#!/usr/bin/env python3
"""fiber-duality-verify.py — numeric + exact checks for FIBER-DUALITY.md (lane fiber-duality).

Sections (mirroring the doc):
  OB-K2  : the rotation-orbit isotypic construction, decided by an exhaustive exact
           search (scripts/obk2_search.c, compiled and run by this driver):
             planar : 1 condition  SUM_edges omega^(a+b) = 0   (pair (+1,-1))
             full   : 30 conditions SUM_edges omega^(s*a-t*b) = 0 for s != t in {+-1,+-2,+-3}
           + exact Z[omega] count-vector enumeration for the planar condition
           (validates the Lam-Leung/Schoenberg structure computationally at length 11),
           + statistical spot-check on random orderings (min isotypic residue),
           + if a witness exists: full float64 H5 verification of the collision.
  F1-REG : regression — canonical T4b exhibit (4,888-pair family) H5 gap ~ 3.469e-18,
           confirming the H5 machinery here matches FORMALIZATION.md's.

All subprocess calls use list-form argv (no shell). Raw output captured to
scripts/fiber-duality-numerics-raw.txt by the caller (or printed to stdout).
"""
import subprocess
import sys
import os
import itertools
import random

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Z[omega] exact
PHI_COEFFS = {  # omega^k as (c0,c1,c2,c3) in basis 1,w,w^2,w^3 ; Phi_12 = x^4-x^2+1
    0: (1,0,0,0), 1: (0,1,0,0), 2: (0,0,1,0), 3: (0,0,0,1),
    4: (-1,0,1,0), 5: (0,-1,0,1), 6: (-1,0,0,0), 7: (0,-1,0,0),
    8: (0,0,-1,0), 9: (0,0,0,-1), 10: (1,0,-1,0), 11: (0,1,0,-1),
}

def omega_val():
    return np.exp(1j*np.pi/6)

def count_vectors_vanishing(total=11, n=12):
    """All m: Z_{>=0}^12, sum(m)=total, sum_k m[k] omega^k == 0 in Z[omega]. Exact."""
    out = []
    m = [0]*n
    def rec(k, left, acc):
        if k == n:
            if left == 0 and acc[0]==0 and acc[1]==0 and acc[2]==0 and acc[3]==0:
                out.append(tuple(m))
            return
        for take in range(left+1):
            m[k] = take
            base = PHI_COEFFS[k % 12]
            rec(k+1, left-take,
                (acc[0]+take*base[0], acc[1]+take*base[1],
                 acc[2]+take*base[2], acc[3]+take*base[3]))
        m[k] = 0
    rec(0, total, (0,0,0,0))
    return out

def decomposes(m):
    """Can m be written as a nonneg integer combination of rotations of the 2-term
    relation {r, r+6} and the 3-term relation {r, r+4, r+8}? (Schoenberg structure for
    n=12.) Small ILP by DFS — length-11 vectors only."""
    m = list(m)
    n_pairs = (11 - 3) // 2  # max plausible
    rels = []
    for r in range(12):
        v = [0]*12; v[r] += 1; v[(r+6) % 12] += 1
        rels.append(tuple(v))
        v = [0]*12; v[r] += 1; v[(r+4) % 12] += 1; v[(r+8) % 12] += 1
        rels.append(tuple(v))
    idx = list(range(len(rels)))
    def dfs(i, rem):
        if all(x == 0 for x in rem):
            return True
        if i >= len(rels):
            return False
        # bound: remaining sum must be even mix of 2s and 3s — just try counts
        rel = rels[i]
        s = sum(rel)
        maxtake = min(rem[j]//rel[j] for j in range(12) if rel[j]) if any(rel) else 0
        for take in range(maxtake, -1, -1):
            nrem = [rem[j]-take*rel[j] for j in range(12)]
            if any(x < 0 for x in nrem):
                continue
            if dfs(i+1, nrem):
                return True
        return False
    return dfs(0, m)

# ---------------------------------------------------------------- H5 machinery
def moments(Z):
    """(mu_hat, rho, C, A1, M3) for window matrix Z (N x 7, unit rows)."""
    N = Z.shape[0]
    rbar = Z.mean(axis=0)
    rho = np.linalg.norm(rbar)
    mu = rbar/rho
    V = Z - np.outer(Z@mu, mu)
    C = (V.T@V)/N
    A1 = sum(np.outer(V[i], V[i+1]) for i in range(N-1))/(N-1)
    def M3_tensor(V):
        T = np.zeros((7,7,7))
        Nv = V.shape[0]
        for i in range(Nv):
            T += np.einsum('i,j,k->ijk', V[i], V[i], V[i])
        return T/Nv
    return mu, rho, C, A1, M3_tensor(V)

def H5_vector(Z):
    mu, rho, C, A1, M3 = moments(Z)
    return np.concatenate([mu, [rho], C.flatten(), A1.flatten(), M3.flatten()])

def gap(u, v):
    return float(np.max(np.abs(u - v)))

# ---------------------------------------------------------------- sections
def sec_obk2(verbose=True):
    print("== OB-K2: rotation-orbit isotypic construction ==")
    # 1) exact count-vector feasibility for the planar condition
    cvs = count_vectors_vanishing(11)
    print(f"[planar] vanishing count vectors (len 11): {len(cvs)}")
    bad = [m for m in cvs if not decomposes(m)]
    print(f"[planar] of these, NOT decomposable into rotated {{r,r+6}} + {{r,r+4,r+8}} sums: {len(bad)}"
          + ("  <-- Schoenberg structure VIOLATED at length 11 (finding!)" if bad else "  (Schoenberg structure confirmed computationally)"))
    # 2) exhaustive exact search, both modes
    exe = os.path.join(HERE, "obk2_search")
    if not os.path.exists(exe):
        print("[build] compiling obk2_search.c ...")
        r = subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(HERE, "obk2_search.c"), "-lm"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("gcc failed:", r.stderr); sys.exit(1)
    for mode in ["planar", "full"]:
        print(f"[search] mode={mode} ...", flush=True)
        r = subprocess.run([exe, mode], capture_output=True, text=True)
        print(r.stdout.strip())
        if "first_witness_g" in r.stdout:
            gw = [int(x) for x in r.stdout.split("first_witness_g:")[1].split()]
            verify_witness_numeric(gw, mode, verbose=True)
        else:
            print(f"[{mode}] NO witness: the isotypic attack cannot land (exhaustive, exact).")
    # 3) statistical spot-check (sanity that the exact machinery isn't vacuous):
    # random orderings, min over samples of max |isotypic residue| for the full condition
    rng = random.Random(7)
    sig = [1,-1,2,-2,3,-3]
    w = omega_val()
    best = None
    for _ in range(200000):
        g = list(range(12)); rng.shuffle(g)
        mx = 0.0
        for sp in sig:
            for sq in sig:
                if sp == sq: continue
                s = sum(w**(((sp*g[i]-sq*g[i+1]) % 12)) for i in range(11))
                mx = max(mx, abs(s))
        if best is None or mx < best:
            best = mx
    print(f"[stat] 200k random orderings: min over samples of max|isotypic residue| = {best:.6f} (unit scale 11)")

def verify_witness_numeric(gw, mode, verbose=True):
    """If a witness ordering exists, build the matching cloud and verify the H5 collision.
    planar mode: orbit under a SINGLE R^2 rotation (angles 2pi/12) — deviations in one 2-plane.
    full mode: orbit under block-diag R with angles (1,2,3)*2pi/12."""
    print(f"[verify] building orbit cloud for witness g={gw} (mode={mode})")
    th = lambda j: (2*np.pi/12)*j
    if mode == "planar":
        Rp = np.array([[np.cos(th(1)), -np.sin(th(1))], [np.sin(th(1)), np.cos(th(1))]])
        R = np.zeros((6,6)); R[0:2,0:2] = Rp  # single block: deviations in span(e1,e2)
    else:
        R = np.zeros((6,6))
        for b,j in enumerate((1,2,3)):
            R[2*b:2*b+2, 2*b:2*b+2] = np.array([[np.cos(th(j)), -np.sin(th(j))], [np.sin(th(j)), np.cos(th(j))]])
    rng = np.random.default_rng(42)
    wv = rng.normal(size=6)
    if mode == "planar":
        wv = np.zeros(6); wv[0], wv[1] = rng.normal(size=2)  # generic PLANAR seed
    wv /= np.linalg.norm(wv)
    scale = 0.3
    N = 12
    axial = np.sqrt(1 - scale**2)
    def cloud(order):
        Z = np.zeros((N,7))
        for i,k in enumerate(order):
            Z[i,:6] = scale * (np.linalg.matrix_power(R, k) @ wv)
            Z[i,6] = axial
        return Z
    Zg = cloud(gw)
    Zg1 = cloud([(k+1) % 12 for k in gw])   # rotation relabel g+1
    g5 = gap(H5_vector(Zg), H5_vector(Zg1))
    d = float(np.linalg.norm(Zg - Zg1))
    # M3 norm (mirror-degeneracy diagnostic: planar orbit is centrally symmetric => M3 = 0)
    _,_,_,_,M3 = moments(Zg)
    m3n = float(np.linalg.norm(M3))
    # dihedral relatedness of the two ORDERINGS: sequence rotations + reversal ONLY
    # (declared room equivalences). NOTE: an index-shift (x+s) is an R^s-RELABEL — the
    # family under test — and must NOT count as dihedral (first implementation bug,
    # caught and corrected: the check must be on sequence positions, not labels).
    def dihedral_related(a, b):
        a, b = list(a), list(b)
        for s in range(len(a)):
            rot = b[s:] + b[:s]
            if rot == a or rot[::-1] == a:
                return True
        return False
    dr = dihedral_related(gw, [(k+1) % 12 for k in gw])
    print(f"[verify] H5(g) vs H5(g+1): max component gap = {g5:.3e}; ||Z_g - Z_(g+1)||_F = {d:.6f}")
    print(f"[verify] ||M3|| = {m3n:.3e} ({'centrally symmetric / mirror-degenerate stratum' if m3n < 1e-12 else 'M3 != 0 stratum'})")
    print(f"[verify] g vs g+1 dihedrally related: {dr}")
    print(f"[verify] collision {'CONFIRMED' if g5 < 1e-12 else 'NOT CONFIRMED (gap too large)'}")

def sec_f1_regression(verbose=True):
    print("== F1 regression: canonical T4b exhibit (ordering phantom) ==")
    mu = np.zeros(7); mu[6] = 1.0
    A = [0.3,-0.3,-0.2,-0.1,0.1,0.2]
    B = [0.1,-0.1,0.2,0.3,-0.3,-0.2]
    def cloud(xs):
        Z = np.zeros((12,7))
        for i,x in enumerate(xs[:6]):
            Z[i,0] = x; Z[i,6] = np.sqrt(1-x*x)
        for i in range(6,12):
            Z[i,6] = 1.0
        return Z
    ZA, ZB = cloud(A), cloud(B)
    g5 = gap(H5_vector(ZA), H5_vector(ZB))
    print(f"[F1] H5 gap A vs B = {g5:.3e}  (FORMALIZATION.md reports 3.469e-18)")
    print(f"[F1] {'regression OK' if g5 < 1e-15 else 'MISMATCH — investigate'}")

def main():
    print("fiber-duality-verify.py — OB-K2 + regressions")
    sec_obk2()
    print()
    sec_f1_regression()

if __name__ == "__main__":
    main()
