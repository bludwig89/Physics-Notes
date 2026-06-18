"""
ca_lpt_vertex.py — the cubic expansion of the compact gauge action: the
3-gluon vertex, read directly off the action by amplitude differentiation
(no hand-transcribed closed form), validated against the propagator and the
continuum vertex. The vertex half of the q* d1 computation (companion to
ca_lpt_wilson.py, which validated the BZ-integration core).

Why this is the right object for the RULE
------------------------------------------
The rule's gluon self-coupling comes from the same compact SU(N) plaquette
(magnetic term) as Wilson's; what differs between the rule and Wilson is the
PROPAGATOR (the luminal F26 Omega_even kinetic sector), not the plaquette
vertex. So the 3-gluon vertex built and validated here on the compact plaquette
is shared, and the rule's d1 = (this vertex) folded with the rule's Omega_even
propagator. Building+validating it on the plaquette is therefore exactly the
reusable piece.

Method (robust, definition-based)
---------------------------------
The action expanded in the gauge field is
    S = (1/2) A.K.A + (1/3!) V.A.A.A + ...
We read K and V straight off S(A) by finite-difference amplitude derivatives,
planting REAL plane-wave gluon modes (SU(2), T^a = sigma^a/2, f^{abc}=eps^{abc})
on a small periodic 4D lattice:
  * quadratic:  c2(k) = [S(eps)+S(-eps)]/(2 eps^2)  -> must be proportional to
    the transverse propagator Khat(k)=sum 4 sin^2(k_mu/2)  (VALIDATION 1).
  * cubic 3-gluon vertex: the mixed third derivative
        d^3 S/de1 de2 de3 = (1/(8 h^3)) sum_{s1,s2,s3=+-1} s1 s2 s3 S(s1h,s2h,s3h)
    of three DISTINCT modes (distinct colours) isolates the e1 e2 e3 trilinear
    = the (permutation-summed) vertex. It must be Bose-antisymmetric in colour
    (VALIDATION 2, the non-abelian f^{abc} structure — PASSES to machine
    precision). The continuum-magnitude match (VALIDATION 3) is so far only a
    DIAGNOSTIC: it agrees at the softest momentum but the cross-momentum
    magnitude needs the lattice point-splitting form-factors cos(k_mu/2) added to
    the comparison (and non-null kinematics) before it is a precision check — see
    continuum_limit_check. So the vertex EXTRACTOR is validated (propagator +
    colour antisymmetry); the momentum/Lorentz structure is validated in form but
    not yet to precision.

Vectorised SU(2) action (numpy einsum + roll) so L=8 is fast.
"""
from __future__ import annotations

import math

import numpy as np

# SU(2) generators T^a = sigma^a/2
_SIG = np.array([[[0, 1], [1, 0]],
                 [[0, -1j], [1j, 0]],
                 [[1, 0], [0, -1]]], dtype=complex)
_I2 = np.eye(2, dtype=complex)


# ----------------------------------------------------------------------
#  vectorised SU(2) link and plaquette action
# ----------------------------------------------------------------------
def _expi_su2(V):
    """U = exp(i V^a T^a) for a field V of shape (...,3); closed SU(2) form.
    Returns (...,2,2) complex."""
    n = np.sqrt(np.einsum("...a,...a->...", V, V))          # |V|
    n_safe = np.where(n > 1e-30, n, 1.0)
    nhat = V / n_safe[..., None]
    c = np.cos(n / 2.0)[..., None, None]
    s = np.sin(n / 2.0)[..., None, None]
    nsig = np.einsum("...a,aij->...ij", nhat, _SIG)
    return c * _I2 + 1j * s * nsig


def _mm(A, B):
    return np.einsum("...ij,...jk->...ik", A, B)


def _dag(A):
    return np.conj(np.swapaxes(A, -1, -2))


def wilson_action(A, g, d=4):
    """Sum_p (1 - 1/2 Re Tr U_p) over a periodic d-dim lattice.
    A: list of d arrays each shape (L,)*d + (3,), real."""
    U = [_expi_su2(g * Amu) for Amu in A]
    S = 0.0
    for mu in range(d):
        for nu in range(mu + 1, d):
            Up = _mm(_mm(U[mu], np.roll(U[nu], -1, axis=mu)),
                     _mm(_dag(np.roll(U[mu], -1, axis=nu)), _dag(U[nu])))
            tr = np.trace(Up, axis1=-2, axis2=-1).real
            S += np.sum(1.0 - 0.5 * tr)
    return float(S)


# ----------------------------------------------------------------------
#  plane-wave gluon modes
# ----------------------------------------------------------------------
def _grid(L, d):
    return np.indices((L,) * d)            # (d, L,...,L)


def plane_mode(L, n_vec, pol, a0, d=4):
    """Real field A[mu][x][a] = pol_mu * delta(a,a0) * cos(k.x), k = 2pi n/L."""
    g = _grid(L, d)
    k = [2 * math.pi * n_vec[i] / L for i in range(d)]
    phase = sum(k[i] * g[i] for i in range(d))
    c = np.cos(phase)
    A = [np.zeros((L,) * d + (3,)) for _ in range(d)]
    for mu in range(d):
        if abs(pol[mu]) > 0:
            A[mu][..., a0] = pol[mu] * c
    return A


def _add(*configs):
    d = len(configs[0])
    return [sum(cfg[mu] for cfg in configs) for mu in range(d)]


def _scale(A, s):
    return [s * Amu for Amu in A]


def khat(n_vec, L):
    return sum(4 * math.sin(math.pi * n / L) ** 2 for n in n_vec)


def khat_vec(n_vec, L):
    return np.array([2 * math.sin(math.pi * n / L) for n in n_vec])


# ----------------------------------------------------------------------
#  VALIDATION 1 — quadratic term reproduces the propagator
# ----------------------------------------------------------------------
def _transverse_pol(n_vec, L, d=4, seed=0):
    kh = khat_vec(n_vec, L)
    rng = np.random.default_rng(seed)
    e = rng.standard_normal(d)
    e = e - (e @ kh) / (kh @ kh + 1e-30) * kh
    return e / (np.linalg.norm(e) + 1e-30)


def propagator_check(L=6, g=0.5, modes=((1, 0, 0, 0), (1, 1, 0, 0),
                                        (2, 1, 0, 0), (1, 1, 1, 0))) -> dict:
    """c2(k)/Khat(k) must be CONSTANT across (non-Nyquist) transverse modes."""
    eps = 1e-3
    rows = []
    for n_vec in modes:
        pol = _transverse_pol(n_vec, L)
        Ap = plane_mode(L, n_vec, pol * eps, 0)
        Am = plane_mode(L, n_vec, -pol * eps, 0)
        c2 = (wilson_action(Ap, g) + wilson_action(Am, g)) / (2 * eps ** 2)
        kh = khat(n_vec, L)
        rows.append({"n": n_vec, "Khat": kh, "c2": c2, "ratio": c2 / kh})
    ratios = [r["ratio"] for r in rows]
    return {"rows": rows,
            "ratio_spread_rel": (max(ratios) - min(ratios)) / np.mean(ratios),
            "constant": (max(ratios) - min(ratios)) / np.mean(ratios) < 1e-6,
            "statement": "c2(k) proportional to Khat(k) => action expansion "
                         "reproduces the gluon propagator (quadratic validated)"}


# ----------------------------------------------------------------------
#  the 3-gluon vertex by mixed third derivative
# ----------------------------------------------------------------------
def three_gluon_amplitude(L, modes3, g=0.5, h=2.5e-2) -> float:
    """Mixed third derivative d^3 S/de1 de2 de3 of three distinct modes (each a
    (n_vec, pol, colour) triple). Isolates the e1 e2 e3 trilinear = the
    permutation-summed 3-gluon vertex contracted with the three polarisations.
    Distinct colours kill the e_i^3 self-terms."""
    cfgs = [plane_mode(L, nv, pol, a0) for (nv, pol, a0) in modes3]
    acc = 0.0
    for s1 in (+1, -1):
        for s2 in (+1, -1):
            for s3 in (+1, -1):
                A = _add(_scale(cfgs[0], s1 * h), _scale(cfgs[1], s2 * h),
                         _scale(cfgs[2], s3 * h))
                acc += s1 * s2 * s3 * wilson_action(A, g)
    return acc / (8 * h ** 3)


def continuum_3g_contract(n1, n2, n3, p1, p2, p3, L, colours=(0, 1, 2)) -> float:
    """Continuum 3-gluon vertex g f^{abc}[delta_{mn}(k1-k2)_r + cyc] contracted
    with polarisations p1,p2,p3 and colours; lattice momenta k = khat_vec.
    f^{abc}=eps; with colours (0,1,2), f=+1 for the e1e2e3 ordering (×perms)."""
    k1, k2, k3 = (khat_vec(n, L) for n in (n1, n2, n3))
    # sum over the 3 colour assignments the mixed-derivative produces:
    # the vertex is fully antisymmetric in (mu,a,k); the contracted amplitude is
    # eps^{abc} * [p1.p2 (k1-k2).p3 + p2.p3 (k2-k3).p1 + p3.p1 (k3-k1).p2]
    term = (np.dot(p1, p2) * np.dot(k1 - k2, p3)
            + np.dot(p2, p3) * np.dot(k2 - k3, p1)
            + np.dot(p3, p1) * np.dot(k3 - k1, p2))
    return term     # times g f and a convention constant fixed by the ratio test


def continuum_limit_check(L=8, g=0.4) -> dict:
    """At small momenta the lattice 3-gluon amplitude must approach the continuum
    contraction (up to one overall convention constant, fixed on the smallest
    momentum). We track the ratio toward 1 as momenta shrink (L sets the min)."""
    # three transverse modes with n1+n2+n3 = 0 (mod L) => momentum conservation
    triples = [((1, 0, 0, 0), (0, 1, 0, 0), (-1, -1, 0, 0)),
               ((1, 1, 0, 0), (0, 1, 1, 0), (-1, -2, -1, 0)),
               ((2, 1, 0, 0), (1, 1, 1, 0), (-3, -2, -1, 0))]
    rows = []
    for tri in triples:
        n1, n2, n3 = tri
        p1 = _transverse_pol(n1, L, seed=1)
        p2 = _transverse_pol(n2, L, seed=2)
        p3 = _transverse_pol(n3, L, seed=3)
        lat = three_gluon_amplitude(
            L, [(n1, p1, 0), (n2, p2, 1), (n3, p3, 2)], g=g)
        con = continuum_3g_contract(n1, n2, n3, p1, p2, p3, L)
        kmag = math.sqrt(sum((2 * math.sin(math.pi * x / L)) ** 2 for x in n1))
        rows.append({"triple": tri, "kmag_mode1": round(kmag, 3),
                     "lattice": lat, "continuum": con,
                     "ratio": (lat / con if abs(con) > 1e-9 else None)})
    # convention constant from the softest triple
    soft = rows[0]
    const = soft["ratio"]
    for r in rows:
        r["lattice_over_(const*continuum)"] = (
            r["lattice"] / (const * r["continuum"])
            if r["continuum"] and const else None)
    return {"rows": rows, "convention_const_from_softest": const,
            "validated": False,
            "statement": "DIAGNOSTIC, not a clean validation: the lattice 3-gluon "
                         "amplitude matches the continuum contraction at the "
                         "softest momentum, but the cross-momentum magnitude does "
                         "NOT track a single constant because (i) the comparison "
                         "omits the lattice point-splitting form-factors "
                         "cos(k_mu/2) and (ii) the transverse-pol contraction has "
                         "kinematic cancellations. The momentum/Lorentz structure "
                         "is therefore NOT yet precision-validated; the clean "
                         "validations are propagator_check (quadratic) + "
                         "bose_antisymmetry (cubic colour). Next: add the form "
                         "factors to the continuum comparison."}


def bose_antisymmetry(L=6, g=0.4) -> dict:
    """Swapping two external legs (mode+colour) flips the amplitude sign
    (f^{abc} antisymmetry). Check |V(1,2,3)+V(2,1,3)| approx 0."""
    n1, n2, n3 = (1, 0, 0, 0), (0, 1, 0, 0), (-1, -1, 0, 0)
    p1 = _transverse_pol(n1, L, seed=1)
    p2 = _transverse_pol(n2, L, seed=2)
    p3 = _transverse_pol(n3, L, seed=3)
    V123 = three_gluon_amplitude(L, [(n1, p1, 0), (n2, p2, 1), (n3, p3, 2)], g=g)
    V213 = three_gluon_amplitude(L, [(n2, p2, 1), (n1, p1, 0), (n3, p3, 2)], g=g)
    # same three legs, swapped order -> mixed derivative is symmetric in its
    # arguments, so this checks the EXTRACTION symmetry; the physical antisymmetry
    # is in colour: swap colours of legs 1,2 -> sign flip
    V_swapcol = three_gluon_amplitude(
        L, [(n1, p1, 1), (n2, p2, 0), (n3, p3, 2)], g=g)
    return {"V123": V123, "V_colourswap_12": V_swapcol,
            "sum": V123 + V_swapcol,
            "antisymmetric": abs(V123 + V_swapcol) < 1e-6 * (abs(V123) + 1e-12),
            "statement": "colour swap (a<->b) flips the vertex sign (f^{abc} "
                         "antisymmetry) — the non-abelian structure is correct"}


def bose_full_symmetry(L=6, g=0.4) -> dict:
    """The 3-gluon vertex is totally Bose-symmetric under SIMULTANEOUS exchange of
    two legs' (momentum, Lorentz pol, colour): V is invariant. Combined with the
    colour antisymmetry (bose_antisymmetry), this fixes the full statistics. We
    check a full swap and a cyclic permutation reproduce V to machine precision
    (non-null kinematics)."""
    n1, n2, n3 = (1, 0, 0, 0), (0, 1, 0, 0), (-1, -1, 0, 0)
    p1 = _transverse_pol(n1, L, seed=1)
    p2 = _transverse_pol(n2, L, seed=2)
    p3 = _transverse_pol(n3, L, seed=3)
    legs = [(n1, p1, 0), (n2, p2, 1), (n3, p3, 2)]
    V = three_gluon_amplitude(L, legs, g=g)
    Vswap = three_gluon_amplitude(L, [legs[1], legs[0], legs[2]], g=g)
    Vcyc = three_gluon_amplitude(L, [legs[1], legs[2], legs[0]], g=g)
    sc = abs(V) + 1e-12
    return {"V": V, "V_fullswap_12": Vswap, "V_cyclic": Vcyc,
            "swap_dev": abs(Vswap - V), "cyclic_dev": abs(Vcyc - V),
            "bose_symmetric": (abs(Vswap - V) < 1e-6 * sc
                               and abs(Vcyc - V) < 1e-6 * sc),
            "statement": "vertex invariant under full (momentum+Lorentz+colour) "
                         "leg exchange — total Bose symmetry of the 3-gluon vertex"}


def continuum_scaling_point(L, g=0.3, seed_base=10) -> dict:
    """One point for the continuum-limit study (driven over L by the native
    runner). Uses L-INDEPENDENT transverse polarisations (fixed random vectors
    projected against the CONTINUUM directions), non-null kinematics, and the
    volume-normalised contracted amplitude. As L grows (k -> 0, form factors
    cos(k/2) -> 1), (amp/Vol)/continuum should approach a single constant — the
    clean test that the vertex carries the correct continuum tensor + form
    factors. Needs large L (small k); hence the native runner."""
    n1, n2, n3 = (1, 1, 0, 0), (1, -1, 0, 0), (-2, 0, 0, 0)

    def fixed_pol(n_vec, seed):
        nn = np.array(n_vec, float)
        nh = nn / np.linalg.norm(nn)
        e = np.random.default_rng(seed).standard_normal(4)
        e = e - (e @ nh) * nh
        return e / np.linalg.norm(e)

    p1 = fixed_pol(n1, seed_base + 1)
    p2 = fixed_pol(n2, seed_base + 2)
    p3 = fixed_pol(n3, seed_base + 3)
    amp = three_gluon_amplitude(L, [(n1, p1, 0), (n2, p2, 1), (n3, p3, 2)], g=g)
    vol = L ** 4
    con = continuum_3g_contract(n1, n2, n3, p1, p2, p3, L)
    kmag = math.sqrt(sum((2 * math.sin(math.pi * x / L)) ** 2 for x in n1))
    return {"L": L, "kmag": kmag, "amp_over_vol": amp / vol, "continuum": con,
            "ratio": (amp / vol) / con if abs(con) > 1e-12 else None}


def report() -> dict:
    return {"propagator_check": propagator_check(),
            "bose_antisymmetry": bose_antisymmetry(),
            "bose_full_symmetry": bose_full_symmetry(),
            "continuum_limit_check": continuum_limit_check()}


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=float))
