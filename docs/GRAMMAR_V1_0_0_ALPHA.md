
# Gramática EBNF da GuruDev® (Versão 1.0.0-alpha - Lexer-Aligned)

Esta EBNF descreve a sintaxe completa da Linguagem de Programação Ontológica e Multissemiótica GuruDev®, alinhada com o comportamento do lexer `ply.lex` implementado. Ela define como o código GuruDev® é estruturado, incluindo suas anotações semânticas e a interoperabilidade nativa com outras linguagens.

-----

### Convenções EBNF

  * `rule = definition ;`
  * `"terminal"`: Palavras-chave e símbolos literais, exatamente como aparecem no código.
  * `[ item ]`: Item opcional (zero ou uma ocorrência).
  * `{ item }`: Item repetível (zero ou mais ocorrências).
  * `item+`: Um ou mais itens.
  * `( item1 | item2 )`: Escolha entre itens.
  * `(* comment *)`: Comentários dentro da gramática.

-----

### 1\. Estrutura Geral do Programa

Um programa GuruDev® é composto por um ou mais blocos principais.

```ebnf
program = { block } ;
```

### 2\. Definição do Bloco Principal (`[bloco]`)

O bloco principal da GuruDev® engloba a estrutura tríplice de metadados, código GuruDev® e subescritas multilíngues.

```ebnf
block = BLOCO_START WHITESPACE overscript_block WHITESPACE gurudev_code_block WHITESPACE subscript_block BLOCO_END ;
```

### 3\. Bloco de Sobrescrita (`[sobrescrita]`)

Define os metadados contextuais, semânticos e hermenêuticos do bloco GuruDev®.

```ebnf
overscript_block = SOBRESCRITA_START WHITESPACE { overscript_attribute } SOBRESCRITA_END ;
overscript_attribute = ( STRING_LITERAL (* "Contexto: descrição do propósito" *)
                       | STRING_LITERAL (* "Campo do conhecimento: área específica" *)
                       | STRING_LITERAL (* "Nível de interpretação: tipo de processamento" *)
                       | NIVEL_ATTR
                       | RAIZ_ATTR
                       | CLAVE_ATTR
                       | ONT_ATTR
                       ) ;

NIVEL_ATTR = LBRACKET "nivel=" STRING_LITERAL RBRACKET ;
RAIZ_ATTR = LBRACKET "raiz=" STRING_LITERAL RBRACKET ;
CLAVE_ATTR = LBRACKET "clave=" STRING_LITERAL RBRACKET ;
ONT_ATTR = LBRACKET "ont=" STRING_LITERAL RBRACKET ; (* Alinhado com [ont="substancia"] *)

(* Note: Os valores internos STRING_LITERAL para Nivel, Raiz, Clave, Ont serão
   mapeados para seus respectivos TokenType específicos pelo lexer.
   Ex: STRING_LITERAL "literal" para NIVEL_LITERAL. *)
```

### 4\. Bloco de Código GuruDev® Principal (`¡codigo!`)

Contém a lógica funcional escrita na sintaxe GuruDev®.

```ebnf
gurudev_code_block = CODIGO_START WHITESPACE { gurudev_statement } CODIGO_END ;

gurudev_statement = ( declaration
                    | assignment
                    | control_flow
                    | function_call
                    | method_call
                    | execution_control_block
                    | return_statement
                    ) SEMICOLON ;

declaration = ( ( type_keyword IDENTIFIER ) | ( case_keyword DOT IDENTIFIER ) ) [ ASSIGN expression ] ; (* Ajusta NOM e tipos *)
assignment = ( ID | ( case_keyword DOT IDENTIFIER ) ) ASSIGN expression ; (* Ajusta ACU *)

type_keyword = ( BOOL_TYPE | STRING_TYPE | INT_TYPE | FLOAT_TYPE | VOID_TYPE
               | ARRAY_TYPE LBRACKET RBRACKET
               | OBJECT_TYPE LESS_THAN ID GREATER_THAN
               | FORMULA_TYPE | TEMPORAL_TYPE | IMAGEM_TYPE | AUDIO_TYPE | VIDEO_TYPE
               | TABELA_TYPE LESS_THAN ID GREATER_THAN
               | GRAFO_TYPE LESS_THAN ID COMMA ID GREATER_THAN
               | ID ) ; (* ID para classes customizadas *)

case_keyword = ( VOC | NOM | ACU | DAT | GEN | INS | LOC | ABL ) ;

function_call = ( ID | ( case_keyword DOT ID ) ) LPAREN [ argument_list ] RPAREN ;
method_call = ID DOT ( ID | ( case_keyword DOT ID ) ) LPAREN [ argument_list ] RPAREN ;
argument_list = expression { COMMA expression } ;

expression = ( literal
             | ID
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

control_flow = ( IF_KEYWORD LPAREN expression RPAREN LBRACE { gurudev_statement } RBRACE [ ELSE_KEYWORD LBRACE { gurudev_statement } RBRACE ]
               | FOR_KEYWORD LPAREN ( declaration | assignment ) SEMICOLON expression SEMICOLON assignment RPAREN LBRACE { gurudev_statement } RBRACE (* for (int i=0; i<n; i++) *)
               | FOR_KEYWORD LPAREN type_keyword ID COLON ID RPAREN LBRACE { gurudev_statement } RBRACE (* for (Float peso : pesos) *)
               | WHILE_KEYWORD LPAREN expression RPAREN LBRACE { gurudev_statement } RBRACE
               ) ;

return_statement = RETURN_KEYWORD [ expression ] ;

execution_control_block = ( SERIE_KEYWORD LBRACE { gurudev_statement } RBRACE
                          | PARALELO_KEYWORD LBRACE { gurudev_statement } RBRACE
                          | EM_KEYWORD ( ID | case_keyword DOT ID ) LBRACE { gurudev_statement } RBRACE (* em python { ... } *)
                          ) ;
```

### 5\. Bloco de Subescritas Multilíngues (`[subescritas]`)

Contém blocos de código em linguagens estrangeiras para interoperabilidade.

```ebnf
subscript_block = SUBESCRITAS_START WHITESPACE { foreign_language_block } SUBESCRITAS_END ;

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

FOREIGN_CODE_CONTENT = ANY_CHARACTER_SEQUENCE ; (* Conteúdo bruto da linguagem estrangeira, não tokenizado pelo lexer da GuruDev® *)
```

### 6\. Terminais (Tokens Reconhecidos pelo Lexer)

Esta seção lista os terminais (tokens) que o lexer produz, com as regras literais ou regex que os definem.

```ebnf
(* Estruturas Principais *)
BLOCO_START = "[bloco]" ;
BLOCO_END = "[/bloco]" ;
SOBRESCRITA_START = "[sobrescrita]" ;
SOBRESCRITA_END = "[/sobrescrita]" ;
SUBESCRITAS_START = "[subescritas]" ;
SUBESCRITAS_END = "[/subescritas]" ;
CODIGO_START = "¡codigo!" ;
CODIGO_END = "!/codigo!" ;

(* Subescritas de Linguagens *)
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

(* Conteúdo Bruto (para código estrangeiro) *)
FOREIGN_CODE_CONTENT = ANY_CHARACTER_SEQUENCE ; (* Captura qualquer sequência de caracteres, incluindo newlines *)

(* Atributos (os valores internos são capturados pelo lexer) *)
NIVEL_ATTR = "[nivel=" STRING_LITERAL "]" ;
RAIZ_ATTR = "[raiz=" STRING_LITERAL "]" ;
CLAVE_ATTR = "[clave=" STRING_LITERAL "]" ;
ONT_ATTR = "[ont=" STRING_LITERAL "]" ;

(* Literais *)
STRING_LITERAL = '"' ( ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE | '\\' ANY_CHARACTER )* '"' ; (* Corrigido para escape de aspas *)
INT_LITERAL = DIGIT+ ;
FLOAT_LITERAL = DIGIT+ "." DIGIT+ [ "f" ] ;
BOOLEAN_LITERAL = "true" | "false" | "verdadeiro" | "falso" ;

(* Palavras-Chave (Tokens com valores literais exatos) *)
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

(* Ignorados pelo Lexer *)
WHITESPACE = ( ' ' | '\t' )+ ;
NEWLINE = ( '\n' | '\r\n' )+ ; (* Reconhecido como token, se parser precisar *)
COMMENT = ( "//" (ANY_CHARACTER_EXCEPT_NEWLINE)* ) | ( "/*" (ANY_CHARACTER)* "*/" ) ;

(* Componentes básicos de caracteres (internos para regex) *)
LETTER = 'a'...'z' | 'A'...'Z' | 'À'...'ÿ' ; (* Inclui caracteres acentuados *)
DIGIT = '0'...'9' ;
ANY_CHARACTER = (* Qualquer caractere Unicode. Em EBNF, é um marcador conceitual. *) ;
ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE = (* Qualquer caractere Unicode exceto aspas duplas. *) ;
ANY_CHARACTER_EXCEPT_NEWLINE = (* Qualquer caractere Unicode exceto quebra de linha. *) ;

```

-----

