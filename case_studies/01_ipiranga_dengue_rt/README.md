# Case study 01 — Ipiranga (PR) dengue Rt, 2025

Supplementary computational evidence for the GEI/EpidBot paper:
**weekly effective reproduction number (Rt) for dengue in Ipiranga, Paraná, Brazil, 2025.**

Corresponds to **Sections 4.3 (orchestration and adaptive repair)** and
**4.4 (provenance and traceability)**.

This directory contains artifacts **recovered from the original session** (datasets,
RO-Crates, the figure, the generating code) alongside **documentation and
reproducibility code written afterwards**. The two categories are kept in separate
directories and labelled throughout. **Nothing in `artifacts/` was edited** — every file
is byte-identical to the copy that still exists in the original storage location, and
the digests are in `MANIFEST.csv`.

> **Read `provenance.md` first.** It grades every claim in the original answer against
> the stored evidence. Several headline numbers — including the Rt values and the growth
> episodes — cannot be re-derived from what was archived, because they exist only in the
> chat narrative. They are marked `[N]` there.

---

## 1. Directory structure

```
case_studies/01_ipiranga_dengue_rt/
├── README.md                          NEW  (this file)
├── provenance.md                      NEW  (evidence tiers, defects, gaps)
├── MANIFEST.csv                       NEW  (sha256 + origin of every file)
├── artifacts/                         RECOVERED — byte-identical, never modified
│   ├── data/
│   │   ├── ds_2023-12-01_2025-12-28/
│   │   │   ├── data.parquet               27,834 B · 109 rows · SE 202349–202553
│   │   │   └── ro-crate-metadata.json      2,728 B
│   │   └── ds_2024-12-01_2026-01-15/
│   │       ├── data.parquet               22,831 B · 59 rows · SE 202449–202602
│   │       └── ro-crate-metadata.json      2,728 B
│   ├── derived/
│   │   ├── ipiranga_weekly_2025.parquet       57 rows
│   │   ├── ipiranga_biweekly_2025.parquet     29 rows
│   │   ├── rt_estimate_a2dc5f17.webp          67,320 B
│   │   └── rt_estimate_8573ff9a.webp          86,512 B
│   ├── figures/
│   │   ├── ipiranga_rt_2025.png               159,506 B — plot id 2735
│   │   └── plot_2735_record.json              recovered plot metadata
│   └── code/
│       ├── snippet_15649__plot_2735.py        generating code (see caveat below)
│       └── snippet_15649_record.json          snippet metadata + retrieval log
├── documentation/                     NEW
│   └── interaction_transcript.md      conversation-derived transcript of session 867
└── reproducibility/                   NEW — not executed when this directory was built
    ├── reproduce_rt.py
    └── requirements.txt
```

### Map to original storage locations

| In this directory | Original path / identifier |
|---|---|
| `artifacts/data/ds_2023-12-01_2025-12-28/` | `/data/mosqlimate/infodengue_dengue_4110508_2023-12-01_2025-12-28/` |
| `artifacts/data/ds_2024-12-01_2026-01-15/` | `/data/mosqlimate/infodengue_dengue_4110508_2024-12-01_2026-01-15/` |
| `artifacts/derived/ipiranga_weekly_2025.parquet` | `/data/public/ipiranga_weekly_2025.parquet` |
| `artifacts/derived/ipiranga_biweekly_2025.parquet` | `/data/public/ipiranga_biweekly_2025.parquet` |
| `artifacts/derived/rt_estimate_*.webp` | `/data/plots/rt_estimate_*.webp` |
| `artifacts/figures/ipiranga_rt_2025.png` | `/data/plots/ipiranga_rt_2025.png` — **plot id 2735** |
| `artifacts/code/snippet_15649__plot_2735.py` | **code snippet 15649**, title `Plot 2735` |

### Caveat on `artifacts/code/snippet_15649__plot_2735.py`

The snippet **record** exists (id 15649, title `Plot 2735`, python, 2026-11-25), but its
**stored source could not be retrieved** — two `search_code_snippets` queries returned no
match. What is shipped here is the generating code recorded inside **plot 2735's own
record**, which is the script that produced the archived PNG. It is the same run, but it
is a **substitution for an unretrievable snippet payload**, not the payload itself. This
is recorded in `artifacts/code/snippet_15649_record.json` under `substitute_used`.

---

## 2. What the investigation did (as reconstructable from artifacts)

1. Pulled InfoDengue weekly dengue counts for Ipiranga (`municipio_geocodigo = 4110508`)
   from Mosqlimate, window `2024-12-01 → 2026-01-15` (59 epi-weeks, SE 202449–202602).
2. Derived `ipiranga_weekly_2025.parquet` (57 rows, SE 202449–202553) and
   `ipiranga_biweekly_2025.parquet` (29 two-week rows; case total 140 in both).
   Verified at packaging time: the weekly file is exactly the 59-row dataset truncated to
   `SE <= 202553`, and the biweekly file is exactly its 14-day aggregation.
3. Produced two `rt_estimate_*.webp` figures whose generating tool is **not recorded**.
4. Pulled a **second, deeper** InfoDengue window `2023-12-01 → 2025-12-28`
   (109 rows, SE 202349–202553).
5. Ran the custom sandbox script (snippet 15649) on that deeper dataset and wrote
   `ipiranga_rt_2025.png` (plot 2735): Cori et al. (2013) sliding-window Rt,
   7-week window, `Gamma(1, 0.2)` posterior prior, gamma serial interval discretised at
   `mean = 2.0` weekly periods, `sd = 1.0` (i.e. 14 d / 7 d), incidence per 100,000
   against a hard-coded population of 14,230.

That step 4 precedes step 5 is visible in file timestamps only. **Why** the deeper pull
was made is inference, not record — see `provenance.md` §4.

---

## 3. Reproducing

```bash
cd case_studies/01_ipiranga_dengue_rt
pip install -r reproducibility/requirements.txt

python reproducibility/reproduce_rt.py \
    --dataset artifacts/data/ds_2023-12-01_2025-12-28/data.parquet \
    --outdir ./out
```

`reproduce_rt.py` re-implements the archived estimator with portable paths and explicit
CLI parameters. It is **new code**, written for this archive; it is *not* the original
artifact. The authoritative script is `artifacts/code/snippet_15649__plot_2735.py`, which
contains absolute `/data/...` paths and writes directly to `/data/plots/`.

**These numbers were not regenerated when this archive was built.** The script was
written but not executed, so that fresh output is never confused with the original run.
Running it produces **new** numbers: report them as a fresh reproduction, never as
corroboration of the original session.

---

## 4. Checks performed at packaging time

| Check | Result |
|---|---|
| Byte-identical copy of every artifact | Yes — `shutil.copy2`, sha256 in `MANIFEST.csv` |
| Manifest digests re-verified after copy | 16/16 match |
| Bundle copy vs original storage path, byte identity | 9/9 identical |
| Weekly file vs 59-row dataset truncated to SE<=202553 | Identical `SE`, `casos`, `Rt` |
| Weekly file vs 109-row dataset filtered to >=2024-12-01 | Identical `SE` list (same 57 weeks) |
| Biweekly file vs 14-day aggregation of weekly | Identical, both total 140 cases |
| 2025 subtotal reproducible from archived parquet | 52 weeks, 137 cases, 962.8 / 100k |
| Credentials / tokens / personal data present | None found — see §5 |
| Unrelated-session artifacts excluded | Yes — see §6 |

The 2025 burden figures (137 cases, 962.8/100k) are the only *analytical* quantities
re-verified here, and only by direct summation — no Rt was recomputed.

---

## 5. Data, licensing and redistribution

* **Upstream source**: InfoDengue / Mosqlimate (`api.mosqlimate.org`), municipality-level
  weekly dengue aggregates for Ipiranga, Paraná.
* **Granularity**: municipality-week counts. No patient-level records, no identifiers,
  no personal data — neither LGPD nor GDPR is implicated by these files.
* **Licence**: the recovered RO-Crates carry **no licence field**. Redistribution is
  therefore governed by the upstream InfoDengue / Mosqlimate terms of use, which this
  archive does not restate. **Verify upstream terms before republishing these parquet
  files**, and cite InfoDengue (Fiocruz) and Mosqlimate.
* **No credentials**: no API keys, tokens, cookies, `.env`, `config.db`,
  `chat_history.duckdb` or `private/` data is included. A pattern scan for
  `api_key|token|secret|password|bearer|authorization` plus GitHub/AWS/Slack/OpenAI key
  formats, private-key blocks, e-mail addresses and personal absolute paths over every
  file in this directory returned **no hits**.

---

## 6. Deliberately excluded

Named `ipiranga` but belonging to **other sessions**, so they are *not* part of this
investigation:

* `/data/public/_ipiranga_weekly.parquet` — 573 rows × 22 cols, schema
  `data/se/casos/...`, mtime 2026-09-17
* `/data/public/_ipiranga_detectores.parquet` — mtime 2026-09-17
* `/data/public/_ipiranga_peers_weekly.parquet` — mtime 2026-09-17
* `private/5/ipiranga_demo_ubs_1_semana/` — mtime 2026-06-16

---

## 7. Known limitations

1. **The original information-gated chain is partly lost.** No tool-call log and no task
   plan survive; the transcript in `documentation/` is conversation-derived and
   **truncated**. See the warning box at the top of that file.
2. **The Rt values are narrative-only.** Every Rt figure in the original answer is graded
   `[N]` in `provenance.md` §3 because the archive was built under an instruction not to
   produce new analysis.
3. **Snippet 15649's payload is a substitution** (see the caveat in §1).
4. **The two `.webp` files are unattributed.** They exist and predate the PNG, but which
   tool produced them and with which parameters is not recorded.
5. **The RO-Crate descriptions are factually wrong** — they read "for 2023" / "for 2024"
   while the data actually cover 2023-12-01→2025-12-28 and 2024-12-01→2026-01-15.
   The files were not corrected, to preserve originality. See `provenance.md` Defect 1.

---

## 8. Citation

If you use this archive, cite the GEI/EpidBot paper, plus InfoDengue (Fiocruz) and
Mosqlimate for the underlying surveillance data. See `MANIFEST.csv` for digests.
