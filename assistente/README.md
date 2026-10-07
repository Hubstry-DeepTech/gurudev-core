# Assistente GuruDev — Base de conhecimento

Base consultada pelo Assistente GuruDev antes de responder. Cada ficha registra origem (arquivo e seção), tipo e estado.

## Estados

| Estado | Significado | Origem do estado |
|---|---|---|
| `roda_hoje` | Código que executa no interpretador atual | Evidência executável, verificada pelo teste |
| `em_reimplementacao` | Recurso ou exemplo ainda não reincorporado | Seção "Em reimplementação" do README e lista `PENDENTES` de `tests/test_examples.py` |
| `documental` | O que a documentação declara | Texto dos documentos; não é evidência de execução |

Regra: a fonte documental informa o que a GuruDev declara; somente evidência executável recebe `roda_hoje`.

## Escopo da fase 1

Documentos em português: `README.md` (sem as seções de negócio), `docs/SINTAXE.md`, `docs/GRAMMAR_V1_0_0_ALPHA.md`, `docs/GURU_MATRIX5D.md`, `docs/BIBLIOTECA_PADRAO.md`, `docs/EXEMPLOS_VALIDACAO.md`, `docs/ARQUITETURA_NAMESPACES.md`, `docs/WHITEPAPER.md`, `docs/DEMO_ROTEIROS.md` e `examples/*.guru`.

Fora da base: modelo financeiro, modelos de receita, perfil do fundador, pitch decks e roadmap. O Assistente trata da tecnologia; não representa comercialmente a empresa.

## Uso

```
python assistente/gerar_base.py   # regenera base_conhecimento.json
pytest assistente/                # verifica a base
```

O teste falha se a base estiver desatualizada em relação aos documentos, se uma ficha `roda_hoje` deixar de executar ou se um exemplo `em_reimplementacao` passar a executar.
