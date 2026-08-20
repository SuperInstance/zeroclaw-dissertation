# Rival Pass 5 — Downgrade Verification: Is It Complete and Honest?

*Committee Rival A, fifth dispatch, 2026-08-19. Single job: confirm the reader-delta downgrade (reader-delta → mean-shift, baseline-relative delta) is complete and honest in chapter-6-the-seam.md, or find where it is not. Read against zeroclaw-switch-verdict.md, SWITCH-TEST-RESULTS-2026-08-19.md, and my own pass-4 + the devil's pass-4. Read-only; no chapter text modified.*

---

## Verdict: DOWNGRADE COMPLETE

The downgrade on the table — reader-delta reduced from "second-order reading" to *a mean-shift, baseline-relative delta that reads the size of the step from a reader's own baseline, not the reader's change-of-reading; real for mean-moving regimes only; a pre-switch classification edge only; "second-order" surviving only as the structural term for baseline-relativity* — **is stated fully and honestly in §6.4 (line 35), and no sentence anywhere re-asserts "second-order reading" as a live claim.** The premise is honestly labeled indeterminate, inside the kill band, with the field test explicitly open. The rival's median-static win is booked with the exact numbers and the exact killing phrase ("no temporal structure at all").

That is the verdict. What follows are four residual problems and two notes. None of them re-smuggles the old claim — every correction is present in the chapter (§6.2's "demolished" and "survived" paragraphs, §6.4, §6.5's "Not claimed"). But each is a place where the chapter leaves a demolished number standing as an unqualified headline and corrects it one paragraph later instead of inline — which is precisely what my pass-4 required edits #1 and #5 told ZeroClaw to fix, and which it did not do inline.

## The four questions, answered

**(1) Full statement, no smuggling?** The downgrade is fully stated in §6.4 line 35. No live sentence re-asserts "second-order reading." But see Residuals 1–2: §6.2's clause bullets leave the pre-demolition strong claims standing unqualified in the headline, corrected only in the following "demolished" paragraph.

**(2) Premise honestly labeled?** Yes. Line 35: "**indeterminate**: the fully-instrumented premise test on real readers remains the open measurement," and the number is placed "inside the devil's 0.3–0.6 kill band." Both halves of the required honest labeling are present.

**(3) Rival wins honestly booked?** Yes — not softened. Line 35 books the exact numbers (0.816 / 0.800 vs 0.435 / 0.467) with "no temporal structure at all." Minor precision issues only (Residual 4).

**(4) Residual "second-order beats first-order"?** Yes, in §6.2's clause bullets (lines 13, 15) — corrected in line 19, not inline. Residuals 1–2.

## Residual problems

### Residual 1 — §6.2 line 15 (the clause 3 bullet) presents four demolished claims as an unqualified headline

Exact quote (line 15):

> **Clause 3 (cross-strata transfer, Rival A's clause):** SEG1→SEG2 numeric transfer r = 0.967, R²_LOO = 0.943, 4.5× better than chance; class transfer 13/13. The strongest first-order variant reaches 12/13 on *labels* and cannot produce a numeric drift prediction at all — it has no baseline, hence no excursion, hence no drift.

Four problems in one sentence, each corrected only one paragraph later (line 19):

- **"cross-strata transfer"** — my required edit #5: *"Everywhere 'cross-strata' appears for SEG1→SEG2: 'cross-condition.'"* ZeroClaw's own line 19 concedes "the clause that ran was cross-condition … not cross-strata." The laundered term survives in the headline; the correction sits below it.
- **"r = 0.967"** — my required edit #1: the honest number is segment-local r = 0.83. Line 19 concedes "segment-local refit: r = 0.829." The inflated number survives in the headline.
- **"4.5× better than chance"** — my §2.2: that is 4.5× against the weakest baseline in the building; the zero-machinery class-conditional mean achieves 6.0× (MAE 0.0153 vs the regression's 0.0206). The strawman headline survives.
- **"cannot produce a numeric drift prediction at all — it has no baseline, hence no excursion, hence no drift"** — demolished as definitional. A class-conditional mean with zero SEG1 data *does* predict e2 (MAE 0.0153 < 0.0206). "cannot … at all" is false in the strong form; it is true only for raw (unnormalized) first-order features. The caveat is one paragraph down.

This is the one bullet where a reader quoting line 15 in isolation gets the crown-claim verbatim with none of the demolition attached.

### Residual 2 — §6.2 line 13 (the clause 1 bullet) states "kill condition does not fire" with the raw 1.000-vs-0.667 margin

Exact quote (line 13):

> … reader-delta purity 1.000 = 2.00× the noise floor … Best first-order variant (of four, including the two strongest ablations): purity 0.667. The kill condition does not fire.

Line 19(c) then concedes that first-order + per-nurse median subtraction reproduces purity 1.000, and that "the margin over a *normalized* first-order is definitional." The bullet prints "kill condition does not fire" and "1.000 vs 0.667" as if the margin were real, with the "the comparison baseline was defined without the winning preprocessing" caveat deferred to line 19. Same statement-then-correction structure as Residual 1.

### Residual 3 — §6.5 line 39 says "not a reindex"; §6.2 line 19 has already reduced it to "not an identity"

Line 19: "**'Not a reindex' survives only as 'not an identity'**".
Line 39: "the second-order object is **not a reindex**, on the conditional premise, at deadman discipline".

My §2.4: *"'not a reindex' must be re-worded to 'not an identity'."* The chapter's own demolition (line 19) performs that re-wording, then §6.5's "Claimed" list re-uses the stronger term. Inconsistent within the same document.

### Residual 4 — §6.4 line 35 conflates localization r with detection rate, and omits the median-static's control-alarm cost

Exact quote (line 35):

> … beat it on switch localization (r 0.816 / 0.800 vs 0.435 / 0.467) …

- **Metric conflation:** "r 0.816 / 0.800" and "0.435 / 0.467" mix two metrics — 0.816 and 0.435 are localization r; 0.800 and 0.467 are detection *rates*. The "r" prefix distributes ambiguously, implying two r-values per cell. The switch test's own table separates "r vs planted" from "detection rate"; the chapter's compression loses the distinction.
- **Omitted trade-off:** the median-static's detection 0.800 carries a control-alarm rate of 0.25 against the drift-reader's 0.0. The localization r (0.816 vs 0.435) is clean either way, so the headline claim stays true; but the detection numbers are less clean than the compressed "0.800 vs 0.467" implies.

## Notes (not smuggling, but worth stating)

### Note A — "field kill ratio 0.5599 real-only / 0.4898 grounded" (line 35)

The number is correctly labeled indeterminate, in-band (0.3–0.6), with the field test open. But the phrase "field kill ratio" sits awkwardly next to "the fully-instrumented premise test on real readers remains the open measurement": the devil's §8 and my §5.2 both established there are no per-reader logs, so no *field* ratio can exist yet. The provenance of 0.5599 / 0.4898 is not in any of the five files I was given to verify against. The labeling is honest; the source should be cited in the chapter, not merely asserted.

### Note B — §6.2 line 21 "the operative quantity … exists as a *fixture-conditional* result"

Correct, and it is the honest residue. No issue.

## Sentences I would rewrite

1. **Line 15** → replace "cross-strata transfer, Rival A's clause" with "cross-condition transfer (run under my name; it was cross-condition, not cross-strata)"; replace "r = 0.967, R²_LOO = 0.943, 4.5× better than chance" with "segment-local r = 0.829, R²_LOO = 0.729; the class-conditional mean beats it (MAE 0.0153 vs 0.0206)"; and delete or inline-flag "cannot produce a numeric drift prediction at all".

2. **Line 13** → append: "— a margin reproduced by first-order + median subtraction (§6.2, below), so the kill margin is a preprocessing step the baseline was defined to lack."

3. **Line 39** → change "not a reindex" to "not an identity (i.e., not a reindex only because the winning normalization was withheld from the baseline)."

4. **Line 35** → "beat it on switch localization (r 0.816 vs 0.435) and detection (0.800 vs 0.467, at a cost of 0.25 control alarms vs 0.0)."

---

*Committee Rival A, fifth dispatch, 2026-08-19. Verdict: DOWNGRADE COMPLETE, with four residual inline-edit gaps (lines 13, 15, 39, 35) that should be closed but do not resurrect the old claim. The mean-shift delta is what the chapter now actually says; the "second-order reading" it was seeded to carry is dead in every operative sentence.*
