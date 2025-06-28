import ply.lex as lex
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict

# --- 1. DEFINIÇÃO DOS TIPOS DE TOKENS (Enum) ---
class TokenType(Enum):
    # Estruturas principais de blocos
    BLOCO_START = "BLOCO_START"                 # [bloco]
    BLOCO_END = "BLOCO_END"                     # [/bloco]
    SOBRESCRITA_START = "SOBRESCRITA_START"     # [sobrescrita]
    SOBRESCRITA_END = "SOBRESCRITA_END"         # [/sobrescrita]
    SUBESCRITAS_START = "SUBESCRITAS_START"     # [subescritas]
    SUBESCRITAS_END = "SUBESCRITAS_END"         # [/subescritas]
    
    # Delimitadores de código GuruDev®
    CODIGO_START = "CODIGO_START"               # ¡codigo!
    CODIGO_END = "CODIGO_END"                   # !/codigo!
    
    # Subescritas específicas de linguagens (start/end tags)
    PYTHON_START = "PYTHON_START"               # ¿python?
    PYTHON_END = "PYTHON_END"                   # ?/python?
    RUST_START = "RUST_START"                   # ¿rust?
    RUST_END = "RUST_END"                       # ?/rust?
    JAVASCRIPT_START = "JAVASCRIPT_START"       # ¿javascript?
    JAVASCRIPT_END = "JAVASCRIPT_END"           # ?/javascript?
    CSHARP_START = "CSHARP_START"               # ¿csharp?
    CSHARP_END = "CSHARP_END"                   # ?/csharp?
    WASM_START = "WASM_START"                   # ¿wasm?
    WASM_END = "WASM_END"                       # ?/wasm?
    CPP_START = "CPP_START"                     # ¿c++?
    CPP_END = "CPP_END"                         # ?/c++?
    JAVA_START = "JAVA_START"                   # ¿java?
    JAVA_END = "JAVA_END"                       # ?/java?
    SQL_START = "SQL_START"                     # ¿sql?
    SQL_END = "SQL_END"                         # ?/sql?
    R_START = "R_START"                         # ¿r?
    R_END = "R_END"                             # ?/r?
    
    # Conteúdo bruto de código estrangeiro
    FOREIGN_CODE_CONTENT = "FOREIGN_CODE_CONTENT"
    
    # Atributos e metadados (para [nivel=""], [raiz=""], [clave=""], [ont=""])
    NIVEL_ATTR = "NIVEL_ATTR"                   # [nivel="literal"]
    RAIZ_ATTR = "RAIZ_ATTR"                     # [raiz="SEG"]
    CLAVE_ATTR = "CLAVE_ATTR"                   # [clave="arte"]
    ONT_ATTR = "ONT_ATTR"                       # [ont="substancia"]
    
    # Níveis hermenêuticos (valores específicos)
    NIVEL_LITERAL = "NIVEL_LITERAL"             # Mapeado de [nivel="literal"]
    NIVEL_ALEGORICO = "NIVEL_ALEGORICO"         # Mapeado de [nivel="alegorico"]
    NIVEL_MORAL = "NIVEL_MORAL"                 # Mapeado de [nivel="moral"]
    NIVEL_MISTICO = "NIVEL_MISTICO"             # Mapeado de [nivel="mistico"]
    NIVEL_FUNCIONAL = "NIVEL_FUNCIONAL"         # Mapeado de [nivel="funcional"]
    NIVEL_ESTETICO = "NIVEL_ESTETICO"           # Mapeado de [nivel="estetico"]
    NIVEL_ONTOLOGICO = "NIVEL_ONTOLOGICO"       # Mapeado de [nivel="ontologico"]
    NIVEL_HOLISTICO = "NIVEL_HOLISTICO"         # Mapeado de [nivel="holistico"]
    NIVEL_MATEMATICO = "NIVEL_MATEMATICO"       # Mapeado de [nivel="matematico"]
    NIVEL_SIMBOLICO = "NIVEL_SIMBOLICO"         # Mapeado de [nivel="simbolico"]
    NIVEL_PARABOLICO = "NIVEL_PARABOLICO"       # Adicionado conforme o PDF
    NIVEL_HISTORICO = "NIVEL_HISTORICO"         # Adicionado conforme o PDF
    NIVEL_LINGUISTICO = "NIVEL_LINGUISTICO"     # Adicionado conforme o PDF

    # Claves de campo semântico (valores específicos)
    CLAVE_ARTE = "CLAVE_ARTE"                   # Mapeado de [clave="arte"]
    CLAVE_CIENCIA = "CLAVE_CIENCIA"             # Mapeado de [clave="ciencia"]
    CLAVE_FILOSOFIA = "CLAVE_FILOSOFIA"         # Mapeado de [clave="filosofia"]
    CLAVE_TRADICAO = "CLAVE_TRADICAO"           # Mapeado de [clave="tradicao"] (ou espiritual)
    CLAVE_GERAL = "CLAVE_GERAL"                 # Mapeado de [clave="geral"]
    
    # Categorias aristotélicas (valores específicos)
    ONT_SUBSTANCIA = "ONT_SUBSTANCIA"
    ONT_QUANTIDADE = "ONT_QUANTIDADE"
    ONT_QUALIDADE = "ONT_QUALIDADE"
    ONT_RELACAO = "ONT_RELACAO"
    ONT_LUGAR = "ONT_LUGAR"
    ONT_TEMPO = "ONT_TEMPO"
    ONT_SITUACAO = "ONT_SITUACAO"
    ONT_CONDICAO = "ONT_CONDICAO"
    ONT_ACAO = "ONT_ACAO"
    ONT_PAIXAO = "ONT_PAIXAO"
    
    # Palavras-chave da GuruDev® (Casos gramaticais e outros)
    VOC = "VOC"                                 # VOCATIVO
    NOM = "NOM"                                 # NOMINATIVO
    ACU = "ACU"                                 # ACUSATIVO
    DAT = "DAT"                                 # DATIVO
    GEN = "GEN"                                 # GENITIVO
    INS = "INS"                                 # INSTRUMENTAL
    LOC = "LOC"                                 # LOCATIVO
    ABL = "ABL"                                 # ABLATIVO
    FUNCAO = "FUNCAO"                           # funcao
    CLASSE = "CLASSE"                           # classe
    EXTENDS = "EXTENDS"                         # extends
    IMPLEMENTS = "IMPLEMENTS"                   # implements
    
    # Tipos de dados
    BOOL_TYPE = "BOOL_TYPE"                     # Bool
    STRING_TYPE = "STRING_TYPE"                 # String
    INT_TYPE = "INT_TYPE"                       # Int
    FLOAT_TYPE = "FLOAT_TYPE"                   # Float
    VOID_TYPE = "VOID_TYPE"                     # Void
    ARRAY_TYPE = "ARRAY_TYPE"                   # Array<T>
    OBJECT_TYPE = "OBJECT_TYPE"                 # Object<T>
    FORMULA_TYPE = "FORMULA_TYPE"               # Formula
    TEMPORAL_TYPE = "TEMPORAL_TYPE"             # Temporal
    IMAGEM_TYPE = "IMAGEM_TYPE"                 # Imagem
    AUDIO_TYPE = "AUDIO_TYPE"                   # Audio
    VIDEO_TYPE = "VIDEO_TYPE"                   # Video
    TABELA_TYPE = "TABELA_TYPE"                 # Tabela<T>
    GRAFO_TYPE = "GRAFO_TYPE"                   # Grafo<K, V>

    # Controle de fluxo
    IF_KEYWORD = "IF_KEYWORD"                   # if/se
    ELSE_KEYWORD = "ELSE_KEYWORD"               # else/senao
    FOR_KEYWORD = "FOR_KEYWORD"                 # for/para
    WHILE_KEYWORD = "WHILE_KEYWORD"             # while/enquanto
    RETURN_KEYWORD = "RETURN_KEYWORD"           # return/retorna
    BREAK_KEYWORD = "BREAK_KEYWORD"             # break/quebra
    CONTINUE_KEYWORD = "CONTINUE_KEYWORD"       # continue/continua
    
    # Execução série/paralelo
    SERIE_KEYWORD = "SERIE_KEYWORD"             # serie
    PARALELO_KEYWORD = "PARALELO_KEYWORD"       # paralelo
    EM_KEYWORD = "EM_KEYWORD"                   # em (em python, em rust)
    
    # Modificadores de acesso
    PUBLICO = "PUBLICO"                         # publico
    PRIVADO = "PRIVADO"                         # privado
    PROTEGIDO = "PROTEGIDO"                     # protegido
    
    # Tokens básicos (capturados pelas regras t_...)
    ID = "ID"                                   # nomes de variáveis, funções
    
    # Tokens especiais (não incluídos no `tokens` para serem passados por `pass` ou tratados no t_error)
    COMMENT = "COMMENT"                         # //, /* */
    WHITESPACE = "WHITESPACE"                   # espaço, tab
    NEWLINE = "NEWLINE"                         # quebra de linha
    EOF = "EOF"                                 # Fim do arquivo
    
    # Operadores
    ASSIGN = "ASSIGN"                           # =
    EQUALS = "EQUALS"                           # ==
    NOT_EQUALS = "NOT_EQUALS"                   # !=
    LESS_THAN = "LESS_THAN"                     # <
    GREATER_THAN = "GREATER_THAN"               # >
    LESS_EQUAL = "LESS_EQUAL"                   # <=
    GREATER_EQUAL = "GREATER_EQUAL"             # >=
    PLUS = "PLUS"                               # +
    MINUS = "MINUS"                             # -
    MULTIPLY = "MULTIPLY"                       # *
    DIVIDE = "DIVIDE"                           # /
    MODULO = "MODULO"                           # %
    AND = "AND"                                 # &&
    OR = "OR"                                   # ||
    NOT = "NOT"                                 # !
    
    # Delimitadores
    LBRACE = "LBRACE"                           # {
    RBRACE = "RBRACE"                           # }
    LPAREN = "LPAREN"                           # (
    RPAREN = "RPAREN"                           # )
    LBRACKET = "LBRACKET"                       # [
    RBRACKET = "RBRACKET"                       # ]
    SEMICOLON = "SEMICOLON"                     # ;
    COMMA = "COMMA"                             # ,
    DOT = "DOT"                                 # .
    COLON = "COLON"                             # :

# --- 2. CLASSE PARA REPRESENTAR UM TOKEN (PLY já tem, mas bom para clareza) ---
# PLY já usa um objeto 'LexToken' internamente, mas mantemos o dataclass para clareza em demos.
# A função tokenize_gurudev_code irá retornar objetos LexToken diretamente.
@dataclass
class Token:
    type: TokenType # Ou str para compatibilidade com ply.lex.LexToken.type
    value: str
    line: int
    column: int

# --- 3. ESTADOS DO LEXER (MÁQUINA DE ESTADOS) ---
# Define os estados do lexer:
# 'INITIAL': Estado padrão (fora de qualquer bloco de código específico GuruDev® ou estrangeiro).
# 'sobrescrita_state': Para o conteúdo da seção [sobrescrita].
# 'gurudevcode_state': Para o código GuruDev® dentro de ¡codigo! ... !/codigo!.
# '[lang]_code_state': Para o código de linguagens estrangeiras (Python, Rust, etc.).
states = (
    ('sobrescrita_state', 'exclusive'),
    ('gurudevcode_state', 'exclusive'),
    ('python_code_state', 'exclusive'),
    ('rust_code_state', 'exclusive'),
    ('javascript_code_state', 'exclusive'),
    ('csharp_code_state', 'exclusive'),
    ('wasm_code_state', 'exclusive'),
    ('cpp_code_state', 'exclusive'),
    ('java_code_state', 'exclusive'),
    ('sql_code_state', 'exclusive'),
    ('r_code_state', 'exclusive'),
)

# --- 4. EXPRESSÕES REGULARES PARA TOKENS ---
# A ordem das regras é importante para PLY (longest match wins, depois ordem de definição)

# REGRA GLOBAL: Caracteres ignorados (espaços e tabs) - ativo em todos os estados por padrão
t_ignore = ' \t'

# --- 4.1. REGRAS ATIVAS NO ESTADO INITIAL ---

# Estruturas de Blocos Principais (mudam de estado)
def t_SOBRESCRITA_START(t):
    r'\[sobrescrita\]'
    t.lexer.begin('sobrescrita_state') # Entra no estado de sobrescrita
    return t

def t_CODIGO_START(t):
    r'¡codigo!'
    t.lexer.begin('gurudevcode_state') # Entra no estado de código GuruDev®
    return t

# Regras de início/fim de subescritas (não mudam de estado sozinhas, mas delimitam)
t_SUBESCRITAS_START = r'\[subescritas\]'
t_SUBESCRITAS_END = r'\[/subescritas\]'

# Regras para os tokens BLOCO_START/END
t_BLOCO_START = r'\[bloco\]'
t_BLOCO_END = r'\[/bloco\]'


# Regras para tags de início de linguagens estrangeiras (mudam para estados específicos)
def t_PYTHON_START(t):
    r'¿python\?'
    t.lexer.begin('python_code_state')
    return t

def t_RUST_START(t):
    r'¿rust\?'
    t.lexer.begin('rust_code_state')
    return t

def t_JAVASCRIPT_START(t):
    r'¿javascript\?'
    t.lexer.begin('javascript_code_state')
    return t

def t_CSHARP_START(t):
    r'¿csharp\?'
    t.lexer.begin('csharp_code_state')
    return t

def t_WASM_START(t):
    r'¿wasm\?'
    t.lexer.begin('wasm_code_state')
    return t

def t_CPP_START(t):
    r'¿c\+\+\?'
    t.lexer.begin('cpp_code_state')
    return t

def t_JAVA_START(t):
    r'¿java\?'
    t.lexer.begin('java_code_state')
    return t

def t_SQL_START(t):
    r'¿sql\?'
    t.lexer.begin('sql_code_state')
    return t

def t_R_START(t):
    r'¿r\?'
    t.lexer.begin('r_code_state')
    return t

# --- REGRAS PARA TOKENS COMUNS A MAIS DE UM ESTADO (não prefixadas com t_state_) ---
# PLY irá usar estas regras se não houver uma regra mais específica no estado atual.
# Para evitar duplicação em t_gurudevcode_, etc., estas regras são definidas globalmente
# e assumimos que o parser vai re-tokenizar o conteúdo gurudevcode_state com essas mesmas regras.
# No entanto, a forma mais idiomática PLY para regras que são as mesmas em vários estados
# é duplicá-las com os prefixos (t_gurudevcode_LPAREN = r'\(') ou usar `module` para organizar.

# Operadores de múltiplos caracteres (ordem importa para match)
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_ARROW = r'->'

# Operadores de um caractere
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

# Delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'


# Comentários (ignoram o conteúdo, mas contam linhas se multilinhas)
def t_COMMENT_SINGLE_LINE(t):
    r'//[^\n]*'
    pass # Ignora o token

def t_COMMENT_MULTI_LINE(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    t.lexer.lineno += t.value.count('\n') # Conta novas linhas
    pass # Ignora o token

# Controle de linha (para newlines fora de conteúdo que é tokenizado em massa)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE" # Mantém NEWLINE como um token se for necessário para o parser
    return t

# Literais
def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1] # Remove as aspas
    return t

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+f?' # Permite sufixo 'f' para float
    t.value = float(t.value.replace('f', ''))
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Palavras-chave e Identificadores
reserved = {
    # Casos gramaticais (sempre maiúsculos nas regras GuruDev®)
    'VOC': 'VOC', 'NOM': 'NOM', 'ACU': 'ACU', 'DAT': 'DAT',
    'GEN': 'GEN', 'INS': 'INS', 'LOC': 'LOC', 'ABL': 'ABL',
    
    # Estruturas e controle de fluxo (minúsculas ou PascalCase)
    'funcao': 'FUNCAO', 'classe': 'CLASSE', 'extends': 'EXTENDS', 'implements': 'IMPLEMENTS',
    'if': 'IF_KEYWORD', 'se': 'IF_KEYWORD', # Alias
    'else': 'ELSE_KEYWORD', 'senao': 'ELSE_KEYWORD', # Alias
    'for': 'FOR_KEYWORD', 'para': 'FOR_KEYWORD', # Alias
    'while': 'WHILE_KEYWORD', 'enquanto': 'WHILE_KEYWORD', # Alias
    'return': 'RETURN_KEYWORD', 'retorna': 'RETURN_KEYWORD', # Alias
    'break': 'BREAK_KEYWORD', 'quebra': 'BREAK_KEYWORD', # Alias
    'continue': 'CONTINUE_KEYWORD', 'continua': 'CONTINUE_KEYWORD', # Alias
    
    # Execução
    'serie': 'SERIE_KEYWORD', 'paralelo': 'PARALELO_KEYWORD', 'em': 'EM_KEYWORD', # 'em python'
    
    # Modificadores de acesso
    'publico': 'PUBLICO', 'privado': 'PRIVADO', 'protegido': 'PROTEGIDO',
    
    # Tipos de dados (PascalCase)
    'Bool': 'BOOL_TYPE', 'String': 'STRING_TYPE', 'Int': 'INT_TYPE', 'Float': 'FLOAT_TYPE',
    'Void': 'VOID_TYPE', 'Array': 'ARRAY_TYPE', 'Object': 'OBJECT_TYPE', 'Formula': 'FORMULA_TYPE',
    'Temporal': 'TEMPORAL_TYPE', 'Imagem': 'IMAGEM_TYPE', 'Audio': 'AUDIO_TYPE',
    'Video': 'VIDEO_TYPE', 'Tabela': 'TABELA_TYPE', 'Grafo': 'GRAFO_TYPE',
    
    # Booleanos literais (minúsculas)
    'true': 'BOOLEAN_LITERAL', 'false': 'BOOLEAN_LITERAL',
    'verdadeiro': 'BOOLEAN_LITERAL', 'falso': 'BOOLEAN_LITERAL', # Alias
}

def t_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*' # Permite caracteres acentuados
    # Prioriza palavras-chave exatas (case-sensitive para tipos e casos gramaticais)
    t.type = reserved.get(t.value, 'ID')
    
    # Se não for uma palavra-chave exata, verifica se é um alias (ex: 'se' para 'if_KEYWORD')
    # O valor original 't.value' é preservado.
    if t.type == 'ID' and t.value.lower() in reserved:
        # Pega o tipo da palavra-chave em minúsculas
        lower_type = reserved[t.value.lower()]
        # Se for um tipo BOOLEAN_LITERAL ou um alias de controle de fluxo, atribui esse tipo
        if lower_type == TokenType.BOOLEAN_LITERAL or lower_type in [
            TokenType.IF_KEYWORD, TokenType.ELSE_KEYWORD, TokenType.FOR_KEYWORD,
            TokenType.WHILE_KEYWORD, TokenType.RETURN_KEYWORD,
            TokenType.BREAK_KEYWORD, TokenType.CONTINUE_KEYWORD
        ]:
            t.type = lower_type
    return t


# --- 4.2. REGRAS PARA O ESTADO 'sobrescrita_state' ---
# Este estado é para o conteúdo dentro de [sobrescrita]...[/sobrescrita]
t_sobrescrita_ignore = ' \t'

def t_sobrescrita_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass # Ignora newlines dentro da sobrescrita (não as retorna como tokens)

# Atributos dentro de sobrescrita ([nivel=""], [raiz=""], [clave=""], [ont=""])
def t_sobrescrita_NIVEL_ATTR(t):
    r'\[nivel="([^"]+)"\]'
    # Mapeia o valor interno (group 1) para um TokenType específico se existir, senão usa NIVEL_ATTR
    # Pega o valor entre aspas e converte para minúsculas
    attr_value = t.value[t.value.find('"')+1 : t.value.rfind('"')].lower()
    t.type = lex.lexer.nivel_map.get(attr_value, TokenType.NIVEL_ATTR)
    return t

def t_sobrescrita_RAIZ_ATTR(t):
    r'\[raiz="([^"]+)"\]'
    # Extrai o valor da raiz (ex: CALC, LING)
    t.value = t.value[t.value.find('"')+1 : t.value.rfind('"')]
    return t

def t_sobrescrita_CLAVE_ATTR(t):
    r'\[clave="([^"]+)"\]'
    attr_value = t.value[t.value.find('"')+1 : t.value.rfind('"')].lower()
    t.type = lex.lexer.clave_map.get(attr_value, TokenType.CLAVE_ATTR)
    return t

def t_sobrescrita_ONT_ATTR(t):
    r'\[ont="([^"]+)"\]'
    attr_value = t.value[t.value.find('"')+1 : t.value.rfind('"')].lower()
    t.type = lex.lexer.ont_map.get(attr_value, TokenType.ONT_ATTR)
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
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}' no bloco de sobrescrita na linha {t.lexer.lineno}, coluna {t.lexer.lexpos - t.lexer.lineno_start_pos + 1}")
    t.lexer.skip(1)

# --- 4.3. REGRAS PARA O ESTADO 'gurudevcode_state' ---
# Neste estado, esperamos código GuruDev® normal.
t_gurudevcode_ignore = ' \t'

def t_gurudevcode_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE" # Mantém NEWLINE como um token
    return t

# Comentários dentro do código GuruDev®
t_gurudevcode_COMMENT_SINGLE_LINE = r'//[^\n]*'
t_gurudevcode_COMMENT_MULTI_LINE = r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
def t_gurudevcode_COMMENT_MULTI_LINE(t):
    t.lexer.lineno += t.value.count('\n')
    pass

# Regras de tokens GuruDev® (copiadas das regras globais, mas agora prefixadas)
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

def t_gurudevcode_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_gurudevcode_FLOAT_LITERAL(t):
    r'\d+\.\d+f?'
    t.value = float(t.value.replace('f', ''))
    return t

def t_gurudevcode_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_gurudevcode_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    if t.type == 'ID' and t.value.lower() in reserved:
        lower_type = reserved[t.value.lower()]
        if lower_type == TokenType.BOOLEAN_LITERAL or lower_type in [
            TokenType.IF_KEYWORD, TokenType.ELSE_KEYWORD, TokenType.FOR_KEYWORD,
            TokenType.WHILE_KEYWORD, TokenType.RETURN_KEYWORD,
            TokenType.BREAK_KEYWORD, TokenType.CONTINUE_KEYWORD
        ]:
            t.type = lower_type
    return t


# Fim do bloco de código GuruDev®, volta ao estado INITIAL
def t_gurudevcode_CODIGO_END(t):
    r'!/codigo!'
    t.lexer.begin('INITIAL') # Volta para o estado inicial
    return t

# Erro no estado gurudevcode
def t_gurudevcode_error(t):
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}' no bloco de código GuruDev® na linha {t.lexer.lineno}, coluna {t.lexer.lexpos - t.lexer.lineno_start_pos + 1}")
    t.lexer.skip(1)

# --- 4.4. REGRAS PARA ESTADOS DE CÓDIGO ESTRANGEIRO (EXCLUSIVOS) ---
# Cada estado de código estrangeiro tem suas próprias regras de conteúdo e fim.

# Python Code State
t_python_code_state_ignore = ' \t'
def t_python_code_state_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    return t

def t_python_code_state_PYTHON_END(t):
    r'\?/python\?'
    t.lexer.begin('INITIAL')
    return t

def t_python_code_state_FOREIGN_CODE_CONTENT(t):
    r'.|\n' # Captura qualquer caractere, incluindo newline
    t.lexer.lineno += t.value.count('\n')
    return t

def t_python_code_state_error(t):
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}' no bloco Python na linha {t.lexer.lineno}, coluna {t.lexer.lexpos - t.lexer.lineno_start_pos + 1}")
    t.lexer.skip(1)


# Rust Code State
t_rust_code_state_ignore = ' \t'
def t_rust_code_state_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    return t

def t_rust_code_state_RUST_END(t):
    r'\?/rust\?'
    t.lexer.begin('INITIAL')
    return t

def t_rust_code_state_FOREIGN_CODE_CONTENT(t):
    r'.|\n'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_rust_code_state_error(t):
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}' no bloco Rust na linha {t.lexer.lineno}, coluna {t.lexer.lexpos - t.lexer.lineno_start_pos + 1}")
    t.lexer.skip(1)


# JavaScript Code State
t_javascript_code_state_ignore = ' \t'
def t_javascript_code_state_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    return t

def t_javascript_code_state_JAVASCRIPT_END(t):
    r'\?/javascript\?'
    t.lexer.begin('INITIAL')
    return t

def t_javascript_code_state_FOREIGN_CODE_CONTENT(t):
    r'.|\n'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_javascript_code_state_error(t):
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}' no bloco JavaScript na linha {t.lexer.lineno}, coluna {t.lexer.lexpos - t.lexer.lineno_start_pos + 1}")
    t.lexer.skip(1)


# E assim por diante para CSHARP, WASM, CPP, JAVA, SQL, R...
# Para cada `LANG_START`, defina um `state` específico (ex: `csharp_code_state`)
# e dentro desse estado, as regras `t_[lang]_code_state_newline`, `t_[lang]_code_state_LANG_END`
# e `t_[lang]_code_state_FOREIGN_CODE_CONTENT = r'.|\n'`
# e `t_[lang]_code_state_error`.

# --- 5. FUNÇÕES DE TOKENIZAÇÃO E DEMO ---

# Mapeia valores de atributos para Tipos de Tokens (usado em t_sobrescrita_NIVEL_ATTR etc.)
# É importante que estes mapas estejam visíveis para t_sobrescrita_*
# Esta é uma forma de fazer o `lex.lexer.nivel_map` funcionar.
def build_lexer_with_maps():
    # Isso é um hack comum em PLY quando você precisa passar dados para as t_funcs.
    # Alternativamente, as t_funcs poderiam ser closures dentro de uma classe Lexer.
    # Mas para o setup de PLY, variáveis globais ou atributos de lexer são mais comuns.
    
    # Criar um objeto para armazenar os mapas que serão acessíveis via `t.lexer`
    class LexerMaps:
        def __init__(self):
            self.nivel_map = {
                'literal': TokenType.NIVEL_LITERAL,
                'alegorico': TokenType.NIVEL_ALEGORICO,
                'moral': TokenType.NIVEL_MORAL,
                'mistico': TokenType.NIVEL_MISTICO,
                'funcional': TokenType.NIVEL_FUNCIONAL,
                'estetico': TokenType.NIVEL_ESTETICO,
                'ontologico': TokenType.NIVEL_ONTOLOGICO,
                'holistico': TokenType.NIVEL_HOLISTICO,
                'matematico': TokenType.NIVEL_MATEMATICO,
                'simbolico': TokenType.NIVEL_SIMBOLICO,
                'parabolico': TokenType.NIVEL_PARABOLICO,
                'historico': TokenType.NIVEL_HISTORICO,
                'linguistico': TokenType.NIVEL_LINGUISTICO,
            }
            self.clave_map = {
                'arte': TokenType.CLAVE_ARTE,
                'ciencia': TokenType.CLAVE_CIENCIA,
                'filosofia': TokenType.CLAVE_FILOSOFIA,
                'tradicao': TokenType.CLAVE_TRADICAO,
                'geral': TokenType.CLAVE_GERAL
            }
            self.ont_map = {
                'substancia': TokenType.ONT_SUBSTANCIA,
                'quantidade': TokenType.ONT_QUANTIDADE,
                'qualidade': TokenType.ONT_QUALIDADE,
                'relacao': TokenType.ONT_RELACAO,
                'lugar': TokenType.ONT_LUGAR,
                'tempo': TokenType.ONT_TEMPO,
                'situacao': TokenType.ONT_SITUACAO,
                'condicao': TokenType.ONT_CONDICAO,
                'acao': TokenType.ONT_ACAO,
                'paixao': TokenType.ONT_PAIXAO
            }
    
    # Constrói o lexer
    # debug=True para ver o processo do lexer
    my_lexer = lex.lex(debug=False)
    my_lexer.nivel_map = LexerMaps().nivel_map
    my_lexer.clave_map = LexerMaps().clave_map
    my_lexer.ont_map = LexerMaps().ont_map
    return my_lexer

# Constrói o lexer uma vez
lexer = build_lexer_with_maps()

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
    serie { // Bloco de execução em série GuruDev
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

VOC.minhaFuncao(); // Chamada de função GuruDev®
ACU.variavel = 123; // Atribuição GuruDev®
Float altura = 1.75f; // Declaração de tipo Float
String nome = "Guilherme"; // Declaração de tipo String
// Este é um comentário de linha única GuruDev
/* Este é um comentário
   de múltiplas linhas GuruDev */
if (x == 10) { return true; } // Controle de fluxo GuruDev®
"Outra string com \"aspas\" dentro" // String literal
"""

    tokens = tokenize_gurudev_code(code_example)
    print("=== TOKENS GERADOS ===")
    for tok in tokens:
        # Excluir WHITESPACE para uma saída mais limpa
        if tok.type != 't_ignore': # PLY por padrão usa 't_ignore' para tipos ignorados
            print(tok)

    print(f"\nTotal de tokens (incluindo ignorados): {len(tokens)}")

    # Contagem de tokens (mais útil para estatísticas)
    token_counts = {}
    for tok in tokens:
        token_counts[tok.type] = token_counts.get(tok.type, 0) + 1
    
    print("\n=== ESTATÍSTICAS ===")
    for token_type, count in sorted(token_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"{token_type:25}: {count}")
