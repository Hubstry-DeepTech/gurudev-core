"""
Testes para o módulo de análise comparativa de linguagens.
"""

import pytest
from alexandria.core.analyzer import LanguageAnalyzer, LanguageComparison, LanguageFamily


class TestLanguageAnalyzer:
    """Testes para a classe LanguageAnalyzer."""
    
    def setup_method(self):
        """Configuração para cada teste."""
        self.analyzer = LanguageAnalyzer()
    
    def test_init(self):
        """Testa inicialização do analisador."""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, 'languages_data')
        assert len(self.analyzer.languages_data) > 0
    
    def test_list_languages(self):
        """Testa listagem de linguagens."""
        languages = self.analyzer.list_languages()
        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "Python" in languages
        assert "JavaScript" in languages
    
    def test_get_language_info(self):
        """Testa obtenção de informações de linguagem."""
        info = self.analyzer.get_language_info("Python")
        assert isinstance(info, dict)
        assert info["nome"] == "Python"
        assert "paradigmas" in info
        assert "tipagem" in info
    
    def test_get_language_info_not_found(self):
        """Testa obtenção de linguagem inexistente."""
        with pytest.raises(ValueError, match="Linguagem não encontrada"):
            self.analyzer.get_language_info("LinguagemInexistente")
    
    def test_compare_languages(self):
        """Testa comparação entre linguagens."""
        comparison = self.analyzer.compare("Python", "JavaScript")
        assert isinstance(comparison, LanguageComparison)
        assert comparison.language_a == "Python"
        assert comparison.language_b == "JavaScript"
        assert 0.0 <= comparison.similarity_score <= 1.0
        assert 0.0 <= comparison.interoperability_score <= 1.0
    
    def test_compare_languages_not_found(self):
        """Testa comparação com linguagem inexistente."""
        with pytest.raises(ValueError, match="Linguagem não encontrada"):
            self.analyzer.compare("Python", "LinguagemInexistente")
    
    def test_search_languages(self):
        """Testa busca de linguagens por critérios."""
        # Busca por paradigma funcional
        functional_langs = self.analyzer.search_languages({"paradigmas": ["Funcional"]})
        assert isinstance(functional_langs, list)
        
        # Busca por ano de criação
        modern_langs = self.analyzer.search_languages({"ano_criacao": 2000})
        assert isinstance(modern_langs, list)
    
    def test_analyze_family(self):
        """Testa análise de família linguística."""
        family = self.analyzer.analyze_family("C")
        assert isinstance(family, LanguageFamily)
        assert family.root_language == "C"
        assert isinstance(family.members, list)
        assert isinstance(family.common_features, list)
        assert isinstance(family.evolution_timeline, dict)


class TestLanguageComparison:
    """Testes para a classe LanguageComparison."""
    
    def test_language_comparison_creation(self):
        """Testa criação de objeto de comparação."""
        comparison = LanguageComparison(
            language_a="Python",
            language_b="Rust",
            similarity_score=0.7,
            paradigm_overlap=["Imperativa"],
            type_compatibility={"int": "i32"},
            syntax_differences=["Uso de chaves"],
            semantic_differences=["Tipagem estática vs dinâmica"],
            interoperability_score=0.6,
            translation_complexity="Média"
        )
        
        assert comparison.language_a == "Python"
        assert comparison.language_b == "Rust"
        assert comparison.similarity_score == 0.7
        assert "Imperativa" in comparison.paradigm_overlap


class TestLanguageFamily:
    """Testes para a classe LanguageFamily."""
    
    def test_language_family_creation(self):
        """Testa criação de objeto de família linguística."""
        family = LanguageFamily(
            root_language="C",
            members=["C", "C++", "C#"],
            common_features=["Imperativa", "Procedural"],
            divergence_points=["Sistemas de tipos"],
            evolution_timeline={"C": 1972, "C++": 1985, "C#": 2000}
        )
        
        assert family.root_language == "C"
        assert len(family.members) == 3
        assert "Imperativa" in family.common_features
        assert family.evolution_timeline["C"] == 1972 