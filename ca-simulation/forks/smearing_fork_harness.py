"""
smearing_fork_harness.py  —  f_k(q) smearing fork for the curl O(k) problem
=============================================================================

**Background (Finding 21)**
The composite-photon curl residual

    curl/|k| = c_lat/√2 ≈ 0.40825  (BCC)

is geometry-independent: it has log-log slope 1.0 (exact O(k)) and the
coefficient c_lat/√2 is fixed across all lattice geometries.  The residual
is intrinsic to the *un-smeared pointwise bilinear*
G^i(k) = ψ^T(k/2) σ^i ψ(k/2).

**This fork**
Tests Bisio et al. Paper 1's smearing function f_k(q): replace the pointwise
bilinear by a weighted average over nearby momentum-split pairs,

    G^i_smeared(k) = Σ_j w(q_j) ψ^T(k/2 + q_j) σ^i φ(k/2 − q_j)

with Gaussian weights  w(q) ∝ exp(−|q|²/(2σ²)).

**Why smearing should help**
Each displaced pair (k/2+q, k/2−q) satisfies Paper 1's exact curl identity
with *its own* n-vector n(k/2+q) rather than n(k/2).  The mismatch is

    i [2 n(k/2+q) − 2 n(k/2)] × B_j  ≈  2i (∂n/∂k)·q × B_j  =  O(q·k).

For an isotropic Gaussian centred at q=0 the first-order term averages to 0
by symmetry (<q> = 0), reducing the effective residual from O(k) to O(σ²/k).
k-proportional smearing (σ ∝ |k|) thus lifts the log-log slope from 1 → 2
and drives the coefficient toward 0 as k → 0.

**Smearing variants tested**
  1. σ = 0 (baseline): must reproduce c_lat/√2 (Finding 21 self-check).
  2. Fixed-width Gaussian: σ ∈ {0.005, 0.01, 0.02, 0.05, 0.1}
     (absolute units; tests the cross-over from slope-1 to slope-2 regime).
  3. k-proportional Gaussian: σ = α × |k|/2,  α ∈ {0.25, 0.5, 1.0, 2.0}
     (expected slope → 2; larger α buys a smaller coefficient).
  4. BCC-shell smearing: q drawn from the 8 BCC nearest-neighbour
     displacements ±h_j/2 × δ, scaled by δ.  Tests a geometry-motivated
     discrete smearing.

**Eigenmode convention (matching baseline)**
  φ = negative-energy eigenmode of U(k/2−q)   (psi_minus at k/2−q)
  ψ = positive-energy eigenmode of U(k/2+q)   (psi_plus  at k/2+q)
Both evolved as e^{-iω Δt} so G_j → e^{-iΩ_j} G_j with
Ω_j = ω(k/2+q_j) + ω(k/2−q_j).  At q=0 this reproduces the
maxwell_curl_residual() baseline exactly (curl/k → c_lat/√2).

**Measurements per variant**
  • log-log slope of curl residual vs k  (target: >1 means improvement)
  • leading coefficient curl/|k| as k→0  (target: <c_lat/√2)
  • effective photon frequency Ω_eff = Σ_j w_j Ω_j vs 2ω(k/2)
  • transversality: 2 n_{k/2} · E_smeared

Run:   python3 forks/smearing_fork_harness.py
Writes: test-results/smearing_fork_results_<date>.json
"""

import os
import sys
import json
import time
import numpy as np

# ── path resolution ──────────────────────────────────────────────────────────
HERE  = os.path.dirname(os.path.abspath(__file__))
CASIM = os.path.dirname(HERE)
for _cand in (CASIM, HERE,
              "/sessions/awesome-vibrant-feynman/mnt/Physics Notes/ca-simulation"):
    if os.path.isfile(os.path.join(_cand, "ca_bcc.py")):
        sys.path.insert(0, _cand)
        CASIM = _cand
        break

import ca_maxwell as mx
import ca_bcc     as bcc

# ── constants ─────────────────────────────────────────────────────────────────
SQRT2  = np.sqrt(2.0)
SQRT3  = np.sqrt(3.0)
C_LAT  = 1.0 / SQRT3               # BCC lattice speed of light
BASELINE_COEFF = C_LAT / SQRT2     # = 1/√6 ≈ 0.40825  (Finding 21)

# BCC nearest-neighbour vectors (lattice parameter 1): (±1,±1,±1)
_BCC_NNS = np.array([[s0, s1, s2]
                      for s0 in (+1, -1)
                      for s1 in (+1, -1)
                      for s2 in (+1, -1)], dtype=float) / 2.0  # 8×3


# ═══════════════════════════════════════════════════════════════════════════════
#  Core: single displaced-pair EM bilinears
# ═══════════════════════════════════════════════════════════════════════════════

def _pair_EM(q_plus, q_minus, n_hat, nmag):
    """Return (E0, B0, G_T, G_T_dag, Omega) for the displaced pair.

    Convention matching maxwell_curl_residual:
      ψ = + eigenmode at q_plus   (psi_plus)
      φ = − eigenmode at q_minus  (psi_minus)
    Both will be evolved as e^{-i·ω} so G → e^{-iΩ} G.

    Parameters
    ----------
    q_plus, q_minus : array-like (3,) — displaced half-momenta
    n_hat  : unit vector of n_{k/2} (central mode direction, for projection)
    nmag   : |n_{k/2}|  (central mode magnitude, for field scaling)

    Returns
    -------
    E0, B0 : complex (3,) — EM fields at t=0 from this pair
    G_T, G_T_dag : complex (3,) — transverse bilinear and conjugate
    Omega  : float — photon frequency from this pair
    """
    psi_p, _,     omega_p = mx.weyl_eigenmodes_3d_bcc(*q_plus)
    _,     psi_m, omega_m = mx.weyl_eigenmodes_3d_bcc(*q_minus)

    # G^i = φ^T σ^i ψ  (Paper 1 Eq. 33)
    G      = mx.bilinear_G(psi_p, psi_m)
    G_T    = mx._transverse_part(G, n_hat)
    G_T_d  = np.conj(G_T)

    E0 = nmag * (G_T + G_T_d)
    B0 = 1j * nmag * (G_T_d - G_T)
    return E0, B0, G_T, G_T_d, float(omega_p + omega_m)


# ═══════════════════════════════════════════════════════════════════════════════
#  Smearing functions: return (q_samples [N×3], weights [N])
# ═══════════════════════════════════════════════════════════════════════════════

def _gaussian_samples(sigma, n_q, rng):
    """Isotropic Gaussian  q ~ N(0, σ²I).  First sample is always q=0."""
    if sigma < 1e-20 or n_q <= 1:
        return np.zeros((1, 3)), np.ones(1)
    q = rng.normal(scale=sigma, size=(n_q, 3))
    q[0] = 0.0
    d2 = np.sum(q * q, axis=1)
    w  = np.exp(-d2 / (2.0 * sigma**2))
    w /= w.sum()
    return q, w


def _bcc_shell_samples(delta):
    """8 BCC nearest-neighbour displacements scaled by delta.  Equal weights."""
    q = _BCC_NNS * delta
    w = np.ones(8) / 8.0
    return q, w


# ═══════════════════════════════════════════════════════════════════════════════
#  Smeared curl residual
# ═══════════════════════════════════════════════════════════════════════════════

def smeared_curl_residual(k_mag, sigma,
                          mode='fixed',
                          shell_delta=None,
                          n_dirs=8, n_q=64, seed=0):
    """Compute the smeared-bilinear curl residual.

    Parameters
    ----------
    k_mag  : float — photon momentum magnitude
    sigma  : float — smearing width (absolute units if mode='fixed';
             proportionality constant α if mode='k_proportional').
    mode   : 'fixed'          — σ is an absolute width in k-space
             'k_proportional' — effective σ = sigma × k_mag / 2
             'bcc_shell'      — 8 BCC-NN displacements × shell_delta
    shell_delta : float — used only with mode='bcc_shell'
    n_dirs : int  — number of random photon directions
    n_q    : int  — number of displacement samples per direction
    seed   : int  — RNG seed

    Returns
    -------
    (curl_E_max, curl_B_max, trans_max, Omega_rel_spread)
      curl_E/B_max    : worst normalised curl residual across directions
      trans_max       : worst transversality error  2n·E / (|E|+|B|)
      Omega_rel_spread: max |Ω_eff − 2ω(k/2)| / (2ω(k/2))  (frequency drift)
    """
    dirs    = mx._random_dirs(n_dirs, seed=seed)
    errs_E  = []
    errs_B  = []
    trans   = []
    o_spread = []

    for i_d, d in enumerate(dirs):
        rng = np.random.default_rng(seed + i_d * 997)
        kx_h, ky_h, kz_h = k_mag * d / 2.0

        # Central n-vector and eigenfrequency
        _, nx, ny, nz = bcc._bcc_uvec(kx_h, ky_h, kz_h, sign='+')
        n_half = np.array([nx, ny, nz], dtype=float)
        nmag   = float(np.linalg.norm(n_half))
        if nmag < 1e-15:
            continue
        n_hat = n_half / nmag

        _, _, omega_0 = mx.weyl_eigenmodes_3d_bcc(kx_h, ky_h, kz_h)
        Omega_central = 2.0 * omega_0

        # Build displacement samples and weights
        if mode == 'fixed':
            effective_sigma = sigma
            q_samps, weights = _gaussian_samples(effective_sigma, n_q, rng)
        elif mode == 'k_proportional':
            effective_sigma = sigma * k_mag / 2.0
            q_samps, weights = _gaussian_samples(effective_sigma, n_q, rng)
        elif mode == 'bcc_shell':
            q_samps, weights = _bcc_shell_samples(
                shell_delta if shell_delta is not None else sigma)
        else:
            raise ValueError(f"Unknown mode: {mode!r}")

        k_half_vec = np.array([kx_h, ky_h, kz_h])

        # Accumulate weighted sums of E(0), B(0), E(1), B(1)
        E0_acc  = np.zeros(3, dtype=complex)
        B0_acc  = np.zeros(3, dtype=complex)
        E1_acc  = np.zeros(3, dtype=complex)
        B1_acc  = np.zeros(3, dtype=complex)
        Omega_eff = 0.0

        for q, w in zip(q_samps, weights):
            if w < 1e-20:
                continue
            q_p = k_half_vec + q
            q_m = k_half_vec - q

            E0_j, B0_j, G_T_j, G_T_d_j, Omega_j = _pair_EM(q_p, q_m, n_hat, nmag)

            # Time-step: G_T → e^{-iΩ} G_T,  conj(G_T) → e^{+iΩ} conj(G_T)
            e_neg = np.exp(-1j * Omega_j)
            e_pos = np.exp(+1j * Omega_j)
            E1_j  = nmag * (e_neg * G_T_j + e_pos * G_T_d_j)
            B1_j  = 1j * nmag * (e_pos * G_T_d_j - e_neg * G_T_j)

            E0_acc   += w * E0_j
            B0_acc   += w * B0_j
            E1_acc   += w * E1_j
            B1_acc   += w * B1_j
            Omega_eff += w * Omega_j

        # Curl residual: (E(1)-E(0)) vs i (2 n_{k/2}) × B(0)
        dE    = E1_acc - E0_acc
        dB    = B1_acc - B0_acc
        two_n = 2.0 * n_half
        rhs_E = 1j * np.cross(two_n, B0_acc)
        rhs_B = -1j * np.cross(two_n, E0_acc)
        denom = float(np.linalg.norm(E0_acc) + np.linalg.norm(B0_acc)) + 1e-30

        errs_E.append(float(np.linalg.norm(dE - rhs_E) / denom))
        errs_B.append(float(np.linalg.norm(dB - rhs_B) / denom))

        # Transversality: 2 n · E_smeared
        trans.append(float(abs(two_n @ E0_acc) / denom))

        # Effective frequency spread
        if Omega_central > 1e-20:
            o_spread.append(abs(Omega_eff - Omega_central) / Omega_central)

    return (max(errs_E) if errs_E else float('nan'),
            max(errs_B) if errs_B else float('nan'),
            max(trans)  if trans  else float('nan'),
            max(o_spread) if o_spread else 0.0)


# ═══════════════════════════════════════════════════════════════════════════════
#  Log-log slope and coefficient helper
# ═══════════════════════════════════════════════════════════════════════════════

def _loglog_fit(ks, res):
    """Linear fit of log(res) vs log(k).  Returns (slope, coefficient)."""
    ks  = np.asarray(ks,  dtype=float)
    res = np.asarray(res, dtype=float)
    mask = np.isfinite(res) & (res > 0) & np.isfinite(ks) & (ks > 0)
    if mask.sum() < 2:
        return float('nan'), float('nan')
    A = np.vstack([np.log(ks[mask]), np.ones(mask.sum())]).T
    slope, intercept = np.linalg.lstsq(A, np.log(res[mask]), rcond=None)[0]
    return float(slope), float(np.exp(intercept))


def scan_sigma(sigma, mode, k_scan, n_dirs=8, n_q=64, seed=0,
               shell_delta=None):
    """Run k-scan for one smearing variant.  Returns dict of results."""
    curl_E_vals = []
    curl_B_vals = []
    for k in k_scan:
        eE, eB, _, _ = smeared_curl_residual(
            k, sigma, mode=mode, shell_delta=shell_delta,
            n_dirs=n_dirs, n_q=n_q, seed=seed)
        curl_E_vals.append(eE)
        curl_B_vals.append(eB)

    slope_E, coeff_E = _loglog_fit(k_scan, curl_E_vals)
    slope_B, coeff_B = _loglog_fit(k_scan, curl_B_vals)
    # Leading coefficient: residual/k at smallest k
    coeff_over_k_E = curl_E_vals[-1] / k_scan[-1]
    coeff_over_k_B = curl_B_vals[-1] / k_scan[-1]

    return {
        "curl_E_scan": dict(zip([f"{k:.1e}" for k in k_scan], curl_E_vals)),
        "curl_B_scan": dict(zip([f"{k:.1e}" for k in k_scan], curl_B_vals)),
        "slope_E": slope_E,
        "slope_B": slope_B,
        "coeff_over_k_E": coeff_over_k_E,
        "coeff_over_k_B": coeff_over_k_B,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  Main run
# ═══════════════════════════════════════════════════════════════════════════════

def run():
    k_scan = [1e-1, 5e-2, 1e-2, 5e-3, 1e-3]
    n_dirs = 8
    n_q    = 64
    seed   = 0

    variants = []

    # ── 1. Baseline (σ=0) ────────────────────────────────────────────────────
    variants.append({
        "label":       "baseline_sigma0",
        "description": "Un-smeared pointwise bilinear (σ=0). Must reproduce c_lat/√2.",
        "sigma":        0.0,
        "mode":        "fixed",
    })

    # ── 2. Fixed-width Gaussian ───────────────────────────────────────────────
    for sig in [0.005, 0.01, 0.02, 0.05, 0.10]:
        variants.append({
            "label":       f"fixed_sigma_{sig:.3f}",
            "description": f"Isotropic Gaussian smearing, fixed σ={sig}",
            "sigma":        sig,
            "mode":        "fixed",
        })

    # ── 3. k-proportional Gaussian ────────────────────────────────────────────
    for alpha in [0.25, 0.5, 1.0, 2.0]:
        variants.append({
            "label":       f"k_prop_alpha_{alpha:.2f}",
            "description": (f"k-proportional Gaussian, σ = {alpha} × |k|/2. "
                            "Expected slope → 2 for any α > 0."),
            "sigma":        alpha,
            "mode":        "k_proportional",
        })

    # ── 4. BCC-shell smearing ─────────────────────────────────────────────────
    for delta in [0.01, 0.05, 0.10]:
        variants.append({
            "label":       f"bcc_shell_delta_{delta:.3f}",
            "description": f"8 BCC-NN displacements × δ={delta}",
            "sigma":        delta,
            "mode":        "bcc_shell",
            "shell_delta":  delta,
        })

    # ── Run all variants ──────────────────────────────────────────────────────
    results = []
    for v in variants:
        t0 = time.time()
        print(f"  [{v['label']}] ... ", end='', flush=True)
        shell_delta = v.get("shell_delta", None)
        res = scan_sigma(
            sigma=v["sigma"], mode=v["mode"],
            k_scan=k_scan, n_dirs=n_dirs, n_q=n_q, seed=seed,
            shell_delta=shell_delta,
        )
        elapsed = time.time() - t0
        print(f"slope_E={res['slope_E']:.3f}, coeff/k={res['coeff_over_k_E']:.5f}  "
              f"({elapsed:.1f}s)")
        results.append({**v, **res})

    # ── Self-check ────────────────────────────────────────────────────────────
    baseline = next(r for r in results if r["label"] == "baseline_sigma0")
    measured = baseline["coeff_over_k_E"]
    rel_err  = abs(measured - BASELINE_COEFF) / BASELINE_COEFF

    out = {
        "meta": {
            "date":                  time.strftime("%Y-%m-%d %H:%M"),
            "baseline_coeff_expected": BASELINE_COEFF,
            "baseline_coeff_measured": measured,
            "baseline_rel_err":        rel_err,
            "k_scan":                  k_scan,
            "n_dirs":                  n_dirs,
            "n_q":                     n_q,
        },
        "variants": results,
    }
    return out


# ═══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Smearing-function fork (Finding 21 follow-up) ===\n")
    print(f"Baseline target: curl/|k| = c_lat/√2 = {BASELINE_COEFF:.5f}\n")

    out = run()

    # Save results
    outdir  = os.path.join(os.path.dirname(CASIM), "test-results")
    os.makedirs(outdir, exist_ok=True)
    datestr = time.strftime("%Y-%m-%d")
    fname   = os.path.join(outdir, f"smearing_fork_results_{datestr}.json")
    with open(fname, "w") as fh:
        json.dump(out, fh, indent=2)

    # ── Summary table ─────────────────────────────────────────────────────────
    m = out["meta"]
    print(f"\n=== Baseline self-check ===")
    print(f"  Expected curl/k = {m['baseline_coeff_expected']:.5f}  "
          f"(c_lat/√2 = 1/√6)")
    print(f"  Measured curl/k = {m['baseline_coeff_measured']:.5f}  "
          f"(rel err {m['baseline_rel_err']:.2e})")

    print(f"\n=== Smearing results (sorted by coeff_over_k_E at k→0) ===")
    hdr = (f"{'label':<30}{'mode':<15}{'sigma':>8}{'slope_E':>10}"
           f"{'coeff/k_E':>12}{'vs baseline':>14}")
    print(hdr)
    print("-" * len(hdr))

    sorted_variants = sorted(out["variants"],
                             key=lambda r: r.get("coeff_over_k_E", float("inf")))
    for r in sorted_variants:
        ratio = r["coeff_over_k_E"] / BASELINE_COEFF
        print(f"{r['label']:<30}{r['mode']:<15}{r['sigma']:>8.4f}"
              f"{r['slope_E']:>10.3f}{r['coeff_over_k_E']:>12.5f}"
              f"{ratio:>13.3f}×")

    print(f"\n[saved] {fname}")
