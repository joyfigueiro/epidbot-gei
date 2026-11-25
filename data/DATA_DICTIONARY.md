# Data dictionary

## Provenance

All tables in this folder derive from the EpidBot session log, a table that records
every conversational turn together with the account, the workspace group, the
timestamp and the tool calls issued in that turn. The log exists for operational and
administrative purposes. It is not a research registry and it was not designed for
this analysis.

The extraction was performed four times (see `usage_snapshots.csv`). Each extraction
applied the same procedure:

1. Restrict to turns between `period_start` and `period_end`.
2. Count sessions, messages, distinct active accounts and user questions.
3. Aggregate by workspace group and by weekday.
4. Discard account identifiers, session identifiers, message text and network
   metadata before the aggregate leaves the production environment.

The four snapshots are kept because the platform was live during the writing of the
manuscript. Differences between S1 and S4 are growth, not extraction error.

## `usage_snapshots.csv`

| Column | Type | Meaning |
| --- | --- | --- |
| `snapshot_id` | text | Extraction label, S1 to S4 in chronological order |
| `snapshot_date` | date | Date on which the extraction ran |
| `total_sessions` | integer | Distinct sessions with at least one turn in the window |
| `total_messages` | integer | All turns, user and assistant, in the window |
| `active_users` | integer | Distinct accounts with at least one turn in the window |
| `user_questions` | integer | User turns classified as a question or a task request |
| `period_start` | date | First day of the window |
| `period_end` | date | Last day of the window |

S1 and S2 share a window and differ only by extraction date; they are identical
because no turn arrived between them. S3 and S4 also share a date and differ by six
messages, which is the expected effect of a late write.

## `usage_by_group.csv`

Same indicators, one row per working group, taken from snapshot S4. Group labels are
replaced by pseudonymous codes, so the file can be distributed.

| Column | Type | Meaning |
| --- | --- | --- |
| `group_id` | text | Pseudonymous code, G01 to G12, assigned in random order |
| `segment` | text | Coarse user context: internal development, internal testing, external academic, external government, external international, external open |
| `users_band` | text | Active accounts in bands: 1-2, 3-5, 6-10, 11-20, more than 20 |
| `active_users` | integer | Distinct accounts in the group, present only when the group has six or more accounts |
| `sessions`, `messages`, `user_questions` | integer | As above |
| `messages_per_session` | decimal | Messages divided by sessions, reported for every group |
| `messages_per_user` | decimal | Messages divided by active accounts, withheld below six accounts |
| `period_start`, `period_end` | date | First and last observed turn in that group |
| `disclosure_note` | text | Reason a value was withheld, empty when nothing was withheld |

Codes were assigned in random order under a fixed seed, so neither the code nor the row
order carries information about group size, scope or chronology. The mapping between
codes and labels is held in an internal key that is not part of this repository. Rates
per account are withheld for groups with fewer than six accounts, because a rate over
one or two accounts describes those accounts individually.

**The rows are not additive.** Groups are workspace labels, not partitions: an
account can belong to several groups, and the two internal groups (`G05` and
`G09`) share accounts by construction. The sum of the group rows is
larger than the all-user total and this is expected. Per-group counts are therefore
descriptive of each group and are never used to build an all-user total.

## `messages_by_weekday.csv`

| Column | Type | Meaning |
| --- | --- | --- |
| `weekday` | text | Monday to Sunday |
| `messages` | integer | All turns on that weekday, snapshot S4 |

This table is additive: the seven rows sum to `total_messages` in S4. The script in
`analysis/` checks this invariant.

## `question_taxonomy.csv`

| Column | Type | Meaning |
| --- | --- | --- |
| `category_id` | text | C1 to C8 |
| `category_en`, `category_pt` | text | Category label in both languages |
| `evidence` | text | Qualitative weight in the sample: dominant, secondary or marginal |
| `example_query_en`, `example_query_pt` | text | Paraphrased representative request |

The taxonomy is qualitative. It was built by reading the sampled user questions and
grouping them by intent. No per-category counts are reported, because the sample of
questions is not a random sample of all turns and a count would suggest a precision
the data do not support. The `evidence` column records only whether a category
recurs often, occurs, or appears occasionally.

## Known caveats

- `total_messages` counts assistant turns as well as user turns. Ratios of messages
  to questions therefore reflect conversational depth, not user effort.
- `user_questions` depends on a classifier over user turns; it is a lower bound,
  because imperative requests are sometimes not phrased as questions.
- Group windows differ (a group that was active only in June has a June window).
  Cross-group comparison of rates should use `messages / active_users / days in the
  group window`, not raw totals.
- The platform was under active development during the observation window, so the
  availability of tools changed over time. Usage growth is therefore a joint effect
  of adoption and capability release, and cannot be read as adoption alone.
