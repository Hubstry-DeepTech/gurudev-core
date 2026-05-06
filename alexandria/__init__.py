"""
GuruDev Core - Alexandria Library
Biblioteca de Interoperabilidade e Programacao Comparada

Autor: Guilherme Goncalves Machado (Hubstry-DeepTech)
Versao: 0.2.0 | Licenca: MIT
"""

__version__ = "0.2.0"
__author__ = "Guilherme Goncalves Machado"
__email__ = "guilhermemachado@hubstry.com"
__company__ = "Hubstry-DeepTech"

from .core.analyzer import LanguageAnalyzer
from .core.translator import CodeTranslator
from .core.type_mapper import TypeMapper
from .core.bridge import LanguageBridge

__all__ = [
    "LanguageAnalyzer",
    "CodeTranslator",
    "TypeMapper",
    "LanguageBridge"
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
