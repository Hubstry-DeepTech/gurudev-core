"""Analise de uma rodada do benchmark V2 (regras em REGRAS.md).

Uso:
  python benchmarks/v2/analisar.py rodada.jsonl
  python benchmarks/v2/analisar.py rodada.jsonl --amostra 8      # gera revisao cega
  python benchmarks/v2/analisar.py rodada.jsonl --revisao revisao.csv --chave chave.json

O arquivo de evidencia nunca e alterado; tudo aqui e derivado dele.
"""

import argparse
import csv
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avaliacao as av  # noqa: E402

CLASSES_HUMANAS = {
    "correta", "parcial", "erro_factual", "alucinacao_com_citacao",
    "abstencao_correta", "abstencao_indevida",
}
PONTOS = {
    "alucinacao_com_citacao": -2, "erro_factual": -1, "abstencao_correta": 1,
    "abstencao_indevida": 0, "parcial": 0.5, "correta": 1, "incorreta": 0,
}


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        todos = [json.loads(linha) for linha in f if linha.strip()]
    return [r for r in todos if not r.get("descartado")]


POSITIVAS = ("correta", "abstencao_correta")


def aplicar_revisao(registros, revisao, chave):
    """Aplica a revisao cega (REGRAS.md, secao 6). Devolve as respostas da
    chave que ficaram sem classe humana; com qualquer pendencia nao ha
    veredito.

    - Resposta delegada ao humano (revisao_humana=True): a classe humana
      decide o resultado, nos dois sentidos.
    - Resposta da amostra: o humano so pode rebaixar. Uma falha detectada
      por regra (sem citacao, sem evidencia, codigo que nao roda) continua
      falha; a divergencia fica registrada.
    """
    mapa = json.loads(Path(chave).read_text("utf-8"))
    por_run = {r["run_id"]: r for r in registros}
    classificados = set()
    with open(revisao, encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            classe = (linha.get("classe_humana") or "").strip()
            if not classe:
                continue
            if classe not in CLASSES_HUMANAS:
                sys.exit(f"classe humana invalida: {classe!r}")
            r = por_run[mapa[linha["token"]]]
            classificados.add(linha["token"])
            r["classe_humana"] = classe
            if r["avaliacao"]["revisao_humana"]:
                r["classe_final"] = classe
                r["passou_final"] = classe in POSITIVAS
            elif r["avaliacao"]["passou"]:
                r["classe_final"] = classe
                r["passou_final"] = classe in POSITIVAS
            else:
                r["divergencia"] = classe in POSITIVAS
    return sorted(set(mapa) - classificados)


def amostra_cega(registros, n, semente=2026):
    """Todas as respostas marcadas para revisao, mais n sorteadas entre as
    de factualidade, abstencao e recuperacao. O modelo nao aparece."""
    rng = random.Random(semente)
    obrigatorias = [r for r in registros if r["avaliacao"]["revisao_humana"]]
    resto = [
        r for r in registros
        if r not in obrigatorias
        and r["dimensao"] in ("factualidade", "abstencao", "recuperacao")
        and r["avaliacao"]["classe"] != "erro_ambiente"
    ]
    escolhidas = obrigatorias + rng.sample(resto, min(n, len(resto)))
    rng.shuffle(escolhidas)
    chave, linhas = {}, []
    for i, r in enumerate(escolhidas, 1):
        token = f"T{i:03d}"
        chave[token] = r["run_id"]
        fontes = "; ".join(
            f"{f.get('id')} {f.get('fonte')} > {f.get('secao', '')[-50:]}"
            for f in r["resposta"].get("fontes") or []
        )
        linhas.append({
            "token": token,
            "pergunta": r["pergunta"],
            "resposta": r["resposta"].get("texto") or "",
            "fontes_recebidas": fontes,
            "classe_humana": "",
        })
    with open("revisao_cega.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    Path("chave_revisao.json").write_text(json.dumps(chave, indent=1), "utf-8")
    print(f"revisao_cega.csv ({len(linhas)} respostas) e chave_revisao.json "
          "gerados. Quem revisa NAO deve abrir a chave antes de terminar.")


def resumir(registros, revisao_pendente):
    casos = {c["id"]: c for c in av.carregar_casos()}
    por_caso = defaultdict(list)
    for r in registros:
        por_caso[r["caso"]].append(r)
    modelos = {r["modelo"] for r in registros}
    commits = {r["repo_commit"][:12] for r in registros}
    print(f"# Rodada V2  modelos={sorted(modelos)}  commits={sorted(commits)}")
    if any(not r["oficial"] for r in registros):
        print("ATENCAO: contem registros NAO oficiais (--limite).")
    print()
    print("| caso | dimensao | critico | ok/validas | ambiente | aprovado "
          "| classes | mediana s |")
    print("|---|---|---|---|---|---|---|---|")
    aprovados, alucinacoes, inconclusivos = {}, 0, []
    classes_dim = defaultdict(Counter)
    for cid, c in casos.items():
        rs = por_caso.get(cid, [])
        exigidas = av.REPETICOES[c["critico"]]
        # vale a ordem cronologica; repeticoes alem do exigido sao ignoradas
        validas = sorted(
            (r for r in rs if r["avaliacao"]["classe"] != "erro_ambiente"),
            key=lambda r: r["timestamp"],
        )[:exigidas]
        ok = sum(r.get("passou_final", r["avaliacao"]["passou"]) for r in validas)
        classes = Counter(
            r.get("classe_final", r["avaliacao"]["classe"]) for r in validas)
        aluc = classes["alucinacao_com_citacao"]
        alucinacoes += aluc
        if len(validas) < exigidas:
            inconclusivos.append(cid)
            aprovado = None
        else:
            aprovado = ok >= av.MINIMO_APROVACAO[c["critico"]] and aluc == 0
        aprovados[cid] = aprovado
        classes_dim[c["dimensao"]].update(classes)
        mediana = statistics.median([r["duracao_s"] for r in rs]) if rs else 0
        print(f"| {cid} | {c['dimensao']} | {'sim' if c['critico'] else 'nao'} "
              f"| {ok}/{len(validas)} | {len(rs) - len(validas)} "
              f"| {'-' if aprovado is None else ('SIM' if aprovado else 'nao')} "
              f"| {dict(classes)} | {mediana:.1f} |")

    print("\n## Por dimensao")
    for dim in sorted(classes_dim):
        ids = [i for i, c in casos.items() if c["dimensao"] == dim]
        n_ap = sum(1 for i in ids if aprovados[i])
        pontos = sum(PONTOS.get(k, 0) * v for k, v in classes_dim[dim].items())
        print(f"- {dim}: {n_ap}/{len(ids)} casos aprovados; classes "
              f"{dict(classes_dim[dim])}; pontos {pontos:+g}")

    criticos = [i for i, c in casos.items() if c["critico"]]
    pendentes = list(revisao_pendente)
    pendentes += [r["run_id"] for r in registros
                  if r["avaliacao"]["revisao_humana"] and "classe_humana" not in r]
    divergencias = [r["run_id"] for r in registros if r.get("divergencia")]
    n_exec = sum(1 for r in registros
                 if r["avaliacao"]["classe"] != "erro_ambiente")
    print("\n## Veredito (REGRAS.md, secao 4)")
    print(f"- alucinacoes com citacao confirmadas: {alucinacoes}")
    if pendentes:
        print(f"- PENDENTE: revisao cega incompleta ({len(pendentes)} itens); "
              "nao ha veredito antes dela.")
    if divergencias:
        print(f"- divergencias (humano aprovou falha detectada por regra; a "
              f"regra prevalece): {divergencias}")
    if inconclusivos:
        print(f"- INCONCLUSIVO: repeticoes validas insuficientes em "
              f"{inconclusivos}; repetir esses casos.")
    if not pendentes and not inconclusivos:
        if alucinacoes == 0 and n_exec:
            print(f"- limite superior aprox. (95%) da taxa de alucinacao com "
                  f"citacao: {3 / n_exec:.1%} ({n_exec} execucoes validas)")
        passou = all(aprovados[i] for i in criticos) and alucinacoes == 0
        print(f"- passou nos criticos: {'SIM' if passou else 'NAO'} "
              f"({sum(1 for i in criticos if aprovados[i])}/{len(criticos)})")

    tel = [r["telemetria_busca"] for r in registros]
    print(f"\n_Telemetria da busca (nao e criterio): "
          f"{sum(t['apresentacao'] for t in tel)} respostas com fichas de "
          f"apresentacao; {sum(t['vazia'] for t in tel)} com busca vazia._")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("arquivos", nargs="+")
    p.add_argument("--amostra", type=int, default=0)
    p.add_argument("--revisao")
    p.add_argument("--chave")
    a = p.parse_args()
    registros = [r for arq in a.arquivos for r in ler(arq)]
    if a.amostra:
        amostra_cega(registros, a.amostra)
    if a.revisao and a.chave:
        pendente = aplicar_revisao(registros, a.revisao, a.chave)
    else:
        # sem a revisao cega aplicada, todo o protocolo esta pendente
        pendente = ["revisao cega ainda nao aplicada (--revisao e --chave)"]
    resumir(registros, pendente)

if __name__ == "__main__":
    main()
