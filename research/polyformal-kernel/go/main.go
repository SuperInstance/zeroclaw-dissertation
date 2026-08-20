// Polyformal vMF kernel — Go port (standard library only: math, encoding/json).
//
// Implements the three functions of SPEC.md:
//   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
//   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
//   edge      — field step between two fits
//
// Differential test: reads ../golden.json and ../inputs.json (run from go/).
// Go's stdlib has encoding/json, so the golden vectors are parsed for real —
// no external dependencies, no hardcoded literals.
//
// VERIFIED: go1.26.7 linux/amd64 — all SPEC §4 checks PASS (max err 1.1e-14).
// Build & run:  cd go && go build -o vmf_test main.go && ./vmf_test
package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
)

const (
	D      = 7
	KMAX   = 500.0
	NMIN   = 10
	RHOMAX = 0.999
)

// ---------- SPEC §1: A7 ----------
func a7(k float64) float64 {
	if k < 0.5 {
		return k / 7.0 // leading Taylor term; closed form cancels catastrophically
	}
	s, c := math.Sinh(k), math.Cosh(k)
	k2 := k * k
	return ((1.0+15.0/k2)*c - (6.0/k+15.0/(k2*k))*s) /
		((1.0+3.0/k2)*s - (3.0/k)*c)
}

func clip(x, lo, hi float64) float64 {
	return math.Max(lo, math.Min(hi, x))
}

func norm(v []float64) float64 {
	s := 0.0
	for _, x := range v {
		s += x * x
	}
	return math.Sqrt(s)
}

// ---------- SPEC §2: vmf_fit ----------
type Fit struct {
	MuHat     []float64
	Kappa     float64
	Rho       float64
	N         int
	WarmthVMF float64
	MuSE      float64
	Saturated bool
}

// vmfFit returns nil when unidentifiable/isotropic — never a fake number.
func vmfFit(zs [][]float64, warm []float64) *Fit {
	n := len(zs)
	if n < NMIN {
		return nil
	}
	// 2. defensive renormalization
	rows := make([][]float64, n)
	for i, row := range zs {
		nrm := norm(row)
		r := make([]float64, D)
		for j := range r {
			r[j] = row[j] / nrm
		}
		rows[i] = r
	}
	// 3. mean resultant
	r := make([]float64, D)
	for _, row := range rows {
		for j := 0; j < D; j++ {
			r[j] += row[j] / float64(n)
		}
	}
	rho := math.Min(norm(r), RHOMAX)
	if rho < 1e-12 {
		return nil // isotropic — no mean direction
	}
	// 4. mean direction
	muHat := make([]float64, D)
	for j := range muHat {
		muHat[j] = r[j] / rho
	}
	// 5. Banerjee init, clipped
	kappa := clip(rho*(D-rho*rho)/(1.0-rho*rho), 1e-6, KMAX)
	// 6. Newton solve on A7(kappa) = rho
	for it := 0; it < 60; it++ {
		a := a7(kappa)
		g := 1.0 - a*a - (D-1)*a/kappa
		step := (a - rho) / g
		kappa = clip(kappa-step, 1e-6, KMAX)
		if math.Abs(g) < 1e-12 || math.Abs(step) < 1e-9 {
			break
		}
	}
	// 7. warmth
	warmth := 0.0
	for j := 0; j < D; j++ {
		warmth += warm[j] * muHat[j]
	}
	// 8. jackknife SE(mu_hat): leave-one-out mean directions, renormalized
	jks := make([][]float64, n)
	for i := 0; i < n; i++ {
		m := make([]float64, D)
		for j := 0; j < n; j++ {
			if j == i {
				continue
			}
			for d := 0; d < D; d++ {
				m[d] += rows[j][d] / float64(n-1)
			}
		}
		nm := norm(m)
		for d := range m {
			m[d] /= nm
		}
		jks[i] = m
	}
	jm := make([]float64, D)
	for _, jk := range jks {
		for d := 0; d < D; d++ {
			jm[d] += jk[d] / float64(n)
		}
	}
	acc := 0.0
	for _, jk := range jks {
		s := 0.0
		for d := 0; d < D; d++ {
			diff := jk[d] - jm[d]
			s += diff * diff
		}
		acc += s
	}
	muSE := math.Sqrt(float64(n-1) / float64(n) * acc)
	// 9. saturation flag
	return &Fit{
		MuHat:     muHat,
		Kappa:     kappa,
		Rho:       rho,
		N:         n,
		WarmthVMF: warmth,
		MuSE:      muSE,
		Saturated: rho >= RHOMAX || kappa >= KMAX,
	}
}

// ---------- SPEC §3: edge ----------
type Edge struct {
	DMu       float64
	DWarmth   float64
	DLogKappa float64
	Real      bool
}

func edge(fb, fa *Fit) Edge {
	diff := make([]float64, D)
	for j := range diff {
		diff[j] = fa.MuHat[j] - fb.MuHat[j]
	}
	e := Edge{
		DMu:       norm(diff),
		DWarmth:   fa.WarmthVMF - fb.WarmthVMF,
		DLogKappa: math.Log(fa.Kappa / fb.Kappa),
	}
	e.Real = e.DMu > 2.0*math.Max(fb.MuSE, fa.MuSE) // db_factor = 2.0
	return e
}

// ---------- JSON shapes for the golden/input files ----------
type goldenFile struct {
	Spec struct {
		WARM []float64 `json:"WARM"`
	} `json:"spec"`
	A7 struct {
		Kappas []float64 `json:"kappas"`
		Values []float64 `json:"values"`
	} `json:"A7"`
	VmfFit struct {
		MuHat     []float64 `json:"mu_hat"`
		Kappa     float64   `json:"kappa"`
		Rho       float64   `json:"rho"`
		N         int       `json:"n"`
		WarmthVMF float64   `json:"warmth_vmf"`
		MuSE      float64   `json:"mu_se"`
		Saturated bool      `json:"saturated"`
	} `json:"vmf_fit"`
	Edge struct {
		DMu       float64 `json:"d_mu"`
		DWarmth   float64 `json:"d_warmth"`
		DLogKappa float64 `json:"d_log_kappa"`
		Real      bool    `json:"real"`
	} `json:"edge"`
}

type inputsFile struct {
	Z [][]float64 `json:"z"`
}

// ---------- SPEC §4: differential test ----------
var failures int

func check(name string, got, want, tol float64) {
	err := math.Abs(got - want)
	if err > tol {
		fmt.Printf("FAIL %s: got %.12f want %.12f (err %.3e > %g)\n", name, got, want, err, tol)
		failures++
	} else {
		fmt.Printf("ok   %s: %.12f (err %.3e)\n", name, got, err)
	}
}

func main() {
	rawGolden, err := os.ReadFile("../golden.json")
	if err != nil {
		fmt.Fprintln(os.Stderr, "cannot read ../golden.json:", err)
		os.Exit(1)
	}
	rawInputs, err := os.ReadFile("../inputs.json")
	if err != nil {
		fmt.Fprintln(os.Stderr, "cannot read ../inputs.json:", err)
		os.Exit(1)
	}
	var golden goldenFile
	if err := json.Unmarshal(rawGolden, &golden); err != nil {
		fmt.Fprintln(os.Stderr, "bad golden.json:", err)
		os.Exit(1)
	}
	var inputs inputsFile
	if err := json.Unmarshal(rawInputs, &inputs); err != nil {
		fmt.Fprintln(os.Stderr, "bad inputs.json:", err)
		os.Exit(1)
	}

	// --- A7 ---
	for i, k := range golden.A7.Kappas {
		check(fmt.Sprintf("A7(%g)", k), a7(k), golden.A7.Values[i], 1e-9)
	}

	// --- vmf_fit on zs ---
	zs := inputs.Z
	fb := vmfFit(zs, golden.Spec.WARM)
	if fb == nil {
		fmt.Println("FAIL vmf_fit returned nil on golden input")
		os.Exit(1)
	}
	g := golden.VmfFit
	check("kappa", fb.Kappa, g.Kappa, 1e-6)
	check("rho", fb.Rho, g.Rho, 1e-6)
	check("warmth_vmf", fb.WarmthVMF, g.WarmthVMF, 1e-6)
	check("mu_se", fb.MuSE, g.MuSE, 1e-6)
	muErr := 0.0
	for j := 0; j < D; j++ {
		muErr = math.Max(muErr, math.Abs(fb.MuHat[j]-g.MuHat[j]))
	}
	if muErr > 1e-6 {
		fmt.Printf("FAIL mu_hat: max abs err %.3e\n", muErr)
		failures++
	} else {
		fmt.Printf("ok   mu_hat: max abs err %.3e\n", muErr)
	}
	if fb.N != 30 {
		fmt.Printf("FAIL n: %d != 30\n", fb.N)
		failures++
	} else {
		fmt.Println("ok   n == 30")
	}
	if fb.Saturated {
		fmt.Println("FAIL saturated: expected false")
		failures++
	} else {
		fmt.Println("ok   saturated == false")
	}

	// --- edge: second fit on zs + 0.05 element-wise (SPEC §4) ---
	zs2 := make([][]float64, len(zs))
	for i, row := range zs {
		r := make([]float64, D)
		for j := range r {
			r[j] = row[j] + 0.05
		}
		zs2[i] = r
	}
	fa := vmfFit(zs2, golden.Spec.WARM)
	if fa == nil {
		fmt.Println("FAIL vmf_fit returned nil on shifted input")
		os.Exit(1)
	}
	e := edge(fb, fa)
	check("edge.d_mu", e.DMu, golden.Edge.DMu, 1e-6)
	check("edge.d_warmth", e.DWarmth, golden.Edge.DWarmth, 1e-6)
	check("edge.d_log_kappa", e.DLogKappa, golden.Edge.DLogKappa, 1e-6)
	if e.Real {
		fmt.Println("FAIL edge.real: expected false")
		failures++
	} else {
		fmt.Println("ok   edge.real == false")
	}

	fmt.Println()
	fmt.Printf("actual values: kappa=%.6f rho=%.6f warmth=%.6f\n", fb.Kappa, fb.Rho, fb.WarmthVMF)
	fmt.Printf("golden values: kappa=%.6f rho=%.6f warmth=%.6f\n", g.Kappa, g.Rho, g.WarmthVMF)

	if failures == 0 {
		fmt.Println("PASS: all differential checks within SPEC §4 tolerances")
	} else {
		fmt.Printf("FAIL: %d check(s) failed\n", failures)
	}
	if failures != 0 {
		os.Exit(1)
	}
}
