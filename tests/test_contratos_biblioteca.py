"""Contratos executaveis da Biblioteca Padrao (runtime atual).

Cada caso corresponde a uma linha "funciona" ou "use hoje" da secao
"Estado de implementacao" de docs/BIBLIOTECA_PADRAO.md. Se o runtime
deixar de cumprir um contrato, a documentacao precisa ser revista.

Itens documentados e nao implementados (Math, Texto, NOM, VOC.ler)
ficam fora deste teste positivo.
"""

import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent

# (id, codigo GuruDev, entrada padrao, saida esperada)
CONTRATOS = [
    (
        "VOC.escrever",
        'VOC.escrever("ok");\nVOC.escrever("ok");',
        "",
        "ok\nok\n",
    ),
    (
        "VOC.imprimir",
        'VOC.imprimir("ok");\nVOC.imprimir("ok");',
        "",
        "ok\nok\n",
    ),
    (
        "ler_entrada",
        "String n = ler_entrada();\nescrever(n);",
        "Ana\n",
        "Ana\n",
    ),
    ("absoluto", "escrever(absoluto(-5));", "", "5\n"),
    ("raiz", "escrever(raiz(16));", "", "4\n"),
    ("arredondar", "escrever(arredondar(3.7));", "", "4\n"),
    ("tamanho", 'escrever(tamanho("abc"));', "", "3\n"),
    (
        "String.maiusculo",
        'String t = "abc";\nescrever(t.maiusculo());',
        "",
        "ABC\n",
    ),
    (
        "String.minusculo",
        'String t = "ABC";\nescrever(t.minusculo());',
        "",
        "abc\n",
    ),
]


@pytest.mark.parametrize(
    "codigo,entrada,esperado",
    [c[1:] for c in CONTRATOS],
    ids=[c[0] for c in CONTRATOS],
)
def test_contrato_executa(codigo, entrada, esperado, tmp_path):
    arquivo = tmp_path / "contrato.guru"
    arquivo.write_text(codigo + "\n", "utf-8")
    r = subprocess.run(
        [sys.executable, "-m", "src.cli", "run", str(arquivo)],
        cwd=RAIZ,
        input=entrada,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == esperado
