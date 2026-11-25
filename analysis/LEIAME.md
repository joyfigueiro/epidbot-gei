# Código de análise

Um script, um trabalho: transformar as tabelas agregadas de `data/` nas tabelas LaTeX de
`supplementary/` e verificar se os agregados são internamente consistentes.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build_usage_tables.py --input ../data --output ../supplementary
```

## O que ele faz

| Função | Saída |
| --- | --- |
| `load_tables` | Lê os quatro CSVs e falha de forma explícita se faltar coluna obrigatória |
| `check_invariants` | Executa as verificações listadas abaixo |
| `table_s1_groups` | `supplementary/table_s1_usage_by_group.tex` |
| `table_s2_snapshots` | `supplementary/table_s2_snapshots.tex` |
| `table_s3_weekday` | `supplementary/table_s3_weekday.tex` |
| `expected_output_markdown` | `supplementary/EXPECTED_OUTPUT.md` |

## Verificações

1. As contagens por dia da semana somam o total geral de mensagens. Esta é a tabela que
   precisa ser aditiva.
2. Nenhum grupo excede o total geral de mensagens.
3. A soma das linhas de grupo excede o total geral, que é a consequência esperada de os
   grupos não serem partições.
4. Os totais de mensagens não diminuem entre extrações.
5. Extrações que compartilham a mesma janela diferem apenas marginalmente.

O script termina com status 1 se alguma verificação falhar, então pode ser usado como
teste de regressão sobre os arquivos de dados.

## Por que não há contagem por categoria

`data/question_taxonomy.csv` é uma classificação qualitativa. A amostra de perguntas a
partir da qual ela foi construída não é uma amostra aleatória de todos os turnos, então
uma contagem por categoria sugeriria uma precisão que os dados não sustentam. A tabela
relata presença, não frequência.

## Estilo do código

O script usa anotações de tipo explícitas, docstring em toda função e nenhum estado
global. Ele lê apenas da pasta passada em `--input` e escreve apenas na pasta passada em
`--output`, de modo que pode ser executado contra uma cópia dos dados sem tocar no
repositório.
