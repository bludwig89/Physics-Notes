"""Backend seam (roadmap §8 / Phase G): default delegates to ca_fft, round-trips
exactly, and an alternative backend can be registered and selected."""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import numpy as np
from casim.lattice import backend


def test_default_is_ca_fft():
    assert backend.backend_name() == "ca_fft"
    assert "ca_fft" in backend.available()


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
    try:
        backend.use("numpy_direct")
        assert backend.backend_name() == "numpy_direct"
        a = np.random.default_rng(1).standard_normal((6, 6))
        assert np.allclose(backend.ifft2(backend.fft2(a)), a, atol=1e-12)
    finally:
        backend.use("ca_fft")
    assert backend.backend_name() == "ca_fft"


if __name__ == "__main__":
    test_default_is_ca_fft()
    test_roundtrip_matches_numpy()
    test_register_and_switch()
    print("backend seam: all checks passed")
