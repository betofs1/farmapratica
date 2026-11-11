"""Gera o bloco <script id="listas-344"> da Conferência de Receitas a partir do
JSON embutido em consultacontrolados/index.html (fonte única das listas).
Uso: python gerar_listas_receitas.py <consultacontrolados/index.html> <receitas/index.html>
"""
import json, re, sys, unicodedata
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', s).strip()
src, dst = sys.argv[1], sys.argv[2]
cc = open(src, encoding='utf-8').read()
d = json.loads(re.search(r'<script type="application/json" id="dados-controlados">(.*?)</script>', cc, re.S).group(1))
L = {}
for cod, lst in d['listas'].items():
    for nome in lst['substancias']:
        nomes = [nome] + re.findall(r'\(([^)]+)\)', nome)
        for n in nomes:
            k = norm(re.sub(r'\([^)]*\)', '', n))
            if len(k) >= 4 and k not in L:
                L[k] = [cod, re.sub(r'\s*\([^)]*\)', '', n).strip()]
X = sorted({norm(re.sub(r'\([^)]*\)', '', k)) for k in d.get('excecoes', {})})
out = {'_fonte': 'consultacontrolados/index.html (dados-controlados) · ' + str(d.get('_capturado_em', '')), 'L': L, 'X': X}
bloco = '<script type="application/json" id="listas-344">' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '</script>'
html = open(dst, encoding='utf-8').read()
if 'id="listas-344"' in html:
    html = re.sub(r'<script type="application/json" id="listas-344">.*?</script>', lambda m: bloco, html, flags=re.S)
else:
    html = html.replace('<script src="../assets/tempo-uso.js"', bloco + '\n\n<script src="../assets/tempo-uso.js"', 1)
open(dst, 'w', encoding='utf-8').write(html)
print('substâncias:', len(L), 'exceções:', len(X), 'bytes:', len(bloco))
