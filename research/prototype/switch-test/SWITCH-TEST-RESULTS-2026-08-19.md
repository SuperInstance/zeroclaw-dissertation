# Switch Test Results — 2026-08-19

**Rival A's counter-proposal, run.** Regime-switching synthetic nurses. The question: does a true second-order (drift-reading) object see a regime change that a first-order fingerprint cannot? Pre-registered kill condition: if a primary first-order cell reaches parity with the drift-reader on BOTH Task A (switch localization) and Task B (regime classification), the second-order object is a reindex.

**Replay:** SHA256 `9d14f392ecbd85991c78a5e0c57127594b91b10d4c534562dc411f3263f32695`, 3/3 identical (seed 20260819). N=19 nurses (15 switching, 4 controls), 7 switch families, T=27 windows, 4 regimes {sauna, jaded, over, osc}, held-out nurse = `nurse-15` (family over→sauna).

---

## The honest verdict: NO CLEAN WIN — the drift-reader fails its own detection threshold, and the rival's median-static normalization beats it on Task A.

**Kill condition does not fire** (`kill.fires = False`), but not for the reason the second-order claim wants. The primary first-order cells (fo-norm, fo-template-euclid, fo-template-cosine) all fail Task A parity — they genuinely cannot localize a regime switch. But the drift-reader *also* fails its own pre-registered Task A threshold, and the boundary median-static cell beats it outright.

## Task A — switch detection + localization

| cell | median err (windows) | r vs planted | detection rate | control alarms |
|---|---|---|---|---|
| **drift-reader** (registered) | 2.0 | 0.435 | **0.467** ❌ | 0.0 |
| drift-online (post-hoc) | 2.0 | 0.454 | 0.667 | 0.0 |
| **fo-median-static** (BOUNDARY) | 2.0 | **0.816** | **0.800** ✅ | 0.25 |
| fo-crowd (BOUNDARY) | 2.0 | 0.609 | 0.533 | 0.25 |
| fo-norm (PRIMARY) | 4.0 | 0.115 | 0.267 | 0.0 |
| fo-template-euclid (PRIMARY) | 4.0 | 0.277 | 0.400 | 0.0 |
| fo-template-cosine (PRIMARY) | 3.0 | 0.336 | 0.400 | 0.0 |

**Pre-registered Task A threshold: detection ≥ 0.80.** The registered drift-reader scores **0.467 — it misses its own threshold.** The boundary `fo-median-static` cell (the rival's §2.4 median-trick normalization, a single global per-nurse median — *no temporal structure at all*) scores 0.800 and r=0.816, **beating the drift-reader on both metrics.**

The only thing keeping the kill condition from firing is that the *primary* first-order cells (fo-norm and the static-template fingerprints) are even worse at localizing switches than the drift-reader. The median-static cell — the exact normalization the rival flagged as capable of reproducing the reader-delta result — is *better* than the drift-reader on the very task the drift-reader was supposed to own.

## Task B — regime classification (4-way, chance 0.25)

| cell | pre acc | post acc |
|---|---|---|
| drift-reader (own segments) | **0.867** | 0.667 |
| fo-median-seg (BOUNDARY) | 0.800 | **0.867** |
| fo-norm-centroid (PRIMARY) | 0.667 | 0.800 |
| fo-raw-1nn (PRIMARY) | 0.733 | 0.800 |
| fo-template (PRIMARY) | 0.533 | 0.200 |

On Task B, the drift-reader wins pre-switch (0.867) but *loses post-switch* (0.667) to both the boundary median-seg cell (0.867) and the primary fo-norm-centroid (0.800). The first-order cells were given the **oracle gift** of guaranteed pre/post windows — yet they still classify post-switch regimes *better* than the drift-reader on its own localized segments.

## Noise sweep

Drift-reader's localization r degrades monotonically under added noise (0.39 → 0.34 → 0.15 → −0.46) and crosses its own usefulness at σ=0.2 (median err 2→4). The crossover is at the noise level where the fixture signal itself is submerged — the drift-reader is not robust to noise the fixtures didn't engineer in.

## Sensitivity (post-hoc, labeled)

Excluding the `osc>osc` family (mean-neutral phase flips, invisible to mean-shift machinery by construction), the drift-reader's localization improves to r=0.787, median err 1.0 (n=13). This is *post-hoc* and cannot be claimed as the registered result, but it isolates the failure: the drift-reader's localization is real for regimes that move the mean, and dead for regimes that only re-phase.

---

## One-sentence honest verdict

*The Switch Test does not deliver the clean win the second-order claim needed: the kill condition does not fire against the primary first-order cells, but the drift-reader fails its own detection threshold (0.467 vs 0.80) and the rival's median-static normalization — which carries no temporal structure at all — beats it on switch localization, so "second-order beats first-order" survives only against the weakest first-order baselines, not against the median trick the rival warned about.*

## Method note (advisor-corrected, 2026-08-19)

The original subagent run was terminated mid-fix after it discovered its own change-point bisection handled only increasing functions. The advisor completed the fix (negated the upper Clopper-Pearson root to increasing form — the CIs had been collapsing to 0.0), re-ran to a verified 3/3 replay, and wrote this report from the corrected `results.json`. No fixture, threshold, or methodology was changed; only the CI bisection bug was repaired.
