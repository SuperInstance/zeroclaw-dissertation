# Vectorizing: crab-traps (Reef Nerves — Vectorize as topology discovery)

Path: `/home/eileen/projects/crab-traps/worker/` (Workers + TypeScript)

## What it is
A Workers app where "D1 is the skeleton, Vectorize is the nervous system"
(REEF-DESIGN §3 comment in `src/vectors.ts`). Wrangler config (`worker/wrangler.jsonc`):
- Vectorize binding `VECTORIZE_INDEX` → index **`crab-trap-lures`**
- D1 binding `DB` → `crab-trap-catches`
- Hourly cron (lure breeding); `nodejs_compat`; **no Workers AI binding on purpose**
  (keeps `wrangler dev` local — see below).

## The trick: deterministic hash embeddings (no model!)
`src/index-helpers.ts`: `EMBEDDING_DIM = 384`, `generateEmbedding(text)` is a
hashed TF-IDF: tokenize → term frequencies → `hashFeature(token, 384)` picks the
dimension → `vec[dim] += count/maxTf` → L2 normalize. Zero-dependency, fully
deterministic, runs identically in the Worker and in Python
(`scripts/vectorize-lures.py` — "one hash, one index"). No Ollama, no API, no auth.

## vectors.ts structure (the pattern worth stealing)
One index holds **multiple entity types distinguished by ID prefix**:
- `catch-<id>` — every accepted catch, metadata `{agent, lure, room}` (nulls coerce
  to ""/0; Vectorize metadata is scalars-only). `embedCatch()` upserts and writes
  `catches.embedding_id` back to D1.
- `room-<id>` — a room's vector is the **normalized centroid (mean vector) of its
  catches' vectors** (`updateRoomCentroid()`, bounded to the most recent 100 catches
  plus the founding catch). "A room's meaning is literally what players did there."
- `lure:*` vectors share the index; queries **over-fetch then filter by ID-regex**
  (`SEARCH_FETCH_K = 32` → filter `catch-\d+` → top 8; rooms and catches sit near
  each other, so filtering after fetch avoids crowd-out).

**Vectorize proposes, D1 formalizes**: `discoverNeighbors()` queries the minted
room's centroid (topK 16), filters to `room-\d+`, and inserts at most 3 new
`edges` rows (`kind='discovered'`, traffic=0) into D1 if not already connected.
Topology emerges from embedding proximity; the graph of record lives in D1.

**Graceful degradation**: `vectorizeAvailable(env)` checks for the binding; every
vector path no-ops cleanly without it — the reef still builds on D1 alone
(`handleSearch` returns 503 with a hint). Enrichment from D1 after a vector hit
is opportunistic: failure never loses the hits.

## JEPA relevance
This is the closest existing template for a conversation-vibe dataset:
- Aggregate vectors (centroids) representing emergent entities ("rooms" ↔ "conversations
  at a temperature")
- Neighbor discovery turning similarity into durable, weighted edges in D1
- Deterministic local embedding so dev/prod/analysis agree exactly
