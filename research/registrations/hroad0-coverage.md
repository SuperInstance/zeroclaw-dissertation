# H-ROAD-0 (Rung 1) — Coverage Registration

*Committed 2026-08-28 (AKDT), pinned before any soak data is read. Builds on research/EGOCENTRIC-LADDER.md Rung 1; schema work landed first (walks-bridge walks/2, commit 3af5824) with zero semantics held.*

## Pre-registered question

*Does the extended tape record link type + link quality for ≥95% of arrivals over a 72-hour soak, with the hash chain still verifying end-to-end?*

## Pin

- **Window:** first 72h of real (non-synthetic) traffic after this registration. Ingress hook = the walks/2 `arrival` stamp at journal ingress (road, link_quality, arrival_meta).
- **Coverage denominator:** all arrivals entering any journal/tape in the window. Legacy/unstamped rows are NOT retro-filled — they count as uncovered if they occur post-registration, honestly `unknown` otherwise (the honesty rule: unknown is honest, guessed is not).
- **Pass:** ≥95% of arrivals carry road + link_quality; sha chain verifies end-to-end (existing exporter self-check).
- **Fail (recorded, not redesigned):** coverage <95% → find the unstamped ingress paths, instrument them, re-register with the gap named. Chain break at ANY point → hard stop, integrity before coverage.

## Soak live lanes (stamp sources)

rd-tap tap rounds, rd-tit registrar loop, dissertation prototype ingress. Synthetic walks stay generator-tier and are excluded from coverage.
