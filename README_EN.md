# gurudev-core
# GuruDev Core - Powered by Hubstry-DeepTech

> Ontological and holistic programming language

**GuruDev** is a holistic and ontological programming language, developed by the deep tech company **Hubstry-DeepTech**.
This repository contains the language core, including its grammar, interpreter, and conceptual architecture.

---

## Vision

GuruDev integrates linguistics, artificial intelligence, epistemology, and software engineering to create a multimodal and semantic paradigm, aligned with the demands of the next generation of computational systems.

---

## Installation

```bash
git clone https://github.com/Hubstry-DeepTech/gurudev-core.git
cd gurudev-core
pip install -e .
```

Requires Python 3.8+ and PLY (Python Lex-Yacc).

---

## Usage

```bash
# Run a .guru file
gurudev run examples/ontologico.guru

# Run control flow examples
gurudev run examples/fluxo.guru

# Run tests
python -m pytest tests/ -v
```

---

## Features (v1.2.0-alpha)

### Language
- **Types**: Int, Float, String, Bool, Void, Array, Object, Formula, Temporal, Imagem, Audio, Video, Tabela, Grafo
- **Grammatical cases**: NOM, VOC, ACU, DAT, GEN, INS, LOC, ABL
- **Bilingual aliases**: `se`/`if`, `senao`/`else`, `enquanto`/`while`, `para`/`for`, `retorna`/`return`

### Control Flow
- **se / senao_se / senao** (if / elif / else) with unlimited elif chaining
- **enquanto** (while) with break/continue
- **para** (C-style for) with initialization, condition, and increment
- **quebra / continua** (break / continue)

### Functions
- Definition with grammatical case: `NOM funcao calcular(Int x, Int y) -> Int { ... }`
- Required and optional parameters with default values (Tesniere's valence)
- Return type with arrow: `-> Int`, `-> String`, etc.
- Return: `return` / `retorna`
- Semantic annotation (Buhler): `#sem: puro`, `#sem: efeito`, `#sem: expressao`
- Built-in functions: `escrever()`, `tipo_de()`, `tamanho()`, `hash_guru()`, `converter_int()`, etc.

### Classes and Objects
- Class definition with inheritance (`extends`) and interfaces (`implements`)
- Methods with `this` / `isto`
- Instantiation and method calls

### Ontological Triple Block
- Overscript with level, root, key, ontology
- Native GuruDev code (`¡codigo!` ... `!/codigo!`)
- Multilingual subscripts: Python, Rust, JavaScript, Java, C#, C++, SQL, R, WASM
- Error compensation: error handling and performance blocks

### General Theory of Function (Linguistic Foundation)
- **Tesniere (Valence)**: Required parameters (actants) and optional with default (circumstants)
- **Buhler (Organon)**: Semantic function classification via `#sem:` (pure/effect/expression)
- **Wilmet (Instituted relation)**: Grammatical case on definition = nature of the relation

---

## Quick Examples

### Control Flow
```gurudev
Int grade = 75;
if (grade >= 90) {
    escrever("A");
} senao_se (grade >= 70) {
    escrever("B");
} senao {
    escrever("F");
}
```

### Optional Parameters (Tesniere)
```gurudev
// name = actant (required), greeting = circumstant (optional)
funcao greet(String name, String greeting = "Hello") {
    escrever(greeting + ", " + name + "!");
}
greet("World");        // Hello, World!
greet("World", "Oi");  // Oi, World!
```

### Semantic Classification (Buhler)
```gurudev
#sem: puro
funcao fibonacci(Int n) -> Int {
    if (n <= 1) { return n; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

#sem: efeito
funcao save_data(String file, String content) {
    // side-effect action
}
```

---

## Repository Structure

```
gurudev-core/
  src/
    lexer/gurudev_lexer.py   - PLY lexer with 9+ states
    parser.py                - PLY parser with full grammar
    ast_nodes.py             - AST nodes (dataclasses)
    interpreter.py           - Tree-walker interpreter + ontological engine
    semantic_analyzer.py     - Alexandria integration (subscript analysis)
    symbol_table.py          - Symbol table with scopes
    cli.py                   - CLI (gurudev run)
  alexandria/
    __init__.py              - v0.3.0, 6 exported classes
    cli.py                   - Alexandria CLI (compare, translate, etc.)
    core/
      analyzer.py            - LanguageAnalyzer (25 languages)
      translator.py          - CodeTranslator
      type_mapper.py         - TypeMapper
      bridge.py              - LanguageBridge / BridgeManager
      quantum_comparator.py  - QuantumComparator + ConsistencyChecker
    data/
      programming_languages.json  - 25 classical languages
      quantum_languages.json      - 8 quantum languages (rho_1-rho_6)
      quantum_algorithms.json     - 4 algorithms (Shor, Grover, VQE, QAOA)
      classical_quantum_pairs.json - 10 classical-quantum pairs
  examples/                  - GuruDev example scripts
  tests/                     - 130 automated tests (pytest)
  grammar/                   - EBNF grammar definitions
  docs/                      - Whitepapers and documentation
  pyproject.toml             - Package configuration
  LICENSE                    - BSL 1.1
```

---

---

## Quantum — Quantum Computing Vertical

GuruDev Core integrates a quantum computing research vertical, based on Machado (2026b) — [DOI: 10.5281/zenodo.18776462](https://doi.org/10.5281/zenodo.18776462):

- **Demonstrated isomorphisms:** identical tensor product between significance vectors and quantum states; canonical bijection between 64 binary profiles and 6-qubit computational basis
- **Formalized analogies:** entanglement as instance of compensation (ρ₆), no-cloning theorem as equivalence limit (ρ₃), decoherence as hermeneutic convergence
- **Proposed extension:** quantum significance profiles with superposition and collapse upon evaluation
- **8 open problems** with testability criteria

> No variant of quantum mysticism is tolerated. All connections are mathematical, with declared limits.

Full documentation: [`docs/VERTICAL_QUANTICA.md`](docs/VERTICAL_QUANTICA.md) | [`docs/VERTICAL_QUANTICA_EN.md`](docs/VERTICAL_QUANTICA_EN.md)

<!-- ALEXANDRIA_SECTION_START -->

## Alexandria — Interoperability and Comparative Programming Library

**Alexandria** (v0.3.0) is GuruDev Core's integrated comparative programming, semantic analysis, and multilingual interoperability library. It provides weighted comparisons between languages, type mapping, code translation, and, as of Phase 1, **hexarelational quantum profiles** based on the ρ₁-ρ₆ algebra from Machado (2026b).

### Modules

| Module | Class | Function |
|---|---|---|
| `core.analyzer` | `LanguageAnalyzer` | Weighted comparative analysis (25 classical languages) |
| `core.translator` | `CodeTranslator` | Cross-language code translation |
| `core.type_mapper` | `TypeMapper` | Cross-language type mapping |
| `core.bridge` | `LanguageBridge` | Async interoperability bridges |
| `core.quantum_comparator` | `QuantumComparator` | Comparison via ρ₁-ρ₆ hexarelational profiles |
| `core.quantum_comparator` | `ConsistencyChecker` | Chain validation ρ₆⇒ρ₅⇒...⇒ρ₁ |

### Alexandria Quantum (Phase 1)

Based on DOI [10.5281/zenodo.18776462](https://doi.org/10.5281/zenodo.18776462), Alexandria Quantum adds:

- **`quantum_languages.json`** — 8 quantum languages (Qiskit, Q#, Cirq, PennyLane, Silq, OpenQASM 3, Quipper, CUDA Quantum) with `perfil_hexarrelacional_conjectural` (ρ₁-ρ₆) and `anomalia_cadeia_implicacao`
- **`quantum_algorithms.json`** — 4 algorithms (Shor, Grover, VQE, QAOA) with profiles and `classificacao_tats`
- **`classical_quantum_pairs.json`** — 10 classical-quantum pairs with dominant ρ (including GuruDev↔Silq as direct correspondence via constitutional containment)
- **`QuantumComparator`** — language/algorithm comparison via Euclidean distance, golden ratio norm (φ^k), and π√ transform
- **`ConsistencyChecker`** — validates the implication chain ρ₆⇒ρ₅⇒...⇒ρ₁ with 0.05 tolerance, detecting anomalies like ρ₄>ρ₃ (Shor, Grover, Cirq, OpenQASM 3)

### Usage

```python
from alexandria import QuantumComparator, ConsistencyChecker

comp = QuantumComparator()

# Compare quantum languages
result = comp.compare_languages("Qiskit", "Cirq")
print(result.similarity_score)

# Check implication chain consistency
check = comp.check_consistency("Shor")  # False (anomaly: rho4 > rho3)
print(check['consistente'])

# Classical-quantum pair GuruDev-Silq
pair = comp.get_pair("GuruDev", "Silq")
print(pair['rho_dominante'])  # rho6
```

<!-- ALEXANDRIA_SECTION_END -->

---

## Official Links

- Official Website: [gurudev-tech.site](https://gurudev-tech.site)
- Repository: [github.com/Hubstry-DeepTech/gurudev-core](https://github.com/Hubstry-DeepTech/gurudev-core)
- GuruDev Interactive Lexer: [dyh6i3cqzgoz.manus.space](https://dyh6i3cqzgoz.manus.space/)

---

## License

This project is licensed under the **Business Source License 1.1 (BSL 1.1)**.

---

**Reprogram the world with semantics, intelligence, and resilience.**
(c) Hubstry-DeepTech - All rights reserved.
