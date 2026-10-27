# Análise das falhas — pilotos de fuzzing

Commit analisado: `2d1bb1d5a5a5c8104e770a91a32931dd7d57c40a` (main, 11/10/2026).
Ambiente: Python 3.13.17, PLY 3.11, 2 núcleos. Duas rodadas locais, semente 7:

| Rodada | Duração | Execuções | Exec/s | Corpus | Assinaturas de falha |
|---|---|---|---|---|---|
| piloto | 30 min | 78.365 | 43,5 | 160 | 32 |
| piloto2 (gerador com a API nativa) | 15 min | 44.589 | 49,5 | 209 | 61 |

A triagem conjunta reduziu 66 assinaturas a 11 famílias de bug, mais uma
família de comportamento esperado (laços infinitos do próprio programa).
Contagens de ocorrências abaixo somam as duas rodadas.

Este documento é a análise humana que acompanha a triagem automática
(`fuzz/triagem.py`). Para cada família ele registra causa, evidência, gravidade,
correção sugerida e a justificativa do xfail. Um caso só entra como
`xfail(strict=True)` nos testes se a família estiver no bloco `xfail` no fim
deste arquivo. Quando o bug for corrigido, o teste vira XPASS e falha: é o aviso
para tirar a família do bloco.

Escala de gravidade:
- **P1**: programa válido, ou recurso documentado, quebra; ou risco de segurança.
- **P2**: erro do programa vira exceção Python em vez de erro da linguagem.
- **P3**: limite de recurso ou validação ausente, sem quebrar programa válido.

## Reconciliação com a sonda inicial

A sonda de 2,5 minutos, sem semente fixa, relatou três indícios. O piloto,
determinístico e com triagem, esclarece os três:

| Indício da sonda | Resultado no piloto |
|---|---|
| `IndexError` no parser | Confirmado: família F1 (`if`/`elif` sem `else`). |
| `TypeError` em operação binária | Confirmado: família F5 (operadores sem checagem de tipo). |
| travamento acima de 5 s | Não confirmado como travamento interno. Os três timeouts do piloto, reexecutados, estavam todos dentro de um laço infinito do próprio programa (`while` com condição sempre verdadeira). Foram reclassificados como esperados. Nenhum travamento do lexer, do parser ou do interpretador apareceu. |

## Famílias

### F1 — `if` com `elif` e sem `else` derruba o parser (P1)

- Família: `CRASH_PARSER|IndexError|p_if_elif_statement`. Ocorrências: 1.573.
- Caso mínimo: `if(7.0){}senao_se(abs){}`.
- Causa: `src/parser.py`, `p_if_elif_statement`. A produção tem 6 símbolos
  (`IF_KEYWORD LPAREN producao_de_valor RPAREN bloco_corpo elif_chain`), mas o
  código lê `p[7]`. O certo é `p[6]`.
- Efeito: todo `if ... elif ...` sem `else` final é inválido na prática. Com
  `else` funciona, porque outra produção (`else_opt`) é usada. A suíte só testa
  a forma com `else` (`tests/test_fluxo.py`), por isso passou.
- Correção sugerida: `for cond, body in p[6]:`.

### F2 — atribuição a propriedade com caso gramatical derruba o parser (P1)

- Família: `CRASH_PARSER|TypeError|p_prop_atribuicao_caso`. Ocorrências: 2.879.
- Caso mínimo: `ACU.x.x=20;`.
- Causa: `p_prop_atribuicao_caso` cria `PropAtribuicao(..., caso_gramatical=p[1])`,
  mas a dataclass `PropAtribuicao` (`src/ast_nodes.py`) não tem esse campo.
- Efeito: a forma `CASO.objeto.prop = valor` nunca funciona.
- Correção sugerida: acrescentar `caso_gramatical: Optional[str] = None` em
  `PropAtribuicao` e decidir a semântica no interpretador.

### F3 — classe com `implements` dentro de um bloco derruba o parser (P1)

- Família: `CRASH_PARSER|AttributeError|visitar`. Ocorrências: 236.
- Caso mínimo: `$$bloco$$¡codigo!classe criar_pessoa implements a{}!/codigo![/bloco]`.
- Causa: `visitar`, dentro de `p_bloco` (`src/parser.py`), propaga atributos
  gm_* para os nós filhos. Ele percorre toda lista da dataclass e chama
  `setattr` em cada item. `DefinicaoClasse.interfaces` é uma lista de `str`, e
  `setattr` em `str` falha.
- Correção sugerida: em `visitar`, visitar apenas itens que sejam `Node`.

### F4 — `break`, `continue` e `return` fora de contexto vazam sinais internos (P2)

- Família: `CRASH_INTERP|SinalDeControle` (3 assinaturas). Ocorrências: 10.805.
- Casos mínimos: `break;`, `continua;`, `return;`.
- Causa: `_x_Break`, `_x_Continue` e `_x_Retorno` levantam `BreakSignal`,
  `ContinueSignal` e `ReturnSignal`, que só são capturados dentro de laços e
  funções. No nível de programa, eles escapam como exceções Python.
- Correção sugerida: capturar os três em `interpretar` e converter em
  `GuruDevError("break fora de laço")` etc., ou rejeitar na análise semântica.

### F5 — operadores sem checagem de tipo (P2)

- Família: `CRASH_INTERP|TypeError|_x_OperacaoBinaria` (9 assinaturas, uma por
  operador) e `CRASH_INTERP|ZeroDivisionError|_x_OperacaoBinaria` (2). Ocorrências: 1.354.
- Casos mínimos: `return"A"-"Acme".dobro;`, `return", tenho ">=10.0;`,
  `dividir=verdadeiro/(0);` e outros 8 em `tests/fuzz_regressoes/casos/`.
- Causa: `_x_OperacaoBinaria` (`src/interpreter.py`) delega direto ao Python
  (`left - right`, `left < right`, `left / right`...). Tipos incompatíveis e
  divisão por zero viram `TypeError`/`ZeroDivisionError`.
- Observação: o mesmo atalho herda semânticas do Python que talvez não sejam
  desejadas na linguagem, como `"ab" * 3` e `"a" % x` (formatação de string).
- Correção sugerida: validar tipos por operador e levantar `GuruDevError` com a
  linha e os tipos; tratar divisão e módulo por zero.

### F6 — operador unário sem checagem de tipo (P2)

- Família: `CRASH_INTERP|TypeError|_x_OperacaoUnaria`. Ocorrências: 243.
- Caso mínimo: `return-"ABC";`.
- Causa e correção: as mesmas de F5, em `_x_OperacaoUnaria`.

### F7 — biblioteca padrão sem validação de argumentos (P2)

- Família: `CRASH_INTERP|Nativas`, 42 assinaturas em 28 funções e métodos.
  Ocorrências: 3.694. Exceções: `TypeError` (27), `ValueError` (5),
  `RuntimeError` (4), `OverflowError` (3), `ZeroDivisionError` (2),
  `JSONDecodeError` (1).
- Agrupamento: a triagem junta numa família toda falha que nasce em
  `src/nativas.py` ou na linha do interpretador que chama a nativa
  (`nativa(*args)`), porque a causa é a mesma.
- Casos mínimos (todos em `tests/fuzz_regressoes/casos/`), por exemplo:
  `seno();`, `escrever(raiz(""));`, `escrever(raiz(1,0));`,
  `escrever(de_json(""));`, `escrever(minimo(""));`, `v=[];escrever(v.pop());`,
  `escrever(potencia(2,9223372036854775808));`, `a=["",2];a.ordenar();`.
- Causa: `src/nativas.py` chama o Python direto (`math.sin`, `abs`, `round`,
  `**`, `json.loads`, `min`, `list.sort`, `str.split`...) sem validar tipo,
  quantidade nem faixa dos argumentos. Algumas nativas já detectam o problema e
  escrevem boa mensagem, mas com a classe errada: `tamanho` levanta `TypeError`
  ("tipo_de(Int) nao suporta tamanho()") e `pop`/`primeiro`/`ultimo` levantam
  `RuntimeError` ("pop() em array vazio.").
- Correção sugerida: uma camada única de validação (decorador com aridade,
  tipos e faixas) que levante `GuruDevError`, e trocar `TypeError`/`RuntimeError`
  deliberados por `GuruDevError`.

### F8 — métodos Python dos valores acessíveis e sem validação (P2, ligado a S1)

- Família: `CRASH_INTERP|TypeError|_x_ChamadaMetodo`. Ocorrências: 54.
- Caso mínimo: `return"".count();`.
- Causa: quando o método não é da GuruDev, `_x_ChamadaMetodo` usa
  `getattr(obj, n.metodo)` e chama o método Python do valor. `count` não é um
  método GuruDev; é de `str` do Python.
- Correção: a mesma de S1.

### F9 — recursão sem limite da linguagem e aridade não checada (P3)

- Família: `RECURSAO|RecursionError|get_func`. Ocorrências: 15.
- Caso mínimo: `fatorial` chamando `fatorial()` sem argumento, sem caso base.
- Causa: duas lacunas. (1) A chamada de função do usuário não confere o número
  de argumentos: `fatorial()` com 0 argumentos é aceita. (2) Recursão infinita
  vira `RecursionError` do Python.
- Correção sugerida: checar aridade em `_x_ChamadaFuncao`; limitar profundidade
  e levantar `GuruDevError("profundidade máxima de recursão")`.

### F10 — repetição de texto sem limite de memória (P3)

- Família: `MEMORIA`. Ocorrências: 2.
- Caso mínimo: `if("ção🙂"*2147483648){}`.
- Causa: `*` entre texto e inteiro usa a repetição do Python; com um inteiro
  grande, tenta alocar gigabytes.
- Correção sugerida: decidir se `texto * inteiro` existe na linguagem; se
  existir, impor um limite de tamanho do resultado.

## Segurança

### S1 — código GuruDev puro alcança atributos internos do Python (P1 para a demo pública)

Fora do fuzzing, ao analisar F8, verifiquei manualmente um caminho mais sério.
`_x_AcessoPropriedade` termina em `getattr(obj, n.propriedade, None)` e
`_x_ChamadaMetodo` em `getattr(obj, n.metodo)`, sem nenhuma restrição de nome.
Identificadores podem começar com `_`. Resultado, sem nenhuma subescrita:

```
String s = "a";
Object c = s.__class__;
Object b = c.__base__;
escrever(b);          // imprime <class 'object'>
```

Chegar a `object` a partir de um valor qualquer é o primeiro passo das fugas
de sandbox conhecidas em Python. Não continuei além desse ponto. A política do
assistente público (`assistente/politica.py`, POL-01) bloqueia só subescritas,
então ela não cobre este caminho. Se a demo do assistente executa código
enviado por usuários, isso deve ser tratado antes de qualquer outra família.

Correção sugerida: em `_x_AcessoPropriedade` e `_x_ChamadaMetodo`, recusar nomes
que começam com `_` e, para valores que não são `Instancia`, permitir apenas os
métodos registrados em `StringMethods`/`ArrayMethods`, levantando `GuruDevError`
para o resto.

### S2 — subescrita Python executa com builtins completos (informativo)

`_x_SubescritaLinguagem` chama `exec(conteudo, {"__builtins__": builtins})`.
Isso é intencional (interoperabilidade) e já está bloqueado na demo pela POL-01.
O harness de fuzzing restringe os builtins por conta própria para proteger a
máquina de testes.

## Nós da AST sem execução

O baseline encontrou 5 classes da AST sem método `_x_` no interpretador:
`AnotacaoSemantica`, `BlocoCompensacao`, `Node`, `Parametro`, `Sobrescrita`.
O interpretador ignora esses nós em silêncio (`_x` devolve `None`). `Node` e
`Parametro` provavelmente não precisam de execução; `BlocoCompensacao` merece
confirmação, porque o recurso é documentado.

## Justificativa dos xfail

Todas as famílias abaixo têm causa identificada no código, caso mínimo estável
(reproduz 3 de 3 vezes) e correção sugerida acima. Elas entram como xfail para
que a suíte continue verde enquanto as correções não são feitas, sem esconder o
bug: cada uma aparece no relatório do pytest como XFAIL com o motivo, e qualquer
correção faz o teste falhar como XPASS até o marcador ser removido.

```xfail
CRASH_PARSER|IndexError|p_if_elif_statement: F1 (P1) parser lê p[7] numa produção de 6 símbolos; ver fuzz/analise-falhas.md
CRASH_PARSER|TypeError|p_prop_atribuicao_caso: F2 (P1) PropAtribuicao não tem o campo caso_gramatical; ver fuzz/analise-falhas.md
CRASH_PARSER|AttributeError|visitar: F3 (P1) visitar faz setattr em str de DefinicaoClasse.interfaces; ver fuzz/analise-falhas.md
CRASH_INTERP|SinalDeControle: F4 (P2) Break/Continue/ReturnSignal escapam fora de laço ou função; ver fuzz/analise-falhas.md
CRASH_INTERP|TypeError|_x_OperacaoBinaria: F5 (P2) operadores delegam ao Python sem checar tipos; ver fuzz/analise-falhas.md
CRASH_INTERP|ZeroDivisionError|_x_OperacaoBinaria: F5 (P2) divisão e módulo por zero sem tratamento; ver fuzz/analise-falhas.md
CRASH_INTERP|TypeError|_x_OperacaoUnaria: F6 (P2) operador unário sem checagem de tipo; ver fuzz/analise-falhas.md
CRASH_INTERP|Nativas: F7 (P2) biblioteca padrão sem validação de argumentos; ver fuzz/analise-falhas.md
CRASH_INTERP|TypeError|_x_ChamadaMetodo: F8 (P2) método Python do valor chamado sem validação; ver fuzz/analise-falhas.md
RECURSAO|RecursionError|get_func: F9 (P3) recursão sem limite da linguagem e aridade não checada; ver fuzz/analise-falhas.md
MEMORIA||?: F10 (P3) repetição de texto sem limite de tamanho; ver fuzz/analise-falhas.md
```
