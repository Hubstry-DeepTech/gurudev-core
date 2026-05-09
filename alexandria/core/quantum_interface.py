"""
Modulo de Interface Quantica — Classificador de Delegacao

Implementa o protocolo semantico da interface classico-quântica do GuruDev.
GuruDev NAO é uma linguagem quantica — é o protocolo semântico que governa
a delegação classico-quântica, como TCP/IP para redes.

Este modulo define:
  - 4 tipos de delegação: EMERGENCIA, ANOMALIA, EQUILIBRIO, CONSERVACAO
  - Verificação de contenção constitucional quântica (AUSENTES_QUANTICO)
  - Classificação de perfis hexarrelacionais por tipo de delegação
  - Perfis conjecturais constantes para linguagens quânticas

Autor: Guilherme Goncalves Machado (Hubstry-DeepTech)
Versao: 0.3.0 | Licenca: MIT
Referencia: Machado (2026b). pi*sqrt(f(A)) e Computacao Quantica.
    DOI: 10.5281/zenodo.18776462
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════
# ENUM — Tipos de Delegação Quântica
# ═══════════════════════════════════════════════════════════

class TipoDelegacao(Enum):
    """
    Tipos de delegação classico-quântica no protocolo GuruDev.

    Cada tipo define a relação semântica entre o código GuruDev (clássico)
    e a operação quântica delegada. A classificação usa os perfis ρ₁-ρ₆
    da álgebra hexarrelacional de significância.

    - EMERGENCIA: rho6 > 0.7 — compensação emerge do sistema composto C+Q.
      O resultado quântico não pode ser reproduzido por simulação clássica.
      Caso canônico: VQE, QAOA.

    - ANOMALIA: rho4 > rho3 — simetria sem equivalência verificável.
      A cadeia de implicação ρ₆⇒ρ₅⇒...⇒ρ₁ é violada.
      Caso canônico: Shor (QFT), Grover (reflexões).

    - EQUILIBRIO: rho5 > 0.6 — equilíbrio clássico-quântico sustentável.
      O gradiente de correção flui em ambas as direções.
      Caso canônico: PennyLane, Quantum ML.

    - CONSERVACAO: rho5 como recurso preservado — a cadeia ρ₆⇒ρ₅ é usada
      como garantia de que a informação quântica não é dissipada.
      Caso canônico: QKD (distribuição de chaves quânticas), Seção 6.5.
    """
    EMERGENCIA = "emergencia"
    ANOMALIA = "anomalia"
    EQUILIBRIO = "equilibrio"
    CONSERVACAO = "conservacao"


# ═══════════════════════════════════════════════════════════
# CONSTITUCIONAL — Operações Ausentes (não proibidas)
# ═══════════════════════════════════════════════════════════

# Operações arquiteturalmente AUSENTES no protocolo.
# Não são proibidas — são constitucionalmente inexistentes.
# GuruDev não as implementa porque violam os princípios
# fundamentais da contenção constitucional quântica.
AUSENTES_QUANTICO: Set[str] = {
    "clonar_estado",       # Teorema da não-clonagem (ρ₃ limit)
    "medir_sem_colapso",   # Colapso é irreversível por construção
    "copiar_qubit",        # Consequência do teorema da não-clonagem
    "determinar_fase",     # Fase global é fisicamente inacessível
}


# ═══════════════════════════════════════════════════════════
# THRESHOLDS — Limiares de Classificação
# ═══════════════════════════════════════════════════════════

THRESHOLD_EMERGENCIA_RHO6 = 0.70   # ρ₆ > 0.70 → EMERGENCIA
THRESHOLD_ANOMALIA_DELTA = 0.05    # ρ₄ - ρ₃ > 0.05 → ANOMALIA
THRESHOLD_EQUILIBRIO_RHO5 = 0.60   # ρ₅ > 0.60 → EQUILIBRIO
THRESHOLD_CONSERVACAO_RHO5 = 0.50  # ρ₅ >= 0.50 + cadeia preservada → CONSERVACAO


# ═══════════════════════════════════════════════════════════
# PERFIS CONJECTURAIS — Constantes para linguagens quânticas
# ═══════════════════════════════════════════════════════════

PERFIS_CONJECTURAIS: Dict[str, Dict[str, Any]] = {
    "Qiskit": {
        "rho": [0.85, 0.70, 0.60, 0.65, 0.50, 0.75],
        "fonte": "Machado 2026b, Secao 5 — inferido de VQE/QAOA",
        "delegacao_esperada": TipoDelegacao.EMERGENCIA,
        "anomalia": False,
    },
    "Q#": {
        "rho": [0.80, 0.75, 0.65, 0.60, 0.45, 0.55],
        "fonte": "Machado 2026b, Secao 5 — inferido de topological qubits",
        "delegacao_esperada": TipoDelegacao.CONSERVACAO,
        "anomalia": False,
    },
    "PennyLane": {
        "rho": [0.70, 0.65, 0.50, 0.55, 0.80, 0.70],
        "fonte": "Machado 2026b, Secao 5 — rho5 alto por equilibrio gradiente",
        "delegacao_esperada": TipoDelegacao.EQUILIBRIO,
        "anomalia": False,
    },
    "Cirq": {
        "rho": [0.90, 0.60, 0.55, 0.75, 0.40, 0.50],
        "fonte": "Machado 2026b, Secao 5 — rho1 alto vs Qiskit",
        "delegacao_esperada": TipoDelegacao.ANOMALIA,
        "anomalia": True,
    },
    "Silq": {
        "rho": [0.65, 0.70, 0.55, 0.60, 0.55, 0.85],
        "fonte": "Machado 2026b, Secao 6 — rho6 alto por contencao constitucional",
        "delegacao_esperada": TipoDelegacao.EMERGENCIA,
        "anomalia": False,
    },
    "OpenQASM 3": {
        "rho": [0.75, 0.60, 0.55, 0.85, 0.35, 0.30],
        "fonte": "Machado 2026b, Secao 5 — rho4 alto por bijecao com circuitos",
        "delegacao_esperada": TipoDelegacao.ANOMALIA,
        "anomalia": True,
    },
    "Quipper": {
        "rho": [0.60, 0.75, 0.50, 0.55, 0.40, 0.45],
        "fonte": "Machado 2026b, Secao 5 — inferido de tipos dependentes",
        "delegacao_esperada": TipoDelegacao.CONSERVACAO,
        "anomalia": False,
    },
    "CUDA Quantum": {
        "rho": [0.70, 0.55, 0.45, 0.60, 0.65, 0.80],
        "fonte": "Machado 2026b, Secao 6 — rho6 alto por emergencia hibrida GPU+QPU",
        "delegacao_esperada": TipoDelegacao.EMERGENCIA,
        "anomalia": False,
    },
}

# Perfis conjecturais para algoritmos
PERFIS_ALGORITMOS: Dict[str, Dict[str, Any]] = {
    "Shor": {
        "rho": [0.9, 0.85, 0.3, 0.7, 0.2, 0.5],
        "delegacao_esperada": TipoDelegacao.ANOMALIA,
        "anomalia": True,
        "classificacao_tats": "anomalia-detectavel",
    },
    "Grover": {
        "rho": [0.95, 0.6, 0.7, 0.9, 0.3, 0.2],
        "delegacao_esperada": TipoDelegacao.ANOMALIA,
        "anomalia": True,
        "classificacao_tats": "anomalia-detectavel",
    },
    "VQE": {
        "rho": [0.7, 0.8, 0.5, 0.6, 0.7, 0.9],
        "delegacao_esperada": TipoDelegacao.EMERGENCIA,
        "anomalia": False,
        "classificacao_tats": "consistente-paradigmatico",
    },
    "QAOA": {
        "rho": [0.6, 0.75, 0.4, 0.5, 0.6, 0.7],
        "delegacao_esperada": TipoDelegacao.EMERGENCIA,
        "anomalia": False,
        "classificacao_tats": "consistente-marginal",
    },
}


# ═══════════════════════════════════════════════════════════
# DATACLASS — Resultado da Classificação
# ═══════════════════════════════════════════════════════════

@dataclass
class ResultadoDelegacao:
    """Resultado da classificação de delegação quântica."""

    tipo: TipoDelegacao
    perfil: List[float]
    nome: str
    rho_dominante: str
    rho_dominante_valor: float
    cadeia_consistente: bool
    anomalia_detectada: bool
    par_anomalia: Optional[str] = None
    justificativa: str = ""
    confianca: float = 0.0


@dataclass
class ResultadoContencao:
    """Resultado da verificação de contenção constitucional."""

    operacao: str
    contida: bool
    categoria: str  # "ausente" ou "presente"
    justificativa: str = ""
    limite_constitucional: Optional[str] = None


# ═══════════════════════════════════════════════════════════
# FUNCOES DE CLASSIFICACAO
# ═══════════════════════════════════════════════════════════

def verificar_contencao(operacao: str) -> ResultadoContencao:
    """
    Verifica se uma operação quântica está contida no protocolo GuruDev.

    Operações em AUSENTES_QUANTICO são arquiteturalmente ausentes (não
    proibidas). Elas não existem no protocolo porque violam princípios
    fundamentais da mecânica quântica — não são implementadas, não são
    acessíveis, e não geram erro quando solicitadas (são ignoradas).

    Args:
        operacao: Nome da operação a verificar (case-insensitive)

    Returns:
        ResultadoContencao com diagnostico completo
    """
    op_normalizada = operacao.strip().lower()

    # Verificar se é uma operação ausente
    for ausente in AUSENTES_QUANTICO:
        if op_normalizada == ausente.lower():
            justificativa = _justificativa_ausente(ausente)
            limite = _limite_constitucional(ausente)
            return ResultadoContencao(
                operacao=operacao,
                contida=False,
                categoria="ausente",
                justificativa=justificativa,
                limite_constitucional=limite,
            )

    # Operação não está na lista de ausentes — pode existir
    return ResultadoContencao(
        operacao=operacao,
        contida=True,
        categoria="presente",
        justificativa=f"Operacao '{operacao}' nao esta na lista de operacoes "
                      f"ausentes. Pode ser implementada no protocolo.",
    )


def classificar_delegacao(
    perfil: List[float],
    nome: str = "",
    tolerancia: float = 0.05,
) -> ResultadoDelegacao:
    """
    Classifica um perfil hexarrelacional ρ₁-ρ₆ por tipo de delegação.

    A classificação segue uma cascata de prioridade:
    1. ANOMALIA — ρ₄ > ρ₃ + tolerancia (simetria sem equivalência).
       Caso canônico: Shor (QFT), Grover (reflexões), Cirq, OpenQASM 3.
       NOTA: esta é a anomalia ESPECIFICA do PDF — unitariedade quântica
       garante simetria (ρ₄) sem equivalência verificável (ρ₃).
       Outras violações de cadeia (ρ₆>ρ₅, ρ₅>ρ₄) são esperadas em
       perfis de compensação/emergência e NÃO são classificadas como ANOMALIA.
    2. EMERGENCIA — ρ₆ > 0.70 (compensação emerge do sistema C+Q)
    3. EQUILIBRIO — ρ₅ > 0.60 (equilíbrio clássico-quântico)
    4. CONSERVACAO — ρ₅ >= 0.50 (recurso preservado) ou fallback

    Args:
        perfil: Lista de 6 floats [rho1, ..., rho6] em [0,1]
        nome: Nome da linguagem ou algoritmo (opcional)
        tolerancia: Tolerancia para deteccao de anomalia (default 0.05)

    Returns:
        ResultadoDelegacao com tipo, justificativa e confiança
    """
    if len(perfil) != 6:
        raise ValueError(
            f"Perfil deve ter 6 valores [rho1..rho6], recebido {len(perfil)}"
        )

    rho1, rho2, rho3, rho4, rho5, rho6 = perfil

    # Verificar ANOMALIA especifica: rho4 > rho3 (padrao canonico Shor/Grover)
    anomalia_rho4_rho3 = rho4 > rho3 + tolerancia

    # Verificar consistencia geral da cadeia (para informacao, nao classificacao)
    cadeia_violada = False
    par_violado = None
    for i in range(4, -1, -1):
        if perfil[i + 1] > perfil[i] + tolerancia:
            cadeia_violada = True
            par_violado = f"rho{i + 2} > rho{i + 1}"
            break

    # Determinar rho dominante
    rho_labels = ["rho1", "rho2", "rho3", "rho4", "rho5", "rho6"]
    max_idx = perfil.index(max(perfil))
    rho_dom = rho_labels[max_idx]
    rho_dom_val = perfil[max_idx]

    # Classificação em cascata de prioridade
    tipo = None
    justificativa = ""
    confianca = 0.0

    # 1. ANOMALIA — rho4 > rho3 (simetria sem equivalência verificável)
    if anomalia_rho4_rho3:
        tipo = TipoDelegacao.ANOMALIA
        delta = rho4 - rho3
        confianca = min(1.0, delta / 0.5)
        justificativa = (
            f"Anomalia: rho4={rho4:.2f} > rho3={rho3:.2f}. "
            f"Simetria sem equivalencia verificavel — propriedade detectavel, "
            f"nao bug. Unitariedade quantica garante rho4 sem rho3. "
            f"Caso canonico: Shor (QFT), Grover (reflexoes)."
        )

    # 2. EMERGENCIA — rho6 > 0.70
    elif rho6 > THRESHOLD_EMERGENCIA_RHO6:
        tipo = TipoDelegacao.EMERGENCIA
        confianca = min(1.0, (rho6 - THRESHOLD_EMERGENCIA_RHO6) / 0.30)
        justificativa = (
            f"rho6={rho6:.2f} > {THRESHOLD_EMERGENCIA_RHO6} — compensacao emerge "
            f"do sistema composto C+Q. Omega(C+Q) >> Omega(C) + Omega(Q). "
            f"Caso canonico: VQE, QAOA, Silq (contencao constitucional)."
        )

    # 3. EQUILIBRIO — rho5 > 0.60
    elif rho5 > THRESHOLD_EQUILIBRIO_RHO5:
        tipo = TipoDelegacao.EQUILIBRIO
        confianca = min(1.0, (rho5 - THRESHOLD_EQUILIBRIO_RHO5) / 0.40)
        justificativa = (
            f"rho5={rho5:.2f} > {THRESHOLD_EQUILIBRIO_RHO5} — equilibrio "
            f"classico-quantico sustentavel. Gradientes fluem em ambas direcoes. "
            f"Caso canonico: PennyLane, Quantum ML."
        )

    # 4. CONSERVACAO — rho5 >= 0.50
    elif rho5 >= THRESHOLD_CONSERVACAO_RHO5:
        tipo = TipoDelegacao.CONSERVACAO
        confianca = min(1.0, rho5 / 1.0)
        justificativa = (
            f"rho5={rho5:.2f} >= {THRESHOLD_CONSERVACAO_RHO5} — cadeia "
            f"preservada, rho5 como recurso. Garantia de que informacao "
            f"quantica nao e dissipada. Caso canonico: QKD (Secao 6.5)."
        )

    # 5. Fallback → CONSERVACAO
    else:
        tipo = TipoDelegacao.CONSERVACAO
        confianca = 0.3
        justificativa = (
            f"Perfil nao atende criterios especificos. "
            f"Delegacao padrao: CONSERVACAO (protocolo minimo)."
        )

    return ResultadoDelegacao(
        tipo=tipo,
        perfil=perfil,
        nome=nome,
        rho_dominante=rho_dom,
        rho_dominante_valor=rho_dom_val,
        cadeia_consistente=not cadeia_violada,
        anomalia_detectada=anomalia_rho4_rho3,
        par_anomalia="rho4 > rho3" if anomalia_rho4_rho3 else None,
        justificativa=justificativa,
        confianca=round(confianca, 4),
    )


def classificar_por_nome(nome: str) -> Optional[ResultadoDelegacao]:
    """
    Classifica uma linguagem ou algoritmo pelo nome usando PERFIS_CONJECTURAIS.

    Args:
        nome: Nome da linguagem (Qiskit, Cirq, ...) ou algoritmo (Shor, VQE, ...)

    Returns:
        ResultadoDelegacao ou None se nao encontrado
    """
    # Buscar em linguagens
    if nome in PERFIS_CONJECTURAIS:
        dados = PERFIS_CONJECTURAIS[nome]
        return classificar_delegacao(dados["rho"], nome=nome)

    # Buscar em algoritmos
    if nome in PERFIS_ALGORITMOS:
        dados = PERFIS_ALGORITMOS[nome]
        return classificar_delegacao(dados["rho"], nome=nome)

    return None


def classificar_todos() -> List[ResultadoDelegacao]:
    """
    Classifica todas as linguagens e algoritmos com perfis conjecturais.

    Returns:
        Lista de ResultadoDelegacao para todas as entradas
    """
    resultados = []
    for nome in PERFIS_CONJECTURAIS:
        resultado = classificar_delegacao(
            PERFIS_CONJECTURAIS[nome]["rho"], nome=nome
        )
        resultados.append(resultado)
    for nome in PERFIS_ALGORITMOS:
        resultado = classificar_delegacao(
            PERFIS_ALGORITMOS[nome]["rho"], nome=nome
        )
        resultados.append(resultado)
    return resultados


def listar_ausentes() -> Set[str]:
    """Retorna o conjunto de operações quânticas arquiteturalmente ausentes."""
    return AUSENTES_QUANTICO.copy()


def resumo_ausentes() -> List[Dict[str, str]]:
    """
    Retorna lista detalhada de operações ausentes com justificativas.

    Returns:
        Lista de dicionarios com operacao, justificativa e limite
    """
    resultado = []
    for op in sorted(AUSENTES_QUANTICO):
        resultado.append({
            "operacao": op,
            "justificativa": _justificativa_ausente(op),
            "limite_constitucional": _limite_constitucional(op),
        })
    return resultado


# ═══════════════════════════════════════════════════════════
# FUNCOES AUXILIARES (internas)
# ═══════════════════════════════════════════════════════════

def _justificativa_ausente(operacao: str) -> str:
    """Retorna justificativa teórica para uma operação ausente."""
    justificativas = {
        "clonar_estado": (
            "Teorema da nao-clonagem (Wootters & Zurek, 1982): "
            "nao existe operacao unitaria que copie um estado quantico "
            "arbitrario. Equivalente ao limite de equivalencia (rho3) "
            "na algebra hexarrelacional."
        ),
        "medir_sem_colapso": (
            "Postulado da medida: toda medida em um estado superposto "
            "causa colapso para um autoestado do observavel. "
            "Nao-medicao sem colapso viola a mecanica quantica — "
            "equivalente a romper a cadeia de implicacao rho6=>rho1."
        ),
        "copiar_qubit": (
            "Consequencia direta do teorema da nao-clonagem: "
            "um qubit desconhecido nao pode ser copiado. "
            "GuruDev respeita este limite constitucionalmente — "
            "a operacao simplesmente nao existe no protocolo."
        ),
        "determinar_fase": (
            "Fase global de um estado quantico e fisicamente "
            "inacessivel — apenas diferencas de fase sao observaveis "
            "(interferencia). Determinar fase global e equivalente "
            "a determinar rho1 absoluto sem referencia."
        ),
    }
    return justificativas.get(operacao, "Operacao ausente por contencao constitucional.")


def _limite_constitucional(operacao: str) -> str:
    """Retorna o limite constitucional violado por uma operação ausente."""
    limites = {
        "clonar_estado": "rho3_equivalencia — limite de equivalencia",
        "medir_sem_colapso": "rho6_compensacao — cadeia de implicacao",
        "copiar_qubit": "rho3_equivalencia — teorema da nao-clonagem",
        "determinar_fase": "rho1_similitude — referencia absoluta",
    }
    return limites.get(operacao, "contencao constitucional geral")
