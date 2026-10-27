"""
fuzz/gramatica.py — Gera programas GuruDev a partir da gramática do próprio parser.

A gramática não é copiada à mão: as produções são lidas do parser PLY em tempo
de execução (parser.productions). Assim, se a gramática mudar, o gerador muda junto.

Para transformar tokens em texto, usa:
  1. lexemas observados nas sementes (fuzz/sementes.py), em texto-fonte;
  2. para tokens nunca vistos: palavras reservadas, mapas de atributos do lexer
     (nivel, clave, ont, paradigma) e uma expansão simples das expressões
     regulares das regras do lexer.

Estratégia de derivação:
  - cada não-terminal tem uma "profundidade mínima" (menor derivação até tokens);
  - abaixo do limite de profundidade, escolhe produções com preferência pelas
    menos usadas até agora (cobertura de produções);
  - no limite, escolhe a produção de menor profundidade (garante término).

Uso:
  python3 fuzz/gramatica.py --n 20 --semente 1     # imprime 20 programas
  python3 fuzz/gramatica.py --relatorio            # cobertura de produções por N programas
"""

import argparse
import contextlib
import io
import json
import os
import random
import re
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, REPO)
sys.path.insert(0, AQUI)

NOVA_LINHA_DEPOIS = {"SEMICOLON", "LBRACE", "RBRACE", "CODIGO_START", "CODIGO_END", "BLOCO_START", "BLOCO_END",
                     "SOBRESCRITA_END", "SUBESCRITAS_START", "SUBESCRITAS_END"}


def _exemplo_de_regex(rx):
    """Expansão mínima de uma regex 'quase literal' em uma string que ela casa."""
    # alternativa de topo: corta no primeiro "|" que não esteja escapado nem em [] ou ()
    nivel, i = 0, 0
    while i < len(rx):
        if rx[i] == "\\":
            i += 2
            continue
        if rx[i] in "[(":
            nivel += 1
        elif rx[i] in "])":
            nivel -= 1
        elif rx[i] == "|" and nivel == 0:
            rx = rx[:i]
            break
        i += 1
    out, i = [], 0
    while i < len(rx):
        c = rx[i]
        if c == "\\" and i + 1 < len(rx):
            out.append(rx[i + 1])
            i += 2
            continue
        if c == "[":
            fim = rx.index("]", i + 1)
            classe = rx[i + 1:fim]
            out.append("a" if classe.startswith("^") else classe[0])
            i = fim + 1
            if i < len(rx) and rx[i] in "*?":
                out.pop()
                i += 1
            elif i < len(rx) and rx[i] == "+":
                i += 1
            continue
        if c in "()":
            i += 1
            continue
        if c in "?*":
            if out:
                out.pop()
            i += 1
            continue
        if c == "+":
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


class Gramatica:
    def __init__(self, vocabulario=None, semente=0):
        from src import parser as mod_parser
        import src.lexer.gurudev_lexer as L

        with contextlib.redirect_stdout(io.StringIO()):
            self.parser = mod_parser.build_parser(debug=False)
        self.L = L
        self.prods = {}
        for p in self.parser.productions[1:]:
            nome, _, corpo = p.str.partition(" -> ")
            simbolos = [] if corpo.strip() == "<empty>" else corpo.split()
            self.prods.setdefault(nome, []).append((p.str, simbolos))
        self.nao_terminais = set(self.prods)
        self.uso = Counter()
        self.rng = random.Random(semente)
        self.vocab = {k: list(v) for k, v in (vocabulario or {}).items() if v}
        self.lexemas_derivados = {}
        self._completar_vocabulario()
        self._profundidade_minima()

    # -------------------------------------------------------- vocabulário
    def _completar_vocabulario(self):
        L = self.L
        tokens = set(L.tokens)
        for palavra, tipo in L.reserved.items():
            self.vocab.setdefault(tipo, [palavra])
        mapas = [("nivel", getattr(L, "nivel_map", {})), ("clave", getattr(L, "clave_map", {})),
                 ("ont", getattr(L, "ont_map", {})), ("paradigma", getattr(L, "paradigma_map", {}))]
        for attr, mapa in mapas:
            for valor, tipo in mapa.items():
                self.vocab.setdefault(tipo, [f'$${attr}="{valor}"$$'])
        for nome, obj in vars(L).items():
            if not nome.startswith("t_") or nome in ("t_error", "t_ignore"):
                continue
            tipo = nome.split("_", 2)[-1] if nome.count("_") >= 2 and nome.split("_")[1].islower() else nome[2:]
            if tipo not in tokens or tipo in self.vocab:
                continue
            rx = obj.__doc__ if callable(obj) else obj
            if isinstance(rx, str) and rx:
                ex = _exemplo_de_regex(rx)
                if ex:
                    self.vocab[tipo] = [ex]
                    self.lexemas_derivados[tipo] = ex
        # nomes de funções nativas e métodos de String/Array: sem eles o gerador
        # quase nunca chama a biblioteca padrão (medido no piloto: nativas.py em 66%)
        self.nativas, self.metodos = [], []
        try:
            from src import interpreter as I, nativas as N
            self.nativas = sorted(I.NATIVAS)
            self.metodos = sorted(set(N.StringMethods._METHODS) | set(N.ArrayMethods._METHODS))
        except Exception:  # noqa: BLE001 — gerador continua sem a API se a estrutura mudar
            pass
        ids = list(self.vocab.get("ID", []))
        self.vocab["ID"] = ids + (self.nativas + self.metodos) * 2
        self.sem_lexema = sorted(t for t in tokens if t not in self.vocab)

    # -------------------------------------------------------- profundidade
    def _profundidade_minima(self):
        INF = 10 ** 9
        prof = {nt: INF for nt in self.nao_terminais}
        mudou = True
        while mudou:
            mudou = False
            for nt, alts in self.prods.items():
                for _, simbolos in alts:
                    d = 1 + max([prof[s] if s in self.nao_terminais else 0 for s in simbolos] or [0])
                    if d < prof[nt]:
                        prof[nt] = d
                        mudou = True
        self.prof = prof

    def _prof_alt(self, simbolos):
        return 1 + max([self.prof[s] if s in self.nao_terminais else 0 for s in simbolos] or [0])

    # -------------------------------------------------------- derivação
    def derivar(self, inicio="programa", max_prof=9, max_tokens=400):
        saida = []

        def expandir(simbolo, prof):
            if len(saida) > max_tokens:
                return
            if simbolo not in self.nao_terminais:
                saida.append(simbolo)
                return
            alts = [a for a in self.prods[simbolo] if a[1] or True]
            if prof >= max_prof:
                melhor = min(self._prof_alt(s) for _, s in alts)
                candidatas = [a for a in alts if self._prof_alt(a[1]) == melhor]
            else:
                # preferência pelas produções menos usadas, com sorteio ponderado
                pesos = [1.0 / (1 + self.uso[a[0]]) for a in alts]
                candidatas = self.rng.choices(alts, weights=pesos, k=1)
            texto, simbolos = self.rng.choice(candidatas)
            self.uso[texto] += 1
            for s in simbolos:
                expandir(s, prof + 1)

        expandir(inicio, 0)
        return saida

    def renderizar(self, tokens):
        partes = []
        for t in tokens:
            opcoes = self.vocab.get(t)
            lex = self.rng.choice(opcoes) if opcoes else f"/*{t}*/"
            partes.append(lex)
            partes.append("\n" if t in NOVA_LINHA_DEPOIS else " ")
        return "".join(partes)

    def programa(self, max_prof=9):
        return self.renderizar(self.derivar(max_prof=max_prof))

    def cobertura_producoes(self):
        todas = [t for alts in self.prods.values() for t, _ in alts]
        usadas = [t for t in todas if self.uso[t]]
        return len(usadas), len(todas), sorted(set(todas) - set(usadas))


def carregar_vocabulario(caminho=None):
    if caminho and os.path.exists(caminho):
        return json.load(open(caminho, encoding="utf-8"))
    from sementes import coletar
    return coletar(REPO)[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--semente", type=int, default=0)
    ap.add_argument("--vocabulario", default=None)
    ap.add_argument("--relatorio", action="store_true", help="mede aceitação pelo parser e cobertura de produções")
    a = ap.parse_args()
    g = Gramatica(carregar_vocabulario(a.vocabulario), a.semente)
    if not a.relatorio:
        for _ in range(a.n):
            print(g.programa())
            print("// ----")
        return
    from src.lexer import build_lexer
    aceitos = 0
    for _ in range(a.n):
        prog = g.programa()
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                ok = g.parser.parse(prog, lexer=build_lexer()) is not None and "Erro sint" not in buf.getvalue()
        except Exception:  # noqa: BLE001
            ok = False
        aceitos += ok
    usadas, total, nunca = g.cobertura_producoes()
    print(json.dumps({"programas": a.n, "aceitos_pelo_parser": aceitos,
                      "producoes_usadas": f"{usadas}/{total}", "tokens_sem_lexema": g.sem_lexema,
                      "lexemas_derivados_de_regex": g.lexemas_derivados, "producoes_nunca_usadas": nunca[:30]},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
