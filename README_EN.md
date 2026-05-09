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
    interpreter.py           - Tree-walker interpreter
    symbol_table.py          - Symbol table with scopes
    cli.py                   - CLI (gurudev run)
  examples/                  - GuruDev example scripts
  tests/                     - Automated tests (pytest)
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
