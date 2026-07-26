"""Test wrapper for F248 — the explicit transverse-traceless (TT) graviton mode
on the BCC lattice (closes the F180 §5 open build).

Runs the self-contained real-arithmetic battery in
ca-simulation/forks/gr_fork_F248_tt_graviton_bcc.py and asserts all five checks
pass, plus the load-bearing physics facts:
  A  TT polarisation basis exists for ANY direction (helicity +/-2, TT, orthonormal);
  B  the spin-2 TT projector fixes both helicities (eigenvalue 1) and kills the
     gauge (spin-1/0) parts, so both helicities share the ONE pole q0 = c_lat|q|;
  C  the BCC even law gives exact non-birefringence and a k->0 slope = 1/sqrt(3)
     isotropically, with a helicity-blind O((k a)^2) anisotropy;
  D  a real-space TT packet on the genuine BCC law propagates at c_lat, both
     polarisations identically;
  E  the explicit BCC constituent loop with tensor vertices is helicity-degenerate
     and quadratic in |q| (the Q^2 pole realised on the lattice).
"""
import importlib.util
import os

HERE = os.path.dirname(__file__)
FORK = os.path.abspath(os.path.join(
    HERE, "..", "..", "ca-simulation", "forks", "gr_fork_F248_tt_graviton_bcc.py"))


def _run():
    spec = importlib.util.spec_from_file_location("gr_fork_F248", FORK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.run_all(), mod


def _detail(res, name):
    for c in res["checks"]:
        if c["check"] == name:
            return c
    raise KeyError(name)


def test_F248_all_checks_pass():
    res, _ = _run()
    failed = [c["check"] for c in res["checks"] if not c["pass"]]
    assert not failed, f"F248 checks failed: {failed}"
    assert res["summary"]["n_pass"] == res["summary"]["n_total"] == 5


def test_F248_tt_basis_any_direction_exact():
    res, _ = _run()
    d = _detail(res, "A_tt_basis_any_direction")["detail"]
    # symmetric, traceless, transverse, orthonormal, helicity +/-2 -- all machine precision
    assert float(d["max_trace"]) < 1e-12
    assert float(d["max_transverse_khat_dot_e"]) < 1e-12
    assert float(d["max_gram_minus_I"]) < 1e-12
    assert float(d["max_helicity_phase_residual"]) < 1e-11


def test_F248_projector_common_pole():
    res, _ = _run()
    d = _detail(res, "B_projector_and_common_pole")["detail"]
    assert float(d["max_Lambda^2_minus_Lambda"]) < 1e-12   # idempotent projector
    assert float(d["max_TT_fixed_point_residual"]) < 1e-12  # both helicities eigenvalue 1
    assert float(d["max_longitudinal_annihilated"]) < 1e-12
    assert float(d["max_trace_annihilated"]) < 1e-12
    assert d["f2_at_q=0"] == "0"                            # pole at Q^2 = 0
    assert "sqrt(3)" in d["poles_q0"]                       # q0 = |q|/sqrt(3) = c_lat|q|


def test_F248_non_birefringent_and_luminal():
    res, mod = _run()
    d = _detail(res, "C_bcc_dispersion_nonbirefringent")["detail"]
    # the two helicities ride one scalar dispersion -> exact non-birefringence
    assert float(d["birefringence_max_|dOmega|"]) == 0.0
    # k->0 slope = c_lat = 1/sqrt(3) for every direction
    for _, dev in d["rel_slope_dev_from_c_lat"].items():
        assert float(dev) < 1e-6
    # leading anisotropy is O(k^2): doubling k quadruples the deviation
    ratio = float(d["anisotropy_[111]_k2overk1_ratio"].split()[0])
    assert abs(ratio - 4.0) < 0.3


def test_F248_realspace_packet_speed():
    res, _ = _run()
    d = _detail(res, "D_realspace_bcc_wavefront")["detail"]
    # centroid travels at the group velocity ( = c_lat in the small-k limit )
    assert abs(float(d["measured_over_group_velocity"]) - 1.0) < 0.02
    assert float(d["polarisation_speed_difference"]) < 1e-12   # non-birefringent
    assert float(d["max_transverse_khat_dot_e"]) < 1e-12
    assert float(d["max_trace"]) < 1e-12


def test_F248_bcc_bubble_degenerate_quadratic():
    res, _ = _run()
    d = _detail(res, "E_bcc_tensor_bubble_degenerate")["detail"]
    # explicit BCC constituent loop: the two helicities are degenerate, and the
    # spin-2 form factor is quadratic in |q| (the Q^2 pole)
    assert float(d["helicity_degeneracy_rel"]) < 1e-9
    assert float(d["quadratic_fit_resid_rel"]) < 5e-2
