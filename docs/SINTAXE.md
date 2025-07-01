# Sintaxe GuruDev® — Exemplos e regras

## Comandos de saída

```gurudev
VOC.escrever("Olá, mundo!");    // Válido
VOC.imprimir("Linha nova!");    // Válido
VOC.ler();                      // Válido
```

## Declarações de variável

```gurudev
String nome = "GuruDev";        // Válido
Int x = 42;                     // Válido
String VOC = "erro";            // Inválido: nome reservado
```

## Chamada de funções

```gurudev
Math.abs(-10);                  // Válido
Texto.tamanho("abc");           // Válido
Math.VOC();                     // Inválido: VOC não é método de Math
```

## Exemplos de código inválido

```gurudev
VOC = "teste";                  // Erro: VOC é reservado
func escrever() { ... }         // Erro: escrever é reservado
var Math = 123;                 // Erro: Math é reservado
```

## Regras de terminador

Sempre use ponto-e-vírgula ao final de cada instrução.
