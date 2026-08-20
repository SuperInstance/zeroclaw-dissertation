// Polyformal vMF kernel — TypeScript differential test.
//
// Reads ../golden.json + ../inputs.json and asserts SPEC §4 tolerances:
//   A7 ≤ 1e-9; fit values ≤ 1e-6; edge ≤ 1e-6; n == 30; saturated == false; real == false.
// The second fit in `edge` is vmf_fit on zs + 0.05 element-wise (SPEC §4).
//
// Typecheck + run:  npx --yes -p typescript tsc -p tsconfig.json && node dist/test.js   (from ts/)
//
// NOTE: `tsc` is not preinstalled on this machine; the typecheck above was run
// via npx (fetches the `typescript` package). If tsc is unavailable entirely,
// the identical kernel in ../js/ is the always-runnable twin.

import { a7, vmfFit, edge } from './main';

// Minimal ambient declarations so the test typechecks with zero dependencies
// (no @types/node needed): Node's fs/path are accessed via a bare require.
declare function require(id: string): any;
declare const __dirname: string;
declare const console: { log(...args: unknown[]): void };
declare const process: { exit(code?: number): never };

const fs = require('fs');
const path = require('path');

const golden = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'golden.json'), 'utf8'));
const inputs = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'inputs.json'), 'utf8'));

let failures = 0;
function check(name: string, got: number, want: number, tol: number): void {
  const err = Math.abs(got - want);
  if (err > tol) {
    console.log(`FAIL ${name}: got ${got} want ${want} (err ${err.toExponential(3)} > ${tol})`);
    failures++;
  } else {
    console.log(`ok   ${name}: ${got} (err ${err.toExponential(3)})`);
  }
}

// ---------- A7 ----------
const { kappas, values } = golden.A7;
for (let i = 0; i < kappas.length; i++) {
  check(`A7(${kappas[i]})`, a7(kappas[i]), values[i], 1e-9);
}

// ---------- inputs ----------
const zs: number[][] = inputs.z; // 30 x 7
const warm: number[] = golden.spec.WARM;

// ---------- vmf_fit on zs ----------
const fb = vmfFit(zs, warm);
if (fb === null) {
  console.log('FAIL vmf_fit returned null on golden input');
  process.exit(1);
}
check('kappa', fb.kappa, golden.vmf_fit.kappa, 1e-6);
check('rho', fb.rho, golden.vmf_fit.rho, 1e-6);
check('warmth_vmf', fb.warmth_vmf, golden.vmf_fit.warmth_vmf, 1e-6);
check('mu_se', fb.mu_se, golden.vmf_fit.mu_se, 1e-6);
let muErr = 0.0;
for (let j = 0; j < 7; j++) muErr = Math.max(muErr, Math.abs(fb.mu_hat[j] - golden.vmf_fit.mu_hat[j]));
if (muErr > 1e-6) {
  console.log(`FAIL mu_hat: max abs err ${muErr}`);
  failures++;
} else {
  console.log(`ok   mu_hat: max abs err ${muErr}`);
}
if (fb.n !== 30) {
  console.log(`FAIL n: ${fb.n} != 30`);
  failures++;
} else {
  console.log('ok   n == 30');
}
if (fb.saturated) {
  console.log('FAIL saturated: expected false');
  failures++;
} else {
  console.log('ok   saturated == false');
}

// ---------- edge: second fit on zs + 0.05 element-wise ----------
const zs2 = zs.map((row) => row.map((x) => x + 0.05));
const fa = vmfFit(zs2, warm);
if (fa === null) {
  console.log('FAIL vmf_fit returned null on shifted input');
  process.exit(1);
}
const e = edge(fb, fa);
check('edge.d_mu', e.d_mu, golden.edge.d_mu, 1e-6);
check('edge.d_warmth', e.d_warmth, golden.edge.d_warmth, 1e-6);
check('edge.d_log_kappa', e.d_log_kappa, golden.edge.d_log_kappa, 1e-6);
if (e.real) {
  console.log('FAIL edge.real: expected false');
  failures++;
} else {
  console.log('ok   edge.real == false');
}

// ---------- summary ----------
console.log('');
console.log(`actual values: kappa=${fb.kappa.toFixed(6)} rho=${fb.rho.toFixed(6)} warmth=${fb.warmth_vmf.toFixed(6)}`);
console.log(`golden values: kappa=${golden.vmf_fit.kappa.toFixed(6)} rho=${golden.vmf_fit.rho.toFixed(6)} warmth=${golden.vmf_fit.warmth_vmf.toFixed(6)}`);

if (failures === 0) {
  console.log('PASS: all differential checks within SPEC §4 tolerances');
  process.exit(0);
} else {
  console.log(`FAIL: ${failures} check(s) failed`);
  process.exit(1);
}
