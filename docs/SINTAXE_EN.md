# GuruDev® Syntax Examples and Rules

> 🌐 **Language / Idioma**: [Português](SINTAXE.md) | **English** | [Bilingual Index](../BILINGUAL_INDEX.md)

## Output Commands

```gurudev
VOC.escrever("Hello, world!");    // Valid
VOC.imprimir("New line!");        // Valid
VOC.ler();                        // Valid
```

## Variable Declarations

```gurudev
String nome = "GuruDev";        // Valid
Int x = 42;                     // Valid
String VOC = "error";           // Invalid: reserved name
```

## Function Calls

```gurudev
Math.abs(-10);                  // Valid
Texto.tamanho("abc");           // Valid
Math.VOC();                     // Invalid: VOC is not a method of Math
```

## Invalid Code Examples

```gurudev
VOC = "test";                   // Error: VOC is reserved
func escrever() { ... }         // Error: escrever is reserved
var Math = 123;                 // Error: Math is reserved
```

## Terminator Rules

Always use semicolon at the end of each instruction.