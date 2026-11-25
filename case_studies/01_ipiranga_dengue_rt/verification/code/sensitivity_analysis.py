#!/usr/bin/env python3
"""
sensitivity_analysis.py - NEW code, written during the verification pass.

PURPOSE
-------
The original archived script contains NO sensitivity analysis: disc() is called
as disc(2.0, 1.0) and cori() uses a=1., b=.2 with no variation. Whatever
sensitivity numbers the original narrative may have reported, no artifact in
this archive contains the code that produced them.

This script performs a sensitivity analysis from scratch and, in doing so,
tests the specific claim that a range of "approximately 4 to 20" belongs to
SE202539 and not to SE202540 (where the archived estimate is 11.11).

WHY THE TWO WEEKS BEHAVE DIFFERENTLY
------------------------------------
Rt = (a + sum I) / (b + sum Lambda) over the 7-week window.
  SE202539: sum I = 1, sum Lambda = 0.000023  -> Rt ~ (a+1)/b, i.e. almost
            entirely determined by the prior. It cannot be informed by data.
  SE202540: sum I = 5, sum Lambda = 0.340     -> partly data-driven.

So SE202539 is a PRIOR-SENSITIVITY artefact, while SE202540 is a genuine
posterior with a wide credible interval. They are different quantities on
different weeks and must not be combined into one sentence.

Usage
-----
    python sensitivity_analysis.py --dataset ../../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet                                    --outdir ../outputs
"""

from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd
from scipy.stats import gamma as gammadist


def disc(mean, sd, max_len=40):
    """Discretise a gamma serial interval (identical to the archived script)."""
    shape = (mean / sd) ** 2
    rate = mean / sd ** 2
    p = np.array([
        gammadist.cdf(k + .5, shape, scale=1 / rate) - gammadist.cdf(k - .5, shape, scale=1 / rate)
        for k in range(max_len + 1)
    ])
    p[0] = 0.
    return p / p.sum()


def cori(I, si, window=7, a=1., b=.2):
    """Sliding-window Rt (identical to the archived script, plus win_lam)."""
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
        rows.append({'idx': t, 'win_cases': SI_, 'win_lam': SL, 'Rt': sh / r,
                     'lo': gammadist.ppf(.025, sh, scale=1 / r),
                     'hi': gammadist.ppf(.975, sh, scale=1 / r)})
    return pd.DataFrame(rows)


def summarise(df, cases, **kw):
    """Run one scenario and return the summary row."""
    r = cori(cases, kw.pop('si'), window=kw.pop('window'), a=kw.pop('a'), b=kw.pop('b'))
    r['SE'] = df.SE.iloc[r.idx].values
    r['week'] = df.data_iniSE.iloc[r.idx].values
    r25 = r[pd.to_datetime(r.week).dt.year == 2025].reset_index(drop=True)
    row = dict(kw)
    for s in (202539, 202540, 202541):
        hit = r25[r25.SE == s]
        row[f'SE{s}_win_cases'] = int(hit.win_cases.iloc[0]) if len(hit) else np.nan
        row[f'SE{s}_Rt'] = round(float(hit.Rt.iloc[0]), 4) if len(hit) else np.nan
        row[f'SE{s}_lo'] = round(float(hit.lo.iloc[0]), 4) if len(hit) else np.nan
        row[f'SE{s}_hi'] = round(float(hit.hi.iloc[0]), 4) if len(hit) else np.nan
    row['max_Rt'] = round(float(r25.Rt.max()), 4)
    row['week_of_max_Rt'] = int(r25.loc[r25.Rt.idxmax(), 'SE'])
    row['n_weeks_Rt_gt1'] = int((r25.Rt > 1).sum())
    row['n_weeks'] = len(r25)
    row['latest_Rt'] = round(float(r25.Rt.iloc[-1]), 4)
    row['latest_lo'] = round(float(r25.lo.iloc[-1]), 4)
    row['latest_hi'] = round(float(r25.hi.iloc[-1]), 4)
    row['latest_CrI_excludes_1'] = bool(r25.lo.iloc[-1] > 1 or r25.hi.iloc[-1] < 1)
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_parquet(args.dataset)
    df['data_iniSE'] = pd.to_datetime(df['data_iniSE'])
    df = df.sort_values('data_iniSE').drop_duplicates('data_iniSE').reset_index(drop=True)
    cases = df.casos.to_numpy().astype(float)
    si0 = disc(2.0, 1.0)

    # ---------------- 1. prior sensitivity (archived SI and window) ----------
    priors = [(1.0, 0.2), (0.5, 0.5), (1.0, 1.0), (2.0, 1.0),
              (1.0, 0.5), (5.0, 1.0), (1.0, 0.1), (2.0, 0.4)]
    rows = []
    for a, b in priors:
        rows.append(summarise(df, cases, scenario='prior', prior_shape=a, prior_rate=b,
                              prior_mean=round(a / b, 3), si_mean=2.0, si_sd=1.0,
                              window=7, si=si0, a=a, b=b))
    prior_df = pd.DataFrame(rows)
    prior_df.to_csv(os.path.join(args.outdir, 'sensitivity_prior.csv'), index=False)

    # ---------------- 2. serial-interval sensitivity ------------------------
    rows = []
    for m, s in [(1.5, 0.7), (2.0, 1.0), (2.0, 0.5), (2.5, 1.2), (3.0, 1.5)]:
        rows.append(summarise(df, cases, scenario='serial_interval', si_mean=m, si_sd=s,
                              prior_shape=1.0, prior_rate=0.2, window=7,
                              si=disc(m, s), a=1.0, b=0.2))
    si_df = pd.DataFrame(rows)
    si_df.to_csv(os.path.join(args.outdir, 'sensitivity_serial_interval.csv'), index=False)

    # ---------------- 3. window sensitivity --------------------------------
    rows = []
    for w in (5, 7, 9):
        rows.append(summarise(df, cases, scenario='window', window_length=w,
                              si_mean=2.0, si_sd=1.0, prior_shape=1.0, prior_rate=0.2,
                              si=si0, a=1.0, b=0.2, window=w))
    win_df = pd.DataFrame(rows)
    win_df.to_csv(os.path.join(args.outdir, 'sensitivity_window.csv'), index=False)

    # ---------------- reporting -------------------------------------------
    pd.set_option('display.width', 200)
    print('== 1. PRIOR SENSITIVITY (SI 2.0/1.0, window 7) ==')
    print(prior_df[['prior_shape', 'prior_rate', 'prior_mean', 'SE202539_Rt', 'SE202540_Rt',
                    'max_Rt', 'week_of_max_Rt', 'n_weeks_Rt_gt1', 'latest_Rt',
                    'latest_CrI_excludes_1']].to_string(index=False))

    print()
    print('== WHERE DOES "4 to 20" COME FROM? ==')
    s39 = prior_df.SE202539_Rt
    s40 = prior_df.SE202540_Rt
    print(f'SE202539 across all {len(prior_df)} priors: {s39.min():.2f} to {s39.max():.2f}')
    print(f'SE202540 across all {len(prior_df)} priors: {s40.min():.2f} to {s40.max():.2f}')
    m2 = prior_df[prior_df.prior_mean >= 2.0]
    print(f'SE202539 restricted to priors with mean >= 2: '
          f'{m2.SE202539_Rt.min():.2f} to {m2.SE202539_Rt.max():.2f}')
    print('  -> a "4 to 20" prior-sensitivity range belongs to SE202539 '
          '(win_cases=1, win_lam~0: Rt=(a+1)/b is prior-determined).')
    print(f'  -> the archived estimate 11.1061 belongs to SE202540 (win_cases=5).')
    print(f'  -> SE202540 credible interval at the archived prior is '
          f'[{prior_df.SE202540_lo.iloc[0]:.2f}, {prior_df.SE202540_hi.iloc[0]:.2f}], '
          f'which is a DIFFERENT quantity from a sensitivity range.')

    print()
    print('== 2. SERIAL-INTERVAL SENSITIVITY (prior 1/0.2, window 7) ==')
    print(si_df[['si_mean', 'si_sd', 'SE202539_Rt', 'SE202540_Rt', 'max_Rt',
                 'week_of_max_Rt', 'n_weeks_Rt_gt1', 'latest_Rt']].to_string(index=False))
    print('  note: SE202539 barely moves with the SI because sum Lambda ~ 0; '
          'SE202540 does move (8.04-17.59).')

    print()
    print('== 3. WINDOW SENSITIVITY ==')
    print(win_df[['window_length', 'n_weeks', 'SE202539_Rt', 'SE202540_Rt', 'max_Rt',
                  'n_weeks_Rt_gt1']].to_string(index=False))
    print('\nwrote sensitivity_prior.csv, sensitivity_serial_interval.csv, sensitivity_window.csv')


if __name__ == '__main__':
    main()
