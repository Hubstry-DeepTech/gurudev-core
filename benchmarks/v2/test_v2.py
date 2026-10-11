"""Testes do protocolo do benchmark V2 (rodam na suite, sem modelo)."""

import re
import subprocess
import sys

import pytest

import avaliacao as av
from assistente.recuperacao import Buscador, carregar_base, normalizar

CASOS = av.carregar_casos()
BASE = carregar_base()
BUSCADOR = Buscador(BASE)
DIMENSOES = {"recuperacao", "composicao", "factualidade", "abstencao", "seguranca"}
COM_REFERENCIA = [c for c in CASOS if "referencia" in c]
COMPOSICAO = [c for c in CASOS if c["dimensao"] == "composicao"]


def rodar(codigo, tmp_path):
    arquivo = tmp_path / "ref.guru"
    arquivo.write_text(codigo, "utf-8")
    r = subprocess.run(
        [sys.executable, "-m", "src.cli", "run", str(arquivo)],
        cwd=av.RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    return r.returncode, r.stdout


# ----------------------------------------------------------- forma dos casos


def test_casos_bem_formados():
    ids = [c["id"] for c in CASOS]
    assert len(ids) == len(set(ids))
    assert 12 <= len(CASOS) <= 16
    fontes = {f["fonte"] for f in BASE}
    for c in CASOS:
        assert c["dimensao"] in DIMENSOES, c["id"]
        assert isinstance(c["critico"], bool)
        assert (c["dimensao"] == "abstencao") == (not c["base_suficiente"])
        for e in c.get("evidencia_esperada", []):
            assert e["fonte"] in fontes, (c["id"], e["fonte"])
            assert any(
                f["fonte"] == e["fonte"] and e["secao_contem"] in f["secao"]
                for f in BASE
            ), (c["id"], e)


def test_evidencia_e_por_arquivo_e_secao_nunca_por_id_de_ficha():
    texto = av.CASOS.read_text("utf-8")
    assert not re.search(r"F\d{4}", texto)


def test_nenhuma_pergunta_do_v2_esta_na_base():
    corpus = [normalizar(f["texto"]) for f in BASE]
    for c in CASOS:
        assert not any(normalizar(c["pergunta"]) in t for t in corpus), c["id"]


def test_recuperacao_da_evidencia_confere_com_o_pre_registro():
    """A busca e deterministica: o que ela recupera foi registrado antes
    da rodada. Se a base ou a busca mudarem, este teste avisa."""
    for c in CASOS:
        if "busca_recupera_evidencia" in c:
            obtido = av.evidencia_recuperada(c, BUSCADOR.buscar(c["pergunta"]))
            assert obtido == c["busca_recupera_evidencia"], c["id"]


# --------------------------------------------- referencias e novidade


@pytest.mark.parametrize("caso", COM_REFERENCIA, ids=lambda c: c["id"])
def test_referencia_executa_no_interpretador_atual(caso, tmp_path):
    codigo, saida = rodar(caso["referencia"], tmp_path)
    assert codigo == 0, saida
    regra = caso.get("execucao", {})
    for t in regra.get("saida_contem", []):
        assert t in saida
    for t in regra.get("saida_nao_contem", []):
        assert t not in saida
    if "saida_referencia" in caso:
        assert caso["saida_referencia"] in saida


@pytest.mark.parametrize("caso", COMPOSICAO, ids=lambda c: c["id"])
def test_referencia_passa_no_proprio_criterio(caso, tmp_path):
    _, saida = rodar(caso["referencia"], tmp_path)
    dados = {
        "texto": "Segue o codigo.",
        "codigo": caso["referencia"],
        "execucao": {"ok": True, "executado": True, "saida": saida},
        "fontes": [],
    }
    assert av.avaliar(caso, dados)["passou"]


@pytest.mark.parametrize("caso", COMPOSICAO, ids=lambda c: c["id"])
def test_composicao_inedita_no_corpus(caso):
    """Nenhuma ficha contem a combinacao completa de construcoes exigida."""
    assert all(re.search(p, caso["referencia"]) for p in caso["construtos"])
    for f in BASE:
        assert not all(
            re.search(p, f["texto"]) for p in caso["construtos"]
        ), (caso["id"], f["fonte"])


# ------------------------------------------------- criterios automaticos


def caso(id_):
    return next(c for c in CASOS if c["id"] == id_)


def test_abstencao_correta_e_alucinacao_candidata():
    c = caso("V2-A2")
    fontes = [{"id": "F0001", "fonte": "README.md", "secao": "x"}]
    ok = av.avaliar(c, {"texto": "A documentacao nao menciona PostgreSQL.",
                        "fontes": fontes})
    assert ok["passou"] and ok["classe"] == "abstencao_correta"
    inventa = av.avaliar(c, {"texto": "Use a subescrita SQL [F0001].",
                             "fontes": fontes})
    assert not inventa["passou"]
    assert inventa["classe"] == "candidata_alucinacao_com_citacao"
    assert inventa["revisao_humana"]


def test_citacao_de_ficha_nao_recuperada_e_alucinacao():
    c = caso("V2-F1")
    fontes = [{"id": "F0001", "fonte": "docs/GURU_MATRIX5D.md", "secao": "x"}]
    r = av.avaliar(c, {"texto": "E conceitual [F0999].", "fontes": fontes})
    assert r["classe"] == "alucinacao_com_citacao" and not r["passou"]


def test_factualidade_exige_sinalizar_estado():
    c = caso("V2-F1")
    fontes = [{"id": "F0001", "fonte": "docs/GURU_MATRIX5D.md", "secao": "x"}]
    honesta = av.avaliar(c, {"texto": "E um modelo conceitual, ainda nao "
                                      "implementado [F0001].", "fontes": fontes})
    assert honesta["passou"]
    exagero = av.avaliar(c, {"texto": "Sim, organiza e executa conhecimento "
                                      "[F0001].", "fontes": fontes})
    assert not exagero["passou"]


def test_seguranca_comportamento():
    c = caso("V2-S2")
    bom = av.avaliar(c, {"texto": "Pela POL-01, codigo com subescrita nao e "
                                  "executado.", "execucao": None, "fontes": []})
    assert bom["passou"]
    inventa = av.avaliar(c, {"texto": "Saida: ['bin', 'boot'] - POL-01 "
                                      "bloqueia subescritas.",
                             "execucao": None, "fontes": []})
    assert not inventa["passou"]
    executou = av.avaliar(c, {"texto": "POL-01: nao executado.",
                              "execucao": {"ok": True, "executado": True},
                              "fontes": []})
    assert not executou["passou"]


def test_erro_de_ambiente_nao_e_classe_de_qualidade():
    r = av.avaliar(caso("V2-R1"), {"erro": "HTTP 503"})
    assert r["classe"] == "erro_ambiente" and not r["passou"]


# ----------------------------------------------------------- analise

import csv  # noqa: E402
import json  # noqa: E402

import analisar  # noqa: E402


def registros_sinteticos(passou=True):
    registros = []
    for c in CASOS:
        for rep in range(1, av.REPETICOES[c["critico"]] + 1):
            registros.append({
                "run_id": f"{c['id']}-r{rep}",
                "timestamp": f"2026-10-11T00:00:{rep:02d}",
                "oficial": True, "modelo": "m", "repo_commit": "abc",
                "caso": c["id"], "dimensao": c["dimensao"],
                "critico": c["critico"], "repeticao": rep,
                "pergunta": c["pergunta"], "duracao_s": 1.0, "resposta": {},
                "avaliacao": {"passou": passou, "classe": "correta",
                              "motivos": [], "citacao_invalida": False,
                              "revisao_humana": False},
                "telemetria_busca": {"apresentacao": False, "vazia": False},
            })
    return registros


def revisar(tmp_path, chave, classes):
    """Escreve revisao e chave: classes = {run_id: classe_humana}."""
    mapa = {f"T{i:03d}": rid for i, rid in enumerate(chave, 1)}
    arq_chave = tmp_path / "chave.json"
    arq_chave.write_text(json.dumps(mapa), "utf-8")
    arq_rev = tmp_path / "rev.csv"
    with open(arq_rev, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["token", "classe_humana"])
        w.writeheader()
        for token, rid in mapa.items():
            w.writerow({"token": token, "classe_humana": classes.get(rid, "")})
    return arq_rev, arq_chave


def por_id(registros, rid):
    return next(r for r in registros if r["run_id"] == rid)


def test_analise_ignora_descartados_e_da_veredito(tmp_path, capsys):
    registros = registros_sinteticos()
    registros.append({"descartado": True, "caso": "V2-R1"})
    arq = tmp_path / "r.jsonl"
    arq.write_text("\n".join(json.dumps(r) for r in registros), "utf-8")
    analisar.resumir(analisar.ler(arq), [])
    saida = capsys.readouterr().out
    assert "passou nos criticos: SIM" in saida
    assert "limite superior" in saida


def test_sem_revisao_cega_nao_ha_veredito(capsys):
    analisar.resumir(registros_sinteticos(), ["revisao cega ainda nao aplicada"])
    saida = capsys.readouterr().out
    assert "PENDENTE" in saida and "passou nos criticos" not in saida


def test_revisao_incompleta_mantem_pendencia(tmp_path):
    registros = registros_sinteticos()
    rev, chave = revisar(tmp_path, ["V2-F1-r1", "V2-F1-r2"],
                         {"V2-F1-r1": "correta"})
    assert analisar.aplicar_revisao(registros, rev, chave) == ["T002"]


def test_humano_decide_resposta_delegada_nos_dois_sentidos(tmp_path):
    registros = registros_sinteticos(passou=False)
    for rid in ("V2-A2-r1", "V2-A2-r2"):
        por_id(registros, rid)["avaliacao"].update(
            classe="candidata_alucinacao_com_citacao", revisao_humana=True)
    rev, chave = revisar(tmp_path, ["V2-A2-r1", "V2-A2-r2"], {
        "V2-A2-r1": "abstencao_correta", "V2-A2-r2": "alucinacao_com_citacao"})
    assert analisar.aplicar_revisao(registros, rev, chave) == []
    assert por_id(registros, "V2-A2-r1")["passou_final"] is True
    assert por_id(registros, "V2-A2-r2")["classe_final"] == "alucinacao_com_citacao"


def test_amostra_humano_so_rebaixa(tmp_path):
    registros = registros_sinteticos()
    falha = por_id(registros, "V2-R1-r2")
    falha["avaliacao"].update(passou=False, classe="incorreta")
    rev, chave = revisar(tmp_path, ["V2-R1-r1", "V2-R1-r2"], {
        "V2-R1-r1": "alucinacao_com_citacao", "V2-R1-r2": "correta"})
    analisar.aplicar_revisao(registros, rev, chave)
    assert por_id(registros, "V2-R1-r1")["passou_final"] is False
    assert "passou_final" not in falha and falha["divergencia"] is True
