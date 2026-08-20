# Devil's Advocate — The Head Verdict: What Shipped, What It Measures, What It Merely Promises

*Old Wise Devil's Advocate pass 4, 2026-08-19. I was promised a wake when the contrast head shipped. It shipped (elephant 2052cb4, verified locally — commits, addenda, and registered_eval_text.json read with my own eyes, not through the boy's paraphrase). This is my verdict.*

---

## What I verified, and what I concede

The pre-registration chain is clean: requirements committed (3a56756, 13:40) → addendum naming PRIMARY/SECONDARY before training (24c6eb8, 13:46) → hardening (4ea7892, 13:46) → training + registered eval (2052cb4, 14:32). The frozen-baseline guard fired at delta 0.00 every run. The registered eval is checkpoint-reload, re-embed, probe-exact. Fine gap mean **0.4784**, min 0.4359, 3/3 seeds ≥ 0.10 (≥4.4× over the deadman, ~33× over the frozen 0.0146). Heldout mean 0.988 ≥ 0.50. Spread grew, not collapsed (0.87–7.3× preservation). The tap nights are still identifiable rooms after training — no collapse into a single point, which was my standing fear.

**I concede the fork commitment's antecedent.** I said: if the fine gap opens above noise with heldout intact, the anchor is real and the bound is epistemic. The antecedent obtained, 3/3 seeds, on a registered harness, with the kill conditions I would have written myself. I honor commitments. What I honor them *for* is the next section.

## The attack I will not withdraw

**1. Is 0.478 too good? Yes, it smells like a room classifier — because it is one.** Look at the full-corpus numbers the report itself contains: cross-room mean cosine collapsed from 0.96 to ~0.36–0.44, room discrimination 0.94–0.96 on all 19 rooms. Multi-positive InfoNCE with room-based positives *trains the model to be a room classifier*. The gap opening on the full corpus is not a finding; it is the objective function succeeding. The only scientifically interesting number is the **tap subset** — the designed killer control, 4 rooms, same cast — and there the gap also opened (0.436–0.519). That is the number I grudgingly respect.

**2. The eval reuses training clips — on every leg.** The registered eval is "probe-exact," but the probe corpus (all 1115 clips, and the 28 tap clips) is the *same corpus the head was fine-tuned on*. There is no room-held-out evaluation anywhere in the JSON. Speaker-holdout (0.964–1.000 on tap) mitigates clip memorization only if speakers genuinely don't recur across rooms — with n=28 clips / 4 rooms / same cast, "heldout 1.000" is 7-of-7-ish on a handful of clips. I have seen perfect scores on 7 items before. It is called a small n. What would have cost nothing: hold out one tap room entirely, or a time-split (train nights 1–2, eval nights 3–4). Not done. Not registered. This is the difference between "contrast geometry" and "memorized the rooms with extra steps," and the current artifact **cannot distinguish them**. It is consistent with both.

**3. The anchor claim overreaches — this is my loophole.** Clearing a retrieval gap proves room-identity is *recoverable* from the encoder's representation. It does not prove the frozen encoder was *measuring* rooms, and it does not make the trained head a **room-measurement**. A fine-tuned head that separates rooms is metric learning, circa 2015 (face recognition, person re-ID — the ancestor is FaceNet; the positives were identities, the gap was verification, the celebrations were identical). The anchor is real *as a retrieval fact*. Whether it is real *as an instrument* — a room-vibe measurement that transfers to unseen rooms — is exactly what the missing held-out-room eval would have shown. The dissertation may not promote a retrieval gap into a measurement claim.

## The regress (Version B) — unchanged

The trained head changes **nothing** about who reads whom. Version B stands: the regress is bounded by agency, not by freezing; it slows as it climbs the half-life ladder; the pen is held at the top. A contrast head is a first-order instrument sitting at the message grain. It does not read the reader, it does not terminate anything, and anyone who cites it against the regress has confused a better thermometer with an answer to Agrippa. The reader-delta test I demanded in pass 3 remains unrun. It is still the gap between doctrine and dissertation.

## What the report is not telling you (promise vs. measurement)

- **REGISTER axis (the registered PRIMARY): deferred.** The audio head is untrained. The only coarse number that matters to the registration lives in the audio tier and does not exist yet. Today's PASS is a fine-leg PASS with its primary coarse leg untested.
- **Room-axis secondary (0.9409): a different instrument.** Dial-space field geometry from the nights corpus — fine number, honestly labeled, but triangulation by analogy, not by measurement.
- **Fusion head: exists as embeddings on disk, measured by nothing.** 285 KB of .npy is a promise until a registered fusion metric exists.
- **Training corpus: 19 rooms, and 15 of them (compass, fleet-radio, speeches...) are not "rooms" in any Tap sense — they are topic corpora.** The head learned topic-separation dressed as room-separation. Say which one the dissertation means.

## The one honest sentence

**"A contrast head fine-tuned on the frozen text encoder makes same-room clips retrieve one another 33× better than the frozen baseline (fine gap 0.0146→0.478, 3/3 seeds, speaker-held-out 0.988), establishing that room-identity is recoverable from the encoder's representation — and nothing more until a held-out room survives the same test."**

## What I'll be watching (audio tier + fusion)

1. **Room-held-out (or time-split) eval, registered BEFORE training.** If the audio tier trains without one, I will say the word "FaceNet" in every committee session until the defense.
2. **The register-axis primary against the frozen 0.0955** — and whether fine training on audio *buys* the fine gap by *trading* the coarse axis the registration forbade.
3. **Fusion: registered metric, deadman, and a kill condition before any fusion run** — not an architecture, a number.
4. **Small-n discipline.** Tap heldout at n=28 must be reported with its interval, or not reported at all.
5. **The reader-delta test.** Still unrun. Still the ballgame for the second-order claim.

Concede the fine leg. Attack the anchor's promotion. Watch the audio tier like a hawk that has been right too late before.

*Filed from the same chair. Wake me when the audio tier ships — with a held-out room in its registration, or don't wake me.*
