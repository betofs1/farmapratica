"""
Patch: 40 novos termos para a categoria "Farmacologia Geral" do Dicionário
Farmacêutico FarmaPrática.

Pedido do usuário: "adicione mais 40 itens de sua escolha na aba
'Farmacologia Geral'" — a categoria com apenas 10 termos cadastrados desde a
v1.0 (Fármaco, Medicamento, Princípio Ativo, Droga, Xenobiótico, Placebo,
Efeito Nocebo, Farmacologia, Farmacognosia, Fitofármaco).

Curadoria: conceitos fundamentais/transversais da disciplina farmacológica
que não pertencem especificamente à Farmacodinâmica ou à Farmacocinética
(que já têm categorias próprias) — classificação de fármacos por origem,
terminologia de desenvolvimento e pesquisa de novos fármacos, metodologia de
ensaios clínicos, ramos/subdisciplinas da Farmacologia, e fenômenos
farmacológicos gerais (tolerância cruzada, sensibilização, abstinência,
potencial de abuso). Verificado programaticamente contra o banco completo
(561 termos) antes da redação, para excluir qualquer duplicata ou
quase-duplicata (ex.: "Alvo Farmacológico" já existe como sinônimo de
"Receptor Farmacológico"; "Dependência Farmacológica" e "Bioequivalência" já
cadastrados).

Todas as definições são redação própria, baseada em literatura farmacológica
consolidada (Katzung, Goodman & Gilman, Rang & Dale, Guyton & Hall) e em
documentos regulatórios/metodológicos de referência (ICH, OMS, Anvisa,
legislação brasileira), seguindo o mesmo schema e padrão duplo (definição
técnica + explicação simplificada + aplicação prática + atenção) já usado em
todas as rodadas anteriores. Roda diretamente sobre o dicionario.json real
do usuário.
"""

import json
import sys

NOVOS_TERMOS = [
    {
        "id": "farmaco-natural", "termo": "Fármaco Natural", "categoria": "farmacologia-geral",
        "sinonimos": ["Produto Natural Farmacologicamente Ativo"],
        "definicao": "Fármaco cujo princípio ativo é obtido diretamente de fontes vegetais, animais, microbianas ou minerais, sem modificação química da molécula original, geralmente por extração, purificação ou fermentação.",
        "explicacaoSimplificada": "É um fármaco que vem pronto da natureza — extraído de uma planta, de um microrganismo, de um animal ou de um mineral — sem passar por alteração química de sua estrutura.",
        "aplicacaoPratica": "Morfina (extraída do ópio), insulina de origem animal (histórica) e diversos antibióticos obtidos de fungos/bactérias (ex.: penicilina, estreptomicina) são exemplos clássicos de fármacos naturais ainda relevantes na terapêutica atual.",
        "atencao": "Fármaco natural não é sinônimo de fármaco seguro ou isento de toxicidade — a origem natural não altera o perfil farmacológico/toxicológico da molécula, confusão comum entre pacientes e cobrada em concursos.",
        "termosRelacionados": ["fitofarmaco", "farmacognosia", "farmaco-sintetico"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica", "Simões — Farmacognosia: da Planta ao Medicamento"]
    },
    {
        "id": "farmaco-sintetico", "termo": "Fármaco Sintético", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Fármaco cujo princípio ativo é produzido inteiramente por síntese química em laboratório, sem depender da extração de uma fonte natural preexistente.",
        "explicacaoSimplificada": "É um fármaco fabricado do zero por reações químicas, em vez de ser extraído de uma planta, animal ou microrganismo.",
        "aplicacaoPratica": "A maioria dos fármacos atualmente comercializados (ex.: a maioria dos antihipertensivos, anti-inflamatórios e psicotrópicos) é de origem sintética, permitindo maior controle de pureza e reprodutibilidade de lote.",
        "atencao": "Não confundir com fármaco semissintético: o sintético não usa nenhuma molécula natural como ponto de partida, enquanto o semissintético parte de uma molécula natural e a modifica quimicamente.",
        "termosRelacionados": ["farmaco-semissintetico", "farmaco-natural"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "farmaco-semissintetico", "termo": "Fármaco Semissintético", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Fármaco obtido pela modificação química parcial de uma molécula de origem natural, com o objetivo de melhorar propriedades farmacocinéticas, farmacodinâmicas, de estabilidade ou de resistência a vias de degradação.",
        "explicacaoSimplificada": "É um fármaco que começa como algo extraído da natureza, mas que passa por alterações químicas no laboratório para ficar melhor — mais estável, mais potente ou com menos efeitos adversos.",
        "aplicacaoPratica": "A amoxicilina e outras penicilinas semissintéticas (derivadas do núcleo beta-lactâmico obtido por fermentação) e opioides semissintéticos (ex.: oxicodona, a partir da tebaína) são exemplos clássicos cobrados em prova.",
        "atencao": "É a categoria intermediária entre fármaco natural e sintético — armadilha comum de concurso é classificar penicilinas semissintéticas como totalmente sintéticas, ignorando a origem fermentativa do núcleo beta-lactâmico.",
        "termosRelacionados": ["farmaco-natural", "farmaco-sintetico"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "farmaco-biotecnologico", "termo": "Fármaco Biotecnológico", "categoria": "farmacologia-geral",
        "sinonimos": ["Biofármaco"],
        "definicao": "Fármaco cujo princípio ativo é produzido a partir de organismos vivos ou de seus componentes (células geneticamente modificadas, culturas celulares, tecnologia de DNA recombinante), incluindo proteínas, anticorpos monoclonais, vacinas e hormônios recombinantes.",
        "explicacaoSimplificada": "É um fármaco produzido usando seres vivos, como bactérias ou células geneticamente modificadas, como fábricas para fabricar a molécula, em vez de produzi-la por síntese química tradicional.",
        "aplicacaoPratica": "Insulina humana recombinante, anticorpos monoclonais (ex.: adalimumabe, infliximabe), eritropoetina e vacinas de subunidade recombinante são exemplos de fármacos biotecnológicos amplamente usados na farmácia clínica.",
        "atencao": "Fármacos biotecnológicos não têm genéricos no sentido tradicional — sua cópia é chamada de biossimilar, com exigências regulatórias próprias de comparabilidade, diferentes do registro de um genérico convencional.",
        "termosRelacionados": ["medicamento-biologico", "biossimilar", "anticorpo-monoclonal"],
        "fontes": ["RDC Anvisa nº 55/2010 (Produtos Biológicos)", "Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "nutraceutico", "termo": "Nutracêutico", "categoria": "farmacologia-geral",
        "sinonimos": ["Alimento Funcional Bioativo"],
        "definicao": "Substância ou componente de alimento com propriedade farmacológica ou de promoção da saúde comprovada, consumido na forma de suplemento ou como parte de alimentos funcionais, situando-se na fronteira entre alimento e medicamento.",
        "explicacaoSimplificada": "É algo que está no meio do caminho entre comida e remédio — um composto presente em alimentos, ou extraído deles, que tem efeito benéfico comprovado sobre a saúde, mas não é regulado exatamente como medicamento.",
        "aplicacaoPratica": "Ômega-3, probióticos padronizados, fitoesteróis e certos flavonoides são comercializados como nutracêuticos; o farmacêutico deve orientar quanto à ausência de evidência robusta de eficácia para muitos produtos dessa categoria.",
        "atencao": "Nutracêutico não é uma categoria regulatória formal na legislação brasileira, que trabalha com alimento, suplemento alimentar e medicamento — é um termo de uso corrente na literatura científica e no mercado, não um status jurídico-sanitário.",
        "termosRelacionados": ["fitofarmaco"],
        "fontes": ["RDC Anvisa nº 243/2018 (Suplementos Alimentares)"]
    },
    {
        "id": "toxina", "termo": "Toxina", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Substância tóxica produzida por organismos vivos (bactérias, fungos, plantas, animais), capaz de causar efeitos deletérios no organismo mesmo em pequenas quantidades, geralmente por mecanismo bioquímico específico.",
        "explicacaoSimplificada": "É um veneno produzido por um ser vivo — por exemplo, por uma bactéria, um fungo, uma planta ou um animal — e que pode causar dano mesmo em quantidades muito pequenas.",
        "aplicacaoPratica": "A toxina botulínica, produzida pela bactéria Clostridium botulinum, é usada terapeuticamente em doses extremamente baixas e controladas — exemplo clássico de como uma toxina pode ser aproveitada farmacologicamente respeitando a margem de segurança.",
        "atencao": "Toxina é diferente de veneno: toxina é sempre produzida por um organismo vivo; veneno é um termo mais amplo, que inclui qualquer substância deletéria, de origem biológica ou não.",
        "termosRelacionados": ["veneno", "peconha", "toxicodinamica"],
        "fontes": ["Klaassen — Toxicologia de Casarett e Doull"]
    },
    {
        "id": "veneno", "termo": "Veneno", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Qualquer substância capaz de produzir efeito nocivo ou letal ao organismo, independentemente de sua origem (biológica, química ou mineral), quando em contato, ingerida, inalada ou absorvida em quantidade e condições suficientes.",
        "explicacaoSimplificada": "É qualquer substância, de qualquer origem, capaz de causar dano ou morte ao organismo, dependendo da dose e da forma de exposição.",
        "aplicacaoPratica": "O princípio de Paracelso, segundo o qual a dose faz o veneno, é a base conceitual da toxicologia: até substâncias essenciais podem ser venenosas em excesso, e substâncias tóxicas podem ser seguras em doses muito baixas.",
        "atencao": "Não confundir com peçonha, que é especificamente o veneno inoculado ativamente por um animal através de um aparelho inoculador — todo veneno peçonhento é veneno, mas nem todo veneno é peçonha.",
        "termosRelacionados": ["toxina", "peconha", "intoxicacao-aguda"],
        "fontes": ["Klaassen — Toxicologia de Casarett e Doull"]
    },
    {
        "id": "peconha", "termo": "Peçonha", "categoria": "farmacologia-geral",
        "sinonimos": ["Veneno Peçonhento"],
        "definicao": "Secreção tóxica produzida por glândulas especializadas de determinados animais (serpentes, aracnídeos, escorpiões, alguns peixes) e inoculada ativamente na vítima por meio de um aparelho inoculador, como presas, ferrões ou aguilhões.",
        "explicacaoSimplificada": "É o veneno que certos animais injetam ativamente em quem eles picam ou ferroam, usando uma estrutura especializada para isso, como as presas de uma cobra.",
        "aplicacaoPratica": "O tratamento de acidentes ofídicos, escorpiônicos e aracnídicos envolve soros antipeçonhentos específicos — a escolha do soro depende da identificação, ou suspeita fundamentada, do animal causador.",
        "atencao": "O termo correto para animais que produzem peçonha é peçonhentos — venenosos é o termo para animais cuja toxicidade decorre de contato passivo, sem aparelho inoculador ativo, distinção clássica de prova.",
        "termosRelacionados": ["veneno", "toxina"],
        "fontes": ["Ministério da Saúde — Manual de Diagnóstico e Tratamento de Acidentes por Animais Peçonhentos"]
    },
    {
        "id": "ligante-farmacologico", "termo": "Ligante Farmacológico", "categoria": "farmacologia-geral",
        "sinonimos": ["Ligante"],
        "definicao": "Qualquer molécula, endógena ou exógena, incluindo fármacos, capaz de se ligar especificamente a um receptor, enzima, canal iônico ou outra macromolécula-alvo, com afinidade determinada, podendo ou não desencadear resposta biológica.",
        "explicacaoSimplificada": "É qualquer substância capaz de se encaixar em um receptor ou outra molécula-alvo do organismo — o fato de se ligar não significa, por si só, que vai produzir um efeito.",
        "aplicacaoPratica": "O conceito de ligante é a base para entender a diferença entre afinidade (capacidade de se ligar ao receptor) e eficácia ou atividade intrínseca (capacidade de ativar o receptor após a ligação) — um antagonista é um ligante sem atividade intrínseca.",
        "atencao": "Nem todo ligante é um agonista: antagonistas, agonistas inversos e agonistas parciais também são ligantes do mesmo receptor, diferindo apenas na resposta funcional que produzem.",
        "termosRelacionados": ["receptor", "agonista", "antagonista"],
        "fontes": ["Rang & Dale — Farmacologia"]
    },
    {
        "id": "farmaco-prototipico", "termo": "Fármaco Prototípico", "sigla": "", "categoria": "farmacologia-geral",
        "sinonimos": ["Protótipo Farmacológico"],
        "definicao": "Fármaco que, por ter sido o primeiro de sua classe farmacológica a ser descoberto, estudado em profundidade ou amplamente utilizado, passa a servir como referência didática e comparativa para os demais fármacos do mesmo grupo.",
        "explicacaoSimplificada": "É o fármaco-modelo de uma classe — aquele usado como referência para explicar e comparar o mecanismo, os efeitos e os usos dos demais fármacos daquele grupo.",
        "aplicacaoPratica": "A morfina é o protótipo dos opioides, a penicilina G o protótipo dos betalactâmicos e a atropina o protótipo dos anticolinérgicos — entender o protótipo facilita compreender toda a classe por comparação.",
        "atencao": "Fármaco prototípico não é necessariamente o mais usado na prática atual nem o mais seguro — é apenas a referência histórica/didática da classe; fármacos mais novos do mesmo grupo podem ter perfil de segurança superior ao protótipo.",
        "termosRelacionados": ["farmacologia", "farmaco"],
        "fontes": ["Katzung — Farmacologia Básica e Clínica"]
    },
    {
        "id": "farmaco-me-too", "termo": "Fármaco Me-Too", "categoria": "farmacologia-geral",
        "sinonimos": ["Me-Too Drug"],
        "definicao": "Fármaco desenvolvido a partir de pequenas modificações estruturais de um fármaco já existente e comercialmente bem-sucedido, pertencente à mesma classe farmacológica, geralmente sem trazer benefício terapêutico substancialmente novo.",
        "explicacaoSimplificada": "É um fármaco parecido com outro que já existe e já faz sucesso no mercado, criado com pequenas mudanças na molécula — geralmente não representa um avanço terapêutico real.",
        "aplicacaoPratica": "A existência de múltiplos fármacos de uma mesma classe com mecanismo de ação quase idêntico (ex.: diversos IBPs, diversas estatinas) ilustra a estratégia me-too — a escolha entre eles costuma depender mais de custo e posologia do que de eficácia superior comprovada.",
        "atencao": "Fármaco me-too não deve ser confundido com nova entidade molecular (NME) — o me-too não representa uma classe farmacológica nova nem um mecanismo de ação inédito, apenas uma variação dentro de uma classe já estabelecida.",
        "termosRelacionados": ["nova-entidade-molecular", "patente-farmaceutica"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "nova-entidade-molecular", "termo": "Nova Entidade Molecular", "sigla": "NME", "categoria": "farmacologia-geral",
        "sinonimos": ["New Molecular Entity"],
        "definicao": "Fármaco cujo princípio ativo apresenta estrutura química inédita, nunca antes aprovada para uso terapêutico por nenhuma agência regulatória, representando genuína inovação molecular e, frequentemente, novo mecanismo de ação.",
        "explicacaoSimplificada": "É um fármaco realmente novo, com uma molécula que nunca tinha sido aprovada antes em lugar nenhum — diferente de uma variação pequena de algo que já existia.",
        "aplicacaoPratica": "Agências regulatórias (como FDA e Anvisa) divulgam anualmente quantos fármacos aprovados são NMEs, indicador frequentemente usado para avaliar o grau de inovação real da indústria farmacêutica em determinado período.",
        "atencao": "Nem toda NME representa avanço terapêutico clinicamente relevante — a classificação é baseada em novidade estrutural/regulatória, não em superioridade de eficácia ou segurança frente a tratamentos já existentes.",
        "termosRelacionados": ["farmaco-me-too", "patente-farmaceutica"],
        "fontes": ["FDA — Novel Drug Approvals", "Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "triagem-farmacologica", "termo": "Triagem Farmacológica", "sigla": "", "categoria": "farmacologia-geral",
        "sinonimos": ["Screening Farmacológico"],
        "definicao": "Etapa inicial da pesquisa e desenvolvimento de fármacos em que um grande número de moléculas é testado, geralmente em sistemas in vitro ou em modelos de alto rendimento (high-throughput screening), para identificar compostos com potencial atividade biológica de interesse.",
        "explicacaoSimplificada": "É a fase em que milhares de moléculas são testadas rapidamente em laboratório para descobrir quais delas têm algum efeito biológico interessante, antes de qualquer teste em animais ou humanos.",
        "aplicacaoPratica": "A triagem de alto rendimento permite testar centenas de milhares de compostos contra um alvo molecular específico em curto espaço de tempo, etapa que precede a seleção de candidatos para os estudos pré-clínicos.",
        "atencao": "A triagem farmacológica ocorre antes dos estudos pré-clínicos em animais — não deve ser confundida com eles, já que ainda não envolve organismos vivos complexos, apenas ensaios in vitro, bioquímicos ou computacionais.",
        "termosRelacionados": ["estudo-pre-clinico"],
        "fontes": ["Katzung — Farmacologia Básica e Clínica"]
    },
    {
        "id": "reposicionamento-farmacos", "termo": "Reposicionamento de Fármacos", "categoria": "farmacologia-geral",
        "sinonimos": ["Drug Repurposing", "Drug Repositioning", "Redirecionamento Terapêutico"],
        "definicao": "Estratégia de pesquisa que busca novas indicações terapêuticas para fármacos já aprovados e com perfil de segurança conhecido, reduzindo tempo e custo de desenvolvimento em comparação ao desenvolvimento de uma molécula inédita.",
        "explicacaoSimplificada": "É encontrar um novo uso para um medicamento que já existe e já é considerado seguro, em vez de desenvolver um fármaco totalmente novo do zero.",
        "aplicacaoPratica": "A sildenafila, originalmente estudada para angina, foi reposicionada para disfunção erétil e, depois, hipertensão pulmonar; a talidomida, retirada do mercado por teratogenicidade, foi reposicionada para mieloma múltiplo e hanseníase sob controle rígido.",
        "atencao": "O reposicionamento não dispensa novos estudos clínicos específicos para a nova indicação — o fato de o fármaco já ser aprovado para outro uso não garante eficácia ou segurança na nova condição.",
        "termosRelacionados": ["ensaio-clinico-randomizado", "nova-entidade-molecular"],
        "fontes": ["Nature Reviews Drug Discovery — Drug repurposing: progress, challenges and recommendations"]
    },
    {
        "id": "patente-farmaceutica", "termo": "Patente Farmacêutica", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Direito de exclusividade temporária concedido pelo Estado ao titular de uma invenção farmacêutica (nova molécula, processo de síntese ou formulação), impedindo que terceiros fabriquem, usem ou comercializem a invenção sem autorização durante o período de vigência.",
        "explicacaoSimplificada": "É o direito exclusivo que a empresa que descobriu um novo fármaco tem de ser a única a fabricá-lo e vendê-lo por um determinado tempo, antes que outras empresas possam copiá-lo.",
        "aplicacaoPratica": "A expiração da patente de um fármaco de referência é o que permite a entrada legal de medicamentos genéricos e similares no mercado, geralmente associada a redução expressiva do preço final ao consumidor.",
        "atencao": "No Brasil, a patente farmacêutica tem prazo de vigência de 20 anos contados do depósito do pedido (Lei nº 9.279/1996), independentemente de quanto tempo ainda resta de proteção comercial efetiva após os anos consumidos em pesquisa e registro regulatório.",
        "termosRelacionados": ["generico", "nova-entidade-molecular"],
        "fontes": ["Lei nº 9.279/1996 (Lei de Propriedade Industrial)"]
    },
    {
        "id": "nome-comercial", "termo": "Nome Comercial", "categoria": "farmacologia-geral",
        "sinonimos": ["Nome de Fantasia", "Nome de Marca"],
        "definicao": "Designação comercial registrada por um fabricante para identificar e diferenciar seu medicamento no mercado, distinta da denominação genérica (DCB/DCI) do princípio ativo que ele contém.",
        "explicacaoSimplificada": "É o nome de marca do medicamento, criado pela empresa para fins comerciais, diferente do nome genérico do princípio ativo que está dentro do produto.",
        "aplicacaoPratica": "Um mesmo princípio ativo pode ser vendido sob diversos nomes comerciais diferentes por fabricantes distintos — o farmacêutico deve sempre confirmar o princípio ativo (DCB) por trás do nome comercial para evitar duplicação terapêutica.",
        "atencao": "A prescrição pelo nome comercial, em vez da DCB, é uma das causas de erro de dispensação e de duplicação terapêutica não percebida, especialmente quando o paciente usa o mesmo princípio ativo sob marcas diferentes prescritas por médicos distintos.",
        "termosRelacionados": ["dcb", "dci", "generico"],
        "fontes": ["Lei nº 9.787/1999 (Lei dos Genéricos)"]
    },
    {
        "id": "classificacao-atc", "termo": "Classificação ATC", "categoria": "farmacologia-geral",
        "sinonimos": ["Sistema ATC", "Anatomical Therapeutic Chemical"],
        "definicao": "Sistema de classificação de fármacos desenvolvido pela Organização Mundial da Saúde que organiza as substâncias ativas em cinco níveis hierárquicos, segundo o órgão ou sistema sobre o qual atuam, sua indicação terapêutica, seu mecanismo de ação e sua estrutura química.",
        "explicacaoSimplificada": "É um sistema internacional, criado pela OMS, que organiza os fármacos em grupos e subgrupos, como um grande índice que vai do mais geral (o sistema do corpo que o fármaco afeta) ao mais específico (a própria substância).",
        "aplicacaoPratica": "A classificação ATC é usada mundialmente em estudos de farmacoepidemiologia e farmacoeconomia para comparar padrões de consumo de medicamentos entre países e ao longo do tempo, geralmente junto com a métrica de Dose Diária Definida.",
        "atencao": "A classificação ATC é organizacional e epidemiológica, não regulatória — não deve ser confundida com a classificação de tarja ou de controle especial do medicamento, que segue critérios legais brasileiros distintos.",
        "termosRelacionados": ["dose-diaria-definida", "farmacoepidemiologia"],
        "fontes": ["OMS/WHO Collaborating Centre for Drug Statistics Methodology — ATC/DDD Index"]
    },
    {
        "id": "dose-diaria-definida", "termo": "Dose Diária Definida", "sigla": "DDD", "categoria": "farmacologia-geral",
        "sinonimos": ["Defined Daily Dose"],
        "definicao": "Unidade técnica de medida estabelecida pela Organização Mundial da Saúde que representa a dose média de manutenção diária de um fármaco quando utilizado em sua indicação principal em adultos, usada como padrão para comparar o consumo de medicamentos entre populações.",
        "explicacaoSimplificada": "É uma dose-padrão definida pela OMS para cada fármaco, usada para medir e comparar, de forma padronizada, quanto de um medicamento é consumido em diferentes lugares ou períodos — não é necessariamente a dose prescrita a um paciente individual.",
        "aplicacaoPratica": "A DDD é usada em estudos de utilização de medicamentos para estimar, por exemplo, o consumo de antimicrobianos por mil habitantes/dia em um hospital ou município, permitindo comparações entre instituições ao longo do tempo.",
        "atencao": "A DDD não deve ser usada como referência de dose terapêutica individual — é uma unidade estatística de comparação populacional, podendo diferir da dose real prescrita para um paciente específico.",
        "termosRelacionados": ["classificacao-atc", "farmacoepidemiologia"],
        "fontes": ["OMS/WHO Collaborating Centre for Drug Statistics Methodology — ATC/DDD Index"]
    },
    {
        "id": "ensaio-clinico-randomizado", "termo": "Ensaio Clínico Randomizado", "sigla": "ECR", "categoria": "farmacologia-geral",
        "sinonimos": ["Randomized Controlled Trial", "RCT"],
        "definicao": "Estudo experimental em que os participantes são alocados aleatoriamente entre um grupo que recebe a intervenção em estudo e um grupo controle, com o objetivo de minimizar viés de seleção e permitir inferência causal sobre a eficácia e a segurança do tratamento.",
        "explicacaoSimplificada": "É o tipo de estudo clínico considerado mais confiável para provar se um tratamento realmente funciona — os participantes são divididos em grupos por sorteio, para que os dois grupos fiquem o mais parecidos possível, exceto pelo tratamento recebido.",
        "aplicacaoPratica": "O ensaio clínico randomizado é considerado o padrão-ouro de evidência para aprovação regulatória de novos fármacos e para a elaboração de diretrizes clínicas baseadas em evidência.",
        "atencao": "Randomização não é sinônimo de cegamento: um estudo pode ser randomizado sem ser duplo-cego, e são conceitos metodológicos distintos, frequentemente cobrados separadamente em prova.",
        "termosRelacionados": ["duplo-cego", "grupo-controle", "vies-pesquisa-clinica"],
        "fontes": ["ICH E6(R2) — Good Clinical Practice", "DiPiro — Pharmacotherapy: A Pathophysiologic Approach"]
    },
    {
        "id": "grupo-controle", "termo": "Grupo Controle", "categoria": "farmacologia-geral",
        "sinonimos": ["Grupo Comparador"],
        "definicao": "Grupo de participantes de um estudo clínico que não recebe a intervenção experimental, recebendo placebo, tratamento padrão já estabelecido ou nenhuma intervenção, servindo de referência para avaliar o efeito real atribuível à intervenção testada no grupo experimental.",
        "explicacaoSimplificada": "É o grupo de comparação em uma pesquisa — enquanto um grupo recebe o tratamento que está sendo testado, o grupo controle recebe outra coisa, para saber se a diferença de resultado é realmente por causa do novo tratamento.",
        "aplicacaoPratica": "Quando já existe tratamento eficaz estabelecido para a condição, considerações éticas geralmente exigem que o grupo controle receba esse tratamento padrão (controle ativo) em vez de placebo, para não privar os participantes de terapia já comprovadamente eficaz.",
        "atencao": "Em contextos onde há tratamento eficaz disponível, o uso de placebo como controle, em vez de controle ativo, pode ser eticamente questionável — comitês de ética em pesquisa avaliam especificamente essa adequação antes de aprovar o protocolo.",
        "termosRelacionados": ["ensaio-clinico-randomizado", "placebo"],
        "fontes": ["ICH E6(R2) — Good Clinical Practice"]
    },
    {
        "id": "duplo-cego", "termo": "Duplo-Cego", "categoria": "farmacologia-geral",
        "sinonimos": ["Mascaramento Duplo", "Double-Blind"],
        "definicao": "Delineamento metodológico de estudo clínico em que tanto o participante quanto o pesquisador/avaliador desconhecem qual intervenção, experimental ou controle, está sendo administrada, com o objetivo de reduzir viés de expectativa em ambas as partes.",
        "explicacaoSimplificada": "É quando nem o paciente nem quem está avaliando o resultado sabem se o paciente recebeu o tratamento novo ou o controle — isso evita que a expectativa de qualquer um dos dois lados influencie o resultado.",
        "aplicacaoPratica": "O duplo-cego é especialmente importante em desfechos subjetivos, como intensidade de dor ou qualidade de vida, onde a expectativa do paciente ou a interpretação do avaliador poderiam favorecer o grupo experimental.",
        "atencao": "Duplo-cego é diferente de simples-cego, em que apenas o paciente ou apenas o avaliador desconhece a alocação, e de estudo aberto, em que nenhuma das partes é cega — distinção clássica cobrada em concursos de metodologia científica.",
        "termosRelacionados": ["ensaio-clinico-randomizado", "placebo", "vies-pesquisa-clinica"],
        "fontes": ["ICH E6(R2) — Good Clinical Practice"]
    },
    {
        "id": "vies-pesquisa-clinica", "termo": "Viés em Pesquisa Clínica", "categoria": "farmacologia-geral",
        "sinonimos": ["Bias"],
        "definicao": "Erro sistemático, não aleatório, introduzido no desenho, na condução, na análise ou na interpretação de um estudo, que distorce a estimativa do efeito real de uma intervenção, podendo favorecer conclusões falsamente positivas ou falsamente negativas.",
        "explicacaoSimplificada": "É um erro sistemático em uma pesquisa — algo que empurra o resultado para um lado, de forma consistente, e que não é apenas uma variação aleatória ao acaso.",
        "aplicacaoPratica": "Viés de seleção, viés de aferição e viés de confusão são os principais tipos avaliados na leitura crítica de artigos científicos, parte da avaliação de qualidade de uma evidência antes de incorporá-la à prática clínica.",
        "atencao": "Viés é diferente de erro aleatório: o viés é sistemático e direcional, enquanto o erro aleatório varia em ambas as direções e tende a se reduzir com o aumento do tamanho amostral — aumentar a amostra não corrige viés.",
        "termosRelacionados": ["ensaio-clinico-randomizado", "duplo-cego"],
        "fontes": ["DiPiro — Pharmacotherapy: A Pathophysiologic Approach"]
    },
    {
        "id": "estudo-pre-clinico", "termo": "Estudo Pré-Clínico", "categoria": "farmacologia-geral",
        "sinonimos": ["Fase Pré-Clínica", "Pesquisa Pré-Clínica"],
        "definicao": "Etapa de investigação de um novo fármaco realizada antes de sua administração em seres humanos, conduzida em modelos in vitro e em animais, destinada a avaliar farmacocinética, farmacodinâmica, toxicidade e segurança preliminar.",
        "explicacaoSimplificada": "É a fase de testes que acontece antes de o fármaco ser testado em pessoas, feita em laboratório e em animais, para ver se é seguro e se funciona como esperado antes de avançar para os estudos clínicos.",
        "aplicacaoPratica": "Os dados de toxicidade aguda, subcrônica, crônica, genotoxicidade e teratogenicidade obtidos nos estudos pré-clínicos são exigidos pelas agências regulatórias como pré-requisito para autorizar o início dos estudos clínicos em humanos.",
        "atencao": "Resultado favorável em estudo pré-clínico, incluindo em animais, não garante eficácia ou segurança em humanos — é uma etapa necessária, mas não suficiente, e muitos candidatos a fármaco falham nas fases clínicas apesar de resultados pré-clínicos promissores.",
        "termosRelacionados": ["fases-estudos-clinicos", "triagem-farmacologica"],
        "fontes": ["ICH M3(R2) — Nonclinical Safety Studies", "Katzung — Farmacologia Básica e Clínica"]
    },
    {
        "id": "fases-estudos-clinicos", "termo": "Fases dos Estudos Clínicos", "categoria": "farmacologia-geral",
        "sinonimos": ["Fases da Pesquisa Clínica", "Fase I", "Fase II", "Fase III", "Fase IV"],
        "definicao": "Sequência de quatro etapas (Fases I a IV) em que o desenvolvimento clínico de um novo fármaco é conduzido em seres humanos, progredindo de amostras pequenas focadas em segurança (Fase I) até estudos pós-comercialização em larga escala (Fase IV).",
        "explicacaoSimplificada": "É a linha do tempo dos testes em pessoas: Fase I testa segurança em poucos voluntários saudáveis; Fase II testa eficácia inicial em pacientes; Fase III confirma eficácia e segurança em grande número de pacientes antes do registro; Fase IV acompanha o fármaco já no mercado.",
        "aplicacaoPratica": "A farmacovigilância pós-comercialização (Fase IV) é o que permite detectar reações adversas raras que não apareceram nas fases anteriores, por envolver uma população muito maior e mais diversa.",
        "atencao": "A aprovação regulatória ocorre normalmente ao final da Fase III, não da Fase IV — a Fase IV é pós-comercialização e serve para vigilância contínua, não é pré-requisito para o fármaco já estar disponível no mercado.",
        "termosRelacionados": ["estudo-pre-clinico", "ensaio-clinico-randomizado", "farmacovigilancia-termo"],
        "fontes": ["ICH E8 — General Considerations for Clinical Trials", "Katzung — Farmacologia Básica e Clínica"]
    },
    {
        "id": "farmacologia-basica", "termo": "Farmacologia Básica", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Ramo da Farmacologia dedicado ao estudo dos mecanismos gerais de ação dos fármacos (farmacodinâmica) e de seu percurso no organismo (farmacocinética), geralmente investigado em modelos experimentais, independentemente de uma aplicação clínica imediata.",
        "explicacaoSimplificada": "É a parte da Farmacologia que estuda como o fármaco funciona por dentro, geralmente em laboratório, sem necessariamente estar ligada diretamente ao tratamento de um paciente específico.",
        "aplicacaoPratica": "O conhecimento de farmacologia básica (receptores, vias de sinalização, parâmetros farmacocinéticos) é o alicerce necessário para a farmacologia clínica, que aplica esse conhecimento à tomada de decisão terapêutica em pacientes reais.",
        "atencao": "Farmacologia básica não deve ser confundida com farmacologia clínica: a básica estuda mecanismos, muitas vezes em modelos experimentais, enquanto a clínica aplica esse conhecimento diretamente ao cuidado de pacientes.",
        "termosRelacionados": ["farmacologia-clinica", "farmacodinamica", "farmacocinetica"],
        "fontes": ["Katzung — Farmacologia Básica e Clínica"]
    },
    {
        "id": "farmacologia-clinica", "termo": "Farmacologia Clínica", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Ramo da Farmacologia que aplica os princípios farmacocinéticos e farmacodinâmicos ao cuidado direto do paciente, abrangendo seleção racional de fármacos, individualização posológica, monitorização terapêutica e avaliação de eficácia e segurança no contexto clínico real.",
        "explicacaoSimplificada": "É a parte da Farmacologia voltada para usar, na prática, com pacientes reais, tudo o que se sabe sobre como os fármacos agem e se movem no corpo, decidindo a melhor escolha e dose para cada situação.",
        "aplicacaoPratica": "O farmacêutico clínico aplica princípios de farmacologia clínica ao realizar ajuste posológico em insuficiência renal, monitorização terapêutica de fármacos de margem estreita e avaliação de interações medicamentosas em pacientes polimedicados.",
        "atencao": "Não confundir Farmacologia Clínica, a disciplina científica, com Farmácia Clínica, a prática assistencial do farmacêutico — são campos relacionados, mas com objetos e profissionais de formação distintos.",
        "termosRelacionados": ["farmacologia-basica", "farmacia-clinica-disciplina"],
        "fontes": ["Katzung — Farmacologia Básica e Clínica"]
    },
    {
        "id": "farmacologia-molecular", "termo": "Farmacologia Molecular", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Ramo da Farmacologia que estuda a interação entre fármacos e seus alvos moleculares (receptores, enzimas, canais iônicos, ácidos nucleicos) no nível atômico e molecular, incluindo estrutura tridimensional, cinética de ligação e vias de transdução de sinal.",
        "explicacaoSimplificada": "É a parte da Farmacologia que olha para o fármaco e seu alvo no nível mais microscópico possível — como as moléculas realmente se encaixam e interagem entre si.",
        "aplicacaoPratica": "O desenho racional de fármacos, baseado em estrutura cristalográfica de receptores e enzimas, é uma aplicação direta da farmacologia molecular, usada para otimizar a afinidade e a seletividade de novos candidatos a fármaco.",
        "atencao": "Farmacologia molecular trabalha no nível subcelular/atômico — diferente da farmacodinâmica geral, que descreve o efeito observável do fármaco no sistema biológico como um todo, sem necessariamente detalhar a interação molécula a molécula.",
        "termosRelacionados": ["farmacodinamica", "receptor"],
        "fontes": ["Rang & Dale — Farmacologia"]
    },
    {
        "id": "neurofarmacologia", "termo": "Neurofarmacologia", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Ramo da Farmacologia dedicado ao estudo dos efeitos dos fármacos sobre o sistema nervoso central e periférico, incluindo neurotransmissão, receptores neuronais e os mecanismos de ação de fármacos psicoativos, anestésicos, anticonvulsivantes e analgésicos centrais.",
        "explicacaoSimplificada": "É a parte da Farmacologia que estuda como os fármacos afetam o sistema nervoso, desde o cérebro até os nervos periféricos.",
        "aplicacaoPratica": "O entendimento neurofarmacológico dos sistemas de neurotransmissão dopaminérgico, serotoninérgico, GABAérgico e glutamatérgico fundamenta o uso racional de antipsicóticos, antidepressivos, benzodiazepínicos e anticonvulsivantes.",
        "atencao": "Neurofarmacologia é mais ampla que psicofarmacologia: a primeira abrange todo o sistema nervoso, incluindo dor, anestesia e movimento, enquanto a psicofarmacologia foca especificamente nos fármacos que afetam humor, cognição e comportamento.",
        "termosRelacionados": ["psicofarmacologia", "farmacodinamica"],
        "fontes": ["Rang & Dale — Farmacologia"]
    },
    {
        "id": "psicofarmacologia", "termo": "Psicofarmacologia", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Ramo da Farmacologia que estuda os efeitos dos fármacos sobre o humor, a cognição, a percepção e o comportamento, incluindo o mecanismo de ação de antidepressivos, antipsicóticos, ansiolíticos, estabilizadores de humor e substâncias psicoativas.",
        "explicacaoSimplificada": "É a parte da Farmacologia que estuda como os fármacos afetam o humor, os pensamentos e o comportamento das pessoas.",
        "aplicacaoPratica": "A psicofarmacologia fundamenta a farmacoterapia de transtornos como depressão, ansiedade, transtorno bipolar e esquizofrenia, orientando a escolha de classes farmacológicas conforme o perfil de neurotransmissores envolvido.",
        "atencao": "A resposta a psicofármacos costuma ter início de efeito tardio em relação ao início do uso — orientar o paciente sobre essa latência é essencial para a adesão ao tratamento e para evitar interrupção precoce por falta de efeito percebido.",
        "termosRelacionados": ["neurofarmacologia", "farmacovigilancia-termo"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "farmacologia-veterinaria", "termo": "Farmacologia Veterinária", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Ramo da Farmacologia dedicado ao estudo do uso de fármacos em animais, considerando diferenças farmacocinéticas e farmacodinâmicas entre espécies, uso de medicamentos de uso humano em animais e particularidades regulatórias de produtos veterinários.",
        "explicacaoSimplificada": "É a parte da Farmacologia que estuda o uso de medicamentos em animais, levando em conta que cada espécie pode reagir de forma diferente ao mesmo fármaco.",
        "aplicacaoPratica": "A diferença de metabolismo entre espécies explica por que certos fármacos seguros em humanos são extremamente tóxicos em animais específicos, como o paracetamol em gatos — conhecimento relevante quando o farmacêutico é consultado sobre produtos de natureza farmacêutica de uso animal.",
        "atencao": "Medicamentos de uso humano não devem ser extrapolados para uso animal sem orientação de médico-veterinário, já que diferenças de metabolismo entre espécies podem alterar radicalmente o perfil de segurança e eficácia.",
        "termosRelacionados": ["farmacocinetica"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "cronofarmacologia", "termo": "Cronofarmacologia", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Ramo da Farmacologia que estuda a influência dos ritmos biológicos, especialmente o ritmo circadiano, sobre a farmacocinética, a farmacodinâmica e a eficácia/toxicidade dos fármacos, buscando otimizar o horário de administração conforme esses ritmos.",
        "explicacaoSimplificada": "É a parte da Farmacologia que estuda como o horário do dia em que um fármaco é tomado pode influenciar sua eficácia e seus efeitos adversos, de acordo com o relógio biológico do corpo.",
        "aplicacaoPratica": "A administração de corticosteroides pela manhã, respeitando o pico circadiano natural do cortisol, e de estatinas à noite, horário de maior síntese hepática de colesterol, são exemplos de recomendações posológicas baseadas em cronofarmacologia.",
        "atencao": "A cronofarmacologia fundamenta recomendações de horário de administração que vão além da simples comodidade posológica — ignorar esse racional pode reduzir a eficácia terapêutica ou aumentar efeitos adversos, mesmo com a dose total diária correta.",
        "termosRelacionados": ["ritmo-circadiano", "farmacocinetica"],
        "fontes": ["Guyton & Hall — Tratado de Fisiologia Médica"]
    },
    {
        "id": "potencial-abuso", "termo": "Potencial de Abuso", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Propriedade farmacológica de uma substância relacionada à sua capacidade de produzir efeitos reforçadores (euforia, bem-estar intenso) que favorecem o uso repetido não terapêutico e o desenvolvimento de dependência, utilizada como critério para classificação de medicamentos controlados.",
        "explicacaoSimplificada": "É a capacidade que uma substância tem de levar a pessoa a querer usá-la repetidamente, de forma não médica, por causa do efeito agradável que ela provoca — é esse risco que justifica o controle especial de certos medicamentos.",
        "aplicacaoPratica": "O potencial de abuso de uma substância é um dos critérios técnicos usados pela Anvisa para incluí-la nas listas de substâncias sujeitas a controle especial, junto com seu potencial de causar dependência física e/ou psíquica.",
        "atencao": "Potencial de abuso não é o mesmo que dependência já instalada: é uma propriedade farmacológica da substância, enquanto a dependência é a condição clínica que pode, ou não, se desenvolver no indivíduo que a utiliza.",
        "termosRelacionados": ["medicamento-controlado", "sindrome-abstinencia"],
        "fontes": ["Portaria SVS/MS nº 344/1998"]
    },
    {
        "id": "tolerancia-cruzada", "termo": "Tolerância Cruzada", "categoria": "farmacologia-geral",
        "sinonimos": ["Cross-Tolerance"],
        "definicao": "Fenômeno em que a tolerância desenvolvida ao uso repetido de uma substância se estende a outra substância, geralmente da mesma classe farmacológica ou que atua sobre o mesmo sistema de receptores, reduzindo a resposta a ambas mesmo sem exposição prévia à segunda substância.",
        "explicacaoSimplificada": "É quando a resistência que o corpo desenvolveu a uma substância, por uso repetido, também diminui o efeito de outra substância parecida, mesmo que essa segunda nunca tenha sido usada antes.",
        "aplicacaoPratica": "A tolerância cruzada entre álcool e benzodiazepínicos é relevante na prática clínica: pacientes com uso crônico de álcool frequentemente necessitam de doses maiores de benzodiazepínicos para sedação, por atuarem sobre o mesmo sistema receptor GABAérgico.",
        "atencao": "Tolerância cruzada é diferente de tolerância simples, à mesma substância — a cruzada se estende a outras substâncias do mesmo mecanismo, com implicações práticas diretas no ajuste de dose de anestésicos e sedativos em usuários crônicos de álcool ou opioides.",
        "termosRelacionados": ["tolerancia", "dependencia-farmacologica"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "sensibilizacao-farmacologica", "termo": "Sensibilização Farmacológica", "categoria": "farmacologia-geral",
        "sinonimos": ["Sensibilização"],
        "definicao": "Fenômeno farmacodinâmico em que a resposta a doses repetidas de uma substância aumenta progressivamente ao longo do tempo, processo inverso à tolerância, geralmente associado a mecanismos de neuroadaptação em vias específicas.",
        "explicacaoSimplificada": "É o efeito contrário da tolerância — em vez de precisar de doses cada vez maiores para sentir o mesmo efeito, a pessoa passa a sentir um efeito cada vez mais forte com a mesma dose, ou até com doses menores.",
        "aplicacaoPratica": "A sensibilização comportamental a estimulantes, como anfetaminas e cocaína, é um fenômeno estudado na farmacologia do abuso de substâncias, relacionado ao desenvolvimento de certos padrões comportamentais com o uso repetido.",
        "atencao": "Não confundir com dessensibilização, a redução da resposta de um receptor por exposição contínua a um agonista, fenômeno farmacodinâmico distinto — sensibilização e dessensibilização são processos opostos e ocorrem em contextos diferentes.",
        "termosRelacionados": ["dessensibilizacao", "tolerancia"],
        "fontes": ["Goodman & Gilman — As Bases Farmacológicas da Terapêutica"]
    },
    {
        "id": "terapia-combinada", "termo": "Terapia Combinada", "categoria": "farmacologia-geral",
        "sinonimos": ["Associação Medicamentosa", "Terapia de Combinação"],
        "definicao": "Estratégia terapêutica que utiliza dois ou mais fármacos simultaneamente, com o objetivo de obter efeito sinérgico ou aditivo, ampliar o espectro de ação, reduzir a dose individual de cada fármaco ou prevenir o desenvolvimento de resistência.",
        "explicacaoSimplificada": "É quando se usa dois ou mais medicamentos juntos, de forma planejada, para obter um efeito melhor do que cada um sozinho, ou para reduzir a chance de resistência ao tratamento.",
        "aplicacaoPratica": "O tratamento da tuberculose (esquema RIPE) e da hipertensão arterial resistente são exemplos clássicos de terapia combinada na prática farmacêutica, cada um com racional farmacológico próprio para a associação.",
        "atencao": "Terapia combinada planejada e racional é diferente de polifarmácia não criteriosa — a primeira tem embasamento farmacológico específico para a associação; a segunda frequentemente reflete acúmulo não revisado de prescrições.",
        "termosRelacionados": ["monoterapia", "poliquimioterapia", "polimedicacao"],
        "fontes": ["Katzung — Farmacologia Básica e Clínica"]
    },
    {
        "id": "monoterapia", "termo": "Monoterapia", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Estratégia terapêutica que utiliza um único fármaco para o tratamento de uma condição clínica, geralmente adotada como abordagem inicial antes de considerar a associação de outros fármacos, quando a resposta à monoterapia é insuficiente.",
        "explicacaoSimplificada": "É tratar uma condição usando apenas um medicamento, em vez de combinar vários.",
        "aplicacaoPratica": "Diretrizes de hipertensão arterial e de epilepsia frequentemente recomendam iniciar o tratamento em monoterapia, avançando para terapia combinada apenas se o controle não for atingido com doses adequadas do primeiro fármaco.",
        "atencao": "A escalada de monoterapia para terapia combinada deve respeitar doses adequadas e tempo suficiente de resposta antes de ser considerada falha — trocar ou associar fármacos prematuramente pode mascarar uma monoterapia ainda não otimizada.",
        "termosRelacionados": ["terapia-combinada", "linha-tratamento"],
        "fontes": ["Diretriz Brasileira de Hipertensão Arterial (SBC)"]
    },
    {
        "id": "linha-tratamento", "termo": "Linha de Tratamento", "categoria": "farmacologia-geral",
        "sinonimos": ["Fármaco de Primeira Linha", "Terapia de Primeira Linha"],
        "definicao": "Classificação hierárquica dos fármacos ou esquemas terapêuticos recomendados para uma condição clínica, segundo diretrizes baseadas em evidência, em que a primeira linha representa a opção inicial preferencial e as linhas subsequentes são reservadas para falha, intolerância ou contraindicação às anteriores.",
        "explicacaoSimplificada": "É a ordem de preferência dos tratamentos para uma doença — o de primeira linha é o que se tenta primeiro; se não funcionar ou não for tolerado, passa-se para a segunda linha, e assim por diante.",
        "aplicacaoPratica": "Em diretrizes clínicas, a classificação por linha de tratamento orienta a prescrição racional e também fundamenta decisões de incorporação de medicamentos nas listas do SUS e em protocolos clínicos institucionais.",
        "atencao": "A linha de tratamento recomendada pode variar conforme características do paciente, como comorbidades, contraindicações e disponibilidade — primeira linha não é uma regra absoluta e universal, mas uma recomendação geral ajustável à individualidade clínica.",
        "termosRelacionados": ["monoterapia", "terapia-combinada"],
        "fontes": ["Diretrizes clínicas baseadas em evidência (ex.: SBC, SBD, Ministério da Saúde)"]
    },
    {
        "id": "farmaco-resgate", "termo": "Fármaco de Resgate", "categoria": "farmacologia-geral",
        "sinonimos": ["Medicação de Resgate", "Rescue Drug"],
        "definicao": "Fármaco utilizado para alívio rápido de sintomas agudos ou de crises, administrado conforme a necessidade, em complemento ao tratamento de manutenção/controle regular, e não como terapia contínua de base.",
        "explicacaoSimplificada": "É o medicamento usado na hora da crise, para alívio rápido de um sintoma, diferente do medicamento usado todos os dias para controlar a doença de base.",
        "aplicacaoPratica": "O broncodilatador de curta duração usado na crise de asma é o fármaco de resgate, diferente do corticosteroide inalatório de uso diário, o fármaco de manutenção — confundir os dois papéis é um erro frequente de adesão que compromete o controle da doença.",
        "atencao": "Uso excessivo do fármaco de resgate é um sinal de alerta de controle inadequado da doença de base e deve motivar reavaliação do tratamento de manutenção, não apenas reposição da medicação de resgate.",
        "termosRelacionados": ["asma", "terapia-combinada"],
        "fontes": ["GINA — Global Initiative for Asthma"]
    },
    {
        "id": "equivalencia-farmaceutica", "termo": "Equivalência Farmacêutica", "categoria": "farmacologia-geral",
        "sinonimos": [],
        "definicao": "Relação entre dois medicamentos que contêm o mesmo princípio ativo, na mesma dose, forma farmacêutica e via de administração, atendendo às mesmas especificações farmacopeicas de qualidade, mas não necessariamente com comprovação de perfil de absorção equivalente.",
        "explicacaoSimplificada": "É quando dois medicamentos têm o mesmo princípio ativo, na mesma dose e na mesma forma farmacêutica — mas isso, por si só, não garante que o corpo vai absorver os dois da mesma maneira.",
        "aplicacaoPratica": "Equivalência farmacêutica é o primeiro requisito avaliado no processo de registro de medicamentos genéricos e similares, mas a intercambialidade com o medicamento de referência só é conferida após a comprovação adicional de bioequivalência.",
        "atencao": "Equivalência farmacêutica não implica automaticamente intercambialidade — dois produtos podem ser equivalentes farmacêuticos e, ainda assim, não serem bioequivalentes, caso apresentem diferenças relevantes de biodisponibilidade.",
        "termosRelacionados": ["bioequivalencia", "intercambialidade", "generico"],
        "fontes": ["RDC Anvisa nº 58/2014"]
    },
    {
        "id": "sindrome-abstinencia", "termo": "Síndrome de Abstinência", "categoria": "farmacologia-geral",
        "sinonimos": ["Síndrome de Retirada", "Withdrawal Syndrome"],
        "definicao": "Conjunto de sinais e sintomas físicos e/ou psíquicos que surge após a interrupção abrupta ou a redução significativa da dose de uma substância à qual o organismo desenvolveu dependência física, geralmente com características opostas aos efeitos farmacológicos originais da substância.",
        "explicacaoSimplificada": "É o conjunto de sintomas que aparece quando uma pessoa para de usar, ou reduz muito, uma substância à qual o corpo já tinha se acostumado, geralmente sentindo o contrário do que a substância causava.",
        "aplicacaoPratica": "A retirada abrupta de benzodiazepínicos pode provocar síndrome de abstinência com ansiedade rebote, insônia e, em casos graves, convulsões — por isso a descontinuação desses fármacos deve ser feita por redução gradual, nunca de forma abrupta.",
        "atencao": "O risco e a gravidade da síndrome de abstinência variam conforme a substância, a dose, o tempo de uso e a velocidade da descontinuação — a orientação de desmame gradual, quando indicada, é uma intervenção farmacêutica importante para prevenir essa complicação.",
        "termosRelacionados": ["dependencia-farmacologica", "tolerancia-cruzada", "benzodiazepinicos"],
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

    novos_ids = [t["id"] for t in NOVOS_TERMOS]
    if len(novos_ids) != len(set(novos_ids)):
        sys.exit("ERRO: ids duplicados dentro do próprio lote novo.")

    if len(NOVOS_TERMOS) != 40:
        sys.exit(f"ERRO: esperado exatamente 40 termos, encontrado {len(NOVOS_TERMOS)}.")

    for t in NOVOS_TERMOS:
        if t["id"] in ids_existentes:
            sys.exit(f"ERRO: id já existe no banco: {t['id']}")
        if t["categoria"] not in cat_ids_validas:
            sys.exit(f"ERRO: categoria inválida em {t['id']}: {t['categoria']}")
        if t["categoria"] != "farmacologia-geral":
            sys.exit(f"ERRO: termo fora da categoria farmacologia-geral: {t['id']}")
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

    print(f"OK: {len(NOVOS_TERMOS)} termos adicionados a farmacologia-geral.")
    print(f"Total de termos no banco: {total_antes} -> {len(data['termos'])}")


if __name__ == "__main__":
    main()
