"""
Módulo de Mapeamento de Tipos Cross-Language

Implementa algoritmos para mapeamento inteligente de tipos entre diferentes
linguagens de programação, considerando semântica e contexto.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class TypeCategory(Enum):
    """Categorias de tipos para mapeamento."""
    PRIMITIVE = "primitive"
    COMPOSITE = "composite"
    REFERENCE = "reference"
    GENERIC = "generic"
    FUNCTIONAL = "functional"
    SPECIAL = "special"

@dataclass
class TypeMapping:
    """Mapeamento de tipo entre linguagens."""
    source_type: str
    target_type: str
    confidence: float
    notes: List[str]
    alternatives: List[str]

@dataclass
class TypeInfo:
    """Informações detalhadas sobre um tipo."""
    name: str
    category: TypeCategory
    size: Optional[int]
    nullable: bool
    mutable: bool
    default_value: Any
    constraints: List[str]

class TypeMapper:
    """
    Mapeador de tipos entre linguagens de programação.
    
    Implementa algoritmos para mapeamento inteligente considerando
    semântica, contexto e características específicas de cada linguagem.
    """
    
    def __init__(self):
        """Inicializa o mapeador de tipos."""
        self.type_definitions = self._load_type_definitions()
        self.mapping_rules = self._load_mapping_rules()
        self.context_rules = self._load_context_rules()
        
    def _load_type_definitions(self) -> Dict[str, Dict[str, TypeInfo]]:
        """Carrega definições de tipos para cada linguagem."""
        return {
            "python": {
                "int": TypeInfo("int", TypeCategory.PRIMITIVE, None, False, False, 0, []),
                "float": TypeInfo("float", TypeCategory.PRIMITIVE, None, False, False, 0.0, []),
                "str": TypeInfo("str", TypeCategory.PRIMITIVE, None, False, False, "", []),
                "bool": TypeInfo("bool", TypeCategory.PRIMITIVE, None, False, False, False, []),
                "list": TypeInfo("list", TypeCategory.COMPOSITE, None, True, True, [], []),
                "dict": TypeInfo("dict", TypeCategory.COMPOSITE, None, True, True, {}, []),
                "tuple": TypeInfo("tuple", TypeCategory.COMPOSITE, None, False, False, (), []),
                "None": TypeInfo("None", TypeCategory.SPECIAL, None, True, False, None, []),
                "object": TypeInfo("object", TypeCategory.REFERENCE, None, True, True, None, [])
            },
            "javascript": {
                "number": TypeInfo("number", TypeCategory.PRIMITIVE, 8, False, False, 0, []),
                "string": TypeInfo("string", TypeCategory.PRIMITIVE, None, False, False, "", []),
                "boolean": TypeInfo("boolean", TypeCategory.PRIMITIVE, 1, False, False, false, []),
                "array": TypeInfo("array", TypeCategory.COMPOSITE, None, True, True, [], []),
                "object": TypeInfo("object", TypeCategory.COMPOSITE, None, True, True, {}, []),
                "null": TypeInfo("null", TypeCategory.SPECIAL, None, True, False, null, []),
                "undefined": TypeInfo("undefined", TypeCategory.SPECIAL, None, True, False, undefined, [])
            },
            "rust": {
                "i8": TypeInfo("i8", TypeCategory.PRIMITIVE, 1, False, False, 0, []),
                "i16": TypeInfo("i16", TypeCategory.PRIMITIVE, 2, False, False, 0, []),
                "i32": TypeInfo("i32", TypeCategory.PRIMITIVE, 4, False, False, 0, []),
                "i64": TypeInfo("i64", TypeCategory.PRIMITIVE, 8, False, False, 0, []),
                "u8": TypeInfo("u8", TypeCategory.PRIMITIVE, 1, False, False, 0, []),
                "u16": TypeInfo("u16", TypeCategory.PRIMITIVE, 2, False, False, 0, []),
                "u32": TypeInfo("u32", TypeCategory.PRIMITIVE, 4, False, False, 0, []),
                "u64": TypeInfo("u64", TypeCategory.PRIMITIVE, 8, False, False, 0, []),
                "f32": TypeInfo("f32", TypeCategory.PRIMITIVE, 4, False, False, 0.0, []),
                "f64": TypeInfo("f64", TypeCategory.PRIMITIVE, 8, False, False, 0.0, []),
                "bool": TypeInfo("bool", TypeCategory.PRIMITIVE, 1, False, False, false, []),
                "String": TypeInfo("String", TypeCategory.PRIMITIVE, None, False, True, String::new(), []),
                "&str": TypeInfo("&str", TypeCategory.PRIMITIVE, None, False, False, "", []),
                "Vec": TypeInfo("Vec", TypeCategory.COMPOSITE, None, True, True, Vec::new(), []),
                "HashMap": TypeInfo("HashMap", TypeCategory.COMPOSITE, None, True, True, HashMap::new(), []),
                "Option": TypeInfo("Option", TypeCategory.GENERIC, None, True, False, None, []),
                "Result": TypeInfo("Result", TypeCategory.GENERIC, None, True, False, Ok(()), [])
            },
            "java": {
                "int": TypeInfo("int", TypeCategory.PRIMITIVE, 4, False, False, 0, []),
                "long": TypeInfo("long", TypeCategory.PRIMITIVE, 8, False, False, 0L, []),
                "float": TypeInfo("float", TypeCategory.PRIMITIVE, 4, False, False, 0.0f, []),
                "double": TypeInfo("double", TypeCategory.PRIMITIVE, 8, False, False, 0.0, []),
                "boolean": TypeInfo("boolean", TypeCategory.PRIMITIVE, 1, False, False, false, []),
                "char": TypeInfo("char", TypeCategory.PRIMITIVE, 2, False, False, '\0', []),
                "String": TypeInfo("String", TypeCategory.REFERENCE, None, False, False, "", []),
                "Integer": TypeInfo("Integer", TypeCategory.REFERENCE, 4, True, False, null, []),
                "Long": TypeInfo("Long", TypeCategory.REFERENCE, 8, True, False, null, []),
                "Float": TypeInfo("Float", TypeCategory.REFERENCE, 4, True, False, null, []),
                "Double": TypeInfo("Double", TypeCategory.REFERENCE, 8, True, False, null, []),
                "Boolean": TypeInfo("Boolean", TypeCategory.REFERENCE, 1, True, False, null, []),
                "Character": TypeInfo("Character", TypeCategory.REFERENCE, 2, True, False, null, []),
                "List": TypeInfo("List", TypeCategory.COMPOSITE, None, True, True, null, []),
                "Map": TypeInfo("Map", TypeCategory.COMPOSITE, None, True, True, null, []),
                "Set": TypeInfo("Set", TypeCategory.COMPOSITE, None, True, True, null, [])
            },
            "csharp": {
                "int": TypeInfo("int", TypeCategory.PRIMITIVE, 4, False, False, 0, []),
                "long": TypeInfo("long", TypeCategory.PRIMITIVE, 8, False, False, 0L, []),
                "float": TypeInfo("float", TypeCategory.PRIMITIVE, 4, False, False, 0.0f, []),
                "double": TypeInfo("double", TypeCategory.PRIMITIVE, 8, False, False, 0.0, []),
                "bool": TypeInfo("bool", TypeCategory.PRIMITIVE, 1, False, False, false, []),
                "char": TypeInfo("char", TypeCategory.PRIMITIVE, 2, False, False, '\0', []),
                "string": TypeInfo("string", TypeCategory.REFERENCE, None, False, False, "", []),
                "object": TypeInfo("object", TypeCategory.REFERENCE, None, True, False, null, []),
                "List": TypeInfo("List", TypeCategory.COMPOSITE, None, True, True, null, []),
                "Dictionary": TypeInfo("Dictionary", TypeCategory.COMPOSITE, None, True, True, null, []),
                "HashSet": TypeInfo("HashSet", TypeCategory.COMPOSITE, None, True, True, null, [])
            }
        }
    
    def _load_mapping_rules(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Carrega regras de mapeamento entre linguagens."""
        return {
            "python_to_javascript": {
                "int": {"target": "number", "confidence": 0.9, "notes": ["JavaScript usa number para todos os números"]},
                "float": {"target": "number", "confidence": 0.9, "notes": ["JavaScript usa number para todos os números"]},
                "str": {"target": "string", "confidence": 0.95, "notes": ["Mapeamento direto"]},
                "bool": {"target": "boolean", "confidence": 0.95, "notes": ["Mapeamento direto"]},
                "list": {"target": "array", "confidence": 0.9, "notes": ["Funcionalidade similar"]},
                "dict": {"target": "object", "confidence": 0.85, "notes": ["Diferenças na iteração"]},
                "tuple": {"target": "array", "confidence": 0.8, "notes": ["JavaScript não tem tuplas imutáveis"]},
                "None": {"target": "null", "confidence": 0.9, "notes": ["Mapeamento direto"]}
            },
            "python_to_rust": {
                "int": {"target": "i32", "confidence": 0.8, "notes": ["Rust tem tipos específicos de tamanho"]},
                "float": {"target": "f64", "confidence": 0.8, "notes": ["Rust tem tipos específicos de precisão"]},
                "str": {"target": "String", "confidence": 0.9, "notes": ["String owned vs &str borrowed"]},
                "bool": {"target": "bool", "confidence": 0.95, "notes": ["Mapeamento direto"]},
                "list": {"target": "Vec", "confidence": 0.9, "notes": ["Vec é o equivalente mais próximo"]},
                "dict": {"target": "HashMap", "confidence": 0.85, "notes": ["HashMap do std::collections"]},
                "tuple": {"target": "tuple", "confidence": 0.9, "notes": ["Tuplas são imutáveis em Rust"]},
                "None": {"target": "Option<T>", "confidence": 0.7, "notes": ["Option é mais expressivo que None"]}
            },
            "javascript_to_python": {
                "number": {"target": "float", "confidence": 0.9, "notes": ["Python usa float para números"]},
                "string": {"target": "str", "confidence": 0.95, "notes": ["Mapeamento direto"]},
                "boolean": {"target": "bool", "confidence": 0.95, "notes": ["Mapeamento direto"]},
                "array": {"target": "list", "confidence": 0.9, "notes": ["Funcionalidade similar"]},
                "object": {"target": "dict", "confidence": 0.85, "notes": ["Diferenças na iteração"]},
                "null": {"target": "None", "confidence": 0.9, "notes": ["Mapeamento direto"]},
                "undefined": {"target": "None", "confidence": 0.8, "notes": ["Python não tem undefined"]}
            }
        }
    
    def _load_context_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Carrega regras de contexto para mapeamento."""
        return {
            "python_to_rust": [
                {
                    "condition": "numeric_operation",
                    "int": "i64",
                    "float": "f64",
                    "reason": "Operações numéricas podem precisar de mais precisão"
                },
                {
                    "condition": "memory_constrained",
                    "int": "i32",
                    "float": "f32",
                    "reason": "Ambientes com restrições de memória"
                },
                {
                    "condition": "performance_critical",
                    "str": "&str",
                    "reason": "String slices são mais eficientes para leitura"
                }
            ],
            "python_to_javascript": [
                {
                    "condition": "web_environment",
                    "list": "Array",
                    "dict": "Object",
                    "reason": "Uso específico para web APIs"
                }
            ]
        }
    
    def map_types(self, source_lang: str, target_lang: str, 
                  context: Optional[Dict[str, Any]] = None) -> Dict[str, TypeMapping]:
        """
        Mapeia tipos de uma linguagem para outra.
        
        Args:
            source_lang: Linguagem de origem
            target_lang: Linguagem de destino
            context: Contexto adicional para mapeamento
            
        Returns:
            Dicionário com mapeamentos de tipos
        """
        if context is None:
            context = {}
        
        source_lang = source_lang.lower()
        target_lang = target_lang.lower()
        
        mapping_key = f"{source_lang}_to_{target_lang}"
        if mapping_key not in self.mapping_rules:
            raise ValueError(f"Mapeamento de {source_lang} para {target_lang} não é suportado")
        
        rules = self.mapping_rules[mapping_key]
        context_rules = self.context_rules.get(mapping_key, [])
        
        mappings = {}
        
        for source_type, rule in rules.items():
            target_type = rule["target"]
            confidence = rule["confidence"]
            notes = rule["notes"].copy()
            alternatives = self._find_alternatives(source_type, source_lang, target_lang)
            
            # Aplica regras de contexto
            for context_rule in context_rules:
                if self._matches_context(context, context_rule):
                    if source_type in context_rule:
                        target_type = context_rule[source_type]
                        notes.append(f"Contexto: {context_rule['reason']}")
                        confidence = min(confidence + 0.1, 1.0)
            
            mappings[source_type] = TypeMapping(
                source_type=source_type,
                target_type=target_type,
                confidence=confidence,
                notes=notes,
                alternatives=alternatives
            )
        
        return mappings
    
    def _find_alternatives(self, source_type: str, source_lang: str, 
                          target_lang: str) -> List[str]:
        """Encontra tipos alternativos para o mapeamento."""
        alternatives = []
        
        # Busca tipos similares na linguagem de destino
        target_types = self.type_definitions.get(target_lang, {})
        source_info = self.type_definitions.get(source_lang, {}).get(source_type)
        
        if source_info:
            for target_type_name, target_info in target_types.items():
                if (target_info.category == source_info.category and 
                    target_type_name != source_type):
                    alternatives.append(target_type_name)
        
        return alternatives[:3]  # Limita a 3 alternativas
    
    def _matches_context(self, context: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """Verifica se o contexto corresponde à regra."""
        condition = rule.get("condition", "")
        
        if condition == "numeric_operation":
            return context.get("operation_type") == "numeric"
        elif condition == "memory_constrained":
            return context.get("memory_constraints", False)
        elif condition == "performance_critical":
            return context.get("performance_requirements", False)
        elif condition == "web_environment":
            return context.get("environment") == "web"
        
        return False
    
    def get_type_info(self, type_name: str, language: str) -> Optional[TypeInfo]:
        """
        Retorna informações detalhadas sobre um tipo.
        
        Args:
            type_name: Nome do tipo
            language: Linguagem do tipo
            
        Returns:
            Informações do tipo ou None se não encontrado
        """
        language = language.lower()
        types = self.type_definitions.get(language, {})
        return types.get(type_name)
    
    def compare_types(self, type_a: str, lang_a: str, type_b: str, lang_b: str) -> Dict[str, Any]:
        """
        Compara dois tipos de linguagens diferentes.
        
        Args:
            type_a: Primeiro tipo
            lang_a: Linguagem do primeiro tipo
            type_b: Segundo tipo
            lang_b: Linguagem do segundo tipo
            
        Returns:
            Dicionário com comparação dos tipos
        """
        info_a = self.get_type_info(type_a, lang_a)
        info_b = self.get_type_info(type_b, lang_b)
        
        if not info_a or not info_b:
            return {"error": "Tipo não encontrado"}
        
        comparison = {
            "type_a": {"name": type_a, "language": lang_a, "info": info_a},
            "type_b": {"name": type_b, "language": lang_b, "info": info_b},
            "similarity": {
                "category_match": info_a.category == info_b.category,
                "size_compatible": self._is_size_compatible(info_a, info_b),
                "nullability_compatible": info_a.nullable == info_b.nullable,
                "mutability_compatible": info_a.mutable == info_b.mutable
            },
            "compatibility_score": self._calculate_type_compatibility(info_a, info_b)
        }
        
        return comparison
    
    def _is_size_compatible(self, info_a: TypeInfo, info_b: TypeInfo) -> bool:
        """Verifica se os tamanhos dos tipos são compatíveis."""
        if info_a.size is None or info_b.size is None:
            return True  # Não podemos determinar
        
        return info_a.size >= info_b.size
    
    def _calculate_type_compatibility(self, info_a: TypeInfo, info_b: TypeInfo) -> float:
        """Calcula score de compatibilidade entre tipos."""
        score = 0.0
        
        # Categoria (peso: 0.4)
        if info_a.category == info_b.category:
            score += 0.4
        
        # Tamanho (peso: 0.2)
        if self._is_size_compatible(info_a, info_b):
            score += 0.2
        
        # Nullability (peso: 0.2)
        if info_a.nullable == info_b.nullable:
            score += 0.2
        
        # Mutabilidade (peso: 0.2)
        if info_a.mutable == info_b.mutable:
            score += 0.2
        
        return score
    
    def suggest_type(self, value: Any, target_language: str, 
                    context: Optional[Dict[str, Any]] = None) -> TypeMapping:
        """
        Sugere o tipo mais apropriado para um valor em uma linguagem.
        
        Args:
            value: Valor para inferir o tipo
            target_language: Linguagem de destino
            context: Contexto adicional
            
        Returns:
            Sugestão de tipo com mapeamento
        """
        if context is None:
            context = {}
        
        target_language = target_language.lower()
        
        # Inferência básica de tipo
        if isinstance(value, bool):
            source_type = "bool"
        elif isinstance(value, int):
            source_type = "int"
        elif isinstance(value, float):
            source_type = "float"
        elif isinstance(value, str):
            source_type = "str"
        elif isinstance(value, list):
            source_type = "list"
        elif isinstance(value, dict):
            source_type = "dict"
        elif value is None:
            source_type = "None"
        else:
            source_type = "object"
        
        # Mapeia para a linguagem de destino
        mappings = self.map_types("python", target_language, context)
        
        if source_type in mappings:
            return mappings[source_type]
        else:
            # Fallback para object/any
            return TypeMapping(
                source_type=source_type,
                target_type="object" if target_language in ["javascript", "csharp"] else "any",
                confidence=0.5,
                notes=["Tipo inferido automaticamente"],
                alternatives=[]
            )
    
    def validate_mapping(self, source_type: str, target_type: str, 
                        source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Valida um mapeamento de tipos.
        
        Args:
            source_type: Tipo de origem
            target_type: Tipo de destino
            source_lang: Linguagem de origem
            target_lang: Linguagem de destino
            
        Returns:
            Resultado da validação
        """
        # Obtém informações dos tipos
        source_info = self.get_type_info(source_type, source_lang)
        target_info = self.get_type_info(target_type, target_lang)
        
        if not source_info or not target_info:
            return {"valid": False, "error": "Tipo não encontrado"}
        
        # Verifica se o mapeamento é válido
        comparison = self.compare_types(source_type, source_lang, target_type, target_lang)
        
        validation = {
            "valid": comparison["compatibility_score"] >= 0.6,
            "compatibility_score": comparison["compatibility_score"],
            "warnings": [],
            "recommendations": []
        }
        
        # Gera warnings e recomendações
        if not comparison["similarity"]["category_match"]:
            validation["warnings"].append("Categorias de tipo diferentes")
        
        if not comparison["similarity"]["size_compatible"]:
            validation["warnings"].append("Possível perda de precisão")
        
        if comparison["compatibility_score"] < 0.8:
            validation["recommendations"].append("Considere tipos alternativos")
        
        return validation 