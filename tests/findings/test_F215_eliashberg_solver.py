#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F215_eliashberg_solver.py
==============================

F215 — imaginary-axis Eliashberg (Z, Delta) solver on the F210 retarded kernel.
Recovers, DYNAMICALLY (no McMillan/Allen-Dynes fit), the mass renormalization
Z=1+lambda that F211/F213 identified as the missing piece:

  EL1  Z(i omega_0) -> 1 + lambda across couplings (mass renormalization emerges)
  EL2  weak-coupling reduces to the (1+lambda)-dressed McMillan/Allen-Dynes limit
  EL3  the (1+lambda) fix: Eliashberg T_c is strongly SUPPRESSED vs naive
       weak-coupling BCS (Pb: 7.6 K vs 32 K) -- the factor plain BCS dropped
  EL4  T_c from (lambda, omega_E, mu*) reproduces measured T_c of 7 elements
       (single Einstein mode, systematically ~high = known Einstein artifact;
       correlation with experiment r>0.97)
  EL5  rho(T) is monotone decreasing through 1 at T_c (well-defined transition)

Standalone or pytest.  Module: ca-simulation/ca_superconductivity.py.
"""
from __future__ import annotations
import os, sys, json, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(_REPO, "ca-simulation"))
import ca_superconductivity as sc  # noqa: E402

RESULTS = {}


def _record(cid, statement, tier, residual, passed, extra=None):
    RESULTS[cid] = {"statement": statement, "tier": tier,
                    "residual": float(residual), "pass": bool(passed)}
    if extra:
        RESULTS[cid].update(extra)


def test_EL1_Z_recovers_one_plus_lambda():
    """Z(i omega_0) approaches 1 + lambda across weak-to-strong coupling -- the
    Eliashberg mass renormalization emerges dynamically."""
    errs = {}
    for el, (lam, mus, wlog, thetaD, tc) in sc.REAL_SUPERCONDUCTORS.items():
        z0 = sc.eliashberg_Z0(lam, wlog, mus)
        errs[el] = abs(z0 - (1.0 + lam)) / (1.0 + lam)
    worst = max(errs.values())
    ok = worst < 0.08                        # Z(omega_0) slightly below 1+lam
    _record("EL1", "Z(i omega_0) -> 1+lambda across couplings (mass renormalization)",
            "numeric", worst, ok, {"rel_err": errs})
    assert ok


def test_EL2_weak_coupling_matches_allen_dynes():
    """At weak coupling the Eliashberg T_c reduces to the (1+lambda)-dressed
    Allen-Dynes value (both include the mass renormalization; they agree to
    ~15%, unlike naive BCS which is 4x too high)."""
    te = sc.eliashberg_tc(0.3, 100.0, 0.0)
    ad = sc.allen_dynes_tc(0.3, 0.0, 100.0)
    resid = abs(te - ad) / ad
    ok = resid < 0.20
    _record("EL2", "weak-coupling Eliashberg T_c matches Allen-Dynes (both 1+lambda-dressed)",
            "numeric", resid, ok, {"Tc_eliashberg": te, "Tc_allen_dynes": ad})
    assert ok


def test_EL3_mass_renormalization_suppresses_Tc():
    """THE FIX: the (1+lambda) mass renormalization suppresses Eliashberg T_c
    far below the naive weak-coupling BCS estimate that omits it.  Every element
    has Tc_Eliashberg < 0.4 * Tc_BCS; Pb is suppressed ~4x."""
    supp = {}
    for el, (lam, mus, wlog, thetaD, tc) in sc.REAL_SUPERCONDUCTORS.items():
        te = sc.eliashberg_tc(lam, wlog, mus)
        bcs = sc.bcs_tc(lam, mus, wlog)
        supp[el] = te / bcs
    ok = all(s < 0.4 for s in supp.values()) and supp["Pb"] < 0.3
    _record("EL3", "(1+lambda) mass renorm suppresses Eliashberg T_c far below naive BCS",
            "numeric", max(supp.values()), ok, {"Tc_Eliashberg_over_BCS": supp})
    assert ok


def test_EL4_tc_reproduces_measured():
    """Eliashberg T_c from (lambda, omega_E=omega_log, mu*) reproduces measured
    T_c for the 7 elements with strong correlation (r>0.97).  The single
    Einstein mode runs systematically ~high (known artifact; a distributed
    alpha^2 F would tighten it)."""
    exp, elz = [], []
    per = {}
    for el, (lam, mus, wlog, thetaD, tc) in sc.REAL_SUPERCONDUCTORS.items():
        te = sc.eliashberg_tc(lam, wlog, mus)
        exp.append(tc); elz.append(te); per[el] = (round(te, 2), tc)
    r = float(np.corrcoef(elz, exp)[0, 1])
    ok = r > 0.97
    _record("EL4", "Eliashberg T_c reproduces measured T_c of 7 elements (r>0.97)",
            "numeric", 1.0 - r, ok, {"corr_with_exp": r, "per_element": per})
    assert ok


def test_EL5_eigenvalue_crosses_one_at_Tc():
    """rho(T) is monotone decreasing and crosses 1 exactly at the solved T_c
    (well-defined transition)."""
    lam, mus, wlog = 1.55, 0.10, 56.0
    Tc = sc.eliashberg_tc(lam, wlog, mus)
    rho_lo = sc.eliashberg_tc_eigenvalue(0.7 * Tc, lam, wlog, mus)
    rho_at = sc.eliashberg_tc_eigenvalue(Tc, lam, wlog, mus)
    rho_hi = sc.eliashberg_tc_eigenvalue(1.4 * Tc, lam, wlog, mus)
    ok = rho_lo > 1.0 > rho_hi and abs(rho_at - 1.0) < 1e-3
    _record("EL5", "rho(T) monotone through 1 at T_c (well-defined transition)",
            "numeric", abs(rho_at - 1.0), ok,
            {"rho_0.7Tc": rho_lo, "rho_Tc": rho_at, "rho_1.4Tc": rho_hi})
    assert ok


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    npass = 0
    for t in tests:
        try:
            t(); npass += 1; print(f"  PASS  {t.__name__}")
        except AssertionError:
            print(f"  FAIL  {t.__name__}")
    out = {"finding": "F215", "title": "Eliashberg (Z,Delta) solver on the F210 kernel",
           "n_pass": npass, "n_total": len(tests), "checks": RESULTS}
    out_dir = os.path.abspath(os.path.join(_HERE, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "F215_eliashberg_solver.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{npass}/{len(tests)} PASS   ->  test-results/F215_eliashberg_solver.json")
    return npass == len(tests)


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
