**GuruInstructionSet v0.1.1 — Conjunto de Instruções do GuruByte (compatível com GuruMatrix 5D)**

---

## 🔍 Visão Geral 

O **GuruInstructionSet** define as instruções executáveis no bytecode `.gurub` interpretado pela GuruDVM (GuruDev® Virtual Machine). As instruções foram criadas para suportar operações multimodais, multissemióticas e semânticas, respeitando os contextos de clave, hermenêutica e ontologia — agora expandidos para uma estrutura de **coordenadas 5D** (GuruMatrix[i][j][k][t][l]).

Cada instrução é composta por uma **operação** principal e **parâmetros** opcionais, podendo ser agrupada em blocos com execução em série, paralela ou compensada.

---

## 📊 Categorias de Instrução

### 1. Instruções de Entrada e Saída

| Opcode     | Descrição                    | Exemplo                      |
|------------|------------------------------|------------------------------|
| `LOAD`     | Carrega um recurso multimodal | `LOAD A001`                  |
| `DISPLAY`  | Exibe um recurso              | `DISPLAY IN CONTEXT`         |
| `ECHO`     | Reproduz áudio ou texto       | `ECHO "Bem-vindo"`           |
| `SAVE`     | Salva o estado atual          | `SAVE CONTEXT current_state` |

### 2. Instruções de Processamento Semântico

| Opcode     | Descrição                                | Exemplo                              |
|------------|--------------------------------------------|--------------------------------------|
| `MAP_TO`   | Mapeia estrutura para uma clave            | `MAP_TO CLAVE filosofia`             |
| `BIND`     | Associa semântica ao recurso ou instrução  | `BIND CLAVE arte`                    |
| `TAG`      | Atribui tag hermenêutica ou ontológica     | `TAG Hermeneutics=3`                 |
| `TRANSLATE`| Traduz recurso entre linguagens            | `TRANSLATE TO en_US`                 |

### 3. Instruções Lógicas e Matemáticas

| Opcode     | Descrição                    | Exemplo                        |
|------------|------------------------------|--------------------------------|
| `EVALUATE` | Avalia expressão ou fórmula  | `EVALUATE F001`                |
| `APPLY`    | Aplica operação               | `APPLY FFT`                    |
| `IF`       | Executa condição              | `IF TAG=3 THEN BLOCK 002`      |
| `COMPARE`  | Compara dois objetos          | `COMPARE A001 WITH A002`       |

### 4. Instruções de Controle de Fluxo

| Opcode       | Descrição                      | Exemplo                          |
|--------------|--------------------------------|----------------------------------|
| `JUMP`       | Salta para outro bloco         | `JUMP TO BLOCK 004`              |
| `CALL`       | Invoca bloco ou função         | `CALL BLOCK 010`                 |
| `RETURN`     | Retorna de função              | `RETURN`                         |
| `PARALLELIZE`| Define execução paralela       | `PARALLELIZE BLOCKS 003,004`     |

### 5. Instruções de Interoperabilidade

| Opcode       | Descrição                               | Exemplo                        |
|--------------|-------------------------------------------|--------------------------------|
| `EXPORT`     | Exporta para linguagem externa            | `EXPORT AS Python`             |
| `IMPORT`     | Importa módulo externo                   | `IMPORT FROM Lua`              |
| `TRANSCODE`  | Converte entre formatos simbólicos       | `TRANSCODE AUDIO TO WAVEFORM`  |
| `INTEROP_MAP`| Mapeia simbolicamente para outra linguagem| `INTEROP_MAP WITH Java`        |

### 6. Instruções Experimentais (v0.1 alpha)

| Opcode   | Descrição                              | Exemplo                        |
|----------|------------------------------------------|--------------------------------|
| `EMOTE`  | Codifica emoção em execução multimodal   | `EMOTE joy ON BLOCK 006`       |
| `TRACE`  | Traça rota semântica até o output        | `TRACE FROM BLOCK 001`         |
| `CLONE`  | Duplica bloco de execução                | `CLONE BLOCK 005 AS BLOCK 009` |

---

## 🧠 Exemplo com GuruMatrix 5D

```gurub
LOAD A001
TAG ONTOLOGY=Substância CLAVE=ciência HERMENEUTICS=3 TIME=execution MODE=imperativo
MAP_TO CLAVE ciência
DISPLAY IN CONTEXT
```

---

## 🧪 Instruções Futuras Planejadas (v0.2+)

| Opcode         | Descrição                                                   |
|----------------|-------------------------------------------------------------|
| `MATRIX_LOOKUP`| Consulta célula i,j,k,t,l da GuruMatrix                     |
| `MATRIX_ROUTE` | Determina caminho de execução entre posições 5D             |
| `ANNOTATE`     | Associa metadados educacionais (dodecálogo) ao código       |
| `MENTOR_HINT`  | Sugestão semântica para ambientes educacionais              |

---

## 🛠️ Roadmap

- Versão 0.2: instruções para IA simbólica e agentes cognitivos
- Versão 0.3: suporte a “bibliotecas educacionais” baseadas no dodecálogo
- Versão 0.4: instruções orientadas por GuruMatrix dinâmica

---

**Fim da Especificação v0.1.1**
