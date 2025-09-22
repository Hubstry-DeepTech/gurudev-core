# GuruDev® Lexer – Overview

> 🌐 **Language / Idioma**: [Português](LEXER_OVERVIEW.md) | **English** | [Bilingual Index](../../BILINGUAL_INDEX.md)

This document explains, in a didactic way, how the lexical analyzer (lexer) of the GuruDev® language works.

## What is a lexer?

The lexer is the "first sieve" of the source code. It transforms text written in GuruDev® into small pieces called **tokens**.  
These tokens are recognized by rules (regular expressions) and serve as the foundation for the parser and program execution.

## Main token groups

- **Block structures**: [bloco], [sobrescrita], [subescritas], etc.
- **Code delimiters**: ¡codigo!, !/codigo!, etc.
- **Grammatical keywords**: VOC, NOM, ACU, etc.
- **Data types**: Bool, String, Int, etc.
- **Operators**: +, -, *, /, ==, !=, etc.
- **Literals**: numbers, strings, booleans.
- **Identifiers**: variable names, functions, etc.
- **Semantic attributes**: [nivel="holistico"], [raiz="SEG"], etc.

## Lexer states

The lexer changes "state" according to the part of the code it's reading, to correctly handle GuruDev® blocks and code from other languages.

## How to test the lexer?

- Run the main script to see the tokens recognized from a commented example.
- Use the `test_lexer.py` file to run automated tests with various GuruDev® code examples.

## File structure

- `token_types.py`: enumerates all token types.
- `token_maps.py`: maps attribute values to token types.
- `gurudev_lexer.py`: lexer rules (PLY), lexer construction and tokenization function.
- `test_lexer.py`: automated tests.

---

> 🌐 **Navigation / Navegação**: [Português](LEXER_OVERVIEW.md) | **English** | [Bilingual Index](../../BILINGUAL_INDEX.md)