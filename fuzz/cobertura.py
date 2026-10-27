"""
fuzz/cobertura.py — Cobertura de src/ (coverage.py, linhas e ramos) alcançada pelo corpus.

Reexecuta o corpus de uma rodada sob coverage.py, em lotes isolados e paralelos,
e compara com a cobertura da suíte registrada no baseline. A métrica é a mesma
do baseline (coverage.py), então os números são comparáveis.

Grava em <saida>/:
  cobertura-corpus.json         só o corpus
  cobertura-uniao.json          suíte + corpus
  cobertura-uniao/              relatório HTML da união
  comparacao.json               suíte vs corpus vs união, por arquivo

Uso:
  python3 fuzz/cobertura.py --rodada resultados/piloto --baseline resultados/baseline --saida resultados/cobertura
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)

LOTE = r'''
import contextlib, io, os, resource, signal, sys, tempfile
sys.path.insert(0, {repo!r}); sys.path.insert(0, {aqui!r})
resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
resource.setrlimit(resource.RLIMIT_FSIZE, (1 << 20, 1 << 20))
from executor import _builtins_restritos, TempoEsgotado
from src import parser as P, interpreter as I
from src.lexer import build_lexer
with contextlib.redirect_stdout(io.StringIO()):
    parser = P.build_parser(debug=False)
I.builtins = _builtins_restritos()
os.chdir(tempfile.mkdtemp())
sys.stdin = io.StringIO("entrada\n" * 64)
def alarme(s, f): raise TempoEsgotado()
signal.signal(signal.SIGALRM, alarme)
sys.setrecursionlimit(3000)
for arq in sys.argv[1:]:
    src = open(arq, encoding="utf-8").read()
    signal.setitimer(signal.ITIMER_REAL, {timeout})
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            ast = parser.parse(src, lexer=build_lexer())
            if ast is not None:
                I.Interpreter().interpretar(ast)
    except BaseException:
        pass
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
'''


def cov(*args, **kw):
    return subprocess.run([sys.executable, "-m", "coverage", *args], cwd=REPO, capture_output=True, text=True, **kw)


def resumo(caminho_json):
    d = json.load(open(caminho_json))
    t = d["totals"]
    return {
        "pct": round(t["percent_covered"], 1),
        "linhas": f'{t["covered_lines"]}/{t["num_statements"]}',
        "ramos": f'{t.get("covered_branches", 0)}/{t.get("num_branches", 0)}',
        "por_arquivo": {k: round(v["summary"]["percent_covered"], 1) for k, v in d["files"].items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rodada", required=True)
    ap.add_argument("--baseline", required=True, help="pasta do baseline (com .coverage da suíte)")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--processos", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--lote", type=int, default=40)
    ap.add_argument("--timeout", type=float, default=3.0)
    a = ap.parse_args()
    saida = os.path.abspath(a.saida)
    os.makedirs(saida, exist_ok=True)
    trabalho = tempfile.mkdtemp(prefix="guru-cov-")
    script = os.path.join(trabalho, "lote.py")
    open(script, "w").write(LOTE.format(repo=REPO, aqui=AQUI, timeout=a.timeout))

    arquivos = sorted(glob.glob(os.path.join(os.path.abspath(a.rodada), "corpus", "*.guru")))
    lotes = [arquivos[i:i + a.lote] for i in range(0, len(arquivos), a.lote)]
    falhos = []

    def rodar(i_lote):
        i, lote = i_lote
        dados = os.path.join(trabalho, f".coverage.corpus.{i}")
        try:
            subprocess.run([sys.executable, "-m", "coverage", "run", "--branch", "--source=src",
                            "--omit=src/parsetab.py", f"--data-file={dados}", script, *lote],
                           cwd=REPO, capture_output=True, timeout=a.timeout * len(lote) + 60)
        except subprocess.TimeoutExpired:
            falhos.append(i)

    print(f"Reexecutando {len(arquivos)} programas do corpus em {len(lotes)} lotes...", flush=True)
    with ThreadPoolExecutor(a.processos) as pool:
        list(pool.map(rodar, enumerate(lotes)))

    corpus_dados = os.path.join(trabalho, ".coverage.corpus")
    partes = glob.glob(os.path.join(trabalho, ".coverage.corpus.*"))
    cov("combine", f"--data-file={corpus_dados}", "--keep", *partes)
    cov("json", f"--data-file={corpus_dados}", "-o", os.path.join(saida, "cobertura-corpus.json"))

    uniao = os.path.join(trabalho, ".coverage.uniao")
    base_dados = os.path.join(os.path.abspath(a.baseline), ".coverage")
    copia_base = os.path.join(trabalho, ".coverage.base")
    shutil.copy(base_dados, copia_base)
    cov("combine", f"--data-file={uniao}", "--keep", corpus_dados, copia_base)
    cov("json", f"--data-file={uniao}", "-o", os.path.join(saida, "cobertura-uniao.json"))
    cov("html", f"--data-file={uniao}", "-d", os.path.join(saida, "cobertura-uniao"))

    comp = {
        "programas_no_corpus": len(arquivos),
        "lotes_estourados": falhos,
        "suite": resumo(os.path.join(os.path.abspath(a.baseline), "cobertura-suite.json")),
        "corpus": resumo(os.path.join(saida, "cobertura-corpus.json")),
        "uniao": resumo(os.path.join(saida, "cobertura-uniao.json")),
    }
    json.dump(comp, open(os.path.join(saida, "comparacao.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps({k: (v if k in ("programas_no_corpus", "lotes_estourados") else {x: v[x] for x in ("pct", "linhas", "ramos")})
                      for k, v in comp.items()}, indent=2, ensure_ascii=False))
    shutil.rmtree(trabalho, ignore_errors=True)


if __name__ == "__main__":
    main()
