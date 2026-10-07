"""Testes da base de conhecimento do Assistente GuruDev.

Executar:  pytest assistente/
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

_spec = importlib.util.spec_from_file_location(
    "gerar_base", AQUI / "gerar_base.py"
)
gerar_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gerar_base)

BASE = json.loads((AQUI / "base_conhecimento.json").read_text("utf-8"))
ESTADOS = {"roda_hoje", "em_reimplementacao", "documental"}


def executa(codigo, tmp_path):
    arquivo = tmp_path / "ficha.guru"
    arquivo.write_text(codigo, "utf-8")
    return subprocess.run(
        [sys.executable, "-m", "src.cli", "run", str(arquivo)],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_base_esta_atualizada():
    """O arquivo publicado corresponde ao que o gerador produz hoje."""
    atual = (AQUI / "base_conhecimento.json").read_text("utf-8")
    assert atual == gerar_base.serializar(gerar_base.gerar()), (
        "base desatualizada: rode python assistente/gerar_base.py"
    )


def test_toda_ficha_tem_origem_e_estado_valido():
    ids = set()
    for ficha in BASE:
        assert ficha["id"] not in ids
        ids.add(ficha["id"])
        assert (RAIZ / ficha["fonte"]).is_file(), ficha["fonte"]
        assert ficha["secao"]
        assert ficha["texto"].strip()
        assert ficha["estado"] in ESTADOS


def test_nenhum_documento_de_negocio():
    for ficha in BASE:
        for proibido in gerar_base.ARQUIVOS_PROIBIDOS:
            assert proibido not in ficha["fonte"], ficha["fonte"]
        for alvo in gerar_base.SECOES_EXCLUIDAS.get(ficha["fonte"], []):
            assert alvo not in ficha["secao"], ficha["secao"]


def test_todos_os_exemplos_estao_na_base():
    na_base = {f["fonte"] for f in BASE if f["tipo"] == "exemplo"}
    exemplos = (RAIZ / "examples").glob("*.guru")
    no_repo = {f"examples/{p.name}" for p in exemplos}
    assert na_base == no_repo


def test_documentacao_nunca_e_roda_hoje():
    """Texto de documentacao declara; so evidencia executavel roda hoje."""
    for ficha in BASE:
        if ficha["tipo"] == "documentacao":
            assert ficha["estado"] != "roda_hoje", ficha["id"]


EXECUTAVEIS = [f for f in BASE if f["estado"] == "roda_hoje"]
PENDENTES = [
    f
    for f in BASE
    if f["tipo"] == "exemplo" and f["estado"] == "em_reimplementacao"
]


@pytest.mark.parametrize(
    "ficha", EXECUTAVEIS, ids=[f["id"] for f in EXECUTAVEIS]
)
def test_roda_hoje_executa(ficha, tmp_path):
    r = executa(ficha["texto"], tmp_path)
    origem = f"{ficha['fonte']} ({ficha['secao']})"
    assert r.returncode == 0, f"{origem}: {r.stderr}"


@pytest.mark.parametrize(
    "ficha", PENDENTES, ids=[f["id"] for f in PENDENTES]
)
def test_em_reimplementacao_ainda_falha(ficha, tmp_path):
    """Se passar a executar, a etiqueta (e PENDENTES) deve ser revista."""
    r = executa(ficha["texto"], tmp_path)
    msg = f"{ficha['fonte']} ja executa: revisar estado"
    assert r.returncode != 0, msg
