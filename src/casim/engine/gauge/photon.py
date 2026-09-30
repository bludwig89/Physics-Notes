"""
ca_photon_pair.py  —  The photon as a bound pair of two spin-½ Weyl quanta
==========================================================================

McPhee's "spinor electrodynamics" picture (notebook pp.5–6): the photon is
NOT a single spin-1 gauge boson, and NOT the helicity↔branch composite bilinear
of `ca_maxwell.py` (which is birefringent and excluded by GRB/AGN polarimetry —
F65/F66/F67).  It is a BOUND PAIR of two spin-½ "fermion-photons" γ_{1/2} that
"behave together like a single boson γ that only occurs as a pair.  They don't
occur separately."  (A Cooper-pair-like, massless, spin-1 bound state.)

The decisive structural difference from the retired composite bilinear
(F67/F68):

  * Composite σ-bilinear (RETIRED as the photon): the two photon helicities
    F^± = E ± iB are assigned to the two BCC chiral branches independently
    (F^+ ↔ Ω^+, F^- ↔ Ω^-).  A generic linear polarization populates both, so
    they split → linear vacuum BIREFRINGENCE (ΔΩ = Ω^+ − Ω^-).  Excluded.

  * Paired photon (THIS module): the photon is the SYMMETRIC (+,−) bound pair.
    Total momentum k is shared, each constituent carrying k/2 — one on the +
    branch, one on the − branch.  The pair phase is the SUM of the constituent
    phases:

        Ω_pair(k) = ω⁺(k/2) + ω⁻(k/2)  ≡  Ω_even(k).

    Because the pair ALWAYS contains both branches symmetrically ("only occurs
    as a pair"), there is no "+only" photon to split off — both helicities of
    the resulting (E,B) field ride the single rate Ω_pair.  NON-birefringent.

This is the physical mechanism behind F68's "identity channel": the U(1) gauge
phase e^{iθ}·I is helicity-blind, and the only (E,B) construction consistent
with it is the helicity-symmetric pair, whose rate is ω⁺(k/2)+ω⁻(k/2).

Massless & luminal: at small k, ω±(k/2) → (1/√3)(k/2)/... so Ω_pair → (1/√3)|k|
(no gap; the binding energy makes the pair rest-massless), giving c = 1/√3
(F26), identical to the constituent light speed.

Propagator: the paired photon's (E,B) evolves by the even-law rotation
R(Ω_pair) — which is exactly `ca_wmu._f26_rotation_step` (already the W/Z law).
So no new propagator is needed; this module names it as THE photon law and
provides the pair construction + verification helpers.

CLAUDE.md: closed-form dispersion + real 2×2 (E,B) rotation only; the spinor
constituents go through the audited ca_bcc Weyl walk.  No np.linalg.eig on
chiral matrices.
"""

import numpy as np
from casim.numerics import fft as _fft
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.engine.lattice.bcc import bcc_dispersion
from casim.engine.gauge.weak_wmu import _f26_rotation_step
from casim.constants import c_lat

ROOT3 = np.sqrt(3.0)

_photon_disp_cache: dict = {}  # shape → (cos_Omega, sin_Omega)


# ----------------------------------------------------------------------
# Pair dispersion  Ω_pair(k) = ω⁺(k/2) + ω⁻(k/2)  (= Ω_even)
# ----------------------------------------------------------------------
def pair_dispersion(kx, ky, kz):
    """Rotation rate per tick of the bound (+,−) photon pair.

    Total momentum k is shared by the two constituents (k/2 each); the pair
    phase is the sum of the two constituent branch phases at k/2.  This is the
    helicity-symmetric (non-birefringent) rate.  Scalars or arrays.
    """
    wp = bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='+')
    wm = bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='-')
    return wp + wm


def pair_birefringence(kx, ky, kz):
    """ΔΩ that the pair does NOT have (would be the split if the photon could
    occur as a single branch).  Returned for diagnostics/contrast only."""
    Op = 2.0 * bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='+')
    Om = 2.0 * bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='-')
    return Op - Om


# ----------------------------------------------------------------------
# The photon propagator: even-law (E,B) rotation at Ω_pair.
# (This IS ca_wmu._f26_rotation_step; named here as the canonical photon law.)
# ----------------------------------------------------------------------
def photon_step_spectral(E, B):
    """One tick of the paired-photon (E,B) evolution on an (3,Lx,Ly,Lz) real
    field.  Rotates the (E,B) pair by R(Ω_pair(k)) per Fourier mode — the
    helicity-symmetric, non-birefringent law.

    Returns (E_new, B_new), real, norm-conserving.
    """
    shape = E.shape[1:]
    # ── Cached even-law dispersion ─────────────────────────────────────────
    if shape not in _photon_disp_cache:
        KX, KY, KZ = make_kgrid_3d(*shape)
        Omega = pair_dispersion(KX, KY, KZ)
        _photon_disp_cache[shape] = (np.cos(Omega), np.sin(Omega))
    cos_O, sin_O = _photon_disp_cache[shape]
    # ── Batched FFT over all 3 polarisation components ─────────────────────
    Ek = _fft.fftn(E, axes=(-3, -2, -1))
    Bk = _fft.fftn(B, axes=(-3, -2, -1))
    E_new = _fft.ifftn(cos_O * Ek + sin_O * Bk, axes=(-3, -2, -1)).real
    B_new = _fft.ifftn(-sin_O * Ek + cos_O * Bk, axes=(-3, -2, -1)).real
    return E_new, B_new


def _pair_omega(shape):
    """Cached Ω_pair(k) grid for a spatial ``shape``."""
    key = ("omega", shape)
    if key not in _photon_disp_cache:
        KX, KY, KZ = make_kgrid_3d(*shape)
        Om = pair_dispersion(KX, KY, KZ)
        Om.setflags(write=False)
        _photon_disp_cache[key] = Om
    return _photon_disp_cache[key]


def _even_rotate(E, B, tau):
    """Rotate the (E,B) pair by ``Ω_pair(k)·tau`` per mode — exactly unitary.

    ``photon_step_spectral`` is this at ``tau = 1``.  Splitting it out is what
    lets the homogeneous part of a dielectric step stay exact.
    """
    Om = _pair_omega(E.shape[1:])
    c, s = np.cos(Om * tau), np.sin(Om * tau)
    Ek = _fft.fftn(E, axes=(-3, -2, -1))
    Bk = _fft.fftn(B, axes=(-3, -2, -1))
    return (_fft.ifftn(c * Ek + s * Bk, axes=(-3, -2, -1)).real,
            _fft.ifftn(-s * Ek + c * Bk, axes=(-3, -2, -1)).real)


def _M_weyl(V, Om, delta):
    """Apply :math:`M=\\tfrac12(\\delta\\,\\Omega + \\Omega\\,\\delta)` to ``V``.

    **Weyl (symmetric) ordering, and it is not a refinement — it is the
    resolution of a genuine ambiguity.**  The classical quantity being promoted
    to an operator is the product :math:`\\delta(x)\\,\\Omega(k)`.  Position and
    momentum do not commute, so "the" operator is not defined until an ordering
    is chosen, and the two obvious choices are not equivalent.

    The asymmetric choice :math:`\\delta\\,\\Omega` is **not self-adjoint**, so
    the generator :math:`\\delta\\Omega J` is not antisymmetric and the evolution
    it produces is **not orthogonal — at any step size**.  Measured: with the
    asymmetric ordering the norm drift *plateaus* at :math:`1.1\\times10^{-5}`
    and stops improving, because sub-stepping reduces the Trotter error but
    cannot remove a non-unitarity that is present in the generator itself.

    The symmetric (Weyl) product is self-adjoint by construction, :math:`J` is
    real antisymmetric with :math:`J^2=-\\mathbb{I}`, so :math:`MJ` is a real
    antisymmetric operator on the doubled :math:`(E,B)` space and its exponential
    is **exactly orthogonal**.  The only residual is then Taylor truncation,
    which converges — measured norm drift falls like :math:`1/n_\\text{sub}^3`,
    reaching :math:`2\\times10^{-10}` at ``n_sub=64``.

    Costs one extra FFT round trip over the asymmetric form.  Worth it: it is
    the difference between an error that converges and one that does not.
    """
    a = delta * _fft.ifftn(Om * _fft.fftn(V, axes=(-3, -2, -1)),
                           axes=(-3, -2, -1)).real
    b = _fft.ifftn(Om * _fft.fftn(delta * V, axes=(-3, -2, -1)),
                   axes=(-3, -2, -1)).real
    return 0.5 * (a + b)


def _dielectric_half(E, B, delta, h):
    """Half-step of the inhomogeneous generator :math:`M J`, to second order.

    :math:`\\Omega(k)` acts in Fourier space (exact, k-resolved) and
    :math:`\\delta(x)` in position space — that non-commutation *is* the
    difficulty, and it is why no single homogeneous FFT can do this.  Lifted
    from ``lattice.curved._half_step_dH``, the audited variable-c construction,
    with two derived corrections (see below and :func:`_M_weyl`).

    **Second order, because :math:`J` makes it free to derive.**  :math:`J`
    commutes with :math:`M` (it acts on the two-component :math:`(E,B)` index,
    :math:`M` on space) and :math:`J^2=-\\mathbb{I}`, so exactly

    .. math:: e^{hMJ} = \\cos(hM)\\,\\mathbb{I} + \\sin(hM)\\,J
              = \\mathbb{I} - \\tfrac{h^2M^2}{2} + hMJ + O(h^3)

    Keeping only :math:`\\mathbb{I}+hMJ` — what the 2-D reference does — leaves
    an :math:`O(h^2)` local error that Strang symmetrisation does **not** cancel,
    so the scheme is globally **first** order: measured convergence exponent
    1.0.  Carrying the :math:`-h^2M^2/2` term restores the second order the
    Strang composition is supposed to deliver: measured exponent **2.00**, and
    the error at ``n_sub=8`` drops from :math:`3.0\\times10^{-2}` to
    :math:`3.7\\times10^{-4}` — a factor of 80.

    Note this is a defect of the 2-D reference as well; see F271.
    """
    Om = _pair_omega(E.shape[1:])
    P_E = _M_weyl(E, Om, delta)
    P_B = _M_weyl(B, Om, delta)
    E_new = E + h * P_B - 0.5 * h * h * _M_weyl(P_E, Om, delta)
    B_new = B - h * P_E - 0.5 * h * h * _M_weyl(P_B, Om, delta)
    return E_new, B_new


def photon_step_dielectric(E, B, K, dt=1.0, n_sub=4):
    """Photon step through the F64 dielectric ``K(x)`` — **k-resolved**, no free
    parameter.

    *Added 2026-08-01 (roadmap P3.6 follow-through, F271). Supersedes the
    eikonal* ``gravity.dielectric_mix_half`` *for the photon channel.*

    **The physics.** For the impedance-matched F64 dielectric ($A=1/K$, $B=K$,
    $AB\\equiv1$) the metric is $ds^2=-A c^2dt^2+B\\,dx^2$, so the local
    coordinate light speed is $c\\sqrt{A/B}=c/K$. F64 states the mechanism as a
    renormalisation of the rotation *rate*, which on the lattice means the
    (E,B) pair turns at

    .. math:: \\Omega_K(x,k) = \\Omega_\\text{pair}(k)\\,/\\,K(x)

    — a rate that is **position-dependent and momentum-dependent at once**, and
    therefore diagonal in neither basis. That is the whole obstruction, and it
    is why the deflection lived only in the F64 fork.

    **The resolution, lifted rather than invented.** Write $s(x)=1/K(x)$ and
    split it about its mean, $s = s_0 + \\delta(x)$:

    * $s_0\\,\\Omega(k)$ — diagonal in $k$, applied as an **exact unitary**
      rotation by $s_0\\Omega(k)\\,dt$;
    * $\\delta(x)\\,\\Omega(k)$ — applied to first order, $\\Omega$ in Fourier
      space and $\\delta$ in position space, symmetrised Strang-wise around the
      exact part and sub-cycled ``n_sub`` times.

    This is exactly the decomposition ``lattice.curved.weyl_step_2d_varc_strang``
    uses for the variable-$c$ Weyl walk — the construction that already
    reproduces Snell's law in this codebase. Nothing new is posited.

    **What it buys over the eikonal.**

    * **No free parameter.** ``dielectric_mix_half`` needed a stated central
      rate $\\omega_0$; here the rate is $\\Omega(k)$, mode by mode.
    * **A uniform dielectric is EXACT.** If $K$ is constant then
      $\\delta\\equiv0$, the perturbation vanishes identically, and the step is
      the exact unitary rotation at $\\Omega(k)/K$ — so the group velocity is
      $c/K$ to machine precision at every $k$. The eikonal cannot do this: it
      would need $\\omega_0=\\Omega(k)$, which is the thing it replaces with a
      number.
    * **The error is controlled, not uncontrolled.** The residual is the Trotter
      error of the split, $O(dt^2\\,|\\nabla K|)$ per tick, falling like
      $1/n_\\text{sub}^2$ — measurable and convergent, where the eikonal's
      $\\omega_0$ error is $O(1)$ and does not converge to anything.

    **Accuracy, measured.** The perturbation half-step uses Weyl-symmetric
    ordering (:func:`_M_weyl`) and is carried to second order
    (:func:`_dielectric_half`); both are *derived*, not tuned. Together:

    ======  ===================  ===================
    n_sub   Trotter error        norm drift
    ======  ===================  ===================
    2       5.7e-03              7.6e-06
    8       3.7e-04              1.2e-07
    32      2.3e-05              1.9e-09
    ======  ===================  ===================

    Convergence exponent **2.00** in the field and **~3** in the norm. Neither
    plateaus; the asymmetric ordering the 2-D reference uses does plateau, at
    1.1e-05, and no amount of sub-stepping removes it.

    **What it does not claim.** The half-step is still a truncated exponential,
    so the step is not unitary to machine precision at finite ``n_sub`` — it is
    *convergently* unitary. A closed form exists (:math:`e^{hMJ}=\\cos(hM)+\\sin(hM)J`
    with :math:`M` self-adjoint) but needs operator functions of a non-diagonal
    :math:`M`; that is the remaining refinement and it is not attempted here.

    ``K ≡ 1`` returns ``photon_step_spectral`` exactly, so an ungravitated run
    is bit-identical.
    """
    K = np.asarray(K, dtype=np.float64)
    s = 1.0 / K
    s0 = float(s.mean())
    delta = s - s0
    if not np.any(delta):                      # uniform dielectric ⇒ exact
        return _even_rotate(E, B, s0 * dt)
    n = max(1, int(n_sub))
    dts = float(dt) / n
    h = 0.5 * dts
    for _ in range(n):
        E, B = _dielectric_half(E, B, delta, h)
        E, B = _even_rotate(E, B, s0 * dts)
        E, B = _dielectric_half(E, B, delta, h)
    return E, B


# ----------------------------------------------------------------------
# Pair construction helper: build the photon (E,B) from a transverse
# polarization, and confirm both helicities ride the single rate Ω_pair.
# ----------------------------------------------------------------------
def build_pair_mode(L, m_index, khat, e1):
    """Plant one real, linearly polarized photon Fourier mode at lattice index
    (m,m,m)·sign(khat-axes): E ∥ e1, B ∥ e2 = k̂×e1, |E|=|B| (a standard
    transverse EM mode — populates both RS helicities F^± = E ± iB).

    The pairing is implicit in the propagator (photon_step_spectral): both
    helicities ride Ω_pair, so this single field is the bound pair.
    Returns (E, B, e1, e2).
    """
    khat = np.asarray(khat, float); khat = khat / np.linalg.norm(khat)
    e1 = np.asarray(e1, float); e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(khat, e1); e2 /= np.linalg.norm(e2)
    Ek = np.zeros((3, L, L, L), complex)
    Bk = np.zeros((3, L, L, L), complex)
    idx = tuple(int(round(m_index)) for _ in range(3))
    cidx = tuple((-int(round(m_index))) % L for _ in range(3))
    for a in range(3):
        Ek[a][idx] = e1[a]; Bk[a][idx] = e2[a]
        Ek[a][cidx] = np.conj(e1[a]); Bk[a][cidx] = np.conj(e2[a])
    E = np.array([_fft.ifftn(Ek[a]).real for a in range(3)])
    B = np.array([_fft.ifftn(Bk[a]).real for a in range(3)])
    return E, B, e1, e2


def group_velocity(nhat, h=1e-5):
    """|dΩ_pair/d|k|| along nhat at small k (the photon's signal speed)."""
    nhat = np.asarray(nhat, float); nhat = nhat / np.linalg.norm(nhat)
    kx, ky, kz = h * nhat
    return float(pair_dispersion(kx, ky, kz) / h)


def group_velocity_at(k0vec, nhat, h=1e-5):
    """dΩ_pair/dk along nhat evaluated AT a finite carrier k0vec (central
    difference).  This is the speed a beam packet centred on k0 travels at —
    at finite k it lies slightly below the k→0 limit 1/√3 (lattice
    dispersion), so the beam tracker compares against this, not c_lat."""
    k0vec = np.asarray(k0vec, float)
    nhat = np.asarray(nhat, float); nhat = nhat / np.linalg.norm(nhat)
    wp = pair_dispersion(*(k0vec + h * nhat))
    wm = pair_dispersion(*(k0vec - h * nhat))
    return float((wp - wm) / (2.0 * h))


# ----------------------------------------------------------------------
# Beam construction: a localized, axis-aligned travelling Gaussian packet.
# (2026-06-06) Added for the photon_beam scenarios — a *moving* beam you can
# track, in contrast to build_pair_mode's single standing Fourier mode.
# ----------------------------------------------------------------------
def build_beam_packet(L, m_index, axis=0, pol_axis=None, sigma=4.0,
                      center=None, polarization="linear"):
    """Build a travelling Gaussian photon beam on an L³ cubic lattice.

    Construction: the RS analytic field F = E + iB is taken one-sided in k,

        f(x) = exp(−|x−x0|² / 2σ²) · exp(i k0 (x_axis − x0_axis)),

    with carrier k0 = 2π·m_index/L along ``axis``.  Under the even pair law
    F_k → e^{−iΩ_pair}F_k, so a one-sided F is a packet travelling in +axis at
    dΩ_pair/dk|_{k0} (the backward −k0 content is suppressed by
    exp(−(k0σ)²); keep k0·σ_axis ≳ 3).

    ``polarization`` selects how the scalar envelope ``f`` is mapped onto the
    RS 3-vector ``F = E + iB``:

    * ``"linear"`` (default) — ``F[pol_axis] = f``, i.e. E and B occupy the
      *same* Cartesian component (``pol_axis``, transverse to ``axis``,
      default ``(axis+1)%3``).  **This is a real (non-null) RS field**:
      ``F·F = f² ≠ 0``, so ``E ∥ B`` pointwise and the Poynting momentum
      ``Σ E×B`` vanishes identically — a real limitation of this mode for any
      momentum-carrying use, not a bug (see ``core.observers.Momentum``'s own
      docstring). Kept as the default, bit-identical to every prior call site,
      because F386–F390's gate records are built on it.
    * ``"circular"`` — the genuine null-RS (radiation) field. With
      ``a1=(axis+1)%3``, ``a2=(axis+2)%3`` and the complex circular
      polarization vector ``ê = (ê_a1 + i·ê_a2)/√2``, set
      ``F_vec = ê·f`` (so ``F·F = f²·(ê·ê) = 0`` exactly, since ê is a null
      complex unit vector), i.e.

          E[a1] = Re(f)/√2,   B[a1] = Im(f)/√2
          E[a2] = −Im(f)/√2,  B[a2] = Re(f)/√2

      giving ``|E|=|B|`` and ``E⊥B`` pointwise (to FFT round-off), a genuine
      nonzero, axis-directed Poynting momentum, and (F·F=0 being propagator-
      invariant under the paired-photon's per-mode rotation, F26/F67-F69)
      exact conservation of ``Σ E×B`` under ``photon_step_spectral``.
      ``pol_axis`` is not used in this mode — the polarization plane is fixed
      by ``axis`` alone.

    ``sigma`` may be a scalar or a length-3 sequence (per-axis widths).  A
    finite transverse width σ⊥ gives the beam an angular spectrum, so its
    axial speed sits below dΩ/dk|k0 by the diffraction deficit ≈ 1/(2(k0σ⊥)²)
    — physical beam optics, vanishing as σ⊥ → ∞.  Along a cubic axis
    Ω_pair(k x̂) = |k|/√3 exactly, so an ideal plane wave is dispersionless.

    Bonus: |F|² = E² + B² is the smooth envelope² (no carrier ripple), so the
    energy-centroid track is clean.

    Returns (E, B, k0vec) with E, B shaped (3, L, L, L).
    """
    axis = int(axis)
    if pol_axis is None:
        pol_axis = (axis + 1) % 3
    pol_axis = int(pol_axis)
    if pol_axis == axis:
        raise ValueError("beam polarization must be transverse (pol_axis != axis)")
    k0 = 2.0 * np.pi * float(m_index) / float(L)
    if center is None:
        center = [L / 4.0 if a == axis else L / 2.0 for a in range(3)]
    sig = np.broadcast_to(np.asarray(sigma, float), (3,))
    x = [np.arange(L, dtype=float) for _ in range(3)]
    X = np.meshgrid(*x, indexing="ij")
    # periodic (minimum-image) displacement from the packet centre
    d = [np.remainder(X[a] - center[a] + L / 2.0, L) - L / 2.0 for a in range(3)]
    r2 = sum((d[a] / sig[a]) ** 2 for a in range(3))
    envelope = np.exp(-r2 / 2.0)
    f = envelope * np.exp(1j * k0 * d[axis])
    E = np.zeros((3, L, L, L))
    B = np.zeros((3, L, L, L))
    if polarization == "linear":
        E[pol_axis] = f.real
        B[pol_axis] = f.imag
    elif polarization == "circular":
        a1, a2 = (axis + 1) % 3, (axis + 2) % 3
        root2 = np.sqrt(2.0)
        E[a1] = f.real / root2
        B[a1] = f.imag / root2
        E[a2] = -f.imag / root2
        B[a2] = f.real / root2
    else:
        raise ValueError("polarization must be 'linear' or 'circular'")
    k0vec = np.zeros(3)
    k0vec[axis] = k0
    return E, B, k0vec


def _field_momentum_k(E, B):
    """``Σ_k E_k × conj(B_k) / N`` — the exact-by-Parseval field momentum
    ``core.observers.Momentum`` uses (its own docstring derives why this,
    not a naive real-space ``Σ_x E×B``, is the bit-identical-conserved
    quantity under ``photon_step_spectral``; the ``/N`` matches that
    observer's own normalisation convention, so this reproduces the
    audit's real-space-summed numbers directly)."""
    n = E[0].size
    Ek = [_fft.fftn(E[a]) for a in range(3)]
    Bk = [_fft.fftn(B[a]) for a in range(3)]
    px = Ek[1] * np.conj(Bk[2]) - Ek[2] * np.conj(Bk[1])
    py = Ek[2] * np.conj(Bk[0]) - Ek[0] * np.conj(Bk[2])
    pz = Ek[0] * np.conj(Bk[1]) - Ek[1] * np.conj(Bk[0])
    return np.array([px.sum(), py.sum(), pz.sum()]).real / n


def check_beam_polarization_fix(L=16, sigma=3.0, m_indices=(2, 4), n_ticks=40,
                                null_check_polarization="circular"):
    """Gate leg for the F386-audit defect (docs/audits/2026-09-16-photon-
    fermion-momentum-investigation.md §2): ``build_beam_packet``'s original
    (``"linear"``) mode has ``E∥B`` pointwise, so ``F=E+iB`` is not a null
    Riemann–Silberstein field and ``Σ E×B≡0`` identically — F390's entire
    momentum-conservation test ran against a field with no momentum to give.
    The ``"circular"`` mode is the fix: a complex circular polarization
    vector makes ``F·F=0`` exactly, i.e. ``|E|=|B|`` and ``E⊥B`` (the null
    condition, references/lattice-conservation-laws-research-review.md §8).

    Any beam a momentum test uses from here on should satisfy this — the
    durable point of this gate leg, not merely a one-off regression check.

    Legs:
        null_condition_holds          |E·B|/(‖E‖‖B‖) < 1e-12, every
                                       axis × m_index combo tested
        equal_magnitude_holds         |‖E‖−‖B‖|/‖E‖ < 1e-12, same combos
        momentum_nonzero_and_aligned  |Σ E×B| > 0 and cos(P,k̂) > 0.99,
                                       same combos
        default_config_magnitude_matches_audit
                                       |Σ E×B| = 75.126 at L=16,σ=3.0,
                                       axis=0, m=2 (the audit's own
                                       reproduced number)
        momentum_conserved_under_free_propagator
                                       rel. drift of the k-space field
                                       momentum under n_ticks of
                                       photon_step_spectral < 5e-15
        linear_mode_bit_identical_to_default
                                       the (unchanged) "linear" mode is
                                       bit-identical whether requested by
                                       omitting `polarization` or passing
                                       it explicitly — the backward-
                                       compatibility contract F386-F391's
                                       own gate records depend on
    """
    checks = {}
    worst_null = 0.0
    worst_mag_diff = 0.0
    worst_cos = 1.0
    any_zero_momentum = False
    for axis in range(3):
        for m in m_indices:
            E, B, k0vec = build_beam_packet(L, m, axis=axis, sigma=sigma,
                                            polarization=null_check_polarization)
            nE, nB = float(np.linalg.norm(E)), float(np.linalg.norm(B))
            null_ratio = abs(float((E * B).sum())) / (nE * nB)
            mag_diff = abs(nE - nB) / nE
            P = _field_momentum_k(E, B)
            nP = float(np.linalg.norm(P))
            khat = k0vec / np.linalg.norm(k0vec)
            cos_pk = float(P @ khat) / nP if nP > 0 else 0.0
            worst_null = max(worst_null, null_ratio)
            worst_mag_diff = max(worst_mag_diff, mag_diff)
            worst_cos = min(worst_cos, cos_pk)
            any_zero_momentum = any_zero_momentum or (nP == 0.0)
    checks["null_condition_holds"] = worst_null < 1e-12
    checks["equal_magnitude_holds"] = worst_mag_diff < 1e-12
    checks["momentum_nonzero_and_aligned"] = (not any_zero_momentum) and worst_cos > 0.99

    E0, B0, _ = build_beam_packet(L, 2, axis=0, sigma=sigma,
                                  polarization=null_check_polarization)
    default_mag = float(np.linalg.norm(_field_momentum_k(E0, B0)))
    checks["default_config_magnitude_matches_audit"] = (
        abs(default_mag - 75.125961) < 1e-2 if L == 16 and sigma == 3.0 else True)

    E, B, _ = build_beam_packet(L, 2, axis=0, sigma=sigma,
                                polarization=null_check_polarization)
    P0 = _field_momentum_k(E, B)
    n0 = float(np.linalg.norm(P0))
    for _ in range(n_ticks):
        E, B = photon_step_spectral(E, B)
    P1 = _field_momentum_k(E, B)
    if n0 > 0:
        drift = float(np.linalg.norm(P1 - P0)) / n0
        checks["momentum_conserved_under_free_propagator"] = drift < 5e-15
    else:
        # nothing to conserve (P0 is exactly zero, the original defect) —
        # a drift ratio is undefined, and there is no baseline to be
        # "conserved" relative to, so this leg cannot pass.
        drift = float("nan")
        checks["momentum_conserved_under_free_propagator"] = False

    E_def, B_def, k_def = build_beam_packet(L, 2, axis=0, sigma=sigma)
    E_exp, B_exp, k_exp = build_beam_packet(L, 2, axis=0, sigma=sigma, polarization="linear")
    checks["linear_mode_bit_identical_to_default"] = (
        np.array_equal(E_def, E_exp) and np.array_equal(B_def, B_exp)
        and np.array_equal(k_def, k_exp))

    n_pass = sum(1 for v in checks.values() if v)
    return {
        "checks": checks,
        "n_pass": n_pass,
        "n_checks": len(checks),
        "ok": n_pass == len(checks),
        "worst_null_condition_ratio": worst_null,
        "worst_magnitude_diff_ratio": worst_mag_diff,
        "worst_cos_P_khat": worst_cos,
        "default_config_momentum_magnitude": default_mag,
        "momentum_drift_40_ticks": drift,
    }


if __name__ == '__main__':
    # quick self-check
    n = np.array([1, 1, 1.]) / ROOT3
    print("Ω_pair(body diag, k=0.3) =", pair_dispersion(*(0.3 * n)))
    print("group velocity → 1/√3 =", group_velocity(n), "vs", c_lat)
