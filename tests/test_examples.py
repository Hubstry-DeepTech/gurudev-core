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

# Exemplos que dependem de recursos ainda nao reimplementados
# (encadeamento de metodos, literal de objeto). Ficam registrados aqui
# ate a reimplementacao.
PENDENTES = {
    "demo_interpreter_pendente.guru": "literal de objeto ({})",
    "hello_pendente.guru": "encadeamento de metodos (texto.trim().maiusculo())",
}


def _casos():
    for exemplo in EXEMPLOS:
        motivo = PENDENTES.get(exemplo.name)
        marcas = [pytest.mark.xfail(reason=motivo, strict=True)] if motivo else []
        yield pytest.param(exemplo, id=exemplo.name, marks=marcas)


# strict=True: se um exemplo pendente passar a funcionar, o teste falha
# e obriga a remove-lo de PENDENTES, mantendo a lista fiel ao codigo.
@pytest.mark.parametrize("exemplo", list(_casos()))
def test_exemplo_executa(exemplo):
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
