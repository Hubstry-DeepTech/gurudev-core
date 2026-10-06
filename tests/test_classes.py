"""Classe funcional: instanciacao, estado/this e contrato de tipos."""

import pytest

from src.instancia import Instancia
from src.interpreter import GuruDevError, Interpreter
from src.parser import parse

EMPRESA = """
NOM classe Empresa {
    String nome;
    String sede = "indefinida";
    Int empregados = 0;
}
"""


def _run(code):
    return Interpreter().interpretar(parse(code))


# ------------------------------------------------------------------
# 1. Instanciacao
# ------------------------------------------------------------------


def test_instanciacao_produz_instancia_da_classe():
    i = _run(EMPRESA + "Empresa e = Empresa();")
    e = i.env.get("e")
    assert isinstance(e, Instancia)
    assert e.classe == "Empresa"


def test_atributos_declarados_nascem_no_estado_inicial():
    e = _run(EMPRESA + "Empresa e = Empresa();").env.get("e")
    assert e.atributos == {"nome": None, "sede": "indefinida", "empregados": 0}


def test_tipo_de_vem_da_identidade_da_instancia(capsys):
    _run(EMPRESA + "Empresa e = Empresa(); escrever(tipo_de(e));")
    assert capsys.readouterr().out.strip() == "Empresa"


def test_instancias_sao_independentes():
    i = _run(EMPRESA + "Empresa a = Empresa(); Empresa b = Empresa();")
    a, b = i.env.get("a"), i.env.get("b")
    assert a is not b
    assert a.atributos is not b.atributos


def test_classe_inexistente_continua_erro():
    with pytest.raises(GuruDevError):
        _run("Empresa e = Fantasma();")
