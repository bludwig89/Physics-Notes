"""
F180 — gravitational-wave speed from the dielectric rotation rule.

Tests the derivation that delta-K perturbations obey a hyperbolic wave equation
whose speed is exactly c_grav = c_lat = 1/sqrt(3), the same light cone as the
paired photon, so |c_grav - c_photon|/c = 0 identically (GW170817 survived).

See findings/F180-gravitational-wave-speed.md and
src/casim/engine/forks/gravity/gr_fork_F180_gw_speed.py.
"""
import os
import sys

import pytest

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
# Forks are loaded by bare name, not as package submodules;
# importing casim appends engine/forks/<sector>/ to sys.path.
import casim as _casim  # noqa: E402,F401
import gr_fork_F180_gw_speed as gw  # noqa: E402


def test_A_coefficient_identity():
    r = gw.check_A_coefficient_identity()
    assert r["res_one_over_G_vs_8pi_sqrt3"] == 0.0
    assert r["res_8piG_c4_vs_a2clat_hbarc"] == 0.0
    assert r["pass"]


def test_B_inverse_coupling_carries_clat():
    r = gw.check_B_inverse_coupling_carries_clat()
    for v in r["detail"].values():
        assert v["rel_spread"] < 5e-3
    assert r["pass"]


def test_C_graviton_inherits_lightcone():
    r = gw.check_C_graviton_inherits_lightcone()
    # induced self-energy depends only on the constituent invariant c^2|q|^2-q0^2
    for v in r["detail"].values():
        assert v["invariant_isocontour_spread"] < 1e-2
    # and the light cone tracks the constituent speed
    assert abs(r["detail"]["c=0.57735"]["lightcone_speed_c_grav"] - gw.C_LAT) < 1e-12
    assert r["pass"]


def test_D_dispersion_and_gw170817():
    r = gw.check_D_dispersion_and_gw170817()
    assert r["slope_residual_c_g_minus_c_gamma"] == 0.0
    assert r["model_residual_at_100Hz_upper_bound"] < 1e-15
    assert r["pass"]


def test_E_realspace_wavefront():
    r = gw.check_E_realspace_wavefront()
    assert abs(r["speed_over_c_lat"] - 1.0) < 0.06
    assert r["static_poisson_fixedpoint_rel_dev"] < 5e-3
    assert r["pass"]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
