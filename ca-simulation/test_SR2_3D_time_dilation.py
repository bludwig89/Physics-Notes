"""
test_SR2_3D_time_dilation.py — SR-2 expansion to 3D using the BCC lattice
=========================================================================

3D analog of `test_SR2_time_dilation.py` (Finding 12).  Tests whether the
3D BCC Dirac QCA reproduces SR time dilation from the emergent-time /
phase-tick framework (Finding 11), with no built-in Lorentz boost.

Lattice setup
-------------
  Spatial: BCC 3D Weyl QCA (Paper 1 Eq. 15) — `ca_bcc.bcc_unitary`.
  Mass:    Dirac off-diagonal coupling im·I (Paper 1 Eq. 23) — built into
           `ca_dirac_bcc.dirac_step_3d_bcc_splitstep`.
  ω_k:     arccos(n · u(k)),  u(k) = c_x c_y c_z + s_x s_y s_z,
           c_i = cos(k_i/√3),  s_i = sin(k_i/√3),  n = √(1 − m²).
  c_lat:   1/√3   (vs 1/√2 in the 2D test).

The test has two parts:

  Part A — Algebraic.
    Pick a packet moving along the x-axis: k = (k_x, 0, 0), so c_y = c_z = 1,
    s_y = s_z = 0, and u(k) = c_x, ω_k = arccos(n·c_x).
    Group velocity along x:
        ∂u/∂k_x = −s_x/√3,
        v_g     = (n · s_x / √3) / sin(ω_k).
    Static frequency:
        ω_static = ω_0 = arccos(n) = arcsin(m).
    Moving (worldline-aligned) frequency:
        ω_moving = ω_k − k_x · v_g.
    SR prediction:
        1/γ_SR = √(1 − (v_g/c_lat)²)  with c_lat = 1/√3.
    Compare ratio_QCA(m, k_x) = ω_moving / ω_static  to  1/γ_SR.
    Residual scales as O(k²) — the leading BCC Lorentz-violation term.

  Part B — Numerical propagation.
    Build a 3D plane wave at on-grid (k_x, 0, 0) from a positive-frequency
    eigenmode of the 4×4 D_k.  Propagate with `dirac_step_3d_bcc_splitstep`.
    Sample η_↑ at the lattice centre (static) and along the worldline
    x(t) = v_g·t (moving, with FFT-based sub-pixel sampling).  Extract
    phase rate ω from each sample via unwrapped least-squares fit.
    Compare ω_moving_num / ω_static_num to:
      (i) the dispersion-derived prediction ω_k − k·v_g (FFT-floor match),
      (ii) 1/γ_SR (continuum SR; characterise the lattice LV gap).

Gates from the roadmap (`lattice-vs-spacetime-tests.md`, SR-2):
  - Dispersion-identity:  ratio_num = (ω_k − k v_g)/arcsin(m) at FFT floor.
  - Continuum-SR:         ratio_num ≈ 1/γ within O(k²) at small k.

Run:
    python3 test_SR2_3D_time_dilation.py
"""

import os, sys, math
import numpy as np

# Allow standalone run from ca-simulation/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ca_bcc as bcc
import ca_dirac_bcc as cdb


C_LAT_3D = 1.0 / math.sqrt(3.0)
INV_ROOT3 = 1.0 / math.sqrt(3.0)


# ══════════════════════════════════════════════════════════════════
#  Part A — Algebraic dispersion-derived predictions
# ══════════════════════════════════════════════════════════════════

def omega_qca_x(kx, m):
    """ω_k along the x-axis (k_y = k_z = 0) for the 3D BCC Dirac.

       u(k) = c_x · 1 · 1 + s_x · 0 · 0 = cos(k_x/√3).
       ω_k  = arccos( √(1−m²) · cos(k_x/√3) ).
    """
    n = math.sqrt(1.0 - m * m)
    arg = n * math.cos(kx * INV_ROOT3)
    arg = max(-1.0, min(1.0, arg))
    return math.acos(arg)


def vgroup_qca_x(kx, m):
    """v_g = ∂ω/∂k_x along the x-axis.

       With u = c_x, ∂u/∂k_x = −s_x/√3, sin(ω) = √(1 − n²c_x²):
       v_g = (n · s_x / √3) / sin(ω_k).
    """
    n = math.sqrt(1.0 - m * m)
    w = omega_qca_x(kx, m)
    s = math.sin(w)
    if s < 1e-15:
        return 0.0
    return (n * math.sin(kx * INV_ROOT3) * INV_ROOT3) / s


def omega_static_qca(m):
    """ω at k=0: arccos(n) = arcsin(m)."""
    return math.asin(m)


def part_A_scan():
    """Scan (m, k_x) and tabulate the QCA-vs-SR time-dilation residual."""
    print("=" * 96)
    print("Part A — Algebraic SR-2 in 3D BCC (QCA dispersion vs SR 1/γ)")
    print("=" * 96)
    print()
    print(f"Lattice c_lat (3D BCC) = 1/√3 = {C_LAT_3D:.12f}")
    print()

    masses  = [0.01, 0.05, 0.1, 0.2, 0.5]
    momenta = [0.001, 0.01, 0.05, 0.1, 0.2, 0.5]

    print(f"{'m':>6} {'k_x':>7} {'v_g':>11} {'v_g/c_lat':>11} "
          f"{'ω_static':>11} {'ω_moving':>11} "
          f"{'ratio_QCA':>11} {'1/γ_SR':>11} {'|Δ|':>11}")
    print("-" * 100)

    rows = []
    for m in masses:
        for kx in momenta:
            ws = omega_static_qca(m)
            wk = omega_qca_x(kx, m)
            vg = vgroup_qca_x(kx, m)
            wm = wk - kx * vg
            beta = vg / C_LAT_3D
            if abs(beta) >= 1.0:
                inv_gamma = float('nan')
            else:
                inv_gamma = math.sqrt(1.0 - beta * beta)
            ratio_qca = wm / ws if ws > 0 else float('nan')
            delta = abs(ratio_qca - inv_gamma) if not math.isnan(inv_gamma) else float('nan')
            print(f"{m:6.3f} {kx:7.4f} {vg:11.6e} {beta:11.6e} "
                  f"{ws:11.6e} {wm:11.6e} "
                  f"{ratio_qca:11.8f} {inv_gamma:11.8f} {delta:11.3e}")
            rows.append((m, kx, vg, beta, ws, wm, ratio_qca, inv_gamma, delta))

    print()
    print("Scaling check at fixed m=0.1 — residual vs k_x:")
    print(f"{'k_x':>8} {'|Δ|':>11} {'|Δ|/k²':>12} {'|Δ|/k⁴':>12}")
    print("-" * 50)
    for r in rows:
        if abs(r[0] - 0.1) < 1e-12:
            m, kx, vg, beta, ws, wm, rq, ig, d = r
            if math.isnan(d):
                continue
            print(f"{kx:8.5f} {d:11.3e} {d/kx**2:12.5e} {d/kx**4:12.5e}")

    print()
    print("Scaling check at fixed k_x=0.05 — residual vs m:")
    print(f"{'m':>8} {'|Δ|':>11} {'|Δ|/m²':>12}")
    print("-" * 40)
    for r in rows:
        m, kx, vg, beta, ws, wm, rq, ig, d = r
        if abs(kx - 0.05) < 1e-12:
            if math.isnan(d):
                continue
            print(f"{m:8.4f} {d:11.3e} {d/m**2:12.5e}")

    finite = [r for r in rows if not math.isnan(r[8])]
    finite.sort(key=lambda r: r[8])
    print()
    print(f"Smallest residual in scan: |Δ| = {finite[0][8]:.3e} "
          f"at m={finite[0][0]}, k_x={finite[0][1]}")
    print(f"Largest  residual in scan: |Δ| = {finite[-1][8]:.3e} "
          f"at m={finite[-1][0]}, k_x={finite[-1][1]}")

    return rows


# ══════════════════════════════════════════════════════════════════
#  Part B — Numerical propagation test
# ══════════════════════════════════════════════════════════════════

def positive_freq_eigenmode_3d(kx_target, ky_target, kz_target,
                               m, Lx, Ly, Lz, sign='+'):
    """Snap (kx_target, ky_target, kz_target) to the grid and build the
       positive-frequency eigenmode of the 4×4 D_k at that on-grid k.

       Returns (kx_grid, ky_grid, kz_grid, ω, v4) with v4 = (e_u, e_d, c_u, c_d).
       The amplitude is phase-normalised so v[0] is real-positive.
    """
    # Snap to nearest grid k (fftfreq convention)
    n_target_x = int(round(kx_target * Lx / (2 * math.pi)))
    n_target_y = int(round(ky_target * Ly / (2 * math.pi)))
    n_target_z = int(round(kz_target * Lz / (2 * math.pi)))
    kx = 2.0 * math.pi * n_target_x / Lx
    ky = 2.0 * math.pi * n_target_y / Ly
    kz = 2.0 * math.pi * n_target_z / Lz

    D = cdb.build_D_k_matrix(kx, ky, kz, m, sign=sign)
    eigvals, eigvecs = np.linalg.eig(D)

    w = float(cdb.bcc_dirac_dispersion(
        np.array(kx), np.array(ky), np.array(kz), m, sign=sign))
    target = np.exp(1j * w)
    idx = int(np.argmin(np.abs(eigvals - target)))
    v = eigvecs[:, idx].astype(complex)

    # Phase-normalise so the first non-tiny component is real-positive
    pivot = None
    for j in range(4):
        if abs(v[j]) > 1e-12:
            pivot = j
            break
    if pivot is not None:
        v = v * np.exp(-1j * np.angle(v[pivot]))
    v = v / np.linalg.norm(v)
    return kx, ky, kz, w, v


def make_plane_wave_3d(L, kx0, ky0, kz0, m, sign='+'):
    """Build a pure plane wave on (L,L,L) at on-shell (kx, ky, kz)."""
    kx_g, ky_g, kz_g, w, v = positive_freq_eigenmode_3d(
        kx0, ky0, kz0, m, L, L, L, sign=sign)
    X, Y, Z = np.meshgrid(np.arange(L), np.arange(L), np.arange(L),
                          indexing='ij')
    phase = np.exp(1j * (kx_g * X + ky_g * Y + kz_g * Z))
    base = phase / math.sqrt(L * L * L)   # uniform-amplitude normalisation
    eta_u = v[0] * base
    eta_d = v[1] * base
    chi_u = v[2] * base
    chi_d = v[3] * base
    return eta_u, eta_d, chi_u, chi_d, kx_g, ky_g, kz_g, w, v


def measure_plane_wave_phase_rate_3d_exact(L, m, kx0, n_steps,
                                           dt=1.0, static=False,
                                           sign='+'):
    """Propagate a pure 3D plane wave and measure phase rotation along
       either the lattice centre (static) or the worldline x(t)=v_g·t.

       Worldline read uses FFT-based sub-pixel sampling — no integer cell
       rounding noise, identical strategy to the 2D test."""
    if static:
        eu, ed, cu_, cd_, kxg, kyg, kzg, w, v = make_plane_wave_3d(
            L, 0.0, 0.0, 0.0, m, sign=sign)
    else:
        eu, ed, cu_, cd_, kxg, kyg, kzg, w, v = make_plane_wave_3d(
            L, kx0, 0.0, 0.0, m, sign=sign)

    n_kin = math.sqrt(1.0 - m * m)
    sw = math.sin(w)
    if sw > 1e-15:
        # ∂ω/∂k_x at (k_x, 0, 0) along x: (n · s_x/√3) / sin(ω)
        s_xg = math.sin(kxg * INV_ROOT3)
        vg = (n_kin * s_xg * INV_ROOT3) / sw
    else:
        vg = 0.0

    samples = np.zeros(n_steps + 1, dtype=complex)

    def read_at(eta_u_field, cx_frac):
        """FFT-shift along axis-0 by `cx_frac` cells, then sample
           (0, L//2, L//2)."""
        F = np.fft.fft(eta_u_field, axis=0)
        kx_grid = np.fft.fftfreq(L) * 2 * math.pi
        phase_shift = np.exp(-1j * kx_grid * cx_frac)
        F_shifted = F * phase_shift[:, None, None]
        shifted = np.fft.ifft(F_shifted, axis=0)
        return shifted[0, L // 2, L // 2]

    centre = (L // 2, L // 2, L // 2)
    samples[0] = (eu[centre] if static
                  else read_at(eu, L // 2 + 0.0))

    for step in range(1, n_steps + 1):
        eu, ed, cu_, cd_ = cdb.dirac_step_3d_bcc_splitstep(
            eu, ed, cu_, cd_, m=m, dt=dt, sign=sign)
        if static:
            samples[step] = eu[centre]
        else:
            samples[step] = read_at(eu, L // 2 + vg * step * dt)

    return samples, vg, kxg, w


def extract_phase_rate(samples, dt):
    """Unwrap and least-squares fit a linear slope.  Returns |ω|."""
    phases = np.unwrap(np.angle(samples))
    t = np.arange(len(samples)) * dt
    A = np.vstack([t, np.ones_like(t)]).T
    slope, _intercept = np.linalg.lstsq(A, phases, rcond=None)[0]
    return abs(slope)


def part_B_propagation(L=48, m=0.1, kx0=0.05, n_steps=400, dt=1.0,
                       sign='+'):
    """Two pure-plane-wave propagations (static + moving) on the 3D BCC
       Dirac, compare phase-rotation frequencies, report num-vs-pred and
       num-vs-SR residuals."""
    print("=" * 96)
    print("Part B — Numerical propagation (3D BCC Dirac plane wave)")
    print("=" * 96)
    print(f"  L={L}, m={m}, kx0={kx0}, n_steps={n_steps}, dt={dt}, sign={sign!r}")
    print()

    samples_s, vg_s, kxg_s, w_s = measure_plane_wave_phase_rate_3d_exact(
        L, m, kx0, n_steps, dt=dt, static=True, sign=sign)
    samples_m, vg_m, kxg_m, w_m = measure_plane_wave_phase_rate_3d_exact(
        L, m, kx0, n_steps, dt=dt, static=False, sign=sign)

    omega_s_num = extract_phase_rate(samples_s, dt)
    omega_m_num = extract_phase_rate(samples_m, dt)

    omega_s_pred = omega_static_qca(m)
    omega_m_pred = abs(w_m - kxg_m * vg_m)

    print(f"Static plane wave (k=0):")
    print(f"  ω_predicted (arcsin m)  = {omega_s_pred:.12f}")
    print(f"  ω_measured              = {omega_s_num:.12f}")
    print(f"  abs error               = {abs(omega_s_num - omega_s_pred):.3e}")
    print()
    print(f"Moving plane wave (snapped k_x = {kxg_m:.6f}, v_g = {vg_m:.6f}):")
    print(f"  ω_predicted (ω_k − k v_g) = {omega_m_pred:.12f}")
    print(f"  ω_measured                = {omega_m_num:.12f}")
    print(f"  abs error                 = {abs(omega_m_num - omega_m_pred):.3e}")
    print()

    ratio_num  = omega_m_num  / omega_s_num
    ratio_pred = omega_m_pred / omega_s_pred
    beta = vg_m / C_LAT_3D
    inv_gamma = math.sqrt(1.0 - beta * beta) if abs(beta) < 1.0 else float('nan')

    print(f"Time-dilation ratio:")
    print(f"  ratio_num   = ω_moving_num / ω_static_num   = {ratio_num:.12f}")
    print(f"  ratio_pred  = (ω_k − k v_g)/arcsin(m)       = {ratio_pred:.12f}")
    print(f"  1/γ_SR      = √(1 − (v_g/c_lat)²)           = {inv_gamma:.12f}")
    print()
    print(f"  Residual num-vs-pred  = {abs(ratio_num - ratio_pred):.3e}")
    print(f"  Residual num-vs-SR    = {abs(ratio_num - inv_gamma):.3e}")
    print(f"  Residual pred-vs-SR   = {abs(ratio_pred - inv_gamma):.3e}")

    return {
        'omega_s_pred': omega_s_pred, 'omega_s_num': omega_s_num,
        'omega_m_pred': omega_m_pred, 'omega_m_num': omega_m_num,
        'ratio_num': ratio_num, 'ratio_pred': ratio_pred,
        'inv_gamma': inv_gamma, 'vg': vg_m, 'kxg': kxg_m,
    }


def part_B_scan(L=32, n_steps=200, dt=1.0, sign='+'):
    """Velocity scan: numerical ratio vs 1/γ across a (m, k) grid on the
       3D BCC lattice."""
    print("=" * 96)
    print("Part B scan — Numerical propagation across (m, k) on 3D BCC")
    print("=" * 96)
    print(f"  L={L}, n_steps={n_steps}, dt={dt}, sign={sign!r}")
    print()
    print(f"{'m':>6} {'k_target':>10} {'k_snap':>10} {'v_g':>10} {'v_g/c_lat':>10} "
          f"{'ratio_num':>13} {'1/γ_SR':>13} {'num-vs-SR':>11} {'num-vs-pred':>11}")
    print("-" * 122)
    rows = []
    grid = [
        (0.05, 0.005), (0.05, 0.01), (0.05, 0.05), (0.05, 0.1),
        (0.10, 0.01), (0.10, 0.05), (0.10, 0.1),
        (0.20, 0.05), (0.20, 0.1),  (0.20, 0.2),
        (0.50, 0.05), (0.50, 0.1),  (0.50, 0.2),  (0.50, 0.3),
    ]
    for m, kx in grid:
        s_s, _, _, _ = measure_plane_wave_phase_rate_3d_exact(
            L, m, kx, n_steps, dt=dt, static=True, sign=sign)
        s_m, vg, kxg, w = measure_plane_wave_phase_rate_3d_exact(
            L, m, kx, n_steps, dt=dt, static=False, sign=sign)
        ws_num = extract_phase_rate(s_s, dt)
        wm_num = extract_phase_rate(s_m, dt)
        ws_pred = omega_static_qca(m)
        wm_pred = abs(w - kxg * vg)
        ratio_num  = wm_num / ws_num
        ratio_pred = wm_pred / ws_pred
        beta = vg / C_LAT_3D
        inv_gamma = math.sqrt(1.0 - beta * beta) if abs(beta) < 1.0 else float('nan')
        print(f"{m:6.3f} {kx:10.4f} {kxg:10.6f} {vg:10.6f} {beta:10.6f} "
              f"{ratio_num:13.10f} {inv_gamma:13.10f} {abs(ratio_num-inv_gamma):11.3e} "
              f"{abs(ratio_num-ratio_pred):11.3e}")
        rows.append((m, kx, kxg, vg, beta, ratio_num, ratio_pred, inv_gamma))
    return rows


# ══════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print()
    rows_A = part_A_scan()
    print()
    out = part_B_propagation(L=48, m=0.1, kx0=0.05, n_steps=400, dt=1.0)
    print()
    rows_B = part_B_scan(L=32, n_steps=200, dt=1.0)
    print()

    # Bottom line
    print("=" * 96)
    print("SR-2 (3D BCC) — Bottom line")
    print("=" * 96)
    print(f"Algebraic test:  ratio_QCA → 1/γ_SR at leading order in (k, m);")
    print(f"  c_lat = 1/√3, residual scales as O(k²) (BCC dispersion correction).")
    print()
    print(f"Numerical test:  the BCC Dirac propagator reproduces the dispersion-derived")
    print(f"  prediction to <{abs(out['ratio_num'] - out['ratio_pred']):.1e}.")
    print()
    print(f"Roadmap gate (dispersion-identity, 1e-12):")
    print(f"  num-vs-pred = {abs(out['ratio_num'] - out['ratio_pred']):.1e}")
    print(f"Roadmap gate (continuum-SR, O(k²) at small k):")
    print(f"  pred-vs-SR  = {abs(out['ratio_pred'] - out['inv_gamma']):.1e}  at  v_g/c_lat = {out['vg']/C_LAT_3D:.4f}")
    print()
