# vMF Engineering Spec — Gate Review (ZeroClaw, 2026-08-19)

*Full spec: `~/.openclaw/workspace/research/vmf-engineering-spec.md`. This file is my gate review, not a duplicate.*

## What the spec delivers

- **True κ MLE, runnable:** window the room (W=8), standardize dials to z∈[−1,1], Newton-solve A₇(κ)=ρ with a numpy-only closed-form half-integer Bessel ratio (~90 lines, `elephant/vmf.py`). Guards: κ=None under N<10 windows, ρ≤0.999, κ≤500, bootstrap CI, jackknife SE(μ̂) doubling as drift deadband.
- **Warmth disambiguated:** warmth_vMF = ŵ·μ̂ (projection); κ = tightness of ρ. Warmth reads μ̂ only; ρ is rotation-invariant — warmth cannot move κ *by construction*. v0's center-mismatched extremity proxy retired from comparison paths.
- **Edge log on existing TapNightSession:** ~60 additive lines, JSONL (session_open / speak / session_close), order-of-arrival (seq), presence_mask, first_by_author, raw field (already computed and discarded in `speak()`), inline fits. Replayable; no rewrite.
- **Night D newcomer intervention** (entry at seq≈60%) as the only clean charisma-vs-acclimation separator.

## Acceptance-gate scorecard (Lucineer's 3-part gate)

| Gate condition | Status |
|---|---|
| 1. Runnable μ̂ via true MLE | 🟡 **Spec + code sketch, not yet run.** Buildable this week per the scout; I haven't executed it. |
| 2. Same-cast conversation displaces μ̂ above noise | ❌ **Not yet — dial-space noise floor is unmeasured** (0.05 is encoder-side). Nights A–C of same cast measure it; until then edges log `real: null`. |
| 3. Matched-edge retrieval beats room-snapshot retrieval | ❌ **Blocked on the contrast head** (gate 1 of the 7) — the DialBank cannot move the fine-gap number. |

**Score: path delivered, proof not.** The spec honestly marks itself "descriptive tier, not the v3 trained room-embedding."

## Highest-risk assumption (the tripwire)

Dial-axis near-orthogonality/isotropy after standardization. Mood/panic/cynicism share lexical triggers; v0 dials saturate → κ partly measures *dial-construction agreement*, not room tightness. Tripwires: axis_spread anisotropy ratio > 3, or |corr(warmth_vMF, log κ)| > 0.8 across ≥4 nights ⇒ report κ as direction-dependent or whiten. Otherwise the snapshot silently re-imports the warmth/κ confound the gate exists to kill.

## Fits with the advisor caveats

- Normalization scoping honored: z-standardization is for the *sphere work only*; `distance()`/contrast stay raw.
- Stillness as doctrine honored: quiescent windows skipped; N<10 ⇒ κ=None, never a fake number — "the room has nothing to retrieve" is encoded, with edge `real` flags deadbanded rather than guessed.

## Next steps (mine)

1. Get the ~90-line `vmf.py` + ~60-line tapnight instrumentation actually built and run (needs an implementation pass, then Nights A–D logged).
2. Until gates 2–3 close, no dissertation prose claims the edge exists — only that it is now *specifiable*.
