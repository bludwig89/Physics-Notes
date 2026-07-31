# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_bcc_gauge.py
# migrated   : 2026-07-30 - 14:48
# target     : src/casim/engine/gauge/bcc_action.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_bcc_gauge.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed (S1/S2 code-clean already applied at F69/F91)
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_bcc_gauge.py — the gauge action on the *genuine* BCC lattice (F265)
=====================================================================
Before F265 the model's gauge sectors were split down the middle: the
propagators were BCC (``ca_bcc.bcc_dispersion(k/2, ±)`` — γ, W, Z, gluon all
route through it) while the **action** was simple-cubic.  Field strength was
built by first collapsing the eight BCC links into three straight ``±x, ±y,
±z`` composites of length 2 ("Build 6 effective SC links from BCC pairs",
``ca_wmu.py`` pre-F265) and then taking ordinary square plaquettes in the
three coordinate planes with ``a2 = 4.0``.

That construction is not merely inelegant, it is **blind**: there is an exact
family of link configurations on which every composite-SC plaquette equals the
identity to machine precision while the genuine BCC plaquettes are maximally
disordered.  Asymptotically it misses exactly **1/3** of the
curvature-carrying link degrees of freedom (F265 §K).  Both actions have the
*same* classical continuum limit, so the defect is invisible in weak-field
normalisation checks and shows up only as missing content — which is why the
composite plaquette left a non-zero Bianchi residual and why the Wilson
lattice-perturbation-theory gate could not be reproduced from it.

Geometry (all constants live in ``ca_lattice``, which is now the single source
of truth for BCC real-space structure):

* conventional cubic cell of side 2, so the nearest-neighbour hop is the
  integer vector ``d ∈ {±1}³`` and ``np.roll`` by ``d`` is an exact lattice
  translation;
* sites are the integer points whose three coordinates share a parity — index
  4 in ℤ³, i.e. only **1/4** of a cubic array's entries are lattice sites;
* no 3-bond closed loops exist, so the minimal gauge loop is a **4-bond
  rhombus** with sides ``(d1, d2)``, ``d2 ≠ ±d1``;
* every such rhombus has ``|d1 × d2| = 2√2`` and its normal on a ⟨110⟩
  face-diagonal axis; modulo translation there are exactly **6** orientations
  forming a single ``O_h`` orbit.

Link convention
---------------
One matrix field per **link axis** (4 of them, ``ca_lattice.BCC_LINK_AXES``);
the reverse direction is not stored but derived:

    U_{d}(x) = U_{−d}(x + d)†          ⟺        U_{−d}(x) = U_{d}(x − d)†

The public helpers accept the legacy 8-entry layout (one array per direction
in ``ca_lattice.BCC_HOP_DIRS`` order, matching ``ca_wmu.BCC_DIRS``) and this
identity is *checked*, not assumed — see ``link_reversal_residual``.

Field-strength reconstruction
-----------------------------
For a plaquette with sides ``(d1, d2)`` the loop phase is

    Φ_p^a = F^a_{μν} d1^μ d2^ν = 2 · m_p · f^a ,
    f^a := (F^a_{23}, −F^a_{13}, F^a_{12}),   m_p := (d1 × d2)/2 ∈ ⟨110⟩.

Because ``Σ_p m_p m_pᵀ = 4·I`` exactly over the 6 orientations, the Cartesian
field strength is recovered by a closed-form projection with **no**
pseudo-inverse and no conditioning issue:

    f^a = (1/8) Σ_p m_p Φ_p^a .

The 6 → 3 map is overdetermined; the residual of the reconstruction is a
free-standing consistency (Bianchi-type) diagnostic, exposed as
``cartesian_reconstruction_residual``.
"""

import numpy as np

from ca_lattice import (BCC_HOP_DIRS, BCC_LINK_AXES, BCC_PLAQUETTES,
                        BCC_PLAQ_NORMALS, BCC_PLAQ_LABELS, BCC_PLAQ_AREA,
                        bcc_site_mask)

__all__ = [
    'shift_by', 'link_for_direction', 'link_reversal_residual',
    'bcc_plaquette', 'bcc_plaquette_set', 'wilson_action_density',
    'plaquette_phases', 'cartesian_field_strength',
    'cartesian_reconstruction_residual',
    'su2_pair_to_matrix', 'su2_matrix_to_pair',
    'PAULI', 'plaquette_field_strength_su2', 'plaquette_field_strength_su3',
]

# ── generator bases ───────────────────────────────────────────────────────
PAULI = np.array([[[0, 1], [1, 0]],
                  [[0, -1j], [1j, 0]],
                  [[1, 0], [0, -1]]], dtype=complex)      # tr(τ^a τ^b) = 2δ

_DIR_INDEX = {tuple(d): i for i, d in enumerate(BCC_HOP_DIRS)}


# ══════════════════════════════════════════════════════════════════════════
#  array plumbing
# ══════════════════════════════════════════════════════════════════════════

def shift_by(A: np.ndarray, d) -> np.ndarray:
    """Return the field ``B`` with ``B[x] = A[x + d]`` (periodic).

    Integer ``np.roll`` is exact here: with the cubic cell at side 2 the BCC
    nearest-neighbour hop *is* the integer vector ``d``.  (Contrast
    ``ca_bcc.bcc_fractional_shift``, which implements the ``d/√3`` hop of the
    momentum-space walk — a different normalisation of the same lattice; see
    F265 §S.)
    """
    return np.roll(A, tuple(-int(c) for c in d), axis=(0, 1, 2))


def _dagger(A: np.ndarray) -> np.ndarray:
    """Hermitian conjugate of a (..., N, N) matrix field."""
    return np.conj(np.swapaxes(A, -1, -2))


def _matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return np.matmul(A, B)


def su2_pair_to_matrix(U_a: np.ndarray, U_b: np.ndarray) -> np.ndarray:
    """Convert the ``(a, b)`` SU(2) parametrisation to a (...,2,2) field.

    ``[[a, −b*], [b, a*]]`` — the convention used throughout ``ca_wmu``.
    """
    M = np.empty(U_a.shape + (2, 2), dtype=complex)
    M[..., 0, 0] = U_a
    M[..., 0, 1] = -np.conj(U_b)
    M[..., 1, 0] = U_b
    M[..., 1, 1] = np.conj(U_a)
    return M


def su2_matrix_to_pair(M: np.ndarray):
    """Inverse of :func:`su2_pair_to_matrix`."""
    return M[..., 0, 0].copy(), M[..., 1, 0].copy()


def _as_matrix_list(U_links):
    """Normalise the accepted link layouts to a list of 8 (...,N,N) fields."""
    if isinstance(U_links, dict):
        return [np.asarray(U_links[tuple(d)]) for d in BCC_HOP_DIRS]
    out = []
    for U in U_links:
        if isinstance(U, tuple) and len(U) == 2 and U[0].ndim == 3:
            out.append(su2_pair_to_matrix(U[0], U[1]))       # legacy SU(2)
        else:
            out.append(np.asarray(U))
    return out


# ══════════════════════════════════════════════════════════════════════════
#  links
# ══════════════════════════════════════════════════════════════════════════

def link_for_direction(U8, d) -> np.ndarray:
    """The link field for hop direction ``d``, from the 8-entry layout."""
    return _as_matrix_list(U8)[_DIR_INDEX[tuple(int(c) for c in d)]]


def link_reversal_residual(U_links) -> float:
    """``max‖ U_{−d}(x + d) − U_d(x)† ‖∞`` over the 4 axes.

    A consistent BCC link field stores one independent matrix per *axis*; the
    reverse direction must be the shifted dagger.  A non-zero residual means
    the eight stored directions carry 8 independent fields instead of 4, in
    which case the plaquettes are not the holonomies of any connection.
    """
    U = _as_matrix_list(U_links)
    worst = 0.0
    for d in BCC_LINK_AXES:
        nd = tuple(-c for c in d)
        lhs = shift_by(U[_DIR_INDEX[nd]], d)
        rhs = _dagger(U[_DIR_INDEX[tuple(d)]])
        worst = max(worst, float(np.abs(lhs - rhs).max()))
    return worst


def symmetrise_links(U_links):
    """Return an 8-entry layout in which the reversal identity holds exactly.

    The 4 axis fields in ``BCC_LINK_AXES`` are kept; the other 4 directions
    are *rebuilt* as ``U_{−d}(x) = U_d(x − d)†``.
    """
    U = _as_matrix_list(U_links)
    out = [None] * 8
    for d in BCC_LINK_AXES:
        out[_DIR_INDEX[tuple(d)]] = U[_DIR_INDEX[tuple(d)]]
        nd = tuple(-c for c in d)
        out[_DIR_INDEX[nd]] = shift_by(_dagger(U[_DIR_INDEX[tuple(d)]]), nd)
    return out


# ══════════════════════════════════════════════════════════════════════════
#  plaquettes
# ══════════════════════════════════════════════════════════════════════════

def bcc_plaquette(U_links, d1, d2) -> np.ndarray:
    """The 4-bond rhombic plaquette based at ``x`` with sides ``(d1, d2)``.

    Path ``x → x+d1 → x+d1+d2 → x+d2 → x``, i.e. steps ``d1, d2, −d1, −d2``::

        P(x) = U_{d1}(x) · U_{d2}(x+d1) · U_{−d1}(x+d1+d2) · U_{−d2}(x+d2)

    All four factors are genuine stored links (or their derived reversals), so
    ``P`` is the exact holonomy of the minimal loop — not a product of
    composite straight-line links.
    """
    U = symmetrise_links(U_links)
    d1 = tuple(int(c) for c in d1)
    d2 = tuple(int(c) for c in d2)
    n1 = tuple(-c for c in d1)
    n2 = tuple(-c for c in d2)

    x = (0, 0, 0)
    P = None
    for d in (d1, d2, n1, n2):
        A = U[_DIR_INDEX[d]]
        A = A if x == (0, 0, 0) else shift_by(A, x)
        P = A if P is None else _matmul(P, A)
        x = tuple(x[i] + d[i] for i in range(3))
    assert x == (0, 0, 0), "plaquette path did not close"
    return P


def bcc_plaquette_set(U_links) -> dict:
    """All 6 minimal plaquette orientations, keyed by ``BCC_PLAQ_LABELS``."""
    return {lab: bcc_plaquette(U_links, d1, d2)
            for lab, (d1, d2) in zip(BCC_PLAQ_LABELS, BCC_PLAQUETTES)}


def wilson_action_density(U_links, sites_only: bool = True) -> float:
    """Mean ``1 − Re tr P / N`` over the 6 orientations.

    With ``sites_only`` (default) the average runs over genuine BCC sites
    only — the all-same-parity quarter of the array (``bcc_site_mask``).
    Including the other 3/4 averages in points that are not lattice sites.
    """
    P6 = bcc_plaquette_set(U_links)
    any_P = next(iter(P6.values()))
    N = any_P.shape[-1]
    mask = bcc_site_mask(any_P.shape[:3]) if sites_only else None
    vals = []
    for P in P6.values():
        dens = 1.0 - np.real(np.trace(P, axis1=-2, axis2=-1)) / N
        vals.append(dens[mask] if mask is not None else dens)
    return float(np.mean(np.concatenate([v.ravel() for v in vals])))


# ══════════════════════════════════════════════════════════════════════════
#  field strength
# ══════════════════════════════════════════════════════════════════════════

def plaquette_phases(U_links, generators, g_lat: float = 1.0) -> dict:
    """Loop phases ``Φ_p^a`` for each of the 6 orientations.

    ``Φ^a = Im tr(T^a P) / (g · c)`` where ``tr(T^a T^b) = c δ^{ab}``; ``c`` is
    measured from the supplied basis rather than assumed, so both the Pauli
    (``c = 2``) and Gell-Mann/2 (``c = 1/2``) conventions work unchanged.

    Returns ``{label: (n_gen, Lx, Ly, Lz) real}``.
    """
    T = np.asarray(generators)
    c = float(np.real(np.trace(T[0] @ T[0])))
    out = {}
    for lab, (d1, d2) in zip(BCC_PLAQ_LABELS, BCC_PLAQUETTES):
        P = bcc_plaquette(U_links, d1, d2)
        phi = np.empty((T.shape[0],) + P.shape[:3])
        for a in range(T.shape[0]):
            tr = np.einsum('ij,xyzji->xyz', T[a], P)
            phi[a] = np.imag(tr) / (g_lat * c)
        out[lab] = phi
    return out


def _normal_matrix() -> np.ndarray:
    """The (6, 3) matrix of half-normals ``m_p``; satisfies ``MᵀM = 4·I``."""
    return np.array(BCC_PLAQ_NORMALS, dtype=float)


def cartesian_field_strength(U_links, generators, g_lat: float = 1.0) -> dict:
    """Cartesian ``F^a_{μν}`` from the 6 BCC plaquette orientations.

    Uses the exact closed-form projection ``f^a = (1/8) Σ_p m_p Φ_p^a`` with
    ``f^a = (F^a_{23}, −F^a_{13}, F^a_{12})``.

    Returns ``{'xy','xz','yz': (n_gen, Lx, Ly, Lz)}`` — the same keys the
    pre-F265 composite-SC routines returned, so downstream Yang-Mills steps
    need no change.
    """
    phi = plaquette_phases(U_links, generators, g_lat=g_lat)
    M = _normal_matrix()
    stack = np.stack([phi[lab] for lab in BCC_PLAQ_LABELS], axis=0)  # (6,a,...)
    f = np.tensordot(M, stack, axes=(0, 0)) / 8.0                    # (3,a,...)
    return {'yz': f[0], 'xz': -f[1], 'xy': f[2]}


def cartesian_reconstruction_residual(U_links, generators,
                                      g_lat: float = 1.0,
                                      mask: np.ndarray = None) -> float:
    """Relative residual of the overdetermined 6 → 3 field-strength fit.

    The 6 plaquette phases are reproduced by the 3 reconstructed Cartesian
    components exactly in the continuum limit; at finite field strength the
    leftover is the lattice's own higher-order/Bianchi content.  Returned
    normalised by the phase scale, so it is O(Φ²) for weak fields.

    ``mask`` restricts the comparison to a boolean sub-region of the spatial
    grid.  Pass one when the test configuration is not periodic (a linear
    gauge potential, say), so that torus-wrap sites do not dominate the max.
    """
    phi = plaquette_phases(U_links, generators, g_lat=g_lat)
    F = cartesian_field_strength(U_links, generators, g_lat=g_lat)
    f = np.stack([F['yz'], -F['xz'], F['xy']], axis=0)               # (3,a,...)
    M = _normal_matrix()
    pred = 2.0 * np.tensordot(M, f, axes=(1, 0))                    # (6,a,...)
    obs = np.stack([phi[lab] for lab in BCC_PLAQ_LABELS], axis=0)
    if mask is not None:
        pred, obs = pred[..., mask], obs[..., mask]
    scale = float(np.abs(obs).max())
    if scale == 0.0:
        return 0.0
    return float(np.abs(pred - obs).max() / scale)


# ── thin wrappers matching the legacy call signatures ────────────────────

def plaquette_field_strength_su2(U_links, g_lat: float = 1.0) -> dict:
    """SU(2) ``F^a_{μν}`` on the genuine BCC plaquettes.

    Drop-in replacement for the pre-F265 ``ca_wmu.plaquette_field_strength``:
    same ``(a, b)``-pair input layout, same ``{'xy','xz','yz'}`` output keys
    and ``(3, L, L, L)`` shapes.
    """
    return cartesian_field_strength(U_links, PAULI, g_lat=g_lat)


def plaquette_field_strength_su3(U_bcc, generators, g_lat: float = 1.0) -> dict:
    """SU(3) ``G^a_{μν}`` on the genuine BCC plaquettes.

    ``generators`` should be ``ca_strong.T_GEN`` (Gell-Mann/2).  Drop-in
    replacement for the pre-F265 ``ca_gluon.plaquette_field_strength_su3_bcc``.
    """
    return cartesian_field_strength(U_bcc, generators, g_lat=g_lat)
