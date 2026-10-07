# Arquitetura de Namespaces e Hierarquia de Objetos

- **VOC**: Objeto global, acesso direto via VOC.
- **VOC.escrever** e **VOC.imprimir**: Métodos diretos de VOC.
- **Math**, **Texto**: Objetos globais para funções utilitárias.
- **Não existe subobjeto (ex: VOC.Console)**.  
  Use sempre a forma direta: `VOC.escrever()`.

## Estado de implementação (runtime atual)

> Verificado em 07/10/2026: `VOC.escrever()` e `VOC.imprimir()` funcionam. Os objetos `Math` e `Texto` ainda não existem no interpretador atual; o exemplo `Math.abs(-5)` abaixo descreve a API planejada. Equivalentes que funcionam hoje: ver "Estado de implementação" em [BIBLIOTECA_PADRAO.md](BIBLIOTECA_PADRAO.md).

## Exemplo

```gurudev
VOC.escrever("Oi");       // OK
VOC.Console.escrever("Oi"); // Inválido!
Math.abs(-5);             // OK
```