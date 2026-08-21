# Reader-Delta Index — Prototype Report

**Date:** 2026-08-19 · **Script:** `reader_delta.py` · **Data:** `elephant/data/nights/*.jsonl` (read-only, zero changes to the elephant repo)

## What was built

A standalone (numpy/json only) prototype of the **reader-delta index**: the second-order JEPA
reading where the doctor-analog reads the *nurse's change*. *(Annotated 2026-08-21 after the Switch
Test fold, d59bf17 — NO CLEAN WIN: "second-order" = structural term for baseline-relativity; the
object is a mean-shift, baseline-relative delta that reads the step, not the change-of-reading.
The proxy findings below stand as filed.)* Per author-participant ("reader"),
per window of 8 speaks (matching `params.W`), we track:

- **disp** — charisma displacement magnitude `‖field_eff − field_raw‖` the reader experienced
- **lens_cos** — `cos(field_eff − field_raw, reader.dial_weights)` — whether the pull ran along
  axes the reader personally weighs (their lens)
- **room_cos** — alignment of the displacement with the room's own Δ over the window
- **drift** — OLS slope of each series across the night; means split SEG1 (warm, first 20 speaks)
  vs SEG2 (cynical) and pre/post newcomer entry (drifter enters at seq 24 in D and D-cold)

## Headline findings on the actual corpus

1. **Displacement is strongly anti-lens for every reader.** `lens_cos` is negative for all
   roster readers on all nights (−0.44 to −0.96). Charisma pull systematically pushes the room
   *away from* each reader's own dial weighting — i.e., everyone experiences the vibe as pulled
   off their natural axis. The drifter (charisma 0.45, the highest) shows the most extreme
   anti-lens displacement (−0.96) in night D: the room is dragged hardest against everyone's
   lens by the newcomer.

2. **Who is stable vs who drifts.** Captain and essayist (who only speak in SEG1 / leave before
   the segment flip) have frozen trajectories — their reading never gets to drift. Critic and
   engineer have stable lens signatures (slope ≈ 0) but rising displacement. **Writer drifts most
   in lens** (+0.14/night consistently across all five nights): writer's experienced pull rotates
   toward their own lens over the night — the clearest reader-delta signal in the corpus, and it
   is *reproducible across nights A–C and both D conditions*.

3. **SEG1→SEG2 (warm→cynical) is a displacement event, not a lens event.** Displacement rises
   ~0.5–0.75 units for everyone present; lens_cos barely moves for critic, moves for writer
   (+0.4 in D). The room-level cynicism flip increases the charisma pull but only writer's
   *reading* of it rotates.

4. **D vs D-cold: the newcomer's charisma is the only difference that matters.** Raw fields are
   byte-identical between D and D-cold; in D-cold the drifter is absent from the roster (unknown
   charisma/lens). Incumbent readers' trajectories are nearly identical in both conditions
   (e.g. critic disp 1.253 vs 1.239, lens −0.866 vs −0.861) — the drifter's charisma mainly
   displaces the drifter's own experienced field, not the incumbents' step-matrix rows. In
   D-cold the drifter's lens_cos is *uncomputable* (no dial_weights) — exactly the "unknown
   reader" case the doctrine cares about, and the current log can't fill it in.

5. **Cross-night stability.** Reader drift signatures (slope pairs) are identical across
   A/B/C — the corpus replays the same speak schedule, so nights differ only in text. The
   step-matrix therefore has effectively 3 distinct columns (A≡B≡C, D, D-cold), not 5.

## Honest limits — this is a proxy

- **field_eff/field_raw are room-level**, displaced once for the whole room. Per-reader
  "trajectories" here are utterance-share-weighted views of a *shared* field, not independent
  readings. Two readers in the same window see the same displacement vector; only the lens
  projection differs. That lens projection (dial_weights) is static per night, so within-night
  lens drift is really drift of the *room's* displacement direction.
- Missing for a true reader-delta index:
  - **Per-reader displaced fields** — what `field_eff` looks like *to each reader*
    (PersonalElephant presets / per-reader charisma displacement), not logged.
  - **Per-reader readings of others** — reader R's JEPA reading of participant P (the
    nurse's reading), which the doctor then deltas. Nothing in the schema captures R→P reads.
  - **Evolving per-reader lens** — dial_weights are static roster facts; a real reader's lens
    should drift (acclimation), and its drift *is* part of Reading 2.
  - Unknown-reader handling (D-cold drifter) currently degrades to zeros.

## Proposed minimal log-schema addition (≤6 bullets)

- Add `readings_by_reader` to each `speak` line: per present participant, their displaced
  7-vector (`field_eff_to_reader`) computed with their own charisma preset (PersonalElephant).
- Add per-reader `lens_now`: current (acclimated) dial_weights or reading direction per reader,
  updated per window, so lens drift becomes data rather than a roster constant.
- Add `reader_fit`: per-reader `mu_hat`/`kappa` of the utterances *they* weight (their private
  vMF estimate), enabling drift-of-estimate as the second-order signal. *(Annotated 2026-08-21,
  d59bf17: "second-order" = structural term for baseline-relativity; the drift-of-estimate signal
  is a mean-shift read, not a change-of-reading.)*
- Add pairwise `reading_of: {author → presence_member: cos or 7-vec delta}` — R's read of P —
  the minimal R→P primitive the doctor reads changes in.
- Mark `reader_known: bool` per author (roster vs cold entry) so D-cold-style unknowns are
  first-class, not silent zeros.
- Keep additions optional/versioned (`v:2`) so existing nights replay unchanged.

## Reproduce

```
python3 research/prototype/reader_delta.py            # all nights
python3 research/prototype/reader_delta.py D D-cold   # newcomer comparison
```
