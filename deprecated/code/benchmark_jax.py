# ===== deprecated/code backup =====================================
# source     : ca-simulation/benchmark_jax.py
# migrated   : 2026-07-31 - 09:18
# target     : src/casim/numerics/benchmark.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: benchmark_jax.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
benchmark_jax.py — Compare propagation step performance:
  1. NumPy loop (original)
  2. NumPy batched (new default)
  3. JAX JIT (new optional)

Run: python3 benchmark_jax.py
"""

import numpy as np
import time, sys, os
sys.path.insert(0, os.path.dirname(__file__))

import ca_fft as _fft
from ca_wmu import (
    w_propagation_step_chiral,
    w_massive_propagation_step_spectral,
    _chiral_dispersions,
    _get_chiral_dispersions,
    _get_omega_even_cached,
    use_jax,
    _JAX_AVAILABLE,
)

WARMUP   = 5
REPEATS  = 50
SIZES    = [32, 64]

# ── Reference: original per-component loop (reconstructed) ───────────────────

def _chiral_loop_orig(E_W, B_W):
    """Exact copy of the old for-loop implementation for baseline timing."""
    import numpy as np
    shape = E_W.shape[1:]
    Op, Om = _chiral_dispersions(shape)          # no cache (original behaviour)
    E_new = np.zeros_like(E_W)
    B_new = np.zeros_like(B_W)
    for a in range(3):
        Ek = _fft.fftn(E_W[a])
        Bk = _fft.fftn(B_W[a])
        Fp = Ek + 1j * Bk
        Fm = Ek - 1j * Bk
        Fp_new = np.exp(-1j * Op) * Fp
        Fm_new = np.exp(+1j * Om) * Fm
        E_new[a] = _fft.ifftn((Fp_new + Fm_new) * 0.5).real
        B_new[a] = _fft.ifftn((Fp_new - Fm_new) * (-0.5j)).real
    return E_new, B_new


def bench(fn, E, B, warmup=WARMUP, repeats=REPEATS, extra_kw=None):
    kw = extra_kw or {}
    for _ in range(warmup):
        fn(E, B, **kw)
    t0 = time.perf_counter()
    for _ in range(repeats):
        fn(E, B, **kw)
    return (time.perf_counter() - t0) / repeats * 1e3   # ms per call


print(f"\n{'='*60}")
print(f"  W-field propagation benchmark  (n={REPEATS} reps after {WARMUP} warmup)")
print(f"  FFT backend: {_fft.get_backend()}")
print(f"  JAX available: {_JAX_AVAILABLE}")
print(f"{'='*60}\n")

for L in SIZES:
    rng = np.random.default_rng(0)
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))

    print(f"  L={L}  ({L**3 * 3 * 2 * 8 / 1e6:.0f} MB for E+B float64)")

    # 1. Original loop (no cache)
    t_orig = bench(_chiral_loop_orig, E, B)

    # 2. New batched numpy (cached dispersions, single fftn call)
    use_jax(False)
    t_batch = bench(w_propagation_step_chiral, E, B)

    print(f"    orig  loop  (no cache):  {t_orig:7.2f} ms")
    print(f"    numpy batched (cached):  {t_batch:7.2f} ms   {t_orig/t_batch:5.2f}× speedup")

    # 3. JAX JIT
    if _JAX_AVAILABLE:
        use_jax(True)
        # Trigger compilation (not counted in bench)
        w_propagation_step_chiral(E, B)
        t_jax = bench(w_propagation_step_chiral, E, B)
        use_jax(False)
        print(f"    JAX JIT (CPU):           {t_jax:7.2f} ms   {t_orig/t_jax:5.2f}× speedup vs orig")
    else:
        print("    JAX: not installed")

    # Massive step
    t_orig_m = bench(lambda e, b: None, E, B)   # dummy to avoid re-measuring
    # reconstruct orig massive (with loop)
    def _massive_loop_orig(E_W, B_W):
        shape = E_W.shape[1:]
        from ca_lattice import make_kgrid_3d
        from ca_bcc import bcc_dispersion
        KX, KY, KZ = make_kgrid_3d(*shape)
        op = bcc_dispersion(KX/2, KY/2, KZ/2, '+') + bcc_dispersion(KX/2, KY/2, KZ/2, '-')
        omega_eff = np.sqrt(0.3**2 + op**2)
        cos_e = np.cos(omega_eff); sin_e = np.sin(omega_eff)
        E_new = np.zeros_like(E_W); B_new = np.zeros_like(B_W)
        for a in range(3):
            Ek = _fft.fftn(E_W[a]); Bk = _fft.fftn(B_W[a])
            E_new[a] = _fft.ifftn(cos_e*Ek + sin_e*Bk).real
            B_new[a] = _fft.ifftn(-sin_e*Ek + cos_e*Bk).real
        return E_new, B_new

    t_mo = bench(_massive_loop_orig, E, B)
    use_jax(False)
    t_mb = bench(w_massive_propagation_step_spectral, E, B, extra_kw={'m_W': 0.3})
    print(f"    massive orig loop:        {t_mo:7.2f} ms")
    print(f"    massive batched (cached): {t_mb:7.2f} ms   {t_mo/t_mb:5.2f}× speedup")

    if _JAX_AVAILABLE:
        use_jax(True)
        w_massive_propagation_step_spectral(E, B, m_W=0.3)
        t_mj = bench(w_massive_propagation_step_spectral, E, B, extra_kw={'m_W': 0.3})
        use_jax(False)
        print(f"    massive JAX JIT (CPU):    {t_mj:7.2f} ms   {t_mo/t_mj:5.2f}× speedup vs orig")

    print()

print("Done.")
