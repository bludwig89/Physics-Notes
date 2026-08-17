# F134b — Phase 4 completion: chiral block-spin, a hand-rolled chiral core, the FFT floor

> **Renumbered F134b at roadmap C8.2 close-out (2026-07-31).** This file shared its number with another finding; the C8 audit found ten such collisions. The `b` suffix keeps the number findable — every existing citation of F134 still resolves — while making the two files distinguishable to tooling. See `docs/design/finding-numbers.yaml`.


`2026-06-11 - 06:20`

**Status.** Closes the remaining Phase-4 lines of
`docs/roadmaps/roadmap-scale-to-real-space.md` that F133 (even-law engine op)
left open. Modules `src/casim/engine/blockspin.py` (chiral/Weyl renormalised
steps), `src/casim/lattice/chiral_core.py` (hand-rolled core),
`src/casim/lattice/backend.py` (numpy_fft backend); tests
`tests/findings/test_F134_phase4_completion.py` (15/15 PASS).

---

## 1. What was open after F133

F133 made the block-spin transform $R_b$ a first-class engine operation, but the
**renormalised propagator** $\Omega(\kappa/b)$ was implemented only for the
even-law ($\gamma$) channel; the roadmap also lists a verified hand-rolled chiral
linear-algebra core, the FFT-floor characterisation, and GPU/distributed kernels.
F134 closes all but the GPU item (hardware, see §5).

## 2. Chiral + per-branch renormalised steps

The faithful coarse rule $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$ now
covers all three F91 propagator classes:

- **chiral W± (F37):** `renormalized_chiral_step` rotates the
  Riemann–Silberstein eigenstates $F^\pm=E\pm iB$ by their own branch rate
  $\Omega^\pm(\kappa/b)=2\omega_\pm(\kappa/2b)$, with the coarse-grid Nyquist
  bins set to the even average (real-field unitarity);
- **per-branch Weyl (BCC QCA):** `renormalized_weyl_step` applies the closed-form
  2×2 unitary $U^\pm(\kappa/b)=u\,I-i\,(n\cdot\sigma)$ to the spinor $(f,g)$.

Both **reduce bit-for-bit** to the audited fine kernels at $b=1$
(`ca_wmu.w_propagation_step_chiral`, `ca_bcc.weyl_step_3d_bcc`; residual $0.0$),
are **unitary** on the coarse lattice (norm drift $<10^{-13}$ over 100 ticks), and
are **dynamically faithful**: on band-limited fields

$$\big\|\,R_b\!\circ\!\text{step}^n_\text{fine}-\text{step}^n_\text{coarse}\!\circ\!R_b\,\big\|
= 1.5\times10^{-15}\ (\text{chiral}),\ 1.3\times10^{-15}\ (\text{Weyl}),$$

so the coarse run reproduces the fine IR dynamics for every channel. The
`WChiralChannel` and `WeylBCCChannel` engine channels switch to the renormalised
step automatically when `lattice.block > 1`.

(The single-branch chiral rate is birefringent — the F30 linear term is chiral —
so the *even-power* speed fit is not its right probe; faithfulness for the chiral
classes rests on the $b{=}1$ reduction, the $R_b$ commutation, and unitarity,
all machine-precision.)

## 3. A verified hand-rolled chiral core

`casim/lattice/chiral_core.py` is the from-scratch library the standing CLAUDE.md
caveat calls for ("if numpy/scipy drop the real or imaginary elements on chiral
transforms, write our own"). Every 2×2 mode mix is done on **explicit (re, im)
real pairs** via `cmul` / `su2_apply` — no `np.linalg`, no reliance on numpy's
complex dtype for the chiral algebra (only the FFT routes through the backend,
which is not the chiral-sensitive step). It provides `weyl_step` and
`chiral_rs_step` (both block-aware) and matches the audited kernels **bit-for-bit**
(weyl $9.9\times10^{-16}$, w_rs $1.3\times10^{-15}$), and its block-renormalised
form matches `blockspin` ($1.8\times10^{-15}$). It registers through the
`casim.lattice.backend` `chiral_transform` seam, so a future numba/GPU kernel
operating on plain real arrays is a drop-in.

## 4. The FFT floor + backend seam

**FFT floor.** The per-step relative norm drift of the spectral propagators is
$\sim10^{-16}$ (≈ 1 ulp of float64) and does **not** degrade as $L$ grows
(measured $L=8,16,32$ over 200 ticks, all $<10^{-14}$/step) — large-$L$ runs stay
at the round-off floor, the scale-invariance the GR/QM battery needs.

**Backend swap.** A second FFT backend (`numpy_fft`) is registered through the
seam and is identical to the default `ca_fft` to round-off
($\Delta<10^{-13}$), with `ifftn∘fftn = id`. This is the exact regression a
GPU/numba backend has to pass; the seam is therefore a validated swap point.

## 5. Honest limits

- **GPU / distributed kernels** are *not* built — they need hardware (cupy/numba
  absent in the sandbox). What F134 delivers is the **validated seam**: an
  independent backend passes the swap regression, so a GPU backend is a
  hardware-dependent drop-in, not a code-structure change.
- The renormalised chiral/Weyl steps are spectral (FFT) like the fine kernels;
  a *local-update* (stencil) kernel for huge $L$ is a separate optimisation.
- The hand-rolled core covers the two chiral spectral transforms (Weyl U±, W± RS);
  the massive-W / Z / gluon sectors reuse the even law (already F133-safe).

## 6. Files

- `src/casim/engine/blockspin.py` — `renormalized_chiral_step`,
  `renormalized_weyl_step` (+ `_renormalized_chiral_dispersions`).
- `src/casim/lattice/chiral_core.py` — `cmul`, `su2_apply`, `weyl_step`,
  `chiral_rs_step`, `ChiralCore` (+ `register`).
- `src/casim/lattice/backend.py` — `_NumpyFftBackend` (swap-validation backend).
- `src/casim/engine/channels.py` — block-aware `WChiralChannel` / `WeylBCCChannel`.
- `tests/findings/test_F134_phase4_completion.py` (15 tests, A–G).
- Exactness inventory rows #75–76.
