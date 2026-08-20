// Polyformal vMF kernel — Rust port (stdlib only, no crates).
//
// Implements the three functions of SPEC.md:
//   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
//   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
//   edge      — field step between two fits
//
// Differential test: reads ../golden.json and ../inputs.json (run from rust/).
// Neither file needs a real JSON parser — values are extracted with a minimal
// key-based number scanner (stdlib only), so no serde dependency is required.
//
// Build & run:  rustc -O main.rs -o vmf_test && ./vmf_test

use std::cell::Cell;
use std::fs;
use std::process;

const D: usize = 7;
const KMAX: f64 = 500.0;
const NMIN: usize = 10;
const RHOMAX: f64 = 0.999;

// ---------- SPEC §1: A7 ----------
fn a7(k: f64) -> f64 {
    if k < 0.5 {
        return k / 7.0; // leading Taylor term; closed form cancels catastrophically
    }
    let s = k.sinh();
    let c = k.cosh();
    let k2 = k * k;
    ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s)
        / ((1.0 + 3.0 / k2) * s - (3.0 / k) * c)
}

fn clip(x: f64, lo: f64, hi: f64) -> f64 {
    x.max(lo).min(hi)
}

fn norm(v: &[f64]) -> f64 {
    v.iter().map(|x| x * x).sum::<f64>().sqrt()
}

// ---------- SPEC §2: vmf_fit ----------
struct Fit {
    mu_hat: Vec<f64>,
    kappa: f64,
    rho: f64,
    n: usize,
    warmth_vmf: f64,
    mu_se: f64,
    saturated: bool,
}

fn vmf_fit(zs: &[Vec<f64>], warm: &[f64]) -> Option<Fit> {
    let n = zs.len();
    if n < NMIN {
        return None; // unidentifiable — never a fake number
    }
    // 2. defensive renormalization
    let rows: Vec<Vec<f64>> = zs
        .iter()
        .map(|row| {
            let nrm = norm(row);
            row.iter().map(|x| x / nrm).collect()
        })
        .collect();
    // 3. mean resultant
    let mut r = vec![0.0f64; D];
    for row in &rows {
        for j in 0..D {
            r[j] += row[j] / n as f64;
        }
    }
    let rho = norm(&r).min(RHOMAX);
    if rho < 1e-12 {
        return None; // isotropic — no mean direction
    }
    // 4. mean direction
    let mu_hat: Vec<f64> = r.iter().map(|x| x / rho).collect();
    // 5. Banerjee init, clipped
    let mut kappa = clip(
        rho * (D as f64 - rho * rho) / (1.0 - rho * rho),
        1e-6,
        KMAX,
    );
    // 6. Newton solve on A7(kappa) = rho
    for _ in 0..60 {
        let a = a7(kappa);
        let g = 1.0 - a * a - (D as f64 - 1.0) * a / kappa;
        let step = (a - rho) / g;
        kappa = clip(kappa - step, 1e-6, KMAX);
        if g.abs() < 1e-12 || step.abs() < 1e-9 {
            break;
        }
    }
    // 7. warmth
    let warmth_vmf: f64 = warm.iter().zip(mu_hat.iter()).map(|(w, m)| w * m).sum();
    // 8. jackknife SE(mu_hat): leave-one-out mean directions, renormalized
    let mut jks: Vec<Vec<f64>> = Vec::with_capacity(n);
    for i in 0..n {
        let mut m = vec![0.0f64; D];
        for (j, row) in rows.iter().enumerate() {
            if j == i {
                continue;
            }
            for d in 0..D {
                m[d] += row[d] / (n - 1) as f64;
            }
        }
        let nm = norm(&m);
        for d in 0..D {
            m[d] /= nm;
        }
        jks.push(m);
    }
    let mut jm = vec![0.0f64; D];
    for jk in &jks {
        for d in 0..D {
            jm[d] += jk[d] / n as f64;
        }
    }
    let mut acc = 0.0f64;
    for jk in &jks {
        let mut s = 0.0;
        for d in 0..D {
            let diff = jk[d] - jm[d];
            s += diff * diff;
        }
        acc += s;
    }
    let mu_se = ((n - 1) as f64 / n as f64 * acc).sqrt();
    // 9. saturation flag
    let saturated = rho >= RHOMAX || kappa >= KMAX;
    Some(Fit {
        mu_hat,
        kappa,
        rho,
        n,
        warmth_vmf,
        mu_se,
        saturated,
    })
}

// ---------- SPEC §3: edge ----------
fn edge(fb: &Fit, fa: &Fit) -> (f64, f64, f64, bool) {
    let diff: Vec<f64> = fa
        .mu_hat
        .iter()
        .zip(fb.mu_hat.iter())
        .map(|(a, b)| a - b)
        .collect();
    let d_mu = norm(&diff);
    let d_warmth = fa.warmth_vmf - fb.warmth_vmf;
    let d_log_kappa = (fa.kappa / fb.kappa).ln();
    let real = d_mu > 2.0 * fb.mu_se.max(fa.mu_se); // db_factor = 2.0
    (d_mu, d_warmth, d_log_kappa, real)
}

// ---------- minimal JSON number extraction (stdlib only) ----------
// Finds the first occurrence of `"key"` and scans `count` float literals after it.
fn numbers_after(text: &str, key: &str, count: usize) -> Vec<f64> {
    let pat = format!("\"{}\"", key);
    let mut i = text
        .find(&pat)
        .unwrap_or_else(|| panic!("key {} not found", key))
        + pat.len();
    let bytes = text.as_bytes();
    let mut out = Vec::with_capacity(count);
    while out.len() < count {
        while i < bytes.len() && !(bytes[i].is_ascii_digit() || bytes[i] == b'-' || bytes[i] == b'+')
        {
            i += 1;
        }
        let start = i;
        while i < bytes.len()
            && (bytes[i].is_ascii_digit()
                || matches!(bytes[i], b'-' | b'+' | b'.' | b'e' | b'E'))
        {
            i += 1;
        }
        out.push(
            text[start..i]
                .parse::<f64>()
                .unwrap_or_else(|_| panic!("bad number after key {}", key)),
        );
    }
    out
}

// ---------- SPEC §4: differential test ----------
fn main() {
    let golden = fs::read_to_string("../golden.json").expect("cannot read ../golden.json");
    let inputs = fs::read_to_string("../inputs.json").expect("cannot read ../inputs.json");

    let failures = Cell::new(0u32);
    let check = |name: &str, got: f64, want: f64, tol: f64| {
        let err = (got - want).abs();
        if err > tol {
            println!("FAIL {}: got {:.12} want {:.12} (err {:.3e} > {})", name, got, want, err, tol);
            failures.set(failures.get() + 1);
        } else {
            println!("ok   {}: {:.12} (err {:.3e})", name, got, err);
        }
    };

    // --- A7 ---
    let kappas = numbers_after(&golden, "kappas", 11);
    let values = numbers_after(&golden, "values", 11);
    for (k, v) in kappas.iter().zip(values.iter()) {
        check(&format!("A7({})", k), a7(*k), *v, 1e-9);
    }

    // --- inputs ---
    let flat = numbers_after(&inputs, "z", 30 * D);
    let zs: Vec<Vec<f64>> = flat.chunks(D).map(|c| c.to_vec()).collect();
    let warm = numbers_after(&golden, "WARM", D);

    // --- vmf_fit on zs ---
    let fb = vmf_fit(&zs, &warm).expect("vmf_fit returned None on golden input");
    let g_kappa = numbers_after(&golden, "kappa", 1)[0];
    let g_rho = numbers_after(&golden, "rho", 1)[0];
    let g_warmth = numbers_after(&golden, "warmth_vmf", 1)[0];
    let g_mu_se = numbers_after(&golden, "mu_se", 1)[0];
    let g_mu = numbers_after(&golden, "mu_hat", D);

    check("kappa", fb.kappa, g_kappa, 1e-6);
    check("rho", fb.rho, g_rho, 1e-6);
    check("warmth_vmf", fb.warmth_vmf, g_warmth, 1e-6);
    check("mu_se", fb.mu_se, g_mu_se, 1e-6);
    let mu_err = fb
        .mu_hat
        .iter()
        .zip(g_mu.iter())
        .map(|(a, b)| (a - b).abs())
        .fold(0.0f64, f64::max);
    if mu_err > 1e-6 {
        println!("FAIL mu_hat: max abs err {:.3e}", mu_err);
        failures.set(failures.get() + 1);
    } else {
        println!("ok   mu_hat: max abs err {:.3e}", mu_err);
    }
    if fb.n != 30 {
        println!("FAIL n: {} != 30", fb.n);
        failures.set(failures.get() + 1);
    } else {
        println!("ok   n == 30");
    }
    if fb.saturated {
        println!("FAIL saturated: expected false");
        failures.set(failures.get() + 1);
    } else {
        println!("ok   saturated == false");
    }

    // --- edge: second fit on zs + 0.05 element-wise (SPEC §4) ---
    let zs2: Vec<Vec<f64>> = zs
        .iter()
        .map(|row| row.iter().map(|x| x + 0.05).collect())
        .collect();
    let fa = vmf_fit(&zs2, &warm).expect("vmf_fit returned None on shifted input");
    let (d_mu, d_warmth, d_log_kappa, real) = edge(&fb, &fa);
    check("edge.d_mu", d_mu, numbers_after(&golden, "d_mu", 1)[0], 1e-6);
    check("edge.d_warmth", d_warmth, numbers_after(&golden, "d_warmth", 1)[0], 1e-6);
    check("edge.d_log_kappa", d_log_kappa, numbers_after(&golden, "d_log_kappa", 1)[0], 1e-6);
    if real {
        println!("FAIL edge.real: expected false");
        failures.set(failures.get() + 1);
    } else {
        println!("ok   edge.real == false");
    }

    println!();
    println!("actual values: kappa={:.6} rho={:.6} warmth={:.6}", fb.kappa, fb.rho, fb.warmth_vmf);
    println!("golden values: kappa={:.6} rho={:.6} warmth={:.6}", g_kappa, g_rho, g_warmth);

    if failures.get() == 0 {
        println!("PASS: all differential checks within SPEC §4 tolerances");
    } else {
        println!("FAIL: {} check(s) failed", failures.get());
    }
    process::exit(if failures.get() == 0 { 0 } else { 1 });
}
