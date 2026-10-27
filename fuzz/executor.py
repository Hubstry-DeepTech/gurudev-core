"""
fuzz/executor.py — Execução isolada de programas GuruDev para testes em massa.

Cada programa roda em um processo próprio, criado por fork a partir de um
"servidor" que já importou o lexer, o parser e o interpretador. Assim o custo
de importação é pago uma vez, e cada programa continua isolado:

- processo filho em sessão própria (o grupo inteiro é morto no timeout);
- limites de memória (RLIMIT_AS), de CPU, de tamanho de arquivo e de processos;
- diretório de trabalho temporário e vazio;
- entrada padrão fixa e semente aleatória fixa (execução determinística);
- saída do programa truncada (não enche disco nem memória);
- bloco de Python embutido ("subescrita") com builtins restritos: sem open,
  sem input, e import só de módulos puros da biblioteca padrão. Isso protege a
  máquina; a restrição é do harness, não altera o código da linguagem.

Classificação do resultado (campo "status"):
  OK            programa executou até o fim
  SINTAXE       o parser rejeitou o programa (comportamento esperado)
  ERRO_GURU     o interpretador levantou GuruDevError (comportamento esperado)
  CRASH_LEXER   exceção Python não tratada no lexer       -> bug
  CRASH_PARSER  exceção Python não tratada no parser      -> bug
  CRASH_INTERP  exceção Python não tratada no interpretador -> bug
  RECURSAO      RecursionError (pode ser recursão do programa ou do interpretador)
  TIMEOUT       passou do tempo limite (laço do programa ou travamento interno)
  MEMORIA       MemoryError ou estouro do limite de memória
  MORTO         o processo morreu sem responder (sinal)

Uso como biblioteca:
    with Executor(repo) as ex:
        r = ex.rodar(codigo_fonte)

Uso direto:
    python3 fuzz/executor.py --repo . programa.guru
"""

import json
import os
import select
import signal
import struct
import subprocess
import sys
import time

PADRAO_TIMEOUT = 5.0
PADRAO_MEMORIA_MB = 1024
LIMITE_SAIDA = 4096

class TempoEsgotado(BaseException):
    """Levantada pelo alarme no filho, um pouco antes do kill: registra ONDE o programa estava."""


STATUS_BUG = {"CRASH_LEXER", "CRASH_PARSER", "CRASH_INTERP", "RECURSAO", "TIMEOUT", "MEMORIA", "MORTO"}

MODULOS_PERMITIDOS = {
    "math", "cmath", "statistics", "random", "json", "re", "itertools", "functools",
    "collections", "string", "decimal", "fractions", "datetime", "operator", "copy",
    "heapq", "bisect", "textwrap", "unicodedata",
}
BUILTINS_PROIBIDOS = {"open", "input", "breakpoint", "exit", "quit", "help", "__import__"}


# ------------------------------------------------------------ protocolo

def _enviar(arq, obj):
    dados = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    arq.write(struct.pack(">I", len(dados)) + dados)
    arq.flush()


def _receber(arq):
    cab = arq.read(4)
    if len(cab) < 4:
        return None
    (n,) = struct.unpack(">I", cab)
    return json.loads(arq.read(n).decode("utf-8"))


# ------------------------------------------------------------ lado do servidor

class _SaidaLimitada:
    """Substitui stdout/stderr: guarda só o começo e conta o resto."""

    def __init__(self):
        self.partes, self.total = [], 0

    def write(self, s):
        if self.total < LIMITE_SAIDA:
            self.partes.append(s[: LIMITE_SAIDA - self.total])
        self.total += len(s)
        return len(s)

    def flush(self):
        pass

    def texto(self):
        return "".join(self.partes)


def _builtins_restritos():
    import builtins

    original_import = builtins.__import__

    def importar(nome, globais=None, locais=None, deslista=(), nivel=0):
        if nivel != 0 or nome.split(".")[0] not in MODULOS_PERMITIDOS:
            raise ImportError(f"[harness] import bloqueado: {nome}")
        return original_import(nome, globais, locais, deslista, nivel)

    d = {k: v for k, v in vars(builtins).items() if k not in BUILTINS_PROIBIDOS}
    d["__import__"] = importar
    return d


def _local_no_repo(tb, repo_src):
    """Frame mais profundo do traceback que está dentro de src/ (onde o bug mora)."""
    import traceback

    frames = traceback.extract_tb(tb)
    dentro = [f for f in frames if os.path.abspath(f.filename).startswith(repo_src)]
    alvo = dentro[-1] if dentro else (frames[-1] if frames else None)
    if alvo is None:
        return "?", []
    rel = os.path.relpath(alvo.filename, os.path.dirname(repo_src))
    pilha = [f"{os.path.relpath(f.filename, os.path.dirname(repo_src)) if os.path.abspath(f.filename).startswith(repo_src) else os.path.basename(f.filename)}:{f.lineno} {f.name}"
             for f in frames[-10:]]
    return f"{rel}:{alvo.lineno} {alvo.name}", pilha


def _filho(codigo, cfg, fd_resultado, parser, mod_lexer, mod_interp, repo_src):
    """Roda dentro do processo filho. Nunca retorna: termina com os._exit."""
    import io
    import random
    import resource
    import tempfile

    os.setsid()
    mem = cfg["memoria_mb"] * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
    cpu = int(cfg["timeout"]) + 2
    resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 1))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1 << 20, 1 << 20))
    try:
        resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
    except (ValueError, OSError):
        pass
    os.chdir(tempfile.mkdtemp(prefix="guru-fuzz-"))
    sys.stdin = io.StringIO("entrada\n" * 64)
    random.seed(0)
    sys.setrecursionlimit(cfg.get("recursao", 3000))

    def _alarme(signum, frame):
        raise TempoEsgotado()

    signal.signal(signal.SIGALRM, _alarme)
    signal.setitimer(signal.ITIMER_REAL, max(0.2, cfg["timeout"] - 0.5))
    mod_interp.builtins = _builtins_restritos()

    saida = _SaidaLimitada()
    sys.stdout = sys.stderr = saida

    cobertos = set()
    if cfg.get("cobertura"):
        mon = sys.monitoring
        ferramenta = mon.COVERAGE_ID
        mon.use_tool_id(ferramenta, "guru-fuzz")
        nomes = {}

        def linha(code, num):
            fn = code.co_filename
            if fn.startswith(repo_src):
                idx = nomes.setdefault(fn, len(nomes))
                cobertos.add((idx, num))
            return mon.DISABLE

        def ramo(code, origem, destino):
            fn = code.co_filename
            if fn.startswith(repo_src):
                idx = nomes.setdefault(fn, len(nomes))
                cobertos.add((idx, -origem - 1, destino))
            return mon.DISABLE

        mon.register_callback(ferramenta, mon.events.LINE, linha)
        eventos = mon.events.LINE
        if hasattr(mon.events, "BRANCH_RIGHT"):
            mon.register_callback(ferramenta, mon.events.BRANCH_LEFT, ramo)
            mon.register_callback(ferramenta, mon.events.BRANCH_RIGHT, ramo)
            eventos |= mon.events.BRANCH_LEFT | mon.events.BRANCH_RIGHT
        else:
            mon.register_callback(ferramenta, mon.events.BRANCH, ramo)
            eventos |= mon.events.BRANCH
        mon.set_events(ferramenta, eventos)

    r = {"status": None}
    t0 = time.perf_counter()
    fase = "lexer"
    try:
        lexer = mod_lexer.build_lexer()
        fase = "parser"
        ast = parser.parse(codigo, lexer=lexer)
        texto_parse = saida.texto()
        r["erro_sintatico_reportado"] = ("Erro sint" in texto_parse) or ("Caractere ilegal" in texto_parse)
        if ast is None:
            r["status"] = "SINTAXE"
        else:
            fase = "interp"
            mod_interp.Interpreter().interpretar(ast)
            r["status"] = "OK"
    except TempoEsgotado as e:
        local, pilha = _local_no_repo(e.__traceback__, repo_src)
        # olha a pilha inteira (a "pilha" salva tem só os 10 frames finais)
        import traceback
        nomes = [f.name for f in traceback.extract_tb(e.__traceback__)]
        laco = any(n in ("_x_Enquanto", "_x_Para", "_x_ParaCada") for n in nomes)
        r.update(status="TIMEOUT", exc="TempoEsgotado", local=local, pilha=pilha, fase=fase,
                 laco_do_programa=laco)
    except mod_interp.GuruDevError as e:
        r.update(status="ERRO_GURU", exc="GuruDevError", msg=str(e)[:300])
    except RecursionError as e:
        local, pilha = _local_no_repo(e.__traceback__, repo_src)
        r.update(status="RECURSAO", exc="RecursionError", msg=str(e)[:300], local=local, pilha=pilha, fase=fase)
    except MemoryError as e:
        r.update(status="MEMORIA", exc="MemoryError", fase=fase)
    except BaseException as e:  # noqa: BLE001 — queremos tudo, inclusive SystemExit
        local, pilha = _local_no_repo(e.__traceback__, repo_src)
        if "gurudev_lexer" in local:
            st = "CRASH_LEXER"
        elif fase == "interp":
            st = "CRASH_INTERP"
        else:
            st = "CRASH_PARSER"
        r.update(status=st, exc=type(e).__name__, msg=str(e)[:300], local=local, pilha=pilha, fase=fase)

    signal.setitimer(signal.ITIMER_REAL, 0)
    if cfg.get("cobertura"):
        sys.monitoring.set_events(sys.monitoring.COVERAGE_ID, 0)
        r["cobertura"] = [hash(c) & 0xFFFFFFFFFFFF for c in cobertos]
        r["n_cobertura"] = len(cobertos)
    r["tempo"] = round(time.perf_counter() - t0, 4)
    r["saida"] = saida.texto()[:500]
    r["saida_bytes"] = saida.total
    try:
        dados = json.dumps(r, ensure_ascii=False, default=str).encode("utf-8")
    except Exception:  # noqa: BLE001
        dados = json.dumps({"status": r["status"], "msg": "resultado não serializável"}).encode()
    with os.fdopen(fd_resultado, "wb") as f:
        f.write(dados)
    os._exit(0)


def _servidor(repo):
    """Importa a GuruDev uma vez e atende pedidos, um fork por programa."""
    repo = os.path.abspath(repo)
    sys.path.insert(0, repo)
    entrada, saida = sys.stdin.buffer, sys.stdout.buffer
    sys.stdout = sys.stderr  # nada de print acidental no canal do protocolo
    import contextlib
    import io

    from src import interpreter as mod_interp
    from src import parser as mod_parser
    from src import lexer as mod_lexer

    with contextlib.redirect_stdout(io.StringIO()):
        parser = mod_parser.build_parser(debug=False)
    repo_src = os.path.join(repo, "src")
    _enviar(saida, {"pronto": True, "python": sys.version.split()[0]})

    while True:
        pedido = _receber(entrada)
        if pedido is None:
            return
        cfg = pedido["cfg"]
        leitura, escrita = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(leitura)
            try:
                _filho(pedido["codigo"], cfg, escrita, parser, mod_lexer, mod_interp, repo_src)
            finally:
                os._exit(70)
        os.close(escrita)
        partes, inicio, estourou = [], time.monotonic(), False
        while True:
            resta = cfg["timeout"] + 1.5 - (time.monotonic() - inicio)
            if resta <= 0:
                estourou = True
                break
            prontos, _, _ = select.select([leitura], [], [], resta)
            if not prontos:
                continue
            bloco = os.read(leitura, 1 << 16)
            if not bloco:
                break
            partes.append(bloco)
        os.close(leitura)
        if estourou:
            try:
                os.killpg(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        _, estado = os.waitpid(pid, 0)
        if estourou:
            # o alarme não conseguiu interromper (ex.: preso dentro de código C, como regex)
            res = {"status": "TIMEOUT", "tempo": cfg["timeout"], "local": "sem-pilha (preso fora do Python)"}
        elif partes:
            try:
                res = json.loads(b"".join(partes).decode("utf-8"))
            except ValueError:
                res = {"status": "MORTO", "msg": "resultado truncado"}
        else:
            sinal = os.WTERMSIG(estado) if os.WIFSIGNALED(estado) else None
            nome = signal.Signals(sinal).name if sinal else f"exit {os.WEXITSTATUS(estado)}"
            # SIGKILL/SIGSEGV por falta de memória aparecem aqui também
            res = {"status": "MORTO", "msg": nome}
        _enviar(saida, res)


# ------------------------------------------------------------ lado do cliente

class Executor:
    def __init__(self, repo, timeout=PADRAO_TIMEOUT, memoria_mb=PADRAO_MEMORIA_MB, cobertura=False):
        self.repo = os.path.abspath(repo)
        self.cfg = {"timeout": float(timeout), "memoria_mb": int(memoria_mb), "cobertura": bool(cobertura)}
        self.proc = None

    def __enter__(self):
        self.iniciar()
        return self

    def __exit__(self, *exc):
        self.fechar()

    def iniciar(self):
        self.proc = subprocess.Popen(
            [sys.executable, "-I", os.path.abspath(__file__), "--servidor", self.repo],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            cwd=self.repo,
        )
        ola = _receber(self.proc.stdout)
        if not ola or not ola.get("pronto"):
            raise RuntimeError("servidor de execução não iniciou")
        self.python = ola["python"]

    def rodar(self, codigo, **cfg_extra):
        if self.proc is None or self.proc.poll() is not None:
            self.iniciar()
        cfg = dict(self.cfg, **cfg_extra)
        try:
            _enviar(self.proc.stdin, {"codigo": codigo, "cfg": cfg})
            r = _receber(self.proc.stdout)
        except (BrokenPipeError, OSError):
            r = None
        if r is None:
            self.fechar()
            return {"status": "MORTO", "msg": "servidor caiu"}
        return r

    def fechar(self):
        if self.proc:
            try:
                self.proc.stdin.close()
                self.proc.wait(timeout=5)
            except Exception:  # noqa: BLE001
                self.proc.kill()
            self.proc = None


def assinatura(r):
    """Identidade de uma falha: status + exceção + local do código onde ocorreu."""
    if r["status"] == "TIMEOUT":
        if r.get("laco_do_programa"):
            return "TIMEOUT|laco-do-programa"
        return f"TIMEOUT|{r.get('local', '?')}"
    if r["status"] in ("MORTO", "MEMORIA"):
        return f"{r['status']}|{r.get('msg', '')}"
    return f"{r['status']}|{r.get('exc', '')}|{r.get('local', '?')}"


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--servidor":
        _servidor(sys.argv[2])
        sys.exit(0)
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--timeout", type=float, default=PADRAO_TIMEOUT)
    ap.add_argument("--memoria-mb", type=int, default=PADRAO_MEMORIA_MB)
    ap.add_argument("arquivos", nargs="+")
    a = ap.parse_args()
    with Executor(a.repo, a.timeout, a.memoria_mb) as ex:
        for arq in a.arquivos:
            with open(arq, encoding="utf-8") as f:
                r = ex.rodar(f.read())
            print(arq, json.dumps({k: v for k, v in r.items() if k != "cobertura"}, ensure_ascii=False))
