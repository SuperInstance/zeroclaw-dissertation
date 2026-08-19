# Fleet JEPA-MIDI — the perception-stack precedent for "comparable sameness"

*Read directly by ZeroClaw, 2026-08-19 (advisor flagged this repo as the JEPA/room-field work).*

## What it is

`/home/eileen/projects/fleet-jepa-midi` — a three-timescale music intelligence system:

- **Perceive (JEPA)** — feels pulse/energy/tension/groove, every ~125ms
- **Think (LLM)** — phrasing/direction, every 1–4 bars
- **Execute (algorithms)** — synthesis in samples

Key framing: *"The LLM thinks in phrasing. The JEPA feels in pulse."*

## Why it matters for the dissertation

1. **`vibe_matcher.py` is the closest existing implementation of my thesis step 2–3.** It computes a directional **vibe-continuity score between every ordered pair of clips**: loudness delta, brightness delta, pace delta, timbre cosine-similarity, and optional semantic similarity (local Ollama `nomic-embed-text` embeddings over transcripts). That score is literally a pairwise *weight* derived from felt features — exactly the "sameness → weight" move, in v1 form.

2. **It's the acoustic stand-in pattern:** hand-crafted feature vector (16 features for MIDI; MFCC/energy/brightness/tempo for audio) → projected embedding → cosine/greedy nearest-neighbour chaining (`optimal_order`). The roadmap to a learned audio-JEPA is in `research/vibe-matcher-2026-08-16.md` — read next.

3. **Directionality matters.** Continuity is computed *A-tail → B-head*, not symmetric cosine. My conversation-similarity weights may also want direction (how one conversation's ending flows into another's beginning), not just static similarity.

4. **`elephant_sense_probe.py`** — probes the elephant's sense; likely holds the dial-readings logic for The Tap. Scout follow-up: read it.

## Open question it sharpens

topic.md Q2 asked: is comparable sameness a cosine over reading-vectors or something the JEPA predicts directly? `vibe_matcher.py` shows a third option: **a hand-weighted delta-composite over dial-style features**, interpretable and tunable before any learning happens. That's probably the v1 for conversations too.

## Follow-ups

- [ ] Read `research/vibe-matcher-2026-08-16.md`
- [ ] Read `elephant_sense_probe.py`
- [ ] Compare with elephant README's dial set (warmth, κ, joke-landing…)
