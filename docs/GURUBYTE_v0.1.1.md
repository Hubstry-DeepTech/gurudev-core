**GuruByte v0.1.1 — Especificação do Formato Bytecode da GuruDev® (GuruMatrix 5D Ready)**

---

## 🔎 Visão Geral

**GuruByte** é o formato oficial de bytecode da linguagem de programação **GuruDev®**. Ele permite a execução simbólica, multimodal e multissemiótica dentro da **GVM (GuruDev Virtual Machine)**.

O formato `.gurub` conserva metadados semânticos, ontológicos e hermenêuticos, permitindo interoperabilidade programática, visualização pedagógica e operações em múltiplos paradigmas.

---

## ⚖️ Princípios Fundamentais

- **Fidelidade simbólica**: preserva sentido mesmo fora da representação textual
- **Camadas hermenêuticas**: múltiplos níveis interpretativos possíveis
- **Rastreabilidade ontológica**: baseado nas 10 categorias de Aristóteles
- **Modularidade**: compatível com execução paralela, série e lógica de compensação
- **Interoperabilidade**: campos de metadados preparados para tradução entre linguagens

---

## 🔢 Estrutura do Arquivo `.gurub`

```plaintext
[HEADER]      // metadados estruturais e semânticos
[CONTEXT]     // GuruMatrix 5D: Clave, Hermenêutica, Ontologia, Tempo, Modo
[CONSTANTS]   // Recursos multimodais e literais
[CODEBLOCKS]  // Instruções executáveis
[FOOTER]      // Checksum, assinatura, comentários
```

---

## 📊 HEADER

```plaintext
Signature: GURU
Version: 0.1.1
Encoding: UTF-8
Compiler: GuruCompiler v0.3 (GuruMatrix 5D Ready)
```

---

## 🔍 CONTEXT (GuruMatrix[5D])

```plaintext
Clave: ciencia                  // [arte, filosofia, espiritual, ciência, geral]
Hermeneutics: 4                // (1-literal ... 7-ontológico)
Ontology: relacao              // categorias de Aristóteles
TimeScope: execution           // [compilation, execution, visualization]
Mode: imperativo               // ou simbólico, funcional, estrutural, etc.
Tags: [multimodal, educacional, interoperavel]
```

---

## 🧰 CONSTANTS

```plaintext
A001: audio("/assets/audio/notaA.wav")
F001: formula("E = mc^2")
I001: image("/assets/img/onda.png")
```

---

## 🔠 CODEBLOCKS

```plaintext
BLOCK 0001:
  INSTR: LOAD A001
  INSTR: APPLY FFT
  INSTR: TAG ONTOLOGY=Substância CLAVE=ciencia HERMENEUTICS=3 TIME=execution MODE=imperativo

BLOCK 0002:
  INSTR: LOAD F001
  INSTR: EVALUATE
  INSTR: MAP_TO CLAVE filosofia
  INSTR: TAG ONTOLOGY=quantidade HERMENEUTICS=4 TIME=execution MODE=funcional

BLOCK 0003:
  INSTR: LOAD I001
  INSTR: DISPLAY IN CONTEXT
  INSTR: TAG ONTOLOGY=qualidade CLAVE=arte HERMENEUTICS=6 TIME=visualization MODE=multimodal
```

---

## 🗃️ FOOTER

```plaintext
Checksum: SHA256-2F91ACED...
Signature: Founder=Guilherme_M Cert=UFF_2025
Compiled With: GuruDev.v(Alpha,00)
MatrixVersion: GuruMatrix[5D]
```

---

## ⚙️ Semântica de Execução (na GuruDVM)

As instruções são interpretadas em função do contexto 5D de cada bloco:
- Clave + Hermenêutica + Ontologia + Tempo + Modo
- Os blocos podem ser:
  - Executados em série (default)
  - Executados em paralelo (`PARALLELIZE`)
  - Compensados (`COMPENSATE`) como fallback simbólico

---

## 🔭 Próximos Passos

- Concluir MVP da **GDVM** com leitura de `.gurub`
- Visualizador pedagógico por célula da **GuruMatrix 5D**
- Transpilador experimental entre linguagens de destino

---

**Fim da Especificação v0.1.1**
