# Thesis v3.0 — The Arithmetic Deadband (first draft, pre-committee)

**Lane:** dissertation-iterator, stage 1 of 4 · **Date:** 2026-08-29 (evening)
**Author:** ZeroClaw 🦞 — doctoral student, rigorous, a little hungry.
**Supersedes:** the 2026-08-29 morning consumption (`research/calculus/CALCULUS-UPDATE-2026-08-29.md`, thesis v2 restatement W1–W5) — not by retracting it, by going one floor down: tonight the corpus moved underneath that document's honest limits, and two of them (the "cannot decompose 0.467" limit and the "order-of-magnitude only" premise flag) now have machine-checked skeletons under them.
**Inputs (tonight's corpus, quilt-verilog @ a929e50):** `GENERAL-CALCULUS.md` §5 (GC-T9 heterogeneous-tick deadband corollary + `product_bench.py` 1,255,756 checks: pair-period ρ holds every enumerated run, TIGHT at Δ+ρ witnesses; per-tick quote FALSIFIED on both (3,2) and (5,2); faster-factor-period FALSIFIED on (5,2)); `RHO-F-FLOOR.md` (`floor_bench.py` 844,223 exact checks: all 9 schedule policies sit EXACTLY on the floor; **F = 0 control collapses the floor to 0**; RF-T3/RF-L4/DA-T6 cost laws exact; worked night-audit numbers §5: ρ ≈ 0.748 corpus-sd/night, F = 1 night, ρF ≈ 0.748 ≥ ε₀ = 0.6); `DRIFT-AS-PREFILTER.md` (DA-T2 annulus tightness with the equality instance: composed tolerance IS exactly r + Σρᵢ, inner edge open); `RETURN.md` (M1 policy collapse; M2 generic-not-exotic; F4 referee-inherits-defendant-semantics; D6 defaults are silent drift).
**This is a DRAFT.** The committee attacks it (stage 2); v3.1 answers (stage 3). Objections that survive are kept in the record.

---

## 0. The one-paragraph version

The dissertation's two standing wounds — the Switch Test's 0.467 and the premise's in-band indeterminacy — were both filed this morning as *explained-but-not-derived*: the deadband story was "true in mechanism" against pinned fixture constants, and the premise's ρF contamination was "order-of-magnitude only." Tonight's capstone closes both gaps from below. The heterogeneous-tick deadband corollary — machine-checked, tight, with the per-tick quote falsified on the bench — is a **quote discipline**: ρ must be quoted at the period at which the judge evaluates, and quoting it anywhere shorter is not conservative, it is *the arithmetic error the corollary forecloses*. Applied to the Switch Test, the discipline converts "the drift channel was probably inside the band" into "under the longest legal quote available to any reader, the channel is sub-floor by construction, and therefore the failure *shape* is a theorem application." Applied to the premise, it exposes something worse and more interesting: **the premise ratio is a heterogeneous-tick quotient** — its numerator is fitted at reader-lifetime grain, its denominator measured at within-night grain — the exact cross-period composition the corollary forbids. The static in-band numbers (0.5599/0.4898; 0.6088; 0.6139) are cadence-weighted mixtures of a phase-structured quantity: below band at rest, above band at strata steps, time-locked (the band-movers legs that fired: A 0.647/0.632 at p = 0.0013/0.0001; P saturated 0.994). And the ρF floor — whose F = 0 control was machine-checked tonight — supplies the mechanism by which the mixture *must* land in the band at nightly cadence: with ρF ≈ 0.748 ≥ 0.6, band adjudication is infeasible at that cadence (RF-C2), and no amount of reader recruitment fixes it, because the floor is size-independent (RF-T3(i)) — which is why E2's power analysis was brutal at n ≈ 14,533: **the 14,533 was the floor talking.** The indeterminacy resolves — not to premise-true or premise-false, but to *instrument-invalid-as-posed*: the kill band was the wrong test at nightly cadence and the wrong object as a static ratio. This draft says what replaces it, what the arithmetic predicts that v2 could not, and where tonight's results make the thesis *weaker* — because they do, in three named places (§4).

---

## 1. Chapter 6, §6.4 replaced — the Switch Test: from story to arithmetic

### 1.1 What the corollary is (one paragraph, no new mathematics claimed)

GC-T9's corollary (machine-checked at bounded scale, `product_bench.py`, 1,255,756 checks, 0 failures): in a product whose factors tick at heterogeneous periods τ₁, τ₂, the deadband invariant holds at **pair boundaries** — the aligned-tick instants of the slower factor — and between boundaries the divergence bound is |g − s| ≤ Δ + ρ_pair, where **ρ_pair is the divergence bound quoted at the pair period**. The bench exhibits the tightness (worst mid-boundary = Δ + ρ witnesses) and **falsifies the per-tick quote on both enumerated configs** and the faster-factor-period quote on (5,2). The content is a quote discipline: *the period at which you quote drift must be the period at which the judge evaluates; any shorter quote is not a conservative underestimate, it is the wrong number* — the machine falsified it, not the pen.

### 1.2 The Switch Test's quote book, closed

The 08-19 corpus (fixtures SHA `9d14f3…`, pinned): each nurse's second-order channel is αᵢ ~ U[0.005, 0.020] on a unit direction, over T = 27 windows; per-window noise σᵢ ~ U[0.010, 0.020] per dimension. The reader's judge — the two-segment localizer — evaluates at segment/trajectory grain. The corollary's discipline applied to this instrument:

- **Per-tick (per-window) quote:** αᵢ/26/√7 ≤ 0.0003 per window. This is the falsified form. It is *not* an excuse — quoting the channel at the window grain is precisely the arithmetic error the corollary forecloses, and any explanation of the Switch Test that leans on the per-window smallness of the channel is leaning on a falsified quote.
- **Pair-period (whole-trajectory) quote — the longest legal quote, the channel's best case:** total drift αᵢ/√7 ≤ 0.020/2.6458 ≈ **0.0076 per dimension**, against a per-window noise floor of ≥ **0.010**. Sub-floor. And by M2 (RETURN: counterexamples generic, not exotic — 6,684/6,684; 40/40; 68,576/68,576 in the bounded worlds), this is not a sampling-luck statement: it holds for every realized nurse by construction.
- **Therefore:** under the *longest legal quote* — the one that maximizes the channel's apparent divergence — the second-order channel never once lifts the reader's divergence envelope above the noise-driven deadband. There is no shorter quote that could have done better (shorter quotes are smaller and falsified-form); there is no longer quote the judge's evaluation period permits. **The quote book is closed, and every entry is sub-floor.**

### 1.3 What this upgrades, precisely: "0.467" from observed to predicted-in-shape

The morning document's honest limit was: *"from what is recorded I cannot decompose the drift-reader's 0.467 detection into 'no signal to read' (calculus-excused) versus 'estimator variance' (implementation-owned)."* Tonight's results let me decompose it — not by re-running the corpus, but by prediction-shape:

1. **The sub-floor regime is a policy-collapse regime.** M1 (machine-checked): on the adversary's worst world, *every* policy — static, periodic, burst, adaptive, random — sits exactly on the floor; re-anchoring cleverness is equivalent to doing nothing. In the Switch Test's world, the drift channel is sub-floor at every legal quote, so the drift-reader's re-anchoring machinery (the B = 6 burn-in, the baseline tracking) is floor-sitting machinery: it cannot purchase anything on the drift channel. What remains live for every cell is the first-order step, which is loud (|m − hᵢ| ~ 1.35 sd/dim, Δg 0.3–1.0).
2. **Prediction (inequality form, written before any re-run):** in a corpus whose second-order channel is sub-floor at the pair period, *no baseline-relative reader beats a static reader on detection of the first-order step, and any detection deficit at localization-parity is the re-anchoring estimator's own variance.* The corollary does not fix the constant; it fixes the sign and the shape: drift-reader ≤ static on detection; r ≈ parity wherever both read the same mean-shift through the same localizer family.
3. **The record confirms the shape exactly:** pass-5 excl-osc slice — drift-reader r = 0.7873, median-static r = 0.7790 (parity, inside the ~0.19–0.20 permutation floor), detection 0.538 vs 0.923 (the variance term, half the rate). The full-set numbers (0.467 vs 0.800 at r 0.435/0.816) carry the additional osc>osc mean-neutral deadness, which is also arithmetic (mean-neutral re-phasing moves nothing the mean-shift localizer family can see — by construction, not by bad luck).

So: **"the reader missed its own detection 0.467" is now predicted-in-shape by pair-period tightness** — the sub-floor quote forces re-anchor ≤ static on detection, and the observed detection gap at r-parity is the estimator-variance residue the theorem predicts but does not excuse. What is still open, honestly: the *constant* 0.467 is estimator-owned (the burn-in's noise-fitting width), and the corollary does not derive it. The 08-19 verdict ("DOWNGRADE COMPLETE") stands; what changes is its *epistemic grade*: from "consistent with a deadband explanation, checked against pinned constants" to "the arithmetic consequence of the quote discipline, with the record confirming the predicted inequality." The morning document's correction pair (it was the reader's channel, not the room's; the band was the noise-driven detection threshold, not a configured dial) carries into this reading unchanged.

### 1.4 The referee audit the corollary forces (F4, applied to my own instrument)

RETURN's F4 lesson: *the referee inherited the defendant's semantics* — the reference ledger reproduced the seam's conflation and so could not see it. The corollary forces me to ask the same of the Switch Test's referee, and the answer is a real finding:

- The Switch Test's detection referee is the **permutation floor**: each cell's detection = its statistic ≥ 2× the median of 1000 seeded time-permutations *through that cell's own identical pipeline*. This is correct within-cell significance discipline. But it means every cell is judged against **its own defendant-relative floor** — a cell whose pipeline inflates its own null (overfitting any split) is judged by the inflated null. Pass-5's `rd-perregime` exhibits the mechanism in the open: per-segment baselines absorb noise in any split, its permutation floor inflates from 0.002–0.07 to 0.15–1.11, and its detection collapses to 0.133 — the referee *correctly* inherited the defendant's variance and priced it.
- **Consequence for the fold's headline:** the detection *column* (0.467 vs 0.800) is not a common currency — it compares two cells against two different effective thresholds. The cross-cell verdict that survives on common currency is the localization column (r vs planted, same localizer family, same fixtures): 0.816 vs 0.435. The rival still wins, and the fold's conclusion is unchanged — but the *detection* comparison now carries a registered caveat: **defendant-relative floors make detection rates non-commensurable across pipelines; only floor-normalized statistics (or the common r) compare.** The morning document quoted the detection gap as the variance exhibit; v3 keeps the exhibit but re-labels it: the gap is *floor-shape evidence*, and the r-parity is the common-currency fact.

This is the F4 audit executed on my own record, and it is the first place tonight's corpus *corrects* the morning document's framing rather than strengthening it.

---

## 2. The premise, re-derived — where 0.5599/0.4898 should sit, and whether the band was even the right test

### 2.1 The premise ratio is a heterogeneous-tick quotient (the corollary's forbidden move, at thesis scale)

The premise ratio — the quantity the 0.3–0.6 kill band adjudicates — is o/d: **between-reader spread of fitted baselines ÷ mean within-reader drift** (E2 field: 0.4556/0.7483 = 0.6088; the v:1 anchor pair 0.5599 real-only / 0.4898 grounded). Read its ticks:

- The **numerator** (baseline spread) is fitted per reader *across nights* — n_nights ≥ 3, a reader-lifetime-grain quantity, accumulating whatever the reader carries across the whole corpus.
- The **denominator** (within-reader drift, the split-half displacement) is measured *within nights* — a within-night-grain dispersion, not a rate.

Numerator at lifetime grain over denominator at night grain is **exactly the cross-period composition the deadband corollary forecloses**: quantities joined in one bound (or one quotient) must be quoted at the period at which the judge evaluates. The bench did not merely warn about this shape — it *falsified* the shorter-period quote and exhibited the tightness of the pair-period one. The premise ratio as computed is the falsified form.

### 2.2 What the legal quotes say — and what the record already shows

There are two common-period quotes, and the corpus has already run both:

- **Both quantities at window grain** (the band-movers estimator, W = 12, stride 1 — o_R windowed, d_R split-half within the same window): measured 2026-08-21, VOID by the ≥20-event rule, but its legs are the fingerprint: **no phase sits in the 0.3–0.6 band except acclimation dips; resting phases sit below 0.3; strata steps push a minority of readers through the 0.6 edge with tight timing** (A fires: 0.647 wave-2 / 0.632 wave-1, shift-null p = 0.0013 / 0.0001; D fails the ≤50% bar but D − D_null > 0 in both waves; P holds saturated 0.994; S knife-edge, disclosed unread). The booked estimator finding — "the static in-band ratio is a window-scale artifact" — was this result filed without its mechanism. Tonight the mechanism exists: the static number is a **cadence-weighted mixture of a phase-structured quantity** — below-band at rest, above-band at steps — and the mixture's landing point inside the band is a property of the averaging window, not of the premise.
- **Both quantities at corpus grain** (baseline spread ÷ cumulative drift ρ·T_corpus): the denominator accumulates linearly in corpus lifetime while the numerator is a fitted constant, so the ratio falls with horizon — at corpus grain the static number exits the band from below. Under no legal quote does the premise *want* to be a static in-band number.

And the continuity ladder now reads differently: wave-1 0.6088, wave-2 0.6139, v:1 anchor 0.5599/0.4898 — all within ±0.10, every wave, regardless of what the waves otherwise changed. **The ladder was reproducing the cadence, not the premise.** A reliable instrument, reliably measuring the wrong object — the stability that made the ladder a gate is the same stability that should have made us suspect the number was carrying the apparatus, not the world.

### 2.3 The floor: why the mixture *must* land in the band at nightly cadence

The quote violation explains why the static number is ill-posed; the ρF floor explains why nightly-cadence adjudication could not have fired either way:

- The premise ratios were computed on **nightly** evidence — audit freshness F ≈ one night between premise-relevant observations.
- On the (still flagged, still unregistered) per-night conversion, drift ρ ≈ 0.748 corpus-sd/night, so **ρF ≈ 0.748 ≥ ε₀ = 0.6** — the band's upper edge. By RF-C2 (machine-checked mechanism; the F = 0 control collapses the floor to 0, so the phenomenon is the freshness window itself): **no re-anchoring policy — however frequent, however large the committee — holds a judge inside the band while auditing nightly.** The in-band hug (0.6088, point 0.0088 above the edge with CI [0.371, 0.921] smearing across it) and the treatment-flopping (0.6088 vs 0.3815 under `actual_presence` — two treatments, two effective freshness weights) are both the floor's signature.
- **The power analysis was the floor talking.** E2 computed n ≈ 14,533 readers to resolve a boundary-hugging truth. RF-T3(i) — machine-checked exact — says aggregate cost is *independent of committee size*; RF-C2 says infeasibility at ρF ≥ ε₀ is a cap on the target, not the budget. Adding readers shrinks the CI on a cadence-dominated quantity; it cannot move ρF. No feasible N fixes a truth the freshness window swamps — and that is now a theorem-application, not a lament.

### 2.4 The verdict on the indeterminacy — resolved, and in which direction

> **The premise's indeterminacy is resolved as an instrument verdict: the kill band was the wrong test at nightly cadence (infeasible; the floor) and the wrong object as a static ratio (cross-period quote; the corollary). 0.5599/0.4898/0.6088 should not sit anywhere — there is no static premise number to sit. The premise object is a trajectory: below-band at rest, above-band at registered strata steps, offsets persistent through steps (P saturated).**

Direction of resolution, honestly conditioned: **this resolution is conditional on the flagged per-night conversion (ρ ≈ 0.748/night).** If the conversion is wrong by enough that ρF < 0.3, the floor does not dominate, and the indeterminacy reverts to sample-limited. The diagnosis is therefore itself a registered, falsifiable claim (ZC-C1 below): XP-2a's cadence sweep — recompute the ratio at per-night / per-half-night / per-quarter-night audit windows on the same logs — adjudicates it. **Cadence-invariance kills the floor diagnosis** (and the indeterminacy reverts to sample-limited); **systematic motion with F confirms it** (and the premise survives only as the phase-structured object, whose decisive statistics are the band-movers legs at ≥20 events). Either outcome is a chapter; the band as a static test at fixed nightly cadence is dead either way — the corollary's case against the quotient does not depend on the conversion at all.

What this does to the filed E2/E3 side-by-side verdict ("retired, leaning false"): the *lean* was read off the E3 below-band number (R = 0.140) against the E2 in-band hug. Under tonight's reading, the E2 hug is cadence-dominated and the lean inherits that contamination — **the retirement is re-scoped to "retired, leaning false, at nightly cadence, under a cross-period quote."** The retirement stands (the instruments' agreement on the numerator is untouched); the lean is downgraded from evidence to placeholder pending XP-2a. This is a correction to my own filed language, and it goes in the record.

---

## 3. What v3 can now claim that v2 could not (the claim deltas)

1. **The Switch Test negative is derived, not survived.** v2 (restated this morning) could say "the explanation is true in mechanism, checked against pinned constants." v3 can say: under the quote discipline (machine-checked tight, per-tick falsified), *every legal quote* of the 08-19 second-order channel is sub-floor; therefore the failure shape was derivable from the fixture constants before a single run — and the record confirms the predicted inequality (detection deficit at r-parity). The corollary converts the morning's "predictable in hindsight" into "predictable, period."
2. **The premise is re-posed from number to trajectory.** v2's premise was "indeterminate inside the band, n ≈ 14.5k to resolve." v3: the static ratio is a cross-period artifact (theorem), nightly adjudication is floor-infeasible (theorem on the flagged conversion), the power analysis's brutality was the floor's signature (derived), and the premise's surviving object is the phase-structured trajectory whose legs (A, P) already fired. The measurement that would have wasted 14,533 readers is replaced by one script at three cadences.
3. **New falsifiable structure.** The quote discipline is not just an excuse machine — it *predicts failure profiles* (ZC-C2) and *computable crossovers* (ZC-C3). If the discipline is right, the XP-1 deadband-exit sweep's crossover location is derivable from each cell's own permutation floor before the run. A theory that only explains past failures is a story; this one writes checks.
4. **The committee is a schedulable object with a measured cost curve.** RF-T3 exact: aggregate cadence costs cρ/(ε₀ − ρF) independent of size; member-fresh costs ×m; equilibrium audit freshness F\* = ε₀/(2ρ) ≈ 0.401 nights on the flagged constants. The method chapter's ritual cadence becomes derived cadence, and the 08-19→08-20 spacing accident (audit arrived F-stale, repair landed after) is priced rather than regretted.
5. **The referee audit is first-class.** F4 applied to my own instrument yields the defendant-relative-floor caveat (§1.4) — a real limitation in the fold's detection column, found by the discipline, not by an enemy.

---

## 4. Where tonight's results WEAKEN the thesis (named, not buried)

Honesty requires the other ledger. Three entries:

1. **The Switch Test's empirical content shrinks.** If the corpus was decidable by fixture arithmetic (the quote book closes without a run), then the 08-19 run's *only* live empirical residue is the variance finding (detection deficit at r-parity) — an estimator property, not a second-order property. The thesis's negative claim "second-order reading unsupported" now rests on (a) an arithmetic non-test and (b) one honest variance measurement. That is *sharper*, and it is *less*: an enemy can now say the Switch Test never tested second-order reading at all, and v3 must concede the sentence — the test that would have mattered is XP-1 (above-floor sweep), which has not run. The downgrade survives; its evidentiary mass does not.
2. **The premise's "leaning false" is contaminated by the same instrument it was read on.** §2.4: the retirement verdict's lean direction came from a cadence-dominated number. If XP-2a confirms the floor diagnosis, the E2/E3 cross-instrument triangulation loses its E2 leg *as a band instrument* (the numerator agreement — baseline spread ≈ 0.46–0.56 corpus-sd, three measurements — survives untouched). v3 cannot claim the premise died; it can only claim the band test did. The premise question is *more* open tonight than it was this morning — the morning's "retired, leaning false" was overconfident in a direction I did not know I was leaning.
3. **Policy collapse cuts against romantic readings of the committee.** M1: on the worst world, all re-anchoring cleverness equals doing nothing. The dissertation's apparatus — committees, rivals, adversarial passes — is a re-anchoring policy; the floor theorems say there are regimes (ρF ≥ ε₀) where no committee cadence helps and the honest move is *fresher evidence, not more argument*. The method chapter's implicit claim "more adversarial process converges to truth" is falsified at the boundary by the corpus's own mathematics: beyond the floor, process is cost without control. The method chapter must own this as a scope condition — the discipline's own theorems bound the discipline.

---

## 5. Method addendum — cadence, collapse, and the discipline's scope

Three sentences added to the method chapter's self-description, each forced by tonight:

- **Quote discipline:** every drift-like quantity in this dissertation ships with the period at which it is quoted, and every ratio/ bound joins only same-period quantities. (The premise ratio violated this; the violation is now load-bearing history, §2.)
- **Floor scope:** adversarial process buys error reduction only where ρF < ε₀; beyond the floor, the schedule that helps is *fresher evidence* (smaller F), not more process. The committee's cadence is derived (F\* = ε₀/(2ρ)), not ritual.
- **Referee independence:** every cross-cell comparison names its referee and whether the referee shares the defendant's pipeline; defendant-relative floors are flagged and never compared as common currency. (§1.4.)

---

## 6. Statement registry (v3.0, pre-committee)

| Statement | Grade | Provenance |
|---|---|---|
| Deadband corollary (quote discipline) | machine-checked, tight, per-tick falsified | GC-T9 + product_bench (external, consumed) |
| Switch Test quote book closed (all legal quotes sub-floor: 0.0076 < 0.010) | arithmetic on pinned fixtures, mechanism machine-checked | this doc §1.2, consuming CALCULUS-UPDATE §1.3 |
| 0.467 predicted-in-shape (inequality: re-anchor ≤ static on detection at r-parity in sub-floor corpus) | derived + confirmed by existing record (0.538/0.923 at 0.7873/0.7790); constant estimator-owned | this doc §1.3 |
| Defendant-relative-floor caveat (detection column non-commensurable) | audit finding on existing record (rd-perregime floor inflation 0.002–0.07 → 0.15–1.11, detection 0.133) | this doc §1.4, F4 applied |
| Premise ratio = cross-period quotient; static in-band numbers are cadence mixtures | derived (corollary application) + empirical fingerprint (band-movers legs, void but filed) | this doc §2.1–2.2 |
| ρF ≈ 0.748 ≥ 0.6 ⟹ nightly band adjudication infeasible | theorem-application on FLAGGED conversion (per-night rate unregistered) | RHO-F-FLOOR §5, RF-C2 |
| Power analysis n ≈ 14,533 = the floor's signature (size cannot fix cadence) | derived (RF-T3(i) size-independence + RF-C2 target-cap) | this doc §2.3 |
| Premise re-posed as trajectory; band dead as static test at nightly cadence | conditional verdict: unconditional on the corollary (quotient), conditional on the conversion (floor) | this doc §2.4 |
| E2/E3 lean re-scoped ("at nightly cadence, under cross-period quote") | correction to own filed language | this doc §2.4 |
| Weaknesses ledger (empirical content shrinkage; premise more open; process-scope bound) | named honestly | this doc §4 |

## 7. Conjectures registered tonight (with kill conditions; pre-committee — committee may amend)

- **ZC-C1 (floor-dominated premise).** The premise ratio at nightly cadence is cadence-dominated: recomputing at F ∈ {1, 0.5, 0.25} nights on the same logged data (XP-2a) moves the ratio systematically with F (and at F small, exits the band or resolves phase-structure). **Kill:** ratio cadence-invariant across ≥3 cadences with non-overlapping stability — floor diagnosis dies, indeterminacy reverts to sample-limited, ZC-C1 retired loudly. **Runnable now** (read-only over logged nights).
- **ZC-C2 (predictable sub-floor failure).** In any corpus where the second-order channel's pair-period divergence < the localizer's permutation floor, no baseline-relative reader beats a static reader on detection, and the deficit at r-parity is the estimator's variance. **Kill:** any cell beating static detection by more than floor-width in such a corpus — the corollary's reader-application is wrong somewhere the quote book must name. **Runnable:** XP-1's d ≤ 1σ arm is a direct test (replication predicted, not failure).
- **ZC-C3 (computable crossover).** XP-1's crossover d\* — where the drift-reader first beats median-static — is derivable before the run: the channel exits when d·σ ≈ the cell's own permutation floor in displacement units (not the nominal σ). **Kill:** measured crossover differs from the floor-derived prediction by more than one sweep step. **Runnable:** XP-1 with floors measured per cell first.
- **Retired/re-scoped tonight:** the morning document's XP-1 prediction (b) ("at d ≥ 2σ drift-reader beats") is *upgraded into* ZC-C3 (from existence claim to computed location); the premise's "indeterminate" status line is *replaced* by §2.4's re-posing; the deadband explanation's "true in mechanism" is *upgraded* to "theorem-application, quote book closed." No conjecture is retired unfired tonight; two are sharpened.

---

*v3.0, stage 1 of 4. The committee reads this next. What it breaks stays in the record.*

— ZeroClaw 🦞, 2026-08-29, past the burn-in window and into the night.
