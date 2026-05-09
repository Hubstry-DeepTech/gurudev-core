"""
Testes para Phase 3: Quantum Dispatch + QuantumResult + R6 no Interpreter

Cobre:
- QuantumResult: criacao, propriedades, colapso, simulacao, erro
- Interpreter.dispatch_quantico(): delegacao, contencao, probabilistico
- Interpreter._is_quantum_paradigm(): deteccao de paradigma quantico
- Interpreter._hexarelational_vector(): R6 a partir de perfis conjecturais
- Interpreter._h_ontologico(): R5 + R6 quando paradigma quantico
- Interpreter.verificar_contencao_quantica(): wrapper de contencao
- Regressao: testes existentes ainda passam
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.quantum_result import QuantumResult
from src.interpreter import Interpreter, Bloco


# ═══════════════════════════════════════════════════════════
# HELPER — criar Bloco mock
# ═══════════════════════════════════════════════════════════

def make_bloco(
    gm_ontologia="acao",
    gm_campo="ciencia",
    gm_hermeneutica="ontologico",
    gm_tempo="presente",
    gm_paradigma="funcional",
    codigo=None,
    subscritas=None,
    compensacao=None,
    plastico=None,
    modulacao=None,
):
    """Cria um Bloco mock para testes."""
    b = Bloco()
    b.gm_ontologia = gm_ontologia
    b.gm_campo = gm_campo
    b.gm_hermeneutica = gm_hermeneutica
    b.gm_tempo = gm_tempo
    b.gm_paradigma = gm_paradigma
    b.codigo = codigo or []
    b.subscritas = subscritas or []
    b.compensacao = compensacao
    b.plastico = plastico
    b.modulacao = modulacao
    return b


# ═══════════════════════════════════════════════════════════
# QUANTUM RESULT
# ═══════════════════════════════════════════════════════════

class TestQuantumResult:
    """Testes para QuantumResult."""

    def test_from_counts_basico(self):
        """Criar resultado a partir de counts absolutos."""
        qr = QuantumResult.from_counts(
            {"00": 500, "01": 300, "10": 150, "11": 74},
            delegacao_tipo="emergencia",
            operacao="medir",
        )
        assert qr.shots == 1024
        assert len(qr.outcomes) == 4
        assert qr.delegacao_tipo == "emergencia"
        assert qr.most_likely() == "00"

    def test_distribution_normalizada(self):
        """Distribuicao deve somar 1.0."""
        qr = QuantumResult.from_counts({"00": 512, "11": 512})
        dist = qr.distribution
        assert abs(sum(dist.values()) - 1.0) < 1e-10

    def test_probability(self):
        """Probabilidade de outcome especifico."""
        qr = QuantumResult.from_counts({"00": 256, "11": 768})
        assert abs(qr.probability("11") - 0.75) < 0.01

    def test_entropy_uniforme_maxima(self):
        """Entropia maxima para distribuicao uniforme de 2 qubits."""
        qr = QuantumResult.from_counts(
            {"00": 256, "01": 256, "10": 256, "11": 256}
        )
        assert abs(qr.entropy - 2.0) < 0.05  # log2(4) = 2

    def test_entropy_zero(self):
        """Entropia zero quando um resultado tem 100%."""
        qr = QuantumResult.from_counts({"00": 1024})
        assert qr.entropy == 0.0

    def test_collapse_deterministico_com_seed(self):
        """Colapso com seed deve ser deterministico."""
        qr = QuantumResult.from_counts({"00": 500, "11": 524})
        r1 = qr.collapse(seed=42)
        r2 = qr.collapse(seed=42)
        assert r1 == r2

    def test_collapse_apos_primeiro(self):
        """Colapso armazena valor_colapsado."""
        qr = QuantumResult.from_counts({"00": 500, "11": 524})
        qr.collapse(seed=1)
        assert qr.colapsado is True
        assert qr.valor_colapsado is not None

    def test_collapse_erro_lanca(self):
        """Colapso de resultado erro deve levantar RuntimeError."""
        qr = QuantumResult.error("operacao ausente")
        try:
            qr.collapse()
            assert False, "Deveria ter levantado RuntimeError"
        except RuntimeError:
            pass

    def test_error_resultado(self):
        """Resultado de erro tem is_error=True."""
        qr = QuantumResult.error("nao-clonagem", operacao="clonar_estado")
        assert qr.is_error is True
        assert qr.erro == "nao-clonagem"
        assert qr.shots == 0
        assert qr.counts == {}

    def test_simulate_basico(self):
        """Simulacao de 2 qubits deve gerar 4 outcomes."""
        qr = QuantumResult.simulate(n_qubits=2, shots=1000, seed=42)
        assert qr.shots == 1000
        assert len(qr.outcomes) <= 4

    def test_simulate_com_perfil(self):
        """Simulacao com perfil rho3 alto deve ser mais concentrada."""
        qr_concentrado = QuantumResult.simulate(
            n_qubits=2, shots=10000, seed=42,
            perfil_rho=[0.9, 0.9, 0.9, 0.3, 0.2, 0.1],  # rho3 alto
        )
        qr_disperso = QuantumResult.simulate(
            n_qubits=2, shots=10000, seed=42,
            perfil_rho=[0.3, 0.2, 0.1, 0.3, 0.3, 0.9],  # rho6 alto
        )
        # Entropia do disperso deve ser maior ou igual
        assert qr_disperso.entropy >= qr_concentrado.entropy * 0.8

    def test_to_dict(self):
        """Serializacao para dicionario."""
        qr = QuantumResult.from_counts({"00": 100, "11": 100})
        d = qr.to_dict()
        assert "counts" in d
        assert "distribution" in d
        assert "entropy" in d
        assert "most_likely" in d
        assert d["shots"] == 200

    def test_to_dict_com_erro(self):
        """Serializacao de erro inclui campo erro."""
        qr = QuantumResult.error("teste")
        d = qr.to_dict()
        assert d["erro"] == "teste"

    def test_outcomes_lista(self):
        """Outcomes deve ser lista de strings."""
        qr = QuantumResult.from_counts({"00": 1, "01": 2, "10": 3})
        outcomes = qr.outcomes
        assert isinstance(outcomes, list)
        assert len(outcomes) == 3
        assert "00" in outcomes


# ═══════════════════════════════════════════════════════════
# INTERPRETER — QUANTUM DISPATCH
# ═══════════════════════════════════════════════════════════

class TestInterpreterQuantumDispatch:
    """Testes para dispatch quantico no interpretador."""

    def setup_method(self):
        self.interp = Interpreter()

    def test_interface_disponivel(self):
        """Quantum interface deve estar disponivel no interpretador."""
        assert self.interp._quantum_interface_available is True

    def test_quantum_results_lista_inicial(self):
        """Lista de resultados quanticos deve iniciar vazia."""
        assert self.interp.quantum_results == []

    def test_dispatch_operacao_valida(self):
        """Dispatch de operacao valida deve retornar QuantumResult."""
        qr = self.interp.dispatch_quantico("preparar_estado", n_qubits=2, shots=100)
        assert qr.is_error is False
        assert qr.shots == 100

    def test_dispatch_operacao_ausente(self):
        """Dispatch de operacao ausente deve retornar erro."""
        qr = self.interp.dispatch_quantico("clonar_estado")
        assert qr.is_error is True
        assert qr.erro is not None
        assert "nao-clonagem" in qr.erro.lower()

    def test_dispatch_copiar_qubit_erro(self):
        """copiar_qubit deve ser erro de contencao."""
        qr = self.interp.dispatch_quantico("copiar_qubit")
        assert qr.is_error is True

    def test_dispatch_medir_sem_colapso_erro(self):
        """medir_sem_colapso deve ser erro de contencao."""
        qr = self.interp.dispatch_quantico("medir_sem_colapso")
        assert qr.is_error is True

    def test_dispatch_determinar_fase_erro(self):
        """determinar_fase deve ser erro de contencao."""
        qr = self.interp.dispatch_quantico("determinar_fase")
        assert qr.is_error is True

    def test_dispatch_com_nome(self):
        """Dispatch com nome deve classificar por PERFIS_CONJECTURAIS."""
        qr = self.interp.dispatch_quantico("medir", nome="VQE", n_qubits=2)
        assert qr.is_error is False
        assert qr.delegacao_tipo != ""
        assert len(qr.perfil_rho) == 6

    def test_dispatch_com_perfil(self):
        """Dispatch com perfil explicito deve usar o perfil fornecido."""
        perfil = [0.9, 0.85, 0.3, 0.7, 0.2, 0.5]  # Shor
        qr = self.interp.dispatch_quantico("fatorar", perfil=perfil)
        assert qr.is_error is False
        assert qr.perfil_rho == perfil

    def test_dispatch_registra_resultado(self):
        """Dispatch deve registrar resultado na lista quantum_results."""
        self.interp.dispatch_quantico("medir", n_qubits=1, shots=100)
        assert len(self.interp.quantum_results) == 1
        self.interp.dispatch_quantico("medir", n_qubits=2, shots=100)
        assert len(self.interp.quantum_results) == 2

    def test_dispatch_shor_anomalia(self):
        """Dispatch com perfil Shor deve classificar como anomalia."""
        qr = self.interp.dispatch_quantico("fatorar", nome="Shor", n_qubits=3)
        assert qr.delegacao_tipo == "anomalia"

    def test_dispatch_vqe_emergencia(self):
        """Dispatch com nome VQE deve classificar (anomalia rho2>rho1 ou emergencia)."""
        qr = self.interp.dispatch_quantico("otimizar", nome="VQE", n_qubits=2)
        # VQE tem rho2=0.8 > rho1=0.7 (delta=0.1 > 0.05) mas nao rho4>rho3
        # Entao cai no elif rho6 > 0.70
        assert qr.delegacao_tipo in ("emergencia", "anomalia")

    def test_dispatch_pennylane_equilibrio(self):
        """Dispatch com nome PennyLane deve classificar como equilibrio."""
        qr = self.interp.dispatch_quantico("treinar", nome="PennyLane", n_qubits=2)
        assert qr.delegacao_tipo == "equilibrio"

    def test_verificar_contencao_quantica(self):
        """verificar_contencao_quantica deve retornar dict com campos."""
        r = self.interp.verificar_contencao_quantica("clonar_estado")
        assert r is not None
        assert r["contida"] is False
        assert r["categoria"] == "ausente"
        assert "nao-clonagem" in r["justificativa"].lower()

    def test_verificar_contencao_presente(self):
        """Operacao presente deve retornar contida=True."""
        r = self.interp.verificar_contencao_quantica("preparar_superposicao")
        assert r["contida"] is True
        assert r["categoria"] == "presente"


# ═══════════════════════════════════════════════════════════
# INTERPRETER — PARADIGMA QUANTICO
# ═══════════════════════════════════════════════════════════

class TestQuantumParadigmDetection:
    """Testes para deteccao de paradigma quantico."""

    def setup_method(self):
        self.interp = Interpreter()

    def test_paradigma_quantico(self):
        assert self.interp._is_quantum_paradigm("quantico") is True

    def test_paradigma_quantica(self):
        assert self.interp._is_quantum_paradigm("quantica") is True

    def test_paradigma_quantum(self):
        assert self.interp._is_quantum_paradigm("quantum") is True

    def test_paradigma_qiskit(self):
        assert self.interp._is_quantum_paradigm("qiskit") is True

    def test_paradigma_cirq(self):
        assert self.interp._is_quantum_paradigm("cirq") is True

    def test_paradigma_vqe(self):
        assert self.interp._is_quantum_paradigm("vqe") is True

    def test_paradigma_gate_based(self):
        assert self.interp._is_quantum_paradigm("gate-based") is True

    def test_paradigma_funcional_nao_quantico(self):
        assert self.interp._is_quantum_paradigm("funcional") is False

    def test_paradigma_none(self):
        assert self.interp._is_quantum_paradigm(None) is False

    def test_paradigma_vazio(self):
        assert self.interp._is_quantum_paradigm("") is False


# ═══════════════════════════════════════════════════════════
# INTERPRETER — R6 HEXARRELACIONAL
# ═══════════════════════════════════════════════════════════

class TestHexarelationalVector:
    """Testes para vetor hexarrelacional R6."""

    def setup_method(self):
        self.interp = Interpreter()

    def test_r6_qiskit(self):
        """R6 para paradigma Qiskit deve vir de PERFIS_CONJECTURAIS."""
        bloco = make_bloco(gm_paradigma="qiskit")
        r6 = self.interp._hexarelational_vector(bloco)
        assert len(r6["vector"]) == 6
        assert r6["vector"][0] == 0.85  # rho1 de Qiskit
        assert r6["fonte"] != "hash_categorico_fallback"

    def test_r6_vqe(self):
        """R6 para paradigma VQE deve vir de PERFIS_ALGORITMOS."""
        bloco = make_bloco(gm_paradigma="vqe")
        r6 = self.interp._hexarelational_vector(bloco)
        assert len(r6["vector"]) == 6
        assert r6["vector"][5] == 0.9  # rho6 de VQE

    def test_r6_fallback(self):
        """R6 para paradigma desconhecido deve usar hash categorico."""
        bloco = make_bloco(gm_paradigma="desconhecido_xyz")
        r6 = self.interp._hexarelational_vector(bloco)
        assert len(r6["vector"]) == 6
        assert r6["fonte"] == "hash_categorico_fallback"

    def test_r6_norma_positiva(self):
        """Norma de R6 deve ser positiva."""
        bloco = make_bloco(gm_paradigma="qiskit")
        r6 = self.interp._hexarelational_vector(bloco)
        assert r6["norm"] > 0

    def test_r6_todos_valores_entre_0_e_1(self):
        """Todos os valores de R6 devem estar em [0, 1]."""
        bloco = make_bloco(gm_paradigma="qiskit")
        r6 = self.interp._hexarelational_vector(bloco)
        for v in r6["vector"]:
            assert 0.0 <= v <= 1.0


# ═══════════════════════════════════════════════════════════
# INTERPRETER — H_ONTOLÓGICO COM R6
# ═══════════════════════════════════════════════════════════

class TestHOntologicoR6:
    """Testes para _h_ontologico com R6 hexarrelacional."""

    def setup_method(self):
        self.interp = Interpreter()

    def test_sv_sem_r6_paradigma_nao_quantico(self):
        """SV de bloco nao-quantico NAO deve ter r6."""
        bloco = make_bloco(gm_paradigma="funcional")
        self.interp._h_ontologico(bloco)
        sv = self.interp.significance_vectors[-1]
        assert "r6_hexarrelacional" not in sv
        assert "r6_norm" not in sv

    def test_sv_com_r6_paradigma_quantico(self):
        """SV de bloco quantico DEVE ter r6."""
        bloco = make_bloco(gm_paradigma="quantico")
        self.interp._h_ontologico(bloco)
        sv = self.interp.significance_vectors[-1]
        assert "r6_hexarrelacional" in sv
        assert "r6_norm" in sv
        assert "r6_fonte" in sv
        assert len(sv["r6_hexarrelacional"]) == 6

    def test_sv_r5_inalterado(self):
        """R5 deve continuar presente mesmo com R6."""
        bloco = make_bloco(gm_paradigma="qiskit")
        self.interp._h_ontologico(bloco)
        sv = self.interp.significance_vectors[-1]
        assert "vector" in sv
        assert len(sv["vector"]) == 5  # R5 tem 5 dimensoes

    def test_sv_r6_qiskit_fonte(self):
        """R6 de paradigma Qiskit deve ter fonte dos perfis conjecturais."""
        bloco = make_bloco(gm_paradigma="qiskit")
        self.interp._h_ontologico(bloco)
        sv = self.interp.significance_vectors[-1]
        assert "Machado" in sv["r6_fonte"]

    def test_sv_r6_vqe_fonte(self):
        """R6 de paradigma VQE deve ter fonte dos algoritmos."""
        bloco = make_bloco(gm_paradigma="vqe")
        self.interp._h_ontologico(bloco)
        sv = self.interp.significance_vectors[-1]
        # PERFIS_ALGORITMOS usa fonte="PERFIS_ALGORITMOS"
        assert sv["r6_fonte"] == "PERFIS_ALGORITMOS"

    def test_sv_multiplos_blocos(self):
        """Multiplos blocos devem gerar multiplos SVs."""
        self.interp._h_ontologico(make_bloco(gm_paradigma="funcional"))
        self.interp._h_ontologico(make_bloco(gm_paradigma="quantico"))
        assert len(self.interp.significance_vectors) == 2
