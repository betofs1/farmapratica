# Módulo Desafio Clínico — FarmaPrática

Simulador interativo de raciocínio clínico farmacêutico: casos clínicos
progressivos (queixa → anamnese → sinais de alerta → hipóteses/diferencial →
medicamentos/interações → exames, quando aplicável → decisão → orientação →
resumo de aprendizado), banco de quiz por categoria e nível, flashcards de
revisão e sistema de pontuação, sequência de dias e conquistas — tudo em
`localStorage`, individual por navegador/dispositivo.

**Conteúdo educacional de apoio ao raciocínio clínico farmacêutico** — não
substitui avaliação médica, protocolo institucional ou julgamento clínico
individualizado diante do paciente real.

## Arquivos do módulo

```
index.html     → aplicação (HTML + CSS + JS), lê os dados de desafio.json em tempo de execução
desafio.json   → banco de categorias, casos clínicos, quiz, flashcards e conquistas
logo.png       → logo da marca (mesma imagem usada nas demais ferramentas)
README.md      → este guia
```

Como `exames`, `interacoes` e `dicionario`, este módulo carrega os dados via
`fetch('desafio.json')` — **para testar localmente é preciso servir a pasta
por um servidor HTTP** (`python3 -m http.server 8000` e abrir
`http://localhost:8000/`); no GitHub Pages funciona sem configuração extra.

## Escopo desta primeira versão (v1.0)

A especificação original é extremamente ampla (10+ "modos de jogo",
motor de geração dinâmica de casos cruzando 4+ ferramentas, quiz, flashcards,
gamificação completa com conquistas, repetição espaçada e dashboard). Para
uma primeira versão tecnicamente sólida, foram feitas as seguintes escolhas
de escopo (decididas com o usuário antes do desenvolvimento):

- **Núcleo curado de conteúdo**, não geração dinâmica: 42 casos clínicos
  (2 por categoria), 63 questões de quiz (3 por categoria) e 63 flashcards
  (3 por categoria), distribuídos pelas 21 categorias clínicas da
  especificação original. Estrutura pronta para expansão incremental — basta
  adicionar objetos a `desafio.json` (ou aos arquivos-fonte em `dados/` do
  processo de build), sem alterar `index.html`.
- **"Modos de jogo" implementados como filtros** sobre o mesmo banco de
  conteúdo, em vez de motores separados: Nível (Básico/Intermediário/
  Avançado/Especialista), Foco (Geral/Farmacoterapêutico/Laboratorial/Sinais
  de Alerta) e Ambiente (Balcão/Consultório) filtram a lista de casos;
  Modo Concurso e Modo Difícil filtram o banco de quiz. Atalhos na página
  inicial (Caso Aleatório, Desafio Rápido, Sinais de Alerta, Modo Concurso,
  Modo Difícil) aplicam esses filtros automaticamente.
- **Integração com o Dicionário Farmacêutico por link direto**: cada caso
  lista termos relacionados (campo `termosDicionario`, validado contra os
  293 ids reais do dicionário) que abrem a ficha do termo em nova aba via
  `../dicionario/?termo=<id>` — o `dicionario/index.html` foi atualizado
  para ler esse parâmetro de URL e abrir o termo diretamente. Não há, nesta
  versão, leitura em tempo de execução dos JSONs de `interacoes/` ou
  `exames/` para montar casos dinamicamente — o conteúdo desses domínios foi
  escrito de forma autocontida e clinicamente revisada dentro de cada caso.
- **Gamificação com escopo definido**: pontuação por caso e por quiz,
  sequência de dias consecutivos de uso, taxa de acerto, e 10 conquistas
  fixas (ver `conquistas.json`). Não há ranking entre usuários nem
  sincronização entre dispositivos — tudo fica salvo localmente
  (`localStorage`, chave `desafioclinico-progresso`).
- **Repetição espaçada simplificada nos flashcards**: cartões marcados como
  "Não sei" ficam guardados (`cartoesDificeis`) e voltam a aparecer
  primeiro na próxima sessão de estudo daquela categoria — não há
  agendamento por data como em sistemas de repetição espaçada completos.

## Estrutura de `desafio.json`

```json
{
  "meta": {"versao","dataAtualizacao","totalCasos","totalQuiz","totalFlashcards","totalCategorias"},
  "categorias": [ {"id","nome","cor","emoji","descricao"} ],
  "casos": [ {...ver campos abaixo...} ],
  "quiz": [ {"id","categoria","nivel","tipo","pergunta","opcoes":[...],"correta","explicacao","concurso"} ],
  "flashcards": [ {"id","categoria","frente","verso"} ],
  "conquistas": [ {"id","nome","emoji","descricao","criterio":{"tipo",...}} ]
}
```

### Campos de cada caso (`casos[]`)

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | identificador único |
| `titulo` | string | título do caso |
| `categoria` | string | precisa bater com um `id` de `"categorias"` |
| `nivel` | string | `basico` \| `intermediario` \| `avancado` \| `especialista` |
| `foco` | string | `geral` \| `farmacoterapeutico` \| `laboratorial` \| `sinal-alerta` — usado como filtro de "modo" |
| `ambiente` | string | `balcao` \| `consultorio` |
| `resumo` | string | teaser de 1 linha exibido no card |
| `etapas` | array | sequência de passos: `{"tipo":"info","titulo","texto"}` (só avança) ou `{"tipo":"decisao","titulo","competencia","texto","opcoes":[{"texto","tipo":"acerto\|atencao\|erro","pontos","feedback"}]}` |
| `resumoFinal` | objeto | "Aprenda com o caso": `condicao`, `sinaisImportantes`, `medicamentos` (opcional), `examesRelevantes` (opcional), `sinalAlerta`, `condutaFarmaceutica`, `memorizar` |
| `termosDicionario` | string[] | ids de termos do `dicionario/` que viram links clicáveis no resumo final |
| `fontes` | string[] | referências gerais usadas na redação do caso |

A pontuação de cada etapa de decisão é definida pela própria opção escolhida
(campo `pontos`); o total possível do caso é a soma da melhor opção de cada
etapa de decisão, usado para calcular a porcentagem exibida no resumo.

### Categorias clínicas (21)

Sistema Cardiovascular, Respiratório, Gastrointestinal, Nervoso,
Musculoesquelético, Dermatológico, Geniturinário, Endócrino; Saúde da
Mulher, Saúde do Homem, Pediatria, Geriatria, Saúde Mental; Doenças
Infecciosas, Dor e Inflamação, Alergias, Condições Crônicas, Urgências e
Sinais de Alerta, Problemas Relacionados a Medicamentos, Intoxicações e
Automedicação — todas com pelo menos 2 casos, 3 questões de quiz e 3
flashcards cadastrados.

## Sistema de pontuação, progresso e conquistas

Salvo em `localStorage` (`desafioclinico-progresso`): casos resolvidos,
pontos totais, sequência de dias consecutivos de uso, questões respondidas
no quiz e taxa de acerto, acertos por competência (`sinal-alerta`,
`farmacoterapia`, `diferencial`, `conduta`, `orientacao`, `exames`) e por
categoria, conquistas desbloqueadas e cartões de flashcard marcados como
difíceis. As 10 conquistas (`conquistas.json`) são recalculadas a cada
caso/quiz/flashcard concluído, com aviso visual (toast) ao desbloquear uma
nova.

## Verificação (Playwright headless, `/opt/pw-browsers/chromium`, servido via
`python3 -m http.server` local)

- 42 casos, 63 questões e 63 flashcards carregados corretamente via `fetch`;
  validação programática prévia (script `merge_validate.py`) checou ids
  duplicados, categorias inválidas, opções de decisão incompletas, índice de
  resposta correta do quiz e — mais importante — que todo id em
  `termosDicionario` existe de fato nos 293 termos do dicionário publicado.
- Larguras 320/390/768/1024/1440px × temas claro/escuro: overflow horizontal
  zero em todas as combinações testadas.
- Fluxo completo de um caso clínico testado do início ao fim (queixa →
  decisões → resumo final), com pontuação calculada corretamente.
- Fluxo completo de quiz (5 questões) testado do início ao resultado final.
- Fluxo de flashcards testado: virar cartão, marcar "não sei" e registro em
  `cartoesDificeis`.
- Sistema de conquistas testado: conquista "Primeiro Caso" desbloqueada
  corretamente após o primeiro caso resolvido, com toast exibido.
- Nenhum erro de console além dos já conhecidos do ambiente sandbox de teste
  (rede/favicon), sem relação com o código da aplicação.

## Link na página inicial

O item "Desafio Clínico" foi ativado em `- INDEX/index.html` tanto no grid
principal de ferramentas (`tools-hub-card`) quanto na lista lateral
(`sidebar-item tool-shortcut`), reaproveitando a cor (`--c-lime`) e o ícone
de alvo já reservados para essa ferramenta nos dois placeholders.

## Próximos candidatos naturais para expansão

- Mais casos por categoria (a especificação original imaginava um banco
  bem maior); a estrutura de dados já suporta isso sem mudanças em `index.html`.
- Integração de dados em tempo real com `interacoes/` e `exames/` (geração
  de casos a partir do banco real dessas ferramentas), adiada nesta versão
  por complexidade técnica.
- Personagens/perfis de paciente variáveis automaticamente, motor de geração
  dinâmica de casos e adaptação automática de dificuldade — funcionalidades
  avançadas da especificação original, propositalmente adiadas para uma
  Fase 2 após validação do uso real desta v1.
