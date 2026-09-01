# FIELD-CARRY-0 — can field.py predict non-carrying from room state alone?

*Registered 2026-08-31, from the matched-pair observation (see
`../field-notes/MATCHED-PAIR.md`). Committed before any computation is run.*

## Claim under test

elephant's `field.py` quantities (warmth, concentration κ, `acclimation_curve`,
`charisma_pull`), computed from the Tap's room transcript + dial inputs, can
distinguish the 08-19 room (carrying > 0 — a moment occurred) from the 08-31 room
(carrying ≈ 0 — perturbation absorbed, no moment), even though the measured dials
(valence 0.0, arousal 0.3, energy 0.3) are identical.

## Procedure (runnable)

1. Extract both visit transcripts from the Tap logs (08-19 window around
   06:56 UTC; 08-31 window covering the drifter arrivals).
2. Run `field.py` over each transcript window: per-line warmth, κ, and
   charisma_pull of the perturbing agent(s) toward the room.
3. Read out: max and mean carrying-proxy (charisma_pull × acclimation gain)
   per visit.

## Kill condition

- **KILL:** the carrying-proxy distributions for 08-19 and 08-31 are
  indistinguishable (overlapping bootstrap 95% CIs on the max/mean), i.e. field.py
  sees two flat rooms where we observed opposite outcomes. The "computable rather
  than felt" bridge dies; the relational-moment claim stays prose-only and the
  dissertation must not cite field.py as its measurement instrument.
- **SURVIVE (weak):** 08-19 > 08-31 with non-overlapping CIs but the margin comes
  mostly from transcript richness (08-19 has more lines), not field structure —
  rerun length-matched before claiming survival.
- **SURVIVE (strong):** separation holds on length-matched windows; proceed to
  pre-registering "carrying > 0" as the moment-predictor on future visits.

## Honesty notes

- n = 2. This is a feasibility probe, not a result. Either outcome upgrades the
  *next* registration (pre-registered prediction on future visits), neither
  settles the doctrine.
- Status: **RUNNABLE — awaiting computation.** No partial reads before this file
  was committed.
