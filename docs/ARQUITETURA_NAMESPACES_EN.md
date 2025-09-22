# Namespace Architecture and Object Hierarchy

> 🌐 **Language / Idioma**: [Português](ARQUITETURA_NAMESPACES.md) | **English** | [Bilingual Index](../BILINGUAL_INDEX.md)

- **VOC**: Global object, direct access via VOC.
- **VOC.escrever** and **VOC.imprimir**: Direct methods of VOC.
- **Math**, **Texto**: Global objects for utility functions.
- **No sub-objects exist (e.g., VOC.Console)**.  
  Always use the direct form: `VOC.escrever()`.

## Example

```gurudev
VOC.escrever("Hi");           // OK
VOC.Console.escrever("Hi");   // Invalid!
Math.abs(-5);                 // OK
```