# vMF kernel — Julia port

**Status: ✅ PASS** (verified 2026-08-20, Julia 1.12.7 via juliaup at `~/.juliaup/bin/julia`).

All 21 differential checks pass within SPEC §4 tolerances (A7 ≤ 1e-9, fit ≤ 1e-6,
edge ≤ 1e-6, n==30, saturated==false, real==false). Matches golden exactly:
kappa=9.032086, rho=0.708484, warmth=0.314092. Worst error 1.6e-14 (kappa).

Standard library only, no packages — JSON numbers are extracted with a small
Base-only regex scanner.

To run:

```sh
cd julia
julia test.jl
```

Exit code 0 on success.
