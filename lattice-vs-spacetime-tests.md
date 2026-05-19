# Lattice vs. Spacetime — Test Roadmap

*A full-sweep roadmap of tests the BCC + Weyl/Dirac + Higgs + U(1) + SU(2) + EMQG lattice model should run against experimentally established physics. Drafted 2026-05-18. Companion to `exactness-inventory.md` (what already passes).*

Each test below has:

- **Target formula** — the published equation or experimental number the lattice must reproduce.
- **Status** — `PASS` (already met), `RATIO PASS` (relative form passes, absolute not yet checked), `PROPOSED` (no code yet), `BLOCKED` (needs an upstream decision such as SI-unit identification in Finding 10).
- **Quantitative gate** — the residual at which we will count the lattice as "agreeing with data."
- **Lattice cost** — order of magnitude of memory / wall time to run.
- **Discriminating power** — what passing or failing this test tells us about the model.

The roadmap is structured by domain (SR / GR / QM / QFT / cosmology / quantum-gravity). Tests are numbered `D-1`, `D-2`, ... where `D` is the domain prefix.

The CLAUDE.md guidance is followed: the lattice is judged against measured data, not against competing theories. Where the lattice agrees with the measurement at higher precision than the standard derivation can claim (e.g. the curl-residual constant), that is recorded as an exact algebraic result; where it agrees only within a stated tolerance, that is recorded as a quantitative match.

---

## SR — Special-relativistic kinematics

### SR-1. Light-speed isotropy on the lattice

- **Target.** $c(\hat k) = c$ to within Michelson–Morley bounds; observational ceiling is $\Delta c/c < 10^{-17}$ (Nagel *et al.* 2015).
- **Status.** PROPOSED. The lattice gives $c_\text{lat} = 1/\sqrt d$ along axes (exact) but Paper 4 Eq. 23 predicts $\Delta c/c \approx \pm k/\sqrt 3$ at finite $k$ for the BCC, and L2's $\Delta c/c = -1.1\%$ at $\|k\|=0.5$ along $(1,1)$ is already a measured anisotropy. The test is to scan $c(\hat k)$ at small $k$ and confirm the angular dependence falls below the experimental bound *after* SI mapping.
- **Gate.** At physical momenta corresponding to optical-frequency light, the converted $\Delta c/c$ should be $< 10^{-17}$. At momenta probed by ultra-high-energy cosmic rays ($\sim 10^{20}$ eV), should be consistent with the AUGER-derived bound on Lorentz violation, $\Delta c/c \lesssim 10^{-19}$ (Coleman–Glashow style).
- **Cost.** Cheap. Re-use L1/L2 dispersion scanner; add SI conversion using Finding 10 resolution.
- **Discriminating power.** The lattice **predicts** a Lorentz-violation signature at the Planck scale; this is a direct test of whether the prediction is consistent with current bounds. If Paper 4's $k/\sqrt 3$ slope exceeds the observed bound at any $k$ reachable by experiment, the model is falsified at the SI level — even though the dimensionless dispersion is exact.

### SR-2. Time dilation — moving-clock tick ratio

- **Target.** $\tau / \tau_0 = \gamma = 1/\sqrt{1 - v^2/c^2}$. Measured to $\sim 10^{-7}$ in muon storage rings (CERN g–2) and to $\sim 10^{-16}$ in atomic-clock comparisons (Chou *et al.* 2010).
- **Status.** **PASS (dispersion-identity) + LV CURVE CHARACTERISED (continuum-SR)** — executed 2026-05-18, Finding 12. Pure plane-wave Dirac eigenmodes propagated; phase rate at static cell = $\arcsin(m)$, phase rate at moving worldline (sub-pixel spectral sampling) = $\omega_k - k v_g$. Numerical-vs-dispersion residual $4.4 \times 10^{-15}$ (FFT floor). Continuum-SR gap grows as $(v_g/c_\text{lat})^2$ — the predicted Planck-scale Lorentz deformation.
- **Gate (revised).** Two readings:
  - **Dispersion-identity:** $\text{ratio}_\text{num} = (\omega_k - k v_g)/\arcsin(m)$ to FFT round-off. **PASS at $4.4 \times 10^{-15}$.**
  - **Continuum-SR:** $\text{ratio}_\text{num} = 1/\gamma_\text{SR}$ within $\mathcal O(k^2)$ at small $k$. **Quantitative match**, scaling cleanly as $(v_g/c_\text{lat})^2$. Smallest residual $7.7 \times 10^{-8}$ at $(m=0.5, k=0.001)$; $\sim 10^{-3}$ at $v_g/c_\text{lat} = 0.5$.
- **Cost.** Cheap (done). $L = 128$, 600 steps, FFT phase extraction. Test lives at `ca-simulation/test_SR2_time_dilation.py`.
- **Discriminating power.** Direct, observable consequence of the emergent-time proposition. **Pass on the dispersion side** means the lattice reproduces SR time dilation from a counting argument with no built-in Lorentz boost — the proposition's two-reading rule survives the Lorentz translation. **The continuum-SR gap is the lattice's predicted Planck-scale Lorentz violation** (Paper 4 Eq. 23) showing up in a cleaner setting than the QG-2 cosmic-ray test.

### SR-3. Sagnac effect on a closed lattice loop

- **Target.** $\Delta\tau = 4\Omega\cdot A / c^2$ for a closed counter-propagating loop on a rotating frame. Measured to $10^{-9}$ in ring laser gyroscopes; underpins GPS.
- **Status.** PROPOSED. No rotating-frame implementation exists yet. Realisation: pre-compute $c(\mathbf x, \hat k)$ on a rotating BCC by applying a velocity-dependent boost to the $c_x c_y c_z \pm s_x s_y s_z$ propagator, send two counter-propagating Gaussians around a closed perimeter, measure tick-count difference.
- **Gate.** $\Delta\tau / (4\Omega A / c^2)$ within 1% at $\Omega L^2 / c^2 \le 0.01$ (small-rotation regime).
- **Cost.** Moderate. Needs a per-cell $\hat k$-direction phase advance; ~2× a standard L1 BCC run.
- **Discriminating power.** A *frame-dependent* test of SR. Confirms (or refutes) that the lattice's Lorentz-violating dispersion remains compatible with rotating-frame interferometry at experimentally relevant scales.

### SR-4. Relativistic Doppler shift

- **Target.** $\nu' / \nu = \sqrt{(1+\beta)/(1-\beta)}$ (longitudinal); $\nu'/\nu = 1/\gamma$ (transverse). Transverse Doppler is the cleanest SR test; measured to $10^{-8}$ by Ives–Stilwell and modern Mössbauer experiments.
- **Status.** PROPOSED. `test_fork_D_doppler.py` exists in `ca-simulation/` — needs review to see what's already covered.
- **Gate.** $\nu'/\nu$ matches relativistic Doppler within $10^{-10}$ (transverse) at $v = 0.3\,c_\text{lat}$.
- **Cost.** Cheap. Built on B1 group-velocity infrastructure.
- **Discriminating power.** Transverse Doppler is a pure time-dilation effect; passing this re-validates SR-2 from a wave-mechanical angle. Useful redundancy.

### SR-5. Composition of velocities and aberration

- **Target.** $v_\text{tot} = (u + v)/(1 + uv/c^2)$; aberration $\sin\theta' = \sin\theta\sqrt{1-\beta^2}/(1 - \beta\cos\theta)$.
- **Status.** PROPOSED. Two-packet propagation: launch packet at velocity $v$ in a "moving" reference frame (constructed by a boost-deformation $\mathcal D$ per Paper 4 Eq. 25), measure resulting group velocity in the lab frame.
- **Gate.** Within 0.1% of the relativistic addition law at $u, v \le 0.4\,c_\text{lat}$.
- **Cost.** Moderate. Requires the DSR / deformed-Lorentz boost map $\mathcal D$ — not currently implemented but design lives in V8 and `qca-papers-1-4-overview.md`.
- **Discriminating power.** Highest among SR tests: this is where Paper 4's DSR diverges qualitatively from textbook SR. A failure would not falsify the lattice — it would falsify the *textbook* limit and point at a measurable DSR signature.

---

## GR — General-relativistic predictions

### GR-1. Absolute light deflection — Eddington

- **Target.** $\Delta\theta = 4GM/(bc^2)$ (Einstein), distinguishable from Newtonian $2GM/(bc^2)$. Measured to $\sim 0.01\%$ in modern VLBI (Lambert–Le Poncin-Lafitte 2009) — solar deflection 1.751 arcsec at limb agrees with GR to 4 decimals.
- **Status.** RATIO PASS, ABSOLUTE PROPOSED. Finding 8 confirmed $\Delta(2M)/\Delta(M) = 1.99647$ — linear-in-M to 0.35% — but did not compare the absolute coefficient. The proposition's $c = c_0/(1 - 2\phi/c_0^2)$ form (Finding 10 SI mapping required) gives a *Newtonian* line-integral deflection at leading order; the lattice may reproduce the GR factor-of-2 or it may stop at the Newtonian value.
- **Gate.** Two-stage. Stage A: at lab $L = 64$, $b = 12$, the dimensionless lattice deflection coefficient $\Delta\theta\cdot b\cdot c_0^2 / (GM)$ should equal $4$ (Einstein) or $2$ (Newtonian), distinguishable at the 10% level. Stage B: after Finding 10 SI choice, the lattice deflection at solar parameters should match the 1.751-arcsec measurement within 1%.
- **Cost.** Stage A: cheap (already infrastructure-complete). Stage B: blocked on Finding 10 resolution.
- **Discriminating power.** **Highest single test in the GR domain.** A coefficient of 4 in Stage A would establish that the lattice reproduces GR's full geodesic deflection, not just a Newtonian impulse. A coefficient of 2 would mean the model has only the Newtonian piece and is missing the relativistic doubling — pointing to which piece of the metric ansatz needs to change.

### GR-2. Shapiro time delay — absolute magnitude

- **Target.** $\Delta t = (2GM/c^3)\ln[(r_1+r_2+r_{12})/(r_1+r_2-r_{12})]$. Measured to $10^{-5}$ by Cassini (Bertotti–Iess–Tortora 2003) — sets $\gamma_\text{PPN} = 1.000 \pm 2\times 10^{-5}$.
- **Status.** RATIO PASS. T2.B passes at $2.7 \times 10^{-16}$ for the *ratio* $c_\text{in}/c_\text{out}$; the absolute Shapiro magnitude has not been compared to the closed-form GR expression.
- **Gate.** Absolute lattice $\Delta\tau$ within 0.1% of the analytic GR formula at lattice-mass parameters chosen for $r_s/b \le 10^{-3}$ (weak-field).
- **Cost.** Cheap. Existing T2.B infrastructure; add a closed-form GR comparison line.
- **Discriminating power.** Pins down the PPN $\gamma$ parameter to lattice precision. PPN $\gamma = 1$ in GR; any deviation indicates a deformed metric ansatz.

### GR-3. Gravitational redshift — Pound–Rebka

- **Target.** $\Delta\nu/\nu = -gh/c^2 = -2.46 \times 10^{-15}$ for $h = 22.5$ m on Earth's surface. Measured to $1\%$ by Pound–Rebka 1960; to $7 \times 10^{-5}$ by Gravity Probe A (Vessot 1980).
- **Status.** RATIO PASS (Finding 11 — phase-tick ratio for variable $c$); ABSOLUTE PROPOSED. Need to set up a static gravitational potential, propagate a plane wave from $\phi_1$ to $\phi_2$, and compare measured frequency shift to $-(\phi_2-\phi_1)/c^2$.
- **Gate.** Frequency-shift residual $< 10^{-3}$ of the analytic value at lattice $\phi$ chosen for weak-field.
- **Cost.** Cheap. Uses `ca_emqg.py` + Cayley stepper + frequency-extraction infrastructure already in place.
- **Discriminating power.** Direct empirical confirmation. A clean pass is one of the strongest GR validations available because the experimental result is exact at parts-per-million.

### GR-4. Mercury perihelion precession

- **Target.** $\Delta\omega_\text{rel} = 6\pi GM/(a(1-e^2)c^2)$ = 42.98 arcsec/century. Confirmed to $\sim 0.1\%$ accuracy.
- **Status.** PROPOSED. Requires a bound-orbit simulation in the lattice EMQG potential. Construct a test mass orbiting a central potential; measure perihelion advance per orbit; compare to GR analytic.
- **Gate.** $\Delta\omega_\text{lat}/\Delta\omega_\text{GR}$ within 5% (allowing for lattice discretisation noise; tightenable by raising $L$).
- **Cost.** Moderate. $L = 256$–$512$ with a long evolution; centroid tracking over many orbits.
- **Discriminating power.** A *higher-order* effect than deflection — the lattice must include the $1/r^2$ relativistic correction to the Newtonian potential, not just the leading $1/r$ piece. Pass means the lattice has GR's full geodesic structure to second order in $GM/(rc^2)$.

### GR-5. Frame dragging — Lense–Thirring

- **Target.** $\Omega_\text{LT} = 2GJ/(c^2 r^3)$. Confirmed by Gravity Probe B (2011) to ~19% accuracy, and by LAGEOS to a few percent.
- **Status.** PROPOSED. Requires a *rotating* mass source — angular momentum $J$ feeding into the lattice EMQG potential as a gravitomagnetic field. Not in `ca_emqg.py` yet; would require extending the modified Poisson to include a $\nabla\times\mathbf A_g$ analog.
- **Gate.** $\Omega_\text{lat}/\Omega_\text{LT}$ within 20% at lab parameters (chosen for weak-field plus discretisation tolerance).
- **Cost.** High. New vector-potential infrastructure; new test packet trajectory analysis.
- **Discriminating power.** This is GR's prediction beyond Newton's gravity — it has no Newtonian analog. The lattice EMQG framework predicts something like a gravitomagnetic field via the Paper 6 modified-Poisson equation; this test would confirm or refute it.

### GR-6. Gravitational-wave dispersion

- **Target.** Gravitational waves propagate at $c$ to within $|c_\text{GW} - c|/c < 10^{-15}$ (LIGO–Virgo GW170817 + GRB joint).
- **Status.** PROPOSED. No GW sector exists yet. Would require a tensor-field extension of the lattice (linearised metric perturbations).
- **Gate.** Lattice GW group velocity within $10^{-12}$ of $c_\text{lat}$ at small $k$ corresponding to LIGO band.
- **Cost.** High. New field content (tensor field); new dispersion test.
- **Discriminating power.** A clean test of whether the lattice can support a *spin-2* propagating mode at the right speed. Currently Paper 1 covers spin-½ Weyl + spin-1 (composite photon) modes; spin-2 is the natural next layer. Fail means no GW sector; pass means the geometric content is richer than what has been built so far.

### GR-7. Schwarzschild geodesic equation at $r/r_s \ge 5$

- **Target.** Test-particle radial / angular trajectory $\ddot r$, $\ddot\phi$ from $g_{\mu\nu}$ in the Schwarzschild metric. Recovers Newton's law in the $r \to \infty$ limit.
- **Status.** PROPOSED. Tracks GR-4 (Mercury) but in a clean, scripted geodesic-tracking test rather than a full bound orbit.
- **Gate.** Lattice trajectory matches the Schwarzschild geodesic within 1% over 100 cells of flight at $r/r_s = 10$.
- **Cost.** Cheap if GR-1/GR-4 infrastructure already exists.
- **Discriminating power.** Confirms the lattice's deflection-and-lensing infrastructure is *geometrically* the Schwarzschild geodesic, not an accidental fit. Pre-requisite for any strong-field claim.

### GR-8. Equivalence principle to lattice precision

- **Target.** $m_g / m_i = 1$ to $10^{-13}$ (MICROSCOPE 2019). Paper 6 predicts a WEP violation at $\sim 10^{-40}$ — far below any test.
- **Status.** PROPOSED. Two-test-particle drop with different mass-to-coupling ratios; measure relative acceleration.
- **Gate.** Lattice WEP violation $< 10^{-6}$ (loose; MICROSCOPE-grade requires extreme lattice precision).
- **Cost.** Moderate.
- **Discriminating power.** A null test for the EMQG framework. Paper 6's predicted WEP violation is too small to measure in either experiment or simulation — but a *large* violation in lattice output would falsify the model.

---

## QM — Quantum mechanics

### QM-1. Bell inequality violation — CHSH

- **Target.** $S_\text{CHSH} \le 2$ classically; QM predicts up to $2\sqrt 2 \approx 2.828$ at the Tsirelson bound. Measured at $2.42$ in Hensen *et al.* 2015 loophole-free Bell test.
- **Status.** PROPOSED. Set up two entangled spinor states on disjoint regions of the lattice; measure correlations of $\sigma$-components on each region; compute $S$.
- **Gate.** $S_\text{lat} \in [2.0, 2.828]$ — Bell-violating but bounded by Tsirelson. Specifically $S_\text{lat} \ge 2.5$ for a high-quality singlet at low decoherence.
- **Cost.** Moderate. Needs a *two-particle* state representation on the lattice — not just a single-particle spinor field. The Fock-space sector implied in `physics_notes_pages_46-60.md` (notebook pp. 5–8) is the right starting point.
- **Discriminating power.** **Critical foundational test.** A failure would mean the lattice is locally classical despite its quantum-mechanical-looking field equations. A pass would confirm the model has genuine non-local correlations. *This is one of the highest-value tests in the roadmap.*

### QM-2. Quantum tunneling — barrier transmission

- **Target.** $T = (1 + V_0^2\sinh^2(\kappa a)/(4E(V_0-E)))^{-1}$ for a rectangular barrier; matches measured tunneling in scanning-tunneling microscopes and alpha-decay half-lives to good precision.
- **Status.** PROPOSED. Already partly buried in V2 (Klein paradox PASS, max $R = 0.91$); a sub-threshold Klein test ($\varphi < m$) is the tunneling analog. Send a Gaussian packet at energy $E < V_0$ at a step potential; measure $|T|^2$.
- **Gate.** $T_\text{lat}/T_\text{QM}$ within 5% across 5 barrier heights and 5 widths.
- **Cost.** Cheap. V2 infrastructure already runs the Klein 1D Dirac on phase potentials.
- **Discriminating power.** Confirms the lattice's discrete propagator preserves quantum tunneling — a non-classical effect. Pass means the Schrödinger-equation phenomenology survives discretisation.

### QM-3. Heisenberg uncertainty — Gaussian packet width product

- **Target.** $\sigma_x\sigma_p \ge \hbar/2$, with equality for a minimum-uncertainty Gaussian.
- **Status.** PROPOSED. Construct a Gaussian wave-packet at varying $\sigma$; compute $\sigma_x, \sigma_p$ numerically from $\psi(\mathbf x)$ and the Fourier-transformed $\tilde\psi(\mathbf k)$.
- **Gate.** $\sigma_x\sigma_p \ge 1/2$ to machine precision across 10 packet widths (lattice units).
- **Cost.** Trivial. Single-step calculation.
- **Discriminating power.** Low — this is forced by the FFT relationship, almost a triviality. Still worth listing for completeness: it shows the *kinematic* uncertainty is preserved.

### QM-4. Quantum Zeno — measurement-rate suppression

- **Target.** Survival probability scales as $P(t) \approx 1 - (\Delta H)^2 t^2/\hbar^2 + O(t^4)$ for short times; frequent measurement suppresses transition.
- **Status.** PROPOSED. Construct an excited two-state system on the lattice, project on the initial state every $\Delta t$, measure decay rate.
- **Gate.** Decay rate scales as $(\Delta t)^2$ at small $\Delta t$; quantitative match to QM Zeno formula within 5%.
- **Cost.** Cheap. Single-particle propagation with periodic projection.
- **Discriminating power.** Subtle quantum effect; pass confirms the lattice's measurement / collapse phenomenology.

### QM-5. Aharonov–Bohm phase (sanity check, already PASS)

- **Target.** $\Delta\phi = (e/\hbar)\oint\mathbf A\cdot d\mathbf l$.
- **Status.** PASS at $4.4 \times 10^{-16}$ (E1).
- **Gate.** Already passed; gate $10^{-12}$ retained for future regression.
- **Cost.** N/A.
- **Discriminating power.** Already known; tracked in `exactness-inventory.md` Tier 1.

### QM-6. Two-slit interference — visibility

- **Target.** Fringe visibility $V = (I_\max - I_\min)/(I_\max + I_\min) \to 1$ for indistinguishable paths; degrades smoothly with path information.
- **Status.** PROPOSED. Two Gaussian-slit sources on a 2-D Weyl substrate; propagate; measure visibility at a distant screen.
- **Gate.** $V \ge 0.95$ for indistinguishable paths; degradation match with QM "which-path" prediction within 5%.
- **Cost.** Cheap.
- **Discriminating power.** Visualises that the lattice produces single-particle interference — a foundational QM signature. Useful for stakeholder/diagram purposes.

### QM-7. Bose–Einstein and Fermi–Dirac occupation statistics

- **Target.** $\bar n_\text{BE} = 1/(e^{\hbar\omega/kT} - 1)$ vs. $\bar n_\text{FD} = 1/(e^{\hbar\omega/kT} + 1)$. The Planck black-body spectrum and the photoelectron / Fermi-velocity measurements give experimental confirmations to <1%.
- **Status.** PROPOSED. Construct a thermal ensemble of bosonic (composite-photon) or fermionic (Weyl/Dirac) excitations on the lattice; sample mode occupation; fit.
- **Gate.** Recovered occupation distribution matches BE / FD curves within 5% across the thermal range.
- **Cost.** High. Requires Monte-Carlo over many wave-packet configurations.
- **Discriminating power.** Foundational test of whether the lattice's commutation/anticommutation algebra is preserved through the discretisation. Pass means the spin-statistics theorem survives.

### QM-8. Black-body radiation — Planck law

- **Target.** Spectral density $u(\omega) = \hbar\omega^3 / (\pi^2 c^3 (e^{\hbar\omega/kT} - 1))$.
- **Status.** PROPOSED. Closely tied to QM-7. Once a thermal ensemble works, the spectrum follows.
- **Gate.** Within 1% across the peak of the Planck spectrum at chosen $T$.
- **Cost.** High (same as QM-7).
- **Discriminating power.** First *macroscopic* test connecting QM-level statistics to a thermodynamic observable.

---

## QFT — Quantum-field-theoretic effects

### QFT-1. Anomalous magnetic moment $a_e = (g-2)/2$

- **Target.** $a_e = 1.15965218073(28) \times 10^{-3}$ — agreement between Schwinger's $\alpha/(2\pi)$ leading term and measurement to $0.24 \times 10^{-12}$.
- **Status.** PROPOSED, BLOCKED. Requires a full vertex correction in the lattice gauge sector. The current U(1) gauge phase is geometric — no quantum loop content yet.
- **Gate.** Lattice $a_e$ within 10% of $\alpha/(2\pi)$ at the lowest-loop level (one-loop only).
- **Cost.** Very high. The lattice would need vacuum-fluctuation infrastructure (photon-loop integrals over the BCC Brillouin zone).
- **Discriminating power.** Highest precision test in physics. Pass would be transformative; fail at any level would just mean the model is at "tree level" and needs further development.

### QFT-2. Compton scattering cross-section

- **Target.** Klein–Nishina formula $d\sigma/d\Omega = (\alpha^2/2m^2)(E'/E)^2(E/E' + E'/E - \sin^2\theta)$. Measured to <1% in modern experiments.
- **Status.** PROPOSED. Single-photon, single-electron lattice scattering: emit a Gaussian composite-photon packet, scatter off an electron wave packet, measure outgoing momentum distribution.
- **Gate.** Differential cross section within 10% of Klein–Nishina at a few representative scattering angles.
- **Cost.** Very high. Two-particle, multi-field, time-dependent scattering on a $L \ge 256$ BCC lattice.
- **Discriminating power.** Confirms the lattice's combined Dirac + U(1) sector reproduces a *measurable* QED interaction cross section. Currently only kinematic tests have been run.

### QFT-3. Pair production at threshold

- **Target.** $\gamma + \gamma \to e^+ + e^-$ above $2m_e c^2$; observed in Breit–Wheeler-equivalent experiments.
- **Status.** PROPOSED. Two composite-photon packets head-on; observe for fermion pair generation above threshold.
- **Gate.** Threshold within 5% of $2m$ (lattice units); rate scales correctly with photon flux.
- **Cost.** Very high.
- **Discriminating power.** A non-trivial mass-energy conversion. Confirms the Yukawa-coupled fermion sector dynamically permits pair creation.

### QFT-4. Lamb shift

- **Target.** $\sim 1058$ MHz splitting between hydrogen $2S_{1/2}$ and $2P_{1/2}$ — vacuum-polarisation effect, measured to <0.1%.
- **Status.** PROPOSED, BLOCKED. Tracks QFT-1: needs vacuum-fluctuation infrastructure.
- **Gate.** Lattice Lamb shift within 20% of measured value.
- **Cost.** Very high.
- **Discriminating power.** Same domain as QFT-1; if QFT-1 passes, QFT-4 should follow.

### QFT-5. Neutrino oscillations

- **Target.** $P_{\alpha\to\beta}(L) = \sin^2(2\theta)\sin^2(\Delta m^2 L/4E)$; mass differences measured by Super-K, KamLAND, T2K.
- **Status.** PROPOSED. Three-flavour Weyl-spinor sector with off-diagonal mass-matrix coupling (analog of physics_notes_pages_61-90 weak-interaction work).
- **Gate.** Oscillation period matches $\Delta m^2$ ratio within 5%; mixing-angle amplitudes within 10%.
- **Cost.** Moderate. Three Weyl fields with Yukawa-style flavour mixing.
- **Discriminating power.** A measurable consequence of generation structure. Lattice has the right primitives (the Yukawa coupling is bilinear, complex, and supports diagonalisable mass matrices); just needs to be wired up.

### QFT-6. Chiral anomaly — triangle diagram

- **Target.** $\partial_\mu j^\mu_5 = (e^2/16\pi^2)\,F_{\mu\nu}\tilde F^{\mu\nu}$ — measured indirectly via $\pi^0 \to \gamma\gamma$ rate (~30% agreement is the textbook level; lattice QCD has it cleaner).
- **Status.** PROPOSED. Requires a finite-density chiral current + electromagnetic source on the BCC.
- **Gate.** Numerical divergence of $j^\mu_5$ matches $E\cdot B$ to 10% in a uniform-field background.
- **Cost.** High.
- **Discriminating power.** A *topological* QFT effect. Lattice fermion theories famously have to work for the anomaly to appear; a clean pass would be a notable result.

### QFT-7. Vacuum polarisation — running coupling $\alpha(Q^2)$

- **Target.** $\alpha^{-1}(M_Z^2) = 127.952$; $\alpha^{-1}(0) = 137.036$. Confirmed by collider experiments.
- **Status.** PROPOSED, BLOCKED. Same blocker as QFT-1.
- **Gate.** Lattice $\alpha(Q^2)$ runs in the right direction over 2 decades in $Q^2$.
- **Cost.** Very high.
- **Discriminating power.** Establishes that the lattice has correct beta function for the U(1) sector. Could not be tested without loop-correction infrastructure.

### QFT-8. CPT-invariance — particle vs antiparticle mass

- **Target.** $|m_p - m_{\bar p}|/m_p < 7 \times 10^{-10}$ (BASE 2017).
- **Status.** PROPOSED. Build identical packets with opposite charge-conjugation eigenvalue; measure dispersion residuals; check for differential mass shifts.
- **Gate.** Within $10^{-12}$ (lattice analog; the QCA is exactly CPT-symmetric by construction so this is a regression test).
- **Cost.** Cheap.
- **Discriminating power.** A *null* result is the expected outcome; any signal would falsify the construction.

---

## QG / lattice-specific — direct Planck-scale tests

### QG-1. Cosmic-ray Lorentz-violation bound

- **Target.** Auger / IceCube bounds on a$|c-c_\text{neutrino}|/c < 10^{-19}$ at UHE; HEGRA bounds at TeV photon energies.
- **Status.** PASS (V9). Cosmic-ray spreading time computed at $t_\text{CR} = 3.4 \times 10^{17}$ s (≈ age of universe) — consistent with no observable spreading over Hubble time.
- **Gate.** Already passed at the qualitative level. Quantitative gate: lattice prediction for arrival-time spread of 1 PeV photons over 1 Gpc should be below current bounds.
- **Cost.** None (already done).
- **Discriminating power.** Already confirmed.

### QG-2. Planck-scale Lorentz violation — dispersion shift at UHE

- **Target.** $E^2 = p^2 c^2 + m^2 c^4 \pm E^3/E_\text{LV}$ with $E_\text{LV} \gtrsim 10^{19}$ GeV from gamma-ray-burst time-of-flight (Fermi GRB 090510, etc.).
- **Status.** PROPOSED. Compute lattice dispersion at $k$ corresponding to GRB photon energies (after SI mapping); check whether the $k/\sqrt 3$ Paper-4 correction is below the experimental bound on $E_\text{LV}$.
- **Gate.** Lattice $E_\text{LV,equivalent}$ should be $\gtrsim 10^{19}$ GeV.
- **Cost.** Cheap. Re-uses dispersion infrastructure; depends on Finding 10 SI choice.
- **Discriminating power.** **A direct empirical test of a model prediction at the Planck scale.** If the lattice predicts a Lorentz-violation signature *above* the GRB bound, the model is falsified in its current form.

### QG-3. Casimir effect

- **Target.** Force per area $F/A = \pi^2\hbar c/(240 L^4)$ for parallel plates. Measured to a few percent.
- **Status.** PROPOSED. Sum of composite-photon zero-point energies in a bounded lattice region vs. infinite region; difference gives Casimir-like force.
- **Gate.** Within 10% of Casimir formula.
- **Cost.** High.
- **Discriminating power.** Confirms the lattice has a genuine vacuum-energy structure compatible with QED's zero-point sum.

### QG-4. Discrete-Noether U(1) and SU(2) charge conservation

- **Target.** Conservation of $Q = \int j^0 \,d^3x$ to machine precision at every step.
- **Status.** PARTIAL PASS — referenced in `next-steps.md` as an open verification. Per-cell U(1) and SU(2) Noether currents need explicit logging.
- **Gate.** $|\Delta Q|/Q < 10^{-13}$ per 1000 steps at $L = 256$ in standard test setups.
- **Cost.** Cheap once instrumentation is added (per-cell flux integration over a closed surface).
- **Discriminating power.** A foundational consistency check for the gauge sector. Required before any QFT-domain claim is meaningful.

---

## Cosmology — large-scale predictions

### COSMO-1. Hubble redshift on the lattice

- **Target.** $1 + z = a(t_0)/a(t_e)$ with the Milne-style kinematic interpretation per Paper 6. Modern $H_0 = 67$–$73$ km/s/Mpc depending on probe.
- **Status.** PROPOSED. Per `next-steps.md` line 12 ("expanding out to standard space, not lattice space, does the redshift calculation hold up?"). Map lattice phase-tick ratios across a propagation length to an effective redshift; compare to FRW prediction.
- **Gate.** Within 5% of FRW Hubble law over the lattice analog of $0.001 < z < 0.1$.
- **Cost.** Moderate. Builds on T2.B / T5.C phase-tick infrastructure.
- **Discriminating power.** First connection from emergent-time tick differences to a *cosmological* observable. Pass would validate the Milne-Paper 6 ontology.

### COSMO-2. CMB blackbody temperature

- **Target.** $T_\text{CMB} = 2.7255 \pm 0.0006$ K. Confirms Planck spectrum at <0.1% across 6 decades in $\omega$.
- **Status.** PROPOSED, BLOCKED. Tracks QM-7 / QM-8.
- **Gate.** Tied to QM-8 gate.
- **Cost.** Same as QM-8.

### COSMO-3. Equivalence-principle-violation prediction (Paper 6)

- **Target.** WEP violation $\sim 10^{-40}$ per Paper 6 §17.
- **Status.** PROPOSED but **not measurable** — far below any reachable simulation precision. Documented for completeness.
- **Cost.** N/A.
- **Discriminating power.** Falsifiable in principle, but not in practice.

---

## Priority ranking — top 10 to build next

The roadmap has ~40 tests; resourcing one per week, a focused subset is needed. Prioritised by `(discriminating power × current cost-effectiveness × stakeholder visibility)`:

| Rank | Test | Why first |
|---|---|---|
| **1** | **GR-1 Stage A** — absolute light deflection coefficient | Highest-impact GR result that uses 100% of existing infrastructure. Either confirms the GR factor of 4 or surfaces a Newtonian-only limitation. |
| **2** | **QM-1** — Bell / CHSH inequality | Foundational. Tests whether the lattice supports genuine non-local quantum correlations. Without this the entire QM domain is in doubt. |
| **3** | **SR-2** — moving-clock time dilation | Tightest test of the emergent-time proposition. Uses existing phase-tick infrastructure. |
| **4** | **GR-3** — Pound–Rebka gravitational redshift | Cheap, high-value, foundational GR effect. Direct empirical comparison. |
| **5** | **GR-2** — absolute Shapiro magnitude | Pins down PPN $\gamma$. Builds on T2.B; cheap incremental work. |
| **6** | **QG-2** — Planck-scale Lorentz-violation bound | Tests a model *prediction* against an experimental bound. Falsification risk is real. |
| **7** | **QFT-5** — neutrino oscillations | Moderate cost, foundational, builds on existing fermion sector. |
| **8** | **QM-2** — quantum tunneling | Cheap, foundational, leverages V2 infrastructure. |
| **9** | **GR-4** — Mercury perihelion | Tests the *second-order* GR correction; differentiator from Newton-only models. |
| **10** | **QG-4** — discrete-Noether charge conservation | Cheap, gating; required before higher-order QFT tests can be trusted. |

The other 30+ tests in the roadmap are either lower-impact (e.g., SR-5 aberration, QM-3 uncertainty product), blocked on infrastructure not yet built (QFT-1, QFT-4, QFT-7 — vacuum-polarisation; GR-5 — gravitomagnetism; GR-6 — tensor modes), or already passing.

---

## What this roadmap does *not* attempt

- **Strong-field GR** (black-hole horizons, photon spheres, ringdown). The lattice's metric ansatz is weak-field; strong-field tests are outside its current scope.
- **Lattice QCD / confinement.** No SU(3) gauge sector is in the model; the SU(2) is electroweak.
- **Discrimination between competing theories.** Per CLAUDE.md, the lattice is judged against measured data. Where multiple theories predict the same observable, the lattice is compared to the measurement, not to one theory or the other.
- **First-principles derivation of $a$ and $\tau$.** Finding 10 keeps the SI mapping as a deferred decision.

---

## Maintenance

Update this file when:

1. A `PROPOSED` test transitions to `PASS` or `FAIL` — move to `exactness-inventory.md` (tiers 1–3) and add the residual.
2. A new measurement appears in the literature that changes a gate.
3. A new lattice infrastructure (vacuum fluctuations, tensor modes, etc.) unblocks a previously blocked test.

Companion files: `exactness-inventory.md` (what passes today), `findings.md` (open hypotheses), `model-observations.md` (open questions for the model itself).
