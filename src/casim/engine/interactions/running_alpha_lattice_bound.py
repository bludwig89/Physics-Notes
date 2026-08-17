"""running_alpha_lattice_bound.py — the B9 re-derivation, post-F277 (F322).

WHY THIS MODULE EXISTS
======================
Rubric row B9 (`docs/status/completeness-2026-08-07.md`) is graded QUANT on one
number: the leptonic Delta alpha(M_Z) agreeing with PDG to 0.24%, from F251 Pi4.
F251 is superseded by S12-F277, which flipped a vacuum-polarization sign, and the
0.24% was flagged un-re-derived for THREE consecutive reports (gap #5a). This
module is that re-derivation. It answers two questions the flag conflated:

  ACCOUNTING  does the 0.24% depend on the refolded path at all?  It does NOT.
              `leptonic_running`'s call closure is {_dalpha_lepton}; `_fermion_B`
              and `_K_lat` are not in it. L1 below measures this rather than
              asserting it: the kernel is violently perturbed and the number is
              required to come back BITWISE identical. So the flag was an
              accounting statement, the same shape as the A11/B12/B11 residuals
              that Amendments 6-8 found mis-stated rather than hard.

  PHYSICS     what the flag should have asked, and nobody had computed: the
              0.24% is a CONTINUUM closed form (alpha/3pi)[ln(s/m^2) - 5/3], so
              what is the model's own LATTICE content in the running, and does it
              leave Delta alpha alone at the precision being quoted?

THE DERIVATION (L2) — q-flatness IS Delta alpha invariance
==========================================================
For q = (Q,0,0,0) Euclidean, transversality gives Pi^{mn} = (q^2 d^{mn} - q^m q^n)
Pi(q^2), so `_fermion_B` = (Pi00 - Pi11)/Q^2 = -Pi(q^2). The running is a
SUBTRACTED object, Delta alpha(s) = Pi(0) - Pi(s), so any q-INDEPENDENT additive
constant in Pi cancels exactly. F251's Pi3 measures exactly that constant:
Delta(Q) = B_rule - B_cont. Hence

    Delta alpha_lattice(s) - Delta alpha_cont(s) = f * [Delta(s) - Delta(0)]

and Pi3's q-flatness is not merely "the log coefficient is propagator-independent"
-- it is the statement that the lattice leaves Delta alpha itself invariant. The
conversion f is EXACT and model-internal, fixed by the module's own b0 gate: the
UV log coefficient is b0^QED/(16 pi^2) = (4/3)/(16 pi^2) = 1/(12 pi^2) in B units,
against d(Delta alpha)/d ln s = alpha/(3 pi) physically, so

    f = (alpha/3pi) / (1/(12 pi^2)) = 4 pi alpha        (L2a asserts this)

A measured spread in Delta over a log range therefore converts to an absolute
bound on the lattice's contribution to Delta alpha(M_Z), by treating the residual
non-flatness as a residual log and extrapolating over ln(M_Z^2/m_e^2). That bound
is what B9 never had.

WHAT IT SHOWS — F277 did not change the number, it created its WARRANT
=====================================================================
Post-F277 the bound is ~1e-5 and FALLS with grid refinement (grid noise, no
residual log): 0.09-0.33x the 7.71e-5 shortfall to PDG. With the refold restored
the bound is ~1.4e-2 and is n-INDEPENDENT (the signature of a genuine spurious
log): 170-190x the shortfall, and 41-46% of Delta alpha itself. So before F277 the
quoted "matches PDG to 0.24%" had a lattice uncertainty ~190x LARGER than the
agreement it claimed -- the number was right and unwarranted at the same time.
That, not a changed value, is the answer to gap #5a.

AND THE 0.24% IS NOW ATTRIBUTED (L3)
====================================
The shortfall is two-loop. F261's two-loop QED beta is sympy-exact, b1 = 1 per
unit-charge fermion in d(1/alpha)/dln mu^2 = -(1/4pi)(b0 + b1 (alpha/pi) + ...),
which gives a two-loop leading-log term alpha^2 L/(4 pi^2) per lepton. It was
never fed into the running. Doing so closes ~80% of the shortfall with the right
sign and moves B9's number 0.245% -> 0.049%. The remainder is the two-loop
non-log constant plus three loops, NOT derived here.

THE EW LEG (L4)
===============
B9's other half is graded on F115 (2026-06-08), whose CM2 ran the bare angle from
the Planck scale and overshot by -74%. F138/F231 superseded that reading: 1/4 is
the compositeness-scale matching at mu* = 4 pi v = 3094 GeV, and one-loop
Higgs-free running to M_Z gives sin^2 theta_W = 0.23173, +0.222% vs PDG MS-bar.
L4 reproduces that and then measures what nobody had: the EW leg takes
alpha_em(M_Z) as an INPUT, and on the model's own leptonic-only alpha -- i.e.
without the hadronic vacuum polarization the model does not derive (row G3) -- the
residual DOUBLES to +0.450%. So B9's two halves share one input and half the EW
leg's precision is owed to it.

No new constants: reference values are imported from qed_vacuum_polarization
(single source) and the registry (D7). Real arithmetic only -- no chiral
transforms anywhere here (CLAUDE.md).
"""
from __future__ import annotations

import math

from casim.numerics import xp as np
from casim.constants import sin2_thetaW_uv_f
from casim.engine.interactions import qed_vacuum_polarization as vp
from casim.engine.interactions import qed_twoloop_ae as tl

# ---- reference values: imported, never re-declared (single source = F251 module)
ALPHA_INV = vp.ALPHA_INV
ALPHA = vp.ALPHA
M_Z_MEV = vp.M_Z_MEV
M_LEPTON_MEV = vp.M_LEPTON_MEV
DALPHA_LEP_PDG = vp.DALPHA_LEP_PDG
B0_QED = vp.B0_QED

# PDG MS-bar EW reference block (F138's inputs, quoted there; not model outputs)
INV_ALPHA_EM_MZ_MSBAR = 127.951
SIN2_MZ_MSBAR_PDG = 0.23122
V_EW_GEV = 246.22
M_Z_GEV = 91.1876
ALPHA_MZ_INV_ONSHELL = vp.ALPHA_MZ_INV_MEAS


# ======================================================================
#  L1 — the 0.24% is refold-independent (measured, not asserted)
# ======================================================================
def refold_independence() -> dict:
    """Perturb the lattice kernel violently and require Delta alpha_lep to come
    back BITWISE identical. This is the accounting answer to gap #5a: the number
    B9 is graded on cannot have moved under F277, because it never touched the
    refolded path."""
    base = vp.leptonic_running()["delta_alpha_lep"]
    orig = vp._K_lat
    try:
        vp._K_lat = lambda kx, ky, kz, kt: 7.3 * orig(kx, ky, kz, kt) + 0.5
        pert = vp.leptonic_running()["delta_alpha_lep"]
    finally:
        vp._K_lat = orig
    return {
        "delta_alpha_lep_base": base,
        "delta_alpha_lep_kernel_perturbed": pert,
        "bitwise_identical": base == pert,
        "call_closure_of_leptonic_running": ["_dalpha_lepton"],
        "statement": "leptonic_running() does not reach _fermion_B or _K_lat; a "
                     "7.3x + 0.5 kernel perturbation leaves Delta alpha bitwise "
                     "unchanged. The three-report flag was accounting, not physics.",
    }


# ======================================================================
#  L2 — the lattice bound on Delta alpha(M_Z)
# ======================================================================
def b_to_dalpha_factor() -> dict:
    """f = 4 pi alpha, derived from the module's own b0^QED = 4/3 gate.

    B units:   dB/d ln(1/Q^2) = -b0/(16 pi^2) = -1/(12 pi^2)
    physical:  d(Delta alpha)/d ln s = alpha/(3 pi)      per unit-charge fermion
    =>         f = (alpha/3pi) * 12 pi^2 = 4 pi alpha
    """
    slope_B = B0_QED / (16.0 * math.pi ** 2)
    f = (ALPHA / (3.0 * math.pi)) / slope_B
    return {
        "b0_QED": B0_QED,
        "slope_in_B_units": slope_B,
        "slope_is_1_over_12pi2": abs(slope_B - 1.0 / (12 * math.pi ** 2)) < 1e-15,
        "f": f,
        "f_is_4pi_alpha": abs(f - 4.0 * math.pi * ALPHA) < 1e-15,
        "statement": "f = 4 pi alpha exactly, from b0^QED = 4/3. Model-internal: no "
                     "fit, no external normalisation.",
    }


def _fermion_B_refold(Q: float, n: int, kernel: str, refold: bool) -> float:
    """`vp._fermion_B` with the F277-removed modular refold optionally restored.
    The refold is the CONTROL knob, so it lives here and not in the physics
    module (whose line stays removed -- F277 T6 asserts that at source level)."""
    if not refold or kernel != "rule":
        return vp._fermion_B(Q, n, kernel)
    ax = (np.arange(n) + 0.5) / n * 2 * math.pi - math.pi
    KX, KY, KZ, KT = np.meshgrid(ax, ax, ax, ax, indexing="ij")
    kq = [KX + Q, KY, KZ, KT]
    kc = [KX, KY, KZ, KT]
    kdotkq = sum(kc[i] * kq[i] for i in range(4))

    def N(m, nn):
        d = 1.0 if m == nn else 0.0
        return 4.0 * (kc[m] * kq[nn] + kc[nn] * kq[m] - d * kdotkq)

    KXQ = ((KX + Q + math.pi) % (2 * math.pi)) - math.pi     # the F277 defect
    denom = vp._K_lat(KX, KY, KZ, KT) * vp._K_lat(KXQ, KY, KZ, KT)
    return (float(np.mean(N(0, 0) / denom))
            - float(np.mean(N(1, 1) / denom))) / Q ** 2


def lattice_bound_on_dalpha(n_grid=(20, 24, 28), Qs=(0.1, 0.15, 0.2, 0.3),
                            refold_control: bool = False) -> dict:
    """Convert the measured q-non-flatness of Delta = B_rule - B_cont into an
    absolute bound on the lattice's contribution to Delta alpha(M_Z).

    refold_control=True restores the F277 defect. It is the D9/H2 control: the
    bound must then EXCEED the PDG shortfall and must stop falling with n.
    """
    f = b_to_dalpha_factor()["f"]
    ln_fit = math.log(max(Qs) ** 2) - math.log(min(Qs) ** 2)
    L_phys = math.log(M_Z_MEV ** 2 / M_LEPTON_MEV["e"] ** 2)
    shortfall = DALPHA_LEP_PDG - vp.leptonic_running()["delta_alpha_lep"]
    rows = []
    for n in n_grid:
        d = [_fermion_B_refold(Q, n, "rule", refold_control)
             - _fermion_B_refold(Q, n, "cont", refold_control) for Q in Qs]
        spread = max(d) - min(d)
        bound = f * (spread / ln_fit) * L_phys
        rows.append({"n": n, "delta_mean": float(np.mean(d)),
                     "delta_spread": spread,
                     "residual_log_slope": spread / ln_fit,
                     "dalpha_bound": bound,
                     "bound_over_shortfall": bound / shortfall,
                     "bound_frac_of_dalpha": bound / DALPHA_LEP_PDG})
    bounds = [r["dalpha_bound"] for r in rows]
    return {
        "refold_control": refold_control,
        "f_4pi_alpha": f, "ln_range_fitted": ln_fit, "L_physical": L_phys,
        "pdg_shortfall": shortfall,
        "rows": rows,
        "bound_max": max(bounds),
        "bound_below_shortfall_at_every_n": all(
            r["bound_over_shortfall"] < 1.0 for r in rows),
        "bound_ratio_max_n_over_min_n": bounds[-1] / bounds[0],
        "bound_falls_fast_with_n": bounds[-1] / bounds[0] < 0.7,
        "statement": "q-flatness of Delta = B_rule - B_cont IS invariance of "
                     "Delta alpha, because a q-independent constant in Pi cancels "
                     "in Pi(0) - Pi(s). Post-F277 the bound is ~1e-5 and falls "
                     "with n (grid noise); with the refold it is ~1.4e-2 and is "
                     "n-independent (a real spurious log). The ratio "
                     "bound(n_max)/bound(n_min) is the discriminator: ~0.40 "
                     "post-F277 vs ~0.97 refolded.",
    }


# ======================================================================
#  L3 — attributing the shortfall: the model's own two-loop b1
# ======================================================================
def two_loop_leading_log(b1_control=None) -> dict:
    """Add the two-loop leading log alpha^2 L/(4 pi^2) per lepton, whose b1 = 1
    is sympy-exact in F261, to the one-loop leptonic running.

    b1_control overrides b1 (the D9/H2 control for this leg).
    """
    beta = tl.two_loop_beta_symbolic()
    b1 = float(beta["b1_QED"]) if b1_control is None else float(b1_control)
    s = M_Z_MEV ** 2
    one, two, per = 0.0, 0.0, {}
    for name, m in M_LEPTON_MEV.items():
        L = math.log(s / m ** 2)
        d1 = (ALPHA / (3.0 * math.pi)) * (L - 5.0 / 3.0)
        d2 = b1 * (ALPHA ** 2 / (4.0 * math.pi ** 2)) * L
        one += d1
        two += d2
        per[name] = {"L": L, "one_loop": d1, "two_loop_LL": d2}
    shortfall = DALPHA_LEP_PDG - one
    return {
        "b1_QED_from_F261": beta["b1_QED"],
        "b1_used": b1,
        "two_loop_beta_exact": beta["two_loop_matches_1_over_2pi2"],
        "per_lepton": per,
        "delta_alpha_one_loop": one,
        "delta_alpha_two_loop_LL": two,
        "delta_alpha_total": one + two,
        "pdg": DALPHA_LEP_PDG,
        "rel_err_one_loop": abs(one - DALPHA_LEP_PDG) / DALPHA_LEP_PDG,
        "rel_err_with_two_loop": abs(one + two - DALPHA_LEP_PDG) / DALPHA_LEP_PDG,
        "shortfall_one_loop": shortfall,
        "frac_of_shortfall_closed": two / shortfall,
        "alpha_MZ_inv_lep_one_loop": ALPHA_INV * (1.0 - one),
        "alpha_MZ_inv_lep_two_loop": ALPHA_INV * (1.0 - one - two),
        "residual_after_two_loop_LL": DALPHA_LEP_PDG - one - two,
        "statement": "The 0.245% shortfall is two-loop. F261's sympy-exact b1 = 1 "
                     "closes ~80% of it with the correct sign, moving B9's number "
                     "to 0.049%. The two-loop non-log constant and three loops are "
                     "NOT derived here.",
    }


# ======================================================================
#  L4 — the EW leg, and the input its precision is owed to
# ======================================================================
def _sin2_MZ(inv_aem: float, n_gen: int = 3, n_higgs: int = 0) -> dict:
    """One-loop GUT-normalised running of sin^2 theta_W down from mu* = 4 pi v
    with the EXACT anchor sin^2 theta_W(mu*) = sin2_thetaW_uv = 1/4 (F138)."""
    b1 = (4.0 / 3.0) * n_gen + 0.1 * n_higgs
    b2 = -22.0 / 3.0 + (4.0 / 3.0) * n_gen + n_higgs / 6.0
    mu_star = 4.0 * math.pi * V_EW_GEV
    L = math.log(mu_star / M_Z_GEV)
    bem = b2 + (5.0 / 3.0) * b1
    inv_a2_MZ = sin2_thetaW_uv_f * (inv_aem - (bem / (2 * math.pi)) * L) \
        + (b2 / (2 * math.pi)) * L
    s2 = inv_a2_MZ / inv_aem
    return {"mu_star_GeV": mu_star, "b1": b1, "b2": b2, "inv_alpha_em_MZ": inv_aem,
            "sin2_MZ": s2,
            "resid_vs_PDG_msbar_pct": 100.0 * (s2 - SIN2_MZ_MSBAR_PDG)
            / SIN2_MZ_MSBAR_PDG}


def ew_leg_alpha_dependence() -> dict:
    """Reproduce F138's +0.222%, then re-run it on the model's OWN alpha(M_Z) --
    leptonic only, i.e. without the hadronic vacuum polarization the model does
    not derive (row G3) -- and report how much of the precision was owed to it."""
    pdg = _sin2_MZ(INV_ALPHA_EM_MZ_MSBAR)
    tll = two_loop_leading_log()
    # scheme-match: shift the model's on-shell 1/alpha by the measured
    # on-shell -> MS-bar offset before feeding the EW running.
    offset = ALPHA_MZ_INV_ONSHELL - INV_ALPHA_EM_MZ_MSBAR
    inv_model_msbar = tll["alpha_MZ_inv_lep_two_loop"] - offset
    model = _sin2_MZ(inv_model_msbar)
    return {
        "with_pdg_alpha": pdg,
        "with_model_leptonic_alpha": model,
        "onshell_to_msbar_offset": offset,
        "hadronic_gap_in_inv_alpha_msbar": inv_model_msbar - INV_ALPHA_EM_MZ_MSBAR,
        "residual_ratio_model_over_pdg": abs(model["resid_vs_PDG_msbar_pct"])
        / abs(pdg["resid_vs_PDG_msbar_pct"]),
        "sensitivity_dsin2_d_invalpha": -(pdg["sin2_MZ"] - sin2_thetaW_uv_f)
        / INV_ALPHA_EM_MZ_MSBAR,
        "statement": "F138's +0.222% is reproduced. On the model's own "
                     "leptonic-only alpha(M_Z) it degrades to +0.450% -- so half "
                     "of B9's EW precision is owed to the hadronic vacuum "
                     "polarization the model defers to row G3. B9's two halves "
                     "share one input.",
    }


# ======================================================================
#  Entry point — the registry record's `entry:`
# ======================================================================
def check_b9_rederivation(n_grid=(20, 24, 28), refold_control: bool = False,
                          b1_control=None) -> dict:
    """B9's re-derivation, six legs.

    Returns a `checks:` leg map and an `all_pass:` verdict rather than raising, so
    that a D9/H2 control can be read off WHICH legs went red (an AssertionError
    hands the runner no payload and scores INVALID, per `runner._entry_payload`).
    `all_pass` is the recognised verdict key in `runner._overall`, and it is this
    record's failure route.
    """
    L1 = refold_independence()
    L2a = b_to_dalpha_factor()
    L2 = lattice_bound_on_dalpha(n_grid=n_grid, refold_control=refold_control)
    L3 = two_loop_leading_log(b1_control=b1_control)
    L4 = ew_leg_alpha_dependence()

    checks = {
        "B9-1": {"ok": bool(L1["bitwise_identical"]),
                 "what": "Delta alpha_lep bitwise refold-independent"},
        "B9-2": {"ok": bool(L2a["slope_is_1_over_12pi2"] and L2a["f_is_4pi_alpha"]),
                 "what": "f = 4 pi alpha exact from b0^QED = 4/3",
                 "f": L2a["f"]},
        "B9-3": {"ok": bool(L2["bound_below_shortfall_at_every_n"]),
                 "what": "lattice bound on Delta alpha below the PDG shortfall "
                         "at every n",
                 "bound_max": L2["bound_max"],
                 "shortfall": L2["pdg_shortfall"]},
        "B9-4": {"ok": bool(L2["bound_falls_fast_with_n"]),
                 "what": "bound falls fast with refinement (grid noise, not a "
                         "residual log: a real log is n-independent)",
                 "ratio_nmax_over_nmin": L2["bound_ratio_max_n_over_min_n"]},
        "B9-5": {"ok": bool(L3["two_loop_beta_exact"]
                            and L3["frac_of_shortfall_closed"] > 0.75
                            and L3["rel_err_with_two_loop"] < 6e-4
                            and L3["rel_err_with_two_loop"]
                            < L3["rel_err_one_loop"]),
                 "what": "F261 b1 = 1 closes >75% of the shortfall; agreement "
                         "improves to <0.06%",
                 "rel_err": L3["rel_err_with_two_loop"],
                 "frac_closed": L3["frac_of_shortfall_closed"]},
        "B9-6": {"ok": bool(abs(L4["with_pdg_alpha"]["resid_vs_PDG_msbar_pct"]
                                - 0.222) < 0.01
                            and L4["residual_ratio_model_over_pdg"] > 1.5),
                 "what": "F138 +0.222% reproduced; leptonic-only alpha degrades "
                         "it by >1.5x",
                 "ratio": L4["residual_ratio_model_over_pdg"]},
    }
    all_pass = all(c["ok"] for c in checks.values())
    # `all_pass` is the harness's recognised verdict key (`runner._overall`) and
    # is therefore this record's FAILURE ROUTE — the driver returns leg verdicts
    # instead of raising, so that a D9/H2 control can be read off WHICH legs went
    # red. `verdict` alone is decorative; `all_pass` is what scores the run.
    return {"all_pass": all_pass,
            "verdict": "PASS" if all_pass else "FAIL",
            "checks": checks,
            "n_pass": sum(1 for c in checks.values() if c["ok"]),
            "n_total": len(checks),
            "L1_refold_independence": L1,
            "L2a_calibration": L2a,
            "L2_lattice_bound": L2,
            "L3_two_loop_LL": L3,
            "L4_ew_leg": L4}


def report() -> dict:
    return check_b9_rederivation()


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path
    out = report()
    p = results_path("F322_b9_running_rederivation.json")
    with open(p, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(json.dumps({"verdict": out["verdict"], "checks": out["checks"]},
                     indent=2, default=str))
    print("wrote", p)
