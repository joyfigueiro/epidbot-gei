#!/usr/bin/env python3
"""Pseudonymise the group-level tables of the GEI usage audit.

Reads the internal group table (labels included) and a key file mapping each
label to a pseudonymous code, then writes the files that can be distributed.
The key is passed as an argument and is never copied into the output folder.

Usage
    python pseudonymise.py --groups groups_latest.csv --key key.csv --out ../data

The script exits with an error if any group label survives into an output file.
"""

import argparse
import json
import pathlib
import sys

import pandas as pd

SEGMENTS = {
    "internal": "internal_dev",
    "internal_test": "internal_test",
    "external_acad": "external_academic",
    "external_gov": "external_government",
    "external_intl": "external_international",
    "external_walk": "external_open",
}

MIN_ACCOUNTS_FOR_RATE = 6


def account_band(n):
    """Return the disclosure band for a group with n accounts."""
    if n <= 2:
        return "1-2"
    if n <= 5:
        return "3-5"
    if n <= 10:
        return "6-10"
    if n <= 20:
        return "11-20"
    return ">20"


def build_table(groups, mapping):
    """Build the pseudonymised group table from the internal group table."""
    rows = []
    for _, r in groups.iterrows():
        n = int(r["users"])
        rows.append({
            "group_id": mapping[r["group"]],
            "segment": SEGMENTS[r["scope"]],
            "users_band": account_band(n),
            "users_exact": n if n >= MIN_ACCOUNTS_FOR_RATE else None,
            "sessions": int(r["sessions"]),
            "messages": int(r["messages"]),
            "questions": int(r["questions"]),
            "messages_per_session": round(r["messages"] / r["sessions"], 2),
            "messages_per_user": (round(r["msg_per_user"], 1)
                                  if n >= MIN_ACCOUNTS_FOR_RATE else None),
        })
    return pd.DataFrame(rows).sort_values("group_id").reset_index(drop=True)


def assert_no_labels(out_dir, labels):
    """Fail if any group label appears in a distributed file."""
    leaks = []
    for path in pathlib.Path(out_dir).rglob("*"):
        if path.suffix.lower() not in {".csv", ".json", ".md", ".tex", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        leaks += [(str(path), lb) for lb in labels if lb.lower() in text]
    if leaks:
        sys.exit("group labels survived pseudonymisation: %s" % leaks)


def main():
    """Entry point."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", required=True, help="internal group table (CSV)")
    ap.add_argument("--key", required=True, help="label to code mapping (CSV)")
    ap.add_argument("--payload", help="dashboard payload JSON, if present")
    ap.add_argument("--out", default="data")
    a = ap.parse_args()

    groups = pd.read_csv(a.groups)
    key = pd.read_csv(a.key)
    mapping = dict(zip(key["group_internal"], key["group_id"]))

    table = build_table(groups, mapping)
    table.to_csv(pathlib.Path(a.out) / "S1_group_characteristics.csv",
                 index=False, na_rep="s")

    if a.payload:
        pay = json.loads(pathlib.Path(a.payload).read_text(encoding="utf-8"))
        pay["group_sessions"]["columns"] = ["group_id", "sessions"]
        pay["group_sessions"]["rows"] = [
            [mapping[name], n] for name, n in pay["group_sessions"]["rows"]]
        (pathlib.Path(a.out) / "dashboard_payload_pseudonymised.json").write_text(
            json.dumps(pay, indent=1, ensure_ascii=False), encoding="utf-8")

    assert_no_labels(a.out, list(key["group_internal"]))
    print("ok: %d groups written" % len(table))


if __name__ == "__main__":
    main()
