# Per-Reader Readings Schema (v:2) + Reader-Expansion Plan — Design

**Date:** 2026-08-19 · **Status:** design + plan (this is the deliverable the devil's pass-4 §8 demands; no elephant files were modified — the elephant repo is cited read-only) · **Owner:** ZeroClaw, for the committee's pass-5 review.

**Why this file exists.** The premise measurement (elephant commit `01fd14a`, `RESEARCH-NOTE-PREMISE-MEASUREMENT-2026-08-19.md`) measured the field's baseline-spread-to-drift ratio at **0.5599 corpus-sd — inside the devil's kill band (0.3–0.6), verdict: indeterminate**. The honest cause is data limitation: **7 real readers across only 2 distinct schedules**, and every per-reader quantity in that measurement was **replayed from the room log by a reconstruction model**, not read as a logged fact. This document specifies (1) the minimal additive log schema that makes per-reader readings *data*, (2) the concrete reader/schedule expansion that satisfies the committee's ≥10 readers × ≥5 strata-transitions discipline, and (3) the pre-registered Antecedent Test (baseline ICC / ratio) with its clear and kill thresholds. Chapter 6's promissory note ("the schema addition is the instrument the field lacks") is redeemed here, on paper, before any engine code moves.

---

## 1. The schema addition — `v:2`, optional, additive

### 1.1 Design rules (tightened from the prototype's ≤6 bullets)

1. **One optional top-level key.** All additions live under a single `readers` object on `speak` lines. Existing consumers key on known fields and ignore unknown keys, so **every existing night (v:1) replays unchanged, byte-for-byte, forever**. v:1 lines never carry `readers`; v:2 lines always do.
2. **Log facts the engine already computes; do not invent new dynamics.** The per-reader displaced field is the *single-agent reduction the engine's own charisma loop already defines* (`tapnight.py:242-253`, docstring: "for a single agent this reduces exactly to charisma_pull"); the acclimated lens is `self._vibe` (`tapnight.py:255-257`). Today these are computed and discarded. v:2 persists them at emission time.
3. **Gating.** One entry per rostered participant plus any lazy-registered speaker (`tapnight.py:482`), keyed by name. Roster membership (not `presence_mask`) is the gate, matching the premise measurement's presence convention: a rostered reader reads the room all night. `reading_of` is additionally restricted to `presence_mask` members (you read who is actually in the window).
4. **Determinism, no text, no model calls.** Everything below is a pure function of engine state + roster params (numpy-only). No message text, no embeddings, no seeds beyond the existing `vmf_fit` bootstrap. `allow_nan=False` discipline is preserved: any quantity that cannot be computed emits `null`, never NaN.
5. **No engine semantics change.** Room `field_raw_after` / `field_eff_after` / `fit` / `edge` are computed exactly as before. v:2 is a *logging* change; a session run with logging disabled is bit-identical to v:1.

### 1.2 The field list (exact)

Each `speak` line gains:

```json
"v": 2,
"readers": {
  "writer": {
    "reader_known": true,          // bool — roster persona vs cold/lazy entry
    "charisma": 0.2,               // float — logged for exactness (roster fact, cheap)
    "field_eff_to_reader": [ ... 7 floats ... ],   // reader-grain displaced field
    "lens_now": {
      "vibe_now":     [ ... 7 floats ... ],        // within-session evolving lens (acclimation)
      "weights_now":  [ ... 7 floats ... ]         // dial_weights snapshot (tunes across cycles)
    },
    "reader_fit": { "mu_hat": [ ... 7 ... ], "kappa": 12.4, "n": 8 }  // or null
  },
  ...
},
"reading_of": {                     // author's read of each presence-mask member
  "poet":   { "cos": 0.83 },        // cos between author's and member's current readings
  "writer": { "cos": 1.0 }          // (self always present; cos = 1 by construction)
}
```

Field-by-field definitions (all vectors in `DIAL_NAMES` order, 7 dials):

| field | definition | engine source |
|---|---|---|
| `field_eff_to_reader[R]` | `clamp(raw + s_R · (vibe_now_R − raw))` with `s_R = 1 − exp(−charisma_R · n_R)`, `n_R` = R's interactions count after this speak; `clamp` = per-dial `DIAL_BOUNDS` | the engine's exact single-agent reduction of `tapnight.py:242-253`, evaluated with R's own charisma and the *logged* raw field |
| `lens_now.vibe_now[R]` | R's acclimated vibe **after** this speak's acclimation step | `self._vibe[R]` post-update (`tapnight.py:255-257`) — currently evolved then discarded |
| `lens_now.weights_now[R]` | R's current `dial_weights` (constant within a night unless a mid-session `tune_participant` call fires; logging per speak makes future in-session tuning *data*) | `Participant.dial_weights` |
| `reader_fit[R]` | vMF fit over R's **own reading window**: the last W speaks' vectors `weights_now ⊙ field_eff_to_reader` (attention-weighted — the reader's private estimate, not the room's). `{mu_hat[7], kappa, n}`; `null` when n < 3 | new call to `vmf_fit` (same estimator, `vmf-mle-newton-v1`) on a per-reader window |
| `reading_of[R→P]` | `cos(field_eff_to_reader[R], field_eff_to_reader[P])` — the minimal R→P primitive: how the speaker currently reads each present member's position. (The 7-vec delta is derivable; the cos is the logged scalar.) | derived from the rows above |
| `reader_known[R]` | `true` iff R was in the session's declared roster; `false` for lazy/cold registration (the D-cold drifter case becomes first-class instead of silent zeros) | track at `_register` vs `start_session` |

`session_open` gains a descriptor (so consumers can detect semantics without sniffing speak lines): `"reader_schema": {"version": 2, "field": "field_eff_to_reader", "lens": ["vibe_now","weights_now"], "fit": "vmf-mle-newton-v1", "gate": "roster"}`.

`session_close` gains, optionally, `reader_final`: each reader's `b̂_R` = componentwise median of their `field_eff_to_reader` over the night — a convenience duplicate of what consumers can compute from speak lines; it makes a night's per-reader baseline a single greppable fact.

**What is deliberately NOT logged:** per-reader κ CIs, per-reader edges, per-reader reaction attribution, text, or embeddings. Anything derivable from the fields above stays derived; the schema logs the minimal primitive set from which the reader-delta index, the ICC, and the switch test all reconstruct exactly. Line size grows ~3–4× (≈ +25 floats/reader/speak ≈ 4 KB/speak at 7 readers; ≈ 200 KB/night) — acceptable for an append-only JSONL corpus.

### 1.3 Why log what a replay model can reconstruct

Honest answer, since the devil will ask: today's reconstruction (`scripts/premise_measurement.py`) works only because the log plus the *current* engine semantics happen to be sufficient. The schema addition converts a **model of the reading** into **the reading**:

- **Replay is engine-version-fragile.** Any future change to the charisma/acclimation update silently invalidates every reconstructed premise number; logged facts survive engine evolution.
- **Replay bakes in the replayer's model choices** (attention gain `g_R`, presence convention, drift estimator). Logged facts pin the semantics at emission.
- **`reading_of` and `reader_fit` are not reconstructible** without re-deriving the whole per-reader stack outside the engine — the exact out-of-engine modeling the deadman discipline distrusts.
- **The premise measurement stops being model-mediated.** The 0.5599 number carries a reconstruction caveat; the v:2 re-run will not.

## 2. The reader-expansion plan — ≥10 readers × ≥5 strata transitions

### 2.1 What the corpus has now

7 real readers (6 occupants + drifter), but only **2 distinct schedules**: warm→cynical (A/B/C byte-share one script) and newcomer entry (D/D-cold share one script modulo the drifter). Spread is thin on dims the cast barely occupies: corpus per-dial sd shows volume 0.0067 and panic 0.0374 nearly dead; baseline separation lives almost entirely on cynicism (critic/drifter) and mood (poet/writer). "Real reader" here means, and will mean: **a rostered engine participant with a declared persona, observed at reader grain** — distinct from the synthetic parameter-thickening the premise note ran (which stays excluded from primary numbers).

### 2.2 Cohort expansion: 7 → 14 readers (pre-registered persona bank)

Add 7 personas targeted at the *unoccupied* dial axes — chosen by a **coverage criterion** (span the 7-dial simplex at pre-declared quantiles), **not** by any feedback from the ratio. This matters: personas tuned after seeing the ratio would rig the antecedent test. The persona table below is the pre-registration; it is committed in this document before any night is generated.

| name | dial_weights emphasis | vibe emphasis | charisma | acclimation |
|---|---|---|---|---|
| `boombox` | volume 0.45, joke 0.20, presence 0.15 | volume 0.90, mood 0.40 | 0.35 | 0.20 |
| `tender` | panic 0.35, earnestness 0.30, presence 0.15 | panic 0.60, earnestness 0.75 | 0.10 | 0.30 |
| `comic` | joke_landing 0.50, mood 0.20, volume 0.15 | joke 0.70, mood 0.30 | 0.25 | 0.25 |
| `hermit` | panic 0.20, cynicism 0.25, earnestness 0.25 | mood −0.20, presence 0.25 | 0.05 | 0.10 |
| `host` | presence 0.30, earnestness 0.25, volume 0.20 | presence 0.85, mood 0.55 | 0.40 | 0.35 |
| `archivist` | earnestness 0.40, presence 0.25, panic 0.10 | earnestness 0.70, presence 0.55 | 0.12 | 0.15 |
| `skeptic2` | cynicism 0.30, joke 0.25, mood 0.20 | cynicism 0.50, mood 0.10, joke 0.35 | 0.22 | 0.25 |

(The original 7 are frozen verbatim — their parameters never change, so existing nights and all prior measurements remain valid.) Nights roster mixed casts (e.g., 4 original + 4 new) so every reader is observed in shared rooms against a common field. Nothing synthetic enters the primary analysis.

### 2.3 Schedule expansion: 2 → ≥8 distinct strata transitions

Five new night scripts in the `nights_abc.py` pattern (deterministic, lexical, fixed 40-message scripts, no model calls):

| night | transition | what it isolates |
|---|---|---|
| `night-E` | calm → panic (mid-night alarm content, TTRPG-anchor style) | the panic axis, dead in the current corpus |
| `night-F` | quiet → loud (hushed SEG1 → party SEG2) | the volume axis, dead in the current corpus |
| `night-G` | earnest → comedy (straight SEG1 → joke-dense SEG2) | joke_landing as the flip dial, not a side effect |
| `night-H` | slow cynicism ramp (no segment flip — continuous gradient) | drift vs step: separates gradual displacement from event displacement |
| `night-I` | warm-newcomer entry + `night-J`: charismatic-exit (a high-charisma occupant leaves mid-night) | entry and its mirror; charisma direction, not just magnitude |

Distinct strata transitions after expansion: warm→cynic (A–C), pre/post-newcomer-cold (D), calm→panic (E), quiet→loud (F), earnest→comic (G), ramp (H), pre/post-newcomer-warm (I), pre/post-exit (J), plus cross-night pairs across *different* schedules (same reader, night boundary) — ≥5 required, ≥8 delivered. Each transition is experienced by every rostered reader present, so drift becomes a **within-reader quantity estimated across ≥5 transitions**, not a two-stratum average.

### 2.4 Minimum viable addition (the honest floor)

If the full 5-night/7-persona build is too heavy, the **MVE** that can still move the ratio out of the band:

- **+3 personas** (one new night each of: `boombox` on night-E, `tender` on night-E, `comic` on night-G) → **10 readers**;
- **+2 distinct schedules** (night-E calm→panic, night-G earnest→comic) → transitions = warm→cynic, pre/post-newcomer (existing) + calm→panic, earnest→comic, + cross-night E↔G pairs → **5 distinct transitions**;
- **v:2 logging on** for both new nights.

That is 2 new scripts + 3 persona dicts + the logging change: roughly a day of harness work after the schema lands. Power sizing (the n<100 interval rule): with 10 readers × 5 transitions, cluster-bootstrap the ratio over readers; **the CI half-width must be ≤ 0.10 corpus-sd (a third of the band width)** for a decisive verdict. If the pilot MVE run's CI is wider than that, escalate to the full 14 × 8 design rather than publish an indeterminate number twice.

**What moves the ratio, stated honestly.** The current 0.5599 sits at the band's top edge; it needs either between-reader spread ↑ or within-reader drift ↓. Spread grows honestly from readers occupying the dead axes *if* those axes move during the night (hence E/F/G must actually exercise volume/panic/joke — a dim nobody moves cannot separate baselines in sd units). Drift shrinks honestly under subtler transitions (the ramp night H is deliberately gentler than the warm→cynical chasm: SEG1→SEG2 displaces ~0.82 corpus-sd because the script is a maximal contrast). Both levers are properties of reader diversity and schedule design — declared up front, not tuned to the outcome.

## 3. The Antecedent Test — pre-registered design

**Runs once v:2 per-reader logs exist, on the expanded corpus, before any further synthetic work** (the rival's rule: the marginal value of one real-reader ICC is the dissertation). Script pattern: `scripts/premise_measurement_v2.py` in the dissertation's prototype dir (read-only against nights, numpy-only, seeded).

### 3.1 Quantities

- **Reading series.** `r_R(t) = field_eff_to_reader[R]` at each speak (logged fact; no reconstruction model).
- **Baselines.** `b̂_R = median_t r_R(t)` within a stratum (segment/night-schedule cell). **Segment-local baselines only** — the rival's discipline fix: no shared estimator between predictor and target, ever (the head-saga rule applied here).
- **Primary statistic (the devil's registration).** In corpus-sd units (per-dial sd of `field_raw` over the full corpus, RMS over dials):
  - between-reader spread `σ_b = sd over readers of ‖b̂_R − grand_mean‖` (the premise note's §4 estimator);
  - within-reader drift `σ_w = mean over readers of stratum-to-stratum displacement `‖mean-stratum − mean-prior-stratum‖`;
  - **ratio = σ_b / σ_w**.
- **Secondary statistic (the rival's unit).** ICC on baselines: fit a one-way random-effects model to per-reader-per-night `b̂_R` estimates; `ICC = σ²_between / (σ²_between + σ²_within)` where `σ²_within` is test-retest variance (same reader, different nights sharing a schedule, plus repeated windows). Reported with its own CI, never substituted for the primary.

### 3.2 Pre-registered thresholds (fixed now, before data exists)

| verdict | primary: ratio (corpus-sd) | equivalent ICC† | action |
|---|---|---|---|
| **CLEAR** (premise holds) | **ratio > 0.6** | ICC > 0.265 | premise prefix lifts where earned; re-run clause 1 + kill comparison on the real corpus at deadman discipline |
| **KILL** (doctrine dies by its own registration) | **ratio < 0.3** | ICC < 0.076 | second-order object demoted to fixture-only consistency proof; Chapter 6 language shrinks accordingly |
| **INDETERMINATE** | 0.3 ≤ ratio ≤ 0.6 | between | corpus still too weak; MVE → full design escalation, or the dissertation carries the fixture prefix permanently |

† `ICC = r²/(r²+1)` under the same variance decomposition; both are reported but **the ratio is the registered primary** (the devil owns the band; the rival owns the ICC — each gets their number, one verdict).

Decision rule details, pre-registered: point estimate decides the verdict; **cluster bootstrap (resample readers, 10k draws, 95% CI) is reported and must be quoted with the verdict**; if the CI straddles a threshold boundary, the verdict is the point estimate *and* the straddle is stated in the same sentence. Sensitivity variants (vs-own-baseline drift estimator, robust medians, drifter-in/out) are reported in an appendix table, never in the abstract.

### 3.3 What clearing buys, and what it does not

Clearing the band activates the conditional for the measurement corpus and licenses the follow-on the devil specified: re-run clause 1 (blind drift-class discrimination) and the kill comparison (reader-delta vs the four first-order variants *including the median-trick cell*) on real per-reader logs at deadman discipline, plus the Switch Test (already prototyped in `research/prototype/switch-test/`). It does **not** license "crown" language (devil §7), does not touch corrigibility claims (rival §2.7), and carries the corpus-prefix everywhere: *proven in fixtures, measured in the measurement corpus, unproven for human readers*. The corpus is an engineered world; the antecedent test settles the premise **for that world** — the same honesty, one level up.

## 4. Honest scope — small schema change vs harness work vs rewrite

| item | class | effort | risk |
|---|---|---|---|
| `readers`/`reading_of` emission in `_speak_event` | **small schema change** — additive, engine already computes every quantity | ~60–100 lines in `tapnight.py` + tests; all facts exist at speak time except `reader_fit` (one extra `vmf_fit` call per reader per speak — W=8 window, numpy, negligible) | none to v:1 nights (immutable); replay tools ignore unknown keys (verified: `reader_delta.py` keys on specific fields) |
| `reader_schema` descriptor, `reader_final` | small | trivial | none |
| new night scripts E–J + persona bank | **harness data/config**, `nights_abc.py` pattern — no engine change | ~1 day total, deterministic, minutes to run | corpus heterogeneity grows; premise analysis must pre-declare which nights enter the primary set (A–J all in; `coarse-anchor` and `A-repro` stay excluded per the premise note) |
| `night-A-repro` determinism check | guardrail | none | **pin it**: the byte-replay check must keep running against frozen v:1 lines; never regenerate v:1 nights with a v:2-emitting harness, or the determinism check silently breaks |
| mid-session `tune_participant` capture | already supported by `weights_now` logging | zero | none |
| cross-cycle nights (multi-night roster persistence) | **small harness feature** — `load_settings` exists; needs a runner flag | ~half day | not required for the antecedent test; defer |
| per-reader PersonalElephant presets as first-class session readers, heterogeneous W, probabilistic readers | **engine work, not needed** — the single-agent reduction + logged lens fully instruments the premise | — | explicitly out of scope; no rewrite is required for the owed measurement |

**Risk register (what could go wrong):**

1. **Replay breakage via regeneration.** Mitigated as above: v:1 nights are frozen artifacts; v:2 applies to new nights only; a `reader_schema` flag on `session_open` lets any consumer branch safely.
2. **Persona-drawing rigging the antecedent.** Mitigated by pre-registration: §2.2's table is committed *in this document* before generation; any post-hoc persona edit must be logged as a new registration with justification.
3. **Ratio drops below 0.3 under reader grain.** Possible and honest: the reconstruction model that produced 0.5599 makes modeling choices a native log may not confirm. That is the point of the instrument — the number is the number, and the kill fires by registration.
4. **Log size / NaN discipline.** ~4 KB/speak, `allow_nan=False` enforced; all null-able quantities null out cleanly (D-cold-style unknown readers emit `reader_known: false` with neutral-parameters fields rather than silent zeros).
5. **Definitional drift between premise-measurement estimators.** The v:1 measurement's estimators are preserved as sensitivity variants; the primary is re-specified here (§3.1) and frozen before v:2 data exists.

## 5. Execution order (for when the committee green-lights)

1. Land v:2 emission in the elephant harness behind `reader_schema` (small change; v:1 default for old scripts).
2. Commit persona bank (§2.2 verbatim) + night scripts E–J (§2.3) as pre-registration; freeze `premise_measurement_v2.py` with thresholds (§3.2) *before* generating nights.
3. Generate nights (MVE first: E + G with 3 new personas → 10 × 5; escalate to full 14 × 8 if the CI is indecisive).
4. Run the Antecedent Test; publish ratio + ICC + CIs + sensitivities; one verdict sentence per registered rule.
5. If cleared: re-run clause 1 / kill comparison / Switch Test on real logs at deadman discipline (phase 2, separately registered).

## Reproduce (nothing yet — design stage)

```
# after implementation:
python3 elephant/scripts/nights_expanded.py        # nights E–J, v:2
python3 research/prototype/premise_measurement_v2.py   # ratio + ICC + CIs, read-only
```

---

*Filed 2026-08-19 from the dissertation side. One design document written; the elephant repo was read, never touched; the persona table and thresholds above are pre-registrations, not results. The stadium's field is now surveyed and staked — build order attached.*
