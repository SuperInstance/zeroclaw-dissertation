#!/usr/bin/env python3
"""
E4 REBOUND — mid-window (day ~1 of 30) corrections-rate check.
Registered metric (registrations/e4-rebound-window.md):
  rate = corrections / forward commits, per repo per day, fleet repos under /home/eileen/projects/
  dormant exclusion: repo with < 5 commits in the measured span is excluded
  threshold: rate > 0.15 => flooding ; <= 0.15 => settling
Correction markers (word-boundary, case-insensitive, on subject line):
  fix/fixes/fixed/fixup, correct/corrections/corrected, revert/reverted,
  address/addressed, bug/bugfix, repair, patch
Spans reported (both honest, both early):
  A) window-to-date: 2026-08-19 00:00 AKDT -> now   (the registered-consistent read; tiny n)
  B) last-7-days context read: 2026-08-13 -> now    ("last several days"; more repos qualify)
LOCAL only. Read-only git. No commits made.
"""
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from random import choices
from zoneinfo import ZoneInfo

AK = ZoneInfo("America/Anchorage")
PROJECTS = Path("/home/eileen/projects")
WINDOW_START = datetime(2026, 8, 19, 0, 0, 0, tzinfo=AK)      # registered window start
CTX_START = datetime(2026, 8, 13, 0, 0, 0, tzinfo=AK)         # 7-day context span
CH6_CORR_DAY_OLD, CH6_CORR_DAY_NEW = 11.6, 20.1               # 11.6 -> 20.1 = +73%
THRESHOLD = 0.15

MARKER = re.compile(
    r"\b(fix|fixes|fixed|fixup|correct|correction|corrections|corrected|"
    r"revert|reverts|reverted|address|addresses|addressed|"
    r"bug|bugs|bugfix|bugfixes|repair|repairs|patch|patches)\b",
    re.IGNORECASE,
)

def fleet_repos():
    out = subprocess.run(
        ["find", str(PROJECTS), "-maxdepth", "2", "-name", ".git", "-type", "d"],
        capture_output=True, text=True, check=True).stdout
    return sorted(Path(l).parent for l in out.splitlines() if l.strip())

def repo_commits(repo):
    """[(epoch_utc, subject)] for commits since CTX_START (fetch enough)."""
    since = CTX_START.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%S")
    r = subprocess.run(
        ["git", "-C", str(repo), "log", f"--since={since}",
         "--no-merges", "--pretty=format:%at%x09%s"],
        capture_output=True, text=True)
    commits = []
    for line in r.stdout.splitlines():
        if "\t" not in line:
            continue
        ts, subj = line.split("\t", 1)
        try:
            commits.append((int(ts), subj))
        except ValueError:
            continue
    return commits

def classify(subj):
    return 1 if MARKER.search(subj) else 0  # 1 = correction, 0 = forward

def bucket(commits, start):
    """repo-day cells + totals for commits at/after start."""
    perday = defaultdict(lambda: [0, 0])  # date -> [corr, fwd]
    for ts, subj in commits:
        when = datetime.fromtimestamp(ts, tz=AK)
        if when < start:
            continue
        d = when.date()
        is_corr = classify(subj)
        perday[d][0 if is_corr else 1] += 1  # slot0=corrections, slot1=forward
    corr = sum(c for c, f in perday.values())
    fwd = sum(f for c, f in perday.values())
    return perday, corr, fwd

def bootstrap_ci(cells, n=5000, seed=42):
    """cells = list of [corr, fwd]; resample cells with replacement; CI of pooled rate."""
    rng = __import__("random").Random(seed)
    if not cells:
        return (float("nan"),) * 2
    rates = []
    for _ in range(n):
        s = rng.choices(cells, k=len(cells))
        c = sum(x[0] for x in s); f = sum(x[1] for x in s)
        if c + f > 0:
            rates.append(c / (c + f))
    if not rates:
        return (float("nan"),) * 2
    rates.sort()
    return rates[int(0.025 * len(rates))], rates[int(0.975 * len(rates))]

def report(label, start, repos_commits):
    days_elapsed = (datetime.now(AK) - start).total_seconds() / 86400.0
    active, cells, tot_c, tot_f, dayset = [], [], 0, 0, set()
    dormant = 0
    for repo, commits in repos_commits.items():
        perday, c, f = bucket(commits, start)
        n = c + f
        if n < 5:  # registered dormant exclusion
            if n > 0:
                dormant += 1
            continue
        rate = c / f if f else float("inf")
        active.append((repo.name, n, c, f, rate))
        for d, (cc, ff) in perday.items():
            cells.append([cc, ff])
            dayset.add(d)
        tot_c += c; tot_f += f
    print(f"\n{'='*72}\n{label}\nspan: {start:%Y-%m-%d %H:%M} AKDT -> now "
          f"({days_elapsed:.1f} days elapsed)\n{'='*72}")
    print(f"active (>=5 commits): {len(active)} repos   dormant-excluded: {dormant} repos with <5")
    if active:
        print(f"\n{'repo':38} {'n':>5} {'corr':>5} {'fwd':>5} {'rate':>7}")
        for name, n, c, f, r in sorted(active, key=lambda x: -x[4]):
            rs = f"{r:.3f}" if r != float("inf") else "inf"
            flag = "  <-- flooding" if r > THRESHOLD else ""
            print(f"{name:38} {n:5d} {c:5d} {f:5d} {rs:>7}{flag}")
        fleet_rate = tot_c / tot_f if tot_f else float("nan")
        ndays = max(len(dayset), 1)
        corr_day = tot_c / max(days_elapsed, 1e-9)
        lo, hi = bootstrap_ci(cells)
        print(f"\nFLEET POOLED RATE  = {tot_c} corrections / {tot_f} forward = {fleet_rate:.4f}")
        print(f"bootstrap 95% CI (repo-day cells, n={len(cells)}): [{lo:.3f}, {hi:.3f}]  (indicative only mid-window)")
        print(f"corrections/day    = {corr_day:.1f}  (Ch6 baselines: 11.6 old -> 20.1 new [+73%])")
        return fleet_rate, corr_day
    print("no active repos (all dormant at <5 commits)")
    return None, None

def main():
    print(f"E4 REBOUND mid-window check — {datetime.now(AK):%Y-%m-%d %H:%M} AKDT")
    print(f"window day ~1 of 30 (start 2026-08-19). EARLY READ, not the window-end verdict.")
    repos = fleet_repos()
    print(f"fleet repos scanned: {len(repos)}")
    rc = {}
    for repo in repos:
        c = repo_commits(repo)
        if c:
            rc[repo] = c
    r_a, cd_a = report("[A] WINDOW-TO-DATE (registered-consistent, day ~1)", WINDOW_START, rc)
    r_b, cd_b = report("[B] LAST-7-DAYS CONTEXT READ", CTX_START, rc)

    print(f"\n{'='*72}\nVERDICT (EARLY, day ~1 of 30 — n is tiny; nothing is settled)\n{'='*72}")
    for lbl, r in (("[A] window-to-date", r_a), ("[B] 7-day context", r_b)):
        if r is None:
            print(f"{lbl}: insufficient active repos"); continue
        v = "FLOODING (>0.15)" if r > THRESHOLD else "SETTLING (<=0.15)"
        print(f"{lbl}: rate {r:.4f} -> {v}")
    if cd_a is not None:
        vs20 = (cd_a - CH6_CORR_DAY_NEW) / CH6_CORR_DAY_NEW * 100
        print(f"corrections/day {cd_a:.1f} vs Ch6 endpoint 20.1: {vs20:+.0f}% "
              f"({'above' if cd_a > CH6_CORR_DAY_NEW else 'at/below'} the +73% trajectory)")

if __name__ == "__main__":
    main()
