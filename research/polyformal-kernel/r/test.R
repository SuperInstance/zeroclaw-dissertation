# Polyformal vMF kernel — R differential test.
#
# Reads ../golden.json + ../inputs.json and asserts SPEC §4 tolerances:
#   A7 <= 1e-9; fit values <= 1e-6; edge <= 1e-6; n == 30; saturated == false; real == false.
# The second fit in `edge` is vmf_fit on zs + 0.05 element-wise (SPEC §4).
#
# No jsonlite dependency: golden.json/inputs.json are flat, so numbers are
# extracted with a small base-R regex scanner (same approach as the C++ port).
# If jsonlite is installed, jsonlite::fromJSON() would work identically.
#
# Run:  Rscript test.R   (from r/)

source("vmf_kernel.R")

# ---------- minimal JSON number extraction (base R only) ----------
numbers_after <- function(text, key, count) {
  pat <- sprintf('"%s"', key)
  m <- regexpr(pat, text, fixed = TRUE)
  if (m < 0) stop("key not found: ", key)
  rest <- substr(text, m + attr(m, "match.length"), nchar(text))
  nums <- regmatches(rest, gregexpr("-?[0-9]+(\\.[0-9]+)?([eE][-+]?[0-9]+)?", rest))[[1]]
  if (length(nums) < count) stop("found ", length(nums), " number(s) after \"", key, "\", wanted ", count)
  as.numeric(nums[seq_len(count)])
}

golden <- paste(readLines("../golden.json", warn = FALSE), collapse = "\n")
inputs <- paste(readLines("../inputs.json", warn = FALSE), collapse = "\n")

failures <- 0L
check <- function(name, got, want, tol) {
  err <- abs(got - want)
  if (err > tol) {
    cat(sprintf("FAIL %s: got %.12f want %.12f (err %.3e > %g)\n", name, got, want, err, tol))
    failures <<- failures + 1L
  } else {
    cat(sprintf("ok   %s: %.12f (err %.3e)\n", name, got, err))
  }
}

# ---------- A7 ----------
kappas <- numbers_after(golden, "kappas", 11)
values <- numbers_after(golden, "values", 11)
for (i in seq_along(kappas)) {
  check(sprintf("A7(%g)", kappas[i]), a7(kappas[i]), values[i], 1e-9)
}

# ---------- inputs ----------
flat <- numbers_after(inputs, "z", 30 * D)
zs <- matrix(flat, nrow = 30, ncol = D, byrow = TRUE)
warm <- numbers_after(golden, "WARM", D)

# ---------- vmf_fit on zs ----------
fb <- vmf_fit(zs, warm)
if (is.null(fb)) {
  cat("FAIL vmf_fit returned NULL on golden input\n")
  quit(status = 1)
}
g_kappa <- numbers_after(golden, "kappa", 1)
g_rho <- numbers_after(golden, "rho", 1)
g_warmth <- numbers_after(golden, "warmth_vmf", 1)
g_mu_se <- numbers_after(golden, "mu_se", 1)
g_mu <- numbers_after(golden, "mu_hat", D)

check("kappa", fb$kappa, g_kappa, 1e-6)
check("rho", fb$rho, g_rho, 1e-6)
check("warmth_vmf", fb$warmth_vmf, g_warmth, 1e-6)
check("mu_se", fb$mu_se, g_mu_se, 1e-6)
mu_err <- max(abs(fb$mu_hat - g_mu))
if (mu_err > 1e-6) {
  cat(sprintf("FAIL mu_hat: max abs err %.3e\n", mu_err))
  failures <- failures + 1L
} else {
  cat(sprintf("ok   mu_hat: max abs err %.3e\n", mu_err))
}
if (fb$n != 30) {
  cat(sprintf("FAIL n: %d != 30\n", fb$n))
  failures <- failures + 1L
} else {
  cat("ok   n == 30\n")
}
if (fb$saturated) {
  cat("FAIL saturated: expected false\n")
  failures <- failures + 1L
} else {
  cat("ok   saturated == false\n")
}

# ---------- edge: second fit on zs + 0.05 element-wise ----------
zs2 <- zs + 0.05
fa <- vmf_fit(zs2, warm)
if (is.null(fa)) {
  cat("FAIL vmf_fit returned NULL on shifted input\n")
  quit(status = 1)
}
e <- edge(fb, fa)
check("edge.d_mu", e$d_mu, numbers_after(golden, "d_mu", 1), 1e-6)
check("edge.d_warmth", e$d_warmth, numbers_after(golden, "d_warmth", 1), 1e-6)
check("edge.d_log_kappa", e$d_log_kappa, numbers_after(golden, "d_log_kappa", 1), 1e-6)
if (e$real) {
  cat("FAIL edge.real: expected false\n")
  failures <- failures + 1L
} else {
  cat("ok   edge.real == false\n")
}

# ---------- summary ----------
cat("\n")
cat(sprintf("actual values: kappa=%.6f rho=%.6f warmth=%.6f\n", fb$kappa, fb$rho, fb$warmth_vmf))
cat(sprintf("golden values: kappa=%.6f rho=%.6f warmth=%.6f\n", g_kappa, g_rho, g_warmth))

if (failures == 0) {
  cat("PASS: all differential checks within SPEC §4 tolerances\n")
  quit(status = 0)
} else {
  cat(sprintf("FAIL: %d check(s) failed\n", failures))
  quit(status = 1)
}
