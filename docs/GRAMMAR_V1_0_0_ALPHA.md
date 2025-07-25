# GuruDev® EBNF — Versão 1.0.0-alpha — Alinhada ao Lexer

> **Autor:** *Guilherme Gonçalves Machado*  
> **Descrição:** Gramática formal da linguagem GuruDev®, cobrindo todos os requisitos do whitepaper.  
> **Status:** *Alpha 1.0.0-alpha (Alinhada ao Lexer)*

---

## ⚠️ Notas Importantes sobre o Lexer e Parser

(*  
--- Comportamento Implícito para Modo de Discurso Direto (Instruções no Topo) ---  
Quando instruções GuruDev® são escritas no topo do arquivo (“modo de discurso direto”, fora de um bloco explícito), o compilador/interpretador irá:
- Encapsular essas instruções, implicitamente, em um `[bloco]...[/bloco]`.
- Gerar uma seção `[sobrescrita]...[/sobrescrita]` padrão, com metadados inferidos (Contexto: "Script de Discurso Direto", Campo: "Geral", Nível: "literal", Raiz: "CORE", Ontologia: "acao").
- Inserir essas instruções dentro de uma função `principal()` implícita, servindo como ponto de entrada do programa.

Isso permite scripts concisos, sem perder a estrutura semântica interna.

Na GuruDev®, usamos "oração de código" para o que em outras linguagens seria chamado de "statement".  
Usamos "produção de valor" para o que seria "expression".  
Isso reforça a analogia linguística da linguagem.
*)

---

## 🎯 Estrutura Principal

### 1. Programa

```ebnf
program = ( block | oracao_de_codigo )+ ; (* Um programa é composto por um ou mais blocos ou orações de código em modo de discurso direto *)
```

### 1.1. Oração de Código

```ebnf
oracao_de_codigo = declaracao_variavel
                 | declaracao_funcao
                 | comando_controle
                 | comando_saida
                 | producao_de_valor ";"
                 | ... ;
```

### 1.2. Produção de Valor

```ebnf
producao_de_valor = valor_literal
                  | chamada_funcao
                  | operacao
                  | ... ;
```

### 1.3. Instruções em Modo de Discurso Direto

```ebnf
top_level_statement = oracao_de_codigo ; (* Uma instrução em modo de discurso direto é qualquer oração de código válida *)
```

---

## 📝 Exemplo: Hello World em modo de discurso direto

```gurudev
String mensagem = "Hello, World!";
VOC.print(mensagem);
```

<!-- O código acima, internamente, será encapsulado como: -->
<!--
[bloco]
  [sobrescrita]
    "Contexto: Script de Discurso Direto"
    [nivel="literal"]
    [clave="geral"]
    [raiz="CORE"]
    [ont="acao"]
  [/sobrescrita]
  ¡codigo!
    NOM funcao principal() {
      String mensagem = "Hello, World!";
      VOC.print(mensagem);
    }
  !/codigo!
[/bloco]
-->

---

## <details>
<summary>Terminais e definições resumidas</summary>

```ebnf
block = "[bloco]" sobrescrita? codigo "[/bloco]" ;

sobrescrita = "[sobrescrita]" metadados "[/sobrescrita]" ;

metadados = ... ;

codigo = "¡codigo!" { oracao_de_codigo } "!/codigo!" ;

oracao_de_codigo = declaracao_variavel
                 | declaracao_funcao
                 | comando_controle
                 | comando_saida
                 | producao_de_valor ";"
                 | ... ;

producao_de_valor = valor_literal
                  | chamada_funcao
                  | operacao
                  | ... ;

declaracao_variavel = tipo identificador "=" producao_de_valor ";" ;

tipo = "String" | "Float" | "Int" | ... ;

identificador = ... ;

valor_literal = ... ;

chamada_funcao = ... ;

comando_controle = ... ;

comando_saida = ... ;
```
</details>

---

## 2. Bloco GuruDev®

```ebnf
block = BLOCO_START WHITESPACE overscript_block WHITESPACE gurudev_code_block WHITESPACE subscript_block WHITESPACE BLOCO_END ;
```

---

## 3. Bloco de Sobrescrita

```ebnf
overscript_block = SOBRESCRITA_START WHITESPACE { overscript_attribute WHITESPACE } SOBRESCRITA_END ;
overscript_attribute = (
  STRING_LITERAL (* Ex: "Contexto: descrição do propósito" *)
  | NIVEL_ATTR
  | RAIZ_ATTR
  | CLAVE_ATTR
  | ONT_ATTR
) ;

NIVEL_ATTR = LBRACKET "nivel=" STRING_LITERAL RBRACKET ;
RAIZ_ATTR  = LBRACKET "raiz=" STRING_LITERAL RBRACKET ;
CLAVE_ATTR = LBRACKET "clave=" STRING_LITERAL RBRACKET ;
ONT_ATTR   = LBRACKET "ont=" STRING_LITERAL RBRACKET ;
```

---

## 4. Bloco de Código GuruDev®

```ebnf
gurudev_code_block = CODIGO_START WHITESPACE { oracao_de_codigo WHITESPACE } CODIGO_END ;

oracao_de_codigo = (
    declaration
  | assignment
  | control_flow
  | function_call
  | method_call
  | execution_control_block
  | return_statement
) SEMICOLON ;
```

---

### 4.1. Declaração e Atribuição

```ebnf
declaration = ( ( type_keyword IDENTIFIER ) | ( case_keyword DOT IDENTIFIER ) ) [ ASSIGN producao_de_valor ] ;
assignment  = ( IDENTIFIER | ( case_keyword DOT IDENTIFIER ) ) ASSIGN producao_de_valor ;
```

### 4.2. Tipos e Casos Gramaticais

```ebnf
type_keyword = (
  BOOL_TYPE | STRING_TYPE | INT_TYPE | FLOAT_TYPE | VOID_TYPE
  | ARRAY_TYPE LBRACKET RBRACKET
  | OBJECT_TYPE LESS_THAN IDENTIFIER GREATER_THAN
  | FORMULA_TYPE | TEMPORAL_TYPE | IMAGEM_TYPE | AUDIO_TYPE | VIDEO_TYPE
  | TABELA_TYPE LESS_THAN IDENTIFIER GREATER_THAN
  | GRAFO_TYPE LESS_THAN IDENTIFIER COMMA IDENTIFIER GREATER_THAN
  | IDENTIFIER
) ; (* IDENTIFIER para classes customizadas *)

case_keyword = ( VOC | NOM | ACU | DAT | GEN | INS | LOC | ABL ) ;
```

### 4.3. Funções, Métodos e Produções de Valor

```ebnf
function_call = ( IDENTIFIER | ( case_keyword DOT IDENTIFIER ) ) LPAREN [ argument_list ] RPAREN ;
method_call   = IDENTIFIER DOT ( IDENTIFIER | ( case_keyword DOT IDENTIFIER ) ) LPAREN [ argument_list ] RPAREN ;
argument_list = producao_de_valor { COMMA producao_de_valor } ;

producao_de_valor = (
    literal
  | IDENTIFIER
  | function_call
  | method_call
  | binary_operation
  | unary_operation
  | LPAREN producao_de_valor RPAREN
) ;

literal = ( STRING_LITERAL | INT_LITERAL | FLOAT_LITERAL | BOOLEAN_LITERAL ) ;

binary_operation = producao_de_valor ( PLUS | MINUS | MULTIPLY | DIVIDE | MODULO
    | EQUALS | NOT_EQUALS | LESS_THAN | GREATER_THAN
    | LESS_EQUAL | GREATER_EQUAL | AND | OR ) producao_de_valor ;
unary_operation = ( PLUS | MINUS | NOT ) producao_de_valor ;
```

---

### 4.4. Controle de Fluxo

```ebnf
control_flow = (
  IF_KEYWORD LPAREN producao_de_valor RPAREN LBRACE { oracao_de_codigo WHITESPACE } RBRACE [ ELSE_KEYWORD LBRACE { oracao_de_codigo WHITESPACE } RBRACE ]
  | FOR_KEYWORD LPAREN ( declaration | assignment ) SEMICOLON producao_de_valor SEMICOLON assignment RPAREN LBRACE { oracao_de_codigo WHITESPACE } RBRACE
  | FOR_KEYWORD LPAREN type_keyword IDENTIFIER COLON IDENTIFIER RPAREN LBRACE { oracao_de_codigo WHITESPACE } RBRACE
  | WHILE_KEYWORD LPAREN producao_de_valor RPAREN LBRACE { oracao_de_codigo WHITESPACE } RBRACE
) ;

return_statement = RETURN_KEYWORD [ producao_de_valor ] ;
```

---

### 4.5. Blocos de Execução

```ebnf
execution_control_block = (
    SERIE_KEYWORD LBRACE { oracao_de_codigo WHITESPACE } RBRACE
  | PARALELO_KEYWORD LBRACE { oracao_de_codigo WHITESPACE } RBRACE
  | EM_KEYWORD ( IDENTIFIER | case_keyword DOT IDENTIFIER ) LBRACE { oracao_de_codigo WHITESPACE } RBRACE
) ;
```

---

## 5. Bloco de Subescritas (Interoperabilidade)

```ebnf
subscript_block = SUBESCRITAS_START WHITESPACE { foreign_language_block WHITESPACE } SUBESCRITAS_END ;

foreign_language_block = (
  PYTHON_START FOREIGN_CODE_CONTENT PYTHON_END
  | RUST_START FOREIGN_CODE_CONTENT RUST_END
  | JAVASCRIPT_START FOREIGN_CODE_CONTENT JAVASCRIPT_END
  | CSHARP_START FOREIGN_CODE_CONTENT CSHARP_END
  | WASM_START FOREIGN_CODE_CONTENT WASM_END
  | CPP_START FOREIGN_CODE_CONTENT CPP_END
  | JAVA_START FOREIGN_CODE_CONTENT JAVA_END
  | SQL_START FOREIGN_CODE_CONTENT SQL_END
  | R_START FOREIGN_CODE_CONTENT R_END
) ;
```

> **Nota:**  
> *FOREIGN_CODE_CONTENT* é reconhecido pelo lexer como todo o conteúdo entre as tags de início e fim da linguagem estrangeira (inclusive quebras de linha e comentários internos), até o token de fechamento da linguagem correspondente. Este conteúdo é tratado como texto bruto e não é tokenizado pelo lexer da GuruDev®.

---

## 🏷️ Terminais (Tokens Reconhecidos pelo Lexer)

<details>
<summary><strong>Clique para expandir</strong></summary>

```ebnf
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

(* Atributos *)
NIVEL_ATTR = "[nivel=" STRING_LITERAL "]" ;
RAIZ_ATTR = "[raiz=" STRING_LITERAL "]" ;
CLAVE_ATTR = "[clave=" STRING_LITERAL "]" ;
ONT_ATTR = "[ont=" STRING_LITERAL "]" ;

(* Literais *)
STRING_LITERAL = '"' ( ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE | '\\' ANY_CHARACTER )* '"' ;
INT_LITERAL = DIGIT+ ;
FLOAT_LITERAL = DIGIT+ "." DIGIT+ [ "f" ] ;
BOOLEAN_LITERAL = "true" | "false" | "verdadeiro" | "falso" ;

(* Palavras-Chave *)
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

(* Identificador *)
ID = LETTER (LETTER | DIGIT | "_")* ;

(* Caracteres Ignorados pelo Lexer *)
WHITESPACE = ( ' ' | '\t' )+ ;
NEWLINE = ( '\n' | '\r\n' )+ ;
COMMENT = ( "//" (ANY_CHARACTER_EXCEPT_NEWLINE)* ) | ( "/*" (ANY_CHARACTER)* "*/" ) ;

(* Componentes Básicos *)
LETTER = 'a'...'z' | 'A'...'Z' | 'À'...'ÿ' ;
DIGIT = '0'...'9' ;
ANY_CHARACTER = (* Qualquer caractere Unicode. *) ;
ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE = (* Qualquer caractere Unicode exceto aspas duplas. *) ;
ANY_CHARACTER_EXCEPT_NEWLINE = (* Qualquer caractere Unicode exceto quebra de linha. *) ;
```
</details>

---

## 📦 Exemplo de Bloco GuruDev® Completo

```gurudev
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
```

---

> **FIM DA GRAMÁTICA**