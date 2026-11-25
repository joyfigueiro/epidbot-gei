# 03. Orchestration and adaptive execution

This document expands Section 4.3. It describes the execution loop, the dispatch of
typed operations, and the specific ways in which the system adapts when a step fails.

## The loop

Execution is a loop of four steps: plan, dispatch, observe, decide. Each iteration
consumes the result of one or more operations and produces one of three outcomes: a final
answer, a revised plan, or a question to the user. The loop is bounded, so a system that
cannot reach an answer stops and says so rather than continuing to search.

## Typed dispatch

The dispatcher sits between the model and the operation. It validates arguments against
the schema, refuses calls whose preconditions fail, and normalises whatever comes back
into a small set of error classes. That normalisation is what makes adaptation possible:
the system reacts to five classes rather than to an open-ended space of error messages.

## Adaptation strategies

| Observed class | Strategy | Example |
| --- | --- | --- |
| Empty result | Widen the scope, or move to a neighbouring source that covers the period | A municipal series with no records for the requested year is re-requested at state level to confirm the gap is real |
| Timeout | Reduce scope, split spatially, or switch to a lighter method | A national query is executed state by state |
| Schema mismatch | Re-read the descriptor and recast the argument | A date column stored as an integer is cast before aggregation |
| Implausible value | Recheck units and recompute from the raw table | An incidence rate per hundred thousand is verified against counts and population |
| Capability absent | Degrade to a descriptive answer and say what is missing | A question about a disease with no registered source returns a statement of the gap |

## Budgets and stopping rules

Three rules bound the loop. A maximum number of iterations, a wall-clock limit, and a
requirement that any final answer cite at least one operation result. The third rule is
the one that matters for trust: it converts an unsupported assertion into a visible gap.

## Parallel and sequential work

Operations that are independent are dispatched together, which reduces the wall-clock
cost of multi-source questions. Operations that depend on a previous result are
sequenced. The distinction is declared in the plan rather than discovered during
execution.

## Why this is not a fixed pipeline

A pipeline encodes the analysis in advance, which is exactly what generalized epidemic
intelligence is meant to avoid. Here the analysis is chosen at run time. The price of
that choice is variability: the same question can take different paths on different days.
The remedy is not to remove the variability but to record the path, which is the subject
of `04_traceability.md`.
