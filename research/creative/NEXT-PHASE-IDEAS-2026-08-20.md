# NEXT-PHASE EXPERIMENT IDEAS — 2026-08-20
## Context: ZeroClaw Dissertation, Post-E2/E3/Slope/Cross-Strata Results

This document proposes 5 novel, infrastructure-backed experiments using the Cloudflare elephant-sim-worker, quilt cell-ledger, and cross-strata lensed-space findings. All avoid repeating work already completed (slope regression, night-H, barkeep robustness, etc.).

---

## Experiment 1: Lensed-Space Transfer Ablation
(a) **One-line claim:** Cross-strata transfer (ρ ≈0.78) is a property of the reader's lensed reading space, not raw room signal, and vanishes when all lens gains are flattened (g_i=1 for all dials).
(b) **Decisive:** If ablation eliminates 95% of transfer, it directly validates the lensed-space finding from cross-strata addendum A4; if transfer remains ≥0.6, transfer is driven by raw room signal, not reader-specific lensing.
(c) **Minimal apparatus:** Cloudflare elephant-sim-worker for parallel 10k lens ablation trials across the E2 S-series corpus, existing per-reader log dataset, quilt cell-ledger to track lens imbalance (|g_i -1|) as field-edge magnitude.
(d) **Decision rule:** If mean ρ across all flattened-lens trials <0.3, claim holds; if mean ρ ≥0.6, claim fails.

---

## Experiment 2: Ramp-Transition Slope Geometry
(a) **One-line claim:** The within-reader baseline-warmth slope (≈0.13 from 2026-08-20 slope regression) shrinks to near 0 when rooms use subtle ramp transitions (night-H) instead of sharp flips.
(b) **Decisive:** Confirms that transition sharpness modulates baseline warmth-tracking, resolving the E2/E3 divergent drift denominators; opposite result proves slope stability across transition types.
(c) **Minimal apparatus:** Cloudflare elephant-sim-worker to run night-H ramp nights alongside existing E2 flip nights, quilt cell-ledger to track transition sharpness as field-edge magnitude, unmodified E2 reader instrumentation.
(d) **Decision rule:** If mean within-reader slope for ramp nights <0.05, claim holds; if slope ≥0.10, claim fails.

---

## Experiment 3: High-Drift Reader Baseline Signature
(a) **One-line claim:** Readers with elevated within-session drift (≥2σ from null drift controls) will show baseline-slopes ≈1 (collapsing to room-warmth estimates), while low-drift readers will show slopes ≈0 (aligned as distinct instruments).
(b) **Decisive:** Links session-grain drift directly to the H-reader≡room hypothesis, resolving the E2/E3 denominator divergence by showing drift magnitude predicts baseline identity.
(c) **Minimal apparatus:** Quilt cell-ledger to tag high-drift readers, Cloudflare worker to filter the S-series corpus for high/low drift cohorts, unmodified slope regression tools.
(d) **Decision rule:** If high-drift readers have mean slope ≥0.75 (collapse band) and low-drift readers have mean slope <0.25 (alignment band), claim holds; else fails.

---

## Experiment 4: Equity Lens Transfer Manipulation
(a) **One-line claim:** Cross-strata transfer strength correlates inversely with lens gain equity (scaled difference between high-variance and low-variance dial gains), as tracked by quilt cell-ledger field-edge magnitude.
(b) **Decisive:** Validates that differential dial gain drives cross-strata transfer, refining the lensed-space finding from addendum A5; opposite result proves transfer is dial-agnostic.
(c) **Minimal apparatus:** Cloudflare worker to batch 5k equity-lens variants across the S-series corpus, quilt cell-ledger to track gain equity as field-edge magnitude, existing transfer estimation pipelines.
(d) **Decision rule:** If Pearson correlation between gain equity and transfer ρ ≤-0.5 with 95% CI excluding 0, claim holds; else fails.

---

## Experiment 5: Static Room Null Transfer Test
(a) **One-line claim:** Cross-strata transfer disappears entirely when rooms are static (no-flip S5 nights only), as session-grain movement is required to drive memory plasticity.
(b) **Decisive:** Confirms that session-grain signal movement, not static reader identity, is the source of cross-strata transfer; opposite result proves transfer is identity-driven.
(c) **Minimal apparatus:** Cloudflare worker to run a static S5 no-flip corpus, quilt cell-ledger to track static vs dynamic room state, existing transfer estimation tools.
(d) **Decision rule:** If mean ρ for static nightly trials <0.2, claim holds; if mean ρ ≥0.6, claim fails.

---

## One-Line Claims Summary
1. Cross-strata transfer (ρ ≈0.78) is a property of the reader's lensed reading space, not raw room signal, and vanishes when all lens gains are flattened (g_i=1 for all dials).
2. The within-reader baseline-warmth slope (≈0.13 from 2026-08-20 slope regression) shrinks to near 0 when rooms use subtle ramp transitions (night-H) instead of sharp flips.
3. Readers with elevated within-session drift (≥2σ from null drift controls) will show baseline-slopes ≈1 (collapsing to room-warmth estimates), while low-drift readers will show slopes ≈0 (aligned as distinct instruments).
4. Cross-strata transfer strength correlates inversely with lens gain equity (scaled difference between high-variance and low-variance dial gains), as tracked by quilt cell-ledger field-edge magnitude.
5. Cross-strata transfer disappears entirely when rooms are static (no-flip S5 nights only), as session-grain movement is required to drive memory plasticity.