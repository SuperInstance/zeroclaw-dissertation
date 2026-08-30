# 05 — Coordinate-quote check (settles rival objections O2/O3 on the record)

**Run:** candidate lane (GLM-5.3), 2026-08-29 evening, seed 20260829, N = 200,000 draws from the pinned generator's parameter distribution (`build_switches.py`): α ~ U[0.005, 0.020], u = normalized 7-dim Gaussian (uniform on the sphere), σ ~ U[0.010, 0.020] per dim.

```python
import numpy as np
rng = np.random.default_rng(20260829)
N = 200000
alpha = rng.uniform(0.005, 0.020, N)
u = rng.normal(0,1,(N,7)); u /= np.linalg.norm(u,axis=1,keepdims=True)
perdim = alpha[:,None]*np.abs(u)          # per-dim total drift over the trajectory
sigma = rng.uniform(0.010,0.020,N)
maxdim = perdim.max(axis=1)
# results:
# max per-dim total drift: median 0.0083, p95 0.0139, p99 0.0159, absmax 0.0193
# share of draws with max-dim drift > own per-window sigma: 0.071
# RMS per-dim drift (the alpha/sqrt7 quote): median 0.0047
c = 13.5/26.0                              # mean t-hat contrast between the two segments, T=27
cd = c*perdim                              # drift contribution to segment-mean contrast, per dim
cn = sigma*np.sqrt(2/13)                   # contrast noise sd, per dim
# share max-dim drift-contrast > contrast-noise sd: 0.237
vecd = np.linalg.norm(c*alpha[:,None]*u,axis=1)
vecn = np.sqrt(7)*cn
# share ||drift contrast|| > ||contrast noise|| (vector-norm quote): 0.000
```

## Findings (what each quote says)

1. **The α/√7 ≈ 0.0076 figure in the morning document and v3.0 §1.2 is an RMS per-dimension quote, not an upper bound.** Max-coordinate drift: median 0.0083, p95 0.0139, absolute max 0.0193 (≈ α_max). **7.1% of draws have some dimension whose total drift exceeds that nurse's own per-window noise sd.** Rival O3 sustained: "for every realized nurse, by construction" is false in the coordinate quote.
2. **At the two-segment localizer's own grain (segment-mean contrast), the naive per-dim comparison is also not uniformly sub-floor:** 23.7% of draws exceed the per-dim contrast noise sd. Rival O2 sustained against v3.0's cross-grain phrasing.
3. **In the vector-norm quote — the drift-reader's actual reading grain (its statistic is the displacement magnitude ‖r − b̂‖ in 7-dim) — the channel is sub-floor on every one of 200,000 draws** (0 exceedances; equality only at the parameter corner c·α = √7·σ_min·√(2/13) ≈ 0.0104). The full-vector drift contrast never exceeds the full-vector contrast noise.

## The corrected sub-floor statement (feeds v3.1 §1.2′)

The quote book closes only per quote: **closed in the RMS and vector-norm quotes (the reader's own grain); open in the per-dimension worst-case quote (7.1% of draws exceed per-window σ; 23.7% exceed per-dim contrast sd).** The empirical decider for the coordinate tail is the pipeline's own permutation floor (which prices whatever the coordinate draws do — and did: no second-order signal survived, counterfactual rate 0.497 ≈ chance), and the prospective decider is XP-1 (ZC-C2/ZC-C3).
