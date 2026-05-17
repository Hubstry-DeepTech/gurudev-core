# === DIAGNOSTIC ===
print("=== Lexer: PARADIGMA_ATTR function ===")
path = "src/lexer/gurudev_lexer.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "t_sobrescrita_PARADIGMA_ATTR" in line:
        for j in range(i, min(i + 10, len(lines))):
            print("%4d [%s]" % (j+1, repr(lines[j])))
        break

print()
print("=== Demo file: lines 1-35 ===")
with open("examples/quantum_demo.guru", "r", encoding="utf-8") as f:
    dlines = f.readlines()
for i, line in enumerate(dlines[:35]):
    print("%4d: %s" % (i+1, line), end="")

print()
print("=== Parser: PARADIGMA rules (lines 275-340) ===")
path2 = "src/parser.py"
with open(path2, "r", encoding="utf-8") as f:
    plines = f.readlines()
for i in range(274, min(340, len(plines))):
    print("%4d: %s" % (i+1, plines[i]), end="")
