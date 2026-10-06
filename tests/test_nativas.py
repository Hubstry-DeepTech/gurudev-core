"""Funcoes nativas, metodos de String/Array e comportamentos restaurados."""

from src.parser import parse
from src.interpreter import Interpreter


def _run(code):
    return Interpreter().interpretar(parse(code))


def test_escrever_imprime(capsys):
    _run('escrever("Ola", 42, verdadeiro);')
    assert capsys.readouterr().out.strip() == "Ola 42 verdadeiro"


def test_metodo_de_string(capsys):
    _run('String s = "gurudev"; escrever(s.maiusculo());')
    assert capsys.readouterr().out.strip() == "GURUDEV"


def test_metodo_de_array(capsys):
    _run('Array a = [3, 1, 2]; a.ordenar(); escrever(a.juntar("-"));')
    assert capsys.readouterr().out.strip() == "1-2-3"


def test_texto_mais_numero(capsys):
    _run('Int n = 7; escrever("n = " + n);')
    assert capsys.readouterr().out.strip() == "n = 7"


def test_recursao_encontra_funcao_externa():
    i = _run(
        "funcao fat(Int n) -> Int { se (n <= 1) { return 1; } return n * fat(n - 1); }"
        "Int r = fat(5);"
    )
    assert i.env.get("r") == 120


def test_cadeia_senao_se(capsys):
    _run(
        'Int nota = 75; se (nota >= 90) { escrever("A"); } '
        'senao_se (nota >= 70) { escrever("B"); } senao { escrever("F"); }'
    )
    assert capsys.readouterr().out.strip() == "B"


def test_parametro_opcional(capsys):
    _run(
        'funcao saudar(String nome, String saudacao = "Ola") '
        '{ escrever(saudacao + ", " + nome + "!"); } saudar("Mundo");'
    )
    assert capsys.readouterr().out.strip() == "Ola, Mundo!"
