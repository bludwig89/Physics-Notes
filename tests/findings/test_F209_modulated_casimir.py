"""
test_F209_modulated_casimir.py  —  Can a *time-modulated* Casimir cavity break
the F207-G1 beable-source vs SEP-vacuum-buoyancy degeneracy?
=============================================================================

F207 G1 showed the STATIC Casimir shift gravitates as Δm=E_C/c², numerically
degenerate with SEP vacuum-buoyancy → static weighing cannot discriminate.
This finding tests the open move: modulation.

Checks:
  M1  Archimedes reflectivity modulation η(t): the beable-source weight and the
      SEP-buoyancy weight are computed by INDEPENDENT formulas (Gauss closure vs
      buoyancy definition) and coincide in the time domain AND in every Fourier
      harmonic, for several modulation frequencies and depths → degeneracy
      survives modulation to ALL orders.
  M2  The mechanism: the beable-vs-template difference lives entirely in the
      homogeneous zero-point offset ρ0, which cancels EXACTLY in a differential
      (tared) weighing (present inside AND outside the cavity, F193 A4).  Its
      contribution to the signal is 0 for arbitrary ρ0; only the beable Casimir
      differential survives.
  M3  DCE real-pair gravitation: the radiated beable energy E_rad=ħΩ_d sinh²(gt)
      (F207 D1) gravitates as Δm=E_rad/c², and the drive-supplied (SEP/energy-
      conservation) accounting weighs an IDENTICAL Δm (residual 0).  The
      template-change and beable-change both equal E_rad (the offset is
      unchanged) → DCE is degenerate too.
  M4  Quantified realism: Archimedes (Avino) and DCE (Wilson) parameters give
      weight signals ~1e-24 N and ~1e-36 N — degenerate AND far below any
      balance sensitivity; recorded as honest-negative, not a lab handle.

CLAUDE.md: real scalar arithmetic only (no chiral transforms / np.linalg.eig).
"""

import sys, os, json, time

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

import numpy as np
from casim.engine.interactions import qed_casimir as cc

RESULTS = os.path.join(os.path.dirname(__file__), '..', '..', 'test-results',
                       'F209_modulated_casimir.json')

TOL = 1e-18          # weight-signal degeneracy tolerance (N); structural zero
results = {"finding": "F209", "checks": {}, "ts": time.strftime("%Y-%m-%d %H:%M")}


def record(name, passed, **info):
    results["checks"][name] = {"pass": bool(passed), **info}
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {info}")
    return passed


# realistic-ish ideal cavity (F207 G1 example): 1 cm², 10 nm gap
AREA = 1e-4
LSEP = 1e-8

ok = True

# ── M1 — Archimedes modulation: degeneracy survives at all harmonics ──
m1_all = True
det = {}
for f_mod in (1.0, 3.7, 1000.0):            # Hz — arbitrary switching rates
    for (eta0, deta) in ((0.5, 0.5), (0.7, 0.3), (0.9, 0.1)):
        t, Wb, Ws, dmax, fftmax = cc.modulated_weight_signals(
            AREA, LSEP, eta0, deta, f_mod)
        # both signals must be non-trivial (actually modulating) ...
        nontrivial = (np.ptp(Wb) > 0.0)
        # ... and identical in time and in every Fourier component
        good = nontrivial and (dmax <= TOL) and (fftmax <= 1e-12 * abs(np.max(Wb) or 1))
        m1_all = m1_all and good
        det[f"f{f_mod}_e{eta0}_{deta}"] = {"time_max_diff": dmax,
                                           "fft_max_diff": fftmax,
                                           "ptp_Wb": float(np.ptp(Wb))}
ok &= record("M1_archimedes_modulation_degenerate", m1_all,
             note="beable(Gauss) vs SEP(buoyancy) coincide in time+all harmonics",
             detail=det)

# ── M2 — homogeneous offset cancels differentially (the mechanism) ──
m2_all = True
offdet = {}
for rho0 in (0.0, 6.0e-10, 3.46e111):       # incl. the F164 bare vacuum density
    offdiff, beable_diff = cc.homogeneous_offset_differential(
        rho0, AREA, LSEP, eta_ref=0.0, eta_sig=1.0)
    # offset never contributes to the differential; beable Casimir does
    good = (offdiff == 0.0) and (beable_diff != 0.0)
    m2_all = m2_all and good
    offdet[f"rho0_{rho0:.3e}"] = {"offset_differential": offdiff,
                                  "beable_differential": beable_diff}
ok &= record("M2_homogeneous_offset_cancels", m2_all,
             note="beable-vs-template split lives in ρ0, which cancels in a tared weighing",
             detail=offdet)

# ── M3 — DCE: real-pair energy gravitates, degenerate with drive/SEP ──
Omega_d = 2 * np.pi * 10.3e9                 # Wilson 2011 ~10.3 GHz drive
gcoup = 0.05                                 # effective parametric coupling
tt = 1.0
E_rad, dm_b, dm_s, res = cc.dce_radiated_gravitating_mass(Omega_d, gcoup, tt, n_modes=1)
tpl_ch, bea_ch, res2 = cc.dce_change_beable_vs_template(Omega_d, gcoup, tt, n_modes=1)
m3 = (res == 0.0) and (res2 == 0.0) and (E_rad > 0.0) and (dm_b == E_rad / cc.C_SI ** 2)
ok &= record("M3_dce_pair_gravitation_degenerate", m3,
             E_rad_J=E_rad, dm_beable_kg=dm_b, dm_sep_kg=dm_s,
             beable_minus_sep=res, template_change_minus_beable_change=res2,
             note="radiated beable energy = drive work; both gravitate identically")

# ── M4 — quantified realism (both regimes: degenerate AND unweighable) ──
# Archimedes signal size (full switch η:0→1)
_, dm_arch, W_arch = cc.casimir_gravitating_mass(AREA, LSEP)
# DCE realistic weight (flux ~1e4 photons/s over 1 s at 10.3 GHz)
flux = 1e4
E_dce_real = cc.HBAR * Omega_d * flux * 1.0
W_dce = 9.81 * E_dce_real / cc.C_SI ** 2
m4 = (abs(W_arch) < 1e-20) and (abs(W_dce) < 1e-30)
ok &= record("M4_signals_unweighable", m4,
             archimedes_weight_N=abs(W_arch), dce_weight_N=W_dce,
             note="both regimes degenerate AND far below balance sensitivity")

results["all_pass"] = bool(ok)
results["n_pass"] = sum(1 for c in results["checks"].values() if c["pass"])
results["n_total"] = len(results["checks"])

os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
with open(RESULTS, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n{results['n_pass']}/{results['n_total']} PASS  →  {RESULTS}")
assert ok, "F209 modulated-Casimir degeneracy checks failed"
