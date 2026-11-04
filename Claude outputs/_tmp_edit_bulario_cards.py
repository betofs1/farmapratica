import io

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected exactly 1 occurrence, found {count}"
    return content.replace(old, new, 1)

# 1) Modernize .grupo-card: rounded icon badge with color glow (same visual language
#    already used for .ct-icon in Dicionário/Exames), softer shadow, nicer hover lift.
old_card = """  /* ================= Grid de grupos (Nível 1) ================= */
  .grupos-grid{ display:grid; grid-template-columns:repeat(5,1fr); gap:10px; }
  .grupo-card{
    position:relative; text-align:left; cursor:pointer;
    display:flex; flex-direction:column; gap:4px;
    background: linear-gradient(160deg, var(--card), color-mix(in srgb, var(--card) 88%, black 12%));
    border:2px solid var(--border); border-left:3px solid var(--gc, var(--accent));
    border-radius:10px; padding:10px 10px 9px;
    box-shadow: 0 2px 0 0 color-mix(in srgb, var(--gc, var(--accent)) 45%, rgba(0,0,0,.5)), 0 2px 8px rgba(0,0,0,.12);
    transition: transform .15s ease, box-shadow .15s ease;
    min-width:0;
  }
  [data-cor="red"]{ --gc:var(--g-red); }
  [data-cor="green"]{ --gc:var(--g-green); }
  [data-cor="amber"]{ --gc:var(--g-amber); }
  [data-cor="magenta"]{ --gc:var(--g-magenta); }
  [data-cor="blue"]{ --gc:var(--g-blue); }
  [data-cor="indigo"]{ --gc:var(--g-indigo); }
  [data-cor="teal"]{ --gc:var(--g-teal); }
  [data-cor="purple"]{ --gc:var(--g-purple); }
  [data-cor="orange"]{ --gc:var(--g-orange); }
  [data-cor="sky"]{ --gc:var(--g-sky); }
  [data-cor="lime"]{ --gc:var(--g-lime); }
  .grupo-card:hover{ transform:translateY(-3px); box-shadow:0 8px 0 0 color-mix(in srgb, var(--gc, var(--accent)) 45%, rgba(0,0,0,.5)), 0 10px 18px rgba(0,0,0,.16); }
  .grupo-card:active{ transform:translateY(1px); }
  .grupo-card-icone{ font-size:1.05rem; }
  .grupo-card-nome{ font-family:'Inter',sans-serif; font-weight:700; font-size:.72rem; line-height:1.2; color:var(--text); }
  .grupo-card-count{ font-size:.6rem; color:var(--text-dim); }"""

new_card = """  /* ================= Grid de grupos (Nível 1) ================= */
  /* 01/11/2026: cards modernizados — mesmo visual de "badge de ícone" com glow colorido já
     usado no Dicionário/Exames (.ct-icon), no lugar do cartão antigo com barra lateral só. */
  .grupos-grid{ display:grid; grid-template-columns:repeat(5,1fr); gap:10px; }
  .grupo-card{
    position:relative; text-align:left; cursor:pointer;
    display:flex; flex-direction:column; gap:8px;
    background:var(--card); border:1px solid var(--border); border-top:3px solid var(--gc, var(--accent));
    border-radius:12px; padding:13px 13px 11px;
    box-shadow: 0 2px 8px rgba(0,0,0,.12);
    transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
    min-width:0;
  }
  [data-cor="red"]{ --gc:var(--g-red); }
  [data-cor="green"]{ --gc:var(--g-green); }
  [data-cor="amber"]{ --gc:var(--g-amber); }
  [data-cor="magenta"]{ --gc:var(--g-magenta); }
  [data-cor="blue"]{ --gc:var(--g-blue); }
  [data-cor="indigo"]{ --gc:var(--g-indigo); }
  [data-cor="teal"]{ --gc:var(--g-teal); }
  [data-cor="purple"]{ --gc:var(--g-purple); }
  [data-cor="orange"]{ --gc:var(--g-orange); }
  [data-cor="sky"]{ --gc:var(--g-sky); }
  [data-cor="lime"]{ --gc:var(--g-lime); }
  .grupo-card:hover{ transform:translateY(-3px); box-shadow:0 8px 20px rgba(0,0,0,.18); border-color:var(--gc, var(--accent)); }
  .grupo-card:active{ transform:translateY(1px); }
  .grupo-card-icone{
    width:32px; height:32px; border-radius:10px; flex-shrink:0;
    background:linear-gradient(145deg, color-mix(in srgb, var(--gc, var(--accent)) 26%, transparent), color-mix(in srgb, var(--gc, var(--accent)) 9%, transparent));
    border:1px solid color-mix(in srgb, var(--gc, var(--accent)) 32%, transparent);
    box-shadow:0 3px 10px color-mix(in srgb, var(--gc, var(--accent)) 26%, transparent), inset 0 1px 0 rgba(255,255,255,.12);
    display:flex; align-items:center; justify-content:center; font-size:1.05rem;
    transition:transform .18s ease, box-shadow .18s ease;
  }
  .grupo-card:hover .grupo-card-icone{ transform:scale(1.08) rotate(-3deg); }
  .grupo-card-nome{ font-family:'Inter',sans-serif; font-weight:700; font-size:.76rem; line-height:1.25; color:var(--text); }
  .grupo-card-count{ font-size:.62rem; color:var(--text-dim); font-weight:600; }"""

content = replace_once(content, old_card, new_card, "grupo-card-modernize")

# 2) Mobile: 3 cards per row (was 2 cols at <=900px and 1 col at <=480px) — merged into the
#    existing <=800px mobile block, with the card's typography/padding scaled down to fit.
old_mobile = """  /* ================= Responsivo (mobile) ================= */
  @media (max-width:900px){
    .grupos-grid{ grid-template-columns:repeat(2,1fr); }
  }
  @media (max-width:800px){
    .page-wrap{ padding:18px 16px 50px; }
    .search-bar-row{ grid-template-columns:1fr; gap:10px; top:0; }
    .ficha-menu-rapido{ display:flex; }
    .ficha-corpo{ grid-template-columns:1fr; }
    .ficha-sidebar{ display:none; }
    .lista-definicao{ grid-template-columns:1fr; }
    .reacao-freq{ width:100%; margin-right:0; }
  }
  @media (max-width:480px){
    .grupos-grid{ grid-template-columns:1fr; }
  }"""

new_mobile = """  /* ================= Responsivo (mobile) ================= */
  @media (max-width:800px){
    .page-wrap{ padding:18px 16px 50px; }
    .search-bar-row{ grid-template-columns:1fr; gap:10px; top:0; }
    .ficha-menu-rapido{ display:flex; }
    .ficha-corpo{ grid-template-columns:1fr; }
    .ficha-sidebar{ display:none; }
    .lista-definicao{ grid-template-columns:1fr; }
    .reacao-freq{ width:100%; margin-right:0; }
    /* 01/11/2026: 3 cards de grupo lado a lado no mobile (antes caíam para 2 e depois 1 por
       linha), com o conteúdo do card compactado para caber confortavelmente em 3 colunas. */
    .grupos-grid{ grid-template-columns:repeat(3,1fr); gap:7px; }
    .grupo-card{ padding:10px 8px 9px; gap:5px; }
    .grupo-card-icone{ width:27px; height:27px; border-radius:8px; font-size:.86rem; }
    .grupo-card-nome{ font-size:.64rem; line-height:1.22; }
    .grupo-card-count{ font-size:.56rem; }
  }"""

content = replace_once(content, old_mobile, new_mobile, "mobile-3-cols")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - bulario grupo-card modernized + 3-col mobile grid")
