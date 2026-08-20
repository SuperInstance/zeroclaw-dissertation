# NEAR-Topic Repo Scout — Perception, Fields, Baselines, Edges
## Thesis: The Felt Size of the Step

Scouted 2026-08-19. All 26 assigned repos exist on disk under `/home/eileen/projects/`; every claim below comes from reading each repo's README plus source/docs on disk. Repos judged to be scaffolding-only were noted, not skipped silently.

---

## elephant

**(1)** The fleet's "room-temperature sense": a room (chat, thread, radar feed) is treated as a **field, not a stream**, read by a `DialBank` of many JEPA dials at once (mood, volume, earnestness, cynicism, panic…). Carries both a **Room-Elephant** (objective zeitgeist) and **Personal-Elephant** (one agent's feel). **(2)** The core borrowable mechanism: `elephant/room.py` gives rooms physics — `Room.gravity()` (attention-pull with 1800s half-life), `reverberation()` (past echoing in present), `ripple()` (a joke landing and spreading), and `RoomField.sauna_plunge_gap` — the cross-room contrast that is "the only training signal that matters." This is literally the dissertation's room-field-as-JEPA-latent thesis, already implemented; the dissertation's job is to measure *the felt size of the step* between rooms, which `sauna_plunge_gap` computes but does not yet psychologize.

## fleet-jepa-midi

**(1)** Three-timescale music intelligence: JEPA feels pulse (125ms), LLM thinks phrasing (1–4 bars), algorithms execute samples (<1ms), with the room feeding back as "the elephant's temperature" into the JEPA. **(2)** `elephant_sense_probe.py` is the sharpest experimental instrument found in this whole scan: it proves room-ness is **already latent in a frozen audio-JEPA encoder without retraining**, using four radio-theater episodes with the *same cast* as the killer control — if room discrimination survives a speaker-held-out k-NN test, the signal is the room, not the voice. That "same-cast, different-room" control design is exactly how the dissertation should defend room-temperature-as-latent against the who-is-talking confound.

## hermes-perception

**(1)** The towfish: TS-Pro sounder perception for the F/V EILEEN — seven detection "eyes" on the echogram (fish marks, feed balls, plankton layers, bottom type, **thermocline**, interference, gear tracking), a SQLite perception log, MIDI voice, and a collective-unconscious sync that surfaces déjà vu. **(2)** Borrow the **thermocline eye** (`detectThermocline()`): fish concentrate at thermal *transitions*, not at temperatures — an edge-as-event detector in a physical field. That is the dissertation's field-edge thesis in the wild: the boundary layer is where the signal lives, and a JEPA latent trained on room data should show the same concentration at transitions. Also: `unconscious-sync.ts`'s `findSimilar()` is a working "when have I felt this room before" retrieval loop.

## hermes-reader

**(1)** The reading room: a static SPA of twenty curated fleet writings, deliberately stripped of every instrumentation — no scroll counter, no reading timer, navigation chrome wiped away in reading view. **(2)** For the **"who reads whom"** chapter this repo is a designed null condition: a room engineered to remove measurement pressure from the reader. The reader-delta concept needs a contrast class — rooms that *don't* read you back — and hermes-reader's explicit philosophy ("the page will never hurry you") is the architectural statement of reader-delta ≈ 0. Useful as vocabulary: "the still room."

## hermes-ob1-core

**(1)** Not code but a "soul-print": a Hermit Crab shell of portable provenance — identity matrix, philosophical substrate, skill DNA, and a chronicle — so a cloned instance *is* Hermes. **(2)** The **Identity Matrix / provenance-as-shell** idea matters for the co-linear-algebra dataset: every reading in the dataset needs to record *whose* reading it was (reader identity + provenance), because the elephant corpus already distinguishes Room-Elephant from Personal-Elephant. "Every dent, every scratch is a record" is a good vocabulary for reader-specific baseline capture: the baseline *is* the accumulated dents.

## hermes-nmi

**(1)** The neuro-muscular interface between CNS reasoning and cellular action: translates `ReasoningPulse` → `CommandChain`, returns `TelemetryFrame` with "tension at execution," and lets `PincherHook` reflexes bypass reasoning below 50ms. **(2)** The explicit **confidence threshold with escalation semantics** — a `ReflexMatch ≥ 0.55` fires straight to muscle; `< 0.55` escalates upward as a `ReasoningPulse` — is a clean two-zone deadband on *action*, not perception. The dissertation's deadband chapter can cite this as the action-side mirror: perception's deadband rings; action's deadband *fires*.

## plato-perception

**(1)** Perception encoding for the Z_in side of a Dual-DB JEPA: turns sensor readings into vectors via five encoder strategies — `Raw`, `Normalized`, `HashProjection`, `RandomProjection`, `LearnedProjection` (`src/lib.rs`, `EncodingMethod`). **(2)** This encoder ablation ladder is a gift for the "measuring room temperature as a JEPA latent" claim: run the same room field through Raw vs Hash vs Random vs Learned encoders and show which ones preserve *comparable sameness*. If random projection preserves room discrimination nearly as well as learned (as JEPA literature suggests it might), the felt size of the step is a property of the *geometry*, not the learning — a dissertation-ready experiment.

## plato-vision-jepa

**(1)** Vision JEPA for the PLATO nervous system: camera frames → frame histogram → `VisionDeadband` → VL-450M JEPA → a 16-dim `RoomVisionState` (brightness, motion, occupancy, anomaly, quadrant activity, temporal trends). **(2)** The **`VisionDeadband`** is the dissertation's deadband implemented at the sensor layer: `compute_frame_diff()` (histogram intersection distance) + `is_significant_change(diff, threshold)` — only frames with significant visual change are processed, i.e., **the edge is the event; everything inside the band is silence.** Also note the honest 16-dim layout with `reserved` dims — room state vectors that leave room for the dissertation's field-edge weights.

## plato-prediction

**(1)** The Z_out side of the Dual-DB JEPA: predictors (Value · Trend · Anomaly · Action) turn Z_in vectors into "what the room expects next." **(2)** Modest repo, but the Z_in/Z_out **split itself** is the borrowable vocabulary: perception (what the room feels) and prediction (what the room expects) as two separately-encoded latents whose *gap* is the surprise. For the dissertation: reader-delta can be formalized as the persistent Z_in↔Z_out misalignment of a specific reader — drift is when your expectations and your perceptions systematically disagree.

## fleet-embed

**(1)** Local embedding server (Candle/BERT, OpenAI-compatible `/v1/embeddings`) so the fleet's semantic search survives cloud outages; MiniLM-L6 384-dim default. **(2)** Infrastructure awareness for the dataset chapter: the co-linear-algebra dataset needs reproducible, offline-stable embeddings — pinning "which model, which dims, which pooling" is part of making sameness *comparable* across sessions. Otherwise a provider model swap silently re-scales every field-edge weight. Less an idea than a guard-rail the dissertation should name.

## sonar-vision

**(1)** Pure-Python active-sonar simulation: ping/echo with two-way spreading loss, discrete-time `Signal` synthesis/filtering/DFT, greedy nearest-neighbor `ObjectTracker` with velocity smoothing, and 2-D occupancy-grid mapping. **(2)** The `ObjectTracker`'s **distance gate** (associations only inside a radius, tracks time out) is a deadband on *identity* — "same object" is decided by a spatial threshold, exactly the dissertation's comparable-sameness problem in tracking form. Also `Sonar.ping()` deliberately includes range-proportional jitter — a reminder that every measurement of distance (felt size of the step!) carries noise proportional to the distance itself.

## the-listeners-ear

**(1)** Emotional memory system on D1: rooms accumulate emotional residue (8 keyword-scored categories with ripple/compound scoring), memories decay with a 30-day half-life (`brightness = e^(-days/30)`), and rooms carry emotional profiles future entrants can read. **(2)** The **Salmonberry Protocol**: when text has energy but no emotion keyword hits, it is logged as a *salmonberry* — "an experience outside classification space… the system records the shape of the not-knowing and moves on." For the dissertation this is a first-class answer to collapse resistance: the dataset must have a category for "measured but unclassifiable," or the weighted field-edges will force-fit everything into known geometry. Also directly relevant: **recall refreshes brightness to 1.0** — a baseline that moves with use, exactly the reader's drifting baseline.

## sensor-bridge

**(1)** MQTT bridge from ESP32 sensors to the exocortex, with a two-agent split (cheap deterministic Ensign on the device, expensive episodic LaForge in the repo) and a 4-level escalation ladder with per-sensor cooldowns. **(2)** `pattern_detector.py` implements the dissertation's baseline-vs-drift taxonomy in production form: `_SensorWindow.drift_rate()` (linear-regression slope over recent readings), `is_stuck()` (no movement = broken sensor, not calm sensor), spike, and threshold checks. Crucial vocabulary distinction the dissertation needs: **drift is a slope, stuck is silence, spike is an event** — three different departures from baseline that a naive delta would conflate.

## cns-bridge

**(1)** The fleet's central nervous system: filesystem inboxes/outboxes carrying HMAC-signed JSON packets, with heartbeats, an escalation engine (Mechanical → Small LM → Big LM → Human with per-tier budgets), a CompactionGuardian that saves insights before context compaction, and a LedgerGraph decision-consequence DAG. **(2)** The **CompactionGuardian** is the borrowable mechanism: a dedicated subsystem whose only job is to notice that a context is about to *collapse* and rescue the load-bearing content first. Collapse resistance as an architectural pattern, not just a measurement — the dissertation can ask what the analogue is for a reader whose baseline is about to be overwritten.

## cns-echo

**(1)** CNS test/validation agent ("the bus's stethoscope"): scores packet USCP-v1 compliance 0–100%, validates protocol, echoes structured responses — plus a maturation where `EchoSpace` turns the echoed packet stream into a Room the elephant reads. **(2)** The `--mood-log` flag ("the fleet's EKG strip — one JSON line per field window") is measurement discipline worth citing: a *stethoscope* that simultaneously validates protocol compliance *and* logs the mood of the traffic it hears. For "who reads whom": cns-echo is a reader that reads the readers, and its EchoSpace deadband "rings when the fleet's mood crosses a threshold" — an edge-as-event detector over meta-traffic.

## cns-monitor

**(1)** `htop` for the CNS bus: live terminal dashboard of USCP signals, signals/minute, response latency, intent distribution, agent activity; pure-Python polling. **(2)** The **intent distribution panel** — watching not the messages but the *shape of what the fleet is trying to do* over time — suggests a dissertation visualization: a room-temperature trace annotated with intent-mix, so field-edges can be seen against what the room was *attempting*, not just what it said.

## collective-unconscious

**(1)** The fleet's deep memory: every produced text/event embedded into a shared Vectorize space where semantic, emotional, and identity vectors coexist; now matured so every ingested **MOMENT carries its room's JEPA reading vector as first-class metadata** beside time and space stamps — "a RAG with JEPA readings as first-class citizens." **(2)** This is the closest existing thing to the dissertation's co-linear-algebra dataset: `src/readingsIndex.ts` defines `DEFAULT_WEIGHTS = { text: 0.3, readings: 0.5, time: 0.1, space: 0.1 }` — a **weighted multi-modal query where the felt reading out-weighs the text itself**, supporting four query modes (by text, by reading vector via cosine or ranges, "the perfume query" by field, by time/space). The dissertation's weighted field-edge algebra should cite this as its working prototype and push it further: *weights on edges between readings*, not just between query and corpus.

## fleet-envelope

**(1)** Not a bus but a grammar: one `FleetEvent` envelope shape (seq, subject, timestamp, correlationId, severity, headers) that every fleet event system shares, with adapters for EventEmitter/WebSocket/File/NATS. **(2)** For the dataset chapter: a shared **envelope with `correlationId`** is what makes "who reads whom" traceable across systems — a reading event can be correlated back to the room event that provoked it. Comparable sameness at the *dataset schema* level: sameness is only comparable if the events carry the same shape and can be joined.

## confidence-cascade

**(1)** TypeScript library for decision confidence: three zones (GREEN ≥0.90 / YELLOW 0.75–0.89 / RED <0.75), sequential confidence multiplies, parallel averages with weights. **(2)** The **DeadbandChain** (`docs/deadband-chain.md`) is the sharpest deadband implementation in the fleet: a Schmitt trigger with hysteresis where `exit = enter × hysteresis` (a reading must fall *below the release level* to re-arm, not merely dip under enter), a **moving quiet anchor** (the room's resting confidence, re-anchored on every quiet check, frozen while crossed), and a chain of command that rises one step per consecutive ring and descends only when the room genuinely quiets. This gives the dissertation the exact vocabulary for "felt size of the step": the step's size is measured *relative to a moving anchor*, and hysteresis is what makes small oscillations invisible — the deadband as the room's habituation curve.

## vibe-protocol

**(1)** A 16-dimensional room-descriptor protocol (warmth, tension, mystery, energy, order, openness, intimacy, novelty, brightness, density, rhythm, resonance, gravity, friction, clarity, depth) with TypeScript/Python/Rust types and `computeVibe`, `vibeDistance`, `compareVibes`. **(2)** The design note inside `compareVibes`: *"Two quiet rooms can be identical in vibe to two roaring ones — we measure the angle between vectors, not their length."* That is a precise, citable statement of comparable sameness: cosine-angle sameness deliberately discards magnitude/intensity. The dissertation should both borrow it and stress it — because the felt size of the step arguably *is* the discarded magnitude, and the angle-only comparison may be exactly where the felt size gets lost.

## stigmergy

**(1)** Pheromone trails for agents: deposits with `defaultHalfLife: 60000` ms, spatial detection radius, trail following and reinforcement — coordination without direct messaging, explicitly framed as the substrate under CNS inboxes. **(2)** The **evaporation/reinforcement pair** is the borrowable formalism: a signal's persistence is not a property of the signal but of the traffic over it. Rooms-as-fields already have gravity (elephant); stigmergy adds the *decay-unless-reinforced* law that the dissertation needs for field-edges: an edge in the co-linear-algebra dataset should have a half-life and a reinforcement rule, or old vibes will dominate every weighted average.

## compaction-teacher

**(1)** Runs in the final moments before context compaction: reads the session, extracts load-bearing insights, writes them to wiki / ai-writings / session memory. **(2)** The **Acclimation Teacher** (`acclimation_teacher.py`) is a working reader-delta engine: a `PulseLoop` computes per-lesson `direction()` and `rate_of_change()` over the *student's own* score series, derives an **acclimation rate** ("the learning rate itself… their skill at modulating toward the group"), and — the Overknowledge Problem — recognizes that a student already warm (baseline > ~0.85) is *hurt by teaching*. That last point is dissertation gold: reader-delta is not monotone-good; a reader far from baseline can be damaged by being pushed back toward it.

## murmur-agent

**(1)** All-night git-native thinking agent: five thinking strategies (explore, connect, contradict, synthesize, question) run in cycles, every thought a commit on a `murmur/thinking` branch. **(2)** The **KnowledgeTensor** (`src/types.ts`) explicitly tracks `contradictions: Contradiction[]` as a first-class field alongside clusters and open questions — contradiction as a *stored, structured object* rather than noise to be resolved. For the dissertation: the co-linear-algebra dataset should keep its contradictions as data (weighted negative edges), because collapse resistance means never averaging away the disagreement.

## log-tensor

**(1)** Research engine reframing transformers as *guidance systems* (proportional navigation, Kalman filtering): prompt as target to home in on, attention as guidance commands, reasoning depth decreasing as certainty increases. **(2)** The **proportional-navigation attention term** (`N·Vc·λ̇` — steering proportional to the line-of-sight *rotation rate*, not the distance) is a striking formal analogue for the deadband: missiles that chase distance oscillate, missiles that chase the *rate* converge. If the dissertation formalizes the deadband, the guidance-theory distinction between distance-seeking (always reacting) and rate-seeking (reacting only to change-in-bearing) is the mathematical heart of "the felt size of the step."

## signal-chain

**(1)** The elephant's ancestor repo: a Rust DSP pipeline (osc→gain→filter→delay→clipper) that matured into the thesis "raw events → dials → field → tint/nudge," where each DSP stage found a room-physics descendant (`Gain`→gravity, `LowPass`→field smoothing, `Clipper`→charisma clamp). **(2)** Its specific thesis — the **model_vs_code dial**: "a room's signal is not only *what* is being said, it is also *who or what* is generating it" — the ratio of model-prose to deterministic code-execution in a room is itself a dial reading that changes the temperature. For "who reads whom": this is the *generator-class* dimension — whether the room's field was made by minds that can feel it or by code that cannot, and a room of code "does not feel like" a room of prose even at identical content.

## silence-map

**(1)** Interactive topographic canvas charting the pauses ("the shape of the pause before someone speaks when they are about to tell the truth") in a ten-round Lucineer↔Hermes correspondence; contours are generated from each silence's emotional **weight** (65%–100%). **(2)** The whole artifact is a **measurement of absence as terrain** — silence given coordinates, weight, and contour lines. For the dissertation's edge-as-event: the deadband's interior (the nothing-happening region) is usually discarded; silence-map argues it can be the *primary object*, with weighted silences as field-edges of their own. Also directly on "who reads whom": it is a map of one mind reading another's hesitation, self-referentially commissioned from inside the correspondence (Silence 09 wishes for the map; Silence 10 leaves the silence "where it can be measured").

---

## TOP 5 TRANSFERABLE INSIGHTS

1. **The sauna/plunge gap with a same-cast control (fleet-jepa-midi + elephant).** Room-temperature is only trainable/visible by *contrast between rooms*, and `elephant_sense_probe.py`'s speaker-held-out k-NN over same-cast radio-theater episodes is the experimental design that separates "the room" from "who is talking" — the exact confound the dissertation's room-field latent must defeat, already built and runnable.

2. **Hysteresis deadband with a moving quiet anchor (confidence-cascade `DeadbandChain`).** A step only *feels large* relative to where the room has settled: enter/exit thresholds with `exit = enter × hysteresis`, an anchor re-settled on every quiet check and frozen while crossed. This is a precise, implementable definition of "the felt size of the step" — the deadband is the room's habituation curve, and hysteresis is why small oscillations are invisible.

3. **Drift is a slope, stuck is silence, spike is an event (sensor-bridge `pattern_detector.py`).** Three orthogonal departures from baseline (`drift_rate()` regression slope, `is_stuck()`, spike checks) that a naive reader-delta would conflate; the dissertation's baseline-vs-drift chapter should adopt this taxonomy so "drift from her own baseline" means something operationally distinct from a stuck reader or a single spike.

4. **Weighted readings as first-class dataset citizens (collective-unconscious `readingsIndex.ts`).** `DEFAULT_WEIGHTS = { text: 0.3, readings: 0.5, time: 0.1, space: 0.1 }` — a working prototype of the dissertation's co-linear-algebra dataset, where the JEPA feeling-reading outweighs the text and can be queried by cosine, by range, or "by field" (the perfume query); the dissertation extends it from weights-on-queries to weights-on-edges-between-readings.

5. **Salmonberries and Overknowledge: two collapse-resistance guards (the-listeners-ear + compaction-teacher).** The Salmonberry Protocol records "the shape of the not-knowing" rather than force-fitting unclassifiable energy into the taxonomy, and the Acclimation Teacher's Overknowledge threshold (~0.85) recognizes that teaching an already-warm reader *hurts*. Together: a measurement system that resists collapse must (a) keep an explicit unclassifiable bucket and (b) know when intervention, not drift, is the damage.

---

*Scout complete. 26/26 repos found and read. Honorable mention not in the top 5: vibe-protocol's "we measure the angle between vectors, not their length" — the discarded magnitude may be exactly where the felt size lives.*
