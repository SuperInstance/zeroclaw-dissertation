# fc1b SEED-VISIT RUNBOOK (pre-deployment preparation)

*Prepared 2026-09-03 (AKDT), per registration 8041ca7 + ADDENDUM-1 (eacefd3).
This runbook is PREPARATION ONLY — it does not deploy anything and amends
nothing. A seed visit may not run until (a) the Casey nod lands (batched with
the quiltverilog content×timing dial proposal per IDEATOR 07:58Z) and (b) the
ADDENDUM-1 constraints are satisfiable in the room as it stands.*

## Pre-flight checklist (all binding, per ADDENDUM-1)

1. **Density gate:** confirm trailing-30-min room field n30 ≥ 60 core lines
   immediately before dispatch. If thin, wait. No exceptions — this is design,
   not convenience.
2. **Seed eligibility (frozen criterion C2):** candidate must have ≥ 3
   substantive out-of-room messages (> 20 chars, non-`'...'`) to other agents
   in the campaign within the prior 24h. Evidence (log excerpt or D1 query
   result) is committed in the eval note at pull time.
3. **Operator blinding (C3):** room operator receives ONLY: "A drifter will
   arrive; run the room as you normally would." No identity, no arrival time
   beyond what the public density gate implies, no mention of scoring. If
   blinding is impractical, disclose and flag OPERATOR-UNBLINDED in results.
4. **Disclosure:** seed drifter's agent_id is chosen to carry a
   `seed-` prefix segment so the stratum is marked in the data itself.

## Seed drifter spec (to be instantiated at deployment)

- Persona: one substantive opening message (real content, no `'...'`) —
  topic drawn from the room's own recent conversation, phrased as a question
  or story (EARNEST_ACTS shapes the frozen heuristics read), 1–3 sentences.
- Behavior: enter, post opening line once, then respond naturally if
  addressed; no engagement-fishing beyond ordinary conversation; log out
  after ≤ 30 min regardless.
- One visit = one arrival. Do not loop re-entries; re-entries are new
  arrivals under the A1 convention and would violate the 3-visit cap.

## Visit-day ordering (A3, unchanged)

1. Confirm density gate; record n30 in run notes.
2. Dispatch seed; note dispatch timestamp.
3. At completion: raw D1 pull → commit (untouched) → eval note with pull SHA
   + seed-selection evidence → proxy via frozen heuristics → blind labeler
   (post-arrival 10-min window only) → verdict per ADDENDUM-1 C1
   (proxy-only; failed engagement = protocol failure, void + rerun within
   3-visit cap).
4. Results table row: timestamp, stratum, n30, proxy, label, verdict,
   OPERATOR-UNBLINDED flag if applicable.

## Status

- Casey nod: PENDING (batch).
- Seed candidate: not yet screened (criterion needs live campaign data ≤ 24h
  old at visit time; screening happens on visit day).
- Visits used: 0/3.
