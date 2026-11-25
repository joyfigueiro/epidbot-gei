# Expected output

Generated on 2026-11-25 by `analysis/build_usage_tables.py` from the files in `data/`.

## Checks

| Check | Result | Detail |
| --- | --- | --- |
| weekday counts sum to the all-user message total | pass | 6967 vs 6967 |
| no group exceeds the all-user message total | pass | largest group 4471, total 6967 |
| group rows are not additive and must exceed the total | pass | sum of groups 10937, total 6967 |
| message totals do not decrease across snapshots | pass | 6688 > 6688 > 6961 > 6967 |
| snapshots sharing a window differ only marginally | pass | 2026-03-28..2026-10-27: 1 distinct totals; 2026-03-28..2026-11-10: 2 distinct totals |

## Headline numbers (latest extraction, S4, 2026-11-10)

- Sessions: 667
- Messages (user and assistant): 6,967
- Active users: 237
- User questions: 995
- Period: 2026-03-28 to 2026-11-10
- Messages per session: 10.4
- Questions per active user: 4.2

## Largest group

G09 with 4,471 messages, the largest single group in the snapshot.

## Weekly rhythm

Busiest day: Tue with 1,454 messages.
Quietest day: Sun with 410 messages.
Weekend share: 14.1%.

## Note

Group rows are not additive (groups are workspace labels, not partitions), so no all-user total is built from them. Groups are identified by pseudonymous codes, so the row order carries no information about size or scope.
