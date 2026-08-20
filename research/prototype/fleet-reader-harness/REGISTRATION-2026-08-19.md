# E3 REGISTRATION — The Fleet-Reader Harness (cross-model premise estimate)

**Registered: 2026-08-19 (pre-run). Committed before the first elicitation call.**
Binding spec: `research/dissertation/chapter-7-future-work.md` §7.5. Premise context: `chapter-6-the-seam.md` §6.2–6.4. This registration fixes every threshold, estimator choice, prompt, and deadman before any field data exists. Post-hoc changes go to the Deviations section of the report, never silently.

## 1. The question

A second, architecturally-independent estimate of the premise: **do distinct real readers — actual model minds, not simulated personas — diverge in their readings of the same real rooms by more than the kill band?** Registered asymmetry (§7.5, restated): the elicitation frame compresses spread (all models anchor to the same visible text and the same prompt), which biases *against* clearing. Therefore **a CLEAR is strong evidence; a MISS is weak evidence** (frame artifact cannot be excluded). Neither direction gets laundered.

## 2. Corpus (frozen)

- The 27 real room-windows the D″ fixtures pin: fixture manifest SHA256 `a423a3783a4a303f281e419d28359844990bcf312955a9eb18e636f753d56429` (verified by `extract_corpus.py`).
- Window = 8 consecutive speaks (W=8) of nights A, B, C, D, D-cold; segment label SEG1 (first speak seq < 20) / SEG2, per the fixture manifest. Two tail windows (D-w5, D-cold-w5) carry 6 speaks — the fixture rule keeps windows with ≥ W/2 speaks; the prompt interpolates the true message count.
- Speak texts are reconstructed verbatim from the deterministic generator (`elephant/scripts/nights_abc.py`) and every speak is verified against the log's `text_sha256`. Any mismatch aborts the run.
- **Registered honesty about stimulus multiplicity:** nights A≡B≡C share one 40-message script; D≡D-cold share one 46-message script. The 27 windows therefore contain **11 distinct window stimuli** (A-type 5 × 3 presentations, D-type 6 × 2). All 27 presentations are elicited (fixture parity); estimators weight **distinct stimuli equally** (§5).
- Elicited stimulus per window: author, verbatim text, and reaction counts (visible room signals). No other context; each window read independently (no cross-window conversation carryover).

## 3. Readers (the roster, 13 registered + 1 dropped)

| # | reader id | model | route | family |
|---|-----------|-------|-------|--------|
| 1 | glm-5.3 | zai glm-5.3 | gateway :8787 | GLM |
| 2 | glm-5.2 | zai glm-5.2 | gateway | GLM |
| 3 | ds-v4-flash | deepseek-chat (V4-Flash) | gateway | DeepSeek |
| 4 | ds-v4-pro | deepseek-reasoner (V4-Pro) | gateway | DeepSeek |
| 5 | seed-2.0-mini | ByteDance/Seed-2.0-mini | DeepInfra direct | Seed |
| 6 | seed-2.0-pro | ByteDance/Seed-2.0-pro | DeepInfra direct | Seed |
| 7 | qwen3.6-35b | Qwen/Qwen3.6-35B-A3B | DeepInfra direct | Qwen |
| 8 | qwen3.5-397b | Qwen/Qwen3.5-397B-A17B | DeepInfra direct | Qwen (MoE, different gen) |
| 9 | hermes-3-405b | NousResearch/Hermes-3-Llama-3.1-405B | DeepInfra direct | Llama-3.1 |
| 10 | claude-sonnet-5 | anthropic/claude-sonnet-5 | DeepInfra direct | Claude |
| 11 | gemma-4-31b | google/gemma-4-31B-it | DeepInfra direct | Gemma |
| 12 | minimax-m3 | MiniMaxAI/MiniMax-M3 | DeepInfra direct | MiniMax |
| 13 | nemotron-120b | nvidia/NVIDIA-Nemotron-3-Super-120B-A12B | DeepInfra direct | Nemotron |

Dropped before registration commit (unreachable in practice, noted per task):
- **glm-5-turbo** — not present on the zai gateway route (configured: glm-5.3/5.2/4.6/4.5-air); no direct zai key available. Substituted by glm-5.2 (same family, different tier).
- **nvidia/Nemotron-3-Ultra-550B** — removed from DeepInfra ("model does not exist"); substituted by Nemotron-3-Super-120B-A12B.
- **moonshotai/Kimi-K3** — a trivial "say OK" probe ran >10 min without completing; unusable for 27×2+18 calls. Not in the roster.

11 distinct architecture families across 13 readers; ≥10 readers required. If a reader fails validity (§6 deadman D2) it is dropped and reported.

## 4. Elicitation frame (frozen in `prompts.py`, SHA committed with this file)

- **Canonical prompt (P0):** participant-observer frame at the writers' salon; the window's 8 speaks verbatim with reaction counts; seven dials each rated 0–100 with grounded anchors (anchor text from the elephant dial docstrings); plus a **private displacement** per dial, −100..+100 ("your own reader's lean away from the room reading you just gave"). Strict-JSON-forced output schema: `{"room_reading": {7 dials}, "private_displacement": {7 dials}}`.
- Dial→native mapping (analysis-side): mood, joke_landing ∈ [−1,1] via `v/50 − 1`; volume, earnestness, cynicism, panic, presence ∈ [0,1] via `v/100`. Displacement (pts) → native units via `pts × (dial native width)/100`, so ±100 pts = the dial's full native width in either direction.
- **Emitted reading** (the premise object, mirroring the D″ nurse's displaced field): `r_i(t) = clip(native(room_reading) + native_disp(private_displacement), dial bounds)`.
- Temperature 0 everywhere supported; registered fallback to 0.01 where a provider rejects 0 (logged in the raw record).
- **Two passes** (identical P0 prompt, independent calls) → within-reader test-retest noise.
- **Paraphrase sweep (one, registered):** levels P1 (light: instruction rewording, anchors verbatim), P2 (moderate: dial order rotated, anchors reworded, transcript reformat, JSON key order flipped), P3 (strong: night-shift bar-back frame, no reactions shown, all anchors reworded). Sweep windows: `A-w0, A-w3, D-w1, D-w4, D-cold-w2, D-cold-w5` (segment- and night-stratified).
- JSON repair: up to 2 repair attempts feeding the parse error back; `response_format: json_object` attempted first, dropped on provider 400.

## 5. Estimator (registered; E2-comparable)

Units: corpus-sd = RMS over dials of the per-dial std of `field_raw_after` across all speaks of the 5 nights (the E2 `corpus_sd` definition; computed in `extract_corpus.py`). Secondary: window-mean-level sd (fixture manifest stats), reported alongside.

- **Pass-averaging:** the primary statistic uses per-window readings averaged over the two passes; per-pass ratios reported as robustness.
- **Segment-local baselines (standing rule 1):** `b̂_i,seg` = reader i's mean emitted reading over all windows of that segment, **equal weight per distinct stimulus** (11 stimuli; A-type not triple-counted).
- **Between-model baseline spread:** `spread_seg = sqrt(mean_dial Var_across_models(b̂_i,seg))`; `baseline_spread_z = mean(spread_SEG1, spread_SEG2) / corpus_sd`.
- **Within-model drift signal:** per reader i and distinct night-script s ∈ {A-type, D-type}: `d_{i,s} = ||mean_i,SEG2(s) − mean_i,SEG1(s)|| / corpus_sd`; `drift_i = mean_s d_{i,s}`; `mean_drift_z = mean_i drift_i`.
- **THE RATIO (field, elicited):** `R = baseline_spread_z / mean_drift_z`.
- **CIs (standing rule 3, n<100):** bootstrap over readers (the registered unit), 10,000 resamples, seed 20260819, percentile 95% CI on R; separate CIs on numerator and denominator; per-reader drift CI via bootstrap over night-scripts is degenerate (n=2) and reported as the two per-script values instead.
- **Secondary decompositions** (registered, reported alongside, never replacing the primary): room_reading-only ratio and displacement-magnitude-only ratio — where does spread live.

## 6. Thresholds, deadmen, verdict (frozen)

- Kill band: **> 0.6 clears / < 0.3 dies / 0.3–0.6 indeterminate**, evaluated on the 95% bootstrap CI of R: CI entirely above 0.6 ⇒ **premise holds (field, elicited) — strong evidence per the asymmetry**; CI entirely below 0.3 ⇒ **below band — weak evidence (miss), frame artifact not excludable**; otherwise ⇒ **indeterminate**, filed with the power note (what reader-N would be needed).
- **D2 (reader validity deadman):** a reader with < 80% valid windows (over 27 × 2 passes) is dropped and reported.
- **D3 (drift-vs-noise deadman, reporting flag only):** if the mean pass-to-pass retest displacement (retest_z) exceeds mean_drift_z for a majority of readers, the denominator is not separable from elicitation noise; the verdict sentence carries that caveat verbatim. Deterministic temp-0 endpoints giving retest_z = 0 do not trigger D3.
- **Paraphrase crossover (registered):** reader m is *destabilized at level k* if mean-over-sweep-windows `||r_m^{P0}(w) − r_m^{Pk}(w)|| / corpus_sd > 2 × max(retest_z_m, 0.02)`. Crossover = lowest k ≥ 1 destabilized (else none). Corpus-level: fraction destabilized per level.

## 7. Procedure discipline

1. This file + `extract_corpus.py` + `prompts.py` + `elicit.py` + `analyze.py` + verified `corpus/corpus.json` are committed BEFORE the first elicitation call (single pre-run commit).
2. Field run (`elicit.py`, resume-safe), then `analyze.py`, then the dated report `REPORT-2026-08-19.md` (or the actual run date) committed with raw readings.
3. The elephant repo is never written to.
4. Every number in the report carries the prefix **"field (elicited)"** — never "on fixtures".
5. Unreachable readers are skipped and noted in the report; the registration is not amended post-run.
