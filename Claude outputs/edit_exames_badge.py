import sys

path = "exames/index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected 1 occurrence, found {count}"
    return content.replace(old, new, 1)

# 1) CSS: add badge styles right after .titulo-descricao rule
old_css = "  .titulo-descricao{ font-size:.76rem; color:var(--text-dim); margin-top:3px; max-width:560px; }\n"
new_css = old_css + "  .exame-count-badge{ display:inline-flex; align-items:center; gap:6px; margin-top:7px; padding:3px 11px; border-radius:999px; background:var(--red-glow); border:1px solid rgba(228,23,44,.35); color:var(--red-bright); font-size:.72rem; font-weight:700; letter-spacing:.02em; }\n  .exame-count-badge svg{ width:13px; height:13px; }\n"
content = replace_once(content, old_css, new_css, "css")

# 2) HTML: insert badge after titulo-descricao div in the header
old_html = '    <div class="titulo-descricao">Consulta rápida a valores de referência, interpretação clínica e interações com medicamentos</div>\n'
new_html = old_html + '    <div class="exame-count-badge" id="exame-count-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v7.31"/><path d="M14 9.3V1.99"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.58 16.5h12.85"/></svg><span id="exame-count-num">—</span> exames no banco</div>\n'
content = replace_once(content, old_html, new_html, "html")

# 3) JS: populate the count once data loads, inside init()
old_js = "function init(){\n  loadStorage();"
new_js = "function init(){\n  loadStorage();\n  const ecEl = document.getElementById('exame-count-num'); if(ecEl) ecEl.textContent = DATA.exames.length;"
content = replace_once(content, old_js, new_js, "js")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK: badge de contagem de exames aplicado (CSS + HTML + JS).")
