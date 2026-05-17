import os, re

# === 1. Lexer: state transitions ===
print("=" * 60)
print("LEXER: All state push/pop and START/END tokens")
print("=" * 60)
path = "src/lexer/gurudev_lexer.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.split("\n")

for i, line in enumerate(lines):
    if "push_state" in line or "pop_state" in line or "START" in line or "END" in line:
        if "print" not in line and "#" not in line:
            print("%4d: %s" % (i+1, line))

# === 2. Parser: structure rules ===
print()
print("=" * 60)
print("PARSER: Rules for bloco/sobrescrita/codigo/programa")
print("=" * 60)
path2 = "src/parser.py"
with open(path2, "r", encoding="utf-8") as f:
    plines = f.readlines()
for i, line in enumerate(plines):
    s = line.strip()
    if "p_programa" in s or "p_bloco" in s or "p_sobrescrita" in s or "p_codigo" in s or "p_conteudo" in s:
        for j in range(i, min(i+5, len(plines))):
            print("%4d: %s" % (j+1, plines[j]), end="")
        print("---")

# === 3. Lexer: sobrescrita state functions ===
print()
print("=" * 60)
print("LEXER: All t_sobrescrita_* functions")
print("=" * 60)
for i, line in enumerate(lines):
    if "t_sobrescrita_" in line or ("r'" in line and i > 0 and "t_sobrescrita" in lines[i-1]):
        if "print" not in line:
            print("%4d: %s" % (i+1, line))

# === 4. Lexer: t_ignore for sobrescrita ===
print()
print("=" * 60)
print("LEXER: t_ignore definitions")
print("=" * 60)
for i, line in enumerate(lines):
    if "t_ignore" in line or "t_sobrescrita_ignore" in line:
        print("%4d: %s" % (i+1, line))

# === 5. Demo file ===
print()
print("=" * 60)
print("DEMO FILE: examples/quantum_demo.guru")
print("=" * 60)
with open("examples/quantum_demo.guru", "r", encoding="utf-8") as f:
    print(f.read())
