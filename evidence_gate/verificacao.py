"""Verificacoes deterministicas da saida do modelo.

Normalizacao (a unica aplicada, nos dois lados da comparacao):
  1. Unicode NFC;
  2. qualquer sequencia de espacos em branco (espaco, tabulacao, quebra
     de linha) vira um espaco; espacos nas pontas sao removidos.
Nao ha casamento aproximado: maiusculas, acentos e pontuacao contam.

Uma afirmacao e "literal" quando o texto normalizado da afirmacao e
igual a sua citacao normalizada E a citacao ocorre na fonte normalizada.
"""

import json
import unicodedata

CAMPOS_RAIZ = {"answer", "claims"}
CAMPOS_AFIRMACAO = {"text", "evidence_quote"}
MAX_AFIRMACOES = 50

INDICADORES_BOOL = (
    "falha_modelo", "fonte_vazia", "json_invalido", "esquema_invalido",
)
INDICADORES_INT = (
    "afirmacoes_total", "citacoes_nao_encontradas", "afirmacoes_nao_literais",
)


def normalizar(texto):
    return " ".join(unicodedata.normalize("NFC", texto).split())


class _ChaveDuplicada(ValueError):
    pass


def _sem_duplicatas(pares):
    vistos = {}
    for chave, valor in pares:
        if chave in vistos:
            raise _ChaveDuplicada(chave)
        vistos[chave] = valor
    return vistos


def _rejeitar_constante(nome):
    raise ValueError(f"constante nao permitida: {nome}")


def remover_cerca(texto):
    """Aceita o JSON cercado por ``` ou ```json (envelope), nada alem."""
    t = texto.strip()
    if t.startswith("```") and t.endswith("```") and t.count("```") == 2:
        primeira_quebra = t.find("\n")
        if primeira_quebra == -1:
            return t
        rotulo = t[3:primeira_quebra].strip().lower()
        if rotulo in ("", "json"):
            return t[primeira_quebra + 1:-3].strip()
    return t


def interpretar_json(bruto):
    """Devolve o objeto ou None. Chaves duplicadas e NaN/Infinity: None."""
    if not isinstance(bruto, str):
        return None
    try:
        return json.loads(
            remover_cerca(bruto),
            object_pairs_hook=_sem_duplicatas,
            parse_constant=_rejeitar_constante,
        )
    except ValueError:  # inclui JSONDecodeError e _ChaveDuplicada
        return None


def esquema_valido(obj):
    if not isinstance(obj, dict) or set(obj) != CAMPOS_RAIZ:
        return False
    if not isinstance(obj["answer"], str):
        return False
    afirmacoes = obj["claims"]
    if not isinstance(afirmacoes, list) or len(afirmacoes) > MAX_AFIRMACOES:
        return False
    for a in afirmacoes:
        if not isinstance(a, dict) or set(a) != CAMPOS_AFIRMACAO:
            return False
        for campo in CAMPOS_AFIRMACAO:
            if not isinstance(a[campo], str) or not normalizar(a[campo]):
                return False
    return True


def indicadores_vazios():
    d = {n: False for n in INDICADORES_BOOL}
    d.update({n: 0 for n in INDICADORES_INT})
    return d


def analisar(fonte, bruto, falha_modelo=False):
    """Devolve (indicadores, detalhes).

    indicadores: so bool/int, entrada da politica.
    detalhes: dados para exibir (resposta e afirmacoes verificadas).
    Nada aqui executa o conteudo do modelo; ele e tratado como texto.
    """
    ind = indicadores_vazios()
    detalhes = {"resposta": None, "afirmacoes": []}
    fonte_n = normalizar(fonte) if isinstance(fonte, str) else ""
    ind["fonte_vazia"] = not fonte_n
    if falha_modelo:
        ind["falha_modelo"] = True
        return ind, detalhes

    obj = interpretar_json(bruto)
    if obj is None:
        ind["json_invalido"] = True
        return ind, detalhes
    if not esquema_valido(obj):
        ind["esquema_invalido"] = True
        return ind, detalhes

    detalhes["resposta"] = obj["answer"]
    for a in obj["claims"]:
        texto_n = normalizar(a["text"])
        citacao_n = normalizar(a["evidence_quote"])
        encontrada = citacao_n in fonte_n
        literal = encontrada and texto_n == citacao_n
        ind["citacoes_nao_encontradas"] += 0 if encontrada else 1
        ind["afirmacoes_nao_literais"] += 0 if literal else 1
        detalhes["afirmacoes"].append({
            "texto": a["text"],
            "citacao": a["evidence_quote"],
            "citacao_encontrada": encontrada,
            "literal": literal,
        })
    ind["afirmacoes_total"] = len(obj["claims"])
    return ind, detalhes
