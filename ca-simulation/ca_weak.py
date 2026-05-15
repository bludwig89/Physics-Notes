"""
ca_weak.py  —  SU(2) weak-isospin gauge coupling  (Phase E2)
==============================================================
Extends the Dirac CA so the left-handed component carries an SU(2)
isospin doublet, while the right-handed component is a singlet.  An
SU(2) gauge field W^a_μ acts ONLY on the left-handed doublet — this is
the parity-violating structure of the Standard-Model weak interaction,
and the structure Ludwig speculated about on notebook page 60.

Per-cell state
--------------
  Left doublet:
      eta_nu  = (eta_nu_up, eta_nu_dn)   2 complex numbers — "upper isospin"
      eta_e   = (eta_e_up,  eta_e_dn)    2 complex numbers — "lower isospin"
  Right singlet:
      chi_e   = (chi_e_up,  chi_e_dn)    2 complex numbers

  Total: 6 complex per cell.

In the simplified Standard-Model-without-Higgs we use here:
  - No right-handed neutrino (massless ν).
  - The right-handed electron pairs with eta_e via a mass term m_e·c².
"""

import numpy as np
from ca_core import weyl_step_2d_splitstep


# Pauli matrices reused as SU(2) generators τ^a = σ^a / 2
SIGMA1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA3 = np.array([[1, 0], [0, -1]], dtype=complex)


def gaussian_weak_2d(shape, sigma=4.0, kind='left_nu', center=None):
    """
    Initial conditions for the weak CA.

    kind:
      'left_nu'   — pure left-chirality, isospin-up   (η_ν only)
      'left_e'    — pure left-chirality, isospin-down (η_e only)
      'left_mix'  — equal mix of η_ν and η_e
      'right_e'   — pure right-chirality (χ_e only) — should not couple to W
    """
    Lx, Ly = shape
    cx, cy = center if center is not None else (Lx // 2, Ly // 2)
    x = np.arange(Lx) - cx
    y = np.arange(Ly) - cy
    X, Y = np.meshgrid(x, y, indexing='ij')
    G = np.exp(-(X**2 + Y**2) / (2.0 * sigma**2)).astype(complex)
    z = np.zeros_like(G)

    eta_nu = [z.copy(), z.copy()]
    eta_e  = [z.copy(), z.copy()]
    chi_e  = [z.copy(), z.copy()]

    if kind == 'left_nu':
        eta_nu[0] = G.copy()
    elif kind == 'left_e':
        eta_e[0]  = G.copy()
    elif kind == 'left_mix':
        eta_nu[0] = G / np.sqrt(2.0)
        eta_e[0]  = G / np.sqrt(2.0)
    elif kind == 'right_e':
        chi_e[0]  = G.copy()
    else:
        raise ValueError(kind)
    return eta_nu, eta_e, chi_e


def weak_norm(eta_nu, eta_e, chi_e):
    """Total probability norm."""
    return float(sum(np.sum(np.abs(c)**2)
                     for v in (eta_nu, eta_e, chi_e) for c in v))


def step_weak_2d(eta_nu, eta_e, chi_e,
                  W1, W2, W3,
                  c=0.5, m_e=0.0, g_weak=1.0, dt=1.0):
    """
    One step of the SU(2)-coupled Dirac CA.

    W1, W2, W3 : real arrays (Lx, Ly) — components of the static SU(2)
                 gauge field (one number per cell per generator τ^a).
                 Only the time-component is used here (W^a_0); spatial
                 components would enter the kinetic step.

    Strang-symmetric split:
      half-step SU(2) phase on η (acts on isospin doublet)
      → full kinetic step on each Weyl component separately
      → half-step SU(2) phase on η

    Mass coupling: m_e mixes η_e ↔ χ_e (electron mass).  ν stays massless.
    Implemented as a global rotation of the (η_e_↑, χ_e_↑) and (η_e_↓, χ_e_↓)
    2-spinors at angle m_e·c²·dt.
    """
    Lx, Ly = eta_nu[0].shape

    # ── Half-step SU(2) phase on the left doublet ────────────────────
    # Per-cell SU(2) generator value:  g·dt/2 · (W1·τ1 + W2·τ2 + W3·τ3)
    # τ^a = σ^a / 2 here.
    half = 0.5 * g_weak * dt * 0.5    # factor 0.5 inside is τ = σ/2

    # The combined matrix at each cell is:
    #   M(x) = exp(-i · half · (W1·σ1 + W2·σ2 + W3·σ3))
    # which we compute via:  M = cos(|W|·half)·I − i·sin(|W|·half)·(Ŵ·σ)
    W_mag = np.sqrt(W1**2 + W2**2 + W3**2)
    Wm_safe = np.where(W_mag == 0.0, 1.0, W_mag)
    angle = W_mag * half
    cos_a = np.cos(angle)
    sin_a_norm = np.sin(angle) / Wm_safe

    # Apply to (eta_nu, eta_e) doublet at each cell:
    #   new_nu = cos·old_nu  + (-i·sin·norm)·[(W1−iW2)·old_e + W3·old_nu]
    # actually the standard form:
    #   M = cos·I − i·sin·(Ŵ·σ)
    # Ŵ·σ = (Ŵ1·σ1 + Ŵ2·σ2 + Ŵ3·σ3)
    #     = [[Ŵ3, Ŵ1−iŴ2], [Ŵ1+iŴ2, −Ŵ3]]
    # So M = [[cos − i·sin·Ŵ3,      −i·sin·(Ŵ1−iŴ2)],
    #         [−i·sin·(Ŵ1+iŴ2),  cos + i·sin·Ŵ3]]
    def apply_su2(a, b):
        """a, b are isospin-up and isospin-down arrays."""
        m00 = cos_a - 1j * sin_a_norm * W3
        m01 = -1j * sin_a_norm * (W1 - 1j * W2)
        m10 = -1j * sin_a_norm * (W1 + 1j * W2)
        m11 = cos_a + 1j * sin_a_norm * W3
        return m00 * a + m01 * b, m10 * a + m11 * b

    new_nu_up, new_e_up = apply_su2(eta_nu[0], eta_e[0])
    new_nu_dn, new_e_dn = apply_su2(eta_nu[1], eta_e[1])
    eta_nu = [new_nu_up, new_nu_dn]
    eta_e  = [new_e_up,  new_e_dn]

    # ── Kinetic step on each Weyl 2-spinor ───────────────────────────
    # eta_nu propagates as a massless Weyl spinor.
    # eta_e and chi_e couple via mass — handle as a Dirac pair.
    # For simplicity here, use weyl_step_2d_splitstep on each independently
    # (mass coupling applied as a global rotation below).
    eta_nu[0], eta_nu[1] = weyl_step_2d_splitstep(eta_nu[0], eta_nu[1], c)
    eta_e[0],  eta_e[1]  = weyl_step_2d_splitstep(eta_e[0],  eta_e[1],  c)
    chi_e[0],  chi_e[1]  = weyl_step_2d_splitstep(chi_e[0],  chi_e[1],  c)

    if m_e != 0.0:
        # Mass mixing between left-electron and right-electron components.
        mphase = m_e * c**2 * dt
        cos_m, sin_m = np.cos(mphase), np.sin(mphase)
        new_e_up = cos_m * eta_e[0] - 1j * sin_m * chi_e[0]
        new_x_up = -1j * sin_m * eta_e[0] + cos_m * chi_e[0]
        new_e_dn = cos_m * eta_e[1] - 1j * sin_m * chi_e[1]
        new_x_dn = -1j * sin_m * eta_e[1] + cos_m * chi_e[1]
        eta_e = [new_e_up, new_e_dn]
        chi_e = [new_x_up, new_x_dn]

    # ── Second half-step SU(2) phase on the left doublet ─────────────
    new_nu_up, new_e_up = apply_su2(eta_nu[0], eta_e[0])
    new_nu_dn, new_e_dn = apply_su2(eta_nu[1], eta_e[1])
    eta_nu = [new_nu_up, new_nu_dn]
    eta_e  = [new_e_up,  new_e_dn]

    return eta_nu, eta_e, chi_e


def parity_violation_test(L=32, n_steps=80, c=0.0, m_e=0.0, g_weak=1.0,
                           dt=1.0, W3_value=1.0, sigma=4.0):
    """
    Static W^3 field rotates the (ν, e) isospin doublet at rate g·W^3/2
    for left-chirality, but leaves right-chirality alone.

    Set c=0 to suppress kinetic motion — isolate the gauge rotation cleanly.

    Returns
    -------
    dict with:
      left_rotation_measured : measured angle the (ν, e) doublet rotates
      left_rotation_analytic : g·W^3·dt·n_steps / 2
      right_population_change: should be ≈ 0 (right chirality immune to W)
    """
    shape = (L, L)
    W1 = np.zeros(shape)
    W2 = np.zeros(shape)
    W3 = np.full(shape, W3_value)

    # Left case: start as pure η_ν, see how much rotates into η_e.
    en, ee, xe = gaussian_weak_2d(shape, sigma=sigma, kind='left_nu')
    n_nu_initial = float(np.sum(np.abs(en[0])**2 + np.abs(en[1])**2))
    for _ in range(n_steps):
        en, ee, xe = step_weak_2d(en, ee, xe,
                                   W1, W2, W3,
                                   c=c, m_e=m_e, g_weak=g_weak, dt=dt)
    # With W^3 only, the W^3·σ^3/2 generator gives σ_z eigenvalues ±1/2,
    # so the *isospin populations* don't rotate into each other — they
    # just pick up opposite phases.  To see population mixing, we'd use
    # W^1 or W^2.  Switch to W^1 for this test.

    W1 = np.full(shape, W3_value)
    W3 = np.zeros(shape)
    en, ee, xe = gaussian_weak_2d(shape, sigma=sigma, kind='left_nu')
    for _ in range(n_steps):
        en, ee, xe = step_weak_2d(en, ee, xe,
                                   W1, W2, W3,
                                   c=c, m_e=m_e, g_weak=g_weak, dt=dt)
    n_nu_final = float(np.sum(np.abs(en[0])**2 + np.abs(en[1])**2))
    n_e_final  = float(np.sum(np.abs(ee[0])**2 + np.abs(ee[1])**2))

    # W^1 rotation:  ν → cos(θ)·ν − i·sin(θ)·e
    # populations:   |ν|² = cos²(θ), |e|² = sin²(θ)
    # so total angle θ = g·W^1·dt·n_steps · (1/2)·2 = g·W^1·dt·n_steps · (1/2 · 1)
    # The half from τ = σ/2, but we apply the half-step factor in both
    # halves of Strang split, so the *full* per-step rotation angle is
    # g·W^1·dt · (1/2) · 2·(half) = g·W^1·dt·(1/2)
    # Wait — let me recompute.  half = 0.5 · g · dt · 0.5 (factor 0.5 inside is τ=σ/2)
    # so half = 0.25·g·dt.  Total rotation in one full step (two half-steps)
    # is 2·half = 0.5·g·dt.  Times n_steps gives 0.5·g·W^1·dt·n_steps.
    theta_analytic = 0.5 * g_weak * W3_value * dt * n_steps
    # Population in η_e after rotation by θ:  sin²(θ)
    pop_e_analytic = np.sin(theta_analytic)**2 * n_nu_initial

    # Right case: start as pure χ, see if it rotates (it shouldn't).
    en2, ee2, xe2 = gaussian_weak_2d(shape, sigma=sigma, kind='right_e')
    n_chi_initial = float(np.sum(np.abs(xe2[0])**2 + np.abs(xe2[1])**2))
    for _ in range(n_steps):
        en2, ee2, xe2 = step_weak_2d(en2, ee2, xe2,
                                      W1, W2, W3,
                                      c=c, m_e=m_e, g_weak=g_weak, dt=dt)
    n_chi_final = float(np.sum(np.abs(xe2[0])**2 + np.abs(xe2[1])**2))
    # χ should be invariant under W (parity violation):
    pop_left_from_right = float(np.sum(
        np.abs(en2[0])**2 + np.abs(en2[1])**2 +
        np.abs(ee2[0])**2 + np.abs(ee2[1])**2))

    return {
        'left_theta_analytic':  theta_analytic,
        'left_e_pop_measured':  n_e_final,
        'left_e_pop_analytic':  pop_e_analytic,
        'left_nu_pop_measured': n_nu_final,
        'left_nu_pop_initial':  n_nu_initial,
        'right_chi_pop_initial': n_chi_initial,
        'right_chi_pop_final':   n_chi_final,
        'right_leakage_to_left': pop_left_from_right,
    }
