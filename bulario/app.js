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
     Armazenamento local (favoritos / histórico)
  --------------------------------------------------------------------- */
  const LS_FAV = "fp-bulario-favoritos";
  const LS_HIST = "fp-bulario-recentes";
  const HIST_MAX = 8;

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
  function toggleFavorito(id) {
    let favs = getFavoritos();
    if (favs.includes(id)) {
      favs = favs.filter((f) => f !== id);
    } else {
      favs.unshift(id);
    }
    setFavoritos(favs);
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

  function buscarMedicamentos(query) {
    const q = normalize(query);
    if (!q) return [];
    return SEARCH_INDEX.filter((entry) => entry.texto.includes(q)).map((e) => e.id);
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

  function route() {
    const hash = decodeURIComponent(location.hash || "");
    window.scrollTo({ top: 0 });
    if (hash.startsWith("#/grupo/")) {
      const id = hash.replace("#/grupo/", "");
      renderGrupo(id);
    } else if (hash.startsWith("#/medicamento/")) {
      const id = hash.replace("#/medicamento/", "");
      renderFicha(id);
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

  function medItemButton(medId) {
    const m = MEDICAMENTOS[medId];
    if (!m) return "";
    const fav = isFavorito(medId) ? "star-on" : "";
    return `
      <button class="med-item" data-med="${medId}" onclick="irPara('#/medicamento/${medId}')">
        <span class="med-item-main">
          <span class="med-item-nome">${esc(m.nomeGenerico)}</span>
          <span class="med-item-sub">${esc(m.classeTerapeutica || "")}</span>
        </span>
        <span class="med-item-fav ${fav}" title="Favorito" aria-hidden="true">★</span>
      </button>`;
  }

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
    setTituloTopo("Bulário Farmacêutico", "Consulte informações farmacológicas, clínicas e farmacoterapêuticas de medicamentos de forma rápida e organizada.");
    const favs = getFavoritos().filter((id) => MEDICAMENTOS[id]);
    const recentes = getRecentes().filter((id) => MEDICAMENTOS[id]);

    const gruposFiltrados = filtroGrupo
      ? GRUPOS.filter((g) => normalize(g.nome).includes(normalize(filtroGrupo)))
      : GRUPOS;

    app.innerHTML = `
      <div class="home-view">
        ${
          favs.length
            ? `<section class="quick-section">
                <h2>⭐ Meus Medicamentos</h2>
                <div class="med-list-flat">${favs.map(medItemButton).join("")}</div>
              </section>`
            : ""
        }
        ${
          recentes.length
            ? `<section class="quick-section">
                <h2>🕘 Recentemente Consultados</h2>
                <div class="med-list-flat">${recentes.map(medItemButton).join("")}</div>
              </section>`
            : ""
        }
        <section class="quick-section">
          <h2>Grupos Farmacológicos</h2>
          <div class="grupos-grid" id="grupos-grid">
            ${gruposFiltrados.map(grupoCard).join("") || `<p class="empty-msg">Nenhum grupo encontrado para esse filtro.</p>`}
          </div>
        </section>
      </div>`;
  }

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
            <div class="subclasse-bloco">
              <button class="subclasse-header" data-open="${i === 0 ? "true" : "false"}" onclick="this.parentElement.classList.toggle('aberto'); this.setAttribute('data-open', this.parentElement.classList.contains('aberto'))">
                <span>${esc(s.nome)}</span>
                <span class="subclasse-count">${s.medicamentos.length}</span>
              </button>
              <div class="subclasse-itens">
                <div class="med-list-flat">${s.medicamentos.map(medItemButton).join("")}</div>
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
  function renderBusca(query) {
    setTituloTopo("Resultado da busca", `"${query}"`);
    const idsGenericos = buscarMedicamentos(query);
    const comerciais = buscarPorNomeComercial(query);

    let html = `<div class="busca-view"><a href="#/" class="btn-voltar">‹ Voltar</a>`;
    html += `<h1 class="grupo-titulo">Resultados para "${esc(query)}"</h1>`;

    if (!idsGenericos.length && !comerciais.length) {
      html += `<p class="empty-msg">Nenhum medicamento encontrado. Tente buscar pelo princípio ativo, nome comercial ou classe farmacológica.</p>`;
    }

    if (idsGenericos.length) {
      html += `<section class="quick-section"><h2>Medicamentos</h2><div class="med-list-flat">${idsGenericos.map(medItemButton).join("")}</div></section>`;
    }

    if (comerciais.length) {
      html += `<section class="quick-section"><h2>Nomes comerciais encontrados</h2><div class="comercial-list">`;
      comerciais.forEach((c) => {
        const m = MEDICAMENTOS[c.medId];
        html += `
          <button class="comercial-item" onclick="irPara('#/medicamento/${c.medId}')">
            <span class="comercial-nome">${esc(c.nome)}</span>
            <span class="comercial-seta" aria-hidden="true">→</span>
            <span class="comercial-generico">${esc(m.principioAtivo)}</span>
          </button>`;
      });
      html += `</div></section>`;
    }

    html += `</div>`;
    app.innerHTML = html;
  }

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

  function secoesFicha(m) {
    const secoes = [];

    secoes.push({
      id: "nomes-comerciais",
      titulo: "Nomes Comerciais",
      html: `
        ${m.nomesComerciais && m.nomesComerciais.referencia ? `<p><strong>Referência:</strong> ${esc(m.nomesComerciais.referencia)}</p>` : ""}
        ${m.nomesComerciais && m.nomesComerciais.similares && m.nomesComerciais.similares.length ? `<p><strong>Similares/genéricos de marca:</strong> ${m.nomesComerciais.similares.map(esc).join(", ")}</p>` : ""}
      `,
    });

    secoes.push({
      id: "generico-farmacia-popular",
      titulo: "Genérico / Farmácia Popular",
      html: `
        <p><strong>Medicamento genérico disponível:</strong> ${m.generico ? "Sim" : "Não"}</p>
        <p><strong>Medicamento similar disponível:</strong> ${m.similar ? "Sim" : "Não"}</p>
        <p><strong>Disponível no Programa Farmácia Popular:</strong> ${m.farmaciaPopular ? "Sim" : "Não"}</p>
      `,
    });

    secoes.push({
      id: "classe",
      titulo: "Classe Terapêutica e Farmacológica",
      html: `
        ${m.classeTerapeutica ? `<p><strong>Classe terapêutica:</strong> ${esc(m.classeTerapeutica)}</p>` : ""}
        ${m.classeFarmacologica ? `<p><strong>Classe farmacológica:</strong> ${esc(m.classeFarmacologica)}</p>` : ""}
        ${m.subclasse ? `<p><strong>Subclasse:</strong> ${esc(m.subclasse)}</p>` : ""}
      `,
    });

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

    if (m.alertasFarmaceuticos && m.alertasFarmaceuticos.length) {
      secoes.push({
        id: "alertas",
        titulo: "Alertas Farmacêuticos",
        html: `<div class="alerta-box"><h3>⚠️ Alertas Farmacêuticos</h3>${listaOuTexto(m.alertasFarmaceuticos)}</div>`,
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
      secoes.push({ id: "gestacao", titulo: "🤰 Gestação", html: `<p>${esc(m.gestacao)}</p>` });
    }
    if (m.lactacao) {
      secoes.push({ id: "lactacao", titulo: "🤱 Lactação", html: `<p>${esc(m.lactacao)}</p>` });
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
          ${m.dispensacao ? `<p><strong>Sujeito a controle especial:</strong> ${m.dispensacao.controleEspecial ? "Sim" : "Não"}</p><p><strong>Retenção de receita:</strong> ${m.dispensacao.retencaoReceita ? "Sim" : "Não"}</p><p><strong>Condições de dispensação:</strong> ${esc(m.dispensacao.condicoes)}</p>` : ""}
        `,
      });
    }

    if (m.referencias && m.referencias.length) {
      secoes.push({
        id: "referencias",
        titulo: "Referências Bibliográficas",
        html: `${listaOuTexto(m.referencias)}<p class="texto-dim"><strong>Última atualização:</strong> ${esc(m.ultimaAtualizacao || NAO_DISPONIVEL)}</p>`,
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
            <button class="btn-favoritar ${fav ? "ativo" : ""}" id="btn-fav" title="Favoritar medicamento" aria-label="Favoritar medicamento">
              <span class="estrela">★</span><span class="btn-favoritar-label">${fav ? "Favoritado" : "Favoritar"}</span>
            </button>
          </div>
          ${tagsHtml(m.tags)}
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
            ${secoes.map((s) => `<section id="sec-${s.id}" class="ficha-secao"><h2>${esc(s.titulo)}</h2>${s.html}</section>`).join("")}
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
          const y = target.getBoundingClientRect().top + window.scrollY - 14;
          window.scrollTo({ top: y, behavior: "smooth" });
        }
      });
    });

    ativarObservadorSecoes();
  }

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

  function initBusca() {
    const inputMed = $("#busca-medicamento");
    const inputGrupo = $("#busca-grupo");
    const clearMed = $("#clear-busca-medicamento");

    const executarBuscaMedicamento = debounce(() => {
      const q = inputMed.value.trim();
      clearMed.hidden = !q;
      if (!q) {
        if (location.hash.startsWith("#/busca/")) irPara("#/");
        return;
      }
      irPara("#/busca/" + encodeURIComponent(q));
    }, 220);

    inputMed.addEventListener("input", executarBuscaMedicamento);
    inputMed.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const q = inputMed.value.trim();
        if (q) irPara("#/busca/" + encodeURIComponent(q));
      }
    });
    clearMed.addEventListener("click", () => {
      inputMed.value = "";
      clearMed.hidden = true;
      inputMed.focus();
      if (location.hash.startsWith("#/busca/")) irPara("#/");
    });

    inputGrupo.addEventListener(
      "input",
      debounce(() => {
        if (!location.hash || location.hash === "#/" || location.hash === "") {
          renderHome(inputGrupo.value.trim());
        } else {
          irPara("#/");
          setTimeout(() => renderHome(inputGrupo.value.trim()), 0);
        }
      }, 150)
    );
  }

  /* ---------------------------------------------------------------------
     Tema (claro/escuro) — inicia sempre em modo claro, como as demais
     ferramentas do FarmaPrática.
  --------------------------------------------------------------------- */
  window.toggleTheme = function () {
    document.body.classList.toggle("light");
  };

  /* ---------------------------------------------------------------------
     Inicialização
  --------------------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", () => {
    buildSearchIndex();
    initBusca();
    route();
  });
})();
