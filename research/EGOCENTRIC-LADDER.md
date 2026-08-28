# Egocentric Experiment Ladder

*Lucineer, 2026-08-28. Operationalizes CHARTER.md + CHARTER-AMENDMENT-1.md per EGOCENTRIC-FRAMING-MEMO.md. Ordered cheapest-first; rungs 1→3 are strictly sequential, rungs 4–5 are parallelizable, rung 6 needs one of them as its subject.*

**Ground truth (probe 2026-08-28): arrival-path/link-quality fields exist in NO current journal.** The memo's "harvest existing tapes" shortcut is dead until instrumentation lands. Instrumentation is rung 1, not rung 0. Nothing below analyzes data that does not exist.

**Commission discipline (EILEEN doctrine):** every rung carries one pre-registered predicate, hash-pinned in `research/registrations/` BEFORE build starts. One predicate per rung. No post-hoc re-tuning; a failed gate is a recorded result, not a redesign.

---

## Rung 1 — H-ROAD-0: arrival-path instrumentation

**Pre-registered question (pin before build):** *Does the extended tape record link type + link quality for ≥95% of arrivals over a 72-hour soak, with the hash chain still verifying end-to-end?*

**Build:** tick-tape schema extension at the ingress hook, wherever messages enter a journal. New fields: `link_type` (enum: `ble|wifi|espnow|tcp|rest|human|paper`), `link_quality` (radio: RSSI/PER; app: latency+loss bucket), `arrived_epoch_ms`, `seq_in_channel`. Writer-side only. Zero semantics downstream: no renderer reads these fields, no field-state computation consumes them, nothing changes behavior. This is a thermometer install, not an experiment.

**Measures:** field coverage rate, chain integrity, writer throughput overhead.

**Decision gate:** ≥95% coverage, chain verifies, throughput regression <5%. Below 50% coverage or any chain break → fix and re-soak; no analysis on partial data. 72h clean soak starts the clock for Rung 2.

**Effort:** 1–2 days code + 3 days soak.

## Rung 2 — PATH-HABIT-7: one week of baseline traffic

**Pre-registered question:** *After 7 days, does per-sender path selection show a stable habitual distribution (KL divergence between the last 48h window and the full prior window < 0.15 for senders with ≥100 arrivals)?*

**Build:** analysis script over the instrumented tapes. Per-sender channel histograms, time-of-day splits, quality distributions. Output: per-sender "habit profile" and the base rates needed for Rung 3's power analysis. Explicitly NO field-state correlation here — that belongs to H-ROAD-1's own registration; peeking early poisons it.

**Measures:** stationarity of path habits; operational definition of "path deviation" (any arrival on a channel with prior probability < 0.2 for that sender, at that hour) — this definition is frozen as part of the registration.

**Decision gate:** ≥5 senders with ≥100 arrivals and stable distributions → proceed. Traffic too thin → extend window to 14 days or add a load-generating cell. Do NOT relax the deviation definition to manufacture events.

**Effort:** 1 day scripting + 7 days wall clock (overlaps nothing; starts after Rung 1 soak passes).

## Rung 3 — H-ROAD-1: the exogenous-channel test

**Pre-registered question:** *Does path-habit deviation predict field-state change within a fixed window τ=10min better than payload valence does?* Pinned: P(field-state change | deviant-path arrival) − P(same change | habitual-path arrival) > 0 at pre-set α=0.05, permutation null via sender-paired shuffling; the same contrast computed on payload valence as the comparison instrument. Kill-band analog: if the shuffled null produces the observed lift in ≥20% of resamples, the effect is chance.

**Build:** pairing script — Rung 2 deviation events × existing field-state deltas; permutation test; valence contrast from payload features already on tape.

**Measures:** co-occurrence lift vs. chance. This is the memo's BLOCKER-1 shot: a physical fact about the world (which road carried the message) as an anchor independent of the dials.

**Decision gate:** pass → the dissertation has its external validity anchor; wave-4 registration may cite it. Land in the kill band → arrival-path is demoted to descriptive metadata, memo §1 is recorded as falsified, ladder continues (Rungs 4–6 don't depend on it). No τ re-tuning, no second contrast.

**Effort:** 2–3 days analysis.

## Rung 4 — PAPER-QUILT: the pencil client

**Pre-registered question:** *Can a human with a printed grid and pen answer ≥8 of 10 "what changed since tick X" queries about their own cell correctly, with no digital assistance, using only hand-producible receipts?*

**Build:** printed grid sheet (rows = cells, columns = ticks), pen, and a receipt grammar sized to a hand: what a hand can actually produce is `(cell-id, tick, initials, 4-hex digest, arrow to linked cell)`. Initials + date = signature (weak receipt, honest about its weakness). Copy-paste receipts: when the human transcribes a payload digest between two digital quilts by hand, that crossing is logged as a `human` link type — the slowest, most subtext-rich transport. Canvas side: an adapter cell that (a) renders outgoing queries onto the paper format and (b) ingests hand-marked responses — asking the paper what changed means diffing the returned grid against the ledger, treating illegible or absent marks as **offline grace, not error**.

**Measures:** receipt loss rate, end-to-end latency (expected: hours), query fidelity, and — the real object — whether the type-agnostic link layer degrades to "person with pen" without core-opcode changes. If the abstraction secretly assumes a wire, this is where it breaks.

**Decision gate:** ≥8/10 fidelity with core opcodes untouched → the "cell is an idea, substrate is costume" claim holds at the honesty test; `human` becomes a first-class link. Below that → enumerate exactly which assumptions broke (that list is the publishable artifact either way).

**Effort:** 2–4 days including protocol drafting. Independent of Rungs 1–3; can start now.

## Rung 5 — EXOCELL: ESP32 + one sensor as an embedded cell

**Pre-registered question:** *Does an ESP32 with one sensor present as one simple cell from the laptop's quilt while running its own first-person bookkeeping inside — with the two renderings agreeing on ≥9 of 10 core facts, disagreements enumerated and typed, none averaged away?*

**Build:** ESP32 firmware, one sensor (temperature), ESP-Now or BLE into the ingress bridge; the laptop sees one embedded cell at 0/0/0-elsewhere; inside, the ESP32 keeps its own quilt-relative tape. Bonus measurement for free: RSSI under varied physical distance gives Rung 1's `link_quality` fields ground-truth validation against physics.

**Measures:** end-to-end visibility of the cell (fields recorded from radio to journal); portal-boundary fact agreement; quality-field fidelity.

**Decision gate:** cell visible + path/quality fields recorded + typed disagreement list produced → portal seam has its first live subject. Radio flakiness is data, not failure.

**Effort:** 3–5 days firmware + bridge.

> **Placeholder — opencode lane module design:** when the opencode lane's module design lands, align this rung's firmware structure (link driver, tape writer, sensor task) with it. Until then this rung's firmware is throwaway-grade on purpose; do not gold-plate.

## Rung 6 — PORTAL-SEAM: both renderings, disagreement held

**Pre-registered question:** *Given one portal cell (paper or ESP32) with two live renderings, does the canvas keep both origins visible — showing both renderings and their delta for 100% of injected de-sync events across a 1-hour soak, with zero auto-reconciliation?*

**Build:** seam panel: cell as rendered by the outside universe beside its self-rendering, delta list underneath, disagreement held open. Requires Rung 4 or 5 as the portal subject — the seam needs two live origins, not a mock.

**Measures:** reader-delta made literal and perspectival (the memo §2 upgrade); whether rendering can hold two origins without collapsing to a view-from-nowhere average.

**Decision gate:** all de-syncs stay visible through the soak → the canvas does the charter's "something new." Any silent collapse to a single view → that IS the charter's seed-3 failure mode; record its mechanism.

**Effort:** 2–3 days.

---

**Order summary:** 1 (instrument) → 2 (habit baseline) → 3 (H-ROAD-1) is the validity-anchor spine; 4 (paper quilt) and 5 (exocell) run in parallel off-spine; 6 (portal seam) consumes whichever lands first. Cheapest total path to the charter's crown claims: ~3 weeks wall clock, most of it soak time.
