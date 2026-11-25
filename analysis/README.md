# Analysis code

One script, one job: turn the aggregate tables in `data/` into the LaTeX tables in
`supplementary/` and check that the aggregates are internally consistent.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build_usage_tables.py --input ../data --output ../supplementary
```

## What it does

| Function | Output |
| --- | --- |
| `load_tables` | Reads the four CSVs and fails loudly if a required column is missing |
| `check_invariants` | Runs the consistency checks listed below |
| `table_s1_groups` | `supplementary/table_s1_usage_by_group.tex` |
| `table_s2_snapshots` | `supplementary/table_s2_snapshots.tex` |
| `table_s3_weekday` | `supplementary/table_s3_weekday.tex` |
| `expected_output_markdown` | `supplementary/EXPECTED_OUTPUT.md` |

## Checks

1. Weekday counts sum to the all-user message total. This is the one table that must
   be additive.
2. No group exceeds the all-user message total.
3. The sum of the group rows exceeds the all-user total, which is the expected
   consequence of groups not being partitions.
4. Message totals do not decrease across snapshots.
5. Snapshots that share a window differ only marginally.

The script exits with status 1 if any check fails, so it can be used as a regression
test over the data files.

## Why there is no per-category count

`data/question_taxonomy.csv` is a qualitative classification. The sample of questions
it was built from is not a random sample of all turns, so a count per category would
imply a precision the data do not support. The table reports presence, not frequency.

## Style of the code

The script uses explicit type hints, a docstring on every function, and no global
state. It reads only from the folder passed in `--input` and writes only to the folder
passed in `--output`, so it can be run against a fork of the data without touching the
repository.

## Section 5 scripts

The Section 5 analysis has its own scripts, kept next to the evidence they produce:

| Script | Job |
| --- | --- |
| `section_05_deployment_and_use/scripts/reproduce_section5.py` | recompute every prompt-level statistic from `data/audit/EXPORT_prompts_anonymised.csv`, verify it against the archived marginals, and write 17 derived tables plus 12 LaTeX tables |
| `section_05_deployment_and_use/scripts/make_section5_figures.py` | draw the six Section 5 figures from those tables at 300 dpi PNG and vector PDF |

They follow the same conventions as `build_usage_tables.py`: type hints, a docstring on
every function, no global state, and an explicit `--input`/`--out` so they can be run
against a fork without touching the repository. `reproduce_section5.py` exits non-zero
if a recomputation disagrees with an archived marginal, which makes it usable as a
regression test.

```bash
python section_05_deployment_and_use/scripts/reproduce_section5.py
python section_05_deployment_and_use/scripts/make_section5_figures.py
```
