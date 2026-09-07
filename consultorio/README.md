# Consultório Farmacêutico — FarmaPrática

Ferramenta para organização, execução, documentação e acompanhamento dos
serviços clínicos farmacêuticos (consulta estruturada, revisão da
farmacoterapia/MAI, conciliação medicamentosa, acompanhamento longitudinal,
plano de cuidado, procedimentos, PRMs/intervenções, farmacovigilância,
encaminhamento/contrarreferência, prescrição farmacêutica, documentação
clínica). Arquivo único `index.html` (HTML+CSS+JS, ~150 KB, sem
dependências externas de rede além das fontes do Google Fonts) —
`localStorage` do navegador como armazenamento, sem backend.

## Reescrita completa (07/09/2026)

Esta é uma reescrita do zero, a pedido do usuário ("a ferramenta ficou
quebrada"). A versão anterior foi descartada; nada do código dela foi
reaproveitado. Nesta versão:

- **Toda a navegação usa um único padrão de delegação de eventos**
  (atributo `data-act="verbo:argumento"` em todo botão/link clicável, um
  único listener de `click` no `document`, mais listeners equivalentes de
  `submit`/`input`/`change`) em vez de reatribuir handlers a cada
  renderização — elimina a classe de bug mais provável por trás de "menu
  não funciona"/"botão não responde" em uma SPA deste tamanho.
- **Testado com cliques reais em navegador (Playwright/Chromium), não com
  manipulação direta de estado via JavaScript.** A rodada anterior tinha
  testado a maior parte dos módulos assim, mas a navegação de nível
  superior (painel, pacientes, agenda, alertas, indicadores, base
  regulatória, configurações) só tinha sido testada via `state.view=...`
  direto — o que mascarava qualquer problema real nos cliques dos itens da
  barra lateral. Nesta rodada, absolutamente toda a navegação (barra
  lateral inteira, as 14 abas do paciente, todos os botões de
  abrir/cancelar/salvar/excluir de cada módulo) foi exercitada com cliques
  reais do Playwright.
- **Verificação visual com capturas de tela**, não só verificação
  funcional — desktop (1440px), mobile (390px, incluindo o menu lateral
  aberto) e tema escuro, todas inspecionadas por mim antes da entrega, além
  de checagem automatizada de overflow horizontal (`scrollWidth` vs.
  `clientWidth`) em cada tela visitada.
- **Testado abrindo o arquivo direto via `file://`** (forma como o usuário
  normalmente abriria o arquivo localmente), não só servido por HTTP.

## O que funciona

Painel principal (KPIs, acesso rápido, alertas recentes, próximos
retornos, pacientes sem acompanhamento recente); cadastro de pacientes;
ficha clínica (identificação, dados clínicos com cálculo de IMC,
histórico) com atualização longitudinal; consulta farmacêutica estruturada
com evolução SOAP (acolhimento, anamnese, histórico de saúde e estilo de
vida embutidos no bloco Subjetivo/Objetivo) e lembretes de checklist
pré-consulta/alta; histórico farmacoterapêutico completo por medicamento;
avaliação de adequação da farmacoterapia (MAI adaptado — ver seção
dedicada abaixo); conciliação medicamentosa com tabela comparativa e
classificação intencional/não intencional/necessita confirmação;
acompanhamento com metas por condição, registro de rastreamento
(PA/glicemia/antropometria/outros — Point-of-Care Testing) e gráfico de
evolução (SVG simples, sem biblioteca externa); plano de cuidado
estruturado (problema → objetivo → intervenção → responsável → prazo →
meta → status); procedimentos (vacinação completa e administração de
medicamentos/dispositivos); educação em saúde por tema e protocolo de
cessação tabágica (com fases preparação → intervenção → acompanhamento →
prevenção de recaída); PRMs com geração de intervenção pré-preenchida a
partir do PRM; farmacovigilância (registro de suspeita de RAM);
encaminhamento farmacêutico com geração de documento para impressão e
contrarreferência embutida; prescrição farmacêutica com **bloqueio
obrigatório** de fundamento normativo para medicamento sujeito a
prescrição médica (testado: a ferramenta impede salvar sem esse campo);
documentos (prontuário, MAI, plano de cuidado, declaração de atendimento,
encaminhamento, prescrição — todos via impressão em nova janela); agenda;
alertas clínicos automáticos (regra simples, rotulados "apoio à decisão");
indicadores (consultório e por paciente); linha do tempo filtrável por
categoria; base regulatória editável (Resolução CFF 585/2013, 586/2013,
RDC 44/2009 como ponto de partida, com aviso de "verifique a fonte
oficial" e estrutura para atualização); exportação/importação de backup em
`.json`; opção de apagar todos os dados.

## Avaliação de Adequação da Farmacoterapia (MAI) — conforme imagem enviada

Segue fielmente a tabela adaptada enviada pelo usuário: bloco
Subjetivo/Objetivo no topo; tabela por medicamento com as 9 colunas na
mesma ordem da imagem; 3 estados por critério (✓ conforme, X não
conformidade, ? informação insuficiente) com campo de justificativa;
citação completa de Hanlon JT, Schmader KE, Samsa GP, Weinberger M, Uttech
KM, Lewis IK, Cohen HJ, Feussner JR. J Clin Epidemiol. 1992;45(10):1045-1051;
aviso de que a pontuação é "Índice adaptado do FarmaPrática", nunca o
escore original; classificação automática 🟢/🟡/🟠/🔴; síntese automática
(medicamentos avaliados, não conformidades, problemas identificados,
necessidade de encaminhamento/monitoramento). Testado com clique real:
9/9 critérios avaliados, 1 não conformidade, 1 sem informação → índice
78%, classificação "🟡 Requer atenção" — cálculo conferido manualmente.

## Consolidação de escopo

Os 51 blocos do pedido original foram organizados em 7 telas de nível
superior (Painel, Pacientes, Agenda, Alertas, Indicadores, Base
regulatória, Configurações) + 14 abas dentro do workspace do paciente
(Ficha · Consulta/SOAP · Farmacoterapia · MAI · Conciliação ·
Acompanhamento · Plano de cuidado · Procedimentos · Educação/Tabagismo ·
PRM/Intervenções · Encaminhamento · Prescrição · Documentos · Linha do
tempo) — mesma lógica de consolidação já aprovada pelo usuário
anteriormente (acolhimento+anamnese+histórico+estilo de vida dentro do
SOAP; revisão da farmacoterapia = a própria aba MAI; PA/glicemia/
antropometria + acompanhamento longitudinal juntos; vacinação +
administração juntos; educação + tabagismo juntos; encaminhamento +
contrarreferência juntos; PRM + intervenção juntos).

## Limitações conhecidas / decisões deliberadas

- **Armazenamento 100% local (`localStorage`).** Sem backend, sem
  sincronização entre dispositivos/navegadores, sem login/senha. Se vários
  farmacêuticos usarem o Consultório em máquinas diferentes, os dados não
  sincronizam nesta versão.
- **Sem integração real com base CMED/ANVISA** para autopreenchimento de
  medicamento — não há hoje essa base integrada em nenhuma ferramenta do
  site para reaproveitar. Cadastro de medicamento é manual; há atalhos
  para o Guia de Dispensação e para verificar interações em nova aba.
- **"Gerar Desafio Clínico" (seção 43 do pedido) não foi implementado
  nesta rodada** — o banco de casos de `desafio/` é curado manualmente com
  validação cruzada, e replicar isso com segurança (garantir remoção de
  identificação) exigiria mais uma rodada dedicada. Se for prioridade,
  posso adicionar um botão que gera um rascunho `.json` anonimizado para
  revisão manual, como a versão anterior tinha esboçado.
- **"Educação continuada" (seção 44 — gerar flashcards/quizzes a partir de
  problemas do consultório) também não foi implementada** nesta reescrita
  — é um recurso novo e relativamente independente do núcleo clínico;
  ficou fora do escopo desta rodada de reconstrução.
- **"Inteligência Clínica" (seção 48) implementada como regras automáticas
  simples**, não IA real — sempre rotulada "apoio à decisão".
- **Chave de armazenamento nova** (`fp_consultorio_db_v2`, era `_v1` na
  versão anterior) — como o `index.html` anterior nunca chegou a ficar
  publicado de fato para uso real (a pasta já estava vazia quando esta
  rodada começou), não há dados antigos para migrar.

## Estrutura de dados

`localStorage` (`fp_consultorio_db_v2`): `pacientes[]` (cada um com
`clinico`, `historico`, `medicamentos[]`, `evolucoes[]`, `maiAvaliacoes[]`,
`conciliacoes[]`, `acompanhamentos[]`, `rastreamentos[]`,
`planosCuidado[]`, `vacinas[]`, `administracoes[]`, `educacoes[]`,
`tabagismo`, `prms[]`, `intervencoes[]`, `encaminhamentos[]`,
`prescricoes[]`, `ram[]`), `agenda[]`, `regulatorio[]` e `config`.

## Verificação feita nesta rodada

`node --check` no bloco `<script>` extraído: sem erros. Balanceamento de
`<div>`/`</div>` (496/496), `<form>`/`</form>` (23/23) e chaves `{}`
(1058/1058). Teste funcional completo em Chromium real (Playwright),
aberto via `file://`: toda a navegação de nível superior e as 14 abas do
paciente exercitadas com **cliques reais** (não manipulação direta de
estado); cadastro de paciente; dados clínicos com cálculo de IMC; consulta/
SOAP; farmacoterapia; MAI (adicionar medicamento, marcar critérios,
conferir cálculo, salvar); conciliação (adicionar item, classificar);
rastreamento; plano de cuidado; vacinação; educação/tabagismo; PRM → geração
de intervenção pré-preenchida (confirmado que os campos vêm corretamente
copiados); encaminhamento + contrarreferência (formulário embutido abre
corretamente); prescrição — **confirmado que a ferramenta bloqueia com
alerta a tentativa de salvar prescrição de medicamento sujeito a
receita médica sem fundamento normativo, e libera assim que preenchido**;
impressão de documento (MAI) em nova janela, conteúdo conferido (contém a
citação de Hanlon); linha do tempo. Zero erros de console/página em todo o
percurso. Zero problemas de overflow horizontal (checado em cada tela,
desktop e mobile). Capturas de tela de desktop, mobile (com menu lateral
aberto) e tema escuro inspecionadas visualmente antes da entrega — sem
sobreposição de elementos, sem quebra de layout. Arquivo gravado
diretamente na pasta real do usuário via `device_commit_files`. Os dois
links do menu inicial (barra lateral "Consultório Farm." e card da grade
"Ferramentas Farmacêuticas", cor índigo) já estavam ativos de uma rodada
anterior e foram reconferidos — continuam apontando para `consultorio/`.

**Falta o usuário rodar `git add`/`commit`/`push`** na pasta `- INDEX`
para publicar no GitHub Pages.

**Pendente / não implementado:** "Gerar Desafio Clínico" e "Educação
continuada" (ver seção de limitações acima); confirmação visual do usuário
em tela real (a verificação desta rodada usou capturas de tela
automatizadas, inspecionadas por mim, mas não substitui o usuário abrindo
a ferramenta pessoalmente).
