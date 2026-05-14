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
- `ca-simulation/ca_core.py` — Core numerics: explicit-Euler steppers (`weyl_step_2d`, `weyl_step_3d`) and exact split-step propagators (`weyl_step_2d_splitstep`, `weyl_step_3d_splitstep`), plus scalar wave CA, CFL sweep, norm tracking, and reversibility test.
- `ca-simulation/run_simulation.py` — Five-stage runner. Currently set to 200 steps, using split-step propagator throughout.
- `ca-simulation/figures/` — Output figures: scalar instability, spinor density snapshots (3 helicities), norm conservation, CFL sweep, graph topology, and reversibility chart.

## Corrections Log

| Date | Location | Issue | Resolution |
|---|---|---|---|
| 2026-05-13 | `physics_notes_pages_31-45.md`, page 38 boxed FD equations | Original transcription was missing `i` on y-derivative terms | Corrected to `+i/2(g_{m+1}−g_{m-1})` and `−i/2(f_{m+1}−f_{m-1})`, consistent with the Weyl PDE (σ_y carries the imaginary factor) |
| 2026-05-13 | `ca-simulation/ca_core.py` — `weyl_step_2d` and `weyl_step_3d` | Confirmed correct: `+1j*dg_dy` and `−1j*df_dy` match the corrected equations | No change required |

## Next Steps

- Continue OCR/transcription for pages 61 onward in batches of ~15.
- Optional: cross-check the quantum-scalar derivation (pages 1–2) against a standard QFT reference (Peskin & Schroeder ch. 2, or similar) to flag any handwriting-OCR errors in signs/factors.

## Diagram files (page 3 & 5)

- `diagrams/page03_photon_graviton.svg` — wavy-line photon vs bumped-arc graviton with parameter *a*; caption "Photon antisymmetric / Graviton symmetric".
- `diagrams/page03_tetrahedron_isomers.svg` — the two tetrahedron isomers with 3 particle types.
- `diagrams/page03_octahedron_isomers.svg` — the three octahedron isomers (top row) plus two rotational variants of isomer 3 (bottom row).
- `diagrams/page05_qed_standard.svg` — standard QED: two e⁻ exchanging a single photon γ.
- `diagrams/page05_spinor_electrodynamics.svg` — spinor electrodynamics: two e⁻ exchanging a correlated pair of γ½ in an "X" configuration.
