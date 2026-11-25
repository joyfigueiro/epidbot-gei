# Material suplementar: Inteligência Epidemiológica Generalizada e a arquitetura do EpidBot

Este repositório reúne o material suplementar do manuscrito

> **Generalized Epidemic Intelligence: an agentic architecture for automated,
> LLM-driven and adaptive epidemiological investigation**
> Joyce Figueiró Braga, Flávio Codeço Coelho, Beatriz Laiate
> (submetido à Springer)

Versão em inglês: [README.md](README.md). Todos os documentos deste repositório
existem nos dois idiomas, com o mesmo conteúdo e os mesmos nomes de arquivo em
`docs/en/` e `docs/pt/`.

---

## 1. O que há aqui

| Item | Onde | Corresponde a |
| --- | --- | --- |
| Documentação das quatro camadas arquiteturais | `docs/pt/01_arquitetura.md` | Seção 4.1 |
| Como um pedido em linguagem natural vira um plano analítico | `docs/pt/02_do_pedido_ao_plano.md` | Seção 4.2 |
| Orquestração, despacho de ferramentas e reparo adaptativo | `docs/pt/03_orquestracao.md` | Seção 4.3 |
| Proveniência, rastreabilidade e reprodutibilidade | `docs/pt/04_rastreabilidade.md` | Seção 4.4 |
| Famílias de dados alcançáveis pelo sistema | `docs/pt/05_fontes_de_dados.md` | Seção 4.1 |
| Ética, proteção de dados e limitações conhecidas | `docs/pt/06_etica_e_limitacoes.md` | Seções 4.4 e 6 |
| Figura da arquitetura | `docs/figures/fig_architecture.png` | Figura 4 |
| Evidência agregada de uso | `data/*.csv` | Seção 5 |
| Corpus codificado de prompts, marginais de capacidade e figuras de auditoria | `data/audit/`, `figures/audit/` | Seções 4.4 e 5 |
| Código que reconstrói cada tabela a partir dos agregados | `analysis/` | Seção 5 |
| Tabelas em LaTeX prontas para colar no manuscrito | `supplementary/*.tex` | Tabelas suplementares S1 a S3 |
| Implementação de referência da pseudonimização | `analysis/pseudonymise_groups.py` | Seção 3.1 |

## 2. O que não há aqui

O código-fonte da aplicação EpidBot não é distribuído neste repositório. O que se
distribui é (i) a documentação que descreve a arquitetura, (ii) a evidência agregada
que sustenta a análise de uso e (iii) o código que transforma essa evidência nas
tabelas relatadas no manuscrito. Qualquer leitor pode, portanto, verificar a
aritmética e as escolhas de agregação por trás de cada número da Seção 5 sem acesso
ao sistema em produção.

## 3. Dados

`data/usage_snapshots.csv` registra quatro extrações sucessivas do log de sessões,
permitindo checar o crescimento entre as datas de extração.
`data/usage_by_group.csv` registra os mesmos indicadores por grupo de usuários.
`data/messages_by_weekday.csv` registra o ritmo semanal do volume de mensagens.
`data/question_taxonomy.csv` registra as oito categorias analíticas usadas para
descrever o que os usuários perguntam, com exemplos parafraseados representativos.

Todos os arquivos são agregados. Nenhum identificador de usuário, endereço de
e-mail, identificador de sessão, texto de mensagem ou endereço IP está incluído.
Ver `data/DICIONARIO_DE_DADOS.md` e `docs/pt/06_etica_e_limitacoes.md`.

### 3.1 Pseudonimização dos grupos de usuários

As contas de usuário no EpidBot podem estar vinculadas a grupos de trabalho. Os
rótulos dos grupos foram atribuídos pelas equipes que implantaram a plataforma e
carregam significado institucional, portanto não fazem parte da afirmação científica
e não são publicados. Cada grupo aparece sob um código de `G01` a `G12`. Os códigos
foram atribuídos em ordem aleatória sob semente fixa, de modo que nem o código nem a
ordem das linhas carregam informação sobre tamanho, escopo ou cronologia. O mapeamento
entre códigos e rótulos fica em uma chave interna que não integra este repositório;
revisores podem solicitá-la ao autor correspondente.

Três precauções valem para `data/usage_by_group.csv`. O número de contas ativas é
apresentado em faixas de uma a duas, três a cinco, seis a dez, onze a vinte, e mais de
vinte, e a contagem exata aparece apenas para grupos com seis ou mais contas. Taxas
por conta são omitidas abaixo desse limiar, porque uma taxa calculada sobre uma ou
duas contas descreve essas contas individualmente. Taxas por sessão são reportadas
para todos os grupos, já que agregam contas distintas e não descrevem uma pessoa.

> **Sobre a aditividade.** Os grupos de usuários não são mutuamente exclusivos: uma
> mesma conta pode pertencer a mais de um grupo, e os dois grupos internos (`G05` e
> `G09`) compartilham contas. As linhas de `usage_by_group.csv` não somam os totais
> gerais de `usage_snapshots.csv` e não devem ser somadas.

## 4. Reprodução

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r analysis/requirements.txt
python analysis/build_usage_tables.py --input data --output supplementary
```

O script verifica as duas invariantes que a extração precisa satisfazer (as contagens
por dia da semana somam o total de mensagens; nenhuma linha de grupo excede o total
geral) e grava as três tabelas LaTeX em `supplementary/`. A saída esperada para os dados
atuais está em `supplementary/EXPECTED_OUTPUT.md`.

## 5. Ética e proteção de dados

A evidência de uso foi produzida para análise administrativa de uma ferramenta de
saúde pública em operação. Ela foi minimizada antes da publicação: o pipeline de
extração agregou o log de sessões e descartou identificadores, e apenas agregados
saíram do ambiente de produção. Os rótulos dos grupos foram substituídos por códigos
atribuídos em ordem aleatória antes da publicação, e taxas por conta são omitidas para
grupos com menos de seis contas, de modo que nenhuma célula descreve uma ou duas contas
identificáveis. O material é compatível com a Lei Geral de Proteção de Dados
(Lei 13.709/2018) porque não contém dado pessoal na definição do Artigo 5º, I.

## 6. Licença

Texto, figuras e tabelas de dados: Creative Commons Atribuição 4.0 Internacional
(CC BY 4.0), ver `LICENSE`.
Código em `analysis/`: MIT, ver `LICENSE-CODE`.

## 7. Como citar

Ver `CITATION.cff`. Se usar os dados agregados, cite o manuscrito e este repositório,
com a tag de versão.

## 8. Contato

Joyce Figueiró Braga, Escola de Matemática Aplicada, Fundação Getúlio Vargas,
Rio de Janeiro, Brasil. joyce.braga@fgv.br
