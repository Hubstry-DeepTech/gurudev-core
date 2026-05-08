# -*- coding: utf-8 -*-
"""Testes de funcoes: definicao, chamada, return, params opcionais, #sem:"""
import pytest
from src.parser import parse


def _parse_ok(code):
    """Parse sem erro, retorna AST."""
    ast = parse(code, debug=False)
    assert ast is not None, f"Parse returned None for: {code}"
    return ast


class TestDefinicaoFuncao:
    """Testes de definicao de funcoes."""

    def test_funcao_simples(self):
        ast = _parse_ok('funcao ola() { escrever("oi"); }')
        assert ast is not None

    def test_funcao_com_parametros(self):
        ast = _parse_ok('funcao somar(Int a, Int b) { return a + b; }')
        assert ast is not None

    def test_funcao_com_retorno_tipado(self):
        ast = _parse_ok('NOM funcao dobrar(Int x) -> Int { return x * 2; }')
        assert ast is not None

    def test_funcao_com_caso_gramatical(self):
        ast = _parse_ok('DAT funcao enviar(String dest, String msg) { escrever(msg); }')
        assert ast is not None

    def test_funcao_multiplos_params(self):
        ast = _parse_ok('funcao calc(Int a, Int b, Int c) -> Int { return a + b + c; }')
        assert ast is not None

    def test_funcao_void(self):
        ast = _parse_ok('funcao imprime_algo() { escrever("teste"); }')
        assert ast is not None


class TestChamadaFuncao:
    """Testes de chamada de funcoes."""

    def test_chamada_simples(self):
        ast = _parse_ok('funcao f() { } f();')
        assert ast is not None

    def test_chamada_com_args(self):
        ast = _parse_ok('funcao soma(Int a, Int b) { } soma(1, 2);')
        assert ast is not None

    def test_chamada_com_expressao(self):
        ast = _parse_ok('funcao f(Int x) { } f(10 + 20);')
        assert ast is not None


class TestParametrosOpcionais:
    """Testes de parametros opcionais com valor default (Tesniere - circunstantes)."""

    def test_param_default_string(self):
        ast = _parse_ok('funcao saudar(String nome, String msg = "Ola") { }')
        assert ast is not None

    def test_param_default_int(self):
        ast = _parse_ok('funcao calc(Int x, Int y = 0) { }')
        assert ast is not None

    def test_param_default_bool(self):
        ast = _parse_ok('funcao flag(Int x, Bool ativo = true) { }')
        assert ast is not None

    def test_multiplos_defaults(self):
        ast = _parse_ok('funcao f(String a, Int b = 0, String c = "x") { }')
        assert ast is not None

    def test_todos_obrigatorios(self):
        ast = _parse_ok('funcao f(Int a, Int b) { }')
        assert ast is not None


class TestAnotacaoSemantica:
    """Testes de anotacao #sem: (Buhler - Organon)."""

    def test_sem_puro(self):
        ast = _parse_ok('#sem: puro\nfuncao f(Int x) -> Int { return x; }')
        assert ast is not None

    def test_sem_efeito(self):
        ast = _parse_ok('#sem: efeito\nfuncao salvar(String s) { }')
        assert ast is not None

    def test_sem_expressao(self):
        ast = _parse_ok('#sem: expressao\nfuncao log() { }')
        assert ast is not None

    def test_sem_com_caso(self):
        ast = _parse_ok('#sem: puro\nNOM funcao calc(Int x) -> Int { return x; }')
        assert ast is not None


class TestFuncaoComControleFluxo:
    """Testes de funcoes com controle de fluxo interno."""

    def test_funcao_com_se(self):
        ast = _parse_ok(
            'funcao abs(Int x) -> Int { '
            'se (x < 0) { return x * -1; } '
            'senao { return x; } '
            '}'
        )
        assert ast is not None

    def test_funcao_com_enquanto(self):
        ast = _parse_ok(
            'funcao contar(Int n) { '
            'Int i = 0; '
            'enquanto (i < n) { escrever(i); i = i + 1; } '
            '}'
        )
        assert ast is not None

    def test_funcao_recursiva(self):
        ast = _parse_ok(
            'funcao fat(Int n) -> Int { '
            'se (n <= 1) { return 1; } '
            'return n * fat(n - 1); '
            '}'
        )
        assert ast is not None


class TestCasoGramaticalWilmet:
    """Testes de Wilmet: caso gramatical na definicao = natureza da relacao."""

    def test_nom_definidora(self):
        ast = _parse_ok('NOM funcao essencia(Int x) -> Int { return x; }')
        assert ast is not None

    def test_dat_direcional(self):
        ast = _parse_ok('DAT funcao enviar(String dest) { }')
        assert ast is not None

    def test_acu_transformadora(self):
        ast = _parse_ok('ACU funcao transformar(String s) -> String { return s; }')
        assert ast is not None
