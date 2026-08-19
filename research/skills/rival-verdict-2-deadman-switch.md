# Rival Pass 2 — The Edge Framing Itself (and the Deadman Switch)

*Source: `/home/eileen/.openclaw/workspace/research/devils-advocate-edge-framing.md`, second devil's advocate (DeepSeek V4-Pro), 2026-08-19.*

## Verdict: STANDS-WITH-CONDITIONS — de facto FALLS today

The edge idea is correct and doctrine-native — it's the only thing that could separate "galley fight" from "galley coffee" — but it's built on the quantity the doctrine measured at statistical zero. **The idea is right; the object is empty.**

## The killer attack (laundry)

Pass 1 killed conversation-temperature citing the 0.015 within-room fine gap — then rebuilt the replacement on that *exact* within-room displacement, borrowing the cross-room edge's legitimate name (0.271). If the edge is cross-room it's a room walk, not a conversation; if within-room it's the retired target. No third reading. The 0.271 was never in doubt and is already served by room-snapshot retrieval.

## Other attacks

2. **μ̂ doesn't exist.** No shipped code computes a vMF mode; `JepaMemory._fields` is 2-D `[warmth, κ]` with the confessed-broken κ proxy. The "edge" is a delta of a vector no interpreter builds.
3. **`distance()` normalizes — magnitude deleted.** A whisper and a scream in the same direction are "the same edge." The felt size of the step — the thing that separates a fight from a quip — is unrepresentable.
4. **Cross-room collinearity is ill-defined.** Heterogeneous dial bounds ([−1,1] vs [0,1]), centers (rest at 0 vs 0.5), κ scales, presence masks. "Same push direction" across a sauna and a plunge pool is a metaphor, not a metric.
5. **Charisma key = popularity index.** `charisma_pull` is frequency-weighted (`s=1−e^(−charisma·n)`); the busiest speaker dominates the edge. Busy≠warm re-enters as "charisma."
6. **Cold-start.** Edges need two snapshots; single-message and field-invariant conversations (most nights) are unretrievable by construction.

## DEADMAN SWITCH — pre-registered 2026-08-19

1. **Threshold:** fine gap 0.015 → **≥ 0.10** cosine (2× the 0.05 noise floor), **speaker-heldout ≥ 0.50** (chance 0.25), within-room spread preserved.
2. **Failure:** three consecutive sub-threshold runs (or clearing it only by collapsing within-room spread) ⇒ edge thesis dead.
3. **Scope of kill:** conversation-as-edge retrieval layer ONLY. Room-snapshot retrieval, moment-grain `query_field`, cross-room edge (0.271) survive as fallback.
4. **Fallback thesis:** room-centroid/snapshot retrieval, cross-room only — dissertation-worthy iff it (a) generalizes beyond speech-vs-music to genuinely distinct speech rooms, and (b) true-κ MLE + spread regularizer avoid collapse.
5. **Honest floor:** if the fallback can't beat the already-shipped `query_field`, the deliverable is "the elephant was already built; here is the test harness."

## Concession condition (acceptance test for the vMF engineering spec)

A **runnable** μ̂/κ (real vMF MLE) where a within-room same-cast conversation displaces μ̂ above noise, AND matched edges retrieve "a fight, not merely another galley" across rooms with different presence masks — i.e. edge-similarity beats room-snapshot retrieval on a benchmark.

## Consequences for the dissertation

- The thesis now has a falsifiable core with pre-registered thresholds. This is a strength, not a wound — the dissertation can report either outcome honestly.
- The vMF engineering spec must ship: true κ MLE, magnitude-preserving edge metric (fix attack 3), per-room affine normalization for cross-room collinearity (fix attack 4), charisma de-frequency-weighted (fix attack 5), and a stillness/point-event channel so quiet nights aren't structurally invisible (fix attack 6).
- The cross-link: rival says μ̂ doesn't exist; the engineering scout is building the MLE that makes it exist. They meet at the 0.10 threshold.
