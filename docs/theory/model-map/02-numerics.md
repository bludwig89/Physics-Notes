# 02 — Numerics façade (`src/casim/numerics/`, decision D8)

**Scope.** Every file in `src/casim/numerics/`. This is the only place numpy, scipy and FFT libraries may be imported (D8). It is **plumbing**: it computes no physics. The one piece with a formula that matters for physics is `chiral` (the answer to the chiral-transform hazard), together with the FFT's sign and normalisation convention, which every spectral kernel inherits. This package is **not** in the engine module registry (it is the D8 package, outside `engine/`), so no registry `status`/`reach` line is given, and exactness is `n/a` unless stated.

**Conventions shared by the batch.**
- **FFT sign and normalisation.** Every wrapper forwards `norm` untouched. The default `norm=None` is numpy's `"backward"`:
  $$\hat f_{\mathbf k}=\sum_{\mathbf x}f_{\mathbf x}\,e^{-2\pi i\,\mathbf k\cdot\mathbf x/N}\ (\text{forward, unnormalised}),\qquad f_{\mathbf x}=\tfrac1N\sum_{\mathbf k}\hat f_{\mathbf k}\,e^{+2\pi i\,\mathbf k\cdot\mathbf x/N}\ (\text{inverse}).$$
  Spot-checked: `fft` of a unit impulse at $x=1$, $N=8$ gives $e^{-i\pi/4}$ at $k=1$. The scipy and pyfftw `numpy_fft` backends use the same convention.
- `fftfreq` and `rfftfreq` are numpy's, in **cycles per sample**, so the physical lattice wavenumber is $k=2\pi\cdot\texttt{fftfreq}(N)$.
- **Precision:** complex128 throughout. The `machine` gate is a relative $10^{-12}$; float32 ($\epsilon=1.19\times10^{-7}$) paths are refused unless `CASIM_ALLOW_FLOAT32=1`.
- **Units:** n/a.

**Modules covered:** `numerics/__init__.py`, `backends.py`, `benchmark.py`, `chiral.py`, `fft.py`, `lazy.py`, `linalg.py`, `precision.py`, `rng.py`.

---

### `numerics/__init__.py` — façade entry (plumbing)
**Status:** D8 package · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** Re-exports `fft, linalg, rng, chiral, backends`. It sets `xp = numpy` (`L50`), which is an honest alias with no dispatch yet. `describe()` (`L55`) names the active FFT backend. **Flags:** none.

---

### `numerics/backends.py` — FFT library/device registry (plumbing)
**Status:** D8 package · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** Holds a single backend registry. Each backend is an object exposing `fftn ifftn fft2 ifft2 fft ifft rfftn irfftn rfft irfft` plus `chiral_transform`.

- **Backends:**
  - `NumpyBackend` (`L122`): always available; the correctness anchor.
  - `ScipyBackend` (`L142`): passes `workers=nworkers()`.
  - `PyfftwBackend` (`L165`): passes `threads=nworkers()`. The plan cache is enabled with a 60 s keepalive (`L308-311`).
  - `CupyBackend`, `JaxBackend` and `MlxBackend` (`L222`, `L234`, `L270`): device round-trip via `_to`/`_from`. They are registered but never auto-selected.
- **Chiral:** `_Base.chiral_transform` (`L114`) **raises**. No backend implements it, so chiral work must go through `numerics.chiral` / `lattice.chiral_core`.
- **Discovery:** `_discover()` (`L294`) prefers pyfftw > scipy > numpy. `CASIM_BACKEND` overrides the choice, and on that path float32 MLX/JAX meet `precision.require_float64` (`L353-357`). JAX discovery enables `jax_enable_x64` process-wide and then checks the live dtype (`L336-341`).
- **Threads:** `nworkers()` (`L57`) parses as `(cpu_count or 1) if workers==-1 else max(1, workers)`, so `set_workers` works. Checked: after `set_workers(2)`, `nworkers()` returns 2.

**Flags:**
- ⚠ **DOC/CODE MISMATCH:** the float32 gate is only on the env-var path. `use("mlx")` (`L71`) and `fft.set_backend("mlx")` do not call `require_float64`. The `MlxBackend` docstring (`L276-278`) and CLAUDE.md both say MLX "refuses to activate unless `CASIM_ALLOW_FLOAT32=1`". The same gap exists for a non-x64 JAX backend.
- **Minor:** the docstring (`L16`) calls the protocol "seven methods (`fftn … ifft` + `chiral_transform`)", but `fft.py` also calls `rfftn/irfftn/rfft/irfft` on every backend.

---

### `numerics/fft.py` — FFT surface (plumbing)
**Status:** D8 package · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** Thin dispatch to `backends.active()`, with the sign and normalisation convention given in the header.

| # | Primitive | What it computes | Where | Exactness |
|---|---|---|---|---|
| 1 | `fftn/ifftn/fft2/ifft2/fft/ifft` | Forward $e^{-2\pi i kx/N}$ unnormalised; inverse with $1/N$ (default `norm=None`) | `fft.py:L102-125` | machine (floor below) |
| 2 | `rfftn(a)` | Half-spectrum of a **real** array: last axis $N\to\lfloor N/2\rfloor+1$ (checked: (4,6,5)→(4,6,3)) | `fft.py:L137 rfftn()` | machine |
| 3 | `irfftn(a, s)` | Inverse of #2. If `s` is given without `axes`, it fills `axes = (-len(s), …, -1)`. Round trip checked at $4.4\times10^{-16}$ | `fft.py:L149-151 irfftn()` | machine |
| 4 | `rfft/irfft` | 1-D versions of #2 and #3 | `fft.py:L154-161` | machine |
| 5 | `fftfreq`, `rfftfreq` | `np.fft.fftfreq/rfftfreq` (cycles/sample; multiply by $2\pi$ for $k$) | `fft.py:L165-166` | exact |
| 6 | `fft_floor_estimate(shape)` | $\epsilon_\text{mach}\,\log_2N\,\sqrt N$, the absolute norm error of one forward+inverse round trip | `fft.py:L190` | n/a |
| 7 | `memory_estimate` | $\prod(\text{shape})\cdot n_\text{fields}\cdot$ itemsize | `fft.py:L178` | n/a |

Also here: `get/set_backend`, `set/get_workers`, `describe`, `info` (L54-96).

**Flags:**
- ⚠ **DOC/CODE MISMATCH:** the module docstring (`L22-24`) says the per-FFT floor is "~eps × log2(N)", about $5\times10^{-14}$ for $64^3$. The function (#6) returns $\epsilon\log_2N\sqrt N=2.05\times10^{-12}$ for $64^3$, and the docstring's own formula gives $4.0\times10^{-15}$. Neither matches the quoted $5\times10^{-14}$.
- **Stale docstring:** `L3-4` says "a deprecation shim remains at the old path until C9", but C9 has already deleted the shims.

---

### `numerics/chiral.py` — explicit-real-pair chiral primitives (chiral-hazard answer)
**Status:** D8 package · **Findings:** (F134 via `lattice/chiral_core.py`) · **Lattice:** n/a · **Law:** n/a (arithmetic under both even and chiral laws) · **Units:** n/a

**Does:** Provides the two arithmetic primitives a chiral transform is built from. Every complex product is formed on explicit (re, im) real arrays, with no complex dtype inside the product and no `np.linalg`. The physics (the BCC Weyl $U^\pm(\mathbf k)=u\,I-i\,\mathbf n\cdot\boldsymbol\sigma$ and the W± Riemann–Silberstein branch rotation) lives in `src/casim/lattice/chiral_core.py` (see 03-lattice.md / 05b gauge).

| # | Equation | What it does | Where | Exactness |
|---|---|---|---|---|
| 1 | $(a_r+ia_i)(b_r+ib_i)=(a_rb_r-a_ib_i)+i(a_rb_i+a_ib_r)$ | `cmul(ar, ai, br, bi)` returns the (real, imag) pair | `chiral.py:L31 cmul()` | exact (float arithmetic, 1 rounding per op) |
| 2 | $\begin{pmatrix}F'\\G'\end{pmatrix}=\begin{pmatrix}U_{ff}&U_{fg}\\U_{gf}&U_{gg}\end{pmatrix}\begin{pmatrix}F\\G\end{pmatrix}$ | `su2_apply`: splits complex inputs into `.real`/`.imag`, forms four `cmul`s, and reassembles $F'=(a_{1r}+a_{2r})+i(a_{1i}+a_{2i})$ and $G'$ likewise | `chiral.py:L47-48 su2_apply()` | exact (as #1) |
| 3 | "both components survive": if $\max\lvert\operatorname{Re}\,\text{before}\rvert>\text{tol}$ then the same holds for after, and likewise for Im | `components_preserved()`, the predicate for the drop-a-component failure | `chiral.py:L60-66` | n/a |

**Notes.** The inputs arrive as complex arrays and the output is complex. Only the *products* are on explicit real pairs. `su2_apply` does not check unitarity of $U$. **Flags:** none.

---

### `numerics/linalg.py` — dense/optional-scipy linear algebra (plumbing)
**Status:** D8 package · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

| # | Primitive | What it computes | Where | Exactness |
|---|---|---|---|---|
| 1 | `batched_matmul(a,b)` | $C_{\dots ik}=\sum_jA_{\dots ij}B_{\dots jk}$ via `np.matmul` (BLAS `zgemm`). Drop-in for `einsum('...ij,...jk->...ik')`. **Not bit-identical**: 1–2 ULP (~$9\times10^{-16}$ abs), bounded in `tests/casim/test_fft_backend_equivalence.py` | `linalg.py:L60` | machine |
| 2 | `dagger(a)` | $A^\dagger=\overline{A}^{\,T}$ on the trailing two axes | `linalg.py:L65` | exact |
| 3 | `eigh, eigh_tridiagonal, eigsh, brentq, sparse` | Pass through to scipy after `require_scipy(name)`, which raises a named-caller error if scipy is missing | `linalg.py:L86-124` | n/a |

**Flags:** none.

---

### `numerics/rng.py` — per-consumer seeded streams (plumbing)
**Status:** D8 package · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:**
- `for_channel(name)` (`L55`) returns `default_rng(SeedSequence(entropy=run_seed, spawn_key=(blake2b_64(name),)))`. It is cached per name and stable across processes (salted `hash()` is avoided, `L44-52`).
- `seed_run(s)` (`L33`) resets the seed and clears the cache. The default seed is 0.
- `spawn(n)` (`L67`) uses `SeedSequence(seed).spawn(n)`. That is **stateful**: successive calls return different children until the next `seed_run`.
- `default()` returns the shared `"__default__"` stream.

**Flags:** none (the `simulation.py:108` "one global RNG" remark in the docstring is historical context).

---

### `numerics/precision.py` — float32 policy (plumbing)
**Status:** D8 package · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:**
- `MACHINE_GATE = 1e-12` (`L44`) mirrors `casim.baselines.MACHINE_FLOOR`.
- `FLOAT32_EPS = 1.1920929e-07` (`L47`).
- `require_float64(name, is_float64)` (`L55`) raises unless the path is float64 or `CASIM_ALLOW_FLOAT32=1`.
- `float32_note()` produces the `describe()` disclosure.

**Flags:** see the backends.py mismatch: this gate is called only from `_discover()`'s env path.

---

### `numerics/lazy.py` — per-cell tick counter for emergent-time work (bookkeeping)
**Status:** D8 package (used by `casim.lattice.__init__` and the emergent-time T1/T5/Shapiro tests) · **Findings:** emergent-time plan T1/T5 · **Lattice:** any · **Law:** n/a · **Units:** ticks

**Does:** Wraps any propagator and counts, per cell, the ticks on which the state changed by more than $\varepsilon$. It is bookkeeping only: the propagator still updates every cell.

| # | Equation | What it does | Where | Exactness |
|---|---|---|---|---|
| 1 | $r(\mathbf x)=\sqrt{\sum_i\lvert\psi_i^\text{post}(\mathbf x)-\psi_i^\text{pre}(\mathbf x)\rvert^2}$ (computed as $\sum(d_r^2+d_i^2)$, keeping both components) | per-cell residual | `lazy.py:L138-139 per_cell_residual_multi()` | exact |
| 2 | $N(\mathbf x)\mathrel{+}=[\,r(\mathbf x)>\varepsilon\,]$, $\varepsilon=10^{-13}$ default | tick increment | `lazy.py:L77,81 TickCounter.increment*()` | exact |
| 3 | $\tau(\mathbf x)=N(\mathbf x)\,\tau_0$ | proper time | `lazy.py:L88 proper_time()` | exact |
| 4 | $\max\lvert\psi_\text{sync}-\psi_\text{lazy}\rvert$ (must be 0: the lazy step never skips the propagator) | sync-vs-lazy regression | `lazy.py:L255-256 sync_vs_lazy_residual()` | exact (bit-for-bit expected) |
| 5 | $\psi'=\text{where}(\text{vacuum},\psi,\text{kick}(\psi))$ | position-space-only lazy kick | `lazy.py:L289` | exact |

**Flags:**
- **OTHER:** the docstring calls the module `ca_lazy.py` (stale name).
- **OTHER:** it imports `numpy` directly (allowed inside `numerics/`) and is emergent-time physics bookkeeping rather than a numerics primitive.

---

### `numerics/benchmark.py` — W-propagation timing script (plumbing, not a library)
**Status:** D8 package · **Findings:** — · **Lattice:** BCC (via `weak_wmu`) · **Law:** chiral (the W± step, F91) · **Units:** lattice

**Does:** Times three versions of the W± step at $L\in\{32,64\}$: a reconstructed per-component loop, the batched numpy `weak_wmu.w_propagation_step_chiral`, and the JAX JIT path. The reference loop's chiral step (`L41-46`) is:
$$F^\pm=\hat E\pm i\hat B,\quad F^+\to e^{-i\Omega^+}F^+,\ F^-\to e^{+i\Omega^-}F^-,\quad E=\operatorname{Re}\,\mathcal F^{-1}\tfrac12(F^++F^-),\ B=\operatorname{Re}\,\mathcal F^{-1}\bigl(-\tfrac i2\bigr)(F^+-F^-).$$
The reference massive loop (`L102-109`) uses $\Omega_\text{eff}=\sqrt{m_W^2+\Omega_\text{op}^2}$ with $\Omega_\text{op}=\omega^+_\text{BCC}(\mathbf k/2)+\omega^-_\text{BCC}(\mathbf k/2)$ and $m_W=0.3$ hard-coded. The real (E, B) rotation is $E'=\cos\Omega\,\hat E+\sin\Omega\,\hat B$, $B'=-\sin\Omega\,\hat E+\cos\Omega\,\hat B$. The canonical versions of these laws are mapped in the gauge section (05b, `weak_wmu.py`). Exactness: unknown (timing only).

**Flags:**
- **OTHER:** the whole benchmark runs at **import** (top-level code, no `__main__` guard, `L60-127`). Any package walk (pkgutil, coverage, `casim index`) that imports `casim.numerics.benchmark` would run minutes of FFTs.
- **OTHER:** it inserts its own directory into `sys.path` (`L12`), and its docstring names it `benchmark_jax.py` (stale).
- **OTHER:** `m_W=0.3` is an unregistered literal (a benchmark parameter, not physics).
