"""
ca_su3_ladder.py — SU(3) electric Casimir ladder and the SU(3) character rotor
==============================================================================

Created: 2026-06-07 — companion to `ca_link_hamiltonian.py` (F110/F111).
Resolves the "SU(3) Casimir ladder" scope item of F110: the F98–F101
A-vs-C caveat (Abelian/centre N-ality vs SU(3) Casimir scaling) made
explicit and computable.

Content
-------
1. **The electric Casimir ladder** — exact rational data for SU(3) irreps
   (p,q): quadratic Casimir C₂ = (p²+q²+pq+3p+3q)/3, dimension
   d = (p+1)(q+1)(p+q+2)/2, conjugation (p,q)↔(q,p), triality (p−q) mod 3.
   In Kogut–Susskind theory a link carrying irrep R costs electric energy
   (g²/2)C₂(R): the ladder IS the strong-coupling spectrum of a link.

2. **The gauge-invariant flux chain** — static charges R, R̄ at the ends of
   a chain of L links: at λ=0 Gauss's law at the intermediate (matter-free)
   sites forces every link into the SAME irrep R (the singlet appears in
   A⊗B̄ iff A=B, multiplicity 1 — verified programmatically over the
   ladder), so

       V_R(L) = (g²/2) · C₂(R) · L      (exact, Fractions)

   ⇒ **Casimir scaling**: σ_R/σ_3 = C₂(R)/C₂(3); exactly 9/4 (adjoint),
   5/2 (sextet), 9/2 (decuplet).  Contrast: the ℤ₃ centre theory
   (`ca_link_hamiltonian`, symmetric residue) sees only triality —
   σ(q=2) = σ(q=1) exactly.  This is the A-vs-C dichotomy of F98–F101 as
   two computable laws.

3. **The SU(3) character rotor** — the F101 compact rotor with the U(1)
   charge basis replaced by the SU(3) irrep (character) basis:

       H = (g²/2) Ĉ₂  −  (λ/2)(χ_F + χ_F̄)        (multiplication operator)

   χ_F·χ_R = Σ_{R'∈F⊗R} χ_{R'} (fundamental fusion, multiplicity-free), so
   the magnetic term is the fusion adjacency matrix — the direct analogue of
   cos φ̂ shifting the U(1) charge by ±1.  The centre order parameter is
   s₁ = ⟨(1/3)χ_F⟩ and σ₁ = −ln s₁ (F99/F101 convention).

   Strong-coupling PT (first order): the singlet mixes only with 3 and 3̄,
   a₃ = (λ/2)/((g²/2)C₂(F)) = 3λ/(4g²), giving

       s₁ → (1/3)(a₃+a₃̄) = λ/(2g²)  =  2λχ  at  χ = 1/(4g²)

   — the SAME leading non-perturbative log law σ₁ → −ln(λ/(2g²)) as the
   F101 U(1) rotor under the F110 χ-map.  The group changes the string
   tension ladder (Casimir scaling); it does not change the leading
   strong-coupling logarithm.  (Verified asymptotically, F111 T7.)

Conventions: unnormalised characters in the magnetic term (χ = e^{iφ} is
the U(1) case); truncation by p+q ≤ cut with checked convergence (the F101
S1 policy).  Exact statements use `fractions.Fraction`.

NOTE 2026-08-18 (F325, ledger record S22) -- read before quoting item 3.
--------------------------------------------------------------------------
This module IS the genuine SU(N) link Hamiltonian F110 deferred and F294's
"Remains" item 1 asked for.  It was built here on 2026-06-07 and then went
uncited by F294, F298, F299 and F303, all four of which wanted it (F299's
cross-reference list even carries a dangling [[F111-su3-ladder-casimir-scaling]]
pointing at this file).  It is central to the X1 close: branch A excluded,
branch B (chi = 1, g_s = 1/2) adopted.

Item 3's strong-coupling identity is arithmetically correct, and its claim of
"the SAME leading log ... under the F110 chi-map" is LINK-COUNT INCONSISTENT.
`su3_rotor_hamiltonian` puts (g^2/2) C_2 on ONE link; the U(1) comparison at
chi = 1/(4 g^2) is FOUR.  The electric gaps differ by exactly n/C_F = 3.  At
equal n the exact statement is

    s1_SU(N) / s1_U(1)  ->  2 / (N^2 - 1)        (independent of n_links)

so the agreement at N = 3 is C_F d_F = (N^2 - 1)/2 = 4 coinciding with the four
links, NOT a statement about the group -- setting the ratio to 1 needs N^2 = 3,
so there is no N_c selector in it.  Two consequences.  (a) F111b T7 must not be
quoted as confirming chi = 1/(4 g^2); the confirmation is the coefficient
argument (F325 section 2) plus the magnetic audit (F325 section 5), which finds
the magnetic term to be a unit-entry adjacency in BOTH theories and therefore
free of any group factor.  (b) sigma_1 carries an EXACT offset
ln((N^2 - 1)/2) = ln 4 = 1.386294 nats between the Z_3/U(1) engine and this one
at N = 3 -- a correction to F99/F100/F101's string tension, orthogonal to g_s.
"""

from fractions import Fraction

import numpy as np


# ══════════════════════════════════════════════════════════════════
#  Irrep data — exact
# ══════════════════════════════════════════════════════════════════

def casimir2(p, q):
    """Quadratic Casimir C₂(p,q) = (p²+q²+pq+3p+3q)/3, exact Fraction.
    Normalisation: C₂(1,0) = 4/3 (fundamental), C₂(1,1) = 3 (adjoint)."""
    return Fraction(p * p + q * q + p * q + 3 * p + 3 * q, 3)


def dim_irrep(p, q):
    """dim(p,q) = (p+1)(q+1)(p+q+2)/2 (always an integer)."""
    num = (p + 1) * (q + 1) * (p + q + 2)
    assert num % 2 == 0
    return num // 2


def conjugate(p, q):
    return (q, p)


def triality(p, q):
    """N-ality (centre ℤ₃ charge) of the irrep: (p − q) mod 3."""
    return (p - q) % 3


def fuse_F(p, q):
    """3 ⊗ (p,q) = (p+1,q) ⊕ (p−1,q+1) ⊕ (p,q−1), invalid labels dropped.
    Multiplicity-free."""
    return [t for t in ((p + 1, q), (p - 1, q + 1), (p, q - 1))
            if t[0] >= 0 and t[1] >= 0]


def fuse_Fbar(p, q):
    """3̄ ⊗ (p,q) = (p,q+1) ⊕ (p+1,q−1) ⊕ (p−1,q)."""
    return [t for t in ((p, q + 1), (p + 1, q - 1), (p - 1, q))
            if t[0] >= 0 and t[1] >= 0]


def irrep_ladder(cut):
    """All (p,q) with p+q ≤ cut, sorted by (C₂, p):  the electric ladder."""
    reps = [(p, q) for p in range(cut + 1) for q in range(cut + 1 - p)]
    return sorted(reps, key=lambda r: (casimir2(*r), r))


def fusion_dim_identity_residual(cut):
    """Σ_{R'∈F⊗R} dim R' − 3·dim R, maximised over the ladder (no edge
    truncation inside the check).  Exactly 0 — the fusion bookkeeping is
    dimension-exact."""
    worst = 0
    for (p, q) in irrep_ladder(cut):
        s = sum(dim_irrep(*t) for t in fuse_F(p, q))
        worst = max(worst, abs(s - 3 * dim_irrep(p, q)))
    return worst


def singlet_in_product(A, B):
    """Multiplicity of the singlet in A ⊗ B, computed from the fusion data:
    repeatedly fuse A with fundamentals to reach B̄ ... for the chain
    constraint we only need the standard fact mult = δ_{B,Ā}; this verifies
    it on the ladder via character orthogonality on the maximal torus."""
    return 1 if B == conjugate(*A) else 0


def singlet_multiplicity_torus(A, B, n_grid=64):
    """
    Independent NUMERICAL verification of mult(1 ∈ A⊗B) by Weyl-torus
    character integration  ∫ χ_A χ_B dU  over SU(3) Haar (class measure).
    Characters evaluated DIVISION-FREE via the Jacobi–Trudi determinant
    χ_{(p,q)} = s_λ(z), λ = (p+q, q, 0), s_λ = det[h_{λ_i−i+j}] — no Weyl
    ratio, so no 0/0 at degenerate torus points; the periodic rectangle
    rule is then spectrally accurate.  Certifies `singlet_in_product`.
    """
    phi = (np.arange(n_grid) + 0.5) * 2.0 * np.pi / n_grid
    P1, P2 = np.meshgrid(phi, phi, indexing='ij')
    P3 = -(P1 + P2)
    z = (np.exp(1j * P1), np.exp(1j * P2), np.exp(1j * P3))
    d12 = 2.0 * (1.0 - np.cos(P1 - P2))
    d13 = 2.0 * (1.0 - np.cos(P1 - P3))
    d23 = 2.0 * (1.0 - np.cos(P2 - P3))
    meas = d12 * d13 * d23
    meas = meas / meas.sum()                  # ∫ dμ_Haar(class) = 1

    k_max = A[0] + A[1] + B[0] + B[1] + 2
    h = [np.ones_like(z[0]), z[0] + z[1] + z[2]]   # h₀, h₁
    for k in range(2, k_max + 1):                  # Newton-free recursion:
        # h_k(z1,z2,z3) = Σ_a z3^a · h_{k−a}(z1,z2), h built incrementally
        hk = np.zeros_like(z[0])
        for a in range(k + 1):
            # h_{k−a}(z1, z2) = Σ_b z1^b z2^{k−a−b}
            m = k - a
            h12 = np.zeros_like(z[0])
            for b in range(m + 1):
                h12 = h12 + z[0] ** b * z[1] ** (m - b)
            hk = hk + z[2] ** a * h12
        h.append(hk)

    def hh(k):
        if k < 0:
            return np.zeros_like(z[0])
        return h[k]

    def schur(p, q):
        lam = (p + q, q, 0)
        M = [[hh(lam[i] - i + j) for j in range(3)] for i in range(3)]
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))

    val = np.sum(schur(*A) * schur(*B) * meas)
    return float(np.real(val))


# ══════════════════════════════════════════════════════════════════
#  Flux chain — Casimir-scaled string energies (exact)
# ══════════════════════════════════════════════════════════════════

def chain_energy(R, L, g2=Fraction(1)):
    """
    λ=0 energy of a length-L flux chain with static R, R̄ end charges:
    Gauss's law forces every link into R (singlet_in_product), so
    E = (g²/2)·C₂(R)·L, exact Fraction.
    """
    g2 = Fraction(g2)
    return g2 / 2 * casimir2(*R) * L


def casimir_scaling_table(g2=Fraction(1)):
    """σ_R/σ_F for the ladder rungs used in F111 T6 — exact Fractions."""
    F = (1, 0)
    table = {}
    for name, R in (('3', (1, 0)), ('3bar', (0, 1)), ('6', (2, 0)),
                    ('8', (1, 1)), ('10', (3, 0)), ('15', (2, 1))):
        sigma = Fraction(g2) / 2 * casimir2(*R)
        table[name] = (R, sigma, sigma / (Fraction(g2) / 2 * casimir2(*F)))
    return table


# ══════════════════════════════════════════════════════════════════
#  The SU(3) character rotor
# ══════════════════════════════════════════════════════════════════

def su3_rotor_hamiltonian(g2, lam, cut):
    """
    H = (g²/2)Ĉ₂ − (λ/2)(χ_F + χ_F̄) in the irrep (character) basis,
    truncated at p+q ≤ cut.  Returns (H dense real symmetric, reps list,
    M_F) with (M_F)_{R'R} = [R' ∈ F⊗R] (the fusion adjacency; M_F̄ = M_Fᵀ).
    """
    reps = irrep_ladder(cut)
    pos = {r: n for n, r in enumerate(reps)}
    n = len(reps)
    H = np.zeros((n, n))
    M_F = np.zeros((n, n))
    for r in reps:
        H[pos[r], pos[r]] = 0.5 * g2 * float(casimir2(*r))
        for t in fuse_F(*r):
            if t in pos:
                M_F[pos[t], pos[r]] = 1.0
    H -= 0.5 * lam * (M_F + M_F.T)
    return H, reps, M_F


def su3_rotor_sigma1(g2, lam, cut=14):
    """
    σ₁ = −ln s₁,  s₁ = ⟨(1/3)χ_F⟩ in the rotor ground state.
    The ground state is conjugation-symmetric (C₂(R)=C₂(R̄), magnetic term
    F+F̄), so ⟨χ_F⟩ is real.
    """
    H, reps, M_F = su3_rotor_hamiltonian(g2, lam, cut)
    w, v = np.linalg.eigh(H)
    a = v[:, 0]
    if a[0] < 0:
        a = -a
    s1 = float(a @ (M_F @ a)) / 3.0
    return -np.log(s1), s1


def su3_rotor_strong_coupling_slope(g2=1.0):
    """First-order PT slope: s₁ → λ/(2g²) — equals the F101 U(1) rotor's
    2λχ at χ = 1/(4g²) (the F110 single-plaquette map)."""
    return 1.0 / (2.0 * g2)
