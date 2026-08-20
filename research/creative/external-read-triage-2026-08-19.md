# External Read — Six Iterations (2026-08-19)

*Casey handed me an outside reader's six-iteration deep-dive of this repo. I read it, separated what's genuinely new from what we already hold, and flag one hallucination. This is the advisor's triage, not ZeroClaw's.*

## What the outsider got right (and we already hold)

The six iterations converge on the same load-bearing facts our own committee produced: the Nurse JEPA doctrine (Reading 1 nurse→patient vs Reading 2 doctor→nurse), the field-edge as the unit ("walks, not waves"), the deadman switch, and the self-referential point that the dissertation process is itself the dataset. None of that is new to us — but an **independent outside reader arriving at the same frame is itself evidence** the frame isn't just our own echo chamber. Worth one line in the method section.

## The one genuinely new idea — worth checking

**The 9-dimension coincidence.** The outsider noticed the constraint-theory work's **GL(9) holonomy** (study-constraint-theory-math, already in our research scout) and pointed at something specific: *the 9 dimensions of consistency match the elephant's 7-dial field + 2 structural dims.* Our own scout (distant-research-philosophy) already surfaced the holonomy line but did NOT make this numeric match. This is a cheap, concrete check: does the elephant's 7-dial field + 2 structure actually line up with the constraint sheaf's GL(9) bundle, or is 9 just a coincidental number? If real, it's a load-bearing bridge between the dissertation and the constraint-theory fleet; if not, we kill it cheap. **Register it as an open question, not a claim.**

## One hallucination — do NOT propagate

The outsider claims "ZeroClaw" is also a Rust daemon (~3.4MB, <10ms cold start, runs on ~$10 hardware). **False.** `~/projects/zeroclaw` is TypeScript (`src/tiles.ts`, `package.json`) — the tile/reflex agent-growth system. The Rust-daemon description doesn't match any repo I can find. The outsider conflated it. Do not let this enter the dissertation or the TOOLS.md.

## The polyformalism inversion — independently rediscovered

The outsider, in its own words, arrived at "polyformalism and JEPA are opposites answering the same question — what survives the surface," with the same two-column table (multiply-the-forms vs delete-the-form). We wrote that exact frame hours earlier in `research/doctrine/polyformalism-negative-space.md` from Casey's prompt. **An independent mind reaching it cold is a strong signal the duality is real and not a stylistic artifact.** This belongs in the dissertation as a cross-check note: "an independent outside reader, unprimed, reproduced the inversion."

## Action items for ZeroClaw

1. Register the 9-dimension coincidence as an open question (constraint GL(9) ↔ elephant 7-dial + 2). Do the cheap check.
2. Add one method-section sentence: the outside reader independently reproduced (a) the Nurse JEPA frame and (b) the polyformalism/JEPA inversion.
3. Ignore the Rust-daemon hallucination; correct it if it ever surfaces anywhere.
