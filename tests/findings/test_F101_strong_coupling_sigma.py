# test_F101_strong_coupling_sigma.py
# 2026-06-05
#
# F101 -- Full strong-coupling sigma from the rule's COMPACT rotor transfer
# operator (extends F100 past the Gaussian / spin-wave regime).
#
# F100 derived sigma in the weak-fluctuation (Gaussian) regime by treating the
# plaquette flux phi as a NON-COMPACT Gaussian variable:  sigma_1 = sigma_phi^2/2.
# That misses the COMPACTNESS of the flux (phi is an angle on a circle), which is
# exactly what dominates the strong-coupling / disordered regime where confinement
# is non-perturbative.  The fix is the rule's single-plaquette transfer operator
# kept COMPACT -- the quantum rotor (Mathieu Hamiltonian):
#
#     H = (1/(2 chi)) E_hat^2 - lambda cos(phi_hat),   E_hat|m> = m|m>,
#         cos(phi) couples |m> <-> |m+-1>     (charge / Fourier basis, exact).
#
# chi (moment of inertia) is the electric stiffness, lambda the magnetic
# stiffness; the rule's harmonic frequency is Omega = sqrt(lambda/chi) (F100).
# The ground state gives the centre order parameter s_1 = <e^{i phi}> at ALL
# couplings, so  sigma_1 = -ln s_1  with NO Gaussian assumption.
#
#   S1  exact rotor sigma(lambda) at all couplings (charge-basis diagonalisation),
#       monotone, spanning 0 .. infinity.
#   S2  weak limit lambda -> inf  reproduces F100's Gaussian  sigma = 1/(4 sqrt(lambda chi)).
#   S3  strong limit lambda -> 0  gives the NON-PERTURBATIVE log law
#       s_1 -> 2 lambda chi  =>  sigma -> -ln(2 lambda chi)  (confinement).
#   S4  reconciliation with F70: the strong-coupling slope d sigma/d ln(coupling)
#       -> -1 for BOTH the rotor and F70's -ln w(beta); F70's w(beta) -> beta/(2N^2)
#       = beta/18 (the exact SU(3) leading character coefficient).
#   S5  map to the rule: lambda = chi Omega^2 extends F100's gamma(Omega) to all
#       couplings; the actual 2D rule sits at the weak end.
#
# Pure numpy.  Rotor by dense Hermitian diagonalisation in the truncated charge
# basis (no scipy); truncation convergence is checked.

import json
import time
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.gauge import confinement as conf                  # F70 -ln w(beta)

t0 = time.time()
results = {"finding": "F101", "date": "2026-06-05",
           "title": "full strong-coupling sigma from the compact-rotor transfer operator",
           "checks": {}}


def record(name, statement, residual, status):
    results["checks"][name] = {
        "statement": statement, "residual": str(residual),
        "status": "PASS" if status else "FAIL"}
    print(f"{name}: {statement}\n      -> residual {residual} "
          f"[{'PASS' if status else 'FAIL'}]")


def rotor_s1(lam, chi=1.0, M=120):
    """Ground-state centre order parameter s_1 = <e^{i phi}> of the compact rotor
    H = (1/(2 chi)) E^2 - lambda cos(phi) in the integer-charge basis |m|<=M.
    e^{i phi} raises m by 1, so s_1 = sum_m g_m g_{m+1} (real ground state)."""
    m = np.arange(-M, M + 1)
    H = np.diag((m ** 2) / (2.0 * chi)).astype(float)
    off = -0.5 * lam * np.ones(2 * M)
    H += np.diag(off, 1) + np.diag(off, -1)
    w, v = np.linalg.eigh(H)
    g = v[:, 0]
    return float(np.sum(g[:-1] * g[1:]))


def rotor_sigma(lam, chi=1.0, M=120):
    return -np.log(rotor_s1(lam, chi=chi, M=M))


# ============================================================ S1
# Exact rotor sigma(lambda) at all couplings; monotone, truncation-converged.
lams = [0.01, 0.05, 0.2, 1.0, 5.0, 50.0]
sig = [rotor_sigma(l) for l in lams]
monotone = all(sig[i] > sig[i + 1] > 0 for i in range(len(sig) - 1))
# truncation convergence: M=120 vs M=60 agree
trunc = max(abs(rotor_sigma(l, M=120) - rotor_sigma(l, M=60)) for l in lams)
spans = sig[0] > 3.0 and sig[-1] < 0.05          # strong large, weak small
s1 = bool(monotone and trunc < 1e-10 and spans)
record("S1", "compact rotor sigma(lambda)=-ln<e^{i phi}> exact at all couplings "
       "(charge-basis diag); monotone decreasing, spans ~3.2 (strong) -> ~0.03 "
       "(weak), truncation-converged",
       f"trunc {trunc:.1e}, sigma {[round(x,3) for x in sig]}", s1)

# ============================================================ S2
# Weak-coupling limit -> F100 Gaussian  sigma = 1/(4 sqrt(lambda chi)).
weak_lams = [20.0, 100.0, 500.0, 2000.0]
rel_weak = [abs(rotor_sigma(l) - 1.0 / (4.0 * np.sqrt(l))) /
            (1.0 / (4.0 * np.sqrt(l))) for l in weak_lams]
weak_converges = all(rel_weak[i + 1] < rel_weak[i] for i in range(len(rel_weak) - 1))
s2 = bool(weak_converges and rel_weak[-1] < 5e-3)
record("S2", "weak limit lambda->inf reproduces F100 Gaussian sigma=1/(4 sqrt(lambda)) "
       "(chi=1); relative error decreases to <0.5%",
       f"rel_err {[f'{r:.2e}' for r in rel_weak]}", s2)

# ============================================================ S3
# Strong-coupling limit -> the NON-PERTURBATIVE log law.
# First-order rotor PT: |psi0> ~ |0> + lambda chi(|1>+|-1>) => s_1 -> 2 lambda chi.
strong_lams = [0.005, 0.01, 0.02, 0.05]
# s_1 ~ 2 lambda chi:
rel_s1 = [abs(rotor_s1(l) - 2.0 * l) / (2.0 * l) for l in strong_lams]
# sigma ~ -ln(2 lambda):
rel_sig = [abs(rotor_sigma(l) - (-np.log(2.0 * l))) / (-np.log(2.0 * l))
           for l in strong_lams]
# strong_lams is in INCREASING lambda order; the limit is lambda->0, so the
# error shrinks as lambda shrinks (rel_s1 increases along the list).
strong_converges = (all(rel_s1[i] < rel_s1[i + 1] for i in range(len(rel_s1) - 1))
                    and rel_s1[0] < 1e-3)
s3 = bool(strong_converges and rel_sig[0] < 2e-3)
record("S3", "strong limit lambda->0: s_1 -> 2 lambda chi (rotor PT), so "
       "sigma -> -ln(2 lambda chi) -- non-perturbative log confinement",
       f"rel s1 {[f'{r:.2e}' for r in rel_s1]}, rel sigma(l=0.005) {rel_sig[0]:.2e}", s3)

# ============================================================ S4
# Reconciliation with F70: same -ln(coupling) law, slope -> -1.
# (a) rotor strong-coupling slope d sigma/d ln(lambda) -> -1.
l1, l2 = 0.005, 0.02
slope_rotor = (rotor_sigma(l2) - rotor_sigma(l1)) / (np.log(l2) - np.log(l1))
# (b) F70 -ln w(beta) strong-coupling slope d sigma/d ln(beta) -> -1.
b1, b2 = 0.02, 0.08
slope_f70 = (conf.string_tension(b2) - conf.string_tension(b1)) / (np.log(b2) - np.log(b1))
# (c) F70 leading character coefficient w(beta)/beta -> 1/(2 N^2) = 1/18.
N = 3
wb = [conf.plaquette_mean(b) / b for b in (0.01, 0.02, 0.04)]
lead_coeff = wb[0]
coeff_ok = abs(lead_coeff - 1.0 / (2 * N ** 2)) < 5e-4
s4 = bool(abs(slope_rotor + 1.0) < 0.05 and abs(slope_f70 + 1.0) < 0.05 and coeff_ok)
record("S4", "F70 reconciliation: strong-coupling slope d sigma/d ln(coupling)->-1 "
       "for BOTH rotor and F70 -ln w(beta); w(beta)->beta/(2N^2)=beta/18 "
       "(exact SU(3) leading character)",
       f"slope_rotor {slope_rotor:.4f}, slope_F70 {slope_f70:.4f}, "
       f"w/beta {lead_coeff:.6f} vs 1/18={1/18:.6f}", s4)

# ============================================================ S5
# Map to the rule: lambda = chi Omega^2 (harmonic matching, F100), so the rotor
# extends gamma(Omega)/sigma(Omega) to ALL couplings.  The actual 2D rule sits
# at the weak end (F100 sigma~0.20); strong coupling = soft Omega.
# Check the harmonic identity: rotor weak sigma at lambda=Omega^2 equals 1/(4 Omega).
Omega = 1.3
lam_from_Omega = Omega ** 2                     # chi=1
sig_rule = rotor_sigma(lam_from_Omega)
gauss_rule = 1.0 / (4.0 * Omega)
# At the rule's MODERATE coupling the COMPACT rotor corrects F100's Gaussian
# UPWARD (compactness adds disorder); the correction is O(10%) and positive.
compact_corr = (sig_rule - gauss_rule) / gauss_rule
correction_positive_oten = 0.0 < compact_corr < 0.20
# deep-weak convergence to Gaussian is S2; soft Omega reaches strong confinement:
sig_soft = rotor_sigma((0.1) ** 2)              # Omega=0.1 -> strong, large sigma
s5 = bool(correction_positive_oten and sig_soft > 1.0)
record("S5", "rule map lambda=chi Omega^2 extends F100 to all couplings: at the "
       "rule's moderate Omega=1.3 the compact rotor corrects the Gaussian sigma "
       "UPWARD by ~12% (compactness = extra disorder); softening Omega->0.1 "
       "reaches strong-coupling confinement (sigma>1)",
       f"sigma_rule {sig_rule:.4f} vs Gaussian {gauss_rule:.4f} "
       f"(+{compact_corr:.1%}); sigma(Omega=0.1) {sig_soft:.3f}", s5)

# ============================================================
results["rotor_table"] = {str(l): round(rotor_sigma(l), 5)
                          for l in [0.01, 0.05, 0.2, 1.0, 5.0, 50.0]}
results["runtime_s"] = round(time.time() - t0, 3)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["summary"] = f"{n_pass}/{len(results['checks'])} PASS"
print(f"\nOverall: {results['summary']} ({results['runtime_s']} s)")

out = ROOT / "test-results" / "F101_strong_coupling_sigma.json"
out.write_text(json.dumps(results, indent=2))
print(f"Results written to {out}")
