# FIBER-DUALITY — Protocol-State General Position and the Fiber-Protocol Duality Theorem

**Lane:** fiber-duality (branch `fiber-duality`, cut from `math-formalization` @ e8954a3; inherits FORMALIZATION.md)
**Date:** 2026-08-31 (night) · **Primary mathematician:** GLM-5.3
**Adversarial referee (central definition):** `claude -p` (Sonnet 5) — pass before final commit (§6).
**Numerics:** `scripts/fiber-duality-verify.py` (numpy float64 + exact ℤ[ω] arithmetic; executed; raw log alongside).
**Status:** building section by section (30-min standing order; commit per section).

---

## 0. Mission recap (from FIBER-DUALITY-BRIEF.md)

1. DEFINE protocol-state general position: (i) under it, observable fiber = symmetry group EXACTLY (no phantom fibers à la T4's ordering pairs); (ii) checkable — finite/algebraic, not generic hand-waving; (iii) real protocols (arena admission-gated fire-with-skip synthesis, SELVEDGE learning plane, TOKEN-NEEDLE repaired core) satisfy it or are named violations with witnesses.
2. STATE and attempt Fiber-Protocol Duality. If it fails, the failure mode IS the result (tapestry doctrine).
3. Close or price OB-K2 (rotation-orbit isotypic construction, finite search) — same phantom-fiber disease.
4. Transfer both directions: 34,560 ring-deadlock incident as fiber phenomenon; phantom observables = unrepresented states wearing an observable's clothes.

---

## 1. Definitions — protocol-state general position

### 1.0 Frame import (TEACHER nudge, 2026-08-31 — do not build this wheel from scratch; merged back after a concurrent-write clobber, gold preserved)

**The classical frame: separating sets.** "Observable fiber = symmetry group EXACTLY" is precisely the classical statement that **O is a separating set for the group action on states**: O(s) = O(s′) ⟺ ∃g ∈ G: s′ = g·s (Derksen–Kemper, *Computational Invariant Theory*). Imports, each load-bearing:

1. **Separating ≠ generating.** A separating set can be strictly smaller than a generating set of the invariant algebra; for reductive groups the gap is fully mapped in the literature. This *is* the "no phantom fibers at minimum cost" question — the room program's T5 ("minimally-fibered") was unknowingly re-asking it, and T5's refutation-as-stated (any odd functional competes with M₃) is the separating/generating gap in miniature.
2. **General position = a named stratum, checkable by polynomial non-vanishing.** The honest checkable condition: a Zariski-open (room side) or finite-complement (protocol side) stratum S with O separating G-orbits *on S* — notation **Sep_O(S)**. **T4″'s trivial-linear-symmetry stratum already IS such a stratum; §1.2's GP is its protocol-side twin.**
3. **The classical failure mode (Mumford, *Geometric Invariant Theory* ch. 1): non-closed orbits.** Orbit-closure collisions are unseparable by ANY invariant — if they exist, phantom fibers are a THEOREM, not a disease, and the "exactly" clause degrades to a semicontinuity caveat.

**Discharge of the TEACHER's check (b) — Lemma F (finiteness kills the Mumford failure).** *For fixed configuration c, S_c is finite and discrete; every G_P-orbit is finite, hence closed. Orbit-closure collisions do not exist on the protocol side. Therefore Fiber-Protocol Duality's "exactly" clause, if it fails for protocols, fails only through separating-set deficiency (the Δ mechanisms of §1.1), never through topology.* Proof: a finite subset of a discrete space is closed; O_I⁻¹(O_I(s)) ⊇ closure(G_P·s) = G_P·s with no gap between orbit and closure. ∎ **This is the structural asymmetry between the two programs:** the room side (continuous state space, state-dependent involution σ_μ̂, E0 stratum) remains exposed to Mumford-type failures — which is exactly why T4″ is only a conjecture there — while the protocol side cannot lose "exactly" topologically; every protocol phantom is algebraic (Δ₁/Δ₂/Δ₃/Δ_F) and therefore, in principle, killable by an added separating functional (an M₃-move). The arena's K2 = the M₃-move is not an analogy; it is the same theorem in the finite setting.

### 1.0.5 The finite-state substrate (P0–P2)

**P0 (Protocol state space).** Fix a configuration c = (NCELL, RCAP, inbuf depths, K_d caps, epoch width). The *fabric state space* S_c is the finite set of all valuations of (RTL state of every cell + ring residency with flit classes + inbuf/egbuf contents + token ledger + epoch registers (gen, eps) + host-contract flags). The *transition relation* →_c ⊆ S_c × S_c is the RTL's next-state relation. R_c ⊆ S_c is the reachable set from reset. Both are finite and effectively enumerable for fixed c (the cosim suite already enumerates R_c for small configs — see quilt-verilog cosim scale-up runs).

**P1 (Protocol observable).** A protocol P *carries* a finite invariant set I = {φ_1, …, φ_k} (machine-checkable maps S_c → V_i; for SELVEDGE: INV1–INV7; for TOKEN-NEEDLE: K1–K3, N1–N2, C1, M1–M2, E1, A1′). The *protocol observable* is O_I: S_c → V_1 × … × V_k, O_I(s) = (φ_1(s), …, φ_k(s)). The *fiber of P at s* is Fiber_P(s) := O_I⁻¹(O_I(s)) ∩ R_c — the reachable states the protocol's proofs cannot distinguish from s.

**P2 (Declared symmetry group).** The arena's documents speak "declared equivalences," never a group — named gap (i) of FORMALIZATION §6.3. Definition: the *declared symmetry group* G_P ⊆ Sym(S_c) is the group generated by the relabelings the protocol's contract declares behavior-irrelevant, *provided each generator is a transition morphism*: γ ∈ Sym(S_c) is admissible iff (a) s → s′ ⟹ γ(s) → γ(s′); (b) γ is listed in the contract as licensed (this is contract data, not mathematics); (c) O_I(γs) = O_I(s) (automatic for well-posed invariants — an invariant that moved under a licensed relabeling was never an invariant). Generators on the record tonight:
- **A (SELVEDGE):** merge-order permutations (INV1 commutativity, M2 order-free multiset semantics) — licensed delivery permutations; idempotent duplicate-delivery class (the semilattice unit law);
- **B (TOKEN-NEEDLE):** flit interchangeability within a token class (M2 commutativity), epoch-wrap ABA classes (§7's *priced* equivalence — licensed but only under the widened eps arithmetic, Attack 4's arithmetic);
- **both:** replica/cell relabeling under the fabric's topological automorphisms, host-event cyclic order (E5's contract).

### 1.1 Phantoms (the disease being defined away)

**P3 (Phantom pair).** Let B: R_c → {wedge, drain} × {fresh, stale} × … be the *behavioral partition* the protocol's theorems are about (wedge-freedom = B's first coordinate constant = drain). A reachable pair (s, s′), s′ ∉ G_P·s, with O_I(s) = O_I(s′) is a **phantom pair**. It is *strong* if B(s) ≠ B(s′) (the observable asserts an equivalence the behavior contradicts), *weak* if B(s) = B(s′) (cosmetic: distinct states, same behavior, no license). T4b's 4,888 H5 pairs are weak phantoms (room-side); INV6's occ=14-wedge-satisfying-with-18-holes pair is a strong phantom (protocol-side: INV6 cannot distinguish the wedged state from a draining state — Attack 3). A's INV4 premise is a *phantom premise*: an observable (egbuf_ready's wait-predicate exit bound) whose fiber over "states with bounded exits" was never computed but is consumed as if trivial.

**P4 (Degeneracy locus).** Δ := Δ₁ ∪ Δ₂ ∪ Δ₃ ∪ Δ_F ⊆ S_c, four named mechanisms (the clause ↔ clause correspondence with tonight's room-side kills is the point — §1.3):

- **Δ₁ (undeclared isotropy).** s is fixed (or permuted within its fiber) by a transition morphism γ that is *not* in G_P's generated license. Protocol witness: the duplicate-delivery schism (Attack 4) — the semilattice readout is fixed by the clone involution (one delivery, its duplicate); the clone pair is readout-identical but ledger-distinct; the involution is a transition morphism (the fabric cannot tell the runs apart) yet only *one* direction is licensed (idempotency licenses dup-after-delivery; it does not license double-count). Room twin: the centrally-symmetric multiset {±w_k} fixed by the tangent mirror σ_μ̂ (the T4′ kill, gap 2.3e-18) — an involution the observable algebra (even functionals) cannot see, undeclared by the room's G.
- **Δ₂ (vanishing/boundary margin of a separating functional).** Every proof in both programs *consumes* a separation: a functional whose nonzero value (or non-boundary value) is load-bearing. s ∈ Δ₂ iff some consumed separation has margin 0 at s. Protocol witnesses: K3's "margin is exactly 1 hole" (kimi finding 5: holes = 1 is the boundary — any configuration change that spends it crosses into wedge-representability; hence the restated per-config inequality 2·(#token classes) + #untokenized ≤ RCAP − 1); epoch distance to wrap = 0 (Attack 4: 3-bit eps at wrap is where the ABA clone lives); K_d at cap (admission boundary). Room twin: M₃ = 0 (the mirror phantom's locus — T4a: H5(s) = H5(σs) ⟺ M₃(s) = 0).
- **Δ₃ (arrangement collapse).** s ∈ Δ₃ iff every carried invariant of P is a function of *counts alone* on a neighborhood of s — the observables determine a scalar profile but not the spatial arrangement. Protocol witnesses: INV6 is exactly this (kimi: "a statement about a scalar count; the cycle lives in the spatial arrangement" — 18 holes' worth of arrangements share the count, one of them wedged); the 34,560 incident register (corpses counted, waiting invisible — §4). Room twin: the collinear stratum (A₁ collapses to rank-1 uuᵀ; fiber = equal-path-weight classes ≫ dihedral — the 4,888).
- **Δ_F (frame singularity).** The observable is defined only relative to a frame that itself moves; s ∈ Δ_F iff s is on or near the frame's singular stratum. Protocol witnesses: A's decay-in-readout W(t) = F(S,T) assumes a *shared* T (Attack 6 / VERDICT §4: under tick divergence the fiber statement becomes dynamics-relative; repair = per-cell T_i + skew term); B's (gen, eps) freshness certificate is a *frame* for single-owner staleness that wraps (the certificate is detection at the frame, not recomputation). Room twin: the equatorial stratum ρ = 0 (E0, outside all domains) and T3a-remark-(iii): σ_μ̂ is state-dependent — "canonical involution," not a group element; the room's own symmetry is a moving frame.

### 1.2 The definition

**P5 (Protocol-state general position).** A reachable state s ∈ R_c is in **general position** for P (written s ∈ GP_P) iff:

1. **(isotropy clause)** Stab_Aut(s) = Stab_{G_P}(s), where Aut(→_c) is the transition-morphism group of the fabric — no undeclared automorphism fixes s;
2. **(margin clause)** every separating functional consumed by P's proofs has margin ≥ m at s, for the protocol's *stated* constants m > 0 (holes ≥ 2 under the restated K3; epoch distance-to-wrap ≥ 2 under widened eps; K_d ≤ cap − residual; B_busy bounds with slack);
3. **(arrangement clause)** the carried observables determine arrangement at s: the arrangement-witness registers P carries (B: entry-identity/V1, needle census N2/E1 stamps; A: per-line epoch-widened merge identity) are present and injective at s — equivalently, the local map counts → configurations has fiber = declared permutations exactly at s;
4. **(frame clause)** s is interior to a trivializing patch of P's moving frame, at distance ≥ stated constant from the singular stratum (ρ-margin; tick-skew bound; epoch-lease remaining).

**Checkability (why this is not "generic" hand-waving).** Each clause is a finite test on a fixed configuration: (1) Stab computation = fixpoint enumeration over the (finite, explicitly constructible) automorphism group of a finite transition system — BDD/SAT-sized, the same engine class the PDR runs already use; (2) margin evaluation = evaluating the invariants the asserts already evaluate, plus the per-config parameter inequalities (kimi's restated K3 is *literally* clause 2 instantiated); (3) injectivity of witness registers at s = a sortedness/uniqueness check on the live register file at s (N2's census, V1's entry-identity); (4) a distance evaluation to a named stratum (ρ, eps distance, skew counter). No measure theory, no "generic cloud" prose. Room-side, the same four clauses are exactly T4″'s stratum conditions (next table) — finite algebraic inequalities there, finite register tests here.

**P5′ (two-sentence form, for the report).** *A protocol state is in general position when every separation its proof consumes is present with explicit nonzero margin, no undeclared transition-symmetry fixes it, its observables pin arrangement and not merely counts, and it sits interior to its moving frame's patch.* *In the frame of §1.0: the state lies in the named stratum S = S_c \ Δ on which the carried observable O_I is required to be a separating set for G_P — Sep_{O_I}(S), a finite check because S_c is finite (Lemma F).* *The four clauses are each decidable by a finite test — fixpoint enumeration, margin evaluation, witness-register injectivity, frame distance — so "general position" is a checkable stratum of the state space, not a genericity sermon.*

### 1.3 The dictionary (room ↔ protocol, clause by clause)

| GP clause | Room form (tonight's theorems) | Protocol form (arena's findings) | Twin kill |
|---|---|---|---|
| Δ₁ isotropy | centrally symmetric multiset fixed by σ_μ̂ (T4′ kill, 2.3e-18) | clone involution on semilattice readout (Attack 4 schism) | undeclared automorphism fixes s ⇒ phantom by construction |
| Δ₂ margin | M₃ = 0 ⟺ mirror in fiber (T4a) | holes = 1 boundary of K3; eps at wrap; K_d at cap | separating functional's vanishing locus is the phantom locus |
| Δ₃ arrangement collapse | collinear: A₁ rank-1, equal-path-weight classes (T4b's 4,888) | INV6 count ≠ arrangement (occ=14, 18 holes, Attack 3); 34,560 register | counts cannot see the spatial cycle; wedge wears the count's clothes |
| Δ_F frame | σ_μ̂ state-dependent (T3a-iii); E0 equatorial | shared-T decay-in-readout under tick divergence (Attack 6); (gen,eps) wrap | symmetry is a moving frame; at the singular stratum the "group" is not a group |

**P6 (Fiber-exactness at s).** s is *fiber-exact* iff Fiber_P(s) = G_P·s ∩ R_c — the "exactly" clause, pointwise, i.e. O_I separates s from every non-orbit state of R_c. General position is *necessary* for fiber-exactness (§2, D2-necessity: each Δ-clause violation manufactures a phantom) and is *conjectured sufficient* (D2-sufficiency, priced §5; finite-state decidability below). By Lemma F the ⊇ half of fiber-exactness is automatic-in-principle (orbits closed; what remains is invariance of O_I under G_P, clause GP0); the entire content of the protocol-side duality is the ⊆ half.

## 2. The Fiber-Protocol Duality theorem — statement, both directions, verdict

**Setup.** Protocol P at configuration c: state space S_c (finite), transition →_c, reachable R_c, carried invariants I, observable O_I, declared group G_P (P2), stratum S := R_c \ Δ (P5). Behavioral partition B (P3).

**Theorem FD (Fiber-Protocol Duality, finite form).** *For every fixed configuration c and every s ∈ R_c in general position (GP_P):* **Fiber_P(s) = G_P·s.** *Equivalently: Sep_{O_I}(S) — the carried observable separates declared-symmetry classes exactly on the general-position stratum. Protocol obligations (admission rules, landing guarantees, epoch disciplines) are precisely the fiber-shrinking moves that enlarge S.*

The theorem splits into two directions of very different difficulty, as the brief predicted.

### 2.1 D1 (soundness: symmetry ⊆ fiber) — PROVEN, with two subtleties named

**D1.** *If every declared generator γ ∈ G_P is (a) a transition morphism of →_c, (b) reachability-preserving (γ(R_c) = R_c), and (c) O_I-invariant, then G_P·s ⊆ Fiber_P(s) for all s ∈ R_c.*

*Proof.* (c) gives O_I(γs) = O_I(s); (b) gives γs ∈ R_c. Induction on word length in the generators gives the whole group. ∎

The subtleties, both real in the record:
1. **Reachability-preservation is not free** (γ(reset) need not be reset). It must be *contract data* — and it is exactly the room-side moving-frame disease (Δ_F) in disguise: the arena licenses epoch-ABA "equivalences" that only preserve reachability under the widened-eps discipline. A licensed relabeling that fails (b) is a frame bug, not a symmetry — Attack 4's schism is precisely a (b)-failure of the naive 3-bit license.
2. **O_I-invariance (c) is the well-posedness of the invariant set**: an "invariant" that moves under a licensed relabeling was never well-defined on the quotient (the room twin: an observable not constant on H5-fibers was never a function of H5). Checking (c) is the cheapest audit in the program and the arena never ran it explicitly — INV1's commutativity miter is (c) for one generator; K1's per-dst ledger is (c) for flit interchange *within* a class; nobody checked (c) across classes (the io-queue omission kimi caught is a cross-class (c)-failure: untokenized classes move under the relabeling that K1's terms don't cover).

### 2.2 D2-necessity (GP violations manufacture phantoms) — PROVEN (constructive)

**D2n.** *If s violates any GP clause, s has a phantom (the violation's check is the witness's construction):*

- **Δ₁ violated ⇒ phantom.** The failing check *is* the witness: an undeclared transition morphism γ with O_I(γs) = O_I(s), γs ∉ G_P·s — P3's definition of a phantom pair, met. Arena instance: the clone involution on the semilattice readout (deliver-once/deliver-twice: readout-fixed, ledger-split — a strong phantom once the ledger enters B). Room instance: σ_μ̂ on {±w} multisets, gap 2.3e-18.
- **Δ₂ violated ⇒ phantom across the boundary.** A consumed separation is a pair (φ, named target class T) appearing in the proof: φ separates s from T with licensed margin m. At margin 0 the named target's member t ∈ T adjacent across the boundary has O_I(s) = O_I(t) (φ was the only separator; it just died). Arena instances: the ABA clone at eps wrap-distance 0 (Attack 4); the last-hole spend at K3's margin-1 boundary (kimi finding 5: the restated inequality is GP2 *written down*, which is why the restatement is a theorem-shape repair, not bureaucracy). Room instance: M₃ = 0 ⟺ mirror in fiber (T4a).
- **Δ₃ violated ⇒ arrangement phantom.** Counts-only observables: any two arrangements with the same count profile collide. Arena instance: INV6 at occ=14 with 18 holes — the wedged arrangement and a draining arrangement share the hole count (Attack 3; kimi: "a true invariant that does not imply the desired property"). Room instance: collinear A₁ rank-collapse, the 4,888 (T4b).
- **Δ_F violated ⇒ frame phantom.** At the singular stratum the trivialization dies: two divergence histories agree in the frame-relative observable while diverging absolutely. Arena instance: Attack 6 — decay-in-readout under tick divergence, F(S,T) blind to (T₁,T₂) skew; repair per-cell T_i = carrying the frame instead of assuming it. Room instance: E0 (ρ = 0) and state-dependent σ_μ̂ (T3a-iii).

*Proof-grade note.* In the finite setting, "the set of separations a proof consumes" is **syntactic** — extractable from the proof term (which invariants appear in which implications with which bounds). GP2's margin is therefore checkable against the proof artifact itself; this makes D2n's witnesses effectively constructible, not merely existent. **Corollary (the audit theorem): a protocol's phantom inventory is computable from (S_c, →_c, I, proof terms, contract) — no genericity, no measure theory.**

### 2.3 D2-sufficiency (GP ⇒ fiber-exact) — DECIDABLE per configuration; UNIFORM form conjectured (priced)

**D2s-finite.** *For fixed c: "∀s ∈ R_c \ Δ: Fiber_P(s) = G_P·s" is decidable by explicit enumeration* (compute O_I on R_c, hash fibers, compare with orbits — the cosim suite's decidable-only classification is this computation in miniature). **The duality's hard half is therefore a *computable* predicate in the protocol world — this is the finite-state dividend of Lemma F.**

**D2s-uniform (conjecture, priced).** *For the parameterized family (all valid configurations of the repaired synthesis core), GP_P(s) ⟹ fiber-exact at s.* Not proven tonight. Its status mirrors T4″ exactly: evidence (the arena's core survives its named attacks; each repaired defect was a Δ-clause restoration), two named attack routes (the parameterized analogue of OB-K2 — configuration families where the per-config inequality boundary is reached asymptotically; and cross-class (c)-failures of D1 like the io omission), price: one chapter-length analysis with the enumeration harness as ground truth. **The uniform form is to the finite form what T4″ is to a fixed-N computation — and the brief's prophecy holds: without GP the duality inherited T4's corpse; with GP defined, the corpse is localized to exactly one clause (D2s-uniform) of one direction.**

### 2.4 The Duality Calculus (both moves; where K2 and M₃ live)

The finite form plus D2n yields the *design calculus* — the theorem's operative content:

**Corollary FD-C (fiber management has exactly two licensed moves).** *Every phantom-killing move in the program's history is one of:*
- **(M-enrich) add a separating functional** to O_I (room: M₃ added to H4 — kills the mirror's representability *in the observable*; protocol: epoch-widened merge identity — separates the clones the readout fused; A₂ lag-2 would separate reversals);
- **(M-exclude) shrink the reachable stratum** so the phantom's birth state is unrepresentable (room: restricting to the T4″ stratum; protocol: **K2 admission — the third flit toward d cannot exist while two sit in d's inbuf; the parked-hit/full-inbuf wedge state is deleted from R_c, not detected**).

*Both moves enlarge the general-position stratum S; neither can create new phantoms (enrichment only refines fibers; exclusion only removes states); the arena's whole dispute (VERDICT §2–5) is the discovery that B's core wins by M-exclude (safety: kill representability) where A attempted M-enrich with an unpriced functional (INV4 — a separation whose margin was never computed — an M-enrich move with a fictional separator).* **K2 : F3-wedge :: M₃ : mirror is now a theorem instance (both are M-moves), not an analogy.**

### 2.5 Instantiation against the real protocols (brief item iii)

- **Admission-gated fire-with-skip synthesis (VERDICT §5): GP-COMPLIANT BY CONSTRUCTION** — the first design in either repo built to satisfy all four clauses without knowing their name: GP1 via epoch-widened merge identity (clones separated ⇒ undeclared isotropy gone); GP2 via the restated per-config K3 (margin ≥ 1 explicit) and 2-bit ow (K1 conservation = the separator actually separates); GP3 via N2 census + V1 entry-identity (arrangement witnessed); GP_F via scoping (gen,eps) to single-owner freshness (frame carried only where trivializable). **The synthesis converged on GP from the hardware side, independently — the strongest evidence tonight that GP is the right definition, not a retrofit.**
- **SELVEDGE: two GP violations with witnesses.** GP2-violation: INV4's exit bound — a consumed separation with uncomputed margin (the unpriced obligation wearing a theorem's clothes); witness: any state where egbuf_ready's wait predicate set exceeds the assumed structural bound (Attack 1's class). GP3-violation: INV6 count-vs-arrangement; witness: occ=14/18-holes (Attack 3). GP_F: soft — shared-T assumption (Attack 6); repair named (per-cell T_i). The learning plane itself (decay-in-readout, INV1 miters) is GP-clean: commutativity licenses merge-order relabeling (D1 by construction), decay is frame-carried not frame-assumed *within* the shared-T patch.
- **TOKEN-NEEDLE as-specified: three GP violations with witnesses** (all repaired in the synthesis): GP2 via 1-bit ow (K1 false as encoded — a separator that doesn't separate; witness: the K_d=2 return burst) and margin-1-hole un-restated; GP1 via the forgeable a2 marker (an undeclared host-writable "isometry" of the op-class partition); GP_F via 3-bit epoch wrap (witness: Attack 4's ABA arithmetic). Repaired core: clean as above.

**Theorem FD verdict: PROVEN in the finite per-configuration form (D1 fully; D2n constructively; D2s-finite by decidability); the uniform parameterized form is a priced conjecture whose failure locus is named (per-config boundary families, cross-class invariance failures). Indeterminate it is not — the finite form closes.**

## 3. OB-K2 resolved — the rotation-orbit isotypic construction, decided by exhaustive exact search

**The attack (FORMALIZATION §5.5, kill #2).** Relabel-ordering the C₁₂-orbit cloud {R^k w : k ∈ Z₁₂} (R = block-diag rotations by (2π/12)·(1,2,3) on R²⊕R²⊕R², generic w) by R maps ordering g ↦ g+1 and conjugates A₁ ↦ R A₁ R⁻¹ while preserving C, M₃ (order-free). Collision of (g, g+1) under H5 ⟺ A₁(g) commutes with R. **Lemma (eigenbasis reduction, seed-independent).** In the eigenbasis of R (eigenvalues ω^{±1}, ω^{±2}, ω^{±3}, ω = e^{iπ/6}): (A₁(g))_{pq} = w_p w_q · Σ_edges ω^{σ_p a − σ_q b}, so for generic w the collision is equivalent to 30 exact integer conditions — **Σ_edges ω^{σa − τb} = 0 for every ordered pair σ ≠ τ ∈ {±1,±2,±3}** — independent of the seed. (The planar reduction Q(g) = Σω^{a+b} = 0 is the pair (+1,−1) — the referee's hand-check, confirmed.) Each condition is a length-11 vanishing sum of 12th roots of unity: a ℤ[ω]-exact arithmetic problem, searchable exhaustively.

**Method.** `scripts/obk2_search.c`: DFS over all orderings of Z₁₂ (g₀ = 0 fixed — global shift multiplies every condition by a unit, preserving exact vanishing), partial sums in exact integers in ℤ[ω] = span_ℤ{1, ω, ω², ω³} (Φ₁₂ = x⁴ − x² + 1), pruned only by the admissible unit-circle bound |S| ≤ remaining edges. Admissible pruning ⇒ the search is exhaustive over all 12!/12 = 39,916,800 shift-reduced orderings. *(Honesty note: my first mag() had sign errors making it overestimate partial sums — inadmissible pruning; caught, fixed, rerun; all numbers below are from the corrected build. Also the first dihedral check was vacuous — it tested index-shifts, which ARE the R-relabel family under test, instead of sequence rotations; corrected to positions-only. Both corrections committed in the script.)*

### 3.1 Results

| mode | conditions | nodes explored | witnesses | verdict |
|---|---|---|---|---|
| planar (single R² block: exponent a+b) | 1 | 32,467,142 | **96,560** | **collision EXISTS** |
| full 6D (block-diag (1,2,3)·2π/12) | 30 | 1,048,318 | **0** | **attack CANNOT land — proven** |

- **Count-vector structure (planar), exact:** 576 vanishing count vectors of length 11 over Z₁₂; **all 576 decompose into rotated 2-term {r, r+6} and 3-term {r, r+4, r+8} relations** — Schoenberg's structure theorem for n = 2²·3 confirmed computationally at length 11 (the referee's hand reduction validated).
- **Planar witness verified in float64:** g = [0,1,2,3,4,5,7,6,8,10,11,9]: H5(g) vs H5(g+1) max component gap **1.388e−17** at cloud distance 0.538; not dihedrally related (corrected check) — a genuine phantom pair. **But: ||M₃|| = 6.2e−18** — the planar orbit is centrally symmetric (R⁶ = −I on a single block ⇒ R⁶w = −w ∈ orbit), so this witness lives **on the M₃ = 0 stratum**, where H5 is *already* non-injective by T4a (the mirror pair (g, g+6) collides there for every ordering). The new (g, g+1) phantom is a distinct pair on an already-diagnosed degenerate stratum.
- **Full 6D: zero witnesses.** The generic orbit (R⁶ = diag(−I, I, −I) ≠ −I: non-centrally-symmetric, M₃ ≠ 0, spanning, distinct unsigned lines — inside T4″'s stratum except clause (i), see below) admits **no ordering whose A₁ commutes with R**: the isotypic construction cannot manufacture an H5 phantom in the family it was named for.
- **Statistical cross-check:** 200k random orderings, min over samples of max isotypic residue = 2.909 (unit scale 11) — exact vanishing is not a near-miss phenomenon; the exhaustive zero is decisive, not lucky.

### 3.2 The resolution (and what it teaches the duality)

**OB-K2 is CLOSED: the attack is dead in the generic family.** The rotation-orbit phantom exists *only* in the degenerate planar embedding, where the cloud is centrally symmetric — i.e., exactly where the mirror phantom already lives (M₃ = 0). The attack's success set and the mirror's blindness stratum **coincide**:

**Theorem OB-K2 (blindness-locus coincidence).** *For the C₁₂-orbit family, the R-relabel ordering-phantom exists iff the embedding is degenerate (M₃ = 0); on the non-degenerate 6D embedding the phantom set is empty (exhaustive, exact).* 

Three consequences, each load-bearing for §2's duality:
1. **T4″ strengthens:** its named residual attack is discharged negative in the attack's own family. What remains open for T4″ is only the general proof obligation (submersion heuristics), no longer a named construction. (Fine print: the orbit cloud has ⟨R⟩ inside its multiset stabilizer — it violates T4″'s clause (i) (trivial linear symmetry) anyway; so OB-K2 could never have killed T4″. What the search proves is stronger and stranger: even WITH undeclared isotropy present, the phantom fails to exist — isotropy alone does not manufacture collisions.)
2. **D2n-Δ₁ sharpens to blindness-conditional form:** an undeclared symmetry γ manufactures a phantom at s iff the observable is γ-blind at s — and the γ-blindness locus is *computable* (here: exactly the degenerate embedding, decided by exhaustive search). **Δ₁ and Δ₂ are not independent clauses: Δ₁-phantoms live on Δ₂ strata.** Protocol translation, exact: the host-forgeable a2 marker (TOKEN-NEEDLE's named defect) is a γ whose blindness locus was "every op-class-visible state" — the whole domain — which is why no margin clause could save it and it needed the M-exclude move (unforgeable op class). Undeclared isotropy is harmless precisely where some carried invariant separates its action — and *only* there.
3. **Both programs agree, independently derived:** the room program killed the phantom by the M₃-move (add the odd separator; its vanishing locus is where phantoms live); the protocol program killed the same-shaped phantom by K2 (delete the state; representability dies). OB-K2's exhaustive negative is the room-side computation of what K2 does structurally: **make the collision unrepresentable rather than detected.**

Committed artifacts: `scripts/obk2_search.c` (exhaustive exact search), `scripts/fiber-duality-verify.py` (driver: ℤ[ω] count vectors, Schoenberg decomposition check, witness verification, F1 regression), `scripts/fiber-duality-numerics-raw.txt` (raw output). F1 regression reproduces FORMALIZATION's canonical exhibit gap 3.469e−18 exactly — the H5 machinery here is the same instrument.

This section complete; committed under the standing order. — §4 (both-directions transfer) next.
