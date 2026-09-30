"""
Single-action lattice QED prototype -- the alternative derivation path.

Companion to docs/audits/2026-09-16-photon-fermion-momentum-investigation.md section 7.
Self-contained (numpy only).  Builds a 2+1D lattice QED toy from ONE Hamiltonian on a
discrete-exterior-calculus complex, and compares it head to head with a "bridged" scheme
of the same shape as the casim F387/F388 recipe.

READ SECTION 7 OF THE AUDIT BEFORE QUOTING ANY NUMBER FROM THE COUPLED-MOMENTUM
SECTIONS (CONFIG A / CONFIG B).  The structural checks T1-T4 are sound; the coupled
momentum results are explicitly NOT established, and CONFIG B is degenerate.

    python3 verify_single_action_prototype.py
"""

import numpy as np

KAPPA = 1.0


# ---------------------------------------------------------------- DEC
def d0(phi):
    return np.stack([np.roll(phi, -1, 0) - phi, np.roll(phi, -1, 1) - phi])


def d1(A):
    return A[0] + np.roll(A[1], -1, 0) - np.roll(A[0], -1, 1) - A[1]


def d1_star(B):
    """The Ampere partner of d1: <d1 A, B> = <A, d1_star B> (exact adjoint)."""
    return np.stack([B - np.roll(B, 1, 1), np.roll(B, 1, 0) - B])


def div(V):
    """-d0^dagger : the divergence whose composition with d1_star vanishes."""
    return (V[0] - np.roll(V[0], 1, 0)) + (V[1] - np.roll(V[1], 1, 1))


# ------------------------------------------------- the single Hamiltonian
def hop(psi, A, q):
    """dH_matter/dpsi*   (the covariant hopping operator, Hermitian)."""
    px, py = np.exp(1j * q * A[0]), np.exp(1j * q * A[1])
    return -KAPPA * (np.roll(px, 1, 0) * np.roll(psi, 1, 0)
                     + np.conj(px) * np.roll(psi, -1, 0)
                     + np.roll(py, 1, 1) * np.roll(psi, 1, 1)
                     + np.conj(py) * np.roll(psi, -1, 1))


def current(psi, A, q):
    """J_i(x) = dH_matter/dA_i(x) = 2 kappa q Im[psi*(x+e_i) e^{iqA_i(x)} psi(x)].
    DERIVED from the action.  Not chosen, not split, no free transverse sector."""
    px, py = np.exp(1j * q * A[0]), np.exp(1j * q * A[1])
    return 2.0 * KAPPA * q * np.stack([
        np.imag(np.conj(np.roll(psi, -1, 0)) * px * psi),
        np.imag(np.conj(np.roll(psi, -1, 1)) * py * psi)])


def energy(psi, A, E, q):
    return (np.real(np.sum(np.conj(psi) * hop(psi, A, q)))
            + 0.5 * np.sum(E ** 2) + 0.5 * np.sum(d1(A) ** 2))


def gauss(psi, A, E, q):
    return div(E) + q * np.abs(psi) ** 2


# ------------------------------------------------------------ observables
def p_matter(psi):
    L = psi.shape[0]
    k = np.fft.fftfreq(L) * 2 * np.pi
    KX, KY = np.meshgrid(k, k, indexing='ij')
    w = np.abs(np.fft.fft2(psi)) ** 2
    return np.array([(KX * w).sum(), (KY * w).sum()]) / w.sum()


def p_field(E, B):
    """sum_x E x B  with B along z, Yee-interpolated onto sites."""
    Bs = 0.25 * (B + np.roll(B, 1, 0) + np.roll(B, 1, 1) + np.roll(np.roll(B, 1, 0), 1, 1))
    Ex = 0.5 * (E[0] + np.roll(E[0], 1, 0))
    Ey = 0.5 * (E[1] + np.roll(E[1], 1, 1))
    return np.array([np.sum(Ey * Bs), -np.sum(Ex * Bs)])


# -------------------------------------------- exact free (E,B) rotation
_cache = {}


def _sym(L):
    if L not in _cache:
        k = np.fft.fftfreq(L) * 2 * np.pi
        KX, KY = np.meshgrid(k, k, indexing='ij')
        gx, gy = np.exp(1j * KX) - 1.0, np.exp(1j * KY) - 1.0
        _cache[L] = (gx, gy, np.sqrt(np.abs(gx) ** 2 + np.abs(gy) ** 2))
    return _cache[L]


def free_rotate_EB(E, B, dt):
    """Exact per-mode rotation of  Edot = d1_star B ,  Bdot = -d1 E .

    Symbols (measured against the real-space operators, not assumed):
        (d1 E)~      = -gy Ex~ + gx Ey~
        (d1_star B)~ = ( -conj(gy) B~ , +conj(gx) B~ )
    so M = [[0, d1_star],[-d1, 0]] has M^2 = -omega^2 on the transverse sector
    and M = 0 on the longitudinal sector of E.  The longitudinal sector is
    therefore EXACTLY invariant under free evolution, which is what makes the
    lattice Gauss law exactly static with no source.
    """
    L = E.shape[1]
    gx, gy, om = _sym(L)
    Ek = np.stack([np.fft.fft2(E[0]), np.fft.fft2(E[1])])
    Bk = np.fft.fft2(B)
    g2 = np.abs(gx) ** 2 + np.abs(gy) ** 2
    nz = g2 > 1e-14
    c = np.cos(om * dt)
    s = np.zeros_like(om)
    s[nz] = np.sin(om[nz] * dt) / om[nz]
    # longitudinal / transverse split of E (longitudinal = image of d0, i.e. (gx,gy))
    gdE = np.conj(gx) * Ek[0] + np.conj(gy) * Ek[1]
    EL = [np.zeros_like(Ek[0]), np.zeros_like(Ek[1])]
    for a, g in enumerate((gx, gy)):
        EL[a][nz] = g[nz] * gdE[nz] / g2[nz]
    ET = [Ek[a] - EL[a] for a in range(2)]
    dE = np.stack([-np.conj(gy) * Bk, np.conj(gx) * Bk])      # d1_star B (transverse)
    dB = -(-gy * Ek[0] + gx * Ek[1])                           # -d1 E
    En = np.stack([EL[a] + c * ET[a] + s * dE[a] for a in range(2)])
    Bn = c * Bk + s * dB
    return (np.stack([np.fft.ifft2(En[0]).real, np.fft.ifft2(En[1]).real]),
            np.fft.ifft2(Bn).real)


def split_TL(V):
    L = V.shape[1]
    gx, gy, _ = _sym(L)
    g2 = np.abs(gx) ** 2 + np.abs(gy) ** 2
    nz = g2 > 1e-14
    Vk = [np.fft.fft2(V[0]), np.fft.fft2(V[1])]
    gdV = np.conj(gx) * Vk[0] + np.conj(gy) * Vk[1]
    VT = []
    for a, g in enumerate((gx, gy)):
        p = np.zeros_like(Vk[a])
        p[nz] = g[nz] * gdV[nz] / g2[nz]
        VT.append(Vk[a] - p)
    return np.stack([np.fft.ifft2(v).real for v in VT])


def _expm_hop(psi, A, q, dt, n_sub=6):
    sub = dt / n_sub
    for _ in range(n_sub):
        k1 = hop(psi, A, q); k2 = hop(k1, A, q)
        k3 = hop(k2, A, q); k4 = hop(k3, A, q)
        psi = (psi - 1j * sub * k1 - 0.5 * sub ** 2 * k2
               + 1j * sub ** 3 / 6.0 * k3 + sub ** 4 / 24.0 * k4)
    return psi


def _A_from_B(B):
    """Coulomb-gauge A with d1 A = B  (the analogue of solve_A_coulomb)."""
    L = B.shape[0]
    gx, gy, om = _sym(L)
    g2 = np.abs(gx) ** 2 + np.abs(gy) ** 2
    nz = g2 > 1e-14
    Bk = np.fft.fft2(B)
    Ax = np.zeros_like(Bk); Ay = np.zeros_like(Bk)
    Ax[nz] = -np.conj(gy)[nz] * Bk[nz] / g2[nz]
    Ay[nz] = np.conj(gx)[nz] * Bk[nz] / g2[nz]
    return np.stack([np.fft.ifft2(Ax).real, np.fft.ifft2(Ay).real])


# ============================================================ THE SCHEMES
def step_single_action(psi, A, E, B, q, dt):
    """Symmetric (Strang) splitting of the ONE Hamiltonian.  The field is
    sourced by the FULL derived current; the ordering is symmetric, which is
    what makes the scheme variational/symplectic."""
    E = E - 0.5 * dt * current(psi, A, q)
    E, B = free_rotate_EB(E, B, dt)
    A = _A_from_B(B)
    psi = _expm_hop(psi, A, q, dt)
    E = E - 0.5 * dt * current(psi, A, q)
    return psi, A, E, B


def step_bridged(psi, A, E, B, q, dt, g_lat=1.0):
    """The casim F387/F388 recipe's shape: free-rotate, then source the field
    from the TRANSVERSE PART only, then step matter on the published A.
    Asymmetric ordering, partial current."""
    E, B = free_rotate_EB(E, B, dt)
    E = E - dt * g_lat * split_TL(current(psi, A, q))
    A = _A_from_B(B)
    psi = _expm_hop(psi, A, q, dt)
    return psi, A, E, B


# ============================================================ INITIAL STATE
def init_state(L, amp, m_index=2, sigma=4.0, beam_axis=0, matter_sigma=2.0):
    X, Y = np.meshgrid(np.arange(L, dtype=float), np.arange(L, dtype=float), indexing='ij')
    cm = [L / 2, L / 2]
    dxm = np.remainder(X - cm[0] + L / 2, L) - L / 2
    dym = np.remainder(Y - cm[1] + L / 2, L) - L / 2
    psi = np.exp(-(dxm ** 2 + dym ** 2) / (2 * matter_sigma ** 2)).astype(complex)
    psi /= np.linalg.norm(psi)

    # A transverse (E,B) pulse that is an exact superposition of free eigenmodes
    # travelling along beam_axis: build it in k-space one-sided in the carrier.
    k0 = 2 * np.pi * m_index / L
    cb = [L / 4 if a == beam_axis else L / 2 for a in range(2)]
    d = [np.remainder((X if a == 0 else Y) - cb[a] + L / 2, L) - L / 2 for a in range(2)]
    env = np.exp(-(d[0] ** 2 + d[1] ** 2) / (2 * sigma ** 2))
    pol = 1 - beam_axis
    E = np.zeros((2, L, L))
    E[pol] = amp * env * np.cos(k0 * d[beam_axis])
    E = split_TL(E)                      # exactly transverse
    # B is the quadrature partner that makes the pulse one-sided (travelling)
    # B IN PHASE with E -- the travelling-wave relation B = (k/omega) E, which is
    # what makes E x B nonzero.  (A quadrature B gives a STANDING wave with
    # sum E x B == 0; this is the 2D analogue of the E-parallel-B defect that makes
    # casim's build_beam_packet carry exactly zero Poynting momentum.)
    om_axis = 2.0 * abs(np.sin(k0 / 2))
    B = (k0 / max(om_axis, 1e-12)) * E[pol] * (1 if beam_axis == 0 else -1)
    B = B - B.mean()
    return psi, _A_from_B(B), E, B


L, DT, NT = 32, 0.05, 300
import numpy as _np; _np.random.seed(0)
BAR = "=" * 98


def run(st, q, amp, nt=NT, dt=DT, L=L):
    psi, A, E, B = init_state(L, amp=amp)
    m0, f0 = p_matter(psi), p_field(E, B)
    G0, H0 = gauss(psi, A, E, q), energy(psi, A, E, q)
    Gm = Hm = 0.0
    for _ in range(nt):
        psi, A, E, B = st(psi, A, E, B, q, dt)
        Gm = max(Gm, np.abs(gauss(psi, A, E, q) - G0).max())
        Hm = max(Hm, abs(energy(psi, A, E, q) - H0))
    return dict(dm=p_matter(psi) - m0, df=p_field(E, B) - f0,
                G=Gm, H=Hm / abs(H0), n=abs(np.linalg.norm(psi) - 1.0))


SCHEMES = (("single action (S)", step_single_action),
           ("bridged/split (C)", step_bridged))

print(BAR)
print("T1  DEC exterior-derivative identities -- the two a curl must satisfy")
print(BAR)
phi = np.random.randn(L, L); Av = np.random.randn(2, L, L); Bv = np.random.randn(L, L)
print("  curl(grad phi) = d1(d0 phi)      max|.| = %.3e   (must be 0)" % np.abs(d1(d0(phi))).max())
print("  div(curl* B)   = div(d1_star B)  max|.| = %.3e   (must be 0)" % np.abs(div(d1_star(Bv))).max())
print("  casim bcc_curl_symbol, same first test:  |C x grad|/(|C||grad|)  max 1.000000, mean 0.742")

print()
print(BAR)
print("T2  The current IS dH/dA.  Continuity as a consequence, not an imposed equation")
print(BAR)
q = 0.7
psi, A, E, B = init_state(L, amp=0.15)
rhodot = 2.0 * np.imag(np.conj(psi) * hop(psi, A, q))
J = current(psi, A, q)
print("  || q drho/dt - div J ||inf / || q drho/dt ||inf = %.3e" % (
    np.abs(q * rhodot - div(J)).max() / np.abs(q * rhodot).max()))
print("  transverse fraction ||J_T||/||J|| of the DERIVED current = %.6f" % (
    np.linalg.norm(split_TL(J)) / np.linalg.norm(J)))
print("  casim F388, same quantity for its constructed current:  2.1e-16 to 2.4e-16")

print()
print(BAR)
print("T3  Free-field control: is sum_x E x B conserved by the free propagator?")
print(BAR)
psi, A, E, B = init_state(L, amp=0.15)
p0 = p_field(E, B); Ex, Bx = E.copy(), B.copy()
for _ in range(400):
    Ex, Bx = free_rotate_EB(Ex, Bx, DT)
print("  |P_field| t=0 %.6f -> t=400 %.6f   rel drift %.3e   direction %s" % (
    np.linalg.norm(p0), np.linalg.norm(p_field(Ex, Bx)),
    np.linalg.norm(p_field(Ex, Bx) - p0) / np.linalg.norm(p0), np.round(p0 / np.linalg.norm(p0), 4)))

print()
print(BAR)
print("T4  Constraints over %d ticks, dt=%.2f, q=%.2f, seeded beam" % (NT, DT, q))
print(BAR)
for nm, st in SCHEMES:
    r = run(st, q, 0.15)
    print("  %s   Gauss drift %.3e   |dH|/|H| %.3e   norm drift %.3e" % (nm, r['G'], r['H'], r['n']))
print("  (Gauss drift is the physical discriminator: the FULL derived current updates the")
print("   longitudinal sector of E, which is exactly what keeps div E - q rho static.")
print("   Sourcing only the transverse part cannot.)")

print()
print(BAR)
print("CONFIG A -- seeded beam + matter at rest (F390's setup).  Is momentum EXCHANGED?")
print("*** NOT ESTABLISHED -- see audit section 7.  This H omits the scalar-potential term,")
print("*** so the longitudinal sector of E is not closed and no conservation argument applies.")
print(BAR)
for nm, st in SCHEMES:
    print()
    print("  %s" % nm)
    print("     q      ||dP_matter||   ||dP_field||    cos(dPm,dPf)   |dPm+dPf|/|dPm|")
    for qq in (0.1, 0.2, 0.4, 0.8):
        r = run(st, qq, 0.15)
        dm, df = r['dm'], r['df']
        nm_, nf_ = np.linalg.norm(dm), np.linalg.norm(df)
        cs = float(dm @ df / (nm_ * nf_)) if nm_ * nf_ > 1e-300 else float('nan')
        print("   %5.2f   %.6e   %.6e   %+.6f      %.6e" % (
            qq, nm_, nf_, cs, np.linalg.norm(dm + df) / max(nm_, 1e-300)))
print()
print("  (cos = -1 and ratio -> 0 is a genuine exchange: what matter gains, the field loses.")
print("   F390 measured cos = -0.989 on-axis but +0.99995 for an off-axis beam, and a")
print("   residual |dPm+dPf|/|dPm| = 0.174 that never closes.)")

print()
print(BAR)
print("CONFIG B -- self-sourced, NO seeded beam (F389's setup).  Coupling-order scaling.")
print("*** DEGENERATE -- a real Gaussian psi at rest with A=0 has J identically 0, so nothing")
print("*** is sourced and both columns are 1e-16 noise.  Needs a complex initial packet.")
print("            F389 measured ||dP_matter|| ~ O(g) and ||dP_field|| ~ O(g^2):")
print("            doubling ratios 1.99-2.00 and 3.99-4.01 -- the ORDER MISMATCH.")
print(BAR)
for nm, st in SCHEMES:
    print()
    print("  %s" % nm)
    print("     q      ||dP_matter||   ratio    ||dP_field||    ratio    |dPm+dPf|/|dPm|")
    pm = pf = None
    for qq in (0.1, 0.2, 0.4, 0.8):
        r = run(st, qq, 0.0)
        dm, df = r['dm'], r['df']
        a, b = np.linalg.norm(dm), np.linalg.norm(df)
        rm = "  --  " if pm is None else "%6.3f" % (a / pm)
        rf = "  --  " if pf is None else "%6.3f" % (b / pf)
        print("   %5.2f   %.6e   %s   %.6e   %s   %.6e" % (
            qq, a, rm, b, rf, np.linalg.norm(dm + df) / max(a, 1e-300)))
        pm, pf = a, b
    print("     (ratio = this q / previous q, q doubling.  2 => linear, 4 => quadratic.)")
