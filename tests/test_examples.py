"""
Executa cada programa de examples/ pela CLI, como um usuario faria.

Garante que os exemplos citados no README continuem rodando e detecta
regressoes do interpretador que os testes unitarios nao cobrem.
"""

import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
EXEMPLOS = sorted((RAIZ / "examples").glob("*.guru"))

# Exemplos que dependem de recursos ainda nao reimplementados no parser
# atual (instanciacao de classes, encadeamento de metodos, literal de
# objeto). Ficam registrados aqui ate a reimplementacao.
PENDENTES = {
    "calc.guru": "instanciacao de classes e atribuicao a this.atributo",
    "demo_interpreter.guru": "literal de objeto ({}) e instanciacao de classes",
    "hello.guru": "encadeamento de metodos (texto.trim().maiusculo())",
}


@pytest.mark.parametrize("exemplo", EXEMPLOS, ids=lambda p: p.name)
def test_exemplo_executa(exemplo):
    if exemplo.name in PENDENTES:
        pytest.xfail(PENDENTES[exemplo.name])
    resultado = subprocess.run(
        [sys.executable, "-m", "src.cli", "run", str(exemplo)],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        timeout=60,
    )
    saida = resultado.stdout + resultado.stderr
    assert resultado.returncode == 0, saida
    assert "erro em runtime" not in saida, saida
    assert "falha no parsing" not in saida, saida
