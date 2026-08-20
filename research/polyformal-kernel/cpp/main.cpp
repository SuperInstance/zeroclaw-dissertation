// Polyformal vMF kernel — C++ port (C++17, standard library only).
//
// Implements the three functions of SPEC.md:
//   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
//   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
//   edge      — field step between two fits
//
// Differential test: reads ../golden.json and ../inputs.json (run from cpp/).
// Neither file needs a real JSON parser — values are extracted with a minimal
// key-based number scanner, so no external JSON library is required.
//
// Build & run:  g++ -O2 -std=c++17 main.cpp -o vmf_test && ./vmf_test

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <string>
#include <vector>

constexpr int D = 7;
constexpr double KMAX = 500.0;
constexpr int NMIN = 10;
constexpr double RHOMAX = 0.999;

using Vec = std::array<double, D>;

// ---------- SPEC §1: A7 ----------
static double a7(double k) {
    if (k < 0.5) return k / 7.0; // leading Taylor term; closed form cancels
    const double s = std::sinh(k), c = std::cosh(k), k2 = k * k;
    return ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s)
         / ((1.0 + 3.0 / k2) * s - (3.0 / k) * c);
}

static double clip(double x, double lo, double hi) {
    return std::clamp(x, lo, hi);
}

static double norm(const Vec &v) {
    double s = 0.0;
    for (double x : v) s += x * x;
    return std::sqrt(s);
}

// ---------- SPEC §2: vmf_fit ----------
struct Fit {
    Vec mu_hat{};
    double kappa = 0.0, rho = 0.0, warmth_vmf = 0.0, mu_se = 0.0;
    int n = 0;
    bool saturated = false;
};

// nullopt when unidentifiable/isotropic — never a fake number.
static std::optional<Fit> vmf_fit(const std::vector<Vec> &zs, const Vec &warm) {
    const int n = static_cast<int>(zs.size());
    if (n < NMIN) return std::nullopt;
    // 2. defensive renormalization
    std::vector<Vec> rows = zs;
    for (auto &row : rows) {
        const double nrm = norm(row);
        for (double &x : row) x /= nrm;
    }
    // 3. mean resultant
    Fit out;
    Vec r{};
    for (const auto &row : rows)
        for (int j = 0; j < D; j++) r[j] += row[j] / n;
    const double rho = std::min(norm(r), RHOMAX);
    if (rho < 1e-12) return std::nullopt; // isotropic — no mean direction
    // 4. mean direction
    for (int j = 0; j < D; j++) out.mu_hat[j] = r[j] / rho;
    // 5. Banerjee init, clipped
    double kappa = clip(rho * (D - rho * rho) / (1.0 - rho * rho), 1e-6, KMAX);
    // 6. Newton solve on A7(kappa) = rho
    for (int it = 0; it < 60; it++) {
        const double a = a7(kappa);
        const double g = 1.0 - a * a - (D - 1) * a / kappa;
        const double step = (a - rho) / g;
        kappa = clip(kappa - step, 1e-6, KMAX);
        if (std::fabs(g) < 1e-12 || std::fabs(step) < 1e-9) break;
    }
    out.kappa = kappa;
    out.rho = rho;
    out.n = n;
    // 7. warmth
    for (int j = 0; j < D; j++) out.warmth_vmf += warm[j] * out.mu_hat[j];
    // 8. jackknife SE(mu_hat): leave-one-out mean directions, renormalized
    std::vector<Vec> jks(n);
    for (int i = 0; i < n; i++) {
        Vec m{};
        for (int j = 0; j < n; j++) {
            if (j == i) continue;
            for (int d = 0; d < D; d++) m[d] += rows[j][d] / (n - 1);
        }
        const double nm = norm(m);
        for (int d = 0; d < D; d++) jks[i][d] = m[d] / nm;
    }
    Vec jm{};
    for (const auto &jk : jks)
        for (int d = 0; d < D; d++) jm[d] += jk[d] / n;
    double acc = 0.0;
    for (const auto &jk : jks) {
        double s = 0.0;
        for (int d = 0; d < D; d++) {
            const double diff = jk[d] - jm[d];
            s += diff * diff;
        }
        acc += s;
    }
    out.mu_se = std::sqrt(static_cast<double>(n - 1) / n * acc);
    // 9. saturation flag
    out.saturated = (rho >= RHOMAX || kappa >= KMAX);
    return out;
}

// ---------- SPEC §3: edge ----------
struct Edge {
    double d_mu, d_warmth, d_log_kappa;
    bool real;
};

static Edge edge(const Fit &fb, const Fit &fa) {
    Vec diff{};
    for (int j = 0; j < D; j++) diff[j] = fa.mu_hat[j] - fb.mu_hat[j];
    Edge e;
    e.d_mu = norm(diff);
    e.d_warmth = fa.warmth_vmf - fb.warmth_vmf;
    e.d_log_kappa = std::log(fa.kappa / fb.kappa);
    e.real = e.d_mu > 2.0 * std::max(fb.mu_se, fa.mu_se); // db_factor = 2.0
    return e;
}

// ---------- minimal JSON number extraction (std lib only) ----------
// Finds the first occurrence of "key" and scans `count` float literals after it.
static std::vector<double> numbers_after(const std::string &text, const std::string &key, int count) {
    const std::string pat = "\"" + key + "\"";
    size_t pos = text.find(pat);
    if (pos == std::string::npos) {
        std::fprintf(stderr, "key %s not found\n", key.c_str());
        std::exit(1);
    }
    pos += pat.size();
    std::vector<double> out;
    out.reserve(count);
    while (static_cast<int>(out.size()) < count) {
        while (pos < text.size() && !(std::isdigit(static_cast<unsigned char>(text[pos]))
                                      || text[pos] == '-' || text[pos] == '+'))
            pos++;
        size_t end = pos;
        while (end < text.size() && (std::isdigit(static_cast<unsigned char>(text[end]))
                                     || text[end] == '-' || text[end] == '+' || text[end] == '.'
                                     || text[end] == 'e' || text[end] == 'E'))
            end++;
        out.push_back(std::stod(text.substr(pos, end - pos)));
        pos = end;
    }
    return out;
}

static std::string read_file(const char *path) {
    std::ifstream f(path);
    if (!f) {
        std::fprintf(stderr, "cannot read %s\n", path);
        std::exit(1);
    }
    std::ostringstream ss;
    ss << f.rdbuf();
    return ss.str();
}

// ---------- SPEC §4: differential test ----------
static int failures = 0;
static void check(const std::string &name, double got, double want, double tol) {
    const double err = std::fabs(got - want);
    if (err > tol) {
        std::printf("FAIL %s: got %.12f want %.12f (err %.3e > %g)\n", name.c_str(), got, want, err, tol);
        failures++;
    } else {
        std::printf("ok   %s: %.12f (err %.3e)\n", name.c_str(), got, err);
    }
}

int main() {
    const std::string golden = read_file("../golden.json");
    const std::string inputs = read_file("../inputs.json");

    // --- A7 ---
    const auto kappas = numbers_after(golden, "kappas", 11);
    const auto values = numbers_after(golden, "values", 11);
    for (int i = 0; i < 11; i++) {
        char name[64];
        std::snprintf(name, sizeof name, "A7(%g)", kappas[i]);
        check(name, a7(kappas[i]), values[i], 1e-9);
    }

    // --- inputs ---
    const auto flat = numbers_after(inputs, "z", 30 * D);
    std::vector<Vec> zs(30);
    for (int i = 0; i < 30; i++)
        for (int j = 0; j < D; j++) zs[i][j] = flat[i * D + j];
    Vec warm{};
    const auto warmv = numbers_after(golden, "WARM", D);
    for (int j = 0; j < D; j++) warm[j] = warmv[j];

    // --- vmf_fit on zs ---
    const auto fbo = vmf_fit(zs, warm);
    if (!fbo) {
        std::printf("FAIL vmf_fit returned nullopt on golden input\n");
        return 1;
    }
    const Fit &fb = *fbo;
    const double g_kappa = numbers_after(golden, "kappa", 1)[0];
    const double g_rho = numbers_after(golden, "rho", 1)[0];
    const double g_warmth = numbers_after(golden, "warmth_vmf", 1)[0];
    const double g_mu_se = numbers_after(golden, "mu_se", 1)[0];
    const auto g_mu = numbers_after(golden, "mu_hat", D);

    check("kappa", fb.kappa, g_kappa, 1e-6);
    check("rho", fb.rho, g_rho, 1e-6);
    check("warmth_vmf", fb.warmth_vmf, g_warmth, 1e-6);
    check("mu_se", fb.mu_se, g_mu_se, 1e-6);
    double mu_err = 0.0;
    for (int j = 0; j < D; j++) mu_err = std::max(mu_err, std::fabs(fb.mu_hat[j] - g_mu[j]));
    if (mu_err > 1e-6) { std::printf("FAIL mu_hat: max abs err %.3e\n", mu_err); failures++; }
    else std::printf("ok   mu_hat: max abs err %.3e\n", mu_err);
    if (fb.n != 30) { std::printf("FAIL n: %d != 30\n", fb.n); failures++; }
    else std::printf("ok   n == 30\n");
    if (fb.saturated) { std::printf("FAIL saturated: expected false\n"); failures++; }
    else std::printf("ok   saturated == false\n");

    // --- edge: second fit on zs + 0.05 element-wise (SPEC §4) ---
    std::vector<Vec> zs2 = zs;
    for (auto &row : zs2)
        for (double &x : row) x += 0.05;
    const auto fao = vmf_fit(zs2, warm);
    if (!fao) {
        std::printf("FAIL vmf_fit returned nullopt on shifted input\n");
        return 1;
    }
    const Edge e = edge(fb, *fao);
    check("edge.d_mu", e.d_mu, numbers_after(golden, "d_mu", 1)[0], 1e-6);
    check("edge.d_warmth", e.d_warmth, numbers_after(golden, "d_warmth", 1)[0], 1e-6);
    check("edge.d_log_kappa", e.d_log_kappa, numbers_after(golden, "d_log_kappa", 1)[0], 1e-6);
    if (e.real) { std::printf("FAIL edge.real: expected false\n"); failures++; }
    else std::printf("ok   edge.real == false\n");

    std::printf("\n");
    std::printf("actual values: kappa=%.6f rho=%.6f warmth=%.6f\n", fb.kappa, fb.rho, fb.warmth_vmf);
    std::printf("golden values: kappa=%.6f rho=%.6f warmth=%.6f\n", g_kappa, g_rho, g_warmth);

    if (failures == 0) std::printf("PASS: all differential checks within SPEC §4 tolerances\n");
    else std::printf("FAIL: %d check(s) failed\n", failures);
    return failures == 0 ? 0 : 1;
}
