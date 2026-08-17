"""Total energy, stress-energy and the closed gravity loop — P3.4/P3.5/P3.6, F270.

*Created 2026-08-01 - 00:05.*

Blocker B4 said "six incompatible energy conventions; **nothing a coupled run
could fail**".  That sentence is the specification for this file: every check
below is something a coupled run can now fail.
"""
from __future__ import annotations

import numpy as np
import pytest

from casim.engine.core.channel import field_energy
from casim.engine.core.simulation import LatticeSpec, Simulation
from casim.gravity import (
    T00_dirac_rest, T00_dirac_kinetic, T0i_dirac, T00_field_energy,
    dielectric_mix_half,
)


def _sim(scn):
    return Simulation.from_scenario(scn)


# ======================================================================
# P3.5 — one energy convention
# ======================================================================
def test_T1_one_gauge_energy_convention_across_the_engine():
    """Every (E,B) channel reports ½Σ(E²+B²) — the B4 defect, closed.

    Before P3.5 ``PhotonPairChannel.energy`` was exactly twice
    ``WSourcedChannel.energy`` for the same field, which is why nothing could
    sum them.  The check is deliberately written as "all channels agree with the
    one helper", so a channel added later with the other convention fails here.
    """
    rng = np.random.default_rng(0)
    L = 8
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))
    expect = 0.5 * float(np.sum(E * E) + np.sum(B * B))
    assert field_energy(E, B) == pytest.approx(expect, rel=0, abs=0)

    from casim.engine.core import channels as ch_mod, coupled as cp_mod
    # coupled.field_energy must BE the same object, not merely agree
    assert cp_mod.field_energy is field_energy
    for cls in (ch_mod.PhotonPairChannel, ch_mod.WChiralChannel,
                ch_mod.ZEvenChannel, ch_mod.GluonBCCChannel):
        c = cls(name="x")
        assert c.energy({"E": E, "B": B}) == pytest.approx(expect)


def test_T2_gauge_energy_agrees_with_the_gravity_source():
    """``energy`` and the T⁰⁰ gravity sources it now the same number.

    They were a factor 2 apart: gravity was sourced from ½(E²+B²) while the
    channel reported Σ(E²+B²). A field cannot weigh half what it costs.
    """
    rng = np.random.default_rng(1)
    L = 6
    E = rng.standard_normal((8, L, L, L))
    B = rng.standard_normal((8, L, L, L))
    assert field_energy(E, B) == pytest.approx(float(T00_field_energy(E, B).sum()))


def test_T3_total_energy_conserves_to_machine_class():
    """The P3 acceptance number: total energy over a long free run.

    The gate reads ``exactness_class``, so a regression shows as a class change
    and not only as a digit.
    """
    r = _sim({
        "name": "te", "lattice": {"L": 16, "topology": "cubic"}, "seed": 3,
        "channels": [{"type": "photon_pair", "name": "gamma", "init": "random"}],
        "observers": [{"type": "total_energy", "every": 25}],
    }).run(1000)
    s = r["observers"]["total_energy"]["summary"]
    assert s["exactness_class"] == "machine", s
    assert s["max_rel_drift"] < 1e-12
    assert s["covered"] == "1/1" and not s["missing"]


def test_T4_a_missing_energy_leg_is_reported_not_counted_as_zero():
    """A channel with no expressible energy density must appear in ``missing``.

    A total that silently drops a term is worse than no total, because it looks
    conserved. ``strict: true`` turns the omission into a stated violation.
    """
    r = _sim({
        "name": "te2", "lattice": {"L": 8, "topology": "bcc"}, "seed": 1,
        "channels": [
            {"type": "gluon_bcc", "name": "g"},
            {"type": "weyl_bcc", "name": "psi"},      # no mass ⇒ no energy leg
        ],
        "observers": [{"type": "total_energy", "every": 5, "strict": True}],
    }).run(10)
    s = r["observers"]["total_energy"]["summary"]
    assert s["missing"] == ["psi"]
    assert s["covered"] == "1/2"
    assert "strict_violation" in s


# ======================================================================
# P3.4 — stress-energy
# ======================================================================
def test_T5_colour_axis_is_summed_not_broadcast():
    """The B5 broadcast bug: a coloured spinor must not rank-4 the gravity field.

    Reproduces the exact configuration that used to silently produce a
    three-copy gravitational field, one per colour.
    """
    rng = np.random.default_rng(2)
    L = 6
    z = np.zeros((3, L, L, L), dtype=complex)
    f = rng.standard_normal((3, L, L, L)) + 1j * rng.standard_normal((3, L, L, L))
    t = T00_dirac_rest(f, z, z, z, m=1.0)
    assert t.shape == (L, L, L), "colour axis survived — the B5 bug is back"
    # and it is a genuine sum over colour, not a slice
    assert t == pytest.approx(np.sum(np.abs(f) ** 2, axis=0))
    # rank-3 input is untouched, so no committed result moves
    g = f[0]
    assert T00_dirac_rest(g, 0 * g, 0 * g, 0 * g, m=2.0) == pytest.approx(
        2.0 * np.abs(g) ** 2)


def _packet(L, w, k=0.0):
    """Normalised Gaussian on an L³ lattice, optionally boosted along +x."""
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    c = L // 2
    env = np.exp(-((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2) / w)
    env = env / np.sqrt(np.sum(env ** 2))
    return (env * np.exp(1j * k * X)).astype(complex)


def test_T6_a_moving_packet_gravitates_by_its_momentum_not_its_mass():
    """D-EM3, quantitatively: the kinetic leg carries exactly the boost energy.

    The rest leg is boost-blind — that is the defect P3.4 exists to close, and
    the first assertion pins it, because a "fix" that also changed the rest leg
    would invalidate every committed F106 result.

    The kinetic leg is then checked against its own closed form rather than a
    threshold.  A centred difference on :math:`\\psi = \\phi\\,e^{ikx}` gives
    :math:`\\sin k` where the continuum gives :math:`k`, so the boost energy is

    .. math:: \\Delta u_\\text{kin} = \\tfrac12 c^2 \\sin^2\\!k \\sum|\\psi|^2

    up to a k-*independent* envelope-averaging factor that tends to 1 as the
    packet widens.  Both halves of that statement are asserted: the ratio to the
    prediction is constant across three momenta (so the :math:`\\sin^2 k` law
    holds exactly), and it moves toward 1 with envelope width (so the residual
    is the envelope, not a wrong coefficient).
    """
    zero = np.zeros((32, 32, 32), dtype=complex)

    slow, fast = _packet(32, 72.0), _packet(32, 72.0, k=1.2)
    assert float(T00_dirac_rest(slow, zero, zero, zero, m=1.0).sum()) == \
        pytest.approx(float(T00_dirac_rest(fast, zero, zero, zero, m=1.0).sum())), \
        "rest leg must stay boost-blind — that is why the kinetic leg is separate"

    from casim.constants import c_lat

    def ratio(L, w, k):
        z = np.zeros((L, L, L), dtype=complex)
        s = float(T00_dirac_kinetic(_packet(L, w), z, z, z).sum())
        f = float(T00_dirac_kinetic(_packet(L, w, k), z, z, z).sum())
        return (f - s) / (0.5 * c_lat ** 2 * np.sin(k) ** 2)

    # (a) the sin²k law: the ratio is k-independent at fixed envelope
    rs = [ratio(32, 72.0, k) for k in (0.4, 0.8, 1.2)]
    assert max(rs) - min(rs) < 1e-4, rs
    assert rs[0] == pytest.approx(0.9726, abs=2e-3)

    # (b) the residual is the envelope: widen it and the ratio approaches 1
    assert ratio(40, 128.0, 0.8) > rs[1]
    assert ratio(40, 128.0, 0.8) == pytest.approx(1.0, abs=0.02)


def test_T7_momentum_density_vanishes_at_rest_and_points_along_the_boost():
    """A scalar Φ cannot represent a moving source; T⁰ⁱ is the leg that can."""
    L = 16
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    env = np.exp(-((X - 8) ** 2 + (Y - 8) ** 2 + (Z - 8) ** 2) / 8.0)
    zero = np.zeros_like(env, dtype=complex)

    at_rest = T0i_dirac(env.astype(complex), zero, zero, zero)
    assert np.allclose(at_rest, 0.0, atol=1e-12)

    boosted = T0i_dirac((env * np.exp(1j * 0.8 * X)).astype(complex),
                        zero, zero, zero)
    px, py, pz = (float(b.sum()) for b in boosted)
    assert px > 0.0
    assert abs(py) < 1e-9 * abs(px) and abs(pz) < 1e-9 * abs(px)


# ======================================================================
# P3.6 — the closed gravity loop
# ======================================================================
def test_T8_dielectric_mix_is_pointwise_unitary_and_flat_identity():
    """The gauge-side gravity coupling may not create or leak field energy.

    Pointwise, not just in sum — otherwise the P3.5 total-energy gate would stop
    meaning anything the moment gravity is switched on.
    """
    rng = np.random.default_rng(4)
    L = 8
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))
    K = 1.0 + 0.5 * rng.random((L, L, L))
    E2, B2 = dielectric_mix_half(E, B, K, 0.7)
    assert np.allclose(E2 ** 2 + B2 ** 2, E ** 2 + B ** 2, rtol=0, atol=1e-13)

    flat = np.ones((L, L, L))
    E3, B3 = dielectric_mix_half(E, B, flat, 0.7)
    assert np.array_equal(E3, E) and np.array_equal(B3, B), \
        "K ≡ 1 must be the exact identity, or every no-gravity result moves"


def test_T8b_uniform_dielectric_is_exact_and_has_no_free_parameter():
    """F271: a uniform K is the **exact** rotation at Ω(k)/K — machine precision.

    This is the sharpest statement separating the k-resolved propagator from the
    eikonal it replaces. With K constant the perturbation vanishes identically,
    so every mode is slowed by exactly 1/K and the step is exactly unitary. The
    eikonal cannot reproduce it at any ω₀: it would need ω₀ = Ω(k), which is the
    k-dependence it replaces with a single number.
    """
    from casim.engine.gauge.photon import (
        photon_step_dielectric, photon_step_spectral, _even_rotate)
    rng = np.random.default_rng(7)
    L = 16
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))

    # K ≡ 1 is bit-identical to the free photon — no gravity, no change
    a = photon_step_dielectric(E, B, np.ones((L, L, L)))
    b = photon_step_spectral(E, B)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])

    for K in (1.3, 2.5, 7.0):
        got = photon_step_dielectric(E, B, np.full((L, L, L), K))
        want = _even_rotate(E, B, 1.0 / K)
        assert np.allclose(got[0], want[0], rtol=0, atol=1e-13)
        assert np.allclose(got[1], want[1], rtol=0, atol=1e-13)


def test_T8c_the_split_converges_at_second_order_and_stays_normed():
    """F271: Trotter error ~ 1/n², norm drift converging — neither plateaus.

    The two derived corrections are what produce this. Weyl-symmetric ordering
    makes the generator self-adjoint, so the norm drift *converges* instead of
    plateauing at 1.1e-5; carrying the h² term restores the second order Strang
    is supposed to give (it was 1.0 without it).
    """
    from casim.engine.gauge.photon import photon_step_dielectric
    rng = np.random.default_rng(1)
    L = 16
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    c = L // 2
    K = 1.0 + 0.6 * np.exp(-((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2) / 20.0)
    n0 = float(np.sum(E ** 2 + B ** 2))

    ref = photon_step_dielectric(E, B, K, n_sub=256)
    errs, norms = [], []
    for ns in (4, 8, 16, 32):
        e, b = photon_step_dielectric(E, B, K, n_sub=ns)
        errs.append(max(float(np.max(np.abs(e - ref[0]))),
                        float(np.max(np.abs(b - ref[1])))))
        norms.append(abs(float(np.sum(e ** 2 + b ** 2)) - n0) / n0)

    for lo, hi in zip(errs, errs[1:]):          # second order in the field
        assert 3.4 < lo / hi < 4.6, errs
    assert norms[-1] < 1e-8, norms             # and the norm drift converges
    for lo, hi in zip(norms, norms[1:]):
        assert hi < lo, norms


def test_T8d_a_ray_bends_toward_higher_K_linearly_in_the_gradient():
    """F271: zero gradient ⇒ exactly zero bend; response linear; right direction.

    The *magnitude* against the continuum ray equation is checked separately and
    loosely on purpose — see the finding. A finite packet in a varying medium is
    not a geometric-optics ray, and the measured ratio runs 1.45 → 0.96 as the
    packet widens, so a tight assertion here would be pinning an artifact.
    """
    from casim.engine.gauge.photon import build_beam_packet, photon_step_dielectric
    L = 32
    y0 = L // 2
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")

    def drift(a):
        K = 1.0 + a * np.sin(2 * np.pi * (Y - y0) / L)
        E, B, _ = build_beam_packet(L, m_index=3, axis=0, sigma=4.0,
                                    center=(6, y0, L // 2))
        def cen():
            u = (E ** 2 + B ** 2).sum(axis=0)
            p = u.sum(axis=(0, 2))
            th = 2 * np.pi * np.arange(L) / L
            z = np.sum(p * np.exp(1j * th)) / p.sum()
            return (L / (2 * np.pi)) * float(np.angle(z)) % L
        prev, tot = cen(), 0.0
        for _ in range(14):
            E, B = photon_step_dielectric(E, B, K, n_sub=3)
            c = cen()
            tot += (c - prev + L / 2) % L - L / 2
            prev = c
        return tot

    assert abs(drift(0.0)) < 1e-12, "a flat dielectric must not bend anything"
    d1, d2 = drift(0.02), drift(0.04)
    assert d1 > 0 and d2 > 0, "light must bend toward higher K (slower medium)"
    assert d2 / d1 == pytest.approx(2.0, rel=0.05), (d1, d2)


def test_T9_light_responds_to_gravity_in_the_production_engine():
    """B5's second half: a gauge channel reads K, outside the fork.

    Two otherwise identical photon runs, one with a gravity partner wired. The
    fields must differ (gravity does something) *and* the coupled run must
    conserve energy (it does it unitarily).
    """
    base = {
        "name": "lens", "lattice": {"L": 24, "topology": "cubic"}, "seed": 5,
        "channels": [
            {"type": "gravity_dielectric", "name": "gmass", "M": 6.0, "sigma": 3.0},
            {"type": "photon_pair", "name": "gamma", "init": "beam",
             "axis": "x", "m_index": 3},
        ],
    }
    flat = _sim(base)
    lensed_spec = {**base, "channels": [
        base["channels"][0],
        {**base["channels"][1], "gravity": "gmass", "grav_n_sub": 4},
    ]}
    lensed = _sim(lensed_spec)

    e0 = lensed.channels["gamma"].energy(lensed.states["gamma"])
    flat.step(50)
    lensed.step(50)
    e1 = lensed.channels["gamma"].energy(lensed.states["gamma"])

    delta = float(np.max(np.abs(lensed.states["gamma"]["E"]
                                - flat.states["gamma"]["E"])))
    assert delta > 1e-3, "gravity had no effect on the gauge field"

    # Energy is conserved *convergently*, not to machine precision — the F271
    # half-step is a truncated exponential, so at finite `n_sub` there is a
    # residual. The claim that matters is that it shrinks when asked to, and the
    # eikonal it replaced had no such handle at all. Assert the convergence, not
    # a magic constant.
    drift = abs(e1 - e0) / e0
    assert drift < 1e-6, drift

    fine = _sim({**lensed_spec, "channels": [
        lensed_spec["channels"][0],
        {**lensed_spec["channels"][1], "grav_n_sub": 16},
    ]})
    f0 = fine.channels["gamma"].energy(fine.states["gamma"])
    fine.step(50)
    f1 = fine.channels["gamma"].energy(fine.states["gamma"])
    drift_fine = abs(f1 - f0) / f0
    assert drift_fine < drift / 4.0, (drift, drift_fine)


def test_T10_gravity_under_blockspin_refuses_rather_than_guesses():
    """F271 removed the last free parameter, and added one honest refusal.

    ``grav_omega0`` is gone — the rate is Ω(k), mode by mode. What replaces the
    old error is narrower and real: the renormalised block-spin rule
    Ω_b(κ)=Ω(κ/b) and the dielectric's own coarse-graining have not been shown
    to commute (F133 covers the free rule only), so a gravitating photon on a
    coarse lattice raises instead of silently applying an unverified factor
    inside a gravity result.
    """
    sim = _sim({
        "name": "bs", "lattice": {"L": 8, "topology": "cubic"}, "seed": 0,
        "channels": [
            {"type": "gravity_dielectric", "name": "gm", "M": 1.0, "sigma": 2.0},
            {"type": "photon_pair", "name": "g", "init": "random",
             "gravity": "gm"},
        ],
    })
    sim.step(1)                       # fine at block = 1
    sim.lattice.block = 2
    with pytest.raises(NotImplementedError, match="block-spin"):
        sim.step(1)
