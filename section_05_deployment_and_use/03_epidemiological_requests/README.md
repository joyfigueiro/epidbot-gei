# 5.3 Epidemiological requests and analytical objectives

**Question.** What were users actually trying to accomplish?

**Short answer.** Of 186 coded requests, the two largest categories are research and
writing support (56, 30.1 %) and platform-meta questions (52, 28.0 %). Substantive
epidemiological description accounts for 21 (11.3 %). The platform is therefore used
as much to *produce and check science* and to *learn what it can do* as to compute
epidemiology — a demand profile that the architecture has to serve, not a weakness of
the user base.

## Evidence

| File | Content |
| --- | --- |
| `derived/objectives.csv` | ten objective codes with counts and shares |
| `derived/sample_funnel.csv` | 186 → (36 meta-only + 9 out-of-scope) → 141 eligible |
| `CODING_GUIDE.md` | the codebook, decision rules, worked examples |
| Table `t5_5`, `t5_9` | LaTeX |
| Figure `fig5_4` | objective distribution |

## Verified numbers

| Code | Inferred gloss | $n$ | % of 186 |
| --- | --- | --- | --- |
| `RES` | Research and writing support | 56 | 30.1 |
| `META` | Platform-meta question | 52 | 28.0 |
| `DESC` | Descriptive epidemiology | 21 | 11.3 |
| `TRAN` | Data transformation / parameter rescaling | 14 | 7.5 |
| `SURV` | Surveillance monitoring | 14 | 7.5 |
| `OOS` | Out of scope | 9 | 4.8 |
| `RISK` | Risk assessment | 7 | 3.8 |
| `PLAN` | Analytical planning | 7 | 3.8 |
| `FORE` | Forecasting | 4 | 2.2 |
| `COMP` | Comparison across units | 2 | 1.1 |

All ten counts reproduce `data/audit/objectives.csv` exactly.

## Demand is shaped by context, not only by volume

| Context | Largest objectives | Reading |
| --- | --- | --- |
| External walk-in | `META` 52.6 %, `DESC` 18.4 % | discovery first: new users ask what exists |
| External academic | `RES` 41.5 %, `TRAN` 19.5 % | production of science and model upkeep |
| External government | `RES` 42.2 %, `DESC` 15.6 %, `FORE` 6.7 % | documents and surveillance; all external forecasting lives here |
| External international | `META` 36.8 %, `SURV` 21.1 % | situational awareness before analysis |
| Internal core team | `RES` 34.9 %, `PLAN` 11.6 % | building the platform and planning investigations |

This differential profile is the most defensible empirical result in §5.3, because it
survives at the level of raw counts and does not depend on the capability coding.

## Two warnings before writing this subsection

**1. The glosses are inferred.** The code-to-label key is not in the repository.
[`CODING_GUIDE.md`](CODING_GUIDE.md) reconstructs it from the corpus; every table
labels it "inferred". Either supply the original codelist or state that the glosses
are the authors' reconstruction.

**2. The sample is purposive.** The selection rule for the 186 requests is not
documented. Therefore:

- write "of the 186 coded requests", never "of user requests";
- attach no confidence interval and run no test;
- do not read the 30.1 % / 28.0 % split as a population share.

## What may be claimed

- The request profile spans the full range of GEI work, from dataset discovery to
  modelling, with writing and meta questions dominating.
- The profile differs by context in an interpretable way.
- Out-of-scope requests exist and are concentrated among walk-in users (7.9 % versus
  0 % internationally).

## What may not be claimed

- That a share of requests *is* a share of all usage (§A7).
- That a user asking for a figure obtained one (§A10).
- That `RES`-heavy demand means the platform is "used for science" in any evaluative
  sense — the corpus cannot distinguish drafting from verification.
