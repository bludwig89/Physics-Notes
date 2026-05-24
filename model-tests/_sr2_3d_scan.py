"""On-grid k scan for the 3D BCC SR-2 test — characterises residuals
   across (L, k_mode, m).  Static run cached per m to halve runtime."""
import sys, os, math, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ca-simulation'))
import numpy as np
import test_SR2_3D_time_dilation as t

configs = [
    (32, 1, 0.10),
    (32, 2, 0.10),
    (32, 3, 0.10),
    (32, 1, 0.30),
    (32, 2, 0.30),
    (32, 1, 0.50),
    (32, 3, 0.50),
    (48, 1, 0.10),
    (48, 2, 0.10),
    (48, 1, 0.30),
]

hdr = ("L", "n", "m", "k_x", "v_g", "v_g/c_lat",
       "ratio_num", "1/g_SR", "num-vs-pred", "num-vs-SR")
print(f"{hdr[0]:>4} {hdr[1]:>3} {hdr[2]:>5} {hdr[3]:>10} {hdr[4]:>10} "
      f"{hdr[5]:>10} {hdr[6]:>13} {hdr[7]:>13} {hdr[8]:>12} {hdr[9]:>11}")
print('-'*120)

n_steps = 80
# Cache the static phase rate for each (L, m) pair
static_cache = {}
t0 = time.time()
for L, n_mode, m in configs:
    if (L, m) in static_cache:
        ws_num = static_cache[(L, m)]
    else:
        s_s, _, _, _ = t.measure_plane_wave_phase_rate_3d_exact(
            L, m, 0.0, n_steps, dt=1.0, static=True)
        ws_num = t.extract_phase_rate(s_s, 1.0)
        static_cache[(L, m)] = ws_num
    k_target = 2*math.pi*n_mode/L
    s_m, vg, kxg, w = t.measure_plane_wave_phase_rate_3d_exact(
        L, m, k_target, n_steps, dt=1.0, static=False)
    wm_num = t.extract_phase_rate(s_m, 1.0)
    ws_pred = t.omega_static_qca(m)
    wm_pred = abs(w - kxg*vg)
    rn = wm_num / ws_num
    rp = wm_pred / ws_pred
    beta = vg / t.C_LAT_3D
    ig = math.sqrt(1.0 - beta*beta) if abs(beta) < 1 else float('nan')
    print(f"{L:>4} {n_mode:>3} {m:>5.2f} {kxg:>10.6f} {vg:>10.6f} "
          f"{beta:>10.6f} {rn:>13.10f} {ig:>13.10f} "
          f"{abs(rn-rp):>12.3e} {abs(rn-ig):>11.3e}")
print(f"\nTotal: {time.time()-t0:.1f}s")
