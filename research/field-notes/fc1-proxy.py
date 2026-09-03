#!/usr/bin/env python3
"""FIELD-CARRY-1 proxy computation — frozen carry-0 heuristics, unmodified.

Per A3 ordering: run AFTER the raw pull commit (770ee4e), BEFORE labeling.
Reads the in-window pull, computes the carrying-proxy for every in-window
drifter arrival, writes fc1-proxy-values.json. Constants identical to
field-carry-0-run.py (POS/NEG/LAUGH/SARCASM/PANIC lists, dial formulas,
c=0.35, 30-min trailing room field, 10-min density, 5-min horizon).
NO threshold logic here — threshold application happens in the eval step,
after labels exist.
"""
import json, math, sys
from datetime import datetime, timedelta
import numpy as np

CLAMP = lambda x, lo, hi: max(lo, min(hi, x))
POS = ["warm", "grin", "laugh", "chuckle", "smil", "easy", "soft",
       "curious", "thank", "glad", "toast", "clink"]
NEG = ["cold", "dead", "dark", "empty", "hasn't", "hasnt", "stare",
       "stares", "forgotten", "alone", "nothing away", "trails off"]
LAUGH = ["haha", "lol", "laugh", "chuckle"]
SARCASM = ["sure,", "obviously", "whatever", "rolls his eyes",
           "rolls her eyes", "/s", "smirk"]
PANIC = ["help", "urgent", "what's happening", "no no no", "?!"]
EARNEST_ACTS = {"statement", "question", "story", "toast"}
CORE = ("the-tap", "npc-")
PULL = "2026-09-03-partial-through-0410Z.json"
CUTOFF = "2026-09-03 00:02:00"

def dials(rows, ts, i):
    r = rows[i]; c = (r["content"] or "").lower(); act = r["speech_act"] or ""
    npos = sum(c.count(k) for k in POS); nneg = sum(1 for k in NEG if k in c)
    mood = CLAMP(0.10 * npos - 0.10 * nneg, -0.6, 0.6)
    rate5 = 1; j = i - 1
    while j >= 0 and (ts[i] - ts[j]) <= timedelta(minutes=5):
        if rows[j]["agent_id"] == r["agent_id"]: rate5 += 1
        j -= 1
    volume = CLAMP(0.25 + 0.45 * min(len(r["content"] or "") / 300, 1)
                   + 0.30 * min(rate5 / 4, 1), 0, 1)
    has_laugh = any(k in c for k in LAUGH)
    e = CLAMP(0.45 + 0.15 * (act in EARNEST_ACTS) - 0.10 * (act == "emote")
              + 0.05 * (r["content"] or "").rstrip().endswith(".")
              - 0.10 * ("..." in (r["content"] or ""))
              - 0.20 * has_laugh
              + 0.05 * ("?" in (r["content"] or "")), 0, 1)
    cyn = CLAMP(0.25 + 0.30 * any(k in c for k in SARCASM), 0, 1)
    panic = CLAMP(0.5 * any(k in c for k in PANIC), 0, 1)
    speakers = set(); j = i
    while j >= 0 and (ts[i] - ts[j]) <= timedelta(minutes=10):
        speakers.add(rows[j]["agent_id"]); j -= 1
    return np.array([mood, volume, e, cyn, 0.0, panic, CLAMP(len(speakers) / 6, 0, 1)])

def main():
    rows = json.load(open(f"research/field-notes/fc1-pulls/{PULL}"))[0]["results"]
    rows = [r for r in sorted(rows, key=lambda r: r["timestamp"]) if r["timestamp"] > CUTOFF]
    ts = [datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S") for r in rows]
    V = [dials(rows, ts, i) for i in range(len(rows))]
    core_idx = [i for i, r in enumerate(rows) if r["agent_id"].startswith(CORE)]
    out = []
    for i, r in enumerate(rows):
        if r["agent_id"].startswith(CORE): continue
        t0 = ts[i]
        room = [V[j] for j in core_idx if t0 - timedelta(minutes=30) < ts[j] < t0]
        if not room: continue
        delta = float(np.linalg.norm(V[i] - np.mean(room, axis=0)))
        r_room = CLAMP(0.6 * sum(1 for j in core_idx
                                 if t0 - timedelta(minutes=10) < ts[j] < t0) / 10, 0, 1)
        proxy = delta * (1 - math.exp(-0.35)) * (1 - math.exp(-r_room * 5))
        out.append(dict(agent_id=r["agent_id"], ts=r["timestamp"],
                        proxy=round(proxy, 4)))
    json.dump(out, open("research/field-notes/fc1-proxy-values.json", "w"), indent=1)
    vals = [o["proxy"] for o in out]
    print(f"in-window arrivals proxied: {len(out)}")
    for o in out:
        print(f"  {o['ts']}  {o['agent_id']:<20} proxy={o['proxy']}")
    if vals:
        print(f"\nthreshold 0.0865 -> proxy-positive: {sum(v >= 0.0865 for v in vals)}/{len(vals)}")

if __name__ == "__main__":
    main()
