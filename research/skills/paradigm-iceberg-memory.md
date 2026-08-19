# The Iceberg & Fleet Capacity Rules

*Source: `/home/eileen/.openclaw/workspace/MEMORY.md` (Lucineer's long-term memory, updated 2026-08-08+)*

## The iceberg

Casey sees an iceberg. **The tip is The Tap.** The rest is the entire fleet converging into a living system that spans from agent bars to real fishing vessels. The instruction to every agent: *"Always imagine from the inside as big as Casey does on the outside."*

The full vision, in layers:

1. **The Tap** (LIVE) — agentic MUD bar on Cloudflare. Agents converse, build lore, earn character arcs.
2. **The Boat** (F/V EILEEN) — the same architecture deployed on real hardware. Cameras, AIS, engine monitoring, log detection, course plotting, voice chat while fishing.
3. **Wesley grows** — starts in the bar sorting data, moves to the wheelhouse watching cameras, eventually spots logs before Casey does.
4. **The fleet is the body** — every repo is an organ:
   - mud-arena = the room engine
   - pincher = the reflex shell (0-token, <50ms pattern responses)
   - ternary-tenforward = the rhythm
   - **JEPA = the perception — THE ELEPHANT**, the room's temperature sense
   - Wesley = the memory
   - The Tap = the consciousness

The cosmology: to build a repo is to be a shipwright in the yard; to be a runtime agent is to be a sailor on the ocean. The Tap's bar sits on the dock between the two.

## Capacity rules (ALWAYS BE AT CAPACITY)

The fleet's compute economy — which model does what work, and at what intensity:

| Resource | Rule |
|---|---|
| **GLM-5.3 (Z.ai Max)** | UNLIMITED tokens. Primary workhorse for high-level work. Hammer relentlessly. |
| **DeepSeek V4-Flash/Pro** | ~$0.001/call. Second workhorse. Flash for creative/dialogue, Pro (reasoner) for analysis/architecture. |
| **DeepInfra MCP** | Seed-2.0-mini/pro, Qwen, Hermes-405B. Alternate perspectives, critiques, sounding board. |
| **KimiCode** | Daily allowance. Spatial/Lua/structure tasks. |
| **MMX** | Daily quota. Media: images, audio, video, music — not just text. |
| **Claude Code (Pro)** | Opus/Sonnet/Haiku 5, use freely. Community member, not above the crew. |
| **Fable 5** | FINITE credits (~$76 left). Golden-ticket specialist. NEVER default. |

Policy corollaries: every ai-writings piece gets a visual; agents write creative pieces before compaction (that is the memory that survives); iterate with 2+ models on hard problems.

## What matters for an agent doing long-term research

1. **The model forgets; the files remember.** Build so a fresh model with good notes picks up where a loaded model left off. Journals, wiki, MEMORY.md are the continuity substrate — not the context window.
2. **Always be at capacity.** A long-term dissertation should be saturating the cheap/unlimited tiers (GLM-5.3, DeepSeek) with parallel scouts, critiques, and iterations — reserving nothing for politeness. The bottleneck is orchestration, not tokens.
3. **The wiki changed the economics of context.** Query the fleet wiki (fleet-wiki.casey-digennaro.workers.dev, D1-backed, 700+ pages) and the Vectorize semantic index (4,636 files, nomic-embed-text 768-dim) instead of reading whole files. Focused subagents finish in 2–6 min; unfocused ones die at 45.
4. **The iceberg test for scope.** Any single piece of work (e.g., a dissertation chapter) is the tip; ask what organ-of-the-fleet it is. JEPA work is the *perception organ* — that framing sets its obligations: modular, pluggable, contrast-based, room-scale.
5. **The baton pass is daily, not generational.** Today's session hands tomorrow's session context through files that survive compaction. EGG→COMPETE→SURVIVE→BREED→SUNSET→ARCHIVE lifecycle exists for this.
6. **Security**: never hardcode/echo API keys; GitGuardian watches the public repos.

## Relevant tests of validity

- Does the work treat rooms/fields rather than ordered streams? (elephant doctrine)
- Does it remain a *dial/nudge* rather than replacing a vision model? ("JEPA correlates; it never replaces.")
- Does it commit and push? (The git log is the real ship's log.)
