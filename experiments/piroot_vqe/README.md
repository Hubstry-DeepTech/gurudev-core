# PiRoot VQE Experiment

> Análise Hexarrelacional do Variational Quantum Eigensolver via Protocolo GuruDev

**Versão:** 0.1.0 | **Autor:** Guilherme Gonçalves Machado (Hubstry-DeepTech)
**Referência:** Machado (2026b). π√f(A) e Computação Quântica. DOI: 10.5281/zenodo.18776462

---

## Resumo

Este experimento demonstra **GuruDev como protocolo semântico da interface clássico-quântica** através da análise do Variational Quantum Eigensolver (VQE) usando a álgebra hexarrelacional ρ₁-ρ₆.

O VQE é o algoritmo mais natural na taxonomia hexarrelacional:
- **ρ₆ = 0.9** (compensação máxima — emergência do sistema C+Q)
- **ρ₅ = 0.7** (equilíbrio clássico-quântico sustentável)
- **Cadeia consistente** — ρ₆ ⇒ ρ₅ ⇒ ... ⇒ ρ₁ preservada
- **Classificação TATS:** consistente-paradigmático

A hipótese PiRoot-VQE afirma que a transformação π√E normaliza a energia do VQE e correlaciona com a norma áurea do perfil hexarrelacional, permitindo monitoramento semântico da convergência.

## Hipóteses

### H1: Monitoramento Semântico via ρ₅
> ρ₅ (equilíbrio clássico-quântico) é um indicador de convergência VQE. ρ₅ cresce durante convergência saudável e degrada durante barren plateaus.

### H2: Detecção de Barren Plateaus
> Barren plateaus são semanticamente detectáveis via degradação da cadeia hexarrelacional. Quando ρ₅ < 0.8 · log₂(2ⁿ), o circuito está em regime de barren plateau.

### H3: Correlação PiRoot
> A transformação π√E da energia correlaciona com a norma áurea do perfil hexarrelacional, sustentando a hipótese PiRoot.

## Estrutura

```
experiments/piroot_vqe/
├── __init__.py              # Inicialização do pacote
├── piroot_vqe.py            # Experimento principal PiRoot-VQE
├── barren_plateau_test.py   # Teste de detecção de barren plateaus
├── results/                 # Resultados de execuções
│   └── .gitkeep
└── README.md                # Este arquivo
```

## Módulos

### `piroot_vqe.py` — Experimento Principal

Classes e funções:
- `pi_root(x)` — Transformação π√ (raiz pi-ésima preservando sinal)
- `norma_aurea(perfil)` — Norma áurea com pesos φᵏ
- `PiRootVQEExperiment` — Classe principal do experimento
  - `run_scenario(n_qubits, depth, iterations, ...)` — Executa cenário VQE simulado
  - `analyze_landscape(n_qubits, depths, ...)` — Análise de paisagem em múltiplas profundidades
  - `compare_algorithms()` — Compara VQE, QAOA, Shor, Grover via perfil hexarrelacional
  - `piroot_correlation_analysis()` — Análise de correlação PiRoot

### `barren_plateau_test.py` — Teste de Barren Plateaus

Classes e funções:
- `BarrenPlateauTest` — Teste de detecção de planícies estéreis
  - `run(depths, iterations_per_depth, ...)` — Executa teste em múltiplas profundidades
  - `run_qubit_scaling(depths, qubit_range, ...)` — Escala qubits e profundidades
- `DepthProfile` — Perfil hexarrelacional por profundidade
- `BarrenPlateauResults` — Resultados completos do teste

## Execução

```python
# Experimento PiRoot-VQE básico
from experiments.piroot_vqe.piroot_vqe import PiRootVQEExperiment

exp = PiRootVQEExperiment(seed=42)
trajectory = exp.run_scenario(n_qubits=4, depth=3, iterations=50)
print(f"Converged: {trajectory.converged}")
print(f"Rho5 delta: {trajectory.rho5_delta}")
print(trajectory.summary())

# Análise de paisagem (múltiplas profundidades)
landscape = exp.analyze_landscape(n_qubits=4, depths=[1, 2, 3, 5, 8, 12])
print(f"Transition depth: {landscape['transition_depth']}")

# Comparação entre algoritmos
comparison = exp.compare_algorithms()
for name, data in comparison['algorithms'].items():
    print(f"{name}: {data['delegacao']} ({data['classificacao_tats']})")

# Análise de correlação PiRoot
corr = exp.piroot_correlation_analysis(n_scenarios=20)
print(f"PiRoot-Norma correlation: {corr['correlation_piroot_norma_aurea']}")
```

```python
# Teste de barren plateau
from experiments.piroot_vqe.barren_plateau_test import BarrenPlateauTest

test = BarrenPlateauTest(n_qubits=6, seed=42)
results = test.run(depths=[1, 2, 3, 5, 8, 12, 16])
print(f"Barren plateau onset: depth {results.onset_depth}")
print(f"Confidence: {results.onset_confidence:.2%}")
print(results.summary())

# Escala qubits x profundidades
scaling = test.run_qubit_scaling()
print(scaling['interpretation'])
```

## Conceitos-chave

### Álgebra Hexarrelacional ρ₁-ρ₆

| Componente | Nome | Papel no VQE |
|---|---|---|
| ρ₁ | Similitude | Correspondência entre estado preparado e Hamiltoniano |
| ρ₂ | Homologia | Estrutura do ansatz preserva simetrias do problema |
| ρ₃ | Equivalência | Reprodutibilidade estatística das medições |
| ρ₄ | Simetria | Invariância unitária do circuito |
| ρ₅ | Equilíbrio | Qualidade da interface clássico-quântico (indicador principal) |
| ρ₆ | Compensação | Emergência do sistema composto C+Q |

### Cadeia de Implicação

ρ₆ ⇒ ρ₅ ⇒ ρ₄ ⇒ ρ₃ ⇒ ρ₂ ⇒ ρ₁

VQE é o único algoritmo com cadeia consistente (sem anomalias detectáveis).

### Critérios de Delegação

| Tipo | Critério | Significado no VQE |
|---|---|---|
| EMERGENCIA | ρ₆ > 0.70 | Resultado emerge do sistema C+Q |
| ANOMALIA | ρ₄ > ρ₃ | Simetria sem equivalência (VQE NÃO tem) |
| EQUILÍBRIO | ρ₅ > 0.60 | Gradientes fluem em ambas direções |
| CONSERVAÇÃO | ρ₅ >= 0.50 | Recurso preservado |

## Limitações

1. **Simulação probabilística** — GuruDev não executa computação quântica real. Os resultados são simulações baseadas na classificação de delegação.
2. **Perfis conjecturais** — Os valores ρ₁-ρ₆ são inferidos da teoria (Machado 2026b), não medidos experimentalmente.
3. **Modelo simplificado de barren plateau** — A degradação segue modelo exponencial simplificado; circuitos reais podem ter comportamento mais complexo.

## Referências

1. Machado, G. G. (2026b). π√f(A) e Computação Quântica. Zenodo. DOI: 10.5281/zenodo.18776462
2. McClean, J. R. et al. (2018). Barren plateaus in quantum neural network training landscapes. Nature Commun., 9(1), 4812.
3. Peruzzo, A. et al. (2014). A variational eigenvalue solver on a photonic quantum processor. Nature Commun., 5, 4213.
4. Kandala, A. et al. (2017). Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets. Nature, 549, 242-246.

## Licença

MIT — Guilherme Gonçalves Machado (Hubstry-DeepTech)
