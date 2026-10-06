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


# ------------------------------------------------------------------
# 3. Contrato de tipos dos atributos
# ------------------------------------------------------------------

EMPRESA_TIPADA = """
NOM classe Empresa {
    String sede;
    Int empregados;
    Float faturamento;
    Bool ativa;
    Array socios;
    Pais pais;
    NOM funcao iniciar(String s, Int n) {
        this.sede = s;
        this.empregados = n;
    }
}
"""


def test_tipos_validos_passam():
    i = _run(
        EMPRESA_TIPADA
        + 'Empresa e = Empresa("Brasil", 100);'
        + " e.faturamento = 1.5; e.ativa = verdadeiro; e.socios = [1, 2];"
    )
    e = i.env.get("e")
    assert e.atributos["empregados"] == 100
    assert e.atributos["socios"] == [1, 2]


def test_float_aceita_inteiro():
    e = _run(EMPRESA_TIPADA + 'Empresa e = Empresa("Brasil", 1); e.faturamento = 10;')
    assert e.env.get("e").atributos["faturamento"] == 10


@pytest.mark.parametrize(
    "atribuicao",
    [
        'e.empregados = "cem";',  # Int recebe String
        "e.empregados = 1.5;",  # Int recebe Float
        "e.empregados = verdadeiro;",  # Int recebe Bool
        "e.sede = 42;",  # String recebe Int
        'e.faturamento = "alto";',  # Float recebe String
        "e.ativa = 1;",  # Bool recebe Int
        'e.socios = "Ana";',  # Array recebe String
    ],
)
def test_tipo_incompativel_falha(atribuicao):
    with pytest.raises(GuruDevError, match="tipo incompativel"):
        _run(EMPRESA_TIPADA + 'Empresa e = Empresa("Brasil", 1); ' + atribuicao)


def test_construtor_com_tipo_incompativel_falha():
    with pytest.raises(GuruDevError, match="Empresa.empregados e Int"):
        _run(EMPRESA_TIPADA + 'Empresa e = Empresa("Brasil", "cem");')


def test_valor_inicial_declarado_tambem_e_verificado():
    with pytest.raises(GuruDevError, match="tipo incompativel"):
        _run('NOM classe E { Int n = "cem"; } E e = E();')


def test_falha_e_deterministica():
    mensagens = set()
    for _ in range(3):
        with pytest.raises(GuruDevError) as exc:
            _run(
                EMPRESA_TIPADA
                + 'Empresa e = Empresa("Brasil", 1); e.empregados = "cem";'
            )
        mensagens.add(str(exc.value))
    assert mensagens == {"tipo incompativel: Empresa.empregados e Int, recebeu String"}


def test_tipo_de_usuario_nao_e_verificado_nesta_etapa():
    e = _run(EMPRESA_TIPADA + 'Empresa e = Empresa("Brasil", 1); e.pais = "qualquer";')
    assert e.env.get("e").atributos["pais"] == "qualquer"


def test_atributo_nao_preenchido_fica_vazio_sem_erro_de_tipo():
    e = _run(EMPRESA_TIPADA + 'Empresa e = Empresa("Brasil", 1);').env.get("e")
    assert e.atributos["faturamento"] is None
    assert e.atributos["ativa"] is None
