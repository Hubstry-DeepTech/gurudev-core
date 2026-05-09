"""Testes de integracao: Interpreter + Alexandria + Hermeneutic Dispatch"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.parser import parse
from src.interpreter import Interpreter, GuruDevError
from src.semantic_analyzer import SemanticAnalyzer, SemanticAnalysisResult
from src.ast_nodes import (
    SubescritaLinguagem, DefinicaoFuncao, Bloco, DeclaracaoVariavel,
    Literal, ChamadaFuncao, BlocoCompensacao, BlocoErro, BlocoAlternativa,
)


def _run(code):
    ast = parse(code, debug=False)
    return Interpreter().interpretar(ast)


BLOCK = "$$bloco$$ $$sobrescrita$$ {} $$/sobrescrita$$ " + chr(0xa1) + "codigo!{} !/codigo! $$/bloco$$"


# ============================================================
# SemanticAnalyzer conectado ao Alexandria
# ============================================================
class TestSemanticAnalyzer:

    def test_init_available(self):
        sa = SemanticAnalyzer()
        assert sa.available is True

    def test_analyze_subscrita_javascript(self):
        sa = SemanticAnalyzer()
        sub = SubescritaLinguagem(linguagem="javascript", conteudo="console.log(1)")
        result = sa.analyze_subscrita(sub)
        assert isinstance(result, SemanticAnalysisResult)
        assert result.language_comparison is not None
        assert result.language_comparison.similarity_score > 0.0
        assert len(result.type_mappings) > 0

    def test_analyze_subscrita_rust(self):
        sa = SemanticAnalyzer()
        sub = SubescritaLinguagem(linguagem="rust", conteudo="fn main() {}")
        result = sa.analyze_subscrita(sub)
        assert isinstance(result, SemanticAnalysisResult)
        assert result.language_comparison is not None

    def test_analyze_subscrita_unknown_lang(self):
        sa = SemanticAnalyzer()
        sub = SubescritaLinguagem(linguagem="brainfuck", conteudo="+++")
        result = sa.analyze_subscrita(sub)
        assert len(result.warnings) > 0

    def test_compare_python_javascript(self):
        sa = SemanticAnalyzer()
        comp = sa.get_comparison("Python", "JavaScript")
        assert comp is not None
        assert comp.similarity_score > 0.0

    def test_compare_nonexistent(self):
        sa = SemanticAnalyzer()
        comp = sa.get_comparison("NonLang", "Python")
        assert comp is None


# ============================================================
# Interpreter: Break / Continue
# ============================================================
class TestBreakContinue:

    def test_break_no_while(self):
        i = _run("Int x = 0; while (x < 100) { x = x + 1; if (x == 5) { break; } }")
        assert i.env.get("x") == 5

    def test_continue_no_while(self):
        i = _run("Int s = 0; Int x = 0; while (x < 5) { x = x + 1; if (x == 3) { continue; } s = s + x; }")
        assert i.env.get("s") == 12

    def test_break_no_for(self):
        i = _run("Int s = 0; para (Int i = 0; i < 100; i = i + 1) { s = s + 1; if (s == 7) { break; } }")
        assert i.env.get("s") == 7


# ============================================================
# Interpreter: ExecucaoSerie / Classe
# ============================================================
class TestExecucaoSerie:

    def test_serie_dentro_funcao(self):
        i = _run("funcao f() -> Int { Int x = 0; serie { x = 42; } return x; } Int r = f();")
        assert i.env.get("r") == 42


class TestDefinicaoClasse:

    def test_classe_basica(self):
        i = _run("classe Pessoa { }")
        assert i.env.has("Pessoa")

    def test_classe_com_metodo(self):
        i = _run("classe Calc { funcao dobro(Int x) -> Int { return x * 2; } }")
        calc = i.env.get("Calc")
        assert "dobro" in calc
        assert isinstance(calc["dobro"], DefinicaoFuncao)


# ============================================================
# Alexandria integration
# ============================================================
class TestAlexandriaIntegration:

    def test_interpreter_has_semantic_analyzer(self):
        i = Interpreter()
        assert i.semantic_analyzer is not None
        assert i.semantic_analyzer.available is True

    def test_subscrita_analyses_list(self):
        i = _run("Int x = 1;")
        assert isinstance(i.subscrita_analyses, list)

    def test_semantic_analyzer_caches_comparisons(self):
        sa = SemanticAnalyzer()
        sub1 = SubescritaLinguagem(linguagem="javascript", conteudo="a")
        sub2 = SubescritaLinguagem(linguagem="javascript", conteudo="b")
        r1 = sa.analyze_subscrita(sub1)
        r2 = sa.analyze_subscrita(sub2)
        assert r1.language_comparison is r2.language_comparison


# ============================================================
# Hermeneutic Dispatch
# ============================================================
class TestHermeneuticDispatch:

    def test_literal_nao_anota(self):
        i = _run(BLOCK.format('$$nivel=\"literal\"$$', "Int x = 42;"))
        assert i.env.get("x") == 42
        assert len(i.hermeneutic_log) == 0

    def test_default_anota_nivel(self):
        i = _run(BLOCK.format('$$nivel=\"alegorico\"$$', "Int y = 10;"))
        assert i.env.get("y") == 10
        assert "alegorico" in i.hermeneutic_log

    def test_todos_13_niveis_anotam_exceto_literal(self):
        niveis = ["alegorico", "moral", "mistico", "funcional", "estetico",
                  "holistico", "matematico", "simbolico", "parabolico",
                  "historico", "linguistico"]
        for nivel in niveis:
            i = _run(BLOCK.format(f'$$nivel=\"{nivel}\"$$', "Int v = 1;"))
            assert nivel in i.hermeneutic_log, f"nivel {nivel} nao anotado"

    def test_ontologico_calcula_sv(self):
        i = _run(BLOCK.format('$$nivel=\"ontologico\"$$ $$clave=\"ciencia\"$$ $$ont=\"acao\"$$', "Int z = 7;"))
        assert i.env.get("z") == 7
        assert len(i.significance_vectors) == 1
        sv = i.significance_vectors[0]
        assert len(sv["vector"]) == 5
        assert sv["norm"] > 0
        assert sv["gm_hermeneutica"] == "ontologico"
        assert sv["gm_campo"] == "ciencia"
        assert sv["gm_ontologia"] == "acao"
        assert sv["gm_tempo"] == "compilacao"
        assert sv["gm_paradigma"] == "imperativo"

    def test_ontologico_nao_anota_hermeneutic_log(self):
        i = _run(BLOCK.format('$$nivel=\"ontologico\"$$', "Int w = 1;"))
        assert "ontologico" not in i.hermeneutic_log


# ============================================================
# Significance Vector
# ============================================================
class TestSignificanceVector:

    def test_categorical_hash_deterministico(self):
        h1 = Interpreter._categorical_hash("acao")
        h2 = Interpreter._categorical_hash("acao")
        assert h1 == h2
        assert 0.0 <= h1 <= 1.0

    def test_categorical_hash_none(self):
        assert Interpreter._categorical_hash(None) == 0.0

    def test_categorical_hash_valores_diferentes(self):
        h_a = Interpreter._categorical_hash("acao")
        h_b = Interpreter._categorical_hash("ciencia")
        assert h_a != h_b

    def test_sv_valores_nulos(self):
        bloco = Bloco()
        i = Interpreter()
        sv = i._significance_vector(bloco)
        assert sv["vector"] == [0.0, 0.0, 0.0, 0.0, 0.0]
        assert sv["norm"] == 0.0


# ============================================================
# Subscrita Python merge
# ============================================================
class TestSubscritaMerge:

    def test_python_merge_para_ambiente(self):
        i = Interpreter()
        sub = SubescritaLinguagem(linguagem="python", conteudo="resultado = 42; contador = 10")
        i._x(sub)
        assert i.env.get("resultado") == 42
        assert i.env.get("contador") == 10

    def test_python_nao_merge_dunder(self):
        i = Interpreter()
        sub = SubescritaLinguagem(linguagem="python", conteudo="x = 1; __name__ = 'test'")
        i._x(sub)
        assert i.env.get("x") == 1
        assert not i.env.has("__name__")


# ============================================================
# Compensacao condicional
# ============================================================
class TestCompensacao:

    def test_erro_somente_em_excecao(self):
        erro_body = DeclaracaoVariavel(tipo="Int", nome="fallback", valor=Literal(valor=99))
        erro_block = BlocoErro(corpo=[erro_body])
        comp = BlocoCompensacao(erros=[erro_block])
        bloco = Bloco(codigo=[ChamadaFuncao(nome="indefinida")], compensacao=comp)
        i = Interpreter()
        i._x(bloco)
        assert i.env.get("fallback") == 99

    def test_erro_nao_ativa_sem_excecao(self):
        erro_body = DeclaracaoVariavel(tipo="Int", nome="fallback", valor=Literal(valor=99))
        erro_block = BlocoErro(corpo=[erro_body])
        comp = BlocoCompensacao(erros=[erro_block])
        good_code = DeclaracaoVariavel(tipo="Int", nome="x", valor=Literal(valor=1))
        bloco = Bloco(codigo=[good_code], compensacao=comp)
        i = Interpreter()
        i._x(bloco)
        assert i.env.get("x") == 1
        assert not i.env.has("fallback")

    def test_alternativa_sem_handler_erro(self):
        alt_body = DeclaracaoVariavel(tipo="Int", nome="alt_val", valor=Literal(valor=77))
        alt_block = BlocoAlternativa(corpo=[alt_body])
        comp = BlocoCompensacao(alternativas=[alt_block])
        bloco = Bloco(codigo=[ChamadaFuncao(nome="indefinida")], compensacao=comp)
        i = Interpreter()
        i._x(bloco)
        assert i.env.get("alt_val") == 77

    def test_propaga_sem_compensacao(self):
        bloco = Bloco(codigo=[ChamadaFuncao(nome="indefinida")])
        i = Interpreter()
        try:
            i._x(bloco)
            assert False, "Deveria ter lancado GuruDevError"
        except GuruDevError:
            pass

    def test_erro_tem_precedencia_sobre_alternativa(self):
        erro_body = DeclaracaoVariavel(tipo="Int", nome="from_erro", valor=Literal(valor=1))
        alt_body = DeclaracaoVariavel(tipo="Int", nome="from_alt", valor=Literal(valor=2))
        comp = BlocoCompensacao(
            erros=[BlocoErro(corpo=[erro_body])],
            alternativas=[BlocoAlternativa(corpo=[alt_body])],
        )
        bloco = Bloco(codigo=[ChamadaFuncao(nome="indefinida")], compensacao=comp)
        i = Interpreter()
        i._x(bloco)
        assert i.env.get("from_erro") == 1
        assert not i.env.has("from_alt")
