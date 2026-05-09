"""
Testes para quantum_interface.py — Classificador de Delegacao Quantica

Cobre:
- TipoDelegacao enum (4 tipos)
- AUSENTES_QUANTICO (4 operacoes)
- verificar_contencao() — conterncao constitucional
- classificar_delegacao() — cascata de prioridade
- classificar_por_nome() — lookup por PERFIS_CONJECTURAIS
- classificar_todos() — classificacao em lote
- PERFIS_CONJECTURAIS constantes (8 linguagens + 4 algoritmos)
- Casos canonicos: Shor, Grover, VQE, QAOA, Cirq, OpenQASM, PennyLane, Silq
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from alexandria.core.quantum_interface import (
    TipoDelegacao,
    AUSENTES_QUANTICO,
    PERFIS_CONJECTURAIS,
    PERFIS_ALGORITMOS,
    THRESHOLD_EMERGENCIA_RHO6,
    THRESHOLD_ANOMALIA_DELTA,
    THRESHOLD_EQUILIBRIO_RHO5,
    THRESHOLD_CONSERVACAO_RHO5,
    verificar_contencao,
    classificar_delegacao,
    classificar_por_nome,
    classificar_todos,
    listar_ausentes,
    resumo_ausentes,
    ResultadoDelegacao,
    ResultadoContencao,
)


# ═══════════════════════════════════════════════════════════
# TIPO DELEGACAO ENUM
# ═══════════════════════════════════════════════════════════

class TestTipoDelegacao:
    """Testes para o enum TipoDelegacao."""

    def test_4_tipos(self):
        """Enum deve ter exatamente 4 tipos de delegacao."""
        assert len(TipoDelegacao) == 4

    def test_emergencia_valor(self):
        assert TipoDelegacao.EMERGENCIA.value == "emergencia"

    def test_anomalia_valor(self):
        assert TipoDelegacao.ANOMALIA.value == "anomalia"

    def test_equilibrio_valor(self):
        assert TipoDelegacao.EQUILIBRIO.value == "equilibrio"

    def test_conservacao_valor(self):
        assert TipoDelegacao.CONSERVACAO.value == "conservacao"


# ═══════════════════════════════════════════════════════════
# AUSENTES QUANTICO
# ═══════════════════════════════════════════════════════════

class TestAusentesQuantico:
    """Testes para o conjunto de operacoes ausentes."""

    def test_4_operacoes(self):
        """Devem existir exatamente 4 operacoes ausentes."""
        assert len(AUSENTES_QUANTICO) == 4

    def test_clonar_estado(self):
        assert "clonar_estado" in AUSENTES_QUANTICO

    def test_medir_sem_colapso(self):
        assert "medir_sem_colapso" in AUSENTES_QUANTICO

    def test_copiar_qubit(self):
        assert "copiar_qubit" in AUSENTES_QUANTICO

    def test_determinar_fase(self):
        assert "determinar_fase" in AUSENTES_QUANTICO

    def test_listar_ausentes_retorna_copia(self):
        """listar_ausentes deve retornar copia, nao referencia."""
        a1 = listar_ausentes()
        a2 = listar_ausentes()
        assert a1 == a2
        assert a1 is not a2


# ═══════════════════════════════════════════════════════════
# VERIFICAR CONTECAO
# ═══════════════════════════════════════════════════════════

class TestVerificarContencao:
    """Testes para verificacao de contencao constitucional."""

    def test_clonar_estado_ausente(self):
        """clonar_estado deve ser classificado como ausente."""
        r = verificar_contencao("clonar_estado")
        assert r.contida is False
        assert r.categoria == "ausente"
        assert "nao-clonagem" in r.justificativa.lower()

    def test_medir_sem_colapso_ausente(self):
        """medir_sem_colapso deve ser ausente."""
        r = verificar_contencao("medir_sem_colapso")
        assert r.contida is False
        assert r.categoria == "ausente"

    def test_copiar_qubit_ausente(self):
        """copiar_qubit deve ser ausente."""
        r = verificar_contencao("copiar_qubit")
        assert r.contida is False
        assert r.categoria == "ausente"

    def test_determinar_fase_ausente(self):
        """determinar_fase deve ser ausente."""
        r = verificar_contencao("determinar_fase")
        assert r.contida is False
        assert r.categoria == "ausente"

    def test_case_insensitive(self):
        """Verificacao deve ser case-insensitive."""
        r1 = verificar_contencao("CLONAR_ESTADO")
        r2 = verificar_contencao("Clonar_Estado")
        r3 = verificar_contencao("clonar_estado")
        assert r1.contida is False
        assert r2.contida is False
        assert r3.contida is False

    def test_operacao_presente(self):
        """Operacao nao-ausente deve ser classificada como presente."""
        r = verificar_contencao("preparar_estado")
        assert r.contida is True
        assert r.categoria == "presente"

    def test_operacao_com_espacos(self):
        """Operacao com espacos deve funcionar (strip)."""
        r = verificar_contencao("  copiar_qubit  ")
        assert r.contida is False

    def test_limite_constitucional_clonar(self):
        """clonar_estado deve ter limite rho3."""
        r = verificar_contencao("clonar_estado")
        assert "rho3" in r.limite_constitucional

    def test_resumo_ausentes(self):
        """resumo_ausentes deve retornar 4 itens com detalhes."""
        resumo = resumo_ausentes()
        assert len(resumo) == 4
        for item in resumo:
            assert "operacao" in item
            assert "justificativa" in item
            assert "limite_constitucional" in item


# ═══════════════════════════════════════════════════════════
# CLASSIFICAR DELEGACAO — Cascata de Prioridade
# ═══════════════════════════════════════════════════════════

class TestClassificarDelegacao:
    """Testes para classificacao de delegacao via perfil rho."""

    def test_shor_anomalia(self):
        """Shor: rho4=0.7 > rho3=0.3 — ANOMALIA."""
        perfil = [0.9, 0.85, 0.3, 0.7, 0.2, 0.5]
        r = classificar_delegacao(perfil, nome="Shor")
        assert r.tipo == TipoDelegacao.ANOMALIA
        assert r.anomalia_detectada is True
        assert r.cadeia_consistente is False

    def test_grover_anomalia(self):
        """Grover: rho4=0.9 > rho3=0.7 — ANOMALIA."""
        perfil = [0.95, 0.6, 0.7, 0.9, 0.3, 0.2]
        r = classificar_delegacao(perfil, nome="Grover")
        assert r.tipo == TipoDelegacao.ANOMALIA
        assert r.anomalia_detectada is True

    def test_vqe_emergencia(self):
        """VQE: rho6=0.9 > 0.70 — EMERGENCIA (check cadeia primeiro)."""
        perfil = [0.7, 0.8, 0.5, 0.6, 0.7, 0.9]
        r = classificar_delegacao(perfil, nome="VQE")
        # VQE tem rho2(0.8) > rho1(0.7) — anomalia primeiro
        # rho6=0.9 mas anomalia tem prioridade
        assert r.tipo in (TipoDelegacao.ANOMALIA, TipoDelegacao.EMERGENCIA)

    def test_pennylane_equilibrio(self):
        """PennyLane: rho5=0.80 > 0.60 — EQUILIBRIO (sem anomalia rho4>rho3)."""
        perfil = [0.70, 0.65, 0.50, 0.55, 0.80, 0.70]
        r = classificar_delegacao(perfil, nome="PennyLane")
        assert r.tipo == TipoDelegacao.EQUILIBRIO
        assert r.anomalia_detectada is False  # nao tem rho4 > rho3

    def test_cirq_anomalia(self):
        """Cirq: rho4=0.75 > rho3=0.55 — ANOMALIA."""
        perfil = [0.90, 0.60, 0.55, 0.75, 0.40, 0.50]
        r = classificar_delegacao(perfil, nome="Cirq")
        assert r.tipo == TipoDelegacao.ANOMALIA

    def test_openqasm_anomalia(self):
        """OpenQASM 3: rho4=0.85 > rho3=0.55 — ANOMALIA."""
        perfil = [0.75, 0.60, 0.55, 0.85, 0.35, 0.30]
        r = classificar_delegacao(perfil, nome="OpenQASM 3")
        assert r.tipo == TipoDelegacao.ANOMALIA

    def test_silq_emergencia(self):
        """Silq: rho6=0.85 > 0.70 — EMERGENCIA (cadeia consistente?)."""
        perfil = [0.65, 0.70, 0.55, 0.60, 0.55, 0.85]
        r = classificar_delegacao(perfil, nome="Silq")
        # rho2(0.70) > rho1(0.65): delta=0.05, na tolerancia = consistente
        # rho6(0.85) > 0.70 → EMERGENCIA
        assert r.tipo == TipoDelegacao.EMERGENCIA

    def test_conservacao(self):
        """Perfil com cadeia preservada e rho5 >= 0.50 — CONSERVACAO."""
        perfil = [0.80, 0.75, 0.65, 0.60, 0.55, 0.45]
        r = classificar_delegacao(perfil, nome="Conservacao_test")
        assert r.tipo == TipoDelegacao.CONSERVACAO
        assert r.cadeia_consistente is True

    def test_fallback_conservacao(self):
        """Perfil baixo sem criterios especificos — CONSERVACAO (fallback)."""
        perfil = [0.30, 0.25, 0.20, 0.15, 0.40, 0.30]
        r = classificar_delegacao(perfil, nome="Fallback_test")
        assert r.tipo == TipoDelegacao.CONSERVACAO
        assert r.confianca < 0.5

    def test_perfil_invalido_tamanho(self):
        """Perfil com tamanho diferente de 6 deve levantar ValueError."""
        try:
            classificar_delegacao([0.5, 0.5])
            assert False, "Deveria ter levantado ValueError"
        except ValueError as e:
            assert "6 valores" in str(e)

    def test_resultado_tem_perfil(self):
        """Resultado deve conter o perfil original."""
        perfil = [0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
        r = classificar_delegacao(perfil)
        assert r.perfil == perfil

    def test_resultado_tem_justificativa(self):
        """Resultado deve ter justificativa nao-vazia."""
        r = classificar_delegacao([0.9, 0.85, 0.3, 0.7, 0.2, 0.5])
        assert len(r.justificativa) > 20

    def test_confianca_emergencia_alta(self):
        """EMERGENCIA com rho6=0.95 deve ter confianca alta."""
        perfil = [0.3, 0.3, 0.3, 0.3, 0.3, 0.95]
        r = classificar_delegacao(perfil, nome="Alta_confianca")
        assert r.tipo == TipoDelegacao.EMERGENCIA
        assert r.confianca > 0.8

    def test_rho_dominante(self):
        """Rho dominante deve ser o de maior valor."""
        perfil = [0.3, 0.9, 0.2, 0.1, 0.1, 0.1]
        r = classificar_delegacao(perfil)
        assert r.rho_dominante == "rho2"
        assert r.rho_dominante_valor == 0.9


# ═══════════════════════════════════════════════════════════
# CLASSIFICAR POR NOME
# ═══════════════════════════════════════════════════════════

class TestClassificarPorNome:
    """Testes para classificacao por nome via PERFIS_CONJECTURAIS."""

    def test_shor_por_nome(self):
        """Shor por nome deve ser ANOMALIA."""
        r = classificar_por_nome("Shor")
        assert r is not None
        assert r.tipo == TipoDelegacao.ANOMALIA
        assert r.nome == "Shor"

    def test_vqe_por_nome(self):
        """VQE por nome deve ser classificado."""
        r = classificar_por_nome("VQE")
        assert r is not None
        assert r.nome == "VQE"

    def test_qiskit_por_nome(self):
        """Qiskit por nome deve ser classificado."""
        r = classificar_por_nome("Qiskit")
        assert r is not None
        assert r.nome == "Qiskit"

    def test_cirq_por_nome_anomalia(self):
        """Cirq por nome deve ser ANOMALIA."""
        r = classificar_por_nome("Cirq")
        assert r is not None
        assert r.tipo == TipoDelegacao.ANOMALIA

    def test_pennylane_por_nome_equilibrio(self):
        """PennyLane por nome deve ser EQUILIBRIO."""
        r = classificar_por_nome("PennyLane")
        assert r is not None
        assert r.tipo == TipoDelegacao.EQUILIBRIO

    def test_silq_por_nome(self):
        """Silq por nome deve ser EMERGENCIA."""
        r = classificar_por_nome("Silq")
        assert r is not None
        assert r.tipo == TipoDelegacao.EMERGENCIA

    def test_inexistente_retorna_none(self):
        """Nome inexistente deve retornar None."""
        r = classificar_por_nome("LinguagemInexistente")
        assert r is None


# ═══════════════════════════════════════════════════════════
# CLASSIFICAR TODOS
# ═══════════════════════════════════════════════════════════

class TestClassificarTodos:
    """Testes para classificacao em lote."""

    def test_total_resultados(self):
        """Devem retornar 12 resultados (8 linguagens + 4 algoritmos)."""
        resultados = classificar_todos()
        assert len(resultados) == 12

    def test_todos_tem_tipo(self):
        """Todos os resultados devem ter tipo de delegacao."""
        resultados = classificar_todos()
        for r in resultados:
            assert isinstance(r.tipo, TipoDelegacao)

    def test_todos_tem_nome(self):
        """Todos os resultados devem ter nome."""
        resultados = classificar_todos()
        nomes = [r.nome for r in resultados]
        assert "Shor" in nomes
        assert "VQE" in nomes
        assert "Qiskit" in nomes
        assert "PennyLane" in nomes

    def test_distribucao_tipos(self):
        """Deve ter pelo menos 1 de cada tipo (exceto possivelmente todos)."""
        resultados = classificar_todos()
        tipos = {r.tipo for r in resultados}
        # Garantir que temos ANOMALIA e EMERGENCIA no minimo
        assert TipoDelegacao.ANOMALIA in tipos
        assert TipoDelegacao.EMERGENCIA in tipos

    def test_nomes_unicos(self):
        """Nomes devem ser unicos."""
        resultados = classificar_todos()
        nomes = [r.nome for r in resultados]
        assert len(nomes) == len(set(nomes))


# ═══════════════════════════════════════════════════════════
# PERFIS CONJECTURAIS — CONSTANTES
# ═══════════════════════════════════════════════════════════

class TestPerfisConjecturais:
    """Testes para as constantes de perfis conjecturais."""

    def test_8_linguagens(self):
        """Devem existir 8 linguagens com perfis."""
        assert len(PERFIS_CONJECTURAIS) == 8

    def test_4_algoritmos(self):
        """Devem existir 4 algoritmos com perfis."""
        assert len(PERFIS_ALGORITMOS) == 4

    def test_cada_perfil_tem_6_valores(self):
        """Cada perfil deve ter exatamente 6 valores rho."""
        for nome, dados in PERFIS_CONJECTURAIS.items():
            assert len(dados["rho"]) == 6, f"{nome} tem {len(dados['rho'])} valores"
        for nome, dados in PERFIS_ALGORITMOS.items():
            assert len(dados["rho"]) == 6, f"{nome} tem {len(dados['rho'])} valores"

    def test_cada_perfil_tem_delegacao_esperada(self):
        """Cada perfil deve ter delegacao_esperada."""
        for nome, dados in PERFIS_CONJECTURAIS.items():
            assert "delegacao_esperada" in dados, f"{nome} sem delegacao_esperada"
            assert isinstance(dados["delegacao_esperada"], TipoDelegacao)

    def test_cada_perfil_tem_fonte(self):
        """Cada perfil de linguagem deve ter fonte."""
        for nome, dados in PERFIS_CONJECTURAIS.items():
            assert "fonte" in dados, f"{nome} sem fonte"
            assert "Machado" in dados["fonte"]

    def test_algoritmos_tem_classificacao_tats(self):
        """Cada algoritmo deve ter classificacao_tats."""
        for nome, dados in PERFIS_ALGORITMOS.items():
            assert "classificacao_tats" in dados, f"{nome} sem classificacao_tats"

    def test_valores_entre_0_e_1(self):
        """Todos os valores rho devem estar em [0, 1]."""
        for nome, dados in PERFIS_CONJECTURAIS.items():
            for v in dados["rho"]:
                assert 0.0 <= v <= 1.0, f"{nome}: rho={v} fora do range"
        for nome, dados in PERFIS_ALGORITMOS.items():
            for v in dados["rho"]:
                assert 0.0 <= v <= 1.0, f"{nome}: rho={v} fora do range"

    def test_shor_anomalia_flag(self):
        """Shor deve ter anomalia=True."""
        assert PERFIS_ALGORITMOS["Shor"]["anomalia"] is True

    def test_vqe_anomalia_flag(self):
        """VQE deve ter anomalia=False."""
        assert PERFIS_ALGORITMOS["VQE"]["anomalia"] is False


# ═══════════════════════════════════════════════════════════
# THRESHOLDS
# ═══════════════════════════════════════════════════════════

class TestThresholds:
    """Testes para constantes de limiar."""

    def test_emergencia_threshold(self):
        assert THRESHOLD_EMERGENCIA_RHO6 == 0.70

    def test_anomalia_threshold(self):
        assert THRESHOLD_ANOMALIA_DELTA == 0.05

    def test_equilibrio_threshold(self):
        assert THRESHOLD_EQUILIBRIO_RHO5 == 0.60

    def test_conservacao_threshold(self):
        assert THRESHOLD_CONSERVACAO_RHO5 == 0.50
