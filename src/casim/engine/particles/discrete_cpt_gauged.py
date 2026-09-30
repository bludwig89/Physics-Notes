"""discrete_cpt_gauged.py — F378: extending F328's discrete CPT theorem to the
SU(2)_L-coupled BCC Dirac walk (ledger row A4r / rubric row A4 / claim CL285)
======================================================================================

[[F328]] proved THETA . D(k) . THETA^-1 = D(k)^-1 exactly, every k, every
|m| <= 1, for the FREE (gauge-decoupled) massive BCC Dirac walk
`casim.engine.particles.dirac_bcc`, and named the SU(2)_L charged-current
extension as the residual (ledger row A4r). This module attacks that residual
directly, per the row's own FIRST STEP: build the gauge-coupled one-tick
unitary as an explicit momentum-diagonal matrix (a spatially-uniform SU(2)
link makes `casim.engine.gauge.weak_wmu.covariant_dirac_doublet_step` exactly
momentum-diagonal — its two building blocks, `covariant_weyl_step_3d_bcc` and
the mass mixing, both factorise into (spin operator) (x) (isospin operator)
at a uniform link, since gauge rotation is applied in POSITION space and
commutes with the FFT there), and test F328's THETA against it.

RESULT SHAPE (three findings, not one; the mechanism differs between them)
----------------------------------------------------------------------------
(1) THE ACTUAL MODULE FAILS EVEN AT ZERO GAUGE COUPLING (leg E). Setting the
    kinetic link U and mass link V both to I2 in `covariant_dirac_doublet_step`
    does NOT reproduce F328's D(k): that module's kinetic term pairs branch
    '+' (eta) with the TRUE OPPOSITE branch '-' (chi), not with branch +'s
    OWN DAGGER the way `dirac_bcc.dirac_step_3d_bcc_splitstep` does (the
    pairing F328's docstring calls "the choice forced by unitarity of the
    full 4x4 D_k" for ITS OWN, non-Strang-split mass ansatz). These are two
    different discretisations of "the massive BCC Dirac fermion" already
    present in the tree, and only one of them (`dirac_bcc.py`) has a proven
    CPT theorem. This is a PRE-EXISTING CROSS-MODULE ARCHITECTURE MISMATCH,
    not evidence that SU(2)_L coupling breaks CPT -- named here, not
    resolved (see Scope below).

(2) TO ISOLATE THE ACTUAL GAUGE-COUPLING QUESTION, this module also builds a
    companion construction, `D_grafted`, that inserts the SU(2)_L link
    directly into `dirac_bcc.py`'s OWN branch+/dagger architecture (the one
    F328 covers) -- literally A^+(k) -> A^+(k) (x) U in the kinetic block,
    everything else unchanged. On THIS architecture, grafting a uniform
    SU(2) link into the KINETIC term ALONE (mass staying an isospin scalar)
    admits an EXACT (machine-precision) CPT-type theorem:

        THETA' . D'(k) . THETA'^-1 = D'(k)^-1,
        THETA' := M' . K,   M' := Sigma . (sigma_y (x) tau_2  (+)  sigma_y (x) tau_2),

    using the SU(2) PSEUDOREALITY identity tau_2 U tau_2^-1 = U* for every
    U in SU(2) (tau_2 = sigma_y numerically; the standard fact underlying
    Majorana mass terms and the reality of the SU(2) doublet), which
    generalises F328's identity (I) A^s(k)* = sigma_y A^s(k) sigma_y to the
    isospin factor. THETA'^2 = +1 (NOT F328's Kramers -1): tensoring a
    SECOND pseudoreal (spin-1/2-like) twist onto the first flips the
    antiunitary involution class, a clean and expected consequence of
    Wigner's classification, not a numerical accident.

(3) COMPANION NO-GO (mass sector): once the model's OWN SU(2)-gauged
    mass-generation mechanism (the Stueckelberg/Yukawa-type link V mixing
    eta and chi, exactly as `covariant_dirac_doublet_step` implements it,
    matching CLAUDE.md decision 4's Stueckelberg W-mass story) is ALSO
    switched on, THETA' (and, by the general proof below, NO fixed isospin
    operator Lambda composed with F328's spin/chirality twist) can restore
    the identity. The required relation for the mass sector is DIFFERENT in
    kind from the kinetic sector's: working through the block algebra (see
    `## Derivation` below) shows the mass off-diagonal block needs

        Lambda . V^T . Lambda^-1  =  V           (transpose, not conjugate)

    for every V in SU(2). V |-> V^T is a group ANTI-automorphism
    ((AB)^T = B^T A^T); conjugation by a fixed Lambda is always an
    automorphism; their composition is therefore an anti-automorphism, and
    an anti-automorphism can equal the identity map only on an ABELIAN
    group. SU(2) is not abelian, so NO fixed Lambda satisfies this for
    every V -- a genuine, general, provable obstruction, not "none found
    by search." (Consistency cross-check: tau_2 itself satisfies the
    RELATED-but-different identity tau_2 V^T tau_2^-1 = V^-1 for every V,
    confirmed below to literal 0.0 -- so tau_2 solves a nearby problem, just
    not this one.) Monte-Carlo legs sample many random Lambda (not just the
    two analytic candidates) and many non-commuting V pairs to confirm the
    obstruction is generic, not an artefact of the two Lambda tried.

SCOPE, STATED NARROWLY (do not overclaim)
----------------------------------------------------------------------------
This is NOT a claim that the model's SU(2)_L gauge theory violates CPT as a
physical statement. Every test above holds the classical gauge/mass link
FIXED under the antiunitary map (Theta maps the walk at background (U, V)
to the INVERSE of the walk at the SAME (U, V)) -- the literal discrete
analogue of how F328 tested D(k) against D(k)^-1 at the SAME m. The
continuum Luders-Pauli argument for a real gauge theory instead lets C, P, T
ALSO transform the gauge field itself (e.g. C acting on the connection, not
holding it pointwise fixed); whether allowing THETA to ALSO map the
background (U, V) to some OTHER background (U', V') restores an identity is
a different, more general question this module does not attempt. The
mass-sector no-go proved here is specifically about the FIXED-background
ansatz Theta = (F328 spin/chirality twist) (x) (fixed isospin operator);
it is a real, general, and structurally clean obstruction to THAT ansatz,
not (without further work) a completed statement about the physical theory.
Per CL285's own falsifier text and ledger row A4r's own caution, promoting
this to "the model's SU(2)_L sector violates CPT" would need its own claim
card and a named experimental confrontation -- not attempted here.

References: F328 (the free-sector theorem this extends), F53 (per-species
charge-label C/P/CP), F91 (even/chiral propagator classification),
`casim.engine.gauge.weak_wmu.covariant_dirac_doublet_step` /
`covariant_weyl_step_3d_bcc` (the gauge-coupled walk under test),
`casim.engine.particles.dirac_bcc` (F328's own free-walk module).
"""

from __future__ import annotations

from casim.numerics import xp as np
from casim.engine.lattice import bcc as _bcc

_I2 = np.eye(2, dtype=complex)
_SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_TAU2 = _SIGMA_Y  # numerically identical 2x2 matrix; kept as a separate name
                  # for readability (spin vs isospin factor)
_SIGMA_SWAP8 = np.block([[np.zeros((4, 4)), np.eye(4)],
                         [np.eye(4), np.zeros((4, 4))]]).astype(complex)


def _A(kx, ky, kz, sign='+'):
    """2x2 BCC Weyl unitary A^s(k), same helper as F328's discrete_cpt._A."""
    Uff, Ufg, Ugf, Ugg = _bcc.bcc_unitary(kx, ky, kz, sign=sign)
    return np.array([[Uff, Ufg], [Ugf, Ugg]], dtype=complex)


def random_su2(rng):
    """Haar-uniform SU(2) matrix [[a,-b*],[b,a*]] via a random unit quaternion."""
    q = rng.normal(size=4)
    q = q / np.linalg.norm(q)
    a = q[0] + 1j * q[3]
    b = q[2] + 1j * q[1]
    return np.array([[a, -np.conj(b)], [b, np.conj(a)]], dtype=complex)


# ══════════════════════════════════════════════════════════════════
#  The ACTUAL gauge-coupled walk, momentum-diagonal at a uniform link
#  (matches casim.engine.gauge.weak_wmu.covariant_dirac_doublet_step
#  bit-for-bit -- cross-checked in check_gauged_cpt_theorem leg X0).
#  Basis order: [f_nu, f_e, g_nu, g_e, cf_nu, cf_e, cg_nu, cg_e]
#  (spin-major, isospin-minor within each chirality block).
# ══════════════════════════════════════════════════════════════════
def D_covariant_doublet(kx, ky, kz, m, U, V):
    """The actual `covariant_dirac_doublet_step` one-tick unitary at a
    spatially-uniform kinetic link U (eta only; chi always uses identity
    links -- no SU(2)_L coupling to the right-handed singlet) and mass link
    V, as an explicit 8x8 matrix. Verified against the real module function
    at machine precision (leg X0)."""
    Ap = _A(kx, ky, kz, '+')
    Am = _A(kx, ky, kz, '-')
    K = np.zeros((8, 8), dtype=complex)
    K[0:4, 0:4] = np.kron(Ap, U)
    K[4:8, 4:8] = np.kron(Am, _I2)

    cm, sm = np.cos(m), np.sin(m)
    Vk = np.kron(_I2, V)
    Vd = np.kron(_I2, V.conj().T)
    Mass = np.zeros((8, 8), dtype=complex)
    Mass[0:4, 0:4] = cm * np.eye(4)
    Mass[0:4, 4:8] = 1j * sm * Vk
    Mass[4:8, 0:4] = 1j * sm * Vd
    Mass[4:8, 4:8] = cm * np.eye(4)

    return K @ Mass @ K


# ══════════════════════════════════════════════════════════════════
#  Comparison construction: graft the SU(2)_L link directly into
#  dirac_bcc.py's OWN branch+/dagger architecture (the one F328 covers),
#  to isolate the gauge-coupling question from the cross-module branch-
#  pairing mismatch above. V=None keeps the mass term an isospin scalar
#  (im * I4); V != None SU(2)-gauges the mass term too.
# ══════════════════════════════════════════════════════════════════
def D_grafted(kx, ky, kz, m, U, V=None):
    Ap = _A(kx, ky, kz, '+')
    n = float(np.sqrt(max(0.0, 1.0 - m * m)))
    Kblk = np.kron(Ap, U)
    Kdag = Kblk.conj().T
    D = np.zeros((8, 8), dtype=complex)
    D[0:4, 0:4] = n * Kblk
    D[4:8, 4:8] = n * Kdag
    if V is None:
        D[0:4, 4:8] = 1j * m * np.eye(4)
        D[4:8, 0:4] = 1j * m * np.eye(4)
    else:
        D[0:4, 4:8] = 1j * m * np.kron(_I2, V)
        D[4:8, 0:4] = 1j * m * np.kron(_I2, V.conj().T)
    return D


def M_cpt_gauged(iso_op):
    """F328's M = Sigma . (sigma_y (+) sigma_y), generalised to the 8-dim
    doublet space with a chosen isospin operator acting alongside sigma_y:
    Sigma_8 . (sigma_y (x) iso_op  (+)  sigma_y (x) iso_op)."""
    block = np.kron(_SIGMA_Y, iso_op)
    full = np.zeros((8, 8), dtype=complex)
    full[0:4, 0:4] = block
    full[4:8, 4:8] = block
    return _SIGMA_SWAP8 @ full


M_ISO_UNTOUCHED = M_cpt_gauged(_I2)
M_TAU2 = M_cpt_gauged(_TAU2)


def theta_squared(M):
    return M @ M.conj()


def cpt_operator_residual(D_fn_result, M):
    """|M D* M - D^-1| for a precomputed 8x8 unitary D."""
    Dk = D_fn_result
    lhs = M @ Dk.conj() @ M
    rhs = np.linalg.inv(Dk)
    return float(np.max(np.abs(lhs - rhs)))


def unitarity_residual(Dk):
    return float(np.max(np.abs(Dk.conj().T @ Dk - np.eye(8))))


# ══════════════════════════════════════════════════════════════════
#  The two isospin group-theory identities (the algebraic content the
#  two results above rest on).
# ══════════════════════════════════════════════════════════════════
def kinetic_isospin_identity_residual(U, iso_op=_TAU2):
    """|iso_op . U . iso_op^-1 - U*| -- generalises F328 identity (I) to
    the isospin factor. tau_2 satisfies this EXACTLY for every U in SU(2)
    (the standard pseudoreality of the fundamental SU(2) representation)."""
    lhs = iso_op @ U @ np.linalg.inv(iso_op)
    return float(np.max(np.abs(lhs - U.conj())))


def mass_isospin_required_identity_residual(V, iso_op):
    """|iso_op . V^T . iso_op^-1 - V| -- the relation the MASS sector's
    off-diagonal block actually needs (derived in the module docstring's
    ## Derivation-equivalent block algebra). Group theory: V -> V^T is an
    anti-automorphism of SU(2); conjugation by a fixed iso_op is always an
    automorphism; their composition is an anti-automorphism, which can
    equal the identity map only if SU(2) were abelian. So this residual
    cannot be driven to zero for every V by ANY fixed iso_op -- verified
    below both algebraically (this docstring) and by Monte-Carlo search
    over random iso_op (leg D2)."""
    lhs = iso_op @ V.T @ np.linalg.inv(iso_op)
    return float(np.max(np.abs(lhs - V)))


def tau2_transpose_gives_inverse_residual(V):
    """Consistency cross-check: tau_2 . V^T . tau_2^-1 = V^-1 (a TRUE
    identity for every V in SU(2), distinct from the required-but-
    impossible V^T -> V relation above). Confirms tau_2 solves a
    neighbouring problem, not this one."""
    lhs = _TAU2 @ V.T @ np.linalg.inv(_TAU2)
    return float(np.max(np.abs(lhs - np.linalg.inv(V))))


def random_unitary_2x2(rng):
    """Haar-random U(2) matrix (broader search space than SU(2) alone, for
    the Monte-Carlo Lambda-search control -- a fixed antiunitary's isospin
    part need not itself be special-unitary)."""
    z = (rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)))
    Q, R = np.linalg.qr(z)
    d = np.diag(R) / np.abs(np.diag(R))
    return Q @ np.diag(d)


# ══════════════════════════════════════════════════════════════════
#  Registry entry point — F378 gate/battery record
# ══════════════════════════════════════════════════════════════════
def check_gauged_cpt_theorem(seed: int = 2026, n_trials: int = 300,
                              use_naive_iso: bool = False):
    """Registry entry point. `use_naive_iso=True` is the declared negative
    control (D9/H2): swaps the isospin twist tau_2 for the trivial I2 in the
    B1/B2/C1 legs (the kinetic-sector positive result). Expected effect:
    B1, B2 and C1 turn red (I2 does not satisfy the kinetic pseudoreality
    identity, so the operator theorem fails and Theta^2 is unaffected --
    I2 (+) I2 tensored with sigma_y still squares to -1, so C1 reddens for
    a DIFFERENT reason: the theorem it is supposed to certify no longer
    holds). X0 (module cross-check), A1 (a fact about tau_2 alone,
    independent of which isospin op the operator theorem under test uses),
    B3 (unitarity, isospin-independent), D1 (also a fact about tau_2 alone),
    D2 (the mass no-go, present regardless), D3 (the Lambda-search control,
    independent of this switch) and E1 (the zero-coupling cross-module
    mismatch, independent of isospin choice since U=V=I there) all stay
    green."""
    rng = np.random.default_rng(seed)
    iso_M = M_ISO_UNTOUCHED if use_naive_iso else M_TAU2
    checks = []

    def add(cid, desc, ok, value):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok), "value": str(value)})

    # --- X0: cross-check D_covariant_doublet against the REAL module ------
    from casim.engine.gauge.weak_wmu import covariant_dirac_doublet_step
    L = 6
    shape = (L, L, L)
    rng_x = np.random.default_rng(11)
    U0 = random_su2(rng_x)
    V0 = random_su2(rng_x)
    m0 = 0.37
    Ua_field = np.full(shape, U0[0, 0], dtype=complex)
    Ub_field = np.full(shape, U0[1, 0], dtype=complex)
    U_links = [(Ua_field, Ub_field) for _ in range(8)]
    Va_field = np.full(shape, V0[0, 0], dtype=complex)
    Vb_field = np.full(shape, V0[1, 0], dtype=complex)
    n_idx = (1, -2, 1)
    kx0, ky0, kz0 = (2 * np.pi * ni / L for ni in n_idx)
    xs = np.arange(L)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing='ij')
    plane = np.exp(1j * (kx0 * X + ky0 * Y + kz0 * Z))
    D_closed = D_covariant_doublet(kx0, ky0, kz0, m0, U0, V0)
    max_x0 = 0.0
    for j in range(8):
        basis = np.zeros(8, dtype=complex)
        basis[j] = 1.0
        fields = [basis[i] * plane for i in range(8)]
        out = covariant_dirac_doublet_step(*fields, U_links, Va_field, Vb_field, m0, dt=1.0)
        ratios = np.array([out[i][0, 0, 0] / plane[0, 0, 0] for i in range(8)])
        max_x0 = max(max_x0, float(np.max(np.abs(ratios - D_closed[:, j]))))
    add("X0-closed-form-matches-real-module",
        "D_covariant_doublet(k) reproduces the real covariant_dirac_doublet_step "
        "output exactly, at a uniform link, grid-compatible k",
        max_x0 < 1e-10, max_x0)

    # --- E: the ACTUAL module fails already at U=V=I (branch mismatch) ----
    max_e = 0.0
    for _ in range(n_trials):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        Dk = D_covariant_doublet(kx, ky, kz, m, _I2, _I2)
        max_e = max(max_e, cpt_operator_residual(Dk, M_ISO_UNTOUCHED))
    add("E1-actual-module-fails-at-zero-coupling",
        "covariant_dirac_doublet_step's OWN architecture (branch -, not "
        "branch+dagger) fails F328's identity even at U=V=I -- a "
        "pre-existing cross-module branch-pairing mismatch, NOT a gauge-"
        "coupling effect (expected large, not small)",
        max_e > 1.0, max_e)

    # --- Kinetic-sector positive result (D_grafted, V=None, Lambda=tau2) --
    max_a = 0.0
    for _ in range(n_trials):
        U = random_su2(rng)
        max_a = max(max_a, kinetic_isospin_identity_residual(U, _TAU2))
    add("A1-kinetic-pseudoreality-identity",
        "tau_2 U tau_2^-1 = U* for every U in SU(2) (generalises F328 identity I)",
        max_a < 1e-10, max_a)

    max_b1 = 0.0
    for _ in range(n_trials):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        U = random_su2(rng)
        Dk = D_grafted(kx, ky, kz, m, U, V=None)
        max_b1 = max(max_b1, cpt_operator_residual(Dk, iso_M))
    add("B1-kinetic-only-cpt-theorem",
        "Theta' = Sigma.(sigma_y (x) tau_2 (+) sigma_y (x) tau_2).K exactly "
        "intertwines D_grafted (SU(2) kinetic coupling, scalar mass) with "
        "its inverse, random (k, m, U)",
        max_b1 < 1e-10, max_b1)

    edge_cases = [(0.0, 0.0, 0.0, 0.6), (1.3, 0.0, 0.0, 0.2),
                  (0.7, 0.3, -0.4, 1.0), (0.7, 0.3, -0.4, 0.0),
                  (0.7, 0.3, -0.4, -1.0)]
    max_b2 = 0.0
    for e in edge_cases:
        U = random_su2(rng)
        Dk = D_grafted(*e, U, V=None)
        max_b2 = max(max_b2, cpt_operator_residual(Dk, iso_M))
    add("B2-kinetic-only-edge-cases",
        "k=0, axis-aligned k, |m| in {0,1} -- no small-k expansion used anywhere",
        max_b2 < 1e-10, max_b2)

    max_b3 = 0.0
    for _ in range(100):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        U = random_su2(rng)
        max_b3 = max(max_b3, unitarity_residual(D_grafted(kx, ky, kz, m, U, V=None)))
    add("B3-unitarity-sanity", "D_grafted (kinetic-only) exactly unitary",
        max_b3 < 1e-9, max_b3)

    c1_plus = float(np.max(np.abs(theta_squared(iso_M) - np.eye(8))))
    c1_minus = float(np.max(np.abs(theta_squared(iso_M) - (-np.eye(8)))))
    add("C1-theta-squared-is-plus-one-not-kramers",
        "Theta'^2 = +1 (residual to +I), NOT F328's Kramers -1 (residual to "
        "-I reported separately) -- tensoring a second pseudoreal twist "
        "onto the spin twist flips the antiunitary involution class",
        c1_plus < 1e-12, c1_plus)
    add("C1b-theta-squared-not-minus-one",
        "confirms Theta'^2 != -1 (residual to -I is O(1), the flip is real)",
        c1_minus > 1.0, c1_minus)

    # --- Mass-sector no-go -------------------------------------------------
    max_d1_tau2_iso = 0.0
    for _ in range(n_trials):
        U = random_su2(rng)
        max_d1_tau2_iso = max(max_d1_tau2_iso, tau2_transpose_gives_inverse_residual(U))
    add("D1-tau2-transpose-gives-inverse-not-self",
        "tau_2 V^T tau_2^-1 = V^-1 exactly for every V (a true, different "
        "identity from the one the mass sector needs)",
        max_d1_tau2_iso < 1e-10, max_d1_tau2_iso)

    max_d2 = 0.0
    for _ in range(n_trials):
        kx, ky, kz = rng.uniform(-np.pi, np.pi, 3)
        m = rng.uniform(-1, 1)
        U = random_su2(rng)
        V = random_su2(rng)
        Dk = D_grafted(kx, ky, kz, m, U, V=V)
        max_d2 = max(max_d2, cpt_operator_residual(Dk, M_TAU2))
    add("D2-gauged-mass-breaks-identity",
        "grafting an independent SU(2) mass link V (matching "
        "covariant_dirac_doublet_step's own Stueckelberg mass architecture) "
        "breaks Theta' at O(1), random (k, m, U, V) -- the localised residual",
        max_d2 > 1.0, max_d2)

    # Monte-Carlo Lambda search: no fixed 2x2 unitary Lambda satisfies the
    # mass-sector requirement for a fixed pair of non-commuting V1, V2
    # simultaneously (the anti-automorphism obstruction is generic, not
    # specific to I2/tau2).
    rng_v = np.random.default_rng(seed + 99)
    V1 = random_su2(rng_v)
    V2 = random_su2(rng_v)
    min_over_lambda = np.inf
    for _ in range(500):
        Lam = random_unitary_2x2(rng_v)
        r1 = mass_isospin_required_identity_residual(V1, Lam)
        r2 = mass_isospin_required_identity_residual(V2, Lam)
        min_over_lambda = min(min_over_lambda, max(r1, r2))
    add("D3-no-lambda-search-control",
        "Monte-Carlo over 500 random unitary 2x2 Lambda: none satisfies "
        "Lambda V^T Lambda^-1 = V simultaneously for two fixed non-commuting "
        "V1, V2 -- the best found residual stays O(1), consistent with the "
        "algebraic anti-automorphism obstruction being generic",
        min_over_lambda > 0.1, min_over_lambda)

    n_pass = sum(1 for c in checks if c["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "pass": n_pass == len(checks),
            "n_trials": n_trials, "seed": seed, "use_naive_iso": use_naive_iso}


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    out = check_gauged_cpt_theorem()
    for c in out["checks"]:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['id']:45s} -> {c['value']}")
    print(f"\n  {out['n_pass']}/{out['n_total']} PASS")
    dest = results_path("F378_discrete_cpt_gauged_theorem.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("wrote", dest)
