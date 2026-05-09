"""
GuruDev Core - Alexandria Library
Biblioteca de Interoperabilidade e Programacao Comparada

Autor: Guilherme Goncalves Machado (Hubstry-DeepTech)
Versao: 0.3.0 | Licenca: MIT
"""

__version__ = "0.3.0"
__author__ = "Guilherme Goncalves Machado"
__email__ = "guilhermemachado.ceo@hubstry.dev"
__company__ = "Hubstry-DeepTech"

from .core.analyzer import LanguageAnalyzer
from .core.translator import CodeTranslator
from .core.type_mapper import TypeMapper
from .core.bridge import LanguageBridge
from .core.quantum_comparator import QuantumComparator, ConsistencyChecker
from .core.quantum_interface import (
    TipoDelegacao,
    verificar_contencao,
    classificar_delegacao,
    classificar_por_nome,
    classificar_todos,
    listar_ausentes,
    resumo_ausentes,
    AUSENTES_QUANTICO,
    PERFIS_CONJECTURAIS,
    PERFIS_ALGORITMOS,
    ResultadoDelegacao,
    ResultadoContencao,
)

__all__ = [
    "LanguageAnalyzer",
    "CodeTranslator",
    "TypeMapper",
    "LanguageBridge",
    "QuantumComparator",
    "ConsistencyChecker",
    "TipoDelegacao",
    "verificar_contencao",
    "classificar_delegacao",
    "classificar_por_nome",
    "classificar_todos",
    "listar_ausentes",
    "resumo_ausentes",
    "AUSENTES_QUANTICO",
    "PERFIS_CONJECTURAIS",
    "PERFIS_ALGORITMOS",
    "ResultadoDelegacao",
    "ResultadoContencao",
]

def get_version():
    return __version__

def get_info():
    return {
        "name": "gurudev-core",
        "version": __version__,
        "author": __author__,
        "company": __company__,
        "url": "https://github.com/marcusvmendes/gurudev-core"
    }
