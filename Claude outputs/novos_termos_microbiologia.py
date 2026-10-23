"""
Rodada 4 do plano de expansão para 1000 termos do Dicionário Farmacêutico.
Categoria: microbiologia (19 -> 45 termos, +26).

Curadoria: cobre três eixos ainda sem verbete próprio na categoria — (1)
principais classes de antimicrobianos por mecanismo de ação (betalactâmicos
e suas subclasses, aminoglicosídeos, macrolídeos, quinolonas, glicopeptídeos,
tetraciclinas, sulfonamidas); (2) mecanismos moleculares de ação/resistência
(parede celular bacteriana, síntese proteica bacteriana, DNA girase,
beta-lactamase) e organismos multirresistentes de relevância clínica (MRSA,
ESBL, KPC, bactéria multirresistente); e (3) conceitos de farmacodinâmica
PK/PD e uso racional de antimicrobianos (tempo × concentração-dependente,
desescalonamento, stewardship), além de antiparasitários ainda não
cobertos (antihelmínticos, antiprotozoários) e conceitos gerais de
virulência/infecção oportunista.

Verificação de deduplicação (script Python, normalização de acentos/caixa
contra termo+sinonimos de todo o banco de 691 termos): nenhuma colisão
textual ou de id encontrada para os 26 candidatos.
"""
import json
import sys

NOVOS_TERMOS = [
    {
        "id": "betalactamicos",
        "termo": "Betalactâmicos",
        "categoria": "microbiologia",
        "sinonimos": ["Beta-Lactâmicos"],
        "definicao": "Classe de antimicrobianos que compartilham o anel beta-lactâmico em sua estrutura química e atuam inibindo a síntese da parede celular bacteriana, ao se ligarem às proteínas ligadoras de penicilina (PBPs) e bloquearem a formação de peptidoglicano — engloba penicilinas, cefalosporinas, carbapenêmicos e monobactâmicos.",
        "explicacaoSimplificada": "É a grande família de antibióticos que têm em comum um 'anel' químico específico (anel beta-lactâmico) e atuam destruindo a parede que protege a bactéria, impedindo que ela se mantenha íntegra e se multiplique — inclui penicilinas, cefalosporinas e carbapenêmicos.",
        "aplicacaoPratica": "São antimicrobianos bactericidas, tempo-dependentes (a eficácia depende do tempo em que a concentração do fármaco permanece acima da CIM, não do pico de concentração) — por isso, em infecções graves, a dosagem mais frequente ou a infusão prolongada é mais importante do que aumentar a dose isolada.",
        "atencao": "A alergia a um betalactâmico não implica automaticamente alergia a toda a classe — o risco de reação cruzada entre penicilinas e cefalosporinas é menor do que tradicionalmente se pensava, especialmente com cefalosporinas de gerações mais recentes, mas a avaliação individual de risco permanece importante antes de reexposição.",
        "termosRelacionados": ["penicilinas", "cefalosporinas", "carbapenemicos", "parede-celular-bacteriana", "beta-lactamase", "antimicrobiano-tempo-dependente"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica", "Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "penicilinas",
        "termo": "Penicilinas",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Subclasse de betalactâmicos, historicamente a primeira descoberta, que inclui a penicilina G (uso parenteral), a penicilina V (uso oral), as aminopenicilinas (amoxicilina, ampicilina, com espectro estendido a gram-negativos) e as penicilinas resistentes a penicilinases (oxacilina), cada subgrupo com espectro de ação diferente.",
        "explicacaoSimplificada": "São os antibióticos betalactâmicos mais antigos, descobertos a partir do fungo Penicillium — existem em diferentes variações, com espectros de ação que vão desde cobertura mais restrita até cobertura ampliada para bactérias gram-negativas, como a amoxicilina.",
        "aplicacaoPratica": "A amoxicilina, frequentemente associada ao ácido clavulânico (inibidor de beta-lactamase), é um dos antibióticos orais mais prescritos na prática ambulatorial para infecções respiratórias e de pele — a associação com clavulanato amplia o espectro para cepas produtoras de beta-lactamase.",
        "atencao": "A alergia à penicilina é uma das alergias a medicamentos mais relatadas pelos pacientes, mas estudos mostram que a maioria dos relatos não se confirma em testes formais de alergia — um rótulo de 'alérgico à penicilina' sem confirmação pode levar ao uso desnecessário de antibióticos de segunda linha, geralmente de espectro mais amplo e maior custo.",
        "termosRelacionados": ["betalactamicos", "beta-lactamase", "mecanismo-resistencia"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "cefalosporinas",
        "termo": "Cefalosporinas",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Subclasse de betalactâmicos organizada em gerações (1ª a 5ª), com progressiva ampliação de cobertura para gram-negativos e, nas gerações mais recentes, cobertura adicional para MRSA (5ª geração) — cada geração sucessiva geralmente perde um pouco de cobertura para gram-positivos em troca de maior cobertura para gram-negativos.",
        "explicacaoSimplificada": "São antibióticos betalactâmicos organizados em 'gerações', sendo que, de forma geral, conforme a geração avança, o antibiótico ganha mais cobertura contra bactérias gram-negativas, às vezes perdendo um pouco de força contra as gram-positivas.",
        "aplicacaoPratica": "A ceftriaxona (3ª geração) é amplamente usada em infecções graves hospitalares por sua ampla cobertura e posologia conveniente (dose única diária); a cefazolina (1ª geração) é a escolha clássica de profilaxia cirúrgica em muitos procedimentos.",
        "atencao": "Cefalosporinas de 1ª e 2ª geração não têm boa penetração no líquido cefalorraquidiano, sendo inadequadas para tratamento de meningite — já cefalosporinas de 3ª geração (como ceftriaxona e cefotaxima) atravessam melhor a barreira hematoencefálica e são opções de primeira linha nesse contexto.",
        "termosRelacionados": ["betalactamicos", "profilaxia-antimicrobiana", "espectro-acao"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "carbapenemicos",
        "termo": "Carbapenêmicos",
        "categoria": "microbiologia",
        "sinonimos": ["Carbapenêmicos"],
        "definicao": "Subclasse de betalactâmicos com o espectro de ação mais amplo entre os antimicrobianos convencionais, geralmente reservada para infecções graves ou causadas por bactérias multirresistentes produtoras de beta-lactamase de espectro estendido (ESBL), funcionando como uma das últimas linhas terapêuticas disponíveis.",
        "explicacaoSimplificada": "São os antibióticos betalactâmicos de espectro mais amplo, usados geralmente como 'últimos recursos' em infecções graves ou causadas por bactérias já resistentes a outros antibióticos mais comuns.",
        "aplicacaoPratica": "São frequentemente reservados para uso hospitalar em infecções graves por bactérias produtoras de ESBL ou em pacientes críticos com sepse de origem não esclarecida, como parte da terapia empírica inicial de amplo espectro, idealmente seguida de desescalonamento.",
        "atencao": "O surgimento de bactérias produtoras de carbapenemase (como a KPC) representa uma ameaça crítica à saúde pública, pois reduz drasticamente as opções terapêuticas restantes — o uso criterioso e reservado dos carbapenêmicos é uma estratégia essencial para preservar sua eficácia futura.",
        "termosRelacionados": ["betalactamicos", "kpc", "esbl", "bacteria-multirresistente", "stewardship-antimicrobiano"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica", "CDC — Antibiotic Resistance Threats Report"],
    },
    {
        "id": "aminoglicosideos",
        "termo": "Aminoglicosídeos",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Classe de antimicrobianos bactericidas (gentamicina, amicacina, tobramicina, entre outros) que atuam inibindo a síntese proteica bacteriana pela ligação irreversível à subunidade ribossomal 30S, com ação concentração-dependente e potencial de nefrotoxicidade e ototoxicidade que exige monitorização terapêutica.",
        "explicacaoSimplificada": "São antibióticos que bloqueiam a produção de proteínas da bactéria, agindo de forma mais eficaz quanto maior a concentração atingida — por isso costumam ser administrados em dose única diária alta, em vez de doses menores e mais frequentes, com monitorização cuidadosa pelo risco de afetar os rins e a audição.",
        "aplicacaoPratica": "A estratégia de dose única diária (em vez de doses fracionadas) aproveita tanto o padrão concentração-dependente da eficácia quanto o efeito pós-antibiótico prolongado dessa classe, além de reduzir a exposição renal acumulada — a monitorização de nível sérico (pico e vale) é recomendada especialmente em uso prolongado.",
        "atencao": "A nefrotoxicidade e a ototoxicidade dos aminoglicosídeos são dose e tempo-dependentes e podem ser irreversíveis (especialmente a ototoxicidade) — o uso concomitante com outros nefrotóxicos (como vancomicina ou contrastes iodados) exige vigilância redobrada da função renal.",
        "termosRelacionados": ["sintese-proteica-bacteriana", "efeito-pos-antibiotico", "nefrotoxicidade", "monitorizacao-terapeutica"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "macrolideos",
        "termo": "Macrolídeos",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Classe de antimicrobianos (azitromicina, claritromicina, eritromicina) que inibem a síntese proteica bacteriana pela ligação à subunidade ribossomal 50S, com boa cobertura para patógenos atípicos respiratórios (Mycoplasma, Chlamydia, Legionella) e ação predominantemente bacteriostática.",
        "explicacaoSimplificada": "São antibióticos usados principalmente em infecções respiratórias, com boa cobertura contra alguns micro-organismos 'atípicos' que não são bem cobertos por betalactâmicos comuns — bloqueiam a produção de proteínas da bactéria.",
        "aplicacaoPratica": "A azitromicina tem a vantagem farmacocinética de meia-vida longa e boa penetração tecidual, permitindo esquemas curtos (3 a 5 dias) com boa adesão; é amplamente usada em infecções respiratórias comunitárias e em algumas infecções sexualmente transmissíveis.",
        "atencao": "Macrolídeos são inibidores do CYP3A4 e podem causar interações clinicamente relevantes com estatinas, warfarina e outros substratos dessa enzima, além de prolongarem o intervalo QT — a claritromicina tem maior potencial de interação do que a azitromicina, que é um inibidor mais discreto do CYP3A4.",
        "termosRelacionados": ["sintese-proteica-bacteriana", "cyp3a4", "interacao-prolongamento-qt", "inibicao-enzimatica"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "quinolonas",
        "termo": "Quinolonas (Fluoroquinolonas)",
        "categoria": "microbiologia",
        "sinonimos": ["Fluoroquinolonas"],
        "definicao": "Classe de antimicrobianos bactericidas (ciprofloxacino, levofloxacino, moxifloxacino) que atuam inibindo enzimas essenciais à replicação do DNA bacteriano (DNA girase e topoisomerase IV), com ação concentração-dependente e boa biodisponibilidade oral.",
        "explicacaoSimplificada": "São antibióticos que impedem a bactéria de duplicar seu material genético, bloqueando enzimas essenciais a esse processo — têm boa absorção por via oral, o que facilita o tratamento ambulatorial de diversas infecções.",
        "aplicacaoPratica": "São amplamente usadas em infecções urinárias e respiratórias, mas o uso tem sido cada vez mais restringido em diretrizes recentes pelo perfil de efeitos adversos — devem ser separadas de cátions polivalentes (cálcio, ferro, magnésio, antiácidos) por sua forte tendência a quelação, que reduz drasticamente a absorção.",
        "atencao": "As fluoroquinolonas carregam alertas regulatórios para risco de tendinite/ruptura tendínea, neuropatia periférica e aneurisma/dissecção de aorta, especialmente em idosos e em uso concomitante com corticosteroides — por isso diversas diretrizes recomendam reservá-las para quando não há alternativa adequada.",
        "termosRelacionados": ["dna-girase", "quelacao", "interacao-antiacidos", "medicamento-alta-vigilancia"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica", "FDA Drug Safety Communications sobre Fluoroquinolonas"],
    },
    {
        "id": "glicopeptideos",
        "termo": "Glicopeptídeos",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Classe de antimicrobianos (vancomicina, teicoplanina) que atuam inibindo a síntese da parede celular bacteriana em um sítio distinto dos betalactâmicos, com espectro restrito a bactérias gram-positivas, incluindo cepas resistentes como MRSA, e ação tempo-dependente.",
        "explicacaoSimplificada": "São antibióticos usados principalmente contra bactérias gram-positivas resistentes, como o MRSA, atuando também na destruição da parede celular bacteriana, mas em um ponto diferente de onde agem os betalactâmicos.",
        "aplicacaoPratica": "A vancomicina exige monitorização terapêutica rigorosa (nível sérico) para equilibrar eficácia e risco de nefrotoxicidade, especialmente em uso prolongado ou associado a outros nefrotóxicos — a infusão deve ser lenta para evitar a 'síndrome do homem vermelho', uma reação relacionada à velocidade de infusão, não uma alergia verdadeira.",
        "atencao": "A síndrome do homem vermelho (rubor, prurido, hipotensão durante a infusão rápida de vancomicina) é frequentemente confundida com alergia verdadeira ao fármaco — na maioria dos casos, basta reduzir a velocidade de infusão para resolver, sem necessidade de suspender o tratamento.",
        "termosRelacionados": ["mrsa", "nefrotoxicidade", "monitorizacao-terapeutica", "parede-celular-bacteriana"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "tetraciclinas",
        "termo": "Tetraciclinas",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Classe de antimicrobianos bacteriostáticos (doxiciclina, tetraciclina) que inibem a síntese proteica bacteriana pela ligação à subunidade ribossomal 30S, com amplo espectro de ação, incluindo alguns patógenos atípicos, mas uso limitado em crianças pequenas e gestantes pelo risco de deposição óssea e dental.",
        "explicacaoSimplificada": "São antibióticos de amplo espectro que bloqueiam a produção de proteínas da bactéria — não são recomendados para crianças pequenas e gestantes, porque podem se depositar nos ossos e dentes em formação, causando manchas dentárias permanentes.",
        "aplicacaoPratica": "A doxiciclina é amplamente usada em infecções por patógenos atípicos, doença de Lyme, acne moderada a grave e algumas zoonoses — deve ser administrada separada de leite, antiácidos e suplementos de ferro/cálcio, que reduzem significativamente sua absorção por quelação.",
        "atencao": "Tetraciclinas estão contraindicadas em gestantes e em crianças menores de 8 anos pelo risco de deposição nos ossos em crescimento e de manchas permanentes no esmalte dentário — essa é uma das contraindicações pediátricas e obstétricas mais citadas em farmacologia clínica.",
        "termosRelacionados": ["sintese-proteica-bacteriana", "interacao-lacteos", "quelacao", "teratogenicidade"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "sulfonamidas",
        "termo": "Sulfonamidas",
        "categoria": "microbiologia",
        "sinonimos": ["Sulfas"],
        "definicao": "Classe de antimicrobianos (como o sulfametoxazol, geralmente associado ao trimetoprima na formulação combinada sulfametoxazol-trimetoprima) que atuam inibindo etapas sequenciais da síntese do ácido fólico bacteriano, produzindo um efeito sinérgico bactericida quando combinadas.",
        "explicacaoSimplificada": "São antibióticos que bloqueiam a produção de ácido fólico da bactéria — geralmente usados em combinação com o trimetoprima, que bloqueia uma etapa diferente da mesma via, somando forças para matar a bactéria com mais eficácia.",
        "aplicacaoPratica": "A combinação sulfametoxazol-trimetoprima é amplamente usada em infecções urinárias, profilaxia e tratamento de pneumonia por Pneumocystis jirovecii em imunossuprimidos, e em algumas infecções de pele por MRSA comunitário.",
        "atencao": "Sulfonamidas estão entre as causas mais comuns de reações de hipersensibilidade medicamentosa, incluindo quadros graves como a síndrome de Stevens-Johnson — pacientes com alergia conhecida a sulfas devem ser identificados claramente antes da dispensação de qualquer medicamento dessa classe, incluindo alguns diuréticos e hipoglicemiantes que compartilham o grupo sulfonamida.",
        "termosRelacionados": ["mrsa", "profilaxia-antimicrobiana", "medicamento-alta-vigilancia"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "beta-lactamase",
        "termo": "Beta-Lactamase",
        "categoria": "microbiologia",
        "sinonimos": ["Penicilinase"],
        "definicao": "Enzima produzida por determinadas bactérias que hidrolisa o anel beta-lactâmico, inativando antimicrobianos dessa classe — é o principal mecanismo de resistência a betalactâmicos, com variantes que vão desde penicilinases simples até enzimas de espectro estendido (ESBL) e carbapenemases (como a KPC).",
        "explicacaoSimplificada": "É uma enzima que algumas bactérias produzem para 'quebrar' o anel químico dos antibióticos betalactâmicos, inativando-os antes que eles consigam agir — é a principal forma de essas bactérias se tornarem resistentes a esses antibióticos.",
        "aplicacaoPratica": "Inibidores de beta-lactamase (ácido clavulânico, sulbactam, tazobactam) são associados a certos betalactâmicos justamente para neutralizar essa enzima e restaurar a eficácia do antibiótico contra cepas produtoras de beta-lactamase.",
        "atencao": "Nem todo inibidor de beta-lactamase neutraliza todos os tipos de beta-lactamase — enzimas de espectro estendido (ESBL) e carbapenemases (como a KPC) resistem à maioria dos inibidores clássicos, exigindo antimicrobianos de reserva ou combinações mais recentes.",
        "termosRelacionados": ["betalactamicos", "esbl", "kpc", "mecanismo-resistencia"],
        "fontes": ["Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "mrsa",
        "termo": "MRSA (Staphylococcus aureus Resistente à Meticilina)",
        "categoria": "microbiologia",
        "sinonimos": ["Staphylococcus aureus Resistente à Meticilina"],
        "definicao": "Cepa de Staphylococcus aureus que adquiriu resistência a todos os betalactâmicos (incluindo oxacilina/meticilina) por meio de uma alteração na proteína ligadora de penicilina (PBP2a, codificada pelo gene mecA), sendo uma das principais causas de infecção hospitalar e comunitária multirresistente.",
        "explicacaoSimplificada": "É uma variante da bactéria Staphylococcus aureus que se tornou resistente a praticamente todos os antibióticos betalactâmicos, incluindo a meticilina/oxacilina — é uma das bactérias resistentes mais importantes tanto em hospitais quanto na comunidade.",
        "aplicacaoPratica": "O tratamento de infecções por MRSA exige antimicrobianos alternativos aos betalactâmicos, como vancomicina, linezolida ou daptomicina, dependendo da gravidade e do sítio da infecção — medidas de controle de infecção (isolamento de contato) também são essenciais para prevenir disseminação hospitalar.",
        "atencao": "O MRSA de origem comunitária (diferente do hospitalar) frequentemente causa infecções de pele e partes moles em pessoas sem fatores de risco hospitalares tradicionais — a suspeita deve existir mesmo fora do ambiente hospitalar, especialmente em lesões de pele que não respondem a betalactâmicos comuns.",
        "termosRelacionados": ["glicopeptideos", "beta-lactamase", "bacteria-multirresistente", "gram-positivo"],
        "fontes": ["CDC — Antibiotic Resistance Threats Report", "Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "esbl",
        "termo": "ESBL (Beta-Lactamase de Espectro Estendido)",
        "categoria": "microbiologia",
        "sinonimos": ["Beta-Lactamase de Espectro Estendido"],
        "definicao": "Família de enzimas beta-lactamase produzidas principalmente por enterobactérias (Escherichia coli, Klebsiella pneumoniae), capazes de hidrolisar penicilinas, cefalosporinas de amplo espectro e monobactâmicos, mas tipicamente ainda suscetíveis a carbapenêmicos e inibidores de beta-lactamase.",
        "explicacaoSimplificada": "É um tipo de beta-lactamase mais potente, capaz de inativar praticamente todas as penicilinas e cefalosporinas comuns, produzida principalmente por certas bactérias intestinais — ainda costuma ser sensível a carbapenêmicos.",
        "aplicacaoPratica": "Infecções por bactérias produtoras de ESBL frequentemente exigem tratamento com carbapenêmicos, já que a maioria dos outros betalactâmicos (incluindo os combinados a inibidores de beta-lactamase clássicos) perde eficácia contra essas cepas.",
        "atencao": "A detecção de ESBL em cultura exige métodos laboratoriais específicos de confirmação, já que testes de sensibilidade de rotina podem subestimar a resistência — o laboratório de microbiologia deve sinalizar claramente essa condição no laudo, pois altera diretamente a escolha terapêutica.",
        "termosRelacionados": ["beta-lactamase", "carbapenemicos", "antibiograma", "bacteria-multirresistente"],
        "fontes": ["CDC — Antibiotic Resistance Threats Report"],
    },
    {
        "id": "kpc",
        "termo": "KPC (Klebsiella pneumoniae Carbapenemase)",
        "categoria": "microbiologia",
        "sinonimos": ["Klebsiella pneumoniae Carbapenemase"],
        "definicao": "Enzima carbapenemase, originalmente descrita em Klebsiella pneumoniae mas hoje disseminada em diversas enterobactérias, capaz de inativar inclusive os carbapenêmicos — representa um dos cenários mais graves de resistência antimicrobiana atual, com opções terapêuticas muito limitadas.",
        "explicacaoSimplificada": "É uma enzima que torna certas bactérias resistentes até mesmo aos carbapenêmicos, que são considerados antibióticos de reserva — bactérias produtoras de KPC são um dos maiores desafios atuais no tratamento de infecções hospitalares graves.",
        "aplicacaoPratica": "O tratamento de infecções por bactérias produtoras de KPC exige antimicrobianos de reserva mais recentes (como certas combinações de nova geração) ou polimixinas, frequentemente em combinação, com manejo idealmente conduzido por infectologista.",
        "atencao": "A disseminação de cepas produtoras de KPC em ambiente hospitalar é uma emergência de saúde pública — medidas rigorosas de controle de infecção (isolamento, vigilância ativa de colonização) são essenciais para conter surtos, já que as opções terapêuticas restantes são escassas e de maior toxicidade.",
        "termosRelacionados": ["carbapenemicos", "esbl", "bacteria-multirresistente"],
        "fontes": ["CDC — Antibiotic Resistance Threats Report", "ANVISA — Nota Técnica sobre Enterobactérias Produtoras de Carbapenemase"],
    },
    {
        "id": "bacteria-multirresistente",
        "termo": "Bactéria Multirresistente",
        "categoria": "microbiologia",
        "sinonimos": ["Multirresistência Bacteriana", "MDR (Multidrug-Resistant)"],
        "definicao": "Bactéria que apresenta resistência a múltiplas classes de antimicrobianos simultaneamente, reduzindo significativamente as opções terapêuticas disponíveis — conceito que engloba organismos como MRSA, enterobactérias produtoras de ESBL ou carbapenemase, e cepas pan-resistentes (resistentes a todas as classes testadas).",
        "explicacaoSimplificada": "É quando uma bactéria se torna resistente a várias classes diferentes de antibióticos ao mesmo tempo, reduzindo drasticamente as opções disponíveis para tratar a infecção — é um dos maiores desafios da medicina atual.",
        "aplicacaoPratica": "O manejo de infecções por bactérias multirresistentes exige coleta de cultura e antibiograma antes do início do tratamento definitivo sempre que possível, com terapia empírica inicial de amplo espectro seguida de desescalonamento conforme o resultado microbiológico.",
        "atencao": "O uso inadequado e excessivo de antimicrobianos (automedicação, prescrição sem indicação, doses/duração incorretas) é o principal fator impulsionador da seleção de bactérias multirresistentes — o farmacêutico tem papel central na educação do paciente e na dispensação responsável de antimicrobianos.",
        "termosRelacionados": ["mrsa", "esbl", "kpc", "stewardship-antimicrobiano", "resistencia-antimicrobiana"],
        "fontes": ["CDC — Antibiotic Resistance Threats Report", "Organização Mundial da Saúde — Global Action Plan on Antimicrobial Resistance"],
    },
    {
        "id": "parede-celular-bacteriana",
        "termo": "Parede Celular Bacteriana",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Estrutura rígida composta principalmente de peptidoglicano que envolve a membrana citoplasmática bacteriana, essencial para a manutenção da forma e integridade celular contra a pressão osmótica — é o alvo de ação dos betalactâmicos e glicopeptídeos, e sua composição é a base da diferenciação Gram-positiva/Gram-negativa.",
        "explicacaoSimplificada": "É a estrutura rígida que envolve e protege a bactéria, mantendo sua forma e evitando que ela se rompa pela pressão interna — é o principal alvo de antibióticos como os betalactâmicos, que impedem sua formação correta.",
        "aplicacaoPratica": "Antimicrobianos que atuam na parede celular (betalactâmicos, glicopeptídeos) são geralmente bactericidas e dependem de a bactéria estar em fase de crescimento/multiplicação ativa para serem eficazes — isso tem implicações para o uso combinado com antimicrobianos bacteriostáticos.",
        "atencao": "Bactérias gram-positivas e gram-negativas diferem significativamente na espessura e composição da parede celular (peptidoglicano muito mais espesso nas gram-positivas, membrana externa adicional nas gram-negativas) — essa diferença estrutural explica por que certos antimicrobianos são eficazes apenas contra um dos dois grupos.",
        "termosRelacionados": ["betalactamicos", "glicopeptideos", "gram-positivo", "gram-negativo"],
        "fontes": ["Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "sintese-proteica-bacteriana",
        "termo": "Síntese Proteica Bacteriana (Ribossomo Bacteriano)",
        "categoria": "microbiologia",
        "sinonimos": ["Ribossomo Bacteriano"],
        "definicao": "Processo de tradução que ocorre no ribossomo bacteriano (subunidades 30S e 50S, estruturalmente diferentes do ribossomo humano 40S/60S), alvo de ação de diversas classes de antimicrobianos (aminoglicosídeos, macrolídeos, tetraciclinas, cloranfenicol, linezolida), cada uma atuando em um sítio específico do ribossomo.",
        "explicacaoSimplificada": "É o processo pelo qual a bactéria produz suas proteínas, usando uma estrutura (o ribossomo bacteriano) diferente da estrutura equivalente das células humanas — essa diferença é o que permite que certos antibióticos ataquem a bactéria sem prejudicar as células do paciente.",
        "aplicacaoPratica": "A diferença estrutural entre o ribossomo bacteriano e o humano é a base da seletividade (e, portanto, da segurança relativa) dos antibióticos que atuam nessa via — entender em qual subunidade (30S ou 50S) cada classe atua ajuda a prever possíveis sinergismos ou antagonismos entre combinações de antimicrobianos.",
        "atencao": "Apesar da seletividade pela diferença estrutural do ribossomo, alguns antimicrobianos dessa via ainda têm toxicidade relevante por outros mecanismos (ex.: ototoxicidade/nefrotoxicidade dos aminoglicosídeos, supressão medular do cloranfenicol) — seletividade pelo alvo não significa ausência completa de efeitos adversos.",
        "termosRelacionados": ["aminoglicosideos", "macrolideos", "tetraciclinas"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "dna-girase",
        "termo": "DNA Girase e Topoisomerase IV",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Enzimas bacterianas essenciais ao superenovelamento e desenovelamento do DNA durante a replicação, alvo específico de ação das quinolonas/fluoroquinolonas — sua inibição impede a replicação do DNA bacteriano, levando à morte celular.",
        "explicacaoSimplificada": "São enzimas essenciais que ajudam a bactéria a 'organizar' seu DNA durante a duplicação — as fluoroquinolonas bloqueiam essas enzimas, impedindo a bactéria de se multiplicar.",
        "aplicacaoPratica": "Mutações nos genes que codificam essas enzimas são o principal mecanismo de resistência bacteriana às fluoroquinolonas, podendo surgir com relativa facilidade em populações bacterianas expostas a uso inadequado ou subdose desse antimicrobiano.",
        "atencao": "A resistência às fluoroquinolonas por mutação na DNA girase pode se desenvolver durante um único tratamento, especialmente se a dose ou duração forem inadequadas — isso reforça a importância da adesão completa ao esquema posológico prescrito.",
        "termosRelacionados": ["quinolonas", "mecanismo-resistencia", "resistencia-antimicrobiana"],
        "fontes": ["Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "farmacodinamica-pkpd-antimicrobiano",
        "termo": "Farmacodinâmica PK/PD de Antimicrobianos",
        "categoria": "microbiologia",
        "sinonimos": ["Índices PK/PD"],
        "definicao": "Conjunto de índices que relacionam parâmetros farmacocinéticos (concentração plasmática) com a atividade antimicrobiana, usados para otimizar o esquema posológico — os três índices principais são o tempo acima da CIM (T>CIM), a razão pico/CIM (Cmax/CIM) e a razão área sob a curva/CIM (AUC/CIM), cada um mais relevante para uma classe de antimicrobiano diferente.",
        "explicacaoSimplificada": "É o estudo de como a concentração do antibiótico no sangue se relaciona com sua eficácia contra a bactéria, usado para decidir a melhor forma de dosar cada classe de antimicrobiano — alguns funcionam melhor com doses frequentes, outros com doses altas e espaçadas.",
        "aplicacaoPratica": "Betalactâmicos (tempo-dependentes) se beneficiam de dosagem mais frequente ou infusão prolongada/contínua; aminoglicosídeos e fluoroquinolonas (concentração-dependentes) se beneficiam de doses mais altas e espaçadas — essa lógica orienta protocolos de otimização posológica em pacientes críticos.",
        "atencao": "Ignorar a classificação PK/PD de um antimicrobiano ao ajustar sua posologia é um erro comum: aumentar a dose de um betalactâmico sem aumentar a frequência/tempo de infusão tem impacto terapêutico muito menor do que otimizar o tempo acima da CIM, que é o que realmente determina sua eficácia.",
        "termosRelacionados": ["antimicrobiano-tempo-dependente", "cim", "monitorizacao-terapeutica"],
        "fontes": ["Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "antimicrobiano-tempo-dependente",
        "termo": "Antimicrobiano Tempo-Dependente × Concentração-Dependente",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Classificação farmacodinâmica dos antimicrobianos conforme o determinante principal de sua eficácia: tempo-dependentes (betalactâmicos, glicopeptídeos) têm eficácia ligada ao tempo em que a concentração plasmática permanece acima da CIM; concentração-dependentes (aminoglicosídeos, fluoroquinolonas) têm eficácia ligada ao pico de concentração atingido, independentemente da duração.",
        "explicacaoSimplificada": "É a classificação dos antibióticos conforme o que mais importa para sua eficácia: alguns funcionam melhor quando ficam por mais tempo no sangue acima de um nível mínimo (tempo-dependentes), enquanto outros funcionam melhor quando atingem um pico de concentração bem alto (concentração-dependentes).",
        "aplicacaoPratica": "Essa classificação orienta diretamente o esquema de administração: betalactâmicos tempo-dependentes se beneficiam de infusão estendida ou doses mais frequentes; aminoglicosídeos concentração-dependentes se beneficiam de dose única diária alta, em vez de doses menores fracionadas.",
        "atencao": "Não confundir essa classificação farmacodinâmica com a classificação de bactericida × bacteriostático — um antimicrobiano pode ser bactericida e, ainda assim, ter sua eficácia determinada principalmente pelo tempo de exposição (como os betalactâmicos), não pela concentração de pico.",
        "termosRelacionados": ["farmacodinamica-pkpd-antimicrobiano", "bactericida", "bacteriostatico", "aminoglicosideos"],
        "fontes": ["Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "desescalonamento-antimicrobiano",
        "termo": "Desescalonamento Antimicrobiano",
        "categoria": "microbiologia",
        "sinonimos": ["De-escalation"],
        "definicao": "Estratégia terapêutica que consiste em reduzir o espectro de um antimicrobiano iniciado empiricamente de amplo espectro, uma vez que o resultado de cultura e antibiograma identifique o agente causador específico e sua sensibilidade, buscando reduzir pressão seletiva de resistência sem comprometer a eficácia do tratamento.",
        "explicacaoSimplificada": "É a estratégia de começar o tratamento com um antibiótico de espectro amplo (para cobrir as possibilidades mais prováveis) e, depois que o exame de cultura identifica exatamente qual bactéria está causando a infecção, trocar para um antibiótico mais específico e de espectro mais estreito.",
        "aplicacaoPratica": "É um dos pilares dos programas de stewardship de antimicrobianos — reduz a pressão seletiva sobre a flora bacteriana do paciente e do ambiente hospitalar, além de frequentemente permitir o uso de antimicrobianos mais baratos e com menos efeitos adversos.",
        "atencao": "O desescalonamento não deve ser confundido com subtratamento — a troca para um espectro mais estreito só deve ocorrer quando há confirmação microbiológica clara do agente e de sua sensibilidade, nunca apenas pela melhora clínica isolada sem resultado de cultura disponível.",
        "termosRelacionados": ["stewardship-antimicrobiano", "antibiograma", "bacteria-multirresistente"],
        "fontes": ["Surviving Sepsis Campaign Guidelines", "Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "stewardship-antimicrobiano",
        "termo": "Stewardship de Antimicrobianos (Uso Racional de Antimicrobianos)",
        "categoria": "microbiologia",
        "sinonimos": ["Programa de Gerenciamento de Antimicrobianos", "Uso Racional de Antimicrobianos"],
        "definicao": "Conjunto coordenado de estratégias institucionais destinadas a otimizar a seleção, dose, via e duração da antibioticoterapia, com os objetivos de melhorar desfechos clínicos, reduzir eventos adversos, conter a disseminação de resistência antimicrobiana e reduzir custos desnecessários.",
        "explicacaoSimplificada": "É o conjunto de estratégias de uma instituição de saúde para garantir que os antibióticos sejam usados da forma mais adequada possível — no fármaco certo, na dose certa, pelo tempo certo —, ajudando a combater o problema crescente de resistência bacteriana.",
        "aplicacaoPratica": "O farmacêutico clínico frequentemente integra equipes de stewardship, revisando prescrições de antimicrobianos, sugerindo desescalonamento quando apropriado, monitorando duração de tratamento e participando da elaboração de protocolos institucionais de uso de antimicrobianos.",
        "atencao": "Programas de stewardship bem implementados reduzem consistentemente o consumo de antimicrobianos de amplo espectro sem piorar desfechos clínicos — a resistência a antimicrobianos é hoje considerada uma das maiores ameaças globais à saúde pública pela Organização Mundial da Saúde, e o uso racional é a principal estratégia de contenção disponível.",
        "termosRelacionados": ["desescalonamento-antimicrobiano", "bacteria-multirresistente", "resistencia-antimicrobiana", "profilaxia-antimicrobiana"],
        "fontes": ["Organização Mundial da Saúde — Global Action Plan on Antimicrobial Resistance", "ANVISA — Diretrizes para Programas de Gerenciamento de Antimicrobianos"],
    },
    {
        "id": "antihelminticos",
        "termo": "Antihelmínticos",
        "categoria": "microbiologia",
        "sinonimos": ["Vermífugos"],
        "definicao": "Classe de fármacos destinados ao tratamento de infecções por helmintos (vermes parasitas), como albendazol, mebendazol e ivermectina, atuando por diferentes mecanismos conforme o fármaco (interferência no metabolismo energético do parasita, paralisia neuromuscular, entre outros).",
        "explicacaoSimplificada": "São os medicamentos usados para tratar infecções por vermes (helmintos), como ascaridíase, enterobíase e outras parasitoses intestinais — popularmente também chamados de vermífugos.",
        "aplicacaoPratica": "O albendazol e o mebendazol são amplamente usados em programas de desparasitação em massa em áreas endêmicas, geralmente em dose única ou esquema curto, com boa tolerabilidade na maioria dos pacientes.",
        "atencao": "Alguns antihelmínticos (como o albendazol em doses mais altas usadas para infecções por tênias/cisticercose) têm contraindicações específicas na gestação e exigem acompanhamento mais cuidadoso — a orientação correta sobre a diferença entre uso de dose única para vermes comuns e esquemas mais complexos para infecções específicas é importante na dispensação.",
        "termosRelacionados": ["antiparasitario", "antiprotozoarios"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "antiprotozoarios",
        "termo": "Antiprotozoários",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Classe de fármacos destinados ao tratamento de infecções causadas por protozoários (organismos unicelulares eucarióticos), como metronidazol (giardíase, amebíase, tricomoníase), antimaláricos (malária) e outros agentes específicos para toxoplasmose e leishmaniose.",
        "explicacaoSimplificada": "São os medicamentos usados para tratar infecções causadas por protozoários — organismos de uma única célula, como os que causam malária, giardíase, amebíase e leishmaniose.",
        "aplicacaoPratica": "O metronidazol, um dos antiprotozoários mais usados na prática farmacêutica, também tem ação contra bactérias anaeróbias, e é a base do efeito dissulfiram-like com álcool — orientação sobre evitar álcool durante e por alguns dias após o tratamento é uma informação farmacêutica essencial.",
        "atencao": "O metronidazol tem efeito dissulfiram-like bem documentado com o consumo de álcool (náusea, rubor, taquicardia) — a orientação sobre essa interação deve ser feita rotineiramente na dispensação, já que o paciente pode não associar o mal-estar à combinação se não for alertado antes.",
        "termosRelacionados": ["efeito-dissulfiram-like", "antihelminticos", "esquistossomose", "malaria"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"],
    },
    {
        "id": "virulencia",
        "termo": "Virulência (Patogenicidade)",
        "categoria": "microbiologia",
        "sinonimos": ["Patogenicidade"],
        "definicao": "Grau ou intensidade da capacidade de um micro-organismo de causar doença em um hospedeiro, determinado por fatores como produção de toxinas, capacidade de adesão e invasão tecidual, evasão da resposta imune e formação de biofilme — distinto do conceito de patogenicidade, que se refere apenas à capacidade (presente ou ausente) de causar doença.",
        "explicacaoSimplificada": "É o quanto um micro-organismo é capaz de causar doença e o quão grave essa doença pode ser, dependendo de características próprias dele, como produção de toxinas e capacidade de invadir tecidos e escapar da defesa do corpo.",
        "aplicacaoPratica": "Compreender os fatores de virulência de um patógeno específico ajuda a prever a gravidade potencial de uma infecção e orienta decisões terapêuticas, como a necessidade de terapia combinada em infecções por organismos de alta virulência.",
        "atencao": "Virulência não é sinônimo de resistência antimicrobiana — um micro-organismo pode ser altamente virulento e totalmente sensível a antimicrobianos comuns, assim como pode ser multirresistente e pouco virulento; são características independentes do micro-organismo.",
        "termosRelacionados": ["biofilme", "infeccao-oportunista", "bacteria-multirresistente"],
        "fontes": ["Mandell — Principles and Practice of Infectious Diseases"],
    },
    {
        "id": "infeccao-oportunista",
        "termo": "Infecção Oportunista",
        "categoria": "microbiologia",
        "sinonimos": [],
        "definicao": "Infecção causada por micro-organismos que normalmente não causam doença em um hospedeiro imunocompetente, mas se tornam patogênicos quando há comprometimento da imunidade (por doença, imunossupressão medicamentosa, neutropenia, entre outros fatores), aproveitando a 'oportunidade' criada pela defesa imunológica reduzida.",
        "explicacaoSimplificada": "É uma infecção causada por micro-organismos que normalmente não adoeceriam uma pessoa com o sistema imunológico funcionando bem, mas que conseguem causar doença quando essa defesa está comprometida — por uma doença, por um medicamento imunossupressor, ou por outro motivo.",
        "aplicacaoPratica": "Pacientes em uso de imunossupressores, agentes biológicos ou quimioterapia devem ser rastreados e, em alguns casos, receber profilaxia específica (ex.: para Pneumocystis jirovecii, tuberculose latente) antes do início do tratamento imunossupressor, justamente pelo risco aumentado de infecções oportunistas.",
        "atencao": "A triagem de tuberculose latente e hepatites virais antes do início de agentes biológicos imunossupressores (anti-TNF e outros) é uma etapa obrigatória em diversas diretrizes — negligenciá-la pode permitir a reativação de uma infecção latente que se torna grave sob imunossupressão.",
        "termosRelacionados": ["virulencia", "tuberculose", "medicamento-alta-vigilancia"],
        "fontes": ["Mandell — Principles and Practice of Infectious Diseases"],
    },
]


def main():
    path = "dicionario.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    termos = data["termos"]
    ids_existentes = {t["id"] for t in termos}
    cat_ids_validas = {c["id"] for c in data["categorias"]}
    novos_ids = [t["id"] for t in NOVOS_TERMOS]
    if len(novos_ids) != len(set(novos_ids)):
        sys.exit("ERRO: ids duplicados dentro do próprio lote novo.")
    if len(NOVOS_TERMOS) != 26:
        sys.exit(f"ERRO: esperado exatamente 26 termos, encontrado {len(NOVOS_TERMOS)}.")
    for t in NOVOS_TERMOS:
        if t["id"] in ids_existentes:
            sys.exit(f"ERRO: id já existe no banco: {t['id']}")
        if t["categoria"] not in cat_ids_validas:
            sys.exit(f"ERRO: categoria inválida em {t['id']}: {t['categoria']}")
        if t["categoria"] != "microbiologia":
            sys.exit(f"ERRO: termo fora da categoria microbiologia: {t['id']}")
        if not t.get("atencao") and not t.get("naoConfunda"):
            sys.exit(f"ERRO: termo sem atencao/naoConfunda: {t['id']}")
        for campo in ["definicao", "explicacaoSimplificada", "aplicacaoPratica"]:
            if len(t.get(campo, "")) < 40:
                sys.exit(f"ERRO: campo {campo} suspeito de curto em {t['id']}")
    ids_apos = ids_existentes | set(novos_ids)
    invalid_refs = []
    for t in NOVOS_TERMOS:
        for rel in t.get("termosRelacionados", []):
            if rel not in ids_apos:
                invalid_refs.append((t["id"], rel))
    if invalid_refs:
        sys.exit(f"ERRO: termosRelacionados invalidos: {invalid_refs}")
    total_antes = len(termos)
    termos.extend(NOVOS_TERMOS)
    data["termos"] = termos
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK: {len(NOVOS_TERMOS)} termos adicionados a microbiologia.")
    print(f"Total de termos no banco: {total_antes} -> {len(data['termos'])}")


if __name__ == "__main__":
    main()
