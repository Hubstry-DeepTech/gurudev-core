
# Gramática EBNF da GuruDev® (Versão 1.0.0-alpha)

Esta EBNF descreve a sintaxe da Linguagem de Programação Multi-Paradigma GuruDev®, baseada em casos gramaticais do proto-indo-europeu e sua estrutura de blocos tríplices. 

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

Um programa GuruDev® é composto por um ou mais blocos tríplices. 

```ebnf
program = { triple_block } ;
```

### 2\. Sintaxe com Casos Gramaticais

Os 8 casos gramaticais servem como palavras-chave sintáticas principais. 

```ebnf
case_keyword = ( "VOC" (* Vocativo - Chamada/Invocação *)
               | "NOM" (* Nominativo - Declaração/Definição *)
               | "ACU" (* Acusativo - Objeto Direto/Atribuição *)
               | "DAT" (* Dativo - Destinatário/Para quem *)
               | "GEN" (* Genitivo - Posse/Pertencimento *)
               | "INS" (* Instrumental - Meio/Ferramenta *)
               | "LOC" (* Locativo - Local/Contexto *)
               | "ABL" (* Ablativo - Origem/Fonte *)
               ) ;

case_usage = case_keyword "." IDENTIFIER ; (* Ex: VOC.minhaFuncao(), NOM funcao, ACU.variavel *)
```

### 3\. Estrutura de Blocos Tríplices

Cada bloco GuruDev® possui três camadas: `[bloco]`, `[sobrescrita]` (para metadados) e `[subescritas]` (para interoperabilidade). 

```ebnf
triple_block = "[bloco]" WHITESPACE
               overscript_block WHITESPACE
               code_block WHITESPACE
               subscript_block
               "[/bloco]" ;

overscript_block = "[sobrescrita]" WHITESPACE
                   { overscript_line }
                   "[/sobrescrita]" ;

overscript_line = '"Contexto:" STRING_VALUE EOL
                | '"Campo do conhecimento:" SEMANTIC_KEYWORD_STRING EOL (* ex: "ciencias exatas" *)
                | '"Nível de interpretação:" INTERPRETATION_LEVEL_STRING EOL (* ex: "matematico" *)
                | '"Raiz semântica:" ROOT_KEYWORD EOL ;

code_block = "¡codigo!" WHITESPACE
             { statement }
             "!/codigo!" ;

subscript_block = "[subescritas]" WHITESPACE
                  { foreign_language_block }
                  "[/subescritas]" ;
```

### 4\. Claves Contextuais, Raízes Semânticas e Níveis de Interpretação

Estas anotações de metadados são parte da `overscript_block`. 

```ebnf
annotation_tag = "[" SEMANTIC_KEYWORD_SHORT "]"  (* ex: [ciencia], [filosofia] *)
                 [ "[" INTERPRETATION_LEVEL_SHORT "]" ] (* ex: [literal], [matematico] *)
                 [ "[" "raiz=\"" ROOT_KEYWORD_STRING "\""]" ] ; (* ex: [raiz="CALC"] *)

SEMANTIC_KEYWORD_SHORT = ( "filosofia" | "espiritual" | "ciencia" | "arte" | "geral" ) ;
INTERPRETATION_LEVEL_SHORT = ( "literal" | "parabolico" | "historico" | "linguistico" | "matematico" | "simbolico" | "holistico" ) ;
ROOT_KEYWORD_STRING = IDENTIFIER_STRING ; (* ex: "CALC", "LING", "MEDIA" *)

(* Estas tags também podem aparecer como atributos em 'overscript_line' *)
SEMANTIC_KEYWORD_STRING = "arte" | "ciencias exatas" | "ciencia da computacao" | "geral" | "contemplativo" | "transcendental" ; (* Exemplo de strings, podem ser mais genéricas *)
INTERPRETATION_LEVEL_STRING = "literal" | "metaforico" | "historico" | "processamento de linguagem" | "matematico" | "simbolico" | "sistemica" | "estrutural" ; (* Exemplo de strings *)
```

### 5\. Tipos de Dados Nativos

GuruDev® suporta uma variedade de tipos de dados explícitos. 

```ebnf
TYPE = ( "Int" | "Float" | "Bool" | "Char" | "String"
       | "Array<" TYPE ">"
       | "Object<" TYPE ">"
       | "Formula" | "Temporal" | "Imagem" | "Audio" | "Video"
       | "Tabela<" TYPE ">"
       | "Grafo<" TYPE "," TYPE ">"
       | IDENTIFIER (* Para classes personalizadas *)
       ) ;
```

### 6\. Interoperabilidade (Subescritas Multilíngues)

Blocos de código em outras linguagens são aninhados nas `[subescritas]`. 

```ebnf
foreign_language_block = "?" LANGUAGE_ID "?" WHITESPACE
                         { FOREIGN_CODE_LINE }
                         "?/" LANGUAGE_ID "?" ;

LANGUAGE_ID = ( "python" | "javascript" | "r" | "sql" | IDENTIFIER ) ; (* Permite outras línguas *)
FOREIGN_CODE_LINE = { CHARACTER } EOL ; (* Linhas de código na linguagem estrangeira *)
```

### 7\. Execução Série/Paralelo

Controle de fluxo explícito para execução sequencial ou simultânea. 

```ebnf
execution_control_block = ( "serie" "{" { statement } "}"
                          | "paralelo" "{" { statement } "}"
                          ) ;
```

### 8\. Regras de Sintaxe Básicas

```ebnf
statement = ( declaration
            | assignment
            | function_call
            | method_call
            | control_flow_statement
            | execution_control_block
            | return_statement
            ) ";" ; (* Ponto-e-vírgula obrigatório no final de cada linha  *)

declaration = case_usage TYPE IDENTIFIER [ "=" expression ] ; (* Adapta NOM caso *)
assignment = case_usage "=" expression ; (* Adapta ACU caso *)

function_call = case_usage "(" [ argument_list ] ")" ; (* Adapta VOC caso *)
method_call = case_usage "." IDENTIFIER"(" [ argument_list ] ")" ; (* Adapta VOC ou GEN caso *)

argument_list = expression { "," expression } ;

expression = ( value
             | function_call
             | method_call
             | binary_operation
             | unary_operation
             | multimodal_literal
             ) ;

value = ( NUMBER | STRING_VALUE | BOOLEAN | IDENTIFIER ) ;

STRING_VALUE = '"' { CHARACTER_EXCEPT_DOUBLE_QUOTE } '"' ; [cite_start](* Strings entre aspas duplas  *)
NUMBER = DIGIT+ [ "." DIGIT+ ] [ "f" ] ; [cite_start](* Float pode ter 'f' no final [cite: 147] *)
BOOLEAN = ( "true" | "false" ) ;
IDENTIFIER = LETTER { LETTER | DIGIT | "_" } ; [cite_start](* camelCase para variáveis, PascalCase para classes  - convenção, não regra EBNF *)

control_flow_statement = ( if_statement | for_loop | foreach_loop ) ;

if_statement = "if" "(" expression ")" "{" { statement } "}" [ "else" "{" { statement } "}" ] ;
for_loop = "for" "(" TYPE IDENTIFIER "=" expression ";" expression ";" assignment ")" "{" { statement } "}" ; (* Exemplo de for tradicional *)
foreach_loop = "for" "(" TYPE IDENTIFIER ":" IDENTIFIER ")" "{" { statement } "}" ; (* Exemplo de for-each *)
return_statement = "return" [ expression ] ;

class_declaration = "NOM" "classe" IDENTIFIER [ "extends" IDENTIFIER ] "{" { class_member } "}" ;
class_member = ( attribute_declaration | method_declaration ) ;

attribute_declaration = case_usage [ "=" expression ] ; (* Adapta GEN caso para propriedades, assumindo type implícito ou inferido *)
method_declaration = "NOM" "funcao" IDENTIFIER "(" [ parameter_list ] ")" [ ":" TYPE ] "{" { statement } "}" ;
parameter_list = parameter { "," parameter } ;
parameter = TYPE IDENTIFIER ; [cite_start](* Tipo explícito [cite: 287] *)

multimodal_literal = ( "carregar(\"" FILEPATH "\")" ) ; [cite_start](* Para Imagem, Audio, Video, Tabela [cite: 156, 157, 158, 159] *)
FILEPATH = { CHARACTER_EXCEPT_DOUBLE_QUOTE } ; (* Caminho para o arquivo *)
[cite_start](* Formula é STRING_VALUE, mas com contexto semântico [cite: 154] *)
[cite_start](* Temporal é STRING_VALUE com formato específico [cite: 155] *)
[cite_start](* Grafo é Object com sintaxe específica new Grafo<K,V>() [cite: 160] *)

(* Comentários [cite: 286] *)
comment = ( "//" { CHARACTER } EOL
          | "/*" { CHARACTER } "*/"
          ) ;

WHITESPACE = ( " " | "\t" | "\n" | "\r" )+ ;
EOL = "\n" | "\r\n" ;
CHARACTER = ANY_UNICODE_CHARACTER ;
CHARACTER_EXCEPT_DOUBLE_QUOTE = ANY_UNICODE_CHARACTER_EXCEPT_DOUBLE_QUOTE ;
```

-----

