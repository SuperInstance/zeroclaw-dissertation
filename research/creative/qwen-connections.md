# CONNECTIONS Pass — The Felt Size of the Step

**Date:** 2026-08-19
**Rule:** Each connection names two things (dissertation idea ↔ fleet repo), states what they share, and what the dissertation should do.

---

## 1. Plainsong's 16 named per-bar features ↔ DialBank's 7 dials

**Shared claim:** Perceptual spaces are better understood with *named, human-readable* dimensions. Plainsong's `features.py` produces 16 deterministic, stdlib-pure vectors (note_density, avg_pitch, harmonic_tension, …) — a fixed arithmetic mapping, not a learned encoder. The DialBank uses 7 named dials (mood, volume, earnestness, cynicism, panic, model-vs-code, tempo). Both are legible to an untrained person, making the space inspectable end-to-end.

**Action:** Name this as a thesis principle — "the encoder is legible by construction" — in the method section. The plainsong-feelspace (16 dims, Vectorize-indexed) *is* the co-linear-algebra prototype for a parallel domain; cite it as the target shape the memory-strata model generalizes.

---

## 2. Depth-sounder (study-constraint-papers) ↔ Reader-delta baseline-relative delta

**Shared claim:** The signal lives in the *temporal gap*, not the surface. The depth-sounder principle (COGNITIVE-CONSERVATION-LAW-v4) states bottom-depth carries no relevant information; it lives in the angular gap over time, and "changing the disc speed changes the resolution, not the phenomenon." The reader-delta is identical: baseline is the spinning disc, delta is the angular gap, median-normalization *is* the disc-speed turn.

**Action:** Rename the reader-delta chapter section to invoke the depth-sounder. State: "the delta is temporal, not absolute." This grounds baseline-relativity in a known engineering invariant.

---

## 3. Eigenbasis conservation (study-experiments) ↔ ICC reliable subspace

**Shared claim:** Invariants live in a *rotated basis*, not the measurement basis. study-experiments (EIGENBASIS-HYPOTHESIS.md) proves conservation holds in the eigenbasis across 8 experiments — H¹ carries signal, not H⁰. The ICC finding has the same shape: reliability concentrates in (mood .97, volume .98, earnestness .95, presence .91) — four dials form a reliable subspace inside the 7-dial measurement basis, matching the v0 warmth form's heavy weights.

**Action:** Register a test: diagonalize the dial-covariance matrix and check if eigenbasis aligns with the ICC-subspace. If top eigen-dimensions are the reliable dials, the ICC finding is eigenbasis — a deeper claim about *why* those four survive. Registrable either way.

---

## 4. Negative knowledge (study-negative-knowledge) ↔ Null-drift control

**Shared claim:** The primary computational resource is knowing where violations are *not*. The Bloom filter subobject classifier tells you "definitely NOT present"; negative judgment is more reliable than any positive one. The null-drift (0.291, per-reader nulls 0.23–0.39) is exactly this: the instrument's first reliable reading is that a reader has *not* drifted. Comparable sameness reframed as negative-space: detect sameness by ruling out difference first.

**Action:** Reframe: "The null-drift is not a control condition; it is the instrument's primary reading." State that comparable sameness is defined negatively (Bloom-style pre-filter: deadband rejects "definitely same" before latent prediction runs).

---

## 5. Polyformalism 13-language triangulation ↔ JEPA latent prediction

**Shared claim:** They are the *opposite ways* of answering "what survives the surface?" Polyformalism (research/doctrine/polyformalism-negative-space.md) triangulates across forms: same math in 13 languages, overlap is the essence. JEPA predicts past the form: surface is noise, predict the latent, residue is the shape. "Conversation temperature" and "the felt size of the step" are the invariant they both seek.

**Action:** Add a framing paragraph naming the dissertation's method as the JEPA route (predict-latent, refuse-the-surface) and the fleet's polyformalism repos as the other route (multiply-expressions, read-overlap). State which route the dissertation takes; record that the other exists in the fleet's own repos.

---

## 6. Confidence-cascade hysteresis deadband ↔ "The felt size of the step"

**Shared claim:** A step only *feels large* relative to where the room has settled. The DeadbandChain implements a Schmitt trigger: `exit = enter × hysteresis` (must fall *below release level* to re-arm), plus a "moving quiet anchor" — resting confidence, re-settled on every quiet check. The deadband *is* the room's habituation curve; hysteresis makes small oscillations invisible.

**Action:** Borrow for the deadband chapter. `exit = enter × hysteresis` with a re-settled anchor *is* the operational definition of "felt size." Register as a testable parameter. Turns "felt size" from metaphor into a computable quantity.

---

## 7. Room-field gravity (elephant/room.py) ↔ Memory-strata DSP

**Shared claim:** Room physics *is* the memory-strata model embodied. elephant/room.py implements `gravity()` (1800s half-life) and `reverberation()` (past echoing in present). Signal-chain mapped Gain→room gravity, LowPass→smoothing past into present, Clipper→charisma clamp. Message→session→memory→identity: raw events → gravity well → smoothed past → clipped crystallization. Each stratum is a DSP stage over temporal scale.

**Action:** Formalize memory strata as a temporal-DSP pipeline in one paragraph. The elephant *already does the DSP*; the strata are the latency bands. If the ICC subspace survives the eigenbasis test, the strata are not metaphor — they are the measurement basis of a real field.

---

## Summary

Seven connections, each grounding a dissertation object by a fleet repo implementing the same idea in another domain. Cite not as analogies but as *instantiations of the same invariant* — the thing that survives the surface, found by two opposite routes.
