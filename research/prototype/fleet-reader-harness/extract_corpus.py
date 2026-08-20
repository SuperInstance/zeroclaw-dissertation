#!/usr/bin/env python3
"""E3 corpus extraction — the frozen 27 real room-windows (SHA a423a378…).

The D″ fixture manifest pins 27 windows over the elephant nights corpus
(A, B, C, D, D-cold), windowed at W=8. The night logs carry only
text_sha256 per speak; the speak TEXTS are reconstructed verbatim from the
deterministic generator scripts (elephant/scripts/nights_abc.py) and every
reconstructed text is verified against the log's text_sha256. The manifest
SHA is re-verified (a423a3783a4a303f281e419d28359844990bcf312955a9eb18e636f753d56429).

Read-only against the elephant repo. Writes corpus/corpus.json here.

Registered in REGISTRATION-2026-08-19.md. Run BEFORE the field run.
"""
import hashlib
import json
import os
import sys

ELEPHANT = "/home/eileen/projects/elephant"
sys.path.insert(0, os.path.join(ELEPHANT, "scripts"))

FIXTURES = ("/home/eileen/projects/zeroclaw-dissertation/research/prototype/"
            "reader-delta-test/fixtures")
NIGHTS_DIR = os.path.join(ELEPHANT, "data", "nights")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "corpus", "corpus.json")

EXPECTED_SHA = "a423a3783a4a303f281e419d28359844990bcf312955a9eb18e636f753d56429"

# Dial native bounds (elephant.tapnight.DIAL_BOUNDS), for the reading scale.
DIAL_BOUNDS = {
    "mood": (-1.0, 1.0), "volume": (0.0, 1.0), "earnestness": (0.0, 1.0),
    "cynicism": (0.0, 1.0), "joke_landing": (-1.0, 1.0), "panic": (0.0, 1.0),
    "presence": (0.0, 1.0),
}
DIALS = list(DIAL_BOUNDS)
W = 8


def load_jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def sha256_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def main():
    # 1. Fixture manifest verification (the frozen corpus definition).
    raw = open(os.path.join(FIXTURES, "manifest.json"), "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    assert got == EXPECTED_SHA, f"fixture SHA drifted: {got}"
    manifest = json.loads(raw)
    wins = manifest["corpus_windows"]
    assert len(wins) == 27, len(wins)

    # 2. Reconstruct speak texts from the deterministic generator.
    from nights_abc import NIGHT_SCRIPT, night_d_script

    scripts = {}
    for night in ("A", "B", "C"):
        scripts[night] = NIGHT_SCRIPT
    scripts["D"] = night_d_script()
    scripts["D-cold"] = scripts["D"]  # identical script (roster timing differs)

    # 3. Verify every logged speak's sha against the reconstruction.
    logs, corpus_sd_rows = {}, []
    for night in ("A", "B", "C", "D", "D-cold"):
        rows = load_jsonl(os.path.join(NIGHTS_DIR, f"night-{night}.jsonl"))
        speaks = [r for r in rows if r["type"] == "speak"]
        speaks.sort(key=lambda r: r["seq"])
        logs[night] = speaks
        corpus_sd_rows += [r["field_raw_after"] for r in speaks]
        assert len(speaks) == len(scripts[night]), (night, len(speaks))
        for i, (row, (author, text, reactions)) in enumerate(zip(speaks, scripts[night])):
            assert row["seq"] == i, (night, i, row["seq"])
            assert row["author"] == author, (night, i, row["author"], author)
            assert row["text_sha256"] == sha256_text(text), \
                f"{night} seq {i}: text sha mismatch"
            assert row["reactions"] == (reactions or {}), (night, i)

    # 4. corpus_sd (E2-comparable): RMS over dials of the per-dial std of the
    #    raw room field, speak-level, over the 5 nights. Secondary: window-level.
    import math
    n = len(corpus_sd_rows)
    cols = list(zip(*corpus_sd_rows))
    means = [sum(c) / n for c in cols]
    var = [sum((x - m) ** 2 for x in c) / (n - 1) for c, m in zip(cols, means)]
    sd_speak = math.sqrt(sum(var) / len(var))
    M = [w["m"] for w in wins]
    mw = len(M)
    wcols = list(zip(*M))
    wmeans = [sum(c) / mw for c in wcols]
    wvar = [sum((x - m) ** 2 for x in c) / (mw - 1) for c, m in zip(wcols, wmeans)]
    sd_window = math.sqrt(sum(wvar) / len(wvar))

    # 5. Emit the corpus with verified texts.
    windows = []
    for idx, w in enumerate(wins):
        night, seq0, seg = w["night"], w["seq0"], w["seg"]
        speaks = logs[night][seq0:seq0 + W]
        assert W // 2 <= len(speaks) <= W  # fixture rule keeps partial tails
        group = "ABC" if night in ("A", "B", "C") else "D"
        windows.append({
            "id": f"{night}-w{w['win']}", "night": night, "win": w["win"],
            "seg": seg, "seq0": seq0, "distinct_group": group,
            "m": w["m"],
            "speaks": [{"seq": r["seq"], "author": r["author"],
                        "reactions": r["reactions"]} for r in speaks],
        })
    # attach texts directly from the verified script
    for win in windows:
        script = scripts[win["night"]]
        for s in win["speaks"]:
            s["text"] = script[s["seq"]][1]

    out = {
        "fixture_sha256": got, "verified": True, "n_windows": len(windows),
        "w": W, "dial_bounds": DIAL_BOUNDS,
        "distinct_scripts": {"ABC": ["A", "B", "C"], "D": ["D", "D-cold"]},
        "corpus_sd_speak_level": sd_speak,
        "corpus_sd_window_level": sd_window,
        "windows": windows,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"corpus verified: fixture SHA {got[:12]}…, 27 windows, "
          f"all speak texts sha-verified ({sum(len(logs[k]) for k in logs)} speaks)")
    print(f"corpus_sd speak-level = {sd_speak:.6f}  window-level = {sd_window:.6f}")


if __name__ == "__main__":
    main()
