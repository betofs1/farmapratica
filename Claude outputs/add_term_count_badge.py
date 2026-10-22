import re, sys, io

PATH = "dicionario/index.html"
with io.open(PATH, encoding="utf-8") as f:
    content = f.read()

def count_divs(s):
    return len(re.findall(r'<div\b', s)), s.count('</div>')

before_open, before_close = count_divs(content)

# 1. CSS: add badge style right after .titulo-descricao rule
old_css = '  .titulo-descricao{ font-size:.76rem; color:var(--text-dim); margin-top:3px; max-width:560px; }\n'
assert content.count(old_css) == 1, f"CSS anchor not found exactly once: {content.count(old_css)}"
new_css = old_css + '  .termo-count-badge{ display:inline-flex; align-items:center; gap:6px; margin-top:7px; padding:3px 11px; border-radius:999px; background:var(--red-glow); border:1px solid rgba(228,23,44,.35); color:var(--red-bright); font-size:.72rem; font-weight:700; letter-spacing:.02em; }\n  .termo-count-badge svg{ width:13px; height:13px; }\n'
content = content.replace(old_css, new_css, 1)

# 2. HTML: insert badge placeholder right after .titulo-descricao div, still inside .titulo-central
old_html = '    <div class="titulo-descricao">Consulta técnica e didática de termos de farmacologia, farmácia clínica e prática profissional</div>\n'
assert content.count(old_html) == 1, f"HTML anchor not found exactly once: {content.count(old_html)}"
new_html = old_html + '    <div class="termo-count-badge" id="termo-count-badge">' + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>' + '<span id="termo-count-num">—</span> termos no banco</div>\n'
content = content.replace(old_html, new_html, 1)

# 3. JS: update the badge once DATA loads, inside the fetch().then() callback
old_js = "  DATA.comparacoes.forEach(c=>COMP_BY_ID[c.id]=c);\n  loadHistorico();"
assert content.count(old_js) == 1, f"JS anchor not found exactly once: {content.count(old_js)}"
new_js = "  DATA.comparacoes.forEach(c=>COMP_BY_ID[c.id]=c);\n  const tcEl = document.getElementById('termo-count-num'); if(tcEl) tcEl.textContent = DATA.termos.length;\n  loadHistorico();"
content = content.replace(old_js, new_js, 1)

after_open, after_close = count_divs(content)
added_divs = after_open - before_open
added_closes = after_close - before_close
assert added_divs == added_closes, f"Div balance broken: +{added_divs} opens vs +{added_closes} closes"
assert added_divs == 1, f"Expected to add exactly 1 new <div> (badge wrapper), got {added_divs}"

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK. div balance delta: +{added_divs} opens / +{added_closes} closes (ambos iguais, consistente)")
