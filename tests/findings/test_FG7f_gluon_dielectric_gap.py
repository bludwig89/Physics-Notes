"""
test_FG7f_gluon_dielectric_gap.py — gap-coupled colour-dielectric gluon propagator
==================================================================================

Verifies Part D of `ca-simulation/ca_colour_dielectric.py` (added 2026-06-08):
the colour-dielectric renormalisation wired into the *time-evolved* gluon
propagator, and the ca_colour_condensate (F88) gap coupled into the dynamical
gluon field.  The thesis: one measured number — the condensate VEV v — sets the
dielectric eps_c, the dual-Meissner gluon mass m_V = e v, the screening length
lambda = 1/m_V and the tension sigma = 2 pi v^2 at once.

  GD1  BCC even-law dielectric step reduces to the free F91 even step
       BIT-FOR-BIT at eps_c=1 (and eps_c=None).                       [tier 1]
  GD2  Uniform dielectric is exactly unitary: (E^2+B^2) conserved over many
       ticks, and c_eff = c_lat sqrt(eps_c).                          [tier 1]
  GD3  Gap coupling: condensate VEV from the F88 MC density chain gives a
       positive m_V = e v and sigma_F86 = 2 pi v^2 (the F86 hand-off).[tier 3]
  GD4  Gap-massive gluon dispersion: evolving with the condensate mass m_V
       reproduces omega_eff = sqrt(m_V^2 + Omega_even^2) to machine eps;
       m_V=0 reduces to the free step bit-for-bit.                    [tier 1]
  GD5  The SAME measured m_V sets the dual-Meissner screening length:
       London colour-electric field decays with lambda = 1/m_V.      [tier 3]
  GD6  Dynamic confinement: a colour-electric packet launched in the tube
       core does NOT propagate into the condensed (eps_c->0) vacuum — flux
       expelled (dual Meissner realised in time evolution).  eps_c=1 control
       transmits freely; eps_c=1 everywhere is bit-for-bit the free step. [tier 3]

Module under test:  ca-simulation/ca_colour_dielectric.py  (Part D)
Created:            2026-06-08
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ca-simulation'))

import ca_colour_dielectric as cd   # noqa: E402
import ca_gluon as cg               # noqa: E402
import ca_wmu as cwmu               # noqa: E402


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ═════════════════════════════════════════════════════════════════════
#  GD1 — BCC dielectric step reduces to the free even step bit-for-bit
# ═════════════════════════════════════════════════════════════════════

def test_GD1_bcc_free_reduction():
    rng = np.random.default_rng(20260608)
    L = 8
    E = rng.standard_normal((8, L, L, L))
    B = rng.standard_normal((8, L, L, L))
    E_free, B_free = cg.gluon_rotation_step_spectral_bcc(E, B)
    E1, B1 = cd.gluon_dielectric_rotation_step_bcc(E, B, eps_c=1.0)
    EN, BN = cd.gluon_dielectric_rotation_step_bcc(E, B, eps_c=None)
    bitexact = (np.max(np.abs(E_free - E1)) + np.max(np.abs(B_free - B1))
                + np.max(np.abs(E_free - EN)) + np.max(np.abs(B_free - BN)))
    # eps_c < 1 actually changes the field
    Eh, Bh = cd.gluon_dielectric_rotation_step_bcc(E, B, eps_c=0.25)
    changed = np.max(np.abs(Eh - E_free)) > 1e-3
    passed = bool(bitexact < 1e-12 and changed)
    return {'test': 'GD1', 'tier': 1, 'passed': passed, 'residual': float(bitexact),
            'name': 'BCC even-law dielectric step == free step bit-for-bit at eps_c=1',
            'detail': {'bit_exact_reduction': float(bitexact),
                       'field_changes_at_eps0.25': bool(changed)}}


# ═════════════════════════════════════════════════════════════════════
#  GD2 — uniform dielectric is exactly unitary; c_eff scaling
# ═════════════════════════════════════════════════════════════════════

def test_GD2_unitarity_and_ceff():
    rng = np.random.default_rng(7)
    L = 8
    E = rng.standard_normal((8, L, L, L))
    B = rng.standard_normal((8, L, L, L))
    e0 = cd.field_energy(E, B)
    Eu, Bu = E.copy(), B.copy()
    for _ in range(200):
        Eu, Bu = cd.gluon_dielectric_rotation_step_bcc(Eu, Bu, eps_c=0.49)
    drift = abs(cd.field_energy(Eu, Bu) - e0) / e0
    ceff = cd.effective_lattice_c(0.49)
    ceff_exp = (1.0 / np.sqrt(3.0)) * np.sqrt(0.49)
    ceff_res = abs(float(ceff) - ceff_exp)
    passed = bool(drift < 1e-10 and ceff_res < 1e-15)
    return {'test': 'GD2', 'tier': 1, 'passed': passed, 'residual': float(drift),
            'name': 'uniform dielectric exactly unitary + c_eff=c sqrt(eps_c)',
            'detail': {'energy_drift_200_ticks': float(drift),
                       'c_eff(0.49)': float(ceff), 'c_eff_expected': float(ceff_exp),
                       'c_eff_residual': float(ceff_res)}}


# ═════════════════════════════════════════════════════════════════════
#  GD3 — gap coupling: condensate VEV from the F88 MC density chain
# ═════════════════════════════════════════════════════════════════════

def test_GD3_condensate_gap():
    vb = cd.condensate_vev_from_mc(L=6, beta=1.8, n_sweeps=160, seed=3)
    # sigma_F86 = 2 pi v^2 consistency
    sigma_check = abs(vb['sigma_F86'] - 2.0 * np.pi * vb['v'] ** 2)
    # m_V = e v = m_D and v = m_D sqrt(beta)  (e^2 = 1/beta)
    v_check = abs(vb['v'] - vb['m_V'] * np.sqrt(vb['beta']))
    passed = bool(vb['v'] > 0 and vb['m_V'] > 0 and vb['rho'] > 0
                  and sigma_check < 1e-9 and v_check < 1e-9)
    return {'test': 'GD3', 'tier': 3, 'passed': passed, 'residual': float(sigma_check),
            'name': 'condensate VEV from measured MC density (F88->F86 hand-off)',
            'detail': vb | {'sigma_consistency': float(sigma_check),
                            'v_eq_mD_sqrt_beta': float(v_check)}}


# ═════════════════════════════════════════════════════════════════════
#  GD4 — gap-massive gluon dispersion omega^2 = m_V^2 + Omega_even^2
# ═════════════════════════════════════════════════════════════════════

def test_GD4_gap_massive_dispersion():
    rng = np.random.default_rng(11)
    beta, rho = 1.8, 0.024
    m_V = cd.gluon_gap_mass(beta, rho)
    L, nstep = 10, 40
    E = np.zeros((8, L, L, L)); B = np.zeros((8, L, L, L))
    E[0] = rng.standard_normal((L, L, L)); B[0] = rng.standard_normal((L, L, L))
    KX, KY, KZ = cwmu._kgrid3d(L, L, L)
    Om = cwmu._omega_even(KX, KY, KZ)
    weff = np.sqrt(m_V ** 2 + Om ** 2)
    C0 = np.fft.fftn(E[0]) + 1j * np.fft.fftn(B[0])
    Ec, Bc = E.copy(), B.copy()
    for _ in range(nstep):
        Ec, Bc = cd.gluon_gap_massive_step_bcc(Ec, Bc, beta, rho)
    Cn = np.fft.fftn(Ec[0]) + 1j * np.fft.fftn(Bc[0])
    Cexp = C0 * np.exp(-1j * weff * nstep)
    amp = np.abs(C0); sig = amp > 1e-8 * amp.max()
    rel = float(np.max(np.where(sig, np.abs(Cn - Cexp) / (amp + 1e-30), 0.0)))
    # gapless reduction: rho=0 -> m_V=0 -> free even step bit-for-bit
    E0, B0 = cd.gluon_gap_massive_step_bcc(E, B, beta, 0.0)
    Ef, Bf = cg.gluon_rotation_step_spectral_bcc(E, B)
    gapless = float(np.max(np.abs(E0 - Ef)) + np.max(np.abs(B0 - Bf)))
    passed = bool(rel < 1e-10 and gapless < 1e-12)
    return {'test': 'GD4', 'tier': 1, 'passed': passed, 'residual': rel,
            'name': 'gap-massive gluon dispersion omega^2 = m_V^2 + Omega_even^2',
            'detail': {'m_V': float(m_V), 'dispersion_residual': rel,
                       'gapless_reduction': gapless}}


# ═════════════════════════════════════════════════════════════════════
#  GD5 — the same m_V sets the dual-Meissner screening length lambda=1/m_V
# ═════════════════════════════════════════════════════════════════════

def test_GD5_screening_from_gap():
    beta, rho = 1.8, 0.024
    m_V = cd.gluon_gap_mass(beta, rho)
    scr = cd.london_screened_field_2d(L=96, m=m_V)
    lam, lexp = cd.fit_penetration_depth(scr, r_min=4, r_max=24)
    rel = abs(lam - lexp) / lexp
    passed = bool(rel < 0.05 and abs(lexp - 1.0 / m_V) < 1e-12)
    return {'test': 'GD5', 'tier': 3, 'passed': passed, 'residual': float(rel),
            'name': 'dual-Meissner screening lambda = 1/m_V from the measured gap',
            'detail': {'m_V': float(m_V), 'lambda_fit': float(lam),
                       'lambda_expected': float(lexp)}}


# ═════════════════════════════════════════════════════════════════════
#  GD6 — dynamic confinement: flux expelled from the condensed vacuum
# ═════════════════════════════════════════════════════════════════════

def test_GD6_dynamic_confinement():
    L = 48
    f = cd.slab_condensate_field_2d(L, core_frac=0.4, axis=1)
    eps = cd.eps_c_field_from_condensate(f)
    yy, xx = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
    c = (L - 1) / 2.0
    pk = np.exp(-((xx - c) ** 2 + (yy - c) ** 2) / (2.0 * 3.0 ** 2))
    E = np.zeros((1, L, L)); B = np.zeros((1, L, L)); E[0] = pk
    cond = eps < 0.05                       # deep condensed vacuum mask

    Ed, Bd = cd.gluon_dielectric_evolve_2d(E.copy(), B.copy(), eps, n_steps=60, dt=0.4)
    Ec, Bc = cd.gluon_dielectric_evolve_2d(E.copy(), B.copy(),
                                           np.ones((L, L)), n_steps=60, dt=0.4)

    def frac_in(Ef, Bf):
        en = Ef[0] ** 2 + Bf[0] ** 2
        return float(en[cond].sum() / en.sum())

    frac_diel = frac_in(Ed, Bd)
    frac_free = frac_in(Ec, Bc)
    suppression = frac_free / max(frac_diel, 1e-30)

    # eps_c=1 everywhere -> one tick is bit-for-bit the free 8-octet step
    Eg = np.random.default_rng(2).standard_normal((8, L, L))
    Bg = np.random.default_rng(3).standard_normal((8, L, L))
    E1, B1 = cd.gluon_dielectric_evolve_2d(Eg, Bg, np.ones((L, L)), n_steps=1, dt=1.0)
    Er, Br = cg.gluon_rotation_step_spectral_2d(Eg, Bg)
    bitexact = float(np.max(np.abs(E1 - Er)) + np.max(np.abs(B1 - Br)))

    passed = bool(frac_diel < 0.05 and frac_free > 0.2
                  and suppression > 10.0 and bitexact < 1e-12)
    return {'test': 'GD6', 'tier': 3, 'passed': passed, 'residual': float(frac_diel),
            'name': 'dynamic flux expulsion from condensed vacuum (dual Meissner)',
            'detail': {'frac_in_condensed_dielectric': frac_diel,
                       'frac_in_condensed_free_control': frac_free,
                       'suppression_factor': suppression,
                       'free_step_bitexact': bitexact}}


# ═════════════════════════════════════════════════════════════════════

def main():
    t_start = time.perf_counter()
    tests = [
        test_GD1_bcc_free_reduction,
        test_GD2_unitarity_and_ceff,
        test_GD3_condensate_gap,
        test_GD4_gap_massive_dispersion,
        test_GD5_screening_from_gap,
        test_GD6_dynamic_confinement,
    ]
    results = []
    n_pass = 0
    for fn in tests:
        t0 = time.perf_counter()
        try:
            r = fn()
            r['elapsed_s'] = time.perf_counter() - t0
            results.append(r)
            ok = bool(r.get('passed'))
            n_pass += int(ok)
            print(f"  [{'PASS' if ok else 'FAIL'}] {r.get('test'):4s}  "
                  f"{r.get('name'):60s}  res = {r.get('residual')}  "
                  f"({r['elapsed_s']:.3f} s)")
        except Exception as exc:
            import traceback
            traceback.print_exc()
            results.append({'test': fn.__name__, 'passed': False, 'error': repr(exc)})
            print(f"  [ERROR] {fn.__name__}: {exc!r}")

    total_t = time.perf_counter() - t_start
    summary = {
        'suite': 'FG-7f — gap-coupled colour-dielectric gluon propagator (Part D)',
        'date': '2026-06-08',
        'n_tests': len(tests),
        'n_passed': n_pass,
        'total_elapsed_s': total_t,
        'results': results,
    }
    print(f"\n  -> {n_pass}/{len(tests)} PASS  in  {total_t:.2f} s")
    return summary


if __name__ == '__main__':
    summary = main()
    out = os.path.join(os.path.dirname(__file__),
                       '..', '..', 'test-results', 'FG7f_gluon_dielectric_gap.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(summary, f, indent=2, cls=_NumpyEncoder)
    print(f"  -> wrote {out}")
    raise SystemExit(0 if summary['n_passed'] == summary['n_tests'] else 1)
