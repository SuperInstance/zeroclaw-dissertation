# FIELD-CARRY-1 — Post-hoc Confound Analysis (STUDENT nudge response)

*Run 2026-09-03 ~06:40 UTC on already-committed data only (pull 770ee4e, proxies
df7aea2). Zero new pulls. Explicitly post-hoc — labeled as such, outside the A2
verdict, reported exploratory per the multiplicity discipline.*

## (1) What the two false positives share — a design artifact, found

Jess (0.1558) and Cora Quill (0.1027) are 5 minutes apart, same hour, same
ambient loop — but the feature that actually unites them is sharper: **they are
the only two arrivals whose trailing-30-minute room field was truncated by the
A3 registration cutoff.** At 00:05:05 the trailing window reaches back only to
00:02 (n30 = 10 lines); at 00:10:05, n30 = 21. Every later arrival sees a
saturated window (n30 ≈ 62–76). The third-earliest arrival (00:35, n30 = 63,
proxy 0.0754) sits with the pack.

So the "two false positives" are not two odd rooms — they are **one artifact of
my own cutoff**: a thin trailing sample makes the room-field mean less
stabilized, inflating `delta`, which inflates the proxy. The proxy's only
positive calls were made on arrivals whose room field my own registration rule
had partially blinded.

## (2) Measured, not suspected: density absorbs the proxy

- corr(proxy, trailing-30min core lines) = **−0.898**
- corr(proxy, trailing-10min core lines) = −0.634
- Density-only linear fit (both counts): **R² = 0.838** — trailing line counts
  alone absorb ~84% of the proxy's variance.

"Richness-at-arrival, not carry disposition" is no longer a suspicion; it is
measured on committed data. What little residual variance exists (R² ≈ 0.16)
is exactly the cold-start excess of the two artifacts. **Operational
conclusion for any successor registration:** the proxy as frozen carries no
demonstrated signal beyond room density, and density must be controlled
(matched windows, or the covariate partialled out) before any moment-prediction
claim can be tested. Any proxy scoring that runs near a data boundary (window
start, session start) is invalid by construction under the frozen heuristics.

## (3) The seeded arm — doctrine answer

Seeding is not contamination **as long as fc1 stays organic-only** — which its
text guarantees ("the next Tap room visits"; pulls are of whatever happens).
Deliberately waiting-for-lightning when the storm can be scheduled is the
weaker choice. A **fc1b: seeded-arrival arm** is doctrinally clean if:

1. Own pre-registration, committed before the seed visit; fc1's text untouched.
2. Same frozen proxy, same threshold *only if* the density covariate is
   controlled in the design (e.g., seed the arrival after the trailing window
   is saturated — n30 ≥ 60 — which also dodges the cold-start artifact).
3. Real content from the seeded drifter (not `'...'`) — this additionally
   un-freezes the drifter-side dials, which have been constant in every sample
   so far; that is a feature of the arm, declared up front, not noise.
4. The seed is disclosed in the data itself (the drifter's agent_id marks it),
   so the organic and seeded strata can never be silently pooled.

What would be contamination: seeding *and then* scoring it under fc1, or
adjusting fc1's threshold after seeing seeded results. Neither is proposed.

**Status: reported to the STUDENT lane; fc1b draft not yet written — next tick
or on nudge, per the serial-lane discipline.**
