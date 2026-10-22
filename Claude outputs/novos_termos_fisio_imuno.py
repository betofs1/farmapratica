#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona 10 novos termos de Fisiologia + 10 novos termos de Imunologia
ao dicionario.json do FarmaPrática. Roda diretamente no arquivo real do
usuário (mesma pasta), com validação completa antes de gravar.
"""
import json
import sys

NOVOS_TERMOS = [
    # ---------- FISIOLOGIA (10) ----------
    {
        "id": "pressao-arterial",
        "termo": "Pressão Arterial (PA)",
        "sigla": "PA",
        "categoria": "fisiologia",
        "sinonimos": ["Tensão arterial"],
        "definicao": "Força exercida pelo sangue contra a parede das artérias durante o ciclo cardíaco, expressa como a razão entre a pressão sistólica (fase de contração ventricular) e a diastólica (fase de relaxamento), em mmHg. Resulta do produto entre o débito cardíaco e a resistência vascular periférica (PA = DC × RVP) e é regulada por mecanismos neuro-humorais, incluindo o sistema nervoso autônomo e o Sistema Renina-Angiotensina-Aldosterona.",
        "explicacaoSimplificada": "É a 'força' com que o sangue empurra as paredes das artérias. Tem dois números: o maior (sistólica, quando o coração contrai) e o menor (diastólica, quando relaxa). Valores normais em adultos giram em torno de 120/80 mmHg.",
        "aplicacaoPratica": "Parâmetro central para orientação e monitorização farmacoterapêutica de anti-hipertensivos, diuréticos e vasodilatadores; a aferição correta (manguito no tamanho adequado, repouso prévio, posição sentada) é competência da farmácia clínica em serviços de aferição de PA.",
        "atencao": "Hipotensão postural (queda ≥20 mmHg na sistólica ou ≥10 mmHg na diastólica ao levantar) é efeito adverso comum de anti-hipertensivos, antipsicóticos e antidepressivos tricíclicos — risco de quedas, especialmente em idosos.",
        "termosRelacionados": ["debito-cardiaco", "fisiologia-sraa", "sistema-nervoso-autonomo"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica", "Diretriz Brasileira de Hipertensão Arterial — SBC"]
    },
    {
        "id": "debito-cardiaco",
        "termo": "Débito Cardíaco",
        "sigla": "DC",
        "categoria": "fisiologia",
        "sinonimos": ["Cardiac output"],
        "definicao": "Volume de sangue bombeado pelo coração por unidade de tempo, calculado como o produto entre o volume sistólico (quantidade ejetada a cada batimento) e a frequência cardíaca (DC = VS × FC), geralmente expresso em L/min.",
        "explicacaoSimplificada": "É quanto sangue o coração 'empurra' por minuto. Depende de quanto sangue sai a cada batida e de quantas vezes o coração bate por minuto.",
        "aplicacaoPratica": "Fármacos inotrópicos (digoxina), cronotrópicos (betabloqueadores, que reduzem a FC e, consequentemente, o DC) e vasodilatadores atuam sobre componentes do débito cardíaco; relevante para entender o mecanismo de ação de medicamentos usados na insuficiência cardíaca.",
        "atencao": "Betabloqueadores reduzem o débito cardíaco ao diminuir a frequência cardíaca — por isso exigem titulação cuidadosa e têm contraindicação relativa em bradicardia significativa ou choque cardiogênico descompensado.",
        "termosRelacionados": ["pressao-arterial", "betabloqueadores", "insuficiencia-cardiaca"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    {
        "id": "equilibrio-acido-base",
        "termo": "Equilíbrio Ácido-Base",
        "categoria": "fisiologia",
        "sinonimos": ["Equilíbrio ácido-básico"],
        "definicao": "Conjunto de mecanismos fisiológicos (tamponamento sanguíneo, compensação respiratória pela ventilação pulmonar e compensação renal pela excreção/reabsorção de bicarbonato e íons hidrogênio) que mantêm o pH sanguíneo dentro da faixa estreita de 7,35–7,45, essencial para a função enzimática e celular normal.",
        "explicacaoSimplificada": "É o controle do quanto o sangue está 'ácido' ou 'básico'. O corpo mantém o pH do sangue quase sempre entre 7,35 e 7,45 usando os pulmões e os rins.",
        "aplicacaoPratica": "Distúrbios ácido-base (acidose/alcalose respiratória ou metabólica) alteram a ionização de fármacos ácidos e básicos fracos, influenciando sua distribuição e eliminação renal — base da alcalinização urinária usada no manejo de algumas intoxicações (ex.: salicilatos, fenobarbital).",
        "atencao": "A alcalinização da urina com bicarbonato de sódio aumenta a excreção renal de ácidos fracos (como o AAS) por aumentar sua fração ionizada — princípio usado no tratamento de intoxicação salicílica.",
        "termosRelacionados": ["descontaminacao-gastrointestinal", "reabsorcao-tubular"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica", "Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "termorregulacao",
        "termo": "Termorregulação",
        "categoria": "fisiologia",
        "sinonimos": [],
        "definicao": "Conjunto de mecanismos fisiológicos (vasodilatação/vasoconstrição cutânea, sudorese, tremor muscular) coordenados pelo hipotálamo para manter a temperatura corporal central em torno de 36,5–37,2 °C, independentemente de variações do ambiente externo.",
        "explicacaoSimplificada": "É o 'termostato' do corpo, comandado pelo hipotálamo, que mantém a temperatura corporal estável suando quando está quente ou tremendo quando está frio.",
        "aplicacaoPratica": "Antipiréticos (dipirona, paracetamol, AINEs) atuam reduzindo o ponto de ajuste hipotalâmico elevado pela febre; alguns fármacos (antipsicóticos, anticolinérgicos) podem comprometer a termorregulação e predispor à hipertermia.",
        "atencao": "Antipsicóticos e anticolinérgicos prejudicam a sudorese e a termorregulação, aumentando o risco de hipertermia em dias quentes ou durante exercício físico — atenção redobrada em idosos e pacientes institucionalizados.",
        "termosRelacionados": ["sistema-nervoso-autonomo"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    {
        "id": "hemostasia",
        "termo": "Hemostasia",
        "categoria": "fisiologia",
        "sinonimos": ["Hemostasia primária e secundária"],
        "definicao": "Conjunto de processos fisiológicos que previnem e interrompem o sangramento após lesão vascular, envolvendo vasoconstrição local, agregação plaquetária (hemostasia primária) e a cascata de coagulação com formação de fibrina (hemostasia secundária), contrabalançado pelo sistema fibrinolítico.",
        "explicacaoSimplificada": "É o processo que o corpo usa para estancar um sangramento: o vaso se contrai, as plaquetas se juntam para tampar o local e depois se forma uma rede de fibrina para firmar o coágulo.",
        "aplicacaoPratica": "Base farmacológica de antiagregantes plaquetários (AAS, clopidogrel), anticoagulantes (varfarina, heparina, DOACs) e antifibrinolíticos (ácido tranexâmico); fundamental para orientar sobre suspensão perioperatória desses fármacos.",
        "atencao": "A combinação de antiagregantes e anticoagulantes (ex.: AAS + varfarina) aumenta significativamente o risco hemorrágico e deve ser monitorada rigorosamente, geralmente reservada a indicações específicas com benefício comprovado.",
        "termosRelacionados": ["indice-terapeutico"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica", "Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "eixo-hipotalamo-hipofise-adrenal",
        "termo": "Eixo Hipotálamo-Hipófise-Adrenal",
        "sigla": "Eixo HHA",
        "categoria": "fisiologia",
        "sinonimos": ["Eixo hipotálamo-hipófise-suprarrenal", "HPA axis"],
        "definicao": "Sistema neuroendócrino regulador da resposta ao estresse e do ritmo circadiano do cortisol, no qual o hipotálamo libera CRH, estimulando a hipófise a secretar ACTH, que por sua vez estimula o córtex da adrenal a produzir cortisol; o próprio cortisol exerce retroalimentação negativa sobre o hipotálamo e a hipófise.",
        "explicacaoSimplificada": "É a 'cadeia de comando' hormonal que liga o cérebro às glândulas adrenais para produzir cortisol, o principal hormônio do estresse e também regulador de várias funções do corpo ao longo do dia.",
        "aplicacaoPratica": "O uso prolongado de corticosteroides sistêmicos (ou mesmo tópicos/inalatórios em altas doses) suprime o eixo HHA por retroalimentação negativa, exigindo desmame gradual em vez de suspensão abrupta para evitar insuficiência adrenal aguda.",
        "atencao": "Suspender corticosteroide sistêmico usado por mais de 2–3 semanas de forma abrupta pode causar insuficiência adrenal aguda (hipotensão, fraqueza, hipoglicemia) — a orientação farmacêutica deve sempre reforçar o desmame gradual prescrito.",
        "termosRelacionados": ["feedback-negativo", "ritmo-circadiano"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica", "Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "motilidade-gastrointestinal",
        "termo": "Motilidade Gastrointestinal",
        "categoria": "fisiologia",
        "sinonimos": ["Peristaltismo", "Trânsito intestinal"],
        "definicao": "Conjunto de contrações musculares coordenadas (peristaltismo) ao longo do trato gastrointestinal que impulsionam o conteúdo luminal, regulado pelo sistema nervoso entérico, por hormônios gastrointestinais e pelo sistema nervoso autônomo.",
        "explicacaoSimplificada": "É o movimento do intestino que empurra o alimento e os medicamentos ao longo do tubo digestivo, desde o estômago até a eliminação.",
        "aplicacaoPratica": "Fármacos anticolinérgicos, opioides e alguns antidepressivos reduzem a motilidade (predispondo a constipação), enquanto procinéticos (domperidona, metoclopramida) a aumentam; a motilidade também influencia o tempo de contato do fármaco com a mucosa absortiva, afetando a biodisponibilidade oral.",
        "atencao": "O uso crônico de opioides reduz a motilidade intestinal de forma previsível e persistente (constipação induzida por opioides), diferente da tolerância que se desenvolve a outros efeitos adversos — geralmente requer profilaxia com laxante desde o início do tratamento.",
        "termosRelacionados": ["esvaziamento-gastrico", "absorcao"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    {
        "id": "esvaziamento-gastrico",
        "termo": "Esvaziamento Gástrico",
        "categoria": "fisiologia",
        "sinonimos": [],
        "definicao": "Velocidade com que o conteúdo do estômago é transferido para o duodeno, processo regulado por fatores neuro-hormonais e pela composição do alimento (refeições ricas em gordura retardam o esvaziamento), que determina o tempo disponível antes de a dissolução de formas farmacêuticas sólidas preceder a absorção intestinal.",
        "explicacaoSimplificada": "É a velocidade com que o estômago 'esvazia' seu conteúdo para o intestino — quanto mais rápido isso acontece, mais rápido um medicamento tomado por via oral chega ao local onde é absorvido.",
        "aplicacaoPratica": "Alimentos, alguns fármacos (opioides e anticolinérgicos retardam; procinéticos aceleram) e condições clínicas (gastroparesia diabética) alteram o esvaziamento gástrico, impactando o tempo para início de ação de medicamentos orais, especialmente formulações de liberação imediata.",
        "atencao": "Gastroparesia (comum em diabetes de longa data) retarda o esvaziamento gástrico e pode atrasar significativamente a absorção e o início de ação de medicamentos orais, incluindo analgésicos usados para alívio rápido de sintomas.",
        "termosRelacionados": ["motilidade-gastrointestinal", "absorcao", "biodisponibilidade"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica", "Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "ritmo-circadiano",
        "termo": "Ritmo Circadiano",
        "categoria": "fisiologia",
        "sinonimos": [],
        "definicao": "Ciclo biológico de aproximadamente 24 horas, regulado pelo núcleo supraquiasmático do hipotálamo em resposta principalmente à luz, que modula variações periódicas em funções como o sono, a secreção hormonal (cortisol, melatonina), a temperatura corporal e, consequentemente, a farmacocinética e a farmacodinâmica de diversos fármacos ao longo do dia.",
        "explicacaoSimplificada": "É o 'relógio biológico' interno de cerca de 24 horas que regula o sono, a liberação de hormônios e outras funções do corpo conforme a hora do dia.",
        "aplicacaoPratica": "Base da cronofarmacologia: estatinas de meia-vida curta são preferencialmente administradas à noite (pico de síntese hepática de colesterol é noturno) e corticosteroides sistêmicos são administrados pela manhã para mimetizar o pico fisiológico de cortisol e minimizar a supressão do eixo HHA.",
        "atencao": "Administrar corticosteroide sistêmico de uso crônico à noite, em vez de pela manhã, aumenta o risco de supressão do eixo hipotálamo-hipófise-adrenal por não respeitar o ritmo circadiano natural do cortisol.",
        "termosRelacionados": ["eixo-hipotalamo-hipofise-adrenal"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    {
        "id": "microbiota-intestinal",
        "termo": "Microbiota Intestinal",
        "categoria": "fisiologia",
        "sinonimos": ["Flora intestinal"],
        "definicao": "Conjunto de microrganismos (predominantemente bactérias) que colonizam o trato gastrointestinal, desempenhando funções fisiológicas como síntese de vitaminas (K e algumas do complexo B), metabolismo de componentes da dieta e de fármacos, e modulação do sistema imunológico.",
        "explicacaoSimplificada": "São os trilhões de bactérias 'boas' que vivem no intestino e ajudam na digestão, na produção de algumas vitaminas e no fortalecimento das defesas do corpo.",
        "aplicacaoPratica": "Antibióticos de amplo espectro podem desequilibrar a microbiota intestinal, favorecendo diarreia associada a antibióticos e, em casos graves, infecção por Clostridioides difficile; probióticos são frequentemente orientados pelo farmacêutico para mitigar esse efeito.",
        "atencao": "O uso de probióticos deve ser orientado para administração distante (geralmente 2 horas) da dose de antibiótico, para reduzir a chance de os microrganismos vivos serem eliminados pelo próprio antimicrobiano.",
        "termosRelacionados": [],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    # ---------- IMUNOLOGIA (10) ----------
    {
        "id": "linfocito",
        "termo": "Linfócito",
        "categoria": "imunologia",
        "sinonimos": ["Linfócitos T e B"],
        "definicao": "Tipo de leucócito (glóbulo branco) responsável pela imunidade adaptativa, subdividido principalmente em linfócitos T (atuam na imunidade celular e auxiliam a resposta imune) e linfócitos B (diferenciam-se em plasmócitos produtores de anticorpos, compondo a imunidade humoral).",
        "explicacaoSimplificada": "São as células de defesa responsáveis pela 'memória' do sistema imunológico — os linfócitos T atacam diretamente ou coordenam a resposta, e os linfócitos B produzem anticorpos.",
        "aplicacaoPratica": "A contagem de linfócitos T CD4+ é parâmetro central no acompanhamento de pacientes com HIV; imunossupressores (usados em transplantes e doenças autoimunes) atuam reduzindo a proliferação ou a ativação de linfócitos.",
        "atencao": "Corticosteroides sistêmicos em doses imunossupressoras reduzem a contagem e a função de linfócitos, aumentando o risco de infecções oportunistas durante o tratamento prolongado.",
        "termosRelacionados": ["resposta-imune", "anticorpo", "mhc"],
        "fontes": ["Abbas — Imunologia Celular e Molecular", "Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    {
        "id": "citocina",
        "termo": "Citocina",
        "categoria": "imunologia",
        "sinonimos": ["Citocinas pró-inflamatórias"],
        "definicao": "Proteína de sinalização celular secretada principalmente por células do sistema imunológico (mas também por outros tecidos), que regula a intensidade e a duração da resposta imune e inflamatória; inclui interleucinas, interferons, fatores de necrose tumoral (TNF) e quimiocinas.",
        "explicacaoSimplificada": "São 'mensageiros químicos' que as células de defesa usam para se comunicar e coordenar a resposta contra uma infecção ou lesão — alguns aumentam a inflamação, outros a controlam.",
        "aplicacaoPratica": "Base farmacológica dos imunobiológicos usados em doenças autoimunes (inibidores de TNF-alfa como adalimumabe e infliximabe, inibidores de interleucinas como tocilizumabe) e da 'tempestade de citocinas', complicação grave descrita em infecções graves e em terapias com células CAR-T.",
        "atencao": "Inibidores de TNF-alfa aumentam o risco de reativação de tuberculose latente — a triagem (PPD/IGRA e radiografia de tórax) é obrigatória antes de iniciar esses imunobiológicos.",
        "termosRelacionados": ["resposta-imune", "interferon", "tuberculose"],
        "fontes": ["Abbas — Imunologia Celular e Molecular"]
    },
    {
        "id": "sistema-complemento",
        "termo": "Sistema Complemento",
        "categoria": "imunologia",
        "sinonimos": ["Complemento (imunologia)"],
        "definicao": "Conjunto de mais de 30 proteínas plasmáticas que atuam em cascata, ativadas por três vias (clássica, alternativa e das lectinas), promovendo opsonização de patógenos, recrutamento de células inflamatórias (anafilatoxinas) e formação do complexo de ataque à membrana, que lisa diretamente microrganismos.",
        "explicacaoSimplificada": "É um grupo de proteínas do sangue que trabalham em cadeia para 'marcar' micróbios para serem destruídos, atrair células de defesa e até romper a membrana de alguns microrganismos diretamente.",
        "aplicacaoPratica": "Deficiências do sistema complemento aumentam a suscetibilidade a infecções por bactérias encapsuladas; fármacos como o eculizumabe, que inibe a fração C5 do complemento, exigem vacinação prévia contra meningococo pelo risco aumentado dessas infecções.",
        "atencao": "Pacientes em uso de inibidores do complemento (ex.: eculizumabe) têm risco muito aumentado de infecção meningocócica e devem estar com a vacinação específica atualizada antes de iniciar o tratamento.",
        "termosRelacionados": ["resposta-imune", "vacina"],
        "fontes": ["Abbas — Imunologia Celular e Molecular"]
    },
    {
        "id": "fagocitose",
        "termo": "Fagocitose",
        "categoria": "imunologia",
        "sinonimos": [],
        "definicao": "Processo pelo qual células especializadas do sistema imunológico inato (principalmente neutrófilos e macrófagos) englobam e digerem partículas estranhas, como microrganismos e debris celulares, por meio da formação de uma vesícula (fagossomo) que se funde a lisossomos.",
        "explicacaoSimplificada": "É quando células de defesa 'engolem' e destroem bactérias, vírus ou restos de células mortas, como uma espécie de limpeza do organismo.",
        "aplicacaoPratica": "Primeira linha de defesa contra microrganismos antes da ativação da resposta imune adaptativa; neutropenia (redução de neutrófilos), comum em quimioterapia, compromete diretamente a fagocitose e aumenta drasticamente o risco de infecções graves.",
        "atencao": "Pacientes neutropênicos (ex.: pós-quimioterapia) têm a fagocitose comprometida e podem não apresentar os sinais clássicos de infecção (como pus ou febre alta) mesmo diante de infecções graves — qualquer febre nesse contexto é emergência médica (neutropenia febril).",
        "termosRelacionados": ["resposta-imune"],
        "fontes": ["Abbas — Imunologia Celular e Molecular"]
    },
    {
        "id": "mhc",
        "termo": "Complexo Principal de Histocompatibilidade (MHC)",
        "sigla": "MHC",
        "categoria": "imunologia",
        "sinonimos": ["HLA (em humanos)", "Antígeno leucocitário humano"],
        "definicao": "Conjunto de proteínas de membrana, codificadas por genes altamente polimórficos, que apresentam fragmentos de antígenos aos linfócitos T — o MHC de classe I apresenta antígenos intracelulares (reconhecidos por linfócitos T CD8+) e o MHC de classe II apresenta antígenos extracelulares processados por células apresentadoras de antígenos (reconhecidos por linfócitos T CD4+).",
        "explicacaoSimplificada": "São 'etiquetas' na superfície das células que mostram pedaços de proteínas para o sistema de defesa reconhecer o que é próprio do corpo e o que é estranho (como um vírus).",
        "aplicacaoPratica": "A compatibilidade de HLA entre doador e receptor é determinante para o sucesso de transplantes de órgãos e de medula óssea, orientando a escolha e a intensidade do esquema imunossupressor pós-transplante.",
        "atencao": "Quanto maior a incompatibilidade de HLA entre doador e receptor, maior o risco de rejeição do enxerto, exigindo esquemas imunossupressores mais intensos e maior vigilância a infecções oportunistas.",
        "termosRelacionados": ["linfocito", "antigeno"],
        "fontes": ["Abbas — Imunologia Celular e Molecular"]
    },
    {
        "id": "interferon",
        "termo": "Interferon",
        "sigla": "IFN",
        "categoria": "imunologia",
        "sinonimos": ["Interferons alfa, beta e gama"],
        "definicao": "Grupo de citocinas produzidas em resposta a infecções virais (entre outros estímulos), que induzem um estado antiviral nas células vizinhas, ativam células natural killer e macrófagos, e modulam a resposta imune adaptativa; também disponível como medicamento biológico (ex.: interferon peguilado) em algumas indicações terapêuticas.",
        "explicacaoSimplificada": "É uma proteína de defesa que as células liberam quando são infectadas por um vírus, avisando as células vizinhas para 'se protegerem' e ativando outras células de defesa.",
        "aplicacaoPratica": "Interferons peguilados foram historicamente usados no tratamento da hepatite C crônica (hoje amplamente substituídos por antivirais de ação direta) e ainda têm indicação em hepatite B crônica selecionada e em algumas doenças oncológicas e autoimunes (ex.: esclerose múltipla).",
        "atencao": "O tratamento com interferon frequentemente causa síndrome gripal (febre, mialgia, calafrios) após a aplicação e pode induzir ou agravar depressão — a avaliação do histórico psiquiátrico é recomendada antes do início da terapia.",
        "termosRelacionados": ["citocina", "resposta-imune"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "doenca-autoimune",
        "termo": "Doença Autoimune",
        "categoria": "imunologia",
        "sinonimos": ["Autoimunidade"],
        "definicao": "Condição patológica na qual o sistema imunológico perde a tolerância a antígenos próprios e passa a atacar células, tecidos ou órgãos do próprio organismo, gerando inflamação crônica e dano tecidual; exemplos incluem artrite reumatoide, lúpus eritematoso sistêmico, tireoidite de Hashimoto e diabetes mellitus tipo 1.",
        "explicacaoSimplificada": "É quando o sistema de defesa do corpo 'erra o alvo' e passa a atacar os próprios tecidos saudáveis, em vez de atacar só invasores externos.",
        "aplicacaoPratica": "Base do uso de imunossupressores, corticosteroides e imunobiológicos (anti-TNF, anti-interleucinas) no tratamento de doenças autoimunes; o farmacêutico deve estar atento à maior suscetibilidade a infecções desses pacientes e às interações entre os diversos imunossupressores frequentemente associados.",
        "atencao": "Pacientes com doença autoimune em uso de múltiplos imunossupressores têm risco cumulativo de infecções oportunistas — a vacinação com vacinas vivas é geralmente contraindicada durante a imunossupressão significativa.",
        "termosRelacionados": ["resposta-imune", "hipersensibilidade"],
        "fontes": ["Abbas — Imunologia Celular e Molecular"]
    },
    {
        "id": "orgaos-linfoides",
        "termo": "Órgãos Linfoides (Primários e Secundários)",
        "categoria": "imunologia",
        "sinonimos": ["Tecido linfoide"],
        "definicao": "Estruturas anatômicas responsáveis pela produção e maturação (órgãos linfoides primários: medula óssea e timo) ou pela ativação e resposta imune a antígenos (órgãos linfoides secundários: linfonodos, baço e tecido linfoide associado a mucosas) de linfócitos.",
        "explicacaoSimplificada": "São os 'órgãos do sistema de defesa': uns fabricam e treinam as células de defesa (medula óssea e timo) e outros são onde essas células encontram os invasores e organizam o ataque (linfonodos, baço, mucosas).",
        "aplicacaoPratica": "O baço é sítio relevante de eliminação de hemácias e de resposta a bactérias encapsuladas — pacientes esplenectomizados (sem baço) têm indicação de vacinação específica (pneumocócica, meningocócica, Haemophilus influenzae tipo b) pelo risco aumentado de sepse fulminante.",
        "atencao": "Pacientes esplenectomizados têm risco elevado de sepse fulminante por bactérias encapsuladas e devem manter o calendário vacinal específico em dia, muitas vezes com reforços periódicos — orientação importante na dispensação para esse público.",
        "termosRelacionados": ["vacina", "fagocitose"],
        "fontes": ["Abbas — Imunologia Celular e Molecular", "Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    {
        "id": "adjuvante-imunologico",
        "termo": "Adjuvante Imunológico",
        "categoria": "imunologia",
        "sinonimos": ["Adjuvante vacinal"],
        "definicao": "Substância incorporada a uma vacina para potencializar e prolongar a resposta imune ao antígeno vacinal, permitindo doses menores de antígeno ou menor número de doses; exemplos incluem sais de alumínio (os mais usados historicamente), emulsões oleosas e, mais recentemente, adjuvantes à base de partículas lipídicas.",
        "explicacaoSimplificada": "É um ingrediente adicionado a algumas vacinas para 'turbinar' a resposta do sistema imunológico ao antígeno, deixando a proteção mais forte e duradoura.",
        "aplicacaoPratica": "Vacinas inativadas e de subunidades costumam depender de adjuvantes para induzir resposta imune adequada (diferente de vacinas vivas atenuadas, que geralmente não precisam); reações no local da aplicação (dor, eritema, nódulo) são frequentemente atribuíveis ao adjuvante, não ao antígeno em si.",
        "atencao": "Reações locais mais intensas (dor, endurecimento, nódulo persistente) são mais associadas a vacinas adjuvantadas do que a vacinas sem adjuvante — informação útil para orientar o usuário sobre o que esperar após a aplicação.",
        "termosRelacionados": ["vacina", "antigeno"],
        "fontes": ["Abbas — Imunologia Celular e Molecular"]
    },
    {
        "id": "anticorpo-monoclonal",
        "termo": "Anticorpo Monoclonal",
        "sigla": "mAb",
        "categoria": "imunologia",
        "sinonimos": ["Anticorpos monoclonais", "Terapia biológica com anticorpos"],
        "definicao": "Anticorpo produzido em laboratório a partir de um único clone de linfócito B, com especificidade idêntica para um único epítopo-alvo; amplamente utilizado como classe terapêutica (imunobiológicos) em oncologia, doenças autoimunes, doenças infecciosas e outras áreas, identificado pelo sufixo '-mabe' na nomenclatura farmacêutica.",
        "explicacaoSimplificada": "É um anticorpo feito em laboratório, todos idênticos entre si, desenhado para atacar um alvo bem específico no corpo — usado hoje como tratamento em diversas doenças, não só como ferramenta de diagnóstico.",
        "aplicacaoPratica": "O sufixo '-mabe' no nome do fármaco (ex.: adalimumabe, trastuzumabe, rituximabe) identifica a classe; a maioria requer administração parenteral (sem via oral, pois seriam degradados no trato digestivo), armazenamento sob refrigeração e cuidados especiais de rede de frio na dispensação.",
        "atencao": "Anticorpos monoclonais exigem conservação em cadeia de frio rigorosa (geralmente 2–8°C) — o transporte e a dispensação inadequados podem inativar o medicamento sem alteração visível no produto.",
        "termosRelacionados": ["cadeia-fria", "resposta-imune", "anticorpo"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
]


def main():
    path = "dicionario.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    termos = data["termos"]
    ids_existentes = {t["id"] for t in termos}
    cat_ids_validas = {c["id"] for c in data["categorias"]}
    comp_ids = {c["id"] for c in data.get("comparacoes", [])}

    novos_ids = [t["id"] for t in NOVOS_TERMOS]
    if len(novos_ids) != len(set(novos_ids)):
        sys.exit("ERRO: ids duplicados dentro do próprio lote novo.")

    for t in NOVOS_TERMOS:
        if t["id"] in ids_existentes:
            sys.exit(f"ERRO: id já existe no banco: {t['id']}")
        if t["categoria"] not in cat_ids_validas:
            sys.exit(f"ERRO: categoria inválida em {t['id']}: {t['categoria']}")
        if not t.get("atencao") and not t.get("naoConfunda"):
            sys.exit(f"ERRO: termo sem atencao/naoConfunda: {t['id']}")
        for campo in ["definicao", "explicacaoSimplificada", "aplicacaoPratica"]:
            if len(t.get(campo, "")) < 40:
                sys.exit(f"ERRO: campo {campo} suspeito de curto em {t['id']}")

    ids_apos = ids_existentes | set(novos_ids)
    for t in NOVOS_TERMOS:
        for rel in t.get("termosRelacionados", []):
            if rel not in ids_apos:
                sys.exit(f"ERRO: termosRelacionados inválido em {t['id']}: {rel}")

    n_fisio = sum(1 for t in NOVOS_TERMOS if t["categoria"] == "fisiologia")
    n_imuno = sum(1 for t in NOVOS_TERMOS if t["categoria"] == "imunologia")
    if n_fisio != 10 or n_imuno != 10:
        sys.exit(f"ERRO: contagem inesperada (fisiologia={n_fisio}, imunologia={n_imuno})")

    total_antes = len(termos)
    termos.extend(NOVOS_TERMOS)
    data["termos"] = termos

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print(f"OK: {len(NOVOS_TERMOS)} termos adicionados ({n_fisio} fisiologia, {n_imuno} imunologia).")
    print(f"Total de termos no banco: {total_antes} -> {len(data['termos'])}")


if __name__ == "__main__":
    main()
