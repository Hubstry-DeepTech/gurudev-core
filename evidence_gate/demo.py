"""Demonstracao com 3 casos: um de cada veredito.

    python3 -m evidence_gate.demo --simulado   # sem rede, respostas fixas
    python3 -m evidence_gate.demo              # modelo real (GURU_MODELO_*)

Com o modelo real, o veredito depende do que o modelo devolver (ele pode,
por exemplo, citar literalmente onde o simulado parafraseia); o modo real
nao compara com o esperado e mostra as afirmacoes para conferencia.
"""

import argparse
import json
import sys

from assistente.modelo import ModeloSimulado
from evidence_gate.portao import Portao

FONTE = (
    "A Lei 14.133, de 1 de abril de 2021, estabelece normas gerais de "
    "licitacao e contratacao para as Administracoes Publicas diretas, "
    "autarquicas e fundacionais da Uniao, dos Estados, do Distrito Federal "
    "e dos Municipios. O agente de contratacao e a pessoa designada pela "
    "autoridade competente para tomar decisoes e acompanhar o tramite da "
    "licitacao."
)

CASOS = [
    ("Quem e o agente de contratacao?", "VALIDADO_LITERAL"),
    ("A lei vale para os Municipios?", "REVISAO_SEMANTICA"),
    ("Qual e a multa por atraso na entrega?", "BLOQUEADO"),
]

_RESPOSTAS = {
    CASOS[0][0]: {
        "answer": "a pessoa designada pela autoridade competente",
        "claims": [{
            "text": "O agente de contratacao e a pessoa designada pela "
                    "autoridade competente para tomar decisoes e acompanhar "
                    "o tramite da licitacao.",
            "evidence_quote": "O agente de contratacao e a pessoa designada "
                              "pela autoridade competente para tomar "
                              "decisoes e acompanhar o tramite da licitacao.",
        }],
    },
    CASOS[1][0]: {
        "answer": "Sim.",
        "claims": [{
            "text": "A lei se aplica aos Municipios.",
            "evidence_quote": "dos Estados, do Distrito Federal e dos "
                              "Municipios",
        }],
    },
    CASOS[2][0]: {
        "answer": "A multa e de 10% do valor do contrato.",
        "claims": [{
            "text": "A multa por atraso e de 10% do valor do contrato.",
            "evidence_quote": "multa de 10% do valor do contrato",
        }],
    },
}


def modelo_simulado():
    def responder(mensagens):
        pergunta = mensagens[-1]["content"].rsplit("PERGUNTA: ", 1)[-1]
        r = _RESPOSTAS.get(pergunta.strip())
        if r is None:
            return '{"answer": "sem resposta simulada", "claims": []}'
        return json.dumps(r, ensure_ascii=False)
    return ModeloSimulado(responder)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--simulado", action="store_true")
    args = p.parse_args(argv)
    if args.simulado:
        modelo = modelo_simulado()
    else:
        from evidence_gate.servidor import criar_modelo
        modelo = criar_modelo()
    portao = Portao(modelo)
    divergencias = 0
    for pergunta, esperado in CASOS:
        r = portao.avaliar(FONTE, pergunta)
        marca = ("" if not args.simulado or r["veredito"] == esperado
                 else f"  (esperado: {esperado})")
        divergencias += bool(marca)
        print(f"- {pergunta}\n  {r['veredito']}: {r['motivo']} "
              f"[{r['duracao_total']} s]{marca}")
        if not args.simulado:
            for a in r["afirmacoes"]:
                print(f"    afirmacao: {a['texto']!r}\n"
                      f"    citacao:   {a['citacao']!r} "
                      f"(encontrada={a['citacao_encontrada']}, "
                      f"literal={a['literal']})")
    return 1 if (args.simulado and divergencias) else 0


if __name__ == "__main__":
    sys.exit(main())
