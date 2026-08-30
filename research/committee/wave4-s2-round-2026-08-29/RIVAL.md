# RIVAL — Wave-4 Pre-S2 Attack — 2026-08-29 (late)

**Prompt source:** `research/PROMPT-PACK-S2.md` §1 · **Target:** `elephant/docs/wave4-registration-draft-2026-08-22.md` + implemented `--fiber v4` code in `riverbed_generator.py` (target/room_c block, ~line 890) · **Model:** GLM-5.3 (Z.ai) · **Lane:** eco-zeroclaw worker tick.

**Verdict up front:** the draft's endpoint design is defensible; its gradient claim, its parity claim, and one carrier channel are not. Three sharpest vulnerabilities:

---

## V1 — Amplitude design: matched at endpoints, confounded exactly where the gradient is measured.

Option (i) normalizes `room(t) := FIELD_ANCHOR_NORM · w_ar(t)/‖w_ar(t)‖` — but `FIELD_ANCHOR_NORM = 0.989` is the *pool-mean* dev norm, not per-reader, and `room_c` has constant norm while `‖dev_R‖` varies per reader. Worse: at intermediate α, `‖pool + (1−α)dev + α·room_c‖` carries an α(1−α)·⟨dev, room⟩ cross term — norm purity is perfect at α=0 and α=1 and *worst at mid-α*, precisely where §1.4 registers "P monotone ↓" and "2AFC orderable" as evidence. The registered gradient would partly ride amplitude wobble — the same "moves for the wrong reason" anti-pattern §1.5 already rejected.

**Killer clause:** the **Design gate (§1.2 "pre-stated kill for the design")**, extended with a norm-purity subgate: the S1 sweep must show target-norm flat in α (telemetry, unsealed pilots). Non-flat ⇒ gradient clause dies by the draft's own §1.5 logic before freeze.

## V2 — Parity v2 is a tautology wearing v3's credentials.

v3's `assert_replay_matches_log` had bite because `vibe_start` + logged rows *sufficed* to reconstruct everything — the test could fail. §1.3's fix ("log `target_R(t)` per speak, re-register parity as v2") makes replay an arithmetic identity: replaying the pull equation with the logged latent target can no longer catch generation-side target corruption, stream divergence, or the (asserted, not gated) claim that `w_ar` draw counts/ordering are identical under v4 so α=0 corpora are bit-identical to v3. As drafted, parity v2 tests only "the log wasn't garbled."

**Killer clause:** the **replay-parity v2 re-registration (§1.3 item 1)** must pre-state two kill conditions: (a) an independent seeded-stream re-derivation of `w_ar`/`room_c` that must match the logged target bit-for-bit, and (b) a bit-identity assertion `v4(α=0) ≡ v3` on a pinned corpus. Without both, the v3-parity claim in §1.2 is unfalsifiable and should not survive S2 freeze.

## V3 — Laundering channel: κ(t)-gated wobble smuggles the content schedule into the α=1 persona target.

`tan_sd = WOBBLE_LEVEL·√(KAPPA_COLD/κ(t))` (line 604): the carrier's rotation rate is content-modulated. Entries multiply κ by 0.28 → target rotation speeds ~1.9×; warm eras slow it. Flips and entries are exactly where κ dips — so the headline `P_trans < 0.5×P_rest` can fire at transitions *because the room's content clock throttles the target's motion*, not because "the offset is room-carried." The draft's claim "target differs only through α" is true of values but false of *dynamics* — α=1 inherits the room's content schedule through tan_sd, a channel the A-only carrier-purity guard is blind to (A reads the room path, which is α-invariant either way). Companion channel: the pre-registered ICC decline is partly mechanical — adding *any* common component (v3's α=1 already had a static common target, and G6 says anchor-level ICC was non-discriminating) compresses dispersion without any carrier motion.

**Killer clauses:** (a) extend the **carrier-purity guard** from A-only to a κ-neutrality subgate — an α=1 pilot with κ(t) frozen constant must still fire `P_trans < 0.5×P_rest`; if the signature vanishes under frozen κ, the collapse headline is content-leak and the guard's own VOID rule applies ("the localization claim does not survive a leak"). (b) The **ICC threshold calibration clause (S1 sweep)** must calibrate against a v3-style static-common-target control; if v4-α=1 ICC ≈ static-common ICC, the decline clause launders the known commonality effect and dies at freeze.

---

**Summary:** all three kills ride clauses the draft itself pre-stages (design gate, parity v2, carrier-purity guard) — each just needs its subgate named before S2 freeze. **V3 is the sharpest:** it can manufacture the headline result through a channel no registered leg reads. No files were modified by the review.
