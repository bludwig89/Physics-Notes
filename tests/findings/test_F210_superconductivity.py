#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F210_superconductivity.py
==============================

F210 — Electrical (electronic) superconductivity on the lattice, built as the
electric S-dual of the F86 magnetic dual-superconductor.  Verifies the six
tasks of the construction with tiered checks (exact > machine > numeric).

The two crown-jewel targets are COUPLING-INDEPENDENT and therefore the honest
tests that this is genuine BCS, not a fit:
    SC2a  2 Delta(0)/kTc  -> 2 pi / e^gamma = 3.5277539777   (machine precision)
    SC2b  dC/C_n          =  12 / (7 zeta(3)) = 1.4261269     (machine precision)

Runs standalone (`python3 test_F210_superconductivity.py`) or under pytest.
Pure numpy; no scipy.  Module: src/casim/engine/interactions/superconductivity.py.
"""
from __future__ import annotations

import os
import sys
import json
import math
import numpy as np

# --- import the kernel (mirror repo convention; conftest also adds this) ----
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import superconductivity as sc  # noqa: E402

RESULTS = {}


def _record(cid, statement, tier, residual, passed, extra=None):
    RESULTS[cid] = {"statement": statement, "tier": tier,
                    "residual": float(residual), "pass": bool(passed)}
    if extra:
        RESULTS[cid].update(extra)


# ---------------------------------------------------------------------------
# Task 1 -- the pairing glue (attractive channel)
# ---------------------------------------------------------------------------
def test_SC1a_phonon_term_attractive_below_omega_q():
    """Retarded phonon exchange is ATTRACTIVE for |omega| < omega_q, repulsive
    above.  Exact sign statement."""
    wq, g2 = 1.0, 0.3
    below = sc.phonon_attractive(0.5 * wq, wq, g2)
    above = sc.phonon_attractive(2.0 * wq, wq, g2)
    ok = (below < 0.0) and (above > 0.0)
    _record("SC1a", "phonon exchange attractive for |w|<w_q, repulsive above",
            "exact", 0.0 if ok else 1.0, ok,
            {"V_below": below, "V_above": above})
    assert ok


def test_SC1b_small_q_constant_contact():
    """The small-q static limit of the acoustic-phonon attraction is a CONSTANT
    (q-independent) -V = -D^2/(rho c_s^2): the BCS contact interaction emerges
    with no extra assumption.  Check q-independence across a decade of q."""
    D, rho, c_s = 1.7, 2.0, 1.0 / math.sqrt(3.0)
    Vconst = sc.small_q_contact_limit(D, rho, c_s)
    # explicit V_ph(q,0) = -2 g_q^2/omega_q with g_q^2 = D^2 q^2/(2 rho omega_q)
    vals = []
    for q in (1e-3, 1e-2, 1e-1):
        wq = c_s * q
        g2 = D ** 2 * q ** 2 / (2.0 * rho * wq)
        vals.append(sc.phonon_attractive(0.0, wq, g2))  # V_ph(q,0)
    vals = np.array(vals)
    spread = float(np.max(np.abs(vals - vals[0])))
    # each should equal -Vconst
    resid = float(np.max(np.abs(vals + Vconst)))
    ok = spread < 1e-12 and resid < 1e-12
    _record("SC1b", "small-q phonon attraction is q-independent constant -V (BCS contact)",
            "exact", max(spread, resid), ok, {"V_const": Vconst})
    assert ok


def test_SC1c_debye_cutoff_is_a_lattice_quantity():
    """omega_D = c_s * (pi/a_mat): tied to the emergent elastic sector, not fit."""
    c_s, a = 1.0 / math.sqrt(3.0), 2.5
    wD = sc.debye_from_elastic(c_s, a)
    ok = abs(wD - c_s * math.pi / a) < 1e-15
    _record("SC1c", "Debye cutoff = c_s * BZ edge (lattice quantity)",
            "exact", abs(wD - c_s * math.pi / a), ok, {"omega_D": wD})
    assert ok


# ---------------------------------------------------------------------------
# Task 2 -- the gap equation (== F77 NJL gap) and universal ratios
# ---------------------------------------------------------------------------
def test_SC2a_universal_gap_ratio():
    """2 Delta(0)/kTc -> 2 pi/e^gamma, coupling- AND omega_D-independent."""
    exact = sc.bcs_ratio_weak_coupling_limit()
    r_weak = sc.universal_gap_ratio(0.05, 1.0)          # deep weak coupling
    resid = abs(r_weak - exact) / exact
    # omega_D independence (exact): same coupling, different cutoff
    r1 = sc.universal_gap_ratio(0.1, 1.0)
    r2 = sc.universal_gap_ratio(0.1, 1000.0)
    wD_indep = abs(r1 - r2)
    ok = resid < 1e-12 and wD_indep < 1e-12
    _record("SC2a", "2 Delta(0)/kTc = 2 pi/e^gamma = 3.5277539777 (coupling & cutoff independent)",
            "machine", max(resid, wD_indep), ok,
            {"exact": exact, "ratio_N0V0.05": r_weak, "wD_independence": wD_indep})
    assert ok


def test_SC2b_specific_heat_jump():
    """dC/C_n = 12/(7 zeta(3)) = 1.4261269, verified to machine precision."""
    val = sc.specific_heat_jump()
    exact = 12.0 / (7.0 * 1.2020569031595942854)   # high-precision zeta(3)
    resid = abs(val - exact)
    ok = resid < 1e-9
    _record("SC2b", "specific-heat jump dC/C_n = 12/(7 zeta3) = 1.4261269",
            "machine", resid, ok, {"value": val})
    assert ok


def test_SC2c_delta_of_T_slope_near_Tc():
    """Delta^2(T) -> (8 pi^2/7 zeta3)(kTc)^2 (1 - T/Tc) as T->Tc: the relation
    behind SC2b, confirmed from the self-consistent finite-T gap."""
    N0V, wD = 0.15, 1.0
    kTc = sc.Tc(N0V, wD)
    pred = 8.0 * math.pi ** 2 / (7.0 * sc.zeta3()) * kTc ** 2
    eps = 2e-4
    d2 = sc.gap_at_T(N0V, wD, (1 - eps) * kTc) ** 2
    ratio = (d2 / eps) / pred
    resid = abs(ratio - 1.0)
    ok = resid < 5e-3
    _record("SC2c", "Delta^2(T) near-Tc slope matches 8 pi^2/(7 zeta3) (kTc)^2",
            "numeric", resid, ok, {"slope_ratio": ratio})
    assert ok


def test_SC2d_gap_equation_is_F77_form():
    """The T=0 gap Delta = omega_D/sinh(1/N0V) is the closed form of
    1 = N0V * arcsinh(omega_D/Delta) -- structurally the F77 NJL gap
    1 = (coupling) x (loop integral).  Check the closed form solves it."""
    N0V, wD = 0.3, 1.0
    D = sc.gap_T0(N0V, wD)
    lhs = N0V * math.asinh(wD / D)
    resid = abs(lhs - 1.0)
    ok = resid < 1e-14
    _record("SC2d", "T=0 gap solves 1 = N0V arcsinh(wD/Delta) (F77-form gap eq)",
            "machine", resid, ok, {"Delta0": D})
    assert ok


# ---------------------------------------------------------------------------
# Task 3 -- the Cooper pair (charged spin-0 singlet)
# ---------------------------------------------------------------------------
def test_SC3a_pair_charge_2e_exact():
    q = sc.pair_charge_units()
    ok = (q == 2)
    _record("SC3a", "Cooper-pair charge = 2e exactly (integer holonomy, F87)",
            "exact", 0.0 if ok else 1.0, ok)
    assert ok


def test_SC3b_pair_winding_and_singlet():
    """Pair phase winds twice (F69 phase-sum) -> factor 2 for Phi0=h/2e; the
    channel is the spin-0 s-wave singlet."""
    w = sc.pair_phase_winding(1)
    qn = sc.pair_spin_singlet_check()
    ok = (w == 2) and (qn["total_spin"] == 0) and (qn["parity"] == 1) \
        and (qn["statistics"] == "boson")
    _record("SC3b", "pair winds 2x (F69 sum) + spin-0 s-wave singlet boson",
            "exact", 0.0 if ok else 1.0, ok)
    assert ok


# ---------------------------------------------------------------------------
# Task 4 -- Meissner effect / London depth (Stueckelberg photon mass)
# ---------------------------------------------------------------------------
def test_SC4a_massive_photon_reduces_to_even_photon():
    """omega^2 = m_gamma^2 + (c_lat k)^2; at m_gamma=0 it is exactly the free
    luminal even-law F69 photon (never the birefringent sigma-bilinear)."""
    k = 0.37
    free = sc.massive_photon_omega(k, 0.0)
    resid = abs(free - (1.0 / math.sqrt(3.0)) * k)
    ok = resid < 1e-15
    _record("SC4a", "massive photon m=0 reduces to luminal even photon c_lat*k",
            "exact", resid, ok)
    assert ok


def test_SC4b_meissner_penetration_depth():
    """Field expelled as B ~ exp(-x/lambda_L); the numerically-solved London
    BVP recovers the analytic penetration depth."""
    lam = 3.0
    x, B = sc.meissner_slab_solve(L=60.0, dx=0.02, lambda_L=lam)
    m = (x > 2) & (x < 20)
    slope = np.polyfit(x[m], np.log(B[m]), 1)[0]
    lam_meas = -1.0 / slope
    resid = abs(lam_meas - lam) / lam
    ok = resid < 1e-4
    _record("SC4b", "Meissner B-expulsion decay length = lambda_L (=1/m_gamma)",
            "numeric", resid, ok, {"lambda_measured": lam_meas})
    assert ok


def test_SC4c_london_depth_scales_with_pair_charge():
    """lambda_L^2 = m*/(mu0 n_s (2e)^2): using 2e (pairs) vs e (singles) shifts
    lambda_L by exactly 1/2 -- the pair-charge signature in the screening."""
    ns, mstar = 1e28, 9.11e-31
    lam_pair = sc.london_depth(ns, mstar, mu0=1.256637e-6, q=2 * sc.E_CHARGE)
    lam_single = sc.london_depth(ns, mstar, mu0=1.256637e-6, q=sc.E_CHARGE)
    ratio = lam_single / lam_pair
    resid = abs(ratio - 2.0)
    ok = resid < 1e-12
    _record("SC4c", "lambda_L(2e)/lambda_L(e) = 1/2 exactly (pair-charge signature)",
            "exact", resid, ok, {"lambda_pair_m": lam_pair})
    assert ok


# ---------------------------------------------------------------------------
# Task 5 -- flux quantization + Josephson
# ---------------------------------------------------------------------------
def test_SC5a_flux_quantum_h_over_2e():
    """Phi0 = h/2e exactly; and it is HALF the single-carrier h/e."""
    phi0 = sc.flux_quantum(1)
    exact = sc.H_PLANCK / (2.0 * sc.E_CHARGE)
    resid = abs(phi0 - exact)
    ratio = sc.PHI0_SINGLE / phi0
    ok = resid < 1e-30 and abs(ratio - 2.0) < 1e-14
    _record("SC5a", "flux quantum Phi0 = h/2e = 2.0678e-15 Wb (= half h/e; carriers are pairs)",
            "exact", max(resid, abs(ratio - 2.0)), ok, {"Phi0": phi0})
    assert ok


def test_SC5b_type_II_kappa_threshold():
    """kappa = lambda_L/xi0 vs 1/sqrt2 separates type I/II (S-dual of F86 tube)."""
    kappa_II = sc.ginzburg_landau_kappa(100e-9, 5e-9)   # lambda>>xi -> type II
    kappa_I = sc.ginzburg_landau_kappa(40e-9, 200e-9)   # lambda<<xi -> type I
    thr = 1.0 / math.sqrt(2.0)
    ok = (kappa_II > thr) and (kappa_I < thr)
    _record("SC5b", "kappa = lambda_L/xi0 sorts type I (<1/sqrt2) vs II (>1/sqrt2)",
            "exact", 0.0 if ok else 1.0, ok,
            {"kappa_II": kappa_II, "kappa_I": kappa_I, "threshold": thr})
    assert ok


def test_SC5c_josephson_relations():
    """DC: I = Ic sin(dtheta).  AC: a constant bias V makes I(t) oscillate at
    f_J = 2eV/h (the Josephson frequency)."""
    Ic, V = 1e-3, 1e-6
    # DC current-phase relation
    dth = np.linspace(0, 2 * math.pi, 9)
    I = sc.josephson_dc(Ic, dth)
    dc_ok = abs(I.max() - Ic) < 1e-15 and abs(I.min() + Ic) < 1e-15
    # AC frequency: recover f_J from the evolved current's phase advance
    fJ_pred = 2.0 * sc.E_CHARGE * V / sc.H_PLANCK
    dt = 1.0 / (fJ_pred * 200)          # 200 samples/period
    t, dtheta, Icur = sc.josephson_evolve(Ic, V, dt, 400)
    fJ_meas = (dtheta[-1] - dtheta[0]) / (2 * math.pi) / (t[-1] - t[0])
    resid = abs(fJ_meas - fJ_pred) / fJ_pred
    ok = dc_ok and resid < 1e-10
    _record("SC5c", "Josephson DC I=Ic sin(dtheta) & AC f_J=2eV/h",
            "machine", resid, ok, {"f_J_pred": fJ_pred, "f_J_meas": fJ_meas})
    assert ok


# ---------------------------------------------------------------------------
# Task 6 -- zero DC resistance / persistent current
# ---------------------------------------------------------------------------
def test_SC6_persistent_vs_normal_current():
    """London eq.1 with E=0 => dJ/dt=0: the supercurrent is a constant of
    motion (persistent, exact).  A Drude (T>Tc) control decays."""
    t, J = sc.supercurrent_evolve(1.0, 0.1, 1000, E=0.0)
    drift = float(abs(J[-1] - J[0]))
    tn, Jn = sc.normal_current_evolve(1.0, 0.1, 1000, tau=2.0)
    decayed = float(Jn[-1])
    ok = drift == 0.0 and decayed < 1e-20
    _record("SC6", "persistent supercurrent dJ/dt=0 (E=0); normal control decays",
            "exact", drift, ok, {"persistent_drift": drift, "normal_final": decayed})
    assert ok


# ---------------------------------------------------------------------------
def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    npass = 0
    for t in tests:
        try:
            t()
            npass += 1
            print(f"  PASS  {t.__name__}")
        except AssertionError:
            print(f"  FAIL  {t.__name__}")
    out = {"finding": "F210", "title": "Electrical superconductivity on the lattice",
           "n_pass": npass, "n_total": len(tests), "checks": RESULTS}
    out_dir = os.path.abspath(os.path.join(_HERE, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "F210_superconductivity.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{npass}/{len(tests)} PASS   ->  test-results/F210_superconductivity.json")
    return npass == len(tests)


if __name__ == "__main__":
    ok = _run_all()
    sys.exit(0 if ok else 1)
