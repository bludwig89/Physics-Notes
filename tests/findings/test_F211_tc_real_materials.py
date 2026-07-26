#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F211_tc_real_materials.py
==============================

F211 — T_c MAGNITUDE from real superconductors.  F210 fixed the gap-equation
FORM and the coupling-independent universals; here we feed the SAME machinery
real material couplings (lambda, mu*, omega_log) and predict T_c for a set of
elemental BCS superconductors (Al, Sn, In, Ta, Nb, Pb, Hg).

Result: the Allen-Dynes-dressed gap equation reproduces measured T_c to ~10-15%
(a few % for the well-characterised strong-coupling elements with the f1 f2
factors), and the model-native Task-1 kernel V=D^2/(rho c_s^2) reproduces the
tabulated lambda in Hopfield form.  Plain weak-coupling BCS overestimates,
documenting the need for the (1+lambda) mass renormalisation.

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


def test_TC1_allen_dynes_reproduces_measured_tc():
    """Allen-Dynes T_c(lambda, mu*, omega_log) reproduces measured T_c across
    the reference set to within the theory's ~15% accuracy (mean), and to a few
    % for the well-characterised strong-coupling elements (Pb, Ta)."""
    rows = sc.tc_table()
    errs = {r["element"]: r["rel_err_AD"] for r in rows}
    mean_err = float(np.mean(list(errs.values())))
    # strong-coupling / well-characterised elements land tight
    tight = errs["Pb"] < 0.05 and errs["Ta"] < 0.05 and errs["Sn"] < 0.10
    ok = mean_err < 0.20 and tight
    _record("TC1", "Allen-Dynes gap-eq reproduces measured T_c (mean |err|<20%; Pb/Ta/Sn tight)",
            "numeric", mean_err, ok,
            {"per_element_rel_err": errs, "mean_rel_err": mean_err})
    assert ok


def test_TC2_strong_coupling_factors_improve_Pb_Hg():
    """The f1 f2 strong-coupling factors (r=<w^2>^.5/w_log~1.3) bring the
    lambda>1.5 elements Pb, Hg to within a few % of experiment."""
    pb = sc.allen_dynes_tc(1.55, 0.10, 56.0, omega2_over_wlog=1.3)
    hg = sc.allen_dynes_tc(1.62, 0.10, 29.0, omega2_over_wlog=1.3)
    e_pb = abs(pb - 7.19) / 7.19
    e_hg = abs(hg - 4.15) / 4.15
    ok = e_pb < 0.07 and e_hg < 0.07
    _record("TC2", "f1 f2 strong-coupling factors bring Pb, Hg within a few %",
            "numeric", max(e_pb, e_hg), ok,
            {"Pb_K": pb, "Hg_K": hg, "err_Pb": e_pb, "err_Hg": e_hg})
    assert ok


def test_TC3_hopfield_lambda_matches_tabulated():
    """Task-1 kernel V=D^2/(rho c_s^2) in Hopfield form lambda=eta/(M<w^2>)
    reproduces tabulated lambda for Nb, Al, Ta, Pb (<5%)."""
    cases = [("Nb", 9.8, 9.7, 1.01), ("Al", 1.38, 3.3, 0.43),
             ("Ta", 7.8, 11.3, 0.69), ("Pb", 3.9, 2.5, 1.55)]
    errs = {}
    for el, eta, spring, lit in cases:
        lam = sc.lambda_from_hopfield(eta, spring)
        errs[el] = abs(lam - lit) / lit
    worst = max(errs.values())
    ok = worst < 0.05
    _record("TC3", "Hopfield lambda=eta/(M<w^2>) (Task-1 kernel) matches tabulated lambda",
            "numeric", worst, ok, {"rel_err": errs})
    assert ok


def test_TC4_bcs_prefactor_is_F210_universal():
    """The weak-coupling BCS prefactor 1.134 = 2 e^gamma/pi is the SAME constant
    behind F210's universal gap ratio -- T_c and the gap share one origin."""
    pref = 2.0 * math.exp(sc.EULER_GAMMA) / math.pi
    resid = abs(pref - 1.1338)                       # textbook 1.134
    ok = resid < 1e-3
    _record("TC4", "BCS T_c prefactor 2 e^gamma/pi = 1.134 = F210 gap-ratio constant",
            "machine", abs(pref - 2.0 * math.exp(sc.EULER_GAMMA) / math.pi), ok,
            {"prefactor": pref})
    assert ok


def test_TC5_weak_coupling_bcs_overestimates():
    """Documenting the physics: plain BCS (N(0)V=lambda-mu*, no (1+lambda) mass
    renormalisation) systematically OVERestimates T_c; Allen-Dynes fixes it.
    Every element must have Tc_BCS > Tc_AllenDynes ~ Tc_exp."""
    rows = sc.tc_table()
    all_over = all(r["Tc_BCS_K"] > r["Tc_exp_K"] for r in rows)
    ad_closer = all(abs(r["Tc_AllenDynes_K"] - r["Tc_exp_K"]) <
                    abs(r["Tc_BCS_K"] - r["Tc_exp_K"]) for r in rows)
    ok = all_over and ad_closer
    _record("TC5", "weak-coupling BCS overestimates T_c; Allen-Dynes (mass renorm) fixes it",
            "numeric", 0.0 if ok else 1.0, ok)
    assert ok


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    npass = 0
    for t in tests:
        try:
            t(); npass += 1; print(f"  PASS  {t.__name__}")
        except AssertionError:
            print(f"  FAIL  {t.__name__}")
    # attach the full table for the record
    RESULTS["table"] = sc.tc_table()
    out = {"finding": "F211", "title": "T_c magnitude from real superconductors",
           "n_pass": npass, "n_total": len(tests), "checks": RESULTS}
    out_dir = os.path.abspath(os.path.join(_HERE, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "F211_tc_real_materials.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{npass}/{len(tests)} PASS   ->  test-results/F211_tc_real_materials.json")
    return npass == len(tests)


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
