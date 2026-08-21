# Vectorizing: Plainsong (The Score — notation → a searchable feel-space)

Path: `/home/eileen/projects/plainsong/` (Python), plus `plainsong-mcp` (Python) and
`plainsong-worker` (TypeScript, on GitHub as **TapScript Worker**). Read 2026-08-19 by
Lucineer. This is the fleet's notation layer; the point of vectorizing it is to give the
ship's music a *memory and a feel-retrieval system* on the edge.

## What Plainsong is

Plain-text music notation that compiles to MIDI and audio. The core idea: **you never
declare durations — you write how many events happen in a bar and the bar divides itself.**
Rows line up in `|`-separated bars; `Chords:`, `Melody:`, `Lyrics:` and `@player` rows
sound together. Zero required dependencies (CI-enforced across Py3.10–3.13 × 3 OSes).
6,321 `.song` files in the repo compile (3,824 of them chord-chart-only in `plainsong/songbook/`).

The pipeline (`pipeline.py::compile_text`) is one call: parse → arrange → render. Everything
above `notation/` + `render/` is optional. The repo is deliberately a compiler, not an app.

## The three things that make this the cleanest vectorization target in the fleet

**1. `features.py` already IS an encoder — a 16-dim, deterministic, model-free, *named*
embedding.** `FEATURE_NAMES` = note_density, avg_pitch, rhythmic_complexity,
harmonic_tension, register_spread, velocity_mean, velocity_std, syncopation,
contour_direction, interval_size, rest_ratio, chord_density, bass_register,
treble_activity, dynamic_range, sustain_ratio. Each bar → one vector, values in `[0,1]`
(`contour` signed). Normalized against **fixed `REFERENCES`**, not against the piece, so a
bar's numbers do not depend on the bars around it and two agents analyzing different
excerpts agree on the same bar. Pure stdlib, no state, analysis-only.

This is the crab-traps pattern taken to its semantic conclusion: crab-traps hashes TF-IDF
into 384 dims (deterministic but *opaque*); plainsong's 16 dims are deterministic **and
human-readable** — dim 3 *means* "harmonic tension," dim 7 *means* "syncopation." That is
what "intuitive system" buys you: the index is legible to a person, not just a nearest
neighbor.

**2. `fingerprint.py` gives a deterministic content ID for free.** `sha256[:16]` over a
canonical note stream (voice/role/program/pitch/start/duration/velocity/emission/arrival,
6-decimal places, sorted). Two builds agree on the digest iff they agree on the music. This
is the perfect Vectorize ID: `song-<digest>`, stable and idempotent.

**3. The songbook is a ready corpus.** 3,824 chord charts across a dozen languages
(`english/jazz`, `english/shanties`, `french/folk-traditional`, …), chord-progressions only
(melody/lyrics stripped for copyright — a progression is not protectable expression). Plus
13 examples and the edge-case files. No provenance problem, no cleaning needed.

## The fleet relationship (what vectorization plugs into)

| Repo | Role | Feeds / consumes Plainsong |
|---|---|---|
| `plainsong-mcp` | MCP server, 27 tools + **ensemble sessions** (many agents, one score; voice claims + versioned writes + deterministic merge) | `analyze_features` re-exports the 16 features |
| `fleet-jepa-midi` | JEPA perceives the *feel* (energy/tension/groove/direction) | consumes the SAME 16-feature vocabulary + `perform/conduct.py` directive JSON |
| `fleet-jepa-midi` | 12-pulse DAW | plays compiled events |
| `plato-music-sync` | Rust conductor (groove/counterpoint/cadence) | measures the fleet's alignment |
| `musician-soul` | persona evolution (32-dim soul_print) | digests the fake book, writes in its evolved voice |
| `flux-genome` | genetic evolution of traditions (25-gene dials) | breeds new traditions |
| `fleet-ensemble` | agentic performance | renders scores as performances |

`perform/conduct.py` is load-bearing for the elephant: it implements the fleet-jepa-midi
directive vocabulary (`lay_back`, `push_forward`, `anticipate`, `drag`, `straighten`,
`deepen_swing`, `float`, `lock_in`, `double_time`, `half_time` + `energy`/`density`/`tension`
scalars) as a pure function `(arrangement, directives) → arrangement`. The "feel" is a set of
named scalar knobs, exactly the dial-space the JEPA work reads.

## Naming collision (verified, worth recording)

`plainsong`'s README "Relation to the fleet" lists `plainsong-worker` as "Cloudflare Worker
version of this compiler." The actual GitHub repo `SuperInstance/plainsong-worker` is
**TapScript Worker** — a TypeScript Worker that compiles *TapScript* (v1 Roman-numeral /
v2 absolute) notation to MIDI on the edge. It is a sibling notation, not the plainsong
compiler itself, and its `wrangler.jsonc` has **no Vectorize/D1/R2 bindings yet** (only
account `049ff5e84ecf636b53b162cbb580aae6` + observability). `tapscript-studio` is itself a
plainsong fork (same README, same hero). Net: the edge compiler exists but is *not yet*
wired to any vector store — that is the greenfield gap this file addresses.

## Vectorization design — "plainsong-feel", an intuitive edge index

The design philosophy: **do not bolt on an ML encoder. The 16 features are the encoder.**
They are deterministic, model-free, stdlib-pure, human-named, and already the vocabulary the
JEPA bandleader speaks. Vectorizing plainsong = indexing the notation corpus by feel, not by
title.

- **Embedding = the 16-dim `BarFeatures.vector`**, L2-normalized. A TS port of `features.py`
  is trivial (it is ~200 lines of arithmetic over the arranger's output) and makes dev/prod
  byte-identical — the crab-traps "one hash, one index" discipline.
- **Index `plainsong-feel` (16-dim, cosine), multi-entity via ID prefix:**
  - `song-<sha256[:16]>` — per-song aggregate (mean of its bar vectors) + metadata
    `{title, key, tempo, meter, collection, dialect, bars, notes, preview}`
  - `bar-<digest>-<n>` — per-bar vectors (the resolution the bandleader reads at)
  - `coll-<name>` — collection centroids (e.g. `coll-english-shanties`)
  - `trad-<name>` — flux-genome tradition dials as a vector (3- or 25-dim projection)
- **D1 formalizes** (Vectorize proposes, D1 formalizes — the fleet idiom):
  - `songs` — the durable record (fingerprint, path, key/tempo/meter, collection, mtime)
  - `edges` — discovered similarity (`from_song, to_song, score, kind='discovered'`)
  - `ensemble_sessions` — the plainsong-mcp session state, lifted to D1 so several agents
    can co-author one score *across* the edge (claims/versions/merge already exist in Python)
  - `retrieval_log` — zeitgeist pattern: what the room reaches for, recency/velocity/novelty
- **Query idiom (intuitive):** "find songs that feel like this fragment" → parse the fragment,
  compute its 16-vector (in-worker or client-side), Vectorize query, D1 enrich. "Find a
  shanty in Am that swings" → D1 filter (collection/key) + Vectorize nearest to a target feel
  vector. The 16 dims make the *query* legible too — you can ask "more syncopation, less
  sustain" as an explicit vector edit rather than hoping a text embedding catches it.

## JEPA relevance (why this matters for the dissertation)

`fleet-jepa-midi` reads exactly these 16 features and the conduct-directive scalars
(`energy`/`tension`/`density`) as its perception layer — "the elephant's temperature sense"
applied to music. Vectorizing plainsong turns the notation corpus into the **co-linear-algebra
dataset substrate for musical feel**: a song's aggregate 16-vector is its temperature reading;
two songs' cosine is their comparable sameness; the `edges` D1 writes are durable graph
structure. The same propose-formalize loop that crab-traps runs over *rooms* and the
zeitgeist-worker runs over *retrieval* can run here over *songs* — and because the dims are
named, the resulting space is inspectable end to end. This is the intuitive system: a
searchable feel-space where the dimensions are musical, the IDs are fingerprints, the encoder
is zero-dependency, and the graph of "what sounds like what" accretes by use.

## Standing caveats

- **Dimension floor (verified 2026-08-19):** Vectorize rejects < 32 dims (`Dimensions must be in range: [32, 1536]`, code 3003). So the 16 features are used twice as **mean(16) ⊕ std(16) = 32 dims** (average feel + internal contrast), still fully named. Index `plainsong-feel` is 32-dim cosine.
- **Centering is load-bearing (verified 2026-08-19):** raw cosine over the chord-chart corpus **collapsed** — mean 0.997, sd 0.008 — because every chart shares the same DC signature (sustain≈1, rest≈0, syncopation≈0). Centering each dim against the corpus centroid before L2-normalize spreads it to mean 0.18 / sd 0.72, and nearest neighbors become musically sane (a jazz ballad's neighbors are jazz/ballads; a shanty's are distant, as they should be). The centroid lives in `tools/corpus-centroids.json`; both the indexer and `query_feel.py` must use it — the query side is what breaks silently if they drift.
- 16 dims is *small*; Vectorize handles it (max 1536) but the space is coarse. The aggregate
  (mean over bars) discards form — verse/chorus shape is lost. Consider per-section vectors
  (`section-<digest>-<name>`) if form matters.
- The songbook is chord-charts-only: the 16 features will be dominated by harmony/rhythm,
  with `rest_ratio`/`sustain_ratio`/melodic features near-zero on most files. The *examples*
  and any full-notation pieces are where the richer dims light up.
- The edge compiler (TapScript Worker) speaks TapScript, not plainsong; porting `features.py`
  to TS is the first real work, and it is honest to note the two notations differ.
