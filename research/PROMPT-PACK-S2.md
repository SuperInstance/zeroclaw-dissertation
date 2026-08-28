# PROMPT-PACK-S2 — Wave-4 Committee Round (Sharpened Executable Prompts)

**Author:** Extracted from STATUS-2026-08-28 (section 4, committee prompts)  
**Purpose:** Multi-model helper round before S2 freeze lock  
**Date:** 2026-08-28  
**Target:** `elephant/docs/wave4-registration-draft-2026-08-22.md`

---

## §1 — RIVAL: Attack the Draft Before It Freezes

**Role:** You are the standing rival. Your job is to attack `elephant/docs/wave4-registration-draft-2026-08-22.md` before it freezes as S2, finding the three sharpest technical vulnerabilities and naming what clause could kill each one.

**Attack Vector 1: Amplitude Design (Unfalsifiability Risk)**

Read the wobble-carrier amplitude specification in the draft. Ask:
- Is there any amplitude that makes H-α-FIBER unfalsifiable either way? (If the wobble is too large, α signal drowns; if too small, wobble becomes decorative noise — find both breakpoints if they exist.)
- Which clause in the draft pins this amplitude to prevent free parameter fitting?
- Check `elephant/scripts/wave4_s1_pilots.py`: verify that the amplitude choice was derived from S1 pilots, not curve-fitted to later results. What would constitute valid S1 provenance vs. post-hoc optimization?

**Verdict:** Name the amplitude vulnerability (if any), state the amplitude value from the draft, cite the pinning clause, and say whether you trust the S1 provenance as written.

---

**Attack Vector 2: Fiber v3-Parity Claim (Byte-Checking vs. Assertion)**

The draft claims: "at α=0 the corpus is identical to wave-3's instrument on every leg."

Read fiber v4 code at commit `5fe5c47` (`elephant/lib/fiber.py` or equivalent):
- Is v3-parity byte-checked in a test suite, or is it asserted in documentation?
- If checked: what test harness verifies it, and does it run on every commit?
- If asserted: how would a reviewer trust it without execution?
- Look for any code path where α=0 could diverge from wave-3 (e.g., initialization order, default parameters, numeric precision, rounding).

**Verdict:** State whether parity is checked (green) or asserted (red). If red, name the test that should exist. If green, cite the test and its pass rate.

---

**Attack Vector 3: Laundering Channels (Detector Blindness Revisited)**

Wave-3's honest negative was "α lives where the legs are blind." Wave-4 moves α to where legs can see. This creates a new risk: which leg could read generator-plumbing (per-t target logging) instead of room behavior?

Inspect the draft for:
- Does any leg consume the target-logging data directly (even indirectly through residuals)?
- Which leg's P-value is most sensitive to per-t target info?
- Can the committee distinguish "leg detects room shift via α" from "leg detects its own target logging"?

For each suspect leg, draft a "kill clause" that would eliminate the laundering channel (e.g., "leg verdict is VOID if it correlates with target-logging timing at >0.5 after residualization").

**Verdict:** Name the three sharpest laundering attacks and the clause that kills each. Rank them by likelihood. If a fourth channel exists, name it.

---

## §2 — DEVIL'S ADVOCATE: The Rigged Exam Frame

**Role:** You are the set-in-his-ways epistemologist. Your job is to argue the *strongest case* that wave-4 is a rigged exam, then state what evidence (if any) rebuts you.

**The Case for Rigging**

Wave-3 discovered: "α lives where the legs are blind." That is a **calibration bound** — the apparatus cannot separate instrument from collapse when α sits in the detector blind spot.

Wave-4's move: re-point α into where the legs *can* see.

The rigging argument runs: **You are fitting the world to the instrument, not the instrument to the world.** You found a parameter that the apparatus cannot detect, so you moved it to a place the apparatus can detect. That is not discovering whether α is real; that is choosing a configuration where detection is possible, then declaring success when detection happens.

Counter-example (to sharpen your thinking): In medical trials, if a biomarker is undetectable at the dosage you tested, you can run a new trial at higher dosage. That is not rigging — it is engineering the system to work. But if you change the dosage only after seeing the data, that is rigging.

**Your task:** Make the strongest epistemological case that wave-4 *is* rigging in the medical-trial sense. Then:

1. **State what evidence in the design (if any) rebuts your case.** Does the draft pre-register the α re-point? Does it pre-register the failure criterion? Are the anti-hypotheses stated *before* generation? Do the sealed corpora prevent post-hoc amplitude fitting?

2. **State what clause would have to be added if nothing rebuts you.** For instance: "S2 freeze must include the anti-hypothesis 'amplitude-matched wobble swamps α signal' as a pre-stated failure mode, with a specific leg P threshold that voids the experiment if the wobble signal is >50% of the α signal."

3. **Final verdict on one line:**
   - [ ] FREEZE-AS-IS (design rebuts rigging frame)
   - [ ] FREEZE-WITH-CLAUSE (need added language to lock in pre-registration)
   - [ ] DO-NOT-FREEZE (rigging vulnerabilities are unfixable)

---

## §3 — METHODOLOGIST: Draft Exact S2 Freeze Text

**Role:** You are the methodologist. Your job is to draft the exact text that locks wave-4 into S2 — the four clauses that make the experiment unfixable and pre-registered.

**Clause A: Wobble-SD Amplitude**

Draft a one-sentence specification:
```
Wobble-SD amplitude: [NUMBER] (chosen from S1 hardening pilots 
at elephant/scripts/wave4_s1_pilots.py; rationale: [describe 
why this amplitude was selected from the pilot data].)
```

Fill in the number, cite the pilot script, and write the one-sentence rationale. Make sure:
- The number can be traced to pilot results, not curve-fitted post-hoc
- The rationale explains why *this* amplitude (not another nearby value)
- A reviewer can re-run the pilot script and verify the choice

---

**Clause B: Branch×Leg Matrix with Pre-Stated Verdicts**

Draft a matrix header and three example rows:

```
| Branch | Leg | Expected Verdict | Success Condition | α-Sensitivity |
|--------|-----|------------------|-------------------|----------------|
| P      | trans | POSITIVE | P_trans < 0.5×P_rest at α=1 | HIGH (α=1 only) |
| [...]  | [...]  | [...]  | [...]  | [...]  |
```

Include:
- All branches (P, S, A, D, V, etc.)
- All legs (trans, rest, ratio, gradient, etc.)
- Which legs are α-sensitive (expected to depend on α ∈ {0, 0.25, 0.5, 0.75, 1})?
- Which legs are expected to be blind (invariant in α)?
- At α=0, is the verdict identical to wave-3's corresponding row? (byte-checked claim)

Extend wave-3's R5 pattern (cite which wave-3 verdicts are carried).

---

**Clause C: VOID Rules (Complete Set)**

List each VOID rule as a one-sentence if-then:

```
**Carried from wave-3:**
- Gate parity: If one branch in a pre/post pair is VOID, both are VOID.
- Null-night rate: If crossing density in null-mode corpora exceeds [WAVE-3 CAP], 
  the entire experiment is VOID.
- Event floor: If any leg counts <20 events, no verdict is declared for that leg.
- Continuity ladder: If any leg's P jumps >±0.10 between consecutive α values, 
  require explicit continuity rationale or VOID that leg.
- Tautology guard: If leg verdicts at α=0 and α=1 are identical, 
  no α-sensitivity claim is made (prevents "α made it visible" when it was always visible).

**New for fiber v4:**
- Wobble laundering: If any leg's verdict aligns with wobble-carrier structure 
  (phase-locked to per-t target logging), that leg is VOID.
- Sealing integrity: If any corpus lid is torn before S4 blinded analysis, 
  all S3-generated corpora from that seed are VOID.
- [Add any new void conditions the committee identified in §2 (DEVIL'S ADVOCATE).]
```

Add new void conditions numbered as committee feedback suggests them.

---

**Clause D: Power Analysis for Matched Pairs**

State:
```
Power certification: Given n=16 sealed corpora (α ∈ {0, .25, .5, .75, 1} 
+ null-mode + five α-only matched pairs), [VERDICT].

[Choose one:]
- n=16 is sufficient to resolve matched α-only pairs within 1–2 orders 
  of room-draw scatter (wave-3 reference: [cite wave-3 scatter stat]).
- n=16 is insufficient; minimum n required is [NUMBER]; 
  S3 generation is blocked until [NUMBER] corpora are sealed and 
  sidecars filed.
```

Justify by:
- Referencing wave-3's variance estimates (room-draw scatter, inter-leg CV)
- Stating the minimum effect size for α-sensitivity (how small can an effect be and still be detected?)
- Confirming that n=16 (or n=[NUMBER]) gives >80% power at that threshold

**Block everything downstream (S3 generation) until power is certified.**

---

## §4 — Execution Protocol

### Who Runs These Prompts?

- **RIVAL:** A model trained to find edge cases and attack-surface vulnerabilities (skeptical orientation)
- **DEVIL'S ADVOCATE:** A model trained on epistemology and research-design philosophy (critical orientation)
- **METHODOLOGIST:** A model trained on experimental design and pre-registration discipline (constructive orientation)

### Output Expectations

Each prompt delivers:
- **RIVAL:** Three vulnerabilities ranked by severity, each with a one-line kill clause
- **DEVIL'S ADVOCATE:** Strongest rigging case + rebuttal evidence + final verdict (FREEZE-AS-IS / WITH-CLAUSE / DO-NOT-FREEZE)
- **METHODOLOGIST:** Four freeze clauses (amplitude, matrix, void rules, power) in pull-request-ready prose

### Gate Actions (Before S2 Lock)

1. Run all three prompts in parallel
2. Integrate RIVAL's vulnerabilities into freeze clauses (new void rules if needed)
3. If DEVIL'S ADVOCATE verdict is DO-NOT-FREEZE: stop, escalate to advisor
4. If verdict is FREEZE-WITH-CLAUSE: merge DEVIL'S ADVOCATE's requested clause into METHODOLOGIST's text
5. If verdict is FREEZE-AS-IS: approve METHODOLOGIST's draft as-is
6. Committee signs off: "Power certified. Void rules locked. S2 freeze approved."
7. **S2 LOCK** → S3 sealed generation begins immediately

---

## §5 — Honest-Negative Frame (Embedded in All Prompts)

**Pre-stated failure criterion (shared by all three prompts):**

If matched α-only pairs are inseparable within 1–2 orders of room-draw scatter on every leg, then:
- H-α-FIBER dies (hypothesis rejected)
- Wave-3's honest negative becomes a **detection-envelope bound** (a methodological finding, not a null result)
- The result is filed as: "Wave-3 and Wave-4 together establish a calibration limit on the apparatus when α is the parameter of interest; this limit is a property of the matched-pair design and holds for this class of instruments"

This frame is **not optional** — it must appear in the S2 freeze text so that failure is a publishable outcome, not a dead end.
