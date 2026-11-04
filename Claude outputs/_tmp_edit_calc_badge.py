import io

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected exactly 1 occurrence, found {count}"
    return content.replace(old, new, 1)

# 1) CSS: badge style, placed right after the .titulo-descricao rule.
old_css = """  .topbar-app .titulo-descricao{
    font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
    font-size: .74rem;
    color: var(--text-dim);
    margin-top:2px;
    white-space:nowrap;
  }"""
new_css = """  .topbar-app .titulo-descricao{
    font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
    font-size: .74rem;
    color: var(--text-dim);
    margin-top:2px;
    white-space:nowrap;
  }
  .calc-count-badge{
    display:inline-flex; align-items:center; gap:6px; margin-top:7px;
    padding:3px 11px; border-radius:999px;
    background:var(--red-glow); border:1px solid rgba(228,23,44,.35);
    color:var(--red-bright); font-size:.72rem; font-weight:700; letter-spacing:.02em;
  }
  .calc-count-badge svg{ width:13px; height:13px; }"""
content = replace_once(content, old_css, new_css, "css-badge")

# 2) HTML: badge markup, right after the .titulo-descricao div.
old_html = """    <div class="titulo-principal">CALCULADORA <span class="titulo-accent">DE DOSES</span></div>
    <div class="titulo-descricao">Cálculo de doses por peso e idade (pediátrico e adulto) com base em bulas e diretrizes atualizadas</div>
  </div>"""
new_html = """    <div class="titulo-principal">CALCULADORA <span class="titulo-accent">DE DOSES</span></div>
    <div class="titulo-descricao">Cálculo de doses por peso e idade (pediátrico e adulto) com base em bulas e diretrizes atualizadas</div>
    <div class="calc-count-badge" id="calc-count-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg><span id="calc-count-num">—</span> medicamentos disponíveis</div>
  </div>"""
content = replace_once(content, old_html, new_html, "html-badge")

# 3) JS: populate the count once DB loads.
old_js = """fetch('dados.json')
  .then(r => r.json())
  .then(data => {
    DB = data;
    renderSidebar();"""
new_js = """fetch('dados.json')
  .then(r => r.json())
  .then(data => {
    DB = data;
    const ccEl = document.getElementById('calc-count-num');
    if(ccEl) ccEl.textContent = (DB.farmacos || []).length;
    renderSidebar();"""
content = replace_once(content, old_js, new_js, "js-count")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - count badge added to Calculadora de Doses")
