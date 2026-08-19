# The Elephant — JEPA as the Room-Temperature Sense

*Source: `/home/eileen/projects/elephant/README.md` (github.com/SuperInstance/elephant, built 2026-08-17, 49 tests)*

## The reframing

Casey (2026-08-17): **pure JEPA is not the answer.** JEPA is a *temperature sense* — attuned to the warmth/coldness of a room, with shaping effects on everything else. You acclimate like room temperature; you don't notice the elephant until you change rooms — and then it's a very different elephant.

Consequences:
- **The unit of perception is the ROOM, not the stream.**
- v2's "beat the 0.849 ordering" headline metric is RETIRED (a conductor's-baton question).
- v3 = room-state embeddings trained on **cold/warm contrast** + **acclimation curves** (agent→room) + **charisma** as measurable pull (room→agent).

## What it is

- **A room is a field, not a stream** (`elephant/room.py`): messages carry **gravity** (how hard they pull attention), rooms **reverberate** (past echoes in present), messages **ripple** (a joke ripples through laughter; fire ripples through panic). Plus windowed **density** — the room's pulse.
- **Many JEPA dials read it at once** (`elephant/dial.py`): one JEPA is a *dial* — one sense for one dimension. A `DialBank` reads the same room simultaneously. The ensemble of all readings is the **Field** — the elephant.
- **The elephant is only visible by contrast.** Inside one room it is invisible. The **sauna/cold-plunge gap** between rooms is the only training signal that matters.

## The dial bank (9 dials, all in `elephant/dials/`)

| Dial | Feels | Range |
|---|---|---|
| `mood` | warm/cold valence | [-1 cold, +1 warm] |
| `volume` | how loud the room talks | [0 quiet, 1 shouting] |
| `earnestness` | how much the room means it | [0 ironic, 1 sincere] |
| `cynicism` | eye-rolling | [0 earnest, 1 sneering] |
| `joke_landing` | the COLLECTIVE laugh or boo | [-1 booed, +1 roared] |
| `panic` | stampede sense | [0 calm, 1 trampling] |
| `presence` | pheromone trace of who's been here | [0 empty, 1 thrumming] |
| `model_vs_code` | model prose vs code generating the signal | [-1 code, +1 model] |
| `vision` | visual aliveness from camera frames (plato 16-dim) | [0 dark+empty, 1 bright+alive] |

v0 dials are **hand-crafted** keyword readers — naive on purpose (they saturate; can't catch sarcasm). Fleet pattern: hand-crafted first, learned second. v1 trains them via the `jepa.py` backbone (EMA + stop-gradient + VICReg over dial time-series).

## The field (`elephant/field.py`)

`RoomField` = the temperature vector:
- `warmth()` — felt temperature, ~[-1,+1]
- `concentration()` κ — v0 proxy `norm(vector−0.5)·2` measures extremity, not tightness; v3 makes it a **von Mises–Fisher tightness**: cold room = high κ (one way to be), warm room = low κ (many ways to be)
- `distance()` — the **elephant gap** between two rooms (training signal = contrast between rooms, never ordering within a stream)
- `sauna_plunge_gap()` — signed walk-in contrast
- `acclimation_curve()` — agent→room; the rate IS the agent's modulation skill
- `charisma_pull()` — room→agent over time/interactions

## Presets: zeitgeist vs personal (`elephant/presets.py`)

- **Room-Elephant** — the zeitgeist, objective, first-class. Reads through the plain bank with neutral defaults; two agents get the same field. Drives MUD descriptions / NPC vibes / input tokens everyone sees.
- **Personal-Elephant** — one agent's feel: `dial_weights` (taste), `bias` (disposition), `attachments` (intangible correlations: event key → memory — the perfume that is grandma's shop). The comparison between the two readings is "the observable of relationship."

## Spaces (`elephant/space.py`)

Core never knows what the space is. `Space` protocol + adapters (`MudSpace`, `ChatSpace`, `SensorSpace`, `AdapterRegistry`), four seams: `ingest()`, `.room`, `.tint_target()`, `send_back(field)`. "One sense, many rooms."

## How it's tested/computed

- Hand-crafted → contrast: three real fleet rooms (Tap / Chapel / Wheelhouse) show the elephant gap (demo: Tap warmth +0.29 vs Wheelhouse −0.05, distance 0.83).
- **Sea legs** (`sensors.py`, `fleetmath.py`): `RadarCoherenceDial`, `SounderBiomassDial`, `FishingDayDial`; `three_reading_kinematics()` (direction/speed/rate-of-change from exactly three readings), `fleet_concentration()` (vMF κ over boat positions), `biomass_anchor()`/`deviation()` (OAS-shrunken Mahalanobis over good-day features — induction without labels).
- **Nudge** (`nudge.py`): dial numbers → attention prior over modalities, blended at strength 0.15. **JEPA correlates; it never replaces.**
- **TapNightSession** (`tapnight.py`): peer-relative self-tuning of `dial_weights` across evenings — the guitarist principle (settings are discovered, not designed). 14 nights: writers→mood, poets→volume, engineers→cynicism; pairwise weight distance 0.389→0.859 (tastes diverge, don't collapse).
- Fleet simulation: 4 boats, 30 days, numbers-only exchange; dark-boat charisma rule reads a hole as attention.
- Roadmap: v1 train the dials; v2 learn the field end-to-end (vMF room-state embeddings, contrastive, percentile-rank acclimation, charisma as field displacement).

## Per-room vs per-conversation field

A conversation is one room at one window; the field is read over the room's windowed message set. Conversation-level JEPA is LOCAL-ONLY on boats (share numbers, never feeds). The room — not the conversation — is the persistent perceiving unit; rooms accumulate presence, acclimation, and anchors across conversations.
