# 04 — Engine core (`src/casim/engine/core/`)

*Written 2026-09-28 - 10:00 (model-map part p04).*

**Scope.** Every `.py` under `src/casim/engine/core/`: the engine spine (`simulation`, `clock`, `graph`, `channel`, `observers`), the concrete core channels (`channels`, `coupled`, `tier3`, `spectral_matter`, `entanglement_register`), the block-spin RG op (`blockspin`), two standalone solvers that live here for historical reasons (`manybody`, `lpt_generator`), the Stage-5 photon–fermion gate (`photon_fermion_push`), and three `_viz_*` plotting helpers. The last section, **"Channel coupling order and data flow"**, documents the tick loop and every channel↔channel exchange in the engine, including the channels registered from `src/casim/particles/channel.py` (outside `engine/`, but it registers into the same channel registry and its channels are the main consumers of the bus).

**Shared conventions.**
- **Lattice.** Most spinor/gauge channels are BCC (canonical, D1): their kinetic steps call `lattice.bcc.bcc_dispersion` / `bcc_unitary` / `weyl_step_3d_bcc`. The FFT grids are plain $L^3$ arrays with $k_i = 2\pi\,\text{fftfreq}(L)$ (`lattice/geometry.py:L77 make_kgrid_3d()`), so "BCC" means the hop rule, not the array layout. `w_chiral`, `z_even`, `charge_photon`, `gauge_mc` and `refraction_2d` declare `topologies=("cubic",)`; `gauge_mc` is the 4-D simple-hypercubic Wilson action (reference, not the model lattice); `lpt_generator` is 4-D hypercubic Wilson perturbation theory.
- **Rotation law (F91).** Each channel declares `propagator` ∈ {even, chiral, per-branch, per-link, dielectric, monte-carlo, variable-c, spectral, non-rel, multigrid}. The even law is $\Omega_\text{even}(k)=\omega_+(k/2)+\omega_-(k/2)$ applied as the real rotation $E'_k=\cos\Omega\,E_k+\sin\Omega\,B_k$, $B'_k=-\sin\Omega\,E_k+\cos\Omega\,B_k$ (`gauge/photon.py:L105 photon_step_spectral()`, identical to `gauge/weak_wmu.py:L690-694 _f26_rotation_step()`). The chiral law rotates $F^\pm=E_k\pm iB_k$ by $e^{\mp i\Omega^\pm}$ with $\Omega^\pm=2\omega_\pm(k/2)$ (`gauge/weak_wmu.py:L912-917 w_propagation_step_chiral()`; `w_propagation_step_spectral` is an alias of it, `weak_wmu.py:L926`).
- **Units.** Lattice units throughout ($a=\tau=\hbar=1$). Exceptions: `spectral_matter` (MeV via the $f_\pi$ anchor), `manybody` (eV / MeV, atomic units internally).
- **Constants.** $c_\text{lat}=1/\sqrt3$ (F26, exact) is the default `LatticeSpec.c_lat`; $8\pi G/c^4\to$ `F106_COEFF_LATTICE` $=1$ exactly (F106, F178); $G_\text{lat}=1/(72\pi)$ (F79); $f_\pi$ anchor $=92.07$ MeV (external, F77/F123) and PDG target $92.4$ MeV (external, comparison only).
- **Energy convention (P3.5).** Gauge field energy is $U=\tfrac12\sum(E^2+B^2)$ (`channel.py:L43 field_energy()`); spinor channels' `energy()` is a probability norm $\sum|\psi|^2$, not an energy.
- **Exactness.** The module registry sets `exact` for `clock` and `graph`, `quantitative` for `lpt_generator`, and nothing for the other core modules, so their equations are `unknown` unless `docs/status/exactness-inventory.md` names the specific result (rows #73–76 for block-spin, the F212/F214/F217 rows for the entanglement channels).
- **D8 note.** Every core module except `photon_fermion_push` imports `numpy` directly (FFTs are routed through `casim.numerics.fft`, but array/linalg calls are not). This is recorded once in the flags file, not repeated per module.

**Modules covered (18):** `__init__`, `_viz_legacy`, `_viz_spinor_color`, `_viz_tick_heatmap`, `blockspin`, `channel`, `channels`, `clock`, `coupled`, `entanglement_register`, `graph`, `lpt_generator`, `manybody`, `observers`, `photon_fermion_push`, `simulation`, `spectral_matter`, `tier3`.

---

### `engine/core/__init__.py` — package docstring
Plumbing only: a docstring and `from __future__ import annotations`. Channel registration happens in `casim/engine/__init__.py:L14-19`, which imports `channels`, `coupled`, `tier3`, `spectral_matter`, `entanglement_register` and `casim.particles.channel` so that their `@register` decorators run.

### `engine/core/_viz_legacy.py` — matplotlib PNG helpers (Weyl CA stages)
**Status:** live · test-only · **Findings:** — · plumbing. It plots norm, CFL, density and reversibility curves to PNG files (`save_*` functions, L31–L270). It contains no physics.

### `engine/core/_viz_spinor_color.py` — Bloch-sphere → RGB colouring
**Status:** live · driven (15 ch) · **Findings:** — · plumbing. It maps a 2-spinor $(f,g)$ to a colour: $\theta=2\arctan(\lvert g\rvert/\lvert f\rvert)$, $\varphi=\arg g-\arg f$, hue from $\varphi$, lightness $(1+\cos\theta)/2$, saturation $\lvert\psi\rvert^2/\text{peak}$ (`spinor_to_rgb()`, L31). This is visual encoding, not physics.

### `engine/core/_viz_tick_heatmap.py` — emergent-time tick-counter heatmap
**Status:** live · package-only · **Findings:** — · plumbing. It renders viridis on $\log_{10}(1+N)$ of the per-cell tick field (`tick_heatmap()` L31, `tick_heatmap_with_phi()` L95).

---

### `engine/core/blockspin.py` — block-spin RG $R_b$ as an engine op
**Status:** live · driven (0 ch) · **Findings:** F130 F133 F134 · **Lattice:** BCC dispersion on an $L^3$ FFT grid (block average is cubic Kadanoff blocking) · **Law:** even / chiral / per-branch renormalised steps · **Units:** lattice

**Does:** It coarse-grains a channel state by $b^3\!\to\!1$ block averaging and provides the renormalised coarse propagators $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$, so a block-$b$ lattice keeps the fine physical dispersion.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\psi_\text{c}(X)=b^{-3}\sum_{x\in\text{block }X}\psi(x)$ over the trailing 3 axes, dtype preserved (complex safe) | Kadanoff block average | `blockspin.py:L62-63 block_average_field()` | machine (inventory #73: bit-identical to `block_average`) |
| 2 | Gravity state: $\varphi_\text{c}=R_b\varphi$, then $K_\text{c}=e^{-2\varphi_\text{c}/c^2}$ (never average $K$ directly), so $A\!\cdot\!B\equiv1$ is kept | log-correct dielectric coarse-graining (F130 T3b) | `blockspin.py:L98 block_state()` | machine (inventory #73: $AB-1<10^{-12}$) |
| 3 | $(E,B)_k\mapsto R\big(\Omega_\text{even}(k/b)\big)(E,B)_k$, with $\Omega_\text{even}(\kappa)=\omega_+(\kappa/2)+\omega_-(\kappa/2)$ | renormalised even step; reduces to `photon_step_spectral` at $b=1$ | `blockspin.py:L124-126 renormalized_even_step()` | machine (inventory #74, commutator $1.8\times10^{-15}$) |
| 4 | $\Omega^\pm_\text{c}=2\,\omega_\pm\!\big(k/(2b)\big)$; on the Nyquist planes of even-$L$ grids $\Omega^\pm\to\tfrac12(\Omega^++\Omega^-)$ | chiral branch rates at $\kappa/b$ with the unitarity fix | `blockspin.py:L139-150 _renormalized_chiral_dispersions()` | machine (inventory #75) |
| 5 | $F^\pm=E_k\pm iB_k$; $F^{+\prime}=e^{-i\Omega^+_\text{c}}F^+$, $F^{-\prime}=e^{+i\Omega^-_\text{c}}F^-$; $E'=\text{Re}\,\mathcal F^{-1}\tfrac12(F^{+\prime}+F^{-\prime})$, $B'=\text{Re}\,\mathcal F^{-1}\tfrac{-i}{2}(F^{+\prime}-F^{-\prime})$ | renormalised chiral (W±) step | `blockspin.py:L168-173 renormalized_chiral_step()` | machine (inventory #75, $b{=}1$ residual 0.0) |
| 6 | $\begin{pmatrix}F\\G\end{pmatrix}'=U^\pm_\text{BCC}(k/b)\begin{pmatrix}F\\G\end{pmatrix}$ (closed-form `bcc_unitary`, no `eig`) | renormalised per-branch Weyl step | `blockspin.py:L192-197 renormalized_weyl_step()` | machine (inventory #75, commutator $1.3\times10^{-15}$) |
| 7 | $L_\text{phys}=L\cdot b$, cells per super-cell $=b^{d}$, $c_\text{lat}$ carried unchanged (RG fixed point, F130 T1) | patch bookkeeping | `blockspin.py:L205, L210, L217-224 physical_L()/cell_factor()/patch_summary()` | unknown (inferred: exact (integer bookkeeping)) |

**Inputs → outputs:** a channel state dict and $b$ → a coarse state dict. $(E,B)$ or $(f,g)$ fine arrays → one coarse tick.  **Depends on:** `lattice.bcc.bcc_dispersion/bcc_unitary` (see 03-lattice.md § bcc.py), `gauge.weak_wmu._f26_rotation_step` (05b), `numerics.fft` (02).  **Flags:** Chiral hazard: rows 5–6 are complex spinor/RS transforms through `numerics.fft` with numpy `exp` and multiplication. Inventory #76 (F134-D) records bit-for-bit agreement with the hand-rolled `chiral_core`, and the step keeps `.real` only after an explicitly Hermitian-symmetric Nyquist fix. `block_state` averages every array whose last 3 axes are cubic. That includes non-field arrays such as `em_photon`'s `rho`/`A`, and those channels have no renormalised step (see flags).

---

### `engine/core/channel.py` — the `Channel` base class and the channel registry
**Status:** live · driven (0 ch) · **Findings:** F389 · **Lattice:** n/a · **Law:** declares `propagator` · **Units:** lattice

**Does:** Defines the uniform channel interface (`init_state`, `step(state, lattice, context, rng)`, `energy`), the bus hooks (`provides`/`consumes`), the unified stress-energy hooks (`energy_density`, `T_munu`), the gravity readback (`read_K`), the default block-spin hook, and the `type_name → class` registry.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $U=\tfrac12\big(\sum E^2+\sum B^2\big)$ summed over every axis, leading colour/component axes included | the engine's single gauge-field energy (P3.5) | `channel.py:L43 field_energy()` | unknown |
| 2 | $u(x)=\tfrac12(E^2+B^2)$ summed over leading axes, when the state has $E,B$ | default energy density (gauge) | `channel.py:L216 energy_density()` → `gravity.T00_field_energy` (`interactions/gravity.py:L278`) | unknown |
| 3 | $u(x)=\sqrt{A}\,m\,\lvert\Psi\rvert^2$ with $\sqrt A=1$ here (`T00_dirac_rest(f,g,0,0,m)`) for $(f,g)$ states; $u=m\lvert\psi\rvert^2$ for `psi`; `None` when no `mass`/`m` is configured | default energy density (matter rest leg, F106-E5) | `channel.py:L221, L223 energy_density()` | unknown |
| 4 | $T^{00}=u$; the $0i$ legs are absent (not zero) | stress-energy legs | `channel.py:L277-278 T_munu()` | unknown |
| 5 | $K=\texttt{context[gravity\_partner]["K"]}$; returns `None` if the partner is absent or $K\equiv1$ | gravity readback (P3.6) | `channel.py:L258-267 read_K()` | n/a (plumbing) |
| 6 | display density $\lvert f\rvert^2+\lvert g\rvert^2$, or $E^2+B^2$ summed over components, or $K-1$ | GUI volume | `channel.py:L305-314 density_field()` | n/a (plumbing) |

**Inputs → outputs:** interface only. `consumes()` (L143–190) returns config values under the keys `sources`, `couplings`, `source`, `partner`, `channel`, `matter`, `gauge`, `fermion`, `photon`, `w_field`. `provides()` (L133–141) returns `(self.name,)` only, and **no channel in the tree overrides either method** (checked by introspection of all 31 registered classes).  **Depends on:** `interactions.gravity` (07a), `core.blockspin`.  **Flags:** The `provides()` docstring describes named exchange quantities (`J_em`, `T00`, `A_mu`, …) that no channel publishes, so the "typed" bus resolves channel names only (see flags). The `step()` docstring still says "registration order", which the bus has superseded (P3.3).

---

### `engine/core/channels.py` — concrete free/pilot channels
**Status:** live · driven (0 ch) · **Findings:** F388 · **Lattice:** mixed (see per row) · **Law:** per channel · **Units:** lattice

**Does:** Thin wrappers over audited kernels for six channel types: `photon_pair`, `weyl_bcc`, `w_chiral`, `z_even`, `gluon_bcc` and `gravity_dielectric`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $(E,B)_k\mapsto R(\Omega_\text{pair}(k))(E,B)_k$, $\Omega_\text{pair}=\omega_+(k/2)+\omega_-(k/2)$ | `photon_pair` free step, even law (F67–F69, F91) | `channels.py:L110 PhotonPairChannel.step()` → `gauge/photon.py:L105-106` | unknown |
| 2 | block $b>1$: $R(\Omega_\text{pair}(k/b))$ | `photon_pair` on a coarse lattice | `channels.py:L107` → `blockspin.py:L124` | machine (inv. #74) |
| 3 | with a gravity partner: $\Omega_K(x,k)=\Omega_\text{pair}(k)/K(x)$, Strang-split about the mean of $1/K$, `n_sub`=`grav_n_sub` (default 4); raises `NotImplementedError` if also `block>1` | photon in the F64 dielectric (F271 k-resolved) | `channels.py:L98-100` → `gauge/photon.py:L202 photon_step_dielectric()` | unknown |
| 4 | $\max_k\big\lvert\Omega_\text{pair}(k)-[\omega_+(k/2)+\omega_-(k/2)]\big\rvert$ over 2000 random $k$ | F69 PP1 dispersion identity check | `channels.py:L121-126 dispersion_residual()` | unknown (identity by construction) |
| 5 | $(f,g)_k\mapsto U^\pm_\text{BCC}(k)(f,g)_k$; block $b$: $U^\pm(k/b)$ | `weyl_bcc` per-branch Weyl QCA | `channels.py:L152-155 WeylBCCChannel.step()` | unknown; $b>1$ machine (inv. #75) |
| 6 | $\max\lVert U^\dagger U-I\rVert$ over the $k$ grid | Weyl unitarity observable | `channels.py:L174 unitarity_residual()` | unknown |
| 7 | chiral RS step, $F^\pm\to e^{\mp i\Omega^\pm}F^\pm$ | `w_chiral` (F37; chiral forced, F91) | `channels.py:L206` → `weak_wmu.py:L912-917`; block: `blockspin.py:L168` | unknown |
| 8 | $R(\Omega)$ rotation of a scalar $(E_Z,B_Z)$ pair | `z_even` (vector part, even) | `channels.py:L233` → `gauge/weak_z.py:L379 z_propagation_step_spectral()` | unknown |
| 9 | even BCC rotation of the $(8,L,L,L)$ octet | `gluon_bcc` (even forced, F91) | `channels.py:L261` → `gauge/gluon.py:L167 gluon_rotation_step_spectral_bcc()` | unknown |
| 10 | init: $\rho$ = Gaussian mass $M,\sigma$; $\varphi=$ open-boundary Poisson$(\rho;G)$; $K=e^{-2\varphi/c^2}$ ($=e^{2GM/rc^2}$ for a point mass) | static F64 lens | `channels.py:L320-325 GravityDielectricChannel.init_state()` | unknown |
| 11 | $T^{00}=\sum_{s\in\text{sources}}w_s\,t_s$ with $t_s=$ `T00_dirac_rest` (massive Dirac, $m=w_s$), $w_s\lvert f\rvert^2+\lvert g\rvert^2$ (Weyl, colour-summed), $w_s\sum\lvert\cdot\rvert^2$ (doublet), or $w_s\,\tfrac12(E^2+B^2)$ (gauge) | F106 source assembly from the context | `channels.py:L335-358 _source_T00()` | unknown |
| 12 | $s=\kappa\,c^2 T^{00}/2$ with $\kappa$=`coupling` (default `F106_COEFF_LATTICE`$=1$) | $\nabla^2\ln K=-\kappa T^{00}$ rewritten for $\varphi$ | `channels.py:L371` → `interactions/gravity.py:L293 phi_source()` | unknown (inferred: exact (coefficient)) |
| 13 | $\varphi^{n+1}=2\varphi^n-\varphi^{n-1}+(c_g\,dt)^2(\nabla^2_\text{lat}\varphi^n-s)$, $\nabla^2_\text{lat}$ = 6-point cubic Laplacian | dynamic Φ leapfrog (D-EM8) | `channels.py:L372-373` → `gravity.py:L339-341 phi_wave_step()` | unknown |
| 14 | $K=e^{-2\varphi^{n+1}/c^2}$ | dielectric rebuild | `channels.py:L376 step()` | unknown |
| 15 | $\tfrac12\sum(\partial_t\varphi)^2+\tfrac12c_g^2\sum\lvert\nabla\varphi\rvert^2$ (dynamic) or $\sum(K-1)$ (static proxy) | channel energy | `channels.py:L385, L387 energy()` | unknown |
| 16 | $\Delta\theta_\text{meas}=\big\lvert\tfrac12[I(y_b{+}1)-I(y_b{-}1)]\big\rvert$, $I(y)=\sum_x 2\varphi/c^2$; compared to $\tfrac{4GM}{c^2b}\cdot\tfrac{X}{\sqrt{X^2+b^2}}$, $X=L/2$ | eikonal lens deflection vs GR | `channels.py:L428-436 observables()` | unknown |

**Inputs → outputs:** see the data-flow section. **Lattice:** `photon_pair` (cubic|bcc: an FFT array with the BCC symbol), `weyl_bcc`/`gluon_bcc` (bcc), `w_chiral`/`z_even` (cubic tag, BCC dispersion inside the kernels), `gravity_dielectric` (cubic|bcc; the Laplacian is the 6-point cubic stencil).  **Depends on:** 05a/05b/05c (photon, weak, gluon), 07a (gravity), 03 (bcc, poisson_open).  **Flags:** `gravity_dielectric`'s docstring gives the F106 law $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ as the field equation. **F178 reclassifies that law** as the static weak-field reduction of $G_{\mu\nu}=8\pi G T_{\mu\nu}$ (supersessions.yaml `S4-F178-full-stress-energy`), and the exponential $K$ is PPN-order only. The channel still implements the reclassified law. `photon_pair`'s dielectric path replaced the eikonal mix (SUPERSEDED by F271, `S10-F271-eikonal-dielectric-photon`). `w_chiral` and `z_even` ignore `lattice.block` (only `w_chiral` has a coarse rule), and `z_even`/`gluon_bcc` run the fine rule on a coarse lattice without a guard.

---

### `engine/core/clock.py` — the engine's physical clock (P3.2)
**Status:** live · driven (1 ch) · **Findings:** F268 · **Lattice:** n/a · **Law:** n/a · **Units:** lattice time

**Does:** It reconciles each channel's native step onto one global $\Delta t$ and decides how many times each channel is sub-cycled per engine tick.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $dt_\text{native}$ = config `dt` if present, else class attr (default 1.0; `None` = time-agnostic). A config `dt_max` may lower the ceiling but never raise it | per-channel timing spec | `clock.py:L211-228 _channel_timing_spec()` | exact (reg) |
| 2 | $\Delta t$ = `clock.dt` if given, else $\max_c dt_\text{native}(c)$ (the coarsest) | global step | `clock.py:L270-275 reconcile()` | exact (reg) |
| 3 | $n_c=\Delta t/dt_\text{native}(c)$ evaluated as `Fraction(str(x))` ratios; a non-integer ratio, $n<1$, $\Delta t>dt_\text{max}$, or $n>1$ on a non-subcyclable channel raises `ClockError` | exact sub-cycle count | `clock.py:L294-318 reconcile()` | exact (reg) |
| 4 | mode `auto` → `legacy` if any $n_c>1$, else `strict`. `legacy` forces $n_c=1$ and flags `desynchronised`, $dt_\text{eff}=dt_\text{native}$ | desync is recorded, not corrected | `clock.py:L320-332` | exact (reg) |
| 5 | $t=\text{tick}\cdot\Delta t$ | physical time | `clock.py:L156 Clock.time` | exact (reg) |

**Inputs → outputs:** channel list + scenario `clock:` block → `Clock` (with `n_sub(name)`).  **Depends on:** nothing.  **Flags:** Spot-check: `photon_pair(dt=0.1)` + `weyl_bcc` gives $\Delta t=1$, auto→legacy, photon `n_sub=1` and flagged desynchronised; under `strict`, photon `n_sub=10`. The engine therefore runs every desynchronised scenario (F268: 18/46) with some channels deliberately slow unless `clock.mode: strict` is set. Every registered class has `dt_native=1.0`; non-unit steps come only from config `dt` keys (`photon_sourced` 0.1, `charge_photon` 0.1, `nr_electron` 0.2, `gluon_sourced` 1.0, `gravity_dielectric` 1.0, …). Several channels read `dt` in `step()` too, so the same key sets both the clock ratio and the kernel's internal step.

---

### `engine/core/coupled.py` — Tier-2 sourced / back-reacting channels
**Status:** live · driven (0 ch) · **Findings:** F384 F385 F386 F387 F388 F389 F390 F392 F395 · **Lattice:** BCC (except `charge_photon`: cubic tag) · **Law:** per channel · **Units:** lattice

**Does:** It holds the two closed matter↔gauge loops (fermion↔W SU(2); fermion↔photon U(1)), the F87 charge→field curl channel and the F54 β-decay vertex channel. It also carries the F388/F389 gate entries.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\theta=\lvert A\rvert$, $s=\sin(\theta/2)/\theta$; $U_a=\cos(\theta/2)+i\,sA^3$, $U_b=-sA^2+i\,sA^1$, with $U=\begin{psmallmatrix}U_a&-\bar U_b\\U_b&\bar U_a\end{psmallmatrix}=\exp(iA^a\tau^a/2)$ | site-wise SU(2) exponential | `coupled.py:L51-57 su2_expmap()` | unknown (spot-check: $\lvert U_a\rvert^2+\lvert U_b\rvert^2-1=4\times10^{-16}$) |
| 2 | $\psi=e^{-r^2/2w^2}e^{ik_0\cdot x}/\lVert\cdot\rVert$ | normalised Gaussian packet | `coupled.py:L65-68 gaussian_packet()` | n/a (init) |
| 3 | $J^1=\text{Re}(\bar f_\nu f_e)$, $J^2=\text{Im}(\bar f_\nu f_e)$, $J^3=\tfrac12(\lvert f_\nu\rvert^2-\lvert f_e\rvert^2)$ (upper Weyl components only) | isospin current of the partner doublet | `coupled.py:L99` → `gauge/weak_wmu.py:L1849 fermion_isospin_current()` | unknown |
| 4 | $(E,B)\to$ chiral RS step; $E\mathrel{+}=g_\text{lat}J$; $A\mathrel{+}=E$ (the new $E$), $g_\text{lat}$ default 0.5 | `w_sourced` tick | `coupled.py:L100-103 WSourcedChannel.step()` | unknown |
| 5 | $U_\ell=\text{su2\_expmap}(\varepsilon A)$, the same for all 8 links; site-averaged covariant BCC Weyl step ($\varepsilon$ default 0.05) | `fermion_doublet` tick (O(a) site-average scheme) | `coupled.py:L135-140 FermionDoubletChannel.step()` → `weak_wmu.py:L273 covariant_weyl_step_3d_bcc()` | unknown |
| 6 | $J=\mathcal F^{-1}\big[i\,C(k)\times\hat A_\text{src}(k)\big]$ with $A_\text{src}$ a Gaussian blob, so $C\cdot J\equiv0$ | divergence-free static source for `charge_photon` | `coupled.py:L183-187 ChargePhotonChannel.init_state()` | unknown |
| 7 | transverse $(E,B)$ rotated by $\vartheta=dt\,\lvert C(k)\rvert$ (Maxwell curl with the BCC curl symbol $C$), then $E\mathrel{-}=dt\,J$; $dt$ default 0.1 | `charge_photon` tick (F87) | `coupled.py:L194` → `gauge/charge_coupling.py:L238-289 maxwell_curl_step()` | unknown |
| 8 | $\sum(E^2+B^2)$ (**no ½**) | `charge_photon` energy | `coupled.py:L198` | unknown |
| 9 | tick 1: `emit_w_minus` (d→u+W⁻ vertex, $g_\text{lat}=0.8$); later ticks: massive Proca spectral step with $m_W=0.6$ | `beta_decay` (F54) | `coupled.py:L240-246 BetaDecayChannel.step()` → `gauge/charged_current.py:L283, L78` | unknown |
| 10 | $\sum(E_W^2+B_W^2)$ (**no ½**) | `beta_decay` energy | `coupled.py:L252` | unknown |
| 11 | $J$ = `conserved_current(f,g)` (F384, purely $\hat C$-longitudinal) or `full_current` (F389, adds the Noether transverse part) | partner fermion current | `coupled.py:L407-412 EmPhotonChannel.step()` → `gauge/em_current.py:L168, L378` | unknown |
| 12 | $J=J_T+J_L$ with the $\hat C(k)$ projector; source $=J_T$ (or $J$ under the `use_naive_sourcing` control) | F387 split sourcing | `coupled.py:L413-414` → `gauge/em_photon_sourcing.py:L113` | unknown |
| 13 | $(E,B)\to R(\Omega_\text{pair})(E,B)$; $E\mathrel{+}=g_\text{lat}J_\text{source}$; $B$ unsourced | `em_photon` radiative sector | `coupled.py:L416-418` | unknown |
| 14 | $\rho\mathrel{+}=g_\text{lat}\,\text{Re}\,\mathcal F^{-1}[-i\,C\cdot\hat J]$ | charge continuity (F384) | `coupled.py:L434-437` | unknown |
| 15 | $\hat E_L=-i\,C\,\hat\rho/\lvert C\rvert^2$ (for $\lvert C\rvert^2>10^{-14}$), i.e. $iC\cdot E_L=\rho$ | algebraic Gauss-law Coulomb field (exposed, **not** fed back) | `coupled.py:L438-444` | unknown |
| 16 | $A$ = `solve_A_coulomb_3d(B)` (Coulomb-gauge $A$ solved fresh from $B$ each tick, not accumulated) | F386 potential for the fermion | `coupled.py:L446` → `gauge/charge_coupling.py:L315` | unknown |
| 17 | $(f,g)\to$ per-link U(1) covariant BCC Weyl step with $A$, charge $q$ | `fermion_em` tick (F385 fork a; norm not conserved) | `coupled.py:L490-491 FermionEmChannel.step()` → `gauge/minimal_coupling.py:L140 u1_link_weyl_step_3d_bcc()` | unknown |
| 18 | $\lVert iC\cdot B\rVert$ | no-monopole residual observable | `coupled.py:L454` → `em_photon_sourcing.iC_dot_B_norm` | unknown |

Gate entries (checklists, not new physics): `check_fermion_photon_backreaction()` L505–681 (F388: ordering contract `ordering_err<1e-10`, self-sourced $P_\text{field}\approx0$, seeded sustained push, norm drift $<0.5$, $\lVert iC\cdot B\rVert<10^{-8}$) and `check_radiative_current_backreaction()` L715–799 (F389: $\lVert\Delta P_\text{field}\rVert>10^{-8}$, recovered fraction in $(0.01,0.9)$, scaling ratios $\Delta P_m(2g)/\Delta P_m(g)\in(1.6,2.4)$ and $\Delta P_f\in(3.0,5.4)$). All of these are `quantitative` thresholds.

**Inputs → outputs:** see the data-flow section.  **Depends on:** 05b (weak_wmu, charged_current), 05a/05c (photon, charge_coupling, em_current, em_photon_sourcing, minimal_coupling), 03 (geometry).  **Flags:** (a) `charge_photon` and `beta_decay` still sum $E^2+B^2$ without the ½, which contradicts `channel.field_energy`'s P3.5 docstring saying the engine now has one convention. (b) `charge_photon` is labelled "paired photon (F69)", but its rotation rate is $\lvert C(k)\rvert$ (the curl symbol), not $\Omega_\text{pair}$. F387 treats these as different functions. (c) The source sign differs between channels: `charge_photon` uses $E\mathrel{-}=dt\,J$ (Ampère) while `w_sourced`/`em_photon`/`photon_sourced`/`gluon_sourced` use $E\mathrel{+}=gJ$. (d) Default partner names (`"fermion_doublet"` L96, `"w_sourced"` L132, `"fermion_em"` L389, `"em_photon"` L486) live in `step()`, not in config, so when a scenario omits the key the bus sees no edge.

---

### `engine/core/entanglement_register.py` — genuine $2^n$ registers and Fock-space channels
**Status:** live · driven (0 ch) · **Findings:** F212 F214 · **Lattice:** lattice-agnostic (the qubits are abstract cells) · **Law:** declared even / per-branch · **Units:** lattice ticks

**Does:** It runs genuinely entangled many-body states live in the engine: an exchange-gate register (F212/F214), gate-level circuits (F218), a second-quantised Hubbard chain (F217), a Fock-space algorithm channel (F220), and density-matrix error correction (F221). It also defines four observers.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\theta=J/4$, $J=\tfrac12\big(\sqrt{U^2+16t^2}-U\big)$, $U=2\arcsin m$, with $t(m)$ **measured** as the mean NN amplitude after one tick of the 2-D Dirac split-step; overridable by `theta_per_tick` | derived per-tick entangling angle | `entanglement_register.py:L76` → `interactions/qi_entanglement.py:L358-365, L337, L343, L316-331` | $J(t,U)$ exact-algebraic (inventory row 243); $\theta$ as a whole quantitative (row 245) |
| 2 | $U_\text{exch}(\theta)=e^{-i\theta\,\sigma_A\cdot\sigma_B}$ applied to pairs $(0,1),(1,2),\dots,(n{-}2,n{-}1)$ in sequence, once per tick | `entanglement_register` tick | `entanglement_register.py:L91-94 step()` → `qi_entanglement.py:L85-97` | unknown (inferred: machine (rows 240/242)) |
| 3 | $S_\text{cut}=-\text{Tr}\,\rho_A\ln\rho_A$; purity $\text{Tr}\rho_A^2$ with $\rho_A=MM^\dagger$ after the partial reshape | entropy/purity observables | `entanglement_register.py:L108-116 observables()` | unknown |
| 4 | one circuit layer per tick, `apply_layer(psi, prog[i], n)` | `quantum_circuit` | `entanglement_register.py:L166` | unknown |
| 5 | $\psi\mapsto V e^{-iw}V^\dagger\psi$, $H=V\,\text{diag}(w)V^\dagger$ the Jordan–Wigner Hubbard Hamiltonian $H(t(m),U(m))$ | `fermion_chain` tick: exact $e^{-iH\cdot1}$ | `entanglement_register.py:L254-255, L277` | unknown (inferred: quantitative+machine (row 248); gap identity exact (row 247)) |
| 6 | one Fock-space program layer per tick (`apply_program_fock`) | `fermion_algorithm` | `entanglement_register.py:L349` | unknown |
| 7 | $\rho\mapsto\sum_i K_i\rho K_i^\dagger$ on every qubit (Kraus), then optional stabiliser recovery; fidelity $\langle\psi_L\rvert\rho\lvert\psi_L\rangle$ | `error_correction` round | `entanglement_register.py:L481-484, L494` → `interactions/qi_noise` | unknown |

Observers here: `circuit_readout` (L189), `fermion_algorithm_readout` (L373), `fermion_entanglement` (L400), `error_correction_fidelity` (L506), `entanglement_entropy` (L529). All of them re-read channel `observables()` (plumbing). `block_spin` is a no-op for all five channels.

**Inputs → outputs:** config → state vector / density matrix. None of these channels reads `context`.  **Depends on:** `interactions.qi_entanglement`, `interactions.qi_noise` (07c), `particles.second_quant` (06a/b).  **Flags:** $t(m)$ is measured on the **2-D square** Dirac stepper (`dirac_step_2d_splitstep`), not the BCC 3-D kernel, while the channel is labelled lattice-agnostic (a convention question). `propagator="even"` on a qubit register is a label only; F91 classes do not apply.

---

### `engine/core/graph.py` — the typed exchange bus (P3.3)
**Status:** live · driven (1 ch) · **Findings:** F269 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** It resolves each channel's `consumes` names to producers, fails at build time on dangling names, finds strongly connected components (coupling cycles), and returns a stable topological order.

| # | Equation / rule | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | producer map $q\mapsto$ channel, over all `provides()`; a duplicate provider raises `BusError` | resolution | `graph.py:L240-251 build_graph()` | exact (reg) |
| 2 | consumes$(c)$ = declared `consumes()` ∪ {every string anywhere in `c.config` that equals another channel's name} | edge discovery (F269 fix) | `graph.py:L260-263`, `L173-212 _config_channel_refs()` | exact (reg) |
| 3 | edge dep→c for each resolved $q$; an unresolved $q$ raises `BusError` under `strict` (default), otherwise it is recorded in `unresolved` | dependency edges | `graph.py:L264-279` | exact (reg) |
| 4 | Tarjan SCC (iterative); each SCC is sorted by registration rank; Kahn over the condensation DAG, ties broken by the earliest member's rank | stable topological order | `graph.py:L118-170, L288-321` | exact (reg) |
| 5 | cycles = SCCs with >1 member; a self-loop is not reported | declared cycles | `graph.py:L326` | exact (reg) |

**Inputs → outputs:** channel list + `bus:` spec → `ChannelGraph(order, edges, cycles, cycle_scheme ∈ {gauss_seidel, jacobi})`.  **Flags:** Because no channel overrides `provides()`, every "quantity" is a channel name, and the keys actually read (`A`, `J_em`, `rho_em`, `J_colour`, `K`, `S`, `alpha`, `centroid_prev`) are never type-checked.

---

### `engine/core/lpt_generator.py` — Wilson-action Feynman-rule generator
**Status:** partial · standalone · **Findings:** F162 · **Lattice:** 4-D simple hypercubic (Wilson plaquette; reference, not BCC) · **Law:** n/a · **Units:** lattice

**Does:** It derives the lattice gluon vertices by expanding $U=e^{iA}$ inside $-\text{Tr}\,U_\text{plaq}$ and keeping multilinear terms, so the vertices are generated rather than hand-transcribed. It is consumed by `gauge.lpt_d1_action_consistent`, `lpt_bcc_vertex`, `lpt_selfenergy` and `colour_theta`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $T^a=\lambda^a/2$, $\text{Tr}\,T^aT^b=\delta^{ab}/2$ | SU(3) generators | `lpt_generator.py:L48-59` | quantitative (reg) (row read: exact) |
| 2 | $U_{\rho\sigma}(0)=U_\rho(0)U_\sigma(\hat\rho)U_\rho(\hat\sigma)^\dagger U_\sigma(0)^\dagger$ | plaquette link list | `lpt_generator.py:L83-90 _plaquette_links()` | quantitative (reg) (row read: exact) |
| 3 | each leg on a direction-$\rho$ link carries $\pm i\,e^{ik\cdot(s+\hat\rho/2)}M_i$ (midpoint convention); $U=\sum_m X^m/m!$ truncated to multilinear terms of degree $\le n$ | link expansion | `lpt_generator.py:L243-259 _link_expansion()` (vectorised: L129-146) | quantitative (reg) (row read: exact (finite algebra)) |
| 4 | $V_n=-\sum_{\rho\ne\sigma}\text{Tr}\,[U_{\rho\sigma}]_{\{1..n\}}$ (ordered planes ⇒ Re Tr) | $n$-point vertex | `lpt_generator.py:L277-288 vertex()`, `L212-233 vertex_vec()` | quantitative (reg) (row read: exact) |
| 5 | background split: $U=e^{iQ}e^{iB}$, $U^\dagger=e^{-iB}e^{-iQ}$ | background-field vertex ($bqq$) | `lpt_generator.py:L170-183, L186-209 vertex_bqq_vec()` | quantitative (reg) (row read: exact) |
| 6 | $\Gamma^{(0)}_{\mu\nu}(k)=\delta_{\mu\nu}\hat k^2-\hat k_\mu\hat k_\nu$, $\hat k_\mu=2\sin(k_\mu/2)$ | Wilson inverse propagator (the validation target) | `lpt_generator.py:L295, L312 khat()/wilson_quadratic_form()` | quantitative (reg) (row read: exact) |
| 7 | gate: generated $V_2(\mu,k;\nu,-k)=C\,\Gamma^{(0)}_{\mu\nu}$ with one constant $C$ | propagator gate | `lpt_generator.py:L315-340 validate_propagator()` | quantitative (reg) (row read: machine (spot-check: $C=1.000$, max dev $4.4\times10^{-16}$)) |
| 8 | $f^{abc}=\text{Re}[-2i\,\text{Tr}([T^a,T^b]T^c)]$ | structure constants | `lpt_generator.py:L353` | quantitative (reg) (row read: exact) |
| 9 | $V_3\to K f^{abc}[\delta_{\mu\nu}(p-q)_\rho+\delta_{\nu\rho}(q-r)_\mu+\delta_{\rho\mu}(r-p)_\nu]$ as $p,q\to0$ | 3-gluon continuum-limit gate (tol $2\times10^{-3}$) | `lpt_generator.py:L367-413 validate_3gluon()` | quantitative (reg) |
| 10 | $V_4$ non-trivial and Bose-symmetric under leg swaps | 4-gluon gate | `lpt_generator.py:L426-456 validate_4gluon()` | quantitative (reg) |

**Depends on:** numpy only.  **Flags:** The comment at L78–80 says the gauge field sits at the link's **base** site; the code (L243, L130) uses the **midpoint** $s+\hat\rho/2$ (⚠ DOC/CODE MISMATCH, cosmetic). The `validate_3gluon` statement string (L411) says "Bose-antisymmetric"; the code comment and check (L398–405) test symmetry $v_1-v_2=0$. The module docstring says the normalisation $1/(2g^2)$ is "fixed once by matching the propagator"; `vertex()` takes `normalise=1` and the gate finds $C=1$. F162 was superseded in part by F272 (`S11-F272-bgfield-refold-removed`), but that concerns `bgfield_loop`, not this generator.

---

### `engine/core/manybody.py` — Hartree SCF atoms and A-body variational nuclei
**Status:** live · driven (9 ch) · **Findings:** — (registry empty; inventory cites F157/F217) · **Lattice:** none (1-D radial grid / continuum Gaussians) · **Law:** n/a · **Units:** atomic units → eV; MeV/fm

**Does:** It holds the two continuum many-body solvers used by `particles.element` and the `element_atom` channel (Aufbau configuration). There is no lattice dynamics.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $-\tfrac12u''+\big[\tfrac{l(l+1)}{2r^2}+V\big]u=\varepsilon u$, 3-point FD, Dirichlet ends, dense `eigh`; $\sum u^2h=1$ | radial eigenproblem | `manybody.py:L55-61 _radial_eigen()` | unknown |
| 2 | $V_H(r)=Q_\text{in}(r)/r+\sum_{r'\ge r}\rho(r')/r'\,h$ | spherical Hartree potential | `manybody.py:L67-69 _hartree_potential()` | unknown |
| 3 | Madelung order; capacities $s,p,d,f=2,6,10,14$ | Aufbau filling | `manybody.py:L85-97 aufbau_configuration()` | unknown (inferred: exact (table)) |
| 4 | $V_\text{eff}=-Z/r+V_H[\rho_\text{tot}-u_o^2]$; mixing $u\leftarrow(1-0.4)u+0.4u_\text{new}$; converged when $\max\lvert\Delta\varepsilon\rvert<10^{-6}$ | Hartree SCF | `manybody.py:L160-178 electron_cloud_hartree()` | unknown |
| 5 | $E=\sum_o n_o\varepsilon_o-\tfrac12\sum_o n_o\langle u_o^2V_{H,o}\rangle$ | Hartree total energy | `manybody.py:L181-191` | unknown |
| 6 | $1\,\text{Ha}=m_ec^2\alpha^2$; IE $=-\varepsilon_\text{HOMO}$ (Koopmans) | unit conversion / ionisation | `manybody.py:L193, L202` | unknown |
| 7 | $\Delta E=-\dfrac{Z_\text{eff}^4\alpha^2}{2n^4}(C-\tfrac34)$, $Z_\text{eff}=n\sqrt{-2\varepsilon}$, $C=n$ ($l=0$) or $n/(l+\tfrac12)$ | scalar-relativistic shift (F125 operator) | `manybody.py:L121-123 _scalar_relativistic_shift_Ha()` | unknown |
| 8 | $E(b)=(A-1)\tfrac34\hbar^2c^2/(M_Nb^2)+\tfrac{A(A-1)}{2}\langle V_\text{cent}-V_0e^{-r^2/2R_0^2}\rangle_b$, $R_0=\hbar c/m_\pi$; pair density $(2\pi b^2)^{-3/2}e^{-r^2/2b^2}4\pi r^2$ | A-body variational energy | `manybody.py:L278-285 nuclear_binding_Abody()` | unknown |
| 9 | $V_0$ fixed by bisection so that $\min_bE_{A=2}=-E_b^\text{deut}$ (the model deuteron, `solve_deuteron` with σ+ω+core+tensor) | deuteron anchor | `manybody.py:L293-302`, `L236-245` | unknown (fit to the model's own deuteron) |

**Depends on:** `particles.nuclear` (06a/b).  **Flags:** It uses unregistered literals `M_E_MEV=0.51099895`, `ALPHA=1/137.035999084` (L81–82) and `omega_g2_4pi=5.39` (L242), which are CODATA/fit values that bypass the D7 constants registry. The `sys.path.insert(_HERE)` hack is at L42–44. The module docstring still calls it `ca_manybody.py`. Its `__main__` block (L318) prints only (no artifact write).

---

### `engine/core/observers.py` — diagnostics run on a tick cadence
**Status:** live · driven (0 ch) · **Findings:** — · **Lattice:** $L^3$ FFT grid · **Law:** n/a · **Units:** lattice

**Does:** It defines the observer base and registry and eight observers: `norm_conservation`, `energy_trace`, `total_energy`, `unitarity_residual`, `dispersion_fit`, `momentum`, `beam_track`, `field_snapshot` and `field_dump`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\delta_c=\lvert e_c(t)-e_c(0)\rvert/\lvert e_c(0)\rvert$ with $e_c$ = channel `energy()` | per-channel drift | `observers.py:L101-104 NormConservation.observe()` | unknown (inferred: declared machine-precision (unknown)) |
| 2 | $E_\text{tot}=\sum_c\sum_x\text{Re}\,u_c(x)$ over channels whose `energy_density` is not None; the others go to `missing` | global energy (P3.5) | `observers.py:L186-198 TotalEnergy.observe()` | unknown |
| 3 | drift class: `machine` if $<10^{-12}$, `tight` if $<10^{-9}$, else `quantitative` | classification | `observers.py:L213-217 summary()` | unknown (inferred: exact (rule)) |
| 4 | $P_\text{matter}=\tfrac1N\sum_{\text{keys}}\sum_k k\,\lvert\hat\psi(k)\rvert^2$ over the complex keys $f,g,f_\nu,f_e,g_\nu,g_e,\eta_{u,d},\chi_{u,d},f_u,f_d$ | lattice-translation Noether momentum $\langle-i\nabla\rangle$ | `observers.py:L401-410 Momentum.observe()` | unknown (inferred: declared exact (unknown)) |
| 5 | $P_\text{field}=\tfrac1N\,\text{Re}\sum_k\hat E_k\times\overline{\hat B_k}=\sum_xE\times B$ (Parseval), only for `photon_pair`/`charge_photon`/`em_photon` | EM field momentum | `observers.py:L417-429` | unknown (inferred: declared exact (unknown)) |
| 6 | $\delta=\max_\text{keys}\lVert P-P_0\rVert/\lVert P_0\rVert$ | momentum drift | `observers.py:L436-451` | unknown |
| 7 | $z=\sum_xp(x)e^{2\pi ix/L}/\sum p$, centroid $=\tfrac{L}{2\pi}\arg z \bmod L$, $p$ = axial profile of $E^2+B^2$; speed = slope of the unwrapped centroid vs tick | beam centroid/speed vs $d\Omega_\text{pair}/dk\rvert_{k_0}$ | `observers.py:L516-529, L545-548 BeamTrack` | unknown (inferred: quantitative) |
| 8 | `unitarity_residual`/`dispersion_fit`: call the channel hooks | pass-through | `observers.py:L243-266` | unknown (inferred: per hook) |

`field_snapshot` (L574) and `field_dump` (L593) are I/O plumbing. `field_dump` splits complex arrays into explicit `_re`/`_im` volumes and never writes complex data implicitly.

**Depends on:** `numerics.fft`, `lattice.geometry`, `gauge.photon.group_velocity_at`, `io.vtk`.  **Flags:** `TotalEnergy` sums $\tfrac12(E^2+B^2)$ for gauge channels. For $(f,g)$ spinors without a `mass`/`m` config the leg is `missing`, and `ParticleChannel` uses `mass`, so only massive singlets are counted. `Momentum.P_matter` sums over every complex key, including the colour axis of `quark_dirac` (shape $(3,L,L,L)$), but it takes `shape` from the first key and skips mismatched keys; for colour-stacked states `make_kgrid_3d(*shape)` receives 4 dims. **Verified 2026-09-28:** `Momentum().observe()` on a `composite` channel raises `TypeError: make_kgrid_3d() takes 3 positional arguments but 4 were given` (the same holds for any $(3,L,L,L)$ `f`/`eta_*` state: Weyl `particle` quarks, `quark_dirac`).

---

### `engine/core/photon_fermion_push.py` — Stage-5 photon→fermion push scenario (gate)
**Status:** live · standalone · **Findings:** F384–F390 F392 F395 · **Lattice:** BCC · **Law:** even (photon) + per-link (fermion) · **Units:** lattice

**Does:** It builds `em_photon` + `fermion_em` (with a $\hat C$-transverse beam packet and a fermion at rest, $k_0=0$) and measures momentum transfer. It adds no new kernels; the dynamics are `coupled.py` rows 11–17.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $E\mathrel{+}=a\,E^\text{beam}_T$, $B\mathrel{+}=a\,B^\text{beam}_T$ (beam projected onto $\hat C(k)$-transverse; `polarization` linear or circular) | beam seeding | `photon_fermion_push.py:L82-87 build_push_run()` | n/a |
| 2 | $\Delta P_m,\Delta P_f$ from the `Momentum` observer; $\Delta E_f$ from `energy()` | run measurement | `photon_fermion_push.py:L105-115 run_push_scenario()` | unknown (inferred: quantitative) |
| 3 | residual $=\lVert\Delta P_m+\Delta P_f\rVert/\lVert\Delta P_m\rVert$; $\cos(\Delta P_m,\hat k_0)$; $\cos(\Delta P_m,\Delta P_f)$ | F390 claims 1/2 | `photon_fermion_push.py:L176-180` | unknown (inferred: quantitative (thresholds 0.9, −0.85, 0.05)) |
| 4 | $T_{(1,0,0)}\circ\Phi^{n}=\Phi^{n}\circ T_{(1,0,0)}$, relative residual $<10^{-9}$ | exact crystal-momentum (translation covariance) check | `photon_fermion_push.py:L389-412 check_stage5_circular_beam_rerun()` | unknown (inferred: machine (threshold $10^{-9}$)) |
| 5 | fermion norm drift $\lvert n_1-n_0\rvert/n_0\in(0,0.5)$ | charge not exactly conserved (F385 fork a) | `photon_fermion_push.py:L381-386` | unknown (inferred: quantitative) |

**Depends on:** `core.coupled`, `core.observers`, `gauge.photon`, `gauge.em_photon_sourcing`.  **Flags:** `c_lat` is imported (L47) but unused. The `__main__` block only prints. This module is the only D8-compliant core module (`from casim.numerics import xp as np`).

---

### `engine/core/simulation.py` — `LatticeSpec` and the `Simulation` tick loop
**Status:** live · driven (0 ch) · **Findings:** — · **Lattice:** declares `topology` ∈ {cubic, bcc} (default **"cubic"**) · **Law:** n/a · **Units:** lattice

**Does:** It builds channels, the clock and the bus from a scenario, then advances every channel one engine tick at a time, runs observers on cadence, applies scheduled block-spin events, and checkpoints/resumes.

| # | Equation / rule | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c_\text{lat}$ default $=1/\sqrt3$ (registry, F26) | lattice light speed | `simulation.py:L97 LatticeSpec` | unknown (inferred: exact) |
| 2 | $L_\text{phys}=L\cdot\text{block}$, `cell_factor` $=\text{block}^{\,d}$; scenario `physical_patch` $P$ ⇒ $L=P/\text{block}$ | patch declaration | `simulation.py:L103, L108, L248` | unknown (inferred: exact) |
| 3 | `applied_order` = topological order if `bus.order` = `topological`, or if `auto` and topological equals declared; otherwise declared order (violations recorded) | execution order | `simulation.py:L220-228 _build_bus()` | unknown (inferred: exact) |
| 4 | per tick: for $c$ in order, $s_c\leftarrow\text{step}_c^{\,n_c}(s_c;\text{ctx})$ with $n_c$ = `clock.n_sub(c)`; ctx = live `states` (Gauss–Seidel), or for cycle members under `jacobi`, live states overlaid with the pre-tick snapshot of the cycle | the tick | `simulation.py:L294-313 step()` | unknown (inferred: exact (control flow)) |
| 5 | after the channel sweep: tick += 1 → observers (`tick % every == 0`) → scheduled $R_b$ → checkpoint | post-tick order | `simulation.py:L314-320` | unknown (inferred: exact) |
| 6 | $R_b$: every state ← `ch.block_spin(state,b)`; $L\to L/b$, block $\to$ block·$b$; asserts $L_\text{phys}$ invariant; re-baselines `_energy0` | block-spin event | `simulation.py:L341-351 block_spin()` | unknown (inferred: exact (bookkeeping)) |

Checkpoint/resume (L414–598) is I/O plumbing: atomic, compressed NPZ plus JSON meta, which round-trips the RNG state, clock spec, bus spec, block-spin schedule and events.

**Depends on:** `core.channel`, `core.observers`, `core.clock`, `core.graph`, `core.blockspin`, constants.  **Flags:** The `LatticeSpec.topology` default is `"cubic"` (L96, L254), while BCC is canonical (D1). A scenario that omits `topology` runs cubic-tagged, and BCC-only channels then fail validation. `run()` fires the observers once at tick 0 before stepping (L363).

---

### `engine/core/spectral_matter.py` — compute-once matter solves as channels
**Status:** live · driven (0 ch) · **Findings:** — · **Lattice:** none (momentum-space solves; tags cubic|bcc) · **Law:** "spectral" · **Units:** MeV

**Does:** It wraps three spectral solvers so the FB02/FB03/FB09/FA06 briefs have a `casim run` target. `init_state` solves once and `step` returns the state unchanged.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | NJL gap + RPA spectrum (`solve_meson_spectrum(Lam, GLam2, m0, g_rhopipi)`), converted to MeV (×10³); chiral check at $m_0=0$: `goldstone_ok` if $\lvert m_\pi\rvert<1$ MeV | `njl_meson` | `spectral_matter.py:L71-106 NJLMesonChannel` → `particles/meson.py` | unknown |
| 2 | relative errors $(x-x_\text{PDG})/x_\text{PDG}$ against $m_c=325$, $m_\pi=137$, $f_\pi$=`f_pi_pdg_target_MeV` (92.4, external) | scoring only | `spectral_matter.py:L62, L102-104` | n/a |
| 3 | `si_registry(f_pi_phys=f_pi_anchor_MeV)` (92.07, external, F77/F123): $m_p=3m_c$, $m_n-m_p$ | `njl_nucleon` | `spectral_matter.py:L138-158` → `lattice/si_scale.py` | unknown |
| 4 | $\sqrt\sigma/f_\pi=(\Lambda/f_\pi)(\sqrt\sigma/\Lambda)$, axis and sphere variants vs empirical 4.56 | `string_tension` | `spectral_matter.py:L185-199` → `interactions/running_scale_ratio.summary()` | unknown |

**Flags:** The `energy()` of these channels returns $f_\pi$, $m_p$ or the axis ratio, not an energy, so `norm_conservation` over them is trivially zero. Hard-coded PDG comparison literals appear at L62 and L134 (scoring only).

---

### `engine/core/tier3.py` — Monte-Carlo gauge and variable-c refraction channels
**Status:** live · driven (0 ch) · **Findings:** — · **Lattice:** cubic (4-D hypercubic MC; 2-D square refraction) · **Law:** monte-carlo / variable-c · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | one Cabibbo–Marinari heat-bath sweep + `n_or` over-relaxation of SU(3) links at $\beta$ (default 5.8), drawing from the engine RNG | `gauge_mc` tick (stochastic) | `tier3.py:L63-64 GaugeMonteCarloChannel.step()` → `forks/gauge/lgt_fork_A_mc.heatbath_sweep` | n/a (Markov chain) |
| 2 | `energy()` = mean plaquette; observables: plaquette and Wilson action | MC order parameter | `tier3.py:L70, L75-77` | unknown |
| 3 | $c(x)$ = smooth step $c_\text{left}\to c_\text{right}$ at $x=L/2$ (width 2); packet $h=(1,e^{i\arg k})/\sqrt2\times$ Gaussian $\times e^{ik\cdot x}$ | refraction setup | `tier3.py:L116-123 DynamicalRefractionChannel.init_state()` | n/a |
| 4 | exact-unitary Strang/Cayley variable-$c$ 2-D Weyl step, `n_sub`=4 | `refraction_2d` tick (F64 time-domain) | `tier3.py:L129-130` → `lattice/curved.weyl_step_2d_varc_strang` | unknown |

**Flags:** `gauge_mc` runs F94's simple-hypercubic Wilson ensemble. **SUPERSEDED by F323/F265** (`S21-F94-hypercubic-action-not-the-model-lattice`: not the model's lattice). `refraction_2d` steps with `lattice.curved`. The S10 note (F271) says the asymmetric-ordering and first-order half-step defects sit in `lattice.curved._half_step_dH` and therefore affect every F64-fork variable-$c$ result. The current code defaults to `ordering='weyl', order=2` (`curved.py:L189`), which suggests the fix has since landed (F276's Weyl ordering). The S10 note has not been updated, so this is an open question for 03-lattice. `gauge_mc`'s `density_field` raises `NotImplementedError`.

---

## Channel coupling order and data flow

*Source of truth: `core/simulation.py`, `core/graph.py`, `core/clock.py`, `core/channel.py`, `core/channels.py`, `core/coupled.py`, `particles/channel.py`. Everything below is read off the code. Scenario YAMLs choose which of these edges exist in a given run.*

### 1. What one engine tick does

1. **Build time** (`Simulation.__init__`, `simulation.py:L170-191`). Each channel is validated against `lattice.topology` and `init_state` is called **in declared order** (so `init_state` never sees a partner). The energy baseline `_energy0` is recorded. `clock.reconcile` fixes $\Delta t$ and $n_c$ (`clock.py:L232-334`). `graph.build_graph` resolves edges and SCCs (`graph.py:L215-335`), and `_build_bus` picks `applied_order` (`simulation.py:L214-229`).
2. **Order.** `step_order` = `applied_order`. Under the default `bus.order: auto` this is the **declared YAML order** unless the stable topological sort already equals it (L225–228). A reorder is applied only with `bus.order: topological`. The topological sort keeps the members of a cycle in declared order (`graph.py:L293`), so for the common two-channel matter↔gauge cycle the declared order **is** the executed order.
3. **Sweep** (`simulation.py:L298-313`). For each channel $c$ in order:
   - **gauss_seidel** (default, `graph.py:L85`): $c$ receives `context = self.states`, the live mapping. It therefore sees the **post-tick** states of every channel stepped before it this tick and the **pre-tick** states of every channel after it. With sub-cycling, `self.states[c]` is updated after each sub-step (L311–312).
   - **jacobi** (opt-in via `bus.cycle_scheme`): a channel that belongs to a cycle gets `dict(states)` overlaid with the frozen pre-tick states of all cycle members (L299–307), so the result inside a cycle is order-independent. Non-cycle channels still see the live mapping.
   - each channel is stepped $n_c$ = `clock.n_sub(c)` times (1 under `legacy`/`auto`-desynchronised).
4. **After the sweep:** `tick += 1` → observers whose `tick % every == 0` (they read `sim.states` post-tick) → the scheduled $R_b$ block-spin (`simulation.py:L317-318`) → the auto-checkpoint.
5. The engine never copies or merges states. **The only exchange mechanism is that a consumer reads its partner's state dict out of `context` by name.** "Quantities" are keys inside that dict; the bus checks the **channel name** only (every `provides()` returns `(name,)`, `channel.py:L141`, and no class overrides it).
6. **Edges seen by the bus** = `consumes()` config keys (`channel.py:L151-190`) ∪ any config string equal to another channel's name (`graph.py:L173-212`). A partner name that is only a **default inside `step()`** (e.g. `w_sourced` → `"fermion_doublet"`, `coupled.py:L96`) is invisible to the bus when the YAML omits it.

### 2. Registered channels (31) and the kernels they drive

Registered by importing `casim.engine` (`casim/engine/__init__.py:L14-19`). "Reads" lists the context keys a channel's `step()` reads from partners. "Publishes" lists the extra keys it writes into its own state for others. All classes declare `dt_native=1.0`, `subcyclable=True`.

| type_name | class (file:line) | F91 class / topology | engine kernel(s) driven per tick | reads (partner key) | publishes |
|---|---|---|---|---|---|
| `photon_pair` | `PhotonPairChannel` (`core/channels.py:L26`) | even / cubic,bcc | `gauge.photon.photon_step_spectral`; `gauge.photon.photon_step_dielectric` if a gravity partner has $K\ne1$; `core.blockspin.renormalized_even_step` if block>1 | `gravity`→`K` (via `read_K`) | `E`,`B` |
| `weyl_bcc` | `WeylBCCChannel` (`core/channels.py:L132`) | per-branch / bcc | `lattice.bcc.weyl_step_3d_bcc`; `blockspin.renormalized_weyl_step` | — | `f`,`g` |
| `w_chiral` | `WChiralChannel` (`core/channels.py:L180`) | chiral / cubic | `gauge.weak_wmu.w_propagation_step_chiral` (`fields.electroweak` re-export); `blockspin.renormalized_chiral_step` | — | `E`,`B` |
| `z_even` | `ZEvenChannel` (`core/channels.py:L216`) | even / cubic | `gauge.weak_z.z_propagation_step_spectral` | — | `E`,`B` |
| `gluon_bcc` | `GluonBCCChannel` (`core/channels.py:L243`) | even / bcc | `gauge.gluon.gluon_rotation_step_spectral_bcc` | — | `E`,`B` (8,L³) |
| `gravity_dielectric` | `GravityDielectricChannel` (`core/channels.py:L271`) | dielectric / cubic,bcc | static: none. dynamic: `interactions.gravity.phi_source`, `phi_wave_step`; init: `gaussian_mass_3d`, `solve_poisson_3d_open` | `sources:{name:w}` → `eta_u..chi_d` \| `f`,`g` \| `f_nu..g_e` \| `E`,`B` | `phi`,`K`,(`phi_prev`) |
| `w_sourced` | `WSourcedChannel` (`core/coupled.py:L74`) | chiral / bcc | `weak_wmu.fermion_isospin_current`, `w_propagation_step_spectral` (= chiral) | `fermion` (default `fermion_doublet`) → `f_nu`,`f_e` | `E`,`B`,`A` |
| `fermion_doublet` | `FermionDoubletChannel` (`core/coupled.py:L110`) | per-branch / bcc | `coupled.su2_expmap`, `weak_wmu.covariant_weyl_step_3d_bcc` | `w_field` (default `w_sourced`) → `A` | `f_nu`,`f_e`,`g_nu`,`g_e` |
| `charge_photon` | `ChargePhotonChannel` (`core/coupled.py:L156`) | even (label) / cubic | `gauge.charge_coupling.maxwell_curl_step` with its own static `J` | — (self-sourced) | `E`,`B`,`J` |
| `beta_decay` | `BetaDecayChannel` (`core/coupled.py:L213`) | chiral / bcc | `gauge.charged_current.emit_w_minus` (tick 1), then `w_massive_propagation_step_spectral` | — (internal $u,d$) | `E_W`,`B_W` |
| `em_photon` | `EmPhotonChannel` (`core/coupled.py:L263`) | even / bcc | `gauge.em_current.conserved_current`\|`full_current`, `gauge.em_photon_sourcing.split_transverse_longitudinal`, `gauge.photon.photon_step_spectral`, `gauge.charge_coupling.bcc_curl_symbol`, `solve_A_coulomb_3d` | `fermion` (default `fermion_em`) → `f`,`g` | `E`,`B`,`A`,`rho`,`E_L` |
| `fermion_em` | `FermionEmChannel` (`core/coupled.py:L460`) | per-link / bcc | `gauge.minimal_coupling.u1_link_weyl_step_3d_bcc` | `photon` (default `em_photon`) → `A` | `f`,`g` |
| `gauge_mc` | `GaugeMonteCarloChannel` (`core/tier3.py:L30`) | monte-carlo / cubic | `forks.gauge.lgt_fork_A_mc.heatbath_sweep` (uses engine RNG) | — | `U` |
| `refraction_2d` | `DynamicalRefractionChannel` (`core/tier3.py:L89`) | variable-c / cubic | `lattice.curved.weyl_step_2d_varc_strang` | — | `f`,`g` |
| `njl_meson` | `NJLMesonChannel` (`core/spectral_matter.py:L49`) | spectral | `particles.meson.solve_meson_spectrum` (init only) | — | `obs` |
| `njl_nucleon` | `NJLNucleonChannel` (`core/spectral_matter.py:L122`) | spectral | `lattice.si_scale.si_registry`, `np_splitting` (init only) | — | `obs` |
| `string_tension` | `StringTensionFpiChannel` (`core/spectral_matter.py:L173`) | spectral | `interactions.running_scale_ratio.summary` (init only) | — | `obs` |
| `entanglement_register` | `EntanglementRegisterChannel` (`core/entanglement_register.py:L53`) | "even" / any | `interactions.qi_entanglement.exchange_gate`, `apply_gate`; init `exchange_angle_per_tick` | — | `psi` |
| `quantum_circuit` | `QuantumCircuitChannel` (`…:L134`) | "even" / any | `qi_entanglement.apply_layer` | — | `psi` |
| `fermion_chain` | `FermionChainChannel` (`…:L225`) | per-branch / any | `particles.second_quant.FermionChain` ($e^{-iH}$) | — | `psi` |
| `fermion_algorithm` | `FermionAlgorithmChannel` (`…:L302`) | per-branch / any | `second_quant.FermionChain.apply_program_fock` | — | `psi` |
| `error_correction` | `ErrorCorrectionChannel` (`…:L432`) | "even" / any | `interactions.qi_noise` (Kraus + recovery) | — | `rho` |
| `particle` | `ParticleChannel` (`particles/channel.py:L116`) | per-branch / bcc | free: `lattice.bcc.weyl_step_3d_bcc`; doublet+weak: `su2_expmap` + `weak_wmu.covariant_weyl_step_3d_bcc`; massive singlet: `particles.dirac_bcc.dirac_step_3d_bcc_splitstep` / `_varm_splitstep`; em: `gauge.minimal_coupling.u1_wrap_weyl_step_3d_bcc` / `u1_wrap_dirac_step_3d_bcc`; quark: `minimal_coupling.su3_rotate_weyl_step_3d_bcc`; gravity: `interactions.gravity.lapse_mix_half` | `couplings.weak`→`A`; `couplings.em`→`alpha`; `couplings.strong`→`A`; `couplings.gravity`→`K`,`phi`; `confine.field`→`S`; `confine.partners[]`→`centroid_prev` | `J_em`,`rho_em` (if em); `J_colour` (if strong); `centroid_prev`; `grav_potential`,`grav_K_centroid` |
| `quark_dirac` | `ColourDiracQuarkChannel` (`particles/channel.py:L530`) | per-branch / bcc | `gauge.gluon._su3_expmap_field` (colour rotation); `dirac_bcc.dirac_step_3d_bcc_varm_splitstep` / `_splitstep` per colour | `couplings.strong`→`A`; `couplings.em`→`alpha`; `confine.*`→`S`/`centroid_prev` | `J_em`,`rho_em`,`J_colour`,`centroid_prev` |
| `nr_electron` | `NonRelElectronChannel` (`particles/channel.py:L695`) | non-rel / cubic,bcc | own Strang Schrödinger split-step; `interactions.gravity.solve_poisson_3d_open` | `sources[]`→`rho_em` | `rho_em`,`J_em` |
| `composite` | `CompositeParticleChannel` (`particles/channel.py:L860`) | per-branch / bcc | `lattice.bcc.weyl_step_3d_bcc` per constituent | — | `f`,`g`,`centroid_prev` |
| `photon_sourced` | `PhotonSourcedChannel` (`particles/channel.py:L943`) | even / cubic,bcc | `gauge.photon.photon_step_spectral`; `gravity.solve_poisson_3d_open` | `sources[]`→`J_em`,`rho_em` | `E`,`B`,`alpha` |
| `gluon_sourced` | `GluonSourcedChannel` (`particles/channel.py:L1012`) | even / bcc | `gauge.gluon.gluon_sourced_step_bcc` | `sources[]`→`J_colour` | `E`,`B`,`A` |
| `colour_bag` | `ColourBagChannel` (`particles/channel.py:L1076`) | dielectric / bcc | mean-field FFT smear; or `strong.dual_gl_backreaction.self_consistent_bag` | `sources[]`→`J_colour` | `S`,`eps_c`,`phi`,`f` |
| `two_grid_atom` | `TwoGridAtomChannel` (`particles/channel.py:L1366`) | multigrid | **private** inner `quark_dirac`×3 on a fine BCC lattice + `lattice.multigrid.coarse_point_potential`, `schrodinger_step` | — (outer context unused) | `psi`, `fine::*` |
| `element_atom` | `ElementAtomChannel` (`particles/channel.py:L1618`) | multigrid | `lattice.multigrid.schrodinger_step`, Gram–Schmidt, Hartree $V_{ee}$; Tier B inner `quark_dirac`; `core.manybody.aufbau_configuration` | — (outer context unused) | `psis`,`V_nuc`,`Vees`,… |

### 3. Exchange edges: producer → quantity → consumer, with the equation applied

Arrows point from the channel whose state is read to the channel that reads it. "Same tick" holds when the producer comes earlier in `step_order`; otherwise the consumer sees the value from the previous tick.

| # | producer → consumer | exchanged | equation on the consumer side | where |
|---|---|---|---|---|
| E1 | `fermion_doublet` / `particle` (doublet) → `w_sourced` | $f_\nu,f_e$ | $J^a=\bar f\,\tfrac{\tau^a}{2}f$ (upper comps.); $E\leftarrow\mathcal R_\text{chiral}E+g_\text{lat}J$; $A\leftarrow A+E$ | `coupled.py:L98-103` |
| E2 | `w_sourced` → `fermion_doublet` | $A$ (isospin triplet) | $U_\ell=\exp(i\varepsilon A^a\tau^a/2)$ on all 8 links; site-averaged covariant BCC Weyl step | `coupled.py:L135-140` |
| E3 | `w_sourced` → `particle` (doublet, `couplings.weak`) | $A$ | same as E2, wrapped inside the optional U(1) phase of E7 | `particles/channel.py:L374-381` |
| E4 | `fermion_em` → `em_photon` | $f,g$ | $J$ = F384 conserved (or F389 full) current; $E\leftarrow R(\Omega_\text{pair})E+g_\text{lat}J_T$; $\rho\mathrel{+}=g_\text{lat}\mathcal F^{-1}(-iC\cdot\hat J)$; $\hat E_L=-iC\hat\rho/\lvert C\rvert^2$; $A=\text{solve\_A\_coulomb}(B)$ | `coupled.py:L406-446` |
| E5 | `em_photon` → `fermion_em` | $A$ (spatial 3-vector) | per-link Peierls step $\psi'=\sum_d e^{iqA\cdot d/\sqrt3}M_d\,\text{shift}_{d/\sqrt3}\psi$ | `coupled.py:L489-491` → `minimal_coupling.py:L140` |
| E6 | `particle` / `quark_dirac` / `nr_electron` → `photon_sourced` | $J_\text{em}$, $\rho_\text{em}$ | $E\leftarrow R(\Omega_\text{pair})E+g_\text{em}\,dt\sum J$; $\varphi_\text{em}=-\text{Poisson}_\text{open}(\sum\rho;G_N=g_c/4\pi)$; $\alpha\leftarrow\alpha+\varphi_\text{em}\,dt$ | `particles/channel.py:L978-1000` |
| E7 | `photon_sourced` → `particle` (`couplings.em`) | $\alpha$ (accumulated $A_0$ Wilson-line angle) | Weyl singlet / Dirac: wrap $e^{+iq\alpha}\,W\,e^{-iq\alpha}$; doublet: the same per member, around the SU(2) step; Weyl quark: the same around the SU(3) step; **confined Dirac**: bare post-step phase $e^{-iq\alpha}$ | `particles/channel.py:L343-348, L361-386, L390-403, L418-421` |
| E8 | `photon_sourced` → `quark_dirac` | $\alpha$ | bare post-step phase $e^{-iq\alpha}$ | `particles/channel.py:L644-648` |
| E9 | `particle` (quark) / `quark_dirac` → `gluon_sourced` | $J^a_\text{colour}=\sum_\text{spin}q^\dagger T^aq$ | $E\leftarrow R_\text{even,BCC}E+g_\text{lat}\,dt\sum J^a$; $A\leftarrow A+E$ | `particles/channel.py:L1035-1045` → `gluon.py:L778-779` |
| E10 | `gluon_sourced` → `particle` (quark) | $A^a$ | $q\to V q$, $V$=`_su3_expmap_field`$(\varepsilon A)$ (site-local SU(3) exponential of the octet; its sign convention is mapped in 05c), then free BCC Weyl step per colour | `particles/channel.py:L395-401` → `minimal_coupling.py:L91` |
| E11 | `gluon_sourced` → `quark_dirac` | $A^a$ | $V=\text{\_su3\_expmap\_field}(\varepsilon A)$ applied to every Dirac component before the Dirac step | `particles/channel.py:L616-625` |
| E12 | `particle` / `quark_dirac` → `colour_bag` | $J_\text{colour}$ | mean field: $\rho=\sum\lVert J^a\rVert$, $\phi=G_\lambda*\rho$, $f^2=e^{-\phi/\phi_0}$, $S=M_\text{bag}f^2$, $\varepsilon_c=1-f^2$; or the self-consistent dual-GL solve (F139) | `particles/channel.py:L1124-1158` |
| E13 | `colour_bag` → `particle`(Dirac) / `quark_dirac` (`confine.field`) | $S(x)$ | $m_\text{eff}(x)=m+S(x)$ in the variable-mass BCC Dirac step | `particles/channel.py:L264-267, L338-342, L628-637` |
| E14 | `particle` / `quark_dirac` ↔ each other (`confine.partners`) | `centroid_prev` (start-of-tick centroid) | $V_i=\sum_{j\ne i}\tfrac\sigma2\lvert x-r_j\rvert$ (pairwise) or $\sigma\lvert x-R_\text{cm}\rvert$ (`anchor: com`), used as a scalar mass (default) or a vector phase $e^{-iV\,dt}$ | `particles/channel.py:L269-308` |
| E15 | `particle` / `quark_dirac` / `nr_electron` → `nr_electron` (`sources`) | $\rho_\text{em}$ | $V=q\,\varphi_\text{em}$, $\varphi_\text{em}=-\text{Poisson}_\text{open}(\rho;G_N=g_c/4\pi)$; Strang $e^{-iV\,dt/2}e^{-ik^2dt/2m}e^{-iV\,dt/2}$ | `particles/channel.py:L734-752, L813-818` |
| E16 | any matter/gauge channel → `gravity_dielectric` (dynamic, `sources:{name:w}`) | spinor components or $E,B$ | $T^{00}=\sum_sw_s t_s$; $s=\kappa c^2T^{00}/2$ ($\kappa=1$); $\varphi$ leapfrog at $c_g$; $K=e^{-2\varphi/c^2}$ | `core/channels.py:L332-377` |
| E17 | `gravity_dielectric` → `photon_pair` (`gravity:`) | $K$ | $\Omega_K=\Omega_\text{pair}(k)/K(x)$, Strang/Weyl-ordered (F271) | `core/channels.py:L81-100` |
| E18 | `gravity_dielectric` → `particle` (massive Dirac, `couplings.gravity`) | $K$ | $\sqrt A=K^{-1/2}$; `lapse_mix_half` before and after the Dirac step: rotation $\eta\leftrightarrow\chi$ by $\theta=-(\sqrt A-1)m\,dt/2$ | `particles/channel.py:L323-356, L469-484` → `gravity.py:L371-378` |
| E19 | `gravity_dielectric` → `particle` (any, `couplings.gravity`) | $\varphi$, $K$ | readouts only: $\langle\varphi\rangle_\rho=\sum\rho\varphi/\sum\rho$, $K$(centroid); these do not affect the dynamics | `particles/channel.py:L486-499` |

Channels with **no** context edges: `weyl_bcc`, `w_chiral`, `z_even`, `gluon_bcc`, `charge_photon`, `beta_decay`, `gauge_mc`, `refraction_2d`, `njl_*`, `string_tension`, the five register channels, `composite`, `two_grid_atom`, `element_atom`. `photon_pair` has an edge only when a `gravity:` partner is wired, and static `gravity_dielectric` consumes nothing. `two_grid_atom` and `element_atom` run a **private** inner Gauss–Seidel sweep over their own fine `quark_dirac` channels, with an inner context that each quark updates in place (`particles/channel.py:L1466-1469, L1947-1951`). Their inner quarks declare `couplings: {em: "photon"}` only so that they publish `rho_em`. No `photon` channel exists inside, so E7/E8 never fire there.

### 4. Cycles and the order contract

- **Genuine two-way loops** (each forms a 2-cycle SCC, so the executed order is the declared order): E1/E2 (`w_sourced` ⇄ `fermion_doublet`), E4/E5 (`em_photon` ⇄ `fermion_em`), E6/E7 (`photon_sourced` ⇄ charged `particle`s), E9/E10 (`gluon_sourced` ⇄ quark `particle`s), E12/E13 (`colour_bag` ⇄ confined quarks), E16/E18 (`gravity_dielectric` ⇄ massive Dirac `particle`s), and E14 among the confined partners.
- **Documented contract** (docstrings `coupled.py:L79-81, L115, L289-291, L467-468`): register the **gauge channel before its fermion**. The gauge channel then consumes the *pre-tick* fermion and publishes an updated $A$ that the fermion consumes in the *same* tick. F388 asserts this as `ordering_pretick_posttick_exact` (`coupled.py:L582-596, L670`).
- The contract is enforced only by declared YAML order. Under `jacobi` both members read pre-tick states instead, which is a different (lagged) scheme. Under `bus.order: topological` a 2-cycle keeps declared order, so nothing is reordered.
- **Clock interaction.** When a partner runs with a different `dt` (e.g. `photon_sourced` $dt=0.1$ against matter at 1.0) and the clock resolves to `legacy`, each gets one step per tick and they advance different physical times while coupled (F268). Only `clock.mode: strict` sub-cycles them.

### 5. Diagram-ready edge list

```
fermion_doublet|particle(doublet) --f_nu,f_e--> w_sourced --A--> fermion_doublet|particle(doublet)
fermion_em --f,g--> em_photon --A--> fermion_em
particle|quark_dirac|nr_electron --J_em,rho_em--> photon_sourced --alpha--> particle|quark_dirac
particle(quark)|quark_dirac --J_colour--> gluon_sourced --A--> particle(quark)|quark_dirac
particle(quark)|quark_dirac --J_colour--> colour_bag --S--> particle(Dirac)|quark_dirac
particle|quark_dirac --centroid_prev--> particle|quark_dirac   (confine.partners)
particle|quark_dirac|nr_electron --rho_em--> nr_electron
{spinor | E,B channels} --T00 legs--> gravity_dielectric(dynamic) --K--> photon_pair
gravity_dielectric --K (sqrtA)--> particle(massive Dirac) ; --phi,K--> particle (readout only)
isolated: weyl_bcc w_chiral z_even gluon_bcc charge_photon beta_decay gauge_mc refraction_2d
          njl_meson njl_nucleon string_tension entanglement_register quantum_circuit
          fermion_chain fermion_algorithm error_correction composite
          two_grid_atom(private inner loop) element_atom(private inner loop)
```
