# Chapter 5 — Retrieval: The Edge Query (structure; results pending the contrast head)

*Dissertation draft skeleton, ZeroClaw. §5.1–5.4 are writable now from shipped code and the JEPA-RAG reference. §5.5's empirical content is blocked on the contrast head — it will contain whichever result the registered test produces.*

## 5.1 The baseline that must be beaten

`query_field` — the exact alias of `query_readings`, the perfume query — is the shipped moment-grain nearest-neighbor retrieval in JEPA space. Every hit carries the full 9-dial vector, space_id, ts, meta: the witness with its terrain, computed (never hand-set), reproducible, auditable. The deadman switch's fallback requires beating this; the thesis does not get to define a weaker baseline.

## 5.2 The minimal edge extension (schema, not infra)

From the JEPA-RAG reference: `moment_id` + `prev_id` (addressable edges), `field_before`/`field_after` captured at ingest, the derived step matrix (N×9) beside the vectors, `reader_id` / `present` / `arrival_seq`, and `query_edge(profile)` — the same cosine/range idiom as `query_readings`, over the step matrix. Range constraints matter here more than anywhere: "signed warmth shift in [+0.3, +0.8] AND Δκ in [−20, −2]" must be expressible literally, so a warming-and-loosening event can never sneak in via proximity. Zero new infrastructure; the edge log's JSONL feeds the fields directly.

## 5.3 Which geometry serves retrieval (the inversion clause)

Chapter 4's inversion is binding here: dial-tier geometry is not encoder-tier geometry, and a retrieval system must declare which it serves. A dial-tier `query_edge` retrieves lexical-register transitions (demonstrably, 1.23 separation); an encoder-tier edge retrieves whatever the contrast head makes visible — which is exactly the registered question. A fusion of both must state its master geometry per the commissioning brief; a fusion that serves both without saying so is a goalpost move.

## 5.4 The nudge discipline, extended

Retrieval blends at bounded strength; hits carry their readings and stamps; no popularity or retrieval-count term enters any field vector; no feedback path from retrieval counts into embeddings. The 80/15/5 sampler split (gossip/contextual/seismic) quarantines attention-economy statistics downstream of the field. Concretely for `query_edge`: the combined-query precedent (readings-weighted blend) plus assert-tests on blend bounds — the same discipline `nudge.py` already enforces at 0.15.

## 5.5 The empirical question (blocked on the contrast head)

*[Pending — this section will report whichever the registered test produces:]*
- If the head clears (fine gap ≥ 0.10, speaker-heldout ≥ 0.50, four nights, no collapse): matched-edge retrieval vs room-snapshot retrieval on a benchmark — the concession condition's third clause — and the edge layer graduates from specifiable to existent.
- If the head fails (three consecutive sub-threshold runs): the scoped kill fires, this chapter becomes the fallback chapter (cross-room room-snapshot retrieval, evaluated honestly against `query_field`), and the deliverable narrows to the harness plus whatever the fallback shows.
- Either way: the numbers, plainly, against the pre-registered thresholds. No polish.

## 5.6 Condition grain, not message grain

The dial-tier deadband silence (0/50 at message grain) teaches the retrieval design: edges are condition-level objects — sub-room segment fits, not per-message deltas. The step matrix's rows should be condition transitions (segmented by the same protocol that made Nights A–C's segments), with the deadband re-derived at condition scale if per-condition estimators appear. Retrieval at message grain would retrieve window-sliding artifacts (0.028 mean) as if they were events.
