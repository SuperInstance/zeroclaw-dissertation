#!/usr/bin/env python3
"""E3 analysis — the cross-model baseline-spread ratio (registered estimator).

Implements exactly the estimator in REGISTRATION-2026-08-19.md §5–§6:
segment-local baselines, distinct-stimulus equal weighting, corpus_sd at
speak level (E2-comparable), bootstrap-over-readers 95% CI (10k, seed
20260819), registered verdict vs the 0.3/0.6 kill band, paraphrase
crossover, and the D2/D3 deadmen.

Run:  python3 analyze.py      (after elicit.py; writes results.json)
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prompts import DIALS, SWEEP_WINDOWS  # noqa: E402

CORPUS = json.load(open(os.path.join(HERE, "corpus", "corpus.json")))
WINDOWS = CORPUS["windows"]
SD = float(CORPUS["corpus_sd_speak_level"])
SD_WIN = float(CORPUS["corpus_sd_window_level"])
BOUNDS = CORPUS["dial_bounds"]
WIDTH = np.array([BOUNDS[d][1] - BOUNDS[d][0] for d in DIALS])
LO = np.array([BOUNDS[d][0] for d in DIALS])
HI = np.array([BOUNDS[d][1] for d in DIALS])
BI_DIAL = {d: i for i, d in enumerate(DIALS)}

SEED = 20260819
NBOOT = 10_000
KILL_LO, KILL_HI = 0.3, 0.6
VALIDITY_FLOOR = 0.80
SWEEP_FLOOR = 0.02

RDIR = os.path.join(HERE, "readings", "raw")
SDIR = os.path.join(HERE, "sweep", "raw")


def native_vecs(parsed):
    """room_reading (0-100) and private_displacement (pts) -> native 7-vecs."""
    rr = np.array([parsed["room_reading"][d] for d in DIALS], float)
    if "mood" in DIALS:  # width-2 dials: v/50 - 1; width-1 dials: v/100
        rr = np.array([rr[i] / 50 - 1 if WIDTH[i] == 2 else rr[i] / 100
                       for i in range(7)])
    pd = np.array([parsed["private_displacement"][d] for d in DIALS], float)
    pd = pd * WIDTH / 100.0
    emitted = np.clip(rr + pd, LO, HI)
    return rr, pd, emitted


def load_reader(rid):
    """Returns dict: window_id -> {"rr": (2,7), "pd": (2,7), "r": (2,7), "ok_passes": int}."""
    out, valid_count, total = {}, 0, 54
    for w in WINDOWS:
        wid = w["id"]
        recs = []
        for p in ("1", "2"):
            path = os.path.join(RDIR, rid, f"{wid}.pass{p}.json")
            if os.path.exists(path):
                rec = json.load(open(path))
                if rec.get("ok") and rec.get("parsed"):
                    recs.append(native_vecs(rec["parsed"]))
        if recs:
            out[wid] = {
                "rr": np.stack([x[0] for x in recs]),
                "pd": np.stack([x[1] for x in recs]),
                "r": np.stack([x[2] for x in recs]),
                "ok_passes": len(recs),
            }
            valid_count += len(recs)
    validity = valid_count / total
    return out, validity


def seg_ids(seg, group=None):
    return [w["id"] for w in WINDOWS
            if w["seg"] == seg and (group is None or w["distinct_group"] == group)]


# distinct stimulus structure: A-type (group ABC) and D-type (group D)
GROUPS = ["ABC", "D"]


def pass_averaged(readings, key="r"):
    """window_id -> mean over passes of the given component."""
    return {wid: v[key].mean(axis=0) for wid, v in readings.items()}


def stats_for(readers_data):
    """Registered estimator on {rid: readings}. Returns dict or None."""
    # segment-local baselines, equal weight per distinct stimulus
    baselines = {}
    for rid, rd in readers_data.items():
        pa = pass_averaged(rd)
        for seg in ("SEG1", "SEG2"):
            ids = [wid for wid in seg_ids(seg) if wid in pa]
            # distinct-stimulus equal weight: mean over windows already
            # equal-weights the 27 presentations by multiplicity; correct to
            # equal stimulus weight by averaging within group first.
            gmeans = []
            for g in GROUPS:
                gids = [wid for wid in seg_ids(seg, g) if wid in pa]
                if gids:
                    gmeans.append(np.mean([pa[wid] for wid in gids], axis=0))
            baselines[(rid, seg)] = np.mean(gmeans, axis=0) if gmeans else \
                np.mean([pa[wid] for wid in ids], axis=0)

    # between-model baseline spread (segment-local, averaged over segments)
    spreads = {}
    for seg in ("SEG1", "SEG2"):
        B = np.stack([baselines[(rid, seg)] for rid in readers_data])
        spreads[seg] = float(np.sqrt(np.mean(B.var(axis=0, ddof=1))))
    baseline_spread = 0.5 * (spreads["SEG1"] + spreads["SEG2"])
    baseline_spread_z = baseline_spread / SD

    # within-model drift: per distinct night-script SEG1->SEG2 displacement
    drifts = {}
    for rid, rd in readers_data.items():
        pa = pass_averaged(rd)
        ds = []
        for g in GROUPS:
            s1 = [pa[wid] for wid in seg_ids("SEG1", g) if wid in pa]
            s2 = [pa[wid] for wid in seg_ids("SEG2", g) if wid in pa]
            if s1 and s2:
                ds.append(np.linalg.norm(np.mean(s2, axis=0) -
                                         np.mean(s1, axis=0)) / SD)
        drifts[rid] = float(np.mean(ds)) if ds else float("nan")
    mean_drift_z = float(np.nanmean(list(drifts.values())))
    if mean_drift_z <= 1e-9:
        return None
    return {
        "spreads": {k: v / SD for k, v in spreads.items()},
        "baseline_spread_z": baseline_spread_z,
        "drifts_z": drifts,
        "mean_drift_z": mean_drift_z,
        "ratio": baseline_spread_z / mean_drift_z,
    }


def bootstrap_ratio(readers_data):
    rids = sorted(readers_data)
    rng = np.random.default_rng(SEED)
    ratios, spreads, drifts = [], [], []
    for _ in range(NBOOT):
        sample = [rids[i] for i in rng.integers(0, len(rids), len(rids))]
        sub = {rid: readers_data[rid] for rid in sample}
        st = stats_for(sub)
        if st:
            ratios.append(st["ratio"])
            spreads.append(st["baseline_spread_z"])
            drifts.append(st["mean_drift_z"])
    out = {}
    for name, arr in (("ratio", ratios), ("spread", spreads),
                      ("drift", drifts)):
        a = np.sort(np.array(arr))
        out[name] = {"mean": float(a.mean()),
                     "lo95": float(a[int(0.025 * len(a))]),
                     "hi95": float(a[int(0.975 * len(a))])}
    return out


def retest_noise(readings):
    """mean over windows of ||pass1 - pass2|| / SD (emitted reading)."""
    ds = []
    for wid, v in readings.items():
        if v["r"].shape[0] == 2:
            ds.append(np.linalg.norm(v["r"][0] - v["r"][1]) / SD)
    return float(np.mean(ds)) if ds else float("nan")


def sweep_analysis(rid, retest_z):
    """Paraphrase crossover per the registered rule."""
    p0 = {}
    for wid in SWEEP_WINDOWS:
        for p in ("1", "2"):
            path = os.path.join(RDIR, rid, f"{wid}.pass{p}.json")
            if os.path.exists(path):
                rec = json.load(open(path))
                if rec.get("ok"):
                    p0[wid] = p0.get(wid, []) + [native_vecs(rec["parsed"])[2]]
    res = {}
    for lvl in ("P1", "P2", "P3"):
        shifts = []
        for wid in SWEEP_WINDOWS:
            path = os.path.join(SDIR, rid, f"{wid}.{lvl}.json")
            if not os.path.exists(path):
                continue
            rec = json.load(open(path))
            if rec.get("ok") and wid in p0:
                pk = native_vecs(rec["parsed"])[2]
                base = np.mean(p0[wid], axis=0)
                shifts.append(np.linalg.norm(pk - base) / SD)
        if not shifts:
            res[lvl] = None
            continue
        shift_z = float(np.mean(shifts))
        thresh = 2 * max(retest_z if retest_z == retest_z else 0.0, SWEEP_FLOOR)
        res[lvl] = {"shift_z": shift_z, "threshold": thresh,
                    "destabilized": bool(shift_z > thresh)}
    crossover = next((lvl for lvl in ("P1", "P2", "P3")
                      if res.get(lvl) and res[lvl]["destabilized"]), None)
    return {"levels": res, "crossover": crossover}


def main():
    reader_dirs = sorted(os.listdir(RDIR)) if os.path.isdir(RDIR) else []
    readers, dropped = {}, []
    per_reader = {}
    for rid in reader_dirs:
        rd, validity = load_reader(rid)
        per_reader[rid] = {"validity": validity,
                           "retest_z": retest_noise(rd),
                           "n_windows_ok": len(rd)}
        if validity < VALIDITY_FLOOR:
            dropped.append((rid, validity))
            continue
        readers[rid] = rd
    if len(readers) < 10:
        print(f"WARNING: only {len(readers)} readers pass D2 "
              f"(<10 required)")

    primary = stats_for(readers)
    boot = bootstrap_ratio(readers)

    # secondary decompositions (registered: where does spread live)
    sec = {}
    for key, label in (("rr", "room_reading_only"), ("pd", "displacement_only")):
        st = _stats_with_key(readers, key)
        sec[label] = st["ratio"] if st else None

    # per-pass robustness
    per_pass = {}
    for p_idx in (0, 1):
        sub = {}
        for rid, rd in readers.items():
            sub[rid] = {wid: {**v, "r": v["r"][p_idx:p_idx + 1],
                              "rr": v["rr"][p_idx:p_idx + 1],
                              "pd": v["pd"][p_idx:p_idx + 1]}
                        for wid, v in rd.items() if v["r"].shape[0] > p_idx}
        st = _stats_with_key(sub, "r")
        per_pass[f"pass{p_idx+1}"] = st["ratio"] if st else None

    sweeps = {rid: sweep_analysis(rid, per_reader[rid]["retest_z"])
              for rid in readers}

    ci = boot["ratio"]
    if ci["lo95"] > KILL_HI:
        verdict = ("CLEAR — CI entirely above 0.6: the premise holds "
                   "(field, elicited); strong evidence per the registered "
                   "asymmetry")
    elif ci["hi95"] < KILL_LO:
        verdict = ("BELOW BAND — CI entirely under 0.3: weak evidence "
                   "(miss); frame artifact cannot be excluded per the "
                   "registered asymmetry")
    else:
        verdict = "INDETERMINATE — CI touches the 0.3–0.6 band"

    d3 = sum(1 for rid in readers
             if per_reader[rid]["retest_z"] == per_reader[rid]["retest_z"]
             and per_reader[rid]["retest_z"] > primary["mean_drift_z"])
    d3_flag = d3 > len(readers) / 2

    out = {
        "date": "2026-08-19", "n_readers": len(readers),
        "readers": sorted(readers), "dropped_d2": dropped,
        "corpus_sd_speak_level": SD, "corpus_sd_window_level": SD_WIN,
        "primary": primary, "bootstrap": boot,
        "secondary": sec, "per_pass_ratios": per_pass,
        "per_reader": per_reader, "sweep": sweeps,
        "d3_majority_retest_exceeds_drift": d3_flag,
        "d3_readers_over": d3,
        "verdict": verdict,
    }
    path = os.path.join(HERE, "results.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(json.dumps({k: out[k] for k in
                      ("n_readers", "primary", "bootstrap", "verdict",
                       "d3_majority_retest_exceeds_drift")}, indent=1,
                     default=float))
    print("per-reader drift_z:", json.dumps(primary["drifts_z"], indent=1))
    print("crossovers:", {r: s["crossover"] for r, s in sweeps.items()})


def _stats_with_key(readers_data, key):
    """stats_for with a specific pass-averaged component key."""
    global pass_averaged
    orig = pass_averaged
    pass_averaged = lambda rd, k=None, _key=key: {  # noqa: E731
        wid: v[_key].mean(axis=0) for wid, v in rd.items()}
    try:
        return stats_for(readers_data)
    finally:
        pass_averaged = orig


if __name__ == "__main__":
    main()
