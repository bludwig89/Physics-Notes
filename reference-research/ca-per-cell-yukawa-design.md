# Per-Cell Yukawa Mechanism — V14 Design Outline

*Created 2026-05-22 - 14:40*

Companion to `ca-electroweak-design.md`, `ca-strong-design.md`, and `ca-unified-v2.md`. Scope: outline the architecture for turning the three first-generation Yukawa couplings $y_e, y_u, y_d$ from **static, hand-tuned scalars** into **per-cell, Φ-coupled, derivable** parameters, and survey the external literature that supplies candidate derivation mechanisms.

---

## 1. Current state of the model (what the outline must replace)

`ca_unified.py` already supports a per-cell Yukawa coupling for a single lepton flavour:
$$
m_e^{\text{eff}}(\mathbf{x}) = y_e \, \mathrm{Re}\,\Phi(\mathbf{x})
$$
via `dirac_step_2d_varm_complex_splitstep` (F3 propositions P1/P2/P4, landed 2026-05-15/16). The corresponding back-reaction is symplectic: $H_\text{rel} = 3.75\%$ over 200 steps, well within the 5% gate.

`ca_strong.py` (V13, landed 2026-05-21) carries the quark sector with **static** flavour-indexed masses: a Python dict `m_flavour = {'u': m_u, 'd': m_d, 's': m_s}` is passed to the Strang stepper and never updated. Per the V13 design doc (lines 60–62) and the `changelog.md` 2026-05-21 entry, this is explicit V14 deferred work.

**Identified gaps:**

1. Quark masses are flavour-static, not Φ-coupled.
2. The three first-generation Yukawa scalars $y_e, y_u, y_d$ are *input constants*, not derived from substrate dynamics. `ca-electroweak-design.md` §5 explicitly flags this as out of scope for v2.
3. No mechanism currently selects flavour: the three couplings could be set to any values, and nothing in the lattice rules picks "the physical ones."
4. No generation count is predicted — the number "3" is also an input.

---

## 2. What the literature offers

The web search surfaced six approach families that could supply a derivation mechanism. Ordered by how cleanly each maps onto the lattice substrate already in `ca-simulation/`:

### 2.1 Bisio-D'Ariano QCA mass-as-coupling (Paper 1 family)

The discrete dispersion $\omega_k = \arccos(\sqrt{1-m^2}\,c_x c_y)$ that we already use forces $n^2 + m^2 = 1$ by unitarity (Finding 9). The mass $m$ is therefore a single dimensionless number in $[0, 1]$ per spinor mode, bounded — not free.

**[Doubly-Special Relativity from QCA](https://www.researchgate.net/publication/258052347_Doubly-Special_Relativity_from_Quantum_Cellular_Automata)** observes that in the 3D Dirac QCA, *a change of rest mass is required to represent boosts* — mass enters the boost-covariance condition. This is the strongest hint in the QCA literature that mass is not a free Lagrangian parameter but a covariance-fixed observable.

**Direct implication for our model:** every $y$ in $\{y_e, y_u, y_d\}$ must produce $m \in [0, 1]$ in lattice units, i.e. $y \cdot v \le 1$ where $v$ is the Higgs VEV in lattice units. This is a hard upper bound the current implementation does not enforce.

**[Quantum field as a QCA: Dirac free evolution](https://www.osti.gov/biblio/22447603)** and **[Path-integral solution of the Dirac QCA](https://arxiv.org/pdf/1406.1021)** give the analytic mass-dependence (Jacobi polynomials) of the QCA propagator that could be inverted to read out $m$ from group-velocity measurements — a self-consistency check against the input $y$.

### 2.2 Koide / Zero-Interaction-Principle (ZIP) derivations

**[Derivation of the Koide Formula from the Zero-Interaction Principle](https://www.academia.edu/145613039/Derivation_of_the_Koide_Formula_from_the_Zero_Interaction_Principle)** claims a derivation of the charged-lepton Koide phase $\delta = 2/9$ from topological moments of a pure-potential state in 3D configuration space (agreement to better than 0.01%). The companion **[E₈ Symmetry and Spectral Geometry preprint (Nov 2025)](https://www.preprints.org/manuscript/202511.0938)** derives charged-lepton masses and Koide's relation from eigenmodes of a Laplace–Beltrami operator on a compactified internal manifold — "hierarchical mass scales without fitted Yukawa parameters."

**Direct implication:** if our BCC lattice supplies the discrete analogue of a Laplace–Beltrami spectrum (it does — the BCC dispersion $\omega(\mathbf{k})$ is exactly that), then the spectrum of bound modes of a per-cell *bound-state operator* could in principle yield $m_e$ as an eigenvalue, not a parameter. The Koide relation $K = (m_e + m_\mu + m_\tau)/(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau})^2 = 2/3$ then becomes a *prediction-target* that our spectrum must reproduce.

**[Extended Koide for quarks](https://www.sciencedirect.com/science/article/pii/S0550321321002431)** ($K_q = 2/3$ for running masses) gives the same target for $y_u, y_d$.

### 2.3 Asymptotic-safety fixed-point Yukawa

**[Asymptotic safety scenario for gauged chiral Higgs-Yukawa](https://link.springer.com/article/10.1140/epjc/s10052-013-2652-y)** and **[Asymptotic safety, the Higgs boson mass, and BSM](https://link.aps.org/pdf/10.1103/PhysRevD.100.115001)** locate an RG fixed point where the Yukawa coupling is *not* a free input — sufficiently large initial values flow to the same IR value (the Pendleton–Ross/Hill fixed point). The top quark sits nearly exactly on this fixed point ($y_t \approx 1$).

**Direct implication:** for the *top* this is the cleanest derivation in the literature; for first-generation $y_e, y_u, y_d \sim 10^{-6}\,\text{–}\,10^{-5}$ the fixed point is *unstable* (small-coupling IR free), so asymptotic safety does *not* fix first-gen Yukawas directly. It would have to be combined with one of the other mechanisms below.

### 2.4 Froggatt-Nielsen / chain-locality

**[Unified Flavor: Lattice Quantization, Chain Locality, and Dynamical Origin of Hierarchical Yukawas](https://arxiv.org/html/2603.11341)** (2026) and **[Flavor in Ninths and a Discrete Gauge Origin](https://arxiv.org/html/2603.03631)** (2026) build the hierarchy from *nearest-neighbour couplings on a theory-space chain*: a flavon vacuum expectation value $\langle\phi\rangle/\Lambda \equiv \lambda$ raised to integer powers fixed by charges. Hierarchies organised in units of $1/9$ match the observed pattern.

**Direct implication for our lattice:** This is the most architecturally compatible mechanism with our setup. "Theory-space chain" = a discrete index on the lattice; "messenger fields" = additional spinor fields at heavy mass; the lattice already supports as many flavour copies as we want via `m_flavour`. The hierarchy
$$
y_e : y_u : y_d \sim \lambda^{n_e} : \lambda^{n_u} : \lambda^{n_d}
$$
with $n_i$ fixed by U(1)_FN charges — a small, finite-integer derivation rather than three independent fits.

**[Modular Origin of Mass Hierarchy](https://arxiv.org/pdf/2105.06237)** and **[Froggatt-Nielsen-like mechanism with modular symmetry](https://arxiv.org/html/2508.13578v1)** (2025) show the same hierarchy can come from modular symmetry of a complex modulus $\tau$ — appealing because the BCC lattice has a natural complex-modulus parametrisation.

### 2.5 Topological-defect generation count

**[Three fermionic generations on a topological defect in extra dimensions](https://arxiv.org/pdf/hep-ph/0011095)** derives the count "3" from the winding/index of a defect in extra dimensions. **[Topological Aspects of Dirac Fermions in a Kagomé Lattice (Dec 2024)](https://arxiv.org/abs/2412.04010)** shows Dirac fermions acquire mass from *simultaneous charge and bond orderings* with topological winding-number labels.

**Direct implication:** if our model is to *predict* "3 generations" instead of "1 generation triplicated to 3" (which is what V13's flavour dict does), the count needs a topological invariant of the BCC lattice. The BCC has a natural defect spectrum (vortex/skyrmion configurations of $\Phi$); the question is whether the count of stable defects in the (3+1)-D effective theory is 3.

### 2.6 Discrete-spacetime Dirac vacuum and self-consistent bound states

**[The Dirac Vacuum in Discrete Spacetime (Gupta & Short, 2024)](https://arxiv.org/pdf/2412.03466)** constructs the filled negative-energy sea on a lattice and identifies the mass eigenvalues as discrete eigenvalues in the gap. **[Resolving the spurious-state problem in Dirac equation by using the staggered-grid method (2025)](https://arxiv.org/pdf/2510.19201)** removes the lattice-doubling artifacts that would otherwise inflate the count of light modes.

**Direct implication:** before we can read off $m_e$ as a bound-state eigenvalue, we must first verify the discrete Dirac vacuum on the BCC. This is largely diagnostic infrastructure (a V14 prerequisite test, not a V14 deliverable in itself).

### 2.7 't Hooft equivalence-class collapse (CAI)

`reference-research/t-hooft-2015-cai-summary.md` already covers this. The relevant claim: in CAI Ch. 7, an *info-equivalence class* of CA states becomes a single ontological basis element, and the *coarse-grained* unitary evolution on those classes acquires effective parameters not present in the original CA rule. Mass would then be an effective parameter of the coarse-grained quantum theory — derived from the equivalence-class structure, not the original rule.

**Direct implication:** the heaviest piece of architecture but the cleanest in principle: if we can construct the equivalence classes for the BCC rule (we cannot today), the Yukawa couplings emerge from class membership, not from any input.

---

## 3. Proposed V14 architecture (per-cell Yukawa)

### 3.1 Code-level changes (uncontroversial, finite scope)

Two changes are wholly mechanical and unblock everything else. They are V14a:

**V14a.1 — Per-cell flavour-indexed Yukawa in `ca_strong.py`.**
Replace the static `m_flavour: dict[str, float]` with a per-flavour Yukawa-coupling dict `y_flavour: dict[str, float]`, and in the stepper compute
$$
m_f^{\text{eff}}(\mathbf{x}) = y_f \, \mathrm{Re}\,\Phi(\mathbf{x}), \quad f\in\{u, d, s\}
$$
exactly mirroring the existing `dirac_step_2d_varm_complex_splitstep` path in `ca_dirac.py`. Cold-link bit-for-bit regression (V13a) must still pass — i.e. when $\Phi \equiv v$ and the y-dict is set to `{f: m_f / v for f, m_f in m_flavour.items()}`, the new code must equal V13's output.

**V14a.2 — Bound-mass test.**
For each flavour, add a test that propagates a Gaussian wavepacket, measures the group velocity, inverts the dispersion $\omega_k = \arccos(\sqrt{1-m^2} c_x c_y)$ to read out $m$, and checks $m = y_f \cdot v$ to FFT precision. This is the analogue of the existing zitterbewegung test (D1) for every flavour. *Gate:* relative error $\le 10^{-12}$.

**V14a.3 — $y_f \cdot v \le 1$ enforcement.**
Add an `assert` in `ca_strong.py`'s stepper and `ca_unified.py` that raises if $y_f \cdot v_\Phi > 1 - \epsilon$. This is the QCA unitarity bound from Bisio et al. — silently going over it would break $n^2 + m^2 = 1$.

V14a is a 1–2 day implementation and gives us the per-cell Yukawa infrastructure without yet *deriving* anything.

### 3.2 Derivation pathway A — Chain locality (most lattice-compatible)

After V14a, the cleanest path to a *derived* $\{y_e, y_u, y_d\}$ is:

**V14b — Add an extra lattice dimension as a flavon chain.**

Augment `ca_strong.py` with one extra discrete index $n \in \{0, 1, \dots, N-1\}$ per cell, and a flavon $\phi_n$ that couples adjacent sites along this chain with strength $\lambda$. The four-fermion vertex
$$
\mathcal{O}_n = \bar\psi_L \phi_n \psi_R / \Lambda
$$
gives an effective Yukawa $y \sim \lambda^n$ where $n$ is the chain-distance the Standard-Model fermion sits from the "heavy end." First-gen lives at large $n$ (small Yukawa), third-gen at $n=0$ (Yukawa near unity).

*Gates:*
- Hierarchy $y_e / y_\mu / y_\tau$ matches Standard Model to within the published Froggatt-Nielsen accuracy ($\sim 30\%$).
- $K_\ell = (m_e + m_\mu + m_\tau)/(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau})^2$ within 1% of $2/3$ — direct Koide test.
- $K_q$ within 5% of $2/3$ for running quark masses — Koide-extended test.

This pathway adds infrastructure (the chain dimension) but does not require any new physics beyond what's published in 2025–2026 arXiv preprints.

### 3.3 Derivation pathway B — Spectral / Laplace-Beltrami (BCC-native)

The BCC dispersion is already a discrete Laplace–Beltrami spectrum. Following **[E₈ Symmetry and Spectral Geometry](https://www.preprints.org/manuscript/202511.0938)**:

**V14c — Compactify an internal direction; identify mass eigenmodes.**

Wrap the BCC lattice on an additional small dimension $L_{\text{int}}$ ($\ll L_{\text{spatial}}$) with periodic boundary conditions. The eigenvalues of the BCC Dirac operator across this dimension form a discrete tower. Exponential suppression $m_n \sim m_0 e^{-c n}$ from the internal curvature reproduces the observed hierarchy.

*Gates:*
- Three lightest eigenmodes per charge sector with mass ratios matching SM first–third generation.
- No additional parameters beyond $L_{\text{int}}$ and one internal-curvature scale.
- Compatible with the existing 13/13 phase tests at $L_{\text{int}} \to \infty$.

This pathway is more architecturally invasive than 3.2 but has the strongest "derivation, not import" character — Yukawas come out as eigenvalues.

### 3.4 Derivation pathway C — Topological defect count

Following **[Three fermionic generations on a topological defect](https://arxiv.org/pdf/hep-ph/0011095)**:

**V14d — Count stable Φ-defects on BCC.**

The Mexican-hat Φ admits vortex configurations on the BCC. Count the stable topological sectors; identify each sector with one generation. *This is the path that would predict the number "3" rather than impose it.*

*Gates:*
- Defect count = 3 (currently unknown for BCC + complex Φ).
- Defect-localised Dirac zero-modes exist and their masses match the Yukawa hierarchy.

Highest risk, highest payoff. Should only be attempted after 3.2 or 3.3 supplies a baseline hierarchy to compare against.

### 3.5 Out of V14 scope (named here so we don't keep tripping over them)

- Asymptotic-safety RG flow (§2.3) — needs continuous RG running, doesn't map naturally to our discrete stepper.
- 't Hooft equivalence-class collapse (§2.7) — requires constructing the BCC info-equivalence classes, which is open even for the simplest 1D CA examples.
- Self-consistent Dirac vacuum (§2.6) — needed as a *diagnostic* (V14e: verify no spurious doublers on BCC), but the published staggered-grid fix can be lifted as-is.

---

## 4. Suggested test order

| Step | Test | Gate | New code |
|---|---|---|---|
| V14a.1 | Per-cell Φ-coupled $m_f^{\text{eff}}$ in `ca_strong.py` | Cold-link bit-for-bit regression vs V13a | `ca_strong.py::step_strong_2d` |
| V14a.2 | Bound-mass readout from group velocity, per flavour | $|m_{\text{measured}} - y_f \cdot v| / m \le 10^{-12}$ | `model-tests/test_V14a_per_cell_yukawa.py` |
| V14a.3 | $y_f \cdot v \le 1$ bound | Assert at construction | inline |
| V14b.1 | Chain-locality flavon (Pathway A, §3.2) | Lepton + quark Koide $K = 2/3 \pm 1\%$ / $5\%$ | `ca_simulation/ca_flavon_chain.py` (new) |
| V14b.2 | Hierarchy fit | $y_e/y_\mu, y_e/y_\tau$ within 30% of SM | extension of V14b.1 |
| V14c | Spectral Kaluza–Klein tower (Pathway B, §3.3) | Mass ratio $m_1:m_2:m_3$ matches SM ± 10% | `ca_simulation/ca_internal_dim.py` (new) |
| V14d | Topological defect count (Pathway C, §3.4) | Defect count = 3, zero-modes hierarchical | `ca_simulation/ca_defects.py` (new) |
| V14e | No-doubler diagnostic | Staggered-grid eigenvalue spectrum has no extra light modes | `model-tests/test_V14e_doublers.py` |

V14a is the unconditional prerequisite. V14b, V14c, V14d are alternative derivation pathways; the recommendation is to attempt them in that order (cheapest first).

---

## 5. Honest caveats

1. **No single paper found in the search supplies a complete derivation of $\{y_e, y_u, y_d\}$ from a lattice CA substrate.** Every candidate mechanism above derives *some* of the three but imports the rest. Chain locality and modular-symmetry FN are the closest to first-principles, but both require extra theory-space structure not yet present in `ca-simulation/`.
2. **The Koide relation $K = 2/3$ is an empirical regularity, not a derivation.** Using it as a gate (§3.2, §3.3) is testing whether our mechanism reproduces a known curiosity, not whether the mechanism is right.
3. **Generation count is the hardest problem.** Pathway C (§3.4) is the only one in the literature that *predicts* "3" rather than assumes it; it is also the highest-risk.
4. **The V14a infrastructure work is unblocked and worth doing regardless of which derivation pathway we eventually back.** It also closes the V13 changelog item and the `next-steps.md` line-3 quark-Yukawa item.

---

## 6. Cross-references

- `ca-electroweak-design.md` §4–5 (the existing three mass paths and the explicit exclusion of fermion-mass derivation from v2).
- `ca-strong-design.md` §3.1 and `ca_strong.py::step_strong_2d` (the current static `m_flavour` to be replaced).
- `ca_unified.py::dirac_step_2d_varm_complex_splitstep` (the lepton Φ-coupled stepper to be mirrored for quarks).
- `findings.md` Finding 9 (the $n^2+m^2=1$ unitarity bound that constrains $y_f \cdot v$).
- `qca-papers-1-4-overview.md` Paper 1 Eq. 23 (the QCA mass-coupling form).
- `t-hooft-2015-cai-summary.md` Ch. 7 (equivalence-class derivation pathway, deferred).

## 7. External references (web search 2026-05-22)

- [Quantum field as a quantum cellular automaton: The Dirac free evolution](https://www.osti.gov/biblio/22447603) — Bisio, D'Ariano, Tosini.
- [Doubly-Special Relativity from Quantum Cellular Automata](https://www.researchgate.net/publication/258052347_Doubly-Special_Relativity_from_Quantum_Cellular_Automata) — boost-induced rest-mass shift.
- [Path-integral solution of the one-dimensional Dirac QCA](https://arxiv.org/pdf/1406.1021) — analytic mass-dependence.
- [Weyl, Dirac and Maxwell Quantum Cellular Automata](https://ar5iv.labs.arxiv.org/html/1601.04842) — composite-photon phenomenology.
- [Derivation of the Koide Formula from the Zero-Interaction Principle](https://www.academia.edu/145613039/Derivation_of_the_Koide_Formula_from_the_Zero_Interaction_Principle) — δ=2/9 topological origin.
- [E₈ Symmetry and Spectral Geometry in Quantized Spacetime](https://www.preprints.org/manuscript/202511.0938) — Laplace–Beltrami eigenmode derivation of fermion masses (Nov 2025).
- [A modified Koide formula from flavor nonets](https://www.sciencedirect.com/science/article/pii/S0550321321002431) — Koide-extended quark relation.
- [Asymptotic safety scenario for gauged chiral Higgs–Yukawa models](https://link.springer.com/article/10.1140/epjc/s10052-013-2652-y) — Pendleton–Ross fixed point.
- [Asymptotic safety, the Higgs boson mass, and BSM physics](https://link.aps.org/pdf/10.1103/PhysRevD.100.115001) — fixed-point prediction analysis.
- [Unified Flavor: Lattice Quantization, Chain Locality, and Dynamical Origin of Hierarchical Yukawas](https://arxiv.org/html/2603.11341) — chain-locality FN.
- [Flavor in Ninths and a Discrete Gauge Origin of the QCD Axion](https://arxiv.org/html/2603.03631) — FN exponents in 1/9 units.
- [Modular Origin of Mass Hierarchy: Froggatt-Nielsen like Mechanism](https://arxiv.org/pdf/2105.06237) — modular-symmetry FN.
- [Three fermionic generations on a topological defect in extra dimensions](https://arxiv.org/pdf/hep-ph/0011095) — generation count from winding.
- [Topological Aspects of Dirac Fermions in a Kagomé Lattice](https://arxiv.org/abs/2412.04010) — winding-number mass on lattice (Dec 2024).
- [The Dirac Vacuum in Discrete Spacetime](https://arxiv.org/pdf/2412.03466) — Gupta & Short, 2024.
- [Resolving the spurious-state problem in Dirac equation by using the staggered-grid method](https://arxiv.org/pdf/2510.19201) — no-doubler diagnostic (2025).
- [The Cellular Automaton Interpretation of Quantum Mechanics](https://arxiv.org/pdf/1405.1548) — 't Hooft, equivalence-class derivation pathway.
