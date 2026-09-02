# PROPOSAL — §8 Feasibility Sketch: The Duality Calculus as a Clause-Pricing Instrument for g3-kinduction

**Status:** PROPOSAL — not merged into FIBER-DUALITY.md. Awaiting captain/lane sign-off.
**Date:** 2026-08-31
**Provenance:** Ideator nudge (eco-riker) → ZeroClaw lane assessment → materials verified live on quilt-verilog @ g3-kinduction (09bbcd9). Extends §6 (6aa169c) / §5 OB-FD1 limitation.

---

## §8.1 The opportunity, stated honestly

OB-FD1 (§5, limitation #2) records that the fiber-duality instantiations are *documentary, not machine-checked*. The g3-kinduction lane holds an object of exactly the shape the Duality Calculus claims to price: **854 extracted PLA clauses of unknown quality** whose provenance is `abc pdr -I` — which SEEDS clauses without verifying them (a false-at-init clause was accepted on probe). The lane's own tooling already performs one sound-but-blind pruning: `gen_assumes.py` drops unresolvable clauses.

The proposed move: classify each candidate clause as an **M-move** and price it —
- **separating**: its cube boundary crosses a frame PDR actually built (kills a reachable-state twin at depth k);
- **Δ-violating**: it manufactures a phantom — a separation with no reachable witness behind it;
- **dead**: it proves nothing PDR's own frames didn't already give.

This converts "854 clauses of unknown quality" into a **priced fiber-inventory**, gives the dissertation its first machine-checked instantiation adjacent to OB-FD1, and gives the hardware lane a principled pre-dump pruning pass.

## §8.2 What the live materials say (verified 2026-08-31, not assumed)

We pulled the inventory and ran fresh counts. The data *reshapes* the sketch:

| Fact | Value | Source |
|---|---|---|
| PLA clauses (.p header) | 854 | `fabric.conservation.invariant.pla` |
| Latch columns in folded_map.json | 673 | `folded_map.json` |
| Columns with **clean** mapping | **5** (0.7%) | `folded_map.json`, status `ok` |
| Columns ambiguous | 668 | same |
| Clauses touching ≥1 ambiguous column | **854/854** (100%) | computed |
| Clauses fully clean | 2 (of 856 parsed rows; 2 rows are non-clause tail) | computed |
| Clauses kept by gen_assumes (resolvable) | 32 (3.7%) | `report.assume.json` |
| Clauses dropped as unresolvable | 822 (96.3%) | same |
| Kept-clause sizes | only 2–3 literals | `clause_size_hist` |
| Clause families in kept set | engine×5, cross-core×8, f_accounting×5 | `families` |
| Literal-count dist (full 854) | 4-lit: 264 · 3-lit: 191 · 5-lit: 167 · 6-lit: 76 · 2-lit: 67 … | computed |

**The headline finding:** the clean/ambiguous stratification we proposed is not 50/50 — it is *ambiguity-dominant by three orders of magnitude*. The "full M-move verdict on clean clauses" path covers essentially nothing (5 columns). The Δ₀-coarseness path is not the auxiliary; **it is the whole instrument**. The §6 pigeonhole-coarseness machinery (observable simply not separating; no symmetry involved) stops being a caveat and becomes the load-bearing transfer: *PLA latch numbering that cannot distinguish two pre-fold latches is precisely a non-separating observable on the twin states those latches represent.*

## §8.3 Classification protocol (feasibility sketch, machine-checkable)

For each clause c over literal set L(c):

1. **Resolve** each lo### column against `folded_map.json` + `.aim`. Resolution outcome is a three-way score per literal: `ok` / `ambiguous` / `<colmap>`-unresolvable.
2. **Coarseness score** κ(c) = fraction of L(c) landing in ambiguous columns, weighted by the pigeonhole count — how many pre-fold latch pairs the lo### numbering fails to separate on c's support. Reuses Δ₀ from §6 as-is; no new mathematics required for this step.
3. **Frame-crossing test** (the "separating" definition, per caution #2): does c's cube boundary exclude a state present in a built PDR frame (reachable-to-depth-k)? Operationalized against the sby PDR run dirs (`fabric.conservation.pdr/model/invariant.txt` provides the committed-readable comparison). A clause that excludes only states PDR never built = **dead**. A clause that excludes nothing at all reachable = **Δ-violating candidate** (phantom separator — the probe already showed PDR accepts these).
4. **Verdict lattice:** `dead` ⊂ `separating` ⊂ `Δ-violating` is *not* a total order — a clause can be separating on one frame and phantom past it. The sketch outputs the verdict **per frame depth**, which is exactly the acclimation-curve shape from the room side. (Noted, not claimed: this correspondence is suggestive, not proven.)

## §8.4 The worked micro-example (scoped commitment)

**Pinned inventory:** `quilt-verilog@g3-kinduction@09bbcd9` — all pulls and scores below are reproducible against that SHA exactly.

**Framing (promoted from limitations per approval provisions):** the 32 kept clauses are precisely the population where the self-confirming-phantom risk is *live* — `pdr -I` seeds are never independently verified (09bbcd9's finding: "ABC re-verified" was PDR self-check only). The κ scores on the 6 kept family-stratified picks therefore double as **the first real audit of gen_assumes' keep-set**. Even a null result prices the keep-set — that is the deliverable either way.

20 clauses, stratified as the data dictates:
- 2 fully-clean clauses (the entire clean population — include both);
- 6 kept-by-gen_assumes clauses (2–3 literal, family-stratified: ≥2 engine, ≥2 cross-core, ≥2 f_accounting);
- 12 dropped clauses sampled across the literal-count distribution (2,4,5,6-lit, ≥2 with `<colmap>` literals, ≥4 with named-but-ambiguous literals like `u_coreA.w_rq[10]`, `u_engA.lad[5]` — these appear repeatedly in `dropped_literals` and give the coarseness score named referents).

Each gets: resolution score, κ(c), frame-crossing verdict per depth, and a one-line prose verdict in the §4 transfer style ("unpriced obligation wearing a theorem's clothes" ↔ "unverified clause wearing an invariant's clothes").

**Claim discipline:** the sketch claims *expressiveness* — "the Duality Calculus is sufficient to price this inventory" — demonstrated on 20 clauses. It does NOT claim industrial instantiation, pruning effectiveness, or any end-to-end improvement to g3-kinduction until someone runs the full pass. That escalation is a separate gate (§8.6).

## §8.5 What this buys each yard

- **Dissertation:** first machine-checked-adjacent instantiation for OB-FD1's otherwise documentary status; the Δ₀-coarseness-as-ambiguity-metric reuse — the one genuinely new mathematical move here — exercised on real hardware data; a negative-result-friendly frame (if the pricing finds mostly-dead clauses, that *supports* the pdr -I seeding critique with evidence).
- **quilt-verilog g3:** a principled pre-dump ordering for the symbol-named re-dump — score before dump, not after; direct evidence for how much of the 854 the lane should even bother naming; a second, independent check on the "ABC re-verified" failure already recorded.
- **Both:** a joint artifact whose value is the *transfer itself* — same mathematics, two yards (tapestry doctrine; the seam made concrete).

## §8.6 Gate to escalation (not part of this proposal)

Full 854-clause pricing pass + pruning-effectiveness measurement (does dropping dead clauses change k-induction outcome or runtime?) is the industrial claim. Prerequisites: symbol-named re-dump complete (so `.ilb` carries real names), frame data exported from a fresh PDR run, and Casey's nod per the spending/routing doctrine (GLM lanes only; serial, per the concurrent-lane starvation lesson).

## §8.7 Honest limitations

- The coarseness score prices *the mapping's* blindness, not the clause's truth. An ambiguous-mapped clause can still be true; κ(c) high does not mean c is phantom — it means we *cannot yet ask*. The sketch says so in-line.
- Frame-crossing uses PDR's own reachable-to-k as oracle; a clause dead at max-k may still matter at k+1. Inherent to any PDR-relative definition; scoped, not hidden.
- The 34,560-strong-phantom analogy (stable fixpoint of visible dynamics) suggests the worst clauses here may be *self-confirming* under pdr -I seeding — the sketch can name this risk but not measure it at 20-clause scale.

---

**Verdict requested:** approve §8 as scoped (micro-example, expressiveness claim only), amend, or hold for the re-dump.
