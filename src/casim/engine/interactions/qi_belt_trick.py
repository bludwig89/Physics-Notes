#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qi_belt_trick.py — the belt-trick / homotopy residual named in F289 (F330)
============================================================================

2026-08-27 - 16:xx

F289 closed completeness row A9's algebraic content — the spin-statistics
theorem's two INPUTS (the spatial dimension, the 2\\pi rotor phase) are both
model OUTPUTS — but named two things left external in its "what remains"
list, item 2 in particular:

    "The homotopy between exchange and 2\\pi rotation (the belt trick) is
    likewise the external Finkelstein-Rubinstein construction. A lattice-
    native version ... is the natural next step and is *not* done here."

completeness-2026-08-20.md row A9 records this as PARTIAL: "topological step
external ... pi_1 = S_n and belt-trick homotopy stay external."

What this module does, and does NOT do
---------------------------------------
It does **not** re-derive the belt trick from the model's own discrete BCC
structure. That attempt was made and abandoned — see F330 Sec.3 for why: the
belt trick's geometric content (parallel transport of a frame around a loop
on the RELATIVE-POSITION sphere S^2) is a fact about the topology of
*continuous* R^3, not about the lattice's finite point group O_h, and nothing
in the BCC structure supplies a substitute.

What it DOES do is narrow and pin down the residual precisely, using the
peer-reviewed formalisation of Anastopoulos (Charis Anastopoulos, "Spin-
statistics theorem and geometric quantisation," quant-ph/0110169, published
version J. Phys. A), which isolates the belt trick's non-topological content
as a single named "Postulate 1": exchange must be realisable as a smooth
one-parameter path in the rotation group whose square composes to exactly
one 2\\pi rotation, with no alternative path homotopy-inequivalent to it
(guaranteed by pi_1(S^2) = 0, i.e. R^3 minus the origin retracts to a
SIMPLY CONNECTED space, so the exchange path is unique up to homotopy and
the "rotate the connecting rod by pi, twice" representative may be used with
no loss of generality).

Given Postulate 1, this module verifies — using the model's OWN su2_rotor,
the identical rotor already carrying F289's R(2\\pi) = -1 result — the two
representation-theoretic facts that make Postulate 1's consequence concrete
for a spin-1/2 pair:

  B1  the antisymmetric two-spin singlet is an EXACT scalar (trivial-
      representation) eigenstate of the diagonal action R(theta,n)⊗R(theta,n)
      for *every* angle theta and *every* axis n — not merely "1-dimensional
      hence automatically scalar" (a tautology this module deliberately does
      NOT rest on): the check is that the rotated singlet does not LEAK into
      the orthogonal (triplet) subspace, which is the substantive fact. (This
      is forced, for ANY su(2) rotor with det=1, by a linear-algebra identity
      on the antisymmetric tensor — see the module's own review note below —
      so the sweep is an implementation-correctness check, not a search for
      new physics; the substantive content is that the true singlet, and not
      the wrong (triplet) state B1's control substitutes, is the invariant one.)
  B2  the symmetric triplet is invariant as a subspace (B2b) but is NOT a
      scalar representation at theta = pi (the belt trick's single-exchange
      angle): its restriction is a genuine spin-1 rotation with eigenvalues
      {-1, +1, -1}, not a multiple of the identity. This is the reason the
      naive "exchange = a single c-number phase" identification is clean
      for the antisymmetric (fermionic) channel and does not directly apply
      to the symmetric one — the substance of why the general n>2 / higher-
      spin case is the open "Berry-Robbins problem" and not a corollary.
  B3  two applications of the theta=pi exchange rotation compose, by the
      operator-composition law R(theta)^2 = R(2 theta), to EXACTLY F289's
      own R(2 pi) = -1 per constituent — i.e. Postulate 1's "exchange
      squared = one 2 pi rotation" is not a new number, it is F289 S1's
      number, reused, not re-derived.
  CONTROLS  (i) replacing the true antisymmetric singlet with the m=0
      TRIPLET member (the same normalisation, the wrong sign) breaks B1's
      invariance under a generic (non-axis-aligned) rotation; (ii) evaluating
      B2 at theta=2*pi instead of pi makes the triplet scalar again
      (integer-spin 2pi-periodicity). Both demonstrate the checks are real
      statements, not tautologies -- see check_belt_trick_reduction's
      docstring for the exact `--param` invocations.

Net verdict (stated before the numbers, because the framing is the point):
Postulate 1 is NOT eliminated. It is precisely NAMED (previously "the belt
trick, imported" — now Anastopoulos's Postulate 1, with a citation and an
exact statement of what it asserts), and its consequence for the spin-1/2
pair specifically is machine-verified using the model's own rotor rather
than asserted. Whether Postulate 1 itself is any less arbitrary IN THIS
MODEL than in generic non-relativistic QM is a separate, narrower argument
made in F330 Sec.4 in prose (the model has no spin Hilbert space independent
of the SU(2) rotor built in F26/decision 2, so there is no rival transport
law available to postulate instead) — that argument is NOT a numeric check
and is not represented in this module's checks, because it cannot be
"machine-verified" any more than the absence of an alternative can be
exhibited; it is stated as a POSIT-narrowing claim, honestly labelled as
such in the finding.

Cross-references: F289 (the rotor, R(2pi)=-1, SWAP^2=1), F291/F292 (d=3
derived), F26 (the rotor's origin, decision 2). External: Finkelstein &
Rubinstein, J. Math. Phys. 9 (1968) 1762; Anastopoulos, quant-ph/0110169
("Spin-statistics theorem and geometric quantisation"); Berry & Robbins,
Proc. R. Soc. A 453 (1997) 1771 (the geometric-phase route this module's C1
is the n=2, spin-1/2 special case of — the general n, general-spin problem
is the still only partially resolved "Berry-Robbins problem").
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from casim.numerics import xp as np

from casim.engine.interactions.qi_spin_statistics import _rotor_for_physical_angle

__all__ = [
    "singlet_state",
    "triplet_m0_state",
    "singlet_invariance_sweep",
    "triplet_scalar_deviation",
    "exchange_squared_is_f289_r2pi",
    "check_belt_trick_reduction",
    "summary",
]

# ======================================================================
# The two-spin states.  Built explicitly from Pauli kets so nothing is
# imported pre-labelled "the singlet" — the ANTIsymmetric combination is
# constructed and then checked, not assumed to be special.
# ======================================================================
_UP = np.array([1.0, 0.0], dtype=complex)
_DOWN = np.array([0.0, 1.0], dtype=complex)


def singlet_state() -> np.ndarray:
    """(|up down> - |down up>) / sqrt(2) — the antisymmetric combination."""
    v = np.kron(_UP, _DOWN) - np.kron(_DOWN, _UP)
    return v / np.linalg.norm(v)


def triplet_m0_state() -> np.ndarray:
    """(|up down> + |down up>) / sqrt(2) — the SYMMETRIC, same-normalisation
    combination.  Used only as the CONTROL: same shape, wrong sign, and it is
    a physically real state (the triplet's m=0 member) rather than a straw
    man."""
    v = np.kron(_UP, _DOWN) + np.kron(_DOWN, _UP)
    return v / np.linalg.norm(v)


def _diagonal_rotor(theta: float, axis) -> np.ndarray:
    """R_phys(theta, axis) tensor R_phys(theta, axis) — the diagonal (equal,
    same-axis) action on the two-spin space that a rigid rotation of the
    whole two-body system by the PHYSICAL angle `theta` realises.

    `su2_rotor(theta, n)` is parametrised by the BLOCH angle (a physical
    rotation by `theta` is `su2_rotor(theta/2, n)` — see its own docstring,
    and qi_spin_statistics._rotor_for_physical_angle, which this module
    reuses so the two convention choices cannot drift apart).
    """
    R = _rotor_for_physical_angle(theta, axis)
    return np.kron(R, R)


def _fibonacci_axes(n: int):
    """Deterministic axis sweep (no RNG), matching F289's own convention in
    qi_spin_statistics.rotor_phase_axis_independence."""
    golden = math.pi * (3.0 - math.sqrt(5.0))
    axes = []
    for i in range(n):
        z = 1.0 - 2.0 * (i + 0.5) / n
        r = math.sqrt(max(0.0, 1.0 - z * z))
        th = golden * i
        axes.append((r * math.cos(th), r * math.sin(th), z))
    return axes


# ======================================================================
# C1 — the true singlet is an exact scalar (trivial-rep) eigenstate for
#      EVERY angle and EVERY axis: it never leaks into the triplet sector.
# ======================================================================
def singlet_invariance_sweep(n_axes: int = 12, n_angles: int = 12,
                             use_wrong_state: bool = False) -> Dict[str, Any]:
    """Sweep (axis, angle) pairs; for each, apply the diagonal rotor to the
    tested state and measure how much of the result lands OUTSIDE the span
    of the original state (the leak).  For the true singlet this is 0.0 to
    machine precision for every pair swept, and the retained coefficient is
    exactly 1 (not just a phase of modulus 1) — the trivial representation.

    `use_wrong_state=True` is the CONTROL (see triplet_m0_state): the same
    normalisation, the symmetric combination instead of the antisymmetric
    one.  It is NOT invariant under a generic (non-axis-aligned) rotation,
    which is what makes the true-singlet result a real statement rather than
    "any 1-dimensional subspace is trivially scalar."
    """
    state = triplet_m0_state() if use_wrong_state else singlet_state()
    axes = _fibonacci_axes(n_axes)
    worst_leak = 0.0
    worst_phase_dev = 0.0
    for axis in axes:
        for j in range(n_angles):
            theta = 2.0 * math.pi * (j + 1) / n_angles  # generic angles too
            M = _diagonal_rotor(theta, axis)
            out = M @ state
            coeff = complex(np.vdot(state, out))         # <state|M|state>
            leak = out - coeff * state
            worst_leak = max(worst_leak, float(np.linalg.norm(leak)))
            worst_phase_dev = max(worst_phase_dev, abs(coeff - 1.0))
    return {"n_axes": n_axes, "n_angles": n_angles,
            "used_wrong_state": use_wrong_state,
            "worst_leak_outside_span": worst_leak,
            "worst_phase_deviation_from_one": worst_phase_dev}


# ======================================================================
# C2 — the triplet is invariant AS A SUBSPACE but is NOT a scalar rep at
#      theta = pi (the exchange angle) — the D^(1)(pi) = diag(-1,1,-1) fact.
# ======================================================================
def triplet_scalar_deviation(theta: float = math.pi,
                             axis=(0.0, 0.0, 1.0)) -> Dict[str, Any]:
    """Restrict R(theta,axis)⊗R(theta,axis) to the 3-dim triplet subspace
    (m = +1, 0, -1 in the given axis's own basis) and measure the deviation
    from a scalar multiple of the identity, ||M - (tr M / 3) I||.  At
    theta = pi this is exactly 2/sqrt(3) x the identity-normalised scale
    (eigenvalues {-1,+1,-1} vs mean -1/3); at theta = 0 (mod 2 pi) it is
    exactly 0, because integer-spin (triplet, j=1) representations ARE
    single-valued / 2 pi-periodic — unlike the half-integer rotor. That
    contrast (period pi vs 2 pi within the SAME two-spin space) is the
    reason the naive geometric argument is clean for the singlet and not
    for the triplet.
    """
    n = np.asarray(axis, dtype=float)
    n = n / np.linalg.norm(n)

    # Triplet basis, symmetric combinations (axis-agnostic construction: use
    # the eigenbasis of n.sigma on each spin, then symmetrise).
    # Build |+n>,|-n> single-spin eigenstates of n.sigma (eigenvalues +-1).
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    ndots = n[0] * sx + n[1] * sy + n[2] * sz
    w, v = np.linalg.eigh(ndots)
    plus = v[:, np.argmax(w)]
    minus = v[:, np.argmin(w)]
    t_plus = np.kron(plus, plus)
    t_zero = (np.kron(plus, minus) + np.kron(minus, plus)) / math.sqrt(2.0)
    t_minus = np.kron(minus, minus)
    basis = np.stack([t_plus, t_zero, t_minus], axis=1)   # 4x3

    M = _diagonal_rotor(theta, axis)
    Msub = basis.conj().T @ M @ basis                     # 3x3, should be
                                                            # block-diagonal
    # Subspace invariance: does M map the triplet span back into itself?
    leak = M @ basis - basis @ Msub
    leak_norm = float(np.linalg.norm(leak))

    scalar_part = np.trace(Msub) / 3.0
    dev = float(np.linalg.norm(Msub - scalar_part * np.eye(3, dtype=complex)))
    eigs = sorted(np.linalg.eigvals(Msub), key=lambda z: (z.real, z.imag))
    return {"theta": float(theta),
            "axis": tuple(float(a) for a in axis),
            "subspace_leak": leak_norm,
            "deviation_from_scalar": dev,
            "eigenvalues": [complex(e) for e in eigs]}


# ======================================================================
# C3 — bookkeeping: theta=pi applied twice is EXACTLY F289's R(2pi) = -1,
#      reused (not re-derived).  R(theta)^2 = R(2 theta) is the operator-
#      composition law, unconditionally true — its content here is which
#      NUMBER it reduces to, already established in F289.
# ======================================================================
def exchange_squared_is_f289_r2pi(theta_exchange: float = math.pi,
                                  axis=(0.0, 0.0, 1.0)) -> Dict[str, Any]:
    """Two applications of the theta_exchange rotation, composed by direct
    matrix multiplication (not by re-deriving R(2*theta) — the composition
    law is used, not assumed).  At theta_exchange = pi this equals the
    IDENTITY exactly, because F289 S1 already establishes R(2 pi) = -1 per
    constituent, so (-1)x(-1) = +1 on the pair: "exchange twice returns the
    identical physical state" (matching F289's independently-derived
    SWAP^2 = 1) is recovered here from the GEOMETRIC route, not reasserted.

    The single-constituent number quoted is F289's own
    `rotor_2pi_phase` residual, imported and surfaced, not recomputed by a
    second, potentially drifting implementation.
    """
    from casim.engine.interactions.qi_spin_statistics import rotor_2pi_phase

    M1 = _diagonal_rotor(theta_exchange, axis)
    M2 = M1 @ M1
    I4 = np.eye(4, dtype=complex)
    two_exchanges_residual = float(np.linalg.norm(M2 - I4))

    f289 = rotor_2pi_phase(axis=axis)
    return {"theta_exchange": float(theta_exchange),
            "two_exchanges_minus_identity_residual": two_exchanges_residual,
            "f289_single_constituent_r2pi_residual":
                f289["residual_R2pi_plus_identity"]}


# ======================================================================
# The registry entry point
# ======================================================================
def check_belt_trick_reduction(theta_exchange: float = math.pi,
                               wrong_singlet: bool = False) -> Dict[str, Any]:
    """The F330 gate.

    Declared controls:

    ``--param theta_exchange=6.283185307179586`` (2*pi instead of pi): the
        belt-trick's own single-exchange angle is pi, not 2pi. At 2pi the
        triplet becomes scalar again (integer-spin 2pi-periodicity), so the
        "triplet is non-scalar" assertion (B2) goes red -- demonstrating pi
        is the angle that makes the argument non-trivial, not an arbitrary
        choice.
    ``--param wrong_singlet=true``  substitute the m=0 TRIPLET member (same
        normalisation, wrong sign) for the tested state in B1.  Its
        invariance under a generic axis fails -- B1 goes red -- showing the
        singlet result is a real statement about the antisymmetric
        combination, not a tautology about 1-dimensional subspaces.
    """
    checks: List[Tuple[str, bool, Any]] = []

    # B1 -- true (or, under control, wrong) singlet invariance sweep
    sw = singlet_invariance_sweep(use_wrong_state=wrong_singlet)
    ok1 = (sw["worst_leak_outside_span"] < 1e-12
           and sw["worst_phase_deviation_from_one"] < 1e-12)
    checks.append(("B1 singlet: exact scalar eigenstate over axis x angle sweep",
                   ok1, sw["worst_leak_outside_span"]))

    # B2 -- triplet non-scalar at theta_exchange (default pi)
    td = triplet_scalar_deviation(theta=theta_exchange)
    ok2 = td["subspace_leak"] < 1e-12 and td["deviation_from_scalar"] > 0.5
    checks.append(("B2 triplet: invariant subspace, NOT a scalar rep at "
                   "theta_exchange", ok2, td["deviation_from_scalar"]))
    checks.append(("B2b triplet subspace leak (should be 0 -- it IS invariant)",
                   td["subspace_leak"] < 1e-12, td["subspace_leak"]))

    # B3 -- exchange-squared bookkeeping against F289
    esq = exchange_squared_is_f289_r2pi(theta_exchange=theta_exchange)
    ok3 = (esq["two_exchanges_minus_identity_residual"] < 1e-12
           and esq["f289_single_constituent_r2pi_residual"] < 1e-12)
    checks.append(("B3 two exchanges == identity, via F289's own R(2pi)",
                   ok3, esq["two_exchanges_minus_identity_residual"]))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"theta_exchange": theta_exchange,
                       "wrong_singlet": wrong_singlet},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    sw = singlet_invariance_sweep()
    td = triplet_scalar_deviation()
    esq = exchange_squared_is_f289_r2pi()
    return {
        "F330_singlet_worst_leak": sw["worst_leak_outside_span"],
        "F330_singlet_worst_phase_deviation": sw["worst_phase_deviation_from_one"],
        "F330_triplet_deviation_from_scalar_at_pi": td["deviation_from_scalar"],
        "F330_triplet_subspace_leak_at_pi": td["subspace_leak"],
        "F330_triplet_eigenvalues_at_pi":
            [str(e) for e in td["eigenvalues"]],
        "F330_two_exchanges_minus_identity": esq["two_exchanges_minus_identity_residual"],
        "F330_f289_r2pi_residual": esq["f289_single_constituent_r2pi_residual"],
    }


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_belt_trick_reduction()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F330_belt_trick_reduction.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("wrote", os.path.basename(out))
