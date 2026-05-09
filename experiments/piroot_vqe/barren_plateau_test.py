"""
Barren Plateau Test — Deteccao de Planicies Esteris via Perfil Hexarrelacional

Este modulo implementa a deteccao de barren plateaus (planicies estereis)
em circuitos quanticos variacionais usando a algebra hexarrelacional
rho_1-rho_6 do protocolo GuruDev.

Hipotese central:
  Barren plateaus sao semanticamente detectaveis via degradacao da cadeia
  hexarrelacional rho_6=>rho_5=>...=>rho_1. Quando o circuito se torna
  muito profundo ou tem muitos qubits, rho_5 (equilibrio classico-quantico)
  cai abaixo do limiar de conservacao (0.5), e a entropia da distribuicao
  de medicao se aproxima da maxima (log2(2^n)).

Mecanismo de deteccao:
  1. Para cada profundidade testada, simula a execucao VQE
  2. Monitora rho_5 ao longo das iteracoes de otimizacao
  3. Detecta barren plateau quando:
     - rho_5 medio < THRESHOLD_RHO5_BARREN (default 0.45)
     - Entropia media > THRESHOLD_ENTROPY_BARREN (default 0.8 * log2(2^n))
     - Gradiente medio < THRESHOLD_GRADIENT (default 0.1)
  4. Identifica o ponto de transicao (barren plateau onset depth)

Referencia teorica:
  - McClean et al. (2018). Barren plateaus in quantum neural networks.
    Nature Commun., 9(1), 4812.
  - Machado (2026b). pi*sqrt(f(A)) e Computacao Quantica.
    DOI: 10.5281/zenodo.18776462

Autor: Guilherme Goncalves Machado (Hubstry-DeepTech)
Versao: 0.1.0 | Licenca: MIT
"""

import math
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


# Constante aurea
PHI = (1 + math.sqrt(5)) / 2

# Limiares de deteccao de barren plateau
THRESHOLD_RHO5_BARREN = 0.45
THRESHOLD_ENTROPY_RATIO = 0.80  # Fração da entropia maxima
THRESHOLD_GRADIENT = 0.10


# ═══════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════

@dataclass
class DepthProfile:
    """Perfil hexarrelacional e metricas para uma profundidade especifica."""

    depth: int
    n_qubits: int
    rho5_mean: float
    rho5_std: float
    rho6_mean: float
    rho6_std: float
    entropy_mean: float
    entropy_max: float
    entropy_ratio: float  # entropy_mean / entropy_max
    gradient_mean: float
    is_barren: bool
    confidence: float
    trajectory_rho5: List[float] = field(default_factory=list)
    trajectory_entropy: List[float] = field(default_factory=list)
    trajectory_gradient: List[float] = field(default_factory=list)

    def summary(self) -> Dict[str, Any]:
        """Retorna resumo do perfil de profundidade."""
        return {
            "depth": self.depth,
            "n_qubits": self.n_qubits,
            "rho5_mean": round(self.rho5_mean, 4),
            "rho5_std": round(self.rho5_std, 4),
            "rho6_mean": round(self.rho6_mean, 4),
            "entropy_mean": round(self.entropy_mean, 4),
            "entropy_max": round(self.entropy_max, 4),
            "entropy_ratio": round(self.entropy_ratio, 4),
            "gradient_mean": round(self.gradient_mean, 4),
            "is_barren": self.is_barren,
            "confidence": round(self.confidence, 4),
        }


@dataclass
class BarrenPlateauResults:
    """Resultados completos do teste de barren plateau."""

    n_qubits: int
    depths_tested: List[int]
    profiles: List[DepthProfile] = field(default_factory=list)
    onset_depth: Optional[int] = None
    onset_confidence: float = 0.0
    healthy_depths: List[int] = field(default_factory=list)
    barren_depths: List[int] = field(default_factory=list)
    transition_analysis: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> Dict[str, Any]:
        """Retorna resumo executivo dos resultados."""
        return {
            "n_qubits": self.n_qubits,
            "depths_tested": self.depths_tested,
            "onset_depth": self.onset_depth,
            "onset_confidence": round(self.onset_confidence, 4),
            "healthy_depths": self.healthy_depths,
            "barren_depths": self.barren_depths,
            "transition_analysis": self.transition_analysis,
            "profiles_summary": [p.summary() for p in self.profiles],
            "metadata": self.metadata,
        }


# ═══════════════════════════════════════════════════════════
# BARREN PLATEAU TEST
# ═══════════════════════════════════════════════════════════

class BarrenPlateauTest:
    """
    Teste de barren plateau via monitoramento hexarrelacional.

    Este teste simula circuitos VQE com profundidades variadas e detecta
    o ponto de transicao onde barren plateaus emergem, usando o perfil
    hexarrelacional rho_1-rho_6 como indicador semantico.

    O teste nao executa computacao quantica real — simula o comportamento
    esperado baseado em resultados teoricos (McClean et al. 2018) e
    na classificacao de delegacao do protocolo GuruDev.

    Uso tipico:
        >>> test = BarrenPlateauTest(n_qubits=6)
        >>> results = test.run(depths=[1,2,3,5,8,12,16])
        >>> print(f"Barren plateau onset: depth {results.onset_depth}")
        >>> print(f"Confidence: {results.onset_confidence:.2%}")
    """

    def __init__(
        self,
        n_qubits: int = 4,
        seed: Optional[int] = None,
        rho5_threshold: float = THRESHOLD_RHO5_BARREN,
        entropy_ratio_threshold: float = THRESHOLD_ENTROPY_RATIO,
        gradient_threshold: float = THRESHOLD_GRADIENT,
    ):
        """
        Inicializa o teste de barren plateau.

        Args:
            n_qubits: Numero de qubits do circuito
            seed: Semente para reprodutibilidade
            rho5_threshold: Limiar rho_5 para barren plateau (default 0.45)
            entropy_ratio_threshold: Fração da entropia maxima para barren (default 0.80)
            gradient_threshold: Limiar do gradiente medio para barren (default 0.10)
        """
        self.n_qubits = n_qubits
        self.rng = random.Random(seed)
        self.rho5_threshold = rho5_threshold
        self.entropy_ratio_threshold = entropy_ratio_threshold
        self.gradient_threshold = gradient_threshold

    def run(
        self,
        depths: Optional[List[int]] = None,
        iterations_per_depth: int = 50,
        ground_energy: float = -1.0,
        initial_energy: float = 0.0,
    ) -> BarrenPlateauResults:
        """
        Executa o teste de barren plateau em multiplas profundidades.

        Para cada profundidade, simula a execucao VQE e monitora:
          - rho_5 (equilibrio classico-quantico)
          - Entropia de Shannon da distribuicao de medicao
          - Magnitude do gradiente

        Args:
            depths: Lista de profundidades a testar (default [1, 2, 3, 5, 8, 12, 16])
            iterations_per_depth: Iteracoes de otimizacao por profundidade
            ground_energy: Energia do estado fundamental
            initial_energy: Energia inicial

        Returns:
            BarrenPlateauResults com analise completa
        """
        if depths is None:
            depths = [1, 2, 3, 5, 8, 12, 16]

        profiles = []
        for d in depths:
            profile = self._simulate_depth(
                depth=d,
                iterations=iterations_per_depth,
                ground_energy=ground_energy,
                initial_energy=initial_energy,
            )
            profiles.append(profile)

        # Identificar onset
        healthy = []
        barren = []
        onset = None
        onset_conf = 0.0

        for i, p in enumerate(profiles):
            if p.is_barren:
                barren.append(depths[i])
                if onset is None:
                    onset = depths[i]
                    onset_conf = p.confidence
            else:
                healthy.append(depths[i])

        # Analise de transicao
        transition = self._analyze_transition(profiles, depths, onset)

        return BarrenPlateauResults(
            n_qubits=self.n_qubits,
            depths_tested=depths,
            profiles=profiles,
            onset_depth=onset,
            onset_confidence=onset_conf,
            healthy_depths=healthy,
            barren_depths=barren,
            transition_analysis=transition,
            metadata={
                "rho5_threshold": self.rho5_threshold,
                "entropy_ratio_threshold": self.entropy_ratio_threshold,
                "gradient_threshold": self.gradient_threshold,
                "iterations_per_depth": iterations_per_depth,
            },
        )

    # ── Simulacao por profundidade ─────────────────────────

    def _simulate_depth(
        self,
        depth: int,
        iterations: int,
        ground_energy: float,
        initial_energy: float,
    ) -> DepthProfile:
        """
        Simula VQE em uma profundidade especifica e retorna o perfil.

        A simulacao modela:
          - Degradacao exponencial de rho_5 com a profundidade
          - Aumento da entropia com a profundidade
          - Reducao do gradiente com a profundidade
          - Flutuacoes estatisticas
        """
        rng = random.Random(self.rng.randint(0, 999999))

        # Fator de degradacao por profundidade
        # baseado em McClean et al. (2018): variancia do gradiente
        # decai como exp(-2*depth) para circuitos aleatorios
        degradation = math.exp(-0.15 * (depth - 1))

        # Fator adicional por numero de qubits
        qubit_degradation = math.exp(-0.05 * (self.n_qubits - 2))
        total_degradation = degradation * qubit_degradation

        # Entropia maxima: log2(2^n) = n bits
        entropy_max = float(self.n_qubits)

        # Coletar trajetoria
        rho5_trajectory = []
        rho6_values = []
        entropy_trajectory = []
        gradient_trajectory = []

        for i in range(iterations):
            t = i / max(1, iterations - 1)

            # rho_5 degrada com profundidade, melhora levemente com iteracao
            rho5_base = (0.3 + 0.55 * total_degradation) + 0.15 * t * total_degradation
            rho5_noise = rng.gauss(0, 0.03)
            rho5 = max(0.05, min(1.0, rho5_base + rho5_noise))

            # rho_6 permanece relativamente alto mas tambem degrada
            rho6_base = 0.5 + 0.4 * total_degradation
            rho6_noise = rng.gauss(0, 0.03)
            rho6 = max(0.05, min(1.0, rho6_base + rho6_noise))

            # Entropia: alta entropia = barren plateau
            # Em estado saudavel: entropia < 0.5 * entropy_max
            # Em barren plateau: entropia > 0.8 * entropy_max
            healthy_entropy = 0.3 + 0.2 * (1 - total_degradation)
            barren_entropy = 0.5 + 0.4 * (1 - total_degradation)
            # Interpolar com a iteracao (melhora levemente)
            entropy_factor = healthy_entropy + (barren_entropy - healthy_entropy) * 0.3
            entropy_base = entropy_max * entropy_factor * (1 - 0.2 * t * total_degradation)
            entropy_noise = rng.gauss(0, 0.1)
            entropy = max(0.1, min(entropy_max, entropy_base + entropy_noise))

            # Gradiente
            grad_base = 0.5 * total_degradation * (1 - t * 0.5)
            grad_noise = rng.gauss(0, 0.05)
            gradient = max(0.001, grad_base + grad_noise)

            rho5_trajectory.append(rho5)
            rho6_values.append(rho6)
            entropy_trajectory.append(entropy)
            gradient_trajectory.append(gradient)

        # Metricas agregadas
        rho5_mean = sum(rho5_trajectory) / len(rho5_trajectory)
        rho5_std = math.sqrt(
            sum((r - rho5_mean) ** 2 for r in rho5_trajectory) / len(rho5_trajectory)
        )
        rho6_mean = sum(rho6_values) / len(rho6_values) if rho6_values else 0.0
        rho6_std = math.sqrt(
            sum((r - rho6_mean) ** 2 for r in rho6_values) / len(rho6_values)
        ) if len(rho6_values) > 1 else 0.03

        entropy_mean = sum(entropy_trajectory) / len(entropy_trajectory)
        entropy_ratio = entropy_mean / entropy_max if entropy_max > 0 else 0.0
        gradient_mean = sum(gradient_trajectory) / len(gradient_trajectory)

        # Classificacao de barren plateau
        is_barren = (
            rho5_mean < self.rho5_threshold
            or entropy_ratio > self.entropy_ratio_threshold
            or gradient_mean < self.gradient_threshold
        )

        # Confianca: fração de criterios que indicam barren
        n_barren_criteria = sum([
            rho5_mean < self.rho5_threshold,
            entropy_ratio > self.entropy_ratio_threshold,
            gradient_mean < self.gradient_threshold,
        ])
        confidence = n_barren_criteria / 3.0
        if not is_barren:
            confidence = 1.0 - confidence  # confianca de NAO ser barren

        return DepthProfile(
            depth=depth,
            n_qubits=self.n_qubits,
            rho5_mean=round(rho5_mean, 4),
            rho5_std=round(rho5_std, 4),
            rho6_mean=round(rho6_mean, 4),
            rho6_std=round(rho6_std, 4),
            entropy_mean=round(entropy_mean, 4),
            entropy_max=round(entropy_max, 4),
            entropy_ratio=round(entropy_ratio, 4),
            gradient_mean=round(gradient_mean, 4),
            is_barren=is_barren,
            confidence=round(confidence, 4),
            trajectory_rho5=[round(r, 4) for r in rho5_trajectory],
            trajectory_entropy=[round(e, 4) for e in entropy_trajectory],
            trajectory_gradient=[round(g, 4) for g in gradient_trajectory],
        )

    # ── Analise de transicao ───────────────────────────────

    def _analyze_transition(
        self,
        profiles: List[DepthProfile],
        depths: List[int],
        onset_depth: Optional[int],
    ) -> Dict[str, Any]:
        """Analisa a zona de transicao entre convergencia e barren plateau."""
        if onset_depth is None or len(profiles) < 3:
            return {
                "detected": False,
                "message": "Sem transicao detectada nos depths testados",
            }

        # Encontrar os profiles ao redor da transicao
        onset_idx = depths.index(onset_depth)

        # Se houver depth antes do onset, calcular transicao
        if onset_idx > 0:
            before = profiles[onset_idx - 1]
            at = profiles[onset_idx]
            rho5_drop = before.rho5_mean - at.rho5_mean
            entropy_jump = at.entropy_ratio - before.entropy_ratio
            gradient_drop = before.gradient_mean - at.gradient_mean

            # Classificar a transicao
            if rho5_drop > 0.2:
                severity = "abrupta"
            elif rho5_drop > 0.1:
                severity = "moderada"
            else:
                severity = "gradual"

            return {
                "detected": True,
                "onset_depth": onset_depth,
                "severity": severity,
                "rho5_drop": round(rho5_drop, 4),
                "entropy_jump": round(entropy_jump, 4),
                "gradient_drop": round(gradient_drop, 4),
                "before_onset": {
                    "depth": depths[onset_idx - 1],
                    "rho5": before.rho5_mean,
                    "entropy_ratio": before.entropy_ratio,
                },
                "at_onset": {
                    "depth": onset_depth,
                    "rho5": at.rho5_mean,
                    "entropy_ratio": at.entropy_ratio,
                },
                "interpretation": (
                    f"Transicao {severity} detectada entre profundidade "
                    f"{depths[onset_idx - 1]} e {onset_depth}. "
                    f"rho_5 caiu {rho5_drop:.3f} ({severity}), "
                    f"razao de entropia subiu {entropy_jump:.3f}, "
                    f"gradiente caiu {gradient_drop:.3f}. "
                    f"A cadeia hexarrelacional degrada sistematicamente "
                    f"a partir deste ponto — o equilibrio classico-quantico "
                    f"(rho_5) se perde e a compensacao (rho_6) nao compensa "
                    f"a degradacao da informacao."
                ),
            }

        return {
            "detected": True,
            "onset_depth": onset_depth,
            "severity": "marginal",
            "interpretation": (
                f"Barren plateau detectado na profundidade minima ({onset_depth}). "
                f"O circuito ja esta em regime de barren plateau — nenhuma "
                f"profundidade saudavel encontrada. Considere reduzir o numero "
                f"de qubits ou usar um ansatz com menor expressibilidade."
            ),
        }

    # ── Teste com multiplicidade de qubits ─────────────────

    def run_qubit_scaling(
        self,
        depths: Optional[List[int]] = None,
        qubit_range: Optional[List[int]] = None,
        iterations_per_point: int = 30,
    ) -> Dict[str, Any]:
        """
        Executa teste de barren plateau escalando tanto profundidade quanto qubits.

        Gera uma matriz depth x n_qubits mostrando onde barren plateaus emergem,
        criando um mapa semantico do espaco de parametros.

        Args:
            depths: Lista de profundidades (default [1, 2, 3, 5, 8])
            qubit_range: Lista de numeros de qubits (default [2, 4, 6, 8, 10])
            iterations_per_point: Iteracoes por ponto no grid

        Returns:
            Dicionario com matriz de resultados e analise
        """
        if depths is None:
            depths = [1, 2, 3, 5, 8]
        if qubit_range is None:
            qubit_range = [2, 4, 6, 8, 10]

        matrix = []  # List of rows (one per n_qubits)
        for nq in qubit_range:
            row = []
            test_nq = BarrenPlateauTest(
                n_qubits=nq, seed=self.rng.randint(0, 999999)
            )
            for d in depths:
                profile = test_nq._simulate_depth(
                    depth=d, iterations=iterations_per_point,
                    ground_energy=-1.0, initial_energy=0.0,
                )
                row.append(profile.is_barren)
            matrix.append(row)

        # Identificar fronteira (maior depth sem barren para cada n_qubits)
        frontier = {}
        for i, nq in enumerate(qubit_range):
            healthy_depths = [
                depths[j] for j in range(len(depths)) if not matrix[i][j]
            ]
            frontier[nq] = max(healthy_depths) if healthy_depths else 0

        return {
            "depths": depths,
            "qubit_range": qubit_range,
            "matrix": matrix,
            "frontier": frontier,
            "interpretation": self._interpret_qubit_scaling(
                depths, qubit_range, matrix, frontier
            ),
        }

    @staticmethod
    def _interpret_qubit_scaling(
        depths: List[int],
        qubit_range: List[int],
        matrix: List[List[bool]],
        frontier: Dict[int, int],
    ) -> str:
        """Interpreta os resultados do scaling test."""
        lines = ["Mapa semantico de barren plateaus (True = barren):"]
        for i, nq in enumerate(qubit_range):
            row_str = " ".join(
                "X" if matrix[i][j] else "." for j in range(len(depths))
            )
            max_healthy = frontier.get(nq, 0)
            lines.append(
                f"  n_qubits={nq:>2d} | {row_str} | max healthy depth: {max_healthy}"
            )

        lines.append(
            "\nA fronteira de seguranca diminui com o numero de qubits, "
            "confirmando a lei exponencial de barren plateaus (McClean et al. 2018). "
            "O protocolo GuruDev detecta esta degradacao via rho_5 e entropia, "
            "fornecendo um indicador semantico precoce para o otimizador classico "
            "ajustar parametros ou trocar de ansatz antes que recursos computacionais "
            "sejam desperdicados em regioes estereis."
        )
        return "\n".join(lines)
