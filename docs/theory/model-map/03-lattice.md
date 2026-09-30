# 03 — Lattice sector (`src/casim/engine/lattice/`)

*Model-map section p03, written 2026-09-28 - 00:00. Source of truth is the code; every equation is cited to `file.py:L<n> function()`.*

**Scope.** Every `.py` in `src/casim/engine/lattice/`. This covers the canonical BCC base layer (`bcc.py`, D1): its Weyl walk update rule, the dispersion $\cos\omega=u$, the unit convention and $c_\text{lat}$. It also covers the real-space BCC geometry and Brillouin zone (`geometry.py`); the **D1 reference implementations** (the simple-cubic and square-lattice cores `core.py`, `core_exact.py`, `curved.py`, and `LatticeConfig.cubic()/square()`); the block-spin RG family; the open-boundary Poisson and multigrid helpers; the lattice↔SI map (`si_scale.py`); and the dimension and time-signature derivation modules (F291/F292/F313/F315/F316/F326/F377/F400).

**Conventions shared by the batch.**

- **Two length units for one crystal.** This is the most important thing to know when reading anything below.
  - **(W) the walk/FFT convention.** `bcc.py` and every walk consumer use this one. The array is an ordinary cubic FFT grid with $k_i\in(-\pi,\pi]$. The walk's trig arguments are $k_i/\sqrt3=k_i\,c_\text{lat}$, so one hop is the translation $\mathbf d/\sqrt3$ with $\lvert\mathbf d/\sqrt3\rvert=1$ (`bcc.py:L227 bcc_fractional_shift()`). In these units the conventional cube edge is $a=2c_\text{lat}=2/\sqrt3$ (F278, `bcc.py:L385`). The walk's $k$-periodicity lattice is $\sqrt3\times$fcc (F267). The FFT cube is *not* a fundamental domain, so an array step is **not** a lattice hop, and the stepper is a band-limited fractional translation (F267 S5).
  - **(G) the gauge/geometry convention.** `geometry.py` (F265) uses this one. The conventional cube side is 2, a hop is the integer vector $\mathbf d\in\{\pm1\}^3$, and `np.roll` by $\mathbf d$ is exact. The reciprocal lattice is fcc $\pi(1,1,0),\dots$, and the cube $(-\pi,\pi]^3$ holds exactly 4 BZ copies.
  - (W) and (G) are the same lattice at a $\sqrt3$ change of length unit. Only (G) makes array sites into lattice sites.
- **Lattice vs SI.** Everything is in lattice units (cells, ticks) except `si_scale.py`, which is the only lattice→SI map in this directory.
- **Even vs chiral law (F91).** The lattice layer supplies the fermion walk $A^\pm(\mathbf k)$, which is **per-branch (chiral)**: '+' and '−' are the two BDPT helicity branches, related by $\omega^+(-\mathbf k)=\omega^-(\mathbf k)$. The even photon law $\Omega=2\omega(k/2)$ is *consumed* (by `blockspin.py`, via `gauge.photon.pair_dispersion` and `gauge.weak_wmu._f26_rotation_step`), never defined here. See 05a-gauge.
- **Sign convention of the update.** The engine walk is $A=u\,\mathbb I-i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}$, with eigenvalue $e^{-i\omega}$ on the $\hat{\mathbf n}\cdot\boldsymbol\sigma=+1$ eigenspinor. `cell_internal_index.walk()` uses the conjugate sign $u\,\mathbb I+i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}$ (flagged).
- **Constants.** $c_\text{lat}=1/\sqrt3$ (F26, exact), $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107, exact).
- **Hazards checked.**
  - No module here builds the photon from the σ-bilinear.
  - Two modules put chiral 2×2 unitaries through `numpy.linalg.eig`: `bcc.measure_bcc_dispersion` (verifier only) and `time_generator_axiom_independence._gaussian_wavepacket` (flagged).
  - `blockspin.block_average` keeps the imaginary part (C3 fix).

**Modules covered (23 + `__init__`).** `__init__`, `bcc`, `bcc_point_symmetry`, `blockspin`, `blockspin_baryon`, `blockspin_binding`, `blockspin_dynamical`, `cell_internal_index`, `coordination_selector`, `core`, `core_exact`, `curved`, `derive_walk_bz_measure`, `dimensionality`, `geometry`, `laurent_pell`, `multigrid`, `poisson_open`, `si_scale`, `time_generator_axiom_independence`, `time_signature`, `time_signature_interacting`, `time_single_generator`, `wavepacket`.

---

### `engine/lattice/__init__.py` — package docstring
**Status:** n/a (not a registry row) · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

Package docstring only. It states that BCC is canonical and the cubic code is the continuum-limit regression target (D1). There are no equations.

---

### `engine/lattice/bcc.py` — canonical BCC Weyl QCA (base layer, D1)
**Status:** live · driven (29 ch) · **Findings:** (none in registry; F1, F26, F267, F278 by content) · **Lattice:** BCC, convention (W) · **Law:** per-branch Weyl walk ($\pm$ = chirality); input to both F91 classes · **Units:** lattice (cells, ticks)

**Does:** defines the single-tick unitary of the BDPT Weyl QCA (Paper 1 Eq. 15, $n_y$ sign-corrected) and applies it diagonally in Fourier space. It is the update rule every fermion and photon kernel is built on.

Notation: $c_i=\cos(k_i/\sqrt3)$, $s_i=\sin(k_i/\sqrt3)$ (argument $k_i\,c_\text{lat}$, `bcc.py:L89–90`), and $s=\pm1$ for sign '±'.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u^\pm=c_xc_yc_z\pm s_xs_ys_z$ | scalar part of the walk | `bcc.py:L107 _bcc_uvec()` | unknown (inferred: exact) |
| 2 | $\tilde n_x=s_xc_yc_z\mp c_xs_ys_z,\ \tilde n_y=\mp c_xs_yc_z+s_xc_ys_z,\ \tilde n_z=c_xc_ys_z\pm s_xs_yc_z$ | Bloch vector ($\tilde n_y$ second-term sign corrected vs the transcribed paper) | `bcc.py:L108–110 _bcc_uvec()` | unknown (inferred: exact) |
| 3 | $u^2+\lvert\tilde{\mathbf n}\rvert^2=1$ | unitarity identity (inventory #1: $4.4\times10^{-16}$) | implied by L107–110; checked `bcc.py:L289 bcc_unitarity_residual()` | unknown (inferred: exact) |
| 4 | $U^\pm(\mathbf k)=u\,\mathbb I-i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}=\begin{pmatrix}u-i\tilde n_z & -i(\tilde n_x-i\tilde n_y)\\ -i(\tilde n_x+i\tilde n_y) & u+i\tilde n_z\end{pmatrix}$ | the 2×2 per-mode update | `bcc.py:L168–171 bcc_unitary()` | unknown (inferred: exact) |
| 5 | $\cos\omega^\pm(\mathbf k)=u^\pm(\mathbf k)$, i.e. $\omega^\pm=\arccos(c_xc_yc_z\pm s_xs_ys_z)$ | dispersion (eigenphases $e^{\mp i\omega}$) | `bcc.py:L122 bcc_dispersion()` | unknown (inferred: exact) |
| 6 | $\omega^+(-\mathbf k)=\omega^-(\mathbf k)$ | branch exchange under $\mathbf k\to-\mathbf k$ (docstring L48; follows from L107) | `bcc.py:L107` | unknown (inferred: exact) |
| 7 | $\hat{\mathbf n}=\tilde{\mathbf n}/\sin\omega,\ \sin\omega=\sqrt{1-u^2}$; $\hat{\mathbf n}(0):=\hat z$ | spin (Bloch) axis; $(\hat{\mathbf n}\cdot\boldsymbol\sigma)\psi_+=\psi_+$ | `bcc.py:L147–153 bcc_spin_axis()` | unknown (inferred: exact) |
| 8 | $\psi_{t+1}=\mathcal F^{-1}\,U^\pm(\mathbf k)\,\mathcal F\,\psi_t$ on $(f,g)$ | **the update rule, one tick** (U cached per shape/sign) | `bcc.py:L263–269 weyl_step_3d_bcc()` | machine (FFT floor; inventory: norm drift $3.7\times10^{-14}$/200 steps) |
| 9 | $\tilde f(\mathbf k)\mapsto\tilde f(\mathbf k)\,e^{i(\mathbf d\cdot\mathbf k)/\sqrt3}$, $\mathbf d\in\{\pm1\}^3$ | BCC hop as a fractional shift by $\mathbf d/\sqrt3$ | `bcc.py:L227 bcc_fractional_shift()` | unknown (inferred: exact (symbol)) |
| 10 | $\omega\to c_\text{lat}\lvert\mathbf k\rvert,\ c_\text{lat}=1/\sqrt3$; relative residual $O(k^2)$ | small-$k$ Weyl limit $H_W=c_\text{lat}\,\boldsymbol\sigma\cdot\mathbf k$ | `bcc.py:L500–501 bcc_smallk_to_weyl_residual()` | unknown (inferred: exact (limit); residual quantitative) |
| 11 | $U(\mathbf 0)=\mathbb I$ | Paper-2 V7 check | `bcc.py:L302 bcc_a0_check()` | unknown (inferred: exact) |
| 12 | $a=2c_\text{lat}=2/\sqrt3$; $\lvert(a/2)(1,1,1)\rvert=1$; $V_\text{prim}=a^3/2=4\sqrt3/9=4/(3\sqrt3)$; $V_\text{cube}/V_\text{BZ}=a^3/2$; $4\pi/a=2\pi\sqrt3$; $2\pi/a=\pi\sqrt3$ (Γ–H); $\omega^\pm(\pi\sqrt3,0,0)=\pi$ | F278 crystal identities: cube edge and reciprocal period | `bcc.py:L385–465 check_lattice_constant_identities()` | unknown (inferred: exact (sympy, checks 3–7); check 8 at 1 ulp) |

**Constants:** $c_\text{lat}=1/\sqrt3$ (F26) is the trig argument scale and `BCC_C` (`bcc.py:L78`).
**Inputs → outputs:** $(f,g)$ complex128 $L^3$ arrays and sign → updated spinors; analytic $u,\tilde{\mathbf n},\omega,\hat{\mathbf n}$ at any $\mathbf k$.
**Depends on:** `geometry.make_kgrid_3d` (below); `casim.numerics.fft` (02-numerics).
**Plumbing:** `_weyl_cache` (per-shape unitary cache, L68, L257–261); `measure_bcc_dispersion` (L306–336, eig-based verifier; `L`, `n_steps` unused); `bcc_norm_drift_test` (L339).

**Flags:**
- ⚠ DOC/CODE MISMATCH, L52: the docstring lists `weyl_step_3d_bcc(f, g, c=1.0/√3, sign='+')`, but the signature at L235 has no `c`.
- ⚠ DOC/CODE MISMATCH, L137–140: the continuum limit $\hat{\mathbf n}\to(k_x,-k_y,k_z)/\lvert k\rvert$ holds only for sign '+'. For '−' the code gives $(k_x,+k_y,k_z)/\lvert k\rvert$ (spot-checked).
- OTHER: the FFT-grid symbol $U(\mathbf k)$ is not $2\pi$-periodic on the grid. Shifting $k_x$ by $2\pi$ changes $U$ by 1.41 (spot-checked), while it *is* invariant under $\sqrt3\pi(1,1,0)$ to $3\times10^{-16}$. So `weyl_step_3d_bcc` is the band-limited fractional walk of F267, not a nearest-neighbour hop on the array.
- OTHER: `measure_bcc_dispersion` calls `np.linalg.eig` on a chiral 2×2 (CLAUDE.md hazard). This is a verifier only.
- OTHER: the registry row carries no findings and no exactness.

---

### `engine/lattice/bcc_point_symmetry.py` — exact point-group covariance of the BCC walk (F344)
**Status:** live · standalone · **Findings:** F344 F26 F30 F291 F302 F342 · **Lattice:** BCC (W) · **Law:** per-branch walk; branch label allowed to move under $g$ · **Units:** n/a (integer algebra on $\{c,s\}^3$ monomials)

**Does:** decides which elements of $O_h$ leave the shipped walk covariant, $A(g\mathbf k)=U(g)A(\mathbf k)U(g)^\dagger$, using exact integer monomial arithmetic.

Notation: $M1_a$ has $s$ in slot $a$ and $c$ elsewhere ($T_{1u}$, $O(k)$); $M2_a$ has $c$ in slot $a$ and $s$ elsewhere ($T_{2g}$, $O(k^2)$).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u^s=c_xc_yc_z+s\,s_xs_ys_z,\quad \tilde n_a=p_a M1_a+q_a M2_a$; shipped $p=(+1,-s,+1),\ q=(-s,+1,+s)$ | the walk as sign-coefficient polynomials (read off `_bcc_uvec`) | `bcc_point_symmetry.py:L78–79, L89–95 _poly_walk()` | exact (reg) |
| 2 | unitarity $\iff \sum_a p_aq_a=-s$ on both branches | cross-term condition, given unit coefficients | `bcc_point_symmetry.py:L103 is_unitary()` | exact (reg) |
| 3 | rank of the 8 squared monomials in the $x_i=c_i^2$ basis $=8$ ⇒ every coefficient has modulus 1 | C1 | `bcc_point_symmetry.py:L221–257 _unit_coefficient_rank()` | exact (reg) |
| 4 | $u^s(g\mathbf k)=u^{\,s\prod_i\varepsilon_i(g)}(\mathbf k)$; 24 of 48 elements swap branch | C2 branch map | `bcc_point_symmetry.py:L305–317` | exact (reg) |
| 5 | $\tilde{\mathbf n}^s(g\mathbf k)=R\,\tilde{\mathbf n}^{\tau_g(s)}(\mathbf k)$ solvable for $R$ ⇔ $g\in L$; shipped $L=D_{4h}$, $\lvert L\rvert=16$, axis $z$ | C3 covariance group | `bcc_point_symmetry.py:L181–206 covariance_R()`, L322–331 | exact (reg) |
| 6 | $\ker(g\mapsto\det R)=D_{2h}$, order 8 | C4 unitarily implementable subgroup | `bcc_point_symmetry.py:L334–337` | exact (reg) |
| 7 | none of the 576 unitary sign conventions admits a body-diagonal $C_3$; $\max\lvert L\rvert=16$ | C5 exhaustive sweep | `bcc_point_symmetry.py:L341–356` | exact (reg) |
| 8 | $\tilde n_x(C_3\mathbf k)-\tilde n_z(\mathbf k)=(q_x-q_z)M2_z=-2s\,s_xs_yc_z$ | C6 closed-form defect, $O(k^2)$ | `bcc_point_symmetry.py:L359–369` | exact (reg) |
| 9 | the $O(k)$ truncation (drop $M2$) is covariant under all 48 | C7: $O_h$ is an exact IR symmetry | `bcc_point_symmetry.py:L372–374` | exact (reg) |
| 10 | shipped-code residual on $L$ $<10^{-12}$; $C_3$ floor ratio at $k=0.1/0.01$ in $(8,12.5)$ | C8 float cross-check | `bcc_point_symmetry.py:L377–411` | machine (reg: exact; row is weaker — see flags) |

**Depends on:** `bcc._bcc_uvec` (above).
**Flags:**
- OTHER: F344 finds the shipped walk's exact symmetry is $D_{4h}$, with $O_h$ only in the IR. This bears on any map text (e.g. F75, CLAUDE.md) that calls the walk $O_h$-symmetric. It is a cross-reference for other sections and is not settled here.

---

### `engine/lattice/blockspin.py` — block-spin RG $R_b$, gauge + gravity (F130)
**Status:** live · test-only · **Findings:** (none in registry; F129, F130, F110, F64, F106 by content) · **Lattice:** generic hypercubic $L^d$ blocking (reference geometry). The dispersion input is the BCC even-law photon · **Law:** consumes the **even** law (`pair_dispersion`, `_f26_rotation_step`) · **Units:** lattice (coarse spacing $b$)

**Does:** Kadanoff block averaging and its consequences. $c_\text{lat}$ is an RG fixed point, LIV operators are irrelevant, Gauss's law telescopes, the dielectric is blocked in $\ln K$, and confinement is the relevant direction.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $(R_bf)(X)=b^{-d}\sum_{r\in[0,b)^d}f(bX+r)$ (complex kept) | block average | `blockspin.py:L145–147 block_average()` | unknown (inferred: exact) |
| 2 | $D_b(k)=\dfrac{\sin(bk/2)}{b\sin(k/2)},\ D_b(0)=1$; same-grid blur $\prod_iD_b(k_i)$ | Fourier form factor of the centred box | `blockspin.py:L158–163 block_kernel_factor()`; `L177–181 box_blur_fourier()` | unknown (inferred: exact) |
| 3 | $\Omega_\text{coarse}(\boldsymbol\kappa)=\Omega(\boldsymbol\kappa/b)$ | coarse rule in coarse units | `blockspin.py:L194 coarse_dispersion()` | unknown (inferred: exact) |
| 4 | $\Omega/\lvert\kappa\rvert=c\,(1+g_2\kappa^2+g_4\kappa^4)$, least squares on $\kappa\in[k_\max/n,k_\max]$ | speed and LIV coefficients | `blockspin.py:L214–222 fit_dispersion_coeffs()` | unknown (inferred: quantitative (fit)) |
| 5 | $\lambda_n=g_n^{(b)}/g_n=b^{-n}$ (matched sampling) | T2 LIV irrelevance; docstring body-diagonal $g_2=-1/162$ (F30) | `blockspin.py:L250–259 rg_eigenvalue()` | exact (inventory F129-A/188); fit floor machine |
| 6 | $c_\text{phys}=b\cdot c_\text{coarse}(b)=c_\text{lat}$ | T1 fixed point | `blockspin.py:L266 c_lat_fixed_point()` | exact (inventory #188) |
| 7 | $(\nabla\!\cdot\!E)(x)=\sum_a[E_a(x)-E_a(x-\hat e_a)]$; coarse $E$ = sum of $b^{d-1}$ fine face links; $\nabla_c\!\cdot\!E_c=\sum_\text{block}\nabla\!\cdot\!E$ | T3a Gauss law survives blocking | `blockspin.py:L291, L295–332, L345, L355–359` | unknown (inferred: exact (integer telescoping)) |
| 8 | $u=\tfrac12\ln K$, blocked as $R_bu$; $K=e^{2u},\ A=1/K,\ B=K$, so $AB\equiv1$ | T3b reciprocal lock under blocking | `blockspin.py:L370, L376–377, L389–390` | unknown (inferred: exact) |
| 9 | Jensen gap $R_b(e^{2u})-e^{2R_bu}\ge0$ | wrong-variable discriminator | `blockspin.py:L406–411 dielectric_jensen_gap()` | unknown (inferred: exact (sign)) |
| 10 | $\max\lvert b^{-2}\nabla^2_c(R_bu)-R_b(\nabla^2u)\rvert$ | Poisson form invariance, $O((ka)^2)$ | `blockspin.py:L429–433 poisson_form_invariance_residual()` | unknown (inferred: quantitative) |
| 11 | $[R_b,R(\Omega)]=0$ per mode | T3c: blocking cannot mix F91 classes | `blockspin.py:L461–470 even_rotation_commutator()` | unknown (inferred: machine) |
| 12 | $\hat\sigma=g^2/2$ ($\lambda=0$); $g^2_\text{coarse}=b\,g^2$; $\lambda_\sigma=b$ | C1 confinement is relevant | `blockspin.py:L488, L497, L505` | unknown (inferred: exact) |
| 13 | $V_\text{coarse}(R_c)$ at $g_c^2=bg^2$ vs $V_\text{fine}(bR_c)$; $r(\lambda)=[\hat\sigma(0)-\hat\sigma(\lambda)]/\hat\sigma(0)$ | coarse F110 static potential; magnetic deformation | `blockspin.py:L531–537, L557–564` | unknown (inferred: quantitative) |

**Depends on:** `bcc.bcc_dispersion`, `gauge.photon.pair_dispersion`, `gauge.weak_wmu._f26_rotation_step` (05a/05b), `interactions.gravity.lap_nd` (07), `gauge.link_hamiltonian` (05).
**Flags:**
- OTHER: #8–#10 use the exponential dielectric $K=e^{2u}$ and the F106 energy-only Poisson law. Under decision 4 / F178 that law is the static weak-field reduction, so these results hold for that regime only (not SUPERSEDED, but reclassified).
- ⚠ DOC/CODE MISMATCH (minor): the docstring (L447) says `ca_wmu._f26_rotation_step`, while the code imports `casim.engine.gauge.weak_wmu._f26_rotation_step`. Only the name is stale.
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown: #7–#13 are unregistered; the tags above are from the inventory and the construction.

---

### `engine/lattice/blockspin_baryon.py` — coarse-grainable hyperradial baryon (F140)
**Status:** live · test-only · **Findings:** (none in registry; F140, F122, F130, F132) · **Lattice:** 1-D hyperradial finite-difference grid · **Law:** n/a (non-relativistic) · **Units:** model units ($m=\sigma=1$)

**Does:** reduces the three-quark $K=0$ hyperspherical problem to a 1-D radial equation with a linear potential, then coarse-grains it by grid decimation.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $-\tfrac1{2m}u''+\tfrac1{2m}\tfrac{15/4}{\rho^2}u+C\sigma\rho\,u=Eu$, with $u(0)=u(\infty)=0$; 3-point $D_2$ on $h=R_\max/(N+1)$ | hyperradial Hamiltonian, lowest eigenpair | `blockspin_baryon.py:L91–104 hyperradial_baryon()` | unknown (inferred: quantitative (FD)) |
| 2 | $\langle\lvert\hat n\cdot\hat e\rvert\rangle_{S^5}=16/(15\pi)$; $C_\sigma=3\sqrt2\cdot16/(15\pi)=16\sqrt2/(5\pi)$; centrifugal $15/4=(d-1)(d-3)/4$ at $d=6$ | hyperangular constants | `blockspin_baryon.py:L63–65` | unknown (inferred: exact (checked: $\Gamma(3)/(\sqrt\pi\,\Gamma(7/2))=16/15\pi$)) |
| 3 | $C_\text{eff}=\kappa C_\sigma,\ \kappa=2.0006$ | calibration to the ECG baryon | `blockspin_baryon.py:L69, L93` | unknown (inferred: **fit**) |
| 4 | $\kappa=(E_\text{ECG}/E_{K=0})^{3/2}$ | how $\kappa$ is obtained | `blockspin_baryon.py:L117 calibrate_to_ecg()` | fit |
| 5 | optional $-\tfrac{2\alpha_s}{3}\cdot3/\sqrt{\rho^2+h^2}$ | regularised OGE (off by default) | `blockspin_baryon.py:L101` | unknown |
| 6 | slope of $\ln E$ vs $\ln\sigma$ ($=2/3$ virial) | confinement scaling | `blockspin_baryon.py:L124 baryon_confinement_scaling()` | unknown (inferred: quantitative) |
| 7 | fine $N$ vs coarse $N/b$ (i.e. $h\to bh$): $E$, rms, overlap | $R_b$ = decimation | `blockspin_baryon.py:L141–156 baryon_coarse_grain()` | unknown (inferred: quantitative) |

**Depends on:** `particles.baryon_dynamics` (06).
**Flags:**
- OTHER: `BARYON_ADIABATIC_CAL = 2.0006` is a hard-coded fitted literal. It is not registered as a constant or as a `MeasuredConstant`.
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown: registry says nothing (tags above are construction-based).

---

### `engine/lattice/blockspin_binding.py` — coarse-grained bound state reproduces fine spectrum (F131)
**Status:** live · test-only · **Findings:** (none in registry; F131) · **Lattice:** simple cubic $L^d$ (`lap_nd` 2d+1 stencil). This is reference geometry, not BCC · **Law:** n/a (Schrödinger) · **Units:** fine-lattice units

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $V=\tfrac12kr^2$; $V=-\alpha/\sqrt{r^2+\text{soft}^2}$ on centred periodic coordinates | test potentials | `blockspin_binding.py:L81, L89` | unknown (inferred: exact) |
| 2 | $\nabla^2$: $-2d$ on the diagonal, $+1$ to each of the $2d$ neighbours (periodic) | sparse Laplacian | `blockspin_binding.py:L95–114 laplacian_sparse()` | unknown (inferred: exact) |
| 3 | $H=-\tfrac1{2m}\nabla^2/a^2+\mathrm{diag}(V)$, Lanczos lowest $n$ | bound states | `blockspin_binding.py:L126–131 solve_bound_states()` | unknown (inferred: quantitative) |
| 4 | $H_\text{coarse}=-\tfrac1{2m}\nabla^2_c/b^2+\mathrm{diag}(R_bV)$; compare $E_n$, $\lvert\langle R_b\psi_f\mid\psi_c\rangle\rvert$ | B1–B3: RG commutes with binding | `blockspin_binding.py:L156–169 coarse_grain_spectrum()` | quantitative (inventory F131-B) |
| 5 | $E_N=\omega(N+d/2),\ \omega=\sqrt{k/m}$ | continuum oscillator target (B4) | `blockspin_binding.py:L186–187` | unknown (inferred: exact) |

**Flags:**
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown.

---

### `engine/lattice/blockspin_dynamical.py` — coarse-graining the pion, deuteron and baryon (F132)
**Status:** live · test-only · **Findings:** (none in registry; F132, F74, F103, F104, F122) · **Lattice:** simple-cubic tight binding (6 neighbours). This is reference geometry, not BCC · **Law:** n/a · **Units:** hopping $t$

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $g_c=2t/W_3$, $W_3=0.5054620197$ | Watson contact-binding threshold | `blockspin_dynamical.py:L58, L78 watson_gc()` | unknown (inferred: exact form; $W_3$ literal external) |
| 2 | $H=6t\,\delta_{ij}-t\sum_\text{nn}-g\,\delta_{x,0}$ | relative-coordinate contact Hamiltonian | `blockspin_dynamical.py:L81–101 _contact_H()` | unknown (inferred: exact) |
| 3 | $t_c=t/b^2$; predicted $g_c^\text{pred}=(g/g_c(t))\,g_c(t_c)$; exact $g_c$ by `brentq` on $E_b$ | relevant contact coupling runs | `blockspin_dynamical.py:L142–157 contact_coarse_grain()` | unknown (inferred: quantitative) |
| 4 | deuteron at $N$ vs $N/b$ (fixed OBE couplings) | irrelevant smooth potential | `blockspin_dynamical.py:L195–207` | unknown (inferred: quantitative) |
| 5 | slope of $\ln E_\text{rel}$ vs $\ln\sigma$ ($\to2/3$); $E=3\sqrt{3k/m}$ harmonic check | baryon as string scale; ECG validation | `blockspin_dynamical.py:L223–238` | unknown (inferred: quantitative / machine) |

**Depends on:** `particles.nuclear`, `particles.baryon_dynamics` (06).
**Flags:**
- OTHER (D7): `WATSON3 = 0.5054620197` (L58) is an unregistered literal.
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown.

---

### `engine/lattice/cell_internal_index.py` — can the cell carry an internal index? (F318)
**Status:** live · standalone · **Findings:** F318 F317 F291 F313 F315 F289 F122 · **Lattice:** BCC (W), Bloch vector re-typed · **Law:** massless Dirac cell = diag($A_+$, $A_-$) · **Units:** n/a

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | Jordan–Wigner: $2k+1$ anticommuting traceless Hermitian generators on $\mathbb C^{2^k}$ | naive Clifford bound on the cell (A1/A2) | `cell_internal_index.py:L124–135 clifford_generators()` | machine (residuals $<10^{-12}$) (reg: exact; row is weaker — see flags) |
| 2 | $W=\mathrm{diag}\big(u^+\mathbb I+i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}^+,\ u^-\mathbb I+i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}^-\big)\otimes\mathbb 1_N$, with $u,\tilde{\mathbf n}$ as `bcc.py` #1–2 | hop on branch ⊗ spin ⊗ internal | `cell_internal_index.py:L170–183 _bloch(),_u()`; `L196–213 walk()` | exact (reg) |
| 3 | $T=(M-M^\dagger)/2i-\mathrm{tr}/d$; real-span rank by SVD over 7 probe $k$ | traceless span of the hop (B1–B3: span 3/6/6; anticommuting rank 3) | `cell_internal_index.py:L216–244`, `L287–306` | machine (reg: exact; row is weaker — see flags) |
| 4 | $A=\sqrt{1-\lvert n\rvert^2}\,\mathbb I+i\sum_a n_a\Gamma_a$ (5 Γ's on $\mathbb C^4$); $J=\mathrm{diag}(1/\sqrt d)$; selector returns $d=5$ | B4 converse | `cell_internal_index.py:L322–347` | exact (reg) |
| 5 | $\dim\{B:[B,W]=0\}$ via $\ker(W\otimes\mathbb I-\mathbb I\otimes W^T)$ | commutant, factor $N^2$ (C1) | `cell_internal_index.py:L353–379` | machine (reg: exact; row is weaker — see flags) |
| 6 | $\max\lvert\Delta\arg\mathrm{eig}\rvert/h$ | clock ⇔ dispersive commuting element (C2) | `cell_internal_index.py:L382–420` | machine (reg: exact; row is weaker — see flags) |
| 7 | $\mathrm{rank}\,\mathcal A_n$ on $(\mathbb C^{2N})^{\otimes n}$ $=\binom{2N}{n}$ | Fermi occupancy cap; $N{=}1$ ⇒ at most 2 (D1–D2) | `cell_internal_index.py:L439–476` | exact (reg) |

**Flags:**
- OTHER (sign convention): `walk()` uses $u\,\mathbb I+i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}$, the adjoint of the engine's $u\,\mathbb I-i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}$. Ranks and commutants are unaffected.
- OTHER (D7): `_bloch`/`_u` re-type the walk with `math.sqrt(3.0)` instead of importing $c_\text{lat}$ or `bcc._bcc_uvec`.

---

### `engine/lattice/coordination_selector.py` — why BCC, not diamond-cubic (F400)
**Status:** live · standalone (1 reachable-from) · **Findings:** F400 · **Lattice:** BCC shell vs diamond (convention G integer vectors) · **Law:** n/a · **Units:** n/a (exact integer/rational)

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | shell $=\{\pm1\}^3$; $T_\pm=\{v:\ v_xv_yv_z=\pm1\}$ | dual-tetrahedron split | `coordination_selector.py:L117, L127–128` | exact (reg) |
| 2 | $G_{jk}=v_j\cdot v_k$; $T_+$ Gram $=4\delta_{jk}-1$ (diag 3, off −1) | regular simplex test | `coordination_selector.py:L132–153` | exact (reg) |
| 3 | $T_+=\{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)\}$ = diamond bonds (units $a/4$) | geometric coincidence | `coordination_selector.py:L168, L180` | exact (reg) |
| 4 | $v\in$ FCC ⇔ $M^{-1}v\in\mathbb Z^3$, with $M=[(0,\tfrac12,\tfrac12),(\tfrac12,0,\tfrac12),(\tfrac12,\tfrac12,0)]$; basis $\{0,(\tfrac14)^3\}$ shifted by $(\tfrac14)^3$ does not return | diamond is not Bravais | `coordination_selector.py:L209–259` | exact (reg) |
| 5 | selectors take no lattice argument (signature introspection) | S1/S2/S3 are coordination-blind | `coordination_selector.py:L271–296` | exact (reg) |

**Flags:** none.

---

### `engine/lattice/core.py` — simple-cubic/square Weyl core (**D1 reference implementation**)
**Status:** live · driven (29 ch) · **Findings:** (none in registry) · **Lattice:** square (2-D) / simple cubic (3-D), **reference implementation, continuum-limit regression target, not canonical (D1)** · **Law:** continuum Weyl ($\omega=c\lvert\mathbf k\rvert$), no BCC structure · **Units:** lattice; `c` = per-tick rotation magnitude `c_unitary` (not $c_\text{lat}$)

**Does:** the notebook-era scalar-wave and Weyl CA (pp. 37–39). It provides explicit-Euler (pedagogical, unstable) and exact split-step steppers, plus CFL, reversibility and dispersion/group-velocity verifiers.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $f^{t+1}=2f^t-f^{t-1}+c^2\nabla^2_{(4)}f^t$ (4-neighbour Laplacian) | 2-D scalar wave CA; docstring CFL $c\le1/\sqrt2$ | `core.py:L39–42 scalar_step_2d()` | unknown |
| 2 | $f'=f+c(-\delta_xg+i\,\delta_yg)$, $g'=g+c(-\delta_xf-i\,\delta_yf)$, with $\delta_x h=h_{x+1}-h_{x-1}$ | explicit-Euler 2-D Weyl (**PEDAGOGICAL, unconditionally unstable**) | `core.py:L98–99 weyl_step_2d()` | unknown |
| 3 | $f'=f+c(-\delta_zf-\delta_xg+i\,\delta_yg)$, $g'=g+c(-\delta_xf-i\,\delta_yf+\delta_zg)$ | explicit-Euler 3-D Weyl of $\partial_t\psi=-\boldsymbol\sigma\cdot\nabla\psi$ (pedagogical) | `core.py:L131–132 weyl_step_3d()` | unknown |
| 4 | $U(\mathbf k)=\cos(c\kappa)\,\mathbb I-i\,\frac{\sin(c\kappa)}{\kappa}\,\boldsymbol\sigma\cdot\mathbf k$ with $\kappa=\lvert\mathbf k\rvert$ ($k_z=0$ in 2-D; sinc → $c$ at $\kappa=0$) | exact split-step: $U=e^{-ic\,\boldsymbol\sigma\cdot\mathbf k}$ | `core.py:L239–248 weyl_step_2d_splitstep()`; `L284–298 weyl_step_3d_splitstep()` | unknown (inferred: machine (docstring $\lvert\Delta\omega\rvert\approx5\text{–}8\times10^{-17}$)) |
| 5 | $\omega=c\,\kappa$ (linear, not periodic in $k$) | dispersion implied by #4 | `core.py:L483, L532 verify_dispersion_*()` | unknown (inferred: exact (by construction)) |
| 6 | $\mathbf v_g=c\,\hat{\mathbf k}$ | analytic group velocity compared to a centroid fit | `core.py:L629 measure_group_velocity_2d()` | unknown (inferred: quantitative (fit)) |
| 7 | $h_+=(\cos\tfrac\theta2,\ \sin\tfrac\theta2 e^{i\varphi})$ | $+$ eigenvector of $\boldsymbol\sigma\cdot\mathbf k$ | `core.py:L436–440 _helicity_plus_eigenvector()` | unknown (inferred: exact) |
| 8 | $\lVert\psi_{2n}(c,-c)-\psi_0\rVert/\lVert\psi_0\rVert$ | time reversal by $c\to-c$ | `core.py:L400–401 run_and_reverse()` | unknown (inferred: machine) |

**Inputs → outputs:** $(f,g)$ plus `c` → updated spinors; sweep and verification dicts.
**Plumbing:** Gaussian initial conditions (L140–181), `cfl_sweep`, `norm_over_time`, `size_sweep_*`.
**Depends on:** `casim.numerics.fft`; raw `np.fft.fftfreq` (permitted index arithmetic).

**Flags:**
- OTHER: #4 is the continuum propagator sampled on the grid. It is not a lattice QCA (it is non-periodic in $k$); `core_exact.py` is the square-lattice QCA.
- OTHER: `c` here is `c_unitary` (default 0.5), not $c_\text{lat}$. The name is overloaded, and the docstring (L196–206) says so.
- EXACTNESS unknown for #1–#3.

---

### `engine/lattice/core_exact.py` — exact 2-D square-lattice Weyl QCA (**D1 reference implementation**)
**Status:** live · driven (22 ch) · **Findings:** (none in registry) · **Lattice:** square (2-D), **reference implementation, continuum-limit regression target, not canonical (D1)** · **Law:** per-branch Weyl walk (single branch) · **Units:** lattice

**Does:** BDPT Paper 1 Eq. 16, the unique $s=2$ square-lattice Weyl QCA. It is the 2-D analogue of `bcc.py`.

Notation: $c_i=\cos(k_i/\sqrt2)$, $s_i=\sin(k_i/\sqrt2)$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u=c_xc_y,\ \tilde{\mathbf n}=(s_xc_y,\ c_xs_y,\ s_xs_y)$ | walk components | `core_exact.py:L47–50 _arccos_2d_uvec()` | unknown (inferred: exact) |
| 2 | $u^2+\lvert\tilde{\mathbf n}\rvert^2=(c_x^2+s_x^2)(c_y^2+s_y^2)=1$ | unitarity | docstring L19–20; checked `L97 exact2d_unitarity_residual()` | exact (inventory #4: norm drift $8.4\times10^{-15}$) |
| 3 | $U=u\,\mathbb I-i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}$ (same entry layout as `bcc.py` #4) | per-mode update | `core_exact.py:L63–66 exact2d_unitary()` | unknown (inferred: exact) |
| 4 | $\omega=\arccos(c_xc_y)$ → $\lvert\mathbf k\rvert/\sqrt2$ as $k\to0$ | dispersion; 2-D $c=1/\sqrt2$ | `core_exact.py:L57 exact2d_dispersion()`; L142 | unknown (inferred: exact) |
| 5 | $\psi_{t+1}=\mathcal F^{-1}U\mathcal F\psi_t$ | update rule | `core_exact.py:L77–83 weyl_step_2d_arccos_splitstep()` | unknown (inferred: machine) |
| 6 | $\lvert\mathbf v_g\rvert-1/\sqrt2$ by central difference ($\epsilon=10^{-5}$) | frequency-dependent speed; exactly 0 along $(1,0)$ | `core_exact.py:L125–128 exact2d_freq_dependent_c()` | unknown (inferred: quantitative) |

**Flags:**
- OTHER (D7): `SQRT2 = np.sqrt(2.0)` (L39) is an unregistered literal. $1/\sqrt2=c_\text{lat}(d{=}2)$ is not imported from `casim.constants`.
- OTHER: the registry row carries no findings and no exactness.

---

### `engine/lattice/curved.py` — variable-$c$ Weyl steppers (**D1 reference implementation**, F276)
**Status:** live · driven (29 ch) · **Findings:** (none in registry; F3b, F271, F276 by content) · **Lattice:** 2-D square, **reference implementation, continuum-limit regression target, not canonical (D1)** · **Law:** continuum Weyl $H=c(\mathbf x)\,\boldsymbol\sigma\cdot\hat{\mathbf p}$ · **Units:** lattice; $c$ = `c_unitary`

**Does:** refraction analogue with a position-dependent speed $c(\mathbf x)$. There are three steppers: blend (approximate), Strang (Weyl-ordered, second order) and Cayley (exactly unitary).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c(x)=c_L(1-\alpha)+c_R\alpha,\ \alpha=\tfrac12[1+\tanh((x-x_b)/w)]$ | two-region speed field | `curved.py:L48–49 make_c_field_step()` | unknown (inferred: exact) |
| 2 | $\psi'=(1-w)\,U_{c_\min}\psi+w\,U_{c_\max}\psi,\ w=(c-c_\min)/(c_\max-c_\min)$ | blend stepper (**not unitary**) | `curved.py:L66–72 weyl_step_2d_varc()` | unknown |
| 3 | $(\boldsymbol\sigma\cdot\nabla\psi)_\uparrow=\partial_xg-i\partial_yg,\ (\cdot)_\downarrow=\partial_xf+i\partial_yf$; spectral $ik$ with the Nyquist bin zeroed, or centred difference | $\boldsymbol\sigma\cdot\nabla$, anti-Hermitian | `curved.py:L124–133, L148–159 _sigma_grad_2d()` | unknown (inferred: exact (anti-Hermiticity)) |
| 4 | $W=\tfrac12\{\delta c,\ \boldsymbol\sigma\cdot\nabla\}$ (Weyl order; `'asymmetric'` $=\delta c\,\boldsymbol\sigma\cdot\nabla$ is **SUPERSEDED by F276**, kept as a control) | generator of the inhomogeneous half-step, $-i\,\delta H=-W$ | `curved.py:L179–186 _W_dH()` | unknown (inferred: exact (anti-Hermitian)) |
| 5 | $e^{-hW}\approx\mathbb I-hW+\tfrac{h^2}2W^2$ (`order=1` drops $W^2$: SUPERSEDED by F276) | second-order truncation | `curved.py:L211–218 _half_step_dH()` | unknown (inferred: quantitative) |
| 6 | per sub-step: $e^{-\delta H\,dt/2}\,U_{c_0}(dt)\,e^{-\delta H\,dt/2}$, $c_0=\overline c$, $dt=1/n_\text{sub}$ | Strang split, global order 2 | `curved.py:L395–407 weyl_step_2d_varc_strang()` | unknown (inferred: quantitative (F276 asserts order 2±0.1; norm ratio ≥6 per doubling, `L456–468`)) |
| 7 | $(\mathbb I+i\tfrac{dt}2H)\psi'=(\mathbb I-i\tfrac{dt}2H)\psi$, $H=c\,\boldsymbol\sigma\cdot(-i\nabla)$, face-averaged $c_{i\pm1/2}=\tfrac12(c_i+c_{i\pm1})$; entries $\pm\tfrac{dt}4c_\text{face}$ and $\mp i\tfrac{dt}4c_\text{face}$ | Cayley / Crank–Nicolson, exactly unitary | `curved.py:L268–311 _build_cayley_matrix_2d()`; `L354–357 CayleyVarcSolver2D.step()` | machine (inventory: $5.5\times10^{-15}$) |
| 8 | Snell: $\sin\theta_R=\sin\theta_L\,c_R/c_L$ | predicted refraction angle | `curved.py:L598–603 measure_refraction()` | unknown (inferred: exact (formula); measurement **broken** per docstring) |

**Flags:**
- SUPERSEDED: `ordering='asymmetric'` and `order=1` (the pre-F276 scheme) are kept only as negative controls.
- OTHER: `measure_refraction`'s outgoing angle is invalid under periodic wrap (the docstring warning, L490–512). No claim rests on it.
- OTHER: the Strang stepper hard-codes an external $dt=1$ (L397).
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown for #2.

---

### `engine/lattice/derive_walk_bz_measure.py` — the walk's BZ is not the FFT cube (F267)
**Status:** live · entry-script · **Findings:** F267 F265 F250 · **Lattice:** BCC (W) vs (G) · **Law:** per-branch walk · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\sqrt3=1/c_\text{lat}$; walk period generators $\sqrt3\pi(1,1,0),\sqrt3\pi(1,0,1),\sqrt3\pi(0,1,1)$ | walk's reciprocal lattice ($\sqrt3\times$fcc) | `derive_walk_bz_measure.py:L92–96` | exact (reg) |
| 2 | $\max\lvert\omega(\mathbf k+\mathbf G)-\omega(\mathbf k)\rvert$ for $\mathbf G\in\{\pi(110),\,2\pi(100),\,\sqrt3\pi(\cdot)\}$ | S1: only the $\sqrt3$fcc shifts are periods | `derive_walk_bz_measure.py:L121–123 s1_periodicity()` | exact (reg) |
| 3 | $V_\text{cube}/V_\text{zone}=(2\pi/\sqrt3)^3/((2\pi)^3/4)=4/(3\sqrt3)$ | S2: cube is 76.98% of one zone | `derive_walk_bz_measure.py:L99, L131–135 s2_volumes()` | exact (reg) |
| 4 | #$\{\omega=0\}=1$, #$\{\omega=\pi\}=0$ per branch at $L=24,36,48$ | S3: no doubler | `derive_walk_bz_measure.py:L147–149` | exact (reg) |
| 5 | cube grid mean vs Monte-Carlo mean over $a\cdot G_\text{walk}$, $a\in[0,1)^3$, for $\omega$ and $1/\omega$ | S4 measure error (10.7% / 16.9%) | `derive_walk_bz_measure.py:L159–175 s4_measure_error()` | quantitative (reg: exact; row is weaker — see flags) |
| 6 | $\mathcal F^{-1}[e^{i(1,1,1)\cdot\mathbf k/\sqrt3}\mathcal F\delta]$ spreads over many cells; $\sum\lvert\cdot\rvert^2=1$ | S5: the hop is fractional | `derive_walk_bz_measure.py:L183–190 s5_hop_is_fractional()` | machine (reg: exact; row is weaker — see flags) |

**Flags:**
- EXACTNESS tension: the registry says `exact`, but S4 is Monte Carlo (quantitative).
- OTHER: `run()` hard-codes the verdicts `fermion_sector_needs_a_measure_correction: True` and `correction_is_the_gauge_factor_4: False` (L211–212). These are asserted, not computed.
- OTHER (D7): `CUBE_OVER_ZONE` uses `np.sqrt(3.0)` while `ROOT3` uses $1/c_\text{lat}$.

---

### `engine/lattice/dimensionality.py` — why $d=3$ (F291) and not $3n$ (F292)
**Status:** live · standalone · **Findings:** F291 F292 · **Lattice:** BCC walk (W) for $d=3$; square for $d=2$; trivial shift for $d=1$ · **Law:** per-branch walk · **Units:** n/a (sympy exact)

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\tilde{\mathbf n}(\mathbf k)$ exact, with argument $k_i/\sqrt d$: $d{=}3$ as `bcc.py` #2, $d{=}2$ as $(s_xc_y,c_xs_y,s_xs_y)$, $d{=}1$ as $(0,0,\sin k)$ | Bloch vector per $d$ | `dimensionality.py:L188–209 bloch_vector()` | exact (reg) |
| 2 | $J=\partial\tilde{\mathbf n}/\partial\mathbf k\rvert_0$ ($3\times d$); for $d\ge4$, rank 3 by counting | Jacobian | `dimensionality.py:L215–233` | exact (reg) |
| 3 | max anticommuting traceless Hermitian set at $s=2$ is 3 ($\{a\cdot\sigma,b\cdot\sigma\}=2a\cdot b$) | internal vector dim | `dimensionality.py:L240–273` | exact (reg) |
| 4 | S1: $\ker J=0$ ⇔ $d\le3$; S2: $\operatorname{coker}J=0$ ⇔ $d\ge3$ ($\dim\operatorname{coker}=3-d$) | upper and lower bounds | `dimensionality.py:L276–306` | exact (reg) |
| 5 | S3: $d(d-1)/2=d\Rightarrow d\in\{0,3\}$; Hodge $d-2=1\Rightarrow d=3$ | $B$ is a vector only at $d=3$ | `dimensionality.py:L313–333` | exact (reg) |
| 6 | $c_\text{lat}(d)=1/\sqrt d$ | Paper 1 Eq. 21 | `dimensionality.py:L342` | exact (reg) |
| 7 | $\det J=\mp3^{-3/2}=\mp c_\text{lat}^3$ (for '+', '−') | chirality as orientation (spot-checked: $\mp\sqrt3/9$) | `dimensionality.py:L361–363 chirality_orientation()` | exact (reg) |
| 8 | $\dim\Lambda^2\mathbb R^d/d=(d-1)/2$; $=1$ only at $d=3$ | S3′ (F292) | `dimensionality.py:L393, L398` | exact (reg) |
| 9 | chirality exists ⇔ $\prod\gamma\not\propto\mathbb I$ ⇔ $D=d+1$ even (recursive Clifford build) | S4 (F292) | `dimensionality.py:L412–459` | exact (reg) |
| 10 | reducible $d=3n$: $J=[\,I/\sqrt3\ \cdots\ I/\sqrt3\,]$, rank 3, $\ker=3(n-1)$, $\operatorname{coker}=0$ | frozen directions | `dimensionality.py:L464–485` | exact (reg) |
| 11 | minimal spinor dim $2^{\lfloor d/2\rfloor}$ | cell needed per $d$ | `dimensionality.py:L403` | exact (reg) |

**Flags:**
- OTHER: `report()` sets `time_dim = 1` as "structural". It is superseded in substance by F313/F326 (`time_signature.py`, `time_single_generator.py`); the code labels it honestly.

---

### `engine/lattice/geometry.py` — k-grids and real-space BCC geometry (F265)
**Status:** live · driven (29 ch) · **Findings:** (none in registry; F264, F265 by content) · **Lattice:** k-grid builders generic; BCC helpers in convention (G); `LatticeConfig.cubic()/square()` = **D1 reference geometry** · **Law:** n/a · **Units:** lattice

**Does:** the single source of FFT $k$-grids for all steppers, plus the real-space BCC structure (hops, links, plaquettes, site mask, fcc reciprocal lattice, BZ mask).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $k_i=2\pi\,\text{fftfreq}(L_i)\in(-\pi,\pi]$, meshgrid `ij` | FFT k-grid (1/2/3-D) | `geometry.py:L57, L67–69, L77–80` | unknown (inferred: exact) |
| 2 | $\mathbf d\in\{\pm1\}^3$ (8 hops); link axes $(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)$ with $U_{-\mathbf d}(x)=U_{\mathbf d}(x-\mathbf d)^\dagger$ | nearest-neighbour shell and link storage | `geometry.py:L129–136` | unknown (inferred: exact) |
| 3 | lattice $=\{\mathbf n\in\mathbb Z^3:n_x\equiv n_y\equiv n_z \pmod 2\}$, index 4 | BCC site mask ("same parity") | `geometry.py:L197 bcc_site_mask()`; `BCC_INDEX_IN_Z3=4` L139 | unknown (inferred: exact) |
| 4 | 6 minimal 4-bond rhombi $(\mathbf d_1,\mathbf d_2)$, $\mathbf d_2\ne\pm\mathbf d_1$, modulo corner relabelling; $\lvert\mathbf d_1\times\mathbf d_2\rvert=2\sqrt2$; half-normals $\mathbf m=(\mathbf d_1\times\mathbf d_2)/2\in\langle110\rangle$ | plaquette orientations (no 3-bond loops) | `geometry.py:L146–177 _bcc_plaquette_reps()`, `BCC_PLAQ_AREA` L143 | unknown (inferred: exact) |
| 5 | $\mathbf G=\pi(1,1,0),\pi(1,0,1),\pi(0,1,1)$ | fcc reciprocal basis | `geometry.py:L202 bcc_reciprocal_basis()` | unknown (inferred: exact) |
| 6 | $V_\text{BZ}=\lvert\det G\rvert=2\pi^3=(2\pi)^3/4$ | true BZ volume | `geometry.py:L207 bcc_bz_volume()` | unknown (inferred: exact (float det; $2\pi^3$ spot-checked)) |
| 7 | BZ mask = minimal-$\lvert\mathbf k\rvert$ member of each coset of $\{(0,0,0),(h,h,0),(h,0,h),(0,h,h)\}$, $h=L/2$ (ties by flat index); $\sum\text{mask}=L^3/4$ | selects one rhombic-dodecahedral BZ | `geometry.py:L225–244 bcc_bz_mask()` | unknown (inferred: exact (count spot-checked)) |
| 8 | weight $=1/4$ | cube-mean → BZ-mean factor (**gauge side (G) only**; does not transfer to the walk, F267) | `geometry.py:L259 make_kgrid_bcc()` | unknown (inferred: exact) |
| 9 | $\Delta k_i=2\pi/L_i$ | bin spacing | `geometry.py:L297 LatticeConfig.__post_init__` | unknown (inferred: exact) |

**Inputs → outputs:** shapes → grids and masks.
**Depends on:** `casim.numerics.fft.fftfreq`, `memory_estimate`.
**Plumbing:** `LatticeConfig` memory reporting, `good_fft_sizes`, `next_good_fft_size`, `print_scaling_table` (FFT cost $n\log_2 n$), L262–477.
**Reference-lattice label:** `LatticeConfig.cubic()` (L304) and `.square()` (L314) carry the D1 banner: **reference implementation, continuum-limit regression target, not canonical.**

**Flags:**
- OTHER: conventions (G) (this file: cube side 2, hop $\mathbf d$) and (W) (`bcc.py`: hop $\mathbf d/\sqrt3$) coexist. `make_kgrid_bcc`'s factor 1/4 is correct for (G) and wrong for the walk (F267 §2).
- OTHER: the registry row carries no findings and no exactness.

---

### `engine/lattice/laurent_pell.py` — Pell descent over the Laurent ring (F316)
**Status:** live · standalone · **Findings:** F316 · **Lattice:** BCC walk as a Laurent polynomial in $w_j=e^{ik_j/\sqrt3}$ · **Law:** '+' branch · **Units:** n/a (exact over $\mathbb Q(i)$; support function in float)

**Does:** replaces Dubickas–Steuding's "deg 0 ⇒ unit" (false in a Laurent ring) with a two-sided width $D$. It proves that the unitary Pell solutions are $\{\pm A^n\}$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\lambda=(1,\sqrt2,\sqrt3)$; $h_f(\lambda)=\max_{m\in\operatorname{supp}f}\langle m,\lambda\rangle$; $D(f)=h_f(\lambda)+h_f(-\lambda)$ | two-sided width | `laurent_pell.py:L144, L159–161 support()`, `L172 width()` | machine (reg) |
| 2 | $(a,b)\cdot(a',b')=(aa'+bb'N,\ ab'+ba')$ in $R[X]/(X^2-N)$; $A=(u,-i)$ | Pell arithmetic; tower $A^n$ | `laurent_pell.py:L203–218` | machine (reg) (row read: exact) |
| 3 | L1: $h_{fg}=h_f+h_g$, $\mathrm{lc}(fg)=\mathrm{lc}f\,\mathrm{lc}g$ | genericity | `laurent_pell.py:L225–254` | machine (reg) |
| 4 | L2: $D(f)=0$ ⇔ monomial ⇔ unit; $1+w_1^{-1}$ has $D>0$ | width detects units | `laurent_pell.py:L257–279` | machine (reg) (row read: exact) |
| 5 | L3: $a^*=a,\ b^*=-b$ ⇒ $h(\lambda)=h(-\lambda)$ | central symmetry from unitarity | `laurent_pell.py:L286–311` | machine (reg) (row read: exact) |
| 6 | L4: $D(a)=D(b)+2c,\ c=h_u(\lambda)$ | height relation | `laurent_pell.py:L318–326` | machine (reg) |
| 7 | L5–L6: $b'=bu+ai,\ b''=bu-ai$; exactly one cancels at the top; $b'b''=1+b^2$ | leading-term sign; product identity | `laurent_pell.py:L329–370` | machine (reg) (row read: exact (identity)) |
| 8 | L7: $D(b')\le D(b)-2c$ (measured drop $=2c$ exactly) | descent | `laurent_pell.py:L373–402` | machine (reg) |
| 9 | L8: base case lands on $\{\pm1,\pm A^{\pm1}\}$ ($u$ has 8 monomials, not 2) | landing set | `laurent_pell.py:L405–425` | machine (reg) (row read: exact) |

**Depends on:** `time_signature.Laurent`, `bcc_u`, `bcc_discriminant` (below).
**Flags:** none. The registry says `machine`, consistent with the float separation legs.

---

### `engine/lattice/multigrid.py` — two-grid proton/electron multigrid (U4)
**Status:** live · driven (9 ch) · **Findings:** (none in registry; F133, F156, F160 by content) · **Lattice:** simple cubic $L^3$ with spacing $a$ (reference geometry) · **Law:** n/a (non-relativistic Schrödinger) · **Units:** physical length in units of $a$; model energy

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\rho_c=R_b\rho_f$ (block average), with $\sum\rho_c\,b^3=\sum\rho_f$ | charge-faithful $R_b$ | `multigrid.py:L67–82 reduce_charge()` | unknown (inferred: exact) |
| 2 | $V=\Phi_\text{cells}/a$ with $\Phi_\text{cells}=$ `solve_poisson_3d_open`$(\rho/\sum\rho,\,G_N=k)$, i.e. $V\to-k/r_\text{phys}$ | electron potential (open BC) | `multigrid.py:L117–122 _coulomb_potential()` | unknown (inferred: quantitative) |
| 3 | $\psi\leftarrow e^{-V\delta\tau/2}\,\mathcal F^{-1}e^{-k^2\delta\tau/2m}\mathcal F\,e^{-V\delta\tau/2}\psi$, renormalised | imaginary-time relaxation | `multigrid.py:L148–152 solve_hydrogen()`; `L198–205 schrodinger_relax()` | unknown (inferred: quantitative) |
| 4 | $E_0=\tfrac1{2m}\langle\psi\rvert k^2\lvert\psi\rangle+\langle V\rangle$; $a_0=\langle r\rangle$ | observables | `multigrid.py:L154–157` | unknown (inferred: quantitative) |
| 5 | $\psi'=e^{-iV dt/2}\mathcal F^{-1}e^{-ik^2dt/2m}\mathcal F e^{-iVdt/2}\psi$ | real-time Strang step (unitary) | `multigrid.py:L184–189 schrodinger_step()` | unknown (inferred: machine (norm)) |
| 6 | represented $a_0/r_p=(\text{orbit cells})\cdot b/r_{p,\text{fine}}$ | scale separation carried by $b$ | `multigrid.py:L280 MultigridAtom.run()` | unknown (inferred: exact (definition)) |

**Depends on:** `core.blockspin.block_average_field` (04), `casim.gravity.solve_poisson_3d_open` (i.e. `poisson_open`).
**Flags:**
- OTHER: `_HERE` is inserted into `sys.path` (L51–53), a legacy flat-import shim.
- OTHER: in `reduce_charge`, the bare `except Exception` silently falls back to a local reshape.
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown.

---

### `engine/lattice/poisson_open.py` — open-boundary 3-D Poisson (James/Hockney)
**Status:** live · driven (29 ch) · **Findings:** (none in registry) · **Lattice:** cubic $L^3$, unit spacing · **Law:** n/a · **Units:** lattice ($G_N$ in lattice units)

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathcal G(r)=-1/(4\pi\max(r,r_\min))$, $r_\min=0.5$, min-image on the $2L$ torus | free-space Green's function | `poisson_open.py:L76–81 green_freespace_3d()` | unknown (inferred: exact (construction)) |
| 2 | $\hat\phi=4\pi G_N\,\hat\rho_\text{pad}\,\hat{\mathcal G}$ ⇒ $\phi(\mathbf x)=-G_N\sum_{\mathbf y}\rho(\mathbf y)/\lvert\mathbf x-\mathbf y\rvert$; crop $[0,L)^3$ | solves $\nabla^2\phi=4\pi G_N\rho$, $\phi\to0$ at infinity | `poisson_open.py:L115–135 solve_poisson_3d_open()` | unknown (inferred: quantitative (far field)) |
| 3 | periodic comparison $\hat\phi=-4\pi G_N\hat\rho/k^2$ | diagnostic only | `poisson_open.py:L200–202` | unknown (inferred: exact) |

**Flags:**
- ⚠ DOC/CODE MISMATCH: the docstring (L28–29, L39–40) claims the free-space potential is recovered "to machine precision". The code computes a *discrete* Green's-function convolution with an $r_\min$ cutoff, whose far field matches $-G_NM/r$ only to discretisation/source-width accuracy (the test prints relative errors, no tolerance).
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown.

---

### `engine/lattice/si_scale.py` — the lattice↔SI unit map (P6)
**Status:** live · driven (3 ch) · **Findings:** (none in registry; F79, F107, F112, F77, F103, F122, F372 by content) · **Lattice:** BCC (W): $a$ is the walk's unit length, 1 cell per tick $=c\sqrt3$ · **Law:** n/a · **Units:** **SI** (m, s, J, GeV, MeV)

**Does:** the only lattice→SI map. The geometric cell fixes metre, second and $G$; the strong sector is fixed by the single anchor $f_\pi$.

Constants: $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107, exact); $\ell_P$ = CODATA (external); $c$, $\hbar$, $G_\text{CODATA}$ external; `J_per_GeV` $=1.602176634\times10^{-10}$ (SI exact); $f_\pi^\text{phys}$ = `f_pi_anchor_MeV` (external, F77/F123).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P$ | metre anchor (cell length) | `si_scale.py:L81 canonical_cell()` | unknown (inferred: exact (ratio); external ($\ell_P$)) |
| 2 | $\tau=a/(c\sqrt3)$ ⇔ $a/\tau=c\sqrt3$, so $c_\text{lat}\,a/\tau=c$ | second anchor (tick) | `si_scale.py:L82`, L89 | unknown (inferred: exact) |
| 3 | $G_\text{pred}=a^2c^3/(8\pi\sqrt3\,\hbar)$ | structural Newton constant (F79/F107); relative error vs CODATA reported | `si_scale.py:L83`, L91 | unknown (inferred: exact form; numerical match external) |
| 4 | $E_\text{UV}=\hbar c/a$ (in GeV via `J_per_GeV`) | UV cutoff | `si_scale.py:L84` | unknown (inferred: exact) |
| 5 | $\text{scale}=f_\pi^\text{phys}/f_\pi^\text{model}$; $m_X^\text{MeV}=10^3\,m_X^\text{GeV,model}\cdot\text{scale}$ | the strong-sector anchor | `si_scale.py:L110–114 strong_spectrum()` | unknown (inferred: exact (map); inputs quantitative) |
| 6 | $m_p\approx3m_c$ | leading constituent nucleon mass | `si_scale.py:L148 nucleon_mass()` | unknown (inferred: quantitative) |
| 7 | $m_n-m_p$ from `neutron_minus_proton`$(m_u{=}2.16,\,m_d{=}4.67,\,\sigma{=}1,\,\alpha_s{=}0.5,\,\delta_\text{em}^p{=}1.00)$ + F372 pairwise EM check ($m_q{=}0.785$) | n–p splitting | `si_scale.py:L160–170 np_splitting()` | unknown (inferred: quantitative / fit (ad hoc EM)) |

**Depends on:** `particles.meson`, `particles.baryon_dynamics` (06); constants (01).
**Flags:**
- OTHER (symbol clash): here $a$ is the walk's unit length (hop $=1$). In F278/`bcc.py` #12, $a=2c_\text{lat}$ is the conventional **cube edge** in the same units. They are different objects under one symbol.
- OTHER (D7): `np.sqrt(3.0)` (L82–83) is used rather than $1/c_\text{lat}$. There are unregistered literals: PDG $m_p=938.272$, $\Delta m=1.293$, $m_u=2.16$, $m_d=4.67$, $\delta_\text{em}^p=1.00$, $m_q=0.785$, $\alpha_s=0.5$ (L152–167).
- OTHER: the registry row carries no findings and no exactness.
- EXACTNESS unknown (registry). The tags above are construction-based.

---

### `engine/lattice/time_generator_axiom_independence.py` — P1 vs the BDPT axioms (F377)
**Status:** live · standalone · **Findings:** F377 · **Lattice:** BCC (W), engine stepper · **Law:** tick-by-tick choice of branch $A^+$ / $A^-$ · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $s_n=\lfloor(n+1)\beta\rfloor-\lfloor n\beta\rfloor$, $\beta=2/(1+\sqrt5)$ | Sturmian (aperiodic) schedule | `time_generator_axiom_independence.py:L140–143 sturmian_word()`, L264 | quantitative (reg) (row read: exact) |
| 2 | $(A^-A^+)^n=\prod(A^-A^+)$, with $B=A^-A^+$ | regrouping lemma (Part B) | `time_generator_axiom_independence.py:L164–183 check_regroup()` | quantitative (reg) (row read: machine ($<10^{-10}$)) |
| 3 | $\mathrm{Var}[\mathbf x](t)\sim t^p$, $p$ = slope of $\ln\mathrm{Var}$ vs $\ln t$ over $t>n/3$, with `weyl_step_3d_bcc` per tick | ballistic exponent | `time_generator_axiom_independence.py:L228–249 ballistic_exponent()` | quantitative (reg) |
| 4 | pass ⇔ $p_\text{periodic-matched}-\max p_\text{aperiodic}\ge0.03$ | falsification-attempt margin | `time_generator_axiom_independence.py:L278–290` | quantitative (reg) |

**Flags:**
- OTHER (possible artifact): the default run ($L=48$, $\sigma=4$, $k_0=(0.3,0.2,0.1)$, 60 ticks) is **not wrap-free**. I re-ran the pure-$A^+$ baseline and the $x$-centroid wraps: edge-slab weight is 0.19 at $t=40$ and 0.23 at $t=60$, and $\bar x$ goes from $+8.8$ to $-2.8$. The variances fitted over $t>20$ include periodic-wrap contamination. `wavepacket.py`'s F20 remediation names this exact failure mode. Not settled here.
- OTHER (hazard): `_gaussian_wavepacket` takes its polarisation from `xp.linalg.eig` of a chiral 2×2 unitary (L201), which is the CLAUDE.md eig-on-chiral caveat. Contrast `wavepacket._fixed_spinor`, which builds it analytically.

---

### `engine/lattice/time_signature.py` — one time from the commutant of the update (F313)
**Status:** live · standalone · **Findings:** F313 · **Lattice:** BCC walk over $R=\mathbb C[w_j^{\pm1}]$, $w_j=e^{ik_j/\sqrt3}$ (infinite volume) · **Law:** '+' branch; $s=4$ Dirac composite as the residual · **Units:** n/a (exact $\mathbb Q(i)$)

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c_j=(w_j+w_j^{-1})/2$, $s_j=(w_j-w_j^{-1})/2i$; $f^*$: $w\to w^{-1}$ with conjugated coefficients | exact Laurent arithmetic; involution = adjoint | `time_signature.py:L273–340 Laurent`, `L365–381 _cos(),_sin()` | exact (reg) |
| 2 | $u$, $\tilde{\mathbf n}$ as `bcc.py` #1–2 in $R$ | the update, exactly | `time_signature.py:L388–407 bcc_u(), bcc_bloch()` | exact (reg) |
| 3 | $N=\lvert\tilde{\mathbf n}\rvert^2=1-u^2=(1-u)(1+u)$, both factors irreducible | squarefree discriminant | `time_signature.py:L410–413`, `L482–505 discriminant_is_squarefree()` | exact (reg) |
| 4 | $\dim\{B:[B,\boldsymbol\sigma\cdot\tilde{\mathbf n}]=0\}=2$, spanned by $\mathbb I,\ \boldsymbol\sigma\cdot\tilde{\mathbf n}$ | C1 commutant | `time_signature.py:L431–450 commutant_dimension()` | exact (reg) |
| 5 | $\gcd(\tilde n_1,\tilde n_2,\tilde n_3)$ is a unit | C2 locality survives | `time_signature.py:L467–475` | exact (reg) |
| 6 | $aa^*=1$ ⇔ $a=\zeta w^{\mathbf m}$ ⇒ scalar part $=U(1)\times\mathbb Z^3$ | C3 shifts (probe-based) | `time_signature.py:L527–545` | exact (reg) |
| 7 | $a^2-b^2N=1$; $A=(u,-i)$ with $\deg b=0$ ⇒ fundamental | C4 Pell group | `time_signature.py:L577–588 fundamental_pell_solution_degree()` | exact (reg) |
| 8 | $A^n=(T_n(u),\,-i\,U_{n-1}(u))$, $\deg b(A^n)=n-1$; $A^{-1}$ descent terminates in $n$ steps; $A^n$ is never a monomial | C5 tower, descent, infinite order | `time_signature.py:L605–629, L644–669, L684–695` | exact (reg) |
| 9 | $d_\text{time}=s-1$ **only at $s=2$** (raises otherwise); $d_\text{space}\le2\log_2s+1$ | signature at the minimal cell | `time_signature.py:L716–735` | exact (reg) |
| 10 | $D=\begin{pmatrix}nA & im\mathbb I\\ im\mathbb I & nA^\dagger\end{pmatrix}$, $V=\mathbb I\otimes A$, $[V,D]=0$ at every $m$ | $s=4$ second flow (residual; killed by F315) | `time_signature.py:L783–830 composite_cell_second_flow()` | machine (reg: exact; row is weaker — see flags) |

**Flags:**
- ⚠ DOC/CODE MISMATCH: `report()`'s verdict string (L859–866) still says "d_time = rank su(2) = 1 … d_space <= dim su(2) = 3, so the signature 3+1 rests on ONE input". The module banner (L141–153) **withdraws** that (dim su, rank su) identity as numerology.
- ⚠ DOC/CODE MISMATCH: `report()` still lists `imported_step: "Abel's theorem"` (L858). The banner says the Abel attribution was wrong (it is Dubickas–Steuding), and F316 (`laurent_pell.py`) discharges the import.
- OTHER: `discriminant_is_squarefree` returns `"is_a_square": False` hard-coded (L504), and `scalar_part_is_exactly_the_shifts` returns `d_space_from_commutant: 3` hard-coded (L544).
- OTHER (open): the ring used is $\mathbb C[\mathbb Z^3]$ in $w_j$, so C3's shift group is $\mathbb Z^3$. The walk itself lives in the BCC sublattice ring (monomials with all exponents odd or all even), and the docstring's input 3 says locality is w.r.t. Λ (index 4), not $\mathbb Z^3$. Whether this changes C3's "$\mathbb Z^3$" to Λ is not settled here.

---

### `engine/lattice/time_signature_interacting.py` — the second flow $V$ does not survive interaction (F315)
**Status:** live · standalone · **Findings:** F315 · **Lattice:** BCC walk on a periodic $L^3$ grid in the **walk variable** $\theta_j=2\pi n_j/L$ (i.e. $\theta=k/\sqrt3$) · **Law:** $s=4$ massive Dirac composite, '+' Weyl block · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u,\tilde{\mathbf n}$ with $c_j=\cos\theta_j,\ s_j=\sin\theta_j$; $A=u\mathbb I-i\boldsymbol\sigma\cdot\tilde{\mathbf n}$; $D=\begin{pmatrix}n_\text{kin}A & im\\ im & n_\text{kin}A^\dagger\end{pmatrix}$, $n_\text{kin}=\sqrt{1-m^2}$; $V=\mathrm{diag}(A,A)$ | per-$k$ operators | `time_signature_interacting.py:L195–206 mode_table()` | machine (reg) (row read: exact) |
| 2 | joint eigenbasis from `eigh` of a generic Hermitian mix $M$; $\Omega_a,\phi^V_a=\arg$ diag | two phases per mode | `time_signature_interacting.py:L215–224` | machine (reg) |
| 3 | antisymmetrised pairs at fixed $K=(k_1+k_2)\bmod L$; $H_{ab}=W_{pqrs}-W_{pqsr}-W_{qprs}+W_{qpsr}$, $W=\text{kern}\cdot\langle\text{overlaps}\rangle$, kern $=1$ (contact) or $1/q^2$ (Coulomb) | two-particle $H_\text{int}$ | `time_signature_interacting.py:L241–286` | machine (reg) (row read: exact (construction)) |
| 4 | $V$ survives ⇔ every live element has $\Delta q_V\equiv0\ (2\pi)$; O(G) deformation obstructed on resonant ($\lvert\Delta\Omega\rvert<10^{-9}$) elements with $\lvert\Delta q_V\rvert>10^{-6}$ | I1–I8 verdicts | `time_signature_interacting.py:L302–325 survival_report()` | machine (reg) |

**Flags:**
- OTHER (convention): the momentum grid is the walk-variable torus $\theta\in2\pi\mathbb Z_L/L$, not `bcc.py`'s FFT convention $k/\sqrt3$ with $k\in2\pi\mathbb Z_L/L$. For even $L$ it contains 4 copies of the walk zone ($U$ is invariant under $\theta\to\theta+\pi(1,1,0)$). The default $L=3$ avoids that; see F267.
- OTHER: the mixing weights 0.8231, 0.6197, 0.2903 are declared arbitrary (L210–216). They are fine.

---

### `engine/lattice/time_single_generator.py` — no second candidate generator (F326)
**Status:** live · standalone · **Findings:** F326 · **Lattice:** engine (`LatticeSpec` cubic topology) + BCC Dirac stepper · **Law:** $s=4$ massive Dirac · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | `Clock` has one time-state field `tick`; `Channel` has no time field; fast-channel calls $=n_\text{sub}\cdot n_\text{ticks}$ | G1 engine single global clock | `time_single_generator.py:L204–263 check_engine_single_global_clock()` | machine (reg) (row read: exact (structural)) |
| 2 | $\mathcal F[\text{step}^n(\psi_0e^{i\mathbf k\cdot\mathbf x})]=D_{\mathbf k}^n\psi_0$ | G2 stepper = one matrix iterated | `time_single_generator.py:L310–343 check_dirac_composite_single_generator()` | machine (reg) |
| 3 | stepper signature has no per-branch `dt` | G2 structural leg | `time_single_generator.py:L348–352` | machine (reg) (row read: exact) |

**Depends on:** `core.clock`, `core.simulation`, `core.channel` (04); `particles.dirac_bcc` (06).
**Flags:**
- OTHER: the docstring (L109–122) itself concedes that G2's residual is near-tautological, because both paths use `bcc_unitary`/`_kinetic_n`. Only the signature leg carries independent weight.
- OTHER: `LatticeSpec(topology="cubic")` in G1 is a probe only, with no physics.

---

### `engine/lattice/wavepacket.py` — closed-form BCC group velocity (F20 remediation)
**Status:** live · standalone · **Findings:** F20 F26 · **Lattice:** BCC (W) · **Law:** per-branch Weyl; massive Dirac · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u^\pm(k\hat x)=\cos(k\,c_\text{lat})$ bit-for-bit for both branches | on-axis identity (off-axis control $O(1)$) | `wavepacket.py:L99–100 onaxis_u_residual()`; `L110–113` | exact (reg) |
| 2 | $\omega(k\hat x)=k\,c_\text{lat}$ for $k\,c_\text{lat}\in[0,\pi]$; bound $2\epsilon/\sin(\pi/(n_k-1))$ | on-axis linear light cone, $\partial^2_{k_x}\omega\equiv0$ | `wavepacket.py:L139–140`, `L125–126`, `L151–152` | machine (through arccos) (reg: exact; row is weaker — see flags) |
| 3 | $\partial u/\partial k_x=-c_\text{lat}\tilde n_x$ ⇒ $\partial\omega/\partial k_i=c_\text{lat}\,\hat n_i(\mathbf k)$ | Weyl group velocity | `wavepacket.py:L166–167 weyl_group_velocity()` | exact (reg) |
| 4 | $\omega=\arccos(n_\text{kin}u)$ ⇒ $\partial\omega/\partial k_i=c_\text{lat}\,n_\text{kin}\,\tilde n_i/\sqrt{1-n_\text{kin}^2u^2}$, $n_\text{kin}=\sqrt{1-m^2}$ | Dirac group velocity | `wavepacket.py:L177–181 dirac_group_velocity()` | exact (reg) |
| 5 | $w(\mathbf k)=\lvert\mathcal F[\text{env}]\rvert^2/\sum$ (σ = **amplitude** width) | packet momentum weights | `wavepacket.py:L209–218` | exact (reg) |
| 6 | $\bar v_x=c_\text{lat}\langle\hat n_x^2\rangle_w$ (fixed seed) or $c_\text{lat}\langle\hat n_x\rangle_w$ (helicity-pure); massive: $\langle\partial\omega/\partial k_x\rangle_w$ | finite-width centroid velocity | `wavepacket.py:L243–248 predicted_packet_velocity()` | exact (reg) |
| 7 | fixed spinor $(\cos\tfrac\theta2,\ e^{i\varphi}\sin\tfrac\theta2)$ of $\hat{\mathbf n}(k_0)$; helicity projector $(\mathbb I+\hat{\mathbf n}\cdot\boldsymbol\sigma)/2$; Dirac $P_+=(D_k-e^{i\omega})/(e^{-i\omega}-e^{i\omega})$ | seeds (no eig call) | `wavepacket.py:L258–263, L274–282, L299–315` | exact (reg) |
| 8 | drift = mean of the last `tail_ticks` per-tick centroid displacements, in a wrap-free box | measured group velocity | `wavepacket.py:L386–388 run_packet()` | machine (branch-pure, massive: $10^{-12}$; massless: $10^{-11}$); fixed seed $10^{-6}$ (reg: exact; row is weaker — see flags) |

**Depends on:** `bcc` (above), `particles.dirac_bcc` (06).
**Flags:**
- OTHER (D7): `offaxis_u_residual` uses `np.sqrt(3.0)` (L111), a control-only literal.
- OTHER: the registry says `exact`, while #2 and #8 are machine-class. The module labels them correctly.
