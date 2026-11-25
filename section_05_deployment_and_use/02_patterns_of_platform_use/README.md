# 5.2 Patterns of platform use

**Question.** How was the platform used, and how concentrated was that use?

**Short answer.** The weekly rhythm is a working-week pattern with a 14.1 % weekend
share; activity is heavily concentrated in a few accounts and in a few workspace
groups; and the conversational depth per session (10.45 messages) indicates
multi-turn work rather than single-shot queries.

## Evidence

| File | Content |
| --- | --- |
| `derived/weekday_rhythm.csv` | messages per weekday, the only additive table |
| `derived/concentration.csv` | top-ten share reproduced from the administrative reports |
| `../../data/messages_by_weekday.csv` | raw aggregate |
| Table `t5_12` | LaTeX |
| Figure `fig5_5(a)` | weekly rhythm |

## Verified numbers

| Weekday | Messages | Share |
| --- | --- | --- |
| Mon | 1,238 | 17.8 % |
| Tue | 1,454 | 20.9 % |
| Wed | 1,136 | 16.3 % |
| Thu | 1,146 | 16.5 % |
| Fri | 1,010 | 14.5 % |
| Sat | 573 | 8.2 % |
| Sun | 410 | 5.9 % |

Weekend share: **14.1 %**. The seven rows sum to 6,967 and the reproduction script
asserts it.

Concentration: top-ten accounts = 2,779 of 6,967 messages (**39.9 %**) at
2026-11-10, and 2,665 of 6,688 (**39.8 %**) at 2026-10-27. Ten accounts are 4.2 %
and 4.3 % of active accounts respectively.

## The one table that is additive

Weekday counts are additive because each message belongs to exactly one weekday.
**Workspace-group rows are not additive**: an account can belong to several groups,
and the two internal groups share accounts by construction. The group rows sum to
10,937 against a total of 6,967 — an inflation of 57 %. Never compute a group share
of platform activity.

## What may be claimed

- Use follows the working week; roughly one message in seven arrives at the weekend.
- A small number of accounts carries a large share of the conversation, and that
  share is stable across two extractions two weeks apart.
- Sessions are multi-turn (10.45 messages each), which is consistent with
  investigate-then-revise behaviour rather than one-shot querying. Treat this as
  consistent with, not as evidence of, iterative refinement.

## What may not be claimed

- **Temporal evolution.** This is the single largest hole in §5.2. There is no
  monthly or weekly activity series in the repository — only four cumulative
  snapshots and one weekday profile. No figure of "use over time" can be drawn
  honestly. See consistency audit §A9.
- **Tool usage by functional category.** No tool-call extract exists. The
  "10,863 tool calls across 36 categories" figure in the draft is unsupported and
  must be removed (§A1).
- **Artifacts produced.** Plots, reports and datasets are not archived against
  sessions, so a count of outputs cannot be reported.
- **Data sources actually accessed.** The corpus records sources *named in the
  request* (62 prompts name at least one), never sources invoked at execution.
- **Quality, efficiency or success.** Message volume is not effort, and turns are
  not outcomes.

## If a time series is wanted

It requires one new extraction, specified in the consistency audit: message and
session counts grouped by ISO week over the window, plus tool invocations grouped by
functional category, from the same session log that produced the existing
aggregates. Until that file exists, §5.2 stays a cross-sectional description.
