# Testes de Validação — GuruDev®

## Válidos

```gurudev
VOC.escrever("Tudo certo!");
String nome = VOC.ler();
Math.abs(-99);
Texto.maiusculo("abc");
```

## Inválidos

```gurudev
var escrever = "tentando";   // ERRO: nome reservado
func VOC() { ... }           // ERRO: nome reservado
VOC = 1;                     // ERRO: não pode sobrescrever objeto nativo
Texto.escrever("oi");        // ERRO: método não existe nesse objeto
```
