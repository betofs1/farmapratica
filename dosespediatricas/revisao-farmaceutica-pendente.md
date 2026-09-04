# Revisão Farmacêutica Pendente — Calculadora de Doses

Este documento reúne os pontos levantados durante a pesquisa de literatura que fundamentou as novas doses de adulto (e a revisão da base pediátrica existente) na Calculadora de Doses. São **9 fármacos, de 72 pesquisados**, com sugestões ou divergências que exigem sua avaliação como farmacêutico responsável pela base antes de qualquer alteração — nada listado aqui foi modificado automaticamente no `dados.json`.

## 1. Amoxicilina + Clavulanato

A faixa pediátrica cadastrada (25–45 mg/kg/dia, base amoxicilina) está correta para o uso geral, mas diretrizes atuais (AAP Clinical Practice Guideline; Nelson's Pediatric Antimicrobial Therapy) recomendam dose alta de **90 mg/kg/dia dividida em 2x/dia** para otite média aguda em áreas com risco de pneumococo resistente, ou infecção grave/complicada. Sugestão: adicionar essa opção de alta dose como alternativa/observação, no mesmo padrão já usado para amoxicilina isolada.

## 2. Cetirizina

A faixa pediátrica usa um único valor fixo (5 mg/dia) para todo o intervalo pediátrico, mas a bula (Zyrtec/GSK) prevê 2,5–5 mg/dia para 2–6 anos e 5–10 mg/dia para ≥6 anos. Como está, uma criança maior pode ficar subdosada. Sugestão: desdobrar em duas faixas etárias reais em vez do valor único.

## 3. Dexclorfeniramina

A fórmula atual (0,15–0,3 mg/kg/dia) aplica um teto único de 12 mg/dia a qualquer idade pediátrica, mas a bula do Polaramine define tetos mais conservadores por faixa: 3 mg/dia (2–6 anos), 6 mg/dia (6–12 anos), 12 mg/dia (≥12 anos/adultos). Uma criança de maior peso na faixa 6–12 anos pode calcular acima do teto etário da bula. Sugestão: adicionar os tetos intermediários (3 mg / 6 mg) além do teto absoluto de 12 mg/dia.

## 4. Dexclorfeniramina + Betametasona

O texto do comprimido no app indica "máx. 4 comprimidos/dia", mas a bula do produto equivalente (Celestamine, mesma associação) define 1–2 comprimidos 3–4x/dia, com teto de **8 comprimidos/dia** — confirmado em duas fontes independentes. Sugestão: corrigir o texto para "máx. 8 comprimidos/dia", mantendo a contraindicação já cadastrada para menores de 12 anos.

## 5. Fexofenadina

A faixa "≥12 anos/adultos" usa dose fixa de 60 mg a cada 12h (120 mg/dia). A bula também prevê 120 mg ou 180 mg 1x/dia para rinite alérgica e, especificamente, **180 mg 1x/dia (não 60 mg 2x/dia) para urticária idiopática crônica**. O comprimido de 180 mg (Allegra 180 mg) existe no mercado brasileiro e não está cadastrado em `formulacoes`. Sugestão: avaliar se vale adicionar essa apresentação e diferenciar a indicação de urticária.

## 6. Racecadotrila

O `doseBase` pediátrico não tem `doseMaximaDiaMg` explícito — só `doseMaximaDoseMg:100` — deixando o teto diário implícito apenas pelo cálculo dinâmico (1,5 mg/kg x3/dia). A bula do Tiorfan pediátrico expressa o teto de forma aproximada (~6 mg/kg/dia) ou em faixas fixas: <9kg → 30 mg/dia; 9–13kg → 60 mg/dia; 14–27kg → 90 mg/dia; >27kg até 12 anos → 180 mg/dia. Sugestão: adicionar um `doseMaximaDiaMg` explícito para reforçar a trava de segurança.

## 7. Nistatina (suspensão oral)

A faixa cadastrada (100.000–400.000 UI, 4x/dia) está dentro do aprovado em bula, mas é mais conservadora que o teto de bula para crianças maiores/adultos, que chega a 600.000 UI (6 mL) por aplicação, 4x/dia. **Não é um erro** — 400.000 UI é dose eficaz e segura —, mas é uma decisão sua se quer ampliar o teto para adolescentes/casos avaliados clinicamente.

## 8. Miconazol (gel oral)

A bula do Daktarin Gel Oral orienta 4x/dia mesmo nas faixas mais jovens (6–24 meses: 1,25 mL 4x/dia; ≥2 anos: 2,5 mL 4x/dia), enquanto o cadastro atual usa 2x/dia para <24 meses e 24–72 meses. Isso pode ser uma escolha deliberada de segurança — reduzir frequência em lactentes pelo risco de engasgo/aspiração, alinhado a alertas de segurança da MHRA (2011/2012) para miconazol oral em lactentes — e não necessariamente um erro. **Recomendo decidir explicitamente qual referência seguir** (bula do fabricante vs. alerta de segurança) antes de qualquer alteração.

## 9. Cloranfenicol (colírio) — divergência regulatória, atenção

As bulas nacionais consultadas (Cloranfenicol Neo Química e Cloranfenicol Allergan, ambas com ácido bórico/borato de sódio no veículo) trazem indicação restrita a **"uso adulto"**, sem posologia pediátrica estabelecida. A ficha atual do app permite qualquer idade (`idadeMinimaMeses: 0`), citando "Bula ANVISA / Pediamécum (AEP)" como fonte. O uso pediátrico é prática comum e descrita em referências internacionais (AEP/Pediamécum, UpToDate), mas é tecnicamente **off-label frente à bula brasileira registrada**, por conta do ácido bórico (risco teórico de acidose bórica com absorção sistêmica repetida). Nada foi alterado na ficha (idade mínima mantida). Sugestões: (1) confirmar se a formulação efetivamente dispensada contém ácido bórico antes de indicar em lactentes/RN; (2) considerar adicionar um aviso de "uso off-label em pediatria" mantendo a orientação clínica atual, já que é prática consolidada na literatura pediátrica.

---

## Observação metodológica

Estes 9 itens foram os únicos, dos 72 fármacos pesquisados, em que a pesquisa de literatura para a dose de **adulto** identificou também uma possível divergência ou oportunidade de refinamento na dose **pediátrica** já existente na base — a pesquisa foi deliberadamente conservadora: nenhuma dose pediátrica foi alterada automaticamente, mesmo quando a sugestão parecia clara, para que a decisão final fique com você. Os demais 63 fármacos tiveram a dose pediátrica confirmada como compatível com a literatura consultada, sem achados que justificassem sinalização.
