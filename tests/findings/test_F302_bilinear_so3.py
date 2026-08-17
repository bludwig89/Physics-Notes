"""F302 — the sigma-bilinear SO(3) audit.

Registry record: `F302-bilinear-so3-covariance` (gate tier, entry-driven).
The physics lives in `casim.engine.gauge.derive_bilinear_so3`; this file is the
pytest face of it and adds nothing of its own.

The one thing worth knowing while reading: C2 asserts a FAILURE. The transpose
bilinear `phi^T sigma^i psi` is expected to break SO(3) covariance at O(1), and
a run where it suddenly passed would mean either the Pauli basis or the matched
SU(2)/SO(3) pair had changed underneath the test — so the assertion is written
as a lower bound, not an upper one.
"""
from __future__ import annotations

from casim.engine.gauge import derive_bilinear_so3 as m


def test_F302_symbolic_core_is_exact():
    """C1 — every symbolic residual is an exact zero, not a small number."""
    for name, val in m.symbolic_core().items():
        assert abs(val) == 0.0, f"{name} = {val!r}, want exact 0"


def test_F302_transpose_fails_so3():
    """C2 — the transpose bilinear is not a 3-vector, and the miss is O(1)."""
    cov = m.so3_covariance()
    assert cov["transpose_bilinear_G"] > 0.1


def test_F302_covariant_forms():
    """C3 — Cartan plus all four Hermitian production forms are covariant."""
    cov = m.so3_covariance()
    for key, val in cov.items():
        if key == "transpose_bilinear_G":
            continue
        assert val < 1e-12, f"{key}: {val:.3e}"


def test_F302_amplitude_law():
    """C4/C5 — the 2 (n.y)^2 law, and the Cartan form's flat amplitude 2."""
    rows, summary = m.amplitude_signature()
    assert summary["max_dev_transpose_from_2_ny_sq"] < 1e-12
    assert summary["max_dev_cartan_from_2"] < 1e-12
    assert summary["max_cartan_longitudinal"] < 1e-12
    assert summary["max_cartan_self_dot"] < 1e-12
    assert summary["hermitian_singlet_transverse_amp"] < 1e-20
    assert any(r["direction"] == "x_hat" and r["amp_transpose"] < 1e-20
               for r in rows)


def test_F302_no_live_sector_on_the_transpose_form():
    """C6 — the audit's negative result, which is the finding."""
    offenders = [a for a in m.sector_audit()
                 if a["form"] == "transpose" and "retired" not in a["sector"]]
    assert not offenders, ", ".join(a["sector"] for a in offenders)


def test_F302_gate():
    """The single entry point the registry record drives."""
    assert m.f302_bilinear_so3_check() is True
