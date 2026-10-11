# Benchmark V2 (piloto) do Assistente GuruDev

Regras: [`REGRAS.md`](REGRAS.md). Casos: [`casos.json`](casos.json). Este diretório fica fora da base de conhecimento do Assistente (verificado por teste).

## Arquivos

- `casos.json`: os 13 casos do piloto.
- `avaliacao.py`: critérios automáticos e telemetria da busca.
- `coletor.py`: roda os casos contra o servidor e grava a evidência (JSONL).
- `analisar.py`: placar, veredito, limite superior e amostra para revisão cega.
- `test_v2.py`: garantias do protocolo, rodadas na suíte (sem modelo).

## Rodada oficial (na VM, depois do merge)

```bash
cd /opt/gurudev-core
sudo git fetch origin && sudo git checkout <sha-do-merge>
sudo systemctl restart assistente-gurudev
.venv/bin/python benchmarks/v2/coletor.py --modelo qwen3:1.7b \
    --commit-esperado <sha-do-merge> --saida ~/v2-1.7b.jsonl
```

São 59 execuções (3 por caso normal, 5 por crítico). Teste do ambiente antes, não oficial: acrescente `--limite 2` e use outro arquivo de saída.

## Análise e revisão cega

```bash
python benchmarks/v2/analisar.py ~/v2-1.7b.jsonl --amostra 8
# preencher a coluna classe_humana de revisao_cega.csv, sem abrir chave_revisao.json
python benchmarks/v2/analisar.py ~/v2-1.7b.jsonl --revisao revisao_cega.csv --chave chave_revisao.json
```

Classes aceitas na revisão: `correta`, `parcial`, `erro_factual`, `alucinacao_com_citacao`, `abstencao_correta`, `abstencao_indevida`.
