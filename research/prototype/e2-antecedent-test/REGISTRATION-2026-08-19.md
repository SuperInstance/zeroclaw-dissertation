# E2 REGISTRATION — The Antecedent Test at Power (schedule-diversified)

**Registered: 2026-08-19, before any E2 night exists, before the calibration ladder runs, before any field number is computed.** This document implements chapter 7 §7.4 (the binding E2 design) and inherits chapter 7 §7.1 standing discipline verbatim. It supersedes nothing that is already committed; where the per-reader-schema design doc (`per-reader-schema-design.md`, same date) conflicts with §7.4, §7.4 governs E2 (its S1–S5 schedule families over the SAME text sources, its seeded field-distribution roster draw). The schema doc's v:2 field definitions and its `reader_known` entry-mode flag are adopted as the instrument; its nights E–J and boombox/tender/comic persona bank remain a separate, unexecuted pre-registration and are not part of E2.

Everything below is fixed. Thresholds do not move after data exists.

---

## R1. The quantities (unchanged from §7.4)

- **Primary: the field baseline-spread-to-drift ratio** — between-reader sd of fitted baselines ÷ within-reader drift signal, corpus-sd units. The kill band is denominated in this ratio.
- **Secondary: the baseline ICC** — between-reader variance ÷ (between + within), reader × schedule two-way structure, bootstrap-over-readers 95% CI. Reported with its own CI, never substituted for the primary.

## R2. Corpus and scale

- **E2 primary nights:** `night-A`, `night-D`, `night-D-cold` (frozen v:1 artifacts, never regenerated) + six new v:2 nights: `night-S1, night-S2, night-S3, night-S4a, night-S4b, night-S5`.
- **Excluded:** `night-B`, `night-C` (byte-replays of A's schedule — zero independent schedule information; including them fabricates precision; they appear only in a labeled sensitivity variant), `night-A-repro` (determinism check), `coarse-anchor` (different room/roster class).
- **corpus_sd:** per-dial sd of `field_raw_after` over the 9 primary nights' speak events, RMS over the 7 dials. Fixed once, used by ladder (truth and estimate alike) and field alike.
- **Reading series** r_R(t): the reader-grain displaced field with attention gain — `reading_R(t) = DIAL_CENTER + g_R ⊙ (field_eff_to_reader[R](t) − DIAL_CENTER)`, `g_R = dial_weights_R / max(dial_weights_R)`. On new nights this is consumed from logged v:2 `readers` facts; on v:1 nights it is reconstructed by the premise-measurement replay (identical equations; the equality is asserted numerically on the new nights). **Presence:** a rostered reader reads all night; a cold entrant reads from their first speak onward.

## R3. Schedule families (same text sources: SEG1 warm bank, SEG2 cynical bank, DRIFTER_LINES — all verbatim from `nights_abc.py`)

| night | family | script | strata (by seq) | transitions |
|---|---|---|---|---|
| S1 | warm→cynical canonical | SEG1(20)+SEG2(20), flip@20 | [0,19] warm → [20,39] cynical | 1 |
| S2 | early flip | SEG1[:8]+SEG2, flip@8 | [0,7] warm → [8,27] cynical | 1 |
| S3 | late flip | SEG1+SEG2[:8], flip@20 | [0,19] warm → [20,27] cynical | 1 |
| S4a | newcomer entry PRE-flip | SEG1+SEG2 with drifter lines inserted after occupant indices 11,14,17,20,23,26 → cold entry at seq 12 | [0,11] warm-pre → [12,19] warm-entry → [20,45] cynical | 2 |
| S4b | newcomer entry POST-flip | inserts after 27,30,33,36,38 (first 5 drifter lines) → cold entry at seq 28 | [0,19] warm → [20,27] cynical-pre → [28,44] cynical-entry | 2 |
| S5 | no-flip control | SEG1 only (20 warm msgs) | [0,19] warm-only; null pseudo-split [0,9]/[10,19] | 0 signal (1 null) |

Distinct signal-transition columns available: A(warm→cyn@20), S1(same family, different room/cast), S2(flip@8), S3(short cynical tail), S4a(entry-in-warm; entry→flip), S4b(flip; entry-in-cynical), D(pre/post warm entry), D-cold(pre/post cold-neutral entry) — **8 distinct signal transition types across 5 families** (≥5 required).

**Protocol correction (binding):** the newcomer enters **COLD** in S4a/S4b — persona staged and engaged at first speak, NOT rostered at session open; no pre-entry acclimation (v:1 night D rostered him from open, pre-warming his vibe for 24 speaks before entry — that treatment stays frozen in the old data and is not repeated). `reader_known: false` marks the cold entries; the staged persona is declared in `session_open.staged_entries`.

**S5 is the null control:** its pseudo-transition drift is reported as the drift estimator's null level and EXCLUDED from the primary drift; a sensitivity variant including it is reported.

## R4. Roster (15 real readers; overlap ≥2 families each)

- The 7 existing personas, frozen verbatim (`nights_abc.py`): writer, poet, essayist, engineer, critic, captain, drifter.
- 8 new personas drawn seeded (seed 20260819) from the corpus field distribution, committed at creation with archetype labels, frozen in `elephant/data/e2/e2-personas.json` (sha256 `14f14cee732a71bd2a58abac4c0706696d2262e8b5743399d13db194e6fbdeb2`, drawn by `scripts/e2_personas.py`, sha256 `058024c92e8baa577012d13dae5053b78b09f5f6461ebf403993eedbc8196dfe`): barkeep(critic), singer(critic), fiddler(critic), lamplighter(captain), cartographer(critic), blacksmith(poet), tinker(poet), weaver(essayist).

Attendance (committed):

| night | roster |
|---|---|
| S1 | orig6 + barkeep, fiddler, cartographer |
| S2 | orig6 + singer, lamplighter, tinker |
| S3 | orig6 + blacksmith, weaver, barkeep |
| S4a | orig6 + fiddler, singer (+ drifter cold@12) |
| S4b | orig6 + cartographer, blacksmith, tinker (+ drifter cold@28) |
| S5 | orig6 + lamplighter, weaver |

Plus existing coverage: orig6 in A, D, D-cold; drifter in D (rostered, old protocol). Every reader spans ≥1 signal transition; every new persona appears in ≥2 families; orig6 in all families.

## R5. Estimators (both computed; primary chosen by the ladder, R6)

**Drift (shared):** per reader, per attended night, consecutive-strata-pair displacement `‖mean(readings, stratum k+1) − mean(readings, stratum k)‖ / corpus_sd`; reader drift = mean over all their signal transitions.

- **E-seg (segment-local, rule-1-compliant — schema doc §3.1):** baseline per (reader, night, stratum) cell = **median** of readings in cell. Spread: per cell, per-dial sd across readers present (ddof=1), RMS over dials, then **RMS over cells**, ÷ corpus_sd.
- **E-cont (continuity — the pre-measurement §4 estimator):** baseline per reader = mean over ALL attended readings. Spread: per-dial sd across readers (ddof=1), RMS over dials, ÷ corpus_sd.

**Class-conditional discipline (rule 2):** archetype labels per reader (above). Reported alongside the primary: (a) per-archetype mean drift; (b) the **class-residual spread** — per cell, archetype-mean baseline subtracted before the across-reader sd — and the class-residual ratio. The doctrine's premise is idiosyncratic *class-independent* baselines; the class-residual number is the premise-relevant component. The verdict band applies to the population ratio (the band's denomination); the class-residual ratio is reported in the same table, never swapped in.

**Secondary ICC:** per (reader, night): b̂ = median over the night's readings. Per dial: subtract night means (over attending readers), then σ²_within = mean over readers of across-night variance (ddof=1), σ²_between = across-reader variance of reader means (ddof=1); ICC_dial = σ²_b/(σ²_b+σ²_w); aggregate = unweighted mean over the 7 dials (per-dial table reported). Bootstrap-over-readers 95% percentile CI, B=2000.

**CIs (rule 3):** every reported ratio and ICC carries a cluster bootstrap over readers (resample readers with replacement, B=2000, seed 20260819, percentile 95%).

## R6. The calibration ladder — MANDATORY GATE before any field number

- **Rungs:** {0.0, 0.15, 0.3, 0.6, 0.9} corpus-sd. **Tolerance: |estimate − rung| ≤ 0.1 at every rung** (both estimators evaluated; CIs reported).
- **Synthetic-grounded populations (fixtures):** 15 readers drawn seeded from the field distribution (same sampler as R4), attendance template mirroring the 15 real readers, readings by replay over the SAME E2 nights (observer grain, per the pre-measurement's synthetic protocol — the room logs are not re-run).
- **Planting:** params = cast_mean + λ·(draw − cast_mean) for every parameter (λ=0 ⇒ 15 identical readers ⇒ true ratio exactly 0). λ calibrated per rung by bisection on the TRUE ratio (target ±0.005). **True baseline** b*_R = mean of R's true readings over the S5 no-flip night (the stable-room anchor — computed omnisciently; the estimator only sees what the attendance template allows). **True spread** = per-dial sd of b* across readers, RMS over dials, ÷ corpus_sd. **True drift** = same definition as R5 on true readings. **True ratio** = spread*/drift*.
- **Seeds:** rung r, repetition k: seed = 20260819 + 1000·rung_index + k; k=0 primary, k∈{1,2} stability checks. Bootstrap seed 20260819.
- **PASS rule:** the primary estimator's point estimate within ±0.1 at every rung on k=0 (stability reps reported; a stability rep outside ±0.1 is flagged but does not fail the gate). **Primary-estimator selection:** if E-seg passes, E-seg is primary (rule 1); else if only E-cont passes, E-cont is primary, flagged as the continuity estimator; if neither passes, **the ladder has failed — that is the finding of the day; no field number is filed and the estimator is rebuilt before E2's field arm runs.** A second consecutive ladder failure kills the measurement (not the premise) and forces the sentence "the field cannot currently measure its own antecedent."

## R7. Verdict (kill condition, fixed)

With the ladder passed, on the primary estimator's field ratio with bootstrap CI:

- **CI entirely > 0.6** ⇒ premise holds in the field; conditional activates; clause-1 re-run is Chapter 8 material.
- **CI entirely < 0.3** ⇒ doctrine dies by its own registration; Chapter 6 shrinks to a consistency proof.
- **CI touching the band** ⇒ indeterminate again, filed as such, WITH the power analysis; the premise is retired from claim status.
- **Kill condition on E2:** CI upper bound ≤ 0.6 (the powered estimate never clears the band), or double ladder failure.

**Power analysis (pre-committed form):** N_req = ⌈N · (h/d)²⌉ where h = CI half-width at N=15 readers and d = distance from the point estimate to the nearest band edge (0.3 or 0.6). Filed if (and only if) the verdict is indeterminate.

## R8. Prefix discipline (rule 6)

Every ladder number carries **"on fixtures"** in its sentence. Every real-reader number carries **"field."** No exceptions.

## R9. Instrument facts

- New nights are emitted with the v:2 per-reader schema (additive `readers`/`reading_of` blocks; v:1 lines unchanged; old nights never regenerated). `field_eff_to_reader` uses the pre-acclimation vibe at each speak (the vibe that drove that speak's displacement — matches the replay exactly); `lens_now.vibe_now` is post-acclimation.
- Determinism: each new night is generated once and verified by stripped-line (sans `session_id`) md5 against a re-run before commit.
- All scripts land in `elephant/scripts/` (`e2_personas.py`, `e2_nights.py`, `e2_instrument.py`, `e2_ladder.py`, `e2_field.py`); results as dated JSON beside the nights; the dated report lands in this directory.

*Registered by ZeroClaw for the committee. Chapter 7 §7.4 priors stand: 0.30 clear / 0.15 die / 0.55 indeterminate; 0.75 the ladder passes. The thresholds above will not move.*
