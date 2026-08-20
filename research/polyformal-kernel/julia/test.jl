# Polyformal vMF kernel — Julia differential test.
#
# Reads ../golden.json + ../inputs.json and asserts SPEC §4 tolerances:
#   A7 ≤ 1e-9; fit values ≤ 1e-6; edge ≤ 1e-6; n == 30; saturated == false; real == false.
# The second fit in `edge` is vmf_fit on zs + 0.05 element-wise (SPEC §4).
#
# No JSON package is required: golden.json/inputs.json are flat, so the test
# extracts numbers with a tiny regex scanner (Base only, same approach as the
# C++ port). If JSON.jl is installed, `using JSON` would also work.
#
# Run:  julia test.jl   (from julia/)

using Printf

include(joinpath(@__DIR__, "vmf_kernel.jl"))

# ---------- minimal JSON number extraction (Base only) ----------
function numbers_after(text::AbstractString, key::AbstractString, count::Int)
    m = findfirst("\"" * key * "\"", text)
    m === nothing && error("key not found: \"$key\"")
    rest = text[nextind(text, last(m)):end]
    out = Float64[]
    for mm in eachmatch(r"-?[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?", rest)
        push!(out, parse(Float64, mm.match))
        length(out) == count && break
    end
    length(out) == count || error("found $(length(out)) number(s) after \"$key\", wanted $count")
    out
end

const GOLDEN = read(joinpath(@__DIR__, "..", "golden.json"), String)
const INPUTS = read(joinpath(@__DIR__, "..", "inputs.json"), String)

failures = 0
function check(name::AbstractString, got::Float64, want::Float64, tol::Float64)
    err = abs(got - want)
    if err > tol
        @printf("FAIL %s: got %.12f want %.12f (err %.3e > %g)\n", name, got, want, err, tol)
        global failures += 1
    else
        @printf("ok   %s: %.12f (err %.3e)\n", name, got, err)
    end
end

# ---------- A7 ----------
kappas = numbers_after(GOLDEN, "kappas", 11)
values = numbers_after(GOLDEN, "values", 11)
for i in 1:11
    check("A7($(kappas[i]))", a7(kappas[i]), values[i], 1e-9)
end

# ---------- inputs ----------
flat = numbers_after(INPUTS, "z", 30 * D)
zs = [flat[(i - 1) * D + 1:i * D] for i in 1:30]
warm = numbers_after(GOLDEN, "WARM", D)

# ---------- vmf_fit on zs ----------
fb = vmf_fit(zs, warm)
if fb === nothing
    println("FAIL vmf_fit returned nothing on golden input")
    exit(1)
end
g_kappa = numbers_after(GOLDEN, "kappa", 1)[1]
g_rho = numbers_after(GOLDEN, "rho", 1)[1]
g_warmth = numbers_after(GOLDEN, "warmth_vmf", 1)[1]
g_mu_se = numbers_after(GOLDEN, "mu_se", 1)[1]
g_mu = numbers_after(GOLDEN, "mu_hat", D)

check("kappa", fb.kappa, g_kappa, 1e-6)
check("rho", fb.rho, g_rho, 1e-6)
check("warmth_vmf", fb.warmth_vmf, g_warmth, 1e-6)
check("mu_se", fb.mu_se, g_mu_se, 1e-6)
mu_err = maximum(abs.(fb.mu_hat .- g_mu))
if mu_err > 1e-6
    @printf("FAIL mu_hat: max abs err %.3e\n", mu_err)
    global failures += 1
else
    @printf("ok   mu_hat: max abs err %.3e\n", mu_err)
end
if fb.n != 30
    println("FAIL n: $(fb.n) != 30")
    global failures += 1
else
    println("ok   n == 30")
end
if fb.saturated
    println("FAIL saturated: expected false")
    global failures += 1
else
    println("ok   saturated == false")
end

# ---------- edge: second fit on zs + 0.05 element-wise ----------
zs2 = [[x + 0.05 for x in row] for row in zs]
fa = vmf_fit(zs2, warm)
if fa === nothing
    println("FAIL vmf_fit returned nothing on shifted input")
    exit(1)
end
e = edge(fb, fa)
check("edge.d_mu", e.d_mu, numbers_after(GOLDEN, "d_mu", 1)[1], 1e-6)
check("edge.d_warmth", e.d_warmth, numbers_after(GOLDEN, "d_warmth", 1)[1], 1e-6)
check("edge.d_log_kappa", e.d_log_kappa, numbers_after(GOLDEN, "d_log_kappa", 1)[1], 1e-6)
if e.real
    println("FAIL edge.real: expected false")
    global failures += 1
else
    println("ok   edge.real == false")
end

# ---------- summary ----------
println()
@printf("actual values: kappa=%.6f rho=%.6f warmth=%.6f\n", fb.kappa, fb.rho, fb.warmth_vmf)
@printf("golden values: kappa=%.6f rho=%.6f warmth=%.6f\n", g_kappa, g_rho, g_warmth)

if failures == 0
    println("PASS: all differential checks within SPEC §4 tolerances")
    exit(0)
else
    @printf("FAIL: %d check(s) failed\n", failures)
    exit(1)
end
