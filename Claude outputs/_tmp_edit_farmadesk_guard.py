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
  if(PEDIATRIC_DRUG_MAP[key]) return PEDIATRIC_DRUG_MAP[key];
  // Produtos combinados (ex.: "Amoxicilina + Clavulanato 875mg"): se não casar o nome
  // completo, tenta casar só pelo primeiro componente, antes do "+".
  if(key.includes('+')){
    const first = key.split('+')[0].trim();
    if(first && PEDIATRIC_DRUG_MAP[first]) return PEDIATRIC_DRUG_MAP[first];
  }
  return null;
}"""

new = """// Trava de segurança: alguns itens da Calculadora de Doses só existem numa forma/via bem
// restrita (ex.: colírio, solução otológica, suspensão para nebulização). Como matchKey()
// descarta palavras de forma farmacêutica para maximizar o casamento, uma menção do MESMO
// princípio ativo em outra via no FarmaDesk (ex.: "Ciprofloxacino 500mg" via oral) poderia
// ser incorretamente ligada a um item de via totalmente diferente (ex.: a solução otológica).
// Este mapa rejeita o casamento quando o texto original do FarmaDesk sinaliza uma via
// claramente incompatível com a do item da Calculadora de Doses — preferindo não mostrar o
// link de dose a mostrar um link que levaria a uma posologia da via errada.
const ROUTE_GUARD = {
  // Único item de ciprofloxacino na Calculadora de Doses é a solução otológica; o FarmaDesk
  // só menciona Ciprofloxacino em uso oral/oftálmico, nunca otológico — bloqueia sempre.
  'ciprofloxacino_otologico': /.*/,
  // Item é suspensão para NEBULIZAÇÃO; não deve casar com spray NASAL (rinite/sinusite).
  'budesonida_nebulizacao': /nasal|spray/,
  // Item é via ORAL; não deve casar com gel VAGINAL.
  'metronidazol': /vaginal/,
  // Item é suspensão ORAL; não deve casar com creme vaginal nem combinação tópica com zinco.
  'nistatina': /vaginal|zinco/,
  // Item é GEL ORAL (candidíase oral); não deve casar com creme/pó tópico para frieira/pé de atleta.
  'miconazol_oral': /\\bp[oó]\\b|\\bcreme\\b|frieira|atleta/,
};
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
  if(guard && guard.test(normalizeDrugName(name))) return null;
  return id;
}"""

content = replace_once(content, old, new, "route-guard")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK - route guard applied")
