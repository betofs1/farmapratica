import io

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected exactly 1 occurrence, found {count}"
    return content.replace(old, new, 1)

old = """  .cat-header{
    display:flex; align-items:center; gap:9px; width:100%; text-align:left;
    background:linear-gradient(180deg, var(--card-hover), var(--panel)); border:1px solid var(--border); border-left:3px solid var(--cc, var(--red-bright));
    border-radius:9px; padding:9px 11px; margin:0; cursor:pointer;
    font-size:.72rem; text-transform:uppercase; letter-spacing:.5px; font-weight:800; color:var(--text-gray);
    transition:transform .12s ease, box-shadow .12s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.28), inset 0 -2px 3px rgba(0,0,0,.1), 0 2px 5px rgba(0,0,0,.18);
  }
  .cat-header:hover{ transform:translateY(-1px); }
  .cat-header .cat-emoji{ font-size:.95rem; flex-shrink:0; }
  .cat-header .cat-nome{ flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--cc, var(--text-gray)); }
  .cat-header .cat-count{ font-size:.64rem; font-weight:700; background:var(--cg, var(--hover-tint)); color:var(--cc, var(--text-dim)); padding:2px 8px; border-radius:20px; flex-shrink:0; }
  .cat-header .cat-chevron{ flex-shrink:0; width:13px; height:13px; transition:transform .2s ease; opacity:.75; color:var(--cc,var(--text-dim)); }
  .cat-header.aberto .cat-chevron{ transform:rotate(90deg); }
  .cat-quiz-btn{
    position:absolute; top:-9px; left:16px; z-index:2;
    display:flex; align-items:center; gap:4px;
    background:linear-gradient(180deg,var(--red-bright),var(--red-dark));
    color:#fff; font-size:.6rem; font-weight:800; letter-spacing:.6px; text-transform:uppercase;
    padding:3px 10px; border-radius:20px; border:none; cursor:pointer;
    box-shadow:0 2px 7px var(--red-glow), 0 1px 3px rgba(0,0,0,.35);
    transition:transform .12s ease, box-shadow .12s ease;
  }"""

new = """  .cat-header{
    display:flex; align-items:center; gap:9px; width:100%; text-align:left;
    background:linear-gradient(180deg, var(--card-hover), var(--panel)); border:1px solid var(--border); border-left:3px solid var(--cc, var(--red-bright));
    border-radius:9px; padding:9px 60px 9px 11px; margin:0; cursor:pointer;
    font-size:.72rem; text-transform:uppercase; letter-spacing:.5px; font-weight:800; color:var(--text-gray);
    transition:transform .12s ease, box-shadow .12s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.28), inset 0 -2px 3px rgba(0,0,0,.1), 0 2px 5px rgba(0,0,0,.18);
  }
  .cat-header:hover{ transform:translateY(-1px); }
  .cat-header .cat-emoji{ font-size:.95rem; flex-shrink:0; }
  .cat-header .cat-nome{ flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--cc, var(--text-gray)); }
  .cat-header .cat-count{ font-size:.64rem; font-weight:700; background:var(--cg, var(--hover-tint)); color:var(--cc, var(--text-dim)); padding:2px 8px; border-radius:20px; flex-shrink:0; }
  .cat-header .cat-chevron{ flex-shrink:0; width:13px; height:13px; transition:transform .2s ease; opacity:.75; color:var(--cc,var(--text-dim)); }
  .cat-header.aberto .cat-chevron{ transform:rotate(90deg); }
  /* 01/11/2026: QUIZ deixou de flutuar sobre o canto superior esquerdo do botão (ficava
     meio solto, longe da contagem) e passou a ficar encostado no final do botão, ao lado
     da contagem/seta — a faixa de padding-right reservada em .cat-header acima abre espaço
     pra ele sem sobrepor o nome da categoria. */
  .cat-quiz-btn{
    position:absolute; top:50%; right:9px; transform:translateY(-50%); z-index:2;
    display:flex; align-items:center; gap:4px;
    background:linear-gradient(180deg,var(--red-bright),var(--red-dark));
    color:#fff; font-size:.6rem; font-weight:800; letter-spacing:.6px; text-transform:uppercase;
    padding:3px 10px; border-radius:20px; border:none; cursor:pointer;
    box-shadow:0 2px 7px var(--red-glow), 0 1px 3px rgba(0,0,0,.35);
    transition:transform .12s ease, box-shadow .12s ease;
  }"""

content = replace_once(content, old, new, "quiz-btn-reposition")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - QUIZ badge repositioned to the end of the row")
