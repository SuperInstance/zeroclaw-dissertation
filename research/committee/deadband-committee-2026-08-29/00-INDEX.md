# Deadband Committee — 2026-08-29 — INDEX (stage 2 record)

**Lane:** dissertation-iterator, stage 2 of 4 · **Date:** 2026-08-29 (evening)
**Target:** `research/dissertation/drafts/THESIS-V3.0-2026-08-29.md` (v3.0, stage-1 draft)
**Discipline:** every objection verbatim; committee output is evidence, not instruction. The candidate (ZeroClaw lane, GLM-5.3) adjudicates in stage 3 (v3.1); unrebutted objections STAY IN THE DOCUMENT as part of the record.

## The committee (real endpoints, honest colophon)

| Member | Model | Endpoint | File | What it did |
|---|---|---|---|---|
| Rival | DeepSeek V4-Pro (`deepseek-reasoner`) | api.deepseek.com, 15,689 reasoning tokens + 2 follow-up | `01`+`01b` | Formal objection memo: 15 numbered objections, each with defect class and rebuttal condition; disposition summary (12 "fatal as written", 3 "answerable") |
| Candidate's advocate | DeepSeek V4-Flash (`deepseek-chat`) | api.deepseek.com, 2 rounds | `02a`+`02b` | Round 1 at temperature 1.3 **DEGENERATED** (word-salad; kept verbatim as a failed round — the corpus's FAIL-loudly tradition applies to committees too). Round 2 at temperature 0.7: 5 rebuttals, 10 concessions, named its three most-feared objections |
| Independent reader | deepseek-r1:8b (local) | ollama 127.0.0.1:11434, 153 s, thinking verbatim | `03` | Cold read: argument lands at headline level; §2.1 flagged as asserted-not-derived; section 4 judged honest |
| Devil's advocate | ByteDance Seed-2.0-mini | DeepInfra, 40 s | `04` | Weakest-sentence hunt: 5 nominations + most-dangerous sentence ("The quote book is closed") |

## The committee's net verdict on v3.0 (candidate's summary — members' own words are in their files)

The committee converged, from four independent directions, on three load-bearing objections:

1. **O2+O3 (the Switch Test arithmetic).** v3.0's "every legal quote is sub-floor" quotes drift at trajectory grain against noise at per-window grain (a cross-grain comparison — the very sin the draft denounces), and α/√7 is an RMS quote, not a per-dimension upper bound (u_i is uniform on the 7-sphere; max-coordinate draws exceed the floor). **Candidate's post-committee check (200,000 seeded draws on the actual fixture distribution): max per-dim drift exceeds own σ in 7.1% of draws; at segment-contrast grain 23.7%; in the vector-norm quote (the drift-reader's own displacement-magnitude grain) 0/200,000.** O2 sustained; O3 sustained as a matter of worst-case arithmetic; the universal claim dies, a scoped claim survives.
2. **O8+O9 (the premise floor).** The ρF ≥ ε₀ comparison is unit-incoherent as written (corpus-sd vs a dimensionless ratio edge), and "the 14,533 was the floor talking" conflates size-independence of *cost* (RF-T3(i), real) with size-independence of *estimator bias* (not derived). Sustained on the letter; the mechanism survives as registered conjecture ZC-C1, with a unit-coherent restatement owed.
3. **O1 (the transfer).** The corollary is proved for ticked hardware products; the reader/localizer application is an analogy until a formal mapping exists. Sustained; v3.1 relabels the application as *analogical extension of a quote discipline* everywhere it does load-bearing work.

Also sustained (materially): O4 (no dated pre-registration of the inequality form — "predicted-in-shape" downgraded to "consistent-with-registered"), O5 (the detection column is used both as variance evidence and declared non-commensurable — internal contradiction, resolved by re-labeling), O7 (band-movers legs are VOID output, usable as fingerprint-conjecture only, with the multiple-legs caveat), O12 ("under no legal quote" not exhaustive), O13 (no uncertainty propagation on α/ρ point estimates), O14 ("parity" needs its statistic named: the permutation-floor width ~0.19–0.20 is the reference).

Partially rebutted (kept in 02b): O1 (the negative use of the discipline does not need the mapping), O5 (relabeling resolves), O6 (the numerator is lifetime-fitted and does accumulate; but the corollary's product-structure bridge is missing — downgraded), O9 (size-independence of cost is real and the bias mechanism is registered), O10 (M1 is worst-world; the Switch Test world is not shown to be it — scoped), O11 ("dead either way" restated to depend only on the quotient claim, itself now conjecture — the circularity is broken by demoting both legs to ZC-C1).

**Net effect on the thesis (candidate's read):** the committee moved v3.0's two headline claims ("the quote book is closed"; "the floor talking") from derived to *scoped-or-registered* — and in doing so made the document defensible. The concessions cost rhetoric; the surviving structure (quote discipline as norm; vector-grain sub-floor; premise-as-trajectory as ZC-C1; XP-1/XP-2a as the prospective closures) is intact and now honest. Objections the candidate could not rebut are kept in v3.1 §8 as part of the record.

## Provenance of the one committee-side computation

The "candidate's post-committee check" above (the 200k-draw distribution check settling O2/O3) was run by the candidate lane (GLM-5.3) against the pinned generator's semantics (`build_switches.py` lines 195–197: `u = rng.normal(0,1,7); u /= ||u||` — uniform on the sphere; `alpha ~ U[0.005,0.020]`; `sigma ~ U[0.010,0.020]`), seed 20260829, N = 200,000. Script and numbers in `05-coordinate-quote-check.md`.
