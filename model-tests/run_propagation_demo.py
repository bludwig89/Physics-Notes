"""
propagation_demo.py — Fresh propagation demonstration on the BCC lattice
========================================================================
Launches three real-space wavepackets and records them traversing the
L^3 BCC lattice, measuring group velocity from the energy-density centroid:

  1. Massless Weyl fermion   (ca_bcc.weyl_step_3d_bcc)
       predicted |v_g| = 1/sqrt(3) along k-hat, independent of |k|.
  2. Massive Dirac fermion   (ca_dirac_bcc.dirac_step_3d_bcc_splitstep, m=0.3)
       predicted |v_g| = dω/d|k| at k0 (slower than light; measured by
       finite-differencing the analytic BCC Dirac dispersion).
  3. Composite photon        (pair of correlated Weyl fields; bilinear
       G^i(x) = φ(x)^T σ^i ψ(x)).  Each Weyl field is a packet at mean
       momentum k0/2, so the bilinear is a photon packet at mean momentum
       k0, predicted |v_g| = 1/sqrt(3).

Also reports the machine-precision momentum-space gates (dispersion,
transversality, Poynting energy conservation) for the composite photon,
so the "exists + moves + conserves energy" claim is shown end-to-end.

Output: prints a JSON-ish result block and writes
  test-results/propagation_demo_<date>.json
  test-results/figures/propagation_demo.png
"""
import os, sys, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
# Allow running from anywhere: locate the ca-simulation package.
for cand in (HERE, os.path.join(HERE, "ca-simulation"),
             "/sessions/blissful-epic-faraday/mnt/Physics Notes/ca-simulation"):
    if os.path.isfile(os.path.join(cand, "ca_bcc.py")):
        sys.path.insert(0, cand)
        CASIM = cand
        break
else:
    raise SystemExit("Could not locate ca-simulation/ca_bcc.py")

import ca_bcc as bcc
import ca_dirac_bcc as dbcc
import ca_maxwell as mx
import ca_fft as fft

SQRT3 = np.sqrt(3.0)
RESULT = {"meta": {"casim_dir": CASIM, "date": time.strftime("%Y-%m-%d %H:%M")}}


# ──────────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────────
def gaussian_packet(L, center, sigma, k0):
    """Real-space Gaussian envelope * plane wave e^{i k0·x}, shape (L,L,L).

    sigma may be a scalar or a per-axis 3-tuple (sx, sy, sz).  A wide
    transverse width keeps the packet's transverse-k content small so the
    measured longitudinal group velocity is not dragged down by off-axis
    BCC modes (whose ∂ω/∂k_x < 1/√3).
    """
    s = np.atleast_1d(np.asarray(sigma, float))
    if s.size == 1:
        s = np.array([s[0], s[0], s[0]])
    ax = np.arange(L)
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r2 = ((X - center[0])/s[0])**2 + ((Y - center[1])/s[1])**2 + ((Z - center[2])/s[2])**2
    env = np.exp(-r2 / 2.0)
    phase = np.exp(1j * (k0[0]*X + k0[1]*Y + k0[2]*Z))
    return (env * phase).astype(np.complex128)


def plus_eigenspinor(k0, sign="+"):
    """2-spinor: the +ω eigenmode of the BCC Weyl unitary at k0 (unit norm)."""
    U_ff, U_fg, U_gf, U_gg = bcc.bcc_unitary(k0[0], k0[1], k0[2], sign=sign)
    M = np.array([[U_ff, U_fg], [U_gf, U_gg]], dtype=complex)
    w, v = np.linalg.eig(M)
    # +ω eigenmode: U = e^{-iω}, so phase = -angle(w); pick largest ω = -angle.
    omega = -np.angle(w)
    idx = int(np.argmax(omega))
    s = v[:, idx]
    return s / np.linalg.norm(s), float(omega[idx])


def centroid_x(rho):
    ax = np.arange(rho.shape[0])
    w = rho.sum(axis=(1, 2))
    return float((ax * w).sum() / w.sum())


def fit_velocity(steps, xs):
    """Least-squares slope of centroid-x vs step index = group velocity (cells/step)."""
    A = np.vstack([steps, np.ones_like(steps)]).T
    slope, _ = np.linalg.lstsq(A, xs, rcond=None)[0]
    return float(slope)


# ──────────────────────────────────────────────────────────────────
#  Run config
# ──────────────────────────────────────────────────────────────────
L = 64
SIGMA = (6.0, 10.0, 10.0)        # compact along propagation (x), wide transverse
N_STEPS = 44
SAMPLE = 2                       # record centroid every SAMPLE steps
KHAT = np.array([1.0, 0.0, 0.0])  # propagate along x for clean centroid
KMAG = 0.8                        # mid-BZ; safely inside |k_i/√3|<0.6 region
K0 = KMAG * KHAT
center0 = np.array([14.0, L/2, L/2])

t_start = time.time()

# ══════════════════════════════════════════════════════════════════
#  1. Massless Weyl fermion packet
# ══════════════════════════════════════════════════════════════════
spinor, omega_w = plus_eigenspinor(K0)
env = gaussian_packet(L, center0, SIGMA, K0)
f = spinor[0] * env
g = spinor[1] * env

steps_rec, xs_w = [], []
for n in range(N_STEPS + 1):
    if n % SAMPLE == 0:
        rho = np.abs(f)**2 + np.abs(g)**2
        steps_rec.append(n); xs_w.append(centroid_x(rho))
    if n < N_STEPS:
        f, g = bcc.weyl_step_3d_bcc(f, g, sign="+")

steps_rec = np.array(steps_rec, float)
vg_weyl = fit_velocity(steps_rec, np.array(xs_w))
RESULT["weyl_fermion"] = {
    "measured_vg_cells_per_step": vg_weyl,
    "predicted_vg": 1.0 / SQRT3,
    "rel_err": abs(vg_weyl - 1.0/SQRT3) / (1.0/SQRT3),
    "centroid_start": xs_w[0], "centroid_end": xs_w[-1],
    "cells_traversed": xs_w[-1] - xs_w[0],
}

# ══════════════════════════════════════════════════════════════════
#  2. Massive Dirac fermion packet (m = 0.3)
# ══════════════════════════════════════════════════════════════════
M_DIRAC = 0.3
# predicted group velocity: dω/d|k| at K0 via central finite difference
h = 1e-4
wp = float(dbcc.bcc_dirac_dispersion((KMAG+h)*KHAT[0], (KMAG+h)*KHAT[1], (KMAG+h)*KHAT[2], M_DIRAC))
wm = float(dbcc.bcc_dirac_dispersion((KMAG-h)*KHAT[0], (KMAG-h)*KHAT[1], (KMAG-h)*KHAT[2], M_DIRAC))
vg_dirac_pred = (wp - wm) / (2*h)

# Build a 4-spinor packet from the *positive-energy Dirac eigenmode* of D_k
# at k0 (else an η-only seed mixes ±energy modes → zitterbewegung smears v_g).
D = dbcc.build_D_k_matrix(K0[0], K0[1], K0[2], M_DIRAC, sign="+")
dw, dv = np.linalg.eig(D)
omega_dk = float(dbcc.bcc_dirac_dispersion(K0[0], K0[1], K0[2], M_DIRAC))
# positive-energy branch: eigenvalue e^{-iω} → angle ≈ -ω
idx_pos = int(np.argmin(np.abs(np.angle(dw) - (-omega_dk))))
spinor4 = dv[:, idx_pos] / np.linalg.norm(dv[:, idx_pos])
env = gaussian_packet(L, center0, SIGMA, K0)
eta_u = spinor4[0] * env
eta_d = spinor4[1] * env
chi_u = spinor4[2] * env
chi_d = spinor4[3] * env

steps_rec2, xs_d = [], []
for n in range(N_STEPS + 1):
    if n % SAMPLE == 0:
        rho = (np.abs(eta_u)**2 + np.abs(eta_d)**2
               + np.abs(chi_u)**2 + np.abs(chi_d)**2)
        steps_rec2.append(n); xs_d.append(centroid_x(rho))
    if n < N_STEPS:
        eta_u, eta_d, chi_u, chi_d = dbcc.dirac_step_3d_bcc_splitstep(
            eta_u, eta_d, chi_u, chi_d, m=M_DIRAC, dt=1.0, sign="+")

vg_dirac = fit_velocity(np.array(steps_rec2, float), np.array(xs_d))
RESULT["dirac_fermion"] = {
    "mass_m": M_DIRAC,
    "measured_vg_cells_per_step": vg_dirac,
    "predicted_vg_dwdk": vg_dirac_pred,
    "rel_err": abs(vg_dirac - vg_dirac_pred) / abs(vg_dirac_pred),
    "c_lat": 1.0/SQRT3,
    "vg_over_clat": vg_dirac / (1.0/SQRT3),
    "centroid_start": xs_d[0], "centroid_end": xs_d[-1],
    "cells_traversed": xs_d[-1] - xs_d[0],
}

# ══════════════════════════════════════════════════════════════════
#  3. Composite-photon packet (two correlated Weyl fields at k0/2)
# ══════════════════════════════════════════════════════════════════
Q0 = K0 / 2.0                      # each Weyl field carries half the photon momentum
sp_half, omega_half = plus_eigenspinor(Q0)
env_h = gaussian_packet(L, center0, SIGMA, Q0)
# two correlated Weyl fields ψ and φ (both + helicity eigenmode at q0)
psi_u = sp_half[0] * env_h; psi_d = sp_half[1] * env_h
phi_u = sp_half[0] * env_h; phi_d = sp_half[1] * env_h

_SX = np.array([[0,1],[1,0]], complex)
_SY = np.array([[0,-1j],[1j,0]], complex)
_SZ = np.array([[1,0],[0,-1]], complex)

def photon_energy_density(pu, pd, fu, fd):
    """Pointwise bilinear G^i(x)=φ^T σ^i ψ; energy proxy Σ_i |G^i(x)|^2."""
    # G^x = φ_u ψ_d + φ_d ψ_u ; G^y = -i φ_u ψ_d + i φ_d ψ_u ; G^z = φ_u ψ_u - φ_d ψ_d
    Gx = fu*pd + fd*pu
    Gy = -1j*fu*pd + 1j*fd*pu
    Gz = fu*pu - fd*pd
    return np.abs(Gx)**2 + np.abs(Gy)**2 + np.abs(Gz)**2

steps_rec3, xs_p = [], []
for n in range(N_STEPS + 1):
    if n % SAMPLE == 0:
        rho = photon_energy_density(psi_u, psi_d, phi_u, phi_d)
        steps_rec3.append(n); xs_p.append(centroid_x(rho))
    if n < N_STEPS:
        psi_u, psi_d = bcc.weyl_step_3d_bcc(psi_u, psi_d, sign="+")
        phi_u, phi_d = bcc.weyl_step_3d_bcc(phi_u, phi_d, sign="+")

vg_photon = fit_velocity(np.array(steps_rec3, float), np.array(xs_p))
RESULT["composite_photon"] = {
    "measured_vg_cells_per_step": vg_photon,
    "predicted_vg": 1.0 / SQRT3,
    "rel_err": abs(vg_photon - 1.0/SQRT3) / (1.0/SQRT3),
    "photon_mean_k": KMAG,
    "centroid_start": xs_p[0], "centroid_end": xs_p[-1],
    "cells_traversed": xs_p[-1] - xs_p[0],
}

# ── momentum-space machine-precision gates (existing verified functions) ──
disp_res = mx.maxwell_dispersion_residual(k_mag=0.05)
trans_res = mx.maxwell_transversality(k_mag=0.05)
energy = mx.composite_photon_energy_conservation_c2(k_mag=0.05, n_steps=200, n_dirs=8)
RESULT["photon_momentum_space_gates"] = {
    "dispersion_residual_rel": float(disp_res),
    "transversality_residual": float(trans_res),
    "poynting_energy_drift_200steps": float(energy if np.isscalar(energy) else np.max(energy)),
}

RESULT["meta"]["wall_seconds"] = time.time() - t_start

# ──────────────────────────────────────────────────────────────────
#  Save JSON + figure
# ──────────────────────────────────────────────────────────────────
outdir = os.path.join(os.path.dirname(CASIM), "test-results")
figdir = os.path.join(outdir, "figures")
os.makedirs(figdir, exist_ok=True)
datestr = time.strftime("%Y-%m-%d")
with open(os.path.join(outdir, f"propagation_demo_{datestr}.json"), "w") as fh:
    json.dump(RESULT, fh, indent=2)

# also drop a copy next to the script for convenience
with open(os.path.join(HERE, f"propagation_demo_{datestr}.json"), "w") as fh:
    json.dump(RESULT, fh, indent=2)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(steps_rec, xs_w, "o-", label=f"Weyl fermion  v={vg_weyl:.4f}")
    ax.plot(steps_rec2, xs_d, "s-", label=f"Dirac m=0.3   v={vg_dirac:.4f}")
    ax.plot(steps_rec3, xs_p, "^-", label=f"composite γ   v={vg_photon:.4f}")
    ax.axhline(L, color="k", ls=":", lw=0.8)
    # light-cone reference line
    ax.plot(steps_rec, xs_w[0] + (1/SQRT3)*steps_rec, "k--", lw=1,
            label="c_lat = 1/√3")
    ax.set_xlabel("CA tick"); ax.set_ylabel("energy-density centroid  x (cells)")
    ax.set_title("Wavepackets traversing the BCC lattice")
    ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout()
    figpath = os.path.join(figdir, "propagation_demo.png")
    fig.savefig(figpath, dpi=120)
    RESULT["meta"]["figure"] = figpath
except Exception as e:
    RESULT["meta"]["figure_error"] = str(e)

print(json.dumps(RESULT, indent=2))
