# 02. From request to analytical plan

This document expands Section 4.2. It describes the sequence through which a free-text
epidemiological request becomes an executable plan, and the points at which the system
stops to ask rather than guess.

## Stages

1. **Intent capture.** The request is stored verbatim. It remains the reference against
   which the final answer is checked, because a plan can drift from the question it was
   meant to answer.
2. **Scope resolution.** Five dimensions are extracted: disease or health event, place,
   time window, spatial and temporal granularity, and comparison baseline. Each dimension
   is explicit, inferred from the conversation, or absent. Absent is a distinct state and
   is not filled with a default.
3. **Catalogue lookup.** The planner searches registered datasets that satisfy the scope.
   It sees descriptors, not data. This step is what prevents the system from promising an
   analysis the substrate cannot support.
4. **Capability selection.** Operations are chosen from the registry according to the
   scope and the available data.
5. **Plan assembly.** Steps are arranged as a directed acyclic graph, with declared inputs
   and outputs, so that partial failures can be localised.
6. **Pre-execution check.** Coverage, units, granularity, expected runtime and, most
   importantly, whether the plan answers the question that was asked.
7. **Clarification.** When a missing dimension would materially change the answer, the
   system asks before running. When it would not, it states the assumption it adopted and
   proceeds.

## A worked example

The request *how did dengue behave in Campinas in 2024* resolves as follows. Disease is
dengue. Place is Campinas, which resolves to the IBGE municipality code 3509502. Time is
the 2024 epidemiological year. Granularity is weekly, because the question asks about
behaviour over time rather than an annual total. Outcome is notified cases. The baseline
for a control diagram is the preceding five years.

The plan then fetches the dengue line list for the municipality, aggregates by
epidemiological week, computes incidence against the municipal population, builds a
control diagram with the endemic channel, produces a figure and a table, and attaches the
provenance record. Each of those steps is a named operation. None of them is a paragraph
of instructions to a model.

## How ambiguity is handled

Ambiguity is resolved before execution when the cost of a wrong run is high, for example
a download that takes minutes. It is resolved after execution when the result itself
reveals the problem, for example an empty table or an incidence rate that is implausible
for the place and period. Both cases are recorded, so a reader can see which assumptions
were made and which were corrected.

## What the plan is not

The plan is not a script. It does not fix the sequence of calls in advance and it is not
reused verbatim across questions. It records the intended path, and the path may be
revised during execution, as described in `03_orchestration.md`.
