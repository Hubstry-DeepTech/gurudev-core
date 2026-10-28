"""Executa a politica GuruDev estatica sobre indicadores tipados.

Falha fechada: qualquer problema (indicador ausente, extra ou de tipo
errado; erro do interpretador; veredito fora da lista) resulta em
BLOQUEADO. So os tres vereditos conhecidos sao aceitos, e so depois de
uma execucao completa da politica.
"""

import threading
from pathlib import Path

from evidence_gate import VEREDITOS
from evidence_gate.verificacao import INDICADORES_BOOL, INDICADORES_INT
from src.interpreter import Interpreter
from src.parser import parse

ARQUIVO_POLITICA = Path(__file__).resolve().parent / "politica.guru"
_TRAVA = threading.Lock()  # o parser (PLY) nao e reentrante


class IndicadorInvalido(ValueError):
    pass


def validar_indicadores(ind):
    if not isinstance(ind, dict):
        raise IndicadorInvalido("indicadores devem ser um dicionario")
    esperados = set(INDICADORES_BOOL) | set(INDICADORES_INT)
    if set(ind) != esperados:
        faltam = sorted(esperados - set(ind))
        sobram = sorted(set(ind) - esperados)
        raise IndicadorInvalido(f"faltam {faltam}; sobram {sobram}")
    for nome in INDICADORES_BOOL:
        if type(ind[nome]) is not bool:
            raise IndicadorInvalido(f"{nome} deve ser bool")
    for nome in INDICADORES_INT:
        if type(ind[nome]) is not int or ind[nome] < 0:
            raise IndicadorInvalido(f"{nome} deve ser int >= 0")


def bloqueado(motivo):
    return {"veredito": "BLOQUEADO", "motivo": motivo, "politica_ok": False}


def decidir(ind, fonte_politica=None):
    """Devolve {"veredito", "motivo", "politica_ok"}."""
    try:
        validar_indicadores(ind)
    except IndicadorInvalido as e:
        return bloqueado(f"indicadores invalidos: {e}")
    try:
        codigo = fonte_politica or ARQUIVO_POLITICA.read_text("utf-8")
        with _TRAVA:
            interp = Interpreter()
            for nome, valor in ind.items():
                interp.env.decl(nome, valor)
            interp.interpretar(parse(codigo))
            veredito = interp.env.get("veredito")
            motivo = interp.env.get("motivo")
    except Exception as e:  # erro da linguagem ou do interpretador
        return bloqueado(f"falha ao executar a politica: {type(e).__name__}")
    if veredito not in VEREDITOS or not isinstance(motivo, str):
        return bloqueado("a politica produziu um veredito desconhecido")
    return {"veredito": veredito, "motivo": motivo, "politica_ok": True}
