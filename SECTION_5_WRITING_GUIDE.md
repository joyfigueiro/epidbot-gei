# Section 5 — writing guide

**Generalized Epidemic Intelligence in Practice**

Prepared 2026-11-25 for the writing session of 2026-11-26. Everything below is
traceable to a file in this repository; where it is not, that is stated.

---

## 1. What Section 5 has to establish

Sections 3 and 4 make three claims: that epidemic intelligence can be generalised
beyond disease-specific pipelines, that the generalisation has an architecture, and
that the architecture is traceable. Section 5 is where those claims meet evidence
that the authors did not generate for the purpose.

The section therefore has one job:

> **Show that the five functional areas of GEI are not a taxonomy imposed on the
> system, but a description of what real users asked it to do — and be precise about
> how far the record can support that.**

The honest shape of the answer is asymmetric, and the section should embrace the
asymmetry rather than hide it:

| Claim | Evidence strength |
| --- | --- |
| Real demand spans all five areas | strong (141 coded requests, cell-verified) |
| Composition is common but shallow | strong (mean 1.61, 41.8 % multi, co-occurrence structure) |
| Demand profile differs by user context | strong (raw-count level, independent of coding) |
| A full investigation can be traced end to end | **one case**, fully archived |
| Sessions completed successfully | **not measured** |

That last row is not a weakness to bury. It is what makes the rest credible.

### Title

Proposed: **Generalized Epidemic Intelligence in Practice**

Alternative if the section reads too close to an evaluation: *Deployment and Use of
an Agentic Epidemic Intelligence System*. Keep "in practice" if the emphasis is on
the demand structure; drop it if a referee might read "practice" as "field
effectiveness", which is not measured.

---

## 2. Structure

### 5.1 Deployment and user base

*Purpose:* establish scale and heterogeneity, and say plainly what cannot be reported.

Opening move: the counts, then immediately the context structure — because the number
of accounts is uninformative on its own and partly internal.

Points to make, in order:

1. 286 registered, 237 active, 667 sessions, 6,967 messages, 995 questions, over 227
   days (28 Mar – 10 Nov 2026).
2. Activity is concentrated: top ten accounts = 39.9 % of messages, stable across two
   extractions two weeks apart (39.8 % / 39.9 %).
3. Five contexts are identifiable, four of them external; 143 of the 186 coded
   requests come from external contexts.
4. Geographic and institutional distribution is withheld at pseudonymisation and is
   not reported. State the reason, once, without apology.

Do **not** write a registered → verified → active funnel: active (237) exceeds
verified (223).

### 5.2 Patterns of platform use

*Purpose:* characterise *how* the platform was used, cross-sectionally.

1. Working-week rhythm, weekend share 14.1 %.
2. Conversational depth: 10.45 messages per session, 7.00 messages per question —
   consistent with multi-turn investigation, not one-shot querying.
3. Concentration, again, from the workspace angle: twelve groups, of which the two
   largest carry most activity — but the rows are not additive and must not be
   turned into shares.
4. Then the boundary: three quantities that would belong here and do not exist
   (time series, tool calls, artifacts). One sentence each, in the Limitations.

*Purpose of including 3 and the boundary:* a reader who trusts §5.2 to be complete
will over-read §5.4. Closing the loop early is cheaper than a referee doing it.

### 5.3 Epidemiological requests and analytical objectives

*Purpose:* answer "what were they trying to do", and make the context-dependence
explicit.

1. The ten-category distribution: `RES` 56 (30.1 %), `META` 52 (28.0 %),
   `DESC` 21 (11.3 %), then a long tail.
2. The interpretive turn: **the platform is used as much to produce and verify
   science, and to find out what it can do, as to compute epidemiology.** This is the
   demand profile an agentic system actually faces.
3. Context differentiation (walk-in = discovery, academic = production, government =
   documents and forecasting, international = orientation, internal = planning).
4. Sampling caveat: purposive corpus, no inference.

### 5.4 Composition of GEI capabilities

*Purpose:* the empirical core. This is the subsection a referee will read closely.

1. Prevalence over 141 eligible requests: `V` 59 (41.8 %), `I` 57 (40.4 %),
   `A` 49 (34.8 %), `K` 38 (27.0 %), `M` 24 (17.0 %).
2. Depth: mean 1.61; 59 requests (41.8 %) ask for two or more; 2.8 % ask for four.
3. **Structure over marginals.** The interesting result is not which area is most
   frequent but how they pair: `A–V` 26, `I–A` 21, and the fact that modelling almost
   never appears alone (11 of 24 `M` requests also involve `K`, 10 involve `A`).
4. Context-dependence of composition: `I` from 20.7 % (academic) to 80.0 %
   (walk-in); `V` from 58.6 % (academic) to 17.6 % (international).
5. Continuity proxy: 80 of 186 requests (43.0 %) depend on earlier context.
6. The honest ceiling: no tool-call record, therefore this is *demand*, not *executed*
   composition. Say it once, clearly, at the end of the subsection.

### 5.5 GEI in real-world settings

*Purpose:* one traced instance plus a documented distribution of demand.

1. Open with the asymmetry as a design choice: one investigation is traced in full;
   the rest is request evidence at level E3.
2. The Ipiranga case (EX-01): request → plan → tools → data → code → figure →
   verification, including the correction that the verification pass forced
   (30/50 → 30/52 weeks). This is where the architecture's claims become checkable.
3. The context signatures (EX-02 to EX-12), one sentence each, grouped by context.
4. Friction: seven categories, 31 mentions, and the finding that the leading category
   is **provenance distrust (9, 4.8 %, four groups)**, not speed or usability.
5. Scope boundary: out-of-scope requests occur and concentrate among walk-in users
   (7.9 %). Describe categorically; never quote.

---

## 3. Canonical numbers — quote only from this table

All values verified against archived files by
`section_05_deployment_and_use/scripts/reproduce_section5.py`.

### Platform (reference extraction S4, 2026-11-10)

| Quantity | Value | Denominator / note |
| --- | --- | --- |
| Registered accounts | 286 | |
| Verified accounts | 223 | not a superset of active — do not use as a funnel |
| Active accounts | 237 | ≥1 turn in window |
| Sessions | 667 | |
| Messages | 6,967 | user + assistant turns |
| User questions | 995 | classified user turns |
| Window | 227 days | 2026-03-28 → 2026-11-10 |
| Messages / session | 10.45 | |
| Messages / active account | 29.4 | |
| Questions / active account | 4.20 | |
| Weekend message share | 14.1 % | 983 / 6,967 |
| Top-ten account share | 39.9 % | 2,779 / 6,967; 4.2 % of accounts |
| Snapshot delta S1→S4 | +19 sessions, +279 messages, +4 accounts, +27 questions | 14 days |

### Coded corpus

| Quantity | Value | Denominator |
| --- | --- | --- |
| Coded requests | 186 | |
| Platform-meta only | 36 | 19.4 % of 186 |
| Out of scope | 9 | 4.8 % of 186 |
| GEI-eligible | 141 | 75.8 % of 186 |
| Mean capabilities per eligible request | 1.61 | 227 occurrences / 141 |
| Requests with ≥2 capabilities | 59 | 41.8 % of 141 |
| Requests with 4 capabilities | 4 | 2.8 % of 141 |
| Requests naming ≥1 data source | 70 | 37.6 % of 186 |
| Requests naming ≥2 data sources | 8 | 4.3 % of 186 (= `crossdomain`) |
| Context-dependent requests | 80 | 43.0 % of 186 |
| Internal / external prompts | 43 / 143 | |

### Capability prevalence (base 141)

`V` 59 (41.8 %) · `I` 57 (40.4 %) · `A` 49 (34.8 %) · `K` 38 (27.0 %) · `M` 24 (17.0 %)

### Co-occurrence (counts, base 141)

`A–V` 26 · `I–A` 21 · `I–V` 14 · `K–M` 11 · `K–V` 11 · `K–A` 10 · `A–M` 10 ·
`M–V` 9 · `I–M` 3 · `I–K` 2

### Context profile (eligible base, per context)

| Context | $n$ eligible | `I` | `K` | `A` | `M` | `V` | multi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Internal core team | 33 | 39.4 | 24.2 | 30.3 | 21.2 | 39.4 | 36.4 |
| External government | 37 | 21.6 | 29.7 | 45.9 | 16.2 | 54.1 | 45.9 |
| External academic | 29 | 20.7 | 37.9 | 17.2 | 24.1 | 58.6 | 44.8 |
| External international | 17 | 58.8 | 29.4 | 23.5 | 17.6 | 17.6 | 35.3 |
| External walk-in | 25 | 80.0 | 12.0 | 52.0 | 4.0 | 24.0 | 44.0 |

### Objectives (base 186)

`RES` 56 (30.1) · `META` 52 (28.0) · `DESC` 21 (11.3) · `TRAN` 14 (7.5) ·
`SURV` 14 (7.5) · `OOS` 9 (4.8) · `RISK` 7 (3.8) · `PLAN` 7 (3.8) · `FORE` 4 (2.2) ·
`COMP` 2 (1.1)

### Friction (base 186)

Provenance distrust 9 (4.8) · report/artifact persistence 6 (3.2) · artifact not
found 4 (2.2) · stalled/slow 4 (2.2) · coverage doubt 4 (2.2) · format
incompatibility 3 (1.6) · retry after failure 1 (0.5)

---

## 4. Claims that must come out of the draft

| Claim | Why it fails |
| --- | --- |
| "10,863 consultations" / "10,863 tool calls across 36 categories" | The number exists in no file, and cannot be both quantities. Nearest archived value, 10,937, is the *non-additive* group sum. See `CONSISTENCY_AUDIT` §A1 |
| Any growth or adoption trend over time | Only four cumulative snapshots; no series exists (§A9) |
| Tool usage by functional category | No tool-call extract at all (§A1) |
| Counts of plots, reports, datasets produced | Not archived against sessions (§A10) |
| Geographic or institutional distribution | Withheld at pseudonymisation (§A11) |
| "Sessions completed successfully" / usefulness | Log records turns, not outcomes |
| "Users combined five capabilities in one investigation" | Prompt text cannot show executed composition (§5.4 ceiling) |
| "286 registered → 223 verified → 237 active" as a funnel | 237 > 223 (§A2) |
| Any confidence interval or test on prompt percentages | Purposive sample, unknown selection (§A7) |
| "Manual human coding" | Single-coder, LLM-assisted, no kappa (§A8) |
| Cross-domain integration as a prominent demand | `crossdomain` ≡ `nsources ≥ 2`; 8 of 186 (§A4) |
| Institutional impact of any example | No file records what anyone did with an output |

---

## 5. Figures

Six figures are ready in `section_05_deployment_and_use/figures/`, each as 300 dpi
PNG and vector PDF, generated by `scripts/make_section5_figures.py` from the derived
CSVs. Numbers in the figures cannot drift from the tables, because the script reads
the tables.

**Recommendation: three figures in the main text, three as supplementary.**

### FIGURE 5 — main text, the candidate centrepiece

`fig5_1_capability_composition` (two panels)

> **Figure 5.** Composition of Generalized Epidemic Intelligence capabilities in real
> requests. (a) Prevalence of the five capability areas among the 141 eligible
> requests; a request may invoke more than one area, so percentages do not sum to 100.
> (b) Number of capability areas requested per prompt. Fifty-nine requests (41.8 %)
> combine two or more areas and the mean is 1.61, indicating that composition is
> frequent but shallow. Base: 141 of 186 coded requests, after excluding 36
> platform-meta and 9 out-of-scope requests.

This single figure carries the section's empirical claim. Panel (b) is what makes it
more than a bar chart.

### FIGURE 6 — main text

`fig5_2_capability_cooccurrence`

> **Figure 6.** Co-occurrence of capability areas across the 141 eligible requests.
> Diagonal cells (shaded) reproduce the marginals. Retrieval and communication
> dominate the pairs (`A–V` 26, `I–A` 21), while modelling rarely appears alone: of
> the 24 requests involving modelling, 11 also involve scientific knowledge and 10
> also involve epidemiological analysis.

### FIGURE 7 — main text

`fig5_5_activity_rhythm_and_groups` (two panels)

> **Figure 7.** Platform activity in the reference window (28 March – 10 November
> 2026; 6,967 messages, 667 sessions, 237 active accounts). (a) Message volume by
> weekday; the weekend accounts for 14.1 % of messages. (b) Messages by pseudonymous
> workspace group. Groups are workspace labels rather than partitions — an account may
> belong to several groups — so group values are absolute activity and do not sum to
> the platform total (sum 10,937 versus 6,967).

### SUPPLEMENTARY — S1

`fig5_3_capability_by_context`

> **Figure S1.** Capability profile by user context, computed over the eligible
> requests of each context. Integration demand rises from 20.7 % among academic users
> to 80.0 % among walk-in users, while visualization demand falls from 58.6 % to
> 17.6 %, indicating that discovery, not output, is the first barrier for new users.

### SUPPLEMENTARY — S2

`fig5_4_analytical_objectives`

> **Figure S2.** Analytical objective of the 186 coded requests. Research and writing
> support (30.1 %) and platform-meta questions (28.0 %) together account for 58 % of
> requests, while descriptive epidemiology accounts for 11.3 %. Objective glosses are
> the authors' reconstruction from the coded corpus and require the original codelist
> for confirmation.

### SUPPLEMENTARY — S3

`fig5_6_observed_friction`

> **Figure S3.** Friction observed in the coded request record (31 mentions across 186
> requests). The largest category is distrust of provenance — explicit doubt that a
> reported number or citation was genuine — appearing in four workspace groups,
> internal included. Speed and usability complaints are less frequent.

---

## 6. Tables

Twelve LaTeX tables are in `section_05_deployment_and_use/tables/`, all booktabs,
all generated by the reproduction script.

| Table | Content | Recommendation |
| --- | --- | --- |
| `t5_1` | capability prevalence (base 141) | main text |
| `t5_2` | composition depth | main text (or fold into Figure 5b) |
| `t5_3` | co-occurrence matrix | supplementary (visual version is Figure 6) |
| `t5_4` | top capability combinations | supplementary |
| `t5_5` | objectives (base 186) | main text |
| `t5_6` | profile by context | main text — this is the context-dependence result |
| `t5_7` | internal vs external | supplementary |
| `t5_8` | evidence dimensions | supplementary |
| `t5_9` | sample funnel | main text or methods |
| `t5_10` | friction categories | main text (visual version is Figure S3) |
| `t5_11` | platform totals | main text |
| `t5_12` | weekday rhythm | supplementary |

If the journal caps tables, `t5_1`, `t5_6` and `t5_11` are the three that must stay.

---

## 7. Limitations paragraph — draft, ready to adapt

> Section 5 characterises the use of a deployed system and is descriptive throughout.
> The request corpus is a purposive sample of 186 requests drawn from a window that
> contains 995, and its selection rule was not recorded, so no proportion reported
> here should be read as a population share and no inferential statistic is
> appropriate. Classification was performed in a single LLM-assisted coding pass
> without independent second coding, so no inter-rater reliability is reported; the
> codebook and the coded corpus are published to make the classification auditable.
> The session log records turns rather than outcomes, so the analysis supports claims
> about demand and process but not about completion or usefulness. Three quantities
> that would strengthen the section are not available: a time series of activity, tool
> invocations by functional category, and the artifacts produced by each session.
> Because the prompt corpus records what was requested and not what was executed,
> capability composition is reported as requested composition; executed composition is
> evidenced only by the single investigation traced end to end. Finally, workspace
> groups are labels rather than partitions, so group-level activity is always reported
> as absolute activity and never as a share of the platform.

---

## 8. Decisions only the authors can make

Ordered by how much they change the section.

**D1 — Sampling rule for the 186 requests.** Recover it or declare the corpus
purposive. *Recommendation:* declare purposive, and add one sentence on how the corpus
was assembled (even "sessions selected for coverage across contexts" is better than
silence). This costs nothing and removes the most attackable assumption.

**D2 — Double coding.** *Recommendation:* double-code 40 prompts and report Cohen's
κ. Two hours of work, and it converts the weakest methodological sentence in §5.4 into
a strength. Protocol in `CODING_GUIDE.md` §6 — start with the five largest combination
cells, where disagreement concentrates.

**D3 — Objective code glossary.** Supply the original codelist or adopt the inferred
glosses. *Recommendation:* adopt them and label them as reconstruction; the codes are
otherwise unreadable to a referee.

**D4 — The 10,863 figure.** *Recommendation:* delete. There is no version of the
manuscript in which keeping it is worth the risk.

**D5 — Verified accounts.** Obtain the definition of "verified" or drop the number.
*Recommendation:* drop it from the main text; keep 286 registered and 237 active, which
are internally consistent.

**D6 — Title of 5.5.** "GEI in Real-World Settings" vs "Illustrative Uses". Given that
only one chain is complete, *Illustrative Uses* is more defensible; *Real-World
Settings* invites the question "how many?". *Recommendation:* keep "Real-World" only if
the subsection opens with the E1/E3 distinction in the first paragraph.

**D7 — Where the Ipiranga case belongs.** It is currently referenced by Sections 4.3
and 4.4. *Recommendation:* keep it there and *also* open §5.5 with a short pointer, so
that §5 does not read as if it has no complete example. Do not duplicate the content.

**D8 — Do you want a time series badly enough to extract one?** A weekly message/session
series plus tool-call counts is one extraction from the same log. *Recommendation:* if
it can be produced before submission, it upgrades §5.2 from cross-sectional to
longitudinal and gives the section a growth figure. If not, leave §5.2 as is — it is
honest and complete for what it claims.

---

## 9. Tomorrow, in order

| # | Task | Time | Why first |
| --- | --- | --- | --- |
| 1 | Read `CONSISTENCY_AUDIT.md` and decide D1–D5 | 30 min | every sentence downstream depends on these |
| 2 | Pick the three main figures and confirm captions | 20 min | fixes the visual argument before prose |
| 3 | Write 5.4 (the core) | 90 min | hardest, highest value |
| 4 | Write 5.3 | 45 min | shorter than it looks; the context table does the work |
| 5 | Write 5.1 and 5.2 | 45 min | mostly numbers already tabulated |
| 6 | Write 5.5 | 60 min | needs care with evidence levels |
| 7 | Insert the limitations paragraph and re-read against §4 | 30 min | prevents §5 from over-claiming what §4 promised |
| 8 | Only if time: double coding (D2) | 120 min | converts a weakness into a result |

Do not start with 5.1. It is the easiest to write and the least consequential, and
starting there is how a day gets spent on counts.

---

## 10. Where everything is

| Need | File |
| --- | --- |
| Full methods text, pasteable | `section_05_deployment_and_use/methodology/SECTION5_METHODS.md` |
| What is wrong and what to do about it | `section_05_deployment_and_use/methodology/CONSISTENCY_AUDIT.md` |
| Machine verification of every number | `section_05_deployment_and_use/methodology/VERIFICATION_REPORT.md` |
| Codebook and validation protocol | `section_05_deployment_and_use/03_epidemiological_requests/CODING_GUIDE.md` |
| Example inventory with evidence levels | `section_05_deployment_and_use/05_real_world_settings/EXAMPLE_INVENTORY.csv` |
| Claim → evidence map | `SECTION_5_EVIDENCE_MATRIX.csv` |
| Figures | `section_05_deployment_and_use/figures/` |
| Tables | `section_05_deployment_and_use/tables/` |
| Rebuild everything | `python section_05_deployment_and_use/scripts/reproduce_section5.py` |
