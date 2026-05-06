#!/usr/bin/env python3
"""
GuruDev Test Runner v1.1.0-alpha
Hubstry-DeepTech
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.parser import parse
from src.interpreter import GuruDevInterpreter

tests_passed = 0
tests_failed = 0
tests_total = 0

def test(nome, code, expected_output_lines=None, expect_error=False):
    global tests_passed, tests_failed, tests_total
    tests_total += 1
    print(f"\n--- Teste: {nome} ---")
    try:
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        ast = parse(code, debug=False)
        if ast is None:
            raise RuntimeError("AST vazia.")
        interp = GuruDevInterpreter(debug=False)
        resultado = interp.interpretar(ast)
        saida = sys.stdout.getvalue()
        sys.stdout = old_stdout
        if expect_error:
            print("  [FALHOU] Esperava erro.")
            tests_failed += 1
            return
        if expected_output_lines is not None:
            for esperada in expected_output_lines:
                if esperada not in saida:
                    print(f"  [FALHOU] Esperava: '{esperada}'")
                    print(f"  Saida: {saida.strip()[:200]}")
                    tests_failed += 1
                    return
        print("  [OK]")
        tests_passed += 1
    except Exception as e:
        sys.stdout = old_stdout
        if expect_error:
            print(f"  [OK] Erro esperado: {e}")
            tests_passed += 1
        else:
            print(f"  [FALHOU] {type(e).__name__}: {e}")
            tests_failed += 1

def run_all_tests():
    print("=" * 60)
    print("GuruDev - Suite de Testes v1.1")
    print("=" * 60)

    test("T1", "Int x = 42;", [])
    test("T1b", "String nome = \"GuruDev\"; escrever(nome);", ["GuruDev"])
    test("T1c", "Bool v = verdadeiro; Bool f = falso; escrever(v); escrever(f);", ["verdadeiro", "falso"])
    test("T2", "Int r = 10 + 20; escrever(r); escrever(10 - 3); escrever(4 * 5); escrever(10 / 3);", ["30", "7", "20"])
    test("T3", "NOM funcao soma(Int a, Int b) -> Int { return a + b; } escrever(soma(3, 4));", ["7"])
    test("T3b", "NOM funcao fat(Int n) -> Int { if (n <= 1) { return 1; } return n * fat(n - 1); } escrever(fat(5));", ["120"])
    test("T4", "if (verdadeiro) { escrever(\"sim\"); }", ["sim"])
    test("T4b", "if (falso) { escrever(\"nao\"); } else { escrever(\"sim\"); }", ["sim"])
    test("T5", "Int s = 0; for (Int i = 1; i <= 3; i = i + 1) { s = s + i; } escrever(s);", ["6"])
    test("T6", "Int n = 0; while (n < 5) { n = n + 1; } escrever(n);", ["5"])
    test("T7", "Array nums = [10, 20, 30]; for (Int x : nums) { escrever(x); }", ["10", "20", "30"])
    test("T8", "Int i = 0; while (verdadeiro) { i = i + 1; if (i >= 3) { break; } } escrever(i);", ["3"])
    test("T8b", "Int i = 0; while (i < 5) { i = i + 1; if (i == 3) { continue; } escrever(i); }", ["1", "2", "4", "5"])
    test("T9", "escrever(\"Ola\", \"Mundo\");", ["Ola Mundo"])
    test("T9b", "escrever(tipo_de(42)); escrever(tipo_de(\"abc\")); escrever(tipo_de(verdadeiro));", ["Int", "String", "Bool"])
    test("T9c", "escrever(hash(\"test\"));", [])
    test("T9d", "escrever(absoluto(-5)); escrever(raiz(25)); escrever(arredondar(3.7));", ["5", "5", "4"])
    test("T10", "escrever(10 == 10); escrever(10 != 5); escrever(3 < 5); escrever(5 > 3);", ["verdadeiro", "verdadeiro", "verdadeiro", "verdadeiro"])
    test("T11", "escrever(verdadeiro && falso); escrever(verdadeiro || falso); escrever(!falso);", ["falso", "verdadeiro", "verdadeiro"])
    test("T12", "[$$bloco$$]\n[$$sobrescrita$$]\n\"Contexto: teste\"\n[$$nivel=\"holistico\"$$]\n[$$raiz=\"TEST\"$$]\n[$$clave=\"ciencia\"$$]\n[$$ont=\"acao\"$$]\n[$$/sobrescrita$$]\n¡codigo!\nString msg = \"bloco executado\";\nescrever(msg);\n!/codigo!\n[$$subescritas$$]\n¿python?\nprint(\"sub\")\n?/python?\n[$$/subescritas$$]\n[$$/bloco$$]", ["bloco executado"])
    test("T13", "serie { escrever(\"a\"); escrever(\"b\"); escrever(\"c\"); }", ["a", "b", "c"])
    test("T14", "NOM classe Ponto { Float x; Float y; } escrever(\"classe Ponto definida\");", ["classe Ponto definida"])
    test("T15", "Int a = converter_int(\"42\"); Float b = converter_float(3); String c = converter_string(100); Bool d = converter_bool(1); escrever(a); escrever(b); escrever(c); escrever(d);", ["42", "3", "100", "verdadeiro"])
    test("T16", "String a = \"Guru\"; String b = \"Dev\"; escrever(a + b);", ["GuruDev"])
    test("T17", "NOM funcao imprimir_algo() { escrever(\"oi\"); } imprimir_algo();", ["oi"])
    test("T18", "Array arr = [1, 2, 3, 4, 5]; escrever(tamanho(arr));", ["5"])
    test("T19", "Int x = 10; if (x > 5) { if (x > 15) { escrever(\"grande\"); } else { escrever(\"medio\"); } } else { escrever(\"pequeno\"); }", ["medio"])
    test("T20", "escrever(inexistente);", expect_error=True)
    test("T21 - String methods", "String s = \"Ola Mundo\"; escrever(s.tamanho()); escrever(s.maiusculo()); escrever(s.minusculo()); escrever(s.contem(\"Mundo\")); escrever(\"  espaco  \".trim()); String partes = s.dividir(\" \"); escrever(partes.tamanho()); escrever(s.substring(0, 3)); escrever(s.substituir(\"Mundo\", \"GuruDev\")); escrever(s.repetir(2)); escrever(s.indice(\"Mundo\")); escrever(s.vazio()); escrever(\"\".vazio()); escrever(\"ola\".maiusculo_primeiro()); escrever(\"OLA\".minusculo_primeiro()); escrever(s.inverter()); escrever(s.comeca_com(\"Ola\")); escrever(s.termina_com(\"do\"));", ["9", "OLA MUNDO", "ola mundo", "verdadeiro", "espaco", "Ola", "Ola", "Ola GuruDev", "Ola MundoOla Mundo", "4", "falso", "verdadeiro", "Ola", "oLA", "odnuM alO", "verdadeiro", "verdadeiro"])
    test("T22 - Array methods", "Array a = [3, 1, 2]; escrever(a.tamanho()); a.adicionar(4); escrever(a.contem(3)); a.ordenar(); escrever(a.juntar(\"-\")); escrever(a.primeiro()); escrever(a.ultimo()); Int removido = a.remover_ultimo(); escrever(removido); escrever(a.tamanho()); Array b = []; escrever(b.vazio()); a.inverter(); escrever(a.primeiro());", ["3", "verdadeiro", "1-2-3-4", "1", "4", "4", "3", "verdadeiro", "3"])
    test("T23 - Classe basica", "NOM classe Ponto { Float x; Float y; NOM funcao iniciar(Float px, Float py) { this.x = px; this.y = py; } NOM funcao distancia() -> Float { return raiz(this.x * this.x + this.y * this.y); } } Ponto p = Ponto(3.0, 4.0); escrever(p.distancia());", ["5"])
    test("T24 - Classe this", "NOM classe Contador { Int valor; NOM funcao iniciar() { this.valor = 0; } NOM funcao incrementar() { this.valor = this.valor + 1; } NOM funcao obter() -> Int { return this.valor; } } Contador c = Contador(); c.incrementar(); c.incrementar(); c.incrementar(); escrever(c.obter());", ["3"])
    test("T25 - Classe isto", "NOM classe Caixa { String nome; NOM funcao iniciar(String n) { isto.nome = n; } NOM funcao saudacao() -> String { return \"Ola da \" + isto.nome; } } Caixa cx = Caixa(\"GuruDev\"); escrever(cx.saudacao());", ["Ola da GuruDev"])
    test("T26 - Classe sem iniciar", "NOM classe Calc { NOM funcao soma(Int a, Int b) -> Int { return a + b; } NOM funcao mult(Int a, Int b) -> Int { return a * b; } } Calc c = Calc(); escrever(c.soma(10, 20)); escrever(c.mult(3, 7));", ["30", "21"])
    test("T27 - Array sort", "Array nums = [5, 3, 8, 1, 9, 2]; nums.ordenar(); escrever(nums.juntar(\" \"));", ["1 2 3 5 8 9"])
    test("T28 - Array inverter", "Array a = [1, 2, 3, 4, 5]; escrever(a.ultimo()); a.inverter(); escrever(a.primeiro());", ["5", "5"])
    test("T29 - String replace", "String s = \"GuruDev\"; String nome = \"mundo\"; escrever(s.inverter()); escrever(nome.substituir(\"mundo\", \"GuruDev\"));", ["veDuruG", "GuruDev"])
    test("T30 - Classe prop", "NOM classe Pessoa { String nome; NOM funcao iniciar(String n) { this.nome = n; } } Pessoa p = Pessoa(\"GuruDev\"); escrever(p.nome);", ["GuruDev"])

    print("\n" + "=" * 60)
    print(f"RESULTADO: {tests_passed}/{tests_total} testes passaram")
    if tests_failed > 0:
        print(f"  {tests_failed} teste(s) falharam")
    print("=" * 60)
    return tests_failed == 0

if __name__ == "__main__":
    sucesso = run_all_tests()
    sys.exit(0 if sucesso else 1)
