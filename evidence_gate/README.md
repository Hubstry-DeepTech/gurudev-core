# GuruDev Evidence Gate (MVP)

Portão de evidências. Um modelo de linguagem (LLM, *large language model*)
responde a uma pergunta sobre um texto-fonte. Ele também lista afirmações, cada
uma com a citação literal que a sustenta. O Python faz verificações
determinísticas. Uma política GuruDev estática (`politica.guru`), executada
pelo interpretador real da linguagem, decide o veredito.

| Veredito | Quando |
|---|---|
| `BLOQUEADO` | falha ou tempo esgotado do modelo, fonte vazia, JSON inválido, esquema errado, nenhuma afirmação, ou alguma citação ausente da fonte |
| `REVISAO_SEMANTICA` | todas as citações existem na fonte, mas ao menos uma afirmação é paráfrase ou inferência, **ou a resposta (`answer`) não é trecho literal da fonte** |
| `VALIDADO_LITERAL` | toda afirmação é igual à sua citação, toda citação está na fonte **e a resposta também é trecho literal da fonte** |

**Limite de produto.** O veredito avalia a resposta e as afirmações por um
critério literal operacional, definido abaixo. `VALIDADO_LITERAL` não significa
que a informação seja verdadeira, nem que sua semântica tenha sido
integralmente comprovada. Uma resposta composta de trechos literais também pode
estar fora de contexto ou induzir a uma conclusão errada.

## Como funciona

1. `portao.py` envia fonte e pergunta ao modelo e pede JSON estrito:
   `{"answer": "...", "claims": [{"text": "...", "evidence_quote": "..."}]}`.
2. `verificacao.py` interpreta o JSON. Rejeita chaves duplicadas, `NaN` e
   campos extras. Depois confere o esquema e procura cada citação na fonte.
3. A resposta (`answer`) também é verificada: precisa ser um trecho contínuo
   da fonte. Uma síntese ou dedução, mesmo correta, leva a `REVISAO_SEMANTICA`.
   Esse critério foi incluído após o teste real de 28/10/2026, em que o modelo
   respondeu "Não" a uma pergunta sobre o inciso XI do artigo 5º da
   Constituição. Era uma inferência, sustentada por duas citações literais.
4. Normalização única, aplicada aos dois lados: Unicode NFC (forma de
   composição canônica) e espaços em branco colapsados. Não há casamento
   aproximado: maiúsculas, acentos e pontuação contam. A única tolerância de
   envelope é uma cerca ` ``` ` ou ` ```json ` em volta do JSON inteiro.
5. O resultado vira oito indicadores, só do tipo `bool` ou `int`.
6. `politica.py` confere nomes e tipos dos indicadores e os injeta no
   interpretador. Em seguida executa `politica.guru`.

**Falha fechada.** Indicador ausente, extra ou de tipo errado, erro do
interpretador, veredito desconhecido, falha do modelo, resposta truncada ou
tempo esgotado resultam em `BLOQUEADO`.

O texto do modelo nunca é executado: só o arquivo `politica.guru` passa pelo
parser, e há teste que verifica isso. Nenhum LLM avalia outro LLM.

## Processamento assíncrono

A página envia a análise (`POST /api/verificar`, resposta 202 com um id) e
consulta o estado (`GET /api/tarefa/<id>`) a cada 1,5 s. Estados:
`aguardando`, `processando`, `concluida` e `falha`. Tudo fica em memória: um
trabalhador, no máximo 20 tarefas aguardando e 200 registradas. Resultados
expiram em 1 hora. Não há banco de dados nem serviço adicional.

## Rodar localmente (sem rede, modelo simulado)

```bash
python3 -m evidence_gate.demo --simulado        # 3 casos, um por veredito
GURU_EVIDENCE_SIMULADO=1 python3 -m evidence_gate.servidor   # http://127.0.0.1:8080
python3 -m pytest -q tests/test_evidence_gate.py
```

## Rodar na VM `hubstry-vm-001` (modelo real, GLM-5.3 via Digiti)

A chave fica no Secret Manager (`digiti-maas-api-key`). Ela é lida a cada
início e não vai para arquivo, repositório nem registro. O servidor escuta só
em `127.0.0.1:8080`, sem porta pública. O acesso é por túnel SSH via IAP
(*Identity-Aware Proxy*, proxy com verificação de identidade do Google Cloud),
a partir do Cloud Shell.

```bash
# 1) No Cloud Shell: iniciar a VM, baixar o código e subir o servidor
gcloud compute instances start hubstry-vm-001 --zone us-central1-a
gcloud compute ssh hubstry-vm-001 --zone us-central1-a --tunnel-through-iap --command '
  test -d gurudev-core || git clone -q https://github.com/Hubstry-DeepTech/gurudev-core
  cd gurudev-core && git fetch -q origin && git checkout -q feat/evidence-gate-mvp && git pull -q
  bash evidence_gate/iniciar_vm.sh --demo'

# 2) No Cloud Shell: túnel (deixe rodando) e depois "Web Preview > porta 8080"
gcloud compute ssh hubstry-vm-001 --zone us-central1-a --tunnel-through-iap -- -N -L 8080:127.0.0.1:8080

# 3) Ao terminar: desligar a VM (para de cobrar CPU; o disco continua cobrando)
gcloud compute instances stop hubstry-vm-001 --zone us-central1-a
```

Variáveis: `GURU_MODELO_URL`, `GURU_MODELO_NOME`, `GURU_MODELO_API_KEY`,
`GURU_MODELO_TEMPO` (300 s), `GURU_MODELO_MAX_TOKENS` (8000; no GLM-5.3 os
tokens de raciocínio contam neste teto), `GURU_HOST`, `GURU_PORTA`.

## Limites conhecidos

- Literal não é verdadeiro: o portão verifica procedência textual, não fatos.
  Substring não demonstra verdade, implicação jurídica nem correção semântica.
- Falso positivo aceito no MVP: uma resposta correta montada com frases
  literais de pontos diferentes da fonte não forma um trecho contínuo e vai
  para `REVISAO_SEMANTICA`. Na prática, `VALIDADO_LITERAL` é um veredito raro
  e forte, e `REVISAO_SEMANTICA` é o caso comum ("citações reais, conclusão do
  modelo").
- Afirmações curtas podem ser literais e pouco informativas. A revisão humana
  continua necessária, sobretudo em `REVISAO_SEMANTICA`.
- Reiniciar o servidor apaga as tarefas em memória.
- O interpretador GuruDev não é um sandbox. Aqui ele só executa o arquivo de
  política versionado, nunca conteúdo externo.
