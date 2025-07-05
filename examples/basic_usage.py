#!/usr/bin/env python3
"""
Exemplo Básico de Uso da Biblioteca Alexandria

Este exemplo demonstra as funcionalidades principais da biblioteca:
- Análise comparativa de linguagens
- Tradução de código
- Mapeamento de tipos
"""

from alexandria.core.analyzer import LanguageAnalyzer
from alexandria.core.translator import CodeTranslator
from alexandria.core.type_mapper import TypeMapper

def main():
    """Função principal do exemplo."""
    print("🏛️ Alexandria: Biblioteca de Interoperabilidade e Programação Comparada")
    print("=" * 70)
    
    # 1. Análise Comparativa
    print("\n📊 1. ANÁLISE COMPARATIVA DE LINGUAGENS")
    print("-" * 50)
    
    analyzer = LanguageAnalyzer()
    
    # Compara Python e Rust
    comparison = analyzer.compare("Python", "Rust")
    print(f"Comparação: {comparison.language_a} vs {comparison.language_b}")
    print(f"Score de Similaridade: {comparison.similarity_score:.2f}")
    print(f"Score de Interoperabilidade: {comparison.interoperability_score:.2f}")
    print(f"Complexidade de Tradução: {comparison.translation_complexity}")
    print(f"Paradigmas Compartilhados: {', '.join(comparison.paradigm_overlap)}")
    
    # Lista todas as linguagens disponíveis
    print(f"\nLinguagens disponíveis: {len(analyzer.list_languages())}")
    
    # Busca linguagens por critérios
    functional_langs = analyzer.search_languages({"paradigmas": ["Funcional"]})
    print(f"Linguagens funcionais: {', '.join(functional_langs)}")
    
    # 2. Tradução de Código
    print("\n🔄 2. TRADUÇÃO DE CÓDIGO")
    print("-" * 50)
    
    translator = CodeTranslator()
    
    # Código Python para traduzir
    python_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def main():
    result = factorial(5)
    print(f"Factorial de 5 é: {result}")
"""
    
    print("Código Python original:")
    print(python_code)
    
    # Traduz para JavaScript
    result = translator.translate(python_code, "python", "javascript")
    print(f"\nTraduzido para JavaScript (confiança: {result.confidence_score:.2f}):")
    print(result.translated_code)
    
    if result.warnings:
        print(f"\n⚠️ Avisos: {', '.join(result.warnings)}")
    
    # 3. Mapeamento de Tipos
    print("\n🗺️ 3. MAPEAMENTO DE TIPOS")
    print("-" * 50)
    
    type_mapper = TypeMapper()
    
    # Mapeia tipos Python para Rust
    type_mappings = type_mapper.map_types("python", "rust")
    
    print("Mapeamento Python → Rust:")
    for source_type, mapping in type_mappings.items():
        print(f"  {source_type} → {mapping.target_type} (confiança: {mapping.confidence:.2f})")
        if mapping.notes:
            print(f"    Notas: {', '.join(mapping.notes)}")
    
    # Sugere tipo para um valor
    value = 42
    suggestion = type_mapper.suggest_type(value, "rust")
    print(f"\nSugestão para valor {value} em Rust:")
    print(f"  Tipo sugerido: {suggestion.target_type} (confiança: {suggestion.confidence:.2f})")
    
    # 4. Análise de Família Linguística
    print("\n👨‍👩‍👧‍👦 4. ANÁLISE DE FAMÍLIA LINGUÍSTICA")
    print("-" * 50)
    
    c_family = analyzer.analyze_family("C")
    print(f"Família da linguagem C:")
    print(f"  Membros: {', '.join(c_family.members)}")
    print(f"  Características comuns: {', '.join(c_family.common_features)}")
    print(f"  Timeline de evolução:")
    for lang, year in c_family.evolution_timeline.items():
        print(f"    {lang}: {year}")
    
    # 5. Demonstração de Funcionalidades Avançadas
    print("\n🚀 5. FUNCIONALIDADES AVANÇADAS")
    print("-" * 50)
    
    # Compara múltiplas linguagens
    languages_to_compare = ["Python", "JavaScript", "Rust", "Java"]
    
    print("Matriz de similaridade entre linguagens:")
    print("          ", end="")
    for lang in languages_to_compare:
        print(f"{lang:>10}", end="")
    print()
    
    for lang1 in languages_to_compare:
        print(f"{lang1:>10}", end="")
        for lang2 in languages_to_compare:
            if lang1 == lang2:
                print(f"{'1.00':>10}", end="")
            else:
                try:
                    comp = analyzer.compare(lang1, lang2)
                    print(f"{comp.similarity_score:>10.2f}", end="")
                except:
                    print(f"{'N/A':>10}", end="")
        print()
    
    print("\n✅ Demonstração concluída!")
    print("\nPara mais informações, consulte a documentação em:")
    print("https://github.com/seu-usuario/alexandria")

if __name__ == "__main__":
    main() 