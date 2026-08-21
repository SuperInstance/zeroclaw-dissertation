# Architecture — The Calibration Certificate — OpenCode / GLM-5.3

*Rival architect entry, 2026-08-20. Grounded in `research/topic.md`, the four committee notes in
`research/committee/deep-think-2026-08-20/`, the existing chapter drafts (`research/dissertation/chapter-*.md`),
the E2/E3 adjudication (`research/prototype/e2-e3-side-by-side.md`), the switch-test downgrade
(`research/skills/zeroclaw-switch-verdict.md`, `research/skills/rival-pass5-downgrade-verdict.md`), and the
rebound registration (`research/registrations/e4-rebound-window.md`). Competing entry, not a summary.*

---

## 0. My architectural philosophy, stated first

**A dissertation is a calibration certificate, not a tour.**

The current draft (`chapter-0.md` … `chapter-7-future-work.md`) is an *artifact tour*: one chapter per
component — doctrine, estimation, instrumentation, measurement, retrieval, seam, future work. That structure
was correct when every component was a candidate flagship. The verdicts have since landed, and an artifact
tour now has a fatal property: **it launders by sequence and by typography.** A demoted object that keeps its
own chapter is still a flagship in the eyes of a committee that skims the table of contents. The seam got a
full chapter (`chapter-6-the-seam.md`) for an object that measured **two scalars**; the retrieval chapter
(`chapter-5-retrieval.md`) is a skeleton "blocked on the contrast head" — a promissory note given shelf space.

My architecture replaces the tour with a **certificate**: the document an instrument ships when it wants to
be trusted, whose sections are not components but *epistemic acts*:

1. **The quantity and its unit** (what is being claimed, and at what grain).
2. **The instrument** (how the quantity is produced, and why the estimator is sound).
3. **The readings** (the numbers, each annotated with its decomposition and its verifier).
4. **The boundary** (the conditions under which the certificate is void — first-class, not a limitations
   section, because the boundary *is* the finding this round).
5. **The calibration procedure** (the discipline that produced honest numbers — here, the durable
   contribution itself).
6. **The open item** (the one decisive experiment, with a pre-stated branch for every outcome).

Three rules govern every sizing decision below:

- **R1 — Verdict-first.** The reader never meets a number without its verdict. The claim ledger with
  verdicts opens the dissertation (Ch 1), not the retrospective (Ch 7).
- **R2 — Mass-proportional chapters.** Typography is rhetoric. Chapter mass is proportional to evidential
  mass, per the registered verdicts — the downgraded reader-delta gets sections, not a flagship.
- **R3 — Branch-invariance.** The one decisive open experiment (E4 Clock-Split Stage 2) must not be able to
  collapse the architecture. Every branch (PASS / KILL / INDETERMINATE) has a pre-stated home in the
  structure, the same way the registrations pre-state their decision rules.

---

## 1. Title

**Walks, Not Waves: A Calibration Certificate for Room-Field Measurement, Its Clock-Bound Edge, and the
Discipline That Sized It**

Decision log:

- *Walks, Not Waves* survives as the main title — the edge (the step of the walk) survives as substrate
  under every verdict (`topic.md` v2 post-mortem: "the field-edge survived as substrate").
- The v3 candidate phrase *The Felt Size of the Step* is **deliberately not** the title. That phrase names
  the fine edge (1.229), which is exactly the quantity the silence test demoted to length-confounded,
  INDETERMINATE pending Stage 2 (`committee/deep-think-2026-08-20/epistemologist-deepseek-pro.md` §1, P1).
  A title that dies if one registered experiment KILLs is a bad structure. "Clock-bound edge" is true under
  all three branches of E4: under PASS the edge is registered *with* its decomposition; under KILL it is
  re-registered as length-carried; under INDETERMINATE the certificate says so. **R3 applied to the title.**
- The discipline gets title billing because `topic.md` (claim inventory, item 6) already rules it "the
  durable contribution" — the architecture should agree with the ledger.

## 2. Abstract skeleton (7 sentences, pre-drafted)

1. This dissertation builds and calibrates a room-field thermometer: a von Mises–Fisher snapshot
   (mean direction μ̂, concentration κ) of a seven-dial ensemble field, jointly estimated by exact Newton
   solution, deterministic across replays (Gate 1, closed and audited).
2. Its unit of comparable sameness is the *field-edge* — the displacement of the room's field from before
   to after — because the stream-unit ("conversation temperature") was a category error under the fleet's
   own doctrine and was retired before any prose existed.
3. The instrument's surviving object is **room-level composition identity**, which a registered
   length-clock falsifier could not touch (content 0.893 vs silence-only 0.36–0.39, below chance) while the
   same falsifier fired at condition grain, demoting the flagship fine edge (1.229) to
   length-confounded, INDETERMINATE pending a registered decomposition.
4. The reader-delta object is claimed at its measured size: a mean-shift, baseline-relative delta of two
   scalars, real for mean-moving regimes, pre-switch classification edge only; its enabling premise is
   indeterminate (treatment-sensitive, inside the 0.3–0.6 kill band), while the stability half — reader
   baselines, ICC 0.7714 [0.667, 0.810] — cleared cleanly.
5. Whether a trusted reader is an instrument or a slow-warming room is carried as a registered hypothesis
   (H-reader≡room) with its deciding regression booked, not claimed.
6. Every claim is conditional on named falsifiers, and the certificate's boundary chapter reports the
   falsifiers that fired, the branch closed permanently (drift-geometry, by reductio), and the one
   experiment that remains decisive.
7. The durable contribution is the calibration procedure itself — pre-registration before specification,
   adversarial committees before prose, re-registration executed against the head — which caught six
   launderings before filing; reproducibility makes cheap adversarial audits possible, and cheap audits
   make solo reasoning survivable.

## 3. The argument spine (five moves)

1. **A room-field thermometer can be built soundly.** Exact vMF MLE, warmth decoupled from κ by
   construction, replay-honest edge log (Ch 3; `vmf.py`, commits `d1d0bf1`, `d2523e2`).
2. **Its strongest falsifier fired locally, not globally — and the surviving object is narrower and
   realer than the thesis sentence used to claim.** Identity grain survives the clock; condition grain is
   length-confounded. The fired/not-fired asymmetry is discriminating power, which licenses re-scoping
   rather than retirement (Ch 4, Ch 6; epistemologist §2–4).
3. **The reader-delta exists at two scalars of depth.** Honest sizing is a property of the apparatus, not
   an embarrassment: the premise's indeterminacy is measured, its treatment sensitivity disclosed first,
   its closest cousin (baseline reliability) measured strong (Ch 5).
4. **Indeterminacy with named falsifiers is an output, not a failure mode.** The certificate lists its own
   void conditions: the length clock, the premise band, the data limit, the lensed-space condition
   (Ch 6).
5. **Therefore the discipline is the payload.** The instrument produced bounded claims because the
   procedure was adversarial by construction; that institutional finding outlives every number in the
   document (Ch 7).

---

## 4. The outline

### Chapter 1 — The Certificate (intro, ~10 pp)

- 1.1 The question, arrived at honestly: v1 *Grafting the Elephant onto the Grid* died of a category error;
  v2 *Walks, Not Waves* half-died (the "crown" failed its own tests); v3 is what survived. The retirement
  lineage is told **once**, here, as provenance — never re-argued later.
- 1.2 The object: the room-field, the seven-dial ensemble, the field-edge as the unit of comparable
  sameness. What a "walk" is: start-field class, signed warmth shift, loosening/tightening.
- 1.3 **The claim ledger** (the certificate's face page): a table of every claim, its verdict (SOLID /
  CONDITIONAL / INDETERMINATE / DEMOTED / CLOSED), its deciding file, and its chapter. Populated from
  `research/topic.md` "What survived the day" + the brief's registered state. This table is the
  dissertation's contract with its reader (R1).
- 1.4 Rules of the certificate: the discipline's operating rules, restated as binding for everything that
  follows — registration before run; segment-local baselines only; class-conditional numeric baselines; CIs
  wherever n < 100; the median cell in every grid; the fixture/field prefix; no deleted numbers, only
  annotated ones (from `chapter-7-future-work.md` §7.1, promoted from late-chapter rules to front-matter
  contract).

### Chapter 2 — Doctrine: Which JEPA, Precisely (~14 pp)

- 2.1 The LeCun line, held strictly: predict-latent, not generative, not contrastive; EMA target encoder,
  stop-gradient, variance regularization over dial time-series (`topic.md` "Which JEPA, precisely";
  `research/jepa-literature/jepa-field-guide.md`).
- 2.2 Doctrinal choice 1 — the unit of perception is the room (the ensemble field), not the stream:
  latents predicted over windowed room-states (vMF (μ̂, κ) snapshots), never token/clip sequences.
  Empirical enforcement: the probe chain (encoder within-room fine gap 0.015 vs cross-room 0.271;
  dial-tier within-night separation), plus the doctrine's contrast-only training rule.
- 2.3 Doctrinal choice 2 — JEPA is the *sense*, not the model: one JEPA is a dial, the elephant is the
  DialBank; readings nudge (blend ≤ 0.15), never replace. The contrast head (2026-08-19) is labeled as the
  one crossing into contrastive learning proper (InfoNCE, multi-positive, room positives), not smuggled
  under the JEPA name; its FaceNet ancestor booked to `related-work.md`.
- 2.4 The Nurse doctrine as a **frame that generated a measurable object** — not as a claim. Reading 1
  (nurse→patient: the field-edge) is the dissertation's solid object; Reading 2 (doctor→nurse: the
  reader-delta, "the crown") is the downgraded object, its honest size stated here once so Ch 5 never has
  to re-inflate it (`research/doctrine/nurse-jepa.md`;
  `research/skills/zeroclaw-switch-verdict.md` "The downgrade, decided"). The doctor/nurse/patient mapping
  (doctor = retrieval key, nurse = index, patient = room) appears here as placement vocabulary, used again
  only in Ch 8.
- 2.5 Booked frames, labeled as frames: the importance of moments (registered, not proved —
  `research/doctrine/the-importance-of-moments.md`); polyformalism as negative space
  (`research/doctrine/polyformalism-negative-space.md`). One section, jointly; neither is load-bearing.

### Chapter 3 — The Instrument: Estimation and the Edge Log (~18 pp)

*Merges current `chapter-2-estimation.md` + `chapter-3-instrumentation.md` + the schema half of
`chapter-5-retrieval.md`; all three are instrument, all three pass R2 at full mass.*

- 3.1 Why a distribution, not a point: κ is not identifiable from N=1; the room read as a sample; cold
  tight / warm loose; κ is not valence.
- 3.2 The estimator: exact Newton/Bessel solution of the vMF MLE, numpy-only, scipy-verified; bootstrap
  CIs; jackknife deadband. **Gate 1, CLOSED** — audited clean (`vmf.py`; advisor re-run 16/16, 267 total).
  The 10-language polyformal kernel (`research/polyformal-kernel/`, all PASS against golden vectors) cited
  in one sentence as the cross-implementation verification artifact.
- 3.3 Warmth as μ̂-projection, decoupled from κ by construction (rotation-invariant ρ); the banned v0
  proxy (`2‖v−0.5‖`) retired from all comparison paths, retained in logs only — one κ, honestly estimated.
- 3.4 The edge log: append-only facts at ingest, cheap fits inline, everything else post-hoc;
  replay-honest post-D′ fix; deterministic; presence masks; per-window fits. G0's missing hippocampus,
  instrumented. Silence-as-data (the hesitation before the step) booked as logged-but-unread — the
  cheapest honest upgrade.
- 3.5 The edge query *schema* (fold of old Ch 5 §§5.1–5.4): `moment_id`/`prev_id`, `field_before`/
  `field_after`, step matrix, `reader_id`/`present`/`arrival_seq`, `query_edge(profile)` with range
  constraints ("signed warmth shift in [+0.3, +0.8] AND Δκ in [−20, −2]"). Schema only — its empirical
  content is a portfolio row in Ch 8, not a promise here.

### Chapter 4 — Primary Readings: The Two Tiers, Annotated (~20 pp)

- 4.1 The two-tier inversion (dial ≠ encoder geometry) stated as a **finding, not a nuisance** — it is the
  frame's own seam, and the silence test later draws its line exactly there (Ch 6.1).
- 4.2 Dial-tier readings, each annotated inline: newcomer displacement 0.830 with κ tightening 21→47; D′
  cold-entry acclimation (half-life ≈ 20 msgs); noise floor exactly 0.
- 4.3 **The fine edge (1.229), decomposed:** reported only with its length annotation — cynicism/volume
  read length at r ≈ −0.30; silence-only ≥ content-only at condition grain; Stage 1 decomposition
  (cross-fitted length-residualization, stratified permutation null on common support) registered and
  INDETERMINATE on the existing corpus; the number is never deleted, only annotated
  (`committee/deep-think-2026-08-20/methodologist-glm53.md` §1–2). Decision in Ch 8.
- 4.4 Identity-tier readings: within-night separation 0.893 (p = 2.7e-5) vs silence-only collapsing below
  chance (0.36–0.39) — **the surviving object**, claimed at this grain and no other.
- 4.5 Encoder tier, honestly split: in-sample fine gap 0.478 (3/3, registered) = room-identity recoverable;
  held-out FAIL (0.0694, seed 2 < 0.05 floor) = does not generalize to unseen nights; the held-out gap
  shrinks with more nights (0.068 → 0.163 across 2/4/5/6 nights) ⇒ **data-limited, not capacity-limited**
  — a retrieval fact, not a measurement instrument. Upgrades registered (Ch 8).

### Chapter 5 — The Reader, Honestly Sized (~16 pp)

*Replaces flagship `chapter-6-the-seam.md`. One chapter-in-five mass, per R2: the object measured two
scalars; it gets sections, not a cathedral.*

- 5.1 The downgraded object, stated once, fully: a mean-shift, baseline-relative delta — slope and mean of
  ‖r−b̂‖ — real for mean-moving regimes (post-hoc r = 0.787), beaten on localization by the rival's static
  median (0.816 / 0.800 vs 0.435 / 0.467, "no temporal structure at all"), pre-switch classification edge
  only (0.867 pre vs 0.667 post), noise-fragile (r inverts at σ = 0.2). "Second-order" survives only as the
  structural term for baseline-relativity. The deeper Nurse claim (reading the reader's
  change-of-reading): **unsupported by current evidence** (`research/skills/rival-pass5-downgrade-verdict.md`
  — DOWNGRADE COMPLETE, and this chapter is written to keep it that way).
- 5.2 Negative knowledge as the primary reading: the null-drift control (0.291; per-reader nulls 0.23–0.39)
  vs primary drift 0.748 — drift is real and 2.6× separable from null; "this reader has NOT drifted from
  herself" is measurable unconditionally; positive drift is conditional on the premise band. Comparable
  sameness defined negatively first.
- 5.3 The premise, at its honest status: E2 at power INDETERMINATE (ratio 0.6088, CI [0.371, 0.921]
  touching the 0.3–0.6 kill band; under `actual_presence`, 0.3815 — inside it: the indeterminacy is
  treatment-structural); the pre-measurement number (0.5599 real-only / 0.4898 synthetic-grounded) also
  inside the band; E3 (13 real readers) below band — R = 0.140, a miss, weak evidence per its own
  registered asymmetry. Side-by-side adjudication, Branch C (post-hoc, gap logged): **retired, leaning
  false — not proven false** (`research/prototype/e2-e3-side-by-side.md`). Numerator replicated across
  three geometries (0.46–0.56); instruments diverge 4.6× on the denominator; power n ≈ 14,533 to resolve at
  current width — stated, not apologized for.
- 5.4 What is clean: **ICC 0.7714 [0.667, 0.810]** — per-reader baselines are real, stable, person-specific;
  per-dial reliability (mood .97, volume .98, earnestness .95, presence .91; panic .30 unreliable — a
  finding about which dials carry reader-identity). The premise's closest cousin measured strong.
- 5.5 The registered hinge — H-reader≡room: a trusted reader as a room that learned its own temperature;
  the deciding instrument is the slope of reader-baseline on visited-room warmth. Slope ≈ 0 ⇒ alignment
  (distinct instrument); slope ≈ 1 ⇒ collapse (the room wearing a reader's name). Between-reader
  INDETERMINATE; within-reader leans ALIGNMENT, collapse bounded ≈ 13%. **Registered hypothesis, not thesis
  statement** — promoting it before the slope exists would be the seventh laundering (`topic.md`, the
  registered-hypothesis ruling). The eigenbasis diagonalization test rides with it: if top eigen-dims align
  with the ICC-reliable subspace, reliability is *eigenbasis conservation*.
- 5.6 Cross-strata transfer, one conditional paragraph: ρ = +0.784, **lensed-space only**, mechanism
  unresolved; the clause that ran in August was cross-condition — the sixth laundering, conceded here and
  counted in Ch 7. The true cross-strata version is now runnable on the v:2 per-reader schema (Ch 8).
- 5.7 The depth-sounder rename, as concept note: the delta is temporal, not absolute; the baseline is the
  spinning disc, the delta the angular gap; median-normalization is a disc-speed turn. (Grounds
  baseline-relativity in a known engineering invariant; two paragraphs, no more.)

### Chapter 6 — The Boundary (~14 pp)

*The certificate's void-conditions page. Most dissertations bury this in "limitations"; here the falsifier
results ARE a chapter, because the fired/not-fired asymmetry is this round's deepest result.*

- 6.1 The silence test, read correctly: a frame-level falsifier registered with a binary clock/object
  branch that behaved as a **graded, localizing instrument**. It fired at condition grain (P1: the 1.229 is
  length-confounded — true and settled) and did not fire at identity grain (P2: "the field is length" —
  refuted, 0.893 vs 0.36). Conflating P1 with P2 is the one epistemic error this document must not make;
  the asymmetry establishes discriminating power and licenses re-scoping, not retirement
  (`committee/deep-think-2026-08-20/epistemologist-deepseek-pro.md` §§1–5). Registration constraint
  honored: STEP=60 auto-clock sessions excluded; the test only has teeth where the clock varies.
- 6.2 The drift-geometry branch, CLOSED PERMANENTLY: the H3 reductio — the kill number is
  geometry-malleable, so no drift-geometry redesign can adjudicate the premise. Closed means closed: no
  redesign appears anywhere in the portfolio (Ch 8), by rule.
- 6.3 The regress — flooding or settling: Ch 6-baseline numbers (corrections/day +73%, counterfactual rate
  0.497) said flooding; the registered rebound window (2026-08-19 → 2026-09-18, threshold 0.15, dormant
  repos excluded) is the clock that decides (`research/registrations/e4-rebound-window.md`). Mid-window
  early read: settling side (0.046–0.087) but the denominator has not normalized and only 6 repos cleared
  the dormant bar — **no verdict; the window-end recompute decides**
  (`research/E4-REBOUND-MIDWINDOW-2026-08-20.md`, including its own slot-inversion bug disclosure, which
  Ch 7 cites as same-day self-audit).
- 6.4 The data boundary: encoder room-identity generalization is data-limited (held-out gap 0.068 → 0.163
  across 2/4/5/6 nights; more identity data helps, more capacity does not). What would falsify the
  data-limit reading itself.
- 6.5 The frame-conditional clause: every claim in this certificate is conditional on the frame having an
  object; the frame-level falsifier is the silence test, now understood as a standing guardrail with a
  measured edge — it reads mean-moves and pacing, not re-phasing; the shape inside has a measured boundary.

### Chapter 7 — The Discipline: Six Launderings and the Audit Loop (~16 pp)

*The payload chapter. The method becomes the thesis (`topic.md`, claim inventory item 6).*

- 7.1 The procedure: pre-registration before specification, specification before code, code before
  measurement, measurement before prose; committees attack before prose exists; advisor verification with
  teeth; commit-early (survived two kernel-crash classes); the re-registration rule executed against the
  head itself — event `77b8aa4` → addendum `508fcfb`, both dated, both pre-training, the
  invalid-after-training clause never triggered.
- 7.2 **The launderings table** — all six, each with the sentence that caught it and the file: edge,
  charisma, bounded, reload-eval, cross-strata (the August cross-condition clause, caught in ZeroClaw's own
  chapter text), and the original conversation-temperature. A seventh-slot column exists and is empty; the
  table's job is to keep it empty.
- 7.3 The method's own gaps, disclosed: the cross-instrument decision tree under-specified its INDETERMINATE
  branch and was filled post-hoc at adjudication — logged as a data point about the method, not hidden
  (`prototype/e2-e3-side-by-side.md` §1); the mid-window script bug caught by eyeball-audit
  (`E4-REBOUND-MIDWINDOW`, provenance note). The discipline audits itself on the record.
- 7.4 How outside reads were metabolized: the hermes worst case answered by the held-out room, the null
  control, the treatment sensitivity — the instruments that fired; the gemini pass's H-reader≡room adopted
  as registered hypothesis, verbatim framing kept for what it means *if the slope says so*. One section,
  method-level; the reads themselves live in `research/creative/`, cited not retold.
- 7.5 The institutional finding: reproducibility makes cheap adversarial audits possible; cheap audits make
  solo reasoning survivable. Stated as the transferable claim, with the fleet's correction economics as
  evidence (subject to 6.3's unresolved verdict — cross-referenced, not double-counted).

### Chapter 8 — The Open Item and the Portfolio (~12 pp)

- 8.0 Where the certificate stands: one decisive experiment, one live clock, a registered portfolio, and a
  placement question.
- 8.1 **THE decisive open experiment: E4 Clock-Split Stage 2 — the length-matched generation corpus**
  (`committee/deep-think-2026-08-20/methodologist-glm53.md` §2). Why Stage 2 and not Stage 1: Stage 1
  (decomposition on the existing corpus) is the repair patch — it runs first, is cheap, and its ratio
  annotates every mention of 1.229 in Ch 4 regardless of outcome (the strategist's committed move,
  `strategist-seedpro.md`: "we fixed the problem in every measurement we already ran"); but Stage 1 alone
  cannot close the generative question — matching is quarantine, decomposition is measurement. Stage 2 is
  confirmatory and decisive: ≥ 6 independent condition nights (3/3; independent seeds AND independent
  length draws), SEG1/SEG2 matched on length marginals and window-scale statistics, a frozen-judge
  content-validity gate, then the raw fine gap recomputed with the clock arm out of fuel by construction.
  Branch table, pre-stated for the architecture (R3):
  - **PASS** (deconfounded gap ≥ 0.37, stratified-null p < 0.05, residualized-content > silence-only): the
    fine edge registers with its decomposition; Ch 4.3's annotation upgrades from "length-confounded,
    indeterminate" to "X% length-carried, Y% condition-specific"; the thesis sentence may re-list the fine
    edge among its evidence — no structural change needed.
  - **KILL** (CI entirely below 0.37, or silence-only ≥ residualized-content − 0.10): 1.229 is
    re-registered as length-carried and henceforth reported only with its decomposition; Ch 4.3's text
    stands as written; the identity-tier object (0.893) carries Ch 4 alone — which the architecture already
    sizes it to do. The title does not move ("clock-bound edge" remains true).
  - **INDETERMINATE** (incl. common-support coverage < 70% or unanticipated gate shape): the declared
    honesty clause — reported, not absorbed; the certificate ships with the condition-grain edge
    explicitly unresolved, listed among the void conditions in Ch 6.
  - Sits in the outline as: **Ch 4.3's annotation + Ch 8.1's branch table.** It is the only open run that
    can move the claim inventory's core in either direction.
- 8.2 The live clock: the rebound window (Ch 6.3) — zero new work, 2026-09-18 recompute decides one
  boundary sentence (flooding vs settling). Explicitly NOT the decisive experiment: it adjudicates a
  boundary condition, not a core claim.
- 8.3 The registered portfolio, resized (table): the slope regression + eigenbasis test (the premise's
  hinge); true cross-strata transfer (now runnable on the v:2 schema; gated); encoder identity-data
  upgrades (the data-limit reading predicts held-out gains with nights — a falsifiable prediction the
  portfolio owns); the rebound extension rule. **Drift-geometry: absent by rule** (closed permanently,
  Ch 6.2).
- 8.4 Housekeeping flags, filed here so they cannot be lost: (a) **E-numbering collision** —
  `chapter-7-future-work.md` §7.2 registers E4 = Rebound Test while the methodologist's 2026-08-20
  registration is E4 = Clock-Split; re-letter before filing (suggestion: Clock-Split = E7, rebound keeps
  E4 with its registration file unchanged); (b) the barkeep outlier robustness check (ratio + ICC,
  barkeep-excluded) is registered and must appear with 5.3/5.4's numbers; (c) cross-check
  `research/quilt/quilt-survey.md` against the placement section before it is cited as settled.
- 8.5 Fleet placement, one section, placement-not-depth (`topic.md`, open question 5): Vectorize proposes,
  D1 formalizes (crab-traps' production pattern); snapshot/edge rows with signed gaps and Δκ; Quilt cells
  read them as live values (grid-as-runtime); zeitgeist quarantined as sampler layer. Whether the
  mean-shift delta earns a place in fleet memory architecture is stated as the open placement question it
  is — a question, not a systems-design chapter.

### Back matter

- **Related work** (`related-work.md`, already committee-mandated): the ancestors named and accounted —
  Shewhart/CUSUM, Jacobson–Truax, GMM-UBM, FaceNet, InfoNCE, d′/SDT, Agrippa, vMF, JEPA, MLOps drift
  monitoring — with the two pass-4 findings (premise sweep, "not an identity" reduction) welded to every
  novelty claim.
- **Appendices:** registrations ledger (every dated commitment with its commit hash); the edge-log schema;
  replay/verification procedures (SHA-verified determinism, md5-identical corpora); the claim-ledger
  change-log (the running diff of Ch 1.3's table across drafts — the document's own audit trail).

---

## 5. What the thesis claims now — vs. what it used to claim

| Claim | Used to be | Now (verdict) | Chapter |
|---|---|---|---|
| Room-field thermometer (vMF snapshot, warmth decoupled from κ, replay-honest log) | Support act | **SOLID** — Gate 1 closed, audited | 3 |
| Room-identity object (content 0.893 vs silence 0.36) | Buried inside encoder tier | **SOLID — the surviving object**, claimed at identity grain | 4.4 |
| Fine edge 1.229 (dial-tier fine gap) | Flagship proof in the thesis sentence | **DEMOTED — length-confounded; annotated; INDETERMINATE pending Stage 2** | 4.3, 8.1 |
| Encoder room-identity | "Room-identity recoverable" | **SPLIT** — in-sample 0.478 real; held-out FAIL; retrieval fact, data-limited | 4.5, 6.4 |
| Reader-delta as "the crown" / second-order reading | Chapter 6 flagship | **DEMOTED — mean-shift baseline-relative delta, two scalars, pre-switch edge only** | 5.1 |
| The premise (idiosyncratic baselines ≫ drift) | Doctrine's enabling condition | **INDETERMINATE / retired-leaning-false** — treatment-sensitive, inside kill band; E2/E3 Branch C | 5.3 |
| Baseline reliability (ICC 0.7714) | Control statistic | **SOLID — the clean half**, the delta's best quantitative support | 5.4 |
| H-reader≡room (reader as slow-warming room) | Candidate thesis statement (harvest gem) | **REGISTERED HYPOTHESIS** — within-reader leans alignment; collapse ≤ 13%; not promoted | 5.5 |
| Negative-knowledge reading (null-drift) | Control condition | **PROMOTED — the instrument's primary unconditional reading** | 5.2 |
| Cross-strata transfer | "Transfer works" (r = 0.967 era) | **CONDITIONAL — ρ = +0.784 lensed-space only; August clause was cross-condition (laundering #6)** | 5.6 |
| Drift-geometry redesign path | Open branch | **CLOSED PERMANENTLY** — H3 reductio: kill number is geometry-malleable | 6.2 |
| The regress terminates | "Settles into a fixed point" | **UNRESOLVED — flooding on Ch 6 numbers; rebound window decides 2026-09-18** | 6.3 |
| Conversation temperature (v1) | The thesis | **DEAD — category error** (told once, Ch 1.1; counted, Ch 7.2) | — |
| The discipline | Preamble | **THE DURABLE CONTRIBUTION — payload chapter, title billing** | 7 |

The dissertation claims **less** than the v2 draft and claims it **cleanly**: one solid instrument, one
solid object, one cleanly-measured small object, one strong reliability result, three registered hinges,
and a discipline — with every demotion visible on the face page.

---

## 6. The cut-list (zero-shot critique at checkpoints)

Method: after drafting each chapter cluster, I stopped and asked — *"Is this essential to the thesis as it
stands, or is it leftover from a retired hypothesis? Does it survive the cut-the-crap test?"* What failed
was cut. Each cut below records its checkpoint and a one-line why.

**Checkpoint 1 — after Ch 1–2 (question + doctrine):**

1. **CUT: the v1 conversation-temperature death, as repeated narrative.** Kept once (Ch 1.1) as
   provenance; cut from every other chapter's throat-clearing. *Why: retelling a dead claim twice is
   defending it; the lineage is provenance, not an argument.*
2. **CUT: the polyformal 10-language kernel as a section.** One citation sentence in Ch 3.2 as
   verification artifact. *Why: a port-a-thon has zero thesis load; its entire epistemic content is "the
   golden vectors reproduce," which is one sentence.*
3. **CUT: the harvest/genealogy tour (gemini, hermes, qwen, plainsong as sections).** Metabolized into
   Ch 7.4 (method-level) and Ch 5.5 (the one adopted hypothesis). *Why: a gratitude tour is not an
   argument; outside reads are inputs, already counted in the files where they landed.*

**Checkpoint 2 — after Ch 3–4 (instrument + readings):**

4. **CUT: `chapter-5-retrieval.md` as a standalone chapter.** Schema folds into Ch 3.5; empirical content
   becomes a Ch 8 portfolio row. *Why: a skeleton "blocked on the contrast head" is a promissory note
   given shelf space — chapter status for an empty result is laundering by architecture.*
5. **CUT: 1.229 from the abstract's evidence list and the thesis sentence.** The number appears only with
   its decomposition annotation (Ch 4.3). *Why: the epistemologist's P1 — the condition-grain falsifier
   fired on exactly this number; citing it unannotated in the abstract is the seventh laundering wearing
   a bow tie.*
6. **CUT: contrast-head anticipation inside the instrument chapter.** Moved to Ch 8. *Why: future work
   inside an instrument chapter inflates the instrument by anticipation.*

**Checkpoint 3 — after Ch 5 (the reader):**

7. **CUT: `chapter-6-the-seam.md` as a standalone flagship.** Its honest mass is ~40% of one chapter →
   Ch 5, five sections. *Why: the object measured two scalars; typography is rhetoric, and a flagship
   chapter for a downgraded object re-inflates it (R2).*
8. **CUT: "the crown" as a framing word, everywhere.** *Why: crowning an INDETERMINATE-premise object is
   a promissory note posing as a result; `topic.md` itself forbids the promotion.*
9. **CUT: clause-3 transfer numbers (r = 0.829 / R² 0.729 / 13-for-13) as supporting evidence.** They
   appear only inside Ch 7.2's launderings table. *Why: class propagation, not drift-reading — a
   class-conditional mean with zero SEG1 data beat it; citing it as support launders the demolition.*
10. **CUT: H-reader≡room as thesis statement.** Stays a registered hypothesis (Ch 5.5). *Why: promoting
    before the slope exists is laundering #7 by `topic.md`'s own ruling; the convergence evidence is
    suggestive, not decisive.*
11. **Kept, with reasons on record (the cut test cuts both ways):** the negative-knowledge reading
    (Ch 5.2), the ICC section (5.4), the depth-sounder note (5.7). *Why kept: each is load-bearing for a
    registered number that exists — cutting honest small results to seem austere is vanity, not
    discipline.*

**Checkpoint 4 — after Ch 6 (the boundary):**

12. **CUT: any drift-geometry redesign from the portfolio and all forward-looking text.** *Why: closed
    permanently by the H3 reductio — a dead branch kept in the exit map is laundering by portfolio.*
13. **CUT: cross-strata transfer as an unconditional claim.** One conditional paragraph (Ch 5.6). *Why:
    lensed-space only, and the clause that ran was cross-condition (laundering #6) — an unconditional
    phrasing would be the same laundering with the number swapped.*
14. **CUT: the Switch Test as evidence for anything.** It survives only as boundary machinery
    (mean-moves-not-re-phasing, Ch 6.5) and as a booked rival win (Ch 5.1). *Why: it was a registered
    miss (0.467 vs 0.80) and the rival's median-static cell beat it — a miss cited as support is the
    purest laundering there is.*

**Checkpoint 5 — after Ch 7–8 (discipline + exit):**

15. **CUT: the rebound test from the "decisive experiment" slot.** Demoted to "the live clock" (Ch 8.2).
    *Why: it is a clock, not an experiment — zero new work, and it decides one boundary sentence, not the
    claim inventory's core; the brief's one-decisive-experiment slot belongs to Stage 2.*
16. **CUT: fleet placement as a systems-design chapter.** One section (Ch 8.5). *Why: open question 5 is
    explicitly "a placement question, not a depth question" — architecture diagrams for an integration
    that hasn't run are vibes with boxes.*
17. **CUT: the moments doctrine as load-bearing.** One labeled section in Ch 2.5. *Why: registered-not-
    proved experiential frame; giving it more mass spends typography the verdicts didn't earn.*

**What survived all five checkpoints — the load-bearing set:** Gate 1 estimation, the edge log, the
identity-tier object, the annotated fine edge, the two-scalar delta, the ICC, the null-drift primary
reading, the registered slope, the launderings table, the Stage 2 branch table. Ten things. That is the
dissertation.

---

## 7. Why this structure wins

1. **It cannot launder by structure.** The artifact tour launders demotions through sequence and chapter
   mass; the certificate puts verdicts on the face page (Ch 1.3) and sizes chapters by evidential mass
   (R2). A skimming committee receives the honest claim set from the table of contents alone.
2. **It is branch-invariant under the decisive experiment (R3).** Stage 2's PASS/KILL/INDETERMINATE
   branches each have a pre-stated home (Ch 8.1); the title survives all three. A rival architecture
   titled *The Felt Size of the Step* dies under KILL — mine doesn't, because "clock-bound edge" is the
   truth under every branch. The outline obeys the same rule the registrations do: every branch
   pre-stated, none absorbed.
3. **It agrees with the ledger, then enforces it.** `topic.md` already rules the discipline "the durable
   contribution" — this architecture gives it the payload chapter and title billing, instead of preamble
   status. And it enforces the boundary as first-class (Ch 6) because the epistemologist's asymmetry —
   fired at condition grain, survived at identity grain — is the round's deepest result; burying it in a
   limitations section would bury the finding.
4. **It cuts 17 things and says so.** The cut-list is part of the deliverable, with checkpoint
   provenance — an architecture that cannot show its own cuts-the-crap test hasn't taken one. The
   residual risk this guards against is structural: chapters are claims, and every claim here has a
   verdict, a file, and a chapter that matches its size.

*No git operations performed, per instruction.*
