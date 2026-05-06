"""
GuruDev Interpreter v1.1.0-alpha
Hubstry-DeepTech

Changes from v1.0:
  - String methods: tamanho, maiusculo, minusculo, dividir, substring, trim,
    contem, substituir, indice, repetir, vazio, minusculo_primeiro, maiusculo_primeiro
  - Array methods: tamanho, adicionar, remover_ultimo, contem, ordenar,
    juntar, remover, inserir, inverter, vazio, fatiar, ultimo, primeiro
  - Functional classes: attributes, methods, iniciar(), this/isto, instantiation
  - Property assignment: obj.attr = valor
  - Property access on string literals and arrays via chaining
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
    ArrayLiteral, PropAtribuicao,
)
from .symbol_table import (
    Ambiente, TabelaDeSimbolos, TipoSimbolo, CategoriaSimbolo,
    EntradaSimbolo,
)


# ============================================================
# 1. SINAIS DE CONTROLE (Flow Control Signals)
# ============================================================

class RetornoSignal(Exception):
    """Sinal de retorno de funcao."""
    def __init__(self, valor: Any = None):
        self.valor = valor

class BreakSignal(Exception):
    """Sinal de break (quebra de loop)."""
    pass

class ContinueSignal(Exception):
    """Sinal de continue (continuacao de loop)."""
    pass


# ============================================================
# 2. INSTANCIA DE CLASSE (RuntimeObject)
# ============================================================

class InstanciaClasse:
    """
    Instancia de uma classe GuruDev em tempo de execucao.
    Atributos dinamicos + referencia a definicao da classe.
    """

    def __init__(self, nome_classe: str, classe_def: dict):
        self._nome_classe = nome_classe
        self._classe_def = classe_def  # {'superclasse', 'interfaces', 'membros', 'ast'}
        self._atributos: Dict[str, Any] = {}
        self._metodos: Dict[str, 'DefinicaoFuncao'] = {}

        # Registrar metodos da classe
        for membro in classe_def.get('membros', []):
            if isinstance(membro, DefinicaoFuncao):
                self._metodos[membro.nome] = membro
            elif isinstance(membro, DeclaracaoVariavel):
                # Atributo default
                if membro.valor is not None:
                    self._atributos[membro.nome] = None  # placeholder, evaluated later

    def obter(self, nome: str) -> Any:
        if nome in self._atributos:
            return self._atributos[nome]
        if nome in self._metodos:
            return self._metodos[nome]
        # Check superclass chain
        if nome in ('this', 'isto'):
            return self
        raise AttributeError(
            f"Atributo ou metodo '{nome}' nao existe na instancia de '{self._nome_classe}'."
        )

    def definir(self, nome: str, valor: Any) -> None:
        self._atributos[nome] = valor

    def tem_metodo(self, nome: str) -> bool:
        return nome in self._metodos

    def obter_metodo(self, nome: str) -> Optional['DefinicaoFuncao']:
        return self._metodos.get(nome)

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={Builtins._repr(v)}" for k, v in self._atributos.items())
        return f"<{self._nome_classe} {{{attrs}}}>"


# ============================================================
# 3. BUILT-IN FUNCTIONS
# ============================================================

class Builtins:
    """
    Funcoes nativas do GuruDev.
    Registradas automaticamente no escopo global.
    """

    @staticmethod
    def escrever(*args) -> None:
        """escrever(...) — imprime no stdout."""
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
        return int(valor)

    @staticmethod
    def converter_float(valor) -> float:
        return float(valor)

    @staticmethod
    def converter_string(valor) -> str:
        return str(valor)

    @staticmethod
    def converter_bool(valor) -> bool:
        return bool(valor)

    @staticmethod
    def ler_entrada() -> str:
        return input()

    @staticmethod
    def para_json(valor) -> str:
        return json.dumps(Builtins._to_json_serializable(valor), ensure_ascii=False, indent=2)

    @staticmethod
    def de_json(texto: str):
        return json.loads(texto)

    @staticmethod
    def randint(inicio: int, fim: int) -> int:
        import random
        return random.randint(inicio, fim)

    @staticmethod
    def raiz(valor, indice: float = 2.0) -> float:
        return valor ** (1.0 / indice)

    @staticmethod
    def absoluto(valor) -> float:
        return abs(valor)

    @staticmethod
    def arredondar(valor, casas: int = 0) -> float:
        return float(round(valor, casas))

    # --- Helpers internos ---

    @staticmethod
    def _repr(valor) -> str:
        """Representacao para impressao."""
        if valor is None:
            return "nulo"
        if isinstance(valor, bool):
            return "verdadeiro" if valor else "falso"
        if isinstance(valor, str):
            return valor
        if isinstance(valor, InstanciaClasse):
            return repr(valor)
        if isinstance(valor, float) and valor == int(valor):
            return str(int(valor))
        return repr(valor)

    @staticmethod
    def _to_json_serializable(valor):
        if isinstance(valor, InstanciaClasse):
            return {"__classe__": valor._nome_classe, **valor._atributos}
        if isinstance(valor, list):
            return [Builtins._to_json_serializable(v) for v in valor]
        if isinstance(valor, dict):
            return {k: Builtins._to_json_serializable(v) for k, v in valor.items()}
        return valor

    @staticmethod
    def registro() -> Dict[str, Any]:
        """Retorna dicionario com todas as builtins prontas para registro."""
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
# 4. STRING METHOD DISPATCHER
# ============================================================

class StringMethods:
    """Dispatch de metodos de string em GuruDev."""

    _METHODS = {}

    @classmethod
    def dispatch(cls, obj_str: str, metodo: str, args: list) -> Any:
        handler = cls._METHODS.get(metodo)
        if handler:
            return handler(obj_str, *args)
        raise AttributeError(
            f"Metodo '{metodo}' nao existe em String."
        )

    @classmethod
    def register(cls, name):
        def decorator(fn):
            cls._METHODS[name] = fn
            return fn
        return decorator

# Register all string methods

@StringMethods.register('tamanho')
def _str_tamanho(s: str) -> int:
    return len(s)

@StringMethods.register('length')
def _str_length(s: str) -> int:
    return len(s)

@StringMethods.register('maiusculo')
def _str_maiusculo(s: str) -> str:
    return s.upper()

@StringMethods.register('minusculo')
def _str_minusculo(s: str) -> str:
    return s.lower()

@StringMethods.register('dividir')
def _str_dividir(s: str, sep: str = " ") -> list:
    return s.split(sep)

@StringMethods.register('substring')
def _str_substring(s: str, inicio: int, fim: int = -1) -> str:
    if fim == -1 or fim is None:
        return s[inicio:]
    return s[inicio:fim]

@StringMethods.register('trim')
def _str_trim(s: str) -> str:
    return s.strip()

@StringMethods.register('contem')
def _str_contem(s: str, sub: str) -> bool:
    return sub in s

@StringMethods.register('substituir')
def _str_substituir(s: str, antigo: str, novo: str) -> str:
    return s.replace(antigo, novo)

@StringMethods.register('indice')
def _str_indice(s: str, sub: str) -> int:
    return s.find(sub)

@StringMethods.register('repetir')
def _str_repetir(s: str, n: int) -> str:
    return s * n

@StringMethods.register('vazio')
def _str_vazio(s: str) -> bool:
    return len(s) == 0

@StringMethods.register('maiusculo_primeiro')
def _str_capitalize(s: str) -> str:
    if not s:
        return s
    return s[0].upper() + s[1:]

@StringMethods.register('minusculo_primeiro')
def _str_lower_first(s: str) -> str:
    if not s:
        return s
    return s[0].lower() + s[1:]

@StringMethods.register('inverter')
def _str_reverse(s: str) -> str:
    return s[::-1]

@StringMethods.register('comeca_com')
def _str_startswith(s: str, prefixo: str) -> bool:
    return s.startswith(prefixo)

@StringMethods.register('termina_com')
def _str_endswith(s: str, sufixo: str) -> bool:
    return s.endswith(sufixo)

@StringMethods.register('ultimo_indice')
def _str_rfind(s: str, sub: str) -> int:
    return s.rfind(sub)


# ============================================================
# 5. ARRAY METHOD DISPATCHER
# ============================================================

class ArrayMethods:
    """Dispatch de metodos de array em GuruDev."""

    _METHODS = {}

    @classmethod
    def dispatch(cls, obj_list: list, metodo: str, args: list) -> Any:
        handler = cls._METHODS.get(metodo)
        if handler:
            return handler(obj_list, *args)
        raise AttributeError(
            f"Metodo '{metodo}' nao existe em Array."
        )

    @classmethod
    def register(cls, name):
        def decorator(fn):
            cls._METHODS[name] = fn
            return fn
        return decorator

# Register all array methods

@ArrayMethods.register('tamanho')
def _arr_tamanho(arr: list) -> int:
    return len(arr)

@ArrayMethods.register('length')
def _arr_length(arr: list) -> int:
    return len(arr)

@ArrayMethods.register('adicionar')
def _arr_adicionar(arr: list, item) -> None:
    arr.append(item)
    return None

@ArrayMethods.register('push')
def _arr_push(arr: list, item) -> None:
    arr.append(item)
    return None

@ArrayMethods.register('remover_ultimo')
def _arr_remover_ultimo(arr: list):
    if not arr:
        raise RuntimeError("remover_ultimo() em array vazio.")
    return arr.pop()

@ArrayMethods.register('pop')
def _arr_pop(arr: list):
    if not arr:
        raise RuntimeError("pop() em array vazio.")
    return arr.pop()

@ArrayMethods.register('contem')
def _arr_contem(arr: list, item) -> bool:
    return item in arr

@ArrayMethods.register('ordenar')
def _arr_ordenar(arr: list) -> list:
    arr.sort()
    return arr

@ArrayMethods.register('juntar')
def _arr_juntar(arr: list, sep: str = ", ") -> str:
    return Builtins._repr(sep).join(Builtins._repr(x) for x in arr)

@ArrayMethods.register('remover')
def _arr_remover(arr: list, item) -> None:
    if item in arr:
        arr.remove(item)
    return None

@ArrayMethods.register('inserir')
def _arr_inserir(arr: list, indice: int, item) -> None:
    arr.insert(indice, item)
    return None

@ArrayMethods.register('inverter')
def _arr_inverter(arr: list) -> list:
    arr.reverse()
    return arr

@ArrayMethods.register('vazio')
def _arr_vazio(arr: list) -> bool:
    return len(arr) == 0

@ArrayMethods.register('fatia')
def _arr_fatia(arr: list, inicio: int, fim: int = -1) -> list:
    if fim == -1 or fim is None:
        return arr[inicio:]
    return arr[inicio:fim]

@ArrayMethods.register('primeiro')
def _arr_primeiro(arr: list):
    if not arr:
        raise RuntimeError("primeiro() em array vazio.")
    return arr[0]

@ArrayMethods.register('ultimo')
def _arr_ultimo(arr: list):
    if not arr:
        raise RuntimeError("ultimo() em array vazio.")
    return arr[-1]

@ArrayMethods.register('indice')
def _arr_indice(arr: list, item) -> int:
    return arr.index(item)

@ArrayMethods.register('limpar')
def _arr_limpar(arr: list) -> None:
    arr.clear()
    return None

@ArrayMethods.register('copiar')
def _arr_copiar(arr: list) -> list:
    return list(arr)

@ArrayMethods.register('mapear')
def _arr_map(arr: list, func) -> list:
    return [func(x) for x in arr]

@ArrayMethods.register('filtrar')
def _arr_filtrar(arr: list, func) -> list:
    return [x for x in arr if func(x)]


# ============================================================
# 6. MATH MODULE
# ============================================================

class ModuloMath:
    """Simula o objeto 'Math' nativo."""

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
# 7. INTERPRETADOR (Tree-Walking)
# ============================================================

class GuruDevInterpreter:
    """
    Interpretador GuruDev — percorre a AST e executa as oracoes.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.tabela = TabelaDeSimbolos()
        self.escopo_atual: Ambiente = self.tabela.global_env
        self.output: List[str] = []
        self._stdout_original = None
        self._capturar_saida = False

        self._registrar_builtins()

    # --- Interface publica ---

    def interpretar(self, ast: Programa) -> Any:
        if self.debug:
            print(f"[DEBUG] Iniciando interpretacao — {len(ast.elementos)} elementos")

        resultado = None
        for elemento in ast.elementos:
            resultado = self._executar(elemento)
            if self.debug and resultado is not None:
                print(f"[DEBUG] Elemento executado: {type(elemento).__name__} -> {resultado!r}")

        if self.debug:
            print(f"\n[DEBUG] Tabela de Simbolos:\n{self.tabela.dump()}")

        return resultado

    def executar_codigo(self, source_code: str, debug: bool = False) -> Any:
        from .parser import parse
        ast = parse(source_code, debug=debug)
        if ast is None:
            raise RuntimeError("Falha no parsing — AST vazia.")
        self.debug = debug
        return self.interpretar(ast)

    def ambiente_atual(self) -> Ambiente:
        """Retorna o escopo atual (para REPL info)."""
        return self.escopo_atual

    # --- Registro de builtins ---

    def _registrar_builtins(self) -> None:
        for nome, func in Builtins.registro().items():
            self.escopo_atual.definir(
                nome=nome,
                tipo_simbolo=TipoSimbolo.BUILTIN,
                tipo_dado="builtin",
                valor=func,
                readonly=True,
            )

        self.escopo_atual.definir(
            nome="Math",
            tipo_simbolo=TipoSimbolo.VARIAVEL,
            tipo_dado="Object",
            valor=ModuloMath(),
        )

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
        novo = self.escopo_atual.criar_escopo(nome)
        self.escopo_atual = novo
        self.tabela.registrar(novo)
        if self.debug:
            print(f"[DEBUG] Entrando no escopo: {nome}")
        return novo

    def _sair_escopo(self) -> None:
        if self.escopo_atual.pai:
            if self.debug:
                print(f"[DEBUG] Saindo do escopo: {self.escopo_atual.nome}")
            self.escopo_atual = self.escopo_atual.pai

    # ============================================================
    # 8. EXECUCAO DE ORACOES (Statements)
    # ============================================================

    def _executar(self, no: Node) -> Any:
        if no is None:
            return None

        metodos = {
            Programa: self._exec_programa,
            Bloco: self._exec_bloco,
            DeclaracaoVariavel: self._exec_declaracao,
            DefinicaoFuncao: self._exec_funcao,
            DefinicaoClasse: self._exec_classe,
            Atribuicao: self._exec_atribuicao,
            PropAtribuicao: self._exec_prop_atribuicao,
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

        return self._avaliar(no)

    def _exec_programa(self, no: Programa) -> Any:
        resultado = None
        for elem in no.elementos:
            resultado = self._executar(elem)
        return resultado

    def _exec_bloco(self, no: Bloco) -> Any:
        if self.debug:
            if no.sobrescrita:
                s = no.sobrescrita
                print(f"[DEBUG] Bloco — nivel:{s.nivel} raiz:{s.raiz} clave:{s.clave} ont:{s.ontologia}")

        resultado = None

        if no.codigo:
            self._entrar_escopo(f"bloco@{no.lineno}")
            try:
                for oracao in no.codigo:
                    resultado = self._executar(oracao)
            finally:
                self._sair_escopo()

        if no.subescritas:
            for sub in no.subescritas:
                if self.debug:
                    print(f"[DEBUG] Subescrita registrada: {sub.linguagem} ({len(sub.conteudo)} chars)")

        return resultado

    # --- Declaracao de Variavel ---

    def _exec_declaracao(self, no: DeclaracaoVariavel) -> Any:
        valor = self._avaliar(no.valor) if no.valor else self._valor_padrao(no.tipo)
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

    # --- Definicao de Funcao ---

    def _exec_funcao(self, no: DefinicaoFuncao) -> Any:
        categoria = no.caso_gramatical if no.caso_gramatical else None

        self.escopo_atual.definir(
            nome=no.nome,
            tipo_simbolo=TipoSimbolo.FUNCAO,
            tipo_dado=no.tipo_retorno or "Void",
            categoria=categoria,
            valor=no,
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

    # --- Definicao de Classe ---

    def _exec_classe(self, no: DefinicaoClasse) -> Any:
        """Registra a classe no escopo atual como callable."""
        categoria = no.caso_gramatical if no.caso_gramatical else None

        classe_def = {
            'superclasse': no.superclasse,
            'interfaces': no.interfaces,
            'membros': no.membros,
            'ast': no,
        }

        # Store as a callable class descriptor
        self.escopo_atual.definir(
            nome=no.nome,
            tipo_simbolo=TipoSimbolo.CLASSE,
            tipo_dado=no.nome,
            categoria=categoria,
            valor=classe_def,
            modificador_acesso=no.modificador_acesso,
            lineno=no.lineno,
        )

        if self.debug:
            extends = f" extends {no.superclasse}" if no.superclasse else ""
            impl = f" implements {', '.join(no.interfaces)}" if no.interfaces else ""
            print(f"[DEBUG] Classe definida: {no.nome}{extends}{impl}")

        return None

    # --- Atribuicao ---

    def _exec_atribuicao(self, no: Atribuicao) -> Any:
        valor = self._avaliar(no.valor)
        try:
            self.escopo_atual.atribuir(no.alvo, valor)
        except (NameError, LookupError):
            # Auto-declarar se a variavel nao existe (comportamento REPL-friendly)
            self.escopo_atual.definir(
                nome=no.alvo,
                tipo_simbolo=TipoSimbolo.VARIAVEL,
                tipo_dado=Builtins.tipo_de(valor),
                valor=valor,
            )
        if self.debug:
            cat = f" [{no.caso_gramatical}]" if no.caso_gramatical else ""
            print(f"[DEBUG] Atribuicao: {no.alvo} = {valor!r}{cat}")
        return valor

    def _exec_prop_atribuicao(self, no: PropAtribuicao) -> Any:
        """Executa atribuicao a propriedade: obj.prop = valor."""
        valor = self._avaliar(no.valor)
        obj = self.escopo_atual.obter(no.objeto)
        if isinstance(obj, InstanciaClasse):
            obj.definir(no.propriedade, valor)
        else:
            raise RuntimeError(
                f"Nao e possivel atribuir propriedade em '{type(obj).__name__}'."
            )
        if self.debug:
            print(f"[DEBUG] PropAtribuicao: {no.objeto}.{no.propriedade} = {valor!r}")
        return valor

    # --- Retorno ---

    def _exec_retorno(self, no: Retorno) -> Any:
        valor = self._avaliar(no.valor) if no.valor else None
        raise RetornoSignal(valor)

    def _exec_break(self, no: Break) -> Any:
        raise BreakSignal()

    def _exec_continue(self, no: Continue) -> Any:
        raise ContinueSignal()

    # --- Controle de Fluxo ---

    def _exec_se(self, no: Se) -> Any:
        condicao = self._avaliar(no.condicao)
        if self._verdadeiro(condicao):
            return self._executar_bloco_oracoes(no.corpo_verdadeiro)
        elif no.corpo_falso:
            return self._executar_bloco_oracoes(no.corpo_falso)
        return None

    def _exec_para(self, no: Para) -> Any:
        self._entrar_escopo(f"para@{no.lineno}")
        try:
            if no.inicializacao:
                self._executar(no.inicializacao)

            while True:
                if no.condicao:
                    cond = self._avaliar(no.condicao)
                    if not self._verdadeiro(cond):
                        break

                try:
                    self._executar_bloco_oracoes(no.corpo)
                except BreakSignal:
                    break
                except ContinueSignal:
                    pass

                if no.incremento:
                    self._executar(no.incremento)
        finally:
            self._sair_escopo()
        return None

    def _exec_para_cada(self, no: ParaCada) -> Any:
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

    # --- Serie / Paralelo / Em ---

    def _exec_serie(self, no: ExecucaoSerie) -> Any:
        resultado = None
        for oracao in no.corpo:
            resultado = self._executar(oracao)
        return resultado

    def _exec_paralelo(self, no: ExecucaoParalelo) -> Any:
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
        resultados.sort(key=lambda x: x[0])
        return [r[1] for r in resultados]

    def _exec_em(self, no: ExecucaoEm) -> Any:
        linguagem = no.linguagem.lower()
        if not no.corpo:
            return None
        if linguagem == "python":
            return self._executar_bloco_oracoes(no.corpo)
        else:
            if self.debug:
                print(f"[DEBUG] em {no.linguagem}: execucao nativa disponivel apenas para python")
            return self._executar_bloco_oracoes(no.corpo)

    def _executar_bloco_oracoes(self, oracoes: List[Node]) -> Any:
        resultado = None
        for oracao in oracoes:
            resultado = self._executar(oracao)
        return resultado

    # ============================================================
    # 9. AVALIACAO DE PRODUCOES DE VALOR (Expressions)
    # ============================================================

    def _avaliar(self, no: Node) -> Any:
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
        valor = no.valor
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
        return [self._avaliar(elem) for elem in no.elementos]

    def _avaliar_identificador(self, no: Identificador) -> Any:
        return self.escopo_atual.obter(no.nome)

    def _avaliar_binaria(self, no: OperacaoBinaria) -> Any:
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
        valor = self._avaliar(no.operando)
        if no.operador == '-':
            return -valor
        elif no.operador == '!':
            return not self._verdadeiro(valor)
        else:
            raise RuntimeError(f"Operador unario desconhecido: '{no.operador}'")

    def _avaliar_chamada_funcao(self, no: ChamadaFuncao) -> Any:
        """Avalia chamada de funcao."""
        args = [self._avaliar(a) for a in no.argumentos]

        entrada = self.escopo_atual.resolver(no.nome)
        if entrada is None:
            raise NameError(f"Funcao '{no.nome}' nao definida.")

        valor = entrada.valor

        # Built-in
        if entrada.tipo_simbolo == TipoSimbolo.BUILTIN:
            if self.debug:
                print(f"[DEBUG] Chamada builtin: {no.nome}({args})")
            return valor(*args)

        # Funcao GuruDev (AST armazenada como valor)
        if entrada.tipo_simbolo == TipoSimbolo.FUNCAO and isinstance(valor, DefinicaoFuncao):
            return self._chamar_funcao_gurudev(valor, args)

        # Class instantiation: ClassName(args)
        if entrada.tipo_simbolo == TipoSimbolo.CLASSE and isinstance(valor, dict):
            return self._instanciar_classe(valor, args)

        # callable generico
        if callable(valor):
            return valor(*args)

        raise RuntimeError(f"'{no.nome}' nao e uma funcao (tipo: {entrada.tipo_simbolo.value}).")

    def _avaliar_chamada_metodo(self, no: ChamadaMetodo) -> Any:
        """Avalia chamada de metodo: objeto.metodo(args)."""
        # Handle literal objects (Literal or ArrayLiteral node)
        if isinstance(no.objeto, Literal):
            # String literal: "texto".metodo(args)
            obj = no.objeto.valor
            args = [self._avaliar(a) for a in no.argumentos]
            if isinstance(obj, str):
                return StringMethods.dispatch(obj, no.metodo, args)

        if isinstance(no.objeto, ArrayLiteral):
            # Array literal: [1,2,3].metodo(args)
            obj = self._avaliar(no.objeto)
            args = [self._avaliar(a) for a in no.argumentos]
            return ArrayMethods.dispatch(obj, no.metodo, args)

        # Normal case: resolve object from scope
        obj = self.escopo_atual.obter(no.objeto)
        args = [self._avaliar(a) for a in no.argumentos]

        # --- String methods ---
        if isinstance(obj, str):
            return StringMethods.dispatch(obj, no.metodo, args)

        # --- Array methods ---
        if isinstance(obj, list):
            return ArrayMethods.dispatch(obj, no.metodo, args)

        # --- InstanciaClasse methods ---
        if isinstance(obj, InstanciaClasse):
            metodo_ast = obj.obter_metodo(no.metodo)
            if metodo_ast is not None:
                return self._chamar_metodo_instancia(obj, metodo_ast, args)

        # --- Math / Console / generic objects ---
        metodo = getattr(obj, no.metodo, None)

        # Mapear nomes comuns para ModuloMath
        if metodo is None:
            nomes_alternativos = {
                'log': 'log', 'abs': 'abs_', 'sqrt': 'sqrt',
                'sin': 'sin', 'cos': 'cos', 'tan': 'tan',
                'floor': 'floor', 'ceil': 'ceil', 'round': 'round_',
                'pow': 'pow', 'append': 'append',
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
    # 10. CLASSES — INSTANCIACAO E METODOS
    # ============================================================

    def _instanciar_classe(self, classe_def: dict, args: list) -> InstanciaClasse:
        """
        Cria uma instancia de uma classe GuruDev.
        1. Cria o objeto InstanciaClasse
        2. Chama o metodo iniciar() se existir, passando os argumentos
        """
        nome_classe = classe_def['ast'].nome
        instancia = InstanciaClasse(nome_classe, classe_def)

        # Initialize default attribute values
        for membro in classe_def.get('membros', []):
            if isinstance(membro, DeclaracaoVariavel):
                if membro.valor is not None:
                    val = self._avaliar_no_contexto(membro.valor, instancia)
                    instancia.definir(membro.nome, val)
                else:
                    instancia.definir(membro.nome, self._valor_padrao(membro.tipo))

        # Call iniciar() constructor if exists
        metodo_iniciar = instancia.obter_metodo('iniciar')
        if metodo_iniciar is not None:
            self._chamar_metodo_instancia(instancia, metodo_iniciar, args)

        if self.debug:
            print(f"[DEBUG] Instancia criada: {nome_classe}")

        return instancia

    def _avaliar_no_contexto(self, no: Node, instancia: InstanciaClasse) -> Any:
        """Avalia um no de AST com a instancia como contexto (this/isto)."""
        self._entrar_escopo(f"init:{instancia._nome_classe}")
        try:
            self.escopo_atual.definir('this', TipoSimbolo.VARIAVEL, 'Object', valor=instancia)
            self.escopo_atual.definir('isto', TipoSimbolo.VARIAVEL, 'Object', valor=instancia)
            return self._avaliar(no)
        finally:
            self._sair_escopo()

    def _chamar_metodo_instancia(self, instancia: InstanciaClasse, metodo_ast: DefinicaoFuncao, args: list) -> Any:
        """
        Executa um metodo de uma instancia de classe.
        'this' e 'isto' sao disponibilizados no escopo do metodo.
        """
        self._entrar_escopo(f"metodo:{instancia._nome_classe}.{metodo_ast.nome}")

        try:
            # Bind this/isto
            self.escopo_atual.definir('this', TipoSimbolo.VARIAVEL, instancia._nome_classe, valor=instancia)
            self.escopo_atual.definir('isto', TipoSimbolo.VARIAVEL, instancia._nome_classe, valor=instancia)

            # Bind parameters
            for i, param in enumerate(metodo_ast.parametros):
                valor_arg = args[i] if i < len(args) else self._valor_padrao(param.tipo)
                valor_arg = self._coercion_tipo(valor_arg, param.tipo)
                self.escopo_atual.definir(
                    nome=param.nome,
                    tipo_simbolo=TipoSimbolo.PARAMETRO,
                    tipo_dado=param.tipo,
                    valor=valor_arg,
                )

            # Execute body
            resultado = None
            try:
                for oracao in metodo_ast.corpo:
                    resultado = self._executar(oracao)
            except RetornoSignal as s:
                resultado = s.valor

            return resultado

        finally:
            self._sair_escopo()

    # ============================================================
    # 11. CHAMADA DE FUNCAO GURUDEV
    # ============================================================

    def _chamar_funcao_gurudev(self, funcao_ast: DefinicaoFuncao, args: list) -> Any:
        self._entrar_escopo(f"funcao:{funcao_ast.nome}@{funcao_ast.lineno}")

        try:
            for i, param in enumerate(funcao_ast.parametros):
                valor_arg = args[i] if i < len(args) else self._valor_padrao(param.tipo)
                valor_arg = self._coercion_tipo(valor_arg, param.tipo)
                self.escopo_atual.definir(
                    nome=param.nome,
                    tipo_simbolo=TipoSimbolo.PARAMETRO,
                    tipo_dado=param.tipo,
                    valor=valor_arg,
                )

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
    # 12. HELPERS
    # ============================================================

    def _verdadeiro(self, valor) -> bool:
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
# 13. INTERFACE PUBLICA
# ============================================================

def interpretar(source_code: str, debug: bool = False) -> Any:
    from .parser import parse
    ast = parse(source_code, debug=debug)
    if ast is None:
        raise RuntimeError("Falha no parsing — AST vazia.")
    interpreter = GuruDevInterpreter(debug=debug)
    return interpreter.interpretar(ast)


def executar_arquivo(caminho: str, debug: bool = False) -> Any:
    with open(caminho, 'r', encoding='utf-8') as f:
        codigo = f.read()
    return interpretar(codigo, debug=debug)


# ============================================================
# 14. CLI
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
