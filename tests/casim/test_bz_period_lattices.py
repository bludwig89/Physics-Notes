"""Which period lattice does each dispersion actually have? — F272 / F267.

*Created 2026-08-01 - 02:45.*

Gate-tier, because two separate bugs have now come from assuming a period a
kernel does not have, and both were invisible until someone measured:

* F272 — ``bgfield_loop`` refolded ``k+q`` by ``2π`` per axis, which the rule
  kernel is not periodic under;
* F265's prescription for that module named the **fcc** BZ, which it is also not
  periodic under.

The cheapest permanent defence is to pin the period lattices themselves, so that
any future refold, mask or BZ average has something to check itself against.
"""
from __future__ import annotations

import numpy as np
import pytest


def _shift_invariance(fn, shift, n=200, seed=0):
    """max |f(k+shift) − f(k)| over random k."""
    rng = np.random.default_rng(seed)
    k = rng.uniform(-1.0, 1.0, (n, 3))
    s = np.asarray(shift, float)
    a = fn(k[:, 0], k[:, 1], k[:, 2])
    b = fn(k[:, 0] + s[0], k[:, 1] + s[1], k[:, 2] + s[2])
    return float(np.max(np.abs(np.asarray(b) - np.asarray(a))))


def _consts():
    """(2π, √3) computed on call.

    Not module-level constants: P1.3's ``import_time_work`` ratchet counts any
    call at module scope, and there is no reason to spend its budget on two
    arithmetic expressions only the test bodies need.
    """
    return 2.0 * np.pi, float(np.sqrt(3.0))


def test_T1_the_rule_dispersion_has_the_sqrt3_fcc_period_not_fcc():
    """Ω_even's period lattice is √3·fcc — the F267 signature, in the gauge sector.

    This is the fact F272 turns on. If this test ever flips, either the BCC
    convention changed or someone rescaled the dispersion, and every BZ average
    downstream needs re-deriving.
    """
    P, R3 = _consts()
    from casim.engine.gauge.gluon_self_energy import omega_even

    # NOT periods — each of these has been assumed by some piece of code
    for shift, name in (((P, 0, 0), "2π per axis (the bgfield_loop refold)"),
                        ((2 * P, 0, 0), "4π per axis"),
                        ((P, P, 0), "plain fcc (make_kgrid_bcc's mask)"),
                        ((P, P, P), "2π(1,1,1)")):
        d = _shift_invariance(omega_even, shift)
        assert d > 1e-3, f"{name} unexpectedly IS a period ({d:.2e})"

    # ARE periods
    for shift, name in (((R3 * P, R3 * P, 0), "√3·fcc (1,1,0)"),
                        ((2 * R3 * P, 0, 0), "√3·fcc (2,0,0)")):
        d = _shift_invariance(omega_even, shift)
        assert d < 1e-10, f"{name} should be a period, got {d:.2e}"


def test_T1b_the_raw_bcc_dispersion_is_also_sqrt3_periodic_not_fcc():
    """F273 §1: the *unhalved* `bcc_dispersion` is √3·fcc-periodic too.

    This is the one that invalidates F265's boundary. F265 held that the gauge
    side had a clean fcc period and earned a factor 4, and only the fermion walk
    did not. Measured, the raw dispersion the gauge side is built from is on the
    same √3 lattice — so the factor 4 never applied anywhere.
    """
    P, R3 = _consts()
    from casim.engine.lattice.bcc import bcc_dispersion

    for sign in ("+", "-"):
        fn = lambda x, y, z, s=sign: bcc_dispersion(x, y, z, sign=s)
        assert _shift_invariance(fn, (P, P, 0)) > 1e-3, "plain fcc is not a period"
        assert _shift_invariance(fn, (R3 * P, R3 * P, 0)) < 1e-10


def test_T1c_the_cube_is_a_biased_subregion_of_the_true_zone():
    """F273 §2: ⟨u⟩ is 0 over the true zone and +0.152 over the cubic grid.

    The consequence for a cot-class moment is not a percentage: ⟨cot ω⟩ vanishes
    identically over the zone (u symmetric about 0 ⇒ ω symmetric about π/2 ⇒
    cot odd about π/2) while the cube gives a converged +0.22. Pinned because
    the classification of I₂ — hence B, hence λ₆ = 0.243 — rests on it.
    """
    P, R3 = _consts()
    from casim.engine.lattice.bcc import _bcc_uvec

    b = R3 * P * np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]], float)
    rng = np.random.default_rng(1)
    k = rng.random((200_000, 3)) @ b
    for sign in ("+", "-"):
        u, _, _, _ = _bcc_uvec(k[:, 0], k[:, 1], k[:, 2], sign=sign)
        assert abs(float(u.mean())) < 0.01, "zone ⟨u⟩ should vanish by symmetry"

    ks = P * np.fft.fftfreq(32)
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing="ij")
    u, _, _, _ = _bcc_uvec(KX, KY, KZ, sign="+")
    assert float(u.mean()) > 0.14, "the cube grid should be visibly biased"


def test_T1d_i2_converges_on_the_cube_and_is_not_drifting_to_zero():
    """F273 §3: I₂'s L→∞ limit is the cube average, not the zone average.

    If I₂ were a stand-in for a continuum BZ integral it would trend toward the
    zone value, which is exactly 0. It does not — it converges to ≈0.222. That
    is the measurement behind classifying it as a mode sum.
    """
    from casim.engine.particles.eg_sextic import i2_lattice

    vals = [i2_lattice(L) for L in (16, 24, 32)]
    assert all(v > 0.2 for v in vals), vals
    assert vals[0] < vals[1] < vals[2], vals            # monotone, not decaying
    assert abs(vals[2] - vals[1]) < abs(vals[1] - vals[0])   # and converging


def test_T2_the_wilson_kernel_is_2pi_periodic_so_its_refold_was_a_no_op():
    """The control that makes removing the refold safe rather than a change.

    Wilson genuinely is 2π-periodic per axis, so dropping the wrap cannot move a
    Wilson number — and measurably does not.
    """
    P, R3 = _consts()
    def wilson(kx, ky, kz):
        return 4.0 * (np.sin(kx / 2) ** 2 + np.sin(ky / 2) ** 2
                      + np.sin(kz / 2) ** 2)

    for shift in ((P, 0, 0), (0, P, 0), (P, P, P)):
        assert _shift_invariance(wilson, shift) < 1e-12


def test_T3_the_refold_is_gone_from_the_background_field_loop():
    """F272: no `% (2*math.pi)` survives in `_Bcoeff_numeric`.

    Written against the source because the defect is a *line*, not a value: the
    numbers it corrupted only diverge once the grid is fine enough for a point to
    cross the cell face (Q > π/n), so a value-only test passes on a coarse grid
    while the bug is still there.
    """
    import inspect
    from casim.engine.gauge import bgfield_loop as bg

    src = inspect.getsource(bg._Bcoeff_numeric)
    body = src.split('"""')[-1]          # skip the docstring, which explains it
    assert "%" not in body, "a modular refold is back in _Bcoeff_numeric"
    assert "kqw" not in body


def test_T4_delta_rule_is_q_flat_and_grid_convergent():
    """The claim the refold was destroying, now asserted both ways.

    q-flatness is what shows b₀ is propagator-independent; grid-convergence is
    what shows the number means anything. With the refold the spread was
    1.6e-2 and the mean moved 70% between n=14 and n=18.
    """
    from casim.engine.gauge.bgfield_loop import lattice_b0_consistency

    a = lattice_b0_consistency(n=10)
    b = lattice_b0_consistency(n=14)

    assert a["b0_propagator_independent"] and b["b0_propagator_independent"]
    assert b["rule_shift_spread"] < 1e-3, b["rule_shift_spread"]
    # grid-convergent: the mean barely moves between resolutions
    assert abs(b["rule_shift_mean"] - a["rule_shift_mean"]) < 5e-3, (
        a["rule_shift_mean"], b["rule_shift_mean"])


def test_T5_b0_stays_exactly_11():
    """The symbolic gate has no grid and must be untouched by any of this."""
    from casim.engine.gauge.bgfield_loop import b0_gate_symbolic
    g = b0_gate_symbolic()
    assert str(g["g_tensor_coeff_total"]) == "22/3"
    assert str(g["g_tensor_coeff_gluon"]) == "20/3"
    assert str(g["g_tensor_coeff_ghost"]) == "2/3"
    assert g["calibration_ok"]


# ----------------------------------------------------------------------
#  F277 — the same defect, in the three modules F272 did not reach
# ----------------------------------------------------------------------
def _refold_free(fn, name):
    """No modular refold survives in `fn`'s executable body.

    Docstrings and `#` comments are stripped first: all three fixed sites carry a
    comment explaining the removed line, and a comment cannot be the defect.
    """
    import inspect
    body = inspect.getsource(fn).split('"""')[-1]
    code = "\n".join(ln.split("#", 1)[0] for ln in body.splitlines())
    assert "%" not in code, f"a modular refold is back in {name}"


def test_T6_the_refold_is_gone_from_all_four_rule_kernel_sites():
    """F277 (audit-V item V-023): the F272 line was a repeat offence.

    It survived in three `src/` modules and one runner, all on the SAME rule
    kernel (3·Ω_even² + kt², period lattice √3·fcc per T1). Source-level for the
    same reason T3 is: the corruption switches on only once Q > π/n, so a
    value-only check passes on a coarse grid while the line is still there.

    The `lpt_*` sites are deliberately NOT listed — their Wilson kernel really is
    2π-periodic per axis (T2), so their wrap is an exact no-op.
    """
    from casim.engine.interactions import qed_vacuum_polarization as vp
    from casim.engine.interactions import qed_electron_self_energy as se
    from casim.engine.gauge import gluon_self_energy as gse

    _refold_free(vp._fermion_B, "qed_vacuum_polarization._fermion_B")
    _refold_free(se._selfenergy_AB, "qed_electron_self_energy._selfenergy_AB")
    _refold_free(gse._bubble, "gluon_self_energy._bubble")


def test_T7_vacuum_polarization_delta_is_q_flat_and_grid_convergent():
    """The claim the refold was destroying in F251, asserted both ways.

    With the refold, Δ = B_rule − B_cont *changed sign* between n=10 and n=14
    and settled at +1.2e-2; without it, it converges monotonically to −2.121e-3.
    The sign is the sharpest assertion available here, so it is asserted.
    """
    from casim.engine.interactions.qed_vacuum_polarization import (
        lattice_b0_consistency)

    a = lattice_b0_consistency(n=10, Qs=(0.1, 0.3))
    b = lattice_b0_consistency(n=14, Qs=(0.1, 0.3))

    assert a["b0_propagator_independent"] and b["b0_propagator_independent"]
    # sign: the refold flipped Δ positive
    assert b["delta_mean"] < 0.0, b["delta_mean"]
    # q-flat: the refold's spread at n=14 was 1.4e-2
    assert b["delta_spread"] < 1e-4, b["delta_spread"]
    # grid-convergent: the refold moved the mean by ~1e-2 over this step
    assert abs(b["delta_mean"] - a["delta_mean"]) < 1e-4, (
        a["delta_mean"], b["delta_mean"])


def test_T8_self_energy_coefficients_are_p_flat():
    """F258's dA drifted 2.3e-4 → 5.9e-4 under the refold; it is now flat."""
    from casim.engine.interactions.qed_electron_self_energy import (
        lattice_consistency)

    r = lattice_consistency(n=14, Ps=(0.1, 0.3))
    assert r["coeff_propagator_independent"]
    # the refold's dA spread at these P was 3.8e-4
    assert r["dA_spread"] < 5e-5, r["dA_spread"]
    assert r["dB_spread"] < 5e-5, r["dB_spread"]


def test_T9_gluon_bubble_runs_at_the_continuum_slope():
    """F155's b₀ universality: the lattice bubble's log-slope must equal the
    continuum's. The refold put the ratio at 0.9933; without it, 1.0000542."""
    from casim.engine.gauge.gluon_self_energy import b0_universal_check

    r = b0_universal_check(n=16, ps=(0.15, 0.30, 0.60))
    assert abs(r["ratio"] - 1.0) < 5e-3, r["ratio"]
