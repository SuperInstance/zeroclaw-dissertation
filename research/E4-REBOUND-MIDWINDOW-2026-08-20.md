# E4 REBOUND — Mid-Window Rate Check (Day ~1 of 30)

**Run:** 2026-08-20 14:38 AKDT · 1.6 days into the registered window (2026-08-19 → 2026-09-18)
**Script:** `scripts/e4_rebound_check.py` (git history walk, 248 fleet repos under `/home/eileen/projects/`, LOCAL only, read-only)
**Status: EARLY READ. This is not the window-end verdict. The registered recompute at 2026-09-18 still decides.**

## Headline numbers

| Read | Span | Active repos | Corrections | Forward | Pooled rate | Verdict vs 0.15 |
|------|------|-----|----|----|----|----|
| **A: window-to-date** (registered-consistent) | 08-19 00:00 → now (1.6d) | 6 of 25 non-quiet | 7 | 154 | **0.0455** | **≤ 0.15 → settling side** |
| **B: last-7-days context** | 08-13 → now (7.6d) | 28 of 90 non-quiet | 81 | 932 | **0.0869** | **≤ 0.15 → settling side** |

Corrections/day: **4.3** (window-to-date) / **10.6** (7-day) — below the old Ch6 baseline of 11.6 and far below the +73% endpoint of 20.1.

## Verdict (early, day ~1)

- **Both reads are on the SETTLING side of the 0.15 threshold** — pooled 0.046 (window) and 0.087 (7-day), comfortably under. No flooding signal in the aggregate.
- **The +73% corrections/day trajectory has not continued.** Corrections/day is currently at or below the *pre-surge* baseline (11.6), not the post-surge 20.1. The corrections flood, if it ever was one, is receding, not accelerating.
- The 7-day bootstrap CI over repo-day cells is [0.047, 0.132] — entirely below 0.15, though indicative only at this n (92 cells, 28 repos).

## The honest caveat that matters most

The registration's question is what happens **"when forward commits normalize."** They haven't yet: the fleet is still mid-surge at **~123 forward commits/day** (932 in 7.6 days across active repos). A low rate sitting on top of an inflated denominator is exactly the configuration Ch6 already flagged as potentially artifactual — the counterfactual 0.497 assumed the denominator returned to normal while corrections held. So this early read **cannot yet distinguish "genuinely settling" from "denominator still surging."** The window has 28 days left to watch which way it breaks as forward-commit volume normalizes.

Secondary caveats:
- Only **6 repos cleared the 5-commit dormant bar** in the 1.6-day window read — the registered per-repo-per-day estimate is running on a skeleton sample. Day ~1 of 30.
- Per-repo spread is wide: `lucineer-system` (4.0), `cns-bridge` (1.33), `fleet-dashboard` (1.0) are individually flooding-shaped but at n=5–7 commits each; `ai-writings` (486 commits, rate 0.013) dominates the pooled denominator and pulls it down.
- Correction markers are heuristic (word-boundary fix/correct/revert/address/bug/repair/patch on the subject line); spot-checks on `mist-game` and `zeroclaw-dissertation` showed the matches are genuine corrections, but misclassification error at ±few percent is expected.
- The window-start line (2026-08-19 00:00 AKDT) splits mid-work-day; day-1 commits are dominated by dissertation and writing-repo forward activity.

## Provenance note

First run of the script had a slot-inversion bug (corrections and forward counts swapped), producing absurd inverted rates (22.0 pooled). Caught by eyeball-audit of raw commit subjects, fixed, re-run; the numbers above are post-fix and spot-verified. The bug is worth remembering at window-end recompute: always eyeball a sample of classified commits.

## Bottom line

**Day-1 read: SETTLING (rate 0.046–0.087, well under 0.15; corrections/day 4–11, below even the old 11.6 baseline).** But the denominator hasn't normalized, the sample is 6 repos deep, and 28 days remain. No verdict, no victory lap — the 2026-09-18 recompute decides.
