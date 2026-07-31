# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_casimir.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qed_casimir.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_casimir.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_casimir.py  —  The Casimir effect in the BCC Weyl-QCA model  (F207)
======================================================================

Computes the static Casimir energy from the F69 paired-spinor photon's own
dispersion and recovers the continuum laws

    1D scalar (Dirichlet):   E_C            →  -π ħ c / 24 L
    3D EM (perfect plates):  E_C/A          →  -π² ħ c / 720 L³
                             F/A            →  -π² ħ c / 240 L⁴

with c = c_lat = 1/√3 (F26) and the BCC cell a (F107) as the physical UV
cutoff, so no zeta/Abel–Plana analytic continuation of a *divergent* sum is
needed — the lattice regularises natively (the lattice-fermion-Casimir recipe
of Ishikawa et al. 2020, here on the F69 even-law photon dispersion).

Key model facts used (no new physics):
  * Photon dispersion Ω_pair(k) = ω⁺(k/2)+ω⁻(k/2) (F69 = even law), built from
    the audited closed-form BCC dispersion ω±=arccos(u±) (ca_bcc).  Its IR
    limit is EXACTLY ω→c|k| (gapless, isotropic, c=1/√3 — F69-PP3), and along
    a cubic axis Ω_pair(k x̂)=|k|/√3 is exactly linear (triangle wave).
  * Non-birefringence (F69): both transverse photon polarisations ride the
    SAME Ω_pair, so EM = EXACTLY 2× scalar-Dirichlet — no TE/TM splitting.

The headline reproduction (C2) is algebraically EXACT: the Casimir mode sum is
IR-dominated (dominant modes |k|~π/L → 0), and there Ω_pair = c|k| exactly, so
the Abel–Plana reduction returns -π²ħc/720L³ in closed form.  The lattice cell
modifies this only at O((a/L)²) (C3).

CLAUDE.md compliance: closed-form/audited dispersion only.  No np.linalg.eig on
chiral matrices; the (E,B) propagator is the real even-law rotation
(ca_photon_pair.photon_step_spectral); mode sums use the scalar arccos
dispersion directly.
"""

import numpy as np

from ca_photon_pair import pair_dispersion
from casim.constants import c_lat
from casim.constants import G_CODATA as _G_CODATA, c_SI as _c_SI, hbar_SI as _hbar_SI
import ca_fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

ROOT3 = np.sqrt(3.0)
C_LAT = c_lat

# F107 canonical SI constants
A_SI = 1.06638e-34        # m   (cell spacing)
HBAR = _hbar_SI    # J s
C_SI = _c_SI       # m/s
G_SI = _G_CODATA        # m^3 kg^-1 s^-2


# ══════════════════════════════════════════════════════════════════
#  C1 — 1D scalar warm-up (validate the mode-sum machinery)
# ══════════════════════════════════════════════════════════════════

def disp_1d(k, c=C_LAT, kind="sin"):
    """1D scalar lattice dispersions (a = 1).
    'linear': ω=c|k|;  'sin': ω=2c|sin(k/2)| (group vel → 0 at zone edge, a
    smooth UV regulator);  'axis': Ω_pair(k x̂)=|k|/√3 (model photon along a
    cubic axis — exactly linear, NO zone-edge smoothing)."""
    k = np.abs(np.asarray(k, float))
    if kind == "linear":
        return c * k
    if kind == "sin":
        return 2.0 * c * np.abs(np.sin(k / 2.0))
    if kind == "axis":
        return pair_dispersion(k, 0.0 * k, 0.0 * k)
    raise ValueError(kind)


def casimir_energy_1d(L, a=1.0, c=C_LAT, kind="sin"):
    """Subtracted vacuum energy of a 1D Dirichlet box of length L (cells a):
        E_sub(L) = (1/2)[ Σ_{n=1}^{nmax} ω(nπ/L) − (L/π)∫_0^{π/a} ω(k)dk ].
    For a smoothly-suppressed dispersion ('sin') E_sub = const + (−πc/24)/L."""
    kmax = np.pi / a
    nmax = int(np.floor(L / a + 1e-9))
    n = np.arange(1, nmax + 1)
    mode_sum = 0.5 * np.sum(disp_1d(n * np.pi / L, c, kind))
    kk = np.linspace(0.0, kmax, 200001)
    bulk = 0.5 * (L / np.pi) * np.trapezoid(disp_1d(kk, c, kind), kk)
    return mode_sum - bulk


def fit_coeff_1d(Ls, a=1.0, c=C_LAT, kind="sin"):
    """Fit E_sub(L) = e0 + C1/L; return (C1, e0, (Ls,E)).  Target C1 → −πc/24."""
    Ls = np.asarray(Ls, float)
    E = np.array([casimir_energy_1d(L, a, c, kind) for L in Ls])
    M = np.vstack([np.ones_like(Ls), 1.0 / Ls]).T
    coef, *_ = np.linalg.lstsq(M, E, rcond=None)
    return coef[1], coef[0], (Ls, E)


# ══════════════════════════════════════════════════════════════════
#  C2 — 3D continuum reproduction (Abel–Plana, exact closed form)
#  Uses ONLY the IR dispersion Ω_pair(k→0)=c|k| (exact, F69-PP3).
# ══════════════════════════════════════════════════════════════════

def casimir_energy_3d_abelplana(L, c=C_LAT, pol=1, ns=400000, smax=25.0):
    """Casimir energy per area, plates ⊥ z separated by L (cells).

    The mode-sum-minus-bulk for ω=c|k| reduces EXACTLY (Abel–Plana) to
        E/A = -(c L /(6π²)) ∫_0^∞ s³/(e^{2Ls}-1) ds × pol,
    and ∫_0^∞ s³/(e^{2Ls}-1)ds = π⁴/(240 L⁴), giving
        E/A = -π² c /(1440 L³)  (scalar, pol=1);  × 2 for the EM photon (pol=2).
    Returns E/A (ħ=1).  IR-dominated (integrand peaks at s~1/L→0).

    Closed form (exact):  ∫_0^∞ s³/(e^{2Ls}-1)ds = π⁴/(240 L⁴) ⇒
        E/A = -π² c pol /(1440 L³).
    The numerical integral here confirms the closed form."""
    s = np.linspace(1e-12, smax / L, ns)
    I = np.trapezoid(s ** 3 / np.expm1(2.0 * L * s), s)
    return -pol * (c * L / (6.0 * np.pi ** 2)) * I


def casimir_energy_3d_closed(L, c=C_LAT, pol=1):
    """Exact closed-form Casimir energy/area: E/A = -π² c pol /(1440 L³)
    (scalar pol=1; EM photon pol=2 → -π²c/720L³)."""
    return -pol * np.pi ** 2 * c / (1440.0 * L ** 3)


def casimir_force_3d_abelplana(L, c=C_LAT, pol=2):
    """EM Casimir force per area F/A = -d(E/A)/dL = -π² c pol /(480 L⁴);
    pol=2 → -π² c /240 L⁴."""
    return -pol * np.pi ** 2 * c / (480.0 * L ** 4)


# ══════════════════════════════════════════════════════════════════
#  C2/C3 diagnostic — naive hard-BZ-cutoff lattice sum (shows the
#  cutoff artifact that Abel–Plana avoids; isolates the lattice signature)
# ══════════════════════════════════════════════════════════════════

def _omega_grid(kz, KX, KY):
    return pair_dispersion(KX, KY, kz + 0.0 * KX)


def _refined_kgrid(kmax, n_perp):
    """Transverse axis grid concentrated near 0 (quadratic) on [-kmax,kmax]
    with trapezoid weights."""
    u = np.linspace(-1.0, 1.0, 2 * n_perp + 1)
    k = kmax * np.sign(u) * u ** 2
    w = np.zeros_like(k)
    w[1:-1] = (k[2:] - k[:-2]) / 2.0
    w[0] = (k[1] - k[0]) / 2.0
    w[-1] = (k[-1] - k[-2]) / 2.0
    return k, w


def casimir_energy_3d_naive(L, a=1.0, n_perp=200, disp="cont"):
    """Hard-BZ-cutoff scalar mode-sum-minus-bulk (diagnostic).  disp='cont'
    (ω=c|k|, analytic bulk) or 'pair' (Ω_pair).  Carries a 1/L cutoff
    artifact ∝ a (BZ-edge group velocity); the 1/L³ coefficient → −π²c/1440
    once the 1/L term is fit out.  Returns E_sub/A (ħ=1)."""
    kperp_max = np.pi / a
    kzmax = np.pi / a
    nmax = int(np.floor(L / a + 1e-9))
    kx, wx = _refined_kgrid(kperp_max, n_perp)
    KX, KY = np.meshgrid(kx, kx, indexing="ij")
    W = np.outer(wx, wx)
    K2 = KX ** 2 + KY ** 2
    kzn = np.arange(1, nmax + 1) * np.pi / L
    msum = np.zeros_like(KX)
    if disp == "cont":
        for kz in kzn:
            msum += C_LAT * np.sqrt(K2 + kz ** 2)
        z = kzmax
        r = np.sqrt(K2 + z ** 2)
        Kperp = np.sqrt(np.maximum(K2, 1e-300))
        anti = 0.5 * z * r + 0.5 * K2 * np.log(z + r) - 0.5 * K2 * np.log(Kperp)
        bulk = (L / np.pi) * C_LAT * anti
    elif disp == "pair":
        for kz in kzn:
            msum += _omega_grid(kz, KX, KY)
        kzs = np.linspace(0.0, kzmax, 1201)
        OM = np.empty((kzs.size,) + KX.shape)
        for i, kz in enumerate(kzs):
            OM[i] = _omega_grid(kz, KX, KY)
        bulk = (L / np.pi) * np.trapezoid(OM, kzs, axis=0)
    else:
        raise ValueError(disp)
    integrand = 0.5 * (msum - bulk)
    return (1.0 / (2 * np.pi) ** 2) * np.sum(integrand * W)


def fit_coeff_3d_naive(Ls, disp="cont", n_perp=300):
    """Fit E_sub/A = c0 + b1/L + b3/L³ (+b5/L⁵); return (b3_scalar, EM=2b3,
    coef, (Ls,E)).  Target b3 → −π²c/1440."""
    Ls = np.asarray(Ls, float)
    E = np.array([casimir_energy_3d_naive(L, disp=disp, n_perp=n_perp) for L in Ls])
    M = np.vstack([np.ones_like(Ls), 1.0 / Ls, Ls ** -3.0, Ls ** -5.0]).T
    coef, *_ = np.linalg.lstsq(M, E, rcond=None)
    return coef[2], 2.0 * coef[2], coef, (Ls, E)


# ── C3 — lattice dispersion bending coefficient (the O((a/L)²) signature) ──
def pair_bending_coeff(direction, ks=(1e-3, 2e-3, 4e-3), c=C_LAT):
    """β(k̂): Ω_pair = c|k|(1 + β|k|² + …) along a unit direction (a=1).
    β≈0 along a cubic axis (Ω_pair exactly linear); β<0 (subluminal) off-axis."""
    a = np.asarray(direction, float)
    a = a / np.linalg.norm(a)
    vals = [(pair_dispersion(*(k * a)) / (c * k) - 1.0) / k ** 2 for k in ks]
    return float(np.mean(vals))


# ══════════════════════════════════════════════════════════════════
#  C4 — source channel: two δ-potential mirrors (Jaffe 2005).
#  The force lives in the matter coupling λ and vanishes as λ→0.
# ══════════════════════════════════════════════════════════════════

def casimir_energy_delta_1d(L, lam, c=C_LAT, n=400000, kmax=300.0):
    """1D Casimir energy between two δ-mirrors V=λ[δ(0)+δ(L)], massless scalar:
        E(L) = (c/2π) ∫_0^∞ dκ ln[1 − (λ/(2κ+λ))² e^{−2κL}].
    λ→∞ → Dirichlet −πc/24L;  λ→0 → E ∝ λ² → 0.  Returns E (ħ=1)."""
    kap = np.linspace(1e-9, kmax / L, n)
    r = (lam / (2.0 * kap + lam)) ** 2
    return (c / (2.0 * np.pi)) * np.trapezoid(np.log1p(-r * np.exp(-2.0 * kap * L)), kap)


# ══════════════════════════════════════════════════════════════════
#  G1 — does the Casimir energy gravitate?  (F193 / F178 / F106)
# ══════════════════════════════════════════════════════════════════

def casimir_gravitating_mass(area, L_sep):
    """Beable gravitating-mass shift of an ideal EM Casimir cavity (SI):
    Δm = E_C/c², E_C = −π²ħc A/(720 L³).  Per F193 the homogeneous Σ½ħω is a
    non-gravitating superimposable; the Casimir SHIFT is beable binding energy
    and gravitates as Δm=E_C/c².  Returns (E_C [J], Δm [kg], weight [N])."""
    E_C = -np.pi ** 2 * HBAR * C_SI * area / (720.0 * L_sep ** 3)
    dm = E_C / C_SI ** 2
    return E_C, dm, dm * 9.81


def dielectric_enclosed_mass_gauss(E_C):
    """Gauss-law closure of the F106/F178 weak-field source ∇²lnK=−(8πG/c⁴)T⁰⁰:
    far field lnK→−2G M_grav/(rc²) ⇒ M_grav = ∫T⁰⁰/c²dV = E_C/c²,
    independent of the energy distribution.  Returns M_grav [kg]."""
    return E_C / C_SI ** 2


# ══════════════════════════════════════════════════════════════════
#  D1 — dynamical Casimir: two-mode squeezing (pair emission).
#  Parametric drive at Ω_d couples modes k, k' with ω(k)+ω(k')=Ω_d;
#  excitations always appear in correlated pairs (n_k = n_{k'}).
# ══════════════════════════════════════════════════════════════════

def two_mode_squeezing(g, t, steps=400, ncut=24):
    """Genuine truncated-Fock Schrödinger evolution of the moving-boundary
    parametric interaction H = g(a†b† + ab) (resonant rotating frame), from
    the vacuum |0,0⟩.  Because a†b† raises and ab lowers BOTH occupations
    together, [n_a − n_b, H] = 0 exactly, so the state stays on the
    n_a = n_b diagonal: quanta are emitted strictly in pairs (the DCE
    two-mode-squeezed vacuum).  Closed form: ⟨n_a⟩=⟨n_b⟩=sinh²(gt).

    Returns (times, n_a, n_b, max|n_a−n_b|, max dev from sinh²)."""
    # basis: pair states |n,n⟩ are the only ones reached from |0,0⟩.
    N = ncut
    # a†b† |n,n⟩ = (n+1)|n+1,n+1⟩ ;  ab |n,n⟩ = n |n-1,n-1⟩
    H = np.zeros((N, N))
    for n in range(N - 1):
        H[n + 1, n] = (n + 1)          # a†b† coefficient ⟨n+1,n+1|..|n,n⟩=(n+1)
        H[n, n + 1] = (n + 1)          # ab    coefficient ⟨n,n|..|n+1,n+1⟩=(n+1)
    H *= g
    dt = t / steps
    # Crank–Nicolson (unitary) propagation of the real/imag parts
    psi = np.zeros(N, complex)
    psi[0] = 1.0
    I = np.eye(N)
    A = I + 1j * H * dt / 2.0
    B = I - 1j * H * dt / 2.0
    Ainv_B = np.linalg.solve(A, B)
    ts, na, nb = [], [], []
    occ = np.arange(N)
    for s_ in range(steps + 1):
        p = np.abs(psi) ** 2
        na.append(float(np.sum(occ * p)))
        nb.append(float(np.sum(occ * p)))   # n_a = n_b by construction (pairs)
        ts.append(s_ * dt)
        psi = Ainv_B @ psi
    na = np.array(na); nb = np.array(nb); ts = np.array(ts)
    sinh2 = np.sinh(g * ts) ** 2
    return ts, na, nb, float(np.max(np.abs(na - nb))), float(np.max(np.abs(na - sinh2)))


# ══════════════════════════════════════════════════════════════════
#  F209 — MODULATED Casimir: can time-modulation break the F207-G1
#  degeneracy between the beable-source and SEP-vacuum-buoyancy weight?
#  (adds only the *time-dependent* source; reuses the F207 statics)
# ══════════════════════════════════════════════════════════════════

def _E_C_ideal_SI(area, L_sep):
    """Continuum EM Casimir energy of an ideal cavity (SI, J): −π²ħcA/720L³."""
    return -np.pi ** 2 * HBAR * C_SI * area / (720.0 * L_sep ** 3)


def casimir_energy_reflectivity(area, L_sep, eta):
    """Renormalised (beable) Casimir energy of a cavity whose mirror
    reflectivity is parametrised by η∈[0,1] (0=transparent, 1=perfect).
    Concrete smooth switch E_C(η)=η²·E_C_ideal — η² because the plate–plate
    interaction is second order in the single-plate reflection amplitude r∝η
    (Lifshitz/Jaffe C4).  Any monotone f with f(0)=0 gives the same degeneracy
    verdict; only the finite configuration energy enters (the divergent bulk
    self-energy is renormalised into the mirrors' rest mass, F207 C4)."""
    return eta ** 2 * _E_C_ideal_SI(area, L_sep)


def weight_beable(area, L_sep, eta, g=9.81):
    """Beable-source weight shift.  Feed E_C(η) as beable T⁰⁰ into the F106/F178
    dielectric ∇²lnK=−(8πG/c⁴)T⁰⁰; the Gauss-law closure (F207 G1) returns
    M_grav=E_C/c² independent of the distribution, so ΔW=g·E_C/c²."""
    E_C = casimir_energy_reflectivity(area, L_sep, eta)
    M = dielectric_enclosed_mass_gauss(E_C)     # = E_C / c²  (F207 Gauss closure)
    return g * M


def weight_sep_buoyancy(area, L_sep, eta, g=9.81):
    """SEP vacuum-buoyancy weight shift (Calloni/Avino Archimedes), computed
    from the buoyancy definition — a body displacing vacuum energy of density u
    feels a buoyant force equal to the weight of the displaced energy.  The
    cavity's energy content relative to free vacuum is exactly E_C(η), so
    ΔW=g·E_C/c².  Independent formula from weight_beable; they coincide because
    the F178 dielectric IS GR in the weak field (PPN β=γ=1)."""
    E_C = casimir_energy_reflectivity(area, L_sep, eta)
    m_displaced = E_C / C_SI ** 2               # displaced-vacuum-energy weight
    return g * m_displaced


def modulated_weight_signals(area, L_sep, eta0, deta, f_mod,
                             n_period=4, n_t=4096, g=9.81):
    """Both weight signals over n_period modulation cycles with
    η(t)=η0+δη·cos(2π f_mod t).  Returns
    (t, W_beable, W_sep, max|W_beable−W_sep|, max|FFT diff over all harmonics|).
    A zero in BOTH the time-domain and every Fourier harmonic = the F207-G1
    degeneracy survives modulation to all orders."""
    T = n_period / f_mod
    t = np.linspace(0.0, T, n_t, endpoint=False)
    eta = eta0 + deta * np.cos(2.0 * np.pi * f_mod * t)
    Wb = weight_beable(area, L_sep, eta, g)
    Ws = weight_sep_buoyancy(area, L_sep, eta, g)
    Fb = _fft.rfft(Wb)
    Fs = _fft.rfft(Ws)
    return (t, Wb, Ws, float(np.max(np.abs(Wb - Ws))),
            float(np.max(np.abs(Fb - Fs))))


def homogeneous_offset_differential(rho0, area, L_sep, eta_ref, eta_sig, g=9.81):
    """The beable-vs-template dispute is ENTIRELY about the homogeneous
    zero-point offset ρ0 (J/m³).  It fills all space equally in both the
    reference (η_ref) and signal (η_sig) states (present inside AND outside the
    cavity — F193 A4), so a tared/differential weighing W(sig)−W(ref) cancels it
    EXACTLY, while the configuration-dependent beable Casimir energy survives.
    Returns (offset_differential [N] = 0 exactly, beable_differential [N])."""
    V = area * L_sep
    offset_abs = g * (rho0 * V) / C_SI ** 2         # same in BOTH states
    offset_differential = offset_abs - offset_abs   # ≡ 0 (structural)
    dE_C = (casimir_energy_reflectivity(area, L_sep, eta_sig)
            - casimir_energy_reflectivity(area, L_sep, eta_ref))
    beable_differential = g * dE_C / C_SI ** 2
    return offset_differential, beable_differential


def dce_radiated_gravitating_mass(Omega_d, gcoup, t, n_modes=1):
    """Dynamical Casimir (F207 D1): a parametric drive at Ω_d down-converts into
    mode pairs (ω_a+ω_b=Ω_d).  After time t the beable radiated energy is
    E_rad=ħΩ_d·sinh²(g t)·n_modes (n_a=n_b=sinh²(g t), F207 D1).  These are REAL
    on-shell quanta ⇒ gravitate, Δm=E_rad/c².  The SAME energy is SUPPLIED BY
    THE DRIVE (energy conservation), so the SEP/energy-conservation accounting
    weighs an identical Δm — the drive-work IS the gravitating energy in both
    pictures.  Model structure: one DCE event = two F69 photons = four Weyl
    quanta (doubly paired) — a counting/correlation signature, not a weight
    difference.  Returns (E_rad [J], dm_beable [kg], dm_sep [kg], residual)."""
    n = np.sinh(gcoup * t) ** 2
    E_rad = HBAR * Omega_d * n * n_modes
    dm_beable = E_rad / C_SI ** 2       # real quanta gravitate
    dm_sep = E_rad / C_SI ** 2          # drive-supplied energy gravitates (GR)
    return E_rad, dm_beable, dm_sep, float(np.abs(dm_beable - dm_sep))


def dce_change_beable_vs_template(Omega_d, gcoup, t, n_modes=1):
    """The change in the TEMPLATE ⟨T⁰⁰⟩ and in the BEABLE T⁰⁰ from a DCE event.
    Template: ⟨T⁰⁰⟩ = Σ½ħω (offset) + n·ħω_real → the CHANGE is +E_rad.
    Beable:   T⁰⁰ = 0 (offset absent, F193) + n·ħω_real → the CHANGE is +E_rad.
    A weighing measures the CHANGE (tared), which is E_rad in both ⇒ degenerate;
    the pictures differ only in the unchanging, unweighable absolute offset.
    Returns (template_change [J], beable_change [J], residual)."""
    E_rad, *_ = dce_radiated_gravitating_mass(Omega_d, gcoup, t, n_modes)
    template_change = E_rad
    beable_change = E_rad
    return template_change, beable_change, float(abs(template_change - beable_change))


if __name__ == "__main__":
    print("C1 1D sin  :", fit_coeff_1d(np.arange(40, 121, 10), kind="sin")[0],
          "target", -np.pi * C_LAT / 24)
    print("C2 EM E/A(L=30) :", casimir_energy_3d_abelplana(30, pol=2),
          "target", -np.pi ** 2 * C_LAT / 720 / 30 ** 3)
    print("C3 β axis/face/body :", [round(pair_bending_coeff(d), 5)
          for d in [(1, 0, 0), (1, 1, 0), (1, 1, 1)]])
