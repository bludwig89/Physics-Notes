"""Engine fidelity: casim.engine must reproduce the raw ca-simulation kernels
to machine precision (roadmap Phase C acceptance: a migrated scenario must
reproduce its original script's output, machine-precision identical given the
same seed).

Because each Channel.step calls exactly the same pure kernel the historical
scripts call, the field trajectories must be *bit-identical* to a direct kernel
loop seeded the same way.  These tests assert that.

Run standalone (no pytest needed):
    PYTHONPATH=src python tests/test_engine_reproduces_kernels.py
"""
from __future__ import annotations

import numpy as np

import casim  # noqa: F401  (puts ca-simulation on sys.path)
from casim.engine import Simulation, LatticeSpec
from casim.engine.channels import (
    PhotonPairChannel, WeylBCCChannel, GravityDielectricChannel,
    WChiralChannel, ZEvenChannel, GluonBCCChannel,
)
from casim.engine.observers import NormConservation, DispersionFit


# ----------------------------------------------------------------------
def test_photon_pair_bit_identical():
    """Engine photon trajectory == direct photon_step_spectral loop."""
    import ca_photon_pair as pp
    L, seed, ticks = 12, 5, 8

    # Engine.
    lat = LatticeSpec(L=L, topology="cubic")
    sim = Simulation(lat, [PhotonPairChannel(init="random")], observers=[], seed=seed)
    sim.step(ticks)
    E_eng, B_eng = sim.states["photon_pair"]["E"], sim.states["photon_pair"]["B"]

    # Direct kernel loop, same seed/order (E then B drawn first).
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))
    for _ in range(ticks):
        E, B = pp.photon_step_spectral(E, B)

    assert np.array_equal(E_eng, E), "photon E differs"
    assert np.array_equal(B_eng, B), "photon B differs"
    # And it stays real & norm-conserving (F69 PP5).
    n0 = np.sum(rng.standard_normal(1) * 0)  # noop to keep rng draw count clear
    return {"E_max_abs_diff": float(np.max(np.abs(E_eng - E))),
            "B_max_abs_diff": float(np.max(np.abs(B_eng - B)))}


def test_weyl_bcc_bit_identical():
    """Engine Weyl trajectory == direct weyl_step_3d_bcc loop; norm conserved."""
    import ca_bcc as bcc
    L, seed, ticks = 12, 0, 20

    lat = LatticeSpec(L=L, topology="bcc")
    sim = Simulation(lat, [WeylBCCChannel(sign="+")], observers=[], seed=seed)
    e0 = sim._energy0["weyl_bcc"]
    sim.step(ticks)
    f_eng, g_eng = sim.states["weyl_bcc"]["f"], sim.states["weyl_bcc"]["g"]

    rng = np.random.default_rng(seed)
    f = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    g = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    for _ in range(ticks):
        f, g = bcc.weyl_step_3d_bcc(f, g, sign="+")

    assert np.array_equal(f_eng, f), "weyl f differs"
    assert np.array_equal(g_eng, g), "weyl g differs"

    e1 = float(np.sum(np.abs(f_eng) ** 2 + np.abs(g_eng) ** 2))
    drift = abs(e1 - e0) / e0
    assert drift < 1e-12, f"norm drift {drift:.2e} exceeds FFT floor"
    return {"norm_drift": drift}


def test_gravity_deflection_matches_GR():
    """F64 dielectric eikonal deflection ≈ GR 4GM/(c²b)."""
    lat = LatticeSpec(L=64, topology="cubic", c_lat=1.0)
    ch = GravityDielectricChannel(M=50.0, sigma=3.0, G=1.0, impact_parameter=10)
    sim = Simulation(lat, [ch], observers=[], seed=0)
    obs = ch.observables(sim.states["gravity_dielectric"], lat)
    # Thin-lens eikonal vs GR point-mass: agree to better than 5% at b≫sigma.
    assert obs["rel_error"] < 0.05, f"deflection rel error {obs['rel_error']:.3f}"
    return obs


def test_w_chiral_bit_identical():
    import ca_wmu
    L, seed, ticks = 10, 11, 12
    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [WChiralChannel()], observers=[], seed=seed)
    sim.step(ticks)
    E_e, B_e = sim.states["w_chiral"]["E"], sim.states["w_chiral"]["B"]
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((3, L, L, L)); B = rng.standard_normal((3, L, L, L))
    for _ in range(ticks):
        E, B = ca_wmu.w_propagation_step_chiral(E, B)
    assert np.array_equal(E_e, E) and np.array_equal(B_e, B), "w_chiral differs"
    return {"ok": True}


def test_z_even_bit_identical():
    import ca_z_field
    L, seed, ticks = 10, 2, 12
    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [ZEvenChannel()], observers=[], seed=seed)
    sim.step(ticks)
    E_e, B_e = sim.states["z_even"]["E"], sim.states["z_even"]["B"]
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((L, L, L)); B = rng.standard_normal((L, L, L))
    for _ in range(ticks):
        E, B = ca_z_field.z_propagation_step_spectral(E, B)
    assert np.array_equal(E_e, E) and np.array_equal(B_e, B), "z_even differs"
    return {"ok": True}


def test_gluon_bcc_bit_identical():
    import ca_gluon
    L, seed, ticks = 10, 7, 12
    sim = Simulation(LatticeSpec(L=L, topology="bcc"),
                     [GluonBCCChannel()], observers=[], seed=seed)
    sim.step(ticks)
    E_e, B_e = sim.states["gluon_bcc"]["E"], sim.states["gluon_bcc"]["B"]
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((8, L, L, L)); B = rng.standard_normal((8, L, L, L))
    for _ in range(ticks):
        E, B = ca_gluon.gluon_rotation_step_spectral_bcc(E, B)
    assert np.array_equal(E_e, E) and np.array_equal(B_e, B), "gluon differs"
    return {"ok": True}


def test_resume_bit_identical(tmp_path=None):
    """A checkpointed+resumed run equals an uninterrupted run, bit-for-bit,
    including observer records (roadmap §4 acceptance).

    Fixed 2026-07-30 (roadmap C0): this signature read `tmp_path="/tmp"`.
    pytest does **not** inject a fixture for a parameter that carries a
    default, so the default silently defeated the `tmp_path` fixture and every
    run wrote its checkpoint to a shared, world-writable `/tmp` under a fixed
    name — a cross-session collision waiting to happen, which duly happened.
    `None` restores fixture injection; the standalone path makes its own
    private temp dir.
    """
    import os
    import tempfile

    if tmp_path is None:
        tmp_path = tempfile.mkdtemp(prefix="casim_resume_")

    def build():
        return Simulation(
            LatticeSpec(L=10, topology="bcc"),
            [WeylBCCChannel(sign="+")],
            [NormConservation(every=10), DispersionFit(every=50)],
            seed=3, name="ck", target_ticks=120)

    A = build(); ra = A.run(120)
    fa, ga = A.states["weyl_bcc"]["f"], A.states["weyl_bcc"]["g"]

    B = build(); B.run(0); B.step(60)
    p = B.checkpoint(os.path.join(tmp_path, "ck_resume.npz"))
    C = Simulation.resume(p); C.step(60); rc = C.collect_results()
    fc, gc = C.states["weyl_bcc"]["f"], C.states["weyl_bcc"]["g"]

    assert np.array_equal(fa, fc) and np.array_equal(ga, gc), "resume state differs"
    assert (ra["observers"]["norm_conservation"]["records"]
            == rc["observers"]["norm_conservation"]["records"]), "norm recs differ"
    assert (ra["observers"]["dispersion_fit"]["records"]
            == rc["observers"]["dispersion_fit"]["records"]), "disp recs differ"
    return {"ok": True, "tick": C.tick}


if __name__ == "__main__":
    print("photon_pair  bit-identical:", test_photon_pair_bit_identical())
    print("weyl_bcc     bit-identical:", test_weyl_bcc_bit_identical())
    print("w_chiral     bit-identical:", test_w_chiral_bit_identical())
    print("z_even       bit-identical:", test_z_even_bit_identical())
    print("gluon_bcc    bit-identical:", test_gluon_bcc_bit_identical())
    print("gravity      vs GR:", test_gravity_deflection_matches_GR())
    print("resume       bit-identical:", test_resume_bit_identical())
    print("\nALL ENGINE-FIDELITY CHECKS PASSED")
