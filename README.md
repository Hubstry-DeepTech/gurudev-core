# gurudev-core
# GuruDev Core - Powered by Hubstry-DeepTech

> Linguagem de programacao ontologica e holistica

**GuruDev** e uma linguagem de programacao holistica e ontologica, desenvolvida pela deep tech **Hubstry-DeepTech**.
Este repositorio contem o nucleo da linguagem, incluindo sua gramatica, interpretador e arquitetura conceitual.

---

## Visao

GuruDev integra linguistica, inteligencia artificial, epistemologia e engenharia de software para criar um paradigma multimodal e semantico, alinhado as demandas da proxima geracao de sistemas computacionais.

---

## Instalacao

```bash
git clone https://github.com/Hubstry-DeepTech/gurudev-core.git
cd gurudev-core
pip install -e .
```

Requer Python 3.8+ e PLY (Python Lex-Yacc).

---

## Como Usar

```bash
# Rodar um arquivo .guru
gurudev run examples/ontologico.guru

# Rodar exemplos de controle de fluxo
gurudev run examples/fluxo.guru

# Rodar testes
python -m pytest tests/ -v
```

---

## Features (v1.2.0-alpha)

### Linguagem
- **Tipos**: Int, Float, String, Bool, Void, Array, Object, Formula, Temporal, Imagem, Audio, Video, Tabela, Grafo
- **Casos gramaticais**: NOM, VOC, ACU, DAT, GEN, INS, LOC, ABL
- **Alias bilingue**: `se`/`if`, `senao`/`else`, `enquanto`/`while`, `para`/`for`, `funcao`/`funcao`, `retorna`/`return`

### Controle de Fluxo
- **se / senao_se / senao** (if / elif / else) com cadeia elif ilimitada
- **enquanto** (while) com break/continue
- **para** (for estilo C) com inicializacao, condicao e incremento
- **quebra / continua** (break / continue)

### Funcoes
- Definicao com caso gramatical: `NOM funcao calcular(Int x, Int y) -> Int { ... }`
- Parametros obrigatorios e opcionais com valor default (valencia a la Tesniere)
- Tipo de retorno com arrow: `-> Int`, `-> String`, etc.
- Retorno: `return` / `retorna`
- Anotacao semantica (Buhler): `#sem: puro`, `#sem: efeito`, `#sem: expressao`
- Funcoes nativas: `escrever()`, `tipo_de()`, `tamanho()`, `hash_guru()`, `converter_int()`, etc.

### Classes e Objetos
- Definicao de classes com heranca (`extends`) e interfaces (`implements`)
- Metodos com `this` / `isto`
- Instanciacao e chamada de metodos

### Bloco Triplice (Estrutura Ontologica)
- Sobrescrita com nivel, raiz, clave, ontologia
- Codigo GuruDev nativo (`¡codigo!` ... `!/codigo!`)
- Subescritas multilingua: Python, Rust, JavaScript, Java, C#, C++, SQL, R, WASM
- Compensacao de erro: blocos de tratamento de erros e desempenho

### Teoria Geral da Funcao (Fundamentacao Linguistica)
- **Tesniere (Valencia)**: Parametros obrigatorios (actantes) e opcionais com default (circunstantes)
- **Buhler (Organon)**: Classificacao semantica de funcoes via `#sem:` (puro/efeito/expressao)
- **Wilmet (Relacao instituida)**: Caso gramatical na definicao = natureza da relacao

---

## Exemplos Rapidos

### Controle de Fluxo
```gurudev
Int nota = 75;
se (nota >= 90) {
    escrever("A");
} senao_se (nota >= 70) {
    escrever("B");
} senao {
    escrever("F");
}
```

### Funcao com Parametros Opcionais (Tesniere)
```gurudev
// nome = actante (obrigatorio), saudacao = circunstante (opcional)
funcao saudar(String nome, String saudacao = "Ola") {
    escrever(saudacao + ", " + nome + "!");
}
saudar("Mundo");       // Ola, Mundo!
saudar("Mundo", "Oi"); // Oi, Mundo!
```

### Classificacao Semantica (Buhler)
```gurudev
#sem: puro
funcao fibonacci(Int n) -> Int {
    se (n <= 1) { return n; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

#sem: efeito
funcao salvar_dados(String arquivo, String conteudo) {
    // acao com efeito colateral
}
```

### Casos Gramaticais (Wilmet)
```gurudev
NOM funcao calcular(Int x, Int y) -> Int { return x + y; }
DAT funcao enviar(String destino, String msg) { escrever(msg + " para " + destino); }
```

---

## Estrutura do Repositorio

```
gurudev-core/
  src/
    lexer/gurudev_lexer.py   - Lexer PLY com 9+ estados
    parser.py                - Parser PLY com grammar completa
    ast_nodes.py             - Nodos da AST (dataclasses)
    interpreter.py           - Interpretador tree-walker
    symbol_table.py          - Tabela de simbolos com escopos
    cli.py                   - CLI (gurudev run)
  examples/
    ontologico.guru          - Exemplo do Motor Ontologico Ativo
    fluxo.guru               - Exemplos de controle de fluxo
    funcoes.guru             - Exemplos de funcoes
    teoria_geral_funcao.guru - Tesniere + Buhler + Wilmet
  tests/
    test_fluxo.py            - 17 testes de controle de fluxo
    test_funcao.py           - Testes de funcoes
  grammar/                   - Definicoes EBNF
  docs/                      - Whitepapers e documentacao
  pyproject.toml             - Configuracao do pacote
  LICENSE                    - BSL 1.1
```

---

## Links Oficiais

- Site Oficial: [gurudev-tech.site](https://gurudev-tech.site)
- Repositorio: [github.com/Hubstry-DeepTech/gurudev-core](https://github.com/Hubstry-DeepTech/gurudev-core)
- GuruDev Interactive Lexer: [dyh6i3cqzgoz.manus.space](https://dyh6i3cqzgoz.manus.space/)

---

## Licenca

Este projeto esta licenciado sob a **Business Source License 1.1 (BSL 1.1)**.

---

**Reprogramar o mundo com semantica, inteligencia e resiliencia.**
(c) Hubstry-DeepTech - Todos os direitos reservados.
