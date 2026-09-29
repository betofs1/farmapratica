# Módulo Exames Laboratoriais (FarmaLab) — FarmaPrática

Ferramenta de consulta rápida a exames laboratoriais para apoio à prática
farmacêutica: valores de referência, interpretação de resultados alterados,
interferentes pré-analíticos, medicamentos que podem alterar o exame,
exames correlacionados, calculadoras (TFG, LDL, relação albumina/creatinina)
e um comparador de resultados ao longo do tempo (armazenado localmente no
navegador do usuário, sem envio a servidor).

**Não substitui diagnóstico médico, laudo laboratorial ou avaliação clínica
profissional** — é uma ferramenta de apoio informativo e organizacional.

## Arquivos do módulo

```
index.html   → aplicação (HTML + CSS + JS), lê os dados de exames.json em tempo de execução
exames.json  → banco de dados dos exames, categorias e glossário
logo.png     → logo da marca (mesma imagem usada nas demais ferramentas)
README.md    → este guia
```

Diferente de `consultacontrolados` (gerado por pipeline Python a partir de
fontes oficiais) e mais parecido com `interacoes`, este módulo carrega os
dados via `fetch('exames.json')` no carregamento da página — **por isso,
para testar localmente, é preciso servir a pasta por um servidor HTTP**
(abrir o `index.html` direto por duplo-clique bloqueia o `fetch` por
política de CORS do navegador para arquivos `file://`):

```
cd "- INDEX/exames"
python3 -m http.server 8000
# depois abrir http://localhost:8000/ no navegador
```

No site publicado (GitHub Pages), o `fetch` funciona normalmente sem
nenhuma configuração adicional.

## Como adicionar ou editar um exame

Edite `exames.json`, dentro do array `"exames"`. Cada exame é um objeto
com os campos abaixo (todos os já cadastrados servem de modelo/exemplo):

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | identificador único, minúsculo, sem espaços (usado em links internos) |
| `nome` | string | nome completo do exame |
| `sigla` | string | sigla/abreviação usual |
| `sinonimos` | string[] | outros nomes pelos quais o exame é conhecido |
| `categoria` | string | precisa bater com um `id` existente em `"categorias"` |
| `ambiente` | string | `"hospitalar"`, `"drogaria"` ou `"ambos"` — usado pelo filtro de ambiente do cabeçalho (ver seção própria abaixo) |
| `grupo` | string | subgrupo dentro da categoria (aparece como rótulo na sidebar) |
| `sistema` | string | sistema fisiológico avaliado |
| `amostraTipo` | string | tipo de amostra, versão curta (aparece nos indicadores/chips) |
| `consultaRapida` | boolean | se `true`, aparece em "Mais Consultados"/"Consulta Rápida" |
| `favoritoPadrao` | boolean | se `true`, aparece como sugestão na tela de Favoritos vazia |
| `descricao` | string | texto de "Visão Geral" — o que é, o que avalia, quando é solicitado |
| `finalidade` | string | para que serve clinicamente |
| `valoresReferencia` | array | lista de `{parametro, faixa, unidade, obs}` — pode ter várias linhas (sexo, idade etc.) |
| `interpretacaoAlta` / `interpretacaoBaixa` | objeto | `{resumo, causas:[], examesApoio:[ids]}` |
| `condicoesClinicas` | objeto | `{aumentado:[], reduzido:[]}` — condições clínicas associadas |
| `medicamentos` | objeto | `{aumentam:[], reduzem:[], interferem:[]}` — sempre com base em fonte farmacológica confiável |
| `interferentes` | array | lista de `{fator, efeito}` — fatores pré-analíticos |
| `preparo` | objeto | `{jejumNecessario:bool, tempoJejumHoras:num, observacoes:[]}` |
| `amostra` | objeto | `{tipo, tubo, armazenamento, rejeicao:[]}` |
| `correlatos` | string[] | **ids** de outros exames já cadastrados em `exames.json` (viram links clicáveis) |
| `correlatosTexto` | string[] | nomes de exames relacionados que ainda **não** têm página própria (aparecem como texto, não clicáveis) |
| `alertas` | string[] | situações que merecem atenção/encaminhamento ("Quando merece atenção?") |
| `observacoes` | string | nota livre adicional, exibida na aba Fontes |
| `fontes` | string[] | referências/diretrizes usadas |
| `dataAtualizacao` | string | data (AAAA-MM-DD) da última revisão do conteúdo deste exame |

Ao adicionar um novo exame que deveria aparecer no **Modo Balcão**, não é
necessário nenhum campo extra — o modo balcão é montado automaticamente a
partir de `descricao`, `valoresReferencia`, `interpretacaoAlta/Baixa`,
`medicamentos`, `correlatos` e `alertas` já preenchidos.

## Categorias

O array `"categorias"` no topo do `exames.json` define as 22 categorias
fixas da ferramenta (Hematologia, Bioquímica, Hormônios, Lipidograma,
Glicemia e Metabolismo, Função Renal, Função Hepática, Eletrólitos,
Marcadores Cardíacos, Marcadores Inflamatórios, Imunologia, Infectologia,
Coagulação, Endocrinologia, Vitaminas e Minerais, Marcadores Tumorais,
Urinálise, Parasitologia, Microbiologia, Gasometria, Exames de Fezes,
Outros). Categorias sem nenhum exame cadastrado continuam aparecendo na
barra lateral, com contador "0" e uma mensagem "Nenhum exame cadastrado
ainda nesta categoria" — isso é proposital (mostra o escopo completo da
ferramenta e convida a expandir o conteúdo). Desde 28/09/2026, apenas
"Outros" (catch-all) permanece nesse estado; todas as demais têm ao menos
1 exame cadastrado.

**Categoria removida em 28/09/2026:** "Imagem e Complementares" (exames de
imagem: USG, RX, TC, RM, ECG) foi retirada da ferramenta após pesquisa da
base regulatória — a Resolução CFF nº 585/2013, que define as atribuições
clínicas do farmacêutico, autoriza apenas a solicitação de **exames
laboratoriais** para monitorização da farmacoterapia (Art. 11, XI) e
determinação de parâmetros bioquímicos/fisiológicos (Art. 12, XIV); não há
previsão de solicitação/interpretação de exames de imagem na prática
clínica farmacêutica brasileira. Nenhum exame estava vinculado a essa
categoria, então a remoção não afetou nenhum registro existente.

Cada categoria tem um campo `"cor"` (nome de uma paleta pré-definida no
CSS: `red, blue, purple, amber, green, sky, crimson, orange, cyan, teal,
indigo, lime, magenta, yellow, brown, petrol, slate, gray`) e um `"icone"`
(chave do objeto `ICONS` dentro do `<script>` do `index.html` — para usar
um ícone novo, adicione a chave/path SVG em `ICONS` antes de referenciá-la
aqui).

## Filtro de ambiente (Hospitalar / Drogaria / Todos)

O cabeçalho da ferramenta tem um seletor com três opções — **Todos os
ambientes** (padrão), **Somente Hospitalar** e **Somente Drogaria** — que
filtra a navegação (sidebar, grade de categorias e busca) pelos exames
relevantes em cada ambiente de atuação farmacêutica.

Cada exame carrega o campo `"ambiente"` com um destes valores:

- `"hospitalar"`: exame de uso/monitorização tipicamente restrito ao
  ambiente hospitalar (ex.: exige infusão contínua monitorada, curva de
  calibração de laboratório de referência, ou é usado predominantemente em
  contexto de internação/emergência).
- `"drogaria"`: exame tipicamente acompanhado no contexto de farmácia
  comunitária/ambulatorial.
- `"ambos"`: exame relevante nos dois ambientes — é o valor padrão para
  a maioria dos exames de rotina (hemograma, glicemia, lipidograma, função
  renal/hepática, hormônios etc.).

Ao filtrar por **Hospitalar**, aparecem os exames com `ambiente` igual a
`"hospitalar"` ou `"ambos"`; ao filtrar por **Drogaria**, aparecem os
exames com `"drogaria"` ou `"ambos"`. **Todos os ambientes** ignora o
campo e mostra tudo, sendo o comportamento padrão ao abrir a página.

Classificação atual (05/09 a 17/09/2026): os 20 exames originais e G6PD e
TP/RNI foram marcados como `"ambos"`; TTPA, Contagem de Reticulócitos,
Atividade Anti-Fator Xa e Dosagem de D-Dímero foram marcados como
`"hospitalar"`, por serem exames de monitorização mais especializada
(infusão hospitalar, curva de calibração de laboratório de referência).
Nenhum exame está marcado como exclusivamente `"drogaria"` ainda — a
classificação deve ser revisada/ajustada conforme o usuário indicar ao
adicionar novos exames.

## Estado atual do conteúdo (atualizado em 28/09/2026)

**142 exames** com todos os campos completos, distribuídos em 21 das 22
categorias (apenas "Outros" permanece vazia, propositalmente, como
catch-all). Contagem por categoria: Infectologia 17, Hormônios 16,
Imunologia 12, Hematologia 11, Glicemia e Metabolismo 10, Bioquímica 9,
Lipidograma 9, Função Renal 9, Marcadores Tumorais 8, Vitaminas e Minerais
8, Endocrinologia 6, Função Hepática 6, Marcadores Cardíacos 6, Eletrólitos
5, Marcadores Inflamatórios 3, Exames de Fezes 2, Coagulação 1, Urinálise
1, Parasitologia 1, Microbiologia 1, Gasometria 1.

Histórico de 05/09 a 17/09/2026 (43 exames): 20 exames originais de
Consulta Rápida (Hemograma, Glicemia de Jejum, HbA1c, Colesterol Total,
HDL, LDL, Triglicerídeos, Creatinina, Ureia, TGO, TGP, GGT, TSH, T4 Livre,
Vitamina D, Vitamina B12, Ferritina, PCR, Sódio e Potássio) + 6 exames de
Hematologia/coagulação (TP/RNI, TTPA, Reticulócitos, Anti-Fator Xa, G6PD,
D-Dímero) + 9 exames de Bioquímica (Ácido Úrico, Fosfatase Alcalina,
Bilirrubinas, LDH, CK Total, Amilase, Lipase, Cálcio, Magnésio) + 8 exames
de Hormônios (T3 Total, Cortisol, Estradiol, Progesterona, Testosterona
Total, Prolactina, LH, FSH).

**Rodada de 28/09/2026 (+94 exames, de 43 para 137):** a pedido do
usuário, que forneceu uma lista de referência com 17 categorias clínicas
(~150 itens), foram identificados os exames genuinamente ausentes,
deduplicando itens citados em múltiplas categorias (ex.: Ferritina,
Fosfatase Alcalina, TGO/AST, Fibrinogênio, CK Total/CK-MB, Proteínas
Totais, Albumina, Vitamina D, Cálcio Total já existiam ou foram
cadastrados uma única vez na categoria mais relevante). Decisão explícita
do usuário: manter a estrutura de dados atual (schema de categoria única
por exame, sem tags multicategoria e sem campo/badge de "valor
calculado"), usando a lista apenas como referência para identificar
lacunas. Exames adicionados em 8 lotes:

- **Lote 1** (11): VLDL, Colesterol Não-HDL, Apo A1, Apo B, Lp(a)
  (Lipidograma) + Troponina I, Troponina T, CK-MB, BNP, NT-proBNP,
  Mioglobina (Marcadores Cardíacos — categoria nova)
- **Lote 2** (12): Ferro Sérico, Transferrina, CTLF, IST (Hematologia) +
  Glicemia Pós-Prandial, Glicemia Casual, TOTG, Frutosamina, Insulina,
  Peptídeo C, HOMA-IR, HOMA-β (Glicemia e Metabolismo)
- **Lote 3** (16): T4 Total, T3 Livre, Tireoglobulina, Anti-TPO, Anti-Tg,
  TRAb (Hormônios) + Albumina, Proteínas Totais, Relação A/G (Função
  Hepática) + TFGe, Cistatina C, Clearance de Creatinina, RACU,
  Microalbuminúria, Proteinúria isolada, Proteinúria de 24h (Função Renal)
- **Lote 4** (13): EAS/Urina Tipo I — painel combinado (Urinálise —
  categoria nova) + Cloro, Cálcio Ionizado, Fósforo, PTH (Eletrólitos/
  Endocrinologia) + Fibrinogênio (Coagulação — categoria nova) + PCR
  Ultrassensível, VHS (Marcadores Inflamatórios) + Ácido Fólico, Vitamina
  A, Vitamina E, Vitamina B1, Vitamina B6 (Vitaminas e Minerais)
- **Lote 5** (9): Eletroforese de Proteínas, IgG, IgA, IgM (Imunologia —
  categoria nova) + Testosterona Livre, SHBG, ACTH, DHEA-S, IGF-1
  (Endocrinologia — categoria nova)
- **Lote 6** (17): painel completo de Sorologia/Infectologia (categoria
  nova) — HBsAg, Anti-HBs, Anti-HBc Total, Anti-HBc IgM, Anti-HCV, HIV
  1/2, Carga Viral HIV, VDRL, FTA-ABS, Toxoplasma IgG/IgM, Dengue NS1/IgM/
  IgG, CMV IgG/IgM, EBV, Rubéola IgG/IgM
- **Lote 7** (8): painel de Autoimunidade — FAN, Fator Reumatoide,
  Anti-CCP, Anti-DNA nativo, Anti-Ro/SSA, Anti-La/SSB, C3, C4 (Imunologia)
- **Lote 8** (8): painel de Marcadores Tumorais (categoria nova) — PSA
  Total, PSA Livre, CEA, CA 19-9, CA 125, CA 15-3, AFP, Beta-hCG. **Todos
  os 8 exames carregam, no campo `alertas`, o aviso clínico obrigatório
  (pedido explícito do usuário): são indicados primariamente para
  acompanhamento terapêutico/reavaliação de recidiva em paciente já
  diagnosticado, não para rastreamento populacional/diagnóstico primário
  isolado.**

Cruzamentos (`correlatos`) de Creatinina, Ureia e Fosfatase Alcalina foram
atualizados para apontar como links clicáveis para EAS, RACU, Clearance de
Creatinina e Fósforo, promovendo textos que antes ficavam apenas em
`correlatosTexto`.

**Lote 9 — categorias zeradas (28/09/2026, +5 exames, de 137 para 142):**
durante a rodada acima, o usuário notou pelo app que várias categorias
ficariam com 0 exames mesmo após os 8 lotes (Parasitologia, Microbiologia,
Gasometria, Exames de Fezes — nenhuma constava na lista de referência
original) e pediu para completá-las, mas **somente com exames que
realmente participam da rotina do farmacêutico** — o que motivou a
pesquisa regulatória da Resolução CFF 585/2013 (ver seção "Categorias"
acima) e a remoção da categoria "Imagem e Complementares". Exames
adicionados, todos escolhidos por relevância direta ao acompanhamento
farmacoterapêutico:

- Parasitológico de Fezes (EPF) — Parasitologia — acompanhamento de
  antiparasitários (albendazol, mebendazol, secnidazol)
- Urocultura com Antibiograma — Microbiologia — ajuste racional de
  antibioticoterapia conforme perfil de sensibilidade
- Gasometria Arterial — Gasometria (`ambiente: hospitalar`) — equilíbrio
  ácido-base para farmacêuticos hospitalares/UTI
- Sangue Oculto nas Fezes e Calprotectina Fecal — Exames de Fezes — risco
  de sangramento por AINEs/AAS/anticoagulantes e monitorização de doença
  inflamatória intestinal (mesalazina, biológicos)

Todo o conteúdo clínico (valores de referência, causas de alteração,
interferentes, medicamentos relacionados) foi redigido com base em
literatura de referência em química clínica/farmacologia e diretrizes de
sociedades médicas brasileiras e internacionais (ver campo `fontes` de
cada exame) — **sempre revise e atualize com a diretriz vigente mais
recente antes de expandir o conteúdo**, e prefira sempre o intervalo de
referência do laboratório do paciente ao interpretar um resultado real.

## Favoritos, histórico e comparador de resultados

Esses três recursos usam `localStorage` do navegador (chaves
`farmalab-favoritos`, `farmalab-historico`, `farmalab-comparador`,
`farmalab-balcao`) — são individuais por navegador/dispositivo, não exigem
login e não trafegam para nenhum servidor. Isso significa que também **não
sincronizam** entre computadores/celulares diferentes do mesmo usuário —
uma melhoria futura possível é integrar com alguma conta/backend do
FarmaPrática, caso a plataforma venha a ter um sistema de usuários.

## Link na página inicial

O card "Exames Laboratoriais" em `- INDEX/index.html` foi atualizado para
apontar para `exames/` (removido o estado `placeholder`/badge "Em breve").
