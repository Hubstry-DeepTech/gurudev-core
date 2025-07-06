# GuruDev Lexer Specification — v0.2 (Experimental Extension)
# Complemento histórico ao Lexer principal da linguagem GuruDev
# Mantém compatibilidade com a estrutura v1.0.0-alpha, mas incorpora elementos da GuruMatrix[5D]

import ply.lex as lex

# Lista de tokens principais estendida
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

# Expressões regulares

t_EQUALS = r'='

def t_STRING(t):
    r'"([^\"]|\\.)*"'
    t.value = t.value[1:-1]  # remove aspas
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
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Inicialização
lexer = lex.lex()

# Exemplo de uso para teste e documentação
if __name__ == '__main__':
    data = 'clave = "ciencia"\nhermeneutica = 4\nmostre energia'
    lexer.input(data)
    for tok in lexer:
        print(tok)
