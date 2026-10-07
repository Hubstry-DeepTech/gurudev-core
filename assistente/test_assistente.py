"""Testes do Assistente V0 contra os roteiros de docs/DEMO_ROTEIROS.md.

O modelo e simulado: os testes verificam a engrenagem deterministica
(recuperacao, politica, execucao, fontes, servidor e cliente HTTP).
"""

import json
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from assistente import executor, politica
from assistente.modelo import ErroModelo, ModeloHTTP, ModeloSimulado
from assistente.nucleo import Assistente, extrair_codigo
from assistente.recuperacao import Buscador, carregar_base
from assistente.servidor import Limitador, criar_handler

BASE = carregar_base()
BUSCADOR = Buscador(BASE)
CODIGO_ROTEIRO = {
    f["secao"].split(" > ")[-1][:3]: f["texto"]
    for f in BASE
    if f["tipo"] == "codigo_roteiro"
}


def resposta_com_codigo(codigo, texto="Segue o codigo."):
    return f"{texto}\n\n```guru\n{codigo}\n```\n"


def assistente_com(resposta):
    return Assistente(ModeloSimulado(resposta), buscador=BUSCADOR)


# ---------------------------------------------------------------- busca


def fontes(pergunta):
    return [f["fonte"] for f in BUSCADOR.buscar(pergunta)]


def test_r01_recupera_apresentacao():
    secoes = [f["secao"] for f in BUSCADOR.buscar("O que é a GuruDev?")]
    assert any(s.endswith("Em uma frase") for s in secoes)
    assert any(s.endswith("1. Introdução") for s in secoes)


def test_r05_recupera_gurumatrix():
    assert "docs/GURU_MATRIX5D.md" in fontes("O que é a GuruMatrix 5D?")


@pytest.mark.parametrize(
    "pergunta", ["gurudev", "Explique a GuruDev", "Fale sobre a GuruDev"]
)
def test_pergunta_generica_cai_na_apresentacao(pergunta):
    secoes = [f["secao"] for f in BUSCADOR.buscar(pergunta)]
    assert any(s.endswith("Em uma frase") for s in secoes)


def test_r07_recupera_ficha_em_reimplementacao():
    fichas = BUSCADOR.buscar("Posso usar texto.trim().maiusculo() em GuruDev?")
    assert any(f["estado"] == "em_reimplementacao" for f in fichas)


def test_pergunta_sem_relacao_nao_inventa_fontes():
    assert BUSCADOR.buscar("xyzzy qwerty") == []


# ------------------------------------------------- roteiros executaveis

ESPERADO = {
    "R02": "Ola, mundo!",
    "R03": "5! = 120",
    "R04": "Ola, eu sou Ana e tenho 30 anos.",
    "R06": "Bloco ontologico ativo: GuruDev",
    "R07": "GURUDEV",
}


@pytest.mark.parametrize("roteiro", sorted(ESPERADO))
def test_roteiro_executavel(roteiro):
    codigo = CODIGO_ROTEIRO[roteiro]
    r = assistente_com(resposta_com_codigo(codigo)).responder(
        "Escreva um programa em GuruDev"
    )
    assert r.codigo == codigo
    assert r.execucao["ok"], r.execucao["erro"]
    assert ESPERADO[roteiro] in r.execucao["saida"]
    assert r.politica is None
    assert r.fontes and all("estado" in f for f in r.fontes)


def test_instrucoes_e_fichas_chegam_ao_modelo():
    modelo = ModeloSimulado("Resposta.")
    Assistente(modelo, buscador=BUSCADOR).responder("O que é a GuruDev?")
    sistema, usuario = modelo.recebido[0]
    assert "estado" in sistema["content"]
    assert "FICHAS:" in usuario["content"]
    assert "PERGUNTA: O que é a GuruDev?" in usuario["content"]


# --------------------------------------------------- politica (R08)

SUBESCRITA = """escrever("antes");
$$bloco$$
¡codigo!
escrever("dentro");
!/codigo!
$$subescritas$$
¿python?
print("python executado")
?/python?
$$/subescritas$$
$$/bloco$$"""


def test_r08_subescrita_nao_executa(monkeypatch):
    def proibido(*a, **k):
        raise AssertionError("o executor nao deveria ser chamado")

    monkeypatch.setattr(executor, "executar", proibido)
    r = assistente_com(
        resposta_com_codigo(SUBESCRITA, "Executei o codigo com sucesso.")
    ).responder("Escreva um programa GuruDev com trecho em Python e execute")
    assert r.execucao is None
    assert r.politica["regra"] == "POL-01"
    assert "¿python?" in r.codigo


@pytest.mark.parametrize(
    "codigo",
    [
        '¿python?\nprint(1)\n?/python?',
        "[subescritas]\n¿rust?\nfn x(){}\n?/rust?\n[/subescritas]",
        "$$subescritas$$\n$$/subescritas$$",
        "¿ javascript ?\nalert(1)\n? / javascript ?",
    ],
)
def test_pol01_detecta_variantes(codigo):
    assert politica.avaliar_codigo(codigo).regra == "POL-01"


def test_executor_recusa_subescrita_mesmo_chamado_direto():
    r = executor.executar('¿python?\nimport os\n?/python?')
    assert r["executado"] is False
    assert r["erro"].startswith("POL-01")


def test_pol03_pergunta_longa_recusada():
    r = assistente_com("nao deveria ser chamado").responder(
        "a" * (politica.MAX_PERGUNTA + 1)
    )
    assert r.politica["regra"] == "POL-03"
    assert r.fontes == []


def test_pol03_tempo_limite():
    r = executor.executar(
        "Int i = 0;\nwhile (verdadeiro) { i = i + 1; }", tempo_limite=2
    )
    assert r["ok"] is False
    assert "tempo limite" in r["erro"]


def test_sem_codigo_sem_execucao():
    r = assistente_com("A GuruDev e uma linguagem.").responder(
        "O que é a GuruDev?"
    )
    assert r.codigo == "" and r.execucao is None


def test_extrair_codigo_pega_primeiro_bloco():
    texto = "a\n```guru\nescrever(1);\n```\nb\n```\nescrever(2);\n```"
    assert extrair_codigo(texto) == "escrever(1);"


# ------------------------------------------------------ cliente HTTP


class _ModeloFalso(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        tamanho = int(self.headers["Content-Length"])
        pedido = json.loads(self.rfile.read(tamanho))
        ultima = pedido["messages"][-1]["content"]
        conteudo = f"<think>pensando</think>modelo={pedido['model']}"
        if ultima.endswith("/no_think"):
            conteudo += " sem_raciocinio"
        corpo = json.dumps(
            {"choices": [{"message": {"content": conteudo}}]}
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


@pytest.fixture
def servidor_local():
    criados = []

    def iniciar(handler):
        s = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=s.serve_forever, daemon=True).start()
        criados.append(s)
        return f"http://127.0.0.1:{s.server_address[1]}"

    yield iniciar
    for s in criados:
        s.shutdown()


def test_modelo_http_compativel_openai(servidor_local):
    url = servidor_local(_ModeloFalso)
    modelo = ModeloHTTP(url=url + "/v1", nome="qwen3:1.7b")
    assert modelo.gerar([{"role": "user", "content": "oi"}]) == (
        "modelo=qwen3:1.7b"
    )


def test_modelo_http_sem_raciocinio(servidor_local):
    url = servidor_local(_ModeloFalso)
    modelo = ModeloHTTP(url=url + "/v1", nome="m", sem_raciocinio=True)
    resposta = modelo.gerar([{"role": "user", "content": "oi"}])
    assert resposta == "modelo=m sem_raciocinio"


def test_modelo_http_exige_configuracao(monkeypatch):
    monkeypatch.delenv("GURU_MODELO_URL", raising=False)
    monkeypatch.delenv("GURU_MODELO_NOME", raising=False)
    with pytest.raises(ErroModelo):
        ModeloHTTP()


# ------------------------------------------------------------ servidor


def post(url, dados):
    pedido = urllib.request.Request(
        url + "/api/perguntar",
        data=json.dumps(dados).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(pedido, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_servidor_responde_com_execucao_e_fontes(servidor_local):
    assistente = assistente_com(resposta_com_codigo(CODIGO_ROTEIRO["R02"]))
    url = servidor_local(criar_handler(assistente))
    status, d = post(url, {"pergunta": "Escreva um Olá Mundo em GuruDev"})
    assert status == 200
    assert d["execucao"]["ok"] and "Ola, mundo!" in d["execucao"]["saida"]
    assert d["fontes"] and "duracao" in d
    with urllib.request.urlopen(url + "/", timeout=10) as r:
        assert b"Assistente GuruDev" in r.read()


def test_servidor_limita_pedidos(servidor_local):
    handler = criar_handler(
        assistente_com("ok"), limitador=Limitador(por_minuto=2)
    )
    url = servidor_local(handler)
    codigos = [post(url, {"pergunta": "O que é a GuruDev?"})[0]
               for _ in range(3)]
    assert codigos == [200, 200, 429]
