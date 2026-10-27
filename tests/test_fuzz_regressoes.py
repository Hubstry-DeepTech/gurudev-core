"""
Testes gerados a partir do fuzzing (fuzz/). Ver fuzz/README.md.

- test_regressao: cada caso mínimo de falha deve terminar sem exceção Python
  vazando (status OK, SINTAXE ou ERRO_GURU). Casos com causa documentada em
  fuzz/analise-falhas.md entram como xfail(strict=True): quando o bug for
  corrigido, o teste passa a "XPASS" e falha, avisando para tirar o xfail.
- test_conformidade: programas válidos do corpus devem manter a mesma saída.

Os programas rodam no executor isolado (processo próprio, timeout, limite de
memória), então um caso que trava ou estoura memória não derruba o pytest.
"""

import json
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DADOS = os.path.join(AQUI, "fuzz_regressoes")
sys.path.insert(0, os.path.join(REPO, "fuzz"))

pytestmark = pytest.mark.skipif(
    os.name != "posix", reason="o executor isolado usa fork (Linux/macOS)"
)

STATUS_ACEITOS = {"OK", "SINTAXE", "ERRO_GURU"}


def _carregar(nome):
    caminho = os.path.join(DADOS, nome)
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def _ler(arquivo):
    with open(os.path.join(DADOS, arquivo), encoding="utf-8") as f:
        return f.read()


CASOS = _carregar("casos.json")
CONFORMIDADE = _carregar("conformidade.json")


@pytest.fixture(scope="module")
def executor():
    from executor import Executor

    with Executor(REPO, timeout=5) as ex:
        yield ex


@pytest.mark.parametrize("caso", CASOS, ids=[c["arquivo"] for c in CASOS])
def test_regressao(caso, executor, request):
    if caso.get("xfail"):
        marca = pytest.mark.xfail(strict=True, reason=caso["xfail"])
        request.applymarker(marca)
    r = executor.rodar(_ler(caso["arquivo"]))
    detalhe = f"{r.get('status')} {r.get('exc', '')} em {r.get('local', '?')}"
    assert r["status"] in STATUS_ACEITOS, detalhe


@pytest.mark.parametrize(
    "caso", CONFORMIDADE, ids=[c["arquivo"] for c in CONFORMIDADE]
)
def test_conformidade(caso, executor):
    r = executor.rodar(_ler(caso["arquivo"]))
    assert r["status"] == "OK", f"{r.get('status')} {r.get('exc', '')}"
    assert r["saida"] == caso["saida"]
