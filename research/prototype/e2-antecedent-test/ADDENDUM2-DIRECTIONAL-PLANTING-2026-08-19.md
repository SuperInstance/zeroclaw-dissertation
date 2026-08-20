# E2 ADDENDUM 2 — Ladder attempt 2: band rungs recovered; rung 0.9 needs a directional planting family

**Filed: 2026-08-19, after ladder attempt 2, BEFORE ladder attempt 3 and before any field number.** Attempt 2's raw results: `elephant/data/e2/e2-ladder-attempt2.json`. No field number has been computed at any point in this sequence; every addendum responds to fixture-side planting/construction obstacles only.

## B1. Attempt 2 result (canonical presence)

On fixtures, with canonical presence (addendum 1's rebuild): every rep of rungs **0.0, 0.15, 0.3, 0.6 recovered within ±0.1 by BOTH estimators** (E-seg max |err| 0.087; E-cont max |err| 0.094) — the entire kill band [0.3, 0.6] and both edges below it are validated. Rung 0.9 was **unplantable** by both registered families (λ-family ceiling 0.476–0.548 for reps 0/1 even at λ=12; λ_vibe ceiling ≈ 0.11), so the attempt-2 gate verdict is formally FAIL — but the failure mode is planting-construction, not estimator recovery, and the two registered failure concepts differ. This addendum separates them honestly rather than letting a construction ceiling masquerade as (or mask) a calibration failure.

## B2. Diagnosis: why 0.9 is hard to plant (a model-space property, on fixtures)

1. **Native-vibe idiosyncrasy acclimates away.** A reader's vibe relaxes toward the room field at their acclimation rate every speak; by mid-night the native-vibe component of readings has decayed. Vibe-only planting (addendum 1's λ_vibe) therefore saturates at ratio ≈ 0.11: the durable between-reader baseline differences live in the **gain structure** (attention weights), which does not decay.
2. **Gain spread amplifies drift.** Gains multiply both the stable deviation of the room from center (→ baseline spread) and the schedule's strata displacement (→ drift). For field-distribution-shaped draws the ratio is geometrically bounded ≈ 0.5–1.0 (observed ceilings 0.476 / 0.548 / 0.998 across reps).
3. **The corpus geometry is asymmetric.** Computed from the logs: per-dial stable deviation δ (warm stratum mean vs dial center) and flip displacement Δ (cynical vs warm): mood δ=0.933, Δ=0.067 (ratio 14.0); earnestness δ=0.454, Δ=0.067 (6.8); cynicism δ=0.000, Δ=0.953 (0.0); joke_landing 1.65; presence 0.55. The flip lives almost entirely on cynicism; mood/earnestness are high-deviation, low-displacement dials. A population whose gains sit on high-δ/low-Δ dials exhibits large baseline spread with small drift — the decoupling the λ-ray cannot produce.

## B3. Planting family 3 (directional-gain), registered

For any rung the λ-family cannot plant within λ ∈ [0, 12]: plant via **λ_dir ∈ [0, 1]**, bisected on the canonical truth (target ±0.005):

- rank dials by δ_d / max(Δ_d, 0.05), restricted to δ_d > 0.08 (top-2 = mood, earnestness on the current corpus — recomputed deterministically from the logs at run time, committed in the results);
- the 15 readers alternate between two gain-camps: w(λ_dir) = (1−λ_dir)·cast_mean_w + λ_dir·(0.8 mass on the camp's dial), renormalized;
- each reader's vibe on their camp dial is pushed toward the warm side of that dial (toward the stratum-mean value, plus a λ_dir-scaled offset in the stable direction, clamped to bounds); all other dials at cast mean;
- charisma/acclimation at cast mean.

Probe (on fixtures): ratio sweeps monotonically 0.000 → 2.322 across λ_dir ∈ [0, 1]; rung 0.9 plants near λ_dir ≈ 0.3. This family is explicitly OUT of the field distribution's shape — its populations are fixture constructs for estimator validation at a known truth, labeled `planted-via-directional` in the results, and they never enter the field number.

λ_vibe (addendum 1's family) is retired: structurally capped by acclimation (B2.1).

## B4. Attempt-3 pass rule (thresholds unchanged)

Every rung, rep 0: |estimate − rung| ≤ 0.1, E-seg-canonical primary candidate, E-cont-canonical continuity; planting order per rung: λ-family [0, 12] first, directional family [0, 1] second. PASS ⇒ field arm runs with the passing estimator. FAIL ⇒ second genuine recovery failure ⇒ the measurement is killed ("the field cannot currently measure its own antecedent"), no field number filed.

## B5. Registered context for the field verdict (a prediction, fixed before the field run)

The B2 geometry bounds what the real cast can express: the real readers' gains are field-distribution-shaped, so the field ratio is expected inside the constructible cone (≲ 1.0; the λ-family cone for real-shaped draws tops out ≈ 0.5–0.85). A CI-entirely-above-0.6 clear is therefore at the edge of what this world's parameter space can produce — registered now so that a near-miss clear is read as the geometric boundary it is, not as a sampling accident.

*No threshold moves: rungs {0.0, 0.15, 0.3, 0.6, 0.9}, tolerance ±0.1, kill band [0.3, 0.6], verdict rules, power analysis, and prefix discipline all stand as registered.*
