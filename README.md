# Supplementary material: Generalized Epidemic Intelligence and the EpidBot architecture

This repository holds the supplementary material for the manuscript

> **Generalized Epidemic Intelligence: an agentic architecture for automated,
> LLM-driven and adaptive epidemiological investigation**
> Joyce Figueiro Braga, Flavio Codeco Coelho, Beatriz Laiate
> (submitted to Springer)

Portuguese version: [README.pt-BR.md](README.pt-BR.md). Every document in this
repository exists in both languages, with the same content and the same file names
under `docs/en/` and `docs/pt/`.

---

## 1. What is in here

| What | Where | Corresponds to |
| --- | --- | --- |
| Documentation of the four architectural layers | `docs/en/01_architecture.md` | Section 4.1 |
| How a free-text request becomes an analytical plan | `docs/en/02_request_to_plan.md` | Section 4.2 |
| Orchestration, tool dispatch and adaptive repair | `docs/en/03_orchestration.md` | Section 4.3 |
| Provenance, traceability and reproducibility | `docs/en/04_traceability.md` | Section 4.4 |
| Data families reachable by the system | `docs/en/05_data_sources.md` | Section 4.1 |
| Ethics, data protection and known limitations | `docs/en/06_ethics_and_limitations.md` | Sections 4.4 and 6 |
| Architecture figure | `docs/figures/fig_architecture.png` | Figure 4 |
| Aggregate usage evidence | `data/*.csv` | Section 5 |
| Coded prompt corpus, capability marginals and audit figures | `data/audit/`, `figures/audit/` | Sections 4.4 and 5 |
| Code that rebuilds every table from the raw aggregates | `analysis/` | Section 5 |
| LaTeX tables ready to paste into the manuscript | `supplementary/*.tex` | Supplementary Tables S1 to S3 |
| Reference implementation of the pseudonymisation step | `analysis/pseudonymise_groups.py` | Section 3.1 |

## 2. What is not in here

The EpidBot application source code is not distributed in this repository. What is
distributed is (i) the documentation that describes the architecture, (ii) the
aggregate evidence that supports the usage analysis, and (iii) the code that turns
that evidence into the tables reported in the manuscript. Anyone can therefore
verify the arithmetic and the aggregation choices behind every number in Section 5
without access to the deployed system.

## 3. Data

`data/usage_snapshots.csv` records four successive extractions of the session log,
so that growth between extraction dates can be checked.
`data/usage_by_group.csv` records the same indicators broken down by user group.
`data/messages_by_weekday.csv` records the weekly rhythm of message volume.
`data/question_taxonomy.csv` records the eight analytic categories used to describe
what users ask, with representative paraphrased examples.

All files are aggregates. No user identifier, e-mail address, session identifier,
message text or IP address is included. See `data/DATA_DICTIONARY.md` and
`docs/en/06_ethics_and_limitations.md`.

### 3.1 Pseudonymisation of user groups

User accounts in EpidBot can be attached to working groups. Group labels were
assigned by the deploying teams and carry institutional meaning, so they are not part
of the scientific claim and are not published. Each group appears under a code from
`G01` to `G12`. The codes were assigned in random order under a fixed seed, so neither
the code nor the row order carries information about group size, scope or chronology.
The mapping between codes and labels is kept in an internal key that is not part of
this repository; reviewers can request it from the corresponding author.

Three precautions apply to `data/usage_by_group.csv`. Active accounts are reported in
bands of one to two, three to five, six to ten, eleven to twenty, and more than twenty,
and the exact count appears only for groups with six or more accounts. Rates per
account are withheld below that threshold, because a rate computed over one or two
accounts describes those accounts individually. Rates per session are reported for
every group, since they aggregate distinct accounts and do not describe a person.

> **Note on additivity.** User groups are not mutually exclusive: a single account
> can belong to more than one group, and the two internal groups (`G05` and `G09`)
> share accounts. Rows of `usage_by_group.csv` therefore do not sum to the all-user
> totals in `usage_snapshots.csv`, and must not be added.

## 4. Reproduction

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r analysis/requirements.txt
python analysis/build_usage_tables.py --input data --output supplementary
```

The script validates the invariants that the extraction must satisfy (weekday
counts sum to the message total; no group row exceeds the all-user total) and writes
the three LaTeX tables into `supplementary/`. Expected output for the current data is in
`supplementary/EXPECTED_OUTPUT.md`.

## 5. Ethics and data protection

The usage evidence was produced for administrative analysis of a deployed public
health tool. It was minimised before publication: the extraction pipeline aggregated
the session log and discarded identifiers, and only aggregates left the production
environment. Group labels were replaced by codes assigned in random order before
publication, and rates per account are withheld for groups with fewer than six
accounts, so that no cell describes one or two identifiable accounts. The material is compatible with the Brazilian General
Data Protection Law (Lei 13.709/2018) because it contains no personal data as defined
by Article 5, I.

## 6. License

Text, figures and data tables: Creative Commons Attribution 4.0 International
(CC BY 4.0), see `LICENSE`.
Code in `analysis/`: MIT, see `LICENSE-CODE`.

## 7. How to cite

See `CITATION.cff`. If you use the aggregate data, please cite both the manuscript
and this repository, with its version tag.

## 8. Contact

Joyce Figueiro Braga, School of Applied Mathematics, Fundacao Getulio Vargas,
Rio de Janeiro, Brazil. joyce.braga@fgv.br
