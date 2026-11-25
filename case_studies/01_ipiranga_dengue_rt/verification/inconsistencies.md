# Resolution of the six flagged inconsistencies

Each item below states the claim as it was flagged, what the archived data and code
actually do, and the corrected statement. Nothing here modifies the original artifacts
or the original transcript — the corrections live only in this file and in
`provenance.md`.

All numbers were recomputed from
`../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet` using the archived estimator;
see `code/verify_archived_algorithm.py` and
`outputs/diagnostics_archived_algorithm.txt`.

---

## 4.1 — Sensitivity range "≈4 to 20" vs estimate 11.11

**Flagged as:** the range ≈4–20 corresponds to SE202539, whereas 11.11 corresponds to
SE202540; do not compare different weeks as if they were the same estimate.

**Verdict: confirmed.** This is a genuine conflation of two different weeks and two
different quantities.

| Week | `casos` | `win_cases` | `win_lam` (ΣΛ) | Rt | 95 % CrI |
|---|---|---|---|---|---|
| **SE202539** | 1 | 1 | **0.000023** | **9.9989** | [1.2109, 27.8550] |
| **SE202540** | 4 | 5 | **0.340245** | **11.1061** | [4.0757, 21.5982] |

- **11.1061 is SE202540.** That is the archived maximum, and the value behind "11.11".
- **A "4 to 20" range is SE202539.** Across the shape-1 priors with mean 2 to 10
  (Gamma(1, 0.5) → mean 2; Gamma(1, 0.1) → mean 10), SE202539 runs from **4.000 to
  19.995**. Across all eight priors tested it runs 2.00–20.00.

Why: at SE202539, \(\sum I = 1\) and \(\sum\Lambda \approx 0\), so
\(R_t \approx (a+1)/b\) — a function of the prior only. It carries essentially no
information from the data. At SE202540, \(\sum\Lambda = 0.340\), so the posterior is
partly data-driven.

**Additional trap.** SE202540's 95 % credible interval at the archived prior is
**[4.08, 21.60]**, which also looks like "4 to 20". So there are *three* distinct things
that can be confused:

1. a prior-**sensitivity range** for **SE202539** (4–20);
2. a **point estimate** for **SE202540** (11.11);
3. a **credible interval** for **SE202540** (4.08–21.60).

They must be reported with their week and their quantity type attached.

**Corrected statement.** *"Rt reached its maximum at SE202540 (11.11, 95 % CrI
4.08–21.60). The adjacent week SE202539 yields 10.00 with a 95 % CrI of 1.21–27.86; with
only one case in its 7-week window its estimate is almost entirely prior-determined, and
across priors of mean 2–10 it ranges from 4.0 to 20.0."*

---

## 4.2 — Window cases in SE202541

**Flagged as:** the window contains seven cases in SE202541, not twelve.

**Verdict: confirmed.**

| Week | `casos` | `win_cases` |
|---|---|---|
| SE202541 | 2 | **7** |
| SE202542 | 5 | **12** |

**12 belongs to SE202542**, not SE202541. Off-by-one week in the window count.

**Corrected statement.** *"SE202541 has 7 cases in its 7-week window (2 in the reporting
week itself); SE202542 has 12."*

---

## 4.3 — "30/50" weeks with Rt > 1

**Flagged as:** verify the reported numbers of zero-case windows and the discrepancy
between 30/50 and 30/52.

**Verdict:** the numerator is right; **the denominator is wrong.**

| Definition | Count |
|---|---|
| `Rt > 1`, calendar-year filter (archived) | **30 / 52** |
| `Rt > 1`, epi-year filter SE202501–202553 | 31 / 53 |
| `Rt > 1`, excluding the 9 zero-case windows | 24 / 43 |
| lower 95 % CrI bound > 1 | 12 / 52 |

No defensible filter yields a denominator of 50. The figure **30/52** is correct for the
archived (calendar-year) analysis. The likely source of "50" is an unrecorded step — it
is not reproducible from the archive, so it should simply be corrected to 30/52 rather
than explained.

**Corrected statement.** *"Rt exceeded 1 in 30 of the 52 weeks analysed (57.7 %)."*

---

## 4.4 — Zero-case weeks and zero-case windows

**Flagged as:** verify the reported numbers of zero-case windows.

**Verdict:** two different quantities were being used interchangeably. Both are now
pinned:

| Quantity | Value | Weeks |
|---|---|---|
| Weeks with `casos = 0` (no cases reported *that week*) | **23 of 52** | scattered |
| Windows with `win_cases = 0` (no cases in the *whole 7-week window*) | **9** | **SE202530–SE202538** |

The 9-window run is the August low-activity trough. Inside it, the estimator has no data
at all, so Rt decays toward the prior mean \((a+0)/(b+0) = 5.0\): the computed values
rise from 0.104 (SE202530) to 4.997 (SE202538) purely as the empty window rolls forward.
These values are **artefacts and must not be interpreted epidemiologically**.

Note also that all 9 of these weeks fall inside the "Rt > 1 for 15 weeks" run
SE202533–SE202547 — which is why that run's case count is only 24. The run is real at its
tail (SE202539 onwards) but its head is prior drift.

**Corrected statement.** *"23 of 52 weeks had no notified cases; in 9 consecutive weeks
(SE202530–SE202538) the entire 7-week window was empty, so Rt drifts toward the prior mean
of 5.0 and is uninterpretable."*

---

## 4.5 — Calendar-year vs epidemiological-year filtering

**Flagged as:** distinguish calendar-year filtering from epidemiological-year filtering.

**Verdict:** the archived script filters by **calendar year of the week-start date**:

```python
r25 = r[pd.to_datetime(r.week).dt.year == 2025]
```

`r.week` is `data_iniSE`, the Sunday on which the epi-week starts. For 2025 that has a
concrete consequence:

| Week | `data_iniSE` | Calendar year | Included by archived filter? |
|---|---|---|---|
| SE202501 | **2024-12-29** | 2024 | **No** |
| SE202502 | 2025-01-05 | 2025 | yes |
| … | … | … | … |
| SE202553 | 2025-12-28 | 2025 | yes |

| Filter | Weeks | Range | Total cases |
|---|---|---|---|
| Calendar year (archived) | **52** | SE202502–SE202553 | 137 |
| Epi-year SE202501–SE202553 | **53** | SE202501–SE202553 | 137 |

So the analysis silently omits **SE202501**, the first epi-week of 2025. This is a
labelling mismatch, not a data loss: SE202501 had 0 cases, so the case total (137) and the
incidence (962.8/100k) are unaffected. But the **denominator changes** (52 vs 53), the
Rt>1 count changes (30 vs 31), and any statement of the form "N of 52 weeks" is a
calendar-year statement.

**Corrected statement.** *"The analysis covers 52 weeks defined by calendar year of the
epi-week start date (SE202502–SE202553). SE202501, which begins on 2024-12-29, is
excluded by this convention; including it gives 53 epi-weeks. Case totals are identical
(137) because that week had no notified cases."*

**Recommendation for the paper:** report the epi-year definition explicitly, and prefer
filtering on `SE` when the intent is epidemiological.

---

## 4.6 — Confidence interval vs credible interval

**Flagged as:** use Bayesian credible intervals when describing posterior quantiles.

**Verdict: confirmed terminology error.** The `lo`/`hi` columns are quantiles of a gamma
**posterior distribution**:

```python
'lo': gammadist.ppf(.025, sh, scale=1/r),
'hi': gammadist.ppf(.975, sh, scale=1/r),
```

This is a posterior credible interval, not a confidence interval — there is no repeated
sampling, no coverage probability over hypothetical replicates. Likewise `Rt` is the
posterior **mean** \((a+\sum I)/(b+\sum\Lambda)\), and `p_gt1` is the posterior
probability that \(R_t > 1\).

Note the archived figure title also says "95% CI", so the error propagates into the
archived artifact itself. The artifact must **not** be edited; the caption used in the
manuscript should say "95 % credible interval".

**Corrected statement.** *"Posterior mean Rt with 95 % credible intervals (gamma
posterior, Cori et al. 2013)."* — and in tables, the column should be headed
"95 % CrI".
