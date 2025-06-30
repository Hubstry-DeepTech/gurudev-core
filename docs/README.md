# GuruDev® EBNF — Gramática Formal da Linguagem

Esta é a gramática EBNF oficial da linguagem de programação GuruDev®, alinhada ao lexer implementado em Python (PLY). Ela define de forma precisa e formal a estrutura sintática da linguagem, servindo como referência para o desenvolvimento do parser, documentação, testes e futuras expansões.

## 📚 Visão Geral

- **Versão:** 1.0.0-alpha  
- **Autor:** Guilherme Gonçalves Machado  
- **Descrição:** Esta gramática cobre todos os requisitos do whitepaper GuruDev®, incluindo blocos tríplices, casos gramaticais, tipos nativos, interoperabilidade multilíngue, anotações semânticas e controle de fluxo.

## 🌱 Estrutura Principal

### Bloco GuruDev®

Cada bloco é composto por:

- `[sobrescrita]` — Metadados/contexto semântico  
- `¡codigo!` — Código GuruDev® principal  
- `[subescritas]` — Blocos de código estrangeiro (interoperabilidade)

**Exemplo:**

```gurudev
[bloco]
    [sobrescrita]
        "Contexto: autenticação"
        [nivel="holistico"]
        [raiz="SEG"]
        [ont="acao"]
    [/sobrescrita]

    ¡codigo!
        NOM funcao verificarSenha(String senhaInserida, String senhaHashArmazenada) {
            return hash(senhaInserida) == hash(senhaHashArmazenada);
        }
    !/codigo!

    [subescritas]
        ¿python?
        def verificar_senha(senha_inserida, senha_armazenada):
            return hash(senha_inserida) == hash(senha_armazenada)
        ?/python?
    [/subescritas]
[/bloco]
```

## 🏷️ Terminais (Tokens Reconhecidos pelo Lexer)

<details>
<summary><strong>Clique para expandir</strong></summary>

```ebnf
BLOCO_START = "[bloco]" ;
BLOCO_END = "[/bloco]" ;
SOBRESCRITA_START = "[sobrescrita]" ;
SOBRESCRITA_END = "[/sobrescrita]" ;
SUBESCRITAS_START = "[subescritas]" ;
SUBESCRITAS_END = "[/subescritas]" ;
CODIGO_START = "¡codigo!" ;
CODIGO_END = "!/codigo!" ;
...
```
</details>

## 🛠️ Como Usar

- O lexer reconhece todos os tokens definidos nesta EBNF.
- Use como base para um parser em PLY, ANTLR ou equivalente.

## 🚀 Contribuindo

- Sugestões e melhorias são bem-vindas.
- Abra uma **Issue** ou **Pull Request** neste repositório.

## 📄 Licença

_Defina a licença desejada para o projeto: MIT, Apache 2.0, etc._

**GuruDev® — Código que transcende paradigmas. Sintaxe que honra a tradição.**