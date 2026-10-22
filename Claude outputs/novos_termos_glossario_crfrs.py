#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona 60 novos termos ao dicionario.json do FarmaPrática, extraídos e
reelaborados a partir do "Glossário técnico-normativo relacionado ao
exercício profissional farmacêutico" (CRF/RS, elaborado entre fev/2020 e
set/2022, atualizado em 03/11/2022), que compila definições das Resoluções
vigentes do Conselho Federal de Farmácia (CFF).

Cada definição foi redigida de próprio punho (não copiada literalmente do
PDF), a partir do conteúdo normativo das Resoluções CFF citadas, seguindo o
schema e o estilo já usados em todo o banco. Roda diretamente no arquivo
real do usuário.
"""
import json
import sys

NOVOS_TERMOS = [
    # ============ LEGISLAÇÃO (8) ============
    {
        "id": "ato-farmaceutico", "termo": "Ato Farmacêutico", "categoria": "legislacao",
        "sinonimos": [],
        "definicao": "Ato privativo do farmacêutico, decorrente dos conhecimentos técnico-científicos adquiridos em sua formação acadêmica, que abrange todas as atividades de natureza técnica, científica e social relacionadas ao medicamento e à atenção à saúde, sendo de sua exclusiva responsabilidade.",
        "explicacaoSimplificada": "É qualquer ação que só o farmacêutico, por sua formação, tem respaldo legal para realizar — da manipulação à dispensação, da análise clínica à orientação farmacêutica.",
        "aplicacaoPratica": "Fundamenta juridicamente a exigência de farmacêutico presente e responsável técnico em toda farmácia e drogaria, e delimita quais atividades podem (ou não) ser delegadas a um auxiliar ou atendente, mesmo sob supervisão.",
        "atencao": "A ausência do farmacêutico durante o horário de funcionamento do estabelecimento compromete a prática do ato farmacêutico e configura infração ética e sanitária, independentemente de o balconista estar tecnicamente capacitado.",
        "termosRelacionados": ["responsavel-tecnico", "farmaceutico-substituto"],
        "fontes": ["Resolução CFF nº 357/2001", "Glossário Técnico-Normativo CRF/RS"]
    },
    {
        "id": "direcao-tecnica", "termo": "Direção Técnica", "categoria": "legislacao",
        "sinonimos": [],
        "definicao": "Função exercida pelo farmacêutico responsável técnico que compreende a coordenação de todos os serviços farmacêuticos do estabelecimento, sendo o fator determinante do gerenciamento da disponibilização do medicamento com atenção ao paciente, à economia, à eficiência e à cooperação com a equipe de saúde.",
        "explicacaoSimplificada": "É a função de comandar tecnicamente a farmácia: organizar os serviços farmacêuticos para que funcionem bem, com segurança e qualidade.",
        "aplicacaoPratica": "A direção técnica é indelegável em seus aspectos de responsabilidade (ainda que tarefas operacionais possam ser delegadas), e sua ausência não planejada exige a atuação do farmacêutico substituto para que o estabelecimento continue funcionando regularmente.",
        "atencao": "A direção técnica não se confunde com a direção administrativa/comercial do estabelecimento — um farmacêutico pode ser diretor técnico sem ser sócio ou gestor financeiro, e vice-versa (quando o gestor não é farmacêutico, a direção técnica precisa de um farmacêutico formalmente designado).",
        "termosRelacionados": ["responsavel-tecnico", "farmaceutico-substituto"],
        "fontes": ["Resolução CFF nº 357/2001"]
    },
    {
        "id": "bacharel-farmacia", "termo": "Bacharel em Farmácia", "categoria": "legislacao",
        "sinonimos": [],
        "definicao": "Denominação do diplomado em curso superior de graduação em Farmácia, devidamente reconhecido pelo Ministério da Educação, condição prévia e necessária para o registro como farmacêutico no Conselho Regional de Farmácia e para o exercício legal da profissão.",
        "explicacaoSimplificada": "É quem concluiu a graduação em Farmácia — o título acadêmico que, após o registro no conselho profissional, habilita a pessoa a exercer como farmacêutico.",
        "aplicacaoPratica": "A conclusão do bacharelado não equivale, por si só, ao exercício profissional: o registro no CRF da jurisdição é etapa obrigatória e distinta, sem a qual o bacharel não pode assumir responsabilidade técnica nem praticar atos privativos da profissão.",
        "atencao": "Exercer qualquer atividade privativa de farmacêutico sem o registro ativo no CRF — mesmo sendo bacharel formado — configura exercício ilegal da profissão.",
        "termosRelacionados": ["responsavel-tecnico"],
        "fontes": ["Resolução CFF nº 638/2017"]
    },
    {
        "id": "codigo-etica-farmaceutica", "termo": "Código de Ética Farmacêutica", "categoria": "legislacao",
        "sinonimos": ["Código de Processo Ético"],
        "definicao": "Conjunto de normas que devem ser observadas pelos farmacêuticos e demais inscritos nos Conselhos Regionais de Farmácia no exercício do âmbito profissional, abrangendo as atividades de ensino, pesquisa e administração de serviços de saúde, com o objetivo de resguardar o zelo pela saúde da população e a dignidade da profissão.",
        "explicacaoSimplificada": "É o conjunto de regras de conduta que todo farmacêutico deve seguir, definindo o que é considerado uma prática profissional correta e o que é uma infração ética.",
        "aplicacaoPratica": "Fundamenta os processos ético-disciplinares conduzidos pelos CRFs e orienta decisões do dia a dia, como sigilo profissional, recusa a dispensar em situações de risco ao paciente e vedação à publicidade enganosa de serviços farmacêuticos.",
        "atencao": "Infração ao Código de Ética é apurada separadamente de eventuais infrações sanitárias: um mesmo fato pode gerar, ao mesmo tempo, processo ético no CRF e autuação sanitária pela vigilância sanitária, com consequências distintas.",
        "termosRelacionados": [],
        "fontes": ["Resolução CFF nº 724/2022"]
    },
    {
        "id": "farmaceutico-fiscal", "termo": "Farmacêutico Fiscal", "categoria": "legislacao",
        "sinonimos": [],
        "definicao": "Profissional farmacêutico concursado e nomeado pelo Conselho Regional de Farmácia, investido de poder de polícia e fé pública, responsável pela fiscalização das atividades farmacêuticas no âmbito do local de atuação em empresas ou estabelecimentos onde se faça necessária a presença de farmacêutico, podendo lavrar termos de inspeção, intimação, notificação e autos de infração.",
        "explicacaoSimplificada": "É o farmacêutico que trabalha para o conselho profissional fiscalizando se as farmácias e outros estabelecimentos estão cumprindo as normas da profissão.",
        "aplicacaoPratica": "Suas visitas de fiscalização avaliam itens como a presença efetiva do responsável técnico, a regularidade dos registros e a observância das Boas Práticas; discrepâncias podem gerar desde uma simples notificação até um auto de infração.",
        "atencao": "O farmacêutico fiscal do CRF atua sobre o exercício profissional e as condições técnicas do estabelecimento — não deve ser confundido com o fiscal sanitário (vinculado à vigilância sanitária), cuja competência e normas de referência são distintas, ainda que as fiscalizações possam ocorrer de forma complementar.",
        "termosRelacionados": ["auto-infracao-sanitaria", "responsavel-tecnico"],
        "fontes": ["Resolução CFF nº 700/2021"]
    },
    {
        "id": "estagio-obrigatorio", "termo": "Estágio Obrigatório (Curso de Farmácia)", "categoria": "legislacao",
        "sinonimos": ["Estágio curricular supervisionado"],
        "definicao": "Atividade definida como tal no projeto pedagógico do curso de Farmácia, cuja carga horária é requisito para aprovação e obtenção do diploma, desenvolvida no ambiente de trabalho sob acompanhamento efetivo de professor orientador e supervisor da parte concedente, com o objetivo de preparar o estudante para a prática profissional.",
        "explicacaoSimplificada": "É a parte prática obrigatória da faculdade de Farmácia, feita em farmácias, hospitais ou laboratórios de verdade, sempre supervisionada, e sem a qual o aluno não se forma.",
        "aplicacaoPratica": "O estágio obrigatório é formalizado por um Termo de Compromisso de Estágio entre estudante, instituição de ensino e unidade concedente, e deve ser distinguido do estágio não obrigatório (atividade opcional, que soma carga horária extra além da regular).",
        "atencao": "O estagiário atua sob supervisão direta e não pode assumir responsabilidade técnica nem praticar, isoladamente, atos privativos do farmacêutico — qualquer atividade do estágio deve ter o acompanhamento efetivo do profissional responsável.",
        "termosRelacionados": [],
        "fontes": ["Resolução CFF nº 634/2016"]
    },
    {
        "id": "titulo-especialista-farmaceutico", "termo": "Título de Especialista Farmacêutico", "categoria": "legislacao",
        "sinonimos": ["Especialidade farmacêutica (título profissional)"],
        "definicao": "Reconhecimento formal concedido pelo Conselho Federal de Farmácia ao farmacêutico que comprova capacitação em uma das linhas de atuação e especialidades reconhecidas pela profissão, obtido por título acadêmico (pós-graduação lato sensu averbada), concurso de título ou realização de cursos livres credenciados, conforme a modalidade.",
        "explicacaoSimplificada": "É o reconhecimento oficial de que o farmacêutico se especializou em determinada área, como Farmácia Clínica, Farmácia Hospitalar ou Análises Clínicas, seguindo regras definidas pelo CFF.",
        "aplicacaoPratica": "Determinadas atribuições clínicas mais complexas (ex.: prescrição farmacêutica em contextos específicos, responsabilidade técnica por serviços especializados como oncologia e radiofarmácia) exigem comprovação de capacitação específica, muitas vezes formalizada por esse título.",
        "atencao": "Nem toda linha de atuação reconhecida pelo CFF exige capacitação formal para ser exercida — algumas exigem apenas a formação de bacharel, enquanto outras (as chamadas especialidades) exigem comprovação específica de capacitação, conforme a Resolução CFF que rege cada área.",
        "termosRelacionados": [],
        "fontes": ["Resolução CFF nº 572/2013", "Resolução CFF nº 580/2013", "Resolução CFF nº 643/2017"]
    },
    {
        "id": "dispensa-obrigatoriedade-registro", "termo": "Dispensa de Obrigatoriedade de Registro", "categoria": "legislacao",
        "sinonimos": [],
        "definicao": "Ato fundamentado na legislação sanitária vigente pelo qual a Agência Nacional de Vigilância Sanitária desobriga determinados produtos — como alguns medicamentos manipulados, fitoterápicos tradicionais ou classes específicas de notificação simplificada — do registro sanitário que normalmente seria exigido para sua comercialização.",
        "explicacaoSimplificada": "É quando a Anvisa libera um tipo de produto de precisar passar pelo processo completo de registro antes de poder ser vendido, por já ter segurança reconhecida ou estar sob outro tipo de controle.",
        "aplicacaoPratica": "Produtos manipulados em farmácia magistral, por exemplo, não têm registro individual na Anvisa — sua segurança é garantida pelo cumprimento das Boas Práticas de Manipulação e pela responsabilidade técnica do farmacêutico, não por um registro de produto específico.",
        "atencao": "Dispensa de registro não significa ausência de controle sanitário: o estabelecimento que produz ou comercializa o produto dispensado de registro continua sujeito à licença de funcionamento, à fiscalização e às Boas Práticas aplicáveis.",
        "termosRelacionados": ["licenca-sanitaria", "boas-praticas-fabricacao"],
        "fontes": ["Resolução CFF nº 530/2010", "Glossário Técnico-Normativo CRF/RS"]
    },

    # ============ GESTÃO FARMACÊUTICA (8) ============
    {
        "id": "estabelecimento-farmaceutico", "termo": "Estabelecimento Farmacêutico", "categoria": "gestao-farmaceutica",
        "sinonimos": [],
        "definicao": "Unidade sustentável centrada no atendimento das necessidades de saúde do indivíduo, da família e da comunidade, por meio da prestação de serviços farmacêuticos e da provisão de medicamentos e outros produtos para a saúde, voltada à promoção e recuperação da saúde e à prevenção de doenças e de outros problemas de saúde.",
        "explicacaoSimplificada": "É o termo amplo e atual que a Resolução CFF usa para designar farmácias, drogarias e outras unidades onde o farmacêutico presta assistência — com ênfase no cuidado ao paciente, não só na venda de produtos.",
        "aplicacaoPratica": "Conceito-guarda-chuva que engloba farmácia comunitária, farmácia hospitalar, farmácia universitária, drogaria e outras modalidades, todas sujeitas a responsabilidade técnica farmacêutica e licenciamento sanitário.",
        "atencao": "A definição atual (Resolução CFF nº 586/2013 e nº 610/2015) desloca o foco do estabelecimento farmacêutico do produto para o cuidado em saúde — relevante para entender a evolução do papel do farmacêutico de dispensador para prestador de serviços clínicos.",
        "termosRelacionados": ["estabelecimento-saude", "responsavel-tecnico"],
        "fontes": ["Resolução CFF nº 586/2013", "Resolução CFF nº 610/2015"]
    },
    {
        "id": "farmacia-comunitaria", "termo": "Farmácia Comunitária", "categoria": "gestao-farmaceutica",
        "sinonimos": [],
        "definicao": "Estabelecimento de prestação de serviços farmacêuticos, de natureza estatal ou privada, dirigido por profissional farmacêutico, destinado a prestar assistência e atenção farmacêutica ao público, incluindo educação para a saúde individual e coletiva, onde se processa a manipulação ou a dispensação de medicamentos magistrais, oficinais ou industrializados, cosméticos e produtos para a saúde.",
        "explicacaoSimplificada": "É a farmácia do bairro, aberta ao público, que tanto manipula como dispensa medicamentos prontos e presta orientação de saúde.",
        "aplicacaoPratica": "Distingue-se formalmente da drogaria por poder manipular fórmulas magistrais e oficinais, além de dispensar produtos industrializados — a drogaria, por definição regulatória, só comercializa produtos em suas embalagens originais.",
        "atencao": "A distinção farmácia × drogaria tem implicações regulatórias concretas: apenas a farmácia (com estrutura e licença para manipulação) pode aviar receitas magistrais.",
        "termosRelacionados": ["estabelecimento-saude", "preparacao-magistral"],
        "fontes": ["Resolução CFF nº 465/2007"]
    },
    {
        "id": "farmacia-hospitalar", "termo": "Farmácia Hospitalar", "categoria": "gestao-farmaceutica",
        "sinonimos": [],
        "definicao": "Unidade clínico-assistencial, técnica e administrativa, dirigida exclusivamente por farmacêutico, onde se processam as atividades relacionadas à assistência farmacêutica, compondo a estrutura organizacional do hospital e integrada funcionalmente com as demais unidades administrativas e de atendimento ao paciente.",
        "explicacaoSimplificada": "É o setor do hospital responsável por todo o ciclo dos medicamentos usados pelos pacientes internados — seleção, aquisição, armazenamento, dispensação e acompanhamento farmacoterapêutico — sempre sob direção de um farmacêutico.",
        "aplicacaoPratica": "Em farmácia hospitalar, atividades como conciliação medicamentosa, revisão da farmacoterapia e participação em comissões (ex.: Comissão de Farmácia e Terapêutica) são rotineiras e de alto impacto na segurança do paciente internado.",
        "atencao": "A farmácia hospitalar é regulamentada de forma específica e distinta da farmácia comunitária, com atribuições próprias (ex.: nutrição parenteral, farmácia clínica em terapia intensiva, oncologia) que exigem capacitação adicional do farmacêutico.",
        "termosRelacionados": ["comissao-farmacia-terapeutica", "conciliacao-medicamentosa"],
        "fontes": ["Resolução CFF nº 730/2022"]
    },
    {
        "id": "farmacia-universitaria", "termo": "Farmácia Universitária", "categoria": "gestao-farmaceutica",
        "sinonimos": [],
        "definicao": "Laboratório didático-especializado de ensino, pesquisa e extensão, vinculado a instituição de ensino superior e devidamente inscrito no Conselho Regional de Farmácia, que visa à formação dos estudantes de Farmácia e à qualificação de farmacêuticos, prestando também serviços e produtos farmacêuticos à comunidade.",
        "explicacaoSimplificada": "É a farmácia-escola das universidades, onde estudantes aprendem na prática enquanto também atendem a população, sob supervisão de professores farmacêuticos.",
        "aplicacaoPratica": "Funciona como campo de estágio obrigatório e espaço de extensão universitária, muitas vezes oferecendo serviços gratuitos ou a baixo custo à comunidade, como aferição de pressão arterial e orientação farmacêutica.",
        "atencao": "Mesmo sendo um espaço de ensino, a farmácia universitária está sujeita às mesmas exigências de responsabilidade técnica e licenciamento sanitário de qualquer outro estabelecimento farmacêutico.",
        "termosRelacionados": ["estagio-obrigatorio"],
        "fontes": ["Resolução CFF nº 610/2015"]
    },
    {
        "id": "logistica-farmaceutica", "termo": "Logística Farmacêutica", "categoria": "gestao-farmaceutica",
        "sinonimos": [],
        "definicao": "Operação que requer altos índices de customizações operacionais, com particularidades técnicas e premissas de boas práticas de armazenagem, gestão de estoques e transportes durante toda a cadeia de valor a que os produtos farmacêuticos são submetidos, abrangendo recebimento, conferência, armazenagem, controle de estoque, separação, inspeção, expedição e gestão dos fluxos diretos e reversos.",
        "explicacaoSimplificada": "É toda a cadeia de movimentação de medicamentos e produtos farmacêuticos — do recebimento no armazém até a entrega final — organizada para garantir que o produto chegue íntegro, no prazo e com rastreabilidade.",
        "aplicacaoPratica": "Abrange desde o planejamento de compras (programação) até o transporte sob cadeia de frio de produtos termolábeis, sendo área de atuação farmacêutica reconhecida (linha de atuação Gestão, Resolução CFF 572/2013).",
        "atencao": "Toda etapa da logística farmacêutica — incluindo transporte terceirizado — requer controle técnico e sanitário; a responsabilidade pela integridade do produto não se transfere automaticamente ao transportador apenas por contrato comercial.",
        "termosRelacionados": ["cadeia-fria", "rastreabilidade"],
        "fontes": ["Resolução CFF nº 679/2020"]
    },
    {
        "id": "pessoal-chave", "termo": "Pessoal-Chave", "categoria": "gestao-farmaceutica",
        "sinonimos": [],
        "definicao": "Gestores definidos pela administração superior de indústrias farmacêuticas, envolvidos na fabricação, aprovação e liberação de medicamentos com poder de decisão — incluindo o farmacêutico responsável pela produção, pela garantia da qualidade, pelo controle de qualidade, pelo desenvolvimento de produtos, pelos assuntos regulatórios e o farmacêutico responsável técnico — cujos postos principais devem ser ocupados por pessoas que trabalhem em tempo integral e sejam independentes entre si.",
        "explicacaoSimplificada": "São os farmacêuticos com poder de decisão dentro de uma indústria farmacêutica, cada um responsável por uma área-chave (produção, qualidade, regulatório etc.), que precisam ser independentes uns dos outros para evitar conflito de interesse.",
        "aplicacaoPratica": "A separação entre o farmacêutico responsável pela produção e o responsável pela garantia/controle de qualidade é um princípio central de Boas Práticas de Fabricação: evita que quem produz também seja quem aprova a liberação do lote.",
        "atencao": "A responsabilidade dos integrantes do pessoal-chave não pode ser delegada, ainda que tarefas específicas possam ser distribuídas a outros profissionais sob sua supervisão.",
        "termosRelacionados": ["boas-praticas-fabricacao", "responsavel-tecnico"],
        "fontes": ["Resolução CFF nº 734/2022"]
    },
    {
        "id": "terceirizacao-servicos-farmaceuticos", "termo": "Terceirização de Serviços Farmacêuticos", "categoria": "gestao-farmaceutica",
        "sinonimos": [],
        "definicao": "Prestação de serviços por empresa contratada em atividades de produção, controle de qualidade, transporte, armazenamento e gestão de estoques de medicamentos, insumos farmacêuticos, produtos para a saúde, cosméticos, alimentos, saneantes e produtos biológicos, mediante contrato formal que preserva a responsabilidade técnica de cada etapa.",
        "explicacaoSimplificada": "É quando uma empresa contrata outra para realizar parte de suas atividades farmacêuticas, como o transporte ou o armazenamento de medicamentos, sem deixar de responder tecnicamente pelo que é terceirizado.",
        "aplicacaoPratica": "Mesmo terceirizando logística ou armazenagem, a empresa contratante continua corresponsável pela qualidade e pela rastreabilidade do produto — o contrato de terceirização deve prever claramente as responsabilidades técnicas de cada parte.",
        "atencao": "A terceirização de etapas críticas (como o transporte de produtos termolábeis) exige que a empresa contratada também cumpra as Boas Práticas e a cadeia de frio aplicáveis — falhas da terceirizada não eximem a contratante de responsabilidade perante a vigilância sanitária.",
        "termosRelacionados": ["cadeia-fria", "logistica-farmaceutica"],
        "fontes": ["Resolução CFF nº 679/2020"]
    },
    {
        "id": "auditoria-e-acreditacao", "termo": "Auditoria e Acreditação", "categoria": "gestao-farmaceutica",
        "sinonimos": ["Acreditação hospitalar"],
        "definicao": "Auditoria é o processo sistemático, documentado e independente para obter evidências e avaliá-las objetivamente, a fim de determinar a extensão na qual os critérios estabelecidos são atendidos; acreditação é o procedimento de avaliação integral da qualidade, voluntário e periódico, por meio do qual uma organização reconhece formalmente que um estabelecimento é competente para realizar tarefas específicas segundo padrões previamente definidos.",
        "explicacaoSimplificada": "Auditoria é a checagem sistemática de que um processo está sendo seguido corretamente; acreditação é o selo de qualidade concedido a um estabelecimento (como um hospital) que passa com sucesso por essa avaliação completa e voluntária.",
        "aplicacaoPratica": "Hospitais acreditados (ex.: pela ONA ou pela Joint Commission International) submetem seus serviços farmacêuticos a auditorias periódicas que avaliam desde a gestão de medicamentos de alta vigilância até a dupla checagem na dispensação.",
        "atencao": "Diferente da fiscalização sanitária (compulsória), a acreditação é um processo voluntário e confidencial — sua ausência não configura irregularidade sanitária, mas costuma ser exigida por operadoras de saúde e grandes contratantes como diferencial de qualidade.",
        "termosRelacionados": ["qualidade", "nao-conformidade"],
        "fontes": ["Resolução CFF nº 641/2017"]
    },

    # ============ FARMÁCIA CLÍNICA (12) ============
    {
        "id": "consulta-farmaceutica", "termo": "Consulta Farmacêutica", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Atendimento realizado pelo farmacêutico ao paciente, respeitando os princípios éticos e profissionais, com a finalidade de obter resultados adequados com a farmacoterapia, promover o uso racional de medicamentos e de outras tecnologias em saúde, promover, proteger e recuperar a saúde, e prevenir doenças e outros problemas de saúde.",
        "explicacaoSimplificada": "É o atendimento individual e estruturado que o farmacêutico faz com o paciente, dedicado especificamente a avaliar e acompanhar sua farmacoterapia — diferente de uma orientação rápida no balcão.",
        "aplicacaoPratica": "Costuma ocorrer em consultório farmacêutico, com anamnese, elaboração de plano de cuidado e registro em prontuário — é a base dos serviços clínicos remunerados que o farmacêutico pode oferecer fora da dispensação.",
        "atencao": "A consulta farmacêutica não substitui a consulta médica nem autoriza o farmacêutico a diagnosticar doenças fora do escopo de problemas de saúde autolimitados — seu foco é a farmacoterapia e o cuidado relacionado a medicamentos.",
        "termosRelacionados": ["atencao-farmaceutica", "plano-cuidado-farmaceutico", "consultorio-farmaceutico"],
        "fontes": ["Resolução CFF nº 585/2013", "Resolução CFF nº 700/2021"]
    },
    {
        "id": "consultorio-farmaceutico", "termo": "Consultório Farmacêutico", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Local de trabalho do farmacêutico destinado ao atendimento de pacientes, familiares e cuidadores, onde se realiza com privacidade a consulta farmacêutica, podendo funcionar de modo autônomo ou como dependência de hospitais, ambulatórios, farmácias comunitárias, unidades multiprofissionais de atenção à saúde e demais serviços de saúde.",
        "explicacaoSimplificada": "É o espaço reservado e privativo onde o farmacêutico atende o paciente individualmente, podendo ficar dentro de uma farmácia ou ser um local independente, só para esse fim.",
        "aplicacaoPratica": "Mesmo o consultório instalado dentro de uma farmácia comunitária precisa garantir privacidade (paredes, porta fechada), requisito indispensável para a realização de anamnese e consulta farmacêutica dignas desse nome.",
        "atencao": "O consultório farmacêutico autônomo (não vinculado a outro estabelecimento de saúde) tem registro e exigências próprias junto ao CRF, distintas das de uma farmácia comunitária comum.",
        "termosRelacionados": ["consulta-farmaceutica"],
        "fontes": ["Resolução CFF nº 585/2013", "Resolução CFF nº 720/2022"]
    },
    {
        "id": "cuidado-centrado-paciente", "termo": "Cuidado Centrado no Paciente", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Relação humanizada que envolve o respeito às crenças, expectativas, experiências, atitudes e preocupações do paciente ou cuidadores quanto às suas condições de saúde e ao uso de medicamentos, na qual farmacêutico e paciente compartilham a tomada de decisão e a responsabilidade pelos resultados em saúde alcançados.",
        "explicacaoSimplificada": "É a forma de cuidar que coloca a pessoa — suas crenças, preferências e contexto de vida — no centro da decisão, em vez de impor uma conduta técnica de cima para baixo.",
        "aplicacaoPratica": "Na prática, significa ajustar a orientação farmacêutica à realidade do paciente (ex.: simplificar o esquema posológico de alguém com baixa adesão, considerar restrições financeiras ao sugerir trocas terapêuticas) em vez de repetir instruções padronizadas.",
        "atencao": "Cuidado centrado no paciente não significa concordar com todas as suas escolhas sem questionamento — envolve dialogar e pactuar a conduta, mantendo o rigor técnico da orientação farmacêutica.",
        "termosRelacionados": ["consulta-farmaceutica", "plano-cuidado-farmaceutico"],
        "fontes": ["Resolução CFF nº 585/2013"]
    },
    {
        "id": "prescricao-farmaceutica", "termo": "Prescrição Farmacêutica", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Ato pelo qual o farmacêutico seleciona e documenta terapias farmacológicas e não farmacológicas, e outras intervenções relativas ao cuidado à saúde do paciente, visando à promoção, proteção e recuperação da saúde e à prevenção de doenças e de outros problemas de saúde, dentro do escopo legal de sua atuação.",
        "explicacaoSimplificada": "É quando o próprio farmacêutico — dentro dos limites que a lei permite, como no manejo de problemas de saúde autolimitados e na dispensação de medicamentos isentos de prescrição — define e registra formalmente a conduta terapêutica.",
        "aplicacaoPratica": "Difere da prescrição médica em escopo: o farmacêutico prescreve predominantemente dentro de situações autolimitadas, medidas não farmacológicas e medicamentos cuja dispensação não exige receita, sempre documentando a conduta.",
        "atencao": "A prescrição farmacêutica não substitui a prescrição médica em doenças crônicas, graves ou que exijam diagnóstico diferencial — seu uso incorreto fora do escopo autorizado configura exercício indevido da medicina.",
        "termosRelacionados": ["problema-saude-autolimitado", "intervencao-farmaceutica"],
        "fontes": ["Resolução CFF nº 585/2013", "Resolução CFF nº 586/2013", "Resolução CFF nº 661/2018"]
    },
    {
        "id": "evolucao-farmaceutica", "termo": "Evolução Farmacêutica", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Registros efetuados pelo farmacêutico no prontuário do paciente, com a finalidade de documentar o cuidado em saúde prestado, propiciando a comunicação entre os diversos membros da equipe de saúde ao longo do acompanhamento.",
        "explicacaoSimplificada": "É a anotação, no prontuário, de como o paciente está evoluindo ao longo do acompanhamento farmacêutico — o que mudou, o que melhorou, o que ainda precisa de atenção.",
        "aplicacaoPratica": "Documentar a evolução farmacêutica de forma estruturada (ex.: metodologia SOAP) é o que dá continuidade ao cuidado entre consultas e permite que outros profissionais da equipe entendam as intervenções já realizadas.",
        "atencao": "Registro omisso ou genérico (apenas 'sem queixas', sem detalhamento) enfraquece a defesa do farmacêutico em caso de questionamento ético ou legal sobre a qualidade do acompanhamento prestado.",
        "termosRelacionados": ["prontuario-paciente", "plano-cuidado-farmaceutico"],
        "fontes": ["Resolução CFF nº 585/2013", "Resolução CFF nº 675/2019"]
    },
    {
        "id": "prontuario-paciente", "termo": "Prontuário do Paciente", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Documento único, constituído de um conjunto de informações, sinais e imagens registrados, gerados a partir de fatos, acontecimentos e situações sobre a saúde do paciente e a assistência a ele prestada, de caráter legal, sigiloso e científico, que possibilita a comunicação entre membros da equipe multiprofissional e a continuidade da assistência prestada.",
        "explicacaoSimplificada": "É o 'histórico completo' de saúde do paciente, reunindo tudo o que os profissionais registram sobre ele — essencial para que o cuidado tenha continuidade, mesmo entre diferentes atendimentos e profissionais.",
        "aplicacaoPratica": "O registro farmacêutico em prontuário (anamnese, plano de cuidado, evolução) integra o prontuário geral do paciente quando o farmacêutico atua em equipe multiprofissional, como em farmácia hospitalar ou unidade de saúde.",
        "atencao": "O prontuário tem valor legal: registros incompletos, rasurados sem ressalva ou alterados após o fato configuram risco ético e jurídico para o profissional, independentemente da categoria que o preencheu.",
        "termosRelacionados": ["evolucao-farmaceutica"],
        "fontes": ["Resolução CFF nº 555/2011", "Resolução CFF nº 727/2022"]
    },
    {
        "id": "telefarmacia", "termo": "Telefarmácia", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Exercício da farmácia clínica mediado por Tecnologia da Informação e de Comunicação (TIC), de forma remota, em tempo real (síncrona) ou assíncrona, para fins de promoção, proteção e monitoramento e recuperação da saúde, prevenção de doenças e de outros problemas de saúde, bem como para a resolução de problemas da farmacoterapia e para o uso racional de medicamentos.",
        "explicacaoSimplificada": "É a prestação de serviços farmacêuticos clínicos à distância, por videochamada, telefone ou outro meio digital, em vez de presencialmente.",
        "aplicacaoPratica": "Permite acompanhamento farmacoterapêutico de pacientes que moram longe ou têm dificuldade de locomoção, mas exige infraestrutura tecnológica adequada e consentimento do paciente, respeitando as mesmas garantias éticas e de sigilo do atendimento presencial.",
        "atencao": "Nem todo serviço farmacêutico pode ser prestado por telefarmácia — avaliações que dependam de exame físico direto ou aferições presenciais continuam exigindo atendimento in loco.",
        "termosRelacionados": ["teleconsulta-farmaceutica", "consulta-farmaceutica"],
        "fontes": ["Resolução CFF nº 727/2022"]
    },
    {
        "id": "teleconsulta-farmaceutica", "termo": "Teleconsulta Farmacêutica", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Consulta realizada pelo farmacêutico, de forma não presencial e síncrona, mediada por Tecnologia da Informação e Comunicação, que permite a interação em tempo real com o paciente, seu responsável legal e acompanhantes, quando necessário, presentes em diferentes ambientes.",
        "explicacaoSimplificada": "É a consulta farmacêutica feita ao vivo por chamada de vídeo ou voz, com o paciente em um local e o farmacêutico em outro.",
        "aplicacaoPratica": "Modalidade específica de telefarmácia (que também engloba comunicação assíncrona); a teleconsulta exige interação em tempo real, o que a diferencia, por exemplo, do telemonitoramento assíncrono via aplicativo.",
        "atencao": "A qualidade da conexão e a garantia de sigilo da chamada (plataformas seguras, ambiente privado em ambos os lados) são requisitos técnicos e éticos para a validade da teleconsulta.",
        "termosRelacionados": ["telefarmacia"],
        "fontes": ["Resolução CFF nº 727/2022"]
    },
    {
        "id": "paciente-critico-grave", "termo": "Paciente Crítico e Paciente Grave", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Paciente crítico é aquele que necessita de cuidado farmacêutico contínuo, especializado, integral e humanizado; paciente grave é aquele com comprometimento de um ou mais dos principais sistemas fisiológicos, com perda de sua autorregulação, necessitando de assistência contínua.",
        "explicacaoSimplificada": "São classificações usadas para pacientes que precisam de atenção farmacêutica intensa e constante — o paciente grave já tem algum sistema do corpo funcionando mal, e o crítico precisa de cuidado farmacêutico especializado contínuo.",
        "aplicacaoPratica": "Orientam a priorização de recursos do farmacêutico clínico em unidades de terapia intensiva: pacientes graves e críticos costumam exigir conciliação medicamentosa mais frequente, ajustes de dose por disfunção orgânica e vigilância redobrada a interações.",
        "atencao": "O manejo farmacoterapêutico de pacientes críticos envolve risco elevado de erro de medicação (múltiplas infusões simultâneas, ajustes renais/hepáticos frequentes), justificando a presença do farmacêutico clínico intensivista na equipe.",
        "termosRelacionados": ["farmaceutico-fiscal"],
        "fontes": ["Resolução CFF nº 675/2019"]
    },
    {
        "id": "cuidados-paliativos", "termo": "Cuidados Paliativos", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Assistência ativa e integral a pacientes cuja doença não mais responde ao tratamento curativo, visando em especial a garantia da melhor qualidade de vida possível, tanto para o paciente como para seus familiares.",
        "explicacaoSimplificada": "É o cuidado voltado a aliviar o sofrimento e manter a qualidade de vida de pacientes com doenças que já não têm perspectiva de cura, em vez de tentar curá-los.",
        "aplicacaoPratica": "O farmacêutico em cuidados paliativos atua fortemente no manejo da dor (incluindo opioides), em ajustes de via de administração quando a via oral se torna inviável, e na desprescrição de medicamentos que deixaram de trazer benefício ao paciente.",
        "atencao": "Em cuidados paliativos, o uso de opioides fortes é frequentemente necessário e tecnicamente adequado — o medo infundado da dependência (a chamada opiofobia) não deve ser motivo para subtratar a dor do paciente nessa fase.",
        "termosRelacionados": ["paciente-critico-grave"],
        "fontes": ["Resolução CFF nº 700/2021", "Resolução CFF nº 720/2022"]
    },
    {
        "id": "visita-multiprofissional", "termo": "Visita Multiprofissional", "categoria": "farmacia-clinica",
        "sinonimos": [],
        "definicao": "Visita realizada à beira do leito para discutir os casos de cada paciente, de forma que todos os membros da equipe de saúde contribuam para o atendimento de maneira coordenada e integrada, centrando suas ações nas necessidades em saúde dos pacientes.",
        "explicacaoSimplificada": "É quando médicos, enfermeiros, farmacêuticos e outros profissionais passam juntos de leito em leito discutindo cada caso, em vez de avaliar o paciente separadamente cada um por sua conta.",
        "aplicacaoPratica": "Na visita multiprofissional, o farmacêutico clínico contribui com informações sobre interações medicamentosas, ajustes de dose, custo-efetividade de alternativas terapêuticas e riscos identificados na farmacoterapia do paciente, em tempo real para a equipe.",
        "atencao": "A participação ativa do farmacêutico na visita multiprofissional (e não apenas sua presença passiva) é o que efetivamente reduz eventos adversos a medicamentos em ambiente hospitalar, segundo a literatura da área.",
        "termosRelacionados": ["evento-adverso", "conciliacao-medicamentosa"],
        "fontes": ["Resolução CFF nº 675/2019"]
    },
    {
        "id": "problema-saude-autolimitado", "termo": "Problema de Saúde Autolimitado", "categoria": "farmacia-clinica",
        "sinonimos": ["Manejo de problemas de saúde autolimitados"],
        "definicao": "Enfermidade aguda de baixa gravidade, de breve período de latência, que desencadeia uma reação orgânica que tende a cursar sem dano para o paciente e que pode ser tratada de forma eficaz e segura com medicamentos e outros produtos com finalidade terapêutica cuja dispensação não exija prescrição médica, incluindo medicamentos industrializados e preparações magistrais, plantas medicinais ou medidas não farmacológicas.",
        "explicacaoSimplificada": "São queixas leves e passageiras — como uma dor de cabeça ocasional ou uma pequena irritação na pele — que o farmacêutico pode avaliar e manejar diretamente, sem a necessidade de encaminhar ao médico.",
        "aplicacaoPratica": "O serviço de manejo de problemas de saúde autolimitados é formalmente reconhecido pelo CFF (Resolução nº 585/2013) e estrutura a atuação do farmacêutico na automedicação responsável, sempre com critério para identificar sinais de alarme que exijam encaminhamento médico.",
        "atencao": "O farmacêutico deve estar atento aos sinais de alarme (febre persistente, piora progressiva, sintomas atípicos para a idade ou comorbidades) que indicam que o quadro deixou de ser autolimitado e exige encaminhamento médico imediato.",
        "termosRelacionados": ["automedicacao", "prescricao-farmaceutica"],
        "fontes": ["Resolução CFF nº 585/2013", "Resolução CFF nº 610/2015"]
    },

    # ============ FARMACOTÉCNICA (9) ============
    {
        "id": "preparacao-magistral", "termo": "Preparação Magistral", "categoria": "farmacotecnica",
        "sinonimos": ["Fórmula magistral (produto)"],
        "definicao": "Medicamento preparado na farmácia a partir de uma prescrição de profissional habilitado, destinado a um paciente individualizado, que estabelece em detalhes sua composição, forma farmacêutica, posologia e modo de usar.",
        "explicacaoSimplificada": "É o medicamento 'sob medida', feito especialmente para um único paciente, seguindo exatamente o que o prescritor pediu na receita — diferente de um medicamento industrializado, que é produzido em massa e igual para todos.",
        "aplicacaoPratica": "Permite ajustar dose, forma farmacêutica (ex.: cápsula para quem não engole comprimido) ou combinar substâncias de forma individualizada, quando não há apresentação industrializada adequada ao paciente.",
        "atencao": "A preparação magistral não passa por registro sanitário individual — sua segurança depende inteiramente do cumprimento das Boas Práticas de Manipulação e da idoneidade técnica do farmacêutico responsável.",
        "termosRelacionados": ["formula-magistral", "processo-manipulacao-magistral", "bpfm"],
        "fontes": ["Resolução CFF nº 661/2018"]
    },
    {
        "id": "formula-magistral", "termo": "Fórmula Magistral", "categoria": "farmacotecnica",
        "sinonimos": [],
        "definicao": "Fórmula constante de uma prescrição que estabelece a composição, a forma farmacêutica e a posologia de um medicamento a ser preparado individualmente na farmácia para um paciente específico, por profissional habilitado ou a partir de conteúdo anódino.",
        "explicacaoSimplificada": "É a 'receita' em si — a combinação de ingredientes e instruções que o prescritor define para aquele medicamento sob medida, antes mesmo de ele ser efetivamente manipulado.",
        "aplicacaoPratica": "Distingue-se da fórmula oficinal: a magistral é específica para um paciente determinado (prescrição individual), enquanto a oficinal segue uma receita padronizada presente em compêndios oficiais, podendo ser preparada antecipadamente para estoque da farmácia.",
        "atencao": "Toda fórmula magistral deve ser avaliada tecnicamente pelo farmacêutico antes do aviamento — incompatibilidades entre os componentes prescritos, doses inadequadas ou vias de administração incoerentes devem ser identificadas e esclarecidas com o prescritor antes da manipulação.",
        "termosRelacionados": ["preparacao-magistral", "formula-padrao-mestra"],
        "fontes": ["Resolução CFF nº 357/2011", "Resolução CFF nº 467/2007"]
    },
    {
        "id": "formula-padrao-mestra", "termo": "Fórmula Padrão (Fórmula Mestra)", "categoria": "farmacotecnica",
        "sinonimos": ["Fórmula-padrão"],
        "definicao": "Documento ou grupo de documentos que especificam as matérias-primas e os materiais de embalagem com suas respectivas quantidades, juntamente com a descrição dos procedimentos e precauções necessárias para a produção de uma determinada quantidade de produto, incluindo instruções sobre os controles em processo.",
        "explicacaoSimplificada": "É o 'documento-receita' interno da farmácia ou indústria que descreve, passo a passo, como produzir corretamente um determinado produto ou lote — a referência técnica que orienta a manipulação, distinta da receita individual do paciente.",
        "aplicacaoPratica": "Em uma farmácia magistral, a fórmula padrão (ou fórmula mestra) de um produto manipulado frequentemente garante que diferentes manipuladores produzam o mesmo resultado, de forma reprodutível e documentada.",
        "atencao": "A fórmula padrão não substitui a avaliação individual da prescrição médica pelo farmacêutico — ela padroniza o processo de manipulação, mas cada prescrição magistral ainda precisa ser avaliada antes do aviamento.",
        "termosRelacionados": ["formula-magistral", "lote-ou-partida"],
        "fontes": ["Resolução CFF nº 406/2003", "Resolução CFF nº 467/2007"]
    },
    {
        "id": "processo-manipulacao-magistral", "termo": "Processo de Manipulação Magistral", "categoria": "farmacotecnica",
        "sinonimos": [],
        "definicao": "Conjunto de operações que transformam os insumos farmacêuticos em um medicamento ou produto farmacêutico, resultantes de uma prescrição de profissional habilitado ou de solicitação de usuário identificado, compreendendo a avaliação da prescrição, a aquisição e controle de qualidade de insumos, as operações farmacotécnicas, o registro de dados para rastreabilidade e a dispensação com orientação ao usuário.",
        "explicacaoSimplificada": "É toda a sequência de etapas, da avaliação da receita até a entrega do medicamento pronto ao paciente, que transforma matérias-primas em um medicamento manipulado seguro e rastreável.",
        "aplicacaoPratica": "Cada etapa do processo (avaliação, aquisição, manipulação, registro, dispensação) gera documentação que compõe o histórico do lote manipulado, essencial para investigar qualquer problema de qualidade identificado posteriormente.",
        "atencao": "Pular ou simplificar qualquer etapa do processo — como a avaliação farmacêutica da prescrição antes de manipular — compromete a rastreabilidade e a segurança de todo o lote produzido.",
        "termosRelacionados": ["preparacao-magistral", "bpfm"],
        "fontes": ["Resolução CFF nº 467/2007"]
    },
    {
        "id": "sala-manipulacao", "termo": "Sala de Manipulação", "categoria": "farmacotecnica",
        "sinonimos": [],
        "definicao": "Ambiente destinado especificamente à manipulação de produtos farmacêuticos, com condições de infraestrutura, limpeza e controle ambiental compatíveis com a natureza dos produtos preparados, podendo haver salas específicas (ex.: sala de manipulação homeopática) quando a natureza do preparo exigir segregação.",
        "explicacaoSimplificada": "É o espaço físico dedicado exclusivamente ao preparo dos medicamentos manipulados, separado das áreas de atendimento ao público, para evitar contaminação e garantir qualidade.",
        "aplicacaoPratica": "Medicamentos de natureza distinta (ex.: homeopáticos versus alopáticos, ou produtos com potencial alergênico como penicilínicos) costumam exigir salas segregadas, para evitar contaminação cruzada entre preparações incompatíveis.",
        "atencao": "A sala de paramentação — onde o manipulador coloca os equipamentos de proteção antes de entrar na sala de manipulação — funciona como barreira física de controle de acesso, e sua ausência ou mau uso compromete a qualidade do ambiente controlado.",
        "termosRelacionados": ["preparacao-magistral"],
        "fontes": ["Resolução CFF nº 467/2007"]
    },
    {
        "id": "base-galenica", "termo": "Base Galênica", "categoria": "farmacotecnica",
        "sinonimos": [],
        "definicao": "Preparação composta de uma ou mais matérias-primas, com fórmula definida, destinada a ser utilizada como veículo ou excipiente de preparações farmacêuticas.",
        "explicacaoSimplificada": "É a 'massa base' — como um creme ou gel neutro — usada para incorporar o princípio ativo em preparações manipuladas, sem efeito terapêutico próprio relevante.",
        "aplicacaoPratica": "A escolha da base galênica (ex.: base lavável versus oleosa, ou gel versus creme) influencia diretamente a absorção, a estabilidade e a aceitabilidade de um produto tópico manipulado.",
        "atencao": "Nem toda base galênica é compatível com todo princípio ativo — incompatibilidades físico-químicas entre o ativo prescrito e a base escolhida podem comprometer a estabilidade ou a eficácia do produto final.",
        "termosRelacionados": ["forma-farmaceutica", "preparacao-magistral"],
        "fontes": ["Resolução CFF nº 467/2007"]
    },
    {
        "id": "material-embalagem", "termo": "Material de Embalagem (Primária e Secundária)", "categoria": "farmacotecnica",
        "sinonimos": ["Embalagem primária", "Embalagem secundária"],
        "definicao": "Qualquer material empregado na embalagem de medicamentos, classificado como primário quando está em contato direto com o produto (ex.: frasco, blíster) ou secundário quando se destina a conter a(s) embalagem(ns) primária(s) sem contato direto com o produto (ex.: cartucho, caixa).",
        "explicacaoSimplificada": "É tudo o que envolve e protege o medicamento: a embalagem primária toca o produto diretamente, e a secundária é a caixa ou cartucho que guarda a embalagem primária.",
        "aplicacaoPratica": "A integridade da embalagem primária é crítica para a estabilidade do medicamento (ex.: blíster danificado pode comprometer a proteção contra umidade) — danos só na embalagem secundária (caixa amassada) geralmente não comprometem o produto em si, mas podem gerar dúvida na dispensação.",
        "atencao": "Produtos estéreis têm regras específicas: o envase estéril, quando aplicável, não é considerado parte do 'processo de embalagem' para fins regulatórios — distinção relevante em auditorias de Boas Práticas de Fabricação.",
        "termosRelacionados": ["rotulo", "lote-ou-partida"],
        "fontes": ["Resolução CFF nº 734/2022"]
    },
    {
        "id": "materia-prima-farmaceutica", "termo": "Matéria-Prima", "categoria": "farmacotecnica",
        "sinonimos": [],
        "definicao": "Substância ativa ou inativa, com especificação definida, utilizada na produção de medicamentos e demais produtos, tanto a que permanece inalterada quanto a passível de modificações durante o processo de fabricação ou manipulação.",
        "explicacaoSimplificada": "É qualquer substância usada para fabricar ou manipular um medicamento, seja o princípio ativo em si ou um ingrediente auxiliar (excipiente).",
        "aplicacaoPratica": "Toda matéria-prima recebida por uma farmácia de manipulação ou indústria deve ser submetida a controle de qualidade e quarentena antes da liberação para uso — não basta o laudo do fornecedor, a legislação exige verificação própria em diversos casos.",
        "atencao": "Matéria-prima com laudo analítico vencido ou sem rastreabilidade de origem não deve ser utilizada, mesmo que aparentemente dentro do prazo de validade declarado pelo fornecedor.",
        "termosRelacionados": ["principio-ativo", "especificacao-farmacopeica"],
        "fontes": ["Resolução CFF nº 467/2007", "Resolução CFF nº 734/2022"]
    },
    {
        "id": "lote-ou-partida", "termo": "Lote ou Partida", "categoria": "farmacotecnica",
        "sinonimos": [],
        "definicao": "Quantidade definida de matéria-prima, material de embalagem ou produto terminado, obtida em um único processo ou série de processos, cuja característica essencial é a homogeneidade.",
        "explicacaoSimplificada": "É o 'grupo' de produtos fabricados de uma só vez, nas mesmas condições — por isso, se há algum problema, ele costuma afetar o lote inteiro, não unidades isoladas.",
        "aplicacaoPratica": "O número do lote, impresso na embalagem, é o que permite rastrear toda a história de um medicamento (matérias-primas usadas, data de fabricação, resultados de controle de qualidade) em caso de recall ou investigação de desvio.",
        "atencao": "Em recolhimento de produtos (recall), a identificação precisa do número do lote afetado é o que define exatamente quais unidades devem ser retiradas do mercado — divulgar o recall sem esse dado gera confusão desnecessária para o paciente.",
        "termosRelacionados": ["material-embalagem", "rotulo"],
        "fontes": ["Resolução CFF nº 467/2007", "Resolução CFF nº 734/2022"]
    },

    # ============ CONTROLE DE QUALIDADE (9) ============
    {
        "id": "certificado-analise", "termo": "Certificado de Análise", "categoria": "controle-qualidade",
        "sinonimos": ["Laudo de análise"],
        "definicao": "Documento que fornece um resumo dos resultados dos testes realizados em amostras de produtos ou de materiais, juntamente com a avaliação de sua conformidade com a especificação declarada, emitido para subsidiar a liberação do lote para comercialização ou uso.",
        "explicacaoSimplificada": "É o 'boletim de notas' de um lote de medicamento ou matéria-prima: mostra os resultados de cada teste de qualidade realizado e se o produto passou ou não nos critérios exigidos.",
        "aplicacaoPratica": "Antes de usar uma matéria-prima em manipulação, o farmacêutico deve conferir o certificado de análise correspondente ao lote recebido — não basta que a substância tenha certificado de análise de algum lote anterior.",
        "atencao": "Um certificado de análise emitido pelo próprio fornecedor não dispensa a farmácia ou indústria de realizar, quando exigido pela legislação, seus próprios testes de identificação da matéria-prima antes da liberação para uso.",
        "termosRelacionados": ["especificacao-farmacopeica", "controle-qualidade-termo"],
        "fontes": ["Resolução CFF nº 734/2022"]
    },
    {
        "id": "amostra-representativa", "termo": "Amostra Representativa", "categoria": "controle-qualidade",
        "sinonimos": [],
        "definicao": "Quantidade de amostra, estatisticamente calculada, que representa adequadamente o universo amostrado, permitindo que os resultados obtidos em sua análise sejam extrapolados com confiança para todo o lote ou população de origem.",
        "explicacaoSimplificada": "É a porção retirada de um lote grande, calculada estatisticamente, para que o resultado do teste feito nela realmente reflita a qualidade de todo o lote — e não apenas daquela porção isolada.",
        "aplicacaoPratica": "Coletar amostra insuficiente ou de forma não aleatória (ex.: sempre do topo do mesmo recipiente) compromete a validade estatística do controle de qualidade, mesmo que a análise em si seja tecnicamente correta.",
        "atencao": "Um resultado de análise obtido de amostra não representativa pode dar falsa segurança sobre a qualidade de um lote inteiro — o plano de amostragem é parte central, não acessória, do controle de qualidade.",
        "termosRelacionados": ["amostra-retencao", "analise-de-controle"],
        "fontes": ["Resolução CFF nº 504/2009"]
    },
    {
        "id": "analise-de-controle", "termo": "Análise de Controle", "categoria": "controle-qualidade",
        "sinonimos": [],
        "definicao": "Análise efetuada em produtos sob regime de vigilância sanitária, após a entrega ao consumo, destinada a comprovar a conformidade do produto com a fórmula e as especificações que deram origem ao seu registro ou notificação sanitária.",
        "explicacaoSimplificada": "É a checagem de qualidade feita em produtos que já estão sendo vendidos no mercado, para confirmar que continuam correspondendo exatamente ao que foi aprovado no registro.",
        "aplicacaoPratica": "Diferencia-se da análise fiscal (realizada em caráter de rotina ou mediante denúncia, com foco em apuração de infração) por seu propósito específico de verificar a conformidade pós-comercialização com o que foi registrado.",
        "atencao": "A análise de controle e a análise fiscal podem incidir sobre o mesmo produto em momentos diferentes, com finalidades distintas — não devem ser confundidas em questões de prova sobre vigilância sanitária.",
        "termosRelacionados": ["analise-fiscal", "qualidade"],
        "fontes": ["Resolução CFF nº 406/2003", "Resolução CFF nº 530/2010"]
    },
    {
        "id": "calibracao", "termo": "Calibração", "categoria": "controle-qualidade",
        "sinonimos": [],
        "definicao": "Conjunto de operações que estabelece, sob condições especificadas, a relação entre os valores indicados por um instrumento ou sistema de medição e os valores correspondentes conhecidos de um padrão de referência rastreável.",
        "explicacaoSimplificada": "É o processo de conferir e ajustar um equipamento de medição (balança, termômetro, pHmetro) comparando-o com um padrão confiável, para garantir que suas leituras estejam corretas.",
        "aplicacaoPratica": "Balanças usadas na manipulação de medicamentos e termômetros de geladeiras de cadeia de frio precisam de calibração periódica com certificado rastreável — equipamento descalibrado pode gerar erro de dose ou falha na conservação de produtos termolábeis sem que ninguém perceba.",
        "atencao": "Um equipamento pode parecer funcionar normalmente e ainda assim estar descalibrado — por isso a calibração periódica documentada é obrigatória, independente da aparente normalidade do funcionamento.",
        "termosRelacionados": ["qualificacao", "controle-qualidade-termo"],
        "fontes": ["Resolução CFF nº 467/2007", "Resolução CFF nº 734/2022"]
    },
    {
        "id": "reanalise", "termo": "Reanálise", "categoria": "controle-qualidade",
        "sinonimos": [],
        "definicao": "Análise realizada em matéria-prima previamente analisada e aprovada, dentro de seu prazo de validade, para confirmar que suas especificações de qualidade permanecem dentro do estabelecido, geralmente quando se aproxima o vencimento do laudo original ou do prazo de retestagem definido pelo fabricante.",
        "explicacaoSimplificada": "É repetir o teste de qualidade de uma matéria-prima antes de usá-la, quando já se passou um tempo desde a última análise, para confirmar que ela ainda está dentro do padrão.",
        "aplicacaoPratica": "Matérias-primas com uso prolongado em estoque — comuns em farmácias de manipulação de menor movimento — frequentemente precisam de reanálise periódica, conforme o prazo de retestagem indicado pelo fornecedor.",
        "atencao": "Reanálise não deve ser confundida com extensão automática do prazo de validade: a reanálise confirma a conformidade naquele momento, mas o produto segue sujeito ao prazo de validade originalmente estabelecido.",
        "termosRelacionados": ["certificado-analise", "materia-prima-farmaceutica"],
        "fontes": ["Resolução CFF nº 406/2003"]
    },
    {
        "id": "reprocessamento", "termo": "Reprocessamento", "categoria": "controle-qualidade",
        "sinonimos": ["Reprocesso"],
        "definicao": "Operação de submeter todo ou parte de um lote de produto com desvio de qualidade a uma ou mais etapas adicionais de produção, a partir de um estágio definido do processo, para que sua qualidade possa ser aceita.",
        "explicacaoSimplificada": "É quando um lote que saiu fora do padrão passa por etapas extras de produção para ser corrigido e aprovado, em vez de ser simplesmente descartado.",
        "aplicacaoPratica": "O reprocessamento só é aceitável quando documentado, justificado tecnicamente e quando o produto reprocessado é novamente submetido a todos os testes de controle de qualidade exigidos antes da liberação.",
        "atencao": "Reprocessamento não deve ser confundido com recuperação (incorporar parte de um lote de qualidade comprovada a outro lote) — são conceitos tecnicamente distintos, embora relacionados, frequentemente cobrados juntos em provas.",
        "termosRelacionados": ["certificado-analise"],
        "fontes": ["Resolução CFF nº 406/2003", "Resolução CFF nº 734/2022"]
    },
    {
        "id": "boas-praticas-laboratorio", "termo": "Boas Práticas de Laboratório (BPL)", "categoria": "controle-qualidade",
        "sinonimos": ["BPL"],
        "definicao": "Sistema da qualidade que diz respeito à organização e às condições sob as quais estudos em laboratório e em campo são planejados, realizados, monitorados, registrados, relatados e arquivados, constituindo um conjunto de princípios que asseguram a confiabilidade dos laudos emitidos por um dado laboratório.",
        "explicacaoSimplificada": "É o conjunto de regras que garante que os resultados produzidos por um laboratório (de análises, de pesquisa, de controle de qualidade) são confiáveis e reprodutíveis.",
        "aplicacaoPratica": "Laboratórios que realizam estudos de estabilidade, bioequivalência ou toxicologia pré-clínica precisam seguir BPL para que seus resultados sejam aceitos pela Anvisa em processos de registro de medicamentos.",
        "atencao": "BPL (foco em estudos laboratoriais e de pesquisa) não deve ser confundida com BPF — Boas Práticas de Fabricação (foco na produção industrial) nem com BPFM — Boas Práticas de Manipulação em Farmácias, embora as três sigam a mesma lógica de sistema de qualidade.",
        "termosRelacionados": ["boas-praticas-fabricacao", "bpfm"],
        "fontes": ["Resolução CFF nº 504/2009"]
    },
    {
        "id": "rotulo", "termo": "Rótulo", "categoria": "controle-qualidade",
        "sinonimos": [],
        "definicao": "Identificação impressa ou litografada, bem como os dizeres pintados ou gravados a fogo, por pressão ou decalque, aplicados diretamente sobre recipientes, vasilhames, invólucros, envoltórios ou qualquer outro protetor de embalagem de um produto.",
        "explicacaoSimplificada": "É toda a informação impressa diretamente na embalagem do medicamento ou produto — nome, lote, validade, composição, instruções — e não apenas uma etiqueta solta.",
        "aplicacaoPratica": "Em medicamentos manipulados, o rótulo precisa conter, no mínimo, identificação do paciente, composição, posologia, data de manipulação, prazo de validade e identificação do farmacêutico responsável — sua ausência ou incompletude é motivo recorrente de autuação sanitária.",
        "atencao": "Rótulo não é o mesmo que bula: o rótulo é a informação impressa na própria embalagem, enquanto a bula é o impresso adjunto e separado do medicamento, com informações mais detalhadas.",
        "termosRelacionados": ["bula", "lote-ou-partida"],
        "fontes": ["Resolução CFF nº 406/2003", "Resolução CFF nº 467/2007"]
    },
    {
        "id": "excursao-temperatura", "termo": "Excursão de Temperatura", "categoria": "controle-qualidade",
        "sinonimos": [],
        "definicao": "Desvio das condições de armazenagem aprovadas para um produto, por um determinado período (mediante estudo de estabilidade do referido produto), seja durante a armazenagem ou o transporte, que pode comprometer sua qualidade, segurança ou eficácia.",
        "explicacaoSimplificada": "É quando um produto que precisa ficar refrigerado (ou em outra faixa de temperatura definida) sai dessa faixa por um tempo — por exemplo, durante uma queda de energia ou falha no transporte.",
        "aplicacaoPratica": "Diante de uma excursão de temperatura em produtos termolábeis (como vacinas e insulinas), a decisão de descartar ou manter o lote deve ser baseada em estudo de estabilidade do fabricante, nunca em avaliação visual subjetiva do tipo 'parece estar bom'.",
        "atencao": "Produto submetido a excursão de temperatura não registrada ou não avaliada tecnicamente deve ser considerado suspeito e segregado até que o fabricante confirme (ou não) a manutenção da qualidade — nunca dispensado por precaução.",
        "termosRelacionados": ["cadeia-fria"],
        "fontes": ["Resolução CFF nº 679/2020"]
    },

    # ============ VIGILÂNCIA SANITÁRIA (6) ============
    {
        "id": "processamento-produto-saude", "termo": "Processamento de Produto para Saúde", "categoria": "vigilancia-sanitaria",
        "sinonimos": [],
        "definicao": "Conjunto de ações relacionadas à esterilização de produtos novos ou à pré-limpeza, recepção, limpeza, secagem, avaliação da integridade e da funcionalidade, preparo, desinfecção ou esterilização, armazenamento e distribuição de produtos para saúde para as unidades consumidoras.",
        "explicacaoSimplificada": "É todo o ciclo pelo qual passam materiais e equipamentos de saúde reutilizáveis (como instrumentais cirúrgicos) para ficarem limpos, desinfetados ou esterilizados e prontos para uso seguro novamente.",
        "aplicacaoPratica": "Costuma ser realizado em Centrais de Material e Esterilização (CME) de hospitais, área de atuação em que farmacêuticos podem assumir responsabilidade técnica, avaliando a eficácia dos processos de esterilização.",
        "atencao": "Produtos para saúde passíveis de reprocessamento devem comprovar, por validação técnica, que mantêm sua eficácia e funcionalidade mesmo após repetidos ciclos de limpeza e esterilização — nem todo produto é reprocessável indefinidamente.",
        "termosRelacionados": ["produtos-para-saude"],
        "fontes": ["Resolução CFF nº 723/2022"]
    },
    {
        "id": "produtos-para-saude", "termo": "Produtos para a Saúde (Produtos Médicos)", "categoria": "vigilancia-sanitaria",
        "sinonimos": ["Produtos médicos"],
        "definicao": "Produtos enquadrados como equipamentos, aparelhos, materiais, artigos ou sistemas de uso ou aplicação médica, odontológica, fisioterapêutica ou laboratorial, destinados à prevenção, diagnóstico, tratamento, reabilitação ou anticoncepção, que não utilizam meio farmacológico, imunológico ou metabólico para realizar sua principal função, podendo, entretanto, ser auxiliados em suas funções por tais meios.",
        "explicacaoSimplificada": "São itens de saúde que não são medicamentos — como seringas, curativos, próteses e equipamentos de diagnóstico — cuja ação não depende de efeito farmacológico direto.",
        "aplicacaoPratica": "A distinção entre medicamento e produto para a saúde define qual via regulatória da Anvisa se aplica ao produto (registro de medicamento versus registro/notificação de produto para saúde), com exigências técnicas diferentes.",
        "atencao": "Alguns produtos ficam na fronteira entre as duas categorias (ex.: certos dispositivos com liberação de substância ativa) — a classificação correta impacta diretamente qual norma sanitária rege sua fabricação, registro e comercialização.",
        "termosRelacionados": ["processamento-produto-saude"],
        "fontes": ["Resolução CFF nº 549/2011", "Resolução CFF nº 679/2020"]
    },
    {
        "id": "empresa-remessa-expressa", "termo": "Empresa de Remessa Expressa (\"Courier\")", "categoria": "vigilancia-sanitaria",
        "sinonimos": ["Courier"],
        "definicao": "Empresa que tem como atividade preponderante a prestação de serviços de transporte expresso, porta a porta, de remessas destinadas a terceiros, em fluxo regular e contínuo, incluindo produtos sujeitos à vigilância sanitária.",
        "explicacaoSimplificada": "É a transportadora especializada em entregas rápidas, porta a porta — como as que trazem encomendas internacionais ou de medicamentos importados por via expressa.",
        "aplicacaoPratica": "Relevante na importação de medicamentos por pessoa física (ex.: tratamentos não disponíveis no Brasil) e na logística de produtos biológicos urgentes, onde o cumprimento da cadeia de frio pela empresa de courier é ponto crítico.",
        "atencao": "Mesmo remessas de pequeno porte por courier, quando envolvem produtos sob vigilância sanitária, estão sujeitas a controle alfandegário e sanitário — não há dispensa automática de fiscalização por se tratar de encomenda individual.",
        "termosRelacionados": ["armazenagem-transito", "cadeia-fria"],
        "fontes": ["Resolução CFF nº 679/2020"]
    },
    {
        "id": "armazenagem-transito", "termo": "Armazenagem em Trânsito", "categoria": "vigilancia-sanitaria",
        "sinonimos": [],
        "definicao": "Conjunto de procedimentos de caráter temporário, relacionados ao trânsito de carga, que envolvem as atividades de recebimento, guarda temporária, conservação e segurança de produtos sujeitos à vigilância sanitária enquanto aguardam seguimento no percurso logístico.",
        "explicacaoSimplificada": "É o período em que a carga de medicamentos ou produtos de saúde fica guardada temporariamente — em um porto, aeroporto ou centro de distribuição — no meio do caminho entre a origem e o destino final.",
        "aplicacaoPratica": "Mesmo sendo temporária, a armazenagem em trânsito exige as mesmas condições de conservação (temperatura, umidade, segurança) do armazenamento definitivo, especialmente para produtos termolábeis.",
        "atencao": "Falhas de conservação durante a armazenagem em trânsito são uma causa frequente, porém pouco lembrada, de perda de qualidade de produtos — a responsabilidade pela integridade do produto não se interrompe durante essa etapa intermediária.",
        "termosRelacionados": ["cadeia-fria", "logistica-farmaceutica"],
        "fontes": ["Resolução CFF nº 679/2020"]
    },
    {
        "id": "fispq", "termo": "Ficha de Segurança de Produtos Químicos (FISPQ)", "categoria": "vigilancia-sanitaria",
        "sinonimos": ["FISPQ"],
        "definicao": "Documento normatizado pela Associação Brasileira de Normas Técnicas (ABNT), conforme a NBR 14725-4, que reúne informações sobre os riscos de um produto químico e as recomendações para seu manuseio, armazenamento, transporte e descarte seguros, além de medidas em caso de acidente.",
        "explicacaoSimplificada": "É o 'manual de segurança' de uma substância química, explicando seus riscos (toxicidade, inflamabilidade etc.) e o que fazer para manuseá-la, guardá-la e descartá-la com segurança.",
        "aplicacaoPratica": "Toda farmácia de manipulação deve manter as FISPQs das matérias-primas e reagentes usados, disponíveis para consulta dos manipuladores e para orientação em caso de acidente (ex.: contato acidental com a pele ou os olhos).",
        "atencao": "A FISPQ não deve ser confundida com o rótulo do produto: ela traz informações técnicas de segurança ocupacional e ambiental, não instruções de uso terapêutico — é voltada a quem manuseia a substância, não ao paciente.",
        "termosRelacionados": [],
        "fontes": ["Resolução CFF nº 731/2022"]
    },
    {
        "id": "classificacao-risco-biologico", "termo": "Classificação de Risco Biológico", "categoria": "vigilancia-sanitaria",
        "sinonimos": [],
        "definicao": "Nível de risco frente à exposição a agentes biológicos, determinado pela patogenicidade do agente, pelo modo e pela relativa facilidade de transmissão, pela disponibilidade de tratamentos e preventivos conhecidos e eficazes, utilizado para orientar as medidas de biossegurança apropriadas.",
        "explicacaoSimplificada": "É a forma de classificar o quanto um microrganismo ou material biológico é perigoso, considerando se causa doença, como se transmite e se já existe tratamento ou prevenção eficaz contra ele.",
        "aplicacaoPratica": "Orienta o nível de biossegurança (classe de risco 1 a 4) exigido no transporte, manuseio e descarte de material biológico, incluindo o tipo de embalagem e as precauções exigidas de quem o transporta.",
        "atencao": "A classificação de risco biológico de um material determina diretamente as exigências de transporte (embalagem tripla, identificação específica) — transportar material de maior risco com embalagem inadequada é infração sanitária grave.",
        "termosRelacionados": ["biosseguranca"],
        "fontes": ["Resolução CFF nº 626/2016"]
    },

    # ============ SAÚDE PÚBLICA (5) ============
    {
        "id": "sus", "termo": "Sistema Único de Saúde (SUS)", "categoria": "saude-publica",
        "sinonimos": ["SUS"],
        "definicao": "Conjunto de ações e serviços de saúde, prestados por órgãos e instituições públicas federais, estaduais e municipais, da administração direta e indireta e das fundações mantidas pelo Poder Público, organizado segundo os princípios da universalidade, integralidade e equidade.",
        "explicacaoSimplificada": "É o sistema público de saúde do Brasil, que garante atendimento gratuito a toda a população, dos postos de saúde aos hospitais, incluindo o fornecimento de medicamentos essenciais.",
        "aplicacaoPratica": "A assistência farmacêutica no SUS organiza-se em ciclo (seleção, programação, aquisição, armazenamento, distribuição e dispensação), tendo a RENAME como referência de medicamentos padronizados nos três níveis de atenção.",
        "atencao": "O acesso gratuito a um medicamento pelo SUS depende de ele estar padronizado (incluído em listas como a RENAME ou protocolos estaduais/municipais) — nem todo medicamento registrado na Anvisa é automaticamente fornecido pelo sistema público.",
        "termosRelacionados": ["rename", "assistencia-farmaceutica"],
        "fontes": ["Lei Federal nº 8.080/1990", "Resolução CFF nº 465/2007"]
    },
    {
        "id": "educacao-em-saude", "termo": "Educação em Saúde", "categoria": "saude-publica",
        "sinonimos": [],
        "definicao": "Serviço que compreende diferentes estratégias educativas que integram o saber popular e científico, de modo a contribuir para aumentar conhecimentos, desenvolver habilidades e atitudes sobre os problemas de saúde e seus tratamentos, com vistas à autonomia dos pacientes e ao comprometimento de todos pela qualidade de vida.",
        "explicacaoSimplificada": "É ensinar e orientar a população sobre saúde e cuidados — de forma acessível, respeitando o que as pessoas já sabem — para que elas ganhem mais autonomia sobre sua própria saúde.",
        "aplicacaoPratica": "Campanhas de orientação em farmácia sobre uso correto de medicamentos, descarte adequado de sobras e prevenção de doenças sazonais são exemplos de educação em saúde praticada rotineiramente pelo farmacêutico comunitário.",
        "atencao": "Educação em saúde eficaz não é apenas repassar informação técnica — envolve dialogar com a cultura e os saberes populares do paciente, sob risco de a orientação ser tecnicamente correta, mas ineficaz na prática.",
        "termosRelacionados": ["automedicacao", "uso-racional-medicamentos"],
        "fontes": ["Resolução CFF nº 465/2007", "Resolução CFF nº 610/2015"]
    },
    {
        "id": "saude-baseada-evidencia", "termo": "Saúde Baseada em Evidência", "categoria": "saude-publica",
        "sinonimos": [],
        "definicao": "Abordagem que utiliza as ferramentas da epidemiologia clínica, da estatística, da metodologia científica e da informática para trabalhar a pesquisa, o conhecimento e a atuação em saúde, com o objetivo de oferecer a melhor informação disponível para a tomada de decisão nesse campo.",
        "explicacaoSimplificada": "É basear as decisões de saúde (tratamentos, protocolos, políticas) nas melhores evidências científicas disponíveis, em vez de opinião pessoal ou tradição sem comprovação.",
        "aplicacaoPratica": "Fundamenta a elaboração de protocolos clínicos e diretrizes terapêuticas (PCDT) e orienta a seleção de medicamentos para listas como a RENAME, priorizando opções com comprovação robusta de eficácia e segurança.",
        "atencao": "Saúde baseada em evidência não significa ignorar o contexto individual do paciente — a melhor evidência científica deve ser conciliada com as características, valores e preferências de cada caso, conforme o próprio conceito de cuidado centrado no paciente.",
        "termosRelacionados": ["cuidado-centrado-paciente"],
        "fontes": ["Resolução CFF nº 585/2013", "Resolução CFF nº 685/2020"]
    },
    {
        "id": "gerenciamento-tecnologias-saude", "termo": "Gerenciamento de Tecnologias em Saúde", "categoria": "saude-publica",
        "sinonimos": [],
        "definicao": "Procedimentos de gestão, planejados e implementados a partir de bases científicas, técnicas, normativas e legais, com o objetivo de garantir a rastreabilidade, qualidade, eficácia, efetividade e segurança das tecnologias em saúde utilizadas na prestação de serviços de saúde, desde o planejamento até o descarte.",
        "explicacaoSimplificada": "É administrar todo o ciclo de vida dos recursos de saúde — medicamentos, equipamentos, insumos — desde a entrada no serviço de saúde até o descarte final, garantindo que sejam usados com qualidade e segurança o tempo todo.",
        "aplicacaoPratica": "Núcleos de Avaliação de Tecnologias em Saúde (NATS) usam evidências disponíveis para orientar gestores hospitalares na incorporação de novas tecnologias, como novos medicamentos de alto custo.",
        "atencao": "O gerenciamento de tecnologias em saúde abrange desde o planejamento até o descarte — negligenciar a etapa de descarte adequado (ex.: de medicamentos vencidos ou equipamentos obsoletos) também é uma falha desse processo, não só uma questão ambiental isolada.",
        "termosRelacionados": ["formulario-terapeutico-nacional"],
        "fontes": ["Resolução CFF nº 672/2019", "Resolução CFF nº 675/2019"]
    },
    {
        "id": "formulario-terapeutico-nacional", "termo": "Formulário Terapêutico Nacional", "categoria": "saude-publica",
        "sinonimos": ["FTN"],
        "definicao": "Documento que reúne informações científicas e baseadas em evidências sobre os medicamentos selecionados na Relação Nacional de Medicamentos Essenciais (Rename), com o objetivo de subsidiar os profissionais de saúde na prescrição, dispensação e uso racional desses medicamentos.",
        "explicacaoSimplificada": "É o 'manual de uso' oficial dos medicamentos que o SUS padroniza — reúne, para cada medicamento da RENAME, informações sobre indicação, posologia, contraindicações e orientações práticas.",
        "aplicacaoPratica": "É uma referência técnica de consulta direta na dispensação e orientação farmacêutica dentro do SUS, complementando a RENAME (que apenas lista os medicamentos padronizados) com informações farmacológicas detalhadas sobre cada um.",
        "atencao": "O Formulário Terapêutico Nacional é atualizado periodicamente acompanhando as revisões da RENAME — usar uma versão desatualizada pode levar a orientações que não refletem mudanças recentes de padronização.",
        "termosRelacionados": ["rename"],
        "fontes": ["Resolução CFF nº 357/2011", "Resolução CFF nº 735/2022"]
    },

    # ============ FARMACOCINÉTICA (cluster hemodiálise, 3) ============
    {
        "id": "hemodialise", "termo": "Hemodiálise", "categoria": "farmacocinetica",
        "sinonimos": ["Diálise peritonial (modalidade relacionada)"],
        "definicao": "Modalidade de diálise na qual o sangue obtido por um acesso vascular é impulsionado por uma bomba para um sistema de circulação extracorpórea contendo um filtro (dialisador), onde ocorrem as trocas entre o sangue e o banho de diálise (dialisato) através de uma membrana semipermeável, removendo substâncias e excesso de líquido acumulados pela insuficiência renal.",
        "explicacaoSimplificada": "É o procedimento que 'filtra artificialmente' o sangue de pacientes cujos rins não conseguem mais fazer essa limpeza sozinhos, retirando toxinas e excesso de líquido.",
        "aplicacaoPratica": "A hemodiálise remove alguns medicamentos do sangue junto com as toxinas (medicamentos dialisáveis) — o farmacêutico precisa saber se um fármaco é removido na sessão para orientar se a dose deve ser reposta após a diálise.",
        "atencao": "A diálise peritonial é outra modalidade de diálise, realizada dentro do próprio corpo do paciente usando o peritônio como membrana filtrante — não deve ser confundida com a hemodiálise, que usa um filtro externo (dialisador).",
        "termosRelacionados": ["dialisabilidade", "insuficiencia-renal", "filtracao-glomerular"],
        "fontes": ["Resolução CFF nº 672/2019"]
    },
    {
        "id": "dialisabilidade", "termo": "Dialisabilidade", "categoria": "farmacocinetica",
        "sinonimos": [],
        "definicao": "Propriedade de um medicamento ser removido do organismo por meio de uma membrana de diálise, dependente de fatores como o peso molecular do fármaco, sua ligação a proteínas plasmáticas, seu volume de distribuição e a técnica dialítica empregada.",
        "explicacaoSimplificada": "É o quanto um medicamento consegue ser 'filtrado para fora' do sangue durante uma sessão de diálise — fármacos pequenos e pouco ligados a proteínas costumam ser mais facilmente removidos.",
        "aplicacaoPratica": "Medicamentos com alta dialisabilidade (ex.: muitos antibióticos hidrossolúveis) frequentemente precisam de uma dose suplementar após a sessão de hemodiálise, para repor o que foi removido pelo procedimento — informação essencial para o ajuste posológico em pacientes renais crônicos.",
        "atencao": "Fármacos com alto volume de distribuição ou alta ligação a proteínas plasmáticas (como a digoxina) têm baixa dialisabilidade, mesmo sendo de peso molecular pequeno — a dialisabilidade não depende de um único fator isolado.",
        "termosRelacionados": ["hemodialise", "ajuste-posologico"],
        "fontes": ["Resolução CFF nº 672/2019"]
    },
    {
        "id": "cphd", "termo": "Concentrado Polieletrolítico para Hemodiálise (CPHD)", "categoria": "farmacocinetica",
        "sinonimos": ["CPHD"],
        "definicao": "Concentrado de eletrólitos, com ou sem glicose, apresentado na forma sólida ou líquida, empregado na terapia dialítica para compor, após diluição em água tratada (STDAH), o dialisato utilizado na sessão de hemodiálise.",
        "explicacaoSimplificada": "É o 'concentrado' de sais minerais que, diluído em água tratada especialmente para esse fim, forma o líquido (dialisato) usado na máquina de hemodiálise para fazer a troca com o sangue do paciente.",
        "aplicacaoPratica": "A manipulação e o controle de qualidade do CPHD em farmácias e serviços de diálise é área reconhecida de atuação farmacêutica (Serviço de Diálise), exigindo controle rigoroso da composição eletrolítica para a segurança do paciente renal.",
        "atencao": "Erros na concentração de eletrólitos do CPHD (como potássio ou sódio fora da especificação) podem causar graves distúrbios eletrolíticos no paciente durante a própria sessão de hemodiálise — o controle de qualidade desse insumo é crítico, não meramente burocrático.",
        "termosRelacionados": ["hemodialise"],
        "fontes": ["Resolução CFF nº 672/2019"]
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

    print(f"OK: {len(NOVOS_TERMOS)} termos adicionados.")
    print(f"Total de termos no banco: {total_antes} -> {len(data['termos'])}")


if __name__ == "__main__":
    main()
