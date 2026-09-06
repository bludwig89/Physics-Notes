"""
ca_link_hamiltonian.py — Real-time Kogut–Susskind link Hamiltonian evolution
=============================================================================

Created: 2026-06-06 - audit B.2 item 2 ("real-time link Hamiltonian evolution
(Kogut–Susskind-type) is not built; Wilson-loop tests run on frozen links").

This module promotes the confinement sector from *frozen-link Euclidean
measurement* (ca_confinement.py, F70/F94) and the *single-plaquette transfer
operator* (F100/F101 compact rotor) to genuine **real-time Hamiltonian
evolution of the gauge links** on a 2D spatial lattice (2+1D theory):

    H  =  (g²/2) Σ_links  Ê_ℓ²   −   λ Σ_plaq  cos φ̂_p

with Ê_ℓ the integer (compact) electric field on link ℓ and cos φ̂_p the
plaquette magnetic operator (raising/lowering of the flux).  This is exactly
the multi-plaquette, real-time generalisation of the F101 rotor
H = (1/2χ)Ê² − λ cos φ̂ — the rotor chain made dynamical.  Mapping to the
rotor convention:  a single open plaquette has 4 exclusive boundary links, so
(g²/2)·4·m² = (1/2χ)m²  ⇒  χ = 1/(4g²);  λ = χΩ² connects to the rule's
rotation rate (F100/F101 S5).

Gauge groups
------------
* 'Z3'  (or any integer N ≥ 2): the centre group ℤ_N — **exact finite Hilbert
  space**, no truncation error.  ℤ₃ is the SU(3) centre that drives the area
  law (F97–F99).  Electric energy uses the symmetric residue
  s(e) = ((e + N//2) mod N) − N//2, the clock convention matching F99's
  centre weight e^{γ cos(2πn/N)} regime.
* 'U1': compact U(1) — the F101 rotor's parent group; electric basis truncated
  at |m| ≤ m_max (truncation-convergence is a *checked* quantity, same policy
  as F101 S1).

Gauss law — exact by construction (dual / height representation)
----------------------------------------------------------------
On an open 2D lattice the constraint  (div Ê)(x) = q(x)  is solved exactly:

    Ê_ℓ  =  m_{p⁺(ℓ)} − m_{p⁻(ℓ)} + η_ℓ ,

where m_p are integer "height" operators on plaquettes (outer face ≡ 0),
p±(ℓ) the two faces adjacent to ℓ, and η a fixed background with
div η = q (a string of η = q links along a path joining the ± charges).
Every state of the height Hilbert space is gauge-invariant; cos φ̂_p acts as
(Γ_p + Γ_p†)/2 with Γ_p the raising operator on m_p.  The equivalence with
the *direct* link-basis Hamiltonian restricted to the Gauss sector is a
machine-precision verified identity (test F110 C1), not an assumption.

What this enables
-----------------
* Static potential V(R) from ground states of H with a charge pair —
  Hamiltonian (energy-per-length) string tension at all couplings, exact
  V(R) = (g²/2)·q²·R at λ = 0 (strong coupling).
* Real-time flux-string dynamics: prepare a string, quench, watch ⟨Ê²_ℓ⟩(t)
  — string persistence (confinement) in *real time*, unitarity and energy
  conservation at machine precision.
* The long-pole dependency for P2 (dynamical baryon, audit C.8) — energy
  stored in links is now a dynamical, measurable object.

Scope (honest):  pure-gauge sector with *static* charges; ℤ_N exact / U(1)
truncated; 2D spatial lattices (open boundaries).  Dynamical-matter coupling
remains future work (the centre projection argument F97–F99 is why ℤ₃ is the
load-bearing case).

The SU(3) Casimir ladder is NO LONGER future work, and how it relates to this
module is now settled (F325, 2026-08-18, ledger record S22):

  * It was built on 2026-06-07 -- `su3_ladder.py`, finding F111b -- five days
    before F144.  F110's deferral here, and F294's request for it, were both
    already answered when they were written.
  * **The Ehat spectrum in this module is a solvability choice, not the model's.**
    The rule's own (E, B) are CONTINUOUS real fields under an SO(2) rotation
    (F26, `weak_wmu._f26_rotation_step`), and the model's links are SU(3)-valued
    matrices (`strong.py`, `gluon.py`, `bcc_action.plaquette_field_strength_su3`,
    F94, F99 D3; the group is derived in F317).  The integer ladder here is the
    exactly-solvable abelian reduction of that -- which is why Gauss's law can be
    solved by heights at all, a construction with no non-abelian analogue.
  * **C7 therefore transfers a COEFFICIENT, not a spectrum.**  Check C1 verifies
    that the F101 rotor IS this Hamiltonian on one plaquette's Gauss sector, so
    both sides of the matching carry the same operator and its eigenvalue
    cancels: chi = 1/(4 g^2), for any group, carrying only the geometric factor
    n = 4.  Matching this module's integer levels against an SU(N) link's C_2
    instead yields a constant (C_F at N <= 3) that is a spectral discrepancy
    rather than a stiffness.  That mixed reading is the whole of the X1 fork,
    and it is CLOSED: branch A excluded, branch B (g_s = 1/2) adopted.
  * **Validity bound, the useful survivor of the withdrawn CN19:** the Z_N ladder
    is a faithful effective description of the SU(N) k-string ladder only for
    N <= 3, and off the k-string tower it is not faithful even at N = 3 -- the
    sextet gives chi = 3/10 against 3/4, and triality-0 irreps give s^2 = 0
    against C_2 != 0, i.e. zero electric cost for an adjoint link.  Use this
    module for the k-string sector at N <= 3, and `su3_ladder.py` otherwise.

All entries dated: 2026-06-06.
"""

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh, expm_multiply


# ══════════════════════════════════════════════════════════════════
#  Geometry — open rectangular grid of plaquettes
# ══════════════════════════════════════════════════════════════════

class PlaquetteGrid:
    """
    Open 2D lattice with nx × ny plaquettes (sites (i,j), 0≤i≤nx, 0≤j≤ny).

    Links (all oriented +x / +y):
      H(i,j): site (i,j) → (i+1,j),  i ∈ [0,nx), j ∈ [0,ny]
      V(i,j): site (i,j) → (i,j+1),  i ∈ [0,nx], j ∈ [0,ny)

    Dual (height) solution of Gauss law:
      E_H(i,j) = m(i,j) − m(i,j−1)      (plaquette above − below)
      E_V(i,j) = m(i−1,j) − m(i,j)      (plaquette left − right)
    with m ≡ 0 on the outer face.  div(curl m) = 0 identically (asserted).

    Each link is stored as (p_plus, p_minus): plaquette indices or -1 (outer).
    """

    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.n_p = nx * ny
        self._pidx = lambda i, j: j * nx + i

        links = []          # (kind, i, j, p_plus, p_minus)
        self.link_id = {}
        for j in range(ny + 1):
            for i in range(nx):
                p_up = self._pidx(i, j) if j < ny else -1
                p_dn = self._pidx(i, j - 1) if j > 0 else -1
                self.link_id[('H', i, j)] = len(links)
                links.append(('H', i, j, p_up, p_dn))
        for j in range(ny):
            for i in range(nx + 1):
                p_l = self._pidx(i - 1, j) if i > 0 else -1
                p_r = self._pidx(i, j) if i < nx else -1
                self.link_id[('V', i, j)] = len(links)
                links.append(('V', i, j, p_l, p_r))
        self.links = links
        self.n_links = len(links)

        # plaquette → (bottom, right, top, left) link ids with signs +,+,−,−
        self.plaq_links = []
        for j in range(ny):
            for i in range(nx):
                self.plaq_links.append((
                    self.link_id[('H', i, j)],       # bottom  (+)
                    self.link_id[('V', i + 1, j)],   # right   (+)
                    self.link_id[('H', i, j + 1)],   # top     (−)
                    self.link_id[('V', i, j)],       # left    (−)
                ))

        self._assert_curl_divergence_free()

    # -- internal sanity: div(curl m) == 0 for random integer heights
    def _assert_curl_divergence_free(self, seed=0):
        rng = np.random.default_rng(seed)
        m = rng.integers(-3, 4, self.n_p)
        E = self.curl_heights(m)
        div = self.divergence(E)
        assert np.all(div == 0), "dual construction broken: div(curl m) != 0"

    def curl_heights(self, m):
        """E_ℓ = m[p⁺] − m[p⁻] (outer face = 0) for integer height vector m."""
        m_ext = np.append(np.asarray(m), 0)          # index -1 → 0
        E = np.empty(self.n_links, dtype=m_ext.dtype)
        for ℓ, (_k, _i, _j, pp, pm) in enumerate(self.links):
            E[ℓ] = m_ext[pp] - m_ext[pm]
        return E

    def divergence(self, E):
        """Integer lattice divergence (div E)(site) = Σ out − Σ in."""
        div = np.zeros((self.nx + 1, self.ny + 1), dtype=np.asarray(E).dtype)
        for ℓ, (k, i, j, _pp, _pm) in enumerate(self.links):
            if k == 'H':
                div[i, j] += E[ℓ]
                div[i + 1, j] -= E[ℓ]
            else:
                div[i, j] += E[ℓ]
                div[i, j + 1] -= E[ℓ]
        return div

    def background_string(self, x1, x2, row, q=1):
        """
        Background η with div η = +q at site (x1,row), −q at (x2,row):
        η = q on the horizontal links (i,row), x1 ≤ i < x2.  Returns (η, charges).
        """
        eta = np.zeros(self.n_links, dtype=np.int64)
        for i in range(x1, x2):
            eta[self.link_id[('H', i, row)]] = q
        charges = {}
        if x2 > x1:
            charges[(x1, row)] = q
            charges[(x2, row)] = -q
        div = self.divergence(eta)
        for (sx, sy), qq in charges.items():
            assert div[sx, sy] == qq
        return eta, charges


# ══════════════════════════════════════════════════════════════════
#  Basis bookkeeping (mixed-radix heights) and electric values
# ══════════════════════════════════════════════════════════════════

def _enumerate_digits(n_p, d):
    """All d**n_p height configurations as an (dim, n_p) int8/int16 array."""
    dim = d ** n_p
    dtype = np.int8 if d < 127 else np.int16
    digits = np.empty((dim, n_p), dtype=dtype)
    t = np.arange(dim)
    for p in range(n_p):
        digits[:, p] = t % d
        t //= d
    return digits


def _strides(n_p, d):
    return np.array([d ** p for p in range(n_p)], dtype=np.int64)


def sym_residue(e, N):
    """Symmetric residue of e mod N: values in {−⌊N/2⌋, …, ⌈N/2⌉−1}·sign conv.
    For N=3: {0,1,2,…} → {0,1,−1}."""
    return ((np.asarray(e) + N // 2) % N) - N // 2


def _heights_from_digits(digits, group, m_max):
    """Physical height values per basis state (int64)."""
    if group == 'U1':
        return digits.astype(np.int64) - m_max
    return digits.astype(np.int64)        # Z_N: heights are mod-N classes


def link_E_values(geom, digits, eta, group='Z3', m_max=None, N=3):
    """
    (dim, n_links) electric values per basis state.
    Z_N: symmetric residue of (m⁺ − m⁻ + η) mod N.   U(1): raw integer.
    """
    m = _heights_from_digits(digits, group, m_max)
    m_ext = np.concatenate([m, np.zeros((m.shape[0], 1), dtype=np.int64)],
                           axis=1)                      # index -1 → 0
    E = np.empty((m.shape[0], geom.n_links), dtype=np.int64)
    for ℓ, (_k, _i, _j, pp, pm) in enumerate(geom.links):
        E[:, ℓ] = m_ext[:, pp] - m_ext[:, pm] + int(eta[ℓ])
    if group != 'U1':
        E = sym_residue(E, N)
    return E


# ══════════════════════════════════════════════════════════════════
#  Dual (gauge-invariant) Kogut–Susskind Hamiltonian
# ══════════════════════════════════════════════════════════════════

def build_dual_hamiltonian(geom, eta=None, g2=1.0, lam=1.0,
                           group='Z3', m_max=None):
    """
    Sparse real-symmetric H = (g²/2) Σ_ℓ s(Ê_ℓ)² − (λ/2) Σ_p (Γ_p + Γ_p†)
    in the height (dual) basis.  Gauss law div Ê = q is exact by construction
    (the background η carries the static charges).

    group: 'Z3' (or any int N ≥ 2 — pass group=N) or 'U1' (needs m_max).
    Returns (H_csr, digits) — digits for observable evaluation.
    """
    if eta is None:
        eta = np.zeros(geom.n_links, dtype=np.int64)
    if group == 'U1':
        assert m_max is not None, "U1 needs m_max"
        d = 2 * m_max + 1
        N = None
    else:
        N = 3 if group == 'Z3' else int(group)
        d = N
    n_p = geom.n_p
    dim = d ** n_p
    digits = _enumerate_digits(n_p, d)
    stride = _strides(n_p, d)

    E = link_E_values(geom, digits, eta, group=('U1' if group == 'U1' else 'ZN'),
                      m_max=m_max, N=(N or 3))
    diag = 0.5 * g2 * np.sum(E.astype(np.float64) ** 2, axis=1)

    rows, cols, vals = [np.arange(dim)], [np.arange(dim)], [diag]
    idx = np.arange(dim, dtype=np.int64)
    for p in range(n_p):
        dp = digits[:, p].astype(np.int64)
        if group == 'U1':
            sel = dp < d - 1
            j = idx[sel] + stride[p]
            i = idx[sel]
        else:                              # Z_N: cyclic raising
            new = (dp + 1) % N
            j = idx + (new - dp) * stride[p]
            i = idx
        rows.append(i); cols.append(j)
        vals.append(np.full(len(i), -0.5 * lam))
        rows.append(j); cols.append(i)     # hermitian conjugate
        vals.append(np.full(len(i), -0.5 * lam))

    H = sp.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(dim, dim))
    return H, digits


def ground_state(H, k=1, dense_threshold=600):
    """(E0, ψ0) — dense eigh for small dims, Lanczos (eigsh) otherwise."""
    if H.shape[0] <= dense_threshold:
        w, v = np.linalg.eigh(H.toarray())
        return float(w[0]), v[:, 0]
    w, v = eigsh(H, k=k, which='SA')
    order = np.argsort(w)
    return float(w[order[0]]), v[:, order[0]]


def ground_energy_lambda0(geom, eta, g2=1.0, group='Z3', m_max=None):
    """
    λ = 0 ground energy without diagonalisation: H is diagonal, so
    E0 = min over height configs of (g²/2)Σ s(E_ℓ)².  Exact (Tier-1 check
    target: equals (g²/2)·q²·R for a straight string of R links).
    """
    H, _ = build_dual_hamiltonian(geom, eta, g2=g2, lam=0.0,
                                  group=group, m_max=m_max)
    return float(H.diagonal().min())


# ══════════════════════════════════════════════════════════════════
#  Real-time evolution and observables
# ══════════════════════════════════════════════════════════════════

def evolve_krylov(H, psi0, t_grid):
    """
    Unitary real-time evolution ψ(t) = e^{−iHt} ψ0 on the given time grid
    (Krylov expm_multiply; machine-accurate — drift is *checked*, not assumed).
    Returns array (n_t, dim) complex.
    """
    t_grid = np.asarray(t_grid, dtype=float)
    out = np.empty((len(t_grid), H.shape[0]), dtype=complex)
    psi = psi0.astype(complex)
    t_prev = 0.0
    A = (-1j) * H.tocsc().astype(complex)
    for n, t in enumerate(t_grid):
        dt = t - t_prev
        if dt != 0.0:
            psi = expm_multiply(A * dt, psi)
        out[n] = psi
        t_prev = t
    return out


def evolve_dense(H, psi0, t_grid):
    """Exact (eigendecomposition) evolution — small dims; the cross-check
    used to certify the Krylov path."""
    w, V = np.linalg.eigh(H.toarray())
    c = V.conj().T @ psi0.astype(complex)
    t_grid = np.asarray(t_grid, dtype=float)
    return np.array([V @ (np.exp(-1j * w * t) * c) for t in t_grid])


def link_E2_profile(psi, E_vals):
    """⟨ s(Ê_ℓ)² ⟩ per link.  E_vals from link_E_values (dim, n_links)."""
    w = np.abs(psi) ** 2
    return w @ (E_vals.astype(np.float64) ** 2)


def energy_expect(H, psi):
    return float(np.real(np.vdot(psi, H @ psi)))


def plaquette_cos_expect(psi, digits, p, group='Z3', m_max=None):
    """⟨ cos φ̂_p ⟩ = ⟨ (Γ_p + Γ_p†)/2 ⟩ for plaquette p."""
    n_p = digits.shape[1]
    if group == 'U1':
        d = 2 * m_max + 1
    else:
        d = 3 if group == 'Z3' else int(group)
    stride = _strides(n_p, d)
    idx = np.arange(len(psi), dtype=np.int64)
    dp = digits[:, p].astype(np.int64)
    if group == 'U1':
        sel = dp < d - 1
        j = idx[sel] + stride[p]
        amp = np.vdot(psi[j], psi[sel])           # ⟨ψ|Γ†|ψ⟩ component
    else:
        N = d
        new = (dp + 1) % N
        j = idx + (new - dp) * stride[p]
        amp = np.vdot(psi[j], psi)
    return float(np.real(amp))                     # (Γ+Γ†)/2 → Re for real ψ…
    # (general ψ: Re⟨Γ⟩ is exactly ⟨(Γ+Γ†)/2⟩)


# ══════════════════════════════════════════════════════════════════
#  Static potential V(R) and Hamiltonian string tension
# ══════════════════════════════════════════════════════════════════

def static_potential(geom, row, R_list, g2=1.0, lam=1.0,
                     group='Z3', m_max=None, center=True):
    """
    V(R) = E0(R) − E0(0) from ground states with a ±1 charge pair separated
    by R horizontal links on `row`.  Charges centred unless center=False.
    Returns dict R → V(R).
    """
    E0_vac = None
    out = {}
    for R in [0] + list(R_list):
        if R == 0:
            eta = np.zeros(geom.n_links, dtype=np.int64)
        else:
            x1 = (geom.nx - R) // 2 if center else 0
            eta, _ = geom.background_string(x1, x1 + R, row)
        if lam == 0.0:
            E0 = ground_energy_lambda0(geom, eta, g2=g2, group=group,
                                       m_max=m_max)
        else:
            H, _ = build_dual_hamiltonian(geom, eta, g2=g2, lam=lam,
                                          group=group, m_max=m_max)
            E0, _ = ground_state(H)
        if R == 0:
            E0_vac = E0
        else:
            out[R] = E0 - E0_vac
    return out


def fit_linear_potential(V):
    """Least-squares V(R) = c + σR over the dict V; returns (σ, c, rms)."""
    R = np.array(sorted(V.keys()), dtype=float)
    y = np.array([V[r] for r in sorted(V.keys())])
    A = np.vstack([R, np.ones_like(R)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    rms = float(np.sqrt(np.mean((A @ coef - y) ** 2)))
    return float(coef[0]), float(coef[1]), rms


def sigma_strong_pt2(geom, row, g2=1.0, group='Z3', m_max=None):
    """
    Second-order strong-coupling PT coefficient c₂ in
    σ(λ) = g²/2 − c₂ λ² + O(λ³): programmatic sum over single-plaquette
    flips m_p → ±1 of (1/4)/ΔE(p,±), differenced between a length-R and
    length-(R−1) string (interior increment — uses R=2 vs R=1 on the given
    geometry, exact integer arithmetic in the denominators).
    """
    def E2_second_order(eta):
        # base config: all heights 0
        base_E = eta.copy()
        N = 3 if group == 'Z3' else (None if group == 'U1' else int(group))

        def diag_energy(E):
            Ev = sym_residue(E, N) if N else E
            return 0.5 * g2 * np.sum(Ev.astype(float) ** 2)

        e0 = diag_energy(base_E)
        corr = 0.0
        for p in range(geom.n_p):
            for s in (+1, -1):
                m = np.zeros(geom.n_p, dtype=np.int64)
                m[p] = s
                dE = diag_energy(base_E + geom.curl_heights(m)) - e0
                corr += 0.25 / dE
        return corr            # ΔE^(2) = −corr · λ²

    x1 = (geom.nx - 2) // 2
    eta2, _ = geom.background_string(x1, x1 + 2, row)
    eta1, _ = geom.background_string(x1, x1 + 1, row)
    c2 = E2_second_order(eta2) - E2_second_order(eta1)
    return float(c2)


# ══════════════════════════════════════════════════════════════════
#  Direct link-basis Hamiltonian (Gauss-sector) — the equivalence check
# ══════════════════════════════════════════════════════════════════

def build_direct_zn(geom, g2=1.0, lam=1.0, N=3, charges=None):
    """
    ℤ_N Kogut–Susskind Hamiltonian in the *direct* link electric basis,
    restricted to the Gauss sector (div e ≡ q mod N at every site, q from
    `charges`: dict (i,j) → q).  Small lattices only (dim N**n_links).

    Returns (H_csr on the physical subspace, n_phys).
    Used for the machine-precision spectral identity with the dual builder.
    """
    if charges is None:
        charges = {}
    nl = geom.n_links
    dim = N ** nl
    digits = _enumerate_digits(nl, N)            # electric values 0..N−1
    stride = _strides(nl, N)

    # Gauss selection (diagonal in the electric basis)
    ok = np.ones(dim, dtype=bool)
    e_sym = sym_residue(digits.astype(np.int64), N)
    for i in range(geom.nx + 1):
        for j in range(geom.ny + 1):
            div = np.zeros(dim, dtype=np.int64)
            for ℓ, (k, li, lj, _pp, _pm) in enumerate(geom.links):
                if k == 'H':
                    if (li, lj) == (i, j):
                        div += e_sym[:, ℓ]
                    if (li + 1, lj) == (i, j):
                        div -= e_sym[:, ℓ]
                else:
                    if (li, lj) == (i, j):
                        div += e_sym[:, ℓ]
                    if (li, lj + 1) == (i, j):
                        div -= e_sym[:, ℓ]
            q = charges.get((i, j), 0)
            ok &= ((div - q) % N == 0)

    phys = np.nonzero(ok)[0]
    n_phys = len(phys)
    lookup = -np.ones(dim, dtype=np.int64)
    lookup[phys] = np.arange(n_phys)

    diag = 0.5 * g2 * np.sum(e_sym[phys].astype(float) ** 2, axis=1)
    rows, cols, vals = [np.arange(n_phys)], [np.arange(n_phys)], [diag]

    for (b, r, t, l) in geom.plaq_links:
        d_new = digits[phys].astype(np.int64)
        delta = np.zeros((n_phys,), dtype=np.int64)
        for ℓ, s in ((b, +1), (r, +1), (t, -1), (l, -1)):
            old = d_new[:, ℓ]
            new = (old + s) % N
            delta += (new - old) * stride[ℓ]
        j_full = phys + delta
        j_sub = lookup[j_full]
        assert np.all(j_sub >= 0), "plaquette operator left the Gauss sector"
        rows.append(np.arange(n_phys)); cols.append(j_sub)
        vals.append(np.full(n_phys, -0.5 * lam))
        rows.append(j_sub); cols.append(np.arange(n_phys))
        vals.append(np.full(n_phys, -0.5 * lam))

    H = sp.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(n_phys, n_phys))
    return H, n_phys


# ══════════════════════════════════════════════════════════════════
#  F101 rotor contact
# ══════════════════════════════════════════════════════════════════

def rotor_hamiltonian(lam, chi=1.0, m_max=20):
    """F101 compact rotor H = (1/2χ)Ê² − λ cos φ̂ in the charge basis
    (independent tridiagonal construction — the contact reference)."""
    m = np.arange(-m_max, m_max + 1)
    H = np.diag(m.astype(float) ** 2 / (2.0 * chi))
    off = -0.5 * lam * np.ones(2 * m_max)
    H += np.diag(off, 1) + np.diag(off, -1)
    return H


def rotor_sigma1(lam, chi=1.0, m_max=20):
    """σ₁ = −ln⟨e^{iφ}⟩ of the rotor ground state (F99/F101 convention)."""
    w, v = np.linalg.eigh(rotor_hamiltonian(lam, chi, m_max))
    g = v[:, 0]
    s1 = float(np.sum(g[:-1] * g[1:]))
    return -np.log(s1), s1


# ══════════════════════════════════════════════════════════════════
#  3D (general-graph) tree-gauge construction — F111
# ══════════════════════════════════════════════════════════════════
#
# In 3D the planar height trick no longer applies (plaquette fluxes obey
# Bianchi constraints per cube), but Gauss's law is still solved EXACTLY by
# a maximal-tree elimination: choose a spanning tree T of the lattice graph;
# the electric fields on off-tree links are the free physical variables, and
# every tree-link field is fixed by the constraint, linearly:
#
#       E_tree = M · E_off + b(q),     div E = q  exact by construction,
#
# with M an integer matrix (leaf-first elimination) and b the static-charge
# background.  Physical dimension = d^(n_links − n_sites + 1), the cycle
# space of the graph.  Each plaquette is a cycle, so the magnetic operator
# Γ_p shifts the off-tree digits by the off-tree part of the plaquette cycle
# vector; consistency of the tree part (c_tree = M·c_off) is ASSERTED for
# every plaquette at build time.  Reduces to the F110 dual height
# representation in 2D (verified as a spectral identity, F111 T1).

class LatticeGraph3D:
    """
    Open rectangular lattice with nx × ny × nz cells (nz=0 → 2D plane).
    Sites (i,j,k); links oriented +x/+y/+z; plaquettes in xy, xz, yz planes.
    BFS spanning tree from (0,0,0), x-links explored first (so straight
    x-axis charge strings live on tree links).
    """

    def __init__(self, nx, ny, nz=0):
        self.nx, self.ny, self.nz = nx, ny, nz
        sites = [(i, j, k)
                 for k in range(nz + 1)
                 for j in range(ny + 1)
                 for i in range(nx + 1)]
        self.sites = sites
        self.site_id = {s: n for n, s in enumerate(sites)}
        self.n_sites = len(sites)

        links = []        # (a_id, b_id) oriented a -> b
        self.link_id = {}

        def add_link(axis, i, j, k, di, dj, dk):
            a = self.site_id[(i, j, k)]
            b = self.site_id[(i + di, j + dj, k + dk)]
            self.link_id[(axis, i, j, k)] = len(links)
            links.append((a, b))

        for k in range(nz + 1):
            for j in range(ny + 1):
                for i in range(nx):
                    add_link('x', i, j, k, 1, 0, 0)
        for k in range(nz + 1):
            for j in range(ny):
                for i in range(nx + 1):
                    add_link('y', i, j, k, 0, 1, 0)
        for k in range(nz):
            for j in range(ny + 1):
                for i in range(nx + 1):
                    add_link('z', i, j, k, 0, 0, 1)
        self.links = links
        self.n_links = len(links)

        # plaquettes as 4-link cycles with orientation signs
        plaqs = []
        L = self.link_id
        for k in range(nz + 1):                      # xy faces
            for j in range(ny):
                for i in range(nx):
                    plaqs.append([(L[('x', i, j, k)], +1),
                                  (L[('y', i + 1, j, k)], +1),
                                  (L[('x', i, j + 1, k)], -1),
                                  (L[('y', i, j, k)], -1)])
        for k in range(nz):                          # xz faces
            for j in range(ny + 1):
                for i in range(nx):
                    plaqs.append([(L[('x', i, j, k)], +1),
                                  (L[('z', i + 1, j, k)], +1),
                                  (L[('x', i, j, k + 1)], -1),
                                  (L[('z', i, j, k)], -1)])
        for k in range(nz):                          # yz faces
            for j in range(ny):
                for i in range(nx + 1):
                    plaqs.append([(L[('y', i, j, k)], +1),
                                  (L[('z', i, j + 1, k)], +1),
                                  (L[('y', i, j, k + 1)], -1),
                                  (L[('z', i, j, k)], -1)])
        self.plaqs = plaqs
        self.n_plaqs = len(plaqs)

        self._build_tree()
        self._build_gauss_solver()

    # ---- spanning tree (BFS, x first because links were added x first)
    def _build_tree(self):
        adj = [[] for _ in range(self.n_sites)]
        for ℓ, (a, b) in enumerate(self.links):
            adj[a].append((b, ℓ))
            adj[b].append((a, ℓ))
        parent_link = [-1] * self.n_sites          # tree link to parent
        seen = [False] * self.n_sites
        order = [0]
        seen[0] = True
        head = 0
        while head < len(order):
            s = order[head]; head += 1
            for (t, ℓ) in adj[s]:
                if not seen[t]:
                    seen[t] = True
                    parent_link[t] = ℓ
                    order.append(t)
        assert all(seen), "lattice graph not connected"
        self.bfs_order = order
        self.parent_link = parent_link
        self.tree_links = sorted(set(parent_link) - {-1})
        self.off_links = [ℓ for ℓ in range(self.n_links)
                          if ℓ not in set(self.tree_links)]
        self.n_off = len(self.off_links)
        assert self.n_off == self.n_links - self.n_sites + 1

    # ---- Gauss elimination: E_tree = M · E_off + b(q), integer exact
    def _solve_tree(self, E_off_vec, q_site):
        """Leaf-first elimination.  E_off_vec over off_links; q_site over
        sites (both integer arrays).  Returns full integer E vector."""
        E = np.zeros(self.n_links, dtype=np.int64)
        for n, ℓ in enumerate(self.off_links):
            E[ℓ] = E_off_vec[n]
        known = [False] * self.n_links
        for ℓ in self.off_links:
            known[ℓ] = True
        # incident links per site with outgoing sign
        inc = [[] for _ in range(self.n_sites)]
        for ℓ, (a, b) in enumerate(self.links):
            inc[a].append((ℓ, +1))
            inc[b].append((ℓ, -1))
        for s in reversed(self.bfs_order):
            if s == self.bfs_order[0]:
                resid = sum(sgn * E[ℓ] for (ℓ, sgn) in inc[s]) - q_site[s]
                assert resid == 0, "total charge not conserved at tree root"
                continue
            ℓp = self.parent_link[s]
            other = sum(sgn * E[ℓ] for (ℓ, sgn) in inc[s] if ℓ != ℓp)
            sgn_p = +1 if self.links[ℓp][0] == s else -1
            # sgn_p * E[ℓp] + other = q  →  E[ℓp] = sgn_p * (q − other)
            E[ℓp] = sgn_p * (q_site[s] - other)
            known[ℓp] = True
        return E

    def _build_gauss_solver(self):
        nq = np.zeros(self.n_sites, dtype=np.int64)
        cols = []
        for n in range(self.n_off):
            e = np.zeros(self.n_off, dtype=np.int64)
            e[n] = 1
            cols.append(self._solve_tree(e, nq)[self.tree_links])
        self.M = np.array(cols, dtype=np.int64).T      # (n_tree, n_off)
        # plaquette-cycle consistency: c_tree == M · c_off for every cycle
        self._cycles_off = []
        off_pos = {ℓ: n for n, ℓ in enumerate(self.off_links)}
        tree_pos = {ℓ: n for n, ℓ in enumerate(self.tree_links)}
        for cyc in self.plaqs:
            c_off = np.zeros(self.n_off, dtype=np.int64)
            c_tree = np.zeros(len(self.tree_links), dtype=np.int64)
            for (ℓ, sgn) in cyc:
                if ℓ in off_pos:
                    c_off[off_pos[ℓ]] = sgn
                else:
                    c_tree[tree_pos[ℓ]] = sgn
            assert np.array_equal(self.M @ c_off, c_tree), \
                "plaquette cycle inconsistent with tree elimination"
            self._cycles_off.append(c_off)

    def charge_background(self, charges):
        """b(q): integer tree-link background for {site_tuple: q} charges."""
        q = np.zeros(self.n_sites, dtype=np.int64)
        for s, qq in charges.items():
            q[self.site_id[s]] = qq
        assert q.sum() == 0, "tree gauge needs total charge 0 (open lattice)"
        return self._solve_tree(np.zeros(self.n_off, dtype=np.int64), q)


def build_tree_hamiltonian(graph, charges=None, g2=1.0, lam=1.0,
                           group='Z3', m_max=None):
    """
    Sparse real-symmetric KS Hamiltonian in the tree-gauge (off-tree electric)
    basis on a LatticeGraph3D:  H = (g²/2) Σ_ℓ s(Ê_ℓ)² − (λ/2) Σ_p (Γ_p+Γ_p†),
    Gauss law exact by construction.  Returns (H_csr, digits, E_vals) with
    E_vals the (dim, n_links) integer electric table for observables.
    """
    if group == 'U1':
        assert m_max is not None
        d = 2 * m_max + 1
        N = None
    else:
        N = 3 if group == 'Z3' else int(group)
        d = N
    n_off = graph.n_off
    dim = d ** n_off
    digits = _enumerate_digits(n_off, d)
    stride = _strides(n_off, d)

    E_off = digits.astype(np.int64) - (m_max if group == 'U1' else 0)
    b = (graph.charge_background(charges) if charges
         else np.zeros(graph.n_links, dtype=np.int64))
    E_vals = np.empty((dim, graph.n_links), dtype=np.int64)
    for n, ℓ in enumerate(graph.off_links):
        E_vals[:, ℓ] = E_off[:, n] + b[ℓ]
    E_tree = E_off @ graph.M.T + b[graph.tree_links]
    for n, ℓ in enumerate(graph.tree_links):
        E_vals[:, ℓ] = E_tree[:, n]
    if N is not None:
        E_vals = sym_residue(E_vals, N)
    diag = 0.5 * g2 * np.sum(E_vals.astype(np.float64) ** 2, axis=1)

    rows, cols, vals = [np.arange(dim)], [np.arange(dim)], [diag]
    idx = np.arange(dim, dtype=np.int64)
    for c_off in graph._cycles_off:
        touched = np.nonzero(c_off)[0]
        if N is not None:                  # Z_N: cyclic shifts, all states map
            delta = np.zeros(dim, dtype=np.int64)
            for n in touched:
                old = digits[:, n].astype(np.int64)
                new = (old + c_off[n]) % N
                delta += (new - old) * stride[n]
            i, j = idx, idx + delta
        else:                              # U(1): clip at the truncation edge
            sel = np.ones(dim, dtype=bool)
            delta = np.zeros(dim, dtype=np.int64)
            for n in touched:
                old = digits[:, n].astype(np.int64)
                new = old + c_off[n]
                sel &= (new >= 0) & (new < d)
                delta += (new - old) * stride[n]
            i, j = idx[sel], (idx + delta)[sel]
        rows.append(i); cols.append(j)
        vals.append(np.full(len(i), -0.5 * lam))
        rows.append(j); cols.append(i)
        vals.append(np.full(len(i), -0.5 * lam))

    H = sp.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(dim, dim))
    return H, digits, E_vals


def build_direct_zn_graph(graph, g2=1.0, lam=1.0, N=3, charges=None):
    """
    Direct link-basis ℤ_N KS Hamiltonian on a LatticeGraph3D, restricted to
    the Gauss sector (div e ≡ q mod N at every site).  Small graphs only.
    Returns (H_csr, n_phys).  The independent identity check for the
    tree-gauge construction (F111 T1).
    """
    if charges is None:
        charges = {}
    nl = graph.n_links
    dim = N ** nl
    digits = _enumerate_digits(nl, N)
    stride = _strides(nl, N)
    e_sym = sym_residue(digits.astype(np.int64), N)

    ok = np.ones(dim, dtype=bool)
    for s_id in range(graph.n_sites):
        div = np.zeros(dim, dtype=np.int64)
        for ℓ, (a, b) in enumerate(graph.links):
            if a == s_id:
                div += e_sym[:, ℓ]
            if b == s_id:
                div -= e_sym[:, ℓ]
        q = charges.get(graph.sites[s_id], 0)
        ok &= ((div - q) % N == 0)

    phys = np.nonzero(ok)[0]
    n_phys = len(phys)
    lookup = -np.ones(dim, dtype=np.int64)
    lookup[phys] = np.arange(n_phys)

    diag = 0.5 * g2 * np.sum(e_sym[phys].astype(float) ** 2, axis=1)
    rows, cols, vals = [np.arange(n_phys)], [np.arange(n_phys)], [diag]
    for cyc in graph.plaqs:
        delta = np.zeros(n_phys, dtype=np.int64)
        for (ℓ, sgn) in cyc:
            old = digits[phys, ℓ].astype(np.int64)
            new = (old + sgn) % N
            delta += (new - old) * stride[ℓ]
        j_sub = lookup[phys + delta]
        assert np.all(j_sub >= 0), "plaquette operator left the Gauss sector"
        rows.append(np.arange(n_phys)); cols.append(j_sub)
        vals.append(np.full(n_phys, -0.5 * lam))
        rows.append(j_sub); cols.append(np.arange(n_phys))
        vals.append(np.full(n_phys, -0.5 * lam))

    H = sp.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(n_phys, n_phys))
    return H, n_phys


def tree_lambda0_min(graph, charges=None, g2=1.0, group='Z3', m_max=None,
                     chunk=200_000):
    """
    λ=0 ground energy in the tree gauge WITHOUT building H: streams over the
    off-tree basis in chunks, computing the diagonal electric energy only.
    Exact (integer arithmetic inside, min of exact halves).
    """
    if group == 'U1':
        d = 2 * m_max + 1
        N = None
    else:
        N = 3 if group == 'Z3' else int(group)
        d = N
    n_off = graph.n_off
    dim = d ** n_off
    b = (graph.charge_background(charges) if charges
         else np.zeros(graph.n_links, dtype=np.int64))
    b_off = np.array([b[ℓ] for ℓ in graph.off_links], dtype=np.int64)
    b_tree = b[graph.tree_links]
    best = None
    for start in range(0, dim, chunk):
        idx = np.arange(start, min(start + chunk, dim), dtype=np.int64)
        digs = np.empty((len(idx), n_off), dtype=np.int64)
        t = idx.copy()
        for p in range(n_off):
            digs[:, p] = t % d
            t //= d
        E_off = digs - (m_max if group == 'U1' else 0)
        E2 = 0
        Eo = E_off + b_off
        Et = E_off @ graph.M.T + b_tree
        if N is not None:
            Eo = sym_residue(Eo, N)
            Et = sym_residue(Et, N)
        s = np.sum(Eo ** 2, axis=1) + np.sum(Et ** 2, axis=1)
        m = int(s.min())
        best = m if best is None else min(best, m)
    return 0.5 * g2 * best


def static_potential_3d(graph_factory, R_list, g2=1.0, lam=1.0,
                        group='Z3', m_max=None, axis_site=(0, 0)):
    """
    V(R) on 3D graphs: charges at (0, j0, k0) and (R, j0, k0).
    graph_factory() → LatticeGraph3D (rebuilt per R only if needed once).
    Returns dict R → V(R) = E0(R) − E0(0).
    """
    graph = graph_factory()
    j0, k0 = axis_site
    out = {}
    E0_vac = None
    for R in [0] + list(R_list):
        charges = None if R == 0 else {(0, j0, k0): 1, (R, j0, k0): -1}
        if lam == 0.0:
            E0 = tree_lambda0_min(graph, charges, g2=g2, group=group,
                                  m_max=m_max)
        else:
            H, _, _ = build_tree_hamiltonian(graph, charges, g2=g2, lam=lam,
                                             group=group, m_max=m_max)
            E0, _ = ground_state(H)
        if R == 0:
            E0_vac = E0
        else:
            out[R] = E0 - E0_vac
    return out


def sigma_strong_pt2_graph(graph, charges_long, charges_short,
                           g2=1.0, group='Z3'):
    """
    2nd-order strong-coupling PT coefficient c₂ for the tree-gauge graph:
    σ(λ) = g²/2 − c₂λ² + O(λ³), from single-plaquette cycle flips on the
    λ=0 string config, differenced between the two charge configs.
    """
    N = 3 if group == 'Z3' else (None if group == 'U1' else int(group))

    def diag_energy(E):
        Ev = sym_residue(E, N) if N else E
        return 0.5 * g2 * np.sum(Ev.astype(float) ** 2)

    def second_order(charges):
        b = graph.charge_background(charges) if charges else \
            np.zeros(graph.n_links, dtype=np.int64)
        e0 = diag_energy(b)
        corr = 0.0
        for cyc in graph.plaqs:
            c = np.zeros(graph.n_links, dtype=np.int64)
            for (ℓ, sgn) in cyc:
                c[ℓ] = sgn
            for s in (+1, -1):
                dE = diag_energy(b + s * c) - e0
                corr += 0.25 / dE
        return corr

    return float(second_order(charges_long) - second_order(charges_short))
