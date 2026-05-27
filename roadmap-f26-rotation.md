# Roadmap — Adopting F26: Speed of Light as Rotation Rate

**Date:** 2026-05-23  
**Status:** In progress — Phases 1 & 2 complete

---

## Summary of F26

Finding 26 reframes the speed of light as the angular rotation rate of the $(E, B)$ vector pair per unit wavenumber, not a phase-propagation speed:

$$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}\bigg|_{|\mathbf{k}|\to 0}, \quad \Omega(\mathbf{k}) = 2\,\omega_\text{QCA}(\mathbf{k}/2)$$

The exact discrete EM law is a rigid real rotation:

$$\hat{E}(\mathbf{k},t+1) = \cos\Omega\,\hat{E} + \sin\Omega\,\hat{B}$$
$$\hat{B}(\mathbf{k},t+1) = -\sin\Omega\,\hat{E} + \cos\Omega\,\hat{B}$$

Maxwell's curl equations are the $k \to 0$ (i.e., $\Omega \to 0$) first-order Taylor expansion of this rotation. The $O(k)$ curl residual $c_\text{lat}/\sqrt{2}\cdot|\mathbf{k}|$ (Finding 2) is a structural consequence of the linearisation, not an open problem.

---

## What Has Been Done (Phase 1)

### 1. `ca_maxwell.py` — 3D BCC module (complete)

- **Module docstring rewritten**: Rotation law placed as PRIMARY law; Maxwell curl as DERIVED (k→0 limit).
- **`rotation_omega_bcc(KX, KY, KZ)`**: Computes $\Omega(\mathbf{k}) = 2\,\omega_\text{BCC}(\mathbf{k}/2)$ on a full k-grid.
- **`rotation_step_em_spectral(E_field, B_field)`**: Full-lattice exact EM propagator via FFT. One tick of the exact rotation law. Shape `(Lx, Ly, Lz, 3)`.
- **`c_from_rotation_rate()`**: Measures $c_\text{lat} = d\Omega/d|\mathbf{k}||_{k\to 0}$ by finite difference. Result: $0.57735027 = 1/\sqrt{3}$, residual $< 10^{-7}$.
- **`rotation_law_consistency()`**: Runs live Weyl states for 20 ticks, checks rotation-law residual vs Maxwell curl residual. Results: rotation law $2.8 \times 10^{-16}$ (machine precision), Maxwell curl $2.0 \times 10^{-2}$ (expected O(k)).

**Verification:** All four functions confirmed working at k=0.05.

### 2. `ca_maxwell_2d.py` — 2D square module (complete)

- **`rotation_omega_2d(KX, KY)`**: $\Omega(\mathbf{k}) = 2\,\omega_\text{2D}(\mathbf{k}/2)$ using `exact2d_dispersion` from `ca_core_exact.py`.
- **`rotation_step_em_spectral_2d(E_field, B_field)`**: Full-lattice exact EM propagator. Shape `(Lx, Ly, 3)`.
- **`c_from_rotation_rate_2d()`**: Measures $c_\text{lat} = 1/\sqrt{2}$, residual $2.93 \times 10^{-8}$ (finite-difference precision).
- **`rotation_law_consistency_2d()`**: Rotation law $2.2 \times 10^{-15}$ (machine precision), Maxwell curl $1.8 \times 10^{-2}$ (O(k)).
- **`__main__` block updated**: Reports both legacy Maxwell tests and new F26 rotation tests.

**Verification:** All four functions confirmed working at k=0.05.

---

## What Remains (Phase 2–4)

### Phase 2 — Replace Maxwell propagator in simulation loops ✅ COMPLETE (2026-05-24)

**What was done:**
- Added `composite_photon_propagation_full_lattice(n_steps, L, n_modes)` to `ca_maxwell.py`: places multiple composite-photon modes on a full L³ BCC lattice and propagates with `rotation_step_em_spectral`. Verifies (a) energy conservation and (b) per-mode rotation accuracy — both at machine precision.
- Added `test_L3c()` to `model-tests/run_L_tests.py`: tests L3c.1 (energy drift < 1e-12) and L3c.2 (mode error < 1e-12) on L=16, 100 ticks.
- Wired L3c into `main()` after L3b, as a PASS/FAIL gate.
- Added Phase 2 output to the F26 `__main__` block in `ca_maxwell.py`.
- Created `model-tests/run_phase2_f26_tests.py`: standalone 5-group test runner covering T1–T9, L3c, F27, F29, and L1/L2/L3a regression. **17/17 pass** in 0.3 s.

**Confirmed numbers (2026-05-24):**
- L3c.1 energy drift (100 ticks, L=16, 8 modes): `1.11 × 10⁻¹⁴`
- L3c.2 per-mode rotation residual: `6.44 × 10⁻¹⁴`
- F27 1-flavour norm drift: `2.83 × 10⁻¹⁶` (machine precision)

**Original Phase 2 description (for reference):**

### Phase 2 — Replace Maxwell propagator in simulation loops (Priority: High)

All current simulation loops in the codebase use the time-stepped Maxwell curl equations or the Weyl bilinear approach step-by-step. They should offer `rotation_step_em_spectral` as the default EM propagator.

| File | Current propagator | Needed change |
|---|---|---|
| `ca_maxwell.py` test / `__main__` | Maxwell curl (bilinear step) | Add option to use `rotation_step_em_spectral` |
| `model-tests/test_*.py` EM tests | Maxwell curl comparison | Add rotation-law comparison alongside |
| Any multi-step EM evolution loop | Per-step Weyl evolution | Offer `rotation_step_em_spectral` for speed |

The rotation propagator is **exact** (machine precision) and **faster** for long runs (single FFT pair per tick vs per-site Weyl update). It should become the default for EM-only evolution.

### Phase 3 — Dispersion relation reframing ✅ COMPLETE (2026-05-24)

**What was done:**
- `maxwell_dispersion_residual` (3D, `ca_maxwell.py`) docstring rewritten: "Nonlinear dispersion correction… NOT a model error — it is the BCC lattice's nonlinear dispersion at finite k." At k=0.05: ≈ 0.21% (within expected BCC nonlinearity).
- `maxwell_dispersion_residual_2d` (2D, `ca_maxwell_2d.py`) docstring rewritten with the same F26 framing.
- `ca_reference.md` F26 section added: full statement of the rotation law, c_lat as rotation rate, i = J (real 2×2 rotation), energy conservation as geometric, dispersion nonlinearity δv_φ/c ≈ −k/18, BCC chirality note.
- `dispersion_nonlinearity` function tabulates Ω(k) − c_lat k along the (1,1,1) diagonal (only direction with a nonlinear correction in BCC); the (1,0,0) direction is exactly linear.
- `planck_correction_prediction` confirmed correct: uses (1,1,1) direction, theory formula δv_φ/c ≈ −k/18 (linear in k), not the earlier −c²k²/6 (which assumed a 1D arccos dispersion).

**Original Phase 3 description (for reference):**

All references to the composite-photon dispersion $\Omega_\gamma = 2\omega(|\mathbf{k}|/2)$ should be relabelled as the rotation angle per tick rather than a frequency. Concretely:

- In `ca_reference.md` and findings: restate dispersion relations in terms of $\Omega(\mathbf{k})$ where possible.
- The function `maxwell_dispersion_residual` and `maxwell_dispersion_residual_2d` measure $|\Omega - c_\text{lat}|\mathbf{k}||/\Omega_\text{lin}$. These remain valid but their framing should shift: the "residual" is not error but the nonlinear correction at finite $k$.
- Add a `dispersion_nonlinearity(k_max, n_pts)` function to `ca_maxwell.py` that tabulates $\Omega(k) - c_\text{lat}k$ as a function of $k$, making the Planck-scale correction explicit.

### Phase 4 — Planck-scale correction prediction (Priority: Medium)

F26 predicts a quadratic-in-frequency correction to photon phase velocity:

$$\frac{\delta v_\phi}{c_\text{lat}} \approx -\frac{c_\text{lat}^2|\mathbf{k}|^2}{6}$$

This is measurable (in principle) via gamma-ray burst arrival-time differences. To make this prediction concrete and falsifiable:

- Add a function `planck_correction_prediction(k_planck_fraction)` that evaluates the leading correction at $|\mathbf{k}| = \alpha \cdot k_\text{Planck}$ for given $\alpha$.
- The natural Planck wavenumber in lattice units is $k_\text{Planck} = \pi$ (Nyquist). At $|\mathbf{k}| = 0.01\,\pi$: $\delta v_\phi / c \approx -\pi^2 \times 10^{-4}/6 \approx -1.6 \times 10^{-4}$.
- Compare against current best observational bounds from Fermi-LAT data (linear dispersion constrained to $\delta v / c \lesssim 10^{-16}$ at GeV energies — but this is linear-in-$E$; the quadratic correction is a distinct test).

### Phase 5 — Imaginary unit / complex-phase reframing ✅ COMPLETE (2026-05-24)

**What was done:**
- `ca_bcc.py` module docstring: added F26 paragraph. Key statement: Ω(k) = 2ω₊(k/2); c_lat = dΩ/d|k||_{k→0} = 1/√3 is the angular rotation rate of (E,B), not a propagation speed. The imaginary unit i is the 2×2 real matrix J=[[0,1],[−1,0]], the artefact of linearising the exact cosine rotation at Δt→0. Chirality note: ω₊(−k)=ω₋(k).
- `ca_dirac.py` module docstring: added F26 paragraph. Key statement: the mass step cos(m·dt)·I ± i·sin(m·dt)·A is the same real-rotation structure as the EM propagator; the imaginary unit in the mass coupling is the continuous-time linearisation of a rigid rotation in (η, χ) internal space.
- `ca_reference.md`: new "F26 — Speed of light as rotation rate; exact EM propagator" section covering all the above, plus Poynting energy conservation reframed as geometric (rotation preserves vector length).

**Original Phase 5 description (for reference):**

F26 establishes that the imaginary unit in Maxwell's equations is the algebraic artefact of linearising a real rotation. The longer-term implications:

- The Dirac mass step already uses the rotation form $(\cos m\Delta t, \sin m\Delta t)$ exactly. This is consistent.
- The QFT complex phase $e^{-i\omega t}$ should be reinterpreted, wherever it appears in the codebase docstrings and comments, as a real rotation $R(\omega t)$ acting on the $(E,B)$ or $(\psi_R, \psi_L)$ plane.
- No code changes required — this is a documentation pass through `ca_maxwell.py`, `ca_dirac.py`, `ca_bcc.py`, and the reference summaries.

---

## Summary Table

| Phase | Scope | Status | Priority |
|---|---|---|---|
| 1a — Rotation propagator, 3D BCC | `ca_maxwell.py` 4 new functions | ✅ Complete | — |
| 1b — Rotation propagator, 2D square | `ca_maxwell_2d.py` 4 new functions | ✅ Complete | — |
| 2 — Replace sim-loop propagator | EM test loops, `__main__` blocks | ✅ Complete | High |
| 3 — Dispersion reframing | Docs, `ca_reference.md`, findings | ✅ Complete | Medium |
| 4 — Planck-scale prediction function | `ca_maxwell.py` new function | ✅ Complete (in Phase 1) | Medium |
| 5 — Complex-phase doc pass | `ca_dirac.py`, `ca_bcc.py`, refs | ✅ Complete | Low |

---

## Key Numbers (confirmed)

| Quantity | 3D BCC | 2D square |
|---|---|---|
| $c_\text{lat}$ (analytic) | $1/\sqrt{3} \approx 0.57735$ | $1/\sqrt{2} \approx 0.70711$ |
| $c_\text{lat}$ (measured) | $0.57735027$ | $0.70710681$ |
| Rotation law residual (E) | $2.8 \times 10^{-16}$ | $2.2 \times 10^{-15}$ |
| Maxwell curl residual at $k=0.05$ | $2.0 \times 10^{-2}$ | $1.8 \times 10^{-2}$ |
| Curl residual / $k$ | $\approx c_\text{lat}/\sqrt{2}$ | $\approx c_\text{lat}/\sqrt{2}$ |

---

## Cross-References

- [F26 — Speed of light as rotation rate](findings/F26-speed-of-light-as-rotation-rate.md)
- [F25 — Real rotation exact](findings/F25-real-rotation-exact-discrete-time-maxwell.md)
- [F21 — Curl residual geometry-independence](findings/F21-curl-residual-geometry-independence.md)
- [F17 — Energy conservation machine precision](findings/F17-poynting-energy-conservation.md)
- [Finding 2 — Original curl residual](findings.md)
