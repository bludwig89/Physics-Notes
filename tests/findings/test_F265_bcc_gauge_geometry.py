"""F265 — The gauge sectors live on the genuine BCC lattice.

Pre-F265 the model was split down the middle: every gauge PROPAGATOR was BCC
(gamma, W, Z, gluon all route through ca_bcc.bcc_dispersion(k/2, +-)) while
every gauge ACTION was simple-cubic.  Field strength was built by collapsing
the 8 BCC links into 3 straight +-x,+-y,+-z composites of length 2 ("Build 6
effective SC links from BCC pairs", ca_wmu.py) and then taking square
plaquettes in the 3 coordinate planes with a2 = 4.0.

This file establishes the correct BCC gauge geometry and proves the old
construction is not merely inelegant but BLIND.

Geometry (exact, integer/sympy):
  G1  Sites.  With the conventional cubic cell at side 2 the 8 nearest-neighbour
      hops are the integer body diagonals d in {+-1}^3, and the lattice they
      generate is {n in Z^3 : all three components share a parity} — index 4 in
      Z^3.  Only 1/4 of a cubic array's entries are lattice sites.
  G2  Brillouin zone.  The reciprocal lattice is fcc (pi(1,1,0) and perms),
      V_BZ = 2 pi^3 = (2pi)^3/4, so the cube [-pi,pi)^3 holds exactly 4 copies.
      Independently established as F264 row 326; here it is re-derived from the
      hop set and the BZ mask is verified to select exactly N/4 grid points.
  G3  Loops.  There are NO 3-bond closed loops, so the minimal gauge loop is a
      4-bond rhombus; every rhombus has |d1 x d2| = 2 sqrt2 with its normal on a
      <110> face-diagonal axis; modulo translation there are exactly 6
      orientations forming a single O_h orbit of size 6.
  G4  Reconstruction.  sum_p m_p m_p^T = 4 I exactly over the 6 orientations, so
      the Cartesian field strength follows from the 6 loop phases by a
      closed-form projection f = (1/8) sum_p m_p Phi_p — no pseudo-inverse.

Action correctness:
  G5  Identity links -> F = 0 and Wilson density = 0 bit-for-bit.
  G6  Pure gauge U_d(x) = V(x)^dag V(x+d) -> both actions vanish to round-off.
  G7  A constant-F abelian embedding is recovered exactly by
      cartesian_field_strength (midpoint links are exact for linear A).
  G8  Continuum limit: sum over the 6 orientations of (F_mn d1^m d2^n)^2
      = 8 F_mn F^mn exactly (sympy), i.e. the U(1) Wilson density tends to
      4 eps^2 F_mn F^mn.

The no-go:
  G9  SAME continuum limit.  The composite-SC action's 3 planes with a2 = 4 give
      the IDENTICAL coefficient 8 (sympy, ratio exactly 1).  So the defect is
      invisible to weak-field normalisation checks.
  G10 EXACT KERNEL.  There is an explicit family of link configurations on which
      every composite-SC plaquette is the identity to machine precision while all
      6 BCC plaquettes are maximally disordered.  It persists at every amplitude
      (eps-scan: S_SC == 0 to 1e-16 while S_BCC ~ 1.6 eps^2), so the composite
      field strength misses O(eps) field strength — not just a lattice artefact.
  G11 RANK COUNT.  Per colour component, over N_s BCC sites:
          link variables      4 N_s
          rank(BCC action)    3 N_s - 3
          rank(SC composite)  2 N_s - 4
      so the composite construction is blind to N_s + 1 further directions:
      exactly 1/4 of the raw link space and, asymptotically, 1/3 of the
      curvature-carrying content.
"""

import itertools
import json
import os
import sys

import numpy as np

try:
    import pytest
except ModuleNotFoundError:  # allow standalone __main__ JSON dump without pytest
    class _Mark:
        def __getattr__(self, _):
            return lambda f: f

    class _Pytest:
        mark = _Mark()

    pytest = _Pytest()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation"))

import ca_lattice as cl  # noqa: E402
import ca_bcc_gauge as bg  # noqa: E402

RESULT = os.path.join(
    os.path.dirname(__file__), "..", "..", "test-results",
    "F265_bcc_gauge_geometry.json",
)
_RNG = np.random.default_rng(20260729)
_OUT: dict = {}


# ------------------------------------------------------------------ helpers
def _oh_group():
    """The 48 signed coordinate permutations."""
    mats = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3), dtype=int)
            for a, p in enumerate(perm):
                M[a, p] = sg[a]
            mats.append(M)
    return mats


def _plaq_class(d1, d2):
    neg = lambda v: tuple(-c for c in v)
    quad = [(d1, d2), (neg(d1), d2), (neg(d1), neg(d2)), (d1, neg(d2))]
    return frozenset(frozenset((a, b)) for a, b in quad)


def _expm(M, terms=60):
    """Series matrix exponential (scipy is not a hard dependency here)."""
    R = np.eye(M.shape[-1], dtype=complex)
    T = np.eye(M.shape[-1], dtype=complex)
    for n in range(1, terms):
        T = T @ M / n
        R = R + T
    return R


def _rand_su2_field(shape):
    v = _RNG.normal(size=shape + (4,))
    v /= np.linalg.norm(v, axis=-1, keepdims=True)
    a = v[..., 0] + 1j * v[..., 1]
    b = v[..., 2] + 1j * v[..., 3]
    return bg.su2_pair_to_matrix(a, b)


_KERNEL_H: dict = {}


def _traceless_hermitian_field(shape):
    H = _RNG.normal(size=shape + (2, 2)) + 1j * _RNG.normal(size=shape + (2, 2))
    H = (H + np.conj(np.swapaxes(H, -1, -2))) / 2.0
    tr = np.trace(H, axis1=-2, axis2=-1)
    H[..., 0, 0] -= tr / 2.0
    H[..., 1, 1] -= tr / 2.0
    return H


def _identity_links(shape, N=2):
    I = np.zeros(shape + (N, N), dtype=complex)
    for i in range(N):
        I[..., i, i] = 1.0
    return [I.copy() for _ in range(8)]


# --------------------------------------------------- the composite-SC action
_COMPOSITE = {'x': [(1, 1, 1), (1, -1, -1)],
              'y': [(1, 1, 1), (-1, 1, -1)],
              'z': [(1, 1, 1), (-1, -1, 1)]}
_AXVEC = {'x': (2, 0, 0), 'y': (0, 2, 0), 'z': (0, 0, 2)}


def _composite_link(U8, axis):
    """The pre-F265 straight-line length-2 composite link."""
    d1, d2 = _COMPOSITE[axis]
    A = bg.link_for_direction(U8, d1)
    B = bg.shift_by(bg.link_for_direction(U8, d2), d1)
    return A @ B


def _composite_plaquettes(U8):
    """The pre-F265 three <100>-plane square plaquettes."""
    Us = bg.symmetrise_links(U8)
    out = {}
    for a, b in (('x', 'y'), ('x', 'z'), ('y', 'z')):
        Ua, Ub = _composite_link(Us, a), _composite_link(Us, b)
        P = (Ua
             @ bg.shift_by(Ub, _AXVEC[a])
             @ np.conj(np.swapaxes(bg.shift_by(Ua, _AXVEC[b]), -1, -2))
             @ np.conj(np.swapaxes(Ub, -1, -2)))
        out[a + b] = P
    return out


def _density(P_dict, shape):
    mask = cl.bcc_site_mask(shape)
    N = next(iter(P_dict.values())).shape[-1]
    vals = [(1.0 - np.real(np.trace(P, axis1=-2, axis2=-1)) / N)[mask]
            for P in P_dict.values()]
    return float(np.mean(np.concatenate([v.ravel() for v in vals])))


def _kernel_config(shape, eps=None):
    """Links with every composite-SC plaquette == I but curvature elsewhere.

    Setting the three composite links to the identity identically requires
        U_{(-1,1,1)}(y) = A(y - (2,0,0)),
        U_{(1,-1,1)}(y) = A(y - (0,2,0)),
        U_{(1,1,-1)}(y) = A(y - (0,0,2)),
    with A = U_{(1,1,1)} completely free.  One of the four axis fields is
    therefore invisible to the composite construction.
    """
    if eps is None:
        A = _rand_su2_field(shape)
    else:
        # one fixed generator field, reused across the whole eps-scan so the
        # eps^2 scaling of S_BCC is visible rather than reseeded noise
        H = _KERNEL_H.setdefault(shape, _traceless_hermitian_field(shape))
        A = np.stack([_expm(1j * eps * h)
                      for h in H.reshape(-1, 2, 2)]).reshape(shape + (2, 2))
    U8 = [None] * 8
    idx = {tuple(d): i for i, d in enumerate(cl.BCC_HOP_DIRS)}
    U8[idx[(1, 1, 1)]] = A
    U8[idx[(-1, 1, 1)]] = bg.shift_by(A, (-2, 0, 0))
    U8[idx[(1, -1, 1)]] = bg.shift_by(A, (0, -2, 0))
    U8[idx[(1, 1, -1)]] = bg.shift_by(A, (0, 0, -2))
    for d in cl.BCC_LINK_AXES:
        nd = tuple(-c for c in d)
        U8[idx[nd]] = bg.shift_by(np.conj(np.swapaxes(U8[idx[tuple(d)]], -1, -2)), nd)
    return U8


# ============================================================ G1  sites
@pytest.mark.exact
def test_G1_lattice_is_same_parity_index_four():
    box = 6
    D = [np.array(d) for d in cl.BCC_HOP_DIRS]
    span = set()
    for c in itertools.product(range(-3, 4), repeat=4):
        v = c[0] * D[0] + c[1] * D[1] + c[2] * D[2] + c[3] * D[3]
        if np.max(np.abs(v)) <= box:
            span.add(tuple(int(q) for q in v))
    same = {(x, y, z)
            for x in range(-box, box + 1)
            for y in range(-box, box + 1)
            for z in range(-box, box + 1)
            if x % 2 == y % 2 == z % 2}
    assert span == same
    det = int(round(abs(np.linalg.det(np.array([D[0], D[1], D[2]])))))
    assert det == cl.BCC_INDEX_IN_Z3 == 4
    fracs = []
    for L in (4, 6, 8, 12):
        m = cl.bcc_site_mask((L, L, L))
        fracs.append(m.sum() / m.size)
    assert all(f == 0.25 for f in fracs)
    _OUT['G1'] = {'span_equals_same_parity': True, 'index_in_Z3': det,
                  'site_fraction': fracs, 'num_hops': len(cl.BCC_HOP_DIRS),
                  'num_link_axes': len(cl.BCC_LINK_AXES)}


# ============================================================ G2  BZ
@pytest.mark.exact
def test_G2_reciprocal_is_fcc_cube_holds_four_bz():
    Gb = cl.bcc_reciprocal_basis()
    for G in Gb:
        for d in list(cl.BCC_HOP_DIRS) + [(2, 0, 0), (0, 2, 0), (0, 0, 2)]:
            q = float(np.dot(G, d)) / (2 * np.pi)
            assert abs(q - round(q)) < 1e-12
    assert abs(cl.bcc_bz_volume() - 2 * np.pi ** 3) < 1e-9
    assert abs((2 * np.pi) ** 3 / cl.bcc_bz_volume() - 4.0) < 1e-9
    counts = {}
    for L in (4, 6, 8, 12, 16):
        _, _, _, in_bz, w = cl.make_kgrid_bcc(L, L, L)
        counts[L] = (int(in_bz.sum()), L ** 3 // 4)
        assert in_bz.sum() == L ** 3 // 4
        assert w == 1.0 / cl.BCC_BZ_COPIES
    # the fcc shifts really are periods of the integer-hop walk
    L = 8
    KX, KY, KZ, _, _ = cl.make_kgrid_bcc(L, L, L)
    worst = 0.0
    for s in ((L // 2, L // 2, 0), (L // 2, 0, L // 2), (0, L // 2, L // 2)):
        r = lambda A: np.roll(A, tuple(-c for c in s), axis=(0, 1, 2))
        for d in cl.BCC_HOP_DIRS:
            p1 = np.exp(1j * (d[0] * KX + d[1] * KY + d[2] * KZ))
            p2 = np.exp(1j * (d[0] * r(KX) + d[1] * r(KY) + d[2] * r(KZ)))
            worst = max(worst, float(np.abs(p1 - p2).max()))
    assert worst < 1e-12
    _OUT['G2'] = {'V_BZ_over_pi3': cl.bcc_bz_volume() / np.pi ** 3,
                  'copies_in_cube': 4, 'bz_mask_counts': counts,
                  'fcc_shift_phase_mismatch': worst}


# ============================================================ G3  loops
@pytest.mark.exact
def test_G3_minimal_loop_is_four_bond_rhombus_six_orientations():
    D = [np.array(d) for d in cl.BCC_HOP_DIRS]
    n3 = sum(1 for i in range(8) for j in range(8) for k in range(8)
             if not np.any(D[i] + D[j] + D[k]))
    assert n3 == 0                                   # no 3-bond loops
    assert len(cl.BCC_PLAQUETTES) == 6
    areas, normals = set(), set()
    for d1, d2 in cl.BCC_PLAQUETTES:
        n = np.cross(np.array(d1), np.array(d2))
        areas.add(round(float(np.linalg.norm(n)), 12))
        normals.add(tuple(sorted(map(abs, (n // 2).tolist()))))
    assert areas == {round(2 * np.sqrt(2), 12)}
    assert abs(cl.BCC_PLAQ_AREA - 2 * np.sqrt(2)) < 1e-15
    assert normals == {(0, 1, 1)}                    # all <110>
    axes = {tuple(m) if tuple(m) > tuple(-np.array(m)) else tuple(-np.array(m))
            for m in cl.BCC_PLAQ_NORMALS}
    assert len(axes) == 6
    seed = cl.BCC_PLAQUETTES[0]
    orbit = {_plaq_class(tuple(M @ np.array(seed[0])), tuple(M @ np.array(seed[1])))
             for M in _oh_group()}
    assert len(orbit) == 6                           # single O_h orbit
    _OUT['G3'] = {'num_3bond_loops': 0, 'num_orientations': 6,
                  'area': 2 * np.sqrt(2), 'normals_are_110': True,
                  'distinct_normal_axes': 6, 'oh_orbit_size': len(orbit)}


# ============================================================ G4  projection
@pytest.mark.exact
def test_G4_normal_gram_is_four_identity():
    M = np.array(cl.BCC_PLAQ_NORMALS, dtype=float)
    G = M.T @ M
    assert np.allclose(G, 4.0 * np.eye(3), atol=0, rtol=0)
    _OUT['G4'] = {'MtM': G.tolist(), 'equals_4I_exactly': True}


# ============================================================ G5  identity
@pytest.mark.exact
def test_G5_identity_links_give_zero():
    shape = (4, 4, 4)
    U8 = _identity_links(shape)
    assert bg.link_reversal_residual(U8) == 0.0
    F = bg.plaquette_field_strength_su2(U8)
    for key in ('xy', 'xz', 'yz'):
        assert np.all(F[key] == 0.0)
    assert bg.wilson_action_density(U8) == 0.0
    _OUT['G5'] = {'F_max': 0.0, 'action': 0.0, 'reversal_residual': 0.0}


# ============================================================ G6  pure gauge
@pytest.mark.machine_precision
def test_G6_pure_gauge_annihilates_both_actions():
    shape = (6, 6, 6)
    V = _rand_su2_field(shape)
    Vd = np.conj(np.swapaxes(V, -1, -2))
    idx = {tuple(d): i for i, d in enumerate(cl.BCC_HOP_DIRS)}
    U8 = [None] * 8
    for d in cl.BCC_LINK_AXES:
        U8[idx[tuple(d)]] = Vd @ bg.shift_by(V, d)      # U_d(x) = V(x)^dag V(x+d)
    for d in cl.BCC_LINK_AXES:
        nd = tuple(-c for c in d)
        U8[idx[nd]] = bg.shift_by(np.conj(np.swapaxes(U8[idx[tuple(d)]], -1, -2)), nd)
    s_bcc = bg.wilson_action_density(U8)
    s_sc = _density(_composite_plaquettes(U8), shape)
    F = bg.plaquette_field_strength_su2(U8)
    fmax = max(float(np.abs(F[k]).max()) for k in F)
    assert abs(s_bcc) < 1e-12 and abs(s_sc) < 1e-12 and fmax < 1e-10
    _OUT['G6'] = {'S_BCC': s_bcc, 'S_SC': s_sc, 'F_max': fmax}


# ============================================================ G7  constant F
@pytest.mark.machine_precision
def test_G7_constant_field_strength_recovered_exactly():
    shape = (8, 8, 8)
    Fin = np.array([[0.0, 0.31, -0.17], [-0.31, 0.0, 0.23], [0.17, -0.23, 0.0]])
    g = 1e-3
    idx = {tuple(d): i for i, d in enumerate(cl.BCC_HOP_DIRS)}
    ix, iy, iz = np.meshgrid(*[np.arange(L, dtype=float) for L in shape],
                             indexing='ij')
    xs = np.stack([ix, iy, iz], axis=-1)
    U8 = [None] * 8
    for d in cl.BCC_LINK_AXES:
        dv = np.array(d, dtype=float)
        mid = xs + dv / 2.0
        A = -0.5 * np.einsum('mn,xyzn->xyzm', Fin, mid)     # A_m = -1/2 F_mn x^n
        phase = g * np.einsum('xyzm,m->xyz', A, dv)
        c, s = np.cos(phase), np.sin(phase)
        M = np.zeros(shape + (2, 2), dtype=complex)
        M[..., 0, 0] = c + 1j * s                            # exp(i phase tau^3)
        M[..., 1, 1] = c - 1j * s
        U8[idx[tuple(d)]] = M
    for d in cl.BCC_LINK_AXES:
        nd = tuple(-c for c in d)
        U8[idx[nd]] = bg.shift_by(np.conj(np.swapaxes(U8[idx[tuple(d)]], -1, -2)), nd)
    # A_m is linear, hence NOT periodic: exclude the torus-wrap shell and keep
    # genuine BCC sites only.
    core = np.zeros(shape, dtype=bool)
    core[2:shape[0] - 2, 2:shape[1] - 2, 2:shape[2] - 2] = True
    sel = cl.bcc_site_mask(shape) & core
    F = bg.cartesian_field_strength(U8, bg.PAULI, g_lat=g)
    got = {'xy': float(np.mean(F['xy'][2][sel])),
           'xz': float(np.mean(F['xz'][2][sel])),
           'yz': float(np.mean(F['yz'][2][sel]))}
    spread = {k: float(np.std(F[k][2][sel])) for k in got}
    want = {'xy': Fin[0, 1], 'xz': Fin[0, 2], 'yz': Fin[1, 2]}
    errs = {k: abs(got[k] - want[k]) for k in want}
    # residual error is the O((g phi)^2/6) of sin(g phi)/g, not a geometry error
    assert max(errs.values()) < 1e-6
    assert max(spread.values()) < 1e-14      # site-independent, as it must be
    res = bg.cartesian_reconstruction_residual(U8, bg.PAULI, g_lat=g, mask=sel)
    assert res < 1e-6
    _OUT['G7'] = {'recovered': got, 'input': want, 'abs_err': errs,
                  'site_spread': spread, 'reconstruction_residual': res}


# ============================================================ G8/G9 continuum
@pytest.mark.exact
def test_G8_G9_same_continuum_limit_coefficient_eight():
    import sympy as sp
    f12, f13, f23 = sp.symbols('f12 f13 f23')
    F = sp.zeros(3, 3)
    F[0, 1], F[1, 0] = f12, -f12
    F[0, 2], F[2, 0] = f13, -f13
    F[1, 2], F[2, 1] = f23, -f23
    S_bcc = 0
    for d1, d2 in cl.BCC_PLAQUETTES:
        phi = sum(F[m, n] * d1[m] * d2[n] for m in range(3) for n in range(3))
        S_bcc += sp.expand(phi ** 2)
    S_sc = sum(sp.expand((4 * F[m, n]) ** 2) for m, n in ((0, 1), (0, 2), (1, 2)))
    FF = sum(F[m, n] ** 2 for m in range(3) for n in range(3))
    r_bcc = sp.simplify(sp.expand(S_bcc) / FF)
    r_sc = sp.simplify(sp.expand(S_sc) / FF)
    assert r_bcc == 8 and r_sc == 8
    assert sp.simplify(sp.expand(S_bcc) - sp.expand(S_sc)) == 0
    _OUT['G8_G9'] = {'ratio_BCC': int(r_bcc), 'ratio_SC': int(r_sc),
                     'difference': 0,
                     'note': 'identical continuum limit; defect is invisible '
                             'to weak-field normalisation checks'}


# ============================================================ G10 the kernel
@pytest.mark.machine_precision
def test_G10_composite_SC_action_has_an_exact_kernel():
    shape = (4, 4, 4)
    U8 = _kernel_config(shape)
    assert bg.link_reversal_residual(U8) < 1e-12
    comp = _composite_plaquettes(U8)
    I = np.eye(2)
    comp_dev = max(float(np.abs(P - I).max()) for P in comp.values())
    s_sc = _density(comp, shape)
    P6 = bg.bcc_plaquette_set(U8)
    bcc_dev = max(float(np.abs(P - I).max()) for P in P6.values())
    s_bcc = bg.wilson_action_density(U8)
    assert comp_dev < 1e-12 and abs(s_sc) < 1e-12       # composite: blind
    assert bcc_dev > 1.0 and s_bcc > 0.5                # BCC: maximally disordered
    scan = []
    for eps in (1.0, 0.3, 0.1, 0.03, 0.01):
        Ue = _kernel_config(shape, eps=eps)
        ssc = _density(_composite_plaquettes(Ue), shape)
        sbc = bg.wilson_action_density(Ue)
        scan.append({'eps': eps, 'S_SC': ssc, 'S_BCC': sbc,
                     'S_BCC_over_eps2': sbc / eps ** 2})
        assert abs(ssc) < 1e-12                          # blind at EVERY amplitude
        assert sbc > 0.0
    _OUT['G10'] = {'composite_plaquette_dev': comp_dev, 'S_SC': s_sc,
                   'bcc_plaquette_dev': bcc_dev, 'S_BCC': s_bcc,
                   'eps_scan': scan}


# ============================================================ G11 rank count
@pytest.mark.exact
def test_G11_composite_blind_to_one_third_of_curvature_content():
    """At quadratic order the colour index decouples, so each action's Hessian
    is B^T B with B the signed loop-incidence matrix; rank = dimG * rank(B)."""
    idx_ax = {tuple(d): i for i, d in enumerate(cl.BCC_LINK_AXES)}
    rows = {}
    for L in (4, 6, 8):
        sites = [s for s in itertools.product(range(L), repeat=3)
                 if s[0] % 2 == s[1] % 2 == s[2] % 2]
        sidx = {s: i for i, s in enumerate(sites)}
        NS = len(sites)
        sh = lambda s, v: tuple((s[i] + v[i]) % L for i in range(3))

        def var(x, d):
            d = tuple(d)
            if d in idx_ax:
                return idx_ax[d] * NS + sidx[x], +1.0
            nd = tuple(-c for c in d)
            return idx_ax[nd] * NS + sidx[sh(x, d)], -1.0

        def incidence(loops):
            B = np.zeros((len(loops), 4 * NS))
            for r, (s, steps) in enumerate(loops):
                x = s
                for d in steps:
                    c, sg = var(x, d)
                    B[r, c] += sg
                    x = sh(x, d)
                assert x == s
            return B

        neg = lambda v: tuple(-c for c in v)
        bcc_loops = [(s, [d1, d2, neg(d1), neg(d2)])
                     for s in sites for d1, d2 in cl.BCC_PLAQUETTES]
        sc_loops = []
        for s in sites:
            for a, b in (('x', 'y'), ('x', 'z'), ('y', 'z')):
                steps = (_COMPOSITE[a] + _COMPOSITE[b]
                         + [neg(d) for d in reversed(_COMPOSITE[a])]
                         + [neg(d) for d in reversed(_COMPOSITE[b])])
                sc_loops.append((s, steps))
        rb = int(np.linalg.matrix_rank(incidence(bcc_loops), tol=1e-8))
        rs = int(np.linalg.matrix_rank(incidence(sc_loops), tol=1e-8))
        assert rb == 3 * NS - 3, (L, rb, 3 * NS - 3)
        assert rs == 2 * NS - 4, (L, rs, 2 * NS - 4)
        assert rb - rs == NS + 1
        rows[L] = {'N_sites': NS, 'link_vars': 4 * NS,
                   'rank_BCC': rb, 'rank_SC': rs,
                   'blind_dirs': rb - rs,
                   'blind_frac_of_link_space': (rb - rs) / (4 * NS),
                   'blind_frac_of_curvature_content': (rb - rs) / rb}
    assert abs(rows[8]['blind_frac_of_link_space'] - 0.25) < 0.01
    assert abs(rows[8]['blind_frac_of_curvature_content'] - 1 / 3) < 0.01
    _OUT['G11'] = {'per_L': rows,
                   'formulae': {'link_vars': '4 N_s',
                                'rank_BCC': '3 N_s - 3',
                                'rank_SC': '2 N_s - 4',
                                'blind': 'N_s + 1'},
                   'asymptotic_blind_fraction_of_link_space': 0.25,
                   'asymptotic_blind_fraction_of_curvature': 1 / 3}


# ============================================================ G12 Bianchi
@pytest.mark.machine_precision
def test_G12_bianchi_converges_at_second_order_in_ka():
    """Bianchi convergence, and why the SC composite *looked* better.

    ``ca_wmu.bianchi_residual`` is the naive Cartesian curl
    ``d_x F_yz + d_y F_zx + d_z F_xy`` taken spectrally on the cubic array.  For
    the composite-SC construction all three planes live on one simple-cubic
    sublattice, where the product of a cube's six faces is an *exact* lattice
    identity — so it converges at O((ka)^3) and its residual is anomalously
    small.  That is not a virtue: it is the same restriction to 3 of the 6
    orientations that makes it blind (G10/G11).

    The genuine BCC field strength is reconstructed from a non-orthogonal frame
    of 6 rhombi whose centres differ per orientation, so the Cartesian curl
    converges at the generic O((ka)^2).  This is the resolution of the
    long-standing "composite BCC plaquette has O(eps) cross-direction
    contributions" roadmap item: the cross terms are physical content, not an
    artefact to be transformed away.
    """
    import ca_wmu as cw
    idx = {tuple(d): i for i, d in enumerate(cl.BCC_HOP_DIRS)}

    def build(L, g=0.01):
        shape = (L, L, L)
        rng = np.random.default_rng(5)
        gr = np.meshgrid(*[np.arange(L, dtype=float)] * 3, indexing='ij')
        A0 = np.zeros(shape + (3,))
        for n in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)):
            ph = 2 * np.pi * sum(n[i] * gr[i] for i in range(3)) / L \
                 + rng.uniform(0, 2 * np.pi)
            A0 += np.sin(ph)[..., None] * rng.normal(size=3)
        U8 = [None] * 8
        for d in cl.BCC_LINK_AXES:
            dv = np.array(d, dtype=float)
            Amid = 0.5 * (A0 + np.roll(A0, tuple(-int(c) for c in d),
                                       axis=(0, 1, 2)))
            p = g * np.einsum('xyzm,m->xyz', Amid, dv)
            c, s = np.cos(p), np.sin(p)
            M = np.zeros(shape + (2, 2), dtype=complex)
            M[..., 0, 0] = c + 1j * s
            M[..., 1, 1] = c - 1j * s
            U8[idx[tuple(d)]] = M
        for d in cl.BCC_LINK_AXES:
            nd = tuple(-c for c in d)
            U8[idx[nd]] = bg.shift_by(
                np.conj(np.swapaxes(U8[idx[tuple(d)]], -1, -2)), nd)
        return U8, g

    rows, prev = [], None
    for L in (16, 24, 32, 48):
        U8, g = build(L)
        F = bg.cartesian_field_strength(U8, bg.PAULI, g_lat=g)
        rel = cw.bianchi_residual(F) / max(float(np.abs(F[k]).max()) for k in F)
        slope = (float('nan') if prev is None
                 else float(np.log(rel / prev[0]) / np.log(prev[1] / L)))
        rows.append({'L': L, 'ka': 2 * np.pi / L, 'rel_bianchi': rel,
                     'slope': slope})
        prev = (rel, L)
    slopes = [r['slope'] for r in rows[1:]]
    assert all(abs(s - 2.0) < 0.1 for s in slopes), rows
    _OUT['G12'] = {'convergence': rows, 'observed_order': 2,
                   'note': 'O((ka)^2); the composite-SC O((ka)^3) came from '
                           'its exact SC cube-face identity, which is the same '
                           'restriction that makes it blind (G10/G11)'}


def _dump():
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, 'w') as fh:
        json.dump(_OUT, fh, indent=1, default=str)
    print(f"wrote {RESULT}")


if __name__ == '__main__':
    for name, fn in sorted(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
            print(f"  ok  {name}")
    _dump()
    print(json.dumps(_OUT, indent=1, default=str))
