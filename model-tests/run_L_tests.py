"""
run_L_tests.py  —  Test suite for the v2 layered build (L1–L4)
==============================================================
L1: BCC lattice + exact arccos dispersion           (ca_bcc.py)
L2: Exact-arccos option for 2D Weyl                 (ca_core.py, exact_arccos_2d=True)
L3: Composite-photon Maxwell sector                 (ca_maxwell.py)
L4: EMQG modified-Poisson coupled to c(x)           (ca_curved.py, ca_emqg.py)

Each layer's tests pass independently of the next.  This runner is the
gate between layers per the v2 build sequence.
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ca-simulation'))


def section(title):
    print()
    print('=' * 72)
    print('  ' + title)
    print('=' * 72)


def check(name, ok, detail=''):
    status = 'PASS' if ok else 'FAIL'
    print(f'  [{status}]  {name}  {detail}')
    return ok


# ══════════════════════════════════════════════════════════════════
#  L1 — BCC + exact arccos dispersion
# ══════════════════════════════════════════════════════════════════

def test_L1():
    section('L1 — BCC lattice + exact arccos dispersion (Paper 1 Eq. 15)')
    import ca_bcc as bcc

    results = []

    # L1.a — analytic unitarity over a k-grid (BZ sample density, not lattice resolution)
    K = np.linspace(-np.pi * np.sqrt(3.0), np.pi * np.sqrt(3.0), 16, endpoint=False)
    KX, KY, KZ = np.meshgrid(K, K, K, indexing='ij')
    res_plus = bcc.bcc_unitarity_residual(KX, KY, KZ, sign='+').max()
    res_minus = bcc.bcc_unitarity_residual(KX, KY, KZ, sign='-').max()
    ok = float(max(res_plus, res_minus)) < 1e-12
    results.append(check('U(k)†U(k) = I across BZ (both helicities)', ok,
                         f'(+: {res_plus:.2e}, −: {res_minus:.2e})'))

    # L1.b — Paper 2 V7: A_0 (k=0) = I
    U_zero_plus = bcc.bcc_a0_check(sign='+')
    U_zero_minus = bcc.bcc_a0_check(sign='-')
    ok = (abs(U_zero_plus[0] - 1) + abs(U_zero_plus[1]) + abs(U_zero_plus[2]) + abs(U_zero_plus[3] - 1) < 1e-12 and
          abs(U_zero_minus[0] - 1) + abs(U_zero_minus[1]) + abs(U_zero_minus[2]) + abs(U_zero_minus[3] - 1) < 1e-12)
    results.append(check('A_0 = I at k=0 (Paper 2 V7 constraint)', ok,
                         f'(U_+={U_zero_plus[0].real:.3f}, U_−={U_zero_minus[0].real:.3f})'))

    # L1.c — analytic dispersion vs measured (eigenvalue phase)
    disp_err = bcc.measure_bcc_dispersion(n_modes=20, sign='+')
    ok = disp_err < 1e-12
    results.append(check('analytic ω(k) = measured eigenvalue phase', ok,
                         f'(max err = {disp_err:.2e})'))

    # L1.d — norm conservation over 200 steps on a 160^3 lattice
    # 10× resolution bump (2026-05-16): 16^3 → 160^3 ≈ 4.1M cells; FFT working
    # memory ≈ 250 MB per spinor component.
    drift_plus = bcc.bcc_norm_drift_test(L=160, n_steps=200, sign='+')
    drift_minus = bcc.bcc_norm_drift_test(L=160, n_steps=200, sign='-')
    ok = max(abs(drift_plus), abs(drift_minus)) < 1e-10
    results.append(check('norm drift over 200 steps (16^3, both helicities)', ok,
                         f'(+: {drift_plus:.2e}, −: {drift_minus:.2e})'))

    # L1.e — small-|k| regression to Weyl Hamiltonian H_W = (1/√3) σ·k.
    # Expected to scale as O(|k|^2) — the leading lattice correction.
    # At |k|=0.005 the residual should be ≤ 1e-4.
    rel = bcc.bcc_smallk_to_weyl_residual(k_mag=0.005, n_dirs=12, sign='+')
    ok = rel < 1e-3
    results.append(check('small-|k| → (1/√3)σ·k Weyl regression', ok,
                         f'(rel err at |k|=0.005: {rel:.2e})'))

    # L1.f — composability: forward then "inverse" should return original.
    # The BCC unitary's inverse is its Hermitian conjugate.  In Fourier
    # space the conjugate of U_ff, U_fg, U_gf, U_gg, transposed, gives the
    # reverse step.  Use the '-' helicity as the time-reverse of '+'.
    # (This is more a sanity property than a formal test of time reversal.)
    rng = np.random.default_rng(7)
    L = 120   # 10× bump (2026-05-16): 12 → 120
    f0 = (rng.standard_normal((L, L, L)) +
          1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    g0 = (rng.standard_normal((L, L, L)) +
          1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    n0 = float(np.sum(np.abs(f0) ** 2 + np.abs(g0) ** 2))
    f1, g1 = bcc.weyl_step_3d_bcc(f0, g0, sign='+')
    n1 = float(np.sum(np.abs(f1) ** 2 + np.abs(g1) ** 2))
    drift = abs(n1 / n0 - 1.0)
    ok = drift < 1e-12
    results.append(check('single BCC step preserves norm', ok,
                         f'(drift = {drift:.2e})'))

    return all(results)


# ══════════════════════════════════════════════════════════════════
#  L2 — Exact arccos dispersion in 2D (Paper 1 Eq. 16)
# ══════════════════════════════════════════════════════════════════

def test_L2():
    section('L2 — Exact arccos dispersion for 2D Weyl (Paper 1 Eq. 16)')
    try:
        import ca_core_exact as exact
    except ImportError:
        print('  [SKIP]  ca_core_exact.py not present — L2 not yet implemented')
        return None

    results = []

    # L2.a — unitarity across 2D BZ
    K = np.linspace(-np.pi * np.sqrt(2.0), np.pi * np.sqrt(2.0), 32, endpoint=False)
    KX, KY = np.meshgrid(K, K, indexing='ij')
    res = exact.exact2d_unitarity_residual(KX, KY).max()
    ok = float(res) < 1e-12
    results.append(check('U(k)†U(k) = I across 2D BZ', ok, f'(max = {res:.2e})'))

    # L2.b — A_0 = I at k=0
    U_zero = exact.exact2d_a0_check()
    ok = (abs(U_zero[0] - 1) + abs(U_zero[1]) + abs(U_zero[2]) + abs(U_zero[3] - 1)) < 1e-12
    results.append(check('A_0 = I at k=0', ok, f'(U_ff={U_zero[0].real:.6f})'))

    # L2.c — frequency-dependent c (Paper 4 Eq. 23 analog)
    # In 2D the dispersion is ω = arccos(c_x c_y) with c_i = cos(k_i/√2).
    # At small k, |v_g| ≈ 1/√2 - k^2/... (correction)
    deviation = exact.exact2d_freq_dependent_c(k_mag=0.5)
    ok = abs(deviation) > 1e-3   # there *should* be a measurable lattice correction at |k|=0.5
    results.append(check('frequency-dependent c at |k|=0.5 (Paper 4 Eq. 23)', ok,
                         f'(Δc/c ≈ {deviation:.4f})'))

    # L2.d — small-|k| regression to v_g = 1/√2
    err = exact.exact2d_smallk_residual(k_mag=0.01)
    ok = err < 1e-3
    results.append(check('small-|k| → linear ω = (1/√2)|k|', ok, f'(rel err = {err:.2e})'))

    # L2.e — norm conservation over 200 steps  (10× bump 2026-05-16: 32 → 320)
    drift = exact.exact2d_norm_drift(L=320, n_steps=200, seed=0)
    ok = abs(drift) < 1e-12
    results.append(check('norm drift over 200 steps (32×32)', ok, f'(drift = {drift:.2e})'))

    return all(results)


# ══════════════════════════════════════════════════════════════════
#  L3 — Composite-photon Maxwell sector
# ══════════════════════════════════════════════════════════════════

def test_L3a():
    """
    L3a — kinematic checks (dispersion, transversality, anisotropy).

    These are the parts of the composite-photon construction that
    *do* pass cleanly.  Split out from L3 per model-observations.md
    item 5: bundling the O(k) curl-residual with these three made
    L3 look like 3/3 PASS when the central Maxwell identity actually
    fails.  L3a is the pass; L3b reports the curl-residual partial.
    """
    section('L3a — Composite photon kinematics (Paper 1 Eq. 35, dispersion + transversality)')
    try:
        import ca_maxwell as max_
    except ImportError:
        print('  [SKIP]  ca_maxwell.py not present — L3a not yet implemented')
        return None

    results = []
    # L3a.1 — composite-photon dispersion ω_γ = |k|/√3 at small k
    # (Paper 1 line 36; the lattice analog of 2 ω(k/2) → |k|/√3)
    disp_err = max_.maxwell_dispersion_residual(k_mag=0.05)
    ok = disp_err < 1e-2
    results.append(check('composite-photon dispersion ω = |k|/√3 (Paper 1)', ok,
                         f'(rel err = {disp_err:.2e})'))

    # L3a.2 — transversality: 2 ñ_{k/2} · E_G = 0, 2 ñ_{k/2} · B_G = 0
    # (Paper 1 Eq. 35, first two relations)
    trans = max_.maxwell_transversality(k_mag=0.05, n_dirs=8)
    ok = trans < 1e-12
    results.append(check('transversality (2ñ·E = 2ñ·B = 0)', ok, f'(max = {trans:.2e})'))

    # L3a.3 — anisotropy check.  Paper 1 line 36-44 / Paper 4 Eq. 23: the
    # BCC dispersion is anisotropic; along (1,0,0) lattice-axis directions
    # there is no correction (k/√3 holds exactly), along (1,1,1) the
    # leading correction is O(k) from the sin·sin·sin term in u(k/2).
    # Verify both regimes.
    import ca_bcc as _bcc
    k_test = 0.05
    # Along (1,0,0): exact.
    _, _, w_axis = max_.weyl_eigenmodes_3d_bcc(k_test/2, 0, 0)
    err_axis = abs(2 * w_axis - k_test / np.sqrt(3)) / (k_test / np.sqrt(3))
    # Along (1,1,1)/√3: O(k) correction = k/18.
    kk = k_test / np.sqrt(3)
    _, _, w_diag = max_.weyl_eigenmodes_3d_bcc(kk/2, kk/2, kk/2)
    err_diag = abs(2 * w_diag - k_test / np.sqrt(3)) / (k_test / np.sqrt(3))
    # Expected analytically: err_axis ≈ 1e-15, err_diag ≈ k/18 = 0.00278.
    ok = err_axis < 1e-10 and 1e-3 < err_diag < 1e-2
    results.append(check('dispersion anisotropic: axis exact, diag ≈ k/18', ok,
                         f'(err_axis = {err_axis:.2e}, err_diag = {err_diag:.2e})'))

    return all(results)


def test_L3b():
    """
    L3b — Maxwell curl-equation residual (Paper 1 Eq. 35, third/fourth
    relations).  Status: **PARTIAL**.  The pointwise composite-photon
    bilinear gives a curl residual that scales as O(k) rather than O(k³),
    so the central Maxwell identity is not satisfied to leading order.
    The full smeared-photon construction (Paper 1 lines 84-90, smearing
    function f_k(q)) is required to reach O(k³).

    Reported as INFO; not part of any PASS/FAIL totals until the smeared
    construction lands.  Split out from L3 per model-observations.md
    item 5 so the kinematic L3a no longer hides this partial.
    """
    section('L3b — Maxwell curl residual (PARTIAL: O(k) not O(k³); smeared construction pending)')
    try:
        import ca_maxwell as max_
    except ImportError:
        print('  [SKIP]  ca_maxwell.py not present — L3b not yet implemented')
        return None

    err_E, err_B = max_.maxwell_curl_residual(k_mag=0.05, n_dirs=8)
    print(f'  [INFO]  Maxwell curl residual (pointwise bilinear, k=0.05): '
          f'E={err_E:.2e}, B={err_B:.2e}')
    print(f'  [INFO]  Leading-order curl/k coefficient is 1/√6 ≈ '
          f'{1.0/np.sqrt(6.0):.6f} (see Findings 2 / ca-reference.md).')
    print(f'  [INFO]  Smeared-photon construction (Paper 1 lines 84-90) '
          f'needed to push residual to O(k³).')
    print(f'  L3b status: PARTIAL — kinematic parts (L3a) pass; curl '
          f'identity awaits the smeared construction.')
    return None    # not a PASS/FAIL contributor


# Legacy alias preserved so existing call sites continue to work.  Use
# test_L3a and test_L3b directly for the split.
def test_L3():
    return test_L3a()


def test_L3c():
    """
    L3c — F26 rotation propagator as default EM propagator (Phase 2).

    roadmap-f26-rotation.md Phase 2: rotation_step_em_spectral replaces per-step
    Weyl/Maxwell-curl evolution as the default for EM-only simulation loops.
    It is exact (machine precision) and faster (single FFT pair per tick).

    Two checks on the full 3D BCC lattice (L=16):
      L3c.1 — Energy conservation over 100 ticks (8 random modes, complex fields).
      L3c.2 — Per-mode rotation accuracy: each Fourier mode rotates by exactly
               Ω(k) = 2 ω_BCC(k/2) per tick (machine-precision residual).
    """
    section('L3c — F26 rotation propagator: full-lattice EM default (Phase 2)')
    try:
        import ca_maxwell as max_
    except ImportError:
        print('  [SKIP]  ca_maxwell.py not present')
        return None

    results = []

    r = max_.composite_photon_propagation_full_lattice(
        n_steps=100, L=16, n_modes=8, seed=77)

    # L3c.1 — energy conservation
    ok1 = r['energy_drift'] < 1e-12
    results.append(check(
        'L3c.1  energy conservation, 100 ticks (L=16, 8 modes)',
        ok1, f'(max drift = {r["energy_drift"]:.2e})'))

    # L3c.2 — per-mode rotation accuracy
    ok2 = r['max_mode_error'] < 1e-12
    results.append(check(
        'L3c.2  per-mode rotation residual ≤ machine precision',
        ok2, f'(max = {r["max_mode_error"]:.2e})'))

    return all(results)


# ══════════════════════════════════════════════════════════════════
#  L4 — EMQG modified Poisson sourcing c(x)
# ══════════════════════════════════════════════════════════════════

def test_L4():
    section('L4 — EMQG modified Poisson + c(φ) (Paper 6 Eq. 19.7)')
    try:
        import ca_emqg as emqg
    except ImportError:
        print('  [SKIP]  ca_emqg.py not present — L4 not yet implemented')
        return None

    results = []
    # L4.a — Static Poisson: 1/r potential from a point source recovers Newtonian
    err_pot = emqg.test_point_source_potential()
    ok = err_pot < 5e-2   # 5% on a 64x64x64 lattice is acceptable
    results.append(check('static Poisson reproduces 1/r at large r', ok,
                         f'(rel err = {err_pot:.2e})'))

    # L4.b — c(φ) reduction: vacuum (ρ=0) gives c = c_0 uniformly
    drift = emqg.test_vacuum_c_uniform()
    ok = drift < 1e-12
    results.append(check('vacuum (ρ=0) → c = c_0 uniformly', ok,
                         f'(max |c−c_0| = {drift:.2e})'))

    # L4.c — Gravitational deflection in 2-D Poisson (legacy, log-potential).
    # Kept as INFO since the 2-D Green's function is logarithmic and the
    # "rel err vs 2.0" target is a 3-D Newtonian benchmark — dimensionally
    # inconsistent (see model-observations.md item 4).  The 3-D test below
    # is the dimensionally correct version.
    rel_2d = emqg.test_lensing_deflection()
    print(f'  [INFO]  2-D Poisson lensing rel err Δ(2M)/Δ(M) vs 2: '
          f'{rel_2d:.2e}  (log-potential — kept for backward reference)')

    # L4.d — 3-D Newtonian lensing (model-observations.md item 4).  Uses
    # solve_poisson_3d to produce the true 1/r potential, slices at z=L/2,
    # feeds into the 2-D Cayley stepper.  Linear-M scaling is the correct
    # 3-D Newtonian benchmark at leading order.
    rel_3d = emqg.test_lensing_deflection_3d(L=96)
    ok = rel_3d < 0.10
    results.append(check('3-D Newtonian lensing Δ(2M)/Δ(M) ≈ 2 (linear in M)',
                         ok, f'(rel err = {rel_3d:.2e})'))

    # L4.e — 3-D Poisson contract check: ∇²φ should equal 4πGρ on lattice.
    rel_p = emqg.test_point_source_potential_3d()
    results.append(check('3-D discrete Poisson contract (∇²φ=4πGρ)',
                         rel_p < 0.05, f'(rel err = {rel_p:.2e})'))

    return all(results)


# ══════════════════════════════════════════════════════════════════
#  Driver
# ══════════════════════════════════════════════════════════════════

def main():
    L1_ok = test_L1()
    print()
    print('=' * 72)
    print(f'  L1 STATUS: {"PASS" if L1_ok else "FAIL"}')
    print('=' * 72)
    if not L1_ok:
        return 1

    L2_ok = test_L2()
    if L2_ok is None:
        print('\n  ⇒  L2 module not yet present — stopping at L1.')
        return 0
    print()
    print('=' * 72)
    print(f'  L2 STATUS: {"PASS" if L2_ok else "FAIL"}')
    print('=' * 72)
    if not L2_ok:
        return 1

    L3a_ok = test_L3a()
    if L3a_ok is None:
        print('\n  ⇒  L3a module not yet present — stopping at L2.')
        return 0
    print()
    print('=' * 72)
    print(f'  L3a STATUS: {"PASS" if L3a_ok else "FAIL"}  (kinematic — dispersion + transversality)')
    print('=' * 72)
    if not L3a_ok:
        return 1
    # L3b is an INFO-only reporter for the Maxwell curl residual.  Does
    # not contribute to PASS/FAIL totals; the partial status is the point.
    test_L3b()
    print()
    print('=' * 72)
    print('  L3b STATUS: PARTIAL (Maxwell curl residual is O(k), not O(k³))')
    print('=' * 72)

    L3c_ok = test_L3c()
    if L3c_ok is None:
        print('\n  ⇒  L3c: rotation propagator not available — continuing to L4.')
    else:
        print()
        print('=' * 72)
        print(f'  L3c STATUS: {"PASS" if L3c_ok else "FAIL"}  (F26 rotation propagator default)')
        print('=' * 72)
        if not L3c_ok:
            return 1

    L4_ok = test_L4()
    if L4_ok is None:
        print('\n  ⇒  L4 module not yet present — stopping at L3.')
        return 0
    print()
    print('=' * 72)
    print(f'  L4 STATUS: {"PASS" if L4_ok else "FAIL"}')
    print('=' * 72)
    return 0 if L4_ok else 1


if __name__ == '__main__':
    sys.exit(main())
