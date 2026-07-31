"""Backend seam (roadmap §8 / Phase G): the default round-trips exactly, and an
alternative backend can be registered and selected.

Updated at roadmap C1.1. `casim.lattice.backend` is now a shim onto
`casim.numerics.backends`, which unified the two competing seams — this object
registry, which no physics module imported, and `ca_fft`'s module-level string
switch, which every kernel used. A GPU backend registered in the former would
never have been reached by a kernel calling the latter.

The visible consequence, asserted below: `backend_name()` returns the LIBRARY
(`numpy`/`scipy`/`pyfftw`) rather than the constant `"ca_fft"`. That
indirection was precisely what made the seam decorative, so the test changed
with it rather than the name being kept alive to satisfy a test. `"ca_fft"`
remains registered as an alias.
"""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import numpy as np
from casim.lattice import backend


def test_default_is_a_named_library_backend():
    assert backend.backend_name() in ("numpy", "scipy", "pyfftw"), (
        "the default must be a real FFT library, not an indirection layer")
    assert "ca_fft" in backend.available(), "the legacy alias must still resolve"


def test_ca_fft_alias_delegates_to_the_active_library():
    """The alias must reach the ACTIVE library — which is not always numpy.

    Fixed at roadmap C7 (2026-07-30 - 19:10). This test asserted
    `array_equal(backend.fftn(a), np.fft.fftn(a))` — bit-identical agreement
    with numpy — and it was red on any machine where P2.1's `pyfftw` extra is
    actually installed. FFTW and numpy differ in the last bits by construction
    (`casim.cli backend --bench` prints that difference), so the old assertion
    tested "the alias resolves to numpy", which is the opposite of what its name
    claims and of what C1.1 built.

    Two claims instead, matching the project's own standards:
      * the alias is bit-identical to `casim.numerics.fft`, i.e. it really is
        the same object the kernels call — that one IS exact;
      * and it agrees with numpy to the `machine` class bound (1e-12), which is
        the honest cross-library statement (cf. `test_roundtrip_matches_numpy`).
    """
    from casim.numerics import fft as active

    rng = np.random.default_rng(1)
    a = rng.standard_normal((8, 8, 8)) + 1j * rng.standard_normal((8, 8, 8))
    live = backend.backend_name()
    try:
        backend.use("ca_fft")
        via_alias = backend.fftn(a)
        assert np.array_equal(via_alias, active.fftn(a)), (
            f"the ca_fft alias is not the live numerics façade "
            f"(active backend: {active.describe()})")
        assert np.allclose(via_alias, np.fft.fftn(a), rtol=0, atol=1e-12), (
            "the active library disagrees with numpy beyond the machine floor")
    finally:
        backend.use(live)


def test_roundtrip_matches_numpy():
    rng = np.random.default_rng(0)
    a = rng.standard_normal((8, 8, 8)) + 1j * rng.standard_normal((8, 8, 8))
    back = backend.ifftn(backend.fftn(a))
    assert np.allclose(back, a, atol=1e-12)
    # and the backend's fftn agrees with numpy's
    assert np.allclose(backend.fftn(a), np.fft.fftn(a), atol=1e-10)


def test_register_and_switch():
    class _NumpyBackend:
        name = "numpy_direct"
        def fftn(self, a, **kw):  return np.fft.fftn(a)
        def ifftn(self, a, **kw): return np.fft.ifftn(a)
        def fft2(self, a, **kw):  return np.fft.fft2(a)
        def ifft2(self, a, **kw): return np.fft.ifft2(a)
        def fft(self, a, **kw):   return np.fft.fft(a)
        def ifft(self, a, **kw):  return np.fft.ifft(a)

    backend.register_backend(_NumpyBackend())
    # Restore whatever was live, NOT a hard-coded "ca_fft". Since C1 unified the
    # two registries this global is shared with casim.numerics, so leaving the
    # legacy alias selected leaked into test_fft_backend_equivalence.py and
    # failed two of its checks from another file.
    live = backend.backend_name()
    try:
        backend.use("numpy_direct")
        assert backend.backend_name() == "numpy_direct"
        a = np.random.default_rng(1).standard_normal((6, 6))
        assert np.allclose(backend.ifft2(backend.fft2(a)), a, atol=1e-12)
    finally:
        backend.use(live)
    assert backend.backend_name() == live


if __name__ == "__main__":
    # C1 renamed test_default_is_ca_fft -> test_default_is_a_named_library_backend
    # when casim.numerics absorbed ca_fft, and this block kept calling the old
    # name — a NameError that only the standalone runner sees, because pytest
    # never executes __main__. Kept in sync deliberately: run_gate.py falls back
    # to these blocks whenever pytest is absent.
    test_default_is_a_named_library_backend()
    test_ca_fft_alias_delegates_to_the_active_library()
    test_roundtrip_matches_numpy()
    test_register_and_switch()
    print("backend seam: all checks passed")
