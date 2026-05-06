"""
GuruDev® Core — Versão 1.1.0-alpha
Núcleo da linguagem de programação GuruDev®
Autor: Guilherme Gonçalves Machado
Organização: Hubstry-DeepTech

Módulos:
  - lexer: Análise léxica (PLY)
  - parser: Análise sintática (PLY Yacc) → AST
  - ast_nodes: Nós da Árvore Sintático-Semântica
  - symbol_table: Tabela de Símbolos e Ambientes (escopos)
  - interpreter: Interpretador/Executor (tree-walking)
"""

__version__ = "1.1.0-alpha"
__author__ = "Guilherme Gonçalves Machado"
__email__ = "guilhermemachado.ceo@hubstry.dev"

from .parser import parse, build_parser
from .interpreter import interpretar, executar_arquivo, GuruDevInterpreter
from .symbol_table import Ambiente, TabelaDeSimbolos

__all__ = [
    # Parser
    'parse',
    'build_parser',
    # Interpreter
    'interpretar',
    'executar_arquivo',
    'GuruDevInterpreter',
    # Symbol Table
    'Ambiente',
    'TabelaDeSimbolos',
]
