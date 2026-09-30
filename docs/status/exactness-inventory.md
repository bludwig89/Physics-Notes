# Exactness Inventory

*A short tally of which lattice results are exact in the algebraic sense (identity, closed form, or bit-for-bit), which are at machine precision (FFT round-off floor, ≲ 1 ulp of complex128 per step), and which are quantitative matches inside a stated tolerance. Pulled from `docs/status/project-status.md`, `findings.md`, `docs/theory/ca-reference.md`, and `test-results/qca-verifications-results.md`. Last updated 2026-06-11 - 06:50 (**F140** — the coarse-grained baryon element (`ca_baryon_blockspin.py`; renumbered F135→F140 to avoid a concurrent session's F135): **2 new rows (#85–86)**. Supplies the lattice baryon F132 deferred (the ECG is a basis, not a lattice): the $K{=}0$ hyperradial reduction of the F122 three-quark Cornell problem — a 1-D radial element (centrifugal $15/4$, $C_\sigma=16\sqrt2/5\pi$ from the $S^5$ hyperangular average) — reproduces the ECG baryon ground energy across $\sigma$ to $<0.05\%$ with ONE $\sigma$-independent adiabatic coefficient $\kappa{\approx}2.0$, is confinement-dominated ($E_\text{rel}\propto\sigma^{2/3}$, slope $0.6666$), and coarse-grains under $R_b$ (hyperradial grid decimation): the proton mass + rms hyperradius reproduce on $b\times$ fewer cells ($0.01\%$ at $b{=}2$ → $0.13\%$ at $b{=}8$, overlap $0.997$–$1.0$, stays confined, error $\sim b^2$). In lattice units the confining $\hat\sigma$ is the F130-C1 relevant operator ($\lambda_\sigma=b$). `test_F135_coarse_grained_baryon.py` 9/9 PASS. Previous: 2026-06-11 - 06:20 (**F134** — Phase-4 completion (chiral block-spin + hand-rolled chiral core + FFT floor): **2 new rows (#75–76)**. The renormalised coarse rule $\Omega(\kappa/b)$ now covers all three F91 classes — `renormalized_chiral_step` (W± RS) and `renormalized_weyl_step` (per-branch $U^\pm$) reduce bit-for-bit to the audited fine kernels at $b{=}1$, stay unitary, and commute with $R_b$ on band-limited fields ($\sim1.5\times10^{-15}$); the W-chiral/Weyl engine channels use them when block>1. A verified hand-rolled chiral core (`casim.lattice.chiral_core`, explicit real/imag arithmetic, no np.linalg — CLAUDE.md) matches the kernels bit-for-bit and registers through the `backend.chiral_transform` seam. The FFT round-off floor is $\sim1$ ulp/step and L-stable ($L{=}8/16/32$, no degradation); a second `numpy_fft` backend is identical to `ca_fft` to round-off — the validated swap point a GPU backend would use (GPU itself is hardware, not built here). `test_F134_phase4_completion.py` 15/15 PASS; casim engine suite unchanged. Previous: 2026-06-11 - 05:40 (**F133** — Phase 4: the block-spin RG $R_b$ as a first-class CASIM engine operation (`src/casim/engine/blockspin.py` + engine wiring): **2 new rows (#73–74)**. A run now declares a physical patch + block factor (`LatticeSpec.block` ⇒ `physical_L=L·block`, `cell_factor=block^d`; scenario `physical_patch`/`block`) and can coarse-grain a LIVE run via `Simulation.block_spin(b)` (adaptive-resolution CA step; schedulable from a scenario `blockspin:` field). The engine $R_b$ reproduces `ca_blockspin.block_average` bit-identically and is complex-safe for spinors; the gravity dielectric uses the F130-T3b log rule ($A\!\cdot\!B\equiv1$). The renormalised coarse propagator $\Omega(\kappa/b)$ (`renormalized_even_step`) reduces to the fine photon step at $b{=}1$ and is dynamically faithful — $[R_b,\text{evolution}]=0$ on band-limited fields ($1.8\times10^{-15}$), with the $c_\text{lat}$ fixed point. `test_F133_blockspin_engine.py` 11/11 PASS; existing casim engine suite unchanged (59/59). Previous: 2026-06-11 - 05:10 (**F132** — coarse-graining the dynamical/relativistic bound states (`ca_blockspin_dynamical.py`): **3 new rows (#70–72)** carrying Phase-2 from the F131 smooth-well toy onto the model's actual F74-family bound states, exposing the Wilsonian relevant/irrelevant split. **P (pion, F74/F103):** the CONTACT coupling is relevant — under $R_b$ it RUNS ($g{=}4\!\to\!1.01$ at $b{=}2$, $\to0.45$ at $b{=}3$) to hold $E_b$ fixed, the flow predicted to a few % by the Watson threshold ratio $g/g_c$; with the run coupling the wavefunction (overlap $\ge0.97$) and size ($<2\%$) reproduce on up to 27× fewer cells. **D (deuteron, F104):** the FINITE-RANGE Yukawa/OBE coupling is irrelevant — held fixed, grid decimation reproduces the shallow halo $E_b{=}2.224$ MeV to $0.4\%$ ($b{=}2$), error $\sim b^2$, no run. **B (baryon, F122):** confinement-dominated, $E_\text{rel}\propto\sigma^{2/3}$ (slope $0.667$) ⇒ mass = the F130-C1-covariant string scale; ECG reproduces the analytic harmonic three-body to $0.3\%$. Unification: relevant couplings = confinement $\sigma$ (eig $b$) + contact ($g/g_c$); irrelevant = LIV ($b^{-n}$) + deconfining $\lambda$ ($b^{-2}$) + smooth finite-range potentials. `test_F132_blockspin_dynamical_bound_states.py` 9/9 PASS. Previous: 2026-06-11 - 04:40 (**F130-C1 + F131** — completing the block-spin RG: confinement flow + the Phase-2 bound-state check. **F130-C1 (1 new exact row #192):** confinement is the one *relevant* RG direction — the F110 static-potential slope $\hat\sigma=g^2/2$ ($\lambda=0$) and bond-moving $g^2\!\to\!b\,g^2$ give eigenvalue $\lambda_\sigma=b>1$ (vs the irrelevant LIV $b^{-n}$); a coarse F110 run on $b\times$ fewer plaquettes reproduces the fine $V(b\cdot R)$ exactly (residual $0.0$ at $\lambda{=}0$), and the deconfining magnetic coupling $\lambda$ is irrelevant (deforms $\hat\sigma$ by $\propto\lambda^2/g^4\to b^{-2}$). **F131 (2 new rows #68–69):** Phase-2 — the RG commutes with binding in the long-wavelength sector. A coarse-grained harmonic bound state ($b{=}2$, 8× fewer cells) reproduces the fine spectrum: low levels match $<1\%$, the $O_h$ first-excited triplet stays 3-fold degenerate, block-averaged-fine ↔ coarse ground overlap $0.99986$, both converge to the analytic $E_N=\omega(N+\tfrac32)$; the softened-Coulomb (F125 hydrogen) ground state is reproduced to $0.45\%$. Coarse error = the irrelevant $O((ka)^2)$ operator (more-IR → smaller, $\sim b^2$ in the block factor). `test_F130_…` 38/38, `test_F131_blockspin_bound_state.py` 10/10 PASS. Previous: 2026-06-11 - 04:17 (**F130** — Phase-1 block-spin / coarse-graining RG scheme, gauge + gravity sectors (`ca_blockspin.py`): **4 new exact rows (#188–191) + 2 new machine-precision rows (#66–67)** proving the Kadanoff transform $R_b$ preserves the rotation rule's physics, so a coarse run of $N$ super-cells faithfully stands in for $(bN)^d$ physical cells. Exact — (T1) $c_\text{lat}$ is an RG fixed point: $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$ makes the physical speed invariant for all $b$ ($1/\sqrt3$ along axis / face- / body-diagonal); (T2) the order-$n$ LIV operator has eigenvalue $b^{-n}$ exactly (matched-sampling identity) — every lattice artifact is irrelevant, $\Omega=c\lvert k\rvert$ the attractive IR fixed point; (T3a) Gauss's law survives blocking as an integer-exact discrete divergence theorem (E blocked as coarse-face flux-sums, charge as block-sums; residual $0.0$); (T3b) the F64/F106 dielectric reciprocal lock $A\!\cdot\!B\equiv1$ is preserved iff the dielectric is coarse-grained in the LOG variable $u=\tfrac12\ln K$ (the linear Poisson potential) — the naive direct-$K$ average breaks it by the Jensen gap, so $u$ is the RG-covariant variable. Machine — (T2num) the leading even-law operator reproduces F30 ($g_2=-1/162$, $\delta v_g/c=-k^2/54$, $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$); (T3c) $[R_b,R(\Omega)]=0$ so blocking cannot mix the F91 even/chiral propagator classes. Plus the gravity-Poisson source law is form-invariant in the IR with a residual that itself coarse-grains away as $b^{-2}$. Free-photon sector is the concurrent F129. `tests/findings/test_F130_blockspin_gauge_gravity.py` 30/30 PASS. Previous: 2026-06-08 - 16:05 (**F117** — the condensate gap wired into the time-evolved gluon propagator (`ca_colour_dielectric.py` Part D): **2 new bit-for-bit + 2 machine-precision rows** — the BCC even-law dielectric step reduces to the free F91 step bit-for-bit at $\varepsilon_c=1$ and the gap-massive step reduces bit-for-bit at $m_V=0$ (GD1/GD4 reductions, residual $0.0$); the uniform dielectric is exactly unitary (energy drift $4.1\times10^{-14}$ over 200 ticks, $c_\text{eff}=c_\text{lat}\sqrt{\varepsilon_c}$ res $0$) and the gap-massive even-law dispersion $\omega^2=m_V^2+\Omega_\text{even}^2$ holds to $1.2\times10^{-13}$ (GD2/GD4); plus the exact hand-off identities $\sigma_{F86}=2\pi v^2$ and $v=m_D\sqrt\beta$ (GD3, residual $0.0$) and the quantitative screening $\lambda=1/m_V$ (2.2%) and dynamic flux expulsion ($\sim38\times$). Headline: the dielectric, the screening length, the tension and the propagator mass gap all collapse onto the single **measured** condensate VEV $v$. `tests/findings/test_FG7f_gluon_dielectric_gap.py` 6/6 PASS; colour/gluon regression unchanged (FG7 20/20, FG7d 6/6, FG7e 8/8, F91 13/13, F99 5/5, F101 5/5). Previous: 2026-06-08 - 14:10 (**F113** — the NN short-range repulsive core derived from the model: **4 new exact (ℚ) rows (#184–#187)** — the SU($N$) Fierz swap algebra ($\sigma\!\cdot\!\sigma$ triplet $+1$/singlet $-3$, $\lambda\!\cdot\!\lambda$ $\bar3$-pair $-8/3$), the single-baryon chromomagnetic energies $N{=}-8$/$\Delta{=}+8\,g_\text{cm}$ fixing $g_\text{cm}=18.31$ MeV from the measured $N$–$\Delta$ splitting, the exact six-quark deuteron-channel norm kernel ($n(0)=20/9>0$, allowed), and the core itself $\Delta E_\text{CM}=+56/3\,g_\text{cm}=+341.8$ MeV (positive ⇒ repulsive) — which **replaces the tuned hard core of F104**: two colour-singlet nucleons (F71) overlapping are six fermions whose Pauli antisymmetriser forces the chromomagnetically-unfavourable [6] state. `ca_nuclear_core.py`, `test_F113_repulsive_core.py` 7/7 PASS (stdlib `fractions` only). Previous: 2026-06-06 - 18:45 (**F64-mainline** — the gravity field element moved fork→production (audit B.2 #1): new `ca_gravity.py` (canonical maps, D-EM8 dynamical Φ, F106 sourcing with $G_\text{lattice}=1/(72\pi)$ structural, F62 lapse mix), dynamic `gravity_dielectric` channel sourced by matter, `ParticleChannel` gravity background→coupled. **1 new row (#182)**: the F106 law as a discrete identity through the production maps + the flat bit-identical reduction + exact mix unitarity. `tests/test_gravity_element.py` 6/6 PASS; particle layer 23/23; scenario `gravity_dynamic_selfsourced` (norm 5.3e-14, K_max 1.025). Previous: 2026-06-06 - 17:55 (**F106** — the ψ→K sourcing law: the fermion sources its own dielectric through its energy density, $\nabla^2\ln K=-(8\pi G/c^4)T^{00}[\psi]$, closing the F64 loop's two posits ($\rho=|\Psi|^2$ proxy, free $G$). **1 new exact-algebraic row (#181)**: the coefficient collapses to pure lattice quantities $8\pi G/c^4=a^2 c_\text{lat}/(\hbar c)$ on substituting F79's structural $G$ and $c_\text{lat}=1/\sqrt3$ (sympy zero residual); the source is $T^{00}$ not $|\Psi|^2$ because by F26 mass *is* confined $(\mathbf E,\mathbf B)$ rotation, so radiation and rest mass with equal $T^{00}$ source equally; the old $|\Psi|^2$ Poisson loop is the nonrel limit ($G_\text{eff}=2Gm$). Sourcing a Gaussian $T^{00}$ through the law recovers the canonical $\ln K\to2GM/rc^2$ (slope $0.04003$ vs $0.04$). `test_F106_psi_K_sourcing.py`, 5/5 PASS. Previous: 2026-06-06 - 16:56 (**stability fix** — the `charge_photon` t3718 blow-up traced to forward-Euler in `ca_charge_coupling.maxwell_curl_step` ($|\lambda|^2=1+dt^2|C|^2>1$ per mode, unconditionally unstable; observed rate 0.0228/tick = predicted band-edge value); replaced by the **exact** per-mode rotation propagator $\exp(dt\,G)=1+(\cos\theta-1)P_T+\sin\theta\,\hat G$ and the curl symbol symmetrised over the grid involution (the analytic odd projection of $n(k/2)$, $4\pi$-periodic, left an even Hermitian-breaking residue on the Nyquist planes). **2 new rows (#179–180)**: the closed-form propagator (exact algebraic; free energy drift $1.6\times10^{-13}$/1000 ticks, Gauss invariance $8.6\times10^{-14}$, no CFL limit) and the grid-odd symbol identity $C(k^*)=-C(k)$ (exact, residual 0.0). F87 20/20 PASS unchanged. Previous: 2026-06-06 - 06:58 (**F104** — matter-binding **P4**, the deuteron, the first nucleus, bound by the pion tensor force (full ³S₁–³D₁ coupled channel; the F74 two-body solver generalised contact→2-channel; m_π/f_π from P3, g_A external via Goldberger-Treiman). **1 new machine-precision row (#178)**: the tensor spin-angular ⟨S₁₂⟩ matrix built from explicit Clebsch-Gordan + spinor-spherical-harmonic quadrature equals the Rarita-Schwinger $[[0,2\sqrt2],[2\sqrt2,-2]]$ to $9.8\times10^{-15}$ — the off-diagonal $2\sqrt2$ is exactly the L=0↔L=2 mixing that binds. Headline (structural): the tensor force is ESSENTIAL — at a fixed core the full OPEP binds (−2.0 MeV) while central-only is unbound (+0.66 MeV); a single shallow $J^P=1^+$ I=0 state, $P_D≈7\%$ (0 without tensor), ³S₁ tail slope $=\kappa=\sqrt{M_N E_b}/\hbar c$ to 0.34%, tunable to $E_b=2.224$ MeV / $\kappa=0.2316$ fm⁻¹. `casim.engine.particles.nuclear`, `tests/findings/test_P4_deuteron.py`, 11/11 PASS. Previous: 2026-06-06 - 06:42 (**F103** — matter-binding **P3**, the dynamical pion as the q̄q pseudoscalar Goldstone; reuses the F77 NJL ladder + F74 relcoord solver with no new free physics. **1 new machine-precision row (#64)**: the real-space relative-coordinate q̄q bound state from the secular Koster-Slater root equals dense diagonalisation to $1.3\times10^{-15}$ (L=12, F74 engine), certifying the pion as a real-space dynamical object. Reuses exact rows #61/#62/#161 (Goldstone $m_\pi=0$, $m_\sigma=2m_c$, polarization split) now in the pion context; the Goldstone *scaling* $m_\pi^2\propto m_0$ is flat to 0.86% (quantitative) and the calibrated spectrum reproduces measured $m_c/m_\pi/f_\pi/\langle\bar qq\rangle$ to 0.2–4.2% with GMOR 0.39%. `casim.engine.particles.meson`, `tests/findings/test_P3_pion.py`, 13/13 PASS. Previous: 2026-06-05 - 19:25 (**F102** — casim particle-layer P2, em + SU(3) back-action made two-way; **2 new machine-precision Ward identities** (#176–177): U(1) minimal-coupling exact gauge covariance $S[\alpha+\beta](e^{iq\beta}\psi)=e^{iq\beta}S[\alpha](\psi)$ to $6.5\times10^{-17}$ with the electrostatic force as exact Bloch acceleration ($1.0\times10^{-15}$), and the SU(3) global Ward identity $V\cdot S_A(q)=S_{VAV^\dagger}(Vq)$ to $3.1\times10^{-16}$ (local $O(a)$, F34/FG-3 status); both built from already-audited architectures (F41/F42 U(1) wrap, F31/F34 SU(2) rotate-then-step) ported to 3D BCC, `ca_minimal_coupling.py`, 8/8 P2 PASS. Previous: 2026-06-05 - 14:20 (**F101** — one-heavy lepton branch located + exactly fitted; **2 new structural theorems + 1 exact closed-form fit + 1 consistency lock + 2 honest negatives** [numbers to reconcile with the F86–F100 concurrent blocks]: structural — the **cliff theorem**: $f'(m)\to-\infty$ at the saturation edge (table slopes $-0.41/-1.5/-5.0/-13.6$ at $y=0.9/0.99/0.999/1.0$), so an interior heavy flavor is always a saddle (verified eig $-1.94$) and the heavy generation is FORCED onto the wall: $y_\tau=1$ exactly — the τ mass is the condensate's saturation scale; exact — the wall-pinned inverse fit is LINEAR: $(\kappa_E,\mu)(W)$ in closed form from the two light-flavor stationarity equations, the measured spectrum a KKT local vacuum over $W\in[0.096,21.6]$ with $W>0$ emergent and $r=\kappa_E/\kappa_0\approx0.986$; consistency — F95's $C=0.636|B_\text{sea}|$ ($B_\text{sea}=-5.69\times10^{-2}$ at the lepton invariants) selects $W^*=6C/e^6=1.46$ INSIDE the admissible window (fit at $W^*$: $\kappa_E=0.657$, Hessian PD, wall margin $-12.8$) — two independent routes pin $W\approx1.5$; negatives — metastability (lepton point never global on the minimal 3-coupling family; squeezed between $(1,1,1)$ and $(0,0,0)$, closest gap $2.5\times10^{-2}$ at $W=0.69$) and the static uniform-mode RPA sextic is NEGATIVE (anti-brake; operator non-PD near the wall) — W underived at static one-loop, the momentum-resolved bubble now precisely posed. 6/6 PASS. Previous: 2026-06-05 - 16:10 (**F102/confinement-chain** [finding number collides with the concurrent casim particle-layer F102 — to reconcile; this is the F97→F102 confinement thread] — coupling several rotors: does the F101-rotor crossover survive when plaquettes are coupled? Exact diagonalisation of $\mathbb{Z}_3$ gauge theory (matvec Lanczos, validated vs dense $2.7\times10^{-14}$, trivial Gauss sector $\langle A_s\rangle=1$) on $P=1,2,3$ plaquette strips: the crossover SURVIVES — $\langle B_p\rangle$ runs $0\to1$, identical across $P$ at strong coupling (plaquettes decouple, spread $2\times10^{-6}$), $\langle W_P\rangle=C_P\langle B_p\rangle^P$ with $C_P=O(1)$ strong $\to1$ weak (F70 product recovered), $\sigma=-\ln\langle B_p\rangle$ log slope $-1.02$ all $P$, weak-coupling order increases with $P$ (transition precursor). The single rotor is the strong-coupling limit of the coupled theory. 5/5 PASS. Previous: Last updated 2026-06-05 - 15:35 (**F101/confinement-chain** [collides with concurrent lepton-branch F101] — full strong-coupling $\sigma$ from the rule's compact-rotor transfer operator (extends F100 past Gaussian); **1 exact-diag + 2 asymptotically-exact limits + 1 reconciliation**: exact — (S1) the compact rotor $H=\tfrac1{2\chi}\hat E^2-\lambda\cos\hat\phi$ in the integer-charge basis, $\sigma_1=-\ln\langle e^{i\phi}\rangle$ at all couplings (truncation-converged $4\times10^{-16}$), monotone $\sim3.9\to0.03$. Limits — (S2) weak $\lambda\to\infty$ → F100 Gaussian $1/(4\sqrt{\lambda\chi})$ (rel→0.3%); (S3) strong $\lambda\to0$ → $s_1\to2\lambda\chi$, $\sigma\to-\ln(2\lambda\chi)$, the non-perturbative log law (rel $2\times10^{-5}$). Reconciliation — (S4) strong-coupling slope $d\sigma/d\ln(\text{coupling})\to-1$ for both rotor ($-0.999$) and F70 $-\ln w(\beta)$ ($-1.004$); F70 $w\to\beta/18=\beta/(2N^2)$ (exact SU(3) leading character). (S5) rule map $\lambda=\chi\Omega^2$: at the rule's $\Omega\approx1.3$ the compact rotor corrects the Gaussian σ upward $+12\%$; soft $\Omega$ confines. One operator interpolates Gaussian↔confinement; compactness produces the $-\ln(\text{coupling})$ area law. Scope: single-plaquette/single-mode (3+1D σ still F94), U(1) parent vs $\mathbb{Z}_3$ (A-vs-C caveat). 5/5 PASS. Previous: 2026-06-05 - 15:05 (**F100** — the $\gamma(\Omega)$ map from the QCA rule's transfer operator (closes F99 §5); **1 new machine-precision + 1 convergent-quadrature + 1 exact-inversion + closed form**: machine — (T1) the rotation tick is an oscillator phase rotation ($R(\Omega)$ orthogonal/$\det1$, $2\times10^{-17}$) whose Wick-rotated transfer operator $T=e^{-\Omega(\hat N+1/2)}$ has Gaussian-vacuum per-mode flux moment $\langle\phi^2\rangle=1/(2\Omega)$ (number-basis diag, $3\times10^{-16}$). Convergent — (T2) the vacuum flux variance $\sigma_\phi^2=\langle1/(2\Omega(k))\rangle_\text{BZ}$ on the actual `rotation_omega_2d` $\to0.40297$ (Richardson $r=0.499$), giving the headline closed form $\sigma_1=\tfrac14\langle1/\Omega\rangle_\text{BZ}=0.20148$. Exact — (T3) the map $\gamma(\Omega)=(s_1^\text{clock})^{-1}(e^{-\sigma_\phi^2/2})$, $\gamma^\star=1.780$, clock round-trip $10^{-16}$, monotone in stiffness; (T4) F99 D4 limits recovered from the rule (stiff $\Omega$→deconfined, soft→confining). Consistency (not identity) — (T5) $\sigma_1\approx0.20$ shares order & BZ-inverse-dispersion origin with F70 floor $\sigma(20)=0.219$ and F95 $I_2=0.2202$. Confinement scale and propagation speed are two faces of one dispersion ($c_\text{lat}=d\Omega/d|k|$ slope, $\sigma=\tfrac14\langle1/\Omega\rangle$ inverse zone-average). Scope: Gaussian/spin-wave regime, 2D area-law, O(1) form factor on absolute $\sigma$. 5/5 PASS. Previous: 2026-06-05 - 14:40 (**F99** — $\sigma$ derived from the QCA rule as the centre-twist Lagrange multiplier of $\mathbb{Z}_N$ non-closure (closes F97 §8 / F98 §4); **3 new exact + 1 machine-precision + 1 reconciliation**: exact — (D1) the centre-projection area law $\sigma_k=-\ln s_k$, $s_k=z(2\pi k/N)/z(0)$, $z(\theta)=\sum_n p(n)e^{in\theta}$, with $s_0=1$ ($\sigma_0=0$) identically, centre-periodicity $s_{k+N}=s_k$, and $k\!\leftrightarrow\!N\!-\!k$ degeneracy (sympy, symbolic $\mathbb{Z}_3$ weights) — re-derives F98 E3/E5 from the rule; (D2) the Lagrange/twist identity — $\theta_k=2\pi k/N$ is the multiplier conjugate to centre charge, stationarity of $\ln z(\theta)-i\theta c$ gives $c=-i\,z'/z$, $\sigma_k=f(\theta_k)=-\ln s_k$, $f(\theta_0)=0$ (no price on closure) — so $\sigma$ **is** the multiplier; (D4) rule→weight $p(n)\propto e^{\gamma\cos(2\pi n/N)}$ with exact limits $\sigma_1(\gamma{\to}\infty)=0$ / $\sigma_1(\gamma{\to}0)=\infty$, monotone. Machine — (D3) the real SU(3) gluon rule is centre-covariant: slice twist $zI$ ⇒ Polyakov $\to z$·Polyakov ($5.0\times10^{-16}$), contractible Wilson loops invariant ($0.0$). Reconciliation — (D5) $-\ln s_k$ is the same law as F70 $\sigma(\beta)=-\ln w(\beta)$ (table reproduced: $3.543/2.811/2.051/1.274/0.624/0.219$ at $\beta=0.5..20$); F86 $\sigma_k=2\pi v^2 k$ the small-σ Abelian-BPS limit. Honest scope: area-law step 2D-exact / strong-coupling beyond (3+1D σ still F94); centre-Lagrange identity rep- & $D$-independent; $\gamma(\Omega)$ map limits-only. 5/5 PASS. Previous: 2026-06-05 - 14:05 (**F98** — testing the F97 §4 closure principle "enforcer of the centre-phase budget = the binder" via P1 Options A/C; **3 new exact + 1 machine-precision**: exact — Option C $\sigma_\text{BPS}=2\pi v^2|n|$ vanishes **iff** the centre budget closes (N-ality 0), multiplier $=$ centre charge ($\sigma(2)=2\sigma(1)$, BPS Tier-1); Option A asymptotic $\sigma_k=\frac{k(N-k)}{N-1}\sigma_1$ depends on N-ality **only**, centre-periodic $\sigma_0=\sigma_N=0$ with $k\!\leftrightarrow\!N\!-\!k$ degeneracy (exact rational, SU(3)); the Lagrange-price structure $E_\text{iso}(\text{closed})=0$ vs $E_\text{iso}(\text{open})=\sigma R\to\infty$ (exact). Machine — A↔C bridge round-trip $\sigma_C(v^*{=}\sqrt{\sigma_A/2\pi})=\sigma_A$ to $<10^{-12}$ (F94 CMP2). One identification: centre charge $k$ is both budget label and binder coefficient, so $\sigma=0\iff$ budget closes — the quantitative form of F97 §4 and the §8 bridge. Honest scope: C (Abelian-BPS) $\sigma_2=2\sigma_1$ vs A (non-Abelian Casimir) $\sigma_2=\sigma_1$ agree on $\sigma_0=0$, $\sigma_{k\ne0}>0$; Lagrange statement structural. 5/5 PASS. Previous: 2026-06-05 - 13:40 (**F97** — baryon-sector no-go for the F92 fixed point; **5 new exact-algebraic + 1 quantitative**: exact — the cap-coincidence theorem, the unitarity cap $\arcsin(N^{-1/2})$ and the wrap cap $\pi/(2N)$ coincide **iff** $N\in\{1,2\}$ (at $N=2$: $\sin45°=1/\sqrt2$ exact; for $N\ge3$ strictly split since $\sin x<x$ and $\pi/(2N)<N^{-1/2}\iff N>\pi^2/4$), so F92's triple saturation is a two-body theorem; both $N=3$ consistency fixed points in closed form — trilinear $3\sqrt3\sin^3t=\sin3t\iff\sin^2t^*=(9\sqrt3-12)/11$ ($t^*=34.831°$) and bilinear $3\sin^2t=\sin3t\iff\sin t^*=(\sqrt{57}-3)/8$ ($t^*=34.662°$), residuals 0 at 50 dp — both over-wrap ($3t^*>90°$), landing inside the forbidden gap $(30°,35.264°)$ ⇒ **no F92-type phase-kinematic baryon exists**; the stable-triple per-constituent cap $m_c\le\sin(\pi/6)=1/2$ exact (the $N=3$ analog of F73's $1/\sqrt2$); and the $\mathbb{Z}_3$ centre-phase closure arithmetic $qqq\to2\pi\equiv0$, $q\bar q\to0$, diquark $\to4\pi/3\ne0$ (exact). Quantitative — PDG quark-sum/proton $=0.96\%$: the no-go is confirmed by data (baryon mass is confinement energy, F70/F86/F94, not phase kinematics). Theorized (structural): one closure grammar across sectors — stability = exact phase-budget closure, enforcer = binder (unitarity wrap ↔ F92 pair; $\mathbb{Z}_3$ centre ↔ F71/F86 baryon). 7/7 PASS. Previous: 2026-06-05 - 04:55 (**F96** — the second-shell $E_g$ gap computation; **5 new exact-algebraic + 2 structural/numeric theorems + 1 constructive demo** [numbers to reconcile with the F86–F95 concurrent blocks]: exact — the channel decomposition $\sum_ay_a^2=3\bar y^2+e^2$ with $(\sum y)^2$ pure $A_{1g}$ and the $r{=}1$ separability identity (sympy 0); the stationarity theorem $\partial E/\partial y_a=\kappa_Ey_a+\lambda+g'(y_a)$, $\lambda=(\kappa_0-\kappa_E)\bar y$ (sympy 0); and the massless-electron texture algebra — $Q(u)=\frac{1+u^2}{(1+u)^2}$, $\tan\delta=\frac{\sqrt3u}{2-u}$, with $Q=\tfrac23\iff u=2-\sqrt3=\tan15°\iff\delta=15°$ exact and $\cos3\delta=1/\sqrt2$ ($3\delta=45°$). Structural — the **two-value theorem**: stable-value census max $=2$ over both amplitude→mass maps, $\kappa_E\in[10^{-3},3]$, $\lambda\in[-0.3,0.3]$ ⇒ a strictly quadratic-cost gap theory supports at most two distinct generation masses; realized on the $13\times13$ phase maps (zero three-distinct minimizers; canonical strong splits exactly on the wall $y_\text{heavy}=1.0$) — F93-O5's quartic no-go made dynamical. Constructive — $W(\sum_ap_a^3)^2$ (the sextic $e^6\cos^23\delta$; square root = F95's cubic) unlocks the three-distinct phase (30 minimizers). Consequence: the observed three distinct lepton masses exclude the quadratic theory — F95's $C$ is necessary for a third independent reason and demonstrably sufficient; measured $\delta=12.733°$ vs the curve's exact $15°$ at Koide is the $m_e>0$ displacement. 8/8 PASS. Previous: 2026-06-04 - 23:30 (**F95** — half of F93's last number derived from the QCA rule; **3 new exact-algebraic + 1 quantitative-closed-form + 1 structural no-go** [numbers to reconcile with the F86–F94 concurrent blocks]: exact — the harmonic selection theorem $\sum_a\cos(k(\delta+2\pi a/3))=3\cos k\delta$ iff $3|k$ else $0$ (roots of unity, $k=1..10$; derives the F93 Landau angular form for ANY analytic per-generation energy), the cubic invariant of $\sum_a y_a^4$ equals exactly $3\bar yA^3\cos3\delta$ ($A_{1g}\times E_g$ interference — vanishes iff $\bar y=0$; pure-$E_g$ has no $\cos3\delta$ through $y^8$), and the closed form $B_\text{lead}=-\tfrac{I_2}{2}3\bar yA^3=-3\sqrt2\,I_2\,\bar y^4$; quantitative — $I_2=\langle\cot\omega_\text{kin}\rangle_\text{BCC}=0.2202$ ($L{=}16/24/32$: $0.21569/0.21913/0.22016$), closed form vs full nonperturbative BZ potential rel $1.4\times10^{-4}$, scaling $|B|\sim\bar y^{3.99}$ / $C\sim\bar y^{7.2}$, physical lock $|B|/(2C)\sim10^{31}$ at $\bar y_\text{phys}=2.4\times10^{-10}$, cap value $2.03$ at $\bar y=0.41$; structural no-go — any per-axis $\sum_a u(m_a)$ shares the $B\sim\text{amp}^4$ vs $C\sim\text{amp}^{\sim8}$ split, so the brake $C=0.636|B|$ the data demand cannot come from a second loop: localized to the second-shell $E_g$ self-interaction at saturation-scale amplitude. Sign result: $B<0$ ⇒ $\delta\in[0°,30°)$ predicted, data $12.73°$ ✓; $\delta^*_\text{loop}=0$ would force $m_e=m_\mu$ — falsified, brake proven to exist. 7/7 PASS. Previous: 2026-06-04 - 20:45 (**F92 + F93** — the two F84 irreducible structural inputs attacked; **7 new exact-algebraic + 2 machine-precision + 2 quantitative** [numbers to reconcile with the F86–F91 concurrent blocks]: **F92 exact** — the consistency theorem $2\sin^2t=\sin2t\iff t=\pi/4$ unique on $(0,\pi/2)$ with $Q(\pi/4)=2/3$ (sympy `solveset` exact; the F73 pair-sum and F78 bilinear mass laws are jointly satisfiable only at 45°), the Fock pair factor $(a^\dagger)^2|0\rangle=\sqrt2|2\rangle$ (residual 0), the F73 cap re-derived as pair-amplitude unitarity $y=\sqrt2\sin t\le1\iff m_c\le1/\sqrt2$ with triple saturation at 45°, and the F27 mass-step allocation $(\cos t,\sin t)$ bit-for-bit ($0.0$ code / $1.1\times10^{-16}$ $D_k$); **F92 quantitative** — the data pin the pair normalization $c^2=2\cot\phi_\text{lepton}=2.000018$ ($1.9\times10^{-5}$). **F93 exact** — $\mathrm{sym}(T_{1u}\otimes T_{1u})=A_{1g}\oplus E_g\oplus T_{2g}$ with the diagonal sector exactly $O_h$-invariant ($E_g$ = the unique non-mixing mass splitter), shell decompositions $[1,1,3,3]$ (1st, no $E_g$) vs $[1,2,3]$ (2nd, $E_g$ present — the orthorhombic field's home), stabilizer counts $|D_{2h}|=8$ with 0 axis permutations at generic $E_g$ angle vs $|D_{4h}|=16$ at $\delta=0$ (F84's $\kappa=0$ as a stabilizer theorem), the $E_g$≡$Z_3$-cosine identity $d_a=e\sqrt{2/3}\cos(\delta-2\pi(a-1)/3)$ (sympy 0, F76-C6 is an $E_g$ condensate), and the sextic Landau criterion (ortho iff $C>0,|B|<2C$, $\cos3\delta^*=-B/2C$; 169-point phase map 0 mismatches, quartic theory and quartic $T_{1u}$-vector OP provably never orthorhombic); **F93 machine** — BCC dispersion exactly $O_h$-symmetric, $\{\omega^\pm(Rk)\}=\{\omega^\pm(k)\}$ at $4.7\times10^{-16}$ over 48 ops × 10 k (zero explicit $E_g$ ⇒ the break must be spontaneous); **F93 quantitative** — lepton condensate angle $\delta=12.7328°$ (generic), $A/\bar y=\sqrt2$ to $1.3\times10^{-5}$, masses reconstructed to $1.8\times10^{-14}$, remaining free number $\cos3\delta=0.785874$. F92 5/5, F93 8/8 PASS. Previous: 2026-06-04 - 14:40 (**F91 migration** — BCC gluon propagator `gluon_rotation_step_spectral_bcc` switched chiral→even law to conform to the F91 pairing-classification theorem; free-gluon dispersion now machine-checked against $\Omega_\text{even}$ ($1.8\times10^{-13}$, FG7 PD.4) instead of $\Omega^+$; massless reduction still bit-for-bit $0.0$ (PD.3). No new identity — a conformance change; regression FG7 20/20, E2E 14/14, F91 13/13, FG7d 6/6, FG7e 8/8, F72 PASS. Previous: 2026-06-04 - 14:05 (**F91** pairing classification theorem — **3 new exact (ℚ/structural-zero) + 4 machine-precision** [numbers to reconcile with concurrent F90 block]: exact — γ axial coupling $Q_L-Q_R\equiv0$ over ℚ; W± right-branch weight $T_3^R=0$ over ℚ with $\|P_L\psi_R\|=0.0$ and the F67 separation $|\Omega^s-\Omega_\text{even}|=|\Delta\Omega|/2$ ($1.4\times10^{-17}$); photon uniqueness — axial of $aT_3+bY/2$ equals $(a-b)T_3$ over ℚ, zero iff coupling $\propto Q$ (the Weinberg rotation isolates all axial coupling in the Z). Machine — same-branch bilinear rate $=\Omega^s$ ($2.1\times10^{-14}$); $\Omega^+(-k)=\Omega^-(k)$ ($0.0$) and chiral step $F^\pm$ at exactly $\Omega^\pm$ ($0.0$); colour coupling branch-blind commutator ($1.1\times10^{-16}$) with colour-phase branch split exactly $0.0$; even octet step non-birefringent $S=0.0$, norm $6.8\times10^{-15}$. Quantitative: massive-Z neglected split $8.6\times10^{-4}$ at $m_Z{=}0.4,k{=}0.2$ ($\sim k^3$). Net: W± chiral FORCED, gluon chiral UNFORCED (even forced; BCC migration recommended), Z mixed/derived. 13/13 PASS. Previous: 2026-06-04 - 01:59 (**F90** E2E non-Abelian W/Z/gluon couplings on the σ-bilinear + closed fermion↔field back-reaction loop — **2 new exact-algebraic + 5 machine-precision + 3 quantitative** [numbers to reconcile with the concurrent F88/F89 blocks]: exact — the chiral-Proca birefringence closed form $\Delta\omega_\text{eff}=(\Omega^{+2}-\Omega^{-2})/(\omega^+_\text{eff}+\omega^-_\text{eff})$ ($\le10^{-15}$ rel over 5 masses) and the $m_g{=}0$ gluon massive→free reduction **bit-for-bit ($0.0$)** alongside the bit-for-bit source kicks (W $4.4\times10^{-16}$, colour $2.2\times10^{-16}$, massive-Z $2.2\times10^{-16}$) and the zero-current/g=0 controls ($0.0$ exact); machine — the **work–energy ledger** $\Delta U_\text{field}=g\,dt\sum J\!\cdot\!E_\text{rot}+\tfrac12g^2dt^2\sum|J|^2$ with a real evolving doublet ($4.0\times10^{-17}$, 30 ticks; $6.9\times10^{-18}$ inside the closed loop), closed-loop fermion norm ($6.4\times10^{-15}$, 20 ticks), global SU(3) covariance $J(Vq)=R_\text{adj}J(q)$ + sourced-step commutation ($3.1\times10^{-15}$), source-basis identity at $g'=g\tan\theta_W$ ($1.8\times10^{-15}$), Proca $m{=}0$ reductions even==even/chiral==chiral ($2.8\times10^{-13}$); quantitative — causal W/Z/gluon fronts (zero at emission, arrival after $d\sqrt3$ ticks) and the **monotone mass suppression of the σ-channel birefringence** ($1.03\times10^{-2}\to1.18\times10^{-3}$, $m:0\to2$). Also repairs the stale WB.5 (F37 alias) — Phase-7 back-reaction suite 5/5 again. 14/14 PASS. Previous: 2026-06-04 - 01:25 (**F89** singlet bilinear is the paired photon — **1 new exact-algebraic + 4 machine-precision** [numbers to reconcile with the concurrent F88 colour-condensate block]: the same-branch σ-channel split equals `pair_birefringence` **exactly ($0.0$)**; machine: cross-branch singlet $\phi^T(i\sigma_y)\psi$ rate $=\Omega_\text{pair}=$ `_f26_rotation_step` angle ($4.9\times10^{-13}$, 8 ticks × 2000 k, branch-swap symmetric $1.2\times10^{-13}$), same-branch rates $=\Omega^\pm$ ($2\times10^{-14}$), Hermitian σ⁰ channel invariant under same-branch transport ($2.8\times10^{-15}$), σ-vector adjoint precession by exactly $2\omega$ ($6.1\times10^{-14}$). One entity, two channels: photon = singlet/cross-branch pairing, W/Z/gluon = σ-vector/same-branch — the even/chiral propagator split derived, not stipulated. 10/10 PASS. Previous: 2026-06-03 - 02:10 (**F87** charge-coupling path re-verified end-to-end on the paired photon — **2 new exact-algebraic + 1 machine-precision** [numbers to reconcile with the concurrent F86 colour-dielectric block]: the **Peierls loop holonomy = q·Φ_enc by discrete Stokes** (residual $1.1\times10^{-16}$, the link sum telescoping to the enclosed plaquette-flux sum) and **exact charge linearity** $W(q)=q\,W(1)$ over $q\in\{1,2,3\}$ alongside **Ampère $\nabla\times B=J$**, both residual $0.0$; plus **dynamical Gauss conservation** $iC\!\cdot\!E-\rho$ to $2.0\times10^{-12}$ over 100 sourced ticks, guaranteed by $C\cdot(C\times x)\equiv0$ ($5.3\times10^{-16}$) so the even-law curl sources no charge under continuity $\partial_t\rho=-iC\cdot J$. Supporting machine-precision: $\nabla\times A=B$/$\nabla\!\cdot\!A=0$ ($\sim10^{-17}$), helicity-blindness $|\phi_+-\phi_-|$ & $[P,U^\pm]$ ($\sim10^{-16}$, F68 dynamical), $\nabla\!\cdot\!B=0$ over 50 ticks ($2.0\times10^{-11}$), resolved-sector magnetostatics $iC\times B=J_T$ ($1.4\times10^{-15}$), E2E holonomy$=$flux on a current-sourced tube ($3.6\times10^{-15}$, enclosed flux $15.9$, field-free path $|B|_\text{path}/|B|_\text{peak}=3.3\times10^{-9}$). Module `ca_charge_coupling.py`; two lattice fixes — odd-in-$k$ curl symbol (real-field), odd $L$ (skip Nyquist self-pair, cf. F37). 20/20 PASS. Previous: 2026-06-02 - 20:05 (F83 fixing the lattice spacing `a` from a measured fermion mass via the F46/F12 map — **2 new exact-algebraic (#172–173) + 1 machine-precision (#63)**: the rest-leg map gives $a=\sqrt d\,\arcsin(m_\text{lat})\,\bar\lambda_C$ (#172), which is *one equation in two unknowns* — a single measured mass cannot fix $a$, only the ray $a(m_\text{lat})$ with ceiling $a\le\sqrt d\,\tfrac\pi2\bar\lambda_C$ set tightest by the **top quark** ($3.11\times10^{-18}$ m $\approx1.9\times10^{17}\,\ell_P$, ~17 decades above $\ell_P$); pinning $a$ at F61's $3.81\,\ell_P$ instead inverts to give each fermion $m_\text{lat}\ll1$ (electron $9.2\times10^{-23}$); plus the $\sqrt d$ reconciliation of si-units-options §3.3 (#173, ratio $=\sqrt3$ to $<10^{-6}$) and the round-trip inversion at $2.48\times10^{-16}$ (#63). Honest limit: $a$ still needs a second anchor (gravity $G$-match or GRB floor); F83 brackets any first-principles $a$ to $(0,3.1\times10^{-18}]$ m. 5/5 PASS. Previous: 2026-06-02 - 02:35 (F79 Newton's constant from the lattice structure, Sakharov-free — **1 new machine-precision + 1 exact-algebraic (#164–165)**: the source-free EM stress tensor is traceless in 3+1D ($\lvert T^\mu{}_\mu\rvert_\text{max}=3.6\times10^{-15}$, #164) so the gravity field $K$ — a conformal-factor *reparametrization* of the $(\mathbf E,\mathbf B)$ rotation rule, not a fundamental field — gets **zero tree stiffness**, which converts F60's loop-channel choice from a stated premise into a theorem ($1/G$ has no tree term to compete with); and with $g_*=48$ now structural ($16$ anomaly-free Weyl/gen $\times\dim T_{1u}=3$ via F75, no 4th generation), the induced coupling is parameter-free, $1/G=2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3)$ with $2\pi\eta g_*\sqrt d=8\pi\sqrt3=43.531$ and the dimensionless prediction $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$ (#165; closed form returns CODATA $G$ to $3\times10^{-8}$). Honest limit: a dimensionful $G$ still needs one ruler (the model predicts $a/\ell_P$); the independent anchor is a measured fermion mass via the F46/F12 map. 6/6 PASS). Previous: 2026-06-01 - 20:05 (F77 self-consistent NJL gap + RPA — **2 new exact-algebraic + 2 machine-precision**: the NJL critical coupling $G_c\Lambda^2=\pi^2/(N_cN_f)=\pi^2/6$ (#160, the dynamical-mass analogue of F74's $g_c$) and the polarization split $\Pi_S-\Pi_\text{PS}=-8N_cN_fM^2K$ (#161, $1.8\times10^{-16}$); plus the chiral-limit Goldstone $m_\pi=0$ (#61) and NJL mean-field $m_\sigma=2m_c$ (#62), both $2.3\times10^{-14}$, where one coupling $G$ generates $m_c$ via the gap equation AND fixes the meson poles via the $q\bar q$ ladder. Quantitative: the canonical SU(2) fit reproduces measured $m_c=311$/$f_\pi=92.6$/$m_\pi=140.5$ MeV and $\langle\bar qq\rangle^{1/3}=-249$ MeV (0.2–4.2%) + GMOR/Goldberger–Treiman; the G-scan shows $m_\sigma/(2m_c)\ge1$ for all couplings ⇒ $E_b\le0$, so the self-consistent scalar confirms F74's near-no-go (EW target $m_H/2m_t=0.363$ unreachable). Previous: 2026-06-01 - 16:42 (F70 + F71 confinement & first hadron — **the F43/FG-7 confinement follow-up is closed and the first composite hadron is built; ~13 new exact-algebraic identities + 5 machine-precision + 2 quantitative**: F70 gives a correctly-implemented Wilson gradient-flow/cooling driver (cold fixed point $0.0$; su(3) force $5.6\times10^{-16}$; **gauge-covariant** $\text{flow}(U^g)=\text{flow}(U)^g$ $7.8\times10^{-15}$; diffusive Laplacian rate $\propto\hat k^2$ $4.9\times10^{-10}$) and — via the exact 2D area law $\langle\tfrac1N\mathrm{Re}\,\mathrm{Tr}\,W\rangle=w(\beta)^{RT}$ ($w$ from deterministic SU(3) Weyl-torus quadrature) — a **string tension $\sigma(\beta)=-\ln w>0$ for every finite $\beta$**, a **loop-size-independent Creutz ratio $\chi=\sigma$** ($2.2\times10^{-16}$), and an **exactly linear static potential $V(R)=\sigma R$** ($8.9\times10^{-16}$): an isolated quark costs infinite energy. F71 builds the colour-singlet baryon $B=\varepsilon_{abc}q_1^aq_2^bq_3^c$ (proton $uud$): gauge invariance $B\to\det(V)B=B$ ($1.2\times10^{-15}$), zero colour charge $G^a|S\rangle=0$ & Casimir $0$ ($1.4\times10^{-16}$), exact $Q=1,B=1$ (Fraction), $S_3$-symmetric spin-flavour wavefunction and total Fermi antisymmetry (both $0.0$), and energetic binding $V(R)=\sigma R\to\infty$. F70/F71 logged as labelled sub-blocks (numbering-reconciliation caveat). Previous: 2026-06-01 - 15:02 (F69 paired-spinor photon — **two new exact identities + one machine-precision result**: the pair dispersion $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$ equals both the branch-sum and the even-law rotation rate of `_f26_rotation_step` (residual $0$, 2000 $k$), the pair phase equals the sum of the two real Weyl constituent phases (residual $0$, "only occurs as a pair"), and the paired photon is non-birefringent ($S=\phi_++\phi_-=-1.8\times10^{-15}$ over 6 ticks vs the retired chiral bilinear's $-\Delta\Omega N=+0.079$); quantitative: massless (gap $\Omega(0)=0$) and luminal ($\Omega/k\to1/\sqrt3$, group velocity FD $7.7\times10^{-6}$), transverse ($|\mathbf E\!\cdot\!\hat k|/|\mathbf E|=1.8\times10^{-17}$), real+norm-conserving ($10^{-15}/6\times10^{-15}$). Establishes the EM photon as the bound (+,−) spinor pair (`ca_photon_pair.py`); composite σ-bilinear retired as the photon (kept for W/Z/gluon). Previous: 2026-06-01 - 14:41 (F68 minimal coupling forces the even photon — **one new machine-precision identity + one exact identity**: the U(1)/hypercharge coupling $P=e^{i\theta}\mathbf I$ commutes with the Weyl unitary $U^\pm(k)=u\mathbf I-i(\mathbf n\cdot\boldsymbol\sigma)$ on both branches (residual $1.1\times10^{-16}$, helicity-blind), and the real `mass_step_1flavor_u1` advances both helicity channels by an equal phase (split $=0.0$, exact) ⇒ minimal coupling sources only $\Omega_\text{even}$ (non-birefringent). Structural: $\lVert[\sigma_x,\mathbf n\cdot\boldsymbol\sigma]\rVert=1.99\neq0$ ⇒ the composite $\sigma$-bilinear is a different SU(2) channel carrying the birefringence ($\Delta\Omega$ gap $1.03\times10^{-2}$ on the body diagonal vs $0$ in the even channel). Establishes the charge-coupling photon is the identity-channel even photon (F66 option 1 derived); the composite bilinear is a separate channel. Previous: 2026-06-01 - 14:23 (F67 even-law photon vs the two-branch bilinear — **two new machine-precision/exact results**: the bilinear→even conversion override equals $+\Delta\Omega/2$ on *both* helicities (residual $1.4\times10^{-17}$, algebraically exact), and the even law nulls the birefringence observable $S=\phi_++\phi_-$ to $1.8\times10^{-15}$ while the chiral law gives $S=-\Delta\Omega\,N$ to the same floor; quantitative: even-law group velocity $\to1/\sqrt3$ (FD $7.7\times10^{-6}$), even step real+norm-conserving ($9\times10^{-16}$/$7.7\times10^{-15}$), body-diagonal override $=(\sqrt3/54)k^2$ ($5\times10^{-6}$). Establishes the composite bilinear photon (birefringent) and the chirality-even gauge photon (non-birefringent) are mutually exclusive, separated by exactly the excluded birefringence. Tested against the model's real propagators `_f26_rotation_step`/`w_propagation_step_chiral`. Previous: 2026-05-31 - 22:02 (F64 canonical-form adoption + D-EM10/D-EM11 — **canonical dielectric K=e^{2GM/rc²} adopted (AB≡1 exact; PPN β=γ=1, GR-identical); the 4πG coupling pinned to the lattice; co-evolving self-redshift confirmed**: (D-EM10) the 4π is the exact 3-D lattice Green's function (point-source FFT Poisson recovers GM=0.988→1; F58: 4πC=1.0004) and G is the Sakharov-induced value pinned by the cell scale a=√(2πη g_*)·d^{1/4}·ℓ_P with η_Weyl=1/12 (F61) — closed form reproduces F61's table (g_*=16→3.809 ℓ_P) — with 1/G∝1/c_lat=√d to MC precision (√2,√3,√4 for d=2,3,4); so 4πG is no longer "by hand". (D-EM11) two rest packets co-evolved in the genuine self-sourced dielectric, clocked by a resolution-free Hilbert instantaneous-frequency estimator, give a redshifted deep/rim ratio 0.931 vs local-lapse 0.860 (8.3%, gradient-sampling-limited). Canonical K=e^{2u} wired into all dynamical maps + docs/theory/key-decisions.md/CLAUDE.md; weak-field battery unchanged (forms agree at O(u)); D-EM-D2b redshift tightened to 0.8966 vs 0.8966. Battery 16/16 PASS. Previous: 2026-05-31 - 16:46 (F64 D-EM7/D-EM8/D-EM9 maturation — **new exact-algebraic PPN identities + quantitative dynamical results, and a falsifiable strong-field correction**: (D-EM9) the dielectric metric's PPN parameters are exact rationals — $\gamma=1$ for all forms (light bending GR-identical, $4GM/bc^2$), while the redshift-fixed $K=(1-u)^{-2}$ has $\beta=\tfrac12$ (perihelion factor $7/6$ ⇒ Mercury $50.1''$/cy vs observed $42.98''$, excluded by MESSENGER $\beta-1=(0.2\pm2.5)\times10^{-5}$) and the impedance-matched $K=e^{2u}$ has $\beta=\gamma=1$ (GR-identical) — so the 2nd-PPN order selects the nonlinear completion $K=e^{2GM/rc^2}$ the linear (D-EM5) derivation left open. (D-EM7) absolute ray deflection $K_\text{bend}=4.165/4.016/4.0015$ at $GM/bc^2=10^{-2/-3/-4}$ → 4 from above (true 3-D $1/r$, removing the 2-D log caveat). (D-EM8) $\Phi$ promoted to a dynamical field $\Box\Phi=-4\pi G\rho$: Poisson well a static fixed point (rel dev $8.8\times10^{-4}$), free pulse causal at $1.014\,c_g$, energy drift $5.3\times10^{-3}$. Battery 14/14 PASS. Previous: 2026-05-31 - 16:31 (F64 D-EM5/D-EM6 build-out — **the dielectric placement is now DERIVED, not posited, via a chain of exact-algebraic identities, plus one quantitative dynamical result**: (D-EM5) the Plebanski equivalent medium of a static isotropic metric is $\varepsilon=\mu=\sqrt{B/A}$ — $=K$ for both the dielectric rep and its conformal partner; source-free Maxwell's conformal invariance ($\mathrm{diag}(-1/K,K,K,K)=K\cdot\mathrm{diag}(-1,K^2,K^2,K^2)$) means the EM sector fixes only the conformal class ($n=K$); requiring a *proper* rotation (impedance $Z=\sqrt{\mu/\varepsilon}=1$) with $n=\sqrt{\varepsilon\mu}=K$ has the unique solution $\varepsilon=\mu=K$; and the factor-1 redshift $\sqrt A=1-u$ fixes the conformal factor $\Rightarrow AB=1$ — all exact in sympy. Lattice confirmation: 1-D FDTD reflection at an abrupt index step is $R=0.009$ (matched, grid floor) vs $0.135/0.056$ (refractive-/clock-only, ≈Fresnel) — the reflected wave is the F26 scalar contamination. (D-EM6) a propagating 2-D Maxwell pulse deflects toward a pure-EM-energy lens (Δθ=−0.260, 76% of its eikonal), dielectric/rest-leg ratio exactly 2.000 (Einstein factor-2), where the rest-leg route sources 0 — light bends light. Battery 11/11 PASS. Previous: 2026-05-31 - 16:00 (F64 built out as a complete dynamic field + full battery vs the emergent-gravity module F62 — **one new bit-for-bit identity and one machine-precision result on the new dynamic path**: the dielectric curved-background stepper at $m=0$, flat $A=B=1$, reduces bit-for-bit to two decoupled exact-QCA Weyl walks (residual $0.0$, D-EM-D1, Tier-1 #150), and a self-gravitating dielectric packet conserves norm under its own evolving metric ($7.5\times10^{-16}$ over 60 ticks, D-EM-D3a, Tier-2 #59); the self-field dielectric/rest-leg eikonal index-slope ratio is exactly $\mathbf{2.000}$ (D-EM4, the same algebraic identity already logged for D-EM2). Dynamic battery 9/9 PASS on F62's same exactly-unitary stepper (only the metric placement differs); quantitative dynamic matches — free-fall $0.910$ + mass-universality $0.085$ ($=$ F62), redshift $0.8966$ vs $0.8915$ ($=$ F62), deflection $K_\text{meas}=-4.006$/$K_\text{eik}=-4.18$ (cleaner than F62's $-3.43/-3.92$, from one field), D-EM4 self-sourced redshift $0.833$ vs $0.822$. Full side-by-side `test-results/F64_vs_F62_comparison.md`. Previous: 2026-05-30 - 21:30 (F64 electromagnetic-connection gravity fork — **one new exact-algebraic structural identity (multi-part), no new machine-precision identity**: of the three single-scalar metric placements, only the impedance-preserving dielectric ($\varepsilon=\mu=K\Rightarrow A=1/K,B=K$) gives *both* the factor-1 redshift slope $Z=1$ *and* the factor-2 deflection $K_\text{bend}=4$, with impedance $\sqrt{\mu/\varepsilon}=1$ exactly $u$-independent — all exact in sympy series (the reciprocal lock $AB=1$ resolves the Finding-19 single-scalar obstruction). Clock-only gives $K_\text{bend}=2$, refractive-only gives $Z=0$. Quantitative downstream: lattice eikonal $K_\text{bend}=3.90$ (dielectric) vs 1.95 (rest leg) on one FFT-Poisson field, ratio **2.0000000**; radiation-shell vs equal-energy mass deflection ratio 1.00002 with rest-leg coupling sourcing 0.0 from massless field energy; mpmath guard $|K_\text{bend}|\to4$. Previous: 2026-05-30 - 21:06 (F63 Einstein–Cartan spin-torsion magnitude estimate — **one new exact (rational) coefficient + one exact-algebraic closed form, no new machine-precision identity**: the EC four-fermion prefactor $3/16$ exact, and the torsion/Dirac energy-density ratio $r_\text{cutoff}(f)=\tfrac{3\pi}{2}f(\ell_P/a)^2=\tfrac{3f}{4\eta g_*\sqrt d}$ as a closed form. Quantitative downstream: worst-case $r=2.9\times10^{-3}$ across F62's four packet densities (torsion-free assumption costs nothing measurable), lattice Cartan density $f^*=3.08$ quanta/cell. Conservative inputs (polarised bound $j_5\le n$, rest-floor $\omega\ge m$), bounded estimate not a dynamical torsion sim. Previous: 2026-05-30 - 16:10 (F62 dynamical Dirac CA on a curved background + linearized backreaction — **one new bit-for-bit identity and one machine-precision result**: the D1 flat-space regression (gravity stepper at $m=0$ ≡ two decoupled exact-QCA Weyl walks, residual $0.0$, Tier-1 #149) and norm conservation under a self-sourced evolving metric ($2.5\times10^{-15}$, Tier-2 #58). Quantitative D2/D3a: Rindler free-fall coefficient $|g|/(a\,c_\text{lat}^2)=0.91$ and **mass-universal** (trajectory spread 8.5%, the lattice equivalence principle); dynamical redshift ratio $0.897$ vs $0.891$; eikonal deflection $K=-3.92$ (Einstein factor-2), dynamical 88%; self-redshift loop closes ($0.903$ vs $0.869$). Also flagged a latent sign error in `ca_dirac.dirac_step_2d_varm_splitstep` ($\delta m$ mix sign inverts a mass-gradient force; invisible at $\delta m=0$). Previous: 2026-05-30 - 15:55 (F61 Weyl heat-kernel $\eta$ + mode count $g_*$ — **one new exact (rational) identity and one machine-precision lattice identity**: $\eta_\text{Weyl}=1/12$ exactly from Seeley–DeWitt $a_1$ + Lichnerowicz + fermionic statistics ($c_\text{Weyl}=1/6$), confirming F59's per-Weyl placeholder; and the BCC 2-spinor eigenphase symmetry $\big||\arg\lambda_1|-|\arg\lambda_2|\big|=4.4\times10^{-16}$ (phase-space factor spin-independent). Quantitative downstream: $g_*=16$ per generation ⇒ $P_\text{pre}=\sqrt{\pi g_*/6}=2.894$, $a=3.81\,\ell_P$, $\tau=2.20\,t_P$ at $d=3$; gauge sector not yet included. Previous: 2026-05-30 - 15:25 (F60 induced-$G$ channel reconciliation — **three machine-precision scaling identities**: bare tree-level wave-operator stiffness $S_\text{bare}=c_\text{lat}^{2.0000}$ (lock $S_\text{bare}/c_\text{lat}^2$ spread $1.1\times10^{-16}$), loop-induced graviton stiffness $B\propto c_\text{lat}^{-1.0000}$, and their gap $B/S_\text{bare}\propto c_\text{lat}^{-3.0000}$ (the tree-vs-loop $c_\text{lat}^3$); resolves the F58↔F59 fork in favour of the loop channel under the emergent-gravity premise, $1/G\propto\sqrt d$). Previous: 2026-05-30 - 14:55 (F59 induced-EH prefactor + Finding-10 selection — **no new bit-for-bit identity, but one exact-algebraic scaling result**: $1/G\propto1/c_\text{lat}=\sqrt d$ confirmed to machine precision ($I\cdot c$ $c$-independent, spread $<10^{-6}$), and the consequent $(a,\tau)$ selection $a=\sqrt{2\pi\eta g_*}\,d^{1/4}\ell_P$, $\tau=\sqrt{2\pi\eta g_*}\,d^{-1/4}t_P$ is exact-algebraic in its $d^{1/4}$ power (prefactor $P_\text{pre}$ scheme/mode-count dependent, $\approx1.02$ for $\eta=1/12,g_*=2$); plus quantitative sector split $\int1/(2\omega)\sim\Lambda^{2.085}$ (Newton) vs $\int\omega/2\sim\Lambda^{3.919}$ (CC), correcting F57's $q{=}0$ reassignment; naive spatial-stress bubble $\Lambda^{5.57}$ ruled out). Previous: 2026-05-30 - 13:40 (F58 clock-rate↔rest-mass coupling from the neighbour rule — **two new Tier-2 machine-precision (algebraically exact) results**: Q0 the weak-equivalence-principle identity $1-\sqrt A$ mass-independent at residual $2.2\times10^{-16}$, and Q3a the F25/F26 lock $\text{stiffness}/c_\text{lat}^2=$ const at residual $1.1\times10^{-16}$; plus quantitative: bare-lattice clock-rate Green's-function $4\pi C=1.0004$, Laplacian anisotropy $5.6\times10^{-8}$, Sakharov $G\propto\ell^2$ exponent $2.014$). Previous: 2026-05-29 - 19:05 (F57 induced-EH from back-reaction — **no new exact results**, quantitative only: matter polarization $\Pi(0)\to0.4466$ convergent, induced EH gradient stiffness $\Pi_2=+0.061>0$, and the sector split $\Pi(0)\propto\Lambda^{2.02}$ (vacuum-energy) vs $\Pi_2\propto\Lambda^{0.25}$ (Newton, logarithmic running) — corrects F56's $q{=}0$ identification). Previous: 2026-05-29 - 18:20 (F56 Einstein-coupling derivation — **one new Tier-1 exact (bit-for-bit) result**: C1 the coupling lock, $\xi=16\pi G/c^4$ and $G_{\mu\nu}$ coupling $8\pi G/c^4$ forced by Newton-$4\pi$ + trace reversal at residual $0.0$; plus quantitative: bare-lattice Green's-function $4\pi C=1.0002$, light-cone isotropy spread $2.4\times10^{-5}$, Sakharov $G\propto\ell^2$ exponent $2.0008$ with $\sqrt d/(4\pi^2)$ coefficient to $0.03\%$). Previous: 2026-05-29 - 17:40 (F55 spatial-metric trace reversal — **two new Tier-1 exact (bit-for-bit) results**: J1 the static-dust trace-reversal identity $h_{ij}=h_{00}=-2\phi/c^2$ at residual $0.0$, and J5 the trace-reversed $(A,B)\equiv$ `gr_fork_E_tensor` linearised at residual $0.0$; plus quantitative: deflection factor-2 $K=4.02$ and uniqueness $K(\lambda)=2(1+\lambda)$. Tier-1 numbers to be reconciled with concurrent F53/FG-9 and F54/FG-8 additions). Previous: 2026-05-29 - 17:05 (F52 gravity-from-rest-leg — no new exact/machine-precision identities; **quantitative only**: loop closure $M_\text{eff}/M = 0.97$–$1.00$, factor-1 redshift ratio $0.997$, eikonal deflection discriminator $K_\text{full}/K_\text{rest} = 2.01$, rest-leg-only Newtonian $K=2.0$ vs full-metric Einstein $K=4.0$). Previous: 2026-05-28 - 14:00 (F47 Majorana branch — Tier-1 #136–#138, Tier-2 #51; Higgs-free $\nu_R$ Majorana mass step and see-saw scaling). Previous: 2026-05-28 - 00:40 (F44 W6.10 promotion sanity — Tier-1 #133–#135; covariant Stueckelberg operator now lives in `ca_wmu.py` Phase 5C); 2026-05-28 - 22:50 (F46 spherical Pythagorean lattice-mass identity, Tier-1 #129–#132, Tier-2 #48–#50); 2026-05-28 - 01:30 (F43 FG-7 dynamical SU(3) gluon sector — Tier-1 #116–#128, Tier-2 #43–#47); 2026-05-28 - 00:20 (F44 W6.9 lattice rank-1 verification, Tier-1 #115); 2026-05-28 - 00:05 (F44 rank-1 Stueckelberg mass block, Tier-1 #112–114); 2026-05-27 - 14:30 (F45 σ↔τ swap Weinberg angle, Tier-1 #108–111); 2026-05-27 - 09:00 (F42 hypercharge extension, Tier-1 #105–107); 2026-05-26 - 17:45 (F41, Tier-1 #102–104, Tier-2 #34–37).*

---

<!-- BEGIN GENERATED: header + tally (casim index) -->

*Tally generated by `casim index`; covers every committed result artifact and findings through **F408**. This block used to be hand-maintained and was 125 findings behind its own tree — the staleness metric P1 surfaced. It is generated now, so it cannot drift.*

| Class | Generated rows | What it means |
|---|---:|---|
| **exact** | 166 | residual algebraically zero |
| **machine** | 196 | below the 1e-12 float/FFT floor |
| **quantitative** | 213 | a number inside a declared tolerance |
| **bracketed** | 0 | the range is the result |
| **external** | 0 | measured input from outside the model |

**Coverage: 575 of 575 residual-bearing entries (100.0%)**, across 602 result artifacts. By classification rule: **153 declared** (the entry labels its own class), **24 by record** (the owning test-registry record's `expect.exactness`, D9), **398 by numerical signature** (this document's own criterion: 0 → exact, <1e-12 → machine, larger → quantitative). 15 entries carry a label that is channel or tier metadata rather than an exactness class (`coupled`, `background`, `Tier-B`); those fall through to the later rules rather than being dropped, which is what P1 could not do.

*The curated Tier 1–3 tables below are **not** generated and stay authoritative for the physics claim: they carry a `Predicted form` column that no artifact records. The generated tables at the end of this file are the complete machine-derived view.*

<!-- END GENERATED: header + tally -->

## Reading the table

| Tier | What it means | Numerical signature |
|---|---|---|
| **Exact algebraic** | Identity that holds at the symbolic level; residual bounded by ε per quantity, with no growth in $N$, $L$, or $n_\text{steps}$ | residual / (relevant scale · ε) < 1 |
| **Machine precision** | Holds to FFT / linear-algebra round-off floor; residual grows as $\sqrt{N_\text{cells}}$ per step or $n$ per step | residual ~ 10⁻¹⁵ – 10⁻¹² over the run, scales as predicted |
| **Quantitative** | Numerical match inside a declared tolerance; finer than published-target precision in most cases | residual in declared % band, no claim of analytic identity |

---

## Tier 1 — Exact algebraic results (curated)

| # | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| 1 | BCC unitarity $u^2 + \|\tilde{\mathbf{n}}\|^2 = 1$ (Paper 1 Eq. 15, sign-corrected) | $= 1$ | $4.4 \times 10^{-16}$ over 100 random $k$ | Finding 1; `ca_bcc.py` |
| 2 | Vacuum freezing $N_\text{binary}(\mathbf x_\text{vac}) = 0$ | $= 0$ bit-for-bit | $= 0$ on 80% of $L=256$ lattice | T5.A; `test_emergent_time_T5.py` |
| 3 | F1 vacuum regression ($\Phi = v$ fixed; fermion = constant-$m$ ref) | bit-for-bit identity | $1.1 \times 10^{-16}$ (Φ), $8.4 \times 10^{-16}$ (fermion) | F1; `run_phaseF_tests.py` |
| 4 | F4 symmetry-restored regression ($\Phi = 0$ fixed; η = pure Weyl) | bit-for-bit identity | $\Phi = 0$ exact; η diff $7.6 \times 10^{-16}$ | F4; `run_phaseF_tests.py` |
| 5 | A₀ = 0 audit (Paper 2 central result) | $U(k=0) = I$ | $= 0$ (exact) | V7; `run_qca_verifications.py` |
| 6 | Goldstone dispersion $\omega = \|k\|$ on lattice | massless | residual / ($\|k\|\cdot\varepsilon$) ≤ 0.88 at $L=640$ | Finding 3; `ca_higgs.py` |
| 7 | ~~Composite-photon curl-residual leading coefficient~~ **WITHDRAWN 2026-08-04 (F306, ledger S18)** | $\frac{1}{\sqrt{2d}}$ — measured correctly, but it is a quadrature artifact, not a coefficient (see #49) | $d=2$: 10 decimals at $k=10^{-5}$; $d=3$: 7 figures. *(This row had been retroactively rewritten to read “$=c_\text{lat}/\sqrt2$ (BCC special case; general law in #49)” — a superseded entry edited to point at the entry that superseded it. Original wording restored, then withdrawn.)* | Finding 7 → **F306**; `bilinear{,_2d}.py` |
| 8 | Composite-photon transversality $2\tilde{\mathbf n}\cdot\mathbf E_G = 2\tilde{\mathbf n}\cdot\mathbf B_G = 0$ | $= 0$ | $4.6 \times 10^{-17}$ (3D), $5 \times 10^{-19}$ – $1.8 \times 10^{-17}$ (2D) | L3; `ca_maxwell.py` |
| 9 | Lattice speed of light $c_\text{lat} = 1/\sqrt d$ | dimensionless | algebraic — Bisio *et al.* unique-QCA result | Finding 7 / Finding 10; `docs/theory/ca-reference.md` |
| 10 | SU(2) parity violation — right-chirality leak under left-only rotation | $= 0$ | $= 0.0$ (machine zero) | E2; `ca_weak.py` |
| 11 | Phase-tick / proper-time ratio $N_\text{phase,in}/N_\text{phase,out} = c_\text{in}/c_\text{out}$ | $= c_\text{in}/c_\text{out}$ | $2.7 \times 10^{-16}$ at T2.B Shapiro gate | Finding 11; T2.B / T5.C |
| 12 | Exact 2D QCA dispersion $\omega = \arccos(c_x c_y)$ | $= \arccos(c_x c_y)$ | max $\|\Delta\omega\| = 3.3 \times 10^{-16}$ across 6 modes | V1; `run_qca_verifications.py` |
| 13 | Exact-QCA Dirac dispersion $\omega = \arccos(\sqrt{1-m^2}\,c_x c_y)$ | $\arccos(\sqrt{1-m^2}\,c_x c_y)$ | $3.9 \times 10^{-16}$ residual | Finding 9; `ca_dirac.py` (2026-05-18) |
| 14 | U(1) Aharonov–Bohm phase pickup | $\exp(i\oint A)$ exact | $4.4 \times 10^{-16}$ | E1; `ca_dirac.py` |
| 15 | CHSH Tsirelson saturation on lattice singlet | $|S| = 2\sqrt 2$ exact | $4.4\times 10^{-16}$ pure; $2.2\times 10^{-9}$ after 12 Weyl ticks | Finding 14.3 / QM-1; `tests-priority/test_02_QM1_CHSH.py` |
| 15a | F226 Tsirelson on the **genuine** $2^n$ register (native exchange gate, Horodecki-optimal) | $S_\text{max} = 2\sqrt 2$ exact | $1.8\times 10^{-15}$ residual | F226; `tests/findings/test_F226_bell_tsirelson.py` |
| 15b | F226 CHSH discreteness correction (angle granularity) $\delta S = -3\sqrt2\,(\delta\phi)^2$ | $-3\sqrt2$ curvature, slope 2 | curvature $-4.25$ vs $-4.243$; log-log slope $2.00$ | F226 (Planck-suppressed to $\sim10^{-54}$) |
| 15c | F227 Lieb–Robinson speed $d\Omega/d\lvert k\rvert = c_\text{lat}=1/\sqrt3$ | $= 1/\sqrt3$ exact | $10^{-16}$ (reuses F180) | F227; `tests/findings/test_F227_decoherence_floor.py` |
| 15d | F227 strict causal cone: connected correlation $C(r,t)=0$ for $r>4t$ | $\equiv 0$ outside cone | $<10^{-12}$ | F227 (native exchange brick-wall) |
| 16 | PMNS 3-flavour unitarity $U U^\dagger = I$ | identity | $7.7\times 10^{-17}$ | Finding 14.8 / QFT-5; `tests-priority/test_07_QFT5_neutrino.py` |
| 17 | 2-flavour PMNS oscillation propagator vs analytic $\sin^2(2\theta)\sin^2(\Delta m^2 L/(4E))$ | identity | $4.4\times 10^{-16}$ across $L \in [0, 2000]$ km | Finding 14.8 / QFT-5; ibid. |
| 18 | Chiral charge $Q_\chi$ conservation at $m=0$ (Weyl regression on Dirac stepper) | $\Delta Q_\chi = 0$ | $2.2\times 10^{-16}$ over 500 steps at $L=128$ | Finding 14.13 / QG-4; `tests-priority/test_10_QG4_charge.py` |
| 19 | BCC dispersion exactly linear along $(1,0,0)$ axis ($\omega = k/\sqrt 3$) | identity | $5.7\times 10^{-16}$ (FFT floor) over the small-$k$ band | Finding 14.7 / QG-2; `tests-priority/test_06_QG2_planck_LV.py` |
| 20 | SR-2 Lorentz-violation coefficient $\beta_\text{LV}(m) = \tfrac12(1 - m/(\sqrt{1-m^2}\arcsin m))$ — 2D-square QCA | closed-form analytic function of $m$ | sympy-confirmed; matches numerical SR-2 grid to FFT floor at small $k$ | Finding 15; `casim.engine.interactions.derive_beta_LV` |
| 21 | SR-2 next-order coefficient $\gamma_\text{LV}(m) = \tfrac18 - m(3-2m^2)/(24(1-m^2)^{3/2}\arcsin m)$ — 2D-square QCA | closed-form analytic function of $m$ | sympy-confirmed; sharpens the $\beta_\text{LV}\beta^2$ fit by 2–4 orders | Finding 15; `casim.engine.interactions.derive_beta_LV` |
| 21b | SR-2 third LV coefficient $\delta_\text{LV}(m) = \tfrac{1}{16} - m(8m^4-20m^2+15)/(240(1-m^2)^{5/2}\arcsin m)$ — 2D-square QCA, 2026-05-21 | closed-form analytic function of $m$ | sympy-confirmed bit-zero residual against series; sharpens $\beta_\text{LV}\beta^2 + \gamma_\text{LV}\beta^4$ fit by 2–4 more decimals on the SR-2 grid | `casim.engine.interactions.derive_beta_LV::delta_LV` |
| 21c | SR-2 fourth LV coefficient $\varepsilon_\text{LV}(m) = \tfrac{5}{128} - m(35 - 70m^2 + 56m^4 - 16m^6)/(896(1-m^2)^{7/2}\arcsin m)$ — 2D-square QCA, 2026-05-21 | closed-form analytic function of $m$ | sympy-confirmed bit-zero residual; pattern proof that the recursion continues indefinitely. At $m=0.20, k=0.05$ adds ~40× to the fit precision over $\delta_\text{LV}\beta^6$ truncation | `casim.engine.interactions.derive_beta_LV::epsilon_LV` |
| 22 | Mohr photon polarization basis — transversality $\hat{k}_s^\dagger \hat{\epsilon}_\lambda = 0$ (Eq. 212) | $= 0$ | $1.6\times 10^{-16}$ over 12 random $\hat{k}$ | `ca_maxwell.py` `test_polarization_basis` |
| 23 | Mohr photon polarization basis — orthonormality $\hat{\epsilon}_\lambda^\dagger \hat{\epsilon}_\mu = \delta_{\lambda\mu}$ (Eq. 211) | $= \delta_{\lambda\mu}$ | $5.6\times 10^{-16}$ | `ca_maxwell.py` `test_polarization_basis` |
| 24 | Mohr photon polarization basis — completeness $\sum_\lambda \hat{\epsilon}_\lambda \hat{\epsilon}_\lambda^\dagger = (\boldsymbol{\tau}\cdot\hat{k})^2$ (Eq. 213) | identity | $4.4\times 10^{-16}$ | `ca_maxwell.py` `test_polarization_basis` |
| 25 | Lorentz boost covariance — transversality of boosted wave function $\hat{k}'_s{}^\dagger \hat{\epsilon}' = 0$ (Mohr Eq. 284) | $= 0$ | $1.3\times 10^{-15}$ over 12 random $(k, v)$ pairs, $v/c = 0.6$ | `ca_maxwell.py` `lorentz_boost_covariance` |
| 26 | Lorentz boost covariance — wave-function form preserved: lower$' = \boldsymbol{\tau}\cdot\hat{k}' \hat{\epsilon}'$ (Mohr Eq. 285) | identity | $5.1\times 10^{-16}$ | `ca_maxwell.py` `lorentz_boost_covariance` |
| 27 | Lorentz boost covariance — scalar factor &#124;$\hat{\epsilon}$&#124; $= \xi = \cosh\zeta + \hat{v}\cdot\hat{k}\sinh\zeta$ (Mohr Eq. 287) | closed-form identity | $6.7\times 10^{-16}$ | `ca_maxwell.py` `lorentz_boost_covariance` |
| 28 | Longitudinal mode zero energy: $\boldsymbol{\tau}\cdot\hat{k}\,\hat{k}_s = 0$ (Mohr Eq. 25 → Eq. 241) | $= 0$ | $5.5\times 10^{-17}$ | `ca_maxwell.py` `longitudinal_transverse_orthogonality` |
| 29 | Longitudinal–transverse orthogonality $\psi_T^\dagger \psi_L = 0$ (Mohr Eq. 249) | $= 0$ | $1.1\times 10^{-16}$ | `ca_maxwell.py` `longitudinal_transverse_orthogonality` |
| 30 | Longitudinal mode purely longitudinal $\Pi^T \psi_L = (\boldsymbol{\tau}\cdot\hat{k})^2 \hat{k}_s = 0$ (Mohr Eq. 240) | $= 0$ | $3.7\times 10^{-17}$ | `ca_maxwell.py` `longitudinal_transverse_orthogonality` |
| 31 | SU(3) Gell-Mann normalisation $\mathrm{Tr}(T^a T^b) = \tfrac12 \delta^{ab}$ | identity | $1.1\times 10^{-16}$ | V13 G0; `ca_strong.py::verify_normalization` |
| 32 | SU(3) cold-link vacuum regression — `step_strong_2d(U_\mu\equiv I)` reduces to 3 colour copies of `dirac_step_2d_splitstep` | bit-for-bit identity | **$0.0$ exact** | V13a; `test_su3_noether.py` |
| 33 | SU(3) global adjoint rotation $Q^a \to V_{\text{adj}}^{ab} Q^b$ under $q\to V q$ | $V_{\text{adj}}^{ab} = 2\,\mathrm{Tr}(T^a V T^b V^\dagger)$ identity | $1.7\times 10^{-14}$ abs, $6.6\times 10^{-16}$ rel | V13b3; `ca_strong.py::adjoint_rotation`, `test_su3_noether.py` |
| 34 | Wilson plaquette trace $\sum_\square \mathrm{Re}\,\mathrm{Tr}\,U_\square$ gauge-invariant under per-cell SU(3) rotation $U_\mu \to V U_\mu V^\dagger$ | identity | $4.4\times 10^{-16}$ (machine $\varepsilon$) | V13b4; `ca_strong.py::plaquette_trace` |
| 35 | C5 — Vector spherical harmonic orthonormality $\int Y^{m\dagger}_{jl}\cdot Y^{m'}_{j'l'}\,d\Omega = \delta_{jj'}\delta_{mm'}\delta_{ll'}$ (Mohr §8) | identity | $1.6\times 10^{-15}$ over $j \le 2$, 20×20 Gauss-Legendre × uniform | `ca_maxwell.py::test_vsh_orthonormality` (2026-05-21) |
| 36 | C5 — Magnetic-multipole VSH transversality $\hat n_s^\dagger \cdot Y^m_{j,M} = 0$ (Mohr §8) | $= 0$ | $3.7\times 10^{-17}$ over $j \le 2$, 8 random directions | `ca_maxwell.py::test_vsh_transversality` |
| 37 | C5 — Electric-multipole VSH transversality $\hat n_s^\dagger \cdot Y^m_{j,E} = 0$ where $Y^m_{j,E} = \sqrt{(j+1)/(2j+1)}\,Y^m_{j,j-1} + \sqrt{j/(2j+1)}\,Y^m_{j,j+1}$ | $= 0$ | $1.7\times 10^{-16}$ | `ca_maxwell.py::test_vsh_transversality` |
| 38 | C6 — Maxwell Green-function inverse off-shell: $(H(k) - (\omega + i\varepsilon)I)\cdot G(\omega, k) = I$ at $\omega = 0.5\,c\|k\|$ | $= I$ | $5.2\times 10^{-16}$ across 8 directions | `ca_maxwell.py::test_green_function_inverse` |
| 39 | C6 — Weyl current $J^0 = \psi^\dagger\psi = 1$ for normalized BCC + eigenmode | $= 1$ | $4.4\times 10^{-16}$ | `ca_maxwell.py::test_weyl_current_structure` |
| 40 | C6 — Weyl current $\|\vec J\| = \|\psi^\dagger\vec\sigma\psi\| = 1$ (helicity-saturated) | $= 1$ | $2.2\times 10^{-16}$ | ibid. |
| 41 | C6 — Weyl current $\vec J = \hat n$ (BCC eigenmode spin-axis, $\to \hat k$ in continuum) | identity | $1.5\times 10^{-15}$ at $k_\text{mag}=0.3$ | ibid. |
| 42 | C6 — Maxwell source-term packaging: $\Xi(x) = (-\mu_0 c\, M J, 0)^T$ has zero lower half (Mohr Eq. 57) | $= 0$ | $0.0$ (exact bit-for-bit) | `ca_maxwell.py::test_source_coupling_shape` |
| 43 | C6 — Maxwell source-term upper half equals $-\mu_0 c\,M J$ bit-for-bit | identity | $0.0$ (exact bit-for-bit) | ibid. |
| 44 | Composite-photon bilinear circularity: $\boldsymbol{A}\cdot\boldsymbol{C} = 0$ and $\|\boldsymbol{A}\|^2 = \|\boldsymbol{C}\|^2$ for $G_T = \boldsymbol{A}+i\boldsymbol{C}$ from BCC $\psi_+^T\sigma\psi_+$ (helicity eigenmode) — origin of Poynting energy conservation at any $c$ | $\boldsymbol{A}\cdot\boldsymbol{C} = 0$, $\|\boldsymbol{A}\|^2 = \|\boldsymbol{C}\|^2$ | $|\boldsymbol{A}\cdot\boldsymbol{C}|/\|G_T\|^2 < 10^{-14}$; $|\|\boldsymbol{A}\|^2-\|\boldsymbol{C}\|^2|/\|G_T\|^2 < 10^{-13}$ at $k\ge 5\times 10^{-2}$ | Finding 17; `ca_maxwell.py` |
| 49 | V13c.1 — Yukawa uniform-Φ regression: `step_strong_2d(phi_field=v·I, yukawa={f: y})` ≡ `step_strong_2d(m_flavour={f: y·v})` bit-for-bit (δm=0 path in varm complex splitstep) | bit-for-bit identity | **0.0 exact** | V13c.1; `test_su3_noether.py::gate_V13c_yukawa_wiring` (2026-05-22) |
| 45 | QCA velocity-addition ratio $\rho(m) = m/(\sqrt{1-m^2}\arcsin m) = 1-2\beta_\text{LV}(m)$ — sympy series derivation, residual = 0 | closed-form identity | **0** (sympy bit-exact) | Finding 22; `casim.engine.interactions.derive_velocity_addition` |
| 46 | QCA deformed velocity-addition formula $u'_\text{QCA} = (u+v)/(1+2\rho^2 uv)$ and LV deviation $\delta u' = 2(1-\rho^2)uv(u+v)/[(1+2\rho^2 uv)(1+2uv)]$ — sympy residual = 0 | closed-form exact | **0** (sympy) | Finding 22; ibid. |
| 47 | Massless limit $m\to 0$ ($\rho\to 1$): $\delta u' = 0$ — SR velocity addition recovered exactly | $= 0$ | **0** (sympy) | Finding 22; ibid. |
| 48 | Leading LV coefficient $8\beta_\text{LV}(m) \approx -4m^2/3$ (small-$m$ expansion of velocity-addition deviation) | $8\beta_\text{LV} = -4m^2/3 + O(m^4)$ | sympy-confirmed; numerical match to 4 digits at $m=0.01$–$0.10$ | Finding 22; ibid. |
| 49 | ~~Composite-photon curl-residual coefficient is geometry-independent: $\dfrac{\text{curl residual}}{\|k\|} = \dfrac{c_\text{lat}}{\sqrt2}$~~ **WITHDRAWN 2026-08-04 (F306, ledger S18)** | not a physical coefficient | The number is right (6 figures across 5 geometries) but it is **quadrature**: the residual differences a *real* $E_G,B_G$ pair against an *imaginary* $i2\tilde n\times B_G$, and $B=\hat n\times E$ exactly, so the two sides are orthogonal and of equal length ($\lVert$LHS$\rVert/\lVert$RHS$\rVert=1.0000000000$). $c_\text{lat}/\sqrt2$ is $c_\text{lat}$ — by its own definition (F26) — times $1/\sqrt2$; look-elsewhere factor 1, evidential weight zero. **Replaced by:** the curl equation closes at $O(k^3)$, coefficient $c_\text{lat}^3/48$, record `F306-curl-closes-at-k3` | Finding 21 (REFUTED) → **F306**; `forks/curl_fork_harness.py` |
| 50 | C7 — SL(2,ℂ) → SO(1,3) homomorphism: Weyl 4-current covariance $j'^\mu = \Lambda^\mu{}_\nu j^\nu$ where $j^\mu = (\psi^\dagger\psi,\psi^\dagger\boldsymbol\sigma\psi)$ and $A = \cosh(\zeta/2)I_2 - \sinh(\zeta/2)(\boldsymbol\sigma\cdot\hat v)$ | algebraic identity (double-cover definition) | $3.71\times 10^{-16}$ max over 12 random $(\hat k,\hat v)$ pairs, $v/c=0.6$ | Finding 24; `ca_maxwell.py::weyl_sl2c_4current_covariance` (2026-05-23) |
| 51 | **RECLASSIFIED 2026-08-04 (F306, ledger S18): an IDENTITY, not a prediction** — it is the $2\times2$ real form of multiplying a complex number by $e^{-i\Omega}$; the residual is $5\times10^{-17}$ at $k=0.1$ *and the same at $k=2.0$*. Exact, and correctly so — but it does not compete with Maxwell, and the “5 orders of magnitude below the Maxwell curl residual” comparison below is between an identity and a quadrature artifact. C8 — Discrete real-rotation law: $E(t+1) = \cos\Omega\,E(t) + \sin\Omega\,B(t)$, $B(t+1) = -\sin\Omega\,E(t) + \cos\Omega\,B(t)$ with $\Omega = 2\omega(k/2)$ — derived from $G_T(t) = e^{-i\Omega t}(A+iC)$, holds for any $\Omega$ and any initial state; no small-$k$ approximation required | exact algebraic identity | $2.0\times 10^{-16}$ (E), $3.3\times 10^{-16}$ (B) max over 12 random BCC directions at $k=0.05$ — 5 orders of magnitude below the Maxwell curl residual | Finding 25; `ca_maxwell.py::real_rotation_vs_maxwell_curl` (2026-05-23) |

| 52 | C9 — BCC spin axis and (1,0) scalar contamination: $|\psi^T\psi|^2 = 1 - \hat{n}_y^2$ where $\hat{n}$ = `bcc_spin_axis(k/2)`. Locks down the contamination of $G^i=\psi^T\sigma^i\psi$ under Lorentz boosts — no free parameters remain | algebraic identity: $\|\cos^2(\Theta/2)+\sin^2(\Theta/2)e^{2i\Phi}\|^2 = 1-\sin^2\Theta\sin^2\Phi = 1-\hat{n}_y^2$ | Track A: $2.84\times 10^{-14}$ ($\|f\|^2+\hat{n}_y^2-1$); Track B: $6.20\times 10^{-14}$ (vs eig) — 12 random dirs, $k=0.3$ | Finding 26; `ca_bcc.py::bcc_spin_axis`, `ca_maxwell.py::weyl_spin_axis_scalar_contamination` (2026-05-23) |
| 53 | F27 — Chiral SU(2) Ward identity: $V\cdot\mathrm{mass\_step}(\psi;U) = \mathrm{mass\_step}(V\cdot\psi;\,V\cdot U)$ where $V(x)\in\mathrm{SU}(2)$ acts only on left-handed $\eta$; right-handed $\chi$ unchanged — local SU(2)_L gauge invariance of the complex-mass coupling (Ludwig 2007, pages 59–60) | algebraic identity (A=(0,U⊗I;U†⊗I,0) Hermitian, A²=I) | $1.055\times 10^{-17}$ — T5; `forks/complex_mass_fork.py::mass_step_doublet` + `su2_gauge_transform` (2026-05-23) |
| 54 | F27 — Chiral SU(2) chirality: right-handed $\chi$ exactly unchanged by SU(2)_L transform | $= 0$ | **$0.000\times10^{0}$ exact** — T6; ibid. |
| 55 | F27 — Dispersion invariance: $\omega(k)$ under complex-mass coupling is $\theta$-independent ($\theta$ is pure gauge) | dispersion = dispersion at $\theta=0$ | $3.331\times 10^{-16}$ max over $\theta\in\{0,\pi/3,\pi/2\}$ — T3; ibid. |
| 56 | F27 — U(1) gauge symmetry of mass step: $(\eta,\chi,\theta)\to(\eta,e^{i\varphi}\chi,\theta-\varphi)$ maps $(\eta_\text{new},\chi_\text{new})\to(\eta_\text{new},e^{i\varphi}\chi_\text{new})$ | algebraic identity | $1.388\times 10^{-17}$ — T4; ibid. |
| 57 | F27 — SU(2) doublet unitarity with spatially varying random U(x) field, 40 steps, L=24 | $\||\psi\|^2 = 1$ | $2.520\times 10^{-14}$ — T2; ibid. |
| 58 | F27 — Weak isospin T₃ = +½ for ν_L state: $\langle T_3 \rangle_\text{left} = +0.5$ exactly | $= +\tfrac12$ | $1.110\times 10^{-16}$ — T8; ibid. |

| 59 | F26 — c_lat from rotation rate (3D BCC): $c_\text{lat} = d\Omega/d|\mathbf{k}||_{k\to 0}$ measured by finite difference at $\varepsilon=10^{-5}$, $\Omega(\mathbf{k})=2\omega_\text{BCC}(\mathbf{k}/2)$ | $= 1/\sqrt{3} = 0.577350\ldots$ | $0.57735027$; residual $< 10^{-7}$ (finite-difference floor) | F26; `ca_maxwell.py::c_from_rotation_rate` (2026-05-23) |
| 60 | F26 — c_lat from rotation rate (2D square): same procedure with $\Omega(\mathbf{k})=2\omega_\text{2D}(\mathbf{k}/2)$ | $= 1/\sqrt{2} = 0.707107\ldots$ | $0.70710681$; residual $2.93\times 10^{-8}$ (finite-difference floor) | F26; `ca_maxwell_2d.py::c_from_rotation_rate_2d` (2026-05-23) |

| 61 | F29 — Hermitian singlet bilinear $G_H^i = \sum_\alpha (\phi^\alpha)^\dagger \sigma^i \psi^\alpha$ is SU(2)-invariant under $V \in \mathrm{SU}(2)$ on the doublet index | $G_H^i \to G_H^i$ (exact) | $2.24\times 10^{-16}$ across 12 random directions, $k=0.3$ | F29; `test_su2_photon_bridge.py::test_B1` (2026-05-23) |
| 62 | F29 — W-triplet bilinear $W^{a,i}$ rotates as adjoint $W^a \to R^{ab}(V) W^b$ with $R^{ab} = \tfrac12 \mathrm{tr}(\tau^a V \tau^b V^\dagger)$ | adjoint SO(3) rotation | $3.08\times 10^{-16}$ across 12 random directions | F29; `test_su2_photon_bridge.py::test_B2` (2026-05-23) |
| 63 | F29 — Triplet magnitude $\sum_a \|W^a\|^2$ SU(2)-invariant | invariant under $V$ | $6.66\times 10^{-16}$ | F29; `test_su2_photon_bridge.py::test_B3` (2026-05-23) |
| 64 | F29 — Per-component rotation-law energy conservation: each $(E^a, B^a)$ rotates at $\Omega(k) = 2\omega_\text{BCC}(k/2)$ with conserved magnitude | $\|E^a\|^2 + \|B^a\|^2 = \mathrm{const}$ per $a$ | $0.0$ (exact, geometric) | F29; `test_su2_photon_bridge.py::test_B5` (2026-05-23) |

| 66 | W1.5 — F27 mass-step Ward identity in W_μ context: $V_\eta \cdot \mathrm{mass}(\psi; U_m) = \mathrm{mass}(V\cdot\eta, \chi;\, V\cdot U_m)$ for chiral $V\in\mathrm{SU}(2)$ acting on $\eta$ only | algebraic identity (proof: $(V U_m)^\dagger (V\eta) = U_m^\dagger V^\dagger V \eta = U_m^\dagger \eta$) | $6.99\times 10^{-18}$ — W1.5; `test_wmu_phase1.py` (2026-05-24) |
| 67 | W1.4 — SU(2) Ward identity for exact covariant BCC step with constant gauge field: $V \cdot \mathrm{step}(\psi; U) = \mathrm{step}(V\psi;\, V\cdot U\cdot V^\dagger)$ where $V(x)=V_0\in\mathrm{SU}(2)$ (spatially constant) and the step uses `covariant_weyl_step_3d_bcc_exact` + `gauge_transform_links_kspace` with fractional $e^{ik\cdot d/\sqrt{3}}$ phases. Note: random-field residual is $\sim 3\times 10^{-2}$ (finite-lattice Nyquist aliasing, not a model error) | algebraic identity for constant $V$; $O(a)$ for full-bandwidth $V$ | $1.21\times 10^{-17}$ (constant $V$) — W1.4; `test_wmu_phase1.py` (2026-05-24) |

| 68 | F30 — Photon dispersion is anisotropic: $\Omega^+_{(1,0,0)} = k/\sqrt3$ exactly (no LIV on the cube axis at any order); leading correction is $-\sqrt3\,k^3/864$ along $(1,1,0)$ ($\delta v/c\sim k^2$, $n=2$) and $-\sqrt3\,k^2/54$ along $(1,1,1)$ ($\delta v/c=-k/18$, $n=1$) | exact sympy series; mpmath log-log slopes $3.0000$ / $2.0020$ confirm exponents | $0.0$ (exact rational coeffs) — F30; `test_F30_dispersion_order.py` (2026-05-24) |
| 69 | F30 — Chirality decomposition: unpolarised (chirality-even) photon dispersion is $n=2$ along every direction (linear chiral terms cancel between helicities); the $n=1$ term survives only as birefringence $\Omega^+-\Omega^- = -\sqrt3\,k^2/27$ along $(1,1,1)$ ($\Delta v_\phi/c = -k/9$, linear) | exact sympy series decomposition | $0.0$ (exact) — F30; `test_F30_dispersion_order.py` (2026-05-24) |

| 70 | W3.1 — Identity W links → plaquette field strength $F^a_{\mu\nu} = 0$ exactly: $U_\square = I \implies U_\square - U_\square^\dagger = 0$ bit-for-bit | $= 0$ | **0.0 exact** | W3.1; `test_wmu_phase3.py` (2026-05-24) |
| 71 | W3.3 — Wilson plaquette ‖F‖² gauge-invariant under constant SU(2) rotation $V$: $F^a \to R^{ab}(V)F^b$ (adjoint), $\|R F\|^2 = \|F\|^2$ since $R\in\mathrm{SO}(3)$ | $\|F\|^2$ invariant | $5.93\times 10^{-16}$ | W3.3; `test_wmu_phase3.py` (2026-05-24) |
| 72 | W4.1 — SU(2)_L Ward identity for full covariant Dirac doublet Strang step: $V\cdot\mathrm{step}(\psi;U) = \mathrm{step}(V\psi;VUV^\dagger)$ (constant $V$) | algebraic identity | $1.687\times 10^{-17}$ | W4.1; `test_wmu_phase4.py` (2026-05-24) |
| 73 | W4.3 — Right-handed $\chi$ exactly decoupled from $W_\mu$ at $m=0$: $\sin(0)=0$ kills the mass coupling; $\chi$ evolves under identity links → bitwise identical regardless of $U_\text{links}$ | $= 0$ | **0.0 exact** | W4.3; `test_wmu_phase4.py` (2026-05-24) |
| 74 | W5.3 — Stueckelberg $m_W = g\sqrt{\langle|\partial_\mu U_\text{st}|^2\rangle}$ invariant under constant left-multiplication $V$: $\partial_\mu(VU) = V\partial_\mu U$, $\mathrm{tr}[(V\partial U)^\dagger(V\partial U)] = \mathrm{tr}[(\partial U)^\dagger V^\dagger V \partial U] = \mathrm{tr}[(\partial U)^\dagger(\partial U)]$ | $m_W$ invariant | **0.0 exact** | W5.3; `test_wmu_phase5_stueckelberg.py` (2026-05-24) |
| 75 | W6.1 — Weinberg mix∘unmix = identity: $O(2)$ rotation composed with its inverse gives $I$ | $= I$ | $8.882\times 10^{-16}$ | W6.1; `test_wmu_phase6.py` (2026-05-24) |
| 76 | W6.3 — $m_Z/m_W = 1/\cos\theta_W$ algebraically: $m_W = gv/2$, $m_Z = v\sqrt{g^2+g'^2}/2$, $\cos\theta_W = g/\sqrt{g^2+g'^2}$ | algebraic identity | **0.0 exact** | W6.3; `test_wmu_phase6.py` (2026-05-24) |
| 77 | W6.4 — Gell-Mann–Nishijima $Q = T_3 + Y/2$ for all 7 electroweak particles ($\nu_L, e_L, u_L, d_L, e_R, W^+, \gamma$) | algebraic identity | $5.551\times 10^{-17}$ | W6.4; `test_wmu_phase6.py` (2026-05-24) |
| 78 | WB.1 — `fermion_isospin_current` pure-$\nu$ state ($f_e=0$): $J^1=J^2=0$ and $J^3 = |f_\nu|^2/2$ — zero imaginary parts and trivial algebra force exact zero | $= 0$ / exact | **0.0 exact** | WB.1; `test_wmu_phase7_backreaction.py` (2026-05-24) |
| 79 | WB.3a — Single sourced step from zero W fields: $E_W^3 \mathrel{+}= g J^3 dt$ with no free-rotation contribution (free rotation of zero is zero) | algebraic | **0.0 exact** | WB.3; `test_wmu_phase7_backreaction.py` (2026-05-24) |
| 80 | WB.3b — Multi-step diagonal isolation: $J^1=J^2=0$ source never populates $W^1$ or $W^2$ after 10 steps (no cross-isospin term in source kick) | $= 0$ | **0.0 exact** | WB.3; `test_wmu_phase7_backreaction.py` (2026-05-24) |
| 81 | WB.5 — Massless limit: `w_massive_propagation_step_spectral(m_W=0, dt=1)` is bitwise identical to `w_propagation_step_spectral` — $\sqrt{0+\Omega^2} = \Omega$ by construction | algebraic identity | **0.0 exact** | WB.5; `test_wmu_phase7_backreaction.py` (2026-05-24) |
| 82 | F37-A — $R(\Omega)(1,-i)^T = e^{-i\Omega}(1,-i)^T$: direct matrix multiplication; $(E_k+iB_k)$ is the $e^{-i\Omega}$ eigenstate of the BCC rotation law | algebraic identity | **exact** (symbolic) | F37; derived 2026-05-24 |
| 83 | F37-B — Hermitian symmetry $\Rightarrow \phi^+(-k) = \phi^-(k)$: the only HS-preserving bihelical dispersion law is $\mathbf{F}_+$ at $\Omega^+(k)$, $\mathbf{F}_-$ at $\Omega^-(k)$; BCC satisfies $\Omega^+(-k)=\Omega^-(k)$ by definition of the two branches | algebraic proof | **exact** | F37; derived 2026-05-24 |
| 84 | F37-C — RCP plane wave ($\mathbf{B}=-i\mathbf{E}$): $\mathbf{F}_- = \mathbf{E}-i(-i\mathbf{E}) = 0$ exactly; LCP ($\mathbf{B}=+i\mathbf{E}$): $\mathbf{F}_+ = 0$ exactly | algebraic identity | **0.0 exact** | F37; derived 2026-05-24 |
| 85 | F37-D — $\Omega_\text{even}$ is the unique single-rotation-matrix approximation that treats both helicities equally: $\Omega_\text{even} = (\Omega^++\Omega^-)/2$ is the only value making both eigenvalues $e^{\mp i\Omega_\text{even}}$ equal in magnitude | algebraic | **exact** (by definition) | F37; derived 2026-05-24 |
| 86 | FG-1.A — Mixed gravitational anomaly: $\sum_i n_i\,Y_i = 2(-1) + 1(2) + 6(\tfrac13) + 3(-\tfrac43) + 3(\tfrac23) = 0$ over the L-handed Weyl content of one generation | $= 0$ | **0 exact (over $\mathbb Q$)** | FG-1; `test_FG1_anomaly_cancellation.py` (2026-05-26 - 02:02) |
| 87 | FG-1.B — Pure $U(1)_Y^3$ anomaly: $\sum_i n_i\,Y_i^3 = -2 + 8 + \tfrac{6}{27} - \tfrac{192}{27} + \tfrac{24}{27} = 6 - 6 = 0$ | $= 0$ | **0 exact (over $\mathbb Q$)** | FG-1; `test_FG1_anomaly_cancellation.py` (2026-05-26 - 02:02) |
| 88 | FG-1.C — $[SU(2)_L]^2\!\cdot\!U(1)_Y$ anomaly: $\sum_\text{doublets} \dim_c \cdot T(R_2)\cdot Y = 1\cdot\tfrac12\cdot(-1) + 3\cdot\tfrac12\cdot\tfrac13 = -\tfrac12 + \tfrac12 = 0$ | $= 0$ | **0 exact (over $\mathbb Q$)** | FG-1; `test_FG1_anomaly_cancellation.py` (2026-05-26 - 02:02) |
| 89 | FG-1.D — $[SU(3)_c]^2\!\cdot\!U(1)_Y$ anomaly: $\sum_\text{triplets} \dim_2 \cdot T(R_3)\cdot Y = 2\cdot\tfrac12\cdot\tfrac13 + 1\cdot\tfrac12\cdot(-\tfrac43) + 1\cdot\tfrac12\cdot\tfrac23 = \tfrac13 - \tfrac23 + \tfrac13 = 0$ | $= 0$ | **0 exact (over $\mathbb Q$)** | FG-1; `test_FG1_anomaly_cancellation.py` (2026-05-26 - 02:02) |
| 90 | FG-1.E — $[SU(3)_c]^3$ anomaly: $\sum_\text{quark Weyls} \dim_2\cdot A(R_3) = 2(+1) + 1(-1) + 1(-1) = 0$ (vector-like colour content) | $= 0$ | **0 exact (over $\mathbb Z$)** | FG-1; `test_FG1_anomaly_cancellation.py` (2026-05-26 - 02:02) |
| 91 | FG-1.F — $[SU(2)_L]^3$ anomaly: identically zero (SU(2) reps are pseudo-real, $A(R)\equiv 0$) | $= 0$ | **0 exact (symbolic)** | FG-1; `test_FG1_anomaly_cancellation.py` (2026-05-26 - 02:02) |
| 92 | FG-6.2 — Two-helicity assembler is linear: $\texttt{EM\_bilinears\_two\_helicity}(\alpha,\beta) = \alpha(E_+,B_+) + \beta(E_-,B_-)$ for arbitrary complex weights | algebraic identity | **0.0 exact** | FG6.2; `test_FG6_two_helicity_photon.py` (2026-05-26 - 03:15) |
| 93 | FG-6.5 — Per-helicity dispersion under chiral propagation: $F^+(k) \to e^{-i\Omega^+(k)} F^+(k)$ and $F^-(k) \to e^{+i\Omega^-(k)} F^-(k)$ per tick, across single-branch + combined initial states (12 cases) | machine precision | $1.5\times10^{-15}$ over 10 ticks | FG6.5; `test_FG6_two_helicity_photon.py` (2026-05-26 - 03:15) |
| 94 | FG-6.6 — Birefringence coefficient on (1,1,1) body diagonal: $\Delta\Omega = \Omega^+ - \Omega^- = -(\sqrt3/27) k^2 + O(k^4)$ (F30 closed form) | $-\sqrt3/27 \approx -0.06415003$ | $4.5\times10^{-5}$ relative (65-point LSQ fit, $k\!<\!0.10$) | FG6.6; `test_FG6_two_helicity_photon.py` (2026-05-26 - 03:15) |
| 95 | FG-6.10 — Riemann-Silberstein decomposition identity: $E = (F^+ + F^-)/2$, $B = (F^+ - F^-)/(2i)$ for arbitrary complex 3-vectors | algebraic identity | **0.0 exact** | FG6.10; `test_FG6_two_helicity_photon.py` (2026-05-26 - 03:15) |
| 96 | F40-Q2 — F27 U(1) β-gauge Ward identity, per quark flavour: $(\eta_f, e^{i\varphi}\chi_f, \theta_f-\varphi) \to (\eta_f, e^{i\varphi}\chi_f)$ under `quark_mass_step_f27`, applied at each colour | algebraic identity | $1.2\times 10^{-16}$ | F40-Q2; `test_FG2_quark_complex_mass.py` (2026-05-26 - 16:30) |
| 97 | F40-Q7 — Cold-link + $\theta=0$ regression: `step_strong_2d_complex_mass` ≡ 9 independent `cdir.dirac_step_complex_mass_1flavor` calls, bit-for-bit | bit-for-bit identity | **0.0 exact** | F40-Q7; `test_FG2_quark_complex_mass.py` (2026-05-26 - 16:30) |
| 98 | F40-Q9 — F27 SU(2)$_L$ Ward identity on the **degenerate** quark $(u,d)$ doublet (mass step alone, per colour): $V\cdot\text{mass}(\psi;U) = \text{mass}(V\psi; V\!\cdot\!U)$ | algebraic identity | $8.4\times 10^{-17}$ | F40-Q9; `test_FG2_quark_complex_mass.py` (2026-05-26 - 16:30) |
| 99 | F40-QE1 — Cold $W$-link regression of `covariant_quark_doublet_step_2d`: $W=I$ reduces bit-for-bit to (per-(f,c) free Weyl half-steps) ∘ (F27 doublet mass) ∘ (per-(f,c) free Weyl half-steps) | bit-for-bit identity | **0.0 exact** | F40-QE1; `test_FG3_quark_electroweak.py` (2026-05-26 - 16:30) |
| 100 | F40-QE2 — SU(2)$_L$ Ward identity for the W-coupled quark doublet step under **constant** $V(x)$ (F34 W4.1 quark analog): $V\cdot\text{step}(\psi; W, U) = \text{step}(V\psi; V\!\cdot\!W\!\cdot\!V^\dagger, V\!\cdot\!U)$ | algebraic identity (linear V commutes with FFT and U_eff) | $2.8\times 10^{-16}$ | F40-QE2; `test_FG3_quark_electroweak.py` (2026-05-26 - 16:30) |
| 101 | F40-QE3 — Right-handed $\chi$ exactly decoupled from $W$ at $m=0$ in the quark sector (F34 W4.3 analog): changing $W$ leaves the $\chi$ output bit-for-bit unchanged | $\Delta\chi = 0$ | **0.0 exact** | F40-QE3; `test_FG3_quark_electroweak.py` (2026-05-26 - 16:30) |
| 102 | F41-Y3 — Higgs-free U(1)_Y extension reduces to F27 bit-for-bit at $\alpha\equiv 0$: `mass_step_doublet_su2xu1y(U, \alpha{=}0) \equiv \text{ca\_dirac.mass\_step\_doublet\_su2}(U)$ | bit-for-bit identity | **0.0 exact** | F41-Y3; `test_hypercharge.py` (2026-05-26 - 17:45) |
| 103 | F41-Y5 — With $U=I$, $U(1)_Y$ induces no isospin leakage: pure $\chi_\nu$ initial state produces no $\eta_e$ output (and symmetrically for $\chi_e$ → $\eta_\nu$) | $\eta_\text{off-diagonal} = 0$ | **0.0 exact** | F41-Y5; `test_hypercharge.py` (2026-05-26 - 17:45) |
| 104 | F41-Y7 — Higgs-equivalent hypercharge algebra: $\Delta Y_e = Y_L - Y_{e_R} = +1$, $\Delta Y_\nu = Y_L - Y_{\nu_R} = -1$, and Gell-Mann–Nishijima $Q = T_3 + Y/2$ on the four lepton states | algebraic identity over $\mathbb Q$ | **0 exact (symbolic)** | F41-Y7; `test_hypercharge.py` (2026-05-26 - 17:45) |
| 105 | F42-Y10 — Quark-sector $U(1)_Y$ extension reduces to F40/`ca_dirac.mass_step_doublet_su2` bit-for-bit at $\alpha\equiv 0$: `mass_step_quark_doublet_su2xu1y(U, \alpha{=}0) \equiv \text{mass\_step\_doublet\_su2}(U)$ | bit-for-bit identity | **0.0 exact** | F42-Y10; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 106 | F42-Y14 — Dynamical $\chi$ kinetic step ($e_R, u_R, d_R$) reduces to `ca_dirac._weyl_half_step_2c` bit-for-bit at $\alpha\equiv 0$, for **any** hypercharge $Y$ (regression guarantee for F27/F41 tests) | bit-for-bit identity | **0.0 exact** | F42-Y14; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 107 | F42-Y15 — Quark Gell-Mann–Nishijima algebra: $\Delta Y_u = Y_{Q_L} - Y_{u_R} = -1$, $\Delta Y_d = Y_{Q_L} - Y_{d_R} = +1$; $Q(u_L)=Q(u_R)=+2/3$, $Q(d_L)=Q(d_R)=-1/3$ via $Q = T_3 + Y/2$ | algebraic identity over $\mathbb Q$ | **$5.6\times 10^{-17}$** (rational-arithmetic FP residual) | F42-Y15; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 108 | F45.1 — σ↔τ swap dimensional decomposition of L-doublet: $\mathbb{C}^2_\sigma\otimes\mathbb{C}^2_\tau = \text{Sym}^2\oplus\Lambda^2$ (3+1), forcing $g'^2/g^2 = 1/3$ under equal per-direction bare coupling | $= 1/3$ | **0 exact (over $\mathbb Q$)** | F45.1; `test_f45_sigma_tau_weinberg.py` (2026-05-27 - 14:30) |
| 109 | F45.2/3 — Bare Weinberg angle: $\sin^2\theta_W = (1/3)/(1+1/3) = 1/4$, $\cos^2\theta_W = 3/4$, $\theta_W = \pi/6$ | $= 1/4$, $= 3/4$ | **0 exact (over $\mathbb Q$)** | F45.2–F45.3; `test_f45_sigma_tau_weinberg.py` (2026-05-27 - 14:30) |
| 110 | F45.4 — Bare mass ratio at $\theta_W = \pi/6$ (composing F45 prediction with F35 W6.3 identity): $m_Z/m_W = 1/\cos(\pi/6) = 2/\sqrt 3$ | $= 2/\sqrt 3 \approx 1.15470$ | $2.2\times 10^{-16}$ (1 ulp on $\cos$) | F45.4; `test_f45_sigma_tau_weinberg.py` (2026-05-27 - 14:30) |
| 111 | F45.5 — Casimir cross-check on L-doublet: $C_2(U(1)_Y)/C_2(SU(2)_L) = (Y_L/2)^2 / [T(T+1)] = (1/4)/(3/4) = 1/3$ — independent route to the same $g'^2/g^2$ ratio | $= 1/3$ | **0 exact (over $\mathbb Q$)** | F45.5; `test_f45_sigma_tau_weinberg.py` (2026-05-27 - 14:30) |
| 112 | F44-W6.6 — Rank-1 $(W^3, B)$ mass block from the F34b+F41 single-Stueckelberg-field construction: $M^2_{(W^3,B)} = f^2\binom{g}{-g'}\binom{g\ -g'}$ — outer product, $\det = 0$ algebraically | $\det = 0$ | $8.66\times 10^{-17}$ rel. to trace², 6 cases incl. SM physical | F44; `test_wmu_phase6_rank1.py` (2026-05-28 - 00:05) |
| 113 | F44-W6.7 — Spectral decomposition of the rank-1 block: eigenvalues $(0,\, f^2(g^2+g'^2))$; eigenvectors $(\sin\theta_W, \cos\theta_W)^\top$ (photon) and $(\cos\theta_W, -\sin\theta_W)^\top$ (Z) in $(W^3, B)$ basis with $\tan\theta_W = g'/g$ — exactly the F35 W6.1 rotation columns | identity | $2.19\times 10^{-16}$ (eig), $1.24\times 10^{-16}$ (vec) | F44; `test_wmu_phase6_rank1.py` (2026-05-28 - 00:05) |
| 114 | F44-W6.8 — Algebraic separation of the two parameterisations: the notebook's diagonal $\mathrm{diag}(m_W^2, m_{W_0}^2)$ rotated by $R(\theta_W)$ produces an $AZ$ cross term $(m_W^2 - m_{W_0}^2)\sin\theta_W\cos\theta_W$ (closed form); the F44 single-field block rotated by $R(\theta_W)$ has zero off-diagonal at machine $\varepsilon$ | identity; $\Delta_{AZ}^\text{single} = 0$ | $4.44\times 10^{-16}$ (two-field formula); $1.51\times 10^{-15}$ (single-field cross) | F44; `test_wmu_phase6_rank1.py` (2026-05-28 - 00:05) |
| 115 | F44-W6.9 lattice — Covariant Stueckelberg Hessian on a $4^3$ lattice with $a = 10^{-2}$: $W^1$/$W^2$ block is *bit-for-bit decoupled* from $(W^3, B)$, i.e. $H_{W^1 W^3} = H_{W^1 B} = H_{W^2 W^3} = H_{W^2 B} = 0$ exact, and $H_{W^1 W^1} = H_{W^2 W^2}$ exact — the lattice operator preserves horizontal SU(2)_L | $= 0$ | **$0.0$ exact** (both symmetry and off-diagonal); 6 cases incl. SM physical | F44; `test_wmu_phase6_rank1.py` (2026-05-28 - 00:20) |
| 116 | F43-PA.1 — SU(3) structure constants $f^{abc}$ satisfy the Jacobi identity $f^{abe}f^{ecd} + f^{bce}f^{ead} + f^{cae}f^{ebd} = 0$ across all $8^4$ index quadruples | algebraic identity | $1.1\times 10^{-16}$ | F43; `test_FG7_gluon_dynamics.py` PA.1 (2026-05-28 - 01:30) |
| 117 | F43-PA.4 — Colour-octet bilinear $G^{a,i}(x) = \sum_f q_f^\dagger \sigma^i T^a q_f$ transforms as the SU(3) adjoint of $V$ under $q\to Vq$ with constant $V$: $G^a_{Vq} = R_\text{adj}^{ab}(V)\,G^b_q$ (2D lattice) — F29 B2 SU(3) analog | algebraic identity | $6.7\times 10^{-16}$ | F43-PA.4; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 118 | F43-PA.5 — $\Sigma_a \\|G^a\\|^2$ SU(3) Casimir invariance under constant $V$ (2D bilinear) | identity | **0.0 exact** | F43-PA.5; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 119 | F43-PA.6 — Colour-octet bilinear $G^a$ adjoint identity on the **BCC** lattice (3D analog of PA.4) | algebraic identity | $7.8\times 10^{-16}$ | F43-PA.6; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 120 | F43-PB.1 — Identity SU(3) links on 2D-square $\Rightarrow$ Wilson plaquette $U_\square = I$ $\Rightarrow$ $G^a_{xy} = 0$ (Tr $T^a \cdot I = 0$ by tracelessness of Gell-Mann generators) — F33 W3.1 SU(3) analog | identity | **0.0 exact bit-for-bit** | F43-PB.1; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 121 | F43-PB.2 — Identity BCC composite SU(3) links $\Rightarrow$ $G^a_{\mu\nu} = 0$ for all three planes ($xy, xz, yz$) | identity | **0.0 exact bit-for-bit** | F43-PB.2; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 122 | F43-PB.4 — $\|G^a_{xy}\|^2$ SU(3)-invariant under constant $V$ (2D plaquette) — F33 W3.3 SU(3) analog. $R_\text{adj}(V) \in \mathrm{SO}(8)$ so the octet magnitude is preserved | identity | $5.4\times 10^{-15}$ (relative) | F43-PB.4; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 123 | F43-PC.1 — Cold-link Wilson loop $\langle\mathrm{Re}\,\mathrm{Tr}\,W(r,t)\rangle = N_c = 3$ exactly for every $r,t\in\{1,2,3\}$ — every product term is $I$ and $\mathrm{Tr}\,I = 3$ | $= 3$ | **0.0 exact bit-for-bit** (9 loop sizes) | F43-PC.1; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 124 | F43-PC.2 — Wilson loop $\langle\mathrm{Re}\,\mathrm{Tr}\,W(r,t)\rangle$ invariant under **local** SU(3) gauge transform $U\to V(x)U V^\dagger$ — $V(x)$ cancels at the loop start/end corner by construction | identity | $4.6\times 10^{-16}$ across 4 loop sizes | F43-PC.2; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 125 | F43-PD.1 — Octet charge density `quark_colour_current_2d` bit-for-bit equals `ca_strong.noether_charge_density` (regression / wrapper consistency) | bit-for-bit identity | **0.0 exact** | F43-PD.1; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 126 | F43-PD.2 — Linearised sourced step is **diagonal in colour**: a pure $J^a = J^{a_0}$ source drives only the $E^{a_0}$ component, leaving every other octet component at $0$ bit-for-bit (8 octet components tested) — F36 WB.3 SU(3) analog | $\Delta E^{a\neq a_0} = 0$ | **0.0 exact** | F43-PD.2; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 127 | F43-PD.3 — Massive gluon step at $m_g = 0$ reduces bit-for-bit to the free rotation step (BCC): $\omega_\text{eff}(k)\|_{m_g=0} = \Omega_\text{even}(k)$ — F36 WB.5 SU(3) analog | bit-for-bit identity | **0.0 exact** | F43-PD.3; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 128 | F43-PD.5 — 20-tick iterated sourced BCC step on free vacuum: $J^{a_0}$-only source drives only $E^{a_0}$; all other octet components remain $0$ bit-for-bit | $\Delta E^{a\neq a_0} = 0$ over 20 ticks | **0.0 exact** | F43-PD.5; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 129 | F46-P1 — Spherical Pythagorean identity $\cos\Omega_\text{Dirac}(\mathbf k, m) = \sqrt{1-m^2}\,\cos\Omega_\text{kin}(\mathbf k)$ on the 2D-square Weyl QCA, closed form, 200 random $(\mathbf k, m)$ | identity | $3.33\times 10^{-16}$ | F46-P1; `test_F46_pythagorean_mass.py` (2026-05-28 - 22:50) |
| 130 | F46-P2 — Same identity from explicit 4×4 $D_k$ eigenvalues (Paper 1 Eq. 23), 80 samples, 2D | eigenvalue identity | $3.33\times 10^{-16}$ | F46-P2; `test_F46_pythagorean_mass.py` (2026-05-28 - 22:50) |
| 131 | F46-P4 — BCC extension: $\cos\Omega_\text{BCC-Dirac}^\pm(\mathbf k, m) = \sqrt{1-m^2}\cdot u^\pm(\mathbf k)$, both helicity branches, 160 samples (3D) | identity | $3.33\times 10^{-16}$ | F46-P4; `test_F46_pythagorean_mass.py` (2026-05-28 - 22:50) |
| 132 | F46-P6 — Rest limit $\Omega_\text{Dirac}(\mathbf k = 0, m) = \arcsin m = \Omega_\text{rest}(m)$ across 8 masses ($m \in \{0,\ldots,0.99\}$) on both 2D and BCC | identity | $\le 2.22\times 10^{-16}$ | F46-P6; `test_F46_pythagorean_mass.py` (2026-05-28 - 22:50) |
| 133 | F44-W6.10(a) — Promoted `ca_wmu.covariant_stueckelberg_lagrangian_uniform` at $W = B = 0$ and $U_\text{st} = I$ returns $\mathcal L_\text{st} = 0$ exactly | $= 0$ | **$0.0$ exact** | F44-W6.10; `test_wmu_phase6_rank1.py` (2026-05-28 - 00:40) |
| 134 | F44-W6.10(b) — Same operator at $W = B = 0$ with arbitrary *constant* (non-identity) $U_\text{st}(x) \equiv V_0 \in \mathrm{SU}(2)$ also returns $\mathcal L_\text{st} = 0$ exactly — confirms the lattice covariant difference of a uniform field is identically zero (i.e., the operator is properly translation-covariant) | $= 0$ | **$0.0$ exact** | F44-W6.10; `test_wmu_phase6_rank1.py` (2026-05-28 - 00:40) |
| 135 | F44-W6.10(c) — Cayley-Klein implementation in `ca_wmu` matches an independent direct 2×2 matrix evaluation $f^2 V \cdot n_\text{dirs}\cdot \mathrm{tr}[(W V^\dagger - I)^\dagger (W V^\dagger - I)]$ at the same $(W, B, U_\text{st}=I)$ — two completely independent code paths to the same scalar | bit-for-bit identity | **$0.0$ exact (rel.)** | F44-W6.10; `test_wmu_phase6_rank1.py` (2026-05-28 - 00:40) |
| 142 | F54-CC1 — SU(2) charged-current algebra of $T^\pm = T^1\pm iT^2$: $[T^3,T^\pm]=\pm T^\pm$ and $[T^+,T^-]=2T^3=\tau^3$ | algebraic identity | **$0.0$ exact bit-for-bit** | F54-CC1; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 143 | F54-CC2 — $d\to u$ isospin raising $T^+\lvert d\rangle = \lvert u\rangle$; transition charge $\Delta Q = Q_u-Q_d = +1 = -Q(W^-)$ | identity over $\mathbb Q$ | **$0$ exact (Fraction)** | F54-CC2; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 144 | F54-CC3 — Charge conservation at *both* charged-current vertices: $d\to u+W^-$ ($\Delta Q=0$) and $W^-\to e^-\bar\nu_e$ ($\Delta Q=0$, $\Delta L=0$) | identity over $\mathbb Q$ | **$0$ exact (Fraction)** | F54-CC3; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 145 | F54-CC4 — Maximal parity violation: V−A vertex projector $P_L=(1-\gamma^5)/2$ annihilates a right-handed spinor ($P_L\psi_R=0$) and is the identity on a left-handed one ($P_L\psi_L=\psi_L$) | $=0$ | **$0.0$ exact bit-for-bit** | F54-CC4; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 146 | F54-CC5 — Quark–lepton universality: identical charged-current bilinear $J^+=f_\text{up}^*f_\text{down}$ and coupling for the $(u,d)$ and $(\nu,e)$ doublets; matches $J^1+iJ^2$ route | bit-for-bit identity | **$0.0$ exact** | F54-CC5; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 147 | F54-CC8 — Heavy-W Fermi limit: $A(q^2)=g^2/[8(m_W^2+q^2)]$ equals $G_F/\sqrt2=g^2/8m_W^2$ exactly at $q^2=0$; relative deviation $=-q^2/(m_W^2+q^2)$ | identity at $q^2{=}0$ | **$0.0$ exact**; rate residual $4.2\times10^{-17}$ | F54-CC8; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 148 | F54-CC9 — Full $\beta$-decay process $d\to u+e^-+\bar\nu_e$: $\Delta Q=\Delta B=\Delta L=\Delta(B-L)=0$ | identity over $\mathbb Q$ | **$0$ exact (Fraction)** | F54-CC9; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 150 | F64-D-EM-D1 — The dielectric curved-background Dirac stepper at $m=0$, flat $A=B=1$ ($K=1$), reduces bit-for-bit to two decoupled exact-QCA Weyl walks (the same D1 regression F62 passes, on the dielectric stepper) | bit-for-bit identity | $0.0$ | F64-D-EM-D1; `test_F64_em_connection.py` (2026-05-31 - 16:00) |
| 151 | F73-BP1 — Spin-0 bound-pair composite mass = sine-addition of constituent rest rotations: $\sin(\arcsin m_1+\arcsin m_2)=m_1\sqrt{1-m_2^2}+m_2\sqrt{1-m_1^2}$ (F46 $\Omega_\text{rest}=\arcsin m$ + F69 phase-sum) | closed-form identity | $1.3\times10^{-51}$ (mp, 121 pairs) | F73-BP1; `test_F73_spin0_bound_pair.py` (2026-06-01 - 17:42) |
| 152 | F73-BP2 — Equal-constituent closed form $m_H=\sin(2\arcsin m_c)=2m_c\sqrt{1-m_c^2}$ | closed-form identity | $4.0\times10^{-51}$ (mp, 99 pts) | F73-BP2; `test_F73_spin0_bound_pair.py` (2026-06-01 - 17:42) |
| 153 | F73-BP4 — Stability saturation: $\Omega_H=2\arcsin m_c=\pi/2$ at $m_c=1/\sqrt2\Rightarrow m_H=1$ (composite mass maximal) | exact bound | $2.7\times10^{-51}$ (mp) | F73-BP4; `test_F73_spin0_bound_pair.py` (2026-06-01 - 17:42) |
| 154 | F75-T1 — Maximal single-valued irrep dimension of the BCC point group $O_h$ is **3** (irrep dims $1,1,2,3,3$ per parity; $\sum d^2=48=\lvert O_h\rvert$; embedded character table cross-checked $\langle\chi_a,\chi_b\rangle=48\delta_{ab}$ over $\mathbb Z$) ⇒ no 4-dim degenerate (4th-generation) multiplet (Schur) | max dim $=3$, $\sum d^2=48$ | **exact (integer)** | F75-T1; `test_F75_three_generations_irrep.py` (2026-06-01 - 20:08) |
| 155 | F75-T2 — BCC nearest-neighbour (cube-vertex) shell decomposition $\Gamma_\text{shell}=A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}$ ($1{+}1{+}3{+}3=8$) by exact rational projection — the lattice realises a triplet channel | exact multiplicities | **exact (rational)** | F75-T2; `test_F75_three_generations_irrep.py` (2026-06-01 - 20:08) |
| 156 | F75-T3 — Parity selection of the scalar F27 mass ($A_{1g}$ s-wave $\eta$ → odd-parity $\chi$): the unique odd-parity *triplet* in the shell is $T_{1u}$ ⇒ generation count $=\dim T_{1u}=3$ ($T_{2g}$ even-parity excluded, $A_{2u}$ a singlet) | unique odd triplet, dim $3$ | **exact (integer)** | F75-T3; `test_F75_three_generations_irrep.py` (2026-06-01 - 20:08) |
| 157 | F75-T4b — A 4-fold-degenerate block on the shell fails to commute with $O_h$ (simplest 4-site projector: commutator norm $=1.0$) ⇒ a symmetry-stable 4th generation is impossible without breaking the lattice symmetry | commutator $>0$ (here $1.0$) | **exact (structural)** | F75-T4b; `test_F75_three_generations_irrep.py` (2026-06-01 - 20:08) |
| 158 | F76-C1 — Splitting of the $T_{1u}$ generation triplet vs vacuum symmetry: cubic $O_h\to[3]$, tetragonal $D_{4h}\to[2,1]$, orthorhombic $D_{2h}\to[1,1,1]$; three distinct masses require $T_{1u}\to B_{1u}\oplus B_{2u}\oplus B_{3u}$ (generations $=$ the three inequivalent axes) | distinct-eigenvalue counts $3/2/3$-levels | **exact (integer degeneracy)** | F76-C1; `test_F76_generation_hierarchy.py` (2026-06-01 - 20:41) |
| 159 | F76-C4 — Identity: Koide $Q=\sum m/(\sum\sqrt m)^2=\tfrac23$ $\Leftrightarrow$ equipartition of $\sqrt m$ between its $A_{1g}$ cubic scalar and traceless $T_{1u}$ triplet, $\cos^2\theta=1/(3Q)=\tfrac12$ ($\theta=45^\circ$, $\lvert A_{1g}\rvert^2=\lvert T_{1u}\rvert^2$) | closed-form identity | **exact (algebraic)** | F76-C4; `test_F76_generation_hierarchy.py` (2026-06-01 - 20:41) |
| 160 | F125-P5-A1 — Positronium two-body reduction: $\mathrm{Ry}(\mathrm{Ps})/\mathrm{Ry}(\mathrm H_\infty)=\tfrac12$ exactly (reduced mass $\mu=m_e/2$), same radial $1/r$ solver | ratio $=\tfrac12$ | $0.0$ (to $10^{-9}$) | F125-P5-A1; `test_P5_hydrogen.py` (2026-06-09 - 19:10) |
| 161 | F125-P5-I — Pure Dirac–Coulomb degeneracy $E(2s_{1/2})=E(2p_{1/2})$ (equal $\lvert\kappa\rvert=1$): the $2s$–$2p$ Lamb shift is a beyond-Dirac QED effect (open QFT-4) | exact degeneracy | $0.0$ ($<10^{-14}$) | F125-P5-I; `test_P5_hydrogen.py` (2026-06-09 - 19:10) |
| 160 | F77-B — NJL critical coupling for chiral-symmetry breaking (3-momentum cutoff, the dynamical-mass analogue of F74's binding threshold $g_c$): $G_c\Lambda^2=\pi^2/(N_cN_f)=\pi^2/6$, from $1=4G_cN_cN_f I_1(0)$ with $I_1(0)=\Lambda^2/4\pi^2$ | $G_c\Lambda^2=\pi^2/6$ | **$0.0$ exact** | F77-B; `test_F77_njl_gap_rpa.py` (2026-06-01 - 20:05) |
| 161 | F77-C3 — Polarization split identity: $\Pi_S(q^2)-\Pi_\text{PS}(q^2)=-8N_cN_fM^2K(q^2)$ for all $q^2$ (the $-(q^2-4M^2)$ vs $q^2$ coefficient in scalar/pseudoscalar bubbles) | closed-form identity | $1.8\times10^{-16}$ | F77-C3; `test_F77_njl_gap_rpa.py` (2026-06-01 - 20:05) |
| 162 | F78-B1 — The Koide ratio $Q=\sum y^2/(\sum y)^2$ ($y=\sqrt m$) is bounded $\tfrac13\le Q\le1$ (floor $=$ democratic/degenerate $y=(1,1,1)$, ceiling $=$ single-axis $y=(1,0,0)$), and the equipartition value is the exact range midpoint $Q=\tfrac23=\tfrac12(\tfrac13+1)$ | $Q\in[\tfrac13,1]$, midpoint $\tfrac23$ | **exact (algebraic)** | F78-B1; `test_F78_koide_amplitude_pairing.py` (2026-06-01 - 21:14) |
| 163 | F78-B4 — A real mass operator with cube $C_{3v}$ (body-diagonal) site symmetry is forced to eigenvalues $\{\mu+2\nu,\mu-\nu,\mu-\nu\}$ (a $[2,1]$ degeneracy); it attains $Q=\tfrac23$ only at $\nu/\mu=1/\sqrt2$ but with two $\sqrt$-masses equal ⇒ cannot give three distinct generations (these need the orthorhombic break, F76-C1) | $[2,1]$ spectrum; $Q=\tfrac23$ at $\nu/\mu=1/\sqrt2$ | **exact (algebraic)** | F78-B4; `test_F78_koide_amplitude_pairing.py` (2026-06-01 - 21:14) |
| 164 | F79-S3 — Source-free EM stress tensor traceless in 3+1D, $T^\mu{}_\mu=-T^{00}+\sum_iT^{ii}=0$ on random $(\mathbf E,\mathbf B)$ ⇒ the conformal factor $K$ (the gravity field) gets **zero tree stiffness** from the dominant sector, forcing the F59/F60 *loop* channel for $1/G$ (massive-scalar control $T^\mu{}_\mu=m^2\phi^2>0$ sources it, the F52 rest leg) | $\lvert T^\mu{}_\mu\rvert_\text{max}=0$ | $3.6\times10^{-15}$ (4000 samples) | F79-S3; `test_F79_structural_G.py` (2026-06-02 - 02:35) |
| 165 | F79-S6 — Parameter-free induced-$G$ coefficient and dimensionless cell prediction: $1/G=2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3)$ with $2\pi\eta g_*\sqrt d=8\pi\sqrt3$ ($\eta=\tfrac1{12}$, $g_*=48=16\times\dim T_{1u}$ structural), giving $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$ — closed form returns CODATA $G$ to $3\times10^{-8}$ (consistency check, not a fit) | $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$; coeff $8\pi\sqrt3$ | **exact-algebraic** (given the 3 structural inputs) | F79-S6; `test_F79_structural_G.py` (2026-06-02 - 02:35) |
| 166 | F80-D1 — Amplitude-rotation→Koide map $Q(\phi)=1/(3\cos^2\phi)$ for $\sqrt m=R[\cos\phi\,\hat n+\sin\phi\,\hat u]$ ($\hat n=(1,1,1)/\sqrt3$): $\phi=0°\to\tfrac13$ (democratic), $\phi=45°\to\tfrac23$ (equipartition), $\phi=\arccos\tfrac1{\sqrt3}=54.74°\to1$ (single-axis) | closed-form identity | **$0.0$ exact** (3 landmark angles) | F80-D1; `test_F80_em_saturation_45deg.py` (2026-06-02 - 11:57) |
| 167 | F80-D2 — SO(2) unification: F73 constituent $(n_c,m_c)=(\cos t,\sin t)$ at the stability cap $t=45°$ ($\Omega_\text{pair}=2t=\pi/2$, $m_c=1/\sqrt2$) and the generation $(\text{common},\text{diff})=(\cos\phi,\sin\phi)$ at Koide equipartition $\phi=45°$ are the identical $45°$-rotated unit vector $(1/\sqrt2,1/\sqrt2)$ — the constituent (F73) and generation (Koide) 45°'s are one SO(2) equal-split | same SO(2) equal-split | **$0.0$ exact** | F80-D2; `test_F80_em_saturation_45deg.py` (2026-06-02 - 11:57) |
| 168 | F81 — Saturated $N$-constituent Koide value $Q_N=1/(3\cos^2(\pi/2N))$ from F69 phase-sum + F73 $\pi/2$ saturation + F80 map: $N=1\to\infty$, $\mathbf{N=2\to2/3}$ (exact), $N=3\to4/9$, $N\to\infty\to1/3$ | closed-form $Q_N$; $N{=}2\Rightarrow\tfrac23$ | **$0.0$ exact** (N=2) | F81-E1; `test_F81_45deg_pair_saturation.py` (2026-06-02 - 12:15) |
| 169 | F81 — Phase-budget equipartition $N\phi_N=\pi/2$ (the stable phase budget split equally among $N$ pair constituents); the pair member's $\pi/4=45°=(1/\sqrt2,1/\sqrt2)$ coincides with the F73 rest-mass cap $\arcsin(1/\sqrt2)$ and the Cooper-pair spin-singlet weight | $N\phi_N=\pi/2$; member $=1/\sqrt2$ | **$0.0$ exact** ($\forall N$) | F81-E3/E4; `test_F81_45deg_pair_saturation.py` (2026-06-02 - 12:15) |
| 170 | F82 — Composite mass $m_H=\sin(2\phi)$ peaks at the saturation edge $\phi=45°$ ($m_H=1$), and the binding energy $E=E_0-\lambda\sin(2\phi)$ is minimised at $\phi=45°$ for **every** $\lambda>0$ ($dE/d\phi=-2\lambda\cos2\phi=0$, $d^2E/d\phi^2=4\lambda>0$) — the $45°$ location is coupling-strength-independent (dissolves F80-D5) | $\arg\min E=45°\ \forall\lambda$ | **exact** ($\lambda\in[10^{-6},10^6]$) | F82-G1/G2; `test_F82_saturation_mass_peak.py` (2026-06-02 - 19:38) |
| 171 | F82 — Flat-direction criterion: with stiffness $\kappa>0$, $E=\tfrac12\kappa\phi^2-\lambda\sin2\phi$ minimises *below* $45°$ ($\to45°$ only as $\kappa\to0$); the observed exact $45°$ ($Q=\tfrac23$) $\Leftrightarrow\kappa=0$ (a free generation-rotation modulus) | exact $45°\iff\kappa=0$ | **exact** (monotone $\phi^*(\kappa)$) | F82-G3; `test_F82_saturation_mass_peak.py` (2026-06-02 - 19:38) |
| 172 | F83 — Lattice-spacing/mass relation from the F46 rest-leg rotation + lightcone $a/\tau=c\sqrt d$: $a=\sqrt d\,\arcsin(m_\text{lat})\,\bar\lambda_C$ with $\bar\lambda_C=\hbar/(m_\text{phys}c)$ (one equation in two unknowns ⇒ a single mass fixes only the ray $a(m_\text{lat})$, with ceiling $a\le\sqrt d\,\tfrac\pi2\bar\lambda_C$, tightest = top quark, $3.11\times10^{-18}$ m) | closed-form identity | **exact** (algebraic) | F83-T2/T5; `test_F83_fix_lattice_spacing.py` (2026-06-02 - 20:05) |
| 173 | F83 — $\sqrt d$ reconciliation with si-units-options §3.3: the Option-C small-mass map $m_\text{lat}=m_\text{phys}ca/(\sqrt d\,\hbar)$ differs from §3.3's $m_\text{phys}ca/\hbar$ by exactly $\sqrt d$ (the lightcone factor) | ratio $=\sqrt d$ | $\lvert\text{ratio}-\sqrt3\rvert<10^{-6}$ | F83-T4; `test_F83_fix_lattice_spacing.py` (2026-06-02 - 20:05) |
| 174 | F84 — The generation Koide ratio interpolates $Q\in[\tfrac13,\tfrac23]$ with the residual democratic ($S_3$) stiffness $\kappa$ in $E=\tfrac12\kappa\phi^2-\lambda\sin2\phi$: $\kappa\to\infty$ (cubic, full $S_3$) $\to Q=\tfrac13$ (= F75 degenerate triplet); $\kappa=0$ (orthorhombic, no $S_3$) $\to Q=\tfrac23$ (= F76/F82 equipartition) | monotone $Q(\kappa)$; endpoints $\tfrac13,\tfrac23$ | **exact** (endpoints) | F84-H1/H2; `test_F84_flatness_from_orthorhombic_break.py` (2026-06-03 - 00:28) |
| 37 | F108-G3/G4 — momentum-resolved sea polarization $\Pi_\theta(q;m)$ (quasi-energy PT assembly) vs exact diagonalization of the mass-modulated F46/BCC walk; $\Pi_y(q\to0)=g''(y)$ | agreement | $1.8\times10^{-6}$ (exact diag); $\le1\%$ ($q\to0$, L16 vs L24) | declared $5\times10^{-3}$ / $2\%$ | F108; `test_F108_democratic_no_go_and_bubble.py` (2026-06-06 - 23:02) |
| 38 | F109-B3/B4 — repulsion rate of the empty fixed point $=4I_2$ (measured $0.8772$ vs $0.8765$ at $L=24$); flavor-resolved condensation reproduces the F92-P5 pin ($Q=0.666661$, $\delta=12.7328°$, equipartition $0.999991$, $c^2=2.000018$) | flow + decomposition | $0.08\%$; $\le2\times10^{-5}$ | declared $5\%$ / $10^{-3}$ | F109; `test_F109_f92_bridge_construction.py` (2026-06-06 - 23:27) |
| 175 | F84 — One orthorhombicity order parameter $s$ controls both phenomena at two thresholds: three *distinct* masses at any $s>0$ (F76-C1), equipartition ($Q\to\tfrac23$, $\kappa\to0$) only at a *complete* break ($s$ large); the same break that distinguishes the generations flattens $\phi$ | distinctness onset $s>0$; $Q\to\tfrac23$ as $s\to\infty$ | **exact** (monotone) | F84-H3; `test_F84_flatness_from_orthorhombic_break.py` (2026-06-03 - 00:28) |
| 176 | F102-P2 — U(1) minimal-coupling exact gauge covariance on the 3D BCC walk (Stueckelberg-form wrap, the F41/F42 architecture): $S[\alpha+\beta](e^{iq\beta}\psi)=e^{iq\beta}S[\alpha](\psi)$ for any $\beta(x)$ — a static gauge angle is unobservable (F27), and a time-dependent angle gives the electrostatic force as exact one-$k$-bin-per-tick Bloch acceleration (rolled spectrum $1.0\times10^{-15}$, sign included) | algebraic identity (phases × unitary spectral step) | $6.5\times10^{-17}$ | F102-P2-2/P2-4; `tests/test_particle_layer.py` (2026-06-05 - 19:25) |
| 177 | F102-P2 — SU(3) global Ward identity for the colour rotate-then-step (the audited SU(2) `covariant_weyl_step_3d_bcc` architecture with Gell-Mann generators): $V\cdot S_A(q)=S_{VAV^\dagger}(Vq)$ for constant $V\in\mathrm{SU}(3)$, potential in the adjoint (re-projected via $\mathrm{tr}(T^aT^b)=\tfrac12\delta_{ab}$); local Ward $O(a)$ as for all improved lattice fermions (matches F34/FG-3) | algebraic identity (constant $V$ commutes with the colour-blind step) | $3.1\times10^{-16}$ | F102-P2-6; `tests/test_particle_layer.py` (2026-06-05 - 19:25) |
| 178 | F104-P4-A — deuteron tensor coupling: the spin-angular matrix of $S_{12}=3(\boldsymbol\sigma_1\!\cdot\!\hat n)(\boldsymbol\sigma_2\!\cdot\!\hat n)-\boldsymbol\sigma_1\!\cdot\!\boldsymbol\sigma_2$ in the $\{{}^3S_1,{}^3D_1\}$ basis, built from explicit Clebsch-Gordan + spinor-spherical-harmonic quadrature, equals the Rarita-Schwinger matrix — the off-diagonal $2\sqrt2$ being exactly the L=0↔L=2 mixing that binds the deuteron | $[[0,2\sqrt2],[2\sqrt2,-2]]$ | $9.8\times10^{-15}$ | F104-P4-A; `test_P4_deuteron.py` (2026-06-06 - 06:58) |
| 179 | Sourced Maxwell-curl exact propagator: $\exp(dt\,G)=1+(\cos\theta-1)P_T+\sin\theta\,\hat G$ with $\theta=dt\lvert C(k)\rvert$, $G=[[0,iC\times],[-iC\times,0]]$, $G^2=-\lvert C\rvert^2 P_T$ — unitary per mode at any $dt$ (no CFL), longitudinal exactly invariant so Gauss $iC\cdot E$ changes only via $-dt\,J$; replaces the unconditionally unstable forward-Euler ($\lvert\lambda\rvert^2=1+dt^2\lvert C\rvert^2$, the charge_photon t3718 blow-up) | formula = matrix $\exp$ (closed form); free energy const | $3.3\times10^{-16}$ vs series expm; energy drift $1.6\times10^{-13}$/1000 ticks, Gauss $8.6\times10^{-14}$ at $dt=0.7$ | `ca_charge_coupling.maxwell_curl_step` (2026-06-06 - 16:56) |
| 180 | Grid-odd curl symbol: $C(k^*)=-C(k)$ under the FFT index involution $k^*=-k\bmod 2\pi$ after symmetrisation $C\leftarrow\tfrac12[C(k)-C(k^*)]$ — the analytic odd part of $n(k/2)$ ($4\pi$-periodic) is NOT grid-odd on the Nyquist planes (even residue $\approx3.15$ there, breaking Hermitian symmetry of the real-field stepper); identical off the Nyquist planes (residual 0.0 before and after) | $C(k)+C(k^*)=0$ identically | $0.0$ | `ca_charge_coupling.bcc_curl_symbol` (2026-06-06 - 16:56) |
| 181 | F106-E1 — the ψ→K sourcing coefficient is pure lattice: $8\pi G/c^4 = a^2 c_\text{lat}/(\hbar c)$ identically, on substituting F79's structural $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ and $c_\text{lat}=1/\sqrt3$ (F26). So the fermion sources its own dielectric by $\nabla^2\ln K=-(a^2 c_\text{lat}/\hbar c)\,T^{00}[\psi]$ with **no free coupling**; the old $\nabla^2\Phi=4\pi G\lvert\Psi\rvert^2$ loop is its nonrel limit ($T^{00}=mc^2\lvert\Psi\rvert^2\Rightarrow G_\text{eff}=2Gm$, E4 exact) | $8\pi G/c^4-a^2 c_\text{lat}/(\hbar c)=0$ | **$0$ exact (sympy)** | F106-E1/E4; `test_F106_psi_K_sourcing.py` (2026-06-06 - 17:55) |
| 182 | F64-mainline — the gravity field element in the production engine: (a) the F106 law holds as a **discrete identity** through the production maps, `lap_nd(ln K) == −T⁰⁰` (zero-mean) when `solve_phi_poisson` inverts the exact stencil symbol $-4\sum_i\sin^2(k_i/2)$ — the static fixed point of the D-EM8 leapfrog is exact; (b) in lattice units the structural Newton constant is $G_\text{lattice}=c_\text{lat}^4/8\pi=1/(72\pi)$ (F79 closed form, same algebra as #181); (c) flat field ($K\equiv1$) ⇒ the gravity-coupled massive Dirac step is **bit-identical** to the free step and the F62 lapse mix is exactly unitary | discrete identity; bit-for-bit flat reduction | resid $<10^{-10}$ (exp/log floor); $0.0$ bit-identical; unitarity $10^{-14}$ | `tests/test_gravity_element.py` G1/G3/G6 (2026-06-06 - 18:45) |
| 183 | F107-L4a — canonical-dielectric absolute lensing: for $K=e^{2u}$ the log-index $\ln K=2GM/(rc^2)$ is exactly Coulombic, so the straight-ray eikonal deflection is $K_\text{bend}=\alpha b c^2/GM=-4$ **at every field strength** (no finite-$u$ correction at straight-ray order — corrections enter only via ray bending); mpmath quadrature returns $-4.0$ for $u=10^{-2}..10^{-5}$; lattice (L=96 FFT-Poisson) absolute coefficient $3.92$ with dielectric/rest ratio $2$ to $7.7\times10^{-14}$; downstream closed forms $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ and $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$ evaluate at the adopted $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ | $K_\text{bend}+4=0$ (sympy); ratio$-2=7.7\times10^{-14}$ | `tests/findings/test_F107_canonical_a_L4_grb_gate.py` L4a–L4d (2026-06-06 - 22:39) |
| 184 | F113-A — SU($N$) Fierz swap operators for the chromomagnetic interaction: $\boldsymbol\sigma_i\!\cdot\!\boldsymbol\sigma_j=2P^s_{ij}-1$ gives $+1$ (spin triplet) / $-3$ (singlet); $\boldsymbol\lambda_i\!\cdot\!\boldsymbol\lambda_j=2P^c_{ij}-2/3$ gives $-8/3$ for a colour-antisymmetric ($\bar3$) pair — the exact algebra (pure rationals, no numpy/chiral) underlying the NN core | triplet $+1$, singlet $-3$; $\bar3$-pair $-8/3$ | **$0$ exact (ℚ)** | F113-A; `test_F113_repulsive_core.py` (2026-06-08 - 14:10) |
| 185 | F113-B — single-baryon chromomagnetic energies from the F71 colour-singlet × SU(6) wavefunctions: $\langle H_\text{CM}\rangle_N=-8\,g_\text{cm}$ (binding), $\langle H_\text{CM}\rangle_\Delta=+8\,g_\text{cm}$ ⇒ $M_\Delta-M_N=16\,g_\text{cm}$; the measured 293 MeV splitting fixes the one external number $g_\text{cm}=18.31$ MeV (the existing colour-magnetic coupling, not new) | $E_N=-8$, $E_\Delta=+8$ g$_\text{cm}$ | **$0$ exact (ℚ)** | F113-B; `test_F113_repulsive_core.py` (2026-06-08 - 14:10) |
| 186 | F113-C — six-quark Pauli norm kernel for the deuteron channel ($S{=}1,T{=}0$): exact RGM coefficients $K_0=K_3=839808$, $K_1=K_2=93312$, full-overlap value $n(R{=}0)=20/9>0$ — the channel is allowed (not kinematically Pauli-forbidden), consistent with the deuteron binding | $n(R{=}0)=20/9$ | **$0$ exact (ℚ)** | F113-C; `test_F113_repulsive_core.py` (2026-06-08 - 14:10) |
| 187 | F113-D — the short-range repulsive core: the Pauli-required spatially-symmetric [6] six-quark state at full overlap has $\langle H_\text{CM}\rangle=+8/3\,g_\text{cm}$ vs $-16$ for two free nucleons ⇒ $\Delta E_\text{CM}=+56/3\,g_\text{cm}=+341.8$ MeV (positive ⇒ repulsive); replaces the tuned hard core of F104. Profile $V_\text{core}(R)$ positive/monotone/vanishing is Tier-B ($b$-dependent) | $\Delta E_\text{CM}=+56/3\,g_\text{cm}>0$ | **$0$ exact (ℚ)**; height $+341.8$ MeV given $g_\text{cm}$ | F113-D; `test_F113_repulsive_core.py` (2026-06-08 - 14:10) |
| 136 | F53-P1 — Charge-conjugation antiparticle table: $C:(T_3,Q,Y)\to(-T_3,-Q,-Y)$ with Gell-Mann–Nishijima $Q=T_3+Y/2$ holding for **both** particle and antiparticle across all 8 first-gen Weyl species (exact rationals) | GMN residual $=0$ | **$0.0$ exact** | F53-P1; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 137 | F53-P2 — $C$ maximally violated by the charged current: the $C$-image (right sector) of each left doublet sources zero SU(2)$_L$ isospin current, so $A_C=1$ | $A_C=1$, $\|J\|_{\rm right}=0$ | **$0.0$ / $A_C=1$ exact** | F53-P2; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 138 | F53-P3 — $P$ maximally violated: doublet $g_L=1$, singlet $g_R=0$ ⇒ $A_P=(g_L-g_R)/(g_L+g_R)=1$ for $\nu_L,e_L,u_L,d_L$ | $A_P=1$ | **exact (rational)** | F53-P3; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 139 | F53-P4b — Neutral-current $CP$ relation $g_R^{\bar f}=-g_L^f$ ⇒ CP-paired vertices have equal magnitude $\lvert g_L^f\rvert=\lvert g_R^{\bar f}\rvert$ for all 7 chiralities (F48/F35 table at $\sin^2\theta_W=1/4$) | $\lvert\Delta\rvert=0$ | **$0.0$ exact** | F53-P4b; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 140 | F53-P4c — Single-generation Jarlskog: physical CP-violating phases $N(n)=(n-1)(n-2)/2$ give $N(1)=0$ (and $N(3)=1$) — no CP phase exists in one generation | $N(1)=0$ | **exact (integer)** | F53-P4c; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 141 | F53-P6 — CPT per species (algebraic): rest frequency $\omega_0(+m)=\omega_0(-m)=\arccos(\cos m)$ for $m\in\{m_e,m_u,m_d\}$ | $\lvert\Delta\omega_0\rvert=0$ | **$0.0$ exact** | F53-P6; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |

**F50 — gravity fork via the F46 spherical triangle (tetrad Dirac), 2026-05-28 - 23:55.** (Global Tier-1 indices pending reconciliation: this table stops at the F47 block, while F48/F49 logged entries only in their findings. F50 items are labelled locally until that catch-up lands.)

| F50-id | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| F50-G2 | Static redshift sits on the **rest** leg: $\Omega_\text{Dirac}^\text{coord}(\mathbf k=0)=\sqrt{A}\,\arcsin m$ exactly; near/far clock ratio$_\text{GR}\to1$ (baseline 2) | identity | $1.67\times 10^{-16}$ | F50-G2; `test_F50_gravity_fork_dirac.py` |
| F50-G3 | Photon limit $m=0$: $c_\text{eff}=c_0\sqrt{A/B}$ equals Fork-E $c_\gamma$ bit-for-bit, and $\Omega=\omega_\text{kin}$ | bit-for-bit / identity | $0.0$ / $1.67\times10^{-16}$ | F50-G3 |
| F50-G4 | Negative control: kinetic-leg-only $\Omega(\mathbf k=0)$ is position-independent $=\arcsin m$ (disproves F46 §9.3 literal wording) | spread $=0$ | $0.0$ | F50-G4 |
| F50-G6 | Bounded exact-QCA leg $r_\text{kin}\arccos(c_x c_y)$ reduces to flat F46 $\cos\Omega=\sqrt{1-m^2}c_x c_y$ at $A=B$, 200 random $(\mathbf k,m)$ | bit-for-bit identity | $4.44\times 10^{-16}$ | F50-G6 |
| F50-G8 | Homogeneous exact-QCA stepper per-tick phase $=r_\text{kin}\arccos(c_x c_y)$ (Paper-1 Eq.16 walk, rate $r_\text{kin}=\sqrt{A/B}$), 20 ticks | bit-for-bit | $0.0$ | F50-G8 |

(Tier-2 companions: F50-G5 prototype Strang stepper norm drift $=0.0$ over 12 steps via the Cayley kinetic leg; F50-G1 spherical→Euclidean reduction log-log slope $4.0008$, the F46-characteristic 4th-order lattice correction with both legs gravitationally renormalised; F50-G7 bounded exact-QCA leg stays in $[0,\pi]$ over 400 random $\mathbf k$ with small-$k$ slope $=r_\text{kin}/\sqrt2$ to $2\times10^{-9}$.)

**F51 — bipartite sublattice carries hypercharge (rep theory on the BCC walk), 2026-05-29 - 04:14.** (Local labels; same numbering-reconciliation caveat as F48–F50.)

| F51-id | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| F51-S4 | $P=e^{i\mathbf Q\cdot\mathbf x}\otimes I_2$ is a spin scalar: $[P,\sigma_a]=0$ for $a=x,y,z$ (Schur ⟹ $U(1)_P$ commutes with cell $SU(2)$) | identity | **$0.0$ exact** | F51-S4; `test_sublattice_hypercharge.py` |
| F51-S5 | Gell-Mann–Nishijima $Q=T_3+Y/2$ over $\mathbb{Q}$ with the sublattice charge supplying the $Y$ slot (F38 table) | exact rational | **$0$ (integer)** | F51-S5; `test_sublattice_hypercharge.py` |

(Tier-2 companions: F51-S1 $A^{s}(\mathbf k+\mathbf Q)=-A^{s}(\mathbf k)$, i.e. $\{P,W\}=0$ / bipartite, residual $1.05\times10^{-15}$; F51-S2 $A^{s}(\mathbf k+\mathbf Q)^2=A^{s}(\mathbf k)^2$, i.e. $[W^2,P]=0$ / sublattice $U(1)$ conserved on the stroboscopic walk, residual $1.80\times10^{-15}$; F51-S3 S1 holds per-branch ⟹ $U(1)_P\perp$ chirality, residual $\le8.5\times10^{-16}$. S1–S3 are algebraic identities holding for all $\mathbf k$; the floor is complex128 round-off.)

**F70 — gradient-flow/cooling driver + exact 2D confinement, 2026-06-01 - 16:35.** (Local labels; same numbering-reconciliation caveat as F48–F51.)

| F70-id | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| F70-GF1 | Cold SU(3) config is a Wilson-flow/cooling fixed point: force $Z=0$, $\exp(\epsilon Z)U=U$, $\text{cool}(U)=U$ | $=0$ bit-for-bit | **$0.0$ exact** | `test_FG7b_gradient_flow.py` |
| F70-GF4 | Flow force $Z=-[U\Sigma^\dagger]_\text{TA}\in\mathfrak{su}(3)$ (anti-Hermitian + traceless) | identity | $5.6\times10^{-16}$ | `test_FG7b_gradient_flow.py` |
| F70-GF5 | Wilson flow is gauge-covariant: $\text{flow}(U^g)=\text{flow}(U)^g$ for local $V(x)$ | identity | $7.8\times10^{-15}$ | `test_FG7b_gradient_flow.py` |
| F70-CF3 | String tension $\sigma(\beta)=-\ln w(\beta)>0$ for every finite $\beta$ ($w$ from SU(3) Weyl-torus quadrature) | $>0\ \forall\beta$ | $\sigma_{\min}=0.219$ | `test_FG7c_confinement.py` |
| F70-CF4 | Creutz ratio $\chi(R,T)=-\ln\frac{W_{RT}W_{R-1,T-1}}{W_{R-1,T}W_{R,T-1}}=\sigma$, **independent of $(R,T)$** | identity $=\sigma$ | $2.2\times10^{-16}$ | `test_FG7c_confinement.py` |
| F70-CF5 | Static potential $V(R)=\sigma R$ exactly linear, $T$-independent loop estimator | identity | $8.9\times10^{-16}$ | `test_FG7c_confinement.py` |
| F70-CF8 | Schur coefficient: $\langle\tfrac1N\mathrm{Tr}\,U\rangle$ real $=w(\beta)$ (Im $=0$ by $\phi\!\leftrightarrow\!-\phi$) ⇒ $\langle U\rangle=wI$ ⇒ $\langle W\rangle=w^{RT}$ | $\mathrm{Im}=0$, $\mathrm{Re}=w$ | $1.3\times10^{-18}$ | `test_FG7c_confinement.py` |

(Tier-2 companions: F70-GF2 flow+cooling preserve SU(3) unitarity+det over 15 steps, $2.5\times10^{-14}$; F70-GF6 flow acts as the lattice Laplacian, per-mode decay $\delta/\hat k^2$ constant across wavevectors, $4.9\times10^{-10}$; F70-CF1 $w(0)=0$ to $1.5\times10^{-17}$; F70-CF2 $w(\beta)$ quadrature grid-converged $2.8\times10^{-17}$. Tier-3: F70-CF6 Metropolis lattice plaquette ↔ $w(\beta)$, rel $4.8\times10^{-3}$; F70-CF7 gradient flow raises $\langle\text{plaq}\rangle 0.07\!\to\!0.96$, lowers $\sigma_\text{eff} 2.66\!\to\!0.04$.)

**F86 — confinement as colour-dielectric / dual superconductor (P1 Option C), 2026-06-03 - 23:58.** (Local labels; same numbering caveat.)

| F86-id | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| F86-CD1 | Bogomolny completion $\tfrac12B^2+|D\phi|^2+\tfrac{\lambda}{2}(|\phi|^2{-}v^2)^2 = \tfrac12(B{+}e(|\phi|^2{-}v^2))^2+|(D_1{+}iD_2)\phi|^2+ev^2B$ at $\lambda=e^2$ ⇒ $\sigma=2\pi v^2n$ | identity (sympy) | **$0.0$ exact (algebraic)** | `test_FG7d_colour_dielectric.py` |
| F86-CD4 | Dielectric gluon step $\to$ free F43 propagator `gluon_rotation_step_spectral_2d` at $\varepsilon_c{=}1$; renorm $\Omega\to\Omega/\sqrt{\varepsilon_c}$, $c_\text{eff}=c_\text{lat}\sqrt{\varepsilon_c}$ | $=$ free step bit-for-bit | **$0.0$ exact (bit-for-bit)** | `test_FG7d_colour_dielectric.py` |
| F86-CD6 | Constant tube cross-section ($z$-independent DGL profile) ⇒ $V(R)=\sigma R$ exactly linear, slope $=\sigma$; $R\to\infty$ ⇒ $\infty$ | linear | $1.0\times10^{-14}$ | `test_FG7d_colour_dielectric.py` |

(Tier-3 / numeric-ODE companions: F86-CD3 numeric $\int$(energy density) on the BPS profile $=2\pi v^2n$ ($n{=}1,2$), rel $4.6\times10^{-6}$ — ODE-exact; F86-CD2 ANO profile BCs $f,a{:}0{\to}1$ monotone + quantised flux $\Phi=2\pi n/e$, rel $1.5\times10^{-4}$; F86-CD5 dual-Meissner London penetration depth $\lambda=1/(ev)$ from $\ln(|E|\sqrt r)$ slope, rel $1.3\times10^{-2}$.)

**F94 — 3+1D SU(3) lattice-gauge MC (P1 Option A) vs Option C, 2026-06-04 - 14:33.** (Local labels; same numbering caveat. Numbered F94 not F87 — F87–F93 were taken by concurrent work.)

| F94-id | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| F94-FA2 | SU(2)-subgroup over-relaxation $R=(V_2^\dagger)^2$ preserves the Wilson action (microcanonical) | $\Delta S=0$ | $1.2\times10^{-16}$ | `test_FA_lgt_mc.py` |
| F94-FA3 | Staple/action-gradient identity $\sum_\text{links}\mathrm{Re\,Tr}(U_\mu R_\mu)=4\cdot$(plaquette-sum $\mathrm{Re\,Tr}$) | ratio $=4$ | $8.9\times10^{-16}$ | `test_FA_lgt_mc.py` |
| F94-CMP2 | Gauge-MC $\sigma_A$ fixes the dual-SC condensate $v^*{=}\sqrt{\sigma_A/2\pi}$; Option C $\sigma_C(v^*){=}\sigma_A$ | identity | $1.2\times10^{-16}$ | `test_FA_vs_FC_comparison.py` |
| F94-CMP3 | $V_A{-}V_C={-}e/R$ exactly (Coulomb term C omits); $e$ recovered from $\mathrm{std}(eR)/\mathrm{mean}$ | $-e/R$ | $\le10^{-12}$ | `test_FA_vs_FC_comparison.py` |

(Tier-2: F94-FA1 heat-bath+OR preserve SU(3) unitarity+det, $1.1\times10^{-15}$. Tier-3 statistical: F94-FA4 mean plaquette matches published SU(3) ⟨P⟩(β=5.7,6.0), rel $1.7\times10^{-2}$; F94-FA5 strong-coupling ⟨plaq⟩→β/18, rel $1.4\times10^{-1}$; F94-FA6 Lüscher–Weisz two-level estimator agrees with direct Polyakov correlator and reduces its variance **~84×**; F94-CMP1 both options confine ($V_A$ rises, $\sigma>0$); F94-CMP4 $\sigma_A>0$ and F70 2D $\sigma(\beta)>0$ & decreasing. Production $\sigma\pm$err is the user-run `run_lgt_confinement.py`.)

**F88 — the colour-magnetic condensate arising within the model, 2026-06-04 - 01:18.** (Local labels; same numbering caveat.)

| F88-id | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| F88-CC1 | Nielsen–Olesen growing mode: $W_\mu = e^{\gamma t}e^{-gB(x^2+y^2)/4}\varepsilon_\mu$ solves the linearised YM EOM (with $\epsilon^{abc}$ self-coupling) iff $\gamma^2 = +gB$; charged-scalar control $\omega^2=+gB$ stable | exact closure / non-vacuous | **$0$ (sympy)** | `derive_colour_condensate.py` D1/D1b |
| F88-CC2 | Savvidy potential: $\zeta_H(-1,\tfrac32)+\zeta_H(-1,-\tfrac12)$ sum $=-\tfrac{11}{12}$ each ⇒ $\mathrm{Re}\,\Delta V$ log coefficient $\tfrac{11}{96\pi^2}g^2B^2$; $B_\text{min}=(\mu^2/g)e^{-1/2cg^2}$, $V_\text{min}=-cg^2B_\text{min}^2/2<0$; $\mathrm{Im}\,V=g^2B^2/16\pi$ | closed forms | **$0$ (sympy)** | `derive_colour_condensate.py` D2 |
| F88-CC5 | DeGrand–Toussaint monopole charge on compact links: integer, gauge-invariant, $\Sigma_c m_c=0$ (torus), constructed Dirac pair exactly $\pm1$ in the endpoint cubes | integers / zeros | **$0.0$ bit-for-bit** | `test_FG7e_colour_condensate.py` CC5 |
| F88-CC7 | Cartan projection of Haar-SU(3) links: integer monopole charges, density $\rho\approx0.49/0.46>0$ | integer + structural | **$0.0$** (quantisation) | `test_FG7e_colour_condensate.py` CC7 |
| F88-D3 | Dual sine-Gordon: $m_D^2=2z/\kappa$; BPS dual-string tension $\sigma_\text{dual}=8\sqrt{2\kappa z}$; kink $\chi=4\arctan e^{m\xi}$ solves Bogomolny | closed forms | **$0$ (sympy)** | `derive_colour_condensate.py` D3 |

(Tier-2 companion: F88-CC6 Villain/Poisson + Coulomb-gas Gaussian duality identities, $\le3.3\times10^{-16}$. Tier-3 companions: F88-CC3 lattice tachyon $\min\Omega^2/\phi\to-1$, $7.5\times10^{-4}$ at $L{=}32$; F88-CC4 lattice Savvidy $\Delta E(B)<0$ monotone; F88-CC8 MC $\rho(\beta)$ dilute tail corr $-0.98$, hand-off $v=m_D/e=0.713$, $\sigma_\text{F86}=2\pi v^2=3.20$.)

**F71 — colour-singlet three-quark (proton) construction, 2026-06-01 - 16:42.** (Local labels; same caveat.)

| F71-id | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| F71-BS1 | Colour tensor $\varepsilon_{abc}$ totally antisymmetric (swap any pair → sign flip) | identity | **$0.0$ exact** | `test_FG7d_baryon_singlet.py` |
| F71-BS3 | Colour-singlet gauge invariance $B=\varepsilon_{abc}q_1^aq_2^bq_3^c\to\det(V)B=B$ under local $V(x)\in$ SU(3) | identity | $1.2\times10^{-15}$ | `test_FG7d_baryon_singlet.py` |
| F71-BS4 | Zero total colour charge: $G^a\lvert S\rangle=0\ \forall a$ and Casimir $C_2\lvert S\rangle=0$ ($\varepsilon$ = unique singlet of $3\otimes3\otimes3$) | $=0$ | $1.4\times10^{-16}$ | `test_FG7d_baryon_singlet.py` |
| F71-BS5 | Proton $uud$: $Q=\tfrac23+\tfrac23-\tfrac13=1$, $B=1$, $T_3=\tfrac12$, GMN-consistent (over $\mathbb Q$) | exact rational | **$0$ (Fraction)** | `test_FG7d_baryon_singlet.py` |
| F71-BS6 | Proton spin-up SU(6) spin-flavour wavefunction (9 terms, $3\times{+}2$/$6\times{-}1$, $\lVert\cdot\rVert^2=18$) fully $S_3$-symmetric | $=0$ | **$0.0$ exact** | `test_FG7d_baryon_singlet.py` |
| F71-BS7 | Full wavefunction antisymmetric under quark exchange: colour$(-1)\times$ spin-flavour$(+1)\times$ space$(+1)=-1$ (Fermi) | sign $=-1$ | **$0.0$ exact** | `test_FG7d_baryon_singlet.py` |
| F71-BS8 | Energetic binding $V(R)=\sigma R\to\infty$ from the F70 string tension (linear, $V/R=\sigma$) | identity | **$0.0$ exact** | `test_FG7d_baryon_singlet.py` |

(Tier-2 companion: F71-BS2 $\det V=1$ for SU(3) gauge matrices — the source of singlet invariance — $3.2\times10^{-15}$.)

| F108-G2 | Matrix-element trace identity $\lvert\langle s',\hat n'\rvert\sigma_1\lvert s,\hat n\rangle\rvert^2=(1+ss'\,\hat n'\!\cdot\tilde n)/2$, $\tilde n=(n_1,-n_2,-n_3)$ | identity | $<10^{-12}$ over 800 random pairs | F108; `test_F108_democratic_no_go_and_bubble.py` |
| F108-T1 | Refit invariance: adding any $w(\bar y)$ leaves $\kappa_E$ and the wall-KKT margin invariant; $\mu\to\mu-w'(\bar y_*)/(3\bar y_*)$ | identity | $\le10^{-9}$ (two unrelated $w$) | F108; same script |
| F108-T2 | Shadow cancellation: $E(\text{lepton})-E(\text{shadow})=\tfrac{\kappa_E}{2}e_*^2+WS_3^{*2}+[\sum g-3g(\bar y_*)]=\Delta_\infty$, independent of every $w(\bar y)$ ⇒ Gap $\ge\Delta_\infty=+0.0386$ | identity + bound | gap monotone $\to\Delta_\infty$, never below ($\lambda\le30$) | F108; same script |

| F109-B2 | Pair composition from the rule: $U(t)\otimes U(t)$ spectrum $\{e^{2it},1,1,e^{-2it}\}$, all four eigenpairs; rotating channel = symmetric two-quantum state $\Rightarrow m_\text{comp}=\sin2t$ (L1 derived) | identity | sympy exact | F109; `test_F109_f92_bridge_construction.py` |
| F109-B3 | Phase-flow endpoint: $t_*=45°$ unique interior attractor; triple saturation exact at the endpoint ($y=\sqrt2\sin t_*=1$, $m=\sin2t_*=1$, $c^2=2\cot t_*=2$) | identity | exact; 33/33 seeds, $0.0$ deviation | F109; same script |
| F118-B2 | Brake/clock identity $W(\sum_a p_a^3)^2=\tfrac{W}{6}e^6\cos^23\delta\Rightarrow C=\tfrac{W}{6}e^6=\lambda_6 e^6$ ($\lambda_6=W/6$); the data+derived-$B$ fix $\lambda_6=0.243$, $W=6\lambda_6=1.460$ | trig identity + fit | identity exact; $W=1.4597$ vs F101 $1.46$ | F118; `test_F118_self_consistent_Wvc_and_C.py` (2026-06-09 - 12:04) |
| F118-A2 | Self-consistent $(W,v,c)$ existence on the $\kappa_E<0$ branch: lepton spectrum is the global ground state | numerical (121³ brute) — **not exact** | gap $-2\times10^{-6}$ (grid floor) | F118; same script |

| F110-C2 | Real-time link Hamiltonian, λ=0 static potential: $V(R)=\frac{g^2}{2}q^2R$ (integer arithmetic; ℤ₃ R=1–6, U(1) R=1–4) | identity | **$0.0$ exact** | F110; `test_F110_link_hamiltonian_realtime.py` (2026-06-06 - 23:55) |
| F110-C7 | One-plaquette dual U(1) KS Hamiltonian $=$ F101 compact rotor with $\chi=1/(4g^2)$ | matrix identity | **$0.0$ exact** (every entry) | F110; same script |
| F248-A | TT graviton basis for arbitrary $\hat{\mathbf k}$: $\{e^+,e^\times\}$ symmetric, traceless, transverse, orthonormal, helicity $\pm2$ | machine identity | $\le6.7\times10^{-16}$ (200 dirs) | F248; `test_F248_tt_graviton_bcc.py` (2026-07-15 - 19:14) |
| F248-B | Spin-2 TT projector $\Lambda$ idempotent, fixes both helicities, kills spin-1/0 gauge parts; common pole $q_0=c_\text{lat}\lvert\mathbf q\rvert$ from $f_2=A\,Q^2$ | sympy identity | $\le3.3\times10^{-16}$; pole $=0$ exact | F248; same script |
| 151 | F115-CM1 — EW reduction at $\sin^2\theta_W=\tfrac14$: $e=g/2$, $g'=g/\sqrt3$, $g_Z=2g/\sqrt3$ (one EW magnitude) | exact rationals | $(e/g)^2{=}\tfrac14$, $(g'/g)^2{=}\tfrac13$ | F115; `test_F115_coupling_magnitudes.py` |
| 152 | F115-CM3 — $g_s$ rotor lock: $\chi=1/(4g_s^2)$ (F110) + rule $\chi=1$ ⇒ $g_s^2\chi=\tfrac14$, $g_s=\tfrac12$ bare | identity | $g_s=0.5$ exact | F115; same script |
| 153 | F116-NJ1 — F77 NJL $\{\Lambda,G\Lambda^2,m_0\}=$ 1 ruler + 2 dimensionless; $G/G_c=1.277$ vs $G_c\Lambda^2=\pi^2/6$ | accounting | exact | F116; `test_F116_njl_lattice_calibration.py` |
| 154 | F116-NJ3 — chiral-limit pion pole $1-2G\Pi_\text{PS}(0)=0$ $\equiv$ gap equation, with BZ regularization (Goldstone) | identity | $3.6\times10^{-15}$ | F116; same script |
| 155 | F122-P2-S0 — ECG three-body engine reproduces the analytic harmonic baryon ground energy $E=3\sqrt{3k/m}$ (exact Gaussian in basis) | $=3\sqrt{3k/m}$ | $5.2\times10^{-14}$ | F122; `test_P2_baryon_bound_state.py` (2026-06-09 - 16:54) |
| 156 | F122-P2-S4 — totally symmetric (S₃) baryon spatial ground state: the three pair separations $\langle r_{12}\rangle=\langle r_{13}\rangle=\langle r_{23}\rangle$ on the permutation-closed ECG basis | three equal | $8.3\times10^{-11}$ | F122; same script |
| 157 | F128-A — the OBE sign rule: scalar (σ) exchange attractive ($\eta=-1$, density·density), isoscalar-vector (ω) exchange repulsive ($\eta=+1$, like baryon-charge $j^0 j^0$); at equal mass $V_\omega\equiv-V_\sigma$ — the channels differ by exactly one sign (same algebra as like-charge Coulomb, F69/F89) | $\eta_V{=}+1$, $\eta_S{=}-1$; $V_\omega{+}V_\sigma{=}0$ | **$0$ exact**; flip $<10^{-10}$ | F128-A; `test_F128_omega_repulsion.py` (2026-06-10 - 23:58) |
| 158 | F128-B — baryon-number coherence: $B_N=3\times\tfrac13=1$ ⇒ the three quarks couple coherently to the isoscalar ω, $g_{\omega NN}=3g_{\omega q}$, $(g_{\omega NN}/g_{\omega q})^2=9$ (the vector analogue of F126's σ-isoscalar $\times3$; SU(6) $g_{\omega NN}=3g_{\rho NN}$) | $g_{\omega NN}=3g_{\omega q}$ | **$0$ exact** | F128-B; same script |
| 159 | F128-C — transverse vector polarization reduction $\Pi_V(q^2)=-\tfrac83 N_cN_f[I_1+(q^2-M^2)K(q^2)]$ verified vs direct $k^0$-residue quadrature; the surviving $I_1$ exposes that the sharp 3-momentum cutoff breaks vector current conservation ⇒ precise NJL $m_\omega$ is scheme-dependent (mass fixed instead by the ρ–ω degeneracy, $0.95\%$) | reduction $=$ trace | $<5\times10^{-4}$ (machine) | F128-C; same script |
| 188 | F130-T1 — $c_\text{lat}$ is a block-spin RG fixed point: under $R_b$ the coarse rule is $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$, so the physical speed $b\cdot d\Omega_\text{coarse}/d\kappa\rvert_0 = d\Omega/dk\rvert_0 = 1/\sqrt3$ for every block factor $b$ (identity; verified along axis / face- / body-diagonal, all $b\in\{1..5\}$) | $c_\text{phys}=1/\sqrt3$ ∀ $b$ | $<10^{-9}$ (fit floor) | F130-T1; `test_F130_blockspin_gauge_gravity.py` |
| 189 | F130-T2 — lattice-artifact (LIV) operators are RG-irrelevant: the order-$n$ velocity operator has eigenvalue $\lambda_n=g_n^{(b)}/g_n=b^{-n}$ exactly (matched-sampling identity; $b\in\{2..5\}$, $n=2,4$); the continuum law $\Omega=c\lvert k\rvert$ is the attractive IR fixed point | $\lambda_n=b^{-n}$ | $<10^{-10}$ ($n{=}2$) | F130-T2; same script |
| 190 | F130-T3a — Gauss's law survives blocking: with $E$ blocked as coarse-face flux-sums and charge as block-sums, $\text{div}_\text{coarse}E_\text{coarse}=R_b(\text{div}\,E)$ = enclosed charge (discrete divergence theorem, integer-exact for $\mathbb Z$-flux) | residual $=0$ | $0.0$ exact | F130-T3a; same script ($b\in\{2,3,4\}$) |
| 191 | F130-T3b — gravity dielectric reciprocal lock $A\!\cdot\!B\equiv1$ preserved under $R_b$ when coarse-grained in the log variable $u=\tfrac12\ln K$ (the linear Poisson potential); the naive direct-$K$ average carries the strictly-positive Jensen gap $\langle e^{2u}\rangle\ge e^{2\langle u\rangle}$ ⇒ $u$, not $K$, is the RG-covariant variable | $A\!\cdot\!B=1$ | $1.1\times10^{-16}$ | F130-T3b; same script |
| 192 | F130-C1 — confinement is the one relevant RG direction: the F110 static-potential slope $\hat\sigma=g^2/2$ ($\lambda=0$) and the bond-moving flow $g^2_\text{coarse}=b\,g^2_\text{fine}$ give $\hat\sigma_\text{coarse}=b\,\hat\sigma_\text{fine}$ (eigenvalue $\lambda_\sigma=b>1$, vs LIV $b^{-n}<1$); a coarse F110 run on $b\times$ fewer plaquettes reproduces the fine $V(b\cdot R)$ at matched physical separation | $V_\text{coarse}(R)=V_\text{fine}(bR)$ | $0.0$ ($\lambda{=}0$); $<10^{-12}$ | F130-C1; `test_F130_blockspin_gauge_gravity.py` |
| 193 | F150-S3 — sharpened $E_g$-brake target (NOT machine-exact; a data/target match): $\cos3\delta^*=-B/(2C)=\cos Q$ with $Q$ the Koide ratio ($Q\to\tfrac23$, F92), i.e. $3\delta^*=Q=\tfrac23$ rad — both invariants of the same second-shell $E_g$ condensate; data $0.785874$ vs $\cos(2/3)=0.785887$ | $3\delta^*=Q$ | $1.7\times10^{-5}$ (target, not exact) | F150-S3; `test_F150_eg_sextic_brake.py` (2026-06-12 - 16:18) |
| 194 | F150 source no-go (structural, two-route) — the brake $C$ cannot be a free-sea loop: F95 per-axis scaling/sign ($B\sim\bar y^4$, $C_\text{loop}\sim\bar y^7$, wrong sign at saturation) ⊕ F147 one-tick rigidity (zero induced stiffness, every channel, exact) ⇒ $C$ is a condensate self-coupling; F145 fixes its kind (induced, rational); exact value = the F124/F144/F145 IR residual | structural no-go | (inherits F95/F147 exact rows) | F150; `test_F150_eg_sextic_brake.py` (2026-06-12 - 16:18) |
| 195 | F152-J2 — the IR face's freeze scale is the dual-Meissner gluon mass $m_D$ (gap-massive propagator $1/(K{+}m_D^2)$ stops the running); $m_D/\Lambda=O(1)$ ($0.86$; continuum $m_g/\Lambda=1.02$) ⇒ finite $\alpha(0)$ ⇒ model on the SATURATING/decoupling branch (not Landau-pole) | branch (numeric) | $m_D/\Lambda=0.86$ | F152-J2; `test_F152_ir_coupling.py` (2026-06-12 - 18:03) |
| 196 | F152-J4 — corrected ledger (post-F151 two-face split): the IR face owns χSB (F145/F77) + the $E_g$ brake $\lambda_6$ (F150, saturation regime); the UV face (F151: V-scheme $+a_1+q_\ast$) owns scale-setting — the pre-F151 "one shared number" framing is superseded | ledger (structural) | — | F152-J4; `test_F152_ir_coupling.py` (2026-06-12 - 18:03) |
| 197 | F153-D2 — the diamagnetic (Peierls-contact) $\delta^2 D_2$ transfer-0 operator is **charge-blind**: identical in the vector and staggered channels ($P^2=1$; the cross-term's $-P$-on-tick-2 and $V_4(\cdot+Q)=-V_4$ sign flips cancel) ⇒ the EW channel splitting $\chi_\text{stag}-\chi_\text{vec}$ is **purely paramagnetic**; analytic operator matches the dense gauged $D_2$ transfer-0 block (D1). Resolves the F149 N6/N7 sign puzzle | exact / machine | $1.1\times10^{-10}$ / $7.8\times10^{-8}$ | F153-D1/D2; `test_F153_diamagnetic_chargeblind_multiplicity.py` (2026-06-12 - 17:40) |
| 198 | F153 negatives — small-$\tilde q$ $R(m)$ NOT cleanly extractable in the two-tick sea (cone/cut artifacts: $\hat y/\hat z$ asym $0.148>$ signal $0.114$; channel-diff sign flips with $\hat q$); vector stiffness has no clean 7/8 channel count (8 eigs = 4 anisotropic pairs; face-axis $\lvert\Delta d\rvert^2{=}4$ cancels under transverse $\hat e$-sum; $m{>}0$ split localizes in antipodal channel via the staggered $-1$ tick sign); physical $E_g$ coupling $O(1)$ ($e=0.728$) ⇒ on-shell $m_Z/m_W=3/\sqrt7$ ($-0.063\%$) is exact algebra independent of $R(m)$ | numeric (neg.) + structural + algebraic | 5/5 PASS | F153-N1/M1/P1; `test_F153_diamagnetic_chargeblind_multiplicity.py` (2026-06-12 - 17:40) |
| 199 | F154-B — Residual B **solved**: the full nonlinear self-consistent gap $M(k)=m_0+24\langle G_S M/\sqrt{K+M^2}\rangle$ (Fierz $2/9$, gap-massive propagator), with $M(0)=1.50$ (=311 MeV, F77), converges to the IR coupling $\alpha_\text{eff}^\ast=0.3764$ ($m_D{=}0.532$) / $0.4111$ ($m_V{=}0.727$) — reproducing F151-S5/F152, $L$-stable ($L{=}16/24/32$); naive running overshoots ($M_0\approx1570$ MeV) | numeric (converged solve) | $\alpha_\text{eff}^\ast=0.376/0.411$; $L$-stable to $2\times10^{-5}$ | F154-B; `test_F154_residuals_A_B.py` (2026-06-12 - 19:28) |
| 200 | F154-A — Residual A cheap route **ruled out**: the gluon-propagator log-moment gives UV scales ($\langle\ln K\rangle_\text{4D}=2$ exact $\Rightarrow q_\ast^\text{bare}=e/a$; $1/K$-weighted $=2.30/a$), above F151's band; the band is reached only by an IR-divergent grid-dependent weight ⇒ $q_\ast$ is the UV-finite lattice−continuum subtraction (full $d_1$ integral), not a moment | numeric (negative) + exact | $\langle\ln K\rangle_\text{4D}=2$ (exact); $q_\ast^\text{bare}=e/a$ | F154-A; `test_F154_residuals_A_B.py` (2026-06-12 - 19:28) |
| 217 | F181 covariant two-function interior kernel (F178 follow-up): two-function areal Schwarzschild solves vacuum $G_{\mu\nu}=0$ identically; the single-scalar dielectric forces anisotropic $p_r=-p_t=-e^{-2u}u'^2/8\pi$ (reproduces F173) so it cannot be the vacuum field equation; the two-function uniform-density interior sources an isotropic perfect fluid $p_r=p_t$, $\rho=3/(8\pi a^2)$ const, with $AB\neq1$; PPN $\beta=\gamma=1$ ⇒ $K_\text{bend}=4$, redshift slope $Z=1$; exact metrics differ at $O(u^2)$ ($B$ coeff $2$ vs $\tfrac32$) and Schwarzschild has a horizon ($A\to0$) where the dielectric does not | $G_{\mu\nu}$ identities; $p_r\pm p_t$; PPN | $0$ (sympy) | F181; `test_F181_covariant_interior_battery.py` (2026-06-30 - 02:30) |
| 218 | F182 full-tensor Friedmann (F178 follow-up): differentiating Friedmann I $H^2=(8\pi G/3)\rho$ and substituting continuity $\dot\rho=-3H(\rho+p/c^2)$ yields $\ddot a/a=-(4\pi G/3)(\rho+3p/c^2)$ identically — the $+3p$ term forced by the Bianchi identity; the energy-only $\ddot a/a=-(4\pi G/3)\rho$ is consistent only if $p=0$; omitted source fraction $3w/(1+3w)$ ($\tfrac12$ radiation, $0$ dust); deceleration $q=\tfrac12(1+3w)$ ($1$ radiation, $\tfrac12$ matter) vs energy-only $\tfrac12$ | acceleration-eq identity; $q$; omitted fraction | $0$ (sympy) | F182; `test_F182_friedmann_pressure.py` (2026-06-30 - 02:45) |
| 219 | F300-G10-1/3a — closed-form low-$k$ expansion of the DERIVED paired-spinor dispersion: $\Omega_\text{pair}=c_\text{lat}\lvert k\rvert[1-A(\hat n)\lvert k\rvert^2]+O(k^5)$ with $A(\hat n)=\tfrac1{72}\sum_{i<j}\hat n_i^2\hat n_j^2+\tfrac1{24}(\hat n_x\hat n_y\hat n_z)^2$ and sphere average $\langle A\rangle=1/315$ | closed form; $\langle A\rangle$ exact | residual $O(k^4)$ relative ($4.4\times10^{-5}$); $\langle A\rangle$ to $7.8\times10^{-15}$ | F300; `casim.engine.interactions.thermodynamics` (2026-08-06 - 12:40) |
| 220 | F300-G10-2 — the paired photon is **exactly** linear along $\langle100\rangle$ at every $\lvert k\rvert$, not asymptotically: $u^\pm=\cos(k/2\sqrt3)$ on a cubic axis, so $\Omega_\text{pair}=c_\text{lat}k$ identically. The branch-odd term cancels in the $(+,-)$ sum — F67/F68 non-birefringence read off the dispersion | identity | $6.0\times10^{-14}$ out to $\lvert k\rvert=3$ | F300; ibid. |
| 221 | F300-G10-3/4/5/6 — the lattice corrections to the radiation equation of state in closed form: $u/u_\text{SB}-1=(40\pi^2/441)\Theta^2$, $\tfrac13-w=(16\pi^2/1323)\Theta^2$, $s/s_\text{SB}-1=(4\pi^2/49)\Theta^2$, and the parameter-free ratio $C_u/C_w=15/2$. $w=1/3$ in the IR is Euler's theorem on a degree-1 homogeneous $\Omega$ | closed forms from $\int x^3/(e^x-1)=\pi^4/15$, $\int x^5/(e^x-1)=8\pi^6/63$ | vs BZ quadrature $\le5.0\times10^{-4}$, residual itself $\propto\Theta^2$; ratio $6.7\times10^{-5}$ | F300; ibid. |
| 222 | F300-G10-12 — **no-go**: $2\pi\sqrt3$ nats is neither $\ln(\text{integer})$ nor $n\ln2$, so F190's per-cell entropy cannot be a microstate count of any finite cell Hilbert space. $e^{2\pi\sqrt3}=53252.295$ (0.295 from an integer); $2\pi\sqrt3/\ln2=15.7006$ (0.299) | arithmetic | exact | F300 §5; ibid. |
| F303 | The BCC nearest-neighbour graph admits **no closed 3-bond loop**, so the minimal gauge loop is the 4-bond rhombus and C7's link count $n=4$ is derived geometry | each Cartesian component of a sum of three $(\pm1,\pm1,\pm1)$ hops is a sum of three odd numbers, hence odd, hence never $0$ | 0 of $8^3$ hop triples close; 216 of $8^4$ quadruples do | exact (parity proof + exhaustive enumeration); closes the only reconciliation that would keep both $g_s=\tfrac12$ and the Casimir ($nC_F=4\Rightarrow n=3$, which would also have forced $N_c=3$ uniquely) | F303; `test_F303_coupling_normalisation.py` (2026-08-06 - 19:58) |
| F303 | F144's rotor lemma constrains only the stiffness **ratio**, so $\chi=1$ is group-blind | with $a=rb$, every entry of $M^{\rm T}M-\mathbb 1$ carries a factor $(r-1)$: $[0,0]=(r-1)\sin^2(b\sqrt r\,t)$ | orthogonality at generic tick $\iff r=1$, independent of $b$; all other roots contain $t$ (half-period tick accidents) | exact (sympy); locates F144's break at step 3 rather than at the circularity argument | F303; `test_F303_coupling_normalisation.py` (2026-08-06 - 19:58) |

| 223 | F304-B1c — the free step's 2-dim invariant subspaces are **invariant but unreadable**: a momentum block of `weyl_step_3d_bcc` leaks $2.2\times10^{-16}$ under one genuine tick, while its projector against the position-diagonal pointer algebra gives $\lVert[\Pi_k,\hat n(x)]\rVert_F=\sqrt{2/N-2/N^2}$ — closed form matched at $N=64$ with residual **literal `0.0`**. So the $d=2$ Gleason hole is structurally unreachable: every readable context is a position record on $N\ge2$ cells | closed form + measured | exact | F304; `test_F304_born_gleason.py`, record `F304-born-rule-gleason` |
| 224 | F304-B2b — **non-contextuality is a property of the generator.** The record channel is $H_\text{int}=\sum_x\hat\alpha(x)\otimes\hat n(x)$, a fixed operator of the rule carrying no reference to the measured basis, so five distinct contexts sharing a ray write the same record: weight spread **literal `0.0`**, record ray infidelity $2.2\times10^{-16}$. The basis-referencing control gives $0.1549$ / $0.4916$. Outcome-label permutation moves the weight by $2.2\times10^{-16}$ | operator identity | exact | F304; same record |
| 225 | F304-B5a — **Gleason rigidity as an integer.** The space of phase-invariant frame functions of polynomial degree $\deg$ in $\rho$ has dimension exactly $d^2$ at $d=3$ and $d=4$ for $\deg=1,2,3$ — it does **not** grow with the degree — and the computed null space **is** the Hermitian forms (every one recovered, max residual $5.7\times10^{-15}$) | rank computation | exact (integer) | F304; same record |
| 226 | F304-B5b — **the $d=2$ hole, in closed form.** The same computation at $d=2$ gives $\dim=1+\sum_{\ell\ \text{odd},\ \ell\le\deg}(2\ell+1)$: $4,4,11,11,22,22$ at $\deg=1..6$, every entry matching its closed form as an **integer** and growing without bound. Born occupies 4 dimensions of an infinite-dimensional space, which is why $d\ge3$ is load-bearing rather than decorative | rank computation vs closed form | exact (integer) | F304; same record |

| 227 | F304-B7 — **Gleason's theorem, proved rather than cited, and both halves of its dichotomy from one formula.** Averaging the frame condition over the bases containing a fixed ray gives $f+(d-1)Bf=W$ with $B$ the mean over $S(v^\perp)$; $B$ is $U(d)$-equivariant, hence a scalar on each isotypic component of $L^2(\mathbb{CP}^{d-1})$, with $$b_k=\frac{P_k^{(d-2,0)}(-1)}{P_k^{(d-2,0)}(1)}=\frac{(-1)^k}{\binom{k+d-2}{k}}.$$ A component survives iff $1+(d-1)b_k=0$. At $d=2$, $\binom kk=1$ ⇒ **every odd $k$** survives (the hole); at $d\ge3$, $\binom{k+d-2}{k}$ is strictly increasing and $>d-1$ for $k\ge2$ ⇒ **only $k=0,1$**, so $f(v)=\langle v\rvert\rho\lvert v\rangle$ on a space of dimension $1+(d^2-1)=d^2$ | closed form, Jacobi at $\pm1$ | exact | F304 §5; `test_F304_born_gleason.py`, record `F304-born-rule-gleason` |
| 228 | F304-B7b/c/d — the selection rule in **exact rational arithmetic**, no floating point: $1+(d-1)b_1=0$ **literally** for $d=2..12$; for $d\ge3$ and $2\le k\le40$ the quantity is strictly positive with minimum gap **$0.5$**, because $\binom{k+d-2}{k}$ is strictly increasing in $k$ and already exceeds $d-1$ at $k=2$ ($\binom d2=d(d-1)/2>d-1\iff d>2$); at $d=2$ the survivors are exactly $k=1,3,5,7,9,11,\dots$ | integer / `Fraction` | exact | F304 §5.3; same record |
| 229 | F304-B7a — the operator $B$'s **spectrum** on the degree-$\le k$ phase-invariant functions matches that closed form **with $\dim V_k=\binom{k+d-1}k^2-\binom{k+d-2}{k-1}^2$ multiplicities** at $(d,k)=(2,1),(2,3),(3,1),(3,2),(4,1),(4,2)$, deviation $\le1.6\times10^{-15}$, and the function-space dimensions $4,16,9,36,16,100$ agree as **integers**. The declared control $b_k\to(-1)^k/(d-1)^k$ — correct at $k\le1$, wrong from $k=2$ — reds it | spectrum vs closed form | exact (integers) + machine | F304 §5.4; same record |
| 230 | F304-B7e — the proof **predicts** rows #225/#226, which were rank *measurements* made before it existed: $1+\sum_{k\ \text{odd}\le\deg}(2k+1)=4,4,11,11,22,22$ at $d=2$ and $1+\dim V_1=d^2$ at $d\ge3$, every entry agreeing as an integer with no fitting | prediction vs prior measurement | exact (integer) | F304 §5.4; same record |
| 231 | BCC rhombus half-normal closure $\sum_p m_pm_p^{\mathsf T}$ over the 6 $\langle110\rangle$ orientations | $= 4I$ | exact over $\mathbb Z$ (integer arithmetic, no float) | F323 leg X1a; F265; `bcc_action.bcc_closure_identities` |
| 232 | BCC link-axis closure $\sum_a aa^{\mathsf T}$ over the 4 $\langle111\rangle$ axes | $= 4I$ | exact over $\mathbb Z$ | F323 leg X1a; `bcc_action.bcc_closure_identities` |
| 233 | Derived anisotropy $\beta_t/\beta_s = 4/(3c_\text{lat}^2)$ and $\xi^2 = 1/c_\text{lat}^2$ at $c_\text{lat}^2=1/3$ | $\beta_t/\beta_s = 4$, $\xi^2 = 3$ | exact `Fraction`; ratio to the hypercubic $\xi^2$ is exactly $4/3$ | F323 legs X1b, X1d; `bcc_action.anisotropy_from_c_lat` |
| 234 | Casimir ratios $C_2(R)/C_F$ from Dynkin labels for 3, 6, 8, 10 | $1$, $5/2$, $9/4$, $9/2$ | exact `Fraction`, computed not tabulated | F323 leg K1c; F299 §2; `bcc_action.casimir_ratio_exact` |
| 235 | Staple is $dS/dU$: $\sum_\text{links}\operatorname{Re}\operatorname{tr}(UA) = 4\sum_\text{loops}\beta\operatorname{Re}\operatorname{tr}P$ on $\mathrm{BCC}_3\times\mathbb Z$ | equality | $2.3\times10^{-16}$ (isotropic), $2.4\times10^{-16}$ ($\beta_t\neq\beta_s$) | F323 legs S1a/S1b; `bcc_action.staple_identity_residual` |
| 236 | Microcanonical over-relaxation preserves the BCC Wilson action | invariant | literal $0.0$ | F323 leg O1a; `bcc_action.sweep_4d(mode='overrelax')` |
| 237 | Translation covariance of the BCC staple construction (cubic shift, time step, $\langle111\rangle$ hop) | covariant | literal $0.0$ | F323 leg T1a |
| 238 | F299's character polynomials against EXPLICIT rep matrices ($\mathrm{Sym}^2$, $\mathrm{Ad}$, $\mathrm{Sym}^3$) | $\chi_R(U) = $ polynomial | $\le 4.6\times10^{-16}$ over 6 Haar samples | F323 leg K1a; `bcc_action.character_identity_residual` |
| 239 | F403 — $O$ residual eigenlines on $T_{1u}$: every non-identity rotation fixes a PMNS column $(1,0,0)$, $(0,\tfrac12,\tfrac12)$ or all-$\tfrac13$ in the cube-axis frame; TM1 $(\tfrac23,\tfrac16,\tfrac16)$ from like-sign $C_2'$ in the trimaximal frame (2026-09-24 - 11:30) | exact rationals | 0 (sympy) | `F403-oh-residual-pmns` legs E1, B1 |
| 240 | F403 — gCP residuals: diagonal $X\Rightarrow J=0$; $y\leftrightarrow z$ mirror $\Rightarrow\theta_{23}=\pi/4$ and $\lvert U_{\mu1}\rvert^2-\lvert U_{\tau1}\rvert^2=\sin2\theta_{12}\sin\theta_{13}\cos\delta$; $C_3$/$C_4$-invariant symmetric $M$ has a degenerate pair (2026-09-24 - 11:30) | identity | 0 (sympy) | `F403-oh-residual-pmns` legs C1, E2 |
| 241 | F404 — for Hermitian amplitude $S$: $Q_\text{phys}-Q_\text{pseudo}=\lVert S_\text{off}\rVert_F^2/(\operatorname{tr}S)^2$; real symmetric $S_U,S_D\Rightarrow J=0$ (CP needs $T_{1g}$) (2026-09-24 - 13:10) | identity | 0 (sympy) | `F404-koide-pseudomass-fork` legs P1, P6 |
| 242 | F403 — subgroup lattice of $O_h$ on $T_{1u}$: 98 subgroups (30 in $O$); a subgroup admits a non-degenerate invariant symmetric mass matrix iff it is elementary abelian 2 (49 subgroups, orders 1/2/4/8); forced columns ⊂ element eigenlines; the 4 BCC $[111]$ directions have Gram off-diagonal $-\tfrac13$ (2026-09-24 - 14:16) | exact (sympy closure + symbolic discriminant) | 0 | `F403-oh-residual-pmns` legs S1, S4 |
| 243 | F405 — Koide $Q=(1+k^2)/3$ is $\delta$-blind and the $\cos3\delta$ coefficient of $\sum y^4$ is $3\bar yA^3$, so $B(k)=k^3B(1)$ and no factor on $B$ moves $k$; an identity-class dressing (uniform $m\to\lambda m$, overall loop factor, mass-independent running) leaves $Q$ invariant (2026-09-24 - 15:40) | exact (sympy); U1/U2 identities | 0 | `F405-quark-B-colour-charge` legs E1, E2, U1, U2 |
| 244 | F406 — lepton frame fork: $\operatorname{Tr}(F\Lambda F^\dagger)^k=\sum\lambda^k$ ($k\le6$) so F118 is spectral (exact (a)/(b) tie); three $O_h\times T$-inequivalent Koide circulants $\arg b=\tfrac29+2\pi j/3$ with τ/e/μ on $(1,1,1)$ and $\arctan(T_{1g}/T_{2g})=\tfrac29,\ \pi/3\mp\tfrac29$; Molien kernel dims 2 (quadratic), 6 (cubic); quadratic crystal-field bounds $R+I\le\tfrac32$, $I\le\tfrac32\sin^2(\pi/3+\tfrac29)$ (2026-09-24 - 15:20) | exact (sympy + closed-form bounds) | 0 | `F406-lepton-frame-fork` legs K1, K3, K5, K7, K8 |
| 245 | F408 — heat-kernel sign split over the model content (48 Weyl, 0 fundamental bosons): $a_0<0$, $\sum\eta_i=g_*/12=4>0$, $\operatorname{sign}a_0\operatorname{sign}a_1=-1$ (Lichnerowicz $R/4$ flips $a_1$ only) (2026-09-27 - 11:38) | identity | 0 (`Fraction`) | `F408-cc-sign-split` legs S1; `cosmology_lambda_sign_split.heat_kernel_signs` |
| 246 | F408 — same content in both moments: $\lvert\rho_{a_0}\rvert(a/R_H)^2\,/\,(3c^4/8\pi GR_H^2)=4N_bI_\text{cc}/(3\sum\eta)=24\sqrt3\pi$, independent of the field count and of $H_0$; the diluted $a_0$ term and F196 are opposite in sign (conditional on composite gauge bosons) | closed form | 0 (sympy) | `F408-cc-sign-split` leg S2-ratio-closed-form |
| 247 | F408 — capacity saturation $2Gm/Lc^2=1$ has no positive root and flat Friedmann-I no real $H$ for $\rho<0$ alone: the one-sided F183/F190 ceiling cannot cancel a negative $a_0$ (elementary) | no-go | exact (sympy) | `F408-cc-sign-split` legs S3 |
| 248 | F408 — capacity energy $E(L)=\sigma_HL$, $\sigma_H=c^4/2G=4\sqrt3\pi\hbar c/a^2$ (linear, sign of $a_1$); Kaloper–Padilla residual independent of $C\in\mathbb R$ (sign-blind) | identity | 0 (sympy) | `F408-cc-sign-split` legs S4, S5 |

(F110 Tier-2 companions: C1 direct link-basis Gauss-sector spectrum == dual height spectrum, vacuum + charged, $\le1.9\times10^{-14}$; C5 real-time norm/⟨H⟩ drift $\le2\times10^{-14}$ over $t\in[0,20]$, Krylov certified vs dense eigendecomposition $5\times10^{-13}$; C7 σ₁ truncation convergence $3\times10^{-14}$, F101 table contact $3.6\times10^{-6}$. Tier-3: C3 increment-estimator $V(R)-V(R-1)$ Cauchy $3.8\times10^{-3}$, σ(λ)=0.4923/0.4303/0.2354 at λ=0.2/0.5/1.0; C4 strong-coupling PT $c_2=1/6$, Richardson ratio 0.9992; C6 flux-tube GS excess fractions 0.61 vs 0.31, quench persistence 0.36 vs melt −8.0.)

**Count: 180 exact algebraic results.** (+4 from F304 §5, rows #227-230, 2026-08-06 - 18:20 — **this is F304 removing its own external citation**: Gleason's theorem is now proved here for $f\in L^2$, and the proof is strictly better than the citation in one respect — the $d=2$ hole and the $d\ge3$ rigidity fall out of the *same line* of the *same formula* $b_k=(-1)^k/\binom{k+d-2}{k}$, so "why is $d\ge3$ the hinge" is answered by an inequality on binomial coefficients rather than deferred. The selection rule is checked in `Fraction` arithmetic (literal zero at $k=1$, strict gap $0.5$ for $k\ge2$), the operator spectrum against the closed form *with* $\dim V_k$ multiplicities, and the whole thing then **predicts** the integers rows #225/#226 had merely measured. What remains cited is one lemma, not a theorem: Cooke–Keane–Moran regularity. `test_F304_born_gleason.py`, record `F304-born-rule-gleason`.) (+4 from F304, rows #223-226, 2026-08-06 - 15:40: the momentum-block commutator closed form $\sqrt{2/N-2/N^2}$ matched at residual **literal `0.0`** (invariant but unreadable, so the $d=2$ Gleason hole is unreachable); the context-blindness of the record channel, weight spread **literal `0.0`** across five contexts sharing a ray with the basis-referencing control at $0.1549$; and the two halves of the Gleason dichotomy as **integers** -- frame-function space dimension $=d^2$ at $d=3,4$ for every degree, versus $1+\sum_{\ell\ \text{odd}\le\deg}(2\ell+1)=4,4,11,11,22,22$ at $d=2$. `test_F304_born_gleason.py`, record `F304-born-rule-gleason`.) (+4 from F300, rows #219-222, 2026-08-06 - 12:40: the closed-form paired-photon dispersion expansion with $\langle A\rangle=1/315$, its exact $\langle100\rangle$ linearity, the three radiation-EoS coefficients with the parameter-free $15/2$ ratio, and the $2\pi\sqrt3$ integrality no-go. +1 from F294, row #168, 2026-08-05 - 22:10: the F110 C7 map $\chi = 1/(4g^2)$ extracted at **every non-zero level of every group** across $\mathbb Z_2,\mathbb Z_3,\mathbb Z_4,\mathbb Z_5,\mathbb Z_7,\mathbb Z_9$ and compact $U(1)$, worst deviation **literal `0.0`** -- the $s(m)^2$ cancels between the electric term and the rotor level, so the identity holds per level and is blind to which levels the group supplies. Non-trivial because the $\mathbb Z_N$ level SET does depend on $N$. This is the measurement underpinning F293 sec.4.1's $N_c$-free bare coupling; note F294 sec.4 for the half that does NOT survive a Casimir reading. `test_F293_why_three_colours.py` checks B6/B6b.) (+2 from F293 / row B10, rows #166-167, 2026-08-05 - 20:55: the full six-constraint hypercharge system has rank 6 and nullspace dimension **1 for every $N_c$** -- verified symbolically in $N_c$ over $\mathbb Q$ and at $N_c=1,2,3,4,5,7$, with ratios $1:(N_c{+}1):(1{-}N_c):-N_c:-2N_c:0$ and both the gravitational and cubic $U(1)^3$ anomalies identically zero **as polynomials in $N_c$**, so anomaly freedom provably selects no $N_c$; and the internal-index control for the colour-is-not-spatial no-go commutes at literal `0.0` while the $O_h$ 3-cycle gives $\max_a\lVert[C_3,\lambda^a]\rVert = 2.449$. `test_F293_why_three_colours.py`, record `F293-why-three-colours`.) (+7 from F289/F281-scaleup, rows #159-165, 2026-08-05 - 18:40: the SWAP involution $\lVert\text{SWAP}^2-\mathbb 1\rVert$ = literal `0.0` with spectrum exactly $\{+1^{(3)},-1^{(1)}\}$ (deviation `0.0`) -- exactly two statistics, the $d\ge3$ consequence; the Jordan-Wigner anticommutators $\{c_i,c_j\}$ and $\{c_i,c_j^\dagger\}-\delta_{ij}$ both literal `0.0`, with the string-removed control at 4.0; Pauli exclusion $c_i^\dagger c_i^\dagger$ = literal `0.0`; the antisymmetriser rank $15=\binom62$ and the $k$-particle sector dimensions $[1,6,15,20,15,6,1]=\binom6k$ exactly as integers (differing from the bosonic $\binom{n+k-1}k$); $R(2\pi)=-\mathbb 1$ at $1.73\times10^{-16}$ over 60 axes and the paired-spinor photon pair phase $+1$ at $3.46\times10^{-16}$; and from the F281 scale-up the commutant of $\{\hat n(x)\}$ having dimension exactly $2^n$ for $n=1..4$ (maximal abelian by matrix rank, so the pointer basis is unique up to phase). `test_F289_spin_statistics.py`, `test_F281_measurement.py`.) (+4 from F281 measurement / A8, rows #155–158, 2026-08-05 - 15:10: the pointer commutator $[H_\text{int},\hat n(y)] = 0$ for the model's own minimal-coupling generator (literal `0.0`, not $10^{-16}$ — every term is diagonal in site occupation, so einselection has no freedom left); the $\ell^2$ change under one real BCC Weyl tick (literal `0.0`, while every other $\ell^p$ moves 3–32%, and the SWAP permutation control conserves all $p$); the fine-grained Born weights $p_k = \lvert c_k\rvert^2$ exact over $\mathbb Q$ with amplitude and envariance residuals both literal `0.0`; and the block-spin coherence eigenvalue $\lambda_\text{coh}(k{=}0,b) = 1$ with coarse-vs-fine charge residual `0.0`, whose $k\ne0$ envelope exponent is exactly $-2$ per dimension. `test_F281_measurement.py`, record `F281-measurement-pointer-born-rg`.) (+4 from F115/F116, rows #151–154: the EW one-magnitude reduction, the $g_s$ rotor lock $g_s^2\chi=\tfrac14$, the NJL dimensional accounting $G/G_c=1.277$, and the BZ-regularized chiral Goldstone identity, 2026-06-08.) (+2 from F110: the λ=0 linear potential in integer arithmetic and the rotor χ-map matrix identity, 2026-06-06 - 23:55.) (+3 from F108: the $\sigma_1$ trace identity, the refit invariance, and the shadow-cancellation no-go bound.) (+1 from F64-D-EM-D1: the *dielectric* curved-background stepper at $m=0$, flat $A=B=1$, reduces bit-for-bit to two decoupled exact-QCA Weyl walks, residual $0.0$, row #150; `test_F64_em_connection.py`, 2026-05-31 - 16:00.) (+1 from F62-D1: the curved-background gravity stepper at $m=0$, flat $A=B=1$, reduces bit-for-bit to two decoupled exact-QCA Weyl walks, residual $0.0$, row #149; `test_F62_dirac_gravity_fork.py`, 2026-05-30 - 16:10.) (+7 from F54 FG-8 β-decay charged current, rows #142–148: SU(2) raising/lowering algebra, $d\to u$ raising + transition charge, both-vertex charge conservation, V−A parity violation, quark–lepton universality, heavy-W Fermi limit at $q^2{=}0$, full-process $\Delta Q=\Delta B=\Delta L=\Delta(B-L)=0$, 2026-05-29 - 20:47.) (+6 from F53 FG-9 antiparticle/per-species $C$,$CP$, rows #136–141 — recorded by the concurrent FG-9 session; see changelog 2026-05-29 - 21:10.) (+3 from F44-W6.10 promotion sanity: zero gauge field + $U_\text{st}=I$ gives $\mathcal L = 0$ exact; zero gauge field + constant non-identity $U_\text{st}$ gives $\mathcal L = 0$ exact (translation covariance of the lattice difference); Cayley-Klein path and direct 2×2 matrix path agree bit-for-bit, 2026-05-28 - 00:40.) (+4 from F46 spherical Pythagorean lattice-mass identity: closed-form 2D identity, 4×4 $D_k$ eigenvalue identity, BCC extension both helicities, rest-limit identity across 8 masses, 2026-05-28 - 22:50.) (+13 from F43 FG-7 dynamical SU(3) gluon sector: Jacobi identity for $f^{abc}$, octet bilinear adjoint identity (2D + BCC), Casimir invariance, identity links $\Rightarrow G^a = 0$ on both lattices, constant-$V$ plaquette magnitude invariance, cold Wilson loop $= N_c$, local-$V$ Wilson loop gauge invariance, octet charge density wrapper, diagonal source coupling, massless step reduction to free step, 20-tick off-diagonal preservation, 2026-05-28 - 01:30.) (+1 from F44-W6.9 lattice horizontal-SU(2)_L preservation: $W^1$/$W^2$ block bit-for-bit decoupled from $(W^3, B)$ and bit-for-bit mass-degenerate, on the discrete covariant Stueckelberg operator, 2026-05-28 - 00:20.) (+3 from F44 rank-1 Stueckelberg mass block: $\det = 0$ at machine ε, spectral decomposition matches W6.1 rotation, two-field vs. single-field cross-term separation, 2026-05-28 - 00:05.) (+4 from F45 σ↔τ swap Weinberg angle: dimensional decomposition forces $g'^2/g^2 = 1/3$; $\sin^2\theta_W = 1/4$; $\cos^2\theta_W = 3/4$; Casimir cross-check, 2026-05-27 - 14:30. Plus the algebraic mass ratio $m_Z/m_W = 2/\sqrt 3$ at 1-ulp.) (+3 from F42 quark hypercharge extension + dynamical $\chi$ kinetic step: quark $\alpha=0$ bit-for-bit reduction, $\chi$ kinetic $\alpha=0$ bit-for-bit reduction across all $Y$, quark GMN algebra, 2026-05-27 - 09:00.) (+3 from F41 hypercharge fork: bit-for-bit F27 reduction, zero isospin leakage at $U=I$, and the GMN / Higgs-Y algebra, 2026-05-26 - 17:45.) (+4 from FG-6 two-helicity photon bilinear: assembler linearity, per-helicity dispersion, F30 birefringence, Riemann-Silberstein identity, 2026-05-26.)

---

## Tier 2 — Machine-precision results (FFT round-off floor) (curated)

| # | Construct | Predicted form | Measured residual | Scaling | Source |
|---|---|---|---|---|---|
| F248-C | TT graviton non-birefringence on the BCC even law: two helicities share one scalar $\Omega(\mathbf k)$ | $\Delta\Omega\equiv0$; slope $=1/\sqrt3$ all dirs; $O((ka)^2)$ anisotropy | $\Delta\Omega=0$ exact; slope dev $\le7\times10^{-9}$ | direction-independent to $k\to0$ | F248; `test_F248_tt_graviton_bcc.py` (2026-07-15 - 19:14) |
| F248-D/E | TT packet speed $=c_\text{lat}$ (both pols); explicit BCC constituent loop helicity-degenerate + spin-2 form factor $\propto\lvert\mathbf q\rvert^2$ | $c_\text{lat}=1/\sqrt3$; degeneracy $0$; quadratic | $0.9998\,c_\text{lat}$; degeneracy $4.5\times10^{-16}$; quad $1.4\times10^{-4}$ | grid-limited (D); $n^3$ BZ (E) | F248; same script |
| 1 | Weyl regression at $m=0$ from Dirac stepper | exact identity in the $m \to 0$ limit | $1.55 \times 10^{-15}$ at $L=320$ | $\sqrt{N_\text{cells}}$ floor | D1; `ca_dirac.py` |
| 2 | Norm drift, Cayley variable-$c$ stepper | unitary | $5.5 \times 10^{-15}$ | exact-unitary (vs 32.6% Strang drift) | F3b / C1; `ca_curved.py` |
| 3 | Norm drift, BCC 200-step | unitary | $3.7 \times 10^{-14}$ | $\sqrt{N}$ per step | L1; `ca_bcc.py` |
| 4 | Norm drift, 2D arccos QCA 200-step | unitary | $8.4 \times 10^{-15}$ | $\sqrt{N}$ per step | L2; `ca_core_exact.py` |
| 5 | Per-step FFT round-off floor — D1 norm over 1000 steps | unitary | $4.0 \times 10^{-13}$ at $L=320$ | exact 10× ratio from $L=32 \to 320$ (Finding 5) | D1; `ca_dirac.py` |
| 6 | Per-step FFT round-off floor — L2 norm over 200 vs 2000 steps at $L=320$ | unitary | $7.6 \times 10^{-13}$ at $n=2000$ | $= 9.985\times$ that at $n=200$ (linear-in-$n$ to 4 figures) | Finding 5; L2 |
| 7 | Poynting energy conservation of composite-photon bilinear: $abs(E_G)^2 + \abs(B_G\)^2 = 4abs(n)^2\abs(G_T\)^2 = $\mathrm{const}$ (Mohr Eq. 55) | constant | $4.5\times 10^{-14}$ over 200 steps, 12 directions — matches $\sim N\cdot\varepsilon$ accumulation ($200\times 2.2\times 10^{-16}$) | `ca_maxwell.py` `composite_photon_energy_conservation` |
| 8 | Global colour charge $Q^a = \sum_x q^\dagger T^a q$ conserved under cold-link SU(3) Strang stepper | $\Delta Q^a = 0$ | $3.8\times 10^{-13}$ over 200 steps at $L=32$ ($m=0.3$, mixed (u,r)+(u,g) packet) | FFT round-off floor | V13b2; `test_su3_noether.py` |
| 9 | Quark-field unitarity under local SU(3) gauge transformation — $\lVert q(t)\rVert = \lVert V(x) q(t) \rVert$ (V random Haar per cell) preserved through 20 Strang ticks of `step_strong_2d` | identity | $4.3\times 10^{-14}$ at $L=16$, $n=20$ | $\sqrt{N}\cdot n$ FFT floor | V13b4; `test_su3_noether.py` |
| 10 | Poynting energy $\|E_G\|^2 + c^2\|B_G\|^2$ conservation under composite-photon propagation (Mohr Eq. 55) | constant | $4.77\times 10^{-14}$ over 200 steps, 12 dirs; per-step rate $1.4\times 10^{-16} \approx \varepsilon_\text{machine}$ at 10 000 steps | $N\cdot\varepsilon$ linear accumulation; algebraically exact (Finding 17) | `ca_maxwell.py::composite_photon_energy_conservation_c2` |
| 11 | C3 refinement — V6 boost transversality at $k'_s$ using the bilinear-derived polarization $\hat\varepsilon_G = G_T/\|G_T\|$ | $= 0$ | $2.9\times 10^{-15}$ across 8 (k, v) pairs | FFT floor on 6×6 matrix algebra | `ca_maxwell.py::lorentz_boost_covariance_bilinear_transversality` |
| 12 | C5 — VSH $J_z$ eigenvalue via $L_z + S_z$ central finite difference (h=10⁻⁴) | $J_z Y^m_{jl} = m Y^m_{jl}$ | $1.1\times 10^{-8}$ over $j \le 2$, 4 directions | $O(h^2)$ central-diff truncation floor | `ca_maxwell.py::test_vsh_Jz_eigenvalue` |
| 13 | $\rho(m) = u_p/u_g$ at $k \to 0$: analytic formula vs numerical ratio at $k=10^{-6}$, $m \in [0.05, 0.90]$ | exact closed form | max residual $3.4\times 10^{-14}$ at $m=0.90$; $2.2\times 10^{-16}$ at $m=0.05$ | grows toward $m=1$ edge of parameter space | Finding 22; `casim.engine.interactions.derive_velocity_addition` |
| 14 | V13c.2 — Colour charge conservation $Q^a$ with spatially varying Yukawa Φ(x), cold links, 50 steps | $\Delta Q^a = 0$ | $1.78\times 10^{-14}$ (max over 8 generators, 50 steps) | FFT floor; 4 orders below tol $5\times 10^{-9}$ | V13c.2; `test_su3_noether.py::gate_V13c_yukawa_wiring` (2026-05-22) |

| 15 | C8 — k-scan O(k) slope: curl\_E/k → $c_\text{lat}/\sqrt{2} = 1/\sqrt{6} \approx 0.408248$ (flat across a decade in $k$); rot\_E/k → 0 (noise floor only, no systematic growth) | curl\_E/k = $c_\text{lat}/\sqrt{2}$ (algebraic, F23 #49); rot\_E/k = 0 | curl\_E/k: 0.408256 at $k=10^{-3}$ to 0.408938 at $k=0.1$ (monotone, theory-expected lattice correction); rot\_E/k: $<1.2\times 10^{-13}$ across all $k$ | Finding 25 (**CORRECTED 2026-08-04, F306/S18**: curl\_E/k is quadrature between two orthogonal equal-length vectors, not a physical coefficient; rot\_E/k is zero *by construction* — the rotation law is the real form of $e^{-i\Omega}$. Under analytic amplitudes the curl residual falls as $c_\text{lat}^3k^2/48$); `casim.engine.gauge.bilinear::real_rotation_k_scan` (2026-05-23) |
| 16 | F26 — Full-lattice rotation propagator (3D BCC): `rotation_step_em_spectral` propagates $(E,B)$ for 20 ticks; rotation-law residual vs exact prediction | $\leq 2\varepsilon_\text{machine}$ per step | $2.8\times 10^{-16}$ (E), cf. Maxwell curl $2.0\times 10^{-2}$ at $k=0.05$ — 5 orders of magnitude below | F26; `ca_maxwell.py::rotation_law_consistency` (2026-05-23) |
| 17 | F26 — Full-lattice rotation propagator (2D square): same test on 2D QCA | $\leq 2\varepsilon_\text{machine}$ per step | $2.2\times 10^{-15}$ (E), $1.3\times 10^{-15}$ (B), cf. Maxwell curl $1.8\times 10^{-2}$ — machine precision | F26; `ca_maxwell_2d.py::rotation_law_consistency_2d` (2026-05-23) |
| 18 | W3.4 — Link unitarity preserved after Yang–Mills self-coupling steps: SU(2) product closure; $\|a\|^2+\|b\|^2=1$ per link | unitary | $\le 10^{-13}$ | W3.4; `test_wmu_phase3.py` (2026-05-24) |
| 19 | W4.2 — Isospin charges $T^a = \sum_x \psi^\dagger (\tau^a/2) \psi$ conserved at $g=0$ (free doublet): no gauge coupling → no source term for $\dot T^a$ | $\Delta T^a = 0$ | $2.741\times 10^{-17}$ over 10 steps | W4.2; `test_wmu_phase4.py` (2026-05-24) |
| 20 | W4.5 — Weak neutral current residual: $W^3$ couples to $T_3 = \pm\tfrac12$ of left-handed doublet; coupling strength asymmetry $\ge 10^{-6}$ | structural non-zero | $1.854\times 10^{-13}$ | W4.5; `test_wmu_phase4.py` (2026-05-24) |
| 21 | W5.2 — Link unitarity after 10 Stueckelberg mass steps: SU(2) product preserves $(a,b)$ Cayley–Klein norm | $\|a\|^2+\|b\|^2=1$ | $1.776\times 10^{-15}$ | W5.2; `test_wmu_phase5_stueckelberg.py` (2026-05-24) |
| 22 | W6.2 — Commutator $[\text{mix}, \text{propagate}] = 0$: Weinberg rotation (constant $O(2)$ in $(B,W^3)$) commutes with F26 BCC propagation (diagonal in $k$-space) | $= 0$ | $1.554\times 10^{-15}$ | W6.2; `test_wmu_phase6.py` (2026-05-24) |
| 23 | W6.5 — $[\text{mix}(\theta_W), \text{propagate}] = 0$ for all $\theta_W \in \{0.1, 0.3, 0.5, 0.7, 1.0\}$ | $= 0$ for each angle | $2.220\times 10^{-15}$ (max) | W6.5; `test_wmu_phase6.py` (2026-05-24) |
| 24 | WB.2 — `fermion_isospin_current` equal-mix state: $J^1 = |\psi|^2/2$ to FFT round-off | $J^1 = |\psi|^2/2$, $J^2=J^3=0$ | $J^1$ err $1.78\times10^{-15}$; $J^2,J^3 \leq 2.1\times10^{-16}$ | WB.2; `test_wmu_phase7_backreaction.py` (2026-05-24) |
| 26 | F37.1 — Chiral propagation: $F^+$ eigenstate tracks $\Omega^+(k) = 2\omega_+(k/2)$ to machine precision (8 modes, $n=200$ steps, L=16) | $F^+(k,n) = F^+(k,0)\,e^{-i\Omega^+ n}$ | $2.9\times10^{-14}$ max relative error | F37; `test_F37_delta_omega.py` (2026-05-24) |
| 27 | F37.2 — Chiral propagation: $F^-$ eigenstate tracks $\Omega^-(k) = 2\omega_-(k/2)$ to machine precision (8 modes, $n=200$ steps) | $F^-(k,n) = F^-(k,0)\,e^{+i\Omega^- n}$ | $2.3\times10^{-14}$ max relative error | F37; `test_F37_delta_omega.py` (2026-05-24) |
| 28 | F37.3 propagation — $\Delta\Omega = \Omega^+ - \Omega^-$ measured at $(1,1,1)$ mode (L=32, $n=10$ steps) vs exact dispersion | exact dispersion value | $1.1\times10^{-14}$ relative error | F37; `test_F37_delta_omega.py` (2026-05-24) |
| 29 | F37.4 — Energy conservation under chiral propagation ($n=300$ steps, L=16, random field): $\|E^a\|^2+\|B^a\|^2 = \mathrm{const}$ | unitary (each mode gets unit-modulus phase; Nyquist bins use even-average) | $4.6\times10^{-14}$ relative drift | F37; `test_F37_delta_omega.py` (2026-05-24) |
| 25 | WB.4 — Massive Proca W dispersion $\omega^2 = m_W^2 + \Omega_\text{even}^2(k)$: closed-form prediction $C_n = C_0 e^{-i\omega_\text{eff} n}$ vs. evolved amplitude for $m_W \in \{0.1, 0.3, 0.8\}$ | $\leq 2\varepsilon_\text{machine}$ per step | $\leq 1.4\times10^{-13}$ (max over all $k$, all 3 masses) | WB.4; `test_wmu_phase7_backreaction.py` (2026-05-24) |
| 30 | F40-Q1 — Unitarity of `step_strong_2d_complex_mass` over 20 steps with random per-flavour $\theta$ field; cold SU(3) links; mixed-chirality state | norm conserved | $5.4\times 10^{-15}$ (L=16, n=20) | F40-Q1; `test_FG2_quark_complex_mass.py` (2026-05-26 - 16:30) |
| 31 | F40-Q8 — Colour-charge $Q^a$ conservation under `step_strong_2d_complex_mass` (cold links, random $\theta$, 20 steps) | $\Delta Q^a = 0$ | $1.7\times 10^{-14}$ rel (abs $1.5\times 10^{-14}$) | F40-Q8; `test_FG2_quark_complex_mass.py` (2026-05-26 - 16:30) |
| 32 | F40-QE4 — Norm conservation of `covariant_quark_doublet_step_2d` over 20 steps with **random** $W$-links (site-averaged $U_\text{eff}$ unitary at each cell) | unitary | $2.1\times 10^{-14}$ (L=12, n=20) | F40-QE4; `test_FG3_quark_electroweak.py` (2026-05-26 - 16:30) |
| 33 | F40-QE6 — Colour-charge $Q^a$ conservation under the W-coupled doublet step (cold colour links, random $W$, 20 steps) — SU(2)$_L$ does not leak into SU(3) | $\Delta Q^a = 0$ | $2.5\times 10^{-14}$ rel | F40-QE6; `test_FG3_quark_electroweak.py` (2026-05-26 - 16:30) |
| 34 | F41-Y1 — $U(1)_Y$ Ward identity for the Higgs-free mass step, e-branch: $V_Y(x)\cdot\text{mass}(\psi;U,\alpha{=}0) \equiv \text{mass}(V_Y\psi;\,U,\alpha{=}\beta)$ where $V_Y = e^{i\beta(x) Y_\psi/2}$ acts per-chirality with $Y_L=-1, Y_{e_R}=-2, Y_{\nu_R}=0$ | algebraic identity (Higgs-Y absorbed in $U(x)$) | $9.04\times10^{-16}$ on $L=24$ random $\beta(x)$ | F41-Y1; `test_hypercharge.py` (2026-05-26 - 17:45) |
| 35 | F41-Y2 — $U(1)_Y$ Ward identity, ν-branch (conjugate-Higgs $\Delta Y_\nu = -1$) | algebraic identity | $9.16\times10^{-16}$ | F41-Y2; `test_hypercharge.py` (2026-05-26 - 17:45) |
| 36 | F41-Y4 — F27 $SU(2)_L$ Ward identity preserved with nontrivial $U(1)_Y$ field $\alpha(x)$: $V_L\cdot\text{mass}(\psi;U,\alpha) = \text{mass}(V_L\psi;\,V_L\!\cdot\!U,\,\alpha)$ | algebraic identity (Y-phase commutes with SU(2)_L on isospin) | $9.16\times10^{-16}$ | F41-Y4; `test_hypercharge.py` (2026-05-26 - 17:45) |
| 37 | F41-Y6 — Mass-step unitarity over 50 random $(U,\alpha)$ steps: $M = c_m I + i s_m A$ with $A^\dagger = A$, $A^2 = I$ preserved under the Higgs-Y extension | unitary | $4.53\times10^{-15}$ relative norm drift | F41-Y6; `test_hypercharge.py` (2026-05-26 - 17:45) |
| 38 | F42-Y8 — Quark $U(1)_Y$ Ward identity, d-branch (Higgs $\Delta Y_d = +1$): $V_Y\cdot\text{mass}_\text{quark}(\psi;U,0) \equiv \text{mass}_\text{quark}(V_Y\psi;U,\beta)$ | algebraic identity | $8.89\times 10^{-16}$ on $L=24$ random $\beta(x)$ | F42-Y8; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 39 | F42-Y9 — Quark $U(1)_Y$ Ward identity, u-branch (conjugate-Higgs $\Delta Y_u = -1$) | algebraic identity | $8.95\times 10^{-16}$ | F42-Y9; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 40 | F42-Y11 — F27 $SU(2)_L$ Ward identity preserved with nontrivial $\alpha(x)$ on the quark side: $V_L\cdot\text{mass}_\text{quark}(\psi;U,\alpha) = \text{mass}_\text{quark}(V_L\psi;V\!\cdot\!U,\alpha)$ | algebraic identity (Y-phase commutes with SU(2)$_L$) | $9.93\times 10^{-16}$ | F42-Y11; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 41 | F42-Y12 — Quark mass-step unitarity under the Y-extension, 50 random $(U,\alpha)$ steps | unitary | $4.43\times 10^{-15}$ relative norm drift | F42-Y12; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 42 | F42-Y13 — Dynamical $\chi$ kinetic step is **exactly** $U(1)_Y$-gauge-covariant: $S[\alpha+\beta](e^{i\beta(x)Y/2}\chi) = e^{i\beta(x)Y/2}S[\alpha](\chi)$ for each of $e_R$ ($Y=-2$), $u_R$ ($Y=+4/3$), $d_R$ ($Y=-2/3$) with random $\alpha(x), \beta(x)$, plus constant-$\alpha$ sanity | algebraic identity (Stueckelberg-wrap construction) | $1.78\times 10^{-15}$ (max over 4 sub-checks) | F42-Y13; `test_hypercharge_extension.py` (2026-05-27 - 09:00) |
| 43 | F43-PA.2 — 2D gluon rotation step preserves $\Sigma_a(\|E^a\|^2 + \|B^a\|^2)$ over 20 ticks (per-component F26 cos/sin rotation in $k$-space, applied to 8 octet components) | identity | $2.0\times 10^{-15}$ relative | F43-PA.2; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 44 | F43-PA.3 — BCC gluon rotation step preserves $\Sigma_a(\|E^a\|^2 + \|B^a\|^2)$ over 10 ticks (chiral $\Omega^\pm$ branch propagation per $a$, 8 octet components) | identity | $2.6\times 10^{-15}$ relative | F43-PA.3; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 45 | F43-PB.5 — 2D SU(3) self-coupling step preserves link unitarity $\|U U^\dagger - I\|_\infty$ over 5 ticks of $\delta U = \exp(i \, dt \, g f^{abc} W^b G^c \, T^a) \cdot U$ — Gell-Mann generator exponentiation is in SU(3) by construction | $UU^\dagger = I$ | $5.3\times 10^{-15}$ | F43-PB.5; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 46 | F43-PB.6 — BCC SU(3) self-coupling step preserves link unitarity over 5 ticks (composite-link Wilson plaquette, 3 planes) | $UU^\dagger = I$ | $7.1\times 10^{-15}$ | F43-PB.6; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 47 | F43-PD.4 — Free-gluon BCC dispersion $\omega(k) = \Omega^+(k) = 2\omega_+(k/2)$ per $a$-component, verified by 50-tick spectral closed-form $C_n(k) = C_0(k)\,e^{-i\Omega^+(k) n}$ on a $L=12$ BCC lattice | rel. err on significant modes | $1.7\times 10^{-13}$ | F43-PD.4; `test_FG7_gluon_dynamics.py` (2026-05-28 - 01:30) |
| 48 | F46-P3 — Time-evolved Dirac eigenstate via `dirac_step_2d_splitstep` reproduces the spherical Pythagorean identity-predicted $\Omega$ for 36 $(\mathbf k, m)$ modes over 25 steps; phase residual extracted as $\|\arg(\langle\psi_0\|\psi_N\rangle\,e^{+iN\Omega_\text{pred}})\|/N$ | $\Omega_\text{num} = \Omega_\text{pred}$ per tick | $6.23\times 10^{-16}$ (max) | F46-P3; `test_F46_pythagorean_mass.py` (2026-05-28 - 22:50) |
| 49 | F46-P5 — Photon limit $m = 0$: $\Omega_\text{Dirac}(\mathbf k, 0) = \Omega_\text{kin}(\mathbf k)$ on 2D (closed form, 60 random $\mathbf k$) and BCC (eigenvalues of $D^{BCC}_k$, 60 random $\mathbf k$) | identity | $2.78\times 10^{-16}$ (2D) / $9.44\times 10^{-16}$ (BCC) | F46-P5; `test_F46_pythagorean_mass.py` (2026-05-28 - 22:50) |
| 50 | F46-P7 — Continuum-limit log-log slope of the Pythagorean residual $\|\Omega^2 - m^2 - \omega_\text{kin}^2\|$ vs scale $s$ across 6 decades — confirms the predicted 4th-order lattice correction $\Omega^2 - m^2 - \omega_\text{kin}^2 = -\tfrac{1}{12}(m^4 + \omega_\text{kin}^4 - 6m^2\omega_\text{kin}^2) + O(s^6)$ | slope $= 4$ | $4.0055$ | F46-P7; `test_F46_pythagorean_mass.py` (2026-05-28 - 22:50) |
| 54 | F54-CC6 — $d\to u+W^-$ emission: the W$^-$ component of the current-sourced step equals $(g/\sqrt2)J^+_\text{quark}\,dt$ with $J^+ = u_L^* d_L$ — the charged $W^-=(W^1+iW^2)/\sqrt2$ is sourced by the raising quark current exactly | $\Delta E(W^-) = (g/\sqrt2)J^+ dt$ | $9.2\times 10^{-16}$ | F54-CC6; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 55 | F54-CC7 — Proca W$^-$ dispersion $\omega^2 = m_W^2 + \Omega_\text{even}^2(k)$ across 3 masses $\{0,0.3,0.6\}$ × 3 isospin components over 30 ticks (closed-form $C_n = C_0 e^{-i\omega_\text{eff} n}$) — the charged W inherits the F36 massive rotation law | rel. err on significant modes | $3.1\times 10^{-13}$ | F54-CC7; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 51 | F53-P5a — CP-phase $\theta$ pure gauge: eigenphases of the one-tick complex-mass Dirac operator are $\theta$-independent over $\theta\in\{0,\pi/3,\pi/2,2,\pi\}$ and 4 momenta, per species ($\theta$-phases cancel: $(im\,e^{+i\theta})(im\,e^{-i\theta})=-m^2$) | $\Delta(\text{eigenphase})=0$ | $3.33\times 10^{-16}$ | F53-P5a; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 52 | F53-P5b — Bit-for-bit chiral gauge removal: rephasing $\chi\to e^{+i\theta}\chi$ maps the $\theta$ mass-step onto the $\theta=0$ mass-step exactly, per species | $\Delta\psi=0$ | $9.0\times 10^{-16}$ | F53-P5b; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 53 | F53-P6 — CPT per species (numerical): charge-conjugated rest packet propagates at identical $\omega$ over 300 ticks ($\nu/e/u/d$), and $\lVert C\psi\rVert^2=\lVert\psi\rVert^2$ | $\lvert\Delta\omega\rvert/\omega=0$; norm $\Delta=0$ | $0.0$ | F53-P6; `test_FG9_C_CP_per_species.py` (2026-05-29 - 21:10) |
| 56 | F58-Q0 — Weak equivalence principle in the clock-rate channel: the fractional clock-rate deficit $1-\sqrt A$ is mass-independent (the lapse $\sqrt A$ multiplies $\arcsin m$ as a common factor), tested over $m\in[0.01,0.9]$ × 4 lapse values — the prerequisite for a single coupling $G$ between clock slowing and rest-mass density | spread over $m$ = 0 | $2.2\times 10^{-16}$ | F58-Q0; `test_F58_clockrate_coupling_derivation.py` (2026-05-30 - 13:40) |
| 57 | F58-Q3a — The F25/F26 lock: clock-rate gradient stiffness and the light-cone speed $c_\text{lat}$ both descend from one neighbour-hopping amplitude $J$, so $\text{stiffness}/c_\text{lat}^2$ is hopping-independent over $J\in\{0.5,1,2,4\}$ — hence $1/G\propto c_\text{lat}^2\propto\sqrt d$ | $\text{stiffness}/c_\text{lat}^2=$ const | $1.1\times 10^{-16}$ | F58-Q3a; `test_F58_clockrate_coupling_derivation.py` (2026-05-30 - 13:40) |
| 58 | F62-D3a — Norm conservation under linearized backreaction: a self-gravitating Dirac packet sourcing its own metric ($\nabla^2\Phi=4\pi G\rho$, refreshed) conserves total norm because each Strang tick is exactly unitary regardless of the (evolving) metric | $\lvert\Delta\lVert\Psi\rVert^2\rvert/\lVert\Psi\rVert^2=0$ | $2.5\times10^{-15}$ over 60 ticks | F62-D3a; `test_F62_dirac_gravity_fork.py` (2026-05-30 - 16:10) |
| 59 | F64-D-EM-D3a — Norm conservation under a self-sourced **dielectric** metric: a self-gravitating packet co-evolved with the dielectric $K(x)$ it generates ($A=1/K,B=K$) conserves norm (each tick exactly unitary), the dielectric counterpart of #58 | $\lvert\Delta\lVert\Psi\rVert^2\rvert/\lVert\Psi\rVert^2=0$ | $7.5\times10^{-16}$ over 60 ticks | F64-D-EM-D3a; `test_F64_em_connection.py` (2026-05-31 - 16:00) |
| 60 | F75-T4 — Schur degeneracies of an $O_h$-invariant Hermitian mass operator on the shell: a group-averaged random Hermitian operator commutes with all 48 elements and has eigenvalue degeneracy multiset $[1,1,3,3]$ = irrep dims ⇒ max symmetry-protected degeneracy $=3$ | commutator $=0$; degeneracies $[1,1,3,3]$ | $4.4\times10^{-16}$ (commutator) | F75-T4; `test_F75_three_generations_irrep.py` (2026-06-01 - 20:08) |
| 61 | F77-C1 — NJL Goldstone theorem: in the chiral limit the pion-pole condition $1-2G\Pi_\text{PS}(0)=0$ is *identically* the gap equation, so $m_\pi=0$ as the self-consistent constituent mass forms (one coupling, no fitting) | $1-2G\Pi_\text{PS}(0)=0$ | $2.3\times10^{-14}$ | F77-C1; `test_F77_njl_gap_rpa.py` (2026-06-01 - 20:05) |
| 62 | F77-C2 — NJL mean-field theorem $m_\sigma=2m_c$: the scalar RPA pole sits exactly at $q^2=4M^2$ (residual of $1-2G\Pi_S(4M^2)$), recovering the F73/F74 ceiling as an *output* of the same coupling that generates $m_c$ | $1-2G\Pi_S(4M^2)=0$ | $2.3\times10^{-14}$ | F77-C2; `test_F77_njl_gap_rpa.py` (2026-06-01 - 20:05) |
| 63 | F83 — Lattice-mass-map round-trip $a\to m_\text{lat}=\sin(a/(\sqrt d\bar\lambda_C))\to a=\sqrt d\arcsin(m_\text{lat})\bar\lambda_C$ over all 9 charged fermions (inversion of identity #172) | bit-for-bit inverse | $2.48\times10^{-16}$ (max rel) | F83-T1; `test_F83_fix_lattice_spacing.py` (2026-06-02 - 20:05) |
| 64 | F103-P3-G — the pion as a real-space dynamical bound state: the relative-coordinate q̄q contact bound state solved two ways on the F74 engine (secular Koster-Slater root vs dense diagonalisation, $L=12$, $g=8t>g_c=3.957t$) agree on the ground-state energy | secular root $==$ dense eigh | $1.3\times10^{-15}$ | F103-P3-G; `test_P3_pion.py` (2026-06-06 - 06:42) |
| 65 | F122-P2-S1 — dynamical baryon ground state solved two independent ways (scipy generalised `eigh(H,S)` vs hand-rolled Cholesky reduction $L^{-1}HL^{-T}$) agree | scipy $==$ Cholesky | $4.5\times10^{-12}$ | F122; `test_P2_baryon_bound_state.py` (2026-06-09 - 16:54) |
| 66 | F130-T2num — the leading even-law LIV operator reproduces F30: along the body diagonal $g_2=-1/162$ in the $\Omega$-form, i.e. $\delta v_g/c=-k^2/54$ ($E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$); extracted by polynomial dispersion fit | $g_2=-1/162$ | $<10^{-6}$ | F130-T2num; `test_F130_blockspin_gauge_gravity.py` (2026-06-10) |
| 67 | F130-T3c — block-spin preserves the F91 even/chiral propagator class: $[R_b, R(\Omega)]=0$ (a real helicity-blind block kernel commutes with the even 2×2 rotation, so it cannot mix branch structure) | commutator $=0$ | $2.9\times10^{-14}$ ($b\in\{2,3,4\}$) | F130-T3c; same script (2026-06-10) |
| 68 | F131-B (Phase-2) — RG commutes with binding: a coarse-grained ($b{=}2$, 8× fewer cells) harmonic bound state reproduces the fine spectrum — ground+first-shell levels match $<1\%$, the $O_h$ first-excited triplet stays 3-fold degenerate (spread $<10^{-6}$), and the block-averaged fine ground state matches the coarse ground state | overlap $\to1$ | $0.99986$ overlap; $0.2\%$ $E_0$ | F131-B1/B2/B3; `test_F131_blockspin_bound_state.py` (2026-06-11) |
| 69 | F131-B4/B5 (Phase-2, quantitative) — both fine and coarse harmonic energies converge to the analytic continuum $E_N=\omega(N+\tfrac32)$ ($<1\%$ ground, $<2\%$ first shell); the softened-Coulomb (F125 hydrogen long-wavelength) ground state $E_0<0$ is reproduced at $b{=}2$ to $0.45\%$ (overlap $0.994$). The coarse error is the irrelevant $O((ka)^2)$ operator — shrinks as the state is more IR, grows $\sim b^2$ | $E\to\omega(N+\tfrac32)$ | $<1\%$ (harmonic), $0.45\%$ (Coulomb) | F131-B4/B5; same script (2026-06-11) |
| 70 | F132-P (Phase-2, dynamical) — the pion (F74/F103) CONTACT coupling is RG-relevant: under $R_b$ it RUNS ($g{=}4\!\to\!1.01$ at $b{=}2$, $\to0.45$ at $b{=}3$) to hold $E_b$ fixed, the flow predicted by the Watson threshold ratio $g/g_c$ ($g_c{=}2t/W_3$) to a few %; with the run coupling the bound-state wavefunction (overlap $\ge0.97$) and rms size ($<2\%$) are reproduced on up to 27× fewer cells | $g_\text{coarse}=(g/g_c)\,g_c(t/b^2)$ | pred vs exact $<5\%$; overlap $0.99$ | F132-P; `test_F132_blockspin_dynamical_bound_states.py` (2026-06-11) |
| 71 | F132-D (Phase-2, dynamical) — the deuteron (F104) FINITE-RANGE Yukawa/OBE coupling is RG-irrelevant: held fixed, decimating the radial grid ($h\!\to\!b h$) reproduces the shallow halo $E_b{=}2.224$ MeV to $0.4\%$ ($b{=}2$) / $1.9\%$ ($b{=}4$) and $r_d{=}1.94$ fm to $<1\%$, staying bound throughout; error grows $\sim b^2$ (the irrelevant $O(h^2)$ operator), no running | $E_b,r_d$ reproduced, no run | $0.4\%$ ($b{=}2$) | F132-D; same script (2026-06-11) |
| 72 | F132-B (Phase-2, dynamical) — the baryon (F122) mass is the F130-C1-covariant string scale: the confined three-body ground energy scales as $E_\text{rel}\propto\sigma^{2/3}$ (linear-potential virial, slope $0.6670$ vs $2/3$), confinement-dominated, so carried by the RG-covariant $\sigma$; the ECG engine reproduces the analytic harmonic three-body $E=3\sqrt{3k/m}$ to $0.3\%$ | slope $=2/3$ | $0.6670$; harmonic $0.3\%$ | F132-B; same script (2026-06-11) |
| 73 | F133-E2/E6 (Phase-4 engine) — the block-spin $R_b$ as a first-class CASIM engine op: `Simulation.block_spin` / `Channel.block_spin` reproduce `ca_blockspin.block_average` bit-identically (complex-safe for spinors — keeps the imaginary part the float-casting helper would drop), and the gravity dielectric coarse-grains by the log rule ($\varphi$ averaged, $K=e^{-2\varphi/c^2}$ rebuilt) so $A\!\cdot\!B\equiv1$ is preserved (not the Jensen-gap $K$-average) | $R_b$ engine $=$ `block_average` | bit-identical; $AB{-}1<10^{-12}$ | F133-E2/E6; `test_F133_blockspin_engine.py` (2026-06-11) |
| 74 | F133-E3 (Phase-4 engine) — the renormalised coarse propagator $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$ (`renormalized_even_step`) reduces bit-for-bit to the fine photon step at $b{=}1$ and is dynamically faithful: $[R_b,\text{evolution}]=0$ on band-limited fields (coarse run reproduces the fine IR dynamics), with the $c_\text{lat}$ fixed point ($b\cdot c_\text{coarse}=1/\sqrt3$) | commutator $=0$ | $1.8\times10^{-15}$ ($n{=}8,b{=}2$) | F133-E3; same script (2026-06-11) |
| 75 | F134-A/B (Phase-4 chiral) — the block-aware renormalised steps for the CHIRAL (W± RS) and PER-BRANCH (Weyl) classes reduce bit-for-bit to the audited fine kernels at $b{=}1$ (`w_propagation_step_chiral`, `weyl_step_3d_bcc`; residual $0.0$) and are dynamically faithful: $[R_b,\text{evolution}]=0$ on band-limited fields (chiral $1.5\times10^{-15}$, Weyl $1.3\times10^{-15}$); coarse steps stay unitary ($<10^{-13}$/100 ticks) | $b{=}1$ reduction; commutator $=0$ | $0.0$ / $1.5\times10^{-15}$ | F134-A/B; `test_F134_phase4_completion.py` (2026-06-11) |
| 76 | F134-D (Phase-4 chiral core) — the hand-rolled chiral linear-algebra core (`casim.lattice.chiral_core`, explicit real/imag arithmetic via `cmul`/`su2_apply`, no `np.linalg` on chiral matrices — CLAUDE.md) reproduces the audited Weyl $U^\pm$ and W± RS kernels bit-for-bit, and matches the block-renormalised steps; registered + dispatched through the `backend.chiral_transform` seam | hand-rolled $=$ kernel | $9.9\times10^{-16}$ (Weyl), $1.3\times10^{-15}$ (RS) | F134-D; same script (2026-06-11) |
| 85 | F140-K1/K2 — the coarse-grained baryon element: the $K{=}0$ hyperradial reduction of the F122 three-quark Cornell problem (1-D radial, centrifugal $15/4$, $C_\sigma=16\sqrt2/5\pi$) reproduces the ECG baryon ground energy across $\sigma$ to $<0.05\%$ with ONE $\sigma$-independent adiabatic coefficient $\kappa{=}2.0005$ (EFT match), confinement-dominated $E_\text{rel}\propto\sigma^{2/3}$ (slope $0.6666$) | $E_\text{rel}\!=\!E_\text{ECG}$; slope $2/3$ | $<0.05\%$; $0.6666$ | F140-K1/K2; `test_F140_coarse_grained_baryon.py` (2026-06-11) |
| 86 | F140-K3/K4 — the baryon element coarse-grains under $R_b$ (hyperradial grid decimation $h\!\to\!bh$): the proton mass + rms hyperradius are reproduced on $b\times$ fewer cells ($E_\text{rel}$ rel-err $0.01\%$ $b{=}2$ → $0.13\%$ $b{=}8$, amplitude overlap $0.997$–$1.0$, stays confined), error $\sim b^2$ (irrelevant $O(h^2)$); in lattice units the confining $\hat\sigma\!\to\!b\hat\sigma$ is the F130-C1 relevant operator ($\lambda_\sigma=b$) | mass reproduced; $\lambda_\sigma=b$ | overlap $0.99994$ ($b{=}2$) | F140-K3/K4; same script (2026-06-11) |
| 75 | F129-A (Phase-1 free photon) — block map $\Omega_\text{coarse}(\kappa)=b\,\Omega(\kappa/b)$ gives coefficient eigenvalue $[\kappa^n]=a_n b^{1-n}$: $c_\text{lat}$ ($n{=}1$) invariant (RG fixed point), LIV operators ($n\!\ge\!2$) irrelevant ($\lambda_n=b^{1-n}$); even-law body-diagonal $a_3=-1/(162\sqrt3)$ matches F30 | $[\kappa^n]=a_n b^{1-n}$ symbolic | Tier-1 exact (sympy, symbolic $b$) | F129-A; `test_F129_blockspin_free_photon.py` (2026-06-11) |
| 76 | F129-RS (Phase-1 free photon, simulation) — the RG commutes with the actual even-law propagator: $R_b\!\circ\!\text{evolve}_\text{fine}^{bN}=\text{evolve}_\text{coarse}^{N}\!\circ\!R_b$ on band-limited $(\mathbf E,\mathbf B)$ fields (coarse run on $b^d$× fewer cells reproduces the fine run), and a planted on-axis mode's measured $c_\text{lat}=\Omega/\lvert k\rvert$ agrees fine-vs-coarse | $R_b$ commutes; $c$ invariant | $5.5\times10^{-15}$ ($b{=}2$); $c$ to $1\times10^{-14}$ | F129-RS/V; same script (2026-06-11) |
| 77 | F135-RT1 (Phase-2 matter, real-time) — the RG commutes with genuine real-time dynamics: a moving, spreading band-limited massive Dirac packet satisfies $R_b\!\circ\!\text{evolve}_\text{fine}^{bN}=\text{evolve}_\text{coarse}^{N}\!\circ\!R_b$ (coarse rule $\Omega_\text{coarse}=b\,\omega(\cdot/b)$) at EVERY coarse tick; velocity (0.533 vs 0.532) and rms spreading reproduced | $R_b$ commutes (whole trajectory) | $1.4\times10^{-15}$ ($b{=}2$), $2.5\times10^{-15}$ ($b{=}3$) | F135-RT1/2/3; `test_F135_blockspin_wavepacket_realtime.py` (2026-06-11) |
| 78 | F135-RT4 (Phase-2 matter) — MASS is the relevant operator: the rest-gap $\omega(0)=\arcsin m$ scales by $b$ under $R_b$ (eigenvalue $b$, like the F130-C1 string tension), $m\to\sin(b\arcsin m)$, physical Compton wavelength $\lambda_C=a/\arcsin m$ invariant; completes the RG class table (mass/$\sigma$ relevant, $c$ marginal, LIV irrelevant) | gap eigenvalue $=b$; $\lambda_C^\text{phys}$ invariant | $<10^{-12}$ ($b{=}2,3,4$) | F135-RT4; same script (2026-06-11) |
| 87 | F406: 3-generation BCC Dirac sea with matrix mass $M=Y^2$ is generation-covariant — identical at the $E_g$-diagonal, the three [111] circulants and random orientations; equals 4× F95 per-axis sea (2026-09-24 - 15:20) | $\Delta E_\text{sea}=0$ | $\le2\times10^{-15}$ | L=6 grid | `F406-lepton-frame-fork` leg K2 |
| 88 | F408 — BCC zero-point moment $I_\text{cc}=3\sqrt3\pi/4$ on the even `sakharov_moments` grid ($n=64$); numeric content-consistent ratio; canonical cell $=$ content ($\sum\eta=4$) | $3\sqrt3\pi/4$; $24\sqrt3\pi$; $(a/\ell_P)^2=8\pi\sqrt3$ | $2.7\times10^{-15}$ / $8.7\times10^{-16}$ / $1.1\times10^{-16}$ | $n=64$ (even $\Rightarrow$ node-wise pairing) | `F408-cc-sign-split` leg S2-ratio-closed-form |

**Pattern (Finding 5):** norm drift per FFT round-trip is ~1 ulp of complex128. The codebase is already at native double precision; upgrading to long-double would shave ~1 decimal of error per step at significant speed cost.

---

## Tier 3 — Quantitative matches (within declared tolerance) (curated)

| # | Construct | Predicted form | Measured | Tolerance / threshold | Source |
|---|---|---|---|---|---|
| 1 | C1 Snell refraction (Strang) | exit angle from Snell's law | 0.51° error | qualitative pass | C1; `ca_curved.py` |
| 2 | C1 Cayley refraction at $\|k\|\approx 0.5$ | exit angle from Snell's law | 5.4° error | lattice-dispersion limited | Phase F3 update; `ca_curved.py` |
| 3 | D1 zitterbewegung at $2\arcsin(m)$, $m=0.5$ | $\pi/3 = 1.04720$ | $1.04877$ | 0.15% (FFT-bin-limited) | Finding 9 closeout; `ca_dirac.py` |
| 4 | Group velocity $v_g = c\hat k$ (B1) | $\|v_g\|/c = 1$ | $0.9995$ – $0.9999$ at $L=640$ | <0.05% at the 10× lattice | Finding 6 / B1; `run_phase_tests.py` |
| 5 | Composite-photon dispersion $\Omega_\gamma = \|k\|/\sqrt 3$ (BCC) | $\|k\|/\sqrt 3$ | 0.21% at $k = 0.05$ | published-target precision | L3; `ca_maxwell.py` |
| 6 | F2 Higgs radial dispersion $\omega = \sqrt{k^2 + 2\mu^2}$ | $\sqrt{k^2 + 2\mu^2}$ | max res $1.0 \times 10^{-3}$ | O(dt²) Verlet-limited | F2; `ca_higgs.py` |
| 7 | EMQG static Poisson rel err | $\nabla^2\phi = 4\pi G\rho$ | 2.75% at $L=64$ → 1.39% at $L=640$ | qualitative | L4.a; `ca_emqg.py` |
| 8 | 3-D Newtonian lensing linear-in-M ratio | $\Delta(2M)/\Delta(M) = 2$ | $1.99647$ at $L=64$ | 0.35% (Newtonian); threshold 10% | Finding 8; `ca_emqg.py` |
| 9 | Klein paradox plateau location (Paper 4 Fig. 3) | reflection plateau in $\varphi \in [m, 2-2m]$ shifted | max $R = 0.91$ in $\varphi \in [1.4, 2.0]$ | qualitative shape match | V2; `run_qca_verifications.py` |
| 10 | Frequency-dependent $c$ at $\|k\|=0.5$ along $(1,1)$ | $\Delta c/c$ per Paper 4 Eq. 23 | $-1.1\%$ | qualitative | L2; `ca_core_exact.py` |
| 11 | Frequency-dependent $c$ off-axis (V5) | sign and magnitude per Paper 4 | dev at $\|k\|=1.0$ = $-6.7\%$ | qualitative | V5; `run_qca_verifications.py` |
| 12 | BCC vs simple-cubic regression (V6) | grow from 0 toward Paper 1 unique-QCA | dev grows 0 → 7.5% across range | qualitative | V6; `run_qca_verifications.py` |
| 13 | DSR Lorentz-deformation signature (V8) | standard-Lorentz residual $\sim k^2$ | qualitative match | qualitative | V8; `run_qca_verifications.py` |
| 14 | F3 symplectic-Yukawa energy drift (200 steps, dt=0.5) | drift bounded $O(dt^2)$ | 3 ppm | qualitative | F3 follow-up; `ca_unified.py` |
| 15 | GR-1 absolute light deflection coefficient $K = \Delta\theta\cdot b\cdot c^2/(GM)$ — **open-BC kernel** | $K = 4$ (Einstein) | $|K| = 3.881$ (truncation-corrected) at $L=192$, $b=8$ (linear-in-$M$ to machine zero) | **3.0% off Einstein — PASS at 5% gate**; PBC version was 12.5% off | Finding 14.15 / GR-1; `poisson_open.py` + `tests-priority/test_01b_GR1_openBC.py` |
| 16 | GR-3 phase-tick redshift ratio vs Paper 6 ansatz $\Delta\nu/\nu = 2\Delta\phi/c^2$ | match Paper 6 form | $-0.998$ (signed) across 4 (near, far) pairs | 0.2% (matches the *ansatz*; falsifies vs measured GR by factor 2) | Finding 14.5 / GR-3; `tests-priority/test_04_GR3_pound_rebka.py` |
| 17 | GR-2 absolute Shapiro $\Delta t_\text{lat}/\Delta t_\text{GR}$ — **open-BC kernel** | $= 1$ (GR closed form) | $1.00058$ at $L=192$, $b=8$ (monotonic in $L$: $1.0062, 1.0029, 1.0016, 1.0010, 1.0006$) | **0.06% off — PASS at 0.1% gate; pins PPN $\gamma=1$**; PBC version was 38% off | Finding 14.16 / GR-2; `poisson_open.py` + `tests-priority/test_05b_GR2_openBC.py` |
| 18 | QG-2 $E_\text{LV}$ from BCC dispersion (diagonal $(1,1,1)$) | $\ge 1.2\times 10^{19}$ GeV (Fermi GRB) | $1.87\times 10^{20}$ GeV at $a = 1.616\times 10^{-35}$ m | $\sim 10\times$ Fermi bound — PASS up to $a \le 1.5\times 10^{-34}$ m | Finding 14.7 / QG-2; `tests-priority/test_06_QG2_planck_LV.py` |
| 19 | QFT-5 3-flavour PMNS atmospheric peak location | $\sim 495$ km/GeV | $553$ km/GeV (lattice 3-flavour with $\theta_{13}=8.6°$, solar mixing) | 11.85% off 2-flavour analytic; consistent with 3-flavour multi-$\Delta m^2$ interference | Finding 14.8 / QFT-5; `tests-priority/test_07_QFT5_neutrino.py` |
| 20 | QM-2 sub-threshold tunneling at $V_0 = 0.15$, width 6, $m=0.1$, $k_x=0.2$ | match Schrödinger $T = (1 + V_0^2\sinh^2(\kappa a)/(4E(V_0-E)))^{-1}$ | $T_\text{lat}/T_\text{QM} = 0.982$ | 1.8% (in-window sweet spot; Klein paradox dominates broader scan) | Finding 14.11 / QM-2; `tests-priority/test_08_QM2_tunneling.py` |
| 21 | GR-4 Mercury perihelion at $v^2/c^2 = 5.6\times 10^{-3}$ | $\Delta\omega = 6\pi GM/(a(1-e^2)c^2)$ | $0.0612$ rad/orbit vs analytic $0.0621$; per-orbit std $1.6\times 10^{-5}$ | 1.5% (1PN truncation, scales as $v^2/c^2$ to expected) | Finding 14.12 / GR-4; `tests-priority/test_09_GR4_mercury.py` |
| 22 | QG-4 U(1) charge conservation at $L=256$, 1000 steps | drift at FFT floor | $|\Delta Q|/Q = 1.83\times 10^{-13}$ (linear in step at $1.8\times 10^{-16}$/step) | FFT-floor (Finding 5) limited; strict 1e-13 gate missed by 1.8× | Finding 14.13 / QG-4; `tests-priority/test_10_QG4_charge.py` |
| 23 | GR-3 redshift after fork fix — ratio$_{GR} = (\Delta\nu/\nu)_\text{lat}/(\Delta\phi/c^2)$ | $= 1$ (measured GR) | Fork A $1.0001$, Fork B $1.0002$, Fork C $0.9998$ (baseline $1.9991$) | $\sim 10^{-4}$ band across 4 (near,far) pairs — **all 3 forks resolve the factor-2** | Finding 16 / GR-3; `forks/gr3_fork_harness.py` |
| 24 | GR-4 Mercury fork discriminator — $\Delta\omega_\text{lat}/\Delta\omega_\text{baseline}$ | A,B $=1$; C $=0.5$ | A $1.0000$, B $1.0000$, C $0.4995$ ($\alpha_A=\alpha_B$: 1,1,0.5) | relative; per-half-orbit ×2 convention. C halves the advance (falsifier) | Finding 16 / GR-4; `forks/gr3_fork_harness.py` |
| 25 | F37.3 coefficient — $\Delta\Omega(k)\approx c\,k^2$ along $(1,1,1)$: least-squares fit of coefficient $c$ vs F30 exact value $-\sqrt3/27$ | $c = -\sqrt3/27 \approx -0.064150$ | $c_\text{meas} = -0.064175$ | **relative error $3.95\times10^{-4}$ — PASS at $5\times10^{-4}$ gate** (residual is higher-order $k^3$ correction, not bias) | F37; `test_F37_delta_omega.py` (2026-05-24) |
| 26 | F40-Q4 — Up/down/strange mass splitting under `step_strong_2d_complex_mass` follows $(m_f/m_u)^2$ in the linear regime: $r_d/r_u = 3.96$ vs $4$; $r_s/r_u = 15.22$ vs $16$ | ratios $\propto (m/m)^2$ in $mt\!\ll\!1$ | $\sim 1\%$ off from the $\sin^2(mt)\to(mt)^2$ truncation | F40-Q4; `test_FG2_quark_complex_mass.py` (2026-05-26 - 16:30) |
| 27 | F54-CC10 — End-to-end $d\to u+W^-\to u+e^-+\bar\nu_e$ pipeline: quark current sources a $W^-$ at site A ($\lvert W^-\rvert_A = 0.36$), which propagates causally (Proca, 24 ticks) to a distant site B — zero signal at B on emission ($1.6\times10^{-13}$), finite after propagation ($2.9\times10^{-3}$) — while global $\Delta Q=\Delta B=\Delta L=\Delta(B-L)=0$ | causal arrival + exact global charge balance | A→B signal causal; charges exact $0$ | F53-CC10; `test_FG8_beta_decay.py` (2026-05-29 - 20:47) |
| 28 | F76-C3 — Charged-lepton Koide ratio $Q=\sum m/(\sum\sqrt m)^2$ vs the cubic-equipartition value $2/3$ | $Q=2/3$ | $Q=0.6666605$, $\lvert Q-2/3\rvert=6.2\times10^{-6}$ ($0.91\sigma$ on $m_\tau$); equipartition angle $44.99974^\circ$ | within $1\sigma$ of $2/3$ — structural identity (#159), value is empirical | F76-C3/C4; `test_F76_generation_hierarchy.py` (2026-06-01 - 20:41) |
| 29 | F76-C5 — $m_\tau$ predicted from $(m_e,m_\mu)$ via the cubic-vector ($Q=2/3$) consistency condition | $m_\tau^\text{PDG}=1776.86\pm0.12$ MeV | $m_\tau^\text{pred}=1776.97$ MeV (rel. err $6.1\times10^{-5}$); $m_e$ from $(m_\mu,m_\tau)$ to $7\times10^{-4}$ | prediction tighter than input precision, within $\sim1\sigma$ | F76-C5; `test_F76_generation_hierarchy.py` (2026-06-01 - 20:41) |
| 30 | F76-C2 — Crystal field *linear in $m$* ruled out as the hierarchy source: traceless fit needs split/mean $>1$ | perturbative split $\ll1$ | $\max\lvert\Delta\rvert/\overline m=1.83$ (non-perturbative) | negative result — selects $\sqrt m$ (not $m$) as the $T_{1u}$ variable | F76-C2; `test_F76_generation_hierarchy.py` (2026-06-01 - 20:41) |
| 31 | F78-A2 — The data select the bilinear ($m=y^2$) variable: the participation ratio $1/Q(s)=(\sum m^s)^2/\sum m^{2s}$ hits the clean rational $3/2$ only at $s=\tfrac12$ | $1/Q(\tfrac12)=3/2$ | $1.500014$ at $s{=}\tfrac12$ vs $1.834,1.119$ at $s{=}\tfrac13,1$ | supports the Cooper-pair origin of $\sqrt m$ (m quadratic in amplitude) | F78-A2; `test_F78_koide_amplitude_pairing.py` (2026-06-01 - 21:14) |
| 32 | F78-B3 — A flavour-symmetric (democratic) NJL gap drives all three masses to a common value ⇒ degenerate, $Q\to\tfrac13$ — symmetric cube dynamics cannot make the hierarchy or reach $Q=\tfrac23$ | degenerate solution | relative spread $<10^{-8}$, $Q=0.33333$ | honest negative: equipartition ($\sqrt2$) is a large explicit breaking, not from symmetric dynamics | F78-B3; `test_F78_koide_amplitude_pairing.py` (2026-06-01 - 21:14) |
| 33 | F80-D4 — EM selection rule across sectors: only the clean EM-coupled, colour-free charged leptons sit at the $45°$ critical point $Q=\tfrac23$; up-type quarks $0.85$, down-type $0.73$ (QCD-contaminated, off and unequal), neutrinos (neutral) unpinned ($Q=0.34$–$0.59$, ordering-dependent) | only charged leptons at $\tfrac23$ | $Q_\ell=0.6667$ vs $Q_u=0.85,Q_d=0.73,Q_\nu$ swings | electric charge is the selector (perturbative-EM magnitude residual logged, D5) | F80-D4; `test_F80_em_saturation_45deg.py` (2026-06-02 - 11:57) |
| 34 | F81-E2 — The measured charged-lepton $Q$ selects the integer constituent number $N=2$ in $Q_N=1/(3\cos^2(\pi/2N))$: best-fit $N=2$ with residual $6\times10^{-6}$ ($N=3$ off by $0.22$) — $Q=2/3$ reads off the two-constituent (Cooper-pair) structure | best integer $N=2$ | $\lvert Q_\text{obs}-Q_2\rvert=6\times10^{-6}$ | constituent-number readout from mass ratios alone | F81-E2; `test_F81_45deg_pair_saturation.py` (2026-06-02 - 12:15) |
| 35 | F82-G4 — $Q$ is monotonic in the composite mass / binding depth ($m_H{=}0\to Q{=}1/3$ democratic; $m_H{=}1\to Q{=}2/3$ max bound), so clean two-body pairs satisfy $Q\le2/3$: charged leptons saturate at $2/3$, while quark $Q_\text{up}=0.85,Q_\text{down}=0.73>2/3$ lie outside the clean-pair band (QCD-confined, not clean two-body pairs) | $Q\in[\tfrac13,\tfrac23]$ for clean pairs | leptons $0.667$; quarks $0.85,0.73$ outside | binding-degree ↔ sector ↔ $Q$ | F82-G4; `test_F82_saturation_mass_peak.py` (2026-06-02 - 19:38) |
| 36 | F84-H4 — The observed $\lvert Q-\tfrac23\rvert=6\times10^{-6}$ (charged leptons, $0.91\sigma$, measurement-limited) bounds the residual democratic ($S_3$) stiffness to $\kappa/\lambda\lesssim2\times10^{-5}$ via $\phi^*(\kappa)$ near $45°$ — the orthorhombic break is essentially complete, $Q=2/3$ robust not tuned | $\kappa/\lambda\lesssim2\times10^{-5}$ | $\epsilon\approx4.6\times10^{-6}$ rad | break essentially complete | F84-H4; `test_F84_flatness_from_orthorhombic_break.py` (2026-06-03 - 00:28) |
| 37 | F112 — Newton's constant from the canonical cell: $G=a^2c^3/(8\pi\sqrt3\hbar)$ at $a=6.59782\,\ell_P$ (no gravitational input) | $G_\text{CODATA}=6.67430\times10^{-11}$ | $G_\text{pred}=6.674300\times10^{-11}$, rel $3.0\times10^{-8}$ | the headline SI prediction; residual = F79 $a/\ell_P$ vs CODATA $\ell_P$ | F112; `test_F112_si_predictions.py` (2026-06-08 - 14:05) |
| 38 | F112 — Absolute solar light deflection through the predicted $G$: $\Delta\theta=4G_\text{pred}M_\odot/(R_\odot c^2)$ | $1.751190''$ (GR/VLBI) | $1.751190''$, rel $3.0\times10^{-8}$ | inherits the $G$ residual; VLBI/Cassini confirm $\gamma=1$ at $10^{-4}/10^{-5}$ | F112; `test_F112_si_predictions.py` (2026-06-08 - 14:05) |
| 39 | F122-P2-S5 — confinement dominance of the dynamical baryon (the F97 statement made dynamical): in the current-quark limit ($m_q=0.01\sqrt\sigma$) the quark-mass sum is a negligible fraction of the three-body bound-state mass | quark sum $\ll m_p$ | $0.11\%$ of $M$ (cf. F97/PDG $0.96\%$) | the mass is the confining string, not the constituents | F122-P2-S5; `test_P2_baryon_bound_state.py` (2026-06-09 - 16:54) |
| 40 | F122-P2-S8 — neutron–proton mass splitting sign and magnitude: $(m_d-m_u)$ strong term beating the proton's larger EM self-energy | $m_n-m_p>0$, $\approx+1.293$ MeV | $+1.51$ MeV (strong $+2.51$, EM $-1.00$); sign positive | sign is the real test of the F40 d–u ratio — passes | F122-P2-S8; `test_P2_baryon_bound_state.py` (2026-06-09 - 16:54) |
| 41 | F123-P6-H2 — the nucleon mass from a single QCD anchor: with $f_\pi=92.07$ MeV fixing the strong scale, the NJL constituent mass $m_c=309.5$ MeV gives $m_p\simeq3m_c$ | $m_p^\text{PDG}=938.27$ MeV | $928.5$ MeV ($-1.05\%$) | F97 made quantitative — nucleon mass is the dynamical constituent mass, not the current-quark sum; resolves the F122 NR overshoot | F123-P6-H2; `test_P6_si_scale.py` (2026-06-09 - 17:40) |
| 42 | F123-P6 — the light-meson sector in absolute MeV on the one $f_\pi$ anchor: $m_\pi=139.7$ (PDG 138.04), $m_\rho=781.2$ (775.26, KSRF/Tier-3), $\langle\bar qq\rangle^{1/3}=-247.7$ ($\sim-272$) | PDG light-hadron set | all within a few % on one scale | only $f_\pi$ is dimensionful; couplings $\{G\Lambda^2,m_0/\Lambda\}$ are dimensionless shape | F123-P6; `test_P6_si_scale.py` (2026-06-09 - 17:40) |
| 43 | F124 — the ratio of the two QCD calibrations $\sqrt\sigma/f_\pi=(\Lambda/f_\pi)(\sqrt\sigma/\Lambda)$: exact chiral factor $\Lambda/f_\pi=7.04$ (NJL/Pagels–Stokar) × confinement factor from the F86/F88 condensate ($\sigma=2\pi v^2$, $v=0.713$) at the BZ-edge cutoff. **[F235, 2026-07-02]** the $+12\%$ residual does **not** close to $<5\%$ from any principled BCC Brillouin-zone cutoff (matching $4.56$ needs $\Lambda_\text{eff}=2.758/a$, below even the axis edge $\pi/a$) — it is a genuine scale-setting object = the same one-loop constant $d_1$ that E3 (F233) and Q2 (F154/F144-A4) reduce to; **Q1=Q2=E3 (one number $d_1$)** | $\sqrt\sigma/f_\pi=4.56$ (empirical) | $4.00$ (axis BZ) / $3.23$ (sphere), $+12$–$29\%$; chiral half exact | chiral half exact; open number = the shared $d_1$; bare-rotor route $\approx1$ locates the strong-coupling gap | F124/F235; `test_F124_qcd_scale_ratio.py`, `test_F235_sqrt_sigma_fpi_scale_setting.py` |
| 44 | F125-P5-D — hydrogen ground state from the model's own $m_e$ and the EM coupling $\alpha$ alone: $\mathrm{Ry}=\tfrac12\mu c^2\alpha^2$, full $-\mathrm{Ry}/n^2$ series + Coulomb $\ell$-degeneracy from the tridiagonal radial solver | $-13.5983$ eV (reduced-mass), $a_0=0.052918$ nm | ground $-13.596$ eV; $\mathrm{Ry}$ to $1.1\times10^{-12}$ of CODATA; $a_0=0.052947$ nm | absolute scale, no fit; $\alpha$ the one EM input ($m_e$ a P0 anchor); grid-floor series + SO(4) $\ell$-degeneracy | F125-P5-D/B/C; `test_P5_hydrogen.py` (2026-06-09 - 19:10) |
| 45 | F125-P5-H — Dirac–Coulomb fine structure: $2p_{3/2}{-}2p_{1/2}$ splitting and its $\alpha^4$(abs)/$\alpha^2$(rel) scaling — the defining fine-structure law from the Dirac (not Schrödinger) operator | $\approx10.969$ GHz ($45.2\ \mu$eV) | $10.95$ GHz ($45.28\ \mu$eV), $0.18\%$; slopes $4.0001$/$2.0000$ | prediction once $\alpha$ fixed; Sommerfeld == $O((Z\alpha)^4)$ series ($5\times10^{-10}$) | F125-P5-F/H; `test_P5_hydrogen.py` (2026-06-09 - 19:10) |
| 46 | F125-P5-G — hand-rolled numerical radial-Dirac integrator (RK4 inward+outward Wronskian matching) reproduces the exact Sommerfeld eigenvalues for $1s_{1/2}$, $2p_{1/2}$, $2p_{3/2}$ | $=$ Sommerfeld | $\le1.3\times10^{-6}$ (rel. to binding) | the fine structure is a genuine solve, not just the closed form | F125-P5-G; `test_P5_hydrogen.py` (2026-06-09 - 19:10) |
| 39 | F112 — Even-channel $n{=}2$ LIV scale $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$ at the canonical cell | $>7.0\times10^{11}$ GeV (LHAASO GRB 221009A) | $1.360\times10^{19}$ GeV $=1.11\,E_P$, clears by $1.9\times10^7$ | one-sided falsifier; a future subluminal $n{=}2$ bound $>1.4\times10^{19}$ GeV kills $a_\text{canon}$ | F112; `test_F112_si_predictions.py` (2026-06-08 - 14:05) |
| 40 | F112 — Electroweak mass ratio $m_Z/m_W=2/\sqrt3$ (F45 bare, zero fit parameters) | PDG $1.1346$ | $1.1547$, $+1.77\%$ | bare lattice value, pre-loop/RG; tighter than tree-level SU(5) | F112/F45; `test_F112_si_predictions.py` (2026-06-08 - 14:05) |
| 41 | F114 — Dielectric (exponential-metric) black hole has NO event horizon: $g_{tt}=-e^{-2u}$ has no finite root; throat (min areal radius) $R_\text{min}=e\,GM/c^2$; photon sphere $2\sqrt e\,GM/c^2$; shadow $b_c=2e\,GM/c^2$; throat redshift $1+z=e$ | exact closed forms ($e,\,2\sqrt e,\,2e$) | sympy zero residual | Tier-1 exact; strong-field departure from Schwarzschild (horizon 2, $R_\text{ph}=3$, $b_c=3\sqrt3$) | F114; `test_F114_dielectric_black_hole.py` (2026-06-08 - 15:10) |
| 42 | F114 — Black-hole shadow enlargement vs Schwarzschild: $b_c/b_c^\text{Schw}=2e/3\sqrt3$ | $1.0463$ (exact) | $+4.63\%$; M87\* $41.5\,\mu$as, Sgr A\* $55.7\,\mu$as vs GR $39.7/53.3$ | within current EHT ring precision ($42\pm3$, $52\pm2\,\mu$as); ngEHT discriminator | F114; `test_F114_dielectric_black_hole.py` (2026-06-08 - 15:10) |
| 43 | F114 — Second-order light bending of the exponential index: $\alpha=4\varepsilon+4\pi\varepsilon^2$ ($\sigma=2$) | GR $4\varepsilon+\tfrac{15\pi}4\varepsilon^2$ ($\sigma=7/4$) | excess $\tfrac{\pi}4\varepsilon^2$ (bends more) | Tier-1 exact (sympy); reuses the F111 second-order-deflection closed form $\alpha_2=\pi(2+\sigma)$ | F114; `test_F114_dielectric_black_hole.py` (2026-06-08 - 15:10) |
| 44 | F297 — K2 BBN, primordial $Y_p$ on the model's structural $G$, the F178 source law, $\dot G/G\equiv0$ and $N_\text{eff}=3.044$ | $Y_p$ from the model's own expansion side, $\eta_{10}=6.137$ external | $0.2449$ vs Aver 2021 $0.2453\pm0.0034$, $-0.11\sigma$ | network's own absolute offset **measured** at $-0.87\%$ against PRIMAT-class reference and carried; every model-level conclusion quoted as a difference inside the same network | F297; `test_F297_bbn.py` (2026-08-05 - 23:20) |
| 45 | F297 — K2 BBN, primordial D/H at the same inputs | D/H from the same run | $2.473\times10^{-5}$ vs Cooke 2018 $2.527\pm0.030\times10^{-5}$, $-1.8\sigma$ | network offset $+0.55\%$; $^7$Li is **NOT validated** ($-92\%$) and is excluded from the battery | F297; `test_F297_bbn.py` (2026-08-05 - 23:20) |
| 46 | F297 — the demoted energy-only law (F106) read as a dynamical law: radiation-era normalisation $S=\sqrt{\kappa/2}$ | $S=1/\sqrt2$ derived by power-matching $\ddot a/a=-(4\pi G/3)\kappa\rho$ against continuity | $Y_p=0.1856$, $-17.6\sigma$; full-tensor law $-0.11\sigma$ | **conditional on a reading** — F182 A1 makes the law internally inconsistent for $p\ne0$, so this excludes it as a *dynamical* law; as a violated constraint the history is identical and BBN is silent | F297; `test_F297_bbn.py` (2026-08-05 - 23:20) |
| 47 | F297 — BBN + $\tau_n$ as a measurement of $m_n-m_p$ | $\partial Y_p/\partial\Delta m=-0.607\ \mathrm{MeV}^{-1}$ ⇒ $\Delta m=1.293\pm0.0056$ MeV ($1\sigma$) | model's $+1.51$ MeV (F122/F123) gives $Y_p=0.1210$ ($-36.6\sigma$), D/H $-22.6\sigma$, $\tau_n=330.8$ s vs $878.4\pm0.4$ s | **F122's own check S8b used $\pm1$ MeV — this is 179× tighter.** Sign survives, value excluded; one of F122's two terms is wrong by 0.217 MeV | F297; `test_F297_bbn.py` (2026-08-05 - 23:20) |
| 48 | F297 — declared NULL: can BBN see the model's deuteron binding? | $B_d$ model $-$ PDG $=-0.026\%$ | D/H moves $+0.078\sigma$ of Cooke 2018; sensitivity $-9.0\times10^{-7}$ per 1% in $B_d$ | recorded so nobody later cites BBN as confirming the derived $B_d$; a parameter-free $B_d$ would have to beat $\sim0.4\%$ to be tested here at all | F297; `test_F297_bbn.py` (2026-08-05 - 23:20) |
| 48a | F361 — K2 BBN, $^7$Li/H after the A=7 rate repair (supersedes row 45's "NOT validated" note for Li7 specifically; Y_p/D_H rows 44-45 unchanged) | Li7/H from the repaired network, same run as rows 44-45 | $4.686\times10^{-10}$ vs PRIMAT-class reference $5.00\times10^{-10}$, $-6.28\%$ (was $-92\%$ pre-repair) | validated to a declared 10% band (K2-13); control (`legacy_a7_bug=true`) reproduces the pre-repair $-92.2\%$ and isolates to K2-13 only | F361; entry-driven `F361-bbn-a7-repair` (2026-09-03 - 18:35) |
| 49 | F299 — B10/H1-vs-H2: $\sigma_R/\sigma_3$ for SU(3) irreps $\bar3,6,8,10,15,15',27$ on the model's own exactly solvable 2D SU(3) engine, at the model's own coupling $\beta=2N/g_s^2=24$ | Casimir scaling $C_2(R)/C_F$ exactly in the continuum limit; centre dominance predicts 1 for every non-zero triality and 0 for triality 0 | $\sigma_6/\sigma_3=2.4911511$ vs Casimir $5/2$ and centre $1$; worst rung $1.36\%$ from Casimir, nearest miss of a centre value $1.49$ absolute | quantitative, tol 0.015 at $\beta=24$ — the residual is the finite-$\beta$ lattice artefact and falls monotonically to $1.7\times10^{-4}$ by $\beta=192$; anchored on `confinement.string_tension` at $1.1\times10^{-16}$ and grid-converged at $5.8\times10^{-15}$ | F299; `test_F299_casimir_scaling.py` (2026-08-06 - 12:35) |
| 50 | Weak-field isotropy ratio, Richardson-extrapolated | $\beta_t/\beta_s = 4$ | $2.3\times10^{-10}$; truncation is $-g^2/16$ with the coefficient held to 4 digits over a factor 2 in $g$ | F323 leg X1c |
| 51 | **PRELIMINARY** $d=4$ Casimir ratios at $\beta_s=5.9$, $6^4$, **3 configs** | $5/2$, $9/4$, $9/2$ | $2.466$, $2.224$, $4.378$ at $2\times2$ ($-1.4\%$, $-1.2\%$, $-2.7\%$); all three fall below Casimir at $3\times3$. NOT a claim — no error estimate, and the $2\times3$ vs $3\times2$ asymmetry exceeds the effect | F323 §3.3; `run-bcc-confinement-d4` |
| 52 | F403 — O_h residual verdicts vs NuFIT 6.0 NO 3σ: cube-axis frame no unitary residual viable; trimaximal frame TM1 viable with $\sin^2\theta_{12}\in[0.3170,0.3195]$, $\delta\in[252.4°,293.4°]$ (2026-09-24 - 12:40) | data box | no cube-frame column within $0.0203$ of the box; TM1 1.3–1.7σ above JUNO $\sin^2\theta_{12}$ | `F403-oh-residual-pmns` legs N1, N2, B2–B4 |
| 53 | F404 — Koide pseudo-mass quark fork: required off-diagonal weight 0.427 (up) / 0.254 (down, all +) of tr S; Schur–Horn δ windows (down, all +: δ ≤ 0.180, excludes δ*); all-positive joint min Koide violation 2.1e-2 at CKM χ² ≤ 1 (corrected from 1.9e-3, a penalty artifact, 2026-09-24 - 15:30); signed-down fits at unitary floor χ² = 0.119 only in the band −0.05 ≲ δ_D−δ_U ≲ 0.1, off-band (0.24, 0.01) fails (2026-09-24 - 13:10) | PDG 2025 masses + CKM | numerical search, 24 starts; scipy prototype agrees | `F404-koide-pseudomass-fork` legs P2–P5, P7 |
| 54 | F403 — subgroup-level verdicts vs NuFIT 6.0 NO 3σ: cube-axis and face-diagonal frames, 0 viable non-trivial residual subgroups; trimaximal frame, 18 survivors, all single-column (TM1/TM2); no three-column residual viable in any frame (2026-09-24 - 14:16) | data box | same grid/tolerance as #52 | `F403-oh-residual-pmns` legs S2–S4 |
| 55 | F405 — lepton-Koide bound on a finite-stiffness selector: quark shifts need $(gR^4)_q/(gR^4)_\ell\ge4.6\times10^3$; power-law undressing $\varepsilon_U/\varepsilon_D=3.88$ vs 4 (coincidence candidate, 1.8–2.4σ) (2026-09-24 - 15:40) | PDG 2024 $m_\tau$ 2σ; PDG 2025 quarks | lepton $\lvert k^2-1\rvert\le3.7\times10^{-5}$; ratio $3.878\pm0.068$ (corr.) | `F405-quark-B-colour-charge` legs S1, P1, P2 |
| 56 | F407 — minimal pseudo-mass quark fit (report derivation three): 9 params vs 10 obs, Jacobian rank 9 (one dof); candidate E_g pairs (δ*,δ*), (δ*/3,2δ*/3), (δ*/3,δ*/2) fit at Δχ² ≤ 1 in both schemes, m_s unpulled, signed down sector emergent; all-positive needs m_s ≈ 27 MeV (mixed) / 12.6 MeV (M_Z); GST not emergent, soft \|V_us\| floor ≈ 0.19–0.20 (2026-09-24 - 17:10) | PDG 2025 masses + CKM (Antusch et al. at M_Z, PDG relative errors) | Δχ² = χ² − 0.119 unitary floor, 1 dof; certificates are upper bounds | `F407-koide-pseudomass-minimal` legs M1–M5 |

---

## Currently failing / not-yet-met

| # | Construct | Where it sits | What blocks it |
|---|---|---|---|
| 1 | ~~Absolute coefficient of light deflection~~ | GR-1 (Finding 14.15) | **RESOLVED → Tier 3 #15**: open-BC James/Hockney Poisson kernel gives $|K| = 3.881$ — 3.0% off Einstein, PASS at the 5% gate. The PBC version (12.5% off) is retired. Residual 3% is finite Gaussian-source extent. |
| 2 | ~~$1/b$ scaling of 3-D EMQG lensing~~ | F8 follow-on → **F244** | **RESOLVED (2026-07-03, F244):** scan re-run on the genuine 3-D EMQG potential (`solve_poisson_3d`, $1/r$ Green's fn) with the parameter-free GR-Shapiro $c=c_0/(1-2\phi/c_0^2)$ — free $\alpha$ eliminated. $\Delta\theta\propto1/b$: exact continuum closed form $\Delta\theta=2GMb/(b^2+\sigma^2)$ slope $-0.9959$ (machine $1/b$), lattice isolated $-1.074$, periodic $-1.062$; Cayley stepper deflects toward mass, norm to $10^{-15}$. |
| 3 | ~~Pointwise composite-photon curl matches free Maxwell at $O(k^3)$~~ | Finding 2 / F21 / F23 / F25 | **CORRECTED (2026-08-04, F306, ledger S18) — the 2026-05-23 reframing below was wrong.** The $O(k)$ residual is an artifact of the residual's *definition*, not a prediction: `EM_bilinears` returns **real** $E_G,B_G$ while the RHS $i2\tilde n\times B_G$ is **imaginary**, and $B=\hat n\times E$ exactly, so the two sides are orthogonal 3-vectors of equal length ($\lVert$LHS$\rVert/\lVert$RHS$\rVert=1.0000000000$ at every $k$) and the residual is $\sqrt2\times$ either one. $c_\text{lat}/\sqrt2$ is $c_\text{lat}$ (by its own definition, F26) times a quadrature factor — **not** a Planck-scale signature. It does **not** reduce to Maxwell as $\Delta t\to0$: measured 0.4082469 / 0.4082468 / 0.4082469 at $\Delta t=10^{-3},10^{-6}$ and for the exact derivative, because $E$ is real by construction. Read as analytic amplitudes the curl equation **closes at $O(k^3)$** with coefficient $c_\text{lat}^3/48=1/(144\sqrt3)$ — the pass criterion at `qca-papers-1-4-overview.md:407`. Smearing was never the variable (F23's negative result stands; its root cause does not). *(Superseded text, kept per the append-only rule: “REFRAMED (2026-05-23): the $O(k)$ residual is a confirmed prediction, not a failure… reduces to the Maxwell curl in the $\Delta t\to0$ limit… the leading Planck-scale signature of the discrete time step.”)* **RESOLVED (2026-07-15, F246, L2):** the subleading coefficients of the F26 even-rotation law have a closed form. $\Omega_\text{even}(k)$ is even in scalar $k$, so **all even-power ($k^2,k^4$) dispersion terms vanish identically** (no CPT-odd LV; leading signature is the CPT-even cubic $\lvert k\rvert^3$). $\Omega_\text{even}/\lvert k\rvert=c_\text{lat}+c_3(\hat k)k^2+\dots$ with $c_3(\hat k)=-(\sqrt3/216)(p+3q)$ (machine-precision $4.5\times10^{-19}$; $c_3(111)=-\sqrt3/486$, vanishes on $\langle100\rangle$). `casim.engine.interactions.derive_f26_dispersion`. |
| 4 | ~~F3 lensing prediction failure at low fermion density~~ | next-steps line 5 → **F243** | **RESOLVED — NOT FALSIFIED (2026-07-03, F243):** F3 back-reaction run from $\rho=1$ to $10^{-3}$; the $\lvert\Phi\rvert$-depression (lensing source) stays correct-sign, positive-definite, non-divergent, survives to the lowest $\rho$, and scales linearly (weak-field log-log slope $1.012$). No low-density failure — the prediction degrades gracefully as source×coupling. |
| 5 | ~~Subleading coefficient $\beta \approx 0.01883$ (3D) / $\alpha \approx -0.0104$ (2D)~~ | Finding 7 → **F245** | **RESOLVED (2026-07-15, F245, L1):** both are closed, direction-resolved. **2D:** $\alpha(p)=(\cos4p-9)/768$ (machine-precision $2.8\times10^{-19}$; on-axis $=-1/96$ derived algebraically — the reported $-0.0104$). **3D:** $\beta(\hat k)=-(\sqrt2/12)\,\hat k_x\hat k_y\hat k_z$ (machine-precision $9\times10^{-15}$; the cubic $xyz$ harmonic, vanishes on coordinate planes). The reported $0.01883$ is $\beta$ at the seed-0 max-residual random direction, **not a constant** ($\langle\beta\rangle_\text{sphere}=0$; max $\lvert\beta\rvert=\sqrt6/108$ at $(1,1,1)$). `casim.engine.interactions.derive_curl_subleading`. |
| 6 | Cayley arm of C1 / F3b / L4.c at $L=1280$ or $L=960$ | 10× bump (2026-05-16) | Sparse-LU memory ≈ 5–10 GB exceeds sandbox. Run at $L=384$–$512$ fallback. |
| 7 | ~~SI-unit identification for $a$ and $\tau$~~ | Finding 10 → F107 → **F232** | **RESOLVED (2026-07-02, F232):** lightcone $a/\tau=c\sqrt d$ adopted; $a=\sqrt{8\pi}3^{1/4}\ell_P$ pinned by the F79 $G$-match (F107). F232 proves the mass-independent lensing route is DEGENERATE (deflection coeff $-4$ is dimensionless/$a$-independent) — a scale-invariance theorem: only the dimensionful $G$ pins $a$. The one honest limit (metre enters once via $\ell_P$) is shared by any theory. |
| 8 | Global-stability invariant (audit C.3) | F101-A2 → F108 → F118 → **F234** | **CLOSED (2026-07-02, F234):** the F108 framing below is superseded. **F118** already found the self-consistent $(W,v,c)$ triple on the $\kappa_E<0$ spontaneous-$E_g$ branch (lepton point GLOBAL, gap $-2\times10^{-6}$, wall-KKT$<0$, PD, all couplings $O(1)$ over a 2D region). **F234** pins the last residual (the brake value): the derived $\delta^*=\tfrac29$ (F174/F175) into $\cos3\delta^*=|B|/2C$ with derived $B$ (F95) gives $\lambda_6=0.243$ exactly ⇒ $\lambda_6$ **derived, not fit** (supersedes F179/CN3). E4 collapses into E1's weight→phase principle. *(Historical F108 note: democratic class excluded exactly Gap$\ge+0.0386$; the pre-F118 one-loop bubble gave wrong-sign sextic — resolved by the $\kappa_E<0$ branch.)* |

---

## Tally (updated 2026-05-28 after F46 — spherical Pythagorean lattice-mass identity)

- **132 exact algebraic** results (128 after F43 + 4 new from F46: closed-form 2D spherical Pythagorean identity (P1); same from explicit 4×4 $D_k$ eigenvalues (P2); BCC extension both helicity branches (P4); rest limit $\Omega_\text{Dirac}(0,m) = \arcsin m$ across 8 masses (P6)).
- **50 machine-precision** results (47 after F43 + 3 new from F46: time-evolved Dirac QCA stepper matches identity per tick (P3); photon limit $m=0$ on 2D + BCC (P5); continuum-limit log-log slope $4.0055$ of the 4th-order Pythagorean residual (P7)).
- **26 quantitative** matches inside their declared tolerances (25 after F37 + 1 new from F40: F40-Q4 up/down/strange mass-splitting ratios).
- **Currently-failing #3** (composite-photon curl O(k³) closure) **reframed as resolved** — the O(k) residual is the correct discrete-time prediction, not a failure.

**Open-BC Poisson upgrade (2026-05-20):** `casim.engine.lattice.poisson_open` adds a free-space (James/Hockney zero-padded FFT) Newtonian Poisson solver. It recovers $\phi = -G_N M/r$ to machine precision at $r \ge 20$ cells. Both GR-domain line-integral tests improve dramatically:

- **GR-1 deflection:** $|K| = 3.50$ (PBC) → $3.88$ (open BC), from 12.5% off Einstein to 3.0% off — PASS at 5% gate.
- **GR-2 Shapiro:** ratio $0.5$ (PBC) → $1.0006$ (open BC), from 38% off to 0.06% off — PASS at 0.1% gate, pins PPN $\gamma=1$.

The periodic-Poisson kernel was confirmed to be the single largest accuracy limit on the GR-domain tests, exactly as Finding 14.9 predicted.
- **7 open/blocked** items requiring code or judgment.

This is the inventory the test roadmap (`lattice-vs-spacetime-tests.md`) is written against. Every PASS already on the books is in tiers 1–3 above; every test in the roadmap is either a new gate that has not yet been built, or an extension of an existing gate (e.g., the absolute-coefficient version of an existing ratio test).

---

## Connections to the literature

*Conceptual bridges that tie the algebraic identities above to claims made independently in the reference papers. Not themselves test items — just documentation of where our exact results are the concrete realisation of a generic statement made elsewhere.*

### 2026-05-21 - 19:41 — 't Hooft CAI Eq. 5.5 ↔ QCA arccos dispersion (Tier 1 #12, #13, #19)

**'t Hooft, CAI §5, Eq. 5.5** (verbatim from the PDF, p. 47):

$$
U_\text{op}(\delta t) \;=\; e^{-iH_\text{op}\,\delta t}, \qquad 0 \le H_\text{op} < 2\pi/\delta t.
$$

Because $U_\text{op}(\delta t)$ for a deterministic CA is a permutation matrix, its eigenvalues are unimodular $e^{-i\omega_i}$ with $\omega_i \in [0, 2\pi)$ (his Eq. 5.4). The Hamiltonian $H_\text{op} = (i/\delta t)\log U_\text{op}$ is therefore well-defined only **modulo $2\pi/\delta t$** — one is free to add integer multiples of $2\pi/\delta t$ to any eigenvalue without changing $U_\text{op}$. 't Hooft flags this branch-cut freedom as one of the three structural obstructions (locality, positivity, additivity) to using $H_\text{op}$ directly.

**Our 2D-square / Dirac / BCC dispersions** (Tier 1 #12, #13, #19):

$$
\omega_{\vec k} \;=\; \arccos(c_x c_y), \qquad
\omega_{\vec k} \;=\; \arccos\!\bigl(\sqrt{1 - m^2}\, c_x c_y\bigr), \qquad
\omega_{\vec k} \;=\; \arccos(\text{BCC kernel}).
$$

The principal-branch $\arccos(\cdot)$ maps the unit interval $[-1, 1]$ onto $[0, \pi]$ — i.e. picks **one specific branch** of the multi-valued $\omega = (i/\delta t)\log\lambda(U)$. In lattice units ($\delta t = 1$) the range $[0, \pi]$ sits inside 't Hooft's $[0, 2\pi)$ window; the other branches ($\omega + 2\pi n$, and the negative-frequency partner from the doubled spinor structure) are exactly the $H_\text{op}$ ambiguity he describes.

**Why these are the same observation.**

| 't Hooft framing | QCA framing |
|---|---|
| Generic: $H_\text{op}$ from a CA propagator is defined mod $2\pi/\delta t$. | Specific: the QCA propagator on BCC/square has eigenvalues $\lambda(\vec k) = e^{\pm i\arccos(\cdot)}$. |
| The mod-$2\pi$ ambiguity is one of three open obstructions. | The Bisio–D'Ariano informational principles (locality + isotropy + linearity + unitarity + homogeneity) **fix the propagator uniquely**, which fixes the dispersion to a specific arccos function. |
| Branch-cut freedom is unresolved. | Branch choice is resolved by the principal arccos and the spinor-doubling that supplies the second branch. Residual at machine precision (Tier 1 #12: $3.3 \times 10^{-16}$; #13: $3.9 \times 10^{-16}$; #19: $5.7 \times 10^{-16}$). |

The arccos dispersion is, structurally, *the concrete answer* to the mod-$2\pi/\delta t$ ambiguity 't Hooft poses, for the unique class of CA propagators consistent with the five informational principles. He poses the problem; the QCA literature resolves it for this class.

**Operational consequences this connection clarifies:**

1. **Why the dispersion is bounded.** $\omega_{\vec k} \in [0, \pi]$ for the principal branch is not a numerical accident — it is the canonical representative of the equivalence class of $H_\text{op}$ values, as constructed in 't Hooft Eq. 5.5.
2. **Why $\beta_\text{LV}(m)$ and $\gamma_\text{LV}(m)$ are closed-form** (Tier 1 #20, #21). The Lorentz-violation residues come from Taylor-expanding the *specific* arccos branch around $\vec k = 0$. There is no branch ambiguity in the small-$k$ expansion because the principal branch is analytic in a neighbourhood of $\vec k = 0$.
3. **Why we are quantitatively ahead of the CAI on this specific point.** 't Hooft writes Eq. 5.5 as an open problem ("there is a lot of freedom in the definition of $H_\text{op}$"); we exhibit the unique branch and verify dispersions to FFT round-off across multiple sectors.

**Cross-reference:** also noted in `references/t-hooft-2015-cai-summary.md` §6 item 6, which proposed adding this annotation to the inventory.

### 2026-05-21 - 20:35 — SR-2 LV expansion is the implicit-function expansion of $\arccos(n\cos u)$; the recursion continues indefinitely

The closed forms in Tier 1 #20, #21, #21b reveal a structural pattern:

$$
R(\beta) - \sqrt{1-\beta^2} \;=\; \sum_{n \ge 1} a_{2n}(m)\, \beta^{2n}, \qquad
a_{2n}(m) \;=\; \frac{1}{2^{2n-1}\binom{2n}{n}/n} \;-\; \frac{P_n(m)}{(2n)!!\cdot (1-m^2)^{(2n-1)/2}\,\arcsin m}
$$

where the rational constants match the SR Taylor expansion of $-\sqrt{1-\beta^2}$ at each order ($\tfrac12, \tfrac18, \tfrac1{16}, \ldots$) and the numerator polynomials are

| Order | $a_{2n}$ | Rational constant | $P_n(m)$ | Denominator factor |
|---|---|---|---|---|
| $\beta^2$ | $\beta_\text{LV}$ | $\tfrac12$ | $m$ | $2\, n^1$ |
| $\beta^4$ | $\gamma_\text{LV}$ | $\tfrac18$ | $m(3 - 2m^2)$ | $24\, n^3$ |
| $\beta^6$ | $\delta_\text{LV}$ | $\tfrac{1}{16}$ | $m(15 - 20m^2 + 8m^4)$ | $240\, n^5$ |
| $\beta^8$ | $\varepsilon_\text{LV}$ | $\tfrac{5}{128}$ | $m(35 - 70m^2 + 56m^4 - 16m^6)$ | $896\, n^7$ |

The rational constants $\{\tfrac12, \tfrac18, \tfrac{1}{16}, \tfrac{5}{128}, \ldots\}$ are the SR Taylor coefficients of $-\sqrt{1-\beta^2}$ at $\beta^{2n}$: they come from the $\beta^{2n}$ matching with $1/\gamma_\text{SR}$ in $R(\beta) - 1/\gamma_\text{SR}$. The polynomial numerators $P_n(m)$ are degree $2n-1$ in $m$ with alternating-sign integer coefficients.

The recursion is mechanical: implicit-function expansion of $\omega(u) = \arccos(n \cos u)$ to order $u^{2N+1}$, inversion $u(\beta) = \sum_{k=1}^{N} c_{2k-1}\beta^{2k-1}$, substitution into $R(\beta) = (\omega - u\,\partial_u\omega)/\arcsin m$, Taylor expansion, and read off $a_{2N}$. Carrying to order $u^{11}, u^{13}, \ldots$ would yield $a_{10}, a_{12}, \ldots$ by the same recipe. The series does not truncate: every coefficient is a rational function of $\arcsin m$ and $\sqrt{1-m^2}$, with $\arcsin m$ entering linearly in the denominator at every order.

Code: `casim.engine.interactions.derive_beta_LV` now derives $\beta_\text{LV}, \gamma_\text{LV}, \delta_\text{LV}, \varepsilon_\text{LV}$ and confirms all four against the symbolic series at zero residual. To extract $\beta^{10}$, raise `SERIES_ORD` to 12 and add $c_{11}$ to the $u(\beta)$ ansatz. Each additional order costs one sympy polynomial inversion — seconds.

## F134 — unified real-space integration (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 75 | unified coupled-chain consistency: per-channel norm drift; system net charge $uud+e$; four loops live | machine / exact / structural | norm drift $1.3\times10^{-14}$; $\lvert Q\rvert<10^{-12}$; all four loops $>0$ |
| 76 | real-space confinement null + EM-loop attraction: proton RMS coupled vs free; min proton–electron separation driven vs free | quantitative | coupled$\equiv$free $<1\%$ (no confinement from linearised gluon); driven min-sep $1.86<3.0$ start, vs free min $3.0$ (Coulomb attraction present) |

Test: `tests/findings/test_F134_unified_real_space.py` (3/3). The strong loop's binding lives in the non-perturbative confinement sector (F86/F94/F110), not the linearised `gluon_sourced` (F43) kernel; the EM loop attracts but a stationary orbit needs the U4 scale separation (F133 block-spin multigrid). See `findings/F134-unified-real-space-integration.md`.

## F135 — real-space scalar confinement (U1) (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 77 | `dirac_step_3d_bcc_varm_splitstep`: uniform field == constant-m step; unitarity under a strong scalar well | machine / bit-for-bit | residual $0.0$; norm drift $<10^{-12}$/100 steps |
| 78 | scalar confinement binds (bounded cluster RMS) vs free dispersal; vector mode Klein-null | quantitative | confined max $3.74$ (plateau) vs free $>7$; vector $\equiv$ free within $15\%$ |

Test: `tests/findings/test_F135_realspace_confinement.py` (3/3). Confinement is a Lorentz-SCALAR linear potential (position-dependent mass = MIT bag = F86 ε_c→0); a VECTOR potential of the same shape Klein-tunnels and does not bind. Closes F134's U1 null. See `findings/F135-realspace-scalar-confinement.md`.

## F136 — scalar string on SU(3) colour quarks (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 79 | uud colour-quark aggregate charge | exact (rational) | $+1$ |
| 80 | colour-quark scalar confinement bound vs free; SU(3) loop live | quantitative / structural | confined max $3.72$ vs free $>6.7$; $J_\text{colour}\!\to\!A>0$; norms $2\times10^{-14}$ |

Test: `tests/findings/test_F136_colour_quark_confinement.py` (3/3). See `findings/F136-colour-triplet-dirac-quark-confinement.md`.

## F137 — live colour-dielectric flux-tube field (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 81 | live colour-dielectric bag binds the colour-quark cluster vs free | quantitative / machine | bag max $<3.0$ vs free $>6$; norms $1.7\times10^{-14}$ |
| 82 | connected flux tube + monotone ≈linear confining $E(R)$ (F86 signature) | quantitative | midpoint $\varepsilon_c$ melted to $R\!\approx\!2\lambda$; $E(R)$ linear $\Delta\!\approx\!33$/unit over $R\lesssim4$ |

Test: `tests/findings/test_F137_live_flux_tube.py` (3/3). The bag is a mean-field dielectric (fixed smear λ); the exact asymptotic σ=2πv²n is F86's BPS result it approximates locally. See `findings/F137-live-colour-dielectric-flux-tube.md`. **The mean-field pinch is closed by F139 (self-consistent dual-GL back-reaction).**

## F138 — Weinberg gap closure: $\sin^2\theta_W=1/4$ matched at $\mu_\star=4\pi v$ (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 83 | $s^2(t^2)=t^2/(1+4t^2)<1/4$, $\to1/4$ as $g_X\to\infty$; bridge $(2/9)/(1/4)=8/9$; $\sin^2_\text{os}=2/9\Leftrightarrow m_Z/m_W=3/\sqrt7$ | algebraic / exact rational | exact (fractions) |
| 84 | $\sin^2\bar\theta_W(M_Z)$ from $1/4$ @ $4\pi v$, 1-loop Higgs-free | quantitative (decisive) | $0.23173$ vs PDG $0.23122$: $+0.22\%$ (was $+8.12\%$ bare); $m_Z/m_W$ vs $3/\sqrt7$: $-0.063\%$ |

Test: `tests/findings/test_F138_weinberg_matching_4piv.py` (3/3). $\mu_\star=4\pi v$ is NDA ($\ln$-offset $0.099$ to the measured crossing 3.42 TeV); the induced-$Y$-kinetic-term lattice loop would make $\mu_\star$ exact. See `findings/F138-weinberg-gap-closure-4piv-matching.md`.

## F139 — self-consistent dual-GL back-reaction (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 85 | pinch-off cured: self-consistent tube stays connected where the F137 mean-field bag pinches (A/B) | quantitative | $\varepsilon_c^{\text{mid}}>0.97$ (SC) vs $0.12$ (mean-field) at $R=11$ |
| 86 | linear $E_{\text{bag}}(R)$ with $R$-independent cross-section (dynamical F86 $\sigma=2\pi v^2 n$) | quantitative | tension flat to factor $1.23$; vacuum $f_{\min}=1.0000$ |

Also: G1 the GL condensate sector is ODE-exact (domain wall $\tanh(x/2\xi)$ to $5.6\times10^{-4}$, mesh-floor); G2 the coupled $(f\leftrightarrow$ flux$)$ loop converges to a fixed point (residual $9.5\times10^{-7}$, monotone). Test: `tests/findings/test_F139_dual_gl_backreaction.py` (4/4). Closes the F137 §5 mean-field pinch. See `findings/F139-self-consistent-dual-gl-backreaction.md`.

## F141 — WS-cell 7-axis lemma + on-shell mass counting (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 87 | BCC Voronoi-relevant vectors = exactly 14 (8 NN + 6 NNN); WS cell = truncated octahedron (24 vertices, $\mu^2=5/4$, 8 hexagonal + 6 square facets, 7 axes mod inversion); relevance closed by $\lvert v\rvert^2\le 4\mu^2=5<8$ | geometric / exact (integer + rational) | **exact** (stdlib `fractions`, no float) |
| 88 | Equal stiffness per structural channel (7 axis + 2 sublattice) $\Rightarrow m_W^2{:}m_Z^2=7{:}9$, $m_Z/m_W=3/\sqrt7$, $\sin^2\theta_W^{\text{os}}=2/9$, bridge $(2/9)/(1/4)=8/9$ | exact rational (conditional on hypothesis U) | exact algebra; PDG: $m_Z/m_W$ $-0.063\%$, on-shell $s^2$ $-0.44\%$ |

Test: `tests/findings/test_F141_ws_cell_mass_counting.py` (11/11). Hypothesis U (universal stiffness quantum; §4 of the finding) is the remaining underived input — (U2) reduces to the same induced-$Y$-kinetic-term lattice loop F138 left open. See `findings/F141-ws-cell-7axes-onshell-mass-counting.md`.

## F142 — dielectric-tube no-go + non-Abelian centre-content scope (2026-06-11)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 89 | Dual-SC dictionary $B=e^2v^4/4$, $\Phi=2\pi n/e$ (BPS) ⇒ thin-wall dielectric-tube tension $\sigma_{\rm FL}=\Phi\sqrt{2B}=(1/\sqrt2)\,2\pi v^2 n$ (right scaling, prefactor $1/\sqrt2$, not $1$) | 1 (algebraic) | prefactor $1/\sqrt2$ to $10^{-12}$ |
| 90 | No-go: continuum $\varepsilon_c=1-f^2$ electric functional does not confine — spread-thin config $\sigma\propto A^{-1/3}\to0$ (decade ratio $=10^{1/3}$); plus SU(3) $k$-string degeneracy $\sigma_2=\sigma_1$ (Casimir $k(N{-}k)$ and sine $\sin(k\pi/N)$ both) | 1 (algebraic / group theory) | $A^{-1/3}$ to $<10^{-6}$; $\sigma_2/\sigma_1=1$ exact |
| 91 | Direct growing-box minimisation: tube tension falls as $L^{-2/3}$ (non-confining) — $\sigma(L{=}61,91,141,201)=1.37,1.04,0.77,0.61$ | 3 (numeric) | matches $L^{-2/3}$ to $<2\%$ |

The no-go resolves F139 §6: $\sigma=2\pi v^2 n$ is the *topological* charge of the magnetic ANO vortex (winding $n$, $f\to v$ pinned at $\infty$), absent from the electric source-charge dielectric tube; F139's constant tension is a finite-box + $\varepsilon$-floor regulator effect. The algebraically-exact map already exists: F99's $\sigma_k=-\ln s_k$, small-$\sigma$ limit $\sigma_k=2\pi v^2 k$. Q2: the full non-Abelian condensate is exactly derivable only in its centre content (existence F88, N-ality F99, Casimir ratios, Abelian dominance); dynamical VEV / 3+1D $\sigma$ remain MC-only (F94). Module `casim.engine.interactions.derive_dielectric_noconfine` (self-checking `main()`). See `findings/F142-dielectric-tension-no-go-and-nonabelian-scope.md`.

## F144 — Route A: $\alpha_s$ from the rule by dimensional transmutation (2026-06-12; renumbered from F143 — concurrent session)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 92 | The lock derived: rule's F26 step exactly circular on $(\mathbf E,\mathbf B)$; lemma orthogonal flow $\iff$ equal stiffness (sympy-exact) ⇒ $\chi=1$; F110 C7 $\chi=1/(4g_s^2)$ matrix identity ⇒ $g_s=\tfrac12$, $\alpha_s(\mu_0)=1/(16\pi)$ | 1 (exact / machine) | kernel residuals $<10^{-15}$; matrix resid $=0$ |
| 93 | Zero-parameter $\alpha_s(M_Z)$: 1-loop $+1.31\%$, 2/3/4-loop converged $+8.4\%$ vs PDG 0.1180; $\Lambda^{(3)}_{\overline{\rm MS}}$ ×1.54 FLAG; hierarchy $N=2.9\times10^{-19}$ ×1.9 of F119 (19 decades, no tuning) | 3 (PREDICTION) | residual ≡ one scheme constant, bounded: equiv $\Lambda$-ratio 1.78 (Wilson 28.81) |

Test: `tests/findings/test_F144_route_a_alpha_s.py` (5/5). Open: the model-action one-loop scheme constant (must be ≈1.8, not ≈29 — sharp falsification target). See `findings/F144-route-a-alpha-s-dimensional-transmutation.md`.

## F143 — wrap-stiffness fermion loop: transverse no-go + longitudinal magnitude (2026-06-12)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 94 | F42 kinetic wrap is a conjugation ⇒ zero induced transverse $Y$ stiffness from the kinetic sea, all orders | exact / machine | $\max\lvert\delta\theta\rvert=1.3\times10^{-15}$ |
| 95 | Induced wrap (Goldstone) stiffness $\hat f=4\pi^2 f^2/m^2\in[0.17,0.38]$ ($m\in[0.3,0.6]$); PT==supercell $5.8\times10^{-4}$; $\Pi\propto q^2$; fermion share of $v^2$ = 0.16–0.36% ⇒ $\mu_\star$ shift $<0.2\%$ | quantitative (decisive) | no large-log; $E_g$ sector owns $\gtrsim99.6\%$ of $f_\theta^2$ |

Test: `tests/findings/test_F143_wrap_loop_stiffness.py` (5/5). Scan: `tests/runners/run_F143_wrap_stiffness_scan.py`. See `findings/F143-wrap-loop-stiffness-nogo.md`.

## F145 — Route C: the induced NJL coupling (2026-06-12)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 96 | Exact Fierz of one-gluon exchange: $c=\tfrac29$ in all four chiral channels (induced interaction exactly $U(2)_L\times U(2)_R$ — F77 form forced); Fock identity $\sum\gamma^\mu T^a\,\gamma_\mu T^a=4C_F=\tfrac{16}3$; corrects F116 NJ4's $\tfrac49$ | 1 (machine-exact, 24-dim algebra) | $8\times10^{-17}$ / exact |
| 97 | Criticality of the induced gap kernel: bare $g_s^2=\tfrac14$ resolved $R=G/G_c=0.075$–$0.10\ll1$ (no-go, $\varepsilon_c$ can't rescue); Route-A running $R=2.6$–$15\gg1$ (χSB forced); $\alpha_\text{crit}=1/(4\pi R_0)=0.20$–$0.27$; F77 fit $1.277\Leftrightarrow\alpha_\text{eff}=0.26$–$0.34$ bracketed | 3 (decisive numeric / PREDICTION) | contact anchor machine ($5\times10^{-15}$); residual = the one IR-coupling/scale-setting number (shared F124/F144-A4) |

Test: `tests/findings/test_F145_route_c_induced_njl.py` (5/5). See `findings/F145-route-c-induced-njl-coupling.md`.

## F147 — walk-loop rigidity + channel equality (2026-06-12)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 98 | One-tick gauge rigidity: half-filled one-tick sea has zero static response to any plane-wave gauge field, both channels; mechanism = gauged spectral closures $\lambda\to-\lambda$ ($\{P,W_A\}=0$, any $A$) and $\lambda\to-\bar\lambda$ ($\theta\to\pi-\theta$, filled pairs sum to $-\pi$) | exact (mechanism verified at $\varepsilon=0.3$) | closures $0.0$; $\lvert\chi\rvert<10^{-12}$; two-tick Ward $0.0$, one-tick staggered Ward fails $9.2\times10^{-3}$ |
| 99 | Stroboscopic channel equality: F51 hypercharge (parity-staggered) bubble = vector bubble pointwise ($\Pi_\text{stag}(\tilde q)=\Pi_\text{vec}(\tilde q+Q)=\Pi_\text{vec}(\tilde q)$); full brute-force response channel-equal ⇒ U2 dynamical ratio $=1$; bare-content $t^2=1/4$, $s^2_\text{free}=1/5$, F49 gap $=(2/7)/(1/4)=8/7$ exact | exact / machine + exact rational | pointwise $10^{-14}$; full response $0.0$ ($L{=}6$), $7.3\times10^{-8}$ ($L{=}8$); rationals exact |

Test: `tests/findings/test_F147_induced_stiffness_loop.py` (10/10). Module `casim.engine.particles.induced_stiffness`. Companion to F143 (wrap route). See `findings/F147-walk-loop-rigidity-channel-equality.md`.

## F148 — modular element assembler (2026-06-12)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 100 | ¹H assembled stable from model-only constants: net charge $=0$ (integer exact); electron 1s $=-\tfrac12\mu c^2\alpha^2$ reconstructed from imported $m_e,m_p,\alpha$; ionization $=+13.598$ eV vs measured | exact (charge/provenance) + quantitative (energies) | net charge $0$; $\lvert E_{1s}+\mathrm{Ry}_\text{model}\rvert/\mathrm{Ry}=2.5\times10^{-5}$; ionization rel $3.6\times10^{-5}$; assembler constants bit-identical to module values |
| 101 | Modular composition: `build_element(Z,N)` correct $A$ + exact neutrality and Aufbau noble-gas closures (He 1s², Ne 2p⁶, Ar 3p⁶) across H…U; $A=2$ deuteron binds via model NN OBE; $A\ge3$/$Z\ge2$ paths raise model-only recipes | exact (structure) + quantitative (deuteron) | neutrality integer-exact all Z; closures exact; deuteron $E_b=2.234$ MeV (no coupling tuned to binding); hooks honest |

Test: `tests/findings/test_F148_modular_element_assembler.py` (13/13). Module `casim.engine.particles.element`. See `findings/F148-modular-element-assembler.md`.

## F149 — condensate channel splitting + content no-go (2026-06-12)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 102 | Dirac parity theorem $\omega_m(q+Q)=\pi-\omega_m(q)$, $D(q+Q)=-XDX$; $\{S,D_A\}=0$ ($S=\hat P\hat X$, gauged); one-tick rigidity survives mass (both channels, $m=0.4$) | exact | $10^{-15}$ / $0.0$ / $\chi<2\times10^{-11}$ |
| 103 | F147 lock breaks for $m>0$: weights split monotone (rel $0.075\to0.727$, $m=0.05\to0.4$) with gaps exactly equal; full-response onset $\propto m^2$ (scaling ratio 1.08); content no-go exact: bare $t^2=1/4$ (needs $\times8/7$), F38-SM $t^2=3/5$, $s^2=3/8$ (needs $\times10/21$) | machine + numeric + exact rational | 8/8 PASS |

Test: `tests/findings/test_F149_condensate_channel_splitting.py`. Module: `ca_induced_stiffness.py` (Dirac section). See `findings/F149-condensate-channel-splitting-content-nogo.md`.

## F155 — q* self-energy machinery + anchor-free freeze bracket (2026-06-13)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 201 | Tadpole sector empty: F26 link exactly $SO(2)$ per mode ($\det R-1$, $R^\top R-\mathbb1$) $\Rightarrow u_0\equiv1$, Wilson $Z_0=0.1549$ structurally absent; gluon luminal $\Omega_\text{even}\to c_\text{lat}\lvert k\rvert$ | exact / machine | $2.2\times10^{-16}$; luminal dev $1.6\times10^{-12}$ |
| 202 | Lattice−continuum subtraction convergent: $d_1^\text{bubble}=16\pi^2(B_\text{lat}-B_\text{cont})=0.1665$ (scalar bubble, true $\Omega_\text{even}^2$ kernel), $b_0$ slope universal; subtracted LM $q_\ast a$ converges to band top $\sim0.97$ $\Rightarrow q_\ast a\in[0.577,0.979]$ ($0.733$ inside), $\Lambda$-ratio $O(1)$ not Wilson $28.81$ | convergent / bracket | spread $<2\times10^{-4}$; slope ratio $0.993$; $\Lambda$-ratio $[1.33,2.25]$ |
| 203 | Residual-B freeze anchor-free: nonlinear χSB onset L-stable ($\alpha_\text{onset}=0.307$ at $L{=}16,24$), set by gluon mass $m_D$; freeze window $[0.31,0.38]$, $M(0)$-anchored $0.39$ at top, inside continuum window $[0.3,0.5]$ | numeric (L-stable) | onset spread $<5\times10^{-3}$; 5/5 PASS |

Test: `tests/findings/test_F155_qstar_self_energy.py` (5/5). Modules: `casim.engine.gauge.gluon_self_energy`, `ca_gap_solve.py` (`chiSB_onset`/`freeze_window`), `tests/runners/run_su3_3d_string_tension.py` (Cornell $\alpha_V$ fit). See `findings/F155-qstar-self-energy-and-freeze-bracket.md`. **Honest: A bracketed, not pinned — gluonic 3g+ghost finite part / high-res static potential remains.**

| 204 | F156 U2 real-space EM-bound electron (`nr_electron`): ground state relaxed in the Coulomb well is STATIONARY (RMS flat 2.45→2.51 over 400 ticks, spread <0.5%) vs free dispersal to 18.3; split-step exactly unitary; q=−1 localises on +1 source | numeric (Tier-3) + machine-precision norm | bound/free RMS ratio <0.15; norm drift ~1×10⁻¹⁴; 4/4 PASS |
| 205 | F157 multi-electron Hartree SCF: helium Koopmans IP 24.0 eV (CODATA 24.59), total −76.5 eV; model-only (m_e, α; screening from density); generalises by Aufbau (Li, C bound) | numeric (Tier-3, Hartree) | IP within 2.5% of CODATA; 5/5 PASS |
| 206 | F157 multi-nucleon A-body variational cluster (model-deuteron-anchored): alpha particle A=4 binding −30.1 MeV (exp −28.3); A=3 bound; central OBE alone unbound (tensor-driven, F104) | numeric (Tier-3, variational) | A=4 within 6% of exp; heavy A overbinds (saturation open) |
| 207 | F158 U3 neutral hydrogen as one real-space object: net charge 0 exact, all four loops live, proton confined (RMS plateaus ≈3.3 vs free), electron bound+concentric (cloud ≈4>nucleus, e–p sep ≲1.5), norms ~1×10⁻¹³ | exact neutrality + machine norm + Tier-3 binding | net Q <10⁻¹²; norm drift ~1×10⁻¹³; 6/6 PASS |

Tests: `test_F156_realspace_electron_bound.py` (4/4), `test_F157_manybody_atoms.py` (5/5), `test_F158_neutral_hydrogen.py` (6/6). Modules: `src/casim/particles/channel.py` (`NonRelElectronChannel`), `casim.engine.core.manybody`, `casim.engine.particles.element`. Scenarios: `realspace_electron_bound/_free`, `unified_hydrogen_atom/_free`. See `findings/F156-*.md`, `F157-*.md`, `F158-*.md`. **Honest: compressed scale (proton:orbit ~10⁴ ratio is U4); nuclear saturation open.**

| 208 | F159 U4 block-spin two-grid multigrid: R_b charge-faithful (proton total charge conserved EXACTLY under block-average; concentrates RMS r_p→r_p/b); R_b commutes with orbit binding (point-vs-resolved gap→0 as a0/r_p↑; E0 invariant under coarse spacing a_c=b·a_f, spread 0.0027); two-grid atom at b=63000 → a0/r_p=4.28e4 (4.63 decades, ≈physical H) on tractable lattices; open-Poisson electron converges E0→−0.5 Ha, ⟨r⟩→1.5 a0 | exact charge + Tier-3 binding | charge 1.000000; E0 b-spread 0.27%; 4/4 PASS |

Test: `tests/findings/test_F159_multigrid_scale_separation.py` (4/4); runner `tests/runners/run_u4_multigrid.py` → `test-results/u4_multigrid.json`. Module `casim.engine.lattice.multigrid`. See `findings/F159-u4-blockspin-multigrid-scale-separation.md`. **Honest: orchestrated multigrid (fine→R_b→coarse); LIVE two-grid engine co-evolution is the next build.**

| 209 | F160 U4 LIVE two-grid atom (one engine run, two_grid_atom channel): fine confined uud proton + coarse electron co-evolve with per-tick R_b charge reduction; net charge 0 (machine), norms ~3e-14, electron orbit resolved+stable (coarse RMS≈6.2 flat), proton confined (fine RMS≈2.6→3.3), represented a0/r_p≈6e4 (≈4.8 decades = physical H) on tractable lattices | exact neutrality+norm + Tier-3 binding/ratio | netQ<1e-9; drift 2.7e-14; 5/5 PASS |

Test: `tests/findings/test_F160_live_two_grid_atom.py` (5/5). Module `src/casim/particles/channel.py` (`TwoGridAtomChannel`), scenario `unified_hydrogen_multigrid.yaml`. See `findings/F160-live-two-grid-multigrid-atom.md`. **U0–U4 unified real-space chain closed.**

| 210 | F161 atomic photon emission (dynamical P1): lines ħω=E_i−E_f (Lyman-α 121.50 nm, Balmer 656/486/434/410 nm, all <1% vs data); Einstein A from dipole d=∫u_f x u_i dx + Δl=±1 rule (2p→1s 6.27e8 s⁻¹ τ=1.59 ns exact; 3p→1s 1.67e8; 3p→2s 2.25e7; 2s→1s,3d→1s forbidden=0); model-only (m_e,α) | Tier-3 quantitative | λ <1%, A few %; 4/4 PASS |

Test: `tests/findings/test_F161_atomic_emission.py` (4/4). Module `casim.engine.gauge.emission`. See `findings/F161-atomic-photon-emission.md`. First member of the dynamical-processes layer.

| 211 | F162 background-field gluon self-energy assembled (Abbott/HKYS ξ=1, gluon loop Γ^F·Γ^F + ghost loop −2(2k+q)(2k+q)): UV log part EXACTLY transverse, g_{μν}=(22/3)(q²δ_{μν}−q_μq_ν), b₀=(N/2)(22/3)=11/3·C_A=**11** with gluon:ghost split 10:1; scalar-bubble calibration g=1 | algebraic exact (sympy) | b₀=11 exact; transverse exact; 3/3 PASS |
| 212 | F162 lattice b₀ = continuum b₀ (subtracted transverse coeff): Δ=B_lat−B_cont q-flat (no residual log) ⇒ propagator-independent running; Wilson shift −0.0787 flat to <1e-3, rule shift →0 (near-perfect action ⇒ q* at band top, NOT yet the digit) | well-conditioned (numerical) | Wilson spread 7e-5 (n=24); rule mean →−2e-4 |

Test: `tests/findings/test_F162_bgfield_loop.py` (3/3). Module `casim.engine.gauge.bgfield_loop`; native `tests/runners/run_bgfield_loop.py`. See `findings/F162-bgfield-self-energy-b0-gate.md`. The b₀ recovery gate (loop assembly) F155 lacked; the finite gluonic d₁ to the digit (vertex form factors, Wilson-28.81 gate) remains OPEN — F155 q* bracket stands.

| 213 | F165 hypercharge quantisation: linear system {SU(2)²·U(1), SU(3)²·U(1), grav²·U(1), down+lepton mass-step invariance} on lattice-fixed reps has a 1-dim solution space over ℚ; U(1)³ identically zero on it; ratios yQ:yu:yd:yL:ye = 1:4:−2:−3:−6 ⇒ F38 table & SM charges (2/3,−1/3,0,−1) |

Test: `tests/findings/test_hypercharge_quantisation.py` (4/4, exact over ℚ via sympy.Rational — literal integer 0). See `findings/F165-hypercharge-quantisation-from-anomaly-and-mass.md`. Closes audit G4: the five SM Y-values reduce to one normalisation input (the charge unit / F49 sin²θ_W); the other four ratios and charge quantisation itself are derived.

| 214 | F168 paired-photon binding is gauge-protected (audit G2): constituents massless from pure-hop A₀=0 (u±(0)=1 ⇒ ω±(0)=0, exact); chiral relation ω⁻(k)=ω⁺(−k) exact (residual 0) ⇒ symmetric (+,−) pair = parity-even vector/identity channel; rest mass lives only in the F27 branch-coupling vertex X (gap=m to 4e-17), identity channel has X≡0 ⇒ Ω(0)=0 forced; split O(k²), no mass term |

Test: `tests/findings/test_F168_paired_photon_binding.py` (4/4: B1 exact, B2 residual 0, B3 quantitative slope 1/√3 + exp≈2, B4 4e-17). See `findings/F168-paired-photon-binding-gauge-protected.md`. Partial closure of G2: zero binding energy is structure/gauge-forced (not kinematic, not tuned, vs the F74 scalar's tuned g>g_c); the full interacting two-body wavefunction (relativistic Bethe–Salpeter, F74 scope) remains open.

| 215 | F169 photon interacting two-body wavefunction: photon = marginally-bound THRESHOLD state of the relative-coordinate contact problem; ψ(p)∝1/(E0−T) exact E=0 secular root at g_c (residual 0), normalizable in 3D; T(0)=ω⁺(0)+ω⁻(0)=0 ⇒ masslessness inherited from gapless constituents; secular=dense diag to 5.6e-14; Ω_even−T=O(k²), slope→1/√3; RMS pair radius ≈1.91 |

Test: `tests/findings/test_F169_photon_bound_state.py` (6/6). Module `casim.engine.gauge.photon_bound_state`. See `findings/F169-photon-interacting-two-body-wavefunction.md`. Builds the interacting wavefunction F69/F74/F168 deferred; masslessness inherited (not tuned), F69 even law = leading small-k threshold. Remaining external input = binding coupling value (criticality g_c, same as F74); all-k gauge-pole proof + relativistic Bethe–Salpeter still open.

| 216 | F180 gravitational-wave equation from the rotation rule: coefficient identity 8πG/c⁴=a²c_lat/(ħc) and 1/G=8π√3·ħ/(a²c³) sympy-exact (residual 0); induced inverse-coupling carries 1/c_lat=√d to 7e-16 (d=1,2,3); induced graviton self-energy Π(q) depends only on the constituent invariant c_lat²\|q\|²−q₀² (isocontour spread 2.2e-5, naive-isotropic control 0.27) ⇒ light cone q₀=c_lat\|q\|; graviton/photon slope identical (=c_lat, exact) ⇒ \|c_grav−c_photon\|/c=0, GW170817 residual ≤3e-83≪1e-15; real-space D-GW wavefront 1.03·c_lat (grid), static limit = F106 Poisson (8.6e-4) |

Test: `tests/findings/test_F180_gw_speed.py` (5/5; A,B exact, C inheritance, D exact slope, E grid). Module `casim.engine.forks.gravity.gr_fork_F180_gw_speed`. See `findings/F180-gravitational-wave-speed.md`. Closes audit-2026-06-29 C1: the gravity sector has a hyperbolic equation (∇²−c_lat⁻²∂t²)lnK=−(8πG/c⁴)T⁰⁰ whose speed c_grav=c_lat is forced (F79 zero tree stiffness ⇒ induced kinetic term = matter vacuum polarization, light cone inherited), not a free knob (D-EM8's c_g). TT-tensor graviton + native high-res wavefront open.

| 219 | F183 black hole under F178 (Schwarzschild/Kerr): horizon 2M, photon sphere 3M, shadow b_c=3√3 M, ISCO 6M, κ=1/4M (exact closed forms, numeric photon-sphere solve <1e-3); Hawking T=ħc³/8πGMk_B present (6.17e-8 K/1M_sun, T∝M⁻¹, lifetime∝M³); eikonal QNM Ω_c=λ=1/3√3 M exact, eikonal real → tabulated GR (28.8%→3.2%, ℓ=2→6), damping 8.2%; Kerr horizons M±√(M²−a²), ergosphere 2M, Ω_H=a/(r₊²+a²), prograde<6M<retrograde ISCO; OS collapse horizon + finite τ=π√(R₀³/8M); lattice core r_core=(48 r_g² a⁴)^{1/6}∝M^{1/3} | GR closed forms + scaling | exact (geometric) / quantitative | F183; `test_F183_blackhole.py` (2026-06-30 - 03:15) |

Test: `tests/findings/test_F183_blackhole.py` (8/8). Module `casim.engine.interactions.blackhole`. The canonical strong-field object is exact Schwarzschild/Kerr (replacing the F114 dielectric BH); the one non-GR feature is the lattice-regulated core. See `findings/F183-blackhole-under-full-tensor.md`.

| 220 | F184-F192 gravity-sector scenarios (catalog build-out): exact/closed-form pieces — F186 geodesic b_c=3√3 M (numeric to <1e-3); F189 chirp df/dt∝f^{11/3} and Mc=m/2^{1/5} (exact); F190 per-horizon-cell entropy s=a²/4ℓP²=2π√3 nats and area law S∝M² (exact); F192 vacuum w=-1 ⇒ ρ+3p=-2ρ (exact sign). Quantitative: F184 SLy M_max=2.08/R(1.4)=11.1; F185 I/MR²=0.31; F187 WKB QNM <7%; F188 z_eq=3430/age=13.8 Gyr; F191 bullet-cluster lensing offset | mixed closed-form + quantitative | exact pieces 0; quantitative in-band | F184-F192; `test_F18{4..9}_*.py`, `test_F19{0..2}_*.py` (2026-06-30) |

Findings F184-F192 (scenario catalog). Modules `ca_ns_eos.py`, `ca_rotation.py`, `ca_raytrace.py`, `ca_qnm.py`, `ca_cosmology.py`, `ca_inspiral.py`, `ca_horizon_entropy.py`, `ca_darkmatter.py`, `ca_vacuum_energy.py`. 27/27 checks. See `docs/roadmaps/gravity-sector-scenarios-2026-06-30.md`.

| 221 | F193 CA-native ontic vacuum gravitates as zero (closes F164 candidate (i)): the beable field-energy density on the empty BCC lattice is exactly 0 ⇒ F64 dielectric K=1, G_μν=0 (bare CC=0 in the ontology, removing both the F164 magnitude and its wrong sign); the +½ħω template sum (=F164 ρ_vac=3.46e111 J/m³) is a superimposable that does not source the beable dielectric. Residual ρ_Λ as holographic IR back-reaction: ρ_vac·(a/R_H)²=2.06e-9 vs observed 6.0e-10 J/m³ (factor 3.4, Δlog₁₀=0.54); CKN c⁴/(8πG R_H²)=2.53e-10 (0.42×). Obstruction = the dilution exponent p=2 (imported from CKN, not derived) | exact (T⁰⁰_vac=0, K=1 structural) + computed coincidence | T⁰⁰_vac=0 / K−1=0 exact; residual 0.54 dex | F193; `test_F193_ontic_vacuum.py` (4/4; 2026-06-30 - 17:35) |

Test: `tests/findings/test_F193_ontic_vacuum.py` (4/4). Module `casim.engine.forks.gravity.gr_fork_F193_ontic_vacuum`. Turns F164 candidate (i) from a position into a derivation (Part A exact) + names the residual obstruction (Part B, holographic). See `findings/F193-ontic-vacuum-gravitates-as-zero.md`.

| 222 | F196 holographic dilution exponent p=2 DERIVED (closes F193 obstruction): rho_grav(L)=M_Schw(L)c²/V(L)=3c⁴/8πG L² ⇒ d ln rho/d ln L=−2.0 exact, p=3(volume)−1(Schwarzschild M∝R, F183). Independent route: F190 horizon-area Bekenstein dof (N∝R²) × Gibbons-Hawking equipartition (ħc/2πR per dof) ⇒ identical 3ħc/8πℓP²R_H²=3c⁴/8πG R_H² (identity ħc/ℓP²=c⁴/G). Both = rho_crit=3H²c²/8πG=7.58e-10 J/m³, 0.10 dex from observed 6.0e-10; residual = Ω_Λ≈0.69 (coincidence). Statistical √N route p=3/2 excluded (+30.6 dex). cell-vs-nat factor = F190 2π√3 | exact (slope −2, route identity) + computed (0.10 dex) | p=2 exact; saturation 0.10 dex | F196; `test_F196_dilution_exponent.py` (5/5; 2026-06-30 - 18:10) |

Test: `tests/findings/test_F196_dilution_exponent.py` (5/5). Module `casim.engine.forks.gravity.gr_fork_F196_dilution_exponent`. Derives the p=2 exponent F193 imported from CKN, via two independent model-native routes (F183 black-hole bound + F190 horizon entropy), reducing the F164 residual to the Ω_Λ coincidence factor. See `findings/F196-dilution-exponent-derived.md`.

| 223 | F199 angular self-duality $C/\lvert B\rvert=1/(2\cos\tfrac23)=0.63622$ NOT derivable (forced posit, 3 grounds): (A) anchor exact — massless Koide ⇒ $3\delta=\pi/4$ ($\delta=\pi/12$, $\cos3\delta=1/\sqrt2$, sympy); (S1) $Q=\tfrac13+\tfrac16r^2$, $\partial Q/\partial\delta\equiv0$ exact ⇒ no F92-analogue second relation ($Q$ radial, $3\delta$ angular, orthogonal); (S2) cubic $B$=sea loop $O(\alpha^0)$ vs sextic $C=\lambda_6e^6$ induced $O(\alpha^{\ge1})$ ⇒ $\alpha_\text{eff}$ does NOT cancel, $C/\lvert B\rvert$ computed; bare Fierz $\tfrac29\to0.582$, needs $1.094\times$ IR factor; (S3) BPS wall degeneracy $(2C-\lvert B\rvert)^2/4C$ at $C/\lvert B\rvert=\tfrac12\neq0.636$ exact. Data sits at self-dual to $1$e$-5$ ($0.89\sigma$), not $2/\pi$ ($4$e$-4$ off); derivation off both by $9\%$ | exact negatives (S1/S3 sympy, A sympy) + computed (S2) | $\partial Q/\partial\delta$, $\pi/4$, $\tfrac12$ threshold exact; $C/\lvert B\rvert$ computed | F199; `test_F199_angular_self_duality_derivation.py` (5/5; 2026-06-30 - 18:52) |

Test: `tests/findings/test_F198_angular_self_duality_derivation.py` (5/5). Analysis-only (sympy + real arithmetic, no chiral transforms). Completes the F176/F177/F179 arc: the lepton-shape angular self-duality is a forced posit, proven non-derivable by three independent structural no-gos, with the $\pi/4$ massless anchor recovered exactly. The one residual is the shared IR coupling $\alpha_\text{eff}^*$ (F124/F144/F145/F151/F152). See `findings/F199-angular-self-duality-derivation-forced-posit.md`.

| 224 | F200 end-to-end induced-coupling computation of C/\lvert B\rvert (`ca_eg_sextic_coupling.py`): full-BZ sea cubic \lvert B\rvert=0.0486 at saturation (1.78× leading, B<0); sea's own sextic C6=−0.018<0 (anti-brake ⇒ C induced, F118 B1); α_eff* recomputed end-to-end [0.376,0.411] mean 0.394 (F152/F154); DERIVATION: λ₆=(2/9)c per-order Fierz, c=1.10⇒0.244 vs F118 independent fit 0.243 (0.6%); C/\lvert B\rvert=(2/9)c e⁶/\lvert B\rvert=0.69 central, band [0.47,0.75] over c∈[0.75,1.20] brackets both self-dual 0.63622 and 2/π; cannot discriminate (residual 20% ≫ split 4e-4) ⇒ computed number, residual = single O(1) quartic c | computed (full BZ + gap solve) + exact rational (λ₆/c=2/9) | C/\lvert B\rvert computed 0.69(central); λ₆=(2/9)c exact-rational reduction | F200; `test_F200_eg_sextic_coupling_computation.py` (5/5; 2026-06-30 - 20:38) |

Test: `tests/findings/test_F200_eg_sextic_coupling_computation.py` (5/5). Module `casim.engine.particles.eg_sextic`. Builds and runs the saturated-condensate induced-coupling calculation F199 pointed to: assembles C/|B| from full-BZ B, saturation e⁶, end-to-end α_eff*, and the induced λ₆=(2/9)c; lands at 0.69 (central), reducing the residual to the single O(1) E_g quartic c. See `findings/F200-eg-sextic-coupling-computed.md`.

| 225 | F195 fully stable block-spin atom for a general element (Z,N) (`element_atom` channel): generalises F160 two-grid H to A=Z+N nucleon fine patch → +Z coarse point (Tier A) + Z-orbital coarse cloud with live Hartree mean field and Gram–Schmidt Pauli. Certified H/He/Li/C: net charge ≡0 (≤2.2e-16, integer Z·(+1)+Z·(−1)); norms 3e-15..7e-16 (split-step exactly unitary); Pauli max⟨i\|j⟩ ≤3.5e-15; cloud RMS bounded over ≥300 ticks (reldrift 0.02–0.14), free control disperses 2.3–5.6×; represented a₀/r_nuc 4.5–5.1 decades (b=30000). Tier B He: 12 live quark_dirac, +Z=2.000 from rho_em, loop-live ‖J_em‖=6.6, cluster bounded (NN OBE binding not wired ⇒ ~50% breathe) | exact (net charge integer, norms unitary, Pauli GS) + Tier-3 bounded radii | net charge/norms/overlap machine-precision; radii/scale Tier-3; absolute fm/eV P6-gated (F123) | F195; `test_F195_blockspin_element_atom.py` (9/9; 2026-06-30 - 22:10) |

Test: `tests/findings/test_F195_blockspin_element_atom.py` (9/9). Module `src/casim/particles/channel.py` (`ElementAtomChannel`, `AtomStabilityReadout`). Scenarios `scenarios/stable_atom_{helium,lithium,carbon}.yaml` + `_free` controls. Generalises the F160 live two-grid hydrogen atom to a general element (Z,N): multi-nucleon fine patch → +Z coarse point, multi-electron coarse cloud with live Hartree + Gram–Schmidt Pauli. See `findings/F195-blockspin-element-atom.md`.
| 226 | F206 Tier-B inter-nucleon NN one-boson-exchange binding (`ElementAtomChannel._setup_nn_potential`/`_apply_nn_binding`): the model NN OBE V_pair=σ(F126)+ω(F128)+quark-Pauli core(F113)−V0·π-tensor(F104), V0 fixed to the model deuteron (E_b=2.234 MeV ⇒ V0=167.7 MeV, well min −49.1 MeV), applied as an exactly-unitary η↔χ scalar-mass (F136) rotation between live nucleon COMs. Certified deuteron + He-4: norm drift 9.4e-14, net charge Q=1.0000/2.0000 (<1e-12); deuteron sep 4.75→2.56 cells (ON) vs 4.02 (OFF), saturates (<2% late variation); g=0.03 settles WIDER (2.77) than g=0.012 (2.56) ⇒ equilibrium set by the F113/F128 repulsive core; He-4 COM-RMS 0.61 (ON) vs 1.07 (OFF) | exact (scalar-mass rotation unitary, charge integer) + Tier-3 bounded equilibrium | norm/charge machine-precision; equilibrium separation Tier-3 (qualitative core-limited bound); absolute fm/MeV P6-gated (F123) | F206; `test_F206_internucleon_nn_binding.py` (6/6; 2026-06-30 - 23:40) |
| 227 | F208 relativistic (F125 Dirac–Coulomb) ionization energies in the multi-electron SCF (`ca_manybody.electron_cloud_hartree(relativistic=True)` + `_scalar_relativistic_shift_Ha`): scalar mass-velocity+Darwin O((Zα)⁴) shift ΔE=−(Z_eff⁴α²/2n⁴)(C(n,l)−¾), C(n,0)=n / C(n,l≥1)=n/(l+½), Z_eff=n√(−2ε). Reproduces F125 H 1s shift −α²/8 Ha=−0.181 meV EXACTLY; Z=1–20 IE sweep vs CRC/NIST: H +0.0%, He −2.5%, then −15..−40% from Li on (mean 27.7%, max 39.4% P) — underbinding ⇒ exchange-correlation (Hartree+Koopmans) ceiling, NOT relativity; valence rel shift <0.6 meV all H→Ca; 1s core shift −0.6(Ne)→−4.3(Ar)→−5.7(Ca) eV, log-log slope 3.38≈Z⁴ | exact (H 1s shift identity, C(n,l) factor) + quantitative (IE map vs CRC/NIST) | H-shift machine-exact; IE accuracy Hartree-tier (~28% underbind, XC-limited); grid ~1% (light) | F207; `test_F208_relativistic_scf_ie.py` (7/7; 2026-07-01 - 00:30) |

| 228 | F207 Casimir effect (`ca_casimir.py`): C2 EM force/energy reproduced EXACTLY from the F69 photon — Abel–Plana reduction of the perfect-plate mode sum = $-\pi^2c/1440L^3$ (scalar) using ONLY the exact IR dispersion $\Omega_\text{pair}\to c\lvert k\rvert$ (F69-PP3) ⇒ $F/A=-\pi^2\hbar c/240L^4$, $E/A=-\pi^2\hbar c/720L^3$ (force ratio $<$1e-12); EM$=2\times$scalar exact (F69 non-birefringence). C1 `sin` machinery $-\pi c/24L$ to 3.5e-5; cubic-axis $\Omega_\text{pair}$ exactly linear ⇒ zero axial Casimir term (exact). C3 bending $\beta_\text{axis}\approx0$/$\beta_\text{body}\approx-6.6$e-3 ⇒ correction $\sim\beta(a/L)^2$. G1 $\Delta m=E_C/c^2$ EXACT (Gauss-law closure of $\nabla^2\ln K=-8\pi T^{00}$) but degenerate with SEP buoyancy (Archimedes can't discriminate — honest negative). D1 DCE pair emission $n_a=n_b$ residual 0 (two-mode squeezing). C4 Jaffe $\delta$-mirror: $E\to0$ as coupling$\to0$ (source channel) | exact-algebraic (C2 closed form, G1 Gauss, D1 pair, axis-linear) + computed (C1, C4) | $F/A=-\pi^2\hbar c/240L^4$ & $\Delta m=E_C/c^2$ exact; $\beta$/lattice-coeff O((a/L)²) bounded | F207; `test_F207_casimir.py` (6/6; 2026-06-30 - 21:32) |

Test: `tests/findings/test_F207_casimir.py` (6/6). Module `casim.engine.interactions.qed_casimir`. Confronts the measured Casimir force with the model's derived constraints (F69/F26/F107/F178/F193); the force is reproduced exactly in the source/H_int channel (Jaffe/Nikolić consensus), consistent with F193 (homogeneous zero-point sum is a non-gravitating superimposable); the Casimir shift gravitates as beable binding energy but is Archimedes-degenerate with SEP buoyancy. See `findings/F207-casimir-effect-source-channel-and-gravitation.md`.

| 229 | F209 modulated Casimir — does time-modulation break the F207-G1 beable-vs-SEP degeneracy? (`ca_casimir.py` new time-dependent fns): **NO, degeneracy structurally forced.** M1 Archimedes η(t) modulation — beable weight (Gauss closure of ∇²lnK=−8πT⁰⁰) vs SEP buoyancy weight computed by INDEPENDENT formulas coincide in time domain AND every Fourier harmonic (residual 0) for f∈{1,3.7,1000}Hz × depths, signal genuinely modulating (∼4.7e-24 N) ⇒ degenerate to ALL orders (same weak-field eqn, F178/F180 PPN β=γ=1). M2 mechanism: the beable-vs-template split lives ENTIRELY in the homogeneous offset ρ0, which cancels EXACTLY in a tared/differential weighing for arbitrary ρ0 (incl. F164 bare 3.46e111) ⇒ the discriminating quantity is unweighable by construction. M3 DCE: radiated beable E_rad=ħΩ_d sinh²(gt) gravitates as E_rad/c² = drive-supplied SEP weight (residual 0); template-change=beable-change=E_rad ⇒ DCE degenerate (energy is drive work, NOT liberated offset; ≠ un-renormalising the CC). M4 signals ≈4.7e-24 N (Archimedes) / ≈7.4e-36 N (DCE) — degenerate AND unweighable. Sharpens F193 caveat: split not lab-accessible via Casimir at ANY order (forced at zeroth order = definition of observable) | exact-algebraic (M1 all-harmonic residual 0, M2 offset cancel, M3 DCE residual 0) + computed (M4 realism) | degeneracy/offset-cancel/DCE exact; O((a/L)²) lattice coeff (F207) still the only non-discriminating Casimir signature | F209; `test_F209_modulated_casimir.py` (4/4; 2026-07-01 - 01:20) |

Test: `tests/findings/test_F209_modulated_casimir.py` (4/4). Module `casim.engine.interactions.qed_casimir` (time-dependent additions; F207 statics reused). Extends F207 G1 (static, degenerate) to the modulated regimes named in the build brief: Archimedes reflectivity switching and dynamical-Casimir pair emission. Both stay degenerate with SEP/template — the beable-vs-template split is not lab-accessible via Casimir at any order, because every weighable quantity is an energy change (beable in both pictures) and the discriminating homogeneous offset cancels differentially. See `findings/F209-modulated-casimir-beable-template-degeneracy.md`.

## F210 — electrical superconductivity (electric S-dual of F86) (2026-07-01)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 230 | BCS universal gap ratio $2\Delta(0)/k_BT_c=2\pi/e^{\gamma}=3.5277539777$, coupling- AND $\omega_D$-independent (crown jewel: parameter-free ⇒ not a fit); gap eq. is the F77 NJL gap $\Delta=\omega_D/\sinh(1/N(0)V)$ | machine | ratio residual $3.8\times10^{-16}$ ($N(0)V{=}0.05$); $\omega_D$-independence $<10^{-15}$; gap-eq closed form solves $1=N(0)V\operatorname{arcsinh}(\omega_D/\Delta)$ to $10^{-14}$ |
| 231 | BCS specific-heat jump $\Delta C/C_n=12/(7\zeta(3))=1.4261269$; near-$T_c$ slope $\Delta^2(T)\to\tfrac{8\pi^2}{7\zeta(3)}(k_BT_c)^2(1-T/T_c)$ | machine + numeric | jump residual $<10^{-9}$; slope ratio $\to1.0000$ ($0.9998$ at $1-T/T_c=2\times10^{-4}$) |
| 232 | Cooper pair = charged spin-0 $s$-wave singlet: charge $=2e$ exact (F87 integer holonomy), phase winding $=2$ (F69 sum) ⇒ $\Phi_0=h/2e$ | exact | charge/winding integer-exact |
| 233 | Meissner = Stueckelberg (F44/F34b) photon mass: $\omega^2=m_\gamma^2+(c_\text{lat}k)^2$ reduces to luminal even F69 photon at $m_\gamma{=}0$; $\lambda_L(2e)/\lambda_L(e)=1/2$; $B\sim e^{-x/\lambda_L}$ | exact + numeric | $m{=}0$ reduction $<10^{-15}$; $\lambda$ ratio $<10^{-12}$; London BVP $\lambda$ residual $1.9\times10^{-6}$ |
| 234 | Flux quantum $\Phi_0=h/2e=2.0678\times10^{-15}$ Wb $=\tfrac12(h/e)$ (carriers are pairs); Josephson DC $I=I_c\sin\Delta\theta$, AC $f_J=2eV/h$ | exact + machine | $\Phi_0$ exact; $h/e$ ratio $2.0$; $f_J$ residual $<10^{-10}$ |
| 235 | Zero DC resistance: London eq. 1 with $E{=}0\Rightarrow\partial_tJ_s=0$ (persistent current); normal Drude control decays | exact | drift $=0.0$; normal $J\to<10^{-20}$ |

Test: `tests/findings/test_F210_superconductivity.py` (16/16). Module `casim.engine.interactions.superconductivity`. Superconductivity is the electric S-dual of the F86 magnetic dual-superconductor; bare fundamental lattice does NOT superconduct (repulsive channel + graviton-only glue) ⇒ emergent-lattice phenomenon. See `findings/F210-electrical-superconductivity.md`.

## F211 — T_c magnitude from real superconductors (2026-07-01)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 236 | Allen-Dynes-dressed F210 gap eq. reproduces measured T_c of Al/Sn/In/Ta/Nb/Pb/Hg fed literature (λ,μ*,ω_log): Pb 0.1%, Ta 0.3%, Sn 4.9%, Hg 6.1%, Nb 10.9%, mean 14.3%; f₁f₂ → Pb 7.5 K (exp 7.19), Hg 4.07 K (exp 4.15) | numeric | mean rel err 14.3%; strong-coupling few-% |
| 237 | Task-1 kernel V=D²/(ρc_s²) in Hopfield form λ=η/(M⟨ω²⟩) reproduces tabulated λ: Nb 1.01, Al 0.42, Ta 0.69, Pb 1.56 | numeric | <5% |
| 238 | BCS T_c prefactor 2e^γ/π = 1.134 = the F210 universal-gap-ratio constant (T_c and gap share one origin) | machine | <10⁻³ |
| 239 | Weak-coupling BCS overestimates T_c for every element (omits (1+λ) mass renorm + retarded μ*); Allen-Dynes (Eliashberg dressing of the same gap eq.) fixes it | numeric | all-over + AD-closer, exact logical |

Test: `tests/findings/test_F211_tc_real_materials.py` (5/5). Module `casim.engine.interactions.superconductivity`. Closes the F210 "absolute T_c" open item to Eliashberg accuracy; remaining first-principles step = derive the Hopfield η from the F64 dielectric strain response. See `findings/F211-tc-magnitude-real-superconductors.md`.
| 240 | F212: product state → exchange(π/8)=exp(−iθσ_A·σ_B) entangler drives reduced-DM entropy S: 0 → ln2 (maximally entangled Bell output from a product input; perfect entangler) | machine | residual 8e-16; sweep vs analytic S(θ), p=cos²2θ, <10⁻¹² |
| 241 | F212: mean-field/Hartree substrate cannot host the generated entanglement — best single-product fidelity to the Bell state = 1/2 (exact); time-dependent Hartree keeps S=2.2e-16; entropy gap = ln2 | exact + machine | Schmidt λ_max=½; ties to ca_manybody being product-ansatz |
| 242 | F212: SWAP=(I+σ_A·σ_B)/2 exact; native 3-qubit |+00⟩→exch(0,1),(1,2) generates genuine tripartite entanglement (all cuts>0); GHZ cuts=ln2 | machine | norm 1 to 10⁻¹²; engine entropy readout validated |

Test: `tests/findings/test_F212_entanglement_generation.py` (5/5). Module `casim.engine.interactions.qi_entanglement`. Realises the genuine-QCA reading of the quantum-computing cross-test: the substrate generates entanglement entropy it is not given, and the exponential 2ⁿ Hilbert space is irreducibly present. See `findings/F212-dynamical-entanglement-generation.md`.

## F213 — first-principles Hopfield η + mass renormalization / gap ratio (2026-07-01)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 240 | Deformation potential D=(2/3)E_F from F64 dilation (rotation-rate energy scale ∝ n^{2/3}); needs only electron density | exact | D=(2/3)E_F to <10⁻¹²; E_F(Al)=11.67 eV from density |
| 241 | λ = N(0)D²/(ρc_s²) = N(0)·V_Task1 (loop closure F210→F211→F213; λ∝D²) | exact | scaling residual <10⁻¹² |
| 242 | Bare jellium λ overestimates free-electron Al/Na by consistent ~2.5× (Al 2.36, Na 2.89) — textbook jellium overestimate; reconciled by screened D (Al 5.1, Na 1.3 eV) via F64 dielectric | numeric | consistent to \|Δover\|=0.53; screened D physical |
| 243 | Mass renormalization Z=1+λ (1.43 Al → 2.62 Hg): the factor weak-coupling BCS omits (F211 overestimate) | exact | Z=1+λ |
| 244 | F210 gap ratio 3.528 is weak-coupling limit; strong-coupling 2Δ/kTc rises (Pb 4.38, Hg 4.60), reproduced to ~3% by 3.528[1+12.5(Tc/ωlog)²ln(ωlog/2Tc)]; correlates with Tc/ωlog r=0.989, with Z r=0.998 | numeric | mean gap-ratio err ~3%; corr 0.99 |

Test: `tests/findings/test_F213_hopfield_and_gap_renormalization.py` (7/7). Module `casim.engine.interactions.superconductivity`. Closes F211 approximations: derives λ from F64 deformation potential (free-electron metals, jellium accuracy) and scopes the Eliashberg Z(ω) extension that fixes the mass renormalization (retarded kernel already present in F210 Task 1). See `findings/F213-hopfield-firstprinciples-and-gap-renormalization.md`.
| 243 | F214: super-exchange J=½(√(U²+16t²)−U) from ca_dirac hopping t(m) [measured, 1 tick] + gap U=2arcsin(m); closed-form == exact two-site Hubbard S_z=0 diagonalisation | exact-algebraic | <10⁻¹²; →4t²/U at large gap (1.4% at m=0.9) |
| 244 | F214: derived per-tick entangling angle θ=J/4 ⇒ Bell time τ=π/(2J); m=0.5 → τ=7.004 ticks | exact + numeric | rate is a lattice prediction, no free knob |
| 245 | F214: LIVE casim entanglement_register channel — product Néel init S=0 → derived exchange generates S→ln2 at the derived tick 7 (0.6931469 vs ln2 0.6931472, discrete-tick err 3.3e-7); norm 1 to 10⁻¹²; checkpoint/resume bit-identical | quantitative + machine (norm/ckpt) | first live 2ⁿ many-body sector; 3-qubit tripartite; |00…⟩ control S=0 |

Tests: `tests/findings/test_F214_live_entanglement_superexchange.py` (6/6). Modules `casim.engine.interactions.qi_entanglement`, `src/casim/engine/manybody.py`. Derives the F212 entangler's coupling from the ca_dirac hopping and wires genuine multi-cell entanglement into the live engine. See `findings/F214-superexchange-and-live-entanglement-channel.md`.

## F215 — imaginary-axis Eliashberg solver on the F210 kernel (2026-07-01)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 245 | Eliashberg mass renormalization Z(iω₀)→1+λ emerges dynamically (Al 1.42/1.43 … Pb 2.41/2.55) from coupled (Z,Δ) on F210's single-Einstein-mode kernel | numeric | worst 8% (ω₀=πT≠0) |
| 246 | (1+λ) fix: Eliashberg T_c suppressed to 0.16–0.24× naive BCS (Pb 7.6 K vs 32 K, exp 7.19) — resolves the F211 BCS overestimate dynamically | numeric | all <0.4×; Pb 0.24× |
| 247 | Dynamic T_c from (λ,ω_E,μ*), NO McMillan/Allen-Dynes fit, reproduces 7 elements at corr r=0.975 (single Einstein mode ~27% high = known artifact) | numeric | r=0.975; mean err 27% |
| 248 | Linearized T_c eigenvalue ρ(T) monotone through 1 at T_c (Pb: 1.35 @0.7Tc, 1.000 @Tc, 0.78 @1.4Tc) | numeric | \|ρ(Tc)−1\|<10⁻³ |

Test: `tests/findings/test_F215_eliashberg_solver.py` (5/5). Module `casim.engine.interactions.superconductivity`. Builds the Eliashberg extension F213 scoped: mass renormalization Z=1+λ + T_c suppression recovered dynamically on the F210 retarded kernel; supersedes the F211 fit. Remaining = distributed α²F(ω) from Task-1 kernel + F130-134 phonon DOS. See `findings/F215-eliashberg-solver.md`.
| 246 | F217: Jordan–Wigner fermions on a lattice chain — {c_i,c_j†}=δ_ij, {c_i,c_j}=0 to machine zero; Pauli exclusion exact (|↑,↓⟩ double-occ=0, ⟨S·S⟩=−¼) | exact/machine | 0.0 anticommutator residual |
| 247 | F217: full 2nd-quantized two-site Hubbard singlet–triplet gap == F214 closed form ½(√(U²+16t²)−U) — super-exchange J EMERGES from second quantization | exact-algebraic | <10⁻¹² (worst 4.7e-16), all m |
| 248 | F217: large-U limit → F212/F214 exchange gate — peak two-site spin entanglement → ln2 (0.693147 at m=0.98), doublon leakage 0.127→0.002; live casim fermion_chain channel S:0→0.692, checkpoint/resume bit-identical | quantitative + machine | finite-U correction = charge fluctuations |

Tests: `tests/findings/test_F217_field_native_fermion_entanglement.py` (5/5). Modules `casim.engine.particles.second_quant`, `src/casim/engine/manybody.py`. Makes the model's entanglement field-native (genuine antisymmetrised Fock space); the F214 effective spin model is the large-U limit. See `findings/F217-field-native-fermion-entanglement.md`.

## F218 — first-principles alpha^2F + Padé dynamic gap ratio (2026-07-01)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 249 | First-principles Eliashberg spectral function α²F(ω)=λω²/ω_max² (F213 deformation potential + acoustic FS phase space); weight normalizes to λ; Matsubara kernel λ(ν)=λ[1−(ν²/ω_max²)ln(1+ω_max²/ν²)] closed form | exact + numeric | norm→λ (<10⁻⁴); ω_log=ω_max/√e exact; kernel matches integral <10⁻⁴ |
| 250 | T_c shape-insensitive at fixed ω_log: Debye ≈ Einstein (mean 27.6% vs 27.4%) ⇒ F215 residual is μ* calibration, not spectrum shape; explains single-mode success | numeric | worst Einstein↔Debye Tc diff <8% |
| 251 | Dynamic strong-coupling 2Δ₀/kTc via Vidberg-Serene Padé continuation (no fit): Al 3.56→BCS, rises to Pb 4.6-4.7/Hg 4.7; corr with measured r=0.988 | numeric | r=0.988; Al +1% vs 3.528 |
| 252 | First-principles Debye α²F tightens gap ratio vs Einstein (mean err 6.4%→5.2%) — gap ratio is shape-sensitive where Tc is not | numeric | md 5.2% < me 6.4% |

Test: `tests/findings/test_F218_alpha2F_and_pade_gap.py` (7/7). Module `casim.engine.interactions.superconductivity` (mpmath Padé). Derives α²F(ω) from F213 deformation potential + Padé-continues the F215 Eliashberg gap to the real axis for the dynamic strong-coupling ratio; supersedes the F213 fit formula. Remaining = Morel-Anderson μ* from F64 dielectric (removes calibration residual). See `findings/F218b-alpha2F-firstprinciples-and-pade-gap-ratio.md`.
| 249 | F218: CZ/CNOT compiled EXACTLY from the lattice exchange gate + SU(2) rotors — σ·σ commutes with ZZ, σz⊗I flips XX,YY ⇒ two exchange gates + σz = exp(iπ/4 ZZ); assembled CZ/CNOT vs textbook | exact-algebraic | 6e-16 (constructive universality) |
| 250 | F218: 2-qubit Grover finds every marked item (0..3) with P=1 (direct AND live in the casim quantum_circuit channel); norm conserved; checkpoint mid-algorithm → resume bit-identical | machine | P=1 to <1e-12; Δψ=0 on resume |
| 251 | F218: Deutsch–Jozsa (1 oracle query) classifies all four oracles — constant→P(q0=1)=0, balanced→1 (deterministic) | machine | exact 0/1 |

Tests: `tests/findings/test_F218_algorithm_through_engine.py` (5/5). Modules `casim.engine.interactions.qi_entanglement`, `casim.engine.interactions.qi_algorithms`, `src/casim/engine/manybody.py`. The substrate runs genuine quantum algorithms with a universal gate set compiled exactly from its own exchange interaction. See `findings/F218-algorithm-through-the-engine.md`.
| 252 | F223: graviton–graviton J=2 (D-wave, L=2) bound state in the DERIVED potential V=−Gm²/r (linearised F79/F180 EH action, α_g=(m/M_Pl)²); hand-rolled real tridiagonal inverse-iteration reproduces Coulomb E₃=−m_red α_g²/18 | machine (grid-limited) | rel_err 1.3e-5 |
| 253 | F223: geon virial mass μ≃√N M_Pl → √2 M_Pl≈1.7e19 GeV (N=2); self-binding needs m~M_Pl since frac binding=(m/M_Pl)⁴/36 | order-of-magnitude (virial + Bohr cross-check) | O(1) |
| 254 | F223: ν_R ν_R→J=2 no-go (gravity-only α_g=(M_R/M_Pl)²; max frac binding 1.3e-22 over M_R∈[keV..1e14 GeV]); CGPP relic exp(−2πμ/H)-suppressed ~10^5 orders (μ/H_inf~3e5) ⇒ Ω_grav≪0.12, needs PBH-remnant/preheating (tunable) | exact-algebraic (no-go) + order-of-magnitude (relic band) | E_b/M_R≤1.3e-22 |

Tests: `tests/findings/test_F223_spin2_binding_relic.py` (6/6 checks, 5/5 test fns). Module `casim.engine.forks.gravity.gr_fork_F223_spin2_binding_relic`. Closes F216 §6: the massive spin-2 DM bound state binds (graviton–graviton geon, μ≃√2 M_Pl) or is a clean no-go (ν_R ν_R); passes the full DM data battery; the residual is the tunable production abundance. See `findings/F223-spin2-bound-state-binding-and-relic.md`.

| 255 | F226: geon stability gate — Hawking evaporation halts at the F190/F107 one-cell horizon ⇒ stable Planck-mass remnant M_rem=(√3/2)^{1/2} M_Pl≈0.9306 M_Pl (N_cells=2(M/M_Pl)²/√3=1) | exact-algebraic (F190 area law + F107 cell) | N=1 to 1e-12 |
| 256 | F226: CGPP Bogoliubov |β|² via hand-rolled real 2-component RK4 vs exactly-solvable Bernard–Duncan closed form (ω²=A+B tanh ρη) | machine-precision-validated | rel_err 1.0e-12; \|α\|²−\|β\|²=1 to ~1e-12 |
| 257 | F226: geon production — CGPP/UV-freeze-in/coalescence all exp-forbidden (μ≫ all scales, μ/H_inf~μ/T_RH~2.9e5 ⇒ 10^{−1..8×10⁵} suppression); only PBH remnants viable, Ω tuned by β(M_form)∝M_form^{3/2}∼10^{−14}..10^{−9} (pre-BBN); geon≡Planck relic (same object) | order-of-magnitude (per-channel + β band) | suppressions 10^{−10⁵}; β<1 |

Tests: `tests/findings/test_F228_geon_production_stability.py` (9/9 checks, 7/7 test fns). Module `casim.engine.forks.gravity.gr_fork_F228_geon_production_stability`. Closes F223 §6: the geon is stable as the F190/F107 one-cell Planck-mass BH remnant; every field-theoretic production channel is exp-forbidden (μ≫ all available scales); PBH remnants are the sole viable route (Ω tunable via β); ontology — geon ≡ Planck relic. Preserves F182/F188 ΛCDM (z_eq≈3430, age≈13.8 Gyr, ΔN_eff≈0). See `findings/F228-geon-production-and-stability.md`.

| 255 | F222: native CCZ (Barenco V=√Z) = diag(1..1,−1) and general native controlled-phase = diag(1,1,1,e^{iφ}), all from exchange+rotors | exact-algebraic | 2.2e-15 / 5.6e-16 |
| 256 | F222: n-qubit Grover (n=3..12) success = analytic sin²((2r+1)arcsin 2^{−n/2}); norm conserved; QFT matches DFT and inverts; BV recovers secret in 1 query; GHZ every-cut = ln2 to n=12 | machine | norm 1.5e-13; QFT 1e-10; BV/GHZ exact |
| 257 | F220: single-qubit field-native fermionic gate exp(−i2θ n̂·S) = abstract su2_rotor on the one-per-site sector (occupation conserved, zero leakage) | exact-algebraic | 8.3e-16 |
| 258 | F220: field-native entangler = genuine Hubbard e^{−iHt}; fidelity to exchange gate → 1 and spin entropy → ln2 as U/t→∞ (Bell on matter); Deutsch–Jozsa verdict correct on all 4 oracles despite sub-% doublon leakage | quantitative (verdict machine) | fid→1.0000; DJ 0/1 |
| 259 | F221: 3-qubit code corrected fidelity = (1−3p²+2p³)+(3p²−2p³)(2ab)² (density-matrix vs closed form); logical infidelity O(p²) | exact-algebraic | 4.4e-16 |
| 260 | F221: 9-qubit Shor code corrects arbitrary single-qubit error (all 27 = {X,Y,Z}×9) to fidelity 1; Kraus channels CPTP ΣE†E=I | exact-algebraic | 4.4e-16 / 1.1e-16 |

Tests: `tests/findings/test_F222_scaled_quantum_algorithms.py`, `test_F220_field_native_execution.py`, `test_F221_noise_error_correction.py` (5/5 each). Modules `casim.engine.interactions.qi_entanglement`, `ca_quantum_algorithms.py`, `ca_second_quant.py`, `ca_quantum_noise.py`, `src/casim/engine/manybody.py`. The QC cross-test is scaled to n≈12 (F222), made field-native on genuine matter (F220), and given decoherence + stabilizer error correction (F221). See findings `F222-scaled-quantum-algorithms.md`, `F220-field-native-execution.md`, `F221-noise-error-correction.md`.

| 261 | F224: super-exchange J(t,U)=½(√(U²+16t²)−U) = two-site Hubbard diagonalisation; →4t²/U (t≪U); dimensionful entangling time 1/(4J)=0.25–50 ms reproduces Trotzky 2008 measured 5 Hz–1 kHz band | exact-algebraic + data-consistency | 2.7e-16 |
| 262 | F224 PREDICTION: at Trotzky symmetric point J/U=0.08, exact gap is −6.93% below textbook 4t²/U (falsifiable refinement) | prediction | −6.93% |
| 263 | F225: doublon leakage d=½(1−1/√(1+(4t/U)²)) = F217 ground-state double occupancy; scales (2t/U)² (log-log slope 1.9997) | exact-algebraic | 5.6e-17 |
| 264 | F225: measured GaAs S-T exchange-qubit leakage 0.13% (Cerfontaine 2020) ↔ model t/U≈0.018 (U/t≈55), standard regime; reproduces form+magnitude, no free parameter | data-consistency | roundtrip <1e-12 |

Tests: `tests/findings/test_F224_qc_si_coldatom.py` (4/4), `test_F225_doublon_leakage_spinqubit.py` (4/4). Module `casim.engine.interactions.qi_qc_si`. Routes 1 & 2 of the QC empirical thread: derived super-exchange + native doublon leakage confront measured cold-atom and quantum-dot data in SI units. See findings `F224-qc-si-coldatom.md`, `F225-doublon-leakage-spinqubit.md`.

## F232 / F230 / F231 — open-derivation attempts L3, E1, E2 (2026-07-02)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 265 | F232 (L3): light-deflection route to pin lattice spacing $a$ is DEGENERATE — canonical $K=e^{2u}$ eikonal coeff $=-4$ exactly, $a$-independent over 47 decades (F107 L4a); scale-invariance theorem: no dimensionless mass-blind observable pins $a$; $G$-match $k^2/(8\pi\sqrt3)\equiv1$ (a scales with $\ell_P$) | exact / negative (degeneracy) | coeff $-4.0$ (resid $1.2\times10^{-7}$); identity $10^{-16}$; mass-independent pin $=$ F79 $a=6.598\,\ell_P$ (dimensionful $G$, not lensing) |
| 266 | F230 (E1): lepton angle $\delta^*=\tfrac29$ rad ($3\delta^*=Q=\tfrac23$) NOT derivable from crystal-field/equipartition geometry — geometry fixes only endpoints (democratic $0$; massless-Koide $3\delta=\pi/4$ exact; equipartition $45°$); interior stopping point is dynamics ($\lambda_6\propto\alpha_\text{eff}^*$); dimensional no-go (radian $\neq$ ratio) | structural / negative (sharpened no-go) | $3\delta^*=Q$ to $2.8\times10^{-5}$ (target, $-0.89\sigma$); endpoint $3\delta=\pi/4$ exact; subsumed by F199 |
| 267 | F231 (E2): $\sin^2\theta_W=\tfrac29$ is the on-shell face of $\tfrac14$, not a rival tree value nor coincidence; exact bridge $8/9=$ [1-loop running $0.927$]$\times$[MS$\to$on-shell scheme $0.965$]$=0.895$; $m_Z/m_W=3/\sqrt7$ | reconciliation / quantitative | $8/9$ decomposition resid $0.67\%$; on-shell $2/9$ vs PDG $-0.44\%$; $m_Z/m_W=3/\sqrt7$ $-0.064\%$ |

Tests: `tests/findings/test_F232_lattice_spacing_degeneracy.py` (5/5), `test_F230_lepton_angle_geometric_nogo.py` (6/6), `test_F231_weinberg_scheme_reconciliation.py` (5/5). Analysis-only (real arithmetic). Executes open-derivation prompts L3, E1, E2: two close negative/degenerate (valid results per House Rules), one reconciles. See findings `F232-lattice-spacing-degeneracy-scale-invariance.md`, `F230-lepton-angle-geometric-nogo.md`, `F231-weinberg-2over9-onshell-face-of-1over4.md`.

## F236 / F237 / F238 — open-derivation attempts D1, D2, D3 (neutrino/dark sector, 2026-07-03)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 268 | F236 (D1): full 3×3 Higgs-free see-saw. Diagonal E_g (Z₃) texture ⇒ light masses = three F47 $M_D^2/M_R$ blocks (masses/hierarchy + F201 keV node DERIVED); but E_g is diagonal-traceless (F93 O1) ⇒ PMNS $=\mathbb 1$ exactly (no-go). Mixing forced onto free second-shell $T_{2g}$ channel (F93 commitment #1); 5 oscillation observables reproducible with 6 inputs ⇒ angles FREE | machine-precision (masses/no-go) + fit/free-input (angles) | $m_\nu=-M_DM_R^{-1}M_D^\top$ resid $\sim10^{-20}$; $\theta_{ij}=0$ to $<10^{-9}°$; 6 inputs / 5 obs |
| 269 | F237 (D2): keV sterile EXCLUDED as 100% DM. Resonant + entropy-dilution cannot thread X-ray line $\wedge$ conservative 3.5 keV Lyman-α at 5.6/7.1 keV (0/154 grid). Anti-correlated levers: X-ray margin $\propto S^{+1}$, Lyman-α floor $\propto S^{-4/9}$ ⇒ no co-improvement. Hand-off to F223/F228 geon; sterile survives sub-dominant | exact-algebraic (scaling no-go) + data-consistency | scaling exponents $<10^{-6}$; best case $+0.78$ dex over X-ray bound (7.1 keV) |
| 270 | F238 (D3): geon relic abundance NOT derivable non-tunably. β(M_form) fixed by Press–Schechter $\beta=\tfrac12\mathrm{erfc}(\delta_c/\sqrt2\,\sigma)$; required $\sigma(k_\text{PBH})\sim0.06$–$0.08$ vs CMB $\sqrt{A_s}=4.6\times10^{-5}$ (~$1.6\times10^6$ boost); scale-invariant ($n_s=1$) spectrum under-produces by ~$2.1\times10^7$ orders; β(σ) monotone (no attractor); no inflaton/spectrum sector ⇒ Ω_DM = free cosmological initial condition. Extends F228 | exact-algebraic (geon side) + order-of-magnitude (PS inversion) + structural (non-derivability) | HZ under-produces ~$2.1\times10^7$ dex; β$<1$ |

Tests: `tests/findings/test_F236_three_generation_seesaw.py` (5/5), `test_F237_kev_sterile_resolution.py` (7/7), `test_F238_geon_relic_abundance.py` (7/7). Modules `casim.engine.particles.majorana`, forks `dm_fork_F237_kev_sterile_resolution.py`, `gr_fork_F238_geon_relic_abundance.py`. Executes open-derivation prompts D1/D2/D3: all three close as sharpened negatives (valid results per House Rules) — masses derived but PMNS free (T₂g); keV sterile excluded as 100% DM; geon abundance a free cosmological initial condition. See findings `F236-three-generation-seesaw-pmns.md`, `F237-kev-sterile-resolution.md`, `F238-geon-relic-abundance.md`.

## F239 / F240 / F241 — open-derivation attempts Q2, Q3, G1 (2026-07-03)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 268 | F239 (Q2): the g_s=½ lattice→MS-bar SCHEME conversion factorises exactly — Λ_MSbar/Λ_rule=1.773 = exp(a₁/2b₀)×(1/q\*a) = 1.299 (V→MS-bar, a₁(6)=11/3 exact, on F151-S1's exact V-scheme lock) × 1.365 (rule→V one-loop = the shared open d₁); α_s(M_Z)=0.1180 once q\* pinned | half EXACT (scheme leg identity, product=full) / half OPEN-bracketed (lattice leg = F162 vertex form factors) | product=full to <1e-12; rule prop-shift ΔB≈0.16× Wilson ⇒ vertex-dominated; bracket q\*a∈[0.577,0.979] ⇒ factor∈[1.33,2.25] (target 1.78) ≪ Wilson 28.81 |
| 269 | F240 (Q3): ω channel from vector sector — KSFR closes with model f_π (m_ρ=√2 g_ρππ f_π), strict-universality g_ωNN²/4π=9·g_ρNN²/4π=25.9 (baryon coherence ×3); full derived OBE (F104 π + F126 σ + F113 core + ω) binds deuteron with NO tuned hard core | Tier-1 (sign, m_ω=m_ρ, ×3 ratio) exact; absolute coupling Tier-B bracket / quantitative | KSFR resid 1.5e-16; ×3 scaling 7e-15; B_d 2.221 MeV (0.1%), r_d 1.978 fm (0.4%); univ overshoots+unbinds ⇒ g_ωNN²/4π∈[5.4,11.1] quenched 0.43× (= F126's 0.45 scalar quench) |
| 270 | F241 (G1): last O(1) CC factor Ω_Λ=0.6847 NOT derivable from F190 area-entropy / F183 BH sector (which fix only the ceiling ρ_crit, Ω=1, dS fixed point); sub-unity value = "why-now" coincidence = 1 − Ω_m (needs cosmic matter fraction, blocked by F197–F199); event-horizon route circular (mispredicts w₀=−0.885); near-hits numerology | structural/exact (ceiling + flatness identity) / machine (event-horizon quadrature) / negative (coincidental-anthropic) | ceiling & 1−Ω_m identity exact; EH quadrature ~1.15 vs analytic ~1.18; not derived to <0.1 dex; p=2 untouched |

Tests: `tests/findings/test_F239_scheme_factor_factorization.py` (3/3), `test_F240_omega_coupling_derivation.py` (10/10), `test_F241_omega_lambda_residual.py` (6/6). Executes open-derivation prompts Q2, Q3, G1: Q2 half-closes (scheme leg exact, lattice leg = shared d₁), Q3 binds the deuteron with a fully-derived OBE (coupling bracketed), G1 closes negative (coincidental/anthropic). See findings `F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1.md`, `F240-omega-coupling-from-vector-sector.md`, `F241-omega-lambda-o1-residual-anthropic.md`.

## F242 / F243 / F244 — open-derivation attempts S1, F1, F2 (2026-07-03)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 271 | F242 (S1): Morel–Anderson μ* DERIVED from the F64 dielectric — its static long-wavelength limit is the Thomas-Fermi screening; FS-averaged screened Coulomb gives μ(r_s)=0.082930 r_s ln(1+6.0299/r_s), then μ*(ω_c)=μ/(1+μ ln(E_F/ω_c)) at the solver cutoff ω_c=6ω_log ⇒ μ*=0.10–0.12 matching empirical with NO fit; Allen-Dynes 7-element error 14.3%→6.3% | closed-form exact (μ(r_s)) + quantitative (μ*, Tc) | μ*∈[0.10,0.12] vs tab 0.10–0.11; AD mean err 6.3%; Eliashberg 27.6%→21.6% (residual = ω_c-window scale, NOT μ*) |
| 272 | F243 (F1): F3 low-density lensing NOT FALSIFIED — depression source stays correct-sign, positive-definite, non-divergent from ρ=1 to 10⁻³, scales linearly (weak-field log-log slope 1.012); no low-density failure | numeric / falsification-survived | slope 1.012 (ideal 1); depression sign holds all ρ; survives to ρ=10⁻³ |
| 273 | F244 (F2): 3-D EMQG lensing obeys Δθ∝1/b on the genuine solve_poisson_3d potential (no free α) — exact continuum closed form Δθ=2GMb/(b²+σ²) slope −0.9959, lattice isolated −1.074, periodic −1.062; Cayley stepper toward-mass, norm 10⁻¹⁵; supersedes the F3b \|Φ\|^α scan | exact-continuum (closed form) + numeric (lattice) + machine (Cayley norm) | closed-form −0.9959; periodic −1.062; norm drift 3e-15 |

Tests: `tests/findings/test_F242_mustar_from_dielectric.py` (5/5), `test_F243_f3_lowdensity_lensing.py` (6/6), `test_F244_emqg_1overb_scan.py` (5/5). Module `casim.engine.interactions.superconductivity` (added `wigner_seitz_rs`, `mu_coulomb_jellium`, `mustar_from_dielectric`); F1/F2 reuse `ca_unified.py`, `ca_emqg.py`, `ca_curved.py`. Executes open-derivation prompts S1, F1, F2: S1 derives μ* (positive, halves Allen-Dynes error; corrects F218's "μ* settles the whole residual" to "only ~6% of it"), F1 retires the low-density falsification target as PASS, F2 confirms 1/b on the physical 3-D potential. See findings `F242-mustar-from-f64-dielectric.md`, `F243-f3-lowdensity-lensing-not-falsified.md`, `F244-emqg-1overb-3d-lensing.md`.

## F250 — the all-k gauge pole of the dual-spinor photon (2026-07-16)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 274 | F250: the F69/F68 paired-photon even-law propagator G(z,k)=(zI−M₆)⁻¹ (M₆=M₂(Ω_pair)⊗I₃) has a single massless transverse gauge pole at ω_freq=±Ω_pair(k) for ALL k in the BZ (not just k→0); residue = transverse rank-2 projector, Ward k·R_T=0; a UNIQUE BZ zero at k=0 (the k/2 sharing folds the Weyl doublers out to \|k\|=2π) ⇒ no gauge doubler | pole location + massless anchor Ω_pair(0)=0 + Ward commutator [M₆,P_T⊗I₂] EXACT (literal 0); residue rank integer-exact; eigenphases / unitarity / completeness / independent-projector MACHINE | GP1 det 1.1e-16 (4000 BZ pts); GP2 =0; GP3 =0; GP4 rank 2/3 exact, Ward 9.3e-17; GP5 4.4e-16; GP6 2.2e-16/1.1e-16; GP7 1 zero at k=0; GP8 7.2e-16 |

Test: `tests/findings/test_F250_allk_gauge_pole.py` (8/8). Analytic proof + verification harness over the audited `ca_photon_pair` even-law propagator and `ca_bcc` walk — no new module. Promotes "the photon is a massless spin-1 gauge boson" from the k→0 reduction to an all-BZ statement; consistent with (and distinct from) F169's O(k²) two-body-floor refinement. See finding `F250-allk-gauge-pole-paired-photon.md`.

## F251 / F252 — the interacting one-loop QED sector (2026-07-16)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 275 | F251: one-loop QED photon self-energy Π^μν = fermion bubble on the F69 paired photon (abelian F162: no ghost, no gauge self-coupling). Ward transversality q_μΠ^μν=0 EXACT; QED beta coefficient b₀^QED=4/3 EXACT (sympy, scalar-bubble calibration g=1, Dirac trace vs explicit γ); lattice b₀=continuum b₀ (subtracted q-flat); leptonic Δα(M_Z)=0.03142 vs PDG 0.03150 ⇒ 1/α(M_Z)\|lep=132.73 (hadronic pull-down to 128.927 deferred to QCD, F151/F152) | Ward + b₀=4/3 EXACT (algebraic); lattice=continuum CONVERGENT; running QUANTITATIVE (leptonic) | P1 literal 0; P2 b₀=4/3; P2b Clifford+trace exact; P3 delta-spread 0.014; P4 0.24% vs PDG |
| 276 | F252: one-loop QED vertex Λ^μ. Ward–Takahashi q_μΛ^μ=S⁻¹(p')−S⁻¹(p) EXACT (fixes Z₁=Z₂); a_e=F₂(0)=α/2π EXACT (Feynman-parameter integral =1) ⇒ 1.16141e-3 vs measured 1.15965e-3 (0.15%); Uehling S-state coeff −4/15 DERIVED from F251 bubble low-q (∫x²(1−x)²=1/30); Lamb shift 2s₁/₂−2p₁/₂ lifts exact Dirac degeneracy (F125) to 1052.2 MHz = 99.5% of measured 1057.845 MHz (residual ~5.6 MHz = higher-order α(Zα)⁵/two-loop) | WT + a_e=α/2π + Uehling coeff EXACT (algebraic); Lamb shift QUANTITATIVE (leading order) | V1 literal 0; V2 param-int=1, 0.15%; V3 −4/15; V4 99.5% |

Tests: `tests/findings/test_F251_vacuum_polarization.py` (5/5), `test_F252_vertex_ae_lamb.py` (4/4). Modules `casim.engine.interactions.qed_vacuum_polarization`, `casim.engine.interactions.qed_vertex_loop`. Closes the F249 Tier-C ledger: C1 (a_e), C2 (running α), C3 (Lamb shift) all flip LEDGER→PASS (`test_F249_qed_comparison_battery.py` now 12/12, 0 ledger items). See findings `F251-qed-vacuum-polarization-running-alpha.md`, `F252-qed-vertex-ae-lamb-shift.md`.

| # | Quantity | Tier | Result |
|---|---|---|---|
| 277 | F253 (E1): weight→phase behind δ*=2/9 rad. 2/9=dim E_g/dim(T_1u⊗T_1u) EXACT (independent O_h projection); measured azimuth =2/9 rad to <0.01%. Equipartition reproduces δ*=2/9 rad EXACTLY given one named posit (POSIT-N: E_g generator unit-normalized ⇒ democratic phase budget=1 rad); without it δ=(2/9)·R scale-degenerate, R=1 not from any O(1) saturation amplitude. Topological route EXCLUDED: only E_g holonomy on BCC 2nd shell =2π/3; 2/9 is a multiplicity not a holonomy, and 2/9 rad ≠ any 2πp/q (q≤24) | 2/9=E_g weight EXACT (algebraic); weight→radian is a NAMED NO-GO (one normalization R); topological escape EXCLUDED | W1 mult_E=1; W2 <0.01%; W3 POSIT-N⇒2/9 exact; W4 no O(1)→R=1; W5 holonomy=2π/3 only |

Test: `tests/findings/test_F253_weight_as_phase_scale_nogo.py` (5/5). Script `casim.engine.particles.derive_weight_as_phase`. Finding `F253-weight-as-phase-scale-nogo.md`. E1 does not close positive but reduces to one normalization constant (the E_g generator norm) and rules out the scale-free topological escape; converges with F179/F199/F230.

| # | Quantity | Tier | Result |
|---|---|---|---|
| 278 | F255 (E1 follow-up): does F118/F234 fix the E_g generator norm R (F253 POSIT-N)? Split into (a) R=1 genuine radian, (b) radian=weight 2/9. **(a) DERIVED**: F118 δ = arg of E_g doublet in the deviation simplex; p_a=√m_a−mean ⊥(1,1,1) to 2.3e-16; E_g irrep metric isotropic (DᵀD=𝟙 to 4.4e-16) ⇒ by Schur the plane angle is canonical, R=1 FORCED (corrects F253 "R free"); geom angle=0.22223=2/9 to 0.003%. **(b) OPEN**: cos3δ*=−B/2C needs λ₆; F234 pins λ₆=0.243 from 2/9 (circular); sea loop excluded (F118 B1/B2); λ₆=1/4 misses 2/9 by ~5% | R=1 DERIVED (Schur, machine-prec); weight-identity CIRCULAR (residual=λ₆) | N1 2.3e-16; N2 4.4e-16; N3 0.003%; N4 λ₆=1/4→5% miss |

Test: `tests/findings/test_F255_generator_norm_from_F118.py` (4/4). Script `casim.engine.particles.derive_generator_norm`. Finding `F255-generator-norm-fixed-by-F118-schur.md`. Answers the follow-up: the solve DOES fix R=1 (Schur); E1's residual sharpens to the single sextic coupling λ₆=0.243 (≈1/4), one number from closure.

| # | Quantity | Tier | Result |
|---|---|---|---|
| 278 | F254 (D1): lattice selector for the PMNS T_2g channel. Under the E_g-stabilizer D_2h, the three axis-mixing amplitudes (t_xy,t_yz,t_zx) transform as three INEQUIVALENT 1-d irreps B_1g⊕B_2g⊕B_3g (distinct zero-sum characters) ⇒ no residual symmetry relates them; democratic point protected by only {±1} (order 2/8) so F92 equipartition inapplicable (triplet split into inequivalent irreps). Democratic/single-channel ansätze miss NuFIT-5.2 NO (462 deg²); only full 3-amp fit reaches data (~1.3e-11 deg), 3 inputs/3 angles no slack. E_g-only PMNS=1 preserved. PMNS angles GENUINELY FREE (three independent D_2h order params; parallel to D3's β) | irrep decomposition EXACT (group theory); equipartition-inapplicability EXACT; one-param no-go NUMERICAL; free-input closure PROVEN | T1 three inequiv irreps; T2 stab order 2; T3 democratic 462 deg² vs full 1.3e-11 deg; T4 PMNS=1 <1e-6 deg |

Test: `tests/findings/test_F254_t2g_pmns_selector.py` (4/4). Script `casim.engine.particles.derive_t2g_pmns`. Finding `F254-t2g-pmns-selector-nogo.md`. Sharpens F236's free-input statement into a stabilizer theorem; D1 mass sector stays derived, mixing is a free three-channel T_2g texture.

| # | Quantity | Tier | Result |
|---|---|---|---|
| 279 | F256 (E1): "derive λ₆=0.243" (E_g sextic clock coupling) is misposed. Two pictures of δ: (I) dynamical minimiser cos3δ*=−B/2C, (II) weight-as-phase δ=2/9 primary. **(I) can't be exact**: B=Dirac-sea cubic (F95, ∝ȳ⁴), C=λ₆e⁶ induced condensate coupling (F150) — independent O(1) origins, no lock ⇒ 3δ*=Q holds only to 1.7e-5 (near-coincidence, sensitivity d3δ/dλ₆=5.2). Required λ₆=0.243 strictly BETWEEN Fierz 2/9 (δ~20% off) and rotor 1/4 (~5% off), matching neither ⇒ no clean number to derive. **(II)** makes λ₆ an output (F234 arrow). Dichotomy: exact E1 closure ⇒ ONLY via weight-as-phase principle (canonical E_g angle=weight, R=1 from F255) | target 3δ*=Q NEAR-COINCIDENCE (1.7e-5) not exact; λ₆ non-rational between 2/9,1/4 (NO-GO); λ₆ derivative in both pictures | L1 1.7e-5; L2 0.243∉{2/9,1/4}; L3 sens 5.2; L4 λ₆ output |

Test: `tests/findings/test_F256_lambda6_sextic_nogo.py` (4/4). Script `casim.engine.particles.derive_lambda6_sextic`. Finding `F256-lambda6-sextic-derivative-nogo.md`. Removes the λ₆/dynamical route as a dead end; with F253 (topological excluded) + F255 (R=1 derived), E1 reduces to the single canonical-angle=weight identity.

## F257 — Bethe logarithm from the model's own hydrogen spectrum (2026-07-20)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 277 | F257: hydrogen Bethe logarithm ln k0(n,l) computed from the model Coulomb resolvent (Dalgarno-Lewis, one tridiagonal solve per energy — no slow state-sum), removing the last literature input in the F252 Lamb shift. ln k0(1s)=2.920, ln k0(2s)=2.748, ln k0(2p)=−0.037 vs accepted 2.984/2.812/−0.030 (~2-3%); below-threshold 1s (for 2p) projected out and added explicitly. Fully model-derived Lamb shift = 1059.9 MHz vs measured 1057.845 (0.2%) | quantitative (uniform-grid O(h), ~2-3%; systematic = continuum/origin representation) | 1s 2.1%, 2s 2.3%, 2p abs 0.007; Lamb 1059.9 MHz (frac 1.002) |

Test: `tests/findings/test_F257_bethe_log_from_spectrum.py` (4/4). Module `casim.engine.interactions.qed_bethe_log` (+ `ca_vertex_loop.lamb_shift_model_bethe`). Removes the one literature constant (tabulated Bethe log) from the F252 Lamb shift, making it fully model-derived. Higher precision (6-digit) needs a log grid / Sturmian basis — noted, not required for the physics point. See finding `F257-bethe-log-from-model-spectrum.md`.

## F258 — One-loop QED electron self-energy Σ(p): δm, Z₂, and Z₁=Z₂ proven (2026-07-22)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 280 | F258: one-loop QED electron self-energy Σ(p)=A p̸+Bm (electron ⊗ paired photon, F87 vertices, F69/F250 internal photon). **Exact (sympy):** numerator γ^μ(k̸+m)γ_μ=−2k̸+4m (d=4); mass shift δm=(3α/4π)m ln(Λ²/m²) — on-shell integral ∫(4−2x)dx=3, prefactor α/4π ⇒ coeff 3/4π; Z₂=1−(α/4π)ln(Λ²/m²) — integral ∫(−2x)dx=−1 — Feynman-gauge Z₁ shares −α/4π ⇒ Z₁=Z₂ log coeff; **differential Ward–Takahashi ∂Σ/∂p_μ=−Λ^μ(p,p)** derived from integrand (d/dp_μ(p̸−m)=γ_μ, d/dp_μ S_F=−S_F γ_μ S_F, exact symbolic inverse) ⇒ Z₁=Z₂ COMPUTED (upgrades F252 assumption); renormalised S_R⁻¹=p̸−m+O((p̸−m)²), residue 1, no leftover divergence. **Convergent:** lattice=continuum, subtracted Δ_A,Δ_B P-flat. **IR:** on-shell Z₂ finite part IR-div (ln μ), regulated, KLN — deferred | δm coeff 3/4π EXACT; Z₂ coeff −1/4π EXACT; Z₁=Z₂ EXACT (differential WT); renorm pole/residue EXACT; lattice=cont CONVERGENT; on-shell Z₂ finite part IR-DIVERGENT (expected) | S1 ∫=3; S2 ∫=−1; S3 WT residual 0 (μ=0,1); S4 residue=1; S5 Δ_A spread 4e-4, Δ_B 8e-5 |

Test: `tests/findings/test_F258_electron_self_energy.py` (6/6). Module `casim.engine.interactions.qed_electron_self_energy`. Finding `F258-electron-self-energy.md`. Completes the one-loop 1PI set {Z₃ (Π, F251), Z₂ (Σ, F258), Z₁ (Λ, F252)} — every Ward identity verified between computed objects; one-loop QED closes.

## F259 — IR sector: soft bremsstrahlung + Bloch–Nordsieck cancellation (2026-07-22)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 281 | F259: eikonal soft-emission factor e(p'·ε/p'·k − p·ε/p·k) reproduced from the F87 identity-channel vertex on an external leg (on-shell Dirac identity ūγ^μ(p̸'+m)=2p'^μū, explicit 4×4 gammas) | exact (sympy, literal 0) | spinor identity 0 for all μ |
| 282 | F259: eikonal current conservation k·J=0 (J^μ=p'^μ/p'·k − p^μ/p·k) ⇒ F250 transverse 2-pol projector sufficient; pol-sum collapse Σ\|ε·J\|²=−J·J | exact (sympy) | k·J = literal 0; collapse exact |
| 283 | F259: soft phase-space ω-integral ∫_μ^ΔE dω/ω = ln(ΔE/μ) (IR log); BCC c_lat=1/√3 cancels from the dimensionless coefficient ⇒ continuum f_IR | exact (sympy) | log verified; c_lat-independent |
| 284 | F259: Bloch–Nordsieck — coeff of ln(μ²) in (σ_virtual+σ_soft)/σ₀ = 0; virtual −(α/π)f_IR ln(−q²/μ²) [F252 F₁ + F258 Z₂] and real +(α/π)f_IR ln(ΔE²/μ²) share f_IR ⇒ μ-independent, finite = 1−(α/π)f_IR ln(−q²/ΔE²) | exact (sympy, literal 0) | ∂/∂μ² = 0; finite form exact |
| 285 | F259: shared IR coefficient f_IR(q²) = ½·(eikonal angular integral); at −q²/m²=10⁴, f_IR=8.217 vs closed ln(−q²/m²)−1=8.210 (leading log ln(−q²/m²)) | quantitative (angular quadrature) | rel err 8e-4 |
| 286 | F259: finite μ-independent O(α) Sudakov observable σ/σ₀=1−(α/π)f_IR ln(−q²/ΔE²); at √−q²=1 GeV, ΔE=100 MeV: O(α)=−0.151, exp(YFS)=0.859; ln(ΔE) is the physical (measurable) part | quantitative | μ-independent; finite |

Test: `tests/findings/test_F259_ir_bremsstrahlung.py` (6/6). Module `casim.engine.interactions.qed_ir_bremsstrahlung`. Finding `F259-ir-bremsstrahlung.md`. The IR-companion to F258: F258's on-shell Z₂ is IR-divergent (same photon-mass μ); its ln μ cancels the real soft emission built here. Makes the one-loop QED sector {F251 Z₃, F258 Z₂, F252 Z₁/F₁} produce physical, finite cross sections.

## F260 — Tree-level QED S-matrix + positron/charge-conjugation + crossing sector (2026-07-22)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 287 | F260: charge conjugation C=iγ²γ⁰ (Dirac rep): Cγ^μC⁻¹=−(γ^μ)^⊤, C^⊤=−C, C unitary, C²=−1 (explicit 4×4 gammas, sympy) — promotes the F27/F46 electron u-spinor to the positron v=Cū^⊤ | exact (sympy, literal 0) | all four identities literal 0 |
| 288 | F260: positron v=Cū^⊤ satisfies (p̸+m)v=0 and completeness Σᵥ v v̄=p̸−m; electron Σ u ū=p̸+m — model's own u,v completeness, **not** eig on chiral matrices (CLAUDE.md) | machine | residuals <1e-11 |
| 289 | F260: crossing — Bhabha(s,t,u)=Møller(u,t,s) [s↔u] and annihilation(a,b)=−Compton(−a,b) [a=p·k₁,b=p·k₂; fermion-crossing sign] — one analytic amplitude across channels | exact (sympy, literal 0) | both crossing identities exact |
| 290 | F260: Compton e γ→e γ spin-averaged \|M\|² (s+u channels, trace on model completeness) = Klein–Nishina Mandelstam form 2e⁴[p·k'/p·k+p·k/p·k'+2m²(1/p·k−1/p·k')+m⁴(…)²] (Peskin 5.87) | machine | worst rel <1e-13, all lab kinematics |
| 291 | F260: Ward/gauge invariance — replacing a photon polarisation by its momentum kills the amplitude: k_μM^{μν}=k'_νM^{μν}=0 (on-shell spinors); justifies the −g_{μν} (F250 transverse) pol sum | machine | <1e-12 |
| 292 | F260: Klein–Nishina total σ(x) by solid-angle integration vs closed KN form; reduces to Thomson σ_T as ω→0 (ties F249 A5): σ(x=1e-4)/σ_T=0.9998=1−2x; σ_T=0.6652459 barn vs CODATA 0.66524587 | quantitative | σ vs closed ≤4.5e-7; σ_T 0.3% |
| 293 | F260: Møller e⁻e⁻ (t/u) \|M\|²=2e⁴[(s²+u²)/t²+(s²+t²)/u²+2s²/(tu)] and Bhabha e⁻e⁺ (s/t) \|M\|²=2e⁴[(s²+u²)/t²+(u²+t²)/s²+2u²/(st)] vs textbook; CM differential cross sections in barn/sr | machine | worst rel <1e-13 |
| 294 | F260: pair annihilation e⁻e⁺→γγ (Dirac 1930): \|M\|² (t/u electron exchange, crossing of Compton) vs textbook; photon Bose symmetry k↔k'; Ward on BOTH photons; total σ=(2πα²/s)(1/β)[(3−β⁴)/(2β)ln((1+β)/(1−β))−(2−β²)] — needs the positron v=Cū^⊤ | machine + quantitative | \|M\|² & Bose <1e-13; Ward <1e-15; σ ≤1.6e-6 |
| 295 | F260: e⁻e⁺→μ⁻μ⁺ s-channel \|M\|²=(8e⁴/s²)[(p₁·k₁)(p₂·k₂)+(p₁·k₂)(p₂·k₁)+m_μ²p₁·p₂]; total σ=(4πα²/3s)β(1+2m_μ²/s)→4πα²/3s (R-ratio unit) — needs 2nd-gen muon (F121 anchor) | machine + quantitative | \|M\|² <1e-13; σ ≤1.6e-8 |

Test: `tests/findings/test_F260_qed_scattering.py` (11/11); also Tier D of `tests/findings/test_F249_qed_comparison_battery.py` (now 16/16). Module `casim.engine.interactions.qed_scattering`. Finding `F260-qed-scattering-smatrix.md`. Closes the S-matrix completeness F249 flagged (A5 stops at Thomson) and establishes the antiparticle sector the model had not exercised. Inputs: α + lepton masses (F120/F121). Tree level; O(α) radiative corrections are the F252/F259 loop/IR companions.

## F261 — Two-loop QED: A₂, two-loop β, muon a_μ + universality (2026-07-23)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 296 | F261: equal-mass VP insertion (from F251's own spectral fn (1/π)Im Π=(α/3π)(1+2m²/s)√(1−4m²/s), via the F252 kernel K₁, dispersive Källén–Lehmann) = 119/36−π²/3 = 0.0156874219 — the model-derived half of A₂ | model-derived (exact target) | abs err 3e-10 |
| 297 | F261: A₂ = (119/36−π²/3) + (−31/16+5π²/12−(π²/2)ln2+(3/4)ζ₃) = 197/144+π²/12−(π²/2)ln2+(3/4)ζ₃ = −0.328478966 (Sommerfield–Petermann); group-sum identity sympy-exact. Group II (6 vertex masters) reproduced as the closed form, not re-derived | exact (sympy closed form) | abs err vs target 5.8e-10 |
| 298 | F261: two-loop QED running μ dα/dμ = 2α²/3π + α³/2π² (sympy-exact from μ de/dμ = e³/12π² + e⁵/64π⁴, α=e²/4π); one-loop = F251 b₀=4/3, two-loop coeff = ½ (α³/π²) i.e. b₁=1 per unit-charge Dirac fermion. Leptonic; quark/hadronic deferred (QCD sector F151/F152) | exact (sympy) | 1/(2π²), b₁=1 exact |
| 299 | F261: a_e through two loops = α/2π + A₂(e)(α/π)², A₂(e)=−0.32847844 (mass-indep + decoupling μ,τ VP) = 1.15963743e-3 vs measured 1.15965218e-3; one-loop 0.15% cut ~2 orders. Residual = 3-loop A₃=1.181… (out of scope) | quantitative | rel err 1.3e-5 |
| 300 | F261: universality — mass-independent A₁=½ and A₂=−0.328478966 IDENTICAL for e and μ (same diagrams, no mass dependence); the same number, not a fit | exact identity | literal equality |
| 301 | F261: A₂^VP(e in μ) = (1/3)ln(m_μ/m_e)−25/36+(π²/4)(m_e/m_μ)+… = 1.09425831 (model, from F251 Π) vs known 1.0942583 — leading source of a_μ>a_e; reverse (μ in e) decouples to 5.2e-7 (asymmetry ~2e6) | quantitative | abs err 1.0e-8 |
| 302 | F261: A₂(μ) = A₂_massindep + A₂^VP(e in μ) + A₂^VP(τ in μ) = −0.328479+1.094258+0.000078 = 0.765857421 vs known 0.765857410; a_μ^QED (2 loops) = 1.16554e-3. Hadronic VP + hadronic LbL (QCD F151/F152) and EW OUT OF SCOPE — no SM/experiment a_μ claim | quantitative (QED only) | abs err 1.1e-8 |

Test: `tests/findings/test_F261_twoloop_ae_amu.py` (7/7). Modules `casim.engine.interactions.qed_twoloop_ae`, `casim.engine.interactions.qed_amu`. Runner `tests/runners/run_F261_twoloop_qed.py` → `test-results/F261_twoloop_qed.json`. Finding `F261-twoloop-qed-ae-amu.md`. First two-loop result in the QED sector: the model's own F251 Π supplies the VP group of A₂, the electron-loop log that lifts a_μ above a_e, and the decoupling of heavy loops; the one-loop counterterms (F251/F252/F258) drive the subdivergence subtraction. Universality is an exact identity, not an input.

## F262 — Bound-state QED: positronium, hydrogen 21 cm, Lamb recoil + finite size (2026-07-23)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 296 | F262: positronium reduced-mass reduction — every Bohr level E_n(Ps)/E_n(H_∞)=½ (ratio of reduced masses (m_e/2)/m_e), grid-independent; ground state −6.803 eV closed / −6.799 eV numeric (F125 solver at μ=m_e/2) | structural (exact ratio) + machine (grid) | worst dev from ½ < 1e-9 |
| 297 | F262: ortho–para hyperfine 7/12 = 1/3 (spin–spin) + 1/4 (annihilation), sympy Rational | exact (literal) | sum_is_7_12 True |
| 298 | F262: spin–spin Fermi-contact coeff = (1/3)α⁴m_ec² from (8π/3)(α/m²)\|ψ(0)\|² with g=2 (F27/F46), \|ψ(0)\|²=(μα)³/π, μ=m_e/2 | machine | rel err < 1e-12 |
| 299 | F262: virtual-annihilation coeff = (1/4)α⁴m_ec² from 2·(πα/m²)\|ψ(0)\|² (^3S_1 only); contact strength πα/m² = model single-photon e⁺e⁻ vertex, threshold σv→πα²/m² (F260 annihilation, β→0) | machine + quantitative | coeff rel err < 1e-12; σv ratio →1 to 4e-4; \|M\|²/e⁴→4 |
| 300 | F262: Ps hyperfine LO = 7/12 α⁴m_ec² = 204 387 MHz vs measured 203 389 (0.5% = O(α⁵) radiative) | quantitative (LO) | +0.49% |
| 301 | F262: para→2γ Γ = 4(σv)_thr\|ψ(0)\|² = (1/2)α⁵m_ec² (σv from F260); τ_LO=0.1245 ns vs 0.1245 ns | machine (coeff) + quantitative | coeff rel err < 1e-12 |
| 302 | F262: Ore–Powell 3γ phase-space integral ∫₀¹P(x)dx = π²−9 (midpoint quadrature); ortho Γ=2(π²−9)/(9π)α⁶m_ec², τ_LO=138.7 ns → 142 measured under O(α) | quantitative | integral rel err < 5e-4 |
| 303 | F262: hydrogen 21 cm Fermi contact (4/3)g_p(m_e/m_p)α⁴m_ec², ×(m_r/m_e)³×(1+a_e) with a_e=α/2π (F252) = 1420.49 MHz vs 1420.4058 (g_p input) | quantitative | rel err 5.8e-5; λ=21.1 cm |
| 304 | F262: finite-nuclear-size 2s shift = (1/12)(Zα)⁴m_r(m_r c r_p/ℏ)² = +0.138 MHz (r_p=0.8409 fm), s-state only; ∝r_p² proton-radius lever (d ln/d ln r_p = 2) | quantitative (r_p input) | 0.138→0.150 MHz for r_p 0.8409→0.8770 |
| 305 | F262: Lamb completeness — baseline 1052.19 (F252/F257) + reduced-mass (m_r/m_e)³ (−1.72, derived) + finite size (+0.138) + EGS pure recoil (+0.36, cited) = 1050.97 MHz; residual +6.87 to 1057.845 = two-loop QED (F261) | quantitative | recoil/size sub-MHz–MHz; residual = higher-order radiative |

Test: `tests/findings/test_F262_positronium_hyperfine.py` (10/10). Modules `casim.engine.particles.positronium`, `casim.engine.particles.hyperfine`. Finding `F262-positronium-hydrogen-hyperfine-lamb.md`. Extends the one-body bound-state QED (F125 fine structure + F252/F257 radiative Lamb) to the two-body + hyperfine sectors. Inputs beyond α, m_e: proton g_p and radius r_p (stated). Annihilation hyperfine + para decay are model-derived from the F260 e⁺e⁻ vertex.

## F263 — Nonlinear/non-perturbative QED: Euler–Heisenberg, light-by-light, birefringence, Schwinger (2026-07-23)

| # | Quantity | Tier | Result |
|---|---|---|---|
| 306 | F263: Euler–Heisenberg $\mathcal L_\text{EH}=(2\alpha^2/45m^4)[(E^2-B^2)^2+7(E\cdot B)^2]$ — prefactor $2/45$ and box invariant weight $7$ (basis $8/45:14/45=4:7$) from the proper-time weak-field expansion $(x\coth x)(y\cot y)-1-(x^2-y^2)/3$, $\int_0^\infty s\,e^{-m^2s}ds=1/m^4$, $e^4=16\pi^2\alpha^2$ | exact (sympy) | prefactor $=2/45$, weight $=7$ literal |
| 307 | F263: light-by-light $\sigma(\gamma\gamma\to\gamma\gamma)=(973/10125\pi)\alpha^4\omega^6/m^8$ (Karplus–Neuman) from the $\mathcal L_\text{EH}$ contact vertex, 16-pol sum + solid-angle integral + identical-particle $\tfrac12$; angular integral closes to a rational $\times1/\pi$ | exact (sympy) | coeff $=973/10125$ literal |
| 308 | F263: four-photon amplitude exactly transverse on **all four legs** ($\epsilon^i\to k^i\Rightarrow\mathcal M=0$, since each photon enters only via $f^i_{\mu\nu}$) + Bose symmetric — the four-leg counterpart of F251's two-leg Ward identity; preserves the F250 massless gauge pole | exact (sympy) | all Ward residuals literal $0$ |
| 309 | F263: field-induced vacuum birefringence $(n_\parallel-1):(n_\perp-1)=7:4$ (Adler 1971) from $\mathcal L_\text{EH}$ 2nd-order probe expansion about constant $B$; nonlinear counterpart of F249-B1's zero **linear** birefringence | exact (sympy) | $7:4$ literal |
| 310 | F263: Schwinger $\operatorname{Im}\mathcal L_n=(eE)^2/(8\pi^3 n^2)e^{-n\pi m^2/eE}$ from the proper-time residue at $s_n=n\pi/eE$; $w=2\operatorname{Im}\mathcal L=(eE)^2/(4\pi^3)\sum_n n^{-2}e^{-n\pi m^2/eE}$; exponent $\pi m^2/eE=\pi E_\text{crit}/E$ | exact (sympy) | ratio to target $=1$ |
| 311 | F263: critical field $E_\text{crit}=m_e^2c^3/e\hbar=1.323\times10^{18}$ V/m; $B_\text{crit}=m_e^2c^2/e\hbar=4.414\times10^{9}$ T (CODATA) | quantitative | rel err $2.5\times10^{-3}$ vs $1.32\times10^{18}$ |
| 312 | F263: non-perturbative — $\exp(-\pi E_\text{crit}/E)$ has an identically-zero Taylor series about $E=0$ (essential singularity); Schwinger production is invisible to any finite order of perturbation theory | exact (sympy) | series $\equiv0$ |

Test: `tests/findings/test_F263_euler_heisenberg_schwinger.py` (7/7). Modules `casim.engine.interactions.qed_euler_heisenberg`, `casim.engine.interactions.qed_schwinger_pair`. Runner `tests/runners/run_F263_euler_heisenberg_schwinger.py` → `test-results/F263_euler_heisenberg_schwinger.json`. Finding `F263-euler-heisenberg-schwinger-nonlinear-qed.md`. The nonlinear/non-perturbative corner of QED on the model's own electron loop: the F251 two-photon bubble becomes the four-photon box (Euler–Heisenberg) and, in an electric field, develops the imaginary part that is pair creation. All coefficients ($2\alpha^2/45$, $7$, $973/10125\pi$, $7:4$, $\pi m^2/eE$) are exact; gauge invariance holds on all four legs. Scope: leading four-field/one-loop, $\omega\ll m$ contact limit (ATLAS Pb+Pb is the full-box measured contact point, not fit), constant-field Schwinger.

## F264 — All-orders QED: renormalizability closure, WT $Z_1{=}Z_2$/charge universality, Callan–Symanzik, ABJ anomaly + Nielsen–Ninomiya (2026-07-26)

| # | result | tier | evidence |
|---|--------|------|----------|
| 313 | F264: superficial degree of divergence $D=4-\tfrac32E_f-E_\gamma$ derived from the QED topology ($L{=}I_f{+}I_\gamma{-}V{+}1$, $2V{=}2I_f{+}E_f$, $V{=}2I_\gamma{+}E_\gamma$); the $V$- and $L$-dependence cancels IDENTICALLY — this cancellation *is* renormalizability | exact (sympy) | $\partial D/\partial V=\partial D/\partial L=0$ literal 0 |
| 314 | F264: counterterm closure — census of $(E_f,E_\gamma)$ with $D\ge0$ after Furry ($C$-parity kills odd-photon) and gauge invariance ($\Pi^{\mu\nu}$ transversality F251/Pi1 reduces $D{=}2\to0$, no photon mass; 4-photon box $D_\text{eff}{=}-4$ FINITE, F263) leaves exactly $\{\Sigma,\Pi,\Lambda\}$ absorbed by exactly $\{Z_1,Z_2,Z_3,\delta m\}$; four-fermion $D{=}-2$ not generated | exact (sympy) | 4 counterterms, set equality; $D_\text{4-fermi}<0$ |
| 315 | F264: operator-basis dual — Lorentz-scalar, $U(1)$-invariant, $P$- and $C$-even local operators of dim $\le4$ from $\{\psi,A_\mu,\partial_\mu\}$ number exactly 4: $\bar\psi i\gamma^\mu\partial_\mu\psi$, $e\bar\psi\gamma^\mu A_\mu\psi$, $m\bar\psi\psi$, $F_{\mu\nu}F^{\mu\nu}$; $A_\mu A^\mu$ excluded by gauge invariance (F251/Pi1, F250), $F\tilde F$ by parity — the latter being the operator the AXIAL ANOMALY multiplies (forbidden as a counterterm, generated as a current divergence) | exact | 4 allowed; both near-misses excluded on stated grounds |
| 316 | F264: the photon-insertion identity $S(p')\slashed q S(p)=S(p)-S(p')$ (from $\slashed q=S^{-1}(p'){-}S^{-1}(p)$) with explicit $4\times4$ gammas, four symbolic momenta and symbolic mass; inserting a vertex ADDS a propagator so $\slashed q$ always sits between $S(k_i{+}q)$ and $S(k_i)$ ⇒ the sum over the $n{+}1$ insertion points TELESCOPES to $T_{n+1}-T_0$ (ends only) ⇒ $q_\mu\Gamma^\mu=S^{-1}(p'){-}S^{-1}(p)$ at EVERY order (internal photons/loop momenta are spectators) | exact (sympy) for the identity; exact-rational (generic momenta) for the assembled $n{=}1..4$ chains | core residual literal 0; closed-form propagator exact; chains literal 0 in $\mathbb Q$ |
| 317 | F264: differential WT $\Gamma^\mu(p,p)=\partial S^{-1}/\partial p_\mu$ (F258/S3 is its one-loop instance) with $S^{-1}{=}Z_2^{-1}(\slashed p{-}m)$, $\Gamma^\mu(p,p){=}Z_1^{-1}\gamma^\mu$ ⇒ $Z_1=Z_2$ as the UNIQUE entry-by-entry solution for every $\mu$; order-independent since WT is | exact (sympy) | unique solution $=Z_2$, all $\mu$; one-loop $Z_1{-}Z_2=0$ (F252/F258 both $-\alpha/4\pi$) |
| 318 | F264: charge universality — $e_R=Z_1^{-1}Z_2Z_3^{1/2}e_0\to Z_3^{1/2}e_0$; the species-dependent $Z_1,Z_2$ (each $\propto\ln(\Lambda^2/m_f^2)$, verified to genuinely DIFFER between two masses) cancel identically ⇒ $\lvert q_e\rvert{=}\lvert q_\mu\rvert{=}\lvert q_\tau\rvert{=}\lvert q_p\rvert$ exactly | exact (sympy) | $e_R^{(1)}-e_R^{(2)}$ literal 0; $Z_2^{(1)}\neq Z_2^{(2)}$ |
| 319 | F264: Callan–Symanzik $[\mu\partial_\mu+\beta\partial_e+n\gamma_2+m\gamma_3]\Gamma^{(n,m)}=0$ with $\beta=e^3/12\pi^2$ recovered from F251's $b_0^\text{QED}=\tfrac43$ (both directions: $b_0$ reads back as exactly $4/3$), $\gamma_3=\alpha/3\pi=e^2/12\pi^2$, $\gamma_2=\alpha/4\pi$ (Feynman gauge, gauge-DEPENDENT and said so) | exact (sympy) | $\beta$, $b_0$, $\gamma_3$ residuals literal 0 |
| 320 | F264: the ALL-ORDERS structural relation $\beta(e)=e\,\gamma_3(e)$ — a consequence of $Z_1{=}Z_2$ ($e_R{=}Z_3^{1/2}e_0$, $e_0$ $\mu$-independent): the entire QED beta function is carried by the PHOTON's anomalous dimension, the fermion sector cannot contribute. RG-level restatement of charge universality | exact (sympy) | $\beta-e\gamma_3$ literal 0 |
| 321 | F264: $\gamma_5=i\gamma^0\gamma^1\gamma^2\gamma^3$ in the F252/F258 basis — $\gamma_5^2{=}1$, $\{\gamma_5,\gamma^\mu\}{=}0$, hermitian, $P_{L,R}$ idempotent/orthogonal/complete; $\mathrm{Tr}[\gamma_5\gamma^\mu\gamma^\nu]{=}0$ (16), $\mathrm{Tr}[\gamma_5\gamma^\mu\gamma^\nu\gamma^\rho\gamma^\sigma]{=}-4i\epsilon$ (256), $\mathrm{Tr}[\gamma_5\sigma^{\mu\nu}\sigma^{\rho\sigma}]{=}+4i\epsilon$ (256) — the relative sign FORCED by $\sigma{=}\tfrac i2[\gamma,\gamma]$, not chosen. The four-gamma trace is the ONLY source of $\epsilon^{\mu\nu\rho\sigma}$, hence the anomaly $\propto\epsilon FF$ and nothing else | exact (sympy) | 512 index combinations, all literal 0 residual |
| 322 | F264: classical divergences — $\partial_\mu(\bar\psi\gamma^\mu\psi)=0$ for ANY $m$; $\partial_\mu(\bar\psi\gamma^\mu\gamma_5\psi)=2im\bar\psi\gamma_5\psi$. One commutator separates them: $\gamma_5$ ANTIcommutes with $\slashed p$ but COMMUTES with $m\mathbb 1$. ⇒ the model has NO exactly conserved chiral charge (F27/F46 Dirac mass), which is the NN hypothesis that must fail | exact (sympy) | both (anti)commutators literal 0 |
| 323 | F264: ABJ coefficient, ROUTE 1 (Fujikawa measure Jacobian): $\slashed D^2=D^2+\tfrac e2\sigma^{\mu\nu}F_{\mu\nu}$ exact (Clifford split literal 0); $\gamma_5$-traces kill orders 0 and 1 in $\sigma\!\cdot\!F$ so ONLY the 2nd-order heat-kernel term survives; $\int d^4k_E/(2\pi)^4e^{-k^2/\Lambda^2}=\Lambda^4/16\pi^2$ exact. The $\Lambda^4$ cancels the $1/\Lambda^4$ MANIFESTLY ⇒ $\partial_\mu j_5^\mu=2im\bar\psi\gamma_5\psi-\tfrac{e^2}{16\pi^2}\epsilon^{\mu\nu\rho\sigma}F_{\mu\nu}F_{\rho\sigma}$, i.e. $\tfrac{2\alpha}{\pi}\mathbf E\!\cdot\!\mathbf B$; regulator-INDEPENDENT | exact (sympy) | $\lvert$coeff$\rvert=1/16\pi^2$ residual 0; $\partial/\partial\Lambda=0$; all three normalisation forms agree |
| 324 | F322: the lattice contribution to $\Delta\alpha(M_Z)$ is BOUNDED, not assumed absent — $q$-flatness of $\Delta=B_\text{rule}-B_\text{cont}$ IS $\Delta\alpha$ invariance (a $q$-independent constant in $\Pi$ cancels in $\Pi(0)-\Pi(s)$), with the conversion $\delta(\Delta\alpha)=4\pi\alpha\,\delta B$ EXACT from F251's own $b_0^\text{QED}=4/3$; measured bound $6.77\times10^{-6}$ at $n{=}28$ = $0.088\times$ the PDG shortfall and FALLING (ratio $0.398$), vs $1.41\times10^{-2}$ = $183$–$190\times$ and $n$-flat (ratio $0.965$) with the F277 refold restored | exact conversion + convergent bound | $f=4\pi\alpha$ residual $<10^{-15}$; bound $<$ shortfall at every $n$ |
| 325 | F322: $\Delta\alpha_\ell(M_Z)$ with F261's sympy-exact $b_1=1$ folded in for the first time — two-loop leading log $\alpha^2L_\ell/(4\pi^2)$ per lepton closes $79.8\%$ of the one-loop shortfall, $0.2447\%\to0.0495\%$ vs PDG leptonic $0.031498$; two-loop NON-log constant and three loops NOT derived (residual $1.559\times10^{-5}$) | quantitative | $0.03148241$ vs $0.031498$; $b_1$ itself exact |
| 326 | F322: B9's EW leg is contingent on an input, quantified — F138's $\sin^2\bar\theta_W(M_Z)=0.2317341$ ($+0.222\%$) reproduced from $\sin^2\theta_W(4\pi v)=\tfrac14$, but on the model's OWN leptonic-only $\alpha(M_Z)$ the residual doubles to $+0.450\%$ (factor $2.02$); the missing $3.795$ in $\alpha^{-1}(\overline{\text{MS}})$ is the hadronic VP the model defers to row G3 | quantitative | sensitivity $d\sin^2/d\alpha^{-1}=1.428\times10^{-4}$ |
| 324 | F264: ABJ coefficient, ROUTE 2 (illegitimate shift of a linearly divergent integral): for $f^\mu{=}k^\mu/(k^2{+}D)^2$ the surface term is $a^\mu/32\pi^2$ — two individually LOG-DIVERGENT pieces cancel leaving a convergent integral, and the result is exactly $D$-INDEPENDENT (required, since the measured ABJ coefficient is mass-independent). Ratio to the anomaly coefficient is exactly 2 = the two chiralities. Two wholly independent arguments (heat-kernel trace vs boundary term at infinity), same rational | exact (sympy) | surface $=1/32\pi^2$; radial $=1/2$; $\partial_D=0$; ratio $=2$ |
| 325 | F264: the vector-safe/axial-anomalous dichotomy — $\gamma^\mu{=}\gamma^\mu(P_L{+}P_R)$ vs $\gamma^\mu\gamma_5{=}\gamma^\mu(P_R{-}P_L)$ ⇒ branch weights $(+1,+1)$ vs $(-1,+1)$ ⇒ $\mathcal A_V{=}0$, $\mathcal A_A{=}-2\mathcal A_0$ (the same factor 2 as #324). MODEL-SPECIFIC: the $(+1,+1)$ weighting is not a charge choice — the F68/F87 coupling $P=e^{iqA\cdot d\ell}\mathbb I_2$ is branch-BLIND ($\mathrm{tr}(\sigma_xP){=}0$, $[P,\sigma_z]{=}0$), so the $U(1)$ is vector-like BY CONSTRUCTION and the gauge anomaly is structurally zero, not an imposed $\sum q^3{=}0$ condition | exact (sympy) | all decompositions literal 0; $\mathcal A_V=0$; branch-blindness literal 0 |
| 326 | F264: the TRUE Brillouin zone of the BCC walk is FCC, not the cube — $G\cdot d\in2\pi\mathbb Z$ for all eight $d\in\{\pm1\}^3$ is satisfied by $\pi(1,1,0),\pi(1,0,1),\pi(0,1,1)$, so $V_\text{BZ}=2\pi^3=(2\pi)^3/4$ and the cube $[-\pi,\pi]^3$ holds exactly 4 copies. A cube census over-counts every Weyl point fourfold (the apparent "8 doublers per branch" is this artefact) | exact (sympy) | all 3 generators valid; copies $=4$ |
| 327 | F264: Weyl-point census in the true BZ — each chiral branch has exactly TWO Weyl points, the Nielsen–Ninomiya MINIMUM: $\Gamma{=}(0,0,0)$ and $R{=}\tfrac\pi2(a,b,c)$ with $abc{=}\pm1$ per branch, chiralities exactly $\mp1$ / $\pm1$ from $\mathrm{sign}\det(\partial n_i/\partial q_j)$ (Berry monopole charge; NO eig on chiral matrices per CLAUDE.md), $\sum\chi=0$. So the walk is a MINIMAL lattice Weyl fermion, not a coarse one with $2^d$ doublers | exact (sympy) | $\det=\pm1$ exactly; $\sum\chi=0$ both branches; $n_\text{Weyl}=2$ |
| 328 | F264: the mechanism — at $q{=}\tfrac\pi2(a,b,c)$ every cosine vanishes and $s_xs_ys_z{=}abc$, so $u^\pm{=}0\pm abc$: exactly one branch is gapless and its PARTNER sits at $u{=}-1$, i.e. $\omega{=}\pi$, the BAND TOP. Since a light Dirac mode needs both branches gapless (the F27/F46 mass couples them), that happens at $\Gamma$ ($u^+{=}u^-{=}1$) and nowhere else ⇒ the light sector holds ONE Weyl pair carrying the full $1/16\pi^2$ while the NN-mandated mirror is gapped at the cutoff — the momentum-space analogue of domain-wall/overlap fermions, done by the $\pm$-branch pairing (F69) instead of an extra dimension | exact (sympy) | $u^\pm$ values exact integers; 1 light point, 1 mirror |
| 329 | F264: Nielsen–Ninomiya threaded correctly — locality, translation invariance and hermiticity/unitarity all HOLD; exactly ONE hypothesis fails, the exactly-conserved local chiral charge (#322, the physical electron mass — same escape route as Wilson fermions, but here the chirality-breaking term is physical rather than an artefact tuned away). $\sum\chi=0$ still holds, so NN is SATISFIED not evaded | structural (the failure itself exact via #322) | 1 of 4 hypotheses fails, correctly identified |
| 330 | F264: **corrected framing (recorded, not buried)** — the F250 paired-photon doubler-folding ($k/2$ sharing puts the photon's would-be doubler pole at $\lvert k_i\rvert{=}2\pi$, outside its BZ) is NOT the mechanism keeping the axial anomaly uncancelled: the anomaly is a FERMION loop integrated over the whole FERMION BZ, so it samples every Weyl point regardless of external photon momenta. The actual mechanism is #328's mirror-point gapping. Both share the $\pm$-branch root cause (F69), which is why they conflate; F250's own claim (about the gauge-BOSON spectrum) stands unchanged | structural correction | mechanism reattributed to the fermion spectrum |
| 331 | F264: the anomaly is MEASURED — $\Gamma(\pi^0\to\gamma\gamma)=\alpha^2m_{\pi^0}^3/64\pi^3f_\pi^2$ (the $1/64\pi^3$ descending from $1/16\pi^2$) gives 7.749 eV vs PDG $7.80\pm0.12$ eV. Simultaneously tests $N_c{=}3$ (F75): $\sum_qN_c(q_u^2{-}q_d^2)=N_c/3=1$ only for $N_c{=}3$; $N_c{=}2$ or 4 give 3.44 / 13.78 eV ($-56\%$ / $+77\%$) | quantitative | rel err $6.5\times10^{-3}$, $0.42\sigma$ |
| 332 | F264: the Landau pole lies OUTSIDE the theory — $\mu_L=m_e\exp(3\pi/2\alpha)\approx10^{277}$ GeV sits 259 decades above the model's own Brillouin-zone cutoff $\Lambda_a=\hbar c/a\approx1.9\times10^{18}$ GeV ($a=6.5978\,\ell_P$, F107). A lattice QED does not inherit the continuum's UV embarrassment (structural remark, not a resolution of the continuum problem) | quantitative | $\log_{10}\mu_L=277.2$ vs $\log_{10}\Lambda_a=18.27$ |

Test: `tests/findings/test_F264_qed_allorders_anomaly.py` (17/17). Modules `casim.engine.interactions.qed_renormalization`, `casim.engine.gauge.chiral_anomaly` → `test-results/F264_qed_allorders_anomaly.json`. Finding `F264-qed-allorders-renormalizability-anomaly.md`. The structural closure of the model's QED: F251/F252/F258 computed the three one-loop 1PI functions; this establishes the all-orders statements that make them a theory — a closed four-element counterterm set at every order, $Z_1{=}Z_2$ from an all-orders Ward identity giving charge universality, an RG whose beta function is carried entirely by the photon ($\beta=e\gamma_3$), and the ABJ anomaly with the correct coefficient by two independent exact routes while satisfying Nielsen–Ninomiya. Three model-specific results: the gauge anomaly is structurally zero (branch-blind F68/F87 coupling, not charge bookkeeping); the BCC walk is a MINIMAL lattice Weyl fermion whose NN mirror is gapped at the band top by the $\pm$-branch pairing; and the Landau pole is outside the lattice's domain of definition. Scope: sign of the anomaly is convention-documented not tuned (magnitude is the gate); the full AVV triangle with vector-Ward redistribution, non-abelian/electroweak anomalies, and Adler–Bardeen two-loop non-renormalization are out of scope; $f_\pi$ is an input.
| 333 | F265: the BCC lattice generated by the 8 body-diagonal hops (conventional cubic cell at side 2) is exactly $\{n\in\mathbb Z^3: n_x\equiv n_y\equiv n_z \bmod 2\}$, of index 4 in $\mathbb Z^3$ ⇒ only **1/4** of a cubic array's sites are lattice sites; the reciprocal lattice is **fcc** ($\pi(1,1,0)$ and perms), $V_\text{BZ}=2\pi^3=(2\pi)^3/4$, so the cube $[-\pi,\pi)^3$ holds exactly **4 copies** of the true BZ — independently reproducing F264 row 326 from the hop set instead of the Weyl-point census. `bcc_bz_mask` returns exactly $N/4$ points for $L=4,6,8,12,16$ | exact | set identity literal; $\lvert\det\rvert=4$; counts exact all $L$; fcc shifts are walk periods to $1.1\times10^{-15}$ |
| 334 | F265: there are **no 3-bond closed loops** on the BCC hop graph (three all-odd vectors cannot sum to zero — 0 of $8^3$), so the minimal gauge loop is the **4-bond rhombus**; modulo translation there are exactly **6** orientations, each of area $\lvert d_1\times d_2\rvert=2\sqrt2$ with normal on a $\langle110\rangle$ face-diagonal axis, forming a single $O_h$ orbit of size 6. The half-normals satisfy $\sum_{p}m_pm_p^{\mathsf T}=4\,\mathbb I$ exactly, giving the closed-form 6→3 field-strength reconstruction $f^a=\tfrac18\sum_p m_p\Phi^a_p$ with no pseudo-inverse | exact | 0 three-loops; 6 orientations; single area; 6 normal axes; Gram $=4\mathbb I$ literal |
| 335 | F265: the composite-SC and genuine-BCC gauge actions have the **identical** classical continuum limit — $\sum_{p=1}^{6}(F_{\mu\nu}d_1^\mu d_2^\nu)^2 = \sum_{\mu<\nu}(4F_{\mu\nu})^2 = 8F_{\mu\nu}F^{\mu\nu}$, difference identically zero — so the migration moves neither the continuum limit nor $g_\text{lat}$, and no weak-field normalisation check could ever have detected the defect | exact (sympy) | both ratios $=8$; difference literal 0; U(1) density ratio $\to4.0$ (3.99975 at $\varepsilon=0.01$) |
| 336 | F265: the composite-SC field strength has an **exact kernel** — fixing the three straight composites to $\mathbb I$ leaves one of the four $\langle111\rangle$ axis fields completely free, so $S_\text{SC}\equiv0$ to round-off while the BCC Wilson density is $\approx1$; persists at *every* amplitude ($\varepsilon$-scan: $S_\text{SC}\sim10^{-16}$, $S_\text{BCC}\to2.345\,\varepsilon^2$), hence $O(\varepsilon)$ field strength is missing. Rank count per colour component over $N_s$ sites: link vars $4N_s$, $\mathrm{rank}_\text{BCC}=3N_s-3$, $\mathrm{rank}_\text{SC}=2N_s-4$, blind $=N_s+1$ ⇒ asymptotically **1/4** of the link space and **1/3** of the curvature-carrying content | exact (integer rank formulae, $L=4,6,8$); kernel to machine precision | formulae hold exactly at all three $L$; both actions annihilate pure gauge ($10^{-16}$); constant $F$ recovered with site spread $4.8\times10^{-17}$ |
| 337 | F265: Bianchi — the naive Cartesian curl converges at the generic $O((ka)^2)$ for the BCC rhombic field strength (measured slope 2.00, 1.97, 1.99 over $L=16..48$) but at $O((ka)^3)$ for the composite-SC construction, because the latter's three planes share one simple-cubic sublattice on which the cube-face product is an *exact* lattice identity. Negative resolution of the open roadmap item: the composite's anomalously small residual **is** its restriction to 3 of 6 orientations, so the cross-direction terms are physical content and no transform should remove them | quantitative (order measured, not fitted) | BCC slopes $1.99\pm0.02$; composite slopes $2.69\to2.98$ |

Tests: `tests/findings/test_F265_bcc_gauge_geometry.py` (12/12) → `test-results/F265_bcc_gauge_geometry.json`. Modules `casim.engine.gauge.bcc_action` (new), `casim.engine.lattice.geometry` (BCC geometry section). Finding `F265-bcc-gauge-action-blindness.md`. Migration verified against the existing suites: `test_wmu_phase3` 5/5, `test_FG7_gluon_dynamics` 20/20, unchanged. Still cubic and explicitly open: the 4D hypercubic `ca_lpt_*` one-loop chain, the `ca_bgfield_loop` BCC-propagator-on-cubic-BZ fold (measure wrong by the factor 4 of row 333), `ca_hypercharge` (2D despite its docstring), and the F94/F146 Monte-Carlo actions.

| # | Result | Class | Evidence |
|---|---|---|---|
| 338 | F278: the fermion walk's BCC **conventional cube edge is $a=2/\sqrt3$**, read off the hop phase $e^{i\mathbf k\cdot\mathbf d/\sqrt3}$ of `bcc_fractional_shift` — the walk's real-space hop is $\boldsymbol\delta=\mathbf d/\sqrt3=\tfrac a2(\pm1,\pm1,\pm1)$, so $\tfrac a2=1/\sqrt3$. Then $\lvert\boldsymbol\delta\rvert=\tfrac{\sqrt3}2a=1$ exactly (the unit hop). $a$ is **not a new constant**: $a=2c_\text{lat}$, the registered $1/\sqrt3$ wearing its length hat — $a/2$ and `c_lat` are the **same IEEE-754 double** (`0x3fe279a74590331d`), not merely equal | exact (sympy + bit compare) | $\lvert\tfrac a2(1,1,1)\rvert-1\equiv0$; $a/2$ `==` `c_lat` is `True`, residual $0.0$. NB a `sympy`-float evaluation of $2/\sqrt3$ lands one ulp off $2c_\text{lat}$ — derive $a$ from `c_lat`, never transcribe it as a literal (D7) |
| 339 | F278: **F267's measured cube/BZ ratio is a primitive-cell volume.** $V_\text{cube}/V_\text{BZ}=(2\pi)^3/[(2\pi)^3/V_\text{prim}]=V_\text{prim}=a^3/2=4\sqrt3/9=0.769800358919501$ — identically F267's $4/(3\sqrt3)$. The ratio equals the primitive cell volume *as a pure number* because the FFT cube is the zone of a unit-volume simple-cubic sampling lattice. Promotes F267's number from **measured** to **closed form** | exact (sympy) | $a^3/2-4/(3\sqrt3)\equiv0$; $V_\text{cube}/V_\text{BZ}-a^3/2\equiv0$; $V_\text{BZ}=322.2266793829$, $V_\text{cube}=248.0502134424$ |
| 340 | F278: **F273's measured "$\sqrt3\cdot$fcc" period lattice is the reciprocal of the same crystal.** The reciprocal of BCC($a$) is fcc($4\pi/a$), and $4\pi/a=2\pi\sqrt3=\sqrt3\times2\pi$ — the measured factor $\sqrt3$ against the $2\pi$ period the cubic grid assumes. Gives the structural reason the F272/F277 $\bmod\,2\pi$ refold is a defect: the simple-cubic $2\pi$ lattice is not a sublattice of fcc($2\pi\sqrt3$). Promotes F273's number from **measured** to **closed form** | exact (sympy) | $4\pi/a-2\pi\sqrt3\equiv0$ |
| 341 | F278: the $\omega=\pi$ mode sits **exactly on the true zone boundary**, not outside it. $\Gamma$–H $=2\pi/a=\pi\sqrt3=5.441398092702654$, and $\omega^\pm(\pi\sqrt3,0,0)=\pi$ on **both** branches. Forces the domain qualifier on the no-doubler claim: one zero at $k=0$ and no $\pi$-mode **on the FFT cube** ($L$ to 128; $\max\omega=3.11355278<\pi$ at $L=48$), a $\pi$-mode at H on the crystal. Does **not** decide whether it is a doubler — that is the open Reading 1 / Reading 2 question | exact (float, literal 0.0) | $2\pi/a-\pi\sqrt3=0.0$; $\omega^\pm(\text H)-\pi=0.0$, $0.0$ |
| 342 | F278: the gauge and fermion measure factors are **one relation at two lattice constants** — $V_\text{cube}/V_\text{BZ}=a^3/2$ gives F265 row 333's **4** at $a=2$ (integer-hop link lattice) and $4\sqrt3/9$ at $a=2/\sqrt3$ (fractional-hop walk), with $a_\text{gauge}/a_\text{fermion}=\sqrt3$ and measure ratio $(\sqrt3)^3=3\sqrt3$. **Answers the standing "$\sqrt3$ question"** (`next-steps.md`, F265 follow-on) negatively: the fermion sector does **not** inherit the gauge side's factor 4; transplanting it over-corrects by $3\sqrt3\approx5.196$ | exact (sympy) | $4/(4\sqrt3/9)-(\sqrt3)^3\equiv0$ |

Finding `F278-bcc-lattice-constant-two-over-root-three.md`. **No test record yet** — a gate-tier `entry:` record is specified in F278 §9 and is a candidate answer to audit item V-016 (nothing currently guards the $c_\text{lat}$ separation). Rows 338–342 change no physics number and move no baseline; 339 and 340 are reclassifications of numbers already in the tree, from *measured* to *exact*.

---



---
## F279 — hypercharge quantisation: constraint attribution corrected (2026-08-02)

Adjudicates F165 against `Claims-and-Falsifiers-Summary.md`. All rows exact-rational over ℚ
(`sympy.Rational`; residuals are the literal integer 0, not floats near zero).

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| F165's published 5-row system reproduces | rank 5, nullspace dim 1; ratios $1:4:-2:-3:-6$ | exact (ℚ) | F279 / test_F279_hypercharge_attribution.py |
| $[\text{grav}]^2U(1)$ row adds no rank once $\nu_R$ is carried | rank 5 with **and** without; grav row $\equiv0$ on the other five | literal 0 | F279 A1 |
| Anomaly + mass rows alone, with $\nu_R$ | nullspace dim **2** ($y_Q$ and $y_\phi$ both free) | exact (ℚ) | F279 A1 |
| F47 Majorana step closes the system | $2y_\nu=0\Rightarrow y_\nu=0$; rank 6, dim 1 | literal 0 | F279 A2 |
| Both anomalies on the corrected line | $[\text{grav}]^2U(1)=0$ and $U(1)^3=0$ identically | literal 0 | F279 A2 |
| Closure is $N_c$-independent | dim 1 for all $N_c$; ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$ | exact (ℚ + symbolic $N_c$) | F279 A3 |
| Cubic anomaly, general $N_c$ | $\equiv0$ on the line for every $N_c$ | literal 0 | F279 A3 |
| Single shared mass phase is load-bearing | two phases $\Rightarrow$ dim 2, $y_u,y_d$ float on $y_{\phi d}$ | exact (ℚ) | F279 A4 |

## F282 — primordial-sector no-go: no slow-roll inflaton direction (2026-08-02)

Rubric row K4 / completeness gap #1. The obstruction constant and the two closed-form
coefficients are exact-algebraic (sympy, re-derived independently of the module); the
$E_g$ radial scan is machine on the model's own F118 couplings.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Lattice spacing in **reduced** Planck units | $a/\ell_\text{red}=(\sqrt{8\pi}\,3^{1/4})/\sqrt{8\pi}=3^{1/4}$ | exact (sympy) | F282 A1 / F79, F107 |
| UV cutoff is sub-Planckian | $\Lambda_\text{UV}=\sqrt{c_\text{lat}}\,M_\text{Pl}=0.759836\,M_\text{Pl}$ | $<10^{-14}$ | F282 A1/A2 |
| Universal obstruction constant | $M_\text{Pl}^2/\Lambda^2=\sqrt3=1/c_\text{lat}$ | exact (sympy) | F282 A1 |
| $E_g$ clock slow-roll ratio | $\epsilon/r=18\tan^2 3\delta$ | exact-algebraic | F282 B1 |
| $E_g$ clock coefficient | $K=9$ at $\cos6\delta=\tfrac13$; amplitude-independent | exact (sympy) | F282 B1 |
| $E_g$ clock required decay constant | $f\ge15\sqrt2\,M_\text{Pl}=21.213\,M_\text{Pl}=27.9\,\Lambda_\text{UV}$ | $<10^{-9}$ | F282 B1 |
| $E_g$ radial hat, $V_0$ forced by F193 | $e_\text{min}=0.6549901$, $V_0=0.2408312$ | $<10^{-9}$ | F282 B2 |
| $E_g$ radial coefficient | $K=5.9215$; hilltop $\eta/r=-8.9523$ | machine | F282 B2 |
| Two $E_g$ directions agree | $f_\text{clock}/f_\text{radial}=1.23$ (robustness) | within factor 2 | F282 B2 |
| Periodic-direction spectral bound | $n_s\le1-p^2r$, since $\min_u\frac{3+u}{1-u}=1$ at $u=-1$ | exact (sympy) | F282 C1 |
| Most generous case vs Planck | $n_s\le1-\sqrt3=-0.7321$ vs $0.9649\pm0.0042$ | $404\sigma$ | F282 C1 |
| Starobinsky $R^2$ shortfall | $c_2^\text{req}=4.93\times10^8$ vs induced $0.106$ | 9.67 decades | F282 C2 |
| Induced scalaron above the cutoff | $M_s=0.8886\,M_\text{Pl}>\Lambda_\text{UV}=0.7598\,M_\text{Pl}$ | — | F282 C2 |
| No nearly-marginal scalar operator | F130 spectrum: exponents $\{+1,-2,-3,\dots\}$; gap to marginality $=1$ | exact (F130 T2/C1) | F282 C3 |

## F283/F284 — elastic lattice excluded; rigid-lattice expansion (2026-08-02)

F283 E1 **corrects F282 falsifier #5**: the obstruction is scale-invariant, so it cannot be
falsified by any choice of spacing. E1 and F1 are sympy-exact with every symbol left free.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Obstruction invariant under $a\to sa$ | $M_\text{Pl}/\Lambda_\text{UV}=3^{1/4}$, $r=\sqrt3$ for all $s$ | $\partial r/\partial s\equiv0$ (literal) | F283 E1 |
| Cause: $G\propto a^2$ is structural | $M_\text{Pl}=3^{1/4}\hbar/(sac)$, $\Lambda=\hbar/(sac)$ — both $\propto1/s$ | exact (sympy) | F283 E1 / F79 |
| Obstruction $=$ BCC coordination geometry | $r=1/c_\text{lat}$, independent of scale | exact | F283 E1 |
| Elastic fraction from LLR | $\dot G/G=2qH$; $q<1.09\times10^{-3}$ | 919× inside comoving | F283 E2 |
| Elastic fraction from BBN | $q<2.52\times10^{-3}$ at $z=4\times10^{8}$ | independent, agrees | F283 E2 |
| Fully comoving lattice vs BBN | $G_\text{BBN}/G_0=6.25\times10^{-18}$ | **17.20 decades off** | F283 E2 |
| Volume-mode PPN scalar (branch B) | Cassini $\Rightarrow\alpha<3.391\times10^{-3}$ | 295× suppression needed | F283 E3 |
| Tree elastic fraction from GW170817 | $f_\text{tree}<6\times10^{-15}$ | 14.22 decades | F283 E4 |
| First resolvable epoch | $H_\text{max}=c_\text{lat}/a=3^{-3/4}M_\text{Pl}=0.438691$ | exact (sympy) | F284 F1 |
| One cell-crossing | $t_\text{min}=1/c_\text{lat}=\sqrt3$ ticks $=3^{3/4}M_\text{Pl}^{-1}$ | exact (both units) | F284 F1 |
| Same epoch in SI | $t_\text{min}=6.161\times10^{-43}$ s $=11.43\,t_\text{P}$ | computed (F107 anchor) | F284 F2 |
| Quarter-power ladder closes | $H_\text{max}=c_\text{lat}\Lambda_\text{UV}$ and $r=1/c_\text{lat}$ | $<10^{-14}$ | F284 F3 |
| Hubble volume cell budget | $R_H=1.287\times10^{60}$ cells; $2.13\times10^{180}$ cells | computed | F284 F2 |
| $\dot G/G$ on a rigid lattice | $\equiv0$ **exactly** (vs $2H_0=1.379\times10^{-10}$/yr) | structural (F79) | F284 §2 |
| Correction is falsifier-only | $r$ from F282 $=$ $r$ from F283 | $<10^{-14}$ | F284 F4 |

## F285 — initial-condition measure cannot supply the tilt (2026-08-02)

Executes the three directions F284 handed on. D0 and D3 are sympy-exact for general
symbolic exponents; the measure rows are structural; the decade counts computed.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Spectral bridge from the model's own Poisson law | $P_\Phi=P_\rho/k^4$, $\Delta^2=k^3P$ $\Rightarrow$ $P_\rho\propto k^{n_s}$ | exact (sympy, general $n_s$) | F285 D0 / F106 |
| Uniform / max-entropy measure | $P_\rho\propto k^0$ $\Rightarrow$ $n_s=0$ | 230σ from Planck | F285 D1a |
| Any short-range-correlated local $\rho$ (incl. critical$^2$) | $P_\rho\to$ const as $k\to0$ $\Rightarrow$ $n_s=0$ | structural (convolution) | F285 D1a |
| Locally conserved (Traschen) initial data | $P_\rho\propto k^4$ $\Rightarrow$ $n_s=4$ | 723σ | F285 D1a |
| Scale-free in the metric ($\Delta^2_\Phi=$ const) | $n_s=1$ **exactly** (Harrison–Zel'dovich) | **8.357σ** | F285 D1a |
| Generic measures bracket without touching | $0<0.9649<4$ | — | F285 D1a |
| Pivot vs Brillouin-zone edge | $k_*/k_\text{BZ}=5.500\times10^{-59}$ | 58.26 decades | F285 D1b |
| Suppression required vs white noise | $(k_*/k_\text{BZ})^{n_s}$ | $10^{-56.21}$ | F285 D1b |
| Enhancement required vs conserved-causal | $(k_*/k_\text{BZ})^{n_s-4}$ | $10^{+176.82}$ | F285 D1b |
| Lattice imprint at the pivot | $(ka)^2=2.986\times10^{-116}$ | 115.5 decades | F285 D2 |
| BZ edge is permanently out of reach | $k/k_\text{BZ}$ time-independent (rigid, F284) | structural | F285 D2 |
| Kadanoff dilation on a power law | $Ak^n\mapsto b^{-(3+n)}Ak^n$, exponent preserved | exact, **general symbolic $n$** | F285 D3 |
| Spectral index is exactly marginal | log-slope out $-$ log-slope in $\equiv0$ | literal 0 (sympy) | F285 D3 |
| Fixed-point set of block-spin | a one-parameter **line** of power laws | exact | F285 D3 |
| Tilt magnitude needing a second scale | $\lvert1-n_s\rvert=0.0351$ vs one lattice scale at $10^{-116}$ | — | F285 D4 |

## F286 — a second scale must be a log, not a length (2026-08-02)

T1 is sympy-exact; T5 is a **pre-registered** frequentist count, and its conclusion is that
the near-miss is **rejected**. The exactness of the identity and the nullity of its
significance are separate rows on purpose.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Tilt log-derivative identity | $\lvert d\ln F/d\ln x\rvert=\lvert dn_s/d\ln k\rvert/\lvert n_s-1\rvert$ | exact (sympy) | F286 T1a |
| Power-law shape | $\lvert d\ln F/d\ln x\rvert=p$ | exact | F286 T1a |
| Log shape | $\lvert d\ln F/d\ln L\rvert=1$, so $1/L=0.00745$ | exact | F286 T1a |
| Planck-derived bound on the shape | $\lvert d\ln F/d\ln x\rvert<0.319$ | external (Planck running) | F286 T1b |
| Every length scale excluded | integer $p\ge1$ (lattice: $p=2$) vs bound $0.319$ | structural | F286 T1b |
| Class prediction, **no free parameter** | $dn_s/d\ln k=-(1-n_s)/L=-2.617\times10^{-4}$ | 25.6× below Planck 1σ | F286 T2 |
| Required coefficient is natural | $C=(1-n_s)L=4.7086$, $O(1)$ | ($3\pi/2$ to 0.08%, no weight placed) | F286 T3 |
| $\alpha_\text{em}$ one-loop tilt | $\alpha/2\pi=1.161\times10^{-3}$ | 30.2× short | F286 T4 |
| $\alpha_s$ unusable at CMB momenta | 38.3 decades below $\Lambda_\text{QCD}$ | structural | F286 T4 |
| $G$ cannot run | $\dot G/G=0$ exactly (F79 + F284) | structural | F286 T4 |
| Identity $\delta^*/2\pi=1/(9\pi)$ | $0.0353678$, $0.064\sigma$ from Planck | **exact** (arithmetic) | F286 T5 |
| Look-elsewhere count | 6 distinct hits in 396 candidates; density 3/σ | computed, family pre-registered | F286 T5 |
| Significance of that near-miss | $p=0.318$ of one this close by chance | **rejected — not evidence** | F286 T5 |

## F295 — the tilt is an anomalous dimension, not a second scale (2026-08-02)

A **correction to F286's framing**, not its algebra. A1 is sympy-exact to a literal zero.
The 2/9 row records that the *shape* argument improved while the *statistics* did not.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Constant $\gamma$ gives a pure power law | $\Delta^2\propto k^{-2\gamma}$, log-slope $=-2\gamma$ | exact (sympy) | F295 A1a |
| Its running vanishes identically | $dn_s/d\ln k=0$ | **literal 0** | F295 A1a |
| $p=0$ lies inside F286 T1's own band | $0<0.319$ | exact (T1 reused) | F295 A1b |
| Required anomalous dimension | $\gamma=(1-n_s)/2=0.017550$ | computed | F295 A1a |
| Sub-class discriminator | constant-$\gamma$ $0$ vs log-class $-2.617\times10^{-4}$ | separable at $2.6\times10^{-4}$ | F295 A2 |
| Required one-loop coupling | $g_\text{eff}=2\pi(1-n_s)=0.220540\pm0.026389$ | computed | F295 A3 |
| $\alpha$ route excluded by the model's own cutoff | $\ln(\mu/m_e)=208.1$, $\mu\sim10^{87.1}$ GeV | **68.1 decades above** $\Lambda_\text{UV}$ | F295 A3a |
| $G$ route excluded on **shape** first | $g_\text{grav}=(k/M_\text{Pl})^2$, $p=2>0.319$ | exact (T1) | F295 A3b |
| $G$ route magnitude, as corroboration only | $g_\text{grav}=1.718\times10^{-116}$ | 115.1 decades short | F295 A3b |
| Three registered constants equal $\tfrac29$ | $\delta^*$, $\sin^2\theta_W^\text{on-shell}$, $c_\text{Fierz}^\text{colour}$ | exact (registry) | F295 A4a |
| $\tfrac29$ vs required $g_\text{eff}$ | $0.2222$ vs $0.2205\pm0.0264$ | $0.064\sigma$ — **shape justified, significance still nil** | F295 A4a |

## F296 — holographic cosmology: T1 validated, operator named, naive reading excluded (2026-08-02)

L2 is the load-bearing row: it tests **our** instrument against an independent published
case. All rows are quantitative or external — nothing here is derived in this repo.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| HC spectrum from $\langle TT\rangle$, no inflaton | $\Delta^2_R=-q^3/4\pi^2/\mathrm{Im}\langle\langle TT\rangle\rangle$ | external (PRL 118 041301) | F296 L1 |
| HC coupling is dimensionful ⇒ $p=-1$ | $g^2_\text{eff}=g^2_{YM}N/q$ | structural | F296 L2a |
| **T1 diagnostic on HC's own fit** | $\lvert d\ln F/d\ln x\rvert=0.6754$ | **2.11× over T1's 0.32** | F296 L2a |
| HC tilt at its fitted point | $n_s-1=-0.02230$ ($g=-0.00703$, $\ln\beta=0.877$) | computed | F296 L2a |
| Implied HC running | $dn_s/d\ln k=+0.01506$ | **2.92σ** from Planck | F296 L2b |
| Agreement with published disfavour | $2.92\sigma$ computed vs $2.2\sigma$ published | retrodiction | F296 L2b |
| Model's branch is $f_1=0$ (conformal, $p=0$) | unanalysed in the literature | citation (PRL fn. 2) | F296 L3 |
| Operator carrying $\gamma$ | $T^i{}_i$, 3D stress-tensor trace | external identification | F296 L4 |
| $\gamma$ required | $0.017550$ | agrees with F295 | F296 L4 |
| $r$ from the model's own content, conformal $\xi=\tfrac18$ | $r=0.32323$ | **9.0× over BK18** | F296 L5a |
| $r$ from the model's own content, minimal $\xi=0$ | $r=0.96970$ | **26.9× over BK18** | F296 L5a |
| Scalars needed to reach $r<0.036$ | $N_\Phi>792$ (model has 2) | 396× short | F296 L5a |
| Naive holographic reading | **excluded** | — | F296 L5b |

---
## F287 — F162 background-field apparatus, soundness post-F272/F277 (2026-08-02)

| Quantity | Value | Exactness | Source |
|---|---|---|---|
| 4D kernel period: $\sqrt3\cdot2\pi(1,1,0,0)$ | $\max\lvert\Delta K\rvert=1.4\times10^{-14}$ | machine (is a period) | F287 A |
| 4D kernel period: $\sqrt3\cdot2\pi(2,0,0,0)$ | $\max\lvert\Delta K\rvert=2.1\times10^{-14}$ | machine (is a period) | F287 A |
| The refold $2\pi(1,0,0,0)$ is **not** a period | $\max\lvert\Delta K\rvert=76.49$ | measured (falsifies) | F287 A |
| Euclidean-**time** leg has no period at all | $\max\lvert\Delta K\rvert=78.80$ at $2\pi(0,0,0,1)$ | measured (new vs F277) | F287 A |
| Rule shift grid-convergence, $n=22\to26$ | rel. step $1.80\times10^{-4}$ (refolded: 70% at $n{=}14\to18$) | measured, convergent | F287 B |
| Rule shift $q$-flatness at $n=26$ | spread $1.783\times10^{-5}$ | measured | F287 B |
| Wilson control convergence, $n=22\to26$ | rel. step $3.42\times10^{-5}$ | measured | F287 C |
| S11-F272 baseline reproduced by an independent integrator | $-0.0125910487428$ vs $-0.0125910487433$ | $5\times10^{-13}$ | F287 §3 |
| $b_0$ recovered **numerically** (abs., $n=40$) | $10.5064$ vs exact $11$ — recovery $0.9551$ | measured, **not** exact — see below | F287 D1 |
| Lattice/continuum log-slope ratio (rule, $n=40$) | $1.0014117$ (target exactly 1) | measured, converging to identity | F287 D2 |
| Both ratios extrapolate to exactly 1 | rule deficit $\sim n^{-1.77}$, wilson $\sim n^{-1.60}$, both $\to0$ | measured power law, $n=26/32/40$ | F287 D2 |
| Near-perfect action in the $b_0$ slope | rule discretisation error $5.27\to5.68\times$ **smaller** than Wilson | measured, monotone | F287 D2 |
| Absolute normalisation is **unusable for $d_1$** | 4.5% deficit at $n=40$; cube is not a fundamental domain | open (F267/F277 §8) | F287 §6 |
| Sub-cell-$Q$ hazard reproduces | $b_0=4.06$ (37% of true) with fit residual $1.0\times10^{-3}$ | measured, guarded | F287 D diag. |

Finding `F287-bgfield-apparatus-sound-post-F277.md`; record `F287-bgfield-apparatus-postF277`
(`tests/runners/run_f287_bgfield_apparatus.py`, 6/6). **Verdict: the F162 apparatus is SOUND**
— but sound *for subtracted differences only*. The two rows that matter downstream are the
absolute-normalisation deficit (which is why $d_1$ cannot be read off this quadrature) and the
log-slope ratio (which is the universality identity being recovered rather than a tolerance
met). No engine module, constant or committed baseline changed. Relates to row 340 (F278:
the $\sqrt3$ factor is the BCC$\to$fcc reciprocal), which supplies the structural reason.

## F291 — why $d=3$: two independent selectors (2026-08-02)

Rubric row A1 (the first ABSENT entry). Everything is exact over $\mathbb Z$/$\mathbb Q$
(sympy, re-derived independently of the module) except the engine cross-check, which finite-
differences `bcc._bcc_uvec` and is therefore machine. All statements are about
$J=\partial\tilde{\mathbf n}/\partial\mathbf k\big|_{\mathbf k=0}:\mathbb R^{d}\to\mathbb R^{3}$.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Internal vector dimension | $\dim\{\text{traceless Hermitian }2\times2\}=3$; anticommuting $\equiv$ orthogonality in $\mathbb R^3$ | exact (sympy) | F291 A1 |
| Bloch Jacobian rank | $\operatorname{rank}J=\min(d,3)$ for $d=1,2,3$; $\le3$ by counting for $d\ge4$ | exact (sympy) | F291 A2 |
| **S1** upper bound | $\ker J=0\iff d\le3$; isotropy makes a nonzero kernel the trivial automaton | exact (sympy) | F291 B1 |
| **S2** lower bound | $\dim\operatorname{coker}J=3-d$; isotropy-invariant intra-branch mass exists iff $\operatorname{coker}J\ne0$ | exact (sympy) | F291 B2 |
| $d=2$ intra-branch mass exhibited | $m\sigma_z$ commutes with $e^{-i\theta\sigma_z/2}$; Hermiticity $\Rightarrow m$ real, no phase | exact (sympy) | F291 B2 |
| $d=3$ has none | $[\mathbf a\cdot\boldsymbol\sigma,\sigma_i]=0\ \forall i\Rightarrow\mathbf a=0$ | exact (sympy) | F291 B2 |
| S1 $\wedge$ S2 | $\{1,2,3\}\cap\{d\ge3\}=\{3\}$ | exact | F291 B3 |
| **S3** magnetic field is a vector | $d(d-1)/2=d$ over $\mathbb Z$ has roots $\{0,3\}$ | exact (sympy) | F291 C1 |
| S3, no $d=7$ loophole | $\star\Lambda^2=\Lambda^1\iff d-2=1$; $\dim\Lambda^2\mathbb R^7=21\ne7$ | exact (sympy) | F291 C1 |
| Orientation corollary | $\det J$ exists only at $d=3$; $\det J=\mp3^{-3/2}=\mp c_\text{lat}^{3}$, sign $=$ helicity branch | exact (sympy) | F291 D1 |
| Engine cross-check | finite-difference $J$ from `bcc._bcc_uvec` vs symbolic | $3.20\times10^{-14}$ | F291 D2 |
| $\lvert\det J\rvert$ vs constants registry | $=c_\text{lat}^{3}$ | $3.21\times10^{-14}$ | F291 D2 |
| Verdict | S1$\wedge$S2 $=\{3\}$ **and** S3 $=\{3\}$, independently | exact | F291 E1 |

Finding `F291-why-three-plus-one-dimensions.md`; record `F291-dimension-selectors`
(`tests/findings/test_F291_dimension_selectors.py`, 9/9, gate tier). **S3 references the cell
dimension $s$ nowhere**, so the result does not rest on BDPT's minimality postulate; S1/S2 do,
and that is the stated boundary. The "+1" was `structural` (single update unitary) and was
deliberately **not** in this table; **F313 moves it in** — see the next section. No engine module,
constant or committed baseline changed.

## F313 — the "+1": one time from the update's commutant (2026-08-12)

Rubric row A1's remaining residual, and the step F291 §7 priced: *"explain why the
Cayley-graph/update split is not itself a choice."* It is not assumed here — it is the
$\det$-splitting of the update's own commutant. Local homogeneous operators are $2\times2$
matrices over $R=\mathbb C[w_1^{\pm1},w_2^{\pm1},w_3^{\pm1}]$, $w_j=e^{ik_j/\sqrt3}$, where
**"local" is exactly "Laurent"**. Every leg is exact over $\mathbb Q(i)$ or $\mathbb Z$ except the
composite-cell measurement, which is a commutator norm and therefore machine.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Commutant dimension | $\dim\{B:[B,A]=0\}=2$, spanned by $\mathbb I$ and $\boldsymbol\sigma\cdot\tilde{\mathbf n}$ | exact (sympy) | F313 C1b |
| No room at $s=2$ | a $2\times2$ unitary is a phase or has distinct eigenvalues — no third option | exact | F313 C1a |
| Traceless part is free rank 1 | $\gcd(\tilde n_1,\tilde n_2,\tilde n_3)=\mathbf 1$ over $\mathbb Q(i)$, a **unit** of $R$ | exact (sympy) | F313 C2 |
| Shifts are all present | $\zeta w^{\mathbf m}$ satisfies $aa^*=1$ | exact (sympy) | F313 C3a |
| **Nothing but shifts is scalar** | $aa^*=1\Rightarrow a$ a unit of $R\Rightarrow a$ a monomial; scalar part $=U(1)\times\mathbb Z^{3}$ | exact (sympy) | F313 C3b |
| Discriminant squarefree | $N=(1-u)(1+u)$, both **irreducible** in $R$ and distinct | exact (sympy) | F313 C4a |
| Update is the fundamental unit | $(a,b)=(u,-i)$ solves $a^2-b^2N=1$ with $\deg b=0$, the minimum for $b\ne0$ | exact (sympy) | F313 C4b |
| Pell tower is Chebyshev | $A^{n}=(T_n(u),\,-i\,U_{n-1}(u))$, $n\le8$, module ring vs sympy recurrence | exact ($\mathbb Q(i)$) | F313 C5a |
| Degree growth | $\deg b(A^{n})=n-1$ exactly | exact | F313 C5a |
| Abel descent | $\deg b$ falls by exactly 1 per step, strictly, lands on $\mathbb I$ in exactly $n$ steps | exact | F313 C5b |
| Update order | $A^{n}$ never a monomial $\times\,\mathbb I$ $\Rightarrow\langle A\rangle\cong\mathbb Z$ | exact | F313 C5c |
| The count at $s=2$ | $(d_\text{space},d_\text{time})=(3,1)$ — **two** statements sharing the $s=2$ premise | exact ($\mathbb Z$) | F313 C6 |
| $s$-general identity | ~~$(\dim\mathfrak{su}(s),\operatorname{rank}\mathfrak{su}(s))$~~ | **WITHDRAWN 2026-08-13** — numerology | review attack 5 |
| Non-tautology control | $d=1$: $\gcd=\sin k$ not a unit **and** $N=\sin^2k$ a perfect square — the theorem correctly **fails** | exact (sympy) | F313 C0 |
| Composite residual | $[\,\mathbb I\otimes A,\ D_\text{Dirac}\,]=0$ at $m=0,\,0.37,\,0.8$ | $2.22\times10^{-16}$ | F313 C7 |

Finding `F313-one-time-dimension-from-the-update-commutant.md`; record `F313-time-signature`
(`tests/findings/test_F313_time_signature.py`, 13/13 after remediation, gate tier, **three controls
verified RED**); claim card **CL269**.

**REMEDIATED 2026-08-13** after `docs/reviews/F313-review-2026-08-13.md` graded the finding
OVERSTATED. Changes visible in this table: the gcd row's value corrected $1+i\to\mathbf 1$ (the
old value was a sympy `ZZ_I` content artifact — the correct domain is $\mathbb Q(i)$, since $R$ has
coefficients in a field); the merged-coincidence row **withdrawn**, which matters because the
review's fair complaint was that *the least supported thing in the finding carried the highest
exactness label in the repo*; and the C0 row added, which is the review's own best check — in
$d=1$ the theorem **fails** on both load-bearing legs, so the 3D result is not a tautology about
the algebra.

**The import is GONE as of 2026-08-13.** The rank-one step was mis-attributed to Abel (whose 1826
paper has no group-structure theorem); the correct source is Pastor (2001) / Dubickas–Steuding
(2004) Thm 2, and the genuine gap was the **polynomial→Laurent transfer**, since D–S needs
"$\deg f=0\Rightarrow f$ constant", which fails in $\mathbb C[w^{\pm}]$. **F316 proves the
transfer in-repo** — see its section below — so F313's chain now cites nothing. **Inputs are three, not one**: $s=2$, **infinite volume**, and the three
Cayley generators. The $s=4$ composite residual (C7 row) is **settled** by F315 — see the F315
section. No engine constant or committed baseline changed.

## F315 — falsifier 5: the second clock does not survive interaction (2026-08-12)

F313's composite-cell residual, run and closed. Homogeneous antisymmetrised two-particle sector at
fixed total momentum; modes in the **joint** eigenbasis of $D(k)$ and $V(k)$ (which exists because
F313 gave $[V,D]=0$), so each mode carries both $\Omega_a(k)$ and $\phi^V_a(k)$. The class is
`machine` — every quantity is a commutator, phase difference or degeneracy count — except the
$L=2$ degeneracy, which is exact.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Joint diagonalisation | one generic Hermitian combination diagonalises $D$ and $V$ at once | $2.0\times10^{-15}$ | F315 C1 |
| Free limit | $[V,D]=0$ at $N=2$ — the F313 C7 recovery | $<10^{-12}$ | F315 C1 |
| **Integrable control** | mode-diagonal $H_\text{int}$ ⇒ $V$ conserved | obstructed $=\mathbf 0$; $\max\lvert\Delta\phi_V\rvert=0.0$ | F315 C2 |
| Contact kernel (F217/F77) | $V$ broken | $\max\lvert\Delta\phi_V\rvert=3.1130$ over 44 618 live elements | F315 C3 |
| Photon exchange (F68, $1/q^2$) | $V$ broken, same magnitude | $\max\lvert\Delta\phi_V\rvert=3.1130$ | F315 C4 |
| **$O(G)$ deformation obstructed** | resonant elements ($\Delta\Omega\equiv0$) with $\Delta q_V\ne0$ | 1 340 of 1 930; $\max\lvert\Delta q_V\rvert=2.876$ | F315 C5 |
| Control on the resonant set | the evolution's own charge is conserved there | $1.8\times10^{-15}$ | F315 C6 |
| Robustness in $K$ | obstructed at $(0,0,0),(1,0,0),(1,2,0)$ | 5 132 / 2 152 / 1 340 | F315 C7 |
| Robustness in $m$ | obstructed at $m=0,\,0.37,\,0.8$ | all $>0$ | F315 C8 |
| $L=2$ degeneracy | $\sin\theta_j\equiv0\Rightarrow\tilde{\mathbf n}\equiv0$, walk trivial | exact ($\mathbb Z$) | F315 C9 |
| $\langle100\rangle$ linearity | $\omega=\lvert k\rvert/\sqrt3$ exactly on-axis | $9.3\times10^{-15}$ | F315 C10 |
| $\langle100\rangle$ does **not** go blind | umklapp breaks additivity despite exact linearity | 2 592 obstructed | F315 C10 |

Finding `F315-V-does-not-survive-interaction.md`; record `F315-V-interaction`
(`tests/findings/test_F315_V_interaction.py`, 11/11, gate tier, **three controls verified RED**);
claim card **CL270**, and **CL269's composite-cell contingency discharged**. The C10 row records a
**prediction of the session that was wrong** — the on-axis line was expected to go blind and does
not — kept because it changes the stated mechanism from lattice curvature to the mod-$2\pi$ folding
of a QCA eigenphase. **Two residuals stay named**: the obstruction is **leading order in $G$**, not
an all-orders proof, and the **F86 colour dielectric** (named in F313's falsifier 5) is not tested.

## F316 — the polynomial->Laurent transfer, proved (2026-08-13)

F313's last import, closed. Dubickas-Steuding Thm 2 runs on $k[x]$ with a degree obeying
"$\deg f=0\Rightarrow f$ constant" — **false** in a Laurent ring. Class is `machine` because the
coefficient arithmetic is exact over $\mathbb Q(i)$ but the support function is evaluated against
an irrational $\lambda$, so the **separation** statements are float comparisons with a reported gap.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Genericity | unique $\lambda$-maximiser ⇒ $h_{fg}=h_f+h_g$, $\mathrm{lc}(fg)=\mathrm{lc}(f)\mathrm{lc}(g)$ | both **0.0**; min maximiser gap $2.0$ | F316 C1 |
| **$D$ detects units** | $D(f)=0\iff f$ monomial $\iff f$ unit — on the counterexample $1+w_1^{-1}$, which has $\deg=0$ and is **not** a unit | $D=1.0>0$; monomials $0.0$ | F316 C2 |
| Unitarity ⇒ central symmetry | $a^*=a$, $b^*=-b$ ⇒ $h(\lambda)=h(-\lambda)$ | $0.0$ | F316 C3 |
| $h_a=h_b+c$ | $D(a)=D(b)+D(u)$ | $3.6\times10^{-15}$ | F316 C4 |
| Leading sign | $\mathrm{lc}(a)=\pm i\,\mathrm{lc}(b)\,\mathrm{lc}(u)$ ⇒ exactly one of $bu\pm ai$ cancels | exact | F316 C5 |
| Product identity | $b'b''=1+b^2$; $D(1+b^2)\le2D(b)$ | exact in the ring | F316 C6 |
| **The descent** | $D(b)$ drops by $\ge D(u)=2c$; measured **exactly** $2c$ | 6 live steps, all strict | F316 C7 |
| Base case | $\mathrm{Newt}(u)$ has **8** monomials ⇒ $u$ is not a difference of two | exact ($\mathbb Z$) | F316 C8 |
| Hypothesis is load-bearing | at $D(b)=0$, $1+b^2=0$ and C6 degenerates | exact | F316 C9 |
| $\lambda$-independence | same verdict under a second $\mathbb Q$-independent direction | agree | F316 C10 |

Finding `F316-laurent-pell-descent-proved.md`; record `F316-laurent-pell`
(`tests/findings/test_F316_laurent_pell.py`, 10/10, gate tier, **three controls verified RED**);
**CL269 moves `contingent → live`, `confidence: medium → high`.** The control worth recording is
`degenerate_lambda`: the first draft used $\lambda=(1,2,3)$, which is $\mathbb Q$-dependent yet
still separates these supports, and it **leaked green** — *blindness*, not irrationality, is the
real hypothesis, and the leak is what showed it. **Scope, stated rather than implied:** this is
proved for *this* $N$ under unitarity; it is not a re-proof of D-S in several variables.

## F292 — why not a higher multiple of three (2026-08-02)

Follow-up to F291, same rubric row A1. **Every leg is exact over $\mathbb Z$ or $\mathbb Q$ —
this finding contains no floating-point step at all.** The Clifford recursion behind S4 is
written twice (module and test, separately typed), so B2 is a cross-check rather than a repeat.

| Construct | Predicted form | Measured residual | Source |
|---|---|---|---|
| Bivector overcount, closed form | $\dim\Lambda^2\mathbb R^{d}/d=(d-1)/2$ | exact (sympy) | F292 A1 |
| **S3′** passes through 1 exactly once | $(d-1)/2=1 \Rightarrow d=3$; at $d=3n$ only $n=1$ | exact (sympy) | F292 A1 |
| $d=6,9,12$ overcounts | $\tfrac52,\ 4,\ \tfrac{11}2$ | exact | F292 A1 |
| Integer-root form | $d(d-1)/2=d$ has roots $\{0,3\}$ | exact (sympy) | F292 A2 |
| Clifford algebra valid | $\{\gamma_a,\gamma_b\}=2\delta_{ab}$ in $\dim 2^{\lfloor D/2\rfloor}$, $D=2\ldots8$ | exact (sympy) | F292 B1 |
| **S4** chirality parity | $\gamma_1\cdots\gamma_D\propto\mathbb I \iff D$ odd; chirality $\iff d$ odd | exact (sympy) | F292 B2 |
| $d=6$ has no chirality | $D=7$ odd $\Rightarrow$ no projector for decision 1 to gauge | exact | F292 B2 |
| $d=9$ clears S4, fails S3′ | $D=10$ even; overcount 4 | exact | F292 B2/A1 |
| S4 / S2 cross-check at $d=2$ | no chirality ($D=3$) **and** real $\sigma_z$ mass — unrelated routes | exact | F292 B3 |
| Reducible $d=3n$, $n$ copies of $\mathbb R^3$ | $\operatorname{rank}J=3$, $\ker J=3(n-1)$, $\operatorname{coker}J=0$ | exact (sympy) | F292 C1 |
| Founding decision 1 survives the reducible case | $\operatorname{coker}J=0$ for all $n$ | exact | F292 C1 |
| Minimal cell does not rescue | $2^{\lfloor d/2\rfloor}$: $d=6\to s=8$, $d=9\to s=16$; S3′/S4 are $s$-free | exact | F292 C2 |

Finding `F292-no-higher-multiple-of-three.md`; record `F292-higher-multiples`
(`tests/findings/test_F292_higher_multiples.py`, 8/8, gate tier). The frozen $3(n-1)$ directions
are a **leading-order** statement — the model has no $3n$ walk to supply $O(k^2)$ terms — but any
such term is irrelevant under F130's measured $\lambda_n=b^{-n}$, and the finding says so rather
than over-claiming. The §6 generations resemblance is recorded and **declined**; B10 untouched.

## F280 — $d_1$ subtracted against the Wilson anchor (2026-08-05)

| Result | Value / residual | Class | Where |
|---|---|---|---|
| Master identity $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=28.8086\,e^{-(T_W+\delta_\text{loops})/2}$ closes against the direct form | $6.7\times10^{-16}$ | exact (bookkeeping) | F280 S1 |
| Slope-normalised constant $\hat C$ invariant under a measure factor $\lambda$ | $3.1\times10^{-15}$ | exact | F280 S2 |
| Analytic-normalised constant drifts by its closed form $2(\lambda-1)\langle\ln(1/Q)\rangle+(\lambda-1)C_0$ | matched $<10^{-12}$ | exact | F280 S2 |
| Target $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=e^{11/42}/q_\ast a$ derived, not written | $1.773444$ | exact (given $q_\ast a$) | F280 §2 |
| Three-leg budget closes | $0.0$; leg1$+$leg3 anchor-fixed | exact | F280 S4 |
| Propagator leg, both normalisations, $1/n^2$ Richardson | $-0.9919\pm0.0439$ | quantitative | F280 S3 |
| Tadpole-free band contains the target, excludes Wilson | $[1,\,7.980]\ni1.7734$; $28.8086$ out by $3.61\times$ | bracketed | F280 S5 |
| Open vertex leg | $-2.0160\in[-2.257,-1.446]$, 36.2% of the shift | bracketed | F280 S6 |

Finding `F280-d1-subtracted-against-wilson.md`; record `F280-d1-subtracted`
(entry `check_d1_subtracted`, 6/6 + control, gate tier). The band's **upper** edge carries a named
monotonicity assumption (the rule is nearer the continuum than Wilson — F129/F130, measured
5.3–5.7$\times$ in F287 §4) and is labelled as an assumption in the module, the finding and CL252.
The absolute quadrature normalisation F287 §6 forbids is **not used anywhere**: every term in the
identity is a difference.

## F288 — structure formation with zero free functions (2026-08-05)

| Claim | Value | Class | Where |
|---|---|---|---|
| $AB\equiv1$ ⇒ linear gravitational-slip coefficient | **literal 0** (sympy) | exact | F288 S1 |
| Residual slip, second order | $\eta-1=2\Phi\approx2\times10^{-5}$ | exact + computed | F288 S1 |
| F106 ⇒ Poisson coefficient | $\mu=1$; $\partial\mu/\partial k=$ **literal 0** | exact | F288 S2 |
| Growth index | $\gamma_g=6/11$ | **exact algebraic** | F288 D1 |
| Amplitude leg: $f\to1$ as $\Omega_m\to1$ | $c=(\sqrt{1+24\mu}-1)/4=1$ iff $\mu=1$ | exact | F288 D1 |
| Meszáros growing mode | $D(y)=1+\tfrac32y$, residual **literal 0** | exact | F288 D2 |
| Meszáros decaying mode | residual 0 | exact | F288 D2 |
| $D(a{=}1)$ vs Carroll–Press–Turner | $0.78799$ vs $0.78719$, $+0.10\%$ | quantitative | F288 D3a |
| Radiation-convention sensitivity of $f$ | $3.8\times10^{-5}$ | quantitative | F288 D3a |
| $f\sigma_8$ vs 7 RSD points (diagonal $\chi^2$) | $\chi^2/N=1.012$, max pull $1.8\sigma$ | quantitative | F288 D3b |
| $\sigma_8$ from a **free** $A_s$ | $0.8204$, $+1.15\%$ vs Planck $0.8111$ | quantitative | F288 D4 |
| $\mu$ pinned by growth, amplitude-anchored | $[0.986,\,1.008]$ at 1σ | quantitative | F288 D5 |
| Discreteness at $8\,h^{-1}$ Mpc | $8.5\times10^{-116}$ | bound | F288 B1 |
| Discreteness at Lyman-α | $1.3\times10^{-112}$ | bound | F288 B1 |
| $\sigma_8$ suppression, 5.6 keV sterile | $2.7\times10^{-6}$ — blind | quantitative | F288 B2 |
| Control: $\mu=0.90$ | 3 legs red, $\sigma_8$ $-32.0\%$, $\Delta\chi^2=+86.0$ | control | F288 C1 |

Finding `F288-structure-formation-zero-free-functions.md`; record
`F288-structure-formation-growth` (entry `run`, 13/13, gate tier); claim card CL254.
$\sigma_8$ is **reported, not claimed** — it is linear in $\sqrt{A_s}$ and $A_s$ is provably free
(K5). The $\approx1\%$ residual after the $\sum m_\nu=0.06$ eV correction is the **imported**
Eisenstein–Hu no-wiggle $T(k)$, not a model residual, and the finding says so in the same table as
the number.

### F300 — G10 lattice thermodynamics (quantitative legs)

| Leg | Measured | Class | Source |
|---|---|---|---|
| Fine-grained von Neumann entropy under the model's own walk, on a **mixed** state ($S_0=591.27$ nats) | drift $\le1.1\times10^{-12}$ over $t=1,17,101$ | machine | F300 G10-7 |
| Branch occupations $n_\pm(k)$ conserved — $2N$ charges, hence a GGE and not Gibbs | $5.4\times10^{-14}$ | machine | F300 G10-8 |
| Coarse-grained entropy $0\to$ plateau at subsystem fraction $1/8$ | $4.3\times10^{-11}\to79.96\pm0.46$ nats | quantitative | F300 G10-9 |
| Plateau $\to$ GGE as the subsystem fraction falls ($1/2$, $1/8$, $1/64$, $1/512$) | $0.5539$, $0.9012$, $0.9872$, $0.9978$ | quantitative | F300 G10-10 |
| **Time reversal**: $S_A(-t)$ rises as $S_A(+t)$ does — the arrow is the initial condition, not the dynamics | $79.943$ vs $79.957$, $1.8\times10^{-4}$ | quantitative | F300 G10-11 |
| Radial-cut (zone-boundary) independence of the EoS at $\Theta=0.005$, $x_\text{max}=45\to75$ | $3.7\times10^{-9}$ relative | control | F300 G10-6b |
| Per-cell capacity vs F190's requirement: $96\ln2=66.542$ nats against $2\pi\sqrt3=10.883$ | $6.11\times$ surplus; horizon occupies 16.4% | quantitative | F300 G10-13 |
| $w=1/3$ margin at the BBN bottleneck (1 MeV), grading F297's continuum assumption | $\tfrac13-w=1.2\times10^{-44}$; $w$ within 1% below $6.2\times10^{30}$ K | quantitative | F300 §3.1 |

Finding `F300-lattice-native-thermodynamics.md`; record `F300-lattice-thermodynamics`
(entry `check_g10`, 15/15, gate tier); claim cards CL260 and CL261. Two declared controls, each
verified red and only where declared: `linear_control=True` reddens G10-3/4/5/6,
`nonunitary_control=True` reddens G10-7/9/10. The equation of state is the **equilibrium** measure
on the derived dispersion; the same finding shows the free sector does not dynamically reach it,
and those are two different statements.

### F301 — A2 finite-$a$ boost covariance: the Poincaré defect (2026-08-06)

The observable is $D_i=\frac1{2c^2}\partial_i(\Omega^2)-k_i=\partial_i\Phi$ with
$\Phi=(\Omega^2-c_\text{lat}^2\lvert k\rvert^2)/2c_\text{lat}^2$. Four algebraic legs establish
that this *single* scalar is the whole obstruction for **arbitrary** $\Omega$, which is why the
result is not a property of a chosen lattice boost. Every numeric residual below is
**truncation**-limited with its order separately verified, not tolerance-limited.

| Leg | Predicted form | Measured residual | Class | Source |
|---|---|---|---|---|
| $[K_i,P_j]=i\delta_{ij}\Omega/c^2$ for arbitrary $\Omega$ | no defect, any dispersion | sympy $0$ | exact | F301 B10 |
| $[K_i,H]-iP_i=iD_i$, and $D_i=\partial_i\Phi$ | the defect is a **gradient** | sympy $0$ | exact | F301 B10 |
| $[K_i,K_j]$ defect $=\frac{i}{c^2}(D_ix_j-D_jx_i)$ | no second obstruction | sympy $0$ | exact | F301 B10 |
| $D_i$ invariant under $K_i\to K_i+f(\mathbf k)$ | not an artifact of the minimal $K$ | sympy $0$ | exact | F301 B10 |
| Massive BCC mass shell | $\sin^2\omega-(1-m^2)\sin^2\omega_0=m^2$ identically | $1.3\times10^{-46}$ | exact | F301 B1 |
| $\langle100\rangle$: $\omega=c_\text{lat}\lvert k\rvert$ and $\mathbf D=0$ to **all** orders, both branches and the even law | exact covariance on the cubic axes | $3.5\times10^{-46}$ | exact | F301 B2 |
| $c_2(\hat k)=-\tfrac16\hat k_x\hat k_y\hat k_z$ vs F246's two published numbers $-\sqrt3/54$, $-\sqrt6/108$ | closed form where F246 had numbers | $5.5\times10^{-48}$ | exact | F301 B4 |
| Deformed $(E,P)$ shell, boosted shell, and group closure | $E^2-c^2\lvert P\rvert^2=m^2$ at finite $a$, every $m$ | $1.3\times10^{-46}$ / $4.4\times10^{-47}$ | machine | F301 B8 |
| Even-law radial defect | $\mathbf D\cdot\hat k=-\tfrac1{18}(p+3q)\lvert k\rvert^3$; anchors $-2/81$, $-1/72$, $-11/648$, $0$ | $1.7\times10^{-17}$ | machine | F301 B3 |
| Even-law full vector | $D_x=-\frac{\lvert k\rvert^3}{36}\hat k_x(\hat k_y^2+\hat k_z^2)(1+3\hat k_y^2\hat k_z^2)$ | $8.3\times10^{-13}$ rel. — the **binding** tolerance | machine | F301 B3 |
| Chiral $k^2$ dispersion term | $b_2(\hat k)=-\tfrac13\hat k_x\hat k_y\hat k_z$ | $7.9\times10^{-14}$, residual verified $O(\lvert k\rvert^2)$ to $2.1\times10^{-5}$ | machine | F301 B4 |
| Chiral-branch defect, one order worse than the photon | $\mathbf D^{(s)}=-s\,c_\text{lat}(k_yk_z,k_zk_x,k_xk_y)$ | $7.4\times10^{-18}$ rel. | machine | F301 B5 |
| Universality gap — the no-go leg | $\Omega_\text{even}-\omega_+=\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2$ | $7.9\times10^{-14}$ | machine | F301 B9 |
| Off-shell residual of the linear boost | $\Omega'-\Omega(\mathbf k')=v(\mathbf D\cdot\hat v)+O(v^2)$ | $1.4\times10^{-14}$ at $v=10^{-13}$, scaling verified | machine | F301 B7 |
| 1D reduction reproduces F22 | $D/k=1/\rho-1=2\beta_\text{LV}/(1-2\beta_\text{LV})$ | 12 figures at four masses | machine | F301 B6 |
| BCC massive branch, same $\rho(m)$ F22 said had no BCC analogue | $D_i\to(1/\rho(m)-1)k_i$ | $4.7\times10^{-15}$ rel. | machine | F301 B6 |
| Control: chirality-odd cancellation is a **suppression**, not a small number | $\lvert D^{(+)}+D^{(-)}\rvert/\lvert D^{(+)}\rvert$ halves with $\lvert k\rvert$ | $8.8\times10^{-3}\to4.4\times10^{-3}$ | control | F301 B5 |
| Control: even-law $c_2$ against single-law $c_2$, same fit and samples | differential, not a fit artifact | $-1.2\times10^{-13}$ vs $-0.03207501496$ | control | F301 B4 |
| Control: universality gap must **vanish** on a coordinate plane | $\hat k_x\hat k_y\hat k_z=0$ | $4.8\times10^{-8}$ | control | F301 B9 |
| Controls: wrong $n^2$ (+1%), $\langle111\rangle$ vs axis, F22's wrong $\rho=m/\arcsin m$, canonical $\mathbf k$ on the deformed shell, $D_i+k_i/100$ | all must fail | $9.9\times10^{-4}$, $1.8\times10^{-3}$, $0.14$, $2.1\times10^{-2}$, symbolically non-zero | control | F301 B1/B2/B6/B8/B10 |

Finding `F301-finite-a-boost-covariance-poincare-defect.md`; record
`F301-boost-covariance-defect` (entry `check_boost_covariance`, 10/10, gate tier, 1.7 s).
**Free inputs: zero.** The record is labelled `machine` rather than `exact` **deliberately**: seven
legs are sympy zeros or $10^{-46}$, but the record asserts everything it checks and the binding
tolerance is the largest one, $8.3\times10^{-13}$. A2 stays `PARTIAL` — this finding is the reason
it is not `EXACT` — but its residual is no longer "unaddressed".

### F310 — K3/G2: $\gamma$ is a block-spin eigenvalue, and the model needs no 3D dual (2026-08-11)

The $t=0$ state of a rigid 3D automaton (F284) **is** a measure on 3D field configurations, so the
3D theory holographic cosmology reaches for *by duality* is present here by construction. Feeding
that through F285's own Poisson bridge with $\Delta_\varepsilon=d-1/\nu$ gives the identity below.
Every leg marked exact is a sympy zero or a literal integer; **no leg uses quadrature**, which is
why the record's `tol` is $0$ rather than a floor.

| Leg | Predicted form | Residual / value | Class | Source |
|---|---|---|---|---|
| $n_s=2\Delta_\varepsilon-3=3-2/\nu=3-2y$ | the tilt is a scaling dimension of the $t{=}0$ measure | sympy identity | exact | F310 C1 |
| $\gamma\equiv\tfrac12(1-n_s)=y-1$ — **the operator identification** | $\gamma$ *is* the anomalous part of the block-spin eigenvalue, $\lambda=b^{1+\gamma}$ | sympy $0$ | exact | F310 C1 |
| Poisson bridge reproduces F285: $\Delta^2_\Phi\propto k^{n_s-1}$ | consistency with F285 S1 | sympy $0$ | exact | F310 C1 |
| $\nu=1$ (spherical / $N{\to}\infty$) | $n_s=1$ exactly (Harrison–Zel'dovich) | integer $1$ | exact | F310 C1 |
| $\nu=\tfrac12$ (Gaussian / mean field) | $n_s=-1$ exactly | integer $-1$ | exact | F310 C1 |
| **Correction to F285 D1 row 2** — critical Gaussian squared | $P_\rho=\dfrac{2\pi}{k}\!\int_0^\infty\!\dfrac{dx}{x}\ln\left\lvert\dfrac{1+x}{1-x}\right\rvert=\dfrac{\pi^3}{k}$, so $n_s=-1$, **not** $k^0$ | bracket $=\pi^2/2$ in two closed halves; no quadrature | exact | F310 C2 |
| Gapped sub-case (where F285 is right) | analytic at $k=0$ ⇒ $n_s=0$ | — | exact | F310 C2b |
| F130's measured Kadanoff spectrum is **all integers** | $b^0$, $b^{+1}$, $b^{-n}$, $b^{-2}$, $b^{-2}$ — no anomalous dimension anywhere | 5 of 5 integer | exact | F310 C3 |
| F130's own $y=1$ through C1 | $n_s=1$ exactly ⇒ excluded at $8.36\sigma$ / $\mathbf{9.94\sigma}$ / $\mathbf{9.38\sigma}$ | prediction exact; $\sigma$ computed | exact | F310 C4 |
| $\Delta_T=d$ (stress tensor protected by conservation) ⇒ $n_t$ | $n_t=2$ **exactly**, strongly blue | sympy $0$ | exact | F310 C6 |
| $\log_{10}r(k_*)$ at $58.26$ decades below the BZ edge | $-118.56$ / $-118.37$ / $-118.10$ vs BK18 $r<0.034$ | zero free parameters | quantitative | F310 C6 |
| $dn_s/d\ln k$ at a critical point | identically $0$ — reproduces F295 A1 from the new structure | sympy $0$ | exact | F310 C7 |
| Required eigenvalue | $y=1.017550$ / $1.015900$ / $1.013600$; $\gamma=1.36$–$1.76\%$ | — | quantitative | F310 C5 |
| $1/N$ target — **asserted not to be a derivation** | $N_\text{req}=62.7/69.1/80.6$; model counts $48,96,110,192$ give $-2.6\sigma$ to $+5.7\sigma$; **no hit** | closest $+1.53\sigma$ | quantitative | F310 C8 |
| Control: $\Delta_T\to d+\tfrac12$ | $n_t\ne2$ must redden C6 | verdict flip, verified RED | control | F310 |
| Control: inject one non-integer exponent ($1.0176$) | C3 must redden — a scan that cannot see the thing it claims absent is not evidence of absence | verdict flip, verified RED | control | F310 |

Finding `F310-gamma-is-a-blockspin-eigenvalue.md`; record `F310-critical-measure`
(entry `check_critical_measure`, **16/16**, gate tier, 1.1 s, `exactness: exact`, `tol: 0`).
Card **CL267** (`contingent`). **Free inputs: zero for $n_t$ and $r$; the primordial spectrum itself
remains a free initial condition** — F282/F284/F285 are untouched, and what narrows is the *shape*
of the freedom, from a free function $P(k)$ to a choice of universality class. The finding's largest
residual is stated in its own §11 and is not a tolerance: **that the $t=0$ measure is critical is
inferred from the observed power law, not derived.**

### F311 — completeness gap #5: three numbers, none of them a physics defect (2026-08-11)

Two legs are measurements of the tree rather than of the lattice, and are labelled so. The one
new *number* is A2/A3's two-loop leptonic term; the one new *exact* statement is A1's bit-identity.

| Leg | Predicted form | Residual / value | Class | Source |
|---|---|---|---|---|
| Pi4 under the reinstated pre-F277 refold | the analytic one-loop sum cannot depend on a grid refold | **whole payload equal** | exact | F311 A1 |
| Pi3 under the same perturbation | the quadrature must move, or the control proves nothing | spread $\times6880$ | computed | F311 A1 |
| S12-F277 is a **partial** supersession | reaches Pi3, does not reach Pi4 | — | structural | F311 A1 |
| Two-loop leptonic $\Delta\alpha(M_Z)$, Källén–Sabry $(\alpha/\pi)^2[L/4+\zeta(3)-5/24]$ | $0.77568\times10^{-4}$ | vs published $0.77621\times10^{-4}$: **0.068 %** | quantitative | F311 A2 |
| The residual after one loop **is** that term | $0.77072\times10^{-4}$ measured | two-loop / residual $=\mathbf{100.6\%}$ | quantitative | F311 A2 |
| B9 with the two-loop term included | $3.149850\times10^{-2}$ vs PDG $3.1498\times10^{-2}$ | $0.245\%\to\mathbf{0.00158\%}$, $\mathbf{155\times}$, **0 fitted parameters** | quantitative | F311 A3 |
| A leading underscore must not defeat `_VOLATILE_RE` | 8 keys enumerated, all matched | — | exact | F311 B1 |
| Ten `candidate` baselines, re-run and diffed vs HEAD | 5 clean / 3 timing / 1 floor / 1 undeclared input | **0 regressions, 0 supersessions** | measured | F311 B2/B3 |
| F182/F184/F200 after the regex fix | reproduce HEAD exactly | — | measured | F311 B1 |
| FA-vs-FC is seed-independent | five seeds | identical to 10 digits | measured | F311 B2 |
| F193 postdates F192 and closes its candidate (i) | — | $12.75$ h | exact (dates) | F311 C1 |
| $w=p/\rho$ undefined at $\rho_\text{vac}=0$ ⇒ F192 V1 vacuous | — | — | structural | F311 C2 |
| F192's committed $\rho_\text{vac}$ vs $3^{-1}\rho_\text{Planck}=\Lambda_\text{UV}^4$ | the same mode sum F79 induces $1/G$ from | $1.65$ dex | computed | F311 C3 |
| Control: drop $\zeta(3)-5/24$ from the two-loop form | the identification must degrade | verified RED | control | F311 |
| Control: reinstate the pre-fix regex | B1 must redden on exactly 3 underscore keys | verified RED, $n=3$ | control | F311 |

Finding `F311-gap5-three-numbers-adjudicated.md`; record `F311-gap5-adjudication`
(entry `check_gap5`, **12/12**, gate tier, 1.0 s). **Free inputs: zero for A2/A3** (only $\alpha$,
$M_Z$ and the three lepton masses, all already in the module). Leg **C derives nothing** and the
finding says so — $\Omega_\Lambda\approx0.685$ is untouched and stays exactly where F241 left it;
what changes is that G1 stops being described as a contradiction. The two-loop formula is the
standard Källén–Sabry leading form, **cited not re-derived**; what is new is the identification of
the model's own residual with it.

### F312 — A6: Gleason's premises on SU(2)_L and SU(3)_c, closed by Schur (2026-08-11)

Closes F304 residual 3. Every leg below is a *premise* of F304 §5's theorem, not the theorem; the
one structural row (G6) is what makes the other groups follow rather than needing their own runs.
No RNG stream is consumed anywhere — every probe state and group element is deterministic (D8).

| Leg | Predicted form | Residual / value | Class | Source |
|---|---|---|---|---|
| $[T^a,T^b]=if^{abc}T^c$, $SU(2)_L$ | closes | **`0.0`** literal | exact | F312 G1 |
| $[T^a,T^b]=if^{abc}T^c$, $SU(3)_c$ | closes | $1.11\times10^{-16}$ | exact | F312 G2 |
| $f^{abc}=\varepsilon^{abc}$ ($SU(2)$) | Levi-Civita | **`0.0`** literal | exact | F312 G1 |
| $f_{123}=1$, $f_{458}=\sqrt3/2$ ($SU(3)$) | closed form | $1.0$; $0.8660254037844388$ | exact | F312 G2 |
| $f^{abc}$ totally antisymmetric | a property, not an input | **`0.0`** both | exact | F312 G1/G2 |
| **$[\hat J^a(x),\hat J^b(y)]=0$ for $x\ne y$ — the $\delta_{xy}$** | the non-Abelian structure is **intra-site** | **`0.0`** both, literal | exact | F312 G1/G2 |
| $[\hat J^a(x),\hat n(y)]=0$ — the record is a gauge singlet | the internal **trace** commutes with every generator | **`0.0`** both | exact | F312 G3 |
| Context weight spread, 5 contexts sharing a ray, $SU(2)_L$ present (dim 64) | context-blind | **`0.0`** literal | exact | F312 G4 |
| Context weight spread, $SU(3)_c$ present (dim 96) | context-blind | **`0.0`** literal | exact | F312 G5 |
| $C_2=\sum_aT^aT^a$ is a multiple of $\mathbb 1$ | Schur | dev **`0.0`** / $2.22\times10^{-16}$ | exact | F312 G6 |
| $C_2=(N^2-1)/2N$ | $3/4$ and $4/3$ | exact to $<10^{-15}$ | exact | F312 G6 |
| $\dim(\mathcal H_p\otimes V)=d_p N$; $SU(3)_c$ clears $d\ge3$ **alone** | $N=3\ge3$ | integer | exact | F312 G7 |
| The $d=2$ hole is unreachable in a charged sector | requires a total singlet with a 2-dim pointer | — | exact | F312 G7 |
| Linearity of the link step on $V$ | superposition survives | $\le2.8\times10^{-16}$ | machine | F312 G8 |
| Unitarity on $V$ | $U^\dagger U=\mathbb 1$ | $\le1.6\times10^{-15}$ | machine | F312 G8 |
| A gauge rotation leaves the record weight fixed | not a context | $\le1.3\times10^{-15}$ | machine | F312 G9 |
| Control: $f^{abc}\to0$ (pretend Abelian) | closure must fail | verified RED on G1 | control | F312 |
| Control: colour-**resolving** record | G3 must fail | verified RED on G3 | control | F312 |
| Control: basis-referencing gauge term | G4/G5 must fail | verified RED on G4 | control | F312 |

Finding `F312-born-rule-nonabelian-premises.md`; record `F312-born-nonabelian`
(entry `check_born_nonabelian`, **18/18**, gate tier, 0.1 s). **Free inputs: $N_c=3$** (ledger row
B10 — used by G7, not derived here). **Gleason's theorem is not re-proved**: it is F304 §5's, and
this supplies its premises on the two non-Abelian factors plus the Schur reduction that makes the
internal index irrelevant to it for *any* compact group. A6's other residual — the
Cooke–Keane–Moran regularity lemma — is **untouched and stays named**; the grade itself is a
completeness-run decision.


### F320 — B12: the absolute W and Z masses, and $\rho=1$ from rank (2026-08-16)

Row B12's residual was "absolute scale is an input". $v$ **is** an input and stays one; what was
wrong was the inference to "$m_W$, $m_Z$ are not predicted". Every leg below is either exact over
$\mathbb Q$, machine, or an explicitly bracketed number — and the bracket is the honest class for
the absolute masses, because $\Delta r$ is external. The headline (V4a) is $\Delta r$-**free** and
is therefore the leg to read first.

| Leg | Predicted form | Residual / value | Class | Source |
|---|---|---|---|---|
| $7{:}2$ count $\Rightarrow\sin^2\theta_W^\text{os}$ | $\tfrac29$, $=$ registry `sin2_thetaW_onshell` | `Fraction(2,9)` identity | exact (ℚ) | F320 B0a |
| $m_Z^2{:}m_W^2$ | $9{:}7$ | `Fraction(9,7)` identity | exact (ℚ) | F320 B0b |
| $c^2/s^2$ (the coefficient $\Delta\rho$ carries in $\Delta r$) | $\tfrac72$ | `Fraction(7,2)` identity | exact (ℚ) | F320 B0c |
| **$\det M^2$ at five independent rationals $u$** | vanishes **identically**, rank one | `0` integer, all five | exact (ℚ) | F320 B1a |
| Photon mass | exactly zero, not to a tolerance | `0` integer | exact | F320 B1b |
| **$\rho=m_W^2/(m_Z^2\cos^2\theta_W)$, every $u$** | $1$ — from rank, **no custodial $SU(2)$** | `Fraction(1,1)` | exact (ℚ) | F320 B1c |
| Massless eigenvector | $(\sqrt2,\sqrt7)/3$ | $4.44\times10^{-16}$ | machine | F320 B1d |
| **Stiffness quantum $u$ eliminated** | $g^2=18\pi\alpha$ | $18.0$, dev $<10^{-12}$ | exact | F320 B2a |
| | $g'^2=36\pi\alpha/7$ | $36/7$, dev $<10^{-12}$ | exact | F320 B2b |
| Closed forms vs the matrix solve | $m_W=\tfrac{3v}2\sqrt{2\pi\alpha}$, $m_Z=\tfrac{9v}2\sqrt{2\pi\alpha/7}$ | $1.42\times10^{-14}$ | machine | F320 B2c |
| Tree $m_W$ | $79.0836$ GeV | $-1.5996\%$ | quantitative | F320 B3b |
| Tree $m_Z$ | $89.6724$ GeV | $-1.6621\%$ | quantitative | F320 B3c |
| **$\Delta r$ cancels in the ratio**, $\Delta r\in[0,0.10]$, 41 points | $m_W^\text{mod}/m_W^\text{obs}=\sqrt{s^2_\text{obs}/(2/9)}$ | $2.22\times10^{-16}$ | machine | F320 B4a |
| $m_W$ excess, $\Delta r$-free | — | $+0.2219\%$ | quantitative | F320 B4b |
| $m_Z$ excess, $\Delta r$-free | — | $+0.1583\%$ | quantitative | F320 B4c |
| Model's $c^2/s^2=\tfrac72$ inside $\Delta r$ vs observed $3.4830$ | second order | $-0.0095\%$ on $m_W$ | quantitative | F320 B4d |
| $m_W$ over the $\Delta r$ bracket | $[80.1473,\ 80.5475]$ GeV | **contains** PDG $80.3692$ (55%) | bracketed | F320 B5a |
| $m_Z$ over the $\Delta r$ bracket | $[90.8785,\ 91.3323]$ GeV | **contains** PDG $91.1880$ | bracketed | F320 B5b |
| Bracket width $=$ the SM's own $\Delta r_\text{rem}$ | $\approx0.0096$ (literature) | $0.009651$ | quantitative | F320 B5c |
| Electroweak input count | $2$ (model) vs $3$ (SM); neither a boson mass | integer | exact (count) | F320 B6a/b |
| Control: `equal_stiffness=false` ($7\to11$) | counting block must fail, $\rho$ must **not** | verified RED on 14 legs | control | F320 |
| Control: `rank_two_breaking=true` | $\rho$ block must fail, counting must **not** | verified RED on B1a/b/c only | control | F320 |
| Control: `eliminate_u=false` | absolute block must fail, ratio and $\rho$ must **not** | verified RED on B2a-c, B3a | control | F320 |

Finding `F320-absolute-gauge-boson-masses-and-rho.md`; record `F320-gauge-boson-masses`
(entry `check_gauge_boson_masses`, **22/22**, gate tier, 0.0 s), **three** controls each verified
`CONTROL` over **disjoint** leg sets — which is what establishes that the ratio, $\rho$ and the
absolute scale rest on three different structural inputs rather than one. **Free inputs: $v$**
(ledger 17, `FIT (N=1)`, F119 — untouched), **$\alpha$** (F127's no-go — untouched), **$\Delta r$**
(external, bracketed), and **F141's equal-stiffness hypothesis (U)**, whose (U1)/(U2)/(U3) legs are
open and which now carries two absolute masses where it previously carried one ratio.

<!-- BEGIN GENERATED: exactness rows (casim index) -->

## Generated tables *(by `casim index` — do not edit by hand)*

Every residual-bearing entry in every committed result artifact, classified by the three-rule chain described in `casim/index/exactness.py`. The `Rule` column says which rule fired: `declared` (the entry's own label), `record` (its test-registry record's `expect.exactness`), or `signature` (the numerical criterion in *Reading the table*). Sort order within a tier is by residual.

### Tier 1 — exact (residual algebraically zero) — 166 rows

| Construct | Residual | Rule | Findings | Result artifact |
|-----------|----------|------|----------|-----------------|
| ) -> m_ω scheme-dep | `0.000e+00` | signature | F128 | `F128_omega_repulsion.json` |
| 10_riemann_silberstein_decomposition | `0.000e+00` | signature | FG6 | `FG6_two_helicity_photon.json` |
| 20-tick sourced-step on BCC, off-diagonal stays zero | `0.000e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| 224) | `0.000e+00` | signature | F128 | `F128_omega_repulsion.json` |
| 2D cold links → G^a = 0 | `0.000e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| 2_two_helicity_linearity | `0.000e+00` | signature | FG6 | `FG6_two_helicity_photon.json` |
| 8 MeV | `0.000e+00` | signature |  | `P4_deuteron.json` |
| 9) UNBINDS the deuteron | `0.000e+00` | signature | F240 | `F240_omega_coupling_derivation.json` |
| A1 V_omega > 0 everywhere (REPULSIVE) | `0.000e+00` | declared | F128 | `F128_omega_repulsion.json` |
| A1_masslessness | `0.000e+00` | declared | F249 | `F249_qed_comparison_battery.json` |
| A2 V_sigma < 0 everywhere (ATTRACTIVE) | `0.000e+00` | declared | F128 | `F128_omega_repulsion.json` |
| A2 baryon-number coherence g_omegaNN = 3 g_rhoNN (exact x3) | `0.000e+00` | declared | F240 | `F240_omega_coupling_derivation.json` |
| A3 at equal mass: V_omega == -V_sigma (lone sign flip) | `0.000e+00` | declared | F128 | `F128_omega_repulsion.json` |
| A4 sign rule eta: scalar=-1, vector=+1 (Coulomb-like) | `0.000e+00` | declared | F128 | `F128_omega_repulsion.json` |
| AF2 | `0.000e+00` | declared | F218 | `F218_alpha2F_and_pade_gap.json` |
| B  G_c Lam^2 = pi^2/(Nc Nf) | `0.000e+00` | declared | F77 | `F77_njl_gap_rpa.json` |
| B  full bound AND central-only unbound | `0.000e+00` | declared |  | `P4_deuteron.json` |
| B1 baryon number 3*(1/3) = 1 | `0.000e+00` | declared | F128 | `F128_omega_repulsion.json` |
| B2 g_ωNN/g_ωq = 3 ;  (g_ωNN)²/(g_ωq)² = 9 | `0.000e+00` | declared | F128 | `F128_omega_repulsion.json` |
| B5_per_component_rotation_law_consistency | `0.000e+00` | signature | F29 | `F29_su2_photon_bridge.json` |
| BCC cold links → G^a_{μν} = 0 | `0.000e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| BCC even-law dielectric step == free step bit-for-bit at eps_c=1 | `0.000e+00` | signature | FG7 | `FG7f_gluon_dielectric_gap.json` |
| BP6 confrontation numbers self-consistent | `0.000e+00` | signature | F73 | `F73_spin0_bound_pair.json` |
| Bogomolny completion -> sigma=2 pi v^2 n (BPS, exact) | `0.000e+00` | signature | FG7 | `FG7d_colour_dielectric.json` |
| C0 route-A and route-B root search actually bracketed a real root (not | `0.000e+00` | signature | F373 | `F373_quark_size_from_confinement_radius.json` |
| C1 deuteron is bound (E_b>0) | `0.000e+00` | declared |  | `P4_deuteron.json` |
| C1_coupling_lock_4pi_implies_16pi | `0.000e+00` | signature | F56 | `F56_einstein_coupling_derivation.json` |
| C2 route A required g_omega^2/4pi stays in the OBE/SU(6) window [3,12] | `0.000e+00` | signature | F373 | `F373_quark_size_from_confinement_radius.json` |
| CC1 SU(2) raising/lowering algebra | `0.000e+00` | signature | FG8 | `FG8_beta_decay.json` |
| CC10 end-to-end d→u+W-→u+e-+ν̄ pipeline | `0.000e+00` | signature | FG8 | `FG8_beta_decay.json` |
| CC2 d->u raising; ΔQ=+1=-Q(W-) | `0.000e+00` | signature | FG8 | `FG8_beta_decay.json` |
| CC3 vertex charge conservation | `0.000e+00` | signature | FG8 | `FG8_beta_decay.json` |
| CC4 V-A vertex kills right-handed | `0.000e+00` | signature | FG8 | `FG8_beta_decay.json` |
| CC5 quark-lepton universality of J+ | `0.000e+00` | signature | FG8 | `FG8_beta_decay.json` |
| CC9 full process d->u e- ν̄ conservation | `0.000e+00` | signature | FG8 | `FG8_beta_decay.json` |
| Cold configuration is a flow/cooling fixed point | `0.000e+00` | signature | FG7 | `FG7b_gradient_flow.json` |
| Cold-link Wilson loop = N_c = 3 (9 sizes) | `0.000e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| D  single bound state (E1 >= 0) | `0.000e+00` | declared |  | `P4_deuteron.json` |
| D-charge-d | `0.000e+00` | signature |  | `P0_dynamical_fermions.json` |
| D-charge-e | `0.000e+00` | signature |  | `P0_dynamical_fermions.json` |
| D-charge-u | `0.000e+00` | signature |  | `P0_dynamical_fermions.json` |
| D1 route A finds a real (bracket-valid) root at b_P2, the one value th | `0.000e+00` | signature | F373 | `F373_quark_size_from_confinement_radius.json` |
| D3 fitted g_ωNN²/4π in OBE/SU(6) window [5,25] | `0.000e+00` | signature | F128 | `F128_omega_repulsion.json` |
| D4 deuteron P_D in physical band [3%,9%] | `0.000e+00` | signature | F128 | `F128_omega_repulsion.json` |
| Diagonal source coupling (all 8 octet components) | `0.000e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| E1 sigma+omega residual well in [-100,-50] MeV at g_omega2/4pi=8 | `0.000e+00` | signature | F240 | `F240_omega_coupling_derivation.json` |
| E3 node count = n-l-1 | `0.000e+00` | declared |  | `P5_hydrogen.json` |
| Energetic binding V(R)=σR → ∞ (no free quark) | `0.000e+00` | signature | FG10 | `FG10_baryon_singlet.json` |
| G1_colour_coupling_branch_blind | `0.000e+00` | signature | F91 | `F91_pairing_classification.json` |
| G2_colour_phase_split_zero | `0.000e+00` | signature | F91 | `F91_pairing_classification.json` |
| G2_lieb_robinson_speed | `0.000e+00` | signature | F227 | `F227_decoherence_floor.json` |
| HOP2 | `0.000e+00` | declared | F213 | `F213_hopfield_and_gap_renormalization.json` |
| HOP3 | `0.000e+00` | declared | F213 | `F213_hopfield_and_gap_renormalization.json` |
| I4 still ONE bound state (E1≥0) | `0.000e+00` | declared |  | `P4_deuteron.json` |
| I5 tensor still essential (central-only unbound) | `0.000e+00` | declared |  | `P4_deuteron.json` |
| J2 finer grid is more accurate | `0.000e+00` | declared |  | `P5_hydrogen.json` |
| M2_u1y_invariance_y_nuR_zero | `0.000e+00` | signature |  | `majorana_fork.json` |
| M3_u1y_selection_rule | `0.000e+00` | signature |  | `majorana_fork.json` |
| M6_seesaw_scaling | `0.000e+00` | signature |  | `majorana_fork.json` |
| Massive step at m_g=0 reduces to free step | `0.000e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| Octet charge density wraps Noether current | `0.000e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| Proton spin-flavour wavefunction S₃-symmetric | `0.000e+00` | signature | FG10 | `FG10_baryon_singlet.json` |
| Proton uud quantum numbers (exact rational) | `0.000e+00` | signature | FG10 | `FG10_baryon_singlet.json` |
| QE3_chi_decoupled_at_m0 | `0.000e+00` | signature | FG3 | `FG3_quark_electroweak.json` |
| S4_parity_spin_scalar_[P,sigma]=0 | `0.000e+00` | signature |  | `sublattice_hypercharge.json` |
| S7 finite positive m_p/sqrt-sigma on string scale | `0.000e+00` | signature | F122 | `P2_baryon_bound_state.json` |
| SC1a | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC3a | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC3b | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC4a | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC4c | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC5a | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC5b | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC6 | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| T4_split_eq_pair_birefringence | `0.000e+00` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| Total wavefunction antisymmetric (Fermi statistics) | `0.000e+00` | signature | FG10 | `FG10_baryon_singlet.json` |
| W3_chiral_step_Fpm_at_Omega_pm | `0.000e+00` | signature | F91 | `F91_pairing_classification.json` |
| W3_reality_maps_branch_to_chiral | `0.000e+00` | signature | F91 | `F91_pairing_classification.json` |
| Y10_quark_alpha_zero_reduces_to_F40 | `0.000e+00` | signature |  | `hypercharge_extension.json` |
| Y14_chi_kinetic_alpha_zero_bitwise | `0.000e+00` | signature |  | `hypercharge_extension.json` |
| Y3_reduction_to_F27_bitwise | `0.000e+00` | signature |  | `hypercharge_fork.json` |
| Y5_su2_lepton_field_undisturbed | `0.000e+00` | signature |  | `hypercharge_fork.json` |
| Y7_GMN_charge_algebra | `0.000e+00` | signature |  | `hypercharge_fork.json` |
| annihilation_contact | `0.000e+00` | signature | F262 | `F262_positronium_hyperfine.json` |
| both options confine (V rises, sigma>0) | `0.000e+00` | signature |  | `FA_vs_FC_comparison.json` |
| condensate VEV from measured MC density (F88->F86 hand-off) | `0.000e+00` | signature | FG7 | `FG7f_gluon_dielectric_gap.json` |
| d_R | `0.000e+00` | signature |  | `wmu_phase6.json` |
| dielectric gluon step: free-reduction + c renorm | `0.000e+00` | signature | FG7 | `FG7d_colour_dielectric.json` |
| e_L | `0.000e+00` | signature |  | `wmu_phase6.json` |
| e_R | `0.000e+00` | signature |  | `wmu_phase6.json` |
| points[0] | `0.000e+00` | signature | F260 | `F260_qed_scattering.json` |
| points[2] | `0.000e+00` | signature | F260 | `F260_qed_scattering.json` |
| points[2] | `0.000e+00` | signature | F260 | `F260_qed_scattering.json` |
| points[3] | `0.000e+00` | signature | F260 | `F260_qed_scattering.json` |
| points[3] | `0.000e+00` | signature | F260 | `F260_qed_scattering.json` |
| points[4] | `0.000e+00` | signature | F260 | `F260_qed_scattering.json` |
| results[0] | `0.000e+00` | signature | FG4 | `FG4_dynamical_Z.json` |
| results[0] | `0.000e+00` | signature |  | `wmu_phase3.json` |
| results[0] | `0.000e+00` | signature |  | `wmu_phase5_stueckelberg.json` |
| results[10] | `0.000e+00` | signature |  | `E2E_nonabelian_bilinear.json` |
| results[11] | `0.000e+00` | signature | FG4 | `FG4_dynamical_Z.json` |
| results[13] | `0.000e+00` | signature |  | `E2E_nonabelian_bilinear.json` |
| results[1] | `0.000e+00` | signature |  | `wmu_phase1.json` |
| results[2] | `0.000e+00` | signature |  | `E2E_nonabelian_bilinear.json` |
| results[2] | `0.000e+00` | signature | FG4 | `FG4_dynamical_Z.json` |
| results[2] | `0.000e+00` | signature |  | `wmu_phase2.json` |
| results[2] | `0.000e+00` | signature |  | `wmu_phase4.json` |
| results[2] | `0.000e+00` | signature |  | `wmu_phase5_stueckelberg.json` |
| results[2] | `0.000e+00` | signature |  | `wmu_phase6.json` |
| results[3] | `0.000e+00` | signature |  | `wmu_phase2.json` |
| results[4] | `0.000e+00` | signature | F37 | `F37_delta_omega.json` |
| results[4] | `0.000e+00` | signature |  | `wmu_phase3.json` |
| results[4] | `0.000e+00` | signature |  | `wmu_phase5_stueckelberg.json` |
| results[7] | `0.000e+00` | signature | FG4 | `FG4_dynamical_Z.json` |
| results[8] | `0.000e+00` | signature | FG4 | `FG4_dynamical_Z.json` |
| results[9] | `0.000e+00` | signature |  | `E2E_nonabelian_bilinear.json` |
| rows[0] | `0.000e+00` | signature | FC05 | `FC05_qm_battery.json` |
| rows[10] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| rows[1] | `0.000e+00` | signature | FC05 | `FC05_qm_battery.json` |
| rows[1] | `0.000e+00` | signature | FC05 | `FC05_qm_battery.json` |
| rows[3] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| rows[3] | `0.000e+00` | signature |  | `test_12_QM3_heisenberg.json` |
| rows[4] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| rows[5] | `0.000e+00` | signature | FC05 | `FC05_qm_battery.json` |
| rows[5] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| rows[5] | `0.000e+00` | signature |  | `test_12_QM3_heisenberg.json` |
| rows[6] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| rows[7] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| rows[8] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| rows[9] | `0.000e+00` | signature | FG9 | `FG9_C_CP_per_species.json` |
| runs[0] | `0.000e+00` | signature | FA09 | `FA09_deflection.json` |
| runs[1] | `0.000e+00` | signature | FA09 | `FA09_deflection.json` |
| runs[2] | `0.000e+00` | signature | FA09 | `FA09_deflection.json` |
| runs[3] | `0.000e+00` | signature | FA09 | `FA09_deflection.json` |
| sample_rows[0] | `0.000e+00` | signature | F46 | `F46_pythagorean_mass.json` |
| sigma_A>0 and F70 2D sigma>0 & decreasing (cross-anchor) | `0.000e+00` | signature |  | `FA_vs_FC_comparison.json` |
| tests[0] | `0.000e+00` | signature | F45 | `F45_sigma_tau_weinberg.json` |
| tests[1] | `0.000e+00` | signature | F45 | `F45_sigma_tau_weinberg.json` |
| tests[2] | `0.000e+00` | signature | F45 | `F45_sigma_tau_weinberg.json` |
| tests[4] | `0.000e+00` | signature | F45 | `F45_sigma_tau_weinberg.json` |
| two_field | `0.000e+00` | signature |  | `wmu_phase6_rank1.json` |
| two_field | `0.000e+00` | signature |  | `wmu_phase6_rank1.json` |
| u_L | `0.000e+00` | signature |  | `wmu_phase6.json` |
| u_R | `0.000e+00` | signature |  | `wmu_phase6.json` |
| ε_{abc} totally antisymmetric | `0.000e+00` | signature | FG10 | `FG10_baryon_singlet.json` |
| ν_L | `0.000e+00` | signature |  | `wmu_phase6.json` |
| SC1c | `1.110e-16` | declared | F210 | `F210_superconductivity.json` |
| A1 KSFR closes: m_rho = sqrt2 g_rhopipi f_pi | `1.453e-16` | declared | F240 | `F240_omega_coupling_derivation.json` |
| B  split identity exact | `1.777e-16` | declared |  | `P3_pion.json` |
| C3 split: Pi_S-Pi_PS = -8NcNf M^2 K | `1.777e-16` | declared | F77 | `F77_njl_gap_rpa.json` |
| S2_volumes | `3.331e-16` | record | F267 | `F267_walk_bz_measure.json` |
| SC1b | `2.665e-15` | declared | F210 | `F210_superconductivity.json` |
| A3 => strict-universality g_omegaNN^2/4pi = 9 g_rhoNN^2/4pi | `7.105e-15` | declared | F240 | `F240_omega_coupling_derivation.json` |
| A1 1-2G Pi_PS(0)=0 IS the gap eq (m_pi=0) | `2.265e-14` | declared |  | `P3_pion.json` |
| MR1 | `5.787e-10` | declared | F213 | `F213_hopfield_and_gap_renormalization.json` |
| A2 pseudoscalar pole at m_pi=0 (chiral) | `1.553e-07` | declared |  | `P3_pion.json` |
| offshell | `5.260e-04` | record | F22 | `F22_rho_identity_and_offshell.json` |
| rows[0] | `1.568e-03` | record | F362 | `F362_blockspin_fluctuation.json` |
| rows[2] | `2.089e-03` | record | F362 | `F362_blockspin_fluctuation.json` |
| rows[4] | `2.350e-03` | record | F362 | `F362_blockspin_fluctuation.json` |
| rows[1] | `3.148e-03` | record | F362 | `F362_blockspin_fluctuation.json` |
| rows[3] | `4.191e-03` | record | F362 | `F362_blockspin_fluctuation.json` |
| rows[5] | `4.712e-03` | record | F362 | `F362_blockspin_fluctuation.json` |
| DES_Y6_3x2pt | `1.200e-02` | record | F288 | `F288_structure_formation.json` |
| combined_CMB | `1.250e-02` | record | F288 | `F288_structure_formation.json` |
| KiDS_Legacy | `1.850e-02` | record | F288 | `F288_structure_formation.json` |

### Tier 2 — machine precision (below the 1e-12 float/FFT floor) — 196 rows

| Construct | Residual | Rule | Findings | Result artifact |
|-----------|----------|------|----------|-----------------|
| A1 Ry(Ps)/Ry(H_inf) = 1/2 (reduced mass) | `0.000e+00` | declared |  | `P5_hydrogen.json` |
| C1 chiral f_pi/M exact (Pagels-Stokar) | `0.000e+00` | declared | F124 | `F124_qcd_scale_ratio.json` |
| C1 vector bubble: direct trace == [I1+(q2-M2)K] reduction | `0.000e+00` | declared | F128 | `F128_omega_repulsion.json` |
| C3 factorisation identity | `0.000e+00` | declared | F124 | `F124_qcd_scale_ratio.json` |
| I  2s_1/2 == 2p_1/2 (same \|kappa\|) | `0.000e+00` | declared |  | `P5_hydrogen.json` |
| SC2d | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| SC5c | `0.000e+00` | declared | F210 | `F210_superconductivity.json` |
| TC4 | `0.000e+00` | declared | F211 | `F211_tc_real_materials.json` |
| BP1 sin(asin m1+asin m2)=m1 n2+m2 n1 | `1.336e-51` | signature | F73 | `F73_spin0_bound_pair.json` |
| BP4 saturation at mc=1/sqrt2 -> m_H=1 | `2.673e-51` | signature | F73 | `F73_spin0_bound_pair.json` |
| BP2 equal-mass closed form | `4.009e-51` | signature | F73 | `F73_spin0_bound_pair.json` |
| T2_baseline_real_CP_conserving | `3.702e-27` | signature | F353 | `F353_delta_cp_t2g_inheritance.json` |
| rows[2] | `4.337e-19` | signature | FC05 | `FC05_qm_battery.json` |
| Schur: ⟨U⟩ = w·I for the single plaquette | `1.291e-18` | signature | FG7 | `FG7c_confinement.json` |
| results[4] | `6.993e-18` | signature |  | `wmu_phase1.json` |
| results[5] | `9.120e-18` | signature |  | `wmu_phase1.json` |
| results[1] | `1.028e-17` | signature |  | `wmu_phase4.json` |
| results[3] | `1.128e-17` | signature |  | `wmu_phase1.json` |
| W2_even_excluded_by_F67_separation | `1.388e-17` | signature | F91 | `F91_pairing_classification.json` |
| two_field | `1.388e-17` | signature |  | `wmu_phase6_rank1.json` |
| w(β) limits and monotonicity | `1.530e-17` | signature | FG7 | `FG7c_confinement.json` |
| results[0] | `1.794e-17` | signature |  | `wmu_phase4.json` |
| results[1] | `2.776e-17` | signature |  | `E2E_nonabelian_bilinear.json` |
| results[9] | `2.776e-17` | signature | FG4 | `FG4_dynamical_Z.json` |
| two_field | `2.776e-17` | signature |  | `wmu_phase6_rank1.json` |
| two_field | `2.776e-17` | signature |  | `wmu_phase6_rank1.json` |
| w(β) quadrature converges (n_grid 160→320) | `2.776e-17` | signature | FG7 | `FG7c_confinement.json` |
| sample_rows[5] | `2.909e-17` | signature | F46 | `F46_pythagorean_mass.json` |
| 1_per_branch_nonzero_and_transverse | `3.365e-17` | signature | FG6 | `FG6_two_helicity_photon.json` |
| G3 | `3.855e-17` | signature |  | `SR5_photon_frame_invariance.json` |
| CC8 heavy-W Fermi limit G_F/√2=g²/8m_W² | `4.163e-17` | signature | FG8 | `FG8_beta_decay.json` |
| rows[3] | `4.163e-17` | signature | FC05 | `FC05_qm_battery.json` |
| Y15_quark_GMN_algebra | `5.551e-17` | signature |  | `hypercharge_extension.json` |
| d_L | `5.551e-17` | signature |  | `wmu_phase6.json` |
| results[3] | `5.551e-17` | signature |  | `wmu_phase6.json` |
| rows[7] | `-5.551e-17` | signature |  | `test_12_QM3_heisenberg.json` |
| sample_rows[4] | `5.914e-17` | signature | F46 | `F46_pythagorean_mass.json` |
| sample_rows[3] | `5.943e-17` | signature | F46 | `F46_pythagorean_mass.json` |
| QE2_ward_constant_V | `6.206e-17` | signature | FG3 | `FG3_quark_electroweak.json` |
| Q9_doublet_su2_ward | `8.356e-17` | signature | FG2 | `FG2_quark_complex_mass.json` |
| Jacobi identity for f^abc | `1.110e-16` | signature | FG7 | `FG7_gluon_dynamics.json` |
| QM-2 tunneling vs Schrödinger/WKB | `1.110e-16` | signature | FC05 | `FC05_qm_battery.json` |
| T2_two_qubit | `1.110e-16` | signature | F208 | `F208_entanglement_generation.json` |
| T2_two_qubit | `1.110e-16` | signature | F212 | `F212_entanglement_generation.json` |
| results[10] | `1.110e-16` | signature | FG4 | `FG4_dynamical_Z.json` |
| results[11] | `1.110e-16` | signature |  | `E2E_nonabelian_bilinear.json` |
| rows[2] | `-1.110e-16` | signature |  | `test_12_QM3_heisenberg.json` |
| rows[3] | `1.110e-16` | signature | FC05 | `FC05_qm_battery.json` |
| rows[4] | `1.110e-16` | signature | FC05 | `FC05_qm_battery.json` |
| rows[4] | `-1.110e-16` | signature |  | `test_12_QM3_heisenberg.json` |
| rows[6] | `1.110e-16` | signature |  | `test_12_QM3_heisenberg.json` |
| rows[8] | `1.110e-16` | signature |  | `test_12_QM3_heisenberg.json` |
| sample_rows[2] | `1.110e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| sample_rows[3] | `1.110e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| sample_rows[4] | `1.110e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| sample_rows[5] | `1.110e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| Q2_u1_ward | `1.186e-16` | signature | FG2 | `FG2_quark_complex_mass.json` |
| Q6_color_neutrality | `1.186e-16` | signature | FG2 | `FG2_quark_complex_mass.json` |
| sigma_A fixes dual-SC condensate v*=sqrt(sigma_A/2pi) | `1.205e-16` | signature |  | `FA_vs_FC_comparison.json` |
| Zero colour charge: G^a\|S⟩=0, C₂\|S⟩=0 | `1.360e-16` | signature | FG10 | `FG10_baryon_singlet.json` |
| sample_rows[1] | `1.665e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| spin_spin | `1.665e-16` | signature | F262 | `F262_positronium_hyperfine.json` |
| A6_ward_charge_conservation | `1.686e-16` | declared | F249 | `F249_qed_comparison_battery.json` |
| points[0] | `1.823e-16` | signature | F260 | `F260_qed_scattering.json` |
| points[1] | `1.892e-16` | signature | F260 | `F260_qed_scattering.json` |
| points[1] | `1.892e-16` | signature | F260 | `F260_qed_scattering.json` |
| A1-disp-d | `2.220e-16` | signature |  | `P0_dynamical_fermions.json` |
| Creutz ratio χ(R,T)=σ ∀(R,T) (exact area law) | `2.220e-16` | signature | FG7 | `FG7c_confinement.json` |
| results[5] | `2.220e-16` | signature |  | `E2E_nonabelian_bilinear.json` |
| results[7] | `2.220e-16` | signature |  | `E2E_nonabelian_bilinear.json` |
| tests[3] | `2.220e-16` | signature | F45 | `F45_sigma_tau_weinberg.json` |
| B1_singlet_H_SU2_invariance | `2.238e-16` | signature | F29 | `F29_su2_photon_bridge.json` |
| points[3] | `2.531e-16` | signature | F260 | `F260_qed_scattering.json` |
| Wilson loop local SU(3) gauge invariance | `2.559e-16` | signature | FG7 | `FG7_gluon_dynamics.json` |
| A1-disp-e | `2.776e-16` | signature |  | `P0_dynamical_fermions.json` |
| sample_rows[1] | `2.791e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| sample_rows[0] | `2.873e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| B2_triplet_adjoint_rotation | `3.078e-16` | signature | F29 | `F29_su2_photon_bridge.json` |
| A1-disp-u | `3.331e-16` | signature |  | `P0_dynamical_fermions.json` |
| BCC rotation magnitude conservation (10 ticks) | `3.357e-16` | signature | FG7 | `FG7_gluon_dynamics.json` |
| over-relaxation preserves Wilson action | `3.691e-16` | signature |  | `FA_lgt_mc.json` |
| Σ_a ‖G^a‖² SU(3) Casimir invariance | `3.938e-16` | signature | FG7 | `FG7_gluon_dynamics.json` |
| 8_triplet_magnitude_SU2_invariance_combined | `4.441e-16` | signature | FG6 | `FG6_two_helicity_photon.json` |
| QM-1 CHSH / Tsirelson | `4.441e-16` | signature | FC05 | `FC05_qm_battery.json` |
| SC2a | `4.441e-16` | declared | F210 | `F210_superconductivity.json` |
| part1 | `4.441e-16` | signature |  | `top10_T02_QM1_CHSH.json` |
| results[0] | `4.441e-16` | signature |  | `E2E_nonabelian_bilinear.json` |
| results[6] | `4.441e-16` | signature | FG4 | `FG4_dynamical_Z.json` |
| two_field | `4.441e-16` | signature |  | `wmu_phase6_rank1.json` |
| G1 | `4.710e-16` | signature |  | `SR5_photon_frame_invariance.json` |
| results[2] | `5.446e-16` | signature |  | `wmu_phase3.json` |
| Flow force Z ∈ su(3) (anti-Hermitian, traceless) | `5.551e-16` | signature | FG7 | `FG7b_gradient_flow.json` |
| sample_rows[2] | `5.738e-16` | signature | F46 | `F46_pythagorean_mass.json` |
| B3_triplet_magnitude_SU2_invariance | `6.661e-16` | signature | F29 | `F29_su2_photon_bridge.json` |
| G4 | `6.661e-16` | signature |  | `SR5_photon_frame_invariance.json` |
| results[0] | `6.661e-16` | signature |  | `wmu_phase1.json` |
| G5 | `8.882e-16` | signature |  | `SR5_photon_frame_invariance.json` |
| Static potential V(R)=σR linear, T-independent | `8.882e-16` | signature | FG7 | `FG7c_confinement.json` |
| results[0] | `8.882e-16` | signature |  | `wmu_phase6.json` |
| results[4] | `8.882e-16` | signature |  | `E2E_nonabelian_bilinear.json` |
| results[6] | `8.882e-16` | signature |  | `E2E_nonabelian_bilinear.json` |
| rows[6] | `8.882e-16` | signature | FC05 | `FC05_qm_battery.json` |
| G^a transforms as SU(3) adjoint (BCC bilinear) | `8.882e-16` | signature | FG7 | `FG7_gluon_dynamics.json` |
| G^a transforms as SU(3) adjoint (2D bilinear) | `8.891e-16` | signature | FG7 | `FG7_gluon_dynamics.json` |
| Y8_quark_u1y_ward_d_branch | `8.892e-16` | signature |  | `hypercharge_extension.json` |
| Y9_quark_u1y_ward_u_branch | `8.951e-16` | signature |  | `hypercharge_extension.json` |
| heat-bath+OR preserve SU(3) | `8.973e-16` | signature |  | `FA_lgt_mc.json` |
| Y1_u1y_ward_e_branch | `9.037e-16` | signature |  | `hypercharge_fork.json` |
| CC6 W- emission = (g/√2) J+ dt | `9.155e-16` | signature | FG8 | `FG8_beta_decay.json` |
| Y2_u1y_ward_nu_branch | `9.155e-16` | signature |  | `hypercharge_fork.json` |
| Y4_su2_L_ward_with_alpha | `9.155e-16` | signature |  | `hypercharge_fork.json` |
| Y11_quark_su2_L_ward_with_alpha | `9.486e-16` | signature |  | `hypercharge_extension.json` |
| S1_anticommute_{P,W}=0 | `1.053e-15` | signature |  | `sublattice_hypercharge.json` |
| E3-quark-norm-conserved | `1.110e-15` | signature |  | `P0_dynamical_fermions.json` |
| Colour-singlet gauge invariance B→det(V)B=B | `1.222e-15` | signature | FG10 | `FG10_baryon_singlet.json` |
| C  dense diag == secular root (L=12) | `1.332e-15` | declared | F74 | `F74_bound_state_binding.json` |
| G  dense diag == secular root (L=12) | `1.332e-15` | declared |  | `P3_pion.json` |
| results[1] | `1.332e-15` | signature |  | `wmu_phase6.json` |
| points[2] | `1.380e-15` | signature | F260 | `F260_qed_scattering.json` |
| results[1] | `1.554e-15` | signature |  | `wmu_phase5_stueckelberg.json` |
| results[3] | `1.554e-15` | signature |  | `wmu_phase3.json` |
| G6 | `1.570e-15` | signature |  | `SR5_photon_frame_invariance.json` |
| Y13_chi_kinetic_gauge_covariance | `1.617e-15` | signature |  | `hypercharge_extension.json` |
| G1_tsirelson_exact | `1.776e-15` | signature | F226 | `F226_bell_tsirelson.json` |
| results[4] | `1.776e-15` | signature |  | `wmu_phase6.json` |
| staple/action-gradient identity (ratio=4) | `1.776e-15` | signature |  | `FA_lgt_mc.json` |
| S2_two_tick_[W2,P]=0 | `1.804e-15` | signature |  | `sublattice_hypercharge.json` |
| E2-su3-density-casimir-invariant | `1.889e-15` | signature |  | `P0_dynamical_fermions.json` |
| G2 | `2.041e-15` | signature |  | `SR5_photon_frame_invariance.json` |
| G2b | `2.224e-15` | signature |  | `SR5_photon_frame_invariance.json` |
| 2D rotation magnitude conservation (20 ticks) | `2.225e-15` | signature | FG7 | `FG7_gluon_dynamics.json` |
| results[8] | `2.665e-15` | signature |  | `E2E_nonabelian_bilinear.json` |
| rows[9] | `2.887e-15` | signature | FC05 | `FC05_qm_battery.json` |
| det V = 1 for SU(3) (source of invariance) | `3.167e-15` | signature | FG10 | `FG10_baryon_singlet.json` |
| results[1] | `3.553e-15` | signature | FG4 | `FG4_dynamical_Z.json` |
| Q1_unitarity | `3.553e-15` | signature | FG2 | `FG2_quark_complex_mass.json` |
| T5_sigma0_invariant | `3.972e-15` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| Y12_quark_mass_unitarity_50_steps | `4.433e-15` | signature |  | `hypercharge_extension.json` |
| Y6_unitarity_50_steps | `4.725e-15` | signature |  | `hypercharge_fork.json` |
| ‖G^a_{xy}‖² constant-V SU(3) invariance | `5.127e-15` | signature | FG7 | `FG7_gluon_dynamics.json` |
| A1_dispersion_invariance_under_SU2 | `5.588e-15` | signature | F29 | `F29_su2_photon_bridge.json` |
| B-norm-d | `5.773e-15` | signature |  | `P0_dynamical_fermions.json` |
| results[12] | `6.439e-15` | signature |  | `E2E_nonabelian_bilinear.json` |
| 2D self-coupling preserves link unitarity (5 ticks) | `6.439e-15` | signature | FG7 | `FG7_gluon_dynamics.json` |
| results[5] | `7.105e-15` | signature | FG4 | `FG4_dynamical_Z.json` |
| rows[4] | `7.105e-15` | signature | FC05 | `FC05_qm_battery.json` |
| rows[8] | `7.883e-15` | signature | FC05 | `FC05_qm_battery.json` |
| Flow is gauge-covariant: flow(U^g) = flow(U)^g | `8.130e-15` | signature | FG7 | `FG7b_gradient_flow.json` |
| BCC self-coupling preserves link unitarity (5 ticks) | `9.326e-15` | signature | FG7 | `FG7_gluon_dynamics.json` |
| rows[7] | `9.437e-15` | signature | FC05 | `FC05_qm_battery.json` |
| A  <S12> = [[0,2√2],[2√2,-2]] (CG) | `9.770e-15` | declared |  | `P4_deuteron.json` |
| Q8_color_charge_conservation | `1.056e-14` | signature | FG2 | `FG2_quark_complex_mass.json` |
| results[1] | `1.151e-14` | signature | F37 | `F37_delta_omega.json` |
| rows[9] | `1.821e-14` | signature |  | `test_12_QM3_heisenberg.json` |
| T4_same_branch_minus_rate | `1.865e-14` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| T4_same_branch_plus_rate | `1.962e-14` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| results[2] | `2.021e-14` | signature |  | `wmu_phase1.json` |
| points[1] | `2.029e-14` | signature | F260 | `F260_qed_scattering.json` |
| SU(3) unitarity + det=1 preserved (flow & cooling) | `2.065e-14` | signature | FG7 | `FG7b_gradient_flow.json` |
| W2_single_branch_rides_Omega_s | `2.124e-14` | signature | F91 | `F91_pairing_classification.json` |
| B-norm-e | `2.132e-14` | signature |  | `P0_dynamical_fermions.json` |
| E1-colour-charge-conserved | `2.132e-14` | signature |  | `P0_dynamical_fermions.json` |
| C1 Goldstone: m_pi = 0 (1-2G Pi_PS(0)=0) | `2.265e-14` | declared | F77 | `F77_njl_gap_rpa.json` |
| C2 NJL theorem: m_sigma = 2 m_c | `2.265e-14` | declared | F77 | `F77_njl_gap_rpa.json` |
| constant cross-section -> linear V(R)=sigma R | `2.986e-14` | signature | FG7 | `FG7d_colour_dielectric.json` |
| B-norm-u | `3.086e-14` | signature |  | `P0_dynamical_fermions.json` |
| results[1] | `3.424e-14` | signature |  | `wmu_phase2.json` |
| results[0] | `3.739e-14` | signature | F37 | `F37_delta_omega.json` |
| uniform dielectric exactly unitary + c_eff=c sqrt(eps_c) | `4.228e-14` | signature | FG7 | `FG7f_gluon_dielectric_gap.json` |
| results[3] | `5.136e-14` | signature | F37 | `F37_delta_omega.json` |
| Q5_theta_pure_gauge | `5.684e-14` | signature | FG2 | `FG2_quark_complex_mass.json` |
| T5_sigma_vector_adjoint_2omega | `6.138e-14` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| Free-gluon BCC dispersion residual (50 ticks, even law) | `7.313e-14` | signature | FG7 | `FG7_gluon_dynamics.json` |
| results[4] | `7.583e-14` | signature |  | `wmu_phase4.json` |
| results[3] | `9.801e-14` | signature | FG4 | `FG4_dynamical_Z.json` |
| QM-3 Heisenberg Δx·Δp ≥ ħ/2 | `1.137e-13` | signature | FC05 | `FC05_qm_battery.json` |
| rows[2] | `-1.137e-13` | signature | FC05 | `FC05_qm_battery.json` |
| T3_branch_swap_symmetric | `1.155e-13` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| gap-massive gluon dispersion omega^2 = m_V^2 + Omega_even^2 | `1.363e-13` | signature | FG7 | `FG7f_gluon_dielectric_gap.json` |
| S0 ECG == analytic 3 sqrt(3k/m) | `1.367e-13` | declared | F122 | `P2_baryon_bound_state.json` |
| results[4] | `1.737e-13` | signature | FG4 | `FG4_dynamical_Z.json` |
| results[3] | `2.799e-13` | signature |  | `E2E_nonabelian_bilinear.json` |
| CC7 Proca W- dispersion ω²=m_W²+Ω² | `2.948e-13` | signature | FG8 | `FG8_beta_decay.json` |
| results[0] | `3.405e-13` | signature |  | `wmu_phase2.json` |
| T1a_singlet_rate_eq_pair_dispersion | `6.161e-13` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| T1b_all_channels_ride_pair_rate | `6.161e-13` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| T2_rate_eq_f26_rotation_step | `6.161e-13` | signature | F89 | `F89_singlet_bilinear_paired_photon.json` |
| points[0] | `6.927e-13` | signature | F260 | `F260_qed_scattering.json` |
| A2 K(0) closed form == quadrature | `1.091e-12` | declared | F77 | `F77_njl_gap_rpa.json` |
| S1 scipy eigh == Cholesky reduction | `5.295e-12` | declared | F122 | `P2_baryon_bound_state.json` |
| A1 I1 closed form == quadrature | `5.900e-12` | declared | F77 | `F77_njl_gap_rpa.json` |
| SC2b | `1.483e-11` | declared | F210 | `F210_superconductivity.json` |
| B0 P2 ground state is S3-symmetric (three pair <r^2> equal) | `4.112e-11` | declared | F373 | `F373_quark_size_from_confinement_radius.json` |
| value | `2.144e-10` | record |  | `bcc_gauge_mc_d4.json` |
| S4 three pair radii equal (symmetric) | `3.532e-10` | declared | F122 | `P2_baryon_bound_state.json` |
| Sommerfeld == O((Za)^4) series | `4.527e-10` | declared | FB05 | `FB05_hydrogen_fine_structure.json` |

### Tier 3 — quantitative (a number with a declared tolerance) — 213 rows

| Construct | Residual | Rule | Findings | Result artifact |
|-----------|----------|------|----------|-----------------|
| B1 E_b increases monotonically with g | `0.000e+00` | declared | F74 | `F74_bound_state_binding.json` |
| B2 E_b -> 0 at threshold g=g_c | `0.000e+00` | declared | F74 | `F74_bound_state_binding.json` |
| B2 R_conf (F146) is the CLOSER of the two candidates to the tuned b | `0.000e+00` | declared | F373 | `F373_quark_size_from_confinement_radius.json` |
| C5 m_sigma ~= 2 m_c (chiral partner) | `0.000e+00` | declared |  | `P3_pion.json` |
| D  ceiling M=2m_c recovered at threshold | `0.000e+00` | declared | F74 | `F74_bound_state_binding.json` |
| E1 m_sigma/(2 m_c) >= 1 for ALL G (E_b <= 0) | `0.000e+00` | declared | F77 | `F77_njl_gap_rpa.json` |
| E2 P_D -> 0 without tensor | `0.000e+00` | declared |  | `P4_deuteron.json` |
| S2 monotone variational decrease | `0.000e+00` | declared | F122 | `P2_baryon_bound_state.json` |
| S8a m_n - m_p sign POSITIVE | `0.000e+00` | declared | F122 | `P2_baryon_bound_state.json` |
| TC5 | `0.000e+00` | declared | F211 | `F211_tc_real_materials.json` |
| BP5 deficit << 1 at EW scale | `1.470e-33` | declared | F73 | `F73_spin0_bound_pair.json` |
| CAL_one_loop_calibration | `1.803e-13` | record | F336 | `F336_twoloop_vp_nonlog.json` |
| F336-1 | `1.803e-13` | record | F336 | `F336_twoloop_vp_nonlog.json` |
| BP3 deficit leading order d~mc^2/2 | `2.500e-13` | declared | F73 | `F73_spin0_bound_pair.json` |
| F336-3 | `4.108e-13` | record | F336 | `F336_twoloop_vp_nonlog.json` |
| bogoliubov_validation | `1.020e-12` | signature | F228 | `F228_geon_production_stability.json` |
| D1 Ry(H) matches reduced-mass CODATA | `1.138e-12` | declared |  | `P5_hydrogen.json` |
| M5_seesaw_closed_form | `1.819e-12` | signature |  | `majorana_fork.json` |
| rows[0] | `1.819e-12` | signature | FC05 | `FC05_qm_battery.json` |
| rows[1] | `1.819e-12` | signature |  | `test_12_QM3_heisenberg.json` |
| 224 MeV (single bound state) | `7.059e-12` | signature | F128 | `F128_omega_repulsion.json` |
| rows[0] | `1.455e-11` | signature |  | `test_12_QM3_heisenberg.json` |
| M1_majorana_unitary | `2.251e-11` | signature |  | `majorana_fork.json` |
| 224 | `2.543e-11` | declared |  | `P4_deuteron.json` |
| 224 MeV | `3.617e-11` | declared |  | `P4_deuteron.json` |
| S6 dominance+symmetry survive 1/2-rule | `9.476e-11` | declared | F122 | `P2_baryon_bound_state.json` |
| ore_powell | `1.317e-10` | signature | F262 | `F262_positronium_hyperfine.json` |
| F1 Sommerfeld == O((Za)^4) series | `4.601e-10` | declared |  | `P5_hydrogen.json` |
| Flow acts as lattice Laplacian (decay rate ∝ k̂²) | `4.942e-10` | signature | FG7 | `FG7b_gradient_flow.json` |
| total_cross_section[0] | `1.967e-09` | signature | F260 | `F260_qed_scattering.json` |
| part3 | `2.198e-09` | signature |  | `top10_T02_QM1_CHSH.json` |
| A5_thomson_cross_section | `2.865e-09` | declared | F249 | `F249_qed_comparison_battery.json` |
| total_cross_section[0] | `3.289e-09` | signature | F260 | `F260_qed_scattering.json` |
| V1_seesaw_roundtrip | `6.274e-09` | signature | F364 | `F364_baryogenesis_boltzmann_test.json` |
| total_cross_section[1] | `1.461e-08` | signature | F260 | `F260_qed_scattering.json` |
| total_cross_section[2] | `1.562e-08` | signature | F260 | `F260_qed_scattering.json` |
| kn_total[0] | `1.563e-08` | signature | F260 | `F260_qed_scattering.json` |
| kn_total[1] | `1.661e-08` | signature | F260 | `F260_qed_scattering.json` |
| A2_luminality | `2.389e-08` | declared | F249 | `F249_qed_comparison_battery.json` |
| G0 Newton G (canonical cell, e-11) | `2.961e-08` | declared | F123 | `P6_si_scale.json` |
| total_cross_section[1] | `3.817e-08` | signature | F260 | `F260_qed_scattering.json` |
| M4_bdg_infinitesimal_match | `4.108e-08` | signature |  | `majorana_fork.json` |
| kn_total[2] | `5.511e-08` | signature | F260 | `F260_qed_scattering.json` |
| 1s_1/2 = -13.605874 eV | `7.634e-08` | declared | FB05 | `FB05_hydrogen_fine_structure.json` |
| EL5 | `1.482e-07` | declared | F215 | `F215_eliashberg_solver.json` |
| A  g_c matches Watson integral | `1.676e-07` | declared | F74 | `F74_bound_state_binding.json` |
| kn_total[3] | `4.503e-07` | signature | F260 | `F260_qed_scattering.json` |
| bcc_self_check_vs_1_over_sqrt6 | `4.613e-07` | signature |  | `curl_fork_results_2026-05-22.json` |
| G  numerical Dirac == Sommerfeld (rel binding) | `1.270e-06` | declared |  | `P5_hydrogen.json` |
| numerical Dirac == Sommerfeld (rel binding) | `1.270e-06` | declared | FB05 | `FB05_hydrogen_fine_structure.json` |
| total_cross_section[2] | `1.570e-06` | signature | F260 | `F260_qed_scattering.json` |
| AF3 | `1.600e-06` | declared | F218 | `F218_alpha2F_and_pade_gap.json` |
| SC4b | `1.852e-06` | declared | F210 | `F210_superconductivity.json` |
| relative-to-binding slope = 2 | `2.392e-06` | declared | FB05 | `FB05_hydrogen_fine_structure.json` |
| AF1 | `2.500e-06` | declared | F218 | `F218_alpha2F_and_pade_gap.json` |
| numeric sigma matches BPS 2 pi v^2 n | `4.618e-06` | signature | FG7 | `FG7d_colour_dielectric.json` |
| E  gauge binding << required (ceiling robust) | `6.656e-06` | declared | F74 | `F74_bound_state_binding.json` |
| C  l-degeneracy (spread within n) | `1.302e-05` | signature |  | `P5_hydrogen.json` |
| 6057 eV | `1.331e-05` | declared |  | `P5_hydrogen.json` |
| J1 ground state converges toward -1 Ry | `1.406e-05` | signature |  | `P5_hydrogen.json` |
| C2 Lambda/f_pi (chiral factor) | `1.501e-05` | declared | F124 | `F124_qcd_scale_ratio.json` |
| E2 1s ~ x e^{-x} (slope -1) | `1.666e-05` | declared |  | `P5_hydrogen.json` |
| 2316/fm | `2.336e-05` | declared |  | `P4_deuteron.json` |
| 2316 /fm | `2.336e-05` | declared |  | `P4_deuteron.json` |
| 3) | `2.499e-05` | signature |  | `P5_hydrogen.json` |
| 5 a0 | `2.499e-05` | declared |  | `P5_hydrogen.json` |
| C1_1d_machinery | `3.026e-05` | signature | F207 | `F207_casimir.json` |
| H3 splitting/binding ∝ alpha^2 (relative) | `4.007e-05` | declared |  | `P5_hydrogen.json` |
| C-zitter-d | `5.033e-05` | signature |  | `P0_dynamical_fermions.json` |
| S2 converged (last step < 1e-2) | `5.519e-05` | declared | F122 | `P2_baryon_bound_state.json` |
| absolute alpha-scaling slope = 4 | `5.676e-05` | declared | FB05 | `FB05_hydrogen_fine_structure.json` |
| V1 | `7.367e-05` | record | F334 | `F334_hadronic_vmd_estimate.json` |
| H2 splitting ∝ alpha^4 (absolute) | `8.323e-05` | declared |  | `P5_hydrogen.json` |
| A2-groupvel-weyl | `1.110e-04` | signature |  | `P0_dynamical_fermions.json` |
| 803 eV | `1.234e-04` | declared |  | `P5_hydrogen.json` |
| ANO profile BCs + quantised colour-electric flux | `1.467e-04` | signature | FG7 | `FG7d_colour_dielectric.json` |
| 5 | `1.561e-04` | signature |  | `P5_hydrogen.json` |
| 6 eV | `1.571e-04` | declared |  | `P5_hydrogen.json` |
| SC2c | `1.589e-04` | declared | F210 | `F210_superconductivity.json` |
| results[2] | `3.947e-04` | signature | F37 | `F37_delta_omega.json` |
| B9-5 | `4.949e-04` | record | F322 | `F322_b9_running_rederivation.json` |
| 0529 nm | `5.450e-04` | declared |  | `P5_hydrogen.json` |
| E3 slope <lnK*r> = 2GM/c^2 | `6.269e-04` | signature | F106 | `F106_psi_K_sourcing.json` |
| S9 proton calibrated quark fraction < 2% of M | `6.752e-04` | declared | F122 | `P2_baryon_bound_state.json` |
| C-zitter-u | `8.974e-04` | signature |  | `P0_dynamical_fermions.json` |
| S9 neutron calibrated quark fraction < 2% of M | `9.375e-04` | declared | F122 | `P2_baryon_bound_state.json` |
| S5 quark sum < 2% of M (string-dominated) | `1.059e-03` | declared | F122 | `P2_baryon_bound_state.json` |
| C-zitter-e | `1.216e-03` | signature |  | `P0_dynamical_fermions.json` |
| 95 GHz | `1.764e-03` | declared |  | `P5_hydrogen.json` |
| C3 f_pi ~= 92 MeV | `1.985e-03` | declared |  | `P3_pion.json` |
| D2 f_pi ~= 92 MeV | `1.985e-03` | declared | F77 | `F77_njl_gap_rpa.json` |
| rows[0] | `-2.102e-03` | signature | F251 | `F251_vacuum_polarization.json` |
| rows[1] | `-2.106e-03` | signature | F251 | `F251_vacuum_polarization.json` |
| rows[2] | `-2.113e-03` | signature | F251 | `F251_vacuum_polarization.json` |
| rows[3] | `-2.119e-03` | signature | F251 | `F251_vacuum_polarization.json` |
| C2 shallow E_b/M_N < 1e-2 | `2.127e-03` | declared |  | `P4_deuteron.json` |
| 97 fm AT b=R_conf | `2.225e-03` | signature | F373 | `F373_quark_size_from_confinement_radius.json` |
| 224 | `3.329e-03` | signature | F240 | `F240_omega_coupling_derivation.json` |
| F  tail slope matches κ | `3.362e-03` | declared |  | `P4_deuteron.json` |
| weyl_fermion | `3.724e-03` | signature |  | `propagation_demo_2026-05-22.json` |
| weyl_fermion | `3.724e-03` | signature |  | `propagation_demo_2026-08-04.json` |
| weyl_fermion | `3.724e-03` | signature |  | `propagation_demo_2026-09-29.json` |
| C4 <qq>^1/3 ~= -250 MeV | `3.795e-03` | declared |  | `P3_pion.json` |
| D4 <qbar q>^1/3 ~= -250 MeV | `3.795e-03` | declared | F77 | `F77_njl_gap_rpa.json` |
| 97 fm | `3.920e-03` | signature | F240 | `F240_omega_coupling_derivation.json` |
| D  GMOR holds | `3.934e-03` | declared |  | `P3_pion.json` |
| D5 GMOR m_pi^2 f_pi^2 = -m0<qq> | `3.934e-03` | declared | F77 | `F77_njl_gap_rpa.json` |
| QM-4 Zeno suppression | `3.985e-03` | signature | FC05 | `FC05_qm_battery.json` |
| MC mean plaquette ↔ quadrature w(β) | `4.791e-03` | signature | FG7 | `FG7c_confinement.json` |
| Wilson action monotonically non-increasing | `-4.922e-03` | signature | FG7 | `FG7b_gradient_flow.json` |
| C6 bare-rotor route (scale-setting gap) | `5.469e-03` | signature | F124 | `F124_qcd_scale_ratio.json` |
| G1 model f_pi vs physical | `5.577e-03` | signature | F123 | `P6_si_scale.json` |
| 55 (tuned) and b=R_conf (insensitivity) | `6.204e-03` | signature | F373 | `F373_quark_size_from_confinement_radius.json` |
| 224 | `6.285e-03` | signature | F240 | `F240_omega_coupling_derivation.json` |
| H  E_b grid-converged | `6.446e-03` | declared |  | `P4_deuteron.json` |
| A6 | `6.498e-03` | signature | F264 | `F264_qed_allorders_anomaly.json` |
| A9_pi0_width | `6.498e-03` | declared | F264 | `F264_qed_allorders_anomaly.json` |
| H5 rho m_rho (KSRF) | `7.713e-03` | signature | F123 | `P6_si_scale.json` |
| PA1 | `8.116e-03` | declared | F218 | `F218_alpha2F_and_pade_gap.json` |
| E  m_pi^2/m0 constant (linear Goldstone) | `8.584e-03` | declared |  | `P3_pion.json` |
| C3 ρ-ω degeneracy: \|m_ω-m_ρ\|/m_ρ <= 2% (flavour-blind bubble + OZI) | `9.545e-03` | signature | F128 | `F128_omega_repulsion.json` |
| H2 nucleon m_p ~ 3 m_c | `1.045e-02` | declared | F123 | `P6_si_scale.json` |
| dirac_fermion | `1.056e-02` | signature |  | `propagation_demo_2026-09-29.json` |
| dirac_fermion | `1.056e-02` | signature |  | `propagation_demo_2026-05-22.json` |
| dirac_fermion | `1.056e-02` | signature |  | `propagation_demo_2026-08-04.json` |
| D6 Goldberger-Treiman g_piqq f_pi = M | `1.083e-02` | declared | F77 | `F77_njl_gap_rpa.json` |
| H1 constituent m_c (vs m_N/3) | `1.113e-02` | declared | F123 | `P6_si_scale.json` |
| MR3 | `1.127e-02` | declared | F213 | `F213_hopfield_and_gap_renormalization.json` |
| PA2 | `1.211e-02` | declared | F218 | `F218_alpha2F_and_pade_gap.json` |
| H8 deuteron OPEP range (1/m_pi) | `1.217e-02` | signature | F123 | `P6_si_scale.json` |
| H4 pion m_pi | `1.232e-02` | signature | F123 | `P6_si_scale.json` |
| gap_ratio_table[6] | `1.250e-02` | signature | F213 | `F213_hopfield_and_gap_renormalization.json` |
| G7 | `1.278e-02` | signature |  | `SR5_photon_frame_invariance.json` |
| HOP1 | `1.286e-02` | declared | F213 | `F213_hopfield_and_gap_renormalization.json` |
| dual Meissner penetration depth lambda=1/(e v) | `1.322e-02` | signature | FG7 | `FG7d_colour_dielectric.json` |
| dynamic flux expulsion from condensed vacuum (dual Meissner) | `1.369e-02` | signature | FG7 | `FG7f_gluon_dielectric_gap.json` |
|  | `1.499e-02` | signature |  | `top10_T09_GR4_mercury.json` |
| gap_ratio_table[2] | `1.556e-02` | signature | F213 | `F213_hopfield_and_gap_renormalization.json` |
| mean plaquette matches known SU(3) ⟨P⟩ | `1.593e-02` | signature |  | `FA_lgt_mc.json` |
| shared large-R slope + Coulomb gap = -e/R (C omits it) | `1.690e-02` | signature |  | `FA_vs_FC_comparison.json` |
| E1 P_D in (2%,12%) nonzero | `1.806e-02` | declared |  | `P4_deuteron.json` |
| gap_ratio_table[3] | `1.884e-02` | signature | F213 | `F213_hopfield_and_gap_renormalization.json` |
| QM-6 two-slit fringe + which-path decoherence | `1.961e-02` | signature | FC05 | `FC05_qm_battery.json` |
| tests[5] | `2.009e-02` | signature | F45 | `F45_sigma_tau_weinberg.json` |
| B1_ln_k0_1s | `-2.135e-02` | declared | F257 | `F257_bethe_log_from_spectrum.json` |
| dual-Meissner screening lambda = 1/m_V from the measured gap | `2.171e-02` | signature | FG7 | `FG7f_gluon_dielectric_gap.json` |
| B2_ln_k0_2s | `-2.272e-02` | declared | F257 | `F257_bethe_log_from_spectrum.json` |
| EL4 | `2.478e-02` | declared | F215 | `F215_eliashberg_solver.json` |
| TC3 | `2.748e-02` | declared | F211 | `F211_tc_real_materials.json` |
| B4_triplet_transversality_smallk | `2.891e-02` | signature | F29 | `F29_su2_photon_bridge.json` |
| 9_triplet_per_branch_transversality | `2.894e-02` | signature | FG6 | `FG6_two_helicity_photon.json` |
| MR2 | `2.899e-02` | declared | F213 | `F213_hopfield_and_gap_renormalization.json` |
| gap_ratio_table[5] | `3.105e-02` | signature | F213 | `F213_hopfield_and_gap_renormalization.json` |
| gap_ratio_table[4] | `3.313e-02` | signature | F213 | `F213_hopfield_and_gap_renormalization.json` |
| gap_ratio_table[0] | `3.860e-02` | signature | F213 | `F213_hopfield_and_gap_renormalization.json` |
| C2 m_pi ~= 135 MeV | `4.089e-02` | declared |  | `P3_pion.json` |
| D3 m_pi ~= 135 MeV | `4.089e-02` | declared | F77 | `F77_njl_gap_rpa.json` |
| composite_photon | `4.213e-02` | signature |  | `propagation_demo_2026-09-29.json` |
| composite_photon | `4.213e-02` | signature |  | `propagation_demo_2026-05-22.json` |
| composite_photon | `4.213e-02` | signature |  | `propagation_demo_2026-08-04.json` |
| C1 m_c ~= 325 MeV | `4.242e-02` | declared |  | `P3_pion.json` |
| D1 M ~= 325 MeV | `4.242e-02` | declared | F77 | `F77_njl_gap_rpa.json` |
| TC2 | `4.295e-02` | declared | F211 | `F211_tc_real_materials.json` |
| 45, agree <10%) | `4.460e-02` | signature | F240 | `F240_omega_coupling_derivation.json` |
| 97 fm | `4.555e-02` | signature | F240 | `F240_omega_coupling_derivation.json` |
| 97 fm AT b=R_conf | `4.835e-02` | signature | F373 | `F373_quark_size_from_confinement_radius.json` |
| PA3 | `5.192e-02` | declared | F218 | `F218_alpha2F_and_pade_gap.json` |
| gap_ratio_table[1] | `5.323e-02` | signature | F213 | `F213_hopfield_and_gap_renormalization.json` |
| 55 fm | `5.464e-02` | declared | F373 | `F373_quark_size_from_confinement_radius.json` |
| G8 | `5.473e-02` | signature |  | `SR5_photon_frame_invariance.json` |
| EL1 | `5.955e-02` | declared | F215 | `F215_eliashberg_solver.json` |
| AF4 | `5.977e-02` | declared | F218 | `F218_alpha2F_and_pade_gap.json` |
| multilevel agrees with & sharpens direct correlator | `6.490e-02` | signature |  | `FA_lgt_mc.json` |
| strong-coupling ⟨plaq⟩ → β/18 | `8.001e-02` | signature |  | `FA_lgt_mc.json` |
| results[1] | `8.689e-02` | signature |  | `wmu_phase3.json` |
| H7 <qbar q>^1/3 (sign/order) | `8.945e-02` | signature | F123 | `P6_si_scale.json` |
| EL2 | `8.994e-02` | declared | F215 | `F215_eliashberg_solver.json` |
| C5 sqrt(sigma)/Lambda (confinement) | `1.175e-01` | declared | F124 | `F124_qcd_scale_ratio.json` |
| Random-link Wilson loops bounded ≪ N_c | `1.192e-01` | signature | FG7 | `FG7_gluon_dynamics.json` |
| 56 | `1.224e-01` | declared | F124 | `F124_qcd_scale_ratio.json` |
| H6 sigma m_sigma in f0(500) band | `1.254e-01` | signature | F123 | `P6_si_scale.json` |
| TC1 | `1.426e-01` | declared | F211 | `F211_tc_real_materials.json` |
| QE5_ward_varying_V | `1.477e-01` | signature | FG3 | `FG3_quark_electroweak.json` |
| H3 m_n - m_p | `1.678e-01` | declared | F123 | `P6_si_scale.json` |
| splitting within 0.18% of measured 10.969 GHz | `1.764e-01` | declared | FB05 | `FB05_hydrogen_fine_structure.json` |
| F2 m_pi << m_rho (vector) | `1.789e-01` | declared |  | `P3_pion.json` |
| 68 fm | `1.858e-01` | signature | F373 | `F373_quark_size_from_confinement_radius.json` |
| results[3] | `2.053e-01` | signature |  | `wmu_phase5_stueckelberg.json` |
| S8b \|m_n-m_p\| within 1 MeV of measured | `2.170e-01` | signature | F122 | `P2_baryon_bound_state.json` |
| String tension σ(β)>0 for all finite β | `2.192e-01` | signature | FG7 | `FG7c_confinement.json` |
| F1 m_pi << m_sigma (chiral partner) | `2.258e-01` | declared |  | `P3_pion.json` |
| EL3 | `2.409e-01` | declared | F215 | `F215_eliashberg_solver.json` |
| Q10_split_mass_breaks_su2 | `2.435e-01` | signature | FG2 | `FG2_quark_complex_mass.json` |
| B1 P2-ECG single-quark spread vs tuned b (companion candidate, INFORMA | `3.377e-01` | declared | F373 | `F373_quark_size_from_confinement_radius.json` |
| QE1_cold_w_regression | `3.610e-01` | signature | FG3 | `FG3_quark_electroweak.json` |
| results[3] | `4.943e-01` | signature |  | `wmu_phase4.json` |
| HOP4 | `5.353e-01` | declared | F213 | `F213_hopfield_and_gap_renormalization.json` |
| Q7_cold_link_regression | `5.478e-01` | signature | FG2 | `FG2_quark_complex_mass.json` |
| Q11_kinetic_breaks_local_su2 | `6.045e-01` | signature | FG2 | `FG2_quark_complex_mass.json` |
| 363 below NJL floor of 1 | `6.371e-01` | declared | F77 | `F77_njl_gap_rpa.json` |
| wilson_gate | `9.174e-01` | signature |  | `d1_vertex_formfactor.json` |
| QE4_norm_conservation | `9.921e-01` | signature | FG3 | `FG3_quark_electroweak.json` |
| QE6_color_charge_conservation | `1.045e+00` | signature | FG3 | `FG3_quark_electroweak.json` |
| 2D random links → G^a non-zero | `1.647e+00` | signature | FG7 | `FG7_gluon_dynamics.json` |
| cbt | `2.163e+00` | record | F347 | `F347_quark_mixed_koide_probe.json` |
| up_type | `2.169e+00` | record | F346 | `F346_quark_shape_probe.json` |
| C5 | `2.171e+00` | record | F347 | `F347_quark_mixed_koide_probe.json` |
| uds | `2.171e+00` | record | F347 | `F347_quark_mixed_koide_probe.json` |
| down_type | `2.205e+00` | record | F346 | `F346_quark_shape_probe.json` |
| C5 | `2.317e+00` | record | F346 | `F346_quark_shape_probe.json` |
| C6 | `2.317e+00` | record | F347 | `F347_quark_mixed_koide_probe.json` |
| Gradient flow smooths disorder → σ_eff decreases | `-2.617e+00` | signature | FG7 | `FG7c_confinement.json` |
| S3 finite gap to 1st excited (discrete) | `-2.889e+00` | declared | F122 | `P2_baryon_bound_state.json` |

*575 generated rows from 602 artifacts. Rules: 153 declared, 24 by record, 398 by signature.*

<!-- END GENERATED -->
