# GuruDev® EBNF — Version 1.0.0-alpha — Aligned with Lexer

> 🌐 **Language / Idioma**: [Português](GRAMMAR_V1_0_0_ALPHA.md) | **English** | [Bilingual Index](../BILINGUAL_INDEX.md)

> **Author:** *Guilherme Gonçalves Machado*  
> **Description:** Formal grammar of the GuruDev® language, covering all whitepaper requirements.  
> **Status:** *Alpha 1.0.0-alpha (Aligned with Lexer)*

---

## ⚠️ Important Notes about Lexer and Parser

(*  
--- Implicit Behavior for Direct Discourse Mode (Top-level Instructions) ---  
When GuruDev® instructions are written at the top of the file ("direct discourse mode", outside an explicit block), the compiler/interpreter will:
- Encapsulate these instructions, implicitly, in a `[bloco]...[/bloco]` (block).
- Generate a default `[sobrescrita]...[/sobrescrita]` (overscript) section, with inferred metadata (Context: "Direct Discourse Script", Field: "General", Level: "literal", Root: "CORE", Ontology: "action").
- Insert these instructions within an implicit `principal()` (main) function, serving as the program's entry point.

This allows concise scripts without losing internal semantic structure.

In GuruDev®, we use "code sentence" for what in other languages would be called "statement".  
We use "value production" for what would be "expression".  
This reinforces the linguistic analogy of the language.
*)

---

## 🎯 Main Structure

### 1. Program

```ebnf
program = ( block | oracao_de_codigo )+ ; (* A program is composed of one or more blocks or code sentences in direct discourse mode *)
```

### 1.1. Code Sentence

```ebnf
oracao_de_codigo = declaracao_variavel
                 | declaracao_funcao
                 | comando_controle
                 | comando_saida
                 | producao_de_valor ";"
                 | ... ;
```

### 1.2. Value Production

```ebnf
producao_de_valor = valor_literal
                  | chamada_funcao
                  | operacao
                  | ... ;
```

### 1.3. Instructions in Direct Discourse Mode

```ebnf
top_level_statement = oracao_de_codigo ; (* An instruction in direct discourse mode is any valid code sentence *)
```

---

## 📝 Example: Hello World in direct discourse mode

```gurudev
String mensagem = "Hello, World!";
VOC.print(mensagem);
```

<!-- The code above, internally, will be encapsulated as: -->
<!--
[bloco]
  [sobrescrita]
    "Context: Direct Discourse Script"
    [nivel="literal"]
    [clave="general"]
    [raiz="CORE"]
    [ont="action"]
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
<summary>Terminals and summarized definitions</summary>

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

## 2. GuruDev® Block

```ebnf
block = BLOCO_START WHITESPACE overscript_block WHITESPACE gurudev_code_block WHITESPACE subscript_block WHITESPACE BLOCO_END ;
```

---

## 3. Overscript Block

```ebnf
overscript_block = SOBRESCRITA_START WHITESPACE { overscript_attribute WHITESPACE } SOBRESCRITA_END ;
overscript_attribute = (
  STRING_LITERAL (* Ex: "Context: purpose description" *)
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

## 4. GuruDev® Code Block

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

### 4.1. Declaration and Assignment

```ebnf
declaration = ( ( type_keyword IDENTIFIER ) | ( case_keyword DOT IDENTIFIER ) ) [ ASSIGN producao_de_valor ] ;
assignment  = ( IDENTIFIER | ( case_keyword DOT IDENTIFIER ) ) ASSIGN producao_de_valor ;
```

### 4.2. Types and Grammatical Cases

```ebnf
type_keyword = (
  BOOL_TYPE | STRING_TYPE | INT_TYPE | FLOAT_TYPE | VOID_TYPE
  | ARRAY_TYPE LBRACKET RBRACKET
  | OBJECT_TYPE LESS_THAN IDENTIFIER GREATER_THAN
  | FORMULA_TYPE | TEMPORAL_TYPE | IMAGEM_TYPE | AUDIO_TYPE | VIDEO_TYPE
  | TABELA_TYPE LESS_THAN IDENTIFIER GREATER_THAN
  | GRAFO_TYPE LESS_THAN IDENTIFIER COMMA IDENTIFIER GREATER_THAN
  | IDENTIFIER
) ; (* IDENTIFIER for custom classes *)

case_keyword = ( VOC | NOM | ACU | DAT | GEN | INS | LOC | ABL ) ;
```

### 4.3. Functions, Methods and Value Productions

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

### 4.4. Control Flow

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

### 4.5. Execution Blocks

```ebnf
execution_control_block = (
    SERIE_KEYWORD LBRACE { oracao_de_codigo WHITESPACE } RBRACE
  | PARALELO_KEYWORD LBRACE { oracao_de_codigo WHITESPACE } RBRACE
  | EM_KEYWORD ( IDENTIFIER | case_keyword DOT IDENTIFIER ) LBRACE { oracao_de_codigo WHITESPACE } RBRACE
) ;
```

---

## 5. Subscript Block (Interoperability)

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

> **Note:**  
> *FOREIGN_CODE_CONTENT* is recognized by the lexer as all content between the start and end tags of the foreign language (including line breaks and internal comments), until the corresponding language closing token. This content is treated as raw text and is not tokenized by the GuruDev® lexer.

---

## 🏷️ Terminals (Tokens Recognized by Lexer)

<details>
<summary><strong>Click to expand</strong></summary>

```ebnf
(* Main Block Structures *)
BLOCO_START = "[bloco]" ;
BLOCO_END = "[/bloco]" ;
SOBRESCRITA_START = "[sobrescrita]" ;
SOBRESCRITA_END = "[/sobrescrita]" ;
SUBESCRITAS_START = "[subescritas]" ;
SUBESCRITAS_END = "[/subescritas]" ;
CODIGO_START = "¡codigo!" ;
CODIGO_END = "!/codigo!" ;

(* Foreign Language Subscripts (Start/End Tags) *)
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

(* Attributes *)
NIVEL_ATTR = "[nivel=" STRING_LITERAL "]" ;
RAIZ_ATTR = "[raiz=" STRING_LITERAL "]" ;
CLAVE_ATTR = "[clave=" STRING_LITERAL "]" ;
ONT_ATTR = "[ont=" STRING_LITERAL "]" ;

(* Literals *)
STRING_LITERAL = '"' ( ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE | '\\' ANY_CHARACTER )* '"' ;
INT_LITERAL = DIGIT+ ;
FLOAT_LITERAL = DIGIT+ "." DIGIT+ [ "f" ] ;
BOOLEAN_LITERAL = "true" | "false" | "verdadeiro" | "falso" ;

(* Keywords *)
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

(* Operators *)
ASSIGN = "=" ; EQUALS = "==" ; NOT_EQUALS = "!=" ;
LESS_THAN = "<" ; GREATER_THAN = ">" ; LESS_EQUAL = "<=" ; GREATER_EQUAL = ">=" ;
PLUS = "+" ; MINUS = "-" ; MULTIPLY = "*" ; DIVIDE = "/" ; MODULO = "%" ;
AND = "&&" ; OR = "||" ; NOT = "!" ; ARROW = "->" ;

(* Delimiters *)
LPAREN = "(" ; RPAREN = ")" ; LBRACE = "{" ; RBRACE = "}" ;
LBRACKET = "[" ; RBRACKET = "]" ; SEMICOLON = ";" ; COMMA = "," ;
DOT = "." ; COLON = ":" ;

(* Identifier *)
ID = LETTER (LETTER | DIGIT | "_")* ;

(* Characters Ignored by Lexer *)
WHITESPACE = ( ' ' | '\t' )+ ;
NEWLINE = ( '\n' | '\r\n' )+ ;
COMMENT = ( "//" (ANY_CHARACTER_EXCEPT_NEWLINE)* ) | ( "/*" (ANY_CHARACTER)* "*/" ) ;

(* Basic Components *)
LETTER = 'a'...'z' | 'A'...'Z' | 'À'...'ÿ' ;
DIGIT = '0'...'9' ;
ANY_CHARACTER = (* Any Unicode character. *) ;
ANY_CHARACTER_EXCEPT_DOUBLE_QUOTE = (* Any Unicode character except double quotes. *) ;
ANY_CHARACTER_EXCEPT_NEWLINE = (* Any Unicode character except line break. *) ;
```
</details>

---

## 📦 Complete GuruDev® Block Example

```gurudev
[bloco]
  [sobrescrita]
    "Context: authentication"
    [nivel="holistic"]
    [raiz="SEG"]
    [ont="action"]
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

> **END OF GRAMMAR**