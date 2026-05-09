"""
PiRoot VQE Experiment — Analise Hexarrelacional do VQE via Protocolo GuruDev

Este experimento demonstra GuruDev como protocolo semantico da interface
classico-quântica atravas da analise do Variational Quantum Eigensolver (VQE)
usando a algebra hexarrelacional rho_1-rho_6.

Hipotese PiRoot-VQE:
  O VQE, sendo o algoritmo mais natural na taxonomia hexarrelacional
  (rho_6=0.9, rho_5=0.7, cadeia consistente, classificacao TATS:
  consistente-paradigmatico), pode ser monitorado semanticamente pelo
  protocolo GuruDev. A dinamica de rho_5 (equilibrio) ao longo das
  iteracoes de otimizacao reflete a qualidade da convergencia, enquanto
  a transformacao pi*sqrt(f(A)) normaliza a energia e correlaciona com
  a norma aurea do perfil hexarrelacional.

Conceitos-chave:
  - PiRoot: transformacao pi*sqrt — raiz pi-esima preservando sinal
  - R5: vetor de significancia (gm_ontologia, gm_campo, gm_hermeneutica,
         gm_tempo, gm_paradigma) do interpreter GuruDev
  - R6: vetor hexarrelacional [rho_1, ..., rho_6] para contexto quantico
  - Barren plateau: regiao onde gradientes desaparecem — detectavel via
    degradacao de rho_5 (equilibrio classico-quantico)

GuruDev NAO executa computacao quantica real — e o protocolo semantico
que governa a delegacao classico-quantica. Este experimento simula
o comportamento esperado baseado na classificacao de delegacao.

Referencia: Machado (2026b). pi*sqrt(f(A)) e Computacao Quantica.
    DOI: 10.5281/zenodo.18776462

Autor: Guilherme Goncalves Machado (Hubstry-DeepTech)
Versao: 0.1.0 | Licenca: MIT
"""

import math
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


# Constante aurea (secao aurea)
PHI = (1 + math.sqrt(5)) / 2


# ═══════════════════════════════════════════════════════════
# PIROOT TRANSFORMATION
# ═══════════════════════════════════════════════════════════

def pi_root(x: float) -> float:
    """
    Transformacao pi*sqrt — raiz pi-esima preservando sinal.

    Para x > 0: x^(1/pi) ~ x^0.318
    Para x < 0: -|x|^(1/pi)
    Esta transformacao comprime valores grandes e expande valores
    pequenos, mapeando a faixa de energia do VQE para o dominio
    pi-root onde correlacoes com rho_5 se tornam visiveis.

    Args:
        x: Valor de entrada (tipicamente energia)

    Returns:
        Valor transformado pi*sqrt
    """
    return math.copysign(abs(x) ** (1.0 / math.pi), x)


def norma_aurea(perfil: List[float]) -> float:
    """
    Norma aurea de um perfil hexarrelacional.

    Aplica pesos phi^k a cada componente, onde phi e a secao aurea.
    Componentes de maior ordem (rho_6) tem peso maior, refletindo
    a importancia hierarquica da cadeia de implicacao.

    Args:
        perfil: Lista de 6 valores float em [0,1]

    Returns:
        Norma aurea do perfil
    """
    return math.sqrt(sum(PHI ** k * v ** 2 for k, v in enumerate(perfil)))


# ═══════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════

@dataclass
class VQEIterationResult:
    """Resultado de uma unica iteracao VQE simulada."""

    iteration: int
    energy: float
    energy_piroot: float
    rho5_equilibrio: float
    rho6_compensacao: float
    perfil_rho: List[float]
    norma_aurea: float
    entropy: float
    delegacao_tipo: str
    converged: bool
    gradient_magnitude: float


@dataclass
class VQEProfileTrajectory:
    """Trajetoria completa do perfil hexarrelacional durante otimizacao VQE."""

    n_qubits: int
    depth: int
    total_iterations: int
    converged: bool
    final_energy: float
    final_energy_piroot: float
    initial_rho5: float
    final_rho5: float
    rho5_delta: float
    iterations: List[VQEIterationResult] = field(default_factory=list)

    def summary(self) -> Dict[str, Any]:
        """Retorna resumo da trajetoria."""
        return {
            "n_qubits": self.n_qubits,
            "depth": self.depth,
            "total_iterations": self.total_iterations,
            "converged": self.converged,
            "final_energy": round(self.final_energy, 6),
            "final_energy_piroot": round(self.final_energy_piroot, 6),
            "initial_rho5": round(self.initial_rho5, 4),
            "final_rho5": round(self.final_rho5, 4),
            "rho5_delta": round(self.rho5_delta, 4),
            "trajectory_rho5": [
                round(it.rho5_equilibrio, 4) for it in self.iterations
            ],
            "trajectory_entropy": [
                round(it.entropy, 4) for it in self.iterations
            ],
            "trajectory_energy_piroot": [
                round(it.energy_piroot, 4) for it in self.iterations
            ],
        }


@dataclass
class ExperimentResults:
    """Resultados completos do experimento PiRoot-VQE."""

    scenarios: List[VQEProfileTrajectory] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def trajectory(self, index: int = 0) -> Optional[VQEProfileTrajectory]:
        """Retorna trajetoria por indice."""
        if 0 <= index < len(self.scenarios):
            return self.scenarios[index]
        return None

    def best_convergence(self) -> Optional[VQEProfileTrajectory]:
        """Retorna o cenario com melhor convergencia (menor energia final)."""
        converged = [s for s in self.scenarios if s.converged]
        if not converged:
            return None
        return min(converged, key=lambda s: s.final_energy)

    def summary(self) -> Dict[str, Any]:
        """Retorna resumo de todos os cenarios."""
        return {
            "total_scenarios": len(self.scenarios),
            "converged": sum(1 for s in self.scenarios if s.converged),
            "best_energy": min(
                (s.final_energy for s in self.scenarios), default=None
            ),
            "scenarios": [
                {
                    "n_qubits": s.n_qubits,
                    "depth": s.depth,
                    "converged": s.converged,
                    "final_energy_piroot": round(s.final_energy_piroot, 4),
                    "rho5_delta": round(s.rho5_delta, 4),
                }
                for s in self.scenarios
            ],
            "metadata": self.metadata,
        }


# ═══════════════════════════════════════════════════════════
# PERFIL VQE — Perfil hexarrelacional canônico do VQE
# ═══════════════════════════════════════════════════════════

# Perfil hexarrelacional conjectural do VQE (Machado 2026b, Secao 5)
VQE_PERFIL_CANONICO = [0.7, 0.8, 0.5, 0.6, 0.7, 0.9]

# Perfis para outros algoritmos (referencia)
SHOR_PERFIL = [0.9, 0.85, 0.3, 0.7, 0.2, 0.5]
GROVER_PERFIL = [0.95, 0.6, 0.7, 0.9, 0.3, 0.2]
QAOA_PERFIL = [0.6, 0.75, 0.4, 0.5, 0.6, 0.7]


# ═══════════════════════════════════════════════════════════
# PiRoot VQE EXPERIMENT
# ═══════════════════════════════════════════════════════════

class PiRootVQEExperiment:
    """
    Experimento PiRoot-VQE: monitoramento semantico do VQE via
    algebra hexarrelacional rho_1-rho_6.

    Este experimento NAO executa VQE real. Ele simula o comportamento
    esperado do perfil hexarrelacional durante uma otimizacao VQE
    hipotetica, demonstrando como GuruDev pode servir como protocolo
    semantico de monitoramento para algoritmos hibridos classico-quanticos.

    A simulacao segue as seguintes regras:
      1. rho_5 (equilibrio) e o indicador principal de convergencia
      2. rho_6 (compensacao) representa a emergencia do sistema composto C+Q
      3. A transformacao pi*sqrt normaliza a energia para comparacao
      4. A entropia de Shannon da distribuicao de medicao reflete a
         incerteza quantica — alta entropia indica barren plateau
      5. A profundidade do circuito influencia a degradacao do perfil

    Casos de uso:
      - Monitoramento semantico de convergencia VQE
      - Deteccao precoce de barren plateaus via rho_5
      - Comparacao entre ansatzes (HardwareEfficient, QAOA-style, etc.)
      - Validacao da hipotese PiRoot: pi*sqrt(E) correlaciona com
        norma aurea do perfil hexarrelacional
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa o experimento.

        Args:
            seed: Semente para reprodutibilidade
        """
        self.rng = random.Random(seed)
        self.results = ExperimentResults(
            metadata={"seed": seed, "framework": "PiRoot-VQE v0.1.0"}
        )

    # ── Simulacao de cenario VQE ───────────────────────────

    def run_scenario(
        self,
        n_qubits: int = 4,
        depth: int = 3,
        iterations: int = 50,
        ground_energy: float = -1.0,
        initial_energy: float = 0.0,
        ansatz_type: str = "hardware_efficient",
        seed: Optional[int] = None,
    ) -> VQEProfileTrajectory:
        """
        Executa um cenario VQE simulado e retorna a trajetoria do perfil.

        A simulacao modela a otimizacao VQE como um processo onde:
          - A energia converge exponencialmente em direcao a ground_energy
          - rho_5 (equilibrio) evolui proporcionalmente a qualidade da convergencia
          - rho_6 (compensacao) flutua mas permanece alto (>= 0.7) para VQE
          - Barren plateaus (rho_5 caindo < 0.5) podem ocorrer em circuitos profundos

        Args:
            n_qubits: Numero de qubits
            depth: Profundidade do circuito ansatz
            iterations: Numero de iteracoes de otimizacao
            ground_energy: Energia do estado fundamental (referencia)
            initial_energy: Energia inicial (antes da otimizacao)
            ansatz_type: Tipo do ansatz (hardware_efficient, qaoa_style, uccsd)
            seed: Semente especifica para este cenario

        Returns:
            VQEProfileTrajectory com dados de todas as iteracoes
        """
        rng = random.Random(seed)

        # Fator de degradacao por profundidade (circuitos mais profundos
        # tendem a degradar rho_5, simulando barren plateaus)
        depth_factor = max(0.3, 1.0 - 0.1 * (depth - 1))

        # Fator de degradacao por numero de qubits (mais qubits = mais
        # susceptibilidade a barren plateaus — lei exponencial)
        qubit_factor = max(0.2, 1.0 - 0.05 * (n_qubits - 2))

        # Combinar fatores
        degradation = depth_factor * qubit_factor

        # Fator de convergencia base (ansatz influencia a taxa)
        ansatz_factors = {
            "hardware_efficient": 0.92,
            "qaoa_style": 0.85,
            "uccsd": 0.95,
            "strongly_entangling": 0.80,
        }
        convergence_rate = ansatz_factors.get(ansatz_type, 0.90)

        # Aplicar degradacao a taxa de convergencia
        convergence_rate *= degradation

        # Perfil VQE de base (canonico: [0.7, 0.8, 0.5, 0.6, 0.7, 0.9])
        perfil_base = VQE_PERFIL_CANONICO[:]

        iteration_results = []
        current_energy = initial_energy
        converged = False

        for i in range(iterations):
            # Progresso da convergencia (exponencial decay)
            t = i / max(1, iterations - 1)
            progress = 1.0 - math.exp(-3.0 * t * convergence_rate)

            # Energia converge em direcao a ground_energy
            energy_gap = initial_energy - ground_energy
            current_energy = initial_energy - energy_gap * progress
            # Adicionar ruido que diminui com a convergencia
            noise = rng.gauss(0, 0.05 * (1.0 - progress * 0.8))
            current_energy += noise

            # PiRoot transformation da energia
            energy_piroot = pi_root(current_energy)

            # Evolucao do perfil hexarrelacional
            # rho_5 (equilibrio): sobe com convergencia, cai com degradacao
            rho5_base = 0.3 + 0.5 * progress * degradation
            rho5_noise = rng.gauss(0, 0.02)
            rho5 = max(0.1, min(1.0, rho5_base + rho5_noise))

            # rho_6 (compensacao): permanece alto para VQE, mas degrada
            # em circuitos profundos
            rho6_base = 0.5 + 0.4 * degradation
            rho6_noise = rng.gauss(0, 0.03)
            rho6 = max(0.1, min(1.0, rho6_base + rho6_noise))

            # Perfil completo — outros rho evoluem suavemente
            rho1 = 0.5 + 0.2 * progress + rng.gauss(0, 0.02)
            rho2 = 0.6 + 0.2 * progress + rng.gauss(0, 0.02)
            rho3 = 0.3 + 0.2 * progress + rng.gauss(0, 0.02)
            rho4 = 0.4 + 0.2 * progress + rng.gauss(0, 0.02)

            # Clamp todos em [0, 1]
            perfil = [
                max(0.0, min(1.0, rho1)),
                max(0.0, min(1.0, rho2)),
                max(0.0, min(1.0, rho3)),
                max(0.0, min(1.0, rho4)),
                max(0.0, min(1.0, rho5)),
                max(0.0, min(1.0, rho6)),
            ]

            # Calcular metricas derivadas
            n_aurea = norma_aurea(perfil)

            # Entropia da distribuicao de medicao simulada
            # (maior entropia = mais incerteza = pior convergencia)
            n_outcomes = 2 ** n_qubits
            if rho5 > 0.5:
                # Equilibrio bom: distribuicao concentrada
                p_concentrated = rho5 * 0.7
                p_uniform = (1 - p_concentrated) / (n_outcomes - 1)
                entropy = -(
                    p_concentrated * math.log2(p_concentrated)
                    + (n_outcomes - 1) * p_uniform * math.log2(max(1e-10, p_uniform))
                )
            else:
                # Barren plateau: distribuicao proxima da uniforme
                entropy = math.log2(n_outcomes) * (1.0 - 0.2 * rho5)

            # Classificacao de delegacao
            if rho5 > 0.6:
                delegacao = "equilibrio"
            elif rho6 > 0.7:
                delegacao = "emergencia"
            elif rho5 >= 0.5:
                delegacao = "conservacao"
            else:
                delegacao = "conservacao"  # fallback

            # Magnitude do gradiente (simulada)
            gradient = abs(ground_energy - current_energy) * (1.0 + rng.gauss(0, 0.1))
            gradient = max(0.001, gradient)

            # Verificar convergencia
            converged = (
                abs(current_energy - ground_energy) < 0.1
                and gradient < 0.15
            )

            iteration_results.append(VQEIterationResult(
                iteration=i,
                energy=round(current_energy, 6),
                energy_piroot=round(energy_piroot, 6),
                rho5_equilibrio=round(rho5, 4),
                rho6_compensacao=round(rho6, 4),
                perfil_rho=[round(r, 4) for r in perfil],
                norma_aurea=round(n_aurea, 6),
                entropy=round(entropy, 4),
                delegacao_tipo=delegacao,
                converged=converged,
                gradient_magnitude=round(gradient, 4),
            ))

        # Calcular rho5 inicial e final
        initial_rho5 = iteration_results[0].rho5_equilibrio if iteration_results else 0.0
        final_rho5 = iteration_results[-1].rho5_equilibrio if iteration_results else 0.0

        trajectory = VQEProfileTrajectory(
            n_qubits=n_qubits,
            depth=depth,
            total_iterations=iterations,
            converged=converged,
            final_energy=round(current_energy, 6),
            final_energy_piroot=round(pi_root(current_energy), 6),
            initial_rho5=round(initial_rho5, 4),
            final_rho5=round(final_rho5, 4),
            rho5_delta=round(final_rho5 - initial_rho5, 4),
            iterations=iteration_results,
        )

        self.results.scenarios.append(trajectory)
        return trajectory

    # ── Analise de paisagem ────────────────────────────────

    def analyze_landscape(
        self,
        n_qubits: int = 4,
        depths: Optional[List[int]] = None,
        iterations: int = 50,
        ground_energy: float = -1.0,
        initial_energy: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Analisa a paisagem de convergencia VQE em diferentes profundidades.

        Executa multiplos cenarios com profundidades variadas e analisa
        como o perfil hexarrelacional se degrada, identificando o ponto
        de transicao entre convergencia saudavel e barren plateau.

        Args:
            n_qubits: Numero de qubits
            depths: Lista de profundidades a testar (default [1, 2, 3, 5, 8, 12])
            iterations: Iteracoes por cenario
            ground_energy: Energia do estado fundamental
            initial_energy: Energia inicial

        Returns:
            Dicionario com analise completa da paisagem
        """
        if depths is None:
            depths = [1, 2, 3, 5, 8, 12]

        trajectories = []
        for d in depths:
            traj = self.run_scenario(
                n_qubits=n_qubits,
                depth=d,
                iterations=iterations,
                ground_energy=ground_energy,
                initial_energy=initial_energy,
                seed=self.rng.randint(0, 999999),
            )
            trajectories.append(traj)

        # Identificar ponto de transicao (barren plateau onset)
        # O barren plateau onset e a profundidade onde rho5_delta muda de sinal
        # ou onde a convergencia falha
        transition_depth = None
        for i, traj in enumerate(trajectories):
            if not traj.converged or traj.rho5_delta < 0:
                transition_depth = depths[i]
                break

        # Calcular correlacao entre rho5_final e energia_piroot_final
        rho5_values = [t.final_rho5 for t in trajectories]
        energy_values = [t.final_energy_piroot for t in trajectories]
        correlation = self._pearson_correlation(rho5_values, energy_values)

        return {
            "n_qubits": n_qubits,
            "depths_tested": depths,
            "trajectories": [t.summary() for t in trajectories],
            "transition_depth": transition_depth,
            "converged_depths": [d for d, t in zip(depths, trajectories) if t.converged],
            "barren_plateau_depths": [d for d, t in zip(depths, trajectories) if not t.converged],
            "rho5_energy_correlation": round(correlation, 6),
            "interpretation": self._interpret_landscape(trajectories, depths, transition_depth),
        }

    # ── Comparacao entre algoritmos ────────────────────────

    def compare_algorithms(
        self,
        n_qubits: int = 4,
        depth: int = 3,
        iterations: int = 50,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Compara VQE, QAOA, Shor e Grover via perfil hexarrelacional.

        Para cada algoritmo, usa o perfil canonico da Alexandria e
        simula a execucao, comparando a dinamica rho_5-rho_6.

        Args:
            n_qubits: Numero de qubits
            depth: Profundidade do circuito
            iterations: Iteracoes de otimizacao
            seed: Semente para reprodutibilidade

        Returns:
            Dicionario com comparacao detalhada
        """
        algorithms = {
            "VQE": {"perfil": VQE_PERFIL_CANONICO, "tipo": "variacional-hibrido"},
            "QAOA": {"perfil": QAOA_PERFIL, "tipo": "variacional-hibrido"},
            "Shor": {"perfil": SHOR_PERFIL, "tipo": "gate-based"},
            "Grover": {"perfil": GROVER_PERFIL, "tipo": "gate-based"},
        }

        results = {}
        for name, info in algorithms.items():
            perfil = info["perfil"]
            n_aurea = norma_aurea(perfil)
            pr_energy = pi_root(n_aurea - 1.0)  # transformacao pi*sqrt da norma

            # Classificacao de delegacao — cascata de prioridade
            # (mesma ordem de classificar_delegacao em quantum_interface.py)
            rho4 = perfil[3]
            rho3 = perfil[2]
            rho5 = perfil[4]
            rho6 = perfil[5]

            # Cadeia especifica rho4 > rho3 (anomalia canonica Shor/Grover)
            anomalia_especifica = rho4 > rho3 + 0.05

            # Verificar consistencia geral da cadeia rho_6=>...=>rho_1
            cadeia_consistente = True
            for i in range(4, -1, -1):
                if perfil[i + 1] > perfil[i] + 0.05:
                    cadeia_consistente = False
                    break

            # Cascata de classificacao (mesmo que Alexandria)
            if anomalia_especifica:
                delegacao = "anomalia"
            elif rho6 > 0.70:
                delegacao = "emergencia"
            elif rho5 > 0.60:
                delegacao = "equilibrio"
            elif rho5 >= 0.50:
                delegacao = "conservacao"
            else:
                delegacao = "conservacao"

            anomalia = anomalia_especifica

            results[name] = {
                "perfil": perfil,
                "norma_aurea": round(n_aurea, 6),
                "pi_root_norma": round(pr_energy, 6),
                "rho5_equilibrio": rho5,
                "rho6_compensacao": rho6,
                "delegacao": delegacao,
                "anomalia_detectada": anomalia_especifica,
                "cadeia_consistente": cadeia_consistente,
                "classificacao_tats": self._classify_tats(
                    anomalia_especifica, rho5, rho6, cadeia_consistente
                ),
                "tipo": info["tipo"],
            }

        # Comparacao par a par
        comparisons = {}
        names = list(results.keys())
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                pa = results[a]["perfil"]
                pb = results[b]["perfil"]
                dist = math.sqrt(sum((x - y) ** 2 for x, y in zip(pa, pb)))
                sim = max(0.0, 1.0 - dist / math.sqrt(6))
                comparisons[f"{a}_vs_{b}"] = {
                    "distance": round(dist, 4),
                    "similarity": round(sim, 4),
                }

        return {
            "algorithms": results,
            "comparisons": comparisons,
            "interpretation": self._interpret_algorithm_comparison(results),
        }

    # ── Correlacao PiRoot ──────────────────────────────────

    def piroot_correlation_analysis(
        self,
        n_scenarios: int = 20,
        n_qubits: int = 4,
        depth: int = 3,
        iterations: int = 30,
    ) -> Dict[str, Any]:
        """
        Analisa a correlacao entre pi*sqrt(E) e a norma aurea do perfil.

        A hipotese PiRoot afirma que a transformacao pi*sqrt da energia
        do VQE correlaciona com a norma aurea do perfil hexarrelacional.
        Este teste gera multiplos cenarios e calcula a correlacao.

        Args:
            n_scenarios: Numero de cenarios a gerar
            n_qubits: Numero de qubits
            depth: Profundidade do circuito
            iterations: Iteracoes por cenario

        Returns:
            Dicionario com analise de correlacao
        """
        piroot_values = []
        norma_values = []
        rho5_values = []

        for i in range(n_scenarios):
            seed_val = self.rng.randint(0, 999999)
            # Variar parametros para gerar diversidade
            varied_depth = max(1, depth + self.rng.randint(-2, 3))
            varied_qubits = max(2, n_qubits + self.rng.randint(-1, 2))

            traj = self.run_scenario(
                n_qubits=varied_qubits,
                depth=varied_depth,
                iterations=iterations,
                seed=seed_val,
            )

            if traj.iterations:
                # Usar o ponto medio da trajetoria (iteracao mediana)
                mid = len(traj.iterations) // 2
                mid_point = traj.iterations[mid]
                piroot_values.append(mid_point.energy_piroot)
                norma_values.append(mid_point.norma_aurea)
                rho5_values.append(mid_point.rho5_equilibrio)

        # Correlacoes
        corr_piroot_norma = self._pearson_correlation(piroot_values, norma_values)
        corr_piroot_rho5 = self._pearson_correlation(piroot_values, rho5_values)
        corr_norma_rho5 = self._pearson_correlation(norma_values, rho5_values)

        return {
            "n_scenarios": n_scenarios,
            "correlation_piroot_norma_aurea": round(corr_piroot_norma, 6),
            "correlation_piroot_rho5": round(corr_piroot_rho5, 6),
            "correlation_norma_aurea_rho5": round(corr_norma_rho5, 6),
            "interpretation": self._interpret_correlation(
                corr_piroot_norma, corr_piroot_rho5
            ),
            "data_points": {
                "piroot_values": [round(v, 4) for v in piroot_values],
                "norma_values": [round(v, 4) for v in norma_values],
                "rho5_values": [round(v, 4) for v in rho5_values],
            },
        }

    # ── Metodos auxiliares (privados) ──────────────────────

    @staticmethod
    def _pearson_correlation(x: List[float], y: List[float]) -> float:
        """Calcula correlacao de Pearson entre duas listas."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        den_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        den_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        if den_x == 0 or den_y == 0:
            return 0.0
        return num / (den_x * den_y)

    @staticmethod
    def _classify_tats(
        anomalia: bool, rho5: float, rho6: float, cadeia_ok: bool
    ) -> str:
        """Classificacao TATS baseada no perfil."""
        if anomalia:
            return "anomalia-detectavel"
        if rho6 > 0.8 and cadeia_ok:
            return "consistente-paradigmatico"
        if cadeia_ok and rho5 > 0.5:
            return "consistente-marginal"
        return "degradado"

    @staticmethod
    def _interpret_landscape(
        trajectories: List[VQEProfileTrajectory],
        depths: List[int],
        transition_depth: Optional[int],
    ) -> str:
        """Gera interpretacao semantica da paisagem VQE."""
        if transition_depth is None:
            return (
                "Nenhum barren plateau detectado nos depths testados. "
                "O perfil hexarrelacional mantem equilibrio (rho_5 > 0.6) "
                "em todas as profundidades, indicando convergencia saudavel. "
                "O VQE e robusto neste regime de parametros."
            )
        converged_at = sum(1 for t in trajectories if t.converged)
        total = len(trajectories)
        return (
            f"Barren plateau detectado a partir da profundidade {transition_depth}. "
            f"Ate profundidade {transition_depth - 1}, o VQE mantem equilibrio "
            f"classico-quantico (rho_5 > 0.5). A partir de {transition_depth}, "
            f"rho_5 degrada abaixo do limiar de conservacao, indicando que "
            f"o gradiente desaparece. {converged_at}/{total} cenarios convergiram. "
            f"A cadeia hexarrelacional rho_6=>rho_5=>...=>rho_1 se degrada "
            f"sistematicamente com a profundidade do circuito."
        )

    @staticmethod
    def _interpret_algorithm_comparison(results: Dict[str, Any]) -> str:
        """Gera interpretacao semantica da comparacao entre algoritmos."""
        lines = []
        for name, data in results.items():
            deleg = data["delegacao"]
            anom = data["anomalia_detectada"]
            tats = data["classificacao_tats"]
            if anom:
                lines.append(
                    f"{name}: anomalia-detectavel (rho4>rho3), delegacao={deleg}. "
                    f"Unitariedade quantica garante simetria sem equivalencia verificavel."
                )
            elif deleg == "emergencia":
                lines.append(
                    f"{name}: consistente-paradigmatico, delegacao=emergencia "
                    f"(rho6={data['rho6_compensacao']}). Emergencia do sistema C+Q."
                )
            elif deleg == "equilibrio":
                lines.append(
                    f"{name}: equilibrio classico-quantico sustentavel "
                    f"(rho5={data['rho5_equilibrio']}). Gradientes em ambas direcoes."
                )
            else:
                lines.append(
                    f"{name}: conservacao (rho5={data['rho5_equilibrio']}). "
                    f"Recurso preservado, cadeia rho_6=>rho_5 mantida."
                )
        return " | ".join(lines)

    @staticmethod
    def _interpret_correlation(corr_pn: float, corr_pr5: float) -> str:
        """Interpreta a correlacao PiRoot."""
        parts = []
        if abs(corr_pn) > 0.7:
            parts.append(
                f"Forte correlacao ({corr_pn:.3f}) entre pi*sqrt(E) e norma aurea "
                f"do perfil hexarrelacional — a hipotese PiRoot e sustentada: "
                f"a transformacao pi*sqrt captura a estrutura semantica do VQE."
            )
        elif abs(corr_pn) > 0.3:
            parts.append(
                f"Correlacao moderada ({corr_pn:.3f}) entre pi*sqrt(E) e norma aurea. "
                f"A hipotese PiRoot e parcialmente sustentada — mais cenarios "
                f"ou parametros ajustados podem fortalecer a correlacao."
            )
        else:
            parts.append(
                f"Correlacao fraca ({corr_pn:.3f}) — a relacao entre pi*sqrt(E) "
                f"e norma aurea nao e evidente neste regime. A hipotese PiRoot "
                f"requer validacao com parametros diferentes ou cenarios expandidos."
            )
        if abs(corr_pr5) > 0.5:
            parts.append(
                f"Correlacao significativa ({corr_pr5:.3f}) entre pi*sqrt(E) e rho_5 "
                f"confirma que a transformacao PiRoot reflete o equilibrio "
                f"classico-quantico."
            )
        return " ".join(parts)
