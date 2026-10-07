"""Clientes de modelo de linguagem.

ModeloHTTP fala com qualquer servidor compativel com a API de chat da
OpenAI (Ollama, llama.cpp server, vLLM), rodando na propria maquina.
Configuracao por variaveis de ambiente:

    GURU_MODELO_URL   ex.: http://127.0.0.1:11434/v1  (Ollama)
    GURU_MODELO_NOME  ex.: qwen3:1.7b
    GURU_SEM_RACIOCINIO=1  pede ao modelo (Qwen3) que nao gere o bloco
                           de raciocinio, reduzindo a latencia

O bloco <think>...</think>, quando vier, e sempre removido da resposta.
"""

import json
import os
import re
import urllib.request

RACIOCINIO = re.compile(r"<think>.*?</think>\s*", re.S)


def limpar(texto):
    return RACIOCINIO.sub("", texto).strip()


class ErroModelo(RuntimeError):
    pass


class ModeloHTTP:
    def __init__(self, url=None, nome=None, tempo_limite=120,
                 sem_raciocinio=None):
        self.url = (url or os.environ.get("GURU_MODELO_URL", "")).rstrip("/")
        self.nome = nome or os.environ.get("GURU_MODELO_NOME", "")
        self.tempo_limite = tempo_limite
        if sem_raciocinio is None:
            sem_raciocinio = os.environ.get("GURU_SEM_RACIOCINIO") == "1"
        self.sem_raciocinio = sem_raciocinio
        if not self.url or not self.nome:
            raise ErroModelo(
                "modelo nao configurado: defina GURU_MODELO_URL e "
                "GURU_MODELO_NOME"
            )

    def gerar(self, mensagens, max_tokens=700):
        if self.sem_raciocinio:
            mensagens = [dict(m) for m in mensagens]
            mensagens[-1]["content"] += "\n/no_think"
        corpo = json.dumps(
            {
                "model": self.nome,
                "messages": mensagens,
                "temperature": 0.2,
                "max_tokens": max_tokens,
                "stream": False,
            }
        ).encode("utf-8")
        pedido = urllib.request.Request(
            self.url + "/chat/completions",
            data=corpo,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(
                pedido, timeout=self.tempo_limite
            ) as r:
                dados = json.loads(r.read().decode("utf-8"))
        except Exception as e:  # rede, tempo, JSON
            raise ErroModelo(f"falha ao consultar o modelo: {e}") from e
        try:
            return limpar(dados["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as e:
            raise ErroModelo("resposta do modelo em formato inesperado") from e


class ModeloSimulado:
    """Modelo de teste: devolve respostas fixas, registra o que recebeu."""

    def __init__(self, resposta):
        self.resposta = resposta
        self.recebido = []

    def gerar(self, mensagens, max_tokens=700):
        self.recebido.append(mensagens)
        if callable(self.resposta):
            return self.resposta(mensagens)
        return self.resposta
