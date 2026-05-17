path = "src/lexer/gurudev_lexer.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show lines 20 to 70 (token list area)
print("=== Lines 20-70 (token list) ===")
for i in range(19, min(70, len(lines))):
    print("%4d: %s" % (i+1, lines[i]), end="")

print()
print("=== Lines with PARADIGMA ===")
for i, line in enumerate(lines):
    if "PARADIGMA" in line:
        print("%4d: %s" % (i+1, line), end="")
