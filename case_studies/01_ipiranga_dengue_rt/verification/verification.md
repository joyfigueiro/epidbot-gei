# Verification pass — re-execution of the archived Rt analysis

**Date of verification:** 2026-11-25 (afternoon/evening, same calendar day as the
original investigation, ~50 minutes after the archived artifacts were written).

**Everything in this directory is NEW.** No file here was produced by the original
investigation. The original artifacts remain untouched in `../artifacts/`, and the
original transcript remains untouched in `../documentation/`.

---

## 0. Status of this document — read first

This pass **re-executed** the archived estimator on the archived data. That is a
different thing from recovering the original execution, and the difference is the
whole point of the exercise:

| Question | Answer |
|---|---|
| Does the archived script, run on the archived data, reproduce the numbers quoted in the original narrative? | **Yes** — see §3 |
| Does this prove the original run produced those numbers? | **No.** The original run's stdout was never archived |
| Was the original task plan recovered? | **No** |
| Was the tool-call log recovered? | **No** |
| Was a sensitivity analysis part of the original investigation? | **Unknown** — the archived script contains none, and the response is truncated |
| Does this establish "adaptive execution"? | **No** — see §7 |

The verification therefore supports one narrow claim: *the archived code and the
archived data are jointly sufficient to regenerate the reported estimates.* It does
not support any claim about the original process.

---

## 1. What was re-executed

Three things, separately:

| # | Object | Code | Purpose |
|---|---|---|---|
| 1 | The **archived estimator** (`artifacts/code/snippet_15649__plot_2735.py`) | `code/verify_archived_algorithm.py` | Regenerate the weekly Rt table and diagnostics |
| 2 | The **portable rewrite** (`../reproducibility/reproduce_rt.py`) | `code/compare_reproduce_rt.py` | Check the rewrite against the archived estimator, numerically and graphically |
| 3 | **Sensitivity** (absent from the archive) | `code/sensitivity_analysis.py` | New analysis, see §5 |

The archived script hardcodes its input path
(`/data/mosqlimate/infodengue_dengue_4110508_2023-12-01_2025-12-28/data.parquet`).
The verification copies `disc()`, `cori()` and `runs()` **function-for-function** and
parameterises only the path. Defaults are unchanged: `window=7`, `a=1.`, `b=.2`,
SI discretised at mean 2.0 / sd 1.0 weekly periods.

```bash
cd verification/code
python verify_archived_algorithm.py \
    --dataset ../../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet \
    --outdir ../outputs
python compare_reproduce_rt.py \
    --dataset ../../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet \
    --reproduce-script ../../reproducibility/reproduce_rt.py \
    --archived-png ../../artifacts/figures/ipiranga_rt_2025.png \
    --outdir ../outputs
python sensitivity_analysis.py \
    --dataset ../../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet \
    --outdir ../outputs
```

---

## 2. Headline numerical results

Recomputed from the 109-row dataset, calendar-year filter (the archived filter).

| Quantity | Recomputed | Original narrative | Agrees? |
|---|---|---|---|
| Weeks in 2025 | **52** | 52 implied | yes |
| 2025 notified cases | **137** | 137 | yes |
| Annual incidence | **962.8 / 100k** | 963 / 100k | yes |
| Peak week | **SE202514** (2025-03-30), 15 cases | SE202514, 15 cases | yes |
| Peak-week incidence | **105.4 / 100k** | 105.4 | yes |
| Max Rt | **11.1061 at SE202540** | 11.11 | yes |
| Growth episode 1 | **SE202509–202517**, Rt max **2.8811** | SE202509–202517, max 2.88 | yes |
| Episode 2 (lower bound > 1) | **SE202539–202543**, Rt **2.00–11.11** | SE202539–202543, 2.0–11.1 | yes |
| Weeks with Rt > 1 | **30 of 52** | "30/50" | numerator yes, **denominator wrong** → §4.3 |
| Latest Rt | **0.5362 [0.1741, 1.0983]** | 0.54 [0.17, 1.10] | yes |

Diagnostics: `outputs/diagnostics_archived_algorithm.txt`.
Full weekly table: `outputs/rt_weekly_reproduced.csv` (columns `SE`, `week`,
`casos`, `win_cases`, `win_lam`, `Rt`, `lo`, `hi`, `p_gt1`, `inc100k`).

---

## 3. Fidelity of the portable rewrite

`code/compare_reproduce_rt.py` runs `../reproducibility/reproduce_rt.py` and compares
its output with the archived estimator over all 52 weeks:

| Column | Max absolute difference |
|---|---|
| `casos` | 0.0 |
| `win_cases` | 0.0 |
| `Rt` | 1.78 × 10⁻¹⁵ |
| `lo` | 2.22 × 10⁻¹⁶ |
| `hi` | 3.55 × 10⁻¹⁵ |
| `p_gt1` | 1.11 × 10⁻¹⁶ |

Differences are at floating-point epsilon. The rewrite is numerically faithful to the
archived estimator.

### Figure comparison

The reproduced PNG (`outputs/rt_2025.png`, 160,090 B) is *not* byte-identical to the
archived `artifacts/figures/ipiranga_rt_2025.png` (159,506 B). Both are 900 × 1950 px.
Pixel differences:

- max pixel difference 1.00, mean 0.00532, 0.87 % of pixels differ by more than 2 %;
- **all** differing rows fall in two bands at full resolution: rows **30–42** and
  **54–72** of 900 — i.e. the two title lines;
- every row outside that band is identical.

Cause: the title subtitle string was rewritten from the archived
`gamma SI mean 14 d (sd 7 d)` to `gamma SI mean 2.0 sd 1.0 weekly periods`, and an em
dash became a hyphen. The plotted geometry — bars, Rt line, credible ribbon, shaded
identification bands, axes — is pixel-identical.

**Consequence for the paper:** the figure difference is a documentation change in the
caption string, not a numerical discrepancy. But it does mean `outputs/rt_2025.png` is
a *new* figure and must not be presented as the archived figure.

---

## 4. Inconsistencies found and resolved

Full detail in [`inconsistencies.md`](inconsistencies.md). Summary:

| # | Issue | Resolution |
|---|---|---|
| 4.1 | "4 to 20" sensitivity range attributed to the same week as the 11.11 estimate | **Confirmed as a conflation.** The 11.11 belongs to **SE202540**; a 4–20 *prior-sensitivity* range belongs to **SE202539**. They are different weeks and different quantities |
| 4.2 | Window contains 7 cases in SE202541, not 12 | **Confirmed.** SE202541 `win_cases = 7`; the value 12 belongs to **SE202542** |
| 4.3 | "30/50" weeks with Rt > 1 | **Numerator right, denominator wrong: 30/52.** No filter reproduces 50 unless zero-case windows are dropped *and* the denominator is misreported |
| 4.4 | Zero-case counts | 23 weeks have `casos = 0`; 9 **windows** have `win_cases = 0` (SE202530–SE202538) |
| 4.5 | Calendar-year vs epi-year filtering | The archived filter is **calendar-year on `data_iniSE`**; it silently drops **SE202501** (2024-12-29). 52 weeks vs 53; cases unchanged at 137 |
| 4.6 | "95% CI" for posterior quantiles | Should read **95% credible interval** |

---

## 5. Sensitivity analysis (NEW — not part of the original investigation)

The archived script contains **no** sensitivity analysis: `disc(2.0, 1.0)` and
`a=1., b=.2` are hard-coded with no variation, and no artifact contains code for one.
Anything the original narrative may have reported about sensitivity is therefore
**unbacked by any archived artifact**.

This pass ran one from scratch. Results in `outputs/sensitivity_*.csv`,
`outputs/diagnostics_sensitivity.txt`.

### 5.1 Prior sensitivity (SI 2.0/1.0, window 7)

| Prior | Mean | SE202539 | SE202540 | Max Rt (week) | weeks Rt>1 | Latest Rt |
|---|---|---|---|---|---|---|
| Gamma(1, 0.2) *archived* | 5.0 | 9.999 | **11.106** | 11.106 (SE202540) | 30/52 | 0.536 |
| Gamma(0.5, 0.5) | 1.0 | 3.000 | 6.546 | 6.546 (SE202540) | 23/52 | 0.468 |
| Gamma(1, 1) | 1.0 | 2.000 | 4.477 | 4.477 (SE202540) | 23/52 | 0.494 |
| Gamma(2, 1) | 2.0 | 3.000 | 5.223 | 5.223 (SE202540) | 32/52 | 0.593 |
| Gamma(1, 0.5) | 2.0 | **4.000** | 7.141 | 7.141 (SE202540) | 30/52 | 0.520 |
| Gamma(5, 1) | 5.0 | 6.000 | 7.461 | 7.461 (SE202540) | 38/52 | 0.889 |
| Gamma(1, 0.1) | 10.0 | **19.995** | 13.629 | 19.995 (**SE202539**) | 30/52 | 0.542 |
| Gamma(2, 0.4) | 5.0 | 7.500 | 9.456 | 9.456 (SE202540) | 33/52 | 0.630 |

Ranges across all eight priors: **SE202539 → 2.00–20.00**; **SE202540 → 4.48–13.63**.

Why they behave differently — the estimator is
\(R_t = (a + \sum I)/(b + \sum \Lambda)\) over the window:

- **SE202539**: \(\sum I = 1\), \(\sum\Lambda = 0.000023\) → \(R_t \approx (a+1)/b\). The
  data contribute essentially nothing; the value is set by the prior.
- **SE202540**: \(\sum I = 5\), \(\sum\Lambda = 0.340\) → genuinely posterior, with a wide
  credible interval \([4.08, 21.60]\).

Two important caveats this exposes:

1. **The identity of the peak week is not robust.** Under a Gamma(1, 0.1) prior and under
   SI 1.5/0.7, the maximum moves from SE202540 to SE202539. "Rt peaked at SE202540" is a
   prior-dependent statement.
2. **"Latest Rt < 1, declining" is not uniformly robust.** The point estimate stays below
   1 across all eight priors (0.468–0.889), but the 95 % credible interval excludes 1
   under only one of the eight (Gamma(0.5, 0.5): [0.140, 0.988]).

### 5.2 Serial-interval sensitivity (prior 1/0.2, window 7)

| SI mean (wk) | SI sd (wk) | SE202539 | SE202540 | Max Rt (week) | weeks Rt>1 |
|---|---|---|---|---|---|
| 1.5 | 0.7 | 10.000 | 8.036 | 10.000 (SE202539) | 31 |
| **2.0** | **1.0** | **9.999** | **11.106** | **11.106 (SE202540)** | **30** |
| 2.0 | 0.5 | 10.000 | 16.874 | 16.874 (SE202540) | 32 |
| 2.5 | 1.2 | 9.980 | 14.904 | 14.904 (SE202540) | 30 |
| 3.0 | 1.5 | 9.646 | 17.586 | 17.586 (SE202540) | 30 |

SE202539 barely moves (9.65–10.00) because \(\sum\Lambda \approx 0\); SE202540 moves
substantially (8.04–17.59). The peak-week identity flips again at SI 1.5/0.7.

### 5.3 Window sensitivity

| Window (weeks) | SE202539 | SE202540 | Max Rt | weeks Rt>1 |
|---|---|---|---|---|
| 5 | 10.000 | 11.106 | 11.106 | 30 |
| **7** | **9.999** | **11.106** | **11.106** | **30** |
| 9 | 9.967 | 11.104 | 11.104 | 32 |

The window length is the least influential of the three choices.

---

## 6. The low-incidence caveat — was it in the response? (point 5)

The original response is **truncated** in the retained conversation window. The
transcript marks the cut with `[CUT]`, immediately after the sentence *"Rt stayed above 1
for **14 consecutive weeks** (SE 202506–202519),"*. Everything after that point is
**not available and was not reconstructed**.

What this means for the two caveats:

| Caveat | Status | Evidence |
|---|---|---|
| **Low-incidence / upstream-Rt is unusable** | **PRESENT in the response** — and not merely in the opening summary. It appears in the *"How I estimated it"* section, mid-response, before the Episode 1 table | `../documentation/interaction_transcript.md`, Turn 2 |
| **Prior sensitivity** | **UNKNOWN.** No mention in the surviving portion; the remainder is unrecoverable | — |

So the premise that the low-incidence caveat was confined to an opening summary is
**not supported**: it is in the body of the response.

And the low-incidence claim is not merely narrative — it is **checkable against an
archived artifact** and it checks out:

- `artifacts/derived/ipiranga_weekly_2025.parquet` carries `infodengue_Rt`;
- **SE202503** has `casos = 1` and `infodengue_Rt = 8.884893` → the quoted **"8.9 in a
  week with one case"**;
- all **25** weeks with `casos = 0` have `infodengue_Rt = 0.0` → the quoted **"0.0 in
  weeks with none"**.

This upgrades that claim from narrative-only to artifact-supported.

**On generalisation:** nothing here licenses a statement about the system as a whole.
This is one case study. A single truncated response cannot establish that EpidBot omits
limitations globally, and the surviving evidence points the other way for the
low-incidence caveat.

---

## 7. Why "adaptive execution" is still not demonstrated

The prior packaging flagged, and this pass confirms, that the reason for the **second
data retrieval** (the 109-row pull at 18:40:59, after derived files had already been
built from the 59-row pull at 18:39:51) is **not recorded anywhere**. The timestamps
establish only the *order*:

```
18:39:51  59-row dataset written          (SE202449–202602)
18:40:35  derived weekly + biweekly written
18:40:40  two rt_estimate_*.webp written  (tool unattributed)
18:40:59  109-row dataset written         (SE202349–202553)
18:41:42  ipiranga_rt_2025.png written    (plot 2735)
```

An ordering is not a motive. "Adaptive execution" would require a record showing that an
observed limitation *caused* the re-retrieval. No such record exists. The manuscript
should describe this as an **observed re-retrieval of unknown motivation**, not as
demonstrated adaptivity.

---

## 8. What remains unverified

| Item | Status |
|---|---|
| Original run's stdout / numerical output | **Not archived.** Recomputed values are new |
| Original task plan | **Not persisted.** Not reconstructed |
| Tool-call log | **Not persisted.** Not reconstructed |
| Identity of the tool behind `rt_estimate_8573ff9a.webp` / `rt_estimate_a2dc5f17.webp` | **Unknown.** Filenames are consistent with a tool-generated plot; nothing names the tool or its parameters |
| Numerical output of that tool-based comparison | **Not archived.** Only the two images survive |
| Snippet 15649's stored payload | **Not retrievable.** `search_code_snippets` returned no match twice; the shipped code is plot 2735's generating code |
| Whether any sensitivity analysis was run originally | **Unknown** |
| Full original response text | **Unrecoverable** — truncated at `[CUT]` |

---

## 9. Files in this directory

| File | Origin | What it is |
|---|---|---|
| `verification.md` | NEW | This document |
| `inconsistencies.md` | NEW | Item-by-item resolution of the six inconsistencies |
| `environment.md` | NEW | Software versions and platform |
| `code/verify_archived_algorithm.py` | NEW | Port of the archived estimator; writes the weekly table |
| `code/compare_reproduce_rt.py` | NEW | Runs the rewrite, diffs numbers and figure |
| `code/sensitivity_analysis.py` | NEW | Prior / SI / window sensitivity |
| `outputs/rt_weekly_reproduced.csv` | NEW | 52 weeks × (cases, window cases, summed infectiousness, Rt, 95 % CrI) |
| `outputs/rt_estimates_2025.csv` | NEW | Output of `reproduce_rt.py` itself |
| `outputs/rt_2025.png` | NEW | Figure regenerated by `reproduce_rt.py` |
| `outputs/sensitivity_prior.csv` | NEW | 8 priors |
| `outputs/sensitivity_serial_interval.csv` | NEW | 5 serial-interval settings |
| `outputs/sensitivity_window.csv` | NEW | 3 window lengths |
| `outputs/diagnostics_archived_algorithm.txt` | NEW | Full stdout of the re-execution |
| `outputs/diagnostics_sensitivity.txt` | NEW | Full stdout of the sensitivity runs |
| `outputs/diagnostics_comparison.txt` | NEW | Full stdout of the rewrite comparison |

None of the files above existed before this pass.
