# Section 5 — Generalized Epidemic Intelligence in practice

This folder holds the evidence for Section 5 of the manuscript. Section 4 explains
*how* EpidBot works; Section 5 asks *what the record shows when the architecture is
actually used*.

The evidence base is not a set of constructed case studies. It is the operational
record of a platform that ran for 227 days, across 237 active accounts, 667 sessions
and 6,967 messages, together with 186 individually coded user requests.

## The argument of Section 5

| Subsection | Question | Answer comes from | Status |
| --- | --- | --- | --- |
| 5.1 Deployment and user base | Who used it, in which contexts? | `01_deployment_and_user_base/` | counts verified; geography unavailable |
| 5.2 Patterns of platform use | How was it used, how concentrated? | `02_patterns_of_platform_use/` | verified; no time series |
| 5.3 Epidemiological requests | What were users trying to accomplish? | `03_epidemiological_requests/` | verified; sampling undocumented |
| 5.4 Composition of GEI capabilities | How were the five areas combined? | `04_gei_capability_composition/` | verified to the last cell |
| 5.5 GEI in real-world settings | What does a traced instance look like? | `05_real_world_settings/` | one traced exemplar only |

## Structure

```
section_05_deployment_and_use/
├── 01_deployment_and_user_base/      README.md, derived/
├── 02_patterns_of_platform_use/      README.md, derived/
├── 03_epidemiological_requests/      README.md, CODING_GUIDE.md, derived/
├── 04_gei_capability_composition/    README.md, derived/
├── 05_real_world_settings/           README.md, EXAMPLE_INVENTORY.csv, derived/
├── methodology/                      SECTION5_METHODS.md, CONSISTENCY_AUDIT.md, VERIFICATION_REPORT.md
├── figures/                          fig5_1 … fig5_6 (PNG 300 dpi + PDF)
├── tables/                           t5_1 … t5_12 (LaTeX, booktabs)
└── scripts/                          reproduce_section5.py, make_section5_figures.py
```

The writing plan for the section is in
[`../SECTION_5_WRITING_GUIDE.md`](../SECTION_5_WRITING_GUIDE.md); the claim-to-evidence
map is in [`../SECTION_5_EVIDENCE_MATRIX.csv`](../SECTION_5_EVIDENCE_MATRIX.csv).

## Reproduce everything

```bash
python section_05_deployment_and_use/scripts/reproduce_section5.py
python section_05_deployment_and_use/scripts/make_section5_figures.py
```

The first script rebuilds all derived tables, the twelve LaTeX tables and the
verification report, and exits non-zero if any recomputation disagrees with an
archived aggregate. The second draws the figures **from those tables only** — no
number is typed into a plotting script.

## Evidence levels

Every example in Section 5 carries one of these labels, and the distinction is
stated in the text rather than blurred:

| Level | Meaning | Present in the repository |
| --- | --- | --- |
| E1 | Request, plan, tool calls, data, code, figure and verification all archived | Ipiranga only (EX-01) |
| E2 | Request archived together with the artifact it produced | none |
| E3 | Coded request record only (no execution trace) | all other examples |
| E4 | Mentioned in an administrative aggregate only | none used |

## Two rules that keep the section honest

1. **Requested composition is not executed composition.** The corpus records what
   users asked for. It does not record which tools ran, whether the run succeeded, or
   what came out. §5.4 describes demand; §5.5 shows one execution in full.
2. **The record shows process, not outcome.** Sessions happened and requests were
   made. That is all the log supports, and
   [`../docs/en/06_ethics_and_limitations.md`](../docs/en/06_ethics_and_limitations.md)
   already says so.

## Where the numbers come from

| Layer | File | Role |
| --- | --- | --- |
| Raw aggregates | `data/usage_snapshots.csv`, `data/usage_by_group.csv`, `data/messages_by_weekday.csv`, `data/audit/S0_totals.csv` | extraction output, never edited |
| Granular record | `data/audit/EXPORT_prompts_anonymised.csv` | 186 rows, the only prompt-level source of truth |
| Archived marginals | `data/audit/capability_prevalence*.csv`, `cooccurrence.csv`, `ncap_distribution.csv`, `objectives.csv`, `scope_profile.csv` | verification targets |
| Derived | `*/derived/*.csv` | rebuilt from the granular record |
| Rendered | `tables/*.tex`, `figures/*` | manuscript inputs |

Discrepancies found while reconciling these layers are itemised, with recommended
actions, in [`methodology/CONSISTENCY_AUDIT.md`](methodology/CONSISTENCY_AUDIT.md).
