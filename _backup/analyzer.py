"""
Módulo de Análise Comparativa de Linguagens

Implementa algoritmos para análise sistemática e comparação de linguagens
de programação baseados nos princípios da Programação Comparada.
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LanguageComparison:
    """Resultado de uma comparação entre duas linguagens."""
    language_a: str
    language_b: str
    similarity_score: float
    paradigm_overlap: List[str]
    type_compatibility: Dict[str, str]
    syntax_differences: List[str]
    semantic_differences: List[str]
    interoperability_score: float
    translation_complexity: str

@dataclass
class LanguageFamily:
    """Análise de família linguística."""
    root_language: str
    members: List[str]
    common_features: List[str]
    divergence_points: List[str]
    evolution_timeline: Dict[str, int]

class LanguageAnalyzer:
    """
    Analisador comparativo de linguagens de programação.
    
    Implementa algoritmos para análise sistemática baseados nos
    princípios da Programação Comparada.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Inicializa o analisador.
        
        Args:
            data_path: Caminho para o arquivo de dados das linguagens
        """
        if data_path is None:
            data_path = Path(__file__).parent.parent.parent / "docs" / "programming_languages.json"
        
        self.data_path = Path(data_path)
        self.languages_data = self._load_languages_data()
        self.paradigm_weights = {
            "Imperativa": 0.3,
            "Funcional": 0.25,
            "Orientada a objetos": 0.25,
            "Procedural": 0.2,
            "Lazy evaluation": 0.1,
            "Concorrente": 0.15,
            "Reflexiva": 0.1
        }
    
    def _load_languages_data(self) -> Dict[str, Any]:
        """Carrega os dados das linguagens do arquivo JSON."""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {lang["nome"]: lang for lang in data}
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {self.data_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Erro ao decodificar JSON: {self.data_path}")
    
    def compare(self, lang_a: str, lang_b: str) -> LanguageComparison:
        """
        Compara duas linguagens de programação.
        
        Args:
            lang_a: Nome da primeira linguagem
            lang_b: Nome da segunda linguagem
            
        Returns:
            Objeto LanguageComparison com os resultados
        """
        if lang_a not in self.languages_data:
            raise ValueError(f"Linguagem não encontrada: {lang_a}")
        if lang_b not in self.languages_data:
            raise ValueError(f"Linguagem não encontrada: {lang_b}")
        
        data_a = self.languages_data[lang_a]
        data_b = self.languages_data[lang_b]
        
        # Calcula similaridade geral
        similarity_score = self._calculate_similarity(data_a, data_b)
        
        # Analisa sobreposição de paradigmas
        paradigm_overlap = self._analyze_paradigm_overlap(data_a, data_b)
        
        # Mapeia compatibilidade de tipos
        type_compatibility = self._map_type_compatibility(data_a, data_b)
        
        # Identifica diferenças sintáticas
        syntax_differences = self._identify_syntax_differences(data_a, data_b)
        
        # Identifica diferenças semânticas
        semantic_differences = self._identify_semantic_differences(data_a, data_b)
        
        # Calcula score de interoperabilidade
        interoperability_score = self._calculate_interoperability_score(
            data_a, data_b, similarity_score, paradigm_overlap
        )
        
        # Avalia complexidade de tradução
        translation_complexity = self._assess_translation_complexity(
            data_a, data_b, similarity_score
        )
        
        return LanguageComparison(
            language_a=lang_a,
            language_b=lang_b,
            similarity_score=similarity_score,
            paradigm_overlap=paradigm_overlap,
            type_compatibility=type_compatibility,
            syntax_differences=syntax_differences,
            semantic_differences=semantic_differences,
            interoperability_score=interoperability_score,
            translation_complexity=translation_complexity
        )
    
    def _calculate_similarity(self, data_a: Dict, data_b: Dict) -> float:
        """Calcula score de similaridade entre duas linguagens."""
        score = 0.0
        total_weight = 0.0
        
        # Compara paradigmas (peso: 0.4)
        paradigm_similarity = self._compare_paradigms(data_a["paradigmas"], data_b["paradigmas"])
        score += paradigm_similarity * 0.4
        total_weight += 0.4
        
        # Compara tipagem (peso: 0.3)
        typing_similarity = self._compare_typing(data_a["tipagem"], data_b["tipagem"])
        score += typing_similarity * 0.3
        total_weight += 0.3
        
        # Compara propósito (peso: 0.2)
        purpose_similarity = self._compare_purpose(data_a["proposito"], data_b["proposito"])
        score += purpose_similarity * 0.2
        total_weight += 0.2
        
        # Compara ano de criação (peso: 0.1)
        age_similarity = self._compare_age(data_a["ano_criacao"], data_b["ano_criacao"])
        score += age_similarity * 0.1
        total_weight += 0.1
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def _compare_paradigms(self, paradigms_a: List[str], paradigms_b: List[str]) -> float:
        """Compara paradigmas de programação."""
        set_a = set(paradigms_a)
        set_b = set(paradigmas_b)
        
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        
        return intersection / union if union > 0 else 0.0
    
    def _compare_typing(self, typing_a: str, typing_b: str) -> float:
        """Compara sistemas de tipagem."""
        # Normaliza strings de tipagem
        typing_a = typing_a.lower().replace(",", "").split()
        typing_b = typing_b.lower().replace(",", "").split()
        
        set_a = set(typing_a)
        set_b = set(typing_b)
        
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        
        return intersection / union if union > 0 else 0.0
    
    def _compare_purpose(self, purpose_a: str, purpose_b: str) -> float:
        """Compara propósitos das linguagens."""
        purposes_a = set(purpose_a.lower().split(", "))
        purposes_b = set(purpose_b.lower().split(", "))
        
        intersection = len(purposes_a.intersection(purposes_b))
        union = len(purposes_a.union(purposes_b))
        
        return intersection / union if union > 0 else 0.0
    
    def _compare_age(self, year_a: int, year_b: int) -> float:
        """Compara anos de criação (quanto mais próximos, mais similar)."""
        age_diff = abs(year_a - year_b)
        # Normaliza para 0-1 (diferença de 50 anos = 0.5 similaridade)
        return max(0.0, 1.0 - (age_diff / 50.0))
    
    def _analyze_paradigm_overlap(self, data_a: Dict, data_b: Dict) -> List[str]:
        """Analisa sobreposição de paradigmas."""
        paradigms_a = set(data_a["paradigmas"])
        paradigms_b = set(data_b["paradigmas"])
        
        return list(paradigms_a.intersection(paradigms_b))
    
    def _map_type_compatibility(self, data_a: Dict, data_b: Dict) -> Dict[str, str]:
        """Mapeia compatibilidade de tipos entre linguagens."""
        # Mapeamento básico de tipos
        type_mappings = {
            "python": {
                "int": "i32", "float": "f64", "str": "String", "bool": "bool",
                "list": "Vec", "dict": "HashMap", "tuple": "tuple"
            },
            "rust": {
                "i32": "int", "f64": "float", "String": "str", "bool": "bool",
                "Vec": "list", "HashMap": "dict", "tuple": "tuple"
            },
            "javascript": {
                "number": "float", "string": "str", "boolean": "bool",
                "array": "list", "object": "dict"
            }
        }
        
        # Simplificado - em implementação real seria mais complexo
        return {"int": "i32", "str": "String", "bool": "bool"}
    
    def _identify_syntax_differences(self, data_a: Dict, data_b: Dict) -> List[str]:
        """Identifica diferenças sintáticas principais."""
        differences = []
        
        # Compara exemplos de hello world
        hello_a = data_a["hello_world"]
        hello_b = data_b["hello_world"]
        
        if "print" in hello_a and "print" not in hello_b:
            differences.append("Diferentes funções de saída")
        
        if ";" in hello_a and ";" not in hello_b:
            differences.append("Uso de ponto e vírgula")
        
        if "{" in hello_a and "{" not in hello_b:
            differences.append("Uso de chaves para blocos")
        
        return differences
    
    def _identify_semantic_differences(self, data_a: Dict, data_b: Dict) -> List[str]:
        """Identifica diferenças semânticas principais."""
        differences = []
        
        # Compara tipagem
        if "dinâmica" in data_a["tipagem"] and "estática" in data_b["tipagem"]:
            differences.append("Tipagem dinâmica vs estática")
        
        # Compara paradigmas
        if "Funcional" in data_a["paradigmas"] and "Funcional" not in data_b["paradigmas"]:
            differences.append("Suporte a programação funcional")
        
        return differences
    
    def _calculate_interoperability_score(self, data_a: Dict, data_b: Dict, 
                                        similarity: float, paradigm_overlap: List[str]) -> float:
        """Calcula score de interoperabilidade."""
        base_score = similarity * 0.6
        
        # Bônus por paradigmas compartilhados
        paradigm_bonus = len(paradigm_overlap) * 0.1
        
        # Bônus por tipagem similar
        typing_bonus = 0.0
        if "dinâmica" in data_a["tipagem"] and "dinâmica" in data_b["tipagem"]:
            typing_bonus = 0.2
        elif "estática" in data_a["tipagem"] and "estática" in data_b["tipagem"]:
            typing_bonus = 0.15
        
        return min(1.0, base_score + paradigm_bonus + typing_bonus)
    
    def _assess_translation_complexity(self, data_a: Dict, data_b: Dict, similarity: float) -> str:
        """Avalia complexidade de tradução entre linguagens."""
        if similarity >= 0.8:
            return "Baixa"
        elif similarity >= 0.6:
            return "Média"
        elif similarity >= 0.4:
            return "Alta"
        else:
            return "Muito Alta"
    
    def analyze_family(self, root_language: str) -> LanguageFamily:
        """
        Analisa família linguística de uma linguagem.
        
        Args:
            root_language: Linguagem raiz da família
            
        Returns:
            Objeto LanguageFamily com a análise
        """
        if root_language not in self.languages_data:
            raise ValueError(f"Linguagem não encontrada: {root_language}")
        
        # Identifica membros da família (simplificado)
        family_members = self._identify_family_members(root_language)
        common_features = self._find_common_features(family_members)
        divergence_points = self._identify_divergence_points(family_members)
        evolution_timeline = self._create_evolution_timeline(family_members)
        
        return LanguageFamily(
            root_language=root_language,
            members=family_members,
            common_features=common_features,
            divergence_points=divergence_points,
            evolution_timeline=evolution_timeline
        )
    
    def _identify_family_members(self, root_language: str) -> List[str]:
        """Identifica membros da família linguística."""
        # Mapeamento simplificado de famílias
        families = {
            "C": ["C", "C++", "C#", "Objective-C"],
            "Lisp": ["Lisp", "Scheme", "Clojure", "Common Lisp"],
            "Java": ["Java", "Kotlin", "Scala", "Groovy"],
            "Python": ["Python", "Ruby", "Perl"]
        }
        
        for family, members in families.items():
            if root_language in members:
                return members
        
        return [root_language]
    
    def _find_common_features(self, members: List[str]) -> List[str]:
        """Encontra características comuns da família."""
        if len(members) == 1:
            return []
        
        common_features = []
        for member in members:
            if member in self.languages_data:
                data = self.languages_data[member]
                common_features.extend(data["paradigmas"])
        
        # Remove duplicatas e retorna mais comuns
        from collections import Counter
        counter = Counter(common_features)
        return [feature for feature, count in counter.most_common(3)]
    
    def _identify_divergence_points(self, members: List[str]) -> List[str]:
        """Identifica pontos de divergência na família."""
        return ["Sistemas de tipos", "Paradigmas dominantes", "Contextos de uso"]
    
    def _create_evolution_timeline(self, members: List[str]) -> Dict[str, int]:
        """Cria timeline de evolução da família."""
        timeline = {}
        for member in members:
            if member in self.languages_data:
                timeline[member] = self.languages_data[member]["ano_criacao"]
        return timeline
    
    def get_language_info(self, language_name: str) -> Dict[str, Any]:
        """
        Retorna informações detalhadas de uma linguagem.
        
        Args:
            language_name: Nome da linguagem
            
        Returns:
            Dicionário com informações da linguagem
        """
        if language_name not in self.languages_data:
            raise ValueError(f"Linguagem não encontrada: {language_name}")
        
        return self.languages_data[language_name].copy()
    
    def list_languages(self) -> List[str]:
        """Retorna lista de todas as linguagens disponíveis."""
        return list(self.languages_data.keys())
    
    def search_languages(self, criteria: Dict[str, Any]) -> List[str]:
        """
        Busca linguagens por critérios específicos.
        
        Args:
            criteria: Dicionário com critérios de busca
                     (paradigma, ano, tipagem, etc.)
        
        Returns:
            Lista de linguagens que atendem aos critérios
        """
        results = []
        
        for lang_name, lang_data in self.languages_data.items():
            matches = True
            
            for key, value in criteria.items():
                if key in lang_data:
                    if isinstance(value, list):
                        if not any(v in lang_data[key] for v in value):
                            matches = False
                    else:
                        if value not in str(lang_data[key]):
                            matches = False
                else:
                    matches = False
            
            if matches:
                results.append(lang_name)
        
        return results 