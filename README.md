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
| Section 5 evidence package: five subsections, methods, consistency audit | `section_05_deployment_and_use/` | Section 5 |
| Section 5 figures (PNG 300 dpi + vector PDF) and LaTeX tables | `section_05_deployment_and_use/figures/`, `tables/` | Section 5 |
| Scripts that rebuild every Section 5 table and figure | `section_05_deployment_and_use/scripts/` | Section 5 |
| Section 5 writing guide and claim-to-evidence map | `SECTION_5_WRITING_GUIDE.md`, `SECTION_5_EVIDENCE_MATRIX.csv` | Section 5 |

## 2. What is not in here

The EpidBot application source code is not distributed in this repository. What is
distributed is (i) the documentation that describes the architecture, (ii) the
aggregate evidence that supports the usage analysis, and (iii) the code that turns
that evidence into the tables reported in the manuscript. Anyone can therefore
verify the arithmetic and the aggregation choices behind every number in Section 5
without access to the deployed system.

## 3. Section 5 — evidence package

Section 5 asks what the operational record shows when the architecture is used. The
evidence is not a set of constructed case studies: it is 227 days of a live platform
(237 active accounts, 667 sessions, 6,967 messages) together with 186 individually
coded user requests.

```
section_05_deployment_and_use/
├── 01_deployment_and_user_base/      who used it, in which contexts
├── 02_patterns_of_platform_use/      how it was used, how concentrated
├── 03_epidemiological_requests/      what users were trying to do (+ CODING_GUIDE.md)
├── 04_gei_capability_composition/    how the five GEI areas were combined
├── 05_real_world_settings/           one traced investigation + 14 archetypes
├── methodology/                      SECTION5_METHODS.md, CONSISTENCY_AUDIT.md, VERIFICATION_REPORT.md
├── figures/                          fig5_1 … fig5_6
├── tables/                           t5_1 … t5_12
└── scripts/                          reproduce_section5.py, make_section5_figures.py
```

Three documents matter most:

- `SECTION_5_WRITING_GUIDE.md` — the writing plan, the canonical numbers, the figure
  captions, the claims that must be removed, and the open decisions.
- `section_05_deployment_and_use/methodology/SECTION5_METHODS.md` — the full methods
  text, including the definitions of every counting unit and the eligibility rule that
  produces the denominator 141.
- `section_05_deployment_and_use/methodology/CONSISTENCY_AUDIT.md` — thirteen itemised
  findings: what reconciles, what is internally inconsistent, and what has no
  supporting evidence at all.

### Verification, not assertion

`reproduce_section5.py` recomputes every prompt-level statistic from the granular
corpus and compares it against the archived marginals. Any disagreement is reported as
a failure rather than silently resolved. An earlier draft of Section 5 quoted a figure
of 10,863 that appears in no file in this repository; the audit records why and what to
use instead.

One convention is deliberately relaxed here: the Section 5 package is English-only for
now, because it is revised daily while the section is being written. The bilingual rule
continues to hold for `docs/en/` and `docs/pt/`.

## 4. Data

`data/usage_snapshots.csv` records four successive extractions of the session log,
so that growth between extraction dates can be checked.
`data/usage_by_group.csv` records the same indicators broken down by user group.
`data/messages_by_weekday.csv` records the weekly rhythm of message volume.
`data/question_taxonomy.csv` records the eight analytic categories used to describe
what users ask, with representative paraphrased examples.

All files are aggregates. No user identifier, e-mail address, session identifier,
message text or IP address is included. See `data/DATA_DICTIONARY.md` and
`docs/en/06_ethics_and_limitations.md`.

### 4.1 Pseudonymisation of user groups

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

## 5. Reproduction

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r analysis/requirements.txt
python analysis/build_usage_tables.py --input data --output supplementary

# Section 5: rebuild every table, then every figure, from the coded corpus
python section_05_deployment_and_use/scripts/reproduce_section5.py
python section_05_deployment_and_use/scripts/make_section5_figures.py
```

`build_usage_tables.py` validates the invariants that the extraction must satisfy
(weekday counts sum to the message total; no group row exceeds the all-user total) and
writes the three LaTeX tables into `supplementary/`; expected output for the current
data is in `supplementary/EXPECTED_OUTPUT.md`.

`reproduce_section5.py` does the same for Section 5: it recomputes the prompt-level
statistics from `data/audit/EXPORT_prompts_anonymised.csv`, compares each result with
the archived marginal, writes 17 derived tables and 12 LaTeX tables, and exits non-zero
if anything disagrees. `make_section5_figures.py` then redraws the figures from those
tables, so no number in a figure is typed by hand.

## 6. Ethics and data protection

The usage evidence was produced for administrative analysis of a deployed public
health tool. It was minimised before publication: the extraction pipeline aggregated
the session log and discarded identifiers, and only aggregates left the production
environment. Group labels were replaced by codes assigned in random order before
publication, and rates per account are withheld for groups with fewer than six
accounts, so that no cell describes one or two identifiable accounts. The material is compatible with the Brazilian General
Data Protection Law (Lei 13.709/2018) because it contains no personal data as defined
by Article 5, I.

## 7. License

Text, figures and data tables: Creative Commons Attribution 4.0 International
(CC BY 4.0), see `LICENSE`.
Code in `analysis/`: MIT, see `LICENSE-CODE`.

## 8. How to cite

See `CITATION.cff`. If you use the aggregate data, please cite both the manuscript
and this repository, with its version tag.

## 9. Contact

Joyce Figueiro Braga, School of Applied Mathematics, Fundacao Getulio Vargas,
Rio de Janeiro, Brazil. joyce.braga@fgv.br
