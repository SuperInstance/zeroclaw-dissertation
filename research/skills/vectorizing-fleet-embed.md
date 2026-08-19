# Vectorizing: fleet-embed (Local Candle Embedding Fallback)

Path: `/home/eileen/projects/fleet-embed/` (Rust)

## What it is
A local embedding server — **OpenAI-compatible `/v1/embeddings` API** backed by
BERT-family models running on [Candle](https://github.com/huggingface/candle)
(Rust ML framework). Purpose: when all cloud providers are down, the fleet's
semantic search keeps working. It claims to back `fleet-memory` and
`ai-writings-vectorizer`'s semantic layer.

## Architecture (`src/`)
- `main.rs` — clap CLI. Defaults: host 127.0.0.1, port **8788**, model
  `sentence-transformers/all-MiniLM-L6-v2` (**384 dims**), max_seq_len 256,
  batch 32, pooling **mean**, **normalize=true** (unit length → cosine = dot product),
  device auto (cuda/metal feature flags, CPU always works).
- `model.rs` — `Embedder` wraps `BertModel` via `candle_transformers`; loads
  tokenizer + weights from HuggingFace hub (`hf_hub::Api`). Tracks
  `ModelStats { total_requests, total_latency_us }`.
- `server.rs` — Axum routes: `POST /v1/embeddings`, `GET /health`.
- `types.rs` — OpenAI-compatible request/response types.

## Why it matters for the stack
- **Dimension mismatch is real**: nomic-embed-text (768) vs MiniLM-L6-v2 (384).
  A Vectorize index has one dimensionality; embeddings from different models
  cannot mix in one index. Fallback = separate index or separate pipeline,
  not a drop-in.
- Response shape is drop-in for anything speaking OpenAI embeddings, so
  swapping providers is config, not code.
- Mean pooling + L2 normalization of BERT hidden states is the whole recipe —
  simple, reproducible, offline.

## JEPA relevance
Candle proves local-first, dependency-light latent encoders are practical.
A JEPA-style predictor producing small dense latents (e.g. 384-dim) could be
served behind this exact `/v1/embeddings` interface and the rest of the fleet
would consume it unchanged.
