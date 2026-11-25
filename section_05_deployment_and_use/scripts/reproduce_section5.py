#!/usr/bin/env python3
"""Rebuild every Section 5 table from the auditable per-prompt corpus.

The Section 5 analysis rests on two kinds of input:

1. ``data/audit/EXPORT_prompts_anonymised.csv`` -- one row per individually coded
   user request (186 rows). This is the only granular record in the repository and
   therefore the source of truth for every prompt-level statistic.
2. The aggregate extracts in ``data/`` and ``data/audit/`` -- platform totals,
   workspace-group activity, weekday rhythm and previously published marginals.

This script recomputes the prompt-level tables from (1) using one explicit
eligibility rule, compares each result against the archived marginal in (2), and
writes the derived tables plus a verification report. Any disagreement between a
recomputation and an archived marginal is reported as FAIL rather than silently
resolved.

Eligibility rule
----------------
A coded prompt enters the GEI-eligible analysis set when it is *neither*:

* labelled ``objective == "OOS"`` (out of scope), *or*
* labelled ``caps == "S"`` (platform-meta request with no epidemiological content).

This yields 141 of 186 prompts and reproduces every published marginal exactly
(see VERIFICATION_REPORT.md). The rule is stated here because it was applied in
the earlier analysis but not documented anywhere in the repository, and because
three prompts carry GEI capability codes *and* ``objective == "OOS"``: they are
excluded by objective, not by absence of capabilities.

Usage
-----
    python reproduce_section5.py --repo-root ../..

Both ``--repo-root`` and ``--input`` default to the repository layout, so the
script runs unchanged from a fresh clone.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

GEI_CAPABILITIES: List[str] = ["I", "K", "A", "M", "V"]
ALL_CODES: List[str] = ["I", "K", "A", "M", "V", "S", "X"]

CAPABILITY_LABELS: Dict[str, str] = {
    "I": "Integration of heterogeneous data sources",
    "K": "Access to scientific knowledge",
    "A": "Epidemiological analysis",
    "M": "Mathematical modelling",
    "V": "Visualization and reporting",
    "S": "Platform-meta request (non-GEI)",
    "X": "Out of scope",
}

SHORT_LABELS: Dict[str, str] = {
    "I": "Data integration",
    "K": "Scientific knowledge",
    "A": "Epidemiological analysis",
    "M": "Mathematical modelling",
    "V": "Visualization & reporting",
    "S": "Platform meta",
    "X": "Out of scope",
}

#: Gloss for the objective codes. The code-to-label key is NOT part of the
#: repository; these glosses are inferred from the coded prompts and from
#: cross-tabulation with the capability codes, and must be confirmed by the
#: authors before publication.
OBJECTIVE_GLOSS_INFERRED: Dict[str, str] = {
    "RES": "Research and writing support",
    "META": "Platform-meta question",
    "DESC": "Descriptive epidemiology",
    "TRAN": "Data transformation / parameter rescaling",
    "SURV": "Surveillance monitoring",
    "OOS": "Out of scope",
    "RISK": "Risk assessment",
    "PLAN": "Analytical planning",
    "FORE": "Forecasting",
    "COMP": "Comparison across units",
}

CONTEXT_ORDER: List[str] = [
    "Internal (core team)",
    "External - government",
    "External - academic",
    "External - international",
    "External - walk-in",
]


# --------------------------------------------------------------------------- #
# Loading and preparation
# --------------------------------------------------------------------------- #

def load_prompts(input_dir: Path) -> pd.DataFrame:
    """Load the coded prompt corpus and derive the eligibility flags."""
    frame = pd.read_csv(input_dir / "audit" / "EXPORT_prompts_anonymised.csv")
    required = {"pid", "scope", "caps", "objective", "deictic", "nsources",
                "crossdomain", "n_gei"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"prompt corpus is missing columns: {sorted(missing)}")

    frame["caps"] = frame["caps"].fillna("")
    frame["is_out_of_scope"] = frame["objective"].eq("OOS")
    frame["is_platform_meta_only"] = frame["caps"].eq("S")
    frame["eligible"] = ~(frame["is_out_of_scope"] | frame["is_platform_meta_only"])

    recomputed = frame["caps"].apply(
        lambda value: sum(1 for code in GEI_CAPABILITIES if code in value)
    )
    if not (recomputed == frame["n_gei"]).all():
        bad = frame.loc[recomputed != frame["n_gei"], "pid"].tolist()
        raise ValueError(f"n_gei disagrees with caps for pids {bad}")
    return frame


def load_aggregates(input_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load the archived aggregate extracts used as verification targets."""
    audit = input_dir / "audit"
    return {
        "totals": pd.read_csv(audit / "S0_totals.csv"),
        "snapshots": pd.read_csv(audit / "snapshots.csv"),
        "usage_snapshots": pd.read_csv(input_dir / "usage_snapshots.csv"),
        "by_group": pd.read_csv(input_dir / "usage_by_group.csv"),
        "weekday": pd.read_csv(input_dir / "messages_by_weekday.csv"),
        "cap_gei": pd.read_csv(audit / "capability_prevalence_gei.csv"),
        "cap_all": pd.read_csv(audit / "capability_prevalence.csv"),
        "ncap": pd.read_csv(audit / "ncap_distribution.csv"),
        "cooc": pd.read_csv(audit / "cooccurrence.csv", index_col=0),
        "objectives": pd.read_csv(audit / "objectives.csv"),
        "scope": pd.read_csv(audit / "scope_profile.csv"),
        "intext": pd.read_csv(audit / "internal_vs_external.csv"),
        "failure": pd.read_csv(audit / "failure_modes.csv"),
        "discovery": pd.read_csv(audit / "discovery_questions.csv"),
        "payload": Path(audit / "dashboard_payload_pseudonymised.json"),
    }


# --------------------------------------------------------------------------- #
# Prompt-level tables
# --------------------------------------------------------------------------- #

def table_capability_prevalence(frame: pd.DataFrame) -> pd.DataFrame:
    """Prevalence of each GEI capability among eligible prompts."""
    eligible = frame[frame["eligible"]]
    n = len(eligible)
    rows = []
    for code in GEI_CAPABILITIES:
        hits = eligible["caps"].str.contains(code).sum()
        rows.append({
            "capability": code,
            "label": CAPABILITY_LABELS[code],
            "n": int(hits),
            "denominator": n,
            "pct": round(100 * hits / n, 1),
        })
    out = pd.DataFrame(rows).sort_values("n", ascending=False)
    out["mean_capabilities_per_prompt"] = round(eligible["n_gei"].mean(), 3)
    return out


def table_all_code_prevalence(frame: pd.DataFrame) -> pd.DataFrame:
    """Prevalence of every code, including the two non-GEI codes, over all prompts."""
    n = len(frame)
    rows = []
    for code in ALL_CODES:
        hits = int(frame["caps"].str.contains(code).sum())
        rows.append({"code": code, "label": CAPABILITY_LABELS[code], "n": hits,
                     "denominator": n, "pct": round(100 * hits / n, 1)})
    return pd.DataFrame(rows)


def table_composition_depth(frame: pd.DataFrame) -> pd.DataFrame:
    """Distribution of the number of GEI capabilities requested per prompt."""
    eligible = frame[frame["eligible"]]
    counts = eligible["n_gei"].value_counts().sort_index()
    out = pd.DataFrame({
        "n_capabilities": counts.index.astype(int),
        "prompts": counts.values,
    })
    out["pct"] = (100 * out["prompts"] / len(eligible)).round(1)
    out["cum_prompts"] = out["prompts"].cumsum()
    out["cum_pct"] = out["pct"].cumsum().round(1)
    return out


def table_cooccurrence(frame: pd.DataFrame) -> pd.DataFrame:
    """Symmetric co-occurrence matrix of GEI capabilities."""
    eligible = frame[frame["eligible"]]
    matrix = pd.DataFrame(0, index=GEI_CAPABILITIES, columns=GEI_CAPABILITIES)
    for value in eligible["caps"]:
        present = [code for code in GEI_CAPABILITIES if code in value]
        for first, second in itertools.combinations_with_replacement(present, 2):
            matrix.loc[first, second] += 1
            if first != second:
                matrix.loc[second, first] += 1
    return matrix.astype(int)


def table_top_combinations(frame: pd.DataFrame, top: int = 12) -> pd.DataFrame:
    """Most frequent exact capability combinations among multi-capability prompts."""
    eligible = frame[frame["eligible"] & (frame["n_gei"] >= 2)]
    counter: Dict[str, int] = {}
    for value in eligible["caps"]:
        combo = "+".join(code for code in GEI_CAPABILITIES if code in value)
        counter[combo] = counter.get(combo, 0) + 1
    rows = [{"combination": key, "capabilities": key.split("+"), "prompts": count}
            for key, count in sorted(counter.items(), key=lambda item: -item[1])]
    out = pd.DataFrame(rows)
    out["pct_of_multi"] = (100 * out["prompts"] / out["prompts"].sum()).round(1)
    out["readable"] = out["capabilities"].apply(
        lambda codes: " + ".join(SHORT_LABELS[code] for code in codes)
    )
    return out.head(top)


def table_objectives(frame: pd.DataFrame) -> pd.DataFrame:
    """Distribution of the coded analytical objective over all 186 prompts."""
    counts = frame["objective"].value_counts()
    out = pd.DataFrame({
        "objective": counts.index,
        "gloss_inferred": [OBJECTIVE_GLOSS_INFERRED.get(code, "") for code in counts.index],
        "prompts": counts.values,
    })
    out["pct"] = (100 * out["prompts"] / len(frame)).round(1)
    return out


def table_sample_funnel(frame: pd.DataFrame) -> pd.DataFrame:
    """Reconciliation of the coded sample into eligible and non-eligible strata."""
    meta_only = int(frame["is_platform_meta_only"].sum())
    out_of_scope = int(frame["is_out_of_scope"].sum())
    eligible = int(frame["eligible"].sum())
    return pd.DataFrame({
        "stage": ["Coded prompts", "GEI-eligible (>=1 GEI capability)",
                  "Platform-meta only", "Out of scope"],
        "prompts": [len(frame), eligible, meta_only, out_of_scope],
        "pct_of_coded": [100.0, round(100 * eligible / len(frame), 1),
                         round(100 * meta_only / len(frame), 1),
                         round(100 * out_of_scope / len(frame), 1)],
    })


def table_context_profile(frame: pd.DataFrame) -> pd.DataFrame:
    """Capability profile by user context, with both denominators reported.

    ``pct_of_all_in_context`` divides by every prompt observed in the context;
    ``pct_of_eligible_in_context`` divides by the eligible prompts only. The two
    differ substantially and the earlier analysis mixed them, so both are kept.
    """
    rows = []
    for context in CONTEXT_ORDER:
        block = frame[frame["scope"] == context]
        eligible = block[block["eligible"]]
        row = {
            "context": context,
            "n_prompts": len(block),
            "n_eligible": len(eligible),
            "mean_gei_all": round(block["n_gei"].mean(), 2),
            "mean_gei_eligible": round(eligible["n_gei"].mean(), 2),
            "pct_multi_of_all": round(100 * (block["n_gei"] >= 2).mean(), 1),
            "pct_multi_of_eligible": round(100 * (eligible["n_gei"] >= 2).mean(), 1),
        }
        for code in GEI_CAPABILITIES:
            row[f"pct_{code}_of_all"] = round(100 * block["caps"].str.contains(code).mean(), 1)
            row[f"pct_{code}_of_eligible"] = round(
                100 * eligible["caps"].str.contains(code).mean(), 1
            )
        rows.append(row)
    return pd.DataFrame(rows)


def table_internal_external(frame: pd.DataFrame) -> pd.DataFrame:
    """All-prompt code prevalence for internal versus external users."""
    frame = frame.copy()
    frame["audience"] = frame["scope"].str.startswith("Internal").map(
        {True: "internal", False: "external"}
    )
    rows = []
    for code in ALL_CODES:
        internal = frame[frame["audience"] == "internal"]
        external = frame[frame["audience"] == "external"]
        rows.append({
            "code": code,
            "label": CAPABILITY_LABELS[code],
            "n_internal": len(internal),
            "pct_internal": round(100 * internal["caps"].str.contains(code).mean(), 1),
            "n_external": len(external),
            "pct_external": round(100 * external["caps"].str.contains(code).mean(), 1),
        })
    return pd.DataFrame(rows)


def table_evidence_dimensions(frame: pd.DataFrame) -> pd.DataFrame:
    """Cross-domain integration, contextual dependence and named data sources."""
    return pd.DataFrame({
        "dimension": [
            "Requests naming >=1 data source",
            "Requests naming >=2 data sources",
            "Explicit cross-domain integration requested",
            "Artifact- or context-dependent request",
            "Independent request",
        ],
        "prompts": [
            int((frame["nsources"] >= 1).sum()),
            int((frame["nsources"] >= 2).sum()),
            int((frame["crossdomain"] > 0).sum()),
            int((frame["deictic"] > 0).sum()),
            int((frame["deictic"] == 0).sum()),
        ],
        "denominator": len(frame),
    }).assign(pct=lambda d: (100 * d["prompts"] / d["denominator"]).round(1))


# --------------------------------------------------------------------------- #
# Platform-level tables
# --------------------------------------------------------------------------- #

def table_platform_totals(aggregates: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Headline platform indicators for the reference snapshot with derived ratios."""
    totals = aggregates["totals"].iloc[0]
    payload = json.loads(aggregates["payload"].read_text(encoding="utf-8"))["kpi"]
    messages = int(totals["messages"])
    sessions = int(totals["sessions"])
    users = int(totals["users_exact"])
    questions = int(totals["questions"])
    return pd.DataFrame({
        "indicator": [
            "Registered accounts", "Verified accounts", "Active accounts",
            "Sessions", "Messages (user + assistant)", "User questions",
            "Observation window (days)", "Messages per session",
            "Messages per active account", "Questions per active account",
            "Messages per question",
        ],
        "value": [
            payload["reg_accounts"], payload["verified"], users, sessions, messages,
            questions, payload["window_days"], round(messages / sessions, 2),
            round(messages / users, 1), round(questions / users, 2),
            round(messages / questions, 2),
        ],
        "source": [
            "dashboard payload (S4)", "dashboard payload (S4)", "S0_totals.csv",
            "S0_totals.csv", "S0_totals.csv", "S0_totals.csv",
            "dashboard payload (S4)", "derived", "derived", "derived", "derived",
        ],
    })


def table_snapshot_reconciliation(aggregates: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Four successive extractions, showing which differences are growth."""
    frame = aggregates["usage_snapshots"].copy()
    frame["messages_delta"] = frame["total_messages"].diff().fillna(0).astype(int)
    frame["questions_delta"] = frame["user_questions"].diff().fillna(0).astype(int)
    frame["same_window_as_previous"] = (
        (frame["period_start"] == frame["period_start"].shift())
        & (frame["period_end"] == frame["period_end"].shift())
    ).fillna(False)
    return frame


def table_group_activity(aggregates: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Workspace-group activity, with an explicit non-additivity warning."""
    frame = aggregates["by_group"].copy()
    frame = frame.sort_values("messages", ascending=False)
    frame["share_of_total_pct"] = (
        100 * frame["messages"] / frame["messages"].sum()
    ).round(1)
    return frame


def table_weekday_rhythm(aggregates: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Weekday rhythm of message volume, with the weekend share derived."""
    frame = aggregates["weekday"].copy()
    total = int(frame["messages"].sum())
    frame["pct"] = (100 * frame["messages"] / total).round(1)
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    frame["day_type"] = ["Weekend" if day in {"Sat", "Sun"} else "Weekday"
                         for day in frame["weekday"]]
    frame = frame.set_index("weekday").reindex(weekday_names).reset_index()
    return frame


def table_activity_concentration() -> pd.DataFrame:
    """Per-account concentration, reproduced from the administrative reports.

    The administrative usage reports list the ten most active accounts by message
    count for each extraction. Only the aggregate share is reproduced here; the
    account labels are not carried into the repository. Workspace-group shares are
    deliberately *not* computed because groups overlap and are not additive.
    """
    reports = {
        "2026-10-27": {"top10_messages": 2665, "messages": 6688, "active_users": 233},
        "2026-11-10": {"top10_messages": 2779, "messages": 6967, "active_users": 237},
    }
    rows = []
    for stamp, values in reports.items():
        rows.append({
            "snapshot": stamp,
            "top10_messages": values["top10_messages"],
            "total_messages": values["messages"],
            "top10_share_pct": round(100 * values["top10_messages"] / values["messages"], 1),
            "active_accounts": values["active_users"],
            "top10_share_of_accounts_pct": round(1000 / values["active_users"], 1),
            "source": "administrative usage report (aggregate only)",
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# LaTeX writers
# --------------------------------------------------------------------------- #

def tex_escape(text: str) -> str:
    """Escape the characters that break LaTeX text mode.

    Braces, dollar signs and tildes are left alone so that captions may contain
    cross-references and inline mathematics.
    """
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def write_tex_table(path: Path, caption: str, label: str, header: List[str],
                    rows: Iterable[List[str]], colspec: str | None = None,
                    notes: str | None = None) -> None:
    """Write a booktabs table built from string cells."""
    colspec = colspec or ("l" + "r" * (len(header) - 1))
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        rf"\caption{{{tex_escape(caption)}}}",
        rf"\label{{{label}}}",
        rf"\begin{{tabular}}{{{colspec}}}",
        r"\toprule",
        " & ".join(tex_escape(cell) for cell in header) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(tex_escape(str(cell)) for cell in row) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    if notes:
        lines.append(rf"\par\smallskip{{\footnotesize {tex_escape(notes)}}}")
    lines.append(r"\end{table}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Verification
# --------------------------------------------------------------------------- #

def verify(derived: Dict[str, pd.DataFrame],
           aggregates: Dict[str, pd.DataFrame]) -> List[Tuple[str, str, str]]:
    """Compare recomputations against archived marginals."""
    checks: List[Tuple[str, str, str]] = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append((name, "pass" if ok else "FAIL", detail))

    eligible = derived["capability_prevalence"]
    archived = aggregates["cap_gei"].set_index("capability")
    ok = all(int(archived.loc[code, "n"]) == int(eligible.set_index("capability").loc[code, "n"])
             for code in GEI_CAPABILITIES)
    record("capability prevalence (n=141)", ok,
           "matches data/audit/capability_prevalence_gei.csv for all five codes")

    depth = derived["composition_depth"].set_index("n_capabilities")["prompts"]
    archived_depth = aggregates["ncap"].set_index("n_gei")["prompts"]
    record("composition depth",
           list(depth.index) == list(archived_depth.index)
           and list(depth.values) == list(archived_depth.values),
           "matches data/audit/ncap_distribution.csv")

    cooc = derived["cooccurrence"]
    record("co-occurrence matrix", bool((cooc.values == aggregates["cooc"].values).all()),
           "matches data/audit/cooccurrence.csv cell by cell")

    obj = derived["objectives"].set_index("objective")["prompts"]
    archived_obj = aggregates["objectives"].set_index("objective")["n"]
    record("objective distribution (n=186)",
           list(obj.index) == list(archived_obj.index)
           and list(obj.values) == list(archived_obj.values),
           "matches data/audit/objectives.csv")

    allcodes = derived["all_code_prevalence"].set_index("code")["n"]
    archived_codes = aggregates["cap_all"].set_index("capability")["n"]
    record("all-code prevalence (n=186)",
           list(allcodes.index) == list(archived_codes.index)
           and list(allcodes.values) == list(archived_codes.values),
           "matches data/audit/capability_prevalence.csv")

    context = derived["context_profile"].set_index("context")
    archived_scope = aggregates["scope"].set_index("scope")
    ok = all(int(context.loc[name, "n_prompts"]) == int(archived_scope.loc[name, "n_prompts"])
             and abs(context.loc[name, "mean_gei_all"] - archived_scope.loc[name, "mean_gei"]) < 5e-3
             for name in CONTEXT_ORDER)
    record("context profile", ok,
           "n_prompts and mean_gei reproduce data/audit/scope_profile.csv")

    funnel = derived["sample_funnel"].set_index("stage")["prompts"]
    record("sample funnel closes", int(funnel["Platform-meta only"] + funnel["Out of scope"]
                                       + funnel["GEI-eligible (>=1 GEI capability)"])
           == int(funnel["Coded prompts"]),
           "36 + 9 + 141 = 186")

    weekday = derived["weekday_rhythm"]
    totals = int(aggregates["totals"].iloc[0]["messages"])
    record("weekday counts are additive", int(weekday["messages"].sum()) == totals,
           f"{int(weekday['messages'].sum())} = {totals}")

    group_sum = int(aggregates["by_group"]["messages"].sum())
    record("group rows are NOT additive (expected)", group_sum > totals,
           f"sum of groups {group_sum} > total {totals}; "
           "group shares must not be interpreted as a partition of activity")

    record("tool-call extract present", False,
           "no tool-call table exists in the repository; "
           "the '10,863 tool calls across 36 categories' figure is unsupported")
    record("time series of activity present", False,
           "only four cumulative snapshots and a weekday rhythm exist; "
           "no monthly or weekly activity series is archived")
    record("geographic or institutional distribution present", False,
           "withheld by design: group labels are pseudonymised and no geography is stored")
    return checks


def verification_report(checks: List[Tuple[str, str, str]], frame: pd.DataFrame) -> str:
    """Render the verification checks as markdown."""
    lines = [
        "# Section 5 — verification report",
        "",
        "Generated by `section_05_deployment_and_use/scripts/reproduce_section5.py`.",
        "",
        f"Coded prompt corpus: {len(frame)} rows, "
        f"{int(frame['eligible'].sum())} eligible under the documented rule.",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    for name, status, detail in checks:
        lines.append(f"| {name} | {status} | {detail} |")
    failures = [check for check in checks if check[1] == "FAIL"]
    lines += [
        "",
        f"**{len(checks) - len(failures)} checks passed, {len(failures)} require attention.**",
        "",
        "A `FAIL` on an archival check means the recomputation disagrees with a stored",
        "aggregate and must be resolved before the number is quoted. A `FAIL` on an",
        "availability check means the evidence does not exist in the repository; the",
        "corresponding claim cannot be made in the manuscript as written.",
    ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main() -> None:
    """Rebuild the derived tables, the LaTeX tables and the verification report."""
    default_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_root)
    parser.add_argument("--input", type=Path, default=None,
                        help="folder holding the raw aggregates (default: <repo>/data)")
    parser.add_argument("--out", type=Path, default=None,
                        help="Section 5 folder (default: <repo>/section_05_deployment_and_use)")
    args = parser.parse_args()

    input_dir = args.input or (args.repo_root / "data")
    out_dir = args.out or (args.repo_root / "section_05_deployment_and_use")
    tables_dir = out_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    frame = load_prompts(input_dir)
    aggregates = load_aggregates(input_dir)

    derived = {
        "capability_prevalence": table_capability_prevalence(frame),
        "all_code_prevalence": table_all_code_prevalence(frame),
        "composition_depth": table_composition_depth(frame),
        "cooccurrence": table_cooccurrence(frame),
        "top_combinations": table_top_combinations(frame),
        "objectives": table_objectives(frame),
        "sample_funnel": table_sample_funnel(frame),
        "context_profile": table_context_profile(frame),
        "internal_external": table_internal_external(frame),
        "evidence_dimensions": table_evidence_dimensions(frame),
        "platform_totals": table_platform_totals(aggregates),
        "snapshot_reconciliation": table_snapshot_reconciliation(aggregates),
        "group_activity": table_group_activity(aggregates),
        "weekday_rhythm": table_weekday_rhythm(aggregates),
        "concentration": table_activity_concentration(),
        "failure_modes": aggregates["failure"].copy(),
        "discovery_questions": aggregates["discovery"].copy(),
    }

    destinations = {
        "capability_prevalence": "04_gei_capability_composition/derived",
        "all_code_prevalence": "04_gei_capability_composition/derived",
        "composition_depth": "04_gei_capability_composition/derived",
        "cooccurrence": "04_gei_capability_composition/derived",
        "top_combinations": "04_gei_capability_composition/derived",
        "context_profile": "04_gei_capability_composition/derived",
        "internal_external": "04_gei_capability_composition/derived",
        "evidence_dimensions": "04_gei_capability_composition/derived",
        "objectives": "03_epidemiological_requests/derived",
        "sample_funnel": "03_epidemiological_requests/derived",
        "failure_modes": "05_real_world_settings/derived",
        "discovery_questions": "05_real_world_settings/derived",
        "platform_totals": "01_deployment_and_user_base/derived",
        "snapshot_reconciliation": "01_deployment_and_user_base/derived",
        "group_activity": "01_deployment_and_user_base/derived",
        "weekday_rhythm": "02_patterns_of_platform_use/derived",
        "concentration": "02_patterns_of_platform_use/derived",
    }
    for name, table in derived.items():
        folder = out_dir / destinations[name]
        folder.mkdir(parents=True, exist_ok=True)
        table.to_csv(folder / f"{name}.csv", index=(name == "cooccurrence"))

    # The sample funnel describes both the sampling (5.3) and the eligibility rule
    # used for the capability analysis (5.4), so it is written to both folders.
    derived["sample_funnel"].to_csv(
        out_dir / "04_gei_capability_composition" / "derived" / "sample_funnel.csv",
        index=False,
    )

    # ---- LaTeX tables ----------------------------------------------------- #
    cap = derived["capability_prevalence"]
    write_tex_table(
        tables_dir / "t5_1_capability_prevalence.tex",
        "Prevalence of the five GEI capability areas in the coded corpus "
        f"({int(cap['denominator'].iloc[0])} eligible prompts). A prompt may request "
        "more than one capability, so percentages do not sum to 100.",
        "tab:s5-capability-prevalence",
        ["Capability", "Code", "Requests", "% of eligible"],
        [[row.label, row.capability, row.n, f"{row.pct:.1f}"] for row in cap.itertuples()],
        colspec="lrrr",
        notes="% of eligible prompts",
    )

    depth = derived["composition_depth"]
    write_tex_table(
        tables_dir / "t5_2_composition_depth.tex",
        "Number of GEI capability areas requested per eligible prompt. "
        "Mean 1.61 capabilities per prompt; 59 prompts (41.8%) request two or more.",
        "tab:s5-composition-depth",
        ["Capabilities per prompt", "Prompts", "%", "Cumulative %"],
        [[row.n_capabilities, row.prompts, f"{row.pct:.1f}", f"{row.cum_pct:.1f}"]
         for row in depth.itertuples()],
        colspec="rrrr",
        notes="% of eligible prompts",
    )

    cooc = derived["cooccurrence"]
    write_tex_table(
        tables_dir / "t5_3_cooccurrence.tex",
        "Co-occurrence of GEI capability areas among the 141 eligible prompts. "
        "Diagonal cells are the marginal counts of Table~\\\\ref{tab:s5-capability-prevalence}.",
        "tab:s5-cooccurrence",
        ["Capability"] + [SHORT_LABELS[code] for code in GEI_CAPABILITIES],
        [[SHORT_LABELS[row] for row in [code]] + [cooc.loc[code, other]
                                                  for other in GEI_CAPABILITIES]
         for code in GEI_CAPABILITIES],
        colspec="lrrrrr",
        notes="Counts are prompt counts, not percentages",
    )

    combos = derived["top_combinations"]
    write_tex_table(
        tables_dir / "t5_4_top_combinations.tex",
        "Most frequent capability combinations among the 59 multi-capability prompts.",
        "tab:s5-combinations",
        ["Combination", "Prompts", "% of multi-capability"],
        [[row.readable, row.prompts, f"{row.pct_of_multi:.1f}"] for row in combos.itertuples()],
        colspec="lrr",
        notes="% of the 59 prompts requesting two or more capabilities",
    )

    obj = derived["objectives"]
    write_tex_table(
        tables_dir / "t5_5_objectives.tex",
        "Distribution of the coded analytical objective over all 186 coded prompts. "
        "Glosses are inferred from the coded prompts and require author confirmation.",
        "tab:s5-objectives",
        ["Objective code", "Inferred gloss", "Prompts", "% of coded"],
        [[row.objective, row.gloss_inferred, row.prompts, f"{row.pct:.1f}"]
         for row in obj.itertuples()],
        colspec="llrr",
        notes="Inferred gloss, not a repository fact",
    )

    ctx = derived["context_profile"]
    header = ["Context", "$n$"] + [SHORT_LABELS[code] for code in GEI_CAPABILITIES] + ["Multi %"]
    rows = []
    for row in ctx.itertuples():
        rows.append([row.context, row.n_eligible]
                    + [f"{getattr(row, f'pct_{code}_of_eligible'):.1f}" for code in GEI_CAPABILITIES]
                    + [f"{row.pct_multi_of_eligible:.1f}"])
    write_tex_table(
        tables_dir / "t5_6_capability_by_context.tex",
        "Capability profile by user context, over the eligible prompts of each context. "
        "Percentages are computed within context and do not sum to 100 across columns.",
        "tab:s5-context",
        header, rows, colspec="l" + "r" * 7,
        notes="% of eligible prompts in the context",
    )

    ie = derived["internal_external"]
    write_tex_table(
        tables_dir / "t5_7_internal_external.tex",
        "Code prevalence for internal versus external users, over all coded prompts of "
        "each audience (internal $n=43$, external $n=143$).",
        "tab:s5-internal-external",
        ["Code", "Capability", "Internal %", "External %", "$\\Delta$"],
        [[row.code, row.label, f"{row.pct_internal:.1f}", f"{row.pct_external:.1f}",
          f"{row.pct_external - row.pct_internal:+.1f}"] for row in ie.itertuples()],
        colspec="llrrr",
        notes="% of coded prompts in the audience",
    )

    ev = derived["evidence_dimensions"]
    write_tex_table(
        tables_dir / "t5_8_evidence_dimensions.tex",
        "Evidence dimensions coded for every prompt: named data sources, explicit "
        "cross-domain integration and dependence on previous conversational context.",
        "tab:s5-evidence-dimensions",
        ["Dimension", "Prompts", "$n$", "%"],
        [[row.dimension, row.prompts, row.denominator, f"{row.pct:.1f}"]
         for row in ev.itertuples()],
        colspec="lrrr",
        notes="% of 186 coded prompts",
    )

    funnel = derived["sample_funnel"]
    write_tex_table(
        tables_dir / "t5_9_sample_funnel.tex",
        "Composition of the coded prompt sample and the eligibility rule used in "
        "Section 5.4.",
        "tab:s5-funnel",
        ["Stage", "Prompts", "% of coded"],
        [[row.stage, row.prompts, f"{row.pct_of_coded:.1f}"] for row in funnel.itertuples()],
        colspec="lrr",
        notes="Eligible = not out of scope and not platform-meta only",
    )

    fail = derived["failure_modes"]
    write_tex_table(
        tables_dir / "t5_10_failure_modes.tex",
        "Friction categories observed in the coded prompt corpus.",
        "tab:s5-failure-modes",
        ["Observed friction", "Prompts", "% of coded", "Groups"],
        [[row.failure_mode, row.n, f"{row.pct:.1f}", row.n_groups]
         for row in fail.itertuples()],
        colspec="lrrr",
        notes="% of 186 coded prompts; a prompt may show more than one friction category",
    )

    totals = derived["platform_totals"]
    write_tex_table(
        tables_dir / "t5_11_platform_totals.tex",
        "Platform activity in the reference window (28 March to 10 November 2026), "
        "extraction of 10 November 2026.",
        "tab:s5-platform-totals",
        ["Indicator", "Value"],
        [[row.indicator, row.value] for row in totals.itertuples()],
        colspec="lr",
        notes="Ratios are derived from the counts in the same table",
    )

    week = derived["weekday_rhythm"]
    write_tex_table(
        tables_dir / "t5_12_weekday_rhythm.tex",
        "Weekday rhythm of message volume in the reference window. The seven rows are "
        "additive and sum to the all-user message total.",
        "tab:s5-weekday",
        ["Weekday", "Messages", "%"],
        [[row.weekday, row.messages, f"{row.pct:.1f}"] for row in week.itertuples()],
        colspec="lrr",
        notes="Additive table; weekend share 14.1%",
    )

    # ---- verification report --------------------------------------------- #
    checks = verify(derived, aggregates)
    (out_dir / "methodology").mkdir(parents=True, exist_ok=True)
    (out_dir / "methodology" / "VERIFICATION_REPORT.md").write_text(
        verification_report(checks, frame), encoding="utf-8"
    )

    print(f"wrote {len(derived)} derived tables and 12 LaTeX tables to {out_dir}")
    for name, status, detail in checks:
        print(f"  [{status:4s}] {name}: {detail}")
    if any(status == "FAIL" for _, status, _ in checks[:8]):
        raise SystemExit("archival recomputation failed; see VERIFICATION_REPORT.md")


if __name__ == "__main__":
    main()
