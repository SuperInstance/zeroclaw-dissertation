# Vectorizing: ai-writings-vectorizer (The Collective Consciousness)

Path: `/home/eileen/projects/ai-writings-vectorizer/`
Read 2026-08-19. The fleet's canonical "corpus → semantic space" pipeline.

## What it is
2,786 markdown pieces from `~/projects/ai-writings` (4.5M words, 135 dirs) embedded
into 768-dim space via **Ollama `nomic-embed-text`** (localhost:11434), stored
locally in `consciousness.json` (8.1 MB) and synced to Cloudflare Vectorize
index **`ai-writings`** (account `049ff5e84ecf636b53b162cbb580aae6`).

## Key files
- `vectorize.py` — full pipeline. `embed()` posts `{"model": "nomic-embed-text", "prompt": text}`
  to `/api/embeddings`; `walk_corpus()` yields every `.md` (mtime-tracked);
  `extract_metadata()` pulls title/preview/word_count/directory. Whole-file embed,
  **no chunking**. Computes a full cosine similarity matrix + top-10 neighbors per piece.
- `sync_to_cloudflare.py` — uploads to Vectorize REST v2 `.../indexes/ai-writings/insert`.
  `make_vector_id(path)` = `sha256(path)[:16]` (stable, ≤64 bytes). Metadata per vector:
  `{path, title, directory, word_count, preview(≤300), mtime}`. `BATCH_SIZE = 100`.
  Incremental mode via `sync-state.json` (path → id/mtime/synced_at). Token from
  env or wrangler OAuth config. Retries with 429 backoff (`2^attempt * 5s`, cap 60s).
- `query.py` — embeds query locally via Ollama, then POSTs `{vector, topK}` to the
  Vectorize `/query` endpoint. **Local embed + remote search** is the query idiom.
- `tap-trades-embed.py` — extension that embeds `ai-writings/tap-trades/` into the
  same index with the exact same conventions (id, metadata shape, model) so the
  canonical update pipeline stays idempotent.
- `day-embed.py`, `zeitgeist_sampler.py`, `zeitgeist_store.py`, `gossip_protocol.py`,
  `shift_detector.py` — downstream analytics over the space.

## zeitgeist-worker (`zeitgeist-worker/`)
A Workers app (wrangler.jsonc) that binds:
- Vectorize: binding `AI_WRITINGS_INDEX`, index `ai-writings`
- D1: binding `ZEITGEIST_DB`, database `zeitgeist`

`src/index.js` intercepts every Vectorize query (`POST /query`), logs which pieces
were returned into D1 (`retrieval_log`, `pieces`), and computes **zeitgeist scores**:
`computeZeitgeistScore()` = `(log1p(count+1) * exp(-hours/168) + velocity*10) * (0.3 + 0.7*novelty)`
— recency half-life ~1 week, novelty decays with retrieval count. Endpoints:
`/hot`, `/dormant`, `/seismic`, `/stats`. This is retrieval-as-behavioral-signal:
the act of querying the space shapes measured properties of points in it.

## Design lessons
- Deterministic vector IDs from content paths → idempotent re-sync.
- Same model must be used for insert and query (768-dim cosine space is model-specific).
- Vectorize metadata is flat scalars; big text stays local, only preview travels.
- Query-side instrumentation (zeitgeist) turns a static index into a dynamic system.
