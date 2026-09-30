# 09 — Top-level compatibility packages (`casim.fields`, `casim.gravity`, `casim.lattice`, `casim.particles`)

*Model map part p09 — written 2026-09-28 - 00:00.*

**Scope.** The four top-level packages that predate the D6/C9 single-tree layout: `src/casim/fields/`, `src/casim/gravity/`, `src/casim/lattice/`, `src/casim/particles/` (every `.py`, 14 files). Most are pure re-export layers onto `casim.engine.*` and get a name → source table only. Five files are **not** thin and are mapped equation by equation: `lattice/chiral_core.py`, `lattice/backend.py`, `particles/spec.py`, `particles/composite.py`, `particles/channel.py`.

**Shared conventions.**
- **None of these 14 files has a record in the engine module registry (D11).** `registry.tsv` has no row for any `src/casim/{fields,gravity,lattice,particles}/` path, and `check_coverage()` walks only `engine/<sector>/`. So every non-thin module below is flagged `UNREGISTERED`, and its exactness defaults to `unknown` unless `docs/status/exactness-inventory.md` names the result.
- `particles/channel.py` is **not** dead: `src/casim/engine/__init__.py:L19` imports it (`from ..particles import channel as _particles`), so its nine `@register` channels and four observers are live engine channel types (`particle`, `quark_dirac`, `nr_electron`, `composite`, `photon_sourced`, `gluon_sourced`, `colour_bag`, `two_grid_atom`, `element_atom`, plus observers). `docs/design/module-migration-manifest.yaml:L79` records that `src/casim/particles/*` is "NOT done and needing its own manifest record before it can move".
- These five modules import `numpy` directly (`import numpy as np`). D8 requires numerics to go through `casim.numerics`. The FFTs in `chiral_core.py` and `channel.py` do go through the `casim.numerics.fft` façade; the array arithmetic, `np.fft.fftfreq`, `np.einsum`, `np.vdot` and `np.gradient` do not. (`fftfreq` on numpy is allowed by D8. The others are listed under OTHER in the flags.)
- **Lattice:** BCC is canonical (D1). Every Weyl/Dirac propagation in `channel.py` calls the BCC kernels. The Schrödinger/Poisson/multigrid sectors use a plain cubic spectral grid ($k=2\pi\,\text{fftfreq}(L)$, continuum $\lvert k\rvert^2$), which the code labels as outside the F91 classes.
- **Units:** lattice units throughout. The one exception is the NN potential in `ElementAtomChannel`, which is in MeV/fm via `engine.particles.nuclear`, converted by the config scales `g_nn` and `r_fm_per_cell`. `si_scale` is not used anywhere.

**Modules covered:** fields/`__init__`, `electroweak`, `em`, `entanglement`, `matter`, `photon`, `strong`; gravity/`__init__`; lattice/`__init__`, `backend`, `chiral_core`; particles/`__init__`, `channel`, `composite`, `spec`.

---

## A. Pure re-export shims

These files hold no equations. Where a module loads by string inside `try/except` (the fields sub-packages), a failed import quietly sets the name to `None`.

### `fields/__init__.py`
Imports the sub-modules `photon, electroweak, strong, matter, em, entanglement` (L15). The docstring's F91 table is prose only; the classification it describes is mapped in 05a–05c.

### `fields/photon.py` — paired-spinor photon (even law, F67/F68/F69)
| Name | Source |
|---|---|
| `ca_photon_pair` | `casim.engine.gauge.photon` (module) |
| `pair_dispersion`, `pair_birefringence`, `photon_step_spectral`, `photon_step_dielectric`, `build_pair_mode`, `build_beam_packet`, `group_velocity`, `group_velocity_at` | `casim.engine.gauge.photon` |

### `fields/electroweak.py` — W±/Z/hypercharge
| Name | Source |
|---|---|
| `ca_wmu` | `casim.engine.gauge.weak_wmu` |
| `ca_weak` | `casim.engine.gauge.weak` |
| `ca_z_field` | `casim.engine.gauge.weak_z` |
| `ca_charged_current` | `casim.engine.gauge.charged_current` |
| `ca_hypercharge` | `casim.engine.gauge.hypercharge` |
| `_f26_rotation_step`, `w_propagation_step_chiral` | attributes of `casim.engine.gauge.weak_wmu` (via `getattr`, L37–38) |

Note: `_f26_rotation_step` and `w_propagation_step_chiral` are bound only when `ca_wmu` imported (L36). If it did not, both names are listed in `__all__` (L40) but undefined. CLAUDE.md names the home as `casim.engine.gauge.wmu`, but the code uses `weak_wmu` (see 05b).

### `fields/em.py` — σ-bilinear construction (W/Z/gluon only, **never the photon**, F65–F69)
| Name | Source |
|---|---|
| `ca_maxwell` | `casim.engine.gauge.bilinear` |
| `ca_maxwell_2d` | `casim.engine.gauge.bilinear_2d` |

### `fields/entanglement.py`
| Name | Source |
|---|---|
| `ca_entanglement` | `casim.engine.interactions.qi_entanglement` |

### `fields/matter.py`
| Name | Source |
|---|---|
| `ca_dirac` | `casim.engine.particles.dirac` |
| `ca_dirac_bcc` | `casim.engine.particles.dirac_bcc` |
| `ca_baryon` | `casim.engine.particles.baryon` |
| `ca_higgs` | `casim.engine.particles.higgs` |

### `fields/strong.py`
| Name | Source |
|---|---|
| `ca_gluon` | `casim.engine.gauge.gluon` |
| `ca_strong` | `casim.engine.gauge.strong` |
| `ca_colour_condensate` | `casim.engine.gauge.colour_condensate` |
| `ca_colour_dielectric` | `casim.engine.gauge.colour_dielectric` |
| `ca_confinement` | `casim.engine.gauge.confinement` |
| `ca_dual_gl_backreaction` | `casim.engine.interactions.gravity_backreaction` |
| `spinor_color` | `casim.engine.core._viz_spinor_color` |

Note: `ca_dual_gl_backreaction` maps to the **gravity**-prefixed module `interactions.gravity_backreaction`, even though its physics is the colour dual-Ginzburg–Landau bag (F139). The name is misleading, but the re-export is correct as written. See 07a.

### `gravity/__init__.py` — F64 dielectric gravity
| Name | Source |
|---|---|
| `ca_gravity` | `casim.engine.interactions.gravity` (module) |
| `C_LAT_BCC`, `F106_COEFF_LATTICE`, `G_LATTICE`, `K_canonical`, `dielectric_from_phi`, `dielectric_mix_half`, `T00_dirac_rest`, `T00_dirac_kinetic`, `T0i_dirac`, `T00_field_energy`, `phi_source`, `lap_nd`, `solve_phi_poisson`, `phi_wave_step`, `phi_field_energy`, `lapse_mix_half` | `casim.engine.interactions.gravity` |
| `poisson_open` | `casim.engine.lattice.poisson_open` (module) |
| `solve_poisson_3d_open`, `gaussian_mass_3d` | `casim.engine.lattice.poisson_open` |
| `ca_curved()` (lazy function, returns module or `None`) | `casim.engine.lattice.curved` |
| `ca_emqg()` (lazy function, returns module or `None`) | `casim.engine.interactions.gravity_emqg` |

The docstring calls the dielectric $K=e^{2GM/rc^2}$ the gravity law. Per decision 4 / F178 it is now the **vacuum/weak-field representation**; the canonical law is the induced Einstein equation. This file only re-exports, so there is nothing further to map here (see 07a § gravity.py).

### `lattice/__init__.py`
| Name | Source |
|---|---|
| `backend` | `casim.lattice.backend` (below) |
| `ca_lattice` | `casim.engine.lattice.geometry` |
| `ca_fft` | `casim.numerics.fft` |
| `ca_bcc` | `casim.engine.lattice.bcc` |
| `ca_core` | `casim.engine.lattice.core` (simple-cubic **reference**, D1) |
| `ca_core_exact` | `casim.engine.lattice.core_exact` (simple-cubic **reference**, D1) |
| `ca_lazy` | `casim.numerics.lazy` (or `None`) |
| `make_kgrid_1d`, `make_kgrid_2d`, `make_kgrid_3d` | `casim.engine.lattice.geometry` |
| `bcc_dispersion`, `bcc_unitary`, `weyl_step_3d_bcc`, `measure_bcc_dispersion`, `bcc_unitarity_residual`, `bcc_norm_drift_test` | `casim.engine.lattice.bcc` |

`chiral_core` is **not** imported by `lattice/__init__.py`. Callers import it directly (`tests/casim/test_chiral_core_caching.py:L38`, `tests/findings/test_F134_phase4_completion.py:L33`).

### `particles/__init__.py`
| Name | Source |
|---|---|
| `ParticleSpec`, `REGISTRY`, `DOUBLETS`, `FORCES`, `get_spec`, `doublet_specs`, `anomaly_traces` | `casim.particles.spec` (below) |
| `CompositeSpec`, `COMPOSITES`, `get_composite`, `beta_decay_ledger` | `casim.particles.composite` (below) |

---

## B. Modules with real code

### `lattice/backend.py` — deprecated FFT/chiral-transform seam shim
**Status:** UNREGISTERED (no module-registry record) · **Findings:** none · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** forwards everything to `casim.numerics.backends` (roadmap C1.1). This is plumbing with no equations.

- `register_backend` / `get_backend` / `backend_name` and `fftn…ifft`, `chiral_transform` forward to `_b.register` / `_b.active()` / `_b.active_name()` (`backend.py:L35–53`).
- `_CaFftAlias` (`backend.py:L56–88`) keeps the legacy name `"ca_fft"` registered (L91–92). Its `_t()` avoids infinite recursion by falling back to the first available of `pyfftw → scipy → numpy` when the alias is itself the active backend.
- The docstring (L11–12) says the file "is deleted at C9". It still exists after C9, because `tests/casim/test_backend.py` (gate tier) and `tests/findings/test_F134_phase4_completion.py` import it, and `chiral_core.register()` routes through it.

**Flags:** UNREGISTERED. The "deleted at C9" docstring is stale.

### `lattice/chiral_core.py` — hand-rolled chiral 2×2 core (F134-D, finding file `F134b`)
**Status:** UNREGISTERED (no module-registry record) · **Findings:** F134b (the code cites "F134"; the file is `findings/F134b-phase4-chiral-blockspin-completion.md`) · **Lattice:** BCC · **Law:** per-branch (Weyl $U^\pm$) and **chiral** (W± RS), F91 · **Units:** lattice

**Does:** re-implements the two chiral spectral transforms, the BCC Weyl tick and the W± Riemann–Silberstein chiral tick. Every per-mode complex product is done on explicit (re, im) real pairs. This answers the CLAUDE.md chiral-transform hazard.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $(a_r+ia_i)(b_r+ib_i)=(a_rb_r-a_ib_i)+i(a_rb_i+a_ib_r)$ | explicit-real complex multiply | `chiral_core.py:L83 cmul()` | unknown (inferred: exact (IEEE arithmetic identity)) |
| 2 | $\begin{pmatrix}F'\\G'\end{pmatrix}=\begin{pmatrix}U_{ff}&U_{fg}\\U_{gf}&U_{gg}\end{pmatrix}\begin{pmatrix}F\\G\end{pmatrix}$, each product via #1 | per-mode SU(2) mix | `chiral_core.py:L99–100 su2_apply()` | unknown (inferred: exact (arithmetic)) |
| 3 | $U^\pm(\mathbf k)=u^\pm\,I-i\,\mathbf n^\pm\!\cdot\boldsymbol\sigma$: $U_{ff}=u-in_z,\ U_{fg}=-i(n_x-in_y),\ U_{gf}=-i(n_x+in_y),\ U_{gg}=u+in_z$, with $(u,\mathbf n)$ from `bcc._bcc_uvec` at arguments $k_i c_\text{lat}$, $c_\text{lat}=1/\sqrt3$ (F25/F26) | closed-form BCC Weyl unitary (no eig) | `chiral_core.py:L112–116 weyl_unitary_real()` | unknown (inferred: exact (closed form; $u^2+\lvert\mathbf n\rvert^2=1$ is in `bcc.py`, see 03-lattice.md)) |
| 4 | $\psi_{t+1}=\mathcal F^{-1}\,U^\pm(\mathbf k/b)\,\mathcal F\,\psi_t$ for $\psi=(f,g)$, with block factor $b$ (`block`) | one BCC Weyl tick; block-renormalised coarse rule for $b>1$ | `chiral_core.py:L132–137 weyl_step()` | machine (inventory #76 F134-D: $9.9\times10^{-16}$ vs `weyl_step_3d_bcc`; measured here $1.3\times10^{-15}$ at $L=8$) |
| 5 | $\Omega^\pm(\mathbf k)=2\,\omega^\pm\!\big(\mathbf k/(2b)\big)$, $\omega^\pm=\arccos u^\pm$ | per-branch W± rotation rates | `chiral_core.py:L152–153 _chiral_branch_rates()` | unknown (inferred: exact (closed form)) |
| 6 | on even-$L$ Nyquist planes: $\Omega^+=\Omega^-=\tfrac12(\Omega^++\Omega^-)$ | Nyquist symmetrisation (even rate on the self-conjugate plane) | `chiral_core.py:L160–163 _chiral_branch_rates()` | unknown (inferred: exact) |
| 7 | $F^\pm=\tilde E\pm i\tilde B$; $F^+\to e^{-i\Omega^+}F^+$, $F^-\to e^{+i\Omega^-}F^-$ (via #1 with cached $\cos,\sin$) | chiral RS branch rotation | `chiral_core.py:L189–196 chiral_rs_step()` | machine (inventory #76: $1.3\times10^{-15}$; measured $8.9\times10^{-16}$ vs `w_propagation_step_chiral` at $L=8$) |
| 8 | $E'=\operatorname{Re}\mathcal F^{-1}\tfrac12(F^+{+}F^-)$, $B'=\operatorname{Re}\mathcal F^{-1}\tfrac{-i}{2}(F^+{-}F^-)$ | reconstruct real $(E,B)$ | `chiral_core.py:L197–198 chiral_rs_step()` | unknown (inferred: machine) |

**Chiral-hazard check: are real and imaginary parts both preserved?** Yes, in both transforms.
- **Weyl (#2–#4).** `su2_apply` splits every complex operand into `.real` and `.imag` and forms all four products per term by hand (#1). It then reassembles `(Σr) + 1j·(Σi)` (L99–100). Nothing is dropped, and the output is returned complex with no `.real` projection. Spot check: a random complex $(f,g)$ at $L=8$ conserves norm to $4.5\times10^{-13}$ absolute on a norm of $\sim10^3$ (relative $\sim10^{-16}$), and agrees with `bcc.weyl_step_3d_bcc` to $1.3\times10^{-15}$.
- **W± RS (#7–#8).** The branch rotation is done by `cmul` on explicit parts, and both $F^\pm$ keep full complex content through the inverse FFT. The final `.real` (L197–198) discards an imaginary part that is **exactly zero** for real input. The reason is that the rates satisfy $\Omega^+(\mathbf k)=\Omega^-(-\mathbf k)$. This follows from $\omega^+(\mathbf k)=\omega^-(-\mathbf k)$, checked to max difference $0.0$ on an $L=8$ grid, while $\omega^+(\mathbf k)\ne\omega^+(-\mathbf k)$ by up to $2.42$. Together with $\tilde E(-\mathbf k)=\tilde E(\mathbf k)^*$, this makes $F^-_\text{new}(-\mathbf k)=F^+_\text{new}(\mathbf k)^*$, so the reconstructions are Hermitian. Measured imaginary residue before `.real`: $0.0$ for both $E$ and $B$ at $L=8$. The Nyquist symmetrisation (#6) is what keeps this true on the self-conjugate planes. $\sum(E^2+B^2)$ is conserved to $4.5\times10^{-13}$ absolute.
- The FFT itself goes through the `casim.numerics.fft` façade (complex transform). Only the 2×2 mode mix is hand-rolled, as the docstring says (L37–38).

**Inputs → outputs:** `weyl_step(f, g, sign, block)` returns complex `(f', g')`. `chiral_rs_step(E, B, block)` returns real `(E', B')`. `ChiralCore.chiral_transform(kind, …)` dispatches `"weyl"` or `"w_rs"` (L218–227). `register()` registers the core as backend `"chiral_core"` through `casim.lattice.backend` (L230–235). Caches keyed on `(shape, sign, block)` / `(shape, block)` are frozen read-only (L66–69).

**Depends on:** `engine.lattice.bcc._bcc_uvec`, `bcc_dispersion` (see 03-lattice.md § bcc.py); `engine.lattice.geometry.make_kgrid_3d`; `casim.numerics.fft` (02-numerics.md). The pure primitives `cmul`/`su2_apply` are **duplicated** verbatim in `casim.numerics.chiral` (02-numerics.md) instead of being imported from it.

**Flags:**
- UNREGISTERED.
- ⚠ DOC/CODE MISMATCH: `docs/status/exactness-inventory.md` row #76 (F134-D) says the core "reproduces … bit-for-bit". The module docstring (L24–35) and the code say it does **not** (a few ULP, $1.4$/$1.8\times10^{-15}$ at $L=32$). The measured behaviour matches the docstring.
- OTHER: `cmul`/`su2_apply` are duplicated in `casim.numerics.chiral`, so there are two copies of the audited primitives. The module also imports `numpy` directly (D8).
- OTHER: the code cites "F134", but the finding file is `F134b-…` (`F134` is the unified real-space integration).

### `particles/spec.py` — typed particles with exact quantum numbers
**Status:** UNREGISTERED (no module-registry record) · **Findings (cited in code):** F38 (FG-1), F35 (W6.4), F53, F27, F64, F68 · **Lattice:** n/a · **Law:** n/a · **Units:** exact `Fraction` charges; `mass` is in lattice units

**Does:** bookkeeping of first-generation Weyl species. Every charge is an exact `fractions.Fraction`, and the force-applicability matrix is derived from the charges rather than declared. Hypercharge uses the **doubled convention** $Q=T_3+Y/2$ (so $Y_{e_R}=-2$).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $Q=T_3+Y/2$ (raises `ValueError` otherwise) | Gell-Mann–Nishijima check at construction | `spec.py:L52 ParticleSpec.__post_init__()` | unknown (registry silent; the arithmetic is exact `Fraction`) |
| 2 | forces $=\{\text{gravity}\}\cup\{\text{em}: Q\ne0\}\cup\{\text{weak}: T_3\ne0\lor Y\ne0\}\cup\{\text{strong}: \text{colour}\}$ | derived applicability matrix | `spec.py:L64–71 couples_to()` | unknown (logic) |
| 3 | $C:(T_3,Q,Y,B,L)\to-(T_3,Q,Y,B,L)$, chirality $L\leftrightarrow R$ | charge conjugation (F53) | `spec.py:L80–82 conjugate()` | unknown (exact `Fraction`) |
| 4 | FG-1 content: $\nu_L(\tfrac12,-1)$, $e_L(-\tfrac12,-1)$, $e_R(0,-2)$, $u_L(\tfrac12,\tfrac13)$, $d_L(-\tfrac12,\tfrac13)$, $u_R(0,\tfrac43)$, $d_R(0,-\tfrac23)$ as $(T_3,Y)$; $Q$ built from #1; quarks $B=\tfrac13$, leptons $L=1$ | first-generation registry, plus generated conjugates | `spec.py:L106–120 _FIRST_GEN / REGISTRY` | unknown (exact data) |
| 5 | Over the left-handed set (doublets plus $e^c_L,u^c_L,d^c_L$), with $n=3$ for colour and $1$ otherwise: $\sum nY$, $\sum nY^3$, $\tfrac12\sum_{T_3\ne0}nY$, $\sum_\text{colour}Y$, $\#\text{triplets}-\#\text{antitriplets}$ | the five anomaly traces grav–Y, Y³, SU(2)²Y, SU(3)²Y, SU(3)³; all vanish | `spec.py:L161–168 anomaly_traces()` | unknown (exact `Fraction`; the F38 result is exact per findings) |

Hand check of #5 with the registry content: $\sum nY=-2+2+2-4+2=0$, and $\sum nY^3=-2+\tfrac29+8-\tfrac{64}9+\tfrac89=0$.

**Inputs → outputs:** `get_spec(name)` / `doublet_specs(name)` return `ParticleSpec`s. `anomaly_traces()` returns a dict of five `Fraction`s. **Depends on:** nothing in casim (pure stdlib).

**Flags:**
- UNREGISTERED. EXACTNESS unknown (#1–5), because the registry is silent. The data and arithmetic are exact `Fraction`.
- ⚠ DOC/CODE MISMATCH (minor): the `anomaly_traces` docstring (L149) says "All **six** vanish", but the code returns **five** traces.
- OTHER: the SU(2)²Y trace carries a stray $\tfrac12$ (L163). It does not change the zero, but the value is not the conventional trace normalisation. The SU(3)³ "trace" counts triplets minus antitriplets and is not a cubic-anomaly coefficient computation.

### `particles/composite.py` — stacked multi-quark composites and β-decay ledger (P4)
**Status:** UNREGISTERED (no module-registry record) · **Findings (cited in code):** F71, F54 · **Lattice:** n/a · **Law:** n/a · **Units:** exact `Fraction`

**Does:** builds the proton ($uud$) and neutron ($udd$) as $\varepsilon_{abc}$ colour-singlet composites of left-handed quark specs, and writes the F54 β-decay conservation ledger. The colour algebra and the vertex arithmetic are delegated to audited engine modules.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $X_\text{tot}=\sum_{c}X_c$ for $X\in\{Q,B,L,T_3,Y\}$ | aggregate quantum numbers | `composite.py:L66–69 quantum_numbers()` | unknown (exact `Fraction`) |
| 2 | $Q_\text{tot}=T_{3,\text{tot}}+Y_\text{tot}/2$; $\varepsilon_{abc}$ requires exactly 3 coloured constituents | composite checks (proton: $T_3=\tfrac12,Y=1,Q=1$; neutron: $T_3=-\tfrac12,Y=1,Q=0$) | `composite.py:L48–61 __post_init__()` | unknown |
| 3 | forces $=\{\text{gravity}\}\cup\{\text{em}:Q_\text{tot}\ne0\}\cup\{\text{weak}:\text{any constituent weak}\}$, no strong | the singlet does not couple to strong at long range | `composite.py:L92–97 couples_to()` | unknown |
| 4 | $\max_a\lVert G^a\lvert S\rangle\rVert$ and $C_2(S)$ | colour-singlet residual and Casimir, delegated to `engine.particles.baryon.singlet_charge_residual`/`singlet_casimir` | `composite.py:L107, L114` | unknown (inferred: delegated (see 06a § baryon.py)) |
| 5 | $\Delta Q,\Delta B,\Delta L$ for $d\to uW^-$, $W^-\to e\bar\nu$, $d\to ue\bar\nu$ (via `charged_current.conservation_residuals`), and $n\to p\,e^-\bar\nu_e$ at composite level: $\Delta X=(X_p+X_e+X_{\bar\nu})-X_n$ | β-decay ledger, all $=0$ | `composite.py:L157–171 beta_decay_ledger()` | unknown (exact `Fraction`) |

**Inputs → outputs:** `get_composite(name)` returns a `CompositeSpec`. `beta_decay_ledger()` returns a dict of residual dicts. **Depends on:** `particles.spec`; `engine.particles.baryon` (06a); `engine.gauge.charged_current` (05b). **Flags:** UNREGISTERED. EXACTNESS unknown (#1–3, #5).

### `particles/channel.py` — particle layer: particle, composite and sourced-field engine channels
**Status:** UNREGISTERED (no module-registry record; but live, since it is imported by `casim/engine/__init__.py:L19` and registers 9 channel types and 4 observers) · **Findings (cited in code):** F27 F43 F46 F54 F62 F64 F67 F68 F69 F70 F71 F86 F91 F104 F106 F113 F122 F125 F126 F128 F133 F135(b) F137 F139 F156 F159 F160 F195 · **Lattice:** BCC for every Weyl/Dirac/gauge step; cubic spectral grid for the Schrödinger/Poisson/multigrid sectors · **Law:** per-branch (matter), **even** (`photon_sourced`, `gluon_sourced`), `non-rel`/`dielectric`/`multigrid` (outside F91) · **Units:** lattice (the NN potential is in MeV/fm, scaled by config)

**Does:** wiring layer that puts typed `ParticleSpec` wavepackets on the BCC lattice as engine channels. It closes the em/weak/strong/gravity loops by publishing currents (`J_em`, `rho_em`, `J_colour`) that the sourced-field channels read, and it hosts the real-space atom channels (U2–U4, F156/F160/F195). The module docstring says "this module is wiring, not physics". Every propagation step does call an audited engine kernel, but the currents, the confining potentials, the source kicks, the bag map, the Hartree field and the NN fit below are computed here.

Observers declare `exactness = "quantitative"` (L1179, L1245, L1526, L2068). Everything else has no registry exactness, so it is `unknown`.

**Currents and helpers**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $J^x=2\operatorname{Re}(\bar f g),\ J^y=2\operatorname{Im}(\bar f g),\ J^z=\lvert f\rvert^2-\lvert g\rvert^2$ (i.e. $\psi^\dagger\boldsymbol\sigma\psi$) | Noether U(1) Weyl vector current | `channel.py:L75–77 weyl_vector_current()` | unknown |
| 2 | $J^a_0=\sum_\text{spin}q_i^*\,T^a_{ij}\,q_j$, with $T^a=\lambda^a/2$ (`strong.T_GEN`, `strong.py:L79`) | colour-octet charge density | `channel.py:L93–94 colour_charge_density()` | unknown |
| 3 | $\bar x_\mu=\tfrac{L}{2\pi}\operatorname{atan2}\!\big(\sum w\sin\theta,\sum w\cos\theta\big)$, with $\theta=2\pi x/L$ | periodic (angular-mean) centroid | `channel.py:L107–109 _centroid()` | plumbing |
| 4 | $r_\text{rms}=\sqrt{\sum\rho\,d^2/\sum\rho}$ with minimum-image $d$ | RMS radius / separation diagnostics | `channel.py:L1205 _rms_radius()`, `L1211 _min_image_sep()` | plumbing |

**`ParticleChannel` (`particle`)**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 5 | forces requested $\subseteq\bigcup_s$ `couples_to`$(s)$; weak only on doublets; $\lvert m\rvert\le1$, and mass only on lepton singlets | build-time applicability guard | `channel.py:L147–176 __init__()` | n/a (validation) |
| 6 | $V_i(\mathbf x)=\sum_{j\ne i}\tfrac{\sigma}{2}\lvert\mathbf x-\mathbf r_j\rvert$ (pairwise Δ-string), or $V=\sigma\lvert\mathbf x-\mathbf R_\text{cm}\rvert$ (`anchor: com`, Y-string), or $V=S(\mathbf x)$ read from a `colour_bag` partner (F137) | confining string potential from the partners' start-of-tick centroids | `channel.py:L295, L305 _confine_potential()`; `L267` (bag) | unknown |
| 7 | massive Dirac singlet: $\text{Mix}_{\sqrt A}\circ\mathcal D\circ\text{Mix}_{\sqrt A}$ with $\sqrt A=K^{-1/2}$ (F62 rest-leg lapse, `gravity.lapse_mix_half`) | two-way gravity Strang wrap | `channel.py:L326–356 step()`; $\sqrt A$ at `L484 _grav_sqrtA()` | unknown |
| 8 | $\mathcal D$ = variable-mass BCC Dirac step with $m_\text{eff}(\mathbf x)=m+V_\text{conf}(\mathbf x)$ (Lorentz-scalar confinement, F135b), then $\psi\to e^{-iq\alpha}\psi$ | scalar-confined Dirac tick | `channel.py:L340–345 step()` | unknown |
| 9 | $\mathcal D=e^{+iq\alpha}\,\mathcal D_\text{BCC}(m)\,e^{-iq\alpha}$ (`minimal_coupling.u1_wrap_dirac_step_3d_bcc`), or the free `dirac_step_3d_bcc_splitstep` | U(1) Stueckelberg wrap / free Dirac tick | `channel.py:L347–352 step()` | unknown (the wrap is exactly unitary per 05c) |
| 10 | doublet: per-member $e^{-iQ\alpha}$ wrap around `weak_wmu.covariant_weyl_step_3d_bcc` with links $U=\exp(i\,\epsilon A^a\tau^a/2)$ (`coupled.su2_expmap`), all 8 BCC links equal; free `weyl_step_3d_bcc` otherwise | W-doublet covariant Weyl tick | `channel.py:L372–386 step()` | unknown |
| 11 | quark (Weyl): wrap $e^{\mp iq\alpha}$ around `minimal_coupling.su3_rotate_weyl_step_3d_bcc`$(A^a,\epsilon_s)$; optional vector kick $e^{-iV\,dt}$ | SU(3) rotate-then-step; vector confinement (the documented Klein null) | `channel.py:L388–416 step()` | unknown |
| 12 | Weyl singlet: `u1_wrap_weyl_step_3d_bcc` or free `weyl_step_3d_bcc` | charged / neutral Weyl tick | `channel.py:L418–425 step()` | unknown |
| 13 | $\mathbf J_\text{em}=q\,(\mathbf J[\eta]-\mathbf J[\chi])$, $\rho_\text{em}=q\,\psi^\dagger\psi$ (Dirac); $\sum_\text{members}Q\,\mathbf J$ (doublet); $\sum_c q\,\mathbf J[f_c,g_c]$ (quark) | published EM source currents | `channel.py:L440–465 _publish_currents()` | unknown |
| 14 | $\langle\Phi\rangle=\sum\rho\,\phi/\sum\rho$; $K$ at the rounded centroid | gravity scalar readouts | `channel.py:L497–499 _grav_readout()` | unknown |
| 15 | $v=\big((\bar x_t-\bar x_{t-1}+L/2)\bmod L\big)-L/2$ | per-tick centroid velocity | `channel.py:L509 observables()` | plumbing |

**`ColourDiracQuarkChannel` (`quark_dirac`)**: a colour-triplet massive Dirac quark, 4 spinor components × 3 colours.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 16 | $\psi_c\to V_{cd}\,\psi_d$, $V=\exp(i\,\epsilon_s A^aT^a)$ (`gluon._su3_expmap_field`, eigendecomposition per site) | SU(3) colour rotation from the gluon potential | `channel.py:L621–625 step()` | unknown |
| 17 | per colour: variable-mass BCC Dirac with $m_\text{eff}=m+V_\text{conf}$ (`dt` from config), or the constant-$m$ split-step | scalar-confined kinetic tick | `channel.py:L634–641 step()` | unknown |
| 18 | $\psi\to e^{-iq\alpha}\psi$ (one-sided) | EM phase | `channel.py:L646–648 step()` | unknown |
| 19 | $J^a_\text{colour}=J^a[\eta]+J^a[\chi]$; $\mathbf J_\text{em}=q\sum_c(\mathbf J[\eta_c]-\mathbf J[\chi_c])$ | published currents | `channel.py:L659–670 _publish_currents()` | unknown |

**`NonRelElectronChannel` (`nr_electron`)**: Schrödinger orbital (F156), propagator `non-rel`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 20 | $V=q\,\phi_\text{em}$, $\phi_\text{em}=-\phi_P$ where $\nabla^2\phi_P=4\pi G\rho$ with $G=g_c/4\pi$, i.e. $\nabla^2\phi_\text{em}=-g_c\rho$ (open BC, `poisson_open`) | Coulomb well from partner `rho_em` plus an optional fixed Gaussian external charge | `channel.py:L751–752 _potential()` | unknown |
| 21 | $\psi\to e^{-iV\,dt/2}\,\mathcal F^{-1}e^{-ik^2dt/2m}\mathcal F\,e^{-iV\,dt/2}\psi$, with $k=2\pi\,\text{fftfreq}(L)$ (continuum $k^2$, cubic grid) | Strang split-step (exactly unitary in form) | `channel.py:L813–818 step()` | unknown |
| 22 | same with $dt\to-i\,d\tau$, plus renormalisation each step | imaginary-time ground-state relaxation | `channel.py:L763–773 _relax_ground_state()` | unknown |
| 23 | $\rho_\text{em}=q\lvert\psi\rvert^2$; $J_\mu=q\,\operatorname{Im}(\psi^*\partial_\mu\psi)/m$, spectral $\partial_\mu=\mathcal F^{-1}ik_\mu\mathcal F$ | published currents | `channel.py:L827–836 _publish_currents()` | unknown |

**`CompositeParticleChannel` (`composite`)**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 24 | constituent $c$ on colour $c$ (leading $\varepsilon_{abc}$ term); each propagated by free `weyl_step_3d_bcc` | structural hadron (no binding; `binding_tier: structural`) | `channel.py:L896–918` | unknown |

**Sourced gauge fields**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 25 | $(E,B)\to R(\Omega_\text{pair})(E,B)$ (`gauge.photon.photon_step_spectral`, **even** law), then $E\mathrel{+}=g_\text{em}\,\mathbf J_\text{em}\,dt$ | paired-spinor photon plus source kick (**not** σ-bilinear) | `channel.py:L985–987 PhotonSourcedChannel.step()` | unknown (the free step is exactly unitary per 05a) |
| 26 | $\alpha\mathrel{+}=\phi_\text{em}\,dt$, $\phi_\text{em}=-\phi_P[\rho;\,G=g_c/4\pi]$ | accumulated $A_0$ Wilson-line angle (Coulomb sector) | `channel.py:L999–1000` | unknown |
| 27 | `gluon.gluon_sourced_step_bcc`$(E,B,J_a=\sum J_\text{colour},dt,g_\text{lat})$ (F43, even BCC), then $A\mathrel{+}=E$ | gluon octet plus potential accumulator | `channel.py:L1040–1045 GluonSourcedChannel.step()` | unknown |
| 28 | $U=\tfrac12\sum(E^2+B^2)$ | field energy (`core.channel.field_energy`) | `channel.py:L1004, L1049` | plumbing (see 04-core.md) |

**`ColourBagChannel` (`colour_bag`)**: live colour-dielectric bag (F137/F139), propagator `dielectric`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 29 | $\rho=\sum_\text{src}\lVert J^a_\text{colour}\rVert_a$; $\phi=\max\!\big(0,\ \mathcal F^{-1}[e^{-\lambda^2k^2/2}\,\mathcal F\rho]\big)$ | octet magnitude, Gaussian-smeared by penetration depth $\lambda$ | `channel.py:L1121, L1072–1073 _gauss_smear()`, `L1155` | unknown |
| 30 | $f^2=e^{-\phi/\phi_0}$, $S=M_\text{bag}f^2$, $\varepsilon_c=1-f^2$ | mean-field bag wall mass and dielectric (F137) | `channel.py:L1156–1158 step()` | unknown |
| 31 | $f$ from `gravity_backreaction.self_consistent_bag`$(g_\text{src}\rho^a,\xi,\dots)$; $S=M_\text{bag}f^2$, $\phi=-\ln f^2$ | self-consistent dual-GL bag (F139) | `channel.py:L1138–1149 step()` | unknown (iterative, `sc_tol`) |

**`TwoGridAtomChannel` (`two_grid_atom`)**: live two-grid hydrogen (F160).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 32 | fine: 3 `quark_dirac` ($u_r,u_g,d_b$) with scalar Y-string (`anchor: com`) on an $L_f$ BCC patch | confined proton | `channel.py:L1405–1413 __init__()`, `L1468` | unknown |
| 33 | $Q=\sum\rho_\text{em}$; $V=-kQ/r$ from a **point** source at the coarse centre (`multigrid.coarse_point_potential`) | $R_b$ charge reduction onto the coarse grid | `channel.py:L1433–1438 _coarse_well()` | unknown |
| 34 | electron: `multigrid.schrodinger_step`$(\psi,V,m,1,dt)$ (same Strang form as #21) | coarse orbital tick | `channel.py:L1474 step()` | unknown |
| 35 | $a_0/r_p=r_\text{rms,e}\cdot b/r_\text{rms,p}$ | represented scale ratio | `channel.py:L1505 observables()` | plumbing |

**`ElementAtomChannel` (`element_atom`)**: general $(Z,N)$ block-spin atom (F195).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 36 | $A$ nucleon centres on a Fibonacci shell of radius `spread`; unit-normalised Gaussian blobs; first $Z$ are charged, so $\sum\rho_q=Z$ | Tier-A static nucleus | `channel.py:L1702–1709 _nucleon_offsets()`, `L1724–1733` | unknown |
| 37 | Aufbau configuration (`manybody.aufbau_configuration`) → spatial orbitals with Hund filling (singles first, then pairs), $\text{occ}\le2$ | orbital occupation | `channel.py:L1596–1615 _spatial_orbitals()` | unknown |
| 38 | $V_\text{nuc}=-kQ/r$ (point); $\nabla^2\phi=4\pi k\rho$, $V_{ee,i}=-(\phi[\rho_\text{tot}]-\phi[\lvert\psi_i\rvert^2])$, $\rho_\text{tot}=\sum\text{occ}\,\lvert\psi\rvert^2$ | nuclear well plus live Hartree (other electrons only) | `channel.py:L1868, L1885–1889 _ee_potentials()` | unknown |
| 39 | $q_i\to\big(q_i-\sum_{r<i}\langle r\lvert q_i\rangle r\big)/\lVert\cdot\rVert$ | modified Gram–Schmidt Pauli antisymmetriser | `channel.py:L1552–1557 _gram_schmidt()` | unknown |
| 40 | per tick: $\psi_i\to$ `schrodinger_step`$(\psi_i,V_\text{nuc}+V_{ee,i})$, then Gram–Schmidt every `gs_every`; Hartree refreshed every `hartree_every`; initial SCF relaxation (`schrodinger_relax`, `e_scf` rounds) | coarse many-electron tick | `channel.py:L1975–1979 step()`, `L1912–1919 _scf_relax()` | unknown |
| 41 | $V_\text{pair}(r)=V_\sigma+V_\omega+V_\text{core}-V_0\,e^{-r^2/2R_0^2}$, $R_0=\hbar c/m_\pi$; $V_0$ by 70-step bisection so $\min_b\big[\tfrac34(\hbar c)^2/(M_Nb^2)+\langle V_\text{pair}\rangle_b\big]=-\lvert E_d^\text{model}\rvert$ | model NN one-boson-exchange, depth fitted to the **model** deuteron (`manybody._model_deuteron_binding`) | `channel.py:L1775–1799 _setup_nn_potential()` | fit (to a model anchor, not data) |
| 42 | $\theta_i(\mathbf x)=g_{nn}\sum_{j\ne i}V_\text{pair}(\lvert\mathbf x-\mathbf R_j\rvert\,s)$, applied as the η↔χ scalar-mass rotation `dirac_bcc._mix_eta_chi_3d` | Tier-B inter-nucleon scalar binding | `channel.py:L1849–1855 _apply_nn_binding()` | unknown |
| 43 | Tier B: $3A$ `quark_dirac` quarks; $Q=\sum\rho_\text{em}$ refreshed each tick → $V_\text{nuc}$ | live-quark nucleus | `channel.py:L1738–1759`, `L1960–1964` | unknown |

**Inputs → outputs:** scenario YAML config goes in; channel states (spinor arrays, `J_em`/`rho_em`/`J_colour`, `alpha`, `A`, `S`) and observable dicts come out. The observers (`ParticleReadout`, `UnificationReadout`, `TwoGridReadout`, `AtomStabilityReadout`) collect RMS radii, separations, net charge and loop-liveness norms.

**Depends on:** `engine.core.channel/coupled/observers/simulation` (04-core.md); `engine.lattice.bcc`, `multigrid`, `poisson_open` (03-lattice.md); `engine.gauge.photon`, `gluon`, `strong`, `weak_wmu`, `minimal_coupling` (05a–05c); `engine.particles.dirac_bcc`, `nuclear` (06a/06b); `engine.interactions.gravity`, `gravity_backreaction` (07a); `engine.core.manybody`; `casim.constants.c_lat` $=1/\sqrt3$ (F25/F26, used only for the fine-grid `LatticeSpec`, L1418/L1861).

**Flags:**
- UNREGISTERED, even though the module is live through `engine/__init__.py:L19`. The manifest (L79) marks it as still needing its own record. Its test `tests/casim/test_particle_layer.py` is a gate-tier record.
- ⚠ DOC/CODE MISMATCH: `ElementAtomChannel.step` comment L1952 says "NN OBE force as a unitary **momentum kick**". The code it calls (`_apply_nn_binding`, docstring L1819–1833) applies a Lorentz-**scalar** mass rotation built from $V$ itself, "not a force impulse". `_nn_Vprime` (L1800) is computed but never used.
- ⚠ DOC/CODE MISMATCH: the module docstring (L4–5) says "this module is wiring, not physics". It in fact computes the confining potentials, source kicks, colour-bag map, Hartree mean field, Gram–Schmidt Pauli step and a fitted NN potential (#6, #25–#31, #36–#42).
- OTHER: `TwoGridAtomChannel._coarse_well` (L1434–1438) computes `rms_c` and then passes `src_rms_cells=min(rms_c, 0.0)`, which is always $\le0$. The source is therefore always a point, and `rms_c` is dead. This may be a typo for `max`.
- OTHER (EM coupling form): the U(1) coupling is a **two-sided** Stueckelberg wrap $e^{+iq\alpha}\mathcal D\,e^{-iq\alpha}$ on the Weyl, doublet, quark and unconfined-Dirac paths (#9–#12). On the scalar-confined Dirac path (L343–345) and in `quark_dirac` (L646–648) it is a **one-sided** phase $e^{-iq\alpha}$ applied every tick with the *accumulated* $\alpha=\sum\phi_\text{em}dt$ (#26). These are different couplings, and the one-sided form re-applies the whole accumulated angle every tick. This needs a physics review; the code was not changed.
- OTHER (sign/normalisation): the photon source kick is $E\mathrel{+}=g\,J\,dt$ (L987), the opposite sign to Ampère's $\partial_tE=\nabla\times B-J$ in the usual convention. $B$ is not kicked, and Gauss's law is not enforced. Coulomb normalisations also differ between channels: $\nabla^2\phi_\text{em}=-g_c\rho$ in `photon_sourced`/`nr_electron`, versus Gaussian $\nabla^2\phi=4\pi k\rho$ in `element_atom`. `gluon_sourced` accumulates $A\mathrel{+}=E$ without a $dt$.
- OTHER: the code cites "F135" for scalar confinement. The file is `F135b-realspace-scalar-confinement.md`, while `F135-…` is the block-spin wavepacket finding.
- OTHER: `ParticleChannel` passes no `dt` to `dirac_step_3d_bcc_varm_splitstep` (L341), whereas `quark_dirac` passes `confine.dt` (L637). The same confinement config therefore gives different step sizes in the two channels.
- OTHER (D8): the module uses `np.einsum`, `np.vdot`, `np.gradient`, `np.interp` and direct numpy array code. FFTs do route through `casim.numerics.fft`.
- EXACTNESS unknown for #1–#34 and #36–#43 (registry silent; the observers self-declare quantitative).
