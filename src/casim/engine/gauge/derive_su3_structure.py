"""derive_su3_structure.py — deriving the STRUCTURE of the colour gauge field
from the model as it stands (completeness rubric row **B1**, colour leg).

THE QUESTION, AND WHAT WOULD COUNT AS AN ANSWER
===============================================
`docs/status/completeness-2026-08-07.md` row B1 reads:

    | B1 | Origin of SU(3)xSU(2)_L xU(1)_Y | PARTIAL | ... | SU(3)_c imposed |
    | ... $SU(2)_L$ derived by beta-gauging the complex-mass step; $U(1)_Y$ from
    | bipartite sublattice parity; ... **Colour is still put in** |

"Put in" is a bundle of at least six separate impositions, and they are not
equally hard:

  (i)   the quark carries an internal index at all;
  (ii)  the index has dimension 3;
  (iii) its invariance group is *unitary*;
  (iv)  the group is *special* unitary -- SU(3), not U(3);
  (v)   the symmetry is *local*, so it carries a connection (the gluon);
  (vi)  the coupling is *vector-like*, where SU(2)_L's is chiral.

This module attacks (iii)-(vi) and, secondarily, (ii).  It does NOT attack
(i), and says so in its own verdict: the existence of the index is the
residual input, and it is the honest headline.

WHAT IS DERIVED HERE (each is a CHECKS row, each has a control)
===============================================================
S1  **Colour cannot be chiral, and SU(2) can.**  The symmetric anomaly
    coefficient A^{abc} = 2 Tr(T^a{T^b,T^c}) vanishes for EVERY triple of
    SU(2) generators -- exactly, over Q[i] -- and does NOT vanish for SU(3)
    (witness A^{888} = -1/sqrt(3), exact).  A single chiral triplet is
    therefore inconsistent, while a single chiral doublet is fine.  So the
    model's own chiral/vector split is not two independent choices: given
    that the weak group is SU(2) and the colour group is SU(3), the first
    MAY be chiral and the second MUST be vector-like.

S2  **... hence the gluon's even propagation law is FORCED.**  F91 G1 proved
    "vector-like => branch-scalar coupling => even law", but recorded the
    vector-like assignment itself as `by construction` and the BCC gluon's
    even law as **unforced** (F91: "the assignment is unforced ... the
    elegant-design philosophy select[s] the even law").  S1 supplies the
    missing premise, so the branch-space coupling matrix diag(g_L,g_R) has
    identically zero traceless part and F91's chain closes.  The contrast
    leg measures what a chiral colour would have cost: a nonzero branch
    split on the body diagonal.

S3  **Locality forces the connection.**  A cellular automaton has no global
    operations: its rule is one operator applied at every cell, so it
    commutes with a *site-dependent* internal rotation V(x) exactly as well
    as with a constant one -- measured at 0.0 for the on-site (mass) step.
    The hopping step is different, because it compares amplitudes at two
    cells: without a compensator its residual is O(1).  Introducing
    U_mu(x) -> V(x) U_mu(x) V^dag(x+mu) restores exact covariance.  The
    gluon field is therefore not added to the model, it is the price of the
    rule being local -- and the SAME argument explains why F27's U(x) needs
    no compensator and is pure gauge.

S4  **Unitarity fixes the group to U(N).**  The rule acts on the internal
    factor as the identity (that is what "internal" MEANS), so the model's
    own two steps generate R (x) 1_N.  The commutant of that algebra is
    computed, not assumed: dim = N^2, i.e. the full matrix algebra M_N, whose
    norm-preserving subgroup is exactly U(N).  A corollary is a prediction
    rather than an input: the spectrum is exactly N-fold degenerate.

S5  **U(N) -> SU(N): the trace part cannot be gauged.**  The U(1) subgroup of
    U(N_c) assigns one colour-blind charge to every quark and none to any
    lepton.  Against the model's OWN hypercharge nullspace (F279/F293,
    re-used here rather than re-derived) the mixed anomaly [SU(2)_L]^2 U(1)
    is *identically zero in N_c* for Y and equal to N_c*b/2 for the colour
    trace.  It is nonzero precisely BECAUSE SU(2)_L is chiral -- i.e. the
    model's derived F27 chirality is what removes the trace.  Every other
    colour anomaly vanishes identically because S1 made colour vector-like.

S6  **The multiplicity, given three-quark baryons.**  A totally antisymmetric
    3-index invariant of SU(N) exists iff N = 3 -- computed as the joint
    kernel of the total generators on Lambda^3(C^N), which is 1-dimensional
    at N=3 and 0-dimensional at N=2,4,5,6.  With Fermi statistics DERIVED
    (F289) rather than imported, and a symmetric space (x) spin (x) flavour
    ground state, this is an upper AND lower bound at once.  It consumes one
    empirical input -- that baryons are three-constituent states -- and is
    labelled so.  It is NOT one of B10's three closed routes (anomaly,
    spatial-3, Z_3) and does not touch them.

S7  **Eight gluons.**  dim su(N) = N^2 - 1 = 8 at N = 3, and the algebra
    closes on the tree's own structure constants (F43).

WHAT IS NOT DERIVED, STATED BEFORE THE RESULTS
==============================================
The existence of the internal index (impositions (i)) is an INPUT.  Nothing
here produces it.  What changes is that everything downstream of it is no
longer independent: grant the model one internal index that its rule does not
read, and the group, its locality, its connection, its representation, its
vector-like coupling and its gluon count all follow.

Cross-references: F27 (beta-gauging; U(x) pure gauge), F91 (the pairing
classification, whose one unforced assignment S1/S2 closes), F68 (the
even-channel argument), F279/F293 (the hypercharge nullspace, imported),
F298 (the independent structural N_c <= 3), F289 (derived Fermi statistics),
F43 (f^{abc}, the octet), F31/F110 (covariant hopping, Gauss law).
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence, Tuple

from casim.numerics import xp as np   # D8: never numpy directly
import sympy as sp

from casim.engine.gauge import strong as cstrong


# ==========================================================================
# Generators of su(N): exact (sympy) and float (numpy)
# ==========================================================================
def su_n_generators_exact(n: int) -> List[sp.Matrix]:
    """T^a for su(n), normalised Tr(T^a T^b) = delta^{ab}/2, exact.

    Standard basis: symmetric off-diagonal, antisymmetric off-diagonal, and
    the (n-1) diagonal Cartan elements.  Built here rather than imported so
    that the SU(2)/SU(3) contrast in S1 is not inherited from the module it
    is meant to be a statement about.
    """
    gens: List[sp.Matrix] = []
    for j in range(n):
        for k in range(j + 1, n):
            m = sp.zeros(n, n)
            m[j, k] = sp.Rational(1, 2)
            m[k, j] = sp.Rational(1, 2)
            gens.append(m)
            m = sp.zeros(n, n)
            m[j, k] = -sp.I / 2
            m[k, j] = sp.I / 2
            gens.append(m)
    for m_idx in range(1, n):
        diag = [sp.Integer(1)] * m_idx + [sp.Integer(-m_idx)] + [sp.Integer(0)] * (n - m_idx - 1)
        norm = sp.sqrt(sp.Rational(1, 2) / sp.Rational(m_idx * (m_idx + 1), 2))
        mat = sp.diag(*diag) * norm / sp.sqrt(2) * sp.sqrt(2)
        # normalisation: Tr(T^2) = (m + m^2) * c^2 = 1/2  =>  c = sqrt(1/(2 m (m+1)))
        c = sp.sqrt(sp.Rational(1, 2) / sp.Integer(m_idx * (m_idx + 1)))
        mat = sp.diag(*diag) * c
        gens.append(mat)
    return gens


def su_n_generators(n: int) -> np.ndarray:
    """Float version of :func:`su_n_generators_exact`, shape (n^2-1, n, n)."""
    return np.array([np.array(g.evalf(), dtype=complex)
                     for g in su_n_generators_exact(n)])


def generator_normalisation_residual(n: int) -> float:
    """max | Tr(T^a T^b) - delta^{ab}/2 | -- the basis is checked, not trusted."""
    T = su_n_generators(n)
    g = np.einsum('aij,bji->ab', T, T)
    return float(np.max(np.abs(g - 0.5 * np.eye(len(T)))))


# ==========================================================================
# S1 -- the symmetric anomaly coefficient: SU(2) may be chiral, SU(3) may not
# ==========================================================================
def anomaly_coefficients_exact(n: int) -> Dict[str, Any]:
    """A^{abc} = 2 Tr(T^a {T^b, T^c}) over every triple, exactly.

    For su(2) every entry is exactly 0 (there is no symmetric invariant), so a
    single chiral doublet is anomaly-free.  For su(3) it is not.
    """
    gens = su_n_generators_exact(n)
    ng = len(gens)
    worst = sp.Integer(0)
    nonzero: List[Tuple[int, int, int, Any]] = []
    all_zero = True
    for a in range(ng):
        for b in range(ng):
            for c in range(ng):
                anti = gens[b] * gens[c] + gens[c] * gens[b]
                val = sp.expand(2 * (gens[a] * anti).trace())
                val = sp.nsimplify(sp.simplify(val))
                if val != 0:
                    all_zero = False
                    if len(nonzero) < 8:
                        nonzero.append((a, b, c, val))
                    if sp.Abs(val) > sp.Abs(worst):
                        worst = val
    return {"n": n, "n_generators": ng, "n_triples": ng ** 3,
            "all_exactly_zero": bool(all_zero),
            "sample_nonzero": [(a, b, c, str(v)) for a, b, c, v in nonzero],
            "largest_magnitude": str(worst)}


def anomaly_witness_exact(n: int) -> Dict[str, Any]:
    """One exact nonzero witness A^{ddd} on the last Cartan generator.

    Cheap where the full
    :func:`anomaly_coefficients_exact` scan is not: at n = 3 this is
    A^{888} = -1/sqrt(3), the standard d^{888}.
    """
    gens = su_n_generators_exact(n)
    t = gens[-1]
    val = sp.simplify(sp.expand(4 * (t * t * t).trace()))
    # compared EXACTLY, not against a float literal: at n = 3 this is the
    # standard d^{888} = -1/sqrt(3).
    target = -1 / sp.sqrt(sp.Integer(n))
    return {"n": n, "generator": "last Cartan (a = n^2-1)",
            "A_ddd": str(val), "is_zero": bool(sp.simplify(val) == 0),
            "equals_minus_one_over_sqrt_n": bool(sp.simplify(val - target) == 0),
            "A_ddd_float": float(sp.N(val))}


def anomaly_coefficients_float_max(n: int) -> float:
    """max |A^{abc}| over all triples, in floats (for n where exact is slow)."""
    T = su_n_generators(n)
    anti = np.einsum('bij,cjk->bcik', T, T) + np.einsum('cij,bjk->bcik', T, T)
    A = 2.0 * np.einsum('aij,bcji->abc', T, anti)
    return float(np.max(np.abs(A)))


def chirality_assignment_table(n: int = 3) -> Dict[str, Any]:
    """Anomaly of candidate colour assignments: A_L - A_R.

    A gauge assignment is consistent iff the total symmetric anomaly cancels.
    Rows:
        vector-like   L = fundamental, R = fundamental   -> 0 identically
        chiral        L = fundamental, R = singlet       -> A(fund)
        conjugate     L = fundamental, R = antifund      -> 2 A(fund)
    Only the first survives, so colour is vector-like -- FORCED, where F91
    recorded it as `by construction`.
    """
    T = su_n_generators(n)
    anti = np.einsum('bij,cjk->bcik', T, T) + np.einsum('cij,bjk->bcik', T, T)
    A_fund = 2.0 * np.einsum('aij,bcji->abc', T, anti)
    A_anti = -A_fund                      # A(Rbar) = -A(R)
    zero = np.zeros_like(A_fund)
    rows = [
        {"assignment": "vector-like  (L=3, R=3)",
         "max_abs_anomaly": float(np.max(np.abs(A_fund - A_fund))),
         "consistent": True},
        {"assignment": "chiral       (L=3, R=1)",
         "max_abs_anomaly": float(np.max(np.abs(A_fund - zero))),
         "consistent": bool(np.max(np.abs(A_fund)) < 1e-14)},
        {"assignment": "conjugate    (L=3, R=3bar)",
         "max_abs_anomaly": float(np.max(np.abs(A_fund - A_anti))),
         "consistent": bool(np.max(np.abs(A_fund - A_anti)) < 1e-14)},
    ]
    n_consistent = sum(1 for r in rows if r["consistent"])
    return {"n": n, "rows": rows, "n_consistent": n_consistent,
            "only_vector_like_survives": bool(n_consistent == 1
                                              and rows[0]["consistent"])}


# ==========================================================================
# S2 -- branch structure of the coupling: the even law, now forced
# ==========================================================================
def branch_coupling_traceless_part(g_L: float, g_R: float) -> float:
    """|| traceless part of diag(g_L, g_R) || in branch space.

    F68/F91: the propagation channel is set by the branch structure of the
    coupling.  A branch SCALAR (traceless part 0) can only source the
    helicity-symmetric even law.  S1 forces g_L = g_R for colour.
    """
    c = np.diag([g_L, g_R]).astype(complex)
    traceless = c - 0.5 * np.trace(c) * np.eye(2)
    return float(np.linalg.norm(traceless))


def branch_split_on_body_diagonal(k: float = 0.4) -> Dict[str, float]:
    """The dispersion split a chiral colour assignment would have cost.

    Uses the model's own BCC dispersion (weak_wmu), evaluated on the body
    diagonal where the two chiral branches separate maximally.  Returns
    |Omega^+ - Omega_even| = |Delta Omega| / 2 (the F67/F91 separation).
    """
    from casim.engine.gauge import weak_wmu as cw
    kk = np.array([[[k / math.sqrt(3.0)]]])
    om_even = float(cw._omega_even(kk, kk, kk)[0, 0, 0])
    om_p = 2.0 * float(cw.bcc_dispersion(kk / 2.0, kk / 2.0, kk / 2.0,
                                         sign='+')[0, 0, 0])
    om_m = 2.0 * float(cw.bcc_dispersion(kk / 2.0, kk / 2.0, kk / 2.0,
                                         sign='-')[0, 0, 0])
    return {"k": k, "Omega_even": om_even, "Omega_plus": om_p,
            "Omega_minus": om_m,
            "split_plus_vs_even": abs(om_p - om_even),
            "half_delta_Omega": abs(om_p - om_m) / 2.0,
            "identity_residual": abs(abs(om_p - om_even)
                                     - abs(om_p - om_m) / 2.0)}


# ==========================================================================
# S3 -- locality forces the connection
# ==========================================================================
def _haar_su(n: int, rng: np.random.Generator) -> np.ndarray:
    z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / math.sqrt(2)
    q, r = np.linalg.qr(z)
    q = q * (np.diag(r) / np.abs(np.diag(r)))
    return q / np.linalg.det(q) ** (1.0 / n)


def locality_forces_connection(n: int = 3, L: int = 12, seed: int = 20260816,
                               use_compensator: bool = True) -> Dict[str, Any]:
    """The forcing argument, on a minimal 1-D ring with an internal index.

    Three legs:

      (a) ON-SITE step.  A CA rule is ONE operator applied at every cell, so a
          site-dependent V(x) acting on an index the operator does not read
          commutes with it exactly.  This is why a local symmetry is free in a
          CA -- and why F27's U(x) needs no compensator and is pure gauge.

      (b) HOPPING step, no compensator.  The hop compares amplitudes at x and
          x+1, which V(x) and V(x+1) rotate differently.  Covariance FAILS at
          O(1).

      (c) HOPPING step, with U(x) transforming as V(x) U(x) V^dag(x+1).
          Covariance is exact.  The connection is the price of locality.

    ``use_compensator=False`` is the declared control: leg (c) must go red,
    because a covariance test that passes without the link variable has not
    tested the forcing.
    """
    rng = np.random.default_rng(seed)
    d = 4                                              # branch (x) spin
    psi = (rng.normal(size=(L, d, n)) + 1j * rng.normal(size=(L, d, n)))
    V = np.array([_haar_su(n, rng) for _ in range(L)])
    U = np.array([_haar_su(n, rng) for _ in range(L)])

    # a random on-site operator that acts on the Dirac factor only
    M = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    M = M + M.conj().T

    def rot(field):
        return np.einsum('xij,xdj->xdi', V, field)

    def onsite(field):
        return np.einsum('de,xen->xdn', M, field)

    def bare_hop(field):
        return np.roll(field, -1, axis=0)

    def cov_hop(field, links):
        return np.einsum('xij,xdj->xdi', links, np.roll(field, -1, axis=0))

    nrm = np.linalg.norm(psi)

    a_res = np.linalg.norm(onsite(rot(psi)) - rot(onsite(psi))) / nrm

    b_res = np.linalg.norm(bare_hop(rot(psi)) - rot(bare_hop(psi))) / nrm

    if use_compensator:
        U_t = np.einsum('xij,xjk,xkl->xil', V, U,
                        np.conj(np.transpose(np.roll(V, -1, axis=0), (0, 2, 1))))
    else:
        U_t = U.copy()                                  # control: no transform
    c_res = np.linalg.norm(cov_hop(rot(psi), U_t) - rot(cov_hop(psi, U))) / nrm

    return {"n": n, "L": L, "use_compensator": bool(use_compensator),
            "onsite_commutes_residual": float(a_res),
            "bare_hop_covariance_residual": float(b_res),
            "covariant_hop_residual": float(c_res),
            "connection_parameters_per_link": n * n - 1}


def locality_forces_connection_tree(seed: int = 20260816,
                                    use_compensator: bool = True
                                    ) -> Dict[str, Any]:
    """The same three legs run through the TREE's own SU(3) operators.

    Uses `casim.engine.gauge.strong`'s quark field, links and gauge
    transformations, so the statement is about the model's implemented colour
    sector and not about a toy written to make it true.
    """
    rng = np.random.default_rng(seed)
    shape = (8, 8)
    q = cstrong.gaussian_quark(shape, flavour='u', colour='r', sigma=2.0)
    U = cstrong.random_su3_links_2d(shape, rng=rng)
    Vf = np.array([[_haar_su(3, rng) for _ in range(shape[1])]
                   for _ in range(shape[0])])

    def norm(field):
        return math.sqrt(sum(float(np.sum(np.abs(v) ** 2))
                             for v in field.values()))

    def diff(f1, f2):
        return math.sqrt(sum(float(np.sum(np.abs(f1[k] - f2[k]) ** 2))
                             for k in f1))

    nq = norm(q)
    qV = cstrong.gauge_transform_quark(q, Vf)
    U_t = (cstrong.gauge_transform_links(U, Vf) if use_compensator
           else U.copy())

    cold = cstrong.cold_links_2d(shape)
    bare_lhs = cstrong.covariant_shift(qV, cold, 0, '+')
    bare_rhs = cstrong.gauge_transform_quark(
        cstrong.covariant_shift(q, cold, 0, '+'), Vf)
    bare_res = diff(bare_lhs, bare_rhs) / nq

    cov_lhs = cstrong.covariant_shift(qV, U_t, 0, '+')
    cov_rhs = cstrong.gauge_transform_quark(
        cstrong.covariant_shift(q, U, 0, '+'), Vf)
    cov_res = diff(cov_lhs, cov_rhs) / nq

    return {"use_compensator": bool(use_compensator),
            "bare_shift_covariance_residual": float(bare_res),
            "covariant_shift_residual": float(cov_res)}


# ==========================================================================
# S4 -- the commutant is M_N, so the group is U(N)
# ==========================================================================
def _f27_mass_step(m: float, theta: float) -> np.ndarray:
    """The F27 mass step on (branch (x) spin), re-typed from the finding.

    M = cos(m) 1_4 + i sin(m) [[0, U],[U^dag, 0]] (x) 1_spin, with the F27
    single-flavour U = e^{i theta}.  Re-typed rather than imported so the
    commutant below is not a statement about one particular code path.
    """
    c, s = math.cos(m), math.sin(m)
    A = np.array([[0.0, np.exp(1j * theta)],
                  [np.exp(-1j * theta), 0.0]], dtype=complex)
    return np.kron(c * np.eye(2) + 1j * s * A, np.eye(2))


def _bcc_walk(kx: float, ky: float, kz: float) -> np.ndarray:
    """The model's own BCC walk on (branch (x) spin), re-typed from Paper 1 Eq. 15.

    Per branch the update is A_s(k) = u_s(k) 1_2 + i n~_s(k) . sigma, with
    u = c_x c_y c_z +- s_x s_y s_z and the sign-corrected Bloch vector carried
    by `casim.engine.lattice.time_signature.bcc_bloch` and
    `casim.engine.lattice.dimensionality.bloch_vector`.  The two branches are
    the two signs.

    Re-typed rather than imported (the F313 precedent), and its UNITARITY is
    asserted downstream rather than assumed -- an unconstrained walk would make
    the commutant count meaningless, which is exactly the V-004 defect class.

    This is the step that mixes SPIN.  Without it the mass step and a
    branch-diagonal phase generate only M_2 (x) 1_spin, and the commutant is
    large for a trivial reason.
    """
    r3 = math.sqrt(3.0)
    c = [math.cos(k / r3) for k in (kx, ky, kz)]
    s = [math.sin(k / r3) for k in (kx, ky, kz)]
    sig_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sig_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sig_z = np.array([[1, 0], [0, -1]], dtype=complex)
    W = np.zeros((4, 4), dtype=complex)
    for slot, sg in enumerate((+1.0, -1.0)):
        u = c[0] * c[1] * c[2] + sg * s[0] * s[1] * s[2]
        n1 = s[0] * c[1] * c[2] - sg * c[0] * s[1] * s[2]
        n2 = -sg * c[0] * s[1] * c[2] + s[0] * c[1] * s[2]
        n3 = c[0] * c[1] * s[2] + sg * s[0] * s[1] * c[2]
        blk = u * np.eye(2) + 1j * (n1 * sig_x + n2 * sig_y + n3 * sig_z)
        W[2 * slot:2 * slot + 2, 2 * slot:2 * slot + 2] = blk
    return W


def walk_unitarity_residual(ks: Sequence[Tuple[float, float, float]] = (
        (0.3, 0.7, 1.1), (1.9, -0.4, 0.8), (-1.2, 2.15, 0.05))) -> float:
    """max || W(k)^dag W(k) - 1 || over probe momenta.

    The guard the F313 review's `check_C4b` lacked: if the re-typed walk were
    not unitary the whole S4 count would be about some other operator.
    """
    worst = 0.0
    for k in ks:
        W = _bcc_walk(*k)
        worst = max(worst, float(np.max(np.abs(W.conj().T @ W - np.eye(4)))))
    return worst


def _generated_algebra_dim(ops: Sequence[np.ndarray], dim: int,
                           tol: float = 1e-9) -> int:
    """Dimension of the *-algebra generated by ``ops`` (with the identity)."""
    basis: List[np.ndarray] = []

    def add(mat):
        v = mat.reshape(-1).copy()
        for b in basis:
            v = v - np.vdot(b, v) * b
        nv = np.linalg.norm(v)
        if nv > tol:
            basis.append(v / nv)
            return True
        return False

    add(np.eye(dim, dtype=complex))
    frontier = [np.eye(dim, dtype=complex)] + [np.asarray(o, dtype=complex)
                                               for o in ops]
    for o in ops:
        add(np.asarray(o, dtype=complex))
        add(np.asarray(o, dtype=complex).conj().T)
    changed = True
    while changed and len(basis) < dim * dim:
        changed = False
        current = [b.reshape(dim, dim) for b in basis]
        for x in current:
            for o in frontier:
                for prod in (x @ o, o @ x):
                    if add(prod):
                        changed = True
    return len(basis)


def commutant_of_the_rule(n: int = 3, n_k: int = 5,
                          rule_reads_colour: bool = False) -> Dict[str, Any]:
    """dim of the commutant of the rule on (Dirac 4) (x) (internal n).

    The rule's operators are R_i (x) 1_n: the model's mass step and its
    branch-diagonal walk at several momenta.  Two numbers are computed:

      * the dimension of the algebra the Dirac-factor operators GENERATE,
        which must be 16 = dim M_4 -- otherwise the commutant would be large
        for a trivial reason and the result would mean nothing;
      * the dimension of the commutant on the full 4n space, which comes out
        n^2 = dim M_n.  Its unitary elements are exactly U(n).

    ``rule_reads_colour=True`` is the declared control: let one Gell-Mann
    matrix into the rule and the index stops being internal -- the commutant
    collapses below n^2.
    """
    probe_k = [(0.3, 0.7, 1.1), (1.9, -0.4, 0.8), (-1.2, 2.15, 0.05),
               (0.9, 0.9, 0.9), (2.4, 1.3, -1.7)][:max(1, n_k)]
    dirac_ops = [_f27_mass_step(0.37, 0.0), _f27_mass_step(0.37, 1.1)]
    dirac_ops += [_bcc_walk(*k) for k in probe_k]
    gen_dim = _generated_algebra_dim(dirac_ops, 4)

    full = [np.kron(o, np.eye(n)) for o in dirac_ops]
    if rule_reads_colour:
        T = su_n_generators(n)
        full.append(np.kron(_bcc_walk(0.21, 0.55, 0.9), T[2] * 2.0))

    dim = 4 * n
    rows = []
    for o in full:
        rows.append(np.kron(o, np.eye(dim)) - np.kron(np.eye(dim), o.T))
    Mstack = np.concatenate(rows, axis=0)
    sv = np.linalg.svd(Mstack, compute_uv=False)
    tol = max(Mstack.shape) * (sv[0] if sv.size else 1.0) * 1e-12
    commutant_dim = int(np.sum(sv < tol)) + (dim * dim - sv.size)

    return {"n": n, "dirac_algebra_dim": int(gen_dim),
            "walk_unitarity_residual": walk_unitarity_residual(),
            "dirac_algebra_is_full_M4": bool(gen_dim == 16),
            "commutant_dim": commutant_dim,
            "expected_if_internal": n * n,
            "commutant_is_M_n": bool(commutant_dim == n * n),
            "rule_reads_colour": bool(rule_reads_colour),
            "group_from_unitarity": f"U({n})"}


def internal_index_degeneracy(n: int = 3) -> Dict[str, Any]:
    """A prediction, not an input: the spectrum is exactly n-fold degenerate.

    If the rule is R (x) 1_n then every eigenvalue of the rule has
    multiplicity a multiple of n, exactly.  This is what makes the index
    unobservable in the dispersion -- i.e. genuinely *internal*.
    """
    R = _f27_mass_step(0.41, 0.6) @ _bcc_walk(0.53, -0.29, 1.4)
    full = np.kron(R, np.eye(n))
    ev_R = np.linalg.eigvals(R)
    ev_full = np.linalg.eigvals(full)

    # multiset match, not a sort: conjugate pairs share a real part, so a
    # lexicographic sort of the two spectra is not a reliable comparison.
    worst = 0.0
    multiplicities = []
    for lam in ev_R:
        d = np.abs(ev_full - lam)
        multiplicities.append(int(np.sum(d < 1e-10)))
        worst = max(worst, float(np.min(d)))
    ok = all(mu == n for mu in multiplicities) and len(ev_full) == n * len(ev_R)
    return {"n": n,
            "degeneracy_residual": worst,
            "multiplicities": multiplicities,
            "every_level_is_n_fold": bool(ok),
            "n_distinct_expected": int(len(ev_R))}


# ==========================================================================
# S5 -- U(N) -> SU(N): the trace part is anomalous
# ==========================================================================
def trace_u1_is_anomalous() -> Dict[str, Any]:
    """[SU(2)_L]^2 U(1)_X for X = hypercharge vs X = the colour trace.

    Only LEFT-handed SU(2) doublets contribute (the model has no right-handed
    doublet -- F27's chirality).  With the F279/F293 nullspace ratios
    y_Q : y_L = 1 : -N_c, imported from `derive_ncolour` rather than
    re-derived:

        X = Y            ->  N_c * y_Q + y_L  ==  0    identically in N_c
        X = colour trace ->  N_c * b          !=  0    for any b != 0

    So the U(1) factor of U(N_c) cannot be gauged, and the colour group is the
    traceless part.  The reason it fails is that SU(2)_L is CHIRAL -- the
    model's own F27 result is what removes the trace.
    """
    from casim.engine.gauge.derive_ncolour import hypercharge_nullspace_symbolic

    nc, b = sp.symbols('N_c b', positive=True)
    ns = hypercharge_nullspace_symbolic()
    ratios = ns["ratios_normalised_to_yQ"]

    # y_Q : y_L from the model's own nullspace, as strings -> sympy
    y_Q = sp.sympify(str(ratios[0])) if not isinstance(ratios, dict) else None
    if isinstance(ratios, dict):
        y_Q = sp.sympify(str(ratios.get("y_Q", 1)))
        y_L = sp.sympify(str(ratios.get("y_L", -nc)))
    else:
        y_L = sp.sympify(str(ratios[3]))
    y_Q = sp.sympify(str(y_Q)).subs({sp.Symbol('N_c'): nc,
                                     sp.Symbol('Nc'): nc, sp.Symbol('n_c'): nc})
    y_L = sp.sympify(str(y_L)).subs({sp.Symbol('N_c'): nc,
                                     sp.Symbol('Nc'): nc, sp.Symbol('n_c'): nc})

    A_Y = sp.simplify(sp.Rational(1, 2) * (nc * y_Q + y_L))
    A_tr = sp.simplify(sp.Rational(1, 2) * (nc * b + 0))

    return {"y_Q": str(y_Q), "y_L": str(y_L),
            "A_su2sq_Y": str(A_Y),
            "A_su2sq_Y_identically_zero": bool(sp.simplify(A_Y) == 0),
            "A_su2sq_colour_trace": str(A_tr),
            "A_su2sq_trace_nonzero_for_b": bool(
                sp.simplify(A_tr.subs(b, 1)) != 0),
            "nullspace_dim": ns["symbolic_nullspace_dim"],
            "one_abelian_direction_only": bool(
                ns["symbolic_nullspace_dim"] == 1),
            "verdict": ("the U(1) subgroup of U(N_c) has a nonzero "
                        "[SU(2)_L]^2 U(1) anomaly and cannot be gauged; "
                        "colour is the traceless SU(N_c)")}


def colour_anomalies_on_the_model_content(n: int = 3,
                                          drop_d_R: bool = False
                                          ) -> Dict[str, Any]:
    """Every colour anomaly, on the model's OWN first-generation content.

    Content (F27 chirality + F42 right-handed quarks): one left-handed
    SU(2)_L doublet of colour triplets (2 members), and two right-handed
    colour-triplet singlets u_R, d_R.

      SU(N)^3          A(fund) * (n_L - n_R) = A(fund) * (2 - 2) = 0
      SU(N)^2 U(1)_Y   2 y_Q - (y_u + y_d), evaluated on the F279/F293
                       nullspace, = 0 IDENTICALLY in N_c

    Neither is vacuous: A(fund) is nonzero (S1b) so the first is a statement
    about the CONTENT, and the second is a nontrivial cancellation between
    y_u = N_c + 1 and y_d = 1 - N_c.  ``drop_d_R=True`` removes one right-handed
    singlet and both go nonzero, which is what makes them checks.
    """
    from casim.engine.gauge.derive_ncolour import hypercharge_nullspace_symbolic

    A_fund = anomaly_coefficients_float_max(n)
    n_L, n_R = 2, (1 if drop_d_R else 2)
    cubic = abs(n_L - n_R) * A_fund

    ns = hypercharge_nullspace_symbolic()
    ratios = ns["ratios_normalised_to_yQ"]
    if isinstance(ratios, dict):
        y_Q = sp.sympify(str(ratios.get("y_Q")))
        y_u = sp.sympify(str(ratios.get("y_u")))
        y_d = sp.sympify(str(ratios.get("y_d")))
    else:
        y_Q, y_u, y_d = (sp.sympify(str(ratios[0])), sp.sympify(str(ratios[1])),
                         sp.sympify(str(ratios[2])))
    mixed = sp.simplify(2 * y_Q - (y_u + (0 if drop_d_R else y_d)))

    return {"n": n, "A_fund_max": A_fund,
            "n_left_triplets": n_L, "n_right_triplets": n_R,
            "cubic_SUN3": float(cubic),
            "cubic_cancels": bool(cubic == 0.0),
            "A_fund_is_nonzero": bool(A_fund > 1e-6),
            "mixed_SUN2_U1Y": str(mixed),
            "mixed_cancels_identically_in_Nc": bool(sp.simplify(mixed) == 0),
            "y_u": str(y_u), "y_d": str(y_d),
            "drop_d_R": bool(drop_d_R)}


# ==========================================================================
# S6 -- the multiplicity: Lambda^3 has a singlet iff N = 3
# ==========================================================================
def antisymmetric_three_index_singlet(n: int) -> Dict[str, Any]:
    """dim of the SU(n)-invariant subspace of Lambda^3(C^n).

    A three-constituent, totally antisymmetric, group-singlet state exists iff
    this is 1.  Computed as the joint kernel of the total generators
    G^a = T^a (x) 1 (x) 1 + 1 (x) T^a (x) 1 + 1 (x) 1 (x) T^a restricted to the
    antisymmetric subspace.
    """
    T = su_n_generators(n)
    d = n ** 3
    idx = [(i, j, k) for i in range(n) for j in range(n) for k in range(n)]
    pos = {t: a for a, t in enumerate(idx)}

    # antisymmetriser projector on (C^n)^{(x)3}
    P = np.zeros((d, d), dtype=complex)
    perms = [((0, 1, 2), 1), ((1, 0, 2), -1), ((0, 2, 1), -1),
             ((2, 1, 0), -1), ((1, 2, 0), 1), ((2, 0, 1), 1)]
    for (i, j, k) in idx:
        src = pos[(i, j, k)]
        for perm, sgn in perms:
            tgt = pos[tuple((i, j, k)[p] for p in perm)]
            P[tgt, src] += sgn / 6.0

    ev, vec = np.linalg.eigh(P)
    keep = vec[:, ev > 0.5]                      # orthonormal basis of Lambda^3
    lam_dim = keep.shape[1]
    if lam_dim == 0:
        return {"n": n, "lambda3_dim": 0, "singlet_dim": 0,
                "has_epsilon_singlet": False}

    eye = np.eye(n, dtype=complex)
    rows = []
    for a in range(len(T)):
        G = (np.kron(np.kron(T[a], eye), eye)
             + np.kron(np.kron(eye, T[a]), eye)
             + np.kron(np.kron(eye, eye), T[a]))
        rows.append(keep.conj().T @ G @ keep)
    stack = np.concatenate(rows, axis=0)
    sv = np.linalg.svd(stack, compute_uv=False)
    # ABSOLUTE tolerance: the generators are O(1) on an orthonormal basis, and
    # a relative tolerance is wrong exactly where the answer is interesting --
    # if the whole of Lambda^3 IS the singlet then sv[0] is itself ~0.
    tol = 1e-9
    singlet_dim = int(np.sum(sv < tol)) + (lam_dim - sv.size)
    return {"n": n, "lambda3_dim": int(lam_dim),
            "singlet_dim": int(singlet_dim),
            "has_epsilon_singlet": bool(singlet_dim == 1)}


def multiplicity_squeeze(n_values: Sequence[int] = (2, 3, 4, 5, 6)
                         ) -> Dict[str, Any]:
    """The scan: Lambda^3 carries a singlet at exactly one n.

    INPUT CONSUMED, stated here and repeated in the finding: that baryons are
    THREE-constituent bound states.  That is empirical (and is what the tree's
    own F71/F122 three-body construction reproduces), not derived here.  Given
    it, plus DERIVED Fermi statistics (F289) and a symmetric space (x) spin (x)
    flavour ground state, the internal multiplicity is 3 exactly -- an upper
    and a lower bound in one computation.
    """
    rows = [antisymmetric_three_index_singlet(n) for n in n_values]
    hits = [r["n"] for r in rows if r["has_epsilon_singlet"]]
    return {"rows": rows, "n_with_singlet": hits,
            "unique_and_three": bool(hits == [3]),
            "empirical_input": "baryons are three-constituent states",
            "derived_input": "Fermi statistics (F289), not imported"}


# ==========================================================================
# S7 -- eight gluons
# ==========================================================================
def adjoint_dimension_and_closure(n: int = 3) -> Dict[str, Any]:
    """dim su(n) = n^2 - 1 gluons, and the algebra closes on f^{abc}."""
    T = su_n_generators(n)
    ng = len(T)
    f = np.zeros((ng, ng, ng))
    worst = 0.0
    for a in range(ng):
        for b in range(ng):
            comm = T[a] @ T[b] - T[b] @ T[a]
            for c in range(ng):
                f[a, b, c] = float(np.real(-2j * np.trace(comm @ T[c])))
            rebuilt = 1j * np.einsum('c,cij->ij', f[a, b], T)
            worst = max(worst, float(np.max(np.abs(comm - rebuilt))))
    antisym = float(np.max(np.abs(f + np.transpose(f, (1, 0, 2)))))
    return {"n": n, "n_gluons": ng, "closure_residual": worst,
            "f_antisymmetry_residual": antisym}


# ==========================================================================
# The registry entry point
# ==========================================================================
def check_su3_structure(n_colour: int = 3,
                        use_compensator: bool = True,
                        chiral_colour: bool = False,
                        rule_reads_colour: bool = False,
                        drop_d_R: bool = False) -> Dict[str, Any]:
    """The B1-colour gate, as a registry entry with real parameters.

    Declared controls (each verified red in the driver, and red only where
    declared):

    ``--param use_compensator=false``  drop the link variable's transformation
        law.  S3c must go red: a covariance test that passes without the
        connection has not tested the forcing, and the whole of S3 would be
        vacuous.

    ``--param chiral_colour=true``     couple colour to one branch only.  S2a
        must go red (the branch-space coupling stops being a scalar), which is
        what makes "the even law is forced" a statement rather than a
        tautology.

    ``--param rule_reads_colour=true`` let one Gell-Mann matrix into the rule.
        S4b must go red: the index stops being internal and the commutant
        collapses below n^2, so U(n) is no longer the invariance group.

    ``--param drop_d_R=true``          delete one right-handed colour triplet
        from the model's content.  S5d AND S5e must go red: the cubic anomaly
        stops cancelling 2 - 2 and the mixed one stops vanishing in N_c, which
        is what makes both statements about the CONTENT rather than identities.

    ``--param n_colour=4``             run the whole argument at N = 4.  S6
        must go red -- Lambda^3(C^4) has no singlet -- which is the check that
        S6 is N-sensitive rather than generic.
    """
    checks: List[Tuple[str, bool, Any]] = []
    nc = int(n_colour)

    # ---- basis sanity: the generators are checked, not trusted -------------
    norm_res = generator_normalisation_residual(nc)
    checks.append(("S0 su(N) basis normalised Tr(T^a T^b) = delta/2",
                   norm_res < 1e-13, norm_res))

    # ---- S1: colour cannot be chiral; SU(2) can ---------------------------
    su2 = anomaly_coefficients_exact(2)
    checks.append(("S1a SU(2): ALL 27 symmetric anomaly coefficients are "
                   "EXACTLY zero => a chiral doublet is allowed",
                   su2["all_exactly_zero"], su2["largest_magnitude"]))
    wit = anomaly_witness_exact(3)
    checks.append(("S1b SU(3): A^{888} = -1/sqrt(3) exactly, nonzero => a "
                   "chiral triplet is NOT allowed",
                   (not wit["is_zero"])
                   and wit["equals_minus_one_over_sqrt_n"],
                   wit["A_ddd"]))
    tab = chirality_assignment_table(nc)
    checks.append(("S1c among {vector-like, chiral, conjugate} ONLY the "
                   "vector-like colour assignment is anomaly-free",
                   tab["only_vector_like_survives"],
                   [(r["assignment"], r["max_abs_anomaly"])
                    for r in tab["rows"]]))

    # ---- S2: hence the gluon's even law is forced --------------------------
    g_L, g_R = (1.0, 0.0) if chiral_colour else (1.0, 1.0)
    tl = branch_coupling_traceless_part(g_L, g_R)
    checks.append(("S2a vector-like => the branch-space coupling is a SCALAR "
                   "(traceless part exactly 0) => F68/F91 even law FORCED",
                   tl == 0.0, tl))
    bs = branch_split_on_body_diagonal()
    checks.append(("S2b ... and the contrast is real: a chiral colour would "
                   "split the branches by |dOmega|/2 on the body diagonal",
                   bs["split_plus_vs_even"] > 1e-3
                   and bs["identity_residual"] < 1e-12,
                   (bs["split_plus_vs_even"], bs["identity_residual"])))

    # ---- S3: locality forces the connection --------------------------------
    loc = locality_forces_connection(n=nc, use_compensator=use_compensator)
    checks.append(("S3a a CA rule is ONE operator per cell, so a SITE-DEPENDENT "
                   "V(x) commutes with the on-site step exactly (F27's U(x) is "
                   "pure gauge for this reason)",
                   loc["onsite_commutes_residual"] < 1e-13,
                   loc["onsite_commutes_residual"]))
    checks.append(("S3b the HOP compares two cells, so covariance fails at "
                   "O(1) with no compensator",
                   loc["bare_hop_covariance_residual"] > 0.1,
                   loc["bare_hop_covariance_residual"]))
    checks.append(("S3c U_mu -> V(x) U_mu V^dag(x+mu) restores it exactly => "
                   "the gluon field is FORCED by locality",
                   loc["covariant_hop_residual"] < 1e-12,
                   loc["covariant_hop_residual"]))
    tree = locality_forces_connection_tree(use_compensator=use_compensator)
    checks.append(("S3d the same three legs on the TREE's own SU(3) operators "
                   "(strong.py), not a toy",
                   tree["bare_shift_covariance_residual"] > 0.1
                   and tree["covariant_shift_residual"] < 1e-12,
                   (tree["bare_shift_covariance_residual"],
                    tree["covariant_shift_residual"])))

    # ---- S4: unitarity fixes U(N) ------------------------------------------
    com = commutant_of_the_rule(n=nc, rule_reads_colour=rule_reads_colour)
    checks.append(("S4a the model's own steps generate the FULL M_4 on the "
                   "Dirac factor (otherwise the commutant would be big for a "
                   "trivial reason), and the re-typed walk IS unitary",
                   com["dirac_algebra_is_full_M4"]
                   and com["walk_unitarity_residual"] < 1e-13,
                   (com["dirac_algebra_dim"],
                    com["walk_unitarity_residual"])))
    checks.append((f"S4b the commutant of the rule is M_{nc} (dim {nc*nc}) "
                   f"=> the invariance group is exactly U({nc})",
                   com["commutant_is_M_n"],
                   (com["commutant_dim"], com["expected_if_internal"])))
    deg = internal_index_degeneracy(nc)
    checks.append((f"S4c corollary and PREDICTION: the spectrum is exactly "
                   f"{nc}-fold degenerate",
                   deg["every_level_is_n_fold"]
                   and deg["degeneracy_residual"] < 1e-12,
                   (deg["multiplicities"], deg["degeneracy_residual"])))

    # ---- S5: U(N) -> SU(N) --------------------------------------------------
    tr = trace_u1_is_anomalous()
    checks.append(("S5a [SU(2)_L]^2 U(1)_Y is IDENTICALLY zero in N_c on the "
                   "model's own nullspace",
                   tr["A_su2sq_Y_identically_zero"], tr["A_su2sq_Y"]))
    checks.append(("S5b [SU(2)_L]^2 U(1)_trace = N_c b / 2 != 0 => the U(1) "
                   "factor of U(N_c) CANNOT be gauged => colour is SU(N_c)",
                   tr["A_su2sq_trace_nonzero_for_b"], tr["A_su2sq_colour_trace"]))
    checks.append(("S5c only ONE abelian direction exists (nullspace dim 1, "
                   "F279/F293) and it is already spent on Y",
                   tr["one_abelian_direction_only"], tr["nullspace_dim"]))
    va = colour_anomalies_on_the_model_content(nc, drop_d_R=drop_d_R)
    checks.append(("S5d on the model's OWN content the cubic SU(N)^3 anomaly "
                   "cancels 2 - 2, and A(fund) itself is NONZERO so this is a "
                   "statement about the content",
                   va["cubic_cancels"] and va["A_fund_is_nonzero"],
                   (va["cubic_SUN3"], va["A_fund_max"])))
    checks.append(("S5e the mixed SU(N)^2 U(1)_Y anomaly 2y_Q - (y_u + y_d) "
                   "vanishes IDENTICALLY in N_c on the model's own nullspace "
                   "(y_u = N_c+1, y_d = 1-N_c)",
                   va["mixed_cancels_identically_in_Nc"],
                   (va["mixed_SUN2_U1Y"], va["y_u"], va["y_d"])))

    # ---- S6: the multiplicity, given three-quark baryons -------------------
    sq = multiplicity_squeeze()
    checks.append(("S6a Lambda^3(C^N) carries an SU(N) singlet at EXACTLY one "
                   "N, and it is 3 (scan N = 2..6)",
                   sq["unique_and_three"],
                   [(r["n"], r["lambda3_dim"], r["singlet_dim"])
                    for r in sq["rows"]]))
    this_n = antisymmetric_three_index_singlet(nc)
    checks.append((f"S6b ... so a three-constituent totally antisymmetric "
                   f"singlet exists at N = {nc}",
                   this_n["has_epsilon_singlet"], this_n["singlet_dim"]))

    # ---- S7: eight gluons ---------------------------------------------------
    ad = adjoint_dimension_and_closure(nc)
    checks.append((f"S7 dim su({nc}) = {nc*nc-1} gluons and the algebra closes "
                   f"on f^abc",
                   ad["n_gluons"] == nc * nc - 1
                   and ad["closure_residual"] < 1e-12
                   and ad["f_antisymmetry_residual"] < 1e-12,
                   (ad["n_gluons"], ad["closure_residual"])))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"n_colour": nc, "use_compensator": bool(use_compensator),
                       "chiral_colour": bool(chiral_colour),
                       "rule_reads_colour": bool(rule_reads_colour),
                       "drop_d_R": bool(drop_d_R)},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    """The one-screen statement of what moved and what did not."""
    return {
        "B1_colour_derived": [
            "unitary: the rule is R (x) 1_N, commutant = M_N, group = U(N)",
            "special: [SU(2)_L]^2 U(1)_trace != 0 removes the U(1) factor",
            "local: a CA rule has no global operations, so V(x) is free "
            "on-site and the hop needs a compensator = the gluon",
            "vector-like: a chiral triplet has A^{888} = -1/sqrt(3) != 0, "
            "while a chiral doublet is anomaly-free -- so the model's "
            "chiral weak / vector strong split is forced, not chosen",
            "even propagation law: F91's one unforced assignment closes",
            "eight gluons: dim su(3) = 8",
        ],
        "B1_colour_still_input": [
            "THAT the quark carries an internal index at all",
        ],
        "B10_touched_only_here": (
            "S6 gives N = 3 exactly from Lambda^3 having a singlet at exactly "
            "one N, GIVEN three-constituent baryons (empirical) and DERIVED "
            "Fermi statistics (F289).  It is not one of B10's three closed "
            "routes and does not re-open them.  It is independent of, and "
            "agrees with, F298's structural N_c <= 3."
        ),
    }


if __name__ == "__main__":       # pragma: no cover
    import json
    res = check_su3_structure()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']} -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    print(json.dumps(res["summary"], indent=2))
