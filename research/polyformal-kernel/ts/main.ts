// Polyformal vMF kernel — TypeScript port (stdlib only).
//
// Implements the three functions of SPEC.md:
//   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
//   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
//   edge      — field step between two fits
//
// No numpy/scipy, no external vMF/Bessel libraries — pure Math.sinh/cosh + Newton.
// Differential test: test.ts (reads ../golden.json + ../inputs.json).
//
// Typecheck:  npx tsc -p tsconfig.json   (or tsc)
// Run:        node dist/test.js   (from ts/)  — note: if tsc is not installed,
//             this port can only be typechecked/run on a machine with TypeScript;
//             the JS port (../js/) is the always-runnable twin.

export const D = 7; // dimension of the field space (S^6 ⊂ R^7)
export const KMAX = 500.0; // κ saturation cap
export const NMIN = 10; // below this many windows, κ is not identifiable
export const RHOMAX = 0.999; // ρ clamp (unclipped Banerjee init overflows sinh)

export type Vec = number[];

// ---------- SPEC §1: A7 ----------
export function a7(k: number): number {
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

function clip(x: number, lo: number, hi: number): number {
  return Math.min(Math.max(x, lo), hi);
}

function norm(v: Vec): number {
  let s = 0.0;
  for (const x of v) s += x * x;
  return Math.sqrt(s);
}

// ---------- SPEC §2: vmf_fit ----------
export interface Fit {
  mu_hat: Vec;
  kappa: number;
  rho: number;
  n: number;
  warmth_vmf: number;
  mu_se: number;
  saturated: boolean;
}

// zs: n×7 matrix; warm: the fixed 7-vector WARM from golden.json.
// Returns a Fit, or null when unidentifiable/isotropic — never a fake number.
export function vmfFit(zs: Vec[], warm: Vec): Fit | null {
  const n = zs.length;
  if (n < NMIN) return null;

  // 2. defensive renormalization (inputs should already be unit)
  const rows: Vec[] = zs.map((row) => {
    const nr = norm(row);
    return row.map((x) => x / nr);
  });

  // 3. mean resultant
  const r: Vec = new Array(D).fill(0.0);
  for (const row of rows) {
    for (let j = 0; j < D; j++) r[j] += row[j] / n;
  }
  const rho = Math.min(norm(r), RHOMAX);
  if (rho < 1e-12) return null; // isotropic — no mean direction

  // 4. mean direction
  const mu_hat: Vec = r.map((x) => x / rho);

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
  let warmth_vmf = 0.0;
  for (let j = 0; j < D; j++) warmth_vmf += warm[j] * mu_hat[j];

  // 8. jackknife SE(μ̂): leave-one-out mean directions, renormalized
  const jks: Vec[] = [];
  for (let i = 0; i < n; i++) {
    const m: Vec = new Array(D).fill(0.0);
    for (let j = 0; j < n; j++) {
      if (j === i) continue;
      for (let d = 0; d < D; d++) m[d] += rows[j][d] / (n - 1);
    }
    const nm = norm(m);
    jks.push(m.map((x) => x / nm));
  }
  const jm: Vec = new Array(D).fill(0.0);
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
  const mu_se = Math.sqrt(((n - 1) / n) * acc);

  // 9. saturation flag
  const saturated = rho >= RHOMAX || kappa >= KMAX;

  return { mu_hat, kappa, rho, n, warmth_vmf, mu_se, saturated };
}

// ---------- SPEC §3: edge ----------
export interface Edge {
  d_mu: number;
  d_warmth: number;
  d_log_kappa: number;
  real: boolean;
}

export function edge(fb: Fit, fa: Fit): Edge {
  const diff: Vec = new Array(D).fill(0.0);
  for (let j = 0; j < D; j++) diff[j] = fa.mu_hat[j] - fb.mu_hat[j];
  const d_mu = norm(diff);
  const d_warmth = fa.warmth_vmf - fb.warmth_vmf;
  const d_log_kappa = Math.log(fa.kappa / fb.kappa);
  // db_factor = 2.0 — the drift deadband
  const real = d_mu > 2.0 * Math.max(fb.mu_se, fa.mu_se);
  return { d_mu, d_warmth, d_log_kappa, real };
}
