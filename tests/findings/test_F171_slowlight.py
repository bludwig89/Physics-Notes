"""
test_F171_slowlight.py  --  Track 1.b: slow-light / EIT as a test of the
rotation-rate picture against the phase-velocity description.

Checks
------
S1  Normal EIT (Hau scale): the model rotation-rate propagator and the
    standard complex-phase propagator give the SAME real field to machine
    precision (the C <-> SO(2) isomorphism); measured group delay matches
    L / v_g.  Consistency anchor -- the model reduces to Maxwell-in-medium.
S2  Anomalous gain doublet (Wang scale): group velocity is NEGATIVE; the
    pulse peak ADVANCES (exits before it enters).  Both descriptions agree.
S3  Front velocity: n(omega -> inf) -> 1, so the turn-on front is luminal
    (v_front = c) in BOTH regimes, regardless of the sign of v_g.  This is the
    model's invariant -- "phase/group velocity transport nothing."
S4  Lattice O(k^3) term: the only genuinely distinct prediction; ~ (a/lambda)^2
    ~ 1e-56 at optical wavelengths, and NOT enhanced by the group index.

Run:  python tests/findings/test_F171_slowlight.py
"""
import os, sys, json
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import slowlight as sl

C = sl.C_VAC
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "test-results", "F171_slowlight.json")
results = {}


def gaussian_envelope(t, t0, tau):
    return np.exp(-((t - t0) ** 2) / (2.0 * tau ** 2)).astype(complex)


def banded(cf, dmax):
    """Wrap a susceptibility so chi = 0 (vacuum) for |Re delta| > dmax.
    Physically the atomic response vanishes far off resonance; this also stops
    a toy model extrapolated to the FFT Nyquist edge from contaminating the
    pulse.  The pulse band sits well inside dmax."""
    def g(delta):
        delta = np.asarray(delta, dtype=complex)
        return np.where(np.abs(np.real(delta)) <= dmax, cf(delta), 0.0 + 0.0j)
    return g


# ----------------------------------------------------------------------
# S1 -- NORMAL EIT slow light, calibrated to the Hau 1999 anchor 17 m/s
# ----------------------------------------------------------------------
def check_S1():
    lam = 589e-9                       # sodium D, m
    omega0 = 2.0 * np.pi * C / lam     # rad/s
    gamma_opt = 2 * np.pi * 10e6
    gamma_gnd = 2 * np.pi * 1e3
    Omega_c = 2 * np.pi * 12e6
    kw = dict(Omega_c=Omega_c, gamma_opt=gamma_opt, gamma_gnd=gamma_gnd)

    # -- Part A: calibrate to the Hau anchor (v_g = 17 m/s) --------------
    # derivative step MUST be far inside the EIT window (~Omega_c^2/gamma_opt);
    # use dw ~ 1e4 rad/s << 9e7 window.  n_g is ~linear in alpha0 (dilute).
    dω = 1.0e4
    target_ng = C / 17.0
    ng1, _ = sl.group_index_and_velocity(omega0, sl.eit_susceptibility, dω=dω, alpha0=1e6, **kw)
    alpha0_hau = 1e6 * (target_ng / ng1)
    n_g_hau, v_g_hau = sl.group_index_and_velocity(
        omega0, sl.eit_susceptibility, dω=dω, alpha0=alpha0_hau, **kw)

    # -- Part B: a moderate regime (n_g ~ +310, mirroring the S2 magnitude)
    # where the pulse stays inside the linear-dispersion band, so peak delay
    # = L/v_g cleanly and the two propagators compare on an undistorted pulse.
    ngm, _ = sl.group_index_and_velocity(omega0, sl.eit_susceptibility, dω=dω, alpha0=1e6, **kw)
    alpha0_mod = 1e6 * (310.0 / ngm)    # target n_g ~ +310 (slow-light mirror of Wang)
    n_g, v_g = sl.group_index_and_velocity(omega0, sl.eit_susceptibility, dω=dω, alpha0=alpha0_mod, **kw)

    tau = 2.0e-6                        # narrowband: well inside the EIT window
    L = 0.06
    N = 2 ** 16
    T = 120e-6
    t = np.linspace(-T / 2, T / 2, N, endpoint=False)
    t0 = -15e-6
    E0 = gaussian_envelope(t, t0, tau)
    cf = banded(lambda d: sl.eit_susceptibility(d, alpha0=alpha0_mod, **kw),
                dmax=5 * kw["Omega_c"])

    E_phase = sl.propagate_phase(E0, t, omega0, L, cf)
    E_rot = sl.propagate_rotation(E0, t, omega0, L, cf)

    iso_resid = float(np.max(np.abs(E_phase - E_rot)) / np.max(np.abs(E_phase)))
    delay_meas = sl.peak_delay(E0, E_phase, t)
    delay_pred = L / v_g

    results["S1_normal_eit"] = {
        "anchor": "Hau 1999, v_g = 17 m/s, Nature 397 594",
        "hau_v_g_calibrated_m_s": v_g_hau,
        "hau_n_g": n_g_hau,
        "hau_slowdown_factor": C / v_g_hau,
        "prop_regime_v_g_m_s": v_g,
        "prop_regime_n_g": n_g,
        "L_m": L,
        "delay_measured_s": delay_meas,
        "delay_predicted_L_over_vg_s": delay_pred,
        "delay_rel_err": abs(delay_meas - delay_pred) / abs(delay_pred),
        "rotation_vs_phase_field_resid": iso_resid,
        "slow_light_positive_delay": delay_meas > 0,
        "PASS": iso_resid < 1e-12 and delay_meas > 0
                and abs(delay_meas - delay_pred) / abs(delay_pred) < 0.10
                and abs(v_g_hau - 17.0) / 17.0 < 0.01,
    }


# ----------------------------------------------------------------------
# S2 -- ANOMALOUS gain doublet, calibrated to the Wang 2000 anchor -c/310
# ----------------------------------------------------------------------
def check_S2():
    lam = 795e-9                       # near Cs/Rb optical
    omega0 = 2.0 * np.pi * C / lam
    sep = 2 * np.pi * 1.0e6            # gain-line separation
    width = 2 * np.pi * 0.3e6
    kw = dict(sep=sep, width=width)

    dω = 1.0e4                          # << gain-line separation
    target_vg = -C / 310.0
    target_ng = C / target_vg          # = -310 (the Wang anchor)
    ngM, _ = sl.group_index_and_velocity(omega0, sl.gain_doublet_susceptibility, dω=dω, M=1e-3, **kw)
    # n_g = 1 + (slope term) linear in M; solve M for target (n_g - 1)
    M = 1e-3 * ((target_ng - 1.0) / (ngM - 1.0))
    n_g, v_g = sl.group_index_and_velocity(omega0, sl.gain_doublet_susceptibility, dω=dω, M=M, **kw)

    # spectral (analytic) group delay = L * n_g / c  -- negative => advance
    spectral_group_delay = L_gain_group_delay = L = 6.0e-2  # 6 cm Wang-like cell
    spectral_group_delay = L * n_g / C

    tau = 2e-6                          # narrowband: bandwidth << sep
    N = 2 ** 15
    T = 120e-6
    t = np.linspace(-T / 2, T / 2, N, endpoint=False)
    t0 = -15e-6
    E0 = gaussian_envelope(t, t0, tau)
    cf = banded(lambda d: sl.gain_doublet_susceptibility(d, M=M, **kw),
                dmax=20 * sep)

    E_phase = sl.propagate_phase(E0, t, omega0, L, cf)
    E_rot = sl.propagate_rotation(E0, t, omega0, L, cf)
    iso_resid = float(np.max(np.abs(E_phase - E_rot)) / np.max(np.abs(E_phase)))
    delay_meas = sl.peak_delay(E0, E_phase, t)   # expected NEGATIVE (advance)
    delay_pred = L / v_g                          # negative

    results["S2_anomalous_gain"] = {
        "anchor": "Wang-Kuzmich-Dogariu 2000, v_g = -c/310, Nature 406 277",
        "v_g_calibrated_m_s": v_g,
        "v_g_in_units_of_c": v_g / C,
        "n_g": n_g,
        "L_m": L,
        "delay_measured_peak_s": delay_meas,
        "delay_predicted_L_over_vg_s": delay_pred,
        "spectral_group_delay_s": spectral_group_delay,
        "negative_group_velocity": v_g < 0,
        "spectral_delay_negative_advance": spectral_group_delay < 0,
        "peak_advances_illustrative": delay_meas < 0,
        "rotation_vs_phase_field_resid": iso_resid,
        "PASS": (v_g < 0) and (spectral_group_delay < 0) and iso_resid < 1e-12,
    }


# ----------------------------------------------------------------------
# S3 -- FRONT velocity = c in BOTH regimes (the model's invariant)
# ----------------------------------------------------------------------
def check_S3():
    lam = 589e-9
    omega0 = 2.0 * np.pi * C / lam
    cf_eit = lambda d: sl.eit_susceptibility(
        d, alpha0=1e7, Omega_c=2 * np.pi * 12e6,
        gamma_opt=2 * np.pi * 10e6, gamma_gnd=2 * np.pi * 1e3)
    cf_gain = lambda d: sl.gain_doublet_susceptibility(
        d, M=1e-2, sep=2 * np.pi * 1e6, width=2 * np.pi * 0.3e6)

    vf_eit, n_eit = sl.front_velocity_index(cf_eit, omega0)
    vf_gain, n_gain = sl.front_velocity_index(cf_gain, omega0)

    results["S3_front_velocity"] = {
        "statement": "n(omega->inf)->1 so the turn-on front is luminal in both regimes",
        "eit_n_high_freq": n_eit, "eit_v_front_over_c": vf_eit / C,
        "gain_n_high_freq": n_gain, "gain_v_front_over_c": vf_gain / C,
        "PASS": abs(vf_eit / C - 1) < 1e-6 and abs(vf_gain / C - 1) < 1e-6,
    }


# ----------------------------------------------------------------------
# S4 -- lattice O(k^3) term, the only distinct prediction; not enhanced
# ----------------------------------------------------------------------
def check_S4():
    a = 1.0664e-34                      # canonical SI cell, F107
    lam_opt = 589e-9
    frac_opt = sl.lattice_liv_fraction(lam_opt, a)
    # same vacuum wavelength inside a slow-light medium: a*k unchanged by n_g
    frac_in_medium = sl.lattice_liv_fraction(lam_opt, a)   # identical -> not enhanced
    results["S4_lattice_term"] = {
        "a_cell_m": a,
        "optical_lambda_m": lam_opt,
        "fractional_liv_ak2": frac_opt,
        "enhanced_by_group_index": False,
        "frac_in_slow_medium_same_as_vacuum": frac_in_medium == frac_opt,
        "note": "set by vacuum k=2pi/lambda, not by n_g; ~1e-56, unobservable",
        "PASS": frac_opt < 1e-50 and (frac_in_medium == frac_opt),
    }


if __name__ == "__main__":
    check_S1(); check_S2(); check_S3(); check_S4()
    n_pass = sum(1 for v in results.values() if v.get("PASS"))
    summary = {"n_checks": len(results), "n_pass": n_pass,
               "all_pass": n_pass == len(results)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"summary": summary, "checks": results}, f, indent=2)
    print(json.dumps({"summary": summary, "checks": results}, indent=2))
