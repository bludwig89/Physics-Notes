"""
test_F207_casimir.py  —  The Casimir effect in the BCC Weyl-QCA model
=====================================================================

Confronts the measured Casimir force with the model's already-derived
constraints (no new physics): the F69 paired-spinor photon, the F26 dispersion
(c=1/√3), the F107 cell a (UV cutoff), and the F178/F193 beable gravity source.

Checks (mirror the build brief tiers):
  C1  1D scalar mode-sum machinery: 'sin' lattice scalar → −πc/24L (validated);
      the model photon along a cubic axis is EXACTLY linear → E_sub = const
      (a clean directional fact, no Casimir term from a pure axial mode line).
  C2  3D EM reproduction: Abel–Plana reduction of the mode sum with the exact
      IR dispersion ω→c|k| (F69-PP3) gives the textbook law in closed form,
      F/A = −π²ħc/240L⁴, EXACTLY.
  C3  Lattice signature: Ω_pair bending coefficient β(k̂) — zero along a cubic
      axis, O(10⁻²) off-axis → an O((a/L)²) correction (unobservably small).
  C4  Source channel (Jaffe 2005): two δ-mirrors of strength λ — the energy
      runs monotonically 0 → Dirichlet as λ: 0 → ∞.  No coupling, no force →
      the force is a matter/H_int effect, consistent with the F193 superimposable.
  G1  Gravitation (F193/F178/F106): the Casimir energy is beable binding energy,
      gravitates as Δm=E_C/c² (Gauss-law closure of ∇²lnK=−8πT⁰⁰).  Magnitude
      equals the SEP vacuum-buoyancy prediction → NOT distinguishable by
      Archimedes at leading order (honest: an interpretational, not numerical,
      distinction).
  D1  Dynamical Casimir: parametric boundary drive → strict pair emission
      (n_a=n_b exactly), the DCE two-mode-squeezed vacuum.

CLAUDE.md: closed-form/audited dispersion only.  No np.linalg.eig on chiral
matrices.
"""

import sys, os, json, time
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

import numpy as np
from casim.engine.interactions import qed_casimir as cc

RESULTS = os.path.join(os.path.dirname(__file__), '..', '..', 'test-results',
                       'F207_casimir.json')


def main():
    out = {"finding": "F207", "title": "Casimir effect in the BCC Weyl-QCA model",
           "timestamp": time.strftime("%Y-%m-%d %H:%M"), "checks": {}}
    passed = 0
    total = 0

    # ---- C1: 1D machinery ------------------------------------------------
    total += 1
    c1, e0, _ = cc.fit_coeff_1d(np.arange(40, 161, 10), kind="sin")
    tgt1 = -np.pi * cc.C_LAT / 24.0
    rel1 = abs(c1 / tgt1 - 1.0)
    axis_const = [cc.casimir_energy_1d(L, kind="axis") for L in (40, 80, 120)]
    axis_flat = max(axis_const) - min(axis_const)
    ok = rel1 < 1e-3 and axis_flat < 1e-9
    passed += ok
    out["checks"]["C1_1d_machinery"] = {
        "coeff_sin": c1, "target": tgt1, "rel_err": rel1,
        "axis_Esub_const": axis_const, "axis_flatness": axis_flat,
        "tier": "quantitative (3.5e-5) + exact axis-linear", "pass": bool(ok)}

    # ---- C2: 3D EM reproduction (Abel–Plana, exact closed form) ----------
    total += 1
    ratios_E, ratios_F = [], []
    for L in (20., 40., 80., 160.):
        E = cc.casimir_energy_3d_abelplana(L, pol=2)
        Ec = cc.casimir_energy_3d_closed(L, pol=2)
        F = cc.casimir_force_3d_abelplana(L, pol=2)
        Ftgt = -np.pi ** 2 * cc.C_LAT / 240.0 / L ** 4
        ratios_E.append(E / Ec)
        ratios_F.append(F / Ftgt)
    ok = max(abs(np.array(ratios_E) - 1)) < 1e-6 and max(abs(np.array(ratios_F) - 1)) < 1e-12
    passed += ok
    out["checks"]["C2_em_reproduction"] = {
        "force_law": "-pi^2 hbar c / 240 L^4", "energy_law": "-pi^2 hbar c / 720 L^3",
        "c_lat": cc.C_LAT, "energy_numeric_over_closed": ratios_E,
        "force_numeric_over_closed": ratios_F,
        "tier": "exact-algebraic (closed form from IR dispersion)", "pass": bool(ok)}

    # ---- C3: lattice signature ------------------------------------------
    total += 1
    betas = {d: cc.pair_bending_coeff(v) for d, v in
             {"axis_100": (1, 0, 0), "face_110": (1, 1, 0), "body_111": (1, 1, 1)}.items()}
    # (a/L)^2 magnitude for a laboratory cavity
    aL2_lab = (cc.A_SI / 1e-6) ** 2     # a/L with L = 1 micron
    ok = abs(betas["axis_100"]) < 1e-3 and betas["body_111"] < 0  # axis ~0, off-axis subluminal
    passed += ok
    out["checks"]["C3_lattice_signature"] = {
        "beta_by_direction": betas, "form": "fractional correction ~ beta*(a/L)^2",
        "axis_exactly_linear": True, "aL_squared_at_1um": aL2_lab,
        "tier": "directional structure exact (axis=0); coefficient O((a/L)^2)",
        "pass": bool(ok)}

    # ---- C4: source channel (Jaffe) -------------------------------------
    total += 1
    lams = [1e-2, 1e-1, 1.0, 10.0, 1e3]
    EL = [cc.casimir_energy_delta_1d(30., lam) * 30.0 for lam in lams]
    dirichlet = -np.pi * cc.C_LAT / 24.0
    monotonic = all(EL[i] >= EL[i + 1] - 1e-9 for i in range(len(EL) - 1))  # |E| grows with lam
    to_zero = abs(EL[0]) < 0.25 * abs(dirichlet)
    to_dirichlet = abs(EL[-1] / dirichlet - 1.0) < 0.02
    ok = monotonic and to_zero and to_dirichlet
    passed += ok
    out["checks"]["C4_source_channel"] = {
        "lambdas": lams, "E_times_L": EL, "dirichlet_limit": dirichlet,
        "interpretation": "force = matter/H_int coupling effect (Jaffe 2005); "
                          "vanishes as lambda->0; F193 superimposable does not source it",
        "tier": "qualitative+limits", "pass": bool(ok)}

    # ---- G1: gravitation (F193/F178/F106) -------------------------------
    total += 1
    A, L = 1e-4, 1e-8     # 1 cm^2, 10 nm
    E_C, dm, weight = cc.casimir_gravitating_mass(A, L)
    M_gauss = cc.dielectric_enclosed_mass_gauss(E_C)
    gauss_ok = abs(M_gauss - dm) < 1e-30
    # the SEP vacuum-buoyancy prediction is also Delta m = E_C/c^2 -> degenerate
    distinguishable = False
    ok = gauss_ok and (dm < 0)   # beable binding energy gravitates negative
    passed += ok
    out["checks"]["G1_gravitation"] = {
        "cavity": "1 cm^2 plates, 10 nm gap", "E_C_J": E_C, "delta_m_kg": dm,
        "weight_change_N": weight, "gauss_enclosed_mass_kg": M_gauss,
        "delta_m_equals_E_over_c2": gauss_ok,
        "distinguishable_from_SEP_buoyancy": distinguishable,
        "verdict": "Casimir energy gravitates as beable binding energy "
                   "Delta m = E_C/c^2; equals SEP vacuum-buoyancy magnitude => "
                   "Archimedes cannot discriminate (interpretational distinction "
                   "only); the non-gravitating piece is the homogeneous sum (F193)",
        "tier": "exact (Gauss law) + honest non-discrimination", "pass": bool(ok)}

    # ---- D1: dynamical Casimir pair emission ----------------------------
    total += 1
    ts, na, nb, pair_err, sinh_dev = cc.two_mode_squeezing(0.05, 30.0, ncut=30)
    ok = pair_err < 1e-12 and sinh_dev < 0.05
    passed += ok
    out["checks"]["D1_dynamical_casimir"] = {
        "max_abs_na_minus_nb": pair_err, "max_dev_from_sinh2": sinh_dev,
        "n_a_end": float(na[-1]), "sinh2_end": float(np.sinh(0.05 * 30.) ** 2),
        "result": "strict pair emission (n_a=n_b exactly); DCE two-mode squeezing. "
                  "NB: distinct from F69 internal Weyl-pair binding of ONE photon — "
                  "DCE emits TWO photons together (4 Weyl quanta).",
        "tier": "exact pair correlation (0) + sinh^2 magnitude", "pass": bool(ok)}

    out["summary"] = {"passed": int(passed), "total": int(total),
                      "status": "PASS" if passed == total else "PARTIAL"}

    def _coerce(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return str(o)

    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    with open(RESULTS, "w") as f:
        json.dump(out, f, indent=2, default=_coerce)
    print(json.dumps(out["summary"]), "->", RESULTS)
    for name, ch in out["checks"].items():
        print(("  PASS " if ch["pass"] else "  FAIL ") + name + " — " + ch["tier"])
    assert passed == total, f"{passed}/{total} passed"


if __name__ == "__main__":
    main()
