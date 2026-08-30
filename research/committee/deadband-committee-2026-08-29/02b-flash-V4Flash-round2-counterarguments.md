# Counterargument Round — Candidate's Advocate Response to Rival Memo

---

## Objection 1 — The corollary's transfer to the reader/localizer is an unproven analogy.

**REBUT.**

The rival demands a "formal mapping from reader state, noise, drift, and judge period into the theorem's product structure." But the draft never claims the corollary *derives* the Switch Test's sub-floor claim — it claims the corollary provides a **quote discipline**: a normative rule about which period to quote drift at. The draft's §1.2 applies this discipline by identifying the two tick structures: the reader's update times (per-window) and the judge's evaluation times (segment/trajectory grain). The theorem's content — that quoting divergence at a shorter period than the judge's evaluation period is the *arithmetic error* the corollary forecloses — transfers directly because it is a statement about the *relationship between quotation period and evaluation period*, not about the specific hardware. The machine-checked falsification of per-tick quotes on (3,2) and (5,2) demonstrates the *principle*: shorter-period quotes underestimate the bound at the judge's evaluation instant. The draft's application to the reader/localizer is an *analogical extension* of this principle, and the draft says so: "The content is a quote discipline" (§1.1). The rival's demand for a full formal model confuses "applying a discipline" with "proving a theorem about a specific estimator." The discipline's content — quote at the judge's period — is what transfers; the specific numbers (ρ_pair, Δ) are what would need re-derivation, and the draft does not claim to derive them.

However, I concede the draft's §1.1 phrase "machine-checked, tight, with the per-tick quote falsified on the bench — is a quote discipline" could be read as claiming the theorem *applies* rather than *motivates*. The honest rewrite: "The corollary — machine-checked on ticked hardware products — motivates a quote discipline: quote drift at the period the judge evaluates. Applied to the reader/localizer as an analogical extension, this discipline yields..."

---

## Objection 2 — The Switch Test's "sub-floor" claim compares drift at pair-period with noise at per-window: the draft commits the very cross-period sin it denounces.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: the draft's §1.2 compares whole-trajectory drift (αᵢ/√7 ≈ 0.0076 per dimension) against per-window noise (σ ≥ 0.010 per dimension). If the judge evaluates at segment grain, the relevant noise aggregation is different. The draft *does* say "The reader's judge — the two-segment localizer — evaluates at segment/trajectory grain" (§1.2), but then quotes the noise floor at per-window grain. This is internally inconsistent.

The honest rewrite: "**Pair-period (whole-trajectory) quote:** total drift αᵢ/√7 ≤ 0.020/2.6458 ≈ 0.0076 per dimension. For a mean-shift localizer over T=27 windows, the relevant noise at segment grain is σ/√(n_seg) per dimension — for n_seg ≈ 13, this is σ/3.6 ≥ 0.010/3.6 ≈ 0.0028. The drift (0.0076) is NOT sub-floor at this aggregation. The sub-floor claim therefore requires a different judge model — one where the noise floor at trajectory grain is σ√T or similar — and this is not established in the draft. **The quote book is open on this point; the sub-floor claim is pending the judge's actual statistic.**"

---

## Objection 3 — αᵢ/√7 is not a per-dimension upper bound unless the unit direction is secretly diagonal.

**REBUT — with a partial concession.**

The rival is correct that a unit vector in R^7 can have a coordinate component as large as αᵢ (if axis-aligned) and that for uniform random directions, the maximum coordinate exceeds αᵢ/√7 with positive probability. The draft's claim "αᵢ/√7 ≤ 0.020/2.6458 ≈ 0.0076 per dimension" is indeed wrong as a *coordinate-wise* bound.

But the draft's actual claim in §1.2 is about the **total drift per dimension** in the context of the localizer's statistic. The two-segment localizer compares means of segments; for a mean-shift detector, the relevant quantity is the *projection* of the drift onto the mean-shift direction. If the drift is in a random direction, its projection onto any fixed direction has expected magnitude αᵢ/√7, and the *worst case* over directions is αᵢ. The draft's "sub-floor by construction, for every realized nurse" (§1.2) requires the worst case over directions to be below the noise floor — which fails for axis-aligned drifts.

**Concede the arithmetic error and rewrite:** "**Pair-period quote, worst-case over direction:** total drift ≤ αᵢ ≤ 0.020 per dimension (axis-aligned worst case). This is NOT sub-floor against per-window noise ≥ 0.010. The sub-floor claim requires either (a) a bound on the maximum coordinate for the actual direction distribution, or (b) a mean-projection argument where the localizer's statistic averages over dimensions. Neither is established in the draft. **The quote book is open on this point.**"

---

## Objection 4 — "Predicted-in-shape" is a post-hoc retrofit unless a dated prediction exists.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: the draft's §1.3 claims "Prediction (inequality form, written before any re-run)" but provides no timestamp, pre-registration, or audit trail. The supporting numbers existed in the 08-19 corpus before this claim was written. The "predicted-in-shape" language is unfalsifiable as presented.

The honest rewrite: "**Post-hoc shape match with a registered prediction for future runs:** the inequality 're-anchor ≤ static on detection at r-parity in sub-floor corpora' is registered as ZC-C2 (with kill condition). The 08-19 record is consistent with this inequality (0.538 vs 0.923 at r-parity), but this is a *retrospective* consistency check, not a prospective prediction. The prospective test is XP-1's d ≤ 1σ arm, which will adjudicate ZC-C2 out of sample."

---

## Objection 5 — The defendant-relative-floor caveat contradicts the use of detection rates as evidence of estimator variance.

**REBUT.**

The rival claims internal inconsistency: the draft uses detection rates as variance evidence in §1.3 while §1.4 says detection rates are non-commensurable. But the draft *does* address this: §1.3's use of detection rates is specifically qualified by the r-parity condition — "any detection deficit at localization-parity is the re-anchoring estimator's own variance" (emphasis on *at localization-parity*). The rival's objection conflates two distinct claims:

1. **Detection rates are non-commensurable across pipelines** (the defendant-relative floor caveat, §1.4).
2. **Within a single cell, detection deficit at r-parity indicates estimator variance** (§1.3).

The second claim does not compare detection rates across cells; it uses the *within-cell* relationship between detection and localization. If a cell's r matches the static baseline (parity on the common-currency localization metric) but its detection is lower, *within that cell's own floor-relative metric*, that is evidence of the estimator's own variance — the floor is the cell's own, so the deficit is relative to the cell's own null. The rival's objection would only hold if the draft compared detection rates *across* cells, which it does not do in the confirmatory claim. The §1.4 caveat is about cross-cell comparison; §1.3's claim is within-cell.

However, I concede that the draft's §1.3 phrase "the variance term, half the rate" could be read as comparing 0.538 to 0.923 across cells, which would violate the caveat. The honest rewrite: "detection 0.538 vs the cell's own permutation floor (which for the drift-reader is inflated by its pipeline), at r-parity with static — the deficit relative to its own floor is the estimator-variance residue."

---

## Objection 6 — The premise ratio is not a "heterogeneous-tick quotient" in the corollary's sense.

**REBUT.**

The rival claims the premise ratio's numerator (cross-sectional dispersion of fitted baselines) and denominator (within-night split-half displacement) are not "time-indexed drift bounds at tick boundaries" in the corollary's sense. But the draft's §2.1 makes a specific temporal claim: the numerator is "fitted per reader *across nights* — n_nights ≥ 3, a reader-lifetime-grain quantity" and the denominator is "measured *within nights* — a within-night-grain dispersion." These are temporal grains in exactly the sense the corollary addresses: the numerator accumulates over a longer period than the denominator. The corollary's content — that joining quantities at different periods in one bound is the arithmetic error — applies directly to a ratio whose numerator and denominator are measured at different temporal grains. The rival's objection that these are "dispersion measures, not rates" misses the point: the corollary is about *periods of measurement*, not about whether quantities are rates or levels. A dispersion measured over nights and a dispersion measured within nights are quantities at different periods, joined in a quotient — precisely the cross-period composition the corollary addresses.

The stronger version of the rival's objection — that the numerator is not "integrated over a reader's lifetime" but a cross-sectional spread — does not undermine the temporal-grain claim: the baseline is *fitted* over the reader's multi-night trajectory, so its spread reflects lifetime-scale variation, while the denominator reflects within-night variation. The temporal asymmetry is real.

---

## Objection 7 — The "phase-structured trajectory" is supported by a VOID estimator and selected legs; it is just-so.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: the band-movers run (2026-08-21) is VOID by the ≥20-event rule (17 counted down-crossings), and the draft's §2.2 uses its legs as a "fingerprint" despite this. The p-values for A are not corrected for multiple legs inspected. D fails the stated bar. S is "knife-edge, disclosed unread." The "P holds saturated 0.994" is undefined as evidence.

The honest rewrite: "**Phase-structured trajectory — conjecture with suggestive but VOID evidence.** The band-movers run (2026-08-21) is VOID by the ≥20-event rule (17 counted down-crossings). Its legs are suggestive but not confirmatory: A's shift-null p-values (0.0013/0.0001) are uncorrected for multiple comparisons; D fails the ≤50% bar (though D − D_null > 0 in both waves); P's 0.994 is undefined as a test statistic. **This is a conjecture (ZC-C1's phase-structure component), not a finding.** The decisive test is XP-2a's cadence sweep at ≥20 events."

---

## Objection 8 — The ρF floor conclusion rests on a flagged, unregistered conversion and an apparent unit mismatch.

**CONCEDE — with the honest weaker rewrite.**

The rival is right on both counts: (a) the conversion from within-night dispersion to per-night rate is unregistered (flagged in both draft and morning doc), and (b) the comparison of ρF ≈ 0.748 (corpus-sd) to ε₀ = 0.6 (dimensionless) is unit-incoherent unless ε₀ has been redefined.

The honest rewrite: "**Conditional on the flagged per-night conversion** (which is unregistered and may be unit-incoherent as currently stated), ρF ≈ 0.748 ≥ ε₀ = 0.6 would imply nightly band adjudication is infeasible (RF-C2). **This is a conditional, flagged result, not a derived one.** The conversion must be registered and ε₀ redefined in matching units before §2.3–2.4 can be marked 'derived.' Until then, the floor conclusion is a *conjecture* (ZC-C1's floor component), not a theorem-application."

---

## Objection 9 — "The power analysis was the floor talking" conflates bias with statistical precision.

**REBUT — with a partial concession.**

The rival is correct that RF-T3(i) says aggregate cadence cost is independent of committee size, not that the standard error of a ratio estimate is independent of N. More readers do shrink CIs. The draft's §2.3 claim "no amount of reader recruitment fixes it, because the floor is size-independent" conflates the floor's size-independence (RF-T3(i)) with the precision of an estimate.

But the draft's broader point survives: E2's power analysis computed n ≈ 14,533 to resolve a boundary-hugging truth (0.6088 vs 0.6). If the *quantity being estimated* is cadence-dominated (the floor's claim), then adding readers shrinks the CI around a quantity whose *bias* (the floor's contribution) is not reduced by N. The power analysis's brutality reflects the difficulty of resolving a boundary-hugging *biased* quantity, not merely a noisy one. The draft's "the 14,533 was the floor talking" is rhetorically strong but should be: "E2's power analysis's brutality is consistent with the floor's prediction that the quantity being estimated is cadence-dominated; the size-independence of the floor (RF-T3(i)) means more readers cannot move the bias, only the precision."

**Concede the overstatement:** the draft's "no amount of reader recruitment fixes it" should be "no amount of reader recruitment fixes the *bias*; it only improves precision around a biased quantity."

---

## Objection 10 — Policy collapse is not transferable to the Switch Test's stochastic sub-floor regime.

**REBUT.**

The rival claims M1 is about an adversary's worst world and the Switch Test is a stochastic world with unspecified sub-floor levels. But the draft's §1.3 does not claim M1 *applies* to the Switch Test; it claims the sub-floor regime is a *policy-collapse regime* in the sense that "re-anchoring cleverness is equivalent to doing nothing" — because the channel is undetectable. The draft's claim is: if the drift channel is sub-floor at every legal quote, then the re-anchoring machinery cannot extract information from that channel, so its only possible contribution is variance on the first-order step. This is an *estimator property* claim (the draft's §4.1 concedes: "the only live empirical residue is the variance finding — an estimator property, not a second-order property"), not a policy-collapse theorem application. The M1 reference is motivational: it shows that in the worst case, re-anchoring buys nothing; the Switch Test's sub-floor regime is a stochastic instance where the same conclusion holds by a different route (the channel is undetectable, so re-anchoring on it is noise-fitting, not signal-extraction).

The rival's objection that "the re-anchoring estimator's variance on the first-order step is an estimator property, not a policy-collapse property" actually *supports* the draft's §4.1 concession. The draft does not claim M1 derives the Switch Test's variance; it claims the sub-floor regime makes re-anchoring on the drift channel pointless, leaving only the first-order step as live signal.

---

## Objection 11 — "Dead either way" for the band test is circular because the corollary's quotient case is the contested point.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: the "either way" claim in §2.4 depends on the premise ratio being a forbidden heterogeneous-tick quotient (Objection 6's contested claim). If that objection fails, the static test may be sample-limited rather than dead.

The honest rewrite: "**Conditional on the corollary's application to the premise ratio** (which is contested, see Objection 6), the band as a static test at fixed nightly cadence is dead either way — the corollary's case against the quotient does not depend on the conversion. **If the quotient objection fails, the static test may be sample-limited rather than dead.** The cadence sweep (XP-2a) adjudicates."

---

## Objection 12 — "Under no legal quote" is an unproven exhaustive claim.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: the draft's §2.2 claims "Under no legal quote does the premise want to be a static in-band number" without defining the legal-quote set or proving the inspected grains cover it.

The honest rewrite: "**For the two constructions examined** (both quantities at window grain; both quantities at corpus grain), the static in-band number does not survive. **The complement is not shown empty.** Other common-grain constructions (per-night, per-event, per-segment, per-reader) are unexplored. The universal claim is an overstatement; replace with 'for the two constructions examined.'"

---

## Objection 13 — Sub-floor and floor-bound comparisons use point estimates as if they were parameters.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: αᵢ and ρ are estimated from finite samples, and no uncertainty is propagated through αᵢ/√7 or ρF. The draft's categorical claims ("sub-floor," "cannot purchase," "floor talking") inherit missing uncertainty.

The honest rewrite: "**Point-estimate comparisons with unquantified uncertainty.** The sub-floor claim (0.0076 vs 0.010) and the floor-bound claim (ρF ≈ 0.748 vs ε₀ = 0.6) are based on point estimates with no reported uncertainty. The exceedance probability — that the true drift exceeds the noise floor, or that true ρF < 0.6 — is not quantified. **These are provisional inequalities pending uncertainty propagation.**"

---

## Objection 14 — "Parity" is not defined as a statistic, so the confirmatory observations are not checkable.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: "parity" is used throughout without an algebraic definition, null distribution, or tolerance. "0.538 vs 0.923" is a difference of rates, not a parity statistic. "A fires" and "P holds saturated" are binary without thresholds.

The honest rewrite: "**'Parity' is used informally.** The draft's confirmatory observations (r = 0.7873 vs 0.7790; detection 0.538 vs 0.923) are reported as descriptive statistics, not as test outputs with defined parity criteria. The permutation floor (0.19–0.20) provides a reference for r, but 'parity' is not formally defined as 'difference within floor width' or any other statistic. **These are descriptive consistencies, not formal confirmations.** A formal parity statistic with null distribution and acceptance region is required before these are confirmatory evidence."

---

## Objection 15 — The machine-checked proof and supporting data are not produced; the audit trail stops where the argument starts.

**CONCEDE — with the honest weaker rewrite.**

The rival is right: no proof artifact, hash, repository, or appendix is cited for the theorem infrastructure, and no data release accompanies the empirical tables. The "machine-checked" claims are, from the committee's standpoint, reports.

The honest rewrite: "**Audit trail pending.** The machine-checked results (GC-T9 corollary, RF-T3(i), RF-C2, M1, M2) are consumed as external artifacts with no repository, hash, or proof script cited. The bench-falsified configurations are not supplied as raw data. The per-night conversion is flagged as unregistered. **These are reports, not auditable results, until the artifacts are deposited.** The thesis's force should be read as conditional on the artifacts' availability."

---

## The three objections I fear most (weakest rebuttals):

1. **Objection 8 (unit mismatch in ρF vs ε₀).** The draft's floor conclusion is load-bearing for the entire premise re-derivation (§2.3–2.4), and the rival is right that comparing corpus-sd to a dimensionless threshold is incoherent as stated. My rebuttal concedes and rewrites as "conditional, flagged conjecture" — but this guts the "floor talking" claim that anchors the thesis's main contribution. The conversion must be registered for the thesis to stand.

2. **Objection 3 (αᵢ/√7 is not a per-dimension bound).** The sub-floor claim — the Switch Test's central arithmetic — fails in the worst case over directions. My rebuttal concedes the arithmetic error and rewrites the claim as open. This is fatal to §1.2's "quote book closed" if the direction distribution is not bounded.

3. **Objection 2 (cross-period comparison of drift and noise).** The sub-floor claim compares whole-trajectory drift to per-window noise, which is the very cross-period sin the corollary denounces. My rebuttal concedes and rewrites as "pending the judge's actual statistic." This undermines the Switch Test's central claim — that the channel is sub-floor at every legal quote — unless the judge's noise aggregation at segment grain is established.

These three objections, if they survive, collectively dismantle the Switch Test's arithmetic (§1.2), the premise's floor argument (§2.3), and the "0.467 predicted-in-shape" upgrade (§1.3). The thesis would survive only as a conjecture-registering document, not a derived one.