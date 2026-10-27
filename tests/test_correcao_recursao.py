"""F9 (parte 1): recursao sem fim vira GuruDevError, nao RecursionError.

O limite de profundidade continua o do Python (na main de 27/10/2026, cerca
de 109 niveis de chamada GuruDev com o limite padrao de 1000 frames). So a
classe do erro muda. A checagem do numero de argumentos (F9, parte 2) e uma
decisao separada: ver fuzz/analise-falhas.md.
"""

import pytest

from src.interpreter import GuruDevError, Interpreter
from src.parser import parse

PROFUNDIDADE = (
    "NOM funcao f(Int n) -> Int {{\n"
    "    if (n == 0) {{ return 0; }}\n"
    "    return 1 + f(n - 1);\n"
    "}}\n"
    "escrever(f({n}));\n"
)


def _run(code, interp=None):
    return (interp or Interpreter()).interpretar(parse(code))


def test_recursao_sem_fim_vira_erro_da_linguagem():
    code = "NOM funcao f(Int n) -> Int { return f(n + 1); }\nescrever(f(1));"
    with pytest.raises(GuruDevError, match="profundidade maxima de recursao"):
        _run(code)


def test_recursao_mutua_sem_fim_vira_erro_da_linguagem():
    code = (
        "NOM funcao a(Int n) -> Int { return b(n); }\n"
        "NOM funcao b(Int n) -> Int { return a(n); }\n"
        "escrever(a(1));\n"
    )
    with pytest.raises(GuruDevError, match="profundidade maxima de recursao"):
        _run(code)


def test_recursao_profunda_demais_vira_erro_da_linguagem():
    with pytest.raises(GuruDevError, match="profundidade maxima de recursao"):
        _run(PROFUNDIDADE.format(n=100000))


def test_recursao_rasa_continua_funcionando(capsys):
    _run(PROFUNDIDADE.format(n=50))
    assert capsys.readouterr().out.strip() == "50"


def test_interpretador_continua_utilizavel_depois_do_erro(capsys):
    interp = Interpreter()
    with pytest.raises(GuruDevError):
        _run(
            "NOM funcao f(Int n) -> Int { return f(n + 1); }\nf(1);", interp
        )
    # o ambiente voltou ao escopo global: da para continuar usando
    assert interp.env.pai is None
    _run('escrever("ok");', interp)
    assert capsys.readouterr().out.strip() == "ok"
