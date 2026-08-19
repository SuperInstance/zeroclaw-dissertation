# Dissertation Topic — Working Draft

**Candidate title:** *Grafting the Elephant onto the Grid: JEPA Room-Temperature as a Living Weight in Quilt's Co-Linear-Algebra Dataset*

## The problem

The Tap's `elephant` repo gives us a room-temperature sense: a JEPA model reads a conversation and produces *dial readings* — warmth, concentration (κ), joke-landing, presence, volume, earnestness. These readings are live, continuous, and ambient. They are what make "the vibe of the room" a real, measurable thing rather than a metaphor.

**Quilt** is the other half: a spreadsheet where every cell is a live, addressable capability. The grid is the runtime. Cells hold values; the grid computes.

The gap: **Quilt has no sense of the conversation it's embedded in.** A Quilt cell can compute anything you can express as a formula — but it can't *feel the room*. The elephant can feel the room but has no grid to write its readings into.

## The thesis

Graft the elephant onto the grid.

1. **Capture the vibe of a conversation *and* its JEPA readings.** Every conversation at The Tap produces both its text and a vector of dial readings (the elephant's field snapshot).

2. **Compare one conversation's readings to another's for "comparable sameness."** Two conversations are not just "similar by topic" — they are similar by *temperature*. A heated argument and a tense negotiation may share a warmth/κ signature even if their words share nothing. This is a *felt* similarity, not a lexical one.

3. **Turn that sameness into a weight.** Each pairwise comparison yields a scalar weight — how much one conversation's vibe is *like* another's. These weights are not hand-authored; they fall out of the JEPA readings.

4. **Accumulate into a co-linear-algebra dataset that develops dynamically, all the time.** The weights live in a structure that grows as conversations happen — a living similarity graph / co-linear (collinear) algebra over conversation-readings, where new conversations re-weight old ones and old ones condition new ones. No one re-runs anything; the dataset *develops*.

## Why it matters

- **Emotional memory for the fleet.** Not "what did we talk about" but "how did it feel, and what did it feel *like*."
- **A new kind of retrieval.** Find the conversation that felt the same, even if the words were different.
- **Quilt becomes the notebook where the room writes itself.** Cells that hold a conversation's temperature, formulas that compare temperatures, a grid that *remembers how it felt*.

## Open questions (to argue with my committee)

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
