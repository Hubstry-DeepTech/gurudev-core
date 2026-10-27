# fuzz/ — Testes em massa da GuruDev (geração pela gramática e fuzzing)

Ferramentas para gerar e executar programas GuruDev em grande quantidade, achar
falhas do lexer, do parser e do interpretador, reduzi-las a casos mínimos e
transformá-las em testes.

Fuzzing é a técnica de bombardear um programa com entradas geradas ou mutadas
automaticamente, em busca de falhas. "Guiado por cobertura" quer dizer que as
entradas que alcançam código novo do interpretador são guardadas e mutadas de
novo; as que não acrescentam nada são descartadas.

## Arquivos

| Arquivo | Função |
|---|---|
| `executor.py` | Roda cada programa num processo próprio (fork), com timeout, limite de memória, de CPU, de arquivo e de processos. Coleta cobertura de `src/` e classifica o resultado. |
| `baseline.py` | Linha de base: commit, versões, hashes de `src/`, suíte com cobertura, exemplos e nós da AST sem execução. |
| `sementes.py` | Programas reais (exemplos e textos dos testes) usados como ponto de partida, e o vocabulário de tokens observado. |
| `gramatica.py` | Gera programas a partir das produções do parser PLY, lidas em tempo de execução. |
| `fuzzer.py` | Laço de fuzzing paralelo: gramática, mutação, cruzamento e valores-limite. Critérios de parada configuráveis. |
| `triagem.py` | Reproduz cada falha 3 vezes, minimiza por delta debugging e agrupa em famílias. |
| `cobertura.py` | Reexecuta o corpus sob coverage.py e compara com a suíte (mesma métrica do baseline). |
| `gerar_testes.py` | Gera `tests/fuzz_regressoes/` (regressões e conformidade) a partir da triagem. |
| `analise-falhas.md` | Análise humana das famílias: causa, evidência e justificativa de cada xfail. |
| `rodar_vm.sh` | Rodada completa numa VM descartável, com desligamento automático e sincronização. |

## Classificação dos resultados

`OK`, `SINTAXE` e `ERRO_GURU` são comportamentos esperados (o programa rodou,
ou foi rejeitado com erro da própria linguagem). Todo o resto é falha:
`CRASH_LEXER`, `CRASH_PARSER`, `CRASH_INTERP` (exceção Python vazando),
`RECURSAO`, `TIMEOUT`, `MEMORIA` e `MORTO`.

Um `TIMEOUT` dentro de um laço do próprio programa (`while (true)`) é esperado e
não é registrado como falha. Os demais timeouts guardam o ponto exato onde o
programa estava, para separar travamento interno de laço legítimo.

## Uso local

```bash
pip install -r fuzz/requirements-fuzz.txt          # Python 3.12+ para a cobertura
python3 fuzz/baseline.py --saida resultados/baseline
python3 fuzz/fuzzer.py   --saida resultados/piloto --processos 2 --max-minutos 30
python3 fuzz/triagem.py  --rodada resultados/piloto --saida resultados/triagem
python3 fuzz/cobertura.py --rodada resultados/piloto --baseline resultados/baseline --saida resultados/cobertura
python3 fuzz/gerar_testes.py --triagem resultados/triagem --rodada resultados/piloto
pytest tests/test_fuzz_regressoes.py
```

Para encerrar uma rodada com segurança: `touch resultados/piloto/PARAR`, ou Ctrl+C.

## Segurança do harness

- Processo filho em sessão própria; no timeout, o grupo inteiro é morto.
- `RLIMIT_AS` (memória), `RLIMIT_CPU`, `RLIMIT_FSIZE` (1 MB) e `RLIMIT_NPROC` (sem novos processos).
- Diretório de trabalho temporário; entrada padrão fixa; semente aleatória fixa.
- Subescrita Python com builtins restritos (sem `open`, `input`; import só de módulos puros).
- Saída do programa truncada em 4 KB.

Limite conhecido: o harness não é um sandbox de sistema operacional. Ver
`analise-falhas.md`, seção de segurança: código GuruDev puro alcança atributos
Python dos valores (`s.__class__`). Na VM, rode como usuário sem privilégios e
sem segredos na máquina.

## Reprodutibilidade

- Cada falha é salva com o programa que a reproduz; a triagem confirma 3 vezes.
- O corpus (`corpus/*.guru`) é o conjunto de entradas que trouxe cobertura nova;
  reexecutá-lo reproduz a cobertura medida.
- A ordem de execução em paralelo não é determinística; os artefatos salvos são.
