import json, re, unicodedata

def norm(s):
    s = s.lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'\([^)]*\)', ' ', s)  # strip parenthetical content on BOTH sides
    s = re.sub(r'[^a-z0-9]+', ' ', s).strip()
    return s

with open('dicionario/dicionario.json', encoding='utf-8') as f:
    data = json.load(f)
terms = data['termos']

existing_norm = {}
for t in terms:
    existing_norm.setdefault(norm(t.get('termo','')), []).append(t.get('id'))
    for s in t.get('sinonimos', []) or []:
        existing_norm.setdefault(norm(s), []).append(t.get('id'))

wanted = [
"Assistencia farmaceutica","Farmacia clinica","Comissao de Farmacia e Terapeutica",
"Centro de Informacao sobre Medicamentos","Padronizacao de medicamentos",
"Medicamento nao padronizado","Uso racional de medicamentos","Farmacoeconomia",
"Validacao da prescricao","Aprazamento","Dispensacao individualizada","Rastreabilidade de medicamentos",
"Farmacovigilancia","Reacao adversa a medicamento","Evento adverso relacionado a medicamento",
"Quase falha","Queixa tecnica","Desvio de qualidade","Medicamento de alta vigilancia",
"Medicamento com nome semelhante","Medicamento com aparencia semelhante","Dupla checagem",
"Gerenciamento de risco","Seguranca do processo de medicacao","Ineficacia terapeutica",
"Farmacocinetica","Farmacodinamica","Interacao medicamentosa","Incompatibilidade farmaceutica",
"Contraindicacao","Indicacao terapeutica","Posologia","Dose maxima","Ajuste posologico",
"Equivalencia de doses","Janela terapeutica","Monitoramento terapeutico de farmacos","Polifarmacia",
"Uso off label","Uso compassivo","Acesso expandido","Consentimento livre e esclarecido",
"Forma farmaceutica","Reconstituicao","Diluicao","Infusao intermitente","Infusao continua",
"Administracao enteral","Administracao parenteral","Administracao por sonda",
"Compatibilidade com alimentos","Estabilidade farmaceutica","Fotossensibilidade","Termolabilidade",
"Flebite","Depuracao da creatinina","Taxa de filtracao glomerular","Insuficiencia renal",
"Insuficiencia hepatica","Eletrolitos concentrados","Nutricao parenteral","Solucao vasoativa",
"Radiofarmaco","Meio de contraste","Risco de queda associado a medicamentos",
"Qualificacao de fornecedores","Programacao de medicamentos","Dispensario eletronico",
"Conciliacao medicamentosa","Uso de medicamento sob investigacao","Medicamento de alto custo",
"Armazenamento segregado","Codigo de barras bidimensional","Dispensacao descentralizada",
"Uso de medicamentos baseado em evidencias"
]

# Exact match only this time (both sides parenthesis-stripped) -- high precision
print(f"{'TERMO':55} | MATCH")
for w in wanted:
    n = norm(w)
    hit = existing_norm.get(n, [])
    print(f'{w!r:55} -> {hit}')
