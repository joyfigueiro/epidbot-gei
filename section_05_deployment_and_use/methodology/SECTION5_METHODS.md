# Section 5 — methods

This document specifies how every number in Section 5 was produced. It is written
so that a referee can reconstruct the analysis from the repository alone, and so
that the authors can lift the relevant passages into the manuscript Methods.

Nothing here depends on the EpidBot source code. Everything depends on two
archived artefacts: the aggregate platform extracts in `data/` and the coded
prompt corpus in `data/audit/EXPORT_prompts_anonymised.csv`.

---

## 1. Design

Section 5 is an **observational study of a deployed system**. There is no
intervention, no control condition and no randomisation. What is measured is what
users asked and how much activity the platform carried, over a fixed calendar
window.

The study answers four descriptive questions and one compositional question:

| Subsection | Question | Unit of analysis |
| --- | --- | --- |
| 5.1 | Who used the platform, and in which contexts? | account, workspace group |
| 5.2 | How was it used, and how concentrated was that use? | session, message, weekday |
| 5.3 | What did users try to accomplish? | coded prompt |
| 5.4 | How were GEI capabilities combined in real requests? | coded prompt |
| 5.5 | What does a traced instance of use look like? | investigation |

Because the design is descriptive, no causal language is warranted anywhere in
Section 5. Adoption growth, for instance, cannot be separated from capability
release: the platform was under active development throughout the window, so a
rise in activity is a joint effect of both.

---

## 2. Observation window and snapshots

The reference window is **28 March 2026 to 10 November 2026** (227 days).

The session log was extracted four times (`data/usage_snapshots.csv`):

| Snapshot | Date | Sessions | Messages | Active accounts | Questions |
| --- | --- | --- | --- | --- | --- |
| S1 | 2026-10-27 | 648 | 6,688 | 233 | 968 |
| S2 | 2026-10-28 | 648 | 6,688 | 233 | 968 |
| S3 | 2026-11-10 18:51 | 667 | 6,961 | 237 | 994 |
| S4 | 2026-11-10 23:55 | 667 | 6,967 | 237 | 995 |

**S4 is the reference extraction for all Section 5 numbers.** The four
extractions are *four views of one accumulating database*, not four independent
samples. They must never be pooled, summed or treated as replicates. S1 and S2
are identical because the window closed the previous day; S3 and S4 differ by six
messages, the expected effect of a late write within the same window.

Growth between S1 and S4 is +19 sessions, +279 messages, +4 active accounts and
+27 questions over 14 days. This is reported as a single delta, not as a trend:
two points in time cannot support a trend.

**Consequence for the manuscript.** Any sentence of the form "use grew steadily
over the study period" is unsupported. The archived evidence supports only
"activity was higher at the end of the window than at the first extraction".

---

## 3. Definitions of the counting units

The manuscript must use these terms consistently, because the raw vocabulary of
the session log is ambiguous and three different quantities were previously
reported under one number.

| Term | Definition used here | Source |
| --- | --- | --- |
| Registered account | Account created in the platform | dashboard payload (S4) |
| Verified account | Account whose address was verified | dashboard payload (S4) |
| Active account | Account with at least one turn in the window | `S0_totals.csv` |
| Session | Conversation with at least one turn in the window | `S0_totals.csv` |
| Message (turn) | One user *or* assistant message | `S0_totals.csv` |
| User question | User turn classified as a question or task request | `S0_totals.csv` |
| Coded prompt | User request selected for the qualitative corpus and given capability and objective codes | `EXPORT_prompts_anonymised.csv` |
| Tool call | One invocation of an analytical tool by the system | **not archived** (see §7) |
| Artifact | Plot, report, dataset or dashboard produced by a session | **not archived** (see §7) |

Two ratios follow directly and appear in Table 5.11: 10.45 messages per session
and 29.4 messages per active account. Neither is a measure of effort or quality.

Note that *messages* counts assistant turns as well as user turns. A high
messages-per-question ratio reflects conversational depth, not user verbosity.

---

## 4. The coded prompt corpus

### 4.1 Size and composition

The corpus contains **186 individually coded user requests**, drawn from the same
window. Each row records: a pseudonymous prompt identifier, the user context, the
GEI capability codes present, the analytical objective, whether the request
depends on previous conversational context, how many distinct data sources it
names, whether it requires more than one domain, and the resulting capability
count.

Context composition: internal core team 43, external government 45, external
academic 41, external walk-in 38, external international 19.

### 4.2 Sampling

**The sampling procedure is not documented in the repository and could not be
recovered.** The corpus is therefore treated as a *purposive sample of requests*,
not as a probability sample of the 995 questions in the window. Two consequences
follow, and both must appear in the manuscript:

1. No count in Sections 5.3 and 5.4 may be reported as "of all user requests". The
   correct phrasing is "of the 186 coded requests".
2. No inferential test (confidence interval, chi-square, test of trend) is
   appropriate, because the selection mechanism is unknown.

The authors must supply the selection rule before submission. Until then, every
prompt-level percentage is a description of the corpus, nothing more.

### 4.3 Coding scheme

Seven capability codes and ten objective codes are defined in
[`../03_epidemiological_requests/CODING_GUIDE.md`](../03_epidemiological_requests/CODING_GUIDE.md).
The GEI codes map one-to-one onto the five functional areas defined in Section 3
of the manuscript:

| Code | Section 3 area |
| --- | --- |
| `I` | Integration of heterogeneous data sources |
| `K` | Access to scientific knowledge |
| `A` | Epidemiological analysis |
| `M` | Mathematical modelling |
| `V` | Visualization and reporting |

Two further codes mark requests outside the GEI frame: `S` (platform-meta request)
and `X` (out of scope).

### 4.4 Who coded, and how

This is a **single-coder, LLM-assisted classification** with no independent second
coding and therefore **no inter-rater reliability statistic**. The manuscript must
say so explicitly. It must not describe the procedure as manual human coding, and
it must not imply agreement between coders that was never measured.

The appropriate remedies, in order of cost, are: (i) state the limitation and
report the coding guide alongside the corpus, which is what this repository now
does; (ii) have a second coder re-code a random subsample of 40 prompts and report
Cohen's kappa; (iii) full double coding. Option (ii) is achievable before
submission and would materially strengthen §5.4.

### 4.5 Eligibility rule for the capability analysis

This rule determines the denominator 141 that appears throughout §5.4, and it was
applied in the earlier analysis but documented nowhere. A coded prompt is
**GEI-eligible** when it is *neither*:

- labelled `objective == "OOS"` (out of scope), **nor**
- labelled `caps == "S"` (platform-meta request with no epidemiological content).

Resulting funnel:

| Stage | Prompts |
| --- | --- |
| Coded prompts | 186 |
| Platform-meta only | 36 |
| Out of scope | 9 |
| **GEI-eligible** | **141** |

The 141 reproduce every published marginal exactly (verified in
[`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md)).

Two subtleties must be stated, because otherwise the denominator looks arbitrary:

1. **Three prompts carry GEI capability codes and are labelled out of scope.** They
   are excluded by objective, not by absence of capability. A request can mention a
   dataset while asking for something the system should refuse.
2. **The `X` flag and the `OOS` objective are not coextensive.** Six prompts carry
   `X`; nine carry `OOS`. The three in the difference are the ones in point 1. The
   manuscript should use the objective, not the flag, and should not report both.

### 4.6 Two denominators, one label

The earlier analysis computed "percentage requesting two or more capabilities" twice,
against two different bases:

- **41.8 %** = 59 / 141, over the eligible prompts.
- **27.9 % to 37.8 %** = e.g. 17 / 45, over *all* prompts observed in a context.

Both are legitimate; reporting them under the same label is not. Section 5.4 uses
**the eligible base (141)** everywhere, and Table 5.6 reports within-context
percentages explicitly as "of the eligible prompts in that context", with the
per-context `n` shown. The all-prompt version is retained in
`context_profile.csv` (columns suffixed `_of_all`) for transparency but should not
be quoted.

The same trap applies to the mean. The two means differ materially — for external
government, 1.42 over all prompts versus 1.68 over eligible ones. The headline
"mean 1.61 capabilities per prompt" is the eligible-base mean.

---

## 5. Statistics reported

All statistics are descriptive. Specifically:

- **Capability prevalence** = prompts containing the code / 141.
- **Composition depth** = distribution of the number of distinct GEI codes per
  prompt; mean = 227 code occurrences / 141 prompts = 1.61.
- **Co-occurrence** = symmetric matrix of prompt counts for each capability pair;
  the diagonal reproduces the marginals.
- **Context profile** = prevalence within each context, over its eligible prompts.
- **Friction categories** = prompts exhibiting each category, out of 186; a prompt
  may exhibit more than one.

No confidence intervals are reported for prompt-level proportions, because the
sample is purposive (§4.2). Where a proportion is quoted, its numerator and
denominator are quoted with it.

---

## 6. Measures of platform activity

- **Weekday rhythm**: messages per weekday over the window. This is the only
  additive table in the repository: the seven rows sum to 6,967, and
  `reproduce_section5.py` asserts this.
- **Workspace-group activity**: messages and sessions per pseudonymous group
  code. Groups are *workspace labels, not partitions*: one account may belong to
  several groups, and the two internal groups share accounts by construction. The
  group rows sum to 10,937 against an all-user total of 6,967, an inflation of
  57 %. Group shares are therefore reported as absolute activity, never as a share
  of the platform.
- **Concentration**: the ten most active accounts produced 39.9 % of all messages
  in both the 2026-10-27 and the 2026-11-10 extraction, while representing 4.3 %
  and 4.2 % of active accounts respectively. Only this aggregate share is
  reproduced; account labels are not carried into the repository.

---

## 7. What this study did not measure

These are not oversights to be papered over; they are the boundary of the
evidence, and the manuscript must respect it.

| Not measured | Why | Consequence |
| --- | --- | --- |
| Tool calls per functional category | No tool-call extract exists in the repository | The "10,863 tool calls across 36 categories" figure is unsupported and must be removed (§8) |
| Growth over time | Only four cumulative snapshots and a weekday rhythm | No trend statement is possible |
| Geographic or institutional distribution | Withheld by design at pseudonymisation | §5.1 cannot report geography |
| Artifacts produced (plots, reports, datasets) | Not archived | Requests cannot be matched to deliverables |
| Completion or success of a session | Log records turns, not outcomes | §5 makes process claims only |
| Accuracy of the answers | No benchmark, no reference answers | Evaluation is future work, stated in `docs/en/06_ethics_and_limitations.md` |
| Inter-rater reliability | Single coding pass | §4.4 applies |

---

## 8. The 10,863 figure

An earlier draft reported **10,863** twice, once as "consultations" (§5.2) and once
as "tool calls across 36 functional categories". The number is **not reproducible
from any table in this repository**, and it cannot be both quantities.

The nearest archived value is **10,937**, the sum of the workspace-group message
rows. That is *not* a platform total: the same data dictionary that supplies it
forbids treating it as one, because groups overlap. The difference between 10,863
and 10,937 (74) does not correspond to any archived quantity either.

**Recommendation:** remove 10,863 from the manuscript. Use 6,967 messages (S4) as
the platform total, and if a group-level statement is wanted, report absolute group
activity with the non-additivity caveat.

---

## 9. Ethics and data protection

The analysis uses administrative data from a tool in operation. Aggregation
happened at the extraction boundary, so no identifier, address, session id, message
text or network metadata left the production environment. Workspace groups were
replaced by codes assigned in random order under a fixed seed. Active accounts are
binned, and per-account rates are withheld below six accounts, so that no published
cell describes one or two identifiable people.

Two residual risks must be acknowledged in the manuscript:

1. **Small-group inference.** A context stratum with 17 to 19 eligible prompts
   (`External - international`) may correspond to a small number of institutions.
   Percentages in Table 5.6 for that stratum are the most re-identification-prone
   cell in Section 5.
2. **Verbatim prompts.** The coded corpus stores codes, not text, which is what
   makes it publishable. Any verbatim request quoted in the manuscript must be
   checked individually: some requests in the sample are personal medical queries
   and are not quotable in any form.

The corpus contains out-of-scope requests by design, because demonstrating that
scope boundaries are tested is one of the empirical points of §5.5. Quoting one
requires paraphrase, not redaction.

---

## 10. Reproduction

```bash
python section_05_deployment_and_use/scripts/reproduce_section5.py
python section_05_deployment_and_use/scripts/make_section5_figures.py
```

The first script rebuilds 17 derived tables, 12 LaTeX tables and
[`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md); it exits non-zero if any
recomputation disagrees with an archived aggregate. The second redraws the six
figures at 300 dpi and as vector PDF, reading only the tables the first script
wrote.
