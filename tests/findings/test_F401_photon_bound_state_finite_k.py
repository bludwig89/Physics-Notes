"""F401 — repairing the finite-k grid-threshold artifact in
`photon_bound_state.critical_coupling`/`threshold_wavefunction`.

Attacks `docs/theory/notebook-followup-2026-09-22.md` Part VI.3 and F169's
own "C2/C4-note": the finite-k grid threshold T=E.min() is a non-monotonic
artifact, documented but not repaired there. This finding adds
`threshold="closed"` to `critical_coupling`/`threshold_wavefunction`
(default stays "grid", so F169's own artifact-diagnostic test is untouched)
and characterizes what the fix reveals.

Five checks. The axis identity (A1) is re-derived here independently of the
module -- re-typed from `dimensionality.bloch_vector`, not imported from
`photon_bound_state_finite_k`.

  A1 (exact)        omega+(q,0,0) = omega-(q,0,0) = |q|/sqrt(3): the chiral
      branches collapse onto the SAME isotropic cone along a coordinate
      axis, re-derived symbolically here, independently of the module.
  A2 (quantitative)  A genuine 2-D coordinate-plane point (both other
      components nonzero) has a real, nonzero Omega_even - T offset -- the
      exact vanishing of A1 is special to a pure axis, not the whole plane.
  B1 (quantitative)  Along (111), at the SAME L values F169's own docstring
      quotes for the grid artifact, threshold="closed" converges
      monotonically while threshold="grid" does not.
  B2 (quantitative)  NARROWED ON REVIEW (attack 4, 2026-09-23): a denser
      L-scan at the SAME (111), |k|=0.2 point shows threshold="closed" is
      NOT monotonic at every L either -- occasional grid-commensurability
      dips persist. What survives, quantified: the closed form's worst-case
      single-step backslide is far smaller than the grid form's over the
      same dense scan, and B1's 7-point monotonicity is a real (if narrow)
      fact, not cherry-picked (the 7 L values are F169's own, not chosen for
      this finding).
  B3 (quantitative)  g_c(k), using threshold="closed" at L=192, decreases
      monotonically with |k| from the F169 k=0 value (2.2596) along (111)
      (checked to |k|=1.0, well past the originally-checked 0.4) and along
      (3,1,1) -- but NOT along (2,1,0) (found on review, attack 12): the
      decreasing trend is a real (111)/(311)-class result, not universal.
      DECLARED CONTROL: at k=0, grid and closed thresholds must agree
      exactly (T=0 either way) -- if they did not, the fix would have
      silently changed a value F169 already certified.
"""
from __future__ import annotations

import numpy as np
import sympy as sp

from casim.engine.gauge import photon_bound_state as pbs
from casim.engine.gauge import photon_bound_state_finite_k as fk
from casim.engine.lattice import dimensionality as dim

L_VALUES = [12, 24, 32, 48, 96, 144, 192]


# ── independently re-typed axis identity (NOT imported from the module) ────

def _axis_identity_indep():
    n_plus, ks_plus = dim.bloch_vector(3, sign="+")
    n_minus, ks_minus = dim.bloch_vector(3, sign="-")
    q = sp.Symbol("q", real=True)
    np_axis = sp.simplify(n_plus.subs({ks_plus[0]: q, ks_plus[1]: 0,
                                        ks_plus[2]: 0}))
    nm_axis = sp.simplify(n_minus.subs({ks_minus[0]: q, ks_minus[1]: 0,
                                         ks_minus[2]: 0}))
    return np_axis, nm_axis, q


# ── checks ────────────────────────────────────────────────────────────────

def check_A1_axis_identity_exact():
    np_axis, nm_axis, q = _axis_identity_indep()
    assert sp.simplify(np_axis - nm_axis) == sp.zeros(3, 1)
    # both branches' Bloch vector along the axis is (sin(q/sqrt3), 0, 0)
    expected = sp.Matrix([sp.sin(q / sp.sqrt(3)), 0, 0])
    assert sp.simplify(np_axis - expected) == sp.zeros(3, 1)
    # so omega+ = omega- = acos(cos(q/sqrt3)) = |q|/sqrt(3) identically
    out = fk.axis_dispersion_isotropic_cone_exact()
    assert out["identity_exact"] is True
    # cross-check numerically against the ENGINE's own dispersion (bcc.py),
    # not just the re-typed symbolic Bloch vector, at several q
    for qval in (0.1, 0.37, 1.0, 2.5):
        wp = float(pbs._w(qval, 0.0, 0.0, sign="+"))
        wm = float(pbs._w(qval, 0.0, 0.0, sign="-"))
        assert abs(wp - wm) < 1e-13
        assert abs(wp - qval / np.sqrt(3.0)) < 1e-13
    return {"identity_exact": True, "checked_q": [0.1, 0.37, 1.0, 2.5]}


def check_A2_in_plane_offset_nonzero():
    out = fk.in_plane_offset_is_not_exactly_zero()
    assert out["all_offsets_genuinely_nonzero"] is True
    for row in out["rows"]:
        assert abs(row["offset"]) > 1e-8
    return {"n_rows": len(out["rows"]), "min_offset": min(
        abs(r["offset"]) for r in out["rows"])}


def check_B1_closed_form_converges_monotonically():
    k = 0.2 / np.sqrt(3) * np.array([1.0, 1.0, 1.0])
    grid_seq = fk.l_convergence(k, L_VALUES, "grid")
    closed_seq = fk.l_convergence(k, L_VALUES, "closed")
    assert fk.is_monotonic(closed_seq), closed_seq
    assert not fk.is_monotonic(grid_seq), (
        "expected the grid sequence to remain non-monotonic (the documented "
        "F169 artifact) -- if it is now monotonic, the artifact this "
        "finding characterizes may no longer reproduce, and the L values "
        "or k used here should be re-checked against F169's own numbers")
    return {"grid_sequence": grid_seq, "closed_sequence": closed_seq,
            "grid_monotonic": False, "closed_monotonic": True}


def check_B2_dense_scan_quantified_improvement():
    """NARROWED ON REVIEW (attack 4, 2026-09-23): B1's 7-point monotonicity
    does not generalize to every L. A denser scan at the same (111), |k|=0.2
    point shows threshold="closed" still has occasional commensurability
    dips -- what survives is a QUANTIFIED reduction in worst-case severity,
    not elimination."""
    k = 0.2 / np.sqrt(3) * np.array([1.0, 1.0, 1.0])
    dense_Ls = list(range(12, 201, 4))
    out = fk.dense_l_scan_comparison(k, dense_Ls)
    assert out["closed_max_backslide"] < out["grid_max_backslide"] / 2.0, (
        "expected the closed form's worst-case backslide to be markedly "
        "smaller than the grid form's over a dense L-scan", out)
    # honesty check: the dense scan must ACTUALLY find at least one
    # violation for the closed form too, or B1's 7-point result would be
    # accidentally representative rather than a narrow special case
    assert out["closed_n_violations"] > 0, (
        "expected the denser scan to reveal at least one closed-form "
        "violation -- if none is found, B1's monotonicity may be a general "
        "fact after all and this check's own premise should be revisited")
    return {"grid_max_backslide": out["grid_max_backslide"],
            "closed_max_backslide": out["closed_max_backslide"],
            "grid_n_violations": out["grid_n_violations"],
            "closed_n_violations": out["closed_n_violations"],
            "n_steps": out["n_steps"]}


def check_B3_gc_k_sweep_decreasing(perturb_k0_threshold=None):
    # DECLARED CONTROL (D9/H2): at k=0, grid and closed T must agree exactly.
    gc0_grid, T0_grid = pbs.critical_coupling([0.0, 0.0, 0.0], 12,
                                               threshold="grid")
    gc0_closed, T0_closed = pbs.critical_coupling([0.0, 0.0, 0.0], 12,
                                                   threshold="closed")
    if perturb_k0_threshold == "break":
        # simulate what would happen if the closed-form T at k=0 were wrong
        # (e.g. a sign or scale bug): compare against a deliberately wrong
        # reference value instead of the true gc0_grid.
        assert abs(gc0_closed - (gc0_grid + 0.5)) < 1e-9, (
            "control: comparing against a deliberately wrong reference "
            "must fail -- if this assertion passes, the test cannot tell "
            "a correct k=0 agreement from an incorrect one")
    else:
        assert gc0_grid == gc0_closed, (gc0_grid, gc0_closed)
        assert T0_grid == 0.0 and T0_closed == 0.0

    sweep_111 = fk.gc_k_sweep_111([0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0], L=192)
    gc_111 = [r["g_c"] for r in sweep_111]
    assert all(gc_111[i + 1] <= gc_111[i] for i in range(len(gc_111) - 1)), \
        gc_111
    assert gc_111[0] < gc0_grid, (
        "expect g_c to have already dropped below the k=0 value by |k|=0.05")

    # confirmed also along (3,1,1) -- a second generic direction
    sweep_311 = fk.gc_k_sweep_direction((3.0, 1.0, 1.0),
                                         [0.05, 0.1, 0.2, 0.4, 0.6, 0.8],
                                         L=192)
    gc_311 = [r["g_c"] for r in sweep_311]
    assert all(gc_311[i + 1] <= gc_311[i] for i in range(len(gc_311) - 1)), \
        gc_311

    # NARROWED ON REVIEW (attack 12): does NOT generalize to (2,1,0) -- the
    # decreasing trend is a real (111)/(311)-class result, not universal.
    sweep_210 = fk.gc_k_sweep_direction((2.0, 1.0, 0.0),
                                         [0.05, 0.1, 0.2, 0.4, 0.6, 0.8],
                                         L=192)
    gc_210 = [r["g_c"] for r in sweep_210]
    assert not all(gc_210[i + 1] <= gc_210[i]
                   for i in range(len(gc_210) - 1)), (
        "expected (2,1,0) to be a genuine counterexample to universal "
        "monotonic decrease -- if it is now also monotonic, the "
        "direction-dependence claim should be re-checked", gc_210)

    return {"gc_k0": gc0_grid, "gc_sweep_111": gc_111,
            "gc_sweep_311": gc_311, "gc_sweep_210": gc_210,
            "111_and_311_monotonically_decreasing": True,
            "210_is_a_counterexample": True}


CHECKS = (
    ("A1_axis_identity_exact", check_A1_axis_identity_exact),
    ("A2_in_plane_offset_nonzero", check_A2_in_plane_offset_nonzero),
    ("B1_closed_form_converges_monotonically",
     check_B1_closed_form_converges_monotonically),
    ("B2_dense_scan_quantified_improvement",
     check_B2_dense_scan_quantified_improvement),
    ("B3_gc_k_sweep_decreasing", check_B3_gc_k_sweep_decreasing),
)


def check_all(perturb_k0_threshold=None):
    """Registry entry point. Returns the full result dict.

    One declared control (D9/H2, `control:` on
    `F401-photon-bound-state-finite-k`):

    ``--param perturb_k0_threshold=break``  B3 compares g_c(k=0, closed)
        against a deliberately wrong reference (gc0_grid + 0.5) instead of
        the true k=0 grid value. Must go RED -- otherwise the k=0 agreement
        control (checking the fix changes nothing F169 already certified)
        could not actually catch a broken closed-form threshold at k=0.
    """
    kw = {"check_B3_gc_k_sweep_decreasing":
          {"perturb_k0_threshold": perturb_k0_threshold}}
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    out["verdict"] = fk.report()["verdict"]
    return out


# --- no pytest surface ------------------------------------------------------
# Deliberately no thin `test_*` wrappers: this record is an `entry:` record.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
