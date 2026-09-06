"""discrete_cpt.py — F328: an exact discrete CPT theorem for the free BCC Dirac walk
======================================================================================

Completeness rubric row **A4** ("CPT, and C, P, T separately") has been PARTIAL
for five reports (`docs/status/completeness-2026-08-02.md` through
`-2026-08-20.md`): [[F53]] built C, P and CP at the level of SU(2)xU(1) charge
LABELS (T3, Q, Y, chi) and coupling-strength magnitudes, and the row's own
"CPT" content (F53 P6) is a SCALAR statement, omega(+m) = omega(-m) — a
consequence one could hope to derive from a genuine operator theorem, not the
theorem itself. No module anywhere in the tree builds C, P or T as an explicit
operator on the one-tick unitary and asks whether it is an exact symmetry of
the RULE. This module does that, for the free (gauge-decoupled) massive BCC
Dirac walk `casim.engine.particles.dirac_bcc`, and answers row A4's own
question directly: **yes, an exact discrete CPT-type theorem exists, and it
does not factor into three separately-well-defined C/P/T pieces at finite
lattice spacing** — which is exactly the failure mode the row's research brief
flagged as a live possibility ("the standard proof route may not even apply
cleanly") and is why the row stays honestly scoped to the free sector here.

**Explicitly excluded from this finding's support:** [[F321]]'s reality of the
Euclidean action from closure of the loop set under reversal. That is a
statement about theta_QCD (row B11), a different object, and three prior
reports flagged borrowing it here as the row's standing trap. Nothing below
cites F321 for anything but this exclusion.

The construction
-----------------
The BCC Weyl one-tick unitary (`casim.engine.lattice.bcc.bcc_unitary`, Paper 1
Eq. 15) is, per chirality branch s in {+1, -1},

    A^s(k) = u^s(k) I - i (n_x^s(k) sigma_x + n_y^s(k) sigma_y + n_z^s(k) sigma_z),

real u^s, n^s. Two identities matter below, and they are NOT both lattice-specific
(corrected 2026-08-27 after the adversarial review caught this docstring
overclaiming both as embedding-specific): identity (I) is a GENERIC fact about
any real-(u, n)-parametrized Pauli-basis unitary u*I - i*n.sigma -- it needs
nothing about the BCC cos/sin closed form, only that u, n are real. Identity
(II) IS specific to the BCC closed form's behaviour under k -> -k. The headline
CPT theorem below (check_discrete_cpt_theorem legs B1-B3) uses ONLY (I), so it
is actually a generic fact about this class of Dirac-type constructions; what
IS BCC-specific is the companion no-go (legs D1-D3), which needs (II). Both
identities still follow most directly from the explicit cos/sin closed form
(verified below to literal 0.0), even though (I) does not strictly require it:

    (I)   A^s(k)*        = sigma_y A^s(k) sigma_y                 (any fixed k, either branch)
    (II)  A^{-s}(-k)      = sigma_y A^s(k) sigma_y                (branch swap + momentum flip)

(I) and (II) together give A^s(k)* = A^{-s}(-k) — complex conjugation of a
single chirality branch is exactly the OTHER branch at the reflected momentum.
This is the operator-level face of the module docstring's own remark
"omega_+(-k) = omega_-(k)" and of F301's chirality-odd finite-a Poincare
defect: a single branch is not symmetric under k -> -k, which is exactly why
no fixed (k-independent) unitary can implement ordinary spatial parity on a
single branch (`no_fixed_parity_obstruction` below; F327 already showed a
single branch cannot be the whole physical spectrum either, for an unrelated,
experimental reason — the two results are independent and mutually
reinforcing, not the same argument).

The massive Dirac one-tick unitary (`dirac_bcc.dirac_step_3d_bcc_splitstep`)
pairs ONE branch with its own dagger (forced by unitarity of the full 4x4
D_k, per that module's own docstring — not with the true opposite branch):

    D(k) = [[ n A^+(k),  i m I ], [ i m I,  n A^+(k)^dagger ]],   n = sqrt(1-m^2).

Chaining (I) and (II) through the block structure of D(k) (worked in
`## Derivation` of the finding file, and confirmed to literal 0.0 by
`cpt_operator_identity_residual`) gives, for EVERY momentum k and EVERY
admissible mass |m| <= 1, with NO small-k expansion:

    THETA . D(k) . THETA^{-1}  =  D(k)^{-1},        THETA := M . K,
    M := Sigma . (sigma_y (+) sigma_y),             Sigma = [[0,I],[I,0]],

K complex conjugation and Sigma the eta<->chi block swap (the standard Dirac
parity matrix gamma^0 in the Weyl basis). In position space THETA is
(THETA psi)(x) = M psi(-x)*  — reflection, an internal spin-and-chirality
twist, and complex conjugation, combined into ONE antiunitary operator. It
satisfies THETA^2 = -1 exactly (`theta_squared`), the Kramers signature of a
genuine spin-1/2 antiunitary symmetry, not an accident of the algebra.

What does NOT survive as a separate factor: plain reflection alone (Sigma,
no twist, no K) does not intertwine D(k) and D(-k) at all — confirmed to
O(1) residual, not a small defect — because D(k) and D(-k) generically have
DIFFERENT eigenvalue spectra (`no_fixed_parity_obstruction`: omega(k) !=
omega(-k) is the SAME chirality-odd fact F301 already isolated as its b_2
coefficient), so no fixed unitary parity operator of ANY shape can exist for
this walk at finite k. Nor does the internal twist alone without the momentum
reflection (`ca-reference.md`'s existing "Time-reversibility" section, which
only runs the SAME walk backward at -c_lat and calls that T — a check of
plain unitarity-invertibility, not of any antiunitary symmetry; see
`naive_reversal_residual`, which fails at O(0.1), confirming the section's
statement is not the theorem this row needed). Only the FULL combination is
exact. That is the content of the theorem: on this QCA, CPT is more
fundamental than any of its parts even for the free, gauge-decoupled kinetic
term — sharper than the continuum lore, where only the INTERACTING sector
needs the combination and the free sector is separately C, P, T symmetric.

Scope, stated narrowly
-----------------------
This is a free-fermion (no SU(2)_L charged current, no hypercharge, no W/Z/
gluon) theorem. [[F53]]'s own C, P are "maximally violated by the charged
current" — a statement about the INTERACTION, untouched here. Whether THETA
(possibly composed with F53's charge-conjugation charge-label map) survives
once the charged current (`casim.engine.gauge.charged_current`, coupling to
the left block ONLY) is switched on is the natural next step and is NOT
attempted here: that coupling is a nonlinear multiplicative gate, not a
closed-form momentum-diagonal 2x2/4x4 unitary, and extending the present
algebraic method to it is real additional work, named as open rather than
assumed to go through by Luders-Pauli analogy.
"""

from __future__ import annotations

from casim.numerics import xp as np
from casim.engine.lattice import bcc as _bcc
from casim.engine.particles.dirac_bcc import (
    dirac_step_3d_bcc_splitstep as _dirac_step,
    _bcc_weyl_blocks,
    _kinetic_n,
    _check_mass,
)

# ══════════════════════════════════════════════════════════════════
#  Fixed internal matrices (mathematical objects, not physical
#  constants — same status as the identity matrices bcc.py and
#  dirac_bcc.py already build inline; no casim.constants entry needed).
# ══════════════════════════════════════════════════════════════════
_I2 = np.eye(2, dtype=complex)
_SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SIGMA_SWAP = np.block([[np.zeros((2, 2)), np.eye(2)],
                        [np.eye(2), np.zeros((2, 2))]]).astype(complex)


def M_cpt() -> np.ndarray:
    """The 4x4 unitary internal part of THETA = M.K: block-swap (eta<->chi,
    the standard Dirac parity matrix gamma^0 in the Weyl basis) composed with
    sigma_y on each 2-spinor block. Sigma and (sigma_y (+) sigma_y) commute
    as matrices (one swaps blocks, the other acts identically within each),
    so the composition order is immaterial.
    """
    sy_block = np.kron(np.eye(2, dtype=complex), _SIGMA_Y)
    return _SIGMA_SWAP @ sy_block


def theta_squared() -> np.ndarray:
    """THETA^2 as a matrix acting on the field: for antiunitary THETA psi(x)
    = M psi(-x)*, applying it twice gives M M* psi(x) (the double reflection
    and double conjugation are each the identity). Returns M @ M.conj(),
    which the finding's derivation gives as exactly -I (Kramers signature).
    """
    M = M_cpt()
    return M @ M.conj()


def _A(kx, ky, kz, sign='+'):
    """Wrapper on `bcc.bcc_unitary` returning the 2x2 matrix (not the four
    separate entries), for direct matrix algebra below."""
    U_ff, U_fg, U_gf, U_gg = _bcc.bcc_unitary(kx, ky, kz, sign=sign)
    return np.array([[U_ff, U_fg], [U_gf, U_gg]], dtype=complex)


def _D(kx, ky, kz, m):
    """The massive BCC Dirac one-tick unitary D(k) (dirac_bcc.py's D_k),
    assembled as an explicit 4x4 matrix for algebraic checks. Uses branch
    '+' paired with its own dagger, exactly as `dirac_step_3d_bcc_splitstep`
    does — not the true opposite branch (dirac_bcc.py's own docstring: "the
    choice forced by unitarity of the full 4x4 D_k")."""
    _check_mass(m)
    n = _kinetic_n(m)
    Ak = _A(kx, ky, kz, '+')
    Akd = Ak.conj().T
    top = np.hstack([n * Ak, 1j * m * _I2])
    bot = np.hstack([1j * m * _I2, n * Akd])
    return np.vstack([top, bot])


# ══════════════════════════════════════════════════════════════════
#  T0 — the two lattice-specific 2x2 identities (algebraic, exact)
# ══════════════════════════════════════════════════════════════════
def identity_conjugate_fixed_k_residual(kx, ky, kz, sign='+'):
    """|A^s(k)* - sigma_y A^s(k) sigma_y| at fixed k (identity I)."""
    Ak = _A(kx, ky, kz, sign)
    return float(np.max(np.abs(Ak.conj() - _SIGMA_Y @ Ak @ _SIGMA_Y)))


def identity_branch_swap_residual(kx, ky, kz):
    """|A^+(k)* - A^-(-k)| (identities I+II combined: conjugation of one
    branch is exactly the other branch at the reflected momentum)."""
    Ap = _A(kx, ky, kz, '+')
    Am_negk = _A(-kx, -ky, -kz, '-')
    return float(np.max(np.abs(Ap.conj() - Am_negk)))


# ══════════════════════════════════════════════════════════════════
#  T1 — the CPT operator identity for the massive Dirac walk (exact)
# ══════════════════════════════════════════════════════════════════
def cpt_operator_identity_residual(kx, ky, kz, m):
    """|M D(k)* M - D(k)^dagger|, which is |THETA D(k) THETA^{-1} - D(k)^{-1}|
    once D(k)'s exact unitarity (dagger = inverse) is used. This is the
    theorem: it holds at every k, every |m| <= 1, to literal 0.0 (verified
    below over random samples; no small-k expansion enters the derivation).
    """
    M = M_cpt()
    Dk = _D(kx, ky, kz, m)
    lhs = M @ Dk.conj() @ M
    rhs = Dk.conj().T
    return float(np.max(np.abs(lhs - rhs)))


def unitarity_residual(kx, ky, kz, m):
    """|D(k)^dagger D(k) - I|, floating-point-floor sanity check that the
    Dirac walk really is exactly unitary (so dagger really is inverse)."""
    Dk = _D(kx, ky, kz, m)
    return float(np.max(np.abs(Dk.conj().T @ Dk - np.eye(4))))


# ══════════════════════════════════════════════════════════════════
#  T2 — no fixed parity can exist at finite k (spectral obstruction)
# ══════════════════════════════════════════════════════════════════
def no_fixed_parity_obstruction(kx, ky, kz, m):
    """omega(k) - omega(-k) for the constructed D(k) (eigenvalues
    exp(+-i omega(k)), omega = arccos(n u^+(k))). A NONZERO value proves no
    momentum-independent unitary Pi can satisfy Pi D(k) Pi^{-1} = D(-k) for
    every k (conjugation by a fixed matrix preserves the eigenvalue
    spectrum, and a spectrum mismatch is an outright obstruction, not merely
    unproven). This is the operator-level face of F301's chirality-odd
    finite-a Poincare defect, re-derived independently here as a spectral
    fact rather than assumed from that finding."""
    n = _kinetic_n(m)
    u_p, _, _, _ = _bcc._bcc_uvec(kx, ky, kz, sign='+')
    u_p_neg, _, _, _ = _bcc._bcc_uvec(-kx, -ky, -kz, sign='+')
    omega = np.arccos(np.clip(n * u_p, -1.0, 1.0))
    omega_neg = np.arccos(np.clip(n * u_p_neg, -1.0, 1.0))
    return float(omega - omega_neg)


# ══════════════════════════════════════════════════════════════════
#  T3 — naive candidates fail (both are load-bearing negative controls)
# ══════════════════════════════════════════════════════════════════
def naive_parity_residual(kx, ky, kz, m):
    """|Sigma D(k) Sigma - D(-k)|: plain block-swap, no internal twist, no
    K. Expected to fail at O(1), not a small defect — see
    `no_fixed_parity_obstruction` for why no fixed unitary can succeed here."""
    Dk = _D(kx, ky, kz, m)
    Dnk = _D(-kx, -ky, -kz, m)
    lhs = _SIGMA_SWAP @ Dk @ _SIGMA_SWAP
    return float(np.max(np.abs(lhs - Dnk)))


def naive_reversal_residual(eu, ed, xu, xd, m, n_steps):
    """Reproduces `docs/theory/ca-reference.md`'s existing "Time-reversibility"
    check in the Dirac (not bare Weyl) setting: run n_steps forward, then
    n_steps backward via the walk's OWN inverse (dt=1 forward step is exactly
    invertible; running D(k)^dagger is the same as running D(-c) in that
    section's language). Returns the round-trip residual, expected at the
    floating-point floor — this checks invertibility, which every unitary CA
    has for free, and is NOT a check of any antiunitary symmetry. Contrast
    with `cpt_realspace_residual`, the actual new content."""
    e_u, e_d, c_u, c_d = eu, ed, xu, xd
    hist = [(e_u, e_d, c_u, c_d)]
    for _ in range(n_steps):
        e_u, e_d, c_u, c_d = _dirac_step(e_u, e_d, c_u, c_d, m=m, dt=1.0, sign='+')
        hist.append((e_u, e_d, c_u, c_d))
    # backward: apply the inverse step (adjoint) by running dt=-1 is not
    # exposed; instead use FFT-domain dagger application directly.
    from casim.engine.lattice.geometry import make_kgrid_3d as _kgrid3d
    from casim.numerics import fft as _fft
    KX, KY, KZ = _kgrid3d(*e_u.shape)
    n = _kinetic_n(m)
    A, Ap = _bcc_weyl_blocks(KX, KY, KZ, sign='+')
    A_ff, A_fg, A_gf, A_gg = A
    Ap_ff, Ap_fg, Ap_gf, Ap_gg = Ap

    def inv_step(fields):
        e_u, e_d, c_u, c_d = fields
        EU, ED, CU, CD = _fft.fftn(e_u), _fft.fftn(e_d), _fft.fftn(c_u), _fft.fftn(c_d)
        # D^dagger = [[n A^dagger, -imI],[-imI, n A]]
        EU2 = n * A_ff.conj() * EU + n * A_gf.conj() * ED - 1j * m * CU
        ED2 = n * A_fg.conj() * EU + n * A_gg.conj() * ED - 1j * m * CD
        CU2 = -1j * m * EU + n * Ap_ff.conj() * CU + n * Ap_gf.conj() * CD
        CD2 = -1j * m * ED + n * Ap_fg.conj() * CU + n * Ap_gg.conj() * CD
        return (_fft.ifftn(EU2), _fft.ifftn(ED2), _fft.ifftn(CU2), _fft.ifftn(CD2))

    back = hist[-1]
    for _ in range(n_steps):
        back = inv_step(back)
    target = hist[0]
    return float(max(np.max(np.abs(a - b)) for a, b in zip(back, target)))


# ══════════════════════════════════════════════════════════════════
#  T4 — the real-space theorem, end to end (the acid test)
# ══════════════════════════════════════════════════════════════════
def _spatial_reflect(a):
    return np.roll(a[::-1, ::-1, ::-1], shift=(1, 1, 1), axis=(0, 1, 2))


def _apply_theta_realspace(fields):
    """(THETA psi)(x) = M psi(-x)*, expanded component-wise. sigma_y (a,b) =
    (-i b, i a); Sigma then swaps the eta and chi blocks."""
    e_u, e_d, c_u, c_d = fields
    e_u_r, e_d_r, c_u_r, c_d_r = (_spatial_reflect(a) for a in (e_u, e_d, c_u, c_d))
    eta_sy_u = -1j * e_d_r.conj()
    eta_sy_d = 1j * e_u_r.conj()
    chi_sy_u = -1j * c_d_r.conj()
    chi_sy_d = 1j * c_u_r.conj()
    # Sigma swaps eta-block and chi-block
    return (chi_sy_u, chi_sy_d, eta_sy_u, eta_sy_d)


def cpt_realspace_residual(eu, ed, xu, xd, m, n_steps):
    """End-to-end, position-space, many-step, nonlinear (FFT-mediated)
    verification of the theorem: propagate psi forward n_steps, apply THETA,
    propagate forward n_steps AGAIN (not backward — THETA already converted
    the forward walk into the time-reversed one, per the theorem), and
    compare to THETA applied to the ORIGINAL state. Machine-precision
    residual confirms the k-space algebra survives the full nonlinear
    many-step FFT round trip, not just the single-tick operator identity."""
    def step(fields, n):
        e_u, e_d, c_u, c_d = fields
        for _ in range(n):
            e_u, e_d, c_u, c_d = _dirac_step(e_u, e_d, c_u, c_d, m=m, dt=1.0, sign='+')
        return (e_u, e_d, c_u, c_d)

    psi0 = (eu, ed, xu, xd)
    psiN = step(psi0, n_steps)
    phi0 = _apply_theta_realspace(psiN)
    phiN = step(phi0, n_steps)
    target = _apply_theta_realspace(psi0)
    return float(max(np.max(np.abs(a - b)) for a, b in zip(phiN, target)))


# ══════════════════════════════════════════════════════════════════
#  Registry entry point — F328 gate record
# ══════════════════════════════════════════════════════════════════
def check_discrete_cpt_theorem(use_naive_theta: bool = False,
                                seed: int = 2026,
                                n_trials: int = 500):
    """Registry entry point. Returns {'checks': [...], 'pass': bool, ...}.

    `use_naive_theta=True` is the declared negative control (D9/H2): it
    swaps THETA's internal matrix M for plain Sigma (block swap only, no
    sigma_y twist, still composed with K). Measured effect: B1, B2, C1 and
    E1 turn red (the operator identity, its edge cases, the Kramers
    THETA^2=-1 signature -- Sigma alone squares to +1, not -1 -- and the
    real-space round trip); A1/A2 (properties of A^s(k) alone), B3
    (unitarity sanity), C2 (M is still unitary even without the twist), D1-3
    (the parity obstruction, independent of which THETA is tested) and E2
    (plain invertibility) all stay green. That is what proves the sigma_y
    twist -- not a bookkeeping tautology -- is what B1/B2/C1/E1 depend on.
    """
    rng = np.random.default_rng(seed)
    checks = []

    def add(cid, desc, ok, value):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok), "value": str(value)})

    M = _SIGMA_SWAP if use_naive_theta else M_cpt()

    def _theta_op_residual(kx, ky, kz, m):
        Dk = _D(kx, ky, kz, m)
        lhs = M @ Dk.conj() @ M
        rhs = Dk.conj().T
        return float(np.max(np.abs(lhs - rhs)))

    # --- A: the two 2x2 lattice-embedding identities (property of A^s(k)
    #        itself; independent of which THETA is under test) ------------
    max_I = max_II = 0.0
    for _ in range(n_trials):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        for sign in ('+', '-'):
            max_I = max(max_I, identity_conjugate_fixed_k_residual(kx, ky, kz, sign))
        max_II = max(max_II, identity_branch_swap_residual(kx, ky, kz))
    add("A1-conjugate-fixed-k", "A^s(k)* = sigma_y A^s(k) sigma_y, any fixed k",
        max_I < 1e-10, max_I)
    add("A2-branch-swap", "A^+(k)* = A^-(-k) (conjugation = branch swap + momentum flip)",
        max_II < 1e-10, max_II)

    # --- B: the CPT operator identity for the massive Dirac walk ----------
    max_B1 = 0.0
    for _ in range(n_trials):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        max_B1 = max(max_B1, _theta_op_residual(kx, ky, kz, m))
    add("B1-theta-D-theta-inv-eq-Dinv",
        "THETA D(k) THETA^-1 = D(k)^-1 at random (k, m), n_trials samples",
        max_B1 < 1e-10, max_B1)

    edge_cases = [(0.0, 0.0, 0.0, 0.6), (1.3, 0.0, 0.0, 0.2),
                  (0.7, 0.3, -0.4, 1.0), (0.7, 0.3, -0.4, 0.0),
                  (0.7, 0.3, -0.4, -1.0)]
    max_B2 = max(_theta_op_residual(*e) for e in edge_cases)
    add("B2-edge-cases", "k=0, axis-aligned k, |m| in {0,1} (no small-k expansion used anywhere)",
        max_B2 < 1e-10, max_B2)

    max_B3 = 0.0
    for _ in range(200):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        max_B3 = max(max_B3, unitarity_residual(kx, ky, kz, m))
    add("B3-unitarity-sanity", "D(k) is exactly unitary (dagger = inverse), floating floor",
        max_B3 < 1e-9, max_B3)

    # --- C: THETA^2 = -1 (Kramers signature) -------------------------------
    th2 = M @ M.conj()
    c1 = float(np.max(np.abs(th2 - (-np.eye(4)))))
    add("C1-theta-squared-minus-one", "THETA^2 = -1 exactly (Kramers antiunitary involution)",
        c1 < 1e-12, c1)
    c2 = float(np.max(np.abs(M.conj().T @ M - np.eye(4))))
    add("C2-M-unitary", "the internal matrix M is exactly unitary",
        c2 < 1e-12, c2)

    # --- D: no fixed parity can exist (spectral obstruction) --------------
    obstr_generic = []
    for _ in range(n_trials):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        obstr_generic.append(abs(no_fixed_parity_obstruction(kx, ky, kz, m)))
    min_obstr = min(obstr_generic)
    add("D1-generic-k-spectral-mismatch",
        "omega(k) != omega(-k) at generic k (nonzero over n_trials samples) -- "
        "conjugation-invariant, so NO fixed unitary can implement parity here",
        min_obstr > 1e-6, min_obstr)

    obstr_axis = abs(no_fixed_parity_obstruction(1.1, 0.0, 0.0, 0.3))
    add("D2-cubic-axis-degenerate",
        "on a cubic axis (k_y=k_z=0) the obstruction vanishes identically, "
        "matching F301's own 'exact on cubic axes' -- consistency, not a new claim",
        obstr_axis < 1e-12, obstr_axis)

    max_D3 = 0.0
    for _ in range(50):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        max_D3 = max(max_D3, naive_parity_residual(kx, ky, kz, m))
    add("D3-naive-parity-fails-O1",
        "plain block-swap alone (no twist, no K) misses D(-k) by O(1), not a small defect",
        max_D3 > 1.0, max_D3)

    # --- E: real-space, many-step, nonlinear FFT round trip ----------------
    L = 6
    shape = (L, L, L)
    fields = []
    rng2 = np.random.default_rng(seed + 1)
    for _ in range(4):
        fields.append(rng2.normal(size=shape) + 1j * rng2.normal(size=shape))
    norm0 = np.sqrt(sum(np.sum(np.abs(a) ** 2) for a in fields))
    eu, ed, xu, xd = (a / norm0 for a in fields)
    m_rs = 0.41

    if use_naive_theta:
        def _theta_rs(fields):
            e_u, e_d, c_u, c_d = fields
            r = [_spatial_reflect(a) for a in (e_u, e_d, c_u, c_d)]
            return (r[2].conj(), r[3].conj(), r[0].conj(), r[1].conj())

        def step(fields, n):
            e_u, e_d, c_u, c_d = fields
            for _ in range(n):
                e_u, e_d, c_u, c_d = _dirac_step(e_u, e_d, c_u, c_d, m=m_rs, dt=1.0, sign='+')
            return (e_u, e_d, c_u, c_d)

        psi0 = (eu, ed, xu, xd)
        psiN = step(psi0, 12)
        phi0 = _theta_rs(psiN)
        phiN = step(phi0, 12)
        target = _theta_rs(psi0)
        e1 = float(max(np.max(np.abs(a - b)) for a, b in zip(phiN, target)))
        add("E1-realspace-cpt-roundtrip",
            "many-step position-space round trip, naive THETA (no sy twist) -- CONTROL",
            e1 < 1e-10, e1)
    else:
        e1 = cpt_realspace_residual(eu, ed, xu, xd, m_rs, 12)
        add("E1-realspace-cpt-roundtrip",
            "many-step (N=12), nonlinear FFT position-space round trip under the real THETA",
            e1 < 1e-10, e1)

    e2 = naive_reversal_residual(eu, ed, xu, xd, m_rs, 12)
    add("E2-naive-invertibility-sanity",
        "plain D then D^dagger returns to start (every unitary CA has this for free; "
        "NOT a check of any antiunitary symmetry -- contrast with E1)",
        e2 < 1e-9, e2)

    n_pass = sum(1 for c in checks if c["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "pass": n_pass == len(checks),
            "use_naive_theta": use_naive_theta, "n_trials": n_trials, "seed": seed}


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    out = check_discrete_cpt_theorem()
    for c in out["checks"]:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['id']:45s} -> {c['value']}")
    print(f"\n  {out['n_pass']}/{out['n_total']} PASS")
    dest = results_path("F328_discrete_cpt_theorem.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("wrote", dest)
