#!/usr/bin/env python3
"""
test_F262_positronium_hyperfine.py — F262: bound-state QED (two-body + hyperfine).

Completes the bound-state side of the QED sector on top of the F125 one-body
Dirac-Coulomb solver and the F252/F257 radiative Lamb shift:

  * POSITRONIUM (ca_positronium): reduced-mass spectrum (1/2 hydrogen, structural),
    the 7/12 alpha^4 ortho-para hyperfine splitting (spin-spin 1/3 + virtual
    annihilation 1/4, the annihilation piece tied to the F260 e+e- vertex), and
    the para->2gamma / ortho->3gamma decay rates.
  * HYDROGEN 21 cm + LAMB COMPLETENESS (ca_hyperfine): Fermi-contact hyperfine
    -> 1420.4 MHz; recoil + finite-nuclear-size corrections on the Lamb shift.

Gates (exactness ladder):
  G1  reduced-mass: E_n(Ps)/E_n(H_inf) = 1/2 exactly; ground state -6.80 eV   structural
  G2  hyperfine coefficients 1/3 + 1/4 = 7/12                                  exact (sympy)
  G3  spin-spin -> 1/3, annihilation -> 1/4 (from |psi(0)|^2 + g=2 + vertex)   machine
  G4  annihilation coupling: threshold sigma*v -> pi alpha^2/m^2 (F260)        quantitative
  G5  Ps hyperfine 7/12 alpha^4 m_e c^2 toward 203 389 MHz (LO ~0.5%)          quantitative
  G6  para->2gamma: Gamma = (1/2) alpha^5 m_e c^2 (from F260); tau=0.125 ns     machine+quant
  G7  Ore-Powell 3gamma integral -> pi^2-9; ortho tau ~139 ns toward 142       quantitative
  G8  hydrogen 21 cm -> 1420.4 MHz (g_p input + a_e from F252)                  quantitative
  G9  finite-size 2s ~0.14 MHz, ∝ r_p^2 (proton-radius lever)                  quantitative
  G10 Lamb + recoil + finite size: shifted value; residual = higher-order QED  quantitative

Run:  python3 tests/findings/test_F262_positronium_hyperfine.py --json out.json
Test: pytest -q tests/findings/test_F262_positronium_hyperfine.py
"""
from __future__ import annotations
import os, sys, json, argparse, math

_HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.particles import positronium as ps   # noqa: E402
from casim.engine.particles import hyperfine as hf      # noqa: E402


# --------------------------------------------------------------------------- G1
def test_reduced_mass_half_hydrogen():
    s = ps.positronium_spectrum()
    assert s["worst_ratio_dev_from_half"] < 1e-9         # exact 1/2, grid-independent
    assert abs(s["ground_state_closed_eV"] - (-6.8028)) < 1e-3
    assert abs(s["ground_state_eV"] - (-6.80)) < 0.02    # numeric solve


# --------------------------------------------------------------------------- G2
def test_hyperfine_coefficients_exact():
    c = ps.hyperfine_coefficients_symbolic()
    assert c["sum_is_7_12"] is True


# --------------------------------------------------------------------------- G3
def test_spin_spin_and_annihilation_coeffs():
    ss = ps.spin_spin_contact_coeff()
    ann = ps.annihilation_contact_coeff()
    assert ss["rel_err"] < 1e-12                          # -> 1/3
    assert ann["rel_err"] < 1e-12                         # -> 1/4


# --------------------------------------------------------------------------- G4
def test_annihilation_coupling_from_model():
    a = ps.annihilation_coupling_from_model()
    assert abs(a["extrapolated_ratio"] - 1.0) < 1e-3      # sigma*v -> pi alpha^2/m^2
    if a.get("model_amplitude_available"):
        assert abs(a["model_M2_over_e4_threshold"] - 4.0) < 1e-3


# --------------------------------------------------------------------------- G5
def test_positronium_hyperfine_value():
    h = ps.positronium_hyperfine()
    assert abs(h["coeff_total"] - 7.0 / 12.0) < 1e-10
    assert h["rel_err_LO"] < 0.01                         # LO within ~0.5% of 203 389


# --------------------------------------------------------------------------- G6
def test_para_2gamma_rate():
    p = ps.para_2gamma_rate()
    assert p["coeff_check_rel_err"] < 1e-12               # Gamma = (1/2) alpha^5 m
    assert abs(p["tau_ns"] - 0.1245) < 5e-3               # 0.125 ns


# --------------------------------------------------------------------------- G7
def test_ore_powell_and_ortho_rate():
    op = ps.ore_powell_factor(n=100000)
    assert op["rel_err"] < 5e-4                            # integral -> pi^2-9
    o = ps.ortho_3gamma_rate()
    assert abs(o["factor"] - 2 * (math.pi**2 - 9) / (9 * math.pi)) < 1e-12
    assert 135.0 < o["tau_ns"] < 145.0                    # LO 138.6 toward 142


# --------------------------------------------------------------------------- G8
def test_hydrogen_21cm():
    a = hf.hydrogen_21cm()
    assert a["rel_err_final"] < 1e-3                       # -> 1420.4 MHz
    assert abs(a["wavelength_cm"] - 21.1) < 0.2            # 21 cm line


# --------------------------------------------------------------------------- G9
def test_finite_size_lever():
    fs = hf.finite_size_shift_2s()
    assert 0.10 < fs["delta_E_fs_2s_MHz"] < 0.18          # ~0.14 MHz
    fs_big = hf.finite_size_shift_2s(0.9 * 2)             # double-ish radius
    # ∝ r_p^2 scaling
    ratio = fs_big["delta_E_fs_2s_MHz"] / fs["delta_E_fs_2s_MHz"]
    assert abs(ratio - (1.8 / hf.R_PROTON_FM) ** 2) < 1e-6


# --------------------------------------------------------------------------- G10
def test_lamb_complete():
    L = hf.lamb_complete()
    assert 1045.0 < L["shifted_total_MHz"] < 1055.0        # baseline + small corrections
    assert L["finite_size_MHz"] > 0.0
    assert L["proton_radius_lever"] > 0.0                  # r_p sensitivity present


# --------------------------------------------------------------------------- JSON
def _build_report() -> dict:
    return {
        "finding": "F262",
        "title": "Bound-state QED: positronium (reduced-mass + hyperfine + decays), "
                 "hydrogen 21 cm, Lamb recoil + finite size",
        "positronium": ps.report(),
        "hyperfine_and_lamb": hf.report(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    rep = _build_report()
    if args.json:
        with open(args.json, "w") as f:
            json.dump(rep, f, indent=2, default=float)
        print(f"wrote {args.json}")
    # quick human summary
    h = rep["positronium"]["hyperfine"]
    d = rep["positronium"]["para_2gamma"]
    o = rep["positronium"]["ortho_3gamma"]
    a = rep["hyperfine_and_lamb"]["hydrogen_21cm"]
    L = rep["hyperfine_and_lamb"]["lamb_complete"]
    print(f"Ps HFS   : {h['delta_E_MHz']:.1f} MHz (meas 203389, LO)")
    print(f"para 2g  : tau {d['tau_ns']:.4f} ns (meas 0.1245)")
    print(f"ortho 3g : tau {o['tau_ns']:.2f} ns (meas 142, LO)")
    print(f"H 21 cm  : {a['E_F_with_a_e_MHz']:.3f} MHz (meas 1420.406)")
    print(f"Lamb     : {L['shifted_total_MHz']:.2f} MHz shifted "
          f"(base {L['baseline_radiative_MHz']:.2f}, meas 1057.845)")


if __name__ == "__main__":
    main()
