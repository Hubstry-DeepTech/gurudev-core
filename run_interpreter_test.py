#!/usr/bin/env python3
"""
GuruDev® Test Runner — Versão 1.0.0-alpha
Testa o pipeline completo: Lexer → Parser → AST → Interpreter
Autor: Guilherme Gonçalves Machado

Execute: python run_interpreter_test.py [--debug]
"""

import sys
import os

# Garante que o src/ está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parser import parse
from src.interpreter import GuruDevInterpreter

# ============================================================
# TESTES UNITÁRIOS
# ============================================================

tests_passed = 0
tests_failed = 0
tests_total = 0


def test(nome, code, expected_output_lines=None, expect_error=False):
    """Executa um teste do interpreter."""
    global tests_passed, tests_failed, tests_total
    tests_total += 1

    print(f"\n--- Teste: {nome} ---")

    try:
        # Capturar stdout
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        ast = parse(code, debug=False)
        if ast is None:
            raise RuntimeError("AST vazia — falha no parsing.")

        interp = GuruDevInterpreter(debug=False)
        resultado = interp.interpretar(ast)

        saida = sys.stdout.getvalue()
        sys.stdout = old_stdout

        if expect_error:
            print(f"  [FALHOU] Esperava erro, mas executou com sucesso.")
            print(f"  Saida: {saida.strip()}")
            tests_failed += 1
            return

        # Verificar saída
        if expected_output_lines is not None:
            linhas_saida = [l.strip() for l in saida.strip().split('\n') if l.strip()]
            for esperada in expected_output_lines:
                if esperada not in saida:
                    print(f"  [FALHOU] Esperava conter: '{esperada}'")
                    print(f"  Saida obtida: {saida.strip()}")
                    tests_failed += 1
                    sys.stdout = old_stdout
                    return

        print(f"  [OK] Resultado: {resultado!r}")
        if saida.strip():
            for linha in saida.strip().split('\n'):
                print(f"       {linha}")
        tests_passed += 1

    except Exception as e:
        sys.stdout = old_stdout
        if expect_error:
            print(f"  [OK] Erro esperado: {e}")
            tests_passed += 1
        else:
            print(f"  [FALHOU] {type(e).__name__}: {e}")
            tests_failed += 1


# ============================================================
# SUITE DE TESTES
# ============================================================

def run_all_tests():
    print("=" * 60)
    print("GuruDev Interpreter — Suite de Testes v1.0")
    print("=" * 60)

    # --- T1: Literais e Variáveis ---
    test("T1 - Literais",
         'Int x = 42;',
         expected_output_lines=[])

    test("T1b - String",
         'String nome = "GuruDev"; escrever(nome);',
         expected_output_lines=["GuruDev"])

    test("T1c - Booleanos",
         'Bool v = verdadeiro; Bool f = falso; escrever(v); escrever(f);',
         expected_output_lines=["verdadeiro", "falso"])

    # --- T2: Operações Aritméticas ---
    test("T2 - Aritmetica",
         'Int r = 10 + 20; escrever(r); escrever(10 - 3); escrever(4 * 5); escrever(10 / 3);',
         expected_output_lines=["30", "7", "20"])

    # --- T3: Funções ---
    test("T3 - Funcao simples",
         '''NOM funcao soma(Int a, Int b) -> Int { return a + b; }
            escrever(soma(3, 4));''',
         expected_output_lines=["7"])

    test("T3b - Recursao fatorial",
         '''NOM funcao fat(Int n) -> Int {
                if (n <= 1) { return 1; }
                return n * fat(n - 1);
            }
            escrever(fat(5));''',
         expected_output_lines=["120"])

    # --- T4: If/Else ---
    test("T4 - If verdadeiro",
         'if (verdadeiro) { escrever("sim"); }',
         expected_output_lines=["sim"])

    test("T4b - If falso com else",
         'if (falso) { escrever("nao"); } else { escrever("sim"); }',
         expected_output_lines=["sim"])

    # --- T5: For ---
    test("T5 - For estilo C",
         '''Int s = 0;
            for (Int i = 1; i <= 3; i = i + 1) { s = s + i; }
            escrever(s);''',
         expected_output_lines=["6"])

    # --- T6: While ---
    test("T6 - While",
         '''Int n = 0;
            while (n < 5) { n = n + 1; }
            escrever(n);''',
         expected_output_lines=["5"])

    # --- T7: For-each ---
    test("T7 - Para cada",
         '''Array nums = [10, 20, 30];
            for (Int x : nums) { escrever(x); }''',
         expected_output_lines=["10", "20", "30"])

    # --- T8: Break/Continue ---
    test("T8 - Break",
         '''Int i = 0;
            while (verdadeiro) {
                i = i + 1;
                if (i >= 3) { break; }
            }
            escrever(i);''',
         expected_output_lines=["3"])

    test("T8b - Continue",
         '''Int i = 0;
            while (i < 5) {
                i = i + 1;
                if (i == 3) { continue; }
                escrever(i);
            }''',
         expected_output_lines=["1", "2", "4", "5"])

    # --- T9: Builtins ---
    test("T9 - Escrever",
         'escrever("Ola", "Mundo");',
         expected_output_lines=["Ola Mundo"])

    test("T9b - Tipo de",
         'escrever(tipo_de(42)); escrever(tipo_de("abc")); escrever(tipo_de(verdadeiro));',
         expected_output_lines=["Int", "String", "Bool"])

    test("T9c - Hash",
         'escrever(hash("test"));',
         expected_output_lines=[])

    test("T9d - Matematica",
         'escrever(absoluto(-5)); escrever(raiz(25)); escrever(arredondar(3.7));',
         expected_output_lines=["5", "5.0", "4.0"])

    # --- T10: Operadores de Comparação ---
    test("T10 - Comparacao",
         '''escrever(10 == 10); escrever(10 != 5); escrever(3 < 5); escrever(5 > 3);''',
         expected_output_lines=["verdadeiro", "verdadeiro", "verdadeiro", "verdadeiro"])

    # --- T11: Operadores Lógicos ---
    test("T11 - Logicos",
         '''escrever(verdadeiro && falso); escrever(verdadeiro || falso); escrever(!falso);''',
         expected_output_lines=["falso", "verdadeiro", "verdadeiro"])

    # --- T12: Bloco Tríplice Completo ---
    test("T12 - Bloco completo",
         '''[$$bloco$$]
            [$$sobrescrita$$]
                "Teste de bloco"
                [$$nivel="holistico"$$]
                [$$raiz="TEST"$$]
                [$$clave="ciencia"$$]
                [$$ont="acao"$$]
            [$$/sobrescrita$$]
            ¡codigo!
                String msg = "bloco executado";
                escrever(msg);
            !/codigo!
            [$$subescritas$$]
                ¿python?
                print("subescrita python")
                ?/python?
            [$$/subescritas$$]
        [$$/bloco$$]''',
         expected_output_lines=["bloco executado"])

    # --- T13: Serie ---
    test("T13 - Serie",
         '''serie { escrever("a"); escrever("b"); escrever("c"); }''',
         expected_output_lines=["a", "b", "c"])

    # --- T14: Classe ---
    test("T14 - Classe",
         '''NOM classe Ponto {
                Float x;
                Float y;
            }
            escrever("classe Ponto definida");''',
         expected_output_lines=["classe Ponto definida"])

    # --- T15: Conversão de tipos ---
    test("T15 - Coercao",
         '''Int a = converter_int("42"); Float b = converter_float(3); String c = converter_string(100); Bool d = converter_bool(1);
            escrever(a); escrever(b); escrever(c); escrever(d);''',
         expected_output_lines=["42", "3.0", "100", "verdadeiro"])

    # --- T16: Concatenação de strings ---
    test("T16 - Concatenacao",
         '''String a = "Guru"; String b = "Dev"; escrever(a + b);''',
         expected_output_lines=["GuruDev"])

    # --- T17: Funcao sem retorno ---
    test("T17 - Void",
         '''NOM funcao imprimir_algo() { escrever("oi"); }
            imprimir_algo();''',
         expected_output_lines=["oi"])

    # --- T18: Array + tamanho ---
    test("T18 - Array tamanho",
         '''Array arr = [1, 2, 3, 4, 5]; escrever(tamanho(arr));''',
         expected_output_lines=["5"])

    # --- T19: Nested if ---
    test("T19 - If aninhado",
         '''Int x = 10;
            if (x > 5) {
                if (x > 15) {
                    escrever("grande");
                } else {
                    escrever("medio");
                }
            } else {
                escrever("pequeno");
            }''',
         expected_output_lines=["medio"])

    # --- T20: Erro - variável não definida ---
    test("T20 - Erro var inexistente",
         'escrever(inexistente);',
         expect_error=True)

    # --- RESUMO ---
    print("\n" + "=" * 60)
    print(f"RESULTADO: {tests_passed}/{tests_total} testes passaram")
    if tests_failed > 0:
        print(f"  {tests_failed} teste(s) falharam")
    print("=" * 60)

    return tests_failed == 0


if __name__ == '__main__':
    debug = '--debug' in sys.argv
    sucesso = run_all_tests()
    sys.exit(0 if sucesso else 1)
