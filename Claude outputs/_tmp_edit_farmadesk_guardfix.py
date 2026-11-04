import io

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_once(content, old, new, label):
    count = content.count(old)
    assert count == 1, f"[{label}] expected exactly 1 occurrence, found {count}"
    return content.replace(old, new, 1)

old = """function lookupPediatricDrugId(name){
  const key = matchKey(name);
  if(!key) return null;
  let id = PEDIATRIC_DRUG_MAP[key] || null;
  // Produtos combinados (ex.: "Amoxicilina + Clavulanato 875mg"): se não casar o nome
  // completo, tenta casar só pelo primeiro componente, antes do "+".
  if(!id && key.includes('+')){
    const first = key.split('+')[0].trim();
    if(first && PEDIATRIC_DRUG_MAP[first]) id = PEDIATRIC_DRUG_MAP[first];
  }
  if(!id) return null;
  const guard = ROUTE_GUARD[id];
  if(guard && guard.test(normalizeDrugName(name))) return null;
  return id;
}"""

new = """// Mesma normalização básica (minúsculas, sem acento) usada pelo ROUTE_GUARD, mas SEM
// descartar o conteúdo de parênteses — ao contrário de normalizeDrugName(), pois é
// justamente dentro dos parênteses que o FarmaDesk costuma indicar a forma farmacêutica
// (ex.: "Miconazol 2% (Creme ou Pó)"), e o guard precisa enxergar essa palavra.
function rawNormalize(s){
  return (s || '')
    .toLowerCase()
    .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
    .replace(/[^a-z0-9\\s+]/g, ' ')
    .replace(/\\s+/g, ' ')
    .trim();
}
function lookupPediatricDrugId(name){
  const key = matchKey(name);
  if(!key) return null;
  let id = PEDIATRIC_DRUG_MAP[key] || null;
  // Produtos combinados (ex.: "Amoxicilina + Clavulanato 875mg"): se não casar o nome
  // completo, tenta casar só pelo primeiro componente, antes do "+".
  if(!id && key.includes('+')){
    const first = key.split('+')[0].trim();
    if(first && PEDIATRIC_DRUG_MAP[first]) id = PEDIATRIC_DRUG_MAP[first];
  }
  if(!id) return null;
  const guard = ROUTE_GUARD[id];
  if(guard && guard.test(rawNormalize(name))) return null;
  return id;
}"""

content = replace_once(content, old, new, "guard-rawnormalize-fix")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - guard now tests against rawNormalize (parens preserved)")
