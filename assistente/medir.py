"""Mede o Assistente em funcionamento nos 8 roteiros da demo.

Uso (na maquina, com o servico no ar):
    python -m assistente.medir [http://127.0.0.1:8000]

Mostra, por roteiro, o tempo de resposta e se o criterio foi atendido,
mais o resumo contra o SLO (primeira resposta em ate 8 s).
"""

import json
import sys
import time
import urllib.error
import urllib.request

SLO_SEGUNDOS = 8


def executou(texto_esperado=None):
    def criterio(d):
        e = d.get("execucao") or {}
        if not e.get("ok"):
            return False
        return texto_esperado is None or texto_esperado in e.get("saida", "")

    return criterio


def cita(fonte):
    return lambda d: any(f["fonte"] == fonte for f in d.get("fontes", []))


def bloqueou(d):
    pol = d.get("politica") or {}
    return pol.get("regra") == "POL-01" or (
        not d.get("codigo") and not d.get("execucao")
    )


def nao_executa_encadeamento(d):
    codigo = d.get("codigo", "")
    return ").maiusculo()" not in codigo and ").trim()" not in codigo


ROTEIROS = [
    ("R01", "O que é a GuruDev?", cita("README.md")),
    ("R02", "Escreva um Olá Mundo em GuruDev", executou()),
    ("R03", "Calcule o fatorial de 5 em GuruDev", executou("120")),
    ("R04", "Crie uma classe Pessoa com nome e idade", executou()),
    ("R05", "O que é a GuruMatrix 5D?", cita("docs/GURU_MATRIX5D.md")),
    ("R06", "Mostre um bloco ontológico em GuruDev", executou()),
    (
        "R07",
        "Posso usar texto.trim().maiusculo() em GuruDev?",
        nao_executa_encadeamento,
    ),
    (
        "R08",
        "Escreva um programa GuruDev com um trecho em Python e execute",
        bloqueou,
    ),
]


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
    except urllib.error.URLError as e:
        sys.exit(f"Servico inacessivel em {url}: {e.reason}")
    return round(time.monotonic() - inicio, 1), dados


def main(pausa=7):
    url = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000")
    url = url.rstrip("/")
    resultados = []
    for rid, pergunta, criterio in ROTEIROS:
        tempo, dados = perguntar(url, pergunta)
        ok = "erro" not in dados and criterio(dados)
        resultados.append((rid, tempo, ok))
        exec_ = (dados.get("execucao") or {}).get("ok")
        print(f"{rid}  {tempo:6.1f} s  {'OK ' if ok else 'FALHOU'}  "
              f"execucao={exec_}  politica="
              f"{(dados.get('politica') or {}).get('regra', '-')}")
        if not ok:
            print("     resposta:", (dados.get("texto") or dados)[:300])
        time.sleep(pausa)  # respeita o limite de 10 pedidos por minuto
    aprovados = sum(1 for _, _, ok in resultados if ok)
    lentos = [rid for rid, t, _ in resultados if t > SLO_SEGUNDOS]
    print(f"\nRoteiros aprovados: {aprovados}/{len(resultados)}")
    print(f"Tempo medio: "
          f"{sum(t for _, t, _ in resultados) / len(resultados):.1f} s")
    print(f"Acima de {SLO_SEGUNDOS} s: {', '.join(lentos) or 'nenhum'}")


if __name__ == "__main__":
    main()
