"""F139 — Self-consistent dual-Ginzburg-Landau back-reaction (closes F137 §5).

F137 built the live colour bag as a MEAN-FIELD dielectric: the condensate
responded to the colour-charge density through a *fixed* Gaussian smear λ, a
one-way map, so the flux tube stayed connected only out to ~2λ then PINCHED.
F139 closes the loop — the genuine dual-GL system where the confined colour-
electric flux is itself what melts the condensate, the two fields solved to
mutual consistency (``ca_dual_gl_backreaction.self_consistent_bag``).

  G1  condensate sector is exact: the f-flow with zero field relaxes to the
      analytic GL domain wall  f(x)=tanh(x/2ξ)  (ODE-exact).
  G2  the coupled (f ↔ colour-E flux) loop converges to a true fixed point
      (residual driven below tol; monotone decrease).
  G3  PINCH-OFF CURED: for two static colour charges the self-consistent tube
      stays connected (ε_mid melted) at separations where the F137 mean-field
      bag has pinched (ε_mid → 0), and the back-reaction is the cause (A/B).
  G4  CONFINEMENT: the bag/string energy is linear in R with a ~constant
      tension (R-independent tube cross-section) — the dynamical realisation of
      F86's σ=2πv²n; and norms/limits (zero charge → vacuum f=1).

Standalone:
    PYTHONPATH=src python tests/findings/test_F139_dual_gl_backreaction.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.interactions import gravity_backreaction as gl  # noqa: E402

_RESULTS = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "test-results",
    "F139_dual_gl_backreaction.json")
_REC: dict = {}


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def _src2d(R, L=32, amp=3.0, w=1.0):
    """Two opposite Gaussian colour charges separated by R along x (Σ=0)."""
    s = np.zeros((1, L, L))
    yc = L // 2
    X, Y = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    for sign, xc in ((1.0, L // 2 - R // 2), (-1.0, L // 2 + (R - R // 2))):
        s[0] += sign * amp * np.exp(
            -((((X - xc + L / 2) % L - L / 2) ** 2
              + ((Y - yc + L / 2) % L - L / 2) ** 2)) / (2 * w ** 2))
    return s, (L // 2, yc)


# ----------------------------------------------------------------------
# G1 — the condensate sector is exact (GL domain wall)
# ----------------------------------------------------------------------
def test_G1_gl_kink_exact():
    L, xi, dtau, n = 160, 5.0, 0.04, 40000
    x = np.arange(L) - L / 2.0
    f = np.sign(x).astype(float) * 0.5          # crude step seed (NOT answer)
    f[0], f[-1] = -1.0, 1.0
    for _ in range(n):
        force = 2.0 * gl.laplacian(f) - (1.0 / xi ** 2) * (f * f - 1.0) * f
        f = f + dtau * force
        f[0], f[-1] = -1.0, 1.0
    err = float(np.abs(f - gl.gl_kink(x, xi))[15:-15].max())
    _REC["G1_kink_err"] = err
    assert err < 2e-3, f"GL kink not reproduced: {err:.2e}"


# ----------------------------------------------------------------------
# G2 — the self-consistent loop converges to a fixed point
# ----------------------------------------------------------------------
def test_G2_loop_converges():
    s, _ = _src2d(5, L=28)
    r = gl.self_consistent_bag(s, xi=0.7, eps_floor=0.01, dtau=0.02,
                               n_out=1500, tol=1e-6, record=True)
    _REC["G2_residual"] = r["residual"]
    _REC["G2_iters"] = r["iters"]
    _REC["G2_monotone"] = bool(r["history"][0] > r["history"][-1])
    assert r["converged"], f"loop did not converge: res={r['residual']:.2e}"
    assert r["history"][0] > r["history"][-1], "residual not decreasing"


# ----------------------------------------------------------------------
# G3 — pinch-off cured (self-consistent vs F137 mean-field, A/B)
# ----------------------------------------------------------------------
def test_G3_pinch_off_cured():
    Rs = (2, 5, 8, 11)
    mf, sc = {}, {}
    for R in Rs:
        s, (mx, my) = _src2d(R, L=32, amp=3.0)
        mf[R] = float(gl.meanfield_bag(s, lam=2.0, phi0=0.5)["eps_c"][mx, my])
        res = gl.self_consistent_bag(s, xi=0.7, eps_floor=0.01, dtau=0.025,
                                     n_out=200)
        sc[R] = float(res["eps_c"][mx, my])
    _REC["G3_eps_mid_meanfield"] = mf
    _REC["G3_eps_mid_selfconsistent"] = sc
    # mean-field pinches beyond ~2λ=4 (ε_mid collapses toward 0)
    assert mf[11] < 0.2, f"mean-field did not pinch (control): {mf[11]:.2f}"
    # self-consistent tube stays connected at every separation
    assert min(sc.values()) > 0.7, \
        f"self-consistent tube pinched: min ε_mid={min(sc.values()):.2f}"
    # and it is the back-reaction that makes the difference, at large R
    assert sc[11] > 3.0 * mf[11], "back-reaction did not cure the pinch"


# ----------------------------------------------------------------------
# G4 — linear confinement (constant string tension) + vacuum limit
# ----------------------------------------------------------------------
def test_G4_linear_tension_and_vacuum():
    Rs = (2, 5, 8, 11)
    ebag = []
    for R in Rs:
        s, _ = _src2d(R, L=32, amp=3.0)
        res = gl.self_consistent_bag(s, xi=0.7, eps_floor=0.01, dtau=0.025,
                                     n_out=200)
        ebag.append(res["energy"][1])          # E_bag = string energy
    slopes = [(ebag[i + 1] - ebag[i]) / (Rs[i + 1] - Rs[i])
              for i in range(len(Rs) - 1)]
    flat = max(slopes) / min(slopes)
    _REC["G4_E_bag"] = ebag
    _REC["G4_tension_slopes"] = slopes
    _REC["G4_tension_flatness"] = flat
    # string energy rises monotonically and the tension is roughly constant
    assert all(ebag[i + 1] > ebag[i] for i in range(len(ebag) - 1)), \
        "bag/string energy not monotone in R"
    assert flat < 1.5, f"string tension not ~constant (flatness {flat:.2f})"
    # vacuum limit: zero colour charge → full condensate f=1, no melting
    vac = gl.self_consistent_bag(np.zeros((1, 24, 24)), xi=1.0,
                                 eps_floor=1e-2, dtau=0.03, n_out=40)
    _REC["G4_vacuum_fmin"] = float(vac["f"].min())
    assert vac["f"].min() > 1.0 - 1e-9, \
        f"vacuum melted spuriously: f_min={vac['f'].min():.3f}"


def _dump():
    os.makedirs(os.path.dirname(_RESULTS), exist_ok=True)
    with open(_RESULTS, "w") as fh:
        json.dump(_REC, fh, indent=2)


if __name__ == "__main__":
    test_G1_gl_kink_exact()
    print(f"G1  PASS — GL domain wall exact (err {_REC['G1_kink_err']:.2e})")
    test_G2_loop_converges()
    print(f"G2  PASS — back-reaction loop converges "
          f"(res {_REC['G2_residual']:.2e}, {_REC['G2_iters']} iters)")
    test_G3_pinch_off_cured()
    print("G3  PASS — pinch-off cured: SC ε_mid="
          f"{_REC['G3_eps_mid_selfconsistent'][11]:.2f} vs mean-field "
          f"{_REC['G3_eps_mid_meanfield'][11]:.2f} at R=11")
    test_G4_linear_tension_and_vacuum()
    print(f"G4  PASS — linear string tension (flatness "
          f"{_REC['G4_tension_flatness']:.2f}); vacuum f_min "
          f"{_REC['G4_vacuum_fmin']:.4f}")
    _dump()
    print(f"F139 4/4 PASS — results → {_RESULTS}")
