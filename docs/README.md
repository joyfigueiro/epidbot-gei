# Documentation index / Índice da documentação

Every document exists twice, once in English and once in Portuguese, with the same
content. The file names differ only in language.

Cada documento existe duas vezes, uma em inglês e uma em português, com o mesmo
conteúdo. Os nomes de arquivo diferem apenas no idioma.

| Topic / Tema | English | Português | Manuscript section |
| --- | --- | --- | --- |
| Architecture and integration / Arquitetura e integração | [en/01_architecture.md](en/01_architecture.md) | [pt/01_arquitetura.md](pt/01_arquitetura.md) | 4.1 |
| From request to analytical plan / Do pedido ao plano analítico | [en/02_request_to_plan.md](en/02_request_to_plan.md) | [pt/02_do_pedido_ao_plano.md](pt/02_do_pedido_ao_plano.md) | 4.2 |
| Orchestration and adaptive execution / Orquestração e execução adaptativa | [en/03_orchestration.md](en/03_orchestration.md) | [pt/03_orquestracao.md](pt/03_orquestracao.md) | 4.3 |
| Traceability and reproducibility / Rastreabilidade e reprodutibilidade | [en/04_traceability.md](en/04_traceability.md) | [pt/04_rastreabilidade.md](pt/04_rastreabilidade.md) | 4.4 |
| Data sources / Fontes de dados | [en/05_data_sources.md](en/05_data_sources.md) | [pt/05_fontes_de_dados.md](pt/05_fontes_de_dados.md) | 4.1 |
| Ethics and limitations / Ética e limitações | [en/06_ethics_and_limitations.md](en/06_ethics_and_limitations.md) | [pt/06_etica_e_limitacoes.md](pt/06_etica_e_limitacoes.md) | 4.4, 6 |

## Figures / Figuras

`figures/fig_architecture.png` is the four-layer architecture diagram, reproduced as
Figure 4 in the manuscript. The Graphviz source is in `figures/src/fig_architecture.dot`
and can be rendered with:

```bash
dot -Tpng figures/src/fig_architecture.dot -o figures/fig_architecture.png
```

`figures/fig_architecture.png` é o diagrama da arquitetura em quatro camadas, reproduzido
como Figura 4 no manuscrito. A fonte Graphviz está em
`figures/src/fig_architecture.dot` e pode ser renderizada com o comando acima.

## Section 5 documentation / Documentação da Seção 5

The Section 5 evidence package is documented in
[`../section_05_deployment_and_use/`](../section_05_deployment_and_use/), starting from
its `README.md`, with methods in `methodology/SECTION5_METHODS.md` and the
consistency audit in `methodology/CONSISTENCY_AUDIT.md`.

**Language exception.** Unlike the documents above, the Section 5 package is currently
English-only. It feeds an English manuscript, it is revised daily during writing, and
keeping two parallel versions in sync at that cadence would create drift. Portuguese
versions will be produced once Section 5 is frozen. The bilingual convention continues
to hold for every document listed in the table above.

O pacote de evidências da Seção 5 está documentado em
[`../section_05_deployment_and_use/`](../section_05_deployment_and_use/), a partir do
`README.md`, com os métodos em `methodology/SECTION5_METHODS.md` e a auditoria de
consistência em `methodology/CONSISTENCY_AUDIT.md`.

**Exceção de idioma.** Diferentemente dos documentos acima, o pacote da Seção 5 está
por ora apenas em inglês. Ele alimenta um manuscrito em inglês e é revisado diariamente
durante a redação; manter duas versões paralelas nessa cadência criaria divergência. As
versões em português serão produzidas quando a Seção 5 estiver congelada. A convenção
bilíngue continua valendo para todos os documentos da tabela acima.
