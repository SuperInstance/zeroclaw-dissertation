// Polyformal vMF kernel — JavaScript port (Node.js, stdlib only).
//
// Implements the three functions of SPEC.md:
//   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
//   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
//   edge      — field step between two fits
//
// No numpy/scipy, no external vMF/Bessel libraries — pure Math.sinh/cosh + Newton.
// Differential test: test.js (reads ../golden.json + ../inputs.json).
//
// Run:  node test.js

'use strict';

const D = 7;                 // dimension of the field space (S^6 ⊂ R^7)
const KMAX = 500.0;          // κ saturation cap
const NMIN = 10;             // below this many windows, κ is not identifiable
const RHOMAX = 0.999;        // ρ clamp (unclipped Banerjee init overflows sinh)

// ---------- SPEC §1: A7 ----------
function a7(k) {
  // Leading Taylor term: the closed form catastrophically cancels for small κ.
  if (k < 0.5) return k / 7.0;
  const s = Math.sinh(k);
  const c = Math.cosh(k);
  const k2 = k * k;
  return (
    ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s) /
    ((1.0 + 3.0 / k2) * s - (3.0 / k) * c)
  );
}

function clip(x, lo, hi) {
  return Math.min(Math.max(x, lo), hi);
}

function norm(v) {
  let s = 0.0;
  for (const x of v) s += x * x;
  return Math.sqrt(s);
}

// ---------- SPEC §2: vmf_fit ----------
// zs: array of n 7-vectors; warm: the fixed 7-vector WARM from golden.json.
// Returns a fit object, or null when unidentifiable/isotropic — never a fake number.
function vmfFit(zs, warm) {
  const n = zs.length;
  if (n < NMIN) return null;

  // 2. defensive renormalization (inputs should already be unit)
  const rows = zs.map((row) => {
    const nr = norm(row);
    return row.map((x) => x / nr);
  });

  // 3. mean resultant
  const r = new Array(D).fill(0.0);
  for (const row of rows) {
    for (let j = 0; j < D; j++) r[j] += row[j] / n;
  }
  const rho = Math.min(norm(r), RHOMAX);
  if (rho < 1e-12) return null; // isotropic — no mean direction

  // 4. mean direction
  const muHat = r.map((x) => x / rho);

  // 5. Banerjee et al. init, clipped to [1e-6, KMAX]
  let kappa = clip((rho * (D - rho * rho)) / (1.0 - rho * rho), 1e-6, KMAX);

  // 6. Newton solve on A7(kappa) = rho, with g = 1 - A7² - (D-1)·A7/κ
  for (let it = 0; it < 60; it++) {
    const a = a7(kappa);
    const g = 1.0 - a * a - ((D - 1) * a) / kappa;
    const step = (a - rho) / g;
    kappa = clip(kappa - step, 1e-6, KMAX);
    if (Math.abs(g) < 1e-12 || Math.abs(step) < 1e-9) break;
  }

  // 7. warmth = WARM · μ̂
  let warmth = 0.0;
  for (let j = 0; j < D; j++) warmth += warm[j] * muHat[j];

  // 8. jackknife SE(μ̂): leave-one-out mean directions, renormalized
  const jks = [];
  for (let i = 0; i < n; i++) {
    const m = new Array(D).fill(0.0);
    for (let j = 0; j < n; j++) {
      if (j === i) continue;
      for (let d = 0; d < D; d++) m[d] += rows[j][d] / (n - 1);
    }
    const nm = norm(m);
    jks.push(m.map((x) => x / nm));
  }
  const jm = new Array(D).fill(0.0);
  for (const jk of jks) {
    for (let d = 0; d < D; d++) jm[d] += jk[d] / n;
  }
  let acc = 0.0;
  for (const jk of jks) {
    for (let d = 0; d < D; d++) {
      const diff = jk[d] - jm[d];
      acc += diff * diff;
    }
  }
  const muSe = Math.sqrt(((n - 1) / n) * acc);

  // 9. saturation flag
  const saturated = rho >= RHOMAX || kappa >= KMAX;

  return { mu_hat: muHat, kappa, rho, n, warmth_vmf: warmth, mu_se: muSe, saturated };
}

// ---------- SPEC §3: edge ----------
function edge(fb, fa) {
  const diff = new Array(D).fill(0.0);
  for (let j = 0; j < D; j++) diff[j] = fa.mu_hat[j] - fb.mu_hat[j];
  const dMu = norm(diff);
  const dWarmth = fa.warmth_vmf - fb.warmth_vmf;
  const dLogKappa = Math.log(fa.kappa / fb.kappa);
  // db_factor = 2.0 — the drift deadband
  const real = dMu > 2.0 * Math.max(fb.mu_se, fa.mu_se);
  return { d_mu: dMu, d_warmth: dWarmth, d_log_kappa: dLogKappa, real };
}

module.exports = { a7, vmfFit, edge, D, KMAX, NMIN, RHOMAX };
