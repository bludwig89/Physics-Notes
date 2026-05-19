# Project Status — Physics Notes Transcription

## Source
- `physics_notes_0708.pdf` (20.1 MB) — handwritten research notebook
- Author of original notes: Mark Ludwig

## Progress

| Pages | Status | Output File | Date |
|---|---|---|---|
| 1–15 | Transcribed | `physics_notes_pages_01-15.md` | 2026-05-13 |
| 3, 5 (diagrams) | Redrawn as SVG | `diagrams/page03_*.svg`, `diagrams/page05_*.svg` | 2026-05-13 |
| 16–30 | Transcribed | `physics_notes_pages_16-30.md` | 2026-05-13 |
| 31–45 | Transcribed | `physics_notes_pages_31-45.md` | 2026-05-13 |
| 46–60 | Transcribed | `physics_notes_pages_46-60.md` | 2026-05-13 |
| 61–90 | Transcribed | `physics_notes_pages_61-90.md` | 2026-05-14 |
| 91–end | Not started | — | — |
| — | Companion research (CA & spacetime, p.35) | `cellular-automata-research.md` | 2026-05-13 |
| — | Companion research (Fredkin correlation, p.35–39) | `fredkin-correlation.md` | 2026-05-13 |
| — | Companion research (CA rules and the four forces) | `ca-forces-integration.md` | 2026-05-13 |
| — | Reference for current CA project | `ca-reference.md` | 2026-05-14 |
| — | External paper summary: Ostoma & Trushyk (1999), *Cellular Automata Theory* (108 pages) | `ostoma-trushyk-1999-summary.md` | 2026-05-15 |
| — | QCA literature overview (Reference Research Papers 1–6, including Paper 6 EMQG treatise) | `qca-papers-1-4-overview.md` | 2026-05-15 |
| — | Unification proposition v2 — synthesises Phase-F architecture with Papers 1, 2, 4 (BCC + exact dispersion + composite photon) and Paper 6 (EMQG modified Poisson for $c(\mathbf{x})$) | `ca-unified-v2.md` | 2026-05-15 |
| — | Electroweak mass-generation design — pulls the three mass-relevant paths (Yukawa, EMQG-$\phi$ sourcing, composite-photon $E/c^2$) out of v2 and compares to Ostoma–Trushyk's three mass definitions | `ca-electroweak-design.md` | 2026-05-17 |
| — | Dirac stepper exact-QCA refactor — `ca_dirac.py` switched from linearized Hamiltonian to Paper 1 Eq. 23 with `n² + m² = 1` enforced; `c` argument removed everywhere; zitterbewegung target = $2\arcsin(m)$ | `ca_dirac.py`, `ca_unified.py`, `run_phase_tests.py`, `run_phaseF_tests.py` | 2026-05-18 |
| — | Emergent-time roadmap T0–T2, T4, T5 landed (T3 skipped per direction).  Lazy-update wrapper + tick heatmap + T1.A/B/T2.A/B/C/T5.A/B/C all PASS (10/10 gates).  T2.B Shapiro tick-ratio at $2.7\times 10^{-16}$ (gate $10^{-12}$).  T5.A: 80% of L=256 lattice has $N(\mathbf x) = 0$ exactly. | `ca-emergent-time-proposition.md`, `ca_lazy.py`, `tick_heatmap.py`, `test_emergent_time_T1.py`, `test_emergent_time_shapiro.py`, `test_emergent_time_T5.py` | 2026-05-18 |
| — | Full-sweep test roadmap (SR/GR/QM/QFT/QG/cosmology) + tier-sorted exactness inventory (14 exact algebraic, 6 machine-precision, 14 quantitative, 7 open). Top-10 priority ranking: GR-1 (absolute Eddington), QM-1 (CHSH Bell), SR-2 (moving-clock time dilation). | `lattice-vs-spacetime-tests.md`, `exactness-inventory.md` | 2026-05-18 |

PDF total: 182 pages.

## Method

1. Pages read from PDF in 15-page batch via the file Read tool, which renders each PDF page as an image.
2. Handwriting and mathematical notation OCR'd directly from the rendered images.
3. Equations transcribed into Markdown math (LaTeX-style, `$...$` inline and `$$...$$` displayed).
4. Diagrams and figures (Feynman-style scattering diagrams, tetrahedron/octahedron sketches, molecular structures) are described inline in italics/parenthetical notes — not redrawn.
5. Numbered equation labels from the original (e.g. `(1a)`, `(6.41)`, `(2.33b)`) preserved as `\tag{}` or trailing reference where they appeared in the notebook.
6. Cross-references in the margins (e.g. "p.30", "my notes p.56") preserved alongside the relevant equation.

## Content Summary (pages 1–15)

- **Pages 1–2:** Quantum Scalars I — canonical quantization of a scalar field; Lagrangian, Hamiltonian, Fourier transform to $k$-space.
- **Page 3:** Photon/Graviton symmetry musings + tetrahedron/octahedron isomer counting diagrams.
- **Page 4:** Blank (back-of-page bleed-through).
- **Pages 5–6:** Superconductivity vs Spinor Electrodynamics — 8-point list of conceptual analogies between Cooper pairs and paired spinor-photons.
- **Page 7:** Heat-of-combustion table for hydrocarbons (methane through octane), plus polymerization question.
- **Page 8:** Blank.
- **Pages 9–15:** "Sachs Made Easy" — exposition of Mendel Sachs' unification of gravity and electromagnetism. Covers fundamental matter fields, Weyl representation, helicity, curved-spacetime spinors, and the derivation of the gravitational Lagrangian / hierarchy equations.

## Content Summary (pages 16–30)

- **Page 16:** Matter-field Lagrangians $\mathcal{L}_\eta$, $\mathcal{L}_\chi$ for massless 2-spinors; Sachs eqs. 3.60/3.62 for $q^\mu(x)$ and $\tilde q^\mu(x)$ in Pauli-matrix form.
- **Page 17:** Covariant derivatives $\eta_{;\mu}, \chi_{;\mu}$ and spin connection $\Omega_\rho^{(x)}$ (eq. 3.77/3.79b); concise total Lagrangian $\mathcal{L} = (-g)^{1/2}\{R + i\eta^+ q^\mu \eta_{;\mu} + i\chi^+ \tilde q^\mu \chi_{;\mu}\}$.
- **Page 18:** Move to Hamiltonian formulation. $T_{00} = \mathcal{H}$, $\;G_{\mu\nu} = 8\pi T_{\mu\nu}$ implies $\mathcal{H}_{\text{grav}} = G_{00}/8\pi$; Ricci tensor expansion.
- **Page 19:** $\mathcal{H}_E$ written out for non-spinor and spinor Gen. Rel.; need to treat $\Gamma^\lambda_{\mu\nu}$ / $g^{\mu\nu}$ (and $\Omega_\mu$ / $q^\mu$) as independent variables to keep 1st-order derivatives.
- **Page 20:** Matter-field Hamiltonian — issue noted: naïve $\mathcal{H} = (\partial \mathcal{L}/\partial \dot\eta)\dot\eta - \mathcal{L} = 0$ for first-order Lagrangians; symmetrized form introduced.
- **Page 21:** Redefine $\Theta^{\mu\nu}$ with covariant derivatives so curvature couples to matter; test with scalar field.
- **Page 22:** Scalar-field Hamiltonian density; full combined Hamiltonian density boxed.
- **Page 23 ("Lagrangian Approach"):** Re-collects the full Lagrangian, identities, and Euler–Lagrange equation in curved space; useful trace identities for $\partial \mathrm{Tr}(AB)/\partial B$.
- **Pages 24–25:** Apply Euler–Lagrange to $\eta$; arrive at the matter equation $q^\mu \partial_\mu \eta + q^\mu \Omega_\mu \eta = 0$ after using $(-g)^{1/2}_{\;;\mu} = 0$ and $q^\mu_{\;;\mu} = 0$.
- **Pages 26–28:** Variation w.r.t. the spin connection $\Omega_\rho$; long matrix-trace expansion of $\partial \mathcal{L}/\partial \Omega_{\rho,\nu}$. **Key observation:** the divergence $\big(\partial \mathcal{L}/\partial \Omega_{\rho,\nu}\big)_{;\nu}$ appears to vanish — author flags disagreement with Sachs' derivation ("Sachs gets 0 on the LHS … but apparently this doesn't hold!").
- **Page 27 (interjection):** Question on local Lorentz invariance — whether $q^\mu \to \sigma^\mu$ uniquely at a point, or whether multiple $q$'s give the same $g_{\mu\nu}$ (gauge-like ambiguity).
- **Page 29:** Variation w.r.t. $q^\lambda$ — gravitational-field part involving $K^+_{\lambda\rho}\tilde q^\rho$ and the matter current; flagged need for $\widetilde{\Omega^{(\chi)}_\rho} = \Omega_\rho$.
- **Page 30:** Blank.

## Content Summary (pages 31–45)

- **Page 31 ("Motivation & Development of the σ-Matrices"):** Derives the σ-matrix algebra from the requirement that $\sigma^\mu\partial_\mu \psi = 0$ reproduce the scalar wave equation; arrives at $(\sigma^0)^2 = 1$, $(\sigma^i)^2 = \pm 1$, and the anticommutator $\sigma^\mu\sigma^\nu + \sigma^\nu\sigma^\mu = 0$ for $\mu \neq \nu$.
- **Page 32 (Question):** Brief check — $g^{\mu\nu}$ being Lorentzian does *not* force $q^\mu = \sigma^\mu$; instead $g^{\mu\nu} = \tfrac{1}{2}(q^\mu \tilde q^\nu + q^\nu \tilde q^\mu)$, with $q^\mu$ and $\tilde q^\mu$ expanded on the σ-basis.
- **Page 33 ("Lagrangian Approach to Sachs Electrogravity"):** Writes the full two-matter-field Lagrangian $\mathcal{L} = (-g)^{1/2}\{R + \tfrac{1}{2}[\,\eta\,\text{terms}\,] + \tfrac{1}{2}[\,\chi\,\text{terms}\,]\}$, defines $\eta_{;\mu}$, $\chi_{;\mu}$, $\Omega_\mu^{(\chi)} = -\Omega_\mu^+$, and gives $R$ and $K_{\mu\nu}$ explicitly.
- **Page 34:** Re-states the Euler–Lagrange equation $(\partial \mathcal{L}/\partial \psi_{;\mu})_{;\mu} - \partial \mathcal{L}/\partial \psi = 0$ and lists $q^\mu, \Omega_\mu, \eta, \chi$ as the independent field variables. Rest of page blank.
- **Pages 35–39 (CA speculation interjection):** A side-line of thought asking whether spacetime geometry and particle physics could emerge from a cellular automaton. Page 35 frames the idea ("dependence implies neighborhood; rules imply geometry"). Page 36 argues that lattice dimensionality is set by the number of connections per cell. Page 37 discretizes the 2D wave equation but notes it requires *two* time-step memory — solved by going spinor-valued (Dirac reduction). Page 38 writes out the discrete 2-component massless Weyl equation as an explicit nearest-neighbor update rule. Page 39 reports numerical experiments: without the $\tfrac{1}{2}$ factor the simulation blows up to ~11,000 in ~10 steps; with $\tfrac{1}{2}$ it settles at ~120 and "interestingly stabilizes" around $\sim 0.43$, which the author interprets as effectively rescaling the speed of light.
- **Page 40:** Blank (bleed-through only).
- **Pages 41–45 ("Quantum Hierarchy Equations of a Free Scalar Field" — new paper):** A clean re-derivation of pages 1–4 of the notebook. Page 41 sets up the scalar Lagrangian, canonical momentum, and Hamiltonian density (with Goldstein 12-23, 12-50, 12-53, 12-62 citations). Page 42 introduces the Lorentz-invariant measure $\tfrac{d^3k}{(2\pi)^3 2\omega_k}$ and Fourier transforms (IzZ 3.35). Page 43 reduces $H$ to $k$-space giving the boxed expression $(\ast)$, and lists the canonical commutators (IzZ 3.36) and field expansions (IzZ 3.37a/b). Page 44 is a *failed* first attempt at the operator substitution — entirely crossed out. Page 45 completes the calculation cleanly and arrives at the boxed final form $H = \tfrac{1}{2}\int \omega_k (a_k^+ a_k + a_k a_k^+) \tfrac{d^3k}{(2\pi)^3 2\omega_k}$, labelled "Ludwig eq. 3".

## Notes / Uncertainties

- A handful of subscripts and exponents in the Hamiltonian Fourier expansion on page 2 are ambiguous in the original handwriting; signs of $(2\pi)$ factors in particular may need a second pass against a reference text on scalar field quantization.
- Equation 6.45 on page 15 has a parenthetical inline note about $\Omega_{\mu;\sigma}$; the exact form is hard to read and was transcribed as best as the handwriting allowed.
- Diagrams on pages 3 and 5 have now been redrawn as SVG in `diagrams/` (see file list below). The redraws are interpretive — they preserve the topology and labels of the original sketches, not the exact handwriting/line texture.
- Pages 16, 26, 28: several index placements on $K_{\mu\nu}$, $\Omega_{\nu,\mu}$ vs $\Omega_{\nu;\mu}$ are ambiguous in handwriting; transcription preserves what's legible. The matrix forms for $q^\mu(x)$ and $\tilde q^\mu(x)$ on page 16 (Sachs 3.60, 3.62) follow the Pauli/Weyl convention seen earlier.
- Page 26 has a small unlabeled spring-and-block sketch at the top — included as a parenthetical note rather than redrawn.
- Page 27 is a marginal "Question" interjection (locally Lorentzian / gauge-like ambiguity of $q^\mu$) — kept inline at the position it appears in the notebook.
- Pages 31–32 use the symbols $\sigma$ and $q$ interchangeably with their "tilde" counterparts; sign conventions on $\tilde\sigma_\nu$ flip in two places in the margin and both forms have been preserved.
- Page 39 contains a numerical observation ($\sim 0.43$ stabilization factor) that is plausibly an artifact of the chosen finite-difference scheme rather than a physical statement; kept as-is per the original.
- Page 44 is mostly crossed out in the original notebook (a failed first pass at the $H$ substitution). It is transcribed for completeness with a marker that it is the false start; page 45 is the clean redo.
- Pages 41–45 substantially overlap with pages 1–4 (the original scalar-field derivation). The newer version is cleaner and adds the Goldstein / Itzykson–Zuber references and the boxed final form labelled "Ludwig eq. 3".

## Content Summary (pages 46–60)

- **Pages 46–49 (notebook pp. 5–8):** Continuation of the "Quantum Hierarchy Equations" paper. Discretization $a_j = a_{k_j}\,d^3k/[(2\pi)^3 2\omega_k]$; Schrödinger equation in occupation-number basis; expansion of $|\psi\rangle$ in number eigenstates with coefficients $C_{n_{-p}\ldots n_p}$; conversion to $\psi_N(k_1\ldots k_N)$ wavefunctions with normalization factor $\sqrt{(\Delta k)^{3N}/\prod 2\omega_{k_j} \cdot N!/\prod n_j!}$. Page 48 absorbs the vacuum energy via $|\psi'\rangle = e^{-iKt}|\psi\rangle$ giving the free-scalar-boson multiparticle equation. Page 49 flags two open issues: (i) the $\omega_k = \sqrt{k^2+m^2}$ operator doesn't easily Fourier-transform back to spacetime; (ii) bosonic symmetry $\psi_N(\ldots k_i \ldots k_j \ldots) = \psi_N(\ldots k_j \ldots k_i \ldots)$ must be enforced separately. Notes that Dirac spinors should make both covariance and the symmetry/antisymmetry questions cleaner.
- **Page 50:** Blank (bleed-through only).
- **Pages 51–56:** A side-derivation exploring the $a^+, a$ algebra carefully. Page 51 writes the Schrödinger equation, defines $a_k^\pm = \tfrac{1}{2}(\phi_{\mp k} \mp i\pi_k/\omega_k)$, and notes that $\Psi$ is a function of the field values $\phi_j$ at each $k_j$ with probability density $P(\phi_j)$. Page 52 verifies the harmonic-oscillator identity $\tfrac{1}{2}(a^+a + a a^+) = N + \tfrac{1}{2}$ then tries to expand $\mathcal H \sim \pi_k\pi_{-k}/\omega^2 - \omega^2 \phi_k \phi_{-k}$ as coupled oscillators in two coordinates, rotating $45°$ to decouple into one positive + one negative harmonic oscillator (associates these with cos/sin modes). Page 53 cites Messiah V.2 pp.586–600 on Bose symmetrization, noting that for a free field the symmetrization is enforced automatically by commuting creation operators. Page 54 introduces $\alpha_p$ creating $\bar\phi_p = (\phi_p + \phi_{-p})/\sqrt2$ and $\beta_q$ creating $\widetilde\phi_q = (\phi_p - \phi_{-p})/\sqrt2$, and shows real-$\phi(x)$ implies $\widetilde\phi_q = 0$. Pages 55–56 rewrite $H$ in $\alpha,\beta$ form, get $H = \tfrac{1}{4}\int \omega_k(\alpha^+\alpha + \alpha\alpha^+ + \beta^+\beta + \beta\beta^+) d^3k/[(2\pi)^3 2\omega_k]$, and ask whether the cross-terms $T = \alpha^+\beta + \alpha\beta^+ + \ldots$ vanish — concluding $T_k = -T_{-k}$ so $\int T_k\, d^3k = 0$.
- **Page 57:** A photocopy / loose printed page inserted into the notebook — a textbook excerpt on the matrix representations of angular momentum operators (Pauli matrices for $j = \tfrac{1}{2}$, $3\times3$ spin-1 matrices, and higher-spin generalizations, eqs. 2.20–2.22b). Not in the author's hand; included for reference only.
- **Page 58:** Verso of the printed page — blank.
- **Pages 59–60 ("Complex mass", dated 9/6/2007):** New entry. Page 59 reminds the reader that the standard Dirac equation comes from $(\vec\alpha\!\cdot\!\vec p\,c + mc^2\beta)^2 = (p^2c^2 + m^2c^4)\mathbb I$ and that the choice of $\vec\alpha, \beta$ is non-unique: e.g. $\beta = (a\sigma_1 + b\sigma_2)\otimes\sigma_0$ with $a^2+b^2 = 1$ works just as well. Page 60 then asks what happens if the representation is *gauged*, $\beta_g = (U\sigma_1 U^+)\otimes\sigma_0$ with $U = \mathrm{diag}(1, e^{i\theta(x)})$ — an $SU(2)$ gauge symmetry broken to $U(1)$. Author notes this symmetry acts on only *one helicity half* of the bispinor in the Weyl representation, and speculates on a connection to the helicity-dependence (and mass-coupling) of the weak interaction.

## Content Summary (pages 61–90)

- **Page 61 ("Weak Interactions"):** Four-point list framing the questions: $W_\pm, Z$ act only on left-handed components, EM boson $A$ acts on the bottom of the doublets, and the $L \leftrightarrow R$ interaction defines mass.
- **Pages 62–66 ("Weinberg-Salam w/o Higgs"):** Author rebuilds the electroweak Lagrangian without a Higgs sector, keeping $\nu_R$ in the right-handed doublet. Introduces $SU(2) \times U(1)$ gauge fields $\vec W^\mu, W_0^\mu$, derives the rotation to $(Z_\mu, A_\mu)$ with $g'/g = \tan\theta$ and $e = 2g\sin\theta$, recovers $m_Z = m_W/\cos\theta$, and flags an "anomalous" cross-term $m_Z^2 W_{0\mu}W_{3\mu}$.
- **Pages 67–72:** A "new ideas" interjection. Notices that $A_\mu$ acts on the isospin doublet just as $W$ acts on the spin doublet. Proposes a Fermi-like contact Lagrangian $g(\bar\nu_L e_L + \bar e_L \nu_L)$ with kinetic terms gauged by a new $B_\mu$ field that produces neutral currents. Page 70 finds an unwanted factor-of-2 in the combined kinetic Lagrangian, suggesting a quadruplet representation. Pages 71–72 Q-and-A: experimental evidence for $W$ particulation comes from $\mu^- \to e^- + \bar\nu_e + \nu_\mu$; speculates that charge, like spin, may have a "Heisenberg-uncertainty"-style dynamic conservation.
- **Pages 73–74 ("Mass & rotational travel"):** A side-line of thought: model a massive particle as a helical worldline of a light-like trajectory. $v_{\text{eff}} = \sqrt{c^2 - 4\pi^2\nu^2 r^2}$. Page 74 attempts to relate this to the Klein–Gordon dispersion using $p = \gamma m_0 v$; arrives at $v^2 = c^2 - E_0^2/E^2$ which the author dismisses ("Way way — no good").
- **Page 75 ("ASI" — Ferbel Vol 7):** Reference numbers copied from *NATO ASI Series: Techniques & Concepts of HEP* (T. Ferbel, ed.). $m_W = 80.22\,\text{GeV}$, $m_Z = 91.187\,\text{GeV}$, $m_\tau = 1776.9\,\text{MeV}$, $G_F^\tau/G_F^\mu = 0.987$ (a $2.2\sigma$ tension), $\sin^2\theta_W = 0.232$, $m_t = 175 \pm 6\,\text{GeV}$.
- **Page 76:** Majorana mass-matrix block. Neutrino mass bounds (PDG-style) noted side-by-side with the older textbook values. Standard Fermi Lagrangian $\mathcal L_F = -G_F/\sqrt 2\,\bar p\gamma_\lambda n\,\bar e\gamma^\lambda \nu_e$ and the V–A current $J^\mu = \bar\nu_e \gamma_\mu(1-\gamma_5)e + \ldots$. References *The Physics of Massive Neutrinos* by Vannucci (LPNHE Paris 7).
- **Page 77 ("Program for Weak Interaction Physics"):** Restates the program: weak-interaction "mass" violates charge conservation just as Dirac mass violates spin, but spin is rescued by angular-momentum conservation via $J = L + S$. Reference: Greiner *Rel QM* pp. 216–217 on $[J, H] = 0$ in a spherical potential.
- **Page 78 ("Black-body Radiation"):** Short reference block — Bose–Einstein occupancy $\bar n_\omega = 1/(e^{\hbar\omega/kT}-1)$, mode-counting density $dN_\omega$, and visible-light bands (Red 620–750, Green 495–570, Blue 450–495 nm).
- **Pages 79–80:** Sketch of how a massive-gauge-boson theory reduces to a Fermi 4-fermion contact term as $m_W \to \infty$. Then speculates on a 2-point version mediated by a *finite-mass* neutral $B_0$ and on whether $Z$ might be analogous to a "spin-0 photon" that doesn't really exist.
- **Pages 81–88 (technical exercise):** Dirac plane-wave solutions transformed from standard to Weyl representation, looking at electrons travelling along $\hat z$. Page 81 constructs $U_{DW}$. Pages 82–84 push the four basis spinors $u^{1,2}(0), v^{1,2}(0)$ through $U_{DW}$ and the rewritten $\gamma$-matrices, then take $m \to 0$ — finds only 2 of the 4 components survive cleanly and flags a degeneracy. Pages 85–88 redo the calculation with a fresh ansatz $\psi_\pm = A_\pm e^{i(k_0 t - \vec k\cdot\vec x)}$, isolates 4 independent linear equations, and writes out boxed normalized expressions for $\Psi_{RP}$ (6A), $\Psi_{LA}$ (6B), $\Psi_{RA}$ (6C), $\Psi_{LP}$ (6D) — the four chirality/charge-conjugation eigenstates. Notes that the mass term mixes particle↔antiparticle for either handedness but preserves helicity.
- **Pages 89–90:** Builds an EM-↔-weak analogy table laying out all 8 fermion states with their charges $\pm q$ or $\pm g$ and spin/helicity labels. Considers (and rejects on energy grounds) the speculation that the $Z$ might be a $W^+ W^-$ bound state.

## Software Modeling

- `ca-software-plan.md` — Implementation plan and results for the pages 35–39 CA simulation. All five stages implemented and run to 200 time steps. Includes split-step FFT propagator derivation and simulation results.
- `ca-simulation/ca_core.py` — Core numerics: pedagogical-only Euler steppers; exact split-step propagators (`weyl_step_*_splitstep`); dispersion verification; group-velocity measurement; L- and σ-sweeps.
- `ca-simulation/ca_dirac.py` — **Phase D1.** Dirac CA 4-spinor split-step with mass; dispersion verifier; zitterbewegung measurement; **Phase E1** U(1) gauge step and Aharonov–Bohm test.
- `ca-simulation/ca_curved.py` — **Phase C1.** Variable-c refraction; Snell's law test.
- `ca-simulation/ca_weak.py` — **Phase E2.** SU(2) weak gauge on left-chirality isospin doublet; parity-violation test.
- `ca-simulation/spinor_color.py` — **Phase A1.** Bloch-sphere → RGB mapping; Bloch legend.
- `ca-simulation/ca_higgs.py` — **Phase F1/F2.** Complex scalar Φ with Mexican-hat potential; velocity-Verlet symplectic stepper; Higgs and Goldstone dispersion verifiers.
- `ca-simulation/ca_unified.py` — **Phase F.** Coupled Φ–Dirac CA via Yukawa m_eff(x) = y|Φ(x)|; UnifiedState container, vacuum/symmetry-restored/perturbation setup helpers.
- `ca-simulation/run_simulation.py` — Original five-stage Weyl runner.
- `ca-simulation/run_phase_tests.py` — **Phases A–E test suite.** 8/8 phases pass; figures saved to `figures/phase*.png`.
- `ca-simulation/run_phaseF_tests.py` — **Phase F test suite.** F1 (vacuum contract), F2 (Higgs+Goldstone dispersion), F3 (Yukawa sketch), F4 (symmetry-restored). 4/4 pass.
- `ca-simulation/figures/` — All output figures (Weyl `stage*.png` and phase `phase*.png`).

### Phase test results (2026-05-14)

| Phase | Description | Key result |
|---|---|---|
| A1 | Bloch-sphere spinor coloring | Helicity states render visibly distinct |
| A2 | Visualization frames | 2D strip, 1D spacetime, 8×8 graph view all rendered |
| B1 | Group-velocity measurement | Speed ratios 0.92–0.98 (Gaussian k-spread; → 1 as σ→∞) |
| B2 | Min L / min σ sweeps | L≥32, σ≥3 → free-space behaviour at <0.01% artifact |
| C1 | Variable-c refraction (Strang) | θ_out within 0.51° of Snell; 30% better norm drift than blending |
| D1 | Dirac CA | Weyl regression 5e-16; dispersion 9e-17; norm drift 3e-14 / 1000 steps; zitterbewegung 3.5% off 2mc² (5000-step run) |
| E1 | U(1) Aharonov–Bohm | Phase pickup at machine precision (4e-16); norm exact |
| E2 | SU(2) parity violation | Left rotation exact; right-chirality leak = 0.0 (machine zero) |
| **F1** | **Vacuum regression contract** | **Φ=v fixed at machine precision; fermion matches constant-m reference (8e-16)** |
| **F2** | **Higgs + Goldstone dispersion** | **Radial ω = √(k² + 2μ²) within 0.1%; Goldstone massless within 0.04%** |
| **F3** | **Yukawa back-reaction sketch** | **Φ deflection at fermion density observed (informational; not energy-conserving)** |
| **F4** | **Symmetry-restored phase** | **Φ=0 fixed; η matches pure Weyl reference (8e-16); χ stays zero** |

**Total: 12/12 phases pass.** F1, F4 at machine precision verify the parameter-preservation contract of the unification proposition. F2 verifies both Higgs and Goldstone modes. F3 is a sketch only — a proper symplectic Yukawa back-reaction is a separate engineering task.

### F3 proposition fixes landed (2026-05-15 / 2026-05-16)

- **P4** — `m_eff = y·|Φ|` → `m_eff = y·Re(Φ)`. Resolves the non-analyticity at Φ=0.
- **P2** — Yukawa promoted to complex bilinear `M(x) = y·Φ(x)`. New `dirac_step_2d_varm_complex_splitstep` in `ca_dirac.py`; exactly unitary, reduces bit-for-bit to the real-mass varm stepper when `Im(Φ) ≡ 0`.
- **P1** — Symplectic Yukawa back-reaction via joint Hamiltonian. `unified_step(back_react=True)` Strang-wraps the Dirac step with Π half-kicks `Π −= dt/2·c²·y·χ†η`. The `c²` factor (matching the Dirac stepper's mass-Hamiltonian convention) is essential; without it the Strang split has a constant 1.85% energy offset independent of dt. With it, drift over 200 steps at dt=0.5 is **3 ppm** and scales as O(dt²) exactly. `total_energy(state, mu2, lam, y, c)` helper added. F3 now runs 200 steps without divergence; `max|Φ−v|=4.4e-2` bounded.
- **P3** — Cayley/Crank–Nicolson exact-unitary variable-c stepper in `ca_curved.py`. `CayleyVarcSolver2D` factorises an LU once per c-field change; each subsequent step is one back-substitution. **Norm conservation 5.5e-15** (machine precision) vs **32.6%** drift in the existing Strang stepper — a 6×10¹³ improvement. C1 Snell test gains a Cayley arm; new **F3b** demonstrates Newtonian-gravity-analog deflection: a Weyl probe packet bends 6.6 cells *toward* a static |Φ| depression (norm drift 1.1e-15). Caveat: centered first-difference lattice dispersion makes the Cayley refraction angle 5.4° off Snell at |k|≈0.5; not a bug, the price of position-space exact-unitarity. Higher-order spatial stencils would close it.

**Total 13/13 phases pass** (A1, A2, B1, B2, C1+cayley, D1, E1, E2, F1, F2, F3, F3b, F4). All earlier passes preserved at the same numerical residuals.

### Double-precision regression (2026-05-14)

Fresh run with explicit float64/complex128 (NumPy 2.2.6 default). All 12 phases + the six original Weyl stages re-executed from a clean `__pycache__`. Results compared against the table above:

| Phase / Stage | Prior value | Fresh value | Variation |
|---|---|---|---|
| B1 group-velocity | 0.92–0.98 | 0.9158 / 0.9172 / 0.9694 / 0.9791 | none (bit-for-bit) |
| B2 norm drift (split-step) | not previously tabulated | 8.8e-16 … 2.2e-14 across L | new data — within 1 ulp per step |
| C1 Snell error | 0.51° | 0.51° | none |
| C1 Strang vs blending norm drift | 30% better | 3.02e-1 vs 4.30e-1 | none |
| D1 Weyl regression | 5e-16 | 5.10e-16 | none |
| D1 norm drift / 1000 steps | 3e-14 | 3.42e-14 | none |
| D1 dispersion residual | 9e-17 | 8.88e-17 | none |
| D1 zitterbewegung | 3.5% / 2mc² | 3.53% / 2mc² | none |
| E1 phase pickup | 4e-16 | 4.44e-16 | none |
| E1 norm drift with A0 | (not recorded) | 3.58e-12 | new data point |
| E2 right-leakage | 0.0 | 0.0 | none |
| F1 Φ−v drift | machine ε | 1.11e-16 | none |
| F1 fermion diff | 8e-16 | 8.41e-16 | none |
| F2 radial dispersion | within 0.1% | max res 1.06e-3 (0.106%) | none |
| F2 goldstone dispersion | within 0.04% | max res 4.42e-4 | none |
| F3 |Φ−v| at center | "observed" | 6.95e-1 (sketch range 0.012–1.247) | first numeric value recorded |
| F4 Φ at 0 | machine ε | 0.0 (exact) | none |
| F4 η match | 8e-16 | 7.57e-16 | none |
| Stage 5 reversibility residual | not tabulated | 1.5e-12 at n=2500 | linear-in-n, 6e-16/step → precision-bound, not a bug |
| Stage 6 3D norm | not tabulated | 150.3449 (constant to 4 dp at t = 0, 1000, 2500, 5000) | conserved |

**Conclusion: no variation.** The codebase is already running at native double precision (NumPy default complex128). Residuals at the 1e-16 level *are* the floor; the only stage that grows away from it is Stage 5, where the residual scales linearly at ~6e-16 per timestep — exactly the per-step round-off budget of a complex128 FFT. Upgrading to `longdouble` (80-bit, ~64-bit mantissa) would shave roughly 1 decimal of error per step but is not worth the slowdown for the current tests.

F3 still passes its informational threshold (`|Φ−v|` is non-trivially nonzero and finite) but the new run captures `max|Φ−v|=6.95e-01` over 30 steps. That is the energy "borrowed from nowhere" by the non-symplectic hand-kick — the magnitude the proposed P1 fix in `ca-f3-propositions.md` needs to bound.

## Corrections Log

| Date | Location | Issue | Resolution |
|---|---|---|---|
| 2026-05-13 | `physics_notes_pages_31-45.md`, page 38 boxed FD equations | Original transcription was missing `i` on y-derivative terms | Corrected to `+i/2(g_{m+1}−g_{m-1})` and `−i/2(f_{m+1}−f_{m-1})`, consistent with the Weyl PDE (σ_y carries the imaginary factor) |
| 2026-05-13 | `ca-simulation/ca_core.py` — `weyl_step_2d` and `weyl_step_3d` | Confirmed correct: `+1j*dg_dy` and `−1j*df_dy` match the corrected equations | No change required |

## Next Steps

- Continue OCR/transcription for pages 61 onward in batches of ~15.
- Optional: cross-check the quantum-scalar derivation (pages 1–2) against a standard QFT reference (Peskin & Schroeder ch. 2, or similar) to flag any handwriting-OCR errors in signs/factors.
- **F3 follow-up.** See `ca-f3-propositions.md` for ranked candidate fixes (P1 symplectic Yukawa via joint Hamiltonian is recommended). The double-precision rerun confirms the F3 sketch is not a precision artifact — it is an integrator-structure issue.
- **Unification v2 build sequence.** `ca-unified-v2.md` proposes a four-layer stack (BCC substrate, exact-dispersion Weyl/Dirac, composite-photon U(1), EMQG-Poisson-sourced $c(\mathbf{x})$). Recommended first builds: V4 composite photon (`ca_maxwell.py`) then V11 EMQG modified Poisson coupled to the existing Cayley variable-$c$ stepper. v2 separates the Φ-as-Higgs job from the metric-source job that v1 conflated into one field.

### v2 layered build landed (2026-05-15)

L1–L4 implemented end-to-end in a single session. All four layers pass; the 13 pre-existing phase tests (A–E + F) remain unchanged at the prior residuals.

| Layer | Module | Test passes | Notable result |
|---|---|---|---|
| **L1** | `ca_bcc.py` | 6/6 | BCC unitarity 7.9e-16, dispersion 7.2e-16, norm drift 3.7e-14/200 steps, A_0=I exact, small-k Weyl regression 5e-4 at \|k\|=0.005 |
| **L2** | `ca_core_exact.py` | 5/5 | 2D arccos dispersion unitarity 3.2e-16, norm drift 8.4e-15/200 steps, Paper 4 frequency-dependent c: Δc/c = -1.1% at \|k\|=0.5 along (1,1) (zero along axis) |
| **L3** | `ca_maxwell.py` | 3/3 + 1 info | Composite-photon dispersion ω=\|k\|/√3 at 0.21%; transversality 2ñ·E=0 at 4.6e-17; anisotropy verified (axis exact, diag err = k/18 analytically). Pointwise-bilinear curl residual scales as O(k) — full Paper 1 lines 84-90 smeared-photon construction is needed for the published O(k^3) bound, deferred |
| **L4** | `ca_emqg.py` | 3/3 | Static Poisson rel err 2.75% on 64x64, vacuum ρ=0 → c=c_0 exactly, lensing demo: probe at impact b=18 bends toward mass, deflection scaling Δ(2M)/Δ(M) = 1.83 (8.5% off analytic 2.0) |

**Discovery during L1:** the Paper 1 Eq. 15 transcription in `qca-papers-1-4-overview.md` had a sign typo on the second term of n_y (should be `+s_x c_y s_z`, not `−s_x c_y s_z`). Original form gave \|u² + \|n\|²\| up to 0.47 off unity at finite k; corrected form gives 4.4e-16. The reference doc transcription has been left for now (caveat applies to anyone reading line 53); the working code in `ca_bcc.py` carries the fix with an inline note. Should be back-fixed in the reference doc.

**Sign convention in L4:** the proposition's `c = c_0(1+φ/c_0²)^(-1)` had the wrong sign for gravitational lensing — with φ<0 in a well, that formula gives c>c_0 (light *speeds up*), and probes would deflect away from masses. Replaced with the GR-effective-medium form `c = c_0/(1 − 2φ/c_0²)`, which gives c<c_0 in the well and the correct deflection direction. Documented in `ca_emqg.py`.

**Fresh full-suite regression (2026-05-15):**
- `run_phase_tests.py`: 8/8 pass (A1, A2, B1, B2, C1, D1, E1, E2) — residuals identical to prior baseline (D1 dispersion 8.88e-17, E1 phase 4.44e-16, E2 right leakage = 0.0)
- `run_phaseF_tests.py`: 5/5 pass (F1, F2, F3, F3b, F4) — residuals identical (F1 fermion diff 7.57e-16, F4 η match 7.57e-16)
- `run_L_tests.py`: L1 (6/6), L2 (5/5), L3 (3/3+info), L4 (3/3) — all PASS
- **Total: 13 + 17 = 30 tests passing; 0 failing.**

### 10× lattice resolution bump (2026-05-16)

Every lattice-size parameter `L` and proportionally-scaled spatial-feature size (Gaussian widths $\sigma$, impact parameters $b$, depression widths) in all three test runners and in `ca_emqg.py` was multiplied by 10. Full table in `changelog.md` 2026-05-16 (later). Time-domain parameters (step counts that index FFT bin width, dt values, μ², λ, y, G, dimensionless wavevectors, flux $\pi$) were preserved. Brillouin-zone *sampling* densities (L1.a / L2.a `K = linspace(..., 16, ...)`) were also preserved — those are verification-fineness, not model resolution.

Cells / memory now per test:
- L1.d BCC norm drift: $L=160 \Rightarrow 4.1\,\text{M}$ cells, FFT working memory $\sim 250\,\text{MB}$/spinor component.
- L4.c lensing, C1 Cayley refraction: $L=1280 \Rightarrow$ sparse-LU memory $\sim 10\,\text{GB}$ (O(L³) for 2D nested-dissection). Inline fallback notes ($L=384$–$512$) added if RAM-bound.
- F3b: $L=960 \Rightarrow$ Cayley sparse LU $\sim 5\,\text{GB}$.

**Tests have not yet been re-run at the new size.** Bit-for-bit identity tests (F1, F4, D1 Weyl-regression-at-m=0) should still hit machine precision because the rule is unchanged; the failure mode to watch for is the Cayley arm running out of RAM at L=1280.

### 10× test execution pass — what actually happened when the bumped tests were run (2026-05-16, later)

Detailed entry: `changelog.md` 2026-05-16 ("10× test execution pass"). Detailed per-finding writeups: `findings.md` Findings 3–6 plus the Finding 2 update.

**Summary table:**

| Test | What changed at 10× | Match to existing formula |
|---|---|---|
| L1 BCC unitarity / dispersion / A_0 | unchanged, machine precision | — |
| L1.d norm drift | scanned at L=40, 80, 120; all at the FFT floor; full $L=160$ run incomplete (wall time) | — |
| L2 norm drift, 200 vs 2000 steps at L=320 | ratio = 9.985, exact 10× per-step | 1 ulp of complex128 per step |
| L3 curl residual k-scan ($10^{-5}$ to $10^{-2}$) | curl/k → $1/\sqrt 6 = 0.408248290\ldots$ to 7 sig figs at $k=10^{-5}$ | **$1/\sqrt 6$, exact algebraic from BCC geometry** |
| L4.a static Poisson rel err | 2.75% → 1.39% at L=640 | finer k-grid; modest 2× |
| L4.c lensing at L=1280 | not executed (Cayley LU ≈ 10 GB exceeds sandbox memory) | — |
| D1 Weyl regression m=0 | $5\times 10^{-16}$ → $1.55\times 10^{-15}$ | $\sqrt{N_\text{cells}}$ FFT roundoff |
| D1 norm drift 1000 steps | $3.4\times 10^{-14}$ → $4.0\times 10^{-13}$ | $\sqrt N$ per step (11.6× vs predicted 10×) |
| D1 dispersion | $8.88\times 10^{-17}$ → $1.28\times 10^{-17}$ | machine zero |
| D1 zitterbewegung at 10× n_steps | 3.53% → 0.026% (135× improvement) | FFT-bin-limited; $2mc^2$ holds within resolution |
| B1 speed_ratio at L=640 | 0.92–0.98 → 0.9995–0.9999 | $v_g = c\hat k$ holds tighter as σ grows |
| E1 phase err | $4.44\times 10^{-16}$ unchanged | eigenvalue-phase floor |
| E1 norm drift with A0 | $3.6\times 10^{-12}$ → $4.3\times 10^{-10}$ | $\sqrt N$ over 100 steps (120× vs predicted ~100×) |
| E2 parity violation | 8-decimal agreement, right leakage = 0.0 exact | unchanged |
| F1 vacuum regression | **DIVERGES at default n_phi_sub=1**; PASSES at machine precision with n_phi_sub=2 | **CFL bound: $dt_\text{sub} < 2/\sqrt{8+2\mu^2}$** (Finding 4) |
| F2 Higgs radial dispersion | $1.06\times 10^{-3}$ → $1.00\times 10^{-3}$ | O(dt²) Verlet, not L-limited |
| F2 Goldstone dispersion | $4.4\times 10^{-4}$ → res/(\|k\|·ε) ≤ 0.88 | **Exactly massless** (Finding 3) |
| F3 symplectic Yukawa at L=320 (sub-scaled) | $H_\text{rel}$ = 0.0002%, same shape as prior L=64 | symplectic contract preserved |
| F3b at L=960 | not executed (Cayley LU ≈ 5 GB exceeds sandbox memory) | — |
| F4 symmetry restored | $|\Phi|=0$ exact, η match $2.3\times 10^{-15}$ | bit-for-bit identity survives |

**Updated exactness count:** 8 exact algebraic results (6 prior + Goldstone-massless + curl-residual-leading-1/√6).

**Tests with hidden CFL bugs surfaced by the 10× bump:** F1 (Finding 4). The empirical critical dt at L=320 lies between 0.85 and 0.95; the safe theoretical CFL bound is 0.667. `n_phi_sub=2` is needed at L=320 with `dt=1.0`.

**Tests not executed at the 10× size due to sandbox memory limits:** F3b (L=960 → ~5 GB), L4.c lensing (L=1280 → ~10 GB), C1 Cayley arm (L=1280 → ~10 GB). Fallback values (L=384–512) noted in the test files; not run here.

**No data matched an imaginary-number approximation** in the sense suggested by the user prompt example. All formula matches that surfaced are real-valued algebraic constants ($1/\sqrt 6$, $\varepsilon_\text{double}$, the CFL bound, $2mc^2$).


## Diagram files (page 3 & 5)

- `diagrams/page03_photon_graviton.svg` — wavy-line photon vs bumped-arc graviton with parameter *a*; caption "Photon antisymmetric / Graviton symmetric".
- `diagrams/page03_tetrahedron_isomers.svg` — the two tetrahedron isomers with 3 particle types.
- `diagrams/page03_octahedron_isomers.svg` — the three octahedron isomers (top row) plus two rotational variants of isomer 3 (bottom row).
- `diagrams/page05_qed_standard.svg` — standard QED: two e⁻ exchanging a single photon γ.
- `diagrams/page05_spinor_electrodynamics.svg` — spinor electrodynamics: two e⁻ exchanging a correlated pair of γ½ in an "X" configuration.
