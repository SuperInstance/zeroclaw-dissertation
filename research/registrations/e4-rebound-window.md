# E4 — Rebound Test: Window-Start Registration

*Committed at dispatch, before any partial data is read. No window shopping. (Ch7 §7.6.)*

## Registration (dated)

- **Window start (dispatch date):** 2026-08-19 (AKDT)
- **Window end:** 2026-09-18 (30 days)
- **Extension rule (pre-registered, fires once only):** if the 30-day CI straddles 0.15, extend to 60 days (end 2026-10-18), then settle whichever way the number points.

## Metric (fixed here)

- **Rate** = corrections ÷ forward commits over the window, computed per repo per day.
- **Dormant exclusion:** a repo with < 5 commits in the window is dormant and excluded.
- **CI:** bootstrap over repos and days, 95%.

## Threshold / deadman

- Dormant-excluded rate **> 0.15** ⇒ the 0.104 "fixed point" was a denominator artifact; **flooding, not settling** becomes the permanent sentence; the convergence claim dies.
- Rate **≤ 0.15** with corrections-per-day flat-or-down ⇒ the rebound falsifier fails to fire; the convergence condition gets its first honest, uncontaminated reading.

## Context (why this exists)

Ch6 §6.3(2) recorded: corrections/day rose 73% (11.6 → 20.1); the 74% rate decline is fully attributable to a 4.8× forward-commit surge (denominator held fixed ⇒ rate rose to 0.497); biggest corrector went dormant, second-biggest worsened (0.649, trending up). This window measures the rebound: when forward commits normalize, does the rate surface above 0.15 (flooding) or not (settling)?

## Measurement duty

Recompute at window end from git history of the fleet repos. Nothing to run at dispatch — this file is the clock.
