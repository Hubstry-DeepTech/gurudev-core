"""
fuzz/gerar_testes.py — Transforma a triagem e o corpus em testes do pytest.

Gera dois conjuntos em tests/fuzz_regressoes/:

1. Regressões (casos.json + casos/*.guru)
   Um caso mínimo por assinatura de falha. O teste exige que o programa termine
   em OK, SINTAXE ou ERRO_GURU, isto é, sem exceção Python vazando.
   Um caso só vira xfail se a família dele tiver causa e justificativa escritas
   em fuzz/analise-falhas.md (bloco ```xfail``` com "familia: motivo"). Sem isso,
   o caso entra como teste normal e falha, de propósito.

2. Conformidade (conformidade.json + conformidade/*.guru)
   Programas do corpus que terminam em OK com saída idêntica em 3 execuções,
   cada uma num servidor novo (semente de hash diferente). O teste compara a
   saída atual com a registrada: mudanças de comportamento aparecem como falha.

Uso:
  python3 fuzz/gerar_testes.py --triagem resultados/triagem --rodada resultados/piloto --max-conformidade 60
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from executor import Executor  # noqa: E402

DESTINO = os.path.join(REPO, "tests", "fuzz_regressoes")


def motivos_xfail():
    """Lê fuzz/analise-falhas.md: blocos ```xfail com linhas 'FAMILIA: motivo'."""
    caminho = os.path.join(AQUI, "analise-falhas.md")
    if not os.path.exists(caminho):
        return {}
    texto = open(caminho, encoding="utf-8").read()
    out = {}
    for bloco in re.findall(r"```xfail\n(.*?)```", texto, re.S):
        for linha in bloco.strip().splitlines():
            if ": " in linha:
                fam, motivo = linha.split(": ", 1)
                out[fam.strip()] = motivo.strip()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--triagem", required=True)
    ap.add_argument("--rodada", required=True, nargs="+")
    ap.add_argument("--max-conformidade", type=int, default=60)
    ap.add_argument("--max-bytes", type=int, default=1500)
    a = ap.parse_args()

    for sub in ("casos", "conformidade"):
        shutil.rmtree(os.path.join(DESTINO, sub), ignore_errors=True)
        os.makedirs(os.path.join(DESTINO, sub), exist_ok=True)

    # ---- 1. regressões
    tri = json.load(open(os.path.join(a.triagem, "triagem.json"), encoding="utf-8"))
    motivos = motivos_xfail()
    casos = []
    for it in tri["itens"]:
        if it["familia"] in ("NAO-REPRODUZ", "ESPERADO|laco-do-programa") or it["assinatura"] == "TIMEOUT|laco-do-programa":
            continue
        nome = os.path.basename(it["caso"])
        shutil.copy(os.path.join(a.triagem, it["caso"]), os.path.join(DESTINO, "casos", nome))
        casos.append({"arquivo": f"casos/{nome}", "familia": it["familia"], "assinatura": it["assinatura"],
                      "xfail": motivos.get(it["familia"])})
    casos.sort(key=lambda c: c["arquivo"])
    json.dump(casos, open(os.path.join(DESTINO, "casos.json"), "w"), indent=2, ensure_ascii=False)
    sem_motivo = sorted({c["familia"] for c in casos if not c["xfail"]})

    # ---- 2. conformidade
    candidatos, vistos = [], set()
    for rodada in a.rodada:
        pasta_corpus = os.path.join(rodada, "corpus")
        for arq in sorted(os.listdir(pasta_corpus)):
            prog = open(os.path.join(pasta_corpus, arq), encoding="utf-8").read()
            if len(prog) <= a.max_bytes and prog not in vistos:
                vistos.add(prog)
                candidatos.append(prog)
    saidas = []
    for rodada in range(3):  # três servidores = três sementes de hash diferentes
        with Executor(REPO, timeout=5) as ex:
            saidas.append([ex.rodar(p) for p in candidatos])
    conf = []
    for i, prog in enumerate(candidatos):
        r = [s[i] for s in saidas]
        if all(x["status"] == "OK" and x.get("saida_bytes", 0) <= 400 for x in r) and len({x["saida"] for x in r}) == 1:
            h = hashlib.sha256(prog.encode()).hexdigest()[:16]
            open(os.path.join(DESTINO, "conformidade", f"{h}.guru"), "w", encoding="utf-8").write(prog)
            conf.append({"arquivo": f"conformidade/{h}.guru", "saida": r[0]["saida"]})
        if len(conf) >= a.max_conformidade:
            break
    json.dump(conf, open(os.path.join(DESTINO, "conformidade.json"), "w"), indent=2, ensure_ascii=False)

    print(json.dumps({"regressoes": len(casos), "com_xfail_documentado": sum(1 for c in casos if c["xfail"]),
                      "familias_sem_motivo_documentado": sem_motivo,
                      "conformidade": len(conf), "candidatos_conformidade": len(candidatos)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
