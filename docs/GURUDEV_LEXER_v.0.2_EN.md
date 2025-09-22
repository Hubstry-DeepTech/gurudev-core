# GuruDev Lexer Specification — v0.2 (Experimental Extension)

> 🌐 **Language / Idioma**: [Português](GURUDEV_LEXER_v.0.2.md) | **English** | [Bilingual Index](../../BILINGUAL_INDEX.md)

# Historical complement to the main GuruDev language lexer
# Maintains compatibility with v1.0.0-alpha structure, but incorporates GuruMatrix[5D] elements

import ply.lex as lex

# Extended main token list
reserved = {
    'fun': 'FUN',
    'tag': 'TAG',
    'clave': 'CLAVE',
    'hermeneutica': 'HERMENEUTICA',
    'mostre': 'MOSTRE',
    'load': 'LOAD',
    'display': 'DISPLAY',
    'map_to': 'MAP_TO',
    'ontologia': 'ONTOLOGIA',
    'tempo': 'TEMPO',
    'modo': 'MODO'
}

tokens = [
    'ID', 'STRING', 'EQUALS', 'NEWLINE'
] + list(reserved.values())

# Regular expressions

t_EQUALS = r'='

def t_STRING(t):
    r'"([^\"]|\\.)*"'
    t.value = t.value[1:-1]  # remove quotes
    return t

def t_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

t_ignore = ' \t'

def t_error(t):
    print(f"Invalid character: {t.value[0]}")
    t.lexer.skip(1)

# Initialization
lexer = lex.lex()

# Usage example for testing and documentation
if __name__ == '__main__':
    data = 'clave = "ciencia"\nhermeneutica = 4\nmostre energia'
    lexer.input(data)
    for tok in lexer:
        print(tok)

---

> 🌐 **Navigation / Navegação**: [Português](GURUDEV_LEXER_v.0.2.md) | **English** | [Bilingual Index](../../BILINGUAL_INDEX.md)