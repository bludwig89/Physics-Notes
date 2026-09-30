# Particles I — derivation scripts, atom and baryons

*Model-map section p06a · written 2026-09-28 - 00:00 · source of truth: the code at the cited lines.*

**Scope.** The `src/casim/engine/particles/` modules that are either (i) bound-state kernels for the atom and the three-quark baryon, or (ii) standalone `derive_*` analysis scripts (lepton shape chain, PMNS/residual-symmetry no-gos, Majorana scale, Higgs compositeness, quark-shape probes, colour condensate). None of these modules runs a lattice time-step; the only lattice object touched is the BCC Dirac step in `derive_lepton_frame_fork.sea_energy` (via `lattice.bcc.bcc_unitary`, see 03-lattice.md § bcc.py). Everything else is closed-form algebra (sympy/`Fraction`), dense linear algebra, or 1-D ODE/quadrature.

**Shared conventions.**
- *Lattice:* `n/a` unless stated; the "shell" in F342/F403/F406 is the BCC nearest-neighbour shell $(\pm1,\pm1,\pm1)$ with point group $O_h$, generations as the $T_{1u}$ triplet (F75).
- *Law:* no propagator is used except the BCC chiral-branch walk in F406 K2 (both branches $\pm$ summed, so branch-blind).
- *Units:* atom = SI-ish (eV, MeV, nm; CODATA literals); baryon ECG = units of $\sqrt\sigma$ ($\sigma=1$), converted to MeV only through `sqrt_sigma_GeV`; NJL = GeV; lepton shape = dimensionless ratios ($\tau$ wall-pinned, $y_\tau=1$ or $\mu=1$).
- *Lepton-shape chain (CLAUDE.md decision 7):* $\delta^*=\tfrac29$ rad is **primary** (`casim.constants.delta_star = Fraction(2,9)`, exact, F175/F253/F255/F256). $\lambda_6$ is registered as `lambda_6 = 0.243` (**a literal value**, `quantitative`, tol $5\times10^{-3}$, provenance F234/F253/F256, `constants/lepton.py:L116`), described as the *output* $\lambda_6=\lvert B\rvert/(2e^6\cos\tfrac23)$. Which modules compute it and which import it as an input is recorded per module below and summarised in the flags.
- Two parametrisations of the Koide circulant coexist: $\sqrt{m_a}\propto1+2\sqrt{\eta^2}\cos(\delta+2\pi a/3)$ with $\eta^2=\tfrac12$ (F175/F92; `derive_lepton_shape_precision_floor`), and $\sqrt{m_a}\propto1+\eta\cos(\ldots)$ with $\eta=\sqrt2$, i.e. "$\eta^2=2$" (`derive_quark_shape_probe`, `derive_quark_mixed_koide_probe`). Same physics, different symbol meaning.
- Most scripts import `numpy`/`scipy` directly (D8 debt, ratcheted elsewhere); noted per module only where it matters for a hazard.

**Modules covered (21):** `__init__.py`, `_results_path.py`, `atom.py`, `baryon.py`, `baryon_dynamics.py`, `baryon_mass_decomposition.py`, `derive_M_R_scale_link.py`, `derive_colour_condensate.py`, `derive_composite_scalar_fermion_coupling.py`, `derive_delta_cp_t2g.py`, `derive_generation_identification_gap.py`, `derive_generator_norm.py`, `derive_higgs_bhl_compositeness.py`, `derive_lambda6_sextic.py`, `derive_lepton_frame_fork.py`, `derive_lepton_shape_precision_floor.py`, `derive_oh_residual_pmns.py`, `derive_quark_B_colour_charge.py`, `derive_quark_mixed_koide_probe.py`, `derive_quark_shape_probe.py`, `derive_t2g_pmns.py`.

---

### `engine/particles/__init__.py` — package marker
Plumbing: empty package docstring (`__init__.py:L1-6`); not in the module registry as a separate record. No equations.

### `engine/particles/_results_path.py` — locate `test-results/`
**Status:** live · package-only · **Findings:** — · **Lattice/Law/Units:** n/a
Plumbing: walks up from `__file__` to the first `test-results/` directory (`_results_path.py:L26 _find_results_dir()`), cached lazily (`L42 results_dir()`), `L57 results_path(name)`. No physics. Used by the `__main__` blocks of most scripts below.

---

### `engine/particles/atom.py` — hydrogen, positronium, Dirac–Coulomb fine structure (P5)
**Status:** live · test-only · **Findings:** (registry: none; F125-P5 per exactness-inventory) · **Lattice:** n/a (continuum radial ODE) · **Law:** n/a · **Units:** SI-ish (MeV, eV, nm); dimensionless solver in Bohr units $x=r/a_0$, Dirac solver in $\hbar=c=m_e=1$

**Does:** solves the non-relativistic Coulomb radial problem on a finite-difference grid and the exact/numerical Dirac–Coulomb spectrum, with $m_e,m_p,\alpha$ as CODATA literals (`atom.py:L84-88`).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mu=m_1m_2/(m_1+m_2)$ | two-body reduced mass | `atom.py:L93 reduced_mass_MeV()` | unknown (inferred: exact) |
| 2 | $\mathrm{Ry}=\tfrac12\mu c^2(Z\alpha)^2$ | absolute Rydberg (eV) | `atom.py:L99 rydberg_eV()` | quantitative (inventory #44, F125-P5-D) |
| 3 | $a_0=\hbar c/(\mu c^2 Z\alpha)$ | Bohr radius (nm) | `atom.py:L104 bohr_radius_nm()` | unknown (inferred: exact (closed form)) |
| 4 | $H=-\tfrac12\partial_x^2+\tfrac{l(l+1)}{2x^2}-\tfrac1x$, tridiagonal: diag $=1/h^2+l(l+1)/(2x^2)-1/x$, off $=-1/(2h^2)$, $u(0)=u(x_\max)=0$ | FD radial Coulomb operator | `atom.py:L128-129 radial_coulomb_levels()` | unknown (inferred: quantitative (grid)) |
| 5 | $E[\mathrm{Ry}]=2\varepsilon\ (\to-1/n^2)$ | eigenvalue conversion | `atom.py:L132 radial_coulomb_levels()` | unknown (inferred: quantitative) |
| 6 | $E_{n,l}=E[\mathrm{Ry}]\cdot\mathrm{Ry}$; positronium uses $\mu=m_e/2$ | absolute spectrum; Ps = H$_\infty$/2 | `atom.py:L158 hydrogen_spectrum()`, `L284 hydrogen_registry()` | Ps ratio exact (inventory #160) |
| 7 | $\kappa=-(l+1)\ (j=l+\tfrac12),\ \kappa=+l\ (j=l-\tfrac12)$ | Dirac quantum number | `atom.py:L169 kappa_of()` | unknown (inferred: exact) |
| 8 | $E/mc^2=[1+(Z\alpha/(n_r+\gamma))^2]^{-1/2}$, $\gamma=\sqrt{\kappa^2-(Z\alpha)^2}$, $n_r=n-\lvert\kappa\rvert$ | Sommerfeld spectrum | `atom.py:L177 sommerfeld_energy()` | exact; $2s_{1/2}=2p_{1/2}$ degeneracy exact (inventory #161) |
| 9 | $E_b\approx-\tfrac12mc^2\tfrac{(Z\alpha)^2}{n^2}[1+\tfrac{(Z\alpha)^2}{n^2}(\tfrac{n}{j+1/2}-\tfrac34)]$ | $O(\alpha^4)$ expansion | `atom.py:L191-192 fine_structure_series_eV()` | unknown (inferred: exact (series)) |
| 10 | $G'=-\tfrac\kappa rG+(E-V+1)F,\ F'=\tfrac\kappa rF-(E-V-1)G,\ V=-Z\alpha/r$ | radial Dirac ODE | `atom.py:L205-206 _dirac_rhs()` | — |
| 11 | ICs $G_0=r_0^\gamma,\ F_0=\tfrac{\gamma+\kappa}{Z\alpha}r_0^\gamma$; tail $F/G=-\sqrt{1-E^2}/(E+1)$; mismatch $G_\text{out}F_\text{in}-F_\text{out}G_\text{in}$ | RK4 shooting + bisection | `atom.py:L230-243 _dirac_mismatch()`, `L246 numerical_dirac_energy()` | quantitative ($\le1.3\times10^{-6}$, inventory #46) |

**Inputs → outputs:** $(m_e,m_p,\alpha,Z,N)$ → level dict in eV, Ry, $a_0$; Sommerfeld/numerical Dirac energies.  **Depends on:** scipy `eigh_tridiagonal` (numpy fallback `L64`).  **Flags:** all physical constants are local CODATA literals (`L84-88`), not `casim.constants`; $\alpha$ is empirical input; registry records no findings/exactness for this module.

---

### `engine/particles/baryon.py` — colour-singlet three-quark operator (F71)
**Status:** live · driven (9 ch) · **Findings:** (registry: none; F71 per inventory) · **Lattice:** n/a (per-site colour algebra; broadcasts over any lattice shape) · **Law:** n/a · **Units:** n/a (dimensionless)

**Does:** builds $B=\varepsilon_{abc}q_1^aq_2^bq_3^c$ and verifies gauge invariance, zero colour charge, exact proton quantum numbers, SU(6) symmetry and Fermi antisymmetry. Colour conventions from `gauge.strong` ($T^a=\lambda^a/2$).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\varepsilon_{012}=+1$, totally antisymmetric | colour tensor | `baryon.py:L45 levi_civita_3()` | unknown (inferred: exact (F71-BS1)) |
| 2 | $B(x)=\varepsilon_{abc}q_1^aq_2^bq_3^c$ | baryon interpolating field | `baryon.py:L72 baryon_field()` | unknown (inferred: exact) |
| 3 | $\max\lvert B[Vq]-B[q]\rvert$, $B\to\det V\,B$ | local SU(3) invariance | `baryon.py:L110 singlet_gauge_residual()`; `L115 det_residual_field()` | unknown (inferred: machine ($1.2\times10^{-15}$, F71-BS3)) |
| 4 | $\lvert S\rangle=\tfrac1{\sqrt6}\varepsilon_{abc}\lvert abc\rangle$; $G^a=T^a\otimes1\otimes1+\ldots$; $\max_a\lVert G^a\lvert S\rangle\rVert$, $C_2=\sum_a(G^a)^2$ | zero colour charge / Casimir | `baryon.py:L132, L142-144, L148 singlet_charge_residual(), L160 singlet_casimir()` | unknown (inferred: machine ($1.4\times10^{-16}$, F71-BS4)) |
| 5 | $Q=\sum q_f=1,\ B=3\cdot\tfrac13=1,\ T_3=\tfrac12$; GMN $Q=T_3+Y/2$, $Y_{Q_L}=\tfrac13$ | proton quantum numbers (Fraction) | `baryon.py:L194-198 proton_quantum_numbers()` | unknown (inferred: exact (F71-BS5)) |
| 6 | $\lvert p\uparrow\rangle\propto2\,\mathrm{Sym}(u\uparrow u\uparrow d\downarrow)-\mathrm{Sym}(u\uparrow u\downarrow d\uparrow)$, $\lVert\cdot\rVert^2=18$ | SU(6) spin–flavour w.f. | `baryon.py:L247-254 proton_spin_flavour_wavefunction()` | unknown (inferred: exact (F71-BS6)) |
| 7 | total sign $=(-1)_\text{colour}(+1)_\text{sf}(+1)_\text{space}$ | Fermi antisymmetry | `baryon.py:L294-302 total_wavefunction_antisymmetry()` | unknown (inferred: exact (F71-BS7)) |
| 8 | $V(R)=\sigma(\beta)R$, $\sigma$ from `gauge.confinement.string_tension` | isolation energy diverges | `baryon.py:L318-319 quark_isolation_energy()` | unknown (inferred: exact identity (F71-BS8)) |

**Inputs → outputs:** colour triplets (from `gauge.strong._colour_triplet`), SU(3) field $V(x)$, $\beta$ → residuals, Fractions, $\sigma R$ table.  **Depends on:** `gauge.strong` (T_GEN), `gauge.confinement` (see 05b/05c).  **Flags:** `total_wavefunction_antisymmetry` sets the total sign equal to the colour sign (`L298`) — the spin-flavour and space factors are asserted $+1$, not computed (spin-flavour symmetry *is* checked separately via `sf_res`; spatial symmetry is not). Structural only, no dynamics (the module says so).

---

### `engine/particles/baryon_dynamics.py` — dynamical three-quark Cornell bound state (P2, F122)
**Status:** live · driven (3 ch) · **Findings:** (registry: none; F122/F372 per docstring & inventory) · **Lattice:** n/a (continuum ECG variational basis) · **Law:** n/a · **Units:** $\sqrt\sigma=1$; MeV via `sqrt_sigma_GeV`

**Does:** rest-frame equal-mass three-body Hamiltonian in Jacobi coordinates, expanded in explicitly-correlated Gaussians with closed-form matrix elements; generalised eigenproblem solved two ways.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $r_p=w_p\cdot\xi$, $w_{12}=(\sqrt2,0)$, $w_{13}=(\tfrac{\sqrt2}2,\tfrac{\sqrt6}2)$, $w_{23}=(-\tfrac{\sqrt2}2,\tfrac{\sqrt6}2)$ | Jacobi pair vectors, $\lVert w\rVert^2=2$ | `baryon_dynamics.py:L98-102 PAIR_W` | unknown (inferred: exact) |
| 2 | $S_{AB}=\det(C)^{-3/2}$, $C=A+B$ | ECG overlap ($(2\pi)^3$ dropped) | `L110 _overlap()` | unknown (inferred: exact) |
| 3 | $\langle T\rangle/S=\tfrac3{2m}\mathrm{Tr}(AC^{-1}B)$ | kinetic element | `L116 _kinetic_over_S()` | unknown (inferred: exact) |
| 4 | $\beta_p=w_p^TC^{-1}w_p$; $\langle r\rangle/S=\sqrt{8\beta_p/\pi}$; $\langle1/r\rangle/S=\sqrt{2/(\pi\beta_p)}$; $\langle r^2\rangle/S=3\beta_p$ | pair-distance elements | `L122, L127, L132, L137` | unknown (inferred: exact) |
| 5 | $R_\text{cyc}=\begin{pmatrix}-\tfrac12&\tfrac{\sqrt3}2\\-\tfrac{\sqrt3}2&-\tfrac12\end{pmatrix}$, $A\mapsto R^TAR$ | $S_3$ closure of basis | `L151, L162-163 symmetrize_basis()` | unknown (inferred: exact) |
| 6 | $H_{ij}=T+\sum_p(s\,\sigma\langle r_p\rangle-\kappa_c\alpha_s\langle1/r_p\rangle)S$, defaults $s=1$, $\kappa_c=\tfrac23$ | Cornell Hamiltonian matrix | `L211-223 build_HS()` | — |
| 7 | $S=U\,s\,U^T$, keep $s_i/s_\max>10^{-10}$, $X=U s^{-1/2}$, eig of $X^THX$ | canonical orthogonalisation | `L234-243 _solve_canonical()` | unknown (inferred: machine) |
| 8 | $L^{-1}HL^{-T}$ (Cholesky) vs `scipy.eigh(H,S)` | two-route solve | `L249-254, L261` | machine ($4.5\times10^{-12}$, inventory #65) |
| 9 | $\langle r_p\rangle,\langle1/r_p\rangle$ in ground vector, $S$-normalised | pair radii (equal by $S_3$) | `L282 pair_radii()`, `L375 pair_inv_radii()` | machine ($8.3\times10^{-11}$, inventory #156) |
| 10 | $E_\text{HO}=3\sqrt{3k/m}$ for $V_p=\tfrac12kr_p^2$ | harmonic self-test | `L338 harmonic_ground_energy_exact()`, `L341` | unknown (inferred: machine ($5.2\times10^{-14}$, #155)) |
| 11 | $X=\alpha_\text{em}\langle1/r\rangle\sqrt\sigma$; $\delta_\text{EM}=X\sum_{i<j}q_iq_j$ with $\sum q_iq_j=0$ (p), $-\tfrac13$ (n) | pairwise EM self-energy (F372) | `L405-406, L441-445 em_self_energy_pairwise()` | unknown (inferred: quantitative) |
| 12 | $M=3m_q+E_\text{rel}$ | baryon mass | `L464 baryon_mass()` | unknown (inferred: quantitative (F122-S5, #39)) |
| 13 | $m_n-m_p=(m_d-m_u)+(\delta_n^\text{EM}-\delta_p^\text{EM})$ | n–p splitting (first order) | `L482-487 neutron_minus_proton()` | unknown (inferred: quantitative (F122-S8, #40)) |

**Inputs → outputs:** $(m_q,\sigma,\alpha_s)$, basis → $E_\text{rel}$, $M$, pair radii, EM self-energies (MeV).  **Depends on:** `casim.constants.sqrt_sigma_GeV` $=0.42$ GeV (quantitative, F122/F124/F146, `constants/strong.py:L553`); `ALPHA_EM` local CODATA literal (`L397`).  **Flags:** ⚠ DOC/CODE MISMATCH — module docstring (`L41-42`) gives the per-pair potential as $V_p=\tfrac\sigma2r-\tfrac{\alpha_s}3\tfrac1r$ (the "½ rule"), while `build_HS` defaults (`L195, L211-212`) compute $V_p=\sigma r-\tfrac23\alpha_s/r$; the ½-rule is only the non-default `conf_per_pair=0.5, oge_casimir=1/3`. `neutron_minus_proton` takes the EM terms as external arguments (F122 used $\delta^\text{EM}_p=1.00$ MeV, ad hoc); `em_self_energy_pairwise` is the model-native replacement but is not wired into it. $m_q,\alpha_s$ are inputs (baseline $m_q=0.785,\alpha_s=0.5$).

---

### `engine/particles/baryon_mass_decomposition.py` — Ji four-term nucleon mass decomposition (F402)
**Status:** live · standalone · **Findings:** F402 F122 F123 F77 F144 F152 · **Lattice:** n/a · **Law:** n/a · **Units:** GeV (NJL); $\sqrt\sigma$ (Cornell)

**Does:** builds $M=H_E+H_m+H_g+H_a$ from the trace sum rule in two model sectors (NJL constituent nucleon; F122 Cornell string) and evolves the gluon momentum fraction at LO.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $H_E=\tfrac34(x_qM-H_m)$, $H_g=\tfrac34x_gM$, $H_a=\tfrac14(M-H_m)$, $x_g=1-x_q$ | Ji quartet (sums to $M$ identically) | `baryon_mass_decomposition.py:L115-118 ji_quartet()` | quantitative (reg) (row read: exact) |
| 2 | $\tfrac{dI_1}{dM}=\tfrac{M}{2\pi^2}\big(\tfrac{\Lambda}{E_\Lambda}-\ln\tfrac{\Lambda+E_\Lambda}{M}\big)$ | tadpole derivative | `L148-149 njl_dI1_dM()` | quantitative (reg) (row read: exact) |
| 3 | $D=1-4GN_cN_f(I_1+MI_1')$; $\partial_{m_0}M=1/D$, $\partial_GM=4N M I_1/D$, $\partial_\Lambda M=4GNM\tfrac{\Lambda^2}{2\pi^2E_\Lambda}/D$ | implicit gap-equation derivatives of $M=m_0+4GN_cN_fMI_1$ | `L158-165 njl_derivatives()` | quantitative (reg) (row read: exact (closed form)) |
| 4 | $M_N=3M_c$, $H_m=3m_0\partial_{m_0}M$, contact $=-2G\cdot3\partial_GM$, regulator $=3\Lambda\partial_\Lambda M$; dilatation $M_N=H_m+\text{contact}+\text{regulator}$ | NJL sigma term & trace identity | `L177-187 njl_nucleon_analog()` | quantitative (reg) (row read: machine (per docstring `L78`)) |
| 5 | $H_m=3m-\langle T\rangle$, $H_E=2\langle T\rangle$, $H_g=\tfrac12\langle V_\text{conf}\rangle+\langle V_\text{coul}\rangle$, $H_a=\tfrac12\langle V_\text{conf}\rangle$; $x_q=\tfrac43(\tfrac94m+\tfrac54\langle T\rangle)/M$; virial $2\langle T\rangle=\langle V_\text{conf}\rangle-\langle V_\text{coul}\rangle$ | Cornell quartet | `L240-252 cornell_quartet()` | quantitative (reg) (row read: machine (identities)) |
| 6 | $m\partial_mM=3m-\langle T\rangle$, $\sigma\partial_\sigma M=\langle V_\text{conf}\rangle$, $\alpha\partial_\alpha M=\langle V_\text{coul}\rangle$ (central FD, $h=10^{-4}$) | Hellmann–Feynman check | `L271-284 cornell_fh_residuals()` | quantitative (reg) |
| 7 | $x_g^\infty=\tfrac{16}{16+3n_f}$, $\lambda=\tfrac{16}9+\tfrac{n_f}3$; $x_g(\tau)=x_g^\infty+(x_{g0}-x_g^\infty)e^{-\lambda\tau}$ | LO second-moment DGLAP | `L293-294 dglap_asymptote()`, `L300 x_g_evolved()` | quantitative (reg) (row read: exact) |
| 8 | $\tau_\text{req}=-\ln\tfrac{x_\infty-x_t}{x_\infty-x_0}/\lambda$; $x_{g0}=x_\infty+(x_t-x_\infty)e^{\lambda\tau}$ | inverse evolution | `L306, L313` | quantitative (reg) (row read: exact) |
| 9 | $\tau=\int\tfrac{\alpha_s}{2\pi}d\ln\mu^2$ (trapezoid); IR band $\tau_\text{IR}=\tfrac{\alpha_\text{eff}^*}{2\pi}\ln(\mu_\text{pert}^2/\Lambda_\text{NJL}^2)$ | model evolution length | `L330 tau_integral()`, `L346-348 evolution_scenarios()` | quantitative (reg) |

**Inputs → outputs:** registered NJL triple $\Lambda_\text{NJL}=0.6515$ GeV, $G\Lambda^2=2.10$, $m_0=5.5$ MeV (**external/fitted**, F77/F116); $\alpha_s(\mu)$ from `interactions.running_alpha_s` (F144); $\alpha^*_\text{eff}\in[0.376,0.411]$ (`endpoint`, bracketed, F145/F152); F122 baseline $(m,\sigma,\alpha_s)=(0.785,1,0.5)$ → quartet percentages, $\sigma_N$, pulls vs lattice targets (`L123 lattice_targets()`, comparison only).  **Depends on:** `baryon_dynamics` ECG kernels (above), `particles.meson.gap_solve/I1_closed` (06b), `interactions.running_alpha_s` (07x).  **Flags:** $x_{g0}=0$ at $\Lambda_\text{NJL}$ is an input choice (docstring says so); lattice targets are literals (fine, comparison only).

---

### `engine/particles/derive_M_R_scale_link.py` — does anything fix the Majorana scale $M_R$? (F343)
**Status:** live · standalone · **Findings:** F343 F47 F79 F107 F201 F236 F253 F282 F341 · **Lattice:** n/a · **Law:** n/a · **Units:** GeV

**Does:** six-leg mechanical null result: cutoff hierarchy, a ratio-power scan, the F79 non-precedent, and blindness of the $Z_3/E_g$ texture to $M_{R0}$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Lambda=3^{-1/4}M_\text{Pl}$, $M_\text{Pl}=1.220890\times10^{19}$ GeV (non-reduced) | lattice cutoff (F282) | `derive_M_R_scale_link.py:L51-54, L64 lattice_cutoff_gev()` | exact (reg) |
| 2 | $\log_{10}(\Lambda/M_{R0})$, $M_{R0}=1$ GeV (F201 benchmark, accommodated) | hierarchy | `L73-80 c1_cutoff_hierarchy()` | exact (reg) |
| 3 | $\min_{r,p}\lvert p\log_{10}r-\log_{10}(M_{R0}/\Lambda)\rvert$, $r\in\{\delta^*,G_\text{lat}=\tfrac1{72\pi},\sqrt2,6\lambda_6,8\pi\sqrt3,1/(a/\ell_P)\}$, $p\le12$ | coincidence scan (72 samples) | `L107-126 c2_ratio_scan()` | exact (reg) |
| 4 | $1/(8\pi\sqrt3)$ | F79 $G$ prefactor, $O(10^{-2})$ | `L157 c3_G_has_no_hierarchy()` | exact (reg) |
| 5 | $\partial_{M_{R0}}\big[M_{R0}(1+\sqrt2\cos(\delta+2\pi a/3))/M_{R0}\big]=0$ (sympy) | $M_{R0}$ factors out | `L183-190 c4_texture_factors_out_M_R0_symbolically()` | exact (reg) |
| 6 | ratios of $\lambda\cdot$`z3_sqrt_texture`$(\delta_\nu)$ invariant, $\delta_\nu=134.86°$ | numeric blindness | `L207-227 c5_...()` | machine (reg: exact; row is weaker — see flags) |
| 7 | source scan of `particles.majorana` imports for "gauge"/"running" | no dynamical route for $\nu_R$ | `L254-264 c6_...()` | n/a (code inspection) |

**Inputs → outputs:** constants `delta_star_f` (2/9, F175), `G_LATTICE` $=1/(72\pi)$ (F79/F107), `a_over_ellP` $=\sqrt{8\pi}\,3^{1/4}$ (F79/F107), `lambda_6` (0.243, registered literal) → six booleans (`L293 check_M_R_scale_link_null_result()`).  **Depends on:** `particles.majorana.z3_sqrt_texture` (06b).  **Flags:** $\Lambda$ here is $3^{-1/4}M_\text{Pl}$ with the **non-reduced** Planck mass; `derive_higgs_bhl_compositeness` defines the same "model cutoff" as $E_P/(a/\ell_P)$, which is smaller by exactly $\sqrt{8\pi}$ (verified: $9.277\times10^{18}$ vs $1.850\times10^{18}$ GeV). Registry says `exact`, but C2/C5 are numeric scans. $\lambda_6$ enters only as a scan sample (imported registry value, not recomputed). C4 multiplies the √-amplitude by $M_{R0}$; `derive_t2g_pmns` multiplies the *squared* amplitude by `MR0` — different scale conventions.

---

### `engine/particles/derive_colour_condensate.py` — colour-magnetic condensate derived (F88)
**Status:** live · test-only · **Findings:** (registry: none; F88 per docstring/inventory) · **Lattice:** n/a (continuum SU(2) reduction) · **Law:** n/a · **Units:** continuum natural; metric $\eta=\mathrm{diag}(1,-1,-1,-1)$

**Does:** four sympy certificates: Nielsen–Olesen instability, scalar control, Savvidy potential, dual sine-Gordon (Debye mass, BPS tension).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+g\epsilon^{abc}A^b_\mu A^c_\nu$ | SU(2) field strength | `derive_colour_condensate.py:L94-100 _ym_field_strength()` | unknown (inferred: exact) |
| 2 | $E^{\nu a}=\partial_\mu F^{\mu\nu a}+g\epsilon^{abc}A^b_\mu F^{\mu\nu c}$ | YM EOM | `L111-125 _ym_eom()` | unknown (inferred: exact) |
| 3 | background $A^3=(0,-By/2,Bx/2,0)$, fluctuation $e^{\gamma t}e^{-gB(x^2+y^2)/4}$; linearised EOM closes iff $\gamma^2=+gB$ (aligned spin); not at $2gB$ | Nielsen–Olesen growing mode | `L131-158 derive_D1_nielsen_olesen()` | unknown (inferred: exact (F88-CC1)) |
| 4 | $-D^2\psi=+gB\,\psi$, $D_j=\partial_j-igA_j$ | scalar control, $\omega^2=+gB$ | `L169-172 derive_D1b_scalar_control()` | unknown (inferred: exact) |
| 5 | $2\zeta_H(-1,\tfrac32)+2\zeta_H(-1,-\tfrac12)=-\tfrac{11}6$; log coeff $\tfrac{11}{96\pi^2}$ | Savvidy coefficient | `L190-197 derive_D2_savvidy()` | unknown (inferred: exact (F88-CC2)) |
| 6 | $V=\tfrac{B^2}2+cg^2B^2(\ln\tfrac{gB}{\mu^2}-\tfrac12)$; $B_\min=\tfrac{\mu^2}ge^{-1/(2cg^2)}$, $V_\min=-\tfrac12cg^2B_\min^2$; $\mathrm{Im}V=\tfrac{g^2B^2}{16\pi}$ | minimum & decay rate | `L202-218` | unknown (inferred: exact) |
| 7 | $m_D^2=2z/\kappa$; $\sigma_\text{dual}=8\sqrt{2\kappa z}$; kink $\chi=4\arctan e^{m\xi}$, $m=\sqrt{2z/\kappa}$ | dual sine-Gordon | `L237-263 derive_D3_sine_gordon()` | unknown (inferred: exact (F88-D3)) |

**Inputs → outputs:** symbols only → booleans / closed forms.  **Depends on:** sympy.  **Flags:** exactness-inventory row F88-CC2 describes the two zeta sums as "$-\tfrac{11}{12}$ each"; the code checks only their total $-\tfrac{11}6$ (`L193`), not the split. SU(2) reduction of SU(3) $f^{abc}$ is a stated simplification. Registry records no findings/exactness for this module.

---

### `engine/particles/derive_composite_scalar_fermion_coupling.py` — σ–quark coupling and species locality (F399)
**Status:** live · standalone · **Findings:** F399 F73 F74 F77 · **Lattice:** n/a · **Law:** n/a · **Units:** GeV (NJL)

**Does:** extracts the NJL scalar residue coupling $g_{\sigma qq}$ at the σ pole and shows the RPA meson propagator is species-diagonal when the contact matrix is.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $I_1=\tfrac1{4\pi^2}\big[\Lambda E_\Lambda-M^2\ln\tfrac{\Lambda+E_\Lambda}M\big]$ | tadpole | `derive_composite_scalar_fermion_coupling.py:L66 _I1_closed()` | quantitative (reg) (row read: exact) |
| 2 | $K(0)=\tfrac1{8\pi^2}\big[\ln\tfrac{\Lambda+E_\Lambda}M-\tfrac\Lambda{E_\Lambda}\big]$ | bubble at $q^2=0$ | `L72 _K0_closed()` | quantitative (reg) (row read: exact) |
| 3 | $K(q^2)=\tfrac1{2\pi^2}\int_0^\Lambda\tfrac{p^2}{E(4E^2-q^2)}dp$ (trapezoid, $2\times10^5$) | bubble, quadrature | `L82-84 _K_quad()` | quantitative (reg) |
| 4 | $K(4M^2)=\tfrac1{8\pi^2}\ln\tfrac{\Lambda+E_\Lambda}M$ | σ-pole bubble, closed form | `L105 _K_sigma_pole_closed()` | quantitative (reg) (row read: exact (spot-check: closed $0.0191976$ vs quad $0.0191974$ at $M=0.3,\Lambda=0.65$)) |
| 5 | $M=m_0+4GN_cN_fMI_1(M)$, damped fixed point | gap equation | `L112-115 gap_solve()` | quantitative (reg) |
| 6 | $f_\pi^2=4N_cM^2K(0)$; $g_{\pi qq}=[2N_cN_fK(0)]^{-1/2}$; $g_{\sigma qq}=[2N_cN_fK(4M^2)]^{-1/2}$ | decay constant, residue couplings | `L121, L128, L136` | quantitative (reg) (row read: exact (closed forms)) |
| 7 | $\Pi_{aa}=2N_cN_f[I_1+(q^2-4M_a^2)K(q^2)]$, $\Pi$ diagonal by construction; $D=[(2G)^{-1}-\Pi]^{-1}$ | 2-flavour RPA propagator | `L160-165 two_flavour_propagator_matrix()` | quantitative (reg) (row read: machine (off-diag $<10^{-12}$)) |

**Inputs → outputs:** $(\Lambda,G\Lambda^2,m_0)=(0.6515,2.10,0.0055)$ **re-typed literals** (`L214-216`), $N_c=3,N_f=2$ → $M$, $f_\pi$, GT residual, $g_{\sigma qq}$, ratio sweep over $G\Lambda^2\in\{1.8,2.1,3,5,10\}$, propagator off-diagonal (`L171 check_composite_scalar_fermion_coupling()`).  **Depends on:** `casim.numerics.xp`.  **Flags:** the NJL triple is typed as literals equal to registered `Lambda_NJL_GeV`, `G_Lambda2_NJL`, `m0_current_quark_MeV` (external/fitted, F77/F116) instead of imported (D7 rogue-literal pattern); docstring advertises `g_sigma_qq(M, G, Lam)` but the function takes `(M, Lam)`; docstring says the scalar ratio varies "by a factor of >6", leg text says ">5x", the check asserts relative spread $>0.5$. Species-locality leg asserts $\Pi_{ab}=0$ rather than computing it (docstring says so). Own `_results_dir()` duplicates `_results_path`.

---

### `engine/particles/derive_delta_cp_t2g.py` — F254's $T_{2g}$ no-go inherited by $\delta_{CP}$ (F353)
**Status:** live · standalone · **Findings:** F353 F92 F236 F254 · **Lattice:** n/a · **Law:** n/a · **Units:** dimensionless (F236 reference masses)

**Does:** shows $D_{2h}$ acts on complex $t_{ab}$ by a real sign only, and that the Jarlskog invariant is generic once $T_{2g}$ amplitudes carry phases; characterises two old Takagi defects (T5, T6).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $(STS^T)_{ab}=s_as_b\,t_{ab}$, $S=\mathrm{diag}(\pm1,\pm1,\pm1)$ | phase shift only $0$ or $\pi$ | `derive_delta_cp_t2g.py:L115-123 check_complex_amplitude_transport()` | machine (random draws, tol $10^{-10}$) (reg: exact; row is weaker — see flags) |
| 2 | $m_\nu=\mathrm{diag}(M_D^2/M_R)+s\begin{pmatrix}0&t_{xy}&t_{zx}\\t_{xy}&0&t_{yz}\\t_{zx}&t_{yz}&0\end{pmatrix}$, $s=\overline{\lvert\mathrm{diag}\rvert}$ | complex light-mass matrix | `L149-153 _mnu_complex()` | — |
| 3 | $J=\mathrm{Im}(U_{e1}U_{\mu2}U^*_{e2}U^*_{\mu1})$ via `majorana.takagi_light_masses` + `sin_delta_cp` | CP invariant | `L162-163, L179-180` | quantitative (reg: exact; row is weaker — see flags) |
| 4 | real fit point ⇒ $\lvert J\rvert<10^{-8}$; random phases ⇒ std$(J)>10^{-3}$, frac$(J{=}0)<1\%$ | baseline & phase-freedom scans | `L156 check_baseline_real_is_CP_conserving()`, `L168 scan_phase_freedom()`, `L191 check_democratic_phase_unprotected()` | quantitative (reg: exact; row is weaker — see flags) |
| 5 | pre-fix: `allclose(imag,0)` at atol $10^{-8}$ → real branch; raw `eigh`$(m^\dagger m)$ ⇒ $J_\text{raw}=-J_\text{fixed}$ | T5/T6 defect reproduction | `L218-233 _pre_fix_takagi()`, `L246, L270` | machine (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** F254 fit point from `derive_t2g_pmns.fit_full()` (Gauss–Newton fit, seed 3) → $J$ statistics.  **Depends on:** `particles.majorana` (06b), `derive_t2g_pmns` (below).  **Flags:** chiral/complex hazard is the subject: T5 (default `allclose` tolerance silently dropping the imaginary part at $m_\nu\sim10^{-9}$) is exactly the "numpy drops the imaginary component" hazard; the fix lives in `majorana.py`, not here (docstring "both fixed here" is loose). Registry `exact` vs module content (random/statistical scans) — tension. The baseline point is itself a 4-parameter fit.

---

### `engine/particles/derive_generation_identification_gap.py` — gauge-charge criterion cannot select $T_{1u}$ (F342)
**Status:** live · standalone · **Findings:** F342 F75 F292 F324 F27 F38 · **Lattice:** BCC nearest-neighbour shell $(\pm1,\pm1,\pm1)$ · **Law:** n/a · **Units:** n/a (exact `Fraction`)

**Does:** shows a site-diagonal $O_h$-invariant charge is forced to a multiple of identity (the shell is one orbit), so "identical gauge quantum numbers" gives no selecting power between $T_{1u}$ and $T_{2g}$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $O=\langle R_z,R_x\rangle$ (24), $O_h=\langle R_z,R_x,-1\rangle$ (48) | group closure | `derive_generation_identification_gap.py:L51-61 _close_group()`, `L168-171` | exact (reg) |
| 2 | number of orbits of $G$ on the 8 vertices; $=1$ ⇔ diagonal invariant $Q\propto1$ | transitivity | `L177-200` | exact (reg) |
| 3 | $M_{v}=v$ (T$_{1u}$), $N_v=(v_yv_z,v_zv_x,v_xv_y)$ (T$_{2g}$); $M^TM=N^TN=8I_3$, $M^TN=0$ | equivariant embeddings | `L203-209` | exact (reg) |
| 4 | $\Pi_{T_{1u}}=\tfrac18MM^T$, $\Pi_{T_{2g}}=\tfrac18NN^T$, $\Pi_{A_{1g}}=\tfrac18\mathbf 1\mathbf 1^T$, $\Pi_{A_{2u}}=I-\Pi_{A_{1g}}-\Pi_{T_{1u}}-\Pi_{T_{2g}}$; ranks $1,1,3,3$; idempotent, orthogonal, commuting | $A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}$ | `L211-238` | exact (reg) |
| 5 | $Q\Pi=\lambda\Pi$ on each triplet; site-diagonal $Q=qI_8\Rightarrow\lambda_{T_{1u}}=\lambda_{T_{2g}}$ | no selecting power | `L261-296` | exact (reg) |

**Inputs → outputs:** `charge_locality` ∈ {site_diagonal, block(control)}, `symmetry_group` ∈ {full_Oh, C4z_only(control)} → checks (`L152 check_generation_identification_gap()`).  **Depends on:** stdlib only.  **Flags:** none.

---

### `engine/particles/derive_generator_norm.py` — $E_g$ generator norm $R=1$ (F255; pre-decision framing)
**Status:** partial · entry-script · **Findings:** F118 (registry); F253/F255 per docstring · **Lattice:** $O_h$ axis-site shell (6 sites) for the Schur check · **Law:** n/a · **Units:** dimensionless ($\tau$ wall-pinned PDG √masses)

**Does:** (a) shows the Koide/F118 angle is the literal argument of the $E_g$ doublet (a genuine radian, $R=1$ by Schur isotropy) — **live, load-bearing (F255)**; (b) shows that deriving $\delta^*=2/9$ from $\lambda_6$ is circular — **framing superseded** by decision 7 (docstring banner `L2-25`, ledger S6-F253-weight-as-phase).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $s_a=\sqrt{m_a}$ (τ,μ,e), $p_a=s_a-\bar s$, $e=\lVert p\rVert$ | deviation vector | `derive_generator_norm.py:L58-61` | unknown (inferred: exact (PDG inputs)) |
| 2 | $p\cdot(1,1,1)/\lVert p\rVert\approx0$ | $p$ lies in the $E_g$ plane | `L67` | machine ($2.3\times10^{-16}$, inventory #278) |
| 3 | $\delta_\text{geom}=\operatorname{atan2}(p\cdot u_2,p\cdot u_1)$, $u_1\propto(2,-1,-1)$, $u_2\perp u_1$ in plane; folded mod $2\pi/3$ then to $[0,\pi/3]$ | geometric $E_g$ phase | `L69-75, L84` | unknown (inferred: machine) |
| 4 | $\delta_\text{Koide}=\operatorname{atan2}(-S,C)\bmod\tfrac{2\pi}3$, $C=\sum c_a\cos\tfrac{2\pi a}3$, $S=\sum c_a\sin\tfrac{2\pi a}3$, $c_a=s_a/\bar s-1$ | circulant phase | `L78-83` | unknown (inferred: machine) |
| 5 | $D(g)$ on $E_g$ basis $u\propto2z^2-x^2-y^2$, $w\propto x^2-y^2$ for $C_3^{[111]},C_4^z,C_2^x$; $\max\lVert D^TD-I\rVert$ | Schur isotropy ⇒ $R=1$ forced | `L109-129 eg_doublet_reps()` | unknown (inferred: machine (F255 (a))) |
| 6 | $C_\text{req}=\lvert B\rvert/(2\cos3\delta^*)$, $B=$`B_sea_cubic` | F234 back-solve | `L144-148` | unknown (inferred: quantitative) |
| 7 | $e^6_\text{implied}=C_\text{req}/\lambda_6$ with $\lambda_6=$ **registry `lambda_6`** (0.243) | amplitude implied by imported $\lambda_6$ | `L150-152` | unknown (inferred: quantitative) |
| 8 | $\delta(\lambda_6)=\tfrac13\arccos(-B/(2\lambda_6e^6))$ at $\lambda_6\in\{\tfrac14,\ 0.243\}$ | route-(I) forward map | `L155-161 delta_from_lambda6()` | unknown (inferred: quantitative) |

**Inputs → outputs:** PDG lepton masses; constants `B_sea_cubic` $=-5.69\times10^{-2}$ (quantitative, F95), `delta_star_f`, **`lambda_6`** → dict `R` (JSON written only under `__main__`).  **Depends on:** numpy, sympy (imported, unused).  **Flags:** **λ₆ used as an input** — `L51, L150, L161` import the registry value and use it to back out $e$ and to run the dynamical minimiser; this contradicts the constants registry's own Site note for this file (`constants/lepton.py:L128-132`: `lam6_F234` "COMPUTED from the F234 arrow … Recorded, never substituted: … importing the answer would make it circular") ⚠ DOC/CODE MISMATCH. The VERDICT text (`L194-208`, "E1 does not close", "derive λ₆ independently") is SUPERSEDED framing (decision 7 / F256), as the banner says. Module executes and prints at import (`L102, L139, L177, L220` are outside `__main__`). `r_ratio` comment (`L87`) is an unfinished note.

---

### `engine/particles/derive_higgs_bhl_compositeness.py` — BHL top-condensation from the model cutoff (F352)
**Status:** live · standalone · **Findings:** F352 F73 F74 F77 F107 · **Lattice:** n/a · **Law:** n/a · **Units:** GeV (SI-scaled via $a/\ell_P$)

**Does:** RG-runs the 1-loop SM $(y_t,\lambda)$ system down from the compositeness condition at $\Lambda_\text{model}$ to $m_t$ and reads off $m_t$, $m_H$ (quantified negative result).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Lambda_\text{model}=E_P/(a/\ell_P)$, $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$, $E_P=1.220890\times10^{19}$ GeV | compositeness scale ($1.850\times10^{18}$ GeV) | `derive_higgs_bhl_compositeness.py:L112, L117` | quantitative (reg) (row read: exact prefactor) |
| 2 | $g_2=\sqrt{e^2/s_W^2}$, $g_1=\sqrt{5/3}\sqrt{e^2/c_W^2}$, $g_3=\sqrt{4\pi\alpha_s}$ at $m_Z$ | gauge inputs (PDG) | `L136-141 gauge_couplings_at_mZ()` | external |
| 3 | $g^{-2}(\mu)=g^{-2}(\mu_0)-\tfrac b{8\pi^2}\ln\tfrac\mu{\mu_0}$, $b=(\tfrac{41}6,-\tfrac{19}6,-7)$ | 1-loop gauge running | `L123, L130-131 _g_running()` | quantitative (reg) (row read: exact (1-loop)) |
| 4 | $16\pi^2\dot y_t=y_t(\tfrac92y_t^2-8g_3^2-\tfrac94g_2^2-\tfrac{17}{12}g_1^2)$ | top Yukawa RGE | `L161-162 _rhs()` | quantitative (reg) (row read: exact (1-loop form)) |
| 5 | $16\pi^2\dot\lambda=24\lambda^2+12\lambda y_t^2-6y_t^4-9\lambda g_2^2-3\lambda g_1^2+\tfrac98g_2^4+\tfrac34g_1^2g_2^2+\tfrac38g_1^4$ | quartic RGE | `L163-166 _rhs()` | quantitative (reg) (row read: exact (1-loop form)) |
| 6 | BC at $\Lambda$: $y_t=Y_0$, $\lambda=Y_0^2/2$; fixed-step RK4 in $t=\ln\mu$ ($2\times10^5$ steps) | compositeness condition | `L176-185 run_down_from_Lambda()` | quantitative (reg) |
| 7 | $m_t=y_tv/\sqrt2$, $m_H=\sqrt{2\lambda}\,v$, $v=246.22$ GeV | pole-mass readout | `L191-192 predict_masses()` | quantitative (reg) |
| 8 | $Y_0\in\{50,100,300\}$ spread $<0.1\%$; Λ sweep | convergence & plateau | `L221-243 run_all()` | quantitative (reg) |

**Inputs → outputs:** PDG literals (`L101-108`) + `a_over_ellP` (F79/F107) → $m_t$, $m_H$, ratio vs F77 ceiling $2m_t$ (`L253 check_bhl_compositeness_prediction()`).  **Depends on:** stdlib only.  **Flags:** $\Lambda_\text{model}=E_P/(a/\ell_P)$ differs by exactly $\sqrt{8\pi}$ from `derive_M_R_scale_link`'s $\Lambda=3^{-1/4}M_\text{Pl}$ (both cite F107) — the two cutoffs are inconsistent (reduced vs non-reduced Planck mass); not settled here. The λ BC $\lambda=y_t^2/2$ is stated as "the same $m_H=2m_t$ ceiling" — with $m_H=\sqrt{2\lambda}v$, $m_t=y_tv/\sqrt2$ this gives $m_H/m_t=\sqrt2\cdot\sqrt2=2$ ✓.

---

### `engine/particles/derive_lambda6_sextic.py` — "derive λ₆" is misposed; λ₆ as output of δ* (F256)
**Status:** partial · entry-script · **Findings:** (registry: none; F256 per inventory #279, F234/F95/F118/F150 per docstring) · **Lattice:** n/a · **Law:** n/a · **Units:** dimensionless ($\tau$ wall-pinned, $y_\tau=1$)

**Does:** compares route (I) dynamical Landau minimiser $\cos3\delta=-B/2C$ with route (II) weight-as-phase $\delta^*=2/9$ primary, and computes $\lambda_6$ as the **output** of (II).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $m=(m_\tau,m_\mu,m_e)/m_\tau$, $s=\sqrt m$, $\bar y=\bar s$; $Q=\sum m/(\sum s)^2$ | PDG Koide ratio | `derive_lambda6_sextic.py:L37-40` | unknown (inferred: quantitative (data)) |
| 2 | circulant $\delta$ as in generator_norm #4 (folded to $[0,\pi/3]$); $\lvert3\delta-Q\rvert=2.84\times10^{-5}$, $\lvert\cos3\delta-\cos Q\rvert=1.76\times10^{-5}$ | data angle vs $Q$ | `L42-50` | unknown (inferred: quantitative) |
| 3 | $A=\sqrt2\,\bar y$, $e=\sqrt3\,\bar y$ ($=0.7279$) | amplitudes from PDG $\bar y$ | `L63` | unknown (inferred: quantitative) |
| 4 | $\lambda_6^{F118}=C_{F118}/e^6$, $C_{F118}=0.0362$ (literal) | legacy value | `L66-67` | fit (inherits F118) |
| 5 | $C_\text{req}=\lvert B\rvert/(2\cos Q)$, $\lambda_6^\text{req}=C_\text{req}/e^6$ | route (I): λ₆ making $3\delta=Q$ | `L80-81` | unknown (inferred: quantitative) |
| 6 | $\delta(\lambda_6)=\tfrac13\arccos\big(-B/(2\lambda_6e^6)\big)$; $d(3\delta)/d\lambda_6$ by central FD | route (I) sensitivity ($5.22$) | `L83-85, L111-113` | unknown (inferred: quantitative) |
| 7 | $\boxed{\lambda_6=\lvert B\rvert/\big(2e^6\cos(3\delta^*)\big)}$, $3\delta^*=\tfrac23$ exact | **F234 arrow: λ₆ as OUTPUT** ($=0.24333$) | `L132-133` | unknown (inferred: quantitative (inherits $B$, $e$)) |

**Inputs → outputs:** PDG lepton masses, `B_sea_cubic` (F95), `delta_star` (Fraction 2/9), `c_fierz_colour_f` (2/9, F145, only as a candidate λ₆) → dict `R`, JSON only under `__main__`.  **Depends on:** numpy, sympy.  **Flags:** the arrow is computed with $e=\sqrt3\,\bar y_\text{PDG}=0.7279$, giving $\lambda_6=0.2433$; the constants registry's derivation string for `lambda_6` cites $e\approx0.733$ (`e_saturation`), and $\lvert B\rvert/(2e^6\cos\tfrac23)$ at $e=0.733$ is $0.2334$ (4% below the registered 0.243, outside tol $5\times10^{-3}$) — ⚠ DOC/CODE MISMATCH between registry derivation and code. Route (I) treats λ₆ as an input (candidates 2/9, 1/4, $\lambda_6^\text{req}$) — deliberately, as the refuted alternative; route (II) is the adopted one. Text "1.7e-5 near-coincidence of 3δ=Q" (`L121`, `L171`) is the $\cos$ residual; the code's $\lvert3\delta-Q\rvert$ is $2.84\times10^{-5}$. Whole script executes and prints at import (`L53, L73, L98, L125, L197-198`), outside `__main__`.

---

### `engine/particles/derive_lepton_frame_fork.py` — $E_g$-diagonal vs [111]-circulant lepton frame (F406)
**Status:** live · standalone · **Findings:** F406 F403 F118 F95 F93 F175 · **Lattice:** BCC (sea leg K2 via `lattice.bcc.bcc_unitary`, both helicity branches) · **Law:** chiral branches $\pm$ summed (generation-blind); control makes one generation hop the opposite branch · **Units:** dimensionless ($\mu=1$; sea: $y_\tau=1$)

**Does:** decides the charged-lepton frame fork: F118/Dirac sea are spectral (tie); the $O_h\times T$ crystal-field kernel invariants decide; the [111] circulant has three inequivalent branches.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\lambda_n=1+\sqrt2\cos(\delta^*+2\pi n/3)$, $n=0,1,2\leftrightarrow\tau,e,\mu$; $\delta^*=\tfrac29$ (sympy Rational) | Koide spectrum, $\eta^2=\tfrac12$ | `derive_lepton_frame_fork.py:L71, L77-78 _lam_sym()` | quantitative (reg) (row read: exact) |
| 2 | $Y_b=F\,\mathrm{diag}(\lambda)F^\dagger$, $F_{ak}=\omega^{ak}/\sqrt3$ | trimaximal picture | `L85-86, L385` | quantitative (reg) (row read: exact) |
| 3 | $Y(\phi)=a\mathbb 1+r(e^{i\phi}P+e^{-i\phi}P^T)$, $a=\bar\lambda$, $r=\sqrt{\sum(\lambda-a)^2/6}$; branches $\phi=\delta^*+j\tfrac{2\pi}3$, $j\in\{0,1,-1\}$ | three circulant branches b1/b2/b3 | `L99-113 circulant_num(), branch_num()` | quantitative (reg) (row read: exact) |
| 4 | $\mathrm{Tr}(F\Lambda F^\dagger)^k=\sum\lambda^k$, $k\le6$ | F118 is spectral ⇒ (a)=(b) tie | `L393-397` (K1) | exact (inventory #244) |
| 5 | $D_k=\begin{pmatrix}N\otimes A_k&iM\otimes1\\iM\otimes1&N\otimes A_k^\dagger\end{pmatrix}$, $M=V\,\mathrm{diag}(y^2)V^\dagger$ ($y/y_\max$), $N=V\,\mathrm{diag}\sqrt{1-y^4}\,V^\dagger$; $E_\text{sea}=-\sum_{s=\pm}\sum_k\sum\lvert\arg\mathrm{eig}D_k\rvert/(2L^3)$ | 3-generation BCC Dirac sea (F46/F95) | `L206-237 sea_energy()` | quantitative (reg) (row read: machine) |
| 6 | $E_\text{sea}(Y_a)=E_\text{sea}(\text{any }UY_aU^\dagger)=4\sum_a f(y_a^2)$ | generation covariance = 4× F95 per-axis | `L410-419` (K2) | machine ($<10^{-12}$, inventory #87) |
| 7 | $b=(Y_b)_{01}=\tfrac{\sqrt2}2e^{i\cdot2/9}$; $(1,1,1)$ carries $a+2\mathrm{Re}\,b=\lambda_j$ (τ on b1, e on b2, μ on b3); $I_\text{T1g}=\tfrac32\sin^2(\delta^*+j\tfrac{2\pi}3)$ | branch identification | `L422-434` (K3) | quantitative (reg) (row read: exact) |
| 8 | kernel invariants $R=\sum(\mathrm{Re}Y_{ab})^2$, $I=\sum(\mathrm{Im}Y_{ab})^2$, $\sum d_cx^2$, $\sum d_cy^2$, $x_{12}x_{23}x_{13}$, $\mathrm{Re}(Y_{12}Y_{23}Y_{31})-x_{12}x_{23}x_{13}$ | $O_h\times T$ invariants vanishing on diagonal $Y$ | `L120-135 kernel_invariants()` | quantitative (reg) (row read: exact) |
| 9 | Molien: $\tfrac1{\lvert G\rvert}\sum_A\exp\sum_k\mathrm{tr}(A^k)t^k/k$; counts $\{1,4,9\}$, kernel $\{0,2,6\}$ | invariant counting | `L175-191 molien_counts()` (K7 `L487-495`) | quantitative (reg) (row read: exact) |
| 10 | $\alpha R+\beta I$ with $R+I\le D=\tfrac12\sum(\lambda-\bar\lambda)^2$, $I\le I_\max=((\lambda_\max-\lambda_\min)/2)^2$: (a) $\alpha,\beta>0$; real texture $\alpha<\min(0,\beta)$; b3 $\beta<\alpha<0$; $T_{1g}$ block $\beta<0<\alpha$ | quadratic phase diagram | `L293-309 quadratic_phase()` (K8 `L498-528`) | quantitative (reg) (row read: exact (bounds) + sampled) |
| 11 | TM1 column $(\tfrac23,\tfrac16,\tfrac16)$ viable only on b2 | fixed-assignment PMNS | `L241-289, L437-450` (K4) | quantitative (reg) |
| 12 | $\arctan(T_{1g}/T_{2g})=\{\delta^*,\ \tfrac\pi3-\delta^*,\ \tfrac\pi3+\delta^*\}$ | axial/polar angle per branch | `L453-458` (K5) | quantitative (reg) (row read: exact) |
| 13 | stabilisers $\lvert\text{Stab}(Y_a)\rvert=8$, $\lvert\text{Stab}(Y_b)\rvert=12$; gradient of random invariant $\approx0$ on both | Michel criticality | `L461-484` (K6) | quantitative (reg) (row read: machine) |
| 14 | $E(b)-E(a)$ with F118 terms on diagonal entries; $\alpha=\beta=-\kappa_E$ | F118 per-axis reading (K1b) | `L341-367 f118_per_axis_fork()` | quantitative (reg) |

**Inputs → outputs:** `delta_star` (Fraction), NuFIT box from `derive_oh_residual_pmns`, F118 fit point $(v,c)=(0.16,1.10)$ (`L338`, fitted in F118) → checks K1–K9, verdict "a" (`L371 check_lepton_frame_fork()`).  **Depends on:** `lattice.bcc` (03), `particles.eg_sextic._bz_omegas/_f_of_m` (06b), `derive_oh_residual_pmns` (below).  **Flags:** `f118_per_axis_fork` `exec`s the source of a **test file** (`tests/findings/test_F118_self_consistent_Wvc_and_C.py`, sliced at `def constrained_H2`, `L349-358`) — an engine module depending on test code; K1b rests on F118's fitted $(v,c)$. Complex eigenvalues of $D_k$ via `xp.linalg.eigvals` on complex128 (no real/imag split risk). RNG is `xp.random.default_rng`, not `casim.numerics.rng`. K9 is prior-dependent (docstring says "indicative").

---

### `engine/particles/derive_lepton_shape_precision_floor.py` — shape residual is m_τ-precision limited (F348)
**Status:** live · standalone · **Findings:** F348 F175 F92 F174b F76 F256 · **Lattice:** n/a · **Law:** n/a · **Units:** MeV / dimensionless ratios

**Does:** evaluates the zero-parameter $\{\delta^*,\eta^2\}=\{\tfrac29,\tfrac12\}$ shape against PDG, shows a single $(\delta,\eta^2)$ offset explains both residuals, and gives the $m_\tau$ precision needed for 3σ/5σ.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $v_a=(1+2\sqrt{\eta^2}\cos(\delta+2\pi a/3))^2$ sorted; $(r_\mu,r_\tau)=(v_1/v_0,v_2/v_0)$ | circulant mass ratios | `derive_lepton_shape_precision_floor.py:L73-76 _lepton_ratios()` | quantitative (reg) (row read: exact) |
| 2 | pct errors at $(\tfrac29,\tfrac12)$: $+0.00098\%$ ($\mu$), $+0.00703\%$ ($\tau$) | F175 D4 reproduction | `L92-96 run_all()` | quantitative (reg) |
| 3 | $\Delta m_\tau=(r_\tau^\text{ex}-r_\tau^\text{PDG})m_e$, $/0.12$ MeV $=1.04\sigma$ | residual in σ | `L100-101` | quantitative (reg) |
| 4 | $\partial(r_\mu,r_\tau)/\partial(\delta,\eta^2)$ forward FD, $h=10^{-7}$; linear $\Delta r=J\cdot(\delta_\text{fit}-\tfrac29,\ \eta^2_\text{fit}-\tfrac12)$ | one joint offset | `L79-87 _jacobian()`, `L111-119` | quantitative (reg) |
| 5 | $\sigma_\text{needed}=\lvert\Delta m_\tau\rvert/n$, improvement $=0.12/\sigma_\text{needed}$, $n\in\{2,3,5\}$ | re-attack thresholds | `L131-136` | quantitative (reg) |

**Inputs → outputs:** `delta_star_f` (2/9, F175) — **primary, no λ₆ anywhere**; `ETA2_STAR = 0.5` literal (F92); F174 fit values $(0.222229, 0.4999908)$ as literals → verdict record (`L142 check_lepton_shape_residual_is_precision_floor_limited()`).  **Depends on:** stdlib.  **Flags:** $\eta^2=\tfrac12$ (a derived exact constant, F92) is a local literal — not a registered constant. Consistent with decision 7.

---

### `engine/particles/derive_oh_residual_pmns.py` — no $O_h$ residual symmetry fixes PMNS (F403)
**Status:** live · standalone · **Findings:** F403 F254 F236 F93 F76 F75 · **Lattice:** BCC point group $O_h$ on $T_{1u}$ (S4 checks the [111] NN Gram) · **Law:** n/a · **Units:** n/a

**Does:** enumerates every rotation/subgroup of $O_h$, maps its 1-dim eigenlines through the charged-lepton frame to PMNS columns, and compares with NuFIT 6.0 (3σ); gCP residuals via symbolic algebra.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $O$ = det$+1$ signed permutations (24); $O_h=O\cup(-O)$; classes by (trace, off-diagonal) | group & classes | `derive_oh_residual_pmns.py:L77-105` | quantitative (reg) (row read: exact) |
| 2 | frames: cube $=I$; face $=\tfrac1{\sqrt2}\begin{pmatrix}1&1&0\\1&-1&0\\0&0&\sqrt2\end{pmatrix}$; trimaximal $F_{ak}=\omega^{ak}/\sqrt3$ | charged-lepton frames | `L119-127 _frame()` | quantitative (reg) (row read: exact) |
| 3 | $\lvert U_c^\dagger v\rvert^2$ for 1-dim eigenlines $v$ of $R$ | PMNS column moduli | `L108-116, L130-133` | quantitative (reg) (row read: exact (sympy)) |
| 4 | standard parametrisation, $\lvert U_{\mu1,2}\rvert^2=a^2+b^2\pm2ab\cos\delta$ over the box | data viability | `L153-197 _column_viable()`, `L200-235` | quantitative (reg) |
| 5 | closure of $O_h$ subgroups (98; 30 in $O$); invariant symmetric $M$ with $g^TMg=M$; non-degenerate iff discriminant $\not\equiv0$ ⇔ elementary abelian 2 (49) | subgroup lattice | `L240-330` | exact (inventory #242) |
| 6 | trimaximal frame: $C_2'$ ⇒ TM1 $(\tfrac23,\tfrac16,\tfrac16)$, $C_2$ ⇒ TM2 $(\tfrac13,\tfrac13,\tfrac13)$ | picture (b) columns | `L451-460` (B1) | exact (inventory #239) |
| 7 | $s_{12}^2=1-\tfrac2{3c_{13}^2}$ | TM1 sum rule | `L473-474` (B3) | quantitative (reg) (row read: exact) |
| 8 | $\cos\delta=-\dfrac{(s_{12}^2-c_{12}^2s_{13}^2)\cos2\theta_{23}}{2s_{12}c_{12}s_{13}\sin2\theta_{23}}$ | TM1 $(\theta_{23},\delta)$ correlation | `L493-495, L504-505` (B4) | quantitative (reg) (row read: exact identity + scan) |
| 9 | diagonal gCP $X$ ⇒ $Q^*=Q$ ⇒ $J=0$; $\mu\tau$ mirror ⇒ $\theta_{23}=\pi/4$, $\lvert U_{\mu1}\rvert^2-\lvert U_{\tau1}\rvert^2=\sin2\theta_{12}\sin\theta_{13}\cos\delta$ | gCP residuals | `L579-607` (C1) | exact (inventory #240) |
| 10 | BCC [111] Gram off-diagonal $=-\tfrac13$ | no orthonormal [111] frame | `L564-566` (S4) | quantitative (reg) (row read: exact) |

**Inputs → outputs:** NuFIT 6.0 NO 3σ box (`L61-67`), JUNO-inclusive $s_{12}^2$ band as a Gaussian ×3 extrapolation (`L70`, labelled approx) → checks (`L367 check_oh_residual_pmns()`).  **Depends on:** sympy, stdlib.  **Flags:** none (data comparison clearly separated from exact group theory).

---

### `engine/particles/derive_quark_B_colour_charge.py` — colour/charge dressing of F95's $B$ is k-blind (F405)
**Status:** live · standalone · **Findings:** F405 F95 F80 F92 F346 F347 · **Lattice:** BCC sea in L2/L3 (`lattice.bcc.bcc_dispersion`, both branches averaged) · **Law:** branch-averaged · **Units:** MeV / dimensionless

**Does:** proves Koide $Q$ depends only on $k$, that $B\propto k^3$, and that any generation-uniform colour/charge dressing cannot move $k$ to the quark values; probes loopholes.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $y_a=\bar y+A\cos(\delta+2\pi a/3)$, $A=\sqrt2k\bar y$: $\sum y=3\bar y$, $\sum y^2=3\bar y^2+\tfrac32A^2$, $Q=(1+k^2)/3$, $\partial_\delta Q=0$ | Q is δ- and B-blind | `derive_quark_B_colour_charge.py:L213-224` (E1) | exact (inventory #243) |
| 2 | $[\cos3\delta]\sum y^4=3\bar yA^3$ ⇒ $B(k)=k^3B(1)$ | B scaling | `L227-232` (E2) | quantitative (reg) (row read: exact) |
| 3 | $k^2_\text{req}=3Q-1$ per sector/scheme | required quark $k^2$ (1.546 up, 1.194 down) | `L236-244` (K1) | quantitative (reg) |
| 4 | $B_q=N_c k_q^3B_\text{sea}$ | dressed $B$ at common $\bar y$ | `L248-249` | quantitative (reg) |
| 5 | $Q(\lambda_am_a)-Q(m_a)\equiv0$ for $\lambda_a=1+gC_FQ_f^2$ uniform in $a$ | identity-class dressing | `L257-263` (U1) | quantitative (reg) (row read: exact) |
| 6 | $\gamma_m=6C_F\alpha_s/4\pi+3Q_f^2\alpha/2\pi$; $m\to me^{-\gamma\ell}$ leaves $Q$ | mass-independent running | `L271-278` (U2) | quantitative (reg) (row read: exact (by construction)) |
| 7 | $S_4/R^4=\tfrac{c^4}3+2c^2s^2+\tfrac{s^4}2+\tfrac{2\sqrt2}3cs^3\cos3\delta$ on $\sum y^2=R^2$; $E=-g\,S_4$; $k^2=\tan^2\phi_\min$ | LO loop $k$-preference (1.896 at δ*) | `L144-160 _S4_circle(), loop_k2_preference()` | quantitative (reg) |
| 8 | $f(m)=-\tfrac12\sum_\pm\langle\arccos(\sqrt{1-m^2}\cos\omega_\pm(\mathbf k))\rangle$ | nonperturbative BCC sea (F95) | `L163-185 loop_k2_nonperturbative()` | quantitative (reg) |
| 9 | $E=K(k^2-1)^2+gR^4V$ linear response; needed $(gR^4)_q/(gR^4)_l=\Delta k^2_q/\text{bound}_l\cdot V'(\delta_l)/V'(\delta_q)$ | finite-stiffness selector | `L314-330` (S1) | quantitative (reg) |
| 10 | $p$: $Q(m^p)=\tfrac23$ (bisection); $\epsilon=1/p-1$; $\epsilon_U/\epsilon_D$ MC | power-law loophole (3.88 vs $Q_u^2/Q_d^2=4$) | `L118-141, L334-364` (P1) | quantitative (reg) |

**Inputs → outputs:** PDG 2025 "mixed" and $M_Z$ quark masses (`L76-87`), `B_sea_cubic`, `delta_star_f`, $N_c=3$, $C_F=\tfrac43$ → checks (`L192 check_quark_B_colour_charge()`).  **Depends on:** `lattice.bcc.bcc_dispersion` (03), `casim.numerics.rng/xp`.  **Flags:** in S1 the variable `k2l = 3Q-2` (`L318`) is $k^2-1$ (dict key says so; name misleading). m_τ literal here is 1776.93 (PDG 2024) vs 1776.86 in the other lepton-shape modules. λ₆ not used.

---

### `engine/particles/derive_quark_mixed_koide_probe.py` — mixed-type quark Koide tuples (F347)
**Status:** live · standalone · **Findings:** F347 F346 F80 F92 F121 F123 F175 · **Lattice:** n/a · **Law:** n/a · **Units:** MeV

**Does:** fits the circulant to $(u,d,s)$ and $(c,b,t)$, checks $Q\approx\tfrac23$, phase vs single-irrep $O_h$ weights, and $\eta^2$ vs the lepton value.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\sqrt{m_a}=\mu(1+\eta\cos(\delta+2\pi a/3))$: $\mu=\tfrac13\sum y$, $\eta e^{i\delta}=\tfrac2{3\mu}\sum_ay_a\omega^{-a}$ | exact circulant inversion (DFT) | `derive_quark_mixed_koide_probe.py:L116-124 fit_circulant()` | quantitative (reg) (row read: exact) |
| 2 | $Q=\tfrac13+\tfrac{\eta^2}6$ | Q–η identity | `L148-149` | quantitative (reg) (row read: exact (check tol $10^{-9}$)) |
| 3 | MC σ of $\delta\bmod\tfrac{2\pi}3$ and $\eta^2$ | measurement precision | `L163-180 _mc_stats()` | quantitative (reg) |
| 4 | $P=\min(1,\,3\cdot2d/L)$, $L=2\pi/3$ | look-elsewhere (union bound) | `L187-190` | quantitative (reg) |
| 5 | $\lvert\eta^2-2\rvert$ in MC σ | $(c,b,t)$ amplitude vs lepton | `L238-249` (C4) | quantitative (reg) |

**Inputs → outputs:** PDG 2024 masses; candidate weights $\{\tfrac19,\delta^*=\tfrac29,\tfrac13\}$ → checks (`L295 check_quark_mixed_koide_probe_result()`).  **Depends on:** `casim.numerics.rng/xp`.  **Flags:** ⚠ DOC/CODE MISMATCH — docstring `L9` cites "F92's eta^2=1/2" but the code's lepton target is $\eta^2=2$ (`L104`; own docstring `L33` also says 2): two parametrisations of the same amplitude ($1+2\sqrt{\eta^2}\cos$ vs $1+\eta\cos$). `fit_circulant` is a verbatim copy of `derive_quark_shape_probe.fit_circulant`.

---

### `engine/particles/derive_quark_shape_probe.py` — lepton shape mechanism has no same-type quark face (F346)
**Status:** live · standalone · **Findings:** F346 F80 F92 F121 F123 F175 · **Lattice:** n/a · **Law:** n/a · **Units:** MeV

**Does:** exact circulant fit of up-type and down-type triplets; MC distance of $\delta$ to $\{\tfrac19,\tfrac29,\tfrac13\}$; look-elsewhere; lepton self-check.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | as mixed-probe #1 | circulant inversion | `derive_quark_shape_probe.py:L131-141 fit_circulant()` | quantitative (reg) (row read: exact) |
| 2 | $Q=\sum m/(\sum\sqrt m)^2$ | Koide ratio | `L149-151 koide_Q()` | quantitative (reg) (row read: exact) |
| 3 | MC std of $\delta\bmod\tfrac{2\pi}3$ | measurement σ | `L175-190 _mc_delta_mod_std()` | quantitative (reg) |
| 4 | $p=2(1-\Phi(\sigma))$; $P=\min(1,3\cdot2d/L)$ | tail / look-elsewhere | `L193-195, L244-249` | quantitative (reg) |
| 5 | lepton self-check: $\eta^2=1.99996$, $\delta\bmod\tfrac{2\pi}3=0.222230$ vs $\tfrac29$ | method validation | `L295-305 c5_lepton_selfcheck()` | quantitative (reg) |

**Inputs → outputs:** PDG 2024 masses and σ (`L96-103`), `delta_star_f` → checks (`L321 check_quark_shape_probe_leaning_null_result()`).  **Depends on:** `casim.numerics.rng/xp`.  **Flags:** ⚠ DOC/CODE MISMATCH — docstring `L18-20` writes the ansatz as $1+2\sqrt{\eta^2}\cos$ with "$\eta^2=1/2$ (F92)", but the fitted/checked ansatz is $1+\eta\cos$ (`L121, L140`) and C5 compares to $\eta^2=2$ (`L408-409`, leg text "eta^2=2"). Same physics, inconsistent symbol.

---

### `engine/particles/derive_t2g_pmns.py` — $T_{2g}$ PMNS amplitudes are genuinely free (F254)
**Status:** live · test-only · **Findings:** (registry: none; F254/F236 per docstring) · **Lattice:** n/a ($D_{2h}\subset O_h$ sign group) · **Law:** n/a · **Units:** F236 reference units ($M_D=(5\times10^{-4},0.1,1)$, $M_{R0}=10^{12}$)

**Does:** $D_{2h}$ character analysis of $(t_{xy},t_{yz},t_{zx})$ plus a numerical no-go for one-parameter symmetric ansätze against NuFIT-5.2.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\chi_{t_{ij}}(S)=s_is_j$ over the 8 sign matrices; each sums to 0, all distinct ⇒ $B_{1g},B_{2g},B_{3g}$ | inequivalent 1-d irreps | `derive_t2g_pmns.py:L78-84 t2g_characters()`, `L92-93 analyse_irreps()` | unknown (inferred: exact) |
| 2 | stabiliser of $(1,1,1)$ has order 2 | democracy unprotected | `L95-101` | unknown (inferred: exact) |
| 3 | $M_{R,a}=M_{R0}s_a^2$, $s_a=1+\sqrt2\cos(\delta_\nu+2\pi a/3)$; $m_{\nu,a}=M_{D,a}^2/M_{R,a}$ | E_g texture light masses (F47 seesaw) | `L117-121 _light_diag()` | unknown (inferred: exact) |
| 4 | $m_\nu=\mathrm{diag}+\bar m\,T$, $T$ off-diagonal $(t_{xy},t_{yz},t_{zx})$ | light mass matrix | `L135-137 _mnu()` | — |
| 5 | angles via `majorana.takagi_light_masses` / `pmns_angles`; cost $\sum(\theta-\theta_\text{NuFIT})^2$ | fit / scans | `L124-128, L140-171` | unknown (inferred: quantitative) |
| 6 | Gauss–Newton with line search on $(\delta_\nu,t_{xy},t_{yz},t_{zx})$, 25 restarts | full fit | `L174-212 fit_full()` | fit |

**Inputs → outputs:** NuFIT-5.2 central angles (`L56`) → irrep verdict, scan costs, full-fit residual (`L216 main()`).  **Depends on:** `particles.majorana` (06b).  **Flags:** ⚠ DOC/CODE MISMATCH — docstring (`L35-36`, `L236`) says the full fit has "exactly 3 inputs for 3 angles", but `fit_full` fits **4** parameters (δ_ν plus three $t$) to 3 angles (`L188-193, L207`). Docstring names the file `derive_t2g_pmns_selector.py`. Registry: no findings/exactness.

---

## Lepton-shape chain — what the code actually does with δ* and λ₆

| Module | δ* | λ₆ | Verdict vs decision 7 |
|---|---|---|---|
| `derive_lepton_shape_precision_floor` | primary (`delta_star_f`) | not used | consistent |
| `derive_lepton_frame_fork` | primary (sympy `Rational(2,9)`) | not used | consistent |
| `derive_lambda6_sextic` | primary (`delta_star`, route II) | **computed as output** $\lvert B\rvert/(2e^6\cos\tfrac23)=0.2433$ with $e=\sqrt3\bar y_\text{PDG}$ (`L132-133`); route (I) treats λ₆ as an input only as the refuted alternative | consistent; registry derivation string ($e\approx0.733$) does not reproduce 0.243 |
| `derive_generator_norm` | `delta_star_f` | **imported from the registry as an input** (`L150`) to back out $e$ and run route (I) | contradicts the registry Site note; framing superseded (banner) |
| `derive_M_R_scale_link` | scan sample | imported (scan sample $6\lambda_6$ only) | harmless |
| quark probes (F346/F347/F405) | comparison weight | not used | consistent |

No code path fits λ₆ to data as a primary parameter; the F179/CN3 fitted-angle route does not appear in these modules.
