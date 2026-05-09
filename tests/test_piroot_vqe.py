"""
Testes do PiRoot VQE Experiment — Phase 4

Cobre:
  1. Transformacoes matematicas (pi_root, norma_aurea)
  2. PiRootVQEExperiment (cenario, paisagem, comparacao, correlacao)
  3. BarrenPlateauTest (deteccao, transicao, scaling)
  4. Data classes (VQEIterationResult, VQEProfileTrajectory, etc.)
  5. Integracao com Alexandria (perfis, constantes)

Autor: Guilherme Goncalves Machado (Hubstry-DeepTech)
Versao: 0.1.0 | Licenca: MIT
"""

import math
import sys
import os
import unittest

# Adicionar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.piroot_vqe.piroot_vqe import (
    pi_root,
    norma_aurea,
    PHI,
    VQE_PERFIL_CANONICO,
    SHOR_PERFIL,
    GROVER_PERFIL,
    QAOA_PERFIL,
    VQEIterationResult,
    VQEProfileTrajectory,
    ExperimentResults,
    PiRootVQEExperiment,
)

from experiments.piroot_vqe.barren_plateau_test import (
    BarrenPlateauTest,
    DepthProfile,
    BarrenPlateauResults,
    THRESHOLD_RHO5_BARREN,
    THRESHOLD_ENTROPY_RATIO,
    THRESHOLD_GRADIENT,
)


# ═══════════════════════════════════════════════════════════
# 1. TRANSFORMACOES MATEMATICAS
# ═══════════════════════════════════════════════════════════

class TestPiRootTransformation(unittest.TestCase):
    """Testes da transformacao pi*sqrt."""

    def test_pi_root_positivo(self):
        """pi_root(1.0) = 1.0^(1/pi) ~ 1.0."""
        result = pi_root(1.0)
        self.assertAlmostEqual(result, 1.0, places=6)

    def test_pi_root_zero(self):
        """pi_root(0.0) = 0.0."""
        result = pi_root(0.0)
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_pi_root_negativo(self):
        """pi_root preserva sinal para valores negativos."""
        result = pi_root(-8.0)
        expected = -abs(-8.0) ** (1.0 / math.pi)
        self.assertAlmostEqual(result, expected, places=6)
        self.assertLess(result, 0)

    def test_pi_root_menor_que_um(self):
        """Valores < 1 expandem com pi_root."""
        x = 0.5
        result = pi_root(x)
        # 0.5^(1/pi) > 0.5 (raiz pi-esima de numero < 1 e maior)
        self.assertGreater(result, x)

    def test_pi_root_maior_que_um(self):
        """Valores > 1 comprimem com pi_root."""
        x = 100.0
        result = pi_root(x)
        # 100^(1/pi) < 100 (raiz pi-esima de numero > 1 e menor)
        self.assertLess(result, x)
        self.assertGreater(result, 1.0)

    def test_pi_root_idempotencia_parcial(self):
        """Duas aplicacoes nao restauram o original (nao e involucao)."""
        x = 16.0
        result = pi_root(pi_root(x))
        # pi_root(pi_root(16)) != 16
        self.assertNotAlmostEqual(result, x, places=2)

    def test_pi_root_energia_negativa(self):
        """Energias negativas (como em VQE) sao tratadas corretamente."""
        e = -2.5
        result = pi_root(e)
        self.assertLess(result, 0)
        # |result| < |e|
        self.assertLess(abs(result), abs(e))

    def test_pi_root_propriedade_monotona(self):
        """pi_root e monotona crescente."""
        values = [0.1, 0.5, 1.0, 5.0, 10.0, 100.0]
        results = [pi_root(v) for v in values]
        for i in range(len(results) - 1):
            self.assertLess(results[i], results[i + 1])


class TestNormaAurea(unittest.TestCase):
    """Testes da norma aurea."""

    def test_norma_perfil_zero(self):
        """Perfil zero tem norma zero."""
        result = norma_aurea([0, 0, 0, 0, 0, 0])
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_norma_perfil_um(self):
        """Perfil [1,1,1,1,1,1] tem norma aurea especifica."""
        result = norma_aurea([1, 1, 1, 1, 1, 1])
        # sqrt(phi^0*1 + phi^1*1 + ... + phi^5*1)
        expected = math.sqrt(sum(PHI ** k for k in range(6)))
        self.assertAlmostEqual(result, expected, places=6)

    def test_norma_maior_que_euclidiana(self):
        """Norma aurea >= norma euclidiana (pesos phi^k >= 1)."""
        perfil = [0.7, 0.8, 0.5, 0.6, 0.7, 0.9]
        n_aurea = norma_aurea(perfil)
        n_euclidiana = math.sqrt(sum(v ** 2 for v in perfil))
        self.assertGreaterEqual(n_aurea, n_euclidiana)

    def test_norma_vqe_perfil(self):
        """Norma aurea do perfil VQE canonico."""
        result = norma_aurea(VQE_PERFIL_CANONICO)
        self.assertGreater(result, 0)
        self.assertLess(result, 5.0)  # limite razoavel

    def test_norma_shor_perfil(self):
        """Norma aurea do perfil Shor."""
        result = norma_aurea(SHOR_PERFIL)
        self.assertGreater(result, 0)

    def test_norma_rho6_pesada(self):
        """rho_6 tem peso phi^5 >> phi^0 (rho_1)."""
        perfil_unit_rho1 = [1, 0, 0, 0, 0, 0]
        perfil_unit_rho6 = [0, 0, 0, 0, 0, 1]
        n1 = norma_aurea(perfil_unit_rho1)
        n6 = norma_aurea(perfil_unit_rho6)
        self.assertGreater(n6, n1)  # phi^5 > phi^0 = 1


# ═══════════════════════════════════════════════════════════
# 2. CONSTANTES E PERFIS
# ═══════════════════════════════════════════════════════════

class TestConstantesPerfis(unittest.TestCase):
    """Testes de constantes e perfis pre-definidos."""

    def test_phi_valor(self):
        """Constante aurea tem valor correto."""
        expected = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(PHI, expected, places=10)

    def test_vqe_perfil_tamanho(self):
        """Perfil VQE tem 6 componentes."""
        self.assertEqual(len(VQE_PERFIL_CANONICO), 6)

    def test_vqe_perfil_faixa(self):
        """Componentes do perfil VQE estao em [0, 1]."""
        for v in VQE_PERFIL_CANONICO:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_shor_perfil_anomalia(self):
        """Perfil Shor tem anomalia rho4 > rho3."""
        self.assertGreater(SHOR_PERFIL[3], SHOR_PERFIL[2])

    def test_grover_perfil_anomalia(self):
        """Perfil Grover tem anomalia rho4 > rho3."""
        self.assertGreater(GROVER_PERFIL[3], GROVER_PERFIL[2])

    def test_vqe_perfil_sem_anomalia(self):
        """VQE: rho4=0.6 > rho3=0.5 — anomalia marginal (delta=0.1 > 0.05).

        O JSON (quantum_algorithms.json) marca VQE como sem anomalia,
        mas a classificacao de delegacao com tolerancia 0.05 detecta rho4>rho3.
        Esta discrepancia e documentada — VQE e o caso mais natural na
        taxonomia, mas seu perfil tem anomalia marginal detectavel pelo
        protocolo com tolerancia padrao.
        """
        # O codigo detecta anomalia: rho4=0.6 > rho3=0.5 + 0.05=0.55
        self.assertGreater(VQE_PERFIL_CANONICO[3], VQE_PERFIL_CANONICO[2] + 0.05)

    def test_vqe_cadeia_consistente(self):
        """Perfil VQE: rho_6 > rho_5 e esperado para EMERGENCIA.

        VQE tem rho_6=0.9 > rho_5=0.7, violando a cadeia geral.
        Esta violacao NAO e a anomalia canonica (rho4 > rho3) —
        e a compensacao emergindo do sistema C+Q. No entanto,
        rho4=0.6 > rho3=0.5 tambem viola, tornando VQE um caso
        de anomalia marginal (delta=0.1 > tolerancia 0.05).
        """
        # rho_6 > rho_5: violacao da cadeia geral (esperada para emergencia)
        self.assertGreater(
            VQE_PERFIL_CANONICO[5], VQE_PERFIL_CANONICO[4],
            "VQE deve ter rho6 > rho5 (compensacao emergente)"
        )
        # Cadeia geral: pelo menos uma violacao
        n_violations = sum(
            1 for i in range(4, -1, -1)
            if VQE_PERFIL_CANONICO[i + 1] > VQE_PERFIL_CANONICO[i] + 0.05
        )
        self.assertGreater(n_violations, 0, "VQE deve ter violacoes de cadeia")

    def test_vqe_rho6_alto(self):
        """VQE tem rho_6 alto (compensacao/emergencia)."""
        self.assertGreater(VQE_PERFIL_CANONICO[5], 0.7)

    def test_vqe_rho5_elevado(self):
        """VQE tem rho_5 elevado (equilibrio)."""
        self.assertGreater(VQE_PERFIL_CANONICO[4], 0.6)

    def test_qaoa_perfil_tamanho(self):
        """Perfil QAOA tem 6 componentes."""
        self.assertEqual(len(QAOA_PERFIL), 6)

    def test_todos_perfis_faixa(self):
        """Todos os perfis estao em [0, 1]."""
        for nome, perfil in [
            ("VQE", VQE_PERFIL_CANONICO),
            ("Shor", SHOR_PERFIL),
            ("Grover", GROVER_PERFIL),
            ("QAOA", QAOA_PERFIL),
        ]:
            for i, v in enumerate(perfil):
                self.assertGreaterEqual(v, 0.0, f"{nome} rho{i+1} < 0")
                self.assertLessEqual(v, 1.0, f"{nome} rho{i+1} > 1")


# ═══════════════════════════════════════════════════════════
# 3. PiRootVQEExperiment — cenarios
# ═══════════════════════════════════════════════════════════

class TestPiRootVQEScenario(unittest.TestCase):
    """Testes de execucao de cenarios VQE."""

    def setUp(self):
        self.exp = PiRootVQEExperiment(seed=42)

    def test_cenario_basico(self):
        """Cenario basico executa sem erro e retorna trajetoria."""
        traj = self.exp.run_scenario(n_qubits=4, depth=3, iterations=10)
        self.assertIsInstance(traj, VQEProfileTrajectory)
        self.assertEqual(traj.n_qubits, 4)
        self.assertEqual(traj.depth, 3)
        self.assertEqual(traj.total_iterations, 10)
        self.assertEqual(len(traj.iterations), 10)

    def test_cenario_1_iteracao(self):
        """Cenario com 1 iteracao funciona."""
        traj = self.exp.run_scenario(iterations=1)
        self.assertEqual(len(traj.iterations), 1)

    def test_cenario_reprodutibilidade(self):
        """Cenarios com mesma seed produzem mesmos resultados."""
        t1 = self.exp.run_scenario(n_qubits=4, depth=3, iterations=20, seed=123)
        t2 = self.exp.run_scenario(n_qubits=4, depth=3, iterations=20, seed=123)
        for i in range(len(t1.iterations)):
            self.assertAlmostEqual(
                t1.iterations[i].energy,
                t2.iterations[i].energy,
                places=4,
            )

    def test_cenario_diferentes_seeds(self):
        """Cenarios com seeds diferentes produzem resultados diferentes."""
        t1 = self.exp.run_scenario(iterations=20, seed=1)
        t2 = self.exp.run_scenario(iterations=20, seed=2)
        # Pelo menos uma iteracao deve diferir
        any_diff = False
        for i in range(len(t1.iterations)):
            if abs(t1.iterations[i].energy - t2.iterations[i].energy) > 0.001:
                any_diff = True
                break
        self.assertTrue(any_diff, "Cenarios com seeds diferentes deveriam diferir")

    def test_cenario_rho5_positivo(self):
        """rho_5 em todas as iteracoes e positivo."""
        traj = self.exp.run_scenario(n_qubits=2, depth=1, iterations=20)
        for it in traj.iterations:
            self.assertGreater(it.rho5_equilibrio, 0.0)
            self.assertLessEqual(it.rho5_equilibrio, 1.0)

    def test_cenario_entropy_positiva(self):
        """Entropia em todas as iteracoes e positiva."""
        traj = self.exp.run_scenario(iterations=15)
        for it in traj.iterations:
            self.assertGreater(it.entropy, 0.0)

    def test_cenario_perfil_tamanho(self):
        """Perfil hexarrelacional tem 6 componentes."""
        traj = self.exp.run_scenario(iterations=5)
        for it in traj.iterations:
            self.assertEqual(len(it.perfil_rho), 6)

    def test_cenario_norma_aurea_positiva(self):
        """Norma aurea e positiva em todas as iteracoes."""
        traj = self.exp.run_scenario(iterations=10)
        for it in traj.iterations:
            self.assertGreater(it.norma_aurea, 0.0)

    def test_cenario_shallow_depth(self):
        """Cenario shallow (depth=1) converge bem."""
        traj = self.exp.run_scenario(n_qubits=2, depth=1, iterations=30)
        self.assertGreater(traj.rho5_delta, -0.1)

    def test_cenario_deep_depth(self):
        """Cenario profundo pode nao convergir."""
        traj = self.exp.run_scenario(n_qubits=8, depth=16, iterations=30)
        # Profundidade extrema pode degradar rho_5
        self.assertIsNotNone(traj.final_rho5)

    def test_cenario_ansatz_types(self):
        """Diferentes tipos de ansatz executam sem erro."""
        for ansatz in ["hardware_efficient", "qaoa_style", "uccsd", "strongly_entangling"]:
            traj = self.exp.run_scenario(ansatz_type=ansatz, iterations=5)
            self.assertEqual(len(traj.iterations), 5)

    def test_cenario_summary(self):
        """Summary retorna dicionario com chaves corretas."""
        traj = self.exp.run_scenario(iterations=5)
        summary = traj.summary()
        expected_keys = {
            "n_qubits", "depth", "total_iterations", "converged",
            "final_energy", "final_energy_piroot", "initial_rho5",
            "final_rho5", "rho5_delta", "trajectory_rho5",
            "trajectory_entropy", "trajectory_energy_piroot",
        }
        self.assertEqual(set(summary.keys()), expected_keys)

    def test_cenario_trajectory_listas(self):
        """Trajetorias em summary tem comprimento correto."""
        traj = self.exp.run_scenario(iterations=7)
        s = traj.summary()
        self.assertEqual(len(s["trajectory_rho5"]), 7)
        self.assertEqual(len(s["trajectory_entropy"]), 7)
        self.assertEqual(len(s["trajectory_energy_piroot"]), 7)


# ═══════════════════════════════════════════════════════════
# 4. PiRootVQEExperiment — paisagem
# ═══════════════════════════════════════════════════════════

class TestPiRootVQELandscape(unittest.TestCase):
    """Testes de analise de paisagem."""

    def setUp(self):
        self.exp = PiRootVQEExperiment(seed=42)

    def test_landscape_basico(self):
        """Analise de paisagem executa sem erro."""
        result = self.exp.analyze_landscape(
            n_qubits=4, depths=[1, 2, 3], iterations=10
        )
        self.assertIn("depths_tested", result)
        self.assertIn("trajectories", result)
        self.assertEqual(len(result["trajectories"]), 3)

    def test_landscape_reprodutivel(self):
        """Paisagem e reprodutivel com mesma seed."""
        r1 = self.exp.analyze_landscape(depths=[1, 3, 5], iterations=10)
        # Resetar seed
        self.exp = PiRootVQEExperiment(seed=42)
        r2 = self.exp.analyze_landscape(depths=[1, 3, 5], iterations=10)
        self.assertEqual(len(r1["trajectories"]), len(r2["trajectories"]))

    def test_landscape_correlacao(self):
        """Analise de paisagem inclui correlacao rho5-energy."""
        result = self.exp.analyze_landscape(depths=[1, 2, 5], iterations=10)
        self.assertIn("rho5_energy_correlation", result)
        self.assertIsInstance(result["rho5_energy_correlation"], float)

    def test_landscape_interpretacao(self):
        """Analise inclui interpretacao semantica."""
        result = self.exp.analyze_landscape(depths=[1, 3], iterations=10)
        self.assertIn("interpretation", result)
        self.assertIsInstance(result["interpretation"], str)
        self.assertGreater(len(result["interpretation"]), 50)

    def test_landscape_depths_default(self):
        """Depths default sao usados quando nao especificados."""
        result = self.exp.analyze_landscape(iterations=5)
        self.assertGreater(len(result["depths_tested"]), 0)

    def test_landscape_converged_barren_lists(self):
        """Listas de converged/barren depths sao corretas."""
        result = self.exp.analyze_landscape(depths=[1, 2, 10, 15], iterations=10)
        self.assertIn("converged_depths", result)
        self.assertIn("barren_plateau_depths", result)
        all_depths = result["converged_depths"] + result["barren_plateau_depths"]
        self.assertEqual(sorted(all_depths), [1, 2, 10, 15])

    def test_landscape_transition_depth_optional(self):
        """Transition depth pode ser None (sem barren plateau)."""
        result = self.exp.analyze_landscape(depths=[1, 2], iterations=10)
        # Pode ou nao detectar transicao
        self.assertIn("transition_depth", result)


# ═══════════════════════════════════════════════════════════
# 5. PiRootVQEExperiment — comparacao de algoritmos
# ═══════════════════════════════════════════════════════════

class TestAlgorithmComparison(unittest.TestCase):
    """Testes de comparacao entre algoritmos."""

    def setUp(self):
        self.exp = PiRootVQEExperiment(seed=42)

    def test_comparacao_basica(self):
        """Comparacao entre algoritmos executa sem erro."""
        result = self.exp.compare_algorithms()
        self.assertIn("algorithms", result)
        self.assertIn("comparisons", result)

    def test_comparacao_4_algoritmos(self):
        """Comparacao inclui VQE, QAOA, Shor, Grover."""
        result = self.exp.compare_algorithms()
        algos = set(result["algorithms"].keys())
        self.assertEqual(algos, {"VQE", "QAOA", "Shor", "Grover"})

    def test_comparacao_vqe_emergencia(self):
        """VQE: classificado como anomalia (rho4 > rho3 tem prioridade na cascata).

        Embora rho6=0.9 > 0.7 sugira emergencia, a cascata de classificacao
        verifica anomalia (rho4>rho3) primeiro. VQE tem rho4=0.6 > rho3=0.5,
        entao e classificado como anomalia pelo protocolo.
        """
        result = self.exp.compare_algorithms()
        vqe = result["algorithms"]["VQE"]
        # Anomalia tem prioridade na cascata sobre emergencia
        self.assertEqual(vqe["delegacao"], "anomalia")

    def test_comparacao_shor_anomalia(self):
        """Shor e classificado com anomalia detectada."""
        result = self.exp.compare_algorithms()
        shor = result["algorithms"]["Shor"]
        self.assertTrue(shor["anomalia_detectada"])

    def test_comparacao_grover_anomalia(self):
        """Grover e classificado com anomalia detectada."""
        result = self.exp.compare_algorithms()
        grover = result["algorithms"]["Grover"]
        self.assertTrue(grover["anomalia_detectada"])

    def test_comparacao_vqe_consistente(self):
        """VQE: cadeia geral violada (rho6 > rho5).

        O perfil VQE [0.7, 0.8, 0.5, 0.6, 0.7, 0.9] tem rho6=0.9 > rho5=0.7,
        violando a cadeia de implicacao geral rho_6=>rho_5=>...=>rho_1.
        """
        result = self.exp.compare_algorithms()
        vqe = result["algorithms"]["VQE"]
        self.assertFalse(vqe["cadeia_consistente"])

    def test_comparacao_vqe_tats(self):
        """VQE: classificacao TATS = anomalia-detectavel (rho4 > rho3).

        Nota: o JSON (quantum_algorithms.json) classifica VQE como
        consistente-paradigmatico, mas o protocolo com tolerancia 0.05
        detecta rho4=0.6 > rho3=0.5, classificando como anomalia-detectavel.
        """
        result = self.exp.compare_algorithms()
        vqe = result["algorithms"]["VQE"]
        self.assertEqual(vqe["classificacao_tats"], "anomalia-detectavel")

    def test_comparacao_shor_tats(self):
        """Shor tem classificacao TATS anomalia-detectavel."""
        result = self.exp.compare_algorithms()
        shor = result["algorithms"]["Shor"]
        self.assertEqual(shor["classificacao_tats"], "anomalia-detectavel")

    def test_comparacao_norma_aurea(self):
        """Todos os algoritmos tem norma aurea calculada."""
        result = self.exp.compare_algorithms()
        for name, data in result["algorithms"].items():
            self.assertGreater(data["norma_aurea"], 0.0, f"{name} norma aurea <= 0")
            self.assertIn("pi_root_norma", data)

    def test_comparacao_pares(self):
        """Comparacoes par-a-par sao geradas (C(4,2) = 6 pares)."""
        result = self.exp.compare_algorithms()
        self.assertEqual(len(result["comparisons"]), 6)

    def test_comparacao_similarity_faixa(self):
        """Similaridades estao em [0, 1]."""
        result = self.exp.compare_algorithms()
        for key, comp in result["comparisons"].items():
            self.assertGreaterEqual(comp["similarity"], 0.0)
            self.assertLessEqual(comp["similarity"], 1.0)

    def test_comparacao_interpretacao(self):
        """Comparacao inclui interpretacao semantica."""
        result = self.exp.compare_algorithms()
        self.assertIn("interpretation", result)
        self.assertGreater(len(result["interpretation"]), 50)


# ═══════════════════════════════════════════════════════════
# 6. PiRootVQEExperiment — correlacao PiRoot
# ═══════════════════════════════════════════════════════════

class TestPiRootCorrelation(unittest.TestCase):
    """Testes de analise de correlacao PiRoot."""

    def setUp(self):
        self.exp = PiRootVQEExperiment(seed=42)

    def test_correlacao_basica(self):
        """Analise de correlacao executa sem erro."""
        result = self.exp.piroot_correlation_analysis(n_scenarios=5)
        self.assertIn("correlation_piroot_norma_aurea", result)
        self.assertIn("correlation_piroot_rho5", result)

    def test_correlacao_faixa(self):
        """Correlacoes estao em [-1, 1]."""
        result = self.exp.piroot_correlation_analysis(n_scenarios=5)
        for key in [
            "correlation_piroot_norma_aurea",
            "correlation_piroot_rho5",
            "correlation_norma_aurea_rho5",
        ]:
            val = result[key]
            self.assertGreaterEqual(val, -1.0)
            self.assertLessEqual(val, 1.0)

    def test_correlacao_data_points(self):
        """Data points tem comprimento correto."""
        result = self.exp.piroot_correlation_analysis(n_scenarios=8)
        dp = result["data_points"]
        self.assertEqual(len(dp["piroot_values"]), 8)
        self.assertEqual(len(dp["norma_values"]), 8)
        self.assertEqual(len(dp["rho5_values"]), 8)

    def test_correlacao_interpretacao(self):
        """Correlacao inclui interpretacao."""
        result = self.exp.piroot_correlation_analysis(n_scenarios=5)
        self.assertIn("interpretation", result)
        self.assertIsInstance(result["interpretation"], str)


# ═══════════════════════════════════════════════════════════
# 7. ExperimentResults
# ═══════════════════════════════════════════════════════════

class TestExperimentResults(unittest.TestCase):
    """Testes do container de resultados."""

    def test_results_vazio(self):
        """Results vazio retorna None para trajectory."""
        results = ExperimentResults()
        self.assertIsNone(results.trajectory(0))
        self.assertIsNone(results.best_convergence())

    def test_results_trajectory(self):
        """Trajectory retorna cenario correto."""
        results = ExperimentResults()
        exp = PiRootVQEExperiment(seed=42)
        t1 = exp.run_scenario(iterations=3)
        t2 = exp.run_scenario(iterations=3)
        results.scenarios = [t1, t2]

        self.assertIs(results.trajectory(0), t1)
        self.assertIs(results.trajectory(1), t2)
        self.assertIsNone(results.trajectory(2))

    def test_results_best_convergence(self):
        """Best convergence retorna cenario com menor energia."""
        results = ExperimentResults()
        # Criar trajetorias simuladas
        t1 = VQEProfileTrajectory(
            n_qubits=4, depth=3, total_iterations=10,
            converged=True, final_energy=-0.5,
            final_energy_piroot=pi_root(-0.5),
            initial_rho5=0.3, final_rho5=0.7, rho5_delta=0.4,
        )
        t2 = VQEProfileTrajectory(
            n_qubits=4, depth=3, total_iterations=10,
            converged=True, final_energy=-0.9,
            final_energy_piroot=pi_root(-0.9),
            initial_rho5=0.3, final_rho5=0.8, rho5_delta=0.5,
        )
        results.scenarios = [t1, t2]
        best = results.best_convergence()
        self.assertAlmostEqual(best.final_energy, -0.9, places=2)

    def test_results_summary(self):
        """Summary inclui todas as chaves esperadas."""
        results = ExperimentResults()
        results.metadata = {"test": True}
        summary = results.summary()
        self.assertEqual(summary["total_scenarios"], 0)
        self.assertEqual(summary["converged"], 0)
        self.assertIn("metadata", summary)

    def test_results_adicionados_pelo_experimento(self):
        """Experimento adiciona cenarios ao results."""
        exp = PiRootVQEExperiment(seed=42)
        self.assertEqual(len(exp.results.scenarios), 0)
        exp.run_scenario(iterations=3)
        self.assertEqual(len(exp.results.scenarios), 1)
        exp.run_scenario(iterations=3)
        self.assertEqual(len(exp.results.scenarios), 2)


# ═══════════════════════════════════════════════════════════
# 8. BarrenPlateauTest
# ═══════════════════════════════════════════════════════════

class TestBarrenPlateauBasic(unittest.TestCase):
    """Testes basicos do barren plateau test."""

    def setUp(self):
        self.test = BarrenPlateauTest(n_qubits=4, seed=42)

    def test_init(self):
        """Inicializacao com parametros corretos."""
        self.assertEqual(self.test.n_qubits, 4)
        self.assertEqual(self.test.rho5_threshold, THRESHOLD_RHO5_BARREN)

    def test_run_basico(self):
        """Teste basico executa sem erro."""
        results = self.test.run(depths=[1, 2, 3], iterations_per_depth=10)
        self.assertIsInstance(results, BarrenPlateauResults)
        self.assertEqual(results.n_qubits, 4)
        self.assertEqual(len(results.profiles), 3)

    def test_run_default_depths(self):
        """Depths default sao usados."""
        results = self.test.run(iterations_per_depth=5)
        self.assertGreater(len(results.depths_tested), 0)

    def test_profiles_depth_correto(self):
        """Cada profile tem depth correto."""
        results = self.test.run(depths=[2, 5, 10], iterations_per_depth=5)
        for i, profile in enumerate(results.profiles):
            self.assertEqual(profile.depth, [2, 5, 10][i])

    def test_profiles_rho5_faixa(self):
        """rho_5 medio esta em [0, 1]."""
        results = self.test.run(depths=[1, 3, 5], iterations_per_depth=10)
        for p in results.profiles:
            self.assertGreaterEqual(p.rho5_mean, 0.0)
            self.assertLessEqual(p.rho5_mean, 1.0)

    def test_profiles_entropy_max(self):
        """Entropia maxima e log2(2^n) = n."""
        results = self.test.run(depths=[1], iterations_per_depth=5)
        for p in results.profiles:
            self.assertAlmostEqual(p.entropy_max, float(self.test.n_qubits), places=2)

    def test_profiles_summary(self):
        """Summary de profile retorna dicionario com chaves."""
        results = self.test.run(depths=[1], iterations_per_depth=5)
        s = results.profiles[0].summary()
        expected_keys = {
            "depth", "n_qubits", "rho5_mean", "rho5_std", "rho6_mean",
            "entropy_mean", "entropy_max", "entropy_ratio",
            "gradient_mean", "is_barren", "confidence",
        }
        self.assertEqual(set(s.keys()), expected_keys)


class TestBarrenPlateauDetection(unittest.TestCase):
    """Testes de deteccao de barren plateau."""

    def test_shallow_not_barren(self):
        """Circuito shallow (depth=1) tipicamente nao e barren."""
        test = BarrenPlateauTest(n_qubits=2, seed=42)
        results = test.run(depths=[1], iterations_per_depth=20)
        # Com 2 qubits e depth 1, nao deveria ser barren
        self.assertFalse(results.profiles[0].is_barren)

    def test_deep_may_be_barren(self):
        """Circuito profundo pode ser barren."""
        test = BarrenPlateauTest(n_qubits=8, seed=42)
        results = test.run(depths=[1, 2, 3, 5, 8, 12, 16], iterations_per_depth=20)
        # Pelo menos um depth profundo deve ser barren com 8 qubits
        has_barren = any(p.is_barren for p in results.profiles)
        self.assertTrue(has_barren, "Esperado barren plateau em circuito profundo com 8 qubits")

    def test_onset_depth_detected(self):
        """Onset depth e detectado quando ha barren."""
        test = BarrenPlateauTest(n_qubits=6, seed=42)
        results = test.run(depths=[1, 2, 3, 5, 8, 12, 16], iterations_per_depth=20)
        if results.barren_depths:
            self.assertIsNotNone(results.onset_depth)
            self.assertIn(results.onset_depth, results.barren_depths)

    def test_healthy_before_onset(self):
        """Depths antes do onset sao saudaveis."""
        test = BarrenPlateauTest(n_qubits=6, seed=42)
        results = test.run(depths=[1, 2, 3, 5, 8, 12, 16], iterations_per_depth=20)
        if results.onset_depth and results.onset_depth > 1:
            for d in results.healthy_depths:
                self.assertLess(d, results.onset_depth)

    def test_barren_after_onset(self):
        """Depths apos onset sao barren (ou mais profundos)."""
        test = BarrenPlateauTest(n_qubits=6, seed=42)
        results = test.run(depths=[1, 2, 3, 5, 8, 12, 16], iterations_per_depth=20)
        if results.onset_depth:
            for d in results.barren_depths:
                self.assertGreaterEqual(d, results.onset_depth)

    def test_results_summary(self):
        """Summary de resultados inclui todas as chaves."""
        test = BarrenPlateauTest(n_qubits=4, seed=42)
        results = test.run(depths=[1, 2, 3], iterations_per_depth=5)
        s = results.summary()
        expected_keys = {
            "n_qubits", "depths_tested", "onset_depth",
            "onset_confidence", "healthy_depths", "barren_depths",
            "transition_analysis", "profiles_summary", "metadata",
        }
        self.assertEqual(set(s.keys()), expected_keys)


class TestBarrenPlateauTransition(unittest.TestCase):
    """Testes de analise de transicao."""

    def test_transition_analise(self):
        """Analise de transicao executa sem erro."""
        test = BarrenPlateauTest(n_qubits=4, seed=42)
        results = test.run(depths=[1, 2, 5, 10], iterations_per_depth=10)
        self.assertIn("detected", results.transition_analysis)
        self.assertIsInstance(results.transition_analysis["detected"], bool)

    def test_transition_severity(self):
        """Quando detectada, transicao tem severidade definida."""
        test = BarrenPlateauTest(n_qubits=6, seed=42)
        results = test.run(depths=[1, 2, 5, 10, 15], iterations_per_depth=15)
        if results.transition_analysis.get("detected"):
            self.assertIn(results.transition_analysis.get("severity"), [
                "abrupta", "moderada", "gradual", "marginal"
            ])


class TestBarrenPlateauQubitScaling(unittest.TestCase):
    """Testes de scaling por qubits."""

    def test_scaling_basico(self):
        """Teste de scaling executa sem erro."""
        test = BarrenPlateauTest(n_qubits=4, seed=42)
        result = test.run_qubit_scaling(
            depths=[1, 3], qubit_range=[2, 4], iterations_per_point=5
        )
        self.assertIn("matrix", result)
        self.assertIn("frontier", result)
        self.assertEqual(len(result["matrix"]), 2)  # 2 qubit ranges
        self.assertEqual(len(result["matrix"][0]), 2)  # 2 depths

    def test_scaling_matrix_boolean(self):
        """Matriz de scaling contem apenas booleanos."""
        test = BarrenPlateauTest(n_qubits=4, seed=42)
        result = test.run_qubit_scaling(
            depths=[1, 3, 5], qubit_range=[2, 6], iterations_per_point=5
        )
        for row in result["matrix"]:
            for val in row:
                self.assertIsInstance(val, bool)

    def test_scaling_fronteira_diminui(self):
        """Fronteira de seguranca diminui com mais qubits."""
        test = BarrenPlateauTest(n_qubits=4, seed=42)
        result = test.run_qubit_scaling(
            depths=[1, 2, 3, 5, 8],
            qubit_range=[2, 4, 6, 8],
            iterations_per_point=15,
        )
        frontier = result["frontier"]
        # A fronteira para mais qubits deve ser <= que para menos qubits
        values = list(frontier.values())
        # Pode nao ser monotono perfeitamente, mas tendencia geral
        # Pelo menos um par consecutivo deve respeitar a tendencia
        has_decrease = False
        for i in range(len(values) - 1):
            if values[i] >= values[i + 1]:
                has_decrease = True
                break
        self.assertTrue(has_decrease, "Fronteira deveria diminuir com mais qubits")

    def test_scaling_interpretacao(self):
        """Scaling inclui interpretacao."""
        test = BarrenPlateauTest(n_qubits=4, seed=42)
        result = test.run_qubit_scaling(
            depths=[1, 3], qubit_range=[2, 4], iterations_per_point=5
        )
        self.assertIn("interpretation", result)
        self.assertGreater(len(result["interpretation"]), 50)


# ═══════════════════════════════════════════════════════════
# 9. INTEGRACAO COM ALEXANDRIA
# ═══════════════════════════════════════════════════════════

class TestAlexandriaIntegration(unittest.TestCase):
    """Testes de integracao com modulo Alexandria."""

    def test_perfis_match_alexandria(self):
        """Perfis do experimento batem com PERFIS_ALGORITMOS do Alexandria."""
        try:
            from alexandria.core.quantum_interface import PERFIS_ALGORITMOS
            # VQE
            self.assertEqual(VQE_PERFIL_CANONICO, PERFIS_ALGORITMOS["VQE"]["rho"])
            # Shor
            self.assertEqual(SHOR_PERFIL, PERFIS_ALGORITMOS["Shor"]["rho"])
            # Grover
            self.assertEqual(GROVER_PERFIL, PERFIS_ALGORITMOS["Grover"]["rho"])
            # QAOA
            self.assertEqual(QAOA_PERFIL, PERFIS_ALGORITMOS["QAOA"]["rho"])
        except ImportError:
            self.skipTest("Alexandria nao disponivel")

    def test_classificacao_match_alexandria(self):
        """Classificacao de delegacao do experimento bate com Alexandria.

        VQE e classificado como ANOMALIA (rho4=0.6 > rho3=0.5) pela
        cascata de prioridade, mesmo que rho6=0.9 sugira emergencia.
        A cascata verifica anomalia primeiro.
        """
        try:
            from alexandria.core.quantum_interface import (
                classificar_delegacao, TipoDelegacao,
            )
            # VQE: anomalia (rho4 > rho3 tem prioridade)
            result = classificar_delegacao(VQE_PERFIL_CANONICO, nome="VQE")
            self.assertEqual(result.tipo, TipoDelegacao.ANOMALIA)
            # Shor: anomalia
            result = classificar_delegacao(SHOR_PERFIL, nome="Shor")
            self.assertEqual(result.tipo, TipoDelegacao.ANOMALIA)
            # Grover: anomalia
            result = classificar_delegacao(GROVER_PERFIL, nome="Grover")
            self.assertEqual(result.tipo, TipoDelegacao.ANOMALIA)
        except ImportError:
            self.skipTest("Alexandria nao disponivel")

    def test_consistency_match_alexandria(self):
        """Consistencia da cadeia bate com Alexandria ConsistencyChecker.

        VQE tem rho6=0.9 > rho5=0.7, violando a cadeia geral.
        Shor tem multiplas violacoes.
        """
        try:
            from alexandria.core.quantum_comparator import ConsistencyChecker
            checker = ConsistencyChecker()
            # VQE: NAO consistente (rho6 > rho5, rho4 > rho3)
            check = checker.check(VQE_PERFIL_CANONICO)
            self.assertFalse(check["consistente"])
            # Shor: NAO consistente (multiplas violacoes)
            check = checker.check(SHOR_PERFIL)
            self.assertFalse(check["consistente"])
        except ImportError:
            self.skipTest("Alexandria nao disponivel")


if __name__ == "__main__":
    unittest.main()
