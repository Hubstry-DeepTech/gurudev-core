"""
Módulo de Tradução Automática de Código

Implementa algoritmos para tradução inteligente de código entre diferentes
linguagens de programação, baseado nos princípios da Programação Comparada.
"""

import re
import ast
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TranslationResult:
    """Resultado de uma tradução de código."""
    source_language: str
    target_language: str
    original_code: str
    translated_code: str
    confidence_score: float
    warnings: List[str]
    notes: List[str]

class CodeTranslator:
    """
    Tradutor automático de código entre linguagens de programação.
    
    Implementa algoritmos de tradução baseados em análise sintática,
    semântica e mapeamento de padrões entre linguagens.
    """
    
    def __init__(self):
        """Inicializa o tradutor."""
        self.translation_patterns = self._load_translation_patterns()
        self.syntax_mappings = self._load_syntax_mappings()
        self.type_mappings = self._load_type_mappings()
        
    def _load_translation_patterns(self) -> Dict[str, Dict[str, str]]:
        """Carrega padrões de tradução entre linguagens."""
        return {
            "python_to_javascript": {
                "def ": "function ",
                "print(": "console.log(",
                "True": "true",
                "False": "false",
                "None": "null",
                "elif ": "else if ",
                "and ": "&& ",
                "or ": "|| ",
                "not ": "!",
                "len(": ".length",
                "range(": "Array.from({length: ",
                "in ": "of ",
                "is ": "===",
                "is not ": "!=="
            },
            "javascript_to_python": {
                "function ": "def ",
                "console.log(": "print(",
                "true": "True",
                "false": "False",
                "null": "None",
                "else if ": "elif ",
                "&& ": "and ",
                "|| ": "or ",
                "!": "not ",
                ".length": "len(",
                "Array.from({length: ": "range(",
                "of ": "in ",
                "===": "is ",
                "!==": "is not ",
                "let ": "",
                "const ": "",
                "var ": ""
            },
            "python_to_rust": {
                "def ": "fn ",
                "print(": "println!(",
                "True": "true",
                "False": "false",
                "None": "None",
                "and ": "&& ",
                "or ": "|| ",
                "not ": "!",
                "len(": ".len()",
                "range(": "0..",
                "in ": "in ",
                "is ": "==",
                "is not ": "!=",
                "return ": "return ",
                "if ": "if ",
                "else:": "} else {",
                "elif ": "} else if ",
                "for ": "for ",
                "while ": "while "
            }
        }
    
    def _load_syntax_mappings(self) -> Dict[str, Dict[str, str]]:
        """Carrega mapeamentos de sintaxe entre linguagens."""
        return {
            "python_to_javascript": {
                "indentation": "braces",
                "colons": "braces",
                "underscore_case": "camelCase",
                "snake_case": "camelCase"
            },
            "javascript_to_python": {
                "braces": "indentation",
                "camelCase": "snake_case",
                "semicolons": "newlines"
            },
            "python_to_rust": {
                "indentation": "braces",
                "colons": "braces",
                "snake_case": "snake_case",
                "underscore_case": "snake_case"
            }
        }
    
    def _load_type_mappings(self) -> Dict[str, Dict[str, str]]:
        """Carrega mapeamentos de tipos entre linguagens."""
        return {
            "python_to_javascript": {
                "int": "number",
                "float": "number",
                "str": "string",
                "bool": "boolean",
                "list": "array",
                "dict": "object",
                "tuple": "array",
                "None": "null"
            },
            "javascript_to_python": {
                "number": "float",
                "string": "str",
                "boolean": "bool",
                "array": "list",
                "object": "dict",
                "null": "None",
                "undefined": "None"
            },
            "python_to_rust": {
                "int": "i32",
                "float": "f64",
                "str": "String",
                "bool": "bool",
                "list": "Vec",
                "dict": "HashMap",
                "tuple": "tuple",
                "None": "Option<T>"
            }
        }
    
    def translate(self, code: str, source_lang: str, target_lang: str, 
                 options: Optional[Dict[str, Any]] = None) -> TranslationResult:
        """
        Traduz código de uma linguagem para outra.
        
        Args:
            code: Código fonte a ser traduzido
            source_lang: Linguagem de origem
            target_lang: Linguagem de destino
            options: Opções de tradução
            
        Returns:
            Objeto TranslationResult com o resultado da tradução
        """
        if options is None:
            options = {}
        
        # Normaliza nomes das linguagens
        source_lang = source_lang.lower()
        target_lang = target_lang.lower()
        
        # Verifica se a tradução é suportada
        translation_key = f"{source_lang}_to_{target_lang}"
        if translation_key not in self.translation_patterns:
            raise ValueError(f"Tradução de {source_lang} para {target_lang} não é suportada")
        
        # Aplica tradução
        translated_code = self._apply_translation(code, translation_key, options)
        
        # Calcula score de confiança
        confidence_score = self._calculate_confidence(code, translated_code, translation_key)
        
        # Gera warnings e notas
        warnings = self._generate_warnings(code, translated_code, source_lang, target_lang)
        notes = self._generate_notes(code, translated_code, source_lang, target_lang)
        
        return TranslationResult(
            source_language=source_lang,
            target_language=target_lang,
            original_code=code,
            translated_code=translated_code,
            confidence_score=confidence_score,
            warnings=warnings,
            notes=notes
        )
    
    def _apply_translation(self, code: str, translation_key: str, 
                          options: Dict[str, Any]) -> str:
        """Aplica a tradução usando padrões e regras."""
        translated_code = code
        
        # Aplica padrões de substituição
        patterns = self.translation_patterns[translation_key]
        for pattern, replacement in patterns.items():
            translated_code = translated_code.replace(pattern, replacement)
        
        # Aplica transformações de sintaxe
        translated_code = self._apply_syntax_transformations(
            translated_code, translation_key, options
        )
        
        # Aplica transformações de estrutura
        translated_code = self._apply_structure_transformations(
            translated_code, translation_key, options
        )
        
        return translated_code
    
    def _apply_syntax_transformations(self, code: str, translation_key: str,
                                    options: Dict[str, Any]) -> str:
        """Aplica transformações de sintaxe específicas."""
        syntax_mappings = self.syntax_mappings.get(translation_key, {})
        
        if "indentation" in syntax_mappings and syntax_mappings["indentation"] == "braces":
            code = self._convert_indentation_to_braces(code)
        
        if "colons" in syntax_mappings and syntax_mappings["colons"] == "braces":
            code = self._convert_colons_to_braces(code)
        
        if "camelCase" in syntax_mappings and syntax_mappings["camelCase"] == "snake_case":
            code = self._convert_camel_case_to_snake_case(code)
        
        return code
    
    def _apply_structure_transformations(self, code: str, translation_key: str,
                                       options: Dict[str, Any]) -> str:
        """Aplica transformações de estrutura de código."""
        lines = code.split('\n')
        transformed_lines = []
        
        for line in lines:
            # Transforma estruturas específicas
            if translation_key == "python_to_javascript":
                line = self._transform_python_to_javascript_structure(line)
            elif translation_key == "javascript_to_python":
                line = self._transform_javascript_to_python_structure(line)
            elif translation_key == "python_to_rust":
                line = self._transform_python_to_rust_structure(line)
            
            transformed_lines.append(line)
        
        return '\n'.join(transformed_lines)
    
    def _transform_python_to_javascript_structure(self, line: str) -> str:
        """Transforma estruturas Python para JavaScript."""
        # Adiciona ponto e vírgula no final
        if line.strip() and not line.strip().endswith(';') and not line.strip().endswith('{'):
            line = line.rstrip() + ';'
        
        # Converte funções
        if line.strip().startswith('def '):
            line = line.replace('def ', 'function ')
            line = line.replace(':', ' {')
        
        # Converte condicionais
        if line.strip().startswith('if ') and line.endswith(':'):
            line = line.replace(':', ' {')
        elif line.strip().startswith('elif ') and line.endswith(':'):
            line = line.replace('elif ', '} else if ')
            line = line.replace(':', ' {')
        elif line.strip() == 'else:':
            line = '} else {'
        
        return line
    
    def _transform_javascript_to_python_structure(self, line: str) -> str:
        """Transforma estruturas JavaScript para Python."""
        # Remove ponto e vírgula
        line = line.rstrip(';')
        
        # Converte funções
        if line.strip().startswith('function '):
            line = line.replace('function ', 'def ')
            line = line.replace(' {', ':')
        
        # Converte condicionais
        if line.strip().startswith('if ') and line.endswith(' {'):
            line = line.replace(' {', ':')
        elif line.strip().startswith('} else if ') and line.endswith(' {'):
            line = line.replace('} else if ', 'elif ')
            line = line.replace(' {', ':')
        elif line.strip() == '} else {':
            line = 'else:'
        
        return line
    
    def _transform_python_to_rust_structure(self, line: str) -> str:
        """Transforma estruturas Python para Rust."""
        # Converte funções
        if line.strip().startswith('def '):
            line = line.replace('def ', 'fn ')
            line = line.replace(':', ' {')
        
        # Converte condicionais
        if line.strip().startswith('if ') and line.endswith(':'):
            line = line.replace(':', ' {')
        elif line.strip().startswith('elif ') and line.endswith(':'):
            line = line.replace('elif ', '} else if ')
            line = line.replace(':', ' {')
        elif line.strip() == 'else:':
            line = '} else {'
        
        # Adiciona ponto e vírgula
        if line.strip() and not line.strip().endswith(';') and not line.strip().endswith('{'):
            line = line.rstrip() + ';'
        
        return line
    
    def _convert_indentation_to_braces(self, code: str) -> str:
        """Converte indentação Python para chaves."""
        lines = code.split('\n')
        result_lines = []
        indent_stack = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                result_lines.append(line)
                continue
            
            # Calcula nível de indentação
            indent_level = len(line) - len(line.lstrip())
            
            # Adiciona chaves de fechamento se necessário
            while indent_stack and indent_stack[-1] > indent_level:
                result_lines.append(' ' * indent_stack.pop() + '}')
            
            # Adiciona chave de abertura se necessário
            if indent_stack and indent_stack[-1] < indent_level:
                result_lines.append(' ' * indent_stack[-1] + '{')
            
            result_lines.append(line)
            indent_stack.append(indent_level)
        
        # Fecha chaves restantes
        while indent_stack:
            result_lines.append(' ' * indent_stack.pop() + '}')
        
        return '\n'.join(result_lines)
    
    def _convert_colons_to_braces(self, code: str) -> str:
        """Converte dois pontos para chaves."""
        lines = code.split('\n')
        result_lines = []
        
        for line in lines:
            if line.strip().endswith(':'):
                result_lines.append(line.replace(':', ' {'))
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _convert_camel_case_to_snake_case(self, code: str) -> str:
        """Converte camelCase para snake_case."""
        import re
        
        def camel_to_snake(name):
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        
        # Aplica a conversão em identificadores
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        for word in words:
            if word != word.lower() and '_' not in word:
                snake_word = camel_to_snake(word)
                code = re.sub(r'\b' + word + r'\b', snake_word, code)
        
        return code
    
    def _calculate_confidence(self, original_code: str, translated_code: str,
                            translation_key: str) -> float:
        """Calcula score de confiança da tradução."""
        confidence = 0.5  # Base
        
        # Bônus por padrões reconhecidos
        patterns = self.translation_patterns[translation_key]
        pattern_matches = 0
        total_patterns = len(patterns)
        
        for pattern in patterns:
            if pattern in original_code:
                pattern_matches += 1
        
        if total_patterns > 0:
            confidence += (pattern_matches / total_patterns) * 0.3
        
        # Bônus por estrutura válida
        if self._is_valid_structure(translated_code, translation_key):
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def _is_valid_structure(self, code: str, translation_key: str) -> bool:
        """Verifica se a estrutura do código traduzido é válida."""
        # Verificações básicas de estrutura
        if translation_key == "python_to_javascript":
            return self._is_valid_javascript_structure(code)
        elif translation_key == "javascript_to_python":
            return self._is_valid_python_structure(code)
        elif translation_key == "python_to_rust":
            return self._is_valid_rust_structure(code)
        
        return True
    
    def _is_valid_javascript_structure(self, code: str) -> bool:
        """Verifica estrutura JavaScript básica."""
        # Verifica se chaves estão balanceadas
        open_braces = code.count('{')
        close_braces = code.count('}')
        return open_braces == close_braces
    
    def _is_valid_python_structure(self, code: str) -> bool:
        """Verifica estrutura Python básica."""
        # Verifica se há dois pontos após estruturas de controle
        lines = code.split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('if ', 'elif ', 'else:', 'def ', 'class ', 'for ', 'while ')):
                if not stripped.endswith(':'):
                    return False
        return True
    
    def _is_valid_rust_structure(self, code: str) -> bool:
        """Verifica estrutura Rust básica."""
        # Verifica se chaves estão balanceadas
        open_braces = code.count('{')
        close_braces = code.count('}')
        return open_braces == close_braces
    
    def _generate_warnings(self, original_code: str, translated_code: str,
                          source_lang: str, target_lang: str) -> List[str]:
        """Gera warnings sobre a tradução."""
        warnings = []
        
        # Verifica se há estruturas não traduzidas
        if source_lang == "python" and target_lang == "javascript":
            if "import " in original_code:
                warnings.append("Imports Python não foram traduzidos para JavaScript")
            if "class " in original_code:
                warnings.append("Classes Python podem precisar de ajustes manuais")
        
        # Verifica complexidade
        if len(original_code.split('\n')) > 50:
            warnings.append("Código longo pode ter tradução incompleta")
        
        return warnings
    
    def _generate_notes(self, original_code: str, translated_code: str,
                       source_lang: str, target_lang: str) -> List[str]:
        """Gera notas sobre a tradução."""
        notes = []
        
        notes.append(f"Tradução automática de {source_lang} para {target_lang}")
        notes.append("Revisão manual recomendada para código em produção")
        
        if source_lang == "python" and target_lang == "javascript":
            notes.append("Considere usar ferramentas como Transcrypt ou Pyodide para melhor compatibilidade")
        
        return notes
    
    def get_supported_translations(self) -> List[Tuple[str, str]]:
        """Retorna lista de traduções suportadas."""
        translations = []
        for key in self.translation_patterns.keys():
            source, target = key.split('_to_')
            translations.append((source, target))
        return translations
    
    def translate_file(self, file_path: str, source_lang: str, target_lang: str,
                      output_path: Optional[str] = None) -> TranslationResult:
        """
        Traduz um arquivo completo.
        
        Args:
            file_path: Caminho do arquivo fonte
            source_lang: Linguagem de origem
            target_lang: Linguagem de destino
            output_path: Caminho do arquivo de saída (opcional)
            
        Returns:
            Objeto TranslationResult com o resultado
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        result = self.translate(code, source_lang, target_lang)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.translated_code)
        
        return result 