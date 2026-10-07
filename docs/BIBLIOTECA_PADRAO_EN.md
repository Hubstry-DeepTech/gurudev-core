# GuruDev® Standard Library

> 🌐 **Language / Idioma**: [Português](BIBLIOTECA_PADRAO.md) | **English** | [Bilingual Index](../BILINGUAL_INDEX.md)

Official documentation of native objects, methods, and functions of the GuruDev® language.  
**These names are reserved: they cannot be used as identifiers for variables, user functions, classes, etc.**

## Implementation status (current runtime)

> Verified on 2026-10-07 against the interpreter in this repository. The rest of this document describes the planned API; this section records what runs today. Contracts marked as working are verified by `tests/test_contratos_biblioteca.py`.

| Documented | Status today | Use today |
|---|---|---|
| `VOC.escrever(text)` | Works, with a difference: adds a line break at the end | — |
| `VOC.imprimir(text)` | Works | — |
| `VOC.ler()` | Not implemented | `ler_entrada()` |
| `NOM.versao()`, `NOM.autor()` | Not implemented | No equivalent |
| `Math.abs(n)` | Not implemented | `absoluto(n)` |
| `Math.sqrt(n)` | Not implemented | `raiz(n)` |
| `Math.ceil(n)`, `Math.floor(n)` | Not implemented | No equivalent. `arredondar(n)` is not a substitute: it rounds instead of always rounding up or down |
| `Texto.tamanho(t)` | Not implemented | `tamanho(t)` |
| `Texto.maiusculo(t)`, `Texto.minusculo(t)` | Not implemented | `t.maiusculo()`, `t.minusculo()` (method of the string itself) |

## Global Objects

| Name    | Description                            | Available Methods             |
|---------|----------------------------------------|------------------------------|
| VOC     | Console access (output and input)      | escrever, imprimir, ler      |
| NOM     | Program properties                     | versao, autor                |
| Math    | Mathematical functions                 | abs, ceil, floor, sqrt       |
| Texto   | Text manipulation utilities            | tamanho, maiusculo, minusculo|

## Methods

### VOC

- `VOC.escrever(texto: String): void`  
  Writes text to standard output (without newline).
  ```gurudev
  VOC.escrever("Hello, GuruDev!");
  ```

- `VOC.imprimir(texto: String): void`  
  Writes text to standard output with newline.
  ```gurudev
  VOC.imprimir("Hello, GuruDev!");
  ```

- `VOC.ler(): String`  
  Reads a line from standard input.
  ```gurudev
  String nome = VOC.ler();
  ```

### NOM

- `NOM.versao(): String`  
  Returns the interpreter version.

- `NOM.autor(): String`  
  Returns the program author.

### Math

- `Math.abs(numero: Int): Int`  
  Returns the absolute value of a number.

- `Math.ceil(numero: Float): Int`  
  Returns the ceiling of a floating-point number.

- `Math.sqrt(numero: Float): Float`  
  Returns the square root of a number.

### Texto

- `Texto.tamanho(texto: String): Int`  
  Returns the length of a string.

- `Texto.maiusculo(texto: String): String`  
  Converts text to uppercase.

- `Texto.minusculo(texto: String): String`  
  Converts text to lowercase.

---

**All these names are reserved and cannot be overridden.**