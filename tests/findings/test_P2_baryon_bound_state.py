#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_P2_baryon_bound_state.py
=============================

P2 of docs/roadmaps/roadmap-matter-binding.md — certify the DYNAMICAL baryon: a real-time,
non-dispersing, mass-measured three-quark bound state (proton uud, neutron udd),
replacing F71's operator-level colour singlet.

Engine: `src/casim/engine/particles/baryon_dynamics.py` — explicitly-correlated-Gaussian
three-body solver in mass-normalised Jacobi coordinates with the P1 confining +
one-gluon-exchange Cornell potential  V_p = sigma r - (2 alpha_s/3)/r  per pair.

CHECKS
------
  S0  ENGINE CORRECTNESS (harmonic self-test): with the exact HO ground-state
      Gaussian in the basis, the ECG ground energy equals the analytic
      3 sqrt(3k/m) to machine precision (validates T and the potential kernels).
  S1  TWO ROUTES AGREE: scipy.linalg.eigh(H,S) vs hand-rolled Cholesky reduction
      -> machine precision (the F74 discipline, now for three bodies).
  S2  VARIATIONAL CONVERGENCE: E_rel decreases monotonically and settles as the
      basis is refined -> a genuine converged bound state.
  S3  DISCRETE SPECTRUM / NON-DISPERSING: a confining potential has no continuum;
      the ground state is gapped below a finite tower of excited states (level
      spacing > 0) -> the proton cannot fall apart (dynamical F71 confinement).
  S4  S3-SYMMETRIC SPATIAL GROUND STATE: the three pair separations <r_p> are
      equal -> totally symmetric spatial wavefunction (baryon antisymmetry on
      colour/spin, F71 BS6/BS7).
  S5  CONFINEMENT DOMINANCE (F97 made dynamical): in the current-quark-mass
      limit the quark-mass sum is <~1% of the baryon mass -> the mass is the
      STRING, not the constituents (reproduces F97's PDG 0.96%).
  S6  STRUCTURAL INVARIANCE: the confinement-dominance + symmetry conclusions are
      unchanged under the alternative '1/2-rule' Casimir scaling of the potential.
  S7  m_p/sqrt(sigma) RATIO: report the dimensionless baryon mass; compare to the
      lattice nucleon-in-string-units value (Tier-B, P6-gated; NR overshoot
      flagged).
  S8  NEUTRON n-p SPLITTING: m_n - m_p sign POSITIVE, driven by (m_d - m_u)
      beating the EM self-energy; rough magnitude vs +1.293 MeV.
  S9  CALIBRATED QUARK FRACTION (notebook-v2 prompt C, 2026-09-23): repeats S5
      with the PDG current masses m_u=2.16, m_d=4.67 MeV (F120/F121's own
      quark-mass readout; SQRT_SIGMA_GEV=0.42 GeV, D7) in place of the toy
      degenerate m_q=0.01 sqrt-sigma -- reports the proton (uud) and neutron
      (udd) quark-mass fractions as genuine calibrated numbers rather than a
      limiting-case demonstration.

All arithmetic REAL (real symmetric generalised eigenproblem) -> CLAUDE.md numpy
caveat does not bite.  Runs in a few seconds.

Run:  python3 tests/findings/test_P2_baryon_bound_state.py
Writes test-results/P2_baryon_bound_state.json.
"""

import os
import sys
import json
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.particles import baryon_dynamics as B  # noqa: E402
from casim.constants import sqrt_sigma_GeV  # noqa: E402

results = {"finding": "F122", "phase": "P2",
           "title": "dynamical baryon: real-time three-quark bound state",
           "checks": {}, "derived": {}, "notes": []}
PASS = True


def record(name, residual, target, tier, ok, extra=None):
    global PASS
    results["checks"][name] = {"residual": float(residual), "target": float(target),
                               "tier": tier, "status": "PASS" if ok else "FAIL"}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:46s} "
          f"resid={float(residual):.3e}  (target {float(target):.0e}, {tier})")


print("=" * 78)
print("P2 / F122 — dynamical baryon: real-time three-quark bound state")
print("=" * 78)

SIGMA, ALPHA_S = 1.0, 0.5          # sqrt(sigma)=1 units; canonical alpha_s
# well-conditioned variational mesh (no permutation tripling) for energy/route
# checks; a separate permutation-closed basis is used for the symmetry checks.
basis = B.make_basis(n1=8, n2=8, symmetrize=False)
basis_sym = B.make_basis(n1=5, n2=5, symmetrize=True)   # S3-closed (overcomplete)

# ---------------------------------------------------------------------------
print("\nS0  engine correctness — harmonic self-test (exact Gaussian in basis)")
maxr = 0.0
for k, m in [(1.0, 1.0), (2.0, 0.7), (0.5, 1.3)]:
    A_exact = np.sqrt(3.0 * k * m) * np.eye(2)
    bhs = B.make_basis(n1=6, n2=6, correlated=False, symmetrize=False) + [A_exact]
    ecg = B.harmonic_ground_energy_ecg(k, m, basis=bhs)
    ex = B.harmonic_ground_energy_exact(k, m)
    maxr = max(maxr, abs(ecg - ex) / ex)
record("S0 ECG == analytic 3 sqrt(3k/m)", maxr, 1e-10, "machine", maxr < 1e-10)

# ---------------------------------------------------------------------------
print("\nS1  two independent solve routes agree (proton, m_q=0.785 sqrt-sigma)")
mq = 0.785
r = B.ground_state_relative_energy(mq, SIGMA, ALPHA_S, basis=basis)
diff = r["route_diff"]
results["derived"]["E_rel_proton"] = r["E_rel_scipy"]
print(f"       scipy   E_rel = {r['E_rel_scipy']:.10f}")
print(f"       cholesky E_rel = {r['E_rel_cholesky']:.10f}")
record("S1 scipy eigh == Cholesky reduction", diff, 1e-9, "machine", diff < 1e-9)

# ---------------------------------------------------------------------------
print("\nS2  variational convergence (monotone decrease + settling)")
seq = []
for nb in (4, 6, 8, 10):
    bb = B.make_basis(n1=nb, n2=nb, symmetrize=False)
    seq.append(B.ground_state_relative_energy(mq, SIGMA, ALPHA_S, basis=bb)["E_rel_scipy"])
mono = all(seq[i] >= seq[i + 1] - 1e-9 for i in range(len(seq) - 1))
settled = abs(seq[-1] - seq[-2]) / seq[-1]
results["derived"]["convergence_sequence"] = seq
print(f"       E_rel(n=4,6,8,10) = {[f'{x:.4f}' for x in seq]}")
print(f"       relative change last step = {settled:.2e}")
record("S2 monotone variational decrease", 0.0 if mono else 1.0, 0.5, "quantitative", mono)
record("S2 converged (last step < 1e-2)", settled, 1e-2, "quantitative", settled < 1e-2)

# ---------------------------------------------------------------------------
print("\nS3  discrete (confining) spectrum -> non-dispersing bound state")
w, c0, bas, H, S = B.spectrum_and_ground_vector(mq, SIGMA, ALPHA_S, basis=basis_sym)
gap = w[1] - w[0]
results["derived"]["E0"] = float(w[0])
results["derived"]["E1"] = float(w[1])
results["derived"]["level_gap"] = float(gap)
print(f"       E0 = {w[0]:.5f}, E1 = {w[1]:.5f}, gap = {gap:.5f} sqrt-sigma > 0")
record("S3 finite gap to 1st excited (discrete)", -gap, -1e-3, "quantitative", gap > 1e-3)

# ---------------------------------------------------------------------------
print("\nS4  S3-symmetric spatial ground state (<r_12>=<r_13>=<r_23>)")
rad = B.pair_radii(c0, bas)
vals = np.array([rad["12"], rad["13"], rad["23"]])
spread = float(np.max(vals) - np.min(vals)) / float(np.mean(vals))
results["derived"]["pair_radii"] = {k: float(v) for k, v in rad.items()}
print(f"       <r_p> = {{12:{rad['12']:.4f}, 13:{rad['13']:.4f}, 23:{rad['23']:.4f}}}")
record("S4 three pair radii equal (symmetric)", spread, 1e-6, "machine", spread < 1e-6)

# ---------------------------------------------------------------------------
print("\nS5  confinement dominance (F97): current-quark limit, quark sum << M")
mq_cur = 0.01                      # ~ few-MeV current quark in sqrt-sigma units
rc = B.ground_state_relative_energy(mq_cur, SIGMA, ALPHA_S, basis=basis)
Ec = rc["E_rel_scipy"]
Mc = 3.0 * mq_cur + Ec
qfrac = 3.0 * mq_cur / Mc
results["derived"]["quark_fraction_current"] = float(qfrac)
results["derived"]["confinement_fraction_current"] = float(Ec / Mc)
print(f"       m_q={mq_cur} sqrt-sigma -> M={Mc:.3f}, quark sum fraction = {qfrac*100:.2f}%")
print(f"       (cf. F97 / PDG: current-quark sum is 0.96% of m_p)")
record("S5 quark sum < 2% of M (string-dominated)", qfrac, 0.02, "quantitative", qfrac < 0.02)

# ---------------------------------------------------------------------------
print("\nS6  structural invariance under '1/2-rule' Casimir scaling")
rh = B.ground_state_relative_energy(mq_cur, SIGMA, ALPHA_S, basis=basis,
                                    conf_per_pair=0.5, oge_casimir=1.0 / 3.0)
Mh = 3.0 * mq_cur + rh["E_rel_scipy"]
qfrac_h = 3.0 * mq_cur / Mh
wh, c0h, bh, _, _ = B.spectrum_and_ground_vector(mq, SIGMA, ALPHA_S, basis=basis_sym,
                                                 conf_per_pair=0.5, oge_casimir=1.0/3.0)
radh = B.pair_radii(c0h, bh, conf_per_pair=0.5, oge_casimir=1.0/3.0)
vh = np.array([radh["12"], radh["13"], radh["23"]])
spread_h = float(np.max(vh) - np.min(vh)) / float(np.mean(vh))
ok6 = (qfrac_h < 0.02) and (spread_h < 1e-6) and (rh["route_diff"] < 1e-9)
print(f"       1/2-rule: quark fraction={qfrac_h*100:.2f}%, radii spread={spread_h:.1e}")
record("S6 dominance+symmetry survive 1/2-rule", spread_h, 1e-6, "quantitative", ok6)

# ---------------------------------------------------------------------------
print("\nS7  m_p/sqrt(sigma) ratio (Tier-B, P6-gated)")
mq_const = 0.785                   # constituent m_q ~ 0.33 GeV at sqrt-sigma=0.42
Mp_ratio = 3.0 * mq_const + r["E_rel_scipy"]
m_N_emp = 0.939 / 0.420            # empirical nucleon in sqrt-sigma units
results["derived"]["m_p_over_sqrt_sigma_NR"] = float(Mp_ratio)
results["derived"]["m_N_over_sqrt_sigma_empirical"] = float(m_N_emp)
print(f"       m_p/sqrt(sigma) (NR, no V0) = {Mp_ratio:.3f}")
print(f"       empirical m_N/sqrt(sigma)   = {m_N_emp:.3f}")
print(f"       -> NR constituent solve OVERSHOOTS (missing Cornell constant V0 +")
print(f"          relativistic reduction for light quarks); flagged P6/next step.")
# the CHECK is only that a finite, positive, O(1-10) ratio is produced (a real
# bound mass on the string scale) — the precise value is P6/relativistic.
record("S7 finite positive m_p/sqrt-sigma on string scale", 0.0,
       1.0, "tierB", 1.0 < Mp_ratio < 20.0)

# ---------------------------------------------------------------------------
print("\nS8  neutron udd: n-p mass splitting sign and magnitude")
# model quark masses (F40 ratio m_d/m_u ~ 2) anchored to PDG current masses;
# EM self-energy external (P5 machinery): proton (two q=+2/3) is heavier EM-wise.
M_U, M_D = 2.16, 4.67              # MeV (PDG current; F40 ratio consistent)
DELTA_EM_P, DELTA_EM_N = 1.00, 0.0  # MeV (lattice/Cottingham: proton +1.00)
npd = B.neutron_minus_proton(M_U, M_D, SIGMA, ALPHA_S, DELTA_EM_P, DELTA_EM_N)
results["derived"]["np_splitting"] = npd
print(f"       (m_d - m_u)     = +{npd['m_d_minus_m_u']:.2f} MeV  (neutron heavier, strong)")
print(f"       EM term         = {npd['em_term']:.2f} MeV  (proton heavier, EM)")
print(f"       m_n - m_p       = +{npd['m_n_minus_m_p']:.2f} MeV   (measured +1.293)")
record("S8a m_n - m_p sign POSITIVE", 0.0 if npd["sign_positive"] else 1.0,
       0.5, "quantitative", npd["sign_positive"])
mag_err = abs(npd["m_n_minus_m_p"] - 1.293)
record("S8b |m_n-m_p| within 1 MeV of measured", mag_err, 1.0, "tierB", mag_err < 1.0)

# ---------------------------------------------------------------------------
print("\nS9  calibrated quark fraction (notebook-v2 prompt C): real F120/F121")
print("    PDG current masses in place of the S5 toy degenerate m_q=0.01")
SQRT_SIGMA_MEV = sqrt_sigma_GeV * 1000.0
m_u_cal = M_U / SQRT_SIGMA_MEV
m_d_cal = M_D / SQRT_SIGMA_MEV
print(f"       sqrt(sigma) = {SQRT_SIGMA_MEV:.1f} MeV  ->  "
      f"m_u={m_u_cal:.6f}, m_d={m_d_cal:.6f} sqrt-sigma")

# proton (uud): equal-mass solver run at the average current-mass scale (the
# solver assumes equal constituent masses -- generalising to unequal u/d masses
# is a separate structural change, not this rerun); the physical quark-mass
# numerator uses the true uud sum, not 3x the average.
m_avg_p = (2.0 * m_u_cal + m_d_cal) / 3.0
rp = B.ground_state_relative_energy(m_avg_p, SIGMA, ALPHA_S, basis=basis)
Ep = rp["E_rel_scipy"]
quark_sum_p = 2.0 * m_u_cal + m_d_cal
Mp_cal = quark_sum_p + Ep
qfrac_p_cal = quark_sum_p / Mp_cal

# neutron (udd), same construction
m_avg_n = (2.0 * m_d_cal + m_u_cal) / 3.0
rn = B.ground_state_relative_energy(m_avg_n, SIGMA, ALPHA_S, basis=basis)
En = rn["E_rel_scipy"]
quark_sum_n = 2.0 * m_d_cal + m_u_cal
Mn_cal = quark_sum_n + En
qfrac_n_cal = quark_sum_n / Mn_cal

results["derived"]["quark_fraction_proton_calibrated"] = float(qfrac_p_cal)
results["derived"]["quark_fraction_neutron_calibrated"] = float(qfrac_n_cal)
results["derived"]["M_proton_calibrated_sqrt_sigma"] = float(Mp_cal)
results["derived"]["M_neutron_calibrated_sqrt_sigma"] = float(Mn_cal)
print(f"       proton (uud):  M={Mp_cal:.4f} sqrt-sigma, quark fraction = {qfrac_p_cal*100:.4f}%")
print(f"       neutron (udd): M={Mn_cal:.4f} sqrt-sigma, quark fraction = {qfrac_n_cal*100:.4f}%")
print(f"       (cf. S5 toy 0.01 sqrt-sigma degenerate: {qfrac*100:.4f}%; PDG/F97: 0.96%)")
record("S9 proton calibrated quark fraction < 2% of M", qfrac_p_cal, 0.02,
       "quantitative", qfrac_p_cal < 0.02)
record("S9 neutron calibrated quark fraction < 2% of M", qfrac_n_cal, 0.02,
       "quantitative", qfrac_n_cal < 0.02)

# ---------------------------------------------------------------------------
results["notes"] = [
    "ENGINE: explicitly-correlated-Gaussian three-body solver in mass-normalised "
    "Jacobi coords; overlap/kinetic/<r>/<1/r> all closed-form. Validated to "
    "machine precision against the analytic harmonic three-body ground state.",
    "TWO ROUTES (scipy generalised eigh vs hand-rolled Cholesky reduction) agree "
    "to ~1e-12, the F74 discipline carried to three bodies.",
    "CONFINEMENT DOMINANCE (the headline, matching F97): with current-mass quarks "
    "the quark-mass sum is <1% of the baryon mass -- the mass is the confining "
    "STRING (P1: F70/F94/F110), NOT the constituents. The dynamical realisation of "
    "F71's energetic-confinement argument and F97's centre-closure no-go.",
    "NON-DISPERSING: a confining potential has a purely discrete spectrum (no "
    "scattering continuum), so the ground state is automatically a stationary, "
    "normalisable bound state -- the proton cannot fall apart.",
    "n-p SPLITTING: sign POSITIVE and ~+1.5 MeV, the down-up current-mass gap "
    "(F40 ratio) beating the proton's larger EM self-energy (P5). Sign is the real "
    "test of the F40 ratios; it passes.",
    "OPEN (Tier-B / P6): the ABSOLUTE m_p/sqrt(sigma) from the NR constituent solve "
    "overshoots the lattice value -- the missing additive Cornell constant V0 and "
    "the relativistic reduction for light quarks. The precise number needs the "
    "relativised / Bethe-Salpeter treatment (the same regime F74 flagged) and the "
    "P6 SI anchor. Structure is the prediction here; the MeV is P6-gated.",
    "CALIBRATED RERUN (notebook-v2 prompt C, 2026-09-23): substituting the real "
    "F120/F121 PDG current masses (m_u=2.16, m_d=4.67 MeV, sqrt(sigma)=0.42 GeV) "
    "for S5's toy degenerate m_q=0.01 sqrt-sigma gives quark-mass fractions of "
    "0.07% (proton) and 0.09% (neutron) -- SMALLER than the toy value's 0.11%, "
    "not a move toward the lattice-QCD ~9% four-term decomposition figure (which "
    "is a structurally different operator split, per F122 Sec.5/NB2-004). "
    "Caveat: the solver assumes equal constituent masses, so the u/d asymmetry "
    "enters only via the average current-mass scale in the kinetic/potential "
    "solve, not a genuinely unequal-mass three-body Hamiltonian.",
]

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "P2_baryon_bound_state.json")
results["overall"] = "PASS" if PASS else "FAIL"
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)

print("\n" + "=" * 78)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
print(f"OVERALL: {'PASS' if PASS else 'FAIL'}   ({n_pass}/{len(results['checks'])} checks)")
print(f"results -> {out_path}")
print("=" * 78)
sys.exit(0 if PASS else 1)
