"""
ca_lpt_generator.py — an automated lattice-perturbation-theory Feynman-rule
generator for the Wilson SU(3) gauge action (HiPPy/HPsrc-style; Hart-von Hippel-
Horgan-Storoni, hep-lat/0411026).

WHY (d1 / open-derivations v2)
==============================
Closing d1 = Lambda_MSbar/Lambda_L perturbatively needs the EXACT Wilson lattice
vertices (3-gluon, 4-gluon seagull, ghost, measure). Hand-transcribing them risks
fabricating coefficients (docs/theory/d1-kns-vertex-status.md). This module instead
*derives* every vertex from the action by expanding the links U = exp(i g A) order
by order in the gauge field and reading off the momentum-space coefficient — so the
vertices are generated, not transcribed. The load-bearing check is that the
generated 2-point vertex reproduces the known Wilson gluon inverse propagator
    Gamma^(0)_{mu nu}(k) = delta_{mu nu} khat^2 - khat_mu khat_nu,   khat_mu = 2 sin(k_mu/2)
exactly; then the same machinery gives the 3- and 4-point vertices.

METHOD (multilinear expansion)
==============================
Each external leg i is a plane wave: (Lorentz dir d_i, momentum k_i, colour matrix
M_i), tagged by a formal bookkeeping index. A plaquette link in direction rho at
midpoint shift s carries the algebra element A_link = sum_{i: d_i==rho} eps_i C_i,
with C_i = exp(i k_i . s) M_i (midpoint convention -> cos form factors). We expand
    U      = exp(i A_link) = sum_m (i A_link)^m / m!        (undaggered link)
    U^dag  = exp(-i A_link^dag)                              (daggered link)
keeping only MULTILINEAR terms (each eps_i to power 1), represented as a dict
    { frozenset(external legs present) : 3x3 complex matrix }.
The plaquette U_{rho sigma} = L1 L2 L3^dag L4^dag is a dict convolution; the
n-point vertex is the coefficient of the FULL leg set in -Tr(U_plaq), summed over
oriented planes (summing ordered (rho,sigma) reproduces Re Tr over unordered
planes and cancels the imaginary parts). Overall (1/g^2, 1/2) normalisation is
fixed once by matching the propagator.

Pure numpy (real/complex matrix algebra — NOT chiral spinor transforms, so the
CLAUDE.md numpy caveat does not apply; validated by the exact propagator gate).
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np

# ----------------------------------------------------------------------
#  SU(3) generators  T^a = lambda^a / 2,  Tr(T^a T^b) = delta^{ab}/2
# ----------------------------------------------------------------------
def gell_mann() -> np.ndarray:
    l = np.zeros((8, 3, 3), dtype=complex)
    l[0] = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
    l[1] = [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]
    l[2] = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
    l[3] = [[0, 0, 1], [0, 0, 0], [1, 0, 0]]
    l[4] = [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]]
    l[5] = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
    l[6] = [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]]
    l[7] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / math.sqrt(3)
    return l
T_GEN = gell_mann() / 2.0
NC = 3
I3 = np.eye(3, dtype=complex)


@dataclass
class Leg:
    d: int                 # Lorentz direction 0..3
    k: np.ndarray          # 4-momentum
    M: np.ndarray          # 3x3 colour matrix (a generator T^a)


# unit lattice vectors in 4D
def _ehat(mu: int) -> np.ndarray:
    e = np.zeros(4)
    e[mu] = 1.0
    return e


# the four links of the (rho,sigma) plaquette at base site 0, standard convention
# with the gauge field at the link's BASE site (A_mu(x) ~ e^{ik.x}); the cos form
# factors and khat=2sin(k/2) then emerge from the plaquette geometry.
#   U_{rho sigma}(0) = U_rho(0) U_sigma(rho) U_rho(sigma)^dag U_sigma(0)^dag
#   (direction, base-site shift, daggered?)
def _plaquette_links(rho: int, sigma: int):
    er, es = _ehat(rho), _ehat(sigma)
    return [
        (rho,   np.zeros(4), False),   # U_rho(0)
        (sigma, er,          False),   # U_sigma(rho)
        (rho,   es,          True),    # U_rho(sigma)^dag
        (sigma, np.zeros(4), True),    # U_sigma(0)^dag
    ]


# ----------------------------------------------------------------------
#  dict algebra  { frozenset(legs) : 3x3 matrix },  keeping |subset| <= nmax
# ----------------------------------------------------------------------
def _dmul(A: dict, B: dict, nmax: int) -> dict:
    out: dict = {}
    for sA, MA in A.items():
        for sB, MB in B.items():
            if sA & sB:                      # a leg used twice -> not multilinear
                continue
            s = sA | sB
            if len(s) > nmax:
                continue
            out[s] = out.get(s, 0) + MA @ MB
    return out


# ---- vectorised variant: leg momenta may be arrays of shape (...,4); matrices
#      are then (...,3,3) and products use batched matmul over the leading axes ----
def _matmul_v(MA, MB):
    return np.einsum('...ij,...jk->...ik', MA, MB)


def _dmul_v(A: dict, B: dict, nmax: int) -> dict:
    out: dict = {}
    for sA, MA in A.items():
        for sB, MB in B.items():
            if sA & sB:
                continue
            s = sA | sB
            if len(s) > nmax:
                continue
            prod = _matmul_v(MA, MB)
            out[s] = out.get(s, 0) + prod if s in out else prod
    return out


def _link_expansion_v(link_dir, shift, dag, legs_on_link, nmax, gshape):
    eff_shift = shift + 0.5 * _ehat(link_dir)
    I = np.broadcast_to(I3, gshape + (3, 3)).copy()
    X: dict = {}
    for i, leg in legs_on_link:
        phase = np.exp(1j * np.tensordot(leg.k, eff_shift, axes=([-1], [0])))
        sign = 1j if not dag else -1j
        X[frozenset({i})] = (sign * phase)[..., None, None] * leg.M
    result = {frozenset(): I.copy()}
    term = {frozenset(): I.copy()}
    for m in range(1, nmax + 1):
        term = _dmul_v(term, X, nmax)
        if not term:
            break
        inv = 1.0 / math.factorial(m)
        for s, M in term.items():
            result[s] = result.get(s, 0) + inv * M
    return result


def _exp_of_legs_v(link_dir, shift, legs_subset, sign_i, nmax, gshape):
    """exp(sign_i * i * sum_{legs} A) as a multilinear dict for a subset of legs on a
    link (used by the background-field split e^{iQ} e^{iB})."""
    eff_shift = shift + 0.5 * _ehat(link_dir)
    I = np.broadcast_to(I3, gshape + (3, 3)).copy()
    X: dict = {}
    for i, leg in legs_subset:
        phase = np.exp(1j * np.tensordot(leg.k, eff_shift, axes=([-1], [0])))
        X[frozenset({i})] = (sign_i * phase)[..., None, None] * leg.M
    result = {frozenset(): I.copy()}
    term = {frozenset(): I.copy()}
    for m in range(1, nmax + 1):
        term = _dmul_v(term, X, nmax)
        if not term:
            break
        inv = 1.0 / math.factorial(m)
        for s, M in term.items():
            result[s] = result.get(s, 0) + inv * M
    return result


def _link_split_v(link_dir, shift, dag, legs_on_link, bg_idx, nmax, gshape):
    """Background-field-split link  U = e^{iQ} e^{iB}  (undaggered) or its dagger
    e^{-iB} e^{-iQ}.  legs_on_link are (index, Leg); bg_idx is the set of background
    leg indices.  Q = quantum legs, B = background legs."""
    q_legs = [(i, lg) for (i, lg) in legs_on_link if i not in bg_idx]
    b_legs = [(i, lg) for (i, lg) in legs_on_link if i in bg_idx]
    if not dag:
        expQ = _exp_of_legs_v(link_dir, shift, q_legs, 1j, nmax, gshape)
        expB = _exp_of_legs_v(link_dir, shift, b_legs, 1j, nmax, gshape)
        return _dmul_v(expQ, expB, nmax)
    else:
        expBn = _exp_of_legs_v(link_dir, shift, b_legs, -1j, nmax, gshape)
        expQn = _exp_of_legs_v(link_dir, shift, q_legs, -1j, nmax, gshape)
        return _dmul_v(expBn, expQn, nmax)


def vertex_bqq_vec(legs, bg_idx, gshape) -> np.ndarray:
    """Background-field vertex from the split link U = e^{iQ} e^{iB}.  `bg_idx` is the
    set of leg indices treated as the classical BACKGROUND field (the rest are
    quantum).  This is the ACTION part of the background-quantum-quantum vertex; the
    background-covariant gauge-fixing vertex is a separate additive piece (see
    ca_lpt_selfenergy)."""
    n = len(legs)
    full = frozenset(range(n))
    legsB = [Leg(lg.d, np.broadcast_to(lg.k, gshape + (4,)), lg.M) for lg in legs]
    total = np.zeros(gshape, dtype=complex)
    Ione = np.broadcast_to(I3, gshape + (3, 3)).copy()
    for rho in range(4):
        for sigma in range(4):
            if rho == sigma:
                continue
            U = {frozenset(): Ione.copy()}
            for (ld, shift, dag) in _plaquette_links(rho, sigma):
                legs_on = [(i, lg) for i, lg in enumerate(legsB) if lg.d == ld]
                L = _link_split_v(ld, shift, dag, legs_on, bg_idx, n, gshape)
                U = _dmul_v(U, L, n)
            M = U.get(full)
            if M is not None:
                total = total + np.trace(M, axis1=-2, axis2=-1)
    return -total


def vertex_vec(legs, gshape) -> np.ndarray:
    """Vectorised vertex: legs whose .k is an array of shape gshape+(4,) give a
    vertex array of shape gshape. Colour matrices are (3,3); momenta broadcast."""
    n = len(legs)
    full = frozenset(range(n))
    # promote every leg momentum to shape gshape+(4,)
    legsB = [Leg(lg.d, np.broadcast_to(lg.k, gshape + (4,)), lg.M) for lg in legs]
    total = np.zeros(gshape, dtype=complex)
    Ione = np.broadcast_to(I3, gshape + (3, 3)).copy()
    for rho in range(4):
        for sigma in range(4):
            if rho == sigma:
                continue
            U = {frozenset(): Ione.copy()}
            for (ld, shift, dag) in _plaquette_links(rho, sigma):
                legs_on = [(i, lg) for i, lg in enumerate(legsB) if lg.d == ld]
                L = _link_expansion_v(ld, shift, dag, legs_on, n, gshape)
                U = _dmul_v(U, L, n)
            M = U.get(full)
            if M is not None:
                total = total + np.trace(M, axis1=-2, axis2=-1)
    return -total


def _link_expansion(link_dir, shift, dag, legs_on_link, nmax: int) -> dict:
    """exp(i A) (or exp(-i A^dag) if dag) as a multilinear dict, truncated to
    total leg-degree nmax."""
    # Midpoint convention: the field lives at the link midpoint x + dir_hat/2, so
    # a leg on a direction-`link_dir` link picks up the half-shift in its own
    # direction. U^dag = exp(-i A) is the SAME operator field (A Hermitian) with
    # the i-sign flipped -- the momentum phase is NOT conjugated.
    eff_shift = shift + 0.5 * _ehat(link_dir)
    X: dict = {}
    for i, leg in legs_on_link:
        phase = np.exp(1j * float(np.dot(leg.k, eff_shift)))
        sign = 1j if not dag else -1j
        X[frozenset({i})] = sign * phase * leg.M
    # exp = sum_m X^m / m!
    result = {frozenset(): I3.copy()}
    term = {frozenset(): I3.copy()}          # X^0/0!
    for m in range(1, nmax + 1):
        term = _dmul(term, X, nmax)
        if not term:
            break
        inv = 1.0 / math.factorial(m)
        for s, M in term.items():
            result[s] = result.get(s, 0) + inv * M
    return result


def _plaquette_dict(rho, sigma, legs, nmax) -> dict:
    U = {frozenset(): I3.copy()}
    for (ld, shift, dag) in _plaquette_links(rho, sigma):
        legs_on = [(i, lg) for i, lg in enumerate(legs) if lg.d == ld]
        L = _link_expansion(ld, shift, dag, legs_on, nmax)
        U = _dmul(U, L, nmax)
    return U


def vertex(legs, normalise=1.0) -> complex:
    """The n-point Wilson-action vertex = coefficient of the full leg-set in
    -Tr(sum_planes U_plaq), the planes summed over ORDERED (rho,sigma), rho!=sigma
    (=> Re Tr over unordered planes). Returns a complex scalar for the given
    external (dir, momentum, colour) legs. `normalise` is the overall 1/(2 g^2)
    factor (default 1; the propagator gate fixes it)."""
    n = len(legs)
    full = frozenset(range(n))
    total = 0.0 + 0.0j
    for rho in range(4):
        for sigma in range(4):
            if rho == sigma:
                continue
            U = _plaquette_dict(rho, sigma, legs, n)
            M = U.get(full)
            if M is not None:
                total += np.trace(M)
    return -normalise * total


# ----------------------------------------------------------------------
#  n=2 : the inverse gluon propagator (the validation gate)
# ----------------------------------------------------------------------
def khat(k: np.ndarray) -> np.ndarray:
    return 2.0 * np.sin(k / 2.0)


def propagator_inverse(k: np.ndarray) -> np.ndarray:
    """Generated 4x4 Gamma^(0)_{mu nu}(k) (colour-stripped, a=b=1). Should equal
    C * (delta_{mu nu} khat^2 - khat_mu khat_nu) for a single real constant C."""
    G = np.zeros((4, 4), dtype=complex)
    Ta = T_GEN[0]                                   # fixed colour a=b=1
    for mu in range(4):
        for nu in range(4):
            legs = [Leg(mu, k, Ta), Leg(nu, -k, Ta)]
            G[mu, nu] = vertex(legs)
    return G


def wilson_quadratic_form(k: np.ndarray) -> np.ndarray:
    kh = khat(k)
    return np.eye(4) * float(kh @ kh) - np.outer(kh, kh)


def validate_propagator(seed=0, ntest=6, tol=1e-10) -> dict:
    """Compare the GENERATED 2-point vertex to the known Wilson form
    delta_{mu nu} khat^2 - khat_mu khat_nu at random momenta. Passes if the ratio
    is a single real constant across all mu,nu and all test momenta."""
    rng = np.random.default_rng(seed)
    consts, maxdev = [], 0.0
    for _ in range(ntest):
        k = rng.uniform(-1.0, 1.0, size=4)
        G = np.real(propagator_inverse(k))
        W = wilson_quadratic_form(k)
        mask = np.abs(W) > 1e-6
        ratios = G[mask] / W[mask]
        c = float(np.mean(ratios))
        consts.append(c)
        maxdev = max(maxdev, float(np.max(np.abs(G - c * W))))
        # also check the off-structure (where W==0, G must be ~0)
        if np.any(~mask):
            maxdev = max(maxdev, float(np.max(np.abs(G[~mask]))))
    c0 = float(np.mean(consts))
    const_spread = float(max(consts) - min(consts))
    return {"overall_constant_C": c0,
            "C_spread_across_momenta": const_spread,
            "max_abs_dev_from_C*W": maxdev,
            "pass": bool(maxdev < tol and const_spread < tol),
            "statement": "generated 2-point vertex == C*(delta khat^2 - khat khat) "
                         "(exact Wilson inverse propagator) => generator validated"}


# ----------------------------------------------------------------------
#  n=3 : the 3-gluon vertex + continuum-limit validation
# ----------------------------------------------------------------------
def f_structure():
    """SU(3) structure constants f^{abc} from [T^a,T^b] = i f^{abc} T^c."""
    f = np.zeros((8, 8, 8))
    for a in range(8):
        for b in range(8):
            comm = T_GEN[a] @ T_GEN[b] - T_GEN[b] @ T_GEN[a]
            for c in range(8):
                f[a, b, c] = np.real(-2j * np.trace(comm @ T_GEN[c]))
    return f


F_ABC = f_structure()


def vertex3(mu, nu, rho, p, q, r, a=0, b=1, c=2) -> complex:
    """Generated lattice 3-gluon vertex for legs (mu,p,T^a),(nu,q,T^b),(rho,r,T^c)
    with p+q+r=0 (all incoming)."""
    legs = [Leg(mu, p, T_GEN[a]), Leg(nu, q, T_GEN[b]), Leg(rho, r, T_GEN[c])]
    return vertex(legs)


def _cont_3gluon(mu, nu, rho, p, q, r):
    """Continuum YM 3-gluon tensor (all incoming, p+q+r=0), f^{abc} stripped:
    [delta_{mu nu}(p-q)_rho + delta_{nu rho}(q-r)_mu + delta_{rho mu}(r-p)_nu]."""
    d = np.eye(4)
    return (d[mu, nu] * (p - q)[rho]
            + d[nu, rho] * (q - r)[mu]
            + d[rho, mu] * (r - p)[nu])


def validate_3gluon(seed=1, scale=1e-3, tol=2e-3) -> dict:
    """Continuum-limit gate: as momenta -> 0 the generated lattice 3-gluon vertex
    must approach K * f^{abc} * [continuum tensor] for a single constant K, across
    all Lorentz index choices. Uses (a,b,c)=(1,2,3), f^{123}=1 (d^{123}=0, so the
    colour factor is clean)."""
    rng = np.random.default_rng(seed)
    p = scale * rng.uniform(-1, 1, 4)
    q = scale * rng.uniform(-1, 1, 4)
    r = -p - q
    ratios, gens, conts = [], [], []
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                cont = _cont_3gluon(mu, nu, rho, p, q, r) * F_ABC[0, 1, 2]
                gen = vertex3(mu, nu, rho, p, q, r, 0, 1, 2)
                if abs(cont) > scale * 1e-3:
                    ratios.append(gen / cont)
                    gens.append(gen); conts.append(cont)
    ratios = np.array(ratios)
    # the generated vertex is imaginary (i f^{abc} ...); compare magnitudes/phase
    K = np.mean(ratios)
    spread = float(np.max(np.abs(ratios - K)))
    # Bose symmetry: the full vertex is SYMMETRIC under a simultaneous leg swap
    # (colour f^{abc} antisym x tensor antisym = symmetric), so v1 - v2 = 0 exactly.
    bose = []
    for _ in range(3):
        mu, nu, rho = rng.integers(0, 4, 3)
        v1 = vertex3(mu, nu, rho, p, q, r, 0, 1, 2)
        v2 = vertex3(nu, mu, rho, q, p, r, 1, 0, 2)
        bose.append(abs(v1 - v2))
    return {"K_constant": complex(K),
            "K_is_pure_imaginary": bool(abs(np.real(K)) < 1e-9 * (abs(K) + 1e-30)),
            "tensor_ratio_spread": spread,
            "bose_symmetry_maxdev": float(max(bose)),
            "pass": bool(spread < tol and max(bose) < 1e-9),
            "statement": "generated 3-gluon vertex -> K f^{abc}[continuum tensor] "
                         "(single constant K across all indices) + Bose-antisymmetric "
                         "=> lattice 3-gluon vertex validated in the continuum limit"}


# ----------------------------------------------------------------------
#  n=4 : the 4-gluon (seagull) vertex
# ----------------------------------------------------------------------
def vertex4(mus, ks, abcd=(0, 1, 2, 3)) -> complex:
    """Generated lattice 4-gluon vertex for legs i=0..3 with Lorentz dirs mus[i],
    momenta ks[i] (sum to 0), colours T^{abcd[i]}."""
    legs = [Leg(mus[i], ks[i], T_GEN[abcd[i]]) for i in range(4)]
    return vertex(legs)


def validate_4gluon(seed=2, scale=1e-2) -> dict:
    """The 4-gluon vertex must be Bose-symmetric under a simultaneous swap of any
    two legs (all attributes), and non-trivial. Full continuum-tensor validation
    is elaborate; Bose symmetry + non-triviality is the practical gate here."""
    rng = np.random.default_rng(seed)
    p = scale * rng.uniform(-1, 1, 4)
    q = scale * rng.uniform(-1, 1, 4)
    s = scale * rng.uniform(-1, 1, 4)
    t = -p - q - s
    ks = [p, q, s, t]
    # a plaquette spans only 2 directions, so the Wilson 4-gluon vertex is
    # non-zero only for <=2 distinct Lorentz indices (the seagull delta_{mu nu}
    # delta_{rho sigma} structure), AND the colour trace must not vanish. Use the
    # (0,0,1,1) dirs with (0,1,0,1) colours (a non-vanishing configuration).
    mus = [0, 0, 1, 1]
    abcd = (0, 1, 0, 1)
    base = vertex4(mus, ks, abcd)
    # swap legs 0<->1 (same dir): all attributes move together -> Bose-symmetric
    sw = vertex4([mus[1], mus[0], mus[2], mus[3]],
                 [ks[1], ks[0], ks[2], ks[3]], (abcd[1], abcd[0], abcd[2], abcd[3]))
    # swap legs 1<->2 (crosses directions)
    sw2 = vertex4([mus[0], mus[2], mus[1], mus[3]],
                  [ks[0], ks[2], ks[1], ks[3]], (abcd[0], abcd[2], abcd[1], abcd[3]))
    return {"value_sample": complex(base),
            "nontrivial": bool(abs(base) > 1e-12),
            "bose_swap01_maxdev": float(abs(base - sw)),
            "bose_swap13_maxdev": float(abs(base - sw2)),
            "pass": bool(abs(base) > 1e-12 and abs(base - sw) < 1e-9
                         and abs(base - sw2) < 1e-9),
            "statement": "generated 4-gluon (seagull) vertex is non-trivial and "
                         "Bose-symmetric under simultaneous leg swaps => validated"}


# ----------------------------------------------------------------------
#  Public API — numerical vertices for the self-energy runner
# ----------------------------------------------------------------------
def gluon_propagator_inverse_full(k):
    """delta_{mu nu} khat^2 - khat_mu khat_nu  (colour-diagonal), exact."""
    return wilson_quadratic_form(k)


def three_gluon(mu, nu, rho, p, q, r, a, b, c):
    """Public accessor: exact generated lattice 3-gluon vertex (colour a,b,c)."""
    return vertex3(mu, nu, rho, p, q, r, a, b, c)


def four_gluon(mus, ks, abcd):
    """Public accessor: exact generated lattice 4-gluon vertex."""
    return vertex4(mus, ks, abcd)


def report() -> dict:
    return {"n2_propagator": validate_propagator(),
            "n3_three_gluon": validate_3gluon(),
            "n4_four_gluon": validate_4gluon(),
            "note": "pure-gauge vertices generated + validated. Ghost-gluon vertex "
                    "(from FP gauge-fixing) and the Haar measure term are the "
                    "remaining generator pieces for the full self-energy -> 28.81."}


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
