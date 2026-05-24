"""
test_su3_noether.py — V13 strong-sector gate

Tests for the SU(3) colour gauge sector implemented in `ca_strong.py`.
Implements the four gates defined in `reference-research/ca-strong-design.md`:

  V13a  — cold-link vacuum regression (bit-for-bit vs. colourless Dirac)
  V13b1 — local Noether current conservation (per-cell 4-divergence)
  V13b2 — global colour charge conservation
  V13b3 — global SU(3) gauge invariance (adjoint rotation of Q^a)
  V13b4 — local SU(3) gauge invariance of observables

Run from the ca-simulation/ directory:
    python test_su3_noether.py

Reports residuals and PASS/FAIL by tolerance.
"""

import json
import time
from pathlib import Path

import numpy as np

import ca_dirac as cdir
import ca_strong as cs


# ══════════════════════════════════════════════════════════════════
#  Gate G0 — generator algebra sanity check
# ══════════════════════════════════════════════════════════════════

def gate_G0_generator_algebra():
    """Check Tr(T^a T^b) = ½ δ^{ab} and basic Hermiticity of generators."""
    print("─" * 70)
    print("G0 Generator algebra")
    print("─" * 70)

    norm_residual = cs.verify_normalization()
    print(f"  max|Tr(T^a T^b) − ½ δ^ab|        = {norm_residual:.3e}")

    herm_residual = max(
        float(np.max(np.abs(cs.T(a + 1) - cs.T(a + 1).conj().T)))
        for a in range(cs.N_GEN)
    )
    print(f"  max|T^a − (T^a)†|                = {herm_residual:.3e}")

    # Verify SU(3) closure under a random exponential.
    rng = np.random.default_rng(seed=42)
    theta = rng.uniform(-np.pi, np.pi, size=8)
    V = cs.su3_exp(theta)
    su3_check = cs.is_su3(V, tol=1e-12)
    err_unit = float(np.max(np.abs(V @ V.conj().T - np.eye(3))))
    err_det = abs(np.linalg.det(V) - 1.0)
    print(f"  exp(iθ^a T^a) ∈ SU(3)?           {su3_check}")
    print(f"    err V V† − I                   = {err_unit:.3e}")
    print(f"    err det V − 1                  = {err_det:.3e}")

    haar_check = True
    rng2 = np.random.default_rng(seed=7)
    for _ in range(5):
        H = cs.su3_haar(rng2)
        haar_check = haar_check and cs.is_su3(H, tol=1e-12)
    print(f"  5 Haar draws all ∈ SU(3)?        {haar_check}")

    passed = (
        norm_residual < 1e-14
        and herm_residual < 1e-15
        and su3_check
        and haar_check
    )
    print(f"  G0 result                        {'PASS' if passed else 'FAIL'}")
    return {
        'norm_residual': norm_residual,
        'hermiticity_residual': herm_residual,
        'su3_unitarity_residual': err_unit,
        'su3_determinant_residual': err_det,
        'passed': passed,
    }


# ══════════════════════════════════════════════════════════════════
#  Gate V13a — cold-link vacuum regression
# ══════════════════════════════════════════════════════════════════

def gate_V13a_cold_link_regression(L=32, n_steps=20, m=0.5):
    """
    Cold links (U_μ ≡ I) must reduce step_strong_2d bit-for-bit to
    three independent colour copies of the colourless Dirac step.

    Setup: single Gaussian in (u, r) channel, left chirality.
    Run two evolutions in parallel:
      A) `step_strong_2d` with cold links, just the (u, r) channel evolves.
      B) `dirac_step_2d_splitstep` on the same initial (η_↑, η_↓, χ_↑, χ_↓).
    Compare bit-for-bit at every step.
    """
    print("─" * 70)
    print(f"V13a Cold-link vacuum regression  (L={L}, n_steps={n_steps}, m={m})")
    print("─" * 70)
    shape = (L, L)
    rng = np.random.default_rng(seed=0)
    # Gaussian initial packet in (u, r) only.
    q = cs.gaussian_quark(shape, flavour='u', colour='r',
                          sigma=3.0, chirality='left')
    U = cs.cold_links_2d(shape)

    # Reference: same Gaussian as a 4-component colourless Dirac packet.
    eu_ref, ed_ref, cu_ref, cd_ref = cdir.gaussian_dirac_2d(
        shape, sigma=3.0, chirality='left'
    )

    max_diff = 0.0
    for step in range(n_steps):
        q = cs.step_strong_2d(q, U, m_flavour={'u': m, 'd': m, 's': m})
        eu_ref, ed_ref, cu_ref, cd_ref = cdir.dirac_step_2d_splitstep(
            eu_ref, ed_ref, cu_ref, cd_ref, m=m
        )
        # Compare (u, r) channel against the reference.
        d_eu = np.max(np.abs(q[('u', 'r', 'eu')] - eu_ref))
        d_ed = np.max(np.abs(q[('u', 'r', 'ed')] - ed_ref))
        d_cu = np.max(np.abs(q[('u', 'r', 'cu')] - cu_ref))
        d_cd = np.max(np.abs(q[('u', 'r', 'cd')] - cd_ref))
        max_diff = max(max_diff, d_eu, d_ed, d_cu, d_cd)

    # The other channels must remain identically zero.
    other_norm = 0.0
    for f in cs.FLAVOURS:
        for c in cs.COLOURS:
            for d in cs.DIRAC:
                if (f, c) == ('u', 'r'):
                    continue
                other_norm = max(other_norm, float(np.max(np.abs(q[(f, c, d)]))))

    print(f"  max|q[(u,r,·)] − dirac_ref|      = {max_diff:.3e}")
    print(f"  max|other (flavour,colour)|      = {other_norm:.3e}")
    passed = (max_diff < 1e-14) and (other_norm < 1e-15)
    print(f"  V13a result                      {'PASS' if passed else 'FAIL'}")
    return {
        'max_diff_vs_dirac': float(max_diff),
        'other_channels_max': float(other_norm),
        'passed': passed,
    }


# ══════════════════════════════════════════════════════════════════
#  Gate V13b2 — global charge conservation (cold links)
# ══════════════════════════════════════════════════════════════════

def gate_V13b2_global_charge_conservation(L=32, n_steps=200, m=0.3):
    """
    For cold links, Q^a = Σ_x J^a_0(x) is conserved by the unitary
    kinetic step (it's a global SU(3) generator on free Dirac).  Should
    drift only at the FFT round-off rate.

    Initial: mixed quark packet (u, r) and (u, g) — non-trivial Q^a.
    """
    print("─" * 70)
    print(f"V13b2 Global charge conservation (cold links)  (L={L}, n={n_steps})")
    print("─" * 70)
    shape = (L, L)
    q1 = cs.gaussian_quark(shape, flavour='u', colour='r',
                           sigma=3.0, chirality='left')
    q2 = cs.gaussian_quark(shape, flavour='u', colour='g',
                           sigma=3.0, chirality='left')
    # Sum the two packets (still in 'q1' container)
    for key in q1:
        q1[key] = q1[key] + q2[key]
    U = cs.cold_links_2d(shape)

    Q0 = cs.noether_charge_total(q1)
    norm0 = cs.quark_norm(q1)

    q = q1
    drift_max = 0.0
    norm_drift_max = 0.0
    for step in range(n_steps):
        q = cs.step_strong_2d(q, U, m_flavour={'u': m, 'd': m, 's': m})
        Q = cs.noether_charge_total(q)
        drift_max = max(drift_max, float(np.max(np.abs(Q - Q0))))
        norm_drift_max = max(norm_drift_max, abs(cs.quark_norm(q) - norm0))

    # Use the per-charge scale for context.
    Q0_scale = float(np.max(np.abs(Q0))) if np.max(np.abs(Q0)) > 0 else 1.0
    print(f"  initial |Q^a| range              = {np.min(np.abs(Q0)):.3e} … "
          f"{np.max(np.abs(Q0)):.3e}")
    print(f"  max|Q(t) − Q(0)| over {n_steps} steps  = {drift_max:.3e}")
    print(f"  norm drift over {n_steps} steps        = {norm_drift_max:.3e}")
    passed = drift_max < 1e-11
    print(f"  V13b2 result                     {'PASS' if passed else 'FAIL'}")
    return {
        'charge_drift_max': float(drift_max),
        'norm_drift_max': float(norm_drift_max),
        'Q_initial_scale': Q0_scale,
        'passed': passed,
    }


# ══════════════════════════════════════════════════════════════════
#  Gate V13b1 — per-cell lattice 4-divergence (informational)
# ══════════════════════════════════════════════════════════════════

def gate_V13b1_per_cell_divergence(L=32, m=0.3):
    """
    Centered-difference lattice 4-divergence

      (∂_μ J^a_μ)(x) ≈ ½ (J^a_0(x, t+1) − J^a_0(x, t-1))
                     + ½ Σ_i (J^a_i(x+î) − J^a_i(x-î))

    For the QCA Dirac propagator this is *not* expected to vanish at
    the FFT floor — the QCA's exact conservation law involves the
    arccos dispersion, not naive centered differences.  The centered-
    difference residual scales with the wave-packet's k-content
    (O(k^2) truncation error).  This gate measures the magnitude and
    reports the max, mean, and ratio to J^a_0.  Informational only;
    no hard threshold.
    """
    print("─" * 70)
    print(f"V13b1 Per-cell 4-divergence (informational)  (L={L}, m={m})")
    print("─" * 70)
    shape = (L, L)
    q = cs.gaussian_quark(shape, flavour='u', colour='r',
                          sigma=3.0, chirality='left')
    # Add g-channel for non-trivial off-diagonal currents.
    q[('u', 'g', 'eu')] = q[('u', 'r', 'eu')] * 0.4
    U = cs.cold_links_2d(shape)

    # Measure J^a_0(t-1), J^a_0(t+1), J^a_i(t) around a centered step.
    m_dict = {'u': m, 'd': m, 's': m}

    # Advance one step to get t=1 state, then take that as the centered t.
    q_tm1 = q
    q_t = cs.step_strong_2d({k: v.copy() for k, v in q_tm1.items()},
                            U, m_flavour=m_dict)
    q_tp1 = cs.step_strong_2d({k: v.copy() for k, v in q_t.items()},
                              U, m_flavour=m_dict)

    J0_tm1 = cs.noether_charge_density(q_tm1)
    J0_tp1 = cs.noether_charge_density(q_tp1)
    Jspat_t = cs.noether_current_spatial(q_t)

    div = cs.lattice_3divergence(J0_tm1, J0_tp1, Jspat_t, dt=1.0)
    J0_t = cs.noether_charge_density(q_t)

    div_max = float(np.max(np.abs(div)))
    div_mean = float(np.mean(np.abs(div)))
    J0_scale = float(np.max(np.abs(J0_t)))
    print(f"  max|J^a_0|                       = {J0_scale:.3e}")
    print(f"  max|(∂_μ J^a_μ)(x)|              = {div_max:.3e}")
    print(f"  mean|(∂_μ J^a_μ)(x)|             = {div_mean:.3e}")
    print(f"  ratio max(div)/max(J^a_0)        = {div_max / max(J0_scale, 1e-30):.3e}")
    # No hard threshold; we expect O(k^2) truncation, not FFT floor.
    passed = True  # informational only
    print(f"  V13b1 result                     INFO (no hard threshold)")
    return {
        'div_max': div_max,
        'div_mean': div_mean,
        'J0_scale': J0_scale,
        'ratio': div_max / max(J0_scale, 1e-30),
        'passed': passed,
        'gate_type': 'informational',
    }


# ══════════════════════════════════════════════════════════════════
#  Gate V13b3 — global SU(3) adjoint rotation
# ══════════════════════════════════════════════════════════════════

def gate_V13b3_global_su3_adjoint(L=32):
    """
    Apply global SU(3) rotation q → V q, V ∈ SU(3) constant.  Check that
    Q^a → V_adj^{ab} Q^b where V_adj = 2 Tr(T^a V T^b V†).
    """
    print("─" * 70)
    print(f"V13b3 Global SU(3) adjoint rotation of Q^a  (L={L})")
    print("─" * 70)
    shape = (L, L)
    # Build a quark state with components in all 3 colours so Q^a has
    # diverse coefficients.
    q = cs.zero_quark_field(shape)
    rng = np.random.default_rng(seed=11)
    Lx, Ly = shape
    cx, cy = Lx // 2, Ly // 2
    x = np.arange(Lx) - cx
    y = np.arange(Ly) - cy
    X, Y = np.meshgrid(x, y, indexing='ij')
    G = np.exp(-(X**2 + Y**2) / (2.0 * 3.0**2)).astype(complex)
    # Random unit-norm 3-spinor per Dirac component.
    for d in cs.DIRAC:
        coeffs = rng.normal(size=3) + 1j * rng.normal(size=3)
        coeffs /= np.linalg.norm(coeffs)
        for i, c in enumerate(cs.COLOURS):
            q[('u', c, d)] = coeffs[i] * G

    Q0 = cs.noether_charge_total(q)

    # Random SU(3) rotation.
    theta = rng.uniform(-1.0, 1.0, size=8)
    V = cs.su3_exp(theta)

    # Apply as a constant gauge transformation (same V at every cell).
    Vfield = np.broadcast_to(V[np.newaxis, np.newaxis, :, :], (Lx, Ly, 3, 3)).copy()
    q_rot = cs.gauge_transform_quark(q, Vfield)
    Q_rot_measured = cs.noether_charge_total(q_rot)

    # Predicted: Q_a^new = V_adj^{ab} Q_b
    Vadj = cs.adjoint_rotation(V)
    Q_rot_predicted = Vadj @ Q0

    residual = float(np.max(np.abs(Q_rot_measured - Q_rot_predicted)))
    Q_scale = float(np.max(np.abs(Q0)))
    print(f"  |Q(0)| max                       = {Q_scale:.3e}")
    print(f"  max|Q_measured − V_adj·Q|        = {residual:.3e}")
    print(f"  relative residual                = {residual / max(Q_scale, 1e-30):.3e}")
    passed = residual < 1e-12
    print(f"  V13b3 result                     {'PASS' if passed else 'FAIL'}")
    return {
        'adjoint_residual': residual,
        'Q_scale': Q_scale,
        'passed': passed,
    }


# ══════════════════════════════════════════════════════════════════
#  Gate V13b4 — local SU(3) gauge invariance
# ══════════════════════════════════════════════════════════════════

def gate_V13b4_local_su3_invariance(L=32, n_steps=20, m=0.3):
    """
    Apply a per-cell SU(3) rotation to (q, U) consistently:
        q(x) → V(x) q(x)
        U_μ(x) → V(x) U_μ(x) V†(x+μ̂)
    Evolve both the rotated and unrotated states for n_steps; check
    that gauge-invariant observables (quark norm, plaquette traces)
    match.
    """
    print("─" * 70)
    print(f"V13b4 Local SU(3) gauge invariance  (L={L}, n={n_steps}, m={m})")
    print("─" * 70)
    shape = (L, L)

    # Setup: random-link background + Gaussian quark packet.
    rng = np.random.default_rng(seed=23)
    q = cs.gaussian_quark(shape, flavour='u', colour='r',
                          sigma=3.0, chirality='left')
    # Add a colour-g component as well so the test is non-trivial.
    q[('u', 'g', 'eu')] = q[('u', 'r', 'eu')] * 0.6

    U = cs.random_su3_links_2d(shape, rng=rng)

    # Random per-cell V(x) ∈ SU(3).
    Lx, Ly = shape
    Vfield = np.zeros((Lx, Ly, 3, 3), dtype=complex)
    for i in range(Lx):
        for j in range(Ly):
            Vfield[i, j] = cs.su3_haar(rng)

    # Gauge-transform the initial state.
    q_rot = cs.gauge_transform_quark(q, Vfield)
    U_rot = cs.gauge_transform_links(U, Vfield)

    # Reference invariants at t = 0.
    norm0 = cs.quark_norm(q)
    norm0_rot = cs.quark_norm(q_rot)
    plaq0 = float(np.sum(np.real(cs.plaquette_trace(U, mu=0, nu=1))))
    plaq0_rot = float(np.sum(np.real(cs.plaquette_trace(U_rot, mu=0, nu=1))))

    print(f"  norm(q) initial                  = {norm0:.6e}")
    print(f"  norm(q_rot) initial              = {norm0_rot:.6e}")
    print(f"  |norm(q) − norm(q_rot)| t=0      = {abs(norm0 - norm0_rot):.3e}")
    print(f"  Σ Re Tr U_□ initial              = {plaq0:.6e}")
    print(f"  Σ Re Tr U_□_rot initial          = {plaq0_rot:.6e}")
    print(f"  |Σ Re Tr ΔU_□| t=0               = {abs(plaq0 - plaq0_rot):.3e}")

    # Now evolve both.
    m_dict = {'u': m, 'd': m, 's': m}
    norm_diff_max = abs(norm0 - norm0_rot)
    plaq_diff_max = abs(plaq0 - plaq0_rot)

    q_evol = q
    q_rot_evol = q_rot
    for step in range(n_steps):
        q_evol = cs.step_strong_2d(q_evol, U, m_flavour=m_dict)
        q_rot_evol = cs.step_strong_2d(q_rot_evol, U_rot, m_flavour=m_dict)
        norm_diff_max = max(
            norm_diff_max, abs(cs.quark_norm(q_evol) - cs.quark_norm(q_rot_evol))
        )

    plaq_final = float(np.sum(np.real(cs.plaquette_trace(U, mu=0, nu=1))))
    plaq_final_rot = float(np.sum(np.real(cs.plaquette_trace(U_rot, mu=0, nu=1))))
    plaq_diff_max = max(plaq_diff_max, abs(plaq_final - plaq_final_rot))

    print(f"  max|norm(q) − norm(q_rot)|       = {norm_diff_max:.3e}")
    print(f"  max|Σ Re Tr ΔU_□|                = {plaq_diff_max:.3e}")
    passed = (norm_diff_max < 1e-11) and (plaq_diff_max < 1e-10)
    print(f"  V13b4 result                     {'PASS' if passed else 'FAIL'}")
    return {
        'norm_diff_max': float(norm_diff_max),
        'plaq_diff_max': float(plaq_diff_max),
        'passed': passed,
    }


# ══════════════════════════════════════════════════════════════════
#  Gate V13c — Yukawa per-cell mass wiring
# ══════════════════════════════════════════════════════════════════

def gate_V13c_yukawa_wiring(L=32, n_steps=50, y=0.3, v=0.7):
    """
    V13c — Quark Yukawa wiring via per-cell Higgs field.

    V13c.1 (uniform Φ regression):
        For a spatially uniform Φ(x) = v (real), the phi_field path
        must reproduce the scalar m_flavour path bit-for-bit:
            step_strong_2d(..., phi_field=v_array, yukawa={'u': y, ...})
              ≡  step_strong_2d(..., m_flavour={'u': y*v, ...})
        Max absolute deviation must be 0 (double-precision bit identity).

    V13c.2 (charge conservation with spatially varying Φ):
        For phi_field drawn from a smooth random field, the total
        colour charge Q^a must be conserved to FFT-floor precision
        over n_steps steps.  Tolerance 1e-10 per step.

    Parameters
    ----------
    L       : lattice side (default 32)
    n_steps : steps for V13c.2 conservation run (default 50)
    y       : Yukawa coupling used for both sub-tests (default 0.3)
    v       : uniform VEV used in V13c.1 (default 0.7)
    """
    print("─" * 70)
    print("V13c Yukawa per-cell mass wiring")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed=99)
    U_cold = cs.cold_links_2d(shape)
    q0 = cs.gaussian_quark(shape, flavour='u', colour='r', sigma=4.0)
    yukawa_dict = {'u': y, 'd': y * 0.9, 's': y * 0.8}

    # ──────────────────────────────────────────────
    # V13c.1  Uniform-Φ regression
    # ──────────────────────────────────────────────
    print("  V13c.1  uniform-Φ regression")

    # Scalar reference
    m_flat = {f: yukawa_dict[f] * v for f in cs.FLAVOURS}
    q_scalar = cs.step_strong_2d(
        {k: arr.copy() for k, arr in q0.items()},
        U_cold,
        m_flavour=m_flat,
        dt=1.0,
    )

    # Yukawa path with uniform Phi = v (real)
    phi_uniform = np.full(shape, v, dtype=complex)
    q_yukawa = cs.step_strong_2d(
        {k: arr.copy() for k, arr in q0.items()},
        U_cold,
        phi_field=phi_uniform,
        yukawa=yukawa_dict,
        dt=1.0,
    )

    max_dev_v13c1 = max(
        float(np.max(np.abs(q_scalar[k] - q_yukawa[k])))
        for k in q0.keys()
    )
    tol_v13c1 = 0.0   # must be bit-exact (δm = 0 path)
    pass_v13c1 = (max_dev_v13c1 == tol_v13c1)
    print(f"    max|q_scalar − q_yukawa|         = {max_dev_v13c1:.3e}  "
          f"{'PASS' if pass_v13c1 else 'FAIL'}")

    # ──────────────────────────────────────────────
    # V13c.2  Charge conservation with varying Φ
    # ──────────────────────────────────────────────
    print("  V13c.2  charge conservation, varying Φ")

    # Smooth random Phi: low-k Fourier modes only (wavelength ≥ L/4)
    # Build in k-space and transform back.
    k_cutoff = L // 4
    phi_k = np.zeros(shape, dtype=complex)
    for kx in range(-k_cutoff, k_cutoff + 1):
        for ky in range(-k_cutoff, k_cutoff + 1):
            phi_k[kx % L, ky % L] += (rng.standard_normal() +
                                       1j * rng.standard_normal())
    phi_var = np.fft.ifft2(phi_k).real.astype(complex)
    # Scale so |Re Φ| ≤ 0.9 (stay inside QCA admissibility)
    phi_var = phi_var * (0.9 / np.max(np.abs(phi_var.real)))

    q_c2 = {k: arr.copy() for k, arr in q0.items()}
    Q0 = cs.noether_charge_total(q_c2)

    max_drift = 0.0
    for _ in range(n_steps):
        q_c2 = cs.step_strong_2d(
            q_c2, U_cold,
            phi_field=phi_var,
            yukawa=yukawa_dict,
            dt=1.0,
        )
        dQ = np.max(np.abs(cs.noether_charge_total(q_c2) - Q0))
        if dQ > max_drift:
            max_drift = dQ

    tol_v13c2 = 1e-10 * n_steps
    pass_v13c2 = (max_drift <= tol_v13c2)
    print(f"    max|ΔQ^a| over {n_steps} steps            = {max_drift:.3e}  "
          f"(tol {tol_v13c2:.0e})  {'PASS' if pass_v13c2 else 'FAIL'}")

    passed = pass_v13c1 and pass_v13c2
    print(f"  V13c overall: {'PASS' if passed else 'FAIL'}")
    return {
        'passed': passed,
        'v13c1_max_dev': max_dev_v13c1,
        'v13c1_pass': pass_v13c1,
        'v13c2_max_charge_drift': max_drift,
        'v13c2_tol': tol_v13c2,
        'v13c2_pass': pass_v13c2,
    }


# ══════════════════════════════════════════════════════════════════
#  Driver
# ══════════════════════════════════════════════════════════════════

def main():
    t0 = time.time()
    results = {}

    results['G0_generator_algebra'] = gate_G0_generator_algebra()
    results['V13a_cold_link_regression'] = gate_V13a_cold_link_regression(
        L=32, n_steps=20, m=0.5
    )
    results['V13b1_per_cell_divergence'] = gate_V13b1_per_cell_divergence(
        L=32, m=0.3
    )
    results['V13b2_global_charge'] = gate_V13b2_global_charge_conservation(
        L=32, n_steps=200, m=0.3
    )
    results['V13b3_global_adjoint'] = gate_V13b3_global_su3_adjoint(L=32)
    results['V13b4_local_invariance'] = gate_V13b4_local_su3_invariance(
        L=16, n_steps=20, m=0.3
    )
    results['V13c_yukawa_wiring'] = gate_V13c_yukawa_wiring(
        L=32, n_steps=50, y=0.3, v=0.7
    )

    elapsed = time.time() - t0
    print("─" * 70)
    print(f"Total wall time: {elapsed:.1f} s")
    print("─" * 70)
    passed_count = sum(1 for r in results.values() if r['passed'])
    total = len(results)
    print(f"Aggregate: {passed_count}/{total} gates passed")

    # Save JSON for the test-results folder.
    out_path = Path(__file__).parent / 'test-results' / 'V13_su3_noether.json'
    out_path.parent.mkdir(exist_ok=True, parents=True)
    # Cast numpy types → builtin Python types for json compatibility.
    def _to_jsonable(obj):
        if isinstance(obj, dict):
            return {k: _to_jsonable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_to_jsonable(v) for v in obj]
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        return obj
    with open(out_path, 'w') as f:
        json.dump(_to_jsonable(results), f, indent=2)
    print(f"Results saved → {out_path}")
    return results


if __name__ == '__main__':
    main()
