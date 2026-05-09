# PiRoot VQE Experiment

> Analise Hexarrelacional do Variational Quantum Eigensolver via Protocolo GuruDev

**Versao:** 0.1.0 | **Autor:** Guilherme Goncalves Machado (Hubstry-DeepTech)
**Referencia:** Machado (2026b). pi*sqrt(f(A)) e Computacao Quantica. DOI: 10.5281/zenodo.18776462

---

## Resumo

Este experimento demonstra **GuruDev como protocolo semantico da interface classico-quântica** através da análise do Variational Quantum Eigensolver (VQE) usando a álgebra hexarrelacional rho_1-rho_6.

O VQE é o algoritmo mais natural na taxonomia hexarrelacional:
- **rho_6 = 0.9** (compensação máxima — emergência do sistema C+Q)
- **rho_5 = 0.7** (equilíbrio clássico-quântico sustentável)
- **Cadeia consistente** — rho_6 => rho_5 => ... => rho_1 preservada
- **Classificação TATS:** consistente-paradigmático

A hipótese PiRoot-VQE afirma que a transformação pi*sqrt(E) normaliza a energia do VQE e correlaciona com a norma áurea do perfil hexarrelacional, permitindo monitoramento semântico da convergência.

## Hipóteses

### H1: Monitoramento Semântico via rho_5
> rho_5 (equilíbrio clássico-quântico) é um indicador de convergência VQE. rho_5 cresce durante convergência saudável e degrada durante barren plateaus.

### H2: Detecção de Barren Plateaus
> Barren plateaus são semanticamente detectáveis via degradação da cadeia hexarrelacional. Quando rho_5 < 0.45 e entropia > 0.8 * log2(2^n), o circuito está em regime de barren plateau.

### H3: Correlação PiRoot
> A transformação pi*sqrt(E) da energia correlaciona com a norma áurea do perfil hexarrelacional, sustentando a hipótese PiRoot.

## Estrutura

```
experiments/piroot_vqe/
├── __init__.py              # Inicializacao do pacote
├── piroot_vqe.py            # Experimento principal PiRoot-VQE
├── barren_plateau_test.py   # Teste de deteccao de barren plateaus
├── results/                 # Resultados de execucoes
│   └── .gitkeep
└── README.md                # Este arquivo
```

## Modulos

### `piroot_vqe.py` — Experimento Principal

Classes e funções:
- `pi_root(x)` — Transformação pi*sqrt (raiz pi-ésima preservando sinal)
- `norma_aurea(perfil)` — Norma áurea com pesos phi^k
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

## Execucao

```python
# Experimento PiRoot-VQE basico
from experiments.piroot_vqe.piroot_vqe import PiRootVQEExperiment

exp = PiRootVQEExperiment(seed=42)
trajectory = exp.run_scenario(n_qubits=4, depth=3, iterations=50)
print(f"Converged: {trajectory.converged}")
print(f"Rho5 delta: {trajectory.rho5_delta}")
print(trajectory.summary())

# Analise de paisagem (multiplas profundidades)
landscape = exp.analyze_landscape(n_qubits=4, depths=[1, 2, 3, 5, 8, 12])
print(f"Transition depth: {landscape['transition_depth']}")

# Comparacao entre algoritmos
comparison = exp.compare_algorithms()
for name, data in comparison['algorithms'].items():
    print(f"{name}: {data['delegacao']} ({data['classificacao_tats']})")

# Analise de correlacao PiRoot
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

### Algebra Hexarrelacional rho_1-rho_6

| Componente | Nome | Papel no VQE |
|---|---|---|
| rho_1 | Similitude | Correspondência entre estado preparado e Hamiltoniano |
| rho_2 | Homologia | Estrutura do ansatz preserva simetrias do problema |
| rho_3 | Equivalência | Reprodutibilidade estatística das medições |
| rho_4 | Simetria | Invariância unitária do circuito |
| rho_5 | Equilíbrio | Qualidade da interface clássico-quântica (indicador principal) |
| rho_6 | Compensação | Emergência do sistema composto C+Q |

### Cadeia de Implicacao

rho_6 => rho_5 => rho_4 => rho_3 => rho_2 => rho_1

VQE é o único algoritmo com cadeia consistente (sem anomalias detectáveis).

### Criterios de Delegacao

| Tipo | Criterio | Significado no VQE |
|---|---|---|
| EMERGENCIA | rho_6 > 0.70 | Resultado emerge do sistema C+Q |
| ANOMALIA | rho_4 > rho_3 | Simetria sem equivalência (VQE NÃO tem) |
| EQUILIBRIO | rho_5 > 0.60 | Gradientes fluem em ambas direções |
| CONSERVACAO | rho_5 >= 0.50 | Recurso preservado |

## Limitacoes

1. **Simulação probabilística** — GuruDev não executa computação quântica real. Os resultados são simulações baseadas na classificação de delegação.
2. **Perfis conjecturais** — Os valores rho_1-rho_6 são inferidos da teoria (Machado 2026b), não medidos experimentalmente.
3. **Modelo simplificado de barren plateau** — A degradação segue modelo exponencial simplificado; circuitos reais podem ter comportamento mais complexo.

## Referencias

1. Machado, G. G. (2026b). pi*sqrt(f(A)) e Computação Quântica. Zenodo. DOI: 10.5281/zenodo.18776462
2. McClean, J. R. et al. (2018). Barren plateaus in quantum neural network training landscapes. Nature Commun., 9(1), 4812.
3. Peruzzo, A. et al. (2014). A variational eigenvalue solver on a photonic quantum processor. Nature Commun., 5, 4213.
4. Kandala, A. et al. (2017). Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets. Nature, 549, 242-246.

## Licenca

MIT — Guilherme Goncalves Machado (Hubstry-DeepTech)
