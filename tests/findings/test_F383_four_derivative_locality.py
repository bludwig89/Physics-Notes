"""
test_F383_four_derivative_locality.py — locality generates, not forbids,
the four-derivative curvature term
=====================================================================
Tests `casim.engine.interactions.gravity_four_derivative_locality`, which
extends F57's own Brillouin-zone matter-density polarization Pi(q) — the
mechanism that induces the model's two-derivative (Einstein-Hilbert)
coefficient Pi2 — one order further, to the q^4 coefficient Pi4. Pi4 is the
scalar/rest-leg-channel analogue of a four-derivative curvature-squared
Wilson coefficient.

Target: rubric row E1 / ledger E1g, the "at-most-second-order" sub-item
F345 L7 left open inside the model's one surviving field-equation posit.

M1  Regression.  Extending the fit to include a q^4 term does not disturb
    F57's own reviewed Pi2 result (sign, order of magnitude).
M2  Pi4 robustly nonzero (SIGN).  Same sign and within a 5x band across four
    independent perturbations (grid, q-window, direction), at a quartic
    (order=4) fit — the leg this finding turns on for sign.
M2b Sign survives a q^6 fit.  The adversarial-review perturbation, kept as
    a permanent check: rerunning M2's own four variants with a q^6 term
    added shifts each |Pi4| by ~2.6-3x (a real, disclosed fit-order
    sensitivity — only sign and order of magnitude are supportable here,
    not the specific M2 figures) but never flips the sign.
M3  Grid convergence.  Pi4 converges under grid refinement — a genuine
    finite BZ integral, not a quadrature artifact.
M4  Cutoff scaling.  Pi4 stays finite across a swept spherical-proxy
    cutoff (descriptive; a numerical anomaly at the largest cutoff tested
    is flagged in the leg's own "caveat" field, not smoothed over).
M5  Direction spread.  Pi4 measured along three non-equivalent BCC
    directions; same sign, isotropic to ~2% in the sample tested.
L   Conclusion.  Given M2, at-most-second-order is NOT forced by lattice
    locality — the identical finite BZ mechanism that induces the accepted
    two-derivative term induces a nonzero four-derivative one too, and no
    symmetry protects it in this channel (F345 L3's d=4 Gauss-Bonnet
    cancellation is a property of the full nonlinear curvature-squared
    invariant, not of this scalar polarization).

Writes test-results/F383_four_derivative_locality.json.

Run:
    python tests/findings/test_F383_four_derivative_locality.py
    pytest tests/findings/test_F383_four_derivative_locality.py
"""

from __future__ import annotations

import json
import os
import sys

_THIS = os.path.dirname(__file__)
_SRC = os.path.abspath(os.path.join(_THIS, "..", "..", "src"))
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from casim.engine.interactions import gravity_four_derivative_locality as f383  # noqa: E402


def test_M1_pi2_regression():
    leg = f383.leg_M1_pi2_regression()
    assert leg["pass"], leg


def test_M2_pi4_robust_nonzero():
    leg = f383.leg_M2_pi4_robust_nonzero()
    assert leg["pass"], leg
    assert leg["same_sign"], "Pi4 changed sign across independent perturbations"


def test_M2b_pi4_sign_survives_q6():
    leg = f383.leg_M2b_pi4_sign_survives_q6()
    assert leg["pass"], leg
    assert leg["sign_matches_order4"], "adding a q^6 term flipped Pi4's sign"


def test_M3_pi4_grid_convergence():
    leg = f383.leg_M3_pi4_grid_convergence()
    assert leg["pass"], leg


def test_M4_pi4_cutoff_scaling():
    leg = f383.leg_M4_pi4_cutoff_scaling()
    assert leg["pass"], leg


def test_M5_pi4_direction_spread():
    leg = f383.leg_M5_pi4_direction_spread()
    assert leg["pass"], leg


def test_L_conclusion():
    m2 = f383.leg_M2_pi4_robust_nonzero()
    leg = f383.leg_L_conclusion(m2)
    assert leg["pass"], leg


def main():
    out = f383.run_all()
    out_dir = os.path.abspath(os.path.join(_THIS, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "F383_four_derivative_locality.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)

    print("=" * 72)
    print("F383 — locality generates, not forbids, the four-derivative curvature term")
    print("=" * 72)
    for leg in out["legs"]:
        print(f"  [{'PASS' if leg['pass'] else 'FAIL':>5}]  {leg['leg']}: {leg['claim']}")
    print("-" * 72)
    print(f"  OVERALL: {'PASS' if out['all_pass'] else 'FAIL'} ({out['n_pass']}/{out['n_legs']})")
    print(f"  wrote {path}")
    return out


if __name__ == "__main__":
    main()
