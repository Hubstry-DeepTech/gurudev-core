"""Recuperacao de fichas da base de conhecimento (BM25, sem dependencias)."""

import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

BASE_PADRAO = Path(__file__).resolve().parent / "base_conhecimento.json"

PALAVRAS_VAZIAS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "e", "ou", "que", "com", "para",
    "por", "se", "como", "eu", "me", "meu", "minha", "isso", "esse",
    "essa", "este", "esta", "ao", "aos", "the", "of", "and", "to", "in",
    "is", "qual", "quais", "ser", "sao", "posso", "pode", "usar",
    "explique", "explica", "fale", "sobre", "diga", "conte", "me",
}


# O nome da linguagem aparece em quase toda ficha e nao distingue nada.
TERMOS_DO_DOMINIO = {"gurudev", "guru"}

# Fichas de apresentacao, usadas quando a pergunta e generica sobre a
# linguagem (ex.: "O que e a GuruDev?").
APRESENTACAO = [
    ("README.md", "Em uma frase"),
    ("docs/WHITEPAPER.md", "1. Introdução"),
    ("README.md", "O Diferencial Ontológico"),
]


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return sem_acento.lower()


def termos(texto):
    return [
        t
        for t in re.findall(r"[a-z0-9_]+", normalizar(texto))
        if len(t) > 1 and t not in PALAVRAS_VAZIAS
    ]


def carregar_base(caminho=BASE_PADRAO):
    return json.loads(Path(caminho).read_text("utf-8"))


class Buscador:
    """BM25 sobre secao + texto de cada ficha."""

    def __init__(self, fichas, k1=1.5, b=0.75):
        self.fichas = fichas
        self.k1 = k1
        self.b = b
        self.docs = [
            Counter(termos(f["secao"] + " " + f["texto"])) for f in fichas
        ]
        self.tamanhos = [sum(d.values()) for d in self.docs]
        self.media = sum(self.tamanhos) / max(len(self.docs), 1)
        df = Counter()
        for d in self.docs:
            df.update(d.keys())
        n = len(self.docs)
        self.idf = {
            t: math.log(1 + (n - q + 0.5) / (q + 0.5)) for t, q in df.items()
        }

    def pontuar(self, consulta, i):
        doc, tam = self.docs[i], self.tamanhos[i]
        total = 0.0
        for t in consulta:
            f = doc.get(t, 0)
            if not f:
                continue
            norm = self.k1 * (1 - self.b + self.b * tam / self.media)
            total += self.idf[t] * f * (self.k1 + 1) / (f + norm)
        return total

    def apresentacao(self, k):
        achadas = []
        for fonte, titulo in APRESENTACAO:
            for f in self.fichas:
                if f["fonte"] == fonte and f["secao"].endswith(titulo):
                    achadas.append(f)
                    break
        return achadas[:k]

    def buscar(self, pergunta, k=4):
        todos = termos(pergunta)
        consulta = [t for t in todos if t not in TERMOS_DO_DOMINIO]
        if todos and not consulta:
            return self.apresentacao(k)
        notas = [(self.pontuar(consulta, i), i) for i in range(len(self.docs))]
        notas = [(p, i) for p, i in notas if p > 0]
        notas.sort(key=lambda x: (-x[0], x[1]))
        if not notas and set(todos) & TERMOS_DO_DOMINIO:
            return self.apresentacao(k)
        return [self.fichas[i] for _, i in notas[:k]]
