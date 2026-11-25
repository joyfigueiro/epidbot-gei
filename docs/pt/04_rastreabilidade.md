# 04. Rastreabilidade e reprodutibilidade

Este documento desenvolve a Seção 4.4. Descreve o que é registrado durante uma
investigação, o que esse registro torna possível e onde ficam os limites da
reprodutibilidade.

## Três registros

| Registro | Conteúdo | Finalidade |
| --- | --- | --- |
| Log de sessão | Todo turno, toda chamada de operação, seus argumentos e um resumo do resultado | Reconstrói o que o usuário pediu e o que o sistema fez |
| Registro de proveniência | Conjuntos de dados usados com versão e data de extração, operações em ordem, parâmetros, avisos | Torna cada número atribuível |
| Artefatos | Figuras, tabelas e relatórios com hora de criação e hash de conteúdo | Permite ao leitor conferir que o arquivo que tem é o arquivo que foi produzido |

## O que torna uma execução reprodutível

O não determinismo é inevitável quando um modelo de linguagem escolhe o caminho. O que se
torna reprodutível é o caminho analítico, não a redação. A sequência ordenada de operações,
seus argumentos e as versões dos dados bastam para recalcular os números, mesmo que uma
nova execução redija a narrativa de outro jeito. A reprodutibilidade é, portanto,
propriedade do registro e não do modelo.

## Proveniência mínima para um número

Todo número em um relatório gerado precisa remontar a uma operação, uma versão de conjunto
de dados e um conjunto de argumentos. O construtor de relatórios aceita apenas valores
devolvidos por uma operação ou calculados pelo script que montou a tabela. Número escrito
de memória do modelo não é admitido em relatório. Esta regra é imposta na montagem, não
solicitada no comando.

## Onde a reprodutibilidade termina

Três limites devem ser declarados explicitamente em qualquer uso do sistema.

- Uma nova execução pode tomar caminho diferente e igualmente válido, então a sequência de
  operações não é garantidamente idêntica.
- Os dados de origem são revisados. Uma execução meses depois pode legitimamente produzir
  números diferentes para o mesmo pedido, e o registro de proveniência mostrará por quê.
- O registro documenta o que foi feito, não se era a coisa certa a fazer. Julgar a
  adequação continua sendo tarefa humana, e é por isso que a etapa de revisão existe como
  estágio separado e não como parte da resposta.
