"""Roadmap P2.1 — every FFT library must agree to the round-off floor.

`ca_fft` picks the fastest available of pyfftw / scipy.fft / numpy.fft. That
choice must never change a physics result. In a project whose product is a
`machine_precision` gate at 1e-12, "different libraries differ in the last
bits" is not a shrug — it is a number that has to be measured and held.

This is also the regression a future GPU backend (roadmap P2.4) has to pass, so
the tolerance here is the contract, not a convenience.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

try:
    import pytest
except ModuleNotFoundError:                                # pragma: no cover
    from test_constants_consistency import pytest         # type: ignore

from casim.numerics import fft as ca_fft
from casim.numerics import backends, chiral, linalg

# The FFT round-off floor. The fft module's own docstring puts it at ~5e-14 at
# 64^3 and ~7e-14 at 320^3 for complex128; 1e-12 is the machine_precision
# marker's bar and leaves headroom without being slack.
FLOOR = 1e-12

# `np.matmul` (BLAS zgemm) and `np.einsum` sum in different orders, so they are
# NOT bit-identical. Measured on complex128 3x3 stacks: ~9e-16 absolute, ~4e-16
# relative, i.e. 1-2 ULP, and `optimize=True` does not close it. Four orders
# under FLOOR, so it cannot move a gate — but it is a real difference and the
# contract states it as a bound rather than pretending to equality.
MATMUL_ULP = 1e-14


def _available() -> list[str]:
    """Every *library* FFT backend present.

    C1 unified the two seams, so this reads the registry rather than poking
    `ca_fft._scipy_fft` / `._pyfftw_fft`, which no longer exist. Device
    backends (cupy, mlx) are excluded: cupy is not bit-comparable on a machine
    without a GPU, and mlx is float32 and cannot meet FLOOR by construction.
    """
    return [n for n in backends.available()
            if n in ("numpy", "scipy", "pyfftw")]


def _sample(L: int = 24, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return (rng.standard_normal((L, L, L))
            + 1j * rng.standard_normal((L, L, L))).astype(np.complex128)


@pytest.mark.machine_precision
def test_backends_agree_to_the_round_off_floor():
    names = _available()
    if len(names) < 2:
        pytest.skip(f"only one FFT backend available ({names[0]}); nothing to "
                    f"cross-check. Install scipy and/or pyfftw.")

    a = _sample()
    original = ca_fft.get_backend()
    results = {}
    try:
        for name in names:
            ca_fft.set_backend(name)
            results[name] = ca_fft.fftn(a)
    finally:
        ca_fft.set_backend(original)

    ref_name = "numpy"
    ref = results[ref_name]
    scale = float(np.max(np.abs(ref)))
    for name, out in results.items():
        if name == ref_name:
            continue
        delta = float(np.max(np.abs(out - ref))) / scale
        assert delta < FLOOR, (
            f"{name} disagrees with {ref_name} by {delta:.3e} (relative), above "
            f"the {FLOOR:.0e} floor. A backend that changes results is not a "
            f"backend, it is a different theory.")


@pytest.mark.machine_precision
def test_roundtrip_is_the_identity_on_every_backend():
    a = _sample()
    original = ca_fft.get_backend()
    try:
        for name in _available():
            ca_fft.set_backend(name)
            back = ca_fft.ifftn(ca_fft.fftn(a))
            err = float(np.max(np.abs(back - a))) / float(np.max(np.abs(a)))
            assert err < FLOOR, f"{name}: ifftn(fftn(x)) != x, error {err:.3e}"
    finally:
        ca_fft.set_backend(original)


@pytest.mark.exact
def test_worker_count_does_not_change_results():
    """Threading must be invisible in the output.

    This is the specific thing P2.1 changed: `set_workers` was documented as
    applying to pyfftw but was never passed through, so the pyfftw path ran
    single-threaded. Now that it is wired, prove that wiring it did not buy
    speed at the cost of reproducibility.
    """
    a = _sample()
    original_backend, original_workers = ca_fft.get_backend(), ca_fft.get_workers()
    try:
        for name in _available():
            ca_fft.set_backend(name)
            ca_fft.set_workers(1)
            one = ca_fft.fftn(a)
            ca_fft.set_workers(-1)
            many = ca_fft.fftn(a)
            assert np.array_equal(one, many), (
                f"{name}: thread count changed the result. FFT decomposition "
                f"must not depend on the worker count.")
    finally:
        ca_fft.set_backend(original_backend)
        ca_fft.set_workers(original_workers)


@pytest.mark.exact
def test_backend_is_described_not_silent():
    """The fallback must announce itself. This is the P2.1 fix in one line."""
    d = ca_fft.describe()
    assert ca_fft.get_backend() in d
    if ca_fft.get_backend() != "pyfftw":
        assert "pyfftw" in d, ("a non-pyfftw backend must say so and say how to "
                               "get pyfftw — silent fallback is what P2.1 fixed")


# ---------------------------------------------------------------------------
# Roadmap C1.2 — the contract extended.
#
# Everything below is new surface the numerics façade introduced, and each
# check exists because the alternative is a silent wrong answer rather than a
# loud failure.
# ---------------------------------------------------------------------------

@pytest.mark.machine_precision
def test_rfftn_agrees_with_fftn_on_real_input():
    """`rfftn` must be the same transform, not merely a similar one.

    The E and B fields are real and have always paid a full complex transform.
    `rfftn` is ~2x cheaper because it stores only the non-redundant half
    spectrum — which means its OUTPUT SHAPE differs, and that is exactly how a
    substitution goes wrong quietly: the array still broadcasts, the norms
    still look plausible, and the high half of k-space is gone.
    """
    rng = np.random.default_rng(11)
    a = rng.standard_normal((16, 16, 16))
    original = ca_fft.get_backend()
    try:
        for name in _available():
            ca_fft.set_backend(name)
            half = ca_fft.rfftn(a)
            full = ca_fft.fftn(a)
            n_last = a.shape[-1] // 2 + 1
            assert half.shape == a.shape[:-1] + (n_last,), (
                f"{name}: rfftn shape {half.shape} is not the half-spectrum")
            err = float(np.max(np.abs(half - full[..., :n_last])))
            err /= float(np.max(np.abs(full)))
            assert err < FLOOR, f"{name}: rfftn != fftn half-spectrum ({err:.3e})"

            back = ca_fft.irfftn(half, s=a.shape)
            rt = float(np.max(np.abs(back - a))) / float(np.max(np.abs(a)))
            assert rt < FLOOR, f"{name}: irfftn(rfftn(x)) != x ({rt:.3e})"
    finally:
        ca_fft.set_backend(original)


@pytest.mark.machine_precision
def test_batched_matmul_matches_einsum_within_one_ulp():
    """BLAS vs einsum: a measured bound, not an assumed equality.

    The first draft of `casim.numerics.linalg` claimed these were equal to the
    last bit. They are not — BLAS sums in a different order. The difference is
    ~1-2 ULP, four orders below FLOOR, so the substitution is safe; the point
    of this test is that the number is pinned, so a future backend that is
    sloppier gets caught.
    """
    rng = np.random.default_rng(3)
    for shape in ((64, 3, 3), (512, 3, 3), (8, 8, 8, 3, 3)):
        A = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
        B = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
        ref = np.einsum("...ij,...jk->...ik", A, B)
        got = linalg.batched_matmul(A, B)
        err = float(np.max(np.abs(got - ref))) / float(np.max(np.abs(ref)))
        assert err < MATMUL_ULP, (
            f"batched_matmul disagrees with einsum by {err:.3e} at {shape}, "
            f"above the {MATMUL_ULP:.0e} bound")
        assert got.shape == ref.shape


@pytest.mark.exact
def test_chiral_transform_preserves_both_components():
    """CLAUDE.md's specific hazard, as an assertion.

    "numpy or scipy on chiral transforms may ... drop the real or imaginary
    elements." A dropped component is invisible to a norm check when the
    dropped part was small, so it needs its own predicate rather than trusting
    an amplitude comparison.
    """
    rng = np.random.default_rng(5)
    shape = (8, 8, 8)

    def cplx():
        return rng.standard_normal(shape) + 1j * rng.standard_normal(shape)

    F, G = cplx(), cplx()
    # A genuine SU(2) mix: [[c, -conj(s)], [s, conj(c)]] with |c|^2+|s|^2 = 1.
    c, s = cplx(), cplx()
    nrm = np.sqrt(np.abs(c) ** 2 + np.abs(s) ** 2)
    c, s = c / nrm, s / nrm
    Fn, Gn = chiral.su2_apply(c, -np.conj(s), s, np.conj(c), F, G)

    assert chiral.components_preserved(F, Fn), "F lost a component"
    assert chiral.components_preserved(G, Gn), "G lost a component"

    # Unitary: the 2-spinor norm is invariant.
    before = float(np.sum(np.abs(F) ** 2 + np.abs(G) ** 2))
    after = float(np.sum(np.abs(Fn) ** 2 + np.abs(Gn) ** 2))
    assert abs(after - before) / before < FLOOR, (
        f"su2_apply is not norm-preserving: {before} -> {after}")

    # And the hand-rolled explicit-real product agrees with complex arithmetic.
    ar, ai, br, bi = F.real, F.imag, G.real, G.imag
    pr, pi = chiral.cmul(ar, ai, br, bi)
    ref = F * G
    err = float(np.max(np.abs((pr + 1j * pi) - ref))) / float(np.max(np.abs(ref)))
    assert err < FLOOR, f"cmul disagrees with complex multiply ({err:.3e})"


@pytest.mark.exact
def test_components_preserved_catches_a_dropped_imaginary_part():
    """The detector must actually detect. A predicate nobody has watched fail
    is a predicate nobody should trust — P0.5's rule, applied to a one-liner."""
    rng = np.random.default_rng(9)
    a = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    assert chiral.components_preserved(a, a.copy())
    assert not chiral.components_preserved(a, a.real.astype(complex)), (
        "components_preserved did not notice the imaginary part being dropped")


@pytest.mark.exact
def test_device_backends_are_registered_but_never_auto_selected():
    """A float32 backend must not be able to become active by accident.

    MLX is float32-backed: eps 1.2e-7, five orders above the 1e-12 gate. If it
    could be auto-selected on an Apple machine, every `machine_precision` claim
    in the project would quietly stop meaning anything.
    """
    assert backends.active_name() in ("numpy", "scipy", "pyfftw"), (
        f"a device backend ({backends.active_name()}) auto-selected; only "
        f"library backends may be chosen without an explicit opt-in")


def _run_standalone() -> int:
    checks = [
        ("backends_agree", test_backends_agree_to_the_round_off_floor),
        ("roundtrip_identity", test_roundtrip_is_the_identity_on_every_backend),
        ("workers_invisible", test_worker_count_does_not_change_results),
        ("backend_described", test_backend_is_described_not_silent),
        # C1.2
        ("rfftn_agrees", test_rfftn_agrees_with_fftn_on_real_input),
        ("matmul_within_ulp", test_batched_matmul_matches_einsum_within_one_ulp),
        ("chiral_preserves", test_chiral_transform_preserves_both_components),
        ("detector_detects",
         test_components_preserved_catches_a_dropped_imaginary_part),
        ("no_device_autoselect",
         test_device_backends_are_registered_but_never_auto_selected),
    ]
    failures = []
    for label, fn in checks:
        try:
            fn()
            print(f"PASS  {label}")
        except AssertionError as e:
            failures.append(f"{label}: {e}")
            print(f"FAIL  {label}")
        except Exception as e:                             # skip() from the shim
            print(f"SKIP  {label}: {e}")
    print(f"\n[fft] backend={ca_fft.describe()}")
    print(f"[fft] available={', '.join(_available())}")
    print(f"[fft] {len(checks) - len(failures)} PASS, {len(failures)} FAIL")
    for f in failures:
        print(f"  --- {f}")
    return 1 if failures else 0


if __name__ == "__main__":                                 # pragma: no cover
    sys.exit(_run_standalone())
