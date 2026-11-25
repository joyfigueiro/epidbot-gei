# 5.4 Composition of GEI capabilities

**Question.** When the five GEI areas are put in front of real users, how are they
combined?

**Short answer.** Over the 141 eligible requests, visualization and reporting is the
most requested area (59, 41.8 %), followed by data integration (57, 40.4 %) and
epidemiological analysis (49, 34.8 %); mathematical modelling is last (24, 17.0 %).
The mean is 1.61 areas per request, and 59 requests (41.8 %) ask for two or more.
**Composition is real but shallow**: the dominant multi-capability pattern is
analysis with reporting, not a five-way pipeline.

This is the empirical core of the manuscript. It is also the part that reproduces
exactly, cell by cell, against the archived marginals.

## Evidence

| File | Content |
| --- | --- |
| `derived/capability_prevalence.csv` | five areas, $n$ and % over 141 |
| `derived/composition_depth.csv` | distribution of areas per request |
| `derived/cooccurrence.csv` | 5×5 symmetric matrix |
| `derived/top_combinations.csv` | most frequent exact combinations |
| `derived/context_profile.csv` | profile by context, both denominators |
| `derived/internal_external.csv` | internal versus external, all 186 |
| `derived/evidence_dimensions.csv` | named sources, cross-domain, continuity |
| Tables `t5_1`–`t5_8` | LaTeX |
| Figures `fig5_1`, `fig5_2`, `fig5_3` | manuscript candidates |

## Verified numbers (base: 141 eligible requests)

| Area | Code | $n$ | % |
| --- | --- | --- | --- |
| Visualization and reporting | `V` | 59 | 41.8 |
| Integration of heterogeneous data sources | `I` | 57 | 40.4 |
| Epidemiological analysis | `A` | 49 | 34.8 |
| Access to scientific knowledge | `K` | 38 | 27.0 |
| Mathematical modelling | `M` | 24 | 17.0 |

Composition depth: 1 area → 82 requests (58.2 %); 2 → 36 (25.5 %); 3 → 19 (13.5 %);
4 → 4 (2.8 %). Mean **1.61**; two or more in **59** requests (**41.8 %**).

Co-occurrence (off-diagonal counts): `A–V` 26, `I–A` 21, `I–V` 14, `K–M` 11,
`K–V` 11, `K–A` 10, `A–M` 10, `M–V` 9, `I–M` 3, `I–K` 2.

## The structural reading

Three facts, in order of importance for the manuscript's argument:

1. **Data plus analysis plus reporting is the modal combination** (`A+I+V`, 12
   requests), and `A+I` adds 7 more. Composition in practice is a two- or three-step
   chain around retrieval and communication, not a full pipeline.
2. **Modelling is the least requested area (17.0 %) and the most *paired* one.** Of
   the 24 requests involving `M`, 11 also involve `K` and 10 involve `A`: modelling
   almost never comes alone. Requests that reach the modelling layer arrive already
   carrying a knowledge or analysis component.
3. **Integration is context-dependent, spectacularly so.** Among eligible prompts,
   `I` rises from 20.7 % in the academic context to 80.0 % among walk-in users and
   58.8 % internationally, while `V` falls from 58.6 % (academic) to 17.6 %
   (international). Integration demand is a *discovery* phenomenon: users ask for
   access before they ask for output.

## Explicit cross-domain integration is rare — read this before writing the claim

`crossdomain` and `nsources ≥ 2` are the same eight requests. So the honest statement
is: **8 of 186 requests (4.3 %) named two or more distinct data sources**, and that is
the only measurable trace of cross-domain demand at prompt level.

The five-area composition claim must therefore rest on *combination depth* (mean 1.61,
41.8 % multi) and *co-occurrence structure*, not on explicit cross-domain requests.
Evidence that heterogeneous sources are actually stitched together comes from the
traced exemplar in §5.5, which chains a surveillance API with derived series and a
verification pass. See consistency audit §A4.

## Continuity

80 of 186 requests (43.0 %) depend on previous conversational context or on an
artifact produced earlier. This is the closest available proxy for investigational
continuity, and it is a proxy only: the corpus has no session-level linkage, so
"investigations that continued across sessions" cannot be counted.

## What may be claimed

- Prevalence, depth and co-occurrence as tabulated, with the base of 141 stated.
- That combination is common but shallow: median two areas, 2.8 % at four.
- That composition differs by context in a way that maps onto what each context is
  trying to do.
- That modelling is rarely requested in isolation.

## What may not be claimed

- **Executed composition.** No tool-call record exists. §5.4 measures *demand*. The
  sentence "users composed five capabilities into one investigation" cannot be
  supported from this corpus; it needs the Ipiranga-style trace.
- **Autonomous orchestration.** Nothing in the prompt text shows which tools ran.
- **Significance.** No test, no interval, no $p$-value on a purposive sample.
- **Either denominator silently.** The all-prompt version (e.g. 27.9 %–37.8 % by
  context) is in the CSV as `_of_all`; it must never be quoted under the same label
  as 41.8 % (§A3).
