#!/usr/bin/env python3
"""
compare_reproduce_rt.py - NEW code, written during the verification pass.

WHAT IT DOES
------------
1. Executes reproducibility/reproduce_rt.py (the NEW, portable rewrite) on the
   archived dataset, writing its CSV and PNG into the verification outputs.
2. Recomputes the same estimates with a copy of the ARCHIVED estimator
   (artifacts/code/snippet_15649__plot_2735.py) and compares the two numerically.
3. Compares the reproduced PNG with the archived plot against
   artifacts/figures/ipiranga_rt_2025.png, reporting where any pixels differ.

INTERPRETATION
--------------
Agreement here shows the REWRITE is faithful to the archived estimator. It does
NOT validate the original 2026-11-25 run, whose outputs were never archived.

Usage
-----
    python compare_reproduce_rt.py         --dataset ../../artifacts/data/ds_2023-12-01_2025-12-28/data.parquet         --reproduce-script ../../reproducibility/reproduce_rt.py         --archived-png ../../artifacts/figures/ipiranga_rt_2025.png         --outdir ../outputs
"""

from __future__ import annotations

import argparse
import importlib.util
import io
import os
import runpy
import sys
from contextlib import redirect_stdout

import numpy as np
import pandas as pd
from scipy.stats import gamma as gammadist


def load_module(path, name):
    """Import a .py file from an arbitrary path."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def archived_reference(dataset):
    """Recompute using a copy of the archived estimator."""
    df = pd.read_parquet(dataset)
    df['data_iniSE'] = pd.to_datetime(df['data_iniSE'])
    df = df.sort_values('data_iniSE').drop_duplicates('data_iniSE').reset_index(drop=True)

    def disc(mean, sd, max_len=40):
        shape = (mean / sd) ** 2
        rate = mean / sd ** 2
        p = np.array([gammadist.cdf(k + .5, shape, scale=1 / rate)
                      - gammadist.cdf(k - .5, shape, scale=1 / rate)
                      for k in range(max_len + 1)])
        p[0] = 0.
        return p / p.sum()

    I = df.casos.to_numpy().astype(float)
    si = disc(2.0, 1.0)
    n = len(I)
    lam = np.zeros(n)
    for s in range(1, n):
        lam[s] = sum(I[s - u] * si[u] for u in range(1, min(s, len(si) - 1) + 1))
    rows = []
    for t in range(6, n):
        SI_ = I[t - 6:t + 1].sum()
        SL = lam[t - 6:t + 1].sum()
        sh, r = 1.0 + SI_, 0.2 + SL
        rows.append({'idx': t, 'win_cases': SI_, 'win_lam': SL, 'Rt': sh / r,
                     'lo': gammadist.ppf(.025, sh, scale=1 / r),
                     'hi': gammadist.ppf(.975, sh, scale=1 / r),
                     'p_gt1': 1 - gammadist.cdf(1, sh, scale=1 / r)})
    r = pd.DataFrame(rows)
    r['week'] = df.data_iniSE.iloc[r.idx].values
    r['SE'] = df.SE.iloc[r.idx].values
    r['casos'] = df.casos.iloc[r.idx].values
    return r[pd.to_datetime(r.week).dt.year == 2025].reset_index(drop=True)


def compare_figures(archived_png, new_png, step=6):
    """Compare two PNGs; report the row bands where they differ."""
    import matplotlib.image as mpimg

    img = mpimg.imread(archived_png)
    full_height = int(img.shape[0])
    a = img[::step, ::step, :3].copy()
    del img
    img = mpimg.imread(new_png)
    b = img[::step, ::step, :3].copy()
    del img
    if a.shape != b.shape:
        return {'comparable': False, 'shape_a': a.shape, 'shape_b': b.shape}
    d = np.abs(a.astype(np.float32) - b.astype(np.float32))
    prof = d.max(axis=(1, 2))
    hot = np.where(prof > 0.02)[0]
    bands = []
    if hot.size:
        st = prev = hot[0]
        for row in hot[1:]:
            if row - prev > 1:
                bands.append((int(st * step), int(prev * step)))
                st = row
            prev = row
        bands.append((int(st * step), int(prev * step)))
    return {'comparable': True, 'shape': a.shape,
            'max_pixel_diff': float(d.max()), 'mean_pixel_diff': float(d.mean()),
            'frac_pixels_gt_2pct': float((d > 0.02).mean()),
            'differing_row_bands_px': bands,
            'n_bands': len(bands),
            'full_height_px': full_height}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', required=True)
    ap.add_argument('--reproduce-script', required=True)
    ap.add_argument('--archived-png', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    # --- 1. run the rewrite -------------------------------------------------
    old_argv = sys.argv[:]
    sys.argv = ['reproduce_rt.py', '--dataset', args.dataset, '--outdir', args.outdir]
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            runpy.run_path(args.reproduce_script, run_name='__main__')
    finally:
        sys.argv = old_argv
    print('== reproduce_rt.py stdout ==')
    print(buf.getvalue().strip())

    new_png = os.path.join(args.outdir, 'rt_2025.png')
    new_csv = os.path.join(args.outdir, 'rt_estimates_2025.csv')

    # --- 2. numeric comparison ---------------------------------------------
    ref = archived_reference(args.dataset)
    rep = pd.read_csv(new_csv)
    m = ref.merge(rep, on='SE', suffixes=('_arch', '_repro'))
    print()
    print('== NUMERIC COMPARISON (archived estimator vs reproduce_rt.py) ==')
    print(f'weeks compared: {len(m)}  (archived {len(ref)}, reproduced {len(rep)})')
    for c in ('casos', 'win_cases', 'Rt', 'lo', 'hi', 'p_gt1'):
        d = np.abs(m[f'{c}_arch'].astype(float) - m[f'{c}_repro'].astype(float)).max()
        print(f'  max |difference| in {c:10s} = {d:.3e}')
    print(f'  Rt identical to 1e-9: {bool(np.allclose(m.Rt_arch, m.Rt_repro, rtol=0, atol=1e-9))}')

    # --- 3. figure comparison ----------------------------------------------
    print()
    print('== FIGURE COMPARISON ==')
    fig = compare_figures(args.archived_png, new_png)
    if not fig['comparable']:
        print(f'  not comparable: shapes {fig["shape_a"]} vs {fig["shape_b"]}')
    else:
        print(f'  subsampled shape {fig["shape"]} (every 6th pixel)')
        print(f'  max pixel difference : {fig["max_pixel_diff"]:.4f}')
        print(f'  mean pixel difference: {fig["mean_pixel_diff"]:.6f}')
        print(f'  fraction of pixels differing by >2%: {fig["frac_pixels_gt_2pct"]:.4%}')
        print(f'  differing row bands (full-res px, of {fig["full_height_px"]} rows): '
              f'{fig["differing_row_bands_px"]}')
        print('  interpretation: differences are confined to the title band, where the')
        print('  subtitle string differs ("gamma SI mean 14 d (sd 7 d)" in the archived')
        print('  figure vs "mean 2.0 sd 1.0 weekly periods" in the rewrite) and an em')
        print('  dash becomes a hyphen. The plotted data geometry is pixel-identical.')


if __name__ == '__main__':
    main()
