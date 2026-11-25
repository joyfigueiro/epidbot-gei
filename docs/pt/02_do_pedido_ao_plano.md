# 02. Do pedido ao plano analítico

Este documento desenvolve a Seção 4.2. Descreve a sequência pela qual um pedido
epidemiológico em linguagem natural se torna um plano executável e os pontos em que o
sistema para para perguntar em vez de adivinhar.

## Etapas

1. **Captura da intenção.** O pedido é guardado literalmente. Ele permanece como
   referência contra a qual a resposta final é conferida, porque um plano pode se afastar
   da pergunta que deveria responder.
2. **Resolução de escopo.** Cinco dimensões são extraídas: doença ou evento de saúde,
   lugar, janela temporal, granularidade espacial e temporal, e base de comparação. Cada
   dimensão é explícita, inferida da conversa ou ausente. Ausente é um estado distinto e
   não é preenchido com um valor padrão.
3. **Consulta ao catálogo.** O planejador busca conjuntos de dados registrados que
   satisfaçam o escopo. Ele vê descritores, não dados. Esta etapa é o que impede o sistema
   de prometer uma análise que o substrato não sustenta.
4. **Seleção de capacidades.** As operações são escolhidas do registro conforme o escopo e
   os dados disponíveis.
5. **Montagem do plano.** Os passos são organizados como grafo acíclico dirigido, com
   entradas e saídas declaradas, para que falhas parciais possam ser localizadas.
6. **Verificação prévia.** Cobertura, unidades, granularidade, tempo de execução esperado
   e, principalmente, se o plano responde à pergunta feita.
7. **Esclarecimento.** Quando uma dimensão ausente mudaria materialmente a resposta, o
   sistema pergunta antes de rodar. Quando não mudaria, ele declara a suposição adotada e
   prossegue.

## Um exemplo trabalhado

O pedido *como a dengue se comportou em Campinas em 2024* se resolve assim. Doença é
dengue. Lugar é Campinas, que resolve para o código IBGE 3509502. Tempo é o ano
epidemiológico de 2024. A granularidade é semanal, porque a pergunta trata do
comportamento ao longo do tempo e não de um total anual. O desfecho são casos notificados.
A base de comparação para um diagrama de controle são os cinco anos anteriores.

O plano então busca a lista de notificações de dengue do município, agrega por semana
epidemiológica, calcula incidência contra a população municipal, constrói o diagrama de
controle com o canal endêmico, produz figura e tabela e anexa o registro de proveniência.
Cada um desses passos é uma operação nomeada. Nenhum deles é um parágrafo de instruções
para um modelo.

## Como a ambiguidade é tratada

A ambiguidade é resolvida antes da execução quando o custo de uma execução errada é alto,
por exemplo um download que leva minutos. É resolvida depois da execução quando o próprio
resultado revela o problema, por exemplo tabela vazia ou taxa de incidência implausível
para o lugar e o período. Os dois casos são registrados, de modo que o leitor vê quais
suposições foram feitas e quais foram corrigidas.

## O que o plano não é

O plano não é um script. Ele não fixa a sequência de chamadas de antemão e não é
reutilizado literalmente entre perguntas. Ele registra o caminho pretendido, e o caminho
pode ser revisado durante a execução, como descrito em `03_orquestracao.md`.
