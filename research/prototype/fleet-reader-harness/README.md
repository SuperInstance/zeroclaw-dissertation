# Fleet-Reader Harness (E3)

The cross-model premise estimate: do distinct real model readers diverge in
their readings of the same real rooms by more than the kill band (0.3–0.6)?
Second, architecturally-independent estimate of the doctrine's premise
(Chapter 7 §7.5; premise context Chapter 6).

- `REGISTRATION-2026-08-19.md` — thresholds, estimator, prompts, roster —
  committed (ffe07c9) BEFORE the field run.
- `extract_corpus.py` → `corpus/corpus.json` — the frozen 27 windows
  (fixture SHA a423a378…), speak texts sha-verified against the elephant logs.
- `prompts.py` — canonical elicitation prompt (P0) + registered paraphrases.
- `elicit.py` — multi-provider runner (gateway :8787 + DeepInfra direct),
  temperature 0, strict-JSON with repair, resume-safe cache.
- `analyze.py` → `results.json` — registered estimator + bootstrap CIs.
- `REPORT-2026-08-19.md` — the field report.

**Result (field, elicited): R = 0.140 [0.111, 0.163] — below band; a miss,
weak evidence per the registered asymmetry (frame artifact not excludable).**
