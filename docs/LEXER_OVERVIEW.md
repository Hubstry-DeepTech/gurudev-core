# Lexer GuruDev® – Visão Geral

Este documento explica, de forma didática, como funciona o analisador léxico (lexer) da linguagem GuruDev®.

## O que é um lexer?

O lexer é a "primeira peneira" do código-fonte. Ele transforma o texto escrito em GuruDev® em pequenas peças chamadas **tokens**.  
Esses tokens são reconhecidos por regras (expressões regulares) e servem de base para o parser e para a execução do programa.

## Principais grupos de tokens

- **Estruturas de bloco**: [bloco], [sobrescrita], [subescritas], etc.
- **Delimitadores de código**: ¡codigo!, !/codigo!, etc.
- **Palavras-chave gramaticais**: VOC, NOM, ACU, etc.
- **Tipos de dado**: Bool, String, Int, etc.
- **Operadores**: +, -, *, /, ==, !=, etc.
- **Literais**: números, strings, booleanos.
- **Identificadores**: nomes de variáveis, funções, etc.
- **Atributos semânticos**: [nivel="holistico"], [raiz="SEG"], etc.

## Estados do lexer

O lexer muda de "estado" conforme a parte do código que está lendo, para tratar corretamente blocos GuruDev® e código de outras linguagens.

## Como testar o lexer?

- Execute o script principal para ver os tokens reconhecidos a partir de um exemplo comentado.
- Use o arquivo `test_lexer.py` para rodar testes automatizados com vários exemplos de código GuruDev®.

## Estrutura dos arquivos

- `token_types.py`: enumera todos os tipos de token.
- `token_maps.py`: faz o mapeamento de valores de atributos para tipos de token.
- `gurudev_lexer.py`: regras do lexer (PLY), construção do lexer e função de tokenização.
- `test_lexer.py`: testes automatizados.

---
