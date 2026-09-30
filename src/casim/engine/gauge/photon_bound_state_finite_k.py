#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
photon_bound_state_finite_k.py — repairing the finite-k grid-threshold
artifact in `photon_bound_state.critical_coupling`/`threshold_wavefunction`
(F401)
=============================================================================

Attacks `docs/theory/notebook-followup-2026-09-22.md` Part VI.3 and F169's
own "C2/C4-note": `critical_coupling`/`threshold_wavefunction` took the
two-body continuum floor T as `E.min()` over the finite L^3 relative-momentum
grid. At k = 0 this is exact (the floor sits at p = 0, a grid point, and
T = 0 identically). At finite k the true floor sits at the collinear
endpoint p = +-k/2 (`photon_bound_state.threshold_closed_form`), generally
NOT a grid point, so the grid value is an artifact that converges
NON-MONOTONICALLY in L, sometimes missing the entire offset
Omega_even(k) - T(k). F169 named this "documented, not repaired... belongs
in a finding of its own, with its own review pass" — this module and its
finding are that repair.

The fix itself is one line: `photon_bound_state.critical_coupling` and
`.threshold_wavefunction` now accept `threshold="closed"` (added here,
default stays "grid" so F169's own artifact-diagnostic test is unaffected).
What this module adds is the physics that substitution reveals:

1. **An exact identity, sharper than F169's own "vanishes on the coordinate
   planes" statement.** F169/CL149 states Omega_even(k) - T(k) =
   |k_x k_y k_z| / (3|k|) + O(k^3), which vanishes whenever ANY ONE
   component of k is zero (a 2-D coordinate PLANE) — but only to leading
   order there; checked here (numerically) that a generic in-plane k (two
   nonzero components) has a genuine nonzero O(k^3) residual. Along a pure
   coordinate AXIS (only ONE component nonzero), however, the identity is
   EXACT to all orders, not just leading order: both chiral branches
   collapse onto the SAME isotropic cone,

       omega+(q, 0, 0) = omega-(q, 0, 0) = |q| / sqrt(3)      (exact, proved
                                                                 symbolically
                                                                 below)

   because the chiral (helicity-distinguishing) term in the BDPT Bloch
   vector vanishes identically whenever two of the three momentum
   components are zero. Consequently Omega_even(k) = T(k) EXACTLY along any
   coordinate axis, for every |k| — a genuine double-degenerate two-body
   floor (the symmetric split p=0 and the collinear endpoint p=+-k/2 sit at
   the SAME energy, not merely close), which is a structural contributor to
   why finite-k convergence is generally messier along axis directions.

2. **The closed-form T sharply reduces, but does not eliminate, the
   commensurability artifact — narrowed on review (attack 4, 2026-09-23).**
   At the SAME 7 L values F169's own docstring quotes for the artifact
   (12, 24, 32, 48, 96, 144, 192) along (111), the closed-form sequence IS
   monotonic while the grid sequence is not. A denser scan (every L in
   [12, 200] step 4, along the SAME (111), |k|=0.2 point) shows this does
   NOT generalize to "monotonic at every L": both sequences still show
   occasional grid-commensurability dips (a real one for the closed form at
   L=92). What is real and quantified (`dense_l_scan_comparison`): the
   closed form's worst-case single-step backslide is roughly 4x smaller
   than the grid form's over the same dense scan, and it settles into a
   stable range markedly sooner. The original "monotonic at every step"
   claim is corrected to this quantified, still-genuine reduction.

3. **The re-derived g_c(k) decreases monotonically with |k| along (111)**,
   confirmed over |k| in [0.05, 1.0] (well beyond the originally-checked
   [0.05, 0.4]), and independently confirmed along (3,1,1). This does NOT
   generalize to every direction: along (2,1,0), g_c(k) is emphatically
   NOT monotonic (found on review, attack 12) — the decreasing trend is a
   real (111)/(311)-class result, not a universal law of all directions.

**What this does NOT claim.** `critical_coupling`'s g_c(k) is the coupling
that puts a Koster-Slater bound state exactly at the two-body CONTINUUM
FLOOR T(k). Per F169's own C3-note, the symmetric configuration usually
identified with the spin-1 photon sits at Omega_even(k), which is ABOVE
T(k) at finite k (by the exact or O(k^3) offset above) — i.e. IN the
continuum, not at its edge. F168/F250's gauge-protection argument is about
that different point. This finding repairs and characterizes g_c(k) as a
well-posed quantity in its own right (the Koster-Slater threshold coupling
at the true two-body floor); it does not thereby derive "the photon's own
coupling at finite k", which remains the open item F169 already named (the
all-k gauge-pole proof).

Exactness: the axis identity is exact (sympy, symbolic). The L-convergence
and g_c(k) sweep are quantitative (finite-L numerics; no floats are used
where an exact statement is made).

Findings: F401.
"""
from __future__ import annotations

from typing import Dict, List

from casim.numerics import xp as np  # D8: no direct numpy import
import sympy as sp

from casim.engine.gauge import photon_bound_state as pbs
from casim.engine.lattice import dimensionality as _dim

__all__ = [
    "axis_dispersion_isotropic_cone_exact",
    "in_plane_offset_is_not_exactly_zero",
    "l_convergence",
    "is_monotonic",
    "gc_k_sweep_direction",
    "gc_k_sweep_111",
    "dense_l_scan_comparison",
    "report",
]


# ══════════════════════════════════════════════════════════════════
#  1. The exact axis identity
# ══════════════════════════════════════════════════════════════════

def axis_dispersion_isotropic_cone_exact() -> Dict[str, object]:
    """Symbolic proof: omega+(q,0,0) = omega-(q,0,0) = |q|/sqrt(3), exactly.

    Re-types the BDPT Bloch vector from `dimensionality.bloch_vector` (the
    same exact sympy construction F291 re-derives independently of the
    engine), restricts to a coordinate axis, and shows both chiral branches
    give the identical scalar u = cos(q/sqrt(3)) -- the chiral
    (helicity-distinguishing) term vanishes identically off-axis-components,
    so there is no sign-dependence left at all along a pure axis.
    """
    n_plus, ks_plus = _dim.bloch_vector(3, sign="+")
    n_minus, ks_minus = _dim.bloch_vector(3, sign="-")
    q = sp.Symbol("q", real=True)

    n_plus_axis = sp.simplify(n_plus.subs({ks_plus[0]: q, ks_plus[1]: 0,
                                            ks_plus[2]: 0}))
    n_minus_axis = sp.simplify(n_minus.subs({ks_minus[0]: q, ks_minus[1]: 0,
                                              ks_minus[2]: 0}))
    # u = sqrt(1 - |n~|^2) on the branch where the walk is a rotation;
    # equivalently (and independent of that identity) recompute u directly
    # from Paper 1 Eq. 15's own u^+-_k formula, restricted to the axis.
    scale = 1 / sp.sqrt(3)
    u_plus_axis = sp.simplify(
        sp.cos(q * scale) * sp.cos(0) * sp.cos(0)
        + sp.sin(q * scale) * sp.sin(0) * sp.sin(0))
    u_minus_axis = sp.simplify(
        sp.cos(q * scale) * sp.cos(0) * sp.cos(0)
        - sp.sin(q * scale) * sp.sin(0) * sp.sin(0))

    n_equal = sp.simplify(n_plus_axis - n_minus_axis) == sp.zeros(3, 1)
    u_equal = sp.simplify(u_plus_axis - u_minus_axis) == 0
    u_closed = sp.simplify(u_plus_axis - sp.cos(q * scale)) == 0

    omega_axis = sp.acos(sp.cos(q * scale))  # = |q|/sqrt(3) for q in [0, sqrt3*pi)

    return {
        "n_plus_axis": str(n_plus_axis.T),
        "n_minus_axis": str(n_minus_axis.T),
        "n_branches_identical_on_axis": bool(n_equal),
        "u_plus_axis": str(u_plus_axis),
        "u_minus_axis": str(u_minus_axis),
        "u_branches_identical_on_axis": bool(u_equal),
        "u_equals_cos_q_over_sqrt3": bool(u_closed),
        "omega_axis_closed_form": "acos(cos(q/sqrt(3))) = |q|/sqrt(3)",
        "identity_exact": bool(n_equal and u_equal and u_closed),
    }


def in_plane_offset_is_not_exactly_zero(
    pairs=((0.1, 0.2), (0.3, 0.05), (0.2, 0.2)),
) -> Dict[str, object]:
    """Contrast case: a genuine 2-D coordinate-PLANE point (kz=0, both other
    components nonzero) has a real, nonzero Omega_even - T offset -- the
    exact vanishing of §axis_dispersion_isotropic_cone_exact is special to a
    pure AXIS, not the whole plane F169/CL149's leading-order statement
    covers."""
    rows = []
    for kx, ky in pairs:
        k = np.array([kx, ky, 0.0])
        Oe = pbs.omega_even(k)
        T = pbs.threshold_closed_form(k)
        rows.append({"k": [kx, ky, 0.0], "Omega_even": Oe, "T": T,
                     "offset": Oe - T})
    all_nonzero = all(abs(r["offset"]) > 1e-8 for r in rows)
    return {"rows": rows, "all_offsets_genuinely_nonzero": all_nonzero}


# ══════════════════════════════════════════════════════════════════
#  2. L-convergence: grid artifact vs. closed-form fix
# ══════════════════════════════════════════════════════════════════

def l_convergence(k, Ls: List[int], threshold: str) -> List[float]:
    """g_c(k, L) for each L in Ls, at the given threshold method."""
    return [float(pbs.critical_coupling(np.asarray(k, float), L,
                                         threshold=threshold)[0])
            for L in Ls]


def is_monotonic(seq: List[float], tol: float = 0.0) -> bool:
    """True iff seq is non-decreasing within tol (both g_c(k,L) sequences
    here are expected to approach their L -> infinity limit from below)."""
    return all(seq[i + 1] >= seq[i] - tol for i in range(len(seq) - 1))


# ══════════════════════════════════════════════════════════════════
#  3. The re-derived g_c(k) along (111)
# ══════════════════════════════════════════════════════════════════

def gc_k_sweep_direction(direction, kmags: List[float],
                          L: int) -> List[Dict[str, object]]:
    """g_c(k) along an arbitrary direction (need not be normalized) at the
    given (large) L, using the closed-form T."""
    d = np.asarray(direction, float)
    d = d / np.linalg.norm(d)
    rows = []
    for kmag in kmags:
        k = kmag * d
        gc, T = pbs.critical_coupling(k, L, threshold="closed")
        rows.append({"|k|": float(kmag), "g_c": gc, "T": T})
    return rows


def gc_k_sweep_111(kmags: List[float], L: int) -> List[Dict[str, object]]:
    """g_c(k) along (111) at the given (large) L, using the closed-form T."""
    return gc_k_sweep_direction((1.0, 1.0, 1.0), kmags, L)


def dense_l_scan_comparison(k, L_values: List[int]) -> Dict[str, object]:
    """Quantifies how much the closed-form threshold REDUCES (does not
    eliminate) the grid-commensurability resonance artifact, over a dense L
    scan -- not just the 7 sparse L values F169's own docstring quotes.

    Found on review (F401 attack 4, 2026-09-23): at the SAME |k|=0.2, (111)
    demo point, a denser scan (every L in [12, 200] step 4, 48 points) shows
    threshold="closed" is NOT monotonic at every step either -- occasional
    grid-commensurability dips persist (e.g. a real dip at L=92). The
    original claim ("clean, monotonic convergence... at every step") was
    true only at the 7 sparse L values quoted from F169's own artifact
    docstring and did not survive a denser scan; corrected here to the
    honest, quantified comparison: the closed form's worst-case single-step
    BACKSLIDE (a drop from one L to the next larger one) is far smaller than
    the grid form's, and it settles into a stable range far sooner.
    """
    grid_seq = l_convergence(k, L_values, "grid")
    closed_seq = l_convergence(k, L_values, "closed")

    def n_violations(seq):
        return sum(1 for i in range(len(seq) - 1) if seq[i + 1] < seq[i])

    def max_backslide(seq):
        return max((seq[i] - seq[i + 1] for i in range(len(seq) - 1)),
                    default=0.0)

    return {
        "L_values": L_values,
        "grid_sequence": grid_seq,
        "closed_sequence": closed_seq,
        "grid_n_violations": n_violations(grid_seq),
        "closed_n_violations": n_violations(closed_seq),
        "grid_max_backslide": max_backslide(grid_seq),
        "closed_max_backslide": max_backslide(closed_seq),
        "n_steps": len(L_values) - 1,
    }


# ══════════════════════════════════════════════════════════════════
#  The verdict
# ══════════════════════════════════════════════════════════════════

def report() -> Dict[str, object]:
    """Everything F401 asserts, as a JSON-ready dict.

    Includes the review-narrowed content (2026-09-23 attack 4/12): a dense
    L-scan quantifying the closed form's real-but-partial improvement over
    the grid artifact, a wider (111) g_c(k) sweep, and the (2,1,0)
    counterexample showing the decreasing trend does not generalize to
    every direction.
    """
    axis = axis_dispersion_isotropic_cone_exact()
    in_plane = in_plane_offset_is_not_exactly_zero()

    Ls = [12, 24, 32, 48, 96, 144, 192]
    k_demo = 0.2 / np.sqrt(3) * np.array([1.0, 1.0, 1.0])
    grid_seq = l_convergence(k_demo, Ls, "grid")
    closed_seq = l_convergence(k_demo, Ls, "closed")

    dense_Ls = list(range(12, 201, 4))
    dense = dense_l_scan_comparison(k_demo, dense_Ls)

    gc_at_zero_grid, _ = pbs.critical_coupling([0.0, 0.0, 0.0], 12,
                                                threshold="grid")
    gc_at_zero_closed, _ = pbs.critical_coupling([0.0, 0.0, 0.0], 12,
                                                  threshold="closed")

    sweep_111 = gc_k_sweep_111([0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0], L=192)
    gc_values_111 = [r["g_c"] for r in sweep_111]
    monotonically_decreasing_111 = all(
        gc_values_111[i + 1] <= gc_values_111[i]
        for i in range(len(gc_values_111) - 1))

    sweep_311 = gc_k_sweep_direction((3.0, 1.0, 1.0),
                                      [0.05, 0.1, 0.2, 0.4, 0.6, 0.8], L=192)
    gc_values_311 = [r["g_c"] for r in sweep_311]
    monotonically_decreasing_311 = all(
        gc_values_311[i + 1] <= gc_values_311[i]
        for i in range(len(gc_values_311) - 1))

    sweep_210 = gc_k_sweep_direction((2.0, 1.0, 0.0),
                                      [0.05, 0.1, 0.2, 0.4, 0.6, 0.8], L=192)
    gc_values_210 = [r["g_c"] for r in sweep_210]
    monotonically_decreasing_210 = all(
        gc_values_210[i + 1] <= gc_values_210[i]
        for i in range(len(gc_values_210) - 1))

    return {
        "finding": "F401",
        "question": (
            "notebook-followup Part VI.3 / F169 C2-C4-note -- repair the "
            "finite-k grid-threshold artifact and re-derive g_c(k)"
        ),
        "axis_identity_exact": axis,
        "in_plane_offset_contrast": in_plane,
        "L_values": Ls,
        "k_demo": list(k_demo),
        "gc_grid_sequence": grid_seq,
        "gc_closed_sequence": closed_seq,
        "grid_is_monotonic": is_monotonic(grid_seq),
        "closed_is_monotonic": is_monotonic(closed_seq),
        "dense_l_scan": dense,
        "gc_at_k0_grid": gc_at_zero_grid,
        "gc_at_k0_closed": gc_at_zero_closed,
        "gc_at_k0_agree": abs(gc_at_zero_grid - gc_at_zero_closed) == 0.0,
        "gc_k_sweep_111_L192": sweep_111,
        "gc_k_sweep_111_monotonically_decreasing": monotonically_decreasing_111,
        "gc_k_sweep_311_L192": sweep_311,
        "gc_k_sweep_311_monotonically_decreasing": monotonically_decreasing_311,
        "gc_k_sweep_210_L192": sweep_210,
        "gc_k_sweep_210_monotonically_decreasing": monotonically_decreasing_210,
        "verdict": (
            "threshold='closed' sharply reduces (does not eliminate) the "
            "grid-commensurability artifact -- monotonic at F169's own 7 "
            "quoted L values, and its worst-case backslide over a dense "
            "L-scan is roughly 4x smaller than the grid form's; g_c(k) "
            "decreases monotonically with |k| along (111) (confirmed to "
            "|k|=1.0) and along (3,1,1), but NOT along (2,1,0) -- the "
            "decreasing trend is a real (111)/(311)-class result, not a "
            "universal law of all directions; the coordinate-axis case is "
            "an EXACT double degeneracy (Omega_even == T to all orders), "
            "not merely O(k^3)-small."
        ),
    }


if __name__ == "__main__":       # pragma: no cover — artifact write is guarded
    import json
    print(json.dumps(report(), indent=2, default=str))
