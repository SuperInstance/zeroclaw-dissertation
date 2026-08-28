# SILENCE-TEST — Gap-Filler Experiment (S2→S3 Window)

**Author:** Extracted from STATUS-2026-08-28 (section 4, gap-filler candidate)  
**Status:** Registered, runnable, pre-approved for parallel execution  
**Corpus Constraint:** STEP=60 sessions excluded (registered 2026-08-19)  
**Date Registered:** 2026-08-19  
**Scheduling:** Slot between S2 freeze and S3 generation (parallel, non-blocking)

---

## Purpose: Falsify the "Measuring the Clock" Frame

**The hermes objection:** The room-field thermometer and the edge-log apparatus might be measuring time structure, not room behavior. If moments correlate with session silence (STEP intervals, gaps in conversation), then the apparent room-shift signature is just an artifact of when people stop talking — not a property of the room itself.

**The silence test:** Run the same room-field and edge-log machinery on a corpus of sessions deliberately *trimmed at STEP=60* (excluded) — sessions where silence intervals ≥60 seconds are removed from the record. If the apparatus "measures the clock," it will collapse when clock-like structure (silence intervals) is removed. If it measures room, it will persist (or show only time-local changes, not apparatus-level failures).

---

## Corpus Design

### Source Data
- **Base:** Tap corpus (field data, epochs where moments occurred, 2026-08-19 baseline)
- **Constraint:** STEP=60 exclusion rule — remove any session with silence intervals ≥60 seconds
- **Expected size:** ~15–20% reduction from Tap corpus (estimate: 80–120 sessions remain from original ~500–600)

### Rationale for STEP=60 Exclusion
- Sessions with long silences are presumed to have maximal "clock structure" (clear temporal separation, frame-like boundaries)
- Removing them removes the most obvious time-domain artifacts
- If apparatus still detects room shifts in the trimmed corpus, time structure is not the generator

### Registration Details
- **Registered:** 2026-08-19, before any wave-3 results were filed
- **Fix:** STEP=60 threshold is frozen (not curve-fitted to results; this is a pre-registered cutoff chosen for construct validity, not post-hoc optimization)
- **Seal:** Trimmed corpus is generated fresh from Tap records using the STEP=60 rule; no hand-curation of "bad" sessions

---

## Apparatus & Measurements

**Machinery: Identical to Tap corpus run**
- Room-field vMF (μ̂, κ) from edge-log dials
- Edge-log per-window fits (order-of-arrival, presence masks)
- Reader-delta baseline-relative drift (ICC post-hoc, mean-shift model)
- Registered collapse leg (P_trans < 0.5×P_rest)

**Scope: Tap moments only**
- Do not cross-validate to other field corpora (preserve moment-class integrity)
- All moment moments × non-moment windows analyzed under Tap's original protocol
- Thresholds: carry wave-3's 0.80/0.60/0.80, ε=1e-2

---

## Verdicts

### Pre-Stated Success Conditions (Any One Suffices)

1. **Apparatus Persistence:** Room-field κ in the trimmed corpus is ≥90% of Tap corpus κ (noise floor / dial-set variance unchanged → apparatus is robust to silence removal)

2. **Collapse Leg Unchanged:** P_trans in trimmed corpus still separates moment vs. non-moment windows with ≥80% precision (collapse signature survives silence trimming → time structure is not the generator)

3. **Reader-Delta Stability:** ICC (mood, volume, earnestness, presence) in trimmed corpus ≥0.70 (reader baseline-relative regimes persist → moment frame, not temporal frame, drives drift)

### Pre-Stated Failure Conditions (Any One Voids)

1. **Apparatus Collapse:** Room-field κ in trimmed corpus <60% of Tap corpus κ (suggests apparatus was artifact of silence structure, not room dials)

2. **Collapse Leg Dies:** P_trans becomes ≤50% precision on moment/non-moment distinction in trimmed corpus (time structure was load-bearing for the signature)

3. **Reader-Delta Breaks:** ICC <0.50 in trimmed corpus (reader's baseline drift was an echo of silence patterns, not independent regimes)

### Interpretation Frame

**If success:** The silence test is a "clean negative" — it rules out the time-structure confound. The finding is publishable as: "Apparatus measurements persist when temporal silence intervals are excluded; time structure is not a necessary condition for room-field or reader-delta signatures."

**If failure:** The silence test is an "honest negative" — it bounds apparatus applicability. The finding is: "Room-field apparatus and reader-delta regimes are sensitive to conversation structure (silence patterns); field data must be pre-processed to remove long-quiet sessions, or apparatus applicability is limited to high-engagement contexts (e.g., Bar Rail, not Office Silence)."

Either outcome is a methodological contribution; neither is a null result.

---

## Timing & Blocking

### Placement in Wave Schedule
```
S2 Freeze (wave-4) locked ─────────┐
                                    │
                  S2→S3 Window: Run silence-test ◄─── PARALLEL, NON-BLOCKING
                                    │
                             (Gap-filler, 3–5 days)
                                    │
S3 Generation (wave-4 corpora) ─────┘  (begins immediately after S2 lock)
```

### Why Non-Blocking?
- Silence-test does not consume sealed wave-4 corpora
- Silence-test does not depend on S2 freeze outcomes
- Silence-test uses Tap field data (already complete, 2026-08-19)
- S3 generation can proceed in parallel without waiting for silence-test verdict

### Gate Condition for S4
- If silence-test verdict (success or failure) arrives before S4 analysis begins, include it in the S4 report as a "concurrent validation" or "methodological bound"
- If silence-test is still running at S4 lock, file it as a separate S4-adjacent report (does not block S4 unblinding)

---

## Void Rules & Integrity Checks

### Corpus-Level Voids
- [ ] If any session removal violates the STEP=60 rule (e.g., ad-hoc exclusion of "noisy" sessions), the trimmed corpus is VOID
- [ ] If silence-interval thresholds are changed post-hoc (e.g., STEP=50 or STEP=75 substituted after initial trim), the analysis is VOID for all reinterpretations
- [ ] If Tap corpus records are modified between silence-test registration (2026-08-19) and trimming run, the trimmed corpus is VOID

### Apparatus Voids
- [ ] If vMF machinery differs from Tap baseline (different κ estimator, different window size, different dial-set), the comparison is VOID
- [ ] If reader-delta model differs from Tap ICC protocol, ICC comparison is VOID
- [ ] If collapse-leg definition differs from wave-3's P_trans rule, leg-level verdict is VOID

### Transparency Voids
- [ ] If STEP=60 threshold was curve-fitted to silence-test results, the verdict is VOID (this is a pre-registration check: was the rule chosen before or after running the test?)
- [ ] If multiple STEP thresholds are tested (STEP=30, STEP=60, STEP=90) and results cherry-picked, all verdicts are VOID

---

## Deliverables

### Phase 1: Corpus Trimming (1–2 days)
```
Input:  research/corpora/tap-full-2026-08-19.jsonl
        (original Tap sessions, 500–600 records)

Rule:   STEP=60 exclusion (remove sessions with silence ≥60 seconds)

Output: research/corpora/tap-silence-trimmed-STEP60-2026-08-28.jsonl
        (trimmed corpus, ~400–480 records)
        + audit log (sessions removed, reason, STEP-interval distribution)
```

### Phase 2: Apparatus Rerun (3–5 days)
```
Input:  tap-silence-trimmed-STEP60
        wave-3 vMF & edge-log config (frozen from wave-3 S5)

Output: silence-test-verdicts-2026-08-28.json
        {
          "room_field_kappa_trim": <float>,
          "room_field_kappa_tap": <float>,
          "kappa_persistence_%": <float>,
          "p_trans_precision_trim": <float>,
          "p_trans_precision_tap": <float>,
          "icc_mood": <float>,
          "icc_volume": <float>,
          "icc_earnestness": <float>,
          "icc_presence": <float>,
          "verdict": "SUCCESS | FAILURE",
          "frame": "clean negative | honest negative"
        }
```

### Phase 3: Report (1 day)
```
Output: research/SILENCE-TEST-RESULTS-2026-08-28.md
        (one-page verdict, metrics, interpretation)
```

---

## Success Metrics Summary

| Metric | Success Threshold | Failure Threshold | Void Condition |
|--------|-------------------|-------------------|-----------------|
| Room-field κ persistence | ≥90% of Tap | <60% of Tap | Different κ estimator used |
| P_trans precision (trimmed) | ≥80% moment/non-moment | ≤50% precision | Different window size used |
| ICC (any subscale) | ≥0.70 | <0.50 | Different ICC protocol used |
| STEP=60 rule freeze | Pre-registered, fixed | Post-hoc curve-fit | Threshold changed mid-run |

---

## Relationship to Wave-4 S2 Freeze

**Non-blocking gate logic:**
- Silence-test and wave-4 S2 are orthogonal (different data, different apparatus, different verdicts)
- Silence-test does not consume S2-freeze decisions
- If silence-test reveals apparatus failure, it is a *methodological bound* (concurrent with wave-4, not a blocker)
- If silence-test succeeds, it is a *validation* (concurrent with wave-4, an independent replication)
- Recommend: publish silence-test as an appendix to wave-4 S4 report or as a separate "methodological validation" paper

---

## Honest-Negative Frame (Silence-Test Version)

**Embedded assumption:** We registered that time structure (silence intervals) could be a confound before we knew the results. Running the test *despite expecting to pass* is the honest move. If we fail, the failure is pre-registered and disclosable without it being a "gotcha" — it is a calibration bound on the apparatus, exactly as wave-3's honest negative was a bound on α-detectability.

**Publication path if failure:** "Apparatus Sensitivity to Conversation Structure: A Methodological Bound on Room-Field Thermometry" (one-page methods + results, filed as supplementary findings).
