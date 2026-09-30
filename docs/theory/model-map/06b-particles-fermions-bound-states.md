# Particles II — fermion walks, discrete symmetries and bound states

Scope: the fifteen `src/casim/engine/particles/` modules that carry the **Dirac quantum walk** (2D square reference and 3D BCC canonical), its **discrete CPT** algebra (free and SU(2)$_L$-grafted), the **mass-generation side modules** (F27 complex/SU(2) mass step, the reference Higgs scalar, the Majorana see-saw), the **induced gauge-stiffness loop** on the BCC walk, and the **bound-state layer** (NJL mesons, the deuteron one-boson-exchange solver and its derived quark-Pauli core, positronium / hydrogen hyperfine, the element assembler) plus the second-quantised Fock layer. All equations below were read from the code; docstrings and findings were used only to name the physics, and any disagreement is flagged.

**Shared conventions.**
- *Dirac spinor* (every walk here): Weyl/chiral basis $\Psi=(\eta_\uparrow,\eta_\downarrow,\chi_\uparrow,\chi_\downarrow)$, $\eta$ left-handed, $\chi$ right-handed. Mass $m$ is dimensionless with $\lvert m\rvert\le1$ (QCA admissibility, hard-checked), and the kinetic weight is $n=\sqrt{1-m^2}$.
- *One-tick Dirac unitary* $D_k=\begin{pmatrix} nA_k & imI\\ imI & nA_k^\dagger\end{pmatrix}$: branch $+$ Weyl block paired with **its own Hermitian conjugate**, not with the opposite branch. `gauge/weak_wmu.covariant_dirac_doublet_step` instead pairs branch $+$ with branch $-$ (see `discrete_cpt_gauged.py`). So there are **two inequivalent massive-Dirac discretisations in the tree**.
- *Lattice (D1):* `dirac.py` is the 2D square-lattice **reference** (Paper 1 Eq. 16, $c=1/\sqrt2$). `dirac_bcc.py`, `discrete_cpt*.py` and `induced_stiffness.py` are on the canonical **BCC** layer (Paper 1 Eq. 15, $c_\text{lat}=1/\sqrt3$, F26). `higgs.py` is a continuum-dispersion 2D square grid. `meson.py`'s real-space demo and `nuclear*.py` are simple-cubic or continuum radial solvers, and `positronium.py`/`hyperfine.py`/`element.py` work in SI/MeV continuum units.
- *Propagator law (F91):* the fermion walks use the Weyl QCA unitary itself (the fermion propagator), so the even/chiral **gauge-boson** classification does not apply to them. Mark `n/a` unless a module couples a gauge boson.
- *Units:* lattice (cells, ticks) for the walks. MeV / fm / eV / MHz with CODATA/PDG literals in the bound-state modules (several of those are **not** routed through `casim.constants`, which is flagged).
- *Numerics:* the D8 façade is only partly honoured. Most modules `import numpy as np` directly and route only FFTs via `casim.numerics.fft`. The chiral-transform hazard is noted wherever `np.linalg.eig`/`inv` touches the 4×4 Dirac structure.

Modules covered (path order): `dirac.py`, `dirac_bcc.py`, `discrete_cpt.py`, `discrete_cpt_gauged.py`, `eg_sextic.py`, `element.py`, `higgs.py`, `hyperfine.py`, `induced_stiffness.py`, `majorana.py`, `meson.py`, `nuclear.py`, `nuclear_core.py`, `positronium.py`, `second_quant.py`.

---

### `engine/particles/dirac.py` — exact-QCA Dirac walk (2D square reference) + F27 complex/SU(2) mass step
**Status:** live · driven (22 ch) · **Findings:** — (registry empty; the code cites F9, F26, F27) · **Lattice:** 2D square (reference, D1) · **Law:** n/a (fermion walk) · **Units:** lattice

**Does:** the single-tick 4×4 Dirac QCA on the 2D square lattice, variable- and complex-mass Strang splits, and the F27 Higgs-free chiral SU(2) mass coupling for the $(\nu,e)$ doublet.

Here $W_k$ is the 2D Weyl unitary `core_exact.exact2d_unitary` (core_exact.py:L60–67): $W_k=uI-i\,\mathbf n\cdot\boldsymbol\sigma$ with $u=c_xc_y$, $n_x=s_xc_y$, $n_y=c_xs_y$, $n_z=s_xs_y$, $c_i=\cos(k_i/\sqrt2)$, $s_i=\sin(k_i/\sqrt2)$ (core_exact.py:L43–52 `_arccos_2d_uvec`).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $n=\sqrt{1-m^2}$, require $\lvert m\rvert\le1$ | kinetic weight from QCA admissibility $n^2+m^2=1$ | `dirac.py:L96 _kinetic_n()`, `L87 _check_mass()` | unknown (inferred: exact) |
| 2 | $D_k=\begin{pmatrix} nW_k & imI\\ imI & nW_k^\dagger\end{pmatrix}$ | one-tick Dirac unitary in Fourier space; $W'=W^\dagger$ is forced by $(D^\dagger D)_{12}=0$ | `dirac.py:L139–142 _apply_D_k()`; $W^\dagger$ built at `L123 _weyl_blocks()` | unknown (inferred: exact (unitarity algebraic)) |
| 3 | $\omega_k=\arccos(n\,c_xc_y)$ | Dirac dispersion; the eigenvalues of $D_k$ are $e^{\pm i\omega_k}$, each twofold | `dirac.py:L108 _dirac_dispersion()` | exact (inventory #13: residual $3.9\times10^{-16}$) |
| 4 | $U_D(k,dt)=\cos(\omega dt)I+\dfrac{\sin\omega dt}{\sin\omega}(D_k-\cos\omega\,I)$, with $\to dt$ at $\sin\omega=0$ | spectral interpolation to arbitrary $dt$; $dt=1$ applies $D_k$ exactly | `dirac.py:L195–204 dirac_step_2d_splitstep()` | unknown (inferred: exact ($dt=1$), machine (FFT)) |
| 5 | $\omega_Z=2\arcsin m$ (the analytic target; $\omega(0)=\arccos n=\arcsin m$) | zitterbewegung frequency of the chirality imbalance $\rho_\eta-\rho_\chi$ | `dirac.py:L384 measure_zitterbewegung_freq_2d()` | quantitative (inventory Q#3: 0.15%, FFT-bin-limited) |
| 6 | $\mathrm{Mix}(\theta)=\cos\theta\,I-i\sin\theta\,\beta$, $\beta=\begin{pmatrix}0&I\\I&0\end{pmatrix}$ | per-cell real-mass rotation | `dirac.py:L447–450 _mix_eta_chi()` | unknown (inferred: exact (unitary)) |
| 7 | $\mathrm{Mix}(\delta m,dt/2)\circ D(m_0,dt)\circ\mathrm{Mix}(\delta m,dt/2)$, $m_0=\langle m\rangle$, $\delta m=m(x)-m_0$ | variable-mass Strang step, $O(dt^2)$ | `dirac.py:L509–515 dirac_step_2d_varm_splitstep()` | unknown (inferred: exact at $\delta m=0$ (bit-for-bit); $O(dt^2)$ otherwise) |
| 8 | $U=\cos(\lvert M\rvert f)I-i\dfrac{\sin(\lvert M\rvert f)}{\lvert M\rvert}\begin{pmatrix}0&M\\M^*&0\end{pmatrix}$, $M=m_R+im_I$ | complex-mass per-cell rotation | `dirac.py:L474–485 _mix_eta_chi_complex()` | unknown (inferred: exact (unitary)) |
| 9 | same Strang split with $\delta M=(m_R-m_0)+im_I$ | complex variable-mass step | `dirac.py:L557–566 dirac_step_2d_varm_complex_splitstep()` | unknown |
| 10 | $W(dt/2)=\cos(\omega dt/2)I+\dfrac{\sin(\omega dt/2)}{\sin\omega}(W_k-\cos\omega I)$, $\omega=\arccos(c_xc_y)$ | massless kinetic half-step on one 2-spinor | `dirac.py:L641–655 _weyl_half_step_2c()` | unknown (inferred: machine) |
| 11 | $\eta'=c_m\eta+is_me^{i\theta}\chi,\ \chi'=is_me^{-i\theta}\eta+c_m\chi$, $c_m=\cos(m\,dt)$, $s_m=\sin(m\,dt)$ | F27 U(1) β-gauged complex-mass step | `dirac.py:L689–692 mass_step_1flavor_u1()` | exact (inventory #56 Ward $1.4\times10^{-17}$) |
| 12 | $K(dt/2)\circ M(\theta,dt)\circ K(dt/2)$ | full 1-flavour step | `dirac.py:L719–724 dirac_step_complex_mass_1flavor()` | unknown |
| 13 | $\eta'=c_m\eta+is_m(U\otimes I_2)\chi,\ \chi'=is_m(U^\dagger\otimes I_2)\eta+c_m\chi$, $U=\begin{pmatrix}a&-b^*\\b&a^*\end{pmatrix}$ | F27 SU(2) doublet mass step (isospin ⊗ spin) | `dirac.py:L819–829 mass_step_doublet_su2()` | exact (inventory #53 Ward) |
| 14 | $\eta\to V\eta,\ \chi\to\chi,\ U\to VU$ | chiral SU(2)$_L$ gauge transformation, the symmetry of #13 | `dirac.py:L904–915 su2_gauge_transform_chiral()` | exact (inventory #53/#54) |
| 15 | $\langle T_3\rangle_{L,R}=\tfrac12(N_\nu-N_e)$ | isospin observable | `dirac.py:L998 isospin_t3_doublet()` | exact (inventory #58) |
| 16 | returns $T_3^2+\lvert T_+\rvert^2$, with $T_3=\tfrac12(N_\nu-N_e)/N$, $T_+=\sum\eta_\nu^*\eta_e/N$ | "SU(2) Casimir" diagnostic | `dirac.py:L1015–1018 su2_casimir_left()` | unknown |

**Inputs → outputs:** four (or eight) complex $(L_x,L_y)$ arrays, $m$, $dt$, and optionally $\theta(x)$, $U(x)$ → updated arrays. Diagnostics return dispersion residuals, $\omega_Z$, norms, $\langle T_3\rangle$.
**Depends on:** `lattice/core_exact` (2D Weyl unitary, see 03-lattice.md § core_exact.py) and `numerics.fft` (02-numerics.md).
**Flags:**
- ⚠ Sign convention. $D_k$ carries $+im\beta$: at $k=0$, $D=\exp(+i\beta\arcsin m)$. The varm mix (#6/#8) applies $\exp(-i\beta\,\delta m\,dt)$. So the Strang composite at $k=0$ rotates by $\arcsin m_0-\delta m$, not $\arcsin(m_0+\delta m)$: the local mass perturbation enters with the **opposite sign**, and linearly in $\delta m$ while the baseline enters as $\arcsin m_0$. The F27 step #11/#13 uses $+i s_m$, consistent with $D_k$.
- ⚠ DOC/CODE MISMATCH #16: the docstring says the value is the Casimir $T(T+1)=\tfrac34$ for a pure doublet. The code returns $\lvert\langle\mathbf T\rangle\rvert^2$-type Bloch length, which is $\tfrac14$ for pure $\nu_L$.
- Stale comment (L389–414, L1021–1034): the removal of the U(1) minimal coupling is justified by "the composite bilinear in `ca_maxwell.py`" as the adopted photon. That σ-bilinear photon is **SUPERSEDED by F69** (S1). The photon is the paired-spinor `gauge/photon.py`.
- D8: `import numpy as np` directly; `np.fft.fftfreq` is allowed.

---

### `engine/particles/dirac_bcc.py` — exact-QCA Dirac walk on the 3D BCC lattice (canonical)
**Status:** live · driven (9 ch) · **Findings:** — (registry empty; the code cites F9 and Paper 1 Eq. 15/23; F86 for the scalar-confinement varm) · **Lattice:** BCC (canonical) · **Law:** n/a (fermion walk) · **Units:** lattice

**Does:** the canonical massive Dirac walk: the 4×4 one-tick unitary built from the BCC Weyl block, its exact dispersion, and a Lorentz-scalar variable-mass (confinement) Strang step.

$A_k$ is `bcc.bcc_unitary` (bcc.py:L156–172): $A_k=uI-i\,\mathbf n\cdot\boldsymbol\sigma$ with, for branch $s=\pm1$ and $c_i=\cos(k_i c_\text{lat})$, $s_i=\sin(k_i c_\text{lat})$, $c_\text{lat}=1/\sqrt3$ (F26):
$u=c_xc_yc_z+s\,s_xs_ys_z$, $n_x=s_xc_yc_z-s\,c_xs_ys_z$, $n_y=-s\,c_xs_yc_z+s_xc_ys_z$, $n_z=c_xc_ys_z+s\,s_xs_yc_z$ (bcc.py:L107–110 `_bcc_uvec`).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $D_k=\begin{pmatrix} nA_k & imI\\ imI & nA_k^\dagger\end{pmatrix}$, $n=\sqrt{1-m^2}$ | one-tick BCC Dirac unitary (default branch $+$) | `dirac_bcc.py:L123–126 _apply_D_k()`; dense form `L266–270 build_D_k_matrix()` | unknown (inferred: exact) |
| 2 | $\omega_k=\arccos\!\big(n\,u(k)\big)$ | BCC Dirac dispersion, eigenvalues $e^{\pm i\omega_k}$, twofold. Spot-checked here at $k=(0.4,-0.7,0.9)$, $m=0.3$: the eigenphases of `build_D_k_matrix` equal $\pm0.797531154002$, which matches the formula to $10^{-12}$ | `dirac_bcc.py:L92 bcc_dirac_dispersion()` | unknown (inferred: exact) |
| 3 | $\omega(0)=\arcsin m$; the small-$k$ form $\cos\omega\approx n(1-\lvert k\rvert^2/6)$ gives $\omega^2\approx m^2+(1-m^2)\lvert k\rvert^2/3$ at leading order in $m$, i.e. $c=c_\text{lat}=1/\sqrt3$ | rest energy and light speed | docstring L28–41 (consequence of #2; not separately computed) | unknown (inferred: exact (from #2)) |
| 4 | $U_D(k,dt)=\cos(\omega dt)I+\dfrac{\sin\omega dt}{\sin\omega}(D_k-\cos\omega I)$ | spectral interpolation | `dirac_bcc.py:L181–189 dirac_step_3d_bcc_splitstep()` | unknown (inferred: exact ($dt=1$), machine (FFT)) |
| 5 | $\mathrm{Mix}(\theta)=\cos\theta\,I-i\sin\theta\,\beta$, with $\delta m$ unbounded | Lorentz-scalar mass rotation | `dirac_bcc.py:L207–210 _mix_eta_chi_3d()` | unknown (inferred: exact (unitary)) |
| 6 | $\mathrm{Mix}(\delta m,dt/2)\circ D(m_0,dt)\circ\mathrm{Mix}(\delta m,dt/2)$, default $m_0=0$ | scalar-confinement (MIT-bag) step | `dirac_bcc.py:L238–242 dirac_step_3d_bcc_varm_splitstep()` | unknown (inferred: exact at $\delta m=0$; $O(dt^2)$ otherwise) |
| 7 | $\lVert D^\dagger D-I\rVert_F$ and $\max\lvert\arg\lambda-\omega_k\rvert$ | unitarity / dispersion verification | `dirac_bcc.py:L319–320`, `L299–302` | unknown (inferred: machine) |

**Inputs → outputs:** four complex $(L,L,L)$ arrays, $m$, $dt$, sign → updated arrays; a dense 4×4 $D_k$ at a point.
**Depends on:** `lattice/bcc` (03-lattice.md § bcc.py), `lattice/geometry.make_kgrid_3d`, `numerics.fft`, `constants.c_lat` $=1/\sqrt3$ (F26; bound here as `C_LAT_3D`, used only as a label).
**Flags:**
- ⚠ The same mix-sign convention as `dirac.py` applies: $D_k\sim e^{+i\beta\arcsin m}$ vs $\mathrm{Mix}=e^{-i\beta\delta m}$.
- The branch pairing $A_+$ with $A_+^\dagger$ differs from `gauge/weak_wmu` ($A_+$ with $A_-$), per F378 leg E1. Two massive-Dirac discretisations coexist.
- The verification uses `np.linalg.eig` on the 4×4 chiral matrix (hazard). It is guarded by an analytic dispersion comparison.
- D8: direct numpy import.

---

### `engine/particles/discrete_cpt.py` — exact discrete CPT theorem, free BCC Dirac walk (F328)
**Status:** live · standalone · **Findings:** F328 F53 F301 F327 F26 · **Lattice:** BCC · **Law:** n/a · **Units:** lattice

**Does:** builds C·P·T as one antiunitary $\Theta=MK$ on `dirac_bcc`'s $D(k)$ and proves $\Theta D\Theta^{-1}=D^{-1}$ at every $k$ and every $\lvert m\rvert\le1$. It also proves that no fixed unitary parity exists at finite $k$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M=\Sigma\,(\sigma_y\oplus\sigma_y)$, $\Sigma=\begin{pmatrix}0&I\\I&0\end{pmatrix}$; $(\Theta\psi)(x)=M\psi(-x)^*$ | the CPT operator (internal part) | `discrete_cpt.py:L140–141 M_cpt()`; real-space `L300–307 _apply_theta_realspace()` | exact (reg) |
| 2 | $\Theta^2=MM^*=-I$ | Kramers signature | `discrete_cpt.py:L151 theta_squared()`; leg C1 `L404–405` | exact (reg) |
| 3 | (I) $A^s(k)^*=\sigma_yA^s(k)\sigma_y$ | generic identity for real $(u,\mathbf n)$ | `discrete_cpt.py:L182 identity_conjugate_fixed_k_residual()` | exact (reg) |
| 4 | (I)+(II) $A^+(k)^*=A^-(-k)$ | conjugation = branch swap + momentum flip (BCC-specific) | `discrete_cpt.py:L190 identity_branch_swap_residual()` | exact (reg) |
| 5 | $M\,D(k)^*\,M=D(k)^\dagger\ (=D(k)^{-1})$ | **the theorem**, for all $k$ and $\lvert m\rvert\le1$ | `discrete_cpt.py:L204–206 cpt_operator_identity_residual()`; $D$ at `L171–173 _D()` | exact (reg) |
| 6 | $\omega(k)-\omega(-k)$, $\omega=\arccos(n\,u^+(k))$; nonzero at generic $k$, zero on the cubic axes | spectral obstruction: no fixed unitary $\Pi$ with $\Pi D(k)\Pi^{-1}=D(-k)$ | `discrete_cpt.py:L231–233 no_fixed_parity_obstruction()` | exact (reg) |
| 7 | $\lvert\Sigma D(k)\Sigma-D(-k)\rvert=O(1)$ | naive-parity negative control | `discrete_cpt.py:L245–246 naive_parity_residual()` | exact (reg) |
| 8 | $D^\dagger=\begin{pmatrix}nA^\dagger&-imI\\-imI&nA\end{pmatrix}$ round trip | plain invertibility (not an antiunitary check) | `discrete_cpt.py:L277–280 naive_reversal_residual()` | machine (reg: exact; row is weaker — see flags) |
| 9 | $D^N\Theta D^N\psi_0=\Theta\psi_0$ | end-to-end real-space FFT round trip | `discrete_cpt.py:L324–329 cpt_realspace_residual()` | machine (< $10^{-10}$) (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** $(k,m)$ samples / random fields → residual dicts; gate entry `check_discrete_cpt_theorem()` (L335) with negative control `use_naive_theta`.
**Depends on:** `dirac_bcc` (this file above), `lattice/bcc`, `numerics.xp`/`fft`.
**Flags:**
- The docstring says the theorem holds "to literal 0.0", but the gate tolerance is $10^{-10}$. The algebra is exact and the numerical check is machine precision.
- Scope is the free sector only; the gauged extension is `discrete_cpt_gauged.py`.

---

### `engine/particles/discrete_cpt_gauged.py` — CPT with SU(2)$_L$ grafted into the walk (F378)
**Status:** live · standalone · **Findings:** F378 F328 F53 F91 · **Lattice:** BCC · **Law:** n/a (uniform SU(2) link held fixed) · **Units:** lattice

**Does:** tests F328's $\Theta$ against (a) the real `weak_wmu.covariant_dirac_doublet_step` at a uniform link and (b) a construction that grafts SU(2) into `dirac_bcc`'s architecture. The kinetic-only extension is proved exact, and the SU(2)-gauged mass sector is proved to obstruct it.

Basis: $[f_\nu,f_e,g_\nu,g_e\,\vert\,cf_\nu,cf_e,cg_\nu,cg_e]$ (spin-major, isospin-minor).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $D_\text{cov}=K\,\mathcal M\,K$, $K=\mathrm{diag}(A^+\otimes U,\ A^-\otimes I_2)$, $\mathcal M=\begin{pmatrix}\cos m\,I&i\sin m\,(I_2\otimes V)\\ i\sin m\,(I_2\otimes V^\dagger)&\cos m\,I\end{pmatrix}$ | closed form of the actual gauged doublet walk (branch $+$ with branch $-$). Leg X0 matches it to the real module at < $10^{-10}$ | `discrete_cpt_gauged.py:L147–160 D_covariant_doublet()` | machine (X0) (reg: exact; row is weaker — see flags) |
| 2 | $D'=\begin{pmatrix}n(A^+\otimes U)&im\,(I_2\otimes V)\\ im\,(I_2\otimes V^\dagger)&n(A^+\otimes U)^\dagger\end{pmatrix}$ ($V=I$ ⇒ scalar mass) | grafted construction in `dirac_bcc` architecture | `discrete_cpt_gauged.py:L171–184 D_grafted()` | exact (reg) |
| 3 | $M'=\Sigma_8\,(\sigma_y\otimes\Lambda\ \oplus\ \sigma_y\otimes\Lambda)$ | generalised CPT matrix; $\Lambda=\tau_2$ (or $I_2$ as a control) | `discrete_cpt_gauged.py:L191–195 M_cpt_gauged()` | exact (reg) |
| 4 | $\tau_2U\tau_2^{-1}=U^*$ for all $U\in SU(2)$ | pseudoreality (extends F328 identity I) | `discrete_cpt_gauged.py:L226–227 kinetic_isospin_identity_residual()` | exact (reg) |
| 5 | $M'D'^*M'=D'^{-1}$ ($V=I$, any $U$, $k$, $m$) | kinetic-sector CPT theorem | `discrete_cpt_gauged.py:L208–211 cpt_operator_residual()`; legs B1/B2 L344–367 | exact (reg) |
| 6 | $\Theta'^2=M'M'^*=+I$ | involution class flips from Kramers $-1$ to $+1$ | `discrete_cpt_gauged.py:L203 theta_squared()`; leg C1 L378 | exact (reg) |
| 7 | the mass sector needs $\Lambda V^T\Lambda^{-1}=V$ for all $V$, which is impossible (an anti-automorphism equals the identity only on abelian groups) | mass-sector no-go | `discrete_cpt_gauged.py:L240–241 mass_isospin_required_identity_residual()`; legs D2/D3 L399–431 | exact (reg) |
| 8 | $\tau_2V^T\tau_2^{-1}=V^{-1}$ | neighbouring true identity | `discrete_cpt_gauged.py:L249–250` | exact (reg) |
| 9 | $\lvert M_\text{iso}D_\text{cov}^*M_\text{iso}-D_\text{cov}^{-1}\rvert>1$ at $U=V=I$ | the real module fails F328's identity already at zero coupling | leg E1 `discrete_cpt_gauged.py:L322–333` | exact (reg) |

**Inputs → outputs:** random $(k,m,U,V)$ → gate dict via `check_gauged_cpt_theorem()` (L266).
**Depends on:** `lattice/bcc`, `gauge/weak_wmu.covariant_dirac_doublet_step` (05c-gauge § weak_wmu), `numerics.xp`.
**Flags:**
- OTHER (architecture): two massive-Dirac discretisations coexist. `dirac_bcc` pairs $A^+$ with $A^{+\dagger}$ in one un-split tick. `weak_wmu` pairs $A^+$ with $A^-$ as a $K\mathcal MK$ Strang sandwich with rotation mass $\cos m$/$\sin m$ rather than $n$/$m$. This is named in the module and not resolved.
- Mass-link fixed-background scope only (docstring L77–95).

---

### `engine/particles/eg_sextic.py` — induced $E_g$ sextic brake $\lambda_6$ and $C/\lvert B\rvert$ pipeline
**Status:** live · test-only · **Findings:** — (registry empty; the code cites F95, F118, F145, F176, F177, F179, F198) · **Lattice:** BCC (sea loop), cubic FFT grid (gap) · **Law:** n/a · **Units:** lattice

**Does:** assembles the cubic Landau invariant $B$ from the full-BZ Dirac-sea loop, the saturation amplitude $e^6$, the IR coupling $\alpha^*_\text{eff}$ from a gap solve, and $\lambda_6$ as an "induced" coupling, then value-discriminates $C/\lvert B\rvert$ between $1/(2\cos\tfrac23)$ and $2/\pi$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $f(m)=-\tfrac12\sum_{s=\pm}\langle\arccos(n\cos\omega_s(k))\rangle_\text{BZ}$ | Dirac-sea energy per generation, both BCC branches | `eg_sextic.py:L83–88 _f_of_m()` | unknown |
| 2 | $y_a=\bar y+\sqrt2\,\bar y\cos(\delta+2\pi a/3)$, $m_a=y_a^2$, $F(\delta)=\sum_af(m_a)$ | equipartition circle | `eg_sextic.py:L101–109 sea_invariants()` | unknown |
| 3 | $\hat B=2\langle F_c\cos3\delta\rangle$, $C_6=2\langle F_c\cos6\delta\rangle$, $C_\text{sea}=2C_6$ | Fourier projection → cubic $B$, the sea's own sextic (negative) | `eg_sextic.py:L112–114` | unknown (inferred: quantitative) |
| 4 | $e^2=3\bar y^2$, $e^6=27\bar y^6$, $\bar y_\text{sat}=1/(1+\sqrt2)=\sqrt2-1$ | saturation amplitude (unitarity cap) | `eg_sextic.py:L65`, `L115–116` | unknown (inferred: exact) |
| 5 | $B_\text{lead}=-3\sqrt2\,I_2\,\bar y^4$, $I_2=\langle\cot\omega\rangle_\text{BCC}$ ($k=0$ excluded) | leading-form cross-check (F95) | `eg_sextic.py:L125`, `L137 i2_lattice()` | unknown (inferred: quantitative) |
| 6 | $G_S=\tfrac29\,(g^2/2)/(K+M_g^2)$, $g^2=4\pi\alpha$; $M\leftarrow\tfrac12M+\tfrac12\max\!\big(0,\ 24\,\mathcal F^{-1}[\hat G_S\,\widehat{M/\sqrt{K+M^2}}]/L^3\big)$ | damped self-consistent gap field $M(k)$ | `eg_sextic.py:L162–172 _saturated_M_field()` | unknown (inferred: quantitative) |
| 7 | $\lambda_6=c_\text{fierz}\cdot c_\text{quartic}=\tfrac29\,c$, with $c=1.10$ (band $[0.75,1.20]$) | "induced" sextic brake | `eg_sextic.py:L208 induced_lambda6()` | fit ($c$ is the F118 fit) |
| 8 | $C/\lvert B\rvert=\lambda_6e^6/\lvert B\rvert$; targets $1/(2\cos3\delta^*)=1/(2\cos\tfrac23)$ and $2/\pi$ | assembly / discrimination | `eg_sextic.py:L236–238`, `L61–62` | unknown (inferred: quantitative) |
| 9 | $c_\text{needed}=T\,\lvert B\rvert/(e^6\,c_\text{fierz})$ | inverse quartic for each target | `eg_sextic.py:L251–252 assemble()` | unknown (inferred: quantitative) |

Constants: $c_\text{fierz}=\text{c\_fierz\_colour}=2/9$ (exact, F77/F116/F256). $\cos3\delta^*=\cos(2/3)$ with $\delta^*=2/9$ (exact, F175/F253). $\lambda_6=0.243$ (quantitative, F234/F253/F256; used only as a comparison).

**Inputs → outputs:** $(L_\text{sea},L_\text{gap},\bar y)$ → dict of $B$, $e^6$, $\alpha^*$ band, $\lambda_6$, $C/\lvert B\rvert$ band.
**Depends on:** `lattice/bcc.bcc_dispersion`, `interactions/running_gap_solve`, `interactions/running_njl` (07b/07c), `constants` (01-constants.md).
**Flags:**
- ⚠ DOC/CODE MISMATCH: the module docstring (L20–24) states $\lambda_6=\tfrac29(g^2/2)J_\text{sat}/M_g^2$. The code computes $\lambda_6=\tfrac29\,c_\text{quartic}$ (L208), and the $J$ moments are "reported for transparency, not used".
- SUPERSEDED (de facto, unrecorded) by F253/F255/F256 (S6, Core decision 7): $\lambda_6$ is an **output** of $\delta^*=2/9$ via the F234 arrow. F256 proves the dynamical Landau route cannot lock $3\delta^*=Q$, and the `c_fierz_colour` provenance names 2/9 as a value $\lambda_6$ is proved **not** to take. The module is not listed in `supersessions.yaml`.
- Magic literals: `24.0` in the gap update (L167; `M0_TARGET * 0 +` is dead arithmetic), `C_QUARTIC_F118 = 1.10`, and the band.
- D8: direct numpy import.

---

### `engine/particles/element.py` — modular element assembler $E(Z,N)$ (F148)
**Status:** live · test-only · **Findings:** — (registry empty; the code cites F148, F122, F125, F113, F126, F128, F104) · **Lattice:** n/a (continuum radial / variational solvers) · **Law:** n/a · **Units:** MeV, eV

**Does:** composes a nucleus (baryon / deuteron OBE / A-body cluster) with an electron cloud (hydrogenic / Hartree) and returns a neutrality + binding stability verdict. It is mostly orchestration.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A=Z+N$; net charge $=Z_p-Z_e$ | bookkeeping | `element.py:L132`, `L353` | unknown (inferred: exact) |
| 2 | $E_b(A{=}1)=0$; $E_b(pn)=$ `nuclear.solve_deuteron(core="derived", b=0.55, tensor, σ with $g^2/4\pi=$SIGMA_G2_4PI_BARE, ω with $g^2/4\pi=5.39$)`; $A\ge3$: `manybody.nuclear_binding_Abody` | nuclear binding dispatch | `element.py:L175–203 Nucleus.binding_energy()` | unknown (inferred: quantitative) |
| 3 | $\mu=m_em_N/(m_e+m_N)$, $m_N(Z{>}1)=Z(m_p+m_n)/2$; the Z=1 ground state is the `atom.hydrogen_spectrum` 1s level | electron energy | `element.py:L291–295`, `L321 _z_nuclear_mass_MeV()` | unknown (inferred: quantitative) |
| 4 | $Z\ge2$: `manybody.electron_cloud_hartree` | multi-electron Hartree | `element.py:L301–303` | unknown (inferred: quantitative) |
| 5 | Madelung $(n+l)$ filling with capacities $2,6,10,14$ | Aufbau configuration | `element.py:L263–276 configuration()` | unknown (inferred: exact) |
| 6 | stable ⇔ neutral ∧ nucleus bound ∧ $E_e<0$ | verdict | `element.py:L356–371 verify_stability()` | unknown (inferred: exact (logic)) |

**Inputs → outputs:** $(Z,N)$ → `Element` with a `verify_stability()` dict.
**Depends on:** `particles/atom`, `particles/baryon_dynamics`, `particles/nuclear` (below), `core/manybody` (04-core.md), `constants.M_n_neutron_MeV` (939.56542052 MeV, external/CODATA).
**Flags:**
- ⚠ DOC/CODE MISMATCH: the docstring (L41–46, L50–53, L173, L287) says the $A\ge3$ nuclei and the $Z\ge2$ electrons raise `NotImplementedError`. The code runs `manybody.nuclear_binding_Abody` / `electron_cloud_hartree`.
- ⚠ DOC/CODE MISMATCH: "zero new parameters" (L20). The code hard-codes $g_\omega^2/4\pi=5.39$ (the empirical OBE window; nuclear.py's own default is 11.0), $b=0.55$ fm, and baryon defaults $m_q=0.785$, $\alpha_s=0.50$, $\sigma=1.0$ (L140–141, L186–188).
- The $Z>1$ reduced mass assumes $N=Z$ regardless of the actual $N$.

---

### `engine/particles/higgs.py` — complex scalar Φ with Mexican-hat potential (reference, non-canonical)
**Status:** live · package-only · **Findings:** — (registry empty; inventory row #6 cites "Finding 3") · **Lattice:** 2D square grid with **continuum** spectral Laplacian · **Law:** n/a · **Units:** lattice

**Does:** a free Klein–Gordon exact rotation step and a velocity-Verlet integrator for $\Box\Phi+\partial V/\partial\Phi^*=0$ with $V=-s\mu^2\lvert\Phi\rvert^2+\lambda\lvert\Phi\rvert^4$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\begin{pmatrix}\Phi\\\Pi\end{pmatrix}_k\mapsto\begin{pmatrix}\cos\omega dt&\frac{\sin\omega dt}{\omega}\\-\omega\sin\omega dt&\cos\omega dt\end{pmatrix}\begin{pmatrix}\Phi\\\Pi\end{pmatrix}_k$, $\omega=\sqrt{k^2+m^2}$ | exact free-KG step (continuum dispersion on the FFT grid) | `higgs.py:L57–69 kg_step_free_2d_splitstep()` | unknown (inferred: machine) |
| 2 | $F(\Phi)=\nabla^2\Phi-(-s\mu^2+2\lambda\lvert\Phi\rvert^2)\Phi$, $\nabla^2\to-k^2$ spectrally; $s=+1$ broken, $-1$ symmetric | force | `higgs.py:L159–163 _force()`, `L138 _laplacian_2d()` | unknown (inferred: machine) |
| 3 | $\Pi_{1/2}=\Pi+\tfrac{dt}2F(\Phi)$, $\Phi'=\Phi+dt\,\Pi_{1/2}$, $\Pi'=\Pi_{1/2}+\tfrac{dt}2F(\Phi')$ | velocity-Verlet (symplectic, $O(dt^2)$) | `higgs.py:L194–199 kg_step_strang()` | unknown (inferred: quantitative) |
| 4 | $\Pi\to\Pi-dt\,[(-s\mu^2+2\lambda\lvert\Phi\rvert^2)-m_0^2]\Phi$ | nonlinear-residual kick (not called by #3) | `higgs.py:L121–128 kg_nonlinear_kick()` | unknown |
| 5 | $v^2=\mu^2/(2\lambda)$; $(\Phi,\Pi)=(v,0)$ is a fixed point | vacuum | `higgs.py:L212 verify_vacuum_fixed_point()` | unknown (inferred: exact) |
| 6 | radial $\omega=\sqrt{k^2+2\mu^2}$ ($m_h^2=2\mu^2$), Goldstone $\omega=\lvert k\rvert$ | small-oscillation dispersion targets | `higgs.py:L259`, `L270`, `L274 verify_higgs_dispersion_2d()` | quantitative (inventory #6, Goldstone) |

**Inputs → outputs:** $(\Phi,\Pi)$ complex arrays, $\mu^2,\lambda$, phase → updated pair; verification dicts.
**Depends on:** `numerics.fft`.
**Flags:**
- OTHER: a Higgs scalar sits against Core decision 3 (hypercharge on $U(x)$, "avoiding any need for the Higgs field"). The module is package-only (unreached) and is not recorded in `supersessions.yaml`. Treat it as a reference/regression artifact, not model physics.
- ⚠ DOC/CODE MISMATCH: the docstring (L19–24) describes the propagator as a Strang split of an FFT-exact linear step with $m_0^2=2\mu^2$ and a kick. `kg_step_strang` is actually plain velocity-Verlet with the full force, and `kg_nonlinear_kick` is unused there.
- The Laplacian and dispersion are continuum $-k^2$ on the grid, not a lattice stencil and not BCC.

---

### `engine/particles/hyperfine.py` — hydrogen 21 cm and Lamb-shift completeness (F262)
**Status:** live · test-only · **Findings:** — (registry empty; the code cites F262, F252, F257) · **Lattice:** n/a · **Law:** n/a · **Units:** SI (eV, MHz, fm)

**Does:** closed-form arithmetic for the hydrogen Fermi-contact hyperfine splitting and the recoil / finite-size additions to the one-loop Lamb shift.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $m_r/m_e=m_p/(m_e+m_p)$ | reduced-mass ratio | `hyperfine.py:L71 reduced_mass_ratio()` | unknown (inferred: exact) |
| 2 | $a_e=\alpha/2\pi$ | Schwinger anomaly (always computed, never pulled from the loop) | `hyperfine.py:L77 a_e_schwinger()` | unknown (inferred: exact) |
| 3 | $\Delta E_F=\tfrac43g_p(m_e/m_p)\alpha^4m_ec^2\cdot(m_r/m_e)^3(1+a_e)$ | 21 cm splitting | `hyperfine.py:L98–102 hydrogen_21cm()` | quantitative (inventory #303: $5.8\times10^{-5}$) |
| 4 | $\Delta E_\text{fs}(2s)=\tfrac1{12}\alpha^4m_rc^2(m_rcr_p/\hbar)^2$ | finite-size 2s shift; $d\ln/d\ln r_p=2$ | `hyperfine.py:L142–145 finite_size_shift_2s()` | unknown (inferred: quantitative (#304)) |
| 5 | $\Delta_\text{red}=E_\text{Lamb}[(m_r/m_e)^3-1]$; $+0.36$ MHz (EGS pure recoil, cited) | recoil | `hyperfine.py:L168`, `L171 recoil_correction_MHz()` | unknown (inferred: quantitative (#305)) |
| 6 | $E=E_\text{F252/F257}+\Delta_\text{fs}+\Delta_\text{rec}$ | Lamb assembly; the fallback baseline is 1052.28 MHz | `hyperfine.py:L189 lamb_complete()`, `L127` | unknown (inferred: quantitative) |

**Inputs → outputs:** $g_p$, $r_p$ → dicts in MHz.
**Depends on:** `interactions/qed_vertex_loop.lamb_shift` (07-interactions QED).
**Flags:**
- OTHER (D7): CODATA/PDG literals are hard-coded (`ALPHA`, `M_E_MEV`, `M_P_MEV`, `H_EV_S`, `HBARC`, $g_p$, $r_p$) rather than imported from `casim.constants`.
- ⚠ DOC/CODE MISMATCH: `a_e_schwinger` says "Pulled from the model's own vertex loop if available", but it always returns $\alpha/2\pi$.
- The $+0.36$ MHz recoil value is a cited literature number.

---

### `engine/particles/induced_stiffness.py` — induced gauge stiffness: one-loop polarisation on the BCC walk (F138/F141/F149/F153)
**Status:** live · test-only · **Findings:** — (registry empty; the code cites F138, F141 U2, F51, F34/F35, F46, F149, F153) · **Lattice:** BCC (lattice coords $q=k/\sqrt3\in(-\pi,\pi]^3$, 8 body-diagonal hops) · **Law:** vector (U(1)/SU(2) Cartan) and staggered (F51 hypercharge) channels · **Units:** lattice

**Does:** computes the static sea polarisation $\chi(\tilde q)$ of the free Weyl and massive Dirac walks under a Peierls-gauged vector field and under the parity-charged staggered field. It uses cut-free circle perturbation theory, validated against dense real-space gauged operators.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A(q)=\sum_{d\in\{\pm1\}^3}e^{id\cdot q}C_d$ | exact 8-hop decomposition (sampling inversion on $q_i\in\{0,\pi/2\}$) | `induced_stiffness.py:L101–112 hop_matrices()` | unknown (inferred: exact (residual check L124)) |
| 2 | $u(q+Q)=-u(q)$, $\mathbf n(q+Q)=-\mathbf n(q)$ ⇒ $\omega(q+Q)=\pi-\omega(q)$, $Q=(\pi,\pi,\pi)$ | parity theorem (F51 S1) | `induced_stiffness.py:L135–141 parity_theorem_residual()` | unknown (inferred: exact) |
| 3 | $V(q_m)=i\sum_d(d\cdot\hat e)e^{id\cdot q_m}C_d$ | midpoint Peierls vertex | `induced_stiffness.py:L175–178 vertex_one_tick()` | unknown (inferred: exact) |
| 4 | $\delta W_2^\text{vec}=W(q+\tilde q)V+VW(q)$; $\delta W_2^\text{stag}=W(q+\tilde q+Q)V-VW(q)$, $V=V(q+\tilde q/2)$ | two-tick $O(\varepsilon)$ vertex per channel | `induced_stiffness.py:L195`, `L198 vertex_W2()` | unknown (inferred: exact) |
| 5 | one-tick sea: occupied $\lvert-\rangle$, $\Omega=\mathrm{wrap}(\mp2\omega)$; two-tick sea: occupied $\Omega\in(-\pi,0]$ | sea conventions | `induced_stiffness.py:L213–223 bands()` | unknown (inferred: exact) |
| 6 | $\chi=\frac1N\sum_q\lvert K_{eo}\rvert^2\cot(\Delta\Omega/2)$, $K_{eo}=ie^{i\Omega_o}\langle e\rvert\delta W_2\lvert o\rangle$ | paramagnetic bubble (circle PT) | `induced_stiffness.py:L271–286 polarization()` | unknown (inferred: quantitative) |
| 7 | $\chi_\text{bf}=-[E(\varepsilon)+E(-\varepsilon)-2E(0)]/(\varepsilon^2N)$ | dense real-space brute force (twisted BC) | `induced_stiffness.py:L347–348 brute_force_chi()` | unknown (inferred: quantitative) |
| 8 | $W_2^\Lambda=e^{i\hat\Lambda\hat P}W_2e^{-i\hat\Lambda\hat P}$ ⇒ $E$ invariant | Ward check of two-tick gauging | `induced_stiffness.py:L397–398 gauge_invariance_residual()` | unknown (inferred: machine) |
| 9 | $\lvert M_\text{stag}\rvert=\lvert M_\text{vec}\rvert$ and equal gaps in the two-tick sea | channel-equality theorem | `induced_stiffness.py:L443–445 channel_equality_residual()` | unknown (inferred: exact (machine-zero)) |
| 10 | $\chi/\tilde q^2=C\ln(1/\tilde q)+c$ | IR-log fit | `induced_stiffness.py:L464–469 log_fit()` | fit |
| 11 | $D(q)=\begin{pmatrix}nA&im\\im&nA^\dagger\end{pmatrix}$; $\omega_m(q+Q)=\pi-\omega_m(q)$; $D(q+Q)=-XD(q)X$, $X=\mathrm{diag}(I,-I)$ | massive walk and its parity theorem | `induced_stiffness.py:L495–500`, `L515–519 dirac_parity_residuals()` | unknown (inferred: exact) |
| 12 | $V_4=\mathrm{diag}\big(nV_A,\ n\,i\textstyle\sum_d(d\cdot\hat e)e^{id\cdot q}C_{-d}^\dagger\big)$ | Dirac hop vertex | `induced_stiffness.py:L536–545 _dirac_vertex4()` | unknown (inferred: exact) |
| 13 | $\{S,D_A\}=0$, $S=\hat P\hat X$ | bipartite closure of the gauged massive walk | `induced_stiffness.py:L722 dirac_S_anticommutation()` | unknown (inferred: machine) |
| 14 | $G_A=-\tfrac14\sum_d(\hat e\cdot d)^2e^{id\cdot q}C_d$; $\delta^2D_2=DG_4+G_4D+\tfrac14[V_4(q+\tilde q/2)^2+V_4(q-\tilde q/2)^2]$ | charge-blind diamagnetic (seagull) operator (F153) | `induced_stiffness.py:L758`, `L776 dirac_d2_transfer0()` | machine (inventory F153-D2) |
| 15 | $\chi_\text{dia}=\frac1{N}\sum_q\mathrm{Re}[ie^{i\Omega_o}\mathrm{Tr}(P_\text{occ}\delta^2D_2)]$ | diamagnetic sea response | `induced_stiffness.py:L795–796 dirac_chi_diamagnetic()` | unknown (inferred: quantitative) |

**Inputs → outputs:** $(L,\tilde q,\hat e,\text{channel},\text{sea},m)$ → $\chi$ values, residuals, fits.
**Depends on:** `lattice/bcc` (`bcc_unitary`, `_bcc_uvec`).
**Flags:**
- Chiral-transform hazard: `dirac_bands` (L572, L584) uses `np.linalg.eig`/`inv` on the 4×4 Dirac matrix to build projectors. It is guarded by an analytic $\arccos(nu)$ dispersion residual. The docstring's "no np.linalg on the 2×2 chiral structure" holds for the Weyl path only.
- Registry exactness is None.
- D8: direct numpy import.

---

### `engine/particles/majorana.py` — three-generation Higgs-free see-saw and PMNS (F236/F353)
**Status:** live · test-only · **Findings:** — (registry empty; the code cites F47, F93, F76, F201, F236, F353) · **Lattice:** n/a · **Law:** n/a · **Units:** any mass unit (GeV in callers)

**Does:** builds the 6×6 type-I see-saw with $E_g$-textured diagonal $M_R$ (+ $T_{2g}$ off-diagonal mixing), and Takagi-factorises the light block into masses, the PMNS angles, the Jarlskog invariant and $\sin\delta_{CP}$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $s_a=1+\sqrt2\cos(\delta+2\pi a/3)$ | $Z_3$ √-mass texture | `majorana.py:L61–63 z3_sqrt_texture()` | unknown (inferred: exact) |
| 2 | $M=\text{scale}\cdot\mathrm{diag}(s_a^2)$ | $E_g$-diagonal mass matrix | `majorana.py:L73–74 eg_diagonal_matrix()` | unknown (inferred: exact) |
| 3 | $T_{2g}=\begin{pmatrix}0&t_{xy}&t_{zx}\\t_{xy}&0&t_{yz}\\t_{zx}&t_{yz}&0\end{pmatrix}$ | axis-mixing (PMNS source) | `majorana.py:L94–100` | unknown (inferred: exact) |
| 4 | $M_6=\begin{pmatrix}0&M_D\\M_D^T&M_R\end{pmatrix}$ | see-saw matrix | `majorana.py:L112–116 seesaw_6x6()` | unknown (inferred: exact) |
| 5 | $m_\nu=-M_DM_R^{-1}M_D^T$ | type-I light block | `majorana.py:L123 light_mass_matrix()` | unknown (inferred: exact) |
| 6 | real branch: $\lvert\text{eig}\rvert$ of `eigh`; complex branch: SVD $m_\nu=W\Sigma V^\dagger$, $\Phi=V^TW$, $U=W\,\mathrm{diag}(e^{-i\arg\Phi_{ii}/2})$ | Takagi factorisation $m_\nu=U\,\mathrm{diag}(m)U^T$ | `majorana.py:L170–193 takagi_light_masses()` | unknown (inferred: machine (reconstruction residual)) |
| 7 | $s_{13}=\lvert U_{e3}\rvert$, $s_{12}=\lvert U_{e2}\rvert/c_{13}$, $s_{23}=\lvert U_{\mu3}\rvert/c_{13}$ | PDG angles | `majorana.py:L205–211 pmns_angles()` | unknown (inferred: exact) |
| 8 | $J=\mathrm{Im}(U_{e1}U_{\mu2}U_{e2}^*U_{\mu1}^*)$; $\sin\delta=J/(s_{12}c_{12}s_{13}c_{13}^2s_{23}c_{23})$ | CP invariants | `majorana.py:L225`, `L239–243` | unknown (inferred: exact) |
| 9 | $U_\text{PMNS}=U_e^\dagger U_\nu$; light-6×6 vs type-I consistency | pipeline | `majorana.py:L272–292 three_gen_seesaw()` | unknown (inferred: quantitative) |

**Inputs → outputs:** $M_D$ diag, $\delta_\nu$, $M_{R0}$, $t_{2g}$ → masses, $\Delta m^2$, angles, $\lvert U\rvert$, residuals.
**Depends on:** numpy only.
**Flags:**
- ⚠ DOC/CODE MISMATCH: the module docstring (L16) writes $\sqrt{M_a}=M_{R0}[1+\sqrt2\cos(\cdot)]$. The code gives $M_a=M_{R0}\,s_a^2$, i.e. $\sqrt{M_a}=\sqrt{M_{R0}}\,s_a$.
- The F47 single-flavour Majorana *step* is not in this module (the docstring says "promotes" it).
- D8: direct numpy import.

---

### `engine/particles/meson.py` — dynamical NJL mesons: π, σ, ρ (P3; F77/F74)
**Status:** live · driven (3 ch) · **Findings:** — (registry empty; the code cites F77, F74, F103) · **Lattice:** continuum 3-momentum cutoff; real-space demo on a simple-cubic tight-binding lattice (reference) · **Law:** n/a · **Units:** GeV (NJL); lattice $t$ (demo)

**Does:** the SU(2) NJL gap equation, RPA meson poles (Goldstone π, σ at $2m_c$), $f_\pi$, condensate, GMOR, KSRF ρ mass, and a Koster–Slater contact-well bound state.

$N_c=3$, $N_f=2$. Canonical parameters: $\Lambda=$`Lambda_NJL_GeV` (0.6515 GeV, external/fit, F77/F116), $G\Lambda^2=$`G_Lambda2_NJL` $=2.10$ (external/fit), $m_0=0.0055$ GeV (literal).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $I_1=\frac1{4\pi^2}[\Lambda E_\Lambda-M^2\ln\frac{\Lambda+E_\Lambda}M]$ | tadpole | `meson.py:L81 I1_closed()` | unknown (inferred: exact) |
| 2 | $K(0)=\frac1{8\pi^2}[\ln\frac{\Lambda+E_\Lambda}M-\frac\Lambda{E_\Lambda}]$; $K(q^2)=\frac1{2\pi^2}\int_0^\Lambda\frac{p^2dp}{E(4E^2-q^2)}$ | bubble | `meson.py:L87`, `L94 K_quad()` | unknown (inferred: exact / quantitative (quadrature)) |
| 3 | $M=m_0+4GN_cN_fM\,I_1(M)$ | gap equation (damped fixed point) | `meson.py:L104–107 gap_solve()` | unknown (inferred: machine) |
| 4 | $G_c\Lambda^2=\pi^2/(N_cN_f)=\pi^2/6$ | χSB onset | `meson.py:L113 G_critical()` | exact (inventory #160) |
| 5 | $\Pi_\text{PS}=2N_cN_f[I_1+q^2K]$, $\Pi_S=2N_cN_f[I_1+(q^2-4M^2)K]$; pole at $1-2G\Pi=0$ | RPA meson poles | `meson.py:L123`, `L127`, `L134–149 meson_pole()` | quantitative; Goldstone identity exact (inventory #61/#154) |
| 6 | $f_\pi^2=4N_cM^2K(0)$; $\langle\bar qq\rangle_f=-2N_cMI_1$ | decay constant, condensate | `meson.py:L157`, `L162` | unknown (inferred: exact (closed form)) |
| 7 | $m_\pi^2f_\pi^2=-m_0\langle\bar qq\rangle_\text{tot}$ | GMOR residual | `meson.py:L167–171 gmor_residual()` | unknown (inferred: quantitative) |
| 8 | $m_\rho=\sqrt2\,g_{\rho\pi\pi}f_\pi$ | KSRF; `g_rho_pi_pi` $=6.0$ (external, PDG) | `meson.py:L183 rho_mass_ksrf()` | unknown (inferred: quantitative (Tier-3)) |
| 9 | $\varepsilon(k)=2t\sum_i(1-\cos k_i)$; $1=g\langle1/(\varepsilon+E_b)\rangle$; $g_c=2t/W_3$ | contact-well secular root; Watson threshold | `meson.py:L204`, `L210`, `L197 watson_gc()` | unknown (inferred: machine (secular vs dense)) |
| 10 | $H=6t\,\delta_{ij}-t\sum_\text{nn}-g\,\delta_{i0}$ | dense real-space check | `meson.py:L235–240 relcoord_dense()` | unknown (inferred: machine) |

**Inputs → outputs:** $(\Lambda,G\Lambda^2,m_0)$ → $m_c,m_\pi,m_\sigma,m_\rho,f_\pi,\langle\bar qq\rangle$, GMOR.
**Depends on:** `constants` (strong sector).
**Flags:**
- Unregistered literals: $m_0=0.0055$ GeV (L65) and `WATSON3 = 0.5054620197` (L196).
- The real-space demo is simple-cubic, not BCC (D1 reference).
- D8: direct numpy import.

---

### `engine/particles/nuclear.py` — deuteron: coupled $^3S_1$–$^3D_1$ one-boson exchange (P4; F104/F113/F126/F128)
**Status:** live · driven (9 ch) · **Findings:** — (registry empty; the code cites F74, F103, F104, F113, F115, F126, F128) · **Lattice:** n/a (1D finite-difference radial grid) · **Law:** n/a · **Units:** MeV, fm ($\hbar c=197.32698$ MeV·fm literal)

**Does:** solves the two-channel radial deuteron Hamiltonian with OPEP (central + tensor), an optional derived quark-Pauli core, σ attraction and ω repulsion. It also tunes $r_c$, $b$ or $g_\sigma$ to $E_b=2.224$ MeV.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $V_\text{core}=g_\text{cm}\big[\frac{N_0+N_1u+N_2u^2+N_3u^3}{D_0+D_1u+D_2u^2+D_3u^3}+16\big]$, $u=e^{-r^2/4b^2}$, $N=(-13436928,15925248,15925248,-13436928)$, $D=(839808,93312,93312,839808)$ | derived F113 repulsive core; $V(0)=\tfrac{56}3g_\text{cm}$, $V(\infty)=0$ | `nuclear.py:L101–104 derived_core_potential()` | exact coefficients (inventory F113-C/D); $g_\text{cm}=18.31$ MeV input |
| 2 | $\tilde Y=\frac{e^{(a\beta)^2}}{2r}\big[e^{-ar}\mathrm{erfc}(a\beta-\tfrac r{2\beta})-e^{ar}\mathrm{erfc}(a\beta+\tfrac r{2\beta})\big]$, $a=m/\hbar c$ | Gaussian-folded Yukawa | `nuclear.py:L136–140 folded_yukawa()` | unknown (inferred: exact) |
| 3 | $V_\sigma=-(g^2/4\pi)m_\sigma\tilde Y$; $g_{\sigma NN}^2/4\pi=9(m_c/f_\pi)^2/4\pi$ | σ attraction ($m_c=$`M0_constituent_MeV` 311.2, $f_\pi=$`f_pi_anchor_MeV` 92.07 ⇒ 8.182; $m_\sigma=622.4$ literal) | `nuclear.py:L147`, `L125` | unknown (inferred: quantitative) |
| 4 | $V_\omega=+(g^2/4\pi)m_\omega\tilde Y$, default $g^2/4\pi=11.0$, $m_\omega=782.66$ | ω repulsion (sign flip for like baryon charge) | `nuclear.py:L176 omega_exchange_potential()` | unknown (inferred: quantitative) |
| 5 | $\langle S_{12}\rangle=\begin{pmatrix}0&2\sqrt2\\2\sqrt2&-2\end{pmatrix}$ via CG + sphere quadrature | tensor spin-angular matrix | `nuclear.py:L240–276 tensor_matrix_via_construction()`, analytic `L287` | exact (inventory F104-P4-A) |
| 6 | $Y=e^{-x}/x$, $T=(1+3/x+3/x^2)e^{-x}/x$, $x=m_\pi r/\hbar c$ | OPEP radial forms | `nuclear.py:L294`, `L298` | unknown (inferred: exact) |
| 7 | $f^2/4\pi=(g_Am_\pi/2f_\pi)^2/4\pi$ | Goldberger–Treiman πNN (`g_A` 1.2723 external; $m_\pi=138.039$ literal) | `nuclear.py:L303–304 f2_over_4pi()` | unknown (inferred: exact (formula)) |
| 8 | $H=\begin{pmatrix}K+V_{SS}&V_{SD}\\V_{SD}&K+6\hbar^2/(2\mu r^2)+V_{DD}\end{pmatrix}$, $V_{SS}=-V_0Y+V_c+V_\sigma+V_\omega$, $V_{SD}=2\sqrt2(-V_0T)$, $V_{DD}=-V_0Y-2(-V_0T)+V_c+\dots$, $V_0=(f^2/4\pi)m_\pi$, $\mu=M_N/2$, $K=\frac{\hbar^2}{2\mu}(-d^2/dr^2)_\text{FD}$ | coupled-channel Hamiltonian; derived core regularises OPEP by $[1-e^{-(r/b)^2}]^2$ | `nuclear.py:L331–382 solve_deuteron()` | unknown (inferred: quantitative) |
| 9 | $E_b=-E_0$, $P_D=\sum w^2/\sum(u^2+w^2)$, $\kappa=\sqrt{2\mu E_b}/\hbar c$, $r_d=\tfrac12r_\text{rms}$ | observables | `nuclear.py:L384–399` | unknown (inferred: quantitative) |
| 10 | bisection of $r_c$ / $b$ / $g_\sigma^2$ to $E_b=2.224$ MeV | tuning knobs | `nuclear.py:L413–460` | fit |

**Inputs → outputs:** $(r_c\text{ or }b,\ \text{channel switches},\ \text{couplings})$ → $E_b$, $P_D$, $\kappa$, wavefunctions.
**Depends on:** `constants` (`M_N_isoaveraged_MeV` 938.918 external; `g_A`; `M0_constituent_MeV`; `f_pi_anchor_MeV`), `nuclear_core.py` (source of #1's coefficients).
**Flags:**
- The σ comment (L117) says $g^2/4\pi=8.09$, but the code value is 8.182 (element.py comment: 8.182).
- ω default 11.0 here vs 5.39 passed by element.py.
- Unregistered literals: `HBARC`, `M_PI_DEFAULT`, `GCM_DEFAULT`, `B_QUARK_DEFAULT`, `M_SIGMA_DEFAULT`, `M_OMEGA_DEFAULT`, `OMEGA_G2_4PI_OBE`.
- The module docstring still describes $r_c$ as "the one tuned knob". With the derived core, $b$ or $g_\sigma$ is tuned instead.

---

### `engine/particles/nuclear_core.py` — derived NN short-range core from six-quark Pauli + chromomagnetism (F113)
**Status:** live · test-only · **Findings:** — (registry empty; the code cites F113, F71, F103) · **Lattice:** n/a (exact rational algebra) · **Law:** n/a · **Units:** $g_\text{cm}$ units; MeV after calibration

**Does:** exact `Fraction` algebra over quark labels (colour ⊗ spin ⊗ flavour). It gives the nucleon and Δ chromomagnetic energies, the six-quark RGM norm kernel, and the $[6]$ full-overlap energy that sets the repulsive core. `nuclear.py`'s embedded coefficients come from here.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\psi_N=\sum\varepsilon_{abc}\otimes\psi_{SU(6)}$, with spin-flavour $2\,\mathrm{Sym}[u\!\uparrow u\!\uparrow d\!\downarrow]-\mathrm{Sym}[u\!\uparrow u\!\downarrow d\!\uparrow]$; Δ⁺⁺ $=\varepsilon_{abc}\,u\!\uparrow^3$ | nucleon / Δ wavefunctions (F71) | `nuclear_core.py:L77–117` | unknown (inferred: exact) |
| 2 | $\Phi_{T=0}=p_An_B-n_Ap_B$ ($S=1$, $S_z=1$) | deuteron-channel two-cluster state | `nuclear_core.py:L119–134 two_cluster()` | unknown (inferred: exact) |
| 3 | $H_\text{CM}=-\sum_{i<j}(2P^c_{ij}-\tfrac23)(2P^s_{ij}-1)=\sum_{i<j}[-4P^cP^s+2P^c+\tfrac43P^s-\tfrac23]$ | chromomagnetic operator via Fierz swaps | `nuclear_core.py:L186–196 H_CM()` | unknown (inferred: exact) |
| 4 | $\langle H_\text{CM}\rangle=\langle\Phi\vert H\Phi\rangle/\langle\Phi\vert\Phi\rangle$: $N=-8$, $\Delta=+8$ ⇒ $M_\Delta-M_N=16g_\text{cm}$ | single-baryon energies | `nuclear_core.py:L200 chromomagnetic_energy()` | exact (inventory F113-B) |
| 5 | $g_\text{cm}=(M_\Delta-M_N)/(E_\Delta-E_N)=293/16=18.31$ MeV | calibration (293 MeV input) | `nuclear_core.py:L264 derive_core()` | unknown (inferred: quantitative (external input)) |
| 6 | $K_m=\sum_{P:\,\text{cross}=m}\mathrm{sgn}(P)\langle\Phi\vert P\Phi\rangle$; $n(R)=\sum_mK_ms^{2m}/K_0$, $s=e^{-R^2/8b^2}$ | RGM norm kernel ($K_0=K_3=839808$, $K_1=K_2=93312$, $n(0)=20/9$) | `nuclear_core.py:L209–212 norm_kernel_coeffs()` | exact (inventory F113-C) |
| 7 | $E_6=\langle\Phi\vert H\mathcal A\Phi\rangle/\langle\Phi\vert\mathcal A\Phi\rangle=+\tfrac83$; $\Delta E=E_6-2E_N=+\tfrac{56}3g_\text{cm}$ | full-overlap $[6]$ energy → core height | `nuclear_core.py:L216–221`, `L268` | exact (inventory F113-D) |
| 8 | $\langle H_\text{CM}\rangle(R)=\sum_P\mathrm{sgn}\langle H\Phi\vert P\Phi\rangle s^{2k}\,/\,\sum_P\mathrm{sgn}\langle\Phi\vert P\Phi\rangle s^{2k}$; $V=g_\text{cm}(\langle H\rangle(R)-2E_N)$ | core profile (float) | `nuclear_core.py:L244–254 core_profile()`, `L277` | unknown (inferred: machine) |

**Inputs → outputs:** $M_\Delta-M_N$ → exact energies, kernel, $V_\text{core}(0)$, profile.
**Depends on:** stdlib only (`fractions`, `itertools`).
**Flags:**
- Consistent with `nuclear.py`: $u=e^{-r^2/4b^2}=s^2$, and the $u^k$ polynomial there is the $s^{2k}$ series here. The numerator coefficients (`_CORE_N`) are "extracted once" and not re-derived at import.
- The registry has no exactness field, although the module is exact rational algebra.

---

### `engine/particles/positronium.py` — positronium spectrum, 7/12 hyperfine and decay rates (F262)
**Status:** live · test-only · **Findings:** — (registry empty; the code cites F262, F260, F125, F27/F46, F69) · **Lattice:** n/a · **Law:** n/a · **Units:** natural ($m_e=1$) → eV/MHz/ns

**Does:** reduced-mass reduction of the $e^+e^-$ Coulomb problem through the F125 solver, closed-form hyperfine coefficients, para/ortho annihilation rates, and an Ore–Powell quadrature.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mu=m_e/2$; $E_n(\text{Ps})/E_n(\text{H}_\infty)=\tfrac12$ | reduced-mass reduction (via `atom.hydrogen_spectrum`) | `positronium.py:L85`, `L99–116 positronium_spectrum()` | exact ratio; machine grid (inventory #296) |
| 2 | $\lvert\psi_{nS}(0)\rvert^2=(Z\mu\alpha)^3/(\pi n^3)$, $\mu=\tfrac12$ | contact density | `positronium.py:L128 psi0_squared_natural()` | unknown (inferred: exact) |
| 3 | $\Delta E_{ss}=\tfrac{8\pi}3\alpha\lvert\psi(0)\rvert^2\cdot1=\tfrac13\alpha^4m$ | spin-spin Fermi contact ($g=2$) | `positronium.py:L165–166 spin_spin_contact_coeff()` | unknown (inferred: machine (#298)) |
| 4 | $\Delta E_\text{ann}=2\,(\pi\alpha)\lvert\psi(0)\rvert^2=\tfrac14\alpha^4m$ | virtual annihilation ($^3S_1$ only) | `positronium.py:L190–191 annihilation_contact_coeff()` | unknown (inferred: machine (#299)) |
| 5 | $\Delta E_\text{hfs}=(\tfrac13+\tfrac14)\alpha^4m_ec^2=\tfrac7{12}\alpha^4m_ec^2$ | ortho–para splitting | `positronium.py:L248–250 positronium_hyperfine()`; symbolic `L138–143` | unknown (inferred: exact (coefficient, #297); quantitative vs data (+0.49%, #300)) |
| 6 | $\sigma=\frac{2\pi\alpha^2}{s\beta}\big[\frac{3-\beta^4}{2\beta}\ln\frac{1+\beta}{1-\beta}-(2-\beta^2)\big]$, $s=4/(1-\beta^2)$, $\sigma v=2\beta\sigma\to\pi\alpha^2$ | threshold $e^+e^-\to2\gamma$ (Dirac closed form); plus an optional F260 trace | `positronium.py:L214–219 annihilation_coupling_from_model()` | unknown (inferred: quantitative (ratio → 1 to $4\times10^{-4}$)) |
| 7 | $\Gamma_\text{para}=4(\sigma v)\lvert\psi(0)\rvert^2=\tfrac12\alpha^5m$, with $(\sigma v)=\pi\alpha^2$ | para → 2γ | `positronium.py:L277–279 para_2gamma_rate()` | unknown (inferred: machine (coeff, #301)) |
| 8 | $\int_0^1P(x)dx=\pi^2-9$, with $P$ the Ore–Powell spectrum | 3γ phase-space integral (midpoint) | `positronium.py:L308–320 ore_powell_factor()` | unknown (inferred: quantitative (#302)) |
| 9 | $\Gamma_\text{ortho}=\frac{2(\pi^2-9)}{9\pi}\alpha^6m$ | ortho → 3γ | `positronium.py:L336–337 ortho_3gamma_rate()` | unknown (inferred: quantitative (#302)) |

**Inputs → outputs:** none (module constants) → dicts (eV, MHz, ns).
**Depends on:** `particles/atom` (F125 solver), optionally `interactions/qed_scattering.annih_M2_trace` (07-interactions QED).
**Flags:**
- ⚠ DOC/CODE MISMATCH: the para rate is described as "built from the model's annihilation cross section", but `para_2gamma_rate` hard-codes $(\sigma v)=\pi\alpha^2/m^2$ (L277). The F260 comparison lives in a separate function and does not feed the rate. Similarly, #9 uses the literal Ore–Powell factor, and the quadrature (#8) is only a side check.
- Internal docstring inconsistency: `ore_powell_factor` says $F=2(\pi^2-9)/9$ and then gives the rate factor as $2(\pi^2-9)/(9\pi)$.
- OTHER (D7): CODATA literals (`ALPHA`, `M_E_MEV`, `H_EV_S`, `HBAR_EV_S`) are not taken from `casim.constants`.

---

### `engine/particles/second_quant.py` — Jordan–Wigner Fock space, Hubbard chain and field-native gates (F217/F220)
**Status:** live · driven (0 ch) · **Findings:** — (registry empty; the code cites F214, F217, F220) · **Lattice:** 1D chain (not BCC) · **Law:** n/a · **Units:** lattice ($t$, $U$)

**Does:** a genuine fermionic Fock space on $2^{2n}$ occupation states with Jordan–Wigner operators, the Hubbard Hamiltonian, emergent super-exchange, and qubit gates executed as fermionic operators.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c_i=\sigma_z^{\otimes i}\otimes\lvert0\rangle\langle1\rvert\otimes I^{\otimes(n-i-1)}$ | JW annihilators; $\{c_i,c_j^\dagger\}=\delta_{ij}$ | `second_quant.py:L62–74 jw_annihilation()` | unknown (inferred: exact) |
| 2 | $H=-t\sum_{\langle ij\rangle\sigma}(c^\dagger_{i\sigma}c_{j\sigma}+\text{h.c.})+U\sum_in_{i\uparrow}n_{i\downarrow}$ | Hubbard chain (open BC) | `second_quant.py:L102–113 _build_H()` | unknown (inferred: exact) |
| 3 | $\psi(t)=Ve^{-iwt}V^\dagger\psi$ | exact evolution via `eigh` | `second_quant.py:L137–139 evolve()` | unknown (inferred: machine) |
| 4 | $S^+=c^\dagger_\uparrow c_\downarrow$, $S_x=\tfrac12(S^++S^-)$, $S_y=-\tfrac i2(S^+-S^-)$, $S_z=\tfrac12(n_\uparrow-n_\downarrow)$ | site spin | `second_quant.py:L150–154 spin_ops()` | unknown (inferred: exact) |
| 5 | $J=\tfrac12(\sqrt{U^2+16t^2}-U)$ | super-exchange (two-site singlet–triplet gap) | `second_quant.py:L202 superexchange_J()` | unknown (inferred: exact (closed form); ED check `L327–347` machine) |
| 6 | $t_\text{exch}=4\theta/J$ from $H_\text{eff}=(J/4)\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B$ | exchange-gate timing | `second_quant.py:L207` | unknown (inferred: exact ($U/t\to\infty$); leakage at finite $U$) |
| 7 | $R=\exp(-i\,2\theta\,\hat n\cdot\mathbf S_s)$; $H=iR(\pi/2,(1,0,1))$, $X=iR(\pi/2,\hat x)$, $Z=iR(\pi/2,\hat z)$ | exact single-qubit gates | `second_quant.py:L196–198`, `L246–254` | unknown (inferred: exact) |
| 8 | $CZ=e^{i\pi/4}\,[-X_eS_cX_eS_c]\,R_z^c(\pi/4)R_z^t(\pi/4)$, $X_e=e^{-iHt(-\pi/8)}$; $CNOT=H_tCZH_t$ | exchange-derived CNOT | `second_quant.py:L261–268 fn_cnot()` | unknown (inferred: quantitative (leakage-limited)) |
| 9 | $S=-\mathrm{Tr}\rho\ln\rho$, $\rho=CC^\dagger$ on the one-per-site sector | spin entanglement | `second_quant.py:L317–323 spin_entanglement()` | unknown (inferred: machine) |
| 10 | $(t,U)=$ (`qi_entanglement.hopping_amplitude(m)`, `mass_gap(m)` $=2\arcsin m$ per the docstring) | links to the Dirac walk | `second_quant.py:L354 hopping_and_gap()` | unknown |

**Inputs → outputs:** $(n_\text{sites},t,U)$, Fock vectors, gate programs → evolved states, $J$, entropy, register amplitudes.
**Depends on:** `interactions/qi_entanglement` (07-interactions QI).
**Flags:**
- Registry reach "driven" with 0 reachable-from channels (inconsistent labelling).
- The 1D chain is a reference geometry, not the BCC lattice.
- The mass gap $U=2\arcsin m$ is only asserted in the docstring. It is computed in `qi_entanglement`, which was not mapped here.
