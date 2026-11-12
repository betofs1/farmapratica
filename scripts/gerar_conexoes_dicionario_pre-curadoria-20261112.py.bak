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
    item = {}
    if t['id'] in casos: item['casos'] = casos[t['id']][:8]; n_c += 1
    if achados: item['bulario'] = achados[:8]; n_b += 1
    if item: out[t['id']] = item
json.dump({'_meta': {'gerado_por': 'scripts/gerar_conexoes_dicionario.py', 'termos_com_casos': n_c, 'termos_com_bulario': n_b}, 'conexoes': out},
          open(P('dicionario', 'conexoes.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('termos com casos:', n_c, '| com Bulário:', n_b, '| total com conexão:', len(out))
