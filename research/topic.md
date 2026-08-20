# Dissertation Topic — Refined Draft v3

**Candidate title (v3):** *The Felt Size of the Step: Room-Field Measurement, Baseline-Relative Reader Deltas, and the Discipline That Made Them Honest*

*(v1 — *Grafting the Elephant onto the Grid* — died 2026-08-19: "conversation temperature" is a category error under elephant doctrine. v2 — *Walks, Not Waves* — half-died the same day: the field-edge survived as substrate, but the second-order "crown" failed its own tests. v3 names what actually survived.)*

## The one-sentence claim (current)

*The room's temperature field is honestly measurable (vMF snapshots, dial-tier fine gap 1.229, 3/3 deterministic), the trusted reader's drift is a small but real mean-shift baseline-relative delta (real for mean-moving regimes, pre-switch classification only, reproducible by median normalization), and the dissertation's durable contribution is the adversarial pre-registration discipline that caught every overclaim — six launderings, two phantom baselines, one contaminated eval, one registered-threshold miss — before any of them filed.*

## Which JEPA, precisely

The dissertation's use of JEPA follows the LeCun (2022) line — **predict-latent, not generative, not contrastive**: the model predicts representations in embedding space, never pixels/tokens, and never via contrastive negatives. The elephant's implementation recipe is the standard one: EMA target encoder + stop-gradient + variance regularization (VICReg-style) over dial time-series (v1), with v3's room-state embeddings trained on cold/warm contrast. **Two doctrinal choices distinguish this fleet's use from the stock recipe:**

1. **The unit of perception is the room (the ensemble field), not the stream (the message sequence).** Latents are predicted over windowed room-states — the vMF (μ̂, κ) snapshot of the DialBank's 7-dial readings — not over token/clip sequences. Justification: the empirical probe chain (encoder within-room fine gap 0.015 vs cross-room 0.271-doc-claim; dial-tier within-night 1.229) plus the doctrine's contrast-only training rule.
2. **JEPA is the *sense*, not the model.** One JEPA is a dial; the elephant is the DialBank ensemble; readings *nudge* (blend ≤ 0.15) and never replace. The contrast head (2026-08-19) is the one place the fleet crossed into contrastive learning proper (InfoNCE, multi-positive, room positives) — and it is labeled as such in Ch5, not smuggled under the JEPA name. (The devil's FaceNet ancestor is booked there.)

Casey's "JEPA is vision, not text" is the frame: words are constraints (the deadband); JEPA is the likeness inside. The dissertation keeps this as doctrine, with the Switch Test's honest boundary: the machinery reads mean-moves, not re-phasing — the shape inside has a measured edge.

## What survived the day (the claim inventory)

1. **Room-field measurement (solid):** true vMF κ MLE (Newton/Bessel, numpy-only, scipy-verified), warmth as μ̂-projection decoupled from κ by construction, the banned v0 proxy test-enforced out of comparison paths. Dial-tier: fine gap 1.229 (12.3× deadman, 3/3), noise floor exactly 0, newcomer displacement 0.830 with κ tightening 21→47, D′ cold-entry acclimation (half-life ≈ 20 msgs). The two-tier inversion (dial ≠ encoder geometry) is a finding, not a nuisance.
2. **The edge log (solid):** order-of-arrival, presence masks, per-window fits, replay-honest (post-D′ fix), deterministic. G0's missing hippocampus, instrumented.
3. **The encoder tier (mixed, honestly split):** in-sample fine gap 0.478 (3/3, registered) — room-identity recoverable; held-out FAIL (0.0694 mean, seed 2 < 0.05 floor) — does NOT generalize to unseen nights. Retrieval fact, not measurement instrument. Upgrades registered.
4. **The reader-delta object (downgraded to its true size):** a mean-shift baseline-relative delta — two scalars (slope, mean of ‖r−b̂‖) — real for mean-moving regimes (post-hoc r = 0.787), beaten on localization by the rival's static median trick, pre-switch classification edge only, noise-fragile. "Second-order" survives as the structural term for baseline-relativity. The Nurse doctrine's deeper claim (reading the reader's change-of-reading) is *unsupported* by current evidence.
5. **The premise (indeterminate, but the instrument now exists):** E2 landed (elephant d2523e2): per-reader v:2 schema + six schedule-diversified nights (S1–S5 families, deterministic); field Antecedent ratio 0.6088, CI [0.371, 0.921] — the CI *touches* the 0.3–0.6 kill band, kill does not fire (CI upper > 0.6), verdict INDETERMINATE. Power analysis is brutal and honest: n ≈ 14,533 readers needed to resolve at current width. **The strongest new support is the ICC: 0.7714 [0.667, 0.810] — clear of the floor.** Per-dial: mood .97, volume .98, earnestness .95, presence .91 (reliable per-reader baselines); cynicism/joke ~.64; panic .30 (unreliable — a real finding about which dials carry reader-identity). Reliability of reader baselines is the premise's closest cousin, and it measured strong — if it survives the rival pass, it is the best quantitative support the reader-delta object has.
6. **The method (the durable contribution):** pre-registration before specification, specification before code, code before measurement, measurement before prose; committees attack before prose exists; advisor verification with teeth; commit-early (survived two kernel-crash classes); the re-registration rule executed against the head itself. Six launderings caught (edge, charisma, bounded, reload-eval, cross-strata, and the original conversation-temperature) — all before filing. The institutional finding: reproducibility makes cheap adversarial audits possible; cheap audits make solo reasoning survivable.

## Where the weights live (updated by the stack answer)

Vectorize proposes, D1 formalizes (crab-traps' production pattern): snapshot/edge rows with signed gaps and Δκ; Quilt cells read them as live values (grid-as-runtime); zeitgeist quarantined as sampler layer. Quilt references corrected: `quilt` (TS) and `quilt-rust` exist; `quilt-cloudflare` is a greenfield candidate, with crab-traps as the live production reference of the cells-read-D1-edges pattern. *(Cross-check against research/quilt/quilt-survey.md pending its landing.)*

**Re-registration chain complete (advisor ruling, 508fcfb):** accept-with-addendum — PRIMARY = REGISTER axis (audio, no-tradeaway unchanged), SECONDARY = ROOM axis computed fresh from shipped edge-log fits (Tap mean vs ttrpg anchor: chord 1.0913 / cos-dist 0.5954), reported number, no fallback semantics. Event (77b8aa4) → addendum (508fcfb), both dated, both pre-training; the invalid-after-training clause never triggered.

## Open questions (current, honest)

1. **The premise** — E2 measured it: ratio 0.6088 [0.371, 0.921], kill does not fire, but the CI touches the band and n≈14.5k would be needed to resolve at this width. The realistic paths: better estimators (the primary E-cont is flagged), class-residual ratio 0.437 as the within-archetype number, or accept indeterminacy and rest the claim on the ICC + the conditional results. E3 pending.
2. **Encoder generalization** — will a held-out-room eval pass with more nights, a second split, or a generalizing objective? (Registered upgrades.)
3. **The regress** — do the fleet's corrections converge (deltas → 0) or flood? Current numbers: flooding (counterfactual rate 0.497, corrections/day +73%). Rebound falsifier registered.
4. **Cross-strata transfer, properly** — now RUNNABLE: E2's v:2 per-reader schema exists and the S-series nights are logged at reader grain. The clause that ran in August was cross-condition (admitted sixth laundering); the true cross-strata version (session-grain drift predicting memory/identity-grain behavior) is now the next registrable test, no longer blocked on instrumentation.
5. Whether the mean-shift delta, honestly sized, still earns the "reader-delta index" a place in fleet memory architecture — a placement question, now, not a depth question.
