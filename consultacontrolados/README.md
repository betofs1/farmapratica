# Módulo Controlados — FarmaPrática

Consulta de medicamentos controlados e antimicrobianos (tipo de receita, vias,
validade, retenção, classe terapêutica e busca por nome comercial). Este
documento explica como manter os dados atualizados.

> **Versão simplificada (nov/2026):** o pipeline original tinha 8 arquivos e
> um ciclo de 5 passos. Esta versão faz o mesmo trabalho em **3 scripts + 2
> arquivos de curadoria + este README**, num ciclo de 2–3 passos. O que
> mudou e por quê está explicado ao longo do documento.

## As três fontes de dados

| O quê | Fonte | O que ela cobre |
|---|---|---|
| Substâncias controladas (A1, A2, A3, B1, B2, C1, C2, C3, C5) | **Portaria SVS/MS 344/98**, Anexo I | Entorpecentes, psicotrópicos, retinoides, imunossupressores, anabolizantes |
| Antimicrobianos | **Instrução Normativa nº 360/2025** | Antibióticos e afins sujeitos a receita com retenção de 2ª via |
| Nomes comerciais (marca → substância) | **CMED/ANVISA** (mesmo banco usado no módulo Equivalentes) | Cruza os 25 mil+ medicamentos registrados com as ~607 substâncias rastreadas acima |

A Portaria 344/98 é a norma "mãe" de controlados desde 1998, atualizada
periodicamente por RDCs. Os antimicrobianos mudaram de casa ao longo do tempo:
eram um anexo dentro da RDC 20/2011; essa RDC foi revogada pela RDC 471/2021,
e a lista de substâncias passou a viver numa Instrução Normativa separada
(hoje a 360/2025). O CMED não é uma norma de controle, é só a base de
preços/registros que já alimenta o módulo Equivalentes — reaproveitada aqui
só para descobrir qual nome comercial corresponde a qual substância
rastreada.

## Arquivos do módulo

Mantenha estes arquivos na mesma pasta do `index.html`:

```
atualizar_fontes.py            → busca as duas normas (Portaria + IN) e gera controlados.json
gerar_marcas.py                 → cruza o CMED com as substâncias rastreadas
atualizar_pagina.py             → injeta os dados direto no index.html real
detalhes_farmacologicos.json    → classe/indicações/mecanismo (edite direto, é dado, não código)
excecoes.json                   → casos pontuais de quantidade máxima/observação (edite direto)
README.md                       → este guia
```

Arquivos gerados pelo processo (não editar manualmente):

```
controlados.json    → Portaria 344/98 + IN antimicrobianos + curadoria, mesclados
marcas.json          → nome comercial → substância, gerado do CMED
index.html.bak       → cópia de segurança do index.html de antes da última injeção
```

### O que foi simplificado, e por quê

- **3 scripts de busca/estrutura em 1** (`atualizar_fontes.py` substitui
  `atualiza_controlados.py` + `atualiza_antimicrobianos.py` +
  `estrutura_controlados.py`): as duas normas são buscadas e mescladas num
  só passo, já comparando com a captura anterior e avisando no terminal
  o que mudou — sem precisar guardar `controlados_YYYYMMDD.json` por data,
  porque isso é publicado no GitHub, e o **histórico de versões já é o
  próprio histórico do git**.
- **Sem `template_consulta.html` nem `gerar_pagina.py`**: esse arquivo de
  molde visual, separado da página real, se perdeu numa sincronização e
  arriscava ficar desatualizado em relação ao design de verdade mesmo
  quando existia. O novo `atualizar_pagina.py` edita o **próprio
  `index.html` em produção**, no lugar — localizando e substituindo só o
  conteúdo dos blocos `<script type="application/json" id="dados-controlados">`
  e `id="dados-marcas">` que já existem na página. Ele faz backup
  automático (`index.html.bak`) antes de gravar e confere, depois, que o
  resto do arquivo (todo o HTML/CSS/JS visual) ficou **byte a byte igual**
  — só os dois blocos de dados mudam.
- **`gerar_detalhes.py` e `gerar_excecoes.py` viraram arquivos de dado
  puro**: antes, cada curadoria nova exigia editar um script Python,
  rodá-lo e rodar de novo o `estrutura_controlados.py` pra mesclar.
  Agora `detalhes_farmacologicos.json` e `excecoes.json` são lidos
  diretamente pelo `atualizar_fontes.py` — editar o JSON já é a curadoria,
  sem passo intermediário.

## Como funciona a atualização, passo a passo

O ciclo completo, sempre que quiser atualizar:

```
python3 atualizar_fontes.py
python3 gerar_marcas.py        # opcional — só se o CMED mudou desde a última vez
python3 atualizar_pagina.py
```

**O que cada um faz:**

1. `atualizar_fontes.py` busca o texto da Portaria 344/98 e da IN vigente
   sobre antimicrobianos, mescla com `detalhes_farmacologicos.json` e
   `excecoes.json` (se existirem), compara com o `controlados.json`
   anterior e avisa no terminal se alguma substância foi adicionada ou
   removida de alguma lista — e grava o `controlados.json` final.
2. `gerar_marcas.py` procura o `medicamentos.json` do CMED primeiro nesta
   pasta e, se não achar, em `../medinter/medicamentos.json` (o mesmo
   arquivo do módulo Equivalentes — não precisa copiar manualmente se ele
   já está atualizado lá). Cruza com o `controlados.json` e gera
   `marcas.json`.
3. `atualizar_pagina.py` lê `controlados.json` e `marcas.json`, faz backup
   do `index.html` atual (`index.html.bak`), injeta os dados novos nos
   blocos já existentes da página e confere que o resto do arquivo não
   mudou. Mostra antes/depois dos totais (listas, substâncias, detalhes,
   exceções, marcas).

Os passos 2 e o carregamento de `detalhes_farmacologicos.json`/
`excecoes.json` no passo 1 são opcionais: se o arquivo correspondente não
existir, o script avisa no terminal e segue sem quebrar — só fica sem
aquela parte da informação naquela geração.

**Importante:** `atualizar_fontes.py` precisa de internet normal, de fora de
qualquer sandbox/ambiente restrito — os dois sites da ANVISA (Datalegis) não
são alcançáveis de dentro de assistentes de IA em nuvem. Rode-o direto no seu
computador.

## Exceções de adendo (`excecoes.json`) — validadas automaticamente

Cada substância cuja regra de dispensação muda por causa de um **adendo** da
Portaria 344/98 (ex.: codeína ≤100 mg → Receita de Controle Especial;
carisoprodol → sem retenção) tem uma entrada em `excecoes.json`. Desde
12/11/2026, toda entrada precisa trazer a **prova** de que o adendo ainda existe:

| Campo | Para que serve |
|---|---|
| `lista`, `adendo_item` | Onde está o adendo (ex.: `"B1"`, `"16"`) |
| `trecho_norma` | Trecho **literal** do adendo (acentos/maiúsculas não importam) |
| `fundamento` | Norma citada na tela |
| `verificado_em`, `revisar_ate` | Data da última conferência e prazo da próxima (≈6 meses) |
| `tipo` | `substitui` (troca a receita), `condicional` (depende de forma/dose) ou `restricao` (mesma receita, restrição de dispensação) |
| `rotulo`, `titulo`, `tag` | Textos opcionais exibidos na página |

A cada execução, `atualizar_fontes.py` confere cada exceção contra o adendo
**recém-capturado**. Se o item tiver virado "(Excluído)", se o trecho não for
mais encontrado ou se a substância saiu da lista, aparece **ERRO** e o
`controlados.json` **não é gravado**. O `atualizar_pagina.py` repete essa
conferência e também se recusa a publicar se `excecoes.json` foi editado sem
rodar o passo anterior. São **avisos** (não bloqueiam): o prazo `revisar_ate`
vencido, o trecho ter mudado de número (renumeração) e um adendo novo que cita
uma substância com regra especial ainda sem exceção cadastrada.

O relatório de mudanças agora compara também os **adendos**, item por item,
e não só os nomes das substâncias. Foi exatamente uma revogação de adendo
(item 4 da B1, zolpidem/zaleplona, RDC 871/2024) que passou despercebida antes.

Depois de editar `excecoes.json` sem precisar baixar as normas de novo:

```
python3 atualizar_fontes.py --sem-rede
python3 atualizar_pagina.py
```

## Quando rodar isso

- **`atualizar_fontes.py`** — tem aviso automático embutido: quando detecta
  mudança desde a última captura, lista exatamente o que foi adicionado ou
  removido, lista por lista. Rotina sugerida: 1x por mês.
- **`gerar_marcas.py`** — só precisa rodar de novo quando o
  `medicamentos.json` do módulo Equivalentes for atualizado (base CMED
  mensal, por exemplo).
- **Curadoria em `detalhes_farmacologicos.json`/`excecoes.json`** — edite
  quando quiser, a qualquer momento; não tem ciclo fixo. Depois de editar,
  rode o ciclo completo (os 3 passos) de novo pra levar a mudança pro
  `index.html`.

Se nada mudou nas duas normas, não precisa rodar os passos seguintes — só
regenera a página quando algo realmente mudou.

### Agendando a checagem mensal

**Windows** — Agendador de Tarefas → criar tarefa nova → rodar
`atualizar_fontes.py` uma vez por mês.

**Mac/Linux** — `crontab -e` e adicionar:
```
0 9 1 * * cd /caminho/da/pasta && python3 atualizar_fontes.py
```

## Antes de publicar uma atualização

1. Rode `atualizar_fontes.py` e leia o que ele reportou de mudança (se
   houver) — ele já compara com a captura anterior automaticamente.
2. Confirme contra o texto oficial antes de publicar:
   - Portaria 344/98:
     `https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/controlados/lista-substancias`
   - IN 360/2025 (ou a que vier substituí-la): busque no Datalegis da ANVISA
     por "Instrução Normativa antimicrobianos ANVISA"
3. Rode `atualizar_pagina.py` e confira a página no navegador.
4. Se algo ficou errado, restaure o backup: `cp index.html.bak index.html`
   (ou `git checkout -- index.html`, já que o git também guarda a versão
   anterior publicada).
5. `git add`, `commit` e `push` normalmente para publicar no GitHub Pages.

**Não precisa mais guardar captura por data manualmente** — isso é o que o
histórico do git já faz, de forma mais confiável.

## Se a IN sobre antimicrobianos for revogada

1. Abra `atualizar_fontes.py`
2. Troque a variável `URL_IN_ANTIMICROBIANOS` (número da IN e ano) pela
   norma nova, mantendo o resto da URL igual
3. Rode de novo pra confirmar que a extração funciona com o novo texto

## Classe terapêutica, indicações e mecanismo de ação

Esse campo **não é gerado automaticamente** — é curadoria manual, guardada
direto em `detalhes_farmacologicos.json` (chave = nome da substância em
minúsculas, igual aparece na lista; valores: `classe`, `indicacoes`,
`mecanismo`).

As substâncias sem curadoria (a maioria das listas A1, B1 e C1 — muitas são
variantes químicas raras, sem uso clínico corrente ou produto registrado no
Brasil) aparecem na página como "não documentado", com link direto pra bula,
em vez de arriscar uma informação clínica incorreta.

**Para expandir a cobertura:** edite `detalhes_farmacologicos.json`
diretamente, seguindo o padrão das entradas existentes, e rode
`atualizar_fontes.py` + `atualizar_pagina.py` de novo. Sempre baseie o
conteúdo em fonte farmacológica confiável (bula, Micromedex, UpToDate,
literatura padrão) — nunca preencha por suposição.

## Busca por nome comercial

O `gerar_marcas.py` cruza o CMED (`medicamentos.json`) com as substâncias
rastreadas, gerando `marcas.json`.

**Como o cruzamento funciona:** para cada medicamento do CMED, verifica se o
campo "princípio ativo" contém uma das substâncias rastreadas (aceitando
formas com sal químico, nomes entre parênteses e variantes separadas por
"ou"). Marcas cujo nome já é igual ao princípio ativo (genéricos "puros")
não entram, só nomes comerciais de fato.

**Limitação conhecida:** o cruzamento é por correspondência textual, não por
uma base de sinônimos farmacológicos completa. Nomes com grafia muito
diferente do princípio ativo oficial podem não ser encontrados. Se notar uma
marca comum faltando, verifique o campo `principio` dela no
`medicamentos.json` e, se necessário, ajuste a função `gerar_candidatos()` em
`gerar_marcas.py`.

## Escopo dos dados

A consulta cobre as listas A1, A2, A3, B1, B2, C1, C2, C3 e C5 da Portaria
344/98 (medicamento efetivamente dispensável em farmácia com receita) mais os
antimicrobianos da IN vigente. As listas D1, D2, E e F da Portaria
(precursores químicos, insumos de síntese, plantas/fungos proscritos e
substâncias de uso proscrito) ficam de fora da consulta — não correspondem a
medicamento registrado que se dispensa com receita.

O campo "quantidade máxima por receita" não está incluído de forma geral:
não é fixa por lista, varia por substância específica, sem valor genérico
confiável (as poucas exceções pontuais onde isso é conhecido ficam em
`excecoes.json`).

## Fontes oficiais

- Portaria SVS/MS 344/98, Anexo I — versão vigente com alterações
  incorporadas, consultada via Datalegis (ANVISA)
- Instrução Normativa nº 360/2025 — lista de substâncias antimicrobianas de
  que trata a RDC nº 471/2021, consultada via Datalegis (ANVISA)
- CMED/ANVISA — Câmara de Regulação do Mercado de Medicamentos, mesma base
  usada no módulo Equivalentes do FarmaPrática
