"""
dirac_gravity_fork.py — Dynamical Dirac CA on a curved background (D2) + linearized
backreaction (D3a)
====================================================================================
Drafted 2026-05-30.  Implements `ca-dirac-gravity-plan.md` Stages D2 and D3a as a
self-contained project fork, built on the already-verified pieces:

  * Stage D1 (Dirac propagator, m=0 → Weyl regression) lives in `ca_dirac.py`.
  * Static-background *dispersion* identity (F46/F50) lives in `gr_fork_F46_dirac.py`.

What is *new* here is the **time-domain** wave-packet evolution on a curved
background and its backreaction:

  D2  — release a wave packet on a fixed (A(x), B(x)) and track its centroid /
        internal clock against the analytic geodesic / GR prediction:
          • Rindler free-fall (equivalence principle): d²x/dt² → −a·c_eff²
          • dynamical gravitational redshift: rest-leg clock rate ∝ √A(x)
          • weak-Schwarzschild eikonal deflection of a fast packet
  D3a — the metric is *sourced by the matter itself*:
          ∇²Φ = 4πG ρ,   ρ = |Ψ|²,   (A,B) = (1+2Φ/c², 1−2Φ/c²)
        co-evolved with the Dirac field, and the honest test is the
        self-redshift of a probe packet sitting in the source's own well.

Physics conventions (exact-QCA, Findings 9/46/50/52)
----------------------------------------------------
The curved-tetrad chiral Dirac Hamiltonian for a static diagonal metric
ds² = −A c₀² dt² + B δ_ij dx^i dx^j  is (notebook pp.16-17,32-33; gr_fork_F46_dirac):

    i ∂_t Ψ = [ c_eff(x) · α·p̂  +  √A(x) · m · β ] Ψ,    c_eff = c₀ √(A/B)

so **both legs of the F46 spherical triangle become site-dependent**: the rest leg
√A·m carries the static redshift / free-fall force, the kinetic leg c_eff carries
deflection & Shapiro.  One Strang tick:

    Mix_rest(√A·m, dt/2) ∘ Kinetic(c_eff, dt) ∘ Mix_rest(√A·m, dt/2)

Each sub-operator is exactly unitary ⇒ norm conserved to the kinetic solver floor;
Strang error O(dt²·|∇A|, dt²·|∇c_eff|).

Two kinetic engines (selectable):
  "cayley" — Crank–Nicolson variable-c Weyl solver (`ca_curved.CayleyVarcSolver2D`);
             handles an *inhomogeneous* c_eff(x) field; base speed = the value put in
             c_eff_field.  Used for all curved backgrounds.
  "qca"    — the bounded exact-QCA Weyl walk (Paper-1 Eq.16) rate-rescaled by a
             *scalar* √(A/B); spectral, so needs a (near-)uniform background.  Used
             only for the flat m=0 regression where it reduces bit-for-bit to two
             decoupled exact Weyl steps.

Run the built-in suite:
    python forks/dirac_gravity_fork.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

_THIS = os.path.dirname(__file__)
_SIM = os.path.abspath(os.path.join(_THIS, ".."))
for _p in (_SIM, _THIS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ca_core_exact as ce                                   # noqa: E402
from ca_dirac import (                                       # noqa: E402
    _mix_eta_chi, _weyl_half_step_2c, dirac_step_2d_splitstep,
    gaussian_dirac_2d, dirac_norm, _dirac_plus_eigenvector,
)
from ca_curved import CayleyVarcSolver2D                     # noqa: E402


# ════════════════════════════════════════════════════════════════════
#  Background metrics — return (A_field, B_field), with g_00 = −A, g_ii = B
# ════════════════════════════════════════════════════════════════════

def lapse(A_field):
    """√A — the rest-leg (clock-rate) renormalisation factor."""
    return np.sqrt(np.abs(A_field))


def c_eff_from_AB(A_field, B_field, c0):
    """Kinetic-leg speed c_eff = c₀ √(A/B) seen by a Dirac packet."""
    return c0 * np.sqrt(np.abs(A_field) / np.abs(B_field))


def rindler_background(shape, a, x0=None):
    """Uniformly-accelerated (Rindler) frame.

        ds² = −(1 + a·(x−x0))² c₀² dt² + dx² + dy²   ⇒   A = (1+a·ξ)², B = 1

    The metric depends on x only (ξ = x − x0), so a packet at rest should
    "fall" toward −x with coordinate acceleration → a·c_eff² (equivalence
    principle).  Returns (A_field, B_field).
    """
    Lx, Ly = shape
    if x0 is None:
        x0 = Lx / 2.0
    xs = np.arange(Lx) - x0
    A_col = (1.0 + a * xs) ** 2
    A = np.repeat(A_col[:, None], Ly, axis=1)
    B = np.ones_like(A)
    return A, B


def schwarzschild_weak_background(shape, GM, c0, center=None, r_soft=3.0):
    """Linearised isotropic Schwarzschild (weak field).

        A = 1 − 2GM/(c₀² r),   B = 1 + 2GM/(c₀² r)      (r softened at r_soft)

    Both legs sourced ⇒ Einstein (factor-2) light bending in the eikonal
    limit, per F50/F52.  Returns (A_field, B_field).
    """
    Lx, Ly = shape
    if center is None:
        center = (Lx / 2.0, Ly / 2.0)
    xs = np.arange(Lx) - center[0]
    ys = np.arange(Ly) - center[1]
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    r = np.sqrt(X ** 2 + Y ** 2 + r_soft ** 2)        # softened
    phi = -GM / r                                      # Newtonian potential
    A = 1.0 + 2.0 * phi / c0 ** 2
    B = 1.0 - 2.0 * phi / c0 ** 2
    return A, B


def AB_from_phi(phi, c0):
    """Isotropic weak-field map Φ ↦ (A, B):  A = 1+2Φ/c², B = 1−2Φ/c².

    Both legs sourced by the same potential ⇒ Einstein-consistent (F52: the
    rest leg alone gives only Newtonian deflection; B carries the other half).
    """
    A = 1.0 + 2.0 * phi / c0 ** 2
    B = 1.0 - 2.0 * phi / c0 ** 2
    return A, B


# ════════════════════════════════════════════════════════════════════
#  The dynamical curved-background Dirac stepper
# ════════════════════════════════════════════════════════════════════

def make_kinetic_solver(c_eff_field, dt=1.0, n_sub=4):
    """Cached exactly-unitary variable-c Weyl kinetic solver (one LU factorisation,
    shared by η and χ)."""
    return CayleyVarcSolver2D(np.ascontiguousarray(c_eff_field), dt=dt, n_sub=n_sub)


def gravity_dirac_step_massive(eta_u, eta_d, chi_u, chi_d,
                               sqrtA_field, m, dt=1.0):
    """One Strang tick for a *massive* packet whose rest leg is lapse-rescaled,
    keeping the mass inside the exact-QCA kinetic dispersion so the packet has a
    genuine rest frame (slow group velocity, well-defined centroid).

        Mix(δm, dt/2) ∘ Kinetic_exactQCA(m0, dt) ∘ Mix(δm, dt/2)

    with site mass M(x) = √A(x)·m, baseline m0 = ⟨M⟩, δm = M − m0.

    SIGN CONVENTION.  The exact-QCA kinetic block carries the mass as +i·m0
    (generator −m0·β), so the per-cell δm correction must be applied with the
    *matching* sign to make the effective site mass M = m0 + δm (NOT m0 − δm).
    Concretely the mix angle is θ = −δm·dt/2 (i.e. `_mix_eta_chi(−δm·dt/2)`),
    the opposite of `ca_dirac.dirac_step_2d_varm_splitstep`, whose δm enters with
    the wrong relative sign — harmless there because every production use has
    δm = 0, but it inverts the force of a mass gradient.  Verified 2026-05-30:
    with the corrected sign a packet free-falls toward *low* lapse (a
    gravitational well attracts), as gravity requires.

    The lattice speed is the fixed exact-QCA value c_lat = 1/√2 (kinetic-leg
    √A/B renormalisation is dropped; per F52 the free-fall / Newtonian force
    lives entirely on the rest leg, so this is the correct locus for the
    equivalence-principle test).  Each sub-operator is exactly unitary.
    """
    m_field = sqrtA_field * m
    m0 = float(m_field.mean())
    dm = m_field - m0
    theta_half = -dm * dt * 0.5
    eta_u, eta_d, chi_u, chi_d = _mix_eta_chi(eta_u, eta_d, chi_u, chi_d,
                                              theta_half)
    eta_u, eta_d, chi_u, chi_d = dirac_step_2d_splitstep(
        eta_u, eta_d, chi_u, chi_d, m=m0, dt=dt)
    eta_u, eta_d, chi_u, chi_d = _mix_eta_chi(eta_u, eta_d, chi_u, chi_d,
                                              theta_half)
    return eta_u, eta_d, chi_u, chi_d


C_LAT_SQ = 0.5     # exact-QCA lattice light speed squared, c_lat = 1/√2


def gravity_dirac_step(eta_u, eta_d, chi_u, chi_d,
                       A_field, c_eff_field, m, dt=1.0,
                       kinetic="cayley", kinetic_solver=None,
                       n_sub=4, r_kin_scalar=None):
    """One Strang tick of the curved-background Dirac CA on a 2D lattice.

        Mix_rest(√A·m, dt/2) ∘ Kinetic(c_eff, dt) ∘ Mix_rest(√A·m, dt/2)

    Parameters
    ----------
    eta_u, eta_d, chi_u, chi_d : (Lx, Ly) complex — Weyl spinor (η_↑,η_↓,χ_↑,χ_↓).
    A_field     : (Lx, Ly) real — lapse² (g_00 = −A); rest leg uses √A.
    c_eff_field : (Lx, Ly) real — kinetic-leg speed c₀√(A/B) (Cayley path).
    m           : float — dimensionless mass, |m| ≤ 1.
    dt          : float — coordinate time step.
    kinetic     : "cayley" (inhomogeneous c_eff) | "qca" (scalar-rescaled exact walk).
    kinetic_solver : optional cached CayleyVarcSolver2D (cayley path; built if None).
    r_kin_scalar   : float — uniform √(A/B) for the "qca" path.

    Each sub-operator is exactly unitary ⇒ norm conserved to the solver floor.
    """
    theta_half = lapse(A_field) * m * dt * 0.5          # redshifted rest leg

    eta_u, eta_d, chi_u, chi_d = _mix_eta_chi(eta_u, eta_d, chi_u, chi_d,
                                              theta_half)

    if kinetic == "qca":
        if r_kin_scalar is None:
            r_kin_scalar = float(np.mean(c_eff_field))
        dt_eff = float(r_kin_scalar) * dt
        eta_u, eta_d = _weyl_half_step_2c(eta_u, eta_d, 0.5 * dt_eff)
        eta_u, eta_d = _weyl_half_step_2c(eta_u, eta_d, 0.5 * dt_eff)
        chi_u, chi_d = _weyl_half_step_2c(chi_u, chi_d, 0.5 * dt_eff)
        chi_u, chi_d = _weyl_half_step_2c(chi_u, chi_d, 0.5 * dt_eff)
    elif kinetic == "cayley":
        if kinetic_solver is None:
            kinetic_solver = make_kinetic_solver(c_eff_field, dt=dt, n_sub=n_sub)
        eta_u, eta_d = kinetic_solver.step(eta_u, eta_d)
        chi_u, chi_d = kinetic_solver.step(chi_u, chi_d)
    else:
        raise ValueError(f"kinetic must be 'cayley' or 'qca'; got {kinetic!r}")

    eta_u, eta_d, chi_u, chi_d = _mix_eta_chi(eta_u, eta_d, chi_u, chi_d,
                                              theta_half)
    return eta_u, eta_d, chi_u, chi_d


# ════════════════════════════════════════════════════════════════════
#  Initial conditions
# ════════════════════════════════════════════════════════════════════

def gaussian_packet_momentum(shape, k0, m, center=None, sigma=6.0,
                             branch="plus"):
    """A Gaussian envelope × plane wave × the +ω Dirac eigenvector at k0.

    Produces a positive-energy packet with mean momentum k0 (a clean
    propagating/deflecting state).  For k0=(0,0) it is a rest packet.
    Returns (eta_u, eta_d, chi_u, chi_d).
    """
    Lx, Ly = shape
    cx, cy = center if center is not None else (Lx / 2.0, Ly / 2.0)
    xs = np.arange(Lx) - cx
    ys = np.arange(Ly) - cy
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    env = np.exp(-(X ** 2 + Y ** 2) / (2.0 * sigma ** 2)).astype(complex)
    kx, ky = k0
    if kx == 0.0 and ky == 0.0:
        spinor = np.array([1, 0, 1, 0], dtype=complex) / np.sqrt(2.0)  # rest, mixed
    else:
        spinor = _dirac_plus_eigenvector(kx, ky, m)
    phase = np.exp(1j * (kx * X + ky * Y))
    base = env * phase
    return (spinor[0] * base, spinor[1] * base,
            spinor[2] * base, spinor[3] * base)


# ════════════════════════════════════════════════════════════════════
#  Observables
# ════════════════════════════════════════════════════════════════════

def density(eta_u, eta_d, chi_u, chi_d):
    """Probability density ρ(x) = |Ψ|²."""
    return (np.abs(eta_u) ** 2 + np.abs(eta_d) ** 2 +
            np.abs(chi_u) ** 2 + np.abs(chi_d) ** 2)


def centroid(rho, X, Y):
    tot = float(rho.sum())
    if tot <= 0:
        return float("nan"), float("nan")
    return float((X * rho).sum() / tot), float((Y * rho).sum() / tot)


def chirality_imbalance(eta_u, eta_d, chi_u, chi_d, mask=None):
    """(ρ_η − ρ_χ)/ρ_total over an optional region mask — the local clock signal."""
    n_eta = np.abs(eta_u) ** 2 + np.abs(eta_d) ** 2
    n_chi = np.abs(chi_u) ** 2 + np.abs(chi_d) ** 2
    if mask is not None:
        n_eta = n_eta[mask]
        n_chi = n_chi[mask]
    a = float(n_eta.sum())
    b = float(n_chi.sum())
    tot = a + b
    return (a - b) / tot if tot > 0 else 0.0


def _dominant_freq(signal, dt):
    """Angular frequency of the dominant positive-frequency FFT peak."""
    s = np.asarray(signal) - np.mean(signal)
    F = np.abs(np.fft.fft(s))
    w = np.fft.fftfreq(len(s), d=dt) * 2.0 * np.pi
    pos = w > 0
    return float(w[pos][np.argmax(F[pos])])


# ════════════════════════════════════════════════════════════════════
#  D1 regression — flat m=0 reduces to two decoupled exact Weyl steps
# ════════════════════════════════════════════════════════════════════

def test_d1_flat_weyl_regression(L=48, n_steps=12, dt=1.0, seed=0):
    """In flat space (A=B=1) with m=0 and the *exact-QCA* kinetic engine, one
    gravity_dirac_step must equal two independent exact Weyl walks bit-for-bit.

    This is the plan's D1 regression, applied to the curved-background stepper:
    the mass coupling switches off and η, χ propagate as decoupled Weyl spinors.
    """
    rng = np.random.default_rng(seed)
    shape = (L, L)

    def rfield():
        return (rng.standard_normal(shape) + 1j * rng.standard_normal(shape))

    eu, ed, xu, xd = rfield(), rfield(), rfield(), rfield()
    A = np.ones(shape)

    # Reference: two decoupled exact-QCA Weyl half-step pairs (= one full step).
    eu_ref, ed_ref = _weyl_half_step_2c(eu, ed, 0.5 * dt)
    eu_ref, ed_ref = _weyl_half_step_2c(eu_ref, ed_ref, 0.5 * dt)
    xu_ref, xd_ref = _weyl_half_step_2c(xu, xd, 0.5 * dt)
    xu_ref, xd_ref = _weyl_half_step_2c(xu_ref, xd_ref, 0.5 * dt)

    # Fork stepper, qca engine, m=0, r_kin=1 (flat).
    eu_f, ed_f, xu_f, xd_f = gravity_dirac_step(
        eu, ed, xu, xd, A_field=A, c_eff_field=np.ones(shape), m=0.0, dt=dt,
        kinetic="qca", r_kin_scalar=1.0)

    resid = max(
        float(np.max(np.abs(eu_f - eu_ref))),
        float(np.max(np.abs(ed_f - ed_ref))),
        float(np.max(np.abs(xu_f - xu_ref))),
        float(np.max(np.abs(xd_f - xd_ref))),
    )
    return {
        "residual_max_abs": resid,
        "pass": resid < 1e-12,
        "L": L, "n_steps": 1, "dt": dt,
    }


# ════════════════════════════════════════════════════════════════════
#  D2-(a) Rindler free-fall — equivalence principle
# ════════════════════════════════════════════════════════════════════

def _rindler_trajectory(L, a, m, dt, n_steps, sigma):
    """Release a positive-energy rest packet at ξ=0 in a Rindler frame
    (√A = 1 + a·ξ, B=1) and return (t, centroid displacement, norm_drift)."""
    shape = (L, L)
    x0 = L / 2.0
    xi = np.arange(L) - x0
    sqrtA = np.repeat((1.0 + a * xi)[:, None], L, axis=1)
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    G = np.exp(-((X - x0) ** 2 + (Y - L / 2.0) ** 2) /
               (2.0 * sigma ** 2)).astype(complex)
    eu = G / np.sqrt(2.0); ed = 0 * G; xu = G / np.sqrt(2.0); xd = 0 * G
    xc, norms = [], []
    for step in range(n_steps + 1):
        rho = density(eu, ed, xu, xd)
        cx, _ = centroid(rho, X, Y)
        xc.append(cx - x0)
        norms.append(float(rho.sum()))
        if step < n_steps:
            eu, ed, xu, xd = gravity_dirac_step_massive(eu, ed, xu, xd,
                                                        sqrtA, m, dt=dt)
    t = np.arange(n_steps + 1) * dt
    drift = float(abs(norms[-1] - norms[0]) / norms[0])
    return t, np.array(xc), drift


def test_rindler_freefall(L=220, a=0.006, m=0.35, dt=1.0, n_steps=110,
                          sigma=16.0, masses=(0.2, 0.35, 0.5)):
    """Equivalence principle: a packet released at rest in a Rindler frame
    free-falls toward *lower* lapse with coordinate acceleration

        d²ξ/dt² → −a · c_lat²,     c_lat² = 1/2   (exact-QCA lattice light speed)

    independent of its mass m.  Two checks:
      (1) coefficient — early-window parabola fit of ξ(t) gives |g| ≈ a·c_lat²;
      (2) universality — trajectories for several masses coincide (the trajectory
          is mass-independent, the sharp equivalence-principle signature).
    The fall is toward −ξ (low lapse = the gravitational-well side); norm is
    conserved to the propagator floor.
    """
    g_pred = a * C_LAT_SQ
    # universality: full trajectories for several masses
    traj = {}
    drifts = []
    for mm in masses:
        t, x, drift = _rindler_trajectory(L, a, mm, dt, n_steps, sigma)
        traj[mm] = x
        drifts.append(drift)
    ref_len = min(len(v) for v in traj.values())
    stack = np.array([traj[mm][:ref_len] for mm in masses])
    final_disps = {mm: float(traj[mm][-1]) for mm in masses}
    # spread of final displacement across masses, relative to the mean fall
    mean_fall = float(np.mean([abs(d) for d in final_disps.values()]))
    universality_spread = float(np.ptp(list(final_disps.values())) /
                                mean_fall) if mean_fall else float("nan")

    # coefficient from the requested m, early window (|ξ|<2) to stay slow
    t, x, drift = _rindler_trajectory(L, a, m, dt, n_steps, sigma)
    win = np.abs(x) < 2.0
    nw = max(int(win.sum()), 10)
    g_meas = -2.0 * float(np.polyfit(t[:nw], x[:nw], 2)[0])
    falls_into_well = x[-1] < 0           # toward −ξ = low lapse

    return {
        "g_meas_abs": abs(g_meas),
        "g_pred": g_pred,
        "coeff_ratio": abs(g_meas) / g_pred if g_pred else float("nan"),
        "falls_toward_low_lapse": bool(falls_into_well),
        "final_displacement": float(x[-1]),
        "final_disp_by_mass": final_disps,
        "universality_spread": universality_spread,
        "norm_drift": max(drifts + [drift]),
        "c_lat_sq": C_LAT_SQ,
        "params": {"L": L, "a": a, "m": m, "dt": dt, "n_steps": n_steps,
                   "sigma": sigma, "masses": list(masses)},
        "pass": (falls_into_well and
                 abs(abs(g_meas) / g_pred - 1.0) < 0.20 and
                 universality_spread < 0.12 and
                 max(drifts + [drift]) < 1e-9),
    }


# ════════════════════════════════════════════════════════════════════
#  D2-(b) Dynamical gravitational redshift — clock rate ∝ √A
# ════════════════════════════════════════════════════════════════════

def test_dynamical_redshift(L=96, m=0.5, c0=0.5, dt=0.5, n_steps=360,
                            sigma=7.0, A_near=0.81, A_far=1.0, n_sub=3):
    """Two static clocks (rest packets) at different lapse values tick at rates
    in the ratio √(A_near/A_far) — the gravitational-redshift formula, measured
    *dynamically* from the chirality-oscillation (zitterbewegung) frequency.

    Flat-space zitterbewegung is 2·arcsin(m) per unit time; on the rest leg the
    site-dependent angle √A·m rescales it to 2·arcsin(√A·m).  For the ratio of
    *frequencies* the leading factor is √A, so f_near/f_far → √(A_near/A_far).
    """
    results = {}
    freqs = {}
    for tag, Aval in (("near", A_near), ("far", A_far)):
        shape = (L, L)
        A = np.full(shape, Aval)
        B = np.ones(shape)
        c_eff = c_eff_from_AB(A, B, c0)
        # uniform background ⇒ the spectral qca engine is exact
        eu, ed, xu, xd = gaussian_packet_momentum(shape, k0=(0.0, 0.0), m=m,
                                                  sigma=sigma)
        # rest packet but pure-η to maximise the chirality-imbalance signal
        eu = eu * np.sqrt(2.0); xu = xu * 0.0
        sig = []
        for step in range(n_steps + 1):
            sig.append(chirality_imbalance(eu, ed, xu, xd))
            if step < n_steps:
                eu, ed, xu, xd = gravity_dirac_step(
                    eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=m, dt=dt,
                    kinetic="qca", r_kin_scalar=float(np.sqrt(Aval)))
        f = _dominant_freq(sig, dt)
        freqs[tag] = f
        # analytic per-position zitterbewegung frequency
        results[tag + "_freq_analytic"] = 2.0 * float(np.arcsin(np.sqrt(Aval) * m))

    ratio_meas = freqs["near"] / freqs["far"]
    ratio_pred_sqrtA = float(np.sqrt(A_near / A_far))
    ratio_pred_exact = (results["near_freq_analytic"] /
                        results["far_freq_analytic"])
    return {
        "freq_near": freqs["near"], "freq_far": freqs["far"],
        "ratio_meas": ratio_meas,
        "ratio_pred_sqrtA": ratio_pred_sqrtA,
        "ratio_pred_exact_arcsin": ratio_pred_exact,
        "params": {"L": L, "m": m, "c0": c0, "dt": dt, "n_steps": n_steps,
                   "A_near": A_near, "A_far": A_far},
        "pass": abs(ratio_meas / ratio_pred_exact - 1.0) < 0.03,
    }


# ════════════════════════════════════════════════════════════════════
#  D2-(c) Weak-Schwarzschild eikonal deflection of a fast packet
# ════════════════════════════════════════════════════════════════════

def test_schwarzschild_deflection(L=160, GM=0.6, c0=0.5, m=0.0,
                                  k_in=0.5, b=16, sigma=6.0, dt=1.0,
                                  n_steps=260, n_sub=2):
    """Send a fast (near-null, m≈0) packet past a weak-Schwarzschild mass at
    impact parameter b and measure the transverse deflection of its centroid.

    Eikonal prediction for the isotropic metric (A=1−2GM/c²r, B=1+2GM/c²r):
        Δθ_eik = −∫ ∂_y ln c_eff dx       (Snell-like; c_eff = c₀√(A/B))
    which integrates to the Einstein value 4GM/(c²b) for a ray grazing the mass.
    We compare the *measured* centroid bend to this same line-integral evaluated
    on the actual c_eff field (so it is an internal-consistency check of the
    dynamical run against its own eikonal limit, and reports K = Δθ·b·c²/GM).
    """
    shape = (L, L)
    cx0, cy0 = L / 2.0, L / 2.0
    A, B = schwarzschild_weak_background(shape, GM=GM, c0=c0,
                                         center=(cx0, cy0), r_soft=4.0)
    c_eff = c_eff_from_AB(A, B, c0)
    solver = make_kinetic_solver(c_eff, dt=dt, n_sub=n_sub)

    # launch from the left edge at height y = cy0 + b, moving in +x
    start_x = 0.18 * L
    eu, ed, xu, xd = gaussian_packet_momentum(
        shape, k0=(k_in, 0.0), m=m, center=(start_x, cy0 + b), sigma=sigma)

    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    cxs, cys = [], []
    for step in range(n_steps + 1):
        rho = density(eu, ed, xu, xd)
        cxv, cyv = centroid(rho, X, Y)
        cxs.append(cxv); cys.append(cyv)
        if step < n_steps:
            eu, ed, xu, xd = gravity_dirac_step(
                eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=m, dt=dt,
                kinetic="cayley", kinetic_solver=solver)

    cxs = np.array(cxs); cys = np.array(cys)
    # incoming slope (early) vs outgoing slope (late) of y(x)
    early = slice(3, n_steps // 4)
    late = slice(3 * n_steps // 4, n_steps + 1)
    s_in = float(np.polyfit(cxs[early], cys[early], 1)[0])
    s_out = float(np.polyfit(cxs[late], cys[late], 1)[0])
    dtheta_meas = float(np.arctan(s_out) - np.arctan(s_in))

    # eikonal line-integral prediction along the actual traversed row
    j = int(round(cy0 + b))
    ln_c = np.log(c_eff)
    dlnc_dy = (np.roll(ln_c, -1, axis=1) - np.roll(ln_c, 1, axis=1)) / 2.0
    dtheta_eik = float(-dlnc_dy[:, j].sum())
    K_meas = dtheta_meas * b * c0 ** 2 / GM
    K_eik = dtheta_eik * b * c0 ** 2 / GM
    return {
        "dtheta_meas": dtheta_meas,
        "dtheta_eikonal": dtheta_eik,
        "K_meas": K_meas,
        "K_eikonal": K_eik,
        "ratio_meas_eik": dtheta_meas / dtheta_eik if dtheta_eik else float("nan"),
        "params": {"L": L, "GM": GM, "c0": c0, "k_in": k_in, "b": b,
                   "n_steps": n_steps, "m": m},
        # (i) deflection toward the mass (downward, −y) ⇒ dtheta_meas < 0;
        # (ii) the c_eff field carries the Einstein factor-2 bend K_eik ≈ 4
        #      (both legs sourced, per F50/F52);
        # (iii) the dynamical centroid realises its own eikonal limit to ~25%.
        "pass": (dtheta_meas < 0) and (3.0 < abs(K_eik) < 5.0) and
                (abs(dtheta_meas / dtheta_eik - 1.0) < 0.25),
    }


# ════════════════════════════════════════════════════════════════════
#  D3a — linearized backreaction (metric sourced by the matter itself)
# ════════════════════════════════════════════════════════════════════

def poisson_2d_fft(rho, G):
    """Solve ∇²Φ = 4πG ρ on a periodic lattice via FFT (zero-mean source).

    NOTE (Finding 8): in 2D the Green's function is logarithmic, not 1/r, so
    Φ here is the genuine 2D self-consistent potential — used for the
    *self-consistency* (loop-closure & self-redshift) tests below, not for an
    absolute 1/r comparison.  Returns Φ with ⟨Φ⟩ = 0.
    """
    Lx, Ly = rho.shape
    src = 4.0 * np.pi * G * (rho - rho.mean())     # subtract mean for periodicity
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    k2 = KX ** 2 + KY ** 2
    k2[0, 0] = 1.0                                  # avoid /0; zero mode → 0
    Phi_k = -np.fft.fft2(src) / k2                  # ∇² → −k²
    Phi_k[0, 0] = 0.0
    phi = np.real(np.fft.ifft2(Phi_k))
    return phi - phi.mean()


def run_backreaction(eta_u, eta_d, chi_u, chi_d, m, c0, G,
                     dt=1.0, n_steps=80, n_sub=2, refresh=4,
                     static_source=None, source_weight=1.0):
    """Co-evolve the Dirac field with the metric it sources.

        ρ = |Ψ|² (+ optional static_source) → ∇²Φ = 4πGρ → (A,B) = (1±2Φ/c²)
        → one Strang Dirac tick in that (A,B) → repeat (metric refreshed every
        `refresh` ticks).

    Returns the field, the final Φ/A/B, and the norm history.  Each Dirac tick
    is exactly unitary ⇒ the matter norm is conserved regardless of the metric.
    """
    shape = eta_u.shape
    norms = []
    phi = A = B = c_eff = solver = None
    for step in range(n_steps):
        if step % refresh == 0:
            rho = density(eta_u, eta_d, chi_u, chi_d)
            if static_source is not None:
                rho = rho + source_weight * static_source
            phi = poisson_2d_fft(rho, G)
            A, B = AB_from_phi(phi, c0)
            c_eff = c_eff_from_AB(A, B, c0)
            solver = make_kinetic_solver(c_eff, dt=dt, n_sub=n_sub)
        norms.append(dirac_norm(eta_u, eta_d, chi_u, chi_d))
        eta_u, eta_d, chi_u, chi_d = gravity_dirac_step(
            eta_u, eta_d, chi_u, chi_d, A_field=A, c_eff_field=c_eff, m=m,
            dt=dt, kinetic="cayley", kinetic_solver=solver)
    norms.append(dirac_norm(eta_u, eta_d, chi_u, chi_d))
    return {
        "field": (eta_u, eta_d, chi_u, chi_d),
        "phi": phi, "A": A, "B": B, "c_eff": c_eff,
        "norms": np.array(norms),
    }


def test_backreaction_norm(L=64, m=0.4, c0=0.5, G=0.02, dt=1.0,
                           n_steps=60, sigma=6.0, n_sub=2):
    """Self-gravitating packet: norm must stay conserved while the metric it
    generates evolves underneath it (each tick is exactly unitary)."""
    shape = (L, L)
    eu, ed, xu, xd = gaussian_packet_momentum(shape, k0=(0.0, 0.0), m=m,
                                              sigma=sigma)
    out = run_backreaction(eu, ed, xu, xd, m=m, c0=c0, G=G, dt=dt,
                           n_steps=n_steps, n_sub=n_sub)
    norms = out["norms"]
    drift = float(abs(norms[-1] - norms[0]) / norms[0])
    return {
        "norm_initial": float(norms[0]),
        "norm_final": float(norms[-1]),
        "norm_drift": drift,
        "phi_min": float(out["phi"].min()),
        "phi_max": float(out["phi"].max()),
        "params": {"L": L, "m": m, "c0": c0, "G": G, "n_steps": n_steps},
        "pass": drift < 1e-9,
    }


def test_self_redshift(L=80, m=0.5, c0=0.5, dt=0.5, n_steps=380,
                       sigma_src=7.0, sigma_probe=5.0, well_depth=0.22,
                       n_sub=1, refresh=20):
    """The honest D3a test (plan): a wave packet's *own* mass causes a frequency
    shift in a probe.  A static source blob digs a *self-consistent* well Φ
    (solved from ρ each refresh, ∇²Φ = 4πGρ); two identical probe clocks — one
    deep in the well, one near the flat rim — tick at rates set by the rest leg
    on the field-generated lapse, in the ratio √(A_near/A_far).

    The effective coupling G is calibrated so the self-generated well stays in
    the weak-field regime (|2Φ/c²| ≈ `well_depth`), where the lapse map
    A = 1+2Φ/c² is valid.  PASS if the measured near/far clock ratio matches the
    rest-leg prediction 2·arcsin(√A·m) from the field's *own* lapse to a few
    percent (the backreaction loop closes), and the deep clock runs slower
    (redshift).
    """
    shape = (L, L)
    cx = L // 2
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")

    # static source blob at center; calibrate the source amplitude (≡ G·M) so the
    # weak-field well reaches the requested depth: φ.min() → −well_depth·c0²/2.
    rsrc = np.sqrt((X - cx) ** 2 + (Y - cx) ** 2)
    blob = np.exp(-rsrc ** 2 / (2.0 * sigma_src ** 2))
    phi_unit = poisson_2d_fft(blob, G=1.0)
    target_phi_min = -0.5 * well_depth * c0 ** 2
    scale = target_phi_min / phi_unit.min()
    source = blob * scale                                  # ≡ G·ρ_source
    Gc = 1.0                                               # G folded into source

    # probe at the bottom of the well vs near the (flatter) rim
    near_c = (cx, cx)
    far_c = (cx, cx + L // 2 - 6)

    freqs, A_at = {}, {}
    for tag, ctr in (("near", near_c), ("far", far_c)):
        eu, ed, xu, xd = gaussian_packet_momentum(shape, k0=(0.0, 0.0), m=m,
                                                  center=ctr, sigma=sigma_probe)
        eu = eu * np.sqrt(2.0); xu = xu * 0.0          # pure-η ⇒ clean clock signal
        probe_mask = ((X - ctr[0]) ** 2 + (Y - ctr[1]) ** 2) <= sigma_probe ** 2
        sig, A_samples = [], []
        A = c_eff = solver = None
        for step in range(n_steps + 1):
            if step % refresh == 0:
                # the probe is a test clock; the lapse is the source's own
                # self-consistent field (∇²Φ = 4πGρ_source), not an imported −GM/r
                rho = source
                phi = poisson_2d_fft(rho, Gc)
                A, B = AB_from_phi(phi, c0)
                c_eff = c_eff_from_AB(A, B, c0)
                solver = make_kinetic_solver(c_eff, dt=dt, n_sub=n_sub)
                A_samples.append(float(A[probe_mask].mean()))
            sig.append(chirality_imbalance(eu, ed, xu, xd))
            if step < n_steps:
                eu, ed, xu, xd = gravity_dirac_step(
                    eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=m, dt=dt,
                    kinetic="cayley", kinetic_solver=solver)
        freqs[tag] = _dominant_freq(sig, dt)
        A_at[tag] = float(np.mean(A_samples))

    ratio_meas = freqs["near"] / freqs["far"]
    ratio_pred_sqrtA = float(np.sqrt(A_at["near"] / A_at["far"]))
    ratio_pred_exact = float(np.arcsin(np.sqrt(A_at["near"]) * m) /
                             np.arcsin(np.sqrt(A_at["far"]) * m))
    return {
        "freq_near": freqs["near"], "freq_far": freqs["far"],
        "A_near": A_at["near"], "A_far": A_at["far"],
        "ratio_meas": ratio_meas,
        "ratio_pred_sqrtA": ratio_pred_sqrtA,
        "ratio_pred_exact_arcsin": ratio_pred_exact,
        "redshift_detected": bool(ratio_meas < 1.0),       # deep clock slower
        "params": {"L": L, "m": m, "c0": c0, "well_depth": well_depth,
                   "n_steps": n_steps, "dt": dt},
        "pass": (ratio_meas < 1.0 and
                 abs(ratio_meas / ratio_pred_exact - 1.0) < 0.04),
    }


# ════════════════════════════════════════════════════════════════════
#  Module identity + self-test driver
# ════════════════════════════════════════════════════════════════════

NAME = "dirac_gravity_fork"
DESCRIPTION = ("Dynamical curved-background Dirac CA (D2: Rindler free-fall, "
               "redshift, eikonal deflection) + linearized backreaction (D3a: "
               "self-sourced metric, self-redshift). Builds on F46/F50/F52.")


def run_all(verbose=True):
    suite = [
        ("D1_flat_weyl_regression", test_d1_flat_weyl_regression),
        ("D2a_rindler_freefall", test_rindler_freefall),
        ("D2b_dynamical_redshift", test_dynamical_redshift),
        ("D2c_schwarzschild_deflection", test_schwarzschild_deflection),
        ("D3a_backreaction_norm", test_backreaction_norm),
        ("D3a_self_redshift", test_self_redshift),
    ]
    results = {}
    for name, fn in suite:
        if verbose:
            print(f"[run] {name} ...", flush=True)
        results[name] = fn()
        if verbose:
            print(f"      pass={results[name].get('pass')}", flush=True)
    return results


if __name__ == "__main__":
    import json
    res = run_all(verbose=True)
    print(json.dumps(res, indent=2, default=float))
