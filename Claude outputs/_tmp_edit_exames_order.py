import io

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected exactly 1 occurrence, found {count}"
    return content.replace(old, new, 1)

old = """function renderInicio(){
  const rapidos = DATA.exames.filter(e=>e.consultaRapida && passaAmbiente(e)).sort((a,b)=>a.nome.localeCompare(b.nome,'pt-BR'));
  let html = '<div class="intro-banner"><span class="intro-banner-icon">'+icon('flask')+'</span>'+
    '<p>Consulte exames laboratoriais, valores de referência, interpretação de resultados, interferentes e relações com medicamentos. Apoio técnico à prática farmacêutica, sem substituir avaliação clínica ou laudo laboratorial.</p></div>';

  html += '<div class="section-title">'+icon('star')+' Consulta Rápida</div>';
  html += '<div class="quick-grid">'+rapidos.map(e=>{
    const cat=getCategoria(e.categoria);
    return '<div class="quick-card" '+ccStyle(cat.cor)+' onclick="abrirExame(\\''+e.id+'\\')"><span class="qc-dot"></span><span>'+e.nome+'</span></div>';
  }).join('')+'</div>';

  if(favoritos.size){
    html += '<div class="section-title">'+icon('star')+' Seus Favoritos</div>';
    html += '<div class="quick-grid">'+[...favoritos].map(id=>getExame(id)).filter(Boolean).map(e=>{
      const cat=getCategoria(e.categoria);
      return '<div class="quick-card" '+ccStyle(cat.cor)+' onclick="abrirExame(\\''+e.id+'\\')"><span class="qc-dot"></span><span>'+e.nome+'</span></div>';
    }).join('')+'</div>';
  }

  if(historico.length){
    html += '<div class="section-title">'+icon('activity')+' Consultados recentemente</div>';
    html += '<div class="quick-grid">'+historico.map(id=>getExame(id)).filter(Boolean).map(e=>{
      const cat=getCategoria(e.categoria);
      return '<div class="quick-card" '+ccStyle(cat.cor)+' onclick="abrirExame(\\''+e.id+'\\')"><span class="qc-dot"></span><span>'+e.nome+'</span></div>';
    }).join('')+'</div>';
  }

  html += '<div class="section-title">'+icon('more')+' Categorias</div>';
  html += '<div class="tiles-grid">'+DATA.categorias.map(cat=>{
    const n = examesDaCategoria(cat.id).length;
    return '<button class="cat-tile" '+ccStyle(cat.cor)+' onclick="toggleCategoriaHome(\\''+cat.id+'\\')">'+
      '<span class="ct-icon">'+icon(cat.icone)+'</span>'+
      '<h4>'+cat.nome+'</h4>'+
      '<span class="ct-count">'+n+' exame'+(n===1?'':'s')+' cadastrado'+(n===1?'':'s')+'</span>'+
    '</button>';
  }).join('')+'</div>';

  html += '<div class="disclaimer-fixed">'+icon('alert')+' Este conteúdo é uma ferramenta de apoio técnico à prática farmacêutica. Valores de referência podem variar entre laboratórios, métodos e populações. Priorize sempre o intervalo informado pelo laboratório do paciente. Um resultado isolado não estabelece diagnóstico; a interpretação deve considerar sintomas, histórico clínico e outros exames. Não substitui avaliação médica.</div>';
  return html;
}"""

new = """function renderInicio(){
  const rapidos = DATA.exames.filter(e=>e.consultaRapida && passaAmbiente(e)).sort((a,b)=>a.nome.localeCompare(b.nome,'pt-BR'));
  const introBanner = '<div class="intro-banner"><span class="intro-banner-icon">'+icon('flask')+'</span>'+
    '<p>Consulte exames laboratoriais, valores de referência, interpretação de resultados, interferentes e relações com medicamentos. Apoio técnico à prática farmacêutica, sem substituir avaliação clínica ou laudo laboratorial.</p></div>';

  let quickSection = '<div class="section-title">'+icon('star')+' Consulta Rápida</div>';
  quickSection += '<div class="quick-grid">'+rapidos.map(e=>{
    const cat=getCategoria(e.categoria);
    return '<div class="quick-card" '+ccStyle(cat.cor)+' onclick="abrirExame(\\''+e.id+'\\')"><span class="qc-dot"></span><span>'+e.nome+'</span></div>';
  }).join('')+'</div>';

  if(favoritos.size){
    quickSection += '<div class="section-title">'+icon('star')+' Seus Favoritos</div>';
    quickSection += '<div class="quick-grid">'+[...favoritos].map(id=>getExame(id)).filter(Boolean).map(e=>{
      const cat=getCategoria(e.categoria);
      return '<div class="quick-card" '+ccStyle(cat.cor)+' onclick="abrirExame(\\''+e.id+'\\')"><span class="qc-dot"></span><span>'+e.nome+'</span></div>';
    }).join('')+'</div>';
  }

  if(historico.length){
    quickSection += '<div class="section-title">'+icon('activity')+' Consultados recentemente</div>';
    quickSection += '<div class="quick-grid">'+historico.map(id=>getExame(id)).filter(Boolean).map(e=>{
      const cat=getCategoria(e.categoria);
      return '<div class="quick-card" '+ccStyle(cat.cor)+' onclick="abrirExame(\\''+e.id+'\\')"><span class="qc-dot"></span><span>'+e.nome+'</span></div>';
    }).join('')+'</div>';
  }

  let categoriasSection = '<div class="section-title">'+icon('more')+' Categorias</div>';
  categoriasSection += '<div class="tiles-grid">'+DATA.categorias.map(cat=>{
    const n = examesDaCategoria(cat.id).length;
    return '<button class="cat-tile" '+ccStyle(cat.cor)+' onclick="toggleCategoriaHome(\\''+cat.id+'\\')">'+
      '<span class="ct-icon">'+icon(cat.icone)+'</span>'+
      '<h4>'+cat.nome+'</h4>'+
      '<span class="ct-count">'+n+' exame'+(n===1?'':'s')+' cadastrado'+(n===1?'':'s')+'</span>'+
    '</button>';
  }).join('')+'</div>';

  // No mobile, "Categorias" vem antes de "Consulta Rápida" (e dos blocos de favoritos/
  // recentes, que ficam junto dela); no desktop a ordem original é mantida.
  let html = introBanner + (isMobile() ? (categoriasSection + quickSection) : (quickSection + categoriasSection));

  html += '<div class="disclaimer-fixed">'+icon('alert')+' Este conteúdo é uma ferramenta de apoio técnico à prática farmacêutica. Valores de referência podem variar entre laboratórios, métodos e populações. Priorize sempre o intervalo informado pelo laboratório do paciente. Um resultado isolado não estabelece diagnóstico; a interpretação deve considerar sintomas, histórico clínico e outros exames. Não substitui avaliação médica.</div>';
  return html;
}"""

content = replace_once(content, old, new, "exames-mobile-order")

# Add isMobile() helper (same convention/threshold used elsewhere in FarmaPrática), if not
# already present — placed right before renderInicio for locality.
assert 'function isMobile(' not in content, "isMobile() already exists — skip adding a duplicate"
content = content.replace(
    "/* ---------------- Render: Main ---------------- */",
    "function isMobile(){ return window.innerWidth <= 800; }\n\n/* ---------------- Render: Main ---------------- */",
    1
)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - Categorias now shows above Consulta Rapida on mobile")
