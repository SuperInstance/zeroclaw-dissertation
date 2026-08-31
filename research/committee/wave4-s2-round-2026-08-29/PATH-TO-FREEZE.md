# PATH-TO-FREEZE — wave-4 S2 (2026-08-30, EXPERT nudge ACCEPTED)

**Purpose:** make freeze execution mechanical. Three sections: certificate
template, pilot re-certification inventory, execution recipe. Written so
"the freeze is executable the hour the certificate exists."

**Non-gating note:** DeepSeek cross-read is 402-blocked (Casey's top-up
pending). It does NOT gate this path — §6/§7 derive from committee response
docs, not derivations. DeepSeek is slotted as confirmation-only when the
key returns.

---

## §1. §5.4 Power Certificate — LITERAL TEMPLATE (every field blank)

File as `POWER-CERTIFICATE-S2-2026-<MMDD>.md` in this directory. Every
`<BLANK>` must resolve before the file counts:

```markdown
# WAVE-4 S2 POWER CERTIFICATE (§5.4)
Certificate date: <BLANK: YYYY-MM-DD>
Code SHA (commit executing the certification): <BLANK: 40-hex>
Attempt number: <BLANK: n of N> — N = 3, PRE-REGISTERED here. Identical-
  design re-runs count against N; any FAIL after attempt 1 requires a
  documented design change or cause analysis in the attempt log BEFORE
  attempt n+1. Exhausting N without PASS = certificate unavailable; design
  returns to S1v4b hardening (§1.2c). This bounds the multiple-testing
  channel: fresh scratch seeds per run otherwise let a marginally-failing
  design pass by seed luck (the wobble-laundering shape, re-closed).
Corpus/version certified against: fiber v4b spec, blob <BLANK: 40-hex of
  METHODOLOGIST-S2-FREEZE-DRAFT.md>
Seed discipline: scratch seeds derived from <BLANK: root seed>, throwaway,
  NEVER the registered master seed 20260829. Seed list: <BLANK: enumeration>
Run command (exact, reproducible): <BLANK: command line>
n replicates per contrast: 500 pairs (§5.4)

Results (§5.4 defines FOUR pass conditions — the template's row 1 covers
both contrasts as §5.4 states them; four rows total, canonical = §5.4):
(1) P-test rejection: ≥0.90 at Δα=1 AND ≥0.80 at Δα=0.25: <BLANK: both values>  PASS/FAIL
(2) false-positive rate on α-identical pairs ≤0.05: <BLANK: value>  PASS/FAIL
(3) A-gap envelope exceedance ≤0.01:                <BLANK: value>  PASS/FAIL
(4) V-leg separation ≥0.95 at Δα=0.25:              <BLANK: value>  PASS/FAIL

Verdict: PASS → proceed to freeze execution recipe (§3 below).
         FAIL → return design to S1v4b hardening (§1.2c). No waiver.

## Correction log
- 2026-08-30 (DEVIL nudge, cb79fe0-successor): (a) row count fixed —
  template showed five rows where §5.4 defines four conditions (P-test at
  both contrasts is ONE condition); canonicality = §5.4, template now
  matches. (b) Attempt budget N=3 pre-registered with cause-analysis rule;
  'no waiver' previously left the seed-shopping channel open.
```

**Closing artifact = the committed certificate file with zero remaining
`<BLANK>` strings and all rows PASS.**

---

## §2. v4b Pilot Inventory & Re-certification Procedure

**What exists now (honest inventory):**
- §1 carrier-sd figure (≈0.14 anchor units) — certified on unsealed pilots
  per the draft, but the pilot run artifacts (seeds, SHAs, outputs) are NOT
  linked from the draft. **This is a phrase, not a procedure — exactly the
  phantom class.** Fill-in needed: locate or re-run the S1v4b sweep that
  produced the wobble-sd floor (≥0.29·corpus_sd) and decorrelation ceiling;
  cite its seed + SHA here:
  - S1v4b sweep run: <BLANK: seed / SHA / output path, or "must re-run">
- §5.3 scatter inputs (P_trans family sd ≈0.01, ICC sd ≈0.04) come from
  wave-3 corpora — dated and registered, considered reachable.

**What "re-certification on unsealed v4b pilots" concretely means:**
1. RE-RUN (not re-sign): the §5.4 protocol of 500 replicate pairs on
   throwaway seeds, using the frozen §1 carrier spec, executed from the
   commit named in §1's Code SHA field. Prior pilot numbers are inputs to
   power claims only; the certificate requires fresh execution.
2. The §1 design subgates (norm-flatness in α, carrier-purity envelope
   0.085, logged-target verification) are re-checked on the same runs.
3. Sign-off = the certificate commit itself. No separate signature exists.

**Definition of done for this section:** the two `<BLANK>`s above resolve
(or the runs are executed and logged), and §1's template is filled from
those runs.

---

## §3. Freeze-Execution Recipe (single commit, in order)

1. Confirm §1 certificate committed, zero `<BLANK>`s, all PASS.
2. Re-verify blob list: `git ls-tree <commit> -- research/committee/wave4-s2-round-2026-08-29/`
   — if any of the 9 blobs differ from FREEZE-AUDIT-DEVIL-2026-08-30.md,
   update that file's list first (the fingerprint must match reality at
   freeze time).
3. Adjudication status line: one line stating cross-read status
   (DONE + pointer, or PENDING + reason). Either is acceptable; absence is not.
4. Execute ONE commit that:
   - adds the done-condition sentence to the freeze draft header — written
     for the FIRST time here: "Power certified. Void rules locked. S2
     freeze approved." — citing the certificate file,
   - cites the verified blob list,
   - carries the adjudication status line.
   Commit message: `S2 FREEZE EXECUTED — certificate <file>, blobs verified
   at <commit>, adjudication <status>`. No other changes in that commit.
5. Only after that commit may S3-GOVERNANCE-PRIMER's dependency table be
   re-derived against the freeze hash (existing Item 7 obligation), and S3
   generation unblocks.

**Estimated critical path:** the §5.4 certification run itself. Everything
else is fill-in measurable in minutes.
