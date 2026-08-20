#!/usr/bin/env python3
"""D″ FIXTURES — synthetic nurses for the reader-delta test (second-order JEPA).

Registered test: research/skills/devils-advocate-regress.md (pass 3) +
zeroclaw-response-rival-a.md (clause 3) + zeroclaw-response-devil-head.md (§2).

What this builds
----------------
N = 13 synthetic "nurses" (reader models). Every nurse reads the SAME shared
room corpus: the actual elephant nights (A, B, C, D, D-cold), windowed at
W=8 speaks (matching elephant params.W). The room stimulus for window t is
m(t) = mean(field_raw_after) over the window's speaks.

Nurse i's EMITTED READING of window t (her displaced field — output only):

    r_i(t) = clip( h_i + g_i(t) * (m(t) - h_i) + alpha_i * t_hat * u_i + eta , -0.05, 1.7 )

  h_i     idiosyncratic home baseline, drawn class-INDEPENDENTLY from the
          corpus field distribution (the doctrine's premise: every reader is
          a calibrated instrument with her own baseline the doctor knows)
  g_i(t)  her (planted, possibly drifting) adoption gain:
            SAUNA  decays  ~0.9 -> ~0.15   (warms less and less; anchors home)
            JADED  flat    ~0.06-0.14      (barely moves)
            OVER   rises   ~0.3  -> ~1.05  (overshoots; g>1 extrapolates past room)
  alpha_i * t_hat * u_i   planted directional drift: random unit direction u_i
          (class-independent), class-specific AMOUNT alpha_i, accumulating
  eta     per-window reading noise N(0, sigma_i^2 I_7), sigma_i ~ U(0.010, 0.020)

Classes: 4 SAUNA + 4 JADED + 4 OVER in the clustering pool (n=12) + ONE
held-out 13th nurse (class drawn by the seeded RNG before any evaluation;
the full 13-fold leave-one-out is also run by the runner, so no class is
cherry-picked).

Determinism: single seeded RNG (SEED=20260819), fixed draw order, canonical
JSON serialization -> stable SHA256 across replays. The elephant repo is
READ-ONLY (we never write there).

numpy + stdlib only. No torch, no GPU, no sklearn.
"""
import json, os, sys, hashlib
import numpy as np

SEED = 20260819
NIGHTS_DIR = os.environ.get("NIGHTS_DIR", "/home/eileen/projects/elephant/data/nights")
NIGHTS = ["A", "B", "C", "D", "D-cold"]
W = 8                # window size in speaks (elephant params.W)
SEG1_SEQ = 20        # SEG1 = warm (first 20 speaks); SEG2 = cynical (rest)
CLASSES = ["sauna", "jaded", "over"]
POOL_PER_CLASS = 4   # 12 in the clustering pool
HELDOUT_COUNT = 1    # the 13th nurse

HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures")


def load_corpus():
    """Shared room corpus: per night, non-overlapping windows of W speaks.
    Returns list of window dicts {night, win, seg, seq0, m (7,)} in stable order."""
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
            if len(win) < W // 2:      # drop tiny tail windows
                continue
            m = np.mean([d["field_raw_after"] for d in win], axis=0)
            wins.append(dict(night=night, win=wi // W,
                             seg="SEG1" if win[0]["seq"] < SEG1_SEQ else "SEG2",
                             seq0=int(win[0]["seq"]), m=m.tolist()))
    return wins


def gain_traj(cls, t_hat, g0, g_end, lam, p):
    if cls == "sauna":
        return g_end + (g0 - g_end) * np.exp(-lam * t_hat)
    if cls == "jaded":
        return np.full_like(t_hat, g0)          # flat (g0 == g_end)
    if cls == "over":
        return g0 + (g_end - g0) * np.power(t_hat, p)
    raise ValueError(cls)


def build():
    rng = np.random.default_rng(SEED)
    wins = load_corpus()
    T = len(wins)
    M = np.array([w["m"] for w in wins], float)           # (T,7) room stimulus
    mu, sd = M.mean(axis=0), M.std(axis=0)                # corpus field stats

    # --- class layout: pool = 4 per class, then 1 held-out (class by RNG) ----
    pool_classes = [c for c in CLASSES for _ in range(POOL_PER_CLASS)]
    pool_classes = list(rng.permutation(pool_classes))    # shuffle assignment order
    heldout_class = str(CLASSES[int(rng.integers(len(CLASSES)))])
    all_classes = pool_classes + [heldout_class] * HELDOUT_COUNT

    nurses = []
    for i, cls in enumerate(all_classes):
        # home baseline: class-INDEPENDENT (doctrine premise, stated in report)
        h = np.clip(mu + rng.normal(0, 1, 7) * sd * 0.9, -0.05, 1.7)
        u = rng.normal(0, 1, 7); u /= (np.linalg.norm(u) + 1e-12)
        if cls == "sauna":
            g0, g_end = rng.uniform(0.85, 0.95), rng.uniform(0.10, 0.20)
            lam, p = rng.uniform(2.5, 3.5), 1.0
            alpha = rng.uniform(0.04, 0.08)
        elif cls == "jaded":
            g0 = g_end = rng.uniform(0.06, 0.14)
            lam, p = 0.0, 1.0
            alpha = rng.uniform(0.000, 0.015)
        else:  # over
            g0, g_end = rng.uniform(0.25, 0.35), rng.uniform(0.95, 1.15)
            lam = 0.0; p = rng.uniform(0.8, 1.2)
            alpha = rng.uniform(0.02, 0.05)
        sigma = rng.uniform(0.010, 0.020)
        t_hat = np.linspace(0.0, 1.0, T)
        g = gain_traj(cls, t_hat, g0, g_end, lam, p)
        drift = alpha * t_hat[:, None] * u[None, :]
        eta = rng.normal(0.0, sigma, size=(T, 7))
        R = h[None, :] + g[:, None] * (M - h[None, :]) + drift + eta
        R = np.clip(R, -0.05, 1.7)
        nurses.append(dict(
            id=f"nurse-{i+1:02d}", cls=cls, heldout=(i >= len(pool_classes)),
            home=h.tolist(), u=u.tolist(), g0=float(g0), g_end=float(g_end),
            lam=float(lam), p=float(p), alpha=float(alpha), sigma=float(sigma),
            gain_traj=g.tolist(), readings=R.tolist(),
        ))

    manifest = dict(
        seed=SEED, nights=NIGHTS, W=W, seg1_seq=SEG1_SEQ, T=T,
        classes=CLASSES, pool_per_class=POOL_PER_CLASS,
        heldout_class=heldout_class,
        corpus_windows=wins,
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
    # separate readable copy for humans (not hashed)
    with open(os.path.join(FIXDIR, "manifest-pretty.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    # per-nurse per-window emitted readings, jsonl (one nurse per line)
    with open(os.path.join(FIXDIR, "readings.jsonl"), "w") as f:
        for n in manifest["nurses"]:
            f.write(canonical({k: n[k] for k in
                               ("id", "cls", "heldout", "readings")}) + "\n")
    h = hashlib.sha256(open(os.path.join(FIXDIR, "manifest.json"), "rb").read()).hexdigest()
    with open(os.path.join(FIXDIR, "FIXTURES-SHA256"), "w") as f:
        f.write(h + "\n")
    counts = {}
    for n in manifest["nurses"]:
        counts[n["cls"]] = counts.get(n["cls"], 0) + 1
    print(f"fixtures built: T={manifest['T']} windows, {len(manifest['nurses'])} nurses, "
          f"counts={counts} (held-out: {manifest['heldout_class']})")
    print(f"FIXTURES-SHA256={h}")


if __name__ == "__main__":
    main()
