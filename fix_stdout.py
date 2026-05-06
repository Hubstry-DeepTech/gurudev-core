import sys
p = "src/interpreter.py"
with open(p,"r",encoding="utf-8") as f: c = f.read()
c = c.replace("self._output.append(text)", "print(text)")
c = c.replace("self._output.append(", "print(", 1)
with open(p,"w",encoding="utf-8") as f: f.write(c)
print("OK")
