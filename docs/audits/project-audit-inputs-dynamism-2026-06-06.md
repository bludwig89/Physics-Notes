# Project Audit — Underived Inputs & Field Dynamism

2026-06-06 - 17:30

> **Addendum 2026-06-06 - 18:45.** Two items below are now closed: (i) the F64 loop's posited pieces (source $=|\Psi|^2$ proxy, free $G$) are derived by **F106** ($\nabla^2\ln K=-(8\pi G/c^4)T^{00}[\psi]$, coefficient $=1$ in lattice units, $G_\text{lattice}=1/(72\pi)$ structural — `findings/F106-psi-K-sourcing-derivation.md`); (ii) **B.2 item 1 is done** — the F64 dielectric is mainlined as the gravity field element (`ca-simulation/ca_gravity.py` + dynamic `gravity_dielectric` channel + `ParticleChannel` gravity tier background→coupled; D-EM8 dynamical Φ, F106 sourcing, F62 lapse mix; `tests/test_gravity_element.py` 6/6, scenario `gravity_dynamic_selfsourced`). The remaining gravity gap narrows to: kinetic-leg $c_\text{eff}$ variation for *massless* packets in the production engine (fork-only; the spectral kernels are homogeneous).

> **Addendum 2026-06-06 - 23:55.** **B.2 item 2 is built** — real-time Kogut–Susskind link Hamiltonian evolution exists (**F110**, `ca-simulation/ca_link_hamiltonian.py`, 7/7 PASS): Gauss-law-exact dual height representation (ℤ₃ exact / U(1) truncation-converged), λ=0 potential exact, linear $V(R)$ at finite coupling, F101 rotor χ-map matrix identity, and the flux tube watched persisting/melting in real time. Remaining in that item: dynamical-matter coupling (P2), 3D tree-gauge, SU(3) Casimir ladder. See the inline note at B.2 §2.

**Scope.** Full audit against three questions: (1) do any "input" values remain that are not derived within the system; (2) is every field fully dynamical with correctly functioning particle interactions; (3) for each remaining underived input, what avenue sources it. Sources: findings F01–F104, `docs/status/exactness-inventory.md` (updated 2026-06-06 - 16:56), `docs/status/project-status.md`, `docs/roadmaps/next-steps.md`, `deprecated/si-units-options.md`, roadmaps, module code in `ca-simulation/`, and test results.

---

## Verdict (one paragraph)

The structural sector is essentially input-free: generation count, Koide $Q=2/3$, the 45° phase, the $E_g$ vacuum channel, $\kappa=0$ flatness, $B$ (cubic Landau coefficient), $\sin^2\theta_W=1/4$, the Newton-constant *form* and $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$, the photon/W/Z/gluon propagator classification, and confinement's area law are all derived (Tier 1/2). **Ten genuinely underived inputs remain**, falling into three clusters: the SI ruler ($a$ and absolute masses), the lepton-spectrum brake ($C$/$W$ plus the F92 bridge), and the QCD-calibration block (NJL fit, $g_A$, $M_N$, $r_c$, $g_{\rho\pi\pi}$, and the bare gauge couplings $e, g, g_s$). On dynamism: all first-generation fields (γ, W±, Z, gluon, leptons, quarks, hypercharge) are fully dynamical with verified two-way back-reaction; **gravity is dynamical only in the F64 fork** (main engine uses a static/Poisson background), **real-time confinement evolution** is not built (2D frozen-link exact only), and **composites are mixed** — the pion is certified as a real-space dynamical object (F103-G), but the proton (F71) is operator-level and the deuteron (F104) is a continuum radial Hamiltonian, not lattice real-time.

---

## Part A — Input ledger

### A.1 Derived (formerly inputs, now closed)

| Quantity | Value | Derivation | Finding |
|---|---|---|---|
| $c_\text{lat}$ | $1/\sqrt{3}$ (BCC) | rotation rate $d\Omega/dabs(k)$ | F25/F26 |
| Generation count | 3 | $T_{1u}$ unique odd 3D irrep of $O_h$; no 4D irrep | F75 |
| Koide $Q$ | $2/3$ | three independent routes; F92 consistency fixed point unique at $t=45°$ | F78/F81/F92 |
| 45° per-constituent phase | exact | joint solvability of $m=\sin 2t$ and $m=y^2$ with Fock $\sqrt2$ | F92 |
| Orthorhombic vacuum identity | $E_g$, 2nd BCC shell | $\mathrm{sym}(T_{1u}\otimes T_{1u})$ decomposition | F93 |
| $\kappa=0$ flatness | exact | $D_{2h}$ stabilizer theorem | F84/F93 |
| $B$ (cubic Landau coeff.) | $-3\sqrt2\,I_2\,\bar y^4$, $I_2=0.2202$ | QCA Dirac-sea loop; sign predicts $\delta\in[0°,30°)$ ✓ | F95 |
| $y_\tau=1$ (heavy flavor) | exact | cliff theorem — saturation edge forces the wall | F101 |
| $\sin^2\theta_W$ | $1/4$ (bare) | σ↔τ swap geometry, two independent routes | F45 |
| $m_Z/m_W$ | $2/\sqrt3$ (bare); $=1/\cos\theta_W$ exact | F35/F45 | |
| $G$ (form) | $1/G = 2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3) = 8\pi\sqrt3\,\hbar/(a^2c^3)$ | loop channel forced (traceless EM stress = zero tree stiffness); $\eta=1/12$, $g_*=48$ structural | F79/F61/F75 |
| $a/\ell_P$ | $\sqrt{8\pi}\,3^{1/4}=6.5978$ | parameter-free; returns CODATA $G$ to $3\times10^{-8}$ | F79 |
| $K(x)$ canonical form | $e^{2GM/rc^2}$, $AB\equiv1$ | impedance match + PPN $\beta=\gamma=1$ | F64 D-EM5/9 |
| Photon channel | even law, non-birefringent | forced by U(1) minimal coupling | F68/F69 |
| Propagator classification | γ even, W± chiral, Z mixed, gluon even | branch structure of each coupling | F91 |
| $\sigma$ (string tension, 2D) | $-\ln w(\beta)>0$ all finite β | exact area law; centre-Lagrange identity | F70/F99 |
| Confinement form | compact rotor $\hat E^2-\lambda\cos\hat\phi$ | from rule's transfer operator | F100/F101(strong) |
| Baryon binder | $Z_3$ centre closure; binder = colour dielectric | cap-coincidence no-go for $N=3$ | F97/F98 |
| Anomaly cancellation | all six traces exactly 0 | exact rationals | F38 |
| Mass mechanism | chiral SU(2)$_L$ complex mass, Higgs-free | Ward identities at machine precision | F27/F41/F44 |

### A.2 Still underived — the open ledger

| # | Input | Current value/status | Where it enters |
|---|---|---|---|
| 1 | Lattice spacing $a$ (the SI ruler) | $a/\ell_P=6.5978$ derived, but one dimensionful anchor still needed; F83 ceiling $a\le3.11\times10^{-18}$ m (top quark) | every SI prediction |
| 2 | Sextic brake $C$ (equivalently $W\approx1.46$) | localized (F95), fitted ($C=0.636\lvert B\rvert$), two routes converge on $W^*=1.46$, but **underived** — static RPA gives wrong sign | charged-lepton spectrum, $\cos3\delta=0.7859$ |
| 3 | Global-stability invariant (democratic quartic $\bar y$ cost) | lepton point metastable on minimal 3-coupling family; one invariant flagged, deliberately not added | F101 A2 |
| 4 | F92 bridge construction | per-tick chirality allocation → collective flavor vector constrained to one point, not built from the update rule | generation-space origin |
| 5 | Gauge coupling magnitudes $e$, $g$, $g_s$ | free (ratio $g'/g$ derived via F45; magnitudes not); no RG running, so the +12% gap $\sin^2\theta_W = 1/4$ vs PDG 0.2232 is unexplained | all interaction strengths |
| 6 | NJL calibration $\Lambda=651.5$ MeV, $G\Lambda^2=2.10$, $m_0=5.5$ MeV | fitted to measured $m_c/f_\pi/m_\pi/\langle\bar qq\rangle$ (0.2–4.2%) | F77 → F103 pion → F104 deuteron |
| 7 | $g_A=1.272$ | external, via Goldberger-Treiman | F104 πNN coupling |
| 8 | $M_N=938.9$ MeV | external — P2 (dynamical baryon mass) not built | F104 binding kinematics |
| 9 | Hard-core radius $r_c=0.448$ fm | the one tuned knob in F104; the "missing ingredient" the roadmap predicted | deuteron short-range repulsion |
| 10 | $g_{\rho\pi\pi}\simeq6$ | external, Tier-3, used only for the ρ contrast | F103-F |
| — | Lepton masses $m_e,m_\mu,m_\tau$ (PDG) | data, used as *targets/constraints*, not model inputs in the dynamical rules — but the spectrum is currently fitted, not predicted, pending #2/#3 | F92/F93/F101 |

---

## Part B — Field dynamism & interaction verification

### B.1 Fully dynamical, two-way back-reaction verified

| Sector | Propagation | Sourced by matter | Matter reads field | Test status |
|---|---|---|---|---|
| Photon (paired-spinor, F69) | F26 even rotation, exact | Ampère $\nabla\times B=J$, Gauss conserved | Peierls/AB holonomy exact | F87 20/20; **forward-Euler instability fixed 2026-06-06** with exact per-mode propagator (#179–180) |
| W± | Proca $\omega^2=m_W^2+\Omega_\text{even}^2$, chiral law | isospin current kick (F36) | covariant doublet step (F31/F34) | F36, F54 β-decay 10/10 end-to-end causal |
| Z | even + mass-suppressed axial | $J^Z=J^3-\sin^2\theta_W J^{em}$ | per-species $g_{L,R}$ exact GMN registry | F48 12/12; Z11 prediction $g_V^{e_L}=0$ at bare angle |
| Gluons (SU(3)) | **even** law (F91 migration 2026-06-04) | quark colour current | parallel transport on links | F43 20/20; E2E 14/14 (F90 closed loop, work–energy ledger $4\times10^{-17}$) |
| Leptons/quarks | exact BCC Weyl/Dirac unitary | — | all four couplings; charge/colour conserved | P0 16/16; F27, F38, F40, FG-2/3 |
| Hypercharge U(1)$_Y$ | pure-gauge, eaten by Z (Stueckelberg) | n/a (by design) | Ward $9\times10^{-16}$ | F41 7/7, F42 |
| casim particle layer | EM + SU(3) back-action **two-way** | exact Bloch acceleration $1.0\times10^{-15}$ | U(1) gauge covariance $6.5\times10^{-17}$ | F102 8/8 (P2 casim) |

No one-way couplings were found in the first-generation sector. The F90 closed fermion↔field loop conserves the work–energy ledger to $6.9\times10^{-18}$ inside the loop.

### B.2 Partially dynamical — gaps

1. **Gravity.** The complete dynamic battery (free-fall/EP, dynamical redshift, deflection, backreaction-norm, $\Box\Phi=-4\pi G\rho$ with finite $c_g$, light-bends-light) passes 16/16 — but lives in `ca-simulation/forks/gr_fork_F64_em_connection.py`. The main engine (`ca_curved.py`, casim gravity) uses a static/instantaneous-Poisson background $K(x)$. **Gap: merge the F64 dynamical Φ into the production engine.**
2. **Confinement.** 2D area law is exact and the rotor chain (F99–F101) derives σ from the rule, but Wilson-loop tests run on frozen links; real-time link Hamiltonian evolution (Kogut–Susskind-type) is not built. 3+1D σ remains the F94 Monte-Carlo route (user-run production script).
   **BUILT 2026-06-06 - 23:55 (F110):** real-time KS link Hamiltonian $H=\frac{g^2}{2}\Sigma\hat E^2-\lambda\Sigma\cos\hat\phi_p$ in `ca-simulation/ca_link_hamiltonian.py` — the F101 rotor made multi-plaquette and dynamical ($\chi=1/(4g^2)$ matrix identity). Gauss law solved exactly (dual height representation; direct-vs-dual full-spectrum identity ≤1.9e-14, vacuum + charged); ℤ₃ exact Hilbert space + truncation-converged U(1); λ=0 potential exact (Tier 1), linear $V(R)$ + PT cross-check at finite λ; real-time unitary evolution (drift ≤2e-14) shows the flux tube persisting at confining coupling and melting at weak coupling. 7/7 PASS, `tests/findings/test_F110_link_hamiltonian_realtime.py`. **Remaining in this item:** dynamical-matter coupling (the P2 leg, C.8), 3D tree-gauge construction, SU(3) Casimir ladder (3+1D σ stays F94 MC); casim engine wiring is engineering.
3. **Colour dielectric/condensate.** `ca_colour_dielectric.py` defines $\varepsilon_c(x)$ and a renormalised rotation step, but it is not wired into the time-evolved gluon propagator; `ca_colour_condensate.py` gap dynamics are not coupled to the dynamical gluon field.

### B.3 Composites — honest classification

| Object | Status | Evidence |
|---|---|---|
| Pion | **dynamical** (best of the three): real-space relative-coordinate q̄q bound state certified — Koster-Slater root = dense diagonalisation to $1.3\times10^{-15}$; Goldstone exact in chiral limit | F103, 13/13 PASS |
| Proton | operator-level only: exact quantum numbers, colour singlet, Fermi antisymmetry, energetic binding $V=\sigma R$ — **no real-time wavepacket, dispersion, or mass measurement** | F71, scope note in finding |
| Deuteron | bound state of a continuum 2-channel radial Hamiltonian (³S₁–³D₁ OPEP), tensor force proven essential ($-2.0$ MeV bound vs $+0.66$ MeV central-only) — **not a lattice real-time object** | F104, 11/11 PASS |

So the answer to "is particle interaction correctly functioning" is **yes at the field/vertex level (all interaction tests pass, ~180 suites)**, and **partially at the composite level** — binding mechanisms are derived and verified, but real-time composite propagation/scattering is future work (roadmap P2).

---

## Part C — Detailed outlines for each underived input

### C.1 Lattice spacing $a$ — the one SI ruler

- **What's already done:** F79 derives the dimensionless prediction $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$ parameter-free, and the closed form returns CODATA $G$ to $3\times10^{-8}$. F83 proves a single measured fermion mass cannot fix $a$ alone (one equation, two unknowns) and brackets $a\in(0,\,3.11\times10^{-18}\,\text{m}]$.
- **Why it can't be fully internal:** any dimensionful number requires one external ruler; the model's job is to reduce the count to exactly one. That reduction is complete.
- **Avenue (per the project's own documents):**
  1. Adopt the F79 value $a=6.5978\,\ell_P$ as canonical (it is the only parameter-free candidate) and treat F83's fermion-mass map as the consistency check, not the anchor.
  2. Close the gravity branch: run the L4 absolute-lensing test on the canonical $K=e^{2u}$ field and confirm the $G$-match independently (deprecated/si-units-options.md Option D).
  3. Falsification gate: GRB/AGN polarimetry. The F30 birefringence onset scales as $1/a$; the F79 value clears existing bounds, the F83 ceiling value does not necessarily — this discriminates the two anchors observationally.
- **Effort class:** small (decision + one test campaign); the physics is done.
- **CLOSED 2026-06-06 - 22:39 (F107):** $a=6.5978\,\ell_P$ adopted; L4 absolute lensing on canonical $K=e^{2u}$ passed (straight-ray $-4$ exact at all $u$; $G$-match and solar 1.7512″ at $3.0\times10^{-8}$); GRB gate discriminates (F79 anchor clears LHAASO $n{=}2$ by $1.9\times10^7$, F83 ceiling excluded by ~9 decades). See `findings/F107-canonical-a-adoption-L4-grb-gate.md`.

### C.2 The sextic brake $C$ / $W$ — the last lepton-spectrum number

- **What's already done:** F95 derived $B$ in closed form and *proved* $C$ cannot come from any per-axis loop (scaling no-go: $|B|\sim\bar y^4$ vs $C\sim\bar y^{7.2}$), localizing it to the second-shell $E_g$ self-interaction. F96 proved the quadratic theory cannot give three distinct masses (two-value theorem) and that the single invariant $W(\sum_a p_a^3)^2$ suffices. F101 found the exact lepton fit as a KKT vacuum over $W\in[0.096,21.6]$ and showed F95's $C=0.636|B|$ independently selects $W^*=1.46$ inside that window.
- **The honest negative:** static uniform-mode RPA yields a **negative** sextic (anti-brake) and loses positivity at the wall — $W$ is not derivable at static one-loop. This is sharply diagnosed, not vague.
- **Avenue (precisely posed in F101):** compute the **momentum-resolved $E_g$-channel bubble** (and/or the second-shell bond self-energy) at saturation amplitude. Hard targets: (i) produce $W\approx1.5$; (ii) restore operator positivity at the wall (the cliff curvature). Success makes the entire charged-lepton spectrum an output of the lattice.
- **Effort class:** the single highest-value computation currently open. Suggest CASIM if the BZ-resolved bubble exceeds sandbox limits.

### C.3 Global-stability invariant (the democratic quartic)

- **Status:** F101 A2 — the lepton point is metastable, squeezed between $(1,1,1)$ and $(0,0,0)$ vacua, closest gap $2.5\times10^{-2}$ at $W\approx0.69$. One more democratic-sector invariant (e.g. quartic $\bar y$ cost) is needed; it was flagged and deliberately not added ad hoc.
- **Avenue:** the same momentum-resolved sea expansion as C.2 should generate the $A_{1g}$-channel quartic alongside the $E_g$ sextic — do both in one computation and check whether the induced $\bar y^4$ coefficient stabilizes the lepton point globally. If it does, C.2 and C.3 close together.
- **Addendum (2026-06-06 - 23:20, F108):** attempted. The flagged democratic candidate is *excluded exactly* — for every $w(\bar y)$ the refit cancels against the democratic shadow and Gap $\ge\Delta_\infty=+0.0386$ (no-go theorem, verified). What works instead: the two-invariant quartic completion $\{v\sum y^4\ (v<0),\ c\,e^4\ (c>0)\}$ makes the exact lepton point the **global** vacuum at fixed $W^*=1.46$, but $v$ feeds the F95 cubic and the angle-shifted $W^*=2.58$ breaks it — the self-consistent $(W,v,c)$ triple is the sharpened open problem. The C.2 momentum-resolved bubble was built and verified ($1.8\times10^{-6}$ vs exact diagonalization) and is honestly negative at one loop (wrong-sign sextic, PD loss at $e\gtrsim0.35$, strongly coupled). See `findings/F108-democratic-no-go-global-stability.md`.

### C.4 The F92 bridge (per-tick chirality → flavor vector)

- **Status:** the identification is constrained to a single point (45°, Fock $\sqrt2$, data-pinned to $1.9\times10^{-5}$) but not constructed from the update rule.
- **Avenue (F92 §6):** a flavor-resolved pairing simulation — evolve the F27 mass step with explicit per-tick $(\cos t,\sin t)$ chirality allocation across three flavor axes and measure whether the collective flavor vector condenses at the $E_g$ angle. This is a simulation build, not new theory; the F27/F93 machinery already exists.
- **Addendum (2026-06-06 - 23:35, F109):** executed. The pair-sum law L1 is now *derived from the update rule* ($U\otimes U$ rotates the symmetric two-quantum channel by exactly $2t$, sympy-exact); the rule-driven phase flow has $t=0$ repulsive (exact rate $4I_2$) and $t=45°$ as the unique attractor (cliff-stiff, wall-pinning dynamical); the flavor-resolved condensation lands on the constrained point with the $(A_{1g},E_g)$ decomposition *measured*: $Q=0.666661$, $\delta=12.733°$, equipartition $0.999991$, Fock $c^2=2.000018$; lepton basin 49.1% with the F108 completion (11.7% metastable minimal; 91.8% wall-constrained). Residuals: relaxational dynamics stands in for real-time QCA condensation; $\cos3\delta$ still fitted. See `findings/F109-f92-bridge-construction.md`.

### C.5 Coupling magnitudes $e$, $g$, $g_s$ + the running gap

- **Status:** the ratio $g'/g$ (hence $\theta_W$) is derived; magnitudes are free. The bare $\sin^2\theta_W=1/4$ sits +12% from PDG 0.2232, and F48 notes the same gap appears in $m_Z/m_W$ and $g_V^{e_L}$ — one number to explain, in three observables.
- **Avenue:**
  1. **Running:** implement lattice loop corrections / RG flow from the bare second-shell scale down — the model has no running at all today, and F48 explicitly assigns the 12% gap to this. Even a leading-log lattice computation would be decisive (it must close the same gap in all three observables simultaneously — a built-in cross-check).
  2. **Magnitude of $g_s$:** the confinement chain offers an internal route — F100/F101 tie σ and the dispersion to one operator ($\sigma_1=\frac14\langle1/\Omega\rangle_{BZ}$); matching the physical string tension (F94 MC) to that form fixes the bare colour coupling internally.
  3. **Magnitude of $e$:** currently no internal route proposed in the findings. The honest options: (a) treat $\alpha$ as the second external ruler alongside $a$; or (b) investigate whether the F87 charge-linearity + paired-photon normalization plus the F95 sextic's $e^6$ appearance over-determines $e$ — the $e^6\cos^23\delta$ structure means a successful C.2 derivation *also* constrains $e$. Worth one dedicated analysis note.

### C.6 NJL calibration ($\Lambda$, $G\Lambda^2$, $m_0$)

- **Status:** F77's three numbers are a fit to measured hadronic data; F103/F104 inherit them verbatim ("no new free physics" downstream, but the upstream fit remains).
- **Avenue:**
  1. $G$ (the four-fermion contact) should come from the model's own binder: F97/F98 prove enforcer = binder = the colour dielectric ($\sigma R$). Integrating out the dynamical gluon/dielectric at the second shell should produce the contact coupling — the same Sakharov-style induced-coupling logic already validated in F57–F61/F79 and F95. F88's hand-off ($v=m_D/e=0.713$, $\sigma_{F86}=2\pi v^2$) is the existing bridge to build on.
  2. $\Lambda$ (the cutoff) is naturally the lattice/BZ edge — it should not be free at all once the NJL is re-derived *on the BCC lattice* instead of in continuum form; the BZ integral replaces the cutoff. This is a re-derivation task, not a fit.
  3. $m_0$ (current quark mass) belongs to the same class as the lepton masses: target of the F92–F101 machinery extended to the quark sector (the F97 no-go already shows the baryon side uses centre closure, not phase kinematics — but the *current-mass* texture is still the orthorhombic condensate's job).

### C.7 $g_A=1.272$

- **Status:** external, entering only through Goldberger-Treiman.
- **Avenue:** $g_A$ is a nucleon matrix element — it requires the dynamical baryon (roadmap P2). Once a real-time three-quark bound state exists, $g_A$ is the axial-current expectation in that state; no new theory needed, only the P2 build. Until then it is correctly flagged as the deuteron's one external coupling.

### C.8 $M_N=938.9$ MeV

- **Status:** external; P2 not built.
- **Avenue (roadmap-matter-binding P2):** dynamical proton/neutron mass = constituent quarks (F77 gap, derived) + confinement energy (F70/F94 σ, derived) in a real-time three-body simulation. The F97 quantitative check (PDG quark-sum/proton = 0.96% via confinement energy) already confirms the decomposition is right; P2 turns it into a computed number. Dependencies: real-time link evolution (B.2 item 2) is the main blocker.

### C.9 Hard-core radius $r_c=0.448$ fm

- **Status:** the one tuned knob in F104; flagged in the finding itself.
- **Avenue (stated in F104):** derive the short-range repulsion from (a) heavy-meson (ω/σ) exchange — the σ is already in the model as the pion's chiral partner at $2m_c$ (F77/F103), and the ω is a vector q̄q state reachable by the same RPA ladder; or (b) a lattice contact term from quark substructure (Pauli repulsion between overlapping three-quark singlets — requires P2). Route (a) is buildable now with existing F77 machinery: add the vector/scalar channels to the OPEP and check whether the induced core reproduces $r_c\approx0.45$ fm and $E_b=2.224$ MeV with zero tuning.

### C.10 $g_{\rho\pi\pi}\simeq6$

- **Status:** external, Tier-3, used only for the light/heavy contrast (KSRF relation).
- **Avenue:** the ρ pole is the vector channel of the same F77 ladder — extending the RPA to the vector channel yields $g_{\rho\pi\pi}$ internally. Low priority (decorative, not load-bearing).

---

## Recommended priority order

1. **C.2 + C.3 together** — momentum-resolved $E_g$ bubble (one computation, two closures; makes the lepton spectrum an output).
2. **C.1** — adopt $a=6.5978\,\ell_P$, run L4 absolute lensing + GRB polarimetry gate (cheap, unlocks all SI predictions).
3. **B.2 item 1** — merge F64 dynamical Φ into the production engine (engineering, no new physics).
4. **C.6 item 2** — re-derive NJL on the BCC lattice (kills $\Lambda$ as an input structurally).
5. **C.9 route (a)** — ω/σ exchange core (buildable now, removes F104's only knob).
6. **B.2 item 2 → C.8 → C.7** — real-time links → P2 dynamical baryon → $M_N$, $g_A$ (the long pole).
7. **C.5 item 1** — lattice running for the 12% Weinberg gap (three observables, one number — high falsification value).

---

## Sources

- `findings/` F25–F104 (key: F45, F48, F64, F70/F71, F75, F77, F79, F83, F87, F90–F93, F95–F104)
- `docs/status/exactness-inventory.md` (2026-06-06 - 16:56) — Tier tallies, #179–180 stability fix, failing/not-yet-met table
- `docs/status/project-status.md`, `docs/roadmaps/next-steps.md`, `deprecated/si-units-options.md`, `docs/roadmaps/roadmap-matter-binding.md`, `docs/theory/key-decisions.md`
- `ca-simulation/` modules and `tests/findings/` suites cited inline
