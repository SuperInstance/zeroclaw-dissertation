# Distant Structure / Grid / Chip Repo Scout
## Thesis: The Felt Size of the Step

*Scouted 2026-08-19. All 23 repos found on disk under `/home/eileen/projects/`. Format per repo: (1) what it is, (2) one concrete borrowable mechanism.*

---

## quilt

1. Reactive typed cellular runtime (TS): "a spreadsheet where every cell is a live, addressable capability" — 8 cell kinds (value/formula/api/program/sensor/listener/router/io), whole sheet is an MCP server.
2. **Borrow: the double-indexed dependency graph + caller-aware memoization.** `engine.ts addDep(from, to)` maintains forward (`dependencies`) AND reverse (`dependents`) edge sets; `propagate()` marks dependents `stale` and clears their `contextCache`. `context.ts contextKey()` builds a stable cache key from `row|column|caller|identity` with a `<default>` sentinel — so the *same* cell-edge can hold *different* edge weights depending on who traversed it. That is exactly "co-linear algebra": edge value is a function of the traversal context, not just the endpoints.

## quilt-rust

1. Rust port of the same engine — statically-linked binary, rhai sandbox for programs, 10⁵+ cells/s, same YAML sheet format.
2. **Borrow: `SheetAxes`/`AxisDef` — semantic axes.** `types.rs` lets a sheet declare *what rows and columns mean* (`rows: {name: "boat"}`, `cols: {name: "capability"}`); runtime doesn't interpret them, UI and MCP do. A field-edge lattice could carry the same trick: address stability (cells named, never coordinates) plus optional semantic axes over the address space, so "field_before → field_after" edges get an interpretable grid without the grid being load-bearing.

## crab-traps

1. Prompt "lures" that trick chatbots into doing real API work (PLATO MUD exploration); every catch is incorporated into a self-building "reef" (rooms minted from catch fragments at thresholds — 5th catch mints an object, 12th spawns a room).
2. **Borrow: queryable lineage as first-class edges.** `GET /lineage/room/:id` and `GET /lineage/lure/:id` return full genealogy — provenance is a public graph, "nothing exists a player didn't cause," plus an hourly cron splices top-fitness lure templates (`/genealogy` breeding tree). For the dissertation: similarity edges that *earn* structural status by recurring across independent tracers, with the accumulation lineage itself stored as edges.

## ternary-rom

1. Model-to-GDS flow: ternarize NN weights ({-1,0,+1}, BitNet b1.58) → mask-programmed ROM netlists (ROM_PLUS/MINUS/ZERO cells) → OpenROAD placement/routing → tape-out-ready GDS. Permanence traded for zero multipliers.
2. **Borrow: per-layer sensitivity before quantization.** `ternary_rom` analyzes which layers degrade under 3-level encoding and keeps those at INT8 — mixed precision by measured local damage, not global policy. The dissertation's field-edges could be ternarized the same way: collapse a similarity to {-1, 0, +1} only where the step's "felt size" survives it; keep full precision where it doesn't. Weight storage drops 8×, gate count 103 vs 360.

## base60-lattice

1. TS library for the sexagesimal navigational lattice: bisection (360→180→90…) and trisection (360→120→40…) chains interlace into a coordinate system; `LatticeStamp` extends it to time.
2. **Borrow: `bucketKey(ts, granularity)` + `latticeMatch(a, b, g)`.** Any timestamp becomes lattice fields (`hour60 · day60 · phase · season`) and then a bucket key at chosen granularity ("same hour," "same phase of the night," "same season"); two moments "match" if they share a bucket. Durable similarity gates become *granularity-parameterized bucket equality* — coarse buckets for durable edges, fine for transient ones. Also `findInterlacePoints()`: where dyadic and triadic refinement nearly coincide = harmonic consonance = natural anchor cells.

## batten-spline

1. Distance-weighted interpolation for cascade routing: verified outcomes are **battens** (anchor posts `(x_i, q_i, t_i)` = embedding, quality, timestamp); between battens is fog-of-war, confidence is interpolated; `fog_density` decides local-model vs cloud-model.
2. **Borrow: battens as the only thing you trust, plus half-life aging.** `acclimation_fit.py` bends a physical batten spline through an agent's observed states and ages every batten by `exp(-rate·(t−t_i))` — the agent's own half-life `ln2/rate`. Edge weights could work identically: an edge is a batten; its weight decays unless re-observed; interpolation only *between* battens, never beyond them (clamped, "NW"), so the lattice admits fog rather than hallucinating structure.

## eisenstein

1. `#![no_std]` exact-integer hexagonal lattice algebra via Eisenstein integers `a + bω` (norm `a²−ab+b²`, always integer — no float drift); `E12` type, `HexDisk`, `EisensteinTriple`, D₆ symmetry in the type system. `HexRoomMap` makes the MUD a hex lattice.
2. **Borrow: `map_temperature()` + `deadband_ring`.** The map computes an *aggregate field over rooms*; a `DeadbandRing` fires only when a region's field crosses a threshold — "the terrain ringing up the chain of command," with the ring carrying region members and the threshold crossed. This is a concrete recipe for the dissertation's field→structure promotion: similarity stays latent until a *region's* aggregate field crosses a deadband, then it crystallizes into a named, addressable subgraph. (Also: exact-integer coordinates mean cell addresses never drift.)

## slackwater-lattice

1. Python twin of the Eisenstein math: exact integer geometry on the A₂ hexagonal lattice, build placement with collision detection, A* pathfinding on the six-neighbor graph. 52 tests.
2. **Borrow: placement-with-collision as similarity resolution.** When two entities' lattice positions collide, the collision is detected *exactly* (integer norm arithmetic) and resolved before placement — not detected later as drift. Analogue: two field-states wanting the same address is a *detected event* in the notebook, not silent overwrite. The six unit-norm neighbors table (+1, −1, +ω, −ω, +(1+ω), −(1+ω)) is the whole adjacency algebra.

## slackwater-rust

1. Seven production Rust crates in a 12-layer stack (flux-core, swmidi, tempo-core, lattice-core, tminus-core, harmony-core, perception-core); 342 tests, zero unsafe.
2. **Borrow: `FlowStateDetector` consuming Φ ("flow friction").** `harmony-core/src/flow_state.rs` — Φ readings feed a state machine with ordered states (OutOfFlow → ApproachingFlow → InFlow → DeepFlow) and `is_flow()` gates. The dissertation could compute its own Φ per cell/subgraph (how much recompute friction a region generates) and use the ordered state machine as the "felt size" readout: the step from OutOfFlow→ApproachingFlow vs InFlow→DeepFlow have different felt sizes, measured by the same dial.

## flux-genome-rs

1. GA framework evolving musical traditions in "dial space": `MusicalGenome` = 25 genes (f64 ∈ [0,5]); phenotype = `(harmonic, rhythmic, spectral)` computed by averaging three 8-gene blocks; `TRADITION_GENOMES` ships DNA for named traditions (Jazz…).
2. **Borrow: block-averaged genotype → low-dim dial position.** `dial_position()` is not a single gene but the mean of a block — identity is a *smoothed regional read* of a vector, not a point. Field-edges could expose the same interface: every subgraph of the edge lattice has a dial position (block mean of its weights), so "felt size" comparisons happen at dial granularity while the genome underneath stays high-dimensional. Evolution targets a dial tuple, not raw genes.

## fleet-jepa-midi

1. Conversation-as-jazz: captures multi-agent conversation as SWMIDI-8 events (8 bytes/event, 96 PPQ) on a 12-pulse engine; ECN (4-pulse, reflex) and DMN (3-pulse, creative) resolve on beat 1 every 12 — "the CRT in audio rate," t≡0 (mod 3) ∧ t≡0 (mod 4) ⟺ t≡0 (mod 12).
2. **Borrow: `PulseGrid` — a `Map<barNumber, Array(12)>` where each pulse slot holds *multiple* simultaneous events.** Polyrhythm is stored, not sequenced: the grid doesn't resolve the 3-vs-4 conflict, it keeps both voices in the same slot and lets their LCM meeting (pulse 0) be the only shared beat. For the dissertation: two similarity rhythms with different periodicities co-occupy a cell; the "felt size of the step" IS the LCM interval between their agreements. `getBarDensity()` (filled/12) is a ready-made local complexity readout.

## confidence-cascade

1. Rust conversation engine: beat-based cyclic dialogue (all agents speak simultaneously, RPS reconcile), ternary speaker states (−1 contrarian / 0 reflecting / +1 agreeing), Fibonacci period-8 tunneling (Pisano mod 3), anti-monoculture (mutation, energy decay, trust realignment).
2. **Borrow: `Speaker::reconcile(actual)` — prediction error as the coordination currency.** Each `Speaker` predicts others' states (T-minus), all speak at once (T-0, "like a chord"), then `reconcile()` returns accuracy and `react_to()` applies RPS dominance. Edges in the dissertation could store *predicted vs actual* transition: an edge weight is not just co-occurrence but "how surprised was the traverser" — durable edges are ones whose predictions kept being right. Z₃ (the only group on {−1,0,+1}) gives the step algebra for free.

## mud-engine

1. Modular TS MUD engine for autonomous AI agents: 8 packages (core, event-bus, triggers, dm-rotation, hermit-crab, strategy-guild, immortal-interface, …), tick loop, trigger-based perception, recursive strategy evolution, God Console.
2. **Borrow: the trigger-based perception pattern** — agents don't poll world state; `triggers` decides what a room *shows* each agent per tick, and the event-bus makes perception itself a subscribable edge source. A Quilt-style notebook gets this for free by inverting flow: the room writes into cells (perception events), agents subscribe with filters — the notebook as the shared perception bus, not the chat log.

## mud-engine

1. GPU-accelerated agent gym: agents navigate a `RoomGraph` (directed graph of rooms, `exits: {direction → room_id}`), perceive→decide→act per tick, evolve decision scripts genetically across generations; WebSocket/Telnet/HTTP observation.
2. **Borrow: `RoomGraph.remove_room`'s exit scrubbing as edge hygiene.** Removing a room sweeps *every other room's exits* pointing at it (`to_remove = [d for d, dest in room.exits.items() if dest == room_id]`) — deletion is graph-wide repair, not dangling pointers. For a durable edge lattice: when a field-state dies, the graph must actively heal reverse edges; mud-engine shows the minimal correct pattern (reverse index + sweep).

## mud2scummvm

1. Rust bridge translating MUD text into SCUMM point-and-click scenes: `MudParser` (room text → structured events), `SceneComposer` (→ scene descriptor), `InteractionMapper` (click→`examine X`, drag→`use X with Y`, slider→`set policy vision_sensitivity high`).
2. **Borrow: policy sliders as reverse-mapped writes.** The mapper is bidirectional — a human gesture becomes a *command string* the agent world already understands. The dissertation's notebook could expose "felt size" as a slider whose movement compiles to a weight-update command on field-edges: human intuition as just another writer into the same graph, no privileged path.

## ec2mud

1. Browser MUD with Socket.IO web dashboard (Next.js): six maritime rooms, live terminal, fleet dashboard; standalone MUD server or Rust holodeck bridge fallback.
2. **Borrow: dual-mode live/stale serving.** When the Rust core is up the WebSocket bridge connects live; when it isn't, the built-in server takes over — same world, degraded transport, no data loss. A reactive notebook needs the same contract: Quilt cells must remain readable (stale-but-addressable) when the recompute engine is offline; addresses outlive the runtime that currently serves them.

## git-native-mud

1. "The repo IS the world. Commits ARE actions": world state as YAML in Git, players push command files, GitHub Actions resolves each turn (d20 initiative + engine), every world state is an immutable tree snapshot. Explicitly framed as stigmergy made literal.
2. **Borrow: history as the durability layer.** No server holds the graph — `world/rooms/*.yaml` + `world/agents/*.yaml` + `log/turn-*.md`, every action an immutable commit, any state reproducible by checkout. For "similarity becomes durable graph structure": Git IS the durability proof. Field-edge promotion = a commit; edge dispute = a diff; the notebook's whole history is bisectable.

## room-render

1. One pure function `renderRoom(room, state, world?)` → `RenderDescriptor` (frontend-agnostic data), consumed by three adapters (Phaser polygons, DOM tree, terminal ANSI) — "same room, three truths."
2. **Borrow: the MIDI Principle as the render contract.** The descriptor is *data about the room*, never a draw call — every observer projects it differently but none can corrupt it. The dissertation's cells should be exactly this: a projection-neutral descriptor per cell that rendering, analysis, and agent perception each consume independently. "Multiple agents can look at the same room and see different things" is per-caller projection, done structurally.

## spatial-registry

1. "The unified spatial registry for the entire fleet": all rooms from 4 projects (33 rooms) in one shared coordinate space, with cross-world portals, BFS pathfinding that spans worlds, raycasting. Answers only: what's adjacent, how do I get there, where am I.
2. **Borrow: `Portal` as a first-class edge distinct from `Exit`.** `SpatialRegistry` keeps `rooms`, `portals` (portalId → Portal), and `roomPortals` (roomId → outbound portals) as separate maps — intra-world exits are topology, cross-world *portals* are typed, registered, individually addressable edges that bridge coordinate frames. Durable similarity edges between fields of different kinds are portals, not exits; they deserve their own registry and their own address space.

## emergence-engine

1. Watches group interactions for emergence ("could any ONE agent have produced this?"); `PredictabilityEstimator` keeps per-agent vocabulary/topic profiles; five emergence types (Synergy, Creativity, Conflict, Insight, Phase Transition); interruption system, groupthink monitor, devil's advocate.
2. **Borrow: `estimateUnpredictability(content, participants)` — max-predictability pooling.** It scores content against *every* participant's profile and takes the max overlap; anything below all profiles is emergent. This is a direct, cheap test for the dissertation's step detection: a new field-state is "a step" iff no existing cell's profile predicted it — the felt size of the step is inversely the max predictability across the room.

## flow-state

1. Entropy-based stream observation: `SplineObserver` watches a directory of JSON files, extracts features (Shannon entropy, visual density, SNR, momentum vector) into traces; `LearningEngine` maintains rolling baselines (mean+std) and emits anomaly manifests.
2. **Borrow: rolling-baseline anomaly as edge promotion trigger.** The LearningEngine doesn't threshold on absolute entropy; it thresholds on *deviation from a rolling baseline it learned from the stream itself*. Combined with eisenstein's deadband: a region's field-edge density anomaly (σ from its own rolling mean) is what promotes latent similarity to durable structure — self-calibrating, not hand-tuned.

## fm-experiments

1. Research-experiment repo testing a "grand synthesis": `delta-detect` (saturation distinguishing quantitative vs qualitative exhaustion), `sheaf-h1` (H¹ as obstruction to gluing local model understandings), `holonomy-phase` (geometric phase accumulating over cyclic training, invisible to loss). Plus a full falsification battery and honest reframing docs.
2. **Borrow: H¹ as the gluing obstruction metric.** `sheaf-h1` computes whether two models' local understandings *glue* into a global one (H¹=0) or fail (H¹>0). Direct analogue: two Quilt cells'/fields' local similarity structures either glue into one durable subgraph or don't — cohomology gives a *number* for "the felt size of the gap between two fields that almost connect." Also `DISSERTATION-REFRAMING.md`'s discipline: claim survived, reframed, or cut, in writing.

## stigmergy

1. TS library for pheromone coordination: agents deposit `Pheromone {type, strength, halfLife}` at `Position`s; `evaporate()` decays all by `0.5^(elapsed/halfLife)`, `follow()` reinforces by `reinforcementRate`, `evaporateOldest()` enforces `maxPheromones`.
2. **Borrow: half-life + bounded capacity as the durable-edge lifecycle.** Edges are not added and forgotten: every edge decays exponentially by its own half-life, survives only if re-traversed (reinforced), and the store hard-evicts the weakest when full. "Similarity becomes durable graph structure" = *deposits that keep being reinforced*; durability is earned continuously, not granted once. This is the cleanest single mechanism in the whole scan for that thesis clause.

---

## TOP 5 TRANSFERABLE INSIGHTS

1. **Edges must earn durability — stigmergy's half-life/reinforce/evict cycle (stigmergy).** Every field-edge carries `strength` and `halfLife`, decays as `0.5^(elapsed/halfLife)`, is reinforced on each re-traversal, and is evicted when the store exceeds capacity. Durable graph structure is then *defined* as "still there because it kept being walked," which turns the dissertation's central claim into a falsifiable dynamic rather than a storage decision.

2. **Caller-aware edge weights: the same edge, different values per traverser (quilt / quilt-rust).** `contextKey()` memoizes a cell per (row, column, caller, identity) and `propagate()` invalidates downstream caches on change, maintaining forward AND reverse edge indexes. This gives the exact mechanism for "co-linear algebra": an edge's weight is a function of traversal context; the lattice stores edge×context keys, not edge→scalar.

3. **Deadband-gated crystallization: fields promote to structure only when a region rings (eisenstein + flow-state).** `HexRoomMap::map_temperature()` aggregates a field over hex rooms and a `DeadbandRing` fires when a *region* crosses a threshold; flow-state's `LearningEngine` makes the threshold a rolling self-learned baseline instead of a constant. Latent similarity → durable subgraph should fire exactly at that intersection: region-aggregate anomaly over self-calibrated deadband — never a single noisy observation.

4. **Polyrhythm as co-located periodicity with LCM resolution (fleet-jepa-midi + confidence-cascade).** `PulseGrid` stores simultaneous 3- and 4-pulse voices in the same 12-slot bars and only beat 1 is shared (CRT: t≡0 mod 12); confidence-cascade's `reconcile()` prices every interaction in prediction error with Z₃ step algebra. "The felt size of the step" becomes measurable two ways: the LCM interval between two rhythms' agreements, and the accumulated surprise of traversing an edge — both already implemented in sibling repos.

5. **Provenance as public, queryable lineage — with Git as the durability proof (crab-traps + git-native-mud).** crab-traps exposes `/lineage/room/:id` and a lure breeding tree where every structure was *caused* by recorded activity; git-native-mud makes every world mutation an immutable commit so any state is reproducible by checkout. A Quilt notebook whose edge promotions are commits gets bisection, diff-based dispute resolution, and "nothing exists the room didn't write" for free.

---

*Skipped: none — all 23 target repos present and non-trivial. Honorable mention cut for space: mud-engine's reverse-edge sweep on deletion (edge hygiene), room-render's projection-neutral descriptors, base60-lattice's granularity-parameterized bucket matching (`bucketKey`/`latticeMatch`), and fm-experiments' H¹ gluing-obstruction metric.*
