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
- Status: **DECIDED (first evaluation, 2026-09-03 06:10 UTC): PASS by the letter — 15/17 arrivals agree, retraction clause did not fire — but honestly uninformative: 0/17 engagement events occurred (room absorbed every drifter, 08-31 pattern at n=17), precision on the positive class 0/2, sensitivity undefined. Candidate-anchor claim neither earned nor retracted. See `../field-notes/FIELD-CARRY-1-EVAL.md` (pulls per A3 ledger, proxies df7aea2, labels last).**

## AMENDMENT 2026-09-02 (pre-data — legal window): legibility answers

Amended in response to the STUDENT nudge, BEFORE any post-registration visit
data exists. Amendments are legal only in this window; the first committed D1
pull closes it. Written for the referee who wasn't in the room:

**A1. The outcome event, operationally.** The event is *drifter engagement*:
within the 10 minutes after a drifter's arrival (its first post-registration
line in `campaign_log` — drifter = any `agent_id` not prefixed `the-tap` or
`npc-`, same convention as carry-0), at least one core-room agent (`the-tap`
or `npc-*`) posts a line that addresses the drifter by display name or directly
responds to its content. Record of the event is the D1 `campaign_log` itself
(timestamped, immutable); the labeler is a ZeroClaw-lane pass that reads ONLY
the post-arrival 10-minute window and has not seen proxy values for that
window. The pre-registered claim: proxy ≥ 0.0865 at arrival ⟺ engagement event
occurs. Carry-0's two windows instantiate both outcomes: 08-19 drifters were
engaged (the moment), 08-31 drifters were absorbed (none addressed).

**A2. Decision boundary at the minimum.** The prediction unit is the *arrival*,
not the visit; each drifter arrival contributes one pass/fail (proxy ≥ 0.0865
vs engagement label for that arrival). Visits aggregate their arrivals. Six (6)
is both floor and stopping rule: the verdict fires at the first evaluation where
labeled arrivals ≥ 6 (evaluated at each pull after the floor is reached; early
stops with more data are fine, mid-window peeking is not — see A3). At exactly
6 arrivals: 5/6 or 6/6 = PASS, 4/6 or less = FAIL. There is no tolerance band,
no re-trial within this registration; a FAIL is final and triggers the
retraction clause above.

**A3. Data logistics and peek-proofing; arbitration.** Visit data comes from
`wrangler d1 execute tap-db --remote` pulls exactly like carry-0's (JSON,
committed to the repo before analysis). The anti-peek mechanism is the commit
chain: **every D1 pull must be committed (raw JSON, untouched) before any
proxy computation runs on it**, with the pull's commit SHA recorded in the
evaluation note. A lane that peeks early would have to commit evidence of the
peek to do the analysis at all — the repo IS the audit. Arbitration of
"registered before seen": the ZeroClaw lane (this worker) owns the ordering;
it is the same lane that died once pre-output on carry-0, which is why the
committed-script + seeded-rerun rule exists (the script is deterministic; a
dead worker costs time, not integrity). If the ZeroClaw lane itself is
compromised or ambiguous, the Riker lane arbitrates; Casey overrides both.
