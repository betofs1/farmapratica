# -*- coding: utf-8 -*-
import json, re, sys

DATA_PATH = "../data.js"

NOVOS = {}

NOVOS["resmetirom"] = {
  "nomeGenerico": "Resmetirom",
  "classeTerapeutica": "Hepatoprotetores e Lipotrópicos (Classe A5B)",
  "classes": [{"codigo":"A5B","nome":"Hepatoprotetores e Lipotrópicos"}],
  "nomesComerciais": {"referencia":"Rezdiffra® (EUA, Madrigal Pharmaceuticals; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Agonista seletivo do receptor beta do hormônio tireoidiano (THR-beta) no fígado, reduzindo esteatose, inflamação e fibrose hepática na esteato-hepatite associada à disfunção metabólica (MASH), sem os efeitos sistêmicos tireotóxicos do THR-alfa.",
  "farmacocinetica": "Absorção oral com alimento; ligação extensa a proteínas plasmáticas; metabolismo hepático (sulfatação, vias CYP); meia-vida longa, permitindo dose única diária; excreção predominantemente fecal.",
  "indicacoes": ["MASH (esteato-hepatite associada à disfunção metabólica) com fibrose hepática F2 ou F3, associado a dieta e atividade física"],
  "contraindicacoes": ["Hipersensibilidade ao resmetirom ou excipientes", "Cirrose hepática descompensada (Child-Pugh B/C)", "Hipertensão porta clinicamente significativa"],
  "precaucoes": ["Monitorar enzimas hepáticas (risco de hepatotoxicidade medicamentosa)", "Ajustar/suspender estatinas concomitantes pelo risco de miopatia por aumento de exposição (inibição de OATP1B1/1B3)", "Uso não estabelecido em cirrose compensada avançada nem em MASH sem fibrose"],
  "posologia": {"adultos":"80 mg VO 1x/dia se peso <100 kg; 100 mg VO 1x/dia se peso >=100 kg, em jejum. Reavaliar biópsia/elastografia em 1 ano.","pediatrica":"Segurança e eficácia não estabelecidas em menores de 18 anos.","idosos":"Sem ajuste específico; monitorar função hepática.","renal":"Sem ajuste em insuficiência renal leve a moderada; dados limitados em grave.","hepatica":"Contraindicado em Child-Pugh B/C; não estudado em cirrose compensada avançada."},
  "apresentacoes": [{"forma":"Comprimido revestido","concentracoes":["60 mg","80 mg","100 mg"],"obs":"via oral, em jejum"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Resmetirom + Estatinas (rosuvastatina, sinvastatina, pravastatina)","mecanismo":"Inibição de transportadores hepáticos OATP1B1/1B3, elevando a exposição à estatina","conduta":"Reduzir dose da estatina conforme bula e monitorar sintomas de miopatia/CK"}],"moderadas":[{"par":"Resmetirom + Substratos de CYP2C8/CYP3A4","mecanismo":"Potencial alteração do metabolismo de outros fármacos","conduta":"Monitorar eficácia/toxicidade de fármacos de janela terapêutica estreita"}],"menores":[{"par":"Resmetirom + Levotiroxina","mecanismo":"Mecanismo hepático tireoidiano seletivo, interação teórica limitada","conduta":"Monitorar função tireoidiana se uso concomitante"}]},
  "interacoesAlimentares": "Tomar preferencialmente em jejum, conforme estudo de registro; alimentos podem alterar a absorção.",
  "reacoesAdversas": {"muitoComuns":["Diarreia","Náusea"],"comuns":["Prurido","Vômito","Dor abdominal","Tontura"],"incomuns":["Elevação de transaminases"],"raras":[],"graves":["Hepatotoxicidade medicamentosa (elevação acentuada de transaminases)","Colelitíase sintomática"]},
  "alertasFarmaceuticos": ["Medicamento novo (aprovação FDA em 2024), sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente.","Primeiro fármaco aprovado especificamente para MASH com fibrose — reforçar que não substitui perda de peso, controle glicêmico/lipídico e abstinência alcoólica.","Checar uso de estatinas em todo paciente candidato, pelo risco de interação farmacocinética relevante."],
  "orientacoesPaciente": {"comoTomar":"1 comprimido por dia, em jejum, sempre no mesmo horário.","esquecimento":"Se esquecer, tomar assim que lembrar no mesmo dia; não duplicar a dose.","dirigir":"Sem restrição conhecida; suspender se tontura importante.","alcool":"Evitar álcool — agrava a doença hepática de base.","alimentos":"Tomar em jejum, conforme orientação do estudo de registro.","sinaisAlerta":"Icterícia, urina escura, fezes claras, dor abdominal intensa, fadiga incomum: procurar atendimento médico e suspender o medicamento."},
  "monitoramento": [{"parametro":"ALT/AST/bilirrubinas","quando":"Antes de iniciar e periodicamente conforme orientação médica"},{"parametro":"Perfil lipídico e CK (se em uso de estatina)","quando":"Periodicamente"},{"parametro":"Elastografia hepática/biópsia","quando":"Reavaliação em 1 ano de tratamento"}],
  "gestacao": "Dados em humanos insuficientes. Em modelos animais, não houve sinal claro de teratogenicidade nas doses estudadas, mas a bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA). Uso não recomendado na gestação por falta de dados robustos.",
  "gestacaoCategoria": "C",
  "lactacao": "Desconhecido se é excretado no leite humano. Pela ausência de dados, avaliar risco-benefício individualmente.",
  "lactacaoCategoria": "L3",
  "pediatria": "Não estabelecido abaixo de 18 anos.",
  "geriatria": "Sem ajuste específico descrito; monitorar função hepática e interação com estatinas, comuns nessa faixa etária.",
  "renal": "Sem ajuste necessário em disfunção renal leve a moderada; dados limitados em insuficiência renal grave.",
  "hepatica": "Contraindicado em cirrose descompensada (Child-Pugh B/C); não recomendado em cirrose compensada avançada por dados insuficientes.",
  "tipoReceituario": "Receita Simples (venda sob prescrição médica — sem registro ANVISA confirmado até o momento desta ficha).",
  "dispensacao": {"controleEspecial": False, "retencaoReceita": False, "condicoes": "Sem registro ANVISA confirmado até a data desta ficha; nos EUA é medicamento de prescrição (Rx). Acompanhar a situação regulatória no Brasil antes de orientar dispensação."},
  "referencias": ["FDA. Rezdiffra (resmetirom) Prescribing Information, 2024.","Harrison SA et al. A Phase 3, Randomized, Controlled Trial of Resmetirom in NASH with Liver Fibrosis. N Engl J Med. 2024.","AASLD Practice Guidance on MASLD/MASH."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: resmetirom")

NOVOS["lenacapavir"] = {
  "nomeGenerico": "Lenacapavir",
  "classeTerapeutica": "Antivirais HIV, Outros (Classe J5C9)",
  "classes": [{"codigo":"J5C9","nome":"Antivirais HIV, Outros"}],
  "nomesComerciais": {"referencia":"Sunlenca® (Gilead); também comercializado como Yeztugo® para PrEP (sem registro confirmado na ANVISA até o momento desta ficha)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Inibidor seletivo do capsídeo do HIV-1, bloqueando múltiplas etapas do ciclo viral (montagem, liberação e desmontagem do capsídeo), com meia-vida longa que permite administração subcutânea semestral.",
  "farmacocinetica": "Biodisponibilidade subcutânea lenta e sustentada após dose de ataque oral; ligação proteica muito alta (>98%); metabolismo por CYP3A e UGT1A1; meia-vida terminal de aproximadamente 8 a 12 semanas, permitindo dose a cada 6 meses.",
  "indicacoes": ["Tratamento do HIV-1 multirresistente, em associação com outros antirretrovirais, em pacientes fortemente tratados previamente", "Profilaxia pré-exposição (PrEP) ao HIV em adultos e adolescentes de risco"],
  "contraindicacoes": ["Hipersensibilidade ao lenacapavir ou excipientes", "Uso concomitante de indutores fortes de CYP3A/P-gp (rifampicina, carbamazepina, fenitoína, erva-de-são-joão)"],
  "precaucoes": ["Reações no local de injeção são comuns e podem persistir por meses (nódulos subcutâneos)", "Confirmar status HIV negativo antes de iniciar para PrEP", "Risco de resistência cruzada com outros inibidores de capsídeo em desenvolvimento"],
  "posologia": {"adultos":"Dose de início oral (dias 1 e 2) seguida de injeção subcutânea no abdome; manutenção com injeção subcutânea a cada 6 meses, conforme esquema específico da bula.","pediatrica":"Aprovado para adolescentes >=35 kg em alguns esquemas; seguir orientação especializada.","idosos":"Sem ajuste específico descrito.","renal":"Sem ajuste em insuficiência renal leve a moderada; dados limitados em grave/diálise.","hepatica":"Sem ajuste em insuficiência hepática leve a moderada; não recomendado em grave."},
  "apresentacoes": [{"forma":"Comprimido revestido (dose de início)","concentracoes":["300 mg"],"obs":"via oral"},{"forma":"Solução injetável subcutânea (manutenção)","concentracoes":["463,5 mg/1,5 mL"],"obs":"aplicação por profissional de saúde, região abdominal"}],
  "viasAdministracao": ["Oral", "Subcutânea"],
  "interacoes": {"graves":[{"par":"Lenacapavir + Indutores fortes de CYP3A/P-gp (rifampicina, fenitoína, carbamazepina, erva-de-são-joão)","mecanismo":"Redução acentuada da concentração plasmática do lenacapavir, com risco de falha terapêutica e resistência","conduta":"Contraindicado o uso concomitante"}],"moderadas":[{"par":"Lenacapavir + Substratos de CYP3A/UGT1A1 de janela terapêutica estreita","mecanismo":"Lenacapavir é inibidor moderado dessas vias, podendo elevar exposição do outro fármaco","conduta":"Monitorar sinais de toxicidade; ajustar dose se necessário"}],"menores":[{"par":"Lenacapavir + Antiácidos","mecanismo":"Possível alteração discreta de absorção da dose oral","conduta":"Sem restrição específica relevante descrita"}]},
  "interacoesAlimentares": "Pode ser administrado com ou sem alimentos na dose oral.",
  "reacoesAdversas": {"muitoComuns":["Reação no local de injeção (nódulo, eritema, dor)"],"comuns":["Cefaleia","Náusea"],"incomuns":["Erupção cutânea"],"raras":[],"graves":["Reação de hipersensibilidade sistêmica (rara)"]},
  "alertasFarmaceuticos": ["Medicamento de aplicação exclusivamente profissional (injeção subcutânea) — orientar o paciente sobre a importância de não faltar às doses semestrais.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente.","Nódulos subcutâneos no local de aplicação podem persistir por meses; orientar o paciente sobre esse efeito esperado para reduzir ansiedade e evitar automedicação."],
  "orientacoesPaciente": {"comoTomar":"Comprimidos orais apenas na fase de início; a manutenção é por injeção aplicada em serviço de saúde a cada 6 meses.","esquecimento":"Não se aplica à injeção (aplicada por profissional); se esquecer comprimido da fase de início, contatar o serviço de saúde.","dirigir":"Sem restrição conhecida.","alcool":"Sem interação relevante descrita; seguir orientação geral de adesão ao tratamento antirretroviral.","alimentos":"Pode tomar com ou sem alimentos.","sinaisAlerta":"Febre, erupção cutânea extensa, inchaço importante no local de aplicação ou falta de ar: procurar atendimento médico."},
  "monitoramento": [{"parametro":"Carga viral de HIV e CD4","quando":"Conforme protocolo de acompanhamento antirretroviral"},{"parametro":"Função hepática","quando":"Periodicamente"},{"parametro":"Local de aplicação (reação/nódulo)","quando":"A cada visita"}],
  "gestacao": "Dados limitados em gestantes; a bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA). Usar apenas se o benefício justificar o risco, conforme avaliação médica especializada em HIV e gestação.",
  "gestacaoCategoria": "C",
  "lactacao": "Não se recomenda amamentação em mães vivendo com HIV, conforme diretrizes brasileiras, independentemente do antirretroviral utilizado.",
  "lactacaoCategoria": "L4",
  "pediatria": "Uso em adolescentes >=35 kg conforme indicação específica; não estabelecido em crianças menores.",
  "geriatria": "Dados limitados; sem ajuste específico descrito.",
  "renal": "Sem ajuste em disfunção renal leve a moderada; cautela em insuficiência renal grave por dados limitados.",
  "hepatica": "Sem ajuste em insuficiência hepática leve a moderada; não recomendado em insuficiência hepática grave.",
  "tipoReceituario": "Receita de Controle Especial (antirretroviral — dispensação em serviço especializado, componente especializado/programa DST-AIDS)",
  "dispensacao": {"controleEspecial": True, "retencaoReceita": True, "condicoes": "Dispensado por programas especializados de HIV/AIDS; aplicação injetável restrita a serviço de saúde. Sem registro ANVISA confirmado até a data desta ficha — verificar situação regulatória."},
  "referencias": ["FDA. Sunlenca (lenacapavir) Prescribing Information, 2022.","FDA. Yeztugo (lenacapavir) Prescribing Information para PrEP, 2025.","Ministério da Saúde. Protocolo Clínico e Diretrizes Terapêuticas para Manejo da Infecção pelo HIV."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: lenacapavir")

NOVOS["zuranolona"] = {
  "nomeGenerico": "Zuranolona",
  "classeTerapeutica": "Antidepressivos Todos os Outros (Classe N6A9)",
  "classes": [{"codigo":"N6A9","nome":"Antidepressivos Todos os Outros"}],
  "nomesComerciais": {"referencia":"Zurzuvae® (EUA, Sage/Biogen; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Modulador alostérico positivo de receptores GABA-A (neuroesteroide sintético análogo da alopregnanolona), com ação rápida de curso curto (14 dias) específica para depressão pós-parto.",
  "farmacocinetica": "Absorção oral aumentada com alimento rico em gordura; ligação proteica muito alta; metabolismo hepático extenso via CYP3A4; meia-vida de aproximadamente 16 a 23 horas.",
  "indicacoes": ["Depressão pós-parto em adultas, ciclo de tratamento de 14 dias"],
  "contraindicacoes": ["Hipersensibilidade à zuranolona ou excipientes"],
  "precaucoes": ["Sonolência intensa — orientar sobre não dirigir nem operar máquinas durante o tratamento e por período após a última dose", "Risco de pensamentos suicidas (classe de antidepressivos) — reforçar sinais de alerta", "Uso concomitante de outros depressores do SNC aumenta sedação"],
  "posologia": {"adultos":"50 mg VO 1x/dia à noite, com alimento gorduroso, por 14 dias consecutivos; não repetir ciclo sem reavaliação médica.","pediatrica":"Não indicado em pediatria (indicação é depressão pós-parto em adultas).","idosos":"Não aplicável à indicação (depressão pós-parto).","renal":"Sem ajuste em insuficiência renal leve a moderada; não recomendado em grave.","hepatica":"Reduzir dose em insuficiência hepática leve a moderada; não recomendado em grave."},
  "apresentacoes": [{"forma":"Cápsula","concentracoes":["20 mg","25 mg","30 mg","40 mg","45 mg","50 mg"],"obs":"tomar à noite, com alimento"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Zuranolona + Álcool e outros depressores do SNC (benzodiazepínicos, opioides)","mecanismo":"Somação de efeitos sedativos e depressores do SNC","conduta":"Evitar associação; se inevitável, alertar sobre sonolência intensa e risco de prejuízo psicomotor"}],"moderadas":[{"par":"Zuranolona + Inibidores/indutores de CYP3A4","mecanismo":"Alteração relevante da concentração plasmática da zuranolona","conduta":"Ajustar dose conforme bula ou evitar associação com indutores fortes"}],"menores":[{"par":"Zuranolona + Contraceptivos hormonais orais","mecanismo":"Interação pouco relevante descrita","conduta":"Sem necessidade de ajuste específico"}]},
  "interacoesAlimentares": "Administrar à noite com refeição rica em gordura para otimizar absorção, conforme estudos de registro.",
  "reacoesAdversas": {"muitoComuns":["Sonolência","Tontura"],"comuns":["Cefaleia","Diarreia","Infecção do trato urinário","Sedação"],"incomuns":["Boca seca"],"raras":[],"graves":["Ideação suicida (classe de antidepressivos)","Comprometimento da capacidade de dirigir"]},
  "alertasFarmaceuticos": ["Orientar explicitamente a não dirigir veículos nem operar máquinas durante os 14 dias de tratamento e nas horas seguintes à última dose, pelo risco de sonolência intensa.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente.","Reforçar que o ciclo é curto (14 dias) e não deve ser repetido ou prolongado sem reavaliação médica."],
  "orientacoesPaciente": {"comoTomar":"1 cápsula à noite, com uma refeição que contenha gordura, por 14 dias seguidos.","esquecimento":"Se esquecer, pular a dose do dia e retomar no horário habitual no dia seguinte; não duplicar.","dirigir":"Não dirigir nem operar máquinas durante o tratamento, pelo risco de sonolência intensa.","alcool":"Evitar álcool completamente durante os 14 dias de tratamento.","alimentos":"Tomar sempre com alimento, preferencialmente com gordura, à noite.","sinaisAlerta":"Pensamentos de se machucar, piora do humor, sonolência incapacitante: procurar ajuda médica imediatamente."},
  "monitoramento": [{"parametro":"Humor e risco de suicídio","quando":"Durante todo o ciclo de 14 dias e após"},{"parametro":"Nível de sedação/sonolência","quando":"Diariamente durante o tratamento"},{"parametro":"Função hepática (se uso prévio alterado)","quando":"Conforme avaliação clínica"}],
  "gestacao": "Não indicado durante a gestação (indicação é pós-parto). Dados de exposição gestacional são limitados; a bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA).",
  "gestacaoCategoria": "C",
  "lactacao": "Presente no leite materno; dados de segurança no lactente limitado. Avaliar risco-benefício com a equipe médica antes de amamentar durante o tratamento.",
  "lactacaoCategoria": "L3",
  "pediatria": "Não aplicável — indicação restrita a depressão pós-parto em adultas.",
  "geriatria": "Não aplicável à indicação.",
  "renal": "Sem ajuste em insuficiência renal leve a moderada; não recomendado em insuficiência renal grave por dados insuficientes.",
  "hepatica": "Reduzir dose em insuficiência hepática leve a moderada (conforme bula); não recomendado em insuficiência hepática grave.",
  "tipoReceituario": "Receita de Controle Especial (ação no SNC — psicotrópico, Lista B1 da Portaria SVS/MS 344/98, por analogia a neuroesteroides moduladores GABAérgicos)",
  "dispensacao": {"controleEspecial": True, "retencaoReceita": True, "condicoes": "Sem registro ANVISA confirmado até a data desta ficha — verificar enquadramento regulatório exato antes de orientar dispensação."},
  "referencias": ["FDA. Zurzuvae (zuranolone) Prescribing Information, 2023.","Deligiannidis KM et al. Zuranolone for the Treatment of Postpartum Depression. Am J Psychiatry. 2023.","ANVISA. Portaria SVS/MS nº 344/1998 (listas de substâncias controladas)."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: zuranolona")

NOVOS["gepotidacina"] = {
  "nomeGenerico": "Gepotidacina",
  "classeTerapeutica": "Todos os Outros Antibióticos (Classe J1X9)",
  "classes": [{"codigo":"J1X9","nome":"Todos os Outros Antibióticos"}],
  "nomesComerciais": {"referencia":"Blujepa® (EUA, GSK; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Antibacteriano triazaacenaftileno, primeira classe nova de antibiótico oral em décadas: inibe seletivamente a topoisomerase bacteriana tipo II (DNA girase e topoisomerase IV) por mecanismo distinto das fluoroquinolonas, bloqueando a replicação do DNA bacteriano.",
  "farmacocinetica": "Absorção oral com biodisponibilidade moderada; ligação proteica intermediária; metabolismo hepático parcial; excreção renal e fecal; meia-vida de aproximadamente 7 a 10 horas.",
  "indicacoes": ["Infecção do trato urinário não complicada (cistite aguda) em mulheres adultas e adolescentes, causada por patógenos suscetíveis"],
  "contraindicacoes": ["Hipersensibilidade à gepotidacina ou excipientes"],
  "precaucoes": ["Reservar para quando antibióticos de primeira linha não forem adequados, por política de uso racional e preservação da nova classe", "Risco de prolongamento do intervalo QT — cautela em cardiopatas e uso concomitante de outros fármacos que prolongam QT", "Pode causar efeitos gastrointestinais significativos (náusea, diarreia)"],
  "posologia": {"adultos":"1.500 mg VO a cada 12 horas, por 5 dias, com alimento.","pediatrica":"Indicado a partir de 12 anos com peso >=40 kg, mesma posologia de adultos; não estabelecido abaixo disso.","idosos":"Sem ajuste específico; considerar função renal.","renal":"Sem ajuste em insuficiência renal leve; cautela e dados limitados em moderada/grave.","hepatica":"Sem ajuste em insuficiência hepática leve a moderada; dados limitados em grave."},
  "apresentacoes": [{"forma":"Comprimido revestido","concentracoes":["750 mg"],"obs":"tomar 2 comprimidos a cada 12 horas, com alimento"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Gepotidacina + Outros fármacos que prolongam o intervalo QT (antiarrítmicos classe IA/III, alguns antipsicóticos, macrolídeos)","mecanismo":"Somação de risco de prolongamento do QT e arritmia","conduta":"Evitar associação; se necessário, monitorar ECG"}],"moderadas":[{"par":"Gepotidacina + Antiácidos/suplementos com cátions polivalentes (cálcio, magnésio, ferro)","mecanismo":"Possível redução da absorção por quelação","conduta":"Espaçar administração em pelo menos 2 a 3 horas"}],"menores":[{"par":"Gepotidacina + Alimentos","mecanismo":"Alimento aumenta a absorção e reduz desconforto gastrointestinal","conduta":"Orientar a tomar sempre com refeição"}]},
  "interacoesAlimentares": "Tomar com alimento para melhorar absorção e tolerabilidade gastrointestinal.",
  "reacoesAdversas": {"muitoComuns":["Diarreia","Náusea"],"comuns":["Dor abdominal","Cefaleia","Vulvovaginite por cândida"],"incomuns":["Tontura"],"raras":[],"graves":["Prolongamento do intervalo QT","Colite associada a Clostridioides difficile (classe de antibióticos)"]},
  "alertasFarmaceuticos": ["Medicamento reservado como alternativa quando antibióticos de primeira linha (ex.: nitrofurantoína, fosfomicina, sulfametoxazol-trimetoprima) não forem adequados, por ser representante de nova classe — reforçar uso racional para preservar eficácia futura.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente.","Checar histórico de arritmia/uso de outros fármacos que prolongam QT antes da dispensação, quando possível."],
  "orientacoesPaciente": {"comoTomar":"2 comprimidos a cada 12 horas, com alimento, por 5 dias completos mesmo que os sintomas melhorem antes.","esquecimento":"Tomar assim que lembrar; se estiver próximo da próxima dose, pular a esquecida e não duplicar.","dirigir":"Sem restrição conhecida; suspender se tontura importante.","alcool":"Sem interação relevante descrita, mas evitar durante tratamento de infecção.","alimentos":"Tomar sempre com refeição para melhor absorção e tolerância.","sinaisAlerta":"Palpitações, desmaio, diarreia intensa com sangue ou febre persistente: procurar atendimento médico."},
  "monitoramento": [{"parametro":"Resolução dos sintomas urinários","quando":"Ao final do tratamento de 5 dias"},{"parametro":"ECG (se fator de risco para QT longo)","quando":"Antes e durante o tratamento, se indicado"},{"parametro":"Sinais de colite por C. difficile","quando":"Durante e após o tratamento, se diarreia persistente"}],
  "gestacao": "Dados em humanos insuficientes; a bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA). Uso não recomendado na gestação por falta de dados robustos.",
  "gestacaoCategoria": "C",
  "lactacao": "Dados insuficientes sobre excreção no leite humano; avaliar risco-benefício individualmente.",
  "lactacaoCategoria": "L3",
  "pediatria": "Indicado a partir de 12 anos com peso >=40 kg; não estabelecido em crianças menores.",
  "geriatria": "Sem ajuste específico; considerar função renal e risco cardiovascular (QT) nessa faixa etária.",
  "renal": "Sem ajuste em insuficiência renal leve; cautela e dados limitados em insuficiência renal moderada a grave.",
  "hepatica": "Sem ajuste em insuficiência hepática leve a moderada; dados limitados em insuficiência hepática grave.",
  "tipoReceituario": "Receita Simples (antibiótico — venda sob prescrição médica, retenção de receita conforme RDC 471/2021)",
  "dispensacao": {"controleEspecial": False, "retencaoReceita": True, "condicoes": "Antimicrobiano sujeito a retenção de receita conforme RDC 471/2021. Sem registro ANVISA confirmado até a data desta ficha — verificar situação regulatória."},
  "referencias": ["FDA. Blujepa (gepotidacin) Prescribing Information, 2025.","Kaye KS et al. Gepotidacin for Uncomplicated Urinary Tract Infection. Lancet. 2024.","ANVISA. RDC nº 471/2021 (retenção de receita de antimicrobianos)."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: gepotidacina")

NOVOS["sotagliflozina"] = {
  "nomeGenerico": "Sotagliflozina",
  "classeTerapeutica": "Antidiabéticos Inibidores de SGLT2, Puros (Classe A10P1)",
  "classes": [{"codigo":"A10P1","nome":"Antidiabéticos Inibidores de SGLT2, Puros"}],
  "nomesComerciais": {"referencia":"Inpefa® (EUA, Lexicon Pharmaceuticals; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Inibidor duplo de SGLT1 (intestinal) e SGLT2 (renal): reduz e retarda a absorção intestinal de glicose e aumenta a excreção urinária de glicose, com benefício adicional em insuficiência cardíaca independentemente do diabetes.",
  "farmacocinetica": "Absorção oral rápida; ligação proteica alta; metabolismo hepático via glicuronidação (UGT1A9); meia-vida de aproximadamente 21 horas, permitindo dose única diária.",
  "indicacoes": ["Redução do risco de morte cardiovascular, hospitalização por insuficiência cardíaca e consultas de urgência por insuficiência cardíaca em adultos com insuficiência cardíaca ou diabetes tipo 2 com fatores de risco cardiovascular/renal"],
  "contraindicacoes": ["Hipersensibilidade à sotagliflozina ou excipientes", "Diabetes tipo 1 (risco aumentado de cetoacidose diabética)", "Diálise"],
  "precaucoes": ["Risco de cetoacidose diabética, inclusive com glicemia normal ou pouco elevada (cetoacidose euglicêmica) — suspender antes de cirurgia eletiva", "Risco de depleção de volume/hipotensão, especialmente em idosos e uso concomitante de diuréticos", "Risco de infecções genitais micóticas e, raramente, gangrena de Fournier", "Monitorar função renal"],
  "posologia": {"adultos":"200 mg VO 1x/dia antes da primeira refeição do dia; pode aumentar para 400 mg conforme tolerância e resposta.","pediatrica":"Segurança e eficácia não estabelecidas em menores de 18 anos.","idosos":"Sem ajuste específico; maior atenção ao risco de depleção de volume.","renal":"Não iniciar com TFG <25 mL/min/1,73m² ou em diálise; pode continuar se já em uso e TFG reduzir, conforme avaliação médica.","hepatica":"Sem ajuste em insuficiência hepática leve a moderada; cautela em grave."},
  "apresentacoes": [{"forma":"Comprimido revestido","concentracoes":["200 mg","400 mg"],"obs":"tomar antes da primeira refeição do dia"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Sotagliflozina + Insulina ou secretagogos (sulfonilureias)","mecanismo":"Risco aumentado de hipoglicemia quando associados","conduta":"Considerar redução da dose de insulina/secretagogo e monitorar glicemia"}],"moderadas":[{"par":"Sotagliflozina + Diuréticos","mecanismo":"Risco somado de depleção de volume e hipotensão","conduta":"Monitorar pressão arterial, estado de hidratação e função renal"}],"menores":[{"par":"Sotagliflozina + Digoxina","mecanismo":"Possível pequena alteração de concentração plasmática","conduta":"Sem necessidade de ajuste rotineiro; monitorar se sintomas"}]},
  "interacoesAlimentares": "Tomar antes da primeira refeição do dia, conforme estudos de registro.",
  "reacoesAdversas": {"muitoComuns":["Hipoglicemia (em uso com insulina/secretagogo)"],"comuns":["Infecção genital micótica","Diarreia","Infecção do trato urinário","Tontura"],"incomuns":["Depleção de volume"],"raras":["Gangrena de Fournier"],"graves":["Cetoacidose diabética (inclusive euglicêmica)","Gangrena de Fournier (fasciíte necrosante perineal)"]},
  "alertasFarmaceuticos": ["Orientar reconhecimento de sinais de cetoacidose (náusea, vômito, dor abdominal, mal-estar, respiração rápida) mesmo com glicemia pouco elevada — procurar atendimento médico imediato e não continuar o medicamento.","Suspender antes de cirurgias eletivas ou doenças agudas graves, conforme orientação médica, pelo risco de cetoacidose.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente."],
  "orientacoesPaciente": {"comoTomar":"1 comprimido por dia, antes da primeira refeição.","esquecimento":"Se esquecer, tomar assim que lembrar no mesmo dia; não duplicar a dose.","dirigir":"Sem restrição direta; atenção caso ocorra hipoglicemia associada a outros antidiabéticos.","alcool":"Evitar consumo excessivo — pode aumentar risco de hipoglicemia e desidratação.","alimentos":"Tomar antes da primeira refeição do dia; manter boa hidratação.","sinaisAlerta":"Náusea/vômito persistente com mal-estar, dor ou vermelhidão intensa na região genital/perineal, sinais de desidratação: procurar atendimento médico imediatamente."},
  "monitoramento": [{"parametro":"Função renal (TFG)","quando":"Antes de iniciar e periodicamente"},{"parametro":"Glicemia e sinais de cetoacidose","quando":"Continuamente, especialmente em situações de estresse agudo"},{"parametro":"Estado de hidratação e pressão arterial","quando":"Periodicamente, principalmente em idosos e uso de diuréticos"}],
  "gestacao": "Não recomendado na gestação, especialmente no segundo e terceiro trimestres, pelo potencial de afetar o desenvolvimento renal fetal (classe dos inibidores de SGLT2). A bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA).",
  "gestacaoCategoria": "C",
  "lactacao": "Não recomendado durante a amamentação; dados limitados e preocupação teórica com desenvolvimento renal do lactente, por analogia à classe.",
  "lactacaoCategoria": "L4",
  "pediatria": "Não estabelecido em menores de 18 anos.",
  "geriatria": "Maior atenção ao risco de depleção de volume e lesão renal aguda nessa faixa etária.",
  "renal": "Não iniciar com TFG <25 mL/min/1,73m² ou em diálise; monitorar função renal durante o tratamento.",
  "hepatica": "Sem ajuste em insuficiência hepática leve a moderada; cautela em insuficiência hepática grave por dados limitados.",
  "tipoReceituario": "Receita Simples (antidiabético — venda sob prescrição médica)",
  "dispensacao": {"controleEspecial": False, "retencaoReceita": False, "condicoes": "Sem registro ANVISA confirmado até a data desta ficha — verificar situação regulatória antes de orientar dispensação."},
  "referencias": ["FDA. Inpefa (sotagliflozin) Prescribing Information, 2023.","Bhatt DL et al. Sotagliflozin in Patients with Diabetes and Recent Worsening Heart Failure. N Engl J Med. 2021.","Sociedade Brasileira de Diabetes. Diretrizes 2023-2024."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: sotagliflozina")

NOVOS["daridorexanto"] = {
  "nomeGenerico": "Daridorexanto",
  "classeTerapeutica": "Hipnóticos e Sedativos Não Barbitúricos Puros (Classe N5B1)",
  "classes": [{"codigo":"N5B1","nome":"Hipnóticos e Sedativos Não Barbitúricos Puros"}],
  "nomesComerciais": {"referencia":"Quviviq® (EUA, Idorsia; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Antagonista duplo dos receptores de orexina (OX1R e OX2R), bloqueando a sinalização dos neuropeptídeos orexina A e B que promovem o estado de vigília, favorecendo o início e a manutenção do sono sem a ação GABAérgica dos hipnóticos clássicos.",
  "farmacocinetica": "Absorção oral rápida; ligação proteica alta; metabolismo hepático predominante via CYP3A4; meia-vida de aproximadamente 8 horas.",
  "indicacoes": ["Insônia em adultos, caracterizada por dificuldade de início e/ou manutenção do sono"],
  "contraindicacoes": ["Hipersensibilidade ao daridorexanto ou excipientes", "Narcolepsia", "Uso concomitante de inibidores fortes de CYP3A4"],
  "precaucoes": ["Sonolência residual no dia seguinte — orientar sobre risco ao dirigir, especialmente se a dose ou o tempo de sono forem insuficientes", "Risco de paralisia do sono e alucinações hipnagógicas/hipnopômpicas (classe dos antagonistas de orexina)", "Cautela em depressão/ideação suicida — avaliar piora de sintomas", "Evitar uso concomitante com álcool"],
  "posologia": {"adultos":"50 mg VO, 1x/noite, até 30 minutos antes de deitar, com pelo menos 7 horas disponíveis para dormir; dose máxima 50 mg/dia.","pediatrica":"Segurança e eficácia não estabelecidas em menores de 18 anos.","idosos":"Mesma dose de adultos; sem ajuste específico, mas monitorar sedação residual.","renal":"Sem ajuste em insuficiência renal leve a moderada; dados limitados em grave.","hepatica":"Sem ajuste em insuficiência hepática leve a moderada; não recomendado em grave."},
  "apresentacoes": [{"forma":"Comprimido revestido","concentracoes":["25 mg","50 mg"],"obs":"tomar até 30 minutos antes de deitar"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Daridorexanto + Inibidores fortes de CYP3A4 (cetoconazol, claritromicina, itraconazol)","mecanismo":"Aumento acentuado da exposição ao daridorexanto, com risco de sedação excessiva","conduta":"Contraindicado o uso concomitante"},{"par":"Daridorexanto + Álcool e outros depressores do SNC","mecanismo":"Somação de efeitos sedativos e depressores respiratórios","conduta":"Evitar associação"}],"moderadas":[{"par":"Daridorexanto + Indutores de CYP3A4 (rifampicina, carbamazepina)","mecanismo":"Redução da eficácia por queda da concentração plasmática","conduta":"Evitar associação ou monitorar eficácia do tratamento da insônia"}],"menores":[{"par":"Daridorexanto + Alimentos","mecanismo":"Alimento gorduroso pode retardar o início de ação","conduta":"Orientar a tomar preferencialmente sem refeição pesada antes de dormir"}]},
  "interacoesAlimentares": "Evitar administração logo após refeição rica em gordura, pois pode retardar o início do efeito hipnótico.",
  "reacoesAdversas": {"muitoComuns":["Sonolência/fadiga no dia seguinte"],"comuns":["Cefaleia","Pesadelos/sonhos anormais"],"incomuns":["Paralisia do sono","Alucinações hipnagógicas"],"raras":[],"graves":["Agravamento de depressão/ideação suicida (classe dos hipnóticos)","Complexos comportamentais do sono (sonambulismo, condução de veículo durante o sono - raro)"]},
  "alertasFarmaceuticos": ["Orientar que o medicamento deve ser tomado apenas quando houver pelo menos 7 horas disponíveis para dormir, pelo risco de sonolência residual e comprometimento psicomotor.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente.","Reforçar que não deve ser associado a álcool nem a outros depressores do SNC."],
  "orientacoesPaciente": {"comoTomar":"1 comprimido até 30 minutos antes de deitar, com pelo menos 7 horas disponíveis para dormir.","esquecimento":"Não tomar se faltarem menos de 7 horas para acordar; não compensar com dose dobrada.","dirigir":"Não dirigir nem operar máquinas se sentir sonolência residual ao acordar.","alcool":"Não associar a bebidas alcoólicas.","alimentos":"Evitar tomar logo após refeição rica em gordura, pois pode atrasar o efeito.","sinaisAlerta":"Piora do humor, pensamentos de autolesão, episódios de sonambulismo ou comportamentos durante o sono: procurar atendimento médico e suspender o uso."},
  "monitoramento": [{"parametro":"Qualidade e padrão do sono","quando":"Reavaliação periódica (sugerido em até 3 meses)"},{"parametro":"Sonolência residual diurna","quando":"A cada consulta"},{"parametro":"Humor e ideação suicida","quando":"Durante todo o tratamento, especialmente em quem já tem histórico"}],
  "gestacao": "Dados em humanos insuficientes; a bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA). Uso não recomendado na gestação por falta de dados robustos.",
  "gestacaoCategoria": "C",
  "lactacao": "Desconhecido se é excretado no leite humano; avaliar risco-benefício individualmente, considerando sedação do lactente.",
  "lactacaoCategoria": "L3",
  "pediatria": "Não estabelecido em menores de 18 anos.",
  "geriatria": "Mesma dose de adultos; maior atenção ao risco de queda e sedação residual nessa faixa etária.",
  "renal": "Sem ajuste em insuficiência renal leve a moderada; dados limitados em insuficiência renal grave.",
  "hepatica": "Sem ajuste em insuficiência hepática leve a moderada; não recomendado em insuficiência hepática grave.",
  "tipoReceituario": "Receita de Controle Especial (ação hipnótica no SNC, Lista B1 da Portaria SVS/MS 344/98, por analogia a hipnóticos não benzodiazepínicos)",
  "dispensacao": {"controleEspecial": True, "retencaoReceita": True, "condicoes": "Sem registro ANVISA confirmado até a data desta ficha — verificar enquadramento regulatório exato antes de orientar dispensação."},
  "referencias": ["FDA. Quviviq (daridorexant) Prescribing Information, 2022.","Mignot E et al. Safety and efficacy of daridorexant in patients with insomnia disorder. Lancet Neurol. 2022.","ANVISA. Portaria SVS/MS nº 344/1998 (listas de substâncias controladas)."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: daridorexanto")

NOVOS["aprocitentanto"] = {
  "nomeGenerico": "Aprocitentanto",
  "classeTerapeutica": "Anti-hipertensivos Puro-ação Periférica (Classe C2A2)",
  "classes": [{"codigo":"C2A2","nome":"Anti-hipertensivos Puro-ação Periférica"}],
  "nomesComerciais": {"referencia":"Tryvio® (EUA, Idorsia; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Antagonista duplo dos receptores de endotelina (ETA e ETB), bloqueando a vasoconstrição mediada pela endotelina-1, indicado como terapia adicional para hipertensão resistente, em associação a outros anti-hipertensivos.",
  "farmacocinetica": "Absorção oral com biodisponibilidade elevada; ligação proteica muito alta; metabolismo hepático via CYP3A4 e CYP2C9; meia-vida longa de aproximadamente 44 horas, permitindo dose única diária.",
  "indicacoes": ["Hipertensão arterial resistente, em associação com pelo menos outras duas classes de anti-hipertensivos (incluindo um diurético), quando a pressão não é controlada"],
  "contraindicacoes": ["Hipersensibilidade ao aprocitentanto ou excipientes", "Gestação (risco de malformações fetais, classe dos antagonistas de endotelina)", "Uso concomitante com outro antagonista de receptor de endotelina"],
  "precaucoes": ["Risco de retenção hídrica e insuficiência cardíaca — contraindicado em insuficiência cardíaca sintomática classe III-IV", "Hepatotoxicidade — monitorar função hepática", "Anemia/queda de hemoglobina — monitorar hemograma", "Exigir confirmação de ausência de gravidez e uso de contracepção eficaz em mulheres com potencial reprodutivo, devido a risco teratogênico (programa de controle de risco)"],
  "posologia": {"adultos":"12,5 mg VO 1x/dia, associado a esquema anti-hipertensivo otimizado contendo diurético.","pediatrica":"Segurança e eficácia não estabelecidas em menores de 18 anos.","idosos":"Sem ajuste específico; maior atenção a retenção hídrica.","renal":"Sem ajuste em insuficiência renal leve a moderada; cautela em grave/diálise.","hepatica":"Contraindicado em insuficiência hepática moderada a grave (Child-Pugh B/C)."},
  "apresentacoes": [{"forma":"Comprimido revestido","concentracoes":["12,5 mg"],"obs":"via oral, 1x/dia, sempre em associação com outros anti-hipertensivos"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Aprocitentanto + Outro antagonista de receptor de endotelina (ex.: bosentana, macitentana)","mecanismo":"Duplicação farmacológica, aumento de risco de hepatotoxicidade e retenção hídrica","conduta":"Não associar"},{"par":"Aprocitentanto + Ciclosporina/Inibidores fortes de CYP3A4","mecanismo":"Aumento importante da concentração plasmática do aprocitentanto","conduta":"Evitar associação ou ajustar conforme orientação médica"}],"moderadas":[{"par":"Aprocitentanto + Contraceptivos hormonais","mecanismo":"Possível redução da eficácia contraceptiva","conduta":"Associar método contraceptivo de barreira adicional"}],"menores":[{"par":"Aprocitentanto + Anti-hipertensivos (IECA, BRA, bloqueadores de canal de cálcio)","mecanismo":"Efeito aditivo esperado e desejado no controle pressórico","conduta":"Monitorar pressão arterial ao associar"}]},
  "interacoesAlimentares": "Pode ser administrado com ou sem alimentos.",
  "reacoesAdversas": {"muitoComuns":["Edema/retenção hídrica"],"comuns":["Cefaleia","Anemia leve","Congestão nasal"],"incomuns":["Elevação de enzimas hepáticas"],"raras":[],"graves":["Insuficiência cardíaca/retenção hídrica grave","Hepatotoxicidade","Teratogenicidade (contraindicado na gestação)"]},
  "alertasFarmaceuticos": ["Exigir confirmação de método contraceptivo eficaz em todas as mulheres com potencial reprodutivo antes da dispensação, pelo risco teratogênico documentado da classe.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente.","Orientar sobre sinais de retenção hídrica (inchaço, ganho de peso rápido, falta de ar) pelo risco de descompensação cardíaca."],
  "orientacoesPaciente": {"comoTomar":"1 comprimido por dia, sempre junto com os demais anti-hipertensivos prescritos.","esquecimento":"Se esquecer, tomar assim que lembrar no mesmo dia; não duplicar a dose.","dirigir":"Sem restrição direta conhecida.","alcool":"Evitar consumo excessivo, pelo impacto na pressão arterial e no fígado.","alimentos":"Pode tomar com ou sem alimentos.","sinaisAlerta":"Inchaço nas pernas/abdome, ganho de peso rápido, falta de ar, icterícia, urina escura: procurar atendimento médico imediatamente."},
  "monitoramento": [{"parametro":"Pressão arterial","quando":"Periodicamente, conforme ajuste terapêutico"},{"parametro":"Enzimas hepáticas (ALT/AST)","quando":"Antes de iniciar e periodicamente"},{"parametro":"Hemoglobina/hematócrito","quando":"Periodicamente"},{"parametro":"Sinais de retenção hídrica/peso","quando":"A cada consulta"}],
  "gestacao": "Contraindicado — classe dos antagonistas de receptor de endotelina é teratogênica em estudos animais, com risco bem estabelecido de malformações fetais. Exigir teste de gravidez negativo antes de iniciar e contracepção eficaz durante todo o tratamento.",
  "gestacaoCategoria": "X",
  "lactacao": "Desconhecido se é excretado no leite humano; pelo risco da classe, evitar amamentação durante o uso.",
  "lactacaoCategoria": "L4",
  "pediatria": "Não estabelecido em menores de 18 anos.",
  "geriatria": "Sem ajuste específico; maior atenção ao risco de retenção hídrica e descompensação cardíaca.",
  "renal": "Sem ajuste em insuficiência renal leve a moderada; cautela em insuficiência renal grave ou diálise por dados limitados.",
  "hepatica": "Contraindicado em insuficiência hepática moderada a grave (Child-Pugh B/C).",
  "tipoReceituario": "Receita Simples, com programa de controle de risco para gestação (venda sob prescrição médica)",
  "dispensacao": {"controleEspecial": False, "retencaoReceita": False, "condicoes": "Sem registro ANVISA confirmado até a data desta ficha. Nos EUA, dispensado sob programa de mitigação de risco (REMS) pelo potencial teratogênico — verificar exigências equivalentes caso haja registro no Brasil."},
  "referencias": ["FDA. Tryvio (aprocitentan) Prescribing Information, 2024.","Schlaich MP et al. Aprocitentan for resistant hypertension (PRECISION trial). Lancet. 2022.","Sociedade Brasileira de Cardiologia. Diretrizes de Hipertensão Arterial."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: aprocitentanto")

NOVOS["durlobactam-sulbactam"] = {
  "nomeGenerico": "Durlobactam + Sulbactam",
  "classeTerapeutica": "Todos os Outros Antibacterianos Beta-lactâmicos (Classe J1P9)",
  "classes": [{"codigo":"J1P9","nome":"Todos os Outros Antibacterianos Beta-lactâmicos"}],
  "nomesComerciais": {"referencia":"Xacduro® (EUA, Entasis/Innoviva; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Associação de sulbactam (antibiótico beta-lactâmico com atividade intrínseca contra Acinetobacter) com durlobactam, inibidor de beta-lactamases de classe A, C e D que restaura a atividade do sulbactam contra cepas produtoras dessas enzimas, incluindo Acinetobacter baumannii-calcoaceticus multirresistente.",
  "farmacocinetica": "Administração exclusivamente intravenosa; ambos os componentes têm eliminação predominantemente renal; meia-vida de aproximadamente 2 a 3 horas, exigindo infusões a cada 6 horas.",
  "indicacoes": ["Infecções intra-abdominais complicadas e pneumonia hospitalar/associada à ventilação mecânica causadas por Acinetobacter baumannii-calcoaceticus suscetível, em adultos"],
  "contraindicacoes": ["Hipersensibilidade a durlobactam, sulbactam ou outros beta-lactâmicos (penicilinas)"],
  "precaucoes": ["Reação de hipersensibilidade cruzada com penicilinas e outros beta-lactâmicos", "Ajuste obrigatório de dose conforme função renal (clearance de creatinina)", "Risco de colite associada a Clostridioides difficile", "Reservado para infecções confirmadas ou fortemente suspeitas por Acinetobacter multirresistente, por política de uso racional"],
  "posologia": {"adultos":"Durlobactam 1 g + Sulbactam 1 g, IV, a cada 6 horas, em infusão de 3 horas, por 7 a 14 dias conforme gravidade e resposta clínica; ajustar conforme função renal.","pediatrica":"Segurança e eficácia não estabelecidas em menores de 18 anos.","idosos":"Sem ajuste específico além do renal.","renal":"Ajuste de dose obrigatório conforme clearance de creatinina, inclusive em diálise — seguir tabela específica da bula.","hepatica":"Sem ajuste específico descrito."},
  "apresentacoes": [{"forma":"Pó liofilizado para solução injetável (uso IV)","concentracoes":["durlobactam 500 mg + sulbactam 500 mg por frasco-ampola"],"obs":"reconstituir e diluir conforme protocolo; infusão IV em 3 horas"}],
  "viasAdministracao": ["Intravenosa"],
  "interacoes": {"graves":[{"par":"Durlobactam-sulbactam + Outros beta-lactâmicos com alergia cruzada conhecida","mecanismo":"Risco de reação de hipersensibilidade grave em pacientes com alergia confirmada a penicilinas","conduta":"Confirmar história de alergia antes do uso; ter suporte para manejo de anafilaxia disponível"}],"moderadas":[{"par":"Durlobactam-sulbactam + Probenecida","mecanismo":"Redução da depuração renal do sulbactam, aumentando sua concentração plasmática","conduta":"Monitorar sinais de toxicidade; ajuste geralmente não necessário em curso curto"}],"menores":[{"par":"Durlobactam-sulbactam + Anticoagulantes orais","mecanismo":"Beta-lactâmicos podem alterar discretamente a flora intestinal produtora de vitamina K","conduta":"Monitorar INR se uso concomitante prolongado"}]},
  "interacoesAlimentares": "Não aplicável — uso exclusivamente intravenoso hospitalar.",
  "reacoesAdversas": {"muitoComuns":[],"comuns":["Elevação de transaminases","Diarreia","Reação no local de infusão","Hipopotassemia"],"incomuns":["Erupção cutânea"],"raras":[],"graves":["Reação de hipersensibilidade grave/anafilaxia","Colite associada a Clostridioides difficile"]},
  "alertasFarmaceuticos": ["Uso exclusivamente hospitalar, intravenoso, reservado para infecções confirmadas ou fortemente suspeitas por Acinetobacter multirresistente — reforçar política de uso racional de antimicrobianos (stewardship).","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar a equipe.","Checar sempre história de alergia a penicilinas/beta-lactâmicos antes da administração, pelo risco de reação cruzada."],
  "orientacoesPaciente": {"comoTomar":"Medicamento de uso hospitalar, administrado por infusão intravenosa por profissional de saúde a cada 6 horas.","esquecimento":"Não aplicável — administração sob supervisão da equipe de enfermagem/farmácia hospitalar.","dirigir":"Não aplicável ao contexto de internação.","alcool":"Não aplicável ao contexto de uso hospitalar agudo.","alimentos":"Não há interação relevante com alimentos (via IV).","sinaisAlerta":"Equipe deve observar sinais de reação alérgica (urticária, edema, falta de ar) durante a infusão e diarreia intensa durante/após o tratamento."},
  "monitoramento": [{"parametro":"Função renal (clearance de creatinina)","quando":"Antes e durante o tratamento, para ajuste de dose"},{"parametro":"Resposta clínica e culturas de controle","quando":"Conforme protocolo da infecção tratada"},{"parametro":"Sinais de hipersensibilidade durante a infusão","quando":"A cada administração"}],
  "gestacao": "Dados limitados em gestantes; penicilinas em geral têm longo histórico de uso considerado relativamente seguro na gestação, mas dados específicos do durlobactam são escassos. A bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA). Usar apenas se claramente necessário.",
  "gestacaoCategoria": "B",
  "lactacao": "Penicilinas em geral são compatíveis com a amamentação em baixas concentrações no leite; dados específicos do durlobactam são limitados — avaliar com a equipe médica.",
  "lactacaoCategoria": "L2",
  "pediatria": "Não estabelecido em menores de 18 anos.",
  "geriatria": "Sem ajuste específico além do renal, frequentemente relevante nessa faixa etária.",
  "renal": "Ajuste obrigatório de dose conforme função renal, inclusive em diálise — seguir tabela posológica específica da bula.",
  "hepatica": "Sem ajuste específico descrito na bula de registro.",
  "tipoReceituario": "Uso restrito hospitalar (antimicrobiano de reserva — dispensação controlada pela farmácia hospitalar/CCIH)",
  "dispensacao": {"controleEspecial": False, "retencaoReceita": True, "condicoes": "Uso exclusivamente hospitalar; dispensação acompanhada por protocolo de controle de infecção hospitalar (CCIH) e antimicrobianos de reserva. Sem registro ANVISA confirmado até a data desta ficha."},
  "referencias": ["FDA. Xacduro (sulbactam/durlobactam) Prescribing Information, 2023.","Kaye KS et al. Durlobactam/sulbactam vs colistin for Acinetobacter infections (ATTACK trial). Lancet Infect Dis. 2023.","ANVISA. RDC nº 471/2021 (retenção de receita de antimicrobianos)."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: durlobactam-sulbactam")

NOVOS["vadadustate"] = {
  "nomeGenerico": "Vadadustate",
  "classeTerapeutica": "Eritropoietínas (Classe B3C)",
  "classes": [{"codigo":"B3C","nome":"Eritropoietínas"}],
  "nomesComerciais": {"referencia":"Vafseo® (EUA/Europa, Akebia/Mitsubishi Tanabe; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Inibidor oral da prolil-hidroxilase do fator induzível por hipóxia (HIF-PHI), estabilizando o HIF e estimulando a produção endógena de eritropoietina e a absorção de ferro, como alternativa oral às eritropoietinas injetáveis no tratamento da anemia da doença renal crônica.",
  "farmacocinetica": "Absorção oral rápida; ligação proteica muito alta; metabolismo hepático parcial (glicuronidação e oxidação); eliminação biliar/fecal predominante; meia-vida de aproximadamente 4 a 6 horas, com administração diária.",
  "indicacoes": ["Anemia associada à doença renal crônica em pacientes em diálise (hemodiálise ou diálise peritoneal) há pelo menos 3 meses"],
  "contraindicacoes": ["Hipersensibilidade ao vadadustate ou excipientes", "Hipertensão não controlada"],
  "precaucoes": ["Risco de eventos tromboembólicos e cardiovasculares (classe dos HIF-PHI), semelhante ao observado com agentes estimuladores de eritropoiese", "Monitorar hemoglobina para evitar correção excessiva (meta de hemoglobina deve seguir faixa definida, evitando valores muito altos)", "Avaliar reservas de ferro antes e durante o tratamento", "Não indicado para anemia não relacionada à doença renal crônica nem para pacientes não dialíticos (uso aprovado restrito a diálise em algumas agências)"],
  "posologia": {"adultos":"Dose inicial de 300 mg VO 1x/dia (ou conforme peso/hemoglobina basal), com ajustes individualizados a cada 4 semanas conforme resposta de hemoglobina, seguindo tabela de titulação da bula.","pediatrica":"Segurança e eficácia não estabelecidas em menores de 18 anos.","idosos":"Sem ajuste específico além dos critérios de titulação por hemoglobina.","renal":"Indicado especificamente para pacientes em diálise; não necessita ajuste adicional além da titulação padrão.","hepatica":"Cautela em insuficiência hepática grave; dados limitados."},
  "apresentacoes": [{"forma":"Comprimido revestido","concentracoes":["150 mg","300 mg","450 mg"],"obs":"via oral, 1x/dia, dose titulada conforme hemoglobina"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Vadadustate + Quelantes de fósforo à base de cátions polivalentes (sevelamer, carbonato de cálcio, lantânio)","mecanismo":"Redução da absorção do vadadustate por ligação no trato gastrointestinal","conduta":"Espaçar a administração do vadadustate em pelo menos 1 hora antes ou 2 horas depois do quelante"}],"moderadas":[{"par":"Vadadustate + Suplementos de ferro oral","mecanismo":"Possível interação de absorção; a eficácia do vadadustate também depende de reservas adequadas de ferro","conduta":"Avaliar necessidade de suplementação de ferro conforme ferritina/saturação de transferrina, ajustando horários se necessário"}],"menores":[{"par":"Vadadustate + Estatinas","mecanismo":"Possível alteração discreta de exposição por via de transportadores hepáticos","conduta":"Sem necessidade de ajuste rotineiro; monitorar se sintomas de miopatia"}]},
  "interacoesAlimentares": "Pode ser administrado com ou sem alimentos.",
  "reacoesAdversas": {"muitoComuns":["Hipertensão"],"comuns":["Diarreia","Náusea","Dor nas costas","Trombose de acesso vascular (em hemodiálise)"],"incomuns":["Hiperpotassemia"],"raras":[],"graves":["Eventos tromboembólicos (trombose venosa profunda, embolia pulmonar)","Eventos cardiovasculares maiores (infarto, AVC)"]},
  "alertasFarmaceuticos": ["Orientar o espaçamento correto entre o vadadustate e quelantes de fósforo/suplementos de ferro, comuns em pacientes em diálise, para não comprometer a absorção.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar o paciente.","Reforçar a importância do monitoramento regular de hemoglobina para evitar correção excessiva, associada a maior risco cardiovascular."],
  "orientacoesPaciente": {"comoTomar":"1 comprimido por dia, no horário combinado, podendo ser com ou sem alimentos.","esquecimento":"Se esquecer, tomar assim que lembrar no mesmo dia; não duplicar a dose no dia seguinte.","dirigir":"Sem restrição direta conhecida.","alcool":"Sem interação direta relevante descrita; seguir orientação geral para pacientes renais crônicos.","alimentos":"Pode tomar com ou sem alimentos; respeitar intervalo de quelantes de fósforo e suplementos de ferro.","sinaisAlerta":"Dor ou inchaço em uma perna, falta de ar súbita, dor no peito, sinais de AVC (fraqueza súbita, dificuldade de fala): procurar atendimento médico de urgência."},
  "monitoramento": [{"parametro":"Hemoglobina","quando":"A cada 2 a 4 semanas durante titulação, depois periodicamente"},{"parametro":"Ferritina e saturação de transferrina","quando":"Periodicamente, para avaliar reservas de ferro"},{"parametro":"Pressão arterial","quando":"A cada consulta"},{"parametro":"Sinais de evento tromboembólico","quando":"Continuamente durante o tratamento"}],
  "gestacao": "Dados em humanos insuficientes; a bula não utiliza mais o sistema clássico de categorias A-X (regra PLLR da FDA). Uso não recomendado na gestação por falta de dados robustos — a anemia da gestação tem manejo próprio, distinto da anemia da doença renal crônica dialítica.",
  "gestacaoCategoria": "C",
  "lactacao": "Dados insuficientes sobre excreção no leite humano; avaliar risco-benefício individualmente.",
  "lactacaoCategoria": "L3",
  "pediatria": "Não estabelecido em menores de 18 anos.",
  "geriatria": "Sem ajuste específico além da titulação padrão por hemoglobina; atenção ao risco cardiovascular, mais prevalente nessa faixa etária.",
  "renal": "Indicado especificamente para pacientes em diálise (hemodiálise ou peritoneal); não é a indicação para doença renal crônica não dialítica nos EUA.",
  "hepatica": "Cautela em insuficiência hepática grave por dados limitados; sem ajuste específico estabelecido.",
  "tipoReceituario": "Receita Simples (uso sob acompanhamento nefrológico)",
  "dispensacao": {"controleEspecial": False, "retencaoReceita": False, "condicoes": "Dispensação tipicamente vinculada a programas de atenção ao paciente renal crônico em diálise. Sem registro ANVISA confirmado até a data desta ficha — verificar situação regulatória."},
  "referencias": ["FDA/EMA. Vafseo (vadadustat) Prescribing Information, 2020/2024.","Eckardt KU et al. Safety and Efficacy of Vadadustat for Anemia in Patients Undergoing Dialysis. N Engl J Med. 2021.","Sociedade Brasileira de Nefrologia. Diretrizes de Anemia na Doença Renal Crônica."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: vadadustate")

NOVOS["elinzanetanto"] = {
  "nomeGenerico": "Elinzanetanto",
  "classeTerapeutica": "Outros Hormônios Sexuais e Produtos Similares (Classe G3X)",
  "classes": [{"codigo":"G3X","nome":"Outros Hormônios Sexuais e Produtos Similares"}],
  "nomesComerciais": {"referencia":"Lynkuet® (EUA, Bayer; sem registro confirmado na ANVISA até o momento)","similares":[]},
  "generico": False, "similar": False, "farmaciaPopular": False,
  "mecanismoAcao": "Antagonista duplo dos receptores de neuroquinina 1 e 3 (NK1/NK3) no hipotálamo, modulando a via termorreguladora alterada pela queda de estrogênio, reduzindo a frequência e a intensidade dos sintomas vasomotores (fogachos) da menopausa sem uso de hormônios.",
  "farmacocinetica": "Absorção oral; ligação proteica alta; metabolismo hepático via CYP3A4 e CYP2C9; meia-vida de aproximadamente 10 a 12 horas, permitindo dose única diária.",
  "indicacoes": ["Sintomas vasomotores moderados a intensos associados à menopausa (fogachos), como alternativa não hormonal"],
  "contraindicacoes": ["Hipersensibilidade ao elinzanetanto ou excipientes", "Insuficiência hepática grave"],
  "precaucoes": ["Monitorar enzimas hepáticas, especialmente nos primeiros meses de tratamento (classe dos antagonistas NK3 associada a risco de elevação de transaminases)", "Não indicado para contracepção nem possui efeito hormonal — não substitui terapia de reposição hormonal quando esta for a indicação clínica", "Uso concomitante com indutores/inibidores de CYP3A4 pode alterar eficácia/segurança"],
  "posologia": {"adultos":"120 mg VO 1x/dia, à noite ou conforme orientação médica, podendo reavaliar continuidade após alguns meses de uso.","pediatrica":"Não aplicável — indicação restrita a sintomas da menopausa.","idosos":"Sem ajuste específico; indicação é tipicamente nessa faixa etária (perimenopausa/pós-menopausa).","renal":"Sem ajuste em insuficiência renal leve a moderada; dados limitados em grave.","hepatica":"Contraindicado em insuficiência hepática grave; cautela e monitoramento em leve a moderada."},
  "apresentacoes": [{"forma":"Comprimido revestido","concentracoes":["120 mg"],"obs":"via oral, 1x/dia"}],
  "viasAdministracao": ["Oral"],
  "interacoes": {"graves":[{"par":"Elinzanetanto + Indutores fortes de CYP3A4 (rifampicina, carbamazepina, erva-de-são-joão)","mecanismo":"Redução importante da concentração plasmática e da eficácia","conduta":"Evitar associação"}],"moderadas":[{"par":"Elinzanetanto + Inibidores de CYP3A4/CYP2C9","mecanismo":"Possível aumento da exposição ao elinzanetanto","conduta":"Monitorar efeitos adversos, especialmente hepáticos"}],"menores":[{"par":"Elinzanetanto + Contraceptivos hormonais","mecanismo":"Elinzanetanto não tem ação hormonal direta; interação pouco provável","conduta":"Sem restrição específica relevante descrita"}]},
  "interacoesAlimentares": "Pode ser administrado com ou sem alimentos.",
  "reacoesAdversas": {"muitoComuns":[],"comuns":["Cefaleia","Elevação de transaminases","Sonolência"],"incomuns":["Dor abdominal"],"raras":[],"graves":["Hepatotoxicidade (elevação significativa de transaminases)"]},
  "alertasFarmaceuticos": ["Classificação farmacológica (G — hormônios sexuais) reflete a indicação clínica em sintomas da menopausa, mas o elinzanetanto NÃO é um hormônio — é um antagonista de neuroquinina; reforçar essa diferença ao orientar a paciente, especialmente quem evita hormônios por contraindicação própria.","Sem registro confirmado na ANVISA até a data desta ficha — conferir Bulário Eletrônico antes de orientar a paciente.","Reforçar a necessidade de monitoramento hepático periódico, sobretudo nos primeiros meses de uso."],
  "orientacoesPaciente": {"comoTomar":"1 comprimido por dia, preferencialmente sempre no mesmo horário.","esquecimento":"Se esquecer, tomar assim que lembrar no mesmo dia; não duplicar a dose.","dirigir":"Avaliar resposta individual quanto à sonolência antes de dirigir.","alcool":"Evitar consumo excessivo, pelo potencial impacto hepático somado.","alimentos":"Pode tomar com ou sem alimentos.","sinaisAlerta":"Icterícia, urina escura, fadiga incomum, dor abdominal no quadrante superior direito: procurar atendimento médico e suspender o uso."},
  "monitoramento": [{"parametro":"Enzimas hepáticas (ALT/AST)","quando":"Antes de iniciar e periodicamente nos primeiros meses"},{"parametro":"Frequência e intensidade dos fogachos","quando":"Reavaliação clínica periódica"},{"parametro":"Necessidade de continuidade do tratamento","quando":"Reavaliação a cada poucos meses"}],
  "gestacao": "Não aplicável — indicação restrita a sintomas vasomotores da menopausa, condição que ocorre fora do período reprodutivo/gestacional.",
  "gestacaoCategoria": "N/A",
  "lactacao": "Não aplicável à indicação (menopausa).",
  "lactacaoCategoria": "N/A",
  "pediatria": "Não aplicável — indicação restrita à menopausa.",
  "geriatria": "Indicação típica dessa faixa etária (perimenopausa/pós-menopausa); sem ajuste específico além do monitoramento hepático.",
  "renal": "Sem ajuste em insuficiência renal leve a moderada; dados limitados em insuficiência renal grave.",
  "hepatica": "Contraindicado em insuficiência hepática grave; monitorar enzimas hepáticas em uso com insuficiência leve a moderada.",
  "tipoReceituario": "Receita Simples (venda sob prescrição médica)",
  "dispensacao": {"controleEspecial": False, "retencaoReceita": False, "condicoes": "Sem registro ANVISA confirmado até a data desta ficha — verificar situação regulatória antes de orientar dispensação."},
  "referencias": ["FDA. Lynkuet (elinzanetant) Prescribing Information, 2025.","Lederman S et al. Elinzanetant for Vasomotor Symptoms of Menopause (OASIS trials). JAMA. 2024.","Sociedade Brasileira de Endocrinologia e Metabologia / Febrasgo — Diretrizes de Climatério."],
  "ultimaAtualizacao": "30/10/2026"
}
print("defined: elinzanetanto")
print("TOTAL NOVOS:", len(NOVOS))

# ---------- Mapeamento id -> (grupo_id, subclasse_id) ----------
MAPA_SUBCLASSE = {
  "resmetirom": ("grp-a", "a5b"),
  "lenacapavir": ("grp-j", "j5c9"),
  "zuranolona": ("grp-n", "n6a9"),
  "gepotidacina": ("grp-j", "j1x9"),
  "sotagliflozina": ("grp-a", "a10p1"),
  "daridorexanto": ("grp-n", "n5b1"),
  "aprocitentanto": ("grp-c", "c2a2"),
  "durlobactam-sulbactam": ("grp-j", "j1p9"),
  "vadadustate": ("grp-b", "b3c"),
  "elinzanetanto": ("grp-g", "g3x"),
}
assert set(MAPA_SUBCLASSE.keys()) == set(NOVOS.keys()), "mapa de subclasses incompleto/divergente"

# ---------- Validador estrutural ----------
def validar_ficha(id_, m):
    erros = []
    campos_obrigatorios = ["nomeGenerico","classeTerapeutica","classes","nomesComerciais",
        "mecanismoAcao","farmacocinetica","indicacoes","contraindicacoes","precaucoes",
        "posologia","apresentacoes","viasAdministracao","interacoes","interacoesAlimentares",
        "reacoesAdversas","alertasFarmaceuticos","orientacoesPaciente","monitoramento",
        "gestacao","gestacaoCategoria","lactacao","lactacaoCategoria","pediatria","geriatria",
        "renal","hepatica","tipoReceituario","dispensacao","referencias","ultimaAtualizacao"]
    for c in campos_obrigatorios:
        if c not in m:
            erros.append(f"{id_}: campo ausente '{c}'")
        elif m[c] in (None, "", [], {}):
            erros.append(f"{id_}: campo vazio '{c}'")

    if not isinstance(m.get("viasAdministracao"), list):
        erros.append(f"{id_}: viasAdministracao deve ser array")
    if not isinstance(m.get("apresentacoes"), list):
        erros.append(f"{id_}: apresentacoes deve ser array")
    else:
        for ap in m["apresentacoes"]:
            if "forma" not in ap or "concentracoes" not in ap:
                erros.append(f"{id_}: apresentacao malformada {ap}")

    inter = m.get("interacoes", {})
    for k in ["graves","moderadas","menores"]:
        if k not in inter or not isinstance(inter[k], list):
            erros.append(f"{id_}: interacoes.{k} ausente/invalido")
        else:
            for item in inter[k]:
                for campo in ["par","mecanismo","conduta"]:
                    if campo not in item or not item[campo]:
                        erros.append(f"{id_}: interacoes.{k} item sem '{campo}'")

    ra = m.get("reacoesAdversas", {})
    for k in ["muitoComuns","comuns","incomuns","raras","graves"]:
        if k not in ra or not isinstance(ra[k], list):
            erros.append(f"{id_}: reacoesAdversas.{k} ausente/invalido")

    op = m.get("orientacoesPaciente", {})
    chaves_op = {"comoTomar","esquecimento","dirigir","alcool","alimentos","sinaisAlerta"}
    if set(op.keys()) != chaves_op:
        erros.append(f"{id_}: orientacoesPaciente chaves incorretas: {set(op.keys())}")

    monit = m.get("monitoramento", [])
    if not isinstance(monit, list) or not monit:
        erros.append(f"{id_}: monitoramento deve ser array nao vazio")
    else:
        for item in monit:
            if "parametro" not in item or "quando" not in item:
                erros.append(f"{id_}: monitoramento item malformado {item}")

    disp = m.get("dispensacao", {})
    for k in ["controleEspecial","retencaoReceita","condicoes"]:
        if k not in disp:
            erros.append(f"{id_}: dispensacao.{k} ausente")

    mec = m.get("mecanismoAcao", "")
    n_palavras = len(mec.split())
    if n_palavras > 55:
        erros.append(f"{id_}: mecanismoAcao com {n_palavras} palavras (verificar concisao)")

    cats_validas_gest = {"A","B","C","D","X","N/A"}
    if m.get("gestacaoCategoria") not in cats_validas_gest:
        erros.append(f"{id_}: gestacaoCategoria invalida: {m.get('gestacaoCategoria')}")
    cats_validas_lact = {"L1","L2","L3","L4","L5","N/A"}
    if m.get("lactacaoCategoria") not in cats_validas_lact:
        erros.append(f"{id_}: lactacaoCategoria invalida: {m.get('lactacaoCategoria')}")

    return erros

todos_erros = []
for id_, m in NOVOS.items():
    todos_erros.extend(validar_ficha(id_, m))

if todos_erros:
    print("ERROS DE VALIDACAO:")
    for e in todos_erros:
        print(" -", e)
    sys.exit(1)
else:
    print(f"Validacao OK: {len(NOVOS)} fichas, todas conformes ao padrao.")

# ---------- Carregar data.js ----------
print("Carregando data.js...")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    content = f.read()

def extrair_bloco(content, marcador, abre, fecha):
    start = content.index(marcador)
    start = content.index(abre, start)
    depth = 0
    i = start
    in_str = False
    esc = False
    while True:
        c = content[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == abre:
                depth += 1
            elif c == fecha:
                depth -= 1
                if depth == 0:
                    return start, i+1
        i += 1

g_start, g_end = extrair_bloco(content, "const GRUPOS", "[", "]")
grupos_json = content[g_start:g_end]
grupos = json.loads(grupos_json)

m_start, m_end = extrair_bloco(content, "const MEDICAMENTOS", "{", "}")
meds_json = content[m_start:m_end]
meds = json.loads(meds_json)

print(f"GRUPOS: {len(grupos)} grupos | MEDICAMENTOS: {len(meds)} fichas (antes)")

# ---------- Checagem de colisao ----------
colisoes = [id_ for id_ in NOVOS if id_ in meds]
if colisoes:
    print("ERRO: IDs ja existentes no catalogo:", colisoes)
    sys.exit(1)

# ---------- Merge seguro (Object.assign equivalente: dict.update, nunca substituicao total) ----------
meds.update(NOVOS)

# ---------- Insercao nos subclasses corretos de GRUPOS ----------
grupos_por_id = {g["id"]: g for g in grupos}
inseridos = []
for novo_id, (grp_id, sub_id) in MAPA_SUBCLASSE.items():
    grupo = grupos_por_id.get(grp_id)
    if grupo is None:
        print(f"ERRO: grupo {grp_id} nao encontrado para {novo_id}")
        sys.exit(1)
    subclasse = next((sc for sc in grupo["subclasses"] if sc["id"] == sub_id), None)
    if subclasse is None:
        print(f"ERRO: subclasse {sub_id} nao encontrada em {grp_id} para {novo_id}")
        sys.exit(1)
    if novo_id in subclasse["medicamentos"]:
        print(f"ERRO: {novo_id} ja presente em {sub_id} (duplicado)")
        sys.exit(1)
    subclasse["medicamentos"].append(novo_id)
    inseridos.append((novo_id, grp_id, sub_id))

print(f"MEDICAMENTOS apos merge: {len(meds)} fichas (+{len(NOVOS)})")
for novo_id, grp_id, sub_id in inseridos:
    print(f"  + {novo_id} -> {grp_id}/{sub_id}")

# ---------- Validacao pos-merge: nenhum id de GRUPOS orfao, nenhum medicamento sem grupo ----------
todos_ids_em_grupos = set()
for g in grupos:
    for sc in g["subclasses"]:
        for mid in sc["medicamentos"]:
            todos_ids_em_grupos.add(mid)

orfaos_grupos = todos_ids_em_grupos - set(meds.keys())
if orfaos_grupos:
    print("ERRO: ids em GRUPOS sem ficha correspondente em MEDICAMENTOS:", orfaos_grupos)
    sys.exit(1)

# ---------- Re-serializacao (mesmo estilo compacto do arquivo original) ----------
novo_grupos_json = json.dumps(grupos, ensure_ascii=False, separators=(",", ":"))
novo_meds_json = json.dumps(meds, ensure_ascii=False, separators=(",", ":"))

novo_content = (
    content[:g_start] + novo_grupos_json + content[g_end:m_start]
    + novo_meds_json + content[m_end:]
)

with open(DATA_PATH, "w", encoding="utf-8") as f:
    f.write(novo_content)

print("data.js atualizado com sucesso.")
print("Novo tamanho do arquivo:", len(novo_content), "bytes")
