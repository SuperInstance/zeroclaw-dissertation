# E2 RESPONSE — To the devil's pre-run audit (d69824b), after the run

**Dated: 2026-08-19.** Companion to `ADDENDUM3-DEVILS-AUDIT-ADOPTION-2026-08-19.md` (the registration for everything below, committed before the S6/S7 generation and these runs). Artifacts: elephant commit (this push) — nights `night-S6/S7.jsonl` (deterministic, verified), `data/e2/e2-audit-response-results.json`, `scripts/e2_audit_response.py`.

## Disposition, attack by attack

| # | audit attack | disposition | action taken |
|---|---|---|---|
| 1 | κ̂ low-bias makes ±0.1 impossibly strict; −0.41 bias seen at 0.9 | **mechanism inapplicable; criterion adopted anyway** | the E2 ratio estimators use no vMF κ̂ (dial-space medians/norms); the −0.41 was the prior instrument. Measured bias curve of THIS estimator (on fixtures, attempt 3 rep 0): +0.094/+0.024/+0.043/+0.004/−0.058 across rungs 0→0.9. Monotonicity registered as the primary ladder criterion (C1); ±0.1 demoted to secondary. Under it, attempt 3 passes for BOTH estimators (E-seg 0.013→0.178→0.376→0.687→0.790; E-cont 0.094→0.174→0.343→0.604→0.852, on fixtures) — the rung-0.9 knife-edge (−0.1096) no longer demotes E-seg. |
| 2 | 5 monotone families just move the degeneracy to step-timing | **conceded and fixed** | S6 (double reversal) + S7 (oscillation) registered in addendum C2 BEFORE generation, built from the same text banks, attendance extended (every new persona ≥3 families). Clear-eligibility now requires CI > 0.6 on the extended corpus AND the non-monotonic-drift variant (the audit's sentence, adopted verbatim). |
| 3 | E3's asymmetry is unfalsifiable | **out of scope here** | E3 is not this experiment; the paraphrase-crossover + dispositive-miss registration (S_max, reversed asymmetry) is flagged to the E3 owner untouched. |
| 4 | terminal indeterminacy unregistered | **adopted (C3)** | fully-inside-band CI ⇒ the filed sentence is "undecidable with this instrument class… unmeasurable at this grain," no more-work-needed prose. Not triggered by any current CI (all upper bounds reach ≥0.92). |
| 5 | two-attempt cap; estimator do-over loop | **ruling requested (C4); moratorium in force** | facts filed: 3 ladder attempts, 2 estimator designs (the cap's own language targets estimator rebuilds; no third estimator was built; attempt 2's formal failure was planting-construction — every plantable rung passed). Field number marked PROVISIONAL; strict-letter and intent readings diverge exactly as C4 states; no further ladder attempts or rebuilds while the ruling is pending. |

## New numbers

**Ladder robustness on the 11-night corpus (on fixtures, canonical presence, not a new attempt):** strict monotonicity holds for both estimators — E-seg 0.011 → 0.206 → 0.392 → 0.705 → 0.808; E-cont 0.078 → 0.167 → 0.342 → 0.607 → 0.847 (rep 0; reps 1–2 stable). E-cont additionally within ±0.1 at every rung, on fixtures.

**Field extended variants (15 real readers, 11 nights, registered corpus_sd 0.2367 frozen):**

| variant (field) | ratio | bootstrap 95% CI | class |
|---|---|---|---|
| extended corpus, E-cont | 0.6718 | [0.4383, 0.9210] | touches band — indeterminate |
| extended corpus, E-seg | 0.7660 | [0.4766, 0.9960] | touches band — indeterminate |
| non-monotonic drift only, E-cont | 0.8494 | [0.5695, 1.0545] | touches band — indeterminate |
| non-monotonic drift only, E-seg | 0.9685 | [0.6455, 1.1010] | above band |

Baseline ICC on the extended corpus (field): 0.7693 (vs 0.7714 primary — stable). **Clear-eligibility test (C2): NOT met** — clearing requires CI entirely >0.6 on both the extended and non-monotonic variants; ext E-cont's lower bound is 0.438 and nonmono E-cont's is 0.570. No kill either; no CI is fully inside the band (C3's undecidable class does not fire). The registered verdict class therefore remains **indeterminate** under every audit-corrected estimator and corpus variant computed.

## What the non-monotonic families show (field)

Reversals and oscillations shrink net within-reader displacement (a reader partially returns toward her own baseline when the room reverses), so drift falls and the ratio rises: points move 0.6088 → 0.6718 (extended) → 0.8494/0.9685 (non-monotonic drift only, field). Direction: toward the premise. Magnitude: not enough to clear — the reader-sample CIs still straddle 0.6, and E-seg's solo above-band CI does not satisfy a rule that requires the continuity estimator too. The honest sentence: **the audit's own fix moves the number toward the premise, and the number still will not commit.**

## Standing status

1. The primary filed number (0.6088, CI [0.371, 0.921], field) is PROVISIONAL pending the C4 ruling; if the strict letter rules, it is withdrawn and replaced by the measurement-death sentence, and every variant above inherits that status.
2. The devil's central warning — "you will run 3 days of compute, get a number in the band, and write 10 pages explaining why it doesn't count" — was answered by registration, not prose: every outcome class the audit demanded is now pre-committed (C2 clear rule, C3 undecidable sentence, C4 moratorium), and the one place the audit's mechanism misfired for this estimator (κ̂) is answered with a measured bias curve, on fixtures, not an argument.
3. Count of launderings: unchanged, six.

*Filed 2026-08-19. Prefix discipline observed: fixtures where fixtures, field where field.*
