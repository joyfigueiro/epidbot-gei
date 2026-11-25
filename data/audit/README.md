# `data/audit/` — data dictionary

This folder holds the coded prompt corpus and the aggregates derived from it. It is
the evidentiary base for Sections 4.4 and 5 of the manuscript.

Two things are worth knowing before using any file here:

1. **`EXPORT_prompts_anonymised.csv` is the source of truth.** It is the only
   granular record; every other file in this folder is either an input to it or a
   marginal derived from it. When a derived marginal and a recomputation disagree,
   the recomputation wins and the marginal is corrected — not the other way round.
2. **Nothing here is a sample of the population of users.** The corpus is a
   purposive selection of requests whose selection rule is not recorded. See
   `../section_05_deployment_and_use/methodology/CONSISTENCY_AUDIT.md` §A7.

---

## The granular record

### `EXPORT_prompts_anonymised.csv` — 186 rows × 8 columns

One row per individually coded user request. No prompt text is stored, which is what
makes the file publishable.

| Column | Type | Meaning |
| --- | --- | --- |
| `pid` | integer | Prompt identifier, stable within this repository. Carries no session, account or timestamp information |
| `scope` | text | User context: `Internal (core team)`, `External - government`, `External - academic`, `External - international`, `External - walk-in` |
| `caps` | text | Set of capability codes present, as concatenated letters: `I`, `K`, `A`, `M`, `V` (GEI areas), `S` (platform-meta), `X` (out of scope). Example: `IAV` |
| `objective` | text | Exactly one analytical objective code: `RES`, `META`, `DESC`, `TRAN`, `SURV`, `OOS`, `RISK`, `PLAN`, `FORE`, `COMP` |
| `deictic` | 0/1 | 1 when the request depends on earlier conversational context or on a previously produced artifact |
| `nsources` | integer | Number of distinct data sources named in the request (0–3) |
| `crossdomain` | 0/1 | **Identical to `nsources >= 2`** — the two variables are one variable; see consistency audit §A4 |
| `n_gei` | integer | Count of distinct GEI codes in `caps`. Verified for all 186 rows |

Codebook and decision rules:
`../section_05_deployment_and_use/03_epidemiological_requests/CODING_GUIDE.md`.

**Eligibility rule.** A request is GEI-eligible when `objective != "OOS"` **and**
`caps != "S"`. This yields 141 of 186. It is the denominator for every §5.4 statistic.
Three requests carry GEI codes *and* are out of scope; they are excluded by objective.

---

## The archived marginals

These files were produced before the reproduction script existed. Each is now a
verification target: the script recomputes the quantity from the granular record and
fails if they disagree.

| File | Content | Denominator | Reproduces? |
| --- | --- | --- | --- |
| `S0_totals.csv` | all-user totals for the reference extraction | — | yes |
| `snapshots.csv` | the four extractions | — | yes |
| `S1_group_characteristics.csv` | group-level characteristics, pseudonymised | — | yes |
| `capability_prevalence.csv` | all seven codes | 186 | yes |
| `capability_prevalence_gei.csv` | the five GEI codes | **141** | yes, exactly |
| `ncap_distribution.csv` | capabilities per prompt | 141 | yes, exactly |
| `cooccurrence.csv` | 5×5 symmetric matrix | 141 | yes, cell by cell |
| `objectives.csv` | ten objective codes | 186 | yes, exactly |
| `scope_profile.csv` | profile by context | 186 (all) | yes, but **`pct_multi` and `mean_gei` use the all-prompt base**, not 141 |
| `internal_vs_external.csv` | internal vs external | 43 / 143 | yes |
| `failure_modes.csv` | seven friction categories | 186 | yes |
| `discovery_questions.csv` | the discovery cluster, **with text** | — | yes |
| `dashboard_payload_pseudonymised.json` | KPI block and chart payloads | — | yes (KPIs) |
| `EXPORT_*.csv` | publication-ready subsets of the above | — | yes |

### Two traps in the archived marginals

- **`scope_profile.csv` mixes bases.** Its `pct_multi` (27.9–37.8 %) is computed over
  *all* prompts in the context; the manuscript's 41.8 % is computed over *eligible*
  prompts. Same label, different denominator. The derived table
  `context_profile.csv` reports both, suffixed `_of_all` and `_of_eligible`.
- **`dashboard_payload_pseudonymised.json` reports 10,863 nowhere** — the figure that
  appeared in an earlier manuscript draft is absent from every file in this
  repository. See consistency audit §A1.

---

## Regenerating

```bash
python section_05_deployment_and_use/scripts/reproduce_section5.py
```

Writes 17 derived tables under `section_05_deployment_and_use/*/derived/`, twelve
LaTeX tables, and `methodology/VERIFICATION_REPORT.md`. Exits non-zero if any
recomputation disagrees with an archived marginal. **No file in this folder is
modified by that script** — historical artefacts are preserved as they are.
