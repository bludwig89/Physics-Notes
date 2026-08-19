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

import math

import numpy as np

from casim.numerics import rng as _rng

from casim.engine.lattice.geometry import (BCC_HOP_DIRS, BCC_LINK_AXES, BCC_PLAQUETTES,
                        BCC_PLAQ_NORMALS, BCC_PLAQ_LABELS, BCC_PLAQ_AREA,
                        bcc_site_mask)

__all__ = [
    'shift_by', 'link_for_direction', 'link_reversal_residual',
    'bcc_plaquette', 'bcc_plaquette_set', 'wilson_action_density',
    'plaquette_phases', 'cartesian_field_strength',
    'cartesian_reconstruction_residual',
    'su2_pair_to_matrix', 'su2_matrix_to_pair',
    'PAULI', 'plaquette_field_strength_su2', 'plaquette_field_strength_su3',
    # 3+1D sampler and observables (BCC_3 x Z time)
    'TIME_AXIS', 'BCC4_LOOPS', 'BCC4_N_LOOPS', 'BCC4_MIXED_AREA',
    'BCC4_STAPLE_TERMS', 'shift4',
    'cold_links_4d', 'hot_links_4d', 'unitarity_residual_4d',
    'plaquette_4d', 'plaquette_traces_4d', 'mean_plaquette_4d',
    'wilson_action_4d', 'staple_sum', 'staple_identity_residual',
    'sweep_4d', 'thermalise_4d',
    'wilson_loop_rt', 'wilson_loop_table', 'creutz_ratios',
    'polyakov_loop_4d', 'gauge_transform_4d', 'check_bcc_gauge_mc',
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


# ══════════════════════════════════════════════════════════════════════════
#  3+1D: the BCC spatial lattice times a Z of Euclidean time
# ══════════════════════════════════════════════════════════════════════════
#
# Why NOT a 4D BCC (D4) lattice
# -----------------------------
# The obvious symmetric choice is to treat all four directions alike on the 4D
# body-centred lattice.  The model forbids it.  F291 S1 caps the Cayley graph at
# three spatial generators, and F313 computes the "+1" as the *commutant* of the
# update -- one commuting flow, generated by a single primitive unitary, which is
# precisely NOT a fourth Cayley generator.  A genuine 4D BCC would make Euclidean
# time a fourth hop direction and contradict the model's own structure.  So the
# 3+1D lattice here is the BCC spatial graph (4 <111> link axes) times an integer
# time, and it is ANISOTROPIC by construction.
#
# Geometry
# --------
#   * spatial links: one matrix field per <111> axis, 4 of them, the same
#     ``BCC_LINK_AXES`` storage and the same reversal identity as the 3D code;
#   * temporal links: one matrix field along +t;
#   * plaquettes: the 6 minimal 4-bond rhombi (|d1 x d2| = 2 sqrt 2) at each
#     time slice, plus 4 mixed space-time RECTANGLES, one per spatial axis,
#     of area |d| a_t = sqrt 3 a_t.  Ten plaquettes per site, not the
#     hypercubic six.
#
# Anisotropy, stated as open
# --------------------------
# ``beta_s`` and ``beta_t`` are independent arguments and ``xi = a_s/a_t``
# is NOT derived here.  F313's primitivity result (no local half-tick) says
# a_t is fixed by the rule rather than tunable, and c_lat = 1/sqrt3 is the
# obvious place a derived xi would come from -- but that argument is not made
# in this module and no default encodes it.  ``beta_t = beta_s`` is a
# convention, flagged, not a result.
#
# Why a local heat-bath is valid on a rhombic lattice
# ---------------------------------------------------
# A local update needs a sublattice on which no two updated links share a
# plaquette.  A rhombus with sides {a, e} carries exactly two a-bonds, stored at
# sites differing by the single hop e -- and the BCC nearest-neighbour graph is
# BIPARTITE (a hop in {+-1}^3 maps all-even coordinates to all-odd), so those two
# sites are always in opposite parity classes.  The mixed rectangle carries two
# a-bonds at the same spatial site one tick apart, which t-parity separates.
# Hence (spatial parity) x (time parity) is a valid 4-colouring, and that is what
# ``heatbath_sweep_4d`` uses.  This is a property of the BCC graph, not an
# assumption: ``check_bcc_gauge_mc`` measures it as the over-relaxation
# action-invariance leg.

TIME_AXIS = 3
_T_HOP = (0, 0, 0, 1)

_AXIS_INDEX = {tuple(a): i for i, a in enumerate(BCC_LINK_AXES)}


def _h4(d3, dt=0):
    """A 4-vector hop from a 3-vector spatial hop and a time step."""
    return (int(d3[0]), int(d3[1]), int(d3[2]), int(dt))


def _vadd(u, v):
    return tuple(int(a) + int(b) for a, b in zip(u, v))


def _vneg(u):
    return tuple(-int(a) for a in u)


def shift4(A: np.ndarray, off) -> np.ndarray:
    """``B[x] = A[x + off]`` on the 4D (space x Euclidean time) torus."""
    if all(c == 0 for c in off):
        return A
    return np.roll(A, tuple(-int(c) for c in off), axis=(0, 1, 2, 3))


def _stored(h):
    """Resolve a 4-vector hop to the field that stores it.

    Returns ``(kind, idx, sign)`` with ``kind in {'s','t'}``.  ``sign = -1``
    means the hop is the reverse of the stored axis, so the field enters
    daggered via ``U_{-d}(x) = U_d(x - d)^dag``.
    """
    if h[3] != 0:
        if any(c != 0 for c in h[:3]):
            raise ValueError(f"mixed hop {h} is not a single lattice bond")
        return ('t', 0, 1 if h[3] > 0 else -1)
    d3 = h[:3]
    if d3 in _AXIS_INDEX:
        return ('s', _AXIS_INDEX[d3], 1)
    nd = _vneg(d3)
    if nd in _AXIS_INDEX:
        return ('s', _AXIS_INDEX[nd], -1)
    raise ValueError(f"{d3} is not a BCC nearest-neighbour hop")


def _field_of(links, kind, idx):
    return links['s'][idx] if kind == 's' else links['t']


def _leg_field(links, h, off) -> np.ndarray:
    """The link field for hop ``h`` based at ``x + off``.

    Forward hops read the stored field directly; reverse hops apply the
    reversal identity, so the eight spatial directions are never stored
    independently and ``link_reversal_residual`` cannot be violated by
    construction on this layout.
    """
    kind, idx, sign = _stored(h)
    F = _field_of(links, kind, idx)
    if sign > 0:
        return shift4(F, off)
    if links.get('_bad_reverse', False):
        # Declared control: drop the ``- d`` of ``U_{-d}(x) = U_d(x - d)^dag``.
        # Everything stays in SU(N) -- the fields are untouched and a product of
        # unitaries is unitary -- so no unitarity leg can see it.  What breaks is
        # gauge invariance and the staple identity, which is the point: this is
        # the realistic off-by-one, and those are the legs that must catch it.
        return _dagger(shift4(F, off))
    return _dagger(shift4(F, _vadd(off, h)))


def _reverse_leg(h, off):
    """The same bond traversed backwards: ``U_h(x+off)^dag = U_{-h}(x+off+h)``."""
    return (_vneg(h), _vadd(off, h))


# ── the ten loops ─────────────────────────────────────────────────────────

def _build_loops():
    """The 6 spatial rhombi and 4 mixed rectangles, as ordered leg lists.

    A loop is ``(label, kind, legs)`` with ``kind in {'s','t'}`` naming the
    coupling it carries (``beta_s`` for a rhombus, ``beta_t`` for a mixed
    rectangle) and ``legs`` a list of ``(hop, offset)`` pairs relative to the
    loop's base site.
    """
    loops = []
    for lab, (d1, d2) in zip(BCC_PLAQ_LABELS, BCC_PLAQUETTES):
        e1, e2 = _h4(d1), _h4(d2)
        legs = [(e1, (0, 0, 0, 0)),
                (e2, e1),
                (_vneg(e1), _vadd(e1, e2)),
                (_vneg(e2), e2)]
        loops.append((lab, 's', legs))
    for i, a in enumerate(BCC_LINK_AXES):
        ha = _h4(a)
        legs = [(ha, (0, 0, 0, 0)),
                (_T_HOP, ha),
                (_vneg(ha), _vadd(ha, _T_HOP)),
                (_vneg(_T_HOP), _T_HOP)]
        loops.append((f'st{i}', 't', legs))
    return tuple(loops)


BCC4_LOOPS = _build_loops()
#: 6 spatial rhombi + 4 mixed space-time rectangles.
BCC4_N_LOOPS = len(BCC4_LOOPS)
#: Area of the mixed rectangle in units of ``a_s a_t``: |d| = sqrt 3.
BCC4_MIXED_AREA = math.sqrt(3.0)


def _build_staple_terms():
    """Enumerate, per stored link field, every plaquette that contains it.

    For each loop and each of its four slots, rotate the cycle so the target
    link is leftmost -- taking the REVERSED loop when the slot is a reverse hop,
    since ``Re tr P = Re tr P^dag`` -- and record the remaining three legs
    re-based on the stored link's own site.  Each of the 4+1 fields collects
    exactly six terms (24 rhombus slots over 4 axes, 16 mixed slots over 4 axes
    and 1 time field), which is the exact bond-counting identity
    ``6 loops/site x 4 bonds/loop = 5 fields/site x n``: the residual of the
    whole construction is measured, not asserted, by
    :func:`staple_identity_residual`.
    """
    terms = {}
    for lab, bkind, legs in BCC4_LOOPS:
        for k in range(4):
            h_k, off_k = legs[k]
            kind, idx, sign = _stored(h_k)
            if sign > 0:
                base = _vneg(off_k)
                order = [(k + 1) % 4, (k + 2) % 4, (k + 3) % 4]
                spec = [(legs[j][0], _vadd(legs[j][1], base)) for j in order]
            else:
                base = _vneg(_vadd(off_k, h_k))
                order = [(k - 1) % 4, (k - 2) % 4, (k - 3) % 4]
                spec = []
                for j in order:
                    rh, roff = _reverse_leg(*legs[j])
                    spec.append((rh, _vadd(roff, base)))
            terms.setdefault((kind, idx), []).append((bkind, lab, spec))
    return {key: tuple(val) for key, val in terms.items()}


BCC4_STAPLE_TERMS = _build_staple_terms()


# ── configurations ────────────────────────────────────────────────────────

def _site_masks(shape4):
    """``(all_sites, even, odd)`` boolean masks on the 4D grid.

    A BCC site is a cubic point whose three coordinates share a parity; the
    two parity classes are the bipartition of the nearest-neighbour graph.
    """
    Lx, Ly, Lz, Lt = shape4
    gx, gy, gz = np.indices((Lx, Ly, Lz))
    even3 = ((gx % 2 == 0) & (gy % 2 == 0) & (gz % 2 == 0))
    odd3 = ((gx % 2 == 1) & (gy % 2 == 1) & (gz % 2 == 1))
    even = np.broadcast_to(even3[..., None], shape4)
    odd = np.broadcast_to(odd3[..., None], shape4)
    return (even | odd), even.copy(), odd.copy()


def cold_links_4d(shape4, N=3):
    """Ordered start: every link the identity."""
    eye = np.broadcast_to(np.eye(N, dtype=complex), tuple(shape4) + (N, N))
    return {'s': [eye.copy() for _ in BCC_LINK_AXES], 't': eye.copy(), 'N': N}


def hot_links_4d(shape4, N=3, channel='bcc_gauge_mc_init'):
    """Disordered start: every link Haar-random in SU(N).

    ``channel`` names an independent RNG stream (D8), so adding this sampler
    does not perturb the numbers any other channel sees.
    """
    gen = _rng.for_channel(channel)
    shape4 = tuple(shape4)

    def _haar():
        Z = (gen.normal(size=shape4 + (N, N))
             + 1j * gen.normal(size=shape4 + (N, N))) / np.sqrt(2.0)
        Q, R = np.linalg.qr(Z)
        ph = np.diagonal(R, axis1=-2, axis2=-1)
        Q = Q * (ph / np.abs(ph))[..., None, :]
        det = np.linalg.det(Q)
        return Q * (det ** (-1.0 / N))[..., None, None]

    return {'s': [_haar() for _ in BCC_LINK_AXES], 't': _haar(), 'N': N}


def gauge_transform_4d(links, channel='bcc_gauge_omega'):
    """Apply a random SU(N) gauge rotation: ``U_d(x) -> W(x) U_d(x) W(x+d)^dag``.

    Every closed loop is invariant, so this is the sharpest available test that
    the link bookkeeping -- in particular the reversal identity for the four
    backward hops -- is right: a product of unitaries stays unitary however the
    shifts are mangled, but it stops being a holonomy the moment one shift is
    wrong.
    """
    N = links['N']
    shape4 = links['t'].shape[:4]
    gen = _rng.for_channel(channel)
    Z = (gen.normal(size=tuple(shape4) + (N, N))
         + 1j * gen.normal(size=tuple(shape4) + (N, N))) / np.sqrt(2.0)
    W, R = np.linalg.qr(Z)
    ph = np.diagonal(R, axis1=-2, axis2=-1)
    W = W * (ph / np.abs(ph))[..., None, :]
    det = np.linalg.det(W)
    W = W * (det ** (-1.0 / N))[..., None, None]
    out = {'N': N, 's': [], 't': None}
    for i, a in enumerate(BCC_LINK_AXES):
        Wf = shift4(W, _h4(a))
        out['s'].append(_matmul(_matmul(W, links['s'][i]), _dagger(Wf)))
    Wt = shift4(W, _T_HOP)
    out['t'] = _matmul(_matmul(W, links['t']), _dagger(Wt))
    if links.get('_bad_reverse', False):
        out['_bad_reverse'] = True
    return out


def unitarity_residual_4d(links) -> float:
    """``max || U U^dag - I ||_inf`` over the 5 stored fields, sites only."""
    N = links['N']
    sites, _, _ = _site_masks(links['t'].shape[:4])
    eye = np.eye(N, dtype=complex)
    worst = 0.0
    for F in list(links['s']) + [links['t']]:
        M = _matmul(F[sites], _dagger(F[sites])) - eye
        worst = max(worst, float(np.abs(M).max()))
    return worst


# ── plaquettes and action ─────────────────────────────────────────────────

def plaquette_4d(links, label) -> np.ndarray:
    """The holonomy of one named loop, as a matrix field on the 4D grid."""
    for lab, _bk, legs in BCC4_LOOPS:
        if lab == label:
            P = None
            for h, off in legs:
                A = _leg_field(links, h, off)
                P = A if P is None else _matmul(P, A)
            return P
    raise KeyError(label)


def plaquette_traces_4d(links) -> dict:
    """``{label: mean over sites of Re tr P / N}`` for all ten loops."""
    N = links['N']
    sites, _, _ = _site_masks(links['t'].shape[:4])
    out = {}
    for lab, _bk, legs in BCC4_LOOPS:
        P = plaquette_4d(links, lab)
        tr = np.real(np.trace(P, axis1=-2, axis2=-1)) / N
        out[lab] = float(tr[sites].mean())
    return out


def mean_plaquette_4d(links) -> dict:
    """Mean ``Re tr P / N`` split by loop class."""
    tr = plaquette_traces_4d(links)
    sp = [tr[lab] for lab, bk, _legs in BCC4_LOOPS if bk == 's']
    tm = [tr[lab] for lab, bk, _legs in BCC4_LOOPS if bk == 't']
    return {'spatial': float(np.mean(sp)), 'temporal': float(np.mean(tm)),
            'all': float(np.mean(sp + tm)), 'by_loop': tr}


def wilson_action_4d(links, beta_s: float, beta_t: float) -> float:
    """``S = beta_s sum_rhombi (1 - Re tr P/N) + beta_t sum_rect (1 - Re tr P/N)``.

    Summed over genuine BCC sites only.  The two couplings are independent:
    see the anisotropy note at the head of this section.
    """
    N = links['N']
    sites, _, _ = _site_masks(links['t'].shape[:4])
    total = 0.0
    for lab, bk, _legs in BCC4_LOOPS:
        P = plaquette_4d(links, lab)
        dens = 1.0 - np.real(np.trace(P, axis1=-2, axis2=-1)) / N
        beta = beta_s if bk == 's' else beta_t
        total += beta * float(dens[sites].sum())
    return total


def staple_sum(links, kind, idx, beta_s: float, beta_t: float,
               include_mixed: bool = True) -> np.ndarray:
    """The beta-weighted staple field for one stored link.

    ``include_mixed=False`` drops the mixed space-time rectangles.  That is
    not an option, it is the declared control: without them the staple is not
    the derivative of the action and :func:`staple_identity_residual` must go
    red.
    """
    A = None
    for bk, _lab, spec in BCC4_STAPLE_TERMS[(kind, idx)]:
        if bk == 't' and not include_mixed:
            continue
        beta = beta_s if bk == 's' else beta_t
        M = None
        for h, off in spec:
            L = _leg_field(links, h, off)
            M = L if M is None else _matmul(M, L)
        M = beta * M
        A = M if A is None else A + M
    if A is None:
        A = np.zeros_like(_field_of(links, kind, idx))
    return A


def staple_identity_residual(links, beta_s: float, beta_t: float,
                             include_mixed: bool = True) -> float:
    """Relative residual of ``sum_links Re tr(U A) == 4 sum_loops beta Re tr P``.

    Every loop has four bonds, so summing ``Re tr(U A)`` over all five stored
    fields counts each plaquette exactly four times.  This is an exact
    algebraic identity of the staple construction and is the single check that
    the 24-slot rhombus enumeration, the reversal identity and the reversed-loop
    handling of backward hops are all correct together.  A wrong staple fails
    it at O(1); nothing else in this module tests the enumeration.
    """
    N = links['N']
    sites, _, _ = _site_masks(links['t'].shape[:4])
    lhs = 0.0
    for kind, idx in [('s', i) for i in range(len(BCC_LINK_AXES))] + [('t', 0)]:
        U = _field_of(links, kind, idx)
        A = staple_sum(links, kind, idx, beta_s, beta_t,
                       include_mixed=include_mixed)
        W = _matmul(U, A)
        lhs += float(np.real(np.trace(W, axis1=-2, axis2=-1))[sites].sum())
    rhs = 0.0
    for lab, bk, _legs in BCC4_LOOPS:
        # The right-hand side is ALWAYS the full action.  Dropping the mixed
        # loops here too would make the control's own identity self-consistent
        # and the control would pass -- which is the defect class CLAUDE.md's
        # V-004 rule exists to prevent.
        beta = beta_s if bk == 's' else beta_t
        P = plaquette_4d(links, lab)
        tr = np.real(np.trace(P, axis1=-2, axis2=-1))
        rhs += beta * float(tr[sites].sum())
    rhs *= 4.0
    scale = max(abs(lhs), abs(rhs), 1.0)
    return abs(lhs - rhs) / scale


# ── Cabibbo-Marinari heat-bath, general N ─────────────────────────────────

def _su2_subgroups(N):
    return tuple((i, j) for i in range(N) for j in range(i + 1, N))


def _quat_to_mat(q0, q1, q2, q3):
    """SU(2) matrix ``q0 I + i(q1 s1 + q2 s2 + q3 s3)``, batched."""
    M = np.empty(np.shape(q0) + (2, 2), dtype=complex)
    M[..., 0, 0] = q0 + 1j * q3
    M[..., 0, 1] = q2 + 1j * q1
    M[..., 1, 0] = -q2 + 1j * q1
    M[..., 1, 1] = q0 - 1j * q3
    return M


def _su2_from_block(w):
    """Project 2x2 blocks onto SU(2): return ``(V2, k)`` with ``k >= 0``.

    Same quaternion convention as the hypercubic fork
    (``forks/gauge/lgt_fork_A_mc._su2_from_block``) so the two samplers can be
    compared directly rather than by eye.
    """
    a0 = 0.5 * (w[..., 0, 0].real + w[..., 1, 1].real)
    a1 = 0.5 * (w[..., 0, 1].imag + w[..., 1, 0].imag)
    a2 = 0.5 * (w[..., 0, 1].real - w[..., 1, 0].real)
    a3 = 0.5 * (w[..., 0, 0].imag - w[..., 1, 1].imag)
    k = np.sqrt(a0 * a0 + a1 * a1 + a2 * a2 + a3 * a3)
    # A vanishing quaternion means the block carries NO constraint (beta = 0, or
    # a staple that has been emptied).  The SU(2) projection is then undefined
    # and the right fallback is the IDENTITY, not the zero matrix: returning
    # zeros propagates a singular link into the reunitarisation and turns a
    # legitimate limit -- and any control that empties a staple -- into a crash
    # instead of a red check.
    live = k > 1e-15
    ksafe = np.where(live, k, 1.0)
    V2 = _quat_to_mat(np.where(live, a0 / ksafe, 1.0),
                      np.where(live, a1 / ksafe, 0.0),
                      np.where(live, a2 / ksafe, 0.0),
                      np.where(live, a3 / ksafe, 0.0))
    return V2, k


def _creutz_a0(xi, gen):
    """Sample ``a0 ~ sqrt(1-a0^2) exp(xi a0)`` on [-1,1], vectorised."""
    a0 = np.empty(np.shape(xi))
    todo = np.ones(np.shape(xi), dtype=bool)
    while todo.any():
        x = xi[todo]
        u = gen.random(x.shape)
        prop = 1.0 + np.log(u + (1.0 - u) * np.exp(-2.0 * x)) / x
        acc = gen.random(x.shape) < np.sqrt(np.maximum(1.0 - prop * prop, 0.0))
        sel = np.zeros_like(todo)
        sel[todo] = acc
        a0[sel] = prop[acc]
        todo[sel] = False
    return a0


def _sample_su2_heatbath(V2, k, N, gen):
    """Heat-bath subgroup matrix.  ``xi = 2 k / N``.

    beta is already folded into the staple by :func:`staple_sum`, so the
    effective coupling carries no separate beta: for a weight
    ``exp((1/N) Re tr(U A))`` and ``Re tr(X2 w) = 2 k a0``, the scalar
    distribution is ``sqrt(1-a0^2) exp((2k/N) a0)``.
    """
    xi = np.maximum((2.0 / N) * k, 1e-12)
    a0 = _creutz_a0(xi, gen)
    nrm = np.sqrt(np.maximum(1.0 - a0 * a0, 0.0))
    cos_t = 2.0 * gen.random(a0.shape) - 1.0
    sin_t = np.sqrt(np.maximum(1.0 - cos_t * cos_t, 0.0))
    phi = 2.0 * np.pi * gen.random(a0.shape)
    X2 = _quat_to_mat(a0, nrm * sin_t * np.cos(phi),
                      nrm * sin_t * np.sin(phi), nrm * cos_t)
    return _matmul(X2, _dagger(V2))


def _su2_overrelax(V2):
    """Microcanonical reflection ``R2 = (V2^dag)^2`` -- preserves the action."""
    Vd = _dagger(V2)
    return _matmul(Vd, Vd)


def _embed_su2(R2, i, j, N):
    E = np.broadcast_to(np.eye(N, dtype=complex),
                        R2.shape[:-2] + (N, N)).copy()
    E[..., i, i] = R2[..., 0, 0]
    E[..., i, j] = R2[..., 0, 1]
    E[..., j, i] = R2[..., 1, 0]
    E[..., j, j] = R2[..., 1, 1]
    return E


def _reunitarise(U, N):
    """Gram-Schmidt on rows, then divide out the determinant phase."""
    V = U.copy()
    for r in range(N):
        for s in range(r):
            ov = np.sum(np.conj(V[..., s, :]) * V[..., r, :], axis=-1)
            V[..., r, :] -= ov[..., None] * V[..., s, :]
        nr = np.sqrt(np.sum(np.abs(V[..., r, :]) ** 2, axis=-1))
        V[..., r, :] /= nr[..., None]
    det = np.linalg.det(V)
    return V * (det ** (-1.0 / N))[..., None, None]


def _update_field(links, kind, idx, beta_s, beta_t, gen, mode,
                  include_mixed=True, skip_checkerboard=False):
    """One heat-bath or over-relaxation pass over a single stored field.

    The staple is recomputed per colour class.  It must be: a staple excludes
    its own link but contains the same-axis link one hop away, which lies in
    the other class, so reusing a staple across classes would sample the wrong
    distribution.  ``skip_checkerboard=True`` does exactly that and is the
    declared control.
    """
    N = links['N']
    _all, even, odd = _site_masks(links['t'].shape[:4])
    teven = np.zeros_like(even)
    teven[..., ::2] = True
    if skip_checkerboard:
        classes = [(even | odd)]
    else:
        classes = [(even & teven), (even & ~teven),
                   (odd & teven), (odd & ~teven)]
    subs = _su2_subgroups(N)
    for cls in classes:
        if not cls.any():
            continue
        A = staple_sum(links, kind, idx, beta_s, beta_t,
                       include_mixed=include_mixed)[cls]
        for (i, j) in subs:
            F = _field_of(links, kind, idx)
            Up = F[cls]
            W = _matmul(Up, A)
            w = W[:, [i, j], :][:, :, [i, j]]
            V2, k = _su2_from_block(w)
            R2 = (_sample_su2_heatbath(V2, k, N, gen) if mode == 'heatbath'
                  else _su2_overrelax(V2))
            E = _embed_su2(R2, i, j, N)
            F[cls] = _matmul(E, Up)
    F = _field_of(links, kind, idx)
    Fn = _reunitarise(F, N)
    if kind == 's':
        links['s'][idx] = Fn
    else:
        links['t'] = Fn
    return links


def sweep_4d(links, beta_s: float, beta_t: float, gen, n_or: int = 0,
             include_mixed: bool = True, skip_checkerboard: bool = False,
             mode: str = 'heatbath'):
    """One full lattice sweep over the 4 spatial axes and the time field."""
    fields = [('s', i) for i in range(len(BCC_LINK_AXES))] + [('t', 0)]
    for kind, idx in fields:
        _update_field(links, kind, idx, beta_s, beta_t, gen, mode,
                      include_mixed=include_mixed,
                      skip_checkerboard=skip_checkerboard)
        for _ in range(n_or):
            _update_field(links, kind, idx, beta_s, beta_t, gen, 'overrelax',
                          include_mixed=include_mixed,
                          skip_checkerboard=skip_checkerboard)
    return links


def thermalise_4d(links, beta_s: float, beta_t: float, n_sweeps: int,
                  n_or: int = 1, channel='bcc_gauge_mc', record=False):
    """Run ``n_sweeps`` heat-bath sweeps; optionally record the plaquette history."""
    gen = _rng.for_channel(channel)
    hist = []
    for _ in range(n_sweeps):
        sweep_4d(links, beta_s, beta_t, gen, n_or=n_or)
        if record:
            hist.append(mean_plaquette_4d(links)['all'])
    return (links, hist) if record else links


# ── Wilson loops, Creutz ratios, Polyakov loop ────────────────────────────

def _transporter(links, h, n, off0=(0, 0, 0, 0)):
    """Straight product of ``n`` links along hop ``h``, based at ``x + off0``.

    Successive <111> hops preserve coordinate parity, so a straight spatial
    transporter never leaves the BCC site set -- which is what makes an
    R x T rectangle a closed loop on this lattice at all.
    """
    M = None
    off = tuple(off0)
    for _ in range(n):
        L = _leg_field(links, h, off)
        M = L if M is None else _matmul(M, L)
        off = _vadd(off, h)
    return M, off


def wilson_loop_rt(links, axis_idx: int, R: int, T: int) -> float:
    """Mean ``Re tr W(R,T) / N`` with R along a <111> axis and T along time.

    Path: R spatial hops, T time steps, R hops back, T steps back.  At
    ``R = T = 1`` this is exactly the mixed rectangle of the action, which is
    the consistency leg ``W1a``.
    """
    N = links['N']
    ha = _h4(BCC_LINK_AXES[axis_idx])
    Sr, end_s = _transporter(links, ha, R)
    Tt_far, _ = _transporter(links, _T_HOP, T, off0=end_s)
    Sr_top, _ = _transporter(links, ha, R,
                             off0=tuple(c * T for c in _T_HOP))
    Tt_base, _ = _transporter(links, _T_HOP, T)
    W = _matmul(_matmul(Sr, Tt_far), _matmul(_dagger(Sr_top), _dagger(Tt_base)))
    sites, _, _ = _site_masks(links['t'].shape[:4])
    tr = np.real(np.trace(W, axis1=-2, axis2=-1)) / N
    return float(tr[sites].mean())


def wilson_loop_table(links, r_max: int, t_max: int) -> dict:
    """``{(R,T): mean Re tr W/N}`` averaged over the 4 spatial axes."""
    out = {}
    for R in range(1, r_max + 1):
        for T in range(1, t_max + 1):
            vals = [wilson_loop_rt(links, i, R, T)
                    for i in range(len(BCC_LINK_AXES))]
            out[(R, T)] = float(np.mean(vals))
    return out


def creutz_ratios(table: dict) -> dict:
    """``chi(R,T) = -ln[ W(R,T) W(R-1,T-1) / (W(R-1,T) W(R,T-1)) ]``.

    The area-law estimator of the string tension in units of ``a_s a_t``: for
    ``W ~ exp(-sigma R T)`` every perimeter and corner term cancels and
    ``chi -> sigma``.
    """
    out = {}
    for (R, T) in table:
        if R < 2 or T < 2:
            continue
        num = table[(R, T)] * table[(R - 1, T - 1)]
        den = table[(R - 1, T)] * table[(R, T - 1)]
        if num <= 0.0 or den <= 0.0:
            continue
        out[(R, T)] = float(-np.log(num / den))
    return out


def polyakov_loop_4d(links) -> complex:
    """Mean over spatial sites of ``tr(prod_t U_t)/N`` -- the order parameter."""
    N = links['N']
    Lt = links['t'].shape[3]
    P, _ = _transporter(links, _T_HOP, Lt)
    sites, _, _ = _site_masks(links['t'].shape[:4])
    tr = np.trace(P, axis1=-2, axis2=-1) / N
    return complex(tr[sites].mean())


# ══════════════════════════════════════════════════════════════════════════
#  gate entry
# ══════════════════════════════════════════════════════════════════════════

def check_bcc_gauge_mc(L: int = 4, Lt: int = 4, N: int = 2,
                       beta_s: float = 1.7, beta_t: float = 1.7,
                       include_mixed: bool = True,
                       skip_checkerboard: bool = False,
                       bad_reverse_shift: bool = False,
                       hypercubic_anisotropy: bool = False,
                       unsymmetrised_reps: bool = False,
                       iso_L: int = 8, iso_g: float = 4.0e-3) -> dict:
    """Gate-tier legs for the 3+1D BCC sampler and its Wilson loops.

    Deterministic and fast by construction: every leg is either an exact
    algebraic identity of the construction or a limit that does not need
    statistics.  The area law itself is NOT here -- it needs production
    statistics and lives in the battery record ``run-bcc-confinement-d4``.

    Control parameters, each reddening a disjoint leg set:

    ``include_mixed=False``     staple drops the mixed space-time rectangles
                               while the action keeps them, so the staple is no
                               longer the derivative of the action -> S1a/S1b.
    ``skip_checkerboard=True``  one colour class instead of four, so a staple is
                               reused for links that share a plaquette ->
                               over-relaxation stops preserving the action, O1a.
    ``bad_reverse_shift=True``  the ``- d`` of ``U_{-d}(x) = U_d(x-d)^dag`` is
                               dropped.  Nothing leaves SU(N), so no unitarity
                               leg can see it; gauge invariance and the staple
                               identity must -> G1a/G1b/S1a/S1b/O1a.
    ``hypercubic_anisotropy``   predict ``beta_t/beta_s = xi^2``, the textbook
                               hypercubic relation, instead of the BCC
                               ``4 lambda^2/a_t^2 = (4/3) xi^2`` -> X1c/X1d.
                               This is the mistake the derivation exists to
                               prevent and the control is the 4/3 itself.
    ``unsymmetrised_reps``      build the higher reps as the raw tensor power
                               (``chi = (Tr W)^k``) instead of projecting onto
                               the symmetric subspace -> K1a.  Also the realistic
                               mistake, and the reason the explicit-matrix
                               cross-check is here at all.

    Note on what is NOT a control: ``c_lat`` cannot be one.  Changing it moves
    ``a_t`` and the prediction together, because the derivation is
    self-consistent at any ``c_lat`` -- the falsifiable content is the relation
    ``beta_t/beta_s = 4 lambda^2/a_t^2``, not the value of ``c_lat`` fed into it.
    """
    # ── structural guards ─────────────────────────────────────────────────
    # These RAISE rather than returning a red check, because a malformed input
    # or a malformed loop table makes every leg below meaningless rather than
    # false.  None of the three declared controls trips one, deliberately: a
    # control has to produce a red CHECK, and an exception is not a negative
    # control -- it shows the driver cannot reach the perturbed point at all.
    assert L % 2 == 0, (
        f"L={L} must be even: the update checkerboard is the parity "
        f"bipartition of the BCC nearest-neighbour graph and an odd extent "
        f"does not close under a <111> hop")
    assert Lt >= 2, f"Lt={Lt} must be >= 2 for a mixed space-time rectangle"
    assert N >= 2, f"N={N} must be >= 2 for a nonabelian SU(N) link"
    assert len(BCC4_STAPLE_TERMS) == len(BCC_LINK_AXES) + 1, (
        f"staple table covers {len(BCC4_STAPLE_TERMS)} fields, expected "
        f"{len(BCC_LINK_AXES) + 1} (4 spatial axes + 1 time)")
    for _lab, _bk, _legs in BCC4_LOOPS:
        _net = (0, 0, 0, 0)
        for _h, _o in _legs:
            _net = _vadd(_net, _h)
        assert _net == (0, 0, 0, 0), (
            f"loop {_lab} does not close: net hop {_net}")

    checks = []

    def add(name, ok, value, note=""):
        checks.append({"name": name, "ok": bool(ok), "value": value,
                       "note": note})

    shape4 = (L, L, L, Lt)
    eps = 1e-12

    # ── C: cold-start limits ──────────────────────────────────────────────
    cold = cold_links_4d(shape4, N=N)
    tr_cold = plaquette_traces_4d(cold)
    worst_cold = max(abs(v - 1.0) for v in tr_cold.values())
    add("C1a", worst_cold < eps, worst_cold,
        "every one of the 10 loops is the identity on the ordered start")
    s_cold = wilson_action_4d(cold, beta_s, beta_t)
    add("C1b", abs(s_cold) < eps, abs(s_cold),
        "Wilson action vanishes identically at zero field strength")
    add("C1c", BCC4_N_LOOPS == 10, BCC4_N_LOOPS,
        "6 minimal rhombi + 4 mixed rectangles; NOT the hypercubic 6")

    # ── H: holonomy structure ─────────────────────────────────────────────
    hot = hot_links_4d(shape4, N=N, channel='bcc_gauge_gate_init')
    if bad_reverse_shift:
        hot['_bad_reverse'] = True

    u_res = unitarity_residual_4d(hot)
    add("H1a", u_res < 1e-11, u_res,
        "all 5 stored fields are in SU(N) on the disordered start")
    worst_holo = 0.0
    eye = np.eye(N, dtype=complex)
    sites, _, _ = _site_masks(shape4)
    for lab, _bk, _legs in BCC4_LOOPS:
        P = plaquette_4d(hot, lab)
        Ps = P[sites]
        dev = np.abs(_matmul(Ps, _dagger(Ps)) - eye).max()
        worst_holo = max(worst_holo, float(dev))
    add("H1b", worst_holo < 1e-11, worst_holo,
        "every loop is a unitary holonomy, so the reversal identity closes")

    # ── G: gauge invariance ───────────────────────────────────────────────
    rot = gauge_transform_4d(hot, channel='bcc_gauge_gate_omega')
    tr_a, tr_b = plaquette_traces_4d(hot), plaquette_traces_4d(rot)
    d_plaq = max(abs(tr_a[k] - tr_b[k]) for k in tr_a)
    add("G1a", d_plaq < 1e-11, d_plaq,
        "all 10 plaquette traces are invariant under a random SU(N) gauge "
        "rotation -- the action is a function of the connection, not the gauge")
    t_a, t_b = wilson_loop_table(hot, 2, 2), wilson_loop_table(rot, 2, 2)
    d_loop = max(abs(t_a[k] - t_b[k]) for k in t_a)
    add("G1b", d_loop < 1e-11, d_loop,
        "every R x T Wilson loop is gauge invariant, so it measures a "
        "holonomy and not a gauge artifact")

    # ── S: the staple IS the derivative of the action ─────────────────────
    r_iso = staple_identity_residual(hot, beta_s, beta_s,
                                     include_mixed=include_mixed)
    add("S1a", r_iso < 1e-12, r_iso,
        "sum_links Re tr(U A) == 4 sum_loops beta Re tr P, isotropic couplings")
    r_aniso = staple_identity_residual(hot, beta_s, 2.5 * beta_s,
                                       include_mixed=include_mixed)
    add("S1b", r_aniso < 1e-12, r_aniso,
        "same identity with beta_t != beta_s -- the anisotropy is carried "
        "correctly through the 24-slot enumeration")
    split = {}
    for key, terms in BCC4_STAPLE_TERMS.items():
        split[key] = (sum(1 for bk, _l, _s in terms if bk == 's'),
                      sum(1 for bk, _l, _s in terms if bk == 't'))
    spatial_ok = all(split[('s', i)] == (6, 2)
                     for i in range(len(BCC_LINK_AXES)))
    add("S1c", spatial_ok and split[('t', 0)] == (0, 8),
        {f"{k[0]}{k[1]}": v for k, v in split.items()},
        "exact bond counting: a spatial axis sits in 6 rhombi (6 orientations "
        "x 4 slots / 4 axes) and 2 mixed rectangles (its own, twice); the time "
        "field sits in 8 (4 rectangles x 2 temporal slots) and in no rhombus. "
        "40 slots over 5 fields, and the split -- not just the total -- is what "
        "catches a mis-enumeration")

    # ── B: the bipartition that makes a local update legal ────────────────
    _all, even, odd = _site_masks(shape4)
    n_sites = int(_all.sum())
    add("B1a", n_sites == (L ** 3 // 4) * Lt, n_sites,
        "genuine BCC sites are 1/4 of the cubic array (index 4 in Z^3)")
    cross = True
    for a in BCC_LINK_AXES:
        shifted = shift4(even, _h4(a))
        if bool((shifted & even).any()):
            cross = False
    add("B1b", cross, cross,
        "every <111> hop maps the even class into the odd class -- the BCC "
        "nearest-neighbour graph is bipartite, which is what makes the "
        "checkerboard heat-bath valid on a rhombic lattice")

    # ── O: over-relaxation is microcanonical ──────────────────────────────
    gen = _rng.for_channel('bcc_gauge_gate_or')
    orl = {'s': [f.copy() for f in hot['s']], 't': hot['t'].copy(), 'N': N}
    s_before = wilson_action_4d(orl, beta_s, beta_t)
    sweep_4d(orl, beta_s, beta_t, gen, mode='overrelax',
             include_mixed=include_mixed,
             skip_checkerboard=skip_checkerboard)
    s_after = wilson_action_4d(orl, beta_s, beta_t)
    drift = abs(s_after - s_before) / max(abs(s_before), 1.0)
    add("O1a", drift < 1e-9, drift,
        "microcanonical reflection R2 = (V2^dag)^2 leaves the action invariant "
        "-- fails if a staple is reused across links that share a plaquette")

    # ── W: the loop builder agrees with the action ────────────────────────
    w11 = float(np.mean([wilson_loop_rt(hot, i, 1, 1)
                         for i in range(len(BCC_LINK_AXES))]))
    mixed_mean = mean_plaquette_4d(hot)['temporal']
    add("W1a", abs(w11 - mixed_mean) < 1e-12, abs(w11 - mixed_mean),
        "W(1,1) IS the mixed rectangle of the action -- the loop builder and "
        "the action are the same object, not two implementations")
    w_cold = wilson_loop_table(cold, 2, 2)
    add("W1b", all(abs(v - 1.0) < eps for v in w_cold.values()),
        max(abs(v - 1.0) for v in w_cold.values()),
        "all R x T loops are 1 on the ordered start")
    tbl = wilson_loop_table(hot, 2, 2)
    add("W1c", all(abs(v) <= 1.0 + 1e-12 for v in tbl.values()),
        max(abs(v) for v in tbl.values()),
        "|Re tr W / N| <= 1 for every measured loop")

    # ── P: the spatial transporter stays on the lattice ───────────────────
    a0 = BCC_LINK_AXES[0]
    walk_ok = True
    for r in range(1, 5):
        pt = tuple(r * c for c in a0)
        if len({c % 2 for c in pt}) != 1:
            walk_ok = False
    add("P1a", walk_ok, walk_ok,
        "straight <111> walks preserve coordinate parity, so an R x T "
        "rectangle closes on the BCC site set for every R")

    # ── T: translation covariance of the whole construction ───────────────
    # An earlier draft asserted here that two calls to ``rng.for_channel`` with
    # the same name reproduce bitwise.  They do not, and should not: the cache
    # returns ONE generator per consumer, so the second call continues the
    # stream.  The guarantee is "same run seed -> same sequence", which can only
    # be tested by calling ``seed_run`` and clearing every other channel's
    # stream mid-gate.  Replay is checked in the battery runner instead, and the
    # leg is spent on something the gate can prove exactly.
    worst_cov = 0.0
    for v in [(2, 0, 0, 0), (0, 0, 0, 1), _h4(BCC_LINK_AXES[1])]:
        moved = {'N': N, 's': [shift4(f, v) for f in hot['s']],
                 't': shift4(hot['t'], v)}
        if hot.get('_bad_reverse', False):
            moved['_bad_reverse'] = True
        for kind, idx in [('s', 0), ('s', 2), ('t', 0)]:
            A_moved = staple_sum(moved, kind, idx, beta_s, beta_t,
                                 include_mixed=include_mixed)
            A_shift = shift4(staple_sum(hot, kind, idx, beta_s, beta_t,
                                        include_mixed=include_mixed), v)
            worst_cov = max(worst_cov,
                            float(np.abs(A_moved - A_shift).max()))
    add("T1a", worst_cov < 1e-12, worst_cov,
        "the staple construction is translation covariant -- shifting the "
        "configuration shifts the staple by the same vector, for a cubic "
        "translation, a time step and a <111> hop (which swaps the two parity "
        "classes). Catches any indexing error that survives the trace")

    # ── X: the anisotropy, derived ────────────────────────────────────────
    from fractions import Fraction
    ci = bcc_closure_identities()
    add("X1a", ci["normals_close_on_4I"] and ci["axes_close_on_4I"],
        {"sum_m_mT": ci["sum_m_mT"][0], "sum_a_aT": ci["sum_a_aT"][0]},
        "the two closure identities the derivation rests on, over Z and exact: "
        "the 6 <110> rhombus half-normals and the 4 <111> link axes EACH give "
        "4*I. They are independent -- different vector sets, different orbit -- "
        "and the shared constant is why beta_t/beta_s comes out rational")
    der = anisotropy_from_c_lat()
    add("X1b", der["beta_ratio"] == Fraction(4) and der["xi_sq"] == Fraction(3),
        {"beta_ratio": str(der["beta_ratio"]), "xi_sq": str(der["xi_sq"]),
         "xi": der["xi"]},
        "from c_lat^2 = 1/3: beta_t/beta_s = 4 and xi^2 = 3 as exact "
        "Fractions, so xi = 1/c_lat = sqrt3. No fitted content")
    predicted = (float(der["xi_sq"]) if hypercubic_anisotropy
                 else float(der["beta_ratio"]))
    iso1 = weak_field_isotropy(shape4=(iso_L,) * 3 + (iso_L,), g=iso_g, pad=2)
    iso2 = weak_field_isotropy(shape4=(iso_L,) * 3 + (iso_L,), g=iso_g / 2.0,
                               pad=2)
    # measured(g) = ratio - c g^2 exactly (coefficient held to 4 digits over a
    # factor 2 in g), so one Richardson step is exact in the g^2 term.
    extrap = (4.0 * iso2["beta_ratio_measured"]
              - iso1["beta_ratio_measured"]) / 3.0
    r_iso_x = abs(extrap - predicted) / abs(predicted)
    add("X1c", r_iso_x < 1e-8, {"extrapolated": extrap,
                                "predicted": predicted,
                                "residual": r_iso_x},
        "MEASURED: a constant-F abelian configuration gives "
        "S_B/S_E -> 4 as g -> 0, matching 4 lambda^2/a_t^2. The g^2 truncation "
        "has an exact coefficient (residual/g^2 = 1/16 held over a factor 4 in "
        "g), so one Richardson step removes it and the limit is the identity")
    ratio_over_xi2 = (Fraction(1) if hypercubic_anisotropy
                      else der["beta_ratio"] / der["xi_sq"])
    add("X1d", ratio_over_xi2 == Fraction(4, 3), str(ratio_over_xi2),
        "the BCC answer is (4/3) xi^2, NOT the hypercubic xi^2. The 4/3 is "
        "geometric -- the rhombus carries |d1 x d2| = 2 sqrt2 against the mixed "
        "rectangle's |d| = sqrt3 -- and it is what a naive hypercubic "
        "substitution would have got wrong by a third")

    # ── K: F299's d=4 Casimir successor ───────────────────────────────────
    if unsymmetrised_reps:
        cid = {"worst_overall": None, "dimensions_match": False}
        gen_c = _rng.for_channel('bcc_casimir_ctrl')
        worst_u = 0.0
        for _ in range(4):
            Z = (gen_c.normal(size=(3, 3))
                 + 1j * gen_c.normal(size=(3, 3))) / np.sqrt(2.0)
            Q, Rq = np.linalg.qr(Z)
            ph = np.diagonal(Rq)
            Q = Q * (ph / np.abs(ph))[None, :]
            Q = Q * np.linalg.det(Q) ** (-1.0 / 3.0)
            t1 = np.trace(Q)
            # the unsymmetrised tensor power: chi = (Tr W)^k
            worst_u = max(worst_u,
                          float(abs(np.trace(sym_power_rep(Q, 2)) - t1 ** 2)),
                          float(abs(np.trace(sym_power_rep(Q, 3)) - t1 ** 3)))
        cid["worst_overall"] = worst_u
        cid["dimensions_match"] = True
    else:
        cid = character_identity_residual(n_samples=4)
    add("K1a", cid["worst_overall"] is not None and cid["worst_overall"] < 1e-13,
        cid["worst_overall"],
        "F299's three character polynomials verified against EXPLICIT "
        "representation matrices -- Sym^2 and Sym^3 by symmetric-subspace "
        "isometry, the adjoint by Ad(U)_ab = 2 tr(T_a U T_b U^dag). The tree "
        "had only ever checked them against the Jacobi-Trudi determinant that "
        "PRODUCED them, which is self-consistency, not verification")
    add("K1b", cid["dimensions_match"],
        cid.get("explicit_dimensions", "n/a"),
        "the explicit reps come out 6, 8 and 10 dimensional")
    ratios = {lab: casimir_ratio_exact(lab) for lab, _pq in D4_CASIMIR_REPS}
    want = {"3": Fraction(1), "6": Fraction(5, 2), "8": Fraction(9, 4),
            "10": Fraction(9, 2)}
    add("K1c", ratios == want, {k: str(v) for k, v in ratios.items()},
        "C_2(R)/C_F reproduces F299's table exactly over Q from the Dynkin "
        "labels alone -- 1, 5/2, 9/4, 9/2 -- not tabulated")
    ctab = higher_rep_loop_table(cold_links_4d((4, 4, 4, 4), N=3), 2, 2)
    worst_c = max(abs(v - 1.0) for d in ctab.values() for v in d.values())
    add("K1d", worst_c < eps, worst_c,
        "every higher-rep loop is exactly 1 on the ordered start, for all four "
        "reps and all R x T")
    hot3 = hot_links_4d((4, 4, 4, 4), N=3, channel='bcc_casimir_gate')
    rot3 = gauge_transform_4d(hot3, channel='bcc_casimir_gate_omega')
    ta = higher_rep_loop_table(hot3, 2, 2)
    tb = higher_rep_loop_table(rot3, 2, 2)
    d_rep = max(abs(ta[lab][k] - tb[lab][k]) for lab in ta for k in ta[lab])
    add("K1e", d_rep < 1e-11, d_rep,
        "every higher-rep loop is gauge invariant, so chi_R measures a "
        "holonomy class and not a gauge artifact")
    fund_direct = float(np.mean([wilson_loop_rt(hot3, ax, 2, 2)
                                 for ax in range(len(BCC_LINK_AXES))]))
    add("K1f", abs(ta["3"][(2, 2)] - fund_direct) < 1e-12,
        abs(ta["3"][(2, 2)] - fund_direct),
        "the rep-3 entry of the character table equals `wilson_loop_rt` -- the "
        "trace-based path and the matrix-based path are the same object")

    n_pass = sum(1 for c in checks if c["ok"])
    return {
        "checks": checks,
        "n_pass": n_pass,
        "n_total": len(checks),
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
        "anisotropy": {"xi": der["xi"], "xi_sq": str(der["xi_sq"]),
                       "beta_ratio": str(der["beta_ratio"]),
                       "bcc_factor_vs_hypercubic": str(
                           der["beta_ratio"] / der["xi_sq"])},
        "params": {"L": L, "Lt": Lt, "N": N, "beta_s": beta_s,
                   "beta_t": beta_t, "include_mixed": include_mixed,
                   "skip_checkerboard": skip_checkerboard,
                   "bad_reverse_shift": bad_reverse_shift,
                   "hypercubic_anisotropy": hypercubic_anisotropy,
                   "unsymmetrised_reps": unsymmetrised_reps,
                   "iso_L": iso_L, "iso_g": iso_g},
    }


# ══════════════════════════════════════════════════════════════════════════
#  the anisotropy xi = a_s/a_t, derived
# ══════════════════════════════════════════════════════════════════════════
#
# `brisk-eager-creutz` left ``beta_t = beta_s`` as a flagged CONVENTION.  It is
# not free.  Two separate statements are needed and they do different jobs.
#
# 1.  WHAT LICENSES A FIXED a_t.  On an ordinary anisotropic lattice the
#     temporal spacing is a tunable and one takes a_t -> 0.  Here it is not:
#     F313 proves the update A is the FUNDAMENTAL unit of ker(det) and, by the
#     review's blind agent, PRIMITIVE -- there is no local half-tick, so the
#     tick has no root inside the local homogeneous algebra and cannot be
#     refined.  a_t is therefore a fixed quantity to be computed, not a limit.
#     Primitivity does NOT supply its value.
#
# 2.  WHAT FIXES ITS VALUE.  Isotropy of the weak-field limit.  Expanding the
#     two loop classes to O(Phi^2) with a physical step lambda per unit integer
#     coordinate:
#
#       6 rhombi   sum (1 - Re tr P/N)  ->  8 g^2 lambda^4 |B|^2
#       4 mixed    sum (1 - Re tr P/N)  ->  2 g^2 lambda^2 a_t^2 |E|^2
#
#     using the TWO independent closure identities of the BCC geometry --
#     sum_p m_p m_p^T = 4 I over the 6 <110> half-normals (F265) and
#     sum_a a a^T = 4 I over the 4 <111> link axes -- and |f| = |B| from the
#     module's own Phi_p = 2 m_p . f.  Equality of the E^2 and B^2 coefficients
#     is Euclidean isotropy, and gives
#
#       beta_t / beta_s = 4 lambda^2 / a_t^2 .
#
#     The emergent light cone then closes it.  One tick moves amplitude one
#     hop, the hop has length lambda sqrt3, and the emergent signal speed is
#     c_lat (a GROUP velocity, not the raw hop rate), so in units c = 1
#
#       a_t = c_lat * lambda sqrt3   ==>   beta_t/beta_s = 4 / (3 c_lat^2) ,
#       xi := (hop length) / a_t     ==>   xi = 1 / c_lat .
#
#     At the model's c_lat^2 = 1/3 these are  beta_t/beta_s = 4  and
#     xi = sqrt3, both EXACT rationals/surds with no fitted content.
#
# WHAT IS NEW HERE, stated narrowly.  On a hypercubic lattice the standard
# relation is beta_t/beta_s = xi^2.  Here it is (4/3) xi^2 -- the 4/3 is BCC
# geometric content, traceable to the rhombus carrying |d1 x d2| = 2 sqrt2
# against the mixed rectangle's |d| = sqrt3, and it is the reason the naive
# hypercubic substitution would have been wrong by a third.  xi = 1/c_lat
# reproduces F284's ratio r = 1/c_lat = 3^(1/2) by a route that never mentions
# cosmology, which is a consistency check on both rather than a new number.
#
# WHAT IS NOT CLAIMED.  c_lat is an input here, not re-derived.  And isotropy
# of the CLASSICAL weak-field limit is a tree-level matching condition: it
# fixes the bare couplings, and radiative corrections to the anisotropy (the
# Karsch coefficients, in the hypercubic literature) are NOT computed.

def anisotropy_from_c_lat(c_lat_sq=None):
    """The derived anisotropy and coupling ratio.

    ``c_lat_sq`` defaults to the model's own 1/3 as an exact ``Fraction``.
    Returns exact objects where they are exact: ``beta_ratio`` is a
    ``Fraction`` and ``xi_sq`` is a ``Fraction``; ``xi`` is the irrational
    square root and is returned as a float alongside ``xi_sq``.
    """
    from fractions import Fraction
    if c_lat_sq is None:
        c_lat_sq = Fraction(1, 3)
    c_lat_sq = Fraction(c_lat_sq).limit_denominator(10 ** 9)
    hop_sq = Fraction(3)                      # |d|^2 for d in {+-1}^3, lambda = 1
    a_t_sq = c_lat_sq * hop_sq                # a_t = c_lat * lambda sqrt3
    beta_ratio = Fraction(4) / a_t_sq         # 4 lambda^2 / a_t^2
    xi_sq = hop_sq / a_t_sq                   # (hop length / a_t)^2 = 1/c_lat^2
    return {
        "c_lat_sq": c_lat_sq,
        "hop_length_sq": hop_sq,
        "a_t_sq": a_t_sq,
        "beta_ratio": beta_ratio,
        "beta_ratio_float": float(beta_ratio),
        "xi_sq": xi_sq,
        "xi": float(xi_sq) ** 0.5,
        "beta_ratio_over_xi_sq": beta_ratio / xi_sq,
        "hypercubic_would_give": xi_sq,
        "bcc_geometric_factor": beta_ratio / xi_sq,
    }


# ── a constant-field-strength configuration, to MEASURE the expansion ─────

def constant_field_links_4d(shape4, E=(0.0, 0.0, 0.0), B=(0.0, 0.0, 0.0),
                            N=2, g=1.0e-3, a_t=1.0):
    """Abelian constant-$F_{\\mu\\nu}$ configuration on the 3+1D BCC lattice.

    Built from the linear potential ``A_nu(X) = (1/2) X^mu F_mu_nu``, for which
    the midpoint rule is EXACT, so the link phase is
    ``theta(X, H) = (g/2) X^mu F_mu_nu H^nu`` -- the ``H F H`` term drops by
    antisymmetry.  The generator is a single Cartan direction, so the holonomy
    is abelian and the plaquette flux carries no commutator correction; that is
    what makes the O(Phi^2) coefficients readable off the lattice rather than
    inferred.

    NOT periodic -- a constant field strength cannot be, without flux
    quantisation.  Callers must mask to the interior; :func:`interior_mask_4d`
    is provided for that and the flux of a fixed loop shape is
    position-independent, so an interior sample is exact rather than
    approximate.

    Coordinates are physical: ``X = (x1, x2, x3, a_t * t)`` with the spatial
    step lambda = 1, and the hop ``H = (d1, d2, d3, a_t * dt)``.
    """
    Lx, Ly, Lz, Lt = (int(c) for c in shape4)
    F = np.zeros((4, 4))
    Bx, By, Bz = (float(c) for c in B)
    Ex, Ey, Ez = (float(c) for c in E)
    # F_ij = eps_ijk B_k
    F[0, 1], F[1, 0] = Bz, -Bz
    F[2, 0], F[0, 2] = By, -By
    F[1, 2], F[2, 1] = Bx, -Bx
    # F_i4 = E_i
    for i, Ei in enumerate((Ex, Ey, Ez)):
        F[i, 3], F[3, i] = Ei, -Ei

    gx, gy, gz, gt = np.indices((Lx, Ly, Lz, Lt))
    X = [gx.astype(float), gy.astype(float), gz.astype(float),
         a_t * gt.astype(float)]

    # A single Cartan generator, normalised so tr(T^2) = 1/2 as for su(2).
    T = np.zeros((N, N), dtype=complex)
    T[0, 0], T[1, 1] = 0.5, -0.5

    def _phase(H):
        th = np.zeros_like(X[0])
        for mu in range(4):
            for nu in range(4):
                if F[mu, nu] != 0.0 and H[nu] != 0.0:
                    th = th + X[mu] * F[mu, nu] * H[nu]
        return 0.5 * g * th

    def _link(H):
        th = _phase(H)
        # exp(i th T) for a diagonal Cartan T: exact, no series.
        U = np.zeros(th.shape + (N, N), dtype=complex)
        for k in range(N):
            U[..., k, k] = np.exp(1j * th * T[k, k].real)
        return U

    out = {'N': N, 's': [], 't': None}
    for a in BCC_LINK_AXES:
        out['s'].append(_link((float(a[0]), float(a[1]), float(a[2]), 0.0)))
    out['t'] = _link((0.0, 0.0, 0.0, a_t))
    return out


def interior_mask_4d(shape4, pad=2):
    """BCC sites at least ``pad`` away from every torus face, in all 4 axes."""
    sites, _, _ = _site_masks(shape4)
    keep = np.zeros(tuple(shape4), dtype=bool)
    keep[pad:-pad, pad:-pad, pad:-pad, pad:-pad] = True
    return sites & keep


def _class_action_density(links, bkind, mask):
    """Mean ``1 - Re tr P / N`` over one loop class, on ``mask``."""
    N = links['N']
    vals = []
    for lab, bk, _legs in BCC4_LOOPS:
        if bk != bkind:
            continue
        P = plaquette_4d(links, lab)
        dens = 1.0 - np.real(np.trace(P, axis1=-2, axis2=-1)) / N
        vals.append(dens[mask])
    return float(np.mean(np.concatenate([v.ravel() for v in vals])) * len(vals))


def weak_field_isotropy(shape4=(10, 10, 10, 10), N=2, g=1.0e-3,
                        c_lat_sq=None, field=1.0, pad=3, a_t=None):
    """Measure ``beta_t/beta_s`` by demanding the weak-field limit be isotropic.

    Puts a pure magnetic field of magnitude ``field`` on the lattice, then a
    pure electric field of the same magnitude, and reads the ratio of the two
    loop classes' action densities.  Isotropy requires
    ``beta_t/beta_s = S_B / S_E`` at equal field magnitude, and the derivation
    predicts ``4 / (3 c_lat^2)``.

    Returns the measured ratio, the predicted one, and the relative residual.
    """
    from fractions import Fraction
    der = anisotropy_from_c_lat(c_lat_sq)
    if a_t is None:
        a_t = float(der["a_t_sq"]) ** 0.5
    mask = interior_mask_4d(shape4, pad=pad)

    magnetic = constant_field_links_4d(shape4, B=(0.0, 0.0, field), N=N, g=g,
                                       a_t=a_t)
    electric = constant_field_links_4d(shape4, E=(0.0, 0.0, field), N=N, g=g,
                                       a_t=a_t)
    S_B = _class_action_density(magnetic, 's', mask)
    S_E = _class_action_density(electric, 't', mask)
    measured = S_B / S_E if S_E != 0.0 else float('inf')
    predicted = float(der["beta_ratio"])
    return {
        "S_B_spatial_class": S_B,
        "S_E_mixed_class": S_E,
        "beta_ratio_measured": measured,
        "beta_ratio_predicted": predicted,
        "relative_residual": abs(measured - predicted) / abs(predicted),
        "a_t": a_t,
        "xi": der["xi"],
        "c_lat_sq": str(der["c_lat_sq"]),
    }


def bcc_closure_identities():
    """The two ``sum = 4 I`` identities the derivation rests on, over Z.

    Both are exact integer statements and are computed here rather than quoted:
    the 6 <110> rhombus half-normals and the 4 <111> link axes each close on
    ``4 I``.  They are independent -- different vector sets, different orbit --
    and the coincidence of the constant is what makes ``beta_t/beta_s`` come out
    as a clean rational.
    """
    M = np.array(BCC_PLAQ_NORMALS, dtype=np.int64)
    A = np.array(BCC_LINK_AXES, dtype=np.int64)
    MtM = M.T @ M
    AtA = A.T @ A
    eye4 = 4 * np.eye(3, dtype=np.int64)
    return {
        "n_normals": int(M.shape[0]),
        "n_axes": int(A.shape[0]),
        "sum_m_mT": MtM.tolist(),
        "sum_a_aT": AtA.tolist(),
        "normals_close_on_4I": bool(np.array_equal(MtM, eye4)),
        "axes_close_on_4I": bool(np.array_equal(AtA, eye4)),
        "rhombus_area": BCC_PLAQ_AREA,
        "mixed_area_over_at": BCC4_MIXED_AREA,
    }


# ══════════════════════════════════════════════════════════════════════════
#  F299's d=4 Casimir successor
# ══════════════════════════════════════════════════════════════════════════
#
# F299 specified this and left it unrun ("Remains" item 2): *"Run F94 at
# beta in [5.8, 6.2] with the three character polynomials above and measure
# where Casimir scaling gives way to screening. No new sampling; parameters in
# mc_reach()."*  Two things blocked it, and both are engine gaps rather than
# physics.
#
#   * The three character polynomials had NEVER been applied to a loop matrix.
#     They exist in `casimir_scaling.mc_reach` as expressions in the three
#     TORUS EIGENVALUES, verified against a 2D quadrature -- not against any
#     Wilson loop, in any dimension.
#   * No function anywhere returned the traces needed to evaluate them.
#     `lgt_fork_A_mc.wilson_loop_planar` takes `np.real(np.trace(acc))/3` and
#     averages over sites on its last line, so the matrix field is local and
#     discarded; `polyakov_loop_field` returns Tr W only, i.e. the first power.
#
# So this section supplies (a) the three traces from a genuine R x T loop
# matrix, (b) the higher-rep loops built from them, and (c) the cross-check the
# tree has never done -- the polynomials against EXPLICIT representation
# matrices, sym^2 and sym^3 built by symmetric-subspace isometry and the adjoint
# by Ad(U)_ab = 2 tr(T_a U T_b U^dag).  A polynomial verified only against a
# torus quadrature is verified against the same Jacobi-Trudi machinery that
# produced it; against an explicit rep matrix it is not.
#
# The asymptotic-tension question stays where it belongs.  Casimir scaling
# holds at intermediate R and must break for triality-0 sources (8, 10) once
# the string can decay -- that is the regime structure F299 says d=2 cannot be
# asked about, it is a STATISTICAL statement, and it lives in the battery
# runner.  Nothing here claims it.

#: Dynkin labels for the reps F299's successor names, in its order.
D4_CASIMIR_REPS = (("3", (1, 0)), ("6", (2, 0)), ("8", (1, 1)), ("10", (3, 0)))


def wilson_loop_traces_rt(links, axis_idx: int, R: int, T: int) -> dict:
    """``Tr W``, ``Tr W^2``, ``Tr W^3`` fields for the R x T loop.

    The gap this fills: every existing loop routine in the tree traces and
    averages before returning, so the powers needed for a higher-rep character
    are unrecoverable.  Here the loop MATRIX is kept and the three traces are
    taken from it.

    Returns ``{'t1','t2','t3'}`` as complex fields on the 4D grid, plus
    ``'W'`` (the matrix field) so a caller can build any character it likes.
    """
    ha = _h4(BCC_LINK_AXES[axis_idx])
    Sr, end_s = _transporter(links, ha, R)
    Tt_far, _ = _transporter(links, _T_HOP, T, off0=end_s)
    Sr_top, _ = _transporter(links, ha, R,
                             off0=tuple(c * T for c in _T_HOP))
    Tt_base, _ = _transporter(links, _T_HOP, T)
    W = _matmul(_matmul(Sr, Tt_far), _matmul(_dagger(Sr_top), _dagger(Tt_base)))
    W2 = _matmul(W, W)
    W3 = _matmul(W2, W)
    tr = lambda M: np.trace(M, axis1=-2, axis2=-1)
    return {'W': W, 't1': tr(W), 't2': tr(W2), 't3': tr(W3)}


def rep_character_from_traces(label, t1, t2, t3):
    """``chi_R`` from the three traces of the fundamental loop matrix.

    The polynomials are F299 §4's, transcribed:

        chi_3  = Tr W
        chi_6  = [ (Tr W)^2 + Tr W^2 ] / 2
        chi_8  = Tr W . Tr W^dag - 1
        chi_10 = [ (Tr W)^3 + 3 Tr W Tr W^2 + 2 Tr W^3 ] / 6

    ``chi_8`` is written with ``Tr W^dag`` rather than ``|Tr W|^2`` because the
    two agree only through the identity ``Tr(W^dag) = conj(Tr W)``; that
    identity is unconditional, but the ADJOINT character equalling
    ``|chi_F|^2 - 1`` is a statement about SU(3) specifically, so the
    conjugate is written explicitly to keep the group assumption visible.
    """
    if label == "3":
        return t1
    if label == "6":
        return (t1 * t1 + t2) / 2.0
    if label == "8":
        return t1 * np.conj(t1) - 1.0
    if label == "10":
        return (t1 ** 3 + 3.0 * t1 * t2 + 2.0 * t3) / 6.0
    raise KeyError(label)


def rep_dimension(label) -> int:
    """``d_R`` for the four reps, from the Dynkin labels."""
    p, q = dict(D4_CASIMIR_REPS)[label]
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def casimir_ratio_exact(label):
    """``C_2(R) / C_2(fund)`` as an exact ``Fraction``.

    Computed from the Dynkin labels, not tabulated:
    ``C_2(p,q) = (p^2 + q^2 + p q + 3p + 3q)/3``, so ``C_F = C_2(1,0) = 4/3``.
    """
    from fractions import Fraction
    p, q = dict(D4_CASIMIR_REPS)[label]
    c2 = Fraction(p * p + q * q + p * q + 3 * p + 3 * q, 3)
    cf = Fraction(4, 3)
    return c2 / cf


# ── explicit representation matrices, for the cross-check ─────────────────

def _sym_power_isometry(N: int, k: int) -> np.ndarray:
    """Isometry ``S`` from ``Sym^k(C^N)`` into ``(C^N)^{otimes k}``.

    Columns are the normalised sums over distinct permutations of a multiset,
    so ``S^dag S = I`` on the symmetric subspace and
    ``Sym^k(U) = S^dag (U ox ... ox U) S``.
    """
    from itertools import combinations_with_replacement, permutations
    multisets = list(combinations_with_replacement(range(N), k))
    S = np.zeros((N ** k, len(multisets)), dtype=complex)
    for col, ms in enumerate(multisets):
        for perm in set(permutations(ms)):
            idx = 0
            for p in perm:
                idx = idx * N + p
            S[idx, col] = 1.0
        S[:, col] /= np.linalg.norm(S[:, col])
    return S


def sym_power_rep(U: np.ndarray, k: int) -> np.ndarray:
    """The ``Sym^k`` representation matrix of a single ``(N,N)`` unitary."""
    N = U.shape[-1]
    Tk = U
    for _ in range(k - 1):
        Tk = np.kron(Tk, U)
    S = _sym_power_isometry(N, k)
    return S.conj().T @ Tk @ S


def _su3_generators() -> np.ndarray:
    """The eight ``T_a = lambda_a / 2``, so ``tr(T_a T_b) = delta_ab / 2``."""
    l = np.zeros((8, 3, 3), dtype=complex)
    l[0] = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
    l[1] = [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]
    l[2] = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
    l[3] = [[0, 0, 1], [0, 0, 0], [1, 0, 0]]
    l[4] = [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]]
    l[5] = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
    l[6] = [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]]
    l[7] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / np.sqrt(3.0)
    return l / 2.0


def adjoint_rep(U: np.ndarray) -> np.ndarray:
    """``Ad(U)_ab = 2 tr(T_a U T_b U^dag)`` -- the 8-dimensional real rep."""
    T = _su3_generators()
    Ud = np.conj(U.T)
    out = np.zeros((8, 8), dtype=complex)
    for a in range(8):
        for b in range(8):
            out[a, b] = 2.0 * np.trace(T[a] @ U @ T[b] @ Ud)
    return out


def character_identity_residual(n_samples: int = 6,
                               channel='bcc_casimir_charcheck') -> dict:
    """Verify the three polynomials against EXPLICIT rep matrices.

    This is the check the tree has never run.  `casimir_scaling.mc_reach`
    verifies the same polynomials against `rep_character`, which is the
    Jacobi-Trudi determinant that generated them -- a self-consistency, not an
    independent one.  Here ``chi_6`` and ``chi_10`` are compared against
    ``Sym^2`` and ``Sym^3`` built by symmetric-subspace isometry from the
    fundamental, and ``chi_8`` against ``Ad(U)_ab = 2 tr(T_a U T_b U^dag)``.
    """
    gen = _rng.for_channel(channel)
    worst = {"6": 0.0, "8": 0.0, "10": 0.0}
    dims = {}
    for _ in range(int(n_samples)):
        Z = (gen.normal(size=(3, 3)) + 1j * gen.normal(size=(3, 3))) / np.sqrt(2.0)
        Q, Rq = np.linalg.qr(Z)
        ph = np.diagonal(Rq)
        Q = Q * (ph / np.abs(ph))[None, :]
        Q = Q * np.linalg.det(Q) ** (-1.0 / 3.0)
        t1 = np.trace(Q)
        t2 = np.trace(Q @ Q)
        t3 = np.trace(Q @ Q @ Q)
        explicit = {"6": sym_power_rep(Q, 2),
                    "10": sym_power_rep(Q, 3),
                    "8": adjoint_rep(Q)}
        for lab, M in explicit.items():
            dims[lab] = int(M.shape[0])
            poly = rep_character_from_traces(lab, t1, t2, t3)
            worst[lab] = max(worst[lab], float(abs(np.trace(M) - poly)))
    return {
        "n_samples": int(n_samples),
        "worst_residual": worst,
        "worst_overall": max(worst.values()),
        "explicit_dimensions": dims,
        "dimensions_expected": {lab: rep_dimension(lab)
                                for lab in ("6", "8", "10")},
        "dimensions_match": all(dims[lab] == rep_dimension(lab)
                                for lab in ("6", "8", "10")),
    }


# ── higher-rep loops on a configuration ───────────────────────────────────

def higher_rep_loop_table(links, r_max: int, t_max: int,
                          reps=D4_CASIMIR_REPS) -> dict:
    """``{rep: {(R,T): mean chi_R(W)/d_R}}``, averaged over the 4 spatial axes.

    "No new sampling -- the same configurations, a different trace" (F299).
    The loop matrix is built once per (axis, R, T) and every rep reads its
    traces, so the cost over the fundamental alone is the two extra matrix
    products in :func:`wilson_loop_traces_rt`.
    """
    sites, _, _ = _site_masks(links['t'].shape[:4])
    out = {lab: {} for lab, _pq in reps}
    for R in range(1, r_max + 1):
        for T in range(1, t_max + 1):
            acc = {lab: [] for lab, _pq in reps}
            for ax in range(len(BCC_LINK_AXES)):
                tr = wilson_loop_traces_rt(links, ax, R, T)
                for lab, _pq in reps:
                    chi = rep_character_from_traces(lab, tr['t1'], tr['t2'],
                                                    tr['t3'])
                    acc[lab].append(float(np.real(chi[sites].mean())
                                          / rep_dimension(lab)))
            for lab, _pq in reps:
                out[lab][(R, T)] = float(np.mean(acc[lab]))
    return out


def casimir_scaling_from_loops(table: dict, reps=D4_CASIMIR_REPS) -> dict:
    """``sigma_R/sigma_3`` from per-rep Creutz ratios, against the exact law.

    Returns per-rep Creutz ratios, the ratio to the fundamental at the largest
    common (R,T), and the exact ``C_2(R)/C_F`` it should approach at
    intermediate R.  A deviation is NOT a failure: for the triality-0 reps (8,
    10) the asymptotic tension must fall BELOW Casimir once the string can
    break, and detecting where that happens is the point of running this in
    d=4 rather than d=2.
    """
    chis = {lab: creutz_ratios(table[lab]) for lab, _pq in reps}
    # Record what a Creutz ratio COULD NOT be formed for, and why. A rep loop
    # can come out non-positive -- chi_8/d_8 sits near zero on a disordered
    # configuration, since chi_8 = |Tr W|^2 - 1 and <|Tr W|^2> ~ 1 -- and the
    # log is then undefined. That is a real regime statement (it is the
    # screening the triality-0 reps are here to show) and low statistics makes
    # it worse, so it is REPORTED rather than silently dropped: an empty rows
    # table with no explanation reads as "measured and consistent".
    dropped = []
    for lab, _pq in reps:
        for (R, T) in sorted(table[lab]):
            if R < 2 or T < 2:
                continue
            if (R, T) in chis[lab]:
                continue
            corners = {f"{r}x{t}": table[lab].get((r, t))
                       for r, t in ((R, T), (R - 1, T - 1), (R - 1, T),
                                    (R, T - 1))}
            dropped.append({"rep": lab, "R": R, "T": T, "corners": corners,
                            "why": "a corner loop is <= 0, so -ln is undefined"})
    common = None
    for lab, _pq in reps:
        keys = set(chis[lab])
        common = keys if common is None else (common & keys)
    common = sorted(common or [])
    rows = []
    for (R, T) in common:
        base = chis["3"].get((R, T))
        if not base:
            continue
        row = {"R": R, "T": T, "sigma_3": base}
        for lab, _pq in reps:
            ex = casimir_ratio_exact(lab)
            meas = chis[lab].get((R, T))
            row[f"ratio_{lab}"] = (meas / base) if meas is not None else None
            row[f"casimir_{lab}"] = float(ex)
            row[f"casimir_{lab}_exact"] = str(ex)
        rows.append(row)
    return {
        "creutz_by_rep": {lab: {f"{R}x{T}": v for (R, T), v in chis[lab].items()}
                          for lab, _pq in reps},
        "rows": rows,
        "dropped": dropped,
        "n_dropped": len(dropped),
        "coverage": (f"{len(rows)} usable (R,T) row(s); {len(dropped)} "
                     f"(rep,R,T) Creutz ratio(s) undefined -- see `dropped`"),
        "casimir_law_exact": {lab: str(casimir_ratio_exact(lab))
                              for lab, _pq in reps},
        "dimensions": {lab: rep_dimension(lab) for lab, _pq in reps},
        "note": ("Casimir scaling is expected at INTERMEDIATE R only. The "
                 "triality-0 reps 8 and 10 must fall below the Casimir line "
                 "asymptotically once the string breaks; locating that is why "
                 "d=4 was asked for and d=2 could not answer."),
    }
