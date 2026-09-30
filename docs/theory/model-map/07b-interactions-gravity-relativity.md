# Interactions — gravity, relativity and horizons

*Model-map section p07b · written 2026-09-28 - 10:00 · source of truth: the code under `src/casim/engine/interactions/` at the working-tree state of that date.*

**Scope.** The gravity field element of the production engine (`gravity.py`), the gravity-sector derivation scripts (field-equation uniqueness, four-derivative locality, band cutoff, core completeness, graviton collapse), the astrophysics kernels that consume the canonical law (TOV interior, neutron-star EoS, inspiral, horizon entropy/entanglement), the Paper-6 EMQG Poisson route and the emergent-gravity (QUMOND) falsifier, plus the special-relativity / Lorentz-violation derivations (`derive_beta_LV`, `derive_velocity_addition`, `derive_boost_covariance`, `derive_chiral_liv_bound`, `derive_f26_dispersion`, `derive_curl_subleading`, `derive_gap5_adjudication`) and one misfiled colour-dielectric module (`gravity_backreaction.py`, which is dual-Ginzburg–Landau confinement, not gravity) and `derive_dielectric_noconfine.py` (colour dielectric).

**The gravity ledger this section is checked against (CLAUDE.md decision 4, F178, supersession S3/S4).** The canonical law is the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ with structural $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ (F79/F107). The dielectric $K=e^{2u}$, $u=GM/(rc^2)=-\Phi/c^2$, $A=1/K$, $B=K$ ($AB\equiv1$) is its vacuum/weak-field representation; $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ (F106) is the static weak-field reduction; the rest-mass-sourced two-leg metric (F50/F52/F62) is superseded by F64 (S3), except F62's lapse-mix **sign**, which is still production code. **What the code does agrees with this ledger** in `gravity.py`: $\nabla^2\Phi=+(\text{coupling}\cdot c_0^2/2)\,T^{00}$ with coupling $=8\pi G/c^4\to1$, i.e. $\nabla^2\Phi=4\pi G\,T^{00}/c^2$ (attractive sign, $4\pi$ in $\Phi$, $8\pi$ in $\ln K$), and $G_\text{lat}=c_\text{lat}^4/(8\pi)=1/(72\pi)$. The mismatches found are in peripheral modules (see per-module Flags and the flags file).

**Conventions shared by the batch.**
- *Lattice (D1).* `gravity.py`, `gravity_backreaction.py` and `gravity_emqg.py` use **simple-cubic / square** nearest-neighbour stencils (the $2d$-neighbour Laplacian, continuum $-k^2$ FFT Poisson) — reference geometry, not the BCC base layer, even where a docstring says "BCC box". The BCC dispersion $u_\pm(k)=\prod_i\cos(k_i/\sqrt3)\pm\prod_i\sin(k_i/\sqrt3)$, $\omega_\pm=\arccos u_\pm$ is used by `derive_boost_covariance`, `derive_chiral_liv_bound`, `gravity_band_cutoff`, `gravity_four_derivative_locality`, `horizon_entanglement`. `derive_beta_LV` and `derive_velocity_addition` are 2-D square-lattice QCA ($c_\text{lat}=1/\sqrt2$).
- *Rotation law (F91).* "Even" $=\Omega_\text{even}(k)=\omega_+(k/2)+\omega_-(k/2)$ (photon/graviton); "chiral" $=$ one branch $\omega_s(k)$ (massive Dirac fermion, and the scalar polarisation in `gravity_four_derivative_locality`).
- *Units.* Lattice natural units $a=\tau=\hbar=1$ unless stated; the astrophysics kernels are SI/cgs/geometric ($G=c=1$). Constants from `casim.constants` are written in closed form: $c_\text{lat}=1/\sqrt3$ (F26), $G_\text{LATTICE}=c_\text{lat}^4/(8\pi)=1/(72\pi)$ (F79/F107), `F106_COEFF_LATTICE` $=8\pi G/c^4=1$ (F106/F178), $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107). CODATA-type values (`G_CODATA`, `c_SI`, `hbar_SI`, `ell_P_m`, `J_per_GeV`) are measured constants.
- *Metric sign conventions differ between modules* and are stated per block: `interior_metric.py` writes $ds^2=-A\,dt^2+B\,dr^2$ ($B=g_{rr}$), `gravity_core_completeness.py` writes $ds^2=-A\,dt^2+dr^2/B$ ($B=1/g_{rr}$).
- *Exactness* defaults to the module registry field; `None` in the registry is written `unknown`. Several `exact`-tagged derivation modules contain numerical legs (fits, quadrature, RK4); those rows are tagged `quantitative` and the tension is flagged.

**Modules covered (22):** `derive_beta_LV.py`, `derive_boost_covariance.py`, `derive_chiral_liv_bound.py`, `derive_curl_subleading.py`, `derive_dielectric_noconfine.py`, `derive_f26_dispersion.py`, `derive_gap5_adjudication.py`, `derive_velocity_addition.py`, `graviton_collapse_threshold.py`, `gravity.py`, `gravity_backreaction.py`, `gravity_band_cutoff.py`, `gravity_core_completeness.py`, `gravity_emergent.py`, `gravity_emqg.py`, `gravity_field_equation_uniqueness.py`, `gravity_four_derivative_locality.py`, `horizon_entanglement.py`, `horizon_entropy.py`, `inspiral.py`, `interior_metric.py`, `ns_eos.py`.

### `engine/interactions/derive_beta_LV.py` — SR-2 Lorentz-violation coefficients of the 2-D QCA (F12/F15)
**Status:** live · standalone · **Findings:** F12 F15 · **Lattice:** 2-D square QCA (D1 reference), $c_\text{lat}=1/\sqrt2$ · **Law:** massive single-branch Dirac, axis slice $\cos\omega=n\cos(k/\sqrt2)$ · **Units:** lattice

**Does:** closed forms for the time-dilation defect $\omega_\text{moving}/\omega_0-1/\gamma_\text{SR}=\beta_\text{LV}\beta^2+\gamma_\text{LV}\beta^4+\delta_\text{LV}\beta^6+\varepsilon_\text{LV}\beta^8$, $n=\sqrt{1-m^2}$, $\beta=v_g/c_\text{lat}$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\beta_\text{LV}=\tfrac12\big(1-\dfrac{m}{n\arcsin m}\big)$ | $\beta^2$ coefficient ($<0$; $\approx-m^2/6$) | `derive_beta_LV.py:L48 beta_LV()` | exact (inventory #20) |
| 2 | $\gamma_\text{LV}=\tfrac18-\dfrac{m(3-2m^2)}{24n^3\arcsin m}$ | $\beta^4$ | `derive_beta_LV.py:L55 gamma_LV()` | exact (reg) |
| 3 | $\delta_\text{LV}=\tfrac1{16}-\dfrac{m(8m^4-20m^2+15)}{240n^5\arcsin m}$ | $\beta^6$ | `derive_beta_LV.py:L72–73 delta_LV()` | exact (reg) |
| 4 | $\varepsilon_\text{LV}=\tfrac5{128}-\dfrac{m(35-70m^2+56m^4-16m^6)}{896n^7\arcsin m}$ | $\beta^8$ | `derive_beta_LV.py:L93–94 epsilon_LV()` | exact (reg) |
| 5 | sympy: $\omega(u)=\arccos(n\cos u)$, $R=(\omega-u\,\omega')/\arcsin m$, invert $\omega'(u)=\beta$, subtract $\sqrt{1-\beta^2}$ | symbolic confirmation (prints, returns nothing) | `derive_beta_LV.py:L113–161 symbolic_verification()` | exact (reg) |
| 6 | $\omega=\arccos(n\cos(k/\sqrt2))$, $v_g=n\sin(k/\sqrt2)/(\sqrt2\sin\omega)$, ratio $=(\omega-kv_g)/\arcsin m$ | numeric SR-2 grid | `derive_beta_LV.py:L182–198` | machine (reg: exact; row is weaker — see flags) |

**Depends on:** stdlib `math` (sympy optional). **Flags:** `C_LAT_2D=1/√2` is a literal (square-lattice $c_\text{lat}$, not a registry constant). Spot-check: $\beta_\text{LV}(0.01)=-1.66679\times10^{-5}$ vs $-m^2/6=-1.66667\times10^{-5}$.

### `engine/interactions/derive_boost_covariance.py` — finite-$a$ Poincaré defect on BCC (F301)
**Status:** live · standalone · **Findings:** F301 F22 F24 F246 F26 · **Lattice:** BCC (mpmath, 45 dps) · **Law:** both — even $\Omega_\text{even}$ and chiral branches $\omega_s$ (and massive $\arccos(n u_s)$) · **Units:** lattice, $c_\text{lat}^2=1/3$ (asserted equal to registry `c_lat` to $10^{-15}$, L141)

**Does:** measures the whole boost defect as $D_i=\partial_i\Phi$, $\Phi=(\Omega^2-c^2k^2)/(2c^2)$, with exact order and coefficient per law.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\omega^s(k,m)=\arccos\!\big(n\,u_s(k)\big)$, $u_s=\prod\cos(k_i/\sqrt3)+s\prod\sin(k_i/\sqrt3)$ | BCC branch (massive) | `derive_boost_covariance.py:L155–164 _u(), omega_branch()` | exact (reg) |
| 2 | $\Omega_\text{even}=\omega^+(k/2)+\omega^-(k/2)$; $\Omega_\text{single}=2\omega^+(k/2)$ | photon law and comparison | `derive_boost_covariance.py:L168–175` | exact (reg) |
| 3 | $D_i=\tfrac1{2c^2}\partial_i(\Omega^2)-k_i$ (mpmath numerical derivative) | Poincaré defect | `derive_boost_covariance.py:L199–200 defect()` | machine (45-dps) (reg: exact; row is weaker — see flags) |
| 4 | $D_x=-\tfrac{\lvert k\rvert^3}{36}\hat k_x(\hat k_y^2+\hat k_z^2)(1+3\hat k_y^2\hat k_z^2)$; $D\cdot\hat k=-\tfrac1{18}(p+3q)\lvert k\rvert^3$, $p=\sum\hat k_i^2\hat k_j^2$, $q=\prod\hat k_i^2$ (anchors $-2/81$ ⟨111⟩, $-1/72$ ⟨110⟩, 0 ⟨100⟩) | even-law closed form, $O(\lvert k\rvert^3)$ | `derive_boost_covariance.py:L205–212 defect_closed_even()`, check `L331–362` | exact (reg) |
| 5 | $D_i=-s\,c_\text{lat}(k_yk_z,k_zk_x,k_xk_y)+O(k^3)$ | chiral-branch defect, $O(\lvert k\rvert^2)$, chirality-odd | `derive_boost_covariance.py:L217–218 defect_closed_branch()`, check `L414–435` | exact (reg) |
| 6 | $\omega^+(k)=c\lvert k\rvert+b_2\lvert k\rvert^2+\dots$, $b_2=-\tfrac13\hat k_x\hat k_y\hat k_z$ ($c_2=b_2/2$ for $\Omega_\text{single}$) | chiral $k^2$ dispersion term | `derive_boost_covariance.py:L223–224 b2_closed()`, check `L370–411` | exact (reg) |
| 7 | $\sin^2\omega(k,m)-(1-m^2)\sin^2\omega_0(k)=m^2$ | exact massive shell at finite $a$; $(E,P)=(\sin\omega,\tfrac{n}{c}\sin\omega_0\hat k)$ | `derive_boost_covariance.py:L298–303, L256–261 deformed_EP()` | exact (reg) |
| 8 | along ⟨100⟩: $\Omega=c_\text{lat}\lvert k\rvert$, $D\equiv0$ for all three laws | all-order axis covariance | `derive_boost_covariance.py:L313–322` | exact (reg) |
| 9 | 1-D: $D/k=1/\rho-1$, $\rho=m/(\sqrt{1-m^2}\arcsin m)$; same $\rho$ on the BCC massive branch | F22 bridge | `derive_boost_covariance.py:L438–471` | machine (reg: exact; row is weaker — see flags) |
| 10 | $\Omega'-\Omega(k')=v\,(D\cdot\hat v)+O(v^2)$ under the linear boost `lorentz()` | operational meaning | `derive_boost_covariance.py:L264–270, L474–489` | machine (reg: exact; row is weaker — see flags) |
| 11 | $\Omega_\text{even}-\omega^+=+\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2+O(k^3)$ | no universal momentum map (DSR no-go) | `derive_boost_covariance.py:L521–540` | exact (reg) |
| 12 | $K_i=\tfrac1{2c^2}\{x_i,\Omega\}$: $[K_i,H]=iP_i+iD_i$, $[K_i,P_j]=i\delta_{ij}\Omega/c^2$, $[K_i,K_j]$ = rotation $+\tfrac{i}{c^2}(D_ix_j-D_jx_i)$, invariant under $K\to K+f(k)$ | algebra, sympy | `derive_boost_covariance.py:L569–623 _check_algebra()` | exact (reg) |

**Depends on:** `c_lat` (01); `derive_velocity_addition.rho` (this file). **Flags:** none beyond the known open items it lists (W/Z/gluon, $\lvert k\rvert^5$).

### `engine/interactions/derive_chiral_liv_bound.py` — chiral $O(\lvert k\rvert^2)$ defect in physical units vs electron LV bounds (F327)
**Status:** live · standalone · **Findings:** F327 F301 F246 F91 F232 · **Lattice:** BCC (mpmath, 32 dps; $c_\text{lat}=1/\sqrt3$ cross-checked vs registry) · **Law:** chiral (the massive Dirac fermion rides one branch); even law as control (`branch="paired"`) · **Units:** lattice → GeV via $E_a=\hbar c/a$, $a=(a/\ell_P)\ell_P$

**Does:** shows a massive BCC Dirac fermion is locked to one chiral branch, converts the F301 $b_2$ term into a dimension-5 operator, and finds it excluded by LHAASO/Crab electron bounds by ~7 decades (CL262 falsifier fired on the physical assignment).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $U_s=u_s\mathbb 1-i\,\mathbf n_s\cdot\boldsymbol\sigma$ (same $u,\mathbf n$ as `horizon_entanglement._uvec`, args $k_i/\sqrt3$) | BCC Weyl unitary | `derive_chiral_liv_bound.py:L117–138 u_branch(), _nvec(), _A()` | quantitative (reg) (row read: exact) |
| 2 | $D_k=\begin{pmatrix}nA_+&im\\ im&nA_+^\dagger\end{pmatrix}$ (model); `naive` lower $=A_-$; `local` $M=-mA_+A_-^\dagger$, $M'=m\mathbb1$ | 4×4 Dirac one-tick unitary and two escape ansätze | `derive_chiral_liv_bound.py:L214–234 _dirac_D()` | quantitative (reg) (row read: exact) |
| 3 | eigenphases $\pm\arccos(n u_+)$, each two-fold | A1: one branch, spin-independent | `derive_chiral_liv_bound.py:L327–336 summary()` | quantitative (reg) (row read: machine (<1e-20 at 32 dps)) |
| 4 | $\lVert D^\dagger D-\mathbb1\rVert$: naive $\neq0$ for $m\neq0$; local $=0$, rest phase $\arcsin m$; local mass shift linear in $m$; local splits $b_2\to\mp\lvert b_2\rvert$ | A2, A2b–d | `derive_chiral_liv_bound.py:L339–384` | quantitative (reg) (row read: machine) |
| 5 | $\operatorname{tr}(VA^\dagger V^\dagger)=\overline{\operatorname{tr}A}=\operatorname{tr}A=2u_s$ | A3 k-independent no-go | `derive_chiral_liv_bound.py:L391–397` | quantitative (reg) (row read: exact) |
| 6 | $b_2=\lim(\omega-c\lvert k\rvert)/\lvert k\rvert^2$ (Richardson), closed $-\tfrac13\hat k_x\hat k_y\hat k_z$ | B1 | `derive_chiral_liv_bound.py:L248–256 _leading_k2()`, `L416–439` | quantitative (reg) (row read: machine) |
| 7 | $3[\omega(K\hat u_{111})^2-\omega(K\hat u_{100})^2]=-\tfrac{2}{\sqrt3}K^3\hat u_x\hat u_y\hat u_z$ ⇔ $E^2=m^2c^4+c^2p^2-\tfrac{2}{\sqrt3}\,\dfrac{(cp_x)(cp_y)(cp_z)}{E_a}$ | B1b dimension-5 operator (mass dependence $-m^2/3$ relative) | `derive_chiral_liv_bound.py:L448–481` | quantitative (reg) (row read: machine) |
| 8 | $\eta(\hat k)=-\tfrac{2}{\sqrt3}(a/\ell_P)\hat k_x\hat k_y\hat k_z$; $\lvert\eta\rvert_\text{max}=\tfrac29(a/\ell_P)=\tfrac29\sqrt{8\pi}\,3^{1/4}$; measured $\eta=2\sqrt3(a/\ell_P)b_2$ | Myers–Pospelov coefficient | `derive_chiral_liv_bound.py:L186, L192, L488–492` | quantitative (reg) (row read: exact) |
| 9 | $E_\text{LV}=M_P/\lvert\eta\rvert_\text{max}=\tfrac92E_a$; $E_a=\hbar c/a$, $M_P=\hbar c/\ell_P$ (GeV) | B3 | `derive_chiral_liv_bound.py:L170–180, L495–497` | quantitative (reg) (row read: exact) |
| 10 | $\Delta v/c=[v_g^\text{fermion}-v_g^\text{even}]/c=-\tfrac2{\sqrt3}\hat k_x\hat k_y\hat k_zK$ | B4 parametrisation-free gap | `derive_chiral_liv_bound.py:L259–262, L503–513` | quantitative (reg) (row read: machine) |
| 11 | $\hat k_x\hat k_y\hat k_z=i\sqrt{2\pi/105}\,(Y_{3,-2}-Y_{3,2})$ | B5 pure $(j,m)=(3,\pm2)$ | `derive_chiral_liv_bound.py:L296–305 _ylm_identity_residual()` | quantitative (reg) (row read: exact) |
| 12 | decades short $=\log_{10}(E^\text{bound}/E_\text{LV})$; $E_\text{th}=(m_e^2M_P/\eta)^{1/3}$; sky fraction $\int\tfrac{\sin\theta}{2}f(\theta)d\theta$, $f=\tfrac2\pi\arcsin\!\big(2\varepsilon/\lvert\sin^2\theta\cos\theta\rvert\big)$ | C1–C4 confrontation | `derive_chiral_liv_bound.py:L521–555, L265–280` | quantitative (reg) |
| 13 | photon $c_3$ measured on ⟨111⟩ vs F246 $\tfrac{\sqrt3}{216}\cdot\tfrac49$; channel ratio; $G$ factor $=(\text{shrink})^2$ | C5, C6 | `derive_chiral_liv_bound.py:L558–580` | quantitative (reg) |

**Inputs → outputs:** `branch` ∈ {single, paired}, `ruler` ∈ {f232, tuned} → 19 checks. **Depends on:** `a_over_ellP`, `c_lat`, `ell_P_m`, `c_SI`, `hbar_SI`, `J_per_GeV`, `m_e_GeV`, `E_crab_photon_max_GeV`, `E_LV_e_sup_min_GeV`, `E_LV_e_sub_min_GeV` (01). See 06a/b § `dirac_bcc` for the Dirac step it quotes.

**Flags:** OTHER — C5 hard-codes `E_crab = 1.12e6` GeV (L558) although the same quantity is imported as the registered `E_crab_photon_max_GeV` (used in C3); F246's $c_3=\tfrac{\sqrt3}{216}\cdot\tfrac49$ is re-typed as a closed form (L569). Registry `quantitative` fits the confrontation legs; the algebraic legs are exact.

### `engine/interactions/derive_curl_subleading.py` — subleading coefficients of the composite-photon curl residual (F7 → F245)
**Status:** live · standalone · **Findings:** F7 F245 · **Lattice:** 2-D square (half-momentum args $k/(2\sqrt2)$) and 3-D BCC (args $k/(2\sqrt3)$) · **Law:** single branch half-momentum walk feeding the **σ-bilinear composite photon** (the superseded photon construction) · **Units:** lattice (mpmath, 50 dps)

**Does:** replicates the eigenmode → σ-bilinear → transverse $(E,B)$ → one-tick curl-residual pipeline of the old `ca_maxwell(_2d).py`, and fits closed forms to its subleading term.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $G^i=\phi^\dagger\sigma^i\psi$ (as $\sum_{ij}\phi_i\sigma_{ij}\psi_j$); $G_T=G-(G\cdot\hat n)\hat n$; $E=\lvert n\rvert(G_T+G_T^*)$, $B=i\lvert n\rvert(G_T^*-G_T)$ | σ-bilinear field construction | `derive_curl_subleading.py:L46–50 _bil()`, `L81–87 _residual.EB` | machine (reg) (row read: exact) |
| 2 | $r=\max(\lVert E_t-E_0-i\,2\mathbf n\times B_0\rVert,\lVert B_t-B_0+i\,2\mathbf n\times E_0\rVert)/(\lVert E_0\rVert+\lVert B_0\rVert)$ | normalised one-tick curl residual | `derive_curl_subleading.py:L89–98 _residual()` | machine (reg) (row read: exact (definition)) |
| 3 | 2-D: $u=c_xc_y$, $\mathbf n=(s_xc_y,c_xs_y,s_xs_y)$; 3-D: BCC $u,\mathbf n$ at $k/2$ | half-momentum walk symbols | `derive_curl_subleading.py:L101–119` | machine (reg) (row read: exact) |
| 4 | $\alpha(p)=(\cos4p-9)/768$ (on-axis $-1/96$) | 2-D subleading ($r/k=\tfrac12+\alpha k^2$) | `derive_curl_subleading.py:L124 alpha_2d()` | machine (reg) |
| 5 | $\beta(\hat k)=-\tfrac{\sqrt2}{12}\hat k_x\hat k_y\hat k_z$ (max $\sqrt6/108$ on ⟨111⟩) | 3-D subleading ($r/k=1/\sqrt6+\beta k$) | `derive_curl_subleading.py:L130 beta_3d()` | machine (reg) |
| 6 | $r/k=\sqrt2\sin(k/2\sqrt2)/k=\tfrac12-k^2/96+\dots$ | algebraic on-axis series | `derive_curl_subleading.py:L135 analytic_alpha_axis()` | machine (reg) (row read: exact) |
| 7 | Richardson $\tfrac13[4f(k/2)-f(k)]$ (2-D), $2f(k/2)-f(k)$ (3-D) | coefficient extraction | `derive_curl_subleading.py:L138–150` | machine (reg) |

**Depends on:** mpmath only (reimplements `bcc` symbols inline). See 05a § `gauge/bilinear.py` for the construction.

**Flags:** SUPERSEDED (object) — the quantity whose subleading terms this module closes is the σ-bilinear curl residual that **S18 / F306** declares a representation artifact (real $E,B$ vs pure-imaginary RHS; $c_\text{lat}/\sqrt2$ withdrawn, inventory #49); F245 is not itself listed in S18 but its object is. The docstring (L8–10) still presents $1/\sqrt{2d}=c_\text{lat}/\sqrt2$ as the Tier-1 leading constant. Hazard: σ-bilinear construction applied to the **photon** (F65–F69 banner: bilinear is W/Z/gluon only) — legitimate only as a record of the superseded composite photon. ⚠ DOC/CODE MISMATCH — `check_closed_forms` docstring says leg A2 compares "the measured on-axis value" against $-1/96$, but code (L209) evaluates the **closed form** `alpha_2d(pi/2)`, so A2 is tautological (only the override control can fail it). Code comment L236–242 records a second mismatch: F245 reports B1 worst 9e-15, code measures 4.0e-12.

### `engine/interactions/derive_dielectric_noconfine.py` — colour-dielectric tube cannot carry $\sigma=2\pi v^2n$ (F142)
**Status:** partial · standalone · **Findings:** F86 F139 F142 · **Lattice:** 2-D square transverse box (5-point Laplacian, Dirichlet $f=1$ edge) · **Law:** n/a · **Units:** lattice / dimensionless dual-SC units

**Does:** a colour-confinement no-go (not gravity): the Friedberg–Lee electric tube with $\varepsilon_c=1-f^2$ does not confine in the continuum; the exact $2\pi v^2n$ belongs to the magnetic ANO vortex's winding.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $B=e^2v^4/4$, $\Phi=2\pi n/e$, $\sigma_\text{ANO}=2\pi v^2n$, $\sigma_\text{bag}=\Phi\sqrt{2B}=\tfrac1{\sqrt2}\,2\pi v^2n$ | BPS dictionary, thin-wall prefactor $1/\sqrt2$ | `derive_dielectric_noconfine.py:L56–60 bag_dictionary()` | exact (inventory F142 #89) |
| 2 | $\sigma=\dfrac{\Phi^2}{4A\delta}+4B\delta^pA$, $\delta^{p+1}=\dfrac{\Phi^2}{16pBA^2}$ ⇒ $\sigma\propto A^{-(p-1)/(p+1)}$ ($A^{-1/3}$ at $p=2$) | spread-thin no-go (control $p=1$ closes it) | `derive_dielectric_noconfine.py:L76–79 spread_tension()` | quantitative (reg) (row read: exact) |
| 3 | $\sigma[f]=\sum[(\nabla f)^2+B(1-f^2)^p]+\Phi^2/(2\sum(1-f^2))$; flow $f\leftarrow f+\Delta\tau[2\nabla^2f+2pBf(1-f^2)^{p-1}-(\Phi/I)^2f]$ | direct box minimisation, $\sigma\propto L^{-2/3}$ | `derive_dielectric_noconfine.py:L108–118 tube_tension_box()` | quantitative (reg) |
| 4 | $\sigma_R/\sigma_F=C_2(R)/C_2(F)$: $1,1,\tfrac94,\tfrac52,\tfrac92$ for $3,\bar3,8,6,10$ | Casimir ratios (Fractions) | `derive_dielectric_noconfine.py:L134–137 su3_casimir_ratios()` | quantitative (reg) (row read: exact) |
| 5 | Casimir $\sigma_k\propto k(N-k)$ vs sine $\sin(k\pi/N)$; equal for $N=3$, split at $N=4$ | k-string degeneracy | `derive_dielectric_noconfine.py:L149–151 su_n_k_string_ratios()` | quantitative (reg) (row read: exact (Casimir) / machine (sine)) |

**Depends on:** numpy, fractions. Related: `gravity_backreaction.py` (this section) and 05a/05b § confinement.

**Flags:** OTHER — colour-sector module filed with gravity/relativity by name only. Minor: `spread_tension` bag term $4B\delta^p$ with $\delta=(1-f^2)/2$ equals `tube_tension_box`'s $B(1-f^2)^p$ only at $p=2$ (the $p=1$ control therefore uses a different normalisation in the two legs; exponents unaffected).

### `engine/interactions/derive_f26_dispersion.py` — subleading coefficients of the F26 even law (F246, L2)
**Status:** live · standalone · **Findings:** F26 F30 F246 · **Lattice:** BCC (args $k_i/(2\sqrt3)$ = half momentum) · **Law:** even (single-branch $2\omega_+(k/2)$ as comparison) · **Units:** lattice (mpmath, 60 dps)

**Does:** expands the photon/gauge rotation angle in $\lvert k\rvert$: only odd powers survive and the cubic coefficient is closed.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Omega_\text{even}(k)=\arccos u_+(k/2)+\arccos u_-(k/2)$ | F26 even law | `derive_f26_dispersion.py:L54–63 _u(), omega_even()` | machine (reg) (row read: exact) |
| 2 | $\Omega_\text{single}=2\arccos u_+(k/2)$ | chiral comparison | `derive_f26_dispersion.py:L68 omega_single()` | machine (reg) (row read: exact) |
| 3 | $u_+(-q)=u_-(q)$ ⇒ $\Omega_\text{even}(-k)=\Omega_\text{even}(k)$ ⇒ $\Omega_\text{even}=c_\text{lat}\lvert k\rvert+c_3\lvert k\rvert^3+c_5\lvert k\rvert^5+\dots$ (even powers $\equiv0$) | structural parity; checked by $c_2,c_4\to0$ (fit floor) vs single law $\lvert c_2\rvert>10^{-3}$ | `derive_f26_dispersion.py:L98–108 _all_powers()`, `L154–167` | machine (reg) (row read: exact (argument) / machine (fit)) |
| 4 | $c_3(\hat k)=-\tfrac{\sqrt3}{216}(p+3q)$, $p=\sum_{i<j}\hat k_i^2\hat k_j^2$, $q=\prod\hat k_i^2$ | cubic coefficient; $0$ on ⟨100⟩, $-\sqrt3/486$ on ⟨111⟩ | `derive_f26_dispersion.py:L76–82 c3_closed()`, measured via `L85–95 _odd_series()` | machine (<1e-17; inventory Tier-3 #5 → F246) |
| 5 | $\Omega_\text{even}/\lvert k\rvert\to c_\text{lat}=1/\sqrt3$ on ⟨100⟩ | leading term | `derive_f26_dispersion.py:L192–194` | machine (reg) (row read: exact (<1e-30)) |

**Depends on:** mpmath only. Cross-reference: `derive_boost_covariance` #4 (same $p+3q$ structure, $D\cdot\hat k=-\tfrac1{18}(p+3q)\lvert k\rvert^3$) and `derive_chiral_liv_bound` C5 (re-types this $c_3$).

**Flags:** ⚠ DOC/CODE MISMATCH — `check_closed_forms` docstring says C3 "replaces the measured C3 body-diagonal value", but code (L197) compares the **closed form** `c3_closed((1,1,1))` with $-\sqrt3/486$, so C3 is an arithmetic identity, not a measurement (C1 is the real measured leg). S2 (L170–172) asserts two hard-coded constants (no computation). Registry says `machine`, consistent with the fits.

### `engine/interactions/derive_gap5_adjudication.py` — three gap-#5 items adjudicated (F311)
**Status:** live · standalone · **Findings:** F311 · **Lattice:** n/a (A1 re-runs QED kernels on a 4-D momentum grid) · **Law:** n/a · **Units:** MeV / SI

**Does:** (A) shows the leptonic $\Delta\alpha(M_Z)$ is untouched by S12-F277 and its residual is the two-loop term; (B) books ten `candidate` baselines as instrument artifacts; (C) argues the Λ "two pictures" are sequential under the induced (F178) law. Only A contains physics equations; B and C are bookkeeping.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | reinstate $k_x\to\operatorname{wrap}(k_x+Q)$ in `_fermion_B`; $B(Q)=\big[\langle N_{00}/D\rangle-\langle N_{11}/D\rangle\big]/Q^2$, $N_{\mu\nu}=4(k_\mu k'_\nu+k_\nu k'_\mu-\delta_{\mu\nu}k\cdot k')$, $D=K(k)K(k')$ | A1 probe: $\Pi_4$ bit-identical, $\Pi_3$ spread moves >100× | `derive_gap5_adjudication.py:L184–209 refold_independence()` (monkey-patch, restored in `finally`) | exact (reg) |
| 2 | $\Delta\alpha^{(1)}_\ell=\tfrac{\alpha}{3\pi}[\ln(s/m_\ell^2)-\tfrac53]$ (from `qed_vacuum_polarization._dalpha_lepton`) | one-loop leptonic running | `derive_gap5_adjudication.py:L237–238 two_loop_leptonic()` | quantitative (reg: exact; row is weaker — see flags) |
| 3 | $\Delta\alpha^{(2)}_\ell=(\alpha/\pi)^2[L/4+\zeta(3)-\tfrac5{24}]$, $L=\ln(s/m_\ell^2)$, summed over $e,\mu,\tau$ | Källén–Sabry leading two-loop (cited, not derived); control drops the constant | `derive_gap5_adjudication.py:L240–245` | quantitative (reg: exact; row is weaker — see flags) |
| 4 | residual $=\Delta\alpha^\text{PDG}-\Delta\alpha^{(1)}$; ratio $\Delta\alpha^{(2)}/\text{residual}\in(0.95,1.05)$; improvement factor $>100$ | A2/A3 | `derive_gap5_adjudication.py:L247–265` | quantitative (reg: exact; row is weaker — see flags) |
| 5 | $\rho_\text{cut}=\rho_P(3^{-1/4})^4=\rho_P/3$ vs F192's $3.456\times10^{111}$ J/m³: $<2$ dex | C3 double-count argument | `derive_gap5_adjudication.py:L334–357 lambda_adjudication()` | quantitative (reg: exact; row is weaker — see flags) |

**Plumbing:** `volatile_key_filter` tests `casim.baselines._VOLATILE_RE` on a key list; `baseline_triage` counts a hard-coded dict; C1/C2 are hard-coded dates and booleans.

**Depends on:** `interactions.qed_vacuum_polarization` (07a/07c § qed), `casim.baselines`. **Flags:** OTHER — registry tags the module `exact`, but only A1's bit-identity is exact; A2/A3/C3 are numerical comparisons, and B/C1/C2 legs assert hard-coded values (cannot fail except by editing the table). `ZETA3`, `rho_planck`, `rho_f192`, the literature two-loop value are literals. Docstring (L162–163) says the module "fixes" the `_seconds` regex hole; the code only tests the regex in `casim.baselines`.

### `engine/interactions/derive_velocity_addition.py` — QCA velocity addition and the off-shell boost defect (F15 → F22)
**Status:** partial · standalone · **Findings:** F15 (registry); docstring/inventory also F22 · **Lattice:** 2-D square QCA axis slice, $c_\text{lat}=1/\sqrt2$ (D1 reference) · **Law:** massive single branch $\omega=\arccos(n\cos(k/\sqrt2))$ · **Units:** lattice

**Does:** defines $\rho(m)=\lim_{k\to0}u_p/u_g$ and a "deformed" velocity-addition law; after the 2026-08-04 F22 review its gate entry checks $\rho=1-2\beta_\text{LV}$ against the F15 module and measures the leading off-shell failure of a linear SR boost.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\omega=\arccos(n\cos(k/\sqrt2))$, $u_g=n\sin(k/\sqrt2)/(\sqrt2\sin\omega)$, $u_p=k\,c^2/\omega=k/(2\omega)$ | dispersion, group and "4-momentum" velocities | `derive_velocity_addition.py:L67–89` | exact (reg) |
| 2 | $\rho(m)=\dfrac{m}{\sqrt{1-m^2}\arcsin m}$, $\beta_\text{LV}=(1-\rho)/2$ | ratio and F15 coefficient ($\rho>1$) | `derive_velocity_addition.py:L95, L100 rho(), beta_LV()` | exact (inventory #45) |
| 3 | $k'=\gamma(k-2v\omega)$, $\gamma=(1-2v^2)^{-1/2}$ | linear SR boost of $(\omega,k)$ | `derive_velocity_addition.py:L121–122 boost_k()` | exact (reg) |
| 4 | $u'_\text{QCA}=\dfrac{u+v}{1+2\rho^2uv}$; $u'_\text{SR}=\dfrac{u+v}{1+2uv}$ (and subtraction forms) | deformed addition law | `derive_velocity_addition.py:L279–308` | exact as algebra (inventory #46) — see Flags |
| 5 | $\delta u'=\dfrac{2(1-\rho^2)uv(u+v)}{(1+2\rho^2uv)(1+2uv)}\approx8\beta_\text{LV}uv(u+v)$ | LV deviation (vanishes at $\rho=1$, $m\to0$) | `derive_velocity_addition.py:L319–324 analytic_delta_add()` | exact (reg) |
| 6 | $\lim_{k\to0}u_p/u_g$ (sympy) $=1-2\beta_\text{LV}^\text{F15}(m)$, via lemma $\arccos\sqrt{1-m^2}=\arcsin m$ (50-dps numeric) | ρ identity with independent sides; control $\rho=42$ must fail | `derive_velocity_addition.py:L517–576 check_rho_identity()` | exact (reg) |
| 7 | $\Delta=\gamma(\omega-vk)-\omega(\gamma(k-v\omega/c^2))$; $\Delta/(vk)\to1/\rho-1=2\beta_\text{LV}/(1-2\beta_\text{LV})$ | off-shell boost coefficient (fails at leading order) | `derive_velocity_addition.py:L592–605 offshell_boost_coefficient()` | quantitative (rel tol 5e-3) (reg: exact; row is weaker — see flags) |

**Plumbing:** `symbolic_verification`, `numerical_scan`, `continuum_check`, `finite_k_lv`, `summary_table` print only. **Depends on:** `derive_beta_LV.beta_LV` (this file). Consumed by `derive_boost_covariance` B6 (`rho`).

**Flags:** ⚠ DOC/CODE MISMATCH — the module docstring (L26–30) derives #4 from "the SR boost acts on the 4-momentum $(\omega,k)$ exactly", but the module's own gate (#7, F22 review) measures that a linear SR boost leaves the dispersion **off shell at leading order** ($\Delta/vk\to1/\rho-1\neq0$); #4/#5 are therefore unverified algebra on a refuted premise, and `numerical_scan` compares the formula to itself (comment L373). Registry lists only F15 although the code is F22's; inventory rows #45–48 are attributed to F22. `C_LAT=1/√2` literal.

### `engine/interactions/graviton_collapse_threshold.py` — two band-top quanta vs the one-cell remnant (F359)
**Status:** live · standalone · **Findings:** F359 F357 F228 F223 F79 F107 · **Lattice:** n/a (uses $A=a/\ell_P$ only) · **Law:** even (control: `chiral_double`, band top doubled) · **Units:** Planck

**Does:** exact kinematic threshold comparison: head-on pair of band-top quanta vs the minimal (one-cell) Schwarzschild remnant. No amplitude is computed.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A=\sqrt{8\pi}\,3^{1/4}$, $A^2=8\pi\sqrt3$ (sympy; registry value to 1e-9) | canonical cell identity (F79/F107) | `graviton_collapse_threshold.py:L109, L119–120 check_A_canonical_cell_identity()` | exact (reg) |
| 2 | $N=16\pi(M/M_P)^2/A^2=1\Rightarrow M_\text{rem}/M_P=A/(4\sqrt\pi)=3^{1/4}/\sqrt2$ | one-cell remnant (F228) | `graviton_collapse_threshold.py:L140–142 check_B_remnant_mass_closed_form()` | exact (reg) |
| 3 | $E_\text{max}/E_P=\pi\sqrt3/A$ (typed, not recomputed from the dispersion; control $2\pi\sqrt3/A$) | F357 band top | `graviton_collapse_threshold.py:L164–167` (repeated L193, L223) | exact (reg) |
| 4 | $\sqrt{s_\text{max}}/(M_\text{rem}c^2)=2E_\text{max}/M_\text{rem}=8\pi^{3/2}\sqrt3/A^2=\sqrt\pi$ | headline: pair is super-threshold | `graviton_collapse_threshold.py:L168–170 check_C_two_quantum_threshold()` | exact (reg) |
| 5 | $E_\text{max}/(M_\text{rem}c^2)=\sqrt\pi/2$ | single quantum sub-threshold | `graviton_collapse_threshold.py:L197–198 check_D_single_quantum_subthreshold()` | exact (reg) |
| 6 | ratios to $\mu_\text{geon}=\sqrt2M_P$: $\sqrt\pi\,3^{1/4}/2$ (pair), $\sqrt\pi\,3^{1/4}/4$ (single) | F223 order-of-magnitude cross-check | `graviton_collapse_threshold.py:L227–234 check_E_geon_virial_cross_check()` | quantitative (order-of-magnitude tier) (reg: exact; row is weaker — see flags) |

**Depends on:** `a_over_ellP` (01), `casim.numerics.xp`; $E_\text{max}$ from `gravity_band_cutoff.py` (this section). Uses the **Schwarzschild** horizon area, consistent with F178 (the horizon-free F114 dielectric hole is superseded, S4).

**Flags:** OTHER — the band top $\Omega_\text{max}=\pi$ enters as the typed closed form $\pi\sqrt3/A$, not re-derived from `gravity_band_cutoff`; the `chiral_double` control is likewise the typed factor 2, so C/D's control reds are by construction. F228's published 0.93060 is a literal.

### `engine/interactions/gravity.py` — the gravity field element (dielectric + F106 source + D-EM8 wave)
**Status:** partial · driven (29 ch) · **Findings:** (registry: none; docstring F64 F79 F106 F62 F178 F271) · **Lattice:** simple-cubic reference stencil ($2d$-neighbour Laplacian, periodic FFT) — not BCC · **Law:** n/a (scalar field); matter coupling is the rest-leg lapse mix · **Units:** lattice ($a=\tau=\hbar=1$)

**Does:** holds the canonical dielectric maps, the energy-density sources, the static and dynamical equations for the potential $\Phi$ that sets $K$, and the unitary matter-side (lapse) and gauge-side (eikonal) couplings that `GravityDielectricChannel` wraps. Per the docstring (L4–11) this is the **vacuum/weak-field representation** of the induced Einstein equation (F178), not the interior field equation.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $G_\text{lat}=c_\text{lat}^4/(8\pi)=1/(72\pi)$ | Newton's constant in lattice units (F79 $G=a^2c^3/(8\pi\sqrt3\hbar)$ at $c=c_\text{lat}=1/\sqrt3$) | `gravity.py:L75` (import of `G_LATTICE`, `constants/gravity.py:L18`) | exact (inventory #182b) |
| 2 | $8\pi G/c^4=a^2c_\text{lat}/(\hbar c)\to1$ | F106 sourcing coefficient in lattice units | `gravity.py:L71` (`F106_COEFF_LATTICE`, `constants/gravity.py:L46`) | exact (inventory #181) |
| 3 | $K=e^{2u}$ | canonical dielectric index | `gravity.py:L86 K_canonical()` | unknown (inferred: exact) |
| 4 | $u=-\Phi/c_0^2,\;K=e^{2u},\;A=1/K,\;B=K$ ($AB\equiv1$) | potential → dielectric legs | `gravity.py:L94–96 dielectric_from_phi()` | unknown (inferred: exact) |
| 5 | $T^{00}_\text{rest}=\sqrt{A}\,m\sum_{\text{comp}}\lvert\psi\rvert^2$ (leading axes summed) | rest-leg energy density (F106-E5) | `gravity.py:L124–129 T00_dirac_rest()` | unknown |
| 6 | $T^{00}_\text{kin}=\sqrt{A}\,\tfrac{c_0^2}{2}\sum_\text{comp}\sum_i\lvert\tfrac12(\psi_{i+1}-\psi_{i-1})\rvert^2$ | kinetic-leg energy density (D-EM3) | `gravity.py:L161–170 T00_dirac_kinetic()` | unknown |
| 7 | $T^{0i}=c_0\sum_\text{comp}\operatorname{Im}\!\big(\psi^*\,\tfrac12(\psi_{i+1}-\psi_{i-1})\big)$ | momentum density | `gravity.py:L196–204 T0i_dirac()` | unknown |
| 8 | $\binom{E}{B}\leftarrow R(\delta)\binom{E}{B},\;\delta=\tfrac{\Delta t}{2}\,\omega_0(1/K-1)$ | eikonal half-step dielectric mix for the $(E,B)$ pair — **SUPERSEDED by F271** (`gauge.photon.photon_step_dielectric`); kept as control | `gravity.py:L263–270 dielectric_mix_half()` | unknown (inferred: exact (pointwise orthogonal)) |
| 9 | $T^{00}_\text{EM}=\tfrac12(E^2+B^2)$ (leading axes summed) | radiation source | `gravity.py:L278–281 T00_field_energy()` | unknown (inferred: exact) |
| 10 | $\nabla^2\Phi=\tfrac{\kappa c_0^2}{2}T^{00}$, $\kappa=8\pi G/c^4$ (default 1) | F106 law $\nabla^2\ln K=-\kappa T^{00}$ rewritten for $\Phi$ via $\ln K=-2\Phi/c_0^2$; with $\kappa=8\pi G/c^4$ this is $\nabla^2\Phi=+4\pi G\,T^{00}/c^2$ (attractive) | `gravity.py:L293 phi_source()` | unknown (inferred: exact) |
| 11 | $(\nabla^2_{\rm lat}P)_x=\sum_{i}(P_{x+e_i}+P_{x-e_i})-2d\,P_x$ | $2d$-neighbour periodic Laplacian (cubic/square) | `gravity.py:L301–304 lap_nd()` | unknown (inferred: exact) |
| 12 | $\hat\Phi(k)=-\hat s(k)/\lambda(k)$, $\lambda=\sum_i4\sin^2(k_i/2)$ (stencil) or $\lvert k\rvert^2$ (continuum); zero mean | static Poisson solve; stencil mode is the exact fixed point of #13 | `gravity.py:L322–329 solve_phi_poisson()` | machine (inventory #182a: `lap_nd(ln K)==−T⁰⁰`, resid $<10^{-10}$; spot-checked here $1\times10^{-15}$) |
| 13 | $\Phi^{n+1}=2\Phi^n-\Phi^{n-1}+(c_g\Delta t)^2(\nabla^2_{\rm lat}\Phi^n-s)$ | D-EM8 leapfrog of $c_g^{-2}\partial_t^2\Phi-\nabla^2\Phi=-s$ | `gravity.py:L339–341 phi_wave_step()` | unknown |
| 14 | $E=\tfrac12\sum(\dot\Phi)^2+\tfrac12c_g^2\sum_i\big(\tfrac12(\Phi_{i+1}-\Phi_{i-1})\big)^2$ | free-field energy diagnostic | `gravity.py:L346–351 phi_field_energy()` | unknown |
| 15 | $\theta=-\tfrac{\Delta t}{2}(\sqrt{A}-1)m$; $\eta\leftarrow\cos\theta\,\eta-i\sin\theta\,\chi$, $\chi\leftarrow\cos\theta\,\chi-i\sin\theta\,\eta$ | F62 sign-corrected Strang half-step lapse mix → effective mass $\sqrt{A}\,m$ | `gravity.py:L371–378 lapse_mix_half()` | exact (unitary; flat ⇒ bit-identical, inventory #182c) |

**Inputs → outputs:** matter fields (Dirac components, $(E,B)$) → $T^{00}$, $T^{0i}$ → source $s$ → $\Phi$ (static FFT or leapfrog) → $(A,B,K)$ → lapse mix on the rest leg / eikonal mix on $(E,B)$. **Depends on:** `casim.constants` (01-constants.md § gravity, geometry), `casim.numerics.fft` (02-numerics.md). Wrapped by `core.channels.GravityDielectricChannel` (04-core.md). F271 replacement lives in `gauge/photon.py` (05c).

**Ledger check (F178).** Signs and factors agree: $\nabla^2\ln K=-\kappa T^{00}$ (negative sign), $\nabla^2\Phi=+4\pi G T^{00}/c^2$, $G_\text{lat}=1/(72\pi)$, and $\kappa\equiv1$ at lattice units — confirmed numerically (random $T^{00}$ on $8^3$: $\max\lvert\nabla^2_\text{lat}\ln K+(T^{00}-\bar T^{00})\rvert=1.1\times10^{-15}$). Only $T^{00}$ (and $T^{0i}$, which nothing here consumes) is sourced — this module implements only the **static weak-field reduction** (F106) plus a scalar wave extension; it does not implement $G_{\mu\nu}=8\pi GT_{\mu\nu}$, consistent with its F178 banner. The superseded rest-mass source (F50/F52/F62) is absent; only F62's lapse **sign** survives (#15), as S3 records.

**Flags:** (i) registry `findings` is empty and `exactness` None although the module carries F64/F79/F106/F178 provenance and inventory rows #181–182. (ii) `dielectric_mix_half` is SUPERSEDED by F271 (docstring banner). (iii) `T00_dirac_kinetic` (#6) uses the centred-difference gradient, not the stencil of `lap_nd`, despite its docstring saying "the same centred difference the lattice Laplacian uses" — `lap_nd` is a nearest-neighbour second difference, whose discrete adjoint gradient is the one-sided difference; ⚠ DOC/CODE MISMATCH (minor). (iv) Laplacian is simple-cubic (D1 reference), not BCC. (v) The D-EM8 wave speed $c_g$ is a free argument; nothing here fixes $c_g=c_\text{lat}$.

### `engine/interactions/gravity_backreaction.py` — self-consistent dual-Ginzburg–Landau colour back-reaction (**not gravity**)
**Status:** live · driven (15 ch) · **Findings:** (registry: none; docstring F86 F137) · **Lattice:** simple-cubic/square reference stencils ($2d+1$-point Laplacian, face-mean divergence); docstring says "3D (BCC box)" · **Law:** n/a · **Units:** lattice

**Does:** relaxes a colour-magnetic condensate $f\in[0,1]$ and the confined colour-electric flux to a mutual fixed point (Friedberg–Lee colour-dielectric form of dual GL), curing F137's mean-field tube pinch. Legacy name `ca_dual_gl_backreaction.py`; the "gravity" in the file name is a migration mis-label.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\partial_i\psi\approx\tfrac12(\psi_{i+1}-\psi_{i-1})$ | central gradient | `gravity_backreaction.py:L80–82 grad()` | unknown (inferred: exact) |
| 2 | $\nabla^2f=\sum_i(f_{i+1}+f_{i-1})-2d\,f$ | periodic Laplacian | `gravity_backreaction.py:L87–88 laplacian()` | unknown (inferred: exact) |
| 3 | $\varepsilon_c=\operatorname{clip}(1-f^2,\varepsilon_\text{floor},1)$ | colour dielectric (F86) | `gravity_backreaction.py:L94 colour_dielectric()` | unknown (inferred: exact) |
| 4 | $\mathcal A[\psi]=-\nabla\!\cdot(\varepsilon\nabla\psi)$ with face-mean $\varepsilon_{i\pm1/2}=\tfrac12(\varepsilon_i+\varepsilon_{i\pm1})$ | dielectric Gauss operator | `gravity_backreaction.py:L103–108 dielectric_op()` | unknown (inferred: exact) |
| 5 | solve $-\nabla\!\cdot(\varepsilon\nabla\psi^a)=\rho^a$ (zero-mean, matrix-free CG, tol $10^{-7}$) | colour-electric potential per octet component | `gravity_backreaction.py:L117–141 dielectric_poisson()` | unknown (inferred: quantitative) |
| 6 | $F=\sum[(\nabla f)^2+\tfrac1{4\xi^2}(f^2-1)^2+\tfrac12D^2/\varepsilon_c]$ | dual-GL energy split (grad, bag, field) | `gravity_backreaction.py:L155–161 gl_energy()` | unknown (inferred: exact) |
| 7 | $f(x)=\tanh(x/2\xi)$ | exact kink of $2f''=\xi^{-2}(f^2-1)f$ (zero-field anchor) | `gravity_backreaction.py:L167 gl_kink()` | unknown (inferred: exact) |
| 8 | $D^a=\varepsilon_c(-\nabla\psi^a)$, $D^2=\sum_a\lvert D^a\rvert^2$ | confined flux | `gravity_backreaction.py:L220–221 self_consistent_bag()` | unknown (inferred: quantitative) |
| 9 | $f\leftarrow\operatorname{clip}\!\big(f+\Delta\tau[2\nabla^2f-\xi^{-2}(f^2-1)f-fD^2/\varepsilon_c^2],0,1\big)$ | gradient flow $-\delta F/\delta f$ at frozen $D$ (the back-reaction term is $-fD^2/\varepsilon_c^2$) | `gravity_backreaction.py:L225–228 self_consistent_bag()` | unknown (inferred: quantitative) |
| 10 | $\rho=\lvert\rho^a\rvert$ smeared by $e^{-\lambda^2k^2/2}$; $f^2=e^{-\phi/\phi_0}$, $\varepsilon_c=1-f^2$ | F137 one-way mean-field bag (A/B comparison) | `gravity_backreaction.py:L248–255 meanfield_bag()` | unknown (inferred: exact) |

**Inputs → outputs:** octet colour-charge stack $\rho^a$ → $(f,\varepsilon_c,D^2,\psi,$ energies$)$. Variational check: $\partial_f[\tfrac12D^2/(1-f^2)]=fD^2/\varepsilon_c^2$ confirms #9 is $-\delta F/\delta f$ (ignoring the clip floor). **Depends on:** `casim.numerics.fft` (02). Colour-dielectric physics: see 05a/05b § gauge colour/confinement.

**Flags:** OTHER — misnamed/misfiled: file is colour confinement (F86/F137), not gravity; registry `findings` empty, `exactness` None. ⚠ DOC/CODE MISMATCH — docstring "3D (BCC box)" but every stencil is simple-cubic. The clip floor on $\varepsilon_c$ is not differentiated in #9 (consistent with the docstring's frozen-flux statement).

### `engine/interactions/gravity_band_cutoff.py` — paired photon/graviton band top $\Omega_\text{max}=\pi$ (F357)
**Status:** live · standalone · **Findings:** F357 F248 F69 F26 F79 F107 F352 · **Lattice:** BCC (constituent domain $\lvert q_i\rvert\le\pi\sqrt3/2$, pair $K=2q$) · **Law:** even (control: single-branch doubled) · **Units:** lattice → Planck

**Does:** proves the even law is bounded by $\pi$ on the BZ and converts the band top into a Planck-unit energy.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\arccos(-a)=\pi-\arccos a$; $\partial_b[\arccos a+\arccos b]=-1/\sqrt{1-b^2}$ ⇒ $\arccos a+\arccos b\le\pi\iff a+b\ge0$ | identity/monotonicity theorem (sympy + $2\times10^5$-point numeric) | `gravity_band_cutoff.py:L107–114 check_A_identity_theorem()` | exact (reg) |
| 2 | $u_\pm(q)=\prod\cos(q_i/\sqrt3)\pm\prod\sin(q_i/\sqrt3)$ | BCC branch invariants | `gravity_band_cutoff.py:L151 _u_pm()` | exact (reg) |
| 3 | $\Omega_\text{even}(K)=\arccos u_+(K/2)+\arccos u_-(K/2)$ | physical photon/graviton law | `gravity_band_cutoff.py:L157–160 omega_even()` | exact (reg) |
| 4 | $2\arccos u_+(K/2)$ | control law (not physical) | `gravity_band_cutoff.py:L167–169 omega_chiral_double()` | exact (reg) |
| 5 | $u_++u_-=2\prod\cos(K_i/2\sqrt3)\ge0$ on the domain ⇒ $\Omega_\text{even}\le\pi$; grid max over $\lvert K_i\rvert\le\pi\sqrt3$ | band-top sweep (161³) | `gravity_band_cutoff.py:L184–196 check_C_grid_bandtop()` | quantitative (tol $5\times10^{-4}$) (reg: exact; row is weaker — see flags) |
| 6 | at $\theta_x=\pi/2$: $u_++u_-=0$ identically | saturation on the whole zone face | `gravity_band_cutoff.py:L216–221 check_D_boundary_saturation()` | exact (reg) |
| 7 | $\tau/t_P=(a/\ell_P)/\sqrt3$; $E_\text{max}/E_P=\Omega_\text{max}\sqrt3/(a/\ell_P)=\sqrt{\pi\sqrt3/8}$ | Planck-unit band top, $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ | `gravity_band_cutoff.py:L86, L240–248 check_E_planck_ratio()` | exact (reg) |
| 8 | $E_\text{max}=\pi\sqrt3\,\Lambda_\text{model}$, $\Lambda_\text{model}=E_P/(a/\ell_P)$ | relation to F352's naive cutoff | `gravity_band_cutoff.py:L87, L271–277 check_F_lambda_model_relation()` | exact (reg) |

**Inputs → outputs:** `pairing_law` → six checks, $E_\text{max}/E_P$. **Depends on:** `a_over_ellP` (01-constants.md), `casim.numerics.xp`; mirrors `lattice/bcc.py` $u_\pm$ (03-lattice.md).

**Flags:** ⚠ DOC/CODE MISMATCH (numeric) — docstrings give $E_\text{max}/E_P=0.82479$ (L56) and the title "0.8248" (L332); the closed form the code evaluates, $\sqrt{\pi\sqrt3/8}$, is $0.824727$ (the `run_all` docstring L302 has the right 0.82473). Grid-sweep legs (C, E, F) are tolerance checks, tagged quantitative against registry `exact`.

### `engine/interactions/gravity_core_completeness.py` — bounded curvature ⇒ $C^{1,1}$ regular core; point-group no-go (F354)
**Status:** live · standalone · **Findings:** F354 F183 F284 F178 F107 · **Lattice:** n/a (continuum GR on the two-function class; BCC enters only via $a$ and point groups) · **Law:** n/a · **Units:** geometric / SI presentation

**Does:** shows a global Kretschmann bound forces a regular centre for the two-function metric **$ds^2=-A\,dt^2+dr^2/B+r^2d\Omega^2$** (note: $B=1/g_{rr}$ here, the opposite of `interior_metric.py`), and records that $O_h$ inversion is neither sufficient nor necessary for the parity condition.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathcal K=R_{abcd}R^{abcd}$ by full Christoffel→Riemann contraction | exact Kretschmann of the two-function metric | `gravity_core_completeness.py:L169–196 _kretschmann_two_function()` | exact (reg) |
| 2 | $\mathcal K=4R_{\hat t\hat r}^2+8R_{\hat t\hat\theta}^2+8R_{\hat r\hat\theta}^2+4R_{\hat\theta\hat\phi}^2$; $R_{\hat\theta\hat\phi}=(1-B)/r^2$, $R_{\hat r\hat\theta}=-B'/2r$, $R_{\hat t\hat\theta}=BA'/(2rA)$, $R_{\hat t\hat r}=(2ABA''+AA'B'-BA'^2)/(4A^2)$ | sum-of-squares identity ⇒ $B(0)=1$, $B'(0)=A'(0)=0$ | `gravity_core_completeness.py:L213–219 check_sum_of_squares()` | exact (reg) |
| 3 | control $B=1-\delta$: $\lim_{r\to0}r^4\mathcal K\neq0$ | solid-angle defect detected as unbounded curvature | `gravity_core_completeness.py:L233–238` | exact (reg) |
| 4 | Hayward $m=Mr^3/(r^3+L^3)$, $\rho=m'/(4\pi r^2)$ has an odd $r^3$ term | "not sufficient" leg | `gravity_core_completeness.py:L262–267 check_point_group_nogo()` | exact (reg) |
| 5 | $\oint xyz\,d\Omega=\oint xyz\,r^2d\Omega=\oint xyz(x^4+y^4+z^4)d\Omega=0$ | "not necessary" leg ($T_d$ invariant ring) | `gravity_core_completeness.py:L270–280` | exact (reg) |
| 6 | Reynolds projection over signed permutations: odd-degree $O_h$-invariant polynomials vanish (deg ≤ 6) | polynomial parity | `gravity_core_completeness.py:L346–363 check_polynomial_parity()` | exact (reg) |
| 7 | $f=1-r^2/L^2$: $\dot r^2=E^2-f$; $E=1$: $\tau=\int dr/\sqrt{1-f}\to\infty$, e-fold rate $1/L$; ticks $=(L/a)\ln(L/a)/c_\text{lat}$ | local geodesic regimes at the core | `gravity_core_completeness.py:L392–406 check_geodesics()` | exact (reg) |
| 8 | Laurent screen: $f(0)=1$, parity, no odd powers, non-flat; Hayward lowest odd term $2M r^5/L^6$ | literature screen (ZM calibration) | `gravity_core_completeness.py:L442–462, L470–485` | exact (reg) |
| 9 | $24/L^4=\mathcal K_\text{max}$: $\mathcal K_\text{max}=1/a^4\Rightarrow L=24^{1/4}a$; $=24/a^4\Rightarrow L=a$, e-fold $=\sqrt3$ ticks ($c_\text{lat}=1/\sqrt3$) | core scale under both ceiling conventions | `gravity_core_completeness.py:L534–543 check_scales()` | exact (reg) |
| 10 | Bardeen $g=(2ML^2)^{1/3}$; ratio to F183 proxy $(48M^2a^4)^{1/6}$ is $2^{1/6}$ | profile-specific core radius | `gravity_core_completeness.py:L547–562` | exact (reg) |
| 11 | core $=(96r_g^2a^4)^{1/6}$; $M_\text{crit}=(a/\ell_P)/\sqrt{96}\,M_P$; $M_\text{ext}=\tfrac{3\sqrt3}4\,24^{1/4}(a/\ell_P)M_P\approx19M_P$; covering radius $\sqrt3a/4$ | SI resolvability numbers | `gravity_core_completeness.py:L610–628 check_resolvability()` | quantitative (SI floats) (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** control knobs `solid_angle_deficit`, `core_profile`, `point_group` → seven legs (substrate tier reported, not counted). **Depends on:** `G_CODATA`, `a_over_ellP`, `c_SI`, `c_lat`, `ell_P_m`, `hbar_SI` (01).

**Flags:** OTHER — the ceiling convention ($\mathcal K_\text{max}=1/a^4$ F183 vs $24/a^4$ F284) is recorded as an open decision (L566–570). `MSUN_KG` literal. Metric-function convention $B=1/g_{rr}$ opposite to `interior_metric.py`.

### `engine/interactions/gravity_emergent.py` — QUMOND emergent gravity and its Bullet-Cluster falsifier (F194)
**Status:** live · test-only · **Findings:** (registry: none; docstring F194 F164 F192) · **Lattice:** n/a (continuum grid in Mpc) · **Law:** n/a · **Units:** SI and (Mpc, km/s, $10^{12}M_\odot$)

**Does:** tests the "induced-$G$ enhancement at low acceleration" alternative to dark matter and shows its lensing peak sits on the gas, not the galaxies (falsified by the Bullet Cluster). Not the canonical gravity law.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\rho_\text{crit}=\rho_\Lambda/\Omega_\Lambda$, $H_0=\sqrt{8\pi G\rho_\text{crit}/(3c^2)}$, $a_0=cH_0/6$ | model $a_0$ from the vacuum scale (Verlinde) | `gravity_emergent.py:L69–71 derive_a0_from_vacuum()` | unknown |
| 2 | $\nu(y)=\tfrac12+\sqrt{\tfrac14+1/y}$ | QUMOND simple interpolation | `gravity_emergent.py:L89 nu_simple()` | unknown (inferred: exact) |
| 3 | $M_b(r)=M_d[1-(1+x)e^{-x}]$, $g=\nu(g_N/a_0)g_N$, $v=\sqrt{gr}$; $v_\text{BTF}=(GM_da_0)^{1/4}$ | exponential-disc rotation curve, baryonic Tully–Fisher | `gravity_emergent.py:L103–110 rotation_curve_emergent()` | unknown |
| 4 | $\hat\Phi=-4\pi G\hat\rho/k^2$ (zero-padded $2\times$ box), $g_N=-\nabla\Phi$ | isolated Newtonian Poisson ($\nabla^2\Phi=+4\pi G\rho$) | `gravity_emergent.py:L135–138 _poisson_gN()` | unknown |
| 5 | $\rho_\text{dyn}=-\tfrac1{4\pi G}\nabla\!\cdot(\nu g_N)$, clipped $\ge0$ | QUMOND lensing density | `gravity_emergent.py:L192–193 bullet_cluster_emergent()` | unknown |
| 6 | lensing-peak offsets from gas/galaxy peaks of $\Sigma=\int\rho\,dz$ | the falsifier observable | `gravity_emergent.py:L226–234 bullet_cluster_emergent()` | unknown (inferred: quantitative) |

**Inputs → outputs:** toy gas+galaxy Gaussian blobs → projected lensing profiles and offsets. **Depends on:** `casim.constants.c_SI` only; $G$, $\rho_\Lambda=6\times10^{-10}\,$J/m³, $\Omega_\Lambda=0.69$, $a_0^\text{emp}$ are literals (L50–59).

**Flags:** ⚠ DOC/CODE MISMATCH — module docstring (L28) gives the phantom density as $\rho_\text{ph}=+\tfrac1{4\pi G}\nabla\!\cdot[(\nu-1)g_N]$; code (L192, and its own comment L190–191) computes the **total** dynamical density $-\tfrac1{4\pi G}\nabla\!\cdot(\nu g_N)$ (opposite sign convention, total not phantom). The code form is the correct one for $g=-\nabla\Phi$. OTHER — `G_SI=6.674e-11` and $G$ in astro units are literals, not the model's structural $G$ or `G_CODATA`. Registry exactness None → unknown.

### `engine/interactions/gravity_emqg.py` — EMQG (Paper 6) Poisson + variable-$c$ lensing
**Status:** live · driven (29 ch) · **Findings:** (registry: none) · **Lattice:** periodic square (2-D) / cubic (3-D) FFT grids, continuum $-k^2$ symbol · **Law:** n/a (feeds the Cayley variable-$c$ Weyl stepper) · **Units:** lattice, free $G$

**Does:** matter density → Newtonian potential → local light speed $c(x)$ → `CayleyVarcSolver2D` probe-packet deflection. An older, parallel route to lensing (Ostoma–Trushyk EMQG), distinct from the canonical dielectric of `gravity.py`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\hat\phi(k)=-4\pi G\hat\rho(k)/\lvert k\rvert^2$, $\hat\phi(0)=0$ | periodic 2-D Poisson $\nabla^2\phi=4\pi G\rho$ | `gravity_emqg.py:L54–56 solve_poisson_2d()` | unknown |
| 2 | same, 3-D | periodic 3-D Poisson | `gravity_emqg.py:L90–92 solve_poisson_3d()` | unknown |
| 3 | $\rho\propto e^{-r^2/2\sigma^2}$, $\sum\rho=M$ | Gaussian point mass (2-D, 3-D) | `gravity_emqg.py:L105–107, L143–145` | unknown (inferred: exact) |
| 4 | $c(x)=c_0/(1-2\phi/c_0^2)$, default $c_0=0.5$ | weak-field refractive speed (index $n=1-2\phi/c_0^2$) | `gravity_emqg.py:L133 c_field_from_phi()` | unknown |
| 5 | $\lvert\nabla^2_{5\text{-pt}}\phi-4\pi G\rho\rvert_\infty/\lvert4\pi G\rho\rvert_\infty$ | Poisson contract check (continuum-inverse vs discrete stencil) | `gravity_emqg.py:L168–175`, `L270–277` | unknown (inferred: quantitative) |
| 6 | $\lvert\Delta y(2M)/\Delta y(M)-2\rvert$ | linear-in-$M$ deflection check through `CayleyVarcSolver2D` | `gravity_emqg.py:L187–252, L280–344` | unknown (inferred: quantitative) |

**Inputs → outputs:** $\rho$ → $\phi$ → $c(x)$ → probe centroid shift. **Depends on:** `lattice.curved.CayleyVarcSolver2D` (03-lattice.md § curved), `casim.numerics.fft`.

**Flags:** ⚠ DOC/CODE MISMATCH — module docstring (L8) states $c=c_0/(1+\phi/c_0^2)$; code (L133) computes $c_0/(1-2\phi/c_0^2)$ (function docstring agrees with the code). OTHER — default $c_0=0.5$ is not $c_\text{lat}=1/\sqrt3$; $G$ is a free knob (0.005–0.01), not $G_\text{lat}=1/(72\pi)$; the index $1-2\phi/c^2$ is the linearisation of the canonical $K=e^{-2\Phi/c^2}$, so this route agrees with the dielectric only at $O(\phi)$ and its relation to F64/F178 is undeclared in the module. Functions named `test_*` live in the kernel (L152–344). Registry exactness None → unknown.

### `engine/interactions/gravity_field_equation_uniqueness.py` — why the induced Einstein equation is the only carriable field equation (F345)
**Status:** live · standalone · **Findings:** F345 F178 F297 F59 F319 F288 F291 F326 F79 F107 F64 F106 F309 · **Lattice:** n/a (continuum sympy geometry) · **Law:** n/a · **Units:** geometric; SI for L4

**Does:** sympy legs showing (L1) Bianchi ⇒ conserved symmetric source, (L2) metric variation ⇒ full 10-component $T_{\mu\nu}$, (L3) Gauss–Bonnet topological only in $d=4$, (L4) size of the higher-derivative truncation, (L5/L6) Brans–Dicke and $f(R)$ unhostable. It *supports* F178's canonical law; it does not integrate it.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Gamma^a_{bc}$, $R^a{}_{bcd}=\partial_c\Gamma^a_{bd}-\partial_d\Gamma^a_{bc}+\Gamma^a_{cf}\Gamma^f_{bd}-\Gamma^a_{df}\Gamma^f_{bc}$, $R_{bd}=R^a{}_{bad}$ | symbolic geometry helpers | `gravity_field_equation_uniqueness.py:L97–151` | exact (reg) |
| 2 | $\nabla^\mu G_{\mu\nu}\equiv0$, $\nabla^\mu g_{\mu\nu}\equiv0$ on $\operatorname{diag}(-e^{2f_0},e^{2f_1},e^{2f_2},e^{2f_3})$, $f_i(t,x)$ | L1 Bianchi | `gravity_field_equation_uniqueness.py:L199–212 leg_L1_bianchi()` | exact (reg) |
| 3 | $\partial\sqrt{-g}/\partial g^{\mu\nu}=-\tfrac12\sqrt{-g}\,g_{\mu\nu}$; $T_{\mu\nu}=-2\,\partial L/\partial g^{\mu\nu}+g_{\mu\nu}L$ ⇒ scalar $\partial_\mu\phi\partial_\nu\phi-\tfrac12g_{\mu\nu}(\partial\phi)^2$, Maxwell $F_{\mu a}F_\nu{}^a-\tfrac14g_{\mu\nu}F^2$ | L2 variational source (10 components) | `gravity_field_equation_uniqueness.py:L270–331 leg_L2_variational_source()` | exact (reg) |
| 4 | $\nabla^\mu T_{\mu\nu}=(\Box\phi)\,\partial_\nu\phi$ | L2b on-shell conservation | `gravity_field_equation_uniqueness.py:L367–380 leg_L2b_conservation_on_shell()` | exact (reg) |
| 5 | $H_{\mu\nu}=2[RR_{\mu\nu}-2R_{\mu a}R^a{}_\nu-2R_{\mu a\nu b}R^{ab}+R_\mu{}^{abc}R_{\nu abc}]-\tfrac12\eta_{\mu\nu}\mathcal G$, $\mathcal G=R^2-4R_{ab}R^{ab}+R_{abcd}R^{abcd}$ on random Kulkarni–Nomizu curvature | L3: $H\equiv0$ in $d=4$, $\neq0$ in $d=5$ | `gravity_field_equation_uniqueness.py:L455–466 _lanczos_tensor_flat()`, `L480–528` | exact (reg) |
| 6 | $\varepsilon=(a/L_\text{curv})^2$, $L_\text{curv}^{-2}=r_s/r^3$; horizon $\varepsilon=a^2\sqrt{12}/r_s^2$; BBN $\varepsilon=(aH/c)^2$, $H^2=\tfrac{8\pi G}{3}\rho/c^2$, $\rho=\tfrac{\pi^2}{30}g_*T^4/(\hbar c)^3$ | L4 truncation size (~$10^{-76}\times$ uncomputed O(1)) | `gravity_field_equation_uniqueness.py:L542–576 leg_L4_truncation_suppression()` | quantitative (reg: exact; row is weaker — see flags) |
| 7 | $\gamma_\text{BD}=(1+\omega)/(2+\omega)$; $\gamma=1$ has no finite-$\omega$ root | L5 scalar-tensor | `gravity_field_equation_uniqueness.py:L620–628 leg_L5_scalar_tensor_closed()` | exact (reg) |
| 8 | $f(R)$: $\omega=0\Rightarrow\gamma=\tfrac12$, overshoot $\tfrac12/2.3\times10^{-5}$ | L6 | `gravity_field_equation_uniqueness.py:L694–697 leg_L6_fR_closed()` | exact (reg) |

**Inputs → outputs:** control knobs `lovelock_dim`, `gb_ricci_coeff`, `model_gamma` → eight legs, `all_pass`. **Depends on:** `G_CODATA`, `a_over_ellP`, `c_SI`, `ell_P_m`, `hbar_SI` (01); `particles._results_path` (06a).

**Flags:** ⚠ DOC/CODE MISMATCH — `leg_L2b` docstring (L353) says $\nabla^\mu T_{\mu\nu}=-(\Box\phi)\partial_\nu\phi$; code (L379) and its claim string (L385) test $+(\Box\phi)\partial_\nu\phi$ (the code sign is correct). OTHER — L4 hard-codes $g_*=10.749339$ (L559, "F309") and the eV→J factor as literals rather than registry constants; L7's "≤ 1.4e-76" is a hard-coded string. L4 is numerical (`exactness: "computed"` in its own payload) although the module registry says `exact`. L5 concedes its three "structural sources" share the F64/F106 premise that S4-F178 reclassifies — only $\dot G/G$ is independent.

### `engine/interactions/gravity_four_derivative_locality.py` — locality generates, not forbids, the four-derivative term (F383)
**Status:** live · standalone · **Findings:** F383 F345 F57 F56 F319 · **Lattice:** BCC dispersion, but integrated over the **cubic** box $[-\Lambda,\Lambda)^3$ (F57's BZ proxy), not the BCC Brillouin zone · **Law:** chiral (single branch, `bcc_dispersion(sign="+")`) · **Units:** lattice

**Does:** extends F57's static polarisation to $q^4$ and shows $\Pi_4\neq0$ with robust sign.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Pi(q)=\int_{[-\Lambda,\Lambda)^3}\tfrac{d^3k}{(2\pi)^3}\,\dfrac{1}{\omega(k)+\omega(k+q)}$, $\omega=\arccos u_+(k)$ (midpoint grid; denominators $<10^{-9}$ dropped) | static matter-density polarisation | `gravity_four_derivative_locality.py:L104–111 static_polarization()` | quantitative (reg) |
| 2 | least squares $\Pi(q)=\Pi_0-\Pi_2q^2+\Pi_4q^4[-\Pi_6q^6]$ along a direction | Taylor coefficients | `gravity_four_derivative_locality.py:L126–145 polarization_taylor_fit()` | fit |
| 3 | $\Pi_2$ (quadratic vs quartic fit) consistent with F57's $+0.061$ | M1 regression | `gravity_four_derivative_locality.py:L156–171` | fit |
| 4 | sign of $\Pi_4$ stable over grid/window/direction, magnitudes within $5\times$ (order 4) / $8\times$ (order 6) | M2, M2b | `gravity_four_derivative_locality.py:L212–229, L247–266` | fit |
| 5 | $\Pi_4$ vs $n_\text{grid}$, vs $\Lambda$, vs direction | M3–M5 descriptive | `gravity_four_derivative_locality.py:L279–366` | quantitative (reg) |

**Inputs → outputs:** none (fixed settings) → legs M1–M5, L. **Depends on:** `lattice.bcc.bcc_dispersion` (03-lattice.md § bcc.py), `casim.numerics.xp` (incl. `xp.linalg.lstsq`).

**Flags:** OTHER — integration domain is a cube $[-\pi,\pi)^3$ rather than the BCC zone ($\lvert k_i\rvert\le\pi\sqrt3/2$ per `bcc.py`), and the channel is the scalar/rest-leg single chiral branch; the docstring states both as F57 proxies. Registry `quantitative`; every magnitude is a fit (the docstring itself says only sign and order of magnitude survive). M4's jump at $\Lambda=2.8$ is flagged undiagnosed in-code.

### `engine/interactions/horizon_entanglement.py` — boundary entanglement entropy of the BCC vacuum (F355)
**Status:** live · standalone · **Findings:** F355 F190 F300 F183 F278 · **Lattice:** BCC (conventional cube edge $a=2c_\text{lat}=2/\sqrt3$, primitive bases, crystal zone including the $\omega=\pi$ nodes) · **Law:** chiral (one Weyl walk; both chiralities checked equal) · **Units:** lattice; SI for the curvature scope

**Does:** computes the Gaussian-state entanglement entropy per $a^2$ of one BCC Weyl walk's filled sea (planes and balls) and compares it with the $2\pi\sqrt3$ nats per cell Bekenstein–Hawking needs.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $s_\text{cell}^\text{req}=(a/\ell_P)^2/4=2\pi\sqrt3$ | required nats per horizon cell (F190) | `horizon_entanglement.py:L85` | quantitative (reg) (row read: exact) |
| 2 | $U=u\,\mathbb 1-i\,\mathbf n\cdot\boldsymbol\sigma$: $u=c_xc_yc_z+s\,s_xs_ys_z$, $n_x=s_xc_yc_z-s\,c_xs_ys_z$, $n_y=-s\,c_xs_yc_z+s_xc_ys_z$, $n_z=c_xc_ys_z+s\,s_xs_yc_z$ (phases $\phi_i=k_ia/2$) | BCC walk symbol | `horizon_entanglement.py:L99–103 _uvec()` | quantitative (reg) (row read: exact) |
| 3 | $P_-(p)=\tfrac12(\mathbb1-\hat n\cdot\boldsymbol\sigma)$, $\hat n=\mathbf n/\sin\omega$ | filled-branch projector (controls: flat $\hat n=\hat z$, random $\hat n$) | `horizon_entanglement.py:L114–132 _filled_projector()` | quantitative (reg) (row read: exact) |
| 4 | $S=-\sum_\nu[\nu\ln\nu+(1-\nu)\ln(1-\nu)]$, $\nu\in\operatorname{spec}C_A$ | Peschel entropy | `horizon_entanglement.py:L137–139 von_neumann()` | quantitative (reg) (row read: machine) |
| 5 | $C_{nn'}=\tfrac1{L_3}\sum_je^{ij(n-n')}P(p_\perp,j)$; $c_{hkl}=\dfrac{\overline{S}}{2\,A_\text{cell}/a^2}$ | planar-cut coefficient per $a^2$ | `horizon_entanglement.py:L184–213 _chain_entropy(), plane_coefficient()` | quantitative (reg) |
| 6 | $K(\Delta n)=\mathrm{IFFT}[P]\,e^{i\pi\sum\Delta n_i/L_i}$ (antiperiodic); $C$ restricted to a ball; $c_\text{sphere}=\langle S\rangle/4\pi R^2$ | ball coefficient | `horizon_entanglement.py:L234–295 correlator_kernel(), ball_entropy(), ball_coefficient()` | quantitative (reg) |
| 7 | fit $c(\hat n)=c_0+c_1(\sum n_i^4-\tfrac35)+c_2(\prod n_i^2-\tfrac1{105})$ | cubic-harmonic average | `horizon_entanglement.py:L307–319 cubic_harmonic_average()` | fit |
| 8 | four gapless nodes $\Gamma,R,H,R'$ with Berry charges $\mp1,\pm1$, sum 0 | node count (Nielsen–Ninomiya) | `horizon_entanglement.py:L433–446 weyl_nodes()`, `L449–464 _berry_charge()` | quantitative (reg) (row read: exact) |
| 9 | ratio $=2c_\text{walk}/(\pi\eta\sqrt3)=24c_\text{walk}/(\pi\sqrt3)$, $\eta=\tfrac1{12}$; $c_\text{req}=\pi/(8\sqrt3)$; $s_\text{cell}=N_\text{walks}c_\text{walk}$ for $N\in\{48,24,12\}$ | $g_*$-independent comparison and the node-counting bracket | `horizon_entanglement.py:L481–488, L511–537 node_counting(), horizon_ledger()` | quantitative (reg) (row read: bracketed) |
| 10 | $(a/r_h)^2$, $r_h=2GM/c^2$ | curvature correction scope | `horizon_entanglement.py:L589–592 curvature_scope()` | quantitative (reg) |

**Inputs → outputs:** scale (`gate`/`full`), controls → E9-1…E9-14, $c_\text{walk}=0.720867\pm0.0070$ (reference constant L615), ratio bracket. **Depends on:** `c_lat`, `a_over_ellP`, `G_CODATA`, `c_SI`, `ell_P_m` (01); `casim.numerics.fft, xp` (02).

**Flags:** OTHER — registry exactness `quantitative`, but the module's own node-counting docstring (L479) says the result class is `bracketed`. `C_REQUIRED`, `ETA_WEYL`, `N_WEYL=48`, `MSUN`, and the reference values `C_WEYL_REF`, `C_PLANE_REF` are literals, not registry constants. Local `_results_path` duplicates `particles._results_path` (write is `__main__`-guarded).

### `engine/interactions/horizon_entropy.py` — horizon tiling and required per-cell entropy (F190)
**Status:** live · test-only · **Findings:** (registry: none; docstring F190 F107 F183) · **Lattice:** n/a (F107 cell size only) · **Law:** n/a · **Units:** SI, $k_B=1$

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A=4\pi r_h^2$, $r_h=2GM/c^2$ | horizon area | `horizon_entropy.py:L43–44 horizon_area_m2()` | unknown |
| 2 | $S_\text{BH}=A/(4\ell_P^2)$ | Bekenstein–Hawking | `horizon_entropy.py:L49 bekenstein_hawking_entropy()` | unknown |
| 3 | $N=A/a^2$, $a=(a/\ell_P)\ell_P$ | cell count | `horizon_entropy.py:L54 lattice_cell_count()` | unknown |
| 4 | $s_\text{cell}=a^2/(4\ell_P^2)=2\pi\sqrt3$ | required per-cell entropy | `horizon_entropy.py:L59 required_entropy_per_cell()` | unknown (inferred: exact (closed form; float evaluation)) |
| 5 | $S(M_2)/S(M_1)=(M_2/M_1)^2$ | area-law ratio | `horizon_entropy.py:L74–75 area_law_check()` | unknown |

**Depends on:** `G_CODATA`, `a_over_ellP`, `c_SI`, `ell_P_m`, `hbar_SI` (01). Superseded as a derivation step by F300/F355 (`horizon_entanglement.py`), which computes rather than posits $s_\text{cell}$.

**Flags:** registry exactness None → unknown. `MSUN`, `KB` literals (KB unused).

### `engine/interactions/inspiral.py` — 0PN compact-binary inspiral (F189)
**Status:** live · test-only · **Findings:** (registry: none; docstring F189 F180 F178) · **Lattice:** n/a · **Law:** n/a (graviton speed assumed $=c$) · **Units:** SI via $T_\odot=GM_\odot/c^3$

**Does:** standard GR quadrupole chirp — the model's prediction is GR's, by F178.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathcal M_c=(m_1m_2)^{3/5}/(m_1+m_2)^{1/5}$ | chirp mass | `inspiral.py:L31 chirp_mass_solar()` | unknown (inferred: exact) |
| 2 | $\dot f=\tfrac{96}{5}\pi^{8/3}\mathcal M_c^{5/3}f^{11/3}$ | chirp rate | `inspiral.py:L37 df_dt()` | unknown (inferred: exact) |
| 3 | $\tau=\tfrac5{256}\mathcal M_c^{-5/3}(\pi f)^{-8/3}$ | time to merger | `inspiral.py:L43 time_to_merger()` | unknown (inferred: exact) |
| 4 | $f_\text{GW}=2f_\text{orb}=6^{-3/2}/(\pi M)$ | Schwarzschild ISCO frequency | `inspiral.py:L50–51 isco_gw_frequency()` | unknown (inferred: exact) |
| 5 | RK4 in $f$, $dt=10^{-4}$ s; $\phi=2\pi\int f\,dt$ (trapezoid); $h=(\pi f)^{2/3}\mathcal M_c^{5/3}\cos\phi$ | evolved waveform | `inspiral.py:L63–75 evolve_chirp()` | unknown (inferred: quantitative) |

**Depends on:** `G_CODATA`, `c_SI` (01).

**Flags:** ⚠ DOC/CODE MISMATCH — docstring amplitude $h\sim(4/D)(\pi f)^{2/3}\mathcal M_c^{5/3}$ (L15); code (L74) omits the $4/D$ (and $c$) factor, so `h` is an un-normalised shape (units of seconds), not a strain. Registry exactness None → unknown for the module; per-row tags above are from the closed forms. `MSUN`, `MPC` literals.

### `engine/interactions/interior_metric.py` — covariant two-function interior (TOV) and exact-Schwarzschild legs (F181)
**Status:** live · test-only · **Findings:** (registry: none; docstring F181 F178 F173 F62 F64) · **Lattice:** 2-D grid for the field builders (square), otherwise continuum · **Law:** n/a · **Units:** geometric ($G=c=1$)

**Does:** the F178 interior: two independent metric functions $ds^2=-A\,dt^2+B\,dr^2+r^2d\Omega^2$ (**$B=g_{rr}$**), TOV-integrated and matched to exact Schwarzschild; plus 2-D isotropic-Schwarzschild and (demoted) dielectric backgrounds for the F62/F64 wave-packet battery.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $p=K\rho^\Gamma$ | polytrope EoS | `interior_metric.py:L57–61 Polytrope` | unknown (inferred: exact) |
| 2 | $m'=4\pi r^2\rho$, $\nu'=\dfrac{m+4\pi r^3p}{r(r-2m)}$, $p'=-(\rho+p)\nu'$ | TOV with both metric functions | `interior_metric.py:L73–76 _tov_two_function_rhs()` | unknown (inferred: exact (RHS)) |
| 3 | RK4, surface by linear interpolation to $p=0$; $\nu\to\nu+\tfrac12\ln(1-2M/R)-\nu(R)$; $A=e^{2\nu}$, $B=(1-2m/r)^{-1}$; $z_\text{surf}=(1-2M/R)^{-1/2}-1$ | integrated interior matched to the exterior | `interior_metric.py:L90–118 integrate_interior()` | unknown (inferred: quantitative) |
| 4 | vacuum $A=1-2M/r$, $B=(1-2M/r)^{-1}$ ($AB=1$ only here) | exact Schwarzschild legs | `interior_metric.py:L127–133 metric_AB_areal()` | unknown (inferred: exact) |
| 5 | $u=GM/(rc_0^2)$ (softened, capped below 2): $A=\big(\tfrac{1-u/2}{1+u/2}\big)^2$, $B=(1+u/2)^4$ | isotropic exact Schwarzschild field | `interior_metric.py:L158–163 schwarzschild_isotropic_field()` | unknown (inferred: exact) |
| 6 | $c_\text{eff}=c_0\sqrt{A/B}$; lapse $\sqrt A$ | kinetic-leg speed and redshift factor | `interior_metric.py:L168, L173` | unknown (inferred: exact) |
| 7 | $A=e^{-2u}$, $B=e^{2u}$ | demoted single-scalar dielectric (reference only; agrees at $O(u)$) | `interior_metric.py:L189–192 dielectric_field()` | unknown (inferred: exact) |

**Depends on:** numpy only; consumed by F181 tests and `stellar.py` (07c/07d § stellar, theory='gr'). This is the ledger's "interior carries its second function".

**Flags:** ⚠ DOC/CODE MISMATCH (arithmetic in docstring) — L32 writes $AB=(1-u^2/4)^2(1+u/2)^2$; the code's legs give $AB=(1-u/2)^2(1+u/2)^2=(1-u^2/4)^2$ (the conclusion $AB\neq1$ stands). `MSUN_KM` literal unused. Registry exactness None → unknown. $B$ convention is $g_{rr}$ (opposite to `gravity_core_completeness.py`).

### `engine/interactions/ns_eos.py` — piecewise-polytrope neutron stars on TOV (F184/F356)
**Status:** live · test-only · **Findings:** (registry: none; docstring F184 F356 F181) · **Lattice:** n/a · **Law:** n/a · **Units:** cgs in, geometric (cm) internally, km/$M_\odot$ out

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $K_1=p_1/\rho_1^{\Gamma_1}$, $K_2=K_1\rho_1^{\Gamma_1-\Gamma_2}$, $K_3=K_2\rho_2^{\Gamma_2-\Gamma_3}$, $\rho_{cc}=(K_\text{crust}/K_1)^{1/(\Gamma_1-\Gamma_\text{crust})}$ | Read et al. 2009 piece constants | `ns_eos.py:L67–72 PiecewisePolytrope.__init__` | unknown (inferred: exact) |
| 2 | $a_i=a_{i-1}+\dfrac{K_{i-1}\rho_b^{\Gamma_{i-1}-1}}{(\Gamma_{i-1}-1)c^2}-\dfrac{K_i\rho_b^{\Gamma_i-1}}{(\Gamma_i-1)c^2}$ | energy-density continuity | `ns_eos.py:L79–83` | unknown (inferred: exact) |
| 3 | $p=K_i\rho^{\Gamma_i}$; $\varepsilon=(1+a_i)\rho+\dfrac{K_i\rho^{\Gamma_i}}{(\Gamma_i-1)c^2}$ | EoS | `ns_eos.py:L97, L102, L108–109` | unknown (inferred: exact) |
| 4 | $m'=4\pi r^2\varepsilon$, $p'=-(\varepsilon+p)\dfrac{m+4\pi r^3p}{r(r-2m)}$ (geometric via $G/c^2$, $G/c^4$) | TOV | `ns_eos.py:L124–127 integrate_tov.rhs` | unknown (inferred: exact (RHS)) |
| 5 | RK4, $h=500$ cm; $z=(1-2M/R)^{-1/2}-1$ | $R$, $M$, surface redshift | `ns_eos.py:L129–143 integrate_tov()` | unknown (inferred: quantitative) |
| 6 | $M_\text{max}$, $R_{1.4}$ on the stable branch over $\rho_c\in[3\times10^{14},4\times10^{15}]$ | summary observables | `ns_eos.py:L157–167 summarize()` | unknown (inferred: quantitative) |

**Depends on:** numpy only. **Flags:** OTHER — `G_CGS`, `C_CGS`, `MSUN_CM` and the Read et al. table are literals, not registry constants (D7); the model's structural $G$ is not used (GR with CODATA $G$). Registry exactness None → unknown.

