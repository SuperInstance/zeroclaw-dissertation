# S3 GOVERNANCE PRIMER — why S3 is hard-blocked, and what would unblock it

**Filed:** 2026-08-30 (worker tick, eco-zeroclaw) · **Booked:** NUDGE [TEACHER], ACCEPTED
**Audience:** a competent outsider — an engineer who will never sit on the committee.
**Sources (only these):** `METHODOLOGIST-S2-FREEZE-DRAFT.md` (this directory), `DIGEST.md` (this directory, §1–§4), `RIVAL.md`, `DEVILS-ADVOCATE.md` (this directory). No elephant-lane or memory files consulted.

---

## The one-paragraph explanation (for the outsider)

S3 is the stage where the program generates its **registered experimental corpus** — 16 synthetic corpora with the α parameter (how much of each reader's target is set by the room rather than by their own static bias) swept from 0 to 1. The wave-4 design as originally landed (fiber v4) was killed at its own pre-registered gate: the collapse signal never fired, and the one thing that *did* move (an inter-reader correlation drop of −0.141) proved the parameter was live but the design couldn't see it where it needed to. Rather than abandon the wave, the methodologist drafted a redesign (fiber v4b: re-specified carrier amplitude floor and decorrelation ceiling) — and, burned by the kill, made S3 conditional on a **500-replicate simulation certificate**: before generating a single registered corpus, the redesigned generator must demonstrate *in simulation, on throwaway seeds* that the statistical test can actually detect the effect it claims to look for (≥90% detection at full contrast, ≥80% at quarter contrast, ≤5% false alarms, ≥95% on the calibration leg). This block is unwaivable by design: the previous wave's failure was exactly a design that was powerful on paper and blind in fact, and the block exists so that no narrative — however plausible — can substitute for a measured power number. A wave whose detection machinery is unproven cannot produce an honest result, so the machinery is proven first, on seeds that don't count, and the certificate (with seeds and code SHA filed) is the key that unlocks generation.

## The dependency table (clause → blocked stage → unblock condition)

Every gate between "here" and "registered corpus exists." Unblock conditions are verbatim-faithful to the sources. If a condition fails, the stated consequence applies — there is no discretion anywhere in the chain.

| # | Clause / rule (source) | What it blocks | Unblock condition | If it fails |
|---|---|---|---|---|
| 1 | **Status clause** (freeze draft, preamble) | Everything downstream of S1v4b | Design gate re-certifies on unsealed v4b pilots AND power certificate passes (§5.4) | No registered corpus, ever, under this registration |
| 2 | **§5.4 Power certificate** (freeze draft) | S3 generation itself | 500-replicate simulation on scratch seeds (20260829-PC): (i) paired-P rejection ≥0.90 at Δα=1, ≥0.80 at Δα=0.25; (ii) FP ≤0.05 on α-identical pairs; (iii) A-gap exceedance ≤0.01; (iv) V separation ≥0.95 at Δα=0.25. Certificate filed as dated doc with seeds + code SHA | Returns design to S1v4b hardening (§1.2c). **May not be waived, narrated around, or downgraded to a caveat.** (VOID rule 10: starting S3 without it voids ALL wave-4 corpora and restarts the wave.) |
| 3 | **RIVAL V1 — norm-purity subgate** (DIGEST §1, merge checklist) | The gradient clause (intermediate-α readings) | S1 sweep shows target-norm flat in α (unsealed telemetry) | Gradient clause killed by the draft's own §1.5 logic |
| 4 | **RIVAL V2 — parity kill conditions (a)/(b)** (DIGEST §1) | The parity re-registration clause | (a) independent seeded-stream re-derivation of `w_ar`/`room_c` matches logged target bit-for-bit; (b) bit-identity assertion `v4(α=0) ≡ v3` on a pinned corpus | Parity claim demoted to "the log wasn't garbled" (tautology), not evidence |
| 5 | **RIVAL V3 — κ-neutrality subgate** (DIGEST §1, sharpest) | The P_trans headline as currently specified | α=1 pilot with κ(t) frozen constant still fires P_trans < 0.5×P_rest | Content-leak ⇒ VOID — the headline fired on the room's content clock, not the carried offset |
| 6 | **ICC calibration clause** (DIGEST §1) | The ICC decline threshold | Threshold calibrated against a v3-style static-common-target control | Threshold is uninterpretable (mechanical-dispersion confound) |
| 7 | **DEVIL clause 1 — phantom-scope** (DIGEST §2) | Any field claim, permanently | Not unblockable — a scope, not a gate | (No wave-4/4b number may ever be cited about real rooms) |
| 8 | **DEVIL clause 2 — retry-limit** (DIGEST §2) | A second redesign | Not unblockable inside this registration — at most one iteration (4b) | If 4b fails the gate: P declared structurally unreadable for this engine; instrument-vs-collapse program closes |
| 9 | **DEVIL clause 3 — detector-independence** (DIGEST §2) | The P-leg headline status | Headline must be a leg untouched by the design iteration (ICC decline or V), threshold re-derived fresh | (If violated, the registration is laundering a designed-for statistic as a discovery) |
| 10 | **VOID rules 8–10** (freeze draft §3) | Individual corpora / the whole wave | 8: A-gap ≤ 0.085 per pair; 9: measured carrier sd ≥ floor and ρ_w ≤ ceiling from logged targets; 10: certificate exists and verifies before S3 | 8 voids the pair's reading; 9 voids the corpus; 10 voids ALL wave-4 corpora |
| 11 | **Merge checklist** (DIGEST §4, 6 items) | S2 lock itself | Items 3–9 above absorbed into the freeze draft text as VOID rules (not warnings); sign-off line re-run: *"Power certified. Void rules locked. S2 freeze approved."* | The freeze draft is a draft, not a freeze — S3 cannot be unblocked by a text that doesn't yet contain its own gates |

## What this table exposes (the honest creak)

Reading the chain end-to-end: **items 3–5 are not yet inside the freeze draft.** They live in `DIGEST.md` as a merge checklist. Until the merge lands (item 11), the answer to "what unblocks S3?" genuinely does require the committee's shared head — the draft's §5.4 covers the power gate, but a reader of the draft alone would not know about the κ-neutrality subgate or the binding DEVIL clauses. That is exactly the gap the TEACHER nudge pointed at, and it has a concrete fix: the merge checklist must go green before the draft is frozen, at which point this table becomes fully self-contained against the freeze text alone.

**Where S3 sits right now:** the methodologist's draft is filed in the dissertation repo as a mirror only; the elephant lane owns the actual freeze commit and ZeroClaw clause review. No certificate has been filed; no v4b pilots have run; the design gate has not re-certified. S3 is blocked at the very first gate in the table, with five more gates behind it.

## Answering the TEACHER's test directly

*"What would have to be true for S3 to unblock?"* — From the paper alone (post-merge): (1) the design gate re-certifies on unsealed v4b pilots, including the norm-purity, parity, and κ-neutrality subgates; (2) the 500-replicate simulation certificate is filed with seeds and code SHA, meeting all four numeric bars; (3) the headline has been re-assigned to an iteration-untouched leg per the detector-independence clause; (4) the merge checklist is green and the sign-off line has been re-run. Nothing else — no judgment call, no narrative — is required or permitted.
