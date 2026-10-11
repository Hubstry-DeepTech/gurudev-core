"""Coletor do benchmark V2: roda os casos de casos.json contra o servidor do
Assistente e grava cada resposta completa, com a avaliacao automatica, num
JSONL imutavel (REGRAS.md, secao 7).

Uso, na raiz do repositorio e com o servidor no ar:
  python benchmarks/v2/coletor.py --modelo qwen3:1.7b \\
      --commit-esperado <sha-do-merge> --saida ~/v2-1.7b.jsonl

Teste rapido (nao oficial): acrescente --limite 2
"""

import argparse
import datetime
import json
import os
import platform
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avaliacao as av  # noqa: E402
from assistente.recuperacao import Buscador, carregar_base  # noqa: E402

UNIDADE = "/etc/systemd/system/assistente-gurudev.service"
TENTATIVAS = 3  # falha de ambiente (timeout, HTTP 5xx) e refeita ate 2 vezes


def obter_json(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def perguntar(url, pergunta):
    pedido = urllib.request.Request(
        url + "/api/perguntar",
        data=json.dumps({"pergunta": pergunta}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    inicio = time.monotonic()
    try:
        with urllib.request.urlopen(pedido, timeout=300) as r:
            dados = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        dados = {"erro": f"HTTP {e.code}"}
    except (urllib.error.URLError, TimeoutError) as e:
        dados = {"erro": f"sem resposta: {e}"}
    return round(time.monotonic() - inicio, 2), dados


def commit_atual():
    r = subprocess.run(
        ["git", "-c", f"safe.directory={av.RAIZ}", "-C", str(av.RAIZ),
         "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return r.stdout.strip()


def digest_carregado(ollama, modelo):
    for m in obter_json(ollama + "/api/ps").get("models", []):
        if modelo in (m.get("name"), m.get("model")):
            return m.get("digest", "")
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--modelo", required=True)
    p.add_argument("--saida", required=True)
    p.add_argument("--commit-esperado", required=True)
    p.add_argument("--url", default="http://127.0.0.1:8000")
    p.add_argument("--ollama", default="http://127.0.0.1:11434")
    p.add_argument("--pausa", type=float, default=7)
    p.add_argument("--limite", type=int, default=0,
                   help="so os N primeiros casos, 1 repeticao (nao oficial)")
    p.add_argument("--sem-verificar-ollama", action="store_true",
                   help="para modelos de nuvem, que o /api/ps pode nao listar")
    a = p.parse_args()

    commit = commit_atual()
    if not commit.startswith(a.commit_esperado):
        sys.exit(f"ABORTADO: repositorio em {commit[:12]}, "
                 f"esperado {a.commit_esperado}")
    if os.path.exists(UNIDADE):
        if f"GURU_MODELO_NOME={a.modelo}\n" not in Path(UNIDADE).read_text():
            sys.exit(f"ABORTADO: o servico nao esta configurado com {a.modelo}")

    casos = av.carregar_casos()
    oficial = a.limite == 0
    if not oficial:
        casos = casos[: a.limite]
    buscador = Buscador(carregar_base())
    try:
        versao_ollama = obter_json(a.ollama + "/api/version").get("version")
    except OSError:
        versao_ollama = None
    ambiente = {
        "host": platform.node(),
        "sistema": platform.platform(),
        "python": platform.python_version(),
        "cpus": os.cpu_count(),
        "ollama_versao": versao_ollama,
        "url": a.url,
    }

    digest = None
    with open(a.saida, "x", encoding="utf-8") as arq:  # nunca sobrescreve
        for c in casos:
            reps = av.REPETICOES[c["critico"]] if oficial else 1
            for rep in range(1, reps + 1):
                for tentativa in range(1, TENTATIVAS + 1):
                    inicio = datetime.datetime.now(datetime.timezone.utc)
                    duracao, dados = perguntar(a.url, c["pergunta"])
                    if "erro" not in dados or tentativa == TENTATIVAS:
                        break
                    # falha de ambiente: fica registrada e a execucao e refeita
                    arq.write(json.dumps({
                        "run_id": f"{inicio:%Y%m%dT%H%M%S}-{c['id']}-r{rep}"
                                  f"-t{tentativa}",
                        "descartado": True, "caso": c["id"], "repeticao": rep,
                        "modelo": a.modelo, "repo_commit": commit,
                        "duracao_s": duracao, "resposta": dados,
                    }, ensure_ascii=False) + "\n")
                    print(f"{c['id']:7} r{rep} falha de ambiente "
                          f"({dados['erro']}); repetindo")
                    time.sleep(a.pausa)
                if digest is None and not a.sem_verificar_ollama:
                    digest = digest_carregado(a.ollama, a.modelo)
                    if digest is None:
                        arq.close()
                        os.remove(a.saida)
                        sys.exit(f"ABORTADO: Ollama sem {a.modelo} carregado")
                aval = av.avaliar(c, dados)
                registro = {
                    "run_id": f"{inicio:%Y%m%dT%H%M%S}-{c['id']}-r{rep}",
                    "timestamp": inicio.isoformat(),
                    "oficial": oficial,
                    "versao_casos": "v2-piloto",
                    "modelo": a.modelo,
                    "modelo_digest": digest,
                    "repo_commit": commit,
                    "caso": c["id"],
                    "dimensao": c["dimensao"],
                    "critico": c["critico"],
                    "repeticao": rep,
                    "pergunta": c["pergunta"],
                    "duracao_s": duracao,
                    "resposta": dados,
                    "avaliacao": aval,
                    "telemetria_busca": av.telemetria_busca(
                        buscador, c["pergunta"]),
                    "ambiente": ambiente,
                }
                arq.write(json.dumps(registro, ensure_ascii=False) + "\n")
                arq.flush()
                print(f"{c['id']:7} r{rep} {duracao:6.1f} s  "
                      f"{'OK ' if aval['passou'] else 'FALHOU'}  "
                      f"{aval['classe']}")
                time.sleep(a.pausa)

    os.chmod(a.saida, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    print(f"\nEvidencia gravada (somente leitura): {a.saida}")
    print(f"Analise: python benchmarks/v2/analisar.py {a.saida}")


if __name__ == "__main__":
    main()
