# E2 ADDENDUM — Ladder attempt 1 failed; estimator rebuild + planting extension

**Filed: 2026-08-19, after ladder attempt 1, BEFORE ladder attempt 2 and before any field number.** This addendum exercises the registration's own failure path (R6: "if neither passes, the ladder has failed — that is the finding of the day; no field number is filed and the estimator is rebuilt before E2's field arm runs"). Attempt 1's raw results are preserved verbatim at `elephant/data/e2/e2-ladder-attempt1.json`.

## A1. Attempt 1 result (as registered): LADDER FAILS

On fixtures, attempt 1 (E-seg / E-cont, actual-presence readings, λ-ray planting): rung 0.0 recovered at 0.176 (E-seg) / 0.168 (E-cont) against a planted truth of 0.088 — error +0.18, outside ±0.1; rungs 0.6 (2 of 3 reps) and 0.9 (all reps) could not be planted at all within λ ∈ [0, 6].

## A2. Diagnosis (three defects, two instrument-side, one model-side)

1. **Truth-anchor defect (implementation).** The registered invariant "λ=0 ⇒ 15 identical readers ⇒ true ratio exactly 0" was violated (truth 0.088 at λ=0): the S5 anchor inherited each template slot's interaction timeline, so identical readers received different anchors. The anchor must be reader-intrinsic.
2. **Participation conflation (a real bias of the attempt-1 estimator).** With actual-presence readings, identical-param readers still read differently because their inherited participation timelines differ (own-charisma displacement scales with interaction count). The attempt-1 estimator therefore measures participation-pattern differences, not only interpretive idiosyncrasy — a +0.18 floor at planted truth 0, on fixtures.
3. **Planting-family ceiling (model-side).** For some draws the λ-ray (uniform scaling of all parameter deviations) saturates near ratio ≈ 0.47–0.75: as gain spread grows, the common schedule displacement is differentially amplified into DRIFT, which grows as fast as spread. Vibe clamping (bounded dials) then pins spread. The λ-family cannot reliably construct rung 0.9 populations. This is a property of the reading-model's parameter space, not of the estimator — and it is reported as a finding in its own right: in this world, populations with premise ratio ≥ 0.9 are not constructible from field-distribution deviations along a single scaling ray.

## A3. The rebuild (attempt 2 instrument): canonical presence

Both the truth and the estimator use **canonical-presence readings**: each reader's replay substitutes the per-speak mean attendee interaction count `n̄(t)` (a logged, reader-independent fact of each night) for the reader's own count. Cold entrants still begin at their entry speak. This removes participation conflation by construction (identical readers ⇒ identical readings on every night ⇒ ratio exactly 0 at both truth and estimate), and makes the premise quantity **participation-deconfounded**: parametric interpretive spread ÷ schedule drift. The field number under this instrument measures the doctrine's antecedent (idiosyncratic interpretation), with attempt-1's actual-presence number retained as a labeled sensitivity variant (its conflation floor is attempt 1's own +0.18, on fixtures).

## A4. Planting extension (for rungs unreachable by the λ-family)

If the original λ-family cannot plant a rung (bisection unreachable within λ ∈ [0, 6]), plant via the **λ_vibe family**: scale ONLY `vibe_start` deviations from cast mean (λ_vibe ∈ [0, 10], bisected on canonical truth); dial_weights, charisma, acclimation stay at cast mean. This isolates spread from the drift-amplification channel (no gain spread) and remains within physical dial bounds. The population is labeled `planted-via-vibe` in the results. Rungs plantable by the original family keep it (continuity with the base registration).

## A5. Attempt-2 pass rule (unchanged thresholds)

Every rung, rep 0: |estimate − rung| ≤ 0.1 for E-seg-canonical (primary candidate) or E-cont-canonical (continuity). PASS ⇒ field arm runs with the passing estimator. FAIL ⇒ **second consecutive ladder failure**: the measurement (not the premise) is killed; the sentence is "the field cannot currently measure its own antecedent," and E2 stops with no field number filed.

*No threshold in the base registration moves. The kill band, verdict rules, power analysis, prefix discipline, and primary/secondary structure all stand as registered.*
