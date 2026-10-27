# Triagem das falhas

Rodadas: `piloto`, `piloto2`. Assinaturas: 66. Famílias (causa provável comum): 12.

| Família | Assinaturas | Ocorrências | Estável | Classe preliminar |
|---|---|---|---|---|
| `CRASH_INTERP|SinalDeControle` | 3 | 10805 | sim | exceção Python vaza do interpretador (deveria ser GuruDevError) |
| `CRASH_INTERP|Nativas` | 42 | 3694 | sim | exceção Python vaza do interpretador (deveria ser GuruDevError) |
| `CRASH_PARSER|TypeError|p_prop_atribuicao_caso` | 1 | 2879 | sim | exceção Python vaza do parser (deveria ser erro sintático) |
| `CRASH_PARSER|IndexError|p_if_elif_statement` | 1 | 1573 | sim | exceção Python vaza do parser (deveria ser erro sintático) |
| `CRASH_INTERP|TypeError|_x_OperacaoBinaria` | 9 | 1341 | sim | exceção Python vaza do interpretador (deveria ser GuruDevError) |
| `CRASH_INTERP|TypeError|_x_OperacaoUnaria` | 1 | 243 | sim | exceção Python vaza do interpretador (deveria ser GuruDevError) |
| `CRASH_PARSER|AttributeError|visitar` | 1 | 236 | sim | exceção Python vaza do parser (deveria ser erro sintático) |
| `CRASH_INTERP|TypeError|_x_ChamadaMetodo` | 1 | 54 | sim | exceção Python vaza do interpretador (deveria ser GuruDevError) |
| `RECURSAO|RecursionError|get_func` | 1 | 15 | sim | RecursionError do Python vaza (a linguagem não limita recursão) |
| `CRASH_INTERP|ZeroDivisionError|_x_OperacaoBinaria` | 2 | 13 | sim | exceção Python vaza do interpretador (deveria ser GuruDevError) |
| `ESPERADO|laco-do-programa` | 3 | 4 | sim | laço infinito do próprio programa (esperado) |
| `MEMORIA||?` | 1 | 2 | sim | consumo de memória sem limite |

## `CRASH_INTERP|Nativas`

- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:390 _x_ChamadaFuncao` — 1749 ocorrências, 11 → 8 bytes, caso `casos/CRASH_INTERP_Nativas__1.guru`
  - mensagem: `math.sin() takes exactly one argument (0 given)`

```
seno();
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:119 raiz` — 62 ocorrências, 19 → 20 bytes, caso `casos/CRASH_INTERP_Nativas__2.guru`
  - mensagem: `unsupported operand type(s) for ** or pow(): 'str' and 'float'`

```
escrever(raiz(""));
```
- assinatura `CRASH_INTERP|ZeroDivisionError|src/nativas.py:119 raiz` — 4 ocorrências, 23 → 21 bytes, caso `casos/CRASH_INTERP_Nativas__3.guru`
  - mensagem: `float division by zero`

```
escrever(raiz(1,0));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:109 de_json` — 52 ocorrências, 22 → 22 bytes, caso `casos/CRASH_INTERP_Nativas__4.guru`
  - mensagem: `the JSON object must be str, bytes or bytearray, not int`

```
escrever(de_json(1));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:79 tamanho` — 42 ocorrências, 21 → 22 bytes, caso `casos/CRASH_INTERP_Nativas__5.guru`
  - mensagem: `tipo_de(Int) nao suporta tamanho().`

```
escrever(tamanho(2));
```
- assinatura `CRASH_INTERP|ValueError|src/interpreter.py:390 _x_ChamadaFuncao` — 20 ocorrências, 22 → 22 bytes, caso `casos/CRASH_INTERP_Nativas__6.guru`
  - mensagem: `min() iterable argument is empty`

```
escrever(minimo(""));
```
- assinatura `CRASH_INTERP|JSONDecodeError|src/nativas.py:109 de_json` — 17 ocorrências, 23 → 23 bytes, caso `casos/CRASH_INTERP_Nativas__7.guru`
  - mensagem: `Expecting value: line 1 column 1 (char 0)`

```
escrever(de_json(""));
```
- assinatura `CRASH_INTERP|RuntimeError|src/nativas.py:370 _arr_pop` — 9 ocorrências, 29 → 24 bytes, caso `casos/CRASH_INTERP_Nativas__8.guru`
  - mensagem: `pop() em array vazio.`

```
v=[];escrever(v.pop());
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:123 absoluto` — 16 ocorrências, 24 → 24 bytes, caso `casos/CRASH_INTERP_Nativas__9.guru`
  - mensagem: `bad operand type for abs(): 'str'`

```
escrever(absoluto(""));
```
- assinatura `CRASH_INTERP|ValueError|src/nativas.py:115 randint` — 6 ocorrências, 25 → 24 bytes, caso `casos/CRASH_INTERP_Nativas__10.guru`
  - mensagem: `empty range in randrange(1, 1)`

```
escrever(randint(1,0));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:115 randint` — 49 ocorrências, 26 → 25 bytes, caso `casos/CRASH_INTERP_Nativas__11.guru`
  - mensagem: `'list' object cannot be interpreted as an integer`

```
escrever(randint([],2));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:323 dispatch` — 733 ocorrências, 35 → 25 bytes, caso `casos/CRASH_INTERP_Nativas__12.guru`
  - mensagem: `_arr_push() missing 1 required positional argument: 'item'`

```
v=[];escrever(v.push());
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:127 arredondar` — 51 ocorrências, 26 → 26 bytes, caso `casos/CRASH_INTERP_Nativas__13.guru`
  - mensagem: `type list doesn't define __round__ method`

```
escrever(arredondar([]));
```
- assinatura `CRASH_INTERP|ZeroDivisionError|src/interpreter.py:390 _x_ChamadaFuncao` — 3 ocorrências, 27 → 26 bytes, caso `casos/CRASH_INTERP_Nativas__14.guru`
  - mensagem: `float division by zero`

```
escrever(logaritmo(2,1));
```
- assinatura `CRASH_INTERP|RuntimeError|src/nativas.py:431 _arr_ultimo` — 11 ocorrências, 36 → 27 bytes, caso `casos/CRASH_INTERP_Nativas__15.guru`
  - mensagem: `ultimo() em array vazio.`

```
v=[];escrever(v.ultimo());
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:198 dispatch` — 307 ocorrências, 37 → 27 bytes, caso `casos/CRASH_INTERP_Nativas__16.guru`
  - mensagem: `_str_indice() missing 1 required positional argument: 'sub'`

```
v="";escrever(v.indice());
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:262 _str_indice` — 15 ocorrências, 38 → 28 bytes, caso `casos/CRASH_INTERP_Nativas__17.guru`
  - mensagem: `find() argument 1 must be str, not int`

```
v="";escrever(v.indice(2));
```
- assinatura `CRASH_INTERP|ValueError|src/nativas.py:437 _arr_indice` — 37 ocorrências, 38 → 28 bytes, caso `casos/CRASH_INTERP_Nativas__18.guru`
  - mensagem: `0 is not in list`

```
v=[];escrever(v.indice(0));
```
- assinatura `CRASH_INTERP|RuntimeError|src/nativas.py:424 _arr_primeiro` — 11 ocorrências, 39 → 29 bytes, caso `casos/CRASH_INTERP_Nativas__19.guru`
  - mensagem: `primeiro() em array vazio.`

```
v=[];escrever(v.primeiro());
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:235 _str_dividir` — 4 ocorrências, 39 → 29 bytes, caso `casos/CRASH_INTERP_Nativas__20.guru`
  - mensagem: `must be str or None, not int`

```
v="";escrever(v.dividir(1));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:83 converter_int` — 7 ocorrências, 29 → 29 bytes, caso `casos/CRASH_INTERP_Nativas__21.guru`
  - mensagem: `int() argument must be a string, a bytes-like object or a real number, not 'list'`

```
escrever(converter_int([]));
```
- assinatura `CRASH_INTERP|ValueError|src/nativas.py:83 converter_int` — 22 ocorrências, 29 → 29 bytes, caso `casos/CRASH_INTERP_Nativas__22.guru`
  - mensagem: `invalid literal for int() with base 10: ''`

```
escrever(converter_int(""));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:252 _str_contem` — 17 ocorrências, 40 → 30 bytes, caso `casos/CRASH_INTERP_Nativas__23.guru`
  - mensagem: `'in <string>' requires string as left operand, not float`

```
v="";escrever(v.contem(0.0));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:267 _str_repetir` — 3 ocorrências, 40 → 30 bytes, caso `casos/CRASH_INTERP_Nativas__24.guru`
  - mensagem: `can't multiply sequence by non-int of type 'str'`

```
v="";escrever(v.repetir(""));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:418 _arr_fatia` — 33 ocorrências, 48 → 30 bytes, caso `casos/CRASH_INTERP_Nativas__25.guru`
  - mensagem: `slice indices must be integers or None or have an __index__ method`

```
v=[];escrever(v.fatia(0,[]));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:458 _arr_filtrar` — 9 ocorrências, 46 → 30 bytes, caso `casos/CRASH_INTERP_Nativas__26.guru`
  - mensagem: `'int' object is not callable`

```
v=[2];escrever(v.filtrar(0));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:453 _arr_map` — 50 ocorrências, 43 → 31 bytes, caso `casos/CRASH_INTERP_Nativas__27.guru`
  - mensagem: `'int' object is not callable`

```
v=[0.0];escrever(v.mapear(0));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:87 converter_float` — 10 ocorrências, 31 → 31 bytes, caso `casos/CRASH_INTERP_Nativas__28.guru`
  - mensagem: `float() argument must be a string or a real number, not 'list'`

```
escrever(converter_float([]));
```
- assinatura `CRASH_INTERP|ValueError|src/nativas.py:87 converter_float` — 17 ocorrências, 31 → 31 bytes, caso `casos/CRASH_INTERP_Nativas__29.guru`
  - mensagem: `could not convert string to float: ''`

```
escrever(converter_float(""));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:296 _str_startswith` — 29 ocorrências, 42 → 32 bytes, caso `casos/CRASH_INTERP_Nativas__30.guru`
  - mensagem: `startswith first arg must be str or a tuple of str, not int`

```
v="";escrever(v.comeca_com(1));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:241 _str_substring` — 15 ocorrências, 43 → 33 bytes, caso `casos/CRASH_INTERP_Nativas__31.guru`
  - mensagem: `slice indices must be integers or None or have an __index__ method`

```
v="";escrever(v.substring(3.5));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:301 _str_endswith` — 12 ocorrências, 44 → 33 bytes, caso `casos/CRASH_INTERP_Nativas__32.guru`
  - mensagem: `endswith first arg must be str or a tuple of str, not int`

```
v="";escrever(v.termina_com(1));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:381 _arr_ordenar` — 167 ocorrências, 49 → 33 bytes, caso `casos/CRASH_INTERP_Nativas__33.guru`
  - mensagem: `'<' not supported between instances of 'str' and 'int'`

```
v=[1,"x"];escrever(v.ordenar());
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:417 _arr_fatia` — 33 ocorrências, 44 → 34 bytes, caso `casos/CRASH_INTERP_Nativas__34.guru`
  - mensagem: `slice indices must be integers or None or have an __index__ method`

```
v=[];escrever(v.fatia("\u0000"));
```
- assinatura `CRASH_INTERP|RuntimeError|src/nativas.py:363 _arr_remover_ultimo` — 8 ocorrências, 44 → 35 bytes, caso `casos/CRASH_INTERP_Nativas__35.guru`
  - mensagem: `remover_ultimo() em array vazio.`

```
v=[];escrever(v.remover_ultimo());
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:257 _str_substituir` — 28 ocorrências, 46 → 35 bytes, caso `casos/CRASH_INTERP_Nativas__36.guru`
  - mensagem: `replace() argument 1 must be str, not int`

```
v="";escrever(v.substituir(2,""));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:306 _str_rfind` — 21 ocorrências, 46 → 36 bytes, caso `casos/CRASH_INTERP_Nativas__37.guru`
  - mensagem: `rfind() argument 1 must be str, not list`

```
v="";escrever(v.ultimo_indice([]));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:399 _arr_inserir` — 5 ocorrências, 49 → 37 bytes, caso `casos/CRASH_INTERP_Nativas__38.guru`
  - mensagem: `'str' object cannot be interpreted as an integer`

```
v=[];escrever(v.inserir("a,b,c",1));
```
- assinatura `CRASH_INTERP|OverflowError|src/interpreter.py:390 _x_ChamadaFuncao` — 3 ocorrências, 44 → 43 bytes, caso `casos/CRASH_INTERP_Nativas__39.guru`
  - mensagem: `math range error`

```
escrever(potencia(2,9223372036854775808));
```
- assinatura `CRASH_INTERP|TypeError|src/nativas.py:242 _str_substring` — 5 ocorrências, 57 → 46 bytes, caso `casos/CRASH_INTERP_Nativas__40.guru`
  - mensagem: `slice indices must be integers or None or have an __index__ method`

```
v="";escrever(v.substring(2147483648,"abc"));
```
- assinatura `CRASH_INTERP|OverflowError|src/nativas.py:267 _str_repetir` — 1 ocorrências, 57 → 47 bytes, caso `casos/CRASH_INTERP_Nativas__41.guru`
  - mensagem: `cannot fit 'int' into an index-sized integer`

```
v="";escrever(v.repetir(9223372036854775808));
```
- assinatura `CRASH_INTERP|OverflowError|src/nativas.py:399 _arr_inserir` — 1 ocorrências, 76 → 58 bytes, caso `casos/CRASH_INTERP_Nativas__42.guru`
  - mensagem: `Python int too large to convert to C ssize_t`

```
v=["b","c"];escrever(v.inserir(9223372036854775808,0.0));
```

## `CRASH_INTERP|SinalDeControle`

- assinatura `CRASH_INTERP|BreakSignal|src/interpreter.py:584 _x_Break` — 2642 ocorrências, 8 → 7 bytes, caso `casos/CRASH_INTERP_SinalDeControle__1.guru`
  - mensagem: ``

```
break;
```
- assinatura `CRASH_INTERP|ReturnSignal|src/interpreter.py:536 _x_Retorno` — 4298 ocorrências, 9 → 8 bytes, caso `casos/CRASH_INTERP_SinalDeControle__2.guru`
  - mensagem: `None`

```
return;
```
- assinatura `CRASH_INTERP|ContinueSignal|src/interpreter.py:587 _x_Continue` — 3865 ocorrências, 11 → 10 bytes, caso `casos/CRASH_INTERP_SinalDeControle__3.guru`
  - mensagem: ``

```
continua;
```

## `CRASH_INTERP|TypeError|_x_ChamadaMetodo`

- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:528 _x_ChamadaMetodo` — 54 ocorrências, 29 → 18 bytes, caso `casos/CRASH_INTERP_TypeError__x_ChamadaMetodo__1.guru`
  - mensagem: `count expected at least 1 argument, got 0`

```
return"".count();
```

## `CRASH_INTERP|TypeError|_x_OperacaoBinaria`

- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:687 _x_OperacaoBinaria` — 209 ocorrências, 18 → 15 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__1.guru`
  - mensagem: `unsupported operand type(s) for /: 'int' and 'str'`

```
return 3/": ";
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:691 _x_OperacaoBinaria` — 234 ocorrências, 21 → 16 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__2.guru`
  - mensagem: `'<' not supported between instances of 'int' and 'NoneType'`

```
return 2<"A".c;
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:692 _x_OperacaoBinaria` — 97 ocorrências, 31 → 21 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__3.guru`
  - mensagem: `'>' not supported between instances of 'float' and 'list'`

```
enquanto((7.0)>[]){}
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:685 _x_OperacaoBinaria` — 78 ocorrências, 30 → 24 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__4.guru`
  - mensagem: `unsupported operand type(s) for -: 'str' and 'NoneType'`

```
return"A"-"Acme".dobro;
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:694 _x_OperacaoBinaria` — 66 ocorrências, 28 → 24 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__5.guru`
  - mensagem: `'>=' not supported between instances of 'str' and 'float'`

```
return", tenho ">=10.0;
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:693 _x_OperacaoBinaria` — 168 ocorrências, 33 → 26 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__6.guru`
  - mensagem: `'<=' not supported between instances of 'float' and 'str'`

```
while(10.0<=", tenho "){}
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:684 _x_OperacaoBinaria` — 99 ocorrências, 44 → 29 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__7.guru`
  - mensagem: `unsupported operand type(s) for +: 'NoneType' and 'bool'`

```
b="3 * 7 =".Calc+verdadeiro;
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:688 _x_OperacaoBinaria` — 213 ocorrências, 41 → 32 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__8.guru`
  - mensagem: `not all arguments converted during string formatting`

```
enquanto(20.0=="Area: "%true){}
```
- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:686 _x_OperacaoBinaria` — 177 ocorrências, 66 → 35 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoBinaria__9.guru`
  - mensagem: `unsupported operand type(s) for *: 'bool' and 'NoneType'`

```
return verdadeiro*" Email: ".trim;
```

## `CRASH_INTERP|TypeError|_x_OperacaoUnaria`

- assinatura `CRASH_INTERP|TypeError|src/interpreter.py:702 _x_OperacaoUnaria` — 243 ocorrências, 15 → 11 bytes, caso `casos/CRASH_INTERP_TypeError__x_OperacaoUnaria__1.guru`
  - mensagem: `bad operand type for unary -: 'str'`

```
push=-"-";
```

## `CRASH_INTERP|ZeroDivisionError|_x_OperacaoBinaria`

- assinatura `CRASH_INTERP|ZeroDivisionError|src/interpreter.py:688 _x_OperacaoBinaria` — 6 ocorrências, 27 → 20 bytes, caso `casos/CRASH_INTERP_ZeroDivisionError__x_OperacaoBinaria__1.guru`
  - mensagem: `float modulo by zero`

```
enquanto(3.0%0.0){}
```
- assinatura `CRASH_INTERP|ZeroDivisionError|src/interpreter.py:687 _x_OperacaoBinaria` — 7 ocorrências, 133 → 66 bytes, caso `casos/CRASH_INTERP_ZeroDivisionError__x_OperacaoBinaria__2.guru`
  - mensagem: `division by zero`

```
dividir=verdadeiro/(0);[bloco]¡codigo!paralelo{}!/codigo![/bloco]
```

## `CRASH_PARSER|AttributeError|visitar`

- assinatura `CRASH_PARSER|AttributeError|src/parser.py:80 visitar` — 236 ocorrências, 79 → 69 bytes, caso `casos/CRASH_PARSER_AttributeError_visitar__1.guru`
  - mensagem: `'str' object has no attribute 'gm_tempo' and no __dict__ for setting new attributes`

```
$$bloco$$¡codigo!classe criar_pessoa implements a{}!/codigo![/bloco]
```

## `CRASH_PARSER|IndexError|p_if_elif_statement`

- assinatura `CRASH_PARSER|IndexError|src/parser.py:813 p_if_elif_statement` — 1573 ocorrências, 36 → 25 bytes, caso `casos/CRASH_PARSER_IndexError_p_if_elif_statement__1.guru`
  - mensagem: `list index out of range`

```
if(7.0){}senao_se(abs){}
```

## `CRASH_PARSER|TypeError|p_prop_atribuicao_caso`

- assinatura `CRASH_PARSER|TypeError|src/parser.py:922 p_prop_atribuicao_caso` — 2879 ocorrências, 25 → 12 bytes, caso `casos/CRASH_PARSER_TypeError_p_prop_atribuicao_caso__1.guru`
  - mensagem: `PropAtribuicao.__init__() got an unexpected keyword argument 'caso_gramatical'`

```
ACU.x.x=20;
```

## `ESPERADO|laco-do-programa`

- assinatura `TIMEOUT|src/interpreter.py:149 _e` — 2 ocorrências, 521 → None bytes, caso `casos/ESPERADO_laco_do_programa__1.guru`
  - mensagem: ``

```
[bloco]
[sobrescrita] $$nivel="linguistico"$$ $$paradigma="vqe"$$ $$nivel="historico"$$ $$paradigma="logico"$$ $$nivel="moral"$$ $$paradigma="hibrido"$$ $$/sobrescrita$$
¡codigo!
enquanto ( 15.0 != "50 - 15 =" . dividir == true ) {
continua ;
}
!/codigo!
[subescritas]
¿sql? 
        # Subescrita Python equivalente
        def somar(a, b):
            return a + b

        def fatorial(n):
            if n <= 1:
                return 1
            return n * fatorial(n - 1)
         ?/sql? $$/subescritas$$
[/bloco]
```
- assinatura `TIMEOUT|src/interpreter.py:58 get` — 1 ocorrências, 1889 → None bytes, caso `casos/ESPERADO_laco_do_programa__2.guru`
  - mensagem: ``

```
// Quantum GuruDev Demo - Pipeline end-to-end
// Run: gurudev run examples/quantum_demo.guru

[bloco]
    [sobrescrita]
        "Contexto: demonstracao completa do Interpreter GuruDev"
        [nivel="ontologico"]
        [raiz="QUANTUM"]
        [clave="ciencia"]
        [ont="relacao"]
    [/sobrescrita]

¡codigo!
        // === 1. Variaveis ===
        String nome = "GuruDev";
        Int versao = 1;
        Float pi = 3.14159;
        Bool ativo = verdadeiro;

        escrever("=== GuruDev Interpreter ===");
        escrever("Nome:", nome);
        escrever("Versao:", versao);
        escr
```
- assinatura `TIMEOUT|src/interpreter.py:677 _x_OperacaoBinaria` — 1 ocorrências, 184 → None bytes, caso `casos/ESPERADO_laco_do_programa__3.guru`
  - mensagem: ``

```
[bloco]
¡codigo!
!/codigo!
$$subescritas$$
¿wasm? 
print("python executado")
 ?/wasm? $$/subescritas$$
[/bloco]
serie {
while ( "  GuruDev  " >= " anos." <= true || verdadeiro ) {
}
}
```

## `MEMORIA||?`

- assinatura `MEMORIA|` — 2 ocorrências, 97 → 53 bytes, caso `casos/MEMORIA__1.guru`
  - mensagem: ``

```
if("ção🙂"*2147483648){}senao_se(E){}senao_se(true){}
```

## `RECURSAO|RecursionError|get_func`

- assinatura `RECURSAO|RecursionError|src/interpreter.py:81 get_func` — 15 ocorrências, 1182 → 128 bytes, caso `casos/RECURSAO_RecursionError_get_func__1.guru`
  - mensagem: `maximum recursion depth exceeded`

```
funcao fatorial(Int n)->Int{se(n){}return n*fatorial();}escrever("5! = " + fatorial(5)); funcao enviar_mensagem(String msg) {
}
```
