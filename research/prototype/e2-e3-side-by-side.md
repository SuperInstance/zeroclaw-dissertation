# E2/E3 Side-by-Side — Two-Instrument Adjudication of the Premise

**Filed: 2026-08-19 (late AKDT).** Status: synthesis of two already-filed field reports — E2 (`prototype/e2-antecedent-test/REPORT-2026-08-19.md`) and E3 (`prototype/fleet-reader-harness/REPORT-2026-08-19.md`) — written against `research/topic.md` v3. This document adds no evidence, runs no new measurement, and performs no estimation. It adjudicates, at the committee's level, what the two registered instruments jointly say about the premise — *readers have idiosyncratic baselines large relative to their drift.* The count of launderings stands at six; none added here.

> **⚠️ ERRATUM (2026-08-20, E5):** the class-residual number cited throughout this document (**0.4366 vs population 0.6088**) is **SUPERSEDED** — an in-place-mutation bug in `e2_instrument.py::spread_seg(class_residual=True)` inflated the filed residual spread. Clean reproduction (`elephant` commit `de228ec`, `scripts/e5_identity_propagation.py`): class-residual ratio **0.1342**, 95% CI [0.0303, 0.1942]; 93–96% of baseline variance is between-archetype (informative cells 0.9436, perm p = 0.0001) — not the ~59% the filed pair implied. **Direction conservative: every E5 conclusion here survives and is strengthened.** All population numbers (0.4556/0.6088), ICC, drift, and sensitivities are unaffected. Affected spots marked §.0, §2 table, §6.6, §8.

## 0. The one-paragraph verdict

**The premise does not survive this round as a claim.** Two registered instruments, two independent elicitation frames — and neither produced a clear. E2 (embedded personas, at power) is **INDETERMINATE**: ratio 0.6088, bootstrap CI [0.371, 0.921], hugging the 0.6 edge of the kill band, kill condition not fired. E3 (13 prompted real model minds, shared stimulus) is **BELOW BAND**: R = 0.140, CI [0.111, 0.163] — a miss, and per its own registered asymmetry, **weak** evidence (the frame compresses spread). The registered decision tree's survival branch (E2 clears ⇒ grade-dependence as boundary condition) did not fire; its kill branch (E2 below band ⇒ premise dies with two instruments) also did not fire as written. The honest sentence is: **retired, leaning false — not proven false.** The "leaning" is carried by E2's treatment sensitivity (under the actual_presence instrument the ratio drops to 0.3815, inside the band, carrying a measured +0.18 conflation floor — the indeterminacy is treatment-structural, not sample-limited) and by the class-conditional decomposition (residual 0.4366 ~~vs population 0.6088 — most of the baseline spread is archetype structure, not class-independent idiosyncrasy~~ **[ERRATUM: corrected class-residual ratio 0.1342 — the archetype-structure conclusion is stronger than filed]**). The "not proven" is carried by the ICC half, which cleared cleanly (0.7714 [0.667, 0.810] — baselines are real, stable, person-specific), and by the numerator half, which is replicated across instruments. The side-by-side's structural discovery: **E2 and E3 agree on the numerator (baseline spread ≈ 0.46–0.56 corpus-sd in three independent measurements) and diverge ~4.6× on the denominator (drift 0.748 vs 3.46).** The crux is therefore not the ratio's magnitude but the baseline's *meaning* — and the single most decisive next experiment is the already-registered slope regression (H-reader≡room): slope ≈ 0 gives the numerator half its strongest pass (baselines are reader-specific instrument constants); slope ≈ 1 explains the failure (baselines are slow warmth — the embedded reader IS the room, and the premise's "idiosyncrasy" was room geometry wearing a reader's name).

## 1. The decision tree as pre-registered

The cross-instrument tree was committed before any E3 elicitation call (E3 registration, commit `ffe07c9`) and states, verbatim (§7.5 kill condition):

> A below-band E3 alone books nothing; if E2 (the antecedent test at power, embedded readers) also lands below band, the premise dies with two independent instruments against it. If E2 clears, this is grade-dependence — the premise holds for embedded readers and fails for prompted ones — booked as a boundary condition.

As committed, the tree has exactly two branches:

- **Branch A — E2 BELOW BAND + E3 BELOW BAND:** premise dies, two independent instruments against it. The strong kill: two frames (embedded, prompted) independently fail.
- **Branch B — E2 CLEARS + E3 BELOW BAND:** grade-dependence; the premise holds for embedded readers and fails for prompted ones; booked as a boundary condition, not a death. The registration's own anticipation that the two frames might not read the same ratio.

What the tree did **not** pre-commit: the propagation of E2's own verdict category *INDETERMINATE*. E2's internal rules always allowed it (CI touching the band ⇒ indeterminate + power analysis), but the cross-instrument tree never said what an E2 shrug does to the adjudication. That gap is filled below, at synthesis time — and the gap itself is logged as a method-chapter data point: the tree was under-specified by one branch, and the discipline caught it at the moment of adjudication rather than pretending Branch C was always there.

## 2. The two instruments, side by side

| | **E2 — Antecedent Test at Power** | **E3 — Fleet-Reader Harness** |
|---|---|---|
| Frame | Embedded personas in a schedule-diversified room simulation (S1–S5 families, six nights, deterministic replay to <1e-9); canonical presence instrument (participation-deconfounded) | 13 prompted real model minds (10 architecture families) reading shared room-windows through one registered prompt frame |
| Readers | 15 (7 frozen personas + 8 seeded field draws; every reader spans ≥2 schedule families; the 6 originals span all 9 nights) | 13/13 passed the D2 validity deadman; the ≥10-readers discipline is met with margin |
| Pre-commitment | Registration + addenda 1–2, all committed before the runs they govern (elephant `d2523e2`) | Registration commit `ffe07c9`, before the first elicitation call |
| **Primary** | **ratio 0.6088 corpus-sd; CI [0.371, 0.921] — touches the 0.3–0.6 band ⇒ INDETERMINATE** | **R = 0.140; CI [0.111, 0.163] — entirely below the 0.3 death line ⇒ BELOW BAND (a miss)** |
| Kill condition | CI upper ≤ 0.6 — **does NOT fire** (upper 0.921) | Entirely below the death line — **fires** |
| Numerator (baseline spread) | 0.4556 (between-reader spread of fitted baselines) | 0.486 [0.379, 0.552] (segment-local, distinct-stimulus weighted) |
| Denominator (drift) | 0.7483 (mean within-reader drift; no-flip null 0.2906 — signal 2.6× null) | 3.46 [3.09, 3.85] (per-reader range 2.02–4.71) |
| Stability half | ICC 0.7714 [0.667, 0.810] — entirely above the 0.265 floor | Retest noise 0.50–2.24 z; D3 deadman NOT fired (drift exceeds retest noise for every reader) |
| Class structure | Class-residual ratio ~~0.4366~~ **[ERRATUM: clean 0.1342, 2026-08-20]** vs population 0.6088 — most spread is archetype structure | Decomposition: room_reading-only 0.085; displacement-only 0.183 — both far below band |
| Live frame artifacts | Participation conflation (fixed by canonical presence; measured +0.18 floor on the actual-presence instrument); planting ceilings (fixed by directional gains) | Prompt anchoring — paraphrase sweep: 7/13 readers destabilize at P1–P3; the mechanism is confirmed live for half the fleet |
| Asymmetry | Canonical presence is the premise-*favorable* reading (§5) | Registered: a miss is WEAK evidence; a frame artifact cannot be excluded |
| Registered role | The powered antecedent test — the tree's hinge | The independent cross-model estimate — books nothing alone |

## 3. What the side-by-side actually shows: numerator agreement, denominator divergence

The registered tree treated E2 and E3 as two independent readings of one ratio. The field data say something more specific, and more interesting.

**Three independent measurements of the numerator agree.** E2's field numerator (between-reader spread of fitted baselines, canonical): 0.4556. E3's numerator: 0.486, CI [0.379, 0.552] — contains 0.4556. E2's pre-measurement embedded estimate, reproduced *exactly* by the continuity check: 0.5599. Three elicitation geometries — embedded persona, prompted fleet, and the earlier embedded corpus — land in a 0.46–0.56 band. The premise's numerator half — *idiosyncratic baseline structure exists at a measurable magnitude* — is replicated, not contested. (E3's report itself flags its numerator as "nearly identical" to E2's pre-measurement 0.56; connecting it to the field numerator 0.4556 is this document's contribution.)

**The denominator is where the instruments part.** E2's within-reader drift: 0.7483 — 2.6× its own no-flip null, so the drift signal is real. E3's within-model drift: 3.46 — a ~4.6× multiple, per-reader range 2.02–4.71. E3's readers all move 2–4.7 sd on the room's regime change while sitting only ~0.5 sd apart in baseline offset: under a shared stimulus, the common response dominates idiosyncrasy roughly 7:1.

This is exactly the divergence Branch B predicted — with the twist that it lives in the denominator, not the numerator. The frames do not disagree about *whether* baselines differ; they disagree about *what the room does to everyone at once*. E3's shared prompt + shared text manufactures a common drift; E2's embedded readers produce displaced, gain-structured fields whose drift is far smaller. So:

- The "two independent instruments" logic held for the numerator and failed for the denominator. The denominator was never going to be instrument-independent — the registration knew this, because grade-dependence *is* that claim.
- But grade-dependence's trigger (Branch B: E2 CLEARS) did not fire. The signature is present in the data (numerator agreement + denominator divergence); the verdict it would license is not.

## 4. Adjudication: which branch fired, and the third branch

- **Branch B (E2 clears ⇒ grade-dependence as boundary condition): did not fire.** E2 is not a clear; its CI touches the band.
- **Branch A (E2 below ⇒ premise dies with two instruments): did not fire as written.** E2 is not below band. The strong sentence — "two independent instruments killed it" — cannot be honestly spoken.
- **Branch C (written now, at synthesis time; post-hoc, gap logged): E2 INDETERMINATE + E3 BELOW ⇒ the premise holds no claim status; verdict "retired, leaning false"; the boundary-condition hypothesis remains live but unestablished.** The tree needed this branch. It is filled post-hoc because the tree under-specified — a pre-commitment gap, now on the record.

**Robustness to the committee's ruling on E2's provenance:** E2's field number exists only under the addendum-2 reading of its own ladder. If the committee rules the strict letter of addendum 1, the E2 field number is withdrawn and the sentence becomes "the field cannot currently measure its own antecedent." Either way, this document's bottom line does not move: no instrument cleared, so no branch of the tree licenses the premise as a claim — and the survival branch requires an E2 clear, which cannot exist under either reading.

## 5. Does E2's treatment-sensitivity rescue anything?

**No — not in the premise's direction.** The treatment sensitivity is the opposite of a rescue:

- Under the actual_presence instrument, the ratio drops to **0.3815 — inside the kill band**. Kill-ward, not clear-ward.
- The number carries the measured +0.18 participation-conflation floor (fixture-measured at planted truth 0). Read with its bias — as the E2 report instructs — the corrected reading sits deeper in the kill zone (≈0.20 by the fixture floor; at minimum, unreadable as a clear).
- The canonical presence instrument — the registered primary, the premise-favorable reading — is the one that produced 0.6088. **The premise gets its best shot under the cleanest instrument and still cannot clear.**

What the treatment sensitivity *does* rescue is precision. It converts "indeterminate" from "we don't know" into "the verdict is treatment-structural": the estimand's definition moves the number across the band, and the direction of movement is known and measured. If actual_presence had been registered canonical, the premise would be a kill. That the premise currently reads "indeterminate" rather than "killed" rests on the registration order — an artifact of the discipline, not of the world. State it plainly: the discipline is what made this visible, and the discipline is what makes it damning.

## 6. Does the premise survive this round?

**No — not as a claim.** The grounds:

1. **R7 retirement (E2's own registration):** a conditional that cannot be activated or killed after a powered attempt is a shrug — and the shrug is now measured. The premise was retired from claim status the moment E2 landed indeterminate.
2. **No instrument cleared.** The tree's only survival branch requires an E2 clear; the powered attempt produced a CI that touches the band.
3. **The independent instrument leans against.** E3 is entirely below the death line — weak evidence against, per its own asymmetry, but against.
4. **The indeterminacy is treatment-structural, not sample-limited.** A defensible treatment (actual_presence, bias-disclosed) lands the premise inside the kill zone; the favorable treatment still cannot clear.
5. **The geometry caps the premise's own best case.** Field-shaped populations cap near ratio 0.5–1.0; the clear regime (>0.6, CI-entirely) sits at the edge of the constructible cone — and the field result (0.6088) landed exactly where addendum 2's B5 geometric prediction said it would. The band quantity is unresolvable at this design point by construction; no feasible N (≈14,533 readers) fixes a boundary-hugging truth.
6. **Most of the spread is class structure, not individual idiosyncrasy.** Class-residual ratio ~~0.4366~~ **[ERRATUM: clean 0.1342, 95% CI [0.0303, 0.1942] — E5, 2026-08-20]** vs population 0.6088: the majority of baseline spread is archetype propagation. The doctrine's fixtures assumed class-independent baselines; the field's spread is substantially class-structural — the identity-propagation null (E5) gets sharper.

**But it is not a clean kill either.** The grounds:

1. **E2's kill condition explicitly did not fire.** CI upper 0.921 > 0.6; the point estimate sits on the clear side of the edge (+0.0088). Branch A's strong sentence is unavailable.
2. **The stability half cleared cleanly.** ICC 0.7714 [0.667, 0.810], entirely above threshold, across schedule families. Reader baselines are real, stable, and person-specific — the premise's closest cousin measured strong.
3. **The numerator half is replicated.** Three independent measurements, 0.46–0.56 corpus-sd. "Idiosyncratic baseline structure exists" is not in doubt; "idiosyncratic baseline structure dominates drift" is what failed.
4. **E3's miss is weak evidence with a confirmed-live artifact.** The paraphrase sweep showed prompt-anchoring destabilizes 7 of 13 readers — the compression mechanism is real, and the registered asymmetry downgrades the below-band reading accordingly.

**Verdict sentence:** *The premise is retired from claim status — leaning false, not proven false. Its numerator half (idiosyncratic baseline structure) is replicated across instruments and stable (ICC 0.7714); its ratio half (baseline spread relative to drift) is frame-dependent — edge-hugging under the embedded frame, below-band under the prompted frame, in-band under a disclosed alternative treatment. Grade-dependence is consistent with the data but unestablished, because its trigger (an E2 clear) did not fire.*

## 7. The single most decisive next experiment

**The slope regression (H-reader≡room) — already registered (advisor, 2026-08-19) and already built on.** Regress each reader's baseline (mean reliable-subspace reading; per-reader; n_nights ≥ 3) on the measured warmth of the rooms they actually visited. Slope ≈ 0 ⇒ alignment (the baseline is a reader-specific instrument constant, carrying information the room does not have). Slope ≈ 1 ⇒ collapse (the baseline is a slow warmth estimate; "trusted reader" = "reader who agrees with the room"; nurse-as-index dissolves into room-warmth retrieval wearing a reader's name).

Why it is the decisive move — and why nothing else on the bench can say this:

1. **The side-by-side's own structure points at it.** The instruments agree on the numerator and diverge on the denominator. The ratio question ("how big is the spread relative to drift?") is now measured, twice, and frame-dependent. The question that remains open is *what the baseline is*. That is precisely what the slope measures — and it is the only registered test that can distinguish "distinct instrument" from "slow-warming room."
2. **It is decisive in both directions.** Slope ≈ 0: the premise's numerator half passes its sharpest possible test — baselines are reader-specific constants, room-independent, and the ICC (0.7714) gains a second, independent pass; the reader-delta object has a referent. Slope ≈ 1: the premise dies *with an explanation* — the "idiosyncrasy" was room geometry all along, the E2/E3 divergence is explained (embedded readers ARE rooms; prompted readers are anchored to the shared text), and the boundary-condition hypothesis converts into a structural finding instead of a shrug.
3. **It is cheap and its data already exist.** E2's v:2 corpus logs per-reader facts (`field_eff_to_reader`, `lens_now`, `reader_known`, `reading_of`, `reader_final`) across six nights and five schedule families; the 6 original readers span all 9 nights (n_nights ≥ 3 satisfied); and the room-warmth side is the dissertation's solid half — the room-field thermometer is the one thing this apparatus measures cleanly. No new corpus, no new ladder, no new fleet.

**Runner-up (registered): the ramp-night drift-geometry redesign (night-H).** It is the only registered path that could change the premise's own band verdict from INDETERMINATE — subtler transitions shrink the denominator and give the premise its best shot. But it is pro-premise by construction, its best case is a boundary-condition booking (Branch B's outcome, which the registration already anticipates), and the geometry warns it will land at the edge of the constructible cone like its predecessor. Run it only if the committee wants the premise's band verdict adjudicated to the last inch; it cannot produce a decisive kill, and its clear is capped.

**Cheap prerequisite (registered): the barkeep-excluded robustness check** (ratio + ICC, barkeep-excluded — the outlier at drift 2.385, n_nights = 2). Run before the slope. It can only change the shade of indeterminate — a 14-reader CI cannot resolve — but it removes a known drag on the point estimate and costs nothing.

**Explicitly not on the table: recruiting 14,533 readers.** The power analysis's honest reading is that no feasible N adjudicates a boundary-hugging truth. The decisive moves are geometric (redesign) or semantic (the slope) — not sample-size.

## 8. What this settles, and what it opens (claim inventory update)

- **The premise: retired, leaning false.** This document's headline. Not a claim, not a clean kill — a measured, treatment-sensitive shrug with an independent weak miss leaning against it.
- **The ICC: paid, and the reader-delta object's best quantitative support.** 0.7714 [0.667, 0.810], clear of the floor, schedule-diversified.
- **The numerator: replicated.** A new sentence is available to the dissertation: "idiosyncratic baseline structure is stable (ICC) and frame-invariant in magnitude (0.46–0.56 corpus-sd across three measurements); its dominance over drift is frame-dependent."
- **Grade-dependence: unestablished but live.** Its evidence (numerator agreement + denominator divergence) is now filed; its trigger (an E2 clear) did not fire. The slope regression decides whether it becomes a structural finding.
- **E5 (identity-propagation null): strengthened.** Class-residual ~~0.4366~~ **[ERRATUM: clean 0.1342, 2026-08-20 — 93–96% of baseline variance between archetypes]** vs population 0.6088 — most spread is archetype structure; the null's sharpest competitor yet.
- **H-reader≡room: promoted in standing, unchanged in status.** The side-by-side makes the slope the crux; the hypothesis remains named and registered, awaiting its deciding test.
- **Method-chapter lesson: the cross-instrument tree under-specified by one branch.** INDETERMINATE was a possible E2 outcome in E2's own rules but was not propagated into the two-instrument tree. Branch C is filled post-hoc and labeled as such. The discipline caught the gap in its own tree at the moment of adjudication — the institutional finding doing exactly what the method chapter says it does.

*The count of launderings stands at six; none added by this document.*

## 9. Provenance and reproduce

- **E2:** `prototype/e2-antecedent-test/REPORT-2026-08-19.md` (elephant repo commit `d2523e2`; registration + addenda 1–2 committed before the runs they govern). Field number valid under the addendum-2 reading; the strict-letter withdrawal does not move this document's verdict (§4).
- **E3:** `prototype/fleet-reader-harness/REPORT-2026-08-19.md` (registration commit `ffe07c9`, pre-elicitation; 695/702 readings; the sweep was re-run clean after the cache-path bug was archived and fixed).
- **Thesis framing:** `research/topic.md` v3.
- **This document:** synthesis only — no new measurement, no new estimation, no new registrations. Reproduce the underlying numbers from the two field reports above; reproduce the adjudication by rereading them.
