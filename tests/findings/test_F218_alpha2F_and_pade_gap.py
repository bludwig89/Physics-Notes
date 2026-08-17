#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F218_alpha2F_and_pade_gap.py
=================================

F218 — closes the two extensions F215 left:

  Part A  first-principles Eliashberg spectral function alpha^2 F(omega) =
          lambda omega^2/omega_max^2 (deformation potential D=(2/3)E_F on a
          Debye acoustic band); omega_log = omega_max/sqrt(e) exact.  Feeding it
          to the solver shows T_c is nearly SHAPE-INSENSITIVE at fixed omega_log
          (Einstein ~ Debye) -- explaining why the F215 single mode worked.
  Part B  Pade (Vidberg-Serene) continuation Delta(i omega_n) -> Delta(omega):
          the strong-coupling 2 Delta_0/kTc rises DYNAMICALLY from 3.53 (Al) to
          ~4.7 (Pb, Hg), tracking the measured trend; the first-principles Debye
          spectrum tightens it (the gap ratio IS shape-sensitive, unlike T_c).

Standalone or pytest.  Module: src/casim/engine/interactions/superconductivity.py (mpmath).
"""
from __future__ import annotations
import os, sys, json, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import superconductivity as sc  # noqa: E402

RESULTS = {}
MEAS_RATIO = {"Al": 3.40, "Sn": 3.50, "In": 3.65, "Ta": 3.60,
              "Nb": 3.80, "Pb": 4.38, "Hg": 4.60}


def _record(cid, statement, tier, residual, passed, extra=None):
    RESULTS[cid] = {"statement": statement, "tier": tier,
                    "residual": float(residual), "pass": bool(passed)}
    if extra:
        RESULTS[cid].update(extra)


def _trap(y, x):
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * (x[1:] - x[:-1])))


# --------------------------- Part A ---------------------------------------
def test_AF1_alpha2F_normalizes_to_lambda():
    """2 int alpha^2F(omega)/omega d omega = lambda (the coupling weight)."""
    wmax, lam = 100.0, 0.8
    w = np.linspace(1e-6, wmax, 400001)
    a2f = sc.alpha2F_debye(w, lam, wmax)
    norm = 2.0 * _trap(a2f / w, w)
    resid = abs(norm - lam) / lam
    ok = resid < 1e-4
    _record("AF1", "2 int alpha^2F/omega = lambda (spectral weight normalization)",
            "numeric", resid, ok, {"norm": norm})
    assert ok


def test_AF2_omega_log_equals_omega_max_over_sqrt_e():
    """omega_log = omega_max/sqrt(e) for the omega^2 spectrum (exact)."""
    wmax = 137.0
    resid = abs(sc.omega_log_of_alpha2F_debye(wmax) - wmax / math.sqrt(math.e))
    inv = abs(sc.omega_max_from_omega_log(wmax / math.sqrt(math.e)) - wmax)
    ok = resid < 1e-9 and inv < 1e-9
    _record("AF2", "omega_log = omega_max/sqrt(e) (Debye omega^2 spectrum)",
            "exact", max(resid, inv), ok)
    assert ok


def test_AF3_debye_matsubara_kernel_closed_form():
    """lambda(nu) closed form = 2 int alpha^2F omega/(omega^2+nu^2) d omega."""
    wmax, lam = 100.0, 0.8
    w = np.linspace(1e-6, wmax, 400001)
    a2f = sc.alpha2F_debye(w, lam, wmax)
    worst = 0.0
    for nu in (50.0, 150.0, 400.0):
        num = 2.0 * _trap(a2f * w / (w ** 2 + nu ** 2), w)
        cf = float(sc.lambda_nu_debye(nu, lam, wmax))
        worst = max(worst, abs(num - cf))
    ok = worst < 1e-4
    _record("AF3", "Debye Matsubara kernel lambda(nu) closed form matches integral",
            "numeric", worst, ok)
    assert ok


def test_AF4_tc_shape_insensitive_at_fixed_omega_log():
    """At fixed omega_log the Debye and Einstein T_c agree to a few % -- T_c is
    set by (lambda, omega_log, mu*), not spectral shape.  This is why F215's
    single Einstein mode reproduced the measured T_c."""
    diffs = {}
    for el, (lam, mus, wlog, thetaD, tc) in sc.REAL_SUPERCONDUCTORS.items():
        te = sc.eliashberg_tc(lam, wlog, mus, spectrum="einstein")
        td = sc.eliashberg_tc(lam, wlog, mus, spectrum="debye")
        diffs[el] = abs(td - te) / te
    worst = max(diffs.values())
    ok = worst < 0.08
    _record("AF4", "T_c shape-insensitive at fixed omega_log (Einstein ~ Debye)",
            "numeric", worst, ok, {"rel_diff": diffs})
    assert ok


# --------------------------- Part B ---------------------------------------
def test_PA1_weak_coupling_ratio_recovers_BCS():
    """Padé-continued gap ratio for the weakest-coupling element (Al) is near
    the BCS 3.53."""
    lam, mus, wlog = sc.REAL_SUPERCONDUCTORS["Al"][0], \
        sc.REAL_SUPERCONDUCTORS["Al"][1], sc.REAL_SUPERCONDUCTORS["Al"][2]
    r = sc.gap_edge_real_axis(lam, wlog, mus)["ratio"]
    resid = abs(r - 3.528) / 3.528
    ok = resid < 0.06
    _record("PA1", "Padé gap ratio -> 3.53 (BCS) for weak-coupling Al",
            "numeric", resid, ok, {"ratio_Al": r})
    assert ok


def test_PA2_strong_coupling_ratio_rises_dynamically():
    """The strong-coupling reduced gap emerges from Padé continuation (no fit):
    Pb, Hg exceed 4.3, and the whole set correlates with measured at r>0.98."""
    els, pred, meas = [], [], []
    for el, (lam, mus, wlog, thetaD, tc) in sc.REAL_SUPERCONDUCTORS.items():
        r = sc.gap_edge_real_axis(lam, wlog, mus)["ratio"]
        els.append(el); pred.append(r); meas.append(MEAS_RATIO[el])
    pred, meas = np.array(pred), np.array(meas)
    corr = float(np.corrcoef(pred, meas)[0, 1])
    pb = pred[els.index("Pb")]; hg = pred[els.index("Hg")]
    ok = pb > 4.3 and hg > 4.3 and corr > 0.98
    _record("PA2", "strong-coupling 2Delta/kTc rises dynamically (Pb,Hg>4.3); corr>0.98",
            "numeric", 1.0 - corr, ok,
            {"corr": corr, "Pb": float(pb), "Hg": float(hg),
             "ratios": {e: round(float(p), 2) for e, p in zip(els, pred)}})
    assert ok


def test_PA3_debye_spectrum_tightens_gap_ratio():
    """The first-principles Debye alpha^2F improves the gap ratio vs the single
    Einstein mode -- the gap ratio is shape-sensitive (where T_c is not)."""
    err_e, err_d = [], []
    for el, (lam, mus, wlog, thetaD, tc) in sc.REAL_SUPERCONDUCTORS.items():
        re = sc.gap_edge_real_axis(lam, wlog, mus, spectrum="einstein")["ratio"]
        rd = sc.gap_edge_real_axis(lam, wlog, mus, spectrum="debye")["ratio"]
        m = MEAS_RATIO[el]
        err_e.append(abs(re - m) / m); err_d.append(abs(rd - m) / m)
    me, md = float(np.mean(err_e)), float(np.mean(err_d))
    ok = md < me
    _record("PA3", "Debye alpha^2F tightens gap ratio vs Einstein (shape-sensitive)",
            "numeric", md, ok, {"mean_err_einstein": me, "mean_err_debye": md})
    assert ok


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    npass = 0
    for t in tests:
        try:
            t(); npass += 1; print(f"  PASS  {t.__name__}")
        except AssertionError:
            print(f"  FAIL  {t.__name__}")
    out = {"finding": "F218",
           "title": "First-principles alpha^2F + Padé dynamic gap ratio",
           "n_pass": npass, "n_total": len(tests), "checks": RESULTS}
    out_dir = os.path.abspath(os.path.join(_HERE, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "F218_alpha2F_and_pade_gap.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{npass}/{len(tests)} PASS   ->  test-results/F218_alpha2F_and_pade_gap.json")
    return npass == len(tests)


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
