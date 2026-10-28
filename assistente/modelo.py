"""Clientes de modelo de linguagem.

ModeloHTTP fala com qualquer servidor compativel com a API de chat da
OpenAI (Ollama, llama.cpp server, vLLM), rodando na propria maquina.
Configuracao por variaveis de ambiente:

    GURU_MODELO_URL   ex.: http://127.0.0.1:11434/v1  (Ollama)
    GURU_MODELO_NOME  ex.: qwen3:1.7b
    GURU_SEM_RACIOCINIO=1  pede ao modelo (Qwen3) que nao gere o bloco
                           de raciocinio, reduzindo a latencia
    GURU_MODELO_API_KEY    chave de API (opcional), enviada como
                           "Authorization: Bearer"; nunca aparece em
                           mensagens de erro nem em registros
    GURU_MODELO_TEMPO      tempo limite por pedido, em segundos (120)
    GURU_MODELO_MAX_TOKENS teto de tokens da resposta (700). Em modelos
                           que raciocinam, os tokens de raciocinio contam
                           dentro deste teto: use um valor alto.

O cabecalho User-Agent e sempre explicito: alguns provedores atras de
CDN recusam o User-Agent padrao do urllib.

O bloco <think>...</think>, quando vier, e sempre removido da resposta.
"""

import json
import os
import re
import urllib.error
import urllib.request

USER_AGENT = "GuruDev-Assistente/0.2 (+https://hubstry.dev)"
RACIOCINIO = re.compile(r"<think>.*?</think>\s*", re.S)


def limpar(texto):
    return RACIOCINIO.sub("", texto).strip()


class ErroModelo(RuntimeError):
    pass


def _numero_env(nome, padrao, tipo):
    valor = os.environ.get(nome, "").strip()
    if not valor:
        return padrao
    try:
        numero = tipo(valor)
    except ValueError as e:
        raise ErroModelo(f"{nome} invalido: {valor!r}") from e
    if numero <= 0:
        raise ErroModelo(f"{nome} deve ser positivo")
    return numero


class ModeloHTTP:
    def __init__(self, url=None, nome=None, tempo_limite=None,
                 sem_raciocinio=None, api_key=None, max_tokens=None,
                 temperatura=0.2, user_agent=USER_AGENT,
                 rejeitar_truncada=False):
        self.url = (url or os.environ.get("GURU_MODELO_URL", "")).rstrip("/")
        self.nome = nome or os.environ.get("GURU_MODELO_NOME", "")
        self.tempo_limite = tempo_limite or _numero_env(
            "GURU_MODELO_TEMPO", 120, float)
        self.max_tokens = max_tokens or _numero_env(
            "GURU_MODELO_MAX_TOKENS", 700, int)
        self.temperatura = temperatura
        self.user_agent = user_agent
        self.rejeitar_truncada = rejeitar_truncada
        # guardada em atributo privado e fora do repr: nao vaza em logs
        self._api_key = api_key or os.environ.get("GURU_MODELO_API_KEY", "")
        if sem_raciocinio is None:
            sem_raciocinio = os.environ.get("GURU_SEM_RACIOCINIO") == "1"
        self.sem_raciocinio = sem_raciocinio
        if not self.url or not self.nome:
            raise ErroModelo(
                "modelo nao configurado: defina GURU_MODELO_URL e "
                "GURU_MODELO_NOME"
            )

    def __repr__(self):
        return f"ModeloHTTP(url={self.url!r}, nome={self.nome!r})"

    def _cabecalhos(self):
        cab = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if self._api_key:
            cab["Authorization"] = "Bearer " + self._api_key
        return cab

    def gerar(self, mensagens, max_tokens=None):
        max_tokens = max_tokens or self.max_tokens
        if self.sem_raciocinio:
            mensagens = [dict(m) for m in mensagens]
            mensagens[-1]["content"] += "\n/no_think"
        corpo = json.dumps(
            {
                "model": self.nome,
                "messages": mensagens,
                "temperature": self.temperatura,
                "max_tokens": max_tokens,
                "stream": False,
            }
        ).encode("utf-8")
        pedido = urllib.request.Request(
            self.url + "/chat/completions",
            data=corpo,
            headers=self._cabecalhos(),
        )
        try:
            with urllib.request.urlopen(
                pedido, timeout=self.tempo_limite
            ) as r:
                dados = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # so o codigo HTTP: o corpo pode ecoar dados do pedido
            raise ErroModelo(f"o modelo respondeu HTTP {e.code}") from None
        except Exception as e:  # rede, tempo, JSON
            raise ErroModelo(
                f"falha ao consultar o modelo: {type(e).__name__}"
            ) from None
        try:
            escolha = dados["choices"][0]
            conteudo = escolha["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise ErroModelo("resposta do modelo em formato inesperado") from e
        if not isinstance(conteudo, str):
            raise ErroModelo("resposta do modelo em formato inesperado")
        if self.rejeitar_truncada and escolha.get("finish_reason") == "length":
            raise ErroModelo(
                "resposta truncada pelo limite de tokens "
                f"(max_tokens={max_tokens})"
            )
        return limpar(conteudo)


class ModeloSimulado:
    """Modelo de teste: devolve respostas fixas, registra o que recebeu."""

    def __init__(self, resposta):
        self.resposta = resposta
        self.recebido = []

    def gerar(self, mensagens, max_tokens=None):
        self.recebido.append(mensagens)
        if callable(self.resposta):
            return self.resposta(mensagens)
        return self.resposta
