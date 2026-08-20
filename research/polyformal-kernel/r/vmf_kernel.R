# Polyformal vMF kernel — R port (base R only, no packages).
#
# Implements the three functions of SPEC.md:
#   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
#   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
#   edge      — field step between two fits
#
# No numpy/scipy, no external vMF/Bessel libraries — sinh/cosh + Newton, base R only.
# Differential test: test.R (reads ../golden.json + ../inputs.json).
#
# Run:  Rscript test.R   (from r/)

D      <- 7        # dimension of the field space (S^6 ⊂ R^7)
KMAX   <- 500.0    # kappa saturation cap
NMIN   <- 10       # below this many windows, kappa is not identifiable
RHOMAX <- 0.999    # rho clamp (unclipped Banerjee init overflows sinh)

# ---------- SPEC §1: A7 ----------
a7 <- function(k) {
  # Leading Taylor term: the closed form catastrophically cancels for small kappa.
  if (k < 0.5) return(k / 7.0)
  s <- sinh(k)
  c <- cosh(k)
  k2 <- k * k
  ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s) /
    ((1.0 + 3.0 / k2) * s - (3.0 / k) * c)
}

clip <- function(x, lo, hi) min(max(x, lo), hi)

norm2 <- function(v) sqrt(sum(v * v))

# ---------- SPEC §2: vmf_fit ----------
# zs: n×7 matrix; warm: the fixed 7-vector WARM from golden.json.
# Returns a list fit, or NULL when unidentifiable/isotropic — never a fake number.
vmf_fit <- function(zs, warm) {
  n <- nrow(zs)
  if (n < NMIN) return(NULL)

  # 2. defensive renormalization (inputs should already be unit)
  rows <- t(apply(zs, 1, function(row) row / norm2(row)))

  # 3. mean resultant
  r <- colMeans(rows)
  rho <- min(norm2(r), RHOMAX)
  if (rho < 1e-12) return(NULL)  # isotropic — no mean direction

  # 4. mean direction
  mu_hat <- r / rho

  # 5. Banerjee et al. init, clipped to [1e-6, KMAX]
  kappa <- clip(rho * (D - rho^2) / (1.0 - rho^2), 1e-6, KMAX)

  # 6. Newton solve on A7(kappa) = rho, with g = 1 - A7^2 - (D-1)*A7/kappa
  for (it in 1:60) {
    a <- a7(kappa)
    g <- 1.0 - a^2 - (D - 1) * a / kappa
    step <- (a - rho) / g
    kappa <- clip(kappa - step, 1e-6, KMAX)
    if (abs(g) < 1e-12 || abs(step) < 1e-9) break
  }

  # 7. warmth = WARM %*% mu_hat
  warmth_vmf <- sum(warm * mu_hat)

  # 8. jackknife SE(mu_hat): leave-one-out mean directions, renormalized
  jks <- matrix(0, n, D)
  for (i in seq_len(n)) {
    m <- colSums(rows[-i, , drop = FALSE]) / (n - 1)
    jks[i, ] <- m / norm2(m)
  }
  jm <- colMeans(jks)
  acc <- sum((jks - matrix(jm, nrow = n, ncol = D, byrow = TRUE))^2)
  mu_se <- sqrt((n - 1) / n * acc)

  # 9. saturation flag
  saturated <- rho >= RHOMAX || kappa >= KMAX

  list(mu_hat = mu_hat, kappa = kappa, rho = rho, n = n,
       warmth_vmf = warmth_vmf, mu_se = mu_se, saturated = saturated)
}

# ---------- SPEC §3: edge ----------
edge <- function(fb, fa) {
  d_mu <- norm2(fa$mu_hat - fb$mu_hat)
  d_warmth <- fa$warmth_vmf - fb$warmth_vmf
  d_log_kappa <- log(fa$kappa / fb$kappa)
  # db_factor = 2.0 — the drift deadband
  real <- d_mu > 2.0 * max(fb$mu_se, fa$mu_se)
  list(d_mu = d_mu, d_warmth = d_warmth, d_log_kappa = d_log_kappa, real = real)
}
