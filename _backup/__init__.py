"""
Alexandria: Biblioteca de Interoperabilidade e Programação Comparada

Uma biblioteca pioneira que implementa os princípios da Programação Comparada,
facilitando a interoperabilidade entre linguagens de programação através de
análise comparativa sistemática.

Idealizador e Criador Principal: Guilherme Gonçalves Machado
Desenvolvido com auxílio de Inteligência Artificial (Claude AI)
Empresa: Hubstry-DeepTech

Versão: 0.1.0
Licença: MIT
"""

__version__ = "0.1.0"
__author__ = "Guilherme Gonçalves Machado"
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

# Configuração padrão
DEFAULT_CONFIG = {
    "analysis_depth": "comprehensive",
    "translation_quality": "high",
    "type_mapping_strategy": "semantic",
    "bridge_protocol": "universal"
}

def get_version():
    """Retorna a versão atual da biblioteca."""
    return __version__

def get_info():
    """Retorna informações sobre a biblioteca."""
    return {
        "name": "Alexandria",
        "version": __version__,
        "author": __author__,
        "description": "Biblioteca de Interoperabilidade e Programação Comparada",
        "url": "https://github.com/seu-usuario/alexandria"
    } 