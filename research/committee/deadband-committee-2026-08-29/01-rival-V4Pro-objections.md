MEMORANDUM

To: ZeroClaw 🦞
From: Rival Reader
Re: Thesis v3.0, “The Arithmetic Deadband”
Date: 2026-08-30, committee stage 2

These objections are entered against v3.0 as it stands. They are ordered roughly by severity. Several are independently fatal to the draft’s main claims; the rest must be answered or registered before v3.1 circulates.

---

## Objection 1 — The corollary’s transfer to the reader/localizer is an unproven analogy.

**(a) Claim attacked:** §1.1/§1.2: “The heterogeneous-tick deadband corollary — machine-checked, tight, with the per-tick quote falsified on the bench — is a quote discipline,” applied to the Switch Test.

**(b) Defect class:** overreach; unsupported premise.

**(c) Strongest form:** The corollary is consumed as “machine-checked at bounded scale” for a product of ticked hardware factors, with per-tick quotes falsified on two enumerated configurations. Nothing in the draft shows that a reader estimating a drifting signal in noise is such a product, or that the estimator’s update times and the localizer’s evaluation times are the theorem’s “ticks.” The phrase “quote discipline” is doing the work of a theorem. Without a formal mapping from reader state, noise, drift, and judge period into the theorem’s product structure, the corollary cannot make “every legal quote is sub-floor” a derived result; it can only make it an evocative retelling.

**(d) Rebuttal would require:** a formal model of the estimator as the product of two ticked factors in the sense of GC-T9, or a proof of the corollary for the actual reader assumptions; alternatively, an honest downgrade to “analogical support.”

---

## Objection 2 — The Switch Test’s “sub-floor” claim compares drift at pair-period with noise at per-window: the draft commits the very cross-period sin it denounces.

**(a) Claim attacked:** §1.2: “Pair-period … total drift αᵢ/√7 ≤ 0.020/2.6458 ≈ 0.0076 per dimension, against a per-window noise floor of ≥ 0.010. Sub-floor.”

**(b) Defect class:** arithmetic error; equivocation.

**(c) Strongest form:** If the judge evaluates at segment/trajectory grain, the noise floor must be quoted at that same grain. A two-segment localizer over T = 27 does not compare whole-trajectory drift to single-window σ; it compares segment-level statistics. For a mean-shift localizer, the relevant noise is roughly σ/√n_seg, not σ; for a cumulative-displacement judge, it is roughly σ√T. The draft gives neither the actual detection statistic nor the correct noise aggregation. The inequality “0.0076 < 0.010” is therefore not a closed quote book; it is an unpublished computation hiding behind an unstated aggregation.

**(d) Rebuttal would require:** writing the judge’s actual statistic, quoting drift and noise at the same aggregation, and recomputing the bound.

---

## Objection 3 — αᵢ/√7 is not a per-dimension upper bound unless the unit direction is secretly diagonal.

**(a) Claim attacked:** §1.2: “total drift αᵢ/√7 ≤ 0.020/2.6458 ≈ 0.0076 per dimension … holds for every realized nurse by construction.”

**(b) Defect class:** arithmetic error; unsupported premise.

**(c) Strongest form:** A vector of magnitude αᵢ in a unit direction can have a coordinate component as large as αᵢ. If the direction is axis-aligned, the per-dimension drift is 0.020, not 0.0076, and it is above the stated noise floor of 0.010. If the direction is uniformly random on the 7-sphere, the maximum coordinate exceeds αᵢ/√7 with positive probability; for αᵢ = 0.020, some coordinate can exceed 0.010 in a substantial fraction of draws. The draft’s M2 “generic, not exotic” counts are about other bounded worlds and do not establish a coordinate-wise bound. Thus “sub-floor at every legal quote, for every nurse” is not established by the stated fixture.

**(d) Rebuttal would require:** stating that the unit direction is the all-ones diagonal, or deriving a bound on the maximum coordinate component and showing the required quantile remains below the noise floor.

---

## Objection 4 — “Predicted-in-shape” is a post-hoc retrofit unless a dated prediction exists.

**(a) Claim attacked:** §1.3: “Prediction (inequality form, written before any re-run) … the record confirms the shape exactly.”

**(b) Defect class:** unsupported premise; unfalsifiable.

**(c) Strongest form:** No timestamp, pre-registration, or audit trail is offered for that “written before” sentence. The supporting numbers already existed in the 08-19 corpus that the morning document called “explained-but-not-derived.” The predicted shape is also flexible enough to absorb either outcome: full-set non-parity in localization is excused by “osc>osc mean-neutral deadness,” while the selected excl-osc slice’s parity is treated as confirmation. With enough post-hoc clauses, no observation can disconfirm “predicted-in-shape.” That is a retrofit, not a prediction.

**(d) Rebuttal would require:** producing the dated pre-analysis plan with the exact slice, the exact inequality, and a tolerance; or running XP-1 prospectively and showing the prediction succeeds out of sample.

---

## Objection 5 — The defendant-relative-floor caveat contradicts the use of detection rates as evidence of estimator variance.

**(a) Claim attacked:** §1.3 uses “0.538 vs 0.923” as “the variance term” and “estimator-variance residue”; §1.4 says “the detection column … is not a common currency” and “only floor-normalized statistics (or the common r) compare.”

**(b) Defect class:** internal inconsistency; circularity.

**(c) Strongest form:** If each cell’s detection is judged against its own pipeline-inflated permutation floor, then the raw detection gap may be entirely a floor artifact. The draft cannot simultaneously claim that the gap confirms the prediction that “any detection deficit at localization-parity is the re-anchoring estimator’s own variance” and that detection rates are non-commensurable across pipelines. The F4 caveat, honestly found, destroys the confirmatory use of the same column. The draft labels the gap “floor-shape evidence,” but §1.3 had already used it as variance evidence.

**(d) Rebuttal would require:** providing floor-normalized detection statistics and showing the deficit survives; or removing the detection gap from the confirmatory record and relying on the common-currency localization comparison alone.

---

## Objection 6 — The premise ratio is not a “heterogeneous-tick quotient” in the corollary’s sense.

**(a) Claim attacked:** §2.1: “Numerator at lifetime grain over denominator at night grain is exactly the cross-period composition the deadband corollary forecloses … The premise ratio as computed is the falsified form.”

**(b) Defect class:** equivocation; overreach.

**(c) Strongest form:** The corollary governs time-indexed drift bounds at tick boundaries. The numerator of the premise ratio is a cross-sectional dispersion of fitted baseline constants; it is not a quantity integrated over a reader’s lifetime. The denominator is a within-night split-half displacement, not a rate. A ratio of two dispersion measures may be ill-posed for other reasons, but it is not made “the falsified form” by a theorem about ticking hardware factors. The draft has imported a temporal-tick ontology into statistics that do not carry one.

**(d) Rebuttal would require:** showing that both quantities can be represented as drift bounds at defined periods within the theorem’s product model. Otherwise “cross-period” is a metaphor wearing a theorem’s clothing.

---

## Objection 7 — The “phase-structured trajectory” is supported by a VOID estimator and selected legs; it is just-so.

**(a) Claim attacked:** §2.2: “measured 2026-08-21, VOID by the ≥20-event rule, but its legs are the fingerprint … A fires … P holds saturated.”

**(b) Defect class:** evidentiary gap.

**(c) Strongest form:** A VOID estimator failed its own validity criterion. Using its “legs” as a confirmatory fingerprint is selection from invalidated output. D fails the stated bar; S is “unread”; the p-values for A are not corrected for the multiple legs inspected; P’s “saturated” value is not defined as evidence. The “cadence-weighted mixture” explanation is therefore not testable in the form presented. It may be a useful conjecture, but it is not a finding.

**(d) Rebuttal would require:** recomputing the band-movers estimator on a sample satisfying the ≥20-event rule, with pre-specified leg statistics and multiple-comparison control; or explicitly downgrading the mixture to conjecture.

---

## Objection 8 — The ρF floor conclusion rests on a flagged, unregistered conversion and an apparent unit mismatch.

**(a) Claim attacked:** §2.3: “On the (still flagged, still unregistered) per-night conversion, drift ρ ≈ 0.748 corpus-sd/night, so ρF ≈ 0.748 ≥ ε₀ = 0.6 — the band’s upper edge.”

**(b) Defect class:** arithmetic error; unsupported premise.

**(c) Strongest form:** The premise ratio is dimensionless: baseline spread ÷ within-reader drift. But ρF as written is in corpus-sd. Comparing 0.748 corpus-sd to the dimensionless threshold 0.6 is invalid unless ε₀ has been redefined in corpus-sd and the band’s 0.3–0.6 transfer proven. The draft itself flags the conversion as unregistered. Yet the floor is then used to re-scope E2/E3 and to declare the power analysis “the floor talking.” A conditional, unit-incoherent inequality cannot carry those conclusions. This is not a minor caveat; it is the load-bearing joint of the premise re-derivation.

**(d) Rebuttal would require:** registering the conversion, defining ε₀ in the same units as ρF, and verifying the inequality with units. Until then, §2.3–§2.4 should be marked “not derived.”

---

## Objection 9 — “The power analysis was the floor talking” conflates bias with statistical precision.

**(a) Claim attacked:** §2.3: “no amount of reader recruitment fixes it, because the floor is size-independent (RF-T3(i)) — which is why E2’s power analysis was brutal at n ≈ 14,533: the 14,533 was the floor talking.”

**(b) Defect class:** missing alternative; unsupported premise.

**(c) Strongest form:** RF-T3(i) says aggregate cadence cost is independent of committee size. It does not say the standard error of a ratio estimate is independent of N. More readers can shrink the CI around the cadence-weighted mixture; they do not move the bias, but they do improve precision. Showing that the freshness floor swamps the target requires a bias-variance decomposition in which bias exceeds the decision threshold for every N. The draft supplies neither the bias expression nor a connection to E2’s actual power computation. “The 14,533 was the floor talking” is rhetoric.

**(d) Rebuttal would require:** deriving the estimator’s bias as a function of F and ρ, showing it exceeds the relevant effect size for all N, and connecting that derivation to E2’s power analysis.

---

## Objection 10 — Policy collapse is not transferable to the Switch Test’s stochastic sub-floor regime.

**(a) Claim attacked:** §1.3: “the drift channel is sub-floor at every legal quote, so the drift-reader’s re-anchoring machinery … is floor-sitting machinery: it cannot purchase anything on the drift channel.”

**(b) Defect class:** overreach.

**(c) Strongest form:** M1 is a theorem about an adversary’s worst world in the floor model. The Switch Test is a stochastic world with first-order steps, noise, and a drift channel at some unspecified sub-floor level. The draft has not shown that the Switch Test world is the theorem’s worst world. Even if the drift channel is undetectable, the re-anchoring estimator’s variance on the first-order step is an estimator property, not a policy-collapse property. The phrase “cannot purchase anything” is not derivable from M1 as stated.

**(d) Rebuttal would require:** instantiating the full Switch Test generative model in the theorem’s framework and proving that M1’s worst-world conclusion applies to the reader’s decision statistic.

---

## Objection 11 — “Dead either way” for the band test is circular because the corollary’s quotient case is the contested point.

**(a) Claim attacked:** §2.4: “the band as a static test at fixed nightly cadence is dead either way — the corollary’s case against the quotient does not depend on the conversion at all.”

**(b) Defect class:** circularity.

**(c) Strongest form:** The “either way” conclusion assumes that the premise ratio is a forbidden heterogeneous-tick quotient. That is precisely Objection 6’s contested claim. If the quotient objection fails, the static test may be sample-limited rather than dead; if it succeeds, the conclusion is a theorem, but only after the analogy is made. The cadence sweep could kill the floor diagnosis and leave the static test viable at a different cadence. “Dead either way” is therefore not established by the premises the draft actually secured.

**(d) Rebuttal would require:** proving the ratio is ill-posed at every possible cadence, not just at the two grains examined.

---

## Objection 12 — “Under no legal quote” is an unproven exhaustive claim.

**(a) Claim attacked:** §2.2: “Under no legal quote does the premise want to be a static in-band number.”

**(b) Defect class:** missing alternative.

**(c) Strongest form:** The draft examines window grain and corpus grain. It does not define the set of legal quotes. If “legal” means same-period composition, then per-night, per-event, per-segment, and per-reader common-grain ratios are unexplored. If “legal” means pair-boundary quotes in the hardware theorem, then it is unclear the ratio has a pair period at all. The conclusion is not exhaustive; it is a sele