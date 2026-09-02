# §8.4 EXECUTED — 20-Clause Resolution + κ/π Pass (Results Addendum)

**Run:** 2026-08-31 · single serial local lane · zero spend, zero external calls (per approved provisions).
**Pinned inventory:** `quilt-verilog@g3-kinduction@09bbcd9` (scores computed via `git show` against that SHA).
**Script:** `section8-twenty-clause-pass.py` (this directory). **Raw scores:** `section8-twenty-clause-results.json`.

## Deviations found at pin time (honest, before results)

- The pinned inventory has **1** fully-clean clause (whole population), not 2 — the earlier "2 clean of 856" count was workspace drift; the pinned `.pla` has exactly 854 clause rows. Sample topped up from the kept set to hold 20 total: 1 clean + 7 kept + 12 dropped.

## Scores (κ = ambiguous-literal fraction; π = unseparated-pair count on support)

| stratum | clauses | κ range | π range |
|---|---|---|---|
| clean (#853, 3-lit) | 1 | 0.0 | 1 |
| kept, 2-lit (#33,37,38,39) | 4 | 1.0 | 1 |
| kept, 5-lit (#54–56) | 3 | 0.8 | 10 |
| dropped, 2-lit (#0–6) | 7 | 0.5 | 1 |
| dropped, 3-lit (#7–11) | 5 | 0.667 | 3 |

**κ: min 0.0 · max 1.0 · mean 0.662.** π tracks κ² (pair-combinatorics of the same ambiguity): a 5-lit clause at κ=0.8 has π=10 of 10 pairs unseparated.

## Findings

1. **The gen_assumes keep-set audit (provision #4):** the 7 sampled kept clauses carry κ = 0.8–1.0 — *every* kept clause in the sample is fully or near-fully unresolvable at the folded-numbering level. Their resolution into RTLIL succeeded only because the `.aim` map resolves lo### ordinals directly; the folded_map's `ok/ambiguous` field judges a *different* question (which pre-fold latch the column represents). So the keep-set is not self-confirming *by mapping* — but its semantic provenance (which fabric signal each clause constrains) is **unaskable** at this inventory. The self-confirming-phantom risk stays live exactly as framed; first real audit verdict: **keep-set provenance unaskable pending symbol-named re-dump.**
2. **Clean clause (#853):** fully resolvable (κ=0), single unseparated pair (itself — trivial), provenance `unverified-pending-redump` — folded_map carries ok-status as (folded_idx, bit) with no symbol name, so even the one clean clause cannot yet be matched against the symbol-named readable. The re-dump is the unlock for the entire clean path, and the clean path has exactly one member to unlock.
3. **Dropped clauses price lower than kept ones** on κ (0.5–0.667 vs 0.8–1.0): gen_assumes dropped them for `<colmap>`-unresolvable literals, but the survivors of that filter are the *most* mapping-blind clauses in the inventory. The filter selected for ambiguity, not against it. This is the pass's sharpest single result.

## Claim status

Expressiveness claim supported at 20-clause scale: Δ₀-coarseness (κ, π) prices every clause in the sample, cleanly separating strata the existing tooling conflates. Industrial claim (full 854 pass + pruning-effectiveness) remains behind the §8.6 gate: re-dump complete AND Casey's explicit nod. Not softened.
