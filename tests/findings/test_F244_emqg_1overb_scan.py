"""
test_F244 — 1/b scaling of 3-D EMQG lensing.
(exactness-inventory not-met #2; extends the F3b |Phi|^alpha scan)
===========================================================================
Move from the phenomenological metric c=c0*(|Phi|/v)^alpha (free alpha) to
the genuine 3-D EMQG Newtonian potential (ca_emqg.solve_poisson_3d, 1/r
Green's fn) with the GR-Shapiro coupling c=c0/(1-2phi/c0^2) (no alpha).
Three levels: (A) exact continuum closed-form thin lens = 2GMb/(b^2+sig^2)
-> 2GM/b (exact 1/b); (B) lattice thin-lens line integral on the isolated
and periodic slices; (C) Cayley exact-unitary stepper (dynamical, toward
mass, norm-conserving).
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'ca-simulation'))
RESULTS = os.path.join(HERE, '..', '..', 'test-results')
import ca_emqg as em
from ca_curved import CayleyVarcSolver2D


def thin_lens(c_field, cy, b):
    lnc = np.log(c_field); j = cy + b
    return float((0.5 * (lnc[:, j + 1] - lnc[:, j - 1])).sum())

def isolated_slice(L, M=1.0, sigma=3.0, G=0.006, c_0=0.4):
    x = np.arange(L); X, Y = np.meshgrid(x, x, indexing='ij')
    c = L // 2
    r = np.sqrt((X - c)**2 + (Y - c)**2 + sigma**2)
    return c_0 / (1.0 - 2.0 * (-G * M / r) / c_0**2), c

def periodic_slice(L, M=1.0, sigma=3.0, G=0.006, c_0=0.4):
    phi = em.solve_poisson_3d(em.gaussian_mass_3d(L, M=M, sigma=sigma), G=G)
    return em.c_field_from_phi(phi[:, :, L // 2], c_0=c_0), L // 2

def slope(bs, v):
    return float(np.polyfit(np.log(np.array(bs, float)), np.log(np.abs(v)), 1)[0])

def _mean_ky(f, g):
    L = f.shape[1]; ky = np.fft.fftfreq(L) * 2 * np.pi
    w = np.abs(np.fft.fft(f, axis=1))**2 + np.abs(np.fft.fft(g, axis=1))**2
    return float((w * ky[None, :]).sum() / w.sum())

def stepper_kick(b, L=100, sigma=3.0, G=0.006, c_0=0.4, n_steps=80,
                 pkt_sigma=5.0, k0=0.5):
    c_field, cy = periodic_slice(L, sigma=sigma, G=G, c_0=c_0)
    c_flat = np.full((L, L), c_0)
    x = np.arange(L); X, Y = np.meshgrid(x, x, indexing='ij')
    env = np.exp(-((X - L//4)**2 + (Y - (cy + b))**2) / (2*pkt_sigma**2))
    f0 = (env * np.exp(1j*k0*X)).astype(np.complex128); g0 = np.zeros_like(f0)
    n0 = float(np.sum(np.abs(f0)**2))
    sc = CayleyVarcSolver2D(c_field, dt=1.0, n_sub=2)
    sf = CayleyVarcSolver2D(c_flat, dt=1.0, n_sub=2)
    fc, gc = f0.copy(), g0.copy(); ff, gf = f0.copy(), g0.copy()
    for _ in range(n_steps):
        fc, gc = sc.step(fc, gc); ff, gf = sf.step(ff, gf)
    kick = _mean_ky(fc, gc) - _mean_ky(ff, gf)
    drift = abs(float(np.sum(np.abs(fc)**2 + np.abs(gc)**2)) - n0) / n0
    return float(kick), float(drift)


def run():
    # A. exact continuum closed form
    sig = 3.0
    b_cf = np.array([20, 40, 80, 160, 320, 640, 1280], float)
    dth_cf = b_cf / (b_cf**2 + sig**2)
    slope_cf = slope(list(b_cf), dth_cf)
    # b*Dtheta -> const as b>>sig; residual at largest b = sig^2/b^2 (exact 1/b)
    prod = b_cf * dth_cf
    resid_cf = float(abs(prod[-1] / prod.max() - 1.0))

    # B. lattice isolated + periodic
    c_iso, cy = isolated_slice(400)
    bs_A = [20, 30, 45, 65, 95, 130]
    slope_A = slope(bs_A, np.array([thin_lens(c_iso, cy, b) for b in bs_A]))
    c_per, cyp = periodic_slice(256)
    bs_B = [10, 15, 22, 32, 46]
    slope_B = slope(bs_B, np.array([thin_lens(c_per, cyp, b) for b in bs_B]))

    # C. stepper
    bs_C = [10, 16, 24]
    kicks = [stepper_kick(b) for b in bs_C]
    ok_toward = bool(all(k < 0 for k, _ in kicks))
    ok_norm = bool(all(dr < 1e-9 for _, dr in kicks))

    checks = [
        ("C1 continuum closed-form slope = -1 (EXACT 1/b)", abs(slope_cf + 1) < 0.02),
        ("C2 lattice isolated-slice slope ~ -1", abs(slope_A + 1) < 0.15),
        ("C3 lattice periodic-slice slope ~ -1 (b<<L/2)", abs(slope_B + 1) < 0.15),
        ("C4 stepper deflection toward mass", ok_toward),
        ("C5 Cayley norm conserved (<1e-9)", ok_norm),
    ]
    result = dict(closed_form_slope=slope_cf, isolated_slope=slope_A,
                  periodic_slope=slope_B,
                  stepper=dict(bs=bs_C, kicks=[k for k, _ in kicks],
                               drifts=[d for _, d in kicks]),
                  checks={k: bool(v) for k, v in checks})
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "F244_emqg_1overb_scan.json"), "w") as f:
        json.dump(result, f, indent=2)
    for k, v in checks:
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"  slopes: closed-form {slope_cf:.4f}, isolated {slope_A:.3f}, "
          f"periodic {slope_B:.3f}")
    npass = sum(1 for _, v in checks if v)
    print(f"F244: {npass}/{len(checks)} PASS")
    return npass == len(checks)


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
