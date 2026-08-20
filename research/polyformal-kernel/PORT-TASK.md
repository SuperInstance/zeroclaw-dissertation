# Polyformal Kernel — Port Task

Read these files first (they are the ground truth):
- `SPEC.md` — the language-agnostic math spec (A7, vmf_fit, edge, tolerances)
- `golden.json` — golden test vectors from the audited Python reference (`elephant/vmf.py`)
- `inputs.json` — the deterministic 30×7 z-vector input matrix

## Your job

Port the vMF kernel (three functions: `A7`, `vmf_fit`, `edge`) to YOUR assigned languages. For each language:

1. Create `research/polyformal-kernel/<lang>/` with:
   - one implementation file (idiomatic to that language, no numpy/scipy — the kernel is closed-form sinh/cosh + Newton, so stdlib math only)
   - one differential test that reads `../golden.json` + `../inputs.json` and asserts the SPEC §4 tolerances (A7 ≤1e-9; fit values ≤1e-6; edge ≤1e-6; n==30; saturated==false; real==false)
2. Run the test for every language. Every language must PASS within tolerance.
3. If a language has no trivial JSON parser, hardcode the golden vectors into the test as literals — but note that in a comment.
4. Report: for each language, PASS/FAIL, and the actual vs golden kappa/rho/warmth to 6 decimals.

The languages are assigned in the command prompt. Write everything under `research/polyformal-kernel/` in the repo `/home/eileen/projects/zeroclaw-dissertation`. Commit and push when done.

The point: prove the dissertation's measurement is essential (language-independent), not accidental to Python/numpy — the polyformalism move applied to the dissertation's own math.
