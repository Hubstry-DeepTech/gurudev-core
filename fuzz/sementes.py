"""
fuzz/sementes.py — Coleta programas GuruDev reais para servir de sementes.

Fontes:
  1. examples/*.guru
  2. textos literais dentro de tests/*.py, assistente/ e benchmarks/ que o parser
     aceita sem erro sintático (são programas que a própria suíte usa)

Também extrai, lexando as sementes, o vocabulário observado: para cada tipo de
token, os lexemas que de fato aparecem. O gerador pela gramática usa isso para
transformar sequências de tokens em texto.

Uso:
  python3 fuzz/sementes.py --saida resultados/sementes
"""

import argparse
import ast
import contextlib
import glob
import hashlib
import io
import json
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)


def _literais_de_python(caminho):
    try:
        arvore = ast.parse(open(caminho, encoding="utf-8").read())
    except (SyntaxError, UnicodeDecodeError):
        return []
    out = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Constant) and isinstance(no.value, str) and len(no.value) >= 15:
            out.append(no.value)
    return out


def coletar(repo=REPO):
    sys.path.insert(0, repo)
    from src import parser as mod_parser
    from src.lexer import build_lexer

    with contextlib.redirect_stdout(io.StringIO()):
        parser = mod_parser.build_parser(debug=False)

    candidatos = []
    for arq in sorted(glob.glob(os.path.join(repo, "examples", "*.guru"))):
        candidatos.append((os.path.relpath(arq, repo), open(arq, encoding="utf-8").read()))
    for pasta in ("tests", "assistente", "benchmarks"):
        for arq in sorted(glob.glob(os.path.join(repo, pasta, "**", "*.py"), recursive=True)):
            for i, txt in enumerate(_literais_de_python(arq)):
                candidatos.append((f"{os.path.relpath(arq, repo)}#{i}", txt))

    sementes, vistos = [], set()
    vocab = defaultdict(set)
    for origem, txt in candidatos:
        h = hashlib.sha256(txt.encode()).hexdigest()
        if h in vistos:
            continue
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                lexer = build_lexer()
                arvore = parser.parse(txt, lexer=lexer)
        except Exception:  # noqa: BLE001 — candidato inválido ou que derruba o parser
            continue
        if arvore is None or "Erro sint" in buf.getvalue() or "Caractere ilegal" in buf.getvalue():
            continue
        # precisa ter ao menos um token além de texto solto
        # Guarda o TEXTO-FONTE de cada token (fatia do programa), não t.value:
        # várias regras do lexer transformam o valor (tiram aspas, extraem atributos).
        try:
            toks = []
            with contextlib.redirect_stdout(io.StringIO()):
                lx = build_lexer()
                lx.input(txt)
                while True:
                    t = lx.token()
                    if t is None:
                        break
                    toks.append((t.type, txt[t.lexpos:lx.lexpos]))
        except Exception:  # noqa: BLE001
            continue
        if len(toks) < 3:
            continue
        vistos.add(h)
        sementes.append({"origem": origem, "sha256": h, "codigo": txt, "n_tokens": len(toks)})
        for tipo, fonte in toks:
            if fonte and len(fonte) <= 300:
                vocab[tipo].add(fonte)
    vocab = {k: sorted(v)[:40] for k, v in sorted(vocab.items())}
    return sementes, vocab


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", default="resultados/sementes")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    sementes, vocab = coletar()
    for s in sementes:
        with open(os.path.join(a.saida, s["sha256"][:16] + ".guru"), "w", encoding="utf-8") as f:
            f.write(s["codigo"])
    json.dump([{k: v for k, v in s.items() if k != "codigo"} for s in sementes],
              open(os.path.join(a.saida, "indice.json"), "w"), indent=2, ensure_ascii=False)
    json.dump(vocab, open(os.path.join(a.saida, "vocabulario.json"), "w"), indent=2, ensure_ascii=False)
    print(f"{len(sementes)} sementes válidas; {len(vocab)} tipos de token com lexemas observados")


if __name__ == "__main__":
    main()
