import json, io

PATH = "dicionario/dicionario.json"
with io.open(PATH, encoding="utf-8") as f:
    data = json.load(f)

VALID_CATS = {c["id"] for c in data["categorias"]}
existing_ids = {t["id"] for t in data["termos"]}
CAT = "vigilancia-sanitaria"

novos = [
  dict(id="autorizacao-especial", termo="AE (Autorização Especial)", categoria=CAT,
    sinonimos=["AE"],
    definicao="Autorização emitida pela Anvisa para empresas que fabricam, importam, exportam, distribuem ou comercializam substâncias sujeitas a controle especial (listas da Portaria SVS/MS nº 344/1998), complementar à AFE, específica para operações com essas substâncias.",
    explicacaoSimplificada="É uma autorização extra, além da AFE, exigida para empresas que trabalham com substâncias controladas (como psicotrópicos e entorpecentes).",
    aplicacaoPratica="Uma farmácia que manipula medicamentos com substâncias da lista A1 precisa, além da AFE, de uma AE específica para essa atividade, renovada periodicamente junto à Anvisa.",
    atencao="A AE é exigida por substância/atividade específica, não substitui a AFE — uma empresa pode ter AFE válida e ainda não ter a AE necessária para uma substância controlada específica.",
    naoConfunda=["autorizacao-funcionamento"],
    termosRelacionados=["autorizacao-funcionamento","medicamento-controlado"],
    fontes=["Portaria SVS/MS nº 344/1998","Anvisa"]),

  dict(id="licenca-sanitaria", termo="Licença Sanitária / Alvará Sanitário", categoria=CAT,
    sinonimos=["Alvará Sanitário","Licença de Funcionamento"],
    definicao="Documento emitido pelo órgão de vigilância sanitária estadual ou municipal que autoriza o funcionamento de um estabelecimento (como farmácia ou drogaria) em determinado endereço, condicionado ao cumprimento de requisitos sanitários locais, com validade e renovação periódica definidas pela legislação estadual/municipal.",
    explicacaoSimplificada="É a autorização, dada pela vigilância sanitária da prefeitura ou do estado, para que o estabelecimento funcione naquele endereço.",
    aplicacaoPratica="Antes de abrir as portas, uma nova drogaria precisa obter a licença sanitária municipal, que inclui vistoria do estabelecimento pela vigilância sanitária local.",
    atencao="A Licença Sanitária é de competência estadual/municipal e distinta da AFE, que é federal (Anvisa) — um estabelecimento pode precisar das duas simultaneamente, pois regulam esferas diferentes.",
    naoConfunda=["autorizacao-funcionamento"],
    termosRelacionados=["autorizacao-funcionamento","responsavel-tecnico"],
    fontes=["Lei nº 6.437/1977","Legislação sanitária estadual/municipal"]),

  dict(id="certificado-boas-praticas", termo="Certificado de Boas Práticas (CBP)", categoria=CAT,
    sinonimos=["CBP","Certificado de Conformidade com as BPF"],
    definicao="Documento emitido pela Anvisa que atesta, após inspeção, que uma linha de produção ou unidade fabril cumpre as Boas Práticas de Fabricação (BPF) vigentes, sendo pré-requisito para a concessão e manutenção do registro de medicamentos fabricados naquela unidade.",
    explicacaoSimplificada="É o documento que comprova, depois de uma inspeção, que a fábrica segue as Boas Práticas de Fabricação.",
    aplicacaoPratica="Antes de registrar um novo medicamento, a empresa precisa comprovar que a linha de produção onde ele será fabricado possui CBP válido para aquela forma farmacêutica.",
    atencao="O CBP tem validade determinada e é específico por linha de produção/forma farmacêutica — não é um certificado único e genérico para toda a fábrica.",
    naoConfunda=[],
    termosRelacionados=["boas-praticas-fabricacao","registro-sanitario-medicamentos"],
    fontes=["RDC Anvisa nº 658/2022"]),

  dict(id="notificacao-sanitaria", termo="Notificação Sanitária", categoria=CAT,
    sinonimos=[],
    definicao="Regime simplificado de regularização, no qual determinados produtos de baixo risco (como alguns cosméticos de Grau 1) podem ser comercializados mediante simples notificação à Anvisa, sem necessidade de análise prévia e concessão de registro.",
    explicacaoSimplificada="É um jeito mais simples de regularizar produtos de baixo risco — a empresa só avisa a Anvisa que vai vender o produto, sem esperar uma análise prévia.",
    aplicacaoPratica="Um sabonete líquido comum (cosmético Grau 1) é comercializado por notificação sanitária, enquanto um protetor solar (Grau 2, maior risco) exige registro com análise prévia da Anvisa.",
    atencao="A notificação sanitária não dispensa a empresa de cumprir todas as exigências técnicas e de qualidade — a Anvisa pode fiscalizar e exigir adequações a qualquer momento, mesmo sem análise prévia.",
    naoConfunda=["registro-sanitario-medicamentos"],
    termosRelacionados=["registro-sanitario-medicamentos","vigilancia-sanitaria-termo"],
    fontes=["RDC Anvisa nº 07/2015 (cosméticos)"]),

  dict(id="dossie-tecnico-regularizacao", termo="Dossiê Técnico de Regularização", categoria=CAT,
    sinonimos=["Dossiê de Registro"],
    definicao="Conjunto estruturado de documentos técnicos e científicos exigido pela Anvisa para instruir um processo de registro, notificação, alteração ou renovação de um produto sujeito à vigilância sanitária, demonstrando sua qualidade, segurança e eficácia.",
    explicacaoSimplificada="É a pasta/arquivo completo com todos os documentos e estudos que comprovam que o produto é seguro e de qualidade, exigido para regularizar o produto junto à Anvisa.",
    aplicacaoPratica="O dossiê técnico de registro de um medicamento genérico inclui estudos de bioequivalência, especificações farmacopeicas e dados de estabilidade, entre outros documentos exigidos pela Anvisa.",
    atencao="O conteúdo exigido no dossiê varia conforme a categoria regulatória do produto (medicamento novo, genérico, similar, cosmético, etc.) — não existe um dossiê-padrão único para todos os casos.",
    naoConfunda=[],
    termosRelacionados=["registro-sanitario-medicamentos","estudo-estabilidade"],
    fontes=["Anvisa"]),

  dict(id="instrucao-normativa", termo="Norma Regulamentadora / Instrução Normativa (IN)", categoria=CAT,
    sinonimos=["IN","Norma Regulamentadora"],
    definicao="Ato normativo editado por um órgão regulador (como a Anvisa) para detalhar, operacionalizar ou esclarecer a aplicação prática de uma resolução (RDC) ou lei, geralmente tratando de aspectos técnicos, prazos ou procedimentos específicos.",
    explicacaoSimplificada="É uma norma mais detalhada que explica como aplicar na prática uma RDC ou uma lei.",
    aplicacaoPratica="Uma RDC estabelece a obrigatoriedade de um novo sistema de rastreamento, e uma Instrução Normativa publicada depois detalha o cronograma de implementação e os formatos técnicos exigidos.",
    atencao="A IN não cria obrigação nova por si só na mesma hierarquia de uma RDC ou lei — ela detalha/operacionaliza uma norma hierarquicamente superior já existente.",
    naoConfunda=["rdc"],
    termosRelacionados=["rdc","anvisa"],
    fontes=["Lei Complementar nº 95/1998"]),

  dict(id="bpdf", termo="BPDF (Boas Práticas de Distribuição e Fracionamento)", categoria=CAT,
    sinonimos=["Boas Práticas de Distribuição e Fracionamento"],
    definicao="Conjunto de normas sanitárias que regulam especificamente as operações de fracionamento (divisão de lotes em quantidades menores) e distribuição de medicamentos e insumos farmacêuticos, complementando as BPDA nos casos em que há fracionamento do produto.",
    explicacaoSimplificada="São as regras específicas para quando um lote de medicamento é dividido (fracionado) em quantidades menores, além das regras de distribuição.",
    aplicacaoPratica="Um distribuidor que fraciona um lote de insumo farmacêutico ativo para atender pedidos menores precisa seguir as BPDF, documentando e rastreando cada fração gerada a partir do lote original.",
    atencao="Não confundir BPDF (fracionamento) com BPDA (armazenagem/distribuição sem fracionamento) — a BPDF é exigida especificamente quando há divisão física do lote, e não em toda operação de distribuição.",
    naoConfunda=["bpda"],
    termosRelacionados=["bpda","rastreabilidade"],
    fontes=["RDC Anvisa nº 430/2020"]),

  dict(id="bpfm", termo="BPFM (Boas Práticas de Manipulação)", categoria=CAT,
    sinonimos=["Boas Práticas de Manipulação"],
    definicao="Conjunto de normas sanitárias que regulam a manipulação de fórmulas magistrais e oficinais em farmácias de manipulação, abrangendo instalações, equipamentos, pessoal, controle de qualidade e documentação do processo de manipulação.",
    explicacaoSimplificada="São as regras de qualidade e segurança para farmácias que preparam fórmulas manipuladas (não industriais).",
    aplicacaoPratica="Uma farmácia de manipulação deve seguir as BPFM ao preparar uma cápsula manipulada, incluindo pesagem calibrada, registro de lote da fórmula e controle de qualidade da matéria-prima utilizada.",
    atencao="As BPFM se aplicam à manipulação magistral/oficinal em farmácia, enquanto as BPF (Boas Práticas de Fabricação) se aplicam à produção industrial em escala — são regimes regulatórios distintos, com normas próprias.",
    naoConfunda=["boas-praticas-fabricacao"],
    termosRelacionados=["boas-praticas-fabricacao","responsavel-tecnico"],
    fontes=["RDC Anvisa nº 67/2007"]),

  dict(id="gerenciamento-risco-sanitario", termo="Gerenciamento de Risco Sanitário (GRS)", categoria=CAT,
    sinonimos=["GRS"],
    definicao="Abordagem regulatória que prioriza as ações de vigilância sanitária (fiscalização, inspeção, educação) com base no grau de risco que produtos, serviços e estabelecimentos representam à saúde da população, concentrando recursos onde o risco é maior.",
    explicacaoSimplificada="É a estratégia da vigilância sanitária de focar a fiscalização onde o risco à saúde da população é maior.",
    aplicacaoPratica="Um hospital classificado como de alto risco sanitário recebe inspeções mais frequentes da vigilância sanitária do que uma farmácia de pequeno porte classificada como baixo risco.",
    atencao="Gerenciamento de Risco Sanitário (classificação de risco de estabelecimentos/produtos pela vigilância sanitária) é diferente de Gerenciamento de Risco em saúde/farmacovigilância (prevenção de erros de medicação em um processo assistencial específico) — o termo \"risco\" é compartilhado, mas o escopo é outro.",
    naoConfunda=["gerenciamento-risco"],
    termosRelacionados=["vigilancia-sanitaria-termo","roteiro-inspecao-sanitaria"],
    fontes=["Anvisa"]),

  dict(id="estudo-estabilidade", termo="Estudo de Estabilidade", categoria=CAT,
    sinonimos=["Estudo de Estabilidade de Longa Duração","Estudo de Estabilidade Acelerado"],
    definicao="Programa estruturado de testes (de longa duração, acelerado e, quando aplicável, de fotoestabilidade), conduzido conforme guias técnicos (ICH Q1A), para determinar como a qualidade de um medicamento varia com o tempo sob a influência de fatores ambientais, definindo seu prazo de validade e condições de armazenamento.",
    explicacaoSimplificada="São os testes feitos ao longo do tempo para descobrir até quando o medicamento continua bom e em que condições ele deve ser guardado.",
    aplicacaoPratica="Para definir a validade de 24 meses de um novo comprimido, o fabricante conduz um estudo de estabilidade de longa duração (condições normais, ao longo de todo esse período) e um estudo acelerado (condições mais extremas, por tempo menor, para estimativa preliminar).",
    atencao="O estudo de estabilidade é o programa de testes que determina o prazo de validade; a Estabilidade (Farmacotécnica) propriamente dita é a característica/propriedade do medicamento que esse estudo avalia — são conceitos relacionados, mas não sinônimos.",
    naoConfunda=["estabilidade-farmaceutica"],
    termosRelacionados=["estabilidade-farmaceutica","dossie-tecnico-regularizacao"],
    fontes=["ICH Q1A(R2)","Anvisa"]),

  dict(id="cosmetovigilancia", termo="Cosmetovigilância", categoria=CAT,
    sinonimos=[],
    definicao="Sistema de monitoramento de eventos adversos relacionados ao uso de produtos cosméticos, com coleta, análise e investigação de notificações para identificar riscos à saúde associados a esses produtos e subsidiar ações regulatórias.",
    explicacaoSimplificada="É a farmacovigilância aplicada a cosméticos — o monitoramento de reações e problemas causados por produtos de higiene e beleza.",
    aplicacaoPratica="Um consumidor relata irritação cutânea grave após o uso de um creme cosmético; a notificação à Anvisa, dentro do sistema de cosmetovigilância, pode levar à investigação do lote e, se confirmado o risco, a um recall do produto.",
    atencao="Cosmetovigilância, Farmacovigilância e Nutrivigilância seguem a mesma lógica de monitoramento pós-comercialização, mas são sistemas distintos, cada um voltado a uma categoria de produto (cosméticos, medicamentos e alimentos/suplementos, respectivamente).",
    naoConfunda=["farmacovigilancia-termo","nutrivigilancia"],
    termosRelacionados=["farmacovigilancia-termo","nutrivigilancia","notivisa"],
    fontes=["Anvisa"]),

  dict(id="nutrivigilancia", termo="Nutrivigilância", categoria=CAT,
    sinonimos=[],
    definicao="Sistema de monitoramento de eventos adversos e queixas técnicas relacionados ao consumo de alimentos, incluindo suplementos alimentares, com coleta e investigação de notificações para subsidiar ações regulatórias de segurança alimentar.",
    explicacaoSimplificada="É a farmacovigilância aplicada a alimentos e suplementos alimentares — o monitoramento de problemas causados por esses produtos.",
    aplicacaoPratica="Vários consumidores relatam mal-estar após o consumo de um suplemento alimentar do mesmo lote; as notificações, registradas no sistema de nutrivigilância, orientam a investigação da Anvisa sobre possível contaminação ou desvio de qualidade.",
    atencao="A nutrivigilância cobre tanto alimentos convencionais quanto suplementos alimentares, categoria que passou a ter regulação própria e mais detalhada da Anvisa a partir de 2018 (RDC nº 243/2018).",
    naoConfunda=["farmacovigilancia-termo","cosmetovigilancia"],
    termosRelacionados=["farmacovigilancia-termo","cosmetovigilancia","notivisa"],
    fontes=["Anvisa","RDC Anvisa nº 243/2018"]),

  dict(id="notivisa", termo="Notivisa", categoria=CAT,
    sinonimos=["Sistema Nacional de Notificações para a Vigilância Sanitária"],
    definicao="Sistema eletrônico oficial da Anvisa utilizado para o registro e o gerenciamento de notificações de eventos adversos, queixas técnicas e outras ocorrências relacionadas a produtos sujeitos à vigilância sanitária (medicamentos, cosméticos, alimentos, produtos para saúde, entre outros).",
    explicacaoSimplificada="É o sistema online onde se registram as notificações de problemas com produtos regulados pela Anvisa (reações, queixas técnicas, etc.).",
    aplicacaoPratica="Um farmacêutico que identifica uma queixa técnica em um lote de medicamento registra a ocorrência no Notivisa, alimentando o sistema de farmacovigilância/tecnovigilância da Anvisa.",
    atencao="O Notivisa é a ferramenta/sistema onde as notificações são registradas; a Farmacovigilância, a Tecnovigilância, a Cosmetovigilância e a Nutrivigilância são os diferentes programas de monitoramento que utilizam esse sistema para coletar dados.",
    naoConfunda=[],
    termosRelacionados=["farmacovigilancia-termo","tecnovigilancia","cosmetovigilancia","nutrivigilancia"],
    fontes=["Anvisa - Notivisa"]),

  dict(id="recall-recolhimento", termo="Recall (Recolhimento de Produto)", categoria=CAT,
    sinonimos=["Recolhimento de Produto","Recall Sanitário"],
    definicao="Procedimento formal de retirada do mercado de um produto que apresenta risco à saúde (desvio de qualidade grave, contaminação, erro de rotulagem, entre outros), determinado pela empresa fabricante/detentora do registro ou pela autoridade sanitária, com comunicação pública e rastreamento dos lotes afetados.",
    explicacaoSimplificada="É a retirada forçada ou voluntária de um produto do mercado, porque ele representa risco à saúde.",
    aplicacaoPratica="Ao identificar contaminação microbiológica em um lote de colírio, a empresa inicia o recall do lote afetado, comunicando distribuidores, farmácias e o público, e orientando o farmacêutico a retirar o produto das prateleiras e orientar pacientes que já o adquiriram.",
    atencao="O recall é diferente da simples devolução de produto ao fornecedor (que pode ocorrer por motivos comerciais ou de vencimento) — o recall é uma ação regulatória formal, acionada por risco à saúde, com rastreamento obrigatório dos lotes.",
    naoConfunda=["devolucao-produto"],
    termosRelacionados=["alerta-sanitario","rastreabilidade","nao-conformidade"],
    fontes=["Anvisa"]),

  dict(id="alerta-sanitario", termo="Alerta Sanitário", categoria=CAT,
    sinonimos=[],
    definicao="Comunicação oficial emitida pela Anvisa (ou outro órgão de vigilância sanitária) para informar rapidamente profissionais de saúde e a população sobre um risco identificado relacionado a um produto ou prática, podendo preceder ou acompanhar um recall.",
    explicacaoSimplificada="É um aviso oficial e rápido da Anvisa sobre um risco relacionado a um produto.",
    aplicacaoPratica="A Anvisa publica um alerta sanitário informando sobre a falsificação de um medicamento específico circulando no mercado, orientando farmacêuticos a verificarem a procedência antes da dispensação.",
    atencao="Um alerta sanitário não implica necessariamente um recall formal do produto — pode ser apenas um aviso informativo sobre um risco identificado, sem necessariamente determinar o recolhimento imediato de lotes.",
    naoConfunda=["recall-recolhimento"],
    termosRelacionados=["recall-recolhimento","notivisa"],
    fontes=["Anvisa"]),

  dict(id="auto-infracao-sanitaria", termo="Auto de Infração Sanitária (AIS)", categoria=CAT,
    sinonimos=["AIS"],
    definicao="Documento administrativo formal, lavrado pelo agente fiscal da vigilância sanitária, que registra a constatação de uma infração à legislação sanitária durante uma inspeção, dando início ao processo administrativo sanitário que pode resultar em penalidade.",
    explicacaoSimplificada="É o documento que registra oficialmente que uma infração sanitária foi constatada durante uma fiscalização.",
    aplicacaoPratica="Durante uma inspeção, o fiscal da vigilância sanitária constata que a farmácia armazena medicamentos termolábeis fora da cadeia de frio e lavra um Auto de Infração Sanitária, iniciando o processo administrativo correspondente.",
    atencao="O Auto de Infração Sanitária registra a constatação da infração; a penalidade propriamente dita (multa, interdição, cancelamento de licença) é definida posteriormente, no Auto de Imposição de Penalidade, após o processo administrativo garantir direito de defesa.",
    naoConfunda=["auto-imposicao-penalidade"],
    termosRelacionados=["auto-imposicao-penalidade","roteiro-inspecao-sanitaria"],
    fontes=["Lei nº 6.437/1977"]),

  dict(id="auto-imposicao-penalidade", termo="Auto de Imposição de Penalidade (AIP)", categoria=CAT,
    sinonimos=["AIP"],
    definicao="Documento administrativo que formaliza a aplicação de uma sanção sanitária (advertência, multa, interdição, cancelamento de licença/autorização, entre outras previstas em lei) a um estabelecimento ou pessoa, emitido após o processo administrativo decorrente de um Auto de Infração Sanitária.",
    explicacaoSimplificada="É o documento que aplica, de fato, a punição depois que a infração sanitária foi apurada e o processo administrativo concluído.",
    aplicacaoPratica="Após o processo administrativo decorrente do Auto de Infração Sanitária, a vigilância sanitária emite um Auto de Imposição de Penalidade determinando multa ao estabelecimento infrator.",
    atencao="A gradação e o tipo de penalidade (advertência, multa, interdição, cancelamento) dependem da gravidade da infração e de reincidência, conforme previsto na Lei nº 6.437/1977 — não é uma sanção automática e uniforme para toda infração.",
    naoConfunda=["auto-infracao-sanitaria"],
    termosRelacionados=["auto-infracao-sanitaria","termo-interdicao-cautelar"],
    fontes=["Lei nº 6.437/1977"]),

  dict(id="termo-interdicao-cautelar", termo="Termo de Interdição Cautelar", categoria=CAT,
    sinonimos=["Interdição Cautelar"],
    definicao="Medida administrativa de caráter preventivo e temporário, aplicada pela vigilância sanitária para impedir imediatamente a fabricação, distribuição, comercialização ou uso de um produto, equipamento ou estabelecimento, quando há risco iminente à saúde, independentemente da conclusão do processo administrativo sanitário.",
    explicacaoSimplificada="É uma medida de emergência que proíbe imediatamente o uso/venda de algo, por risco iminente à saúde, mesmo antes de o processo terminar.",
    aplicacaoPratica="Ao identificar um lote de medicamento com forte suspeita de contaminação, a vigilância sanitária lavra um Termo de Interdição Cautelar, proibindo imediatamente sua comercialização enquanto a investigação prossegue.",
    atencao="Por ser cautelar, essa medida é aplicada antes da conclusão do processo administrativo, justamente para conter o risco imediatamente — não se confunde com a penalidade final, que só vem após o processo (Auto de Imposição de Penalidade).",
    naoConfunda=["auto-imposicao-penalidade"],
    termosRelacionados=["apreensao-inutilizacao","auto-infracao-sanitaria"],
    fontes=["Lei nº 6.437/1977"]),

  dict(id="apreensao-inutilizacao", termo="Apreensão e Inutilização", categoria=CAT,
    sinonimos=[],
    definicao="Medidas administrativas sanitárias aplicadas a produtos irregulares, falsificados, com desvio de qualidade grave ou vencidos, consistindo na retirada física do produto de circulação (apreensão) seguida de sua destruição controlada e documentada (inutilização), impedindo seu retorno ao mercado.",
    explicacaoSimplificada="É quando a vigilância sanitária retira um produto irregular de circulação (apreende) e depois o destrói de forma controlada (inutiliza), para garantir que ele não volte a ser vendido.",
    aplicacaoPratica="Ao encontrar medicamentos falsificados durante uma inspeção, a vigilância sanitária apreende o lote e posteriormente determina sua inutilização, com registro documental de todo o processo.",
    atencao="A inutilização deve ser documentada e, em geral, acompanhada por autoridade competente, para garantir que o produto apreendido não seja desviado ou comercializado de forma irregular antes da destruição.",
    naoConfunda=[],
    termosRelacionados=["termo-interdicao-cautelar","nao-conformidade"],
    fontes=["Lei nº 6.437/1977"]),

  dict(id="roteiro-inspecao-sanitaria", termo="Roteiro de Inspeção Sanitária", categoria=CAT,
    sinonimos=["Check-list de Inspeção Sanitária"],
    definicao="Instrumento técnico padronizado, utilizado por agentes de vigilância sanitária durante inspeções, que lista os itens, requisitos e critérios a serem verificados em um estabelecimento ou processo, garantindo uniformidade e completude na avaliação.",
    explicacaoSimplificada="É a lista padronizada de itens que o fiscal da vigilância sanitária verifica durante uma inspeção.",
    aplicacaoPratica="Durante a inspeção de uma farmácia, o fiscal segue o roteiro de inspeção sanitária, verificando item a item: responsável técnico presente, condições de armazenamento, escrituração de controlados, entre outros.",
    atencao="O roteiro de inspeção varia conforme o tipo de estabelecimento (farmácia, drogaria, distribuidora, indústria) — não existe um roteiro único e genérico para todos os tipos de inspeção.",
    naoConfunda=[],
    termosRelacionados=["auto-infracao-sanitaria","gerenciamento-risco-sanitario"],
    fontes=["Anvisa"]),

  dict(id="capa-acao-corretiva-preventiva", termo="Ação Corretiva e Preventiva (CAPA)", categoria=CAT,
    sinonimos=["CAPA"],
    definicao="Metodologia estruturada de gestão da qualidade que investiga a causa raiz de uma não conformidade ou desvio, implementa ações corretivas (para eliminar o problema já ocorrido) e ações preventivas (para evitar sua recorrência ou ocorrência em situações semelhantes).",
    explicacaoSimplificada="É o processo de descobrir por que algo deu errado (causa raiz) e agir tanto para corrigir o problema atual quanto para evitar que ele se repita.",
    aplicacaoPratica="Após identificar uma não conformidade recorrente em um lote de comprimidos, a equipe de qualidade abre um CAPA: a ação corretiva ajusta o parâmetro de processo que causou o desvio no lote atual, e a ação preventiva revisa o procedimento operacional padrão para evitar recorrência em lotes futuros.",
    atencao="Uma ação corretiva, isolada, resolve o problema pontual já ocorrido; só o CAPA completo (corretiva + preventiva), com investigação de causa raiz documentada, evita que o mesmo problema volte a se repetir.",
    naoConfunda=["nao-conformidade"],
    termosRelacionados=["nao-conformidade","garantia-qualidade"],
    fontes=["ICH Q10","Anvisa"]),

  dict(id="qualificacao-transporte", termo="Qualificação de Transporte", categoria=CAT,
    sinonimos=["Validação de Transporte"],
    definicao="Processo documentado que comprova, por meio de estudos (como mapeamento térmico de rotas e veículos), que o sistema de transporte utilizado mantém as condições especificadas (principalmente de temperatura) necessárias para preservar a qualidade do medicamento ou insumo durante o trajeto.",
    explicacaoSimplificada="São os testes que comprovam que o transporte (caminhão, veículo refrigerado etc.) mantém a temperatura e as condições certas durante toda a viagem do produto.",
    aplicacaoPratica="Antes de contratar uma transportadora para distribuir vacinas, a empresa exige um estudo de qualificação de transporte com mapeamento térmico da rota, comprovando que a temperatura permanece dentro da faixa exigida durante todo o percurso.",
    atencao="A qualificação de transporte é uma exigência específica dentro das BPDA, especialmente crítica para produtos termolábeis que dependem da cadeia fria — nem todo transporte de medicamentos precisa do mesmo nível de controle de temperatura.",
    naoConfunda=[],
    termosRelacionados=["bpda","cadeia-fria","qualificacao"],
    fontes=["RDC Anvisa nº 430/2020"]),

  dict(id="pgrss", termo="PGRSS (Plano de Gerenciamento de Resíduos de Serviços de Saúde)", categoria=CAT,
    sinonimos=["Plano de Gerenciamento de Resíduos de Serviços de Saúde"],
    definicao="Documento obrigatório que estabelece as diretrizes de manejo dos resíduos gerados por estabelecimentos de saúde (farmácias, hospitais, clínicas), desde a geração até a destinação final, classificando-os por categoria de risco (biológico, químico, perfurocortante, comum) e definindo procedimentos seguros para cada etapa.",
    explicacaoSimplificada="É o plano obrigatório que define como o estabelecimento vai lidar com o lixo que gera (medicamentos vencidos, agulhas, luvas etc.), de forma segura, desde a geração até o descarte final.",
    aplicacaoPratica="Uma farmácia elabora seu PGRSS classificando medicamentos vencidos como resíduo químico, definindo acondicionamento, coleta e destinação por empresa especializada, conforme a legislação local.",
    atencao="O PGRSS é exigido mesmo em estabelecimentos de pequeno porte, como farmácias e drogarias, não só em hospitais — a ausência do plano é item comumente verificado em inspeções de vigilância sanitária.",
    naoConfunda=[],
    termosRelacionados=["biosseguranca","descarte-medicamento"],
    fontes=["RDC Anvisa nº 222/2018","Resolução CONAMA nº 358/2005"]),

  dict(id="biosseguranca", termo="Biossegurança", categoria=CAT,
    sinonimos=[],
    definicao="Conjunto de ações, normas e procedimentos destinados a prevenir, minimizar ou eliminar riscos inerentes às atividades que envolvam agentes biológicos, químicos ou físicos, protegendo a saúde do profissional, do paciente, da comunidade e do meio ambiente.",
    explicacaoSimplificada="São as regras e cuidados para evitar riscos (biológicos, químicos, físicos) nas atividades de saúde, protegendo quem trabalha e quem é atendido.",
    aplicacaoPratica="As normas de biossegurança de uma farmácia incluem o uso de EPI para manipulação de certos produtos, o descarte adequado de perfurocortantes e o PGRSS do estabelecimento.",
    atencao="Biossegurança é um conceito guarda-chuva que engloba, entre outras coisas, o uso correto de EPI/EPC e o gerenciamento de resíduos (PGRSS) — não é sinônimo exclusivo de nenhum desses itens isoladamente.",
    naoConfunda=[],
    termosRelacionados=["epi-epc","pgrss","ccih"],
    fontes=["Ministério da Saúde"]),

  dict(id="ccih", termo="CCIH (Comissão de Controle de Infecção Hospitalar)", categoria=CAT,
    sinonimos=["Comissão de Controle de Infecção Hospitalar"],
    definicao="Comissão multiprofissional, de existência obrigatória em hospitais, responsável por planejar, executar e avaliar ações de prevenção e controle de infecções relacionadas à assistência à saúde, incluindo o uso racional de antimicrobianos.",
    explicacaoSimplificada="É a comissão do hospital responsável por prevenir e controlar infecções hospitalares, incluindo o uso correto de antibióticos.",
    aplicacaoPratica="A CCIH de um hospital elabora o protocolo de profilaxia antimicrobiana cirúrgica e monitora indicadores de infecção relacionados a dispositivos invasivos, como cateteres.",
    atencao="A CCIH tem papel central na política de uso racional de antimicrobianos e no controle de resistência antimicrobiana dentro do hospital — é uma exigência legal, não uma boa prática opcional.",
    naoConfunda=[],
    termosRelacionados=["profilaxia-antimicrobiana","resistencia-antimicrobiana","biosseguranca"],
    fontes=["Portaria MS/SNVS nº 2.616/1998"]),

  dict(id="epi-epc", termo="EPI / EPC (Equipamento de Proteção Individual e Coletiva)", categoria=CAT,
    sinonimos=["Equipamento de Proteção Individual","Equipamento de Proteção Coletiva"],
    definicao="Equipamentos destinados a proteger a saúde e a segurança do trabalhador — individualmente (EPI, como luvas, máscaras e óculos de proteção, de uso pessoal) ou coletivamente (EPC, como capelas de exaustão e lava-olhos, que protegem todo o ambiente/equipe).",
    explicacaoSimplificada="São os equipamentos de proteção usados no trabalho — individuais (como luvas e máscaras, de uso pessoal) ou coletivos (como uma capela, que protege todo o ambiente).",
    aplicacaoPratica="Ao manipular um produto com potencial irritante, o farmacêutico utiliza EPI (luvas, óculos de proteção) e trabalha sob um EPC (capela de exaustão), somando as duas camadas de proteção.",
    atencao="EPC não substitui EPI, e vice-versa — são camadas complementares de proteção, e a ausência de qualquer uma delas, quando exigida, é item de não conformidade em inspeções de biossegurança.",
    naoConfunda=[],
    termosRelacionados=["biosseguranca"],
    fontes=["Ministério do Trabalho - NRs"]),

  dict(id="pop-procedimento-operacional", termo="POP (Procedimento Operacional Padrão)", categoria=CAT,
    sinonimos=["Procedimento Operacional Padrão"],
    definicao="Documento escrito que descreve, de forma detalhada e sequencial, como uma atividade ou tarefa deve ser executada, garantindo padronização, rastreabilidade e reprodutibilidade do processo, independentemente de quem o execute.",
    explicacaoSimplificada="É o documento que descreve passo a passo como uma tarefa deve ser feita, para que sempre seja feita da mesma forma, não importa quem a execute.",
    aplicacaoPratica="A farmácia possui um POP para a limpeza e higienização das bancadas de manipulação, detalhando produtos utilizados, frequência e responsável pela execução e registro.",
    atencao="A ausência de POP para atividades críticas (manipulação, limpeza, controle de temperatura) é um dos itens mais comumente apontados em inspeções sanitárias — ter o documento escrito não substitui garantir que ele seja efetivamente seguido e registrado.",
    naoConfunda=[],
    termosRelacionados=["boas-praticas-farmacia","garantia-qualidade"],
    fontes=["Anvisa"]),

  dict(id="processamento-produtos-saude", termo="Processamento de Produtos para Saúde", categoria=CAT,
    sinonimos=[],
    definicao="Conjunto de etapas (limpeza, desinfecção e/ou esterilização) aplicadas a produtos para saúde reutilizáveis (como instrumentais e alguns equipamentos), com o objetivo de reduzir a carga microbiana a um nível seguro antes de seu reuso.",
    explicacaoSimplificada="É o conjunto de etapas (limpar, desinfetar e/ou esterilizar) para deixar um instrumento ou equipamento reutilizável seguro para usar de novo.",
    aplicacaoPratica="Um instrumental cirúrgico reutilizável passa por limpeza, desinfecção e esterilização antes de retornar ao uso, seguindo protocolo validado de processamento de produtos para saúde.",
    atencao="O método de processamento exigido (desinfecção ou esterilização) depende da classificação de risco do produto para saúde (crítico, semicrítico ou não crítico), conforme seu uso pretendido.",
    naoConfunda=["esterilizacao","desinfeccao"],
    termosRelacionados=["esterilizacao","desinfeccao","biosseguranca"],
    fontes=["Anvisa"]),

  dict(id="fator-risco-sanitario", termo="Fator de Risco Sanitário", categoria=CAT,
    sinonimos=[],
    definicao="Característica, condição ou prática que aumenta a probabilidade de ocorrência de um dano à saúde relacionado a um produto, processo, serviço ou estabelecimento, utilizada como critério para a classificação e priorização de ações de vigilância sanitária.",
    explicacaoSimplificada="É qualquer característica ou prática que aumenta a chance de um produto ou estabelecimento causar dano à saúde — usado para decidir onde a fiscalização deve focar mais.",
    aplicacaoPratica="A ausência de responsável técnico presente, o armazenamento inadequado de termolábeis e a falta de escrituração de controlados são exemplos de fatores de risco sanitário que elevam a classificação de risco de uma farmácia em inspeções.",
    atencao="A identificação de fatores de risco sanitário é a base do Gerenciamento de Risco Sanitário — é o que permite à vigilância sanitária decidir onde concentrar recursos de fiscalização.",
    naoConfunda=[],
    termosRelacionados=["gerenciamento-risco-sanitario","roteiro-inspecao-sanitaria"],
    fontes=["Anvisa"]),

  dict(id="vcpaf", termo="Vigilância Sanitária de Portos, Aeroportos e Fronteiras (VCPAF)", categoria=CAT,
    sinonimos=["VIPAF"],
    definicao="Segmento da vigilância sanitária responsável pelo controle sanitário de pessoas, cargas, bagagens, meios de transporte e produtos que entram ou saem do território nacional por portos, aeroportos, fronteiras terrestres e recintos alfandegados, prevenindo a introdução e disseminação de doenças e produtos irregulares.",
    explicacaoSimplificada="É a parte da vigilância sanitária que fiscaliza o que entra e sai do país por portos, aeroportos e fronteiras.",
    aplicacaoPratica="Um lote de medicamento importado é retido pela vigilância sanitária de portos, aeroportos e fronteiras para verificação de regularidade antes de ser liberado para distribuição no país.",
    atencao="Essa vigilância atua na entrada/saída do território nacional, de forma complementar à vigilância sanitária exercida dentro do território (estadual/municipal) sobre estabelecimentos já instalados.",
    naoConfunda=[],
    termosRelacionados=["vigilancia-sanitaria-termo","anvisa"],
    fontes=["Lei nº 9.782/1999","Anvisa"]),

  dict(id="analise-fiscal", termo="Análise Fiscal", categoria=CAT,
    sinonimos=[],
    definicao="Análise laboratorial realizada por laboratório oficial, a pedido da autoridade sanitária, em amostra de produto apreendida ou coletada durante fiscalização, com o objetivo de verificar sua conformidade com os padrões de qualidade exigidos, podendo subsidiar um processo administrativo sanitário.",
    explicacaoSimplificada="É a análise de laboratório feita a pedido da vigilância sanitária, geralmente em um produto apreendido, para verificar se ele está dentro das normas de qualidade.",
    aplicacaoPratica="Um lote de medicamento suspeito de desvio de qualidade é enviado para análise fiscal em laboratório oficial, cujo resultado confirma teor de princípio ativo fora do especificado, fundamentando o Auto de Infração Sanitária.",
    atencao="A análise fiscal tem caráter formal e pode ser usada como prova em processo administrativo sanitário — difere de uma análise de controle de qualidade de rotina feita pela própria empresa fabricante.",
    naoConfunda=[],
    termosRelacionados=["auto-infracao-sanitaria","nao-conformidade"],
    fontes=["Lei nº 6.437/1977"]),

  dict(id="rotulagem-bula", termo="Rotulagem e Bula", categoria=CAT,
    sinonimos=[],
    definicao="Conjunto de informações obrigatórias impressas na embalagem (rotulagem) e no material informativo que acompanha o medicamento (bula), destinadas a identificar o produto e orientar seu uso correto por profissionais de saúde e/ou pacientes, conforme exigências regulatórias específicas.",
    explicacaoSimplificada="É o conjunto de informações que aparecem na embalagem (rotulagem) e na bula do medicamento, exigidas por lei para identificar e orientar o uso do produto.",
    aplicacaoPratica="Antes de dispensar um medicamento, o farmacêutico confere se a rotulagem está íntegra e legível e orienta o paciente com base nas informações da bula, especialmente sobre modo de uso e cuidados.",
    atencao="A bula tem versões distintas — \"Bula do Paciente\" (linguagem acessível) e \"Bula do Profissional de Saúde\" (linguagem técnica) — e a rotulagem deve ser consistente com as informações aprovadas no registro do medicamento.",
    naoConfunda=["bula"],
    termosRelacionados=["bula","tarja-medicamento"],
    fontes=["RDC Anvisa nº 47/2009"]),

  dict(id="snvs", termo="SNVS (Sistema Nacional de Vigilância Sanitária)", categoria=CAT,
    sinonimos=["Sistema Nacional de Vigilância Sanitária"],
    definicao="Conjunto articulado de instituições (Anvisa, vigilâncias sanitárias estaduais, distrital e municipais, além de laboratórios de referência) que atuam de forma integrada e descentralizada na execução das ações de vigilância sanitária em todo o território nacional, sob coordenação da Anvisa.",
    explicacaoSimplificada="É a rede formada pela Anvisa junto com as vigilâncias sanitárias estaduais e municipais, que juntas executam a vigilância sanitária no país.",
    aplicacaoPratica="Uma ação de recall nacional de medicamento é coordenada pela Anvisa, mas sua execução local (retirada efetiva do produto em cada farmácia) depende da atuação das vigilâncias sanitárias estaduais e municipais que compõem o SNVS.",
    atencao="A Anvisa coordena o SNVS, mas não substitui as vigilâncias sanitárias estaduais e municipais, que têm competências próprias e são responsáveis pela fiscalização local (como a emissão de licenças sanitárias).",
    naoConfunda=["anvisa"],
    termosRelacionados=["anvisa","vigilancia-sanitaria-termo","licenca-sanitaria"],
    fontes=["Lei nº 9.782/1999"]),
]

# ---- Validações ----
errors = []
novo_ids = [n["id"] for n in novos]
if len(novo_ids) != len(set(novo_ids)):
    dups = [i for i in novo_ids if novo_ids.count(i) > 1]
    errors.append(f"IDs duplicados dentro do novo lote: {set(dups)}")

for nid in novo_ids:
    if nid in existing_ids:
        errors.append(f"ID já existe no banco: {nid}")

all_ids_after = existing_ids | set(novo_ids)

required_fields = ["id","termo","categoria","sinonimos","definicao","explicacaoSimplificada","aplicacaoPratica","termosRelacionados","fontes"]
for n in novos:
    for field in required_fields:
        if field not in n:
            errors.append(f"{n.get('id','???')}: campo obrigatorio ausente: {field}")
    if n.get("categoria") not in VALID_CATS:
        errors.append(f"{n.get('id')}: categoria invalida: {n.get('categoria')}")
    if not n.get("atencao") and not n.get("naoConfunda"):
        errors.append(f"{n.get('id')}: falta atencao E naoConfunda (pelo menos um e obrigatorio)")
    for rel in n.get("termosRelacionados", []):
        if rel not in all_ids_after:
            errors.append(f"{n.get('id')}: termoRelacionado nao resolve: {rel}")
    for nc in n.get("naoConfunda", []) or []:
        if nc not in all_ids_after:
            errors.append(f"{n.get('id')}: naoConfunda nao resolve: {nc}")
    if not n.get("definicao") or not n.get("explicacaoSimplificada") or not n.get("aplicacaoPratica"):
        errors.append(f"{n.get('id')}: definicao/explicacaoSimplificada/aplicacaoPratica vazio")

if errors:
    print("ERROS DE VALIDACAO - NADA FOI ESCRITO:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

for n in novos:
    data["termos"].append({
        "id": n["id"],
        "termo": n["termo"],
        "categoria": n["categoria"],
        "sinonimos": n.get("sinonimos", []),
        "definicao": n["definicao"],
        "explicacaoSimplificada": n["explicacaoSimplificada"],
        "aplicacaoPratica": n["aplicacaoPratica"],
        "atencao": n.get("atencao", ""),
        "naoConfunda": n.get("naoConfunda", []),
        "termosRelacionados": n["termosRelacionados"],
        "fontes": n["fontes"],
    })

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK: {len(novos)} termos adicionados. Total agora: {len(data['termos'])}")
