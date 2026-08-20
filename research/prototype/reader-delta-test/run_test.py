#!/usr/bin/env python3
"""READER-DELTA TEST — the pre-registered three-clause test (2026-08-19).

Registered in:
  research/skills/devils-advocate-regress.md   (clauses 1+2, kill condition)
  research/skills/zeroclaw-response-rival-a.md  (clause 3: cross-strata transfer)
  research/skills/zeroclaw-response-devil-head.md (D″ fixtures framing)

CLAUSE 1 (blind discrimination). Unsupervised k-means (k=3) over the
  READER-DELTA representation — computed ONLY from each nurse's emitted
  readings (never room inputs): fitted baseline b̂ = componentwise median of
  her own readings; delta δ(t)=r(t)−b̂; normalized excursion
  e(t)=‖δ(t)‖/(‖b̂‖+ε); feature vector = [e(0..T−1), slope(e), mean(e),
  std(e), lag-1 autocorr(δ)] — the doctor's three reads: displacement per
  window, tempo (slope), volatility (variance/autocorr). Threshold:
  purity ≥ 2× noise floor (median of 1000 seeded label permutations of the
  same partition; p95 also reported), 3/3 deterministic replays, held-out
  13th nurse assigned to its planted class by nearest centroid.

KILL CONDITION. The SAME clustering on the FIRST-ORDER representation:
  plain similarity of the readings themselves (concatenated r(t), no
  baseline model, no centering). If it performs as well, the second-order
  object is a reindex. Ablations reported in the open: first-order+cosine,
  and first-order+per-nurse-centering (centering IS the baseline model —
  the smuggled second-order; reported so the committee can see where the
  information lives).

CLAUSE 2 (calibration, the D″). Pre-registered scalar indices from the
  reader-delta representation: DI = OLS slope of e(t) (drift tempo),
  MI = mean e (drift amount). d′ per planted class-pair on each index
  (pooled-SD form) + 2-D Mahalanobis d′ on (DI,MI); aggregate = mean over
  pairs. A calibrated delta, not a felt one.

CLAUSE 3 (cross-strata transfer, Rival A's clause). From SEG1 (warm,
  first-20-speaks windows) outputs ONLY: features ê1 = mean e over SEG1,
  slope1 = OLS slope of e vs global window index within SEG1. Leave-one-
  nurse-out (13-fold): linear regression [1, ê1, slope1] → ê2 (mean e over
  SEG2) on 12 nurses, predict the held-out nurse's SEG2 excursion; plus
  nearest-class-centroid classification of SEG2 class from SEG1 features.
  First-order best attempt at the same question: 1-NN in SEG1 raw readings
  → copy neighbor's SEG2 class. Chance = 1/3.

Determinism: every stochastic step (k-means inits, permutations) is seeded
from SEED in fixed order; the whole pipeline is re-run 3× by --verify-replay
and the canonical results hash must be identical 3/3.

numpy + stdlib only.
"""
import json, os, sys, hashlib, subprocess
import numpy as np

SEED = 20260819
K = 3
N_PERM = 1000
HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures")
sys.path.insert(0, HERE)
from build_fixtures import load_corpus, canonical, NIGHTS, W, SEG1_SEQ  # noqa: E402


# ---------------------------------------------------------------- utilities
def kmeans(X, k, seed, n_init=25, iters=200):
    """Deterministic Lloyd k-means. Returns labels, centroids, inertia."""
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n_init):
        C = X[rng.choice(len(X), size=k, replace=False)].copy()
        for _ in range(iters):
            D = np.linalg.norm(X[:, None, :] - C[None, :, :], axis=2)
            lab = D.argmin(axis=1)
            newC = np.array([X[lab == j].mean(axis=0) if np.any(lab == j)
                             else C[j] for j in range(k)])
            if np.allclose(newC, C, atol=1e-12):
                break
            C = newC
        D = np.linalg.norm(X[:, None, :] - C[None, :, :], axis=2)
        inertia = float((D.min(axis=1) ** 2).sum())
        if best is None or inertia < best[2] - 1e-12:
            best = (lab.copy(), C.copy(), inertia)
    return best


def purity(labels, classes):
    classes = np.asarray(classes)
    tot = 0
    for c in np.unique(labels):
        members = classes[labels == c]
        tot += np.max([int(np.sum(members == g)) for g in np.unique(classes)])
    return tot / len(classes)


def perm_noise_floor(labels, classes, seed, n_perm=N_PERM):
    """Purity of the SAME partition against permuted planted labels."""
    rng = np.random.default_rng(seed)
    classes = np.asarray(classes)
    vals = np.array([purity(labels, rng.permutation(classes)) for _ in range(n_perm)])
    return float(np.median(vals)), float(np.percentile(vals, 95))


def zscore_fit(X):
    mu, sd = X.mean(axis=0), X.std(axis=0) + 1e-12
    return (X - mu) / sd, mu, sd


def assign(C, X):
    D = np.linalg.norm(X[:, None, :] - C[None, :, :], axis=2)
    return D.argmin(axis=1), D.min(axis=1)


def dpair(x, a, b, classes):
    """Univariate d′ (pooled-SD) of index x for class a vs class b."""
    xa, xb = x[classes == a], x[classes == b]
    s = np.sqrt((xa.var(ddof=1) + xb.var(ddof=1)) / 2.0) + 1e-12
    return float((xa.mean() - xb.mean()) / s)


def mahalanobis_dprime(X, a, b, classes):
    """2-D Mahalanobis d′ between class means, pooled within-class covariance."""
    A, B = X[classes == a], X[classes == b]
    d = A.mean(axis=0) - B.mean(axis=0)
    S = ((A - A.mean(0)).T @ (A - A.mean(0)) + (B - B.mean(0)).T @ (B - B.mean(0))) \
        / (len(A) + len(B) - 2)
    S += np.eye(2) * 1e-6
    return float(np.sqrt(max(d @ np.linalg.solve(S, d), 0.0)))


def majority(vals):
    """Deterministic majority (ties -> lexicographically first)."""
    u, c = np.unique(np.asarray(vals), return_counts=True)
    return str(u[int(np.argmax(c))])



def ols_slope(y, x):
    x = np.asarray(x, float); y = np.asarray(y, float)
    xm, ym = x.mean(), y.mean()
    return float(((x - xm) * (y - ym)).sum() / (((x - xm) ** 2).sum() + 1e-12))


def lag1_acorr(D):
    """Mean lag-1 autocorrelation over dims of delta series D (T,7)."""
    vals = []
    for j in range(D.shape[1]):
        s = D[:, j]; s = s - s.mean()
        den = (s * s).sum()
        vals.append((s[:-1] * s[1:]).sum() / (den + 1e-12))
    return float(np.mean(vals))


# ------------------------------------------------------------- the pipeline
def run():
    man = json.load(open(os.path.join(FIXDIR, "manifest.json")))
    T = man["T"]
    nurses = man["nurses"]
    # integrity: corpus windows must match the live elephant data (read-only)
    live = load_corpus()
    assert T == len(live) and all(a["m"] == b["m"] and a["night"] == b["night"]
                                  for a, b in zip(man["corpus_windows"], live)), \
        "fixture corpus drifted from elephant nights"

    ids = [n["id"] for n in nurses]
    cls = np.array([n["cls"] for n in nurses])
    heldout = np.array([n["heldout"] for n in nurses])
    R = np.array([n["readings"] for n in nurses], float)      # (N,T,7)
    N = len(nurses)
    t = np.arange(T, dtype=float)
    seg1 = np.array([w["seg"] == "SEG1" for w in man["corpus_windows"]])
    seg2 = ~seg1

    # ---- reader-delta representation (OUTPUT-ONLY) --------------------------
    B = np.median(R, axis=1)                                  # (N,7) fitted baseline
    D = R - B[:, None, :]                                     # (N,T,7) deltas
    nb = np.linalg.norm(B, axis=1) + 1e-9
    E = np.linalg.norm(D, axis=2) / nb[:, None]               # (N,T) excursion
    DI = np.array([ols_slope(E[i], t / max(T - 1, 1)) for i in range(N)])
    MI = E.mean(axis=1)
    SI = E.std(axis=1)
    A1 = np.array([lag1_acorr(D[i]) for i in range(N)])
    delta_feats = np.column_stack([E, DI, MI, SI, A1])        # (N, T+4)

    # ---- first-order representations ---------------------------------------
    fo = R.reshape(N, T * 7)                                  # plain readings
    fo_cos = fo / (np.linalg.norm(fo, axis=1, keepdims=True) + 1e-12)
    fo_cent = fo - fo.mean(axis=1, keepdims=True)             # smuggled baseline
    fo_norm = np.linalg.norm(R, axis=2)                       # reading-norm traj (no baseline)

    pool = ~heldout
    pool_ids = [ids[i] for i in np.where(pool)[0]]

    # =============== CLAUSE 1 =================================================
    seed = SEED + 1
    out = {}
    cl1 = {}
    for name, X in (("delta", delta_feats), ("first-order", fo),
                    ("first-order-cosine(ablation)", fo_cos),
                    ("first-order-centered(ablation)", fo_cent),
                    ("first-order-normtraj(ablation)", fo_norm)):
        Xz, mu_z, sd_z = zscore_fit(X[pool])                  # fit on pool only
        lab, C, inertia = kmeans(Xz, K, seed); seed += 1
        pur = purity(lab, cls[pool])
        floor_med, floor_p95 = perm_noise_floor(lab, cls[pool], seed); seed += 1
        # 1-NN retrieval (euclidean in the same standardized space)
        dmat = np.linalg.norm(Xz[:, None] - Xz[None, :], axis=2)
        np.fill_diagonal(dmat, np.inf)
        nn_same = float(np.mean(cls[pool][dmat.argmin(1)] == cls[pool]))
        cl1[name] = dict(purity=pur, floor_med=floor_med, floor_p95=floor_p95,
                         ratio=pur / floor_med, retrieval_1nn=nn_same)
    out["clause1"] = cl1

    # held-out 13th nurse (never in clustering) — nearest centroid in delta space
    Xz, mu_z, sd_z = zscore_fit(delta_feats[pool])
    _, C, _ = kmeans(Xz, K, SEED + 1)
    lab_pool, _ = assign(C, Xz)
    ho_i = int(np.where(heldout)[0][0])
    z_ho = ((delta_feats[ho_i] - mu_z) / sd_z)[None, :]
    ho_lab = int(assign(C, z_ho)[0][0])
    ho_members = cls[pool][lab_pool == ho_lab]
    ho_pred = {g: int((ho_members == g).sum()) for g in np.unique(cls[pool])}
    ho_pred_cls = max(ho_pred, key=ho_pred.get)
    out["heldout_13th"] = dict(id=ids[ho_i], true=cls[ho_i], pred=ho_pred_cls,
                               votes=ho_pred, correct=bool(ho_pred_cls == cls[ho_i]))

    # 13-fold leave-one-out (no cherry-pick: every nurse held out in turn)
    loo_ok, loo_detail = 0, []
    for j in range(N):
        tr = np.array([i for i in range(N) if i != j])
        Xz2, m2, s2 = zscore_fit(delta_feats[tr])
        lab2, C2, _ = kmeans(Xz2, K, SEED + 100 + j)
        votes = {}
        for c in np.unique(lab2):
            mem = cls[tr][lab2 == c]
            votes[majority(mem)] = int((lab2 == c).sum())
        pred = max(sorted(votes), key=lambda g: (votes[g], g))
        zj = (delta_feats[j] - m2) / s2
        nearest = int(assign(C2, zj[None, :])[0][0])
        # majority planted class of that nearest cluster
        mem = cls[tr][lab2 == nearest]
        p = majority(mem)
        ok = p == cls[j]
        loo_ok += ok
        loo_detail.append(dict(id=ids[j], true=cls[j], pred=p, correct=bool(ok)))
    out["loo_13fold_accuracy"] = loo_ok / N

    # k-means seed stability of the winning delta partition (up to relabeling)
    def canon_part(lab):
        return tuple(sorted(tuple(sorted(np.where(lab == c)[0].tolist()))
                            for c in np.unique(lab)))
    parts = [canon_part(kmeans(zscore_fit(delta_feats[pool])[0], K, SEED + 500 + s)[0])
             for s in range(10)]
    seed_purities = [purity(kmeans(zscore_fit(delta_feats[pool])[0], K, SEED + 500 + s)[0],
                            cls[pool]) for s in range(10)]
    out["kmeans_seed_stability"] = len(set(parts)) == 1
    out["kmeans_seed_purity_min"] = float(min(seed_purities))
    out["retrieval_chance"] = float(np.mean(
        [np.sum(cls[pool] == g) - 1 for g in cls[pool]]) / (int(pool.sum()) - 1))

    # =============== CLAUSE 2 (d′ calibration) ================================
    cl2 = {"pairs": {}}
    for a, b in (("sauna", "over"), ("sauna", "jaded"), ("jaded", "over")):
        m = mahalanobis_dprime(np.column_stack([DI, MI]), a, b, cls)
        cl2["pairs"][f"{a}-vs-{b}"] = dict(
            dprime_DI=dpair(DI, a, b, cls), dprime_MI=dpair(MI, a, b, cls),
            dprime_mahalanobis=m)
    cl2["aggregate_mahalanobis_mean"] = float(np.mean(
        [v["dprime_mahalanobis"] for v in cl2["pairs"].values()]))
    out["clause2"] = cl2

    # =============== CLAUSE 3 (cross-strata transfer) =========================
    e1 = E[:, seg1].mean(axis=1)                     # SEG1 excursion level
    e2 = E[:, seg2].mean(axis=1)                     # SEG2 excursion level
    sl1 = np.array([ols_slope(E[i, seg1], t[seg1]) for i in range(N)])
    X3 = np.column_stack([np.ones(N), e1, sl1])

    # LOO regression e2 ~ [1, e1, slope1]  (fit on 12, predict the held-out)
    preds, actuals, base_preds = [], [], []
    for j in range(N):
        tr = np.array([i for i in range(N) if i != j])
        beta, *_ = np.linalg.lstsq(X3[tr], e2[tr], rcond=None)
        preds.append(float(X3[j] @ beta)); actuals.append(float(e2[j]))
        base_preds.append(float(e2[tr].mean()))
    preds, actuals, base_preds = map(np.array, (preds, actuals, base_preds))
    r = float(np.corrcoef(preds, actuals)[0, 1])
    mae = float(np.mean(np.abs(preds - actuals)))
    mae_base = float(np.mean(np.abs(base_preds - actuals)))
    r2_loo = float(1 - (np.sum((preds - actuals) ** 2)) /
                   (np.sum((base_preds - actuals) ** 2)))

    # LOO class transfer: nearest class-centroid in SEG1 (e1, slope1) space
    X3z = np.column_stack([(e1 - e1.mean()) / (e1.std() + 1e-12),
                           (sl1 - sl1.mean()) / (sl1.std() + 1e-12)])
    cent = {g: X3z[cls == g].mean(axis=0) for g in np.unique(cls)}
    # honest LOO: centroid of class g excludes nurse j
    tr3_ok = 0
    for j in range(N):
        cents = {}
        for g in np.unique(cls):
            mem = [i for i in range(N) if cls[i] == g and i != j]
            cents[g] = X3z[mem].mean(axis=0)
        p = min(cents, key=lambda g: np.linalg.norm(X3z[j] - cents[g]))
        tr3_ok += (p == cls[j])

    # first-order best attempts: 1-NN and 3-NN on SEG1 raw readings -> copy SEG2 class
    fo1 = R[:, seg1, :].reshape(N, int(seg1.sum()) * 7)
    fo1n = np.linalg.norm(R[:, seg1, :], axis=2)          # SEG1 norm traj variant
    fo_ok, fo3_ok, fon_ok = 0, 0, 0
    fo_miss, fo3_miss, fon_miss = [], [], []
    for j in range(N):
        tr = [i for i in range(N) if i != j]
        d = np.linalg.norm(fo1[tr] - fo1[j], axis=1)
        order = np.array(tr)[np.argsort(d)]
        fo_ok += (cls[order[0]] == cls[j])
        if cls[order[0]] != cls[j]:
            fo_miss.append(dict(id=ids[j], true=cls[j], pred=str(cls[order[0]])))
        top3 = cls[order[:3]]
        p3 = majority(top3)
        fo3_ok += (p3 == cls[j])
        if p3 != cls[j]:
            fo3_miss.append(dict(id=ids[j], true=cls[j], pred=p3))
        dn = np.linalg.norm(fo1n[tr] - fo1n[j], axis=1)
        pn = cls[np.array(tr)[int(dn.argmin())]]
        fon_ok += (pn == cls[j])
        if pn != cls[j]:
            fon_miss.append(dict(id=ids[j], true=cls[j], pred=str(pn)))
    out["clause3"] = dict(
        transfer_r=r, mae=mae, mae_chance_baseline=mae_base, r2_loo=r2_loo,
        class_transfer_accuracy=tr3_ok / N, class_transfer_chance=1 / 3,
        firstorder_1nn_accuracy=fo_ok / N,
        firstorder_3nn_accuracy=fo3_ok / N,
        firstorder_normtraj_1nn_accuracy=fon_ok / N,
        firstorder_1nn_misses=fo_miss, firstorder_3nn_misses=fo3_miss,
        firstorder_normtraj_misses=fon_miss)

    out["meta"] = dict(N=N, T=T, seed=SEED,
                       class_counts={str(g): int((cls == g).sum()) for g in np.unique(cls)},
                       heldout_class=man["heldout_class"])
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "run":
        print(json.dumps(run(), indent=1, sort_keys=True))
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
