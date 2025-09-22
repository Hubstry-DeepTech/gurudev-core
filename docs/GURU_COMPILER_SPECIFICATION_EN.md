**GuruCompiler Specification v0.2 — GuruDev® Compiler with GuruMatrix[5D] Support**

> 🌐 **Language / Idioma**: [Português](GURU_COMPILER_SPECIFICATION.md) | **English** | [Bilingual Index](../../BILINGUAL_INDEX.md)

---

## 🔍 Overview

The **GuruCompiler** is the official compiler for the **GuruDev®** language. It transforms symbolic, multimodal, and multisemiotic source code into **bytecode `.gurub`**, interpreted by the **GVM (Guru Virtual Machine)**.

Version **v0.2** introduces integral mapping to **GuruMatrix[5D]**, enabling precise representation of semantic, hermeneutic, ontological, temporal, and paradigmatic dimensions.

---

## 📊 Compilation Pipeline

```plaintext
[Source .guru] ➔ Lexer ➔ Parser ➔ Context Analyzer (GuruMatrix Mapper)
         ➔ Ontology Mapper ➔ Instruction Generator ➔ Bytecode Generator ➔ [.gurub]
```

---

## 🔋 Detailed Stages

### 1. **Lexer (Lexical Analyzer)**

* Tokenizes words, structures, types, keys, multimodal tags
* Support for symbolic, musical, visual, and literal operators

### 2. **Parser (Syntactic Analyzer)**

* Builds the **GuruAST** (Abstract Syntax Tree)
* Enforces intermodal coherence and scopes
* Identifies grammatical structures and execution blocks

### 3. **Context Analyzer — GuruMatrix Mapper [5D]**

* Extracts and validates **GuruMatrix[5D]** dimensions:

  * `Clave` (semantic field: art, science, philosophy, spiritual, general)
  * `Hermeneutics` (1 to 7)
  * `Ontology` (10 Aristotelian categories)
  * `TimeScope` (compilation | execution | visualization)
  * `Mode` (imperative, symbolic, functional, structural...)
  * `rho_i`: semantic relations like symmetry, equivalence, etc.

### 4. **Ontology Mapper**

* Maps instructions, types, and operators to Aristotelian categories
* Enables ontological traceability in bytecode

### 5. **Instruction Generator**

* Converts GuruAST into **GuruInstructionSet v0.1** instructions
* Defines sequential, parallel, or compensatory execution
* Allows rich annotations for educational visualization

### 6. **Bytecode Generator**

* Generates `.gurub` file with sections:

  * `HEADER` (signature, version)
  * `CONTEXT` (GuruMatrix per block)
  * `CONSTANTS` (multimodal resources)
  * `CODEBLOCKS` (execution + 5D tags)
  * `FOOTER` (checksum + symbolic signature)

---

## 🌍 Mode Support

| Mode             | Additional output generated                  |
| ---------------- | ------------------------------------------- |
| Educational      | JSON or HTML with GuruMatrix visualization   |
| Cognitive Agent  | Enriched GuruAST                            |
| Interoperable    | Transpilers to Python, Lua, JS, etc.       |

---

## 📊 Conversion Example

### Source (.guru)

```gurudev
[bloco]
  [sobrescrita]
    "Contexto: Teorema da Energia"
    [nivel="ontologico"]
    [clave="ciencia"]
    [ont="relacao"]
  [/sobrescrita]

  ¡codigo!
    NOM funcao energia() {
      String f = "E = mc^2";
      VOC.print(f);
    }
  !/codigo!
[/bloco]
```

### Bytecode (.gurub)

```plaintext
HEADER: GURU v0.1.1
CONTEXT: CLAVE=ciencia, HERMENEUTICS=7, ONTOLOGY=relacao, TIME=execution, MODE=imperativo
CONSTANTS: F001=formula("E = mc^2")
BLOCK 0001:
  LOAD F001
  DISPLAY
  TAG ONTOLOGY=relacao CLAVE=ciencia HERMENEUTICS=7 TIME=execution MODE=imperativo
```

---

## 🚀 Roadmap v0.3+

* ✅ Educational visualizer for GuruMatrix 5D (interactive mode)
* ✅ GVM MVP with .gurub block execution
* ✅ Transpiler to classic languages (Python, Lua, Rust)
* ✅ Integration with symbolic AI assistants

---

**End of GuruCompiler v0.2 Specification**

---

> 🌐 **Navigation / Navegação**: [Português](GURU_COMPILER_SPECIFICATION.md) | **English** | [Bilingual Index](../../BILINGUAL_INDEX.md)