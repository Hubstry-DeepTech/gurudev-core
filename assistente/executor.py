"""Execucao isolada de codigo GuruDev ja aprovado pela politica.

O codigo roda em processo separado, em diretorio temporario, sem
entrada padrao, com ambiente minimo, limite de tempo e de saida e,
em Linux, limites de memoria, CPU e tamanho de arquivo.

Isto nao substitui um sandbox de sistema operacional: na maquina da
demo, o servico deve rodar com usuario sem privilegios.
"""

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from assistente import politica

RAIZ = Path(__file__).resolve().parent.parent


def _limites():  # pragma: no cover - depende do sistema operacional
    try:
        import resource
    except ImportError:
        return
    resource.setrlimit(resource.RLIMIT_AS, (512 * 2**20, 512 * 2**20))
    tempo = politica.TEMPO_LIMITE + 1
    resource.setrlimit(resource.RLIMIT_CPU, (tempo, tempo))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2**20, 2**20))


def _cortar(texto):
    if len(texto) > politica.MAX_SAIDA:
        return texto[: politica.MAX_SAIDA] + "\n[saida truncada]"
    return texto


def executar(codigo, tempo_limite=None):
    """Executa codigo GuruDev. Retorna dict com ok, saida, erro e tempo.

    Recusa (sem executar) o que a politica nao permitir.
    """
    decisao = politica.avaliar_codigo(codigo)
    if not decisao.permitido:
        return {
            "ok": False,
            "executado": False,
            "saida": "",
            "erro": f"{decisao.regra}: {decisao.motivo}",
            "tempo": 0.0,
        }
    limite = tempo_limite or politica.TEMPO_LIMITE
    ambiente = {
        "PATH": os.environ.get("PATH", ""),
        "LANG": "C.UTF-8",
        "PYTHONIOENCODING": "utf-8",
    }
    with tempfile.TemporaryDirectory(prefix="guru_") as pasta:
        arquivo = Path(pasta) / "programa.guru"
        arquivo.write_text(codigo + "\n", "utf-8")
        inicio = time.monotonic()
        try:
            r = subprocess.run(
                [sys.executable, "-E", "-s", "-m", "src.cli", "run",
                 str(arquivo)],
                cwd=RAIZ,
                env=ambiente,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=limite,
                preexec_fn=_limites if os.name == "posix" else None,
            )
        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "executado": True,
                "saida": "",
                "erro": f"POL-03: tempo limite de {limite} s excedido",
                "tempo": round(time.monotonic() - inicio, 3),
            }
        return {
            "ok": r.returncode == 0,
            "executado": True,
            "saida": _cortar(r.stdout),
            "erro": _cortar(r.stderr.strip()),
            "tempo": round(time.monotonic() - inicio, 3),
        }
