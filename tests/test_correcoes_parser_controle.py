"""Comportamento correto apos as correcoes F1-F4 (ver fuzz/analise-falhas.md).

F1  if com exatamente um elif e sem else derrubava o parser (IndexError).
F2  CASO.obj.prop = valor derrubava o parser (campo ausente na AST).
F3  classe com implements dentro de bloco derrubava o parser.
F4  break/continue/return fora de contexto vazavam sinais internos; e
    break/continue dentro de funcao encerravam, em silencio, o laco de
    quem chamou a funcao.
"""

import pytest

from src.ast_nodes import PropAtribuicao
from src.instancia import Instancia
from src.interpreter import GuruDevError, Interpreter
from src.parser import parse


def _run(code):
    return Interpreter().interpretar(parse(code))


def _saida(capsys, code):
    _run(code)
    return capsys.readouterr().out.split()


# ------------------------------------------------------------------
# F1 — if / elif sem else
# ------------------------------------------------------------------

# Na main, o bug aparecia com EXATAMENTE um elif sem else (em qualquer
# posicao); com dois ou mais, a gramatica usa outra producao (else_opt).
RAMOS = [
    'if (x == 1) {{ escrever("um"); }}',
    'elif (x == 2) {{ escrever("dois"); }}',
    'elif (x == 3) {{ escrever("tres"); }}',
]
SAIDA_POR_X = {1: ["um"], 2: ["dois"], 3: ["tres"], 9: []}


@pytest.mark.parametrize("ultima", [True, False], ids=["ultima", "no_meio"])
@pytest.mark.parametrize("n_elif", [1, 2], ids=["1elif", "2elif"])
@pytest.mark.parametrize("x", [1, 2, 3, 9])
def test_elif_sem_else_executa_o_ramo_certo(capsys, x, n_elif, ultima):
    ramos = " ".join(RAMOS[: 1 + n_elif]).format()
    depois = "" if ultima else 'escrever("fim");\n'
    code = f"Int x = {x};\n{ramos}\n{depois}"
    esperado = SAIDA_POR_X[x] if x <= 1 + n_elif else []
    assert _saida(capsys, code) == esperado + ([] if ultima else ["fim"])


def test_senao_se_sem_senao(capsys):
    code = 'Int x = 2; se (x == 1) { escrever("a"); } senao_se (x == 2) ' \
        '{ escrever("b"); }'
    assert _saida(capsys, code) == ["b"]


def test_elif_com_else_continua_igual(capsys):
    code = (
        "Int x = 5;\n"
        'if (x == 1) { escrever("um"); } elif (x == 2) { escrever("dois"); }'
        ' else { escrever("outro"); }\n'
    )
    assert _saida(capsys, code) == ["outro"]


# ------------------------------------------------------------------
# F2 — atribuicao de propriedade com caso gramatical
# ------------------------------------------------------------------

CAIXA = "NOM classe Caixa { Int v = 1; }\nCaixa c = Caixa();\n"


def test_atribuicao_com_caso_altera_a_instancia():
    c = _run(CAIXA + "ACU.c.v = 5;").env.get("c")
    assert isinstance(c, Instancia)
    assert c.atributos["v"] == 5


def test_caso_gramatical_fica_registrado_na_ast():
    no = parse("ACU.c.v = 5;").elementos[0]
    assert isinstance(no, PropAtribuicao)
    assert (no.caso_gramatical, no.objeto, no.propriedade) == (
        "ACU", "c", "v"
    )


# ------------------------------------------------------------------
# F3 — classe com implements dentro de bloco
# ------------------------------------------------------------------


def test_implements_dentro_de_bloco():
    code = (
        "[bloco]\n"
        "¡codigo!\n"
        "NOM classe Pessoa implements Autenticavel { String nome; }\n"
        "Pessoa p = Pessoa();\n"
        "!/codigo!\n"
        "[/bloco]\n"
    )
    p = _run(code).env.get("p")
    assert isinstance(p, Instancia)
    assert p.classe == "Pessoa"


# ------------------------------------------------------------------
# F4 — break / continue / return fora de contexto
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "code, mensagem",
    [
        ("break;", "break fora de laco"),
        ("continua;", "continue fora de laco"),
        ("return;", "return fora de funcao"),
        ("return 3;", "return fora de funcao"),
    ],
)
def test_sinal_no_nivel_do_programa_vira_erro_da_linguagem(code, mensagem):
    with pytest.raises(GuruDevError, match=mensagem):
        _run(code)


@pytest.mark.parametrize(
    "corpo, mensagem",
    [("break;", "break fora de laco"), ("continua;", "continue fora de laco")],
)
def test_break_em_funcao_nao_encerra_o_laco_de_quem_chama(corpo, mensagem):
    code = (
        "NOM funcao f() { " + corpo + " }\n"
        "Int i = 0;\n"
        "while (i < 3) { i = i + 1; f(); escrever(i); }\n"
    )
    # antes: o laco do chamador terminava em silencio
    with pytest.raises(GuruDevError, match=mensagem):
        _run(code)


def test_break_em_metodo_nao_encerra_o_laco_de_quem_chama():
    code = (
        "NOM classe K { NOM funcao m() { break; } }\n"
        "K k = K();\n"
        "Int i = 0;\n"
        "while (i < 3) { i = i + 1; k.m(); }\n"
    )
    with pytest.raises(GuruDevError, match="break fora de laco"):
        _run(code)


def test_controle_legitimo_continua_igual(capsys):
    code = (
        "NOM funcao primeiro_par(Array a) -> Int {\n"
        "    for (Int x : a) {\n"
        "        if (x % 2 == 1) { continua; }\n"
        "        return x;\n"
        "    }\n"
        "    return -1;\n"
        "}\n"
        "escrever(primeiro_par([1, 3, 4, 6]));\n"
        "Int i = 0;\n"
        "while (true) { i = i + 1; if (i == 3) { break; } }\n"
        "escrever(i);\n"
    )
    assert _saida(capsys, code) == ["4", "3"]
