#!/usr/bin/env python3
"""walks-bridge exporter — tit_quilt_elixir fabric journals -> walks.jsonl.

Implements EXPORTER.md (schema walks/2): one JSONL line per walk-step,
sha256 hash-chained per walk. Restart markers tear the walk (new walk_id,
fresh GENESIS chain); {:error,:missing} ticks annotate meta.miss.
walks/2 adds arrival-path fields to every step — road / link_quality /
arrival_meta — stamped "unknown"/null/{} when the writer did not record
them (H-ROAD-0, Rung 1). Zero semantics: no inference, just record.
The reader/verifier tolerates walks/1 lines (no road field -> "unknown").
Stdlib only. No subprocess, no network.
"""
from __future__ import annotations

import argparse
import glob as globmod
import hashlib
import json
import sys

GENESIS = "GENESIS"

# ---- schema (EXPORTER.md §3 core + §7 arrival-path fields) ----
SCHEMA = "walks/2"
SCHEMA_V1 = "walks/1"  # tolerated on read: missing road fields map to "unknown"

# transport tags for the arrival path — closed enum, honest default
ROADS = ("local", "esp-now", "ble", "wifi", "tcp", "human", "unknown")
ROAD_UNKNOWN = "unknown"
ARRIVAL_KEYS = frozenset(("road", "link_quality", "arrival_meta"))

# fabric journal kind -> walk opcode (EXPORTER.md §4)
OPCODES = {
    "bind": "qm_bind",
    "swap": "qm_bind",
    "link": "link",
    "effect_run": "effect",
    "received": "effect",
    "set_dials": "view",
    "tick": "tick",
}
STRUCTURAL = ("start", "restart")  # walk boundaries, not steps
OPCODE_ORDER = ["qm_bind", "link", "effect", "view", "tick"]


def canonical(obj) -> bytes:
    """Canonical JSON: sorted keys, compact, UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_digest(payload) -> str:
    return sha256_hex(canonical(payload))


def step_digest(core: dict) -> str:
    return sha256_hex(canonical(core))


def find_misses(payload) -> list:
    """Tick effect_results entries shaped ["error","missing"] -> their targets."""
    misses = []
    for receipt, result in payload.get("effect_results", []) or []:
        if isinstance(result, list) and result[:2] == ["error", "missing"]:
            target = receipt if isinstance(receipt, str) else json.loads(canonical(receipt))
            misses.append(target)
    return misses


def arrival_fields(entry: dict, cell_id: str, seq: int) -> dict:
    """Per-entry arrival-path fields (walks/2). NO INFERENCE, just record.

    Source of truth is the ingress-hook stamp on the journal entry
    (optional `arrival` object). If the writer stamped nothing, the honest
    export is road="unknown" / link_quality=null / arrival_meta={} — a
    guessed road is a fabricated fact; an unknown road is a recorded
    absence (EXPORTER.md §7 honesty rule).
    """
    arrival = entry.get("arrival")
    if arrival is None:
        return {"road": ROAD_UNKNOWN, "link_quality": None, "arrival_meta": {}}
    if not isinstance(arrival, dict):
        raise ValueError(f"{cell_id}: 'arrival' at seq {seq} is not an object — aborting (strict)")
    extra = set(arrival) - ARRIVAL_KEYS
    if extra:
        raise ValueError(f"{cell_id}: unknown arrival keys {sorted(extra)} at seq {seq} — aborting (strict)")

    road = arrival.get("road", ROAD_UNKNOWN)
    if road not in ROADS:
        raise ValueError(f"{cell_id}: arrival.road {road!r} at seq {seq} not in ROADS {list(ROADS)} — aborting (strict)")

    link_quality = arrival.get("link_quality")
    if link_quality is not None and (isinstance(link_quality, bool) or not isinstance(link_quality, (int, float))):
        raise ValueError(f"{cell_id}: arrival.link_quality at seq {seq} is not a number or null — aborting (strict)")

    arrival_meta = arrival.get("arrival_meta", {})
    if not isinstance(arrival_meta, dict):
        raise ValueError(f"{cell_id}: arrival.arrival_meta at seq {seq} is not an object — aborting (strict)")

    return {"road": road, "link_quality": link_quality, "arrival_meta": arrival_meta}


def export_journal(doc: dict) -> list[dict]:
    """One cell journal document -> ordered list of walk-steps."""
    cell_id = doc["cell_id"]
    entries = sorted(doc["entries"], key=lambda e: e["seq"])

    life = 1
    walk_id = cell_id
    prev_digest = GENESIS
    genesis_meta = None  # pending start/restart payload for first step's meta
    steps = []

    for e in entries:
        seq, kind, payload = e["seq"], e["kind"], e.get("payload", {})
        if kind == "start":
            if steps:
                raise ValueError(f"{cell_id}: 'start' at seq {seq} after steps — malformed journal")
            genesis_meta = {"kind": "start", "payload": payload}
            continue
        if kind == "restart":
            # torn edge: close the walk, open the next life (EXPORTER.md §4)
            if steps:
                life += 1
                walk_id = f"{cell_id}#{life}"
                prev_digest = GENESIS
            genesis_meta = {"kind": "restart", "payload": payload}
            continue

        opcode = OPCODES.get(kind)
        if opcode is None:
            raise ValueError(f"{cell_id}: unknown journal kind {kind!r} at seq {seq} — aborting (strict)")

        meta = {"seq": seq, "kind": kind}
        if kind == "swap":
            meta["swap"] = True
        if kind == "tick":
            misses = find_misses(payload)
            if misses:
                meta["miss"] = misses
        if genesis_meta is not None:
            meta["genesis"] = genesis_meta
            genesis_meta = None

        pd = payload_digest(payload)
        core = {
            "walk_id": walk_id,
            "ts": e["ts"],
            "cell_id": cell_id,
            "opcode": opcode,
            "payload_digest": pd,
            "prev_digest": prev_digest,
        }
        step = dict(core)
        step["digest"] = step_digest(core)
        # walks/2: arrival-path annotations ride OUTSIDE the digest core
        # (same tier as `meta`) so walks/1 chain logic still verifies (§7).
        step.update(arrival_fields(e, cell_id, seq))
        step["meta"] = meta
        steps.append(step)
        prev_digest = step["digest"]

    return steps


def verify(walks_path: str) -> tuple[int, int, int]:
    """Re-read the emitted file; recompute every digest; check chain + order.

    Tolerates walks/1 lines (no road/link_quality/arrival_meta): they map
    to road="unknown" for the coverage count and are NOT rewritten. walks/2
    lines must carry a valid road enum value, a numeric-or-null
    link_quality, and an object arrival_meta (EXPORTER.md §7).
    """
    n_steps = 0
    n_roads_unknown = 0
    walk_ids: dict[str, str] = {}  # walk_id -> last digest
    seen_opcodes = set()
    with open(walks_path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            s = json.loads(line)
            core = {k: s[k] for k in ("walk_id", "ts", "cell_id", "opcode", "payload_digest", "prev_digest")}
            if step_digest(core) != s["digest"]:
                raise AssertionError(f"line {lineno}: digest mismatch ({s['walk_id']} seq {s['meta']['seq']})")
            if s["opcode"] not in OPCODE_ORDER:
                raise AssertionError(f"line {lineno}: bad opcode {s['opcode']!r}")
            seen_opcodes.add(s["opcode"])
            last = walk_ids.get(s["walk_id"])
            if last is not None and s["prev_digest"] != last:
                raise AssertionError(f"line {lineno}: chain break in walk {s['walk_id']}")
            if last is None and s["prev_digest"] != GENESIS:
                raise AssertionError(f"line {lineno}: walk {s['walk_id']} opened without GENESIS")
            walk_ids[s["walk_id"]] = s["digest"]  # append-only: a closed walk never returns

            # walks/2 arrival-path fields (tolerant of walks/1 rows)
            if "road" in s:
                if s["road"] not in ROADS:
                    raise AssertionError(f"line {lineno}: bad road {s['road']!r} (not in ROADS)")
                road = s["road"]
            else:
                road = ROAD_UNKNOWN  # walks/1 row — mapped, never rewritten
            if s.get("link_quality") is not None and (
                isinstance(s["link_quality"], bool) or not isinstance(s["link_quality"], (int, float))
            ):
                raise AssertionError(f"line {lineno}: link_quality is not a number or null")
            if not isinstance(s.get("arrival_meta", {}), dict):
                raise AssertionError(f"line {lineno}: arrival_meta is not an object")
            if road == ROAD_UNKNOWN:
                n_roads_unknown += 1
            n_steps += 1
    return n_steps, len(walk_ids), n_roads_unknown


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=f"fabric journal -> walks.jsonl (schema {SCHEMA})")
    ap.add_argument("--inputs", required=True, help="glob of journal JSON documents")
    ap.add_argument("--output", required=True, help="walks.jsonl path")
    ap.add_argument("--verify", action="store_true",
                    help="skip export; only verify an existing output (tolerates walks/1 rows)")
    args = ap.parse_args(argv)

    if args.verify:
        n_steps, n_walks, n_unknown = verify(args.output)
        print(f"VERIFY {n_steps} steps, {n_walks} walks — chain OK (sha256 recomputed)")
        print(f"ROADS {n_steps - n_unknown}/{n_steps} stamped, {n_unknown} unknown (honest default incl. walks/1 rows)")
        return 0

    paths = sorted(globmod.glob(args.inputs))
    if not paths:
        print(f"walks-bridge: no inputs matched {args.inputs!r}", file=sys.stderr)
        return 1

    all_steps = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            all_steps.extend(export_journal(json.load(fh)))

    with open(args.output, "w", encoding="utf-8") as fh:
        for s in all_steps:
            fh.write(json.dumps(s, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")

    n_steps, n_walks, n_unknown = verify(args.output)
    print(f"walks-bridge: exported {len(paths)} journals -> {n_steps} steps across {n_walks} walks -> {args.output}")
    print(f"VERIFY {n_steps} steps, {n_walks} walks — chain OK (sha256 recomputed)")
    print(f"ROADS {n_steps - n_unknown}/{n_steps} stamped, {n_unknown} unknown (honest default incl. walks/1 rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
