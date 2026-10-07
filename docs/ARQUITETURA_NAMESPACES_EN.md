# Namespace Architecture and Object Hierarchy

> 🌐 **Language / Idioma**: [Português](ARQUITETURA_NAMESPACES.md) | **English** | [Bilingual Index](../BILINGUAL_INDEX.md)

- **VOC**: Global object, direct access via VOC.
- **VOC.escrever** and **VOC.imprimir**: Direct methods of VOC.
- **Math**, **Texto**: Global objects for utility functions.
- **No sub-objects exist (e.g., VOC.Console)**.  
  Always use the direct form: `VOC.escrever()`.

## Implementation status (current runtime)

> Verified on 2026-10-07: `VOC.escrever()` and `VOC.imprimir()` work. The `Math` and `Texto` objects do not exist in the current interpreter yet; the `Math.abs(-5)` example below describes the planned API. Equivalents that work today: see "Implementation status" in [BIBLIOTECA_PADRAO_EN.md](BIBLIOTECA_PADRAO_EN.md).

## Example

```gurudev
VOC.escrever("Hi");           // OK
VOC.Console.escrever("Hi");   // Invalid!
Math.abs(-5);                 // OK
```