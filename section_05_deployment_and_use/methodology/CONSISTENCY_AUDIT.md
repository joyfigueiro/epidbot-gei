# Section 5 — consistency audit

Every quantitative statement planned for Section 5 was traced back to a file. This
document records what was found: what reconciles, what conflicts, and what has no
support at all. It is the companion to
[`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md), which records the machine
checks, and it is deliberately blunt.

**Status key**

| Status | Meaning | Manuscript action |
| --- | --- | --- |
| `OK` | reproduces exactly from an archived file | quote freely |
| `DEFINE` | reproduces only once a definition is stated | quote with the definition |
| `FIX` | internally inconsistent, resolvable by the authors | resolve before submission |
| `UNSUPPORTED` | no evidence in the repository | remove or obtain evidence |
| `MISSING` | the quantity was never measured | state as a limitation |

---

## A1. `10,863` — UNSUPPORTED (blocking)

The draft reports 10,863 twice, as "consultations" and as "tool calls across 36
functional categories".

- No file in the repository contains 10,863.
- No file contains a tool-call table at all, so "36 functional categories" cannot
  be checked either.
- The same integer cannot be both a count of user consultations and a count of tool
  calls.

The nearest archived quantity is **10,937**, the sum of the workspace-group message
rows, which the data dictionary explicitly forbids using as a platform total
(groups overlap; the sum inflates the true total by 57 %). The gap of 74 between
10,863 and 10,937 matches no archived quantity.

**Action.** Delete 10,863. Replace with 6,967 messages (S4) for the platform total.
If a tool-call statement is wanted, it requires a new extraction, specified in §C1.

---

## A2. "Verified" accounts are fewer than active accounts — FIX

| Quantity | Value |
| --- | --- |
| Registered accounts | 286 |
| Verified accounts | 223 |
| Active accounts | 237 |
| Active / registered | 82.9 % |
| Active / verified | **106.3 %** |

If the three numbers were a funnel, active accounts (237) could not exceed verified
accounts (223). The 14-account excess means "verified" is *not* a property
satisfied by every active account: most plausibly the flag covers one
authentication route (e.g. institutional e-mail) while federated logins never set
it, or the two figures come from extracts taken at different moments.

**Action.** Either obtain the definition and report the two figures in separate
sentences, or drop the verified count. Do **not** present "286 registered → 223
verified → 237 active" as a conversion funnel — a referee will notice in one pass.

---

## A3. Two denominators under one label — FIX

"Requesting two or more capabilities" was computed twice:

- 59 / 141 = **41.8 %** (eligible base) — the headline figure.
- 17 / 45 = 37.8 %, 12 / 43 = 27.9 %, 13 / 41 = 31.7 %, 11 / 38 = 28.9 %,
  6 / 19 = 31.6 % (all-prompt base, per context).

Both appear in archived files. Quoting both as "the share of multi-capability
requests" is a contradiction. The same applies to the mean: 1.42 (all prompts) vs
1.68 (eligible) for external government.

**Action.** Use the eligible base throughout §5.4. Table 5.6 states its base in the
caption and shows per-context `n`. The `_of_all` columns stay in the CSV for
transparency and are not quoted.

---

## A4. Cross-domain integration is `nsources ≥ 2` — DEFINE

The set of prompts flagged `crossdomain == 1` is **exactly** the set with
`nsources ≥ 2` — all eight, same prompt ids. The two variables are one variable.

So the finding "8 requests (4.3 %) called for explicit cross-domain data
integration" is, operationally, "8 requests named two or more distinct data
sources". That is a weaker and more defensible statement, and it matters, because
cross-domain integration is one of the five GEI areas: at prompt level it is
**rarely requested explicitly**.

**Action.** Report it as "named two or more data sources (8/186, 4.3 %)", and do not
claim the integration capability is prominent in demand. Supporting evidence for
integration composition, if needed, comes from the Ipiranga case (which chains
InfoDengue/Mosqlimate with derived series), not from the prompt corpus.

---

## A5. Eligibility rule for the 141 — DEFINE

The denominator 141 is not the count of prompts with ≥1 capability code (that is
146). It is 186 minus 9 out-of-scope minus 36 platform-meta-only. Three prompts carry
capability codes *and* are out of scope; they are excluded by objective.

**Action.** State the rule in Methods (done in
[`SECTION5_METHODS.md`](SECTION5_METHODS.md) §4.5). Without it, a reader who
recounts from the CSV gets 146 and cannot reproduce 41.8 %.

---

## A6. Objective code glossary — DEFINE

The ten objective codes (`RES`, `META`, `DESC`, `TRAN`, `SURV`, `OOS`, `RISK`,
`PLAN`, `FORE`, `COMP`) have no documented key anywhere in the repository. Glosses
in this repository are **inferred** from the coded prompts and from the
cross-tabulation with capability codes, and are marked as such in every table.

**Action.** Supply the codelist from the original coding sheet, or accept the
glosses and say they are the authors' reconstruction. Either way, Table 5.5's
gloss column must not be presented as an archived definition.

---

## A7. Sampling of the 186 — MISSING

No selection rule is recorded. It is not known whether the corpus is a random
sample, a stratified sample, or a convenience sample of notable sessions, nor
whether it was drawn before or after the capabilities were defined.

**Action.** Supply the rule. Until then, no prompt-level percentage may be
generalised beyond the corpus, and no confidence interval may be attached. If the
sample was purposive, say "purposive" and drop inferential statistics.

---

## A8. Single-coder classification — MISSING

There is no record of a second independent coding and therefore no kappa. The
manuscript must not describe the procedure as manual human coding, and must not
imply coder agreement.

**Action.** State "single-coder, LLM-assisted classification; the coding guide and
the coded corpus are published, and no inter-rater reliability is reported". If time
allows, double-code 40 prompts and report Cohen's kappa — the single highest-value
addition available before submission.

---

## A9. Growth over time — MISSING

Four cumulative snapshots of one database and one weekday profile. There is no
monthly or weekly activity series anywhere in the repository.

**Action.** No trend claim. The only defensible temporal statements are the
S1→S4 delta (+19 sessions, +279 messages, +4 accounts, +27 questions over 14 days)
and the weekday rhythm.

---

## A10. Artifacts produced — MISSING

Plots, reports, datasets and dashboards exist as user-facing objects, but no table
maps them to sessions, and none is archived. Requests therefore cannot be matched to
deliverables except in the one hand-traced case.

**Action.** §5.5 is written as one fully traced investigation plus a coded
distribution of requests, and says explicitly that completion is not measured. See
`docs/en/06_ethics_and_limitations.md`, which already makes this point.

---

## A11. Geographic and institutional distribution — MISSING by design

Group labels were pseudonymised before publication and no geography is stored.

**Action.** §5.1 reports *contexts* (internal, government, academic, international,
walk-in) and *pseudonymous group codes*, and states that geographic distribution is
not reported for data-protection reasons. Do not promise a map.

---

## A12. Figure provenance — FIXED

`figures/audit/fig1`–`fig10` had no generating script and were rendered at 150 dpi,
below the 300 dpi usually required for raster submission. Content language could not
be verified because the SVG text is stored as outlines.

**Action taken.** Section 5 figures are now generated by
`scripts/make_section5_figures.py` from the derived tables at 300 dpi PNG plus
vector PDF, in English. The ten legacy figures are left untouched in
`figures/audit/` as historical records; they are not referenced by Section 5.

---

## A13. Group rows are not additive — OK, already documented

The group rows sum to 10,937 against a total of 6,967 (inflation 57 %). Both
`data/DATA_DICTIONARY.md` and the verification script state that groups are
workspace labels rather than partitions. This is the one place where the earlier
documentation was already airtight.

**Action.** Keep the caveat wherever group activity appears.

---

## Summary

| # | Item | Status |
| --- | --- | --- |
| A1 | `10,863` | UNSUPPORTED — remove |
| A2 | Active exceeds verified | FIX |
| A3 | Two denominators for multi-capability share | FIX |
| A4 | `crossdomain` ≡ `nsources ≥ 2` | DEFINE |
| A5 | Eligibility rule for 141 | DEFINE (now documented) |
| A6 | Objective code glossary | DEFINE |
| A7 | Sampling of the 186 | MISSING |
| A8 | Inter-rater reliability | MISSING |
| A9 | Activity over time | MISSING |
| A10 | Artifacts produced | MISSING |
| A11 | Geography | MISSING by design |
| A12 | Figure provenance | FIXED |
| A13 | Group non-additivity | OK |

Nine of thirteen items are definitional or documentary and can be closed by the
authors without new data. Two (A2, A4) need one file each from the platform. Two
(A7, A8) need a decision and, in A8's case, about two hours of work.
