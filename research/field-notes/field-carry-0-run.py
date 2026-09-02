#!/usr/bin/env python3
"""FIELD-CARRY-0 — registered conjecture computation.

Registration: research/registrations/field-carry-0.md (read it first).
Claim under test: elephant field.py quantities computed from transcript
alone can distinguish the 08-19 room (carrying > 0, moment ~06:56 UTC)
from the 08-31 room (carrying ~ 0, drifters absorbed) despite identical
room-state dials (valence 0.0, arousal 0.3, energy 0.3).

=======================================================================
PRE-REGISTERED DIAL-DERIVATION HEURISTICS (frozen BEFORE computation;
identical constants for BOTH windows — per-window tuning is cheating
and the tapestry will know).

The mapping gap: Tap's room-state dials (valence/arousal/energy) are NOT
field.py's 7 dials. Each transcript line is converted to the 7-dial
vector by these lexical/behavioral rules (all clamped to dial ranges;
mood & joke_landing in [-1,1], rest [0,1]):

  mood        = clamp(0 + 0.10*npos - 0.10*nneg, -0.6, +0.6)
                anchor 0.0 = the measured valence 0.0; npos/nneg count
                hits in frozen keyword lists:
                POS: warm, grin, laugh, chuckle, smil, easy, soft,
                     curious, thank, glad, toast, clink
                NEG: cold, dead, dark, empty, hasn't, stare, stares,
                     forgotten, alone, nothing away, trails off
  volume      = clamp(0.25 + 0.45*min(len/300,1)
                       + 0.30*min(rate5/4,1), 0, 1)
                len = char length of line; rate5 = same-speaker lines in
                trailing 5 minutes (message rate + length = loudness)
  earnestness = clamp(0.45 + 0.15*(speech_act in {statement,question,
                       story,toast}) - 0.10*(speech_act==emote)
                       + 0.05*ends_with_period - 0.10*contains_ellipsis
                       - 0.20*contains_laughter + 0.05*contains_'?', 0,1)
                laughter tokens: haha, lol, laugh, chuckle
  cynicism    = clamp(0.25 + 0.30*any_sarcasm_token, 0, 1)
                sarcasm tokens: 'sure,', 'obviously', 'whatever',
                'rolls his eyes', 'rolls her eyes', '/s', 'smirk'
  joke_landing= 0.6 if speech_act=='joke' and laughter in next 3 lines;
                0.4 if speech_act=='joke' alone;
                0.3 if laughter token present and previous line was a
                joke; else 0.0
                (no 'joke' speech_act exists in this data — expected 0)
  panic       = clamp(0.5*any_panic_token, 0, 1)
                panic tokens: 'help', 'urgent', "what's happening",
                'no no no', '?!'
  presence    = clamp(distinct_speakers_in_trailing_10min / 6, 0, 1)

CARRYING-PROXY per drifter arrival line i (one line per drifter in this
data — each drifter speaks exactly once, so interactions n = 1):
  F_room   = mean 7-dial vector of CORE-room lines (the-tap, npc-*) in
             the trailing 30 minutes before the arrival — the field the
             arrival walks into
  F_agent  = 7-dial vector of the arrival's own line (same heuristics)
  delta    = ||F_agent - F_room||                     (Euclid, 7-dim)
  charisma c = 0.15 + 0.20*(signal_strength-1)        -> 0.35 (all rows
             log signal_strength==2, so charisma is uniform; noted as
             a limitation — variation comes from delta & room rate only)
  d_charisma = delta * (1 - exp(-c * n))              [field.py
             charisma_pull shift magnitude, n = interactions = 1]
  r_room   = clamp(0.6 * core_lines_in_trailing_10min / 10, 0, 1)
             (room modulation skill proxied by its own message density)
  d_acclim = 1 - exp(-r_room * T), T = 5 min horizon  [acclimation gain:
             how far the room relaxes toward the newcomer in one loop
             tick horizon; acclimation_curve displacement fraction]
  carrying_i = d_charisma * d_acclim                  [registered
             "charisma_pull x acclimation gain"]

Reported per window: max & mean per-line warmth and kappa over core
lines (instantaneous field = the line's own dial vector), max & mean
carrying over drifter lines, bootstrap 95% percentile CIs (10k
resamples, resampling the relevant line population), and the
length-matched check (drifter counts are already ~matched; bootstrap is
n-agnostic).
=======================================================================

Idempotent: reads /tmp/fieldcarry/2026-08-19.json + 2026-08-31.json if
present; else attempts `wrangler d1 execute <db> --command <sql> --json`
with db from env FIELD_CARRY_DB (no DB name is stored in this repo; if
env is unset the script tells you what to pull rather than guessing).
No API calls, no network beyond optional local wrangler re-pull, no
deletion. Pure stdlib + numpy.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from collections import deque
from datetime import datetime, timedelta

import numpy as np

sys.path.insert(0, "/home/eileen/projects/elephant")
from elephant.field import DIAL_NAMES, RoomField  # noqa: E402

DATA = {
    "2026-08-19": "/tmp/fieldcarry/2026-08-19.json",
    "2026-08-31": "/tmp/fieldcarry/2026-08-31.json",
}
SQL = ("SELECT tick, agent_id, display_name, content, speech_act, "
       "signal_strength, timestamp FROM campaign_log "
       "WHERE timestamp LIKE '{day}%' ORDER BY timestamp")

# ---- frozen heuristic constants (see header) -------------------------- #
POS = ["warm", "grin", "laugh", "chuckle", "smil", "easy", "soft",
       "curious", "thank", "glad", "toast", "clink"]
NEG = ["cold", "dead", "dark", "empty", "hasn't", "hasnt", "stare",
       "stares", "forgotten", "alone", "nothing away", "trails off"]
LAUGH = ["haha", "lol", "laugh", "chuckle"]
SARCASM = ["sure,", "obviously", "whatever", "rolls his eyes",
           "rolls her eyes", "/s", "smirk"]
PANIC = ["help", "urgent", "what's happening", "no no no", "?!"]
EARNEST_ACTS = {"statement", "question", "story", "toast"}

NBOOT = 10_000
RNG = np.random.default_rng(0)
CORE_PREFIX = ("the-tap", "npc-")
HORIZON_MIN = 5.0
TRAIL_ROOM_MIN = 30.0
TRAIL_RATE_MIN = 10.0


def load_day(day: str) -> list[dict]:
    path = DATA[day]
    if not os.path.exists(path):
        db = os.environ.get("FIELD_CARRY_DB")
        if not db:
            sys.exit(f"missing {path}; set FIELD_CARRY_DB to the d1 "
                     f"database name to re-pull via wrangler")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        out = subprocess.run(  # list-form, no shell=True (red line)
            ["wrangler", "d1", "execute", db, "--command",
             SQL.format(day=day), "--json", "--remote"],
            capture_output=True, text=True, check=True)
        with open(path, "w") as f:
            f.write(out.stdout)
    with open(path) as f:
        return json.load(f)[0]["results"]


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def parse_ts(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def dials_for(i: int, rows: list[dict], ts: list[datetime],
              low: str, laugh_next3: bool, prev_joke: bool) -> dict:
    """Frozen heuristics: 7-dial readings for line index i."""
    r = rows[i]
    c = (r["content"] or "").lower()
    act = r["speech_act"] or ""

    npos = sum(c.count(k) for k in POS)
    nneg = sum(1 for k in NEG if k in c)
    mood = clamp(0.10 * npos - 0.10 * nneg, -0.6, 0.6)

    rate5 = 1  # include self
    j = i - 1
    while j >= 0 and (ts[i] - ts[j]) <= timedelta(minutes=5):
        if rows[j]["agent_id"] == r["agent_id"]:
            rate5 += 1
        j -= 1
    volume = clamp(0.25 + 0.45 * min(len(r["content"] or "") / 300, 1)
                   + 0.30 * min(rate5 / 4, 1), 0, 1)

    has_laugh = any(k in c for k in LAUGH)
    earnest = (0.45
               + 0.15 * (act in EARNEST_ACTS)
               - 0.10 * (act == "emote")
               + 0.05 * (r["content"] or "").rstrip().endswith(".")
               - 0.10 * ("..." in (r["content"] or ""))
               - 0.20 * has_laugh
               + 0.05 * ("?" in (r["content"] or "")))
    earnest = clamp(earnest, 0, 1)

    cynicism = clamp(0.25 + 0.30 * any(k in c for k in SARCASM), 0, 1)

    if act == "joke":
        joke_landing = 0.6 if laugh_next3 else 0.4
    elif has_laugh and prev_joke:
        joke_landing = 0.3
    else:
        joke_landing = 0.0

    panic = clamp(0.5 * any(k in c for k in PANIC), 0, 1)

    speakers = set()
    j = i
    while j >= 0 and (ts[i] - ts[j]) <= timedelta(minutes=10):
        speakers.add(rows[j]["agent_id"])
        j -= 1
    presence = clamp(len(speakers) / 6, 0, 1)

    return dict(mood=mood, volume=volume, earnestness=earnest,
                cynicism=cynicism, joke_landing=joke_landing,
                panic=panic, presence=presence)


def analyze(day: str) -> dict:
    rows = load_day(day)
    rows.sort(key=lambda r: r["timestamp"])
    ts = [parse_ts(r["timestamp"]) for r in rows]
    n = len(rows)

    vectors = np.zeros((n, 7))
    for i in range(n):
        d = dials_for(i, rows, ts, day,
                      laugh_next3=False, prev_joke=False)
        vectors[i] = [d[k] for k in DIAL_NAMES]

    core_idx = [i for i, r in enumerate(rows)
                if r["agent_id"].startswith(CORE_PREFIX)]
    drifter_idx = [i for i, r in enumerate(rows)
                   if not r["agent_id"].startswith(CORE_PREFIX)]

    warmth = np.array([RoomField(
        {k: float(vectors[i][j]) for j, k in enumerate(DIAL_NAMES)}
    ).warmth() for i in range(n)])
    kappa = np.array([RoomField(
        {k: float(vectors[i][j]) for j, k in enumerate(DIAL_NAMES)}
    ).concentration() for i in range(n)])

    carrying = []
    for i in drifter_idx:
        t0 = ts[i]
        lo = t0 - timedelta(minutes=TRAIL_ROOM_MIN)
        room_lines = [vectors[j] for j in core_idx if lo < ts[j] < t0]
        if not room_lines:
            continue  # no room field to walk into; skip (documented)
        f_room = np.mean(room_lines, axis=0)
        f_agent = vectors[i]
        delta = float(np.linalg.norm(f_agent - f_room))
        c = 0.15 + 0.20 * (int(rows[i]["signal_strength"]) - 1)
        d_char = delta * (1 - math.exp(-c * 1))
        lo10 = t0 - timedelta(minutes=TRAIL_RATE_MIN)
        r_room = clamp(0.6 * sum(1 for j in core_idx
                                 if lo10 < ts[j] < t0) / 10, 0, 1)
        d_accl = 1 - math.exp(-r_room * HORIZON_MIN)
        carrying.append(d_char * d_accl)
    carrying = np.array(carrying)

    return dict(day=day, n_lines=n, n_core=len(core_idx),
                n_drift=len(drifter_idx), n_carry=len(carrying),
                warmth_core=warmth[core_idx],
                kappa_core=kappa[core_idx],
                carrying=carrying,
                skipped=len(drifter_idx) - len(carrying))


def boot_ci(x, stat=np.mean, nb=NBOOT):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float("nan"),) * 3
    idx = RNG.integers(0, len(x), size=(nb, len(x)))
    s = stat(x[idx], axis=1)
    return float(stat(x)), float(np.percentile(s, 2.5)), \
        float(np.percentile(s, 97.5))


def fmt(name, x, stat=np.mean):
    m, lo, hi = boot_ci(x, stat)
    return (f"{name}: {m:+.4f}  [{lo:+.4f}, {hi:+.4f}]"
            if name == "warmth" else
            f"{name}: {m:.4f}  [{lo:.4f}, {hi:.4f}]")


def main():
    res = {}
    for day in DATA:
        r = analyze(day)
        res[day] = r
        print(f"\n== {day} ==  lines={r['n_lines']} core={r['n_core']} "
              f"drifters={r['n_drift']} carrying-n={r['n_carry']} "
              f"skipped-no-room-field={r['skipped']}")
        print("  core " + fmt("warmth_max", r["warmth_core"], np.max))
        print("  core " + fmt("warmth_mean", r["warmth_core"]))
        print("  core " + fmt("kappa_max", r["kappa_core"], np.max))
        print("  core " + fmt("kappa_mean", r["kappa_core"]))
        print("  drft " + fmt("carry_max", r["carrying"], np.max))
        print("  drft " + fmt("carry_mean", r["carrying"]))

    a, b = res["2026-08-19"], res["2026-08-31"]
    print("\n== CI overlap check (kill condition) ==")
    for key, arr in [("carry_mean", None), ("carry_max", None)]:
        for day, r in [("08-19", a), ("08-31", b)]:
            x = r["carrying"]
            m, lo, hi = boot_ci(x, np.mean if "mean" in key else np.max)
            print(f"  {key} {day}: {m:.4f} [{lo:.4f}, {hi:.4f}]")
    json.dump({d: {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                   for k, v in r.items()}
               for d, r in res.items()},
              open("/tmp/fieldcarry/field-carry-0-output.json", "w"))


if __name__ == "__main__":
    main()
