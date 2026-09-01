#!/usr/bin/env python3
"""FORMALIZATION lane — numerical re-verification of the ladder table + T4 H5 falsification.

Re-runs, in numpy float64, the six glm53 counterexamples whose parameters are
explicit in identifiability-glm53.txt, and measures the ladder-table digits of
THESIS-V3.2 §2.0 against fresh execution. Mismatches are findings, reported as-is.

KILL CONDITIONS — registered BEFORE execution (2026-08-31, before any run):

  R1 (ladder re-verification): each counterexample must reproduce its published
      digits to 6 decimals, else the ladder table entry is a FINDING (reported,
      not patched).
  T4-KILL (H5 minimally-fibered claim): the claim dies if a search finds a pair
      (s, s') of DISTINCT configurations with H5(s) = H5(s') to within 1e-9
      componentwise, where s' is NOT obtained from s by a symmetry-group
      element G = <tangent mirror, phase shift (cyclic window shift), time
      reversal> on a symmetric cloud. The search space is declared exhaustively
      below (sign-pattern families, phase-shifted clouds, small amplitudes,
      N=12 and N=10); anything outside it is stated as UNSEARCHED.
"""
import numpy as np

rng = np.random.default_rng
OUT = []

def rep(tag, val):
    OUT.append(f"{tag}: {val}")
    print(f"{tag}: {val}")

np.set_printoptions(precision=6, suppress=False)

e = np.eye(7)

# ---------- observable definitions (per prompt; tangent frame = ambient dial axes) ----------
def tangent(Z):
    rbar = Z.mean(0)
    rho = np.linalg.norm(rbar)
    mu = rbar / rho
    V = (Z - np.outer(Z @ mu, mu))          # ambient-centered, then projected? use standard:
    V = Z - np.outer(Z @ mu, mu)            # tangent deviation v_i = z_i - (z_i.mu) mu
    return rbar, rho, mu, V

def H_parts(Z):
    rbar, rho, mu, V = tangent(Z)
    C = V.T @ V / len(Z)
    return rbar, rho, mu, V, C

def A1(V):
    n = len(V) - 1
    return sum(np.outer(V[i], V[i+1]) for i in range(n)) / n

def M3(V):
    return np.einsum('ni,nj,nk->ijk', V, V, V).mean(0)

def mirror(Z):
    rbar, rho, mu, V = tangent(Z)
    sig = 2*np.outer(mu, mu) - np.eye(7)
    return Z @ sig.T

def matched_dist(Z, Zp):
    """exact-ish matching distance via brute-force permutations for small N is N! —
    use the declared permutation when the construction gives one, else greedy/Hungarian."""
    from scipy.optimize import linear_sum_assignment
    D2 = ((Z[:, None, :] - Zp[None, :, :])**2).sum(-1)
    r, c = linear_sum_assignment(D2)
    return np.sqrt(D2[r, c].sum())

HAVE_SCIPY = True
try:
    from scipy.optimize import linear_sum_assignment
except ImportError:
    HAVE_SCIPY = False

def matched_dist(Z, Zp):
    if not HAVE_SCIPY:
        return np.linalg.norm(Z - Zp)  # fallback: same-index (valid when constructions align)
    D2 = ((Z[:, None, :] - Zp[None, :, :])**2).sum(-1)
    r, c = linear_sum_assignment(D2)
    return np.sqrt(D2[r, c].sum())

print("="*80)
print("CX1 — H1 fiber gadget (orthogonal-axis pair swap)")
th = np.pi/6
u, w = e[0], e[1]
E7 = e[6]
base = [np.cos(th)*E7 + np.sin(th)*u, np.cos(th)*E7 - np.sin(th)*u,
        np.cos(th)*E7 + np.sin(th)*w, np.cos(th)*E7 - np.sin(th)*w] + [E7.copy() for _ in range(8)]
Z = np.array(base)
Zp = Z.copy(); Zp[[0,1,2,3]] = Zp[[2,3,0,1]]
d = np.abs(Z.mean(0) - Zp.mean(0)).max()
rep("CX1 max|meanA - meanB|", f"{d:.3e}  (published: 1e-17)")
rep("CX1 rho", f"{np.linalg.norm(Z.mean(0)):.6f}  (published rho value for CX2 gadget; here informational)")

print("="*80)
print("CX2 — H2spec pair (rotation phi=pi/5 mixing dial1->dial3, alpha=pi/6, N=12)")
alpha, phi = np.pi/6, np.pi/5
u1 = np.cos(phi)*e[0] + np.sin(phi)*e[2]; u2 = e[1]
def cloud(vs):
    pts = [np.cos(alpha)*E7 + np.sin(alpha)*v for v in vs] + [np.cos(alpha)*E7 - np.sin(alpha)*v for v in vs]
    pts += [E7.copy() for _ in range(8)]
    return np.array(pts)
ZA = cloud([e[0], e[1]]); ZB = cloud([u1, u2])
_, rhoA, muA, VA, CA = H_parts(ZA)
_, rhoB, muB, VB, CB = H_parts(ZB)
evA = np.sort(np.linalg.eigvalsh(CA))[::-1]; evB = np.sort(np.linalg.eigvalsh(CB))[::-1]
rep("CX2 rho A/B", f"{rhoA:.6f} / {rhoB:.6f}  (published: 0.955342 both)")
rep("CX2 max|eigA-eigB|", f"{np.abs(evA-evB).max():.3e}  (published: 1.7e-18)")
rep("CX2 eigs A", np.array2string(evA, precision=6))
rep("CX2 max|CA-CB|", f"{np.abs(CA-CB).max():.6f}  (published: 0.019814)")
rep("CX2 matched distance", f"{matched_dist(ZA, ZB):.6f}  (published: 0.437016)")

print("="*80)
print("CX3 — H2full pair (sign patterns, k=0.1, N=12)")
k = 0.1
patA = np.array([+3,+3,-2,-2,-1,-1])*k
patB = np.array([+3,-3,+2,-2,+1,-1])*k
def cloud1d(pats):
    pts = [np.sqrt(1-a*a)*E7 + a*e[0] for a in pats] + [E7.copy() for _ in range(6)]
    return np.array(pts)
Z3A = cloud1d(patA); Z3B = cloud1d(patB)
_, rhoA, muA, VA, CA = H_parts(Z3A)
_, rhoB, muB, VB, CB = H_parts(Z3B)
m3A = (VA**3).mean(0); m3B = (VB**3).mean(0)
rep("CX3 rho A/B", f"{rhoA:.6f} / {rhoB:.6f}  (published: 0.988120 both)")
rep("CX3 max|CA-CB|", f"{np.abs(CA-CB).max():.6f}  (published: 0.000e+00)")
rep("CX3 third moment e1 A/B", f"{m3A[0]:.6f} / {m3B[0]:.6f}  (published: 0.003000 / 0.000000)")
rep("CX3 matched distance", f"{matched_dist(Z3A, Z3B):.6f}  (published: 0.200000)")

print("="*80)
print("CX4 — 2-atomic moment sharpness (1D check, b=2)")
b = 2.0; wgt = 1/(1+b*b)
# mu = .5(d_-1 + d_+1); nu = w d_b + (1-w) d_-1/b ; moments deg 0,1,2
for deg in [0,1,2]:
    m_mu = 0.5*((-1)**deg + (1)**deg)
    m_nu = wgt*(b**deg) + (1-wgt)*((-1/b)**deg)
    rep(f"CX4 moment deg{deg} mu/nu", f"{m_mu:.12f} / {m_nu:.12f}")
rep("CX4 deg3 mu/nu", f"{0.5*((-1)**3 + 1):.12f} / {wgt*(b**3)+(1-wgt)*((-1/b)**3):.12f}  (differ => 2N-1 sharp in 1D)")

print("="*80)
print("CX5 — antiphase twins (N=10, +/-0.2 e1 alternating)")
a = 0.2
zplus = np.sqrt(1-a*a)*E7 + a*e[0]; zminus = np.sqrt(1-a*a)*E7 - a*e[0]
ZA5 = np.array([zplus if i%2==0 else zminus for i in range(10)])
ZB5 = np.array([zminus if i%2==0 else zplus for i in range(10)])
_,_,_,VA5,_ = H_parts(ZA5); _,_,_,VB5,_ = H_parts(ZB5)
gap = max(np.abs(A1(VA5)-A1(VB5)).max(), 0.0)
rep("CX5 max|A1A - A1B|", f"{gap:.3e}  (published: 0.000e+00)")
rep("CX5 A1[0,0] A/B", f"{A1(VA5)[0,0]:.6f} / {A1(VB5)[0,0]:.6f}  (published: -0.040000 both)")
rep("CX5 distance", f"{np.linalg.norm(ZA5-ZB5):.6f}  (published: 1.264911 = sqrt(10)*0.4)")

print("="*80)
print("CX6 — mirror pair (generic N=12, seed 3/7 as declared)")
g = np.random.default_rng(3)
Zg = g.normal(size=(12,7)); Zg /= np.linalg.norm(Zg, axis=1, keepdims=True)
Zm = mirror(Zg)
_, rhoA, muA, VA, CA = H_parts(Zg)
_, rhoB, muB, VB, CB = H_parts(Zm)
g46 = max(np.abs(CA-CB).max(), np.abs(A1(VA)-A1(VB)).max())
rep("CX6 rho", f"{rhoA:.6f}  (published: 0.877161 — note: published seed spec '3/7' ambiguous; any generic cloud tests the same claim)")
rep("CX6 max |C,A1 gaps|", f"{g46:.3e}  (published: 1.0e-17)")
rep("CX6 third moment flip", f"{(VA**3).mean(0)[np.argmax(np.abs((VA**3).mean(0)))]:.6f} -> {(VB**3).mean(0)[np.argmax(np.abs((VA**3).mean(0)))]:.6f}")
rep("CX6 distance", f"{np.linalg.norm(Zg - Zm):.6f}  (published: 3.250513 for its generic cloud)")

print("="*80)
print("T4 FALSIFICATION SEARCH — H5 = (H4, M3) on declared families (small N)")
print("Kill: distinct s,s' with H5 gap < 1e-9, s' not in G·s (mirror/cyclic-shift/reversal).")
print("G-check is by construction in each family (documented per family).")

def H5(Z):
    rbar, rho, mu, V, C = H_parts(Z)
    return np.concatenate([mu, [rho], C.ravel(), A1(V).ravel(), M3(V).ravel()])

def h5gap(Za, Zb):
    return np.abs(H5(Za) - H5(Zb)).max()

# Family F1: sign-pattern families on collinear clouds, exhaustive over symmetric sign patterns.
# Construction: multiset fixed, order varied. Order variation is NOT a G-element in general
# (only cyclic shift / reversal are), so equal H5 under other orders = KILL.
import itertools
k = 0.1; mags = np.array([3,3,2,2,1,1])*k
# For collinear clouds v_i = a_i e1: mu, rho, C, M3 depend ONLY on the multiset {a_i};
# A1 depends only on adjacent products sum_{i} a_i a_{i+1} (times e1e1^T/(N-1)).
# So H5(s)=H5(s') is possible only if [multiset equal] AND [adjacent-product sums equal].
# Cross-pattern: M3 differs => no kill possible; verify that claim numerically first.
sigs = sorted({s for s in itertools.product([+1,-1], repeat=6)
               if sum(np.array(s)*mags) == 0})
rep("F1 zero-sum sign patterns found", len(sigs))
m3 = lambda p: (np.array(p)**3).mean()
m3s = [m3(np.array(s)*mags) for s in sigs]
collide_m3 = [(sigs[i], sigs[j]) for i in range(len(sigs))
             for j in range(i+1, len(sigs)) if abs(m3s[i]-m3s[j]) < 1e-12]
rep("F1 distinct-pattern pairs with equal M3", collide_m3 if collide_m3 else "none — every distinct zero-sum pattern pair differs in M3")
# same-multiset orderings: A1 sum of adjacent products; kill iff two orderings of the SAME
# multiset give equal adjacent-product sums but are not related by cyclic shift or reversal.
best_f1 = 1e9; best_pair = None; kills = []
G_class = lambda seq: {tuple(np.roll(seq, r)) for r in range(len(seq))} | \
                     {tuple(np.roll(seq[::-1], r)) for r in range(len(seq))}
for s in sigs:
    base = list(np.array(s)*mags)
    seen = {}   # adjacent-sum -> representative ordering
    for ordn in set(itertools.permutations(base)):
        adj = sum(ordn[i]*ordn[i+1] for i in range(5))
        if adj in seen:
            for rep_ in seen[adj]:
                if tuple(ordn) not in G_class(list(rep_)):
                    kills.append((rep, tuple(ordn), adj))
                    break
            seen[adj].append(tuple(ordn))
        else:
            seen[adj] = [tuple(ordn)]
    adjs = sorted(seen.keys())
    if len(adjs) > 1:
        g_ = min(adjs[i+1]-adjs[i] for i in range(len(adjs)-1))
        if g_ < best_f1: best_f1, best_pair = g_, s
rep("F1 A1-colliding ordering pairs NOT dihedrally related (cyclic/reversal)",
    f"{len(kills)} found; canonical example: {kills[0] if kills else 'none'}")
rep("F1 verdict", "*** KILL of 'fiber = exactly symmetry group' ***" if kills
    else "NO KILL (within search space)")
# full-float verification of the canonical kill pair (the write-up's exhibit):
kill_ex = ((0.3, -0.3, -0.2, -0.1, 0.1, 0.2), (0.1, -0.1, 0.2, 0.3, -0.3, -0.2))
def cl12(ps):
    pts = [np.sqrt(1-x*x)*E7 + x*e[0] for x in ps] + [E7.copy() for _ in range(6)]
    return np.array(pts)
ZA_, ZB_ = cl12(kill_ex[0]), cl12(kill_ex[1])
rep("F1 exhibit H5 gap (full float64, N=12 sequence)", f"{h5gap(ZA_, ZB_):.3e}")
rep("F1 exhibit same multiset? ", f"{sorted(kill_ex[0]) == sorted(kill_ex[1])}")
rep("F1 exhibit dihedrally related? ", f"{kill_ex[1] in G_class(list(kill_ex[0]))}")

# Family F2: phase-shifted clouds — cyclic shifts of a periodic sequence (G-element by
# construction => expected equal, verifying G is in the fiber); NON-multiple shifts of
# an aperiodic sequence (NOT a G-element unless exactly periodic) => kill if equal.
best_f2 = None
for seed in [1,2,3]:
    g_ = np.random.default_rng(seed)
    Z = g_.normal(size=(12,7)); Z /= np.linalg.norm(Z, axis=1, keepdims=True)
    for shift in range(1,12):
        Zs = np.roll(Z, shift, axis=0)
        gap = h5gap(Z, Zs)
        if best_f2 is None or gap < best_f2[0]:
            best_f2 = (gap, seed, shift)
rep("F2 min H5 gap, aperiodic clouds x non-identity rolls", f"{best_f2[0]:.3e} (seed={best_f2[1]}, shift={best_f2[2]})")
rep("F2 verdict", "NO KILL" if best_f2[0] > 1e-9 else "*** KILL ***")
# periodic sequence, shift by period = G-element: confirm equality (sanity, not kill)
g_ = np.random.default_rng(7)
blk = g_.normal(size=(6,7)); blk /= np.linalg.norm(blk, axis=1, keepdims=True)
Zp_ = np.vstack([blk, blk])
rep("F2 sanity: period-6 cloud, roll by 6 (G-element)", f"gap={h5gap(Zp_, np.roll(Zp_,6,axis=0)):.3e} (expected ~0)")

# Family F3: small-amplitude clouds — perturbations at scale eps; look for accidental
# H5 collisions between generic small clouds (dimension says impossible generically;
# kill = any found).
best_f3 = 1e9
for seed in range(20):
    g_ = np.random.default_rng(1000+seed)
    A = g_.normal(size=(10,7)); A /= np.linalg.norm(A,axis=1,keepdims=True)
    B = g_.normal(size=(10,7)); B /= np.linalg.norm(B,axis=1,keepdims=True)
    eps = 0.05
    Za = np.sqrt(1-eps**2)*np.ones((10,7)) + 0  # careful: use E7-based small clouds
    Za = np.array([np.sqrt(1-eps**2)*E7 + eps*a for a in A])
    Zb = np.array([np.sqrt(1-eps**2)*E7 + eps*b for b in B])
    g__ = h5gap(Za, Zb)
    best_f3 = min(best_f3, g__)
rep("F3 min H5 gap, 20 random small-amplitude (eps=0.05) cloud pairs, N=10", f"{best_f3:.6f}")
rep("F3 verdict", "NO KILL" if best_f3 > 1e-9 else "*** KILL ***")

# Family F4: mirror-separated check — H5 must separate mirror pairs (the claim's core).
worst_mir = 0.0
for seed in range(20):
    g_ = np.random.default_rng(2000+seed)
    Z = g_.normal(size=(12,7)); Z /= np.linalg.norm(Z,axis=1,keepdims=True)
    worst_mir = max(worst_mir, h5gap(Z, mirror(Z)))
rep("F4 max H5 gap over 20 random mirror pairs (must be > 0; separation claim)", f"{worst_mir:.6f}")
rep("F4 verdict", "M3 separates mirrors on all sampled" if worst_mir > 1e-6 else "*** separation FAILS somewhere ***")

with open('/tmp/formalization-numerics.txt','w') as f:
    f.write("\n".join(OUT))
print("\n[saved to /tmp/formalization-numerics.txt]")

print("="*80)
print("KILL-#1 CORRECTED VERIFICATION (claude referee, corrected by this lane):")
print("tangent mirror on centrally symmetric multiset {+-w1..+-w6}, eps=0.06, N=12")
def H5v(Z):
    rbar = Z.mean(0); rho = np.linalg.norm(rbar); mu = rbar/rho
    V = Z - np.outer(Z @ mu, mu); C = V.T@V/len(Z)
    A_1 = sum(np.outer(V[i],V[i+1]) for i in range(len(V)-1))/(len(V)-1)
    M_3 = np.einsum('ni,nj,nk->ijk',V,V,V).mean(0)
    return np.concatenate([mu,[rho],C.ravel(),A_1.ravel(),M_3.ravel()])
gaps = []
for seed in range(10):
    g_ = np.random.default_rng(seed)
    W = g_.normal(size=(6,7)); W[:,6] = 0; W /= np.linalg.norm(W,axis=1,keepdims=True)
    devs = np.vstack([W,-W])
    Z = np.array([np.sqrt(1-0.06**2)*E7 + 0.06*d for d in devs])
    Z = Z[np.random.default_rng(100+seed).permutation(12)]
    sig = 2*np.outer(E7,E7) - np.eye(7)
    gaps.append(np.abs(H5v(Z)-H5v(Z @ sig.T)).max())
rep("K1 corrected: max H5 gap, tangent mirror on centrally symmetric clouds", f"{max(gaps):.3e} (kill confirmed if ~1e-18)")
rep("K1 sanity: GLOBAL negation (claude's literal statement) gap", f"{np.abs(H5v(Z)-H5v(-Z)).max():.6f} (separated => the literal form FAILS, correction was required)")
