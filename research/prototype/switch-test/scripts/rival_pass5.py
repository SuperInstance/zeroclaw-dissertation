#!/usr/bin/env python3
"""RIVAL PASS-5 — is the reader-delta downgrade COMPLETE? (2026-08-20)

Question (stated before any Pass-5 number was computed):
  The reader-delta object was downgraded (topic.md, claim inventory #4) to
  "a mean-shift baseline-relative delta — two scalars (slope, mean of
  ||r-b_hat||) ... beaten on localization by the rival's static median
  trick". Is that scoping COMPLETE — once the reader-delta is correctly
  scoped as a mean-shift/baseline-relative object, does the rival's
  static-median normalization still win switch localization with NO
  residual second-order (temporal, self-referential) signal surviving
  anywhere in scope — or does a residual survive that needs re-scoping?

Cells (SAME fixtures, SAME localizer, SAME seed schedule as the Switch
Test, results.json 2026-08-19; per-nurse numbers must reproduce exactly):
  drift-reader     ci=0  registered burn-in baseline — TEMPORAL baseline,
                       the last remnant of the second-order claim
  fo-median-static ci=2  rival sec-2.4 global static per-nurse median
  drift-online     ci=4  post-hoc causal expanding median — TEMPORAL
  rd-perregime     ci=7  NEW — the ONE fair upgrade within the downgraded
                       scope: the downgrade's own scalar (mean ||r-b_hat||)
                       computed PER-REGIME. For each candidate split u over
                       windows [B,T): segment-local median baselines
                       b_L(u), b_R(u); total normalized excursion
                       TE(u) = sum_L ||r-b_L||/||b_L|| + sum_R ||r-b_R||/||b_R||;
                       predicted split = argmin_u TE(u); stat = TE_1 - min TE(u)
                       (single global-baseline total minus best two-regime
                       total). Readings smoothed by the same 3-window median
                       filter first (reading-level analog of smooth3).
                       Detection: stat >= 2x median of 1000 seeded
                       time-permutations of the raw readings through the
                       SAME pipeline. No temporal structure, no oracle:
                       pure baseline-relative mean-shift with segment-local
                       baselines (rival sec-5.3 rule 1 applied to the
                       downgraded object itself).

PRE-STATED VERDICT RULE:
  1. Reproduction gate: per-nurse s_hat + detection flags (and cell-level
     r / median_err / detection_rate / control_alarms) for drift-reader,
     fo-median-static, drift-online must EQUAL results.json (identical
     seed schedule). Else the pass ABORTS with no verdict.
  2. A reader-delta-scoped cell DOMINATES the rival iff
     (r > rival_r + max(r_floor of the two cells)) AND
     (detection_rate > rival detection_rate) AND (median_err <= rival's).
  3. VERDICT = DOWNGRADE COMPLETE iff the gate passes AND no in-scope
     cell dominates fo-median-static on the FULL registered set (15
     switching nurses). If any in-scope cell dominates: INCOMPLETE
     (a residual survives; re-scope needed).
  4. The excl-osc>osc slice (mean-moving regimes only) is reported as
     context; the rule is evaluated on the full registered set.

Determinism: seeded RNGs only; canonical JSON; 3/3 replay verification.
numpy + stdlib only. CPU. Fixtures SHA256-pinned, NOT rebuilt.
"""
import json, os, sys, hashlib, subprocess
import numpy as np

SEED = 20260819
B = 6
N_PERM = 1000

HERE = os.path.dirname(os.path.abspath(__file__))
SWDIR = os.path.dirname(HERE)
FIXDIR = os.path.join(SWDIR, "fixtures")
sys.path.insert(0, SWDIR)

from run_switch import (localize_signal, bootstrap_median_ci, pearson,  # noqa: E402
                        r_floor_and_p)
from build_switches import canonical  # noqa: E402

CELLS = [
    ("drift-reader", 0, "signal"),
    ("fo-median-static", 2, "signal"),
    ("drift-online", 4, "signal"),
    ("rd-perregime", 7, "perregime"),
]


# ---------------------------------------------------------- signals
def signal(cell, r):
    """Identical to run_switch.signal for the three reproduced cells."""
    T = r.shape[0]
    if cell == "drift-reader":
        b = np.median(r[:B], axis=0)
        s_ = np.linalg.norm(r - b, axis=1) / (np.linalg.norm(b) + 1e-9)
    elif cell == "drift-online":
        s_ = np.zeros(T)
        for tt in range(B, T):
            b = np.median(r[:tt], axis=0)
            s_[tt] = np.linalg.norm(r[tt] - b) / (np.linalg.norm(b) + 1e-9)
    elif cell == "fo-median-static":
        b = np.median(r, axis=0)
        s_ = np.linalg.norm(r - b, axis=1) / (np.linalg.norm(b) + 1e-9)
    else:
        raise ValueError(cell)
    return s_[B:]


# ---------------------------------------------------------- the upgrade
def smooth_dims(x):
    """3-window median filter per reading-dimension (reading-level smooth3)."""
    xp = np.pad(np.asarray(x, float), ((1, 1), (0, 0)), mode="edge")
    return np.median(np.stack([xp[:-2], xp[1:-1], xp[2:]]), axis=0)


def perregime_fit(x):
    """Per-regime baseline mean-excursion fit. Returns (split, TE_1 - min TE).

    For each candidate split u (both blocks >= 3, same range as two_const):
    segment-local componentwise-median baselines; total normalized
    excursion TE(u). Split = argmin TE (ties -> first). Stat = single-
    baseline total minus best two-regime total (delta, analogous to
    delta-SSE in the registered localizer).
    """
    xs = smooth_dims(x)
    n = xs.shape[0]
    us = np.arange(3, n - 2)
    ball = np.median(xs, axis=0)
    te1 = float(np.sum(np.linalg.norm(xs - ball, axis=1) /
                       (np.linalg.norm(ball) + 1e-9)))
    te2 = np.empty(len(us))
    for k, u in enumerate(us):
        L, Rr = xs[:u], xs[u:]
        bL, bR = np.median(L, axis=0), np.median(Rr, axis=0)
        te2[k] = float(np.sum(np.linalg.norm(L - bL, axis=1) /
                              (np.linalg.norm(bL) + 1e-9)) +
                       np.sum(np.linalg.norm(Rr - bR, axis=1) /
                              (np.linalg.norm(bR) + 1e-9)))
    k = int(np.argmin(te2))
    return int(us[k]), float(te1 - te2[k])


def localize_perregime(x, seed):
    """Same detection logic as localize_signal: stat >= 2x median null,
    null = 1000 seeded time-permutations of the RAW readings through the
    same pipeline (permute -> smooth -> per-regime fit)."""
    split, stat = perregime_fit(x)
    rng = np.random.default_rng(seed)
    null = np.empty(N_PERM)
    for i in range(N_PERM):
        _, null[i] = perregime_fit(rng.permutation(x))
    return split, stat, bool(stat >= 2.0 * np.median(null)), float(np.median(null))


# ---------------------------------------------------------- the run
def load():
    man = json.load(open(os.path.join(FIXDIR, "manifest.json")))
    h = hashlib.sha256(open(os.path.join(FIXDIR, "manifest.json"), "rb").read()).hexdigest()
    pinned = open(os.path.join(FIXDIR, "FIXTURES-SHA256")).read().strip()
    assert h == pinned, "fixture manifest hash drift"
    nurses = man["nurses"]
    ids = [n["id"] for n in nurses]
    R = np.array([n["readings"] for n in nurses], float)
    sw = np.array([n["switch"] if n["switch"] is not None else -1
                   for n in nurses], int)
    fam = [None if n["control"] else n["family"] for n in nurses]
    return man, ids, R, sw, fam


def run():
    man, ids, R, sw, fam = load()
    N, T = R.shape[0], R.shape[1]
    is_sw = sw > 0
    idx_sw = np.where(is_sw)[0]
    prev = json.load(open(os.path.join(SWDIR, "results.json")))

    # optional live-corpus check (fixtures are pinned either way)
    corpus_check = "skipped"
    try:
        from build_switches import load_corpus
        live = load_corpus()
        ok = all(a["m"] == b["m"] and a["night"] == b["night"]
                 for a, b in zip(man["corpus_windows"], live)) and len(live) == T
        corpus_check = "match" if ok else "MISMATCH"
    except Exception:
        corpus_check = "skipped"

    out = {"meta": dict(pass_name="RIVAL-PASS-5", date="2026-08-20",
                        seed=SEED, burnin=B, T=T, N=N,
                        n_switching=int(is_sw.sum()),
                        corpus_live=corpus_check,
                        cells={c: ci for c, ci, _ in CELLS})}

    cells_out, repro = {}, {}
    for cell, ci, kind in CELLS:
        per, errs, shats, det_sw, det_ct = [], [], [], [], []
        for i in range(N):
            seed_l = SEED + 10_000 + 97 * ci + i   # identical schedule
            if kind == "signal":
                y = signal(cell, R[i])
                split, stat, det, floor = localize_signal(y, seed_l)
            else:
                split, stat, det, floor = localize_perregime(R[i][B:], seed_l)
            s_hat = B + split
            shats.append(s_hat)
            if is_sw[i]:
                errs.append(abs(s_hat - sw[i]))
                det_sw.append(det)
            else:
                det_ct.append(det)
            per.append(dict(id=ids[i], s_hat=int(s_hat),
                            s=int(sw[i]) if is_sw[i] else None,
                            stat=round(float(stat), 4),
                            floor=round(float(floor), 4), detected=det))
        shats = np.array(shats)
        errs = np.array(errs, float)
        fl, f95, p = r_floor_and_p(shats[idx_sw], sw[idx_sw],
                                   SEED + 1_500_000 + 31 * ci)
        cells_out[cell] = dict(
            median_err=round(float(np.median(errs)), 3),
            err_ci=bootstrap_median_ci(errs, SEED + 500_000 + 31 * ci),
            r=round(pearson(shats[idx_sw], sw[idx_sw]), 4),
            r_floor=round(fl, 4), r_floor_p95=round(f95, 4),
            r_perm_p=round(p, 4),
            detection_rate=round(float(np.mean(det_sw)), 3),
            control_alarms=round(float(np.mean(det_ct)), 3),
            per_nurse=per,
            temporal_baseline=cell in ("drift-reader", "drift-online"),
            new_in_pass5=cell == "rd-perregime")
        old = prev["taskA"]["cells"].get(cell)
        if old is not None:
            ok = (old["r"] == cells_out[cell]["r"]
                  and old["median_err"] == cells_out[cell]["median_err"]
                  and old["detection_rate"] == cells_out[cell]["detection_rate"]
                  and old["control_alarms"] == cells_out[cell]["control_alarms"]
                  and all(o["s_hat"] == n2["s_hat"] and o["detected"] == n2["detected"]
                          for o, n2 in zip(old["per_nurse"], per)))
            repro[cell] = bool(ok)

    out["taskA"] = {"cells": cells_out}
    out["reproduction_gate"] = repro

    # sensitivity slice: switching nurses excluding the osc>osc family
    keep = [j for j, i in enumerate(idx_sw) if fam[i] != "osc>osc"]
    sens = {}
    for cell in cells_out:
        sh = np.array([q["s_hat"] for q in cells_out[cell]["per_nurse"]])[idx_sw]
        det = np.array([q["detected"] for q in cells_out[cell]["per_nurse"]])[idx_sw]
        sh_k, s_k, det_k = sh[keep], sw[idx_sw][keep], det[keep]
        sens[cell] = dict(
            n=int(len(keep)), r=round(pearson(sh_k, s_k), 4),
            median_err=round(float(np.median(np.abs(sh_k - s_k))), 3),
            detection_rate=round(float(np.mean(det_k)), 3))
    out["sensitivity_excl_osc"] = sens

    # paired errors vs the rival (15 switching nurses)
    def errs_of(cell):
        return np.array([abs(q["s_hat"] - q["s"])
                         for q in cells_out[cell]["per_nurse"] if q["s"] is not None])
    riv = errs_of("fo-median-static")
    paired = {}
    for cell in ("drift-reader", "drift-online", "rd-perregime"):
        e = errs_of(cell)
        paired[cell] = dict(better=int(np.sum(e < riv)),
                            tie=int(np.sum(e == riv)),
                            worse=int(np.sum(e > riv)))
    out["paired_vs_rival_n15"] = paired

    # verdict per the pre-stated rule
    gate_ok = all(repro.get(c, False)
                  for c in ("drift-reader", "fo-median-static", "drift-online"))
    rival = cells_out["fo-median-static"]
    dominates = []
    for cell, c in cells_out.items():
        if cell == "fo-median-static":
            continue
        margin = max(c["r_floor"], rival["r_floor"])
        if (c["r"] > rival["r"] + margin
                and c["detection_rate"] > rival["detection_rate"]
                and c["median_err"] <= rival["median_err"]):
            dominates.append(cell)
    if not gate_ok:
        verdict = "ABORT: reproduction gate FAILED — no verdict"
    elif dominates:
        verdict = "INCOMPLETE: residual survives (re-scope needed)"
    else:
        verdict = ("DOWNGRADE COMPLETE: rival's static median holds; "
                   "no second-order signal survives in scope")
    out["verdict"] = dict(gate_ok=gate_ok, dominating_cells=dominates,
                          verdict=verdict,
                          rule=("dominance = r > rival_r + max(perm floors) AND "
                                "detection strictly higher AND median_err <= rival's; "
                                "evaluated on the 15 registered switching nurses"))
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "run":
        res = run()
        with open(os.path.join(SWDIR, "rival-pass5-results.json"), "w") as f:
            f.write(canonical(res))
        print("\n================ RIVAL PASS-5 (2026-08-20) ================")
        print(f"reproduction gate: {res['reproduction_gate']}")
        print(f"corpus live check: {res['meta']['corpus_live']}\n")
        hdr = f"{'cell':<18}{'med_err':>8}{'r':>9}{'det':>7}{'ctrl':>6}   sens_r(excl-osc)"
        print(hdr)
        for cell, c in res["taskA"]["cells"].items():
            s = res["sensitivity_excl_osc"][cell]
            tag = "  <-- NEW upgrade" if c["new_in_pass5"] else \
                  ("  (temporal baseline)" if c["temporal_baseline"] else "  (rival)")
            print(f"{cell:<18}{c['median_err']:>8}{c['r']:>9}"
                  f"{c['detection_rate']:>7}{c['control_alarms']:>6}"
                  f"   r={s['r']}, det={s['detection_rate']}{tag}")
        print(f"\npaired vs rival (n=15): {res['paired_vs_rival_n15']}")
        print(f"\nFINAL VERDICT: {res['verdict']['verdict']}")
        print("===========================================================")
    elif mode == "hash":
        print(hashlib.sha256(canonical(run()).encode()).hexdigest())
    elif mode == "--verify-replay":
        hs = []
        for i in range(3):
            h = subprocess.run([sys.executable, os.path.abspath(__file__), "hash"],
                               capture_output=True, text=True, check=True)
            hs.append(h.stdout.strip())
            print(f"replay {i+1}/3: {hs[-1]}")
        print("REPLAYS_IDENTICAL_3_OF_3:", len(set(hs)) == 1)


if __name__ == "__main__":
    main()
