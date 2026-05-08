# -*- coding: utf-8 -*-
"""Testes de controle de fluxo: se/senao_se/senao, enquanto, para."""
import pytest
from src.parser import parse


def _parse_ok(code):
    """Parse sem erro, retorna AST."""
    ast = parse(code, debug=False)
    assert ast is not None, f"Parse returned None for: {code}"
    return ast


class TestSeSimples:
    """Testes basicos de se/senao."""

    def test_if_true(self):
        ast = _parse_ok('Int x = 10; se (x > 5) { Int y = 1; }')
        assert ast is not None

    def test_if_false(self):
        ast = _parse_ok('Int x = 3; se (x > 5) { Int y = 1; }')
        assert ast is not None

    def test_if_else(self):
        ast = _parse_ok('Int x = 3; se (x > 5) { Int y = 1; } senao { Int z = 2; }')
        assert ast is not None

    def test_if_comparacao(self):
        ast = _parse_ok('Int a = 10; se (a == 10) { Int ok = 1; }')
        assert ast is not None


class TestSeElif:
    """Testes de se/senao_se/senao (elif chain)."""

    def test_elif_primeiro(self):
        ast = _parse_ok(
            'Int x = 95; '
            'se (x > 90) { Int r = 1; } '
            'senao_se (x > 70) { Int r = 2; } '
            'senao { Int r = 3; }'
        )
        assert ast is not None

    def test_elif_segundo(self):
        ast = _parse_ok(
            'Int x = 75; '
            'se (x > 90) { Int r = 1; } '
            'senao_se (x > 70) { Int r = 2; } '
            'senao { Int r = 3; }'
        )
        assert ast is not None

    def test_elif_senao(self):
        ast = _parse_ok(
            'Int x = 30; '
            'se (x > 90) { Int r = 1; } '
            'senao_se (x > 70) { Int r = 2; } '
            'senao { Int r = 3; }'
        )
        assert ast is not None

    def test_elif_multi(self):
        ast = _parse_ok(
            'Int n = 55; '
            'se (n >= 90) { Int g = 1; } '
            'senao_se (n >= 70) { Int g = 2; } '
            'senao_se (n >= 50) { Int g = 3; } '
            'senao_se (n >= 30) { Int g = 4; } '
            'senao { Int g = 5; }'
        )
        assert ast is not None

    def test_if_somente(self):
        ast = _parse_ok('se (true) { Int a = 1; }')
        assert ast is not None


class TestEnquanto:
    """Testes de enquanto (while)."""

    def test_enquanto_simples(self):
        ast = _parse_ok(
            'Int i = 0; '
            'enquanto (i < 3) { i = i + 1; }'
        )
        assert ast is not None

    def test_enquanto_false(self):
        ast = _parse_ok(
            'Int i = 10; '
            'enquanto (i < 3) { i = i + 1; }'
        )
        assert ast is not None


class TestPara:
    """Testes de para (for estilo C)."""

    def test_para_simples(self):
        ast = _parse_ok(
            'para (Int i = 0; i < 3; i = i + 1) { Int x = i; }'
        )
        assert ast is not None

    def test_para_decremento(self):
        ast = _parse_ok(
            'para (Int i = 5; i > 0; i = i - 1) { Int x = i; }'
        )
        assert ast is not None


class TestAninhado:
    """Testes de estruturas aninhadas."""

    def test_if_dentro_while(self):
        ast = _parse_ok(
            'Int i = 0; '
            'enquanto (i < 3) { '
            '  se (i == 1) { Int a = 1; } '
            '  senao { Int b = 2; } '
            '  i = i + 1; '
            '}'
        )
        assert ast is not None

    def test_while_dentro_if(self):
        ast = _parse_ok(
            'Int x = 5; '
            'se (x > 0) { '
            '  Int j = 0; '
            '  enquanto (j < 2) { j = j + 1; } '
            '}'
        )
        assert ast is not None


class TestBreakContinue:
    """Testes de break/continue."""

    def test_break_no_while(self):
        ast = _parse_ok(
            'enquanto (true) { quebra; }'
        )
        assert ast is not None

    def test_continue_no_while(self):
        ast = _parse_ok(
            'Int i = 0; '
            'enquanto (i < 5) { '
            '  i = i + 1; '
            '  continua; '
            '}'
        )
        assert ast is not None
