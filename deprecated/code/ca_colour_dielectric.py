# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_colour_dielectric.py
# migrated   : 2026-07-30 - 14:48
# target     : src/casim/engine/gauge/colour_dielectric.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_colour_dielectric.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed (S1/S2 code-clean already applied at F69/F91)
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_colour_dielectric.py — Confinement as a colour-dielectric / dual superconductor  (P1, Option C)
==================================================================================================

Created: 2026-06-03

The binding-force fork the notebook actually gestures at (pp. 5-6, the BCS
thread).  The model's signature is *rotation-rate physics*:

  F26 — c is the rotation rate of the real (E,B) pair, not a phase velocity.
  F64 — gravity is a single, impedance-matched lattice **dielectric** K(x)
        renormalising that (E,B) rotation rule (no rest-mass-sourced metric).
  F46 — mass is rest-leg rotation.

The natural binding-force analogue is the **dual superconductor**: the QCD
vacuum is a colour-**magnetic** condensate that, by the dual Meissner effect,
squeezes colour-**electric** flux between a q-qbar pair into a tube of fixed
energy-per-length sigma -> linear potential V(R)=sigma R -> confinement.

Recast in the model's own language this is a **colour-dielectric** eps_c(x)
that renormalises the F43 gluon (E,B)-rotation rule — exactly parallel to F64's
gravitational dielectric, but in the *opposite regime*:

    F64 gravity dielectric :  eps = mu = K, impedance-matched (AB=1),
                              transparent — bends light, does not expel it.
    Confining dielectric   :  eps_c -> 0 in the condensed vacuum,
                              impedance-BROKEN, **expels** colour-electric flux
                              (dual Meissner) -> squeezes it into the tube.

Both are one position-dependent renormalisation of the same rotation rule; the
sign of the impedance mismatch is what separates "bend" from "confine".  This
is the unification the roadmap (Option C) asks for: one mechanism — dielectric
rotation-rule renormalisation — underlies both gravity (F64) and confinement.

------------------------------------------------------------------------------
Layout
------------------------------------------------------------------------------
Part A — Dual-superconductor flux tube (the mechanism).
    Abelian-Higgs / dual-Ginzburg-Landau (ANO) vortex in the transverse plane.
    Exact BPS string tension  sigma = 2 pi v^2 n  at critical coupling (kappa=1),
    pure-numpy RK4 shooting for the profile (no scipy), flux quantisation.

Part B — Colour-dielectric renormalisation of the F43 gluon rotation rule.
    eps_c(x) from the condensate; a renormalised gluon rotation step that
    reduces to `ca_gluon.gluon_rotation_step_spectral_2d` bit-for-bit when
    eps_c == 1 everywhere, and rescales the rotation rate (hence c) otherwise.

Part C — Dual Meissner / London screening + linear potential.
    Screened (dual-London) colour-electric field, penetration depth
    lambda = 1/(e v); constant tube cross-section -> V(R) = sigma R linear.

Conventions
-----------
  phi          dual monopole condensate, |phi| -> v in the vacuum.
  f(x)         normalised condensate profile, f = |phi|/v, f(0)=0, f(inf)=1.
  a(x)         dimensionless gauge profile, a(0)=0, a(inf)=1.
  x = e v r    dimensionless radius in vector-mass (m_V = e v) units.
  kappa^2 = 2 lambda / e^2   Ginzburg-Landau parameter; kappa=1 is the BPS /
            type-I|II boundary where the tension is exactly topological.
  n            winding (units of quantised colour-electric flux).

References:  F43 (dynamical gluons + Wilson primitives), F64 (gravity
dielectric — the structural template), F70 (2D-exact area-law sigma — the
complementary strong-coupling anchor), F26 (rotation = c).
"""

import numpy as np

import ca_gluon as cg
import ca_wmu as cwmu                  # BCC even dispersion + k-grid (Part D)
import ca_colour_condensate as cc      # the gap / condensate source (Part D)
import ca_maxwell_2d as cm2            # 2D rotation dispersion (Part D)
from casim.constants import c_lat as C_LAT_REGISTRY
import ca_fft as _fft  # roadmap C1.3: route FFTs through casim.numerics


# ══════════════════════════════════════════════════════════════════
#  Part A — Dual-superconductor (ANO / dual-Ginzburg-Landau) flux tube
# ══════════════════════════════════════════════════════════════════
#
#  Energy per unit length of the Abelian-Higgs vortex (transverse plane),
#  dimensionless radius x = e v r, at the *critical (BPS) coupling*:
#
#    sigma = 2 pi v^2  ∫_0^∞ x dx [ f_x^2
#                                   + n^2 f^2 (1-a)^2 / x^2
#                                   + (n^2 / (2 x^2)) a_x^2
#                                   + (1/2) (f^2 - 1)^2 ]
#
#  At the BPS point the energy density completes to a sum of two squares plus
#  a total derivative, and the squares vanish on solutions of the *first-order*
#  Bogomolny equations
#    f_x = n f (1-a) / x ,    a_x = (x/n) (1 - f^2) ,
#  so the tension is the profile-independent topological value
#    sigma = 2 pi v^2 * n [ (1-a)(f^2-1) ]_0^∞ = 2 pi v^2 n      (exact).
#  (The boundary term evaluates to +1: a,f: 0->1.)  These first-order equations
#  also satisfy the second-order EL equations at the critical coupling.


def bps_string_tension(v=1.0, n=1):
    """Exact BPS (kappa=1) flux-tube tension  sigma = 2 pi v^2 |n|  (Tier 1)."""
    return 2.0 * np.pi * v ** 2 * abs(n)


def penetration_depth(e=1.0, v=1.0):
    """Dual-London penetration depth  lambda = 1/(e v) = 1/m_V.

    The dual photon acquires mass m_V = e v in the condensate, so the
    colour-electric field is screened over lambda — the dual Meissner length
    that sets the tube radius.
    """
    return 1.0 / (e * v)


def coherence_length(e=1.0, v=1.0, kappa=1.0):
    """Condensate coherence length  xi = 1/m_S = 1/(kappa e v).

    kappa = lambda_pen-ratio = m_S/m_V.  kappa<1 type-I, kappa>1 type-II,
    kappa=1 BPS (the tension is exactly topological).
    """
    m_S = kappa * e * v
    return 1.0 / m_S


# ---- pure-numpy RK4 shooting for the BPS profile --------------------

def _bps_rhs(x, f, a, n):
    """First-order Bogomolny RHS (kappa=1):  f_x = n f (1-a)/x,  a_x = (x/n)(1-f^2)."""
    fx = n * f * (1.0 - a) / x
    ax = (x / n) * (1.0 - f * f)
    return fx, ax


def _integrate_bps(c, n, x0=1e-4, x_max=14.0, dx=2e-3):
    """RK4-integrate the BPS equations from x0 with seed f(x0)=c*x0^n.

    Near x->0 the regular solution behaves as  f ~ c x^n,  a ~ x^2/(2n).
    Returns arrays (xs, fs, as_).  `c` is the shooting parameter fixed by the
    boundary condition f(inf)=1.
    """
    nx = int(round((x_max - x0) / dx))
    xs = np.empty(nx + 1)
    fs = np.empty(nx + 1)
    as_ = np.empty(nx + 1)
    x = x0
    f = c * x0 ** n
    a = x0 ** 2 / (2.0 * n)
    xs[0], fs[0], as_[0] = x, f, a
    for i in range(nx):
        k1f, k1a = _bps_rhs(x, f, a, n)
        k2f, k2a = _bps_rhs(x + dx / 2, f + dx / 2 * k1f, a + dx / 2 * k1a, n)
        k3f, k3a = _bps_rhs(x + dx / 2, f + dx / 2 * k2f, a + dx / 2 * k2a, n)
        k4f, k4a = _bps_rhs(x + dx, f + dx * k3f, a + dx * k3a, n)
        f = f + dx / 6 * (k1f + 2 * k2f + 2 * k3f + k4f)
        a = a + dx / 6 * (k1a + 2 * k2a + 2 * k3a + k4a)
        x = x + dx
        xs[i + 1], fs[i + 1], as_[i + 1] = x, f, a
        # divergence guard for the shooting bracket
        if not np.isfinite(f) or abs(f) > 10.0:
            return xs[:i + 2], fs[:i + 2], as_[:i + 2]
    return xs, fs, as_


def solve_bps_profile(n=1, x_max=14.0, dx=2e-3, tol=1e-12, max_iter=200):
    """
    Solve the BPS (kappa=1) ANO vortex profile by pure-numpy RK4 shooting.

    The regular solution near the origin is  f ~ c x^n,  a ~ x^2/(2n).  The
    seed slope c is a separatrix parameter:

        c too SMALL -> f rises then collapses back to 0   (a runs away to +inf)
        c too LARGE -> f overshoots 1 and diverges
        c = c*      -> f -> 1, a -> 1   (the BPS vortex)

    We bisect on that separatrix: a trajectory that diverges is above c*
    (hi = c), anything else is below (lo = c).  Pushing c up to the edge of
    divergence lands on the vortex from below.  Returns xs, f, a, c.

    No scipy: deliberate, per project practice (hand-rolled numerics on the
    delicate transforms).
    """
    DIVERGED = 1.02          # f beyond this -> overshoot/divergence branch
    lo, hi = 0.0, 5.0
    for _ in range(max_iter):
        c = 0.5 * (lo + hi)
        xs, fs, as_ = _integrate_bps(c, n, x_max=x_max, dx=dx)
        diverged = (xs[-1] < x_max - dx) or (np.max(fs) > DIVERGED)
        if diverged:
            hi = c               # above the separatrix -> reduce c
        else:
            lo = c               # below (collapse or marginal) -> raise c
        if hi - lo < tol:
            break
    c = lo                       # last known non-divergent seed
    xs, fs, as_ = _integrate_bps(c, n, x_max=x_max, dx=dx)
    # The separatrix solution rises monotonically to f=1, a=1; just off c* it
    # then peels away.  The physical vortex is the clean rising segment, so
    # truncate at the first crossing f>=1 (where a has also reached ~1).  The
    # truncated tail is f=a=1 with vanishing energy density — it contributes
    # nothing to the BCs or the tension integral.
    above = np.where(fs >= 1.0)[0]
    i_end = int(above[0]) if above.size else int(np.argmax(fs))
    xs, fs, as_ = xs[:i_end + 1], fs[:i_end + 1], as_[:i_end + 1]
    return {'x': xs, 'f': fs, 'a': as_, 'c': c, 'n': n, 'kappa': 1.0}


def string_tension_numeric(profile, v=1.0):
    """
    Numerically integrate the energy functional on a BPS profile.

    sigma/(2 pi v^2) = ∫ x dx [ f_x^2 + n^2 f^2 (1-a)^2/x^2
                                + (n^2/(2 x^2)) a_x^2 + (1/4)(f^2-1)^2 ]

    For a BPS solution this equals n exactly (topological); the numeric value
    is the ODE/quadrature check on `bps_string_tension`.
    """
    x = profile['x']
    f = profile['f']
    a = profile['a']
    n = profile['n']
    fx = np.gradient(f, x)
    ax = np.gradient(a, x)
    dens = (fx ** 2
            + n ** 2 * f ** 2 * (1.0 - a) ** 2 / x ** 2
            + (n ** 2 / (2.0 * x ** 2)) * ax ** 2
            + 0.5 * (f ** 2 - 1.0) ** 2)        # critical-coupling potential
    integ = np.trapz(x * dens, x)
    return 2.0 * np.pi * v ** 2 * integ


def colour_electric_flux(profile, e=1.0):
    """
    Total quantised colour-electric flux  Phi = ∫ B d^2x = 2 pi n / e.

    B(x) = (n/(e r)) a_x  with x = e v r; in dimensionless form the flux is
    Phi = (2 pi n / e) * a(x_max)  -> 2 pi n / e as a(inf)->1.  Returns the
    numerically integrated flux (units 1/e).
    """
    n = profile['n']
    a_inf = profile['a'][-1]
    return 2.0 * np.pi * n * a_inf / e


# ══════════════════════════════════════════════════════════════════
#  Part B — Colour-dielectric renormalisation of the F43 gluon rotation rule
# ══════════════════════════════════════════════════════════════════
#
#  The dual superconductor IS a colour-dielectric: eps_c -> 0 in the condensed
#  vacuum (colour-electric flux expelled) and eps_c -> 1 in the normal tube
#  core.  Mapping the condensate profile f = |phi|/v to a dielectric:
#
#       eps_c(x) = 1 - f(x)^2      (core f=0 -> eps_c=1; vacuum f=1 -> eps_c=0)
#
#  This is the colour analogue of F64's gravitational index K(x): a
#  position-dependent renormalisation of the (E,B) rotation rate.  The local
#  refractive factor is  n_c = eps_c^{-1/2}  (the impedance form, parallel to
#  F64's K), so the gluon rotation rate / lattice c is rescaled  c -> c / n_c.
#  In the confining limit eps_c -> 0, n_c -> inf, the rotation freezes: the
#  colour field cannot rotate (propagate) into the condensed vacuum — confined.


def colour_dielectric_from_condensate(f):
    """eps_c = 1 - f^2 from a normalised condensate profile f = |phi|/v in [0,1].

    f=0 (tube core, normal phase)  -> eps_c = 1 (free propagation)
    f=1 (condensed vacuum)         -> eps_c = 0 (colour-electric flux expelled)
    """
    f = np.asarray(f, dtype=float)
    return 1.0 - f ** 2


def refractive_factor(eps_c, floor=1e-12):
    """n_c = eps_c^{-1/2}  (impedance form, F64 parallel).  eps_c->0 => n_c->inf."""
    eps_c = np.maximum(np.asarray(eps_c, dtype=float), floor)
    return eps_c ** (-0.5)


def gluon_dielectric_rotation_step_2d(E_G, B_G, eps_c=None):
    """
    One tick of the F43 gluon (E,B) rotation rule renormalised by a *uniform*
    colour-dielectric eps_c.

    The rotation angle Omega(k) of the free F43 step is rescaled by the local
    refractive factor:  Omega -> Omega / n_c  with  n_c = eps_c^{-1/2}.  This
    is the colour analogue of F64's dielectric renormalisation of the EM
    rotation rule.

    Parameters
    ----------
    E_G, B_G : (8, Lx, Ly) real colour-octet fields.
    eps_c    : float (uniform colour permittivity) or None.
               None or 1.0 -> reduces to `ca_gluon.gluon_rotation_step_spectral_2d`
               BIT-FOR-BIT (the F64-parallel invariant: trivial dielectric = free
               rule).

    Returns
    -------
    E_new, B_new : (8, Lx, Ly) real.

    Notes
    -----
    A *uniform* eps_c keeps the step spectral and exactly unitary while still
    demonstrating the rotation-rate (hence c) renormalisation.  The spatially
    varying, flux-expelling case is the dual-Meissner mechanism handled
    analytically in Part A / Part C (the DGL profile), not by a single
    spectral tick.
    """
    if eps_c is None or eps_c == 1.0:
        return cg.gluon_rotation_step_spectral_2d(E_G, B_G)

    n_c = float(eps_c) ** (-0.5)
    if E_G.shape[0] != 8 or B_G.shape[0] != 8:
        raise ValueError("E_G, B_G must have first axis size 8 (SU(3) octet)")

    import ca_maxwell_2d as cm2
    Lx, Ly = E_G.shape[1], E_G.shape[2]
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    Omega = cm2.rotation_omega_2d(KX, KY) / n_c      # <-- dielectric rescaling
    cosO = np.cos(Omega)
    sinO = np.sin(Omega)
    E_new = np.zeros_like(E_G)
    B_new = np.zeros_like(B_G)
    for a in range(8):
        Ek = _fft.fft2(E_G[a])
        Bk = _fft.fft2(B_G[a])
        E_new[a] = _fft.ifft2(cosO * Ek + sinO * Bk).real
        B_new[a] = _fft.ifft2(-sinO * Ek + cosO * Bk).real
    return E_new, B_new


def effective_lattice_c(eps_c):
    """Renormalised lattice light/colour speed  c_eff = c_lat / n_c = c_lat * sqrt(eps_c).

    c_lat = 1/sqrt(3) is the model's luminal rate (CLAUDE.md decision 5).  In a
    colour-dielectric the gluon rotation rate scales the same way the EM rate
    does under F64.
    """
    c_lat = C_LAT_REGISTRY
    return c_lat * np.sqrt(np.asarray(eps_c, dtype=float))


# ══════════════════════════════════════════════════════════════════
#  Part C — Dual Meissner / London screening + linear static potential
# ══════════════════════════════════════════════════════════════════


def london_screened_field_2d(L=64, m=0.5, src_sep=None, seed=0):
    """
    Solve the dual-London (screened-Poisson / Helmholtz) equation for the
    colour-electric field of a static q-qbar pair in the condensate:

        (-∇^2 + m^2) E(x) = rho(x) ,        m = e v = 1/lambda_pen .

    In the condensed vacuum the dual photon is massive, so the colour-electric
    field is screened over lambda = 1/m — the dual Meissner effect.  Solved
    spectrally on an L×L periodic lattice (pure numpy FFT).

    Returns dict with the field E (L,L) and the lattice geometry, for the
    penetration-depth fit in the test battery.
    """
    rho = np.zeros((L, L))
    c0 = L // 2
    if src_sep is None:
        rho[c0, c0] = 1.0                       # single static source
    else:
        rho[c0, (c0 - src_sep // 2) % L] += 1.0
        rho[c0, (c0 + src_sep // 2) % L] -= 1.0  # q and qbar
    kx = np.fft.fftfreq(L) * 2.0 * np.pi
    ky = np.fft.fftfreq(L) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k2 = (2.0 - 2.0 * np.cos(KX)) + (2.0 - 2.0 * np.cos(KY))   # lattice -∇^2
    denom = k2 + m ** 2
    E = _fft.ifft2(_fft.fft2(rho) / denom).real
    return {'E': E, 'L': L, 'm': m, 'center': c0}


def fit_penetration_depth(screen, r_min=3, r_max=14):
    """
    Fit lambda from the large-r decay of a single-source London field.

    In 2D the screened Green's function of (-∇^2 + m^2) is the modified Bessel
    function  E(r) = (1/2 pi) K_0(m r) ~ sqrt(pi/(2 m r)) exp(-m r), so a *pure*
    exponential fit is biased by the 1/sqrt(r) prefactor.  We remove it by
    fitting  ln( |E| * sqrt(r) )  vs r, whose slope is exactly -1/lambda = -m.

    Returns (lambda_fit, expected = 1/m).
    """
    E = screen['E']
    c0 = screen['center']
    rs = np.arange(r_min, r_max)
    vals = np.array([abs(E[c0, (c0 + r) % screen['L']]) for r in rs])
    good = vals > 0
    rs, vals = rs[good], vals[good]
    y = np.log(vals * np.sqrt(rs))               # K_0 prefactor removed
    A = np.vstack([rs, np.ones_like(rs, dtype=float)]).T
    slope, _ = np.linalg.lstsq(A, y, rcond=None)[0]
    lam_fit = -1.0 / slope
    return lam_fit, 1.0 / screen['m']


def linear_potential(R, sigma, mu=0.0):
    """Static q-qbar potential from a constant-cross-section flux tube:
    V(R) = sigma R + mu.  Linear because the tube energy/length is fixed."""
    return sigma * np.asarray(R, dtype=float) + mu


def tube_energy_vs_length(profile, lengths, v=1.0):
    """
    Total flux-tube energy E(R) = sigma * R for a z-independent tube built from
    the (R-independent) transverse DGL profile.

    Returns (E_array, sigma) where sigma = string_tension_numeric(profile).
    The point of confinement: E grows *linearly* and without bound in R, so an
    isolated colour charge (R->inf) costs infinite energy.
    """
    sigma = string_tension_numeric(profile, v=v)
    return sigma * np.asarray(lengths, dtype=float), sigma


def tube_rms_radius(profile):
    """
    Transverse RMS radius of the flux-tube energy density (in m_V^{-1} units).

    Constant across tube length R (the DGL solution is z-independent), which is
    exactly why V(R) is linear: a fixed cross-section means fixed energy/length.
    """
    x = profile['x']
    f = profile['f']
    a = profile['a']
    n = profile['n']
    fx = np.gradient(f, x)
    ax = np.gradient(a, x)
    dens = (fx ** 2
            + n ** 2 * f ** 2 * (1.0 - a) ** 2 / x ** 2
            + (n ** 2 / (2.0 * x ** 2)) * ax ** 2
            + 0.5 * (f ** 2 - 1.0) ** 2)        # critical-coupling potential
    w = x * dens                      # radial weight (2D measure)
    r2 = np.trapz(x ** 2 * w, x) / np.trapz(w, x)
    return np.sqrt(r2)


# ══════════════════════════════════════════════════════════════════
#  Part D — time-evolved gluon propagator: dielectric renorm + gap coupling
# ══════════════════════════════════════════════════════════════════
#  Created: 2026-06-08
#
#  Parts B/C above are single-tick (uniform) and static-field constructions.
#  Part D wires the colour-dielectric *into the time-evolved gluon propagator*
#  and *couples the condensate gap* (ca_colour_condensate, F88) to the
#  dynamical gluon field, so that one measured number — the condensate VEV v —
#  simultaneously sets:
#     (1) the dielectric eps_c(x) that renormalises the (E,B) rotation rate,
#     (2) the dual-Meissner mass m_V = e v the gluon acquires in the vacuum,
#     (3) the screening length lambda = 1/m_V and the tension sigma = 2 pi v^2.
#
#  D-i  — uniform colour-dielectric on the BCC *even-law* propagator
#         (F91: the gluon propagator is the even law).  Exact, spectral,
#         reduces BIT-FOR-BIT to `ca_gluon.gluon_rotation_step_spectral_bcc`
#         at eps_c=1; rescales the rotation rate (hence c) by sqrt(eps_c)
#         otherwise.  This is the BCC twin of `gluon_dielectric_rotation_step_2d`.
#  D-ii — gap coupling: condensate VEV / dual-Meissner mass from the
#         ca_colour_condensate MC density chain (rho -> z -> m_D -> v).
#  D-iii— gap-massive gluon step: the gluon evolved with the condensate-induced
#         effective mass m_V (Proca even law); m_V=0 reduces to the free step.
#  D-iv — spatially-varying eps_c(x) split-step evolution: the dynamical
#         demonstration of flux expulsion (dual Meissner) — a colour-electric
#         packet cannot propagate into the condensed (eps_c->0) vacuum.


# ---- D-i : uniform colour-dielectric on the BCC even-law propagator -------

def gluon_dielectric_rotation_step_bcc(E_G, B_G, eps_c=None):
    """
    One tick of the F43/F91 *even-law* BCC gluon (E,B) rotation rule
    renormalised by a *uniform* colour-dielectric eps_c.

    The even dispersion Omega_even(k) = omega_+(k/2)+omega_-(k/2) of the free
    step is rescaled by the local refractive factor n_c = eps_c^{-1/2}:
        Omega_even -> Omega_even / n_c = Omega_even * sqrt(eps_c).
    This is the BCC twin of `gluon_dielectric_rotation_step_2d` and the colour
    analogue of F64's dielectric renormalisation of the EM rotation rule.

    Parameters
    ----------
    E_G, B_G : (8, L, L, L) real colour-octet fields.
    eps_c    : float (uniform colour permittivity) or None.
               None or 1.0 -> reduces to
               `ca_gluon.gluon_rotation_step_spectral_bcc` BIT-FOR-BIT.

    Returns
    -------
    E_new, B_new : (8, L, L, L) real.

    A uniform eps_c keeps the step spectral and exactly orthogonal (energy
    conserving) while rescaling c.  The spatially-varying, flux-expelling case
    is `gluon_dielectric_evolve_bcc` (D-iv).
    """
    if eps_c is None or eps_c == 1.0:
        return cg.gluon_rotation_step_spectral_bcc(E_G, B_G)
    if E_G.shape[0] != 8 or B_G.shape[0] != 8:
        raise ValueError("E_G, B_G must have first axis size 8 (SU(3) octet)")
    s = float(eps_c) ** 0.5                            # = 1 / n_c
    shape = E_G.shape[1:]
    KX, KY, KZ = cwmu._kgrid3d(*shape)
    Omega = cwmu._omega_even(KX, KY, KZ) * s           # <-- dielectric rescaling
    cosO = np.cos(Omega)
    sinO = np.sin(Omega)
    E_new = np.zeros_like(E_G)
    B_new = np.zeros_like(B_G)
    for a in range(8):
        Ek = _fft.fftn(E_G[a])
        Bk = _fft.fftn(B_G[a])
        E_new[a] = _fft.ifftn(cosO * Ek + sinO * Bk).real
        B_new[a] = _fft.ifftn(-sinO * Ek + cosO * Bk).real
    return E_new, B_new


# ---- D-ii : gap coupling — condensate VEV / dual-Meissner mass -----------

def condensate_vev(beta, rho):
    """Condensate VEV bundle from the F88 monopole-density chain (Part F of
    ca_colour_condensate): rho -> fugacity z -> Debye mass m_D -> v = m_D/e.

    Returns dict {v, m_V, sigma_F86, beta, rho} with m_V = e v = m_D the
    dual-Meissner (dual-photon) mass and sigma_F86 = 2 pi v^2 the F86 tension.
    All three are fixed by the single measured density rho.
    """
    v, sigma_f86, mD = cc.f86_vev_from_density(beta, rho)
    return {'v': float(v), 'm_V': float(mD), 'sigma_F86': float(sigma_f86),
            'beta': float(beta), 'rho': float(rho)}


def condensate_vev_from_mc(L=6, beta=1.8, n_sweeps=120, seed=3):
    """Measure rho on an equilibrated 3D compact-U(1) configuration and return
    `condensate_vev`.  Couples the *measured* gap to the gluon field with no
    assumed VEV (the F88 hand-off to F86)."""
    _, hist = cc.u1_metropolis_3d(L=L, beta=beta, n_sweeps=n_sweeps, seed=seed)
    rho = float(np.mean(hist))
    out = condensate_vev(beta, rho)
    out['n_sweeps'] = n_sweeps
    out['L_mc'] = L
    return out


def gluon_gap_mass(beta, rho):
    """Dual-Meissner gluon mass m_V = e v = m_D induced by the condensate gap
    (e^2 = 1/beta in 3D lattice units, so m_V = m_D directly)."""
    return float(cc.debye_mass(beta, rho))


# ---- D-iii : gap-massive gluon step (gap coupled into the dynamical field) -

def gluon_gap_massive_step_bcc(E_G, B_G, beta, rho, dt=1.0):
    """
    Evolve the gluon (E,B) field with the *condensate-induced* effective mass
    m_V = e v (the dual-Meissner mass from the gap), using the Proca even-law
    step `ca_gluon.gluon_massive_step_spectral_bcc`.

    Dispersion:  omega_eff(k) = sqrt(m_V^2 + Omega_even(k)^2).
    Gapless limit (rho -> 0  =>  m_V -> 0) reduces BIT-FOR-BIT to the free
    even-law step.  This is the dynamical statement of confinement: the
    colour field propagates with a mass gap set by the measured condensate.
    """
    m_V = gluon_gap_mass(beta, rho)
    return cg.gluon_massive_step_spectral_bcc(E_G, B_G, m_g=m_V, dt=dt)


# ---- D-iv : spatially-varying eps_c(x) split-step evolution (flux expulsion)

def eps_c_field_from_condensate(f_field):
    """eps_c(x) = 1 - f(x)^2 from a (real-space) normalised condensate field
    f = |phi|/v in [0,1].  Tube core f=0 -> eps_c=1 (free); condensed vacuum
    f=1 -> eps_c=0 (colour-electric flux expelled)."""
    return colour_dielectric_from_condensate(f_field)


def _free_even_step_dt_bcc(E_G, B_G, dt):
    """Free even-law BCC gluon step for a general dt (Omega_even * dt).
    dt=1 reduces to `ca_gluon.gluon_rotation_step_spectral_bcc` bit-for-bit."""
    shape = E_G.shape[1:]
    KX, KY, KZ = cwmu._kgrid3d(*shape)
    Omega = cwmu._omega_even(KX, KY, KZ) * dt
    cosO, sinO = np.cos(Omega), np.sin(Omega)
    E_new = np.zeros_like(E_G)
    B_new = np.zeros_like(B_G)
    for a in range(E_G.shape[0]):
        Ek = _fft.fftn(E_G[a])
        Bk = _fft.fftn(B_G[a])
        E_new[a] = _fft.ifftn(cosO * Ek + sinO * Bk).real
        B_new[a] = _fft.ifftn(-sinO * Ek + cosO * Bk).real
    return E_new, B_new


def _free_even_step_dt_2d(E_G, B_G, dt):
    """Free gluon step on the 2D square lattice for a general dt.
    dt=1 reduces to `ca_gluon.gluon_rotation_step_spectral_2d` bit-for-bit."""
    Lx, Ly = E_G.shape[1], E_G.shape[2]
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    Omega = cm2.rotation_omega_2d(KX, KY) * dt
    cosO, sinO = np.cos(Omega), np.sin(Omega)
    E_new = np.zeros_like(E_G)
    B_new = np.zeros_like(B_G)
    for a in range(E_G.shape[0]):
        Ek = _fft.fft2(E_G[a])
        Bk = _fft.fft2(B_G[a])
        E_new[a] = _fft.ifft2(cosO * Ek + sinO * Bk).real
        B_new[a] = _fft.ifft2(-sinO * Ek + cosO * Bk).real
    return E_new, B_new


def gluon_dielectric_evolve_2d(E_G, B_G, eps_c_field, n_steps=1, dt=0.5):
    """
    Time-evolve the gluon (E,B) field through a *spatially-varying* colour-
    dielectric eps_c(x) on the 2D square lattice (the transverse plane).

    Scheme (per tick): the free rotation increment is locally rescaled by the
    refractive slow-down  s(x) = sqrt(eps_c(x)) in [0,1]:

        (E,B)_new = (E,B) + s(x) * [ R_free(Omega*dt)(E,B) - (E,B) ] ,

    R_free the spectral even-law rotation.  Properties:
      * eps_c == 1 everywhere  =>  s == 1  =>  (E,B)_new = R_free(E,B)
        BIT-FOR-BIT (the free propagator is recovered exactly).
      * in the condensed vacuum eps_c -> 0  =>  s -> 0: the field there is
        FROZEN — colour-electric flux cannot rotate (propagate) into it, the
        dual-Meissner expulsion realised dynamically.
      * orthogonal/energy-exact only in the uniform limit; with spatial
        variation it is a 2nd-order-in-dt split-step (use small dt), exactly as
        a variable-speed wave problem requires.

    Parameters
    ----------
    E_G, B_G    : (noct, Lx, Ly) real (noct typically 8, or 1 for a probe).
    eps_c_field : (Lx, Ly) real in [0,1].
    n_steps     : number of ticks.
    dt          : sub-tick (keep <~0.5 for the varying case).

    Returns E_G, B_G after n_steps.
    """
    s = np.sqrt(np.clip(np.asarray(eps_c_field, dtype=float), 0.0, 1.0))
    s = s[None, :, :]                          # broadcast over octet axis
    E, B = E_G, B_G
    for _ in range(int(n_steps)):
        E_r, B_r = _free_even_step_dt_2d(E, B, dt)
        E = E + s * (E_r - E)
        B = B + s * (B_r - B)
    return E, B


def gluon_dielectric_evolve_bcc(E_G, B_G, eps_c_field, n_steps=1, dt=0.5):
    """BCC analogue of `gluon_dielectric_evolve_2d`.

    E_G, B_G    : (noct, L, L, L) real.
    eps_c_field : (L, L, L) real in [0,1].
    Same split-step / freezing properties; eps_c==1 -> free even step bit-for-bit.
    """
    s = np.sqrt(np.clip(np.asarray(eps_c_field, dtype=float), 0.0, 1.0))
    s = s[None, :, :, :]
    E, B = E_G, B_G
    for _ in range(int(n_steps)):
        E_r, B_r = _free_even_step_dt_bcc(E, B, dt)
        E = E + s * (E_r - E)
        B = B + s * (B_r - B)
    return E, B


def field_energy(E_G, B_G):
    """Lattice (E,B) energy  Sum_{a,x} (E^2 + B^2) — the rotation-invariant
    norm conserved by the uniform even-law step."""
    return float(np.sum(E_G ** 2) + np.sum(B_G ** 2))


def slab_condensate_field_2d(L, core_frac=0.5, axis=1):
    """Build a test condensate field f(x) on an L×L lattice: a normal 'tube
    core' (f=0, eps_c=1) occupying the central `core_frac` fraction along
    `axis`, with the condensed vacuum (f=1, eps_c=0) outside.  Smoothly ramped
    (cosine) over 2 sites to avoid ringing.  Returns f (L,L)."""
    coord = np.arange(L)
    half = core_frac * L / 2.0
    c0 = (L - 1) / 2.0
    d = np.abs(coord - c0)
    f1d = np.clip((d - half) / 2.0, 0.0, 1.0)        # 0 in core -> 1 outside
    f1d = 0.5 - 0.5 * np.cos(np.pi * f1d)            # smooth ramp
    if axis == 1:
        return np.tile(f1d[None, :], (L, 1))
    return np.tile(f1d[:, None], (1, L))
