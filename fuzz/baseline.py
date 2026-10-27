"""
fuzz/baseline.py — Registra a linha de base reproduzível antes de qualquer fuzzing.

Grava em <saida>/:
  ambiente.json        commit, branch, versões (Python, PLY, pytest, coverage), SO,
                       hash SHA-256 de cada arquivo em src/
  pytest.log           saída completa da suíte
  pytest-junit.xml     resultado teste a teste
  cobertura-suite.json cobertura de linhas e ramos de src/ pela suíte (coverage.py)
  cobertura-suite/     relatório HTML da mesma cobertura
  exemplos.json        resultado de cada examples/*.guru no executor isolado
  nos-sem-execucao.json classes da AST sem método _x_ no interpretador
                       (o interpretador ignora esses nós em silêncio)
  baseline.json        resumo de tudo acima

Uso:
  python3 fuzz/baseline.py --saida resultados/baseline
"""

import argparse
import glob
import hashlib
import inspect
import json
import os
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from executor import Executor  # noqa: E402


def sh(*cmd, **kw):
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, **kw)


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", default="resultados/baseline")
    a = ap.parse_args()
    saida = os.path.abspath(a.saida)
    os.makedirs(saida, exist_ok=True)

    import ply
    import pytest
    import coverage

    arquivos_src = sorted(glob.glob(os.path.join(REPO, "src", "**", "*.py"), recursive=True))
    ambiente = {
        "registrado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit": sh("git", "rev-parse", "HEAD").stdout.strip(),
        "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD").stdout.strip(),
        "arvore_limpa_em_src": sh("git", "status", "--porcelain", "--", "src").stdout.strip() == "",
        "python": sys.version.split()[0],
        "ply": ply.__version__,
        "pytest": pytest.__version__,
        "coverage": coverage.__version__,
        "sistema": platform.platform(),
        "nucleos": os.cpu_count(),
        "sha256_src": {os.path.relpath(p, REPO): sha256(p) for p in arquivos_src if "parsetab" not in p},
    }
    json.dump(ambiente, open(os.path.join(saida, "ambiente.json"), "w"), indent=2, ensure_ascii=False)

    # 1) Suíte com cobertura de linhas e ramos de src/
    print("Rodando a suíte com cobertura...", flush=True)
    dados_cov = os.path.join(saida, ".coverage")
    r = sh(sys.executable, "-m", "coverage", "run", "--branch", "--source=src", "--omit=src/parsetab.py", f"--data-file={dados_cov}",
           "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rxXs",
           f"--junitxml={os.path.join(saida, 'pytest-junit.xml')}")
    open(os.path.join(saida, "pytest.log"), "w").write(r.stdout + r.stderr)
    resumo_linha = (re.findall(r"^=*\s*(\d+ passed.*?)\s*=*$", r.stdout, re.M) or ["?"])[-1]
    sh(sys.executable, "-m", "coverage", "json", f"--data-file={dados_cov}", "-o", os.path.join(saida, "cobertura-suite.json"))
    sh(sys.executable, "-m", "coverage", "html", f"--data-file={dados_cov}", "-d", os.path.join(saida, "cobertura-suite"))
    cov = json.load(open(os.path.join(saida, "cobertura-suite.json")))
    por_arquivo = {k: round(v["summary"]["percent_covered"], 1) for k, v in cov["files"].items()}

    # 2) Exemplos no executor isolado
    print("Rodando os exemplos no executor isolado...", flush=True)
    exemplos = {}
    with Executor(REPO, timeout=10) as ex:
        for arq in sorted(glob.glob(os.path.join(REPO, "examples", "*.guru"))):
            res = ex.rodar(open(arq, encoding="utf-8").read())
            exemplos[os.path.relpath(arq, REPO)] = {k: res.get(k) for k in ("status", "exc", "msg", "local", "tempo")}
    json.dump(exemplos, open(os.path.join(saida, "exemplos.json"), "w"), indent=2, ensure_ascii=False)

    # 3) Nós da AST que o interpretador ignora em silêncio (sem _x_<Classe>)
    sys.path.insert(0, REPO)
    from src import ast_nodes, interpreter
    classes = [n for n, c in inspect.getmembers(ast_nodes, inspect.isclass) if c.__module__ == ast_nodes.__name__]
    sem = sorted(n for n in classes if not hasattr(interpreter.Interpreter, "_x_" + n))
    json.dump({"classes_ast": len(classes), "sem_execucao": sem}, open(os.path.join(saida, "nos-sem-execucao.json"), "w"),
              indent=2, ensure_ascii=False)

    resumo = {
        "commit": ambiente["commit"],
        "suite": resumo_linha,
        "suite_codigo_saida": r.returncode,
        "cobertura_total_pct": round(cov["totals"]["percent_covered"], 1),
        "cobertura_linhas": f'{cov["totals"]["covered_lines"]}/{cov["totals"]["num_statements"]}',
        "cobertura_ramos": f'{cov["totals"].get("covered_branches", 0)}/{cov["totals"].get("num_branches", 0)}',
        "cobertura_por_arquivo_pct": por_arquivo,
        "exemplos": {k: v["status"] for k, v in exemplos.items()},
        "nos_ast_sem_execucao": sem,
    }
    json.dump(resumo, open(os.path.join(saida, "baseline.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(resumo, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
