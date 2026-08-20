// Polyformal vMF kernel — Zig port (standard library only).
//
// Implements the three functions of SPEC.md:
//   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
//   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
//   edge      — field step between two fits
//
// Differential test: reads ../golden.json and ../inputs.json (run from zig/).
// Values are extracted with a minimal key-based number scanner rather than
// std.json, so the port is insensitive to std.json API changes across versions.
//
// VERIFIED: zig 0.14.1 (linux x86_64) — all SPEC §4 checks PASS (max err 3.0e-13).
// Build & run:  cd zig && zig build-exe main.zig -O ReleaseFast && ./main

const std = @import("std");

const D: usize = 7;
const KMAX: f64 = 500.0;
const NMIN: usize = 10;
const RHOMAX: f64 = 0.999;
const MAXN: usize = 64;

const Vec = [D]f64;

// ---------- SPEC §1: A7 ----------
fn a7(k: f64) f64 {
    if (k < 0.5) return k / 7.0; // leading Taylor term; closed form cancels
    const s = std.math.sinh(k);
    const c = std.math.cosh(k);
    const k2 = k * k;
    return ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s) /
        ((1.0 + 3.0 / k2) * s - (3.0 / k) * c);
}

fn clip(x: f64, lo: f64, hi: f64) f64 {
    return @min(@max(x, lo), hi);
}

fn norm(v: Vec) f64 {
    var s: f64 = 0.0;
    for (v) |x| s += x * x;
    return @sqrt(s);
}

// ---------- SPEC §2: vmf_fit ----------
const Fit = struct {
    mu_hat: Vec,
    kappa: f64,
    rho: f64,
    n: usize,
    warmth_vmf: f64,
    mu_se: f64,
    saturated: bool,
};

// Returns null when unidentifiable/isotropic — never a fake number.
fn vmfFit(zs: []const Vec, warm: Vec) ?Fit {
    const n = zs.len;
    if (n < NMIN) return null;
    // 2. defensive renormalization
    var rows: [MAXN]Vec = undefined;
    for (zs, 0..) |row, i| {
        const nrm = norm(row);
        for (0..D) |j| rows[i][j] = row[j] / nrm;
    }
    // 3. mean resultant
    var r: Vec = @splat(0.0);
    for (0..n) |i| {
        for (0..D) |j| r[j] += rows[i][j] / @as(f64, @floatFromInt(n));
    }
    const rho = @min(norm(r), RHOMAX);
    if (rho < 1e-12) return null; // isotropic — no mean direction
    // 4. mean direction
    var out: Fit = undefined;
    for (0..D) |j| out.mu_hat[j] = r[j] / rho;
    // 5. Banerjee init, clipped
    var kappa = clip(rho * (@as(f64, D) - rho * rho) / (1.0 - rho * rho), 1e-6, KMAX);
    // 6. Newton solve on A7(kappa) = rho
    for (0..60) |_| {
        const a = a7(kappa);
        const g = 1.0 - a * a - (@as(f64, D) - 1.0) * a / kappa;
        const step = (a - rho) / g;
        kappa = clip(kappa - step, 1e-6, KMAX);
        if (@abs(g) < 1e-12 or @abs(step) < 1e-9) break;
    }
    out.kappa = kappa;
    out.rho = rho;
    out.n = n;
    // 7. warmth
    var w: f64 = 0.0;
    for (0..D) |j| w += warm[j] * out.mu_hat[j];
    out.warmth_vmf = w;
    // 8. jackknife SE(mu_hat): leave-one-out mean directions, renormalized
    var jks: [MAXN]Vec = undefined;
    for (0..n) |i| {
        var m: Vec = @splat(0.0);
        for (0..n) |j| {
            if (j == i) continue;
            for (0..D) |d| m[d] += rows[j][d] / @as(f64, @floatFromInt(n - 1));
        }
        const nm = norm(m);
        for (0..D) |d| jks[i][d] = m[d] / nm;
    }
    var jm: Vec = @splat(0.0);
    for (0..n) |i| {
        for (0..D) |d| jm[d] += jks[i][d] / @as(f64, @floatFromInt(n));
    }
    var acc: f64 = 0.0;
    for (0..n) |i| {
        var s: f64 = 0.0;
        for (0..D) |d| {
            const diff = jks[i][d] - jm[d];
            s += diff * diff;
        }
        acc += s;
    }
    out.mu_se = @sqrt(@as(f64, @floatFromInt(n - 1)) / @as(f64, @floatFromInt(n)) * acc);
    // 9. saturation flag
    out.saturated = rho >= RHOMAX or kappa >= KMAX;
    return out;
}

// ---------- SPEC §3: edge ----------
const Edge = struct {
    d_mu: f64,
    d_warmth: f64,
    d_log_kappa: f64,
    real: bool,
};

fn edge(fb: Fit, fa: Fit) Edge {
    var diff: Vec = undefined;
    for (0..D) |j| diff[j] = fa.mu_hat[j] - fb.mu_hat[j];
    const d_mu = norm(diff);
    return .{
        .d_mu = d_mu,
        .d_warmth = fa.warmth_vmf - fb.warmth_vmf,
        .d_log_kappa = @log(fa.kappa / fb.kappa),
        .real = d_mu > 2.0 * @max(fb.mu_se, fa.mu_se), // db_factor = 2.0
    };
}

// ---------- minimal JSON number extraction (std lib only) ----------
// Finds the first occurrence of "key" and scans `count` float literals after it.
fn numbersAfter(text: []const u8, key: []const u8, out: []f64) !void {
    var pat_buf: [128]u8 = undefined;
    const pat = try std.fmt.bufPrint(&pat_buf, "\"{s}\"", .{key});
    var i = (std.mem.indexOf(u8, text, pat) orelse return error.KeyNotFound) + pat.len;
    for (out) |*slot| {
        while (i < text.len and !(std.ascii.isDigit(text[i]) or text[i] == '-' or text[i] == '+')) i += 1;
        const start = i;
        while (i < text.len and (std.ascii.isDigit(text[i]) or text[i] == '-' or text[i] == '+' or
            text[i] == '.' or text[i] == 'e' or text[i] == 'E')) i += 1;
        slot.* = try std.fmt.parseFloat(f64, text[start..i]);
    }
}

// ---------- SPEC §4: differential test ----------
var failures: u32 = 0;

fn check(stdout: anytype, name: []const u8, got: f64, want: f64, tol: f64) !void {
    const err = @abs(got - want);
    if (err > tol) {
        try stdout.print("FAIL {s}: got {d:.12} want {d:.12} (err {e:.3} > {d})\n", .{ name, got, want, err, tol });
        failures += 1;
    } else {
        try stdout.print("ok   {s}: {d:.12} (err {e:.3})\n", .{ name, got, err });
    }
}

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const stdout = std.io.getStdOut().writer();

    const golden = try std.fs.cwd().readFileAlloc(allocator, "../golden.json", 1 << 20);
    const inputs = try std.fs.cwd().readFileAlloc(allocator, "../inputs.json", 1 << 20);

    // --- A7 ---
    var kappas: [11]f64 = undefined;
    var values: [11]f64 = undefined;
    try numbersAfter(golden, "kappas", &kappas);
    try numbersAfter(golden, "values", &values);
    for (kappas, values) |k, v| {
        var name_buf: [64]u8 = undefined;
        const name = try std.fmt.bufPrint(&name_buf, "A7({d})", .{k});
        try check(stdout, name, a7(k), v, 1e-9);
    }

    // --- inputs ---
    var flat: [30 * D]f64 = undefined;
    try numbersAfter(inputs, "z", &flat);
    var zs: [30]Vec = undefined;
    for (0..30) |i| {
        for (0..D) |j| zs[i][j] = flat[i * D + j];
    }
    var warm: Vec = undefined;
    try numbersAfter(golden, "WARM", &warm);

    // --- vmf_fit on zs ---
    const fb = vmfFit(&zs, warm) orelse {
        try stdout.print("FAIL vmf_fit returned null on golden input\n", .{});
        std.process.exit(1);
    };
    var one: [1]f64 = undefined;
    try numbersAfter(golden, "kappa", &one);
    const g_kappa = one[0];
    try numbersAfter(golden, "rho", &one);
    const g_rho = one[0];
    try numbersAfter(golden, "warmth_vmf", &one);
    const g_warmth = one[0];
    try numbersAfter(golden, "mu_se", &one);
    const g_mu_se = one[0];
    var g_mu: Vec = undefined;
    try numbersAfter(golden, "mu_hat", &g_mu);

    try check(stdout, "kappa", fb.kappa, g_kappa, 1e-6);
    try check(stdout, "rho", fb.rho, g_rho, 1e-6);
    try check(stdout, "warmth_vmf", fb.warmth_vmf, g_warmth, 1e-6);
    try check(stdout, "mu_se", fb.mu_se, g_mu_se, 1e-6);
    var mu_err: f64 = 0.0;
    for (0..D) |j| mu_err = @max(mu_err, @abs(fb.mu_hat[j] - g_mu[j]));
    if (mu_err > 1e-6) {
        try stdout.print("FAIL mu_hat: max abs err {e:.3}\n", .{mu_err});
        failures += 1;
    } else {
        try stdout.print("ok   mu_hat: max abs err {e:.3}\n", .{mu_err});
    }
    if (fb.n != 30) {
        try stdout.print("FAIL n: {d} != 30\n", .{fb.n});
        failures += 1;
    } else {
        try stdout.print("ok   n == 30\n", .{});
    }
    if (fb.saturated) {
        try stdout.print("FAIL saturated: expected false\n", .{});
        failures += 1;
    } else {
        try stdout.print("ok   saturated == false\n", .{});
    }

    // --- edge: second fit on zs + 0.05 element-wise (SPEC §4) ---
    var zs2: [30]Vec = undefined;
    for (0..30) |i| {
        for (0..D) |j| zs2[i][j] = zs[i][j] + 0.05;
    }
    const fa = vmfFit(&zs2, warm) orelse {
        try stdout.print("FAIL vmf_fit returned null on shifted input\n", .{});
        std.process.exit(1);
    };
    const e = edge(fb, fa);
    try numbersAfter(golden, "d_mu", &one);
    try check(stdout, "edge.d_mu", e.d_mu, one[0], 1e-6);
    try numbersAfter(golden, "d_warmth", &one);
    try check(stdout, "edge.d_warmth", e.d_warmth, one[0], 1e-6);
    try numbersAfter(golden, "d_log_kappa", &one);
    try check(stdout, "edge.d_log_kappa", e.d_log_kappa, one[0], 1e-6);
    if (e.real) {
        try stdout.print("FAIL edge.real: expected false\n", .{});
        failures += 1;
    } else {
        try stdout.print("ok   edge.real == false\n", .{});
    }

    try stdout.print("\n", .{});
    try stdout.print("actual values: kappa={d:.6} rho={d:.6} warmth={d:.6}\n", .{ fb.kappa, fb.rho, fb.warmth_vmf });
    try stdout.print("golden values: kappa={d:.6} rho={d:.6} warmth={d:.6}\n", .{ g_kappa, g_rho, g_warmth });

    if (failures == 0) {
        try stdout.print("PASS: all differential checks within SPEC §4 tolerances\n", .{});
    } else {
        try stdout.print("FAIL: {d} check(s) failed\n", .{failures});
    }
    std.process.exit(if (failures == 0) 0 else 1);
}
