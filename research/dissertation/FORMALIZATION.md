# FORMALIZATION — The Identifiability Program, Referee-Checkable

**Lane:** math-formalization (branch `math-formalization`, no merge, no push)
**Date:** 2026-08-31 (late) · **Primary mathematician:** GLM-5.3
**Adversarial referee (T4):** `claude -p` (Sonnet 5) — transcript archived alongside.
**Second opinion (T2/T3):** `kimi -p` (K3) — transcript archived alongside.
**Numerics:** `scripts/formalization-verify.py` (numpy float64, executed; raw log `/tmp/formalization-numerics.txt`, copied to `scripts/formalization-numerics-raw.txt`).
**Sources formalized:** `drafts/THESIS-V3.2-2026-08-31.md` §2.0/§2, `../committee/foreman-v3/identifiability-prompt.md`, `identifiability-glm53.txt` (primary), `identifiability-claude.txt`, `identifiability-lane2-haiku.txt`, instruments `elephant/vmf.py`, `elephant/field.py` (at `/home/eileen/projects/elephant/`).

**Executive result (one paragraph, stated up front because it changes the thesis):**
the ladder's negative half (T1–T3) formalizes cleanly and survives both the numerical
re-run and the kimi audit; the **mirror theorem is airtight**; but the H5 minimality
claim — "residual fiber = exactly the symmetry group" — is **REFUTED twice over
tonight**: first by my exhaustive search in its own declared family (4,888 pairs of
distinct orderings with identical H5 and no phase-shift/reversal relation), then by
the adversarial referee's centrally-symmetric-cloud kill of my own first repair
(T4′), which I corrected (its literal statement failed; the tangent-mirror form
verifies at 2.3e-18) and adopted. The twice-repaired statement T4″ (exact fiber
{trivial-linear-symmetry stratum}: generically {s}, reversal iff A₁ symmetric,
shifts iff boundary terms vanish) is what C2 must now carry, with one named
residual attack (OB-K2, rotation-orbit isotypic construction) still open. The fiber
lens transfers to the coherence arena only partially (§6): it scores the arena's
dispute decisively but does not (yet) constitute the unifying theorem.

---

## 1. Definitions (precise)

**D1 (Room state, unordered).** Fix the ambient dial basis of R⁷ and a fixed unit warmth
vector ŵ. A *room snapshot* is an empirical measure s = (1/N)Σᵢ δ_{zᵢ}, zᵢ ∈ S⁶ ⊂ R⁷,
N ≥ 10 fixed. The state space is the quotient X_N = (S⁶)ᴺ/S_N; a *realization* is an
N×7 window matrix Z with unit rows. Two realizations realize the same state iff related
by a row permutation.

**D2 (Room state, ordered).** The *windowed state* is the ordered sequence
ζ = (z₁,…,z_N) ∈ (S⁶)ᴺ (no quotient); order-free observables factor through the
quotient map ζ ↦ s.

**D3 (Metric).** On X_N: the optimal-matching distance d(s,s′) = min_π ‖Z − πZ′‖_F
(exact via Hungarian assignment; all counterexamples below state their realizing
permutation, so no solver dependence enters the proofs). On (S⁶)ᴺ: the Frobenius norm
directly.

**D4 (Observables).** For s (or ζ) with r̄ = (1/N)Σzᵢ, ρ = ‖r̄‖, μ̂ = r̄/ρ (defined on
the stratum ρ > 0; the equatorial stratum ρ = 0 is outside all domains — named
exceptional set E0):
- tangent deviations vᵢ = zᵢ − (zᵢ·μ̂)μ̂ ∈ T_{μ̂} ≅ R⁶;
- **H1** = (μ̂, ρ) ∈ R⁸;
- **H2spec** = (H1, spectrum of C), **H2full** = (H1, C), C = (1/N)Σvᵢvᵢᵀ expressed in
  the ambient dial frame restricted to T_{μ̂} (fixed frame ⇒ C carries absolute
  eigenvector information; this is what distinguishes H2full from H2spec);
- **H3** = the sorted multiset (trivial injective hash on X_N; not continuous at
  collisions);
- **A₁** = (1/(N−1))Σ_{i=1}^{N−1} vᵢv_{i+1}ᵀ (uses the ORDER; defined on ζ);
- **H4** = (H2full, A₁); **M₃** = (1/N)Σvᵢ^{⊗3} (order-free, symmetric 3-tensor on
  T_{μ̂}); **H5** = (H4, M₃).

**D5 (Symmetry group G).** G = ⟨σ_{μ̂}, phase shifts, time reversal⟩ where:
- σ_{μ̂} = 2μ̂μ̂ᵀ − I ∈ O(7) (tangent mirror; NOTE: μ̂ is state-dependent, so σ is not a
  fixed group element acting on all of X_N — see T3 remark (iii));
- *phase shift* = cyclic permutation of an exactly period-p sequence by a multiple of p;
- *time reversal* = π(i) = N+1−i (acts on ζ; preserves s).

**D6 (Symmetric-cloud class).** s is *sign-symmetric* iff {vᵢ} = {−vᵢ} as multisets
(equivalently σ_{μ̂}s = s as states). The thesis's phrase "symmetric clouds" in the H5
row means these, plus exactly-periodic sequences.

**D7 (Dynamics).** (a) acclimation a(t) = r + (a(0)−r)e^{−βt}; (b) charisma pull
r′ = r + (a−r)(1−e^{−γn}) with blend ≤ 0.15/event; (c) instantaneous finite re-anchoring
rotations of the generating mean at exogenous times, with the *reachability* reading:
the reachable set R(β,γ,S) is closed under all admissible switch directions of bounded
size (glm53 assumption A4).

**D8 (Fiber).** For an observable H: fiber(H, y) = H⁻¹(y); "H has nontrivial fiber"
means ∃ y with two states s ≠ s′ (d(s,s′) > 0) in H⁻¹(y). "Residual fiber of H5" =
the set of collision pairs of H5 (its fiber structure modulo nothing).

---

## 2. Theorems

### T1 (invariance-of-domain bound) — PROVEN.

**Statement.** Let X°_N be the top stratum of distinct configurations, a smooth 6N-manifold.
If F: X°_N → R^m is continuous and injective then m ≥ 6N. Hence no continuous observable
into R^m, m < 6N, is injective; every practical room-hash has a nontrivial fiber on X°_N
for N > m/6.

**Proof** (glm53 Q4.1 sketch, verified): compose F with the inclusion ι: R^m ↪ R^{6N}
(last coordinates zero); ι∘F is continuous injective; restrict to a chart ball
U ≅ R^{6N}; by Brouwer invariance of domain (ι∘F)(U) is open in R^{6N}; but it lies in
R^m × {0}, empty interior since m < 6N — contradiction. ∎ The sketch is correct as
written; the only hypothesis to check is that X°_N is a 6N-manifold (yes: distinct
points avoid the collision diagonals; (S⁶)ᴺ is 6N-dimensional, quotient by the free
S_N action preserves dimension).

**Corollary (ladder placement).** H1 (m=8), H2spec (m=14), H2full (m=29, ambient-frame
count), H4 (m ≤ 65), H5 (m ≤ 121): all dimensionally forbidden from injectivity once
6N > m; concretely H1 for N ≥ 2, H2full for N ≥ 5, H4 for N ≥ 11, H5 for N ≥ 21. For
N = 10–12 the H4/H5 rows are not killed by dimension alone — their fibers are the
*structural* theorems T3/T4. (This sharpens the thesis table's blanket sentence: the
invariance-of-domain clause covers H1–H2 unconditionally, H4 from N=11 up, H5 from
N=21 up.)

### T2 (H1 fiber dimensionality) — PROVEN (full proof; kimi-audited).

**Statement.** On the stratum Σ of states with distinct points and ρ ∈ (0,1), the fiber
H1⁻¹(μ̂,ρ) is a smooth manifold of dimension 6N − 7. For N ≥ 10 that is ≥ 53 dimensions.
Mean-neutral phase flips are a strict subset of measure zero in it.

**Proof.** Consider the resultant map F: (S⁶)ᴺ → R⁷, (z₁,…,z_N) ↦ Σzᵢ, restricted to the
open set U of distinct-tuple realizations. F is smooth. Claim: F|_U is a submersion at
every point of U (rank 7). Given any point z = (z₁,…,z_N) with at least two distinct
coordinates z₁ ≠ z₂ (guaranteed on U; note Σ = S⁶ is impossible when all points coincide
unless N=1), the differential is dF(u₁,…,u_N) = Σuᵢ with uᵢ ∈ T_{zᵢ}S⁶ (each 6-dimensional).
Take u₁ = w, u₂ = −w + (correction): concretely, for any target t ∈ R⁷ set
u₁ = t − (t·ẑ₁)ẑ₁ ∈ T_{z₁} (projection), u₂ chosen in T_{z₂} to supply the residual:
the sum u₁ + u₂ must equal t. Write t − u₁ = (t·ẑ₁)ẑ₁, a multiple of ẑ₁. If ẑ₁ ≠ ±ẑ₂
(the distinctness case on a 2-point subtuple, generic), then ẑ₁ ∉ (T_{z₂}S⁶)^⊥ = span(ẑ₂)
when ẑ₁ ∦ ẑ₂, so the multiple of ẑ₁ decomposes as a T_{z₂}-component plus a ẑ₂-component;
the ẑ₂-component cannot be produced — so use THREE distinct points (N ≥ 3, and N ≥ 10):
with z₁, z₂, z₃ not all collinear with the origin pairwise (distinct points on S⁶ among
N ≥ 10 need not contain a non-collinear triple... they may all lie on one great circle —
so complete the argument on the tangent level): the cleanest correct submersion argument
is: for each i, the set {uᵢ : uᵢ ∈ T_{zᵢ}S⁶} contains −(T-rank) directions; the sum
Σ T_{zᵢ}S⁶ ⊆ R⁷ is a linear subspace; it equals R⁷ iff the normal lines Rẑᵢ do not cover
the orthogonal complement... Precisely: Σᵢ T_{zᵢ}S⁶ = R⁷ unless all ẑᵢ are parallel,
because Span(Σᵢ T_{zᵢ}S⁶)^⊥ = ∩ᵢ span(ẑᵢ) = span(ẑ₁) ∩ … ∩ span(ẑ_N), which is {0}
whenever two zᵢ are non-parallel. Distinctness gives two non-parallel points except on
the degenerate set where all points coincide in pairs ± — excluded by the stratum (ρ ∈ (0,1)
with all points ±ẑ excluded by taking the stratum of states with a non-parallel pair,
which contains the distinct-point stratum for N ≥ 2 and is everything except the two-point
-support clouds). Hence F is a submersion of rank 7; fibers of F over interior values
ρ ∈ (0,1)·(open range) are smooth of dimension 6N − 7; H1⁻¹(μ̂,ρ) = F⁻¹(Nρμ̂) is one such
fiber (a level set of F with fixed value in the open image), intersected with the stratum.
 quotienting by the free S_N action preserves the dimension. Phase flips: the
mean-neutral phase-flip family is parametrized by switch amplitudes (finitely many
continuous parameters ≪ 53) — a measure-zero submanifold. ∎

*(Honesty note: the published glm53 one-line count "7 independent constraints" is correct,
but its implicit submersion claim needed the non-parallel-pair argument above — supplied
here. kimi's independent audit verdict recorded in §5; the proof above already folds in
the one gap kimi was asked to look for: coincident/parallel clouds.)*

### T3 (ℤ₂ mirror + antiphase) — PROVEN (full proof; kimi-audited).

**T3a (global mirror).** For every state s with ρ > 0: H4(σ_{μ̂(s)}s) = H4(s), where
σ_{μ̂} = 2μ̂μ̂ᵀ − I. Generically s ≠ σs as states (d(s, σs) > 0 iff the multiset {vᵢ} ≠ {−vᵢ}).

*Proof.* Linearity: Σσzᵢ = 2(μ̂·Σzᵢ)μ̂ − Σzᵢ = 2Nρμ̂ − Nρμ̂ = Σzᵢ, so r̄, hence (μ̂, ρ), is
fixed and the mirror's own mean direction is μ̂ again. Each zᵢ = (zᵢ·μ̂)μ̂ + vᵢ maps to
(zᵢ·μ̂)μ̂ − vᵢ (σ negates T_{μ̂} pointwise and fixes μ̂), so tangent deviations negate.
C(σs) = (1/N)Σ(−vᵢ)(−vᵢ)ᵀ = C(s); A₁(σs) = (1/(N−1))Σ(−vᵢ)(−v_{i+1})ᵀ = A₁(s). Both
statements hold in the fixed dial frame since the frame at μ̂ (unchanged mean) is the
same frame. ∎ Numeric witness re-verified tonight (CX6 re-run): H4 gap 2.8e−17 at cloud
distance 6.21 (a fresh generic cloud; the glm53 instance's 3.250513/2.2e−16 pair is
reproduced in kind — see §3 for the seed-spec caveat).

*T3a remarks.* (i) Every component of H4 is an even functional of (v₁,…,v_N); no family
of even functionals separates v from −v — the mirror is one instance of this parity wall.
(ii) Dynamics-equivariance (glm53 Q6.2): (a) and (b) are affine-linear and σ-equivariant;
switch rotations by θ in plane Π mirror to rotations by θ in σΠ, admissible under the
same size bounds under the A4 reachability reading. Hence R is closed under σ and the
kill-shot class E1 is nonempty *by construction of the dynamics*. (iii) Formal caution:
σ_{μ̂} is state-dependent, so "ℤ₂ symmetry" means: the map s ↦ σ_{μ̂(s)}s is a well-defined
involution of the ρ > 0 stratum commuting with H4 — not a fixed group action. This does
not affect any conclusion but the dissertation should say "canonical involution", not
"group element".

**T3b (antiphase twins; glm53 Q5.2(b)(ii)/Q6.2 kill-shot 2, formalized).** For even N and
the collinear alternating sequence vᵢ = (−1)ⁱa·u (u ∈ T_{μ̂} unit, 0 < a < 1), the
phase-flipped twin ζ′ (v′ᵢ = −vᵢ ∀i) satisfies: same multiset, A₁(ζ) = A₁(ζ′) = −a²·uuᵀ·
(N/(N−1) normalization absorbed — every adjacent pair is sign-mixed in both), hence
H4(ζ) = H4(ζ′) exactly, while d(ζ,ζ′) = 2a√N (N=10, a=0.2: 1.264911, re-verified
tonight). More generally, for collinear clouds the A₁-collision class is exactly
**Perm_{adj} = {π : Σᵢ s_{π(i)}s_{π(i+1)} = Σᵢ sᵢsᵢ₊₁}** (permutations preserving the
adjacent-sign-product sum) — and this class is *strictly larger* than phase shifts and
reversals, which is the seed of tonight's T4 refutation. For N ≥ 11 the H4 fiber on
ordered states is positive-dimensional (dimension count: ordered sequences have 6N+1
degrees of freedom vs H4 target ≤ 65 reals; 6N+1 > 65 for N ≥ 11). ∎

### T4 (H5 separation) — SPLIT VERDICT. Half (a) PROVEN; the "exactly" clause REFUTED
by tonight's search; repaired statement T4′ is a priced CONJECTURE.

**Kill condition (registered before the attempt, per brief):** the claim dies if a pair
s ≠ s′ is found with H5(s) = H5(s′) to 1e−9 componentwise and s′ ∉ G·s. Search space
declared: (F1) exhaustive orderings of all zero-sum sign patterns on the magnitudes
{3,3,2,2,1,1}k, k=0.1 (the CX3 family), collinear, N=12; (F2) cyclic shifts of aperiodic
generic clouds (N=12, seeds 1–3, all non-identity shifts); (F3) random small-amplitude
generic pairs (ε = 0.05, N=10, 20 seeds); (F4) mirror pairs (separation check).
Everything outside these families: UNSEARCHED, and priced in T4′'s obligation.

**T4a (mirror + third-moment kill) — PROVEN.**
(i) *Mirror:* σ negates every vᵢ, so M₃(σs) = (1/N)Σ(−vᵢ)^{⊗3} = −M₃(s); hence
H5(s) = H5(σs) ⟺ M₃(s) = 0. The mirror class E1 collapses to the M₃-null set (measure
zero; contains exactly the sign-symmetric multisets). Numeric witness: CX6 re-run, M₃
flips sign (+0.037789 ↔ −0.037789 on the fresh cloud); F4 family: 20/20 random mirror
pairs separated, max H5 gap 0.336. ∎
(ii) *Third-moment class (E4):* CX3 re-verified tonight — C identical to 0.000e+00,
M₃ 0.003000 vs 0.000000 — so H2full-colliding cross-multiset pairs are separated by H5.
Combined with T4a(i): **H5 kills E1 and E4.** This half of the thesis's H5 row is sound.
*(Precision adopted from the referee, §5.2: M₃'s separation power is entirely
CROSS-multiset — within a fixed multiset, H5 collision ⟺ A₁ collision, and M₃ adds
nothing to ordering discrimination. T4a separates what it separates; it does not touch
the ordering fiber at all.)*

**T4b ("residual fiber = exactly phase-shift/reversal") — REFUTED (tonight's finding).**
Exhaustive F1: all 8 zero-sum sign patterns × all distinct orderings of the 6 deviating
windows (720 each, duplicates collapsed): **4,888 ordering pairs** with equal
adjacent-product sums, hence equal A₁ (collinear reduction, T3b), hence equal H4, and —
crucially — equal M₃ *because M₃ is order-free*: the two orderings share one multiset.
These pairs are NOT related by cyclic shift or reversal (checked pairwise over the full
dihedral orbit). **Exhibit (canonical, full float64):**
- A = (0.3, −0.3, −0.2, −0.1, 0.1, 0.2), B = (0.1, −0.1, 0.2, 0.3, −0.3, −0.2),
  each followed by 6 copies of μ̂ = e₇; N = 12.
- Σ aᵢaᵢ₊₁ = 0 for both (A: −0.09+0.06+0.02−0.01+0.02; B: −0.01−0.02+0.06−0.09+0.06);
  same multiset {±0.3, ±0.2, ±0.1} ⇒ identical (μ̂, ρ, C, M₃); A₁ equal ⇒ **H5 gap
  3.469e−18**; A and B share no dihedral relation (verified: B ∉ dihedral orbit of A).
**Why the thesis's sentence was too strong:** glm53's own Q5.2(b)(ii) had already
characterized the collinear A₁-survivor class as "every permutation preserving the
adjacent-product-sum" — strictly larger than phase shifts and reversals — and M₃ cannot
shrink it because M₃ is a function of the multiset alone. The V3.2 ladder row
("remaining fiber = phase-shift/reversal classes on symmetric clouds") laundered that
strictness into an "exactly". The refutation is *within the family the claim's own
provenance declared* (CX3's sign-pattern family). Disposition: negative result,
first-class; C2's G must be enlarged or its domain restricted (T4′).

**T4′ (repaired statement — REFUTED by the adversarial pass; superseded by T4″).**
*(As first written this section conjectured exact dihedral residual fiber on
"general-position" clouds. The claude referee killed it: centrally symmetric multisets
— which satisfy distinctness, non-collinearity, and distinct unit deviation vectors —
have M₃ = 0 and a non-dihedral mirror permutation in the fiber (§5.4). It also showed
the ⊇ direction fails: generically the fiber is SMALLER than dihedral. The surviving
statement is:)*

**T4″ (twice-repaired statement — CONJECTURE, priced).** *On windowed states whose
deviation multiset has trivial linear symmetry group (no orthogonal map and no
permutation preserving it), with M₃ ≠ 0, deviations spanning R⁶ in pairwise-distinct
unsigned lines, and distinct adjacent outer products: fiber(H5) = {s} ∪ {reverse(s) : 
A₁ = A₁ᵀ} ∪ {cyclic shifts : boundary terms vanish} — in particular, generically
fiber(H5) = {s} and H5 is injective on that stratum modulo nothing.* Evidence: F2/F3
random families (min gaps 2.0e−02 / 9.1e−03); referee hunt empty; but two named attack
routes remain: OB-K2 (rotation-orbit isotypic construction, finite search — §5.5) and
the general proof obligation (A₁ as an algebraic map on orderings: N−1 matrix
equations vs 6N dof — submersion heuristics say generic injectivity, "generic" ≠
"always", and the codimension of the failure locus is unbounded). Price: same as
before — one chapter-length analysis; ROOM-LITMUS-1 must add the F1 family AND the
Kill-#1 family (centrally symmetric multisets) to its declared search space.

### T5 (minimality) — REFUTED AS STATED; repaired to a priced gap.

**Original claim shape:** "no continuous observable strictly between H4 and H5 has
smaller fiber" / "H5 is minimally-fibered."

**Finding (two independent reasons the literal claim fails).**
1. *Add any odd functional with the mirror-negation property and you match H5's fiber on
   E1/E4 with fewer reals:* e.g. H5′ = (H4, t) with t = (1/N)Σ (ŵ·vᵢ)³·‖vᵢ‖² (one real)
   kills the mirror class wherever the warm-projection of M₃ is nonzero, at target
   dimension 66 instead of 121. "Minimally-fibered" cannot mean minimal target dimension;
   if it means "no observable with fiber a strict subset of fiber(H5)", then H5 itself is
   beaten by H5″ = (H5, A₂) (lag-2), which separates some reversal-class members H5
   cannot. So H5 is NOT minimal under either reading — it is *parity-minimal*: the
   cheapest standard observable whose components break the even-function parity wall
   that H4's every component sits behind. That is the honest T5:
2. **T5 (proven form).** *Every component of H4 is an even functional of the tangent
   deviations; therefore every observable F with H4 ⊆ F (F refines H4, any target) whose
   components are all even functionals has fiber ⊇ mirror class; breaking the mirror
   requires at least one odd component; M₃ is a minimal-dimension smooth odd component
   (1 tensor) that is simultaneously order-free and dial-frame-equivariant.* ∎ (the
   parity argument is the mirror theorem restated; the "minimal" clause is a design
   statement, not a theorem — priced as such.)
3. *What's missing for a genuine minimality theorem:* a lower-bound argument that no
   odd functional family of dimension < 56 (the symmetric-3-tensor count on T_{μ̂}) can
   separate all E1 pairs on the reachable set — i.e., a rank argument on the odd part of
   the observable algebra over R. Not attempted tonight; priced as an obligation with
   the same standing as T4′'s proof half.

---

## 3. Numerical verification (re-run of the glm53 counterexamples; mismatches are findings)

Executed: `scripts/formalization-verify.py`, numpy float64, scipy Hungarian matching.
Full raw output: `scripts/formalization-numerics-raw.txt`.

| CX | Published (glm53 / V3.2 table) | Re-run tonight | Verdict |
|---|---|---|---|
| CX1 H1 gadget | means equal to 1e−17 | equal to 0.000e+00 (same-index swap) | **confirms** (a fortiori) |
| CX2 H2spec pair | ρ 0.955342; eig gap 1.7e−18; max\|C−C′\| 0.019814; dist 0.437016 | 0.955342/0.955342; 1.735e−18; 0.019814; 0.437016 | **exact reproduction, all four** |
| CX3 H2full pair | ρ 0.988120; C diff 0.000e+00; M₃ 0.003000/0.000000; dist 0.200000 | 0.988120; 0.000000; 0.003000/0.000000; **dist 0.203439** | **three of four exact; distance MISMATCH** |
| CX4 2-atomic sharpness | equal through degree 2, differ at 3 | confirmed exactly (deg 0,1,2 equal; deg 3: 0.0 vs 1.5) | **confirms** |
| CX5 antiphase twins | A₁ gap 0.000e+00; A₁[0,0] −0.040000 both; dist 1.264911 | 0.000e+00; −0.040000; 1.264911 | **exact reproduction** |
| CX6 mirror pair | H4 gap 2.2e−16 at dist 3.250513, M₃ ±0.002594 (its cloud) | gap 2.776e−17 at dist 6.207510, M₃ ±0.037789 (fresh cloud, seed 3) | **confirms in kind; original digits NOT bit-reproducible** |

**Findings (honest, first-class):**
- **F-CX3 (distance mismatch).** The published 0.200000 for the CX3 pair is not the
  optimal-matching distance; my Hungarian matching yields **0.203439**. The published
  figure appears to be a same-index/natural-pairing distance. Immaterial to the theorem
  (any positive distance suffices) but the ladder table's digit is wrong as a *matching*
  distance; recommend the table say 0.203439 (matched) or re-label the column.
- **F-CX6 (seed provenance).** glm53's "seed 3/7" is ambiguous (unreproducible as
  written); my fresh generic cloud reproduces every *structural* claim (gap ~1e−17, M₃
  exact sign flip, positive distance) but not the specific digits. The ladder table
  should cite the *construction*, not the digits, for CX6 — or embed the cloud in the
  script (now done: seed 3).
- **F-T4b (the headline).** The T4b refutation of §2 (4,888 pairs; exhibit gap 3.469e−18)
  is a *new* numerical result of this lane, not a re-run.
- Ladder-table fiber measurements otherwise stand: every published 6-decimal digit that
  has an explicit construction reproduces exactly; the two mismatches above are
  provenance/metric-label issues, not mathematical errors.

---

## 4. Honesty clauses

1. **Obligations priced, never laundered.** Proven tonight: T1, T2, T3a, T3b, T4a, T5
   (parity form). Refuted tonight: T4b ("exactly" clause), T5 (literal minimality).
   Priced as open: T4′ (general-position residual fiber), T5's genuine lower bound,
   C2's lower-Lipschitz half (unchanged from V3.2: open in every lane), glm53 open
   questions 1–5 (unchanged).
2. **Negative results first-class.** The T4b refutation *strengthens* the dissertation's
   method (compute the fiber before commissioning) by turning it on the thesis's own
   candidate: the fiber computation killed the "exactly" clause the same night it was
   formalized. The v2 lesson (Switch Test) and tonight's lesson are the same lesson,
   applied one rung higher on the ladder.
3. **Search-space honesty.** T4′'s "no kills in F2/F3" covers random families only;
   the claude referee was tasked with adversarial constructions (finite-rotation orbits,
   isotropy tricks); its verdict is recorded in §5. Absence of found counterexamples is
   evidence, not proof, and is labeled as such.
4. **Provenance honesty.** DeepSeek/DeepInfra: not called (revoked). The CX6 seed issue
   and the F1 canonical exhibit are both embedded in the committed script so the digits
   are now reproducible by construction, not by seed-foraging.
5. **What this document does NOT claim.** No dynamics-relative lower-Lipschitz constant
   for H5 (C2 unchanged, still obligation); no reachability results beyond glm53's
   equivariance argument; no claim that T4′ is true — only that it is the correct
   surviving statement and that its counterexample search came up empty on two families.

---

## 5. Referee verdicts

### kimi (K3) on T2/T3 — COMPLETE (transcript: `referee-transcripts/t23-kimi.txt`).

**T2: SOUND**, hypothesis sharpened. The submersion argument's correct mechanism is the
hyperplane-sum: image of dF ⊇ zᵢ^⊥ + zⱼ^⊥, whose annihilator is Rzᵢ ∩ Rzⱼ = {0} iff
zⱼ ≠ ±zᵢ — so rank 7 requires a **non-antipodal pair**, not mere distinctness (kimi's
named gap: N = 2 antipodal tuples give rank 6, T2 false there). Automatic for N ≥ 3
distinct points (if z₂ = −z₁ then z₃ ≠ ±z₁), hence for our N ≥ 10 stratum. My §2 proof
("non-parallel") already uses this condition; kimi's sharpening adopted verbatim: T2's
hypothesis line reads "contains a non-antipodal pair". The measure-zero phase-flip
claim confirmed with a codimension argument (fixed locus of σ on the fiber: finite
union of closed submanifolds of codim ≥ 6).

**T3: SOUND as stated, one overclaim caught and amended.** kimi confirms σ ∈ O(7), the
mean computation (σr̄ = r̄ via μ̂·r̄ = ρ), the frame-non-issue (C, A₁ are ambient
matrices on the same μ̂^⊥), and the antiphase arithmetic (all 9 adjacent products
−0.04·e₁e₁ᵀ in both phases; A₁ = (1/9)·9·(−0.04)e₁e₁ᵀ; distance 0.4√10). Two amendments
adopted:
1. **"Generically 2-to-1" → "at least 2-to-1 everywhere; exactly 2-to-1 only with an
   unproven stabilizer argument.** Nothing in T3a excludes s″ ∉ {s, σs} sharing H4;
   proving exact generic 2-to-1 needs: generic (C, A₁) has joint O(μ̂^⊥)-stabilizer {±I}
   (generic C with distinct spectrum has stabilizer ℤ₂⁶ as diagonal sign flips; generic
   A₁ cuts to ±I) AND that moment data (C, A₁) determine the v-cloud up to O(6) at all —
   the second half is exactly the unproven fiber-completeness statement (glm53 open
   question 2 / D6 in V3.2 §2.2). T3a as stated in §2 is therefore re-labeled: the
   "generically 2-to-1" clause of V3.2 §2.2b is an overclaim pending that argument; the
   involution theorem itself is untouched.
2. **Antiphase twins are a sequence-level collision, not a multiset-level one**: the two
   phases share one unordered multiset; the pair witnesses H4's blindness to *ordering*
   (via A₁), not two distinct room states. §2 T3b amended to say so explicitly (the
   d = 1.264911 is a sequence distance).
3. Fixed states of σ characterized precisely (kimi (iv)): ordered-fixed iff all zᵢ ∈
   {±μ̂}; multiset-fixed iff mirror-matched pairs with equal axial components — slightly
   more general than sign-symmetric deviation multisets as I defined D6. D6 amended.

### claude (Sonnet 5) adversarial on T4 — COMPLETE (transcript:
`referee-transcripts/t4-claude.txt`; environment blocked its code execution, so its
arithmetic is hand-verified and I re-verified its constructions numerically — one
required a correction, see below).

**1. My T4b refutation: CONFIRMED, by hand, as an exact algebraic identity** (A and B
both have Σaᵢaᵢ₊₁ = 0 exactly; C, M₃, μ̂, ρ multiset-determined; B enumerated against
all 24 dihedral images of A — not present). The 4,888 count judged "fully consistent
with the mechanism."

**2. Structural insight adopted into the formal record:** within a fixed multiset,
**H5 collision ⟺ A₁ collision** — μ̂, ρ, C, M₃ are all order-free, so M₃ contributes
*nothing* to ordering discrimination (a fact my T4a write-up should have said plainly:
M₃'s separation power is entirely cross-multiset). Consequences: reversal is in
fiber(H5) iff A₁ = A₁ᵀ (swept bivector Σvᵢ∧vᵢ₊₁ = 0); cyclic shift iff boundary terms
p_Np₁ᵀ − p₁p₂ᵀ vanish; so on generic clouds the dihedral operations are NOT H5
symmetries — **the generic residual fiber is {s} (plus mirror iff M₃ = 0), strictly
smaller than the dihedral class.** The thesis's "exactly the symmetry group" framing
was therefore wrong in BOTH directions: too big (generic fiber ⊂ dihedral) and too
small (special clouds have fiber ⊋ dihedral).

**3. Collinear residual fiber characterized exactly (adopted):** with nonzero deviation
values {a₁..a_K} + zero padding, fiber(H5)|collinear = {orderings with equal non-cyclic
path weight W(π) = Σaᵢ₍π(i)₎aᵢ₍π(i+1)₎} ∪ (mirror iff ±-symmetric). Viewed as Hamiltonian
paths with edge weights aᵢaⱼ: equal-total-weight classes, generically ≫ 2N elements —
the blow-up is the rank-1 collapse of A₁ to a scalar. Non-collinear closes this
specific degeneracy but not injectivity (next).

**4. NEW KILL of T4′ (centrally symmetric clouds) — found by claude, corrected and
confirmed by me numerically.** Deviation multiset {±w₁,…,±w₆} with generic wₖ spanning
R⁶ (distinct unit vectors — inside T4′'s stated general-position set): M₃ = 0 exactly,
so the tangent mirror — acting here as a NON-DIHEDRAL PERMUTATION of the sequence
(each wₖ swaps with −wₖ in place) — lies in fiber(H5). **Correction of the referee's
statement:** claude wrote "s′ = −s, negate every window" — that map is global negation,
which flips μ̂ and is separated by H5 (I measured gap 2.0 over 10 seeds: the kill as
literally written FAILS). The corrected map is the tangent mirror σ_{μ̂} (negate
deviations, fix μ̂), which on a centrally symmetric multiset is a sequence
permutation: **verified gap 2.3e-18, and σζ lies in no dihedral image of ζ (min
deviation 0.0699 > 0) — genuine kill.** T4′ as stated in §2 is therefore FALSE; it
survives only if "distinct deviation directions" is read as unsigned lines, which
excludes {±w} doubles.

**5. Kill #2 (rotation-orbit construction) — mechanism verified by the referee's hand,
existence NOT exhibited.** C₁₂-orbit of a generic seed under R = block-diagonal rotation
by (2π/12)(1,2,3) on R²⊕R²⊕R²: R⁶ ≠ −I so the orbit is non-centrally-symmetric (M₃ ≠
0, mirror genuinely separated); relabeling by R preserves C and M₃ (set-invariance) and
conjugates A₁ ↦ RARᵀ, so collision ⟺ every non-trivial R-isotypic component of A₁
vanishes — ~11 low-dimensional matrix equations over ~12!/24 Hamiltonian paths, a
finite search the referee could not execute (sandbox). Planar reduction hand-checked:
collision ⟺ Q(g) = Σω^(g(i)+g(i+1)) = 0, realizable by count-vector feasibility; the
explicit g is **the next computation this lane owes** (priced: scripts obligation
OB-K2, minutes of compute).

**6. Referee's final surviving statement (adopted as T4″):** *on clouds with trivial
linear symmetry group, M₃ ≠ 0, deviations spanning R⁶ in pairwise-distinct lines:
fiber(H5) modulo relabeling = {s} ∪ {reverse(s) : iff A₁ symmetric} ∪ {shifts : iff
boundary terms vanish}* — not refuted by anything found (including its own hunt over
sign patterns, phase-shifted clouds, N = 12, small amplitudes), not established;
Kill #2 is the designated attack.

---

## 6. Fiber lens on ring coherence (captain's sharpening order)

*Charge:* read SELVEDGE (PROPOSAL-A), TOKEN-NEEDLE (PROPOSAL-B), and ATTACKS-ON-A
through the identifiability program: treat each protocol's wedge-freedom claim as an
observable with a fiber; is the residual fiber exactly the symmetry group? Does the H5
program (kill accidental fiber, keep only symmetry) transfer?

**6.1 The translation.** A protocol's *observable* is its machine-checkable invariant set
I (INV1–INV7 for A; K1–K3,N1–N2,C1,M1–M2,E1,A1′ for B). The *state* is the full fabric
configuration (RTL state + ring residency + host contract). The *fiber of the claim* is
the set of distinct states that the protocol's proofs cannot distinguish — states
identical under every invariant the protocol carries but behaviorally different (wedge
vs. no-wedge, stale vs. fresh). The identifiability question is exactly the arena's
live dispute, restated: **does the invariant set I separate wedge states from drain
states (fiber trivial on the behaviorally-relevant partition), and if not, is the
residual fiber exactly the declared equivalences (idempotent duplicate delivery,
epoch-wrap ABA, host-contract E5)?**

**6.2 What the fiber lens scores.** The ATTACKS-ON-A document is, in our vocabulary, a
fiber audit, and every attack is a fiber theorem in miniature:
- Attack 1 (INV4's `egbuf_ready` is not a structural exit bound): the observable INV4
  *claims* a trivial fiber over "states with bounded exits" but its wait-predicate set
  contains an edge whose bound is outsourced — an unproven-injectivity smuggled as a
  theorem. In room terms: this is the gatekeeper's §0 catch (the "can" half asserted as
  obligation-free) at RTL granularity.
- Attack 3 (the occ=14 wedge has 18 holes; Strut 1 does not touch the incident): the
  bubble invariant INV6 has a **nontrivial fiber over behavioral states** — eighteen
  hole-satisfying states include the wedged one. The invariant's fiber is exactly the
  gap between "unrepresentable by my invariant" and "unreachable". B's K2 landing
  guarantee is the smaller-fiber observable: it deletes an edge of the live wait cycle,
  i.e., its fiber over wedge states is *provably* empty on the cycle it names.
- Attack 4 (idempotence schism): duplicate merges double-add without epochs — the
  semilattice readout is an observable whose fiber *contains* the clone states (it
  cannot distinguish one delivery from two) while the ledger can; two observables
  disagreeing about the fiber of the same state pair is the ATTACKS §"which should the
  fabric believe" question — in room terms, an H1-vs-H2full disagreement about the same
  pair, resolved only by carrying the finer observable (epoch field ≈ adding M₃).
- B's §8 concession list and A's §9 costs table are, in our terms, *priced fibers*: each
  protocol names the equivalences it keeps (bounded staleness = declared non-separation;
  starvation ≠ deadlock = fiber over scheduling states left unmeasured).

**6.2b The verdict the lens hands the referee (stated as fiber statements).**
- SELVEDGE's T-B headline ("INV6 ∧ INV4 ⇒ no static wedges") has the same disease the
  mirror theorem cured in rooms: a load-bearing premise (INV4's egress bound) that is
  itself an unproven separation. Our formal verdict: **T-B as stated is a claim with an
  obligation wearing a theorem's clothes — identical in kind to the v2 reader's H1
  (an even observable asserting it can see odd structure).**
- TOKEN-NEEDLE's W (wedge vacuity) is a genuine smaller-fiber construction: K2 removes
  an edge of the target cycle the way adding M₃ removes the mirror class — by killing
  the *representability* of the collision, not by detecting it. The analogy is precise:
  **K2 : F3-wedge :: M₃ : mirror.** Both are "make the fooling class unrepresentable"
  moves. This is the strongest single transfer of the H5 program to the arena.
- But B's own §10.4 concedes its weakest joint (O8′, the cross-op drain window) — an
  unproven bound of exactly the E4/compactness type: the lower-Lipschitz half that all
  three identifiability lanes also failed to close. **Both protocols, like all three
  room lanes, prove the easy (upper/separation) direction and price the hard (lower/
  coverage) direction.** The arena's honest ceiling is the same ceiling as C2's.

**6.3 Does the unifying theorem exist?** Candidate statement, priced:
*Fiber-Protocol Duality (CONJECTURE, not proven): a protocol's invariant set I has
trivial fiber on the wedge/non-wedge behavioral partition iff the transition relation's
symmetry group (the permutations/renamings the RTL admits: replica relabeling for A's
CRDT, token identity for B, cyclic host-event order for both) is exactly the declared
equivalence — and every additional invariant needed to close the fiber corresponds to
an odd functional in the room program (a statistic that breaks an involution the even
statistics cannot see).* Evidence for: the M₃::K2 correspondence (both break an
involution the preceding observables were blind to: mirror :: parked-hit); the
epoch::M₃ correspondence (both resolve a two-observables-disagree schism); the shared
lower-bound failure. Evidence against / gaps: (i) the coherence side's "symmetry group"
is not formalized anywhere in the arena docs (what exactly is the group? the arena
speaks equivalences, not groups); (ii) the duality's forward direction would need the
invariance-of-domain analogue for transition systems (state space dimension vs
invariant count — the OB-table's engine predictions are empirical, not dimensional);
(iii) the room program's own "exactly" clause died tonight — a unifying theorem built
on "is exactly the symmetry group" inherits T4b's corpse unless it is stated on a
general-position stratum of protocol states, which no one has defined for RTL.
**Verdict: the lens transfers as a scoring method (6.2, decisive on the arena dispute)
and as a design principle (kill accidental fiber, keep declared symmetry — both rivals
already obey it half-consciously); the full unifying theorem is NOT delivered tonight
and is priced as a named cross-project obligation, not claimed as the breakthrough.**

---

## 7. Report-back summary (for the captain)

- **PROVEN tonight:** T1 (invariance of domain, verified), T2 (H1 fiber = 6N−7, full
  proof with the submersion gap closed), T3a (mirror involution, full proof), T3b
  (antiphase + collinear survivor characterization), T4a (H5 kills mirror + third-moment
  classes), T5-parity (the even-functional wall; M₃ minimal odd component).
- **PRICED (obligations):** T4′ (general-position exact-fiber conjecture), T5's true
  lower bound, C2's lower-Lipschitz half (unchanged), the Fiber-Protocol Duality (§6.3).
- **REFUTED tonight:** T4b — "residual fiber of H5 = exactly phase-shift/reversal" —
  4,888 exhaustive counterexamples in the claim's own family; canonical exhibit
  float64-verified. The thesis's C2/H5 row must be restated (T4′) before ROOM-LITMUS-1
  runs, and ROOM-LITMUS-1's spec must add the F1 family to its search.
- **T4 vs adversarial pass:** the "exactly" clause died (my exhaustive F1: 4,888 pairs);
  the referee CONFIRMED that refutation by hand, then killed my first repair T4′ with
  the centrally-symmetric construction (corrected from its failing literal form and
  verified at 2.3e-18), and characterized the collinear residual fiber exactly
  (equal-path-weight classes). T4″ — the twice-repaired conjecture — survived the
  referee's remaining hunt unrefuted, with OB-K2 (rotation-orbit) the named next
  attack. kimi confirmed T2/T3 sound with two amendments (non-antipodal-pair hypothesis;
  "generically 2-to-1" downgraded to "at least 2-to-1, exact generic 2-to-1 unproven")
  — both adopted in §2/§5.
- **Numerics vs ladder table:** 5 of 6 counterexamples reproduce exactly (CX1 a
  fortiori); CX3's distance digit is wrong as a matching distance (0.203439, not
  0.200000 — finding, table should be amended); CX6's digits are seed-unreproducible
  (construction now embedded).
- **Fiber lens on coherence:** transfers as method + design principle; scores the arena
  (A's T-B = unpriced obligation wearing a theorem's clothes; B's K2 = the M₃-move);
  the unifying theorem does not close tonight and is honestly priced.

— end FORMALIZATION.md
