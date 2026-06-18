"""
ca_dual_gl_backreaction.py — Self-consistent dual-Ginzburg-Landau back-reaction
================================================================================

Created: 2026-06-11

What this closes
----------------
F86 built the dual-superconductor flux tube as the *analytic* BPS (ANO) vortex
(exact σ = 2π v² n at κ=1).  F137 made the confining bag **live** — the
colour-magnetic condensate f(x) melted where the quark colour charge sits — but
only as a **mean-field** dielectric: the condensate responded to the colour-
charge density through a *fixed* Gaussian smear λ, a one-way map.  Consequently
the flux tube stayed connected and linear only out to ~2λ, then **pinched off**
(F137 §5, the honest open edge).

This module closes that loop.  It implements the genuine **self-consistent
dual-Ginzburg-Landau back-reaction**: the colour-electric flux that the
condensate confines is *itself* what melts the condensate, and the two fields
are solved to **mutual consistency**.  The condensate digs the channel; the
channel (its expelled flux) re-shapes the condensate; iterate to a fixed point.

The coupled system (Friedberg-Lee colour-dielectric form of the dual GL free
energy, the real-space partner of F86's gauge-vortex BPS functional)
-------------------------------------------------------------------------------
Order parameter  f(x) ∈ [0,1]  (normalised condensate |φ|/v, f→1 vacuum, f→0
melted core).  Colour-dielectric  ε_c(f) = 1 − f²  (F86: ε_c→0 condensed
vacuum expels flux, ε_c→1 melted core conducts it).  Quark colour charge ρ^a(x)
(octet components, each colour-singlet so Σ_x ρ^a = 0).

Free energy:

    F[f] = ∫ d^dx [ (∇f)²  +  (1/4ξ²)(f²−1)²  +  ½ Σ_a |D^a|² / ε_c(f) ] ,

with the colour-electric displacement D^a = ε_c E^a, E^a = −∇ψ^a fixed by the
**dielectric Gauss law**  ∇·(ε_c ∇ψ^a) = −ρ^a  (the dual-superconductor
constraint: the quarks pin the flux, the condensate must let it pass).

Euler-Lagrange / gradient flow for the condensate (E^a, hence D^a, frozen
during each f-substep; ψ^a re-solved each outer sweep):

    ∂f/∂τ = −δF/δf = 2∇²f − (1/ξ²)(f²−1)f − f Σ_a |D^a|²/ε_c² .

The last term is the **back-reaction**: where the confined flux |D|² is large it
drives f→0 (melts the condensate), which raises ε_c there, which lets more flux
through — the self-consistent feedback F137 lacked.  The fixed point is a flux
tube whose **cross-section is R-independent** (constant energy-per-length →
linear confinement) that stays connected to arbitrary separation — the F137 2λ
pinch is cured.

Exact anchors
-------------
* Zero-field limit:  the f-flow relaxes to the exact GL domain wall
  f(x)=tanh(x/2ξ)  (the kink of 2f''=(1/ξ²)(f²−1)f).  ``gl_kink`` is the
  analytic reference — the ODE-exact validation of the condensate sector.
* Confinement:  the bag/string energy is linear in R with a **constant**
  tension (the dynamical realisation of F86's σ=2π v² n, which remains the
  analytic gauge-vortex value this real-space tube reproduces qualitatively).

Pure numpy throughout (CLAUDE.md: hand-rolled numerics on the delicate
transforms; no scipy).  Works in 2D (transverse / q-q̄ plane) and 3D (BCC box).
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "grad", "laplacian", "dielectric_op", "dielectric_poisson",
    "colour_dielectric", "gl_energy", "gl_kink",
    "self_consistent_bag", "meanfield_bag",
]


# ----------------------------------------------------------------------
# Lattice differential operators (periodic, central differences)
# ----------------------------------------------------------------------
def grad(psi):
    """Central-difference gradient, periodic.  Returns (d, *shape)."""
    return np.stack(
        [0.5 * (np.roll(psi, -1, ax) - np.roll(psi, 1, ax))
         for ax in range(psi.ndim)], axis=0)


def laplacian(f):
    """7-point (2d+1) periodic Laplacian Σ(f_{+}+f_{−}) − 2d·f."""
    return (sum(np.roll(f, -1, ax) + np.roll(f, 1, ax) for ax in range(f.ndim))
            - 2.0 * f.ndim * f)


def colour_dielectric(f, eps_floor=1e-3):
    """ε_c = 1 − f², floored to keep the variable-coefficient Poisson operator
    non-singular (F86: f=1 vacuum → ε_c=0 expels flux; f=0 core → ε_c=1)."""
    return np.clip(1.0 - np.asarray(f, float) ** 2, eps_floor, 1.0)


# ----------------------------------------------------------------------
# Variable-coefficient dielectric Gauss law:  −div(ε ∇ψ) = ρ
# ----------------------------------------------------------------------
def dielectric_op(psi, eps):
    """A[ψ] = −div(ε ∇ψ) with arithmetic face-mean ε, periodic.  SPD on the
    zero-mean subspace (nullspace = constants)."""
    out = np.zeros_like(psi)
    for ax in range(psi.ndim):
        ep = 0.5 * (eps + np.roll(eps, -1, ax))   # face between i, i+1
        em = 0.5 * (eps + np.roll(eps, 1, ax))    # face between i−1, i
        out += ep * (psi - np.roll(psi, -1, ax)) + em * (psi - np.roll(psi, 1, ax))
    return out


def dielectric_poisson(rho, eps, tol=1e-7, maxit=600):
    """Solve −div(ε ∇ψ) = ρ on a periodic lattice by matrix-free CG.

    ρ is projected to zero mean (periodic solvability; a colour-singlet source
    already satisfies Σρ=0).  Returns (ψ, iters, relative_residual).
    """
    rho = rho - rho.mean()
    psi = np.zeros_like(rho)
    r = rho - dielectric_op(psi, eps)
    r -= r.mean()
    p = r.copy()
    rs = float((r * r).sum())
    r0 = rs if rs > 0 else 1.0
    rsn = rs
    it = 0
    for it in range(1, maxit + 1):
        Ap = dielectric_op(p, eps)
        Ap -= Ap.mean()
        den = float((p * Ap).sum())
        if den == 0.0:
            break
        alpha = rs / den
        psi += alpha * p
        r -= alpha * Ap
        rsn = float((r * r).sum())
        if rsn <= tol * tol * r0:
            break
        p = r + (rsn / rs) * p
        rs = rsn
    psi -= psi.mean()
    return psi, it, float(np.sqrt(rsn / r0))


# ----------------------------------------------------------------------
# Dual-GL energy and the analytic kink anchor
# ----------------------------------------------------------------------
def gl_energy(f, D2, xi, eps_floor=1e-3):
    """Return (E_grad, E_bag, E_field, E_total) of the dual-GL free energy for
    a condensate ``f`` and confined colour-flux density ``D2`` = Σ_a|D^a|².

      E_grad  = Σ (∇f)²            (condensate gradient / surface)
      E_bag   = Σ (1/4ξ²)(f²−1)²   (volume condensation / bag constant)
      E_field = Σ ½ D²/ε_c         (confined colour-electric energy)
    """
    eps = colour_dielectric(f, eps_floor)
    g2 = sum((0.5 * (np.roll(f, -1, ax) - np.roll(f, 1, ax))) ** 2
             for ax in range(f.ndim))
    e_grad = float(g2.sum())
    e_bag = float(((1.0 / (4.0 * xi ** 2)) * (f * f - 1.0) ** 2).sum())
    e_field = float((0.5 * D2 / eps).sum())
    return e_grad, e_bag, e_field, e_grad + e_bag + e_field


def gl_kink(x, xi):
    """Exact GL domain wall  f(x)=tanh(x/2ξ)  — the zero-field fixed point of
    the f-flow (2f'' = (1/ξ²)(f²−1)f).  The condensate-sector anchor."""
    return np.tanh(np.asarray(x, float) / (2.0 * xi))


# ----------------------------------------------------------------------
# The self-consistent dual-GL back-reaction loop
# ----------------------------------------------------------------------
def self_consistent_bag(sources, xi=1.0, eps_floor=1e-2, dtau=0.03,
                        n_out=400, sweeps=1, tol=2e-6, f_init=None,
                        poisson_tol=3e-6, poisson_maxit=300,
                        record=False):
    """Relax the coupled (condensate f, colour-electric flux) system to the
    dual-GL fixed point.

    Parameters
    ----------
    sources : array (k, *shape)
        Signed colour-charge octet components ρ^a (each Σ=0); k = number of
        components, shape = (L,L) or (L,L,L).  Always an explicit stack: pass
        ``rho[None]`` for a single component.
    xi : float
        Condensate coherence length (bag-wall thickness); smaller ξ → stiffer
        bag (type-II), sharper tube.
    eps_floor : float
        Dielectric floor in the condensed vacuum (residual conductivity);
        eps_floor→0 is the ideal dia-electric (full flux expulsion).
    dtau, n_out, sweeps, tol :
        Gradient-flow step, max outer iterations, f-substeps per Poisson solve,
        and the convergence tolerance on the per-step f update.
    f_init : array, optional
        Warm-start condensate (e.g. previous tick's f in the live channel).
        Defaults to the full vacuum f=1.

    Returns
    -------
    dict with keys f, eps_c, D2, psi (last component), energy (4-tuple),
    residual, iters, converged, [history if record].
    """
    sources = np.asarray(sources, float)             # (k, *shape) stack
    shape = sources.shape[1:]

    f = np.ones(shape) if f_init is None else np.clip(np.array(f_init, float), 0.0, 1.0)
    history = [] if record else None
    res = np.inf
    it = 0
    psi = np.zeros(shape)
    D2 = np.zeros(shape)
    for it in range(1, n_out + 1):
        eps = colour_dielectric(f, eps_floor)
        # 1) confined colour-electric flux for each octet component
        D2 = np.zeros(shape)
        for a in range(sources.shape[0]):
            psi, _, _ = dielectric_poisson(sources[a], eps,
                                           tol=poisson_tol, maxit=poisson_maxit)
            D = eps * (-grad(psi))                  # D^a = ε_c E^a
            D2 = D2 + (D * D).sum(axis=0)
        # 2) GL gradient flow of the condensate under the frozen flux
        eps_d2 = np.maximum(eps, 1e-12) ** 2          # guard the back-reaction divisor
        for _ in range(int(sweeps)):
            force = (2.0 * laplacian(f)
                     - (1.0 / xi ** 2) * (f * f - 1.0) * f
                     - f * D2 / eps_d2)
            f = np.clip(f + dtau * force, 0.0, 1.0)
        res = float(np.abs(dtau * force).max())
        if record:
            history.append(res)
        if res < tol and it > 5:
            break
    eps = colour_dielectric(f, eps_floor)
    out = {"f": f, "eps_c": eps, "D2": D2, "psi": psi,
           "energy": gl_energy(f, D2, xi, eps_floor),
           "residual": res, "iters": it, "converged": bool(res < tol)}
    if record:
        out["history"] = history
    return out


def meanfield_bag(sources, lam=2.0, phi0=0.5):
    """The F137 mean-field bag for A/B comparison: ρ=Σ|J| smeared by a *fixed*
    Gaussian λ → f²=exp(−φ/φ0), ε_c=1−f².  One-way (no back-reaction); pinches
    beyond ~2λ.  ``sources`` is the (k,*shape) stack; returns dict f, eps_c."""
    sources = np.asarray(sources, float)             # (k, *shape) stack
    rho = np.sqrt((sources ** 2).sum(axis=0))        # octet magnitude
    shape = rho.shape
    k = [2.0 * np.pi * np.fft.fftfreq(n) for n in shape]
    KK = np.meshgrid(*k, indexing="ij")
    ker = np.exp(-0.5 * lam ** 2 * sum(K ** 2 for K in KK))
    phi = np.clip(np.real(np.fft.ifftn(np.fft.fftn(rho) * ker)), 0.0, None)
    f2 = np.exp(-phi / max(phi0, 1e-12))
    return {"f": np.sqrt(f2), "eps_c": 1.0 - f2, "phi": phi}
