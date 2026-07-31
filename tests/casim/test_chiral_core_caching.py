"""Roadmap C1.4 — the chiral-core mode caches must be free.

`weyl_step` rebuilt `make_kgrid_3d` AND the full 2x2 unitary on every call;
`_chiral_branch_rates` rebuilt the k-grid, both dispersion branches, the
Nyquist mask and four transcendental tables on every call. `ca_bcc` has had
`_weyl_cache` and `ca_wmu` `_disp_cache` all along, so this was a regression
against the very kernels the module mirrors.

A cache is only free if it cannot change an answer. Three things are asserted:

  1. a cached call equals an uncached one **exactly** — the cache is a memo,
     not an approximation;
  2. repeated calls are identical, so nothing accumulates;
  3. the cached arrays are **read-only**, so a caller that mutates one gets a
     loud `ValueError` instead of silently corrupting every later tick.

Plus the honest accuracy bound against the audited kernels, which is a few ULP
and NOT bit-for-bit — the claim this module carried until C1.4.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
for _p in (os.path.join(_REPO, "src"), os.path.join(_REPO, "ca-simulation")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    import pytest
except ModuleNotFoundError:                                # pragma: no cover
    from test_constants_consistency import pytest          # type: ignore

from casim.lattice import chiral_core as cc

# Measured at L=32 (see the chiral_core module docstring). Explicit-real
# arithmetic associates differently from numpy's complex multiply.
ULP_BOUND = 1e-14


def _fields(L: int = 16):
    rg = np.random.default_rng(0)
    f = rg.standard_normal((L, L, L)) + 1j * rg.standard_normal((L, L, L))
    g = rg.standard_normal((L, L, L)) + 1j * rg.standard_normal((L, L, L))
    E = rg.standard_normal((3, L, L, L))
    B = rg.standard_normal((3, L, L, L))
    return f, g, E, B


@pytest.mark.exact
def test_cache_is_a_memo_not_an_approximation():
    f, g, E, B = _fields()

    cc.clear_caches()
    cold_f, cold_g = cc.weyl_step(f, g, sign="+")
    warm_f, warm_g = cc.weyl_step(f, g, sign="+")
    assert np.array_equal(cold_f, warm_f) and np.array_equal(cold_g, warm_g), (
        "weyl_step changed once its unitary came from the cache")

    cc.clear_caches()
    cold_E, cold_B = cc.chiral_rs_step(E, B)
    warm_E, warm_B = cc.chiral_rs_step(E, B)
    assert np.array_equal(cold_E, warm_E) and np.array_equal(cold_B, warm_B), (
        "chiral_rs_step changed once its rate tables came from the cache")


@pytest.mark.exact
def test_cached_arrays_are_read_only():
    f, g, _, _ = _fields()
    cc.clear_caches()
    cc.weyl_step(f, g, sign="+")
    assert cc._weyl_cache, "nothing was cached"
    for key, arrays in cc._weyl_cache.items():
        for a in arrays:
            with pytest.raises(ValueError):
                a[(0,) * a.ndim] = 0
            assert not a.flags.writeable


@pytest.mark.exact
def test_cache_keys_separate_geometries():
    """Two shapes, two signs and two block factors must not share an entry."""
    f16, g16, _, _ = _fields(16)
    f8, g8, _, _ = _fields(8)
    cc.clear_caches()
    cc.weyl_step(f16, g16, sign="+")
    cc.weyl_step(f16, g16, sign="-")
    cc.weyl_step(f8, g8, sign="+")
    cc.weyl_step(f16, g16, sign="+", block=2)
    assert len(cc._weyl_cache) == 4, (
        f"expected 4 distinct cache entries, got {len(cc._weyl_cache)} — a key "
        f"collision would serve one geometry's unitary to another")


@pytest.mark.machine_precision
def test_agreement_with_the_audited_kernels_is_a_few_ulp():
    """The honest bound. This module claimed 'bit-for-bit' until C1.4; it is
    a few ULP, which is fine, but the number is what gets asserted."""
    import ca_bcc
    import ca_wmu

    f, g, E, B = _fields(16)
    cc.clear_caches()

    ref_f, ref_g = ca_bcc.weyl_step_3d_bcc(f, g, sign="+")
    got_f, got_g = cc.weyl_step(f, g, sign="+")
    scale = float(np.max(np.abs(ref_f)))
    err = float(np.max(np.abs(got_f - ref_f))) / scale
    assert err < ULP_BOUND, f"weyl_step drifted from ca_bcc: {err:.3e}"

    ref_E, ref_B = ca_wmu.w_propagation_step_chiral(E, B)
    got_E, got_B = cc.chiral_rs_step(E, B)
    scale = float(np.max(np.abs(ref_E)))
    err = float(np.max(np.abs(got_E - ref_E))) / scale
    assert err < ULP_BOUND, f"chiral_rs_step drifted from ca_wmu: {err:.3e}"


def _run_standalone() -> int:
    checks = [
        ("cache_is_a_memo", test_cache_is_a_memo_not_an_approximation),
        ("cached_read_only", test_cached_arrays_are_read_only),
        ("keys_separate", test_cache_keys_separate_geometries),
        ("ulp_agreement", test_agreement_with_the_audited_kernels_is_a_few_ulp),
    ]
    failures = []
    for label, fn in checks:
        try:
            fn()
            print(f"PASS  {label}")
        except AssertionError as e:
            failures.append(f"{label}: {e}")
            print(f"FAIL  {label}")
    print(f"\n[chiral cache] {len(checks) - len(failures)} PASS, "
          f"{len(failures)} FAIL")
    for f in failures:
        print(f"  --- {f}")
    return 1 if failures else 0


if __name__ == "__main__":                                 # pragma: no cover
    sys.exit(_run_standalone())
