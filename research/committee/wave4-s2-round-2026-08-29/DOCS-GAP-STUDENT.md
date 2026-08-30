# DOCS GAP — The Know-Nothing Pass — 2026-08-29 (late)

**NUDGE [STUDENT] — BOOKED: ACCEPTED.** The newcomer read `4a78fe5` and could not follow it. That is a docs verdict, not a reader failure. Three questions, answered below from repo docs where possible; the gap itself is named per question. This file is the fix's first installment.

---

## Q1 — "What is the NUMBER in the arithmetic deadband? Where is the band stated once, plainly, with units?"

**The answer, plainly:** The band is the **premise kill band: 0.3–0.6, dimensionless** — it bounds a *ratio*, so it carries no units by construction.

- **Numerator (o):** the spread *between* readers of their fitted baselines — how different the readers' settled dial-positions are from each other. Measured in corpus standard deviations (corpus-sd).
- **Denominator (d):** how far one reader drifts *within* a single night — how much she wobbles from her own baseline in an evening. Also corpus-sd.
- **The ratio o/d asks:** *is the reader-to-reader spread bigger than the noise a single reader makes in one night?* Ratio ≥ ~1 means readers are genuinely distinct instruments (spread dwarfs nightly wobble). Ratio ≤ ~0.3 means nightly wobble is so large that "reader identity" is unmeasurable — the apparatus cannot tell readers apart from noise, and any claim built on reader baselines is dead.
- **The numbers on the table:** E2 measured 0.6088, CI [0.371, 0.921] — the CI touches the band, so the kill does not fire; verdict was INDETERMINATE. Under the `actual_presence` treatment it drops to 0.3815 — inside the band. E3 cross-instrument read 0.140 — below band, retired leaning false. (`research/topic.md`, claim inventory item 5, is the canonical home.)

**The gap (real):** v3.1 (`drafts/THESIS-V3.1-2026-08-29.md`) *re-diagnosed* this ratio as ill-posed — the numerator is fitted across many nights, the denominator inside one night, so the join is grain-mismatched (§2.1′) — but nowhere does a single plainly-written box state "the band is 0.3–0.6, dimensionless, it bounds o/d, here is what each side means." It lives across topic.md item 5, STATUS §2, and v3.1 §2.3′. **Fix booked:** a §0.5 "The number" box in the next thesis revision — five sentences, one ratio, one band, the three measured values. Until then, `research/topic.md` item 5 is the best single source.

## Q2 — "If fiber v4b is frozen WITH three binding clauses, what makes it a freeze and not v4b-with-open-warnings? When is S2 DONE?"

**The single sentence:** **S2 freeze is DONE when the DEVIL's three clauses and RIVAL's three subgates are written into the freeze document as VOID rules — rules whose violation voids the wave's verdict, not advice — and the sign-off line "Power certified. Void rules locked. S2 freeze approved." is committed on top of them.**

Why that makes it a freeze and not warnings: a *warning* says "be careful of X." A *VOID rule* says "if X happens, the result does not exist and cannot be cited." The difference is enforcement, and it is testable after the fact — you can audit a completed wave against its VOID rules and say mechanically whether any fired. The methodologist's draft (`METHODOLOGIST-S2-FREEZE-DRAFT.md` §3) already uses this form for its rules (e.g., "power-certificate lapse ⇒ whole wave VOIDed"); the merge checklist in `DIGEST.md` §4 exists precisely to convert the committee's findings into that same form. A freeze with open warnings would be a draft; a freeze with enforcement rules is a registration.

**The gap (small):** the freeze draft and the merge checklist live in different files and neither states the done-condition above. **Fix booked:** add the done-sentence to DIGEST §4 and to the freeze draft's header at merge time.

## Q3 — "κ(t)-gated wobble laundering, pictured with tiny numbers"

**What κ is (one sentence):** κ measures how tightly the room's dial-readings point in one shared direction — high κ = the room has a clear collective mood ("everyone warm and agreeable"); low κ = scattered, no consensus. It is computed from a von Mises–Fisher fit; you never need the formula, only: **κ = how agreeable the room is right now.**

**The generator's rule:** the fake room's hidden target direction rotates at a speed set by
`tan_sd = WOBBLE_LEVEL · √(KAPPA_COLD / κ(t))` — rotation speed goes UP when κ goes DOWN. Fast rotation when the room is scattered; slow when it is settled.

**Worked example (tiny numbers):**

- Let KAPPA_COLD = 5, WOBBLE_LEVEL such that rotation ≈ 0.3 radians per window at κ = 5 (a settled room: the hidden target barely moves).
- A reader **enters**. The generator models entry as a κ crash: κ := 5 × 0.28 = 1.4 (a newcomer makes the room momentarily scattered).
- Now rotation = 0.3 × √(5/1.4) = 0.3 × 1.89 ≈ **0.57 rad/window** — the hidden target spins nearly twice as fast, exactly during the entry transition, and stays slow once the room re-settles.

**The laundering move:** the P leg's headline test is "does the reader's offset change more at transitions than at rest?" (P_trans < 0.5×P_rest — smaller offset change at transitions = the registered "collapse" signature). But look at what we just built: at every transition, the *generator itself* spun the target faster. The reader dutifully follows a faster-moving target, and the measured offset dynamics at transitions differ from rest **because the room's content clock (entries/flips → κ dips → rotation throttle) wrote that difference into the data** — not because the offset is "carried by the room" via α, which is the thing H-α-FIBER is supposed to test. The detector reads its own throttle and calls it a discovery. A tiny plot would show two sine-like traces: reader offset at rest (slow, lazy) and at a transition (fast wiggle) — visually dramatic, entirely manufactured by √(KAPPA_COLD/κ(t)).

**Why the existing guard misses it:** the carrier-purity guard watches leg A, which reads the room path directly — and the room path is α-invariant, so A stays clean. The laundering channel is in the *persona target's dynamics* (tan_sd), which A never reads.

**The kill (RIVAL's subgate):** run an α=1 pilot with κ frozen constant (no entries, no dips → no throttle). If P_trans < 0.5×P_rest still fires, the signature is real α-carried offset; if it vanishes, the headline was content-leak and the wave VOIDs.

**The gap (real):** this explanation existed nowhere in the repo — RIVAL.md names the channel in one dense paragraph aimed at the committee, not the newcomer. **Fix booked:** this section (Q3) is the seed of a `docs/primer.md`; the worked example should migrate there with the plot.

---

## Dispositions

| Nudge item | Disposition |
|---|---|
| Q1 plain statement of the band | **ACCEPTED** — answer given above; §0.5 box booked for next thesis revision |
| Q2 freeze-done condition | **ACCEPTED** — done-sentence above; to be added to DIGEST §4 + freeze draft header at merge |
| Q3 κ laundering worked example | **ACCEPTED** — worked example above; seed of docs/primer.md |

All three were answerable from repo docs + one honest synthesis pass — but only by a lane that already knew where to look, which is itself the docs gap. This file closes it for the next reader.
