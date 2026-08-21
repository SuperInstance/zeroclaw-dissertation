# External Zeroclaw Ideas — Synthesis (2026-08-20)

Casey dropped two external docs (from another agent) as "ideas for the zeroclaw while you keep working."
Verdict: **~85% re-derivation of ground we've already covered; ~15% genuinely useful to fold in.** Filed verbatim in `research/external/`.

## What these docs propose vs. where we actually are

| External proposal | Our actual state (already run) |
|---|---|
| "Phase 0-1 scaffolding" (dial_bank.py, edge_extractor.py, edge_matcher.py, baselines.py, reader_delta.py, deadman.py, harvester.py, pipeline.py) | Gate 1 (`vmf.py`) CLOSED, audited clean. Encoder-tier room-heldout FAILED 1/3 → memorization finding. Reader-delta DOWNGRADED to "mean-shift, baseline-relative". Rival pass-5, silence test (SPLIT), E5 (94% archetype structure), slope regression (H-reader≡room), E4 Clock-Split (INDETERMINATE → Stage 2), drift-geometry sweep (reductio). |
| "vMF MLE is ~20 lines of SciPy" | Already implemented + GPU-batched (111.6× speedup, bit-parity). |
| "reader calibration = blind source separation (M_r s + b_r)" | Crisp framing, but reader-delta already empirically downgraded — the "doctor reads the nurse" second-order reading failed the Switch Test. |
| "sheaf cohomology / GL(9) holonomy = philosophical decoration" | Already ruled the same way internally. Confirms. |
| "co-linear algebra = Cayley graph of R^9" | Matches our existing framing (cocycle conditions already proven at 1e-12 in field-edge↔ledger bridge). |

## The genuinely useful ~15% (worth folding in)

1. **Caller-aware dependency weights** — the gems doc's crispest articulation: "a spreadsheet where A1's value depends on *who asked* is a genuinely new primitive." Good one-liner for the dissertation intro.
2. **Steiger's Z-test for dependent correlations** — a concrete statistical test for "edge beats state-baseline" deadman gates we don't yet use. Candidate addition to the falsification protocol.
3. **Triangulation as weighted least-squares** — M_r matrix + per-reader Σ_r, closed-form fusion. Even though reader-delta was downgraded *empirically*, this is the correct *math* to cite when we explain WHY it's mean-shift-only.
4. **The "gems" distillation** (3 primitives + 2 methodologies + 1 operationalization) — a clean external summary that validates our claim inventory. Useful as a "what a neutral reader sees" sanity check against `topic.md`.

## Not worth re-litigating

- Re-building the scaffolding (we're past it).
- Sheaf cohomology / GL(9) holonomy (both sides agree: decoration).
- Polyformalism/JEPA "inverses" as a duality (both sides agree: not a theorem).

*Action: folded into `topic.md` claim inventory next time it's updated; no new experiments triggered.*
