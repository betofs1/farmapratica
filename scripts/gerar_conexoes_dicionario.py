#!/usr/bin/env python3
"""
Gera dicionario/conexoes.json — para cada verbete do Dicionário, os casos do
Desafio Clínico que o citam (campo termosDicionario) e as fichas do Bulário
com o mesmo nome (fármaco, classe no plural como "Insulinas" ou classe
terapêutica do Bulário, como "Anti-histamínicos").

Rodar a partir da pasta "- INDEX":   python3 scripts/gerar_conexoes_dicionario.py
Regenerar quando mudar dicionario/dicionario.json, desafio/desafio.json ou bulario/dados-busca.json.
"""
import json, os, re, unicodedata
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(BASE, *a)
def norm(s):
    s = unicodedata.normalize('NFD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', s)).strip()
SAIS = r'\b(cloridrato|dicloridrato|bromidrato|maleato|sulfato|fosfato|acetato|succinato|tartarato|hemitartarato|besilato|mesilato|fumarato|citrato|sodico|sodica|potassico|potassica|calcico|calcica|monoidratado|hiclato)\b( de)?'
def base(s): return re.sub(r'\s+', ' ', re.sub(SAIS, ' ', norm(s))).strip()

dic = json.load(open(P('dicionario', 'dicionario.json'), encoding='utf-8'))
des = json.load(open(P('desafio', 'desafio.json'), encoding='utf-8'))
bul = json.load(open(P('bulario', 'dados-busca.json'), encoding='utf-8'))['medicamentos']
cats = {c['id']: c['nome'] for c in des.get('categorias', [])}


# 12/11/2026: curadoria manual para verbetes de CLASSE farmacológica. A busca
# automática pela classe ATC do Bulário trazia pares errados (ex.: "AINEs" ->
# tacrolimo/pimecrolimo, da classe ATC de anti-inflamatórios dermatológicos;
# "Antipsicóticos" -> clonazepam; "Macrolídeos" -> clindamicina) e cortava os
# fármacos de referência porque os 8 primeiros em ordem alfabética eram
# associações. Para estes verbetes vale SÓ a lista abaixo, na ordem dada:
# cada item é o princípio ativo (sem sal); "a + b" pede a associação exata.
CURADO = {
  'aines': ['ibuprofeno','diclofenaco','naproxeno','cetoprofeno','nimesulida','meloxicam','celecoxibe','piroxicam','etoricoxibe','acido mefenamico','indometacina','tenoxicam'],
  'ieca': ['captopril','enalapril','lisinopril','ramipril','perindopril','benazepril','fosinopril','trandolapril'],
  'ibp': ['omeprazol','pantoprazol','esomeprazol','lansoprazol','rabeprazol','dexlansoprazol'],
  'betalactamicos': ['amoxicilina','amoxicilina + clavulanato','ampicilina','penicilina g benzatina','cefalexina','cefuroxima','ceftriaxona','meropenem','imipenem'],
  'penicilinas': ['amoxicilina','amoxicilina + clavulanato','ampicilina','penicilina g benzatina','oxacilina','piperacilina + tazobactam'],
  'macrolideos': ['azitromicina','claritromicina','eritromicina','espiramicina','roxitromicina'],
  'antipsicoticos': ['haloperidol','risperidona','quetiapina','olanzapina','aripiprazol','clorpromazina','clozapina','ziprasidona','levomepromazina','lurasidona'],
  'corticosteroides-sistemicos': ['prednisona','prednisolona','dexametasona','metilprednisolona','hidrocortisona','betametasona','deflazacorte'],
  'anticoagulantes-orais': ['varfarina','rivaroxabana','apixabana','dabigatrana','edoxabana'],
  'diureticos': ['hidroclorotiazida','clortalidona','indapamida','furosemida','bumetanida','espironolactona','amilorida','eplerenona'],
  'antiagregantes-plaquetarios': ['acido acetilsalicilico','clopidogrel','ticagrelor','prasugrel','cilostazol','dipiridamol'],
  'anticonvulsivantes': ['carbamazepina','fenitoina','acido valproico','divalproato','lamotrigina','levetiracetam','topiramato','fenobarbital','oxcarbazepina','lacosamida'],
  'bifosfonados': ['alendronato','risedronato','ibandronato','acido zoledronico','pamidronato'],
  'antiemeticos': ['ondansetrona','metoclopramida','bromoprida','domperidona','dimenidrinato','meclozina','granisetrona','aprepitanto'],
  'cefalosporinas': ['cefalexina','cefadroxila','cefaclor','cefuroxima','cefdinir','ceftriaxona','ceftazidima','cefepima'],
  'corticosteroides': None,
}
CURADO = {k: v for k, v in CURADO.items() if v}
def achar_curado(chave, bul):
    partes = [base(x) for x in chave.split('+')]
    for m in sorted(bul, key=lambda m: (len(m['nome']), m['nome'])):
        b = base(m['nome']); n_comp = m['nome'].count('+') + 1
        if n_comp == len(partes) and all(re.search(r'\b' + re.escape(pt) + r'\b', b) for pt in partes):
            return m
    return None

casos = {}
for c in des['casos']:
    for tid in c.get('termosDicionario') or []:
        casos.setdefault(tid, []).append({'id': c['id'], 'titulo': c['titulo'], 'cat': cats.get(c.get('categoria'), '')})

bul_idx = {}
for m in bul:
    bul_idx.setdefault(base(m['nome']), []).append(m)

out, n_c, n_b = {}, 0, 0
for t in dic['termos']:
    nomes = [t['termo']] + (t.get('sinonimos') or [])
    achados, vistos = [], set()
    for n in nomes:
        k = base(re.sub(r'\(.*?\)', '', n))
        if len(k) < 4: continue
        cand = list(bul_idx.get(k, []))
        if not cand and k.endswith('s') and len(k) > 5:          # classe no plural: "insulinas" -> "insulina ..."
            sing = k[:-1]
            cand = [m for kk, ms in bul_idx.items() if kk == sing or kk.startswith(sing + ' ') for m in ms]
        # só para verbetes que nomeiam classes de fármacos (evita casar doença com classe, ex.: HAS x HAP)
        if not cand and len(k) >= 7 and t.get('categoria') in ('farmacoterapia', 'microbiologia'):                              # classe terapêutica: "inibidores da eca" -> fichas da classe
            cand = [m for m in bul if re.search(r'\b' + re.escape(k) + r'\b', norm(m.get('classe', '')))]
        for m in cand:
            if m['id'] not in vistos:
                vistos.add(m['id']); achados.append({'id': m['id'], 'nome': m['nome']})
    if t['id'] in CURADO:
        achados = []
        for chave in CURADO[t['id']]:
            m = achar_curado(chave, bul)
            if m and m['id'] not in {x['id'] for x in achados}:
                achados.append({'id': m['id'], 'nome': m['nome']})
    else:
        # monofármacos antes das associações
        achados.sort(key=lambda x: (x['nome'].count('+'), len(x['nome']), x['nome']))
        # uma ficha por princípio ativo (ignora variações de hidratação/sal)
        HID = r'\b(mono|di|tri|sesqui|hemi)? ?-?hidratad[oa]s?|monoidratad[oa]|trihidratad[oa]|tri hidratad[oa]|di hidratad[oa]\b'
        unicos, vistos_b = [], set()
        for x in achados:
            kb = re.sub(r'\s+', ' ', re.sub(HID, ' ', base(x['nome']))).strip()
            if kb not in vistos_b: vistos_b.add(kb); unicos.append(x)
        achados = unicos
    item = {}
    if t['id'] in casos: item['casos'] = casos[t['id']][:8]; n_c += 1
    if achados: item['bulario'] = achados[:8]; n_b += 1
    if item: out[t['id']] = item
json.dump({'_meta': {'gerado_por': 'scripts/gerar_conexoes_dicionario.py', 'termos_com_casos': n_c, 'termos_com_bulario': n_b}, 'conexoes': out},
          open(P('dicionario', 'conexoes.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('termos com casos:', n_c, '| com Bulário:', n_b, '| total com conexão:', len(out))
