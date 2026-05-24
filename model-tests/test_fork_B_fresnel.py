"""
test_fork_B_fresnel.py  —  Fork B: Fizeau/refractive-index test
==============================================================
Determines whether the existing variable-c CA model reproduces the
Fresnel/Fizeau formula for a moving refractive medium:

    v_c = c / n + (1 - 1/n²) · V              (paper eq. 18.31)

Two parts:
  Part 1 — Static medium: v_g = c_0/n.  Expected PASS (trivial in our
           model since c is the local lattice speed).
  Part 2 — Drifting slab: c(x, t) = c_0/n inside a slab of width W
           centred at x_0 + V·t, c_0 outside.  A photon traverses the
           moving slab.  Does the measured transit velocity match
           Fresnel, or does it equal c_0/n regardless of V?

The latter would falsify the dynamic-Fresnel part of Fork B — our CA's
c-field is a *lab-frame* parameter, not a Lorentz-rest-frame property of
a moving medium.
"""

import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ca-simulation'))

import ca_core as ca
import ca_curved as cc

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)


# ──────────────────────────────────────────────────────────────────
#  Part 1 — Static uniform medium: v_g = c_0/n at several n.
# ──────────────────────────────────────────────────────────────────

def part1_static_index():
    print('\n' + '=' * 72)
    print('  Fork B, Part 1 — static uniform medium: does v_g = c_0/n?')
    print('=' * 72)

    L = 128
    c_raw = 0.5
    sigma = 8.0
    k0 = (0.4, 0.0)
    n_steps = 80

    print(f'  L={L}, c_raw={c_raw}, sigma={sigma}, k0={k0}')
    print(f'  {"n":>5}  {"c_eff=c_raw/n":>14}  {"v_g_measured":>14}  '
          f'{"ratio":>8}  {"norm_drift":>12}')
    print('  ' + '-' * 65)

    results = []
    for n in (1.0, 1.5, 2.0, 3.0, 5.0):
        c_eff = c_raw / n
        c_field = np.full((L, L), c_eff)

        f, g = ca._gaussian_packet_2d(L, k0, sigma=sigma)
        solver = cc.CayleyVarcSolver2D(c_field, dt=1.0, n_sub=2)
        norm0 = float(np.sum(np.abs(f)**2 + np.abs(g)**2))

        xs = np.arange(L)
        X, Y = np.meshgrid(xs, xs, indexing='ij')
        centroids = []
        for step in range(n_steps + 1):
            d = np.abs(f)**2 + np.abs(g)**2
            tot = float(d.sum())
            cx = float((X * d).sum() / tot)
            cy = float((Y * d).sum() / tot)
            centroids.append((cx, cy))
            if step < n_steps:
                f, g = solver.step(f, g)

        norm1 = float(np.sum(np.abs(f)**2 + np.abs(g)**2))
        centroids = np.array(centroids)
        ts = np.arange(n_steps + 1)
        # Use mid-window slice (avoid initial transient & wrap-around)
        fit = slice(n_steps // 4, 3 * n_steps // 4)
        vx = float(np.polyfit(ts[fit], centroids[fit, 0], 1)[0])
        vy = float(np.polyfit(ts[fit], centroids[fit, 1], 1)[0])
        v_meas = float(np.sqrt(vx * vx + vy * vy))
        ratio = v_meas / c_eff

        drift = abs(norm1 - norm0) / norm0
        print(f'  {n:>5.1f}  {c_eff:>14.4f}  {v_meas:>14.6f}  '
              f'{ratio:>8.4f}  {drift:>12.3e}')
        results.append({'n': n, 'c_eff': c_eff, 'v_meas': v_meas, 'ratio': ratio})

    # The relevant test for the static refractive-index *reinterpretation*
    # is whether v_g scales linearly with c_eff = c_raw/n.  The absolute
    # ratio carries a lattice-dispersion factor (cos(k_x) · CN-correction)
    # because the Cayley solver uses centered finite differences — same as
    # the 5° Snell offset we documented in Phase C1.  Test the *consistency*
    # of the ratio across n instead.
    ratios = [r['ratio'] for r in results]
    mean_ratio = float(np.mean(ratios))
    spread     = float(np.std(ratios))
    ok = spread / mean_ratio < 0.05      # all ratios within 5% of each other
    print(f"\n  Mean v_g/c_eff = {mean_ratio:.4f}  ±  {spread:.4f}")
    print(f"  Part 1 verdict: {'PASS' if ok else 'FAIL'}  (linear scaling "
          f'v_g ∝ c_eff holds to {spread/mean_ratio:.2%} — '
          f'consistent with the static-medium refractive-index reading).')
    print(f"  Caveat: absolute factor ~{mean_ratio:.2f} is the centered-")
    print(f"          finite-difference lattice dispersion of the Cayley")
    print(f"          stepper (cos(k_x)≈0.92 at k_x=0.4 plus Crank–Nicolson")
    print(f"          correction); it is *not* a Fresnel/refractive-index")
    print(f"          effect.  An 8-neighbor isotropic stencil (Fork A)")
    print(f"          would close the gap.")
    return ok, results


# ──────────────────────────────────────────────────────────────────
#  Part 2 — Drifting slab: photon traverses a moving medium.
# ──────────────────────────────────────────────────────────────────

def part2_drifting_slab():
    print('\n' + '=' * 72)
    print('  Fork B, Part 2 — drifting slab: does v_c = c/n + (1-1/n²)V hold?')
    print('=' * 72)

    L = 64
    c_raw = 0.5
    n_idx = 2.0          # rest-frame refractive index
    W_slab = 28          # slab width along x
    sigma = 4.0
    k0 = (0.4, 0.0)      # photon along +x
    n_steps = 160
    edge_width = 2.0     # smooth slab edges with tanh of this width

    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    def c_field_at(t, V):
        """Slab of c = c_raw/n centred at x_0 + V·t, c_raw outside."""
        x_centre = (L // 2) + V * t
        inside = 0.5 * (1.0 + np.tanh((W_slab / 2 - np.abs(X - x_centre))
                                       / edge_width))
        return c_raw / n_idx * inside + c_raw * (1.0 - inside)

    # Predictions (small-V Fresnel):
    v_inside_static  = c_raw / n_idx
    v_outside        = c_raw
    print(f'  L={L}, c_raw={c_raw}, n={n_idx}, slab width={W_slab}, sigma={sigma}')
    print(f'  static photon-in-slab velocity (Fresnel V=0):   c/n = {v_inside_static:.4f}')

    print(f'  {"V":>6}  {"v_measured_in_slab":>20}  '
          f'{"Fresnel pred":>14}  {"Galilean pred":>14}  {"verdict":>10}')
    print('  ' + '-' * 75)

    rows = []
    V_grid = (0.0, 0.08, -0.08)
    refactor_every = 8   # refactor LU every N steps to save time
    for V in V_grid:
        # Photon starts to the LEFT of the slab; slab starts at lattice centre.
        f, g = ca._gaussian_packet_2d(L, k0, sigma=sigma,
                                       center=(L // 4, L // 2))

        solver = cc.CayleyVarcSolver2D(c_field_at(0.0, V), dt=1.0, n_sub=2)

        centroids_x = []
        c_local_trace = []
        for step in range(n_steps + 1):
            d = np.abs(f)**2 + np.abs(g)**2
            tot = float(d.sum())
            cx = float((X * d).sum() / tot)
            centroids_x.append(cx)
            # Sample local c at packet centroid
            c_local_trace.append(
                float(c_field_at(step, V)[int(round(cx)) % L,
                                            int(round(L // 2)) % L]))
            if step < n_steps:
                if step % refactor_every == 0:
                    # Update LU at evolving c-field
                    solver.refactor(c_field_at(step + 0.5, V))
                f, g = solver.step(f, g)

        centroids_x = np.array(centroids_x)
        c_local_trace = np.array(c_local_trace)

        # Identify steps where centroid is well inside the slab
        # (local c at centroid below midpoint of c_raw/n and c_raw).
        c_mid = 0.5 * (c_raw / n_idx + c_raw)
        in_slab = c_local_trace < c_mid
        if in_slab.sum() < 20:
            print(f'  {V:>6.2f}  {"<insufficient in-slab>":>20}')
            rows.append({'V': V, 'v_meas': None})
            continue
        in_idx = np.where(in_slab)[0]
        fit_lo, fit_hi = in_idx[5], in_idx[-5]   # avoid entrance/exit transient
        if fit_hi - fit_lo < 10:
            fit_lo, fit_hi = in_idx[0], in_idx[-1]
        ts = np.arange(n_steps + 1)
        v_meas = float(np.polyfit(ts[fit_lo:fit_hi],
                                   centroids_x[fit_lo:fit_hi], 1)[0])

        v_fresnel  = v_inside_static + (1.0 - 1.0 / (n_idx * n_idx)) * V
        v_galilean = v_inside_static + V
        # Verdict: which prediction does v_meas match?
        err_fresnel  = abs(v_meas - v_fresnel)
        err_galilean = abs(v_meas - v_galilean)
        err_static   = abs(v_meas - v_inside_static)
        nearest = min(('static', err_static),
                       ('fresnel', err_fresnel),
                       ('galilean', err_galilean), key=lambda r: r[1])[0]
        print(f'  {V:>+6.2f}  {v_meas:>20.6f}  {v_fresnel:>14.4f}  '
              f'{v_galilean:>14.4f}  {nearest:>10}')
        rows.append({'V': V, 'v_meas': v_meas, 'v_fresnel': v_fresnel,
                      'v_galilean': v_galilean, 'v_static': v_inside_static,
                      'nearest': nearest})

    # Plot: measured vs. predicted as a function of V.
    Vs_real = [r['V'] for r in rows if r.get('v_meas') is not None]
    vs_meas = [r['v_meas']     for r in rows if r.get('v_meas') is not None]
    vs_fr   = [r['v_fresnel']  for r in rows if r.get('v_meas') is not None]
    vs_gal  = [r['v_galilean'] for r in rows if r.get('v_meas') is not None]
    vs_st   = [r['v_static']   for r in rows if r.get('v_meas') is not None]
    fig, ax = plt.subplots(figsize=(8, 5))
    Vs_sort = np.argsort(Vs_real)
    Vs_a = np.array(Vs_real)[Vs_sort]
    ax.plot(Vs_a, np.array(vs_meas)[Vs_sort], 'ko-', label='measured')
    ax.plot(Vs_a, np.array(vs_fr)[Vs_sort],   'b--', label='Fresnel c/n + (1-1/n²)V')
    ax.plot(Vs_a, np.array(vs_gal)[Vs_sort],  'r:',  label='Galilean c/n + V')
    ax.plot(Vs_a, np.array(vs_st)[Vs_sort],   'g--', label='static c/n')
    ax.set_xlabel('slab drift velocity V')
    ax.set_ylabel('photon group velocity inside slab')
    ax.legend(); ax.grid(alpha=0.3)
    ax.set_title('Fork B Part 2 — drifting slab Fresnel test')
    out = os.path.join(FIGURES_DIR, 'forkB_fresnel_drifting_slab.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()

    # Verdict: count how many rows match each predicted regime
    counts = {'static': 0, 'fresnel': 0, 'galilean': 0}
    for r in rows:
        if r.get('nearest'):
            counts[r['nearest']] += 1
    most = max(counts, key=counts.get)
    print(f'\n  Part 2 verdict: closest to {most.upper()} in '
          f'{counts[most]} / {sum(counts.values())} drift values.')
    print(f'  → Fork B (dynamic-Fresnel via c(x,t)): '
          f'{"CONFIRMED" if most == "fresnel" else "FALSIFIED"} for this CA.')
    return most == 'fresnel', rows


if __name__ == '__main__':
    ok1, _ = part1_static_index()
    ok2, _ = part2_drifting_slab()
    print('\n' + '=' * 72)
    print('  Fork B SUMMARY')
    print('=' * 72)
    print(f'  Part 1 (static index): {"PASS" if ok1 else "FAIL"}')
    print(f'  Part 2 (drifting slab Fresnel): '
          f'{"CONFIRMED" if ok2 else "FALSIFIED"}')
