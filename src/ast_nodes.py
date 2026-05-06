"""
GuruDev® AST Nodes — Versão 1.0.0-alpha
Definição dos nós da Árvore Sintático-Semântica (AST)
Autor: Guilherme Gonçalves Machado

Terminologia linguística:
  - oracao_de_codigo (statement) → OracaoDeCodigo
  - producao_de_valor (expression) → ProducaoDeValor
  - bloco → Bloco (parágrafo computacional)
  - programa → Programa (discurso pragmático)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any


# ============================================================
# BASE
# ============================================================

@dataclass
class Node:
    """Nó base da AST. Todos os nós herdam deste."""
    lineno: int = 0
    # Coordenadas GuruMatrix (preenchidas pelo semantic_analyzer)
    gm_ontologia: Optional[str] = None      # i - categoria aristotélica
    gm_campo: Optional[str] = None          # j - campo do conhecimento
    gm_hermeneutica: Optional[str] = None   # k - nível hermenêutico
    gm_tempo: Optional[str] = None          # t - tempo de execução
    gm_paradigma: Optional[str] = None      # l - paradigma/linguagem


# ============================================================
# PROGRAMA (Discurso Pragmático)
# ============================================================

@dataclass
class Programa(Node):
    """Nó raiz: o programa completo (discurso pragmático)."""
    elementos: List[Node] = field(default_factory=list)


# ============================================================
# BLOCO TRÍPLICE (Parágrafo)
# ============================================================

@dataclass
class Sobrescrita(Node):
    """Metadados semânticos do bloco."""
    contextos: List[str] = field(default_factory=list)   # strings descritivas
    nivel: Optional[str] = None
    raiz: Optional[str] = None
    clave: Optional[str] = None
    ontologia: Optional[str] = None


@dataclass
class SubescritaLinguagem(Node):
    """Código em linguagem estrangeira."""
    linguagem: str = ""
    conteudo: str = ""
    tipo_mapeamento: Optional[str] = None   # automatico, manual, estrito
    conversao: Optional[str] = None


@dataclass
class Bloco(Node):
    """Bloco tríplice: sobrescrita + código + subescritas."""
    sobrescrita: Optional[Sobrescrita] = None
    codigo: List[Node] = field(default_factory=list)          # orações de código
    subescritas: List[SubescritaLinguagem] = field(default_factory=list)
    compensacao: Optional['BlocoCompensacao'] = None
    plastico: Optional['BlocoPlastico'] = None
    modulacao: Optional['BlocoModulacao'] = None


# ============================================================
# BLOCOS DE INTEROPERABILIDADE
# ============================================================

@dataclass
class BlocoErro(Node):
    tipo_erro: Optional[str] = None
    alvo_subescrita: Optional[str] = None
    corpo: List[Node] = field(default_factory=list)


@dataclass
class BlocoDesempenho(Node):
    estrategia: Optional[str] = None
    alvo_subescrita: Optional[str] = None
    corpo: List[Node] = field(default_factory=list)


@dataclass
class BlocoAlternativa(Node):
    condicao: Optional[str] = None
    alvo_subescrita: Optional[str] = None
    corpo: List[Node] = field(default_factory=list)


@dataclass
class BlocoCompensacao(Node):
    erros: List[BlocoErro] = field(default_factory=list)
    desempenhos: List[BlocoDesempenho] = field(default_factory=list)
    alternativas: List[BlocoAlternativa] = field(default_factory=list)


@dataclass
class BlocoPlastico(Node):
    corpo: List[Node] = field(default_factory=list)


@dataclass
class ModulacaoAlvo(Node):
    linguagem: str = ""
    inversao: Optional[str] = None
    corpo: List[Node] = field(default_factory=list)


@dataclass
class BlocoModulacao(Node):
    alvos: List[ModulacaoAlvo] = field(default_factory=list)


# ============================================================
# DECLARAÇÕES E DEFINIÇÕES
# ============================================================

@dataclass
class DeclaracaoVariavel(Node):
    """Ex: String nome = "Guilherme"; """
    tipo: str = ""
    nome: str = ""
    valor: Optional[Node] = None
    caso_gramatical: Optional[str] = None   # VOC, NOM, ACU, etc.
    modificador_acesso: Optional[str] = None  # publico, privado, protegido


@dataclass
class DefinicaoFuncao(Node):
    """Ex: NOM funcao calcular(Int x, Int y) -> Float { ... }"""
    nome: str = ""
    parametros: List['Parametro'] = field(default_factory=list)
    tipo_retorno: Optional[str] = None
    corpo: List[Node] = field(default_factory=list)
    caso_gramatical: Optional[str] = None
    modificador_acesso: Optional[str] = None


@dataclass
class Parametro(Node):
    tipo: str = ""
    nome: str = ""


@dataclass
class DefinicaoClasse(Node):
    """Ex: NOM classe Pessoa extends SerVivo implements Autenticavel { ... }"""
    nome: str = ""
    superclasse: Optional[str] = None
    interfaces: List[str] = field(default_factory=list)
    membros: List[Node] = field(default_factory=list)
    caso_gramatical: Optional[str] = None
    modificador_acesso: Optional[str] = None


# ============================================================
# ORAÇÕES DE CÓDIGO (Statements)
# ============================================================

@dataclass
class Atribuicao(Node):
    """Ex: ACU.variavel = valor; ou nome = valor;"""
    alvo: str = ""
    valor: Optional[Node] = None
    caso_gramatical: Optional[str] = None


@dataclass
class Retorno(Node):
    """Ex: return valor; / retorna valor;"""
    valor: Optional[Node] = None


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


# ============================================================
# CONTROLE DE FLUXO
# ============================================================

@dataclass
class Se(Node):
    """if/se"""
    condicao: Optional[Node] = None
    corpo_verdadeiro: List[Node] = field(default_factory=list)
    corpo_falso: List[Node] = field(default_factory=list)


@dataclass
class Para(Node):
    """for/para (estilo C)"""
    inicializacao: Optional[Node] = None
    condicao: Optional[Node] = None
    incremento: Optional[Node] = None
    corpo: List[Node] = field(default_factory=list)


@dataclass
class ParaCada(Node):
    """for-each: para (Tipo item : colecao)"""
    tipo: str = ""
    variavel: str = ""
    iteravel: str = ""
    corpo: List[Node] = field(default_factory=list)


@dataclass
class Enquanto(Node):
    """while/enquanto"""
    condicao: Optional[Node] = None
    corpo: List[Node] = field(default_factory=list)


# ============================================================
# EXECUÇÃO SÉRIE/PARALELO
# ============================================================

@dataclass
class ExecucaoSerie(Node):
    corpo: List[Node] = field(default_factory=list)


@dataclass
class ExecucaoParalelo(Node):
    corpo: List[Node] = field(default_factory=list)


@dataclass
class ExecucaoEm(Node):
    """em python { ... } / em rust { ... }"""
    linguagem: str = ""
    corpo: List[Node] = field(default_factory=list)


# ============================================================
# PRODUÇÕES DE VALOR (Expressions)
# ============================================================

@dataclass
class ArrayLiteral(Node):
    """Array literal: [expr1, expr2, ...]"""
    elementos: List[Node] = field(default_factory=list)


@dataclass
class Literal(Node):
    """String, Int, Float, Bool literal"""
    valor: Any = None
    tipo: str = ""   # "string", "int", "float", "bool"


@dataclass
class Identificador(Node):
    nome: str = ""


@dataclass
class ChamadaFuncao(Node):
    """Ex: VOC.minhaFuncao(arg1, arg2)"""
    nome: str = ""
    argumentos: List[Node] = field(default_factory=list)
    caso_gramatical: Optional[str] = None


@dataclass
class ChamadaMetodo(Node):
    """Ex: objeto.metodo(arg1, arg2)"""
    objeto: str = ""
    metodo: str = ""
    argumentos: List[Node] = field(default_factory=list)
    caso_gramatical: Optional[str] = None


@dataclass
class OperacaoBinaria(Node):
    """Ex: a + b, x == y, p && q"""
    esquerda: Optional[Node] = None
    operador: str = ""
    direita: Optional[Node] = None


@dataclass
class OperacaoUnaria(Node):
    """Ex: -x, !flag"""
    operador: str = ""
    operando: Optional[Node] = None


@dataclass
class AcessoPropriedade(Node):
    """Ex: GEN.usuario.nome"""
    objeto: str = ""
    propriedade: str = ""
    caso_gramatical: Optional[str] = None
