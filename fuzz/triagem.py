"""
fuzz/triagem.py — Reproduz, minimiza e classifica as falhas encontradas pelo fuzzer.

Para cada pasta em <rodada>/falhas/:
  1. reproduz o programa salvo 3 vezes no executor isolado (estável ou instável);
  2. minimiza por delta debugging (ddmin) em nível de token, mantendo a mesma
     assinatura (status + exceção + local);
  3. agrupa as assinaturas em FAMÍLIAS: mesmo status, mesma exceção, mesma função.
     Várias linhas da mesma função (ex.: cada operador em _x_OperacaoBinaria)
     costumam ser uma única causa raiz; a família é a unidade de análise.

Grava em <saida>/:
  casos/<familia>__<n>.guru   caso mínimo de cada assinatura (programa reprodutor)
  triagem.json                tudo: assinaturas, família, estabilidade, tamanhos, mensagens
  triagem.md                  relatório legível por família

Não decide sozinho se algo é bug "esperado". A classificação automática é
preliminar; a causa e a justificativa de cada família são escritas por uma
pessoa em fuzz/analise-falhas.md antes de qualquer teste virar xfail.

Uso:
  python3 fuzz/triagem.py --rodada resultados/piloto --saida resultados/triagem
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from executor import Executor, assinatura  # noqa: E402

TOKEN_RX = re.compile(r'"(?:[^"\\\n]|\\.)*"|\d+\.\d+|\d+|[A-Za-z_À-ÿ][\wÀ-ÿ]*|\s+|[^\w\s]')

CLASSE_PRELIMINAR = {
    "CRASH_INTERP": "exceção Python vaza do interpretador (deveria ser GuruDevError)",
    "CRASH_PARSER": "exceção Python vaza do parser (deveria ser erro sintático)",
    "CRASH_LEXER": "exceção Python vaza do lexer (deveria ser erro léxico)",
    "RECURSAO": "RecursionError do Python vaza (a linguagem não limita recursão)",
    "TIMEOUT": "travamento: precisa investigar a causa",
    "MEMORIA": "consumo de memória sem limite",
    "MORTO": "processo morreu (sinal)",
}


def _linha_do_repo(local):
    """Texto da linha de src/ indicada em 'arquivo:linha funcao' (para reconhecer a chamada de uma nativa)."""
    import linecache
    try:
        arq, resto = local.split(":", 1)
        return linecache.getline(os.path.join(REPO, arq), int(resto.split(" ")[0])).strip()
    except (ValueError, IndexError):
        return ""


def familia_de(assin, res):
    partes = assin.split("|")
    status = partes[0]
    local = res.get("local") or ""
    # Biblioteca padrão: a falha nasce em src/nativas.py ou na linha que chama a nativa.
    # A causa comum é a ausência de validação de argumentos nas nativas: uma família.
    if status == "CRASH_INTERP" and (local.startswith("src/nativas.py") or "nativa(" in _linha_do_repo(local)):
        return "CRASH_INTERP|Nativas"
    if status == "TIMEOUT":
        local = res.get("local", "?")
        return "TIMEOUT|" + (local.split(" ")[-1] if " " in local else local)
    exc = partes[1] if len(partes) > 1 else ""
    funcao = (res.get("local") or "? ?").split(" ")[-1]
    # sinais de controle (Return/Break/Continue) vazando são uma família só
    if exc.endswith("Signal"):
        return f"{status}|SinalDeControle"
    return f"{status}|{exc}|{funcao}"


def ddmin(tokens, ainda_falha, max_testes=400):
    """Delta debugging clássico (Zeller): menor subsequência que ainda falha."""
    n, testes = 2, 0
    while len(tokens) >= 2 and testes < max_testes:
        tam = max(1, len(tokens) // n)
        reduziu = False
        for i in range(0, len(tokens), tam):
            complemento = tokens[:i] + tokens[i + tam:]
            testes += 1
            if complemento and ainda_falha(complemento):
                tokens, n, reduziu = complemento, max(n - 1, 2), True
                break
            if testes >= max_testes:
                break
        if not reduziu:
            if n >= len(tokens):
                break
            n = min(len(tokens), n * 2)
    return tokens, testes


def limpar_espacos(prog):
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", prog)).strip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rodada", required=True, nargs="+", help="uma ou mais rodadas; assinaturas repetidas ficam com o menor programa")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--timeout", type=float, default=3.0)
    ap.add_argument("--max-testes", type=int, default=400)
    a = ap.parse_args()
    os.makedirs(os.path.join(a.saida, "casos"), exist_ok=True)

    # junta as rodadas: por assinatura, fica o menor programa e soma as ocorrências
    entradas = {}
    for rodada in a.rodada:
        pasta_falhas = os.path.join(rodada, "falhas")
        for p in sorted(os.listdir(pasta_falhas)):
            base = os.path.join(pasta_falhas, p)
            if not os.path.exists(os.path.join(base, "programa.guru")):
                continue
            meta = json.load(open(os.path.join(base, "resultado.json"), encoding="utf-8"))
            prog = open(os.path.join(base, "programa.guru"), encoding="utf-8").read()
            atual = entradas.get(meta["assinatura"])
            if atual is None:
                entradas[meta["assinatura"]] = (meta, prog)
            else:
                meta_a, prog_a = atual
                meta_a["ocorrencias"] = (meta_a.get("ocorrencias") or 0) + (meta.get("ocorrencias") or 0)
                if len(prog) < len(prog_a):
                    entradas[meta["assinatura"]] = (meta_a, prog)
    itens = []
    with Executor(REPO, timeout=a.timeout) as ex:
        for assin, (meta, prog) in sorted(entradas.items()):

            reps = [assinatura(ex.rodar(prog)) for _ in range(3)]
            estavel = all(r == assin for r in reps)
            item = {"assinatura": assin, "ocorrencias": meta.get("ocorrencias"), "origem": meta.get("origem"),
                    "reproduz": reps.count(assin), "estavel": estavel, "tamanho_original": len(prog)}
            if all(r == "TIMEOUT|laco-do-programa" for r in reps):
                item.update(familia="ESPERADO|laco-do-programa", classe="laço infinito do próprio programa (esperado)",
                            minimo=prog, reclassificado_de=assin, estavel=True)
                itens.append(item)
                print(f"reclassificado como laço do programa: {assin}", flush=True)
                continue
            if reps.count(assin) == 0:
                item.update(familia="NAO-REPRODUZ", classe="não reproduziu fora da rodada", minimo=prog)
                itens.append(item)
                print(f"não reproduz: {assin}", flush=True)
                continue

            def ainda_falha(toks):
                return assinatura(ex.rodar("".join(toks))) == assin

            # 1º por linhas (rápido em programas grandes), 2º por tokens (fino)
            linhas, t1 = ddmin(prog.splitlines(keepends=True), ainda_falha, a.max_testes)
            toks, t2 = ddmin(TOKEN_RX.findall("".join(linhas)), ainda_falha, a.max_testes)
            testes = t1 + t2
            minimo = "".join(toks)
            limpo = limpar_espacos(minimo)
            if limpo != minimo and len(limpo) <= len(minimo) + 1 and assinatura(ex.rodar(limpo)) == assin:
                minimo = limpo
            res = ex.rodar(minimo)
            item.update(
                familia=familia_de(assin, res), classe=CLASSE_PRELIMINAR.get(assin.split("|")[0], "?"),
                minimo=minimo, tamanho_minimo=len(minimo), testes_minimizacao=testes,
                exc=res.get("exc"), msg=res.get("msg"), local=res.get("local"), pilha=res.get("pilha"),
            )
            itens.append(item)
            print(f"{assin}: {len(prog)} -> {len(minimo)} bytes ({testes} testes), estável={estavel}", flush=True)

    familias = defaultdict(list)
    for it in itens:
        familias[it["familia"]].append(it)
    for fam, lista in familias.items():
        nome = re.sub(r"[^\w]+", "_", fam).strip("_")[:70]
        for i, it in enumerate(sorted(lista, key=lambda x: x.get("tamanho_minimo", 1e9))):
            caminho = os.path.join(a.saida, "casos", f"{nome}__{i + 1}.guru")
            open(caminho, "w", encoding="utf-8").write(it["minimo"])
            it["caso"] = os.path.relpath(caminho, a.saida)

    json.dump({"rodadas": [os.path.abspath(r) for r in a.rodada], "assinaturas": len(itens), "familias": len(familias),
               "itens": itens}, open(os.path.join(a.saida, "triagem.json"), "w"), indent=2, ensure_ascii=False)

    linhas = ["# Triagem das falhas", "",
              f"Rodadas: {', '.join('`' + os.path.basename(os.path.normpath(r)) + '`' for r in a.rodada)}. Assinaturas: {len(itens)}. Famílias (causa provável comum): {len(familias)}.", "",
              "| Família | Assinaturas | Ocorrências | Estável | Classe preliminar |", "|---|---|---|---|---|"]
    for fam, lista in sorted(familias.items(), key=lambda kv: -sum(x.get("ocorrencias") or 0 for x in kv[1])):
        linhas.append(f"| `{fam}` | {len(lista)} | {sum(x.get('ocorrencias') or 0 for x in lista)} | "
                      f"{'sim' if all(x['estavel'] for x in lista) else 'NÃO'} | {lista[0]['classe']} |")
    for fam, lista in sorted(familias.items()):
        linhas += ["", f"## `{fam}`", ""]
        for it in sorted(lista, key=lambda x: x.get("tamanho_minimo", 1e9)):
            linhas += [f"- assinatura `{it['assinatura']}` — {it.get('ocorrencias')} ocorrências, "
                       f"{it['tamanho_original']} → {it.get('tamanho_minimo')} bytes, caso `{it.get('caso')}`",
                       f"  - mensagem: `{(it.get('msg') or '')[:160]}`",
                       "", "```", it["minimo"].strip()[:600], "```"]
    open(os.path.join(a.saida, "triagem.md"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print(f"{len(itens)} assinaturas em {len(familias)} famílias. Relatório: {os.path.join(a.saida, 'triagem.md')}")


if __name__ == "__main__":
    main()
