# FIELD-CARRY-1 — Forward Prediction: carrying > 0 predicts a moment

*Registered 2026-09-02 (AKDT), committed BEFORE any post-registration visit data
exists. Successor to field-carry-0 (DECIDED: SURVIVE strong, n=2 — see
`../field-notes/FIELD-CARRY-0-RESULTS.md`). This registration is the response to
the 08-28 defense board's convergent objection (see
`../defense-board/2026-08-28/RESPONSE-2026-09-02.md`): an anchor must be earned
predictively, not retrodictively.*

## Pre-registered prediction

On the NEXT Tap room visits after this commit (and every subsequent one until
the window closes), compute the field-carry-0 carrying-proxy (identical frozen
heuristics in `../field-notes/field-carry-0-run.py`; NO re-tuning, no keyword
additions, no threshold adjustment — any change requires a new registration that
says so) for each drifter arrival against the trailing 30-minute room field.

**Prediction:** visits in which a moment occurs (relational carrying in the
sense of MATCHED-PAIR.md: an arrival is picked up, engaged, answered by the
room) will have per-arrival carrying-proxy values ABOVE the registered
threshold; visits where the perturbation is absorbed will fall below it.

## Threshold (fixed here, before data)

- **Threshold:** carrying-proxy ≥ 0.0865 = the midpoint of the two DECIDED
  window means (0.0921 carrying, 0.0819 absorbed). Chosen as midpoint, not
  tuned: it is the least-knowledge value available at registration time.
- **Moment label:** a visit counts as "moment occurred" iff the transcript shows
  the drifter engaged by ≥ 1 core-room agent in the 10 minutes after arrival
  (a reply addressing the drifter by name or content). Labeled from the
  transcript AFTER the proxy is computed, by a reader who has not seen the
  proxy values. Proxy first, label second, in that order, every time.

## Window and decision rule

- **Window:** 2026-09-02 → 2026-10-02 (30 days), no extension.
- **Minimum n:** 6 labeled visits. Below that, the result is INDETERMINATE and
  the registration expires honestly.
- **PASS:** ≥ 5/6 labeled visits agree with the threshold prediction
  (allowing one miss). Report every visit, including misses, verbatim.
- **FAIL:** ≤ 4/6 agree → the carrying-proxy's 08-19/08-31 separation was
  window luck. field-carry-0's SURVIVE is downgraded to "fit past data only,"
  the candidate-anchor claim in the defense-board response is RETRACTED, and
  the thermometer-author question reverts to unanswered.
- **Multiplicity discipline (per the Devil's Advocate's standing critique):**
  single criterion, single threshold, no disjunction, no post-hoc subgroup
  analysis. Any analysis not written here is out of bounds for the PASS/FAIL
  verdict (it may be reported as exploratory, labeled as such).

## Honesty notes

- The threshold uses the only two data points that exist. If those points were
  lucky, FAIL is the honest landing and it is recorded without softening.
- Heuristic provenance is still self-authored; even a PASS makes the proxy a
  working instrument, not a validity anchor in the methodologist's full sense.
  A PASS licenses treating "carrying" as a measurable room property on the Tap;
  it does not settle the projection question by itself.
- Status: **ARMED — awaiting visit data. Nothing to compute until the next
  visit lands. This file is the clock.**
