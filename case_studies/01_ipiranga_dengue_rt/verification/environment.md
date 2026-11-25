# Execution environment for the verification pass

Captured at run time from the sandbox interpreter that executed
`verification/code/*.py`. Reported by `platform`/`sys` and module `__version__`.

## Software

| Component | Version |
|---|---|
| Python | **3.12.16** |
| numpy | **2.5.5** |
| pandas | **2.3.3** |
| scipy | **1.18.1** |
| matplotlib | **3.11.2** |
| pyarrow | **26.0.1** |

Platform string:
`Linux-6.8.0-124-generic-x86_64-with-glibc2.41`

## Parquet engine

`pandas.read_parquet` requires a Parquet engine. In this environment it is
**pyarrow 26.0.1**. `../reproducibility/requirements.txt` did not list it; that omission
has been corrected — see the updated file. Without pyarrow (or fastparquet) the scripts
fail at the first `read_parquet` call.

## Determinism notes

- The estimator is closed-form (gamma posterior quantiles); there is no Monte Carlo
  sampling, so there is no random seed to fix.
- Numerical agreement between the archived estimator and the portable rewrite is at
  floating-point epsilon (max |ΔRt| = 1.78 × 10⁻¹⁵). Any re-run on a platform with the
  same scipy `gamma.ppf` implementation will agree to that order.
- The **figure** is not bit-reproducible across matplotlib versions: layout, font
  rasterisation and anti-aliasing vary. Reproducing byte-identical PNGs is not an
  achievable target and is not claimed here. The 900 × 1950 px geometry and the plotted
  data were reproduced; the title text differs by design (see `verification.md` §3).

## Version provenance honestly stated

These versions are those of the **verification** environment (2026-11-25, verification
pass). The versions used during the **original** investigation were not recorded anywhere
in the archive, and are therefore **unknown**. Do not present the table above as the
original environment.

## How to reproduce this environment

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r ../reproducibility/requirements.txt
python -c "import numpy,pandas,scipy,matplotlib,pyarrow; \
print(numpy.__version__, pandas.__version__, scipy.__version__, \
matplotlib.__version__, pyarrow.__version__)"
```
