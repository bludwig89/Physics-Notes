"""Exactness/fidelity suite for the casim engine (roadmap Phase F).

Each test wraps one canonical check from ``casim.verify`` and carries the
matching pytest marker.  The same checks feed the auto-generated exactness
inventory (``casim inventory`` / conftest ``pytest_sessionfinish``), so the
inventory can never drift from what the tests actually assert.

Runs under pytest, or standalone:  PYTHONPATH=src python tests/test_casim_exactness.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import casim.verify as V  # noqa: E402

# pytest is optional: provide a no-op marker shim when it is absent.
try:
    import pytest
    mark = pytest.mark
except Exception:  # pragma: no cover
    class _M:
        def __getattr__(self, _):
            return lambda f: f
    mark = _M()


@mark.exact
def test_fidelity_photon_pair():
    assert V.fidelity_photon_pair().passed


@mark.exact
def test_fidelity_weyl_bcc():
    assert V.fidelity_weyl_bcc().passed


@mark.exact
def test_fidelity_w_chiral():
    assert V.fidelity_w_chiral().passed


@mark.exact
def test_fidelity_z_even():
    assert V.fidelity_z_even().passed


@mark.exact
def test_fidelity_gluon_bcc():
    assert V.fidelity_gluon_bcc().passed


@mark.exact
def test_unitarity_weyl():
    assert V.unitarity_weyl().passed


@mark.exact
def test_resume_roundtrip():
    assert V.resume_roundtrip().passed


@mark.exact
def test_fidelity_backreaction():
    assert V.fidelity_backreaction().passed


@mark.exact
def test_fidelity_beta_decay():
    assert V.fidelity_beta_decay().passed


@mark.exact
def test_fidelity_gauge_mc():
    assert V.fidelity_gauge_mc().passed


@mark.exact
def test_fidelity_refraction():
    c = V.fidelity_refraction()
    if c is None:
        try:
            import pytest
            pytest.skip("ca_curved / SciPy not available")
        except Exception:
            return
    assert c.passed


@mark.machine_precision
def test_charge_photon_continuity():
    assert V.charge_photon_continuity().passed


@mark.machine_precision
def test_norm_drift_weyl():
    assert V.norm_drift_weyl().passed


def test_gravity_deflection_vs_GR():
    assert V.gravity_deflection().passed


if __name__ == "__main__":
    checks = V.run_all()
    for c in checks:
        print(f"  {c.name:22s} {c.channel:18s} {c.exactness:18s} "
              f"{c.residual:.3e}  {'PASS' if c.passed else 'FAIL'}")
    n = sum(c.passed for c in checks)
    print(f"\n{n}/{len(checks)} checks pass")
    sys.exit(0 if n == len(checks) else 1)
