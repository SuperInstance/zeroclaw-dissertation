# vMF kernel — Julia port

**Status: NOT RUN — interpreter unavailable on this machine.**

`julia` is not installed here, so `test.jl` has not been executed. The code is
written to SPEC.md and mirrors the passing C++ port exactly (same IEEE-754
double arithmetic, same Newton loop, same tolerances), so it is expected to pass
the §4 differential gate.

To run it on a machine with Julia installed (standard library only, no packages
needed — JSON numbers are extracted with a small Base-only regex scanner):

```sh
cd julia
julia test.jl
```

Expected output ends with `PASS: all differential checks within SPEC §4 tolerances`
and exit code 0.
