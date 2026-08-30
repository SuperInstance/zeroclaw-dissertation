# DIGEST — Wave-4 S2 Committee Round — 2026-08-29 (late)

**Lane:** eco-zeroclaw worker tick · **Models:** GLM-5.3 ×3 (RIVAL / DEVIL'S ADVOCATE / METHODOLOGIST), isolated subagents · **Prompts:** `research/PROMPT-PACK-S2.md` (executed verbatim) · **Target:** `elephant/docs/wave4-registration-draft-2026-08-22.md` + fiber v4 code + the v4 S1 kill.

**Gate action per protocol §4:** RIVAL vulnerabilities → merged into freeze clauses below; DEVIL verdict = **FREEZE-WITH-CLAUSE**; METHODOLOGIST freeze text drafted (filed verbatim as `METHODOLOGIST-S2-FREEZE-DRAFT.md`, mirrored from `elephant/docs/wave4-S2-freeze-DRAFT-2026-08-29.md`). S3 generation stays blocked.

## 1. RIVAL — three vulnerabilities, three killer subgates

- **V1 (mid-α amplitude confound):** `room_c` has constant norm; `‖dev_R‖` varies per reader; the α(1−α)·⟨dev,room⟩ cross term peaks exactly where the gradient clause measures. → **Norm-purity subgate in the Design gate:** S1 sweep must show target-norm flat in α (unsealed telemetry); non-flat kills the gradient clause by the draft's own §1.5 logic.
- **V2 (parity v2 is a tautology):** logging `target_R(t)` per speak makes replay an arithmetic identity — it tests only "the log wasn't garbled." → **Two kill conditions on parity v2:** (a) independent seeded-stream re-derivation of `w_ar`/`room_c` matching the logged target bit-for-bit; (b) bit-identity assertion `v4(α=0) ≡ v3` on a pinned corpus.
- **V3 (κ(t)-gated wobble laundering — the sharpest):** `tan_sd = WOBBLE_LEVEL·√(KAPPA_COLD/κ(t))` content-modulates the carrier's rotation rate; the P_trans headline can fire on the room's content clock, not room-carried offset; the A-only purity guard is blind to it. → **κ-neutrality subgate:** α=1 pilot with κ(t) frozen constant must still fire P_trans < 0.5×P_rest, else content-leak ⇒ VOID. **ICC calibration clause:** S1 ICC threshold calibrated against a v3-style static-common-target control (mechanical-dispersion-compression control).

## 2. DEVIL'S ADVOCATE — verdict FREEZE-WITH-CLAUSE

The rigging charge (α moved into the detector's field of view) is substantially rebutted — the S1 kill was honored and filed same-day, the designed-in rigging didn't even work (P never fired), and the design hygiene (matched pairs, amplitude matching, carrier-purity guard, version-pinned legacy fiber, blinded S4) is real. **What nothing rebuts:** wave-4 is calibration on a known-source phantom, unbounded retries are structurally tempting, and P sat in the design loop. Three binding clauses for any wave-4b freeze:

1. **Phantom-scope clause:** wave-4/4b numbers are instrument-calibration claims only; no field claims about real rooms, ever.
2. **Retry-limit clause:** at most one further design iteration (4b); if it fails the gate, P is declared structurally unreadable for this engine and the instrument-vs-collapse program closes.
3. **Detector-independence clause:** leg statistics consulted during design (P, at minimum) are labeled "designed-for," demoted from headline; the headline of any passing registration must be a leg untouched by the iteration (ICC decline or the V anchor leg), threshold re-derived fresh.

## 3. METHODOLOGIST — S2 freeze text drafted (fiber v4b)

Filed: `METHODOLOGIST-S2-FREEZE-DRAFT.md`. Key elements: (a) direction-only amplitude-matched carrier frozen, plus v4b **scale floor** (carrier sd ≥ 0.29·corpus_sd, G6-derived, ×2 margin) and **decorrelation ceiling** (ρ_w ≤ 0.2 at transition spacing; AR_PHI 0.9→0.5), with roster-mean-centering survival rule and re-kill condition; (b) full branch×leg matrix with frozen verdict pre-statement (S4 = adjudication, not invention); (c) VOID rules: 7 carried from wave-3 + 3 new (carrier-purity A-leak envelope 0.085; wobble-spec violation from logged targets; power-certificate lapse voids the wave); (d) power: n=16 corpora, 9 family-level paired differences per leg, MDE ≈ 1.03σ_d, ICC-decline case powered ~3.4×; **S3 hard-blocked** behind a 500-replicate simulation certificate (≥0.90 power at Δα=1, ≥0.80 at Δα=0.25, ≤0.05 FP, ≤0.01 leak, ≥0.95 V separation), unwaivable. Priors filed up front (endpoint recovery P≈0.55, humbled by the v4 kill).

## 4. Reconciliation — what the freeze draft must absorb before S2 lock

The methodologist drafted before the RIVAL/DEVIL results were in the room. **Merge checklist (blocking items):**

- [ ] Add RIVAL V1 norm-purity subgate to the Design gate (§ freeze draft).
- [ ] Add RIVAL V2 parity kill conditions (a)/(b) to the parity re-registration clause.
- [ ] Add RIVAL V3 κ-neutrality subgate + static-common-target ICC calibration to the VOID set.
- [ ] Add DEVIL clauses 1–3 (phantom-scope, retry-limit, detector-independence) as binding freeze text.
- [ ] Methodologist's wobble-spec-violation VOID rule already anticipates V3's laundering channel — confirm the logged-target check covers the κ(t)-gating dynamics, not just amplitude.
- [ ] Re-run the committee's sign-off line ("Power certified. Void rules locked. S2 freeze approved.") only after the merge checklist is green.
- [ ] (DEVIL nudge, 2026-08-30) Re-derive the S3-GOVERNANCE-PRIMER dependency table against the merged freeze text BEFORE the freeze commit; update its `Re-derived against:` provenance line. Canonical = freeze draft; primer = derived pointer, never authority.

## 5. What this round does NOT do

No elephant file was frozen, registered, or committed by this lane (the methodologist's file is a DRAFT in elephant/docs, awaiting elephant-lane ownership). No corpus generated. Wave-3's falsified verdict and provenance stand untouched. The dissertation-side conjecture register (ZC-C1/C2/C3) is unaffected — this round is wave-4 machinery, which feeds H-α-FIBER, not the premise branches.
