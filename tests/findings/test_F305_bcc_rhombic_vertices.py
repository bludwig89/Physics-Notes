"""F305 — LPT Feynman rules of the GENUINE BCC gauge action (the 4-bond rhombus).

Registry record `F305-bcc-rhombic-vertices`, tier gate, entry
`check_bcc_vertices` on `casim.engine.gauge.lpt_bcc_vertex`.
"""
import json
import os

import pytest

from casim.engine.gauge.lpt_bcc_vertex import (
    brillouin_zone, check_bcc_vertices, gate_antisymmetry, gate_isotropy,
    gate_three_point, gate_two_point, gate_ward, mode_fork, propagator_split,
)


def _results_path(name):
    here = os.path.abspath(__file__)
    root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    return os.path.join(root, "test-results", name)


def test_G1_two_point_is_the_bcc_inverse_propagator():
    """The load-bearing gate: the generated 2-point vertex IS
    Gamma_ij = delta_ij sum_l khat_l^2 - khat_i khat_j, with K = 1."""
    g = gate_two_point()
    assert g["structure_spread"] < 1e-12, g
    assert abs(g["K_mean"] - 1.0) < 1e-12, g
    assert g["pass"]


def test_G2_four_link_axes_are_isotropic_exactly():
    g = gate_isotropy()
    assert g["deviation_from_4I"] == 0.0, g          # sum_i d_i d_i^T = 4 I exactly
    for q in g["quartic_coefficient_measured"]:
        assert abs(q + 1.0 / 3.0) < 1e-3, g
    assert g["pass"]


def test_G3_three_point_has_the_yang_mills_continuum_limit():
    """K = i and the deviation falls as a^2 (rel-spread ratio ~100 per decade)."""
    g = gate_three_point()
    assert abs(g["rows"][-1]["K_im"] - 1.0) < 1e-6, g
    assert abs(g["rows"][-1]["K_re"]) < 1e-9, g
    for o in g["order_ratios"]:
        assert 50.0 < o < 200.0, g
    assert g["pass"]


def test_G4_and_G5_antisymmetry_and_ward():
    a = gate_antisymmetry()
    w = gate_ward()
    assert a["max_residual"] < 1e-13, a
    assert w["max_relative_residual"] < 1e-13, w


def test_G6_mode_fork_is_real_and_named():
    """One gauge zero mode and FOUR massless modes against three in continuum
    4-D YM; the redundant link-axis combination is the extra one, and it couples."""
    g = mode_fork()
    assert g["n_zero_modes"] == 1, g
    assert g["nhat_eigenvector_in_continuum_limit"], g
    assert g["vertex_coupling_to_nhat"] > 1e-3, g
    assert g["projector_isometry_residual"] == 0.0, g
    assert g["n_propagating_bcc"] == 4 and g["n_propagating_continuum_4d"] == 3


def test_G7_cube_holds_exactly_four_brillouin_zones():
    g = brillouin_zone()
    assert abs(g["cube_over_bz"] - 4.0) < 1e-9, g
    assert g["periodicity_residual"] < 1e-12, g
    assert abs(g["ws_fraction_of_cube_mc"] - 0.25) < 5e-3, g


def test_declared_gap_action_and_propagator_are_not_the_same_object():
    """Honest scope: S/4 -> 3 Omega_even^2 only in the continuum limit."""
    g = propagator_split()
    assert g["agree_in_continuum"], g
    assert g["worst_generic_deviation"] > 0.1, g     # they really do differ


def test_control_tilting_nhat_reddens_G6_and_nothing_else():
    """The declared D9 control, asserted here as well as in the registry."""
    base = check_bcc_vertices()["legs"]
    ctrl = check_bcc_vertices(nhat_perturb=0.4)["legs"]
    assert base["G6_mode_fork"] is True
    assert ctrl["G6_mode_fork"] is False
    for k in base:
        if k != "G6_mode_fork":
            assert ctrl[k] == base[k], (k, base[k], ctrl[k])


def test_full_record_passes_and_writes_its_artifact():
    r = check_bcc_vertices()
    assert r["pass"], r["legs"]
    with open(_results_path("F305_bcc_rhombic_vertices.json"), "w") as f:
        json.dump(r, f, indent=1, default=str)


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
