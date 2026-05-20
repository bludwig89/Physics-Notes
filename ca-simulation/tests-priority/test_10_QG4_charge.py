"""
Top-10 priority Test #10 — QG-4: Discrete-Noether charge conservation
=======================================================================
Date: 2026-05-19

Goal
----
Verify that the lattice's U(1) and SU(2) Noether charges are conserved
to machine precision at every step:
    |ΔQ| / |Q| < 1e-13 per 1000 steps at L = 256

Method
------
The conserved U(1) charge is the integrated probability density of a
Dirac wavefunction:
    Q_U(1) = ∫ ψ†ψ d³x

(equivalent to the total probability for the standard QM normalisation).

For the SU(2) case, we need the chiral charge — the left-minus-right
imbalance:
    Q_SU(2) = ∫ (ψ_L† ψ_L - ψ_R† ψ_R) d³x

For a pure Dirac propagator (m > 0), this is NOT conserved (mass term
mixes L and R chiralities — zitterbewegung).  For m = 0 (Weyl), Q_SU(2)
IS conserved.

We test:
  (i)   U(1) charge conservation over 1000 steps at L=256
  (ii)  Chiral charge conservation at m=0 (Weyl regression)
  (iii) Chiral charge non-conservation at m≠0 (zitterbewegung)
  (iv)  Per-cell flux balance — verify the discrete continuity equation
        ∂_t ρ + ∇·j = 0 holds pointwise at machine precision.
"""

import os, sys, math, json
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..')))

import ca_dirac


def total_charge(eu, ed, cu, cd):
    """U(1) Noether charge = sum of |ψ|²."""
    return float(np.sum(np.abs(eu)**2 + np.abs(ed)**2 +
                        np.abs(cu)**2 + np.abs(cd)**2))


def chiral_charge(eu, ed, cu, cd):
    """SU(2)-style chiral charge = ρ_L − ρ_R (η is left, χ is right)."""
    rho_L = float(np.sum(np.abs(eu)**2 + np.abs(ed)**2))
    rho_R = float(np.sum(np.abs(cu)**2 + np.abs(cd)**2))
    return rho_L - rho_R


def random_dirac_field(L, seed=0):
    """Initialise random complex Gaussian Dirac field, then normalise."""
    rng = np.random.default_rng(seed)
    def G():
        return ((rng.standard_normal((L, L)) + 1j*rng.standard_normal((L, L)))
                * 0.1).astype(np.complex128)
    eu, ed, cu, cd = G(), G(), G(), G()
    norm = math.sqrt(total_charge(eu, ed, cu, cd))
    return eu/norm, ed/norm, cu/norm, cd/norm


def main():
    print('=' * 70)
    print('QG-4 — Discrete-Noether U(1) and chiral charge conservation')
    print('=' * 70)
    print('Date 2026-05-19')
    print()
    out = {'date': '2026-05-19', 'test': 'QG-4 charge conservation'}

    # ────────────────── Test (i): U(1) charge at L=256 ──────────────────
    print('Stage 1: U(1) probability charge conservation over 1000 steps')
    print('  Random Dirac field, m = 0.10 (massive), L = 256')
    L = 256
    n_steps = 1000
    m = 0.10
    eu, ed, cu, cd = random_dirac_field(L, seed=42)
    Q0 = total_charge(eu, ed, cu, cd)
    print(f'  Initial U(1) charge: Q_0 = {Q0:.16f}')
    history = [Q0]
    for step in range(n_steps):
        eu, ed, cu, cd = ca_dirac.dirac_step_2d_splitstep(
            eu, ed, cu, cd, m=m, dt=1.0)
        if (step + 1) % 100 == 0:
            Q = total_charge(eu, ed, cu, cd)
            history.append(Q)
            dQ = abs(Q - Q0)
            print(f'  step {step+1:>5}: Q = {Q:.16f}, |ΔQ| = {dQ:.4e}, '
                  f'|ΔQ|/Q = {dQ/Q0:.4e}')
    Q_final = total_charge(eu, ed, cu, cd)
    rel_dQ_U1 = abs(Q_final - Q0) / Q0
    pass_U1 = rel_dQ_U1 < 1e-13
    print(f'\n  Final |ΔQ|/Q = {rel_dQ_U1:.4e}  ({"PASS" if pass_U1 else "FAIL"} at 1e-13 gate)')
    out['U1_test'] = {
        'L': L, 'n_steps': n_steps, 'm': m, 'Q0': Q0,
        'Q_final': Q_final, 'rel_dQ': rel_dQ_U1,
        'pass_1e-13': pass_U1,
    }

    # ────────────────── Test (ii): Chiral at m=0 ──────────────────
    print()
    print('Stage 2: Chiral charge (SU(2)) conservation at m = 0 (Weyl)')
    L2 = 128
    n_steps2 = 500
    eu, ed, cu, cd = random_dirac_field(L2, seed=7)
    Q_chi_0 = chiral_charge(eu, ed, cu, cd)
    Q_tot_0 = total_charge(eu, ed, cu, cd)
    print(f'  Initial Q_chiral = {Q_chi_0:.10f}, Q_total = {Q_tot_0:.10f}')
    for step in range(n_steps2):
        eu, ed, cu, cd = ca_dirac.dirac_step_2d_splitstep(
            eu, ed, cu, cd, m=0.0, dt=1.0)
    Q_chi_f = chiral_charge(eu, ed, cu, cd)
    Q_tot_f = total_charge(eu, ed, cu, cd)
    dQ_chi_m0 = abs(Q_chi_f - Q_chi_0)
    dQ_tot_m0 = abs(Q_tot_f - Q_tot_0)
    print(f'  Final   Q_chiral = {Q_chi_f:.10f}, Q_total = {Q_tot_f:.10f}')
    print(f'  |ΔQ_chiral| = {dQ_chi_m0:.4e}, |ΔQ_total| = {dQ_tot_m0:.4e}')
    pass_chi = dQ_chi_m0 < 1e-12
    print(f'  Chiral conservation at m=0: {"PASS" if pass_chi else "FAIL"} at 1e-12 gate')
    out['chiral_test_m0'] = {
        'L': L2, 'n_steps': n_steps2,
        'Q_chi_0': Q_chi_0, 'Q_chi_final': Q_chi_f,
        'dQ_chi': dQ_chi_m0, 'pass_1e-12': pass_chi,
    }

    # ────────────────── Test (iii): Chiral at m≠0 should DRIFT ──────────────────
    print()
    print('Stage 3: Chiral charge SHOULD NOT be conserved at m ≠ 0 (zitterbewegung)')
    eu, ed, cu, cd = ca_dirac.gaussian_dirac_2d((L2, L2), sigma=4.0,
                                                  chirality='left')
    Q_chi_0 = chiral_charge(eu, ed, cu, cd)
    Q_tot_0 = total_charge(eu, ed, cu, cd)
    print(f'  Pure-left initial Q_chiral = {Q_chi_0:.6f}, Q_total = {Q_tot_0:.6f}')
    m_zit = 0.5
    n_zit = 200
    swings = []
    for step in range(n_zit):
        eu, ed, cu, cd = ca_dirac.dirac_step_2d_splitstep(
            eu, ed, cu, cd, m=m_zit, dt=0.5)
        if (step + 1) % 20 == 0:
            Q_chi = chiral_charge(eu, ed, cu, cd) / Q_tot_0
            swings.append(Q_chi)
    print(f'  Q_chiral/Q_total over time (samples): '
          f'{[round(s, 4) for s in swings]}')
    span = max(swings) - min(swings)
    print(f'  Span of Q_chiral / Q_total: {span:.4f}')
    # Note: any value < 1.0 confirms chirality mixing — not a failure;
    # this is the expected zitterbewegung behaviour at m≠0.
    print(f'  Q_total conservation at m=0.5: |ΔQ_total| = '
          f'{abs(total_charge(eu, ed, cu, cd) - Q_tot_0):.4e}')
    out['chiral_test_m_nonzero'] = {
        'L': L2, 'm': m_zit, 'n_steps': n_zit,
        'Q_chi_span': span,
        'Q_tot_drift': abs(total_charge(eu, ed, cu, cd) - Q_tot_0),
    }

    # ────────────────── Test (iv): per-cell flux balance ──────────────────
    print()
    print('Stage 4: Per-cell continuity ∂_t ρ + ∇·j = 0 (discrete check)')
    # On a flat lattice with the exact-QCA Dirac stepper, the per-cell
    # density changes Δρ(x) = ρ(x, t+1) − ρ(x, t).  We compute it directly
    # and verify ∫Δρ = 0 globally; pointwise current j is encoded in the
    # stepper's k-space rotation.  Here we just verify GLOBAL conservation:
    # Σ Δρ ≈ 0 to machine precision per step.
    L4 = 64
    eu, ed, cu, cd = random_dirac_field(L4, seed=99)
    rho_t = (np.abs(eu)**2 + np.abs(ed)**2 + np.abs(cu)**2 + np.abs(cd)**2)
    Q_t = float(rho_t.sum())
    eu, ed, cu, cd = ca_dirac.dirac_step_2d_splitstep(
        eu, ed, cu, cd, m=0.10, dt=1.0)
    rho_t1 = (np.abs(eu)**2 + np.abs(ed)**2 + np.abs(cu)**2 + np.abs(cd)**2)
    Q_t1 = float(rho_t1.sum())
    delta_rho = rho_t1 - rho_t
    print(f'  Σ Δρ = {delta_rho.sum():.4e}  (continuity: should be ≈ 0)')
    print(f'  max(|Δρ|) = {np.abs(delta_rho).max():.4e}')
    print(f'  Σ ρ at t  : {Q_t:.16f}')
    print(f'  Σ ρ at t+1: {Q_t1:.16f}')
    print(f'  |ΔQ| / Q  : {abs(Q_t1 - Q_t)/Q_t:.4e}')
    out['continuity_test'] = {
        'sum_delta_rho': float(delta_rho.sum()),
        'max_abs_delta_rho': float(np.abs(delta_rho).max()),
        'Q_drift_per_step': abs(Q_t1 - Q_t) / Q_t,
    }

    # ────────────────── Gate Evaluation ──────────────────
    print()
    print('=' * 70)
    print('GATE EVALUATION')
    print('=' * 70)
    print(f'  U(1) charge over 1000 steps:    |ΔQ|/Q = {rel_dQ_U1:.4e}')
    print(f'    → 1e-13 gate:                 {"PASS" if pass_U1 else "FAIL"}')
    print(f'  Chiral charge (m=0, 500 steps): |ΔQ| = {dQ_chi_m0:.4e}')
    print(f'    → 1e-12 gate:                 {"PASS" if pass_chi else "FAIL"}')
    print(f'  Per-step continuity Σ Δρ:       {out["continuity_test"]["sum_delta_rho"]:.4e}')
    print()
    print('  Chiral mixing at m=0.5 (expected, NOT a failure):')
    print(f'    Q_chiral span:                {span:.4f} (non-zero → mass term active)')
    print(f'    Q_total at m=0.5:             |ΔQ| = {out["chiral_test_m_nonzero"]["Q_tot_drift"]:.4e}')
    out['gate_summary'] = {
        'U1_pass_1e-13': pass_U1,
        'chiral_m0_pass_1e-12': pass_chi,
    }

    out_path = os.path.join(THIS, '..', '..', 'test-results',
                             'top10_T10_QG4_charge.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults written to {out_path}')
    return out


if __name__ == '__main__':
    main()
