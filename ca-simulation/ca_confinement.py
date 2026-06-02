"""
ca_confinement.py — Static quark potential, string tension, confinement  (FG-7c)
================================================================================

Created: 2026-06-01

Delivers the confinement *measurement* layer on top of the Wilson-loop
primitives in `ca_gluon.py` and the gradient-flow smoother in `ca_cooling.py`.
This is the second half of the F43/FG-7 follow-up: showing that the lattice
gauge sector produces a **linear static quark potential** — the statement that
an isolated colour charge costs infinite energy, i.e. *why a quark cannot exist
alone*.

Why 2D is the right testbed
---------------------------
In two Euclidean dimensions, SU(N) lattice gauge theory is exactly solvable:
after gauge-fixing to the axial gauge U_x ≡ I, the plaquette variables are
independent, and a Wilson loop enclosing area A = R·T factorises.  Using
Schur's lemma — the single-plaquette mean of a *class-invariant* distribution
is ⟨U⟩ = w·I with w = ⟨(1/N)Re Tr U⟩ — the loop expectation is **exactly**

        ⟨(1/N) Re Tr W(R,T)⟩ = w(β)^{R·T}            (exact area law)

so the string tension, Creutz ratio, and static potential are known in closed
form for *all* couplings:

        σ(β)   = −ln w(β)                       (string tension)
        χ(R,T) = σ                              (Creutz ratio, R,T-independent)
        V(R)   = −lim_{T→∞} (1/T) ln⟨W(R,T)⟩ = σ·R   (linear potential)

σ(β) > 0 for every finite β: 2D gauge theory confines at all couplings.
The single-plaquette mean w(β) is computed deterministically by SU(3)
Weyl-torus quadrature (machine precision), so σ, χ and V are exact.

A light Metropolis sampler is included to cross-check the analytic area law on
a full 2D lattice; a heavier version lives in `model-tests/run_confinement_mc.py`.

Coupling convention (standard Wilson normalisation)
---------------------------------------------------
The full-lattice Wilson action is  S = β Σ_□ (1 − (1/N) Re Tr U_□).  In 2D
axial gauge the path integral factorises into independent single-plaquette
integrals each weighted by exp((β/N) Re Tr U_□), so

    dμ_β(U) ∝ exp((β/N) · Re Tr U) dU_Haar ,   w(β) = ⟨(1/N) Re Tr U⟩ ,  N = 3.

With this normalisation `plaquette_mean(β)` matches the lattice Metropolis
mean plaquette at the *same* β directly (verified in test FG7c CF6).
"""

import numpy as np

import ca_strong as cstr
import ca_gluon as cg
import ca_cooling as cc


# ══════════════════════════════════════════════════════════════════
#  Single-plaquette mean  w(β)  via exact SU(3) Weyl-torus quadrature
# ══════════════════════════════════════════════════════════════════

def _weyl_grids(n_grid):
    """φ1, φ2 grid on the SU(3) maximal torus (φ3 = −φ1−φ2)."""
    phi = np.linspace(0.0, 2.0 * np.pi, n_grid, endpoint=False)
    P1, P2 = np.meshgrid(phi, phi, indexing='ij')
    P3 = -(P1 + P2)
    return P1, P2, P3


def _weyl_measure(P1, P2, P3):
    """|Δ|² = ∏_{i<j} |e^{iφ_i} − e^{iφ_j}|² = ∏ 2(1 − cos(φ_i − φ_j))."""
    d12 = 2.0 * (1.0 - np.cos(P1 - P2))
    d13 = 2.0 * (1.0 - np.cos(P1 - P3))
    d23 = 2.0 * (1.0 - np.cos(P2 - P3))
    return d12 * d13 * d23


def plaquette_mean(beta, n_grid=240, n_c=3):
    """
    w(β) = ⟨(1/N) Re Tr U⟩ for the single-plaquette Wilson distribution
    dμ_β ∝ exp((β/N)·Re Tr U) dU, computed by deterministic Weyl-torus
    quadrature (standard Wilson coupling normalisation, N=3).

    Periodic integrand → the rectangle rule is spectrally (exponentially)
    accurate; n_grid≈240 reaches machine precision.  Returns a float in (0, 1).

    Exact limits:  w(0) = 0   (⟨Tr U⟩_Haar = 0 for SU(3));   w(∞) → 1.
    """
    P1, P2, P3 = _weyl_grids(n_grid)
    meas = _weyl_measure(P1, P2, P3)
    ReTr = np.cos(P1) + np.cos(P2) + np.cos(P3)
    weight = meas * np.exp((beta / n_c) * ReTr)
    Z = np.sum(weight)
    num = np.sum((ReTr / 3.0) * weight)
    return float(num / Z)


def plaquette_mean_complex(beta, n_grid=240, n_c=3):
    """
    Complex ⟨(1/N) Tr U⟩ for the single-plaquette distribution.

    By the Weyl-measure φ↔−φ symmetry the imaginary part vanishes exactly, so
    ⟨(1/N)Tr U⟩ is real and equals w(β).  Together with Schur's lemma this is
    the deterministic statement ⟨U⟩ = w·I that drives the exact area law.
    Returns a complex number (Im ≈ machine ε).
    """
    P1, P2, P3 = _weyl_grids(n_grid)
    meas = _weyl_measure(P1, P2, P3)
    ReTr = np.cos(P1) + np.cos(P2) + np.cos(P3)
    TrU = (np.exp(1j * P1) + np.exp(1j * P2) + np.exp(1j * P3)) / n_c
    weight = meas * np.exp((beta / n_c) * ReTr)
    return complex(np.sum(TrU * weight) / np.sum(weight))


def string_tension(beta, n_grid=240):
    """σ(β) = −ln w(β)  (lattice units).  Positive for every finite β."""
    w = plaquette_mean(beta, n_grid=n_grid)
    return float(-np.log(w))


# ══════════════════════════════════════════════════════════════════
#  Exact area law, Creutz ratio, static potential
# ══════════════════════════════════════════════════════════════════

def area_law_loops(w, r_max=5, t_max=5):
    """Exact loop expectations ⟨(1/N)Re Tr W(R,T)⟩ = w^{R·T}."""
    return {(r, t): w ** (r * t)
            for r in range(1, r_max + 1) for t in range(1, t_max + 1)}


def creutz_ratio(loops, r, t):
    """
    χ(R,T) = −ln[ W(R,T)·W(R−1,T−1) / (W(R−1,T)·W(R,T−1)) ].

    `loops` is a dict (R,T) → ⟨W(R,T)⟩.  For an exact area law W = w^{RT},
    χ(R,T) = −ln w = σ for every R,T ≥ 2 (the cleanest confinement signature).
    """
    num = loops[(r, t)] * loops[(r - 1, t - 1)]
    den = loops[(r - 1, t)] * loops[(r, t - 1)]
    return float(-np.log(num / den))


def static_potential_from_loops(loops, r, t):
    """
    V(R) from the temporal decay of the Wilson loop:
        V(R) = −(1/T) ln[ W(R,T) / W(R,T−1) ]   (one-step estimator).
    For the exact area law this equals σ·R for every T (T-independent).
    """
    return float(-np.log(loops[(r, t)] / loops[(r, t - 1)]))


def static_potential_linear(w, r):
    """Closed-form static potential V(R) = σ·R with σ = −ln w."""
    return float(-np.log(w) * r)


# ══════════════════════════════════════════════════════════════════
#  Metropolis sampler (full 2D lattice) — MC cross-check of the area law
# ══════════════════════════════════════════════════════════════════

def _staple_at(U, mu, x, y):
    """Single-site staple sum Σ_μ(x,y) (small helper for local Metropolis)."""
    Sigma = cc.staple_sum_2d(U)        # (2, Lx, Ly, 3, 3)
    return Sigma[mu, x, y]


def metropolis_sweep_2d(U, beta, rng, eps=0.3, n_hit=2):
    """
    One Metropolis sweep over all links of the 2D-square SU(3) lattice.

    Proposal U → R·U with R = su3_exp(eps·θ), θ~N(0,1)^8; accept with
    probability min(1, exp(−ΔS)), ΔS = −(β/N) Re Tr[(U_new−U_old) Σ†].
    Returns (U_updated, acceptance_rate).
    """
    Lx, Ly = U.shape[1:3]
    n_acc = 0
    n_tot = 0
    for mu in range(2):
        for x in range(Lx):
            for y in range(Ly):
                Sigma = _staple_at(U, mu, x, y)
                for _ in range(n_hit):
                    R = cstr.su3_exp(eps * rng.standard_normal(8))
                    U_old = U[mu, x, y]
                    U_new = R @ U_old
                    dS = -(beta / 3.0) * np.real(
                        np.trace((U_new - U_old) @ np.conj(Sigma.T)))
                    if dS <= 0 or rng.random() < np.exp(-dS):
                        U[mu, x, y] = U_new
                        n_acc += 1
                    n_tot += 1
    return U, n_acc / n_tot


def single_plaquette_mean_matrix(beta, n_samples=4000, eps=0.3, seed=99, n_c=3):
    """
    Monte-Carlo estimate of ⟨U⟩ for the single-plaquette distribution
    dμ_β ∝ exp((β/N)·Re Tr U) dU (Metropolis on one SU(3) matrix).

    Schur's lemma forces ⟨U⟩ = w·I (the engine of the 2D area law): the
    class-invariant single-plaquette mean is proportional to the identity,
    with coefficient w = ⟨(1/N)Re Tr U⟩.  Returns (mean_matrix, w_mc).
    """
    rng = np.random.default_rng(seed)
    U = np.eye(3, dtype=complex)
    acc = np.zeros((3, 3), dtype=complex)
    tr = []
    n_keep = 0
    for s in range(n_samples + 500):
        R = cstr.su3_exp(eps * rng.standard_normal(8))
        U_new = R @ U
        dS = -(beta / n_c) * np.real(np.trace(U_new - U))
        if dS <= 0 or rng.random() < np.exp(-dS):
            U = U_new
        if s >= 500:                       # discard burn-in
            acc += U
            tr.append(np.real(np.trace(U)) / n_c)
            n_keep += 1
    return acc / n_keep, float(np.mean(tr))


def mc_wilson_loops(beta, L=6, n_therm=80, n_meas=120, r_max=3, t_max=3,
                    eps=0.3, seed=1234, measure_every=2):
    """
    Monte-Carlo estimate of ⟨(1/N)Re Tr W(R,T)⟩ on an L×L lattice at coupling β.

    Returns dict (R,T) → mean loop, plus the measured single-plaquette mean.
    Light defaults so it finishes inside a sandbox tick; use
    `model-tests/run_confinement_mc.py` for production statistics.
    """
    rng = np.random.default_rng(seed)
    U = cstr.cold_links_2d((L, L))
    for _ in range(n_therm):
        U, _ = metropolis_sweep_2d(U, beta, rng, eps=eps)

    acc = {(r, t): [] for r in range(1, r_max + 1) for t in range(1, t_max + 1)}
    plaq = []
    n_done = 0
    for s in range(n_meas):
        U, _ = metropolis_sweep_2d(U, beta, rng, eps=eps)
        if s % measure_every:
            continue
        n_done += 1
        plaq.append(cc.mean_plaquette_2d(U))
        for (r, t) in acc:
            acc[(r, t)].append(cg.wilson_loop_2d_avg(U, r, t) / 3.0)
    loops = {k: float(np.mean(v)) for k, v in acc.items()}
    return loops, float(np.mean(plaq)), n_done
