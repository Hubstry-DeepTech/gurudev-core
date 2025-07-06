# **GuruCompiler Specification — Compilador GuruDev® → GuruByte**

**GuruCompiler Specification — Compilador GuruDev® → GuruByte**

---

## 🔍 Visão Geral

O **GuruCompiler** é o compilador oficial da linguagem GuruDev®. Ele transforma código-fonte semântico e multimodal escrito em GuruDev® para bytecode GuruByte (.gurub), pronto para execução na GVM.

O compilador é estruturado em módulos que garantem a preservação de marcadores semânticos, ontológicos e hermenêuticos, possibilitando compilação simbólica de dados e estruturas não-verbais.

---

## 📅 Pipeline de Compilação

```
[Fonte .guru] ➔ Lexer ➔ Parser ➔ Context Analyzer ➔ Ontology Mapper
         ➔ Instruction Generator ➔ Bytecode Generator ➔ [.gurub]

```

---

## 🔋 Etapas

### 1. **Lexer (Analisador Léxico)**

- Define o alfabeto simbólico da linguagem
- Tokeniza:
    - Palavras reservadas
    - Delimitadores ((), {}, :, etc.)
    - Claves, Tags, Operadores multimodais

### 2. **Parser (Analisador Sintático)**

- Constrói a GuruAST (Abstract Syntax Tree)
- Identifica blocos lógicos, relações de escopo, declarações, multimodalidade

### 3. **Context Analyzer**

- Extrai e valida:
    - Clave (campo do conhecimento)
    - Hermenêutica (1 a 7)
    - Categoria Ontológica
    - Relacionamentos semânticos (rho_i)

### 4. **Ontology Mapper**

- Mapeia cada objeto, atributo ou expressão para uma das 10 categorias de Aristóteles
- Marca semanticamente o tipo de dado ou função envolvida

### 5. **Instruction Generator**

- Traduz AST em instruções de baixo nível (GuruInstructionSet)
- Encadeia execução de blocos
- Define paralelismo, compensações, interop

### 6. **Bytecode Generator**

- Gera o arquivo `.gurub` com:
    - HEADER com metadados
    - CONTEXT com marcações
    - CODEBLOCKS com instruções lineares ou paralelas
    - CHECKSUM + ASSINATURA DIGITAL (opcional)

---

## 🛋️ Suporte a Extensões

- **Modo Educacional:** exporta arquivos com visualização pedagógica (JSON, HTML)
- **Modo IA:** gera AST simbólica para agentes cognitivos
- **Modo Interop:** permite transpiladores para Python, Lua, etc.

---

## 📊 Exemplo de Conversão

**Fonte (.guru)**

```
def energia = "E = mc^2"
tag hermeneutica=7
clave ciencia
mostre energia

```

**Bytecode (.gurub)**

```
HEADER: GURU 0.1.0
CONTEXT: clave=ciencia, hermeneutica=7, ontologia=relacao
CONSTANTS: F001=formula("E=mc^2")
BLOCK 0001:
  LOAD F001
  DISPLAY
  TAG Hermeneutics=7
  MAP_TO CLAVE ciencia

```

---

## 🌐 Roadmap do GuruCompiler

- v0.1: Lexer + Parser + Instruction Generator (offline)
- v0.2: Ontology Mapper + Bytecode export
- v0.3: API REST + transpiler para Python

---

**Fim da Especificação do GuruCompiler v0.1**
