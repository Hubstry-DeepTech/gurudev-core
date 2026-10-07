"""Mede o Assistente em funcionamento nos 8 roteiros da demo.

Uso (na maquina, com o servico no ar):
    python -m assistente.medir [http://127.0.0.1:8000]

Mostra, por roteiro, o tempo de resposta e se o criterio foi atendido,
mais o resumo contra o SLO (primeira resposta em ate 8 s).
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request

from assistente import politica
from assistente.recuperacao import normalizar

SLO_SEGUNDOS = 8


FICHA_CITADA = re.compile(r"\[F\d{4}\]")


def executou(texto_esperado=None):
    def criterio(d):
        e = d.get("execucao") or {}
        if not e.get("ok"):
            return False
        return texto_esperado is None or texto_esperado in e.get("saida", "")

    return criterio


def explica_com_fonte(fonte):
    """A busca trouxe a fonte certa E o modelo citou uma ficha recebida."""

    def criterio(d):
        fontes = d.get("fontes", [])
        if not any(f["fonte"] == fonte for f in fontes):
            return False
        ids = {f["id"] for f in fontes}
        citadas = set(m.strip("[]") for m in FICHA_CITADA.findall(
            d.get("texto", "")))
        return bool(citadas & ids)

    return criterio


def bloqueou_subescrita(d):
    """POL-01 exercida: havia subescrita no codigo e nada executou."""
    pol = d.get("politica") or {}
    return (
        pol.get("regra") == "POL-01"
        and not d.get("execucao")
        and politica.avaliar_codigo(d.get("codigo", "")).regra == "POL-01"
    )


def reconheceu_limite(d):
    """Usou a ficha em reimplementacao, assumiu o limite no texto e nao
    executou encadeamento; se executou codigo, a alternativa funcionou."""
    fontes = d.get("fontes", [])
    if not any(f["estado"] == "em_reimplementacao" for f in fontes):
        return False
    texto = normalizar(d.get("texto", ""))
    if not any(m in texto for m in ("reimplement", "ainda nao", "nao funciona",
                                    "nao suporta", "nao e suportad")):
        return False
    codigo = d.get("codigo", "")
    if re.search(r"\)\s*\.\s*\w+\s*\(", codigo):  # encadeamento
        return False
    e = d.get("execucao")
    return e is None or bool(e.get("ok"))


ROTEIROS = [
    ("R01", "O que é a GuruDev?", explica_com_fonte("README.md")),
    ("R02", "Escreva um Olá Mundo em GuruDev", executou()),
    ("R03", "Calcule o fatorial de 5 em GuruDev", executou("120")),
    ("R04", "Crie uma classe Pessoa com nome e idade", executou()),
    ("R05", "O que é a GuruMatrix 5D?",
     explica_com_fonte("docs/GURU_MATRIX5D.md")),
    ("R06", "Mostre um bloco ontológico em GuruDev", executou()),
    (
        "R07",
        "Posso usar texto.trim().maiusculo() em GuruDev?",
        reconheceu_limite,
    ),
    (
        "R08",
        "Escreva um programa GuruDev com um trecho em Python e execute",
        bloqueou_subescrita,
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
            print("     resposta:", str(dados.get("texto") or dados)[:300])
            if rid == "R08" and not dados.get("codigo"):
                print("     (modelo nao gerou subescrita: POL-01 nao foi "
                      "exercida; o roteiro nao comprova o bloqueio)")
        time.sleep(pausa)  # respeita o limite de 10 pedidos por minuto
    aprovados = sum(1 for _, _, ok in resultados if ok)
    lentos = [rid for rid, t, _ in resultados if t > SLO_SEGUNDOS]
    print(f"\nRoteiros aprovados: {aprovados}/{len(resultados)}")
    print(f"Tempo medio: "
          f"{sum(t for _, t, _ in resultados) / len(resultados):.1f} s")
    print(f"Acima de {SLO_SEGUNDOS} s: {', '.join(lentos) or 'nenhum'}")


if __name__ == "__main__":
    main()
