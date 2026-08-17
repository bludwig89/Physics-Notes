"""P2.7 — every device path is gated on precision, and the gate is asserted.

Why this file exists
--------------------
C1 gave the MLX backend a `CASIM_ALLOW_FLOAT32` gate and a test asserting no
device backend can self-activate. Both were correct and neither covered the JAX
path in `casim.engine.gauge.weak_wmu`, because that path is a fused `@jax.jit`
kernel rather than a registered FFT backend — so it sat outside the registry the
test guards *and* outside `audit_numerics.py`'s `np|numpy` regex. It ran the W
propagator in complex64 (float32 eps 1.2e-7, five orders above the `machine`
gate) with no gate and no test.

So the policy moved into `casim.numerics.precision`, which both kinds of path
now import, and this file asserts the policy rather than trusting it. The tests
that need a device library **skip** when it is absent — the honest state on a
Linux sandbox with no GPU — but the ones that matter here do not: the gate
itself is pure logic and is tested unconditionally.
"""
from __future__ import annotations

import pytest

from casim.numerics import backends, precision


# --------------------------------------------------------------------------
# The gate itself — no device library required
# --------------------------------------------------------------------------
@pytest.mark.exact
def test_require_float64_refuses_float32_by_default(monkeypatch):
    """A float32 path must raise unless it was explicitly accepted."""
    monkeypatch.delenv("CASIM_ALLOW_FLOAT32", raising=False)
    with pytest.raises(RuntimeError) as ei:
        precision.require_float64("probe", is_float64=False)
    msg = str(ei.value)
    # The message has to name the path and the two numbers, or it is a message
    # nobody can act on.
    assert "probe" in msg
    assert "1e-12" in msg or "1E-12" in msg
    assert "CASIM_ALLOW_FLOAT32" in msg


@pytest.mark.exact
def test_require_float64_passes_on_float64(monkeypatch):
    monkeypatch.delenv("CASIM_ALLOW_FLOAT32", raising=False)
    precision.require_float64("probe", is_float64=True)      # must not raise


@pytest.mark.exact
def test_require_float64_honours_explicit_acceptance(monkeypatch):
    """The escape hatch works, and it is an env var so it shows up in a log."""
    monkeypatch.setenv("CASIM_ALLOW_FLOAT32", "1")
    precision.require_float64("probe", is_float64=False)     # must not raise
    assert precision.allow_float32() is True


@pytest.mark.exact
def test_machine_gate_matches_the_baseline_engine():
    """The gate this module quotes must be the one baselines actually use.

    Two copies of 1e-12 that can drift apart would let a device path be
    measured against a different bar than the results are.
    """
    from casim.baselines import MACHINE_FLOOR
    assert precision.MACHINE_GATE == MACHINE_FLOOR


# --------------------------------------------------------------------------
# The JAX path — gated, and asserted to be gated
# --------------------------------------------------------------------------
@pytest.mark.exact
def test_jax_path_is_gated_not_merely_documented(monkeypatch):
    """`use_jax(True)` must go through the precision policy.

    Runs whether or not JAX is installed: with JAX absent it must raise the
    not-installed error, and with JAX present in float32 it must raise the
    precision error. What it must never do is quietly enable.
    """
    monkeypatch.delenv("CASIM_ALLOW_FLOAT32", raising=False)
    from casim.engine.gauge import weak_wmu as w

    rep = w.jax_precision_report()
    if not rep["available"]:
        with pytest.raises(RuntimeError, match="JAX not installed"):
            w.use_jax(True)
        return
    if not rep["x64"]:
        with pytest.raises(RuntimeError, match="float32"):
            w.use_jax(True)
    else:
        w.use_jax(True)
        try:
            assert w._USE_JAX is True
        finally:
            w.use_jax(False)
    assert w._USE_JAX is False


@pytest.mark.machine_precision
def test_jax_kernel_matches_the_numpy_kernel():
    """If the JAX path is usable, it must agree with numpy to the machine bound.

    This is the contract C1.2 holds every backend to, extended to the one device
    path that is a fused kernel rather than a transform supplier. Skips when JAX
    is absent — and that skip is the honest report, not a pass.
    """
    import numpy as np

    from casim.engine.gauge import weak_wmu as w

    rep = w.jax_precision_report()
    if not rep["available"]:
        pytest.skip("JAX not installed — the contract exists and is unexercised")
    if not rep["x64"]:
        pytest.skip("JAX present but float32; the gate refuses it (see above)")

    rng = np.random.default_rng(0)
    L = 8
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))

    w.use_jax(False)
    E_np, B_np = w.w_propagation_step_spectral(E.copy(), B.copy())
    try:
        w.use_jax(True)
        E_jx, B_jx = w.w_propagation_step_spectral(E.copy(), B.copy())
    finally:
        w.use_jax(False)

    for got, ref, nm in ((E_jx, E_np, "E"), (B_jx, B_np, "B")):
        denom = max(float(np.max(np.abs(ref))), 1e-300)
        rel = float(np.max(np.abs(got - ref))) / denom
        assert rel < precision.MACHINE_GATE, f"{nm}: rel {rel:.3e}"


# --------------------------------------------------------------------------
# The registry — no device backend may auto-select
# --------------------------------------------------------------------------
@pytest.mark.exact
def test_no_device_backend_is_active_by_default():
    """Restates C1's assertion, now that `jax` is a registered name too."""
    assert backends.active_name() not in ("mlx", "cupy", "jax"), (
        f"a device backend ({backends.active_name()}) auto-selected; device "
        f"backends are opt-in via CASIM_BACKEND and, for float32 ones, "
        f"CASIM_ALLOW_FLOAT32")


@pytest.mark.exact
def test_every_registered_device_backend_declares_its_precision():
    """A device backend's `describe()` must say if it is float32.

    P2.1's rule generalised: a fallback you can see is a choice, one you cannot
    is a bug. The same holds for a precision downgrade.
    """
    for name in ("mlx", "jax", "cupy"):
        b = backends._REGISTRY.get(name)
        if b is None:
            continue
        d = b.describe()
        assert d, f"{name} has no describe()"
        if "FLOAT32" in d.upper():
            assert "machine_precision" in d, (
                f"{name} declares float32 but does not say it is excluded "
                f"from machine_precision scenarios")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
