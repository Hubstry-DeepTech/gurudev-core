# Validation Tests — GuruDev®

> 🌐 **Language / Idioma**: [Português](EXEMPLOS_VALIDACAO.md) | **English** | [Bilingual Index](../BILINGUAL_INDEX.md)

## Valid

```gurudev
VOC.escrever("All good!");
String nome = VOC.ler();
Math.abs(-99);
Texto.maiusculo("abc");
```

## Invalid

```gurudev
var escrever = "trying";     // ERROR: reserved name
func VOC() { ... }           // ERROR: reserved name
VOC = 1;                     // ERROR: cannot override native object
Texto.escrever("hi");        // ERROR: method doesn't exist on this object
```