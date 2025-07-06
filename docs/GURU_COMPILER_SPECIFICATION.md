**GuruCompiler Specification v0.2 — Compilador GuruDev® com Suporte à GuruMatrix\[5D]**

---

## 🔍 Visão Geral

O **GuruCompiler** é o compilador oficial da linguagem **GuruDev®**. Ele transforma o código-fonte simbólico, multimodal e multissemótico em **bytecode `.gurub`**, interpretado pela **GVM (Guru Virtual Machine)**.

A versão **v0.2** introduz o mapeamento integral à **GuruMatrix\[5D]**, permitindo representação precisa de dimensões semânticas, hermenêuticas, ontológicas, temporais e paradigmáticas.

---

## 📊 Pipeline de Compilação

```plaintext
[Fonte .guru] ➔ Lexer ➔ Parser ➔ Context Analyzer (GuruMatrix Mapper)
         ➔ Ontology Mapper ➔ Instruction Generator ➔ Bytecode Generator ➔ [.gurub]
```

---

## 🔋 Etapas Detalhadas

### 1. **Lexer (Analisador Léxico)**

* Tokeniza palavras, estruturas, tipos, claves, tags multimodais
* Suporte a operadores simbólicos, musicais, visuais e literais

### 2. **Parser (Analisador Sintático)**

* Constrói a **GuruAST** (Abstract Syntax Tree)
* Reforça coerência intermodal e escopos
* Identifica estruturas gramaticais e blocos de execução

### 3. **Context Analyzer — GuruMatrix Mapper \[5D]**

* Extrai e valida dimensões da **GuruMatrix\[5D]**:

  * `Clave` (campo semântico: arte, ciência, filosofia, espiritual, geral)
  * `Hermenêutica` (1 a 7)
  * `Ontologia` (10 categorias aristotélicas)
  * `TimeScope` (compilation | execution | visualization)
  * `Mode` (imperativo, simbólico, funcional, estrutural...)
  * `rho_i`: relações semânticas como simetria, equivalência etc.

### 4. **Ontology Mapper**

* Mapeia instruções, tipos e operadores para categorias aristotélicas
* Habilita rastreabilidade ontológica no bytecode

### 5. **Instruction Generator**

* Converte GuruAST em instruções do **GuruInstructionSet v0.1**
* Define execução sequencial, paralela ou compensatória
* Permite anotações ricas para visualização educacional

### 6. **Bytecode Generator**

* Gera arquivo `.gurub` com seções:

  * `HEADER` (assinatura, versão)
  * `CONTEXT` (GuruMatrix por bloco)
  * `CONSTANTS` (recursos multimodais)
  * `CODEBLOCKS` (execução + tags 5D)
  * `FOOTER` (checksum + assinatura simbólica)

---

## 🌍 Suporte a Modos

| Modo             | Saída adicional gerada                      |
| ---------------- | ------------------------------------------- |
| Educacional      | JSON ou HTML com visualização da GuruMatrix |
| Agente Cognitivo | GuruAST enriquecida                         |
| Interoperável    | Transpiladores para Python, Lua, JS etc.    |

---

## 📊 Exemplo de Conversão

### Fonte (.guru)

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

* ✅ Visualizador educacional da GuruMatrix 5D (modo interativo)
* ✅ MVP da GVM com execução de blocos .gurub
* ✅ Transpilador para linguagens clássicas (Python, Lua, Rust)
* ✅ Integração com assistentes de IA simbólica

---

**Fim da Especificação GuruCompiler v0.2**
