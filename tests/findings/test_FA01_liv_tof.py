#!/usr/bin/env python3
"""FA01 — Lorentz-violation time-of-flight scale (sharp falsifier).

Symbolic + arithmetic verification of the parameter-free prediction

    E_QG,2 = sqrt(54) * hbar * c / a = 1.360e19 GeV  (subluminal, quadratic n=2)

from the F30 even-law paired-photon dispersion and the F79/F107 canonical cell

    a = sqrt(8*pi) * 3**(1/4) * ell_P = 1.06638e-34 m.

Per CLAUDE.md: NO chiral transforms through numpy/scipy. We use sympy exact
rationals for the dispersion-series algebra and plain Python floats / mpmath
for the SI readout. The BCC bands here are real-valued arccos expressions, so
sympy handles them exactly; nothing complex/chiral is pushed through numpy.

Gate (from tests/falsification/FA01-liv-time-of-flight.md):
  PASS  if E_QG,2 = 1.360e19 GeV to fit floor AND current best bound
        (LHAASO 7e11 GeV) is below it.
  FALSIFIED if a confirmed subluminal n=2 bound exceeds 1.4e19 GeV,
        OR any superluminal n=2 signal, OR a net linear (n=1) ToF effect.
"""

import json
import math
from datetime import date

import sympy as sp


def even_law_k2_coefficient():
    """Symbolically extract the even-law (n=2) dispersion coefficients along (1,1,1).

    BCC bands (F30):  omega^pm(k) = arccos(cx*cy*cz pm sx*sy*sz),
        ci = cos(k_i/sqrt3), si = sin(k_i/sqrt3).
    Composite photon:  Omega^pm(k) = 2 * omega^pm(k/2).
    Even (unpolarised) law: Omega_even = (Omega^+ + Omega^-)/2.

    Returns dict with exact sympy coefficients.
    """
    k = sp.symbols('k', positive=True)
    s3 = sp.sqrt(3)

    # Along the body diagonal (1,1,1): each component argument is (k/sqrt3)
    # evaluated at half-wavenumber for the composite photon -> arg = (k/2)/sqrt3.
    def omega_pm(kk, sign):
        # Body-diagonal (1,1,1): each component k_i = k/sqrt3, and c_i = cos(k_i/sqrt3),
        # so the scalar argument is k/3 (NOT k/sqrt3). This reproduces the exact F30
        # bands: Omega^+ = k/sqrt3 - sqrt3 k^2/54, even group dv/c = -k^2/54.
        arg = kk / 3
        c = sp.cos(arg)
        s = sp.sin(arg)
        return sp.acos(c**3 + sign * s**3)

    # composite photon Omega^pm(k) = 2 * omega^pm(k/2)
    Omega_plus = 2 * omega_pm(k / 2, +1)
    Omega_minus = 2 * omega_pm(k / 2, -1)
    Omega_even = (Omega_plus + Omega_minus) / 2

    # Series expansions
    ser_plus = sp.series(Omega_plus, k, 0, 4).removeO()
    ser_minus = sp.series(Omega_minus, k, 0, 4).removeO()
    ser_even = sp.series(Omega_even, k, 0, 4).removeO()

    clat = sp.Rational(1, 1) / s3  # 1/sqrt3

    # Even-law k^2 coefficient (the n=2 term in Omega)
    a2_even = sp.simplify(ser_even.coeff(k, 2))
    # Single-chirality k^2 coefficient (subluminal branch, +)
    a2_plus = sp.simplify(ser_plus.coeff(k, 2))
    # Linear-in-k birefringent (odd) term: should be the surviving n=1 split
    Omega_odd = sp.simplify((Omega_plus - Omega_minus) / 2)
    ser_odd = sp.series(Omega_odd, k, 0, 4).removeO()
    a2_odd = sp.simplify(ser_odd.coeff(k, 2))   # odd k^2 piece
    a1_even = sp.simplify(ser_even.coeff(k, 1))  # linear coeff of even law (should be c_lat)

    # phase-velocity correction: Omega = c_lat*k + a2*k^2 -> v_phi = Omega/k = c_lat + a2*k
    # delta v_phi / c = (v_phi - c_lat)/c_lat = (a2/c_lat) * k    [first order]
    # Reported as coefficient of k^2 in delta v_phi/c? F30 reports -k^2/162.
    # Careful: F30 even PHASE law is -k^2/162; let's compute it from a2_even.
    # v_phi/c_lat = 1 + (a2_even/c_lat)*k + ...  -> delta v_phi/c = (a2_even/c_lat) k.
    # But F30 states delta v_phi/c = -k^2/162. That implies a k^2 phase correction,
    # i.e. Omega_even has NO k^2 term and the leading correction is k^3.
    # We verify which is true below.

    return {
        'k': k,
        'clat': clat,
        'ser_plus': ser_plus,
        'ser_minus': ser_minus,
        'ser_even': ser_even,
        'ser_odd': ser_odd,
        'a1_even': a1_even,
        'a2_even': a2_even,
        'a2_plus': a2_plus,
        'a2_odd': a2_odd,
    }


def group_velocity_law():
    """Compute the GROUP-velocity dispersion delta v_g/c from the even-law Omega(k).

    Returns the exact coefficient of k^2 in delta v_g/c along (1,1,1).
    """
    k = sp.symbols('k', positive=True)
    s3 = sp.sqrt(3)

    def omega_pm(kk, sign):
        # Body-diagonal argument is k/3 (see note in even_law_k2_coefficient).
        arg = kk / 3
        return sp.acos(sp.cos(arg)**3 + sign * sp.sin(arg)**3)

    Omega_even = (2 * omega_pm(k / 2, +1) + 2 * omega_pm(k / 2, -1)) / 2
    clat = 1 / s3

    # v_g = dOmega/dk ; delta v_g/c = (v_g - clat)/clat
    vg = sp.diff(Omega_even, k)
    dvg = sp.simplify((vg - clat) / clat)
    ser = sp.series(dvg, k, 0, 5).removeO()
    coeff_k2 = sp.simplify(ser.coeff(k, 2))

    # Also the phase law for cross-check
    vph = Omega_even / k
    dvph = sp.simplify((vph - clat) / clat)
    ser_ph = sp.series(dvph, k, 0, 5).removeO()
    coeff_ph_k2 = sp.simplify(ser_ph.coeff(k, 2))

    return coeff_k2, coeff_ph_k2, ser, ser_ph


def main():
    out = {
        'test_id': 'FA01',
        'title': 'Lorentz-violation time-of-flight scale (canonical cell a)',
        'date': '2026-06-10',
    }

    # --- Step 1: symbolic dispersion ---------------------------------------
    sym = even_law_k2_coefficient()
    coeff_vg_k2, coeff_vph_k2, ser_vg, ser_vph = group_velocity_law()

    # Expected: group law delta v_g/c = -k^2/54 ; phase law delta v_phi/c = -k^2/162
    expect_vg = sp.Rational(-1, 54)
    expect_vph = sp.Rational(-1, 162)

    vg_ok = sp.simplify(coeff_vg_k2 - expect_vg) == 0
    vph_ok = sp.simplify(coeff_vph_k2 - expect_vph) == 0

    # Subluminal: coefficient is negative
    subluminal = (coeff_vg_k2 < 0)

    # Even law has NO linear (n=1) net term: coefficient of k^1 in delta v_g/c is 0
    k = sym['k']
    no_linear = sp.simplify(ser_vg.coeff(k, 1)) == 0

    out['symbolic'] = {
        'group_velocity_k2_coeff': str(coeff_vg_k2),
        'group_velocity_k2_coeff_float': float(coeff_vg_k2),
        'expected_group_k2': '-1/54',
        'group_law_matches': bool(vg_ok),
        'phase_velocity_k2_coeff': str(coeff_vph_k2),
        'expected_phase_k2': '-1/162',
        'phase_law_matches': bool(vph_ok),
        'subluminal': bool(subluminal),
        'net_linear_n1_term_present': not bool(no_linear),
        'even_law_linear_coeff_is_clat': bool(sp.simplify(sym['a1_even'] - sym['clat']) == 0),
    }

    # --- Step 2: SI readout E_QG,2 = sqrt(54) * hbar * c / a ----------------
    # CODATA 2018
    hbar = 1.054571817e-34       # J s
    c = 299792458.0              # m/s
    ell_P = 1.616255e-35         # m (Planck length, CODATA 2018)
    eV = 1.602176634e-19         # J
    GeV = 1e9 * eV
    E_P = 1.22089e19             # GeV (Planck energy, for the 1.11 E_P cross-check)

    a = math.sqrt(8 * math.pi) * (3 ** 0.25) * ell_P  # canonical cell (F79/F107)
    E_QG2_J = math.sqrt(54) * hbar * c / a
    E_QG2_GeV = E_QG2_J / GeV

    predicted_GeV = 1.360e19
    rel_err = abs(E_QG2_GeV - predicted_GeV) / predicted_GeV

    out['si_readout'] = {
        'a_m': a,
        'a_over_ellP': a / ell_P,
        'E_QG2_GeV': E_QG2_GeV,
        'E_QG2_over_EP': E_QG2_GeV / E_P,
        'predicted_brief_GeV': predicted_GeV,
        'rel_err_vs_brief': rel_err,
    }

    # --- Step 3: gate against measured bound --------------------------------
    bound_LHAASO_GeV = 7.0e11    # one-sided subluminal n=2 bound, GRB 221009A (F28)
    threshold_falsify_GeV = 1.4e19  # brief criterion 1

    bound_below_prediction = bound_LHAASO_GeV < E_QG2_GeV
    margin_decades = math.log10(E_QG2_GeV / bound_LHAASO_GeV)
    falsified_by_bound = bound_LHAASO_GeV > threshold_falsify_GeV

    out['gate'] = {
        'measured_bound_GeV': bound_LHAASO_GeV,
        'measured_bound_source': 'LHAASO GRB 221009A, n=2 subluminal one-sided (F28)',
        'falsify_threshold_GeV': threshold_falsify_GeV,
        'bound_below_prediction': bound_below_prediction,
        'margin_decades_above_bound': margin_decades,
        'superluminal_n2_detected': False,
        'net_linear_n1_detected': False,
        'falsified_by_bound_above_threshold': falsified_by_bound,
    }

    # --- Verdict ------------------------------------------------------------
    symbolic_pass = (
        out['symbolic']['group_law_matches']
        and out['symbolic']['phase_law_matches']
        and out['symbolic']['subluminal']
        and not out['symbolic']['net_linear_n1_term_present']
    )
    si_pass = rel_err < 5e-3   # fit floor; brief quotes 3 sig figs (1.360)
    gate_pass = bound_below_prediction and not falsified_by_bound

    if symbolic_pass and si_pass and gate_pass:
        verdict = 'PASS'
    else:
        verdict = 'FALSIFIED'

    out['checks'] = {
        'symbolic_pass': symbolic_pass,
        'si_pass': si_pass,
        'gate_pass': gate_pass,
    }
    out['verdict'] = verdict
    out['gate_text'] = ('PASS: E_QG,2 = 1.360e19 GeV to fit floor AND best measured '
                        'bound (7e11 GeV) is below it.')
    out['commands'] = [
        'python3 tests/findings/test_FA01_liv_tof.py',
    ]
    out['timestamp'] = date.today().isoformat() + 'T00:00:00'

    print(json.dumps(out, indent=2))

    import os
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_path = os.path.join(repo, 'test-results', 'FA01_liv_tof.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)

    return out


if __name__ == '__main__':
    r = main()
    print('\nVERDICT:', r['verdict'])
