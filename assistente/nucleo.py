"""Nucleo do Assistente GuruDev.

Fluxo: pergunta -> politica (POL-03) -> recuperacao na base ->
modelo gera resposta/codigo -> politica (POL-01/03) -> execucao
isolada -> resposta com fontes e estado.

O modelo e gerador; a politica e o runtime sao a autoridade.
"""

import re
from dataclasses import asdict, dataclass, field

from assistente import executor, politica
from assistente.recuperacao import Buscador, carregar_base

INSTRUCOES = """Voce e o Assistente GuruDev, que explica e escreve codigo \
na linguagem de programacao GuruDev.

Regras:
1. Responda somente com base nas FICHAS fornecidas. Se as fichas nao \
cobrirem a pergunta, diga que nao ha informacao na documentacao.
2. Cada ficha tem um estado: "roda_hoje" (executa no interpretador \
atual), "em_reimplementacao" (ainda nao funciona) ou "documental" \
(descrito na documentacao, sem garantia de que executa). Nunca diga \
que algo "em_reimplementacao" ou apenas "documental" funciona hoje.
3. Cite as fichas usadas pelo identificador, por exemplo [F0012].
4. Quando escrever codigo GuruDev, coloque-o em UM bloco ```guru e use \
apenas construcoes que rodam hoje:
   - saida: escrever("texto", valor);
   - tipos: String, Int, Float, Bool, Array; instrucoes terminam em ;
   - funcao: NOM funcao nome(Int a) -> Int { return a; }
   - classe: NOM classe Nome { String campo; NOM funcao iniciar(String c) \
{ this.campo = c; } }  e  Nome x = Nome("valor");
   - controle: if (...) { } else { }, while (...) { }, for (Int x : lista) { }
   - nativas: absoluto(), raiz(), arredondar(), tamanho(), \
converter_string()
   - metodos de texto: t.trim(), t.maiusculo(), t.minusculo() \
(um metodo por instrucao; encadeamento esta em reimplementacao)
   - Nao use Math, Texto, NOM.versao(), VOC.ler() nem literal de objeto {}.
5. Nao inclua subescritas (codigo de outra linguagem) a menos que o \
usuario peca; se pedir, explique que a demo publica nao as executa.
6. Responda em portugues, de forma curta e direta.
"""

BLOCO = re.compile(r"```[^\n]*\n(.*?)```", re.S)


@dataclass
class Resposta:
    texto: str = ""
    fontes: list = field(default_factory=list)
    codigo: str = ""
    execucao: dict = None
    politica: dict = None

    def como_dict(self):
        return asdict(self)


def formatar_fichas(fichas, limite=1500):
    partes = []
    for f in fichas:
        texto = f["texto"]
        if len(texto) > limite:
            texto = texto[:limite] + " [...]"
        partes.append(
            f"[{f['id']}] {f['fonte']} > {f['secao']} "
            f"(estado: {f['estado']})\n{texto}"
        )
    return "\n\n".join(partes)


def extrair_codigo(texto):
    m = BLOCO.search(texto)
    return m.group(1).strip() if m else ""


class Assistente:
    def __init__(self, modelo, buscador=None, k=4):
        self.modelo = modelo
        self.buscador = buscador or Buscador(carregar_base())
        self.k = k

    def responder(self, pergunta, executar=True):
        decisao = politica.avaliar_pergunta(pergunta)
        if not decisao.permitido:
            return Resposta(
                texto=f"Pergunta recusada ({decisao.regra}): "
                f"{decisao.motivo}.",
                politica={"regra": decisao.regra, "motivo": decisao.motivo},
            )
        fichas = self.buscador.buscar(pergunta, k=self.k)
        mensagens = [
            {"role": "system", "content": INSTRUCOES},
            {
                "role": "user",
                "content": "FICHAS:\n\n"
                + (formatar_fichas(fichas) or "(nenhuma ficha encontrada)")
                + f"\n\nPERGUNTA: {pergunta}",
            },
        ]
        texto = self.modelo.gerar(mensagens)
        resposta = Resposta(
            texto=texto,
            fontes=[
                {k: f[k] for k in ("id", "fonte", "secao", "estado")}
                for f in fichas
            ],
            codigo=extrair_codigo(texto),
        )
        if resposta.codigo and executar:
            decisao = politica.avaliar_codigo(resposta.codigo)
            if decisao.permitido:
                resposta.execucao = executor.executar(resposta.codigo)
            else:
                resposta.politica = {
                    "regra": decisao.regra,
                    "motivo": decisao.motivo,
                }
        return resposta
