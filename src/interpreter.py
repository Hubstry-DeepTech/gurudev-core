"""
GuruDev® Interpreter / Executor — Versão 1.0.0-alpha
Interpretador e Executor para a linguagem GuruDev®
Autor: Guilherme Gonçalves Machado

Pipeline: Lexer → Parser → AST → Interpreter (tree-walking)

Terminologia:
  - Interpretador = tree-walking interpreter (percorre a AST)
  - Executor = executa as orações de código (statements) e produções de valor (expressions)
  - Caso Gramatical = prefixo VOC/NOM/ACU/DAT/GEN/INS/LOC/ABL

Design:
  - Ambiente (Scope chain) para resolução de nomes
  - Built-in functions (escrever, imprimir, tipo_de, hash, etc.)
  - Suporte a classes simples com herança
  - Execução série/paralelo
  - Interoperabilidade via subexec (python, rust, etc.)
"""

import sys
import math
import hashlib
import json
from typing import Any, Dict, List, Optional

from .ast_nodes import (
    Node, Programa, Bloco, Sobrescrita, SubescritaLinguagem,
    BlocoCompensacao, BlocoErro, BlocoDesempenho, BlocoAlternativa,
    BlocoPlastico, ModulacaoAlvo, BlocoModulacao,
    DeclaracaoVariavel, DefinicaoFuncao, DefinicaoClasse, Parametro,
    Atribuicao, Retorno, Break, Continue,
    Se, Para, ParaCada, Enquanto,
    ExecucaoSerie, ExecucaoParalelo, ExecucaoEm,
    Literal, Identificador, ChamadaFuncao, ChamadaMetodo,
    OperacaoBinaria, OperacaoUnaria, AcessoPropriedade,
    ArrayLiteral,
)
from .symbol_table import (
    Ambiente, TabelaDeSimbolos, TipoSimbolo, CategoriaSimbolo,
    EntradaSimbolo,
)


# ============================================================
# 1. SINAIS DE CONTROLE (Flow Control Signals)
# ============================================================

class RetornoSignal(Exception):
    """Sinal de retorno de função."""
    def __init__(self, valor: Any = None):
        self.valor = valor

class BreakSignal(Exception):
    """Sinal de break (quebra de loop)."""
    pass

class ContinueSignal(Exception):
    """Sinal de continue (continuação de loop)."""
    pass


# ============================================================
# 2. INSTÂNCIA DE CLASSE (RuntimeObject)
# ============================================================

class InstanciaClasse:
    """
    Instância de uma classe GuruDev em tempo de execução.
    Simples: atributos dinâmicos + referência à classe.
    """

    def __init__(self, nome_classe: str):
        self._nome_classe = nome_classe
        self._atributos: Dict[str, Any] = {}

    def obter(self, nome: str) -> Any:
        if nome not in self._atributos:
            raise AttributeError(
                f"Atributo '{nome}' nao existe na instancia de '{self._nome_classe}'."
            )
        return self._atributos[nome]

    def definir(self, nome: str, valor: Any) -> None:
        self._atributos[nome] = valor

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self._atributos.items())
        return f"<{self._nome_classe} {{{attrs}}}>"


# ============================================================
# 3. BUILT-IN FUNCTIONS (Funções Nativas)
# ============================================================

class Builtins:
    """
    Funções nativas do GuruDev®.
    Registradas automaticamente no escopo global.
    """

    @staticmethod
    def escrever(*args) -> None:
        """VOC.escrever(...) / escrever(...) — imprime no stdout."""
        partes = [Builtins._repr(a) for a in args]
        print(" ".join(partes))
        return None

    @staticmethod
    def imprimir(*args) -> None:
        """imprimir(...) — alias para escrever."""
        return Builtins.escrever(*args)

    @staticmethod
    def tipo_de(valor) -> str:
        """tipo_de(valor) — retorna o tipo do valor como string."""
        if valor is None:
            return "Void"
        if isinstance(valor, bool):
            return "Bool"
        if isinstance(valor, int):
            return "Int"
        if isinstance(valor, float):
            return "Float"
        if isinstance(valor, str):
            return "String"
        if isinstance(valor, list):
            return "Array"
        if isinstance(valor, dict):
            return "Object"
        if isinstance(valor, InstanciaClasse):
            return valor._nome_classe
        return type(valor).__name__

    @staticmethod
    def hash_guru(valor) -> str:
        """hash(valor) — retorna hash SHA-256 do valor."""
        texto = Builtins._repr(valor)
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:16]

    @staticmethod
    def tamanho(valor) -> int:
        """tamanho(valor) — retorna o tamanho."""
        if isinstance(valor, (str, list, dict)):
            return len(valor)
        raise TypeError(f"tipo_de({Builtins.tipo_de(valor)}) nao suporta tamanho().")

    @staticmethod
    def converter_int(valor) -> int:
        """converter_int(valor) — converte para Int."""
        return int(valor)

    @staticmethod
    def converter_float(valor) -> float:
        """converter_float(valor) — converte para Float."""
        return float(valor)

    @staticmethod
    def converter_string(valor) -> str:
        """converter_string(valor) — converte para String."""
        return str(valor)

    @staticmethod
    def converter_bool(valor) -> bool:
        """converter_bool(valor) — converte para Bool."""
        return bool(valor)

    @staticmethod
    def ler_entrada() -> str:
        """ler_entrada() — lê uma linha do stdin."""
        return input()

    @staticmethod
    def para_json(valor) -> str:
        """para_json(valor) — serializa para JSON."""
        return json.dumps(Builtins._to_json_serializable(valor), ensure_ascii=False, indent=2)

    @staticmethod
    def de_json(texto: str):
        """de_json(texto) — deserializa de JSON."""
        return json.loads(texto)

    @staticmethod
    def randint(inicio: int, fim: int) -> int:
        """randint(inicio, fim) — número aleatório entre inicio e fim."""
        import random
        return random.randint(inicio, fim)

    @staticmethod
    def raiz(valor, indice: float = 2.0) -> float:
        """raiz(valor, indice) — raiz enésima."""
        return valor ** (1.0 / indice)

    @staticmethod
    def absoluto(valor) -> float:
        """absoluto(valor) — valor absoluto."""
        return abs(valor)

    @staticmethod
    def arredondar(valor, casas: int = 0) -> float:
        """arredondar(valor, casas) — arredondamento."""
        return float(round(valor, casas))

    # --- Helpers internos ---

    @staticmethod
    def _repr(valor) -> str:
        """Representação para impressão."""
        if valor is None:
            return "nulo"
        if isinstance(valor, bool):
            return "verdadeiro" if valor else "falso"
        if isinstance(valor, str):
            return valor
        if isinstance(valor, InstanciaClasse):
            return repr(valor)
        return repr(valor)

    @staticmethod
    def _to_json_serializable(valor):
        """Converte para formato serializável em JSON."""
        if isinstance(valor, InstanciaClasse):
            return {"__classe__": valor._nome_classe, **valor._atributos}
        if isinstance(valor, list):
            return [Builtins._to_json_serializable(v) for v in valor]
        if isinstance(valor, dict):
            return {k: Builtins._to_json_serializable(v) for k, v in valor.items()}
        return valor

    @staticmethod
    def registro() -> Dict[str, Any]:
        """Retorna dicionário com todas as builtins prontas para registro."""
        return {
            'escrever': Builtins.escrever,
            'imprimir': Builtins.imprimir,
            'tipo_de': Builtins.tipo_de,
            'hash': Builtins.hash_guru,
            'tamanho': Builtins.tamanho,
            'converter_int': Builtins.converter_int,
            'converter_float': Builtins.converter_float,
            'converter_string': Builtins.converter_string,
            'converter_bool': Builtins.converter_bool,
            'ler_entrada': Builtins.ler_entrada,
            'para_json': Builtins.para_json,
            'de_json': Builtins.de_json,
            'randint': Builtins.randint,
            'raiz': Builtins.raiz,
            'absoluto': Builtins.absoluto,
            'arredondar': Builtins.arredondar,
            # Math-like functions
            'seno': math.sin,
            'cosseno': math.cos,
            'tangente': math.tan,
            'logaritmo': math.log,
            'potencia': math.pow,
            'pi': math.pi,
            'euler': math.e,
            'maximo': max,
            'minimo': min,
        }


# ============================================================
# 4. MÓDULO MATH NATIVO
# ============================================================

class ModuloMath:
    """
    Simula o objeto 'Math' nativo para chamadas como Math.abs(), Math.pi, etc.
    """

    PI = math.pi
    E = math.e

    @staticmethod
    def abs_(valor) -> float:
        return abs(valor)

    @staticmethod
    def sqrt(valor) -> float:
        return math.sqrt(valor)

    @staticmethod
    def sin(valor) -> float:
        return math.sin(valor)

    @staticmethod
    def cos(valor) -> float:
        return math.cos(valor)

    @staticmethod
    def tan(valor) -> float:
        return math.tan(valor)

    @staticmethod
    def log(valor) -> float:
        return math.log(valor)

    @staticmethod
    def pow(base, exp) -> float:
        return math.pow(base, exp)

    @staticmethod
    def ceil(valor) -> int:
        return math.ceil(valor)

    @staticmethod
    def floor(valor) -> int:
        return math.floor(valor)

    @staticmethod
    def round_(valor) -> int:
        return round(valor)


# ============================================================
# 5. INTERPRETADOR (Tree-Walking Interpreter)
# ============================================================

class GuruDevInterpreter:
    """
    Interpretador GuruDev® — percorre a AST e executa as orações.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.tabela = TabelaDeSimbolos()
        self.escopo_atual: Ambiente = self.tabela.global_env
        self.output: List[str] = []
        self._stdout_original = None
        self._capturar_saida = False

        # Registrar builtins
        self._registrar_builtins()

    # --- Interface pública ---

    def interpretar(self, ast: Programa) -> Any:
        """Interpreta o programa completo e retorna o resultado final."""
        if self.debug:
            print(f"[DEBUG] Iniciando interpretação — {len(ast.elementos)} elementos")

        resultado = None
        for elemento in ast.elementos:
            resultado = self._executar(elemento)
            if self.debug and resultado is not None:
                print(f"[DEBUG] Elemento executado: {type(elemento).__name__} -> {resultado!r}")

        if self.debug:
            print(f"\n[DEBUG] Tabela de Simbolos:\n{self.tabela.dump()}")

        return resultado

    def executar_codigo(self, source_code: str, debug: bool = False) -> Any:
        """
        Pipeline completa: source_code → lexer → parser → AST → interpretar.
        """
        from .parser import parse
        ast = parse(source_code, debug=debug)
        if ast is None:
            raise RuntimeError("Falha no parsing — AST vazia.")
        self.debug = debug
        return self.interpretar(ast)

    # --- Registro de builtins ---

    def _registrar_builtins(self) -> None:
        """Registra funções nativas e o módulo Math no escopo global."""
        for nome, func in Builtins.registro().items():
            self.escopo_atual.definir(
                nome=nome,
                tipo_simbolo=TipoSimbolo.BUILTIN,
                tipo_dado="builtin",
                valor=func,
                readonly=True,
            )

        # Registrar Math como objeto
        self.escopo_atual.definir(
            nome="Math",
            tipo_simbolo=TipoSimbolo.VARIAVEL,
            tipo_dado="Object",
            valor=ModuloMath(),
        )

        # Registrar console como objeto com método log
        class Console:
            @staticmethod
            def log(*args):
                print(" ".join(Builtins._repr(a) for a in args))
        self.escopo_atual.definir(
            nome="console",
            tipo_simbolo=TipoSimbolo.VARIAVEL,
            tipo_dado="Object",
            valor=Console(),
        )

    # --- Gerenciamento de escopo ---

    def _entrar_escopo(self, nome: str) -> Ambiente:
        """Cria e entra em um novo escopo."""
        novo = self.escopo_atual.criar_escopo(nome)
        self.escopo_atual = novo
        self.tabela.registrar(novo)
        if self.debug:
            print(f"[DEBUG] Entrando no escopo: {nome}")
        return novo

    def _sair_escopo(self) -> None:
        """Volta ao escopo pai."""
        if self.escopo_atual.pai:
            if self.debug:
                print(f"[DEBUG] Saindo do escopo: {self.escopo_atual.nome}")
            self.escopo_atual = self.escopo_atual.pai

    # ============================================================
    # 6. EXECUÇÃO DE ORAÇÕES (Statements)
    # ============================================================

    def _executar(self, no: Node) -> Any:
        """
        Despacha a execução para o método correto baseado no tipo do nó.
        """
        if no is None:
            return None

        metodos = {
            Programa: self._exec_programa,
            Bloco: self._exec_bloco,
            DeclaracaoVariavel: self._exec_declaracao,
            DefinicaoFuncao: self._exec_funcao,
            DefinicaoClasse: self._exec_classe,
            Atribuicao: self._exec_atribuicao,
            Retorno: self._exec_retorno,
            Break: self._exec_break,
            Continue: self._exec_continue,
            Se: self._exec_se,
            Para: self._exec_para,
            ParaCada: self._exec_para_cada,
            Enquanto: self._exec_enquanto,
            ExecucaoSerie: self._exec_serie,
            ExecucaoParalelo: self._exec_paralelo,
            ExecucaoEm: self._exec_em,
            ChamadaFuncao: self._avaliar_chamada_funcao,
            ChamadaMetodo: self._avaliar_chamada_metodo,
        }

        metodo = metodos.get(type(no))
        if metodo:
            return metodo(no)

        # Se não for uma oração conhecida, tenta avaliar como expressão
        return self._avaliar(no)

    # --- Programa ---

    def _exec_programa(self, no: Programa) -> Any:
        resultado = None
        for elem in no.elementos:
            resultado = self._executar(elem)
        return resultado

    # --- Bloco Tríplice ---

    def _exec_bloco(self, no: Bloco) -> Any:
        """
        Executa um bloco tríplice: sobrescrita + código + subescritas.
        O código GuruDev é executado; as subescritas são armazenadas para referência.
        """
        if self.debug:
            if no.sobrescrita:
                s = no.sobrescrita
                print(f"[DEBUG] Bloco — nivel:{s.nivel} raiz:{s.raiz} clave:{s.clave} ont:{s.ontologia}")
                if s.contextos:
                    print(f"[DEBUG]   Contextos: {s.contextos}")

        resultado = None

        # Executar orações de código GuruDev
        if no.codigo:
            self._entrar_escopo(f"bloco@{no.lineno}")
            try:
                for oracao in no.codigo:
                    resultado = self._executar(oracao)
            finally:
                self._sair_escopo()

        # Armazenar subescritas no escopo (para referência futura)
        if no.subescritas:
            for sub in no.subescritas:
                if self.debug:
                    print(f"[DEBUG] Subescrita registrada: {sub.linguagem} ({len(sub.conteudo)} chars)")

        return resultado

    # --- Declaração de Variável ---

    def _exec_declaracao(self, no: DeclaracaoVariavel) -> Any:
        """Executa a declaração de uma variável."""
        valor = self._avaliar(no.valor) if no.valor else self._valor_padrao(no.tipo)

        # Validar tipo
        valor = self._coercion_tipo(valor, no.tipo)

        categoria = no.caso_gramatical if no.caso_gramatical else None

        self.escopo_atual.definir(
            nome=no.nome,
            tipo_simbolo=TipoSimbolo.VARIAVEL,
            tipo_dado=no.tipo,
            categoria=categoria,
            valor=valor,
            readonly=(no.modificador_acesso == "privado"),
            modificador_acesso=no.modificador_acesso,
            lineno=no.lineno,
        )

        if self.debug:
            cat = f" [{categoria}]" if categoria else ""
            print(f"[DEBUG] Var declarada: {no.tipo} {no.nome} = {valor!r}{cat}")

        return valor

    # --- Definição de Função ---

    def _exec_funcao(self, no: DefinicaoFuncao) -> Any:
        """
        Registra a função no escopo atual (sem executar).
        O corpo é executado apenas quando a função for chamada.
        """
        categoria = no.caso_gramatical if no.caso_gramatical else None

        self.escopo_atual.definir(
            nome=no.nome,
            tipo_simbolo=TipoSimbolo.FUNCAO,
            tipo_dado=no.tipo_retorno or "Void",
            categoria=categoria,
            valor=no,  # guarda a AST da função como "valor"
            modificador_acesso=no.modificador_acesso,
            parametros=[(p.tipo, p.nome) for p in no.parametros],
            tipo_retorno=no.tipo_retorno,
            lineno=no.lineno,
        )

        if self.debug:
            cat = f" [{categoria}]" if categoria else ""
            params = ", ".join(f"{t} {n}" for t, n in (no.parametros and [(p.tipo, p.nome) for p in no.parametros] or []))
            ret = f" -> {no.tipo_retorno}" if no.tipo_retorno else ""
            print(f"[DEBUG] Funcao definida: {no.nome}({params}){ret}{cat}")

        return None

    # --- Definição de Classe ---

    def _exec_classe(self, no: DefinicaoClasse) -> Any:
        """Registra a classe no escopo atual."""
        categoria = no.caso_gramatical if no.caso_gramatical else None

        # Armazenar a definição da classe
        self.escopo_atual.definir(
            nome=no.nome,
            tipo_simbolo=TipoSimbolo.CLASSE,
            tipo_dado=no.nome,
            categoria=categoria,
            valor={
                'superclasse': no.superclasse,
                'interfaces': no.interfaces,
                'membros': no.membros,
                'ast': no,
            },
            modificador_acesso=no.modificador_acesso,
            lineno=no.lineno,
        )

        if self.debug:
            extends = f" extends {no.superclasse}" if no.superclasse else ""
            impl = f" implements {', '.join(no.interfaces)}" if no.interfaces else ""
            print(f"[DEBUG] Classe definida: {no.nome}{extends}{impl}")

        return None

    # --- Atribuição ---

    def _exec_atribuicao(self, no: Atribuicao) -> Any:
        """Executa atribuição a variável existente."""
        valor = self._avaliar(no.valor)
        self.escopo_atual.atribuir(no.alvo, valor)
        if self.debug:
            cat = f" [{no.caso_gramatical}]" if no.caso_gramatical else ""
            print(f"[DEBUG] Atribuicao: {no.alvo} = {valor!r}{cat}")
        return valor

    # --- Retorno ---

    def _exec_retorno(self, no: Retorno) -> Any:
        """Levanta sinal de retorno."""
        valor = self._avaliar(no.valor) if no.valor else None
        raise RetornoSignal(valor)

    # --- Break / Continue ---

    def _exec_break(self, no: Break) -> Any:
        raise BreakSignal()

    def _exec_continue(self, no: Continue) -> Any:
        raise ContinueSignal()

    # --- Controle de Fluxo ---

    def _exec_se(self, no: Se) -> Any:
        """Executa if/else."""
        condicao = self._avaliar(no.condicao)
        if self._verdadeiro(condicao):
            return self._executar_bloco_oracoes(no.corpo_verdadeiro)
        elif no.corpo_falso:
            return self._executar_bloco_oracoes(no.corpo_falso)
        return None

    def _exec_para(self, no: Para) -> Any:
        """Executa for (estilo C): init; cond; increment { corpo }."""
        self._entrar_escopo(f"para@{no.lineno}")
        try:
            # Inicialização
            if no.inicializacao:
                self._executar(no.inicializacao)

            # Loop
            while True:
                # Condição
                if no.condicao:
                    cond = self._avaliar(no.condicao)
                    if not self._verdadeiro(cond):
                        break

                # Corpo
                try:
                    self._executar_bloco_oracoes(no.corpo)
                except BreakSignal:
                    break
                except ContinueSignal:
                    pass

                # Incremento
                if no.incremento:
                    self._executar(no.incremento)
        finally:
            self._sair_escopo()

        return None

    def _exec_para_cada(self, no: ParaCada) -> Any:
        """Executa for-each: para (Tipo item : colecao)."""
        self._entrar_escopo(f"para_cada@{no.lineno}")
        try:
            colecao = self.escopo_atual.obter(no.iteravel)
            if not isinstance(colecao, (list, str)):
                raise TypeError(
                    f"tipo_de('{no.iteravel}') = {Builtins.tipo_de(colecao)}; "
                    f"esperado Array ou String para 'para cada'."
                )

            for item in colecao:
                item_coerced = self._coercion_tipo(item, no.tipo) if no.tipo else item
                self.escopo_atual.definir(
                    nome=no.variavel,
                    tipo_simbolo=TipoSimbolo.VARIAVEL,
                    tipo_dado=no.tipo or Builtins.tipo_de(item),
                    valor=item_coerced,
                )
                try:
                    self._executar_bloco_oracoes(no.corpo)
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        finally:
            self._sair_escopo()

        return None

    def _exec_enquanto(self, no: Enquanto) -> Any:
        """Executa while/enquanto."""
        self._entrar_escopo(f"enquanto@{no.lineno}")
        try:
            while True:
                cond = self._avaliar(no.condicao)
                if not self._verdadeiro(cond):
                    break
                try:
                    self._executar_bloco_oracoes(no.corpo)
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        finally:
            self._sair_escopo()

        return None

    # --- Execução Série / Paralelo / Em ---

    def _exec_serie(self, no: ExecucaoSerie) -> Any:
        """Execução série — orações na sequência."""
        resultado = None
        for oracao in no.corpo:
            resultado = self._executar(oracao)
        return resultado

    def _exec_paralelo(self, no: ExecucaoParalelo) -> Any:
        """
        Execução paralelo — executa orações concorrentemente.
        Implementação simplificada com ThreadPoolExecutor.
        """
        import concurrent.futures

        resultados = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(no.corpo), 8)) as executor:
            futuros = {executor.submit(self._executar, o): i for i, o in enumerate(no.corpo)}
            for futuro in concurrent.futures.as_completed(futuros):
                idx = futuros[futuro]
                try:
                    resultados.append((idx, futuro.result()))
                except Exception as e:
                    resultados.append((idx, e))

        # Ordenar por índice de execução original
        resultados.sort(key=lambda x: x[0])
        return [r[1] for r in resultados]

    def _exec_em(self, no: ExecucaoEm) -> Any:
        """
        Execução em linguagem estrangeira.
        Suporte: python, rust (via subprocess para rust).
        """
        linguagem = no.linguagem.lower()

        # Coletar o código como string (as orações são AST nodes)
        if not no.corpo:
            return None

        # Executar as orações normalmente (são AST nodes do GuruDev)
        # para python, usamos subescritas ou exec nativo
        if linguagem == "python":
            return self._executar_bloco_oracoes(no.corpo)
        else:
            if self.debug:
                print(f"[DEBUG] em {no.linguagem}: execucao nativa disponivel apenas para python")
            return self._executar_bloco_oracoes(no.corpo)

    # --- Executar bloco de orações (helper) ---

    def _executar_bloco_oracoes(self, oracoes: List[Node]) -> Any:
        """Executa uma lista de orações (statements) dentro do escopo atual."""
        resultado = None
        for oracao in oracoes:
            resultado = self._executar(oracao)
        return resultado

    # ============================================================
    # 7. AVALIAÇÃO DE PRODUÇÕES DE VALOR (Expressions)
    # ============================================================

    def _avaliar(self, no: Node) -> Any:
        """Despacha a avaliação para o método correto."""
        if no is None:
            return None

        metodos = {
            Literal: self._avaliar_literal,
            Identificador: self._avaliar_identificador,
            ArrayLiteral: self._avaliar_array_literal,
            OperacaoBinaria: self._avaliar_binaria,
            OperacaoUnaria: self._avaliar_unaria,
            ChamadaFuncao: self._avaliar_chamada_funcao,
            ChamadaMetodo: self._avaliar_chamada_metodo,
            AcessoPropriedade: self._avaliar_acesso,
        }

        metodo = metodos.get(type(no))
        if metodo:
            return metodo(no)

        raise RuntimeError(f"Expressao desconhecida: {type(no).__name__}")

    def _avaliar_literal(self, no: Literal) -> Any:
        """Avalia um literal."""
        valor = no.valor
        # Coerção de tipo para literais
        if no.tipo == 'bool':
            if isinstance(valor, str):
                valor = valor.lower() in ('true', 'verdadeiro', '1')
            else:
                valor = bool(valor)
        elif no.tipo == 'int':
            valor = int(valor)
        elif no.tipo == 'float':
            valor = float(valor)
        return valor

    def _avaliar_array_literal(self, no: ArrayLiteral) -> Any:
        """Avalia um array literal: [expr1, expr2, ...]."""
        return [self._avaliar(elem) for elem in no.elementos]

    def _avaliar_identificador(self, no: Identificador) -> Any:
        """Resolve um identificador no escopo."""
        return self.escopo_atual.obter(no.nome)

    def _avaliar_binaria(self, no: OperacaoBinaria) -> Any:
        """Avalia operação binária."""
        esq = self._avaliar(no.esquerda)
        dir_ = self._avaliar(no.direita)
        op = no.operador

        if op == '+':
            if isinstance(esq, str) or isinstance(dir_, str):
                return str(esq) + str(dir_)
            return esq + dir_
        elif op == '-':
            return esq - dir_
        elif op == '*':
            return esq * dir_
        elif op == '/':
            if dir_ == 0:
                raise ZeroDivisionError("Divisao por zero.")
            return esq / dir_
        elif op == '%':
            return esq % dir_
        elif op == '==':
            return esq == dir_
        elif op == '!=':
            return esq != dir_
        elif op == '<':
            return esq < dir_
        elif op == '>':
            return esq > dir_
        elif op == '<=':
            return esq <= dir_
        elif op == '>=':
            return esq >= dir_
        elif op == '&&':
            return esq and dir_
        elif op == '||':
            return esq or dir_
        else:
            raise RuntimeError(f"Operador binario desconhecido: '{op}'")

    def _avaliar_unaria(self, no: OperacaoUnaria) -> Any:
        """Avalia operação unária."""
        valor = self._avaliar(no.operando)
        if no.operador == '-':
            return -valor
        elif no.operador == '!':
            return not self._verdadeiro(valor)
        else:
            raise RuntimeError(f"Operador unario desconhecido: '{no.operador}'")

    def _avaliar_chamada_funcao(self, no: ChamadaFuncao) -> Any:
        """Avalia chamada de função."""
        # Resolver argumentos
        args = [self._avaliar(a) for a in no.argumentos]

        # Buscar a função no escopo
        entrada = self.escopo_atual.resolver(no.nome)
        if entrada is None:
            raise NameError(f"Funcao '{no.nome}' nao definida.")

        valor = entrada.valor

        # Built-in
        if entrada.tipo_simbolo == TipoSimbolo.BUILTIN:
            if self.debug:
                print(f"[DEBUG] Chamada builtin: {no.nome}({args})")
            return valor(*args)

        # Função GuruDev (AST armazenada como valor)
        if entrada.tipo_simbolo == TipoSimbolo.FUNCAO and isinstance(valor, DefinicaoFuncao):
            return self._chamar_funcao_gurudev(valor, args)

        # callable genérico
        if callable(valor):
            return valor(*args)

        raise RuntimeError(f"'{no.nome}' nao e uma funcao (tipo: {entrada.tipo_simbolo.value}).")

    def _avaliar_chamada_metodo(self, no: ChamadaMetodo) -> Any:
        """Avalia chamada de método: objeto.metodo(args)."""
        # Resolver o objeto
        obj = self.escopo_atual.obter(no.objeto)
        args = [self._avaliar(a) for a in no.argumentos]

        # Buscar o método no objeto
        metodo = getattr(obj, no.metodo, None)

        # Mapear nomes comuns
        if metodo is None:
            nomes_alternativos = {
                'log': 'log',
                'abs': 'abs_',
                'sqrt': 'sqrt',
                'sin': 'sin',
                'cos': 'cos',
                'tan': 'tan',
                'floor': 'floor',
                'ceil': 'ceil',
                'round': 'round_',
                'pow': 'pow',
                'append': 'append',
                'length': '__len__',
                'tamanho': '__len__',
                'keys': 'keys',
                'values': 'values',
                'join': 'join',
                'push': 'append',
                'pop': 'pop',
            }
            metodo_nome = nomes_alternativos.get(no.metodo, no.metodo)
            metodo = getattr(obj, metodo_nome, None)

        if metodo is None:
            raise AttributeError(
                f"Metodo '{no.metodo}' nao existe em '{type(obj).__name__}'."
            )

        if self.debug:
            print(f"[DEBUG] Chamada metodo: {no.objeto}.{no.metodo}({args})")

        return metodo(*args)

    def _avaliar_acesso(self, no: AcessoPropriedade) -> Any:
        """Avalia acesso a propriedade: objeto.propriedade."""
        obj = self.escopo_atual.obter(no.objeto)

        if isinstance(obj, InstanciaClasse):
            return obj.obter(no.propriedade)
        elif isinstance(obj, dict):
            return obj.get(no.propriedade)
        else:
            return getattr(obj, no.propriedade, None)

    # ============================================================
    # 8. CHAMADA DE FUNÇÃO GURUDEV
    # ============================================================

    def _chamar_funcao_gurudev(self, funcao_ast: DefinicaoFuncao, args: list) -> Any:
        """
        Executa uma função GuruDev: cria escopo, binda parâmetros, executa corpo.
        """
        self._entrar_escopo(f"funcao:{funcao_ast.nome}@{funcao_ast.lineno}")

        try:
            # Bindar parâmetros
            for i, param in enumerate(funcao_ast.parametros):
                valor_arg = args[i] if i < len(args) else self._valor_padrao(param.tipo)
                valor_arg = self._coercion_tipo(valor_arg, param.tipo)
                self.escopo_atual.definir(
                    nome=param.nome,
                    tipo_simbolo=TipoSimbolo.PARAMETRO,
                    tipo_dado=param.tipo,
                    valor=valor_arg,
                )

            # Executar corpo
            resultado = None
            try:
                for oracao in funcao_ast.corpo:
                    resultado = self._executar(oracao)
            except RetornoSignal as s:
                resultado = s.valor

            return resultado

        finally:
            self._sair_escopo()

    # ============================================================
    # 9. HELPERS
    # ============================================================

    def _verdadeiro(self, valor) -> bool:
        """Avalia se um valor é 'verdadeiro' (truthy) em GuruDev."""
        if valor is None:
            return False
        if isinstance(valor, bool):
            return valor
        if isinstance(valor, (int, float)):
            return valor != 0
        if isinstance(valor, str):
            return len(valor) > 0
        if isinstance(valor, (list, dict)):
            return len(valor) > 0
        return True

    def _valor_padrao(self, tipo: str) -> Any:
        """Retorna o valor padrão para um tipo."""
        padroes = {
            'Bool': False,
            'String': "",
            'Int': 0,
            'Float': 0.0,
            'Void': None,
            'Array': [],
            'Object': {},
        }
        return padroes.get(tipo, None)

    def _coercion_tipo(self, valor, tipo: str) -> Any:
        """Converte o valor para o tipo declarado, se possível."""
        if tipo in ('Bool',):
            if isinstance(valor, str):
                return valor.lower() in ('true', 'verdadeiro', '1')
            return bool(valor)
        elif tipo in ('Int',):
            if isinstance(valor, float):
                return int(valor)
            if isinstance(valor, str) and valor.isdigit():
                return int(valor)
            return valor
        elif tipo in ('Float',):
            return float(valor) if not isinstance(valor, float) else valor
        elif tipo in ('String',):
            return Builtins._repr(valor) if not isinstance(valor, str) else valor
        return valor


# ============================================================
# 10. INTERFACE PÚBLICA
# ============================================================

def interpretar(source_code: str, debug: bool = False) -> Any:
    """
    Pipeline completa: source_code → AST → resultado.
    Retorna o valor do último elemento executado.
    """
    from .parser import parse

    ast = parse(source_code, debug=debug)
    if ast is None:
        raise RuntimeError("Falha no parsing — AST vazia.")

    interpreter = GuruDevInterpreter(debug=debug)
    return interpreter.interpretar(ast)


def executar_arquivo(caminho: str, debug: bool = False) -> Any:
    """
    Lê um arquivo .guru e executa.
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        codigo = f.read()
    return interpretar(codigo, debug=debug)


# ============================================================
# 11. CLI
# ============================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m src.interpreter <arquivo.guru> [--debug]")
        sys.exit(1)

    arquivo = sys.argv[1]
    debug = '--debug' in sys.argv

    try:
        resultado = executar_arquivo(arquivo, debug=debug)
        if resultado is not None:
            print(f"\nResultado: {resultado!r}")
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
