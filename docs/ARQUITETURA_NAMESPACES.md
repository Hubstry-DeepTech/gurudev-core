# Arquitetura de Namespaces e Hierarquia de Objetos

- **VOC**: Objeto global, acesso direto via VOC.
- **VOC.escrever** e **VOC.imprimir**: Métodos diretos de VOC.
- **Math**, **Texto**: Objetos globais para funções utilitárias.
- **Não existe subobjeto (ex: VOC.Console)**.  
  Use sempre a forma direta: `VOC.escrever()`.

## Exemplo

```gurudev
VOC.escrever("Oi");       // OK
VOC.Console.escrever("Oi"); // Inválido!
Math.abs(-5);             // OK
```