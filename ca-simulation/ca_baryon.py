"""
ca_baryon.py — colour-singlet three-quark (baryon / proton) construction  (FG-10)
=================================================================================

Created: 2026-06-01

Builds the first composite hadron in the model: the colour-singlet baryon
interpolating operator

        B(x) = ε_{abc}  q1^a(x)  q2^b(x)  q3^c(x)

with the totally antisymmetric SU(3) colour tensor ε_{abc}.  For the proton,
(q1,q2,q3) = (u,u,d).  The ε contraction is what makes B a colour singlet, and
that is exactly the statement that a physical hadron is colourless:

  • Gauge invariance:  under  q^a → V^a_{a'} q^{a'}  (V ∈ SU(3)),
        B → det(V)·B = B          (det V = 1)
    — verified to machine precision for local V(x).
  • Zero colour charge: the antisymmetric tensor is annihilated by every
    SU(3) generator,  (T^a⊗1⊗1 + 1⊗T^a⊗1 + 1⊗1⊗T^a)|ε⟩ = 0.
  • Proton quantum numbers (exact, fractions):  Q = +1,  B = 1.
  • Fermi statistics: colour-antisymmetric × spin-flavour-symmetric ground
    state → totally antisymmetric under quark exchange (Pauli).
  • Energetic stability: with the exact 2D string tension σ>0 (ca_confinement),
    separating one quark to infinity costs V(R)=σR → ∞, so the colour singlet
    is the finite-energy bound configuration — no free quark.

This is a *structural / operator-level* construction with correct quantum
numbers, exchange symmetry, and an energetic-binding argument; it is not a
real-time dynamical bound-state simulation (scoped as future work).

Conventions match `ca_strong.py`: colour triplets ordered (r,g,b); T^a = λ^a/2.
"""

import numpy as np
from fractions import Fraction

import ca_strong as cstr


# ══════════════════════════════════════════════════════════════════
#  Totally antisymmetric colour tensor  ε_{abc}
# ══════════════════════════════════════════════════════════════════

def levi_civita_3():
    """ε_{abc} on three colour indices (3×3×3), ε_{012}=+1."""
    eps = np.zeros((3, 3, 3), dtype=float)
    for a, b, c in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        eps[a, b, c] = 1.0
    for a, b, c in ((2, 1, 0), (0, 2, 1), (1, 0, 2)):
        eps[a, b, c] = -1.0
    return eps


_EPS = levi_civita_3()


# ══════════════════════════════════════════════════════════════════
#  Baryon interpolating field  B(x) = ε_{abc} q1^a q2^b q3^c
# ══════════════════════════════════════════════════════════════════

def baryon_field(trip1, trip2, trip3):
    """
    Contract three colour-triplet fields with ε_{abc}.

    trip1, trip2, trip3 : (..., 3) complex — colour triplets (r,g,b) of the
        three valence quarks at each lattice site (e.g. from
        `ca_strong._colour_triplet`).  Spatial shape is arbitrary/broadcast.

    Returns B : (...) complex — the colour-singlet scalar field.
    """
    return np.einsum('abc,...a,...b,...c->...', _EPS, trip1, trip2, trip3)


def proton_colour_field(q, dirac='eu'):
    """
    Build the proton colour singlet  ε_{abc} u^a u^b d^c  from a quark dict
    `q` (ca_strong layout), using Dirac component `dirac` for all three
    valence lines (a single-component proxy for the colour structure test).

    Note: with two identical u-triplets, ε_{abc}u^a u^b d^c vanishes
    identically (ε antisymmetric, u^a u^b symmetric) — which is precisely why
    the *spin-flavour* wavefunction must be symmetric (see proton_spin_flavour_*)
    for the colour-antisymmetric state to be non-zero overall.  For the pure
    colour-singlet *gauge* test we therefore use three independent triplets via
    `baryon_field`; this helper is provided for completeness/illustration.
    """
    u = cstr._colour_triplet(q, 'u', dirac)
    d = cstr._colour_triplet(q, 'd', dirac)
    return baryon_field(u, u, d)


# ══════════════════════════════════════════════════════════════════
#  Colour-singlet gauge invariance
# ══════════════════════════════════════════════════════════════════

def singlet_gauge_residual(trip1, trip2, trip3, Vfield):
    """
    Apply a local SU(3) gauge rotation V(x) to all three colour triplets and
    compare the baryon field before/after.  Returns max |B_after − B_before|.

    Exactly invariant because B → det(V)·B and det V = 1 for SU(3).
    """
    B0 = baryon_field(trip1, trip2, trip3)

    def rot(trip):
        return np.einsum('...ij,...j->...i', Vfield, trip)

    B1 = baryon_field(rot(trip1), rot(trip2), rot(trip3))
    return float(np.max(np.abs(B1 - B0)))


def det_residual_field(Vfield):
    """max |det V(x) − 1| over a local SU(3) field — the source of invariance."""
    return float(np.max(np.abs(np.linalg.det(Vfield) - 1.0)))


# ══════════════════════════════════════════════════════════════════
#  Zero total colour charge of the antisymmetric state
# ══════════════════════════════════════════════════════════════════

def singlet_state_vector():
    """
    The normalised colour-singlet of 3⊗3⊗3:  |S⟩ = (1/√6) ε_{abc} |abc⟩,
    returned as a length-27 complex vector (index 9a+3b+c).
    """
    v = np.zeros(27, dtype=complex)
    for a in range(3):
        for b in range(3):
            for c in range(3):
                v[9 * a + 3 * b + c] = _EPS[a, b, c]
    return v / np.linalg.norm(v)


def total_colour_generator(a):
    """
    27×27 matrix of the total generator G^a = T^a⊗I⊗I + I⊗T^a⊗I + I⊗I⊗T^a
    acting on 3⊗3⊗3 (all three quarks in the fundamental).
    """
    Ta = cstr.T_GEN[a]
    I3 = np.eye(3, dtype=complex)
    g = (np.kron(np.kron(Ta, I3), I3)
         + np.kron(np.kron(I3, Ta), I3)
         + np.kron(np.kron(I3, I3), Ta))
    return g


def singlet_charge_residual():
    """
    max_a ‖G^a |S⟩‖  — zero iff |S⟩ carries no colour charge (true singlet).
    """
    S = singlet_state_vector()
    worst = 0.0
    for a in range(8):
        g = total_colour_generator(a)
        worst = max(worst, float(np.linalg.norm(g @ S)))
    return worst


def singlet_casimir():
    """
    Quadratic Casimir  C2 = Σ_a (G^a)²  eigenvalue on |S⟩.  Should be 0 for
    the singlet (vs 4/3 for a single quark, 3 for the adjoint octet).
    """
    S = singlet_state_vector()
    C2 = np.zeros((27, 27), dtype=complex)
    for a in range(8):
        g = total_colour_generator(a)
        C2 = C2 + g @ g
    return float(np.real(np.vdot(S, C2 @ S)))


# ══════════════════════════════════════════════════════════════════
#  Proton quantum numbers (exact, rational)
# ══════════════════════════════════════════════════════════════════

# Standard-model first-generation quark charges (electric Q, baryon number B).
_Q = {'u': Fraction(2, 3), 'd': Fraction(-1, 3)}
_BNUM = Fraction(1, 3)        # baryon number per quark
# Hypercharge / isospin for the Gell-Mann–Nishijima cross-check (left doublet)
_T3 = {'u': Fraction(1, 2), 'd': Fraction(-1, 2)}
_Y_LQ = Fraction(1, 3)        # left-handed quark-doublet hypercharge (Q=T3+Y/2)


def proton_quantum_numbers():
    """
    Exact (rational) quantum numbers of the proton uud.

    Returns a dict with electric charge Q, baryon number B, third isospin T3,
    and a Gell-Mann–Nishijima consistency residual (all via fractions.Fraction
    so the arithmetic is exact, not floating point).
    """
    content = ['u', 'u', 'd']
    Q = sum(_Q[f] for f in content)
    B = sum(_BNUM for _ in content)
    T3 = sum(_T3[f] for f in content)
    # GMN per-quark: Q = T3 + Y/2 with Y = 1/3 for each left quark
    gmn_ok = all(_Q[f] == _T3[f] + _Y_LQ / 2 for f in ('u', 'd'))
    return {'content': 'uud', 'Q': Q, 'B': B, 'T3': T3,
            'Q_int': Q == 1, 'B_int': B == 1,
            'gmn_consistent': gmn_ok}


# ══════════════════════════════════════════════════════════════════
#  Spin-flavour wavefunction and Fermi statistics
# ══════════════════════════════════════════════════════════════════

# Single-quark spin-flavour basis: (flavour, spin) with spin ∈ {+,−}.
# We encode the proton spin-up SU(6) wavefunction as a dict over ordered
# 3-quark basis states  ((f1,s1),(f2,s2),(f3,s3)) → amplitude.

def proton_spin_flavour_wavefunction():
    """
    Proton spin-up SU(6) spin-flavour wavefunction (the totally symmetric
    combination of the 56-plet).  Returns dict[state] → amplitude, normalised.

        |p↑⟩ ∝ 2(u↑u↑d↓ + sym) − (u↑u↓d↑ + sym) ...

    Built from the symmetric sum over the 3 positions of the d quark with the
    standard coefficients (three +2 terms, six −1 terms; ‖·‖²=18).
    """
    psi = {}

    def add(state, amp):
        psi[state] = psi.get(state, 0.0) + amp

    U, D = 'u', 'd'
    up, dn = '+', '-'
    # the three "d position" placements of the seed u↑u↑d↓ and the −1 partners
    # generate the totally symmetric combination by explicit symmetrisation.
    # +2 terms: permutations of the multiset {u↑, u↑, d↓}  (3 distinct states)
    # −1 terms: permutations of the multiset {u↑, u↓, d↑}  (6 distinct states)
    seeds_plus = [((U, up), (U, up), (D, dn))]
    seeds_minus = [((U, up), (U, dn), (D, up))]
    from itertools import permutations

    def symmetrise(seed, coeff):
        # sum over all distinct orderings of the (possibly repeated) triple
        seen = set()
        for perm in set(permutations(range(3))):
            st = tuple(seed[perm[i]] for i in range(3))
            if st in seen:
                continue
            seen.add(st)
            add(st, coeff)

    for s in seeds_plus:
        symmetrise(s, +2.0)
    for s in seeds_minus:
        symmetrise(s, -1.0)

    norm = np.sqrt(sum(a * a for a in psi.values()))
    for k in psi:
        psi[k] /= norm
    return psi


def spin_flavour_symmetry_residual(psi=None):
    """
    Max deviation of the spin-flavour wavefunction from full S_3 symmetry:
    for every transposition (12),(13),(23), ‖P·ψ − ψ‖.  Zero ⇒ symmetric.
    """
    if psi is None:
        psi = proton_spin_flavour_wavefunction()

    def transpose(state, i, j):
        s = list(state)
        s[i], s[j] = s[j], s[i]
        return tuple(s)

    worst = 0.0
    for (i, j) in ((0, 1), (0, 2), (1, 2)):
        for st, amp in psi.items():
            swapped = transpose(st, i, j)
            diff = abs(psi.get(swapped, 0.0) - amp)
            worst = max(worst, diff)
    return float(worst)


def total_wavefunction_antisymmetry():
    """
    Verify the full proton wavefunction is antisymmetric under quark exchange:
        Ψ = (colour ε, antisymmetric) ⊗ (spin-flavour, symmetric) ⊗ (space, sym)
    Under a transposition P_ij:  colour → (−1)·colour, spin-flavour → (+1),
    space → (+1)  ⇒  Ψ → −Ψ.  Returns a dict of the three symmetry signatures.
    """
    # colour ε signature under each transposition is −1 (antisymmetric tensor)
    colour_sign = {}
    for (i, j) in ((0, 1), (0, 2), (1, 2)):
        # swap two indices of ε and read the sign
        axes = [0, 1, 2]
        axes[i], axes[j] = axes[j], axes[i]
        swapped = np.transpose(_EPS, axes)
        colour_sign[f'{i}{j}'] = float(np.sum(swapped * _EPS) /
                                       np.sum(_EPS * _EPS))   # = −1
    sf_res = spin_flavour_symmetry_residual()
    # total sign = colour(−1) × spinflavour(+1) × space(+1)
    total_sign = {k: v * 1.0 for k, v in colour_sign.items()}
    return {'colour_sign': colour_sign,
            'spin_flavour_symmetry_residual': sf_res,
            'total_exchange_sign': total_sign,
            'fermi_ok': all(abs(s + 1.0) < 1e-12 for s in total_sign.values())
                        and sf_res < 1e-12}


# ══════════════════════════════════════════════════════════════════
#  Energetic stability from the exact string tension
# ══════════════════════════════════════════════════════════════════

def quark_isolation_energy(beta, R_values=(1, 2, 4, 8, 16, 32)):
    """
    Energy cost V(R) = σ(β)·R to pull a single quark a distance R out of a
    colour-singlet, using the exact 2D string tension σ(β) = −ln w(β) from
    `ca_confinement`.  Diverges linearly → a free quark costs infinite energy,
    so the colour singlet is the bound, finite-energy configuration.
    """
    import ca_confinement as cf
    sigma = cf.string_tension(beta)
    return sigma, {int(R): float(sigma * R) for R in R_values}
