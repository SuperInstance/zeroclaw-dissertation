# vMF kernel — R port

**Status: ✅ PASS** (verified 2026-08-20, R 4.6.1 via micromamba/conda-forge at
`~/micromamba-envs/r/bin/Rscript`).

All 21 differential checks pass within SPEC §4 tolerances (A7 ≤ 1e-9, fit ≤ 1e-6,
edge ≤ 1e-6, n==30, saturated==false, real==false). Matches golden exactly:
kappa=9.032086, rho=0.708484, warmth=0.314092. Worst error 3.0e-13 (A7(0.7)).

Base R only, no packages — JSON numbers are extracted with a small base-R regex
scanner.

To run:

```sh
cd r
Rscript test.R
```

Exit code 0 on success.
