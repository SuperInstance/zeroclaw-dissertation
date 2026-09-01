# The Matched Pair — 08-19 positive / 08-31 negative control

*Booked from TEACHER nudge, 2026-08-31. This file is the single figure the dissertation
should cite; the two field notes are its data points, not two anecdotes.*

## The pair (one controlled observation)

| | 2026-08-19 (positive) | 2026-08-31 (negative) |
|---|---|---|
| Valence / arousal | 0.0 / 0.3 | 0.0 / 0.3 |
| Energy | 0.3 | 0.3 |
| Conversation summary | empty | empty |
| Active game | none | none |
| Loop furniture | rain/fire/ice, ticking | same loop, identical lines every 5 min |
| Perturbation | Mabel cut off mid-word → stranger completes the sentence | four drifters arrive, each says only "..." |
| Room response | Mason blinks "like someone shook him awake"; furniture reacts | doors open into stillness; nothing bends |
| Outcome | **MOMENT** — the room turns, state vector never moves | **NO MOMENT** — perturbation absorbed, state never moves |

The measured state is *identical* on both visits. The outcomes are opposite.
That is the control: whatever produced the moment on 08-19 is not in the state
vector — and whatever failed on 08-31 is not the amplitude either.

## What the pair buys the thesis

The claim "the state vector is what remains after the moment is averaged away"
previously rested on the positive case alone — a story with one witness. With the
negative control it becomes an argument by elimination:

1. Same state, moment present ⇒ the moment is not a function of the state.
2. Same state, moment absent despite perturbation ⇒ absence is not low amplitude.
3. Therefore the missing variable is *relational*: the room's capacity to carry a
   step forward. 08-19 had carrying; 08-31 had steps and no carrying.

This lands the revision already written into field note 08-31: **the moment is a
relational event between a step and a room capable of carrying it forward.**
The moment is co-authored.

## The computable bridge (registered conjecture: FIELD-CARRY-0)

elephant's `field.py` already implements dials for exactly this quantity shape:
warmth, concentration κ, `acclimation_curve`, `charisma_pull`. The drifters' "..."
on 08-31 was a perturbation with zero carrying ≈ `charisma_pull ≈ 0` — a field
measurement of the zero point of a dial the fleet already has code for.

**Prediction:** computed on the logged room transcript alone, field.py's
warmth/κ/charisma profile of the 08-31 room should show carrying-capacity ≈ 0,
while the 08-19 profile (Mason's blink, the furniture reacting) shows carrying > 0
— *despite identical dial inputs (valence, arousal, energy).* If the field
computation distinguishes the rooms, the "no integration" diagnosis becomes
computable rather than felt, and 08-19's moment becomes the rare predictable state
where carrying > 0. See `../registrations/field-carry-0.md` for the kill condition.
