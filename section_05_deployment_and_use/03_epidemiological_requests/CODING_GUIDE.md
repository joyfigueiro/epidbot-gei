# Coding guide — GEI capability and analytical objective

This is the codebook for the corpus in
[`../../data/audit/EXPORT_prompts_anonymised.csv`](../../data/audit/EXPORT_prompts_anonymised.csv).
It exists so that the classification can be audited, re-applied and, if the authors
choose, reproduced by a second coder.

The guide was reconstructed from the coded corpus, not recovered from the original
coding session. Where a rule had to be inferred, that is stated. Nothing here
changes the codes: the archived codes are the record, and the guide describes what
they imply.

---

## 1. Unit of analysis

One row = **one user request**, identified by `pid`. A request may contain several
instructions ("generate the figure *and* update the README"); it is still one row,
and it may receive several capability codes.

The corpus is a sample of requests, and its selection rule is not documented. See
[`../methodology/CONSISTENCY_AUDIT.md`](../methodology/CONSISTENCY_AUDIT.md) §A7.

---

## 2. Capability codes

A capability code is applied when the **request itself** asks for that kind of work.
It is not applied because the answer would need it, nor because the system happens
to use it internally. The distinction matters: the corpus measures *requested*
composition, never *executed* composition.

### `I` — Integration of heterogeneous data sources

| | |
| --- | --- |
| Apply when | The request names a data source, a dataset, a provider or a coverage question that requires locating data ("InfoDengue", "SIM", "the catalogue", "data for Hungary", "notification periods available in DATASUS") |
| Do not apply when | No source is named and none is implied by a coverage constraint |
| Boundary case | "Which datasets are available?" is `I`, not `A`: retrieving and inventorying sources is integration work, not analysis |
| Archived example | `pid 116` — "What data is available for Hungary?" (`I`, objective `META`) |

`I` is the most frequent code after `V` (57/141, 40.4 %) and the most frequent among
walk-in users (80.0 % of eligible walk-in prompts), which is the empirical signature
of a discovery bottleneck.

### `K` — Access to scientific knowledge

| | |
| --- | --- |
| Apply when | The request needs literature, definitions, methodological precedent or bibliographic verification ("what is the definition of vulnerability in public health", "which models are used for dengue", "check this DOI") |
| Do not apply when | The knowledge required is about the platform itself — that is `S` |
| Boundary case | A request to *rewrite* a manuscript section is `S`+`R`-type work, not `K`, unless it asks for literature |

### `A` — Epidemiological analysis

| | |
| --- | --- |
| Apply when | The request asks for a substantive epidemiological computation: incidence, comparison across places or periods, age standardisation, case definition, descriptive statistics of health events |
| Do not apply when | The computation is purely a data-management step (that is `I`) or a model fit (that is `M`) |
| Boundary case | "How did dengue behave in Rio and São Paulo in 2024" is `A`. "Convert annual parameters to weekly" is `M`, not `A` |

### `M` — Mathematical modelling

| | |
| --- | --- |
| Apply when | The request involves model fitting, parameter estimation, forecasting, scenario simulation, sensitivity analysis, $R_0$/$R_t$ estimation |
| Do not apply when | The request is descriptive only |
| Boundary case | Rescaling parameters from annual to weekly is `M`: it changes the model's time base |
| Rare in the corpus | 24/141 (17.0 %) — the least requested capability |

### `V` — Visualization and reporting

| | |
| --- | --- |
| Apply when | The request asks for a figure, table, slide, dashboard, PDF/Word report, or a specific visual encoding |
| Do not apply when | The request only asks for numbers |
| Boundary case | "Generate figures for slides 1 and 2" is `V`+`S` |
| Most frequent | 59/141 (41.8 %) |

### `S` — Platform-meta request (non-GEI)

| | |
| --- | --- |
| Apply when | The request is about the system itself: which model it uses, what it can do, how to use it, who built it, where an artifact went |
| Effect | A prompt coded `S` **and nothing else** is excluded from the GEI-eligible set |
| Archived examples | `pid 172` — "O que você pode fazer?"; `pid 121` — "What datasets are available? What is the difference between you and other LLMs?" |
| Caution | `S` co-occurs with real work: 66 of 186 prompts carry `S`, but only 36 are `S`-only. A request for a figure *of the platform* is `S`+`V`, and stays eligible |

### `X` — Out of scope

| | |
| --- | --- |
| Apply when | The request seeks individual clinical advice, or is otherwise outside population-level epidemiological intelligence |
| Effect | Excluded from the eligible set — but note that the exclusion is applied through `objective == OOS`, not through this flag |
| Archived examples | `pid 28`, `pid 137`, `pid 138`, `pid 185` (all `X`, objective `OOS`) |
| Interaction with `K` | Two prompts are `KX`: they ask a knowledge question that lands out of scope. A request can be well-formed and still refuse-worthy |

---

## 3. Analytical objective codes

Exactly one objective per prompt. The glossary is **inferred** from the corpus and
from cross-tabulation with the capability codes; the original codelist was not
recovered. Confirm or replace before submission.

| Code | Inferred gloss | $n$ | Typical signal |
| --- | --- | --- | --- |
| `RES` | Research and writing support | 56 | rewrite a section, shorten the abstract, check a reference |
| `META` | Platform-meta question | 52 | what data exist, what the system can do, which model it uses |
| `DESC` | Descriptive epidemiology | 21 | how a disease behaved in a place and period |
| `TRAN` | Data transformation / parameter rescaling | 14 | convert annual to weekly, aggregate, join |
| `SURV` | Surveillance monitoring | 14 | current situation, alert level, nowcast |
| `OOS` | Out of scope | 9 | individual clinical advice |
| `RISK` | Risk assessment | 7 | probability of introduction, layer pricing |
| `PLAN` | Analytical planning | 7 | "how should I structure this analysis" |
| `FORE` | Forecasting | 4 | predict the next season |
| `COMP` | Comparison across units | 2 | municipalities or states against each other |

The distribution is itself a finding: **`RES` + `META` = 58 % of all requests.** The
platform is used as much for producing science and for learning what it can do as
for computing epidemiology. That is a statement about demand, and it belongs in
§5.3 — with the caveat that the sample is purposive.

---

## 4. Secondary fields

| Field | Values | Definition |
| --- | --- | --- |
| `deictic` | 0/1 | 1 when the request depends on previous conversational context or on an artifact produced earlier ("this figure", "the same thing for dengue", "rewrite it"). 80/186 = 43.0 % |
| `nsources` | 0–3 | Number of distinct data sources named in the request. 0: 116; 1: 70; 2: 6; 3: 2 |
| `crossdomain` | 0/1 | **Identical to `nsources >= 2`** — all eight prompts, no exceptions. Treat as one variable; see consistency audit §A4 |
| `n_gei` | 0–4 | Count of distinct GEI codes (`I`,`K`,`A`,`M`,`V`). Verified against `caps` for all 186 rows |

`deictic` is the closest available proxy for investigative continuity: 43.0 % of
coded requests continue an earlier thread rather than starting cold. It is a proxy,
not a trajectory measure — the corpus has no session-level linkage.

---

## 5. Worked classification of the corpus

| Step | Rule | Result |
| --- | --- | --- |
| 1 | Every row receives 1–4 capability codes and exactly one objective | 186 rows |
| 2 | `n_gei` recounted from `caps` | 0 discrepancies |
| 3 | Exclude `objective == OOS` | −9 |
| 4 | Exclude `caps == "S"` | −36 |
| 5 | Remaining = eligible set | **141** |
| 6 | Capability prevalence over the eligible set | reproduces archived marginals exactly |
| 7 | Multi-capability share | 59/141 = 41.8 % |

---

## 6. Validation protocol for the authors

A two-hour protocol that closes the largest methodological gap in §5.4:

1. **Screen the eight largest cells first**, not the whole corpus. The combinations
   `A+V+I` (12), `A+I` (7), `K+M` (6), `A+V` (6), `K+V` (6) cover 37 of the 59
   multi-capability prompts. Disagreement concentrates where codes co-occur.
2. **Re-code 40 prompts blind** — 20 drawn at random from the eligible set, 20 from
   the `S`-only and `OOS` strata, since eligibility drives every denominator. Have
   the second coder use only this guide.
3. **Report Cohen's kappa** per code. Expected kappa for `S` and `OOS` is high;
   for `A` versus `M` it will be the weakest, because the boundary is a judgement
   call that this guide resolves by rule (descriptive → `A`, model-based → `M`).
4. **Publish the disagreement table.** Four disagreements honestly reported are worth
   more than a silent second pass.
5. If kappa is below 0.6 for any code, merge or redefine that code rather than
   defend it.

---

## 7. What the coding does not support

- It does not measure execution. A prompt coded `M` may have produced no model.
- It does not measure success, satisfaction or usefulness.
- It does not measure capability *use*, only capability *demand*.
- It cannot be aggregated to "all user requests" (§A7).
- It cannot be compared across contexts without stating the denominator (§A3).
