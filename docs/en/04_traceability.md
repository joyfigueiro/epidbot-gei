# 04. Traceability and reproducibility

This document expands Section 4.4. It describes what is recorded during an investigation,
what that record makes possible, and where the limits of reproducibility lie.

## Three records

| Record | Content | Purpose |
| --- | --- | --- |
| Session log | Every turn, every operation call, its arguments and a summary of its result | Reconstructs what the user asked and what the system did |
| Provenance record | Datasets used with version and extraction date, operations in order, parameters, warnings | Makes each number attributable |
| Artifacts | Figures, tables and reports with creation time and content hash | Allows a reader to check that the file they have is the file that was produced |

## What makes a run reproducible

Non-determinism is unavoidable when a language model chooses the path. What is made
reproducible is the analytical path, not the wording. The ordered sequence of operations,
their arguments and the data versions are sufficient to recompute the numbers, even if a
re-run would phrase the narrative differently. Reproducibility is therefore a property of
the record, not of the model.

## Minimum provenance for a number

Every number in a generated report must trace to one operation, one dataset version and
one argument set. The report builder accepts only values returned by an operation or
computed by the script that assembled the table. A number written from model memory is not
admitted into a report. This rule is enforced at assembly, not requested in the prompt.

## Where reproducibility stops

Three limits should be stated explicitly in any use of the system.

- A re-run may take a different but equally valid path, so the operation sequence is not
  guaranteed to be identical.
- Upstream data are revised. A re-run months later may legitimately produce different
  numbers for the same request, and the provenance record will show why.
- The record documents what was done, not whether it was the right thing to do. Judging
  appropriateness remains a human task, which is why the review step exists as a separate
  stage rather than as part of the answer.
