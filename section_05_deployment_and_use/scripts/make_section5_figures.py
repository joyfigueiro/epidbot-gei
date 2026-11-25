#!/usr/bin/env python3
"""Regenerate the Section 5 figures from the derived tables.

Every figure in this script is drawn from a CSV produced by
``reproduce_section5.py`` (or from an archived aggregate that the same script
verified), so a figure can never disagree with the table it illustrates. No
number is typed into this file.

Outputs, for each figure, a 300 dpi PNG for word processors and a vector PDF for
LaTeX. Both carry identical content. Labels, ticks and annotations are in English.

Usage
-----
    python make_section5_figures.py --repo-root ../..
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# House style
# --------------------------------------------------------------------------- #

CAPABILITY_COLORS: Dict[str, str] = {
    "I": "#1b6ca8",
    "K": "#2a9d8f",
    "A": "#e76f51",
    "M": "#6a4c93",
    "V": "#f4a261",
    "S": "#8d99ae",
    "X": "#b0b0b0",
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

GEI_CAPABILITIES: List[str] = ["I", "K", "A", "M", "V"]

DPI: int = 300


def apply_style() -> None:
    """Apply the shared matplotlib style for all Section 5 figures."""
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": DPI,
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.titlesize": 9.5,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#d9d9d9",
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "pdf.fonttype": 42,
    })


def save(fig: plt.Figure, out_dir: Path, name: str) -> None:
    """Write one figure as 300 dpi PNG and as vector PDF."""
    fig.savefig(out_dir / f"{name}.png", dpi=DPI, bbox_inches="tight",
                facecolor="white")
    fig.savefig(out_dir / f"{name}.pdf", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Figures
# --------------------------------------------------------------------------- #

def fig_capability_composition(derived: Path, out_dir: Path) -> None:
    """Prevalence of the five capabilities beside the depth of composition."""
    prevalence = pd.read_csv(derived / "04_gei_capability_composition/derived/capability_prevalence.csv")
    depth = pd.read_csv(derived / "04_gei_capability_composition/derived/composition_depth.csv")
    eligibility = pd.read_csv(derived / "04_gei_capability_composition/derived/sample_funnel.csv")
    n_eligible = int(eligibility.set_index("stage").loc["GEI-eligible (>=1 GEI capability)", "prompts"])

    fig, (left, right) = plt.subplots(1, 2, figsize=(7.2, 2.9),
                                      gridspec_kw={"width_ratios": [1.35, 1]})

    order = prevalence.sort_values("n")
    colors = [CAPABILITY_COLORS[code] for code in order["capability"]]
    left.barh([SHORT_LABELS[code] for code in order["capability"]], order["n"],
              color=colors, height=0.62, edgecolor="white", linewidth=0.8)
    for position, (value, pct) in enumerate(zip(order["n"], order["pct"])):
        left.text(value + 1.0, position, f"{value}  ({pct:.1f}%)", va="center", fontsize=8)
    left.set_xlim(0, max(order["n"]) * 1.34)
    left.set_xlabel(f"Prompts requesting the capability (n = {n_eligible} eligible)")
    left.set_title("(a) Capability prevalence", loc="left")
    left.grid(axis="y", visible=False)

    right.bar(depth["n_capabilities"], depth["prompts"], color="#4a5c6a",
              width=0.62, edgecolor="white", linewidth=0.8)
    for row in depth.itertuples():
        right.text(row.n_capabilities, row.prompts + 1.6, f"{row.prompts}",
                   ha="center", fontsize=8)
    right.set_xticks(depth["n_capabilities"])
    right.set_xlabel("Capability areas requested per prompt")
    right.set_ylabel("Prompts")
    right.set_ylim(0, depth["prompts"].max() * 1.22)
    multi = int((depth.loc[depth["n_capabilities"] >= 2, "prompts"]).sum())
    right.set_title("(b) Composition depth", loc="left")
    right.annotate(f"{multi} prompts ({100 * multi / n_eligible:.1f}%) request\n"
                   f"two or more areas; mean {prevalence['mean_capabilities_per_prompt'].iloc[0]:.2f}",
                   xy=(0.50, 0.64), xycoords="axes fraction", fontsize=7.6, va="top")
    right.grid(axis="x", visible=False)

    fig.tight_layout()
    save(fig, out_dir, "fig5_1_capability_composition")


def fig_cooccurrence(derived: Path, out_dir: Path) -> None:
    """Co-occurrence matrix of the five capability areas."""
    matrix = pd.read_csv(derived / "04_gei_capability_composition/derived/cooccurrence.csv",
                         index_col=0)
    matrix = matrix.loc[GEI_CAPABILITIES, GEI_CAPABILITIES]

    fig, ax = plt.subplots(figsize=(4.5, 3.6))
    shown = matrix.values.astype(float)
    masked = np.where(np.eye(len(matrix), dtype=bool), np.nan, shown)
    image = ax.imshow(masked, cmap="Blues", vmin=0, vmax=np.nanmax(masked))

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            value = int(shown[i, j])
            on_diagonal = i == j
            ax.text(j, i, f"{value}", ha="center", va="center", fontsize=8.5,
                    color="white" if (not on_diagonal and value > 0.55 * np.nanmax(masked)) else "#1a1a1a",
                    fontweight="bold" if on_diagonal else "normal")
            if on_diagonal:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=True,
                                           facecolor="#cfd8dc", edgecolor="white",
                                           linewidth=1.4, zorder=1))
                ax.text(j, i, f"{value}", ha="center", va="center", fontsize=8.5,
                        color="#1a1a1a", fontweight="bold", zorder=2)

    labels = [SHORT_LABELS[code] for code in GEI_CAPABILITIES]
    ax.set_xticks(range(len(labels)), labels, rotation=28, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    ax.grid(False)
    ax.set_title("Capability co-occurrence (prompt counts)", loc="left")
    bar = fig.colorbar(image, ax=ax, fraction=0.044, pad=0.03)
    bar.set_label("Prompts (off-diagonal)")
    bar.outline.set_visible(False)
    fig.tight_layout()
    save(fig, out_dir, "fig5_2_capability_cooccurrence")


def fig_capability_by_context(derived: Path, out_dir: Path) -> None:
    """Capability profile of each user context, over eligible prompts."""
    profile = pd.read_csv(derived / "04_gei_capability_composition/derived/context_profile.csv")
    profile = profile.iloc[::-1].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(7.0, 3.1))
    height = 0.15
    positions = np.arange(len(profile))
    for offset, code in enumerate(GEI_CAPABILITIES):
        values = profile[f"pct_{code}_of_eligible"]
        ax.barh(positions + (offset - 2) * height, values, height=height,
                color=CAPABILITY_COLORS[code], label=SHORT_LABELS[code],
                edgecolor="white", linewidth=0.5)
    ax.set_yticks(positions,
                  [f"{row.context}\n(n = {row.n_eligible})" for row in profile.itertuples()])
    ax.set_xlabel("% of eligible prompts in the context")
    ax.set_xlim(0, 100)
    ax.grid(axis="y", visible=False)
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.14), frameon=False)
    ax.set_title("")
    fig.tight_layout()
    save(fig, out_dir, "fig5_3_capability_by_context")


def fig_objectives(derived: Path, out_dir: Path) -> None:
    """Distribution of coded analytical objectives."""
    objectives = pd.read_csv(derived / "03_epidemiological_requests/derived/objectives.csv")
    objectives = objectives.sort_values("prompts")
    total = int(objectives["prompts"].sum())

    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    colors = ["#b0b0b0" if code in {"OOS"} else "#2b6f8a"
              for code in objectives["objective"]]
    ax.barh(objectives["objective"], objectives["prompts"], color=colors,
            height=0.66, edgecolor="white", linewidth=0.8)
    for position, row in enumerate(objectives.itertuples()):
        ax.text(row.prompts + 0.7, position, f"{row.prompts} ({row.pct:.1f}%)",
                va="center", fontsize=7.8)
    ax.set_xlim(0, objectives["prompts"].max() * 1.36)
    ax.set_xlabel(f"Coded prompts (n = {total})")
    ax.grid(axis="y", visible=False)
    ax.set_title("Analytical objective of the coded requests", loc="left")
    fig.tight_layout()
    save(fig, out_dir, "fig5_4_analytical_objectives")


def fig_activity(derived: Path, out_dir: Path) -> None:
    """Weekday rhythm beside the distribution of activity across workspace groups."""
    weekday = pd.read_csv(derived / "02_patterns_of_platform_use/derived/weekday_rhythm.csv")
    groups = pd.read_csv(derived / "01_deployment_and_user_base/derived/group_activity.csv")

    fig, (left, right) = plt.subplots(1, 2, figsize=(7.2, 2.9),
                                      gridspec_kw={"width_ratios": [1, 1.15]})

    colors = ["#c8cdd4" if day in {"Sat", "Sun"} else "#2b6f8a"
              for day in weekday["weekday"]]
    left.bar(weekday["weekday"], weekday["messages"], color=colors, width=0.66,
             edgecolor="white", linewidth=0.8)
    weekend = weekday.loc[weekday["day_type"] == "Weekend", "messages"].sum()
    left.set_ylabel("Messages")
    left.set_xlabel("Day of week")
    left.grid(axis="x", visible=False)
    left.set_title("(a) Weekly rhythm", loc="left")
    left.annotate(f"weekend share {100 * weekend / weekday['messages'].sum():.1f}%",
                  xy=(0.60, 0.96), xycoords="axes fraction", fontsize=7.6, va="top")

    ordered = groups.sort_values("messages")
    right.barh(ordered["group_id"], ordered["messages"], color="#4a5c6a",
               height=0.68, edgecolor="white", linewidth=0.8)
    for position, row in enumerate(ordered.itertuples()):
        right.text(row.messages + 60, position, f"{row.messages:,}", va="center", fontsize=7.4)
    right.set_xlabel("Messages")
    right.set_xlim(0, ordered["messages"].max() * 1.25)
    right.grid(axis="y", visible=False)
    right.set_title("(b) Activity by workspace group", loc="left")
    right.annotate("groups overlap: shares are\nnot a partition of activity",
                   xy=(0.34, 0.24), xycoords="axes fraction", fontsize=7.2, va="top")

    fig.tight_layout()
    save(fig, out_dir, "fig5_5_activity_rhythm_and_groups")


def fig_friction(derived: Path, out_dir: Path) -> None:
    """Friction categories observed in the coded corpus."""
    friction = pd.read_csv(derived / "05_real_world_settings/derived/failure_modes.csv")
    friction = friction.sort_values("n")
    total = 186

    fig, ax = plt.subplots(figsize=(6.4, 2.7))
    ax.barh(friction["failure_mode"], friction["n"], color="#a4553f", height=0.66,
            edgecolor="white", linewidth=0.8)
    for position, row in enumerate(friction.itertuples()):
        ax.text(row.n + 0.12, position, f"{row.n} ({row.pct:.1f}%)", va="center", fontsize=7.8)
    ax.set_xlim(0, friction["n"].max() * 1.55)
    ax.set_xlabel(f"Coded prompts exhibiting the category (n = {total})")
    ax.grid(axis="y", visible=False)
    ax.set_title("Friction observed in the request record", loc="left")
    fig.tight_layout()
    save(fig, out_dir, "fig5_6_observed_friction")


def main() -> None:
    """Render every Section 5 figure."""
    default_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_root)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    out_dir = args.out or (args.repo_root / "section_05_deployment_and_use" / "figures")
    out_dir.mkdir(parents=True, exist_ok=True)
    derived = args.repo_root / "section_05_deployment_and_use"

    apply_style()
    fig_capability_composition(derived, out_dir)
    fig_cooccurrence(derived, out_dir)
    fig_capability_by_context(derived, out_dir)
    fig_objectives(derived, out_dir)
    fig_activity(derived, out_dir)
    fig_friction(derived, out_dir)
    print(f"wrote 6 figures (PNG {DPI} dpi + PDF) to {out_dir}")


if __name__ == "__main__":
    main()
