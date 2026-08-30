# RIVAL Objections — Response Status

**Created:** 2026-08-30 (post-committee analysis)  
**Status:** All RIVAL objections have been addressed through design modifications or specifications

## Response Summary

All three RIVAL vulnerabilities have been addressed:

### V1: Mid-α amplitude confound → RESOLVED
- **Original claim:** Amplitude design confounded gradient measurement at mid-α
- **Response:** Adopted direction-only amplitude matching (rejecting raw-amplitude option)
- **Implementation:** Carrier specified as `room_carrier(t) = FIELD_ANCHOR_NORM · w_ar(t) / ‖w_ar(t)‖`
- **Subgate added:** Scale floor + decorrelation ceiling jointly control carrier behavior

### V2: Parity v2 is a tautology → ADDRESSED
- **Original claim:** Logging `target_R(t)` makes replay an arithmetic identity
- **Response:** Added two kill conditions to parity registration
- **Kill conditions:**
  1. Independent seeded-stream re-derivation must match logged target bit-for-bit
  2. Bit-identity assertion `v4(α=0) ≡ v3` on pinned corpus
- **Status:** Conditions documented for implementation before parity registration

### V3: κ(t)-gated wobble laundering → ADDRESSED
- **Original claim:** Content-modulated carrier rotation through κ(t) can manufacture results
- **Response:** Added κ-neutrality subgate + ICC calibration clause
- **Subgate:** α=1 pilot with frozen κ(t) must still fire P_trans < 0.5×P_rest
- **Calibration:** S1 ICC threshold calibrated against v3-style static-common-target control
- **Status:** Laundering channel detected, kill conditions documented

## Integration Status
- V1 resolved through design specification (already implemented in freeze draft)
- V2 and V3 addressed through documented kill conditions to be implemented before registration
- No unresolved RIVAL objections remain