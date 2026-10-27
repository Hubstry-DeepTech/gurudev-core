"""Fronteira entre programas GuruDev e objetos Python do interpretador.

Um programa GuruDev nao deve alcancar atributos internos dos objetos Python
que representam seus valores. Estes testes cobrem as duas regras de
src/interpreter.py (secao "FRONTEIRA COM O PYTHON"):

1. nomes iniciados por "_" sao recusados em propriedade e em metodo;
2. valores basicos (texto, numeros, listas) so expoem os metodos da
   propria linguagem, nunca os do Python.

Os testes negativos usam so acessos de leitura inofensivos; o que importa e
que todos terminem em GuruDevError. Os positivos garantem que o
comportamento legitimo continua igual.
"""

import pytest

from src.instancia import Instancia
from src.interpreter import GuruDevError, Interpreter
from src.parser import parse


def _run(code):
    return Interpreter().interpretar(parse(code))


# ------------------------------------------------------------------
# Regra 1: nomes internos ("_...") recusados
# ------------------------------------------------------------------

NOMES_INTERNOS = [
    'String s = "a"; Object x = s.__class__;',
    'String s = "a"; Object x = s.__doc__;',
    'String s = "a"; Object x = s._qualquer;',
    "Int n = 3; Object x = n.__class__;",
    "Array a = [1]; Object x = a.__class__;",
    'String s = "a"; Object x = s.__sizeof__();',
    "Array a = [1]; Object x = a.__len__();",
]


@pytest.mark.parametrize("codigo", NOMES_INTERNOS)
def test_nome_interno_e_recusado(codigo):
    with pytest.raises(GuruDevError, match="nao permitido"):
        _run(codigo)


def test_nome_interno_recusado_tambem_em_instancia():
    codigo = (
        "NOM classe Caixa { Int v = 1; }\n"
        "Caixa c = Caixa();\n"
        "Object x = c.__class__;"
    )
    with pytest.raises(GuruDevError, match="nao permitido"):
        _run(codigo)


def test_nome_interno_recusado_no_espaco_de_nomes_da_classe():
    codigo = "NOM classe Caixa { Int v = 1; }\nObject x = Caixa.__metodos__;"
    with pytest.raises(GuruDevError, match="nao permitido"):
        _run(codigo)


# ------------------------------------------------------------------
# Regra 2: valores basicos nao expoem atributos nem metodos do Python
# ------------------------------------------------------------------

METODOS_SO_DO_PYTHON = [
    'String s = "aba"; Object x = s.count("a");',
    'String s = "a"; Object x = s.upper();',
    "Array a = [1]; a.append(2);",
    "Array a = [1, 2]; Object x = a.index(2);",
]


@pytest.mark.parametrize("codigo", METODOS_SO_DO_PYTHON)
def test_metodo_python_de_valor_basico_e_recusado(codigo):
    with pytest.raises(GuruDevError, match="nao encontrado"):
        _run(codigo)


PROPRIEDADES_SO_DO_PYTHON = [
    "Int n = 3; Object x = n.real;",
    "Float f = 1.5; Object x = f.imag;",
    'String s = "a"; Object x = s.upper;',
]


@pytest.mark.parametrize("codigo", PROPRIEDADES_SO_DO_PYTHON)
def test_propriedade_python_de_valor_basico_e_recusada(codigo):
    with pytest.raises(GuruDevError, match="nao existe"):
        _run(codigo)


# ------------------------------------------------------------------
# Comportamento legitimo preservado
# ------------------------------------------------------------------


def test_metodos_de_texto_da_linguagem_continuam(capsys):
    _run(
        'String s = "  guru  "; String t = s.trim();'
        " escrever(t.maiusculo());"
    )
    assert capsys.readouterr().out.strip() == "GURU"


def test_metodos_de_lista_da_linguagem_continuam():
    i = _run("Array a = [3]; a.push(1); a.ordenar();")
    assert i.env.get("a") == [1, 3]


def test_atributos_e_metodos_de_instancia_continuam(capsys):
    codigo = (
        "NOM classe Conta {\n"
        "    Int saldo = 10;\n"
        "    NOM funcao dobro() -> Int { return this.saldo * 2; }\n"
        "}\n"
        "Conta c = Conta();\n"
        "escrever(c.saldo);\n"
        "escrever(c.dobro());\n"
    )
    i = _run(codigo)
    assert isinstance(i.env.get("c"), Instancia)
    assert capsys.readouterr().out.split() == ["10", "20"]


def test_propriedade_de_dicionario_continua(capsys):
    interp = Interpreter()
    interp.env.decl("d", {"nome": "Ana"})
    interp.interpretar(parse("escrever(d.nome);"))
    assert capsys.readouterr().out.strip() == "Ana"
