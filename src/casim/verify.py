"""casim.verify — canonical fidelity & exactness checks.

Single source of truth for the checks that (a) the pytest suite asserts on and
(b) the exactness-inventory generator reports.  Each check returns a
``Check`` record (name, channel, exactness class, residual, tolerance, pass).

Keeping these here (not in ``tests/``) lets both pytest and the standalone
``casim inventory`` generator run them without a pytest dependency — important
because the model is often developed where pytest isn't installed.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List
import numpy as np

from .engine import Simulation, LatticeSpec
from .engine.core.channel import build_channel
from .engine.core.observers import NormConservation, DispersionFit
from .analysis import TOL


@dataclass
class Check:
    name: str
    channel: str
    exactness: str          # "exact" | "machine-precision" | "quantitative"
    residual: float
    tol: float | None
    passed: bool

    def as_row(self) -> Dict[str, Any]:
        return asdict(self)


def _check(name, channel, exactness, residual) -> Check:
    tol = TOL.get(exactness)
    passed = True if tol is None else (residual <= tol)
    return Check(name, channel, exactness, float(residual), tol, bool(passed))


# ----------------------------------------------------------------------
# Bit-identical kernel-fidelity checks (engine == raw kernel, same seed).
# ----------------------------------------------------------------------
def fidelity_photon_pair(L=12, seed=5, ticks=8) -> Check:
    from casim.engine.gauge import photon as pp
    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [build_channel({"type": "photon_pair", "init": "random"})],
                     [], seed=seed)
    sim.step(ticks)
    Ee, Be = sim.states["photon_pair"]["E"], sim.states["photon_pair"]["B"]
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((3, L, L, L)); B = rng.standard_normal((3, L, L, L))
    for _ in range(ticks):
        E, B = pp.photon_step_spectral(E, B)
    res = max(np.max(np.abs(Ee - E)), np.max(np.abs(Be - B)))
    return _check("kernel_fidelity", "photon_pair", "exact", res)


def fidelity_weyl_bcc(L=12, seed=0, ticks=20) -> Check:
    from casim.engine.lattice import bcc as bcc
    sim = Simulation(LatticeSpec(L=L, topology="bcc"),
                     [build_channel({"type": "weyl_bcc", "sign": "+"})], [], seed=seed)
    sim.step(ticks)
    fe, ge = sim.states["weyl_bcc"]["f"], sim.states["weyl_bcc"]["g"]
    rng = np.random.default_rng(seed)
    f = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    g = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    for _ in range(ticks):
        f, g = bcc.weyl_step_3d_bcc(f, g, sign="+")
    res = max(np.max(np.abs(fe - f)), np.max(np.abs(ge - g)))
    return _check("kernel_fidelity", "weyl_bcc", "exact", res)


def fidelity_w_chiral(L=10, seed=11, ticks=12) -> Check:
    from casim.engine.gauge import weak_wmu as ca_wmu

    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [build_channel({"type": "w_chiral"})], [], seed=seed)
    sim.step(ticks)
    Ee, Be = sim.states["w_chiral"]["E"], sim.states["w_chiral"]["B"]
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((3, L, L, L)); B = rng.standard_normal((3, L, L, L))
    for _ in range(ticks):
        E, B = ca_wmu.w_propagation_step_chiral(E, B)
    res = max(np.max(np.abs(Ee - E)), np.max(np.abs(Be - B)))
    return _check("kernel_fidelity", "w_chiral", "exact", res)


def fidelity_z_even(L=10, seed=2, ticks=12) -> Check:
    from casim.engine.gauge import weak_z as ca_z_field

    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [build_channel({"type": "z_even"})], [], seed=seed)
    sim.step(ticks)
    Ee, Be = sim.states["z_even"]["E"], sim.states["z_even"]["B"]
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((L, L, L)); B = rng.standard_normal((L, L, L))
    for _ in range(ticks):
        E, B = ca_z_field.z_propagation_step_spectral(E, B)
    res = max(np.max(np.abs(Ee - E)), np.max(np.abs(Be - B)))
    return _check("kernel_fidelity", "z_even", "exact", res)


def fidelity_gluon_bcc(L=10, seed=7, ticks=12) -> Check:
    from casim.engine.gauge import gluon as ca_gluon

    sim = Simulation(LatticeSpec(L=L, topology="bcc"),
                     [build_channel({"type": "gluon_bcc"})], [], seed=seed)
    sim.step(ticks)
    Ee, Be = sim.states["gluon_bcc"]["E"], sim.states["gluon_bcc"]["B"]
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((8, L, L, L)); B = rng.standard_normal((8, L, L, L))
    for _ in range(ticks):
        E, B = ca_gluon.gluon_rotation_step_spectral_bcc(E, B)
    res = max(np.max(np.abs(Ee - E)), np.max(np.abs(Be - B)))
    return _check("kernel_fidelity", "gluon_bcc", "exact", res)


# ----------------------------------------------------------------------
# Physics / infrastructure checks.
# ----------------------------------------------------------------------
def norm_drift_weyl(L=16, seed=0, ticks=200) -> Check:
    sim = Simulation(LatticeSpec(L=L, topology="bcc"),
                     [build_channel({"type": "weyl_bcc", "sign": "+"})], [], seed=seed)
    e0 = sim._energy0["weyl_bcc"]
    sim.step(ticks)
    e1 = sim.channels["weyl_bcc"].energy(sim.states["weyl_bcc"])
    return _check("norm_drift", "weyl_bcc", "machine-precision", abs(e1 - e0) / e0)


def unitarity_weyl(L=16, seed=0) -> Check:
    sim = Simulation(LatticeSpec(L=L, topology="bcc"),
                     [build_channel({"type": "weyl_bcc", "sign": "+"})], [], seed=seed)
    res = sim.channels["weyl_bcc"].unitarity_residual(sim.lattice, sim.rng)
    return _check("unitarity_residual", "weyl_bcc", "exact", res)


def gravity_deflection(L=64, seed=0) -> Check:
    ch = build_channel({"type": "gravity_dielectric", "M": 50.0, "sigma": 3.0,
                        "G": 1.0, "impact_parameter": 10})
    sim = Simulation(LatticeSpec(L=L, topology="cubic", c_lat=1.0), [ch], [], seed=seed)
    obs = ch.observables(sim.states["gravity_dielectric"], sim.lattice)
    # quantitative gate: agree with finite-aperture GR to <1%.
    c = _check("eikonal_vs_GR", "gravity_dielectric", "quantitative", obs["rel_error"])
    c.tol = 0.01
    c.passed = obs["rel_error"] <= 0.01
    return c


def resume_roundtrip(L=10, seed=3, ticks=120) -> Check:
    def build():
        return Simulation(LatticeSpec(L=L, topology="bcc"),
                          [build_channel({"type": "weyl_bcc", "sign": "+"})],
                          [NormConservation(every=10), DispersionFit(every=50)],
                          seed=seed, name="ck", target_ticks=ticks)
    A = build(); ra = A.run(ticks)
    fa, ga = A.states["weyl_bcc"]["f"], A.states["weyl_bcc"]["g"]
    B = build(); B.run(0); B.step(ticks // 2)
    import tempfile, os
    p = B.checkpoint(os.path.join(tempfile.gettempdir(), "casim_verify_ck.npz"))
    C = Simulation.resume(p); C.step(ticks - ticks // 2); rc = C.collect_results()
    fc, gc = C.states["weyl_bcc"]["f"], C.states["weyl_bcc"]["g"]
    same = (np.array_equal(fa, fc) and np.array_equal(ga, gc) and
            ra["observers"]["norm_conservation"]["records"]
            == rc["observers"]["norm_conservation"]["records"] and
            ra["observers"]["dispersion_fit"]["records"]
            == rc["observers"]["dispersion_fit"]["records"])
    return _check("resume_bit_identical", "weyl_bcc", "exact", 0.0 if same else 1.0)


# ----------------------------------------------------------------------
# Tier-2 sourced / coupled channels (bit-identical to their kernels).
# ----------------------------------------------------------------------
def fidelity_backreaction(L=8, ticks=20, g_lat=0.5, eps=0.05) -> Check:
    """Engine fermion↔W loop == the E2E `_run_loop` kernel, bit-for-bit."""
    from casim.engine.gauge import weak_wmu as ca_wmu

    from .engine.core.coupled import gaussian_packet, su2_expmap
    # reference loop
    f_nu = gaussian_packet(L, (L // 2, L // 2, L // 2), 1.5, k0=(0.5, 0, 0))
    f_e = gaussian_packet(L, (L // 2 - 1, L // 2, L // 2), 1.5)
    g_nu = np.zeros_like(f_nu); g_e = np.zeros_like(f_e)
    E = np.zeros((3, L, L, L)); B = np.zeros((3, L, L, L)); A = np.zeros((3, L, L, L))
    for _ in range(ticks):
        J = ca_wmu.fermion_isospin_current(f_nu, f_e)
        E_rot, B_rot = ca_wmu.w_propagation_step_spectral(E, B)
        E = E_rot + g_lat * J; B = B_rot; A = A + E
        U_a, U_b = su2_expmap(eps * A)
        f_nu, f_e, g_nu, g_e = ca_wmu.covariant_weyl_step_3d_bcc(
            f_nu, f_e, g_nu, g_e, [(U_a, U_b)] * 8, sign="+")
    # engine
    sim = Simulation(LatticeSpec(L=L, topology="bcc"), [
        build_channel({"type": "w_sourced", "name": "w_sourced",
                       "fermion": "fermion_doublet", "g_lat": g_lat}),
        build_channel({"type": "fermion_doublet", "name": "fermion_doublet",
                       "w_field": "w_sourced", "eps": eps})], [], seed=0)
    sim.step(ticks)
    fs, ws = sim.states["fermion_doublet"], sim.states["w_sourced"]
    res = max(np.max(np.abs(fs["f_nu"] - f_nu)), np.max(np.abs(fs["f_e"] - f_e)),
              np.max(np.abs(ws["E"] - E)), np.max(np.abs(ws["B"] - B)))
    return _check("kernel_fidelity", "fermion↔W", "exact", res)


def fidelity_beta_decay(L=16, ticks=10, g_lat=0.8, m_W=0.6) -> Check:
    """Engine β-decay W trajectory == emit_w_minus + chiral Proca loop, bit-for-bit.
    (The W± propagate on the chiral law, F91; the reference followed the channel
    from the even Proca step to the chiral one on 2026-09-29.)"""
    from casim.engine.gauge import charged_current as cc
    profA = cc.gaussian_blob((L, L, L), (L // 4, L // 2, L // 2), 1.5)
    f_u = profA.astype(complex) * (0.9 + 0.0j)
    f_d = profA.astype(complex) * (0.7 * np.exp(0.3j))
    E_W = np.zeros((3, L, L, L)); B_W = np.zeros((3, L, L, L))
    E_W, B_W, _ = cc.emit_w_minus(E_W, B_W, f_u, f_d, g_lat=g_lat, dt=1.0)
    for _ in range(ticks - 1):
        E_W, B_W = cc.w_massive_propagation_step_chiral(E_W, B_W, m_W, dt=1.0)
    sim = Simulation(LatticeSpec(L=L, topology="bcc"),
                     [build_channel({"type": "beta_decay", "g_lat": g_lat,
                                     "m_W": m_W, "sigma": 1.5})], [], seed=0)
    sim.step(ticks)
    bd = sim.states["beta_decay"]
    res = max(np.max(np.abs(bd["E_W"] - E_W)), np.max(np.abs(bd["B_W"] - B_W)))
    return _check("kernel_fidelity", "beta_decay", "exact", res)


def charge_photon_continuity(L=13) -> Check:
    """F87 charge current is divergence-free under the model BCC curl (odd L)."""
    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [build_channel({"type": "charge_photon", "amp": 0.2,
                                     "sigma": 2.0})], [], seed=0)
    obs = sim.channels["charge_photon"].observables(
        sim.states["charge_photon"], sim.lattice)
    return _check("charge_continuity", "charge_photon", "machine-precision",
                  obs["div_J_max"])


# ----------------------------------------------------------------------
# Tier-3 non-unitary / heavy channels.
# ----------------------------------------------------------------------
def fidelity_gauge_mc(L=4, D=4, beta=5.6, ticks=5, seed=7) -> Check:
    """Engine gauge-MC Markov chain == the lgt_fork_A_mc heat-bath loop,
    bit-for-bit (same engine RNG, cold start)."""
    from casim.engine.forks.gauge import lgt_fork_A_mc as mc
    ref_rng = np.random.default_rng(seed)
    U = mc.cold_links(L, D)
    for _ in range(ticks):
        U = mc.heatbath_sweep(U, beta, ref_rng, n_or=1)
    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [build_channel({"type": "gauge_mc", "D": D, "beta": beta,
                                     "start": "cold", "n_or": 1})], [], seed=seed)
    sim.step(ticks)
    res = float(np.max(np.abs(sim.states["gauge_mc"]["U"] - U)))
    return _check("kernel_fidelity", "gauge_mc", "exact", res)


def fidelity_refraction(L=64, ticks=10) -> Check | None:
    """Engine variable-c refraction == ca_curved Strang loop, bit-for-bit.
    Returns None (skipped) where SciPy / ca_curved is unavailable."""
    try:
        from casim.engine.lattice import curved as cv
    except Exception:
        return None
    from .engine.core.channel import build_channel as _bc
    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [_bc({"type": "refraction_2d", "n_sub": 4})], [], seed=0)
    st0 = sim.states["refraction_2d"]
    f, g, c_field, n_sub = st0["f"].copy(), st0["g"].copy(), st0["c_field"], st0["n_sub"]
    sim.step(ticks)
    for _ in range(ticks):
        f, g = cv.weyl_step_2d_varc_strang(f, g, c_field, n_sub=n_sub)
    res = max(float(np.max(np.abs(sim.states["refraction_2d"]["f"] - f))),
              float(np.max(np.abs(sim.states["refraction_2d"]["g"] - g))))
    return _check("kernel_fidelity", "refraction_2d", "exact", res)


ALL_CHECKS = [
    fidelity_photon_pair, fidelity_weyl_bcc, fidelity_w_chiral,
    fidelity_z_even, fidelity_gluon_bcc,
    norm_drift_weyl, unitarity_weyl, gravity_deflection, resume_roundtrip,
    fidelity_backreaction, fidelity_beta_decay, charge_photon_continuity,
    fidelity_gauge_mc,
]
# SciPy-dependent; appended only when ca_curved imports (else inventory stays
# green where SciPy is absent, e.g. the sandbox).
def _maybe_refraction():
    try:
        from casim.engine.lattice import curved  # noqa: F401
        return [fidelity_refraction]
    except Exception:
        return []


ALL_CHECKS += _maybe_refraction()


def run_all() -> List[Check]:
    return [fn() for fn in ALL_CHECKS]
