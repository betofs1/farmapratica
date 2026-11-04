import io

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected exactly 1 occurrence, found {count}"
    return content.replace(old, new, 1)

old = """    .rail-group{
      display:grid; grid-template-columns:1fr 1fr; gap:8px;
      padding-left:0; margin-bottom:18px; align-content:start;
    }
    .rail-group::before{ display:none; }
    .rail-title{
      grid-column:1/-1; margin:0 0 8px; padding:6px 10px 6px 9px;
      border-radius:8px; border:1px solid var(--border); border-left:3px solid var(--rail-color);
      background: var(--card);
    }
    .rail-title::before{ display:none; }
    .rail-node{ margin-bottom:0; }
    .rail-node::before{ display:none; }
    .rail-card{
      flex-direction:column; align-items:flex-start; justify-content:flex-start;
      gap:6px; min-height:82px; padding:10px 10px; border-radius:14px;
    }
    .rail-card .rc-ic{
      width:26px; height:26px; border-radius:8px;
      background: var(--panel); color: var(--rail-color);
    }
    .rail-card .rc-ic .ic{ width:15px; height:15px; }
    .rail-card.active .rc-ic{ background: rgba(255,255,255,.2); color:#fff; }
    .rail-card .rc-label{ flex:none; width:100%; font-size:.72rem; line-height:1.25; }
    .rail-card .rc-ring{ align-self:flex-end; margin-top:auto; width:24px; height:24px; }"""

new = """    /* 01/11/2026: 3 cartões de categoria lado a lado no mobile (antes eram 2 por linha),
       com o conteúdo do cartão compactado para caber confortavelmente em 3 colunas. */
    .rail-group{
      display:grid; grid-template-columns:repeat(3,1fr); gap:6px;
      padding-left:0; margin-bottom:18px; align-content:start;
    }
    .rail-group::before{ display:none; }
    .rail-title{
      grid-column:1/-1; margin:0 0 8px; padding:6px 10px 6px 9px;
      border-radius:8px; border:1px solid var(--border); border-left:3px solid var(--rail-color);
      background: var(--card);
    }
    .rail-title::before{ display:none; }
    .rail-node{ margin-bottom:0; }
    .rail-node::before{ display:none; }
    .rail-card{
      flex-direction:column; align-items:flex-start; justify-content:flex-start;
      gap:5px; min-height:76px; padding:8px 8px; border-radius:12px;
    }
    .rail-card .rc-ic{
      width:22px; height:22px; border-radius:7px;
      background: var(--panel); color: var(--rail-color);
    }
    .rail-card .rc-ic .ic{ width:13px; height:13px; }
    .rail-card.active .rc-ic{ background: rgba(255,255,255,.2); color:#fff; }
    .rail-card .rc-label{ flex:none; width:100%; font-size:.62rem; line-height:1.2; }
    .rail-card .rc-ring{ align-self:flex-end; margin-top:auto; width:20px; height:20px; }"""

content = replace_once(content, old, new, "checklist-3-cols")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - checklist category cards now 3 per row on mobile")
