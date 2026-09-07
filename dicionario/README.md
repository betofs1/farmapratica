# Módulo Dicionário Farmacêutico — FarmaPrática

Ferramenta de consulta rápida, didática e tecnicamente confiável de termos de
Farmacologia, Farmacocinética, Farmacodinâmica, Farmácia Clínica, Dispensação,
Farmacoterapia, Farmacovigilância, Toxicologia, Farmacotécnica, Controle de
Qualidade, Microbiologia, Imunologia, Fisiologia, Patologia/Fisiopatologia,
Semiologia, Legislação Farmacêutica, Saúde Pública, Vigilância Sanitária e
Gestão Farmacêutica.

**Não inclui a categoria Análises Clínicas** — esse conteúdo já é coberto em
profundidade pelo módulo `exames/` (FarmaLab), com valores de referência,
interpretação e interações com medicamentos.

**Sem Flashcards, Quiz, Favoritos ou Anotações** nesta primeira versão — a
prioridade foi um dicionário robusto, com busca inteligente e ficha de verbete
completa. Esses recursos ficam como candidatos naturais para uma Fase 2.

**Conteúdo educacional de apoio à prática farmacêutica** — não substitui bula
oficial, protocolo institucional ou a legislação sanitária vigente.

## Arquivos do módulo

```
index.html       → aplicação (HTML + CSS + JS), lê os dados de dicionario.json em tempo de execução
dicionario.json  → banco de dados de categorias, termos e comparações "não confunda"
logo.png         → logo da marca (mesma imagem usada nas demais ferramentas)
README.md        → este guia
```

Assim como `exames` e `interacoes`, este módulo carrega os dados via
`fetch('dicionario.json')` no carregamento da página — **por isso, para testar
localmente, é preciso servir a pasta por um servidor HTTP** (abrir o
`index.html` direto por duplo-clique bloqueia o `fetch` por política de CORS
do navegador para arquivos `file://`):

```
cd "- INDEX/dicionario"
python3 -m http.server 8000
# depois abrir http://localhost:8000/ no navegador
```

No site publicado (GitHub Pages), o `fetch` funciona normalmente sem nenhuma
configuração adicional.

## Estrutura de `dicionario.json`

```json
{
  "meta": {"versao": "1.0", "dataAtualizacao": "AAAA-MM-DD", "totalTermos": 293},
  "categorias": [ {"id","nome","cor","icone","descricao"} ],
  "termos": [ { ...ver campos abaixo... } ],
  "comparacoes": [ {"id","titulo","termos":["id1","id2"],"resumo","tabela":[{"aspecto","valores":[...]}]} ]
}
```

### Campos de cada termo (`termos[]`)

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | identificador único, minúsculo, sem espaços/acentos (usado em links internos) |
| `termo` | string | nome principal do verbete |
| `sigla` | string | sigla/abreviação principal, quando existir |
| `categoria` | string | precisa bater com um `id` existente em `"categorias"` |
| `sinonimos` | string[] | sinônimos técnicos ou termos equivalentes |
| `definicao` | string | definição técnica, objetiva e cientificamente correta |
| `explicacaoSimplificada` | string | explicação didática, em linguagem simples |
| `aplicacaoPratica` | string | onde o conceito aparece na rotina farmacêutica |
| `exemploPratico` | string | exemplo contextualizado de uso do conceito |
| `vocePrecisaSaber` | string | (opcional) 1–3 frases com o ponto mais importante a memorizar |
| `atencao` | string | (opcional) erros conceituais comuns, pegadinhas de prova, alertas |
| `naoConfunda` | string[] | (opcional) **ids** de entradas em `"comparacoes"` |
| `termosRelacionados` | string[] | (opcional) **ids** de outros termos já cadastrados (viram chips clicáveis) |
| `cascata` | objeto | (opcional, para classes farmacológicas) `{subclasse, mecanismo, exemplos:[], aplicacoes:[]}` |
| `fontes` | string[] | referências gerais usadas na redação do verbete |

Termos e comparações são renderizados dinamicamente — não é necessário editar
`index.html` para adicionar conteúdo novo, apenas `dicionario.json`.

### Categorias

O array `"categorias"` define as 20 categorias fixas da ferramenta. Cada uma
tem um campo `"cor"` (nome de uma paleta pré-definida no CSS: `red, blue,
purple, amber, green, sky, crimson, orange, cyan, teal, indigo, lime, magenta,
yellow, brown, petrol, slate, gray`) e um emoji de indicador visual definido
no objeto `CATEGORY_EMOJI` dentro do `<script>` do `index.html`. Categorias
sem nenhum termo cadastrado continuam aparecendo na barra lateral, com
contador "0" — proposital, mostra o escopo completo da ferramenta.

### Comparações ("Não Confunda")

Cada entrada em `"comparacoes"` compara 2 ou 3 termos (`"termos"`, na ordem
em que aparecem nas colunas da tabela) e é referenciada a partir do campo
`"naoConfunda"` dos termos envolvidos. A tabela (`"tabela"`) é uma lista de
linhas `{aspecto, valores:[...]}`, com um valor por termo comparado, na mesma
ordem de `"termos"`.

### Classificação em cascata

Termos que representam uma classe farmacológica (ex.: Betabloqueadores, IECA,
BRA, Estatinas, IBP, AINEs, Benzodiazepínicos, ISRS) podem incluir o campo
`"cascata"`, exibido como um fluxo Classe → Subclasse → Mecanismo → Exemplos →
Aplicações Clínicas na ficha do termo.

## Sistema de busca

Implementado em `index.html` (funções `buscaGlobal`, `normaliza`,
`levenshtein`): busca parcial e por sinônimos/siglas normalizando acentos e
maiúsculas/minúsculas, indexando também definição, explicação simplificada,
aplicação prática e exemplo prático (permite buscar por mecanismo, classe ou
condição clínica mencionados no verbete). Quando a busca não encontra
correspondência exata, sugere o termo mais próximo por distância de
Levenshtein ("Você quis dizer...?"), cobrindo erros de digitação. Autocomplete
em tempo real na barra lateral e na busca da página inicial. Histórico dos
últimos 10 termos consultados fica salvo em `localStorage`
(`farmadic-historico`) — individual por navegador/dispositivo, não sincroniza
entre aparelhos.

## Nível de complexidade

Cada ficha de termo tem um alternador ⚡ Rápido / 📚 Completo / 🎓 Estudo, que
controla quais blocos ficam visíveis (`data-min-nivel` no HTML de cada bloco):
Rápido mostra definição e aplicação prática; Completo adiciona explicação
simplificada, cascata, exemplo prático e "Você Precisa Saber"; Estudo também
mostra "Atenção" e a seção "Não Confunda".

## Estado atual do conteúdo (v1.0 — 07/09/2026)

293 termos distribuídos pelas 20 categorias, priorizando os conceitos de
maior relevância clínica, prática e de concursos públicos em cada área — não
é uma cobertura exaustiva de toda a terminologia listada na especificação
original (que somaria bem mais de 500 termos), e sim um núcleo robusto e
tecnicamente revisado, com a estrutura pronta para expansão. 37 comparações
"Não Confunda" e 8 classes farmacológicas com classificação em cascata
completa (Betabloqueadores, IECA, BRA, Estatinas, IBP, AINEs,
Benzodiazepínicos, ISRS).

Todo o conteúdo foi redigido com base em literatura de referência em
farmacologia, farmácia clínica e legislação sanitária brasileira (ver campo
`fontes` de cada termo) — **sempre revise e atualize com a fonte vigente mais
recente antes de expandir o conteúdo**, especialmente números de RDC/Portaria,
que podem ser revogados ou atualizados.

### Próximos candidatos naturais para expansão

- **Farmacologia por sistemas**: mais classes com cascata (anticoagulantes orais diretos, insulinas, broncodilatadores, antipsicóticos, opioides).
- **Legislação**: mais detalhamento de listas de substâncias controladas (A1/A2/A3/B1/B2/C1-C5) e RDCs específicas.
- **Semiologia/Fisiopatologia**: ampliar condições crônicas (DRC, hepatopatias, transtorno bipolar).
- **Flashcards, Quiz e Favoritos/Anotações**: recursos previstos na especificação original, propositalmente adiados para uma Fase 2, após validação do dicionário em uso real.

## Link na página inicial

O card "Dicionário Farmacêutico" em `- INDEX/index.html` foi atualizado para
apontar para `dicionario/` (removido o estado `placeholder`/badge "Em breve").
