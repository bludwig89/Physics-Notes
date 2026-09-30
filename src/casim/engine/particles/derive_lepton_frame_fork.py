"""
casim.engine.particles.derive_lepton_frame_fork
===============================================

F406 -- Deciding the charged-lepton frame fork energetically: picture (a), the
E_g-diagonal condensate (cube-axis eigenstates, residual D_2h), against picture
(b), the [111] trigonal circulant (trimaximal eigenstates, residual C3).  This
is next-derivation #2 of the 2026-09-24 flavour report
(`reports/Quark neutrino hierarchy lattice fit.md`) and open step (i) of F403.

The two pictures carry the SAME Koide spectrum, Y_b = F Y_a F^dagger with F the
Z3 Fourier (trimaximal) matrix and Y the amplitude matrix sqrt(M).  The
question "which is the ground state at the F118 couplings" therefore has three
layers, and this module tests each.

1. The F118 functional and the derived Dirac sea are SPECTRAL.  Every F118
   term is a symmetric function of the three amplitudes (ybar, e^2 = Tr P^2,
   S3 = Tr P^3, sum y^4 = Tr Y^4, the clock (Tr P^3)^2, the sea sum_a g(y_a)),
   so its natural extension to a Hermitian Y is U(3)-invariant and (a), (b)
   and every other orientation of the spectrum are exactly degenerate (K1,
   sympy).  The sea is not merely extendable that way: with a generation-
   blind BCC walk the 3-generation Dirac step is covariant under generation
   unitaries, so its sea energy is identical at (a) and (b) to machine
   precision (K2, the real F46/F95 D_k built from `lattice.bcc`).  The F118
   couplings cannot decide the fork.

2. What CAN decide it is the O_h x T crystal-field anisotropy: the invariants
   that vanish on diagonal matrices (the kernel of the restriction to F118's
   domain).  There are 2 at quadratic order and 6 through cubic order (K7,
   Molien series over O_h x T, exact).  Both (a) and (b) are Michel critical
   orbits -- stationary for EVERY invariant functional -- because their
   stabilisers (D2, C3) have finite fixed-point sets on the fixed-spectrum
   orbit (K6).

3. The [111]-circulant realisation is not unique.  The spectrum admits three
   O_h-inequivalent Hermitian circulants, arg b in {2/9, 2/9 + 2pi/3,
   2/9 - 2pi/3} (K3).  The C3-invariant direction (1,1,1) carries mass
   a + 2 Re b, which is tau, e and mu on the three branches.  TM1 (F403's
   opening) needs the ELECTRON on (1,1,1), i.e. branch b2; the report's
   reading tan(delta*) = T1g/T2g along [111] is branch b1 (K4, K5).  The two
   selling points of picture (b) live on different vacua.

   At quadratic order the crystal field is alpha R + beta I (R, I = T2g and
   T1g weights of the off-diagonal part) and the phase diagram is exact (K8):
   (a) for alpha, beta > 0; a real constant-diagonal texture for
   alpha < min(0, beta); the circulant b3 for beta < alpha < 0; a T1g e-tau
   block texture for beta < 0 < alpha.  b1 and b2 are never strict ground
   states (their T1g fraction lies strictly between two competitors').  With
   the six cubic invariants they become reachable in a small fraction of
   coupling space (K9, indicative, prior-dependent).

Exactness: K1, K3-K7 and the K8 inequalities are exact (sympy / closed-form
bounds); K2 is machine precision; K4's data comparison and K9 are quantitative.
"""
from __future__ import annotations

import itertools
import math

import sympy as sp

from casim.constants import delta_star
from casim.engine.lattice import bcc
from casim.engine.particles import derive_oh_residual_pmns as oh
from casim.engine.particles.eg_sextic import _bz_omegas, _f_of_m
from casim.numerics import xp

# ---- the spectrum ----------------------------------------------------------
# sqrt(m_n) = mu (1 + sqrt2 cos(delta* + 2 pi n / 3)), n = 0 (tau), 1 (e), 2 (mu)
# (F175 / decision 7; eta^2 = 1/2).  mu = 1 throughout: only ratios matter.
DELTA = sp.Rational(delta_star.numerator, delta_star.denominator)
SQRT2 = sp.sqrt(2)
LEPTON_OF_N = ("tau", "e", "mu")
W = oh.W                                          # primitive cube root of unity


def _lam_sym(delta=DELTA):
    return [1 + SQRT2 * sp.cos(delta + 2 * sp.pi * n / 3) for n in range(3)]


def _lam_num(delta=float(DELTA)):
    return xp.array([1 + math.sqrt(2) * math.cos(delta + 2 * math.pi * n / 3) for n in range(3)])


def _fourier_sym():
    return sp.Matrix(3, 3, lambda a, k: W ** (a * k)) / sp.sqrt(3)


def _fourier_num():
    w = complex(sp.N(W, 20))
    return xp.array([[w ** (a * k) for k in range(3)] for a in range(3)]) / math.sqrt(3)


def _perm_P_num():
    """Cyclic permutation P (C3 about [111]): P[i, i+1] = 1."""
    return xp.roll(xp.eye(3), 1, axis=1)


def circulant_num(phi, delta=float(DELTA)):
    """a 1 + b P + b* P^2 with a = mean amplitude, |b| fixed by the spectrum, arg b = phi."""
    lam = _lam_num(delta)
    a = float(lam.mean())
    r = math.sqrt(float(((lam - a) ** 2).sum()) / 6.0)
    P = _perm_P_num()
    return a * xp.eye(3) + r * (complex(math.cos(phi), math.sin(phi)) * P
                                + complex(math.cos(phi), -math.sin(phi)) * P.T)


BRANCHES = {"b1": 0, "b2": 1, "b3": -1}   # arg b = delta* + j 2pi/3; mode n then carries lambda_{n+j}


def branch_num(k, delta=float(DELTA)):
    return circulant_num(delta + BRANCHES[k] * 2 * math.pi / 3, delta)


# ---- crystal-field kernel invariants (vanish on diagonal Y) -----------------
_PAIRS = ((0, 1, 2), (1, 2, 0), (0, 2, 1))


def kernel_invariants(Y):
    """The six O_h x T invariants through cubic order that vanish on diagonal Y.

    R = sum (Re Y_ab)^2 (T2g weight), I = sum (Im Y_ab)^2 (T1g weight),
    sum d_c (Re Y_ab)^2, sum d_c (Im Y_ab)^2 (c the third index),
    x12 x23 x13, and Re(Y12 Y23 Y31) - x12 x23 x13.  Y may carry leading batch axes.
    """
    Y = xp.asarray(Y)
    dg = xp.real(xp.einsum("...ii->...i", Y))
    x = xp.stack([Y[..., a, b].real for a, b, _ in _PAIRS], -1)
    y = xp.stack([Y[..., a, b].imag for a, b, _ in _PAIRS], -1)
    dc = xp.stack([dg[..., c] for _, _, c in _PAIRS], -1)
    t = Y[..., 0, 1] * Y[..., 1, 2] * Y[..., 2, 0]
    xxx = x[..., 0] * x[..., 1] * x[..., 2]
    return xp.stack([(x ** 2).sum(-1), (y ** 2).sum(-1), (dc * x ** 2).sum(-1),
                     (dc * y ** 2).sum(-1), xxx, t.real - xxx], -1)


def _signed_perms_num():
    out = []
    for p in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            R = xp.zeros((3, 3))
            for i in range(3):
                R[i, p[i]] = s[i]
            out.append(R)
    return out


# ---- Molien counting (exact) ----------------------------------------------
def _coord_action(R, conj):
    """9x9 real matrix of Y -> R Y R^T (then complex conjugation if conj) on the
    coordinates (d1, d2, d3, x12, x23, x13, y12, y23, y13)."""
    basis = []
    idx = [(0, 0), (1, 1), (2, 2)]
    offd = [(0, 1), (1, 2), (0, 2)]
    for i, j in idx:
        E = sp.zeros(3, 3); E[i, j] = 1; basis.append(E)
    for i, j in offd:
        E = sp.zeros(3, 3); E[i, j] = 1; E[j, i] = 1; basis.append(E)
    for i, j in offd:
        E = sp.zeros(3, 3); E[i, j] = sp.I; E[j, i] = -sp.I; basis.append(E)

    def coords(Y):
        return [sp.re(Y[i, i]) for i, _ in idx] + [sp.re(Y[i, j]) for i, j in offd] \
            + [sp.im(Y[i, j]) for i, j in offd]
    cols = []
    for E in basis:
        Z = R * E * R.T
        if conj:
            Z = Z.conjugate()
        cols.append(coords(Z))
    return sp.Matrix(cols).T


def molien_counts(max_deg=3):
    """Number of O_h x T invariant polynomials of degree d on Hermitian 3x3 Y,
    and the kernel dimension (minus the p_3(d) symmetric polynomials of the
    diagonal, which the restriction hits surjectively via Tr Y^k)."""
    t = sp.symbols("t")
    mats = [_coord_action(R, c) for R in oh._full_oh() for c in (False, True)]
    # 1/det(1 - tA) = exp(sum_k tr(A^k) t^k / k): exact integer traces
    tot = 0
    for A in mats:
        tr = [(A ** k).trace() for k in range(1, max_deg + 1)]
        tot += sp.series(sp.exp(sum(sp.Rational(tr[k - 1], k) * t ** k
                                    for k in range(1, max_deg + 1))), t, 0, max_deg + 1).removeO()
    ser = sp.expand(tot / len(mats))
    n_inv = {d: int(ser.coeff(t, d)) for d in range(1, max_deg + 1)}
    p3 = {d: sum(1 for a in range(d + 1) for b in range(a, d + 1) if a + b <= d
                 and d - a - b >= b) for d in range(1, max_deg + 1)}
    return n_inv, {d: n_inv[d] - p3[d] for d in n_inv}


# ---- the 3-generation BCC Dirac sea (F46/F95), matrix mass ------------------
def _mfun(Y, f):
    ev, V = xp.linalg.eigh(Y)
    return V @ xp.diag(f(ev)) @ V.conj().T


def sea_energy(Y, L=6, generation_blind=True):
    """-sum |eigenphase| / (2 L^3) of the 12x12 step
        D = [[N (x) A_k, i M (x) 1], [i M (x) 1, N (x) A_k^dagger]],
    M = Y^2 (m = y^2, F78), N = sqrt(1 - M^2), both BCC branches.  With
    generation_blind=False generation 0 hops on the opposite helicity branch
    (a unitary, generation-NON-blind walk: the negative control)."""
    ev, V = xp.linalg.eigh(xp.asarray(Y))
    ev = ev / ev.max()                                # tau wall-pinned: y_tau = 1 exactly
    Vd = V.conj().T
    M = V @ xp.diag(ev ** 2) @ Vd                     # m = y^2 (F78)
    # N from the same eigenbasis: sqrt(1 - m^2) vanishes EXACTLY at the wall
    # (building it as sqrt of the matrix 1 - M^2 would take sqrt(roundoff) ~ 1e-8)
    N = V @ xp.diag(xp.sqrt(1 - ev ** 4)) @ Vd
    k = 2 * math.pi * xp.fft.fftfreq(L)
    tot = 0.0
    I2 = xp.eye(2)
    Z6 = xp.zeros((6, 6), dtype=complex)
    coin = xp.block([[xp.kron(N, I2), 1j * xp.kron(M, I2)], [1j * xp.kron(M, I2), xp.kron(N, I2)]])
    for s in "+-":
        for kx, ky, kz in itertools.product(k, k, k):
            blocks = []
            for g in range(3):
                sg = s if (generation_blind or g) else ("-" if s == "+" else "+")
                a = bcc.bcc_unitary(kx, ky, kz, sign=sg)
                blocks.append(xp.array([[complex(a[0]), complex(a[1])],
                                        [complex(a[2]), complex(a[3])]]))
            if generation_blind:
                # the F46/F95 D_k with a matrix mass (generation (x) spinor)
                D = xp.block([[xp.kron(N, blocks[0]), 1j * xp.kron(M, I2)],
                              [1j * xp.kron(M, I2), xp.kron(N, blocks[0].conj().T)]])
            else:
                # control: generation 0 hops on the other helicity branch; shift x coin is unitary
                B = Z6.copy()
                for g in range(3):
                    B[2 * g:2 * g + 2, 2 * g:2 * g + 2] = blocks[g]
                D = xp.block([[B, Z6], [Z6, B.conj().T]]) @ coin
            tot += float(xp.abs(xp.angle(xp.linalg.eigvals(D))).sum())
    return -tot / (2 * L ** 3)


# ---- fixed-assignment PMNS viability ---------------------------------------
def _column_viable_fixed(p, data, n=121, tol=1e-9):
    """Is (|U_e i|^2, |U_mu i|^2, |U_tau i|^2) = p for SOME column i of SOME PMNS
    matrix in the 3-sigma box?  Same scan as F403's `_column_viable`, but the
    rows are FIXED (the circulant branch decides which lepton sits where)."""
    cmin, cmax = oh._cos_range(data["delta_deg"])
    s12lo, s12hi = data["s12sq"]
    s23lo, s23hi = data["s23sq"]
    t13lo, t13hi = (math.radians(x) for x in data["th13_deg"])
    pe, pm, pt = (float(x) for x in p)
    if math.sin(t13lo) ** 2 - tol <= pe <= math.sin(t13hi) ** 2 + tol and pe < 1:
        if s23lo - tol <= pm / (1 - pe) <= s23hi + tol:
            return True
    for t13 in oh._grid(t13lo, t13hi, 21):
        c13sq = math.cos(t13) ** 2
        s13 = math.sin(t13)
        for col in (1, 2):
            x = pe / c13sq
            if not (0 <= x <= 1):
                continue
            s12sq = 1 - x if col == 1 else x
            if not (s12lo - tol <= s12sq <= s12hi + tol):
                continue
            s12, c12 = math.sqrt(s12sq), math.sqrt(1 - s12sq)
            for s23sq in oh._grid(s23lo, s23hi, n):
                s23, c23 = math.sqrt(s23sq), math.sqrt(1 - s23sq)
                a, b = (s12 * c23, c12 * s23 * s13) if col == 1 else (c12 * c23, s12 * s23 * s13)
                sgn = 1.0 if col == 1 else -1.0
                ends = (a * a + b * b + sgn * 2 * a * b * cmin, a * a + b * b + sgn * 2 * a * b * cmax)
                if min(ends) - 1e-4 <= pm <= max(ends) + 1e-4:
                    return True
    return False


def branch_columns(j):
    """Exact PMNS columns (rows e, mu, tau) from every 1-dim eigenline of the 23
    rotations of O, with the charged leptons on the Fourier modes that the
    circulant branch assigns them."""
    F = _fourier_sym()
    # mode n carries a + 2|b| cos(delta* + j 2pi/3 + 2 pi n/3) = lambda_{n + j}
    mode_of = {LEPTON_OF_N[(n + j) % 3]: n for n in range(3)}
    cols = set()
    for R in oh._rotations():
        if R == sp.eye(3):
            continue
        for _, v in oh._one_dim_eigenlines(R):
            c = F.H * v
            mods = tuple(sp.nsimplify(sp.simplify(sp.Abs(c[mode_of[l]]) ** 2)) for l in ("e", "mu", "tau"))
            cols.add(mods)
    return mode_of, sorted(cols, key=str)


# ---- quadratic crystal-field phase diagram (exact) --------------------------
def quadratic_phase(alpha, beta, delta=float(DELTA), imax_scale=1.0):
    """Ground state of alpha R + beta I on the fixed-spectrum orbit, from the exact
    bounds R + I <= D (Cauchy-Schwarz on the diagonal) and I <= ((l_max - l_min)/2)^2
    (operator norm of Im Y = (Y - Y^T)/2i; for 3x3 antisymmetric K, ||K||_op^2 = sum_{a<b} K_ab^2)."""
    lam = _lam_num(delta)
    D = float(((lam - lam.mean()) ** 2).sum()) / 2
    Imax = imax_scale * ((float(lam.max()) - float(lam.min())) / 2) ** 2
    cands = {"a": 0.0, "real_constant_diagonal": alpha * D,
             "b3_circulant": alpha * (D - Imax) + beta * Imax, "T1g_block": beta * Imax}
    ok = {"a": alpha > 0 and beta > 0,
          "real_constant_diagonal": alpha < 0 and alpha < beta,
          "b3_circulant": beta < alpha < 0,
          "T1g_block": beta < 0 < alpha}
    win = [k for k, v in ok.items() if v]
    if min(abs(alpha), abs(beta), abs(alpha - beta)) < 1e-9:
        win = []                                      # on a phase boundary: ties, no unique winner
    return (win[0] if len(win) == 1 else "boundary"), cands, D, Imax


def _unitary_batch(rng, n, scale=None):
    Z = rng.normal(size=(n, 3, 3)) + 1j * rng.normal(size=(n, 3, 3))
    if scale is None:
        Q, _ = xp.linalg.qr(Z)
        return Q
    H = (Z + xp.conj(xp.swapaxes(Z, 1, 2))) * (scale / 2)
    ev, V = xp.linalg.eigh(H)
    return V @ (xp.exp(1j * ev)[..., None] * xp.conj(xp.swapaxes(V, 1, 2)))


def _real_constant_diagonal(delta=float(DELTA)):
    """Real symmetric texture with constant diagonal and the Koide spectrum:
    off-diagonals (p, p, r), 2p^2 + r^2 = D, 2 p^2 r = prod(l - lbar)."""
    lam = _lam_num(delta)
    mu = lam - lam.mean()
    D = float((mu ** 2).sum()) / 2
    det = float(mu.prod())
    roots = xp.roots([-1.0, 0.0, D, -det])           # r (D - r^2) = det
    r = max(float(z.real) for z in roots if abs(z.imag) < 1e-12 and D - z.real ** 2 > 0)
    p = math.sqrt((D - r * r) / 2)
    a = float(lam.mean())
    return xp.array([[a, p, p], [p, a, r], [p, r, a]], dtype=complex)


# ---- F118 read literally per axis (diagonal-entry extension) ---------------
F118_DRIVER = "tests/findings/test_F118_self_consistent_Wvc_and_C.py"
F118_V, F118_C = 0.16, 1.10          # F118 section 4 representative closure point (fitted there)


def f118_per_axis_fork(v=F118_V, c=F118_C):
    """E(b) - E(a) with every F118 term read on the DIAGONAL ENTRIES of Y.

    F118 has no engine module: its functional (sea tables, wall-pinned closed-form
    refit, W*(v)) lives in its driver, which is loaded here by path.  A circulant
    has constant diagonal ybar, so on diagonal entries it sits at the unbroken
    point (ybar, ybar, ybar).  The kappa_E e^2 term alone contributes
    alpha = beta = -kappa_E to the quadratic crystal field alpha R + beta I."""
    import pathlib
    import types
    root = pathlib.Path(__file__).resolve().parents[4]
    src = (root / F118_DRIVER).read_text()
    # the driver is a legacy script that runs (and writes its JSON) below its
    # definitions; execute only the definitions (sea tables, refit, W*, E)
    mod = types.SimpleNamespace()
    ns = {"__file__": str(root / F118_DRIVER), "__name__": "_f118_definitions"}
    exec(compile(src[:src.index("def constrained_H2")], F118_DRIVER, "exec"), ns)
    mod.__dict__.update(ns)
    W, _ = mod.Wstar_of_v(v)
    Et, kE, _, _, _ = mod.make_Et(W, v, c)
    Y = mod.Y_DAT
    ybar = xp.full(3, float(Y.mean()))
    e_a, e_b = float(Et(Y)[0]), float(Et(ybar)[0])
    sea_a, sea_b = float(mod.g_of(Y).sum()), float(mod.g_of(ybar).sum())
    return {"W": float(W), "kappa_E": float(kE), "dE_all_per_axis": e_b - e_a,
            "dE_sea_spectral_landau_per_axis": (e_b - sea_b) - (e_a - sea_a),
            "alpha_eq_beta_from_kE": -float(kE)}


# ---- the gate entry ---------------------------------------------------------
def check_lepton_frame_fork(sea_L: int = 6, sea_generation_blind: bool = True,
                            s12sq_band: str = "juno", n_samples: int = 120000,
                            n_couplings: int = 3000, seed: int = 20260924,
                            imax_scale: float = 1.0) -> dict:
    """Run legs K1-K9 and the verdict V.  Returns {checks, pass, params}."""
    checks = {}

    def rec(name, ok, detail=None):
        checks[name] = {"pass": bool(ok), **{k: str(v) for k, v in (detail or {}).items()}}

    rng = xp.random.default_rng(seed)
    lam = _lam_num()
    Ya = xp.diag(lam).astype(complex)
    Fn = _fourier_num()
    Yb = Fn @ Ya @ Fn.conj().T
    Yk = {k: branch_num(k) for k in BRANCHES}

    def orbit_sample(n, Y0=Ya, scale=None):
        U_ = _unitary_batch(rng, n, scale)
        return U_ @ Y0 @ xp.conj(xp.swapaxes(U_, 1, 2))

    # K1 -- F118 is spectral: Tr(Y_b^k) = sum lambda^k exactly, symbolic spectrum
    l1, l2, l3 = sp.symbols("l1 l2 l3", real=True)
    F = _fourier_sym()
    Yb_s = F * sp.diag(l1, l2, l3) * F.H
    ok1 = all(sp.simplify(sp.expand((Yb_s ** k).trace() - (l1 ** k + l2 ** k + l3 ** k))) == 0
              for k in range(1, 7))
    rec("K1_f118_spectral_reading_exact_tie", ok1,
        {"identity": "Tr(F diag(l) F^+)^k = sum l^k, k=1..6 (sympy; an identity, true for any unitary)",
         "consequence": "every F118 term (ybar, e^2, S3, sum y^4, clock, sum g) is a function of Tr Y^k: E(a)=E(b)"})

    # K1b -- F118 read literally per axis (its kappa_E, c, clock are E_g-channel
    # self-interactions, F118 section 4): its own couplings then favour (a)
    pa = f118_per_axis_fork()
    rec("K1b_f118_per_axis_reading_favours_a",
        pa["dE_all_per_axis"] > 0 and pa["dE_sea_spectral_landau_per_axis"] > 0 and pa["alpha_eq_beta_from_kE"] > 0,
        {**pa, "reading": "diagonal-entry extension: E(b) - E(a) > 0 and alpha = beta = -kappa_E > 0 (stiff quadrant)"})

    # K2 -- the derived Dirac sea is generation-covariant (machine precision)
    sa = sea_energy(Ya, sea_L, sea_generation_blind)
    others = {k: sea_energy(v, sea_L, sea_generation_blind) for k, v in Yk.items()}
    for i, Yr_ in enumerate(orbit_sample(2)):
        others[f"random_U{i}"] = sea_energy(Yr_, sea_L, sea_generation_blind)
    dmax = max(abs(v - sa) for v in others.values())
    om = _bz_omegas(sea_L)
    per_axis = 4 * sum(_f_of_m(float(y / lam.max()) ** 2, om) for y in lam)
    rec("K2_dirac_sea_generation_covariant", dmax < 1e-12 and abs(sa - per_axis) < 1e-12,
        {"sea_a": sa, "max_dev_over_orbit": dmax, "per_axis_F95_sum_x4": per_axis, "L": sea_L,
         "generation_blind": sea_generation_blind})

    # K3 -- three O_h-inequivalent circulant realisations; which lepton sits on (1,1,1)
    b_s = sp.simplify((F * sp.diag(*_lam_sym()) * F.H)[0, 1])
    ok3a = abs(complex(sp.N(b_s - SQRT2 / 2 * sp.exp(sp.I * DELTA), 40))) < 1e-35
    on111 = {k: LEPTON_OF_N[j % 3] for k, j in BRANCHES.items()}     # a + 2 Re b = lambda_j
    m111_ok = all(abs(float((Yk[k].sum() / 3).real) - lam[j % 3]) < 1e-13 for k, j in BRANCHES.items())
    t1g = {k: float(kernel_invariants(Yk[k])[1]) for k in BRANCHES}
    t1g_exact = {k: float(sp.N(sp.Rational(3, 2) * sp.sin(DELTA + j * 2 * sp.pi / 3) ** 2, 20))
                 for k, j in BRANCHES.items()}
    spec_ok = all(float(xp.abs(xp.sort(xp.linalg.eigvalsh(Yk[k])) - xp.sort(lam)).max()) < 1e-14 for k in Yk)
    ok3 = ok3a and m111_ok and spec_ok and on111 == {"b1": "tau", "b2": "e", "b3": "mu"} \
        and all(abs(t1g[k] - t1g_exact[k]) < 1e-13 for k in t1g) and len({round(v, 10) for v in t1g.values()}) == 3
    rec("K3_three_inequivalent_circulant_branches", ok3,
        {"b_of_Fourier_rotation": "sqrt2/2 exp(i 2/9) (sympy, 40 digits)", "lepton_on_111": on111,
         "T1g_weight_I_(invariant_so_branches_inequivalent)": t1g_exact})

    # K4 -- TM1 needs the electron on (1,1,1): branch b2 only; b1 keeps only TM2
    data = dict(oh.NUFIT60_3SIG)
    if s12sq_band == "juno":
        data["s12sq"] = oh.NUFIT61_S12SQ_3SIG_APPROX
    viable, allcols = {}, {}
    for k, j in BRANCHES.items():
        _, cols = branch_columns(j)
        allcols[k] = cols
        viable[k] = [c for c in cols if _column_viable_fixed(c, data)]
    tm1 = (sp.Rational(2, 3), sp.Rational(1, 6), sp.Rational(1, 6))
    ok4 = viable["b2"] == [tm1] and viable["b1"] == [] and viable["b3"] == []
    rec("K4_TM1_only_on_b2_no_viable_residual_on_b1", ok4,
        {"band": s12sq_band,
         "viable_columns": {k: [tuple(str(x) for x in c) for c in v] for k, v in viable.items()},
         "all_columns": {k: [tuple(str(x) for x in c) for c in v] for k, v in allcols.items()}})

    # K5 -- the axial/polar angle along [111] per branch (exact)
    ang = {"b1": DELTA, "b2": sp.pi / 3 - DELTA, "b3": sp.pi / 3 + DELTA}
    ok5 = all(abs(float(sp.N(sp.Abs(sp.tan(DELTA + j * 2 * sp.pi / 3)) - sp.tan(ang[k]), 40))) < 1e-35
              for k, j in BRANCHES.items())
    rec("K5_axial_polar_angle_per_branch", ok5,
        {"arctan_T1g_over_T2g": {k: str(v) for k, v in ang.items()},
         "reading": "tan(delta*) = T1g/T2g holds on b1 only; the TM1 vacuum b2 has pi/3 - 2/9"})

    # K6 -- Michel: stabilisers and finite fixed sets => both orbits critical for any invariant
    perms = _signed_perms_num()
    stab_a = sum(1 for R in perms if xp.allclose(R @ Ya @ R.T, Ya))
    stab_b = sum(1 for R in perms if xp.allclose(R @ Yb @ R.T, Yb) or xp.allclose(R @ Yb.conj() @ R.T, Yb))
    kap = rng.normal(size=6)
    gens = []
    for i, j_ in [(0, 0), (1, 1), (2, 2)]:
        H = xp.zeros((3, 3), dtype=complex); H[i, i] = 1; gens.append(H)
    for i, j_ in [(0, 1), (1, 2), (0, 2)]:
        H = xp.zeros((3, 3), dtype=complex); H[i, j_] = H[j_, i] = 1; gens.append(H)
        H = xp.zeros((3, 3), dtype=complex); H[i, j_] = 1j; H[j_, i] = -1j; gens.append(H)

    def grad_norm(Y0, h=1e-5):
        g = []
        for H in gens:
            Up = _mfun(h * H, lambda x: xp.exp(1j * x))
            ep = float(kernel_invariants(Up @ Y0 @ Up.conj().T) @ kap)
            em = float(kernel_invariants(Up.conj().T @ Y0 @ Up) @ kap)
            g.append((ep - em) / (2 * h))
        return max(abs(x) for x in g)
    grads = {"a": grad_norm(Ya), **{k: grad_norm(v) for k, v in Yk.items()}}
    generic = grad_norm(orbit_sample(1)[0])
    rec("K6_michel_both_orbits_critical", stab_a == 8 and stab_b == 12 and max(grads.values()) < 1e-8 < generic,
        {"stabiliser_a_signed_perms": stab_a, "stabiliser_b1_incl_antiunitary": stab_b,
         "max_orbit_gradient_random_invariant": grads, "generic_point_gradient": generic})

    # K7 -- kernel dimensions (Molien, exact) and the explicit basis
    n_inv, ker = molien_counts(3)
    inv_ok = max(float(xp.abs(kernel_invariants(R @ Yb @ R.T) - kernel_invariants(Yb)).max()) for R in perms) < 1e-13 \
        and float(xp.abs(kernel_invariants(Yb.conj()) - kernel_invariants(Yb)).max()) < 1e-13
    Ms = orbit_sample(200)
    Mrank = int(xp.linalg.matrix_rank(xp.column_stack([xp.ones(200), kernel_invariants(Ms)]), 1e-9))
    ok7 = n_inv == {1: 1, 2: 4, 3: 9} and ker == {1: 0, 2: 2, 3: 6} \
        and float(xp.abs(kernel_invariants(Ya)).max()) == 0.0 and inv_ok and Mrank == 7
    rec("K7_crystal_field_kernel_dimensions", ok7,
        {"n_invariants": n_inv, "kernel_dim": ker, "basis_rank_on_orbit_incl_const": Mrank})

    # K8 -- quadratic phase diagram: exact bounds, sampled confirmation, b1/b2 never strict
    RI = kernel_invariants(orbit_sample(n_samples))[:, :2]
    D = float(((lam - lam.mean()) ** 2).sum()) / 2
    Imax = ((float(lam.max()) - float(lam.min())) / 2) ** 2
    Yr = _real_constant_diagonal()
    r_ok = float(xp.abs(xp.sort(xp.linalg.eigvalsh(Yr)) - xp.sort(lam)).max()) < 1e-12
    m0, y0 = (lam[0] + lam[1]) / 2, (lam[0] - lam[1]) / 2          # the tau-e block
    Yblock = xp.diag(lam).astype(complex)
    Yblock[0, 0] = Yblock[1, 1] = m0
    Yblock[0, 1], Yblock[1, 0] = -1j * y0, 1j * y0
    wit = {"a": Ya, "real_constant_diagonal": Yr, "b3_circulant": Yk["b3"], "T1g_block": Yblock}
    bound_ok = float(RI.sum(1).max()) <= D + 1e-12 and float(RI[:, 1].max()) <= Imax + 1e-12
    diag_ok, never_b12, rows = True, True, []
    for th in xp.linspace(0, 2 * math.pi, 24, endpoint=False):
        al, be = math.cos(th), math.sin(th)
        win, cands, _, _ = quadratic_phase(al, be, imax_scale=imax_scale)
        if win == "boundary":
            continue
        ab = xp.array([al, be])
        e_win = cands[win]
        e_wit = float(kernel_invariants(wit[win])[:2] @ ab)
        e_smp = float((RI @ ab).min())
        e_b = {k: float(kernel_invariants(Yk[k])[:2] @ ab) for k in ("b1", "b2")}
        diag_ok &= abs(e_wit - e_win) < 1e-12 and e_smp >= e_win - 1e-12
        never_b12 &= min(e_b.values()) > e_win + 1e-9
        rows.append((round(float(th), 3), win))
    s2 = {k: float(kernel_invariants(Yk[k])[1]) / D for k in BRANCHES}
    between = 0 < s2["b1"] < s2["b3"] and 0 < s2["b2"] < s2["b3"] and abs(s2["b3"] - Imax / D) < 1e-12
    rec("K8_quadratic_phase_diagram_b1_b2_never_ground",
        bound_ok and r_ok and diag_ok and never_b12 and between,
        {"D": D, "Imax": Imax, "T1g_fractions": s2, "winners_by_direction": rows,
         "rule": "a: alpha,beta>0 | real texture: alpha<min(0,beta) | b3: beta<alpha<0 | T1g block: beta<0<alpha"})

    # K9 -- cubic crystal field: b1/b2 become reachable, b2 is the rarest vacuum (indicative)
    Vs = kernel_invariants(orbit_sample(n_samples))
    special = {"a": Ya, **Yk}
    Vsp = {k: kernel_invariants(v) for k, v in special.items()}
    Vl = {k: kernel_invariants(orbit_sample(3000, v, 0.05)) for k, v in special.items()}
    cnt = {}
    for _ in range(n_couplings):
        kv = rng.normal(size=6)
        es = {k: float(v @ kv) for k, v in Vsp.items()}
        k = min(es, key=es.get)
        good = es[k] <= float((Vs @ kv).min()) + 1e-12 and float((Vl[k] @ kv).min()) >= es[k] - 1e-12
        lab = k if good else "other"
        cnt[lab] = cnt.get(lab, 0) + 1
    frac = {k: cnt.get(k, 0) / n_couplings for k in ("a", "b1", "b2", "b3", "other")}
    ok9 = frac["b2"] <= min(frac["b1"], frac["b3"], frac["a"]) and frac["b1"] < frac["a"]
    rec("K9_cubic_crystal_field_b2_rarest_vacuum", ok9,
        {"fractions_gaussian_prior": frac,
         "note": "indicative: isotropic Gaussian prior on the 6 kernel couplings; b1/b2 reachable only beyond quadratic order"})

    # V -- verdict
    core = ("K1_f118_spectral_reading_exact_tie", "K1b_f118_per_axis_reading_favours_a", "K2_dirac_sea_generation_covariant",
            "K3_three_inequivalent_circulant_branches", "K4_TM1_only_on_b2_no_viable_residual_on_b1",
            "K5_axial_polar_angle_per_branch", "K8_quadratic_phase_diagram_b1_b2_never_ground")
    verdict = "a" if all(checks[c]["pass"] for c in core) else "undecided"
    rec("V_verdict_picture_a", verdict == "a",
        {"verdict": verdict,
         "why": "summary of K1, K1b, K2-K5, K8 (not an independent leg): spectral reading ties; F118's per-axis "
                "reading puts the crystal field in the stiff quadrant, where (a) is the ground state; (b)'s "
                "delta*-reading (b1) and its TM1 (b2) are different vacua, neither a quadratic-order ground state"})

    return {"checks": checks, "pass": all(c["pass"] for c in checks.values()),
            "params": {"sea_L": sea_L, "sea_generation_blind": sea_generation_blind,
                       "s12sq_band": s12sq_band, "n_samples": n_samples,
                       "n_couplings": n_couplings, "seed": seed, "imax_scale": imax_scale}}
