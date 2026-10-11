# Política de segurança do Assistente

O runtime atual da GuruDev **aceita** subescritas em outras linguagens (`¿python? ... ?/python?` e equivalentes) e executa as subescritas Python via `exec()` (`src/interpreter.py`). Essa capacidade faz parte da linguagem e **não é alterada**.

A restrição abaixo pertence ao **Assistente GuruDev** da demo pública, não à linguagem:

- **POL-01:** programa que contenha qualquer bloco de subescrita (`[subescritas]`, `$$subescritas$$` ou marcadores `¿<linguagem>? ... ?/<linguagem>?`) **não é executado**. O Assistente pode exibir e explicar o código, mas recusa a execução.
- **POL-02:** a verificação de POL-01 é feita por regra no código da aplicação, antes de qualquer execução, e não por instrução ao modelo.
- **POL-03:** execuções permitidas rodam com limite de tempo e de tamanho de entrada e saída.
