# S1 — Fronteira com o Python: revisão e regressão combinada (PR #25 + PR #24)

Registro pedido na revisão do PR #25. Data: 27/10/2026. Ambiente: Python 3.13.17,
PLY 3.11, pytest 9.1.1, Linux x86_64.

## Commits

| Papel | Commit |
|---|---|
| `main` (base) | `2d1bb1d5a5a5c8104e770a91a32931dd7d57c40a` |
| PR #24 (fuzzing e testes; não altera `src/`) | `600a9971413ecad2a69bbe68978db68d9005b01b` |
| PR #25 (esta correção) | `6142f9b46755779d4d076dfdc8e005c9494adfbc` |
| Integração local #25 + #24 (não publicada) | `5dc821e25d3d130e8fbb4acade3dbe50e27da0bb` |

## Ponto 1 — Compatibilidade semântica

A primeira versão do PR transformava "propriedade inexistente" de `None` em
`GuruDevError`. Isso mudava 3 programas de conformidade e 4 casos de F5. A
mudança foi **retirada deste PR**. A regra agora é:

| Situação | Antes (`main`) | Agora |
|---|---|---|
| Propriedade que a linguagem não conhece (`"abc".c`, `a.juntar`) | `None` | `None` (igual) |
| Propriedade que só o Python conhece (`n.real`, `s.upper`) | valor do Python | `None` (o Python não é consultado) |
| Nome iniciado por `_` (`s.__class__`, `c.__metodos__`) | valor do Python | `GuruDevError` |
| Método que só o Python conhece (`"aba".count("a")`, `a.append(2)`) | executa o método do Python | `GuruDevError` ("método não encontrado") |
| Métodos da linguagem, instâncias, dicionários | funcionam | funcionam (igual) |

As três primeiras linhas de mudança são a própria mitigação. Trocar `None` por
erro em propriedade desconhecida fica para uma decisão separada.

Testes de compatibilidade: `test_propriedade_desconhecida_continua_none`
(os 3 padrões dos programas de conformidade), além dos testes de texto, lista,
instância e dicionário.

## Ponto 2 — Fronteira de objetos

Antes, o fallback `getattr` valia para qualquer tipo que não fosse básico, ou
seja, uma lista de negação. Agora vale só para tipos de uma **allowlist
explícita**, `Interpreter.tipos_interop`, **vazia por padrão**. Quem embute o
interpretador e precisa expor um tipo Python inclui o tipo nessa lista, e
mesmo assim os nomes iniciados por `_` continuam recusados.

Medição que sustenta a allowlist vazia: instrumentei os dois ramos (propriedade
e método) no código de `main` e rodei a suíte, os 10 exemplos e os 369 programas
dos corpora do fuzzing. **Nenhum objeto fora dos tipos básicos (texto, números,
listas) chegou ao fallback.** Hoje, portanto, nada legítimo depende dele.

Efeito colateral documentado: objetos Python criados dentro de uma subescrita
deixam de ter métodos acessíveis pelo código GuruDev, salvo se o tipo for
incluído na allowlist. Nenhum teste, exemplo ou programa do corpus usa isso.

Continua valendo: **isto não é um sandbox.** Código de terceiros deve rodar com
isolamento do sistema operacional.

Testes: `test_objeto_fora_da_allowlist_*` (negativos),
`test_allowlist_libera_metodos_e_propriedades_publicos` (positivo) e
`test_allowlist_nao_libera_nomes_internos`.

## Ponto 3 — Regressão combinada

### Suítes

| Base | Resultado |
|---|---|
| `main` + #24 (`600a997`) | 518 aprovados, 65 xfail, 0 falhas |
| `main` + #25 (`6142f9b`) | 486 aprovados, 2 xfail, 0 falhas |
| Integração #25 + #24 (`5dc821e`) | 546 aprovados, 64 xfail, **1 falha** |

A falha única é `XPASS(strict)` do caso F8, `return"".count();`: a correção
resolveu o bug que o teste documentava. É o comportamento esperado do xfail
rígido.

Testes de segurança de #25 contra o interpretador de `main`: os 20 de segurança
falham, o que confirma a exposição, e os 8 de compatibilidade e de
comportamento legítimo passam. Com a correção, os 28 passam.

### Diferencial programa a programa

Cada programa conhecido rodou nas duas bases (`main`+#24 e integração), no
executor isolado do #24, comparando status, exceção e saída. Toda diferença foi
reconfirmada mais 2 vezes.

Programas: 565, sendo 10 exemplos, 63 casos de regressão, 60 de conformidade,
369 dos corpora, 66 programas de falha dos pilotos e 115 sementes (com
duplicatas removidas por hash).

**Diferenças: 3, todas estáveis, todas da família F8:**

| Programa | `main` + #24 | Integração |
|---|---|---|
| `casos/CRASH_INTERP_TypeError__x_ChamadaMetodo__1.guru` — `return"".count();` | `CRASH_INTERP` TypeError | `ERRO_GURU` |
| `corpus/5cc7c274c5b6a482.guru` — `"...".count(true)` | `CRASH_INTERP` TypeError | `ERRO_GURU` |
| falha do piloto `..._x_ChamadaMetodo-8dc56312` — `"".count(true)` | `CRASH_INTERP` TypeError | `ERRO_GURU` |

Nenhum programa passou de `OK` para erro. Nenhuma saída de conformidade mudou.

### Reclassificação

| Item | Antes da revisão | Agora |
|---|---|---|
| F8 (1 caso) | XPASS | XPASS. **Corrigido por #25.** Ao integrar, remover F8 do bloco xfail do #24. |
| F5 (4 casos) | XPASS (efeito do `None`→erro) | Continuam xfail. O bug de F5 permanece e os testes seguem documentando-o. |
| Conformidade (3 programas) | saída mudava | Saída idêntica |

Nenhum teste do #24 foi alterado para acomodar esta mudança.

Observação cosmética, fora do escopo: a mensagem "método não encontrado"
imprime a representação interna do nó (`Literal(...)`) quando o objeto é uma
expressão. A mensagem já era assim em `main`.

## Como reproduzir

```bash
git fetch origin main testes/fuzzing-piloto seguranca/restringir-atributos-python
git worktree add ../base-24 origin/testes/fuzzing-piloto
git worktree add ../integracao origin/seguranca/restringir-atributos-python
git -C ../integracao merge --no-edit origin/testes/fuzzing-piloto
(cd ../base-24 && python3 -m pytest -q)
(cd ../integracao && python3 -m pytest -q -rX)
python3 -I diferencial.py ../base-24 ../integracao diferencial.json \
  "../base-24/examples/*.guru" "../base-24/tests/fuzz_regressoes/casos/*.guru" \
  "../base-24/tests/fuzz_regressoes/conformidade/*.guru" \
  "resultados/piloto/corpus/*.guru" "resultados/piloto2/corpus/*.guru" \
  "resultados/piloto/falhas/*/programa.guru" "resultados/piloto2/falhas/*/programa.guru"
```

`diferencial.py` usa o executor e as sementes do #24:

```python
"""Compara, programa a programa, o resultado em duas bases (status, exceção, saída)."""
import glob, hashlib, json, os, sys
BASE_A, BASE_B, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(BASE_A, "fuzz"))
from executor import Executor
from sementes import coletar
progs = {}
def add(origem, txt):
    progs.setdefault(hashlib.sha256(txt.encode()).hexdigest()[:16], (origem, txt))
for pad in sys.argv[4:]:
    for f in sorted(glob.glob(pad)):
        add(f.replace(os.path.dirname(os.path.dirname(f)) + "/", ""), open(f, encoding="utf-8").read())
for s in coletar(BASE_A)[0]:
    add("semente:" + s["origem"], s["codigo"])
def chave(r):
    return (r.get("status"), r.get("exc"), r.get("saida"))
res = {}
for nome, base in (("A", BASE_A), ("B", BASE_B)):
    with Executor(base, timeout=3) as ex:
        res[nome] = {h: ex.rodar(t) for h, (o, t) in progs.items()}
difs = []
with Executor(BASE_A, timeout=3) as exa, Executor(BASE_B, timeout=3) as exb:
    for h, (o, t) in progs.items():
        a, b = res["A"][h], res["B"][h]
        if chave(a) == chave(b):
            continue
        estavel = all(chave(exa.rodar(t)) == chave(a) and chave(exb.rodar(t)) == chave(b) for _ in range(2))
        difs.append({"id": h, "origem": o, "estavel": estavel, "programa": t[:400],
                     "A": {k: a.get(k) for k in ("status", "exc", "msg", "local", "saida")},
                     "B": {k: b.get(k) for k in ("status", "exc", "msg", "local", "saida")}})
json.dump({"base_A": BASE_A, "base_B": BASE_B, "programas": len(progs), "diferencas": difs},
          open(SAIDA, "w"), indent=2, ensure_ascii=False)
print("programas:", len(progs), "| diferencas:", len(difs), "| estaveis:", sum(d["estavel"] for d in difs))
```
