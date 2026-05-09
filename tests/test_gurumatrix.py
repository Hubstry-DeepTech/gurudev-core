import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.parser import parse

def _parse(code):
    return parse(code, debug=False)

BLOCK = """
 $$bloco$$     $$sobrescrita$$         {attrs}
    $$/sobrescrita$$     \xa1codigo!
        {code}
    !/codigo!
 $$/bloco$$"""

class TestGuruMatrixPopulacao:

    def test_nivel_literal_popula_gm_hermeneutica(self):
        ast = _parse(BLOCK.format(attrs='$$nivel="literal"$$', code=''))
        bloco = ast.elementos[0]
        assert bloco.gm_hermeneutica == 'literal'

    def test_clave_ciencia_popula_gm_campo(self):
        ast = _parse(BLOCK.format(attrs='$$clave="ciencia"$$', code=''))
        bloco = ast.elementos[0]
        assert bloco.gm_campo == 'ciencia'

    def test_ont_acao_popula_gm_ontologia(self):
        ast = _parse(BLOCK.format(attrs='$$ont="acao"$$', code=''))
        bloco = ast.elementos[0]
        assert bloco.gm_ontologia == 'acao'

    def test_sobrescrita_sem_dimensoes_tem_defaults(self):
        ast = _parse(BLOCK.format(attrs='"So contexto"', code=''))
        bloco = ast.elementos[0]
        assert bloco.gm_hermeneutica is None
        assert bloco.gm_campo is None
        assert bloco.gm_ontologia is None
        assert bloco.gm_tempo == 'compilacao'
        assert bloco.gm_paradigma == 'imperativo'

    def test_propagacao_para_filhos(self):
        attrs = '$$nivel="alegorico"$$\n        $$clave="filosofia"$$\n        $$ont="substancia"$$'
        code = 'NOM funcao f(Int x) -> Int { return x; }'
        ast = _parse(BLOCK.format(attrs=attrs, code=code))
        bloco = ast.elementos[0]
        func = bloco.codigo[0]
        assert func.gm_hermeneutica == 'alegorico'
        assert func.gm_campo == 'filosofia'
        assert func.gm_ontologia == 'substancia'

    def test_todos_atributos_juntos(self):
        attrs = '"Teste completo"\n        $$nivel="holistico"$$\n        $$clave="arte"$$\n        $$ont="relacao"$$\n        $$raiz="TEST"$$'
        ast = _parse(BLOCK.format(attrs=attrs, code=''))
        bloco = ast.elementos[0]
        assert bloco.gm_hermeneutica == 'holistico'
        assert bloco.gm_campo == 'arte'
        assert bloco.gm_ontologia == 'relacao'
        assert bloco.gm_tempo == 'compilacao'
        assert bloco.gm_paradigma == 'imperativo'
        assert bloco.sobrescrita is not None
        assert bloco.sobrescrita.raiz == 'TEST'
