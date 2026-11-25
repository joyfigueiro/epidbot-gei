# Provenance and evidence tiers

**Revision 2 — 2026-11-25, verification pass.**

What changed in this revision, and why:

- A **verification pass** re-executed the archived estimator on the archived data
  (`verification/`). That produced a genuinely new evidence class — *reproduced*
  values — which the original two-tier scheme had no way to express. New tiers
  **[R]** and **[V]** were added.
- Six specific inconsistencies were checked item by item; three claims originally
  graded **[N]** are now **[A]** (they are checkable against an archived artifact), one
  is **corrected**, and one narrative figure is **wrong**.
- Original grades are **retained and annotated**, not overwritten. Where a grade moved,
  the old grade is shown in the "was" column.

**No original artifact was modified in this revision.** `artifacts/` and
`documentation/interaction_transcript.md` are byte-identical to the earlier packaging.
Corrections live in `verification/inconsistencies.md` and in this file only.

## Tier definitions

| Tier | Meaning |
|---|---|
| **[A]** | Supported by a stored artifact included in this archive, checkable offline |
| **[A-]** | Partially supported: the artifact exists but the specific value is not in it |
| **[N]** | Asserted **only** by the original chat narrative. No archived artifact backs it |
| **[R]** | **Reproduced** by re-execution in `verification/` from the archived code + data. This is a *new* number that happens to agree with the narrative — agreement is corroboration, not recovery |
| **[V]** | **New analysis performed during verification.** Was not part of the original investigation, has no narrative counterpart, and must not be attributed to it |
| **[I]** | Inference drawn by the assistant at packaging/verification time from timestamps or file content — not a record |
| **[U]** | Unavailable. No record exists. Not reconstructed |
| **[X]** | **Contradicted / corrected** by re-execution |

---

## 1. Setting and method

| Claim | Tier | Was | Basis |
|---|---|---|---|
| Ipiranga, PR; IBGE geocode **4110508** | **[A]** | [A] | `municipio_geocodigo` in both parquets |
| Population **14,230** | **[A]** | [A] | `pop` column = 14230.0 |
| Source: InfoDengue via Mosqlimate | **[A]** | [A] | RO-Crate `wasDerivedFrom: #Mosqlimate` |
| Estimator: Cori et al. (2013) sliding window | **[A]** | [A] | `def cori(...)` in the generating code |
| Window = **7** weeks | **[A]** | [A] | `cori(..., 7)` |
| Gamma prior **a=1, b=0.2** (mean 5) | **[A]** | [A] | `def cori(I,si,window=7,a=1.,b=.2)` |
| SI discretised at mean 2.0, sd 1.0 weekly periods | **[A]** | [A] | `disc(2.0,1.0)` |
| SI phrased as "14 d (sd 7 d)" | **[A-]** | [A-] | code uses 2.0/1.0 **weeks**; day phrasing appears only in the plot title string |
| No nowcasting applied | **[A]** | [A] | no delay-correction code |

---

## 2. Data retrieval

| Claim | Tier | Was | Basis |
|---|---|---|---|
| Retrieved `2024-12-01 → 2026-01-15`, 59 epi-weeks (SE202449–202602) | **[A]** | [A] | `artifacts/data/ds_2024-12-01_2026-01-15/` |
| Retrieved `2023-12-01 → 2025-12-28`, 109 epi-weeks (SE202349–202553) | **[A]** | [A] | `artifacts/data/ds_2023-12-01_2025-12-28/` |
| The published figure was computed from the **2023-12-01** dataset | **[A]** | [A] | absolute path hard-coded in the generating script |
| RO-Crate descriptions read "for 2023" / "for 2024" and are **wrong** | **[A]** | [A] | see Defect 1; uncorrected by design |

---

## 3. Results — narrative vs reproduced

This is the section that changed most. **All [R] values are new**; they were produced on
2026-11-25 by running the archived code on the archived data. Their agreement with the
narrative is evidence that the narrative was arithmetically consistent with the archive,
**not** evidence that the original run printed them.

| Claim | Narrative | Reproduced | Tier | Was |
|---|---|---|---|---|
| 2025 notified cases | 137 | **137** | **[A]**/[R] | [A] |
| Annual incidence | 963 / 100k | **962.8** | **[A]**/[R] | [A] |
| Weeks analysed | "52" implied | **52** (SE202502–SE202553) | **[R]** | — |
| Peak week | SE202514, 15 cases | **SE202514, 15 cases, 105.4/100k** | **[R]** | [N] |
| Max Rt | 11.11 | **11.1061 at SE202540** | **[R]** | [N] |
| Episode 1 | SE202509–202517, max 2.88 | **SE202509–202517, Rt 1.15–2.88** | **[R]** | [N] |
| Rt>1 for 14 consecutive weeks | SE202506–202519 | **SE202506–202519, 14 wks** | **[R]** | [N] |
| Episode 2 | SE202539–202543, Rt 2.0–11.1 | **SE202539–202543, Rt 2.00–11.11** | **[R]** | [N] |
| Latest Rt | 0.54 [0.17, 1.10] | **0.5362 [0.1741, 1.0983]** | **[R]** | [N] |
| "30/50 weeks with Rt>1" | 30/50 | **30/52** | **[X]** | [N] |
| "Rt 8.9 in a week with one case" | 8.9 | **SE202503: casos=1, `infodengue_Rt`=8.8849** | **[A]** | [N] |
| "Rt 0.0 in weeks with none" | 0.0 | **all 25 zero-case weeks: `infodengue_Rt`=0.0** | **[A]** | [N] |
| An independent implementation reproduced the tool's latest Rt | asserted | **the rewrite reproduces the archived estimator to 1.8×10⁻¹⁵** — but the *tool's* output was never archived, so the original comparison cannot be checked | **[A-]** | [N] |

### Notes on the upgraded rows

- The two `infodengue_Rt` claims are now **[A]** because
  `artifacts/derived/ipiranga_weekly_2025.parquet` carries the upstream `Rt` column and
  the quoted values are in it. This claim never needed to be narrative-only.
- **"30/50" is corrected to 30/52.** No filter over the archived data produces a
  denominator of 50. See `verification/inconsistencies.md` §4.3.
- The row about the independent implementation is deliberately **[A-]**: the rewrite's
  agreement with the *archived estimator* is proven, but agreement with the
  *pre-implemented tool* is not, because that tool's numeric output was never saved —
  only the two unattributed `.webp` images.

---

## 4. New analyses performed during verification — **[V]**

None of the following existed in the original investigation. They must be presented as
verification-time analysis, never as part of the original results.

| Analysis | Result | File |
|---|---|---|
| Prior sensitivity, 8 priors | SE202539 spans **2.00–20.00**; SE202540 spans **4.48–13.63** | `verification/outputs/sensitivity_prior.csv` |
| Serial-interval sensitivity, 5 settings | SE202540 spans **8.04–17.59**; SE202539 effectively fixed | `verification/outputs/sensitivity_serial_interval.csv` |
| Window sensitivity, 5/7/9 weeks | max Rt stable ~11.10–11.11 | `verification/outputs/sensitivity_window.csv` |
| Peak-week robustness | max Rt moves from SE202540 to **SE202539** under a Gamma(1,0.1) prior and under SI 1.5/0.7 | same |
| "Latest Rt < 1" robustness | point estimate < 1 under all 8 priors (0.468–0.889), but the 95 % CrI excludes 1 under only **1 of 8** | same |
| Calendar vs epi-year | archived filter drops **SE202501**; 52 vs 53 weeks; cases unchanged | `verification/outputs/diagnostics_archived_algorithm.txt` |
| Rewrite fidelity | max \|ΔRt\| = **1.78×10⁻¹⁵**; PNG differs only in the title band (rows 30–42, 54–72 of 900) | `verification/outputs/diagnostics_comparison.txt` |

Two of these materially weaken the original narrative and should be carried into the
manuscript as limitations:

1. **The peak week is prior-dependent.** Reporting "max Rt 11.11 at SE202540" as a
   finding overstates it; the maximum moves to SE202539 under two of the tested
   specifications.
2. **The "declining" conclusion is not statistically robust.** The point estimate is
   below 1 throughout, but the credible interval includes 1 under 7 of 8 priors.

---

## 5. Claims that remain unsupported

| Claim / item | Tier | Why it cannot be upgraded |
|---|---|---|
| The original run printed any specific number | **[U]** | its stdout was never archived; [R] values are new |
| Any sensitivity analysis in the original investigation | **[U]** | the archived script hard-codes prior/SI/window; the response is truncated |
| Peak-window Rt for SE202539 as a *data-driven* estimate | **[U]** | it is prior-determined (\(\sum\Lambda \approx 0\)); no data-driven value exists |
| Identity of the tool behind `rt_estimate_8573ff9a.webp` / `rt_estimate_a2dc5f17.webp` | **[U]** | nothing names the tool or its parameters |
| Numerical output of that tool-based comparison | **[U]** | only the images survive |
| Snippet 15649's stored payload | **[U]** | `search_code_snippets` returned no match twice; shipped code is plot 2735's generating code |
| Original task plan | **[U]** | not persisted; not reconstructed |
| Tool-call log | **[U]** | not persisted; not reconstructed |
| Full original response text | **[U]** | truncated at `[CUT]` |
| That the process demonstrated "adaptive execution" | **[U]** | the ordering of retrievals is timestamped; the *reason* for the second retrieval is not recorded anywhere |

---

## 6. Execution ordering — what the timestamps show, and what they do not

Recovered mtimes (2026-11-25, UTC) — unchanged from revision 1:

| Time | Artifact |
|---|---|
| 18:39:51 | `ds_2024-12-01_2026-01-15/data.parquet` (59 rows) |
| 18:40:35 | `ipiranga_weekly_2025.parquet` + `ipiranga_biweekly_2025.parquet` |
| 18:40:40 | `rt_estimate_a2dc5f17.webp` + `rt_estimate_8573ff9a.webp` |
| 18:40:59 | `ds_2023-12-01_2025-12-28/data.parquet` (109 rows) |
| 18:41:00 | its `ro-crate-metadata.json` |
| 18:41:42 | `ipiranga_rt_2025.png` (plot 2735) |
| 19:16–19:31 | **verification pass** (new; `verification/`) |

**[A]** The derived weekly/biweekly files and the two `rt_estimate_*` figures were written
*before* the 109-row dataset existed. The final figure comes from the 109-row dataset.

**[I]** The derived files were built from the 59-row pull; two tool-based Rt estimates
were produced on weekly and biweekly bases; a deeper pull was then made; the final figure
was recomputed from it. This remains inference.

**[U]** **Not recorded, therefore not reconstructed:** why the second retrieval happened;
whether either `rt_estimate_*` run was a deliberate "compare against the built-in tool"
step; whether any sensitivity analysis was run.

The verification pass did **not** change this. Re-executing the analysis cannot recover a
motive.

---

## 7. Known defects in the recovered artifacts (preserved as-is)

1. **RO-Crate descriptions are wrong** — "for 2023"/"for 2024" while the data span
   2023-12→2025-12 and 2024-12→2026-01. Field source is tagged `data_inferred`.
   Do not quote them. Additionally the crates carry **no licence field** — see `NOTICE.md`.
2. **`rt_estimate_*.webp` are unattributed.**
3. **Population hard-coded** as `14230` in the archived script rather than read from
   `pop` — incidence would silently mis-scale for any other municipality.
4. **Upstream `Rt` is carried in the derived weekly file** as `infodengue_Rt` and is easy
   to confuse with the re-estimated Rt. Different quantities; never pool them.
5. **The archived figure title says "95% CI"** for what are posterior credible intervals.
   The artifact is preserved as-is; the manuscript caption must not repeat the error.
