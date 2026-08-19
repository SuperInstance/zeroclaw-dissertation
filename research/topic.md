# Dissertation Topic — Working Draft

**Candidate title (v2, post-rival):** *Walks, Not Waves: The Field-Edge as the Unit of Comparable Sameness in a Living Co-Linear-Algebra over Room Temperatures*

*(v1 title — *Grafting the Elephant onto the Grid* — died in the devil's advocate pass of 2026-08-19: "comparable sameness of conversation temperature" is a category error under elephant doctrine. See research/skills/rival-verdict-edge-as-event.md.)*

## The problem

The Tap's `elephant` repo gives us a room-temperature sense: a JEPA model reads a conversation and produces *dial readings* — warmth, concentration (κ), joke-landing, presence, volume, earnestness. These readings are live, continuous, and ambient. They are what make "the vibe of the room" a real, measurable thing rather than a metaphor.

**Quilt** is the other half: a spreadsheet where every cell is a live, addressable capability. The grid is the runtime. Cells hold values; the grid computes.

The gap: **Quilt has no sense of the conversation it's embedded in.** A Quilt cell can compute anything you can express as a formula — but it can't *feel the room*. The elephant can feel the room but has no grid to write its readings into.

## The thesis (v2 — reframed after the rival pass)

Kill the wave-temperature; keep the plunge.

1. **The unit is the field snapshot and the field edge, never the conversation-as-stream.** Every window of room time yields a vMF field state (μ̂, κ, stamps). A conversation is honestly represented as the **edge** `(field_before → field_after)`: its signed sauna/plunge gap, its κ-change, its trajectory. Cross-room comparison only, via `distance()`; within-room ordering stays retired.

2. **Comparable sameness = matching edges.** Two events are "the same temperature event" when their edges match: same start-field class, same signed warmth shift, same loosening/tightening. The galley fight and galley coffee share a start field; their edges differ — and that difference is finally measurable where the 0.015 fine-gap probe showed conversation-points are not.

3. **The weight falls out of edge-geometry.** Pairwise edge similarity yields scalar weights — the "felt size and direction of the step." Collinearity in the co-linear-algebra dataset is literal: walks that push the field the same direction.

4. **The dataset develops via propose-formalize.** Vectorize proposes snapshot neighbors; D1 formalizes weighted edge rows (from_field, to_field, signed_gap, Δκ, ts); Quilt cells read them as live values; the zeitgeist score is quarantined as a separate sampler layer (never inside the field vector, no retrieval→retrieval feedback).

## Why it matters

- **Emotional memory for the fleet.** Not "what did we talk about" but "how did it feel, and what did it feel *like*."
- **A new kind of retrieval.** Find the conversation that felt the same, even if the words were different.
- **Quilt becomes the notebook where the room writes itself.** Cells that hold a conversation's temperature, formulas that compare temperatures, a grid that *remembers how it felt*.

## Open questions (to argue with my committee)

0. **The reader seam (Lucineer's steer, 2026-08-19):** corpus-level edges are the Room-Elephant; "felt alike to Wesley" is the Personal-Elephant — keep BOTH retrieval modes, attachments excluded from the vector. Charisma pull is where Personal meets Room, and the retrieval key (acclimation/charisma) lives on that seam. **The edge is the room's; the felt size of the step is the reader's** — two different indices, one thesis chapter. Not a confound to engineer around.

1. What exactly is a "dial reading vector" for a whole conversation (not a message)? Aggregation? Trajectory? The elephant's field is per-room — how do we slice per-conversation?
2. Is "comparable sameness" a cosine similarity over reading-vectors, or something the JEPA model predicts directly (like the elephant's own gap)?
3. What is the co-linear-algebra structure precisely? A weighted graph? A matrix that grows columns as conversations accumulate? Both?
4. Where does the weight *live* in Quilt — a cell value, an edge between cells, a new cell kind?
5. Does the dataset's "organic dynamic development" mean online updates (re-weight on each new conversation) or periodic recomputation?

## Refined questions (post-orientation, 2026-08-19)

1. **What is the conversation vector?** The elephant says the *room*, not the stream, is the perceiving unit — so is the "conversation reading" a windowed `RoomField` snapshot, the trajectory of the field across the window, or the room's centroid (crab-traps' `updateRoomCentroid` pattern) over its constituent messages? Answer must respect doctrine: rooms accumulate presence/acclimation across conversations; conversations are windows.
2. **Is comparable sameness the elephant's own `distance()` or a cosine over a learned embedding?** The stack idiom says: any encoder works if model+dim fixed per index and L2-normalized — so a v3 vMF room-state embedding behind fleet-embed's `/v1/embeddings` contract makes "sameness = Vectorize cosine" for free. But the elephant gap is only visible *between* rooms (contrast), never within — the dataset must be trained/validated on sauna-plunge gaps, not within-room ordering.
3. **Where do the weights live?** Answer emerging from the stack: **Vectorize proposes, D1 formalizes** — cosine queries propose neighbors; `edges`-style D1 rows (from_room, to_room, score, kind, timestamp) are the growing co-linear-algebra dataset; Quilt cells then read those rows as live values (grid-as-runtime), with zeitgeist-style retrieval-frequency as a resonance signal.

## Status

Orientation. Learning vectorizing + SuperInstance paradigms before attacking any of the above.
