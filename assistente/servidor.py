"""Servidor web minimo do Assistente GuruDev (somente biblioteca padrao).

Uso:
    GURU_MODELO_URL=http://127.0.0.1:11434/v1 GURU_MODELO_NOME=qwen3:1.7b \\
        python -m assistente.servidor

Variaveis opcionais: GURU_HOST (padrao 127.0.0.1), GURU_PORTA (8000).

Protecoes: limite de tamanho do pedido, limite de pedidos por IP,
fila de um pedido por vez (o modelo roda em CPU) e registro sem o
conteudo das perguntas.
"""

import json
import logging
import os
import threading
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from assistente.modelo import ErroModelo, ModeloHTTP
from assistente.nucleo import Assistente

MAX_CORPO = 4096  # bytes
PEDIDOS_POR_MINUTO = 10
PAGINA = Path(__file__).resolve().parent / "pagina.html"

log = logging.getLogger("assistente")


class Limitador:
    def __init__(self, por_minuto=PEDIDOS_POR_MINUTO):
        self.por_minuto = por_minuto
        self.historico = defaultdict(deque)
        self.trava = threading.Lock()

    def permitir(self, chave):
        agora = time.monotonic()
        with self.trava:
            fila = self.historico[chave]
            while fila and agora - fila[0] > 60:
                fila.popleft()
            if len(fila) >= self.por_minuto:
                return False
            fila.append(agora)
            return True


def criar_handler(assistente, limitador=None):
    limitador = limitador or Limitador()
    fila = threading.Lock()  # um pedido ao modelo por vez

    class Handler(BaseHTTPRequestHandler):
        server_version = "AssistenteGuruDev/0"

        def log_message(self, formato, *args):  # sem conteudo
            pass

        def _json(self, codigo, dados):
            corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)

        def do_GET(self):
            if self.path == "/saude":
                return self._json(200, {"ok": True})
            if self.path in ("/", "/index.html"):
                corpo = PAGINA.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                return self.wfile.write(corpo)
            self._json(404, {"erro": "nao encontrado"})

        def do_POST(self):
            if self.path != "/api/perguntar":
                return self._json(404, {"erro": "nao encontrado"})
            tamanho = int(self.headers.get("Content-Length") or 0)
            if tamanho <= 0 or tamanho > MAX_CORPO:
                return self._json(413, {"erro": "pedido grande demais"})
            if not limitador.permitir(self.client_address[0]):
                return self._json(
                    429, {"erro": "muitos pedidos; tente em um minuto"}
                )
            try:
                dados = json.loads(self.rfile.read(tamanho).decode("utf-8"))
                pergunta = str(dados.get("pergunta", ""))
            except (ValueError, AttributeError):
                return self._json(400, {"erro": "JSON invalido"})
            inicio = time.monotonic()
            try:
                with fila:
                    resposta = assistente.responder(pergunta)
            except ErroModelo as e:
                log.warning("erro de modelo: %s", e)
                return self._json(503, {"erro": "modelo indisponivel"})
            duracao = round(time.monotonic() - inicio, 2)
            log.info(
                "pergunta respondida em %ss; fontes=%s; politica=%s",
                duracao,
                [f["id"] for f in resposta.fontes],
                (resposta.politica or {}).get("regra", "-"),
            )
            saida = resposta.como_dict()
            saida["duracao"] = duracao
            self._json(200, saida)

    return Handler


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    host = os.environ.get("GURU_HOST", "127.0.0.1")
    porta = int(os.environ.get("GURU_PORTA", "8000"))
    assistente = Assistente(ModeloHTTP())
    servidor = ThreadingHTTPServer((host, porta), criar_handler(assistente))
    log.info("Assistente GuruDev em http://%s:%s", host, porta)
    servidor.serve_forever()


if __name__ == "__main__":
    main()
