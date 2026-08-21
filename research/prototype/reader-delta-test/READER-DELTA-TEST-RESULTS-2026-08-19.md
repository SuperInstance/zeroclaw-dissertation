# Reader-Delta Test — Results (the pre-registered three-clause test)

**Date:** 2026-08-19 · **Artifacts:** `build_fixtures.py`, `run_test.py`, `fixtures/`, `results.json` (this directory) · **Data:** elephant nights, read-only (elephant repo verified clean post-run)

Registered in `research/skills/devils-advocate-regress.md` (clauses 1–2 + kill condition), amended by `research/skills/zeroclaw-response-rival-a.md` (clause 3: cross-strata transfer), framed by `research/skills/zeroclaw-response-devil-head.md` (§2: D″ fixtures) and `devils-advocate-head-verdict.md` §5 ("still unrun — still the ballgame"). This is that test, run.

---

> **ANNOTATION (2026-08-21) — superseded by the Switch Test fold (d59bf17, NO CLEAN WIN).**
> The registered, SHA-verified results below are **not deleted or altered**; they stand as filed. But the status they carried on 2026-08-19 — "second-order beats first-order; the second-order object is not a reindex" — was **downgraded** the same evening by the Switch Test (`research/skills/zeroclaw-switch-verdict.md`, folded at d59bf17): the drift-reader failed its own registered detection threshold (0.467 vs 0.80); a static per-nurse median — no temporal structure at all — beat it on switch localization (r 0.816/0.800 vs 0.435/0.467); the classification edge is pre-switch only; noise robustness is absent at σ=0.2; the salvageable kernel is mean-moving regimes only (localization r = 0.787).
> The operative framing today: **reader-delta = mean-shift, baseline-relative delta — it reads the step, not the change-of-reading.** "Second-order" survives only as the structural term for baseline-relativity. These D″ fixtures instantiate the doctrine's *premise* (idiosyncratic baselines); the Switch Test tested the object's temporal claim and found no clean win. Read every "second-order" below with this header.

---

## 1. D″ fixtures — what was built

**Shared room corpus (real data):** all 5 nights (A, B, C, D, D-cold), non-overlapping windows of W=8 speaks → **T = 27 windows**. Room stimulus m(t) = mean `field_raw_after` over the window. SEG1 = warm (first 20 speaks), SEG2 = cynical — per night, as in `reader_delta.py`.

**N = 13 synthetic nurses** (reader models). Pool = 12 (4 sauna + 4 jaded + 4 over); the **13th nurse is held out of all clustering** (her class — jaded — was drawn by the seeded RNG before any evaluation; the full 13-fold leave-one-out is also run, so nothing is cherry-picked).

Each nurse's emitted reading of window t, from her own planted reader model only:

```
r_i(t) = clip( h_i + g_i(t)·(m(t) − h_i) + α_i·t̂·u_i + η, −0.05, 1.7 )
```

- `h_i` — idiosyncratic home baseline, drawn **class-independently** from the corpus field distribution
- `g_i(t)` — planted adoption-gain trajectory: **sauna** decays 0.85–0.95 → 0.10–0.20 (warms less and less); **jaded** flat 0.06–0.14 (barely moves); **over** rises 0.25–0.35 → 0.95–1.15 (overshoots; g>1 extrapolates past the room)
- `α_i·t̂·u_i` — directional drift: **random direction** per nurse (class-independent), class-specific amount (sauna 0.04–0.08, jaded 0–0.015, over 0.02–0.05)
- `η` — per-window reading noise, σ_i ~ U(0.010, 0.020) per dim

**Honest premise, stated up front (the fifth-laundering guard):** these fixtures *instantiate the doctrine's premise* — every reader has an idiosyncratic baseline (`h_i`), independent of her drift class. The kill question is then exactly the registered one: *given* that premise, does knowing the model (baseline + delta) beat reading the output? If real readers' baselines do not vary idiosyncratically, this result does not transfer. The premise is the doctrine's, not a rigged deck — but it is a premise, and the committee should read it as such.

**Determinism:** single seeded RNG (SEED=20260819), fixed draw order, canonical JSON. `FIXTURES-SHA256 = a423a3783a4a303f281e419d28359844990bcf312955a9eb18e636f753d56429`. Full-pipeline canonical results hash, 3/3 replays:

```
replay 1/3: 6317001c11e38c588c56a4be02e5067720b20a8fa1c69e501d7c74d59b484239
replay 2/3: 6317001c11e38c588c56a4be02e5067720b20a8fa1c69e501d7c74d59b484239
replay 3/3: 6317001c11e38c588c56a4be02e5067720b20a8fa1c69e501d7c74d59b484239
REPLAYS_IDENTICAL_3_OF_3: True
```

(A nondeterminism bug — `max(set(...))` tie-breaks under PYTHONHASHSEED — was found during verification and fixed with deterministic tie-breaking before these numbers were taken. The k-means delta partition is also stable across 10 re-seeded inits: min purity 1.000.)

## 2. The two representations

**Reader-delta (second-order), output-only.** From each nurse's emitted readings alone: fitted baseline b̂ᵢ = componentwise median of her own readings; δᵢ(t) = rᵢ(t) − b̂ᵢ; normalized excursion eᵢ(t) = ‖δᵢ(t)‖/(‖b̂ᵢ‖+ε). Feature vector = [eᵢ(0…26), slope(eᵢ), mean(eᵢ), std(eᵢ), lag-1 autocorr(δᵢ)] — the doctor's three reads: displacement-from-baseline per window, tempo, volatility. **No room input is ever touched.** (Feature standardization is fitted on the 12 pool nurses, applied to the held-out — no leakage.) *(2026-08-21: per d59bf17 this object is a mean-shift, baseline-relative delta — it reads the step, not the change-of-reading.)*

**First-order (kill baseline).** Plain similarity of the readings themselves: concatenated rᵢ(t) (7×27 dims), no baseline model, no centering. Three *strengthened* first-order ablations reported in the open: cosine-normalized; per-nurse centered (the "smuggled baseline"); and per-window reading-norm trajectory ‖rᵢ(t)‖ (magnitudes only, still baseline-free) — so the kill comparison is against the *best* first-order, not a strawman.

## 3. Clause 1 — blind discrimination (threshold: purity ≥ 2× noise floor, 3/3 replays, held-out nurse)

Unsupervised k-means (k=3, seeded, n_init=25). Noise floor = median purity of 1000 seeded label-permutations of the same partition (p95 = 0.667 also reported).

| representation | purity | ratio vs floor (median 0.500) | 1-NN retrieval (chance 0.273) |
|---|---|---|---|
| **reader-delta** | **1.000** | **2.00×** | **1.000 (3.7× chance)** |
| first-order (plain) | 0.583 | 1.17× | 0.583 |
| first-order centered (ablation) | 0.583 | 1.17× | 0.750 |
| first-order cosine (ablation) | 0.667 | 1.33× | 0.750 |
| first-order norm-traj (ablation) | 0.667 | 1.33× | 0.750 |

**Threshold note, in the open:** purity is bounded above by 1.0, so the registered "≥2× noise floor" against the median floor (2×0.500 = 1.000) is met *exactly*, and no bounded metric could satisfy 2×p95 (=1.333). The floor construction follows the deadman's (baseline value × 2), and both floors are printed here for the committee to re-weight.

**Held-out 13th nurse** (never in any clustering): nurse-13, planted jaded, nearest-centroid votes {jaded: 4, sauna: 0, over: 0} → **correct**. **13-fold leave-one-out: 13/13 (1.000).**

**Clause 1 verdict: PASS** (delta: 1.000 = 2.0× floor; first-order best: 0.667 = 1.33× floor — fails threshold).

## 4. Clause 2 — calibration (the D″): d′ of the reader-delta index

Pre-registered scalar indices from the reader-delta representation: **DI** = OLS slope of e(t) (drift tempo), **MI** = mean e (drift amount). d′ per planted class-pair, pooled-SD form (n = 5 jaded incl. held-out, 4 sauna, 4 over), plus 2-D Mahalanobis d′ on (DI, MI):

| class-pair | d′(DI) | d′(MI) | d′ (Mahalanobis) |
|---|---|---|---|
| sauna vs over | −12.28 | −6.65 | 13.24 |
| sauna vs jaded | −20.27 | +17.30 | 26.76 |
| jaded vs over | −7.52 | −13.02 | 13.95 |
| **aggregate (mean Mahalanobis)** | | | **17.99** |

Signs are meaningful (sauna drifts down in tempo, jaded lowest in amount, etc.). **Calibration delivered:** every class-pair separates at |d′| ≥ 6.6; the aggregate d′ = 17.99 with per-pair values is a *measured* sensitivity, not a felt one. Caveat stated plainly: d′ this large is a property of synthetic fixtures with planted separation and modest noise; on real per-reader logs the same machinery should be expected to yield single-digit d′ at best. The deliverable is the calibrated index, not the magnitude.

## 5. Clause 3 — cross-strata transfer (Rival A's clause)

From **SEG1 (warm) outputs only**: ê1 = mean excursion, slope1 = within-SEG1 slope of e. Predict **SEG2 (cynical) behavior**, leave-one-nurse-out (13-fold):

- **Numeric transfer:** LOO linear regression ê2 ~ [1, ê1, slope1] → **r = 0.967, MAE = 0.0206 vs chance-MAE 0.0924 (4.5× better), R²_LOO = 0.943**.
- **Class transfer:** nearest class-centroid in (ê1, slope1) space → **13/13 (1.000)** vs chance 1/3.
- **First-order's best attempts at the same question** (label-borrowing; it has no drift parameter to transfer):
  - 1-NN on SEG1 raw readings: **11/13 (0.846)** — misses nurse-08 (sauna→over), nurse-12 (jaded→sauna)
  - 3-NN: 9/13 (0.692)
  - 1-NN on SEG1 norm trajectory (strongest baseline-free variant): **12/13 (0.923)** — misses nurse-01 (jaded→sauna)

Honest reading: because all nurses read the *same* rooms, raw magnitude levels are partially cross-nurse comparable, and the strongest baseline-free variant gets close on *labels* (12/13 vs 13/13). What first-order cannot do at any accuracy is the registered question itself: it has no per-nurse baseline, hence no excursion, hence no drift estimate — it cannot *predict how far the nurse will move in SEG2* (its best numeric act is the chance-MAE mean, 0.0924). The second-order representation poses and answers the numeric question (r = 0.967). **Clause 3: PASS for the reader-delta representation; first-order fails the numeric form and loses the label form (12/13 vs 13/13).** *(Annotation: this PASS stands on these D″ fixtures; the Switch Test (d59bf17) later bounded the object — the transfer reads mean-moving regimes, not re-phasing ones — see header.)*

## 6. Kill condition — the head-to-head

The registration: if first-order performs *as well as* reader-delta on clause 1, the second-order object is a reindex and the doctrine collapses. *(Annotation: on these D″ fixtures the reindex kill does not fire — that verdict stands as filed; the Switch Test (d59bf17) found a different, bounded miss instead, detailed in the header.)*

- reader-delta: purity **1.000**, retrieval **1.000**
- best first-order (of four variants, including the two strongest ablations): purity **0.667**, retrieval **0.750**

**The kill condition does not fire.** First-order fails the registered threshold by a wide margin (0.667 vs required ≥1.000-equivalent 2×floor; the gap is 4 misclustered nurses).

**The ablations also locate *where* the information lives — and it is not where a lazy version of the doctrine would put it.** Per-nurse *centering* alone (the smuggled baseline) does NOT recover the classes (0.583). The operative second-order object is the **displacement-magnitude trajectory** — ‖r − b̂‖ per window, its tempo and volatility — not baseline removal per se. The doctor reads the *size of the step from her own baseline*, not the step's direction, not the raw notes. (The thesis's own earlier line — "the felt size of the step is the reader's" — is what survived this test.) *(Annotation: this surviving reading is exactly the downgraded object — mean-shift, baseline-relative, reads the step, not the change-of-reading — per d59bf17.)*

## 7. Verdict

**On the D″ fixtures — which instantiate the doctrine's premise of idiosyncratic reader baselines — second-order beats first-order (clause 1: 1.000 vs 0.667 purity against a 2×-floor threshold of 1.000; clause 2: aggregate d′ 17.99; clause 3: 13/13 and r = 0.967 vs 12/13 label-borrowing with no numeric capability); the second-order object is not a reindex.** *(Verdict bound to these fixtures and to the conditional premise — as filed; the Switch Test (d59bf17, NO CLEAN WIN) later downgraded the object's temporal claim, per the annotation header.)*

## 8. Honest limits (for the committee)

1. **Synthetic fixtures instantiate the doctrine's premise.** Idiosyncratic, class-independent baselines are *assumed*, not found. If real readers' baselines are not idiosyncratic, first-order may do fine there, and this result will not transfer. The test settles the *conditional* claim: given the premise, knowing the model beats reading the output.
2. **The fixtures' drift lives in gain trajectories**, which modulate excursion magnitude; representations that track magnitudes (delta) are favored by construction over direction-sensitive ones. The centered ablation (0.583) shows it is not *merely* level-removal, but the committee should note the design choice.
3. **d′ magnitudes are synthetic-curve numbers**; the machinery (per-pair calibrated sensitivity) is the deliverable.
4. **Clause 3's first-order norm-traj variant reached 12/13** on labels. The doctrine's clause-3 margin on labels is one nurse; the decisive margin is the numeric prediction (impossible without a baseline), which the report states rather than hides.
5. Purity's ceiling makes "2× median floor" exactly attainable and "2× p95" unattainable for *any* representation; both floors are reported so the committee can apply its own weight.

## 9. Reproduce

```bash
cd research/prototype/reader-delta-test
python3 build_fixtures.py          # writes fixtures/ + FIXTURES-SHA256 (a423a378…)
python3 run_test.py run            # full three-clause run → results.json numbers
python3 run_test.py --verify-replay  # 3/3 identical: 6317001c11e38c58…
```

Elephant nights were read from `/home/eileen/projects/elephant/data/nights` and never written; the runner re-verifies the corpus against the live data on every run and asserts equality. numpy + stdlib only; no torch, no GPU, no sklearn.
