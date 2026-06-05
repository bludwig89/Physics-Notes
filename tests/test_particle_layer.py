"""Particle-layer suite (roadmap-particle-layer.md, Phase P1).

Asserts:
  P1.1  registry exactness — Gell-Mann–Nishijima per species (constructor-
        enforced), C-conjugation involution, FG-1 anomaly traces exactly 0
  P1.2  force-applicability matrix derived from charges; forbidden couplings
        refused at build time
  P1.3  free particle is bit-identical to the raw ``weyl_step_3d_bcc`` kernel
  P1.4  norm conservation of the free particle (machine precision)
  P1.5  weak-coupled particle doublet reproduces the audited E2E pattern
        (``w_sourced`` + ``fermion_doublet``) bit-for-bit
  P1.6  EM source: a charged particle injects photon field energy; an
        unsourced photon stays exactly zero
  P1.7  strong source: total colour charge of a pure-r quark packet is
        exactly (norm/2, norm/(2√3)) in (J³, J⁸); gluon field grows
  P1.8  gravity background readouts: φ < 0 near the mass, K > 1
  P1.9  checkpoint/resume of a particle scenario is bit-identical

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/test_particle_layer.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import casim  # noqa: E402,F401  (puts ca-simulation on sys.path)
from casim.engine import Simulation, LatticeSpec, build_channel  # noqa: E402
from casim.particles import (  # noqa: E402
    REGISTRY, get_spec, doublet_specs, anomaly_traces,
)

try:
    import pytest
    mark = pytest.mark
    raises = pytest.raises
except Exception:  # pragma: no cover
    import contextlib

    class _M:
        def __getattr__(self, _):
            return lambda f: f
    mark = _M()

    @contextlib.contextmanager
    def raises(exc):
        try:
            yield
        except exc:
            return
        raise AssertionError(f"expected {exc.__name__}")

ROOT3 = float(np.sqrt(3.0))


def _lattice(L=8):
    return LatticeSpec(L=L, dims=3, topology="bcc", c_lat=1.0 / ROOT3)


# ----------------------------------------------------------------------
@mark.exact
def test_P1_1_registry_exact():
    # 7 first-gen species + 7 antiparticles
    assert len(REGISTRY) == 14
    for s in REGISTRY.values():
        assert s.Q == s.T3 + s.Y / 2                  # GMN, exact Fraction
        cc = s.conjugate().conjugate()
        assert (cc.T3, cc.Y, cc.Q, cc.B, cc.Lnum) == \
               (s.T3, s.Y, s.Q, s.B, s.Lnum)          # C is an involution
        assert s.conjugate().Q == -s.Q                # F53 P1
    tr = anomaly_traces()
    for key, val in tr.items():
        assert val == Fraction(0), f"anomaly trace {key} = {val} != 0"


@mark.exact
def test_P1_2_coupling_matrix():
    assert get_spec("nu_e_L").couples_to() == frozenset({"gravity", "weak"})
    assert get_spec("e_L").couples_to() == frozenset({"gravity", "weak", "em"})
    assert get_spec("e_R").couples_to() == frozenset({"gravity", "weak", "em"})
    for q in ("u_L", "d_L", "u_R", "d_R"):
        assert get_spec(q).couples_to() == \
            frozenset({"gravity", "weak", "em", "strong"})
    # Forbidden: lepton → strong, refused at build time.
    with raises(ValueError):
        build_channel({"type": "particle", "name": "bad", "species": "e_L",
                       "couplings": {"strong": "gluon_field"}})
    # Forbidden: neutrino → em.
    with raises(ValueError):
        build_channel({"type": "particle", "name": "bad2", "species": "nu_e_L",
                       "couplings": {"em": "photon_field"}})
    # P1 restriction: singlet weak (Z) coupling not wired yet.
    with raises(ValueError):
        build_channel({"type": "particle", "name": "bad3", "species": "e_R",
                       "couplings": {"weak": "w_field"}})


@mark.exact
def test_P1_3_free_particle_bit_identical_to_kernel():
    import ca_bcc
    from casim.engine.coupled import gaussian_packet
    L, ticks = 8, 12
    lat = _lattice(L)
    ch = build_channel({"type": "particle", "name": "e", "species": "e_R",
                        "init": {"center": [4, 4, 4], "width": 1.5,
                                 "k0": [0.5, 0.0, 0.0]}})
    sim = Simulation(lattice=lat, channels=[ch], seed=3)
    sim.step(ticks)
    # Raw kernel reference, same initial packet.
    f = gaussian_packet(L, (4, 4, 4), 1.5, k0=(0.5, 0.0, 0.0))
    g = np.zeros_like(f)
    for _ in range(ticks):
        f, g = ca_bcc.weyl_step_3d_bcc(f, g, sign="+")
    assert np.array_equal(sim.states["e"]["f"], f)
    assert np.array_equal(sim.states["e"]["g"], g)


@mark.machine_precision
def test_P1_4_free_particle_norm():
    lat = _lattice(8)
    ch = build_channel({"type": "particle", "name": "e", "species": "e_R",
                        "init": {"center": [4, 4, 4], "width": 1.5}})
    sim = Simulation(lattice=lat, channels=[ch], seed=0)
    e0 = sim.state_norms()["e"]
    sim.step(50)
    assert abs(sim.state_norms()["e"] - e0) / e0 < 1e-12


@mark.exact
def test_P1_5_weak_loop_reproduces_e2e_pattern():
    """particle(species=lepton_doublet_L, weak) == fermion_doublet channel."""
    L, ticks = 8, 10
    ref = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "w_sourced", "name": "w_field",
                       "fermion": "fermion_doublet"}),
        build_channel({"type": "fermion_doublet", "name": "fermion_doublet",
                       "w_field": "w_field"}),
    ], seed=7)
    new = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "w_sourced", "name": "w_field",
                       "fermion": "electron"}),
        build_channel({"type": "particle", "name": "electron",
                       "species": "lepton_doublet_L",
                       "init": {"center": [L // 2, L // 2, L // 2],
                                "width": 1.5, "k0": [0.5, 0.0, 0.0]},
                       "couplings": {"weak": "w_field"}}),
    ], seed=7)
    ref.step(ticks)
    new.step(ticks)
    for key in ("f_nu", "f_e", "g_nu", "g_e"):
        assert np.array_equal(ref.states["fermion_doublet"][key],
                              new.states["electron"][key]), key
    for key in ("E", "B", "A"):
        assert np.array_equal(ref.states["w_field"][key],
                              new.states["w_field"][key]), key


@mark.machine_precision
def test_P1_6_em_source():
    L = 8
    sim = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "particle", "name": "electron",
                       "species": "lepton_doublet_L",
                       "init": {"center": [4, 4, 4], "width": 1.5,
                                "k0": [0.5, 0.0, 0.0]},
                       "couplings": {"em": "photon_field"}}),
        build_channel({"type": "photon_sourced", "name": "photon_field",
                       "sources": ["electron"]}),
        build_channel({"type": "photon_sourced", "name": "photon_unsourced"}),
    ], seed=1)
    sim.step(10)
    assert sim.state_norms()["photon_field"] > 0.0
    assert sim.state_norms()["photon_unsourced"] == 0.0   # exactly


@mark.exact
def test_P1_7_strong_source_colour_charge():
    L = 8
    sim = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "particle", "name": "quark", "species": "u_L",
                       "colour": "r",
                       "init": {"center": [4, 4, 4], "width": 1.5},
                       "couplings": {"strong": "gluon_field"}}),
        build_channel({"type": "gluon_sourced", "name": "gluon_field",
                       "sources": ["quark"]}),
    ], seed=2)
    # Total colour charge of a pure-r packet: q†T³q = norm/2, q†T⁸q = norm/(2√3)
    J = sim.states["quark"]["J_colour"]
    norm = sim.state_norms()["quark"]
    totals = J.reshape(8, -1).sum(axis=1)
    assert abs(totals[2] - norm / 2.0) < 1e-12                   # a=3
    assert abs(totals[7] - norm / (2.0 * ROOT3)) < 1e-12         # a=8
    for a in (0, 1, 3, 4, 5, 6):
        assert abs(totals[a]) < 1e-12
    sim.step(10)
    assert sim.state_norms()["gluon_field"] > 0.0


@mark.machine_precision
def test_P1_8_gravity_background_readout():
    L = 16
    sim = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "gravity_dielectric", "name": "gmass",
                       "M": 5.0, "sigma": 2.0}),
        build_channel({"type": "particle", "name": "e", "species": "e_R",
                       "init": {"center": [L // 2, L // 2, L // 2],
                                "width": 1.5},
                       "couplings": {"gravity": "gmass"}}),
    ], seed=4)
    sim.step(2)
    obs = sim.channels["e"].observables(sim.states["e"], sim.lattice)
    assert obs["grav_potential"] < 0.0          # Newtonian well
    assert obs["grav_K_centroid"] > 1.0         # K = exp(-2φ/c²) > 1
    assert obs["couplings"]["gravity"]["tier"] == "background"


@mark.exact
def test_P1_9_checkpoint_resume_bit_identical():
    L, t1, t2 = 8, 5, 5

    def _channels():
        return [
            build_channel({"type": "w_sourced", "name": "w_field",
                           "fermion": "electron"}),
            build_channel({"type": "particle", "name": "electron",
                           "species": "lepton_doublet_L",
                           "init": {"center": [4, 4, 4], "width": 1.5,
                                    "k0": [0.5, 0.0, 0.0]},
                           "couplings": {"weak": "w_field"}}),
        ]

    straight = Simulation(lattice=_lattice(L), channels=_channels(), seed=9)
    straight.step(t1 + t2)

    broken = Simulation(lattice=_lattice(L), channels=_channels(), seed=9)
    broken.step(t1)
    with tempfile.TemporaryDirectory() as td:
        path = broken.checkpoint(os.path.join(td, "p_t5.npz"))
        resumed = Simulation.resume(path)
        resumed.step(t2)
    for key in ("f_nu", "f_e", "g_nu", "g_e"):
        assert np.array_equal(straight.states["electron"][key],
                              resumed.states["electron"][key]), key
    for key in ("E", "B", "A"):
        assert np.array_equal(straight.states["w_field"][key],
                              resumed.states["w_field"][key]), key


# ======================================================================
# Phase P2 — two-way em/strong back-action + F27 mass (ca_minimal_coupling)
# ======================================================================
def _packet(L, center, width, k0=None):
    from casim.engine.coupled import gaussian_packet
    return gaussian_packet(L, center, width, k0=k0)


@mark.exact
def test_P2_1_u1_wrap_alpha0_bit_identical():
    import ca_bcc
    import ca_minimal_coupling as mc
    L = 8
    f = _packet(L, (4, 4, 4), 1.5, k0=(0.4, 0, 0))
    g = np.zeros_like(f)
    a0 = np.zeros((L, L, L))
    f1, g1 = mc.u1_wrap_weyl_step_3d_bcc(f, g, a0, q=-1.0)
    f2, g2 = ca_bcc.weyl_step_3d_bcc(f, g)
    assert np.array_equal(f1, f2) and np.array_equal(g1, g2)


@mark.machine_precision
def test_P2_2_u1_wrap_exact_gauge_covariance():
    """S[α+β](e^{iqβ}ψ) = e^{iqβ} S[α](ψ) — exact for any β(x) (3D BCC port
    of the F41/F42 covariance statement)."""
    import ca_minimal_coupling as mc
    rng = np.random.default_rng(11)
    L, q = 8, -1.0
    f = _packet(L, (4, 4, 4), 1.5, k0=(0.3, 0.2, 0))
    g = (rng.standard_normal((L, L, L))
         + 1j * rng.standard_normal((L, L, L))) * 0.01
    alpha = rng.standard_normal((L, L, L))
    beta = rng.standard_normal((L, L, L))
    ph = np.exp(1j * q * beta)
    lhs = mc.u1_wrap_weyl_step_3d_bcc(ph * f, ph * g, alpha + beta, q=q)
    rhs = mc.u1_wrap_weyl_step_3d_bcc(f, g, alpha, q=q)
    res = max(np.max(np.abs(lhs[0] - ph * rhs[0])),
              np.max(np.abs(lhs[1] - ph * rhs[1])))
    assert res < 1e-13, res


@mark.machine_precision
def test_P2_3_u1_wrap_unitary():
    import ca_minimal_coupling as mc
    rng = np.random.default_rng(5)
    L = 8
    f = _packet(L, (4, 4, 4), 1.5)
    g = np.zeros_like(f)
    alpha = rng.standard_normal((L, L, L))
    n0 = np.sum(np.abs(f) ** 2 + np.abs(g) ** 2)
    for _ in range(50):
        f, g = mc.u1_wrap_weyl_step_3d_bcc(f, g, alpha, q=-1.0)
        alpha = alpha + 0.05 * rng.standard_normal((L, L, L))  # dynamic α
    n1 = np.sum(np.abs(f) ** 2 + np.abs(g) ** 2)
    assert abs(n1 - n0) / n0 < 1e-12


@mark.machine_precision
def test_P2_4_bloch_acceleration_exact_force_law():
    """The wrap's force law on the lattice, exactly: for integer charge q a
    uniform-gradient angle α_n(x) = n·(2π/L)·x is single-valued on the torus
    (e^{-iq(2π/L)x} closes since q ∈ ℤ), and each tick shifts every momentum
    mode by exactly −q·(2π/L)·x̂ — one k-bin per tick (Bloch acceleration).
    After N ticks the momentum spectrum is the initial spectrum rolled by
    −qN bins, to FFT round-off.  Sign check: −q∇α is the kick direction."""
    import ca_minimal_coupling as mc
    L, N = 8, 3
    x = np.arange(L)
    X = np.meshgrid(x, x, x, indexing="ij")[0].astype(float)
    grad = 2.0 * np.pi / L

    for q in (-1.0, +1.0):
        f = _packet(L, (4, 4, 4), 1.5)
        g = np.zeros_like(f)
        spec0 = (np.abs(np.fft.fftn(f)) ** 2
                 + np.abs(np.fft.fftn(g)) ** 2)
        for n in range(1, N + 1):
            alpha = n * grad * X            # α grows linearly per tick
            f, g = mc.u1_wrap_weyl_step_3d_bcc(f, g, alpha, q=q)
        # Undo the wrap's outer frame phase to compare spectra directly.
        ph_frame = np.exp(-1j * q * N * grad * X)
        specN = (np.abs(np.fft.fftn(ph_frame * f)) ** 2
                 + np.abs(np.fft.fftn(ph_frame * g)) ** 2)
        expected = np.roll(spec0, -int(q) * N, axis=0)
        res = np.max(np.abs(specN - expected)) / np.max(spec0)
        assert res < 1e-10, (q, res)


@mark.exact
def test_P2_5_su3_A0_bit_identical_and_unitary():
    import ca_bcc
    import ca_minimal_coupling as mc
    rng = np.random.default_rng(3)
    L = 8
    f_c = np.zeros((3, L, L, L), complex)
    f_c[0] = _packet(L, (4, 4, 4), 1.5)
    g_c = np.zeros_like(f_c)
    fA, gA = mc.su3_rotate_weyl_step_3d_bcc(f_c, g_c, None)
    fr, gr = ca_bcc.weyl_step_3d_bcc(f_c[0], g_c[0])
    assert np.array_equal(fA[0], fr) and np.array_equal(gA[0], gr)
    assert not np.any(fA[1:]) and not np.any(gA[1:])
    # Unitarity with a random potential on:
    A = 0.3 * rng.standard_normal((8, L, L, L))
    n0 = np.sum(np.abs(f_c) ** 2)
    f2, g2 = f_c.copy(), g_c.copy()
    for _ in range(20):
        f2, g2 = mc.su3_rotate_weyl_step_3d_bcc(f2, g2, A, eps=0.1)
    n1 = np.sum(np.abs(f2) ** 2 + np.abs(g2) ** 2)
    assert abs(n1 - n0) / n0 < 1e-12


@mark.machine_precision
def test_P2_6_su3_global_ward_identity():
    """V·S_A(q) = S_{VAV†}(V·q) for constant V ∈ SU(3) — the audited SU(2)
    Ward statement, colour version."""
    import ca_minimal_coupling as mc
    import ca_strong as cstr
    rng = np.random.default_rng(7)
    L = 8
    f_c = (rng.standard_normal((3, L, L, L))
           + 1j * rng.standard_normal((3, L, L, L))) * 0.1
    g_c = (rng.standard_normal((3, L, L, L))
           + 1j * rng.standard_normal((3, L, L, L))) * 0.1
    A = 0.4 * rng.standard_normal((8, L, L, L))
    V = cstr.su3_haar(rng=np.random.default_rng(1))
    fV, gV = mc.su3_global_transform(f_c, g_c, V)
    A_t = mc.su3_adjoint_transform_potential(A, V)
    lhs = mc.su3_rotate_weyl_step_3d_bcc(fV, gV, A_t, eps=0.2)
    rhs0 = mc.su3_rotate_weyl_step_3d_bcc(f_c, g_c, A, eps=0.2)
    rhs = mc.su3_global_transform(rhs0[0], rhs0[1], V)
    res = max(np.max(np.abs(lhs[0] - rhs[0])), np.max(np.abs(lhs[1] - rhs[1])))
    assert res < 1e-12, res


@mark.exact
def test_P2_7_massive_dirac_particle():
    """mass config → exact BCC Dirac split-step; bit-identical to the raw
    kernel; norm conserved; doublet/quark mass refused."""
    from ca_dirac_bcc import dirac_step_3d_bcc_splitstep
    L, m, ticks = 8, 0.3, 10
    ch = build_channel({"type": "particle", "name": "e", "species": "e_R",
                        "mass": m,
                        "init": {"center": [4, 4, 4], "width": 1.5,
                                 "k0": [0.4, 0.0, 0.0]}})
    sim = Simulation(lattice=_lattice(L), channels=[ch], seed=0)
    e0 = sim.state_norms()["e"]
    sim.step(ticks)
    eu = _packet(L, (4, 4, 4), 1.5, k0=(0.4, 0.0, 0.0))
    ed = np.zeros_like(eu); xu = np.zeros_like(eu); xd = np.zeros_like(eu)
    for _ in range(ticks):
        eu, ed, xu, xd = dirac_step_3d_bcc_splitstep(eu, ed, xu, xd, m=m)
    st = sim.states["e"]
    assert np.array_equal(st["eta_u"], eu) and np.array_equal(st["chi_d"], xd)
    assert abs(sim.state_norms()["e"] - e0) / e0 < 1e-12
    with raises(ValueError):
        build_channel({"type": "particle", "name": "bad",
                       "species": "lepton_doublet_L", "mass": 0.2})
    with raises(ValueError):
        build_channel({"type": "particle", "name": "bad2",
                       "species": "u_L", "mass": 0.2})


@mark.quantitative
def test_P2_8_two_way_scenario_end_to_end():
    """Electron (massive, em-coupled) + photon Coulomb sector + quark with
    SU(3) back-action — norms conserved, α and A grow, fields act back."""
    L = 12
    sim = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "gravity_dielectric", "name": "gmass",
                       "M": 1.0, "sigma": 2.0}),
        build_channel({"type": "photon_sourced", "name": "photon_field",
                       "sources": ["electron", "u_quark"]}),
        build_channel({"type": "gluon_sourced", "name": "gluon_field",
                       "sources": ["u_quark"]}),
        build_channel({"type": "particle", "name": "electron",
                       "species": "e_R", "mass": 0.2,
                       "init": {"center": [8, 6, 6], "width": 1.5},
                       "couplings": {"em": "photon_field",
                                     "gravity": "gmass"}}),
        build_channel({"type": "particle", "name": "u_quark",
                       "species": "u_L", "colour": "r",
                       "init": {"center": [3, 6, 6], "width": 1.5},
                       "couplings": {"strong": "gluon_field",
                                     "em": "photon_field",
                                     "gravity": "gmass"}}),
    ], seed=7)
    e0 = sim.state_norms()
    sim.step(20)
    e1 = sim.state_norms()
    for p in ("electron", "u_quark"):
        assert abs(e1[p] - e0[p]) / e0[p] < 1e-10, p
    assert np.any(sim.states["photon_field"]["alpha"])      # Coulomb α active
    assert np.any(sim.states["gluon_field"]["A"])           # gluon A active
    obs = sim.channels["electron"].observables(
        sim.states["electron"], sim.lattice)
    assert obs["couplings"]["em"]["tier"] == "coupled"


# ======================================================================
# Phase P3 — GUI sidebar data feed (headless; live readouts == observables())
# ======================================================================
@mark.exact
def test_P3_1_sidebar_model_matches_observables():
    """The P3 gate: every value in the sidebar model is exactly the value the
    channel's own observables() returns — particles split from fields by role,
    field panels carry the F91 propagator class."""
    from casim.gui.sidebar import sidebar_model, sidebar_text
    L = 12
    sim = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "gravity_dielectric", "name": "gmass",
                       "M": 1.0, "sigma": 2.0}),
        build_channel({"type": "photon_sourced", "name": "photon_field",
                       "sources": ["electron"]}),
        build_channel({"type": "particle", "name": "electron",
                       "species": "e_R", "mass": 0.2,
                       "init": {"center": [8, 6, 6], "width": 1.5},
                       "couplings": {"em": "photon_field", "gravity": "gmass"}}),
    ], seed=1)
    sim.step(6)
    m = sidebar_model(sim)
    assert m["tick"] == sim.tick

    # Role split: the typed particle is a particle; the two fields are fields.
    pnames = {p["name"] for p in m["particles"]}
    fnames = {f["name"] for f in m["fields"]}
    assert pnames == {"electron"}
    assert fnames == {"gmass", "photon_field"}

    # Every payload is bit-identical to the channel's own observables().
    for entry in m["particles"] + m["fields"]:
        ch = sim.channels[entry["name"]]
        ref = ch.observables(sim.states[entry["name"]], sim.lattice)
        assert entry["observables"] == ref, entry["name"]
        assert entry["propagator"] == ch.propagator
        assert entry["type"] == ch.type_name

    # The particle panel surfaces position, velocity, exact charges + tiers.
    e = next(p for p in m["particles"] if p["name"] == "electron")["observables"]
    assert e["couplings"]["em"]["tier"] == "coupled"
    assert e["charges"][0]["Q"] == str(get_spec("e_R").Q)  # exact (str of Fraction)
    # The gravity field panel surfaces K_max; the photon panel α_max.
    g = next(f for f in m["fields"] if f["name"] == "gmass")["observables"]
    assert "K_max" in g and g["K_max"] >= 1.0
    ph = next(f for f in m["fields"]
              if f["name"] == "photon_field")["observables"]
    assert "alpha_max" in ph

    # Text render names every channel and never raises.
    txt = sidebar_text(sim)
    for nm in ("electron", "gmass", "photon_field"):
        assert nm in txt


# ======================================================================
# Phase P4 — composites (F71 proton) + particle-level β-decay (F54)
# ======================================================================
@mark.exact
def test_P4_1_proton_quantum_numbers_exact():
    """Proton uud: Q=+1, B=1, T3=+1/2 (exact Fraction); GMN on the totals;
    ε_abc colour singlet (zero colour charge, zero Casimir) per F71."""
    from casim.particles import get_composite
    p = get_composite("proton")
    qn = p.quantum_numbers()
    assert qn["Q"] == Fraction(1) and qn["B"] == Fraction(1)
    assert qn["T3"] == Fraction(1, 2) and qn["Y"] == Fraction(1)
    assert qn["Q"] == qn["T3"] + qn["Y"] / 2                # GMN exact
    assert p.is_colour_singlet
    assert p.colour_singlet_residual() < 1e-12             # F71 zero colour
    assert abs(p.colour_casimir()) < 1e-12
    # Neutron udd: Q=0, B=1.
    n = get_composite("neutron").quantum_numbers()
    assert n["Q"] == Fraction(0) and n["B"] == Fraction(1)


@mark.exact
def test_P4_2_composite_couplings_derived():
    """A colour singlet carries no net colour ⇒ no long-range strong force;
    em iff total Q≠0 (proton yes, neutron no)."""
    from casim.particles import get_composite
    p = get_composite("proton").couples_to()
    n = get_composite("neutron").couples_to()
    assert "strong" not in p and "strong" not in n        # colourless
    assert "em" in p                                       # Q=+1
    assert "em" not in n                                   # Q=0
    assert "gravity" in p and "gravity" in n


@mark.machine_precision
def test_P4_3_composite_channel_stacks_and_propagates():
    """The stacked-quark proton channel propagates its 3 constituents by the
    audited free kernel (norm conserved) and reports exact aggregate charges."""
    L, ticks = 12, 8
    ch = build_channel({"type": "composite", "name": "proton",
                        "composite": "proton",
                        "init": {"center": [6, 6, 6], "width": 1.5,
                                 "k0": [0.3, 0.0, 0.0]}})
    sim = Simulation(lattice=_lattice(L), channels=[ch], seed=0)
    e0 = sim.state_norms()["proton"]
    sim.step(ticks)
    assert abs(sim.state_norms()["proton"] - e0) / e0 < 1e-12
    obs = ch.observables(sim.states["proton"], sim.lattice)
    assert obs["charges"]["Q"] == "1" and obs["charges"]["B"] == "1"
    assert obs["content"] == "uud"
    assert obs["colour_singlet"] and obs["colour_singlet_residual"] < 1e-12
    assert obs["binding_tier"] == "structural"


@mark.exact
def test_P4_4_beta_decay_conservation_exact():
    """β-decay as a particle-level process (F54): every vertex conserves
    Q, B, L exactly — d→u+W⁻, W⁻→e⁻+ν̄, the full chain, and the composite
    neutron→proton+e⁻+ν̄."""
    from casim.particles import beta_decay_ledger
    led = beta_decay_ledger()
    for key in ("vertex_d_to_u_W", "W_to_e_nubar", "full_d_to_u_e_nubar"):
        d = led[key]
        assert d["dQ"] == Fraction(0), (key, d)
        assert d["dB"] == Fraction(0), (key, d)
        assert d["dL"] == Fraction(0), (key, d)
    comp = led["neutron_to_proton"]
    assert comp["dQ"] == Fraction(0)
    assert comp["dB"] == Fraction(0)
    assert comp["dL"] == Fraction(0)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    fns = [(k, v) for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for name, fn in fns:
        try:
            fn()
            print(f"PASS  {name}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {name}: {exc!r}")
    print(f"\n{len(fns) - failed}/{len(fns)} PASS")
    sys.exit(1 if failed else 0)
