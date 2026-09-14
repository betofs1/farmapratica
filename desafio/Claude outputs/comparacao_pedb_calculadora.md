# Comparação PEDB × Calculadora de Doses (FarmaPrática) — Medicamentos Gratuitos

Comparação das posologias/cálculos dos 20 itens listados na seção "Medicamentos Gratuitos" do PEDB (pedb.com.br/medicamentos/painel) com os dados equivalentes da sua página **Calculadora de Doses** (`dosespediatricas/dados.json`).

**Observação metodológica:** o PEDB, sem peso/idade informados no formulário, às vezes exibe a fórmula mg/kg (ex.: Ibuprofeno, Paracetamol, Dipirona, Amoxicilina, Azitromicina) e às vezes exibe apenas um exemplo de dose fixa/padrão sem revelar a fórmula subjacente (ex.: Ambroxol, Cetirizina, Loratadina, Salbutamol xarope). Nesses casos, a comparação de faixas mg/kg não é possível diretamente — comparei o que estava disponível.

---

## 1. Ibuprofeno

- **PEDB:** 5–10 mg/kg/dose, 6/6h ou 8/8h, máx. 40 mg/kg/dia (não exceder 1200 mg/dia). Tetos por apresentação: gotas 200 mg/dose, xarope 210 mg/dose, EV 400 mg/infusão.
- **Minha calculadora:** 5–10 mg/kg/dose, 4x/dia, dose máx. 400 mg/dose, máx. 1200 mg/dia. Idade mínima 6 meses.
- **Avaliação:** faixa mg/kg e teto diário (1200 mg) coincidem. Diferença: meu teto por dose é fixo em 400 mg para todas as formulações orais, enquanto o PEDB aplica tetos menores (200–210 mg) nas apresentações líquidas — provavelmente limitado pelo volume prático do frasco, não por uma restrição clínica adicional. Sem inconsistência clínica relevante.

## 2. Paracetamol

- **PEDB:** 10–15 mg/kg/dose, 4/4h ou 6/6h, máx. 75 mg/kg/dia. Tetos por dose variam: gotas 750 mg (≥12 anos: 1000 mg), suspensão 32 mg/mL até 960 mg, suspensão 100 mg/mL até 1000 mg.
- **Minha calculadora:** 10–15 mg/kg/dose, até 5x/dia, dose máx. 750 mg/dose, máx. 3000 mg/dia (pediátrico). Adulto (≥50 kg): 500–1000 mg, 4x/dia, máx. 4000 mg/dia.
- **Avaliação:** faixa mg/kg igual. **Diferença a revisar:** minha calculadora aplica teto fixo de 750 mg/dose para todo o público pediátrico, mas o PEDB permite até 1000 mg/dose em formulações mais concentradas (provavelmente para adolescentes/crianças maiores, pré-transição). Vale confirmar se sua "Regra de Ouro" (trava no teto adulto) já cobre esse intervalo de 12–17 anos de forma equivalente, ou se crianças de 40–49 kg ficam sub-dosadas por herdar o teto de 750 mg em vez de subir até 1000 mg antes da transição para o modo adulto.

## 3. Dipirona (Metamizol)

- **PEDB:** 10–15 mg/kg/dose, máx. 4 doses/dia (6/6h). Contraindicado <3 meses ou <5 kg. Tetos por dose: xarope/gotas até 1000 mg/dose (40 gotas ou 20 mL).
- **Minha calculadora:** 10–15 mg/kg/dose, 4x/dia, dose máx. **500 mg/dose**, máx. **2000 mg/dia** (pediátrico). Idade mínima 3 meses.
- **Avaliação:** faixa mg/kg e idade mínima (3 meses) coincidem. **Discrepância relevante:** meu teto por dose (500 mg) e diário (2000 mg) são a metade do que o PEDB permite (1000 mg/dose, até 4000 mg/dia com 4 tomadas). Isso significa que uma criança mais pesada (por ex. 35–40 kg, onde 15 mg/kg ultrapassaria 500 mg) seria limitada artificialmente pela minha calculadora antes de atingir o teto que o PEDB considera seguro. Recomendo revisar a fonte (bula Novalgina) para confirmar se o teto de 500 mg/dose é uma escolha deliberada mais conservadora ou uma pendência a corrigir.

## 4. Amoxicilina

- **PEDB (Otite Média Aguda):** 40–50 mg/kg/dia, 8/8h ou 12/12h, máx. 500 mg/dose. Para ≥40 kg, usar posologia adulta.
- **Minha calculadora:** 20–50 mg/kg/dia, fracionado em 3x/dia (8/8h), máx. 1750 mg/dia.
- **Avaliação:** minha faixa (20–50 mg/kg/dia) é mais ampla porque cobre indicações gerais, não só OMA — o PEDB documenta especificamente a dose "alta" de OMA (40–50). Já há uma nota em `observacoesExtras` mencionando 80–90 mg/kg/dia para OMA "a confirmar protocolo" — o valor do PEDB (40–50) é mais moderado que essa nota antiga; vale reconciliar as duas fontes. Fracionamento: PEDB aceita tanto 8/8h quanto 12/12h; minha calculadora está fixa em 3x/dia — poderia permitir 12/12h como alternativa, especialmente para uso ≥40 kg.

## 5. Amoxicilina + Clavulanato

- **PEDB:** 25–45 mg/kg/dia (componente amoxicilina), **máx. 2 g/dia**. 8/8h ou 12/12h conforme apresentação. Para ≥40 kg, usar posologia adulta.
- **Minha calculadora:** 25–45 mg/kg/dia, fracionado em 2x/dia, **máx. 1750 mg/dia**.
- **Avaliação:** faixa mg/kg idêntica. **Discrepância a revisar:** teto diário do PEDB é 2000 mg, o meu é 1750 mg — 250 mg de diferença que pode subdosar uma criança próxima do teto de peso pediátrico antes da transição para adulto. Fracionamento também diverge (PEDB aceita 8/8h ou 12/12h; minha calculadora está fixa em 2x/dia).

## 6. Azitromicina

- **PEDB:** 10 mg/kg/dia no 1º dia, seguido de 5 mg/kg/dia nos dias 2–5 (esquema clássico), máx. 500 mg/dia.
- **Minha calculadora:** 10 mg/kg/dia (dia 1), 1x/dia, máx. 500 mg/dia; observação registra o mesmo esquema clássico (10 mg/kg dia 1, 5 mg/kg dias 2–5).
- **Avaliação:** coincidência total. Nenhuma discrepância.

## 7. Cefalexina

- **PEDB:** "Dose geral" — volumes de suspensão (250 mg/5 mL e 500 mg/5 mL) a cada 6h, sem exibir a fórmula mg/kg/dia sem peso informado.
- **Minha calculadora:** 25–50 mg/kg/dia, fracionado em 4x/dia (6/6h), máx. 4000 mg/dia; observação menciona até 100 mg/kg/dia em infecções graves "a confirmar protocolo".
- **Avaliação:** o intervalo de 6/6h coincide. Não foi possível comparar a faixa mg/kg diretamente pois o PEDB não exibiu a fórmula nesta consulta sem peso. Sem inconsistência identificável com os dados disponíveis.

## 8. Cetirizina

- **PEDB:** "Rinite Alérgica" — comprimido 10 mg 1x/dia; solução oral 1 mg/mL, 10 mL/dia em até 2 doses (exemplo padrão, sem discriminar por idade nesta tela).
- **Minha calculadora:** dose fixa por faixa etária — mas a estrutura de dados tem **uma única faixa** (`doseMg: 5`, válida para qualquer peso), embora a descrição registrada no próprio arquivo diga "2–6 anos: 2,5–5 mg/dia | ≥6 anos: 5–10 mg/dia (ajustar pela idade)".
- **⚠️ Ponto a verificar no site:** a *descrição* da faixa reconhece dois patamares etários, mas o *dado estruturado* (`doseBase.faixas`) só tem um valor fixo (5 mg), sem uma segunda faixa para ≥6 anos com 10 mg. Se a lógica de cálculo do site não tiver um tratamento especial em código para elevar a dose a partir dos 6 anos, crianças maiores podem estar recebendo sistematicamente a dose mínima (5 mg) em vez de até 10 mg/dia. Vale conferir o comportamento real da calculadora para uma criança de, por exemplo, 8 anos.

## 9. Desloratadina

- **PEDB:** "Rinite alérgica" — xarope 0,5 mg/mL: 10 mL 24/24h; comprimido 5 mg 1x/dia; gotas 1,25 mg/mL: 80 gotas 24/24h (exemplos padrão, sem discriminar por idade nesta tela).
- **Minha calculadora:** faixa etária bem detalhada — 6–11 meses: 1 mg; 1–5 anos: 1,25 mg; 6–11 anos: 2,5 mg; ≥12 anos: 5 mg. Idade mínima 6 meses.
- **Avaliação:** minha calculadora é mais granular/completa que o exemplo padrão mostrado pelo PEDB nesta tela (que parece assumir o paciente maior, dose de 5 mg). Nenhuma inconsistência encontrada — minha estruturação parece mais alinhada à bula do Desalex (com faixas por idade) do que o exemplo único exibido pelo PEDB.

## 10. Dexclorfeniramina

- **PEDB:** quatro apresentações documentadas, incluindo um **alerta de segurança explícito**: *"Não confundir com a solução 0,4 mg/mL: gotas 2,8 mg/mL são sete vezes mais concentradas."* Regimes: gotas 2,8 mg/mL (20 gotas 8/8h ≈ 2 mg/dose); comprimido 2 mg (8/8h); drágea LP 6 mg Repetabs® (>12 anos, 12/12h); xarope/gotas 0,4 mg/mL do SUS (5 mL 8/8h, contraindicado <2 anos).
- **Minha calculadora:** 0,15–0,3 mg/kg/dia, fracionado em 3x/dia, máx. 12 mg/dia. Formulações cadastradas: apenas xarope 2 mg/5 mL (0,4 mg/mL) e comprimido 2 mg. Idade mínima 24 meses.
- **⚠️ Lacuna de conteúdo relevante:** minha calculadora não cadastra a apresentação em **gotas 2,8 mg/mL**, nem o alerta do PEDB sobre a confusão entre as duas concentrações de gotas (0,4 mg/mL vs. 2,8 mg/mL — risco de erro de dose em 7x). Isso é uma informação de segurança valiosa para incluir, especialmente por já existir no seu projeto uma pendência de revisão sobre dexclorfeniramina (a combinação com betametasona, registrada em `review_notes.json`). Sugiro adicionar essa apresentação e o alerta de concentração.
- Doses convertidas coincidem com meu teto diário (2 mg × 3–4x/dia ≤ 12 mg/dia).

## 11. Loratadina

- **PEDB:** comprimido 10 mg 1x/dia; xarope 1 mg/mL, 10 mL 1x/dia (exemplo padrão único, sem discriminar por peso nesta tela).
- **Minha calculadora:** faixa fixa por peso — <30 kg: 5 mg; ≥30 kg: 10 mg. Idade mínima 24 meses.
- **Avaliação:** minha calculadora está mais alinhada à bula (que de fato prevê 5 mg para crianças menores) do que o exemplo único do PEDB (que mostra apenas a dose de 10 mg, provavelmente por assumir peso não informado ou paciente maior). Sem inconsistência clínica — meu dado é mais completo.

## 12. Ondansetrona

- **PEDB:** "Dose Geral" com regime repetido a cada 8h: xarope 4 mg/5 mL (10 mL 8/8h); injetável 2 mg/mL (3,75 mL EV 8/8h conforme necessidade); comprimido orodispersível 4 mg (2 comp. sublingual 8/8h = 8 mg/dose).
- **Minha calculadora:** 0,15 mg/kg/**dose única** (não fracionada — vezesDia: 1), dose máx. 8 mg, máx. 24 mg/dia. Idade mínima 6 meses.
- **Avaliação — diferença de filosofia de uso:** minha calculadora modela ondansetrona como antiemético de **dose única** (padrão para gastroenterite aguda em pronto-socorro/emergência), enquanto o PEDB apresenta um **regime repetido 8/8h** (até 3x/dia). Os valores de teto batem (8 mg/dose e até 24 mg/dia no PEDB via 3 doses de 8 mg), mas a intenção de uso é diferente. Vale decidir explicitamente se sua página deve continuar limitada à dose única (mais comum na prática de balcão/PA) ou também contemplar o esquema de repetição do PEDB.

## 13. Prednisolona

- **PEDB ("Asma <12 anos"):** xarope 3 mg/mL e gotas 11 mg/mL, 1–2x/dia, por 3 a 10 dias (sem exibir a fórmula mg/kg sem peso informado, mas indicação restrita a asma).
- **Minha calculadora:** 1–2 mg/kg/dia, dose única diária, máx. 60 mg/dia. Observação: "curso curto (crise asmática/laringite): 3–5 dias, geralmente sem necessidade de desmame". Idade mínima 0.
- **Avaliação:** faixa mg/kg provavelmente compatível (não confirmável sem a fórmula do PEDB nesta tela). Pequena diferença de duração: minha nota sugere 3–5 dias, o PEDB permite até 10 dias — ambos plausíveis conforme protocolo/gravidade; não é uma contradição, apenas uma faixa mais ampla no PEDB.

## 14. Salbutamol

- **PEDB:** injetável 0,5 mg/mL (0,5 mL EV em 10 min); xarope 2 mg/5 mL (exemplo fixo "10 mL 8/8h", sem fórmula mg/kg exibida); **nebulização 5 mg/mL** (diluir 0,5 mL/10 gotas em SF 0,9% até 2,5 mL, 6/6h); spray 100 mcg (1–2 jatos 6/6h).
- **Minha calculadora:** 0,1–0,15 mg/kg/dose, 4x/dia, dose máx. 4 mg. Formulações cadastradas: xarope 2 mg/5 mL (6–8h) e spray 100 mcg/dose ("1–2 jatos a cada 4–6 horas").
- **⚠️ Lacuna de conteúdo:** minha calculadora **não tem uma formulação de nebulização/solução inalatória** para salbutamol, que é exatamente a via preferencial em crise aguda (e que o PEDB documenta). Vale considerar adicionar essa apresentação.
- **Pequena diferença de intervalo do spray:** PEDB registra 6/6h fixo; minha calculadora registra "4–6 horas" (intervalo mais flexível/curto). Não é necessariamente um erro, mas vale confirmar qual reflete melhor a bula/uso em crise.

## 15. Bromoprida

- **PEDB:** solução oral 1 mg/mL (8–10 mL 8/8h); gotas 4 mg/mL (50–58 gotas 8/8h); injetável 5 mg/mL (1,5–3 mL IM/EV 8/8h) — sem fórmula mg/kg exibida nesta tela.
- **Minha calculadora:** dose "individualizada" com cálculo especial por gotas/kg; contraindicado <1 ano; dose adulto de referência 10 mg 3x/dia, máx. 60 mg/dia.
- **Avaliação:** ambas as fontes tratam a bromoprida como cálculo não-linear/especial (gotas por peso), consistente entre si. Sem dados suficientes do PEDB para comparação quantitativa mais fina.

## 16. Soro de Reidratação Oral (SRO)

- **PEDB:** regra simples — oferecer 100–200 mL após cada episódio de evacuação/vômito.
- **Minha calculadora:** modelo estruturado da OMS/Ministério da Saúde — **Plano A** (prevenção em casa): ≈10 mL/kg por episódio, com faixas específicas por idade (<1 ano: 50–100 mL; 1–10 anos: 100–200 mL; >10 anos: à vontade); **Plano B** (unidade de saúde): 50–100 mL/kg em 4–6h fracionado a cada 10–15 min.
- **Avaliação:** sua calculadora é **substancialmente mais completa e melhor referenciada** (cita diretamente o guia de Diarreia Aguda do MS/OMS/SBP) do que o dado simplificado do PEDB, que corresponde apenas à faixa "1–10 anos" do seu Plano A. Nenhuma ação necessária — ponto positivo do seu conteúdo.

## 17. Ambroxol

- **PEDB:** quatro apresentações com doses fixas de exemplo (sem fórmula mg/kg exibida sem peso): xarope infantil 30 mg/5 mL (2,5 mL 8/8h); solução inalatória 7,5 mg/mL (2–3 mL, 1–2x/dia); gotas 7,5 mg/mL (100 gotas 8/8h); xarope 15 mg/5 mL (indicado até 12 anos).
- **Minha calculadora:** 1,2–1,6 mg/kg/dia, fracionado em 2x/dia, máx. 90 mg/dia. Formulações: xarope infantil 3 mg/mL, xarope adulto 6 mg/mL, comprimido 30 mg.
- **Avaliação:** não foi possível confirmar a fórmula mg/kg do PEDB nesta tela para comparação direta. Note que o PEDB tem uma apresentação de **solução inalatória** (7,5 mg/mL) que não consta na sua calculadora — possível lacuna de conteúdo a avaliar, embora o uso inalatório de ambroxol seja menos comum na prática brasileira atual.

---

## Medicamentos do PEDB "Gratuitos" ausentes da sua Calculadora de Doses

Três itens da lista de gratuitos do PEDB não têm entrada correspondente no seu banco de 72 fármacos:

1. **Adrenalina** — Anafilaxia: 0,01 mg/kg/dose IM, máx. 0,3 mg, a cada 5–15 min (apresentação IM/SC 1 mg/mL).
2. **Butilbrometo de escopolamina** — Cólicas gastrointestinais: gotas 10 mg/mL (20 gotas, repetir 3x/dia), drágea 10 mg (1–2 drágeas, 3–5x/dia), injetável 20 mg/mL.
3. **Dexametasona** — Anti-inflamatório: elixir 0,1 mg/mL (12,5 mL 6/6h), injetável 2 mg/mL (2 mL IM/EV em 2–3 doses).

São três fármacos de uso relativamente comum na prática pediátrica/emergência (adrenalina em anafilaxia é especialmente crítica) — podem ser candidatos a inclusão futura na Calculadora de Doses, caso o escopo da página seja expandido além do uso ambulatorial/balcão atual.

---

## Resumo dos pontos que merecem revisão prioritária

1. **Dipirona:** teto por dose (500 mg) e diário (2000 mg) da sua calculadora são metade do que o PEDB documenta (1000 mg/dose, 4000 mg/dia) — maior prioridade de verificação.
2. **Cetirizina:** a estrutura de dados só registra uma faixa de dose fixa (5 mg), apesar de a própria descrição mencionar até 10 mg/dia para ≥6 anos — possível sub-dosagem não intencional para crianças maiores.
3. **Dexclorfeniramina:** falta a apresentação em gotas concentradas (2,8 mg/mL) e o alerta de segurança do PEDB sobre confusão de concentração com a solução 0,4 mg/mL.
4. **Amoxicilina + Clavulanato:** teto diário (1750 mg) é 250 mg menor que o do PEDB (2000 mg).
5. **Paracetamol:** teto fixo de 750 mg/dose pode ser conservador demais para crianças maiores/mais pesadas, frente aos 1000 mg/dose do PEDB.
6. **Salbutamol:** ausência de formulação para nebulização (via preferencial em crise aguda).
7. **Ondansetrona:** diferença de filosofia (dose única vs. regime repetido 8/8h) — vale decisão consciente, não necessariamente um erro.

Os demais itens (Ibuprofeno, Azitromicina, Loratadina, Desloratadina, SRO, Bromoprida) apresentaram boa concordância ou dados equivalentes/superiores na sua calculadora.
