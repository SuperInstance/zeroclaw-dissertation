#!/usr/bin/env python3
"""SWITCH-TEST FIXTURES — regime-switching nurses (Rival A's counter-proposal).

Registered in research/skills/rival-reader-delta-review.md §5.1 (the Switch
Test — falsifier #1) and §2.4 (falsifier #2, the median-trick cell), under
the discipline fixes of §5.3. This file IS the registration: thresholds
below were written BEFORE the first run. numpy + stdlib only, no torch.

THE RIVAL'S PRECISE POINT (pass 4, §5.1)
----------------------------------------
A first-order FINGERPRINT — static similarity of a nurse's readings, or
similarity of readings to a static per-class template — cannot SEE a regime
change: it maps a whole trajectory to a class, with no per-nurse temporal
model. A drift-reader — per-nurse baseline fitted from her own history +
displacement trajectory over time — MUST see it. The prior "pass" was partly
a fixture artifact (class propagation, §2.2), so this test is engineered to
force the two representations apart BY CONSTRUCTION:

  * switch points are DECOORDINATED per nurse (s_i ~ U[8,20] independent),
    so any cell whose changepoint is driven by the SHARED room corpus (raw
    magnitudes, static templates) cannot correlate its prediction with the
    planted switch, while a self-referential displacement trajectory can;
  * first-order cells receive every fair gift the rival's audit demands:
    oracle-clean fixed segments for classification, LOO supervised static
    templates for detection, and the median-trick / crowd-normalization
    BOUNDARY cells (§2.4) reported in every table.

WHAT THIS BUILDS
----------------
Same shared room corpus and reader model as reader-delta-test/build_fixtures.py
(reused family): all 5 elephant nights, W=8 windows -> T windows; room
stimulus m(t) = mean(field_raw_after). Nurse i's emitted reading:

    r_i(t) = clip( h_i + g_i(t)*(m(t) - h_i) + alpha_i*t_hat*u_i + eta, -.05, 1.7 )

h_i     idiosyncratic home baseline, class-INDEPENDENT (doctrine premise)
g_i(t)  REGIME-SWITCHING gain: pre-regime canonical curve on pre-local time
        t in [0, s_i), post-regime canonical curve (fresh params, LOCAL time
        restart) on [s_i, T). The switch at s_i is planted and known.
        Regime primitives (local time t_loc in [0,1]):
          sauna  g_end + (g0-g_end)*exp(-lam*t_loc)   g0~.80-.95 -> .10-.20, lam~1.0-1.8
          jaded  flat ~ .06-.14
          over   g0 + (g_end-g0)*t_loc**p             g0~.45-.60 -> .95-1.15
          osc    .55 + A*sin(2*pi*F*t_loc + phi)      A~.25-.35, F~1.5-2.5; post flips phase (pi)
alpha_i*t_hat*u_i  tiny class-independent directional drift
eta     per-window noise N(0, sigma_i^2 I_7), sigma_i ~ U(.010,.020)

FAMILIES (7): all 6 ordered pairs of {sauna, jaded, over} + osc>osc (phase
flip). Pool = 2 nurses per family (14) + 1 held-out switching nurse (family
drawn by the seeded RNG before any evaluation) = 15 switching. Plus 4
NO-SWITCH controls (one per single regime incl. osc) = 19 nurses total.
N >= 12 required; 19 delivered.

PRE-REGISTERED THRESHOLDS (written before the first run; burner = T/8 ~= 3)
--------------------------------------------------------------------------
Representations compared by ONE localizer for continuous signals: two-
segment piecewise-linear fit of the signal over windows [B=6, T); split
point = predicted switch, delta-SSE = single-line SSE minus best two-line
SSE; detection flag if delta-SSE >= 2x the median of 1000 seeded
time-permutations of the same signal. Label-sequence cells (static
templates) use the analogous optimal two-block label split. All cells share
this machinery: any difference is representational, not estimatorial.

TASK A (switch detection/localization) — drift-reader passes iff ALL:
  (a) Pearson r(shat, s) across the 15 switching nurses >= 2x the
      permutation floor (median |r| over 1000 seeded permutations of s);
  (b) median |shat - s| <= 3 windows;
  (c) per-nurse detection rate >= 80% of switching nurses.
KILL CONDITION (reindex): fires iff a PRIMARY first-order cell (fo-norm,
fo-template-euclid, fo-template-cosine — no per-nurse model) reaches parity
with the drift-reader on Task A (median err <= 1.25x drift-reader's AND
r within floor noise of drift-reader's AND detection within 10 points) AND
Task B parity (LOO accuracy CIs overlapping on both pre and post).
BOUNDARY cells (fo-median-static, fo-median-seg, fo-crowd: per-reader static
normalization / cross-nurse consensus) adjudicate LANGUAGE ONLY (rival §2.4
concession): if a boundary cell ties, the verdict is "not an identity, one
normalization", not full reindex.

TASK B (regime classification, 4-way {sauna,jaded,over,osc}, chance .25) —
drift-reader passes iff LOO accuracy >= 2x chance (.50) on BOTH pre and
post regimes, using its own LOCALIZED segments and segment-local baselines
(rival §5.3 rule 1: no shared estimator). First-order cells receive
ORACLE-CLEAN FIXED windows [0,8) and [21,T) — segments guaranteed pre/post
for every nurse by planting (s in [8,20]): a gift the drift-reader does not
need; if first-order still loses with oracle segments, the loss is
representational, not segmentational.

Noise sweep: extra sigma in {.02,.05,.10,.20} added at run time (seeded,
fixtures untouched); crossover = first level where drift-reader fails (b).
CIs: bootstrap (10k, seeded) on medians; exact Clopper-Pearson on accuracy.
Replays: canonical results hash 3/3 identical; fixtures SHA256-pinned.

AMENDMENT LOG
-------------
2026-08-19 (pre-run): none. Thresholds above written before the first run.
2026-08-19 (post first run, disclosed): the RUNNER's localizer was amended
  (piecewise-linear -> smoothed two-segment constant fit) after the first
  run showed the linear fit ill-identified under within-regime room wiggle;
  see run_switch.py AMENDMENT 1. This file's generative code and fixtures
  are untouched (FIXTURES-SHA256 unchanged). The osc>osc family was
  registered as exploratory for localization: mean-neutral phase flips are
  invisible to mean-shift machinery by construction.

Determinism: single seeded RNG (SEED=20260819), fixed draw order with
branch-independent consumption (every nurse draws the same block shapes),
canonical JSON. Elephant data is READ-ONLY.
"""
import json, os, hashlib
import numpy as np

SEED = 20260819
NIGHTS_DIR = os.environ.get("NIGHTS_DIR", "/home/eileen/projects/elephant/data/nights")
NIGHTS = ["A", "B", "C", "D", "D-cold"]
W = 8
B_BURNIN = 6          # drift-reader burn-in windows (pre-registered)
S_LO, S_HI = 8, 20    # planted switch window range, inclusive (decoordinated)
PRE_W_END = 8         # fixed oracle pre-window  [0, 8)   (s >= 8 for all)
POST_W_START = 21     # fixed oracle post-window [21, T)  (s <= 20 for all)
FAMILIES = ["sauna>jaded", "jaded>sauna", "sauna>over", "over>sauna",
            "jaded>over", "over>jaded", "osc>osc"]
CONTROLS = ["sauna", "jaded", "over", "osc"]
PER_FAMILY = 2
HELDOUT_COUNT = 1

HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures")


def load_corpus():
    """Identical loader to reader-delta-test/build_fixtures.py (reused family)."""
    wins = []
    for night in NIGHTS:
        speaks = []
        for line in open(f"{NIGHTS_DIR}/night-{night}.jsonl"):
            d = json.loads(line)
            if d["type"] == "speak":
                speaks.append(d)
        speaks.sort(key=lambda d: d["seq"])
        for wi in range(0, len(speaks), W):
            win = speaks[wi:wi + W]
            if len(win) < W // 2:
                continue
            m = np.mean([d["field_raw_after"] for d in win], axis=0)
            wins.append(dict(night=night, win=wi // W,
                             seg="SEG1" if win[0]["seq"] < 20 else "SEG2",
                             seq0=int(win[0]["seq"]), m=m.tolist()))
    return wins


def regime_params(rng, regime, flip_phase=False):
    """Draw a FIXED block of 6 uniforms, then map by regime (branch-independent
    RNG consumption). Returns (params dict, gain function of local time)."""
    q = rng.uniform(size=6)
    if regime == "sauna":
        p = dict(g0=0.80 + 0.15 * q[0], g_end=0.10 + 0.10 * q[1],
                 lam=1.0 + 0.8 * q[2])
        f = lambda tl: p["g_end"] + (p["g0"] - p["g_end"]) * np.exp(-p["lam"] * tl)
    elif regime == "jaded":
        p = dict(g=0.06 + 0.08 * q[0])
        f = lambda tl: np.full_like(np.asarray(tl, float), p["g"])
    elif regime == "over":
        p = dict(g0=0.45 + 0.15 * q[0], g_end=0.95 + 0.20 * q[1],
                 pw=0.8 + 0.4 * q[2])
        f = lambda tl: p["g0"] + (p["g_end"] - p["g0"]) * np.power(tl, p["pw"])
    elif regime == "osc":
        p = dict(A=0.25 + 0.10 * q[0], F=1.5 + 1.0 * q[1],
                 phi=2 * np.pi * q[2], flip=bool(flip_phase))
        sgn = -1.0 if flip_phase else 1.0
        f = lambda tl: 0.55 + sgn * p["A"] * np.sin(2 * np.pi * p["F"] * tl + p["phi"])
    else:
        raise ValueError(regime)
    return p, f


def build():
    rng = np.random.default_rng(SEED)
    wins = load_corpus()
    T = len(wins)
    assert T >= POST_W_START + 3, f"corpus too short: T={T}"
    M = np.array([w["m"] for w in wins], float)
    mu, sd = M.mean(axis=0), M.std(axis=0)

    # --- layout: pool (2 per family, permuted) + 1 held-out + 4 controls ----
    pool_fams = [f for f in FAMILIES for _ in range(PER_FAMILY)]
    pool_fams = [str(x) for x in rng.permutation(pool_fams)]
    heldout_fam = str(FAMILIES[int(rng.integers(len(FAMILIES)))])

    layout = [(f, False) for f in pool_fams] + [(heldout_fam, True)] \
        + [(f"control:{c}", False) for c in CONTROLS]

    nurses = []
    for i, (fam, heldout) in enumerate(layout):
        control = fam.startswith("control:")
        h = np.clip(mu + rng.normal(0, 1, 7) * sd * 0.9, -0.05, 1.7)
        u = rng.normal(0, 1, 7); u /= (np.linalg.norm(u) + 1e-12)
        sigma = float(rng.uniform(0.010, 0.020))
        alpha = float(rng.uniform(0.005, 0.020))
        s = int(rng.integers(S_LO, S_HI + 1))          # always drawn (branch-free)
        pre, post = (fam.split(">") + [None])[:2] if not control else \
            (fam.split(":")[1], fam.split(":")[1])
        pp, fpre = regime_params(rng, pre)
        qp, fpost = regime_params(rng, post, flip_phase=(post == "osc"))
        eta = rng.normal(0.0, sigma, size=(T, 7))
        t_glob = np.arange(T, dtype=float)

        # gain trajectory: pre-regime on pre-local time, post on post-local.
        # CONTROLS: one pure regime instance over the full span, NO restart
        # (the post block is still drawn+stored to keep RNG order branch-free).
        g = np.empty(T)
        n_pre = max(s, 1)
        if control:
            g[:] = fpre(t_glob / max(T - 1, 1))
        else:
            g[:s] = fpre(t_glob[:s] / max(n_pre - 1, 1))
            if s < T:
                g[s:] = fpost((t_glob[s:] - s) / max(T - 1 - s, 1))
        drift = alpha * (t_glob / max(T - 1, 1))[:, None] * u[None, :]
        R = h[None, :] + g[:, None] * (M - h[None, :]) + drift + eta
        R = np.clip(R, -0.05, 1.7)

        nurses.append(dict(
            id=f"nurse-{i+1:02d}", family=None if control else fam,
            control=control, heldout=bool(heldout),
            pre=pre, post=post, switch=None if control else int(s),
            home=h.tolist(), u=u.tolist(), sigma=sigma, alpha=alpha,
            pre_params=pp, post_params=qp,
            gain_traj=g.tolist(), readings=R.tolist(),
        ))

    manifest = dict(
        seed=SEED, nights=NIGHTS, W=W, T=T, burnin=B_BURNIN,
        s_range=[S_LO, S_HI], oracle_pre_window=[0, PRE_W_END],
        oracle_post_window=[POST_W_START, T],
        families=FAMILIES, controls=CONTROLS, per_family=PER_FAMILY,
        heldout_family=heldout_fam, corpus_windows=wins,
        corpus_stats=dict(mu=mu.tolist(), sd=sd.tolist()),
        nurses=nurses,
    )
    return manifest


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def main():
    manifest = build()
    os.makedirs(FIXDIR, exist_ok=True)
    with open(os.path.join(FIXDIR, "manifest.json"), "w") as f:
        f.write(canonical(manifest))
    with open(os.path.join(FIXDIR, "manifest-pretty.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    with open(os.path.join(FIXDIR, "readings.jsonl"), "w") as f:
        for n in manifest["nurses"]:
            f.write(canonical({k: n[k] for k in
                               ("id", "family", "control", "heldout", "pre",
                                "post", "switch", "readings")}) + "\n")
    h = hashlib.sha256(open(os.path.join(FIXDIR, "manifest.json"), "rb").read()).hexdigest()
    with open(os.path.join(FIXDIR, "FIXTURES-SHA256"), "w") as f:
        f.write(h + "\n")
    fam_counts = {}
    for n in manifest["nurses"]:
        if not n["control"]:
            fam_counts[n["family"]] = fam_counts.get(n["family"], 0) + 1
    sw = [n["switch"] for n in manifest["nurses"] if n["switch"] is not None]
    print(f"switch fixtures: T={manifest['T']} windows, "
          f"{len(manifest['nurses'])} nurses "
          f"({sum(fam_counts.values())} switching, 4 controls)")
    print(f"family counts: {fam_counts}  held-out: {manifest['heldout_family']}")
    print(f"planted switches: {sorted(sw)}")
    print(f"FIXTURES-SHA256={h}")


if __name__ == "__main__":
    main()
