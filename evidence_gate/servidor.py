"""Servidor web do Evidence Gate (somente biblioteca padrao).

Uso (na VM, sem porta publica):
    export GURU_MODELO_URL=https://ldgllm.digiti.net.br/v1
    export GURU_MODELO_NOME=glm-5.3
    export GURU_MODELO_API_KEY=...  # do Secret Manager, nunca do repositorio
    python3 -m evidence_gate.servidor

Variaveis opcionais: GURU_HOST (127.0.0.1), GURU_PORTA (8080),
GURU_MODELO_TEMPO (300 s), GURU_MODELO_MAX_TOKENS (8000),
GURU_EVIDENCE_SIMULADO=1 (modelo simulado, sem rede, para demonstracao).

Processamento assincrono, so em memoria: POST /api/verificar devolve 202
e um id de tarefa; a pagina consulta GET /api/tarefa/<id>. Estados:
aguardando, processando, concluida, falha (falha tambem traz veredito
BLOQUEADO). Um trabalhador processa uma tarefa por vez; no maximo
MAX_FILA aguardando e MAX_TAREFAS registradas; resultados expiram em
VALIDADE_TAREFA segundos. Registros nunca contem a fonte,
a pergunta, a resposta nem a chave.
"""

import json
import logging
import os
import queue
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from assistente.servidor import Limitador
from evidence_gate.portao import EntradaInvalida, Portao, validar_entrada

PASTA = Path(__file__).resolve().parent
ESTATICOS = {
    "/": ("pagina.html", "text/html; charset=utf-8"),
    "/index.html": ("pagina.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}
MAX_CORPO = 256 * 1024  # bytes (fonte de ate 60 mil caracteres em UTF-8)
MAX_TAREFAS = 200
VALIDADE_TAREFA = 3600  # segundos
MAX_FILA = 20
CABECALHOS_SEGURANCA = {
    "Content-Security-Policy": (
        "default-src 'none'; script-src 'self'; style-src 'self' "
        "'unsafe-inline'; connect-src 'self'; img-src 'self'; "
        "base-uri 'none'; form-action 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
}

log = logging.getLogger("evidence_gate")


class Tarefas:
    """Fila com um trabalhador e um registro de tarefas com validade."""

    def __init__(self, portao, max_fila=MAX_FILA):
        self.portao = portao
        self.fila = queue.Queue(maxsize=max_fila)
        self.registro = {}
        self.trava = threading.Lock()
        self.trabalhador = threading.Thread(target=self._trabalhar,
                                            daemon=True)
        self.trabalhador.start()

    def _limpar(self):
        agora = time.time()
        with self.trava:
            vencidas = [i for i, t in self.registro.items()
                        if t["estado"] in ("concluida", "falha")
                        and agora - t["criada"] > VALIDADE_TAREFA]
            for i in vencidas:
                del self.registro[i]
            return len(self.registro)

    def criar(self, fonte, pergunta):
        if self._limpar() >= MAX_TAREFAS:
            return None
        ident = secrets.token_urlsafe(16)
        tarefa = {"estado": "aguardando", "etapa": "aguardando",
                  "criada": time.time(), "resultado": None}
        with self.trava:
            self.registro[ident] = tarefa
        try:
            self.fila.put_nowait((ident, fonte, pergunta))
        except queue.Full:
            with self.trava:
                del self.registro[ident]
            return None
        return ident

    def consultar(self, ident):
        with self.trava:
            t = self.registro.get(ident)
            if t is None:
                return None
            return {
                "estado": t["estado"],
                "etapa": t["etapa"],
                "decorrido": round(time.time() - t["criada"], 1),
                "resultado": t["resultado"],
            }

    def _etapa(self, ident, etapa):
        with self.trava:
            self.registro[ident]["etapa"] = etapa

    def _trabalhar(self):
        while True:
            ident, fonte, pergunta = self.fila.get()
            with self.trava:
                self.registro[ident]["estado"] = "processando"
            estado = "concluida"
            try:
                resultado = self.portao.avaliar(
                    fonte, pergunta,
                    progresso=lambda e, i=ident: self._etapa(i, e))
            except Exception as e:  # falha fechada; o trabalhador continua
                log.warning("tarefa falhou: %s", type(e).__name__)
                estado = "falha"
                resultado = {"veredito": "BLOQUEADO",
                             "motivo": "erro interno ao avaliar",
                             "politica_ok": False}
            log.info("tarefa concluida: veredito=%s motivo=%s modelo=%ss",
                     resultado.get("veredito"), resultado.get("motivo"),
                     resultado.get("duracao_modelo", "-"))
            with self.trava:
                t = self.registro[ident]
                t.update(estado=estado, etapa=estado,
                         resultado=resultado)
            self.fila.task_done()


def criar_handler(tarefas, limitador=None):
    limitador = limitador or Limitador()

    class Handler(BaseHTTPRequestHandler):
        server_version = "EvidenceGate/0"

        def log_message(self, formato, *args):  # sem conteudo
            pass

        def _enviar(self, codigo, corpo, tipo):
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            for k, v in CABECALHOS_SEGURANCA.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(corpo)

        def _json(self, codigo, dados):
            corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
            self._enviar(codigo, corpo, "application/json; charset=utf-8")

        def do_GET(self):
            caminho = self.path.split("?", 1)[0]
            if caminho == "/saude":
                return self._json(200, {"ok": True})
            if caminho in ESTATICOS:
                arquivo, tipo = ESTATICOS[caminho]
                return self._enviar(200, (PASTA / arquivo).read_bytes(), tipo)
            if caminho.startswith("/api/tarefa/"):
                estado = tarefas.consultar(caminho[len("/api/tarefa/"):])
                if estado is None:
                    return self._json(404, {"erro": "tarefa nao encontrada"})
                return self._json(200, estado)
            self._json(404, {"erro": "nao encontrado"})

        def do_POST(self):
            if self.path != "/api/verificar":
                return self._json(404, {"erro": "nao encontrado"})
            try:
                tamanho = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                tamanho = 0
            if tamanho <= 0 or tamanho > MAX_CORPO:
                return self._json(413,
                                  {"erro": "pedido vazio ou grande demais"})
            if not limitador.permitir(self.client_address[0]):
                return self._json(429, {"erro": "muitos pedidos; aguarde"})
            try:
                dados = json.loads(self.rfile.read(tamanho).decode("utf-8"))
                fonte, pergunta = dados["fonte"], dados["pergunta"]
                validar_entrada(fonte, pergunta)
            except EntradaInvalida as e:
                return self._json(400, {"erro": str(e)})
            except (ValueError, KeyError, TypeError, UnicodeDecodeError):
                return self._json(400, {"erro": "JSON invalido"})
            ident = tarefas.criar(fonte, pergunta)
            if ident is None:
                return self._json(503, {"erro": "fila cheia; tente depois"})
            self._json(202, {"id": ident})

    return Handler


def criar_modelo():
    if os.environ.get("GURU_EVIDENCE_SIMULADO") == "1":
        from evidence_gate.demo import modelo_simulado
        return modelo_simulado()
    from assistente.modelo import ModeloHTTP
    return ModeloHTTP(
        tempo_limite=float(os.environ.get("GURU_MODELO_TEMPO") or 300),
        max_tokens=int(os.environ.get("GURU_MODELO_MAX_TOKENS") or 8000),
        sem_raciocinio=False,  # sem /no_think e sem parametro de raciocinio
        temperatura=0,
        rejeitar_truncada=True,
        user_agent="GuruDev-EvidenceGate/0.1 (+https://hubstry.dev)",
    )


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    host = os.environ.get("GURU_HOST", "127.0.0.1")
    porta = int(os.environ.get("GURU_PORTA", "8080"))
    modelo = criar_modelo()
    tarefas = Tarefas(Portao(modelo))
    servidor = ThreadingHTTPServer((host, porta), criar_handler(tarefas))
    log.info("Evidence Gate em http://%s:%s (modelo: %r)",
             host, porta, modelo)
    servidor.serve_forever()


if __name__ == "__main__":
    main()
