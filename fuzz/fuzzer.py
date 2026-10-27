"""
fuzz/fuzzer.py — Fuzzing guiado por cobertura do lexer, parser e interpretador GuruDev.

Cada entrada roda no executor isolado (fuzz/executor.py) com cobertura de linhas
e ramos de src/. Entradas que alcançam código novo entram no corpus; entradas
que revelam falhas são salvas por assinatura (status + exceção + local).

Fontes de entradas (pesos ajustáveis):
  gramatica  programa novo derivado da gramática do parser (fuzz/gramatica.py)
  mutacao    1 a 4 mutações em nível de token de um item do corpus
  cruzamento prefixo de um item + sufixo de outro, em fronteira de token
  valores    troca literais por valores-limite (0, -1, 2**63, 1e309, "", texto longo, unicode)
  api        chamada direta a funções nativas e métodos de String/Array com argumentos variados

Saída (--saida):
  corpus/<hash>.guru        entradas com cobertura nova (corpus reproduzível)
  falhas/<assinatura>/      menor programa que reproduz cada falha + resultado.json
  estatisticas.jsonl        uma linha a cada --intervalo segundos
  resumo.json               estado final
  PARAR                     crie este arquivo para encerrar com segurança

Critérios de parada (o primeiro que ocorrer):
  --max-minutos, --max-execucoes, --parar-sem-novidade-min (sem cobertura nova
  E sem assinatura nova por N minutos), arquivo PARAR, ou SIGTERM/SIGINT.

Uso:
  python3 fuzz/fuzzer.py --saida resultados/fuzz --processos 2 --max-minutos 10
"""

import argparse
import hashlib
import json
import os
import random
import re
import signal
import sys
import threading
import time
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
sys.path.insert(0, REPO)

from executor import STATUS_BUG, Executor, assinatura  # noqa: E402
from gramatica import Gramatica  # noqa: E402
from sementes import coletar  # noqa: E402

TOKEN_RX = re.compile(r'"(?:[^"\\\n]|\\.)*"|\d+\.\d+|\d+|[A-Za-z_À-ÿ][\wÀ-ÿ]*|\s+|[^\w\s]')
VALORES_LIMITE = ["0", "-1", "1", "2147483648", "9223372036854775808", "1e309", "-0.0", "0.000001",
                  '""', '"' + "a" * 5000 + '"', '"\\u0000"', '"ção🙂"', "[]", "[[[[[[]]]]]]", "nulo", "true", "false"]


def h(txt):
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()


def nome_seguro(assin):
    return re.sub(r"[^\w.-]+", "_", assin)[:90] + "-" + h(assin)[:8]


class Fuzzer:
    def __init__(self, a):
        self.a = a
        self.rng = random.Random(a.semente)
        self.saida = os.path.abspath(a.saida)
        for sub in ("corpus", "falhas"):
            os.makedirs(os.path.join(self.saida, sub), exist_ok=True)
        sementes, vocab = coletar(REPO)
        self.vocab = vocab
        self.gram = Gramatica(vocab, a.semente)
        self.lexemas = [x for v in self.gram.vocab.values() for x in v if len(x) < 60]
        self.corpus = []           # lista de textos
        self.cobertura = set()
        self.falhas = {}           # assinatura -> dict
        self.status = Counter()
        self.origem_novidade = Counter()
        self.execucoes = 0
        self.inicio = time.time()
        self.ultima_novidade = time.time()
        self.lock = threading.Lock()
        self.parar = False
        self._carregar_existente()
        self.fila_inicial = [s["codigo"] for s in sementes] + list(self.corpus)
        self.corpus = []

    # -------------------------------------------------------- persistência
    def _carregar_existente(self):
        pasta = os.path.join(self.saida, "corpus")
        for arq in sorted(os.listdir(pasta)):
            if arq.endswith(".guru"):
                self.corpus.append(open(os.path.join(pasta, arq), encoding="utf-8").read())
        for d in sorted(os.listdir(os.path.join(self.saida, "falhas"))):
            meta = os.path.join(self.saida, "falhas", d, "resultado.json")
            if os.path.exists(meta):
                m = json.load(open(meta, encoding="utf-8"))
                self.falhas[m["assinatura"]] = m

    def _salvar_corpus(self, prog):
        caminho = os.path.join(self.saida, "corpus", h(prog)[:16] + ".guru")
        if not os.path.exists(caminho):
            open(caminho, "w", encoding="utf-8").write(prog)

    def _registrar_falha(self, assin, prog, res, origem):
        pasta = os.path.join(self.saida, "falhas", nome_seguro(assin))
        f = self.falhas.get(assin)
        if f is None:
            os.makedirs(pasta, exist_ok=True)
            f = {"assinatura": assin, "ocorrencias": 0, "primeira_vez_s": round(time.time() - self.inicio, 1),
                 "origem": origem, "tamanho": None}
            self.falhas[assin] = f
            self.ultima_novidade = time.time()
            novo = True
        else:
            novo = False
        f["ocorrencias"] += 1
        if f["tamanho"] is None or len(prog) < f["tamanho"]:
            f["tamanho"] = len(prog)
            f["resultado"] = {k: v for k, v in res.items() if k != "cobertura"}
            open(os.path.join(pasta, "programa.guru"), "w", encoding="utf-8").write(prog)
        if novo or f["ocorrencias"] % 50 == 0:
            json.dump(f, open(os.path.join(pasta, "resultado.json"), "w"), indent=2, ensure_ascii=False)
        return novo

    # -------------------------------------------------------- geração de entradas
    def _tokens(self, prog):
        return TOKEN_RX.findall(prog)

    def _mutar(self, prog):
        t = self._tokens(prog)
        if not t:
            return self.gram.programa()
        for _ in range(self.rng.randint(1, 4)):
            if not t:
                break
            i = self.rng.randrange(len(t))
            op = self.rng.random()
            if op < 0.2:
                t.pop(i)
            elif op < 0.35:
                t.insert(self.rng.randrange(len(t) + 1), t[i])
            elif op < 0.5:
                j = self.rng.randrange(len(t))
                t[i], t[j] = t[j], t[i]
            elif op < 0.8:
                t.insert(i, " " + self.rng.choice(self.lexemas) + " ")
            else:
                j = min(len(t), i + self.rng.randint(1, 30))
                t[i:i] = t[i:j]  # duplica um trecho
        return "".join(t)

    def _cruzar(self, a, b):
        ta, tb = self._tokens(a), self._tokens(b)
        if not ta or not tb:
            return a
        return "".join(ta[: self.rng.randrange(len(ta) + 1)] + tb[self.rng.randrange(len(tb)):])

    def _valores(self, prog):
        t = self._tokens(prog)
        idx = [i for i, x in enumerate(t) if re.fullmatch(r'\d+(\.\d+)?|"(?:[^"\\]|\\.)*"', x)]
        if not idx:
            return self._mutar(prog)
        for i in self.rng.sample(idx, min(len(idx), self.rng.randint(1, 3))):
            t[i] = self.rng.choice(VALORES_LIMITE)
        return "".join(t)

    def _api(self):
        """Chamada direta a uma nativa ou a um método, com argumentos-limite e de tipos misturados."""
        args_pool = VALORES_LIMITE + ["0", "2", "3.5", '"abc"', '"a,b,c"', "[3, 1, 2]", '["b", "a"]', "[1, \"x\"]",
                                      "verdadeiro", "falso"]
        def args(n):
            return ", ".join(self.rng.choice(args_pool) for _ in range(n))
        if self.gram.metodos and self.rng.random() < 0.5:
            alvo = self.rng.choice(['"Texto, de exemplo"', "[3, 1, 2]", '["b", "a", "c"]', '""', "[]", "[1, \"x\", 2.5]"])
            return f"Object v = {alvo};\nescrever(v.{self.rng.choice(self.gram.metodos)}({args(self.rng.randint(0, 3))}));\n"
        if self.gram.nativas:
            return f"escrever({self.rng.choice(self.gram.nativas)}({args(self.rng.randint(0, 3))}));\n"
        return self.gram.programa()

    def proxima(self):
        if self.fila_inicial:
            return self.fila_inicial.pop(0), "semente"
        pesos = self.a.pesos
        base = self.corpus or [self.gram.programa()]
        modo = self.rng.choices(["gramatica", "mutacao", "cruzamento", "valores", "api"], weights=pesos)[0]
        if modo == "api":
            return self._api(), modo
        if modo == "gramatica":
            return self.gram.programa(max_prof=self.rng.randint(5, 12)), modo
        escolhido = self.rng.choice(base)
        if modo == "mutacao":
            return self._mutar(escolhido), modo
        if modo == "cruzamento":
            return self._cruzar(escolhido, self.rng.choice(base)), modo
        return self._valores(escolhido), modo

    # -------------------------------------------------------- laço principal
    def processar(self, prog, origem, res):
        with self.lock:
            self.execucoes += 1
            st = res.get("status", "?")
            self.status[st] += 1
            feats = set(res.get("cobertura") or ())
            novas = feats - self.cobertura
            if novas and st not in ("TIMEOUT", "MORTO"):
                self.cobertura |= novas
                if len(prog) <= self.a.max_bytes_corpus:
                    self.corpus.append(prog)
                    self._salvar_corpus(prog)
                self.ultima_novidade = time.time()
                self.origem_novidade[origem] += 1
            if st in STATUS_BUG:
                assin = assinatura(res)
                if assin == "TIMEOUT|laco-do-programa" and not self.a.registrar_lacos:
                    return
                if self._registrar_falha(assin, prog, res, origem):
                    print(f"[{self._tempo()}] NOVA FALHA: {assin}", flush=True)

    def _tempo(self):
        s = int(time.time() - self.inicio)
        return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"

    def estatistica(self):
        dur = time.time() - self.inicio
        return {
            "tempo_s": round(dur, 1), "execucoes": self.execucoes,
            "exec_por_s": round(self.execucoes / dur, 1) if dur else 0,
            "corpus": len(self.corpus), "cobertura_pontos": len(self.cobertura),
            "assinaturas": len(self.falhas),
            "assinaturas_bug": sum(1 for k in self.falhas if k != "TIMEOUT|laco-do-programa"),
            "minutos_sem_novidade": round((time.time() - self.ultima_novidade) / 60, 1),
            "status": dict(self.status), "novidade_por_origem": dict(self.origem_novidade),
        }

    def deve_parar(self):
        if self.parar or os.path.exists(os.path.join(self.saida, "PARAR")):
            return "sinal ou arquivo PARAR"
        if self.a.max_minutos and time.time() - self.inicio >= self.a.max_minutos * 60:
            return "max-minutos"
        if self.a.max_execucoes and self.execucoes >= self.a.max_execucoes:
            return "max-execucoes"
        if self.a.parar_sem_novidade_min and not self.fila_inicial and \
                time.time() - self.ultima_novidade >= self.a.parar_sem_novidade_min * 60:
            return "sem-novidade"
        return None

    def rodar(self):
        local = threading.local()
        execs = []

        def trabalho(prog):
            ex = getattr(local, "ex", None)
            if ex is None:
                ex = local.ex = Executor(REPO, timeout=self.a.timeout, memoria_mb=self.a.memoria_mb, cobertura=True)
                ex.iniciar()
                with self.lock:
                    execs.append(ex)
            return ex.rodar(prog)

        estat = open(os.path.join(self.saida, "estatisticas.jsonl"), "a")
        proxima_estat = time.time()
        motivo = None
        print(f"[{self._tempo()}] início: {len(self.fila_inicial)} sementes, {self.a.processos} processos, "
              f"produções na gramática: {sum(len(v) for v in self.gram.prods.values())}", flush=True)
        with ThreadPoolExecutor(max_workers=self.a.processos) as pool:
            pendentes = {}
            while True:
                motivo = self.deve_parar()
                while not motivo and len(pendentes) < self.a.processos * 2:
                    prog, origem = self.proxima()
                    pendentes[pool.submit(trabalho, prog)] = (prog, origem)
                if not pendentes:
                    break
                prontos, _ = wait(list(pendentes), timeout=1, return_when=FIRST_COMPLETED)
                for fut in prontos:
                    prog, origem = pendentes.pop(fut)
                    try:
                        self.processar(prog, origem, fut.result())
                    except Exception as e:  # noqa: BLE001 — erro do próprio harness não pode derrubar a rodada
                        print(f"[harness] erro ao processar entrada: {e!r}", flush=True)
                if time.time() >= proxima_estat:
                    with self.lock:
                        e = self.estatistica()
                    estat.write(json.dumps(e, ensure_ascii=False) + "\n")
                    estat.flush()
                    print(f"[{self._tempo()}] exec {e['execucoes']} ({e['exec_por_s']}/s) | corpus {e['corpus']} | "
                          f"cobertura {e['cobertura_pontos']} | falhas {e['assinaturas_bug']} | "
                          f"sem novidade há {e['minutos_sem_novidade']} min", flush=True)
                    proxima_estat = time.time() + self.a.intervalo
                if motivo and not pendentes:
                    break
        for ex in execs:
            ex.fechar()
        final = self.estatistica()
        final["motivo_parada"] = motivo
        final["parametros"] = vars(self.a)
        final["falhas"] = {k: {"ocorrencias": v["ocorrencias"], "tamanho": v["tamanho"],
                               "primeira_vez_s": v["primeira_vez_s"], "origem": v["origem"]}
                           for k, v in sorted(self.falhas.items())}
        for k, v in self.falhas.items():
            pasta = os.path.join(self.saida, "falhas", nome_seguro(k))
            json.dump(v, open(os.path.join(pasta, "resultado.json"), "w"), indent=2, ensure_ascii=False)
        estat.write(json.dumps({k: final[k] for k in final if k not in ("falhas", "parametros")}, ensure_ascii=False) + "\n")
        estat.close()
        json.dump(final, open(os.path.join(self.saida, "resumo.json"), "w"), indent=2, ensure_ascii=False)
        print(f"[{self._tempo()}] fim ({motivo}). {final['execucoes']} execuções, "
              f"{final['assinaturas_bug']} assinaturas de falha, cobertura {final['cobertura_pontos']} pontos.", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saida", default="resultados/fuzz")
    ap.add_argument("--processos", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--semente", type=int, default=1)
    ap.add_argument("--timeout", type=float, default=3.0)
    ap.add_argument("--memoria-mb", type=int, default=1024)
    ap.add_argument("--max-minutos", type=float, default=0)
    ap.add_argument("--max-execucoes", type=int, default=0)
    ap.add_argument("--parar-sem-novidade-min", type=float, default=0)
    ap.add_argument("--intervalo", type=float, default=30)
    ap.add_argument("--max-bytes-corpus", type=int, default=20000)
    ap.add_argument("--registrar-lacos", action="store_true",
                    help="também salva timeouts em laço do próprio programa (esperados)")
    ap.add_argument("--pesos", type=float, nargs=5, default=[0.22, 0.40, 0.13, 0.13, 0.12],
                    metavar=("GRAMATICA", "MUTACAO", "CRUZAMENTO", "VALORES", "API"))
    a = ap.parse_args()
    fz = Fuzzer(a)

    def _sinal(signum, frame):
        fz.parar = True
        print(f"[{fz._tempo()}] sinal {signum} recebido: encerrando com segurança...", flush=True)

    signal.signal(signal.SIGTERM, _sinal)
    signal.signal(signal.SIGINT, _sinal)
    fz.rodar()


if __name__ == "__main__":
    main()
