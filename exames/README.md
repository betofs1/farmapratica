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

O array `"categorias"` no topo do `exames.json` define as 23 categorias
fixas da ferramenta (Hematologia, Bioquímica, Hormônios, Lipidograma,
Glicemia e Metabolismo, Função Renal, Função Hepática, Eletrólitos,
Marcadores Cardíacos, Marcadores Inflamatórios, Imunologia, Infectologia,
Coagulação, Endocrinologia, Vitaminas e Minerais, Marcadores Tumorais,
Urinálise, Parasitologia, Microbiologia, Gasometria, Exames de Fezes,
Imagem e Complementares, Outros). Categorias sem nenhum exame cadastrado
continuam aparecendo na barra lateral, com contador "0" e uma mensagem
"Nenhum exame cadastrado ainda nesta categoria" — isso é proposital
(mostra o escopo completo da ferramenta e convida a expandir o conteúdo).

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

## Estado atual do conteúdo (atualizado em 17/09/2026)

35 exames com todos os campos completos. Aos 20 originais — cobrindo os
itens listados como "Consulta Rápida"/"Mais Consultados": Hemograma,
Glicemia de Jejum, HbA1c, Colesterol Total, HDL, LDL, Triglicerídeos,
Creatinina, Ureia, TGO, TGP, GGT, TSH, T4 Livre, Vitamina D, Vitamina B12,
Ferritina, PCR, Sódio e Potássio — somaram-se, em 17/09/2026, 6 exames na
categoria Hematologia (a pedido do usuário, ao lado do Hemograma Completo,
mesmo tratando-se em parte de exames de coagulação): Tempo de Protrombina
(TP/RNI), Tempo de Tromboplastina Parcial Ativada (TTPA), Contagem de
Reticulócitos, Atividade Anti-Fator Xa, Atividade da G6PD e Dosagem de
D-Dímero.

Ainda em 17/09/2026, a categoria Bioquímica passou a ter 9 exames próprios:
Ácido Úrico, Fosfatase Alcalina, Bilirrubinas Totais e Frações, Lactato
Desidrogenase (LDH), Creatinoquinase Total (CK), Amilase, Lipase, Cálcio
Total e Magnésio. O usuário pediu originalmente 19 exames bioquímicos, mas
11 deles já existiam como páginas próprias em categorias mais específicas
(Glicose/Glicemia de Jejum, Ureia e Creatinina em Função Renal; TGO, TGP e
GGT em Função Hepática; Colesterol Total, HDL e Triglicerídeos em
Lipidograma; Sódio e Potássio em Eletrólitos) — para não duplicar
conteúdo, ficou definido (decisão explícita do usuário) manter esses 11
exames apenas em suas categorias originais, e adicionar à Bioquímica
somente os 9 exames que ainda não tinham página. Os cruzamentos
("correlatos") de TGO, TGP, GGT, Vitamina D, Triglicerídeos, Contagem de
Reticulócitos e G6PD foram atualizados para apontar, como links
clicáveis, para os novos exames de Bioquímica e Hematologia correlatos.

As demais categorias (Marcadores Cardíacos, Imunologia, Infectologia,
Coagulação, Urinálise, Parasitologia, Microbiologia, Gasometria, Fezes,
Imagem, Marcadores Tumorais, Endocrinologia além de TSH/T4L) estão
estruturadas na navegação, mas ainda sem exames — próximos candidatos
naturais: CK-MB e Troponina (cardíacos), Sorologias virais e VDRL
(infectologia), EAS/Urina tipo I (urinálise), PTH (endocrinologia).

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
