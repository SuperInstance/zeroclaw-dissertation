# FIELD-CARRY-1 — EVALUATION (first decision point reached)

*Evaluated 2026-09-03 ~06:10 UTC. Ordering per A3 held: pull committed (770ee4e) →
proxy values committed (df7aea2) → labels computed last, by this pass. Window runs
to 2026-10-02 but the A2 rule fires at the first evaluation with ≥6 labeled
arrivals; 17 are available.*

## Per-arrival results (threshold 0.0865; engagement label per A1)

All 17 in-window drifter arrivals: **NO engagement event** — zero core-agent lines
address any drifter by name in any 10-minute post-arrival window; drifter content
is uniformly `'...'`, so no content-response is possible either. The room's core
lines are ambient loops (rain, fire, Barnacle's glass, Sage's notebook) — the
08-31 absorption pattern, now at n=17.

| arrival | proxy | predicted | label | agree? |
|---|---|---|---|---|
| 00:05:05 Jess | 0.1558 | POS | not-engaged | ✗ |
| 00:10:05 Cora Quill | 0.1027 | POS | not-engaged | ✗ |
| 00:35:27 Jess … 04:10:30 Captain Reed (15 arrivals) | 0.065–0.080 | NEG | not-engaged | ✓ ×15 |

## Verdict: **PASS by the letter of A2 (15/17 ≥ 5/6) — and honestly uninformative**

The registered rule fires PASS: 15/17 arrival-level predictions agree, floor met.
**The retraction clause does not fire.** But writing PASS without its shape would
be the tapestry's sin, so:

1. **The pass is base-rate degenerate.** Zero engagement events occurred. A rule
   that predicted "never engaged" for every arrival scores 15/17 in a stretch
   where the room carries nobody. Agreement with a null stretch validates nothing.
2. **Precision on the positive class: 0/2.** Both proxy-positive arrivals (Jess
   0.1558, Cora Quill 0.1027 — the two highest scores in the sample) were false
   positives. Sensitivity is *undefined* — the moment never happened, so the
   proxy never got the chance to detect it.
3. **What the 17 actually show:** the room absorbed every drifter, exactly as on
   08-31 and unlike 08-19. The proxy's top scores landed on the two earliest
   arrivals, where trailing room-field structure was densest — consistent with
   the proxy measuring *room richness at arrival*, not the room's disposition to
   carry. That is a real observation, and it is not the registered claim.

## Anchor status (per the defense-board response)

The candidate-anchor claim is **NOT earned**. It is also **not retracted** — the
FAIL clause (≤4/6) did not fire, and the registered decision rule returns PASS.
The honest landing is: *instrument survived its first forward exposure with no
false negatives and no opportunity to demonstrate true positives; the anchor
question remains open and now has a sharper form* — the 08-19-style moment has
not recurred in the sample; until one does, "carrying > 0 predicts a moment" is
untestable, not untested-true.

## Next (pre-registered here, in the same discipline)

The window runs to 2026-10-02. Continue pulls; the decision rule stays armed for
**a future evaluation only if an engagement event actually occurs** — the
informative stratum. Arrivals predicted NEG and labeled not-engaged are no longer
evidence either way (they are the base rate); this is a reporting rule, not a
threshold change — the A2 verdict above stands as fired.
