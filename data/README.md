
# Data files / Arquivos de dados

Four aggregate tables, no personal data. Quatro tabelas agregadas, sem dado pessoal.

| File | Rows | English | Português |
| --- | --- | --- | --- |
| `usage_snapshots.csv` | 4 | Successive extractions of the session log | Extrações sucessivas do log de sessões |
| `usage_by_group.csv` | 12 | Indicators by workspace group (not additive) | Indicadores por grupo de trabalho (não aditivo) |
| `messages_by_weekday.csv` | 7 | Message volume by weekday (additive) | Volume de mensagens por dia da semana (aditivo) |
| `question_taxonomy.csv` | 8 | Qualitative categories of user requests | Categorias qualitativas dos pedidos dos usuários |

Full documentation / Documentação completa:
[`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) (English) ·
[`DICIONARIO_DE_DADOS.md`](DICIONARIO_DE_DADOS.md) (Português).

Rebuild the manuscript tables from these files with `analysis/build_usage_tables.py`.
Reconstrua as tabelas do manuscrito a partir destes arquivos com
`analysis/build_usage_tables.py`.
