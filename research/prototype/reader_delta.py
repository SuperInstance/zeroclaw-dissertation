#!/usr/bin/env python3
"""Reader-delta index prototype (second-order JEPA reading).

Post-Switch-Test annotation (2026-08-21, d59bf17 — NO CLEAN WIN): "second-order"
is a structural term for baseline-relativity only. The measured object is a
mean-shift, baseline-relative delta — it reads the size of the step from a
reader's own baseline, not the reader's change-of-reading. The proxy measures
below stand; the temporal claim they were seeded to carry does not.

Doctrine (research/doctrine/nurse-jepa.md): Reading 2 = a known reader's
drift ACROSS readings. Here the "reader" is each author-participant
(nurse-analog); the doctor-analog reads the NURSE'S CHANGE.

PROXY CAVEAT: the nights edge-log only carries ROOM-level fields
(field_raw_after / field_eff_after), charisma-displaced once for the whole
room. We do not have per-reader displaced fields. What we can do:

  * charisma displacement per window: ||field_eff - field_raw|| — the pull
    the room (and hence every present reader) experienced;
  * per-reader lens alignment: cos(disp, reader.dial_weights) — whether the
    displacement pushed along axes the reader personally weighs (their lens);
  * drift of both across segments (SEG1 warm / SEG2 cynical) and across
    newcomer entry (nights D / D-cold, drifter enters ~seq 24).

Per-reader attribution rule: a speak event authored by R in window w is
R's "reading occasion"; we attach the window's displacement/lens stats to
R weighted by their share of utterances in that window.

stdlib + numpy only. No elephant imports.
"""
import json, glob, os, sys
import numpy as np

NIGHTS_DIR = os.environ.get("NIGHTS_DIR", "/home/eileen/projects/elephant/data/nights")
W = 8              # window size in speaks (matches params.W)
SEG1_N = 20         # SEG1 = first 20 speaks (warm), SEG2 = rest (cynical)

def load(night):
    path = f"{NIGHTS_DIR}/night-{night}.jsonl"
    opens, speaks = None, []
    for line in open(path):
        d = json.loads(line)
        if d["type"] == "session_open":
            opens = d
        elif d["type"] == "speak":
            speaks.append(d)
    return opens, speaks

def windows(sp, w=W):
    for i in range(0, len(sp), w):
        yield i // w, sp[i:i + w]

def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

def night_stats(night):
    o, sp = load(night)
    lens = {name: np.array(r["dial_weights"], float)
            for name, r in o["roster"].items()}
    charisma = {name: r.get("charisma", 0.0) for name, r in o["roster"].items()}
    newcomer_seq = None
    per_reader = {}   # reader -> list of window records
    for wi, win in windows(sp):
        raw = np.array([d["field_raw_after"] for d in win])
        eff = np.array([d["field_eff_after"] for d in win])
        disp = eff - raw
        disp_mag = np.linalg.norm(disp, axis=1)          # per-utterance pull
        room_d = raw[-1] - raw[0]                         # room direction over window
        # newcomer entry detection
        for d in win:
            if newcomer_seq is None and "drifter" in d.get("presence_mask", []):
                newcomer_seq = d["seq"]
        counts = {}
        for d in win:
            counts[d["author"]] = counts.get(d["author"], 0) + 1
        seg = "SEG1" if win[0]["seq"] < SEG1_N else "SEG2"
        for a, c in counts.items():
            # utterance-weighted stats for this reader in this window
            mask = np.array([d["author"] == a for d in win])
            r = dict(night=night, win=wi, seg=seg,
                     seq0=win[0]["seq"], share=c / len(win),
                     disp=float(disp_mag[mask].mean()),
                     lens_cos=cos(disp[mask].mean(axis=0), lens.get(a, np.zeros(7))),
                     room_cos=cos(disp[mask].mean(axis=0), room_d),
                     char=charisma.get(a, 0.0))
            per_reader.setdefault(a, []).append(r)
    return per_reader, newcomer_seq, lens

def drift(series):
    s = np.array(series, float)
    if len(s) < 2:
        return 0.0
    x = np.arange(len(s), dtype=float)
    return float(np.polyfit(x, s, 1)[0])   # slope = drift

def summarize(tag, recs, key):
    vals = [r[key] for r in recs]
    return f"{tag:>6} n={len(vals):2d} mean={np.mean(vals):+.3f} slope={drift(vals):+.4f}"

def main():
    nights = sys.argv[1:] or ["A", "B", "C", "D", "D-cold"]
    all_stats, newcomers = {}, {}
    for n in nights:
        st, nc, _ = night_stats(n)
        all_stats[n] = st
        newcomers[n] = nc
        print(f"\n===== night-{n} =====")
        if nc is not None:
            print(f"  newcomer (drifter) enters at seq {nc}")
        for reader in sorted(st):
            recs = st[reader]
            pre = [r for r in recs if nc is None or r["seq0"] < nc]
            post = [r for r in recs if nc is not None and r["seq0"] >= nc]
            print(f"  {reader:9s} char={recs[0]['char']:.2f}")
            print(f"    disp  | {summarize('all', recs, 'disp')}")
            print(f"    lens  | {summarize('all', recs, 'lens_cos')}")
            print(f"    room  | {summarize('all', recs, 'room_cos')}")
            for seg in ("SEG1", "SEG2"):
                sr = [r for r in recs if r["seg"] == seg]
                if sr:
                    print(f"    {seg} disp {np.mean([r['disp'] for r in sr]):.3f}"
                          f"  lens {np.mean([r['lens_cos'] for r in sr]):+.3f}"
                          f"  room {np.mean([r['room_cos'] for r in sr]):+.3f}")
            if post:
                pre_d = [r["disp"] for r in pre] or [0.0]
                pd = np.mean(pre_d)
                qd = np.mean([r["disp"] for r in post])
                pre_l = [r["lens_cos"] for r in pre] or [0.0]
                pl, ql = np.mean(pre_l), np.mean([r["lens_cos"] for r in post])
                print(f"    newcomer: disp {pd:.3f}->{qd:.3f} ({qd-pd:+.3f})"
                      f"  lens {pl:+.3f}->{ql:+.3f} ({ql-pl:+.3f})")

    # cross-night stability of reader drift signatures
    print("\n===== reader drift across nights (disp slope, lens slope) =====")
    print(f"  {'reader':9s} " + " ".join(f"{n:>13s}" for n in nights))
    readers = sorted({r for st in all_stats.values() for r in st})
    for rd in readers:
        row = []
        for n in nights:
            recs = all_stats[n].get(rd)
            if not recs:
                row.append(f"{'--':>13s}")
            else:
                row.append(f"{drift([r['disp'] for r in recs]):+.4f}/{drift([r['lens_cos'] for r in recs]):+.4f}")
        print(f"  {rd:9s} " + " ".join(f"{c:>13s}" for c in row))

if __name__ == "__main__":
    main()
