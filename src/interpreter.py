"""GuruDev Interpreter v1.2.0-alpha — Hermeneutic dispatch + compensacao + Alexandria + Quantum"""
import copy
import math
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


HERMENEUTIC_ORDINAL = {
    "literal": 1, "alegorico": 2, "moral": 3, "mistico": 4,
    "funcional": 5, "estetico": 6, "ontologico": 7, "holistico": 8,
    "matematico": 9, "simbolico": 10, "parabolico": 11,
    "historico": 12, "linguistico": 13,
}


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
    """Interpretador tree-walking GuruDev com dispatch hermeneutico e Alexandria."""

    def __init__(self):
        self.env = Ambiente()
        self.call_log = []
        self.recipients = {}
        self.subscrita_analyses = []
        self.last_subscrita_result = None
        self.semantic_analyzer = None
        self.significance_vectors = []
        self.hermeneutic_log = []
        self.quantum_results = []
        self._hermeneutic_handlers = {
            "literal": self._h_literal,
            "ontologico": self._h_ontologico,
        }
        self._init_alexandria()

    def _init_alexandria(self):
        try:
            from .semantic_analyzer import SemanticAnalyzer
            self.semantic_analyzer = SemanticAnalyzer()
        except Exception:
            pass
        self._quantum_interface_available = False
        try:
            from alexandria.core.quantum_interface import (
                classificar_delegacao,
                classificar_por_nome,
                verificar_contencao,
                PERFIS_CONJECTURAIS,
                PERFIS_ALGORITMOS,
            )
            self._quantum_interface_available = True
            self._qi_classificar = classificar_delegacao
            self._qi_classificar_nome = classificar_por_nome
            self._qi_verificar = verificar_contencao
            self._qi_perfis = PERFIS_CONJECTURAIS
            self._qi_algoritmos = PERFIS_ALGORITMOS
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

    # ================================================================
    # HERMENEUTIC DISPATCH
    # ================================================================

    def _exec_bloco_com_compensacao(self, bloco):
        """Executa codigo + subscritas com compensacao condicional (so em except)."""
        try:
            for stmt in bloco.codigo:
                self._x(stmt)
            if hasattr(bloco, 'subscritas') and bloco.subscritas:
                for sub in bloco.subscritas:
                    self._x(sub)
        except (ReturnSignal, BreakSignal, ContinueSignal):
            raise
        except Exception as e:
            if bloco.compensacao:
                if bloco.compensacao.erros:
                    for err_block in bloco.compensacao.erros:
                        self._x(err_block)
                    return
                elif bloco.compensacao.alternativas:
                    for alt in bloco.compensacao.alternativas:
                        self._x(alt)
                    return
            raise
    
    def _h_literal(self, bloco):
        """Nivel Literal: executa diretamente, sem anotacao."""
        self._exec_bloco_com_compensacao(bloco)

    def _h_ontologico(self, bloco):
        """Nivel Ontologico: executa + calcula Significance Vector R5 + R6 (quantico)."""
        self._exec_bloco_com_compensacao(bloco)
        sv = self._significance_vector(bloco)
        # R6 hexarrelacional quando paradigma quantico
        if self._is_quantum_paradigm(bloco.gm_paradigma):
            r6 = self._hexarelational_vector(bloco)
            sv["r6_hexarrelacional"] = r6["vector"]
            sv["r6_norm"] = r6["norm"]
            sv["r6_fonte"] = r6["fonte"]
        self.significance_vectors.append(sv)

    def _h_default(self, bloco):
        """Nivel padrao: executa + anota nivel hermeneutico."""
        self._exec_bloco_com_compensacao(bloco)
        if bloco.gm_hermeneutica:
            self.hermeneutic_log.append(bloco.gm_hermeneutica)

    # ================================================================
    # SIGNIFICANCE VECTOR (R5) + HEXARRELACIONAL (R6)
    # ================================================================

    def _significance_vector(self, bloco):
        """Calcula Significance Vector R5 e norma Euclidiana."""
        v0 = self._categorical_hash(bloco.gm_ontologia)
        v1 = self._categorical_hash(bloco.gm_campo)
        v2 = HERMENEUTIC_ORDINAL.get(bloco.gm_hermeneutica, 0) / 13.0
        v3 = self._categorical_hash(bloco.gm_tempo)
        v4 = self._categorical_hash(bloco.gm_paradigma)
        norm = math.sqrt(v0*v0 + v1*v1 + v2*v2 + v3*v3 + v4*v4)
        return {
            "vector": [v0, v1, v2, v3, v4],
            "norm": round(norm, 6),
            "gm_ontologia": bloco.gm_ontologia,
            "gm_campo": bloco.gm_campo,
            "gm_hermeneutica": bloco.gm_hermeneutica,
            "gm_tempo": bloco.gm_tempo,
            "gm_paradigma": bloco.gm_paradigma,
        }

    def _is_quantum_paradigm(self, paradigma):
        """Verifica se o paradigma indica contexto quantico."""
        if paradigma is None:
            return False
        p = paradigma.lower()
        quantum_markers = [
            "quantico", "quantica", "quantum",
            "qiskit", "q#", "cirq", "pennylane",
            "gate-based", "variacional", "hibrido",
            "vqe", "qaoa", "shor", "grover",
        ]
        return any(marker in p for marker in quantum_markers)

    def _hexarelational_vector(self, bloco):
        """
        Calcula vetor hexarrelacional R6 (rho1-rho6) para blocos quanticos.

        Se gm_paradigma corresponder a uma linguagem/algoritmo conhecido,
        usa o perfil conjectural. Caso contrario, computa a partir das
        dimensoes do bloco via hash categorico.

        Returns:
            Dicionario com vector (6 floats), norm, fonte
        """
        if self._quantum_interface_available:
            paradigma = (bloco.gm_paradigma or "").lower()
            # Buscar perfil conjectural por nome
            for nome, dados in self._qi_perfis.items():
                if nome.lower() in paradigma:
                    rho = dados["rho"]
                    fonte = dados.get("fonte", "PERFIS_CONJECTURAIS")
                    norm = math.sqrt(sum(v*v for v in rho))
                    return {
                        "vector": rho,
                        "norm": round(norm, 6),
                        "fonte": fonte,
                    }
            for nome, dados in self._qi_algoritmos.items():
                if nome.lower() in paradigma:
                    rho = dados["rho"]
                    fonte = dados.get("fonte", "PERFIS_ALGORITMOS")
                    norm = math.sqrt(sum(v*v for v in rho))
                    return {
                        "vector": rho,
                        "norm": round(norm, 6),
                        "fonte": fonte,
                    }

        # Fallback: computar R6 via hash categorico das dimensoes do bloco
        dimensoes = [
            bloco.gm_ontologia or "",
            bloco.gm_campo or "",
            bloco.gm_hermeneutica or "",
            bloco.gm_tempo or "",
            bloco.gm_paradigma or "",
            "quantico",  # 6a dimensao: paradigma quantico
        ]
        rho = [self._categorical_hash(d) for d in dimensoes]
        norm = math.sqrt(sum(v*v for v in rho))
        return {
            "vector": rho,
            "norm": round(norm, 6),
            "fonte": "hash_categorico_fallback",
        }

    @staticmethod
    def _categorical_hash(value):
        """Converte string categorica para float em [0, 1]."""
        if value is None:
            return 0.0
        h = 0
        for ch in value:
            h = (h * 31 + ord(ch)) % 997
        return h / 997.0

    # ================================================================
    # PROGRAMA / BLOCO
    # ================================================================

    def _x_Programa(self, n):
        for elem in n.elementos:
            self._x(elem)

    def _x_Bloco(self, n):
        handler = self._hermeneutic_handlers.get(n.gm_hermeneutica, self._h_default)
        handler(n)
        if n.plastico:
            self._x(n.plastico)
        if n.modulacao:
            self._x(n.modulacao)

    # ================================================================
    # DECLARACOES
    # ================================================================

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

    # ================================================================
    # CHAMADAS
    # ================================================================

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

    # ================================================================
    # CONTROLE DE FLUXO
    # ================================================================

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

    # ================================================================
    # EXECUCAO SERIE / PARALELO / EM
    # ================================================================

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

    # ================================================================
    # INTEROPERABILIDADE: SUBESCRTA
    # ================================================================

    def _x_SubescritaLinguagem(self, n):
        if self.semantic_analyzer and self.semantic_analyzer.available:
            analysis = self.semantic_analyzer.analyze_subscrita(n)
            self.subscrita_analyses.append(analysis)
        if n.linguagem == "python" and n.conteudo:
            try:
                local_vars = {}
                exec(n.conteudo, {"__builtins__": builtins}, local_vars)
                self.last_subscrita_result = local_vars
                for nome, valor in local_vars.items():
                    if not nome.startswith("__"):
                        self.env.decl(nome, valor)
            except Exception as e:
                self.last_subscrita_result = {"__error__": str(e)}
        else:
            self.last_subscrita_result = {"__lang__": n.linguagem}

    # ================================================================
    # COMPENSACAO
    # ================================================================

    

    def _x_BlocoErro(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_BlocoDesempenho(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_BlocoAlternativa(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    # ================================================================
    # PLASTICIDADE / MODULACAO
    # ================================================================

    def _x_BlocoPlastico(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    def _x_BlocoModulacao(self, n):
        for alvo in n.alvos:
            self._x(alvo)

    def _x_ModulacaoAlvo(self, n):
        for stmt in n.corpo:
            self._x(stmt)

    # ================================================================
    # EXPRESSOES
    # ================================================================

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

    # ================================================================
    # QUANTUM DISPATCH — Protocolo Semantico Classico-Quantico
    # ================================================================

    def dispatch_quantico(self, operacao, perfil=None, nome=None, n_qubits=2, shots=1024):
        """
        Despacha uma operacao quantica via protocolo GuruDev.

        GuruDev NAO executa computacao quantica real — e o protocolo semantico
        que governa a interface classico-quantica. Este metodo:
        1. Verifica contencao constitucional (AUSENTES_QUANTICO)
        2. Classifica a delegacao via rho1-rho6
        3. Gera QuantumResult probabilistico simulado

        Args:
            operacao: Nome da operacao quantica
            perfil: Perfil hexarrelacional [rho1..rho6] (opcional)
            nome: Nome da linguagem/algoritmo para lookup (opcional)
            n_qubits: Numero de qubits para simulacao (default 2)
            shots: Numero de medicoes simuladas (default 1024)

        Returns:
            QuantumResult com distribuicao probabilistica
        """
        from .quantum_result import QuantumResult

        # 1. Verificar contencao constitucional
        if self._quantum_interface_available:
            contencao = self._qi_verificar(operacao)
            if not contencao.contida:
                qr = QuantumResult.error(
                    mensagem=contencao.justificativa,
                    operacao=operacao,
                )
                qr.metadata["limite_constitucional"] = contencao.limite_constitucional
                self.quantum_results.append(qr)
                return qr

        # 2. Classificar delegacao
        delegacao_tipo = "conservacao"  # default
        rho_perfil = perfil or [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

        if self._quantum_interface_available:
            if perfil:
                resultado = self._qi_classificar(rho_perfil, nome=nome or operacao)
                delegacao_tipo = resultado.tipo.value
                rho_perfil = resultado.perfil
            elif nome:
                resultado = self._qi_classificar_nome(nome)
                if resultado:
                    delegacao_tipo = resultado.tipo.value
                    rho_perfil = resultado.perfil

        # 3. Gerar resultado probabilistico simulado
        qr = QuantumResult.simulate(
            n_qubits=n_qubits,
            delegacao_tipo=delegacao_tipo,
            operacao=operacao,
            perfil_rho=rho_perfil,
            shots=shots,
        )
        qr.metadata["delegacao_classificada"] = True

        self.quantum_results.append(qr)
        return qr

    def verificar_contencao_quantica(self, operacao):
        """
        Verifica se uma operacao quantica esta contida no protocolo.

        Args:
            operacao: Nome da operacao a verificar

        Returns:
            Dict com 'contida', 'categoria', 'justificativa' ou None se interface indisponivel
        """
        if not self._quantum_interface_available:
            return None
        r = self._qi_verificar(operacao)
        return {
            "contida": r.contida,
            "categoria": r.categoria,
            "justificativa": r.justificativa,
            "limite_constitucional": r.limite_constitucional,
        }
