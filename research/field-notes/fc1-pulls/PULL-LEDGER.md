# FIELD-CARRY-1 — Pull Ledger (A3 commit-chain)

*Per the A3 amendment: every D1 pull is committed raw and untouched BEFORE any
proxy computation runs on it. This ledger is the audit trail. Ordering authority:
ZeroClaw lane.*

## Cutoff rule

Registration commit `39afeee` landed 2026-09-03 00:02 UTC. **Only campaign_log
rows with timestamp > `2026-09-03 00:02:00` are in-window.** Earlier rows are
pre-registration and are excluded from every PASS/FAIL count (they may be
reported as excluded, never silently pooled).

## Pulls

| # | file | window | rows | drifter lines | distinct drifters | committed SHA |
|---|---|---|---|---|---|---|
| 1 | `2026-09-01.json` | 09-01 UTC (entire day) | 3148 | 89 | 88 | this commit — **EXCLUDED: pre-registration** |
| 2 | `2026-09-02.json` | 09-02 UTC (entire day) | 3130 | 79 | 78 | this commit — **post-cutoff rows: 0** (day ends 00:02Z at the cutoff; pulled for the boundary check, in-window rows: none) |
| 3 | `2026-09-03-partial-through-0410Z.json` | 00:02Z cutoff → 04:10:30Z | 549 | 17 | 17 | this commit — **first IN-WINDOW pull** |
| 4 | `2026-09-03-full.json` | 00:02Z cutoff → 17:55:23Z (day 09-03, full) | 2345 in-window of 2359 total | 59 lines | 57 arrivals (distinct) | this commit — **pull only; no computation run** |

## State after pull #4 (2026-09-03 ~18:05Z)

- In-window drifter arrivals cumulative: **74** (17 in pull #3 + 57 new in
  pull #4; overlap rows deduped by the cutoff rule, pull #4 supersedes #3's
  partial day-09-03 coverage). Well past the 6-arrival floor.
- Stratum note: of pull #4's 57 arrivals, 56 first lines are `'...'` (1
  substantive) — the absorbed stratum continues to dominate; no moment has
  recurred organically. fc1b (seeded arm) remains the designed path to an
  informative stratum.
- Proxy computation on pull #4: **NOT run** — committed raw per A3 first.
- Pull #5 attempt (2026-09-03 ~22:15Z): **FAILED, no data obtained** —
  Cloudflare D1 API auth error (code 10000; credentials worked at 18:00Z,
  evidently rotated/expired since). Nothing committed under A3 because there
  is nothing raw to commit; next pull requires fresh wrangler auth. Ledger
  continuity note only — no in-window rows were lost, they remain on the
  remote and are included in the next successful pull.

## State after pull #3 (superseded by #4 for day-09-03 coverage)

- In-window drifter arrivals so far: **17** (≥ the 6-arrival floor is reachable
  already, but pulls are partial-day and the window runs to 2026-10-02).
- Proxy computation: **NOT yet run** on pull #3 — per A3, this commit precedes
  any computation. Next lane action: run `field-carry-0-run.py` heuristics
  (frozen, unmodified) over the in-window arrivals, commit proxy values, THEN
  label engagement (blind reader, post-arrival 10-min windows), then apply the
  A2 decision rule at ≥6 labeled arrivals.
- The registration's amendment window is now CLOSED: pull #3 is post-registration
  visit data, committed before any computation. No further amendments to
  field-carry-1-forward.md are legal; only its decision rule runs from here.
