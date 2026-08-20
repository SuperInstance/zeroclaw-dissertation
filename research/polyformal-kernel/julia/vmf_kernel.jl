# Polyformal vMF kernel — Julia port (standard library only).
#
# Implements the three functions of SPEC.md:
#   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
#   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
#   edge      — field step between two fits
#
# No numpy/scipy, no external vMF/Bessel libraries — sinh/cosh + Newton, Base only.
# Differential test: test.jl (reads ../golden.json + ../inputs.json).
#
# Run:  julia test.jl   (from julia/)

const D = 7                # dimension of the field space (S^6 ⊂ R^7)
const KMAX = 500.0         # κ saturation cap
const NMIN = 10            # below this many windows, κ is not identifiable
const RHOMAX = 0.999       # ρ clamp (unclipped Banerjee init overflows sinh)

# ---------- SPEC §1: A7 ----------
function a7(k::Float64)
    # Leading Taylor term: the closed form catastrophically cancels for small κ.
    k < 0.5 && return k / 7.0
    s = sinh(k)
    c = cosh(k)
    k2 = k * k
    ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s) /
    ((1.0 + 3.0 / k2) * s - (3.0 / k) * c)
end

clip(x::Float64, lo::Float64, hi::Float64) = min(max(x, lo), hi)

norm2(v::AbstractVector{Float64}) = sqrt(sum(abs2, v))

# ---------- SPEC §2: vmf_fit ----------
# zs: n×7 matrix (Vector of 7-vectors); warm: the fixed 7-vector WARM from golden.json.
# Returns a NamedTuple fit, or nothing when unidentifiable/isotropic — never a fake number.
function vmf_fit(zs::Vector{Vector{Float64}}, warm::Vector{Float64})
    n = length(zs)
    n < NMIN && return nothing

    # 2. defensive renormalization (inputs should already be unit)
    rows = [row ./ norm2(row) for row in zs]

    # 3. mean resultant
    r = zeros(Float64, D)
    for row in rows
        r .+= row ./ n
    end
    rho = min(norm2(r), RHOMAX)
    rho < 1e-12 && return nothing          # isotropic — no mean direction

    # 4. mean direction
    mu_hat = r ./ rho

    # 5. Banerjee et al. init, clipped to [1e-6, KMAX]
    kappa = clip(rho * (D - rho^2) / (1.0 - rho^2), 1e-6, KMAX)

    # 6. Newton solve on A7(kappa) = rho, with g = 1 - A7² - (D-1)·A7/κ
    for _ in 1:60
        a = a7(kappa)
        g = 1.0 - a^2 - (D - 1) * a / kappa
        step = (a - rho) / g
        kappa = clip(kappa - step, 1e-6, KMAX)
        (abs(g) < 1e-12 || abs(step) < 1e-9) && break
    end

    # 7. warmth = WARM · μ̂
    warmth_vmf = sum(warm .* mu_hat)

    # 8. jackknife SE(μ̂): leave-one-out mean directions, renormalized
    jks = Vector{Vector{Float64}}(undef, n)
    for i in 1:n
        m = zeros(Float64, D)
        for j in 1:n
            j == i && continue
            m .+= rows[j] ./ (n - 1)
        end
        jks[i] = m ./ norm2(m)
    end
    jm = sum(jks) ./ n
    acc = sum(sum(abs2, jk .- jm) for jk in jks)
    mu_se = sqrt((n - 1) / n * acc)

    # 9. saturation flag
    saturated = rho >= RHOMAX || kappa >= KMAX

    (; mu_hat, kappa, rho, n, warmth_vmf, mu_se, saturated)
end

# ---------- SPEC §3: edge ----------
function edge(fb, fa)
    d_mu = norm2(fa.mu_hat .- fb.mu_hat)
    d_warmth = fa.warmth_vmf - fb.warmth_vmf
    d_log_kappa = log(fa.kappa / fb.kappa)
    # db_factor = 2.0 — the drift deadband
    (; d_mu, d_warmth, d_log_kappa, real = d_mu > 2.0 * max(fb.mu_se, fa.mu_se))
end
