#!/usr/bin/env python3
"""GuruDev Core v0.2.0 - End-to-End Example"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.lexer.gurudev_lexer import tokenize
from src.parser import parse

EXAMPLE = """
$$bloco$$
    $$sobrescrita$$
        $$nivel="literal"$$
        $$raiz="HELLO"$$
        $$clave="geral"$$
        $$ont="acao"$$
    $$/sobrescrita$$
¡codigo!
        String msg = "Namaskar, Mundo!";
    !/codigo!
$$/bloco$$
"""

def main():
    print("GuruDev Core v0.2.0 - End-to-End Example")
    print("=" * 50)
    tokens = tokenize(EXAMPLE)
    print("")
    print("[LEXER] " + str(len(tokens)) + " tokens:")
    for t in tokens[:8]:
        print("  " + t.type + " | " + str(t.value)[:35])
    if len(tokens) > 8:
        print("  ... (+" + str(len(tokens)-8) + " mais)")
    ast = parse(EXAMPLE)
    if ast:
        print("")
        print("[PARSER] AST OK - tipo: " + type(ast).__name__)
    if hasattr(ast, 'elementos'):
        print("  Elementos: " + str(len(ast.elementos)))
    print("")
    print("Concluido!")

if __name__ == "__main__":
    main()
