# FIELD-CARRY-0 — RESULTS (DECIDED)

*Run 2026-09-02. Registration: `../registrations/field-carry-0.md` (procedure + kill
condition read before any computation; heuristics frozen in `field-carry-0-run.py`
header BEFORE running). Script: `field-carry-0-run.py` (committed). Raw per-line
outputs regenerated idempotently by the script to `/tmp/fieldcarry/field-carry-0-output.json`.*

## Verdict: SURVIVE (strong) — on the length-matched condition, n = 2 caveat intact

The registered KILL condition (indistinguishable carrying-proxy distributions,
overlapping 95% bootstrap CIs) does **not** fire. The carrying-proxy separates the
two rooms in the registered direction, and — decisively — the separation **survives
and strengthens under the length-matched rerun** that SURVIVE-weak demanded.

## Headline numbers

| metric | 08-19 (moment occurred) | 08-31 (absorbed) | separated? |
|---|---|---|---|
| carry_mean (registered proxy) | **0.0921** [0.0876, 0.0969] | 0.0819 [0.0800, 0.0846] | YES — CIs disjoint |
| carry_max | 0.1766 [0.1319, 0.1766] | 0.1749 [0.0934, 0.1749] | no (overlap) |
| core warmth mean | 0.0636 [0.0621, 0.0652] | 0.0657 [0.0641, 0.0673] | disjoint but *inverted* — see below |
| core κ mean | 2.0715 [2.0670, 2.0758] | 2.0751 [2.0708, 2.0795] | disjoint but trivial margin |

Difference CI (10k bootstrap, means): **carry_mean diff = +0.0102 [+0.0051, +0.0154]**.

## The length-matched rerun — the confound check that made the result

The registration's SURVIVE-weak caveat: if the margin comes from transcript
richness (08-19 "has more lines"), rerun length-matched before claiming survival.
The confound was real-looking and *per-drifter*, not per-window: 08-19 drifter
lines average **792 chars**, 08-31 drifter lines average **3 chars** — and the
volume dial (via `min(len/300,1)`) feeds `delta`, which feeds `d_charisma`, which
feeds the carrying-proxy. So the raw margin could have been a length artifact.

Rerun with the length term stripped from the volume dial **identically in both
windows** (same frozen constants, only `L=0` substituted):

- 08-19: 0.0761 · 08-31: 0.0557 · **diff = +0.0204 [+0.0141, +0.0267]**

The separation did not shrink — it **roughly doubled**. The 08-19 room carries
*more* once you stop rewarding long lines. Transcript richness was masking the
effect, not creating it. Margin direction and size both satisfy SURVIVE-strong's
"separation holds on length-matched windows."

## Honest limitations (kept from registration, plus new ones)

1. **n = 2.** A feasibility probe. This upgrades the *next* registration
   (pre-registered "carrying > 0" as moment-predictor on future visits); it does
   not settle the doctrine.
2. The instrument is a *derived* dial mapping (lexical/behavioral heuristics,
   frozen in the script header), not field.py's native inputs — field.py's 7 dials
   are not the Tap's measured (valence, arousal, energy). The claim tested is
   "field.py's functional form, fed transcript-derived dials, separates the
   rooms" — a claim about the instrument's *shape*, not about measured dials.
3. Warmth and κ separate trivially and warmth's tiny margin runs the *wrong way*
   (08-31 microscopically warmer) — consistent with the registration's premise
   that flat dial readings miss the moment. The carrying-proxy (charisma_pull ×
   acclimation gain, per drifter arrival against the trailing room field) does
   the work. The room twin of this fact is the §6 finding: a field scalar that
   doesn't separate is exactly Δ₀-coarseness; the *relational* quantity does.
4. joke_landing is identically 0 (no `joke` speech_act in this data); charisma is
   uniform (signal_strength == 2 for all drifter rows → c = 0.35). Variation comes
   from field distance and room rate only.
5. Dispatch note: the compute ran local-only (numpy + the committed script); one
   mid-flight worker restart occurred before any output was produced — no partial
   reads influenced the run; the script is deterministic (seeded RNG) and was
   re-executed end-to-end.

## What this buys

The registered next step is now licensed: pre-register "carrying > 0 predicts a
moment" on the next visits and check it *before* reading outcome data. The
deepest thing seen: the room's ability to carry was invisible in every flat
scalar — warmth, κ, the measured dials — and visible only in the quantity defined
*relationally* (arrival against trailing field). That is the room twin of the
fiber result: separation lives in the move, not in the state.
