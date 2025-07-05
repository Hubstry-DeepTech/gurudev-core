#!/usr/bin/env python3
"""
CLI para Alexandria: Biblioteca de Interoperabilidade e Programação Comparada

Interface de linha de comando para acessar as funcionalidades da biblioteca.
"""

import click
import asyncio
from pathlib import Path
from typing import Optional

from .core.analyzer import LanguageAnalyzer
from .core.translator import CodeTranslator
from .core.type_mapper import TypeMapper
from .core.bridge import BridgeManager, BridgeProtocol
from . import get_version, get_info


@click.group()
@click.version_option(version=get_version(), prog_name="Alexandria")
def main():
    """
    🏛️ Alexandria: Biblioteca de Interoperabilidade e Programação Comparada
    
    Uma biblioteca pioneira que implementa os princípios da Programação Comparada,
    facilitando a interoperabilidade entre linguagens de programação.
    """
    pass


@main.command()
@click.option('--source', '-s', required=True, help='Linguagem de origem')
@click.option('--target', '-t', required=True, help='Linguagem de destino')
@click.option('--output', '-o', help='Arquivo de saída')
def compare(source: str, target: str, output: Optional[str]):
    """Compara duas linguagens de programação."""
    try:
        analyzer = LanguageAnalyzer()
        comparison = analyzer.compare(source, target)
        
        result = f"""
📊 Comparação: {comparison.language_a} vs {comparison.language_b}
{'='*50}

🔍 Métricas de Similaridade:
  • Score de Similaridade: {comparison.similarity_score:.2f}
  • Score de Interoperabilidade: {comparison.interoperability_score:.2f}
  • Complexidade de Tradução: {comparison.translation_complexity}

🔄 Paradigmas Compartilhados:
  • {', '.join(comparison.paradigm_overlap) if comparison.paradigm_overlap else 'Nenhum'}

🗺️ Compatibilidade de Tipos:
"""
        for source_type, target_type in comparison.type_compatibility.items():
            result += f"  • {source_type} → {target_type}\n"
        
        result += f"""
⚡ Diferenças Sintáticas:
  • {chr(10) + '  • '.join(comparison.syntax_differences) if comparison.syntax_differences else 'Nenhuma diferença significativa'}

🧠 Diferenças Semânticas:
  • {chr(10) + '  • '.join(comparison.semantic_differences) if comparison.semantic_differences else 'Nenhuma diferença significativa'}
"""
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result)
            click.echo(f"✅ Resultado salvo em: {output}")
        else:
            click.echo(result)
            
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)


@main.command()
@click.option('--source', '-s', required=True, help='Linguagem de origem')
@click.option('--target', '-t', required=True, help='Linguagem de destino')
@click.option('--file', '-f', help='Arquivo com código para traduzir')
@click.option('--code', '-c', help='Código para traduzir (se não usar --file)')
@click.option('--output', '-o', help='Arquivo de saída')
def translate(source: str, target: str, file: Optional[str], code: Optional[str], output: Optional[str]):
    """Traduz código entre linguagens de programação."""
    try:
        translator = CodeTranslator()
        
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                source_code = f.read()
        elif code:
            source_code = code
        else:
            click.echo("❌ Erro: Especifique --file ou --code", err=True)
            return
        
        result = translator.translate(source_code, source, target)
        
        output_text = f"""
🔄 Tradução: {source} → {target}
{'='*50}

📝 Código Original ({source}):
{'-'*30}
{result.original_code}

📝 Código Traduzido ({target}):
{'-'*30}
{result.translated_code}

📊 Métricas:
  • Confiança: {result.confidence_score:.2f}
  • Avisos: {len(result.warnings)}
  • Notas: {len(result.notes)}
"""
        
        if result.warnings:
            output_text += f"\n⚠️ Avisos:\n"
            for warning in result.warnings:
                output_text += f"  • {warning}\n"
        
        if result.notes:
            output_text += f"\n📝 Notas:\n"
            for note in result.notes:
                output_text += f"  • {note}\n"
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result.translated_code)
            click.echo(f"✅ Código traduzido salvo em: {output}")
        else:
            click.echo(output_text)
            
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)


@main.command()
@click.option('--source', '-s', required=True, help='Linguagem de origem')
@click.option('--target', '-t', required=True, help='Linguagem de destino')
def map_types(source: str, target: str):
    """Mapeia tipos entre linguagens de programação."""
    try:
        type_mapper = TypeMapper()
        mappings = type_mapper.map_types(source, target)
        
        result = f"""
🗺️ Mapeamento de Tipos: {source} → {target}
{'='*50}
"""
        
        for source_type, mapping in mappings.items():
            result += f"""
📋 {source_type} → {mapping.target_type}
  • Confiança: {mapping.confidence:.2f}
  • Alternativas: {', '.join(mapping.alternatives) if mapping.alternatives else 'Nenhuma'}
  • Notas: {', '.join(mapping.notes) if mapping.notes else 'Nenhuma'}
"""
        
        click.echo(result)
        
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)


@main.command()
def list_languages():
    """Lista todas as linguagens disponíveis."""
    try:
        analyzer = LanguageAnalyzer()
        languages = analyzer.list_languages()
        
        result = f"""
📚 Linguagens Disponíveis ({len(languages)})
{'='*50}
"""
        
        for i, lang in enumerate(sorted(languages), 1):
            info = analyzer.get_language_info(lang)
            result += f"{i:2d}. {lang} ({info['ano_criacao']}) - {info['proposito']}\n"
        
        click.echo(result)
        
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)


@main.command()
@click.option('--paradigm', '-p', help='Paradigma de programação')
@click.option('--year', '-y', type=int, help='Ano de criação')
@click.option('--tipagem', '-t', help='Tipo de tipagem')
def search(paradigm: Optional[str], year: Optional[int], tipagem: Optional[str]):
    """Busca linguagens por critérios específicos."""
    try:
        analyzer = LanguageAnalyzer()
        criteria = {}
        
        if paradigm:
            criteria['paradigmas'] = [paradigm]
        if year:
            criteria['ano_criacao'] = year
        if tipagem:
            criteria['tipagem'] = tipagem
        
        if not criteria:
            click.echo("❌ Erro: Especifique pelo menos um critério de busca", err=True)
            return
        
        languages = analyzer.search_languages(criteria)
        
        result = f"""
🔍 Resultado da Busca
{'='*30}
Critérios: {criteria}
Linguagens encontradas: {len(languages)}
"""
        
        for lang in languages:
            info = analyzer.get_language_info(lang)
            result += f"• {lang} ({info['ano_criacao']}) - {info['proposito']}\n"
        
        click.echo(result)
        
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)


@main.command()
@click.option('--language', '-l', required=True, help='Linguagem para analisar')
def family(language: str):
    """Analisa família linguística de uma linguagem."""
    try:
        analyzer = LanguageAnalyzer()
        family_info = analyzer.analyze_family(language)
        
        result = f"""
👨‍👩‍👧‍👦 Família Linguística: {language}
{'='*50}

👥 Membros da Família:
  • {', '.join(family_info.members)}

🔗 Características Comuns:
  • {', '.join(family_info.common_features) if family_info.common_features else 'Nenhuma'}

🔄 Pontos de Divergência:
  • {', '.join(family_info.divergence_points)}

📅 Timeline de Evolução:
"""
        
        for lang, year in sorted(family_info.evolution_timeline.items(), key=lambda x: x[1]):
            result += f"  • {year}: {lang}\n"
        
        click.echo(result)
        
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)


@main.command()
def info():
    """Exibe informações sobre a biblioteca Alexandria."""
    info_data = get_info()
    
    result = f"""
🏛️ Alexandria: Biblioteca de Interoperabilidade e Programação Comparada
{'='*70}

📋 Informações:
  • Nome: {info_data['name']}
  • Versão: {info_data['version']}
  • Autor: {info_data['author']}
  • Descrição: {info_data['description']}
  • URL: {info_data['url']}

🎯 Funcionalidades:
  • Análise comparativa de linguagens
  • Tradução automática de código
  • Mapeamento de tipos cross-language
  • Pontes de interoperabilidade
  • Análise de famílias linguísticas

📚 Comandos Disponíveis:
  • compare: Compara duas linguagens
  • translate: Traduz código entre linguagens
  • map-types: Mapeia tipos entre linguagens
  • list-languages: Lista linguagens disponíveis
  • search: Busca linguagens por critérios
  • family: Analisa família linguística
  • info: Exibe informações da biblioteca

💡 Exemplo de Uso:
  alexandria compare --source Python --target Rust
  alexandria translate --source python --target javascript --file code.py
  alexandria map-types --source python --target rust
"""
    
    click.echo(result)


if __name__ == '__main__':
    main() 