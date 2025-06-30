(* 
  GuruDev® EBNF Completa
  Versão: 1.0.0-alpha (Alinhada ao Lexer)
  Autor: Guilherme Gonçalves Machado
  Descrição: Gramática formal da linguagem GuruDev®, cobrindo todos os requisitos do whitepaper.
*)

(*
  --- Notas Importantes sobre o Lexer e Parser ---
  - WHITESPACE e NEWLINE são tokens produzidos pelo lexer, mas geralmente ignorados pelo parser entre os não-terminais, exceto onde sua presença é semanticamente relevante (ex: fim de linha para inferência de ponto-e-vírgula, não aplicável na GuruDev® com SEMICOLON explícito).
  - Comentários são ignorados pelo lexer e não chegam ao parser.
  - A ordem das regras é crucial no lexer (maior especificidade primeiro). No parser (usando ply.yacc, por exemplo), a gramática resolve ambiguidades com precedência e associatividade.
*)

program = { block } ;

block = BLOCO_START WHITESPACE overscript_block WHITESPACE gurudev_code_block WHITESPACE subscript_block WHITESPACE BLOCO_END ;

overscript_block = SOBRESCRITA_START WHITESPACE { overscript_attribute WHITESPACE } SOBRESCRITA_END ;
overscript_attribute = ( STRING_LITERAL (* Ex: "Contexto: descrição do propósito" *)
                       | NIVEL_ATTR
                       | RAIZ_ATTR
                       | CLAVE_ATTR
                       | ONT_ATTR
                       ) ;

NIVEL_ATTR = LBRACKET "nivel=" STRING_LITERAL RBRACKET ;
RAIZ_ATTR  = LBRACKET "raiz=" STRING_LITERAL RBRACKET ;
CLAVE_ATTR = LBRACKET "clave=" STRING_LITERAL RBRACKET ;
ONT_ATTR   = LBRACKET "ont=" STRING_LITERAL RBRACKET ;

gurudev_code_block = CODIGO_START WHITESPACE { gurudev_statement WHITESPACE } CODIGO_END ;

gurudev_statement = ( declaration
                    | assignment
                    | control_flow
                    | function_call
                    | method_call
                    | execution_control_block
                    | return_statement
                    ) SEMICOLON ;

declaration = ( ( type_keyword IDENTIFIER ) | ( case_keyword DOT IDENTIFIER ) ) [ ASSIGN expression ] ;
assignment  = ( IDENTIFIER | ( case_keyword DOT IDENTIFIER ) ) ASSIGN expression ;

type_keyword = ( BOOL_TYPE | STRING_TYPE | INT_TYPE | FLOAT_TYPE | VOID_TYPE
               | ARRAY_TYPE LBRACKET RBRACKET
               | OBJECT_TYPE LESS_THAN IDENTIFIER GREATER_THAN
               | FORMULA_TYPE | TEMPORAL_TYPE | IMAGEM_TYPE | AUDIO_TYPE | VIDEO_TYPE
               | TABELA_TYPE LESS_THAN IDENTIFIER GREATER_THAN
               | GRAFO_TYPE LESS_THAN IDENTIFIER COMMA IDENTIFIER GREATER_THAN
               | IDENTIFIER ) ; (* IDENTIFIER para classes customizadas *)

case_keyword = ( VOC | NOM | ACU | DAT | GEN | INS | LOC | ABL ) ;

function_call = ( IDENTIFIER | ( case_keyword DOT IDENTIFIER ) ) LPAREN [ argument_list ] RPAREN ;
method_call   = IDENTIFIER DOT ( IDENTIFIER | ( case_keyword DOT IDENTIFIER ) ) LPAREN [ argument_list ] RPAREN ;
argument_list = expression { COMMA expression } ;

expression = ( literal
             | IDENTIFIER
             | function_call
             | method_call
             | binary_operation
             | unary_operation
             | LPAREN expression RPAREN
             ) ;

literal = ( STRING_LITERAL | INT_LITERAL | FLOAT_LITERAL | BOOLEAN_LITERAL ) ;

binary_operation = expression ( PLUS | MINUS | MULTIPLY | DIVIDE | MODULO
                              | EQUALS | NOT_EQUALS | LESS_THAN | GREATER_THAN
                              | LESS_EQUAL | GREATER_EQUAL | AND | OR ) expression ;
unary_operation = ( PLUS | MINUS | NOT ) expression ;

control_flow = ( IF_KEYWORD LPAREN expression RPAREN LBRACE { gurudev_statement WHITESPACE } RBRACE [ ELSE_KEYWORD LBRACE { gurudev_statement WHITESPACE } RBRACE ]
               | FOR_KEYWORD LPAREN ( declaration | assignment ) SEMICOLON expression SEMICOLON assignment RPAREN LBRACE { gurudev_statement WHITESPACE } RBRACE
               | FOR_KEYWORD LPAREN type_keyword IDENTIFIER COLON IDENTIFIER RPAREN LBRACE { gurudev_statement WHITESPACE } RBRACE
               | WHILE_KEYWORD LPAREN expression RPAREN LBRACE { gurudev_statement WHITESPACE } RBRACE
               ) ;

return_statement = RETURN_KEYWORD [ expression ] ;

execution_control_block = ( SERIE_KEYWORD LBRACE { gurudev_statement WHITESPACE } RBRACE
                          | PARALELO_KEYWORD LBRACE { gurudev_statement WHITESPACE } RBRACE
                          | EM_KEYWORD ( IDENTIFIER | case_keyword DOT IDENTIFIER ) LBRACE { gurudev_statement WHITESPACE } RBRACE
                          ) ;

subscript_block = SUBESCRITAS_START WHITESPACE { foreign_language_block WHITESPACE } SUBESCRITAS_END ;
foreign_language_block = ( PYTHON_START FOREIGN_CODE_CONTENT PYTHON_END
                         | RUST_START FOREIGN_CODE_CONTENT RUST_END
                         | JAVASCRIPT_START FOREIGN_CODE_CONTENT JAVASCRIPT_END
                         | CSHARP_START FOREIGN_CODE_CONTENT CSHARP_END
                         | WASM_START FOREIGN_CODE_CONTENT WASM_END
                         | CPP_START FOREIGN_CODE_CONTENT CPP_END
                         | JAVA_START FOREIGN_CODE_CONTENT JAVA_END
                         | SQL_START FOREIGN_CODE_CONTENT SQL_END
                         | R_START FOREIGN_CODE_CONTENT R_END
                         ) ;

(*
FOREIGN_CODE_CONTENT: Este token é reconhecido pelo lexer como todo o conteúdo entre as tags de início e fim da linguagem estrangeira (inclusive quebras de linha e comentários internos), até o token de fechamento da linguagem correspondente. Este conteúdo é tratado como texto bruto e não é tokenizado pelo lexer da GuruDev®.
*)

(* --- TERMINAIS (TOKENS RECONHECIDOS PELO LEXER) --- *)

(* Estruturas de Blocos Principais *)
BLOCO_START = "[bloco]" ;
BLOCO_END = "[/bloco]" ;
SOBRESCRITA_START = "[sobrescrita]" ;
SOBRESCRITA_END = "[/sobrescrita]" ;
SUBESCRITAS_START = "[subescritas]" ;
SUBESCRITAS_END = "[/subescritas]" ;
CODIGO_START = "¡codigo!" ;
CODIGO_END = "!/codigo!" ;

(* Subescritas de Linguagens Estrangeiras (Tags de Início/Fim) *)
PYTHON_START = "¿python?" ;
PYTHON_END = "?/python?" ;
RUST_START = "¿rust?" ;
RUST_END = "?/rust?" ;
JAVASCRIPT_START = "¿javascript?" ;
JAVASCRIPT_END = "?/javascript?" ;
CSHARP_START = "¿csharp?" ;
CSHARP_END = "?/csharp?" ;
WASM_START = "¿wasm?" ;
WASM_END = "?/wasm?" ;
CPP_START = "¿c++?" ;
CPP_END = "?/c++?" ;
JAVA_START = "¿java?" ;
JAVA_END = "?/java?" ;
SQL_START = "¿sql?" ;
SQL_END = "?/sql?" ;
R_START = "¿r?" ;
R_END = "?/r?" ;

(* Atributos (os valores internos são STRING_LITERAL capturados pelo lexer) *)
NIVEL_ATTR = "[nivel=" STRING_LITERAL "]" ;
RAIZ_ATTR = "[raiz=" STRING_LITERAL "]" ;
CLAVE_ATTR = "[clave=" STRING_LITERAL "]" ;
ONT_ATTR = "[ont=" STRING_LITERAL "]" ;

(* Literais *)
STRING_LITERAL = '"' ( ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE | '\\' ANY_CHARACTER )* '"' ;
INT_LITERAL = DIGIT+ ;
FLOAT_LITERAL = DIGIT+ "." DIGIT+ [ "f" ] ;
BOOLEAN_LITERAL = "true" | "false" | "verdadeiro" | "falso" ;

(* Palavras-Chave (Tokens com valores literais exatos ou aliases) *)
VOC = "VOC" ; NOM = "NOM" ; ACU = "ACU" ; DAT = "DAT" ;
GEN = "GEN" ; INS = "INS" ; LOC = "LOC" ; ABL = "ABL" ;
FUNCAO = "funcao" ; CLASSE = "classe" ; EXTENDS = "extends" ; IMPLEMENTS = "implements" ;
BOOL_TYPE = "Bool" ; STRING_TYPE = "String" ; INT_TYPE = "Int" ; FLOAT_TYPE = "Float" ;
VOID_TYPE = "Void" ; ARRAY_TYPE = "Array" ; OBJECT_TYPE = "Object" ; FORMULA_TYPE = "Formula" ;
TEMPORAL_TYPE = "Temporal" ; IMAGEM_TYPE = "Imagem" ; AUDIO_TYPE = "Audio" ;
VIDEO_TYPE = "Video" ; TABELA_TYPE = "Tabela" ; GRAFO_TYPE = "Grafo" ;
IF_KEYWORD = "if" | "se" ; ELSE_KEYWORD = "else" | "senao" ;
FOR_KEYWORD = "for" | "para" ; WHILE_KEYWORD = "while" | "enquanto" ;
RETURN_KEYWORD = "return" | "retorna" ; BREAK_KEYWORD = "break" | "quebra" ;
CONTINUE_KEYWORD = "continue" | "continua" ;
SERIE_KEYWORD = "serie" ; PARALELO_KEYWORD = "paralelo" ; EM_KEYWORD = "em" ;
PUBLICO = "publico" ; PRIVADO = "privado" ; PROTEGIDO = "protegido" ;

(* Operadores *)
ASSIGN = "=" ; EQUALS = "==" ; NOT_EQUALS = "!=" ;
LESS_THAN = "<" ; GREATER_THAN = ">" ; LESS_EQUAL = "<=" ; GREATER_EQUAL = ">=" ;
PLUS = "+" ; MINUS = "-" ; MULTIPLY = "*" ; DIVIDE = "/" ; MODULO = "%" ;
AND = "&&" ; OR = "||" ; NOT = "!" ; ARROW = "->" ;

(* Delimitadores *)
LPAREN = "(" ; RPAREN = ")" ; LBRACE = "{" ; RBRACE = "}" ;
LBRACKET = "[" ; RBRACKET = "]" ; SEMICOLON = ";" ; COMMA = "," ;
DOT = "." ; COLON = ":" ;

(* Identificador (nomes de variáveis, funções, classes, etc. que não são palavras-chave) *)
ID = LETTER (LETTER | DIGIT | "_")* ;

(* Caracteres Ignorados pelo Lexer (não chegam ao Parser) *)
WHITESPACE = ( ' ' | '\t' )+ ;
NEWLINE = ( '\n' | '\r\n' )+ ;
COMMENT = ( "//" (ANY_CHARACTER_EXCEPT_NEWLINE)* ) | ( "/*" (ANY_CHARACTER)* "*/" ) ;

(* Componentes Básicos de Caracteres (usados nas definições acima) *)
LETTER = 'a'...'z' | 'A'...'Z' | 'À'...'ÿ' ; (* Inclui caracteres acentuados *)
DIGIT = '0'...'9' ;
ANY_CHARACTER = (* Qualquer caractere Unicode. Em EBNF, é um marcador conceitual. *) ;
ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE = (* Qualquer caractere Unicode exceto aspas duplas. *) ;
ANY_CHARACTER_EXCEPT_NEWLINE = (* Qualquer caractere Unicode exceto quebra de linha. *) ;

(* --- FIM DA GRAMÁTICA --- *)

(* --- Exemplo de Bloco GuruDev® Completo --- *)

[bloco]
    [sobrescrita]
        "Contexto: autenticação"
        [nivel="holistico"]
        [raiz="SEG"]
        [ont="acao"]
    [/sobrescrita]

    ¡codigo!
        NOM funcao verificarSenha(String senhaInserida, String senhaHashArmazenada) {
            return hash(senhaInserida) == hash(senhaHashArmazenada);
        }
    !/codigo!

    [subescritas]
        ¿python?
        def verificar_senha(senha_inserida, senha_armazenada):
            return hash(senha_inserida) == hash(senha_armazenada)
        ?/python?
    [/subescritas]
[/bloco]
