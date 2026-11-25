# 5.1 Deployment and user base

**Question.** Who used the platform, and in which contexts?

**Short answer.** 286 registered accounts, 237 of them active in the window,
distributed across five identifiable contexts and twelve pseudonymous workspace
groups. The internal team accounts for the largest single share of activity; the
external base is heterogeneous in a way that matters more than its size.

## Evidence

| File | Content |
| --- | --- |
| `derived/platform_totals.csv` | headline indicators with derived ratios and the source of each |
| `derived/snapshot_reconciliation.csv` | the four extractions and their deltas |
| `derived/group_activity.csv` | twelve workspace groups, pseudonymised |
| `../../data/usage_snapshots.csv`, `../../data/usage_by_group.csv` | raw aggregates |
| Table `t5_11`, `t5_12` | LaTeX |
| Figure `fig5_5(b)` | activity by group |

## Verified numbers

| Indicator | Value |
| --- | --- |
| Registered accounts | 286 |
| Verified accounts | 223 |
| Active accounts in window | 237 |
| Sessions | 667 |
| Messages (user + assistant) | 6,967 |
| User questions | 995 |
| Window | 2026-03-28 to 2026-11-10 (227 days) |
| Messages per session | 10.45 |
| Messages per active account | 29.4 |
| Questions per active account | 4.20 |

## Contexts, not geography

Contexts are coded as: internal core team (43 coded prompts), external government
(45), external academic (41), external walk-in (38), external international (19).

**Geographic and institutional distribution is not reported.** Group labels were
pseudonymised before publication and no geography is stored in any published file.
This is a deliberate data-protection choice, not a gap in the analysis, and the
manuscript must say so rather than promise a map it cannot show.

## What may be claimed

- The platform ran with a live user base across at least five distinct contexts, of
  which four are external.
- Activity is concentrated: the ten most active accounts produced 39.9 % of all
  messages in both the 2026-10-27 and the 2026-11-10 extraction, while being 4.3 %
  and 4.2 % of active accounts. The stability of that share across two extractions
  is the strongest single concentration signal in the dataset.
- The internal team is not the only producer of content: four external contexts are
  present in the coded corpus with 143 of 186 prompts.

## What may not be claimed

- **Any funnel from registered to verified to active.** Active accounts (237) exceed
  verified accounts (223). The two flags are not nested. See
  [`../methodology/CONSISTENCY_AUDIT.md`](../methodology/CONSISTENCY_AUDIT.md) §A2.
- **Growth or adoption trend.** Four cumulative snapshots of one database are not a
  time series.
- **Institutional impact.** No file records what any institution did with an output.
- **Professional identity.** The corpus stores context labels, never occupations.
  Do not write "epidemiologists used it" unless that comes from somewhere else.
