# Dicionário de dados

## Proveniência

Todas as tabelas desta pasta derivam do log de sessões do EpidBot, uma tabela que
registra cada turno da conversa junto com a conta, o grupo de trabalho, o carimbo de
data e hora e as chamadas de ferramenta emitidas naquele turno. O log existe para
fins operacionais e administrativos. Não é um registro de pesquisa e não foi
desenhado para esta análise.

A extração foi executada quatro vezes (ver `usage_snapshots.csv`). Cada extração
aplicou o mesmo procedimento:

1. Restringir aos turnos entre `period_start` e `period_end`.
2. Contar sessões, mensagens, contas ativas distintas e perguntas de usuário.
3. Agregar por grupo de trabalho e por dia da semana.
4. Descartar identificadores de conta, de sessão, texto de mensagem e metadados de
   rede antes de o agregado sair do ambiente de produção.

As quatro extrações são mantidas porque a plataforma estava em operação durante a
redação do manuscrito. A diferença entre S1 e S4 é crescimento, não erro de extração.

## `usage_snapshots.csv`

| Coluna | Tipo | Significado |
| --- | --- | --- |
| `snapshot_id` | texto | Rótulo da extração, S1 a S4 em ordem cronológica |
| `snapshot_date` | data | Data em que a extração rodou |
| `total_sessions` | inteiro | Sessões distintas com ao menos um turno na janela |
| `total_messages` | inteiro | Todos os turnos, de usuário e de assistente, na janela |
| `active_users` | inteiro | Contas distintas com ao menos um turno na janela |
| `user_questions` | inteiro | Turnos de usuário classificados como pergunta ou pedido |
| `period_start` | data | Primeiro dia da janela |
| `period_end` | data | Último dia da janela |

S1 e S2 compartilham a janela e diferem apenas na data de extração; são idênticas
porque nenhum turno chegou entre elas. S3 e S4 também compartilham a data e diferem
em seis mensagens, o que é o efeito esperado de uma escrita tardia.

## `usage_by_group.csv`

Os mesmos indicadores, uma linha por grupo de trabalho, retirados da extração S4. Os
rótulos dos grupos são substituídos por códigos pseudônimos, de modo que o arquivo pode
ser distribuído.

| Coluna | Tipo | Significado |
| --- | --- | --- |
| `group_id` | texto | Código pseudônimo, G01 a G12, atribuído em ordem aleatória |
| `segment` | texto | Contexto agregado do usuário: interno de desenvolvimento, interno de testes, externo acadêmico, externo governamental, externo internacional, externo aberto |
| `users_band` | texto | Contas ativas em faixas: 1-2, 3-5, 6-10, 11-20, mais de 20 |
| `active_users` | inteiro | Contas distintas no grupo, presente apenas quando o grupo tem seis ou mais contas |
| `sessions`, `messages`, `user_questions` | inteiro | Como acima |
| `messages_per_session` | decimal | Mensagens divididas por sessões, reportado para todos os grupos |
| `messages_per_user` | decimal | Mensagens divididas por contas ativas, omitido abaixo de seis contas |
| `period_start`, `period_end` | data | Primeiro e último turno observado no grupo |
| `disclosure_note` | texto | Motivo da omissão de um valor, vazio quando nada foi omitido |

Os códigos foram atribuídos em ordem aleatória sob semente fixa, portanto nem o código
nem a ordem das linhas carregam informação sobre tamanho, escopo ou cronologia. O
mapeamento entre códigos e rótulos fica em uma chave interna que não integra este
repositório. Taxas por conta são omitidas para grupos com menos de seis contas, porque
uma taxa sobre uma ou duas contas descreve essas contas individualmente.

**As linhas não são aditivas.** Grupos são rótulos de trabalho, não partições: uma
conta pode pertencer a vários grupos, e os dois grupos internos (`G05` e
`G09`) compartilham contas por construção. A soma das linhas de grupo é
maior que o total geral e isso é esperado. As contagens por grupo são descritivas de
cada grupo e nunca são usadas para construir um total geral.

## `messages_by_weekday.csv`

| Coluna | Tipo | Significado |
| --- | --- | --- |
| `weekday` | texto | Segunda a domingo |
| `messages` | inteiro | Todos os turnos naquele dia da semana, extração S4 |

Esta tabela é aditiva: as sete linhas somam `total_messages` em S4. O script em
`analysis/` verifica essa invariante.

## `question_taxonomy.csv`

| Coluna | Tipo | Significado |
| --- | --- | --- |
| `category_id` | texto | C1 a C8 |
| `category_en`, `category_pt` | texto | Rótulo da categoria nos dois idiomas |
| `evidence` | texto | Peso qualitativo na amostra: dominante, secundária ou marginal |
| `example_query_en`, `example_query_pt` | texto | Pedido representativo, parafraseado |

A taxonomia é qualitativa. Foi construída lendo as perguntas amostradas e agrupando
por intenção. Não são relatadas contagens por categoria, porque a amostra de
perguntas não é aleatória em relação a todos os turnos e uma contagem sugeriria uma
precisão que os dados não sustentam. A coluna `evidence` registra apenas se uma
categoria recorre com frequência, ocorre ou aparece ocasionalmente.

## Ressalvas conhecidas

- `total_messages` conta turnos do assistente além dos turnos do usuário. A razão
  entre mensagens e perguntas reflete profundidade da conversa, não esforço do
  usuário.
- `user_questions` depende de um classificador sobre turnos de usuário; é um limite
  inferior, porque pedidos no imperativo às vezes não são formulados como pergunta.
- As janelas dos grupos diferem (um grupo ativo apenas em junho tem janela de junho).
  A comparação de taxas entre grupos deve usar
  `messages / active_users / dias da janela do grupo`, não totais brutos.
- A plataforma estava em desenvolvimento ativo durante a janela de observação, então
  a disponibilidade de ferramentas mudou ao longo do tempo. O crescimento de uso é,
  portanto, efeito conjunto de adoção e de liberação de capacidades, e não pode ser
  lido como adoção isolada.
