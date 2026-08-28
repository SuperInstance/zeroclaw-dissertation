# walks-bridge — the fabric→walks exporter (v1)

**Lane:** WALKS-BRIDGE (re-fired 2026-08-28 after the tmux-server death; the dead
run's draft is preserved in `_archive/`).
**Status: infrastructure only.** Synthetic fabric walks are generator-corpus tier,
not field tier. Nothing here is registered or sealed.

## 1. What bridges to what

The dissertation's "walks, not waves" survivor wants **walk records**: the path a
measured unit actually took, step by step, with replayable integrity. The
`tit_quilt_elixir` fabric already produces exactly that substrate for free — each
cell appends to an immutable, hash-chained journal
(`lib/tit_quilt_elixir/cell.ex` §journal):

```elixir
entry     = {seq, ts, kind, payload}                 # what happened
full      = {seq, ts, kind, payload, hash}           # what is stored
hash      = :erlang.phash2({entry, prev_hash})       # genesis: :fabric_start
```

This exporter translates one fabric cell's journal into one **walk** — a JSONL
hash chain the dissertation tooling can consume without a BEAM in sight.

## 2. Input contract — fabric journal export

One JSON document per cell (`sample/input/<cell_id>.json`), oldest-first (the
in-process journal list is newest-first; the export reverses it):

```json
{
  "cell_id": "cell-alpha",
  "entries": [
    {"seq": 1, "ts": 100000, "kind": "start",  "payload": {"pid": "#PID<0.1.0>"}},
    {"seq": 2, "ts": 100120, "kind": "bind",   "payload": {"name": "wobble", "arity": 1}}
  ]
}
```

Elixir terms are rendered to JSON losslessly-enough for export: atoms → strings,
tuples → arrays, `:fabric_start` → `"fabric_start"`, `{:error, :missing}` →
`["error", "missing"]`. The on-BEAM phash2 hashes ride along only as provenance;
the exporter re-chains with sha256 (phash2 is not stable across BEAM builds and
is not needed for export-side integrity).

## 3. Output — `walks.jsonl` schema `walks/1`

One line per **walk-step**, append order = fabric seq order:

| field | type | meaning |
|---|---|---|
| `walk_id` | string | the walk this step belongs to |
| `ts` | int | fabric monotonic timestamp (µs), pass-through |
| `cell_id` | string | emitting cell, pass-through |
| `opcode` | enum | one of `qm_bind` \| `link` \| `effect` \| `view` \| `tick` |
| `payload_digest` | hex | sha256 of the canonical fabric payload |
| `prev_digest` | hex64 or `"GENESIS"` | digest of the previous step in this walk; `"GENESIS"` opens a walk |
| `digest` | hex64 | sha256 over `prev_digest` + canonical step core — this is the chain link |
| `meta` | object | `{seq, kind, ...extras}` — fabric seq, original journal kind, genesis markers, miss annotations |

### Canonical form

`json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")`
— code-point-sorted keys, compact, UTF-8. No floats in digested fields.

### Digest construction

```
payload_digest = sha256(canonical(payload))
core           = {walk_id, ts, cell_id, opcode, payload_digest, prev_digest}
digest         = sha256(canonical(core))
```

`prev_digest` sits inside the hashed core — that *is* the "sha256 of
prev+entry" rule, in a form that survives JSON round-trips.

## 4. Kind → opcode mapping

| fabric kind | opcode | note |
|---|---|---|
| `bind` | `qm_bind` | a measurement binding is installed |
| `swap` | `qm_bind` | meta `"swap": true` — the binding identity changed |
| `link` | `link` | cell-to-cell edge receipt |
| `effect_run` | `effect` | outbound effect |
| `received` | `effect` | inbound arrival receipt |
| `set_dials` | `view` | the dial snapshot is the observable state view |
| `tick` | `tick` | heartbeat; effects + misses live in its payload |
| `start` | — (structural) | genesis: folds into first step's `meta.genesis`; emits no step alone |
| `restart` | — (structural) | **torn edge**: closes the current walk, opens the next |

Unknown kinds abort the export — strict, no silent dropping.

### Restarts (the torn walk)

A `restart` marker at seq N means the BEAM process died and the journal's life
ended there. The exporter **never splices across the tear**: steps after the
restart belong to a new `walk_id` = `<cell_id>#<life>` (life 1 is bare
`<cell_id>`), re-chained from `"GENESIS"`. The discontinuity is the data —
speech events can never offer this annotation; the fabric hands it over for
free.

### Misses

A tick payload's `effect_results` may contain `["error", "missing"]` — the
receiver was dead. The step is exported as `tick` with
`meta.miss = [target, ...]` so downstream walk analysis can see receipted
non-delivery without re-parsing payloads.

## 5. Invariants

1. **Chain integrity** — for every walk, step *n*'s `prev_digest` equals step
   *n−1*'s `digest`, and every `digest` recomputes from its six core fields.
   Verified by re-reading the emitted file after every run; a mismatch aborts
   with the offending `walk_id`/`seq`.
2. **Append-only** — steps appear in fabric seq order per walk; a walk, once
   closed by a restart, never reopens. Verification rejects regressions.
3. **Totality** — every non-structural journal entry maps to exactly one step;
   step count = entries − structural markers (with documented edge case: a
   trailing structural marker with no following entry maps to nothing).

## 6. Usage

```bash
python3 research/walks-bridge/exporter.py \
    --inputs 'research/walks-bridge/sample/input/*.json' \
    --output  research/walks-bridge/sample/walks.jsonl
```

Stdlib only, no subprocess, no network. Exits non-zero on any violation.
