"""GuruDev Interpreter v1.0.0-alpha"""
import copy
from .ast_nodes import *


class GuruDevError(Exception):
    pass


class ReturnSignal(Exception):
    def __init__(self, value=None):
        self.value = value


class Ambiente:
    """Ambiente de execucao com suporte a escopos e congelamento (ACU)."""

    def __init__(self, pai=None):
        self.vars = {}
        self.funcs = {}
        self.frozen = set()
        self.pai = pai

    def get(self, nome):
        if nome in self.vars:
            return self.vars[nome]
        if self.pai:
            return self.pai.get(nome)
        raise GuruDevError(f"variavel '{nome}' nao definida")

    def set(self, nome, valor, freeze=False):
        if nome in self.frozen:
            raise GuruDevError(f"variavel '{nome}' imutavel (ACU)")
        self.vars[nome] = valor
        if freeze:
            self.frozen.add(nome)

    def decl(self, nome, valor, freeze=False):
        self.vars[nome] = valor
        if freeze:
            self.frozen.add(nome)


class Interpreter:
    """Interpretador tree-walking GuruDev com semantica de casos gramaticais."""

    def __init__(self):
        self.env = Ambiente()
        self.call_log = []
        self.recipients = {}

    def interpretar(self, ast):
        if ast is None:
            raise GuruDevError("AST vazia")
        self._x(ast)
        return self

    def _x(self, node):
        if node is None:
            return None
        nome = type(node).__name__
        handler = getattr(self, "_x_" + nome, None)
        if handler:
            return handler(node)
        return None

    def _e(self, node):
        return self._x(node)

    # --- Programa e Bloco ---

    def _x_Programa(self, n):
        for elem in n.elementos:
            self._x(elem)

    def _x_Bloco(self, n):
        for stmt in n.codigo:
            self._x(stmt)

    # --- Declaracoes ---

    def _x_DeclaracaoVariavel(self, n):
        val = self._e(n.valor) if n.valor else None
        caso = n.caso_gramatical
        freeze = (caso == "ACU")
        if caso == "ABL" and val is not None:
            val = copy.deepcopy(val)
        self.env.decl(n.nome, val, freeze=freeze)
        if caso == "DAT":
            self.recipients[n.nome] = val

    def _x_DefinicaoFuncao(self, n):
        self.env.funcs[n.nome] = n
        if n.caso_gramatical == "VOC":
            self.call_log.append(n.nome)

    def _x_Atribuicao(self, n):
        val = self._e(n.valor)
        caso = n.caso_gramatical
        if caso == "ABL" and val is not None:
            val = copy.deepcopy(val)
        if caso == "ACU":
            self.env.set(n.alvo, val, freeze=True)
        elif caso == "DAT":
            self.env.set(n.alvo, val)
            self.recipients[n.alvo] = val
        else:
            self.env.set(n.alvo, val)

    # --- Chamadas ---

    def _x_ChamadaFuncao(self, n):
        caso = n.caso_gramatical
        if caso == "VOC":
            self.call_log.append(n.nome)
        fn = self.env.funcs.get(n.nome)
        if fn is None:
            raise GuruDevError(f"funcao '{n.nome}' indefinida")
        args = [self._e(a) for a in n.argumentos]
        if caso == "INS":
            call_env = Ambiente()
        else:
            call_env = Ambiente(pai=self.env)
        for p, a in zip(fn.parametros, args):
            call_env.decl(p.nome, a)
        old = self.env
        self.env = call_env
        try:
            for stmt in fn.corpo:
                self._x(stmt)
        except ReturnSignal as r:
            self.env = old
            if caso == "ABL":
                return copy.deepcopy(r.value)
            return r.value
        finally:
            self.env = old
        return None

    # --- Controle de fluxo ---

    def _x_Retorno(self, n):
        raise ReturnSignal(self._e(n.valor) if n.valor else None)

    def _x_Se(self, n):
        if self._e(n.condicao):
            for s in n.corpo_verdadeiro:
                self._x(s)
        elif n.corpo_falso:
            for s in n.corpo_falso:
                self._x(s)

    def _x_Enquanto(self, n):
        while self._e(n.condicao):
            for s in n.corpo:
                self._x(s)

    def _x_Para(self, n):
        self._x(n.inicializacao)
        while self._e(n.condicao):
            for s in n.corpo:
                self._x(s)
            self._x(n.incremento)

    # --- Expressoes ---

    def _x_Literal(self, n):
        return n.valor

    def _x_Identificador(self, n):
        return self.env.get(n.nome)

    def _x_OperacaoBinaria(self, n):
        left = self._e(n.esquerda)
        right = self._e(n.direita)
        op = n.operador
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        if op == "%":
            return left % right
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right
        if op == "&&":
            return left and right
        if op == "||":
            return left or right
        raise GuruDevError(f"operador desconhecido: {op}")

    def _x_OperacaoUnaria(self, n):
        val = self._e(n.operando)
        if n.operador == "-":
            return -val
        if n.operador == "!":
            return not val
        raise GuruDevError(f"operador unario desconhecido: {n.operador}")

    def _x_ChamadaMetodo(self, n):
        raise GuruDevError("ChamadaMetodo nao suportada ainda")

    def _x_AcessoPropriedade(self, n):
        raise GuruDevError("AcessoPropriedade nao suportado ainda")
