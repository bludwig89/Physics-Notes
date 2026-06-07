"""Gravity-element suite — the F64 fork mainlined (audit B.2 #1, 2026-06-06).

Asserts:
  G1  structural constants — G_LATTICE = c_lat⁴/(8π) = 1/(72π) exactly (F79
      closed form in lattice units), F106 coupling = 1 (lattice units)
  G2  static back-compat — the default (non-dynamic) gravity_dielectric
      channel is bit-identical to the pre-merge construction (poisson_open
      lens; step is the identity)
  G3  map consistency (F106) — ∇²ln K = −coupling·T⁰⁰ holds to machine
      precision through the production maps (phi_source → solve_phi_poisson
      → dielectric_from_phi)
  G4  D-EM8 in 3D — the Poisson well is a static fixed point of
      phi_wave_step; a free Φ pulse propagates causally at c_g; the free
      field conserves energy
  G5  engine sourcing — a dynamic gravity channel sourced by a massive
      particle digs a well (Φ < 0 at the packet, K > 1), causally (far
      corner flat at early ticks)
  G6  two-way coupling — flat field ⇒ the massive particle step is
      bit-identical to the no-gravity step; lapse mix is exactly unitary;
      in a static well a rest packet free-falls toward the mass (F62-D2a,
      the sign-corrected mix attracts)

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/test_gravity_element.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import casim  # noqa: E402,F401  (puts ca-simulation on sys.path)
from casim.engine import Simulation, LatticeSpec, build_channel  # noqa: E402

try:
    import pytest
    mark = pytest.mark
except ImportError:  # standalone
    class _M:
        def __getattr__(self, _):
            return lambda f: f
    mark = _M()


def _lattice(L, topology="bcc"):
    return LatticeSpec(L=L, topology=topology)


# ----------------------------------------------------------------------
@mark.exact
def test_G1_structural_constants():
    from casim.gravity import C_LAT_BCC, F106_COEFF_LATTICE, G_LATTICE
    # F79 closed form G = a²c³/(8π√3 ħ) in lattice units (a=ħ=1, c=c_lat):
    G_f79 = C_LAT_BCC ** 3 / (8.0 * np.pi * np.sqrt(3.0))
    assert G_LATTICE == 1.0 / (72.0 * np.pi)
    assert abs(G_f79 / G_LATTICE - 1.0) < 1e-14
    # F106-E1 in lattice units: 8πG/c⁴ = a²c_lat/(ħc) = 1.
    coeff = 8.0 * np.pi * G_LATTICE / C_LAT_BCC ** 4
    assert abs(coeff - F106_COEFF_LATTICE) < 1e-14


@mark.exact
def test_G2_static_mode_bit_identical():
    """Default channel == pre-merge static lens, and step is the identity."""
    from casim.gravity import gaussian_mass_3d, solve_poisson_3d_open
    L, M, sigma, G = 16, 5.0, 2.0, 1.0
    ch = build_channel({"type": "gravity_dielectric", "name": "g",
                        "M": M, "sigma": sigma, "G": G})
    lat = _lattice(L)
    rng = np.random.default_rng(0)
    st = ch.init_state(lat, rng)
    # pre-merge construction, verbatim:
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d_open(rho, G_N=G)
    c = 1.0 / np.sqrt(3.0)
    K = np.exp(-2.0 * phi / c ** 2)
    assert np.array_equal(st["phi"], phi)
    assert np.array_equal(st["K"], K)
    assert "phi_prev" not in st                      # no leapfrog memory
    st2 = ch.step(st, lat)
    assert st2 is st                                 # static: identity


@mark.machine_precision
def test_G3_f106_map_consistency():
    """∇²ln K = −coupling·T⁰⁰ through the production maps."""
    from casim.gravity import (dielectric_from_phi, lap_nd, phi_source,
                               solve_phi_poisson)
    L, c0 = 32, 1.0 / np.sqrt(3.0)
    x = np.arange(L) - L / 2
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    T00 = np.exp(-(X ** 2 + Y ** 2 + Z ** 2) / (2 * 2.0 ** 2))
    T00 *= 1e-2 / T00.sum()      # weak field, but above the exp/log
    #                              round-trip floor (ln(1+ε) precision)
    coupling = 1.0                                  # structural (F106)
    phi = solve_phi_poisson(phi_source(T00, c0, coupling))
    _, _, K = dielectric_from_phi(phi, c0)
    lnK = np.log(K)
    # the solver inverts the exact lap_nd symbol, so the F106 law holds as a
    # *discrete identity*: lap_nd(ln K) == −coupling·T⁰⁰ (zero-mean) to the
    # exp/log round-trip floor.
    lhs = lap_nd(lnK)
    rhs = -coupling * (T00 - T00.mean())            # periodic zero-mean source
    resid = np.max(np.abs(lhs - rhs)) / np.max(np.abs(rhs))
    assert resid < 1e-10, resid


@mark.machine_precision
def test_G4_dem8_dynamics_3d():
    """D-EM8 mainlined: fixed point, causal speed, energy conservation."""
    from casim.gravity import (lap_nd, phi_field_energy, phi_source,
                               phi_wave_step, solve_phi_poisson)
    L, c_g, dt = 48, 1.0 / np.sqrt(3.0), 0.5
    x = np.arange(L) - L / 2
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)

    # (a) static fixed point
    T00 = np.exp(-R ** 2 / (2 * 3.0 ** 2)); T00 *= 0.02 / T00.sum()
    src = phi_source(T00, 1.0, coupling=1.0)
    src = src - src.mean()
    phi0 = solve_phi_poisson(src)
    phi, phi_prev = phi0.copy(), phi0.copy()
    maxdev = 0.0
    for _ in range(120):
        phi, phi_prev = phi_wave_step(phi, phi_prev, src, c_g, dt)
        maxdev = max(maxdev, float(np.max(np.abs(phi - phi0))))
    assert maxdev / float(np.max(np.abs(phi0))) < 5e-3

    # (b)+(c) free pulse: causal speed + conserved energy
    phi = np.exp(-R ** 2 / (2 * 2.5 ** 2)); phi_prev = phi.copy()
    zeros = np.zeros_like(phi)
    times, radii, Es = [], [], []
    for n in range(60):
        phi, phi_prev = phi_wave_step(phi, phi_prev, zeros, c_g, dt)
        Es.append(phi_field_energy(phi, phi_prev, c_g, dt))
        if n % 10 == 9:
            thr = 0.02 * float(np.abs(phi).max()) + 1e-12
            m = np.abs(phi) > thr
            times.append((n + 1) * dt)
            radii.append(float(R[m].max()) if m.any() else 0.0)
    speed = float(np.polyfit(times[1:], radii[1:], 1)[0])
    assert abs(speed / c_g - 1.0) < 0.15, speed      # causal at ~c_g
    Es = np.array(Es)
    # one-sided velocity estimator biases the launch-from-rest transient;
    # after it settles (tick ~20) the free field conserves energy
    assert abs(Es[-1] - Es[20]) / Es[20] < 1e-2      # kinetic term conserves


@mark.machine_precision
def test_G5_engine_sourcing_psi_to_K():
    """A massive packet sources its own well through the engine (F106)."""
    L, m = 20, 0.5
    cen = L // 2
    sim = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "particle", "name": "e", "species": "e_R",
                       "mass": m,
                       "init": {"center": [cen, cen, cen], "width": 2.0},
                       "couplings": {"gravity": "gfield"}}),
        build_channel({"type": "gravity_dielectric", "name": "gfield",
                       "M": 0.0, "dynamic": True, "dt": 1.0,
                       "sources": {"e": m}}),
    ], seed=7)
    g0 = sim.states["gfield"]
    assert float(np.max(np.abs(g0["phi"]))) == 0.0   # starts flat
    sim.step(12)
    g = sim.states["gfield"]
    # a well forms at the packet: Φ < 0 there, K > 1
    assert g["phi"][cen, cen, cen] < 0.0
    assert g["K"][cen, cen, cen] > 1.0
    # causality: the far corner (distance ≳ L√3/2 ≈ 17 > c_g·12 ≈ 7) is
    # still (numerically) flat relative to the well
    well = abs(float(g["phi"][cen, cen, cen]))
    corner = abs(float(g["phi"][0, 0, 0]))
    assert corner < 0.05 * well, (corner, well)


@mark.exact
def test_G6_two_way_lapse_coupling():
    """Flat ⇒ bit-identical; mix unitary; well attracts (F62 sign)."""
    from casim.gravity import lapse_mix_half
    L, m = 24, 0.5
    cen = L // 2

    # (a) flat field: gravity-coupled step bit-identical to free step
    sim_flat = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "gravity_dielectric", "name": "gfield",
                       "M": 0.0}),
        build_channel({"type": "particle", "name": "e", "species": "e_R",
                       "mass": m, "init": {"center": [cen, cen, cen],
                                           "width": 2.0},
                       "couplings": {"gravity": "gfield"}}),
    ], seed=3)
    sim_free = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "particle", "name": "e", "species": "e_R",
                       "mass": m, "init": {"center": [cen, cen, cen],
                                           "width": 2.0}}),
    ], seed=3)
    sim_flat.step(5); sim_free.step(5)
    for k in ("eta_u", "eta_d", "chi_u", "chi_d"):
        assert np.array_equal(sim_flat.states["e"][k], sim_free.states["e"][k])

    # (b) the lapse mix is exactly unitary
    rng = np.random.default_rng(1)
    arrs = [rng.normal(size=(8, 8, 8)) + 1j * rng.normal(size=(8, 8, 8))
            for _ in range(4)]
    sqrtA = 1.0 - 0.05 * rng.random((8, 8, 8))
    out = lapse_mix_half(*arrs, sqrtA, m=0.5)
    n_in = sum(float(np.sum(np.abs(a) ** 2)) for a in arrs)
    n_out = sum(float(np.sum(np.abs(a) ** 2)) for a in out)
    assert abs(n_out / n_in - 1.0) < 1e-14

    # (c) free fall: a rest packet released beside a static well moves
    # toward it (the F62 sign-corrected mix ATTRACTS)
    off = 5
    sim_well = Simulation(lattice=_lattice(L), channels=[
        build_channel({"type": "gravity_dielectric", "name": "gfield",
                       "M": 60.0, "sigma": 2.5, "G": 1.0}),
        build_channel({"type": "particle", "name": "e", "species": "e_R",
                       "mass": m, "init": {"center": [cen + off, cen, cen],
                                           "width": 2.0},
                       "couplings": {"gravity": "gfield"}}),
    ], seed=3)
    x0 = sim_well.channels["e"].observables(
        sim_well.states["e"], sim_well.lattice)["centroid"][0]
    sim_well.step(40)
    x1 = sim_well.channels["e"].observables(
        sim_well.states["e"], sim_well.lattice)["centroid"][0]
    fall = x0 - x1                                   # >0 ⇒ moved toward cen
    assert fall > 0.05, fall
    # norm conserved through the coupled evolution
    norm = sim_well.channels["e"].energy(sim_well.states["e"])
    assert abs(norm - 1.0) < 1e-12


if __name__ == "__main__":
    for fn in [test_G1_structural_constants, test_G2_static_mode_bit_identical,
               test_G3_f106_map_consistency, test_G4_dem8_dynamics_3d,
               test_G5_engine_sourcing_psi_to_K,
               test_G6_two_way_lapse_coupling]:
        fn()
        print(f"PASS {fn.__name__}")
    print("all gravity-element checks passed")
