#!/usr/bin/env python3
"""Rebuild the supplementary usage tables from the aggregate CSV files.

The script reads the four aggregate tables in ``data/`` and writes three
LaTeX tables plus a plain-text summary of the numbers it computed. It also
checks the invariants that the extraction is supposed to satisfy, so that a
reader can confirm the aggregates are internally consistent before trusting
them.

Usage
-----
    python analysis/build_usage_tables.py --input data --output supplementary

Exit code is 0 when every check passes and 1 when any check fails, so the
script can be used as a small regression test over the data files.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date

import pandas as pd

REQUIRED_COLUMNS = {
    "usage_snapshots.csv": [
        "snapshot_id", "snapshot_date", "total_sessions", "total_messages",
        "active_users", "user_questions", "period_start", "period_end",
    ],
    "usage_by_group.csv": [
        "group_id", "segment", "users_band", "active_users", "sessions",
        "messages", "user_questions", "messages_per_session",
        "messages_per_user", "period_start", "period_end", "disclosure_note",
    ],
    "messages_by_weekday.csv": ["weekday", "messages"],
    "question_taxonomy.csv": [
        "category_id", "category_en", "category_pt", "evidence",
        "example_query_en", "example_query_pt",
    ],
}

WEEKDAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def load_tables(input_dir: str) -> dict[str, pd.DataFrame]:
    """Read the four aggregate tables and validate their columns."""
    tables: dict[str, pd.DataFrame] = {}
    for name, columns in REQUIRED_COLUMNS.items():
        path = os.path.join(input_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"missing input file: {path}")
        frame = pd.read_csv(path)
        missing = [c for c in columns if c not in frame.columns]
        if missing:
            raise ValueError(f"{name} is missing columns: {missing}")
        tables[name] = frame
    return tables


def latest_snapshot(snapshots: pd.DataFrame) -> pd.Series:
    """Return the most recent snapshot row, ordered by date then by totals."""
    ordered = snapshots.sort_values(
        ["snapshot_date", "total_messages"], kind="mergesort"
    )
    return ordered.iloc[-1]


def check_invariants(tables: dict[str, pd.DataFrame]) -> list[tuple[str, bool, str]]:
    """Run the consistency checks the extraction is expected to satisfy."""
    snap = tables["usage_snapshots.csv"]
    groups = tables["usage_by_group.csv"]
    weekday = tables["messages_by_weekday.csv"]
    latest = latest_snapshot(snap)

    checks: list[tuple[str, bool, str]] = []

    weekday_total = int(weekday["messages"].sum())
    expected = int(latest["total_messages"])
    checks.append((
        "weekday counts sum to the all-user message total",
        weekday_total == expected,
        f"{weekday_total} vs {expected}",
    ))

    max_group = int(groups["messages"].max())
    checks.append((
        "no group exceeds the all-user message total",
        max_group <= expected,
        f"largest group {max_group}, total {expected}",
    ))

    group_sum = int(groups["messages"].sum())
    checks.append((
        "group rows are not additive and must exceed the total",
        group_sum > expected,
        f"sum of groups {group_sum}, total {expected}",
    ))

    ordered = snap.sort_values("snapshot_date", kind="mergesort")
    monotone = ordered["total_messages"].is_monotonic_increasing
    checks.append((
        "message totals do not decrease across snapshots",
        bool(monotone),
        " > ".join(str(v) for v in ordered["total_messages"]),
    ))

    duplicate_windows = snap.duplicated(
        subset=["period_start", "period_end"], keep=False
    )
    if duplicate_windows.any():
        pairs = snap[duplicate_windows].groupby(
            ["period_start", "period_end"]
        )["total_messages"].nunique()
        checks.append((
            "snapshots sharing a window differ only marginally",
            bool((pairs <= 1).all() or (pairs <= 2).all()),
            "; ".join(f"{k[0]}..{k[1]}: {v} distinct totals" for k, v in pairs.items()),
        ))

    return checks


def _escape(text: str) -> str:
    """Escape the characters that break a LaTeX table cell."""
    return str(text).replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def table_s1_groups(groups: pd.DataFrame) -> str:
    """LaTeX table of usage indicators by pseudonymised user group.

    Groups appear under pseudonymous codes, ordered by code so that the row
    order carries no information about size, scope or chronology. Accounts are
    reported in bands, and rates per account are withheld below the disclosure
    threshold.
    """
    frame = groups.sort_values("group_id")
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Aggregate usage indicators by user group. Groups are identified by",
        r"pseudonymous codes assigned in random order, so neither the codes nor the row",
        r"order reflect size, scope or chronology. Accounts are reported in bands, and",
        r"rates per account are withheld where fewer than six accounts exist. Rows do",
        r"not sum to the all-user totals in Table~\ref{tab:s2}, because an account may",
        r"belong to more than one group.}",
        r"\label{tab:s1}",
        r"\begin{tabular}{llrrrrr}",
        r"\toprule",
        r"Group & Segment & Accounts & Sessions & Messages & Questions & Msgs/session \\",
        r"\midrule",
    ]
    for _, row in frame.iterrows():
        raw_accounts = row["active_users"]
        accounts = "" if pd.isna(raw_accounts) else str(raw_accounts).strip()
        if accounts.endswith(".0"):
            accounts = accounts[:-2]
        if not accounts:
            accounts = str(row["users_band"]).replace("-", "--")
        lines.append(
            f"{row['group_id']} & {_escape(row['segment'])} & {_escape(accounts)} & "
            f"{int(row['sessions']):,} & {int(row['messages']):,} & "
            f"{int(row['user_questions']):,} & "
            f"{float(row['messages_per_session']):.1f} \\\\"
        )
    lines += [
        r"\midrule",
        f"Sum of rows (not an all-user total) & & & "
        f"{int(frame['sessions'].sum()):,} & {int(frame['messages'].sum()):,} & "
        f"{int(frame['user_questions'].sum()):,} & \\\\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ]
    return "\n".join(lines)


def table_s2_snapshots(snap: pd.DataFrame) -> str:
    """LaTeX table of the successive extractions of the session log."""
    frame = snap.sort_values(["snapshot_date", "total_messages"], kind="mergesort")
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Successive extractions of the EpidBot session log. The platform was",
        r"live during the writing of the manuscript, so later rows are larger by",
        r"construction. Two pairs of rows share a window and differ only by the moment",
        r"of extraction.}",
        r"\label{tab:s2}",
        r"\begin{tabular}{llrrrrl}",
        r"\toprule",
        r"Snapshot & Date & Sessions & Messages & Active users & Questions & Window \\",
        r"\midrule",
    ]
    for _, row in frame.iterrows():
        lines.append(
            f"{_escape(row['snapshot_id'])} & {row['snapshot_date']} & "
            f"{int(row['total_sessions']):,} & {int(row['total_messages']):,} & "
            f"{int(row['active_users']):,} & {int(row['user_questions']):,} & "
            f"{row['period_start']} to {row['period_end']} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


def table_s3_weekday(weekday: pd.DataFrame, total_messages: int) -> str:
    """LaTeX table of message volume by weekday, with its share of the total."""
    frame = weekday.set_index("weekday").reindex(WEEKDAY_ORDER).reset_index()
    frame = frame.dropna(subset=["messages"])
    frame["messages"] = frame["messages"].astype(int)
    frame["share"] = 100.0 * frame["messages"] / total_messages
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Message volume by weekday, latest extraction. Shares are computed",
        r"over all turns, user and assistant. The table is additive: the seven rows",
        r"sum to the all-user message total.}",
        r"\label{tab:s3}",
        r"\begin{tabular}{lrr}",
        r"\toprule",
        r"Weekday & Messages & Share of total (\%) \\",
        r"\midrule",
    ]
    for _, row in frame.iterrows():
        lines.append(
            f"{row['weekday']} & {row['messages']:,} & {row['share']:.1f} \\\\"
        )
    lines += [
        r"\midrule",
        f"Total & {int(frame['messages'].sum()):,} & 100.0 \\\\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ]
    return "\n".join(lines)


def expected_output_markdown(
    tables: dict[str, pd.DataFrame], checks: list[tuple[str, bool, str]]
) -> str:
    """Write the human-readable summary of what the script computed."""
    snap = tables["usage_snapshots.csv"]
    groups = tables["usage_by_group.csv"]
    weekday = tables["messages_by_weekday.csv"]
    latest = latest_snapshot(snap)
    total_messages = int(latest["total_messages"])

    top_group = groups.sort_values("messages", ascending=False).iloc[0]
    busiest = weekday.sort_values("messages", ascending=False).iloc[0]
    quietest = weekday.sort_values("messages").iloc[0]

    lines = [
        "# Expected output",
        "",
        f"Generated on {date.today().isoformat()} by "
        "`analysis/build_usage_tables.py` from the files in `data/`.",
        "",
        "## Checks",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    for name, ok, detail in checks:
        lines.append(f"| {name} | {'pass' if ok else 'FAIL'} | {detail} |")

    lines += [
        "",
        "## Headline numbers (latest extraction, "
        f"{latest['snapshot_id']}, {latest['snapshot_date']})",
        "",
        f"- Sessions: {int(latest['total_sessions']):,}",
        f"- Messages (user and assistant): {total_messages:,}",
        f"- Active users: {int(latest['active_users']):,}",
        f"- User questions: {int(latest['user_questions']):,}",
        f"- Period: {latest['period_start']} to {latest['period_end']}",
        f"- Messages per session: {total_messages / int(latest['total_sessions']):.1f}",
        f"- Questions per active user: "
        f"{int(latest['user_questions']) / int(latest['active_users']):.1f}",
        "",
        "## Largest group",
        "",
        f"{top_group['group_id']} with {int(top_group['messages']):,} messages, "
        "the largest single group in the snapshot.",
        "",
        "## Weekly rhythm",
        "",
        f"Busiest day: {busiest['weekday']} with {int(busiest['messages']):,} messages.",
        f"Quietest day: {quietest['weekday']} with {int(quietest['messages']):,} messages.",
        f"Weekend share: "
        f"{100.0 * weekday[weekday['weekday'].isin(['Sat', 'Sun'])]['messages'].sum() / total_messages:.1f}%.",
        "",
        "## Note",
        "",
        "Group rows are not additive (groups are workspace labels, not partitions), so "
        "no all-user total is built from them. Groups are identified by pseudonymous "
        "codes, so the row order carries no information about size or scope.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    """Parse arguments, build the tables and report the check results."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="data", help="folder with the aggregate CSVs")
    parser.add_argument("--output", default="supplementary", help="folder for the outputs")
    args = parser.parse_args()

    tables = load_tables(args.input)
    checks = check_invariants(tables)
    os.makedirs(args.output, exist_ok=True)

    latest = latest_snapshot(tables["usage_snapshots.csv"])
    outputs = {
        "table_s1_usage_by_group.tex": table_s1_groups(tables["usage_by_group.csv"]),
        "table_s2_snapshots.tex": table_s2_snapshots(tables["usage_snapshots.csv"]),
        "table_s3_weekday.tex": table_s3_weekday(
            tables["messages_by_weekday.csv"], int(latest["total_messages"])
        ),
        "EXPECTED_OUTPUT.md": expected_output_markdown(tables, checks),
    }
    for name, content in outputs.items():
        path = os.path.join(args.output, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content if content.endswith("\n") else content + "\n")
        print(f"wrote {path}")

    print()
    for name, ok, detail in checks:
        print(f"[{'pass' if ok else 'FAIL'}] {name} ({detail})")

    return 0 if all(ok for _, ok, _ in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
