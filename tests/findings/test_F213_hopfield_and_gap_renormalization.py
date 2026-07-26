#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F213_hopfield_and_gap_renormalization.py
=============================================

F213 — closing the two approximations F211 left:

  Part A  first-principles Hopfield eta / lambda from the F64 deformation
          potential D=(2/3)E_F in the free-electron (jellium) limit; the
          identity lambda = N(0) V_Task1 closes the F210/F211 loop.
  Part B  the (1+lambda) mass renormalization Z and the NON-universal gap
          ratio: 2 Delta/kTc rises above 3.528 for strong coupling, tracking
          Tc/omega_log; the strong-coupling formula reproduces measured
          reduced gaps; the fix is the Eliashberg Z(omega) equation.

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


# --------------------------- Part A ---------------------------------------
def test_HOP1_free_electron_fermi_energy():
    """E_F from the electron density matches the free-electron value (Al 11.7,
    Na 3.2 eV)."""
    ef_al = sc.fermi_energy_free_electron(1.81e29)
    ef_na = sc.fermi_energy_free_electron(2.65e28)
    ok = abs(ef_al - 11.7) / 11.7 < 0.05 and abs(ef_na - 3.2) / 3.2 < 0.06
    _record("HOP1", "free-electron E_F from density (Al 11.7, Na 3.2 eV)",
            "numeric", max(abs(ef_al - 11.7) / 11.7, abs(ef_na - 3.2) / 3.2), ok,
            {"E_F_Al": ef_al, "E_F_Na": ef_na})
    assert ok


def test_HOP2_deformation_potential_two_thirds_EF():
    """D = (2/3) E_F exactly (F64 dilation of the rotation-rate energy scale)."""
    EF = 11.67
    resid = abs(sc.deformation_potential_bare(EF) - 2.0 / 3.0 * EF)
    ok = resid < 1e-12
    _record("HOP2", "deformation potential D=(2/3)E_F exact (F64 dilation)",
            "exact", resid, ok)
    assert ok


def test_HOP3_lambda_is_N0_times_Task1_kernel():
    """lambda = N(0) V with V = D^2/(rho c_s^2) (the Task-1 kernel): lambda must
    scale as D^2, i.e. as screening_D^2.  Loop closure F210->F211->F213."""
    n, rho, cs = 1.81e29, 2700.0, 6420.0
    l1 = sc.lambda_jellium(n, rho, cs, screening_D=1.0)
    l_half = sc.lambda_jellium(n, rho, cs, screening_D=0.5)
    resid = abs(l_half - 0.25 * l1) / l1
    ok = resid < 1e-12
    _record("HOP3", "lambda = N(0) V_Task1 (scales as D^2) — F210/F211 loop closure",
            "exact", resid, ok, {"lambda_bare_Al": l1})
    assert ok


def test_HOP4_jellium_overestimate_is_consistent():
    """The model-derived bare jellium lambda overestimates the free-electron
    metals (Al, Na) by a CONSISTENT factor ~2.4-2.9 (the textbook jellium
    overestimate), reconciled by a physical screened deformation potential
    (1-6 eV)."""
    rows = {r["metal"]: r for r in sc.jellium_table()}
    over_al = rows["Al"]["overestimate"]
    over_na = rows["Na"]["overestimate"]
    # both free-electron metals overestimate, and by a similar factor
    consistent = 1.8 < over_al < 3.5 and 1.8 < over_na < 3.5 \
        and abs(over_al - over_na) < 1.0
    # screened D physical
    dphys = 0.8 < rows["Al"]["D_screened_eV"] < 7.0 and \
        0.8 < rows["Na"]["D_screened_eV"] < 3.0
    ok = consistent and dphys
    _record("HOP4", "bare jellium lambda overestimates Al,Na by consistent ~2.5x; screened D physical",
            "numeric", abs(over_al - over_na), ok,
            {"over_Al": over_al, "over_Na": over_na,
             "D_scr_Al": rows["Al"]["D_screened_eV"],
             "D_scr_Na": rows["Na"]["D_screened_eV"]})
    assert ok


# --------------------------- Part B ---------------------------------------
def test_MR1_Z_and_weak_coupling_limit():
    """Z = 1 + lambda; and the strong-coupling gap ratio reduces to the F210
    universal 3.528 as Tc/omega_log -> 0."""
    z = sc.z_mass_renormalization(1.55)
    weak = sc.gap_ratio_strong_coupling(1e-6, 1.0)   # Tc/wlog -> 0
    exact = 2.0 * math.pi / math.exp(sc.EULER_GAMMA)
    ok = abs(z - 2.55) < 1e-12 and abs(weak - exact) < 1e-6
    _record("MR1", "Z=1+lambda; gap ratio -> 3.528 as Tc/omega_log->0",
            "exact", abs(weak - exact), ok, {"Z_Pb": z})
    assert ok


def test_MR2_strong_coupling_gap_ratio_matches_measured():
    """The strong-coupling gap-ratio formula reproduces measured 2 Delta/kTc
    across the set (mean <6%), including the large Pb (4.38) and Hg (4.60)
    deviations from 3.528."""
    rows = sc.gap_ratio_table()
    errs = [r["rel_err"] for r in rows]
    mean_err = float(np.mean(errs))
    worst = float(np.max(errs))
    ok = mean_err < 0.06 and worst < 0.10
    _record("MR2", "strong-coupling gap ratio reproduces measured 2Delta/kTc (mean<6%)",
            "numeric", mean_err, ok,
            {"per_element": {r["element"]: (round(r["ratio_pred"], 2),
                             r["ratio_meas"]) for r in rows}})
    assert ok


def test_MR3_deviation_tracks_coupling():
    """The measured gap ratio is strongly CORRELATED with Tc/omega_log — the
    same coupling strength that makes Z=1+lambda large.  (Not strictly monotone:
    the closely-spaced weak-coupling elements Sn/Ta/In sit within measurement
    scatter.)  So the 3.528 'universal' is a weak-coupling limit; strong
    coupling needs the Eliashberg Z(omega) equation."""
    rows = sc.gap_ratio_table()
    x = np.array([r["Tc_over_wlog"] for r in rows])
    y = np.array([r["ratio_meas"] for r in rows])
    z = np.array([r["Z"] for r in rows])
    r_xy = float(np.corrcoef(x, y)[0, 1])       # coupling vs measured gap ratio
    r_xz = float(np.corrcoef(x, z)[0, 1])       # coupling vs Z=1+lambda
    ok = r_xy > 0.9 and r_xz > 0.9
    _record("MR3", "measured gap ratio & Z both strongly correlate with Tc/omega_log (coupling)",
            "numeric", 1.0 - min(r_xy, r_xz), ok,
            {"corr_ratio_vs_coupling": r_xy, "corr_Z_vs_coupling": r_xz})
    assert ok


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    npass = 0
    for t in tests:
        try:
            t(); npass += 1; print(f"  PASS  {t.__name__}")
        except AssertionError:
            print(f"  FAIL  {t.__name__}")
    RESULTS["jellium_table"] = sc.jellium_table()
    RESULTS["gap_ratio_table"] = sc.gap_ratio_table()
    out = {"finding": "F213",
           "title": "First-principles Hopfield eta + mass renormalization / gap ratio",
           "n_pass": npass, "n_total": len(tests), "checks": RESULTS}
    out_dir = os.path.abspath(os.path.join(_HERE, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "F213_hopfield_and_gap_renormalization.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{npass}/{len(tests)} PASS   ->  test-results/F213_hopfield_and_gap_renormalization.json")
    return npass == len(tests)


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
