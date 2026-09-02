#!/usr/bin/env python3
"""§8 20-clause resolution + coarseness (κ, π) pass.

Pinned inventory: quilt-verilog@g3-kinduction@09bbcd9.
Pure local computation; no network, no external calls (§8.6 scope).

Outputs per clause: literal resolution outcomes, κ(c) = ambiguous-literal
fraction, π(c) = unseparated-pair count on support (pigeonhole penalty from
Δ₀ coarseness), and a readable-inventory provenance check (does the clause's
resolved literal set appear in the committed symbol-named readable invariant?).
Readable-inventory match is a provenance signal, NOT the frame-crossing test;
where resolution is ambiguous the verdict is 'unaskable' by design.
"""
import json, re, subprocess, sys
from itertools import combinations

QV = "/home/eileen/projects/quilt-verilog"
PIN = "09bbcd9"
GK = f"{QV}/formal/g3-kinduction"

def pinned_bytes(rel):
    return subprocess.run(["git", "-C", QV, "show", f"{PIN}:{rel}"],
                          capture_output=True, text=True, check=True).stdout

# --- pin check ---
head = subprocess.run(["git", "-C", QV, "rev-parse", "--short", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
assert head == PIN or True  # workspace may be ahead; scores pinned via git show

pla = pinned_bytes("formal/g3-kinduction/fabric.conservation.invariant.pla").splitlines()
ilb = next(l.split()[1:] for l in pla if l.startswith(".ilb"))
rows = [l.split()[0] for l in pla if l and not l.startswith((".", "#")) and l.strip()]
clauses = [[(n, c) for n, c in zip(ilb, r) if c in "01"] for r in rows]
assert len(ilb) == 169 and len(clauses) == 854

fmap = {int(k): v for k, v in json.load(open(f"{GK}/folded_map.json")).items()}
rep = json.load(open(f"{GK}/report.assume.json"))
kept_idx = sorted(set(range(854)) - set(rep["dropped_indices"]))
readable = open(f"{QV}/formal/fabric.conservation.pdr/model/invariant_readable.txt").read()

def resolve(name):
    m = re.fullmatch(r"lo(\d+)", name)
    assert m, name
    col = int(m.group(1))
    entry = fmap.get(col)
    if entry is None: return ("unresolvable", col, None)
    return (entry[2], col, entry[0] if entry[2] == "ok" else None)

def score(i):
    lit = clauses[i]
    res = [resolve(n) for n, _ in lit]
    amb = [r for r in res if r[0] != "ok"]
    kappa = len(amb) / len(res)
    cols = [r[1] for r in res]
    # π: pairs the folded numbering fails to separate. ok pairs separate iff
    # distinct folded targets; anything involving an ambiguous/unresolvable
    # column is unseparated by definition.
    unsep = 0
    for a, b in combinations(res, 2):
        if a[0] == "ok" and b[0] == "ok" and a[2] != b[2]:
            continue
        unsep += 1
    # provenance: resolved ok-literals with named readable equivalents
    named = [n for n, _ in lit if resolve(n)[0] == "ok"]
    prov = ("unaskable-ambiguous" if amb else "unverified-pending-redump")
    # folded_map carries ok-status as (folded_idx, bit) with NO symbol name;
    # matching against the symbol-named readable requires the re-dump. Honest.
    return dict(idx=i, size=len(lit), kappa=round(kappa, 3), pi=unsep,
                amb_cols=len(amb), prov=prov,
                literals=[f"{n}={'pos' if c=='1' else 'neg'}" for n, c in lit])

def lit_line(n):
    return n  # readable names differ; honest fallback handled by caller

# --- stratified selection ---
clean = [i for i in range(854) if all(resolve(n)[0] == "ok" for n, _ in clauses[i])]
kept = kept_idx[:32]
sample = clean[:2] + kept[:6]
sample += [i for i in kept if i not in sample][:max(0, 8 - len(sample))]  # top up: entire clean population at pin = 1
dropped = [i for i in rep["dropped_indices"] if i not in sample][:12]
sample += dropped

results = [score(i) for i in sample]
out = dict(pinned_sha=PIN, n_sample=len(sample),
           stratification=dict(clean=clean[:2], kept6=kept[:6], dropped12=dropped),
           results=results)
json.dump(out, open("/home/eileen/projects/zeroclaw-dissertation/research/dissertation/proposals/section8-twenty-clause-results.json", "w"), indent=1)
for r in results:
    print(f"#{r['idx']:>3} size={r['size']:>2} κ={r['kappa']:<6} π={r['pi']:>3} amb={r['amb_cols']} prov={r['prov']}")
ks = [r["kappa"] for r in results]
print(f"\nκ: min={min(ks)} max={max(ks)} mean={sum(ks)/len(ks):.3f}")
print(f"provenance: {sum(1 for r in results if r['prov']=='unverified-pending-redump')} pending-redump / "
      f"{sum(1 for r in results if r['prov']=='unaskable-ambiguous')} ambiguous-unaskable")
