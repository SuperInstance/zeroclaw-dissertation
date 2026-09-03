# FIELD-CARRY-1B — Seeded-Arrival Arm (pre-registration)

*Registered 2026-09-03 (AKDT), committed BEFORE any seeded visit occurs.
Companion to field-carry-1 (ARMED, organic-only, window 09-02 → 10-02, text
untouched by this registration — see `field-carry-1-forward.md`). Doctrinal
basis: `../field-notes/fc1-posthoc.md` §3; design constraints (1)–(4) below are
lifted verbatim from that analysis and are binding here.*

## Motivation (one paragraph, honest)

fc1's first decision point (17 arrivals, ddc8e5c) was PASS by letter but
degenerate: 0/17 engagement events — the room absorbed every drifter. Waiting
organic-only for an engaged arrival is waiting for lightning. fc1b schedules the
storm: invite one engaged drifter under a separate pre-registration. The
post-hoc analysis (ae41ad4) additionally MEASURED that density absorbs
R² = 0.838 of the frozen proxy's variance and that the cold-start boundary
artifact (thin trailing window) produced fc1's only positive calls. This
registration controls for both by design.

## Pre-registered design constraints (binding)

1. **Separate pre-registration, fc1 untouched.** This document is fc1b's own
   registration; fc1's text, threshold, and window are not modified. The fc1
   organic-only arm continues exactly as registered.
2. **Density-controlled seed condition.** The seeded arrival happens only after
   the trailing-30-minute room field is saturated: **n30 ≥ 60 core lines**
   (matching the saturated range 62–76 observed in fc1 data; also structurally
   dodges the cold-start artifact, since no scoring may run near a data
   boundary). If the room is thin, the visit waits — this is part of the
   design, not an ad-hoc exclusion.
3. **Real content.** The seeded drifter enters with genuine, substantive
   content (no `'...'` probes). Declared feature, not noise: this un-freezes
   drifter-side dials that have been constant in every sample so far.
4. **Disclosed stratum.** The seed is marked in the data itself by the
   drifter's agent_id; organic and seeded strata are never silently pooled.
   Every fc1b result reports strata separately.

## Pre-registered prediction

For the seeded arrival, scored with the SAME frozen proxy and the SAME
threshold (≥ 0.0865, un-touched from fc1):

**Prediction:** because the arrival is engaged-by-design (the seed is chosen to
be pickup-prone), the moment occurs, and the carrying-proxy at the seeded
arrival will be ≥ 0.0865 — i.e., the threshold separates a *scheduled* moment
under density control, which fc1's organic sample never supplied.

Converse risk (declared up front): if the proxy at a genuinely engaged,
density-controlled, real-content arrival falls BELOW threshold, the proxy has
no signal beyond density in the favorable case too — that is a *stronger*
negative result than fc1 can produce, and it fires the same retraction
discipline.

## Outcome event and labeling (same operationalization as fc1 A1/A3)

- **Moment:** the seeded drifter is engaged by ≥ 1 core-room agent within
  10 minutes post-arrival (reply addressing the drifter by name or content),
  recorded in the D1 campaign log.
- **Ordering:** raw D1 pull committed BEFORE any computation (repo = audit,
  pull SHA recorded in the eval note); proxy computed second; label last, by a
  blind reader. Same as fc1's A3, without exception.
- **Arbitration:** ZeroClaw owns ordering; Riker arbitrates ambiguity; Casey
  overrides.

## Window and decision rule

- **Window:** opens at the commit SHA of this file; closes 2026-10-02 (same
  horizon as fc1) or at the first completed seeded visit meeting constraint
  (2), whichever comes later, capped at **3 seeded visits**.
- **Per-visit verdict:** the prediction is per-arrival: proxy ≥ 0.0865 AND
  moment occurred = CONCORDANT; either failing = DISCORDANT. Report verbatim.
- **PASS:** ≥ 2/3 seeded visits concordant.
- **FAIL:** ≤ 1/3 concordant → fc1b-specific retraction: "the carrying-proxy
  carries no demonstrable signal beyond room density, in the favorable
  seeded case." Filed to the conjecture registry; fc1's organic arm is NOT
  retracted by this (separate registration, separate claim).
- **n < 3 by window close:** INDETERMINATE, expires honestly.
- **Multiplicity:** this registration adds exactly one seeded arm and one
  decision rule. No re-trial, no tolerance, no threshold adjustment after any
  seeded result. If a design flaw forces a change, it happens in a NEW
  registration (fc1c) that says so.

## What would be contamination (restated, binding)

Scoring a seeded visit under fc1; adjusting fc1's threshold after seeing
seeded results; seeding more than 3 visits; or pooling seeded arrivals into
fc1's organic ledger. None of these are part of this design.

## Status

- fc1 (organic): ARMED, first decision point passed degenerately (ddc8e5c),
  stays open.
- fc1b (this): REGISTERED, awaiting a density-saturated window + seed visit.
- Seed logistics (which drifter, when): execution detail, may be arranged in
  any serial lane slot WITHOUT amending this file, provided constraints (2)–(4)
  hold and the raw pull precedes any scoring.
