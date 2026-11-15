#!/usr/bin/env python3
"""
Gera bulario/atalhos.json — mapa de cada fármaco do Bulário para as
ferramentas relacionadas do FarmaPrática (Interações, Calculadora
Pediátrica, Substituição de Medicamentos e Controle Especial).

Rodar a partir da pasta "- INDEX":   python3 scripts/gerar_atalhos_bulario.py
Regenerar sempre que mudar: bulario/data.js, interacoes/medicamentos.json,
dosespediatricas/dados.json, medinter/medicamentos.json ou as listas
embutidas em consultacontrolados/index.html.
"""
import json, re, unicodedata, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(BASE, *a)

def norm(s):
    s = unicodedata.normalize('NFD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', s)).strip()

# Sais/ésteres que não mudam o fármaco de referência para fins de atalho
SAIS = r'(cloridrato|dicloridrato|bromidrato|maleato|dimaleato|sulfato|fosfato|acetato|succinato|tartarato|hemitartarato|' \
       r'besilato|mesilato|fumarato|hemifumarato|citrato|di?propionato|valerato|furoato|butirato|' \
       r'sodico|sodica|potassico|potassica|calcico|calcica|magnesico|cloreto|bissulfato|oxalato|' \
       r'pamoato|lactato|gluconato|carbonato|hidrobrometo|monoidratado|monoidratada|di?hidratado|tri?hidratado|' \
       r'cloridratada|hiclato|estolato|etinilestradiol nao)'
def base(s):
    n = norm(s)
    n = re.sub(r'\b' + SAIS + r'\b( de)?', ' ', n)
    n = re.sub(r'^\s*de\s+', ' ', n)
    return re.sub(r'\s+', ' ', n).strip()

def extrair_obj(texto, marcador):
    i = texto.index(marcador); j = texto.index('{', i); d = 0
    for k in range(j, len(texto)):
        c = texto[k]
        if c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: return json.loads(texto[j:k+1])
    raise ValueError(marcador)

def main():
    bul = extrair_obj(open(P('bulario', 'data.js'), encoding='utf-8').read(), 'const MEDICAMENTOS')

    inter = json.load(open(P('interacoes', 'medicamentos.json'), encoding='utf-8'))
    inter_idx = {}
    for m in inter:
        for n in [m['id'].replace('_', ' '), m['nome']] + (m.get('aliases') or []):
            for k in {norm(n), base(n), base(re.sub(r'\(.*?\)', '', n))}:
                if k: inter_idx.setdefault(k, m['id'])

    calc = json.load(open(P('dosespediatricas', 'dados.json'), encoding='utf-8'))['farmacos']
    calc_idx = {}
    for f in calc:
        for k in {norm(f['nome']), base(f['nome']), base(re.sub(r'\(.*?\)', '', f['nome']))}:
            if k: calc_idx.setdefault(k, f['id'])

    html = open(P('consultacontrolados', 'index.html'), encoding='utf-8').read()
    listas = json.loads(re.search(r'<script[^>]*id="dados-controlados"[^>]*>(.*?)</script>', html, re.S).group(1))['listas']
    ctrl_idx = {}
    for cod, lista in listas.items():
        for nome in lista.get('substancias', []):
            for k in {norm(nome), base(nome)}:
                if k: ctrl_idx.setdefault(k, {'nome': nome, 'lista': cod})

    cmed = json.load(open(P('medinter', 'medicamentos.json'), encoding='utf-8'))['medicamentos']
    princ = set()
    for m in cmed:
        for p in str(m.get('principio') or '').split(';'):
            b = base(p)
            if b: princ.add(b)

    out, cont = {}, {'interacoes': 0, 'calc': 0, 'controlado': 0, 'medinter': 0}
    for mid, m in bul.items():
        nome = m.get('nomeGenerico') or mid
        chaves = [norm(nome), base(nome)]
        # associações (ex.: "dexametasona + clotrimazol"): usa só o nome completo
        a = {}
        for k in chaves:
            if 'interacoes' not in a and k in inter_idx: a['interacoes'] = inter_idx[k]
            if 'calc' not in a and k in calc_idx: a['calc'] = calc_idx[k]
            if 'controlado' not in a and k in ctrl_idx: a['controlado'] = ctrl_idx[k]
        b = base(nome)
        if b and len(b) >= 4 and b in princ:
            a['medinter'] = b
        if a:
            out[mid] = a
            for k in a: cont[k] += 1

    destino = P('bulario', 'atalhos.json')
    with open(destino, 'w', encoding='utf-8') as fh:
        json.dump({'_meta': {'gerado_por': 'scripts/gerar_atalhos_bulario.py', 'total_farmacos': len(bul), 'contagem': cont}, 'atalhos': out},
                  fh, ensure_ascii=False, separators=(',', ':'))
    print('fármacos com atalho:', len(out), 'de', len(bul), cont, '->', destino)

if __name__ == '__main__':
    main()
