import re, sys, io

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected exactly 1 occurrence, found {count}"
    return content.replace(old, new, 1)

# 1) Replace the PEDIATRIC_DRUG_MAP block: normalizeDrugName stays, add matchKey + FORM_WORDS,
#    and switch loadPediatricDrugMap/lookupPediatricDrugId to use matchKey with a "+"-fallback.
old_block = """async function loadPediatricDrugMap(){
  try{
    const res = await fetch('../dosespediatricas/dados.json', { cache: 'no-store' });
    const data = await res.json();
    (data.farmacos || []).forEach(f => {
      const key = normalizeDrugName(f.nome);
      if(key) PEDIATRIC_DRUG_MAP[key] = f.id;
    });
  }catch(e){
    // Calculadora Pediátrica pode não estar acessível (ex.: aberto localmente sem
    // servidor, ou pasta movida) — o link de dose pediátrica simplesmente não aparece,
    // sem quebrar nada do restante da página.
  }
}
function lookupPediatricDrugId(name){
  const key = normalizeDrugName(name);
  return key ? (PEDIATRIC_DRUG_MAP[key] || null) : null;
}"""

new_block = """// Palavras de forma farmacêutica/via/unidade que aparecem no texto do FarmaDesk
// (ex.: "Amoxicilina 500mg xarope") mas não fazem parte do nome do fármaco em si —
// se não forem removidas, impedem o casamento com o nome puro usado na Calculadora
// de Doses (ex.: "Amoxicilina"), reduzindo bastante a cobertura do recurso.
const FORM_WORDS = new Set([
  'xarope','creme','comprimido','comprimidos','capsula','capsulas','gotas','spray',
  'shampoo','xampu','colirio','pomada','locao','solucao','injetavel','nasal','oral',
  'oftalmico','oftalmica','vaginal','topico','topica','sublingual','suspensao',
  'granulado','pastilha','pastilhas','sache','saches','ampola','ampolas','frasco',
  'gel','emulsao','po','liquido','liquida','efervescente','mastigavel','mastigaveis',
  'retard','elixir','adesivo','inalatorio','inalatoria','bucal',
  'mg','mcg','g','ui','iu','microgramas','unidade','unidades','dose','doses',
  'potencia','baixa','media','alta'
]);
function matchKey(s){
  let key = normalizeDrugName(s);
  // remove dosagem no formato número+unidade (ex.: "500mg", "1.000 mg", "5 ui")
  key = key.replace(/\\d+[.,]?\\d*\\s*(mg|mcg|microgramas?|ml|g|ui|iu)\\b/g, ' ');
  // remove números soltos remanescentes (concentrações isoladas)
  key = key.replace(/\\b\\d+[.,]?\\d*\\b/g, ' ');
  // remove palavras de forma farmacêutica/via/unidade
  key = key.split(' ').filter(w => w && !FORM_WORDS.has(w)).join(' ').trim();
  return key;
}
async function loadPediatricDrugMap(){
  try{
    const res = await fetch('../dosespediatricas/dados.json', { cache: 'no-store' });
    const data = await res.json();
    (data.farmacos || []).forEach(f => {
      const key = matchKey(f.nome);
      if(key) PEDIATRIC_DRUG_MAP[key] = f.id;
    });
  }catch(e){
    // Calculadora de Doses pode não estar acessível (ex.: aberto localmente sem
    // servidor, ou pasta movida) — o link de dose simplesmente não aparece,
    // sem quebrar nada do restante da página.
  }
}
function lookupPediatricDrugId(name){
  const key = matchKey(name);
  if(!key) return null;
  if(PEDIATRIC_DRUG_MAP[key]) return PEDIATRIC_DRUG_MAP[key];
  // Produtos combinados (ex.: "Amoxicilina + Clavulanato 875mg"): se não casar o nome
  // completo, tenta casar só pelo primeiro componente, antes do "+".
  if(key.includes('+')){
    const first = key.split('+')[0].trim();
    if(first && PEDIATRIC_DRUG_MAP[first]) return PEDIATRIC_DRUG_MAP[first];
  }
  return null;
}"""

content = replace_once(content, old_block, new_block, "pediatric-drug-map-matchkey")

# 2) Rename the chip's visible text from "dose pediátrica" to "dose", and update the
#    tooltip/comment wording to match (the tool now covers pediatric AND adult dosing).
old_link = '''        pedLink.title = `Abrir "${mainDrug}" direto na Calculadora Pediátrica`;
        pedLink.className = 'drug-link-secondary drug-ped-link';
        pedLink.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="8" x2="16" y2="8"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="8" y1="16" x2="12" y2="16"/></svg> dose pediátrica`;'''
new_link = '''        pedLink.title = `Abrir "${mainDrug}" direto na Calculadora de Doses`;
        pedLink.className = 'drug-link-secondary drug-ped-link';
        pedLink.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="8" x2="16" y2="8"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="8" y1="16" x2="12" y2="16"/></svg> dose`;'''
content = replace_once(content, old_link, new_link, "chip-text-rename")

# 3) Small comment-wording touch-ups near the integration header (non-functional, just
#    keeps the comments honest now that it's not pediatric-only matching anymore).
old_comment = """// ---------- INTEGRAÇÃO CRUZADA: Calculadora Pediátrica e Substituição de Medicamentos ----------
// Reaproveita a lista real de fármacos da Calculadora Pediátrica (dosespediatricas) para
// só oferecer o link de dose pediátrica quando o fármaco realmente existir lá."""
new_comment = """// ---------- INTEGRAÇÃO CRUZADA: Calculadora de Doses e Substituição de Medicamentos ----------
// Reaproveita a lista real de fármacos da Calculadora de Doses (dosespediatricas) para
// só oferecer o link de dose quando o fármaco realmente existir lá. O casamento usa
// matchKey() (abaixo) em vez do nome bruto, pois o FarmaDesk costuma incluir dosagem/forma
// farmacêutica no texto (ex.: "Amoxicilina 500mg"), o que impediria o match exato."""
content = replace_once(content, old_comment, new_comment, "header-comment")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - all 3 edits applied")
