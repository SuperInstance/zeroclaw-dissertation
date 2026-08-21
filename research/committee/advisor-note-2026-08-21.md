# Advisor Note — 2026-08-21 (Lucineer, senior advisor)

*Filed to the committee folder per the advisor role the Captain assigned at 10:00 AKDT.*

## The work ahead, in order

1. **E2/E3 premise-band-movers — the next registered test, now.** The design
   (`memory/E2E3-premise-band-movers-design-2026-08-21.md`) is complete and
   registered. Implementation route is named but unmade:
   `scripts/premise_band_movers.py` + topic.md addendum. Run it per the design
   exactly: primary on wave-2 T-nights (21 readers, 66 signal + 7 null), wave-1
   S1–S5 as replication, never pooled. Four registered statistics (A timing vs
   circular-shift nulls, D coverage, P persistence, S x-regression with reader
   FE vs roster competitor). Kill criteria and VOID-by-rule are pre-stated —
   honor them. The bare crossing rate is NEVER evidence; only timing,
   persistence, and x-invariance carry content.
2. **The decisive experiment (abstract sentence 6)**: a length-matched
   generation corpus with every branch pre-stated. This is the endgame — the
   premise band (0.3–0.6, ratio 0.6088) decides whether a trusted reader is an
   instrument or a slow-warming room. E2/E3 is the vanguard; the length-matched
   corpus is the verdict.
3. **Chapter drafting against the merged master outline.** The spine is
   settled (Edge Log + Certificate face page, R1–R5). Draft chapters to it:
   grain-native shelving, verdict-first, no deleted numbers (only annotated).
4. **The naming doctrine (Captain's ruling, 10:00)**: elephant STAYS elephant
   for v1 — perfected for what it is. The NEXT major species earns a new name.
   The elephant-in-the-room metaphor is the correct frame for JEPA (felt, not
   wordable). Do not rename; document the rationale.
5. **Discipline guardrails (unchanged)**: pre-registration before
   specification, adversarial committees before prose, re-registration against
   the head. Six launderings caught before filing is the standard to hold.

## Handed to ZeroClaw

- Rival pass-5 stragglers: propagated (3031a3e, annotate-only). Confirm the
  downgrade holds across the claim inventory.
- Class-residual tripwire adjudication remains a documented committee item —
  not a landing blocker, but schedule it.
- The addendum (a43235f) is the registration layer; v3 registration stands.

*Advisor's standing: the ledger is the contribution. Keep it honest, keep it
append-only.*

---

## Wave-2 verdicts — filed 2026-08-21 (annotate-only; the ledger stays append-only)

The four wave-2 research docs are filed to
`research/committee/research-wave2-2026-08-21/` (post-reg1, array-gain, cohesion,
jepa-implementation). What they change, in order of consequence:

### 1. Temperature ≠ warmth — the re-booking (REG-1, branch B)

The REG-1 rotation verdict re-books the foundation's central assumption. The
a-priori warm direction **W does not align with the data-derived temperature axis
v\*** — W sits 64–86° off it (cos(W, v\*) = 0.08–0.48 across the sensitivity grid,
never ≥ 0.48), while W remains the leading personality axis (cos(W, PC1_pers) =
0.857–0.976). The room's measured shared state is a **volume(+) / presence(−)
participation-energy contrast**, not warmth. Warmth is valence and belongs to the
readers (mood is the most reader-stable dial, ICC 0.965/0.983); temperature is
energy and belongs to the room. **The room has temperature and no warmth; the
readers have warmth and no temperature.** The instrument was a thermometer read as
a mood ring.

### 2. The dual-R4 annotation — every warmth claim must now carry it

Per the post-reg1 synthesis, no warmth output or warmth-adjacent number survives
without two filed quantities plus a rephrase:

1. **cos(W, v\*) ≤ 0.44** (CI ≤ 0.50) — "warmth is not the temperature axis."
2. **cos(W, PC1_pers) ≥ 0.80** (filed 0.857–0.976) — "warmth *is* the personality
   axis."
3. **Rephrase:** "warmth measures reader disposition; the room's shared state is
   the volume/presence contrast v\*."

The confound is labeled for visibility, not killed (ZeroClaw's ruling) — but it is
now labeled with a measured angle, not a metaphor.

### 3. Next registrations

- **REG-4** — V/P-axis replication: does v\* itself reproduce (cos(v\*_new, v\*_filed)
  ≥ 0.8) on a fresh corpus?
- **REG-5** — family-invariance of the V/P contrast (S- vs T- vs D-nights).
- **REG-6** — do room transitions move μ̂ along v\*, not W (cos(Δμ̂, v\*) >
  cos(Δμ̂, W))?
- **REG-4-ARRAY** — subsampling calibration (R ∈ {5, 8, 10, 15, 21}): the Captain's
  100-boat doctrine as a power-vs-R certificate. Leg-D is the 100-boat leg
  (exponential/logistic approach, not √R); the wave-2 E2/E3 VOID was attendance,
  not signal (21 enrolled at 38% attendance ⇒ effective R ≈ 8 ⇒ 14–17 events < the
  20-event floor).
- **COH-1** — cohesion as the third orthogonal registered object (base-orbit
  translation ‖Δb̄‖ = ‖ĉ‖/corpus_sd; q = RMS(r_R)/RMS(o_pre) as purity),
  pre-registered with P1–P4 and a >2× signal/rest verdict bar in both waves;
  retires the saturated P-cosine (P_trans 0.994 vs P_rest 0.9935) into a
  two-channel (rigidity + purity) readout.

### 4. JEPA-v1 sequenced for S4

The JEPA implementation path is booked: frozen vMF field encoder → 2-layer MLP
(64→32→7) predictor → L1 loss on the registered v\*/κ axes, q-rule masked, no
reconstruction. Sequenced for **S4** (post-REG-1), falsifiable via a >15% beat of
the persistence baseline on held-out nights. No new corpus required — it trains on
the existing wave-1/2 corpora.

### 5. The premise, re-anchored

The premise ("a trusted reader = instrument or slow-warming room") does **not**
survive REG-1 in its warmth form. It survives only as a **V/P-band**: *a trusted
reader is an instrument of the room's participation energy, or a reader whose
energy slowly tracks the room — never a reader who warms a room, because the room
was never warm.* The thesis's thermometer was right; the quantity it was named for
was the wrong one.

*Annotated, not rewritten: the v3 registration and all prior addenda stand; this
is a wave-2 verdict filing note only.*
