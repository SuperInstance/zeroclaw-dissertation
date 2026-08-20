# Vectorizing Stack — Synthesis

Written 2026-08-19, scout session `vectorizing-stack-scout`. Sources: the four
skill files in this directory. One correction to the orientation brief:
`quilt-cloudflare` does not exist; `quilt` (TS/Rust cellular runtime) does.

## The stack at a glance

| System | Embedding | Dims | Index | Store | Where embedding happens |
|---|---|---|---|---|---|
| ai-writings-vectorizer | Ollama `nomic-embed-text` | 768 | Vectorize `ai-writings` (+ D1 `zeitgeist`) | local `consciousness.json` | local machine, whole-file, no chunking |
| zeitgeist-worker | (reuses above index) | 768 | `AI_WRITINGS_INDEX` binding | D1 `zeitgeist` | queries embed client-side |
| fleet-embed | Candle BERT (`all-MiniLM-L6-v2`) | 384 | none (OpenAI-compatible server :8788) | in-memory | local Rust, mean pool + L2 norm |
| crab-traps | deterministic hash TF-IDF (`generateEmbedding`) | 384 | Vectorize `crab-trap-lures` | D1 `crab-trap-catches` | inside the Worker, no model |
| plainsong | deterministic 16-feature per-bar (`features.py`, named musical dims) | 16 | Vectorize `plainsong-feel` (proposed) | D1 `songs`/`edges`/`ensemble_sessions` (proposed) | pure stdlib, portable to TS in-worker |

## Embedding models & dims
Two "real" encoders in the fleet: nomic-embed-text@768 (corpus-scale, Ollama) and
MiniLM-L6-v2@384 (fallback, Candle). Plus one model-free encoder (crab-traps'
hash TF-IDF, 384). **Dims don't mix** — each index is model+dim-bound.

## Vectorize index design
- Insert: REST v2 `/insert` batch 100, ids = `sha256(path)[:16]` or
  `catch-<id>` / `room-<id>` prefixes. Stable deterministic IDs → idempotent sync.
- Metadata: flat scalars only (`{path,title,directory,word_count,preview,mtime}`,
  `{agent,lure,room}`, `{name}`); nulls coerce to ""/0.
- Query: **client-side embed, remote search** (query.py) or **in-worker embed,
  binding search** (`env.VECTORIZE_INDEX.query(vector, {topK, returnMetadata:true})`).
- Multi-entity-type indexes via ID prefix + over-fetch-then-filter
  (`SEARCH_FETCH_K=32` → regex filter → top 8). Metric: cosine throughout
  (everything L2-normalized upstream).
- 429 backoff: exponential, cap 60s.

## Fallback strategy (layered)
1. Ollama local (primary, 768-d).
2. fleet-embed Candle server (cloud-down fallback, 384-d, OpenAI-shaped API).
3. crab-traps goes further: zero-model deterministic embedding + every vector op
   degrades to a clean no-op when the binding is missing — D1 alone still works.

## Emergent-behavior patterns already in production
- **Retrieval as signal** (zeitgeist-worker): every query logged to D1; scores
  combine frequency, recency (168h decay), velocity, novelty.
- **Centroid-as-entity** (crab-traps): a room's vector = normalized mean of its
  constituent vectors, recomputed bounded to recent history.
- **Vectorize proposes, D1 formalizes**: nearest neighbors in embedding space
  become `edges` rows with weights/kinds only if D1 confirms; similarity becomes
  durable graph structure.

## How this serves a JEPA conversation-temperature dataset
The dissertation needs: capture a conversation's vibe AND its JEPA readings,
compute **comparable sameness** between conversations, store it as a growing
**co-linear-algebra dataset**. Mapping onto existing machinery:

1. **One Vectorize index** (e.g. `conversation-vibes`, 384-d to allow in-Worker
   generation and Candle fallback parity) with ID prefixes:
   - `conv-<id>` — a conversation's aggregate vibe vector (centroid pattern from
     `updateRoomCentroid()`)
   - `turn-<n>` — per-turn or windowed readings (the `catch-<id>` pattern)
   - `dial-<name>` — fixed anchor vectors for named temperatures if dials are
     calibrated reference points rather than free coordinates
2. **JEPA embeddings as a new encoder tier**: nomic/MiniLM embed *text*; the JEPA
   predictor embeds *latent state*. Same downstream contract (`upsert/query`,
   flat scalar metadata) — serve it behind fleet-embed's `/v1/embeddings` shape.
3. **Comparable sameness = cosine via Vectorize query**; the weight lives in D1
   (`edges`-style: from_conv, to_conv, score, kind='discovered', timestamp) —
   exactly crab-traps' "propose-formalize" split. Dataset grows organically via
   cron (crab-traps' hourly-pass + reef_state claim-bucket pattern prevents
   double-fires).
4. **Zeitgeist instrumentation** analog: track *which conversations are compared
   to which* — retrieval frequency of a conversation's vector is itself a
   "resonance" signal (this idea is latent in zeitgeist-worker's design).

## Three most important architectural facts
1. **Local embed + remote search is the fleet idiom** — the encoder can be
   anything (Ollama, Candle, a future JEPA head) as long as model+dim are fixed
   per index and output is L2-normalized.
2. **Deterministic IDs + prefix namespaces + scalar-only metadata** make a single
   Vectorize index a multi-type, idempotently-synced semantic store.
3. **Similarity becomes durable structure only through D1** — Vectorize proposes
   neighbors, D1 formalizes weighted edges; zeitgeist adds temporal dynamics on
   top. The co-linear-algebra dataset is exactly this propose-formalize loop run
   over conversation-temperature vectors.
