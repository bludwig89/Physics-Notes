"""
test_F50_gravity_fork_dirac.py — Gravity fork via the F46 spherical triangle
============================================================================
Verifies the covariant restatement of Finding 46 implemented in
`ca-simulation/forks/gr_fork_F46_dirac.py`:

    cos Ω_Dirac^coord(x,k,m) = cos(√A(x)·arcsin m) · cos ω_kin(k; c_eff(x))

with lapse A (g_00 = -A), c_eff = c_0√(A/B).

Tests
-----
G1  Continuum reduction: the spherical-triangle Ω matches the curved-tetrad
    Hamiltonian dispersion Ω² = A m² c₀⁴ + (A/B) c₀²|k|² as the legs → 0,
    with the expected slope-4 lattice (spherical→Euclidean) correction.
G2  Static redshift (k=0) lives on the REST leg: Ω = √A·arcsin m, and the
    near/far clock ratio reproduces the GR factor-1 redshift (Δν/ν = Δφ/c²),
    NOT the baseline factor 2.
G3  Photon limit (m=0): Ω = ω_kin(k; c_eff) and c_eff equals Fork-E c_γ
    = c₀√(A/B) to machine precision.
G4  Negative control: a kinetic-leg-ONLY scheme (rest leg frozen at arcsin m)
    gives a position-independent Ω at k=0 → zero static redshift, proving the
    redshift cannot sit on the kinetic leg (corrects F46 §9.3 wording).
G5  Prototype stepper (Strang: rest √A + kinetic c_eff) conserves norm.

Writes test-results/F50_gravity_fork_dirac.json.

Run:
    python model-tests/test_F50_gravity_fork_dirac.py
"""

from __future__ import annotations
import json
import os
import sys

import numpy as np

THIS = os.path.dirname(__file__)
SIM = os.path.abspath(os.path.join(THIS, "..", "ca-simulation"))
FORKS = os.path.join(SIM, "forks")
for p in (SIM, FORKS):
    if p not in sys.path:
        sys.path.insert(0, p)

import importlib.util  # noqa: E402

import gr_fork_F46_dirac as gf       # noqa: E402


def _load(modname, filename):
    spec = importlib.util.spec_from_file_location(
        modname, os.path.join(FORKS, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ───────────────────────────────────────────────────────────────────
#  Helpers
# ───────────────────────────────────────────────────────────────────

C0 = 0.5
MODE = "exact_isotropic"


def newtonian_phi(r, GM=0.02):
    """Analytic Newtonian potential φ = -GM/r (lattice units)."""
    return -GM / r


# ───────────────────────────────────────────────────────────────────
#  G1 — continuum reduction (slope-4 lattice correction)
# ───────────────────────────────────────────────────────────────────

def test_G1_continuum_slope():
    rng = np.random.default_rng(0)
    # one representative site with a real well
    phi = np.array([newtonian_phi(8.0, GM=0.02)])
    m = 0.3
    scales = np.array([2.0**(-j) for j in range(2, 10)])
    resid = []
    for s in scales:
        k = np.array([0.7, 0.4]) * s          # shrink the kinetic leg
        m_s = m * s                            # shrink the rest leg together
        om_sph = gf.dirac_omega_coord(k, phi, C0, m_s, MODE, form="continuum")[0]
        om_cont = gf.dirac_omega_continuum(k, phi, C0, m_s, MODE)[0]
        resid.append(abs(om_sph**2 - om_cont**2))
    resid = np.array(resid)
    # log-log slope of |Ω²_sph − Ω²_cont| vs scale s should be ≈ 4
    sl = np.polyfit(np.log(scales), np.log(resid + 1e-300), 1)[0]
    return {
        "name": "G1_continuum_slope4",
        "slope": float(sl),
        "target": 4.0,
        "tol": 0.1,
        "status": "PASS" if abs(sl - 4.0) < 0.1 else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  G2 — static redshift on the rest leg (GR factor 1)
# ───────────────────────────────────────────────────────────────────

def test_G2_static_redshift():
    m = 0.3
    pairs = [(6.0, 16.0), (8.0, 22.0), (10.0, 28.0), (12.0, 30.0)]
    ratios = []
    rest_resid = []
    for r_n, r_f in pairs:
        phi_n = np.array([newtonian_phi(r_n)])
        phi_f = np.array([newtonian_phi(r_f)])
        # rest-leg = √A·arcsin m, and Ω(k=0) must equal it exactly
        om_n = gf.dirac_omega_coord(np.array([0.0, 0.0]), phi_n, C0, m, MODE)[0]
        rest_n = gf.rest_leg(phi_n, C0, m, MODE)[0]
        rest_resid.append(abs(om_n - rest_n))
        # clock ratio from the rest legs (= τ ratio)
        tau_n = gf.tau_rate(phi_n, C0, MODE)[0]
        tau_f = gf.tau_rate(phi_f, C0, MODE)[0]
        dnu = tau_n / tau_f - 1.0
        pred_GR = -(float(phi_f[0]) - float(phi_n[0])) / C0**2
        ratios.append(dnu / pred_GR)
    ratios = np.array(ratios)
    return {
        "name": "G2_static_redshift_rest_leg",
        "mean_ratio_GR": float(ratios.mean()),
        "std_ratio_GR": float(ratios.std()),
        "baseline_ratio_GR": 2.0,
        "max_rest_leg_residual": float(np.max(rest_resid)),
        "target_ratio": 1.0,
        "status": "PASS" if (abs(ratios.mean() - 1.0) < 0.05
                             and max(rest_resid) < 1e-13) else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  G3 — photon limit: Ω = ω_kin(c_eff), c_eff = Fork-E c_γ
# ───────────────────────────────────────────────────────────────────

def test_G3_photon_limit():
    forkE = _load("gr_fork_E_tensor_t", "gr_fork_E_tensor.py")
    rs = np.array([6.0, 9.0, 13.0, 20.0])
    phi = newtonian_phi(rs)
    ceff = gf.c_eff_matter(phi, C0, MODE)
    cE = forkE.make_fork(MODE).c_photon(phi, C0)
    resid_c = float(np.max(np.abs(ceff - cE)))
    # at m=0 the spherical Ω equals the kinetic leg exactly
    k = np.array([0.5, 0.3])
    resid_omega = []
    for p in phi:
        om = gf.dirac_omega_coord(k, np.array([p]), C0, 0.0, MODE)[0]
        kin = gf.kinetic_leg(k, np.array([p]), C0, 0.0, MODE)[0]
        resid_omega.append(abs(om - kin))
    return {
        "name": "G3_photon_limit",
        "max_c_eff_minus_forkE_cgamma": resid_c,
        "max_omega_minus_kinetic_leg": float(np.max(resid_omega)),
        "tol": 1e-13,
        "status": "PASS" if (resid_c < 1e-13
                             and max(resid_omega) < 1e-13) else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  G4 — negative control: kinetic-leg-only gives NO static redshift
# ───────────────────────────────────────────────────────────────────

def test_G4_kinetic_only_fails_redshift():
    """Freeze the rest leg at arcsin(m) (F46 §9.3 literal reading) and put ALL
    site dependence on the kinetic leg.  At k=0 the kinetic leg vanishes, so
    Ω is identical at every site → redshift ratio = 0 (failure)."""
    m = 0.3
    arcsin_m = float(np.arcsin(m))
    omegas = []
    for r in (6.0, 12.0, 24.0):
        phi = np.array([newtonian_phi(r)])
        ceff = gf.c_eff_matter(phi, C0, MODE)[0]
        # kinetic-leg-only Ω at k=0: cos Ω = cos(arcsin m)·cos(c_eff·0)=√(1-m²)
        cosom = np.sqrt(1 - m**2) * np.cos(ceff * 0.0)
        omegas.append(float(np.arccos(cosom)))
    omegas = np.array(omegas)
    spread = float(omegas.max() - omegas.min())
    # all equal to arcsin(m); redshift signal is zero
    return {
        "name": "G4_kinetic_only_negative_control",
        "omega_spread_across_sites": spread,
        "omega_value": float(omegas[0]),
        "arcsin_m": arcsin_m,
        "note": "spread≈0 proves kinetic-leg-only yields no static redshift",
        "status": "PASS" if (spread < 1e-15
                             and abs(omegas[0] - arcsin_m) < 1e-13) else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  G5 — prototype stepper conserves norm
# ───────────────────────────────────────────────────────────────────

def test_G5_stepper_norm():
    from ca_dirac import gaussian_dirac_2d, dirac_norm
    L = 48
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    r = np.sqrt((X - L / 2) ** 2 + (Y - L / 2) ** 2) + 2.0
    phi = newtonian_phi(r, GM=0.05)
    A, B = gf.metric(phi, C0, MODE)
    ceff = gf.c_eff_matter(phi, C0, MODE)

    eu, ed, cu, cd = gaussian_dirac_2d((L, L), sigma=4.0, chirality="mixed")
    n0 = dirac_norm(eu, ed, cu, cd)
    m = 0.3
    n_steps = 12
    solver = gf.make_kinetic_solver(ceff, dt=0.5, n_sub=4)  # exactly-unitary, cached
    for _ in range(n_steps):
        eu, ed, cu, cd = gf.gravity_dirac_step_2d(
            eu, ed, cu, cd, A, ceff, m, dt=0.5, n_sub=4,
            kinetic_solver=solver)
    n1 = dirac_norm(eu, ed, cu, cd)
    drift = abs(n1 - n0) / n0
    return {
        "name": "G5_prototype_stepper_norm",
        "norm_initial": n0,
        "norm_final": n1,
        "relative_drift": float(drift),
        "n_steps": n_steps,
        "tol": 1e-10,
        "status": "PASS" if drift < 1e-10 else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  G6 — bounded exact-QCA leg reduces to flat F46 at A=B (φ=0)
# ───────────────────────────────────────────────────────────────────

def test_G6_flat_reduces_to_F46():
    """At φ=0 ⇒ A=B=1 ⇒ r_kin=1, the bounded exact-QCA Dirac dispersion must
    equal the flat F46 identity cos Ω = √(1−m²)·c_x·c_y bit-for-bit."""
    phi0 = np.array([0.0])
    rng = np.random.default_rng(3)
    resid = []
    for _ in range(200):
        m = float(rng.uniform(0, 0.95))
        k = rng.uniform(-np.pi, np.pi, size=2)
        om = gf.dirac_omega_coord(k, phi0, C0, m, MODE, form="exact_qca")[0]
        cx = np.cos(k[0] / np.sqrt(2.0))
        cy = np.cos(k[1] / np.sqrt(2.0))
        om_F46 = np.arccos(np.clip(np.sqrt(1 - m**2) * cx * cy, -1, 1))
        resid.append(abs(om - om_F46))
    mx = float(np.max(resid))
    return {
        "name": "G6_flat_reduces_to_F46",
        "max_residual_vs_F46": mx,
        "n_samples": 200,
        "tol": 1e-14,
        "status": "PASS" if mx < 1e-14 else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  G7 — bounded leg stays in the Brillouin zone; small-k slope = r_kin/√2
# ───────────────────────────────────────────────────────────────────

def test_G7_bounded_and_slope():
    phi = np.array([newtonian_phi(8.0, GM=0.02)])
    r = gf.r_kin(phi, C0, MODE)[0]
    # boundedness across the full BZ at m=0.5
    rng = np.random.default_rng(5)
    ks = rng.uniform(-np.pi, np.pi, size=(400, 2))
    oms = np.array([gf.dirac_omega_coord(k, phi, C0, 0.5, MODE, "exact_qca")[0]
                    for k in ks])
    in_band = bool(np.all((oms >= 0.0) & (oms <= np.pi + 1e-12)))
    # small-k slope of the kinetic leg along the diagonal → r·(1/√2)
    s = 1e-4
    k_small = np.array([s, s]) / np.sqrt(2.0)  # |k| = s
    kin = float(np.asarray(gf.kinetic_leg(k_small, phi, C0, 0.0, MODE, "exact_qca")).ravel()[0])
    slope = kin / s
    slope_target = r / np.sqrt(2.0)
    slope_err = abs(slope - slope_target)
    return {
        "name": "G7_bounded_and_slope",
        "omega_in_band_0_pi": in_band,
        "kinetic_slope": float(slope),
        "slope_target_r_over_sqrt2": float(slope_target),
        "slope_abs_err": float(slope_err),
        "tol_slope": 1e-6,
        "status": "PASS" if (in_band and slope_err < 1e-6) else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  G8 — homogeneous exact-QCA stepper realises ω_kin = r·arccos(c_x c_y)
# ───────────────────────────────────────────────────────────────────

def test_G8_qca_stepper_phase_match():
    """Propagate a Weyl plane-wave eigenstate (m=0) with the gravity stepper's
    exact-QCA kinetic path at a uniform rate r=√(A/B), and check the measured
    per-tick phase equals the bounded leg r·arccos(c_x c_y) at machine ε."""
    import ca_core_exact as ce

    L = 32
    # uniform background: pick a constant well so r_kin is a scalar
    phi_val = newtonian_phi(10.0, GM=0.02)
    A_field = np.full((L, L), 0.0)            # rest leg off (m=0)
    A, B = gf.metric(np.array([phi_val]), C0, MODE)
    r = float(gf.r_kin(np.array([phi_val]), C0, MODE)[0])

    ix, iy = 3, 2
    kx = 2 * np.pi * ix / L
    ky = 2 * np.pi * iy / L

    # +ω eigenvector of the 2×2 exact-QCA Weyl unitary at (kx,ky)
    Uff, Ufg, Ugf, Ugg = (np.asarray(x).reshape(()) for x in
                          ce.exact2d_unitary(np.array(kx), np.array(ky)))
    U2 = np.array([[complex(Uff), complex(Ufg)],
                   [complex(Ugf), complex(Ugg)]])
    omega0 = float(ce.exact2d_dispersion(np.array(kx), np.array(ky)))
    evals, evecs = np.linalg.eig(U2)
    idx = int(np.argmin(np.abs(evals - np.exp(-1j * omega0))))
    v = evecs[:, idx]; v = v / np.linalg.norm(v)

    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    ph = np.exp(1j * (kx * X + ky * Y))
    f0 = v[0] * ph
    g0 = v[1] * ph
    eu, ed, cu, cd = f0.copy(), g0.copy(), np.zeros_like(f0), np.zeros_like(f0)

    n_steps = 20
    dt = 1.0
    norm0 = np.sum(np.abs(f0) ** 2 + np.abs(g0) ** 2)
    per_tick = []
    fu, gu = f0.copy(), g0.copy()       # current η-field reference
    for _ in range(n_steps):
        eu, ed, cu, cd = gf.gravity_dirac_step_2d(
            eu, ed, cu, cd, A_field, None, m=0.0, dt=dt,
            kinetic="qca", r_kin_scalar=r)
        # incremental phase between consecutive ticks (always < π)
        ip = np.sum(np.conj(fu) * eu + np.conj(gu) * ed) / norm0
        per_tick.append(-float(np.angle(ip)))   # eigenvalue e^{-iω}
        fu, gu = eu.copy(), ed.copy()
    meas_phase = float(np.mean(per_tick))                # per tick
    pred_phase = r * omega0                               # bounded leg
    err = abs(((meas_phase - pred_phase + np.pi) % (2 * np.pi)) - np.pi)
    return {
        "name": "G8_qca_stepper_phase_match",
        "r_kin": r,
        "omega0_flat_qca": omega0,
        "measured_per_tick_phase": meas_phase,
        "predicted_r_times_omega0": pred_phase,
        "abs_err": float(err),
        "tol": 1e-12,
        "status": "PASS" if err < 1e-12 else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  Driver
# ───────────────────────────────────────────────────────────────────

def main():
    tests = [
        test_G1_continuum_slope,
        test_G2_static_redshift,
        test_G3_photon_limit,
        test_G4_kinetic_only_fails_redshift,
        test_G5_stepper_norm,
        test_G6_flat_reduces_to_F46,
        test_G7_bounded_and_slope,
        test_G8_qca_stepper_phase_match,
    ]
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:  # noqa: BLE001
            results.append({"name": t.__name__, "status": "ERROR",
                            "error": repr(e)})

    overall = "PASS" if all(r.get("status") == "PASS" for r in results) else "FAIL"
    out = {
        "finding": "F50",
        "title": "Gravity fork via F46 spherical triangle (tetrad Dirac / Fork E3)",
        "date": "2026-05-28",
        "C0": C0, "metric_mode": MODE,
        "overall": overall,
        "tests": results,
    }

    out_dir = os.path.abspath(os.path.join(THIS, "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "F50_gravity_fork_dirac.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)

    print("=" * 64)
    print("F50 — gravity fork via F46 spherical triangle")
    print("=" * 64)
    for r in results:
        print(f"  [{r.get('status','?'):>5}]  {r['name']}")
        for kk, vv in r.items():
            if kk in ("name", "status"):
                continue
            print(f"            {kk}: {vv}")
    print("-" * 64)
    print(f"  OVERALL: {overall}")
    print(f"  wrote {path}")
    return out


if __name__ == "__main__":
    main()
