"""Gera a base de conhecimento do Assistente GuruDev.

Le os documentos e exemplos selecionados para a fase 1 e produz
`base_conhecimento.json`: uma lista de fichas, cada uma com origem
(arquivo e secao), tipo e estado.

Regra de estado:
- a fonte documental informa o que a GuruDev declara ("documental");
- so evidencia executavel recebe "roda_hoje";
- "em_reimplementacao" vem da secao homonima do README e da lista
  PENDENTES de tests/test_examples.py.

A saida e deterministica (sem datas, ordem fixa), para que o teste
possa verificar se a base esta atualizada em relacao aos documentos.

Uso:  python assistente/gerar_base.py
"""

import ast
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = Path(__file__).resolve().parent / "base_conhecimento.json"

# Documentos da fase 1 (somente portugues).
DOCUMENTOS = [
    "README.md",
    "docs/SINTAXE.md",
    "docs/GRAMMAR_V1_0_0_ALPHA.md",
    "docs/GURU_MATRIX5D.md",
    "docs/BIBLIOTECA_PADRAO.md",
    "docs/EXEMPLOS_VALIDACAO.md",
    "docs/ARQUITETURA_NAMESPACES.md",
    "docs/WHITEPAPER.md",
    "docs/DEMO_ROTEIROS.md",
]

# Secoes de negocio do README ficam fora: o Assistente trata da
# tecnologia, nao representa comercialmente a empresa.
SECOES_EXCLUIDAS = {
    "README.md": [
        "Modelo de negócio",
        "Verticais de Negócio",
        "Como se envolver",
        "Próximos marcos",
        "Para quem",
        "Sobre o Criador",
    ],
}

# Arquivos que nunca entram na base (verificado pelo teste).
ARQUIVOS_PROIBIDOS = [
    "FINANCIAL_MODEL",
    "REVENUE_MODELS",
    "FOUNDER_PROFILE",
    "pitch_decks",
    "roadmap",
]

TITULO = re.compile(r"^(#{1,4})\s+(.*\S)\s*$")
BLOCO_CODIGO = re.compile(r"```[^\n]*\n(.*?)```", re.S)


def pendentes():
    """Le PENDENTES de tests/test_examples.py sem importar o pytest."""
    caminho = RAIZ / "tests" / "test_examples.py"
    arvore = ast.parse(caminho.read_text("utf-8"))
    for no in arvore.body:
        if isinstance(no, ast.Assign) and any(
            getattr(alvo, "id", None) == "PENDENTES" for alvo in no.targets
        ):
            return ast.literal_eval(no.value)
    return {}


def secoes(texto):
    """Divide um markdown em (caminho_de_titulos, conteudo)."""
    caminho, linhas, resultado = [], [], []
    em_codigo = False
    for linha in texto.splitlines():
        if linha.lstrip().startswith("```"):
            em_codigo = not em_codigo
        m = None if em_codigo else TITULO.match(linha)
        if m:
            resultado.append((list(caminho), "\n".join(linhas).strip()))
            nivel = len(m.group(1))
            caminho = caminho[: nivel - 1] + [m.group(2)]
            linhas = []
        else:
            linhas.append(linha)
    resultado.append((list(caminho), "\n".join(linhas).strip()))
    return [(c, t) for c, t in resultado if t]


def excluida(fonte, caminho):
    alvos = SECOES_EXCLUIDAS.get(fonte, [])
    return any(t.startswith(a) for t in caminho for a in alvos)


def fichas_de_documento(fonte):
    fichas = []
    texto = (RAIZ / fonte).read_text("utf-8")
    for caminho, conteudo in secoes(texto):
        if excluida(fonte, caminho):
            continue
        secao = " > ".join(caminho)
        if any(t.startswith("Em reimplementação") for t in caminho):
            estado = "em_reimplementacao"
        else:
            estado = "documental"
        fichas.append(
            {
                "fonte": fonte,
                "secao": secao,
                "tipo": "documentacao",
                "estado": estado,
                "texto": conteudo,
            }
        )
        # Codigo dos roteiros executaveis (R02, R03...) e evidencia
        # verificada: ganha ficha propria com estado "roda_hoje".
        roteiro = caminho[-1] if caminho else ""
        eh_roteiro = re.match(r"R\d\d ", roteiro)
        if fonte == "docs/DEMO_ROTEIROS.md" and eh_roteiro:
            for codigo in BLOCO_CODIGO.findall(conteudo):
                fichas.append(
                    {
                        "fonte": fonte,
                        "secao": secao,
                        "tipo": "codigo_roteiro",
                        "estado": "roda_hoje",
                        "texto": codigo.strip(),
                    }
                )
    return fichas


def fichas_de_exemplos():
    pend = pendentes()
    fichas = []
    for arquivo in sorted((RAIZ / "examples").glob("*.guru")):
        nome = arquivo.name
        fichas.append(
            {
                "fonte": f"examples/{nome}",
                "secao": nome,
                "tipo": "exemplo",
                "estado": (
                    "em_reimplementacao" if nome in pend else "roda_hoje"
                ),
                "texto": arquivo.read_text("utf-8").strip(),
            }
        )
    return fichas


def gerar():
    fichas = []
    for fonte in DOCUMENTOS:
        fichas.extend(fichas_de_documento(fonte))
    fichas.extend(fichas_de_exemplos())
    for i, ficha in enumerate(fichas, 1):
        ficha["id"] = f"F{i:04d}"
    return fichas


def serializar(fichas):
    texto = json.dumps(fichas, ensure_ascii=False, indent=1, sort_keys=True)
    return texto + "\n"


def main():
    fichas = gerar()
    SAIDA.write_text(serializar(fichas), "utf-8")
    estados = {}
    for f in fichas:
        estados[f["estado"]] = estados.get(f["estado"], 0) + 1
    print(f"{len(fichas)} fichas geradas em {SAIDA.name}: {estados}")


if __name__ == "__main__":
    main()
