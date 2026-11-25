#!/usr/bin/env python3
"""
reproduce_rt.py - NEW code, written for the 01_ipiranga_dengue_rt archive.

This is NOT the original analysis script. The authoritative artefact is
artifacts/code/snippet_15649__plot_2735.py, which is what actually produced
artifacts/figures/ipiranga_rt_2025.png (plot 2735).

This rewrite exists only to make the archived estimator runnable with portable
paths. The estimator is unchanged: Cori et al. (2013) sliding-window Rt with a
Gamma(a, b) posterior prior over incidence from a discretised gamma serial
interval.

Dependencies (see requirements.txt): numpy, pandas, scipy, matplotlib.

Usage
-----
    python reproduce_rt.py \
        --dataset ../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet \
        --outdir ./out

Outputs
-------
    <outdir>/rt_estimates_2025.csv    per-week Rt with 95% CI
    <outdir>/rt_2025.png              figure equivalent to plot 2735

CAVEAT
------
Running this produces NEW numbers. Report them as a fresh reproduction, never as
corroboration of the original session - the original outputs are the ones in
artifacts/ and they are the record.
"""

from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd
from scipy.stats import gamma as gammadist

# Defaults mirror the archived script exactly.
DEFAULT_WINDOW = 7          # weeks
DEFAULT_PRIOR_A = 1.0       # Gamma prior, shape
DEFAULT_PRIOR_B = 0.2       # Gamma prior, rate
DEFAULT_SI_MEAN = 2.0       # serial interval mean, in weekly periods
DEFAULT_SI_SD = 1.0         # serial interval sd,   in weekly periods
FALLBACK_POP = 14230.0      # archived script hard-codes this


def discretise_gamma(mean: float, sd: float, max_len: int = 40) -> np.ndarray:
    """Discretise a gamma distribution over integer lags 0..max_len."""
    if mean <= 0 or sd <= 0:
        raise ValueError("serial interval mean and sd must be positive")
    shape = (mean / sd) ** 2
    rate = mean / sd ** 2
    p = np.array(
        [
            gammadist.cdf(k + 0.5, shape, scale=1.0 / rate)
            - gammadist.cdf(k - 0.5, shape, scale=1.0 / rate)
            for k in range(max_len + 1)
        ]
    )
    p[0] = 0.0
    total = p.sum()
    if total <= 0:
        raise ValueError("degenerate serial interval after discretisation")
    return p / total


def load_series(path: str) -> tuple[pd.DataFrame, float]:
    """Read an InfoDengue parquet and return (sorted unique week series, population)."""
    df = pd.read_parquet(path)
    required = {"data_iniSE", "SE", "casos"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required column(s): {sorted(missing)}")

    df = df.copy()
    df["data_iniSE"] = pd.to_datetime(df["data_iniSE"])
    df = (
        df.sort_values("data_iniSE")
        .drop_duplicates("data_iniSE")
        .reset_index(drop=True)
    )
    if "p_inc100k" not in df.columns:
        df["p_inc100k"] = np.nan

    pop = FALLBACK_POP
    if "pop" in df.columns and df["pop"].notna().any():
        pop = float(df["pop"].dropna().iloc[0])
    return df, pop


def cori_rt(
    incidence: np.ndarray,
    si: np.ndarray,
    window: int = DEFAULT_WINDOW,
    prior_a: float = DEFAULT_PRIOR_A,
    prior_b: float = DEFAULT_PRIOR_B,
) -> pd.DataFrame:
    """Sliding-window Rt, Cori et al. (2013), gamma posterior.

    For each window ending at t, the posterior is Gamma(a + sum(I), b + sum(Lambda))
    where Lambda is the force-of-infection from earlier incidence convolved with SI.
    """
    n = len(incidence)
    lam = np.zeros(n)
    for s in range(1, n):
        upper = min(s, len(si) - 1)
        lam[s] = sum(incidence[s - u] * si[u] for u in range(1, upper + 1))

    rows = []
    for t in range(window - 1, n):
        win_cases = incidence[t - window + 1 : t + 1].sum()
        win_lam = lam[t - window + 1 : t + 1].sum()
        shape = prior_a + win_cases
        rate = prior_b + win_lam
        rows.append(
            {
                "idx": t,
                "win_cases": win_cases,
                "Rt": shape / rate,
                "lo": gammadist.ppf(0.025, shape, scale=1.0 / rate),
                "hi": gammadist.ppf(0.975, shape, scale=1.0 / rate),
                "p_gt1": 1.0 - gammadist.cdf(1.0, shape, scale=1.0 / rate),
            }
        )
    return pd.DataFrame(rows)


def find_runs(mask: list[bool], min_len: int) -> list[tuple[int, int]]:
    """Return (start, end) index runs where mask is True for at least min_len steps."""
    out: list[tuple[int, int]] = []
    start = None
    for i, flag in enumerate(mask):
        if flag and start is None:
            start = i
        if not flag and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(mask) - 1))
    return [(a, b) for a, b in out if b - a + 1 >= min_len]


def plot(r25: pd.DataFrame, out_png: str, subtitle: str) -> None:
    """Render the cases/Rt figure."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = np.arange(len(r25))
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.bar(x, r25["casos"], color="#9ecae1", edgecolor="#6baed6",
           label="weekly notified cases")
    ax2 = ax.twinx()
    ax2.fill_between(x, r25["lo"], r25["hi"], color="#e6550d", alpha=0.22,
                     label="Rt 95% CI")
    ax2.plot(x, r25["Rt"], color="#e6550d", lw=2, label="Rt (posterior mean)")
    ax2.axhline(1, color="k", ls="--", lw=1)
    for a, b in find_runs(list(r25["lo"] > 1), 2):
        ax2.axvspan(a - 0.5, b + 0.5, color="#fdae6b", alpha=0.28, zorder=0)

    ax2.set_ylim(0, 12)
    ax.set_ylim(0, 17)
    ax.set_ylabel("notified cases / week")
    ax2.set_ylabel("Rt")
    ax.set_xticks(x[::4])
    ax.set_xticklabels([f"SE{int(v)}" for v in r25["SE"][::4]], rotation=45,
                       ha="right", fontsize=8)
    ax.set_title(f"Ipiranga (PR) - dengue Rt, 2025\n{subtitle}", fontsize=11)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)
    ax.set_xlabel("epidemiological week (InfoDengue)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", required=True,
                    help="InfoDengue parquet (municipality-week dengue counts)")
    ap.add_argument("--outdir", default="./out", help="output directory")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW)
    ap.add_argument("--si-mean", type=float, default=DEFAULT_SI_MEAN,
                    help="serial interval mean in weekly periods (2.0 == 14 days)")
    ap.add_argument("--si-sd", type=float, default=DEFAULT_SI_SD,
                    help="serial interval sd in weekly periods (1.0 == 7 days)")
    ap.add_argument("--prior-a", type=float, default=DEFAULT_PRIOR_A)
    ap.add_argument("--prior-b", type=float, default=DEFAULT_PRIOR_B)
    ap.add_argument("--year", type=int, default=2025)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    df, pop = load_series(args.dataset)
    si = discretise_gamma(args.si_mean, args.si_sd)

    r = cori_rt(df["casos"].to_numpy(dtype=float), si,
                window=args.window, prior_a=args.prior_a, prior_b=args.prior_b)
    r["week"] = df["data_iniSE"].iloc[r["idx"].values].values
    r["SE"] = df["SE"].iloc[r["idx"].values].values
    r["casos"] = df["casos"].iloc[r["idx"].values].values
    r["inc100k"] = df["p_inc100k"].iloc[r["idx"].values].values

    r_year = r[pd.to_datetime(r["week"]).dt.year == args.year].reset_index(drop=True)
    if r_year.empty:
        raise SystemExit(f"no Rt estimates fall inside {args.year}")

    csv_path = os.path.join(args.outdir, f"rt_estimates_{args.year}.csv")
    r_year.to_csv(csv_path, index=False)

    for a, b in find_runs(list(r_year["Rt"] > 1), 3):
        seg = r_year["Rt"][a : b + 1]
        print(f"Rt>1 run  SE{int(r_year['SE'][a])}-{int(r_year['SE'][b])}: "
              f"{b - a + 1} wks, Rt {seg.min():.2f}-{seg.max():.2f}")
    for a, b in find_runs(list(r_year["lo"] > 1), 2):
        seg = r_year["Rt"][a : b + 1]
        print(f"CI>1 run  SE{int(r_year['SE'][a])}-{int(r_year['SE'][b])}: "
              f"{b - a + 1} wks, Rt {seg.min():.2f}-{seg.max():.2f}")

    n_cases = int(r_year["casos"].sum())
    print(f"\n{args.year}: {len(r_year)} weeks, {n_cases} cases, "
          f"{n_cases / pop * 100000:.1f} per 100k (pop {pop:.0f})")
    print(f"latest Rt: {r_year['Rt'].iloc[-1]:.2f} "
          f"[{r_year['lo'].iloc[-1]:.2f}, {r_year['hi'].iloc[-1]:.2f}]")

    png = os.path.join(args.outdir, f"rt_{args.year}.png")
    plot(r_year, png,
         f"Cori et al. (2013), {args.window}-week window, gamma SI "
         f"mean {args.si_mean} sd {args.si_sd} weekly periods; shaded = 95% CI > 1")
    print(f"\nwrote {csv_path}\nwrote {png}")


if __name__ == "__main__":
    main()
