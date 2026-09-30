# 05c — Gauge sector III: the photon, lattice perturbation theory (`lpt_*`), weak/Z, strong, links

*Written 2026-09-28 - 00:00 (part p05c). Code is the source of truth; every row cites `file.py:L<n> function()` at the line where the quantity is computed. Exactness defaults to the module registry's `exactness` field, overridden only where `docs/status/exactness-inventory.md` names the specific result; registry `None` → `unknown`.*

**Scope.** Twenty-four modules under `src/casim/engine/gauge/`: the canonical paired-spinor photon and its bound-state / packet / Pryce studies; the SU(2) $W_\mu$ kernel (`weak_wmu.py`, which holds `_f26_rotation_step`, the even rotation law); the Z neutral current; the 2-D weak reference; U(1)/SU(3) minimal coupling; the `lpt_*` chain (Wilson and BCC-rhombus lattice perturbation theory for the one-loop gluon self-energy and $d_1$); plus `link_hamiltonian`, `propagator`, `reflection_positivity`, `strong`, `su3_ladder`, and `rotation` (which is misfiled — it is Hartle frame dragging, an interactions/astrophysics module).

**Shared conventions.**
- *Lattice.* Spectral kernels store the field on a cubic $L^3$ array with $k\in$ `fftfreq`$\times2\pi$ (`lattice.geometry.make_kgrid_3d`), and evaluate the **BCC** Weyl-walk dispersion on it: $u^\pm(k)=c_xc_yc_z\pm s_xs_ys_z$ with $c_i=\cos(k_i/\sqrt3)$, $s_i=\sin(k_i/\sqrt3)$, $\omega^\pm=\arccos u^\pm$ (`lattice/bcc.py:L89 _bcc_uvec()`, `L122 bcc_dispersion()`; see 03-lattice.md § bcc.py). So "BCC" here means BCC *dispersion* on a cubic storage grid with hops $d/\sqrt3$, not a BCC site mask. The `lpt_*` modules use the 4-D hypercubic Wilson action (reference, D1) and, from F305 on, the genuine BCC rhombus action with integer $\langle111\rangle$ link axes.
- *Rotation law (F91).* Even law: $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$, applied as one real rotation $E\to\cos\Omega\,E+\sin\Omega\,B$, $B\to-\sin\Omega\,E+\cos\Omega\,B$, equivalently $F=E+iB\to e^{-i\Omega}F$. Used by the photon, hypercharge B, the Z, and the massive W. Chiral law (F37): $F^\pm=E\pm iB$ at $\Omega^\pm=2\omega^\pm(k/2)$, used by the **massless W** step.
- *Constants.* $c_\text{lat}=1/\sqrt3$ (`c_lat`, exact, F26 — see 01-constants.md). No other `casim.constants` symbol is used in this batch except `q_star_a_implied` (0.7327, quantitative, F151/F155), `G_CODATA`, `c_SI` (external). Many numbers the `lpt_*` modules use are typed literals, not registry constants: $Z_0=0.154933390231$, $28.8086$, $C_{\overline{MS}}=131/66$, $C_A=3$, $\theta_W=\pi/6$.
- *Units.* Lattice units (cells, ticks, $a=1$) throughout, except `rotation.py` (geometric km, converted to SI via `c_SI`, `G_CODATA`).
- *Hazards checked.* (i) No module in this batch applies the σ-bilinear construction to the photon; `photon.py` / `photon_packet.py` explicitly use the even pair law. (ii) The chiral W step (`w_propagation_step_chiral`) keeps real fields real: $F^-=\overline{F^+(-k)}$ and $\Omega^+(-k)=\Omega^-(k)$ except at Nyquist bins, which are forced to the even average; spot-checked energy drift $2\times10^{-16}$ at $L=8$. (iii) Superseded code is marked where it is mapped (the composite-SC plaquette, F265; the refold defect in `lpt_wilson_selfenergy`, F307/F308).

**Spot-checks run for this section** (PYTHONPATH=src, <1 s each): $\Omega_\text{pair}(h\hat n)/h\to0.5773502$ at $h=10^{-3}$ ($1/\sqrt3=0.5773503$); $\Omega_\text{pair}(1.3,0,0)-1.3/\sqrt3=-1.1\times10^{-16}$; $\Omega_\text{pair}(k)-\Omega_\text{pair}(-k)=0$; `photon_step_spectral` vs `_f26_rotation_step` agree to $8.9\times10^{-16}$; `z_couplings(π/6)` gives $e_R$: $(g_V,g_A)=(1/4,-1/4)$; `threshold_closed_form` vs `omega_even` at $k=(0.2,0.3,0.4)$: offset $0.0163$ vs leading-order $\lvert k_xk_yk_z\rvert/3\lvert k\rvert=0.0149$.

**Modules (path order):** link_hamiltonian · lpt_bcc_vertex · lpt_d1_action_consistent · lpt_d1_subtracted · lpt_selfenergy · lpt_vertex · lpt_ward · lpt_wilson · lpt_wilson_selfenergy · lpt_ws_mask_cutcell · minimal_coupling · photon · photon_bound_state · photon_bound_state_finite_k · photon_packet · photon_pryce_commutator · propagator · reflection_positivity · rotation · strong · su3_ladder · weak · weak_wmu · weak_z.

### `engine/gauge/link_hamiltonian.py` — real-time Kogut–Susskind link Hamiltonian, $\mathbb Z_N$ / U(1) (F110, F111)
**Status:** live · test-only · **Findings:** (registry: none; docstring F100 F101 F110 F111 F325) · **Lattice:** open square 2-D plaquette grid and open cubic 3-D graph (simple-cubic reference, D1 — not BCC) · **Law:** n/a (Hamiltonian, not rotation law) · **Units:** lattice ($g^2,\lambda$ dimensionless)

**Does:** builds $H=\tfrac{g^2}2\sum_\ell s(\hat E_\ell)^2-\tfrac\lambda2\sum_p(\Gamma_p+\Gamma_p^\dagger)$ with Gauss's law solved exactly (heights in 2-D, spanning-tree elimination in 3-D), evolves it in real time, and extracts static potentials / string tension.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $E_\ell=m_{p^+(\ell)}-m_{p^-(\ell)}+\eta_\ell$ (outer face $m=0$), $\mathrm{div}\,\mathrm{curl}\,m=0$ asserted | dual (height) Gauss solution | `link_hamiltonian.py:L164–169 curl_heights()`, `L234–247 link_E_values()` | unknown (inferred: exact (integer)) |
| 2 | $s(e)=((e+\lfloor N/2\rfloor)\bmod N)-\lfloor N/2\rfloor$ | $\mathbb Z_N$ symmetric residue | `L224 sym_residue()` | unknown (inferred: exact) |
| 3 | $H_{ii}=\tfrac{g^2}2\sum_\ell s(E_\ell)^2$; off-diagonal $-\lambda/2$ for $m_p\to m_p+1$ (cyclic mod $N$; U(1) truncated at $\lvert m\rvert\le m_\text{max}$) + h.c. | dual KS Hamiltonian | `L280–302 build_dual_hamiltonian()` | unknown (inferred: exact (sparse matrix)) |
| 4 | $E_0(\lambda{=}0)=\min\tfrac{g^2}2\sum s(E)^2$; straight string: $V(R)=\tfrac{g^2}2q^2R$ | strong-coupling potential | `L321–323 ground_energy_lambda0()` | exact (inventory F110-C2) |
| 5 | $\psi(t)=e^{-iHt}\psi_0$ (Krylov `expm_multiply`; dense eigh cross-check) | real-time evolution | `L340–346 evolve_krylov()`, `L353–356 evolve_dense()` | unknown (inferred: machine (per docstring, drift checked)) |
| 6 | $\langle s(E_\ell)^2\rangle$, $\langle\cos\hat\phi_p\rangle=\Re\langle\Gamma_p\rangle$ | observables | `L361–362`, `L377–388` | n/a |
| 7 | $V(R)=E_0(R)-E_0(0)$; LSQ $V=c+\sigma R$ | static potential, string tension | `L405–421 static_potential()`, `L427–432 fit_linear_potential()` | unknown (inferred: quantitative (eigensolver)) |
| 8 | $\sigma(\lambda)=\tfrac{g^2}2-c_2\lambda^2$, $c_2=\sum_{p,\pm}\tfrac14/\Delta E$ differenced $R{=}2$ vs $R{=}1$ | 2nd-order strong-coupling PT | `L443–466 sigma_strong_pt2()` | unknown (inferred: exact (rational arithmetic in floats)) |
| 9 | Gauss-sector direct link basis: keep states with $(\mathrm{div}\,e-q)\bmod N=0$; plaquette shifts $(+,+,-,-)$ | independent cross-check | `L490–535 build_direct_zn()` | unknown (inferred: exact (spectral identity, F110 C1)) |
| 10 | $H=\tfrac1{2\chi}\hat E^2-\lambda\cos\hat\phi$ (tridiagonal); $\sigma_1=-\ln\sum g_mg_{m+1}$ | F101 rotor contact; one plaquette ⇒ $\chi=1/(4g^2)$ | `L545–549 rotor_hamiltonian()`, `L554–557 rotor_sigma1()` | exact (inventory F110-C7 matrix identity) |
| 11 | $E_\text{tree}=M E_\text{off}+b(q)$, leaf-first elimination; plaquette cycles satisfy $c_\text{tree}=Mc_\text{off}$ (asserted); dim $=d^{\,n_\ell-n_s+1}$ | 3-D tree-gauge Gauss solution | `L703`, `L714`, `L727 LatticeGraph3D` | unknown (inferred: exact (integer)) |
| 12 | same $H$ in the off-tree basis | 3-D KS Hamiltonian | `L766–801 build_tree_hamiltonian()` | unknown (inferred: exact (matrix)) |
| 13 | streamed $\min\tfrac{g^2}2(\sum s(E_\text{off})^2+\sum s(E_\text{tree})^2)$ | 3-D $\lambda{=}0$ energy | `L885–893 tree_lambda0_min()` | unknown (inferred: exact) |

**Depends on:** numpy, `scipy.sparse`, `scipy.sparse.linalg.eigsh/expm_multiply` imported directly (not via `casim.numerics`, D8). **Flags:** abelian integer electric spectrum is a solvability choice, not the model's continuous $(E,B)$ (docstring L70–90, F325) — valid for the $k$-string sector at $N\le3$ only; registry lists no findings although inventory rows F110-C2/C7 rest on it.

### `engine/gauge/lpt_bcc_vertex.py` — Feynman rules of the genuine BCC rhombus gauge action (F305)
**Status:** live · standalone · **Findings:** F305 F265 F278 F162 F163 · **Lattice:** BCC link lattice (4 integer $\langle111\rangle$ axes + Euclidean time = 5 axes) and hypercubic Wilson ('sc') on one code path · **Law:** n/a (Euclidean action) · **Units:** lattice

**Does:** derives the 2- and 3-point vertices of any compact plaquette action from its loop words, and gates them.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | axes $D_i\in\{(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)\}\times\{0\}\cup\{\hat t\}$; $\hat n=(-1,1,1,1,0)/2$ with $\sum_i n_iD_i=0$ | geometry | `lpt_bcc_vertex.py:L89`, `L94` | exact (reg) |
| 2 | loops: 6 rhombi $(d_1,d_2)$ both senses + 4 temporal rhombi both senses (20) vs Wilson's 12 | loop words | `L134–153 _loops_bcc()`, `_loops_sc()` | exact (reg) |
| 3 | $V=\sum_tc_t\exp(i\sum_rk_r\cdot v_{t,r})$, $c_t=-\mathrm{Tr}$ of the ordered $e^{iA}$ expansion, factor $(\pm i)^{m}$ per slot, $1/m!$ orderings | n-point vertex from the action | `L198–207 terms()`; `L221–224 vertex3()`; `L232–234 vertex2()` | exact (reg) |
| 4 | $\hat k_i=2\sin(k\cdot D_i/2)$; $S(k)=\sum_i\hat k_i^2$ | hatted momentum, the action's own inverse propagator | `L246 khat()`, `L251 quadratic_form()` | exact (reg) |
| 5 | G1: $\Gamma_{ij}=\delta_{ij}S-\hat k_i\hat k_j$ with $K=1$ | two-point gate | `L297–306 gate_two_point()` | machine (tol 1e-12) (reg: exact; row is weaker — see flags) |
| 6 | G2: $\sum_iD_iD_i^T=4I$; on-axis $S=4k^2-k^4/3$ | isotropy | `L313–324 gate_isotropy()` | exact (reg) |
| 7 | G3: $V_3\to i[\delta_{ij}(p-q)\cdot D_l+\delta_{jl}(q-r)\cdot D_i+\delta_{li}(r-p)\cdot D_j]$, deviation $O(a^2)$ | continuum limit | `L335–337 _axis_ym()`, `L369 gate_three_point()` | quantitative (reg: exact; row is weaker — see flags) |
| 8 | G5: $\sum_j\Gamma_{ij}\hat k_j=0$ | Ward identity | `L400–401 gate_ward()` | exact (reg) |
| 9 | G6: $\Gamma$ has 1 zero mode + 4 massless (continuum 4-D YM: 3); $\hat n^T\Gamma\hat n/S\to1$, $\hat n$ couples to $V_3$; projector $P=D^T/2$, $PP^T=I$ | redundant-mode fork | `L423–441 mode_fork()` | exact (reg) |
| 10 | reciprocal basis $2\pi(P^{-1})^T$, $P$ = BCC primitive cell; cube/BZ $=4$; WS mask $k\cdot G\le\lvert G\rvert^2/2$ | fundamental domain (F278) | `L261`, `L278–279 ws_mask()`, `L466–480 brillouin_zone()` | exact (reg) |
| 11 | $S/4$ vs $3\Omega_\text{even}^2$: agree as $k\to0$, differ $O(1)$ at generic $k$ | action ≠ rotation-law propagator at finite $a$ (declared gap) | `L497–498 propagator_split()` | quantitative (always `pass: True`) (reg: exact; row is weaker — see flags) |

**Depends on:** `core.lpt_generator` (`T_GEN`, 04-core.md), `lattice.geometry.BCC_LINK_AXES/BCC_PLAQUETTES` (03-lattice.md), `gluon_self_energy.omega_even` (05a/05b). **Flags:** link hop here is the integer $\langle111\rangle$ vector (length $\sqrt3$) while the Weyl walk hops $d/\sqrt3$ — two different BCC scalings in the codebase; G5 (row 8) checks the closed-form $\Gamma$, not the generated `vertex2`, so it is tautological; `propagator_split` cannot fail.

### `engine/gauge/lpt_d1_action_consistent.py` — action-consistent $d_1$ loop, BCC vs Wilson (F307/F337/F382)
**Status:** partial · standalone · **Findings:** F307 F305 F280 F287 F272 F277 F337 F350 F382 · **Lattice:** BCC rhombus on its WS cell vs hypercubic Wilson on the cube · **Law:** n/a (Euclidean 4-D); rule-propagator alternative $K_\text{true,4d}=3\Omega_\text{even}^2+k_t^2$ tested and rejected · **Units:** lattice

**Does:** one-loop background-field $\Pi_{\mu\nu}$ with each side's own vertices, propagator and Brillouin zone; slope-normalised $d_1$ estimator; refold, propagator-scheme and domain diagnostics.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $V^\text{gf}_{aml}=\delta_{am}\hat k(-k-q)_l-\delta_{ml}\hat k(k)_a$ (axis space) | gauge-fixing vertex | `lpt_d1_action_consistent.py:L100–101 _Vgf()` | bracketed (reg) (row read: exact (closed form)) |
| 2 | $W=\Re(T_3(k,q,-k-q)/i)+V^\text{gf}(k,q)$, $Z=\Re(T_3(k+q,-q,-k)/i)+V^\text{gf}(k+q,-q)$; $t=\hat k(k)+\hat k(k+q)$; phys branch: $W,Z,t$ projected by $P=I-\hat n\hat n^T$ | loop numerator pieces | `L137–144 pi_loop()` | bracketed (reg) (row read: exact integrand) |
| 3 | $\Pi_{mn}=\tfrac{C_A}2\dfrac{\sum_kw(k)\,[W_{aml}Z_{lna}-2t_mt_n]/(S(k)S(k+q))}{\sum_kw(k)}$, $w$ = 1 (cube) or WS mask (sharp or cut-cell) | one-loop self-energy, midpoint grid, no refold | `L145–152 pi_loop()`; chunked `L368–376 pi_loop_chunked()` | bracketed (reg) (row read: quantitative (quadrature)) |
| 4 | $B=(\Pi_{LL}-\langle\Pi_{TT}\rangle)/Q^2$, $L$ = time axis | transverse coefficient | `L159–160 transverse_B()` | bracketed (reg) (row read: quantitative) |
| 5 | $P=B$ if fitted slope $>0$ else $-B$; then `slope_normalised_constant` | sign-normalised side constant | `L166–168 _side()` | bracketed (reg) (row read: quantitative) |
| 6 | $\delta_\text{loops}=\hat C(\text{rule})-\hat C(\text{wilson})$, $1/n^2$ extrapolation, midpoint of both normalisations; quotable iff $\lvert b_0^\text{rec}-1\rvert<0.15$ both sides | full loops difference | `L204–213 _delta_loops()` | bracketed (reg) |
| 7 | $\hat C_\text{rule}=\hat C^W_\text{loops}-\delta_\text{loops}$, $\Lambda=e^{\hat C/2}$ | feed into F280 budget | `L226–230 budget_with_full_dloops()` | bracketed (reg) |
| 8 | $K_\text{true,4d}$ substituted for $S$ on BCC side; own $\lvert b_0^\text{rec}-1\rvert$ non-increasing, swapped diverges | L6 leg 1 (propagator scheme) | `L421`, `L457–459 propagator_scheme_divergence()` | bracketed (reg) (row read: quantitative) |
| 9 | $\max\lvert M(k+G)-M(k)\rvert/\max\lvert M\rvert>0.05$ for reciprocal $G$, while $S(k+G)=S(k)$ to 1e-8 | vertex numerator not $G$-periodic (F382) | `L592–606 vertex_g_periodicity()` | bracketed (reg) (row read: quantitative) |
| 10 | cube domain: $b_0^\text{rec}$ strictly increasing past 1.5; WS bounded | domain-choice test | `L652–654 domain_choice_divergence()` | bracketed (reg) (row read: quantitative) |

**Depends on:** `lpt_bcc_vertex` (this section), `lpt_d1_subtracted` (estimator, constants), `lpt_selfenergy._pi_bgfield` (refold demo), `lpt_ws_mask_cutcell.smoothed_ws_mask`, `gluon_self_energy.K_true_4d` (05a/05b), `core.lpt_generator`. **Flags:** "WHAT THIS MODULE ALSO FOUND" docstring (L45–59) describes the `lpt_selfenergy` refold as surviving, but `lpt_selfenergy` now defaults to `refold=False` (repaired, F308) — stale present tense; row 9 shows the WS-cell domain (G7) is justified for the propagator only, not the full integrand (open, F382).

### `engine/gauge/lpt_d1_subtracted.py` — $d_1$ subtracted against the Wilson 28.8086 anchor (F280)
**Status:** live · standalone · **Findings:** F280 F287 F239 F163 F162 F155 · **Lattice:** cubic BZ quadrature via `bgfield_loop` (continuum vertices, rule/Wilson/continuum propagators) · **Law:** n/a · **Units:** lattice, $1/g^2$ convention

**Does:** bookkeeping that expresses $\Lambda_{\overline{MS}}/\Lambda_\text{rule}$ through differences only, plus a measure-invariant constant estimator and the measured propagator leg.

Convention: $\Pi(q^2)=\tfrac{b_0}{16\pi^2}[\ln(1/q^2)+C]$, $b_0=11$; $\Pi=-B$ of `bgfield_loop`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | slope$_\text{an}=2b_0^{(1/g^2)}=2\cdot\tfrac{11}{16\pi^2}$; $C_{\overline{MS}}=131/66$ (literal) | constants | `lpt_d1_subtracted.py:L117`, `L123` | bracketed (reg) (row read: exact) |
| 2 | $dC=2\ln\Lambda$, $\Lambda=e^{dC/2}$, $d_1=\tfrac{11}{16\pi^2}dC$ | conversions | `L143`, `L148`, `L153` | bracketed (reg) (row read: exact) |
| 3 | $\Lambda_{\overline{MS}}/\Lambda_\text{rule}=e^{11/42}/(q^\ast a)$, $q^\ast a$ = `q_star_a_implied` $=0.7327$ (F151/F155, quantitative) | target | `L167 lambda_ratio_rule_target()` | exact given $q^\ast a$ (inventory F280 §2: 1.773444) |
| 4 | $28.8086\,e^{-(T_W+\delta_\text{loops})/2}=e^{(dC^W_\text{loops}-\delta_\text{loops})/2}$, $T_W=dC^W-dC^W_\text{loops}$ | master identity | `L192–195 master_identity()` | exact (bookkeeping; inventory 6.7e-16) |
| 5 | $s=$ fitted $d\Pi/d\ln(1/Q)$; $\hat C=2\langle\Pi/s-\ln(1/Q)\rangle$ | slope-normalised constant (invariant under $\Pi\to\lambda\Pi$) | `L222–228 slope_normalised_constant()` | exact invariance (inventory 3.1e-15) |
| 6 | analytic-normalised drift $=2(\lambda-1)\langle\ln(1/Q)\rangle+(\lambda-1)C_0$ | control | `L252 measure_invariance()` | bracketed (reg) (row read: exact) |
| 7 | $\delta^\text{prop}_\text{loops}=\hat C(\text{rule})-\hat C(\text{wilson})$ at continuum vertices, $Q=r\cdot2\pi/n$, $r\in2\times\{1.05,1.3,1.6,2\}$ | propagator face | `L291–296 propagator_leg()` | bracketed (reg) (row read: quantitative) |
| 8 | $v(n)=a+b/n^2$ fit, midpoint ± half-spread of two normalisations | extrapolation | `L323–330 propagator_leg_extrapolated()` | bracketed (reg) (row read: quantitative) |
| 9 | total $=dC_\text{rule}^\text{req}-dC_W$; leg1 $=dC^W_\text{loops}-dC_W$; leg2 measured; leg3 $=$ total − leg1 − leg2 | three-leg budget | `L364–369 budget()` | bracketed (reg) (row read: exact bookkeeping; leg3 OPEN) |
| 10 | band $[1,e^{dC^W_\text{loops}/2}]$ (monotonicity assumption) | tadpole-free band | `L412 tadpole_free_band()` | bracketed (reg) |

**Depends on:** `lpt_wilson_selfenergy.B0_INV_G2`, `LAMBDA_RATIO_WILSON_SU3` (this section), `bgfield_loop._Bcoeff_numeric` (05a/05b), constant `q_star_a_implied` (01-constants.md). **Flags:** `F163_C_LAT_WILSON_LOOPS=6.138642608418188` and `C_MSBAR=131/66` are literals copied from F163's artifact, not registry constants; S3 gate band $-1.20<\text{leg2}<-0.80$ is a hand-set window.

### `engine/gauge/lpt_selfenergy.py` — one-loop gluon self-energy from the generated Wilson vertices (+ F308 refold repair)
**Status:** live · test-only · **Findings:** (registry: none; docstring F162 F239 F272 F307 F308) · **Lattice:** 4-D hypercubic Wilson (reference, D1); `kernel='rule'` swaps in $K_\text{true,4d}$ · **Law:** n/a · **Units:** lattice, SU(3), Feynman (background) gauge

**Does:** assembles $\Pi_{\mu\nu}(q)$ from exact generated 3-gluon vertices, ghosts, derived gauge-fixing vertex, Haar measure and seagull, and extracts the transverse finite constant.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\hat K(k)=4\sum_\mu\sin^2(k_\mu/2)$; midpoint grid $(j+\tfrac12)2\pi/n-\pi$ | propagator, grid | `lpt_selfenergy.py:L72 _khat2()`, `L65–67 _bz_grid()` | unknown (inferred: exact / n/a) |
| 2 | $T_{\mu\alpha\beta}=V_3^{(0,1,2)}/(i f^{123})$ | colour-stripped exact 3-gluon tensor | `L130 three_gluon_tensor_grid()` | unknown (inferred: exact (generator)) |
| 3 | $\Pi^\text{gl}_{mn}=\tfrac{C_A}2\big\langle\sum_{\alpha\beta}\Re[T_{m\alpha\beta}(q,k,r)T_{n\alpha\beta}(-q,-k,-r)]/(\hat K(k)\hat K(r))\big\rangle$, $r=-k-q$ | gluon loop | `L151–157 _pi_gluon_loop()` | unknown (inferred: quantitative) |
| 4 | $\Pi^\text{gh}_{mn}=-C_A\langle t_mt_n/(\hat K(k)\hat K(k+q))\rangle$, $t=2\sin\tfrac k2+2\sin\tfrac{k+q}2$ | ghost loop | `L199–203 _pi_ghost_loop()` | unknown (inferred: quantitative) |
| 5 | $V^\text{gh}_\mu=2\sin((p+p')_\mu/2)$ | exact lattice ghost vertex | `L182 ghost_vertex_lattice_exact()` | unknown (inferred: exact (derived)) |
| 6 | $\ln J(X)=\mathrm{tr}_\text{adj}\ln[(1-e^{-\mathrm{ad}_X})/\mathrm{ad}_X]=-c\sum(X^a)^2$, $c=C_A/24$; $\Pi^\text{meas}=-\delta_{mn}C_A/12$ | Haar measure | `L234–252 haar_measure_coefficient()` | unknown (inferred: machine (numeric eigvals, tol 1e-6)) |
| 7 | $Z_0=\langle1/\hat K\rangle$; seagull mass $\tfrac{d-1}2C_AZ_0$ | seagull tadpole | `L268–272 seagull_tadpole()` | unknown (inferred: quantitative) |
| 8 | $V^\text{gf}_{aml}=\delta_{am}(-k-q)_l-\delta_{ml}k_a$; Abbott $=$ symmetric $+V^\text{gf}$ (0/64 mismatches, sympy) | derived gauge-fixing vertex | `L346–347`, `L358–367 gauge_fixing_identity_check()` | unknown (inferred: exact) |
| 9 | $V^\text{gf,lat}=\delta_{am}\widehat{(-k-q)}_l-\delta_{ml}\hat k_a$ (×midpoint phases $e^{-i(q+k)_m/2}$, $e^{ik_m/2}$ if fp='exact') | lattice gf vertex | `L441–450 gauge_fixing_vertex_lattice()` | unknown (inferred: exact (closed form)) |
| 10 | $\Pi_{mn}=\tfrac{C_A}2\langle[W_{aml}Z_{lna}-2t_mt_n]/(K(k)K(k+q))\rangle$, $W$=Abbott$_\text{lat}(k,q)$, $Z$=Abbott$_\text{lat}(k+q,-q)$, $K\in\{\hat K,K_\text{true,4d}\}$ | background-field self-energy | `L483–502 _pi_bgfield()` | unknown (inferred: quantitative) |
| 11 | $C=16\pi^2(B_\text{lat}-B_\text{cont})$, $B=(\Pi_{00}-\Pi_{11})/Q^2$; $\Lambda=\exp(\bar C/22)$ | finite constant | `L521–527 finite_constant_bgfield()` | unknown (inferred: quantitative) |
| 12 | fold $k\to((k+\pi)\bmod2\pi)-\pi$ only if `refold=True` | F307/F308 defect switch (default off) | `L103 _wrap()`, `L109 _folder()` | n/a |

**Depends on:** `core.lpt_generator` (04-core.md), `gauge.bgfield_loop`, `gauge.gluon_self_energy.K_true_4d` (05a/05b). **Flags:** registry lists no findings for a module whose entry point `check_refold_repaired` backs F308; `_pi_gluon_loop`/`_pi_ghost_loop` (rows 3–4) have no gauge-fixing vertex and are superseded in use by `_pi_bgfield` (row 10) — kept for the gluon-only wiring milestone.

### `engine/gauge/lpt_vertex.py` — 3-gluon vertex by amplitude differentiation of the SU(2) Wilson action
**Status:** live · test-only · **Findings:** (registry: none; docstring F155 chain) · **Lattice:** 4-D hypercubic (reference, D1) · **Law:** n/a · **Units:** lattice

**Does:** reads the quadratic and cubic terms of $S(A)$ off finite differences of the compact action.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $U=\cos\tfrac{\lvert V\rvert}2I+i\sin\tfrac{\lvert V\rvert}2\hat V\cdot\sigma$ | $e^{iV^aT^a}$, $T=\sigma/2$ | `lpt_vertex.py:L67 _expi_su2()` | unknown (inferred: exact) |
| 2 | $S=\sum_p(1-\tfrac12\Re\,\mathrm{Tr}\,U_p)$ | Wilson plaquette action | `L85–88 wilson_action()` | unknown (inferred: exact) |
| 3 | $c_2=[S(\epsilon)+S(-\epsilon)]/2\epsilon^2$ ∝ $\hat K=\sum4\sin^2(\pi n/L)$ | quadratic check | `L149–154 propagator_check()` | unknown (inferred: quantitative (spread <1e-6)) |
| 4 | $\partial^3S=\tfrac1{8h^3}\sum_{s_i=\pm}s_1s_2s_3S(s_1h,s_2h,s_3h)$ | 3-gluon amplitude | `L170–176 three_gluon_amplitude()` | unknown (inferred: quantitative (FD)) |
| 5 | $p_1\!\cdot\!p_2(k_1-k_2)\!\cdot\!p_3+\text{cyc}$ | continuum contraction | `L187–190` | unknown (inferred: exact) |

**Flags:** `continuum_limit_check` returns `validated: False` (docstring: missing form factors); premise "rule and Wilson share the plaquette vertex" (L10–16) is invalidated by F265 per `lpt_bcc_vertex` docstring — **SUPERSEDED by F305** as the rule's vertex source.

### `engine/gauge/lpt_ward.py` — continuum 3-gluon vertex Ward identity (sympy)
**Status:** live · test-only · **Findings:** (registry: none) · **Lattice:** continuum · **Law:** n/a · **Units:** n/a

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Gamma_{m_1m_2m_3}=\delta_{m_1m_2}(p_1-p_2)_{m_3}+\delta_{m_2m_3}(p_2-p_3)_{m_1}+\delta_{m_3m_1}(p_3-p_1)_{m_2}$ | vertex | `lpt_ward.py:L42–45 _gamma()` | unknown (inferred: exact) |
| 2 | $D^{-1}_{ab}(p)=p^2\delta_{ab}-p_ap_b$ | inverse propagator | `L51 _dinv()` | unknown (inferred: exact) |
| 3 | $p_1^{m_1}\Gamma_{m_1m_2m_3}=D^{-1}(p_3)-D^{-1}(p_2)$, all 16 components | Ward–Takahashi | `L65–68 ward_identity_symbolic()` | unknown (inferred: exact (sympy)) |
| 4 | $\Gamma_{m_2m_1m_3}(p_2,p_1,p_3)=-\Gamma_{m_1m_2m_3}(p_1,p_2,p_3)$ | Bose antisymmetry of stripped vertex | `L85–91` | unknown (inferred: exact) |

**Flags:** none.

### `engine/gauge/lpt_wilson.py` — Wilson BZ-quadrature core: tadpole $Z_0$ and sum rule
**Status:** live · test-only · **Findings:** (registry: none; docstring F155) · **Lattice:** 4-D hypercubic (reference) · **Law:** n/a · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\int\!\tfrac{d^dk}{(2\pi)^d}f\approx\mathrm{mean}$ over midpoint grid | BZ quadrature | `lpt_wilson.py:L50`, `L64 bz_integral()` | unknown (inferred: quantitative) |
| 2 | $Z_0=\int1/\hat K$, $\hat K=4\sum\sin^2(k_\mu/2)$; target 0.154933390231 | Wilson tadpole | `L55`, `L71 tadpole_Z0()` | unknown (inferred: quantitative) |
| 3 | $\int\hat k_x^2/\hat K=1/4$ | exact sum rule | `L85–86 sum_rule()` | unknown (inferred: quantitative (exact target)) |
| 4 | $b_0=11\cdot3/(48\pi^2)$ | $1/g^2$ convention | `L45` | unknown (inferred: exact) |

**Flags:** docstring says "machine precision, certain values" (L14) but a midpoint rule on the integrable $1/\hat K$ singularity converges algebraically — quantitative; literals `Z0_PUBLISHED`, `LAMBDA_RATIO_WILSON_SU3` are unregistered constants.

### `engine/gauge/lpt_wilson_selfenergy.py` — full Wilson background-field self-energy and the 28.81 test (F163)
**Status:** live · test-only · **Findings:** (registry: none; docstring F155 F162 F163) · **Lattice:** 4-D hypercubic Wilson (reference) · **Law:** n/a · **Units:** lattice, SU(3)

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\hat k_\mu=2\sin(k_\mu/2)$, $\bar c_\mu=\cos(k_\mu/2)$, $\hat K=\sum\hat k^2$ | primitives | `lpt_wilson_selfenergy.py:L89`, `L94`, `L99` | unknown (inferred: exact) |
| 2 | $\Gamma=\delta_{12}\widehat{(k_1-k_2)}_3\bar c(k_3)_3+\text{cyc}$ | Wilson 3-gluon vertex with form factors | `L110–118 gamma3_lattice()` | unknown (inferred: exact (closed form; continuum limit $O(a^2)$ L133–154)) |
| 3 | $\Gamma^F_{aml}=-2\hat q_l\bar c_q\delta_{am}+2\hat q_a\bar c_q\delta_{ml}-(\hat k+\widehat{k+q})_m\delta_{la}$ | lattice Abbott AQQ vertex | `L167–173 gammaF_lattice()` | unknown (inferred: exact (closed form)) |
| 4 | $\Pi_{mn}=\tfrac{C_A}2\langle[\Gamma^F_{aml}(k,q)\Gamma^F_{lna}(k+q,-q)-2V^\text{gh}_mV^\text{gh}_n]/(\hat K(k)\hat K(k+q))\rangle$, $V^\text{gh}=\bar c_q(\hat k+\widehat{k+q})$, $k+q$ **wrapped** into $[-\pi,\pi)$ | loops, chunked over $k_0$ | `L213–234 _pi_chunked()` (wrap L214, ghost L222) | unknown (inferred: quantitative) |
| 5 | $\Pi(q^2)=[\Pi^\text{loop}_{11}(q)-M^2]/\hat q^2$, $M^2=\Pi^\text{loop}_{00}(0)$ | transversality-restored scalar | `L295–296 transverse_scalar()` | unknown (inferred: quantitative) |
| 6 | $f=(-\Pi_{00}(Q),-M^2,-M^2,-M^2)$, check $\hat q\cdot(\Pi+\mathrm{diag}f)=0$ | transversality gate | `L309–313 transversality_check()` | unknown (inferred: quantitative) |
| 7 | $16\pi^2\Pi=11/\bar\epsilon-11\ln(q^2/\mu^2)+131/6$ ⇒ $C_{\overline{MS}}=131/66$ | analytic dim-reg reference | `L383–393 continuum_msbar_constant()` | unknown (inferred: exact (sympy)) |
| 8 | $\Lambda=\exp(C/(2b_0))$, $b_0=11/16\pi^2$; $dC=(\Pi_\text{lat}-\Pi_\text{cont})/(11/16\pi^2)$, $\Lambda_\text{BZ}=e^{dC/2}$ | Λ ratio | `L402`, `L434–436` | unknown (inferred: quantitative) |
| 9 | off-axis $f_\nu=-(\hat q\Pi)_\nu/\hat q_\nu$, $\Pi_S=\mathrm{tr}(\Pi+\mathrm{diag}f)/3\hat q^2$, linear $q\to0$ extrapolation, $\Lambda=e^{(C_\text{lat}-C_{\overline{MS}})/2}$ | Λ estimate (~6–9 vs 28.81) | `L509–513 lambda_status()` | unknown (inferred: quantitative) |

**Flags:** row 4 wraps $k+q$ while the ghost factor $\hat k(k)+\hat k(k+q)$ is a sum of $4\pi$-periodic terms — the F307/F308 refold defect that `lpt_selfenergy` repaired is **still present here** (no `refold` switch; `supersessions.yaml` F277 record declares the `lpt_*` Wilson wraps "an exact no-op", which F307 later showed false for the leading ghost sum, and F308's repair touched only `lpt_selfenergy`) — bites only when $Q>\pi/n$ on the midpoint grid; row 6 is near-tautological ($f_0$ is defined as $-\Pi_{00}$ and the only nonzero $\hat q$ component is 0, so it checks $\Pi_{0n}=0$); docstring "Z0 validated to machine precision" — quadrature, quantitative.

### `engine/gauge/lpt_ws_mask_cutcell.py` — anti-aliased Wigner–Seitz mask (F350)
**Status:** live · driven (1 ch) · **Findings:** F350 F337 F305 F280 · **Lattice:** BCC reciprocal (fcc) WS cell in the cubic $[-\pi,\pi)^3$ · **Law:** n/a · **Units:** lattice

**Does:** fractional WS-cell volume per voxel by adaptive octree, for the BCC loop integral.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | first-shell $G=n\cdot2\pi(P^{-1})^T$, $n\in\{-1,0,1\}^3\setminus0$ (26); plane offset $\lvert G\rvert^2/2$ | half-spaces | `lpt_ws_mask_cutcell.py:L118–121 _shell1_planes()` | exact (reg) |
| 2 | inside iff $\min_\text{voxel}(\lvert G\rvert^2/2-k\cdot G)=\lvert G\rvert^2/2-k_0\cdot G-h\sum_i\lvert G_i\rvert\ge0\ \forall G$; outside iff some $G$ has max $<0$ | interval classification | `L153–159 _classify()` | exact (reg) |
| 3 | $w=\sum_\text{depth}8^{-(d+1)}\#\text{inside children}+\tfrac12\,8^{-D}\#\text{unresolved}$ | octree fraction | `L181–193 _cutcell_fraction_batch()`; batch $=\max(1,\lfloor\text{budget}/8^D\rfloor)$ `L215` | quantitative (bias set by depth only) (reg: exact; row is weaker — see flags) |
| 4 | mask $=1$ inside, 0 outside, row 3 on boundary voxels | smoothed mask | `L237–245 smoothed_ws_mask()` | quantitative (reg: exact; row is weaker — see flags) |
| 5 | $\lvert\langle w\rangle-1/4\rvert$ vs $n$, log-log slopes | isolation gate (target $V_\text{WS}/V_\text{cube}=1/4$) | `L263–277 mask_isolation_convergence()` | quantitative (<5e-3) (reg: exact; row is weaker — see flags) |

**Depends on:** `lpt_bcc_vertex.ws_mask` (this section). **Flags:** registry exactness `exact` but the delivered mask is an approximation with measured bias (rows 3–5 quantitative); only the classification (row 2) and G1 shell match are exact.

### `engine/gauge/minimal_coupling.py` — U(1) wrap, U(1) Peierls links, SU(3) rotate-then-step
**Status:** live · driven (9 ch) · **Findings:** (registry: none; cites F27 F41 F42) · **Lattice:** BCC walk (spectral) · **Law:** n/a (fermion walk) · **Units:** lattice

**Does:** couples fermions to U(1) and SU(3) gauge fields on the 3-D BCC walk.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\psi'=e^{+iq\alpha}\,\mathrm{BCC}[e^{-iq\alpha}\psi]$ | U(1) Stueckelberg-form wrap (Weyl) | `minimal_coupling.py:L62–65 u1_wrap_weyl_step_3d_bcc()` | unknown (docstring: covariance to machine precision) |
| 2 | same wrap around `dirac_step_3d_bcc_splitstep` | massive Dirac version | `minimal_coupling.py:L80–85 u1_wrap_dirac_step_3d_bcc()` | unknown |
| 3 | $\tilde q_i=V_{ij}q_j$, $V=\exp(i\varepsilon A^aT^a)$, then BCC step per colour | SU(3) site-local rotate-then-step | `minimal_coupling.py:L108–115 su3_rotate_weyl_step_3d_bcc()` | unknown |
| 4 | $A'^a=2\,\Re\,\mathrm{tr}(T^aVHV^\dagger)$, $H=A^aT^a$ | adjoint transform of the potential | `minimal_coupling.py:L130–133 su3_adjoint_transform_potential()` | unknown |
| 5 | $\psi'=\sum_dU_d\,M_d\,\mathrm{shift}_{d/\sqrt3}\psi$, $U_d=\exp(iq\,c_\text{lat}\,\mathbf A\cdot d)$ | per-link Peierls U(1) step; uniform $A$ ⇒ $U_\text{BCC}(k+qA)$ | `minimal_coupling.py:L221–229 u1_link_weyl_step_3d_bcc()` (phase L226) | unknown (non-unitary for non-uniform $A$, docstring) |
| 6 | $\lVert\psi'\rVert^2-\lVert\psi\rVert^2$ | norm drift of row 5 | `minimal_coupling.py:L239–242` | n/a (diagnostic) |

**Depends on:** `lattice.bcc.weyl_step_3d_bcc`, `bcc_fractional_shift`; `weak_wmu._SPINOR_MATS`, `BCC_DIRS` (this section); `gauge.gluon._su3_expmap_field`, `gauge.strong.T_GEN`; `particles.dirac_bcc`. Constant: $c_\text{lat}=1/\sqrt3$ (F26). **Flags:** none beyond the stated non-unitarity of row 5 (fork `forks/gauge/u1_link_unitarity_forks.py`, 08a/08b).

### `engine/gauge/photon.py` — paired-spinor photon (THE photon)
**Status:** partial · driven (20 ch) · **Findings:** (registry: none; module cites F26 F64 F65–F69 F105 F271 F386–F390) · **Lattice:** BCC dispersion on cubic k-grid · **Law:** even · **Units:** lattice

**Does:** propagates the real $(\mathbf E,\mathbf B)$ doublet by the helicity-symmetric pair rate $\Omega_\text{pair}$; also a k-resolved step through the F64 dielectric, and beam/mode builders.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$, $\omega^\pm=\arccos u^\pm$ | pair rotation rate per tick | `photon.py:L73 pair_dispersion()` | unknown (registry None); on-axis $\Omega_\text{pair}(k\hat x)=c_\text{lat}k$ **exact** (inventory #220, F300) |
| 2 | $\Delta\Omega=2\omega^+(\mathbf k/2)-2\omega^-(\mathbf k/2)$ | the birefringent split the pair does *not* have (diagnostic only) | `photon.py:L81 pair_birefringence()` | unknown |
| 3 | $\tilde E'=\cos\Omega_\text{pair}\,\tilde E+\sin\Omega_\text{pair}\,\tilde B,\ \ \tilde B'=-\sin\Omega_\text{pair}\,\tilde E+\cos\Omega_\text{pair}\,\tilde B$ per mode, same scalar $\Omega$ on all 3 components | one tick of the photon | `photon.py:L105–106 photon_step_spectral()` | unknown (norm-conserving rotation; identical to `_f26_rotation_step`, spot-check $8.9\times10^{-16}$) |
| 4 | same rotation at angle $\Omega_\text{pair}\tau$ | exact unitary part of a split step | `photon.py:L128–132 _even_rotate()` | unknown |
| 5 | $M V=\tfrac12\big(\delta\,\mathcal F^{-1}\Omega\mathcal F V+\mathcal F^{-1}\Omega\mathcal F(\delta V)\big)$ | Weyl-ordered product $\delta(x)\Omega(k)$ | `photon.py:L161–165 _M_weyl()` | unknown |
| 6 | $E'=E+hMB-\tfrac{h^2}{2}M^2E,\ \ B'=B-hME-\tfrac{h^2}{2}M^2B$ | 2nd-order half step of $e^{hMJ}$ | `photon.py:L197–198 _dielectric_half()` | unknown (inferred: quantitative (truncated exponential; docstring measures $O(n_\text{sub}^{-2})$)) |
| 7 | $s=1/K,\ s_0=\langle s\rangle,\ \delta=s-s_0$; Strang: half($\delta$) · rotate($s_0\Omega\,dt/n$) · half($\delta$), $n_\text{sub}$ times; if $\delta\equiv0$ exact rotation at $\Omega/K$ | photon in the F64 dielectric, rate $\Omega_K=\Omega_\text{pair}(k)/K(x)$ | `photon.py:L275–286 photon_step_dielectric()` | unknown (inferred: quantitative (uniform-$K$ branch L279 exact rotation)) |
| 8 | $\mathbf e_2=\hat k\times\mathbf e_1$, planted at $\pm m$ with Hermitian conjugate | single linearly polarised mode | `photon.py:L305–314 build_pair_mode()` | n/a (constructor) |
| 9 | $v=\Omega_\text{pair}(h\hat n)/h$; $v(k_0)=[\Omega(k_0+h\hat n)-\Omega(k_0-h\hat n)]/2h$ | group velocity (small-k and at carrier) | `photon.py:L322 group_velocity()`, `L334 group_velocity_at()` | unknown (finite difference); spot-check → $1/\sqrt3$ |
| 10 | $f=e^{-r^2/2\sigma^2}e^{ik_0 d_\text{axis}}$; linear: $E_p=\Re f,\ B_p=\Im f$ (same component); circular: $E_{a1}=\Re f/\sqrt2,\ B_{a1}=\Im f/\sqrt2,\ E_{a2}=-\Im f/\sqrt2,\ B_{a2}=\Re f/\sqrt2$ | one-sided RS beam packet | `photon.py:L409–421 build_beam_packet()` | n/a (constructor) |
| 11 | $\mathbf P=\tfrac1N\Re\sum_k\tilde{\mathbf E}_k\times\overline{\tilde{\mathbf B}_k}$ | Parseval field momentum | `photon.py:L439–442 _field_momentum_k()` | unknown (inferred: machine (gate `momentum_conserved_under_free_propagator` < 5e-15, L520)) |

**Verified from code (task checklist):** *paired spinor / $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$* — yes (row 1). *Even law* — yes, a single real rotation, and $\Omega_\text{pair}(-k)=\Omega_\text{pair}(k)$ (spot-check 0.0; because $u^+(-k)=u^-(k)$). *$c=1/\sqrt3$* — the step never uses `c_lat`; it emerges from $\arccos u$ with arguments $k/(2\sqrt3)$: small-$k$ slope $0.57735$ (spot-check), and exactly $c_\text{lat}k$ on a cubic axis. *Non-birefringent* — structural: one scalar $\Omega(k)$ multiplies every Cartesian component, so both helicities $F^\pm$ share it; the propagator carries no helicity index. *No σ-bilinear* — confirmed; `bilinear` is not imported. The imported `_f26_rotation_step` (L53) is **not called**; the photon re-implements the identical formula.

**Inputs → outputs:** real `(3,Lx,Ly,Lz)` $E,B$ (+ optional $K(x)$) → same shape. **Depends on:** `lattice.bcc.bcc_dispersion` (03-lattice.md § bcc.py), `lattice.geometry.make_kgrid_3d`, `casim.numerics.fft` (02-numerics.md). **Flags:** registry lists no findings for the module; the docstring (L35) states "$\omega^\pm(k/2)\to(1/\sqrt3)(k/2)/\ldots$" (truncated); `build_beam_packet` "linear" default is a non-null RS field ($\mathbf E\parallel\mathbf B$, zero Poynting momentum) retained for F386–F390 bit-compatibility (docstring L360–365, fix L415–421).

### `engine/gauge/photon_bound_state.py` — two-body contact bound state of the paired photon (F169)
**Status:** live · test-only · **Findings:** (registry: none; docstring F69 F74 F168 F169 F397 F401) · **Lattice:** BCC dispersion, relative-momentum grid $p\in[0,2\pi)^3$ · **Law:** even at $p=0$ · **Units:** lattice

**Does:** Koster–Slater rank-1 contact problem in the relative momentum of the $(+,-)$ constituents at fixed total $k$; the photon is the threshold state.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $E_0(p;k)=\omega^+(k/2+p)+\omega^-(k/2-p)$ | free two-body dispersion | `photon_bound_state.py:L73–75 relative_dispersion()` | unknown |
| 2 | $\Omega_\text{even}(k)=E_0(0;k)$ | paired-photon rate | `photon_bound_state.py:L81 omega_even()` | unknown |
| 3 | $T(k)=\min(\omega^+(k),\omega^-(k))$ | continuum floor, closed form (collinear endpoint $p=\pm k/2$) | `photon_bound_state.py:L106 threshold_closed_form()` | unknown (docstring: 60-digit check) |
| 4 | $\Omega_\text{even}-T\approx\lvert k_xk_yk_z\rvert/(3\lvert k\rvert)$ | leading-order offset | `photon_bound_state.py:L120 threshold_offset_closed_form()` | unknown (leading order only; spot-check 0.0149 vs 0.0163 true at $\lvert k\rvert=0.54$) |
| 5 | $g_c=1/\langle 1/(E_0-T)\rangle_\text{BZ}$ over $E_0>T+\epsilon$; $T$ = grid min (default) or row 3 | critical (threshold) coupling | `photon_bound_state.py:L181–189 critical_coupling()` | unknown (inferred: unknown; F169 row 215: exact secular root at $g_c$) |
| 6 | $\psi(p)\propto1/(E_0-T)$, normalised | threshold wavefunction | `photon_bound_state.py:L207–210 threshold_wavefunction()` | unknown |
| 7 | $1=g\langle1/(E_0-E_b)\rangle$, bisection on $E_b<T_\text{grid}$ | bound-state energy | `photon_bound_state.py:L235 bound_state_secular()` | unknown (inferred: quantitative (bisection tol 1e-13)) |
| 8 | lowest eigenpair of $\mathrm{diag}(E_0)-g\lvert c\rangle\langle c\rvert$ | dense cross-check | `photon_bound_state.py:L243–246 bound_state_dense()` | unknown (inferred: machine (eigh)) |
| 9 | $r_\text{rms}=\sqrt{\sum\lvert\psi(x)\rvert^2x^2}$, $\psi(x)=\mathcal F^{-1}\psi(p)$ | size | `photon_bound_state.py:L253–258` | n/a |

**Depends on:** `lattice.bcc.bcc_dispersion`. **Flags:** the BZ average (rows 5–7) runs over $p\in[0,2\pi)^3$ (`_grid`, L64) — but $\omega^\pm$ evaluated at $k/\sqrt3$ has period $2\sqrt3\pi$, not $2\pi$, so this is not a full BZ of the walk nor the `fftfreq` window other kernels use; the domain choice is not justified in code (OTHER, open). `bound_state_secular` has no `threshold="closed"` option (still grid T). Registry lists no findings.

### `engine/gauge/photon_bound_state_finite_k.py` — finite-k threshold repair (F401)
**Status:** live · standalone (1 ch listed) · **Findings:** F401 F169 F397 · **Lattice:** BCC dispersion · **Law:** even · **Units:** lattice

**Does:** proves the on-axis double degeneracy symbolically and sweeps $g_c(k,L)$ with the closed-form threshold.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u^\pm(q,0,0)=\cos(q/\sqrt3)$ ⇒ $\omega^+=\omega^-=\lvert q\rvert/\sqrt3$ ⇒ $\Omega_\text{even}=T$ on an axis | axis identity (sympy) | `photon_bound_state_finite_k.py:L135–157 axis_dispersion_isotropic_cone_exact()` | quantitative (reg) (row read: exact) |
| 2 | $\Omega_\text{even}-T\ne0$ at $k_z=0$, generic $k_x,k_y$ | in-plane contrast | `L172–176 in_plane_offset_is_not_exactly_zero()` | quantitative (reg) |
| 3 | $g_c(k,L)$ via `critical_coupling(threshold=...)` | L-ladder | `L186–188 l_convergence()` | quantitative (reg) |
| 4 | $g_c(\lvert k\rvert\hat d)$ with closed $T$ | direction sweeps (111), (311), (210) | `L210 gc_k_sweep_direction()`; verdicts `L289–305 report()` | quantitative (reg) |
| 5 | #violations, max backslide of $g_c(L)$ sequences | dense-L artifact metric | `L239–244 dense_l_scan_comparison()` | quantitative (reg) |

**Depends on:** `photon_bound_state` (above), `lattice.dimensionality.bloch_vector` (03-lattice.md), sympy. Imports numpy via `casim.numerics.xp` (D8). **Flags:** row 1 re-types $u^\pm$ in sympy rather than evaluating the engine's `_bcc_uvec` (it checks the formula, not the code path); inherits the $[0,2\pi)^3$ domain question of `photon_bound_state`.

### `engine/gauge/photon_packet.py` — real-space photon packet propagation (F314)
**Status:** live · standalone · **Findings:** F314 F20 F69 F105 · **Lattice:** BCC dispersion on cubic grid (non-cubic box allowed) · **Law:** even (uses `photon.photon_step_spectral` unmodified) · **Units:** lattice

**Does:** closed-form pair group velocity and a wrap-free measured packet run compared against it.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u^s=c_xc_yc_z+s\,s_xs_ys_z$; $g^s_x=s_xc_yc_z-s\,c_xs_ys_z$, $g^s_y=c_xs_yc_z-s\,s_xc_ys_z$, $g^s_z=c_xc_ys_z-s\,s_xs_yc_z$ (args $k\,c_\text{lat}$) | Bloch scalar and $-\partial u/\partial k_i / c_\text{lat}$ | `photon_packet.py:L131–134 _u_and_grad()` | exact (reg) |
| 2 | $\partial_{k_i}\Omega_\text{pair}=\tfrac{c_\text{lat}}2\sum_\pm g^\pm_i(k/2)/\sqrt{1-(u^\pm)^2}$ | pair group velocity | `photon_packet.py:L150–154 pair_group_velocity()` | exact (reg) |
| 3 | $u^\pm(k\hat e/2)=\cos(k\,c_\text{lat}/2)$ | on-axis identity, tol 0 | `L179–180 onaxis_pair_u_residual()` | exact (inventory #220) |
| 4 | $\max\lvert\Omega_\text{pair}(k\hat e)-k\,c_\text{lat}\rvert\le$ arccos bound | on-axis linearity | `L206–207` | machine (reg: exact; row is weaker — see flags) |
| 5 | $\partial_{k_x}\Omega_\text{pair}=c_\text{lat}$, $\partial^2_{k_x}\Omega_\text{pair}=0$ on axis | no on-axis dispersion | `L220–221`, `L235–236` | machine / FD (reg: exact; row is weaker — see flags) |
| 6 | $w(k)=\lvert\tilde F\rvert^2/\sum\lvert\tilde F\rvert^2$; $\bar v=\sum_kw(k)\,\partial_{k_x}\Omega_\text{pair}$ | exact finite-width centroid velocity | `L277–278 packet_spectrum()`, `L291 predicted_packet_velocity()` | exact (reg) |
| 7 | $\Delta v/v\approx1/(2(k_0\sigma_\perp)^2)$ | F105 small-angle approx (for comparison) | `L303 diffraction_deficit_approx()` | n/a (approximation) |
| 8 | $\bar x=\sum x\rho/\sum\rho$, $\rho=\lvert E\rvert^2+\lvert B\rvert^2$; bias $\le\varepsilon L$ | estimator and its bound | `L316–318 _centroid_track()`, `L356 centroid_bias_bound()` | n/a |
| 9 | gate: $\lvert v_\text{meas}-\bar v\rvert/\bar v\le10^{-12}$, energy drift $\le10^{-12}$, polarisation independence $\le10^{-14}$ | registry checks | `L620–629 check_photon_packet_propagation()` | machine (reg: exact; row is weaker — see flags) |

**Depends on:** `gauge.photon` (this section), `lattice.wavepacket.arccos_amplification_bound`, `casim.numerics`. **Flags:** registry exactness `exact` while the propagation gate is a 1e-12 tolerance (machine) — mixed module; docstring flags `lattice.wavepacket.weyl_group_velocity` ($c_\text{lat}\hat n_i$) as wrong off the x-axis (cross-sector, 03-lattice.md).

### `engine/gauge/photon_pryce_commutator.py` — Pryce composite-boson test (F398)
**Status:** live · standalone · **Findings:** F398 F69 F169 · **Lattice:** relative-momentum grid of `photon_bound_state` · **Law:** n/a · **Units:** lattice

**Does:** builds $a^\dagger_k=\sum_p\psi_k(p)\,b^\dagger_{+,k/2+p}b^\dagger_{-,k/2-p}$ exactly on a small fermionic Fock space and measures the two-photon norm deficit.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c^\dagger_m$: sign $(-1)^{\#\{\text{occ}<m\}}$, 0 if occupied | exact Jordan–Wigner creation | `photon_pryce_commutator.py:L77–81 _apply_creation()` | quantitative (reg) (row read: exact) |
| 2 | $a^\dagger_0=\sum_p\psi(p)\,b^\dagger_{+,p}b^\dagger_{-,-p}$ ("shared" control: partner ≡ 0) | composite creation | `L105–119 _apply_a_dagger_fock()` | quantitative (reg) (row read: exact) |
| 3 | $\lVert(a^\dagger)^2\lvert0\rangle\rVert^2=2(1-\sum_p\psi^4)$ | closed-form two-photon norm | `L146 deficit_closed_form()`, `L152 two_photon_norm_closed_form()` | quantitative (reg) (row read: exact (algebraic identity; gate < 1e-10 vs Fock, L274)) |
| 4 | $\sum_p(E_0-T)^{-2}/L^3$ | bulk normalisation ratio | `L160–164 bulk_normalization_ratio()` | quantitative (reg) |
| 5 | $\min_{L'\in[L-4,L+4]}\sum\psi^4$ | resonance-robust deficit; gate ratio $d(10)/d(100)\in[20,200]$ | `L208–219 deficit_robust_min()`, `L282` | quantitative (reg) |

**Depends on:** `photon_bound_state.threshold_wavefunction`, `relative_dispersion`. **Flags:** registry `quantitative` fits rows 4–5; rows 1–3 are exact. Writes `test-results/F398_...json` only under `__main__` (guarded).

### `engine/gauge/propagator.py` — cached spectral propagator objects (fermion walks)
**Status:** live · test-only · **Findings:** (registry: none) · **Lattice:** BCC Weyl/Dirac (3-D, canonical) and 2-D exact / linear (reference, D1) · **Law:** n/a (spinor walks, not the $(E,B)$ rotation law) · **Units:** lattice

**Does:** precomputes the unitary $U(k)$ once per shape so each tick is FFT · multiply · IFFT. Mostly plumbing; the physics lives in `lattice.bcc`, `lattice.core_exact`, `particles.dirac_bcc`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\begin{pmatrix}\tilde f'\\\tilde g'\end{pmatrix}=U_\text{BCC}^\pm(k)\begin{pmatrix}\tilde f\\\tilde g\end{pmatrix}$ | cached BCC Weyl tick | `propagator.py:L107–109 BccWeylPropagator.step()` | unknown (see 03-lattice.md § bcc.py) |
| 2 | $D_k$: $\eta'=nA\eta+im\,\chi$, $\chi'=im\,\eta+nA^\dagger\chi$, $n=\sqrt{1-m^2}$ | BCC Dirac tick | `propagator.py:L203–209 _apply_Dk_k()` | unknown (see 06a/06b § dirac_bcc) |
| 3 | $\psi(dt)=\cos(\omega dt)\psi+\tfrac{\sin(\omega dt)}{\sin\omega}(D_k-\cos\omega)\psi$ | fractional-dt spectral interpolation | `propagator.py:L193–197`, `L239–242 step()` | unknown |
| 4 | $U=\cos(c\kappa)I-i\tfrac{\sin(c\kappa)}{\kappa}\begin{pmatrix}0&k_x-ik_y\\k_x+ik_y&0\end{pmatrix}$ | 2-D linear Weyl step | `propagator.py:L335–342 Linear2DPropagator._build()` | unknown |
| 5 | $\lvert\omega\rvert$ = slope of unwrapped phase (LSQ); zero-padded Hann-windowed DFT peak, $\Delta\omega_\text{eff}=2\pi/(N_tp\,dt)$ | phase-rate extraction (estimators) | `propagator.py:L378–382 phase_rate_lsq()`, `L423–438 phase_rate_zeropad()` | n/a (estimator) |

**Depends on:** `lattice.bcc.bcc_unitary`, `lattice.core_exact.exact2d_unitary`, `particles.dirac_bcc.bcc_dirac_dispersion`, `casim.numerics.fft`. **Flags:** `phase_rate_zeropad` searches only the first half of the padded spectrum (L434) — negative frequencies of a complex signal are not seen; the docstring floor scalings (L34–36) are asserted, not computed.

### `engine/gauge/reflection_positivity.py` — Osterwalder–Seiler link reflection positivity on BCC$_3\times\mathbb Z$ (F335)
**Status:** live · standalone · **Findings:** F335 F265 F323 F313 F94 · **Lattice:** BCC spatial × integer time (4-D Euclidean, `bcc_action` links) · **Law:** n/a · **Units:** lattice

**Does:** checks the OS/Menotti–Pelissetto hypotheses on the loop list, the reflection map, SU(2) character positivity, and a Monte-Carlo Gram-matrix smoke check.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | rhombi: $\Delta t=0$; mixed loops: exactly two temporal legs, signs $\{-1,+1\}$, hop $(0,0,0,\pm1)$; counts 6 + 4 | structural hypotheses | `reflection_positivity.py:L102–128 loop_structure_reflection_hypotheses()` | machine (reg) (row read: exact (integer/boolean)) |
| 2 | $\theta$: spatial $\tau\to L_t-1-\tau$ (no dagger); temporal $\tau\to(L_t-2-\tau)\bmod L_t$ with dagger | reflection map | `L158–162 theta_reflect_config()` | machine (reg) (row read: exact) |
| 3 | $\theta\circ\theta=\mathrm{id}$ | involution | `L170–175` | machine (reg) |
| 4 | $\mathrm{Tr}\,\theta P_\text{mixed}(\tau)=\overline{\mathrm{Tr}\,P_\text{mixed}(\tau_m)}$, $\tau_m=(L_t-2-\tau)\bmod L_t$ | cyclic-trace identity (certifies the dagger) | `L195–200 mixed_plaquette_reflection_trace_residual()` | machine (reg) |
| 5 | $\chi_j(\theta)=\sin((2j+1)\theta/2)/\sin(\theta/2)$; $a_j(\beta)=\int_0^{2\pi}\tfrac1\pi\sin^2\tfrac\theta2\,e^{2\beta\cos(\theta/2)}\chi_j\,d\theta$ (midpoint rule) | SU(2) character coefficient; closed form (docstring, not computed) $I_{2j}(2\beta)-I_{2j+2}(2\beta)=\tfrac{2j+1}\beta I_{2j+1}(2\beta)>0$ | `L211–213`, `L225–228 su2_character_coeff_numeric()` | quantitative (numeric witness; proof is the Bessel identity) (reg: machine; row is weaker — see flags) |
| 6 | $G_{ij}=\tfrac1M\sum F_i(\text{mirror})F_j(\tau_+)$, symmetrised; eigenvalues + 200-sample bootstrap of $\lambda_\text{min}$ | Gram-matrix MC cross-check | `L321–331 reflection_positivity_gram_check()` | quantitative (MC; gate asserts only $\lambda_\text{max}>0$, L405) (reg: machine; row is weaker — see flags) |

**Depends on:** `gauge.bcc_action` (`BCC4_LOOPS`, `plaquette_4d`, `sweep_4d`, … — 05a/05b), `casim.numerics.xp/rng`. **Flags:** the Gram smoke gate G1 asserts only the dominant eigenvalue; the subleading directions are unresolved (module docstring §4).

### `engine/gauge/rotation.py` — Hartle slow-rotation frame dragging (misfiled: not a gauge module)
**Status:** live · test-only · **Findings:** (registry: none; docstring F181 F185) · **Lattice:** n/a (radial ODE) · **Law:** n/a · **Units:** geometric km ($G=c=1$) → SI

**Does:** solves Hartle's $\varpi$ ODE on the F181 interior metric and returns the moment of inertia.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $j=(AB)^{-1/2}$ | Hartle $j(r)$ | `rotation.py:L40 _background()` | unknown |
| 2 | $\varpi''=-(4/r+j'/j)\varpi'-\tfrac{4j'}{rj}\varpi$ (expanded $(r^4j\varpi')'+4r^3j'\varpi=0$), $\varpi(0)=1,\varpi'(0)=0$, semi-implicit Euler–Cromer | frame-drag ODE | `rotation.py:L56–59 frame_drag()` | unknown (inferred: quantitative (1st-order integrator)) |
| 3 | $J=\tfrac16R^4\varpi'(R)$, $\Omega=\varpi(R)+\tfrac R3\varpi'(R)$, $I=J/\Omega$ | angular momentum, spin, inertia | `rotation.py:L62–64` | unknown (inferred: quantitative) |
| 4 | $I_\text{SI}=I_{\text{km}^3}\cdot10^9\,c^2/G$ | unit conversion (`c_SI`, `G_CODATA`, external) | `rotation.py:L83 moment_of_inertia_SI()` | external constants |

**Depends on:** `interactions.interior_metric` (07-series). **Flags:** sector misplacement (astrophysics in `gauge/`); `sys.path.insert` at import (L30).

### `engine/gauge/strong.py` — SU(3)$_c$ quark sector on frozen links, F27 masses, 2-D EW doublet (Phase E3)
**Status:** live · driven (17 ch) · **Findings:** (registry: none; docstring F27 F31 F34 F40 FG-2 FG-3) · **Lattice:** 2-D square (reference, D1) throughout · **Law:** n/a (Dirac walk; cold links use the exact-QCA arccos step of `particles.dirac`) · **Units:** lattice

**Does:** 3-flavour × 3-colour × 4-Dirac quark field on 2-D SU(3) links: generators, Haar sampling, gauge transforms, covariant kinetic steps (cold: FFT; non-cold: Cayley), colour Noether current, Wilson action, F27 complex mass, and a 2-D W-link SU(2)$_L$ doublet step.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $T^a=\lambda^a/2$ (Gell-Mann), $\mathrm{Tr}\,T^aT^b=\tfrac12\delta^{ab}$ | generators (`T_GEN`, reused by `minimal_coupling`, `lpt_*`) | `strong.py:L66–79`; check `L99–103` | unknown (inferred: exact) |
| 2 | $V=e^{iH}$, $H=\theta^aT^a=U\mathrm{diag}(\lambda)U^\dagger$ ⇒ $V=U\mathrm{diag}(e^{i\lambda})U^\dagger$ | SU(3) exponential (Hermitian eigh) | `L122–124 su3_exp()` | unknown (inferred: machine) |
| 3 | QR of $(A+iB)/\sqrt2$, Mezzadri phase fix, $Q\to Q\,\overline{\det Q}^{1/3}$ | Haar SU(3) | `L137–148 su3_haar()` | n/a (sampler) |
| 4 | $q\to Vq$; $U_\mu\to V(x)U_\mu V^\dagger(x+\hat\mu)$ | local gauge transform | `L282`, `L300–301 gauge_transform_links()` | unknown (inferred: exact) |
| 5 | $q_\text{cov}=\tfrac1{2n_\text{dir}}\sum_\mu[U_\mu q(x+\hat\mu)+U_\mu^\dagger(x-\hat\mu)q(x-\hat\mu)]$ | covariant shift average (non-unitary, per docstring) | `L376–385 covariant_half_step()`, `L399–419 covariant_shift()` | n/a |
| 6 | $(I+\kappa\sigma_xD_\mu)\eta'=(I-\kappa\sigma_xD_\mu)\eta$; $\chi$ with $-\kappa$; $D_\mu\psi=U_\mu\psi(x+\hat\mu)-U_\mu^\dagger(x-\hat\mu)\psi(x-\hat\mu)$; dense cyclic $6L\times6L$ solve per slice | covariant Cayley (Crank–Nicolson) step, one direction | `L525–549 _cov_cayley_1dir()` | unknown (inferred: machine (Cayley ⇒ unitary; `np.linalg.solve`)) |
| 7 | Strang $K_x(\kappa=\tau/8)\,K_y(\tau/4)\,K_x(\tau/8)$ | 2-D kinetic half step | `L579–593 _covariant_kinetic_half_cayley()` | unknown (inferred: quantitative (splitting)) |
| 8 | cold links: `dirac_step_2d_splitstep` per $(f,c)$; else kinetic(½) · F27 mass · kinetic(½) | full strong tick | `L679–693 step_strong_2d()` | unknown |
| 9 | $J^a_0=\sum_{f,d}q^\dagger T^aq$; $J^a_i=q^\dagger\alpha_iT^aq$, $\alpha_x=\mathrm{diag}(\sigma_x,-\sigma_x)$, $\alpha_y=\mathrm{diag}(\sigma_y,-\sigma_y)$ | colour Noether current | `L723–733 noether_charge_density()`, `L771–801 noether_current_spatial()` | unknown |
| 10 | $\partial_\mu J^a_\mu\approx(J_0^+-J_0^-)/2dt+\sum_i(J_i(x+\hat i)-J_i(x-\hat i))/2$ | lattice divergence (V13) | `L821–824 lattice_3divergence()` | n/a (diagnostic) |
| 11 | $V^{ab}_\text{adj}=2\,\Re\,\mathrm{Tr}(T^aVT^bV^\dagger)$ | adjoint rotation | `L846` | unknown (inferred: exact) |
| 12 | $S_g=\beta\sum_\square(1-\tfrac1{N_c}\Re\,\mathrm{Tr}\,U_\square)$ | 2-D Wilson action | `L865–881` | unknown (inferred: exact) |
| 13 | $M(\theta_f)=\begin{pmatrix}c_mI&is_me^{i\theta_f}I\\ is_me^{-i\theta_f}I&c_mI\end{pmatrix}$ per $(f,c)$ via `dirac.mass_step_1flavor_u1` | F27 quark mass | `L975–987 quark_mass_step_f27()` | unknown (see 06a/06b § dirac) |
| 14 | $(\eta_u,\eta_d)\to V(\eta_u,\eta_d)$, $\chi$ fixed, $U\to VU$ | chiral SU(2)$_L$ transform | `L1146–1153 quark_doublet_su2_transform_chiral()` | unknown (inferred: exact) |
| 15 | $W_\mu\to V(x)W_\mu V^\dagger(x+\hat\mu)$; $U_\text{eff}=\sum_\mu W_\mu/\lVert\cdot\rVert$ | 2-D W links | `L1239–1243`, `L1268–1276` | unknown (inferred: exact / unknown) |
| 16 | [colour `covariant_half_step`] · K$_W$(½): $\eta_\text{doublet}\to U_\text{eff}\eta$ then `_weyl_half_step_2c`; $\chi$ unrotated · doublet mass · K$_W$(½) · [colour step] | covariant quark doublet step | `L1413–1422 covariant_quark_doublet_step_2d()` | unknown |

**Depends on:** `particles.dirac` (`dirac_step_2d_splitstep`, `_weyl_half_step_2c`, `mass_step_1flavor_u1`, `mass_step_doublet_su2`, `dirac_step_complex_mass_1flavor` — 06a/06b); numpy directly (not `casim.numerics`, D8). **Flags:** (a) row 6 uses $\sigma_x$ for **both** directions ($H_\mu=\sigma_xp_\mu$ for $\mu=y$ too, L443, L525–545), whereas the cold-link path is the exact 2-D Weyl QCA — the non-cold and cold paths are different Hamiltonians (open, not settled here); (b) `step_strong_2d_complex_mass` docstring (L994–1001) describes `parallel_transport` Strang steps, code uses Cayley (L1036–1052); (c) row 16 wraps the unitary doublet step in the non-unitary `covariant_half_step` (row 5) when `U_color` is given; (d) `parallel_transport` (L309–342) is **deprecated** (gauge-variant), retained as alias; dead loop L1321–1337 computes and discards `eu_rot/ed_rot`.

### `engine/gauge/su3_ladder.py` — SU(3) electric Casimir ladder and character rotor (F111b, F325)
**Status:** live · test-only · **Findings:** (registry: none; docstring F98–F101 F110 F111 F325) · **Lattice:** single link / 1-D flux chain (no spatial lattice) · **Law:** n/a · **Units:** lattice ($g^2$, $\lambda$)

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $C_2(p,q)=(p^2+q^2+pq+3p+3q)/3$; $\dim=(p+1)(q+1)(p+q+2)/2$; triality $(p-q)\bmod3$ | irrep data | `su3_ladder.py:L96 casimir2()`, `L101–103 dim_irrep()`, `L112 triality()` | unknown (inferred: exact (Fraction)) |
| 2 | $3\otimes(p,q)=(p{+}1,q)\oplus(p{-}1,q{+}1)\oplus(p,q{-}1)$; $\bar3\otimes$ analogous | fundamental fusion | `L118`, `L124 fuse_F()`, `fuse_Fbar()` | unknown (inferred: exact) |
| 3 | $\sum_{R'\in F\otimes R}\dim R'-3\dim R=0$ | fusion dimension check | `L139–142` | unknown (inferred: exact) |
| 4 | $\int\chi_A\chi_B\,d\mu$ on the Weyl torus, $\chi=\det[h_{\lambda_i-i+j}]$, measure $\prod\lvert z_i-z_j\rvert^2$ | singlet multiplicity, numerical | `L162–199 singlet_multiplicity_torus()` | unknown (inferred: machine (spectral rectangle rule)) |
| 5 | $V_R(L)=\tfrac{g^2}2C_2(R)L$; $\sigma_R/\sigma_3=C_2(R)/C_2(3)$ (9/4 adjoint, 5/2 sextet, 9/2 decuplet) | Casimir scaling | `L213 chain_energy()`, `L222–223 casimir_scaling_table()` | unknown (inferred: exact) |
| 6 | $H=\tfrac{g^2}2\hat C_2-\tfrac\lambda2(M_F+M_F^T)$, $(M_F)_{R'R}=[R'\in F\otimes R]$, truncated $p+q\le$ cut | SU(3) character rotor | `L243–247 su3_rotor_hamiltonian()` | unknown (inferred: exact (matrix); truncation checked) |
| 7 | $s_1=\tfrac13\langle a\rvert M_F\lvert a\rangle$, $\sigma_1=-\ln s_1$ | centre order parameter | `L262–263 su3_rotor_sigma1()` | unknown (inferred: machine (eigh)) |
| 8 | $s_1\to\lambda/(2g^2)$ | first-order strong-coupling slope | `L269 su3_rotor_strong_coupling_slope()` | unknown (inferred: exact) |

**Depends on:** numpy, `fractions`. **Flags:** module's own F325 note (L56–81) states row 8's "same log law as the U(1) rotor under $\chi=1/(4g^2)$" is link-count inconsistent (1 link vs 4); the function still returns the uncorrected slope. `singlet_in_product` (L150) returns $\delta_{B,\bar A}$ by fiat — its docstring says it "verifies" via torus orthogonality, which is done by the separate function row 4.

### `engine/gauge/weak.py` — 2-D SU(2)$_L$ reference (Phase E2)
**Status:** live · driven (6 ch) · **Findings:** (registry: none) · **Lattice:** 2-D square (reference, `lattice.core.weyl_step_2d_splitstep`; D1 non-canonical) · **Law:** n/a (split-step Weyl) · **Units:** lattice

**Does:** static $W^a_0$ field rotates the left doublet $(\eta_\nu,\eta_e)$; right $\chi_e$ is untouched — parity violation demonstrator.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M=\cos(\lvert W\rvert h)I-i\sin(\lvert W\rvert h)\,\hat W\cdot\sigma$, $h=\tfrac14 g\,dt$ | half-step SU(2) phase on $\eta$ | `weak.py:L102–127 step_weak_2d()` (h L102, M L123–126) | unknown |
| 2 | kinetic `weyl_step_2d_splitstep` on $\eta_\nu,\eta_e,\chi_e$ independently | free motion | `weak.py:L139–141` | unknown (inferred: see 03-lattice.md § core.py) |
| 3 | $\eta_e'=\cos(m\,dt)\eta_e-i\sin(m\,dt)\chi_e$, $\chi_e'=-i\sin(m\,dt)\eta_e+\cos(m\,dt)\chi_e$ | electron mass mixing | `weak.py:L146–153` | unknown |
| 4 | $\theta=\tfrac12gW\,dt\,n$, $P_e=\sin^2\theta\,P_\nu(0)$ | analytic reference for the $W^1$ rotation | `weak.py:L215–217 parity_violation_test()` | unknown |

**Inputs → outputs:** 2-D spinor lists + static $W^{1,2,3}$ arrays → updated lists. **Depends on:** `lattice.core` (03-lattice.md). **Flags:** the first $W^3$ run in `parity_violation_test` (L187–190) is computed and discarded; 2-D square lattice only (reference implementation).

### `engine/gauge/weak_wmu.py` — SU(2) $W_\mu$ links, W propagation (chiral + even), Stueckelberg mass, Weinberg mixing
**Status:** live · driven (29 ch) · **Findings:** (registry: none; module cites F26 F27 F29 F35 F36 F37 F41 F44 F45 F265) · **Lattice:** BCC dispersion on cubic k-grid; links on the 8 $(\pm1,\pm1,\pm1)$ directions as integer `np.roll` shifts · **Law:** chiral for massless W (`w_propagation_step_spectral`); even for `_f26_rotation_step`, hypercharge, massive W · **Units:** lattice, $g_\text{lat}=1$

**Does:** the W-boson kernel: SU(2) Cayley–Klein links, covariant Weyl hopping for the $(\nu,e)$ doublet, the free W step (chiral), the **even rotation law `_f26_rotation_step`** that photon/Z/B/massive-W share, Yang–Mills self-interaction, Stueckelberg mass, and $W^3$–$B$ mixing.

SU(2) convention everywhere: $U=\begin{pmatrix}a&-\bar b\\ b&\bar a\end{pmatrix}$, $\lvert a\rvert^2+\lvert b\rvert^2=1$; product $(a_1,b_1)(a_2,b_2)=(a_1a_2-\bar b_1b_2,\ b_1a_2+\bar a_1b_2)$ (`L996–997 _su2_product()`).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M_d=\tfrac18\begin{pmatrix}1+is\,abc-c+is\,ab & a(c-1)-is\,b(1+c)\\ -a(1+c)+is\,b(1-c) & 1+is\,abc+c-is\,ab\end{pmatrix}$, $U_\text{BCC}(k)=\sum_d M_d e^{ik\cdot d/\sqrt3}$ | 8-term decomposition of the BCC unitary | `weak_wmu.py:L105–110 _spinor_matrix()`; check `L374–383 verify_spinor_matrix_decomp()` | unknown (docstring: <1e-14) |
| 2 | $U_\ell(x)=V(x+d)V(x)^\dagger$: $a=V_a'\bar V_a+\bar V_b'V_b,\ b=V_b'\bar V_a-\bar V_a'V_b$ | pure-gauge link init | `weak_wmu.py:L205–206 make_w_link_field()` | n/a |
| 3 | $U_\text{eff}=\sum_\ell U_\ell\big/\lVert\sum_\ell U_\ell\rVert$ | site-average re-unitarised link | `weak_wmu.py:L265–270 _u_eff_from_links()` | unknown |
| 4 | $\psi'=\mathrm{BCC}_\text{spectral}[U_\text{eff}(x)\psi(x)]$ per flavour | O(a) covariant Weyl step (norm-exact) | `weak_wmu.py:L331–339 covariant_weyl_step_3d_bcc()` | unknown (local Ward O(a), docstring) |
| 5 | $\psi'(x)=\sum_d U_d(x)\,M_d\,[\mathrm{shift}_{d/\sqrt3}\psi](x)$ | per-link covariant step; unitary only if all $U_d=I$ | `weak_wmu.py:L460–480 covariant_weyl_step_3d_bcc_exact()` | unknown |
| 6 | $U_\ell\to V(x+d)U_\ell V(x)^\dagger$ (integer roll) | local gauge transform | `weak_wmu.py:L510–527 gauge_transform_links()` | unknown |
| 7 | $U_d\to V(x)U_dV^\dagger(x+d/\sqrt3)$ (fractional FFT shift) | gauge transform matched to row 5 | `weak_wmu.py:L599–607 gauge_transform_links_kspace()` | unknown |
| 8 | $W^1=2\Im b,\ W^2=-2\Re b,\ W^3=2\Im a$, averaged over 8 links | linearised $W^a$ | `weak_wmu.py:L645–654 extract_EW_BW()` | unknown |
| 9 | **$\Omega(k)=\omega^+(k/2)+\omega^-(k/2)$; $\tilde E'=\cos\Omega\,\tilde E+\sin\Omega\,\tilde B,\ \tilde B'=-\sin\Omega\,\tilde E+\cos\Omega\,\tilde B$** | **the even (F26) rotation law** | `weak_wmu.py:L688–695 _f26_rotation_step()` | unknown (registry None); m=0 reduction bit-for-bit (inventory #127 SU(3) analog) |
| 10 | $\Omega^\pm=2\omega^\pm(k/2)$; at Nyquist planes $\Omega^+=\Omega^-=\tfrac12(\Omega^++\Omega^-)$ | chiral dispersions | `weak_wmu.py:L725–741 _chiral_dispersions()` | exact identity $\Omega^+(-k)=\Omega^-(k)$ off-Nyquist (inventory #83) |
| 11 | $F^\pm=\tilde E\pm i\tilde B$; $F^+\to e^{-i\Omega^+}F^+$, $F^-\to e^{+i\Omega^-}F^-$; $E=\Re\,\mathcal F^{-1}\tfrac12(F^++F^-)$, $B=\Re\,\mathcal F^{-1}\tfrac{-i}{2}(F^+-F^-)$ | massless W step; `w_propagation_step_spectral` is an alias | `weak_wmu.py:L912–917 w_propagation_step_chiral()`, alias `L926` | machine (inventory F37.1/.2: 2.9e-14, 2.3e-14; energy 4.6e-14) |
| 12 | $\delta W^a=g\,dt\,\epsilon^{abc}W^b\bar F^c$, $\bar F=\tfrac13(F_{xy}+F_{xz}+F_{yz})$; $R=(\cos\tfrac\theta2+i\,\delta W^3\tfrac{\sin(\theta/2)}\theta,\ (\delta W^2+i\,\delta W^1)\tfrac{\sin(\theta/2)}\theta)$, $U\to RU$ | non-Abelian self-interaction kick | `weak_wmu.py:L1158–1183 w_self_interaction_step()` | unknown |
| 13 | $F^a_{\mu\nu}$ from genuine BCC rhombus plaquettes (delegated) | field strength | `weak_wmu.py:L1036 plaquette_field_strength()` → `bcc_action.plaquette_field_strength_su2` (05a/05b) | unknown (inferred: see 05a/05b) |
| 14 | composite-SC plaquette, $F^1=\Im P_b/4g,\ F^2=\Re P_b/4g,\ F^3=\Im P_a/4g$ | **SUPERSEDED by F265** (blind to 1/3 of curvature) | `weak_wmu.py:L1124–1137 _plaquette_field_strength_composite_sc()` | n/a |
| 15 | $\max\lvert\mathcal F^{-1}[ik_zF_{xy}-ik_yF_{xz}+ik_xF_{yz}]\rvert$ | Abelian Bianchi residual | `weak_wmu.py:L1206 bianchi_residual()` | unknown |
| 16 | $J^a_\mu=\eta^\dagger\sigma^\mu\tau^a\eta$, $\eta=\begin{pmatrix}f_\nu&f_e\\g_\nu&g_e\end{pmatrix}$ | bilinear isospin current (F29) | `weak_wmu.py:L1257–1268 fermion_current_isospin()` | unknown |
| 17 | Strang kinetic(½, $\eta$ with links, sign +; $\chi$ identity links, sign −) · mass: $\eta'=\cos m\,\eta+i\sin m\,(U\otimes I)\chi$, $\chi'=i\sin m\,(U^\dagger\otimes I)\eta+\cos m\,\chi$ · kinetic(½) | Dirac doublet with W coupling on L only | `weak_wmu.py:L1296–1339 covariant_dirac_doublet_step()` | unknown |
| 18 | $m_W^\text{est}=g\sqrt{\langle\lvert\nabla U_a\rvert^2+\lvert\nabla U_b\rvert^2\rangle}$ (spectral $\nabla$); mass field $=g^2(\Im U_b,-\Re U_b,\Im U_a)$ | Stueckelberg mass estimate | `weak_wmu.py:L1403–1420 stueckelberg_mass_term()` | unknown |
| 19 | $\tilde U_{st}\to e^{-k^2dt}\tilde U_{st}$, re-unitarise; links $U\to R(\text{mass field}\cdot dt)U$ | Stueckelberg step (heat-flow, not wave) | `weak_wmu.py:L1448–1470 wmu_mass_stueckelberg()` | unknown |
| 20 | $W_\mu=e^{i a(g/2)W^a\tau^a}$: $a=\cos\theta+i\sin\theta\,n_z,\ b=\sin\theta(in_x-n_y)$, $\theta=a(g/2)\lvert W\rvert$; $V=e^{ia(g'/2)B}$ | uniform SU(2)$_L$, U(1)$_Y$ links | `weak_wmu.py:L1595–1614 make_su2_link_uniform()`, `make_u1y_link_uniform()` | n/a |
| 21 | $D_\mu U_{st}=\tfrac1a[W_\mu(x)U_{st}(x+\mu)V_\mu^\dagger(x)-U_{st}(x)]$; $\mathcal L=f^2\sum 2(\lvert A\rvert^2+\lvert B\rvert^2)$ | covariant Stueckelberg Lagrangian (F44 rank-1 mass block) | `weak_wmu.py:L1644–1660`, `L1703–1704 covariant_stueckelberg_lagrangian()` | unknown |
| 22 | $A=\cos\theta_W B+\sin\theta_W W^3,\ Z=-\sin\theta_W B+\cos\theta_W W^3$ (default $\theta_W=\pi/6$, F45) and inverse | Weinberg rotation | `weak_wmu.py:L1813–1816 weinberg_mix()`, `L1828–1831 weinberg_unmix()` | unknown (O(2) rotation, algebraically exact) |
| 23 | $Q=T^3+Y/2$ | charge | `weak_wmu.py:L1841 ew_charge()` | unknown (inferred: exact (identity)) |
| 24 | $J^1=\Re(\bar f_\nu f_e),\ J^2=\Im(\bar f_\nu f_e),\ J^3=\tfrac12(\lvert f_\nu\rvert^2-\lvert f_e\rvert^2)$ | L-doublet isospin density | `weak_wmu.py:L1870–1872 fermion_isospin_current()` | unknown |
| 25 | chiral step then $E^a\mathrel{+}=g\,J^a\,dt$ | sourced W | `weak_wmu.py:L1904–1906 w_sourced_propagation_step()` | unknown |
| 26 | $\omega_\text{eff}=\sqrt{m_W^2+\Omega_\text{even}^2}$, even rotation by $\omega_\text{eff}dt$ | massive (Proca) W | `weak_wmu.py:L1960–1969 w_massive_propagation_step_spectral()` | machine (inventory WB.4, F54-CC7) |
| 27 | hypercharge B: `_f26_rotation_step` | free U(1)$_Y$ | `weak_wmu.py:L1785 hypercharge_propagation_step()` | unknown |

**W± chirality — what the code actually does.** (a) The *fermion coupling* is left-only: in row 17 only $\eta$ (sign '+') sees the links, $\chi$ is stepped with identity links; the current row 24 uses only the upper $f$ components. There is no explicit "right-branch weight ≡ 0" parameter or $P_L$ projector object in this file — the left projection is structural (which spinor gets links). (b) The *propagator* for the massless W is the chiral law (row 11), assigning helicity $F^\pm$ to branch $\Omega^\pm$ for **all three** isospin components. (c) The massive W (row 26) uses the **even** law, not the chiral one.

**Inputs → outputs:** link lists `[(U_a,U_b)]×8`, spinor components `(Lx,Ly,Lz)` complex, W fields `(3,Lx,Ly,Lz)` real. **Depends on:** `lattice.bcc` (`bcc_dispersion`, `bcc_unitary`, `weyl_step_3d_bcc`, `bcc_fractional_shift`), `gauge.bcc_action` (05a/05b), `casim.numerics.fft/precision`; optional JAX kernels (L839–861, same formulas as rows 11 and 26 — plumbing). **Flags:** see flags table — `_f26_rotation_step` docstring says "$\Omega_\text{even}\to2c\lvert k\rvert$" (code gives $c\lvert k\rvert$); `w_massive` docstring says it reduces at $m=0$ to `w_propagation_step_spectral` (now the chiral alias; it reduces to `_f26_rotation_step`); row 12's $R_b=(\delta W^2+i\delta W^1)\sin(\theta/2)/\theta$ has the opposite $W^2$ sign from row 20's $b=\sin\theta(in_x-n_y)$ and from row 8's extraction; `measure_photon_dispersion_from_mix` (L2045) predicts $2\omega^+(k/2)$ while evolving with $\Omega_\text{even}$; CLAUDE.md's "`casim.engine.gauge.wmu._f26_rotation_step`" — no `wmu.py` exists, the function lives here.

### `engine/gauge/weak_z.py` — dynamical Z and the neutral current (FG-4)
**Status:** live · driven (6 ch) · **Findings:** (registry: none; module cites F35 F36 F45 F48) · **Lattice:** BCC dispersion on cubic k-grid · **Law:** even (all Z modes) · **Units:** lattice

**Does:** propagates a single real $(E_Z,B_Z)$ pair by the even law (massless or Proca), kicks it with the SM neutral current, and tabulates per-species Z couplings.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $g_L=T_3-Q s_W^2$ (L species; $g_L:=0$ for R species), $g_R=-Qs_W^2$, $g_V=g_L+g_R$, $g_A=g_L-g_R$ | per-species couplings | `weak_z.py:L203–221 z_couplings()` | unknown (inventory #139 cites the table at $s_W^2=1/4$ as exact) |
| 2 | $g_Z=g/\cos\theta_W$; $e=g\sin\theta_W$; $m_Z=m_W/\cos\theta_W$ | couplings and mass ratio | `weak_z.py:L242`, `L249`, `L256` | unknown (inferred: exact (closed form)) |
| 3 | $J^\text{em}=\sum_fQ^f\rho^f$, $J^3=\sum_fT_3^f\rho^f$, $J^Z=J^3-s_W^2J^\text{em}$ | neutral current | `weak_z.py:L279`, `L294`, `L315 fermion_neutral_current()` | unknown |
| 4 | $J^Z=\sum_{f_L}g_L\rho+\sum_{f_R}g_R\rho$ | per-species cross-check | `weak_z.py:L331–334` | unknown |
| 5 | `_f26_rotation_step` on $(E_Z,B_Z)$ | free massless Z | `weak_z.py:L391 z_propagation_step_spectral()` | unknown |
| 6 | $\omega_\text{eff}=\sqrt{m_Z^2+\Omega_\text{even}^2}$, rotation by $\omega_\text{eff}dt$ | Proca Z | `weak_z.py:L408–416` | unknown |
| 7 | free step then $E_Z\mathrel{+}=g_ZJ_Z\,dt$ | sourced Z | `weak_z.py:L460 z_sourced_propagation_step()` | unknown (docstring Z7 "bit-for-bit") |
| 8 | $gW^3J^3+g'B(J^\text{em}-J^3)=eAJ^\text{em}+g_ZZ(J^3-s_W^2J^\text{em})$ with $(A,Z)$ = Weinberg rotation | source-basis identity residual | `weak_z.py:L527–534 source_basis_identity_residual()` | unknown (inferred: exact when $g'=g\tan\theta_W$ (checked algebraically for this map)) |

**Z propagation — what the code does vs CLAUDE.md decision 5.** Decision 5 says "Z even for its vector part with a mass-suppressed axial split". The code applies **one even rotation to the whole Z field** (rows 5–6); there is no vector/axial decomposition of the propagator and no axial split term anywhere in this module. The Z field is a **scalar per site** `(Lx,Ly,Lz)`, not a 3-vector. The only V/A structure is in the coupling table (row 1). ⚠ DOC/CODE MISMATCH (logged).

**Inputs → outputs:** densities dict species→$\rho$; $(E_Z,B_Z)$ real arrays. **Depends on:** `weak_wmu._f26_rotation_step`, `_omega_even`, `weinberg_mix/unmix` (this file § weak_wmu). **Flags:** docstring Z10 claims $g_V=T_3-2Qs_W^2$, $g_A=T_3$ "bit-for-bit for all 7 species"; code gives $e_R$: $(g_V,g_A)=(1/4,-1/4)$ (spot-check), i.e. $(-Qs^2,+Qs^2)$, not $(-2Qs^2,0)$. `THETA_W_F45=np.pi/6` is a literal, not a registry constant (F45 value; `sin2_thetaW_onshell` is a different 2/9). `_bcc_dispersion` imported unused.

