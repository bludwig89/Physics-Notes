"""
curl_fork_harness.py  —  cross-geometry diagnostics for the curl-O(k) question
==============================================================================
Runs identical measurements on each geometry fork (BCC baseline vs the
simple-cubic candidate) to answer: is the composite-photon curl residual's
O(k) scaling caused by the BCC geometry, and would simple-cubic geometry
(which gives c_lat = 1) fix it?

Measured per geometry
---------------------
  c_lat (axis, diagonal)   small-k ω/|k|
  dispersion isotropy      ω(diag)/ω(axis) at fixed small |k|
  curl residual k-scan     residual(k) over decades; log-log slope = scaling
                           exponent; residual/k as k→0 = leading coefficient
  fermion doublers         number of ω≈0 modes on the FFT simulation grid

Self-check: the BCC arm must reproduce Finding 2 (curl/k → 1/√6 = 0.40825,
scaling exponent 1).

Run:  python3 forks/curl_fork_harness.py
Writes: test-results/curl_fork_results_<date>.json
"""
import os, sys, json, time
import numpy as np

# locate ca-simulation package
HERE = os.path.dirname(os.path.abspath(__file__))
CASIM = os.path.dirname(HERE)
for cand in (CASIM, HERE,
             "/sessions/blissful-epic-faraday/mnt/Physics Notes/ca-simulation"):
    if os.path.isfile(os.path.join(cand, "ca_bcc.py")):
        sys.path.insert(0, cand)
        sys.path.insert(0, os.path.join(cand, "forks"))
        CASIM = cand
        break

import ca_maxwell as mx
from ca_fft import fftfreq
import curl_fork_baseline_bcc as bcc_fork
import curl_fork_cubic as cub_fork

SQRT6 = np.sqrt(6.0)
SQRT3 = np.sqrt(3.0)


# ──────────────────────────────────────────────────────────────────
#  Generic diagnostics (parameterised by a geometry fork module)
# ──────────────────────────────────────────────────────────────────
def curl_residual(fork, k_mag, n_dirs=8, seed=0):
    """Composite-photon curl residual for `fork`, mirroring
    ca_maxwell.maxwell_curl_residual but with the fork's uvec/eigenmodes.
    Returns (curl_E_err, curl_B_err) normalised by |E|+|B|."""
    dirs = mx._random_dirs(n_dirs, seed=seed)
    errsE, errsB = [], []
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, psi_m, omega_half = fork.eigenmodes(kh[0], kh[1], kh[2])
        psi, phi = psi_p, psi_m
        _, nx, ny, nz = fork.uvec(kh[0], kh[1], kh[2])
        n_half = np.array([float(nx), float(ny), float(nz)])
        E0, B0 = mx.EM_bilinears(psi, phi, n_half)
        ph = np.exp(-1j * omega_half)            # dt = 1
        Et, Bt = mx.EM_bilinears(psi * ph, phi * ph, n_half)
        dE, dB = Et - E0, Bt - B0
        two_n = 2.0 * n_half
        rhsE = 1j * np.cross(two_n, B0)
        rhsB = -1j * np.cross(two_n, E0)
        denom = np.linalg.norm(E0) + np.linalg.norm(B0) + 1e-30
        errsE.append(float(np.linalg.norm(dE - rhsE) / denom))
        errsB.append(float(np.linalg.norm(dB - rhsB) / denom))
    return max(errsE), max(errsB)


def emergent_c(fork, k_small=1e-4):
    """Return c_lat measured along the x-axis and the body diagonal."""
    c_axis = float(fork.dispersion(k_small, 0.0, 0.0)) / k_small
    dh = k_small / SQRT3
    c_diag = float(fork.dispersion(dh, dh, dh)) / k_small
    return c_axis, c_diag


def dispersion_isotropy(fork, k_mag=0.1):
    """ω(diagonal)/ω(axis) at fixed |k|.  1.0 => isotropic."""
    w_axis = float(fork.dispersion(k_mag, 0.0, 0.0))
    dh = k_mag / SQRT3
    w_diag = float(fork.dispersion(dh, dh, dh))
    return w_diag / w_axis


def count_doublers(fork, N=12, tol=1e-9):
    """Count ω≈0 modes on the N^3 FFT simulation grid (the grid the
    steppers actually sample).  N even so k_i=±π is hit."""
    k = fftfreq(N) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    w = fork.dispersion(KX, KY, KZ)
    return int(np.count_nonzero(np.asarray(w) < tol))


def loglog_slope(ks, res):
    ks, res = np.asarray(ks, float), np.asarray(res, float)
    A = np.vstack([np.log(ks), np.ones_like(ks)]).T
    slope, intercept = np.linalg.lstsq(A, np.log(res), rcond=None)[0]
    return float(slope), float(np.exp(intercept))


# ──────────────────────────────────────────────────────────────────
#  Run
# ──────────────────────────────────────────────────────────────────
def run():
    forks = {"bcc": bcc_fork, "cubic": cub_fork}
    k_scan = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]
    out = {"meta": {"date": time.strftime("%Y-%m-%d %H:%M")}, "geometries": {}}

    for key, fk in forks.items():
        c_axis, c_diag = emergent_c(fk)
        iso = dispersion_isotropy(fk, 0.1)
        doublers = count_doublers(fk)
        curlE, curlB = [], []
        for kk in k_scan:
            e, b = curl_residual(fk, kk)
            curlE.append(e); curlB.append(b)
        slopeE, coeffE = loglog_slope(k_scan, curlE)
        # leading coefficient = residual/k extrapolated to k->0 (use smallest k)
        coeff_over_k = curlE[-1] / k_scan[-1]
        out["geometries"][key] = {
            "name": fk.GEOMETRY_NAME,
            "c_lat_axis": c_axis,
            "c_lat_diagonal": c_diag,
            "dispersion_isotropy_diag_over_axis": iso,
            "fermion_doublers_on_grid": doublers,
            "curl_residual_k_scan": dict(zip([f"{k:.0e}" for k in k_scan], curlE)),
            "curl_loglog_slope": slopeE,
            "curl_residual_over_k": coeff_over_k,
        }

    # self-check vs Finding 2
    bcc_coeff = out["geometries"]["bcc"]["curl_residual_over_k"]
    out["meta"]["bcc_self_check_vs_1_over_sqrt6"] = {
        "measured_curl_over_k": bcc_coeff,
        "expected_1_over_sqrt6": 1.0 / SQRT6,
        "rel_err": abs(bcc_coeff - 1.0/SQRT6) / (1.0/SQRT6),
    }
    return out


if __name__ == "__main__":
    res = run()
    # save
    outdir = os.path.join(os.path.dirname(CASIM), "test-results")
    os.makedirs(outdir, exist_ok=True)
    datestr = time.strftime("%Y-%m-%d")
    with open(os.path.join(outdir, f"curl_fork_results_{datestr}.json"), "w") as fh:
        json.dump(res, fh, indent=2)

    # pretty table
    g = res["geometries"]
    print("\n=== Curl-fork geometry comparison ===")
    hdr = f"{'metric':<34}{'BCC (baseline)':>20}{'simple-cubic':>20}"
    print(hdr); print("-" * len(hdr))
    rows = [
        ("c_lat (axis)", "c_lat_axis"),
        ("c_lat (diagonal)", "c_lat_diagonal"),
        ("dispersion isotropy (diag/axis)", "dispersion_isotropy_diag_over_axis"),
        ("fermion doublers (grid)", "fermion_doublers_on_grid"),
        ("curl residual log-log slope", "curl_loglog_slope"),
        ("curl residual / k  (k->0)", "curl_residual_over_k"),
    ]
    for label, kk in rows:
        bv, cv = g["bcc"][kk], g["cubic"][kk]
        if isinstance(bv, float):
            print(f"{label:<34}{bv:>20.6f}{cv:>20.6f}")
        else:
            print(f"{label:<34}{bv:>20}{cv:>20}")
    sc = res["meta"]["bcc_self_check_vs_1_over_sqrt6"]
    print(f"\nBCC self-check: curl/k = {sc['measured_curl_over_k']:.6f} vs "
          f"1/√6 = {sc['expected_1_over_sqrt6']:.6f}  (rel err {sc['rel_err']:.2e})")
    print(f"\n[saved] test-results/curl_fork_results_{datestr}.json")
