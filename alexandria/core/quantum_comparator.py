"""
Modulo de Comparacao Quantica via Perfis Hexarrelacionais

Implementa comparacao entre linguagens quanticas e entre pares
classico-quanticos usando os perfis rho_1-rho_6 da algebra
hexarrelacional de significancia.

Autor: Guilherme Goncalves Machado (Hubstry-DeepTech)
Versao: 0.3.0 | Licenca: MIT
Referencia: Machado (2026b). pi*sqrt(f(A)) e Computacao Quantica.
"""

import json
import math
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

# Constante aurea
PHI = (1 + math.sqrt(5)) / 2

# Chaves do perfil hexarrelacional
RHO_KEYS = [
    "rho1_similitude",
    "rho2_homologia",
    "rho3_equivalencia",
    "rho4_simetria",
    "rho5_equilibrio",
    "rho6_compensacao",
]


def norma_aurea(perfil: List[float]) -> float:
    """
    Norma aurea de um perfil hexarrelacional.
    Pesos phi^k aplicados a cada componente.

    Args:
        perfil: Lista de 6 valores float em [0,1]

    Returns:
        Norma aurea do perfil
    """
    return math.sqrt(sum(PHI ** k * v ** 2 for k, v in enumerate(perfil)))


def pi_radical(x: float) -> float:
    """
    Transformacao pi*sqrt — raiz pi-esima preservando sinal.

    Args:
        x: Valor de entrada

    Returns:
        x^(1/pi) com sinal preservado
    """
    return math.copysign(abs(x) ** (1.0 / math.pi), x)


def perfil_from_dict(perfil_dict: Dict[str, float]) -> List[float]:
    """
    Extrai vetor rho [rho1, ..., rho6] de um dicionario de perfil.

    Args:
        perfil_dict: Dicionario com chaves rho1_similitude ... rho6_compensacao

    Returns:
        Lista de 6 floats [rho1, rho2, rho3, rho4, rho5, rho6]
    """
    return [perfil_dict.get(k, 0.0) for k in RHO_KEYS]


@dataclass
class QuantumComparison:
    """Resultado de uma comparacao entre duas linguagens quanticas."""

    language_a: str
    language_b: str
    perfil_a: List[float]
    perfil_b: List[float]
    similarity_score: float
    distance_euclidiana: float
    norma_aurea_diff: float
    rho_dominante_diff: str
    anomalias_a: List[str]
    anomalias_b: List[str]
    cadeia_implicacao_a: bool
    cadeia_implicacao_b: bool
    nota: str = ""


@dataclass
class ClassicalQuantumComparison:
    """Resultado de uma comparacao par classico-quantico."""

    classica: str
    quantica: str
    rho_dominante: str
    rho_valor_dominante: float
    perfil_classica: Optional[List[float]] = None
    perfil_quantica: Optional[List[float]] = None
    nota: str = ""
    fonte: str = ""


class ConsistencyChecker:
    """
    Verifica consistencia da cadeia de implicacao rho_6 => rho_5 => ... => rho_1.

    A cadeia de implicacao estabelece que rho_k <= rho_{k-1} para todo k.
    Violacoes sao anomalias detectaveis.
    """

    TOLERANCIA = 0.05

    def check(self, perfil: List[float]) -> Dict[str, Any]:
        """
        Verifica se um perfil rho_1-rho_6 respeita a cadeia de implicacao.

        Args:
            perfil: Lista de 6 floats [rho1, rho2, rho3, rho4, rho5, rho6]

        Returns:
            Dicionario com diagnostico completo
        """
        anomalias = []
        pares_violados = []

        # Verifica rho_{k+1} <= rho_k para k = 5..1 (indice 4..0)
        for i in range(4, -1, -1):
            rho_maior = perfil[i + 1]
            rho_menor = perfil[i]
            if rho_maior > rho_menor + self.TOLERANCIA:
                par = f"rho{i + 2} > rho{i + 1}"
                anomalias.append(f"{par} — anomalia detectavel")
                pares_violados.append({
                    "par": par,
                    "rho_maior": rho_maior,
                    "rho_menor": rho_menor,
                    "delta": rho_maior - rho_menor,
                })

        consistente = len(anomalias) == 0
        n = norma_aurea(perfil)
        pr = pi_radical(n)

        return {
            "perfil": perfil,
            "norma_aurea": round(n, 6),
            "pi_radical": round(pr, 6),
            "consistente": consistente,
            "anomalias": anomalias,
            "pares_violados": pares_violados,
            "total_anomalias": len(anomalias),
        }


class QuantumComparator:
    """
    Comparador de linguagens quanticas via perfis hexarrelacionais.

    Carrega dados de quantum_languages.json e quantum_algorithms.json
    e implementa comparacao baseada em rho_1-rho_6.
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Inicializa o comparador.

        Args:
            data_path: Caminho para o diretorio alexandria/data/
        """
        if data_path is None:
            # Tenta alexandria/data/ (do diretorio do pacote)
            data_path = Path(__file__).resolve().parent.parent / "data"

        self.data_path = Path(data_path)
        self.languages = self._load_json("quantum_languages.json")
        self.algorithms = self._load_json("quantum_algorithms.json")
        self.pairs = self._load_json("classical_quantum_pairs.json")
        self.checker = ConsistencyChecker()

    def _load_json(self, filename: str, index_key: Optional[str] = "nome") -> Any:
        """Carrega arquivo JSON do diretorio de dados."""
        filepath = self.data_path / filename
        if not filepath.exists():
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Indexa por chave se for lista
        if isinstance(data, list):
            if index_key and data and index_key in data[0]:
                return {item[index_key]: item for item in data}
            return data  # retorna como lista (para pares)
        return data

    def compare_languages(self, lang_a: str, lang_b: str) -> QuantumComparison:
        """
        Compara duas linguagens quanticas via perfis rho_1-rho_6.

        Args:
            lang_a: Nome da primeira linguagem
            lang_b: Nome da segunda linguagem

        Returns:
            QuantumComparison com resultado detalhado

        Raises:
            ValueError: se linguagem nao encontrada
        """
        if lang_a not in self.languages:
            raise ValueError(f"Linguagem quantica nao encontrada: {lang_a}")
        if lang_b not in self.languages:
            raise ValueError(f"Linguagem quantica nao encontrada: {lang_b}")

        data_a = self.languages[lang_a]
        data_b = self.languages[lang_b]

        perfil_a = perfil_from_dict(data_a["perfil_hexarrelacional_conjectural"])
        perfil_b = perfil_from_dict(data_b["perfil_hexarrelacional_conjectural"])

        # Distancia euclidiana entre perfis
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(perfil_a, perfil_b)))

        # Similaridade: 1 - dist normalizada (max dist = sqrt(6) ~ 2.45)
        similarity = max(0.0, 1.0 - dist / math.sqrt(6))

        # Diff de norma aurea
        na = norma_aurea(perfil_a)
        nb = norma_aurea(perfil_b)
        na_diff = abs(na - nb)

        # Rho dominante na diferenca
        diffs = [abs(a - b) for a, b in zip(perfil_a, perfil_b)]
        max_diff_idx = diffs.index(max(diffs))
        rho_dominante_diff = RHO_KEYS[max_diff_idx].replace("rho", "rho_").split("_")[0]

        # Anomalias de cada linguagem
        anomalias_a = []
        anomalias_b = []
        anom_a = data_a.get("anomalia_cadeia_implicacao", {})
        anom_b = data_b.get("anomalia_cadeia_implicacao", {})
        if anom_a.get("detectada", False):
            anomalias_a.append(f"{anom_a['par']} — {anom_a.get('hipotese', '')}")
        if anom_b.get("detectada", False):
            anomalias_b.append(f"{anom_b['par']} — {anom_b.get('hipotese', '')}")

        # Consistencia da cadeia de implicacao
        check_a = self.checker.check(perfil_a)
        check_b = self.checker.check(perfil_b)

        return QuantumComparison(
            language_a=lang_a,
            language_b=lang_b,
            perfil_a=perfil_a,
            perfil_b=perfil_b,
            similarity_score=round(similarity, 4),
            distance_euclidiana=round(dist, 4),
            norma_aurea_diff=round(na_diff, 4),
            rho_dominante_diff=rho_dominante_diff,
            anomalias_a=anomalias_a,
            anomalias_b=anomalias_b,
            cadeia_implicacao_a=check_a["consistente"],
            cadeia_implicacao_b=check_b["consistente"],
        )

    def compare_algorithms(self, alg_a: str, alg_b: str) -> Dict[str, Any]:
        """
        Compara dois algoritmos quanticos via perfis hexarrelacionais.

        Args:
            alg_a: Nome do primeiro algoritmo (Shor, Grover, VQE, QAOA)
            alg_b: Nome do segundo algoritmo

        Returns:
            Dicionario com comparacao detalhada
        """
        if alg_a not in self.algorithms:
            raise ValueError(f"Algoritmo nao encontrado: {alg_a}")
        if alg_b not in self.algorithms:
            raise ValueError(f"Algoritmo nao encontrado: {alg_b}")

        data_a = self.algorithms[alg_a]
        data_b = self.algorithms[alg_b]

        perfil_a = perfil_from_dict(data_a["perfil_hexarrelacional_conjectural"])
        perfil_b = perfil_from_dict(data_b["perfil_hexarrelacional_conjectural"])

        check_a = self.checker.check(perfil_a)
        check_b = self.checker.check(perfil_b)

        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(perfil_a, perfil_b)))
        similarity = max(0.0, 1.0 - dist / math.sqrt(6))

        return {
            "algoritmo_a": alg_a,
            "algoritmo_b": alg_b,
            "perfil_a": perfil_a,
            "perfil_b": perfil_b,
            "similaridade": round(similarity, 4),
            "distancia": round(dist, 4),
            "anomalia_a": check_a["anomalias"] if check_a["anomalias"] else [],
            "anomalia_b": check_b["anomalias"] if check_b["anomalias"] else [],
            "classificacao_a": data_a.get("classificacao_tats", ""),
            "classificacao_b": data_b.get("classificacao_tats", ""),
        }

    def get_pair(self, classica: str, quantica: str) -> Optional[Dict[str, Any]]:
        """
        Recupera informacao de um par classico-quantico.

        Args:
            classica: Nome da linguagem classica
            quantica: Nome da linguagem quantica

        Returns:
            Dicionario do par, ou None se nao encontrado
        """
        pairs = self.pairs.values() if isinstance(self.pairs, dict) else self.pairs
        if not isinstance(pairs, list):
            pairs = list(pairs) if pairs else []
        for pair in pairs:
            nome_c = pair.get("classica", "")
            nome_q = pair.get("quantica", "")
            if nome_c == classica and nome_q == quantica:
                return pair
        return None

    def list_quantum_languages(self) -> List[str]:
        """Retorna lista de todas as linguagens quanticas disponiveis."""
        return list(self.languages.keys())

    def list_algorithms(self) -> List[str]:
        """Retorna lista de todos os algoritmos quanticos disponiveis."""
        return list(self.algorithms.keys())

    def list_pairs(self) -> List[Dict[str, str]]:
        """Retorna lista de todos os pares classico-quanticos."""
        if isinstance(self.pairs, dict):
            return list(self.pairs.values())
        if isinstance(self.pairs, list):
            return self.pairs
        return []

    def check_consistency(self, nome: str) -> Dict[str, Any]:
        """
        Verifica consistencia da cadeia de implicacao para linguagem ou algoritmo.

        Args:
            nome: Nome da linguagem ou algoritmo

        Returns:
            Diagnostico de consistencia
        """
        if nome in self.languages:
            perfil_dict = self.languages[nome]["perfil_hexarrelacional_conjectural"]
            return self.checker.check(perfil_from_dict(perfil_dict))
        elif nome in self.algorithms:
            perfil_dict = self.algorithms[nome]["perfil_hexarrelacional_conjectural"]
            return self.checker.check(perfil_from_dict(perfil_dict))
        else:
            raise ValueError(f"Nome nao encontrado: {nome}")
