# 5.5 GEI in real-world settings

**Question.** What does Generalized Epidemic Intelligence look like when it is
actually used?

**Short answer.** One investigation is traced end to end, with data, code, figure and
a verification pass that caught an error in the original narrative. Around it, a coded
inventory of fourteen request archetypes shows how the five areas appear across
contexts. The section is honest about the asymmetry: exactly one chain is complete,
and the rest is demand evidence.

This is deliberately **not** a collection of constructed disease case studies. Every
example below came from the operational record.

## Evidence

| File | Content |
| --- | --- |
| `EXAMPLE_INVENTORY.csv` | fourteen archetypes with provenance and evidence level |
| `derived/failure_modes.csv` | seven friction categories |
| `derived/discovery_questions.csv` | the discovery-request cluster, with text |
| `../../case_studies/01_ipiranga_dengue_rt/` | the traced exemplar |
| Figure `fig5_6` | friction observed in the record |
| Table `t5_10` | friction categories |

## The traced exemplar (EX-01)

Ipiranga (PR, IBGE 4110508) dengue $R_t$ for 2025 is the only investigation in this
repository with the full chain archived: request, plan, tool calls, retrieved data,
derived series, generating code, figure, and an independent verification pass. It is
also the only place where a claim about *execution* can be checked.

Its verification pass is itself part of the argument. Revision 2 re-executed the
archived estimator on the archived data and found one narrative figure wrong
("30/50 weeks" became **30/52**), resolved six flagged inconsistencies, and left the
original artifacts byte-identical, with the corrections living in a separate
`verification/` tree. That is the behaviour the manuscript claims for the
architecture, demonstrated on a real case rather than asserted.

Use it for: traceability, adaptive repair, and what a completed GEI investigation
looks like. Do not generalise from it: $n = 1$.

## The distribution (EX-02 to EX-14)

Context shapes demand in a way that is worth a paragraph each:

| Context | Signature | Examples |
| --- | --- | --- |
| Internal core team | planning and construction; `PLAN` almost exclusive (5 of 7) | EX-02, EX-03, EX-04 |
| External academic | science production; `RES` 41.5 %, `TRAN` 19.5 % | EX-05, EX-06 |
| External government | documents, surveillance, all external forecasting | EX-07, EX-08, EX-09 |
| External international | orientation before analysis; `SURV` 21.1 %, `META` 36.8 % | EX-10, EX-11 |
| External walk-in | discovery; `META` 52.6 %, `I` 80.0 % of eligible | EX-12, EX-13 |

## Friction — and the one that matters

| Category | $n$ | % of 186 | Groups |
| --- | --- | --- | --- |
| Provenance / hallucination distrust | 9 | 4.8 | 4 |
| Report or artifact persistence | 6 | 3.2 | 3 |
| Artifact not delivered or not found | 4 | 2.2 | 3 |
| Stalled, slow or bottlenecked | 4 | 2.2 | 4 |
| Doubt about data coverage | 4 | 2.2 | 4 |
| Input or format incompatibility | 3 | 1.6 | 3 |
| Retry after failed execution | 1 | 0.5 | 1 |

Thirty-one mentions across 186 requests. The largest category is not a usability
complaint: **it is distrust that a number or a citation was invented**, and it appears
in four different workspace groups, internal included. Two smaller categories —
artifact persistence and artifact retrieval — are the same failure seen from both
sides: things were produced and could not be found again.

This is the strongest material in §5.5 for the Discussion, because it is a
substantive finding about what users of an agentic epidemiological system worry about,
and it is measurable.

## Discipline for this subsection

1. **Label every example with its evidence level** (E1/E3) in the text or the caption.
2. **Never quote EX-13.** It is an out-of-scope personal medical request. Its value is
   categorical — that the boundary is tested — and it must be described at the level
   of category, never content.
3. **Do not convert an archetype into a case study.** EX-07 is "government users asked
   for surveillance figures", not "a health department produced its surveillance
   report with EpidBot". The second claim needs an artifact and a counterpart we do
   not have.
4. **Do not claim institutional impact.** No file records what any institution did
   with an output.

## What may be claimed

- Real demand spans discovery, analysis, modelling, reporting and writing, with a
  context-specific signature for each.
- One investigation is traced end to end, including a verification pass that found and
  corrected an error.
- Friction is documented and its leading category is provenance distrust, not speed.

## What may not be claimed

- That any archetype other than EX-01 completed successfully.
- That the platform changed a decision, a report or an outbreak response anywhere.
- That the fourteen archetypes are a complete taxonomy: they are a curated selection
  from a corpus whose sampling rule is undocumented.
