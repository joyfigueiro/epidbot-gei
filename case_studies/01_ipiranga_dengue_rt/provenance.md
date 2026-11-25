# Provenance and evidence tiers

Every statement in the original answer is graded below. The grading is deliberately strict:
an artifact "supports" a claim only if the claim can be checked against the artifact itself.

## Tier definitions

| Tier | Meaning |
|---|---|
| **[A]** | Supported by a stored artifact included in this archive, checkable offline |
| **[A-]** | Partially supported: the artifact exists but the specific value is not in it |
| **[N]** | Supported **only** by the chat narrative (the answer as delivered). No artifact backs it |
| **[I]** | My inference drawn at packaging time from timestamps or file content — not a record |
| **[U]** | Unavailable. No record exists. Not reconstructed |

---

## 1. Setting and method

| Claim | Tier | Basis |
|---|---|---|
| Ipiranga, PR; IBGE geocode **4110508** | **[A]** | `municipio_geocodigo` in both parquet files |
| Population **14,230** | **[A]** | `pop` column = 14230.0 in both files |
| Source: InfoDengue via Mosqlimate | **[A]** | RO-Crate `wasDerivedFrom: #Mosqlimate`, `spatialCoverage: Parana, Brazil` |
| Estimator: Cori et al. (2013) sliding window | **[A]** | `def cori(...)` in the generating code |
| Window = **7** weeks | **[A]** | `r=cori(..., 7)` in the code |
| Gamma prior **a=1, b=0.2** | **[A]** | `def cori(I,si,window=7,a=1.,b=.2)` |
| Serial interval discretised at mean 2.0, sd 1.0 weekly periods | **[A]** | `disc(2.0,1.0)` in the code |
| SI expressed as "14 d (sd 7 d)" | **[A-]** | code uses 2.0/1.0 *weeks*; the day-unit phrasing appears only in the plot title string, which is in the artifact |
| No nowcasting applied | **[A]** | no delay-correction code in the script |

## 2. Data retrieval

| Claim | Tier | Basis |
|---|---|---|
| Retrieved `2024-12-01 → 2026-01-15`, 59 epi-weeks (SE 202449–202602) | **[A]** | `artifacts/data/ds_2024-12-01_2026-01-15/` |
| Retrieved `2023-12-01 → 2025-12-28`, 109 epi-weeks (SE 202349–202553) | **[A]** | `artifacts/data/ds_2023-12-01_2025-12-28/` |
| The published figure was computed from the **2023-12-01** dataset | **[A]** | absolute path hard-coded in `snippet_15649__plot_2735.py` |
| RO-Crate descriptions read "for 2023" / "for 2024" | **[A]** | metadata files — and see **Defect 1** below |

## 3. Results

| Claim | Tier | Basis |
|---|---|---|
| 2025 burden: **137 notified cases** | **[A]** | direct sum over archived parquet (packaging-time check) |
| 2025 annual incidence **962.8 / 100,000** (rounded 963) | **[A]** | same sum / 14230 × 1e5 |
| 52 epidemiological weeks in 2025 | **[A]** | row count |
| Peak week **SE202514** (w/c 30 Mar), **15 cases**, **105.4/100k** | **[N]** | narrative only. *105.4 is arithmetically 15/14230×1e5, so it is internally consistent, but the peak was not recomputed* |
| Growth episode 1: **SE202509–202517**, Rt max **2.88**, 14 weeks Rt>1 (SE202506–202519) | **[N]** | narrative only |
| Episode 2: **SE202539–202543**, Rt **2.0–11.1** | **[N]** | narrative only |
| Latest Rt **0.54 [0.17, 1.10]** | **[N]** | narrative only |
| Rt max overall **11.11**, 30/50 weeks with Rt>1 | **[N]** | narrative only |
| "Raw InfoDengue Rt unusable at small counts" | **[A-]** | the derived weekly parquet **does** carry an `infodengue_Rt` column copied from upstream `Rt`, so the quantity being criticised is inspectable; the specific values quoted (8.9 at 1 case, 0.0 at 0 cases) are **[N]** |
| An independent implementation reproduced the tool's latest Rt | **[N]** | narrative only; no comparison output was archived |

**Why the [N] rows cannot be upgraded.** The archived parquet and the archived script are
sufficient to *recompute* every Rt value — but recomputation is analysis, and this archive
was built under an explicit instruction not to produce new results. So those numbers remain
narrative-only. Anyone re-running `reproducibility/reproduce_rt.py` will obtain fresh
numbers that must be reported as *new*, not as corroboration of the original run.

## 4. Execution ordering — what the timestamps show, and what they do not

Recovered mtimes (2026-11-25, UTC):

| Time | Artifact |
|---|---|
| 18:39:51 | `ds_2024-12-01_2026-01-15/data.parquet` (59 rows) |
| 18:40:35 | `ipiranga_weekly_2025.parquet` + `ipiranga_biweekly_2025.parquet` |
| 18:40:40 | `rt_estimate_a2dc5f17.webp` + `rt_estimate_8573ff9a.webp` |
| 18:40:59 | `ds_2023-12-01_2025-12-28/data.parquet` (109 rows) |
| 18:41:00 | its `ro-crate-metadata.json` |
| 18:41:42 | `ipiranga_rt_2025.png` (plot 2735) |

**[A]** Facts: the derived weekly/biweekly files and the two `rt_estimate_*` figures were
written *before* the 109-row dataset existed on disk. The final figure comes from the
109-row dataset.

**[I]** Inference (not recorded): the derived files were built from the 59-row pull; two
tool-based Rt estimates were produced on weekly and biweekly bases; a deeper pull was then
made because the 59-row window gives no baseline for the start of 2025; and the final
figure was recomputed from that deeper pull.

**[U]** Not recorded, therefore **not reconstructed**:
* whether the deeper pull was planned up front or introduced mid-execution;
* whether the two `rt_estimate_*.webp` runs were a deliberate "compare against the
  built-in tool" step — the naming is consistent with a tool-generated plot
  (`rt_estimate_<hash>.webp`) rather than the sandbox script (which writes a named PNG),
  but no record names the tool;
* whether any sensitivity analysis was run, and if so with what parameters.

Note also that value equality alone cannot tell you which dataset the derived weekly file
came from: the 109-row dataset filtered to `>= 2024-12-01` yields the identical 57 weeks.
Only the timestamps disambiguate, and only in one direction.

## 5. Retrieval failures and substitutions

| Item | Status |
|---|---|
| Original **task plan** (any `update_todos` state) | **[U]** not persisted anywhere queryable |
| Original **response text**, in full | **[U]** only a truncated narrative survives in conversation history. `plot_2735_record.json` preserves its opening sentence, which was stored as the plot description |
| **Snippet 15649 stored source** | **[A-]** the snippet record exists (`title="Plot 2735"`, python, 2026-11-25), but two `search_code_snippets` queries returned no match, so its stored text could not be read by the available tools. The file shipped here is the generating code recorded inside **plot 2735's own record** — the same script, bound to the same figure |
| **Comparison output** from the pre-implemented Rt capability | **[U]** the two `.webp` plots are archived, but the numeric table they came from was not saved |
| **Execution call log** | **[U]** no tool-call log is retrievable |

## 6. Known defects in the recovered artifacts (not corrected — preserved as-is)

1. **RO-Crate descriptions are wrong.** Both say *"Dengue data from Mosqlimate / InfoDengue
   for 2023 in Parana"* / *"for 2024"*, but the two datasets span 2023-12→2025-12 and
   2024-12→2026-01. The crate itself tags the field source as `"data_inferred"`, i.e.
   machine-guessed from the directory name's first year. Do not quote these descriptions.
2. **`rt_estimate_8573ff9a.webp` / `rt_estimate_a2dc5f17.webp` are unattributed.** Nothing
   in the archive states which tool produced them or what parameters were used.
3. **Population is hard-coded** as `14230` in the script rather than read from the `pop`
   column, so incidence would silently mis-scale on any other municipality.
4. **Upstream `Rt` is carried in the derived weekly file** (`infodengue_Rt`) and is easy to
   confuse with the re-estimated Rt. They are different quantities and must not be pooled.
