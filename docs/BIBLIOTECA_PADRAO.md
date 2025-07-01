# Biblioteca Padrão GuruDev®

Documentação oficial dos objetos, métodos e funções nativas da linguagem GuruDev®.  
**Estes nomes são reservados: não podem ser usados como identificadores de variáveis, funções do usuário, classes, etc.**

## Objetos Globais

| Nome    | Descrição                              | Métodos Disponíveis           |
|---------|----------------------------------------|------------------------------|
| VOC     | Acesso ao console (saída e entrada)    | escrever, imprimir, ler      |
| NOM     | Propriedades do programa               | versao, autor                |
| Math    | Funções matemáticas                    | abs, ceil, floor, sqrt       |
| Texto   | Utilidades para manipulação de texto   | tamanho, maiusculo, minusculo|

## Métodos

### VOC

- `VOC.escrever(texto: String): void`  
  Escreve texto na saída padrão (sem nova linha).
  ```gurudev
  VOC.escrever("Olá, GuruDev!");
VOC.imprimir(texto: String): void
Escreve texto na saída padrão com nova linha.

gurudev
VOC.imprimir("Olá, GuruDev!");
VOC.ler(): String
Lê uma linha da entrada padrão.

gurudev
String nome = VOC.ler();
NOM
NOM.versao(): String
Retorna a versão do interpretador.

NOM.autor(): String
Retorna o autor do programa.

Math
Math.abs(numero: Int): Int
Math.ceil(numero: Float): Int
Math.sqrt(numero: Float): Float
Texto
Texto.tamanho(texto: String): Int
Texto.maiusculo(texto: String): String
Texto.minusculo(texto: String): String
Todos esses nomes são reservados e não podem ser sobrescritos. EOF

Crie docs/GRAMMAR_EXTRAS_VOC_EBNF.ebnf
cat <<'EOF' > docs/GRAMMAR_EXTRAS_VOC_EBNF.ebnf // Palavras-chave e nomes reservados RESERVED = "VOC" | "NOM" | "Math" | "Texto" | "escrever" | "imprimir" | "ler" | "tamanho" | "maiusculo" | "minusculo" | "abs" | "ceil" | "floor" | "sqrt" | "versao" | "autor" ;

// Identificador de usuário (não pode ser RESERVED) IDENTIFICADOR = LETTER (LETTER | DIGIT | "_")* ; IDENTIFICADOR_INVALIDO = IDENTIFICADOR onde IDENTIFICADOR ∈ RESERVED ; // Erro!

// Oração de código (nível superior) oracao_de_codigo = declaracao_variavel | chamada_funcao | comando_saida | ... ;

// Comando de saída de texto comando_saida = VOC "." ("escrever" | "imprimir") "(" argumento ")" ";" ;

// Chamada de função geral (exclui RESERVED) chamada_funcao = IDENTIFICADOR "(" argumento? ")" ";" ;

// Exemplo de declaração de variável (garante que não usa RESERVED) declaracao_variavel = tipo IDENTIFICADOR "=" expressao ";" ; EOF

Crie docs/SINTAXE.md
cat <<'EOF' > docs/SINTAXE.md

Sintaxe GuruDev® — Exemplos e regras
Comandos de saída
gurudev
VOC.escrever("Olá, mundo!");    // Válido
VOC.imprimir("Linha nova!");    // Válido
VOC.ler();                      // Válido
Declarações de variável
gurudev
String nome = "GuruDev";        // Válido
Int x = 42;                     // Válido
String VOC = "erro";            // Inválido: nome reservado
Chamada de funções
gurudev
Math.abs(-10);                  // Válido
Texto.tamanho("abc");           // Válido
Math.VOC();                     // Inválido: VOC não é método de Math
Exemplos de código inválido
gurudev
VOC = "teste";                  // Erro: VOC é reservado
func escrever() { ... }         // Erro: escrever é reservado
var Math = 123;                 // Erro: Math é reservado
Regras de terminador
Sempre use ponto-e-vírgula ao final de cada instrução. EOF

Crie docs/EXEMPLOS_VALIDACAO.md
cat <<'EOF' > docs/EXEMPLOS_VALIDACAO.md

Testes de Validação — GuruDev®
Válidos
gurudev
VOC.escrever("Tudo certo!");
String nome = VOC.ler();
Math.abs(-99);
Texto.maiusculo("abc");
Inválidos
gurudev
var escrever = "tentando";   // ERRO: nome reservado
func VOC() { ... }           // ERRO: nome reservado
VOC = 1;                     // ERRO: não pode sobrescrever objeto nativo
Texto.escrever("oi");        // ERRO: método não existe nesse objeto
