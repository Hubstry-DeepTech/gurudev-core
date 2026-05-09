"""Testes de integracao: Interpreter + Alexandria"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.parser import parse
from src.interpreter import Interpreter, GuruDevError
from src.semantic_analyzer import SemanticAnalyzer, SemanticAnalysisResult
from src.ast_nodes import SubescritaLinguagem, DefinicaoFuncao


def _run(code):
    ast = parse(code, debug=False)
    return Interpreter().interpretar(ast)


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
        assert "int" in result.type_mappings or "str" in result.type_mappings

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
        assert len(comp.paradigm_overlap) >= 0

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
        # s = 1 + 2 + 4 + 5 = 12 (pula 3)
        assert i.env.get("s") == 12

    def test_break_no_for(self):
        i = _run("Int s = 0; para (Int i = 0; i < 100; i = i + 1) { s = s + 1; if (s == 7) { break; } }")
        assert i.env.get("s") == 7


# ============================================================
# Interpreter: ExecucaoSerie
# ============================================================
class TestExecucaoSerie:

    def test_serie_dentro_funcao(self):
        i = _run("funcao f() -> Int { Int x = 0; serie { x = 42; } return x; } Int r = f();")
        assert i.env.get("r") == 42


# ============================================================
# Interpreter: DefinicaoClasse
# ============================================================
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
# Interpreter: Alexandria integration
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
        assert r1.language_comparison is r2.language_comparison  # same cached object
