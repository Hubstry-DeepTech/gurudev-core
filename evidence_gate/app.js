// Todo conteudo vindo do servidor e inserido com textContent (nunca HTML).
"use strict";
const $ = (id) => document.getElementById(id);
const INTERVALO_MS = 1500;
const MAX_ESPERA_MS = 15 * 60 * 1000;

function el(tag, classe, texto) {
  const e = document.createElement(tag);
  if (classe) e.className = classe;
  if (texto !== undefined && texto !== null) e.textContent = String(texto);
  return e;
}

function mostrar(r) {
  const alvo = $("resultado");
  alvo.replaceChildren();
  const v = ["VALIDADO_LITERAL", "REVISAO_SEMANTICA", "BLOQUEADO"].includes(r.veredito)
    ? r.veredito : "BLOQUEADO";
  const caixa = el("div", "veredito " + v, v);
  caixa.appendChild(el("span", "motivo", r.motivo || ""));
  alvo.appendChild(caixa);

  if (r.resposta) {
    const c = el("div", "cartao");
    c.appendChild(el("div", "rotulo", "Resposta do modelo"));
    c.appendChild(el("div", null, r.resposta));
    c.appendChild(el("div", "marca", r.resposta_literal
      ? "✔ resposta é trecho literal da fonte"
      : "≈ resposta não é trecho literal da fonte (síntese ou inferência do modelo)"));
    alvo.appendChild(c);
  }
  (r.afirmacoes || []).forEach((a, i) => {
    const c = el("div", "cartao");
    c.appendChild(el("div", "rotulo", "Afirmação " + (i + 1)));
    c.appendChild(el("div", null, a.texto));
    c.appendChild(el("div", "rotulo", "Citação"));
    c.appendChild(el("div", null, "“" + a.citacao + "”"));
    const marca = a.citacao_encontrada
      ? (a.literal ? "✔ citação encontrada; afirmação literal"
                   : "≈ citação encontrada; afirmação reescrita (paráfrase ou inferência)")
      : "✘ citação não encontrada na fonte";
    c.appendChild(el("div", "marca", marca));
    alvo.appendChild(c);
  });
  if (r.erro_modelo) alvo.appendChild(el("div", "cartao", "Erro do modelo: " + r.erro_modelo));

  const d = el("details");
  d.appendChild(el("summary", null, "Detalhes técnicos"));
  d.appendChild(el("pre", null, JSON.stringify({
    indicadores: r.indicadores, politica_ok: r.politica_ok,
    duracao_modelo: r.duracao_modelo, duracao_total: r.duracao_total,
    saida_bruta: r.saida_bruta,
  }, null, 2)));
  alvo.appendChild(d);
}

async function acompanhar(id) {
  const inicio = Date.now();
  while (Date.now() - inicio < MAX_ESPERA_MS) {
    await new Promise((ok) => setTimeout(ok, INTERVALO_MS));
    let t;
    try {
      const resp = await fetch("api/tarefa/" + encodeURIComponent(id), { cache: "no-store" });
      t = await resp.json();
      if (!resp.ok) throw new Error(t.erro || resp.status);
    } catch (e) {
      $("estado").textContent = "Falha ao consultar a tarefa: " + e.message;
      return;
    }
    $("estado").textContent = "Etapa: " + t.etapa + " · " + t.decorrido + " s";
    if (t.estado === "concluida" || t.estado === "falha") { mostrar(t.resultado); return; }
  }
  $("estado").textContent = "Tempo de espera esgotado na página. Tente de novo.";
}

$("enviar").addEventListener("click", async () => {
  const botao = $("enviar");
  botao.disabled = true;
  $("resultado").replaceChildren();
  $("estado").textContent = "Enviando…";
  try {
    const resp = await fetch("api/verificar", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fonte: $("fonte").value, pergunta: $("pergunta").value }),
    });
    const d = await resp.json();
    if (resp.status !== 202) { $("estado").textContent = "Erro: " + (d.erro || resp.status); return; }
    await acompanhar(d.id);
  } catch (e) {
    $("estado").textContent = "Erro de rede: " + e.message;
  } finally {
    botao.disabled = false;
  }
});
