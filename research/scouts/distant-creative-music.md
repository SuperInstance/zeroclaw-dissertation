# Distant Creative & Music Repo Scout
## Thesis: The Felt Size of the Step

---

## plainsong

### README: /home/eileen/projects/plainsong/README.md\n
# Plainsong

<p align="center">
  <img src="assets/images/hero-musicbox.jpg" alt="The band lives in the music — a music box open on a glowing sheet of plainsong" width="640">
</p>

[![PyPI](https://img.shields.io/pypi/v/plainsong.svg)](https://pypi.org/project/plainsong/)
[![Python](https://img.shields.io/pypi/pyversions/plainsong.svg)](https://pypi.org/project/plainsong/)
[![CI](https://github.com/SuperInstance/plainsong/actions/workflows/ci.yml/badge.svg)](https://github.com/SuperInstance/plainsong/actions/workflows/ci.yml)
[![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#hello-world)
[![License](https://img.shields.io/pypi/l/plainsong.svg)](https://github.com/SuperInstance/plainsong/blob/master/LICENSE)

Music notation you can write in any text editor, read like a lead sheet, keep in
version control, and compile to MIDI and audio.

```plainsong
[V1] (Verse - 4 Bars)
Chords: | Am . . . | F . . . | C . . . | G . . . |
Melody: | A4 . C5 E5 | F4 . A4 C5 | E4 . G4 C5 | D4 . F4 B4 |
Lyrics: | the tide  came | in  before  dawn | and  left  a | line  of  salt |
@bass   | a1 . e2 . | f1 . c2 . | c1 . g1 . | g1 . d2 . | vel: 70
```

That is the whole idea. Four rows that line up, bars separated by `|`, and a
file any editor, any diff tool and any language model can read.

**If you read music but not code**, you already understand most of that block —
it is a lead sheet with the bars drawn in. Start with
[Your first song](https://github.com/SuperInstance/plainsong/blob/master/docs/tutorial-first-song.md); it assumes nothing about
programming and gets you to something you can hear.

**If you write code but not music**, the thing to know is that you never
declare durations. You write how many events happen in a bar and the bar divides
itself. Start with [the notation reference](https://github.com/SuperInstance/plainsong/blob/master/docs/notation.md).

**If you are an agent**, read [AGENTS.md](https://github.com/SuperInstance/plainsong/blob/master/AGENTS.md) first. It is short, and
most of it is the mistakes other agents have already made here.

## Try it without installing anything


### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

`@anything` is a named player — `@bass`, `@piano`, `@horns`. Rows of different
| [Deck Work](https://github.com/SuperInstance/plainsong/blob/master/examples/plainsong-5-deck-work.song) | Several named players |

## plainsong-mcp

### README: /home/eileen/projects/plainsong-mcp/README.md\n
# plainsong-mcp

<p align="center">
  <img src="assets/images/hero.jpg" alt="Agents composing — the MCP seam between notation and sound" width="640">
</p>

A Model Context Protocol server for [Plainsong](https://github.com/SuperInstance/plainsong),
so any agent can read, write and compile music notation — and so several agents
can work on one score at the same time without overwriting each other.

```bash
plainsong-mcp                 # JSON-RPC over stdio, what most clients expect
plainsong-mcp --http          # loopback HTTP, for remote and multi-agent setups
plainsong-mcp --list-tools    # what it exposes
```

## Install

```bash
pip install git+https://github.com/SuperInstance/plainsong-mcp
```

That brings in the compiler as well. Neither has any other dependency: the
protocol, both transports, the session store and the compiler itself are
written against the standard library. Python 3.10 or newer.

The compiler comes from PyPI as `plainsong>=1.1.0`. That is the first release
carrying `plainsong.features`, the per-bar analysis this package re-exports
rather than duplicating, so the floor is a real requirement: below it the
install succeeds and the import fails.

## Point a client at it

For a client that launches servers over stdio, the usual shape is:

```json
{
  "mcpServers": {
    "plainsong": {
      "command": "plainsong-mcp"

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

carrying `plainsong.features`, the per-bar analysis this package re-exports
## Reading a score as features
`analyze_features` computes sixteen per-bar features — note density, harmonic
it had become its own thing rather than a feature of the compiler. Two names had

## plainsong-worker

### README: /home/eileen/projects/plainsong-worker/README.md\n
# TapScript Worker

**A [Cloudflare Worker](https://workers.cloudflare.com/) that compiles [TapScript](https://github.com/SuperInstance/tapscript-studio) notation to [MIDI](https://en.wikipedia.org/wiki/MIDI) on the edge — no server, no cold start, no dependencies.**

> *Write music in plain text. Get MIDI back. In 50ms. From anywhere on Earth.*

---

## Table of Contents

- [Vision](#vision)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Key Concepts](#key-concepts)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Further Reading](#further-reading)
- [Relation to the Fleet](#relation-to-the-fleet)

---

## Vision

[TapScript Studio](https://github.com/SuperInstance/tapscript-studio) proved that plain-text music notation works. But it's a local Python tool — you need Python installed, you need to run it on your machine, and the output stays local.

**TapScript Worker brings TapScript to the edge.** Write TapScript notation, POST it to a Cloudflare Worker, and get back a standard MIDI file. The compilation runs on [Cloudflare's edge network](https://workers.cloudflare.com/) — meaning it's fast (~50ms), it's always available, and it's free under the Workers free tier.

The worker includes a built-in HTML playground (no setup required) and a JSON API for programmatic access. It compiles both TapScript v1 (Roman numeral) and v2 (absolute pitch) notation.

### Why a Worker?

| Local Python Script | Cloudflare Worker |
|---|---|
| Requires Python + [pretty_midi](https://craffel.github.io/pretty-midi/) installed | Zero dependencies — just a URL |
| Output stays on your machine | Accessible from any browser or API client |
| Cold start: ~2s (Python) | Cold start: ~5ms ([V8 isolate](https://v8.dev/blog/embedded-v8-designs)) |
| No rate limiting | Built-in per-IP rate limiting (30 req/min) |
| Only works locally | Works from anywhere via HTTP |

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

No matching thesis-relevant mechanisms found

## tapscript-studio

### README: /home/eileen/projects/tapscript-studio/README.md\n
# Plainsong

<p align="center">
  <img src="assets/images/hero-musicbox.jpg" alt="The band lives in the music — a music box open on a glowing sheet of plainsong" width="640">
</p>

[![PyPI](https://img.shields.io/pypi/v/plainsong.svg)](https://pypi.org/project/plainsong/)
[![Python](https://img.shields.io/pypi/pyversions/plainsong.svg)](https://pypi.org/project/plainsong/)
[![CI](https://github.com/SuperInstance/plainsong/actions/workflows/ci.yml/badge.svg)](https://github.com/SuperInstance/plainsong/actions/workflows/ci.yml)
[![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#hello-world)
[![License](https://img.shields.io/pypi/l/plainsong.svg)](https://github.com/SuperInstance/plainsong/blob/master/LICENSE)

Music notation you can write in any text editor, read like a lead sheet, keep in
version control, and compile to MIDI and audio.

```plainsong
[V1] (Verse - 4 Bars)
Chords: | Am . . . | F . . . | C . . . | G . . . |
Melody: | A4 . C5 E5 | F4 . A4 C5 | E4 . G4 C5 | D4 . F4 B4 |
Lyrics: | the tide  came | in  before  dawn | and  left  a | line  of  salt |
@bass   | a1 . e2 . | f1 . c2 . | c1 . g1 . | g1 . d2 . | vel: 70
```

That is the whole idea. Four rows that line up, bars separated by `|`, and a
file any editor, any diff tool and any language model can read.

**If you read music but not code**, you already understand most of that block —
it is a lead sheet with the bars drawn in. Start with
[Your first song](https://github.com/SuperInstance/plainsong/blob/master/docs/tutorial-first-song.md); it assumes nothing about
programming and gets you to something you can hear.

**If you write code but not music**, the thing to know is that you never
declare durations. You write how many events happen in a bar and the bar divides
itself. Start with [the notation reference](https://github.com/SuperInstance/plainsong/blob/master/docs/notation.md).

**If you are an agent**, read [AGENTS.md](https://github.com/SuperInstance/plainsong/blob/master/AGENTS.md) first. It is short, and
most of it is the mistakes other agents have already made here.

## Try it without installing anything


### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

`@anything` is a named player — `@bass`, `@piano`, `@horns`. Rows of different
| [Deck Work](https://github.com/SuperInstance/plainsong/blob/master/examples/plainsong-5-deck-work.song) | Several named players |

## tapscript-worker

### README: /home/eileen/projects/tapscript-worker/README.md\n
# TapScript Worker

**A [Cloudflare Worker](https://workers.cloudflare.com/) that compiles [TapScript](https://github.com/SuperInstance/tapscript-studio) notation to [MIDI](https://en.wikipedia.org/wiki/MIDI) on the edge — no server, no cold start, no dependencies.**

> *Write music in plain text. Get MIDI back. In 50ms. From anywhere on Earth.*

---

## Table of Contents

- [Vision](#vision)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Key Concepts](#key-concepts)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Further Reading](#further-reading)
- [Relation to the Fleet](#relation-to-the-fleet)

---

## Vision

[TapScript Studio](https://github.com/SuperInstance/tapscript-studio) proved that plain-text music notation works. But it's a local Python tool — you need Python installed, you need to run it on your machine, and the output stays local.

**TapScript Worker brings TapScript to the edge.** Write TapScript notation, POST it to a Cloudflare Worker, and get back a standard MIDI file. The compilation runs on [Cloudflare's edge network](https://workers.cloudflare.com/) — meaning it's fast (~50ms), it's always available, and it's free under the Workers free tier.

The worker includes a built-in HTML playground (no setup required) and a JSON API for programmatic access. It compiles both TapScript v1 (Roman numeral) and v2 (absolute pitch) notation.

### Why a Worker?

| Local Python Script | Cloudflare Worker |
|---|---|
| Requires Python + [pretty_midi](https://craffel.github.io/pretty-midi/) installed | Zero dependencies — just a URL |
| Output stays on your machine | Accessible from any browser or API client |
| Cold start: ~2s (Python) | Cold start: ~5ms ([V8 isolate](https://v8.dev/blog/embedded-v8-designs)) |
| No rate limiting | Built-in per-IP rate limiting (30 req/min) |
| Only works locally | Works from anywhere via HTTP |

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

No matching thesis-relevant mechanisms found

## musician-soul

### README: /home/eileen/projects/musician-soul/README.md\n
# musician-soul

Vector database personas that learn musicians through MIDI digestion, develop their own "what-works" through jam sessions, and evolve from imitation into something with genuine musical identity.

## Why This Exists

A music AI that copies Miles Davis isn't Miles Davis — it's a photocopy. Real musical identity isn't about reproducing solos; it's about *digesting* influences and developing independent taste. This crate implements that process: MIDI files get parsed into phrases, phrases get embedded into 32-dimensional vectors capturing pitch contour, rhythm feel, dynamics arc, interval preferences, and register tendency. Those vectors go into a per-persona pattern database. When personas jam together, they reinforce or penalize patterns based on harmonic fit and surprise. Over time, the most successful patterns *mutate* into new generation-1 patterns that no MIDI file ever contained — that's the soul.

The architecture mirrors real musical development: start by copying your influences (generation 0), then through enough productive jam sessions, develop patterns that are yours alone (generation 1+). The `soul_print()` is the centroid of high-confidence patterns — the mathematical signature of what makes this persona unique.

## Architecture

```text
MIDI files ──► Phrase Extraction ──► MusicEmbedding (32-dim)
                                           │
                                           ▼
                                    PatternVectorDB
                                    ┌─────────────────┐
                                    │ Gen-0 patterns   │ ← from MIDI digestion
                                    │ Gen-1+ patterns  │ ← evolved through jamming
                                    │ Soul Print       │ ← centroid of confident patterns
                                    └─────────────────┘
                                           │
                                           ▼
                                    JamSession
                                    ┌─────────────────┐
                                    │ Persona A        │──┐
                                    │ Persona B        │──┼──► Output + Learning
                                    │ Persona C        │──┘
                                    └─────────────────┘
                                           │
                                    ┌──────┴──────┐
                                    │ harmony > 0.3│
                                    │ surprise > 0.2│
                                    └──────┬──────┘
                                           ▼
                                    Productive? → reinforce patterns
                                    Unproductive? → penalize patterns
                                    Gen-0 with >5 successes → spawn mutated Gen-1
```

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

# musician-soul
A music AI that copies Miles Davis isn't Miles Davis — it's a photocopy. Real musical identity isn't about reproducing solos; it's about *digesting* influences and developing independent taste. This crate implements that process: MIDI files get parsed into phrases, phrases get embedded into 32-dimensional vectors capturing pitch contour, rhythm feel, dynamics arc, interval preferences, and register tendency. Those vectors go into a per-persona pattern database. When personas jam together, they reinforce or penalize patterns based on harmonic fit and surprise. Over time, the most successful patterns *mutate* into new generation-1 patterns that no MIDI file ever contained — that's the soul.
The architecture mirrors real musical development: start by copying your influences (generation 0), then through enough productive jam sessions, develop patterns that are yours alone (generation 1+). The `soul_print()` is the centroid of high-confidence patterns — the mathematical signature of what makes this persona unique.
                                    │ Soul Print       │ ← centroid of confident patterns
- **`PatternVectorDB`** — Fixed-capacity vector store with eviction, K-nearest query, soul print computation
- **`MusicianPersona`** — A musician with influences, pattern DB, jam tracking, and emergent soul name
| Dim | Feature | Meaning |
use musician_soul::*;
// Check soul development
let report = jam.soul_report();
for (name, soul_pct) in report {
    println!("{}: {:.1}% soul", name, soul_pct);
- `.soul_print()` — Centroid of high-confidence patterns
- `.evolution_ratio()` — Fraction of evolved (gen>0) patterns
- `.soul_percentage()` — How much is the persona's own vs borrowed
- `.soul_report()` — Each persona's soul percentage
This is a prototype for *emergent musical identity*. The hypothesis: if you give a system enough influences, a mechanism for testing what works, and a feedback loop that rewards successful deviations, it will develop something that looks like artistic taste. The `soul_print()` isn't a metaphor — it's a concrete vector that represents what this persona has independently discovered works.
The generation counter is the key mechanism. Gen-0 patterns come from MIDI (imitation). Gen-1 patterns come from mutating successful Gen-0 patterns during jams (exploration). When a persona has enough Gen-1+ patterns, it "names its soul" — transitioning from "Miles-influenced" to something genuinely new.
- [`musician-soul-v2`](../musician-soul-v2) — Adds cross-persona influence graphs, genre emergence, temporal evolution, and call-response chains

## plato-music-sync

### README: /home/eileen/projects/plato-music-sync/README.md\n
# plato-music-sync

**Music cognition patterns for synchronizing Plato rooms.**

This crate uses music cognition theory to model and coordinate distributed room systems. The key insight: rooms ticking at different frequencies form a **polyrhythmic ensemble**. The engine room ticks at 0.2 Hz (slow bass), the backdeck at 2 Hz (fast percussion), the galley at 0.017 Hz (ambient drone). Music cognition provides the tools to keep them in sync.

## The Music-Cognition Isomorphism

Room synchronization and musical ensemble performance share deep structural parallels:

| Music Concept | Room Sync Analog |
|---|---|
| Polyrhythm | Multiple rooms at different tick rates |
| Groove | Fleet alignment / sync quality |
| Counterpoint | Productive vs wasteful room interactions |
| Cadence | Alarm → action → resolution patterns |
| Tempo | Adaptive tick rate adjustment |
| Rubato | Smooth tempo curves during transitions |

Every room is a voice in the ensemble. Every tick cycle is a rhythm. The fleet's health is the music it makes together.

## Modules

### `polyrhythm` — Polyrhythmic Scheduling

Coordinate rooms with different tick rates using LCM-based scheduling. Each room has a "time signature" derived from its tick frequency. The LCM of all tick rates (as rational numbers) gives the **master cycle** — the shortest period after which all rooms realign.

```rust
use plato_music_sync::PolyrhythmicScheduler;
use plato_music_sync::polyrhythm::Room;

let rooms = vec![
    Room { name: "engine".into(), tick_hz: 0.2 },   // Slow bass
    Room { name: "backdeck".into(), tick_hz: 2.0 },  // Fast percussion
    Room { name: "galley".into(), tick_hz: 0.017 },  // Ambient drone
];

let scheduler = PolyrhythmicScheduler::new(rooms);
println!("Master cycle: {} seconds", scheduler.master_cycle());
println!("Engine ticks per cycle: {}", scheduler.schedule_for("engine").unwrap().len());

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

| Groove | Fleet alignment / sync quality |
### `groove` — Groove Tracking
Measure how "in the groove" the fleet is. The **groove score** ranges from 0.0 (total chaos) to 1.0 (perfect sync). Each room's tick should land on the expected phase within the master cycle.
use plato_music_sync::GrooveTracker;
let mut tracker = GrooveTracker::new(100, 0.8); // window=100, threshold=0.8
// Check groove
    println!("Groove dropped to {} — sync correction needed!", tracker.groove());
The groove score uses exponential decay over phase errors: `groove = exp(-avg_error * 20)`. When groove drops below the configured threshold, it signals that sync correction is needed. The tracker uses a sliding window of recent events so groove can recover as rooms catch up.
**Connection to agent-groove:** The groove tracker's scoring model connects to agent-groove's groove scheduling model, which uses the same metric to decide when to rebalance work across the fleet.
│  │ Polyrhythmic │    │   Groove Tracker     │   │
│  │  Scheduler   │───▶│ (fleet alignment)    │   │
- **agent-groove** — Groove scheduling model for fleet-wide rebalancing decisions
The master cycle is the LCM of all periods. In this ensemble, the groove score tells you if the boat is running smoothly. The counterpoint analyzer tells you if engine and bilge are working productively together. The cadence detector tracks whether alarms are being properly resolved. And the tempo map adjusts tick rates when things heat up.
- 4 groove tests (perfect sync, late room, recovery, threshold)

## songforge

### README: /home/eileen/projects/songforge/README.md\n
# SongForge

> AI song covers from rough recordings, plus a research lab for transmission-chain experiments.

SongForge takes an old, imperfect recording of an original song and turns it
into a modern AI cover: separate the vocals, verify the melody, polish the
voice, generate a new performance, mix it back over the original instruments.
It also hosts a running experiment series — the **relay rounds** — that
studies what happens when a song is handed from voice to voice through a
chain of models, and measures the signal's fate in decibels.

**You'll need the song's lyrics.** SongForge verifies transcription against
them (`--compare`); the cover step takes them as input. It's a verification
tool as much as a generator.

## The Problem

You have an old recording. The vocals are buried, the mix is rough, and modern
AI cover tools can't even detect the melody in it. SongForge bridges the gap:

1. **Separates** vocals from instruments (Demucs source separation)
2. **Transcribes** the isolated vocals (Whisper) to verify against known lyrics
3. **Enhances** the vocal track (volume, EQ, optional de-noise)
4. **Generates** a new cover via AI music generation (MMX / MiniMax)
5. **Mixes** the cover with the original instrumental for a polished result

## Quick Start

```bash
pip install -r requirements.txt

# Cover a song from an imperfect recording
python -m songforge cover \
  --input song.mp3 \
  --lyrics "your lyrics here" \
  --style "acoustic indie folk, warm intimate vocals" \
  --output cover.mp3

# Just separate stems
python -m songforge separate --input song.mp3 --output-dir stems/

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

  analyze.py    — spectral precheck: measures spectral features for real
The experiments, not the covers, are the soul of this repo. Four TTS voices
  (anchor − X/2), the depth, and the sign of the feature. The joint

## music

⚠️  No README file found in /home/eileen/projects/music

## covers

### README: /home/eileen/projects/covers/README.md\n
# Covers

> *Three recordings of the same song, made in three different decades of the singer's life, in three different rooms, with three different understandings of what the song is about.*
> — [DeepSeek Production Prompts](v10_deepseek_prompts.md)

## What This Is

The fleet's music laboratory — **23,909 files** of cover song experiments generated through the [ACE-Step](https://github.com/SuperInstance/ACE-Step-1.5) pipeline, MMX (MiniMax-M3), and local model experiments. Starting from an 11-second phone recording of Casey's original song "One Day, I..." (E major, 110 BPM, vocals at -74 dB), the fleet has generated dozens of cover variations across genres: warm folk, indie folk, chamber folk, Nashville alt-country, ambient, blues, gospel, cello baroque, orchestral, synthwave, and full-band.

The project documents the full pipeline: audio separation (6 Demucs architectures, spectral filtering, AI enhancement), melody extraction (pyin, MIDI transcription), style transfer (ACE-Step v1-v6), and creative direction (DeepSeek production prompts describing three lifetimes of the same song).

## The Song

**"One Day, I..."** — Casey's original, 11.2 seconds, recorded on a phone. E major, 110 BPM, 128kbps. The vocals sit at -74 dB — below the noise floor. The voice and guitar are fused at the frequency level. No algorithm currently exists that can pull them apart cleanly.

From this seed, the fleet generated:
- **Session 5:** 12 variations across genres — warm folk to synthwave
- **Session 6 (ACE-Step v6):** 6 polished covers — Nashville confession, 3 AM kitchen, gospel hymn, Celtic ballad, blues crossroads, chamber/ambient
- **Three Decades, Three Rooms:** DeepSeek production prompts imagining the song recorded in a Joshua Tree gas station (age 60s), a Vermont hospice (age 70s), and Sound City (age 50s reunion)
- **MMX generations:** Warm folk (warmest track, 794 Hz centroid), polished folk (Bon Iver/Sufjan refs), ambient (most spacious, -16.63 LUFS)

## The Three Rooms

The [DeepSeek production prompts](v10_deepseek_prompts.md) are the creative heart of this repository. They imagine the same song across three decades of a singer's life:

1. **The Desert Recording (Joshua Tree)** — A man in his mid-sixties, lifetime smoker who quit. Neumann U 47 through Neve 1073. 1958 Martin 00-18. The room IS the reverb. "The whole record has the feeling of something being preserved rather than captured."

2. **The Hospice Session (Vermont)** — A man in his early seventies. Music therapy room, sage green walls. Shure SM7B, no reverb, no compression. Nylon-string guitar. "Whispers verses, finds almost-normal voice for chorus. Cries for two bars in the third verse and keeps singing."

3. **The Full Band Reunion (Sound City)** — A man in his late fifties. Five musicians who haven't been in the same room in 25 years. Studer A800 at 30 ips. "Misses a harmony cue, joins late, you hear the grin."

Each version is the same song. Each is completely different. The song doesn't change — the understanding of what the song is about changes.

## Sessions

| Session | Date | Tracks | Genres |
|---------|------|--------|--------|
| 25 | Aug 9, 2026 | 12 | warm folk, indie folk, chamber folk, nashville, ambient folk, blues, gospel, cello baroque, orchestral, synthwave, fullband, cabin folk |

## Structure

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

No matching thesis-relevant mechanisms found

## mist-game

### README: /home/eileen/projects/mist-game/README.md\n
# MIST — Tale of a Sheepdog Puppy 🐕🐑

A cozy browser game that teaches kids **how machines learn**. You play a young
sheepdog puppy herding a flock through misty meadows — and every mechanic *is*
an AI concept made playable. Sheep are data points, barking is an algorithm's
influence function, and flocking is emergence you can watch happen.

Built with **Next.js 16 (App Router) · TypeScript · Tailwind CSS 4 · shadcn/ui ·
Zustand · Prisma (SQLite)**. No canvas engine — the whole world is rendered with
DOM tiles, emoji sprites, and Framer Motion.

## Quick Start

```bash
npm install        # or: bun install
cp .env.example .env   # DATABASE_URL for Prisma (SQLite file)
npx prisma db push     # create the local SQLite database (legacy save API)
npm run dev            # http://localhost:3000
```

Other useful scripts:

| Script | What it does |
|---|---|
| `npm run build` | Production build (standalone output) |
| `npm start` | Serve the standalone production build (uses `bun`) |
| `npm run lint` | ESLint (Next core-web-vitals + typescript rules) |
| `npm run db:push` | Push Prisma schema to SQLite (`--accept-data-loss`) |
| `npm run db:generate` | Regenerate the Prisma client |

Player progress for the live game is stored in `localStorage`; the Prisma/SQLite

⚠️  [... middle content omitted — showing head and tail ...]


```python
from slackwater_art_spectrum import ArtCatalog, AssetCategory

catalog = ArtCatalog(repo_root=".")
catalog.scan()

for asset in catalog.by_category(AssetCategory.CHARACTER):
    print(f"{asset.filename} — {asset.era.value}, {asset.style.value}")

print(catalog.stats())
# {'total': 90, 'images': 85, 'audio': 5, 'categories': 10, ...}
```

### SpectrumAnalyzer
Analyzes the catalog for coverage gaps and balance across all dimensions.

```python
from slackwater_art_spectrum import SpectrumAnalyzer

analyzer = SpectrumAnalyzer()
report = analyzer.analyze(catalog)


### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

- [slackwater-perception](https://github.com/SuperInstance/slackwater-perception) — Multi-track MIDI perception

## slackwater-cognition

### README: /home/eileen/projects/slackwater-cognition/README.md\n
# Slackwater Dynamic Cognition Architecture

A novel system where a **fast "Local Thinker"** plays a game and journals its thoughts,
while a **slower "Conductor"** agent watches the thought stream and improves the
Local Thinker's prompts and parameters in real time.

This is **dynamic machine learning in a novel form**: the training signal is the
stream of consciousness itself, the loss function is play quality, and the gradient
is prompt/parameter adjustment — happening every 30 seconds, not every epoch.

## Architecture

```
Game State ──→ Local Thinker ──→ Thought Stream ──→ Conductor
    ↑              │                   │                │
    │              ▼                   ▼                │
    │         Action Selection    Journal (JSONL)   Prompt Update
    │              │                   │            Parameter Delta
    │              ▼                   ▼            Policy Update
    │         Game API            Training Data    Commentary
    │                                                  │
    └──────────────────────────────────────────────────┘
                    (feedback loop)
```

### Layer 1: The Local Thinker (Fast Iterator)

- **Cadence:** ~1 thought every 5 seconds
- **Model:** GLM via API (Phase 1), local Ollama model (Phase 2)
- **What it does:** Observes game state → thinks a thought → selects an action → journals everything
- **What it does NOT do:** Deep reasoning, complex planning, self-reflection (that's the Conductor's job)

Each thought cycle:
1. Fetch game state from Worker API (position, nearby objects, bond level, weather)
2. Build context window from state + system prompt + recent thoughts
3. Call LLM for a 2-4 sentence thought + action lean
4. Algorithmic action policy converts lean → concrete action (with cooldowns, curiosity bonuses)
5. Execute action via Worker API
6. Write thought to journal (JSONL + markdown)
7. Score quality (novelty, specificity, engagement, spatial awareness)

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

No matching thesis-relevant mechanisms found

## slackwater-perception

### README: /home/eileen/projects/slackwater-perception/README.md\n
# slackwater-perception

![tests](https://img.shields.io/badge/tests-104%20passed-brightgreen)
![version](https://img.shields.io/badge/version-0.1.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-blue)

Perceive the world as multi-track MIDI. This package encodes any experience — audio frames, text, game state — as a nine-track MIDI score where each perceptual dimension gets its own track: pitch, tempo, velocity, timbre, inflection, silence, gesture, intention, and attention. The result is not a recording but a score that captures the resonance between dimensions.

## Installation

```bash
pip install slackwater-perception
```

Dependencies: `mido`, `numpy`.

## The Nine Tracks

| Track | MIDI Encoding | Captures |
|---|---|---|
| `PITCH` | Note on/off | Fundamental frequency + harmonics |
| `TEMPO` | Meta `set_tempo` | BPM changes |
| `VELOCITY` | CC #7 (volume) | Intensity/weight of events |
| `TIMBRE` | CC #71–76 | Spectral color (warm, cold, nasal, breathy, bright) |
| `INFLECTION` | Pitch bend | Direction of pitch movement (rising, falling, flat) |
| `SILENCE` | Note on vel=0 | Rests between phrases |
| `GESTURE` | CC #80–87 | Physical/contextual cues (nod, look, point, breath, trade) |
| `INTENTION` | CC #74 | Pre-event prediction confidence |
| `ATTENTION` | CC #91 | Where focus is directed |

## API Reference

### MultiTrackEncoder

```python
from slackwater_perception import MultiTrackEncoder, PerceptionTrack, PerceptionEvent

MultiTrackEncoder(
    ticks_per_beat: int = 480,
    default_bpm: float = 120.0,

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

# slackwater-perception
pip install slackwater-perception
from slackwater_perception import MultiTrackEncoder, PerceptionTrack, PerceptionEvent
### PerceptionEvent
class PerceptionEvent:
A single event on a perception track. Convert to MIDI messages via `.to_midi_messages()`.
from slackwater_perception import PitchTracker
from slackwater_perception import VelocityMapper, VelocityCurve, VelocityConfig
from slackwater_perception import IntentionPropagator
from slackwater_perception import AttentionTracker
from slackwater_perception import ConvergenceDetector, ConvergenceEvent, ConvergenceStrength
Detects "in the pocket" moments — when all nine tracks align. The alignment metric Φ (phi) is computed as `√variance / (mean + ε)`. Low Φ = high alignment. Convergence is classified as `NONE`, `WEAK`, `MODERATE`, `STRONG`, or `PEAK`.
from slackwater_perception import MultiTrackEncoder
mid.save("perception.mid")  # 9-track MIDI file

## slackwater-harmony

### README: /home/eileen/projects/slackwater-harmony/README.md\n
# slackwater-harmony

![tests](https://img.shields.io/badge/tests-102%20passed-brightgreen)
![version](https://img.shields.io/badge/version-0.1.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-blue)

Cognitive friction monitoring and FEP-driven improvisation. This package implements a triadic architecture for measuring system-wide alignment: a Harmony Governor that tracks Φ (cognitive friction) per agent, an Executive that improvises when friction exceeds the deadband, a Groove Detector that spots system-wide harmony, and a Flow State layer that detects and protects the deepest state of player alignment.

## Installation

```bash
pip install slackwater-harmony
```

## Architecture

```
Layer 1 — Sandbox:        Forward simulation, hypothesis testing
Layer 2 — Governor:       Friction measurement, deadband enforcement
Layer 3 — Executive:      Improvisation when friction alarms fire

Flow layer extends all three with player-centric signals.
```

**Φ (phi) — Cognitive Friction:**

```
Φ(t) = α · H(prediction_error) + β · L(compute) + γ · Δ(state)
```

Default weights: α=0.50, β=0.30, γ=0.20. When Φ exceeds an agent's deadband, the Governor fires a `FrictionAlarm`. The Executive wakes and improvises.

## API Reference

### HarmonyGovernor

```python
from slackwater_harmony import HarmonyGovernor, FrictionAlarm, AlarmSeverity

HarmonyGovernor(

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

Cognitive friction monitoring and FEP-driven improvisation. This package implements a triadic architecture for measuring system-wide alignment: a Harmony Governor that tracks Φ (cognitive friction) per agent, an Executive that improvises when friction exceeds the deadband, a Groove Detector that spots system-wide harmony, and a Flow State layer that detects and protects the deepest state of player alignment.
### GrooveDetector
from slackwater_harmony import GrooveDetector, GrooveState
GrooveDetector(
Watches the Governor for groove states. A groove requires all agents below deadband AND low Φ variance, sustained for `min_sustained_beats`.
detector.update(beat: int | None = None) -> GrooveState
detector.in_groove -> bool
detector.groove_quality() -> float    # 0.0–1.0
Extends GrooveDetector with four player-centric signals:
Modified by groove state: ×1.1 if in pocket, ×0.8 if disrupted.

## slackwater-tempo

### README: /home/eileen/projects/slackwater-tempo/README.md\n
# slackwater-tempo

![tests](https://img.shields.io/badge/tests-43%20passed-brightgreen)
![version](https://img.shields.io/badge/version-0.1.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-blue)

Tempo is the first-class citizen that everything else depends on. This package provides BPM tracking with smooth transitions (accelerando / ritardando), time-signature support, groove shaping (swing, push/drag, humanization), game-state tempo presets, player-behavior-to-BPM energy mapping, and a shared beat clock for agent synchronization.

## Installation

```bash
pip install slackwater-tempo
```

## Architecture

```
EnergyAdapter ──observes──▶ PlayerBehavior
       │
       ▼
   TempoMap ◀── GrooveEngine (swing, push/drag, presets)
       │
       ▼
  BeatClock (shared sync)
```

The `BeatClock` owns a `TempoMap` and provides convenience methods. The `EnergyAdapter` reads player telemetry and drives BPM transitions. The `GrooveEngine` shapes raw beats into felt time.

## API Reference

### TempoMap

```python
from slackwater_tempo import TempoMap, TimeSignature, TransitionCurve

TempoMap(
    bpm: float = 120.0,
    time_signature: TimeSignature | None = None,
)

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

Tempo is the first-class citizen that everything else depends on. This package provides BPM tracking with smooth transitions (accelerando / ritardando), time-signature support, groove shaping (swing, push/drag, humanization), game-state tempo presets, player-behavior-to-BPM energy mapping, and a shared beat clock for agent synchronization.
   TempoMap ◀── GrooveEngine (swing, push/drag, presets)
The `BeatClock` owns a `TempoMap` and provides convenience methods. The `EnergyAdapter` reads player telemetry and drives BPM transitions. The `GrooveEngine` shapes raw beats into felt time.
### GrooveEngine
from slackwater_tempo import GrooveEngine, GameState, TempoPreset
GrooveEngine(
groove.timing_offset(beat_in_bar: int = 0, is_off_beat: bool = False) -> float
groove.apply_preset(state: GameState, tempo: TempoMap, *, transition_time: float = 4.0) -> TempoPreset
groove.apply_agent_groove(agent_name: str) -> None
groove.is_in_the_pocket() -> bool
**Agent Grooves:**
### Full pipeline: energy → tempo → groove
from slackwater_tempo import BeatClock, GrooveEngine, EnergyAdapter, PlayerBehavior, GameState
groove = GrooveEngine(swing=0.55, push_drag_ms=2.0)
groove.apply_preset(GameState.STEADY, clock.tempo_map, transition_time=2.0)
offset = groove.timing_offset(beat_in_bar=clock.beat_in_bar())

## slackwater-tminus

### README: /home/eileen/projects/slackwater-tminus/README.md\n
# slackwater-tminus

![tests](https://img.shields.io/badge/tests-103%20passed-brightgreen)
![version](https://img.shields.io/badge/version-0.1.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-blue)

Predict-and-confirm timing that replaces polling. Declare future events with predicted completion times in beats. Subscribers confirm readiness. When quorum is met and the countdown reaches zero, precompiled scripts fire — zero latency, one notification, no polling. Countdowns are measured in beats, not seconds, integrating directly with `slackwater-tempo`'s BeatClock.

## Installation

```bash
pip install slackwater-tminus
```

## Core Concept

**Polling:** "Is it done yet? Is it done yet? Is it done yet?" — N messages.

**T-Minus:** "It will be done at beat 16." + "Confirmed." — 2 messages. The fire is just the trigger pull.

For a 60-second job polled at 0.5s intervals, T-Minus saves 118 messages (60× reduction).

## API Reference

### CountdownEvent

```python
from slackwater_tminus import CountdownEvent, CountdownState

CountdownEvent(
    name: str,
    predicted_beat: float,
    id: str = <auto>,
    quorum: int = 1,
    script: Callable | None = None,
    metadata: dict = {},
)

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

No matching thesis-relevant mechanisms found

## slackwater-forge

### README: /home/eileen/projects/slackwater-forge/README.md\n
# 🔥 Slackwater Forge

**Overnight GPU production line that produces a morning briefing.**

Slackwater Forge treats a local GPU (via [Ollama](https://ollama.ai)) as a production line. You define jobs, start the forge, and let it run overnight. In the morning, it synthesizes all the artifacts into a structured briefing.

```
$ forge run --session overnight --duration 8h
$ forge brief --format md --format html
```

## Features

- **Works with ANY Ollama model** — Granite, Qwen, Llama, Mistral, Phi, anything
- **Job spec system** — define what the forge works on (code review, creative writing, research, etc.)
- **Artifact tracking** — every output saved with metadata (model, tokens, timing)
- **Morning briefing** — AI-synthesized summary with priorities, findings, and recommendations
- **Offline mode** — generate briefings without Ollama (metadata-only synthesis)
- **Beautiful output** — markdown + styled HTML briefings
- **Cost: $0** — entirely local, no API keys, no cloud

## Install

```bash
git clone https://github.com/SuperInstance/slackwater-forge.git
cd slackwater-forge
pip install -e ".[dev]"
```

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) running locally
- At least one pulled model: `ollama pull granite3.1-dense:2b`

## Quick Start

### 1. Check your setup
```bash
forge models          # list available Ollama models

### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

## Features
  --prompt "Write a detailed backstory for an NPC named {name} who lives in a coastal fishing village." \

## ideation-games

⚠️  No README file found in /home/eileen/projects/ideation-games

## flux-genome

### README: /home/eileen/projects/flux-genome-rs/README.md\n
# flux-genome-rs

Rust port of [flux-genome](https://github.com/SuperInstance/flux-genome) — a genetic algorithm framework for evolving musical traditions in dial space.

## Overview

A `MusicalGenome` is a vector of 25 genes (`f64` in `[0, 5]`) encoding a musical tradition's position in "dial space". The phenotype is a 3-tuple `(harmonic, rhythmic, spectral)` computed by averaging each 8-gene block.

The `GeneticAlgorithm` evolves populations of genomes toward target dial positions using selection, crossover, and mutation.

## Usage

### Create a genome from a tradition

```rust
use flux_genome::MusicalGenome;
use rand::rngs::StdRng;
use rand::SeedableRng;

let mut rng = StdRng::seed_from_u64(42);
let genome = MusicalGenome::from_tradition("Jazz", &mut rng).unwrap();
println!("Jazz dial position: {:?}", genome.dial_position());
```

### Run evolution toward a target

```rust
use flux_genome::{MusicalGenome, GeneticAlgorithm};

let mut ga = GeneticAlgorithm::new(100, 0.1, 0.8, 3);
ga.initialize((2.5, 2.5, 2.5), None, Some(42));
ga.evolve(50);
println!("Best: {}", ga.best());
```

### Use built-in tradition DNA

```rust
use flux_genome::tradition_dna::TRADITION_GENOMES;


### Thesis-Relevant Insights (keywords: feature, groove, soul, alignment, crossover, flock, vibe, perception, latent, named, boid):

The `GeneticAlgorithm` evolves populations of genomes toward target dial positions using selection, crossover, and mutation.
### Run evolution toward a target
### Track evolution with logs
use flux_genome::{GeneticAlgorithm, evolution_log::EvolutionLog};
let mut log = EvolutionLog::new();
- **Crossover**: uniform, arithmetic, blend (BLX-α)

---

## TOP 5 TRANSFERABLE INSIGHTS
1.  **musician-soul**: Evolution of musical personas from borrowed influence patterns (gen-0, derived from MIDI digestion) to emergent, original identity (gen-1+ mutated patterns) via jam-based reinforcement learning, with a quantifiable `soul_print()` centroid vector that captures unique artistic taste.
2.  **plainsong-mcp**: 16 named per-bar feature vectors (including note density, harmonic structure, and dynamic contour) for standardized music notation analysis, enabling granular, machine-readable measurement of musical latent space.
3.  **slackwater-harmony + slackwater-perception**: Combined alignment metrics (`Φ` cognitive friction score and groove quality) that quantify when distributed systems or musical ensembles are "in the pocket", providing a measurable signal for the "felt size of the step" between aligned states.
4.  **flux-genome-rs**: Genetic crossover, selection, and mutation of musical tradition dial-position vectors, allowing quantitative evolution of musical styles across a defined latent space to study comparable sameness across traditions.
5.  **covers repo**: Radical recontextualization of a single source song across decades, physical spaces, and interpretive prompts, demonstrating that perceived sameness of a work comes from interpretive continuity rather than fixed audio or notation — directly addressing the thesis's core question of felt vs. literal identity.