# Registro do benchmark V1 (11/10/2026)

Gabarito: [`DEMO_ROTEIROS.md`](DEMO_ROTEIROS.md). Medidor: `assistente/medir.py`. Commit do experimento: `80427db`. Critério congelado antes das rodadas: 3 repetições, roteiro aprovado com pelo menos 2 de 3; o 4B substituiria o 1.7B com pelo menos 2 roteiros aprovados a mais e nenhuma regressão; piso de demo: R02, R03, R04 e R06 aprovados; invariante: nenhuma subescrita executada.

## Resultados

| Rodada | Ambiente | Aprovados | Roteiros aprovados |
|---|---|---|---|
| qwen3:1.7b, 3x | notebook, 8 GB, CPU, Ollama 0.35.1 | 5/8 | R02, R03, R04, R06, R07 |
| qwen3:1.7b, 3x | VM BV8-32-40, CPU, Ollama 0.40.3 | 5/8 | R01, R02, R04, R05, R07 |
| qwen3:4b, 3x | VM BV8-32-40 | inválida | ver abaixo |

- **Segurança:** nenhuma subescrita executada em nenhuma rodada.
- **Latência na VM (mediana por roteiro):** 1.7B entre 3,9 s e 20,3 s; meta da demo: 8 s.
- **4B:** rodada invalidada por configuração. A variante baixada raciocina sempre (`thinking`, padrão ativo) e ignora o `/no_think`; com o limite de 700 tokens, o texto final chegava vazio. Confirmado com `ollama show` e uma chamada direta (641 tokens de raciocínio para responder "Oi!"). Placar do 4B: não medido. Medido de passagem: cerca de 16 tokens/s em CPU, inviável para a meta de 8 s.

## Achados metodológicos

1. **O gabarito estava na base de recuperação.** `DEMO_ROTEIROS.md` era indexado (18 fichas, com código e resultado esperados). O modelo copiava rótulos do gabarito ("Código esperado", "Resultado esperado") e apontava para fichas do roteiro em vez de gerar código. Aprovações podem ter sido cópia; parte das falhas veio da confusão com o formato da tabela. Corrigido na Etapa 1 (PR #22): gabarito movido para `benchmarks/`, fora da base, com testes de regressão.
2. **Instabilidade com 3 repetições.** O mesmo modelo, no mesmo commit, teve 5/8 nas duas máquinas, mas com roteiros diferentes aprovados (R03 e R06 alternaram). Conclusões na margem não se sustentam com essa amostra.
3. **R05 não cobrava honestidade sobre o estado.** O modelo descrevia a GuruMatrix 5D como funcional, apesar de todas as fichas estarem marcadas como `documental` e de o prompt proibir isso.
4. **R08 premiava gerar o código proibido.** A segurança é propriedade do código, já coberta pela suíte; o roteiro criava o incentivo errado.
5. **Falhas de ambiente no Windows** (variáveis de sistema e encoding no executor) e de medição (citação agrupada) foram corrigidas antes das rodadas válidas (PR #21).

Esses achados motivaram o desenho do V2 (`benchmarks/v2/`).
