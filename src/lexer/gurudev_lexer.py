Lexer Completo para GuruDev® (Baseado em PLY com Máquina de Estados)
Este lexer é projetado para src/lexer/gurudev_lexer.py. Ele incorpora a sintaxe da GuruDev® (casos gramaticais, estruturas de blocos, anotações semânticas) e gerencia os diferentes tipos de conteúdo, incluindo código estrangeiro aninhado.

Python

import ply.lex as lex

# --- DEFINIÇÃO DOS TOKENS ---
# A ordem dos tokens (e das regras t_ para PLY) importa:
# Regras mais específicas/longas devem vir antes das mais gerais/curtas.
# Operadores de múltiplos caracteres antes dos de um único caractere.
tokens = [
    # Estruturas principais de blocos
    'BLOCO_START', 'BLOCO_END',                 # [bloco] [/bloco]
    'SOBRESCRITA_START', 'SOBRESCRITA_END',     # [sobrescrita] [/sobrescrita]
    'SUBESCRITAS_START', 'SUBESCRITAS_END',     # [subescritas] [/subescritas]
    
    # Delimitadores de código GuruDev®
    'CODIGO_START', 'CODIGO_END',               # ¡codigo! !/codigo!
    
    # Subescritas específicas de linguagens (start/end tags)
    'PYTHON_START', 'PYTHON_END',
    'RUST_START', 'RUST_END',
    'JAVASCRIPT_START', 'JAVASCRIPT_END',
    'CSHARP_START', 'CSHARP_END',
    'WASM_START', 'WASM_END',
    'CPP_START', 'CPP_END',
    'JAVA_START', 'JAVA_END',
    'SQL_START', 'SQL_END',
    'R_START', 'R_END',

    # Conteúdo bruto de código estrangeiro
    'FOREIGN_CODE_CONTENT',
    
    # Atributos e metadados (para [nivel=""], [raiz=""], [clave=""], [ont=""])
    'NIVEL_ATTR', 'RAIZ_ATTR', 'CLAVE_ATTR', 'ONT_ATTR',
    
    # Literais básicos
    'STRING_LITERAL',
    'INT_LITERAL',
    'FLOAT_LITERAL',
    'BOOLEAN_LITERAL', # true, false, verdadeiro, falso
    
    # Identificadores (para nomes de variáveis, funções, etc.)
    'ID',
    
    # Operadores
    'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'LESS_THAN', 'GREATER_THAN', 'NOT',
    'ARROW', # ->
    'EQUALS', 'NOT_EQUALS', 'LESS_EQUAL', 'GREATER_EQUAL', # Operadores de dois caracteres
    'AND', 'OR', # Operadores lógicos de dois caracteres
    
    # Delimitadores
    'LPAREN', 'RPAREN',       # ( )
    'LBRACE', 'RBRACE',       # { }
    'LBRACKET', 'RBRACKET',   # [ ]
    'SEMICOLON',              # ;
    'COMMA',                  # ,
    'DOT',                    # .
    'COLON',                  # :
]

# --- ESTADOS DO LEXER (MÁQUINA DE ESTADOS) ---
# Usamos estados para lidar com os blocos de código GuruDev® e os blocos de código estrangeiro.
# 'exclusive' significa que apenas as regras do estado e as regras sem prefixo (t_) são ativas.
states = (
    ('gurudevcode', 'exclusive'), # Para o código GuruDev® dentro de ¡codigo! ... !/codigo!
    ('foreigncode', 'exclusive'), # Para o código estrangeiro dentro de ¿lang? ... ?/lang?
    ('sobrescrita', 'exclusive'), # Para o conteúdo literal da sobrescrita
)

# --- REGRAS DE EXPRESSÕES REGULARES (t_) ---

# Regras para tokens simples que são válidos em qualquer estado inicial (INITIAL)
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_NOT = r'!'
t_COLON = r':'

# Operadores de múltiplos caracteres (devem vir antes dos de um caractere, se houver sobreposição)
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_ARROW = r'->'

# Strings (válidas em muitos contextos, mas não dentro de código GuruDev principal ou estrangeiro, a menos que seja um literal)
t_STRING_LITERAL = r'"([^"\\]|\\.)*"'
def t_STRING_LITERAL(t):
    t.value = t.value[1:-1] # Remove as aspas
    return t

# Números (inteiros e floats)
def t_FLOAT_LITERAL(t):
    r'\d+\.\d+f?' # Permite sufixo 'f' para float
    t.value = float(t.value.replace('f', ''))
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Comentários (ignoram o conteúdo, mas contam linhas se multilinhas)
def t_COMMENT_SINGLE_LINE(t):
    r'//[^\n]*'
    pass # Ignora o token

def t_COMMENT_MULTI_LINE(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    t.lexer.lineno += t.value.count('\n') # Conta novas linhas
    pass # Ignora o token

# Caracteres ignorados (espaços e tabs)
t_ignore = ' \t'

# Controle de linha (para newlines fora de conteúdo que é tokenizado em massa)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE" # Mantém NEWLINE como um token se for necessário para o parser
    return t

# --- PALAVRAS-CHAVE RESERVADAS E IDENTIFICADORES ---
# Mapeia strings para seus TokenType específicos
# Palavras-chave GuruDev® (minúsculas para lookups case-insensitive ou exatas)
# A ordem aqui é importante para PLY se houver sobreposição (ex: 'if' antes de 'identifier')
# PLY usa a ordem das regras t_ para desempate entre regexes que casam o mesmo prefixo.
# A função t_ID é a que verifica `reserved`.

reserved = {
    # Casos gramaticais
    'VOC': 'VOCATIVO', 'NOM': 'NOMINATIVO', 'ACU': 'ACUSATIVO', 'DAT': 'DATIVO',
    'GEN': 'GENITIVO', 'INS': 'INSTRUMENTAL', 'LOC': 'LOCATIVO', 'ABL': 'ABLATIVO',
    
    # Estruturas e controle de fluxo
    'funcao': 'FUNCAO', 'classe': 'CLASSE', 'extends': 'EXTENDS', 'implements': 'IMPLEMENTS',
    'if': 'IF', 'se': 'IF', # Alias
    'else': 'ELSE', 'senao': 'ELSE', # Alias
    'for': 'FOR', 'para': 'FOR', # Alias
    'while': 'WHILE', 'enquanto': 'WHILE', # Alias
    'return': 'RETURN', 'retorna': 'RETURN', # Alias
    'break': 'BREAK', 'quebra': 'BREAK', # Alias
    'continue': 'CONTINUE', 'continua': 'CONTINUE', # Alias
    
    # Execução
    'serie': 'SERIE', 'paralelo': 'PARALELO', 'em': 'EM_KEYWORD', # 'em python'
    
    # Modificadores de acesso
    'publico': 'PUBLICO', 'privado': 'PRIVADO', 'protegido': 'PROTEGIDO',
    
    # Tipos de dados (PascalCase na EBNF, mas aqui minúsculas para match consistente)
    'Bool': 'BOOL_TYPE', 'String': 'STRING_TYPE', 'Int': 'INT_TYPE', 'Float': 'FLOAT_TYPE',
    'Void': 'VOID_TYPE', 'Array': 'ARRAY_TYPE', 'Object': 'OBJECT_TYPE', 'Formula': 'FORMULA_TYPE',
    'Temporal': 'TEMPORAL_TYPE', 'Imagem': 'IMAGEM_TYPE', 'Audio': 'AUDIO_TYPE',
    'Video': 'VIDEO_TYPE', 'Tabela': 'TABELA_TYPE', 'Grafo': 'GRAFO_TYPE',
    
    # Booleanos literais (podem ser palavras-chave)
    'true': 'BOOLEAN_LITERAL', 'false': 'BOOLEAN_LITERAL',
    'verdadeiro': 'BOOLEAN_LITERAL', 'falso': 'BOOLEAN_LITERAL', # Alias
}

def t_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*' # Permite caracteres acentuados
    # Checa por palavras reservadas (case-sensitive para tipos/casos, case-insensitive para aliases)
    # Primeiro checa case-sensitive
    t.type = reserved.get(t.value, 'ID')
    
    # Se não for match case-sensitive, tenta matchar case-insensitive para aliases
    if t.type == 'ID' and t.value.lower() in reserved and reserved[t.value.lower()] in [
        TokenType.IF, TokenType.ELSE, TokenType.FOR, TokenType.WHILE, TokenType.RETURN,
        TokenType.BREAK_KEYWORD, TokenType.CONTINUE_KEYWORD, TokenType.BOOLEAN_LITERAL # Para 'se', 'senao', etc.
    ]:
        t.type = reserved[t.value.lower()]
        
    return t

# --- REGRAS PARA TOKENS ESPECIAIS E ESTADOS DO LEXER ---

# Regras para os tokens de início/fim de blocos GuruDev® e de código estrangeiro.
# Essas regras devem mudar o estado do lexer.

# INITIAL state rules (when not inside any specific code block)
# Rules without 't_state_' prefix are active in all states or specifically in 'INITIAL'

# Estruturas GuruDev® principais
def t_BLOCK_START(t):
    r'\[bloco\]'
    return t

def t_BLOCK_END(t):
    r'\[/bloco\]'
    return t

def t_SOBRESCRITA_START(t):
    r'\[sobrescrita\]'
    t.lexer.begin('sobrescrita') # Entra no estado de sobrescrita
    return t

def t_SUBESCRITAS_START(t):
    r'\[subescritas\]'
    # Não muda de estado aqui, as tags de linguagem cuidarão disso.
    return t

def t_SUBESCRITAS_END(t):
    r'\[/subescritas\]'
    return t

def t_CODIGO_START(t):
    r'¡codigo!'
    t.lexer.begin('gurudevcode') # Entra no estado de código GuruDev®
    return t

# --- REGRAS PARA O ESTADO 'sobrescrita' ---
# Neste estado, esperamos strings de contexto, raiz, nível, etc.
# Ignora whitespace mas não comentários (eles são parte da string)
t_sobrescrita_ignore = ' \t'
t_sobrescrita_newline = r'\n+' # Permite newlines dentro da sobrescrita
def t_sobrescrita_newline(t):
    t.lexer.lineno += len(t.value)
    pass # Ignora newlines dentro da sobrescrita

# Atributos dentro de sobrescrita (NIVEL, RAIZ, CLAVE, ONT)
def t_sobrescrita_NIVEL_ATTR(t):
    r'\[nivel="([^"]+)"\]'
    # Mapeia o valor do atributo para um TokenType específico se existir, senão usa NIVEL_ATTR
    t.type = lex.lexer.nivel_map.get(t.value[8:-2].lower(), TokenType.NIVEL_ATTR)
    return t

def t_sobrescrita_RAIZ_ATTR(t):
    r'\[raiz="([^"]+)"\]'
    t.value = t.value[7:-2] # Extrai o valor da raiz (ex: CALC, LING)
    return t

def t_sobrescrita_CLAVE_ATTR(t):
    r'\[clave="([^"]+)"\]'
    t.type = lex.lexer.clave_map.get(t.value[7:-2].lower(), TokenType.CLAVE_ATTR)
    return t

def t_sobrescrita_ONT_ATTR(t): # [ont="substancia"]
    r'\[ont="([^"]+)"\]'
    t.type = lex.lexer.ont_map.get(t.value[5:-2].lower(), TokenType.ONT_ATTR)
    return t

# String literal (para "Contexto: descrição") dentro da sobrescrita
t_sobrescrita_STRING_LITERAL = r'"([^"\\]|\\.)*"'
def t_sobrescrita_STRING_LITERAL(t):
    t.value = t.value[1:-1] # Remove as aspas
    return t

# Fim da sobrescrita, volta ao estado INITIAL
def t_sobrescrita_SOBRESCRITA_END(t):
    r'\[/sobrescrita\]'
    t.lexer.begin('INITIAL') # Volta para o estado inicial
    return t

# Erro no estado sobrescrita
def t_sobrescrita_error(t):
    print(f"Caractere ilegal no bloco de sobrescrita '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# --- REGRAS PARA O ESTADO 'gurudevcode' ---
# Aqui, esperamos código GuruDev® normal.
# Ignoramos whitespace e newlines, e comentários, como em código normal.
t_gurudevcode_ignore = ' \t'
t_gurudevcode_newline = r'\n+'
def t_gurudevcode_newline(t):
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE" # Mantém NEWLINE como um token
    return t

t_gurudevcode_COMMENT_SINGLE_LINE = r'//[^\n]*'
t_gurudevcode_COMMENT_MULTI_LINE = r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
def t_gurudevcode_COMMENT_MULTI_LINE(t):
    t.lexer.lineno += t.value.count('\n')
    pass

# Inclui todas as regras de tokens simples/operadores/literais/IDs para o estado gurudevcode
# Palavras-chave e IDs (t_ID, t_FLOAT_LITERAL, t_INT_LITERAL, t_STRING_LITERAL, etc.)
# Essas regras são as mesmas da INITIAL, mas ativas especificamente no estado gurudevcode
# PLY requer que as regras sejam prefixadas com t_nomedostate_
# Por exemplo: t_gurudevcode_LPAREN = r'\('

# Para evitar duplicação de regexes, pode-se iterar e criar dinamicamente as regras
# OU copiar/colar as regras de t_ inicial para t_gurudevcode_
# Abaixo, estamos listando as regras que seriam prefixadas.

# Copie as regras t_ para gurudevcode aqui. Ex:
t_gurudevcode_LPAREN = r'\('
t_gurudevcode_RPAREN = r'\)'
t_gurudevcode_LBRACE = r'\{'
t_gurudevcode_RBRACE = r'\}'
t_gurudevcode_LBRACKET = r'\['
t_gurudevcode_RBRACKET = r'\]'
t_gurudevcode_SEMICOLON = r';'
t_gurudevcode_COMMA = r','
t_gurudevcode_DOT = r'\.'
t_gurudevcode_ASSIGN = r'='
t_gurudevcode_PLUS = r'\+'
t_gurudevcode_MINUS = r'-'
t_gurudevcode_TIMES = r'\*'
t_gurudevcode_DIVIDE = r'/'
t_gurudevcode_MODULO = r'%'
t_gurudevcode_LESS_THAN = r'<'
t_gurudevcode_GREATER_THAN = r'>'
t_gurudevcode_NOT = r'!'
t_gurudevcode_COLON = r':'
t_gurudevcode_EQUALS = r'=='
t_gurudevcode_NOT_EQUALS = r'!='
t_gurudevcode_LESS_EQUAL = r'<='
t_gurudevcode_GREATER_EQUAL = r'>='
t_gurudevcode_AND = r'&&'
t_gurudevcode_OR = r'\|\|'
t_gurudevcode_ARROW = r'->'

def t_gurudevcode_FLOAT_LITERAL(t):
    r'\d+\.\d+f?'
    t.value = float(t.value.replace('f', ''))
    return t

def t_gurudevcode_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_gurudevcode_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_gurudevcode_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    # A lógica case-insensitive para aliases tbm se aplicaria aqui
    if t.type == 'ID' and t.value.lower() in reserved and reserved[t.value.lower()] in [
        TokenType.IF, TokenType.ELSE, TokenType.FOR, TokenType.WHILE, TokenType.RETURN,
        TokenType.BREAK_KEYWORD, TokenType.CONTINUE_KEYWORD, TokenType.BOOLEAN_LITERAL # Para 'se', 'senao', etc.
    ]:
        t.type = reserved[t.value.lower()]
    return t


# Fim do bloco de código GuruDev®, volta ao estado INITIAL
def t_gurudevcode_CODIGO_END(t):
    r'!/codigo!'
    t.lexer.begin('INITIAL') # Volta para o estado inicial
    return t

# Erro no estado gurudevcode
def t_gurudevcode_error(t):
    print(f"Caractere ilegal no bloco de código GuruDev® '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# --- REGRAS PARA O ESTADO 'foreigncode' ---
# Este estado consome TUDO como conteúdo bruto até encontrar a tag de fim da linguagem.
def t_foreigncode_FOREIGN_CODE_CONTENT(t):
    # Procura pela próxima tag de fim de linguagem.
    # A ordem dos padrões PLY é a que dita a prioridade de match.
    # Precisamos encontrar o *primeiro* end tag de QUALQUER linguagem que esteja ativa para a subescrita.
    
    # Essa regex é simplificada. Numa implementação real, você precisaria de um
    # mecanismo mais sofisticado que busque pelo SELF.foreign_end_token.pattern_string
    # para evitar capturar end_tags de outras linguagens por engano.
    # Por exemplo: `re.search(r'\?/python\?', t.lexer.lexdata, t.lexer.lexpos)`
    # Isso exigiria uma lógica mais customizada no t_foreigncode_FOREIGN_CODE_CONTENT ou em uma função auxiliar.
    
    # Por enquanto, esta regra genérica captura tudo exceto o início de um novo bloco ou fim de linha,
    # mas o desafio é que PLY não sabe qual é o 'end_token' específico que está sendo procurado.
    # A melhor abordagem em PLY para isso é ter uma regra t_FOREIGN_CODE_CONTENT para CADA par de início/fim
    # e que cada t_LANG_START defina o que está procurando.
    # Exemplo: t_foreigncode_python_CONTENT
    
    # Devido à complexidade do PLY com estados dinâmicos para a mesma regra,
    # a maneira mais PLY-idiomática é ter regras separadas para CADA LINGUAGEM ESTRANGEIRA NO ESTADO ESTRANGEIRO.
    # Ex:
    # states = (..., ('python_state', 'exclusive'), ('javascript_state', 'exclusive'), ...)
    # def t_python_state_PYTHON_END(t): ...
    # def t_python_state_content(t): r'.|\n'
    # Essa abordagem evita a necessidade do `foreign_end_token` no lexer.
    
    # Pela sua proposta de um ÚNICO FOREIGN_CODE_CONTENT, isso é mais complexo no PLY.
    # Uma solução seria ter um mapa de regexes de fim no t.lexer, e o t_foreigncode_FOREIGN_CODE_CONTENT
    # teria um regex negativo que não casa com NENHUM dos end_tags.
    
    # Para simplicidade e para que o PLY consiga fazer o match:
    # Vamos ter regras específicas para cada linguagem, mesmo no estado 'foreigncode'
    # E vamos precisar de regras t_LANG_START para entrar em estados específicos de linguagem (ex: python_code)
    # Isso vai simplificar a lógica do FOREIGN_CODE_CONTENT

    # Este é um placeholder, a implementação real exigiria estados específicos por linguagem estrangeira.
    r'(.*?)(?=\?/python\?|\?/rust\?|\?/javascript\?|\?/csharp\?|\?/wasm\?|\?/c\+\+\?|\?/java\?|\?/sql\?|\?/r\?)'
    # Esta regex buscará todo o conteúdo até o próximo fechamento de qualquer linguagem.
    # Em um sistema real, você teria estados específicos por linguagem (e.g., python_STATE, rust_STATE)
    # para que t_python_STATE_CONTENT só procure por ?/python?.
    
    # Para o propósito desta resposta, assumindo que PLY vai fazer o longest match
    # e que t_LANG_END será tratado primeiro se aparecer.
    # O conteúdo bruto precisa ser tratado.
    t.type = 'FOREIGN_CODE_CONTENT'
    # Ajustar linhas/colunas para o conteúdo
    t.lexer.lineno += t.value.count('\n')
    return t

# Regras de início de linguagem que entram em estado `foreigncode`
# (estas regras são ativas no estado INITIAL e no estado `gurudevcode` para `em python { }`)

# Python
def t_PYTHON_START(t):
    r'¿python\?'
    t.lexer.begin('foreigncode') # Entra no estado de código estrangeiro genérico
    t.lexer.language_end_marker = r'\?/python\?' # Guarda o marcador de fim esperado
    t.type = 'PYTHON_START'
    return t

# Rust
def t_RUST_START(t):
    r'¿rust\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/rust\?'
    t.type = 'RUST_START'
    return t

# JavaScript
def t_JAVASCRIPT_START(t):
    r'¿javascript\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/javascript\?'
    t.type = 'JAVASCRIPT_START'
    return t

# C#
def t_CSHARP_START(t):
    r'¿csharp\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/csharp\?'
    t.type = 'CSHARP_START'
    return t

# WebAssembly
def t_WASM_START(t):
    r'¿wasm\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/wasm\?'
    t.type = 'WASM_START'
    return t

# C++
def t_CPP_START(t):
    r'¿c\+\+\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/c\+\+\?'
    t.type = 'CPP_START'
    return t

# Java
def t_JAVA_START(t):
    r'¿java\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/java\?'
    t.type = 'JAVA_START'
    return t

# SQL
def t_SQL_START(t):
    r'¿sql\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/sql\?'
    t.type = 'SQL_START'
    return t

# R
def t_R_START(t):
    r'¿r\?'
    t.lexer.begin('foreigncode')
    t.lexer.language_end_marker = r'\?/r\?'
    t.type = 'R_START'
    return t


# Regra para tokens de fim de linguagem dentro do estado `foreigncode`
# Precisa de uma função para cada tipo de linguagem, pois a regra t_ precisa ser específica.
# E o lexer precisa saber qual END token ele está buscando.
# PLY não tem um mecanismo para "t.lexer.end_pattern = pattern" e uma única regra genérica
# O mais idiomático é ter um estado por linguagem estrangeira.
# Para manter 'foreigncode' genérico, precisamos uma ordem de regras que priorize os END tokens.

def t_foreigncode_PYTHON_END(t):
    r'\?/python\?'
    if t.lexer.language_end_marker == r'\?/python\?': # Verifica se é o marcador esperado
        t.lexer.begin('INITIAL') # Volta para o estado inicial
        return t
    else:
        # Se não for o end token esperado, trata como parte do FOREIGN_CODE_CONTENT
        t.lexer.skip(1) # Avança 1 e tenta de novo

def t_foreigncode_RUST_END(t):
    r'\?/rust\?'
    if t.lexer.language_end_marker == r'\?/rust\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

def t_foreigncode_JAVASCRIPT_END(t):
    r'\?/javascript\?'
    if t.lexer.language_end_marker == r'\?/javascript\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

def t_foreigncode_CSHARP_END(t):
    r'\?/csharp\?'
    if t.lexer.language_end_marker == r'\?/csharp\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

def t_foreigncode_WASM_END(t):
    r'\?/wasm\?'
    if t.lexer.language_end_marker == r'\?/wasm\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

def t_foreigncode_CPP_END(t):
    r'\?/c\+\+\?'
    if t.lexer.language_end_marker == r'\?/c\+\+\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

def t_foreigncode_JAVA_END(t):
    r'\?/java\?'
    if t.lexer.language_end_marker == r'\?/java\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

def t_foreigncode_SQL_END(t):
    r'\?/sql\?'
    if t.lexer.language_end_marker == r'\?/sql\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

def t_foreigncode_R_END(t):
    r'\?/r\?'
    if t.lexer.language_end_marker == r'\?/r\?':
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.skip(1)

# Esta regra captura o *conteúdo* do código estrangeiro. Deve ser a última regra no estado 'foreigncode'.
# Ela precisa ser cuidadosa para não capturar o próprio marcador de fim.
# A regex `r'.|\n'` em um estado 'exclusive' captura tudo, e as regras de FIM devem ser ativadas antes.
def t_foreigncode_FOREIGN_CODE_CONTENT(t):
    r'.|\n' # Captura qualquer caractere, incluindo newline
    t.lexer.lineno += t.value.count('\n')
    t.type = 'FOREIGN_CODE_CONTENT'
    return t


# Tratamento de erros para o estado foreigncode
def t_foreigncode_error(t):
    print(f"Caractere ilegal no bloco de código estrangeiro '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)


# --- TRATAMENTO DE ERROS GERAIS ---
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex(
    # Para depuração, descomente a linha abaixo
    # debug=True,
    # Regras t_ podem ser definidas globalmente ou passadas em módulos
    # Mas aqui estão definidas diretamente para simplificar o exemplo.
)

# --- FUNÇÃO DE TOKENIZAÇÃO E DEMO ---
def tokenize_gurudev_code(code: str) -> List[lex.LexToken]:
    lexer.input(code)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    return tokens_list

# Exemplo de uso (para teste interno)
if __name__ == '__main__':
    code_example = """
[bloco]
    [sobrescrita]
        "Contexto: Camada de segurança: autenticação"
        "Raiz semântica: SEG"
        [nivel="holistico"]
        [ont="acao"]
    [/sobrescrita]

    ¡codigo!
    serie { // Bloco de execução em série
        em python { dados = processar_csv("usuarios.csv") }
        em rust { resultado = validar(dados) }
    }

    NOM funcao verificarSenha(String senhaInserida, String senhaHashArmazenada) {
        return hash(senhaInserida) == hash(senhaHashArmazenada);
    }
    !/codigo!

    [subescritas]
        ¿rust?
        fn verificar_senha(senha_inserida: &str, senha_armazenada: &str) -> bool {
            // Este é um comentário dentro do Rust
            hash(senha_inserida) == hash(senha_armazenada)
        }
        ?/rust?

        ¿python?
        def verificar_senha(senha_inserida, senha_armazenada):
            # Outro comentário Python
            return hash(senha_inserida) == hash(senha_armazenada)
        ?/python?
    [/subescritas]
[/bloco]

VOC.minhaFuncao();
ACU.variavel = 123;
Float altura = 1.75f;
String nome = "Guilherme";
// Este é um comentário de linha única GuruDev
/* Este é um comentário
   de múltiplas linhas GuruDev */
if (x == 10) { return true; }
"Outra string com \"aspas\" dentro"
"""

    tokens = tokenize_gurudev_code(code_example)
    print("=== TOKENS GERADOS ===")
    for tok in tokens:
        # Excluir WHITESPACE para uma saída mais limpa, mas o lexer o produz
        if tok.type != 'WHITESPACE':
            print(tok)

    print(f"\nTotal de tokens: {len(tokens)}")
