import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.parser import parse
from src.interpreter import Interpreter, GuruDevError


def _run(code):
    ast = parse(code, debug=False)
    return Interpreter().interpretar(ast)


class TestInterpreterBasico:

    def test_declara_funcao(self):
        i = _run("funcao f() -> Int { return 42; }")
        assert i.env.funcs["f"] is not None

    def test_chamada_retorna_valor(self):
        i = _run("funcao f() -> Int { return 42; } Int r = f();")
        assert i.env.get("r") == 42

    def test_soma(self):
        i = _run("funcao soma(Int a, Int b) -> Int { return a + b; } Int r = soma(3, 4);")
        assert i.env.get("r") == 7

    def test_string_concat(self):
        i = _run('funcao saudacao(String nome) -> String { return "oi " + nome; } Int r = saudacao("mundo");')
        assert i.env.get("r") == "oi mundo"


class TestCasoACU:

    def test_acu_congela_variavel(self):
        try:
            _run("ACU.x = 10; ACU.x = 20;")
            assert False, "deveria ter lancado GuruDevError"
        except GuruDevError as e:
            assert "imutavel" in str(e).lower()


class TestCasoVOC:

    def test_voc_rastreia_invocacao(self):
        i = _run('funcao ola() -> String { return "oi"; } VOC.ola();')
        assert "ola" in i.call_log


class TestCasoDAT:

    def test_dat_registra_destinatario(self):
        i = _run("DAT.resultado = 42;")
        assert i.recipients.get("resultado") == 42


class TestCasoINS:

    def test_ins_escopo_isolado(self):
        i = _run("Int x = 1; funcao f() { Int x = 99; } INS.f();")
        assert i.env.get("x") == 1


class TestCasoNOM:

    def test_nom_e_default(self):
        i = _run("NOM funcao f() -> Int { return 7; } Int r = f();")
        assert i.env.get("r") == 7


class TestControleFluxo:

    def test_if_no_interpreter(self):
        i = _run("Int x = 10; if (x == 10) { x = 20; }")
        assert i.env.get("x") == 20

    def test_while_no_interpreter(self):
        i = _run("Int i = 0; while (i < 3) { i = i + 1; }")
        assert i.env.get("i") == 3
