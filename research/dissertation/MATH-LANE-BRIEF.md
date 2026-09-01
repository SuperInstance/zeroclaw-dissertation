# MATH-LANE BRIEF — Formalization of the Identifiability Program

You are the FORMALIZATION lane for the dissertation mathematics. Repo: /home/eileen/projects/zeroclaw-dissertation. Branch: `math-formalization` (commit there, do NOT merge to master, do NOT push). DeepSeek/DeepInfra REVOKED — do not call. Use `claude -p` (Sonnet 5) as adversarial referee; `kimi -p` as second opinion; you (GLM-5.3) are the primary mathematician.

## Deliverable
`research/dissertation/FORMALIZATION.md` — referee-checkable formalization of the identifiability program.

## Read first (in order)
1. `research/dissertation/drafts/THESIS-V3.2-2026-08-31.md` — §2.0 observable ladder H1→H2spec→H2full→H4→H5 (measured fibers); §2 doctoral core; §2.3 priced obligation; C2 = H5 fiber conjecture.
2. `research/committee/foreman-v3/identifiability-prompt.md`, `identifiability-claude.txt`, `identifiability-lane2-haiku.txt` — dual-lane derivations (theorems 4, 6, Q5.2, Q6.1; counterexamples 1–6).
3. `research/dissertation/THESIS-V3.md` §6.5 — scoping discipline.
4. `elephant/vmf.py`, `elephant/field.py` — the measured instruments.

## The conjecture to formalize
Every practical room-hash lives on the ladder (invariance of domain: no injective continuous observable into R^m, m < 6N). Choosing an observable = choosing a fiber. Claim on the table: **H5 = (H4, M₃) kills mirror + third-moment classes; residual fiber = exactly the problem's symmetry group (phase-shift/reversal on symmetric clouds)** — H5 is minimally-fibered.

## Sections to write
1. Precise definitions: room state (empirical measure on S⁶, N≥10), H1..H5 as functions, fiber, symmetric-cloud class, phase-shift/reversal transformations.
2. Theorems with proofs or exactly-priced gaps:
   - T1 invariance-of-domain bound (verify glm53 sketch)
   - T2 H1 fiber dimensionality (6N−7) — full proof or exact gap
   - T3 ℤ₂ mirror: Q5.2/Q6.1 formalized (H4 global mirror fiber; antiphase twins positive-dimensional for N≥11)
   - T4 H5 separation — THEOREM-with-attempt or named CONJECTURE: (a) counterexample search space, (b) concrete numpy falsification experiment on small N, (c) kill condition registered BEFORE the attempt
   - T5 minimality: no continuous observable strictly between H4 and H5 has smaller fiber — prove, or state exactly what's missing
3. Numerical verification: re-run the glm53 counterexamples (explicit parameters exist) in numpy float64; confirm the ladder table's fiber measurements; mismatches are findings — report honestly.
4. Honesty clauses: obligations priced, never laundered; negative results first-class.
5. Sharpening pass (captain's order): section "Fiber lens on ring coherence" — read /home/eileen/projects/quilt-verilog/docs/coherence-arena/PROPOSAL-A.md (SELVEDGE) + PROPOSAL-B.md (TOKEN-NEEDLE) + ATTACKS-ON-A.md. Treat each protocol's wedge-freedom claim as an observable with a fiber: is the residual fiber exactly the symmetry group? Does the H5 program (kill accidental fiber, keep only symmetry) transfer to protocol invariants? If yes, that unifying theorem is the breakthrough.

## Adversarial passes
- `claude -p "Here is conjecture T4: <paste>. Hunt for a counterexample: a configuration where H4 agrees but H5 also fails to separate. Try sign-pattern families, phase-shifted clouds, N=12, small amplitudes."` — if it finds one, the refutation IS the result; publish it.
- `kimi -p` independent read of T2/T3 proofs.

## Report back
Which theorems PROVEN tonight / which PRICED; did T4 survive the adversarial pass; numerical re-run results vs the ladder table; did the fiber lens transfer to coherence.
