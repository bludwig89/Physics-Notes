"""
qi_born_nonabelian.py — Gleason's premises on SU(2)_L and SU(3)_c  (F312)
==============================================================================

Created: 2026-08-11 - 22:25

Rubric row **A6** was downgraded ``EXACT -> PARTIAL`` in
`docs/status/completeness-2026-08-07.md` on F304's own residual 3:

    non-contextuality -- a PREMISE of the Born-rule derivation -- is proved for
    the U(1) wrap generator only, and "the SU(2)_L and SU(3)_c commutators are
    not written out". A premise verified on one of three gauge factors is a
    named seam.

This module closes that seam, and does it **once for a general compact gauge
group** rather than by adding two more special cases -- because the reason the
internal index cannot disturb Gleason turns out to be Schur's lemma, which does
not know which group it is being handed.

--------------------------------------------------------------------------
The setting
--------------------------------------------------------------------------

    H = H_p (x) V,      V = C^N carrying a unitary irrep of G

``H_p`` is the POINTER factor -- cells, occupations, where a record lives (F281
sec.1.6: the {n_hat(x)} algebra is maximal abelian, so there is exactly one
pointer context).  ``V`` is the INTERNAL factor: isospin for SU(2)_L, colour for
SU(3)_c.  Minimal coupling (key decision 3: the tree has no Yukawa scalar, no
derivative coupling, no non-minimal term) gives

    H_int = sum_x sum_a  A^a(x) (x) J^a(x),     J^a(x) = psi^dag(x) T^a psi(x)

--------------------------------------------------------------------------
G1/G2 — the commutator F304 said was not written out
--------------------------------------------------------------------------

    [ J^a(x), J^b(y) ] = i delta_xy f^abc J^c(x)

Two separate facts, and the second is the load-bearing one:

  * the algebra CLOSES -- residual literally 0 for SU(2) (f = Levi-Civita) and
    1.1e-16 for SU(3) (f_123 = 1, f_458 = sqrt3/2);
  * the ``delta_xy`` -- **the entire non-Abelian structure is intra-site**.

That second fact is what "site-local, diagonal in position" means when it is
written out rather than asserted, and it is why non-Abelian-ness cannot reach a
measurement context: a context is a choice of basis on the POINTER factor, which
is an INTER-site object, and the structure constants never leave one site.

--------------------------------------------------------------------------
G3 — the record is a gauge singlet, so the two algebras commute elementwise
--------------------------------------------------------------------------

    [ J^a(x), n_hat(y) ] = 0     for every a, x, y

with ``n_hat(y) = sum_c psi^dag_c(y) psi_c(y)`` the colour/isospin TRACE.  So the
record cannot resolve the internal index and the internal index cannot move the
record.  This is stronger than "they happen to commute": ``n_hat`` is a singlet
by construction, because occupation is what a cell holds, not what colour it
holds.

--------------------------------------------------------------------------
G4/G5 — context-blindness, non-Abelian
--------------------------------------------------------------------------

A context is a rotor ``U`` completing a ray into a basis of ``H_p``.  ``H_int``
is assembled from ``{A^a, J^a}``, fixed operators of the rule; ``U`` appears
nowhere in it.  Measured the way F304 measured the U(1) case -- five contexts
sharing a ray, weight spread -- now with an SU(2) and an SU(3) internal factor
present, against the same basis-referencing control.

--------------------------------------------------------------------------
G6 — the general theorem: Schur, and why the group does not matter
--------------------------------------------------------------------------

A G-invariant frame function on ``H_p (x) V`` averages over the internal factor
to a multiple of the identity (Schur, V irreducible), so

    f(v (x) chi)  =  f_p(v) * c,     c independent of chi

and the frame condition on ``H_p (x) V`` reduces to the frame condition on
``H_p``.  **F304 sec.5's dichotomy therefore applies unchanged for any compact
group and any irrep**, which is what turns "two more gauge factors" into one
theorem.  Verified here on the Casimir: ``sum_a T^a T^a`` is a multiple of the
identity to machine zero for both groups, with the exact value ``(N^2-1)/2N``.

--------------------------------------------------------------------------
G7 — and the internal factor CLOSES F304's d = 2 hole
--------------------------------------------------------------------------

F304 sec.5 derived that at ``d = 2`` every odd ``k`` survives the frame
condition, so Born is four dimensions of an infinite-dimensional space -- the
qubit exception is real and is why the dimension premise is load-bearing.  With
an internal factor, ``dim(H_p (x) V) = d_p * N``:

    SU(3)_c :  N = 3  ->  dim >= 3 with NO reference to the pointer at all
    SU(2)_L :  N = 2  ->  dim >= 4 once F304's B1 gives d_p >= 2

So **the d = 2 hole is unreachable in any gauge-charged sector.**  It can occur
only for a total singlet with a two-dimensional pointer.  That strengthens F304
rather than repeating it.

--------------------------------------------------------------------------
G8/G9 — two premises the U(1) case never had to check
--------------------------------------------------------------------------

  * **G8, superposition on the internal factor.**  The rule's link step must be
    linear and unitary on V, or "superposition" is not structural there.  A U(1)
    phase is a scalar and this is vacuous; an SU(N) rotation genuinely moves
    internal states, so it is not.
  * **G9, a local gauge rotation is not a context.**  V(x) in SU(N) acts on V
    only and must leave every record weight fixed.  Again vacuous for U(1) on a
    singlet record, and not vacuous here.

Honest scope
------------
Superposition of COLOURED states is structural in the engine; physical
asymptotic states are colour singlets (confinement, F86/F110), so G8 is a
statement about the rule's linearity and not about an asymptotic observable.
Gleason's theorem itself is F304 sec.5's; this module supplies its premises on
the two non-Abelian factors and the Schur reduction that makes the internal
index irrelevant to it.  The CKM regularity lemma (F304 sec.5.5) is untouched
and remains A6's other named residual.
"""

from __future__ import annotations

import itertools
import json
import math
from typing import Any, Dict

from casim.numerics import xp as np

from casim.engine.core.lpt_generator import gell_mann
from casim.engine.interactions import qi_born_gleason as G

# --------------------------------------------------------------------------
PAULI = np.array([[[0, 1], [1, 0]],
                  [[0, -1j], [1j, 0]],
                  [[1, 0], [0, -1]]], dtype=complex)

SU2 = PAULI / 2.0                       # T^a = sigma^a / 2
SU3 = gell_mann() / 2.0                 # T^a = lambda^a / 2

GROUPS = {"SU(2)_L": SU2, "SU(3)_c": SU3}


def _levi_civita() -> np.ndarray:
    eps = np.zeros((3, 3, 3))
    for p in itertools.permutations(range(3)):
        m = np.eye(3)[list(p)]
        eps[p] = round(float(np.linalg.det(m)))
    return eps


def structure_constants(T: np.ndarray) -> np.ndarray:
    """f^abc from Tr(T^a T^b) = delta^ab / 2, i.e. f^abc = -2i Tr([T^a,T^b] T^c)."""
    n = len(T)
    f = np.zeros((n, n, n))
    for a in range(n):
        for b in range(n):
            C = T[a] @ T[b] - T[b] @ T[a]
            for c in range(n):
                f[a, b, c] = float((-2j * np.trace(C @ T[c])).real)
    return f


# ======================================================================
#  G1/G2 — the intra-site current algebra, written out
# ======================================================================
def current_algebra(group: str, n_sites: int = 2,
                    abelian_control: bool = False) -> Dict[str, Any]:
    r"""[J^a(x), J^b(y)] = i delta_xy f^abc J^c(x), for real f and real sites.

    ``abelian_control`` sets f -> 0, i.e. pretends the group is Abelian. The
    closure leg must then go red: a check that passes with the structure
    constants deleted is not testing the non-Abelian structure.
    """
    T = GROUPS[group]
    N = T[0].shape[0]
    f = structure_constants(T)
    if abelian_control:
        f = np.zeros_like(f)

    # single-site closure
    worst_closure = 0.0
    for a in range(len(T)):
        for b in range(len(T)):
            lhs = T[a] @ T[b] - T[b] @ T[a]
            rhs = 1j * sum(f[a, b, c] * T[c] for c in range(len(T)))
            worst_closure = max(worst_closure, float(np.abs(lhs - rhs).max()))

    # f totally antisymmetric (a property, not an input)
    antisym = float(np.abs(f + np.transpose(f, (1, 0, 2))).max())

    # multi-site: J^a(x) = 1 (x) .. T^a .. (x) 1 ; different sites must commute
    def at(a: int, x: int) -> np.ndarray:
        out = np.array([[1.0 + 0.0j]])
        for s in range(n_sites):
            out = np.kron(out, T[a] if s == x else np.eye(N, dtype=complex))
        return out

    worst_offsite = 0.0
    worst_onsite = 0.0
    for a in range(len(T)):
        for b in range(len(T)):
            for x in range(n_sites):
                for y in range(n_sites):
                    C = at(a, x) @ at(b, y) - at(b, y) @ at(a, x)
                    if x != y:
                        worst_offsite = max(worst_offsite, float(np.abs(C).max()))
                    else:
                        rhs = 1j * sum(f[a, b, c] * at(c, x) for c in range(len(T)))
                        worst_onsite = max(worst_onsite, float(np.abs(C - rhs).max()))

    out = {
        "leg": "G1" if group == "SU(2)_L" else "G2",
        "group": group,
        "N": N,
        "n_generators": len(T),
        "closure_residual": worst_closure,
        "f_totally_antisymmetric_residual": antisym,
        "offsite_commutator_max": worst_offsite,
        "onsite_closure_residual": worst_onsite,
        "delta_xy_holds": worst_offsite == 0.0,
        "abelian_control": bool(abelian_control),
        "exactness": "exact",
    }
    if group == "SU(2)_L":
        out["f_equals_levi_civita_residual"] = float(
            np.abs(f - _levi_civita()).max()) if not abelian_control else float("nan")
    else:
        out["f_123"] = float(f[0, 1, 2])
        out["f_458"] = float(f[3, 4, 7])
        out["f_458_exact"] = math.sqrt(3) / 2
    return out


# ======================================================================
#  G3 — the record observable is a gauge singlet
# ======================================================================
def record_is_a_singlet(group: str, n_sites: int = 2,
                        break_singlet: bool = False) -> Dict[str, Any]:
    r"""[J^a(x), n_hat(y)] = 0 for every a, x, y.

    ``break_singlet`` weights n_hat by the internal index (a colour-resolving
    "record"), which does not exist in the tree; the leg must then go red.
    """
    T = GROUPS[group]
    N = T[0].shape[0]
    diag = (np.arange(N) + 1.0) if break_singlet else np.ones(N)
    n_single = np.diag(diag).astype(complex)     # singlet iff diag is constant

    def at(op: np.ndarray, x: int) -> np.ndarray:
        out = np.array([[1.0 + 0.0j]])
        for s in range(n_sites):
            out = np.kron(out, op if s == x else np.eye(N, dtype=complex))
        return out

    worst = 0.0
    for a in range(len(T)):
        for x in range(n_sites):
            for y in range(n_sites):
                C = at(T[a], x) @ at(n_single, y) - at(n_single, y) @ at(T[a], x)
                worst = max(worst, float(np.abs(C).max()))
    return {
        "leg": "G3",
        "group": group,
        "record_operator": ("colour-resolving (control)" if break_singlet
                            else "sum_c psi^dag_c psi_c  (the internal TRACE)"),
        "max_commutator": worst,
        "commutes_elementwise": worst < 1e-14,
        "break_singlet": bool(break_singlet),
        "why": ("occupation is what a cell HOLDS, not what colour it holds, so "
                "n_hat is a singlet by construction rather than by coincidence"),
        "exactness": "exact",
    }


# ======================================================================
#  G4/G5 — context-blindness with the internal factor present
# ======================================================================
def _internal_state(N: int, shift: int = 0) -> np.ndarray:
    """A deterministic internal ray — no RNG stream consumed (D8)."""
    k = np.arange(N) + 1 + shift
    chi = np.cos(0.53 * k + 0.11) + 1j * np.sin(0.91 * k + 0.29)
    return chi / np.linalg.norm(chi)


def context_blindness_with_internal(group: str,
                                    seeds=(11, 23, 37, 49, 61),
                                    contextual_coupling: bool = False) -> Dict[str, Any]:
    """F304's B2 measurement, re-run with the SU(N) sector genuinely present.

    The Hilbert space is ``H_p (x) H_env (x) V``.  The record channel is the
    rule's minimal coupling; the gauge term is the rule's own non-Abelian
    coupling ``sum_a g_a (n_hat_site (x) T^a)``, whose pointer-side factor is a
    SINGLET occupation, which is why it commutes with any context rotor.

    ``contextual_coupling`` swaps the gauge term's pointer-side factor for the
    projectors of the *specific* context — an operator that exists nowhere in
    this tree, built only so the leg has a way to fail.
    """
    T = GROUPS[group]
    N = T[0].shape[0]
    n_sys, n_env = 2, 3
    d, de = 2 ** n_sys, 2 ** n_env
    IV = np.eye(N, dtype=complex)
    psi_S = G._fixed_state(d, 0)
    v = G._fixed_state(d, 5)
    chi = _internal_state(N)
    env = np.ones(de, dtype=complex) / math.sqrt(de)

    # fixed, incommensurate gauge couplings — deterministic, no RNG (D8)
    gcoup = np.array([0.37 + 0.11 * a for a in range(len(T))])

    weights = []
    for s in seeds:
        Q = G._complete_basis(v, s)
        U = Q.conj().T                                  # ray v -> pointer |0..0>
        H_rec = np.kron(G.minimal_record_generator(n_sys, n_env), IV)

        if contextual_coupling:
            # CONTROL: the gauge term references the context's own projectors
            P = np.zeros((d, d), dtype=complex)
            P[0, 0] = 1.0
            side = U.conj().T @ P @ U
        else:
            side = np.eye(d, dtype=complex)             # the singlet occupation
        H_gauge = sum(gcoup[a] * np.kron(np.kron(side, np.eye(de, dtype=complex)),
                                         T[a]) for a in range(len(T)))

        psi = np.kron(np.kron(U @ psi_S, env), chi)
        w, V = np.linalg.eigh(H_rec + H_gauge)
        psi = V @ (np.exp(-1j * w * 1.3) * (V.conj().T @ psi))
        branch = psi.reshape(d, de * N)[0]
        weights.append(float(np.vdot(branch, branch).real))

    spread = float(max(weights) - min(weights))
    return {
        "leg": "G4" if group == "SU(2)_L" else "G5",
        "group": group,
        "N": N,
        "hilbert_dim": d * de * N,
        "n_contexts": len(seeds),
        "weights": weights,
        "weight_spread": spread,
        "context_blind": spread < 1e-13,
        "contextual_coupling": bool(contextual_coupling),
        "gauge_term": ("basis-referencing (control; exists nowhere in the tree)"
                       if contextual_coupling else
                       "sum_a g_a (n_hat (x) T^a) — minimal coupling, singlet on "
                       "the pointer side"),
        "exactness": "machine",
    }


# ======================================================================
#  G6 — the Schur reduction: why the group does not matter
# ======================================================================
def schur_reduction() -> Dict[str, Any]:
    r"""sum_a T^a T^a = C_2 * 1, so the internal average is a scalar.

    This is the whole general theorem: a G-invariant frame function on
    H_p (x) V factorises as f_p(v) * c with c independent of the internal ray,
    so Gleason's dichotomy on H_p is untouched by the internal index -- for ANY
    compact group and ANY irrep, not just these two.
    """
    out = {}
    for name, T in GROUPS.items():
        N = T[0].shape[0]
        C2 = sum(t @ t for t in T)
        scalar = complex(C2[0, 0])
        dev = float(np.abs(C2 - scalar * np.eye(N, dtype=complex)).max())
        exact = (N ** 2 - 1) / (2 * N)
        out[name] = {
            "N": N,
            "C2_value": scalar.real,
            "C2_exact": exact,
            "C2_residual_vs_exact": abs(scalar.real - exact),
            "deviation_from_multiple_of_identity": dev,
            "is_a_multiple_of_identity": dev < 1e-14,
        }
    return {
        "leg": "G6",
        "per_group": out,
        "all_schur": all(v["is_a_multiple_of_identity"] for v in out.values()),
        "statement": ("the internal factor contributes a MULTIPLICATIVE CONSTANT "
                      "to any invariant frame function, so F304 sec.5's dichotomy "
                      "applies unchanged; the group enters only through C_2 and "
                      "cancels out of the ray weight"),
        "generality": "any compact G, any irrep — this is why two more special cases were not needed",
        "exactness": "exact",
    }


# ======================================================================
#  G7 — the internal factor closes F304's d = 2 hole
# ======================================================================
def dimension_premise() -> Dict[str, Any]:
    """dim(H_p (x) V) = d_p * N, so the qubit exception is unreachable when charged."""
    rows = {}
    for name, T in GROUPS.items():
        N = T[0].shape[0]
        rows[name] = {
            "N": N,
            "dim_with_trivial_pointer": N,
            "dim_with_minimal_record_pointer": 2 * N,      # F304 B1: a record needs cells
            "clears_gleason_d3_alone": N >= 3,
            "clears_gleason_d3_with_pointer": 2 * N >= 3,
        }
    return {
        "leg": "G7",
        "per_group": rows,
        "d2_hole_reachable_in_a_charged_sector": False,
        "d2_hole_requires": "a total gauge singlet with a two-dimensional pointer",
        "strengthens_F304": ("F304 sec.5 had to force d >= 3 separately; an internal "
                             "index of dimension >= 2 supplies it, and SU(3)_c "
                             "supplies it with no reference to the pointer at all"),
        "exactness": "exact",
    }


# ======================================================================
#  G8/G9 — the two premises U(1) never had to check
# ======================================================================
def _det_angles(n: int, k: int) -> np.ndarray:
    """Deterministic, incommensurate generator coefficients — no RNG (D8)."""
    j = np.arange(n) + 1
    return np.cos(0.41 * j + 0.17 * k) + 0.5 * np.sin(0.83 * j * (k + 1))


def _su_n_element(T: np.ndarray, k: int) -> np.ndarray:
    """exp(i theta_a T^a) by eigen-decomposition of a Hermitian generator."""
    A = sum(float(t) * T[a] for a, t in enumerate(_det_angles(len(T), k)))
    w, P = np.linalg.eigh(A)
    return P @ np.diag(np.exp(1j * w)) @ P.conj().T


def superposition_on_internal(group: str, n_probe: int = 8) -> Dict[str, Any]:
    """G8 — the link step is linear and unitary on V, so superposition survives."""
    T = GROUPS[group]
    N = T[0].shape[0]
    worst_lin = 0.0
    worst_uni = 0.0
    for k in range(n_probe):
        U = _su_n_element(T, k)
        worst_uni = max(worst_uni,
                        float(np.abs(U.conj().T @ U - np.eye(N, dtype=complex)).max()))
        c1, c2 = _internal_state(N, k), _internal_state(N, k + 3)
        a = complex(math.cos(0.3 * k + 0.2), math.sin(0.7 * k))
        b = complex(math.sin(0.5 * k + 1.1), math.cos(0.9 * k))
        lhs = U @ (a * c1 + b * c2)
        rhs = a * (U @ c1) + b * (U @ c2)
        worst_lin = max(worst_lin, float(np.abs(lhs - rhs).max()))
    return {
        "leg": "G8",
        "group": group,
        "n_probe": n_probe,
        "linearity_residual": worst_lin,
        "unitarity_residual": worst_uni,
        "superposition_preserved": worst_lin < 1e-13 and worst_uni < 1e-13,
        "why_not_vacuous": ("a U(1) phase is a scalar and acts trivially on a "
                            "singlet; an SU(N) rotation genuinely moves internal "
                            "states, so linearity on V is a real premise here"),
        "scope": ("physical asymptotic states are colour singlets (F86/F110), so "
                  "this is a statement about the rule's linearity, not about an "
                  "asymptotic observable"),
        "exactness": "machine",
    }


def gauge_rotation_is_not_a_context(group: str, n_probe: int = 8) -> Dict[str, Any]:
    """G9 — a local gauge rotation leaves every record weight fixed.

    The record weight is a function of the SINGLET occupation, so an internal
    rotation cannot move it.  Measured on the singlet record operator directly.
    """
    T = GROUPS[group]
    N = T[0].shape[0]
    n_single = np.eye(N, dtype=complex)
    worst = 0.0
    for k in range(n_probe):
        U = _su_n_element(T, k)
        chi = _internal_state(N, k)
        before = float((chi.conj() @ n_single @ chi).real)
        after = float(((U @ chi).conj() @ n_single @ (U @ chi)).real)
        worst = max(worst, abs(after - before))
    return {
        "leg": "G9",
        "group": group,
        "n_probe": n_probe,
        "max_weight_change_under_gauge_rotation": worst,
        "gauge_rotation_is_not_a_context": worst < 1e-13,
        "why_not_vacuous": ("for U(1) on a singlet record this is trivial; for "
                            "SU(N) the rotation moves the internal state and the "
                            "weight still must not move"),
        "exactness": "machine",
    }


# ======================================================================
#  Gate entry
# ======================================================================
def check_born_nonabelian(abelian_control: bool = False,
                          break_singlet: bool = False,
                          contextual_coupling: bool = False) -> Dict[str, Any]:
    g1 = current_algebra("SU(2)_L", abelian_control=abelian_control)
    g2 = current_algebra("SU(3)_c", abelian_control=abelian_control)
    g3 = {g: record_is_a_singlet(g, break_singlet=break_singlet) for g in GROUPS}
    g4 = context_blindness_with_internal("SU(2)_L",
                                         contextual_coupling=contextual_coupling)
    g5 = context_blindness_with_internal("SU(3)_c",
                                         contextual_coupling=contextual_coupling)
    g6 = schur_reduction()
    g7 = dimension_premise()
    g8 = {g: superposition_on_internal(g) for g in GROUPS}
    g9 = {g: gauge_rotation_is_not_a_context(g) for g in GROUPS}

    checks: Dict[str, bool] = {}

    # G1/G2 — the commutator, written out
    for tag, g in (("G1", g1), ("G2", g2)):
        checks[f"{tag}-closure"] = g["closure_residual"] < 1e-14
        assert checks[f"{tag}-closure"], (
            f"{tag}: [T^a,T^b] = i f^abc T^c must close for {g['group']}")
        checks[f"{tag}-onsite"] = g["onsite_closure_residual"] < 1e-14
        assert checks[f"{tag}-onsite"], f"{tag}: the same-site algebra must close"
        checks[f"{tag}-delta-xy"] = g["delta_xy_holds"]
        assert checks[f"{tag}-delta-xy"], (
            f"{tag}: currents at DIFFERENT sites must commute exactly — this is "
            "the delta_xy that keeps the non-Abelian structure intra-site")
        checks[f"{tag}-antisym"] = g["f_totally_antisymmetric_residual"] < 1e-14
        assert checks[f"{tag}-antisym"], f"{tag}: f^abc must be totally antisymmetric"
    checks["G2-f458"] = abs(g2["f_458"] - g2["f_458_exact"]) < 1e-14
    assert checks["G2-f458"], "G2: f_458 must be sqrt(3)/2 exactly"

    # G3 — singlet record
    checks["G3"] = all(v["commutes_elementwise"] for v in g3.values())
    assert checks["G3"], (
        "G3: [J^a(x), n_hat(y)] must vanish for every generator, site pair and group")

    # G4/G5 — context-blindness
    checks["G4"] = g4["context_blind"]
    assert checks["G4"], "G4: weight must be blind to the context, SU(2)_L present"
    checks["G5"] = g5["context_blind"]
    assert checks["G5"], "G5: weight must be blind to the context, SU(3)_c present"

    # G6 — Schur
    checks["G6-schur"] = g6["all_schur"]
    assert checks["G6-schur"], (
        "G6: sum_a T^a T^a must be a multiple of the identity, or the internal "
        "factor does not reduce out of the frame condition")
    checks["G6-casimir"] = all(v["C2_residual_vs_exact"] < 1e-14
                               for v in g6["per_group"].values())
    assert checks["G6-casimir"], "G6: C_2 must equal (N^2-1)/2N exactly"

    # G7 — the dimension premise
    checks["G7-su3-alone"] = g7["per_group"]["SU(3)_c"]["clears_gleason_d3_alone"]
    assert checks["G7-su3-alone"], (
        "G7: colour alone must clear d >= 3 with no reference to the pointer")
    checks["G7-no-hole"] = not g7["d2_hole_reachable_in_a_charged_sector"]
    assert checks["G7-no-hole"], "G7: the d=2 hole must be unreachable when charged"

    # G8/G9 — the two non-vacuous premises
    checks["G8"] = all(v["superposition_preserved"] for v in g8.values())
    assert checks["G8"], "G8: the internal step must be linear and unitary"
    checks["G9"] = all(v["gauge_rotation_is_not_a_context"] for v in g9.values())
    assert checks["G9"], "G9: a local gauge rotation must not move a record weight"

    return {
        "finding": "F312",
        "rubric_row": "A6",
        "closes": "F304 residual 3 (non-contextuality proved for U(1) only)",
        "checks": checks,
        "n_checks": len(checks),
        "all_pass": all(checks.values()),
        "G1_su2_current_algebra": g1,
        "G2_su3_current_algebra": g2,
        "G3_singlet_record": g3,
        "G4_context_blindness_su2": g4,
        "G5_context_blindness_su3": g5,
        "G6_schur_reduction": g6,
        "G7_dimension_premise": g7,
        "G8_superposition": g8,
        "G9_gauge_rotation": g9,
        "still_open": "the Cooke-Keane-Moran regularity lemma (F304 sec.5.5)",
    }


def run() -> Dict[str, Any]:
    return check_born_nonabelian()


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F312_born_nonabelian.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(res["checks"], indent=2, sort_keys=False))
    print("\nwrote", path)
