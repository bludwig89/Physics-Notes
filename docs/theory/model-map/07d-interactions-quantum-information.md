# Interactions — quantum information (`qi_*`)

**Scope.** The sixteen `src/casim/engine/interactions/qi_*.py` modules: the $2^n$ register and its native gate set (F212/F214/F218), algorithms and error correction (F218–F222), the SI bridge (F224/F225), Bell/Tsirelson (F226), the decoherence floor (F227), measurement, the Born rule and Gleason (F281/F304/F312/F329), spin-statistics and the belt trick (F289/F330/F379), and cluster decomposition (F290/F331/F380).

**Shared conventions.**
- *Lattice.* Almost everything here is **plain finite-dimensional linear algebra on qubit registers**. There is no lattice unless one is named. The lattice appears in only four places. (i) `weyl_step_3d_bcc` (BCC, canonical) in `qi_measurement.lp_conservation_bcc` and `qi_born_gleason.momentum_block_is_not_a_context`. (ii) The BCC Dirac dispersion $\omega=\arccos(n\,u(\mathbf k))$ with F267's reciprocal generators in `qi_cluster_interacting_3d` and `qi_cluster_asymptotic_series`. (iii) `bcc._bcc_uvec` in `qi_so3_kinematic_gap`. (iv) The **2-D square** split-step Dirac walk in `qi_entanglement.hopping_amplitude`, which is a D1 reference implementation, not canonical. `qi_cluster` uses a 1-D staggered chain, and `qi_measurement` M3 uses the Cartesian block average `block_average_field` on an $L^3$ array.
- *Rotor convention.* `su2_rotor(θ, n̂)` $=\cos\theta\,\mathbb 1-i\sin\theta\,\hat n\cdot\boldsymbol\sigma=e^{-i\theta\hat n\cdot\sigma}$ is a Bloch rotation by $2\theta$. A physical rotation by $\varphi$ is `su2_rotor(φ/2, n̂)` (`qi_spin_statistics._rotor_for_physical_angle`).
- *Qubit ordering.* Qubit 0 is the most significant bit. $\hat n=(\mathbb 1-Z)/2=\lvert1\rangle\langle1\rvert$.
- *Law (F91).* No gauge propagator is stepped in this batch, so **Law: n/a** throughout. The σ-bilinear construction is never used, and the paired-spinor photon appears only as a $2\pi$-phase bookkeeping (`qi_spin_statistics` S6).
- *Units.* Lattice/dimensionless, except `qi_qc_si`, `qi_decoherence_floor` and `qi_bell_tsirelson`, which carry SI/eV. Their SI bridge is **hard-coded literals** in two of the three (see flags).
- *Numerics / D8.* The seven `origin=manifest` modules import `numpy` directly: `qi_algorithms`, `qi_bell_tsirelson`, `qi_decoherence_floor`, `qi_entanglement`, `qi_noise`, `qi_qc_si`. The spine modules use `casim.numerics.xp`, but several of them draw from `np.random.default_rng` directly rather than from `casim.numerics.rng`. No chiral transform passes through an FFT anywhere except the two cluster-3D modules. Those take a real-valued $1/(2\omega)$ through `fft.ifftn`, and only the real part is kept, which is correct because the correlator is real.
- *Exactness.* Registry `exactness` is `None` for the seven manifest modules. For those, rows are tagged from `docs/status/exactness-inventory.md` where a row names the result, and `unknown` otherwise. Several spine modules are registered `exact` although their checks are float residuals $<10^{-12}$, i.e. `machine`. Where that matters it is flagged.

**Modules covered:** `qi_algorithms`, `qi_bell_tsirelson`, `qi_belt_trick`, `qi_born_gleason`, `qi_born_nonabelian`, `qi_cluster`, `qi_cluster_asymptotic_series`, `qi_cluster_interacting_3d`, `qi_decoherence_floor`, `qi_entanglement`, `qi_gleason_regularity`, `qi_measurement`, `qi_noise`, `qi_qc_si`, `qi_so3_kinematic_gap`, `qi_spin_statistics`.

---

### `engine/interactions/qi_algorithms.py` — circuit builders (Grover, DJ, BV, QFT, GHZ)
**Status:** live · test-only · **Findings:** (registry: none; docstring F218/F219) · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** returns JSON gate-list programs (layers of `["h"|"x"|"cz"|"cnot"|"cphase"|"mcz", …]`) that `qi_entanglement.run_circuit` executes on the native gate set. Almost all of it is circuit plumbing. The equations are the textbook circuit identities.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $k_\text{opt}=\max\!\big(1,\operatorname{round}(\tfrac{\pi}{4}\sqrt{2^n/M}-\tfrac12)\big)$ | optimal Grover iteration count | `qi_algorithms.py:L92 grover_iterations()` | unknown |
| 2 | oracle $=X_\text{mask}\,\mathrm{MCZ}\,X_\text{mask}$; diffusion $=H^{\otimes n}X^{\otimes n}\,\mathrm{MCZ}\,X^{\otimes n}H^{\otimes n}$ | n-qubit Grover | `qi_algorithms.py:L108-L109 grover_nq()` | unknown |
| 3 | $f(x)=s\cdot x \bmod 2$ as CNOTs $q\to\text{anc}$ for $s_q=1$, ancilla in $\lvert-\rangle$ | Bernstein–Vazirani | `qi_algorithms.py:L127-L128 bernstein_vazirani()` | unknown |
| 4 | QFT: $H_j$ then $\mathrm{CP}(\pi/2^{k-j})_{k\to j}$ for $k>j$, then bit-reversal SWAPs (3 CNOTs each); inverse = reversed order with $\theta\to-\theta$ | QFT / QFT$^\dagger$ | `qi_algorithms.py:L150, L153, L159 qft_circuit()` | unknown |
| 5 | $P(q_0{=}1)=\lvert\psi_{10}\rvert^2+\lvert\psi_{11}\rvert^2$ | DJ readout | `qi_algorithms.py:L79 measured_bit0_probability()` | unknown |

**Inputs → outputs:** (marked item / secret / n) → (program, n). **Depends on:** `qi_entanglement` (runner, native gates; this file). **Flags:** unregistered findings (the docstring cites F218/F219, and F222 exercises the module); D8 violation: a bare `import numpy` at L77.

---

### `engine/interactions/qi_bell_tsirelson.py` — CHSH/Tsirelson on the native register (F226)
**Status:** live · test-only · **Findings:** (registry: none; docstring F226) · **Lattice:** n/a · **Law:** n/a · **Units:** SI/eV (literal bridge)

**Does:** measures CHSH on the entangled pair that the native exchange gate makes from $\lvert\uparrow\downarrow\rangle$, and bounds the lattice correction from the granularity of the analyzer angle.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $E=\langle\psi\rvert A\otimes B\lvert\psi\rangle$, $\;\sigma_{xz}(\theta)=\cos\theta\,Z+\sin\theta\,X$ | correlator, analyzer family | `qi_bell_tsirelson.py:L84 correlator()`, `L79 sigma_xz()` | unknown (inferred: machine) |
| 2 | $S=E(a,b)-E(a,b')+E(a',b)+E(a',b')$ | CHSH | `qi_bell_tsirelson.py:L91-L92 chsh_value()` | unknown (inferred: machine) |
| 3 | $S_\text{max}=2\sqrt{t_1+t_2}$, $t_i$ = two largest eigenvalues of $T^\mathsf TT$, $T_{ij}=\langle\sigma_i\otimes\sigma_j\rangle$ | Horodecki optimum (native state gives $2\sqrt2$) | `qi_bell_tsirelson.py:L104-L105 chsh_max_horodecki()` | exact (inv. 15a: $1.8\times10^{-15}$, i.e. machine residual) |
| 4 | $\lvert\psi\rangle=U_\text{exch}(\pi/8)\lvert\uparrow\downarrow\rangle$ | native entangled pair | `qi_bell_tsirelson.py:L118 native_entangled_pair()` | unknown (inferred: machine) |
| 5 | code: $S(\varphi)$ at $(a,a',b,b')=(0,2\varphi,\varphi,3\varphi)$ on $\lvert\Psi^-\rangle$ evaluates to $-(3\cos\varphi-\cos3\varphi)$ | one-parameter Bell family | `qi_bell_tsirelson.py:L134 chsh_singlet_of_phi()` | unknown (inferred: machine) |
| 6 | $\lvert S(\pi/4+\delta)\rvert\approx2\sqrt2-3\sqrt2\,\delta^2$ (coefficient returned as the literal $-3\sqrt2$) | stationary curvature | `qi_bell_tsirelson.py:L142 dS_quadratic_coeff()` | exact (inv. 15b; curvature $-4.25$ vs $-4.243$) |
| 7 | $\delta\varphi=E/E_\text{lat}$, $E_\text{lat}=\hbar/\tau$ | angle granularity per Planckian tick | `qi_bell_tsirelson.py:L150 angle_granularity()`; `L63 E_LAT_EV` | unknown |
| 8 | $\lvert\delta S\rvert\le3\sqrt2\,(E/E_\text{lat})^2$ ($1.3\times10^{-54}$ at 1.8 eV) | discreteness correction | `qi_bell_tsirelson.py:L158 dS_from_discreteness()` | unknown |
| 9 | $\max_{U_A}\lvert\langle\Psi^-\rvert U_A\otimes\mathbb 1\lvert\psi\rangle\rvert^2=(\sum_i s_i)^2$, with $s$ the singular values of $\psi_{2\times2}\Psi^{-\dagger}_{2\times2}$ | native pair = singlet up to a local unitary | `qi_bell_tsirelson.py:L187-L190 native_equals_singlet_up_to_local()` | unknown (inferred: machine) |

**Inputs → outputs:** analyzer angles / $E$ [eV] → $S$, $\delta S$. **Depends on:** `qi_entanglement` (`exchange_gate`, `Register`). **Flags:**
- ⚠ DOC/CODE MISMATCH at L131-L134: the docstring says $S(\varphi)=3\cos\varphi-\cos3\varphi$ with max $2\sqrt2$. The code returns the negative, $S(\pi/4)=-2\sqrt2$, because the singlet has $E=-\cos$. The magnitude and the curvature coefficient are unaffected.
- SI literals $\tau=2.05366\times10^{-43}$ s, $a=1.06638\times10^{-34}$ m and $\hbar$ in eV·s (L60-L62) are hard-coded rather than taken from `casim.constants` (`a_over_ellP`, F79/F107). $\tau$ matches $a/(c\sqrt3)$ to 6 sf.
- D8: bare `numpy`.
- Findings are not registered.

---

### `engine/interactions/qi_belt_trick.py` — belt-trick residual, spin-½ pair (F330)
**Status:** live · standalone · **Findings:** F330 F289 F291 F292 F26 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** checks, on the model's own rotor, the representation facts behind Anastopoulos's Postulate 1 for a spin-½ pair. The singlet is a scalar. The triplet is invariant but not scalar at $\theta=\pi$. Two exchanges give the identity via F289's $R(2\pi)=-1$. The module states that it does **not** derive Postulate 1.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\lvert S\rangle=(\lvert\uparrow\downarrow\rangle-\lvert\downarrow\uparrow\rangle)/\sqrt2$; control $\lvert T_0\rangle$ with the $+$ sign | two-spin states | `qi_belt_trick.py:L132-L133, L141-L142` | exact (reg) |
| 2 | $M(\theta,\hat n)=R_\text{phys}(\theta,\hat n)^{\otimes2}$, $R_\text{phys}(\theta)=$ `su2_rotor(θ/2)` | diagonal rigid rotation | `qi_belt_trick.py:L155-L156 _diagonal_rotor()` | exact (reg) |
| 3 | leak $=\lVert M\lvert S\rangle-\langle S\rvert M\lvert S\rangle\lvert S\rangle\rVert=0$ and $\langle S\rvert M\lvert S\rangle=1$ over 12 Fibonacci axes × 12 angles | B1 singlet scalar | `qi_belt_trick.py:L199-L202 singlet_invariance_sweep()` | exact (reg) |
| 4 | $M_\text{sub}=B^\dagger MB$ on $\{\lvert{+}{+}\rangle,\lvert T_0\rangle,\lvert{-}{-}\rangle\}$; dev $=\lVert M_\text{sub}-\tfrac13\operatorname{tr}M_\text{sub}\,\mathbb 1\rVert_F$; at $\theta=\pi$: eigenvalues $\{-1,+1,-1\}$, dev $=2\sqrt6/3=1.633$ | B2 triplet not scalar | `qi_belt_trick.py:L245-L253 triplet_scalar_deviation()` | exact (reg) |
| 5 | $\lVert M(\pi)^2-\mathbb 1_4\rVert$ alongside F289's $\lVert R(2\pi)+\mathbb 1\rVert$ | B3 two exchanges = identity | `qi_belt_trick.py:L284-L286 exchange_squared_is_f289_r2pi()` | exact (reg) |

**Inputs → outputs:** (`theta_exchange`, `wrong_singlet`) → check rows. **Depends on:** `qi_spin_statistics._rotor_for_physical_angle`, `rotor_2pi_phase` (this file). **Flags:**
- ⚠ DOC/CODE MISMATCH at L218-L219: the docstring says the deviation at $\theta=\pi$ is "exactly $2/\sqrt3$ × the identity-normalised scale". The code's Frobenius norm is $2\sqrt6/3\approx1.633$ (spot-checked).
- EXACTNESS: registered `exact`, but every leg is a float residual with a $10^{-12}$ threshold, i.e. machine.
- Under the $\theta_\text{exchange}=2\pi$ control, B3 still passes, because $R(4\pi)^{\otimes2}=\mathbb 1$. Only B2 carries that control.

---

### `engine/interactions/qi_born_gleason.py` — Born rule via Gleason, premises forced (F304)
**Status:** live · standalone · **Findings:** F304 F281 F290 F227 F87 F41 · **Lattice:** BCC (B1c and B6b only; the rest is abstract $\mathbb C^d$) · **Law:** n/a · **Units:** n/a

**Does:** argues that the two premises of Gleason's theorem are properties of the rule in this model: dimension $\ge3$ because a record needs environment cells, and non-contextuality because the record generator is a fixed minimal coupling. It then proves the frame-function dichotomy for $f\in L^2$ with the zonal-eigenvalue formula.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $H_\text{int}=\sum_{x,j}g_{xj}\,\hat n_x Z_j$, $\;g_{xj}=0.71+0.23x+0.46j+0.07xj$ | model's minimal-coupling record generator | `qi_born_gleason.py:L198 minimal_record_generator()`; `L179 _couplings()` | exact (reg) |
| 2 | control: $H=\sum_k(1+0.7k)g_{0j}\,(U^\dagger P_kU)\otimes Z_j$ | basis-referencing (contextual) generator | `qi_born_gleason.py:L215-L218 contextual_record_generator()` | exact (reg) |
| 3 | $\dim\{X:[X,\hat n_x]=0\;\forall x\}=d^2-\operatorname{rank}\big[\hat n_x\otimes\mathbb 1-\mathbb 1\otimes\hat n_x^\mathsf T\big]=2^{n}$ | B1a pointer algebra maximal abelian | `qi_born_gleason.py:L233-L239 pointer_commutant_dimension()` | exact (inv. #159-165 family) |
| 4 | $\lvert D(t)\rvert=\prod_j\lvert\cos g_jt\rvert$; empty product $=1$ ⇒ minimum measurement dimension 4 | B1b | `qi_born_gleason.py:L253-L260 record_requires_environment()` | exact (reg) |
| 5 | one `weyl_step_3d_bcc` tick keeps a plane wave in its $\mathbf k$ block (leakage $\to0$); $\lVert[\Pi_\mathbf k,\hat n(x)]\rVert_F=\sqrt{2/N-2/N^2}$ | B1c momentum blocks are invariant but not contexts | `qi_born_gleason.py:L291-L296, L299, L305 momentum_block_is_not_a_context()` | exact (inv. #223) |
| 6 | $w(v)=\lVert\big(e^{-iH_\text{int}t}\,(U\psi_S\otimes\lvert+\rangle^{\otimes n_e})\big)_{0,\cdot}\rVert^2$, $U=Q^\dagger$, $Q_{:,0}=v$ | record weight of ray $v$ in a context | `qi_born_gleason.py:L346-L358 record_for_ray()` | machine (reg: exact; row is weaker — see flags) |
| 7 | spread of $w$ and record infidelity over 5 contexts sharing $v$ | B2a/B2b context-blindness | `qi_born_gleason.py:L381-L382 context_blindness()` | exact (inv. #224; literal 0.0) |
| 8 | $\rho_B$ unchanged under $U_A\otimes\mathbb 1$ on 6 cells; control adds $0.9\,g\,\hat n_A Z_{B\text{-env}}$ | B3a remote context = no-signalling | `qi_born_gleason.py:L436-L443, L461 remote_context_invariance()` | machine (reg: exact; row is weaker — see flags) |
| 9 | $f(v)=\tfrac12+\epsilon P_3(\hat z\cdot\mathbf b(v))$, $P_3=(5z^3-3z)/2$ | B4a $d=2$ non-Born frame function | `qi_born_gleason.py:L481, L490 d2_frame_function()` | machine (reg: exact; row is weaker — see flags) |
| 10 | spread of $\sum_{v\in\text{triad}}f_3(v)$ for the lifted $P_3$ family | B4b fails at $d=3$ | `qi_born_gleason.py:L556-L561 d3_hole_closes()` | quantitative (reg: exact; row is weaker — see flags) |
| 11 | $\dim\{\text{degree-}\deg\text{ frame fns}\}=K^2-\operatorname{rank}A$; $d\ge3$: $d^2$; $d=2$: $1+\sum_{\ell\text{ odd}\le\deg}(2\ell+1)$ | B5a/B5b dichotomy (rank measurement) | `qi_born_gleason.py:L618-L620 frame_function_space_dimension()`; `L652 gleason_dichotomy()` | exact (integer; inv. #225/#226) |
| 12 | $b_k=(-1)^k/\binom{k+d-2}{k}$ (`Fraction`); control $(-1)^k/(d-1)^k$ | zonal eigenvalue of the averaging operator $B$ | `qi_born_gleason.py:L735 zonal_eigenvalue()` | exact (inv. #227) |
| 13 | $\dim V_k=\binom{k+d-1}{k}^2-\binom{k+d-2}{k-1}^2$ | isotypic dimension in $L^2(\mathbb{CP}^{d-1})$ | `qi_born_gleason.py:L742 dim_isotypic()` | exact (reg) |
| 14 | $f+(d-1)Bf=W$; $B$ built from $P_{\mathrm{Sym}^k(v^\perp)}/\binom{k+d-2}{k}$; spectrum vs $\{b_j\}$ with multiplicity $\dim V_j$ | B7a operator spectrum | `qi_born_gleason.py:L795, L801-L802 averaging_operator_spectrum()` | exact (integers) + machine (inv. #229) |
| 15 | $1+(d-1)b_k=0$ iff ($d=2$, $k$ odd) or $k=1$; strict gap $\ge0.5$ for $d\ge3,k\ge2$ | B7b/c/d selection rule, exact rationals | `qi_born_gleason.py:L832 frame_selection_exact()` | exact (inv. #228) |
| 16 | $d=2$: $1+\sum_{k\text{ odd}\le\deg}\dim V_k$; $d\ge3$: $1+\dim V_1=d^2$ | B7e proof predicts B5 | `qi_born_gleason.py:L885, L890 proof_predicts_the_measurements()` | exact (inv. #230) |
| 17 | $\lvert w(v)-\lvert\langle v\vert\psi\rangle\rvert^2\rvert$ | B6a Born value on a lattice state | `qi_born_gleason.py:L915-L916 born_value_on_lattice_state()` | machine (reg: exact; row is weaker — see flags) |
| 18 | $\ell^2$ change $=0$, other $\ell^p$ change $>10^{-3}$ under one BCC tick (via `qi_measurement.lp_conservation_bcc`) | B6b F281 leg 1 as a corollary | `qi_born_gleason.py:L930-L941 l2_conservation_corollary()` | exact (inv. #156) |

**Inputs → outputs:** (`coupling`, `locality`, `gleason_dim`, `zonal`) → 21 check rows. **Depends on:** `lattice/bcc.py weyl_step_3d_bcc` (see 03-lattice.md § bcc.py), `casim.numerics.fft` (see 02-numerics.md), `qi_measurement`. **Flags:**
- B6a (row 17) is close to true by construction. $H_\text{int}$ commutes with $\hat n$, so the pointer-slot-0 population is conserved and equals $\lvert(Q^\dagger\psi_S)_0\rvert^2=\lvert\langle v\vert\psi_S\rangle\rvert^2$ whatever the dynamics.
- B1b hard-codes `min_measurement_dim: 4` and `gleason_dimension_premise_met: True` (L259-L260). Only the empty-product 1 is computed.
- D8: `np.random.default_rng` is used directly (L322, L453, L522, L546, L614, L784) instead of `casim.numerics.rng`.

---

### `engine/interactions/qi_born_nonabelian.py` — Gleason premises on SU(2)_L and SU(3)_c (F312)
**Status:** live · standalone · **Findings:** F312 · **Lattice:** n/a (abstract sites $\otimes$ internal $\mathbb C^N$) · **Law:** n/a · **Units:** n/a

**Does:** extends F304's non-contextuality premise to the non-Abelian gauge factors. It checks the intra-site current algebra, that the occupation record is a gauge singlet, context-blindness with an internal factor present, and the Casimir "Schur reduction".

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $T^a=\sigma^a/2$ (SU(2)), $T^a=\lambda^a/2$ (SU(3), `gell_mann()`) | generators | `qi_born_nonabelian.py:L144-L145` | exact (reg) |
| 2 | $f^{abc}=\operatorname{Re}\big(-2i\operatorname{Tr}([T^a,T^b]T^c)\big)$ | structure constants | `qi_born_nonabelian.py:L166 structure_constants()` | exact (reg) |
| 3 | $[J^a(x),J^b(y)]=i\delta_{xy}f^{abc}J^c(x)$; off-site commutator $=0$; $f$ antisymmetric; SU(2): $f=\epsilon$; SU(3): $f_{123}=1$, $f_{458}=\sqrt3/2$ | G1/G2 current algebra | `qi_born_nonabelian.py:L191-L193, L211-L216 current_algebra()` | exact (reg) |
| 4 | $[J^a(x),\hat n(y)]=0$, $\hat n=\operatorname{diag}(1,\dots,1)$ (trace over colour); control $\operatorname{diag}(1,2,\dots,N)$ | G3 singlet record | `qi_born_nonabelian.py:L253, L266 record_is_a_singlet()` | exact (reg) |
| 5 | $H=H_\text{rec}\otimes\mathbb 1_V+\sum_a g_a\,(\mathbb 1_p\otimes\mathbb 1_e\otimes T^a)$, $g_a=0.37+0.11a$; weight spread over 5 contexts | G4/G5 context-blindness | `qi_born_nonabelian.py:L317, L323, L332-L339 context_blindness_with_internal()` | machine (reg: exact; row is weaker — see flags) |
| 6 | $C_2=\sum_aT^aT^a=\tfrac{N^2-1}{2N}\mathbb 1$ | G6 Casimir scalar | `qi_born_nonabelian.py:L374-L377 schur_reduction()` | exact (reg) |
| 7 | $\dim=d_p N$: $N$ alone, $2N$ with the minimal record | G7 dimension premise | `qi_born_nonabelian.py:L409-L412 dimension_premise()` | exact (reg) |
| 8 | $U=e^{i\theta_aT^a}$; $U(a c_1+b c_2)=aUc_1+bUc_2$; $U^\dagger U=\mathbb 1$ | G8 linearity/unitarity on $V$ | `qi_born_nonabelian.py:L437-L439, L450-L457 superposition_on_internal()` | machine (reg: exact; row is weaker — see flags) |
| 9 | $\chi^\dagger\mathbb 1\chi$ before vs after $U$ | G9 gauge rotation is not a context | `qi_born_nonabelian.py:L488-L490 gauge_rotation_is_not_a_context()` | machine (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** (`abelian_control`, `break_singlet`, `contextual_coupling`) → check dict. **Depends on:** `core/lpt_generator.gell_mann` (04-core.md), `qi_born_gleason`. **Flags:**
- G7 hard-codes `d2_hole_reachable_in_a_charged_sector: False` (L417). The check `G7-no-hole` reads that literal, so it cannot fail.
- G9 is vacuous as coded. The record operator is the identity (L483), so "weight change" is just norm preservation under a unitary.
- G6 verifies $C_2\propto\mathbb 1$ only. The docstring calls this "the whole general theorem" (frame function factorises $f_p(v)\cdot c$), but that factorisation is not computed anywhere.
- The gate uses `assert` (L527-L571). A declared control therefore raises `AssertionError` instead of returning a red row.
- The G4/G5 gauge term is $\mathbb 1_p\otimes\mathbb 1_e\otimes\sum g_aT^a$, which commutes with everything on the pointer side by construction.

---

### `engine/interactions/qi_cluster.py` — no-signalling, strict cone, 1-D clustering (F290)
**Status:** live · standalone · **Findings:** F290 F227 F226 F212 F281 · **Lattice:** 1-D chain (qubit brick-wall; staggered-mass fermion chain), not BCC · **Law:** n/a · **Units:** lattice

**Does:** C1 is exact no-signalling under local unitaries. C2 is a strict brick-wall light cone of the native exchange gate. C3 is exponential clustering $\xi\sim\Delta^{-1}$ on the 1-D staggered chain, with the gapless point as a power-law control.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\rho_B=M^\dagger M$, $M=\psi_{2^{n_A}\times2^{n_B}}$ | partial trace | `qi_cluster.py:L79-L80 reduced_state()` | machine (reg) (row read: exact) |
| 2 | $\max\lVert\rho_B[(U_A\otimes\mathbb 1)\psi]-\rho_B[\psi]\rVert$ over 12 local rotors × 3 states | C1 no-signalling | `qi_cluster.py:L132-L134 no_signalling_residual()` | machine (reg) |
| 3 | control: $U_\text{exch}(\pi/8)$ across the cut moves $\rho_B$ | C1b | `qi_cluster.py:L155-L157 nonlocal_control_moves_rho_B()` | machine (reg) |
| 4 | $r_\text{cone}(t)=t$ per brick-wall layer (1 site/layer; 2 per full tick; F227's $4t$ = 2 offsets × 2 evolved operators) | cone radius | `qi_cluster.py:L180 cone_radius()`; `L249-L253 cone_convention_check()` | machine (reg) (row read: exact) |
| 5 | $\Delta\rho_r=\lVert\rho_r^\text{kick}-\rho_r\rVert$, Néel start, kick $=R(\pi/3,\hat x)$, layers of $U_\text{exch}(\pi/16)$ | C2 operational cone scan | `qi_cluster.py:L221-L226 operational_cone_scan()` | machine (reg) |
| 6 | $C\,e^{-(r-vt)/\xi}$ with $v=2,\xi=C=1$ | generic Lieb–Robinson comparison | `qi_cluster.py:L264 lieb_robinson_bound()` | n/a (illustrative) |
| 7 | $H=-t\sum(c_i^\dagger c_{i+1}+\text{h.c.})+m\sum(-1)^in_i$; $G_{ij}=\langle c_i^\dagger c_j\rangle$ from the filled lower band; $\Delta=2m$, $v=2t$ | staggered Dirac chain | `qi_cluster.py:L279-L293 staggered_chain_correlations()` | machine (reg) |
| 8 | $\ln\lvert C(r)\rvert=a-r/\xi$ (one sublattice), $\ln\lvert C\rvert=a-p\ln r$ | fits | `qi_cluster.py:L318-L323 _fit_exponential()`, `L338-L343 _fit_powerlaw()` | fit |
| 9 | $\log\xi$ vs $\log\Delta$ slope (measured $\approx-0.93$, continuum $-1$) | C3b $\xi\sim\Delta^{-1}$ | `qi_cluster.py:L387 correlation_length_vs_gap()` | quantitative (fit) (reg: machine; row is weaker — see flags) |

**Inputs → outputs:** (`locality`, `cone_slack`, `mass`) → check rows. **Depends on:** `qi_entanglement` (`su2_rotor`, `exchange_gate`). **Flags:**
- ⚠ DOC/CODE MISMATCH, module docstring L39-L41 vs `correlation_length_vs_gap` L352-L364. The header says "$\xi\Delta\sim v$ … the correlation length is not fitted, it is the gap". The code fits a log–log exponent ($-0.93$) and itself reports that $\xi\Delta/v$ drifts about 30%.
- ⚠ DOC/CODE MISMATCH at L430-L431: the `cone_slack=-1` control docstring says it "pins the cone radius to 2t". `cone_radius` is $r\le t$ per layer.
- Hardwired controls. The `mass=0` branch appends C3b/C3d as literal `False` (L499-L500). The `locality=nonlocal` branch reuses the C1b control rather than perturbing C1's own computation.
- The registry says `machine` while C3/C3b are fits (quantitative).

---

### `engine/interactions/qi_cluster_asymptotic_series.py` — F331's residual as one prefactor power (F380)
**Status:** live · standalone · **Findings:** F380 F331 F290 · **Lattice:** BCC (through F331's correlator) · **Law:** n/a · **Units:** lattice

**Does:** re-expresses the mass-dependent ratio $\kappa_\text{meas}/\kappa_\text{exact}$ from F331 as the OLS bias of an omitted $-p\ln r$ prefactor. It tests that the implied $p_\text{eff}$ is mass-independent and close to the theoretical $p=3/2$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $w=S_{r,\ln r}/S_{rr}$ over F331's adaptive window, $r=i\cdot4/\sqrt3$ | exact OLS bias weight | `qi_cluster_asymptotic_series.py:L156-L162 _ols_bias_weight()` | quantitative (reg) (row read: exact (algebra)) |
| 2 | $p_\text{eff}(m)=(\kappa_\text{meas}-\kappa_\text{ref})/w$; ref $=\kappa_{100}$ (control: $\kappa_{110}$) | implied prefactor power | `qi_cluster_asymptotic_series.py:L180 effective_power()` | quantitative (reg) |
| 3 | $p_\text{th}=1+\tfrac12=\tfrac32$ (transverse Gaussian $r^{-1}$ + axial $\omega\sim\sqrt{2\epsilon}$ branch point $r^{-1/2}$) | theoretical power (literal) | `qi_cluster_asymptotic_series.py:L146 THEORY_POWER` | quantitative (reg) (row read: exact (as asserted; derivation is in the docstring, not in the code)) |
| 4 | C1: $\sigma_p/\bar p<5\%$ over $m=0.05..0.90$; C2: $\lvert\bar p-\tfrac32\rvert/\tfrac32<5\%$; C3: $z(m^*)<3$ at the NJL mass | gate | `qi_cluster_asymptotic_series.py:L213-L231 check_named_residual_K()` | quantitative (reg) |

**Inputs → outputs:** (`reference`, `g_above_gc`, `L=256`) → checks + summary. **Depends on:** `qi_cluster_interacting_3d` (this file). **Flags:**
- $p=3/2$ is a hard-coded literal (L146) compared against a measurement. The Watson's-lemma/branch-point derivation is prose only. The module's own docstring states the PARTIAL, not MACHINE, status.
- The docstring's result numbers (1.489 ± 0.039, 0.71%, spread 2.65%) are quoted results; they were not re-run here.
- The literal `_STEP_PHYS = 4/ROOT3` duplicates `_AXIS100_STEP_PHYS`.

---

### `engine/interactions/qi_cluster_interacting_3d.py` — 3-D BCC clustering, free and NJL-interacting (F331)
**Status:** live · standalone · **Findings:** F331 F290 F267 F77 F26 · **Lattice:** BCC (true reciprocal generators, F267) · **Law:** n/a (massive Dirac dispersion, `'+'` branch) · **Units:** lattice

**Does:** has two pieces. The first is the closed-form (100)-axis decay rate of the free massive BCC Dirac equal-time correlator, validated by an oblique-grid FFT. The second is a lattice-native NJL mean-field gap equation whose dynamical mass $m^*$ sets a finite correlation length.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\sqrt3=1/c_\text{lat}$, $c_\text{lat}=1/\sqrt3$ (F26) | constant | `qi_cluster_interacting_3d.py:L104 ROOT3` | quantitative (reg) (row read: exact) |
| 2 | $\omega(\mathbf k)=\arccos\big(n\,u(\mathbf k)\big)$, $n=\sqrt{1-m^2}$, $u=c_xc_yc_z+s_xs_ys_z$ at argument $k_i/\sqrt3$ | BCC Dirac dispersion (imported) | `particles/dirac_bcc.py:L92 bcc_dirac_dispersion()`; `lattice/bcc.py:L107 _bcc_uvec()` | quantitative (reg) (row read: exact) |
| 3 | $\kappa_{100}(m)=\sqrt3\,\operatorname{arccosh}\!\big(1/\sqrt{1-m^2}\big)\;\to\sqrt3\,m$ for $m\to0$ | (100)-axis decay rate (max of $R^2=xy+(1-x)(1-y)$ at the corner) | `qi_cluster_interacting_3d.py:L157-L158 axis100_kappa_exact()` | quantitative (reg) (row read: exact (registry says quantitative; the closed form is exact)) |
| 4 | $\kappa_{110}(m)=\sqrt3\,\operatorname{arccosh}\!\big((1-m^2)^{-1/4}\big)$ | (110) companion, not numerically validated | `qi_cluster_interacting_3d.py:L173-L174 axis110_kappa_exact()` | quantitative (reg) (row read: unknown) |
| 5 | $\mathbf k(p,q,s)=\tfrac pL\mathbf g_1+\tfrac qL\mathbf g_2+\tfrac sL\mathbf g_3$, $\mathbf g_i=\sqrt3\pi\{(1,1,0),(1,0,1),(0,1,1)\}$ | oblique BZ grid (F267) | `qi_cluster_interacting_3d.py:L200-L202 _oblique_kgrid()` | quantitative (reg) (row read: exact) |
| 6 | $G(\mathbf r)=\mathrm{IFFT}[1/(2\omega)]$; (100) axis $=$ diagonal $n_1=n_2=t$, even $t$ only, $4/\sqrt3$ per kept step | equal-time correlator along (100) | `qi_cluster_interacting_3d.py:L227-L237 axis100_correlator_diagonal()`; `L110 _AXIS100_STEP_PHYS` | quantitative (reg) (row read: machine) |
| 7 | $\ln\lvert C\rvert=a-\kappa r$ on the window $[\lceil2.5/k_d\rceil,\ \min(\text{lo}+\lceil10/k_d\rceil,\ L/5,\ \lfloor25/k_d\rfloor))$, $k_d=\kappa\cdot$step | fitted decay (window scaled to $\xi$) | `qi_cluster_interacting_3d.py:L250-L252 _fit_kappa()`; `L279-L289 _adaptive_window()` | fit |
| 8 | $I_1^\text{lat}(m)=\big\langle1/(2\omega(\mathbf k,m))\big\rangle_\text{fund. domain, MC}$; $I_1^\text{lat}(1)=1/\pi$ exactly ($\omega\equiv\pi/2$) | NJL tadpole, finite-BZ regulated | `qi_cluster_interacting_3d.py:L353-L354 lattice_njl_I1()`; MC points `L330-L331` | quantitative (reg) |
| 9 | $1=g\,I_1^\text{lat}(m^*)$, bisection on $(10^{-4},1-10^{-4})$; nontrivial only for $g\in(g_c,\pi)$, $g_c=1/I_1^\text{lat}(0)\approx2.637$ | self-consistent dynamical mass | `qi_cluster_interacting_3d.py:L382-L397 solve_gap_equation()` | quantitative (reg) |
| 10 | C1: $\lvert\kappa_\text{meas}/\kappa_{100}-1\rvert<0.35$; C3: the same at $m^*$ | clustering gates | `qi_cluster_interacting_3d.py:L441, L469-L470 check_cluster_interacting_3d()` | quantitative (reg) |

**Inputs → outputs:** (`use_correct_bz`, $g$, $m$, $L$, `n_mc`, `seed`) → checks + summary. **Depends on:** `lattice/derive_walk_bz_measure.WALK_RECIPROCAL_GENERATORS`, `particles/dirac_bcc.bcc_dirac_dispersion` (03-lattice.md, 06b-particles-*.md), `casim.numerics.fft/rng` (02-numerics.md), constant `c_lat` (01-constants.md). **Flags:**
- ⚠ DOC/CODE MISMATCH, module docstring L86-L90 (C3 control). It says that below $g_c$ "the correlator does NOT decay exponentially". The code sets `ok3 = False` without computing any correlator (L472-L475).
- `_naive_cube_kgrid` (control) is the simple-cubic reference grid by design (the F267 hazard).
- The `1e-300` floor is added inside the log fit (L247).

---

### `engine/interactions/qi_decoherence_floor.py` — intrinsic decoherence floor and QC light cone (F227)
**Status:** live · test-only · **Findings:** (registry: none; docstring F227, F130, F26/F180) · **Lattice:** 1-D qubit chain (brick-wall) · **Law:** n/a · **Units:** eV / s (literal SI bridge)

**Does:** bounds any intrinsic non-unitarity by Planck-suppressed LIV rates, shows the strict brick-wall causal cone of the native exchange gate, and compares these against collapse models, clock/transmon coherence, and emergent doublon leakage.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $E_\text{lat}=\hbar/\tau$ (literals $\tau=2.05366\times10^{-43}$ s, $\hbar$ in eV·s) | lattice energy | `qi_decoherence_floor.py:L63 E_LAT_EV` | unknown |
| 2 | $\Gamma_\text{LIV}\lesssim(E/\hbar)(E/E_\text{lat})^2$ | leading-LIV rate (F130 $n=2$) | `qi_decoherence_floor.py:L84 intrinsic_rate_liv()` | unknown |
| 3 | $\Gamma_\text{cons}\lesssim E^2/(\hbar E_\text{lat})$ | pessimistic single-power ceiling | `qi_decoherence_floor.py:L90 intrinsic_rate_conservative()` | unknown |
| 4 | "slope" $=[\Omega(dk)-\Omega(0)]/dk$ with $\Omega(k)=k/\sqrt3$ hard-coded | claims $d\Omega/dk=c_\text{lat}$ | `qi_decoherence_floor.py:L108-L109 fundamental_dispersion_slope()` | exact (inv. 15c), but tautological |
| 5 | $C(r,t)=\langle Z_0Z_r\rangle-\langle Z_0\rangle\langle Z_r\rangle=0$ for $r>4t$; Néel start, $U_\text{exch}(\pi/16)$ brick-wall | strict Lieb–Robinson cone | `qi_decoherence_floor.py:L141-L155 exchange_chain_lightcone()` | machine (inv. 15d) |
| 6 | $\log_{10}$ ratios of $\Gamma$ vs $1/T_\text{clock}$, $1/T_2^\text{transmon}$, $\lambda_\text{CSL}$ | confrontation table | `qi_decoherence_floor.py:L164-L186 confront_experiment()` | unknown |
| 7 | $d=(2t/U)^2$; per-gate floor $\Gamma_\text{LIV}\,\hbar/E$ | doublon leakage vs fundamental floor | `qi_decoherence_floor.py:L196 doublon_leakage()`; `L203-L208 floor_vs_leakage_separation()` | unknown |

**Inputs → outputs:** $E$ [eV], $t/U$ → rates and orders of magnitude; chain size → cone fronts. **Depends on:** `qi_entanglement`; constant `c_lat=1/\sqrt3` (F26, recorded Site). **Flags:**
- Row 4 cannot fail. It differentiates the literal $k/\sqrt3$, not the model's dispersion, and uses the literal `math.sqrt(3.0)` instead of `c_lat` (L108).
- The SI literals $\tau$, $a$, $\hbar$, $E_P$ (L60-L64) are unregistered duplicates of `casim.constants` values (F79/F107 ruler).
- Experimental references (CSL, clock, transmon) are literals.
- D8: bare `numpy`.
- Findings are not registered.

---

### `engine/interactions/qi_entanglement.py` — genuine $2^n$ register, native gates, super-exchange (F212/F214/F218)
**Status:** live · driven (5 ch) · **Findings:** (registry: none; docstring F212, F214, F218, F26) · **Lattice:** none for the register; **2-D square** Dirac walk (D1 reference) in `hopping_amplitude` · **Law:** n/a · **Units:** lattice

**Does:** the dense state-vector register and gate application. It supplies the model's native primitives (the SU(2) rotor and the exchange entangler), the exact compilation of H/CZ/CNOT/CPhase/CCZ, the super-exchange coupling taken from Dirac hopping, and the circuit runner that the live channels use.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $R(\theta,\hat n)=\cos\theta\,\mathbb 1-i\sin\theta\,\hat n\cdot\boldsymbol\sigma=e^{-i\theta\hat n\cdot\sigma}$ | single-cell rotor (Bloch angle $2\theta$) | `qi_entanglement.py:L82 su2_rotor()` | unknown (inferred: exact) |
| 2 | $U_\text{exch}(\theta)=e^{-i\theta\,\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}=e^{-i\theta}P_T+e^{3i\theta}P_S$ (via `eigh`) | two-cell entangler | `qi_entanglement.py:L96-L97 exchange_gate()` | unknown (inferred: machine) |
| 3 | $\mathrm{SWAP}=\tfrac12(\mathbb 1+\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B)$ | permutation point | `qi_entanglement.py:L104 swap_gate()` | exact (inv. 242) |
| 4 | $\lvert\psi\rangle=\bigotimes_i\lvert c_i\rangle$; op on targets via transpose/reshape; $\rho_\text{keep}=MM^\dagger$; $S=-\sum\lambda\ln\lambda$ ($\lambda>10^{-15}$) | register, gate application, reduced state, entropy | `qi_entanglement.py:L121-L125, L128-L142, L159, L166 Register`; flat versions `L266-L296` | unknown (inferred: machine) |
| 5 | $\lvert\uparrow\downarrow\rangle\xrightarrow{U_\text{exch}(\pi/8)}S=\ln2$ | perfect entangler | `qi_entanglement.py:L236-L238 is_perfect_entangler_demo()` | machine (inv. 240) |
| 6 | $\lambda_\text{max}=\sigma_\text{max}^2$ of $\psi_{d_A\times d_B}$ | best product fidelity (mean-field limit) | `qi_entanglement.py:L184-L187 best_product_fidelity()` | exact (inv. 241: ½ on Bell) |
| 7 | step $U_\text{exch}(\theta/N)$, then rank-1 SVD projection | Hartree-constrained evolution (keeps $S\approx0$) | `qi_entanglement.py:L203-L210 meanfield_evolve_2q()` | unknown (inferred: machine) |
| 8 | $t(m)=\tfrac14\sum_\text{nn}\big(\lvert e_\uparrow\rvert+\lvert e_\downarrow\rvert+\lvert c_\uparrow\rvert+\lvert c_\downarrow\rvert\big)$ after one `dirac_step_2d_splitstep` tick from a point source | hopping amplitude | `qi_entanglement.py:L327-L331 hopping_amplitude()` | unknown |
| 9 | $U(m)=2\arcsin m$ | double-occupancy gap $=2\omega(k{=}0)$ | `qi_entanglement.py:L337 mass_gap()` | unknown |
| 10 | $J=\tfrac12\big(\sqrt{U^2+16t^2}-U\big)\to4t^2/U$ | two-site Hubbard singlet–triplet gap | `qi_entanglement.py:L343 superexchange_J()`; ED check `L350-L355` | unknown (inferred: exact (ED matches to machine)) |
| 11 | $\theta_\text{tick}=J/4$; $\tau_\text{Bell}=(\pi/8)/(J/4)$ | derived entangling rate | `qi_entanglement.py:L365 exchange_angle_per_tick()`, `L371 bell_time_ticks()` | unknown |
| 12 | $H=iR(\pi/2,(1,0,1)/\sqrt2)=(X+Z)/\sqrt2$ | native Hadamard | `qi_entanglement.py:L388 native_hadamard()` | unknown (inferred: machine (spot-checked $9\times10^{-17}$)) |
| 13 | $U_\text{exch}(-\varphi)\,(-iZ\otimes\mathbb 1)\,U_\text{exch}(-\varphi)\,(-iZ\otimes\mathbb 1)=-e^{2i\varphi ZZ}$; `native_zz(θ)` negates this to return $e^{i\theta ZZ}$ | ZZ from two exchanges | `qi_entanglement.py:L396 native_zz_quarter()`, `L412 native_zz()` | unknown (inferred: machine) |
| 14 | $\mathrm{CP}(\phi)=e^{i\phi/4}e^{i\phi ZZ/4}e^{-i\phi Z_a/4}e^{-i\phi Z_b/4}$ | controlled phase | `qi_entanglement.py:L423 native_cphase()` | unknown (inferred: machine) |
| 15 | $\mathrm{CZ}\propto e^{i\pi/4}\,(\text{zz-quarter})\,R_z\otimes R_z$ (phase-aligned); $\mathrm{CNOT}=(\mathbb 1\otimes H)\,\mathrm{CZ}\,(\mathbb 1\otimes H)$ | CZ, CNOT | `qi_entanglement.py:L490-L494 native_cz()`, `L500-L504 native_cnot()` | unknown (inferred: machine) |
| 16 | $\mathrm{CCZ}=\mathrm{CS}_{23}\,\mathrm{CNOT}_{12}\,\mathrm{CS}^\dagger_{23}\,\mathrm{CNOT}_{12}\,\mathrm{CS}_{13}$ | Barenco CCZ | `qi_entanglement.py:L436-L441 native_ccz()` | unknown (inferred: machine) |
| 17 | MCZ: negate the all-controls-1 block; MCX: swap the target slices on that block | direct multi-controlled actions | `qi_entanglement.py:L467-L470 apply_mcz()`, `L477-L484 apply_mcx()` | unknown (inferred: exact) |
| 18 | circuit runner, gate-spec dispatch, $\lvert\psi\rvert^2$ | plumbing | `qi_entanglement.py:L510-L563` | — |

**Inputs → outputs:** product kets, gate specs → state vector, entropies, $J(m)$. **Depends on:** `particles/dirac.dirac_step_2d_splitstep` (06b-particles-*.md). Consumed by every other `qi_*` module and by five channels (04-core.md). **Flags:**
- ⚠ DOC/CODE MISMATCH at L391-L396: `native_zz_quarter` says it builds $e^{i\pi/4\,ZZ}$. It returns $-e^{i\pi/4\,ZZ}$ (spot-checked), a global phase that `native_cz` later removes by phase alignment. `native_zz` documents and corrects the same sign.
- `hopping_amplitude` uses the 2-D square split-step walk (D1 reference), not BCC, so the derived $J$ and $\tau_\text{Bell}$ inherit square-lattice hopping.
- $t(m)$ sums the absolute values of four components rather than a coherent amplitude, so the definition of $t$ is heuristic.
- `CNOT_REF`/`HADAMARD` are textbook matrices, used only for validation and GHZ building (L245-L260).
- D8: bare `numpy`.
- Findings are not registered.

---

### `engine/interactions/qi_gleason_regularity.py` — non-negative frame functions are regular (F329)
**Status:** live · standalone · **Findings:** F329 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** closes F304's Cooke–Keane–Moran residual by citing Gleason 1957 Thm 2.8 and Lemma 3.3/Thm 3.5. It machine-checks three things: the hypothesis of Thm 3.5 at the model's context dimensions, the frame condition for a quadratic form, and the equator-constancy identity. The covering lemmas 2.5–2.7 are cited, not re-derived.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | model context dimensions $\{3,4,6,64,96\}$; excluded $d=2$ | dimensions tested | `qi_gleason_regularity.py:L183, L191` | exact (reg) |
| 2 | $B=[e_0,e_1,e_2]\subset\mathbb C^d$, $G=B^\dagger B=\mathbb 1_3$ (real) | completely-real 3-subspace (H1) | `qi_gleason_regularity.py:L212, L226-L230 completely_real_subspace_exists()` | exact (reg) |
| 3 | $u$: $(x_i,x_j)\mapsto(-x_j,x_i)$ about $e_0$ | polar rotation by $\pi/2$ | `qi_gleason_regularity.py:L247-L252 polar_rotation()` | exact (reg) |
| 4 | $f(x)=x^\mathsf TTx$, $T=(A+A^\mathsf T)/2$ random; control adds $\epsilon P_3(x_1)$, $P_3=\tfrac12(5t^3-3t)$ | regular frame function / control | `qi_gleason_regularity.py:L263 regular_frame_function()`, `L279 p3_harmonic()` | exact (reg) |
| 5 | spread of $\sum_{i}f(e_i)$ over 400 random orthonormal bases of $\mathbb R^3$ ($=\operatorname{tr}T$ when $\epsilon=0$) | H2 frame condition | `qi_gleason_regularity.py:L314-L322 frame_condition_across_bases()` | machine ($<10^{-10}$) (reg: exact; row is weaker — see flags) |
| 6 | $g(q)=f(q)+f(uq)=W-f(p)$ for every $q\perp p$; Gram of $\{p,q,uq\}=\mathbb 1$ | H3 equator constancy (core of Thm 2.8) | `qi_gleason_regularity.py:L363-L371 equator_constancy_identity()` | machine ($<10^{-9}$) (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** (`control`, `seed`) → checks. **Depends on:** none in the engine. **Flags:**
- ⚠ DOC/CODE MISMATCH at L60-L61 vs L183. The docstring lists the model's dimensions as "d = 4, 8, 9, 16, 64, 96". `MODEL_DIMENSIONS=(3,4,6,64,96)`; the comment at L168-L178 says 8/9/16 were removed.
- ⚠ DOC/CODE MISMATCH at L269-L276 vs L300-L302. `p3_harmonic` says the $P_3$ mode "is annihilated by the frame condition" at $d\ge3$, while `frame_condition_across_bases` says the cubic "is NOT annihilated by the frame condition at d=3". The code (it breaks the frame sum) matches the second wording.
- H1 is tautological: the Gram matrix of standard basis vectors is exactly $\mathbb 1$ for any $d\ge3$.
- Registered `exact`; H2/H3 are float tolerances, i.e. machine.
- D8: `np.random.default_rng`.

---

### `engine/interactions/qi_measurement.py` — pointer basis, Born legs, RG classicality (F281)
**Status:** live · standalone · **Findings:** F281 F227 F226 F212 F218 F130 F133 F87 F41 · **Lattice:** BCC (M2 $\ell^p$ tick); Cartesian block-spin on an $L^3$ array (M3); abstract registers (M1) · **Law:** n/a · **Units:** lattice

**Does:** M1 shows that minimal coupling forces the site-occupation pointer basis, via a commutator, a predictability sieve, and a maximal-abelian commutant. M2 gives the Born rule on two legs: only $\ell^2$ is conserved by a real tick, and envariance plus fine-graining. M3 shows coherence is RG-irrelevant under the block average, with Dirichlet-kernel eigenvalue $b^{-2}$ per dimension.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\hat n=(\mathbb 1-Z)/2$ | charge density | `qi_measurement.py:L162 number_op()` | exact (reg) |
| 2 | $g_{xj}=(\sqrt{2+x+3j}\bmod1)+0.5$ | incommensurate couplings | `qi_measurement.py:L181 _couplings()` | exact (reg) |
| 3 | $H_\text{int}=\sum g_{xj}\hat n_xZ_j$; control $\sum g_{xj}X_xZ_j$; $H_\text{hop}=\tfrac t2\sum(X_xX_{x+1}+Y_xY_{x+1})$ | generators | `qi_measurement.py:L201, L217, L229-L230` | exact (reg) |
| 4 | $\lVert[H_\text{int},\hat n_y]\rVert_F=0$; $\lVert[H_\text{hop},\hat n]\rVert,\lVert[H_\text{int},X_y]\rVert>0$ | M1a/c/d pointer commutators | `qi_measurement.py:L250-L254 pointer_commutator_norms()` | exact (inv. 155: literal 0.0) |
| 5 | $\bar S(\theta)=\tfrac12\sum_{b\in\{0,1\}}S\big(\operatorname{Tr}_E\,e^{-iHt}(R_y(\theta)\lvert b\rangle\otimes\lvert+\rangle^{\otimes n_e})\big)$; argmin over $\theta$ | predictability sieve | `qi_measurement.py:L300-L318 sieve_entropy()`; `L325-L337` | machine (reg: exact; row is weaker — see flags) |
| 6 | $\lvert D(t)\rvert=\prod_j\lvert\cos g_jt\rvert$, vs $2\lvert\rho_{01}\rvert$ numerically | M1e decoherence factor | `qi_measurement.py:L347-L350`; `L358-L374` | machine (reg: exact; row is weaker — see flags) |
| 7 | fraction of $t$ with $\lvert D\rvert>0.9$ vs $n_e$, log-linear fit; $\log_{10}T_\text{rec}=-\text{slope}\cdot N-\text{intercept}$ | Poincaré recurrence extrapolation | `qi_measurement.py:L394-L399 recurrence_statistics()`; `L416-L417` | fit |
| 8 | $\dim\operatorname{comm}\{\hat n_x\}=d^2-\operatorname{rank}=2^{n}$ | M1f maximal abelian | `qi_measurement.py:L465-L472 commutant_dimension()` | exact (inv. #159-165) |
| 9 | $S=0$ on all $2^n$ occupation states; $S>0$ on generic states; DFS probe $\lvert01\rangle-\lvert10\rangle$ | M1g/h many-cell sieve | `qi_measurement.py:L513-L552 sieve_manycell()` | machine (reg: exact; row is weaker — see flags) |
| 10 | $W_p=\sum_i\lvert\psi_i\rvert^p$; relative change under one `weyl_step_3d_bcc` tick | M2a only $p=2$ conserved | `qi_measurement.py:L597 lp_weight()`; `L623-L628 lp_conservation_bcc()` | exact (inv. 156) |
| 11 | same under $U_\text{exch}(\pi/8)$ (mixing) vs SWAP (monomial control) | M2b | `qi_measurement.py:L640-L646` | machine (reg: exact; row is weaker — see flags) |
| 12 | flip $u=R(\pi/2,\hat x)=-iX$; $\lvert\langle\psi\rvert u\otimes u\lvert\psi\rangle\rvert=1$ for $(\lvert00\rangle+\lvert11\rangle)/\sqrt2$ | M2c/d envariance | `qi_measurement.py:L663, L685-L692` | machine (reg: exact; row is weaker — see flags) |
| 13 | $\max_{u_E}\lvert\langle\psi\rvert u_S\otimes u_E\lvert\psi\rangle\rvert=\lVert B^\dagger A\rVert_*=2c_0c_1<1$ if $c_0\ne c_1$ | M2e unequal amplitudes not envariant | `qi_measurement.py:L716-L722 envariance_unequal_amplitudes_fails()` | machine (reg: exact; row is weaker — see flags) |
| 14 | $\psi_{mm}=1/\sqrt M$, $M=\sum\mu_k$; $p_k=\#\{m:\ell_m=k\}/M=\mu_k/M$ (`Fraction`) | M2f/g fine-graining Born weights | `qi_measurement.py:L741-L744 finegrain_state()`; `L794-L798`; `L827-L829 born_exact_over_Q()` | exact (inv. 157) |
| 15 | environment cells $2R^3$; $\log_{10}M_\text{max}=2R^3\log_{10}2$; ticks $=R/4$ | cone capacity | `qi_measurement.py:L852-L856 cone_capacity()` | exact (reg) (row read: unknown) |
| 16 | $D_b(k)=e^{ik(b-1)/2}\,\dfrac{\sin(kb/2)}{b\sin(k/2)}$ | Dirichlet kernel of block average | `qi_measurement.py:L874-L876 dirichlet_kernel()` | exact (reg) |
| 17 | $\lambda_\text{coh}(\mathbf k,b)=\prod_i\lvert D_b(k_i)\rvert^2$; $=1$ at $k=0$; envelope $(b\sin\tfrac k2)^{-2}$ per dim | RG eigenvalue of coherence | `qi_measurement.py:L891-L893 coherence_rg_eigenvalue()` | exact (inv. 158) |
| 18 | $\max\lvert R_b[e^{ikx}]\rvert^2$ vs $\lambda_\text{coh}$ (`block_average_field`) | M3a closed form vs the model's $R_b$ | `qi_measurement.py:L909-L917 coherence_rg_numeric()` | machine (spot-checked $7\times10^{-16}$) (reg: exact; row is weaker — see flags) |
| 19 | $b^3\sum$coarse $=\sum$fine | M3b population marginality | `qi_measurement.py:L931-L936` | exact (reg) |
| 20 | slope of $\log[(b^2\sin^2\tfrac k2)^{-\text{dims}}]$ vs $\log b$ $=-2\,\text{dims}$ | M3d exponent | `qi_measurement.py:L951-L954 coherence_exponent()` | exact (reg) |
| 21 | $N\log_{10}\big[(b^2\sin^2\tfrac k2)^{-3}\big]$, $b=10$, $N=35$ | macroscopic coherence suppression | `qi_measurement.py:L973-L976` | exact (reg) (row read: unknown) |

**Inputs → outputs:** (`coupling`, `flip_angle_over_pi`, `block_b`) → 20 check rows + summary. **Depends on:** `core/blockspin.block_average_field` (04-core.md), `lattice/bcc.weyl_step_3d_bcc` (03-lattice.md), `qi_noise.embed/embed2`, `qi_entanglement` gates. **Flags:**
- ⚠ DOC/CODE MISMATCH at L725-L734. `finegrain_state` says the equal-amplitude state is produced "by a controlled-copy onto counters … a CNOT". The code writes $1/\sqrt M$ directly on the diagonal of an $M\times M$ Schmidt matrix, with no gate applied. So M2f/M2g ($p_k=\mu_k/M$) are true by construction: the label counts equal $\mu_k$ because `labels` is built from $\mu_k$.
- ⚠ DOC/CODE MISMATCH at L848-L852. The text says "a BCC ball of radius R holds $2R^3$ cells". $2R^3$ is a BCC *cube* of edge $R$; a ball would be about $\tfrac{8\pi}{3}R^3$.
- M3d (row 20) fits the log of the module's own closed-form envelope, so it cannot deviate from $-2\,\text{dims}$.
- The M1f check is hardwired to the control: `… and (coupling == "minimal")` (L1127). The commutant computation does not depend on `coupling`.
- Registered `exact`, while M1e, M1g, M2b–M2e and M3a are float-tolerance (machine) and row 7 is a fit.

---

### `engine/interactions/qi_noise.py` — Kraus channels and stabilizer codes (F221)
**Status:** live · driven (0 ch listed) · **Findings:** (registry: none; docstring F221) · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** exact density-matrix noise channels, plus 3-qubit bit/phase-flip and 9-qubit Shor encoders and recovery built from native CNOT/H.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $O_q=\mathbb 1^{\otimes q}\otimes O\otimes\mathbb 1^{\otimes(n-q-1)}$; two-qubit embedding via `apply_gate` columns | embedding (plumbing) | `qi_noise.py:L55-L59 embed()`, `L64-L69 embed2()` | unknown (inferred: exact) |
| 2 | $F=\langle\psi\rvert\rho\lvert\psi\rangle$ | fidelity | `qi_noise.py:L78` | unknown (inferred: exact) |
| 3 | bit flip $\{\sqrt{1-p}\,\mathbb 1,\sqrt p\,X\}$; phase flip $\{\sqrt{1-p}\,\mathbb 1,\sqrt p\,Z\}$; depolarising $\{\sqrt{1-3p/4}\,\mathbb 1,\sqrt{p/4}\,X,Y,Z\}$; amplitude damping $E_0=\operatorname{diag}(1,\sqrt{1-\gamma})$, $E_1=\sqrt\gamma\lvert0\rangle\langle1\rvert$ | Kraus sets | `qi_noise.py:L83, L87, L93-L94, L99-L101` | unknown (inferred: exact) |
| 4 | $\rho\to\sum_kE_k\rho E_k^\dagger$ on qubit $q$ | channel application | `qi_noise.py:L106-L110 apply_channel()` | unknown (inferred: machine) |
| 5 | $\alpha\lvert000\rangle+\beta\lvert111\rangle$ (CNOT fan-out); phase code $=H^{\otimes3}$ on it; Shor $=$ outer phase code on leaders 0,3,6, then inner bit-flip | encoders | `qi_noise.py:L132-L135, L140-L143, L155-L163` | unknown (inferred: machine) |
| 6 | $\rho\to\sum_sC_sP_s\rho P_sC_s^\dagger$, $P_\pm=\tfrac12(\mathbb 1\pm S)$, syndromes $Z_0Z_1,Z_1Z_2$ (inner) and $X^{\otimes3}X^{\otimes3}$ (outer) | recovery | `qi_noise.py:L169-L171 _proj_pm()`; `L178-L190 recover_bitflip()`; `L196-L199`; `L207-L237 recover_shor()` | unknown (inferred: machine) |
| 7 | $F_\text{corr}=(1-3p^2+2p^3)+(3p^2-2p^3)(2ab)^2$ | analytic corrected fidelity | `qi_noise.py:L252-L253 bitflip_corrected_fidelity()` | unknown (inferred: exact) |
| 8 | $F_\text{unc}=(1-p)^3+p^3(2ab)^2$ | analytic uncorrected fidelity | `qi_noise.py:L261 bitflip_uncorrected_fidelity()` | unknown (inferred: exact) |

**Inputs → outputs:** $p,\gamma$, amplitudes → $\rho$, fidelities. **Depends on:** `qi_entanglement` (`apply_gate`, `native_cnot`, `native_hadamard`). **Flags:**
- Registry `reach=driven` with `n_reachable_from=0`, which is inconsistent.
- D8: bare `numpy`.
- Findings are not registered.
- Both the Pauli matrices and `H1` are literals, not the native gates. This matters for recovery in the Hadamard basis (L196).

---

### `engine/interactions/qi_qc_si.py` — SI anchoring of super-exchange and doublon leakage (F224/F225)
**Status:** live · test-only · **Findings:** (registry: none; docstring F224, F107/F123, F130, F214, F217, F220) · **Lattice:** n/a · **Law:** n/a · **Units:** SI (via `casim.constants`)

**Does:** maps the dimensionless super-exchange $J(t,U)$ and doublon weight to Hz/s. It compares these with the Trotzky 2008 cold-atom superexchange and the GaAs singlet–triplet (S–T) exchange-qubit leakage.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $a=(a/\ell_P)\,\ell_P$, $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107); $\tau=a/(c\sqrt3)$; $h=2\pi\hbar$ | canonical cell and tick | `qi_qc_si.py:L50-L51, L47` | unknown (inferred: exact ($a/\ell_P$); external ($\ell_P,c,\hbar$)) |
| 2 | $J=\tfrac12(\sqrt{U^2+16t^2}-U)$; $J_\text{lead}=4t^2/U$; $(J-J_\text{lead})/J_\text{lead}$ | exact vs leading super-exchange | `qi_qc_si.py:L72, L78, L84` | unknown (inferred: exact) |
| 3 | $t_\text{Bell}=1/(4J)$ with $H_\text{eff}=(hJ/4)\,\boldsymbol\sigma\cdot\boldsymbol\sigma$; period $1/J$ | SI entangling time, swap period | `qi_qc_si.py:L92, L98` | unknown (inferred: exact) |
| 4 | $E_\text{lat}=\hbar/\tau$ in eV ($3.205\times10^{27}$) | fundamental tick energy | `qi_qc_si.py:L103` | unknown (inferred: exact (given the constants)) |
| 5 | $d=\tfrac12\big(1-1/\sqrt{1+(4t/U)^2}\big)\to(2t/U)^2$ | two-site Hubbard double occupancy (leakage) | `qi_qc_si.py:L115-L116, L121` | unknown (inferred: exact) |
| 6 | $t/U=\tfrac14\sqrt{(1-2d)^{-2}-1}$ | invert leakage | `qi_qc_si.py:L127-L128 tU_from_leakage()` | unknown (inferred: exact) |
| 7 | $J_\text{Hz}=J/(2\pi\tau_\text{eff})$; $\tau_\text{eff}=J/(2\pi J_\text{target})$ | emergent-lattice tick mapping | `qi_qc_si.py:L134, L140` | unknown (inferred: exact) |

**Inputs → outputs:** $(t,U)$, $J_\text{Hz}$, $d$ → SI times, $t/U$. **Depends on:** `casim.constants` `a_over_ellP`, `c_SI`, `ell_P_m`, `hbar_SI` (01-constants.md). **Flags:**
- The constants imported here are not recorded as `Site`s in the constants registry.
- `EV_PER_J` uses the literal $1/1.602176634\times10^{-19}$ (L52).
- Experimental anchors (Trotzky 5 Hz–1 kHz, $J/U=0.08$; GaAs leakage 0.0013, fidelity 0.995) are literals.
- D8: bare `numpy`.
- Findings are not registered.

---

### `engine/interactions/qi_so3_kinematic_gap.py` — emergent continuous SO(3) cannot supply Postulate 1 (F379)
**Status:** live · standalone · **Findings:** F379 F330 F289 F344 F129 F130 · **Lattice:** BCC (`_bcc_uvec`, both branches) · **Law:** n/a (Weyl $u,\mathbf n$ of the BCC walk) · **Units:** lattice

**Does:** K1 extends the covariance of $H_W=\mathbf k\cdot\boldsymbol\sigma/\sqrt3$ to continuous SO(3) using the F289 rotor. K2 checks the leading-order covariance of the shipped BCC $\mathbf n(\mathbf k)$ under a non-$O_h$ rotation. K3 is an uncorrelated-rotor control. The closure argument (Postulate 1 is prequantisation-level, so no dynamical fact bears on it) is prose.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $R=\mathbb 1+\sin\alpha\,K+(1-\cos\alpha)K^2$ | Rodrigues rotation | `qi_so3_kinematic_gap.py:L191 rodrigues()` | exact (reg) |
| 2 | $U(R)\,(\mathbf k\cdot\boldsymbol\sigma)\,U(R)^\dagger=(R\mathbf k)\cdot\boldsymbol\sigma$, $U=$ `su2_rotor(α/2, n̂)`; 8 axes × 7 generic angles × 5 $\mathbf k$ | K1 continuous covariance | `qi_so3_kinematic_gap.py:L220-L222 idealized_weyl_continuous_covariance()` | exact (reg) |
| 3 | $\mathbf n(R\mathbf k)\approx(SRS)\,\mathbf n(\mathbf k)$, $S=\operatorname{diag}(1,-1,1)$ ('+') or $\mathbb 1$ ('−'); relative defect per decade of $\lvert\mathbf k\rvert$, ratio $\to10$ | K2 shipped-walk covariance defect $O(k)$ | `qi_so3_kinematic_gap.py:L252-L270 shipped_walk_continuous_covariance_decades()` | quantitative (ratios 9.84, 9.98, 9.998) (reg: exact; row is weaker — see flags) |
| 4 | residual with the correct rotor vs with $U(\hat x,0.4)$ for $R(\hat z,1.7)$ | K3 control | `qi_so3_kinematic_gap.py:L290-L294 uncorrelated_rotor_control()` | machine (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** (`use_uncorrelated_rotor`, `n_axes`) → checks + summary. **Depends on:** `qi_entanglement.su2_rotor`, `qi_spin_statistics._rotor_for_physical_angle`, `lattice/bcc._bcc_uvec` (03-lattice.md). **Flags:**
- K2's geometry is degenerate. $\mathbf k$ is placed **along the rotation axis** (`k = ax * mag`, L258), so $R\mathbf k=\mathbf k$ (spot-checked, $|R\mathbf k-\mathbf k|=10^{-16}$). The rotation therefore does not act on the momentum. K2 tests only that $\mathbf n(\mathbf k)$ is approximately an eigenvector of $SRS$, not covariance under a generic rotation.
- ⚠ DOC/CODE MISMATCH at L78-L84 vs L232-L247. The module docstring says K2 sweeps "a swept family of generic axes and angles". The code evaluates one fixed axis/angle.
- Registered `exact`; K2 is quantitative (decade ratio within 0.5 of 10).
- The literals `axis=(0.4082482905, 0.4082482905, -0.8164965809)`, which is $(1,1,-2)/\sqrt6$, and `angle=1.1071487178`, which is $\arctan2$, are truncated decimals.

---

### `engine/interactions/qi_spin_statistics.py` — spin-statistics from derived premises (F289)
**Status:** live · standalone · **Findings:** F289 F291 F292 F217 F195 F68 F26 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** checks the theorem's inputs on the model's own objects. The rotor gives $R(2\pi)=-1$ on every axis. SWAP is an involution, so there are no anyons in $d\ge3$. Jordan–Wigner operators anticommute, which gives Pauli exclusion and $\binom nk$ sectors. The paired-spinor photon has phase $(-1)^2=+1$, so it is a boson.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $R_\text{phys}(\varphi,\hat n)=$ `su2_rotor(φ/2, n̂)` | physical-angle rotor | `qi_spin_statistics.py:L103 _rotor_for_physical_angle()` | exact (reg) |
| 2 | $\lVert R(2\pi)+\mathbb 1\rVert$, $\lVert R(4\pi)-\mathbb 1\rVert$; over 60 Fibonacci axes | S1/S2 double-valuedness | `qi_spin_statistics.py:L116-L121, L139-L140` | exact (inv. #159-165: $1.7\times10^{-16}$, machine residual) |
| 3 | $\mathrm{SWAP}^2=\mathbb 1$, spectrum $\{+1^{(3)},-1^{(1)}\}$ | S3 exchange involution | `qi_spin_statistics.py:L157-L166 exchange_is_involution()` | exact (reg) |
| 4 | $U_\alpha=e^{i\pi\alpha}\mathrm{SWAP}$ is unitary but $U_\alpha^2\ne\mathbb 1$ for $\alpha\notin\{0,1\}$ | anyonic control | `qi_spin_statistics.py:L185-L187`; `L391-L394` | machine (reg: exact; row is weaker — see flags) |
| 5 | $c_i=Z^{\otimes i}\otimes\sigma^-\otimes\mathbb 1^{\otimes(n-i-1)}$; $\{c_i,c_j\}=0$, $\{c_i,c_j^\dagger\}=\delta_{ij}$; string-less control | S4 Jordan–Wigner | `qi_spin_statistics.py:L208-L217 _jw()`; `L235-L239`, `L250` | exact (reg) |
| 6 | $(c_i^\dagger)^2=0$; $P_\text{anti}=\tfrac12(\mathbb 1-\text{swap})$ with rank $\binom n2$, killing same-mode states | S5/S5c Pauli exclusion | `qi_spin_statistics.py:L267, L279-L289, L304` | exact (reg) |
| 7 | sector dims of $N=\sum c^\dagger c$: $\binom nk$ vs bosonic $\binom{n+k-1}{k}$ | S5b | `qi_spin_statistics.py:L318-L323 fock_sector_dimensions()` | exact (reg) |
| 8 | $R(2\pi)^{\otimes2}=(+1)\mathbb 1_4$ | S6 paired-spinor photon is a boson | `qi_spin_statistics.py:L346-L350`; `L433-L434` | exact (reg) |

**Inputs → outputs:** (`rotation_turns`, `exchange_alpha`, `jw_string`) → 11 check rows. **Depends on:** `qi_entanglement.su2_rotor`, `swap_gate`. **Flags:**
- The `jw_string=false` control is hardwired. S4 becomes `False` through `… if jw_string else False` (L409). No string-less operators are fed into S4, although S4b computes them separately.
- S6 is the pair-phase bookkeeping for the decision-5 paired-spinor photon, not a propagated photon. It uses no σ-bilinear construction.
- Registered `exact`; S1/S2/S6 are float residuals (machine).
