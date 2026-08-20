/* Polyformal vMF kernel — C port (C11, libc/libm only).
 *
 * Implements the three functions of SPEC.md:
 *   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
 *   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
 *   edge      — field step between two fits
 *
 * Differential test: reads ../golden.json and ../inputs.json (run from c/).
 * Neither file needs a real JSON parser — values are extracted with a minimal
 * key-based number scanner (strtod), so no external JSON library is required.
 *
 * Build & run:  gcc -O2 -std=c11 main.c -lm -o vmf_test && ./vmf_test
 */

#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define D 7
#define KMAX 500.0
#define NMIN 10
#define RHOMAX 0.999
#define MAXN 64

/* ---------- SPEC §1: A7 ---------- */
static double a7(double k) {
    if (k < 0.5) return k / 7.0; /* leading Taylor term; closed form cancels */
    double s = sinh(k), c = cosh(k), k2 = k * k;
    return ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s)
         / ((1.0 + 3.0 / k2) * s - (3.0 / k) * c);
}

static double clip(double x, double lo, double hi) {
    return x < lo ? lo : (x > hi ? hi : x);
}

static double norm7(const double v[D]) {
    double s = 0.0;
    for (int j = 0; j < D; j++) s += v[j] * v[j];
    return sqrt(s);
}

/* ---------- SPEC §2: vmf_fit ---------- */
typedef struct {
    double mu_hat[D];
    double kappa, rho, warmth_vmf, mu_se;
    int n;
    int saturated;
} Fit;

/* Returns 1 on success, 0 when unidentifiable/isotropic (never a fake number). */
static int vmf_fit(const double zs[][D], int n, const double warm[D], Fit *out) {
    if (n < NMIN) return 0;
    /* 2. defensive renormalization */
    double rows[MAXN][D];
    for (int i = 0; i < n; i++) {
        double nrm = norm7(zs[i]);
        for (int j = 0; j < D; j++) rows[i][j] = zs[i][j] / nrm;
    }
    /* 3. mean resultant */
    double r[D] = {0};
    for (int i = 0; i < n; i++)
        for (int j = 0; j < D; j++) r[j] += rows[i][j] / n;
    double rho = norm7(r);
    if (rho > RHOMAX) rho = RHOMAX;
    if (rho < 1e-12) return 0; /* isotropic — no mean direction */
    /* 4. mean direction */
    for (int j = 0; j < D; j++) out->mu_hat[j] = r[j] / rho;
    /* 5. Banerjee init, clipped */
    double kappa = clip(rho * (D - rho * rho) / (1.0 - rho * rho), 1e-6, KMAX);
    /* 6. Newton solve on A7(kappa) = rho */
    for (int it = 0; it < 60; it++) {
        double a = a7(kappa);
        double g = 1.0 - a * a - (D - 1) * a / kappa;
        double step = (a - rho) / g;
        kappa = clip(kappa - step, 1e-6, KMAX);
        if (fabs(g) < 1e-12 || fabs(step) < 1e-9) break;
    }
    out->kappa = kappa;
    out->rho = rho;
    out->n = n;
    /* 7. warmth */
    double w = 0.0;
    for (int j = 0; j < D; j++) w += warm[j] * out->mu_hat[j];
    out->warmth_vmf = w;
    /* 8. jackknife SE(mu_hat): leave-one-out mean directions, renormalized */
    double jks[MAXN][D], jm[D] = {0};
    for (int i = 0; i < n; i++) {
        double m[D] = {0};
        for (int j = 0; j < n; j++) {
            if (j == i) continue;
            for (int d = 0; d < D; d++) m[d] += rows[j][d] / (n - 1);
        }
        double nm = norm7(m);
        for (int d = 0; d < D; d++) jks[i][d] = m[d] / nm;
    }
    for (int i = 0; i < n; i++)
        for (int d = 0; d < D; d++) jm[d] += jks[i][d] / n;
    double acc = 0.0;
    for (int i = 0; i < n; i++) {
        double s = 0.0;
        for (int d = 0; d < D; d++) {
            double diff = jks[i][d] - jm[d];
            s += diff * diff;
        }
        acc += s;
    }
    out->mu_se = sqrt((double)(n - 1) / n * acc);
    /* 9. saturation flag */
    out->saturated = (rho >= RHOMAX || kappa >= KMAX);
    return 1;
}

/* ---------- SPEC §3: edge ---------- */
static void edge(const Fit *fb, const Fit *fa,
                 double *d_mu, double *d_warmth, double *d_log_kappa, int *real) {
    double diff[D];
    for (int j = 0; j < D; j++) diff[j] = fa->mu_hat[j] - fb->mu_hat[j];
    *d_mu = norm7(diff);
    *d_warmth = fa->warmth_vmf - fb->warmth_vmf;
    *d_log_kappa = log(fa->kappa / fb->kappa);
    double mx = fb->mu_se > fa->mu_se ? fb->mu_se : fa->mu_se;
    *real = *d_mu > 2.0 * mx; /* db_factor = 2.0 */
}

/* ---------- minimal JSON number extraction (libc only) ---------- */
/* Finds the first occurrence of "key" and scans `count` float literals after it. */
static void numbers_after(const char *text, const char *key, double *out, int count) {
    char pat[128];
    snprintf(pat, sizeof pat, "\"%s\"", key);
    const char *p = strstr(text, pat);
    if (!p) { fprintf(stderr, "key %s not found\n", key); exit(1); }
    p += strlen(pat);
    for (int i = 0; i < count; i++) {
        while (*p && !(isdigit((unsigned char)*p) || *p == '-' || *p == '+')) p++;
        char *end = NULL;
        out[i] = strtod(p, &end);
        if (end == p) { fprintf(stderr, "bad number after key %s\n", key); exit(1); }
        p = end;
    }
}

static char *read_file(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) { fprintf(stderr, "cannot read %s\n", path); exit(1); }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *buf = malloc((size_t)sz + 1);
    if (fread(buf, 1, (size_t)sz, f) != (size_t)sz) { fprintf(stderr, "read error %s\n", path); exit(1); }
    buf[sz] = '\0';
    fclose(f);
    return buf;
}

/* ---------- SPEC §4: differential test ---------- */
static int failures = 0;
static void check(const char *name, double got, double want, double tol) {
    double err = fabs(got - want);
    if (err > tol) {
        printf("FAIL %s: got %.12f want %.12f (err %.3e > %g)\n", name, got, want, err, tol);
        failures++;
    } else {
        printf("ok   %s: %.12f (err %.3e)\n", name, got, err);
    }
}

int main(void) {
    char *golden = read_file("../golden.json");
    char *inputs = read_file("../inputs.json");

    /* --- A7 --- */
    double kappas[11], values[11];
    numbers_after(golden, "kappas", kappas, 11);
    numbers_after(golden, "values", values, 11);
    for (int i = 0; i < 11; i++) {
        char name[64];
        snprintf(name, sizeof name, "A7(%g)", kappas[i]);
        check(name, a7(kappas[i]), values[i], 1e-9);
    }

    /* --- inputs --- */
    double flat[30 * D];
    numbers_after(inputs, "z", flat, 30 * D);
    double zs[30][D];
    for (int i = 0; i < 30; i++)
        for (int j = 0; j < D; j++) zs[i][j] = flat[i * D + j];
    double warm[D];
    numbers_after(golden, "WARM", warm, D);

    /* --- vmf_fit on zs --- */
    Fit fb;
    if (!vmf_fit((const double (*)[D])zs, 30, warm, &fb)) {
        printf("FAIL vmf_fit returned unidentifiable on golden input\n");
        return 1;
    }
    double g_kappa, g_rho, g_warmth, g_mu_se, g_mu[D];
    numbers_after(golden, "kappa", &g_kappa, 1);
    numbers_after(golden, "rho", &g_rho, 1);
    numbers_after(golden, "warmth_vmf", &g_warmth, 1);
    numbers_after(golden, "mu_se", &g_mu_se, 1);
    numbers_after(golden, "mu_hat", g_mu, D);

    check("kappa", fb.kappa, g_kappa, 1e-6);
    check("rho", fb.rho, g_rho, 1e-6);
    check("warmth_vmf", fb.warmth_vmf, g_warmth, 1e-6);
    check("mu_se", fb.mu_se, g_mu_se, 1e-6);
    double mu_err = 0.0;
    for (int j = 0; j < D; j++) {
        double e = fabs(fb.mu_hat[j] - g_mu[j]);
        if (e > mu_err) mu_err = e;
    }
    if (mu_err > 1e-6) { printf("FAIL mu_hat: max abs err %.3e\n", mu_err); failures++; }
    else printf("ok   mu_hat: max abs err %.3e\n", mu_err);
    if (fb.n != 30) { printf("FAIL n: %d != 30\n", fb.n); failures++; }
    else printf("ok   n == 30\n");
    if (fb.saturated) { printf("FAIL saturated: expected false\n"); failures++; }
    else printf("ok   saturated == false\n");

    /* --- edge: second fit on zs + 0.05 element-wise (SPEC §4) --- */
    double zs2[30][D];
    for (int i = 0; i < 30; i++)
        for (int j = 0; j < D; j++) zs2[i][j] = zs[i][j] + 0.05;
    Fit fa;
    if (!vmf_fit((const double (*)[D])zs2, 30, warm, &fa)) {
        printf("FAIL vmf_fit returned unidentifiable on shifted input\n");
        return 1;
    }
    double d_mu, d_warmth, d_log_kappa, g_dmu, g_dw, g_dlk;
    int real;
    edge(&fb, &fa, &d_mu, &d_warmth, &d_log_kappa, &real);
    numbers_after(golden, "d_mu", &g_dmu, 1);
    numbers_after(golden, "d_warmth", &g_dw, 1);
    numbers_after(golden, "d_log_kappa", &g_dlk, 1);
    check("edge.d_mu", d_mu, g_dmu, 1e-6);
    check("edge.d_warmth", d_warmth, g_dw, 1e-6);
    check("edge.d_log_kappa", d_log_kappa, g_dlk, 1e-6);
    if (real) { printf("FAIL edge.real: expected false\n"); failures++; }
    else printf("ok   edge.real == false\n");

    printf("\n");
    printf("actual values: kappa=%.6f rho=%.6f warmth=%.6f\n", fb.kappa, fb.rho, fb.warmth_vmf);
    printf("golden values: kappa=%.6f rho=%.6f warmth=%.6f\n", g_kappa, g_rho, g_warmth);

    if (failures == 0) printf("PASS: all differential checks within SPEC §4 tolerances\n");
    else printf("FAIL: %d check(s) failed\n", failures);
    free(golden);
    free(inputs);
    return failures == 0 ? 0 : 1;
}
