# METHODOLOGIST — Defense Board Round 1 (2026-08-28)

**Role:** empirical-methods reviewer (pre-registration discipline, power, CI correctness, held-out hygiene).
**Audited:** the wave-4 S2 freeze plan (`research/S2-FREEZE-PREP.md`, `research/PROMPT-PACK-S2.md`, elephant `docs/wave4-registration-draft-2026-08-22.md`, elephant `docs/wave4-S1-hardening-2026-08-22.md`) and the geometry foundation (`research/GEOMETRY-FOUNDATION.md`, `docs/RE-THINK-2026-08-28.md`). `research/SILENCE-TEST.md` audited as the parallel lane. STATUS-2026-08-28 and topic.md v3 used as claim inventory.
**Repo state at audit:** dissertation `master` @ `1898fb4`; elephant @ `a348503` (08-26), fiber v4 landed `5fe5c47`; S1 sweep executed 08-22 @ `5b8af52`.
**Headline: 3 BLOCKS-S2 items (R1, R2, R3). Freezing as currently drafted would violate the project's own pre-registered design gate, rest on uncertified power, and carry an ambiguous kill predicate. All three are fixable in text before lock; none requires new data except a post-fix pilot certification (R6) and a possible redesign sweep (R1).**

---

## Part 1 — Methodological risks, with severity and mitigation

### R1 — The freeze plan freezes a design whose pre-stated design gate already FAILED — **BLOCKS-S2**

**Evidence.** Elephant `docs/wave4-S1-hardening-2026-08-22.md` (executed, unsealed, 08-22):

- Gate clause "P fires at α=1": pre-stated bar `P_trans < 0.5×P_rest`; result **P_trans 0.9754, P_rest 0.9948 (ratio 0.981) — FAIL**.
- Filed verdict, verbatim: "GATE: FAIL … the rework failed and must not be registered. No redesign attempted here; goes to Casey."
- The registration draft §1.2 pre-stated this as "the kill for the design, not the corpus."

The S2-FREEZE-PREP and PROMPT-PACK documents (both 08-28, six days later) build the committee round around H-α-FIBER with "P_trans < 0.5×P_rest at α=1" as the expected POSITIVE matrix cell, list the machinery checklist as if generation-ready, and **do not mention the S1 failure anywhere**. Freezing on that text would (a) violate the draft's own kill rule, and (b) launder a dead design into a registration — the exact laundering pattern (7 caught so far) the method chapter is built on.

One live signal exists in the S1 data: **ICC declines 0.885 (α=0) → 0.744 (α=1)** — the §1.4 predicted direction, and a within-pair gap of 0.141 against wave-3 within-pair ICC gaps ≤ 0.005 (≈28× the pair envelope). But promoting ICC to primary *after seeing it fire* is outcome-switching unless handled as a fresh registration (below), and ICC-at-0.744 has a discriminability problem: wave-3's instrument-corpus ICC range was .73–.88, so 0.744 is **inside the wave-3 instrument range** corpus-level; only the paired gap discriminates.

**Mitigation (concrete).**
1. The S2 freeze text must open with a **design-gate status disclosure**: the 08-22 v4 FAIL, verbatim numbers, and the escalation to Casey.
2. Then one of two paths, frozen in writing before any sealed generation:
   - **(a) Redesign path:** fiber v5 with a mechanistic fix for the diagnosed cause (roster-mean centering subtracts the common-mode moving target; AR_PHI=0.9 wobble persistence vs trailing W=12 estimator), a fresh S1 sweep, and gate PASS — with the redesign itself registered (what changed, why, and the iteration budget of R7).
   - **(b) Re-registration path (wave-4b):** H-α-ICC (or committee-designated successor) as a new hypothesis frozen before new corpus generation, S1 pilots quarantined as design-phase evidence and disclosed as such, with the **paired within-pair gap** (not the corpus-level value) as the registered statistic — corpus-level ICC at 0.744 is indistinguishable from wave-3 instrument corpora by wave-3's own G6 re-band.
3. Either way, the branch×leg matrix's P row expected-verdict flips from POSITIVE to the honestly pre-stated failure cell until a gate PASS exists.

### R2 — Power is uncertified, and at n=5 matched pairs the design cannot reach p<0.05 two-sided even with a perfect outcome — **BLOCKS-S2**

**Evidence.** S2-FREEZE-PREP Clause D correctly demands power certification and blocks downstream until then — but nothing in the pack computes it, and the arithmetic is unfavorable as constituted:

- 5 α-only matched pairs. Exact sign test, all 5 pairs concordant: two-sided p = 2·(1/2)^5 = **0.0625 > 0.05**. One-sided: 0.03125 — significant **only if** the one-sided direction is frozen in advance. Nothing in the draft pre-states sidedness.
- Wave-3 reference scatter (the only variance estimates available): within-pair A-rate gaps median ~0.011, max ~0.085; ICC pair gaps ≤ 0.005; pair separations on A ~18×, P_trans ~16×, S ~10×, spread ~75×, ICC ~28× *below* room-draw scatter (that was the blindness finding — i.e., the noise floor).
- S1 pilot effect sizes: P gap 0.0002 (dead, per R1); ICC gap 0.141; A gap 0.0333 (inside envelope, as designed).
- The ≥20-event floor: pilot A fired on 15–16 events over 5 nights; wave-3 sealed corpora carry 9 nights (~29 events at the pilot rate) — plausible but **not computed per leg** anywhere in the freeze text.

**Mitigation.** Freeze, in the S2 text, with arithmetic shown: (i) sidedness — one-sided is defensible because direction is pre-registered (monotone decline in α); state it, or (ii) grow to n≥6 pairs (6/6 two-sided p = 0.03125), or (iii) pre-register a paired bootstrap CI on pair gaps with a frozen threshold and simulated power from the wave-3 envelopes + S1 effects. Per pre-named leg: minimum detectable effect (MDE) vs its envelope, and a rule that MDE > ½ the pilot effect ⇒ underpowered, design does not freeze. Per-leg event-floor arithmetic (nights × event rate ≥ 20 for every leg, including P's flip events and D's crossings) written into the corpus spec.

### R3 — The kill-band predicate exists in three inconsistent formulations across plan documents — **BLOCKS-S2**

**Evidence.** Three different rules are in circulation:

1. **Registered implementation** (`scripts/e2_instrument.py::verdict()`, CI-based): `lo > 0.6` CLEAR / `hi < 0.3` KILL / otherwise INDETERMINATE. This is what adjudicated E2 (ratio 0.6088, CI [0.371, 0.921] → INDETERMINATE, "kill does not fire (CI upper > 0.6)").
2. **S2-FREEZE-PREP** (point-estimate-based): "if a ratio sits in 0.3–0.6 band, the kill condition is disclosed alongside the measurement."
3. **S2-FREEZE-PREP, enforcement line** (garbled): "do not declare if ≤0.3 or ≥0.6 uncertainty straddles band."

Formulations 1 and 2 disagree on real cases: a ratio at 0.61 with CI [0.35, 0.92] is CLEAR under rule 2 and INDETERMINATE under rule 1; a ratio at 0.55 with CI [0.62, 0.90] is KILL-side under rule 2 and CLEAR under rule 1. The premise question — the wound that produced the 0.3–0.6 doctrine — is exactly where this adjudication freedom would land. An ambiguous predicate in the freeze text is a post-hoc adjudication channel.

**Mitigation.** Freeze exactly one predicate, verbatim from the registered implementation, and pin the implementing artifact (file, function, commit) in the S2 text. Recommended: the CI rule (it is what E2 was adjudicated under; changing it now would re-open a filed verdict). Any premise-side ratio quoted anywhere in wave-4 output carries: point estimate, CI, band-touch flag, dual-R4 annotation — and is annotation-only, never a verdict input (premise power is honestly dead at current width: n ≈ 14,533 readers to resolve; the registered slope regression remains the premise's decisive test, not wave-4).

### R4 — CI computation correctness: the silent-numeric-bug class has two documented members and no standing guard — **weakens**

**Evidence.** (a) The CI bisection wound: bisection negated wrong mid-fix, CIs collapsed to 0.0, caught only because the responsible subagent died and the failure was visible. (b) E5 erratum: in-place mutation bug inflated class-residual 0.4366 → clean 0.1342 (CI [0.0303, 0.1942]). Both are the same class: silent numeric errors producing plausible-but-wrong headline numbers, caught late by audit rather than by the pipeline. Current machinery (percentile bootstrap, B=2000, frozen seeds 20260819/20260821, reader-clustered) is the simple variant and currently clean — but nothing structurally prevents per-experiment re-derivation, and wave-4 adds new statistics (q-rule, kl_sym, calibration curve).

**Mitigation.** One frozen CI utility, version-pinned in the S2 text; a golden-value harness as a freeze-commit gate: (i) synthetic data with closed-form CIs, (ii) invariants on every registered output — lo ≤ point ≤ hi, width > 0 for non-degenerate input, seed-reproducibility bit-identical, (iii) E5-class guard: inputs copied, never mutated in place (assert in the harness). Any new CI method (BCa, test-inversion, any root-finding) requires the harness green at its first registered use — a bisection that converges to a degenerate interval must fail loud, not return 0.0.

### R5 — Multiple-comparison exposure is unquantified: an implicit family of ~100+ tests with no family-wise control — **weakens**

**Evidence.** Count the adjudicated cells the plan implies: R5-style branch table (5 branch rows × 7 legs = 35) + 5 pairs × 5 statistics (25) + REG-1′/2/3 branch tables (~8) + W∈{8,16} sensitivity doubling primary legs + presence canonical/actual doubling premise-side ratios — the treatment axis with a **known** verdict-flipping sensitivity (ratio 0.6088 canonical vs 0.3815 under `actual_presence`). Family ≈ 100+ tests at nominal thresholds ⇒ ~5 expected false positives at 5%, with no correction, hierarchy, or family size stated anywhere in the freeze pack. Wave-3's own history shows the failure mode: P's 0.99-class "PASS" cells that turned out to be non-discriminating mislead cell-by-cell reading.

**Mitigation.** In the S2 text: (i) exactly one primary endpoint per hypothesis; (ii) an enumerated family with an explicit hierarchy — primary / secondary / exploratory — and secondaries labeled "no family-wise control, descriptive"; (iii) within-run replication required for the primary: the α=1 signal must appear in both the k-series and the pair-series independently; (iv) a pre-stated treatment for the presence axis (canonical is registered; `actual_presence` is a disclosed sensitivity, never a re-adjudication); (v) dual-R4 annotation mandatory on every ratio.

### R6 — Pilot provenance predates the 08-26 probe-honesty fix — **weakens**

**Evidence.** S1 pilots ran 08-22; the probe-honesty fix (vMF estimator path, entrance dedup — the fix for the Tap κ-delta window-composition artifact on a banned κ proxy) landed 08-26 (`738b434`, `a348503`). The fix targeted the live-probe path, and the pilots' legs read generated corpora via `wave3_s3_legs.py` — contamination is unlikely but **uncertified**, and the fix's event-counting changes (entrance dedup) are exactly the kind of thing that moves pilot-derived thresholds and the ≥20-event arithmetic.

**Mitigation.** A one-paragraph written certification in the freeze text: the code paths consumed by `wave4_s1_pilots.py` legs vs the paths changed by `a348503`, with a conclusion of non-overlap — or, cheaper than the argument, a re-run of the S1 sweep on the fixed code (unsealed, hours). Plus a standing exclusion: pilot corpora can never enter the sealed set (the fresh master seed 20260822 already prevents stream overlap; state the corpus-level exclusion explicitly).

### R7 — No iteration budget on the design gate: the sharpest post-hoc channel — **weakens**

**Evidence.** The design gate permits unsealed pilots until PASS. Without a frozen budget, amplitude/fiber parameters can be tuned until the desired leg fires and then "frozen" — curve-fitting the design to the outcome. PROMPT-PACK's RIVAL prompt attacks the amplitude's S1 provenance but no clause caps iterations. Post-R1 this is more acute: a redesign loop is now certain, and every loop is a degree of freedom.

**Mitigation.** Freeze in the S2 text: exactly N design iterations permitted after the 08-22 failure (recommend N=1); each iteration's parameter deltas logged with a mechanistic rationale (not "it made P fire"); budget exhausted + gate FAIL ⇒ the design dies, honest negative files as a detection-envelope bound (the pre-stated frame). Amplitude clause carries the pilot script, the exact pilot output it derives from, and re-runnability (a reviewer re-runs `wave4_s1_pilots.py` and reproduces the number).

### R8 — Silence test: internally inconsistent adjudication and self-contradictory corpus arithmetic — **weakens**

**Evidence.** (a) Success = "any one of 3" while failure = "any one of 3": a mixed outcome (κ persistence ≥90% AND ICC < 0.50) has no pre-stated verdict — the tie-break is missing. (b) Corpus sizing contradicts itself: "~15–20% reduction … 80–120 sessions remain from original ~500–600" vs deliverables "~400–480 records"; 15–20% removed from 500–600 leaves 400–510 — the 80–120 figure counts removed sessions, not remaining. (c) No power statement for any threshold (κ persistence 90% vs 60%; P_trans precision 80% vs 50%; ICC 0.70 vs 0.50) or expected n_readers on the trimmed corpus.

**Mitigation.** Pre-state the tie-break (recommend, honest-negative tradition: any failure-threshold firing ⇒ FAILURE verdict regardless of successes; successes only count when no failure fires). Correct the n figure and state expected n_readers and the ICC CI width on the trimmed corpus. Keep it parallel and non-blocking as registered — but its verdicts are annotation-grade for the thermometer claim, not re-adjudications (it was registered 08-19 before wave-3 results; that provenance is its strength, don't spend it on a sloppy adjudication rule).

### R9 — Construction-null clause is queued, not registered: held-out discipline must be a void rule, not a memo — **weakens**

**Evidence.** The known wound: encoder-tier in-sample 0.478 vs held-out 0.0694 — the in-sample similarity structure was memorization, not measurement (board cites 4–15× across variants). GEOMETRY-FOUNDATION §2.4 now supplies the general instrument: an 8-dim embedding achieves adjacent-pair cosine 0.7394 vs ~0.01 random **with zero training** — similarity structure alone can never evidence measurement. §4 queues the construction-null clause for committee but registers nothing. REG-1′ is in-sample by design (calibration-only, honestly labeled) — fine — but wave-4+ (the RE-THINK substrate lane, encoder upgrades of open Q2) will generate embedding claims, and today nothing registered stops an in-sample similarity citation from entering a verdict.

**Mitigation.** Register now, as a standing void rule riding the S2 text: any similarity-structure evidence (encoder, embedding, substrate) presented as instrument evidence is VOID unless it shows held-out separation against a locality-correlated-by-construction baseline of the same dimension. One clause; closes the class the encoder wound opened.

### R10 — Single-corpus intermediate-α levels make the continuity ladder fragile — **weakens**

**Evidence.** α ∈ {0.25, 0.5, 0.75} is carried by one k-corpus each in the 16-corpus skeleton; the ladder rule (±0.10 between consecutive α) can therefore VOID the gradient clause off one noisy corpus at one level, with no replication inside the k-series. The five pairs replicate α-contrasts, not levels.

**Mitigation.** Either duplicate the intermediate levels (16 → 19 corpora; cheap — generation is the smallest cost in this pipeline) or pre-state in the matrix which corpus is ladder-authoritative and that pair members are replication inputs, never ladder inputs. State the consequence before generation, not at adjudication.

### R11 — Geometry numbers are self-verified in-session — **cosmetic (upgrade to weakens if any frozen doc cites them)**

**Evidence.** 9/9 tests and digit-for-digit headline reproduction (tile growth → φ² = 2.618; gen-5: 1915 tiles, 3730 edges, avg degree 3.90; diffusion variance 1.0000→0.6894; adjacent cosine 0.7394) were performed by the authoring lane. Fine for a research note; not sufficient provenance for registration-grade citation. Also: random-pair baseline is draw-dependent (README 0.0092 vs independent draw 0.0134) and must be quoted as "~0.01", never as a constant.

**Mitigation.** One independent reproduction (different agent or machine), result recorded in the doc, before any frozen document cites a geometry number. Quoting discipline for the baseline stated in the doc itself.

### R12 — Snap and diffusion parameters are unregistered modeling choices — **cosmetic**

**Evidence.** Pythagorean snap histogram {5:320, 13:535, 17:855, 25:530}; diffusion depth 8 rounds — both disclosed honestly as choices, not derived constants ("8 rounds is a choice"; snapping "must be registered like any threshold"). The risk is latent: the first corpus analysis that quietly uses snapped coordinates launders the discretization into the metric.

**Mitigation.** The queued snap-parameter registration template (GEOMETRY-FOUNDATION §4c) becomes a hard gate: no corpus data touches snap coordinates or the gravity field's convergence depth until those parameters are frozen. Booking after wave-4 S5, as filed — acceptable, since no registered analysis currently consumes them.

---

## Part 2 — Severity table

| # | Risk | Severity | One-line fix |
|---|------|----------|--------------|
| R1 | Freeze ignores the 08-22 design-gate FAIL (P dead at α=1) | **BLOCKS-S2** | Disclose FAIL in freeze text; redesign+new gate, or wave-4b re-registration with paired-gap statistic |
| R2 | Power uncertified; 5 pairs cannot reach p<0.05 two-sided (0.0625) | **BLOCKS-S2** | Freeze one-sided direction, or n≥6 pairs, or bootstrap-on-gaps with shown arithmetic |
| R3 | Kill-band predicate stated 3 inconsistent ways | **BLOCKS-S2** | Freeze the registered CI rule verbatim + implementing artifact |
| R4 | Silent numeric bug class (CI bisection, E5 mutation) unguarded | weakens | Frozen CI utility + golden-value harness as freeze-commit gate |
| R5 | ~100+ implicit tests, no family-wise control | weakens | One primary endpoint; enumerated hierarchy; k+pair dual replication |
| R6 | Pilots predate the 08-26 estimator fix | weakens | Written path certification or cheap post-fix re-run; pilots excluded from sealed set |
| R7 | No design-gate iteration budget | weakens | N=1 redesign, mechanistic rationale per delta, budget-out = design dies |
| R8 | Silence-test tie-break missing; n self-contradiction | weakens | Worst-firing-metric rule; correct 400–510 figure; state n_readers |
| R9 | Construction-null clause queued, not registered | weakens | Register as standing void rule in S2 text |
| R10 | Ladder fragile on single-corpus α levels | weakens | Duplicate intermediates (16→19) or name ladder-authoritative corpus |
| R11 | Geometry self-verified; draw-dependent baseline quoting | cosmetic | One independent reproduction; quote baseline as ~0.01 |
| R12 | Snap/diffusion parameters unregistered | cosmetic | Hard gate: no corpus use before parameter freeze |

---

## Part 3 — Pre-registration checklist (freeze in writing BEFORE any S3 generation)

**Hypotheses**
- [ ] Primary hypothesis verbatim (H-α-FIBER successor or redesign), with both anti-hypotheses pre-stated: (i) amplitude-matched wobble swamps α → all legs blind, envelope bound extends; (ii) legs see wobble/carrier, not α → laundering, void.
- [ ] Design-gate status disclosed in the freeze text: the 08-22 FAIL (P_trans 0.9754 / P_rest 0.9948), the redesign (if any) with mechanistic rationale, the new gate result, and the iteration budget consumed (R1, R7).
- [ ] One primary endpoint: named leg + statistic + threshold + direction + sidedness (R2). If ICC: the paired within-pair gap is the registered statistic; corpus-level ICC values carry the wave-3 instrument-range overlap (.73–.88) disclosure.

**Metrics and thresholds**
- [ ] Frozen thresholds with provenance: 0.80/0.60/0.80, ε=1e-2, B=2000, bootstrap seeds (20260819/20260821 lineage), W=12 primary, W∈{8,16} sensitivity-only, presence canonical (actual = disclosed sensitivity only).
- [ ] Kill-band predicate frozen verbatim from `e2_instrument.py::verdict()` (CI rule), with implementing file + commit pinned (R3).
- [ ] Wobble-SD amplitude: one number, pilot script + exact pilot output it derives from, re-runnable by a reviewer (R7), and the R6 post-fix certification of pilot provenance.
- [ ] Branch×leg matrix: every cell's expected verdict pre-stated; α-sensitive vs expected-blind legs marked; α=0 parity byte-checked in the test suite, not asserted (wave-3 carry-forward).
- [ ] Every ratio anywhere in output carries: point estimate, CI, band-touch flag, dual-R4 annotation; premise-side ratios are annotation-only (premise power n≈14,533 honestly dead; slope regression remains the premise's test).

**Power**
- [ ] Clause D executed with arithmetic: MDE per pre-named leg vs its wave-3 envelope (A: 0.011/0.085; ICC: ≤0.005); n pairs vs sidedness resolved (5 pairs one-sided, or ≥6 pairs); >80% power stated; per-leg event-floor arithmetic (nights × rate ≥ 20 for A, P flips, D crossings).

**VOID rules (carry-forward + new)**
- [ ] Carried: gate parity; null-night crossing cap (wave-3 value pinned); ≥20-event floor; continuity ladder ±0.10 with ladder-authoritative corpus named (R10); tautology guard (α=0 vs α=1 identical ⇒ no visibility claim).
- [ ] New: wobble-laundering (phase-lock to per-t target logging ⇒ leg VOID); sealing integrity (torn lid ⇒ seed VOID); carrier-purity (A within-pair gap outside envelope 0.011/0.085 ⇒ pair VOID); construction-null standing rule (R9); CI-golden-harness green at freeze commit (R4).

**Stopping rule and exclusions**
- [ ] Sealed n fixed at freeze; no interim looks; S4 verdicts filed blinded before S5 unblinding (G3 one-shot seals; no re-analysis after unblinding — the wave-3 procedure, kept).
- [ ] Exclusions: pilot corpora permanently excluded from sealed sets; STEP=60 trim applies to the silence-test corpus only, never wave-4 corpora; barkeep-exclusion robustness registered wherever premise ratios appear.
- [ ] Estimator freeze: generator commit + fiber flag + leg-script SHAs + frozen CI utility pinned; kl_sym and q-rule unit tests referenced by commit.

**Failure frame**
- [ ] Honest-negative text embedded verbatim (matched α-only pairs inseparable within 1–2 orders of room-draw scatter on every leg ⇒ H dies; wave-3 + wave-4 negatives file as a detection-envelope bound series — a methodological finding, not a null result).

**Parallel lane**
- [ ] Silence test: tie-break rule pre-stated, corpus n corrected (400–510 remaining), n_readers stated; remains non-blocking and annotation-grade for thermometer claims (R8).

---

## Verdict for the board

**BLOCKS-S2 items found: 3** — R1 (freeze contradicts the executed design-gate FAIL of 2026-08-22), R2 (power uncertified; 5 pairs cannot reach two-sided p<0.05), R3 (kill-band predicate ambiguous across three formulations). All three are text-level fixes plus at most one unsealed pilot re-run/certification; none touches sealed or frozen artifacts. The freeze discipline itself — sealed sidecars, blinded-first verdicts, pre-stated anti-hypotheses, honest-negative frames — is sound and should be kept exactly as wave-3 executed it. The single largest risk to the dissertation is not any one clause; it is the pattern R1 exemplifies: plan documents drafted ahead of the evidence ledger that will adjudicate them. The S2 text must cite the S1 sweep's FAIL in its own body, or the method chapter's seventh laundering becomes the eighth.

*Provenance: all documents cited above read in full this session; elephant repo read-only; no sealed, frozen, or registered artifact modified; no corpus generated.*
