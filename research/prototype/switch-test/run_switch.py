#!/usr/bin/env python3
"""SWITCH TEST RUNNER — Rival A's counter-proposal, run (2026-08-19).

Registered: research/skills/rival-reader-delta-review.md §5.1 (falsifier #1),
§2.4 (falsifier #2: the median-trick cell), discipline §5.3 (segment-local
baselines, class-conditional baselines, CIs for n<100, noise sweeps as
crossover points, full ablation grid). Pre-registered thresholds live in
build_switches.py's docstring, written BEFORE the first run.

TASK A (switch detection + localization). One localizer for every continuous
representation (AMENDMENT 1, disclosed above): 3-window running-median
smoothing, then two-segment CONSTANT (mean-shift) fit of the per-window
signal over [B=6, T); predicted switch = best split; detection = delta-SSE
>= 2x median of 1000 seeded permutations of the raw signal (permuted, then
smoothed and fitted through the same pipeline). Label cells (static
templates) use the analogous optimal two-block label split with its own
permutation null. Any difference between cells is REPRESENTATIONAL, not
estimatorial.

  drift-reader  (second-order): burn-in baseline b-hat = median of her own
               first B readings; signal e(t) = ||r(t)-b-hat|| / ||b-hat||.
               Temporal, self-referential: models the nurse.
  fo-norm       (primary first-order): ||r(t)|| — magnitudes, no baseline.
  fo-template-* (primary first-order): LOO static per-class templates from
               other nurses' PLANTED-labeled windows (supervised fingerprint);
               per-window nearest template -> label sequence -> block split.
  fo-median-static (BOUNDARY, rival §2.4): global per-nurse median over all
               windows (static normalization, no time structure).
  fo-crowd      (BOUNDARY): per-window deviation from the LOO cross-nurse
               consensus reading (static consensus, no per-nurse model).

TASK B (regime classification, 4-way {sauna,jaded,over,osc}, chance 0.25).
  drift-reader: its OWN localized segments + segment-local baselines (§5.3
               rule 1), features (mean, slope, std) of excursion, LOO
               nearest-class-centroid; held-out nurse reported explicitly.
  first-order: ORACLE-CLEAN FIXED windows [0,8) and [21,T) — guaranteed
               pre/post for every nurse by planting; a gift the drift-reader
               does not need. Cells: raw-1nn, norm-traj-centroid, static
               template, and the boundary median-seg (segment-local median).

KILL CONDITION: a PRIMARY first-order cell (fo-norm, fo-template-euclid,
fo-template-cosine) at parity with drift-reader on Task A (median err
<= 1.25x drift's, r within floor noise, detection within 10 points) AND
Task B (accuracy CIs overlapping, pre and post) => reindex. Boundary cells
at parity => "not an identity, one normalization" (language verdict only).

Determinism: fixed seed schedule, canonical JSON, 3/3 replay verification.
numpy + stdlib only. Elephant data read-only.
"""
import json, os, sys, hashlib, subprocess, math
import numpy as np

SEED = 20260819
B = 6                       # burn-in (pre-registered)
N_PERM = 1000
N_BOOT = 10000
HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures")
sys.path.insert(0, HERE)
from build_switches import load_corpus, canonical  # noqa: E402

REGIMES = ["sauna", "jaded", "over", "osc"]
CONT_CELLS = ["drift-reader", "fo-norm", "fo-median-static", "fo-crowd"]
PRIMARY = ["fo-norm", "fo-template-euclid", "fo-template-cosine"]
BOUNDARY = ["fo-median-static", "fo-median-seg", "fo-crowd"]


# ------------------------------------------------------------- localizer
# AMENDMENT 1 (2026-08-19, disclosed): the registered localizer was a two-
# segment PIECEWISE-LINEAR fit; the first run showed it ill-identified under
# within-regime room wiggle (SSE nearly flat across splits, detection dead at
# 13%, drift r=0.098). Amended estimator — applied IDENTICALLY to every
# continuous cell, so all differences remain representational:
#   signal -> 3-window running-median smoothing (the doctor reads her over
#   the last few patients) -> two-segment CONSTANT (mean-shift) fit.
# Null: same pipeline (permute RAW, then smooth, then fit) x1000 seeded.
# Pre-amendment numbers are quoted in the results report; git history of the
# first run is preserved in the report's amendment section.
def smooth3(y):
    pad = 1
    yp = np.pad(np.asarray(y, float), pad, mode="edge")
    return np.array([np.median(yp[i:i + 3]) for i in range(len(y))])


def two_const(y):
    """Best two-block constant fit. Returns (split idx, delta-SSE).
    Deterministic (ties -> first)."""
    n = len(y)
    us = np.arange(3, n - 2)                      # both blocks >= 3 points
    cs = np.concatenate(([0.], np.cumsum(y)))
    cs2 = np.concatenate(([0.], np.cumsum(y * y)))
    m = us.astype(float)
    tot = (cs2[us] - cs[us] ** 2 / m) + \
          ((cs2[n] - cs2[us]) - (cs[n] - cs[us]) ** 2 / (n - m))
    k = int(np.argmin(tot))
    full = cs2[n] - cs[n] ** 2 / n
    return int(us[k]), float(full - tot[k])


def localize_signal(y, seed):
    """Split (global offset applied by caller), delta-SSE, detection flag."""
    ysm = smooth3(y)
    split, dsse = two_const(ysm)
    rng = np.random.default_rng(seed)
    null = np.empty(N_PERM)
    for i in range(N_PERM):
        _, null[i] = two_const(smooth3(rng.permutation(y)))
    detected = bool(dsse >= 2.0 * np.median(null))
    return split, float(dsse), detected, float(np.median(null))


def block_minority(lab):
    return len(lab) - np.max([int(np.sum(lab == g)) for g in np.unique(lab)])


def localize_labels(lab, seed):
    """Optimal two-block split of a label sequence; err-reduction + null."""
    n = len(lab)
    us = np.arange(3, n - 2)
    errs = np.array([block_minority(lab[:u]) + block_minority(lab[u:]) for u in us])
    k = int(np.argmin(errs))
    split = int(us[k])
    derr = int(block_minority(lab) - errs[k])
    rng = np.random.default_rng(seed)
    null = np.empty(N_PERM)
    for i in range(N_PERM):
        lp = rng.permutation(lab)
        e = np.array([block_minority(lp[:u]) + block_minority(lp[u:])
                      for u in us])
        null[i] = block_minority(lp) - e.min()
    detected = bool(derr >= max(2, 2.0 * np.median(null)))
    return split, derr, detected, float(np.median(null))


# ------------------------------------------------------------- statistics
def bootstrap_median_ci(x, seed):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    idx = rng.integers(0, len(x), size=(N_BOOT, len(x)))
    meds = np.median(x[idx], axis=1)
    return [float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))]


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() < 1e-12 or b.std() < 1e-12:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def r_floor_and_p(shat, s, seed):
    """Permutation floor for r(shat, s): 1000 seeded perms of s."""
    rng = np.random.default_rng(seed)
    s = np.asarray(s); shat = np.asarray(shat, float)
    rp = np.array([pearson(shat, rng.permutation(s)) for _ in range(N_PERM)])
    return float(np.median(np.abs(rp))), float(np.percentile(np.abs(rp), 95)), \
        float(np.mean(np.abs(rp) >= abs(pearson(shat, s))))


def binom_cdf(k, n, p):
    return float(sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i)
                     for i in range(0, k + 1)))


def cp_ci(k, n, alpha=0.05):
    """Exact Clopper-Pearson 95% CI (binary search on the binomial).
    Both root functions negated to INCREASING form for the bisection.
    lower: CDF(k-1, p) = 1 - a/2   (k>0)    upper: CDF(k, p) = a/2   (k<n)"""
    def solve_incr(f, lo, hi):
        for _ in range(80):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve_incr(
        lambda p: (1 - alpha / 2) - binom_cdf(k - 1, n, p), 0.0, 1.0)
    upper = 1.0 if k == n else solve_incr(
        lambda p: alpha / 2 - binom_cdf(k, n, p), 0.0, 1.0)
    return [round(lower, 4), round(upper, 4)]


def ols_slope(y, x):
    x, y = np.asarray(x, float), np.asarray(y, float)
    xm, ym = x.mean(), y.mean()
    return float(((x - xm) * (y - ym)).sum() / (((x - xm) ** 2).sum() + 1e-12))


# ------------------------------------------------------------- the run
def run():
    man = json.load(open(os.path.join(FIXDIR, "manifest.json")))
    T = man["T"]
    live = load_corpus()
    assert T == len(live) and all(a["m"] == b["m"] and a["night"] == b["night"]
                                  for a, b in zip(man["corpus_windows"], live)), \
        "fixture corpus drifted from elephant nights"

    nurses = man["nurses"]
    N = len(nurses)
    ids = [n["id"] for n in nurses]
    R = np.array([n["readings"] for n in nurses], float)     # (N,T,7)
    sw = np.array([n["switch"] if n["switch"] is not None else -1
                   for n in nurses], int)
    is_sw = sw > 0
    pre_cls = np.array([n["pre"] for n in nurses])
    post_cls = np.array([n["post"] for n in nurses])
    heldout = np.array([n["heldout"] for n in nurses])
    idx_sw = np.where(is_sw)[0]
    ho_i = int(np.where(heldout & is_sw)[0][0])
    t = np.arange(T, dtype=float)

    out = {"meta": dict(
        N=N, T=T, seed=SEED, burnin=B, n_switching=int(is_sw.sum()),
        n_controls=int((~is_sw).sum()), heldout=dict(id=ids[ho_i],
        family=nurses[ho_i]["family"], s=int(sw[ho_i])),
        family_counts={f: int(sum(1 for n in nurses if n["family"] == f))
                       for f in man["families"]},
        class_counts_pre={r: int((pre_cls == r).sum()) for r in REGIMES},
        class_counts_post={r: int((post_cls == r).sum()) for r in REGIMES},
        planted_switches=[int(x) for x in sw[idx_sw]],
        thresholds=dict(taskA_r_ge="2x perm-floor median", taskA_mederr_le=3,
                        taskA_detect_ge=0.80, taskB_acc_ge=0.50,
                        chance=0.25))}

    # ---- continuous signals per cell ---------------------------------------
    # "drift-online" is a POST-HOC labeled variant (added after the registered
    # burn-in drift-reader missed its detection threshold): causal EXPANDING
    # per-nurse median baseline b(t)=median(r[0..t-1]) — arguably the more
    # faithful "doctor knows her day-in-day-out" reader. Disclosed, not
    # substituted for the registered cell.
    def signal(cell, i, Rmat=None):
        Rm = R if Rmat is None else Rmat
        r = Rm[i]
        if cell == "drift-reader":
            b = np.median(r[:B], axis=0)
            s_ = np.linalg.norm(r - b, axis=1) / (np.linalg.norm(b) + 1e-9)
        elif cell == "drift-online":
            s_ = np.empty(T)
            for tt in range(B, T):
                b = np.median(r[:tt], axis=0)
                s_[tt] = np.linalg.norm(r[tt] - b) / (np.linalg.norm(b) + 1e-9)
        elif cell == "fo-norm":
            s_ = np.linalg.norm(r, axis=1)
        elif cell == "fo-median-static":
            b = np.median(r, axis=0)
            s_ = np.linalg.norm(r - b, axis=1) / (np.linalg.norm(b) + 1e-9)
        elif cell == "fo-crowd":
            others = np.delete(Rm, i, axis=0)
            mu_t = others.mean(axis=0)                        # (T,7)
            s_ = np.linalg.norm(r - mu_t, axis=1) / \
                (np.linalg.norm(mu_t, axis=1) + 1e-9)
        else:
            raise ValueError(cell)
        return s_[B:]

    # ---- static-template labels (supervised fingerprint, LOO) --------------
    def template_labels(variant, j):
        lab_win = []
        for i in range(N):
            if i == j:
                continue
            for tt in range(T):
                regime = pre_cls[i] if (not is_sw[i] or tt < sw[i]) else post_cls[i]
                lab_win.append((R[i, tt], regime))
        templates = {}
        for g in REGIMES:
            V = np.array([r_ for r_, g_ in lab_win if g_ == g], float)
            templates[g] = V.mean(axis=0)
        labs = []
        for tt in range(T):
            r_ = R[j, tt]
            if variant == "euclid":
                g = min(REGIMES, key=lambda g: np.linalg.norm(r_ - templates[g]))
            else:
                g = max(REGIMES, key=lambda g: float(
                    np.dot(r_, templates[g]) /
                    (np.linalg.norm(r_) * np.linalg.norm(templates[g]) + 1e-12)))
            labs.append(g)
        return np.array(labs)[B:]

    # ================= TASK A =================================================
    taskA = {"cells": {}, "priors": {}}
    shat_store = {}
    POST_HOC_CELLS = {"drift-online"}
    for ci, cell in enumerate(CONT_CELLS + ["drift-online", "fo-template-euclid",
                                             "fo-template-cosine"]):
        det, errs, shats = [], [], []
        per = []
        for i in range(N):
            if cell.startswith("fo-template"):
                v = cell.split("-")[-1]
                labs = template_labels(v, i)
                split, dstat, detected, floor = localize_labels(
                    labs, SEED + 10_000 + 97 * ci + i)
            else:
                y = signal(cell, i)
                split, dstat, detected, floor = localize_signal(
                    y, SEED + 10_000 + 97 * ci + i)
            s_hat = B + split
            shats.append(s_hat)
            if is_sw[i]:
                errs.append(abs(s_hat - sw[i]))
            det.append(detected)
            per.append(dict(id=ids[i], s_hat=int(s_hat),
                            s=int(sw[i]) if is_sw[i] else None,
                            stat=round(float(dstat), 4),
                            floor=round(float(floor), 4), detected=detected))
        shat_store[cell] = np.array(shats)
        errs = np.array(errs, float)
        med = float(np.median(errs))
        ci_ = bootstrap_median_ci(errs, SEED + 500_000 + 31 * ci)
        fl, f95, p = r_floor_and_p(shat_store[cell][idx_sw], sw[idx_sw],
                                   SEED + 1_500_000 + 31 * ci)
        rr = pearson(shat_store[cell][idx_sw], sw[idx_sw])
        taskA["cells"][cell] = dict(
            median_err=round(med, 3), err_ci=ci_,
            r=round(rr, 4), r_floor=round(fl, 4), r_floor_p95=round(f95, 4),
            r_perm_p=round(p, 4),
            detection_rate=round(float(np.mean([d for d, i in
                                                zip(det, range(N)) if is_sw[i]])), 3),
            control_alarms=round(float(np.mean([d for d, i in
                                                zip(det, range(N)) if not is_sw[i]])), 3),
            per_nurse=per, boundary=cell in BOUNDARY,
            primary=cell in PRIMARY, post_hoc=cell in POST_HOC_CELLS)
    # prior baselines
    rngp = np.random.default_rng(SEED + 777)
    uni = rngp.integers(8, 21, size=int(is_sw.sum()))
    taskA["priors"] = dict(
        constant_mid14=dict(median_err=round(float(np.median(np.abs(
            np.full_like(sw[idx_sw], 14) - sw[idx_sw]))), 3), r=0.0),
        uniform_random=dict(median_err=round(float(np.median(np.abs(
            uni - sw[idx_sw]))), 3), r=round(pearson(uni, sw[idx_sw]), 4)))
    # post-hoc sensitivity (labeled): drift-reader excluding the exploratory
    # osc>osc family (mean-neutral phase flips are invisible to mean-shift
    # machinery by construction — see registration note in build_switches.py)
    osc_ids = [i for i in idx_sw if man["nurses"][i]["family"] == "osc>osc"]
    keep = [j for j, i in enumerate(idx_sw) if i not in osc_ids]
    sh_k = shat_store["drift-reader"][idx_sw][keep]
    s_k = sw[idx_sw][keep]
    taskA["sensitivity_posthoc"] = dict(
        note="drift-reader excluding osc>osc family (post-hoc, labeled)",
        r=round(pearson(sh_k, s_k), 4),
        median_err=round(float(np.median(np.abs(sh_k - s_k))), 3),
        n=len(keep))
    out["taskA"] = taskA

    # ================= TASK B =================================================
    pre_w = slice(0, man["oracle_pre_window"][1])
    post_w = slice(man["oracle_post_window"][0], T)

    def seg_feats(r, seg):
        b = np.median(r[seg], axis=0)
        e = np.linalg.norm(r[seg] - b, axis=1) / (np.linalg.norm(b) + 1e-9)
        x = np.arange(len(e), dtype=float)
        return np.array([e.mean(), ols_slope(e, x), e.std()])

    def norm_feats(r, seg):
        n_ = np.linalg.norm(r[seg], axis=1)
        x = np.arange(len(n_), dtype=float)
        return np.array([n_.mean(), ols_slope(n_, x), n_.std()])

    def loo_centroid(X, labels):
        ok = 0
        for j in range(len(labels)):
            tr = [i for i in range(len(labels)) if i != j]
            Xt = X[tr]
            mu, sd = Xt.mean(axis=0), Xt.std(axis=0) + 1e-12
            cents = {}
            for g in REGIMES:
                mem = [i for i in tr if labels[i] == g]
                if mem:
                    cents[g] = ((X[mem] - mu) / sd).mean(axis=0)
            zj = (X[j] - mu) / sd
            pred = min(sorted(cents), key=lambda g: np.linalg.norm(zj - cents[g]))
            ok += (pred == labels[j])
        return ok / len(labels)

    def loo_1nn(X, labels):
        ok = 0
        for j in range(len(labels)):
            tr = np.array([i for i in range(len(labels)) if i != j])
            d = np.linalg.norm(X[tr] - X[j], axis=1)
            ok += (labels[tr[int(d.argmin())]] == labels[j])
        return ok / len(labels)

    taskB = {"cells": {}}
    # drift-reader: own localized segments, segment-local baselines
    for tag, seg_of, cls_of in (("pre", "pre_seg", pre_cls), ("post", "post_seg", post_cls)):
        sh = shat_store["drift-reader"]
        X = np.array([seg_feats(R[i], slice(0, sh[i]) if tag == "pre"
                                else slice(sh[i], T)) for i in range(N)])
        sub = idx_sw
        acc = loo_centroid(X[sub], cls_of[sub])
        ho_ok = None
        j = int(np.where(sub == ho_i)[0][0])
        tr = [i for i in range(len(sub)) if i != j]
        mu, sd = X[sub][tr].mean(axis=0), X[sub][tr].std(axis=0) + 1e-12
        cents = {g: ((X[sub][[i for i in tr if cls_of[sub][i] == g]] - mu) / sd).mean(axis=0)
                 for g in REGIMES if any(cls_of[sub][i] == g for i in tr)}
        zj = (X[sub][j] - mu) / sd
        pred = min(sorted(cents), key=lambda g: np.linalg.norm(zj - cents[g]))
        ho_ok = bool(pred == cls_of[sub][j])
        k = int(round(acc * len(sub)))
        taskB["cells"][f"drift-reader-{tag}"] = dict(
            acc=round(float(acc), 4), n=int(len(sub)), ci_cp=cp_ci(k, len(sub)),
            heldout_ok=ho_ok, heldout_pred=pred,
            heldout_true=str(cls_of[ho_i]), oracle=False)

    # first-order cells on ORACLE windows (gift: guaranteed pre/post by planting)
    for tag, w in (("pre", pre_w), ("post", post_w)):
        cls_of = pre_cls if tag == "pre" else post_cls
        Xraw = R[:, w, :].reshape(N, -1)
        acc_1nn = loo_1nn(Xraw[sub], cls_of[sub])
        taskB["cells"][f"fo-raw-1nn-{tag}"] = dict(
            acc=round(float(acc_1nn), 4), n=int(len(sub)),
            ci_cp=cp_ci(int(round(acc_1nn * len(sub))), len(sub)), oracle=True,
            primary=True)
        Xn = np.array([norm_feats(R[i], w) for i in range(N)])
        a2 = loo_centroid(Xn[sub], cls_of[sub])
        taskB["cells"][f"fo-norm-centroid-{tag}"] = dict(
            acc=round(float(a2), 4), n=int(len(sub)),
            ci_cp=cp_ci(int(round(a2 * len(sub))), len(sub)), oracle=True,
            primary=True)
        Xm = np.array([seg_feats(R[i], w) for i in range(N)])
        a3 = loo_centroid(Xm[sub], cls_of[sub])
        taskB["cells"][f"fo-median-seg-{tag}"] = dict(
            acc=round(float(a3), 4), n=int(len(sub)),
            ci_cp=cp_ci(int(round(a3 * len(sub))), len(sub)), oracle=True,
            boundary=True)
        # static template on mean reading of the oracle window
        ok_t = 0
        Xtm = Xraw.reshape(N, -1, 7).mean(axis=1)
        for jj in range(len(sub)):
            j = int(sub[jj])
            tr = [int(x) for x in sub if x != j]
            cents = {g: Xtm[[i for i in tr if cls_of[i] == g]].mean(axis=0)
                     for g in REGIMES if any(cls_of[i] == g for i in tr)}
            pred = min(sorted(cents), key=lambda g: np.linalg.norm(Xtm[j] - cents[g]))
            ok_t += (pred == cls_of[j])
        a4 = ok_t / len(sub)
        taskB["cells"][f"fo-template-{tag}"] = dict(
            acc=round(float(a4), 4), n=int(len(sub)),
            ci_cp=cp_ci(ok_t, len(sub)), oracle=True, primary=True)
    out["taskB"] = taskB

    # ================= KILL CONDITION =========================================
    dA = taskA["cells"]["drift-reader"]
    dBp = taskB["cells"]["drift-reader-pre"]
    dBq = taskB["cells"]["drift-reader-post"]
    kill_cells = []
    for cell in PRIMARY:
        cA = taskA["cells"][cell]
        cBp = taskB["cells"].get(f"{cell}-pre")
        cBq = taskB["cells"].get(f"{cell}-post")
        if cBp is None:            # template detection cells map to template-B
            cBp = taskB["cells"].get(f"fo-template-pre")
            cBq = taskB["cells"].get(f"fo-template-post")
        a_parity = (cA["median_err"] <= 1.25 * dA["median_err"]
                    and abs(cA["r"] - dA["r"]) <= dA["r_floor"] * 2
                    and cA["detection_rate"] >= dA["detection_rate"] - 0.10)
        b_parity = (cBp["ci_cp"][0] <= dBp["ci_cp"][1]
                    and cBq["ci_cp"][0] <= dBq["ci_cp"][1])
        kill_cells.append(dict(cell=cell, taskA_parity=bool(a_parity),
                               taskB_parity=bool(b_parity),
                               kill=bool(a_parity and b_parity)))
    boundary_notes = []
    for cell in BOUNDARY:
        if cell in taskA["cells"]:
            cA = taskA["cells"][cell]
            boundary_notes.append(dict(
                cell=cell, median_err=cA["median_err"], r=cA["r"],
                detection=cA["detection_rate"],
                ties_drift=bool(cA["median_err"] <= 1.25 * dA["median_err"])))
    out["kill"] = dict(
        fires=any(k["kill"] for k in kill_cells), cells=kill_cells,
        boundary=boundary_notes,
        drift_taskA=dict(median_err=dA["median_err"], r=dA["r"],
                         detection=dA["detection_rate"]),
        drift_taskB=dict(pre=dBp["acc"], post=dBq["acc"]))

    # ================= NOISE SWEEP ============================================
    sweep = []
    # sweep the best CONTINUOUS primary cell (template cells are label-based;
    # fo-norm is the only continuous primary — pick by baseline r among these)
    cont_primary = [c for c in PRIMARY if c in CONT_CELLS]
    best_static_by_r = max(cont_primary,
                           key=lambda c: abs(taskA["cells"][c]["r"]))
    crossover = None
    for li, sig in enumerate((0.02, 0.05, 0.10, 0.20)):
        rng2 = np.random.default_rng(SEED + 2_000_000 + li)
        R2 = R + rng2.normal(0.0, sig, size=R.shape)
        row = dict(sigma_extra=sig)
        for cell in ("drift-reader", best_static_by_r):
            errs, sh_ = [], []
            for i in idx_sw:
                y = signal(cell, i, R2)
                split, _, _, _ = localize_signal(y, SEED + 3_000_000 + 97 * li + i)
                sh_.append(B + split)
                errs.append(abs(B + split - sw[i]))
            row[cell] = dict(median_err=round(float(np.median(errs)), 3),
                             r=round(pearson(np.array(sh_), sw[idx_sw]), 4))
        sweep.append(row)
        if crossover is None and row["drift-reader"]["median_err"] > 3:
            crossover = sig
    out["noise_sweep"] = dict(rows=sweep, best_static_cell=best_static_by_r,
                              crossover_sigma=crossover)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "run":
        res = run()
        with open(os.path.join(HERE, "results.json"), "w") as f:
            f.write(canonical(res))
        print(json.dumps(res, indent=1, sort_keys=True))
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
