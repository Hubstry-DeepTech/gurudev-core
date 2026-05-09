"""GuruDev Interpreter v1.1.0-alpha - Tree-walking com casos gramaticais + Alexandria"""
import copy
import builtins
from .ast_nodes import *


class GuruDevError(Exception):
    pass


class ReturnSignal(Exception):
    def __init__(self, value=None):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class Ambiente:
    """Ambiente de execucao com suporte a escopos, congelamento e classes."""

    def __init__(self, pai=None):
        self.vars = {}
        self.funcs = {}
        self.classes = {}
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

    def has(self, nome):
        if nome in self.vars:
            return True
        if self.pai:
            return self.pai.has(nome)
        return False


class Interpreter:
    """Interpretador tree-walking GuruDev com casos gramaticais e Alexandria."""

    def __init__(self):
        self.env = Ambiente()
        self.call_log = []
        self.recipients = {}
        self.subscrita_analyses = []
        self.last_subscrita_result = None
        self.semantic_analyzer = None
        self._init_alexandria()

    def _init_alexandria(self):
        try:
            from .semantic_analyzer import SemanticAnalyzer
            self.semantic_analyzer = SemanticAnalyzer()
        except Exception:
            pass

    def interpretar(self, ast):
        if ast is None:
            raise GuruDevError("AST vazia")
        self._x(ast)
        return self

    def _x(self, node):
        if node is None:
            return None
        handler = getattr(self, "_x_" + type(node).__name__, None)
        if handler:
            return handler(node)
        return None

    def _e(self, node):
        return self._x(node)

    # ---- Programa / Bloco ----

    def _x_Programa(self, n):
        for elem in n.elementos:
            self._x(elem)

    def _x_Bloco(self, n):
        for stmt in n.codigo:
            self._x(stmt)
        for sub in n.subscritas:
            self._x(sub)
        if n.compensacao:
            self._x(n.compensacao)
        if n.plastico:
            self._x(n.plastico)
        if n.modulacao:
            self._x(n.modulacao)

    # ---- Declaracoes ----

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

    def _x_DefinicaoClasse(self, n):
        class_ns = {"__name__": n.nome, "__super__": n.superclasse}
        for membro in n.membros:
            if isinstance(membro, DefinicaoFuncao):
                class_ns[membro.nome] = membro
        self.env.decl(n.nome, class_ns)
        self.env.classes[n.nome] = class_ns

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

    # ---- Chamadas ----

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

    def _x_ChamadaMetodo(self, n):
        obj = self.env.get(n.objeto)
        args = [self._e(a) for a in n.argumentos]
        if isinstance(obj, dict):
            fn = obj.get(n.metodo)
            if isinstance(fn, DefinicaoFuncao):
                call_env = Ambiente(pai=self.env)
                for p, a in zip(fn.parametros, args):
                    call_env.decl(p.nome, a)
                old = self.env
                self.env = call_env
                try:
                    for stmt in fn.corpo:
                        self._x(stmt)
                except ReturnSignal as r:
                    return r.value
                finally:
                    self.env = old
                return None
            elif callable(fn):
                return fn(*args)
        else:
            method = getattr(obj, n.metodo, None)
            if callable(method):
                return method(*args)
        raise GuruDevError(f"metodo '{n.metodo}' nao encontrado em '{n.objeto}'")

    # ---- Controle de fluxo ----

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
            try:
                for s in n.corpo:
                    self._x(s)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _x_Para(self, n):
        self._x(n.inicializacao)
        while self._e(n.condicao):
            try:
                for s in n.corpo:
                    self._x(s)
                self._x(n.incremento)
            except BreakSignal:
                break
            except ContinueSignal:
                self._x(n.incremento)
                continue

    def _x_ParaCada(self, n):
        iteravel = self.env.get(n.iteravel)
        for item in iteravel:
            self.env.decl(n.variavel, item)
            try:
                for s in n.corpo:
                    self._x(s)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _x_Break(self, n):
        raise BreakSignal()

    def _x_Continue(self, n):
        raise ContinueSignal()

    # ---- Execucao Serie / Paralelo / Em ----

    def _x_ExecucaoSerie(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_ExecucaoParalelo(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_ExecucaoEm(self, n):
        lang = n.linguagem.lower()
        if lang == "python":
            for stmt in n.corpo:
                self._x(stmt)
        else:
            raise GuruDevError(f"Execucao em {n.linguagem} nao suportada")

    # ---- Interoperabilidade: Subescrita ----

    def _x_SubescritaLinguagem(self, n):
        if self.semantic_analyzer and self.semantic_analyzer.available:
            analysis = self.semantic_analyzer.analyze_subscrita(n)
            self.subscrita_analyses.append(analysis)
        if n.linguagem == "python" and n.conteudo:
            try:
                local_vars = {}
                exec(n.conteudo, {"__builtins__": builtins}, local_vars)
                self.last_subscrita_result = local_vars
            except Exception as e:
                self.last_subscrita_result = {"__error__": str(e)}
        else:
            self.last_subscrita_result = {"__lang__": n.linguagem}

    # ---- Compensacao ----

    def _x_BlocoCompensacao(self, n):
        for erro in n.erros:
            self._x(erro)
        for d in n.desempenhos:
            self._x(d)
        for alt in n.alternativas:
            self._x(alt)

    def _x_BlocoErro(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_BlocoDesempenho(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_BlocoAlternativa(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    # ---- Plasticidade / Modulacao ----

    def _x_BlocoPlastico(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_BlocoModulacao(self, n):
        for alvo in n.alvos:
            self._x(alvo)

    def _x_ModulacaoAlvo(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    # ---- Expressoes ----

    def _x_Literal(self, n):
        return n.valor

    def _x_Identificador(self, n):
        return self.env.get(n.nome)

    def _x_OperacaoBinaria(self, n):
        left = self._e(n.esquerda)
        right = self._e(n.direita)
        op = n.operador
        if op == "+": return left + right
        if op == "-": return left - right
        if op == "*": return left * right
        if op == "/": return left / right
        if op == "%": return left % right
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == "<": return left < right
        if op == ">": return left > right
        if op == "<=": return left <= right
        if op == ">=": return left >= right
        if op == "&&": return left and right
        if op == "||": return left or right
        raise GuruDevError(f"operador desconhecido: {op}")

    def _x_OperacaoUnaria(self, n):
        val = self._e(n.operando)
        if n.operador == "-":
            return -val
        if n.operador == "!":
            return not val
        raise GuruDevError(f"operador unario desconhecido: {n.operador}")

    def _x_AcessoPropriedade(self, n):
        obj = self.env.get(n.objeto)
        if isinstance(obj, dict):
            return obj.get(n.propriedade)
        return getattr(obj, n.propriedade, None)
