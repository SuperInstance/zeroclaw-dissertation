# JEPA-RAG — Reference Summary (ZeroClaw, 2026-08-19)

*Full scout report: `~/.openclaw/workspace/research/jepa-rag-scout.md`. Source: `elephant/jepa_rag.py` + docs + tests.*

## What ships today (moment axis — honest, tested)

- **Moment schema:** `{text, readings (9 dials, computed by the DialBank — never hand-set), ts, space_id, meta}`.
- **Six numpy queries:** text (BoW cosine, zero-overlap masked), readings (raw cosine OR literal (lo,hi) range constraints — a panicky moment can never sneak in via proximity), field (alias of readings — "the perfume query"), time (hard window), space (hard filter, recency), combined (readings .5 / text .3 / time .1 / space .1).
- **Honesty guarantee (tested):** every hit carries the full reading vector + space_id + meta + text — the witness with its terrain, reproducible/auditable. Negative cosine = anti-aligned feeling, allowed.

## What it cannot do (edge axis — aspiration)

No reader identity (whose reading), no field_before/after (which transition), no arrival_seq (what order — ts is synthetic chunk order for markdown paths), no presence mask (presence is a scalar dial, not a set). G0 — the fleet's missing hippocampus ("who pulled whom") — lives exactly on this gap.

## Minimal edge extension (no new infra)

1. `moment_id` + `prev_id` (stable, addressable edges)
2. `field_before` + `field_after` dicts captured at ingest
3. derived `step` matrix (N×9) beside `_vectors`
4. `reader_id`, `present: set`, `arrival_seq`
5. `query_edge(profile)` — same cosine/range idiom over the step matrix

This is G0's "cheapest of all" enabling move: timestamp fidelity, no new ML. It is also the exact bridge between the vMF spec (which produces before/after fits) and retrieval — the edge log's JSONL feeds these fields directly.

## Dissertation relevance

- `query_field` is the fallback thesis's baseline (deadman switch: matched-edge retrieval must beat it).
- The combined-query weights (readings .5 / text .3) are the nudge discipline precedent — retrieval blends, never gates; extend the 0.15 blend-bound assert to `query_edge`.
- The reader_id delta is where the Personal-Elephant seam (open Q0) becomes concretely retrievable: one index per reader is the natural sharding, exactly as Lucineer steered.
