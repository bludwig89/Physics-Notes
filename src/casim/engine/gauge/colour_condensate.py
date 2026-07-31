"""
ca_colour_condensate.py — the colour-magnetic condensate arising within the model (F88)
=======================================================================================

Created: 2026-06-04

Companion to `derive_colour_condensate.py` (the sympy-exact half).  F86 built
the binding force on a colour-magnetic condensate that was *assumed*; this
module demonstrates it *arising* from the model's own physics, two ways:

Route 1 — instability (the perturbative vacuum is forced to condense)
    Part A: uniform-flux compact links on the 2D torus (the model's own
            link-variable language; plaquette angle exactly uniform).
    Part B: lattice charged-vector spectrum in that background.  The spin-
            aligned tower Omega^2 = lambda_n - 2 sin(phi) has a NEGATIVE
            lowest eigenvalue -> in F26 language the (E,B) rotation rate is
            imaginary: the mode grows instead of rotating.  Continuum check:
            min Omega^2 / phi -> -1 (the Nielsen–Olesen tachyon).
    Part C: one-loop lattice vacuum energy (finite mode sum, lattice = UV
            regulator).  dE(B) = E(B) - E(0) < 0: switching on a chromo-
            magnetic background LOWERS the quantum vacuum energy (Savvidy).

Route 2 — mechanism (what condenses: monopoles from compactness)
    Part D: DeGrand–Toussaint monopole number on compact links — integer-
            quantised, gauge-invariant, total charge zero on the torus,
            exactly +-1 on a constructed Dirac-string pair.  Monopoles are
            unavoidable consequences of the model's compact U(x): no extra
            ingredient is added.
    Part E: exact duality identities that turn the monopole gas into the
            dual superconductor: the Villain/Poisson link identity and the
            Gaussian Coulomb-gas <-> sine-Gordon identity (machine-eps).
    Part F: 3D compact U(1) Metropolis — the monopole density rho(beta) > 0
            measured on equilibrated configurations; chain
              rho -> fugacity z -> Debye mass m_D = sqrt(2z/kappa),
              kappa = beta/(4 pi^2)  (Polyakov)
            and the F86 hand-off  v = m_D / e  (so m_V = e v = m_D), giving
            sigma_F86 = 2 pi v^2 n > 0 with v now MEASURED, not assumed.

Conventions
-----------
  phi          plaquette angle of the uniform-flux background, 2 pi q / L^2.
  lambda       eigenvalue of the gauge-covariant lattice Laplacian -D^2.
  Omega^2      lattice rotation-rate squared of a charged-gluon mode
               (F26 language): Omega^2 = lambda + s * 2 sin(phi), s = -+1.
  theta        compact U(1) link angles, shape (3, L, L, L) for 3D.
  rho          monopole density (monopole+antimonopole count / volume).
  z            fugacity, dilute-gas z = rho / 2.
  e^2 = 1/beta 3D lattice coupling; v = m_D / e is the F86 VEV.

References: Nielsen–Olesen 1978 (vacuum instability), Savvidy 1977,
DeGrand–Toussaint 1980 (lattice monopoles), Polyakov 1977 (compact U(1)_3
confinement).  Model: F26, F43, F70, F86.
"""

import numpy as np


# ══════════════════════════════════════════════════════════════════
#  Part A — uniform-flux compact links on the 2D torus
# ══════════════════════════════════════════════════════════════════

def flux_links_2d(L, q):
    """Compact U(1) links carrying exactly uniform plaquette angle
    phi = 2 pi q / L^2 on the L x L torus.

    Standard construction: U_y(n) = exp(i phi n_x) everywhere, and the
    boundary column of x-links U_x(n_x=L-1, n_y) = exp(-i phi L n_y) closes
    the torus so that EVERY plaquette (including the seam) has angle phi
    (mod 2pi).  Requires integer q (total flux quantisation 2 pi q)."""
    phi = 2.0 * np.pi * q / L**2
    nx = np.arange(L)[:, None] * np.ones(L)[None, :]
    ny = np.arange(L)[None, :] * np.ones(L)[:, None]
    Ux = np.ones((L, L), dtype=complex)
    Ux[L - 1, :] = np.exp(-1j * phi * L * ny[L - 1, :])
    Uy = np.exp(1j * phi * nx)
    return Ux, Uy, phi


def plaquette_angles_2d(Ux, Uy):
    """arg of U_x(n) U_y(n+x) U_x^*(n+y) U_y^*(n) for every site."""
    P = (Ux * np.roll(Uy, -1, axis=0) *
         np.conj(np.roll(Ux, -1, axis=1)) * np.conj(Uy))
    return np.angle(P)


# ══════════════════════════════════════════════════════════════════
#  Part B — lattice charged-vector spectrum: the tachyonic tower
# ══════════════════════════════════════════════════════════════════

def charged_laplacian_matrix(Ux, Uy):
    """Gauge-covariant lattice Laplacian -D^2 as a dense Hermitian matrix
    acting on a charged field on the L x L torus:

        (-D^2 psi)(n) = 4 psi(n) - U_x(n) psi(n+x) - U_x^*(n-x) psi(n-x)
                                 - U_y(n) psi(n+y) - U_y^*(n-y) psi(n-y)."""
    L = Ux.shape[0]
    N = L * L
    idx = np.arange(N).reshape(L, L)
    M = np.zeros((N, N), dtype=complex)
    M[np.arange(N), np.arange(N)] = 4.0
    for axis, U in ((0, Ux), (1, Uy)):
        nbr = np.roll(idx, -1, axis=axis)
        M[idx.ravel(), nbr.ravel()] -= U.ravel()
        M[nbr.ravel(), idx.ravel()] -= np.conj(U.ravel())
    return M


def charged_spectrum_2d(L, q):
    """Eigenvalues of -D^2 in the uniform-flux background."""
    Ux, Uy, phi = flux_links_2d(L, q)
    M = charged_laplacian_matrix(Ux, Uy)
    lam = np.linalg.eigvalsh(M)
    return lam, phi


def tachyon_certificate(L, q):
    """Spin-aligned charged-gluon tower: Omega^2 = lambda - 2 sin(phi).

    Returns (min Omega^2, ratio min Omega^2 / phi, phi).  The Nielsen–Olesen
    statement is min Omega^2 < 0 with ratio -> -1 as phi -> 0."""
    lam, phi = charged_spectrum_2d(L, q)
    omega2 = lam - 2.0 * np.sin(phi)
    return float(omega2.min()), float(omega2.min() / phi), phi


# ══════════════════════════════════════════════════════════════════
#  Part C — one-loop lattice vacuum energy (Savvidy, finite mode sum)
# ══════════════════════════════════════════════════════════════════

def one_loop_energy_2plus1(L, q, Lz=None):
    """One-loop vacuum energy per site of the charged vector pair on an
    L x L x Lz lattice with uniform flux phi in the xy plane.

    Mode frequencies: omega^2 = lambda_i + 2 - 2 cos(k_z) + s 2 sin(phi),
    s = +-1 (the two transverse spin states).  E = (1/2) sum Re omega.
    Tachyonic omega^2 < 0 contribute Re omega = 0 (their imaginary part is
    the decay rate — derive_colour_condensate.py D2).  The lattice is the
    UV regulator: the sum is finite, no renormalisation needed for the
    DIFFERENCE dE(B) = E(B) - E(0)."""
    if Lz is None:
        Lz = L
    lam, phi = charged_spectrum_2d(L, q)
    kz = 2.0 * np.pi * np.arange(Lz) / Lz
    ez = 2.0 - 2.0 * np.cos(kz)
    base = lam[:, None] + ez[None, :]
    E = 0.0
    for s in (+1.0, -1.0):
        w2 = base + s * 2.0 * np.sin(phi)
        w2 = np.where(w2 > 0.0, w2, 0.0)      # Re omega of tachyons = 0
        E += 0.5 * np.sqrt(w2).sum()
    return E / (L * L * Lz), phi


def savvidy_scan(L, qs, Lz=None):
    """dE(B) = E(B) - E(0) per site for a list of flux quanta.  Savvidy:
    dE < 0 (quantum energy is lowered by the background), increasingly so
    per unit B^2 as B decreases (the +B^2 ln B structure)."""
    E0, _ = one_loop_energy_2plus1(L, 0, Lz)
    out = []
    for q in qs:
        Eq, phi = one_loop_energy_2plus1(L, q, Lz)
        out.append((q, phi, Eq - E0))
    return out


# ══════════════════════════════════════════════════════════════════
#  Part D — DeGrand–Toussaint monopoles from compact links
# ══════════════════════════════════════════════════════════════════

def _plaq_angle_3d(theta, mu, nu):
    """Plaquette angle theta_P in the (mu,nu) plane, shape (L,L,L)."""
    return (theta[mu] + np.roll(theta[nu], -1, axis=mu)
            - np.roll(theta[mu], -1, axis=nu) - theta[nu])


def _principal(a):
    """Reduce angle to the principal branch (-pi, pi]."""
    return a - 2.0 * np.pi * np.floor((a + np.pi) / (2.0 * np.pi))


def dgt_monopole_field(theta):
    """DeGrand–Toussaint monopole number per elementary cube.

    theta: link angles, shape (3, L, L, L).  The physical (principal-branch)
    plaquette angle is theta_P_bar = theta_P - 2 pi n_P with integer n_P
    (the Dirac-string number).  The monopole charge in the cube at n is

        m(n) = -(1/2pi) sum_{P in boundary of cube} theta_P_bar
             =  sum of the six n_P with orientation  — an integer.

    Implemented as the lattice divergence of n_P over the cube faces."""
    planes = {(0, 1): None, (0, 2): None, (1, 2): None}
    nP = {}
    for (mu, nu) in planes:
        tp = _plaq_angle_3d(theta, mu, nu)
        nP[(mu, nu)] = np.rint((tp - _principal(tp)) / (2.0 * np.pi))
    # cube at n has faces: (nu,rho) planes at n and n+mu_hat for the three
    # plane choices; the oriented sum is the discrete divergence of the dual
    # field  m = d n  (DeGrand–Toussaint Eq. 6 equivalent):
    m = np.zeros_like(nP[(0, 1)])
    for (mu, nu), comp in (((1, 2), 0), ((0, 2), 1), ((0, 1), 2)):
        sgn = -1.0 if comp == 1 else 1.0   # orientation of the (mu,nu) face
        f = nP[(mu, nu)]
        m += sgn * (np.roll(f, -1, axis=comp) - f)
    return m


def gauge_transform_3d(theta, alpha):
    """theta_mu(n) -> theta_mu(n) + alpha(n) - alpha(n+mu)  (compact)."""
    out = np.empty_like(theta)
    for mu in range(3):
        out[mu] = theta[mu] + alpha - np.roll(alpha, -1, axis=mu)
    return out


def dirac_pair_config(L, sep=None):
    """Construct a monopole–antimonopole pair from the continuum Dirac
    potential.  A_mono (string along -z, total flux 2pi = one DGT unit):

        A = (1 - z/r) / (2 rho^2) * (-y, x, 0),   rho^2 = x^2 + y^2.

    Pair field A(r) = A_mono(r - r_plus) - A_mono(r - r_minus) with
    r_plus = r_minus + sep * z_hat: the semi-infinite strings cancel below
    r_minus, leaving one Dirac string on the segment — invisible mod 2pi.
    Link angles by the midpoint rule theta_mu(n) = A_mu(n + mu_hat/2); the
    DGT charge is topological, so the discretisation cannot shift it off
    +-1.  Returns (theta, r_plus, r_minus)."""
    if sep is None:
        sep = 2 * (L // 6)
    # monopoles live at CUBE CENTRES (half-integer coordinates) so the
    # Dirac string pierces plaquettes through their centres
    c = L // 2 + 0.5
    r_minus = np.array([c, c, L // 2 - sep / 2.0 + 0.5])
    r_plus = r_minus + np.array([0.0, 0.0, float(sep)])

    def A_mono(px, py, pz):
        r = np.sqrt(px**2 + py**2 + pz**2)
        rho2 = px**2 + py**2
        fac = (1.0 - pz / r) / (2.0 * rho2)
        return -py * fac, px * fac

    theta = np.zeros((3, L, L, L))
    n = np.arange(L)
    X, Y, Z = np.meshgrid(n, n, n, indexing='ij')
    for mu, (dx, dy, dz) in enumerate(((0.5, 0., 0.), (0., 0.5, 0.),
                                       (0., 0., 0.5))):
        mx, my, mz = X + dx, Y + dy, Z + dz
        if mu == 2:
            continue                      # A_z = 0 for this gauge
        tot = np.zeros((L, L, L))
        for centre, sgn in ((r_plus, +1.0), (r_minus, -1.0)):
            ax, ay = A_mono(mx - centre[0], my - centre[1], mz - centre[2])
            tot += sgn * (ax if mu == 0 else ay)
        theta[mu] = tot
    return theta, r_plus, r_minus


def random_compact_links_3d(L, scale=np.pi, seed=0):
    rng = np.random.default_rng(seed)
    return rng.uniform(-scale, scale, size=(3, L, L, L))


def su3_diag_phases(U):
    """Naive Abelian projection of SU(3) link fields: the two independent
    Cartan angles from the diagonal phases, theta_i = arg(U_ii), i = 1,2.
    U: (..., 3, 3) complex.  Returns (theta1, theta2) with shape (...)."""
    t1 = np.angle(U[..., 0, 0])
    t2 = np.angle(U[..., 1, 1])
    return t1, t2


def haar_su3(shape, seed=0):
    """Haar-random SU(3) field of given leading shape (QR of Ginibre,
    determinant-normalised)."""
    rng = np.random.default_rng(seed)
    A = (rng.standard_normal(shape + (3, 3)) +
         1j * rng.standard_normal(shape + (3, 3))) / np.sqrt(2.0)
    Q, R = np.linalg.qr(A)
    d = np.einsum('...ii->...i', R)
    Q = Q * (d / np.abs(d))[..., None, :]
    det = np.linalg.det(Q)
    Q = Q / det[..., None, None] ** (1.0 / 3.0)
    return Q


# ══════════════════════════════════════════════════════════════════
#  Part E — exact duality identities (Villain / Coulomb gas / sine-Gordon)
# ══════════════════════════════════════════════════════════════════

def villain_poisson_residual(beta, thetas, n_max=40):
    """Poisson resummation that opens the duality chain:

        sum_n exp(-beta/2 (theta - 2 pi n)^2)
            = 1/sqrt(2 pi beta) sum_m exp(-m^2/(2 beta)) e^{i m theta}.

    Returns max |LHS - RHS| over the supplied theta values."""
    thetas = np.asarray(thetas, dtype=float)
    ns = np.arange(-n_max, n_max + 1)
    lhs = np.exp(-0.5 * beta * (thetas[:, None] - 2 * np.pi * ns[None, :])**2).sum(axis=1)
    ms = np.arange(-n_max, n_max + 1)
    rhs = (np.exp(-ms[None, :]**2 / (2.0 * beta)) *
           np.exp(1j * ms[None, :] * thetas[:, None])).sum(axis=1) / np.sqrt(2 * np.pi * beta)
    return float(np.abs(lhs - rhs.real).max() + np.abs(rhs.imag).max())


def coulomb_gas_gaussian_residual(n_sites=3, kappa=1.3, mass2=0.7,
                                  charges=(1, -1, 0), n_quad=80):
    """The Coulomb-gas <-> sine-Gordon engine is the Gaussian identity

        < exp(i sum_j q_j chi_j) >_Gaussian = exp(-1/2 q^T G q),

    G = (kappa(-Delta) + mass2)^{-1} on a small periodic chain.  LHS by
    dense Gauss–Hermite quadrature (machine-converged), RHS by linear
    algebra.  Returns |LHS - RHS|."""
    # precision matrix
    K = np.zeros((n_sites, n_sites))
    for i in range(n_sites):
        K[i, i] = 2.0 * kappa + mass2
        K[i, (i + 1) % n_sites] -= kappa
        K[i, (i - 1) % n_sites] -= kappa
    G = np.linalg.inv(K)
    q = np.asarray(charges, dtype=float)
    rhs = np.exp(-0.5 * q @ G @ q)

    # LHS: rotate to principal axes, Gauss–Hermite per axis
    w, V = np.linalg.eigh(K)            # K = V diag(w) V^T
    # chi = V y, y_k Gaussian with variance 1/w_k
    # <e^{i q.chi}> = prod_k <e^{i (V^T q)_k y_k}> = prod_k e^{-(V^T q)_k^2/(2 w_k)}
    # quadrature check of each 1D factor:
    a = V.T @ q
    nodes, wts = np.polynomial.hermite_gauss.hermgauss(n_quad) \
        if hasattr(np.polynomial, 'hermite_gauss') else np.polynomial.hermite.hermgauss(n_quad)
    lhs = 1.0
    for k in range(n_sites):
        yk = nodes * np.sqrt(2.0 / w[k])
        fk = (wts * np.exp(1j * a[k] * yk)).sum() / np.sqrt(np.pi)
        lhs *= fk
    return float(abs(lhs - rhs))


def debye_mass(beta, rho):
    """Polyakov chain: dual stiffness kappa = beta/(4 pi^2), fugacity
    z = rho/2 (dilute gas), m_D = sqrt(2 z / kappa) = 2 pi sqrt(rho/beta)."""
    kappa = beta / (4.0 * np.pi**2)
    zfug = rho / 2.0
    return float(np.sqrt(2.0 * zfug / kappa))


def f86_vev_from_density(beta, rho):
    """Hand-off to F86: m_V = e v = m_D with e^2 = 1/beta (3D lattice units)
    => v = m_D sqrt(beta).  Returns (v, sigma_F86 = 2 pi v^2)."""
    mD = debye_mass(beta, rho)
    v = mD * np.sqrt(beta)
    return float(v), float(2.0 * np.pi * v**2), mD


# ══════════════════════════════════════════════════════════════════
#  Part F — 3D compact U(1) Monte-Carlo (monopole density measurement)
# ══════════════════════════════════════════════════════════════════

def _staple_sum_3d(theta, mu):
    """Sum of the 4 staple angles' cos/sin contribution for links in
    direction mu: returns (Sx, Sy) with the local action
    S(theta_mu) = -beta * [cos(theta_mu)*Sx + sin(theta_mu)*Sy] up to const,
    where Sx + i Sy = sum of e^{-i (staple angle)}."""
    L = theta.shape[1]
    Sre = np.zeros((L, L, L))
    Sim = np.zeros((L, L, L))
    for nu in range(3):
        if nu == mu:
            continue
        # forward staple: theta_nu(n+mu) - theta_mu(n+nu) - theta_nu(n)
        f = (np.roll(theta[nu], -1, axis=mu)
             - np.roll(theta[mu], -1, axis=nu) - theta[nu])
        # backward staple: -theta_nu(n+mu-nu) - theta_mu(n-nu) + theta_nu(n-nu)
        b = (-np.roll(np.roll(theta[nu], -1, axis=mu), 1, axis=nu)
             - np.roll(theta[mu], 1, axis=nu) + np.roll(theta[nu], 1, axis=nu))
        Sre += np.cos(f) + np.cos(b)
        Sim += -np.sin(f) - np.sin(b)
    return Sre, Sim


def u1_metropolis_3d(L=8, beta=1.0, n_sweeps=300, step=1.0, seed=1,
                     n_meas=10):
    """Vectorised checkerboard Metropolis for 3D compact U(1) with Wilson
    action S = -beta sum_P cos(theta_P).  Returns (theta, rho_history) with
    rho measured every n_sweeps//n_meas sweeps in the second half."""
    rng = np.random.default_rng(seed)
    theta = rng.uniform(-np.pi, np.pi, size=(3, L, L, L))
    xs = np.arange(L)
    parity = (xs[:, None, None] + xs[None, :, None] + xs[None, None, :]) % 2
    masks = [parity == 0, parity == 1]
    rho_hist = []
    meas_every = max(1, n_sweeps // (2 * n_meas))
    for sweep in range(n_sweeps):
        for mu in range(3):
            Sre, Sim = _staple_sum_3d(theta, mu)
            for mk in masks:
                prop = theta[mu] + rng.uniform(-step, step, size=(L, L, L))
                dS = -beta * ((np.cos(prop) - np.cos(theta[mu])) * Sre
                              + (np.sin(prop) - np.sin(theta[mu])) * Sim)
                acc = (rng.uniform(size=(L, L, L)) < np.exp(-np.clip(dS, -50, 50))) & mk
                theta[mu] = np.where(acc, _principal(prop), theta[mu])
        if sweep >= n_sweeps // 2 and (sweep % meas_every == 0):
            m = dgt_monopole_field(theta)
            rho_hist.append(float(np.abs(m).sum() / L**3))
    return theta, rho_hist


def monopole_density_vs_beta(L=8, betas=(0.6, 1.0, 1.4, 1.8, 2.2),
                             n_sweeps=300, seed=3):
    """rho(beta) on equilibrated 3D compact U(1) configurations."""
    out = []
    for i, b in enumerate(betas):
        _, hist = u1_metropolis_3d(L=L, beta=b, n_sweeps=n_sweeps,
                                   seed=seed + i)
        out.append((float(b), float(np.mean(hist))))
    return out
