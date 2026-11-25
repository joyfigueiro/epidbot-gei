#!/usr/bin/env python3
"""
verify_archived_algorithm.py - NEW code, written for the verification pass.

WHAT THIS IS
------------
A port of the estimator in artifacts/code/snippet_15649__plot_2735.py, with the
hard-coded input path replaced by an argument and with two extra columns
(win_lam = summed infectiousness, and the epi-year bookkeeping) written out.

The estimator itself is NOT modified: disc(), cori() and runs() are copied
function-for-function from the archived script, including its defaults
(window=7, a=1., b=.2, SI mean 2.0 sd 1.0).

WHAT THIS IS NOT
----------------
This is a RE-EXECUTION, not the original execution. It establishes that the
archived code, run on the archived data, produces numbers consistent with the
narrative. It does not recover the original run's outputs, and it cannot
establish what the original process was.

Usage
-----
    python verify_archived_algorithm.py --dataset ../../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet                                        --outdir ../outputs
"""

from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd
from scipy.stats import gamma as gammadist


# ----------------------------------------------------------------------------
# Copied verbatim from artifacts/code/snippet_15649__plot_2735.py
# ----------------------------------------------------------------------------
def disc(mean, sd, max_len=40):
    """Discretise a gamma serial interval over integer lags."""
    shape = (mean / sd) ** 2
    rate = mean / sd ** 2
    p = np.array([
        gammadist.cdf(k + .5, shape, scale=1 / rate) - gammadist.cdf(k - .5, shape, scale=1 / rate)
        for k in range(max_len + 1)
    ])
    p[0] = 0.
    return p / p.sum()


def cori(I, si, window=7, a=1., b=.2):
    """Sliding-window Rt, Cori et al. (2013); gamma posterior Gamma(a+sum I, b+sum Lambda)."""
    n = len(I)
    lam = np.zeros(n)
    for s in range(1, n):
        lam[s] = sum(I[s - u] * si[u] for u in range(1, min(s, len(si) - 1) + 1))
    rows = []
    for t in range(window - 1, n):
        SI_ = I[t - window + 1:t + 1].sum()
        SL = lam[t - window + 1:t + 1].sum()
        sh = a + SI_
        r = b + SL
        rows.append({
            'idx': t,
            'win_cases': SI_,
            'win_lam': SL,
            'Rt': sh / r,
            'lo': gammadist.ppf(.025, sh, scale=1 / r),
            'hi': gammadist.ppf(.975, sh, scale=1 / r),
            'p_gt1': 1 - gammadist.cdf(1, sh, scale=1 / r),
        })
    return pd.DataFrame(rows)


def runs(mask, minlen):
    """Index runs of True lasting at least minlen steps."""
    out = []
    st = None
    for i, v in enumerate(mask):
        if v and st is None:
            st = i
        if not v and st is not None:
            out.append((st, i - 1))
            st = None
    if st is not None:
        out.append((st, len(mask) - 1))
    return [(a, b) for a, b in out if b - a + 1 >= minlen]


# ----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_parquet(args.dataset)
    df['data_iniSE'] = pd.to_datetime(df['data_iniSE'])
    df = df.sort_values('data_iniSE').drop_duplicates('data_iniSE').reset_index(drop=True)

    r = cori(df.casos.to_numpy().astype(float), disc(2.0, 1.0), 7)
    r['week'] = df.data_iniSE.iloc[r.idx].values
    r['SE'] = df.SE.iloc[r.idx].values
    r['casos'] = df.casos.iloc[r.idx].values
    r['inc100k'] = df.p_inc100k.iloc[r.idx].values

    # ---- the archived filter: CALENDAR year of the week-start date ----------
    r25 = r[pd.to_datetime(r.week).dt.year == 2025].reset_index(drop=True)
    # ---- alternative: EPI-YEAR filter on the SE label -----------------------
    epi25 = r[(r.SE >= 202501) & (r.SE <= 202553)].reset_index(drop=True)

    out_csv = os.path.join(args.outdir, 'rt_weekly_reproduced.csv')
    r25.to_csv(out_csv, index=False)

    print('== FILTERING ==')
    print(f'dataset rows={len(df)} SE {df.SE.min()}-{df.SE.max()}')
    print(f'SE202501 in dataset: {bool((df.SE == 202501).any())} '
          f'(data_iniSE={df.loc[df.SE == 202501, "data_iniSE"].iloc[0].date() if (df.SE == 202501).any() else "n/a"})')
    print(f'calendar-year filter (archived): n={len(r25)} weeks, SE{int(r25.SE.iloc[0])}-{int(r25.SE.iloc[-1])}')
    print(f'epi-year filter SE202501-202553: n={len(epi25)} weeks, SE{int(epi25.SE.iloc[0])}-{int(epi25.SE.iloc[-1])}')
    print(f'excluded by calendar filter: {sorted(set(epi25.SE) - set(r25.SE))}')

    print()
    print('== INCIDENCE ==')
    print(f'2025 cases (calendar): {int(r25.casos.sum())}')
    print(f'2025 cases (epi-year) : {int(epi25.casos.sum())}')
    print(f'annual incidence: {r25.casos.sum() / 14230 * 100000:.1f} per 100k (pop 14230)')
    pk = r25.loc[r25.casos.idxmax()]
    print(f'peak week: SE{int(pk.SE)} ({pk.week.date()}) {int(pk.casos)} cases, {pk.inc100k:.1f}/100k')

    print()
    print('== THRESHOLD COUNTS ==')
    print(f'Rt>1 : {int((r25.Rt > 1).sum())} of {len(r25)}  (epi-year: {int((epi25.Rt > 1).sum())} of {len(epi25)})')
    print(f'lo>1 : {int((r25.lo > 1).sum())} of {len(r25)}')
    print(f'weeks with casos==0        : {int((r25.casos == 0).sum())}')
    print(f'windows with win_cases==0  : {int((r25.win_cases == 0).sum())} '
          f'(SE{int(r25.SE[r25.win_cases == 0].min())}-{int(r25.SE[r25.win_cases == 0].max())})')
    print(f'  -> in zero-case windows Rt drifts to prior mean (a+0)/(b+0)=5.0; '
          f'values {r25.loc[r25.win_cases == 0, "Rt"].min():.2f}-{r25.loc[r25.win_cases == 0, "Rt"].max():.2f}')

    print()
    print('== SUSTAINED-GROWTH RUNS (Rt>1 for >=3 weeks) ==')
    for a, b in runs(list(r25.Rt > 1), 3):
        print(f'  SE{int(r25.SE[a])}-{int(r25.SE[b])}: {b - a + 1} wks, '
              f'Rt {r25.Rt[a:b + 1].min():.2f}-{r25.Rt[a:b + 1].max():.2f}, '
              f'cases {int(r25.casos[a:b + 1].sum())}')
    print('== RUNS WITH LOWER 95% CREDIBLE BOUND > 1 (>=2 weeks) ==')
    for a, b in runs(list(r25.lo > 1), 2):
        print(f'  SE{int(r25.SE[a])}-{int(r25.SE[b])}: {b - a + 1} wks, '
              f'Rt {r25.Rt[a:b + 1].min():.2f}-{r25.Rt[a:b + 1].max():.2f}, '
              f'cases {int(r25.casos[a:b + 1].sum())}')

    print()
    print('== KEY WEEKS (week-level detail) ==')
    for s in (202538, 202539, 202540, 202541, 202542, 202543, 202553):
        row = r25[r25.SE == s]
        if len(row):
            row = row.iloc[0]
            print(f'  SE{s}: casos={int(row.casos)} win_cases={int(row.win_cases)} '
                  f'win_lam={row.win_lam:.6f} Rt={row.Rt:.4f} '
                  f'95%CrI=[{row.lo:.4f},{row.hi:.4f}]')

    print()
    print(f'max Rt: {r25.Rt.max():.4f} at SE{int(r25.loc[r25.Rt.idxmax(), "SE"])}')
    print(f'latest Rt: {r25.Rt.iloc[-1]:.4f} '
          f'[{r25.lo.iloc[-1]:.4f}, {r25.hi.iloc[-1]:.4f}] at SE{int(r25.SE.iloc[-1])}')
    print(f'\nwrote {out_csv}')


if __name__ == '__main__':
    main()
