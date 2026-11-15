/* =========================================================================
   BULÁRIO FARMACÊUTICO — FarmaPrática
   Lógica de navegação, busca, favoritos, histórico e renderização.
   Depende de data.js (GRUPOS, MEDICAMENTOS, NAO_DISPONIVEL) já carregado.
   ========================================================================= */

(function () {
  "use strict";

  /* ---------------------------------------------------------------------
     Utilitários
  --------------------------------------------------------------------- */
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $all = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  function normalize(str) {
    if (!str) return "";
    return str
      .toString()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .toLowerCase()
      .trim();
  }

  function esc(str) {
    if (str === undefined || str === null) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function debounce(fn, ms) {
    let t;
    return function (...args) {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), ms);
    };
  }

  /* ---------------------------------------------------------------------
     Mapa medId -> cor do grupo farmacologico (GRUPOS[].cor), usado para
     colorir a borda esquerda dos cards de medicamento e dos cabecalhos de
     subclasse, facilitando a identificacao visual rapida por categoria
     (Rodada 36 - pedido do usuario para deixar os botoes "bem faceis de
     visualizar", mantendo o toque de cor sutil da Rodada 35).
  --------------------------------------------------------------------- */
  const MED_GRUPO_COR = {};
  (typeof GRUPOS !== "undefined" ? GRUPOS : []).forEach((g) => {
    (g.subclasses || []).forEach((s) => {
      (s.medicamentos || []).forEach((medId) => {
        if (!(medId in MED_GRUPO_COR)) MED_GRUPO_COR[medId] = g.cor;
      });
    });
  });

  /* ---------------------------------------------------------------------
     Armazenamento local (favoritos / histórico)
  --------------------------------------------------------------------- */
  const LS_FAV = "fp-bulario-favoritos";
  const LS_HIST = "fp-bulario-recentes";
  const HIST_MAX = 10;

  function getFavoritos() {
    try {
      return JSON.parse(localStorage.getItem(LS_FAV) || "[]");
    } catch (e) {
      return [];
    }
  }
  function setFavoritos(arr) {
    try {
      localStorage.setItem(LS_FAV, JSON.stringify(arr));
    } catch (e) {
      /* localStorage indisponível — segue sem persistir */
    }
  }
  function isFavorito(id) {
    return getFavoritos().includes(id);
  }

  // Sincroniza com o painel de Favoritos da página inicial do FarmaPrática
  // (- INDEX/index.html), que lê a chave compartilhada "fp_favoritos_hub"
  // do localStorage (mesma origem) — mesmo padrão usado por medinter,
  // farmadesk, dosespediatricas e consultacontrolados.
  function syncFavoritoNoHub(id, label, adicionado) {
    try {
      const HUB_KEY = "fp_favoritos_hub";
      const raw = localStorage.getItem(HUB_KEY);
      let list = raw ? JSON.parse(raw) : [];
      const hubId = "bulario-" + id;
      if (adicionado) {
        if (!list.some((f) => f.id === hubId)) {
          list.push({
            id: hubId,
            label: label,
            source: "bulario",
            sourceLabel: "Bulário Farmacêutico",
            href: "bulario/#/medicamento/" + encodeURIComponent(id),
          });
        }
      } else {
        list = list.filter((f) => f.id !== hubId);
      }
      localStorage.setItem(HUB_KEY, JSON.stringify(list));
    } catch (e) {
      /* localStorage indisponível — segue sem sincronizar */
    }
  }

  function toggleFavorito(id) {
    let favs = getFavoritos();
    let adicionado;
    if (favs.includes(id)) {
      favs = favs.filter((f) => f !== id);
      adicionado = false;
    } else {
      favs.unshift(id);
      adicionado = true;
    }
    setFavoritos(favs);
    const m = MEDICAMENTOS[id];
    syncFavoritoNoHub(id, m ? m.nomeGenerico : id, adicionado);
    return isFavorito(id);
  }

  function getRecentes() {
    try {
      return JSON.parse(localStorage.getItem(LS_HIST) || "[]");
    } catch (e) {
      return [];
    }
  }
  function addRecente(id) {
    let rec = getRecentes().filter((r) => r !== id);
    rec.unshift(id);
    rec = rec.slice(0, HIST_MAX);
    try {
      localStorage.setItem(LS_HIST, JSON.stringify(rec));
    } catch (e) {
      /* segue sem persistir */
    }
  }

  /* ---------------------------------------------------------------------
     Índice de busca
  --------------------------------------------------------------------- */
  let SEARCH_INDEX = [];
  let COMERCIAL_INDEX = []; // { nomeComercial, medId }

  function buildSearchIndex() {
    SEARCH_INDEX = [];
    COMERCIAL_INDEX = [];
    Object.keys(MEDICAMENTOS).forEach((id) => {
      const m = MEDICAMENTOS[id];
      // O texto pesquisável geral cobre nome genérico, princípio ativo e
      // classes — nomes comerciais são buscados separadamente (ver
      // COMERCIAL_INDEX) para permitir o destaque "nome comercial → nome
      // genérico" na tela de busca (item 25 da especificação).
      const campos = [
        m.nomeGenerico,
        m.principioAtivo,
        m.classeTerapeutica,
        m.classeFarmacologica,
        m.subclasse,
      ];
      if (m.nomesComerciais) {
        if (m.nomesComerciais.referencia) {
          COMERCIAL_INDEX.push({ nome: m.nomesComerciais.referencia, medId: id });
        }
        (m.nomesComerciais.similares || []).forEach((s) => {
          COMERCIAL_INDEX.push({ nome: s, medId: id });
        });
      }
      SEARCH_INDEX.push({
        id,
        texto: normalize(campos.filter(Boolean).join(" | ")),
        nomeGenerico: m.nomeGenerico,
      });
    });
  }


  /* ---------------------------------------------------------------------
     15/11/2026 — Busca modernizada: ranking por relevância, múltiplos
     termos, destaque do trecho encontrado e sugestões instantâneas.
  --------------------------------------------------------------------- */
  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function termos(q) { return normalize(q).split(/[\s+/,-]+/).filter(Boolean); }
  // Destaca (sem acento/maiúsculas) os termos buscados dentro do texto original.
  function destacar(texto, q) {
    const t = String(texto || "");
    const ts = termos(q || "");
    if (!ts.length || !t) return esc(t);
    const base = normalize(t);
    // normalize() pode remover combinações de acento sem mudar o comprimento visual;
    // mapeamos índice a índice pela versão NFD sem diacríticos.
    const marcas = new Array(t.length).fill(false);
    ts.forEach((term) => {
      let i = base.indexOf(term);
      while (i !== -1 && term) { for (let k = i; k < i + term.length && k < t.length; k++) marcas[k] = true; i = base.indexOf(term, i + term.length); }
    });
    if (base.length !== t.length) return esc(t);
    let out = "", aberto = false;
    for (let i = 0; i < t.length; i++) {
      if (marcas[i] && !aberto) { out += "<mark>"; aberto = true; }
      if (!marcas[i] && aberto) { out += "</mark>"; aberto = false; }
      out += esc(t[i]);
    }
    return out + (aberto ? "</mark>" : "");
  }
  function pontuar(nome, resto, ts) {
    const n = normalize(nome);
    let total = 0;
    for (const term of ts) {
      if (n === term) total += 120;
      else if (n.startsWith(term)) total += 90;
      else if (new RegExp("(^|[\\s(+/-])" + escRe(term)).test(n)) total += 70;
      else if (n.includes(term)) total += 45;
      else if (resto.includes(term)) total += 15;
      else return 0; // todos os termos precisam aparecer
    }
    return total - Math.min(n.length, 60) / 60; // nomes mais curtos primeiro em empate
  }
  function buscarRanqueado(query, limite) {
    const ts = termos(query);
    if (!ts.length) return [];
    const res = [];
    SEARCH_INDEX.forEach((e) => {
      const sc = pontuar(e.nomeGenerico, e.texto, ts);
      if (sc > 0) res.push({ id: e.id, sc });
    });
    res.sort((x, y) => y.sc - x.sc || MEDICAMENTOS[x.id].nomeGenerico.localeCompare(MEDICAMENTOS[y.id].nomeGenerico, "pt-BR"));
    return (limite ? res.slice(0, limite) : res).map((r) => r.id);
  }
  function buscarComerciaisRanqueado(query, limite) {
    const ts = termos(query);
    if (!ts.length) return [];
    const vistos = new Map();
    COMERCIAL_INDEX.forEach((c) => {
      const chave = normalize(c.nome).replace(/[^a-z0-9]/g, "") + "|" + c.medId;
      if (vistos.has(chave)) return;
      const sc = pontuar(c.nome, "", ts);
      if (sc > 0) vistos.set(chave, { ...c, sc });
    });
    const arr = Array.from(vistos.values()).sort((x, y) => y.sc - x.sc || x.nome.localeCompare(y.nome, "pt-BR"));
    return limite ? arr.slice(0, limite) : arr;
  }
  function buscarGrupos(query) {
    const ts = termos(query);
    if (!ts.length) return [];
    const res = [];
    GRUPOS.forEach((g) => {
      const scG = pontuar(g.nome, "", ts);
      if (scG > 0) res.push({ tipo: "grupo", grupo: g, nome: g.nome, sc: scG + 5, total: g.subclasses.reduce((a, s) => a + s.medicamentos.length, 0) });
      g.subclasses.forEach((s, i) => {
        const sc = pontuar(s.nome, "", ts);
        if (sc > 0) res.push({ tipo: "subclasse", grupo: g, idx: i, nome: s.nome, sc, total: s.medicamentos.length });
      });
    });
    return res.sort((x, y) => y.sc - x.sc);
  }

  function buscarMedicamentos(query) {
    return buscarRanqueado(query);
  }

  function buscarPorNomeComercial(query) {
    const q = normalize(query);
    if (!q) return [];
    const vistos = new Set();
    const resultados = [];
    COMERCIAL_INDEX.forEach((c) => {
      if (normalize(c.nome).includes(q) && !vistos.has(c.medId + "|" + c.nome)) {
        vistos.add(c.medId + "|" + c.nome);
        resultados.push(c);
      }
    });
    return resultados;
  }

  function grupoInfoDoMedicamento(medId) {
    for (const g of GRUPOS) {
      for (const s of g.subclasses) {
        if (s.medicamentos.includes(medId)) {
          return { grupo: g, subclasse: s };
        }
      }
    }
    return null;
  }

  /* ---------------------------------------------------------------------
     Roteamento (hash-based)
  --------------------------------------------------------------------- */
  const app = $("#app-view");

  // Pilha de navegação interna: permite o botão "Voltar" do cabeçalho
  // funcionar sem depender do botão voltar do navegador. Cada mudança de
  // hash que não veio do próprio botão "Voltar" empilha o hash anterior.
  let NAV_STACK = [];
  let NAV_ULTIMO_HASH = null;
  let NAV_INDO_PARA_TRAS = false;

  function atualizarBotaoVoltar() {
    const btn = $("#btn-topo-voltar");
    if (btn) btn.disabled = NAV_STACK.length === 0;
  }

  function voltarPagina() {
    if (!NAV_STACK.length) return;
    const hashAnterior = NAV_STACK.pop();
    NAV_INDO_PARA_TRAS = true;
    location.hash = hashAnterior;
  }
  window.voltarPagina = voltarPagina;

  function route() {
    const hash = decodeURIComponent(location.hash || "");
    const hashAtual = hash || "#/";
    window.scrollTo({ top: 0 });
    if (NAV_INDO_PARA_TRAS) {
      NAV_INDO_PARA_TRAS = false;
    } else if (NAV_ULTIMO_HASH !== null && NAV_ULTIMO_HASH !== hashAtual) {
      NAV_STACK.push(NAV_ULTIMO_HASH);
    }
    NAV_ULTIMO_HASH = hashAtual;
    atualizarBotaoVoltar();
    if (hash.startsWith("#/grupo/")) {
      const id = hash.replace("#/grupo/", "");
      renderGrupo(id);
    } else if (hash.startsWith("#/medicamento/")) {
      const id = hash.replace("#/medicamento/", "");
      renderFicha(id);
    } else if (hash.startsWith("#/comparar")) {
      const partes = hash.replace("#/comparar", "").split("/");
      const a = partes[1] && MEDICAMENTOS[partes[1]] ? partes[1] : null;
      const b = partes[2] && MEDICAMENTOS[partes[2]] ? partes[2] : null;
      renderComparar(a, b);
    } else if (hash.startsWith("#/busca/")) {
      const q = hash.replace("#/busca/", "");
      renderBusca(q);
    } else {
      renderHome();
    }
  }
  window.addEventListener("hashchange", route);

  function irPara(hash) {
    location.hash = hash;
  }
  window.irPara = irPara;

  /* ---------------------------------------------------------------------
     Componentes reutilizáveis
  --------------------------------------------------------------------- */
  function tagsHtml(tags) {
    if (!tags || !tags.length) return "";
    return `<div class="tag-row">${tags.map((t) => `<span class="tag-chip">${esc(t)}</span>`).join("")}</div>`;
  }

  // Uma ficha é considerada "completa" quando já foi pesquisada e escrita
  // (mecanismo de ação preenchido é o campo mais confiável como indicador,
  // pois é o primeiro a ser preenchido na revisão manual de cada fármaco).
  function fichaCompleta(m) {
    return !!(m && m.mecanismoAcao);
  }

  function iniciais(nome) {
    const p = String(nome || "").replace(/\(.*?\)/g, "").split(/[\s+]+/).filter((w) => w.length > 2);
    return ((p[0] || "?")[0] + (p[1] ? p[1][0] : (p[0] || "")[1] || "")).toUpperCase();
  }
  function medItemButton(medId, q) {
    const m = MEDICAMENTOS[medId];
    if (!m) return "";
    const fav = isFavorito(medId);
    const completo = fichaCompleta(m);
    const cor = MED_GRUPO_COR[medId];
    return `
      <div class="med-item${completo ? " med-item-completo" : ""}" role="link" tabindex="0" data-med="${medId}"${cor ? ` data-cor="${cor}"` : ""}
        onclick="irPara('#/medicamento/${medId}')" onkeydown="if(event.key==='Enter'){irPara('#/medicamento/${medId}')}">
        <span class="med-avatar" aria-hidden="true">${esc(iniciais(m.nomeGenerico))}</span>
        <span class="med-item-main">
          <span class="med-item-nome">${q ? destacar(m.nomeGenerico, q) : esc(m.nomeGenerico)}</span>
          <span class="med-item-sub">${esc(m.classeTerapeutica || "")}</span>
        </span>
        <button type="button" class="med-item-fav ${fav ? "star-on" : ""}" title="${fav ? "Remover dos favoritos" : "Adicionar aos favoritos"}" aria-label="${fav ? "Remover dos favoritos" : "Adicionar aos favoritos"}" aria-pressed="${fav}"
          onclick="event.stopPropagation(); bxToggleFav(this, '${medId}')">★</button>
        <span class="med-item-seta" aria-hidden="true">›</span>
      </div>`;
  }
  window.bxToggleFav = function (btn, medId) {
    const on = toggleFavorito(medId);
    btn.classList.toggle("star-on", on);
    btn.setAttribute("aria-pressed", on);
    btn.title = on ? "Remover dos favoritos" : "Adicionar aos favoritos";
    btn.classList.remove("pop"); void btn.offsetWidth; btn.classList.add("pop");
  };

  function grupoCard(g) {
    const totalMeds = g.subclasses.reduce((acc, s) => acc + s.medicamentos.length, 0);
    return `
      <button class="grupo-card" data-cor="${g.cor}" onclick="irPara('#/grupo/${g.id}')">
        <span class="grupo-card-icone" aria-hidden="true">${g.icone}</span>
        <span class="grupo-card-nome">${esc(g.nome)}</span>
        <span class="grupo-card-count">${totalMeds} medicamento${totalMeds === 1 ? "" : "s"}</span>
      </button>`;
  }

  /* ---------------------------------------------------------------------
     VIEW: Home (grupos + favoritos + recentes)
  --------------------------------------------------------------------- */
  function renderHome(filtroGrupo) {
    const totalMedicamentos = Object.keys(MEDICAMENTOS).length;
    setTituloTopo("Bulário Farmacêutico", `Consulte informações farmacológicas, clínicas e farmacoterapêuticas de medicamentos de forma rápida e organizada. ${totalMedicamentos.toLocaleString("pt-BR")} medicamentos catalogados.`);
    const favs = getFavoritos().filter((id) => MEDICAMENTOS[id]);
    const recentes = getRecentes().filter((id) => MEDICAMENTOS[id]).slice(0, 10);
    const gruposFiltrados = filtroGrupo
      ? GRUPOS.filter((g) => normalize(g.nome).includes(normalize(filtroGrupo)))
      : GRUPOS;
    const totalSub = GRUPOS.reduce((a, g) => a + g.subclasses.length, 0);

    app.innerHTML = `
      <div class="home-view">
        <section class="bx-stats" aria-label="Resumo do Bulário">
          <div class="bx-stat"><strong>${totalMedicamentos.toLocaleString("pt-BR")}</strong><span>medicamentos</span></div>
          <div class="bx-stat"><strong>${GRUPOS.length}</strong><span>grupos ATC</span></div>
          <div class="bx-stat"><strong>${totalSub}</strong><span>subclasses</span></div>
          <div class="bx-stat"><strong>${favs.length}</strong><span>favoritos</span></div>
          <button type="button" class="bx-btn bx-btn-ghost bx-sorteio" onclick="bxSortear()" title="Abrir a ficha de um medicamento aleatório — bom para estudar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8.5" cy="8.5" r="1.2" fill="currentColor"/><circle cx="15.5" cy="15.5" r="1.2" fill="currentColor"/><circle cx="15.5" cy="8.5" r="1.2" fill="currentColor"/><circle cx="8.5" cy="15.5" r="1.2" fill="currentColor"/></svg>
            Fármaco aleatório
          </button>
        </section>
        ${
          favs.length
            ? `<section class="quick-section">
                <div class="bx-sec-head"><h2>Meus medicamentos</h2><span class="bx-sec-dica">${favs.length} favorito${favs.length === 1 ? "" : "s"}</span></div>
                <div class="med-list-flat med-grid">${favs.map((id) => medItemButton(id)).join("")}</div>
              </section>`
            : ""
        }
        <section class="quick-section">
          <div class="bx-sec-head"><h2>Grupos farmacológicos</h2><span class="bx-sec-dica">classificação ATC</span></div>
          <div class="grupos-grid" id="grupos-grid">
            ${gruposFiltrados.map(grupoCard).join("") || `<p class="empty-msg">Nenhum grupo encontrado para esse filtro.</p>`}
          </div>
        </section>
      </div>`;
  }
  window.bxSortear = function () {
    const ids = Object.keys(MEDICAMENTOS).filter((id) => fichaCompleta(MEDICAMENTOS[id]));
    if (ids.length) irPara("#/medicamento/" + ids[Math.floor(Math.random() * ids.length)]);
  };

  /* ---------------------------------------------------------------------
     VIEW: Grupo (subclasses em acordeão + lista de medicamentos)
  --------------------------------------------------------------------- */
  function renderGrupo(grupoId) {
    const g = GRUPOS.find((x) => x.id === grupoId);
    if (!g) {
      renderHome();
      return;
    }
    setTituloTopo(g.nome, "Subclasses e medicamentos deste grupo farmacológico.");
    app.innerHTML = `
      <div class="grupo-view">
        <a href="#/" class="btn-voltar">‹ Todos os grupos</a>
        <h1 class="grupo-titulo"><span aria-hidden="true">${g.icone}</span> ${esc(g.nome)}</h1>
        <div class="subclasses-lista">
          ${g.subclasses
            .map(
              (s, i) => `
            <div class="subclasse-bloco" data-cor="${g.cor}">
              <button class="subclasse-header" data-open="${i === 0 ? "true" : "false"}" onclick="this.parentElement.classList.toggle('aberto'); this.setAttribute('data-open', this.parentElement.classList.contains('aberto'))">
                <span>${esc(s.nome)}</span>
                <span class="subclasse-count">${s.medicamentos.length}</span>
              </button>
              <div class="subclasse-itens">
                <div class="med-list-flat">${s.medicamentos.map((id) => medItemButton(id)).join("")}</div>
              </div>
            </div>`
            )
            .join("")}
        </div>
      </div>`;
    if (g.subclasses.length) {
      $(".subclasse-bloco", app).classList.add("aberto");
    }
  }

  /* ---------------------------------------------------------------------
     VIEW: Busca
  --------------------------------------------------------------------- */
  let ESCOPO_BUSCA = "tudo";
  function renderBusca(query) {
    setTituloTopo("Resultado da busca", `"${query}"`);
    const ids = buscarRanqueado(query);
    const comerciais = buscarComerciaisRanqueado(query);
    const grupos = buscarGrupos(query);
    const n = { tudo: ids.length + comerciais.length + grupos.length, med: ids.length, com: comerciais.length, grp: grupos.length };
    if (ESCOPO_BUSCA !== "tudo" && !n[ESCOPO_BUSCA]) ESCOPO_BUSCA = "tudo";
    const aba = (k, rot) => `<button type="button" class="bx-tab${ESCOPO_BUSCA === k ? " ativo" : ""}" onclick="bxEscopo('${k}')"${n[k] || k === "tudo" ? "" : " disabled"}>${rot}<span>${n[k]}</span></button>`;
    const ver = (k) => ESCOPO_BUSCA === "tudo" || ESCOPO_BUSCA === k;
    const LIM = 12;

    let html = `<div class="busca-view">
      <div class="bx-busca-head">
        <h1 class="grupo-titulo">Resultados para <span class="bx-q">“${esc(query)}”</span></h1>
        <div class="bx-tabs" role="tablist">${aba("tudo", "Tudo")}${aba("med", "Medicamentos")}${aba("com", "Nomes comerciais")}${aba("grp", "Grupos e classes")}</div>
      </div>`;

    if (!n.tudo) {
      html += `<div class="bx-vazio"><div class="bx-vazio-ico">${'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'}</div>
        <h3>Nada encontrado para “${esc(query)}”</h3>
        <p>Confira a grafia ou tente o princípio ativo, um nome comercial ou a classe (ex.: “estatina”, “IECA”, “antifúngico”).</p></div>`;
    }

    if (ids.length && ver("med")) {
      const mostrar = ESCOPO_BUSCA === "tudo" ? ids.slice(0, LIM) : ids;
      html += `<section class="quick-section"><div class="bx-sec-head"><h2>Medicamentos</h2><span class="bx-sec-dica">${ids.length} encontrado${ids.length === 1 ? "" : "s"} · por relevância</span></div>
        <div class="med-list-flat med-grid">${mostrar.map((id) => medItemButton(id, query)).join("")}</div>
        ${ESCOPO_BUSCA === "tudo" && ids.length > LIM ? `<button class="bx-btn bx-btn-ghost bx-ver-mais" onclick="bxEscopo('med')">Ver todos os ${ids.length} medicamentos</button>` : ""}</section>`;
    }
    if (grupos.length && ver("grp")) {
      html += `<section class="quick-section"><div class="bx-sec-head"><h2>Grupos e classes</h2><span class="bx-sec-dica">${grupos.length}</span></div><div class="bx-grp-list">`;
      grupos.forEach((r) => {
        html += `<button class="bx-grp-item" data-cor="${r.grupo.cor}" onclick="bxAbrirGrupo('${r.grupo.id}', ${r.tipo === "subclasse" ? r.idx : -1})">
            <span class="bx-grp-ico" aria-hidden="true">${r.grupo.icone}</span>
            <span class="bx-grp-txt"><strong>${destacar(r.nome, query)}</strong><small>${r.tipo === "subclasse" ? "Subclasse de " + esc(r.grupo.nome) : "Grupo farmacológico"} · ${r.total} medicamento${r.total === 1 ? "" : "s"}</small></span>
            <span class="med-item-seta" aria-hidden="true">›</span></button>`;
      });
      html += `</div></section>`;
    }
    if (comerciais.length && ver("com")) {
      const mostrar = ESCOPO_BUSCA === "tudo" ? comerciais.slice(0, LIM) : comerciais;
      html += `<section class="quick-section"><div class="bx-sec-head"><h2>Nomes comerciais</h2><span class="bx-sec-dica">${comerciais.length}</span></div><div class="comercial-list">`;
      mostrar.forEach((c) => {
        const m = MEDICAMENTOS[c.medId];
        html += `
          <button class="comercial-item" data-cor="${MED_GRUPO_COR[c.medId] || ""}" onclick="irPara('#/medicamento/${c.medId}')">
            <span class="comercial-nome">${destacar(c.nome, query)}</span>
            <span class="comercial-seta" aria-hidden="true">→</span>
            <span class="comercial-generico">${esc(m.principioAtivo || m.nomeGenerico)}</span>
          </button>`;
      });
      html += `</div>${ESCOPO_BUSCA === "tudo" && comerciais.length > LIM ? `<button class="bx-btn bx-btn-ghost bx-ver-mais" onclick="bxEscopo('com')">Ver todos os ${comerciais.length} nomes comerciais</button>` : ""}</section>`;
    }
    html += `</div>`;
    app.innerHTML = html;
  }
  window.bxEscopo = function (k) {
    ESCOPO_BUSCA = k;
    const q = decodeURIComponent(location.hash).replace("#/busca/", "");
    renderBusca(q);
  };
  window.bxAbrirGrupo = function (gid, idx) {
    irPara("#/grupo/" + gid);
    if (idx >= 0) setTimeout(() => {
      const blocos = $all(".subclasse-bloco", app);
      blocos.forEach((b, i) => b.classList.toggle("aberto", i === idx));
      if (blocos[idx]) blocos[idx].scrollIntoView({ behavior: "smooth", block: "start" });
    }, 60);
  };

  /* ---------------------------------------------------------------------
     VIEW: Ficha do medicamento
  --------------------------------------------------------------------- */
  function listaOuTexto(v) {
    if (Array.isArray(v)) {
      if (!v.length) return "";
      return `<ul>${v.map((i) => `<li>${esc(i)}</li>`).join("")}</ul>`;
    }
    if (v === undefined || v === null || v === "") return "";
    return `<p>${esc(v)}</p>`;
  }

  function interacoesBloco(titulo, classe, icone, lista) {
    if (!lista || !lista.length) return "";
    return `
      <div class="interacao-grupo interacao-${classe}">
        <h3>${icone} ${titulo}</h3>
        ${lista
          .map(
            (it) => `
          <div class="interacao-item">
            <p class="interacao-par">${esc(it.par)}</p>
            <p><strong>Mecanismo:</strong> ${esc(it.mecanismo)}</p>
            <p><strong>Conduta:</strong> ${esc(it.conduta)}</p>
          </div>`
          )
          .join("")}
      </div>`;
  }

  function reacoesBloco(titulo, lista) {
    if (!lista || !lista.length) return "";
    return `<div class="reacao-freq"><h4>${esc(titulo)}</h4><ul>${lista.map((i) => `<li>${esc(i)}</li>`).join("")}</ul></div>`;
  }

  // Bolinha colorida de risco em Gestação/Lactação. Gestação usa as
  // categorias clássicas FDA (A/B/C/D/X); Lactação usa as Categorias de
  // Risco em Lactação de Hale (L1-L5), padrão clínico real para esse uso —
  // ambas mapeadas para a mesma escala visual verde→vermelho. Campos
  // opcionais (gestacaoCategoria/lactacaoCategoria): fichas antigas sem eles
  // simplesmente não mostram a bolinha (retorno ""), sem quebrar nada.
  const RISCO_CORES_GESTACAO = { A: "verde", B: "verde", C: "amarelo", D: "laranja", X: "vermelho" };
  const RISCO_CORES_LACTACAO = { L1: "verde", L2: "verde", L3: "amarelo", L4: "laranja", L5: "vermelho" };

  function riscoDotHtml(categoria, tipo) {
    if (!categoria) return "";
    const mapa = tipo === "lactacao" ? RISCO_CORES_LACTACAO : RISCO_CORES_GESTACAO;
    const cor = mapa[categoria];
    if (!cor) return "";
    return ` <span class="risco-dot risco-dot-${cor}" title="Categoria ${esc(categoria)}" aria-hidden="true"></span><span class="risco-label">Categoria ${esc(categoria)}</span>`;
  }

  function secoesFicha(m) {
    const secoes = [];
    // Registros ainda sem ficha farmacoterapêutica completa não trazem
    // alertasFarmaceuticos/referencias/ultimaAtualizacao próprios — usamos
    // o aviso padrão definido uma única vez (AVISO_FICHA_PENDENTE) em vez de
    // repeti-lo em cada um dos milhares de registros.
    const alertas = (m.alertasFarmaceuticos && m.alertasFarmaceuticos.length) ? m.alertasFarmaceuticos : [AVISO_FICHA_PENDENTE];
    const referencias = (m.referencias && m.referencias.length) ? m.referencias : null;
    const ultimaAtualizacao = m.ultimaAtualizacao || null;

    if (m.nomesComerciais && (m.nomesComerciais.referencia || (m.nomesComerciais.similares && m.nomesComerciais.similares.length))) {
      secoes.push({
        id: "nomes-comerciais",
        titulo: "Nomes Comerciais",
        html: `
          ${m.nomesComerciais.referencia ? `<p><strong>Medicamento referência:</strong> ${esc(m.nomesComerciais.referencia)}</p>` : ""}
          ${m.nomesComerciais.similares && m.nomesComerciais.similares.length ? `<p><strong>Similares:</strong> ${m.nomesComerciais.similares.map(esc).join(", ")}</p>` : ""}
        `,
      });
    }

    if (m.generico !== undefined || m.similar !== undefined || m.farmaciaPopular !== undefined) {
      secoes.push({
        id: "generico-farmacia-popular",
        titulo: "Genérico / Farmácia Popular",
        html: `
          <p><strong>Medicamento genérico disponível:</strong> ${m.generico ? "Sim" : "Não"}</p>
          <p><strong>Medicamento similar disponível:</strong> ${m.similar ? "Sim" : "Não"}</p>
          <p><strong>Disponível no Programa Farmácia Popular:</strong> ${m.farmaciaPopular ? "Sim" : "Não"}</p>
        `,
      });
    }

    if (m.classeTerapeutica || m.classeFarmacologica || m.subclasse) {
      secoes.push({
        id: "classe",
        titulo: "Classe Terapêutica e Farmacológica",
        html: `
          ${m.classeTerapeutica ? `<p><strong>Classe${m.classes && m.classes.length > 1 ? "s terapêuticas" : " terapêutica"}:</strong> ${esc(m.classeTerapeutica)}</p>` : ""}
          ${m.classeFarmacologica ? `<p><strong>Classe farmacológica:</strong> ${esc(m.classeFarmacologica)}</p>` : ""}
          ${m.subclasse ? `<p><strong>Subclasse:</strong> ${esc(m.subclasse)}</p>` : ""}
        `,
      });
    }

    if (m.mecanismoAcao) {
      secoes.push({ id: "mecanismo", titulo: "Mecanismo de Ação", html: `<p>${esc(m.mecanismoAcao)}</p>` });
    }

    if (m.farmacocinetica) {
      const fc = m.farmacocinetica;
      const linhas = [
        ["Absorção", fc.absorcao],
        ["Biodisponibilidade", fc.biodisponibilidade],
        ["Distribuição", fc.distribuicao],
        ["Ligação a proteínas plasmáticas", fc.ligacaoProteica],
        ["Metabolismo", fc.metabolismo],
        ["Meia-vida", fc.meiaVida],
        ["Excreção", fc.excrecao],
        ["Clearance", fc.clearance],
      ].filter(([, v]) => v);
      secoes.push({
        id: "farmacocinetica",
        titulo: "Farmacocinética",
        html: `<ul class="lista-definicao">${linhas.map(([k, v]) => `<li><strong>${k}:</strong> ${esc(v)}</li>`).join("")}</ul>`,
      });
    }

    if (m.indicacoes && m.indicacoes.length) {
      secoes.push({ id: "indicacoes", titulo: "Indicações", html: listaOuTexto(m.indicacoes) });
    }

    if ((m.contraindicacoes && m.contraindicacoes.length) || (m.precaucoes && m.precaucoes.length)) {
      secoes.push({
        id: "contraindicacoes",
        titulo: "Contraindicações e Precauções",
        html: `
          ${m.contraindicacoes && m.contraindicacoes.length ? `<h4>Contraindicações</h4>${listaOuTexto(m.contraindicacoes)}` : ""}
          ${m.precaucoes && m.precaucoes.length ? `<h4>Precauções e advertências</h4>${listaOuTexto(m.precaucoes)}` : ""}
        `,
      });
    }

    if (m.posologia) {
      const p = m.posologia;
      const blocos = [
        ["Adultos", p.adultos],
        ["Pediátrica", p.pediatrica],
        ["Idosos", p.idosos],
        ["Insuficiência renal", p.renal],
        ["Insuficiência hepática", p.hepatica],
      ].filter(([, v]) => v);
      secoes.push({
        id: "posologia",
        titulo: "Posologia e Ajuste de Dose",
        html: blocos.map(([k, v]) => `<h4>${k}</h4><p>${esc(v)}</p>`).join(""),
      });
    }

    if (m.apresentacoes && m.apresentacoes.length) {
      secoes.push({
        id: "apresentacoes",
        titulo: "Apresentações",
        html: `<ul>${m.apresentacoes
          .map((a) => `<li><strong>${esc(a.forma)}:</strong> ${a.concentracoes.map(esc).join(", ")}${a.obs ? ` — <span class="texto-dim">${esc(a.obs)}</span>` : ""}</li>`)
          .join("")}</ul>`,
      });
    }

    if (m.viasAdministracao && m.viasAdministracao.length) {
      secoes.push({ id: "administracao", titulo: "Formas de Administração", html: `<p>${m.viasAdministracao.map(esc).join(" · ")}</p>` });
    }

    if (m.interacoes && (m.interacoes.graves.length || m.interacoes.moderadas.length || m.interacoes.menores.length)) {
      secoes.push({
        id: "interacoes",
        titulo: "Interações Medicamentosas",
        html:
          interacoesBloco("Graves", "grave", "🔴", m.interacoes.graves) +
          interacoesBloco("Moderadas", "moderada", "🟠", m.interacoes.moderadas) +
          interacoesBloco("Menores", "menor", "🟢", m.interacoes.menores),
      });
    }

    if (m.interacoesAlimentares && m.interacoesAlimentares.length) {
      secoes.push({ id: "interacoes-alimentares", titulo: "Interações com Alimentos", html: listaOuTexto(m.interacoesAlimentares) });
    }

    if (m.reacoesAdversas) {
      const r = m.reacoesAdversas;
      secoes.push({
        id: "reacoes-adversas",
        titulo: "Reações Adversas",
        html:
          reacoesBloco("Muito comuns", r.muitoComuns) +
          reacoesBloco("Comuns", r.comuns) +
          reacoesBloco("Incomuns", r.incomuns) +
          reacoesBloco("Raras", r.raras) +
          (r.graves && r.graves.length ? `<div class="reacao-freq reacao-graves"><h4>⚠️ Graves / exigem atenção imediata</h4><ul>${r.graves.map((i) => `<li>${esc(i)}</li>`).join("")}</ul></div>` : ""),
      });
    }

    if (alertas && alertas.length) {
      secoes.push({
        id: "alertas",
        titulo: "Alertas Farmacêuticos",
        html: `<div class="alerta-box${(!m.alertasFarmaceuticos || !m.alertasFarmaceuticos.length) ? " alerta-box-info" : ""}"><h3>⚠️ ${(!m.alertasFarmaceuticos || !m.alertasFarmaceuticos.length) ? "Ficha em Revisão" : "Alertas Farmacêuticos"}</h3>${listaOuTexto(alertas)}</div>`,
      });
    }

    if (m.orientacoesPaciente) {
      const o = m.orientacoesPaciente;
      const linhas = [
        ["Como tomar?", o.comoTomar],
        ["O que fazer se esquecer uma dose?", o.esquecimento],
        ["Pode dirigir?", o.dirigir],
        ["Pode consumir álcool?", o.alcool],
        ["Pode tomar com alimentos?", o.alimentos],
        ["Quando procurar atendimento médico?", o.sinaisAlerta],
      ].filter(([, v]) => v);
      secoes.push({
        id: "orientacoes-paciente",
        titulo: "Orientações ao Paciente",
        html: linhas.map(([k, v]) => `<p><strong>${k}</strong><br>${esc(v)}</p>`).join(""),
      });
    }

    if (m.monitoramento && m.monitoramento.length) {
      secoes.push({
        id: "monitoramento",
        titulo: "Exames e Monitoramento",
        html: `
          <table class="tabela-monitoramento">
            <thead><tr><th>Parâmetro</th><th>Monitoramento</th></tr></thead>
            <tbody>${m.monitoramento.map((r) => `<tr><td>${esc(r.parametro)}</td><td>${esc(r.quando)}</td></tr>`).join("")}</tbody>
          </table>`,
      });
    }

    if (m.gestacao) {
      secoes.push({ id: "gestacao", titulo: "🤰 Gestação", tituloExtra: riscoDotHtml(m.gestacaoCategoria, "gestacao"), html: `<p>${esc(m.gestacao)}</p>` });
    }
    if (m.lactacao) {
      secoes.push({ id: "lactacao", titulo: "🤱 Lactação", tituloExtra: riscoDotHtml(m.lactacaoCategoria, "lactacao"), html: `<p>${esc(m.lactacao)}</p>` });
    }

    const especiais = [
      ["Pediatria", m.pediatria],
      ["Geriatria", m.geriatria],
      ["Insuficiência renal", m.renal],
      ["Insuficiência hepática", m.hepatica],
    ].filter(([, v]) => v);
    if (especiais.length) {
      secoes.push({
        id: "populacoes-especiais",
        titulo: "Populações Especiais",
        html: especiais.map(([k, v]) => `<h4>${k}</h4><p>${esc(v)}</p>`).join(""),
      });
    }

    if (m.tipoReceituario || m.dispensacao) {
      secoes.push({
        id: "receituario",
        titulo: "Tipo de Receituário e Dispensação",
        html: `
          ${m.tipoReceituario ? `<p><strong>Tipo de receituário:</strong> ${esc(m.tipoReceituario)}</p>` : ""}
          ${m.dispensacao ? ((typeof m.dispensacao === "object" && !Array.isArray(m.dispensacao)) ? `<p><strong>Sujeito a controle especial:</strong> ${m.dispensacao.controleEspecial ? "Sim" : "Não"}</p><p><strong>Retenção de receita:</strong> ${m.dispensacao.retencaoReceita ? "Sim" : "Não"}</p><p><strong>Condições de dispensação:</strong> ${esc(m.dispensacao.condicoes)}</p>` : `<p><strong>Condições de dispensação:</strong></p>${listaOuTexto(m.dispensacao)}`) : ""}
        `,
      });
    }

    if (referencias && referencias.length) {
      secoes.push({
        id: "referencias",
        titulo: "Referências Bibliográficas",
        html: `${listaOuTexto(referencias)}<p class="texto-dim"><strong>Última atualização:</strong> ${esc(ultimaAtualizacao || NAO_DISPONIVEL)}</p>`,
      });
    }

    return secoes;
  }

  function renderFicha(medId) {
    const m = MEDICAMENTOS[medId];
    if (!m) {
      renderHome();
      return;
    }
    addRecente(medId);
    setTituloTopo(m.nomeGenerico, m.classeTerapeutica || "");
    const secoes = secoesFicha(m);
    const gi = grupoInfoDoMedicamento(medId);
    const fav = isFavorito(medId);

    app.innerHTML = `
      <div class="ficha-view">
        <div class="ficha-topo">
          <a href="${gi ? `#/grupo/${gi.grupo.id}` : "#/"}" class="btn-voltar">‹ ${gi ? esc(gi.grupo.nome) : "Todos os grupos"}</a>
          <div class="ficha-titulo-row">
            <h1 class="ficha-titulo">${esc(m.nomeGenerico)}</h1>
            <div class="ficha-acoes">
              <button class="btn-ficha-acao" type="button" onclick="compararCom('${medId}')" title="Comparar com outro fármaco"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4 3 8l4 4"/><path d="M3 8h13"/><path d="m17 20 4-4-4-4"/><path d="M21 16H8"/></svg>Comparar</button>
              <button class="btn-ficha-acao" type="button" onclick="abrirCartaoPaciente('${medId}')" title="Cartão de orientação para entregar ao paciente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><circle cx="9" cy="11" r="2"/><path d="M6.5 16c.6-1.4 1.5-2 2.5-2s1.9.6 2.5 2"/><path d="M14 10h4M14 13.5h3"/></svg>Cartão do paciente</button>
              <button class="btn-favoritar ${fav ? "ativo" : ""}" id="btn-fav" title="Favoritar medicamento" aria-label="Favoritar medicamento">
                <span class="estrela">★</span><span class="btn-favoritar-label">${fav ? "Favoritado" : "Favoritar"}</span>
              </button>
            </div>
          </div>
          ${tagsHtml(m.tags)}
          ${seloFichaHtml(m)}
          <div class="ficha-atalhos" id="ficha-atalhos" hidden></div>
        </div>

        <nav class="ficha-menu-rapido" aria-label="Acesso rápido às seções">
          ${secoes.map((s) => `<a href="#sec-${s.id}" class="menu-rapido-item" data-target="sec-${s.id}">${esc(s.titulo)}</a>`).join("")}
        </nav>

        <div class="ficha-corpo">
          <aside class="ficha-sidebar" aria-label="Menu de seções">
            <ul>
              ${secoes.map((s) => `<li><a href="#sec-${s.id}" data-target="sec-${s.id}">${esc(s.titulo)}</a></li>`).join("")}
            </ul>
          </aside>
          <div class="ficha-conteudo">
            ${secoes.map((s) => `<section id="sec-${s.id}" class="ficha-secao"><h2>${esc(s.titulo)}${s.tituloExtra || ""}</h2>${s.html}</section>`).join("")}
            <p class="aviso-secao-final">Alguma informação desta ficha não estava disponível na base consultada? Ela foi omitida em vez de presumida — consulte sempre a bula vigente e o julgamento clínico.</p>
          </div>
        </div>
      </div>`;

    $("#btn-fav", app).addEventListener("click", () => {
      const novoEstado = toggleFavorito(medId);
      const btn = $("#btn-fav", app);
      btn.classList.toggle("ativo", novoEstado);
      $(".btn-favoritar-label", btn).textContent = novoEstado ? "Favoritado" : "Favoritar";
    });

    // Scroll suave nas âncoras (sidebar + menu rápido mobile)
    $all('a[data-target]', app).forEach((a) => {
      a.addEventListener("click", (ev) => {
        ev.preventDefault();
        const target = document.getElementById(a.dataset.target);
        if (target) {
          const header = document.querySelector(".search-bar-row");
          const headerH = header ? header.getBoundingClientRect().height : 0;
          const y = target.getBoundingClientRect().top + window.scrollY - headerH - 14;
          window.scrollTo({ top: y, behavior: "smooth" });
        }
      });
    });

    ativarObservadorSecoes();
    renderAtalhos(medId);
  }

  // ---------- Atalhos para as outras ferramentas do FarmaPrática ----------
  // atalhos.json é gerado por scripts/gerar_atalhos_bulario.py (cruzamento por
  // nome com Interações, Cálculo de Doses, Controle Especial e CMED).
  let atalhosPromise = null;
  function carregarAtalhos() {
    if (!atalhosPromise) {
      atalhosPromise = fetch("atalhos.json")
        .then((r) => (r.ok ? r.json() : { atalhos: {} }))
        .then((d) => (d && d.atalhos) || {})
        .catch(() => ({}));
    }
    return atalhosPromise;
  }
  const ICO_AT = {
    interacoes: '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
    calc: '<rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="11" x2="8.01" y2="11"/><line x1="12" y1="11" x2="12.01" y2="11"/><line x1="16" y1="11" x2="16.01" y2="11"/><line x1="8" y1="16" x2="8.01" y2="16"/><line x1="12" y1="16" x2="12.01" y2="16"/><line x1="16" y1="16" x2="16.01" y2="16"/>',
    medinter: '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    controlado: '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5z"/><polyline points="14 2 14 8 20 8"/><path d="M9 15h6"/><path d="M12 12v6"/>'
  };
  function atalhoLink(href, tipo, titulo, sub) {
    return `<a class="atalho-chip atalho-${tipo}" href="${esc(href)}">
      <span class="atalho-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICO_AT[tipo]}</svg></span>
      <span class="atalho-txt"><strong>${esc(titulo)}</strong><small>${esc(sub)}</small></span></a>`;
  }
  function renderAtalhos(medId) {
    carregarAtalhos().then((mapa) => {
      const box = document.getElementById("ficha-atalhos");
      if (!box || location.hash !== "#/medicamento/" + medId) return;
      const a = mapa[medId];
      if (!a) return;
      const html = [];
      if (a.interacoes) html.push(atalhoLink("../interacoes/?med=" + encodeURIComponent(a.interacoes), "interacoes", "Checar interações", "Interações Medicamentosas"));
      if (a.calc) html.push(atalhoLink("../dosespediatricas/?farmaco=" + encodeURIComponent(a.calc), "calc", "Calcular dose", "Cálculo de Doses"));
      if (a.medinter) html.push(atalhoLink("../medinter/?med=" + encodeURIComponent(a.medinter), "medinter", "Equivalentes e preços", "Substituição de Medicamentos"));
      if (a.controlado) {
        const lista = a.controlado.lista === "ANTIMICROBIANO" ? "Antimicrobiano (retenção de receita)" : "Controle especial · Lista " + a.controlado.lista;
        html.push(atalhoLink("../consultacontrolados/?substancia=" + encodeURIComponent(a.controlado.nome), "controlado", "Receituário", lista));
      }
      if (!html.length) return;
      box.innerHTML = `<span class="atalhos-rotulo">Abrir em outras ferramentas</span><div class="atalhos-lista">${html.join("")}</div>`;
      box.hidden = false;
    });
  }

  /* ---------------------------------------------------------------------
     10/11/2026 — Selo de completude, comparação entre dois fármacos e
     cartão de orientação ao paciente.
  --------------------------------------------------------------------- */
  function dataBR(iso) {
    if (!iso || !/^\d{4}-\d{2}-\d{2}/.test(iso)) return iso || "";
    const [y, mm, d] = iso.slice(0, 10).split("-");
    return `${d}/${mm}/${y}`;
  }
  function seloFichaHtml(m) {
    const completa = fichaCompleta(m);
    const nRef = (m.referencias || []).length;
    if (!completa) {
      return `<div class="ficha-selo selo-pendente"><span class="selo-tag">◔ Ficha mínima</span><span>Conteúdo farmacoterapêutico em revisão — confira a bula vigente.</span></div>`;
    }
    return `<div class="ficha-selo"><span class="selo-tag">✓ Ficha completa</span>` +
      (m.ultimaAtualizacao ? `<span>Revisada em <b>${esc(dataBR(m.ultimaAtualizacao))}</b></span>` : "") +
      (nRef ? `<a href="#sec-referencias" data-target="sec-referencias">${nRef} referência${nRef > 1 ? "s" : ""}</a>` : "") +
      `</div>`;
  }

  // ---------- Comparar dois fármacos ----------
  function textoCurto(v) {
    if (v === undefined || v === null || v === "") return "";
    if (Array.isArray(v)) return v.length ? `<ul>${v.map((i) => `<li>${esc(typeof i === "string" ? i : (i.par || JSON.stringify(i)))}</li>`).join("")}</ul>` : "";
    return `<p>${esc(v)}</p>`;
  }
  const LINHAS_COMPARACAO = [
    ["Classe terapêutica", (m) => textoCurto(m.classeTerapeutica)],
    ["Mecanismo de ação", (m) => textoCurto(m.mecanismoAcao)],
    ["Indicações", (m) => textoCurto(m.indicacoes)],
    ["Posologia — adultos", (m) => textoCurto(m.posologia && m.posologia.adultos)],
    ["Posologia — pediátrica", (m) => textoCurto(m.posologia && m.posologia.pediatrica)],
    ["Contraindicações", (m) => textoCurto(m.contraindicacoes)],
    ["Interações graves", (m) => { const g = (m.interacoes && m.interacoes.graves) || []; return g.length ? `<p class="cmp-num">${g.length}</p>` + textoCurto(g.map((x) => x.par)) : `<p class="texto-dim">Nenhuma registrada</p>`; }],
    ["Reações adversas comuns", (m) => { const r = m.reacoesAdversas || {}; return textoCurto([].concat(r.muitoComuns || [], r.comuns || [])); }],
    ["Reações adversas graves", (m) => textoCurto((m.reacoesAdversas || {}).graves)],
    ["Gestação", (m) => (m.gestacaoCategoria ? `<p>${riscoDotHtml(m.gestacaoCategoria, "gestacao")}</p>` : "") + textoCurto(m.gestacao)],
    ["Lactação", (m) => (m.lactacaoCategoria ? `<p>${riscoDotHtml(m.lactacaoCategoria, "lactacao")}</p>` : "") + textoCurto(m.lactacao)],
    ["Insuficiência renal", (m) => textoCurto(m.renal || (m.posologia && m.posologia.renal))],
    ["Insuficiência hepática", (m) => textoCurto(m.hepatica || (m.posologia && m.posologia.hepatica))],
    ["Idosos", (m) => textoCurto(m.geriatria)],
    ["Receituário", (m) => textoCurto(m.tipoReceituario)],
    ["Genérico / Farmácia Popular", (m) => `<p>Genérico: <b>${m.generico ? "sim" : "não"}</b> · Farmácia Popular: <b>${m.farmaciaPopular ? "sim" : "não"}</b></p>`],
  ];
  function seletorComparacaoHtml(slot, medId, outro) {
    const m = medId ? MEDICAMENTOS[medId] : null;
    return `<div class="cmp-slot" data-slot="${slot}">
      ${m ? `<div class="cmp-escolhido"><span class="cmp-letra">${slot === "a" ? "A" : "B"}</span><div><b>${esc(m.nomeGenerico)}</b><small>${esc(m.classeTerapeutica || "")}</small></div>
        <button type="button" class="cmp-trocar" onclick="limparComparacao('${slot}')">Trocar</button></div>` : ""}
      <div class="cmp-busca"${m ? " hidden" : ""}>
        <input type="text" class="cmp-input" placeholder="Buscar fármaco ${slot === "a" ? "A" : "B"} (nome ou marca)" autocomplete="off" data-slot="${slot}" data-outro="${esc(outro || "")}">
        <div class="cmp-sugestoes"></div>
      </div>
    </div>`;
  }
  function renderComparar(a, b) {
    const ma = a ? MEDICAMENTOS[a] : null, mb = b ? MEDICAMENTOS[b] : null;
    setTituloTopo("Comparar fármacos", "Dois fármacos lado a lado, com os mesmos campos da ficha");
    let html = `<div class="cmp-view">
      <a href="${ma ? `#/medicamento/${a}` : "#/"}" class="btn-voltar">‹ ${ma ? esc(ma.nomeGenerico) : "Todos os grupos"}</a>
      <h1 class="ficha-titulo">Comparar fármacos</h1>
      <div class="cmp-seletores">${seletorComparacaoHtml("a", ma ? a : null, b)}<span class="cmp-vs">×</span>${seletorComparacaoHtml("b", mb ? b : null, a)}</div>`;
    if (ma && mb) {
      html += `<div class="cmp-tabela" role="table">
        <div class="cmp-linha cmp-cab" role="row"><div role="columnheader"></div>
          <div role="columnheader"><a href="#/medicamento/${a}">${esc(ma.nomeGenerico)}</a></div>
          <div role="columnheader"><a href="#/medicamento/${b}">${esc(mb.nomeGenerico)}</a></div></div>` +
        LINHAS_COMPARACAO.map(([rot, fn]) => {
          const va = fn(ma) || `<p class="texto-dim">—</p>`, vb = fn(mb) || `<p class="texto-dim">—</p>`;
          return `<div class="cmp-linha${va === vb ? " cmp-igual" : ""}" role="row"><div class="cmp-rot" role="rowheader">${rot}${va === vb ? `<small>igual</small>` : ""}</div><div class="cmp-col" data-nome="${esc(ma.nomeGenerico)}" role="cell">${va}</div><div class="cmp-col" data-nome="${esc(mb.nomeGenerico)}" role="cell">${vb}</div></div>`;
        }).join("") + `</div>
        <p class="aviso-secao-final">Comparação gerada a partir das fichas do Bulário. Confira sempre a bula vigente de cada produto.</p>`;
    } else {
      html += `<p class="cmp-dica">Escolha os dois fármacos para ver a comparação lado a lado.</p>`;
    }
    html += `</div>`;
    app.innerHTML = html;
    ligarSeletoresComparacao(a, b);
    const vazio = $(".cmp-input:not([hidden])", app);
    const primeiro = $all(".cmp-busca", app).find((el) => !el.hidden);
    if (primeiro) $(".cmp-input", primeiro).focus();
  }
  function ligarSeletoresComparacao(a, b) {
    $all(".cmp-input", app).forEach((inp) => {
      const box = inp.nextElementSibling;
      const mostrar = debounce(() => {
        const q = inp.value.trim();
        if (q.length < 2) { box.innerHTML = ""; return; }
        const ids = [];
        buscarMedicamentos(q).forEach((id) => { if (!ids.includes(id)) ids.push(id); });
        buscarPorNomeComercial(q).forEach((c) => { if (!ids.includes(c.medId)) ids.push(c.medId); });
        box.innerHTML = ids.slice(0, 8).map((id) => `<button type="button" data-id="${id}"><b>${esc(MEDICAMENTOS[id].nomeGenerico)}</b><small>${esc(MEDICAMENTOS[id].classeTerapeutica || "")}</small></button>`).join("") ||
          `<div class="cmp-sem">Nenhum fármaco encontrado</div>`;
      }, 140);
      inp.addEventListener("input", mostrar);
      box.addEventListener("click", (ev) => {
        const btn = ev.target.closest("button[data-id]"); if (!btn) return;
        const id = btn.dataset.id;
        const na = inp.dataset.slot === "a" ? id : a, nb = inp.dataset.slot === "b" ? id : b;
        irPara(`#/comparar/${na || ""}/${nb || ""}`);
      });
      inp.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter") { const f = $("button[data-id]", box); if (f) f.click(); }
      });
    });
  }
  window.limparComparacao = function (slot) {
    const partes = decodeURIComponent(location.hash).replace("#/comparar", "").split("/").filter((x, i) => i > 0);
    const a = partes[0] || "", b = partes[1] || "";
    irPara(`#/comparar/${slot === "a" ? "" : a}/${slot === "b" ? "" : b}`);
  };
  window.compararCom = function (medId) { irPara(`#/comparar/${medId}/`); };

  // ---------- Cartão de orientação ao paciente ----------
  const CARTAO_ITENS = [
    ["comoTomar", "💊", "Como tomar"],
    ["esquecimento", "⏰", "Esqueceu uma dose?"],
    ["alimentos", "🍽️", "Alimentos"],
    ["alcool", "🍷", "Bebida alcoólica"],
    ["dirigir", "🚗", "Dirigir e máquinas"],
    ["sinaisAlerta", "🚨", "Procure atendimento se"],
  ];
  const PROF_KEY = "fp-etiqueta-profissional"; // compartilhado com a etiqueta do Cálculo de Doses
  let cartaoMedId = null;
  function lerProf() { try { return JSON.parse(localStorage.getItem(PROF_KEY) || "{}"); } catch (e) { return {}; } }
  function garantirModalCartao() {
    if ($("#cartao-overlay")) return;
    const div = document.createElement("div");
    div.innerHTML = `
      <div class="cartao-overlay" id="cartao-overlay" role="dialog" aria-modal="true" aria-labelledby="cartao-titulo">
        <div class="cartao-modal">
          <div class="cartao-modal-cab"><h3 id="cartao-titulo">Cartão de orientação ao paciente</h3><button type="button" class="cartao-fechar" aria-label="Fechar" onclick="fecharCartaoPaciente()">✕</button></div>
          <div class="cartao-modal-corpo">
            <div class="cartao-campos">
              <label>Drogaria / farmácia<input id="cartao-drogaria" type="text" autocomplete="off" placeholder="Nome do estabelecimento"></label>
              <label>Paciente (opcional)<input id="cartao-paciente" type="text" autocomplete="off"></label>
              <label>Farmacêutico(a)<input id="cartao-prof" type="text" autocomplete="off"></label>
              <label>CRF<input id="cartao-crf" type="text" autocomplete="off" placeholder="CRF-UF 0000"></label>
              <label>Telefone para dúvidas<input id="cartao-tel" type="text" autocomplete="off" placeholder="(00) 00000-0000"></label>
              <div class="cartao-botoes">
                <button type="button" class="cartao-btn" onclick="copiarCartaoPaciente(this)">Copiar texto (WhatsApp)</button>
                <button type="button" class="cartao-btn primario" onclick="imprimirCartaoPaciente()">Imprimir</button>
              </div>
            </div>
            <div class="cartao-preview-wrap"><div id="cartao-preview"></div></div>
          </div>
        </div>
      </div>
      <div id="cartao-print-area"></div>`;
    while (div.firstElementChild) document.body.appendChild(div.firstElementChild);
    $("#cartao-overlay").addEventListener("click", (e) => { if (e.target.id === "cartao-overlay") fecharCartaoPaciente(); });
    $all(".cartao-campos input").forEach((el) => el.addEventListener("input", renderCartaoPaciente));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && $("#cartao-overlay").classList.contains("aberto")) fecharCartaoPaciente(); });
  }
  function renderCartaoPaciente() {
    const m = MEDICAMENTOS[cartaoMedId]; if (!m) return;
    const o = m.orientacoesPaciente || {};
    const v = (id) => ($("#" + id).value || "").trim();
    const drog = v("cartao-drogaria"), pac = v("cartao-paciente"), prof = v("cartao-prof"), crf = v("cartao-crf"), tel = v("cartao-tel");
    $("#cartao-preview").innerHTML = `
      <div class="cartao-papel">
        <div class="cp-cab"><span class="cp-drog">${drog ? esc(drog) : "Farma<b>Prática</b>"}</span><span>${new Date().toLocaleDateString("pt-BR")}</span></div>
        ${pac ? `<div class="cp-pac">Para: <b>${esc(pac)}</b></div>` : ""}
        <div class="cp-med">${esc(m.nomeGenerico)}</div>
        <div class="cp-classe">${esc(m.classeTerapeutica || "")}</div>
        <div class="cp-grade">
          ${CARTAO_ITENS.filter(([k]) => o[k]).map(([k, ico, rot]) => `<div class="cp-item${k === "sinaisAlerta" ? " cp-alerta" : ""}"><div class="cp-ico">${ico}</div><div><b>${rot}</b><p>${esc(o[k])}</p></div></div>`).join("")}
        </div>
        <div class="cp-rod">${prof || crf || tel ? `Dúvidas? Fale com ${prof ? "o(a) farmacêutico(a) <b>" + esc(prof) + "</b>" : "o farmacêutico"}${crf ? " · " + esc(crf) : ""}${tel ? " · " + esc(tel) : ""}.` : "Dúvidas? Fale com o farmacêutico."} Este cartão não substitui a bula nem a orientação do prescritor.</div>
      </div>`;
  }
  window.abrirCartaoPaciente = function (medId) {
    garantirModalCartao();
    cartaoMedId = medId;
    const p = lerProf();
    $("#cartao-drogaria").value = p.drogaria || "";
    $("#cartao-prof").value = p.nome || "";
    $("#cartao-crf").value = p.crf || "";
    $("#cartao-tel").value = p.telefone || "";
    $("#cartao-paciente").value = "";
    renderCartaoPaciente();
    $("#cartao-overlay").classList.add("aberto");
  };
  window.fecharCartaoPaciente = function () { const o = $("#cartao-overlay"); if (o) o.classList.remove("aberto"); };
  function salvarProf() {
    const p = lerProf();
    p.drogaria = $("#cartao-drogaria").value.trim(); p.nome = $("#cartao-prof").value.trim();
    p.crf = $("#cartao-crf").value.trim(); p.telefone = $("#cartao-tel").value.trim();
    try { localStorage.setItem(PROF_KEY, JSON.stringify(p)); } catch (e) {}
  }
  window.imprimirCartaoPaciente = function () {
    salvarProf();
    const area = $("#cartao-print-area");
    area.innerHTML = $("#cartao-preview").innerHTML;
    document.body.classList.add("imprimindo-cartao");
    const limpar = () => { document.body.classList.remove("imprimindo-cartao"); area.innerHTML = ""; window.removeEventListener("afterprint", limpar); };
    window.addEventListener("afterprint", limpar);
    window.print();
    setTimeout(() => { if (!matchMedia("print").matches) limpar(); }, 1500);
  };
  window.copiarCartaoPaciente = function (btn) {
    salvarProf();
    const m = MEDICAMENTOS[cartaoMedId]; const o = m.orientacoesPaciente || {};
    const drog = $("#cartao-drogaria").value.trim(), pac = $("#cartao-paciente").value.trim();
    const txt = [
      drog ? `*${drog}*` : "",
      pac ? `Orientações para ${pac}` : "Orientações de uso",
      `*${m.nomeGenerico}*`,
      "",
      ...CARTAO_ITENS.filter(([k]) => o[k]).map(([k, ico, rot]) => `${ico} *${rot}:* ${o[k]}`),
      "",
      "Dúvidas? Fale com o farmacêutico. Estas orientações não substituem a bula nem a orientação do prescritor.",
    ].filter((l, i) => l !== "" || i > 2).join("\n");
    const ok = () => { const t = btn.textContent; btn.textContent = "Copiado ✓"; setTimeout(() => (btn.textContent = t), 1600); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(txt).then(ok).catch(() => {});
    else { const ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); ok(); } catch (e) {} ta.remove(); }
  };

  function ativarObservadorSecoes() {
    const secoesEls = $all(".ficha-secao", app);
    if (!secoesEls.length || !("IntersectionObserver" in window)) return;
    const links = $all('a[data-target]', app);
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            links.forEach((l) => l.classList.toggle("ativo", l.dataset.target === id));
          }
        });
      },
      { rootMargin: "-15% 0px -70% 0px", threshold: 0 }
    );
    secoesEls.forEach((el) => observer.observe(el));
  }

  /* ---------------------------------------------------------------------
     Cabeçalho: título central + busca + menu mobile
  --------------------------------------------------------------------- */
  function setTituloTopo(titulo, descricao) {
    const t = $(".titulo-principal");
    const d = $(".titulo-descricao");
    if (t) t.textContent = titulo;
    if (d) d.textContent = descricao || "";
  }

  // Contador persistente no cabeçalho (independente da rota atual) com o
  // progresso de preenchimento das fichas farmacoterapêuticas completas.
  function atualizarContadorCompletos() {
    const el = $("#contador-completos");
    if (!el) return;
    const total = Object.keys(MEDICAMENTOS).length;
    const completos = Object.values(MEDICAMENTOS).filter(fichaCompleta).length;
    el.textContent = `${completos.toLocaleString("pt-BR")} de ${total.toLocaleString("pt-BR")} catalogados`;
  }

  function initBusca() {
    const inputMed = $("#busca-medicamento");
    const clearMed = $("#clear-busca-medicamento");
    const box = $("#bx-sugestoes");
    let itens = [], sel = -1;

    function fechar() { box.hidden = true; inputMed.setAttribute("aria-expanded", "false"); sel = -1; }
    function marcar(i) {
      const els = $all(".bx-sug", box);
      els.forEach((e, k) => e.classList.toggle("ativo", k === i));
      if (els[i]) { els[i].scrollIntoView({ block: "nearest" }); inputMed.setAttribute("aria-activedescendant", els[i].id); }
      sel = i;
    }
    function abrir(i) {
      const it = itens[i];
      if (!it) return;
      fechar();
      if (it.href) irPara(it.href); else if (it.fn) it.fn();
    }
    function sugerir() {
      const q = inputMed.value.trim();
      clearMed.hidden = !q;
      if (q.length < 2) { fechar(); return; }
      const meds = buscarRanqueado(q, 6);
      const coms = buscarComerciaisRanqueado(q, 4).filter((c) => !meds.includes(c.medId));
      const grps = buscarGrupos(q).slice(0, 3);
      itens = [];
      let html = "";
      const sec = (t) => `<div class="bx-sug-titulo">${t}</div>`;
      if (meds.length) {
        html += sec("Medicamentos");
        meds.forEach((id) => {
          const m = MEDICAMENTOS[id]; const k = itens.length;
          itens.push({ href: "#/medicamento/" + id });
          html += `<div class="bx-sug" id="bx-sug-${k}" role="option" data-i="${k}" data-cor="${MED_GRUPO_COR[id] || ""}"><span class="med-avatar">${esc(iniciais(m.nomeGenerico))}</span><span class="bx-sug-txt"><strong>${destacar(m.nomeGenerico, q)}</strong><small>${esc(m.classeTerapeutica || "")}</small></span></div>`;
        });
      }
      if (coms.length) {
        html += sec("Nomes comerciais");
        coms.forEach((c) => {
          const m = MEDICAMENTOS[c.medId]; const k = itens.length;
          itens.push({ href: "#/medicamento/" + c.medId });
          html += `<div class="bx-sug" id="bx-sug-${k}" role="option" data-i="${k}" data-cor="${MED_GRUPO_COR[c.medId] || ""}"><span class="bx-sug-tag">®</span><span class="bx-sug-txt"><strong>${destacar(c.nome, q)}</strong><small>→ ${esc(m.principioAtivo || m.nomeGenerico)}</small></span></div>`;
        });
      }
      if (grps.length) {
        html += sec("Grupos e classes");
        grps.forEach((r) => {
          const k = itens.length;
          itens.push({ fn: () => window.bxAbrirGrupo(r.grupo.id, r.tipo === "subclasse" ? r.idx : -1) });
          html += `<div class="bx-sug" id="bx-sug-${k}" role="option" data-i="${k}" data-cor="${r.grupo.cor}"><span class="bx-sug-tag bx-sug-emoji">${r.grupo.icone}</span><span class="bx-sug-txt"><strong>${destacar(r.nome, q)}</strong><small>${r.total} medicamento${r.total === 1 ? "" : "s"}</small></span></div>`;
        });
      }
      const k = itens.length;
      itens.push({ href: "#/busca/" + encodeURIComponent(q) });
      html += `<div class="bx-sug bx-sug-todos" id="bx-sug-${k}" role="option" data-i="${k}">${'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'}<span>Ver todos os resultados para “${esc(q)}”</span><kbd>Enter</kbd></div>`;
      box.innerHTML = html;
      box.hidden = false;
      inputMed.setAttribute("aria-expanded", "true");
      sel = -1;
    }

    inputMed.addEventListener("input", debounce(sugerir, 90));
    inputMed.addEventListener("focus", () => { if (inputMed.value.trim().length >= 2) sugerir(); });
    inputMed.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" && !box.hidden) { e.preventDefault(); marcar(Math.min(sel + 1, itens.length - 1)); }
      else if (e.key === "ArrowUp" && !box.hidden) { e.preventDefault(); marcar(Math.max(sel - 1, 0)); }
      else if (e.key === "Escape") { if (!box.hidden) fechar(); else inputMed.blur(); }
      else if (e.key === "Enter") {
        e.preventDefault();
        const q = inputMed.value.trim();
        if (!box.hidden && sel >= 0) abrir(sel);
        else if (q) { fechar(); ESCOPO_BUSCA = "tudo"; irPara("#/busca/" + encodeURIComponent(q)); }
      }
    });
    box.addEventListener("mousedown", (e) => {
      const el = e.target.closest(".bx-sug");
      if (!el) return;
      e.preventDefault();
      abrir(+el.dataset.i);
    });
    box.addEventListener("mousemove", (e) => {
      const el = e.target.closest(".bx-sug");
      if (el && +el.dataset.i !== sel) marcar(+el.dataset.i);
    });
    document.addEventListener("click", (e) => { if (!e.target.closest("#bx-search")) fechar(); });
    clearMed.addEventListener("click", () => {
      inputMed.value = "";
      clearMed.hidden = true;
      fechar();
      inputMed.focus();
      if (location.hash.startsWith("#/busca/")) irPara("#/");
    });
    // Atalhos: "/" ou Ctrl/⌘+K focam a busca
    document.addEventListener("keydown", (e) => {
      const tag = (e.target.tagName || "").toLowerCase();
      const digitando = tag === "input" || tag === "textarea" || tag === "select" || e.target.isContentEditable;
      if ((e.key === "/" && !digitando) || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k")) {
        e.preventDefault(); inputMed.focus(); inputMed.select();
      }
    });
    // Mantém o texto da busca sincronizado com a rota
    window.addEventListener("hashchange", () => {
      fechar();
      const h = decodeURIComponent(location.hash || "");
      if (h.startsWith("#/busca/")) { inputMed.value = h.replace("#/busca/", ""); clearMed.hidden = false; }
      else if (document.activeElement !== inputMed) { inputMed.value = ""; clearMed.hidden = true; }
    });
  }

  /* ---------------------------------------------------------------------
     Tema (claro/escuro) — 20/10/2026: inicia sempre em modo escuro por
     padrão. A preferência salva em localStorage('farmapratica-theme') é
     lida de volta logo após a abertura do <body> (script inline no HTML),
     e este toggle grava a escolha para as próximas visitas.
  --------------------------------------------------------------------- */
  window.toggleTheme = function () {
    document.body.classList.toggle("light");
    try{ localStorage.setItem('farmapratica-theme', document.body.classList.contains('light') ? 'light' : 'dark'); }catch(e){}
  };

  /* ---------------------------------------------------------------------
     Inicialização
  --------------------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", () => {
    buildSearchIndex();
    initBusca();
    atualizarContadorCompletos();
    route();
  });
})();
