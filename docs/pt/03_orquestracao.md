# 03. Orquestração e execução adaptativa

Este documento desenvolve a Seção 4.3. Descreve o laço de execução, o despacho de
operações tipadas e as formas específicas pelas quais o sistema se adapta quando um passo
falha.

## O laço

A execução é um laço de quatro passos: planejar, despachar, observar, decidir. Cada
iteração consome o resultado de uma ou mais operações e produz um de três desfechos:
resposta final, plano revisado ou pergunta ao usuário. O laço é limitado, então um sistema
que não chega à resposta para e diz isso, em vez de continuar procurando.

## Despacho tipado

O despachante fica entre o modelo e a operação. Valida argumentos contra o esquema, recusa
chamadas cujas pré-condições falham e normaliza o que volta em um conjunto pequeno de
classes de erro. É essa normalização que torna a adaptação possível: o sistema reage a
cinco classes, não a um espaço aberto de mensagens de erro.

## Estratégias de adaptação

| Classe observada | Estratégia | Exemplo |
| --- | --- | --- |
| Resultado vazio | Ampliar o escopo ou mudar para fonte vizinha que cubra o período | Série municipal sem registros no ano pedido é reconsultada em nível estadual para confirmar que a lacuna é real |
| Tempo esgotado | Reduzir escopo, dividir espacialmente ou usar método mais leve | Consulta nacional é executada estado por estado |
| Esquema incompatível | Releitura do descritor e recodificação do argumento | Coluna de data guardada como inteiro é convertida antes da agregação |
| Valor implausível | Rever unidades e recalcular a partir da tabela bruta | Taxa por cem mil é conferida contra contagens e população |
| Capacidade ausente | Degradar para resposta descritiva e declarar o que falta | Pergunta sobre doença sem fonte registrada devolve declaração da lacuna |

## Orçamentos e regras de parada

Três regras limitam o laço. Um número máximo de iterações, um limite de tempo de parede e
a exigência de que toda resposta final cite pelo menos um resultado de operação. A
terceira regra é a que importa para a confiança: ela converte uma afirmação sem suporte em
lacuna visível.

## Trabalho paralelo e sequencial

Operações independentes são despachadas juntas, o que reduz o tempo de parede de perguntas
com múltiplas fontes. Operações que dependem de resultado anterior são sequenciadas. A
distinção é declarada no plano, não descoberta durante a execução.

## Por que isto não é um pipeline fixo

Um pipeline codifica a análise de antemão, que é exatamente o que a inteligência
epidemiológica generalizada pretende evitar. Aqui a análise é escolhida em tempo de
execução. O preço dessa escolha é variabilidade: a mesma pergunta pode tomar caminhos
diferentes em dias diferentes. O remédio não é remover a variabilidade, e sim registrar o
caminho, que é o tema de `04_rastreabilidade.md`.
