"""Politica de seguranca do Assistente (docs/DEMO_ROTEIROS.md).

POL-01: programa com subescrita nao e executado.
POL-02: a decisao e tomada por regra deterministica neste modulo,
        nunca pelo modelo.
POL-03: limites de tamanho de entrada, de codigo, de saida e de tempo.

A restricao pertence ao Assistente da demo publica. O runtime da
GuruDev continua aceitando subescritas.
"""

import re
from dataclasses import dataclass

MAX_PERGUNTA = 500  # caracteres
MAX_CODIGO = 5000  # caracteres
MAX_SAIDA = 10000  # caracteres
TEMPO_LIMITE = 5  # segundos

PADROES_SUBESCRITA = [
    re.compile(r"¿\s*[A-Za-z_+#]+\s*\?"),  # ¿python? ... ?/python?
    re.compile(r"\?\s*/\s*[A-Za-z_+#]+\s*\?"),
    re.compile(r"\[\s*/?\s*subescritas?\s*\]", re.I),
    re.compile(r"\$\$\s*/?\s*subescritas?\s*\$\$", re.I),
]


@dataclass
class Decisao:
    permitido: bool
    regra: str = ""
    motivo: str = ""


def avaliar_pergunta(pergunta):
    if not pergunta or not pergunta.strip():
        return Decisao(False, "POL-03", "pergunta vazia")
    if len(pergunta) > MAX_PERGUNTA:
        return Decisao(
            False, "POL-03", f"pergunta acima de {MAX_PERGUNTA} caracteres"
        )
    return Decisao(True)


def avaliar_codigo(codigo):
    if len(codigo) > MAX_CODIGO:
        return Decisao(
            False, "POL-03", f"codigo acima de {MAX_CODIGO} caracteres"
        )
    for padrao in PADROES_SUBESCRITA:
        if padrao.search(codigo):
            return Decisao(
                False,
                "POL-01",
                "o codigo contem subescrita (codigo de outra linguagem); "
                "a execucao de subescritas esta bloqueada na demo publica",
            )
    return Decisao(True)
