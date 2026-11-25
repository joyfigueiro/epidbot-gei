# 06. Ética, proteção de dados e limitações

Este documento declara como os dados pessoais são tratados, onde termina o escopo do
sistema e quais limitações devem ser lidas junto com os resultados da Seção 5.

## Dados pessoais

A evidência de uso em `data/` foi produzida para análise administrativa de uma ferramenta
em operação. Ela foi minimizada antes da publicação. A agregação ocorreu na fronteira de
extração, de modo que identificadores nunca saíram do ambiente de produção, e as tabelas
deste repositório não contêm identificador de usuário, endereço de e-mail, identificador de
sessão, texto de mensagem nem metadados de rede.

Os rótulos dos grupos foram substituídos por códigos atribuídos em ordem aleatória
antes da publicação, de modo que nem os códigos nem a ordem das linhas carregam
informação sobre tamanho, escopo ou cronologia. O número de contas ativas é apresentado
em faixas, e taxas por conta são omitidas para grupos com menos de seis contas, de modo
que nenhuma célula publicada descreve uma ou duas contas identificáveis. O material é
compatível com a Lei Geral de Proteção de Dados porque não
contém dado pessoal na definição do Artigo 5º, I. Usuários são identificados nos relatórios
internos apenas para fins administrativos, e esses relatórios não fazem parte deste
repositório.

## Fronteiras de escopo

O sistema responde perguntas epidemiológicas sobre populações. Orientação clínica
individual está fora do escopo, e quando um pedido cruza essa fronteira a resposta
adequada é dizer isso e não responder. O registro de uso mostra que essa fronteira é
testada na prática, e é por isso que ela aparece como regra de projeto e não apenas como
aviso.

Documentos enviados por um usuário são tratados como dados, não como instruções. Essa é a
defesa prática contra conteúdo que tenta redirecionar o sistema pelo próprio conteúdo
enviado.

## Verificação de afirmações

Números que aparecem em um relatório vêm de resultado de operação ou do script que montou
a tabela, nunca da memória do modelo. Referências bibliográficas são resolvidas contra APIs
bibliográficas antes de serem citadas, e uma referência que não resolve é descartada em vez
de mantida com um identificador de aparência plausível. Quando uma fonte não tem dados para
um período, o sistema relata a ausência em vez de interpolar em silêncio.

## Limitações

- **Cobertura.** O substrato é centrado no Brasil. Perguntas sobre outros países só são
  respondíveis onde uma fonte internacional os cobre.
- **Latência e revisão.** Períodos recentes são provisórios, e resultados calculados em
  datas diferentes podem diferir por razões legítimas.
- **Não determinismo.** O mesmo pedido pode tomar caminhos diferentes e produzir respostas
  redigidas de outro modo. Os números continuam rastreáveis, a narrativa não se repete
  literalmente.
- **Custo.** Planos complexos consomem tempo e tokens. O projeto aceita esse custo em troca
  da capacidade de responder perguntas não previstas.
- **Avaliação.** Este repositório relata uso, não acurácia. Uma avaliação formal contra
  perguntas epidemiológicas de referência, com respostas estabelecidas por especialistas, é
  o passo seguinte natural e não é relatada aqui.
- **Evidência de desfecho.** O registro de uso mostra que as sessões aconteceram e o que foi
  perguntado. Não mostra que cada sessão terminou em análise concluída. Afirmações sobre
  utilidade no manuscrito são, portanto, sobre processo e não sobre desfecho.
