# S2 Freeze Preparedness Checklist — Wave-4 Committee Gate

**Author:** Extracted from STATUS-2026-08-28 (section 4, advisory sweep)  
**Gate:** Wave-4 S2 freeze (before registered corpus generation begins)  
**Date:** 2026-08-28

---

## What Must Be True Before S2 Freeze

### Machinery State
- [ ] Fiber v4 is landed on elephant main (`5fe5c47`): α re-pointed into fiber's within-night target trajectory
- [ ] Wobble carrier is amplitude-matched; per-t target logging is active
- [ ] 16 sealed corpora from `riverbed_generator` on fiber v4 exist with α ∈ {0, .25, .5, .75, 1} + null-mode + five α-only matched pairs
- [ ] Sealed sidecars and decoys are filed S3-side, calibration curve registered pre-S4
- [ ] `elephant/docs/wave4-registration-draft-2026-08-22.md` is complete and circulated

### Hypothesis Clarity
- [ ] H-α-FIBER is stated: α-re-pointing makes registered legs α-sensitive; at α=1 the registered collapse signature (P_trans < 0.5×P_rest) becomes reachable for the first time
- [ ] Anti-hypotheses are pre-stated in writing:
  - (i) amplitude-matched wobble swamps α signal → all legs blind again, detection envelope extends
  - (ii) legs see wobble, not α → laundering channel committee must attack

### Honest-Negative Doctrine
- [ ] Wave-3 honest negative is recorded: "α lives where the legs are blind" (apparatus cannot separate instrument from collapse because α was positioned in detector blind spot)
- [ ] Wave-4 moves α to where legs can see — this is disclosed as a *design change from wave-3*, not a new finding
- [ ] Frame for wave-4 failure is prepared: if matched α-only pairs inseparable within 1–2 orders of room-draw scatter on every leg, then H-α-FIBER dies and honest negative files as a **detection-envelope bound** (wave-3's negative becomes a series, a methodological finding)

### Kill-Band (0.3–0.6) Doctrine — Materialized Rules
- [ ] Reader-delta premise was DOWNGRADED to baseline-relative delta; E2 ratio 0.6088 [0.371, 0.921] touches kill band (treatment-sensitive: drops to 0.3815 with `actual_presence`)
- [ ] **Rule:** any premise-side ratio quoted in wave-4 carries dual-R4 annotation; if a ratio sits in 0.3–0.6 band, the kill condition is disclosed alongside the measurement, not buried in methods
- [ ] **Enforcement:** wave-3's kill-band threshold (do not declare if ≤0.3 or ≥0.6 uncertainty straddles band) remains active for wave-4
- [ ] All verdicts subject to kill-band re-check before S2 freeze

---

## What the α-in-the-Fiber Registration Draft Must Contain

### Clause 1: Amplitude Specification (CRITICAL OPEN DECISION)
**Frozen value required.**
- The wobble-sd amplitude for the carrier must be pinned to a single number before S3 generation begins
- Provenance: S1 hardening pilots at `elephant/scripts/wave4_s1_pilots.py` (executed, sidecars present)
- Rationale: attack surface is whether any amplitude makes H-α-FIBER unfalsifiable in either direction
- Committee gate: **RIVAL prompt specifically audits this** (section §4.1 below)

### Clause 2: Branch×Leg Matrix with Pre-Stated Verdicts
**Extends wave-3's R5 pattern.**
- Explicit matrix: each branch × leg cell gets a pre-stated success condition (e.g., "P_trans < 0.5×P_rest", "κ gradient monotone in α")
- α-sensitivity marking: which legs are α-sensitive? which are expected blind? (carry wave-3's null-night analysis into wave-4)
- Fiber v3-parity claim: at α=0 the corpus is identical to wave-3's instrument on every leg (byte-checked, not asserted)
- Committee gate: **METHODOLOGIST prompt drafts exact text** (section §4.3 below)

### Clause 3: VOID Rules (Carry-Forward + New)
**Necessary conditions that, if violated, void the experiment.**

**Carried from wave-3:**
- Gate parity: no pre/post pair can survive if one branch is VOID
- Null-night rate: crossing density in null-mode corpora must stay below wave-3's cap
- Event floor: ≥20 counted events per leg (no branch declared if <20)
- Continuity ladder: ±0.10 band guards against discontinuity-jumping (if a leg's P crosses ±0.10 between legs, require continuity rationale)
- Tautology guard: never claim α makes a leg visible if the leg's verdicts at α=0 and α=1 are identical

**New for fiber v4:**
- [ ] Wobble laundering: any leg's verdict that aligns with wobble-carrier structure (phase-locked to per-t target logging) is VOID
- [ ] Sealing integrity: if any corpus lid is torn before S4 blinded analysis, all S3-generated corpora from that seed are VOID
- [ ] (Methodologist drafts additional void conditions in committee round)

### Clause 4: Success & Failure Criteria (Pre-Stated)
**Success (any of):**
- P_trans (or a pre-named leg) separates α=0 vs α=1 endpoints under frozen threshold (0.80/0.60/0.80, ε=1e-2)
- Gradient clause fires monotonically in α across the registered leg set

**Failure (pre-stated):**
- Matched α-only pairs inseparable within 1–2 orders of room-draw scatter on every leg
- If failure: H-α-FIBER dies, honest negative files as a detection-envelope bound (wave-3 becomes a *series* of negatives, a methodological contribution)

---

## Committee Round Attack Surface (What Committee Must Certify)

### 1. Amplitude Design — Unfalsifiability Risk
**RIVAL prompt audits:**
- Is there any amplitude that makes H-α-FIBER unfalsifiable either way?
- Which clause pins the amplitude choice?
- Can the committee verify S1-pilot provenance?

**Gate passes if:** amplitude is pinned to a registrable number with auditable S1 provenance, and no amplitude vulnerability is found.

### 2. Fiber v3-Parity Claim — Byte-Checking vs. Assertion
**RIVAL prompt verifies:**
- Fiber v4 code (5fe5c47): is v3-parity byte-checked or asserted?
- At α=0, is the output byte-identical to wave-3 instrument on every leg?

**Gate passes if:** parity is checked in test suite, not assumed.

### 3. Laundering Channels — Detector Blindness Revisited
**RIVAL and DEVIL'S ADVOCATE jointly audit:**
- Which leg could read generator-plumbing (per-t target logging) rather than room behavior?
- Name the three sharpest laundering attacks and what clause kills each
- Is the committee gate clause sufficient to prevent it?

**Gate passes if:** three laundering channels are named, each has a kill clause, and no fourth channel exists.

### 4. Epistemological Framing — Is Wave-4 a Rigged Exam?
**DEVIL'S ADVOCATE makes the strongest case that wave-4 is fitting the world to the instrument:**
- Wave-3 said: "α lives where the legs are blind"
- Wave-4 says: "move α to where the legs can see"
- Argument: this is re-positioning the parameter into the detector's field of view, not the instrument to the world

**Gate passes if:** the design has countermeasures to the rigging claim, or the freeze text explicitly flags the design trade-off.

---

## Methodologist's S2 Freeze Text Template

**What the freeze must specify (four sections):**

1. **Wobble-SD Amplitude Clause**
   - One frozen number (e.g., wobble_sd = 0.XX)
   - Provenance from `elephant/scripts/wave4_s1_pilots.py`
   - Rationale: "chosen to [reason from pilots]"

2. **Branch×Leg Matrix with Verdicts**
   - Rows: branches (P, S, A, D, V, …)
   - Columns: legs (trans, rest, ratio, gradient, etc.)
   - Each cell: pre-stated verdict condition
   - Carry wave-3's R5 pattern and α-sensitivity mapping

3. **VOID Rules**
   - Wave-3 carry-forward (gate parity, null-night rate, ≥20-event floor, continuity ladder, tautology guard)
   - Wobble-laundering guard
   - Sealing integrity
   - (Committee adds any new void conditions)

4. **Power Analysis for Matched Pairs**
   - Given n=16 sealed corpora, is this enough for α-only matched pairs?
   - If not, state minimum n required
   - **Block everything downstream until power is certified**

---

## Void Rules Reference — Kill-Band Doctrine

**Kill-band 0.3–0.6 is a measurement-quality filter, not a threshold.**

**Applied to premise-side ratios:**
- E2 reader-delta baseline ratio: 0.6088 [0.371, 0.921] — **touches kill band**, disclosed with dual-R4 annotation
- E3 R=0.140 — **below band** (dropped from disclosure as premise-side verdict)
- When a ratio's CI straddles 0.3–0.6, the measurement is deemed unreliable in that range; do not declare a branch verdict until the ratio is pushed outside the band (by design iteration or higher n) or the kill condition is disclosed alongside the measurement

**Applied to wave-4:**
- Any premise-side ratio in the corpus must carry kill-band annotation
- If a ratio sits in 0.3–0.6 band after committee amends the draft, the VOID rule activates: either the ratio is removed from the verdict, or the kill condition is disclosed in the S2 freeze text itself

---

## Sign-Off Gate (Committee Actions Before S2 Lock)

- [ ] RIVAL prompt executed: amplitude, parity, laundering channels audited
- [ ] DEVIL'S ADVOCATE prompt executed: rigging-exam frame addressed, epistemological trade-offs disclosed
- [ ] METHODOLOGIST prompt executed: S2 freeze text drafted (amplitude, matrix, void rules, power certified)
- [ ] Kill-band audit: every premise-side ratio checked for 0.3–0.6 straddling
- [ ] Honest-negative frame: failure criterion (detection-envelope bound) is written into freeze as explicit outcome
- [ ] Draft amended by committee feedback
- [ ] **S2 FREEZE LOCKED** → S3 sealed generation begins
