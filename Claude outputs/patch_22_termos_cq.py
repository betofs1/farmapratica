import json, sys, io

F_FARMACOPEIA = "Farmacopeia Brasileira, 6ª edição (Anvisa)"
F_RDC166 = "RDC Anvisa nº 166/2017 — Validação de Métodos Analíticos"
F_ICHQ2 = "ICH Q2(R1) — Validation of Analytical Procedures: Text and Methodology"

novos = [
  {
    "id": "qualidade", "termo": "Qualidade", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Grau em que um conjunto de características inerentes a um medicamento atende aos requisitos e especificações estabelecidos, garantindo identidade, teor, pureza e desempenho adequados para o uso a que se destina.",
    "explicacaoSimplificada": "É o quanto um medicamento realmente corresponde ao que deveria ser — na quantidade certa de princípio ativo, livre de contaminantes e funcionando como esperado.",
    "aplicacaoPratica": "Um comprimido com qualidade apresenta teor, dissolução e uniformidade de dose dentro dos limites especificados; a qualidade é o resultado final que todo o sistema de Controle de Qualidade e Garantia da Qualidade busca assegurar.",
    "atencao": "Qualidade é o atributo do produto (o resultado); Controle de Qualidade é a atividade de verificação; Garantia da Qualidade é o sistema que assegura esse resultado de forma consistente — os três termos são frequentemente confundidos em prova.",
    "termosRelacionados": ["controle-qualidade-termo", "garantia-qualidade", "especificacao-farmacopeica"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "garantia-qualidade", "termo": "Garantia da Qualidade (GQ)", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Sistema abrangente de ações planejadas e sistemáticas, que engloba todos os aspectos que influenciam a qualidade, destinado a assegurar que os medicamentos sejam consistentemente produzidos e controlados conforme os padrões de qualidade apropriados ao uso pretendido.",
    "explicacaoSimplificada": "É o sistema geral que organiza tudo — documentação, treinamento, validação, Boas Práticas de Fabricação e Controle de Qualidade — para garantir que o medicamento sempre saia com a qualidade esperada.",
    "aplicacaoPratica": "A Garantia da Qualidade engloba o Controle de Qualidade (que analisa amostras) como uma de suas partes, mas vai além, cobrindo documentação, qualificação de equipamentos, validação de processos e treinamento de pessoal.",
    "atencao": "Não confundir com Controle de Qualidade: o CQ é uma atividade pontual de verificação (analisar, medir); a GQ é o sistema organizacional mais amplo que inclui o CQ e também a prevenção de desvios.",
    "termosRelacionados": ["controle-qualidade-termo", "boas-praticas-fabricacao", "qualidade", "validacao"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "amostragem", "termo": "Amostragem", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Processo de seleção de uma quantidade representativa de unidades de um lote, segundo plano estatístico definido, destinada à realização de ensaios de controle de qualidade.",
    "explicacaoSimplificada": "É a retirada de algumas unidades de um lote de medicamentos, de forma planejada, para representar o lote inteiro nos testes de qualidade.",
    "aplicacaoPratica": "Retirar comprimidos de diferentes pontos (início, meio e fim) de um lote de produção para análise, de modo que a amostra reflita de fato a variabilidade real do lote.",
    "atencao": "Uma amostragem mal planejada (ex.: retirar unidades só do início do lote) pode não detectar heterogeneidades reais do processo, comprometendo a validade de todo o resultado do Controle de Qualidade.",
    "termosRelacionados": ["controle-qualidade-termo", "uniformidade-dose"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "identidade", "termo": "Identidade", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Ensaio que confirma que a substância analisada corresponde de fato ao princípio ativo ou material declarado, por meio de métodos físico-químicos, cromatográficos ou espectroscópicos característicos.",
    "explicacaoSimplificada": "É o teste que responde à pergunta 'isso é realmente o que deveria ser?' — confirma que o pó ou comprimido contém o princípio ativo declarado, e não outro.",
    "aplicacaoPratica": "Confirmar, por espectroscopia de infravermelho ou cromatografia, que um lote rotulado como paracetamol realmente contém paracetamol, e não outra substância por erro de rotulagem ou contaminação cruzada.",
    "atencao": "O ensaio de identidade é qualitativo (confirma 'o que é'), diferente do ensaio de teor, que é quantitativo (confirma 'quanto tem') — os dois são complementares e exigidos juntos na liberação de um lote.",
    "termosRelacionados": ["teor", "especificacao-farmacopeica"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "teor", "termo": "Teor", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Quantidade de princípio ativo presente em uma amostra, expressa geralmente como porcentagem da quantidade declarada no rótulo.",
    "explicacaoSimplificada": "É a quantidade real de princípio ativo que o comprimido (ou outra forma farmacêutica) contém, comparada com o que está escrito na embalagem.",
    "aplicacaoPratica": "Determinar por cromatografia líquida (HPLC) a quantidade de princípio ativo presente em um comprimido e compará-la com os limites de especificação (ex.: 95–105% do declarado).",
    "atencao": "Um teor fora da especificação pode indicar tanto um problema de fabricação (erro de pesagem, degradação) quanto, se detectado após o uso, risco de subdosagem ou sobredosagem para o paciente.",
    "termosRelacionados": ["identidade", "pureza", "especificacao-farmacopeica"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "pureza", "termo": "Pureza", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Grau de ausência de substâncias estranhas ou impurezas indesejáveis (produtos de degradação, resíduos de síntese, contaminantes) em um princípio ativo ou medicamento, dentro dos limites estabelecidos.",
    "explicacaoSimplificada": "É o quanto uma substância está livre de 'contaminações' ou impurezas que não deveriam estar ali.",
    "aplicacaoPratica": "Determinar por HPLC as impurezas relacionadas ao princípio ativo em um lote, comparando o resultado com os limites máximos permitidos na farmacopeia ou no dossiê de registro.",
    "atencao": "Impurezas podem ser mais tóxicas que o próprio princípio ativo, mesmo em baixas concentrações — por isso a pureza é controlada com limites frequentemente mais rígidos que o teor do próprio fármaco.",
    "termosRelacionados": ["teor", "limite-quantificacao", "limite-deteccao"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "uniformidade-dose", "termo": "Uniformidade de Dose", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Ensaio que verifica se as unidades individuais de um lote (comprimidos, cápsulas etc.) apresentam quantidade de princípio ativo dentro de uma faixa estreita em torno do valor declarado, garantindo consistência entre unidades.",
    "explicacaoSimplificada": "Verifica se cada comprimido do lote tem, individualmente, aproximadamente a mesma quantidade de princípio ativo — não basta a média estar certa, cada unidade precisa estar dentro da faixa.",
    "aplicacaoPratica": "Analisar individualmente 10 (ou mais) comprimidos de um mesmo lote para verificar a variação de conteúdo entre eles, especialmente crítico em formulações de baixa dosagem ou fármacos de margem terapêutica estreita.",
    "atencao": "A uniformidade de dose é diferente do teor médio do lote: um lote pode ter teor médio correto e, ainda assim, falhar na uniformidade se unidades individuais variarem muito entre si (algumas subdosadas, outras sobredosadas).",
    "termosRelacionados": ["teor", "amostragem", "indice-terapeutico"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "desintegracao", "termo": "Desintegração", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Ensaio que determina o tempo necessário para que uma forma farmacêutica sólida se fragmente em partículas menores, sob condições padronizadas de agitação e meio, sem necessariamente implicar a dissolução completa do princípio ativo.",
    "explicacaoSimplificada": "Mede quanto tempo o comprimido leva para se quebrar/esfarelar em pedaços menores — é só a quebra física, não a liberação do fármaco no sangue.",
    "aplicacaoPratica": "Avaliar, em aparelho de desintegração padronizado, quanto tempo um comprimido leva para se fragmentar completamente em determinado meio líquido e temperatura.",
    "atencao": "Não confundir com dissolução: desintegração é a quebra física da forma farmacêutica; dissolução é a liberação do princípio ativo no meio — um comprimido pode se desintegrar rapidamente e ainda assim dissolver mal, ou vice-versa.",
    "termosRelacionados": ["dissolucao", "forma-farmaceutica"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "qualificacao", "termo": "Qualificação", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Demonstração documentada de que instalações, equipamentos, sistemas ou utilidades estão corretamente instalados, operam conforme especificado e apresentam desempenho adequado ao uso pretendido.",
    "explicacaoSimplificada": "É a comprovação de que um equipamento ou sistema (não um método) está funcionando corretamente e é adequado para o que vai ser usado.",
    "aplicacaoPratica": "Qualificar uma balança analítica (verificando calibração, exatidão e linearidade dela própria) antes de utilizá-la em ensaios de Controle de Qualidade.",
    "atencao": "Não confundir com validação: qualificação se refere a equipamentos, instalações e sistemas; validação se refere a métodos e processos — um método de HPLC é validado, o cromatógrafo usado nele é qualificado.",
    "termosRelacionados": ["validacao", "boas-praticas-fabricacao"],
    "fontes": [F_RDC166]
  },
  {
    "id": "exatidao", "termo": "Exatidão", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Grau de concordância entre o resultado obtido por um método analítico e o valor verdadeiro ou aceito como referência, geralmente expresso como percentual de recuperação.",
    "explicacaoSimplificada": "Mostra o quanto o resultado de um método está próximo do valor real/verdadeiro daquilo que está sendo medido.",
    "aplicacaoPratica": "Um método determina 100,1 mg de princípio ativo em uma amostra cujo valor de referência certificado é 100 mg — a pequena diferença indica alta exatidão do método.",
    "atencao": "Exatidão não é o mesmo que precisão: um método pode ser preciso (resultados próximos entre si) e ainda assim impreciso quanto à exatidão (todos sistematicamente afastados do valor verdadeiro) — e vice-versa.",
    "termosRelacionados": ["precisao", "robustez"],
    "fontes": [F_ICHQ2, F_RDC166]
  },
  {
    "id": "precisao", "termo": "Precisão", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Grau de concordância entre resultados obtidos em medições repetidas de uma mesma amostra, independentemente de estarem próximos do valor verdadeiro; avaliada nos níveis de repetibilidade, precisão intermediária e reprodutibilidade.",
    "explicacaoSimplificada": "Mostra o quanto resultados repetidos de uma mesma análise ficam parecidos entre si — não importa se estão certos, importa se são consistentes.",
    "aplicacaoPratica": "Cinco análises da mesma amostra, pelo mesmo método, apresentam resultados muito próximos entre si — isso indica boa precisão do método, mesmo antes de confirmar a exatidão.",
    "atencao": "Precisão não garante exatidão: resultados podem ser altamente concordantes entre si e, ainda assim, estarem todos igualmente afastados do valor verdadeiro (erro sistemático).",
    "termosRelacionados": ["exatidao", "repetibilidade", "precisao-intermediaria", "reprodutibilidade"],
    "fontes": [F_ICHQ2, F_RDC166]
  },
  {
    "id": "repetibilidade", "termo": "Repetibilidade", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Nível de precisão obtido sob as mesmas condições de operação — mesmo analista, mesmo equipamento, mesmo método e curto intervalo de tempo.",
    "explicacaoSimplificada": "É a precisão testada da forma mais controlada possível: a mesma pessoa, com o mesmo equipamento, repetindo a análise logo em seguida.",
    "aplicacaoPratica": "Um mesmo analista realiza seis determinações consecutivas da mesma amostra, no mesmo equipamento, no mesmo dia, para avaliar a repetibilidade do método.",
    "atencao": "A repetibilidade é o nível mais 'fácil' de se obter bons resultados, por eliminar fontes de variação externas — um método repetível não garante automaticamente boa precisão intermediária ou reprodutibilidade.",
    "termosRelacionados": ["precisao", "precisao-intermediaria", "reprodutibilidade"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "precisao-intermediaria", "termo": "Precisão Intermediária", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Nível de precisão que avalia a concordância de resultados dentro do mesmo laboratório, considerando variações como diferentes dias, analistas ou equipamentos.",
    "explicacaoSimplificada": "É a precisão testada variando alguns fatores (dia, analista, equipamento), mas ainda dentro do mesmo laboratório.",
    "aplicacaoPratica": "O mesmo método é executado por analistas diferentes, em dias diferentes, dentro do mesmo laboratório, para verificar se o resultado se mantém consistente mesmo com essas variações internas.",
    "atencao": "Precisão intermediária fica entre a repetibilidade (mesmas condições) e a reprodutibilidade (laboratórios diferentes) — avalia a robustez do método frente a variações do dia a dia dentro de um mesmo laboratório.",
    "termosRelacionados": ["repetibilidade", "reprodutibilidade", "precisao"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "reprodutibilidade", "termo": "Reprodutibilidade", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Nível de precisão obtido em condições diferentes, geralmente entre laboratórios distintos, avaliando a transferência de um método analítico entre diferentes locais.",
    "explicacaoSimplificada": "É a precisão testada entre laboratórios diferentes — verifica se o método funciona igual quando outro laboratório o executa.",
    "aplicacaoPratica": "Dois laboratórios diferentes realizam o mesmo método analítico validado, com equipamentos e analistas próprios, para confirmar que o método é transferível e confiável fora do laboratório de origem.",
    "atencao": "A reprodutibilidade só é avaliada quando o método será usado em mais de um laboratório (ex.: estudos colaborativos, transferência de tecnologia) — nem toda validação de método exige esse nível de precisão.",
    "termosRelacionados": ["precisao", "precisao-intermediaria", "repetibilidade"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "robustez", "termo": "Robustez", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Capacidade de um método analítico de permanecer confiável e inalterado diante de pequenas variações deliberadas em suas condições operacionais (ex.: pH, temperatura, fluxo, lote de coluna).",
    "explicacaoSimplificada": "Mostra se o método continua dando resultados confiáveis mesmo quando pequenos detalhes do processo mudam um pouco.",
    "aplicacaoPratica": "Alterar levemente o pH da fase móvel, o fluxo ou a temperatura de um método de HPLC e verificar que o resultado da análise não é significativamente afetado.",
    "atencao": "Robustez não deve ser confundida com precisão: a robustez testa a tolerância do método a pequenas variações deliberadas nas condições analíticas; a precisão testa a concordância entre repetições sem alterar essas condições.",
    "termosRelacionados": ["exatidao", "precisao", "linearidade"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "seletividade-analitica", "termo": "Seletividade/Especificidade Analítica", "categoria": "controle-qualidade",
    "sinonimos": ["Especificidade Analítica"],
    "definicao": "Capacidade de um método analítico de determinar o analito de interesse de forma inequívoca, mesmo na presença de outros componentes da amostra, como excipientes, impurezas e produtos de degradação.",
    "explicacaoSimplificada": "É a capacidade do método de 'enxergar' exatamente o princípio ativo que está procurando, sem se confundir com outras substâncias presentes na amostra.",
    "aplicacaoPratica": "Quantificar corretamente o princípio ativo de um comprimido mesmo na presença de excipientes, corantes e produtos de degradação que também estão na matriz da amostra.",
    "atencao": "Não confundir com a 'Seletividade' farmacodinâmica (capacidade de um fármaco agir preferencialmente sobre um tipo de receptor): aqui o termo descreve uma propriedade do método analítico, em contexto de validação de métodos, não de ação farmacológica.",
    "termosRelacionados": ["linearidade", "robustez", "exatidao"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "linearidade", "termo": "Linearidade", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Capacidade de um método analítico de produzir resultados diretamente proporcionais à concentração do analito dentro de uma faixa determinada.",
    "explicacaoSimplificada": "Mostra se, ao dobrar a quantidade da substância, a resposta do método também dobra de forma proporcional — uma reta quando colocada em gráfico.",
    "aplicacaoPratica": "Preparar soluções em diferentes concentrações conhecidas e verificar que a resposta analítica (ex.: área do pico cromatográfico) aumenta proporcionalmente, com coeficiente de correlação adequado.",
    "atencao": "A linearidade só é válida dentro da faixa (intervalo) estudada — não se deve extrapolar o método para concentrações fora da faixa validada sem nova avaliação.",
    "termosRelacionados": ["faixa", "exatidao", "robustez"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "faixa", "termo": "Faixa (Intervalo)", "categoria": "controle-qualidade",
    "sinonimos": ["Intervalo Analítico"],
    "definicao": "Intervalo entre os níveis inferior e superior de concentração do analito para os quais foi demonstrado que o método analítico apresenta exatidão, precisão e linearidade adequadas.",
    "explicacaoSimplificada": "É a 'faixa de uso' validada do método — os limites de concentração dentro dos quais ele é confiável.",
    "aplicacaoPratica": "Um método é validado para concentrações de 50% a 150% da concentração nominal do princípio ativo, cobrindo tanto possíveis desvios de teor quanto estudos de dissolução em diferentes pontos do tempo.",
    "atencao": "Resultados obtidos fora da faixa validada de um método não têm a mesma confiabilidade demonstrada na validação, mesmo que o método pareça funcionar — exige nova avaliação para extensão da faixa.",
    "termosRelacionados": ["linearidade", "exatidao", "precisao"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "limite-deteccao", "termo": "Limite de Detecção (LD)", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Menor quantidade de analito em uma amostra que pode ser detectada, mas não necessariamente quantificada com exatidão e precisão adequadas.",
    "explicacaoSimplificada": "É a menor quantidade de uma substância que o método consegue perceber que está presente, mesmo sem conseguir dizer com precisão quanto tem.",
    "aplicacaoPratica": "Detectar a presença de uma impureza em concentração muito baixa em um lote, mesmo que o método ainda não seja capaz de quantificá-la com confiabilidade nesse nível.",
    "atencao": "O limite de detecção é sempre numericamente menor que o limite de quantificação do mesmo método — detectar 'que existe' é um requisito menos exigente do que quantificar 'quanto existe' com confiabilidade.",
    "termosRelacionados": ["limite-quantificacao", "pureza"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "limite-quantificacao", "termo": "Limite de Quantificação (LQ)", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Menor quantidade de analito em uma amostra que pode ser determinada quantitativamente, com precisão e exatidão adequadas, sob as condições experimentais estabelecidas.",
    "explicacaoSimplificada": "É a menor quantidade de uma substância que o método consegue não só detectar, mas medir de forma confiável.",
    "aplicacaoPratica": "Quantificar com confiabilidade uma impureza presente em concentração muito baixa em um lote, dentro do limite máximo estabelecido para essa impureza.",
    "atencao": "Particularmente relevante na análise de impurezas e produtos de degradação, onde os limites regulatórios aceitáveis costumam ser muito baixos — o método precisa ter limite de quantificação inferior a esses limites para ser adequado.",
    "termosRelacionados": ["limite-deteccao", "pureza"],
    "fontes": [F_ICHQ2]
  },
  {
    "id": "nao-conformidade", "termo": "Não Conformidade", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Falha em atender a um requisito, especificação ou critério de qualidade estabelecido para um produto, processo ou sistema.",
    "explicacaoSimplificada": "É quando algo (um lote, um processo, um resultado) não atende ao que foi definido como aceitável.",
    "aplicacaoPratica": "Um lote de comprimidos apresenta teor de princípio ativo abaixo do limite especificado — essa não conformidade impede a liberação do lote até investigação da causa raiz.",
    "atencao": "Toda não conformidade exige investigação de causa raiz e registro documentado (não apenas o descarte do lote), pois pode indicar falha sistêmica no processo que afetaria outros lotes.",
    "termosRelacionados": ["especificacao-farmacopeica", "qualidade"],
    "fontes": [F_FARMACOPEIA]
  },
  {
    "id": "amostra-retencao", "termo": "Amostra de Retenção", "categoria": "controle-qualidade",
    "sinonimos": [],
    "definicao": "Amostra representativa de um lote de medicamento, mantida em condições adequadas de armazenamento por período definido após a fabricação, para possibilitar avaliações futuras relacionadas à qualidade do lote.",
    "explicacaoSimplificada": "É uma parte do lote guardada de propósito, para que seja possível investigar o produto depois, caso surja alguma dúvida ou reclamação sobre ele.",
    "aplicacaoPratica": "Guardar unidades de um lote de medicamento por tempo determinado após sua fabricação, permitindo reanálise em caso de reclamação, desvio de qualidade identificado no mercado ou investigação regulatória.",
    "atencao": "Amostra de retenção não deve ser confundida com amostra de referência/padrão de trabalho usada em rotina analítica: a amostra de retenção é do próprio lote comercializado, guardada especificamente para investigações futuras daquele lote.",
    "termosRelacionados": ["qualidade", "nao-conformidade"],
    "fontes": [F_FARMACOPEIA]
  },
]

PATH = "dicionario/dicionario.json"
with io.open(PATH, encoding="utf-8") as f:
    data = json.load(f)

termos = data["termos"]
existing_ids = {t["id"] for t in termos}
categorias_validas = {c["id"] for c in data["categorias"]}

errors = []

new_ids = [t["id"] for t in novos]
if len(new_ids) != len(set(new_ids)):
    errors.append("IDs duplicados dentro do lote novo")

for t in novos:
    if t["id"] in existing_ids:
        errors.append(f"ID já existe no dicionário: {t['id']}")
    if t["categoria"] not in categorias_validas:
        errors.append(f"Categoria inválida para {t['id']}: {t['categoria']}")
    if not (t.get("atencao") or t.get("naoConfunda")):
        errors.append(f"{t['id']}: sem atencao nem naoConfunda (cobertura desigual)")

all_ids_after = existing_ids | set(new_ids)
for t in novos:
    for rel in t.get("termosRelacionados", []):
        if rel not in all_ids_after:
            errors.append(f"{t['id']}: termoRelacionado '{rel}' não resolve a nenhum id existente ou novo")

required_fields = ["id", "termo", "categoria", "definicao", "explicacaoSimplificada", "aplicacaoPratica", "termosRelacionados", "fontes"]
for t in novos:
    for f_ in required_fields:
        if f_ not in t:
            errors.append(f"{t['id']}: campo obrigatório ausente: {f_}")

if errors:
    print("ERROS DE VALIDACAO:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

termos.extend(novos)
data["termos"] = termos

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK: {len(novos)} termos adicionados. Total agora: {len(termos)}")
