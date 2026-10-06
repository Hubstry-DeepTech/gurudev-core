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


# ------------------------------------------------------------------
# 2. Estado da instancia / this
# ------------------------------------------------------------------

EMPRESA_COM_CONSTRUTOR = """
NOM classe Empresa {
    String nome;
    String sede;
    NOM funcao iniciar(String n, String s) {
        this.nome = n;
        this.sede = s;
    }
    NOM funcao mudar_sede(String s) {
        isto.sede = s;
    }
    NOM funcao descricao() -> String {
        return this.nome + " (" + this.sede + ")";
    }
}
"""


def test_ciclo_completo_iniciar_this_leitura(capsys):
    # Empresa(...) -> iniciar(...) -> this.sede = "Brasil" -> e.sede
    _run(
        EMPRESA_COM_CONSTRUTOR
        + 'Empresa e = Empresa("Acme", "Brasil"); escrever(e.sede);'
    )
    assert capsys.readouterr().out.strip() == "Brasil"


def test_metodo_le_estado_via_this(capsys):
    _run(
        EMPRESA_COM_CONSTRUTOR
        + 'Empresa e = Empresa("Acme", "Brasil"); escrever(e.descricao());'
    )
    assert capsys.readouterr().out.strip() == "Acme (Brasil)"


def test_isto_e_alias_de_this_no_mesmo_objeto(capsys):
    _run(
        EMPRESA_COM_CONSTRUTOR
        + 'Empresa e = Empresa("Acme", "Brasil"); e.mudar_sede("Portugal");'
        + " escrever(e.descricao());"
    )
    assert capsys.readouterr().out.strip() == "Acme (Portugal)"


def test_atribuicao_externa_a_propriedade(capsys):
    _run(
        EMPRESA_COM_CONSTRUTOR
        + 'Empresa e = Empresa("Acme", "Brasil"); e.sede = "Chile"; escrever(e.sede);'
    )
    assert capsys.readouterr().out.strip() == "Chile"


def test_estado_nao_vaza_entre_instancias(capsys):
    _run(
        EMPRESA_COM_CONSTRUTOR
        + 'Empresa a = Empresa("A", "Brasil"); Empresa b = Empresa("B", "Chile");'
        + " escrever(a.sede, b.sede);"
    )
    assert capsys.readouterr().out.strip() == "Brasil Chile"


def test_atributo_inexistente_e_erro():
    with pytest.raises(GuruDevError):
        _run(
            EMPRESA_COM_CONSTRUTOR + 'Empresa e = Empresa("A", "B"); escrever(e.cnpj);'
        )


def test_metodo_inexistente_e_erro():
    with pytest.raises(GuruDevError):
        _run(EMPRESA_COM_CONSTRUTOR + 'Empresa e = Empresa("A", "B"); e.voar();')
