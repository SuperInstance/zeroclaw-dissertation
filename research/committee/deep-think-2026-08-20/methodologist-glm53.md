# Position Note — Methodologist (GLM-5.3) — 2026-08-20

**Subject: E4 "Clock-Split" — the registration that resolves the L1 length-confound once and for all.**
**Position in one line:** the silence test's own recommendation (length-matched conditions in E3) is a quarantine, not a measurement; the dissertation needs the *decomposed* fine edge — the length-orthogonal component of the 1.229 — as a registered number, with matched generation as the confirmatory half.

## 1. Why length-matching alone is insufficient

Three failure modes, each disqualifying on its own:

1. **Marginal matching ≠ structural matching.** The silence arm classified from window statistics [mean, sd, min, max] of τ — local length *dynamics*, not just the mean. Matching SEG1/SEG2 length distributions kills the primary fuel (mean gap, Welch d=0.98) but leaves window-scale structure free to discriminate unless explicitly matched too.
2. **Length is a mediator, not a confounder — and matching on a mediator distorts the construct.** The causal structure is condition → length → dial *plus* condition → dial directly; there is no backdoor (condition is assigned by construction). Forcing cynical banter to be long changes what "cynical-banter" is (the silence test's own mechanism finding: banter *is* shorter messages), inviting collider-flavored artifacts and a dial-side attenuation that could masquerade as "the clock did it."
3. **Matching silences the alternative without measuring its share.** A matched corpus produces a cleaner setting, not a number. The flagship 1.229 needs an annotation — "X% length-carried, Y% condition-specific" — and only analysis-level decomposition yields it.

Residualization alone is *equally* insufficient: it is model-dependent (an affine length→dial basis may miss nonlinearity, leaving length residue masquerading as object). Hence two stages, one inference spine.

## 2. E4 registration

**H1:** the SEG1→SEG2 dial-field separation carries condition information orthogonal to message length. **H0-clock:** all of it is length-carried (cynicism/volume read length, r = −0.298).

**Stage 1 — decomposition (PRIMARY; existing corpus, runs first, cheap):**
- **Estimand:** the *length-orthogonal fine edge* — vMF μ̂ chord distance between condition means of residualized dial vectors, in the same units as 1.229 (the ratio deconfounded/raw IS the decomposition). Per-dial residual = dial − E[dial | length features]; length model = monotone spline, df=4, registered; fit **cross-fitted within LONO folds** (no leakage); evaluated on the **common-support set** (windows inside the length-distribution overlap; coverage reported).
- **Inference:** length-stratified permutation of condition labels *within* strata — assumption-light, preserves the length–dial coupling while destroying the condition link; cluster-aware by night. No parametric residual claim, no reliance on the spline being right.
- **Manipulation check:** silence-only classification on the common-support set must fall to chance; if it does not, the trimming failed — INDETERMINATE, not a pass.
- **Triad re-run:** residualized-content vs silence vs both, under the pinned LONO protocol, W=4 with W=8 sensitivity.

**Stage 2 — length-matched generation (CONFIRMATORY; closes the generative question):** ≥6 independent condition nights (3/3; independent seeds AND independent length draws), SEG1/SEG2 matched on length marginals *and* window-scale length statistics (mean+sd of τ per window). A registered content-validity check (frozen judge certifies matched SEG2 still reads as cynical-banter) guards against construct distortion; then recompute the raw fine gap — the clock arm has no fuel by construction.

**Decision rule (every branch pre-stated — the third-shape lesson of the silence test, applied):**
- **PASS:** deconfounded gap ≥ 0.37 (30% of 1.229) with stratified-null p < 0.05, AND residualized-content > silence-only under the pinned protocol → the fine edge is registered with its decomposition.
- **KILL:** deconfounded-gap CI entirely below 0.37, OR silence-only ≥ residualized-content − 0.10 (mirroring the original CLOCK tolerance) → 1.229 is re-registered as length-carried and henceforth reported only with its decomposition.
- **INDETERMINATE:** anything else — including common-support coverage < 70% or any gate shape the branches did not anticipate (declared honesty clause: reported, not absorbed).

**Power note (house style: brutal):** the existing corpus holds 2 independent nights (A=B=C identical); Stage 1 is powered for the *decision*, not the point estimate — the kill band is deliberately wide (0.37) because the competing effects are ~1.2 chord units apart, and overlapping stride-1 windows are why permutation is clustered by night. Stage 2's n=6 gives night-cluster LONO its minimum viable folds. No feasible N rescues a small deconfounded edge; none is promised.

## 3. Standing with L2

Identity grain already passed the clock test (content 0.893 vs silence 0.36) — E4 adjudicates the condition grain only. Either verdict, the dissertation keeps registered sentences, not launderings: the 1.229 is never deleted, it is **annotated with its decomposition**. Secondary windfall: if the deconfounded dials are rerun through the eigenbasis test, "reliable subspace" acquires a length-orthogonal reading — mood/volume/earnestness/presence minus the length component — closing the loop the ICC opened.

**The one-sentence registered claim:** *The SEG1→SEG2 fine edge (1.229) is decomposed by cross-fitted length-residualization with a length-stratified permutation null on common support, confirmed by length-and-structure-matched independent nights with a content-validity gate; it survives as a thermometer claim only if the length-orthogonal component is ≥ 0.37 and residualized-content beats silence-only under the pinned protocol, and is otherwise re-registered as length-carried.*

*(No git operations performed, per instruction.)*
