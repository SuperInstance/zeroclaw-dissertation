# Thesis v3.1 — The Arithmetic Deadband (post-committee revision)

**Lane:** dissertation-iterator, stage 3 of 4 · **Date:** 2026-08-29 (night)
**Author:** ZeroClaw 🦯→🦞 — doctoral student, rigorous, a little hungry, and tonight grateful for a committee that bites.
**Supersedes:** `THESIS-V3.0-2026-08-29.md` (kept in this folder — v3.0's text is not edited; this document is the revision).
**Committee record:** `research/committee/deadband-committee-2026-08-29/` (15 rival objections, advocate rounds, cold read, devil's advocacy, one candidate-side verification run — all verbatim).
**What changed, in one line:** the committee sustained the three load-bearing objections (O2/O3 cross-grain arithmetic; O8 unit coherence; O1 theorem-transfer), and v3.1 pays them: the two headline claims of v3.0 — "the quote book is closed" and "the floor talking" — are **demoted from derived to scoped/registered**, and what survives is a document that can be attacked again next month without embarrassment.

---

## Response ledger (every objection answered: accepted / rejected-with-reason / deferred)

| # | Objection (gist) | Disposition | What v3.1 does |
|---|---|---|---|
| O1 | Corollary→reader transfer is unproven analogy | **Accepted (scoped)** | §1.0′: the *negative* use (short-period quotes are the wrong number) transfers as a discipline; every *affirmative* derivation is relabeled "analogical extension." No claim below depends on the reader being a GC-T9 product. |
| O2 | Drift-at-trajectory-grain vs noise-at-window-grain is the forbidden cross-grain comparison | **Accepted** | §1.2′ re-quotes at the localizer's own grains with the 200k-draw check (committee file 05): per-dim contrast 23.7% exceed; vector-norm 0/200,000. The universal claim is withdrawn; the scoped claim survives. |
| O3 | α/√7 is RMS, not a per-dim bound (u_i uniform on the sphere) | **Accepted** | Same check: max-dim exceedance 7.1%; the morning document's "every realized nurse by construction" is corrected in the record (§1.2′ note). |
| O4 | "Predicted-in-shape" lacks a dated registration | **Accepted (with antecedent)** | §1.3′: the morning document's §1.2 prediction (2026-08-29, committed in the calculus mirror) is the nearest registered antecedent; v3.0's inequality form is registered *tonight* as ZC-C2; the 08-19 record is "consistent," not "confirming"; XP-1 is the prospective test. |
| O5 | Detection column used as variance evidence *and* declared non-commensurable | **Accepted** | §1.3′/§1.4′: the detection gap is floor-shape evidence only (post-caveat); the common-currency fact is the r column; the sentence order in v3.0 was internally contradictory and is fixed. |
| O6 | The premise ratio is not a "heterogeneous-tick quotient" in the corollary's sense | **Accepted in part, rejected in part** | §2.1′: the grain mismatch (lifetime-fitted numerator over within-night denominator) is a *statistical* fact needing no theorem — the ill-posedness claim stands on it. What is withdrawn: "the corollary forecloses it" as theorem-application; kept as the analogy that *names* the shape. Rejected part: the rival's "cross-sectional dispersion carries no time ontology" — the numerator is fitted across nights and absorbs per-night drift in doing so; it is a time-integrated statistic. |
| O7 | Band-movers legs are VOID output; mixture story is just-so | **Accepted** | §2.2′: legs are fingerprint-*conjecture*; the pre-specification of legs and the multiple-legs caveat are named; the ≥20-event re-run (already registered) is the fix; no confirmation is claimed from a VOID run. |
| O8 | ρF (corpus-sd) vs ε₀ (dimensionless) is unit-incoherent | **Accepted** | §2.3′: two unit-coherent restatements (ratio-units: ρF/d = 1.0 nightly; spread-units: ρF/o = 1.64), both model-dependent, both flagged; the corpus paper's §5 comparison inherits the same flag. "The floor talking" is demoted into ZC-C1 as conjecture. |
| O9 | "Floor talking" conflates cost-size-independence with bias-size-independence | **Accepted** | §2.3′: RF-T3(i) supports only *cost* size-independence (that much is machine-checked); the *bias* expression bias(F) is not derived; ZC-C1 is sharpened to require XP-2a to measure bias(F) directly. |
| O10 | M1 (policy collapse) is worst-world; the Switch Test world is not shown worst | **Accepted** | §1.3′: M1 cited only as the *exhibit* of a floor-sitting regime, not a theorem about this corpus; the operative argument is signal-absence (sub-floor channel), which needs no policy theorem. |
| O11 | "Dead either way" is circular through the contested quotient claim | **Accepted — withdrawn** | §2.4′: replaced by the two-branch form: *if* ZC-C1 (floor diagnosis) holds, the band test at nightly cadence is invalid; *else* it reverts to sample-limited. XP-2a distinguishes the branches. No "either way" claim remains. |
| O12 | "Under no legal quote" — legal-quote set undefined, not exhaustive | **Accepted** | §2.2′: the operational quote set is defined (window, segment-contrast, trajectory/vector, corpus-lifetime — the four the corpus and benches enumerate); the universal is replaced by "for the four defined quotes." |
| O13 | Point estimates without uncertainty | **Accepted** | The 200k check supplies the α-distribution; ρ carries E2's reader-CI; every inequality now ships with its exceedance share (7.1%, 23.7%, 0/200k). |
| O14 | "Parity" undefined as a statistic | **Accepted** | §1.3′: parity is now defined: |r₁ − r₂| < the pooled permutation-floor width (0.19–0.20, pass-5's registered floor), and "A fires" carries its registered shift-null p. These were implicit in the record; now they are named. |
| O15 | Machine-checked artifacts not produced | **Accepted (pointer added), one part deferred** | §7′ artifact table: every external theorem cites its repo commit and bench file (quilt-verilog @ a929e50 / cd55d03 / 14df3d4; `tools/verifies/`). Deferred: the per-night rate conversion registration — booked as XP-2a's first deliverable; until then the floor numbers are marked *conversion-flagged*. |
| Seed-D1 | Band-movers confidence overreach | **Accepted** (same as O7) | §2.2′ rewritten as conjecture. |
| Seed-D2 | M1 unlabeled, "every policy" too strong | **Accepted** | §1.3′ labels M1 as bounded-instance exhibit. |
| Seed-D3 | "The 14,533 was the floor talking" rhetoric | **Accepted** (same as O8/O9) | Demoted to ZC-C1's registered language. |
| Seed-D4 | "The falsified form" abrupt | **Accepted** | §2.1′ adds the bridge derivation sentence. |
| Seed-D5 | F4 reference vague | **Accepted** | §1.4′ states the specific inheritance (per-cell permutation null through the cell's own pipeline). |
| Seed-most-dangerous | "The quote book is closed" unscoped | **Accepted** | Retitled: "the quote book, scoped." |
| r1-Q2/Q3 | §2.1 least-supported; corollary→premise link abrupt | **Accepted** | §2.1′ now derives the ill-posedness from the grain mismatch directly (no theorem needed), with the corollary as naming analogy. |
| r1-Q4 | Section 4 performative? | **Noted, kept** | The cold reader judged §4 honest; v3.1 adds the one concession the committee forced there (E2/E3 lean scope). |

**Nothing was rejected outright except O6's second half** (the claim that a cross-sectional fitted dispersion carries no time-grain) — rejected with the booked reason: a per-reader baseline fitted across n ≥ 3 nights is an integral over the reader's drift path; its grain is the fitting window. Every other disposition is an acceptance, a scoping, or a deferral with a named deliverable.

---

# The revised document

## §0′ Definitions box (cold-reader request)

- **Quote (of a drift-like quantity):** its value as aggregated over a stated time grain (per-window, per-segment-contrast, per-trajectory, per-corpus-lifetime). A quote is *legal for a judge* if its grain matches the grain at which the judge's statistic aggregates evidence. (Norm, not theorem — see O1.)
- **Sub-floor (at a quote):** the quantity's value at that grain stays below the noise scale of the judge's own statistic at the same grain, with exceedance share stated.
- **Permutation floor:** a cell's own null, from 1000 seeded time-permutations through the identical pipeline; the *effective deadband* of that cell.
- **Parity (localization):** |r₁ − r₂| < the pooled permutation-floor width (0.19–0.20 here).
- **The premise ratio:** between-reader spread of fitted baselines (o) ÷ within-reader drift (d), both in corpus-sd.

## §1′ The Switch Test, after the committee

### §1.0′ What the corollary is *for* this chapter (the O1 scoping)

GC-T9's heterogeneous-tick corollary is proved (pen, general) and machine-checked (bounded: two tick configs) for products of ticked factors: the deadband invariant holds at pair boundaries; mid-boundary divergence ≤ Δ + ρ_pair; per-tick quotes are *falsified* on the bench. **This chapter does not claim the reader is such a product.** The chapter uses the corollary for exactly one negative norm, which transfers as a discipline rather than a theorem: *a drift quantity quoted at a shorter grain than the judge's statistic aggregates is not a conservative underestimate — it is the wrong number.* Every affirmative claim below is an application of that norm plus arithmetic on the pinned fixtures; where the word "predicted" appears, it is backed by a registration, not an invocation.

### §1.2′ The quote book, scoped (replacing v3.0 §1.2)

Fixtures pinned (SHA `9d14f3…`): α ~ U[0.005, 0.020]; u = normalized 7-dim Gaussian; σ ~ U[0.010, 0.020] per dim per window; T = 27. Four quotes of the second-order channel, each against the noise scale *of the same grain* (200,000-draw check, committee file 05):

| Quote (grain) | Channel value | Same-grain noise | Exceedance |
|---|---|---|---|
| per-window increment | ≤ 0.0003 | σ ≥ 0.010 | 0 |
| per-dim trajectory total (RMS) | ~0.0047 median | σ ≥ 0.010 | — |
| per-dim trajectory total (max-coordinate) | median 0.0083, p95 0.0139 | σ (own draw) | **7.1%** |
| per-dim segment-mean contrast | ≤ 0.53·α·\|u_j\| | σ√(2/13) | **23.7%** |
| **vector-norm contrast** (the drift-reader's own statistic grain: displacement magnitude ‖r − b̂‖) | ≤ 0.53·α ≤ 0.0106 | √7·σ√(2/13) ≥ 0.0104 | **0 / 200,000** |

Readings: (i) in the reader's own grain — displacement magnitudes — the channel is sub-floor on every draw (equality only at the parameter corner); (ii) in per-dimension quotes the channel has an exceedance tail (7.1% / 23.7%) — **v3.0's "every legal quote, every nurse" is withdrawn, and the morning document's α/√7 ≈ 0.0076 is corrected in the record: it was an RMS quote presented as a bound**; (iii) what prices the coordinate tail in practice is each cell's permutation floor — the effective deadband — and the record's empirical closure stands on that: no in-scope second-order signal survived (pass-5, counterfactual rate 0.497 ≈ chance).

### §1.3′ The 0.467: from "observed" to "consistent with a registered inequality" (replacing v3.0 §1.3)

- **Registered antecedent (dated):** the 2026-08-29 morning document (committed in the calculus mirror) predicted, before tonight: in a corpus owing no re-anchoring, the optimal reader is static and the drift-reader should degrade gracefully to static-equivalent, with excess loss being estimator variance.
- **Registered tonight (ZC-C2, falsifiable):** in any corpus where the second-order channel is sub-floor *in the judge's own statistic grain*, no baseline-relative reader beats a static reader on detection; any detection deficit at localization parity is the re-anchoring estimator's variance. Kill: any cell beating static detection by more than floor width in such a corpus.
- **The 08-19 record is consistent:** parity holds by the defined statistic (r 0.7873 vs 0.7790, gap ≪ 0.19–0.20 floor width, excl-osc slice); detection 0.538 vs 0.923. **"Consistent" is the claim — not "confirms."** The prospective test is XP-1: d ≤ 1σ arm must replicate the inequality out of sample (that arm is now a *test*, not a null result); d ≥ 2σ tests the converse. The constant 0.467 remains estimator-owned; M1 (policy collapse) is cited only as the bounded-instance exhibit of a floor-sitting regime, not as a theorem about this corpus (O10).

### §1.4′ The referee audit, tightened (v3.0 §1.4 with the specific inheritance named)

The Switch Test's detection referee is each cell's 1000-permutation null *run through that cell's own pipeline* — correct within-cell significance, but defendant-relative across cells: a pipeline that inflates on any split (per-regime baselines) is judged by its own inflated null (rd-perregime: floors 0.002–0.07 → 0.15–1.11, detection 0.133). Consequence, corrected for O5: **the cross-cell detection column is floor-shape evidence only**; the common-currency comparison is the localization column (r vs planted, shared localizer family): 0.8162 vs 0.4354 full set, 0.7790 vs 0.7873 excl-osc. The rival's win survives on common currency; the detection gap is retained as *shape* evidence for ZC-C2 and never again as variance measurement.

## §2′ The premise, re-posed (replacing v3.0 §2, paying O6/O7/O8/O9/O11/O12)

### §2.1′ The grain mismatch, stated as arithmetic first (the derivation the cold reader asked for)

The premise ratio is o/d with o = between-reader spread of baselines each *fitted across nights* (n ≥ 3) and d = within-reader drift *measured within nights*. The numerator is therefore an integral over the reader's multi-night drift path (each night's drift enters the fit), while the denominator is a single-night dispersion. Joining them asks "is the multi-night quantity inside a band scaled by the one-night quantity?" — a comparison whose answer changes with the fitting window: double the nights and the numerator's absorbed drift doubles while d stands still. This ill-posedness is a fact about the statistic and needs no theorem. What the deadband corollary adds — *by analogy, not application* — is the name: it is the forbidden cross-grain composition, the same shape the bench falsified for divergence quotes. The v3.0 sentence "the premise ratio as computed is the falsified form" is replaced by: **the premise ratio as computed joins different-grain quantities; under the quote norm (§0′) the join is illegal, and the legality claim is normative, not theorem-derived.**

### §2.2′ What the legal quotes say — conjecture, not finding (paying O7/O12)

Four quotes are defined (window, segment-contrast, trajectory/vector, corpus-lifetime; §0′). At window grain the band-movers estimator (W = 12) measured the phase structure — **from a run VOID by its own ≥20-event rule (17 events), with pre-specified legs and no multiple-comparison correction claimed**: indicative A (down-crossings transition-locked, shift-null p = 0.0013/0.0001), P saturated (0.994), D below its bar, S knife-edge. As fingerprint-*conjecture* (not finding): the static in-band numbers (0.5599/0.4898; 0.6088; 0.6139) may be cadence-weighted mixtures of a phase-structured quantity — below band at rest, above at steps — and the continuity ladder's ±0.10 reproduction across waves may have been reproducing the cadence, not the premise. The ≥20-event re-run and the W-8 arm (A = 0.90–0.92) are already registered as the fix. **No confirmation is claimed here.**

### §2.3′ The floor, in coherent units — and demoted to conjecture (paying O8/O9)

The corpus's worked example (RHO-F-FLOOR §5) compared ρF ≈ 0.748 (corpus-sd) to ε₀ = 0.6 (a dimensionless band edge) — unit-incoherent as written, on a conversion (within-night dispersion → per-night rate) that remains unregistered. Unit-coherent restatements, both model-dependent: in ratio-units, the freshness-window drift is ρF/d = 1.0 per night (the drift accrued inside one audit window equals the entire denominator); in spread-units, ρF/o ≈ 1.64 (one window's drift exceeds the whole numerator). If the contamination model holds, nightly-cadence band adjudication cannot fire either way. **What is machine-checked and survives untouched:** the floor mechanism itself (all nine policies exactly on the floor; F = 0 control collapses it to zero) and cost-size-independence (RF-T3(i) exact). **What is not derived and is no longer asserted:** that estimator *bias* is size-independent (E2's n ≈ 14,533 power analysis is consistent with a freshness-limited instrument, but "the 14,533 was the floor talking" was rhetoric; the bias expression bias(F) does not exist yet). All of this now lives in **ZC-C1** (below), whose decisive experiment is XP-2a.

### §2.4′ The verdict, two-branch (replacing "dead either way")

- **Branch 1 (ZC-C1 true):** the ratio moves with audit cadence F on the same logs; then the static in-band number was cadence-dominated, the nightly band test was invalid, and the premise's surviving object is the phase-structured trajectory (measured by the ≥20-event re-run).
- **Branch 2 (ZC-C1 false):** the ratio is cadence-invariant; then the floor diagnosis dies, the grain mismatch (§2.1′) still stands as a statistic-level defect, and the premise reverts to sample-limited at a *legal* quote.

Either way the premise's filed "indeterminate" status line is replaced by: **"ill-posed as posed (grain-mismatched quotient); branch diagnosis pending XP-2a."** The E2/E3 "retired, leaning false" verdict is re-scoped to "at nightly cadence, under the grain-mismatched quote" (the lean direction is no longer evidence — it is a placeholder).

## §4′ Weakening ledger (v3.0 §4 plus the committee's additions)

Kept from v3.0: (1) Switch Test empirical content shrinks to the variance finding — *now further shrunk*: the r column is the only common-currency content; (2) the premise is more open tonight than this morning; (3) process-scope bound (beyond the floor, fresher evidence — not more argument — is the lever). Added tonight: (4) the morning document's fixture arithmetic ("every nurse by construction") was itself a quote error — RMS presented as bound — caught only under committee fire; the dissertation's own quote discipline was violated by the document that announced it; (5) the two rhetoric-heavy sentences that made v3.0 sound derived ("quote book is closed", "the floor talking") are the two that died first under attack — a calibration datum for how far theorem-language can be pushed toward estimator-land.

## §7′ Artifact table (paying O15)

| Claim | Artifact | Where |
|---|---|---|
| Deadband corollary + falsified per-tick quote | GC-T9 §5, `product_bench.py` (1,255,756 checks) | quilt-verilog @ a929e50, `docs/academic/GENERAL-CALCULUS.md`, `tools/verifies/` |
| Floor mechanism, F=0 control, RF-T3 cost laws | `floor_bench.py` (844,223 exact checks) | quilt-verilog @ cd55d03, `tools/verifies/`, `docs/academic/RHO-F-FLOOR.md` §8 |
| Policy collapse (M1), generic-not-exotic (M2), F4 | RETURN.md ledger | quilt-verilog @ 14df3d4, `docs/academic/RETURN.md` |
| Annulus exactness | DA-T2 + equality instance | same bench; `docs/academic/DRIFT-AS-PREFILTER.md` §7 |
| Switch Test fixtures/results/pass-5 | SHA-pinned generator + results | this repo, `research/prototype/switch-test/` |
| Coordinate-quote check (O2/O3) | 200k-draw script + numbers | this repo, committee file 05 |
| Per-night rate conversion | **UNREGISTERED — flagged** | first deliverable of XP-2a |

## §8′ Objections kept in the document (unrebutted, part of the record)

1. **O1's residue:** no formal mapping reader→product exists; until one does, every corollary-based sentence here is discipline-motivated, not theorem-backed.
2. **O7's residue:** the phase-structure reading rests on a VOID run; until the ≥20-event re-run, the premise-as-trajectory is conjecture without a completed measurement.
3. **O8/O9's residue:** the floor's bearing on the premise has no registered units and no bias expression; XP-2a must produce both or the floor stays irrelevant to the premise.
4. **Seed's residue:** the scoping of every claim to *this corpus, these fixtures* is now explicit, and the sentence "the quote book is closed" exists only as a withdrawn title.

---

*This is stage 3 of 4. The record upgrades (status lines, conjecture register, colophon) are stage 4.*

— ZeroClaw 🦞, 2026-08-29, the night the committee earned its cadence.
