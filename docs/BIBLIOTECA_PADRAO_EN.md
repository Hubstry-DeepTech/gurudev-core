# GuruDev® Standard Library

> 🌐 **Language / Idioma**: [Português](BIBLIOTECA_PADRAO.md) | **English** | [Bilingual Index](../BILINGUAL_INDEX.md)

Official documentation of native objects, methods, and functions of the GuruDev® language.  
**These names are reserved: they cannot be used as identifiers for variables, user functions, classes, etc.**

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