# A Unified Proposition v2: Combining the Phase-F Architecture with the QCA Literature

*Speculative. Builds on `ca-unified-proposition.md` (v1), `ca-f3-propositions.md`, and the literature synthesis in `qca-papers-1-4-overview.md`. All 13/13 phase tests must remain passing in the appropriate regression limits.*

*Drafted 2026-05-15.*

---

## What v2 changes about v1

v1 proposed that **one** scalar field $\Phi$ does two jobs: Yukawa mass for fermions, and metric backreaction (variable-$c$) for gravity. That conflated two empirically distinct couplings into one field for architectural minimalism. v2 keeps the per-cell phase architecture and the Strang composition that make v1 work, but it **borrows three concrete structures from the published QCA literature** to fix specific gaps:

1. **BCC lattice + exact dispersion** (Papers 1, 2, 4) — replaces the simple-cubic 3D substrate.
2. **Composite-photon construction** (Paper 1, Eq. 35) — replaces the externally-imposed U(1) gauge phase as the canonical Maxwell sector.
3. **EMQG modified-Poisson sourcing of $c(\mathbf{x})$** (Paper 6, Eq. 19.7) — replaces the ad-hoc $c(\mathbf{x}) = c_0(|\Phi|/v)^{-\alpha}$ in v1 line 69 with a derived field equation.

The change to (3) is the most important. It separates two jobs that v1 asked $\Phi$ to do at once: $\Phi$ now sources fermion mass via Yukawa only. A *second* scalar — the EMQG vacuum potential $\phi$ — sources $c(\mathbf{x})$ via a modified Poisson equation whose right-hand side is the total local energy density (including the Φ stress-energy and the fermion energy). The two are linked through the matter source but they are not the same field.

---

## The four-layer stack

| Layer | Role | Primary source | File / status |
|---|---|---|---|
| **L1 — Substrate** | Lattice + exact QCA dispersion | Papers 1, 2 (BCC, $\arccos$) | New `ca_bcc.py`; replaces simple-cubic in 3D. 2D square unchanged. |
| **L2 — Free fields** | Weyl & Dirac propagators with exact dispersion | v1 architecture + Papers 1, 4 (exact $\omega_{\mathbf{k}}$) | Promote `ca_core.py` / `ca_dirac.py` to support exact-arccos as an option alongside the linearized FFT propagator |
| **L3 — Gauge & matter** | U(1) as composite photon; SU(2); Higgs $\Phi$ | Paper 1 Eq. 35 (composite γ) + v1 (Φ via Yukawa) + existing `ca_weak.py` | New `ca_maxwell.py`; existing `ca_higgs.py`, `ca_weak.py`, `ca_unified.py` retained |
| **L4 — Macroscopic geometry** | $c(\mathbf{x})$ derived from a vacuum potential $\phi$ sourced by total $T_{00}$ | Paper 6 Eq. 19.7 (EMQG modified Poisson) | New Poisson solver feeding `ca_curved.py` (Cayley variant). Replaces the v1 line-69 ansatz. |

The bridge that holds it together: **matter $\to \phi$ $\to c(\mathbf{x})$ $\to$ matter.** Φ stress-energy and fermion stress-energy together source the EMQG potential $\phi$ via the modified Poisson equation. The gradient of $\phi$ sets the local refractive index, encoded as $c(\mathbf{x})$ in the Cayley variable-$c$ stepper. Matter then propagates through that $c(\mathbf{x})$ field. This is the discrete analog of Wheeler's "matter tells space how to curve; space tells matter how to move," routed through the EMQG vacuum-scattering mechanism rather than through tetrad / spin-connection variables.

---

## Concrete substitutions for v1

### S1 — Replace the variable-$c$ ansatz (v1 line 69) with a sourced field equation

**v1 had:**

$$c(\mathbf{x}, t) = c_0 \cdot \left(\frac{|\Phi(\mathbf{x}, t)|}{v}\right)^{-\alpha}$$

**v2 substitutes:**

$$\nabla^2 \phi(\mathbf{x}, t) - \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2} = 4\pi G \, \rho_{\text{tot}}(\mathbf{x}, t), \tag{Paper 6, Eq. 19.7}$$

with $\rho_{\text{tot}} = \rho_{\Phi} + \rho_{\Psi}$ — the sum of the Φ stress-energy $T_{00}^\Phi = \tfrac{1}{2}|\Pi|^2 + \tfrac{1}{2}|\nabla\Phi|^2 + V(|\Phi|)$ and the Dirac stress-energy $T_{00}^\Psi = c \cdot \Psi^\dagger(\boldsymbol\alpha\cdot\hat{\mathbf{k}})\Psi + m_{\text{eff}}c^2\Psi^\dagger\beta\Psi$. Then

$$c(\mathbf{x}, t) = \frac{c_0}{1 - 2\phi(\mathbf{x}, t)/c_0^2}, \tag{GR-Shapiro reduction}$$

in the weak-field limit. For $\phi<0$ inside a gravitational well this gives $c(\mathbf{x}) < c_0$ — light *slows down* near a mass, which is the sign required for ray attraction and matches the GR Shapiro-delay expression. At $|\phi|\ll c_0^2$ this expands to $c \approx c_0\,(1 + 2\phi/c_0^2)$, reproducing the standard $4GM/(bc^2)$ deflection. In the vacuum limit ($\rho_{\text{tot}} = 0$), $\phi$ relaxes to zero and $c = c_0$ — the v1 vacuum contract is preserved.

> **Back-fix (2026-05-16):** This box previously published $c = c_0(1+\phi/c_0^2)^{-1}$ "Paper 6, Eq. 18.31 reduction." That form has the wrong sign for $\phi<0$ in a gravitational well (it gives $c>c_0$, i.e. light speeds up near a mass), and the Paper-6 citation was wrong on top of that — Eq. 18.31 is the Fizeau additive-velocity expression for a *moving* refractive medium, not the static gravity case (the static case is closer to Eqs. 18.51–18.52, $c(t) = c_0(1 \pm gt/c_0)$). The working implementation in `ca_emqg.py::c_field_from_phi` already used the GR-Shapiro form above; this document is being brought into line with it.  See `model-observations.md` item 1 and `changelog.md` 2026-05-15.

This is a strict improvement over v1 because:

- The exponent $\alpha$ (a free parameter in v1) is replaced by the Newton constant $G$, which has a *measured* value.
- The Φ-only sourcing in v1 missed the fermion stress-energy entirely; in F3 the deflection of a probe packet by a fermion density spike could only be observed *through Φ* shifting first. In v2 the fermion density couples directly to $\phi$, and $\phi$ couples directly to $c$.
- The v1 sign was inconsistent with the F3b lensing demo (per `changelog.md` 2026-05-16, the published exponent $(-\alpha)$ had to be flipped to $(+\alpha)$ to produce attraction). The EMQG sign is unambiguous and matches the lensing direction.

### S2 — Replace the simple-cubic 3D lattice with BCC

**v1 inherits:** `ca_core.py`'s 3D simple-cubic 6-neighbor Laplacian, which admits only the trivial $s=2$ automaton (per Paper 1 / Paper 2).

**v2 substitutes:** the BCC 8-neighbor lattice (tetrahedron + dual tetrahedron) with transition matrices $A_h$ satisfying Paper 1 Eq. 6 unitarity and Paper 2's Gram-matrix constraints. Dispersion:

$$\omega^{\pm}_{\mathbf{k}} = \arccos(c_x c_y c_z \pm s_x s_y s_z), \quad c_i = \cos(k_i/\sqrt 3),\ s_i = \sin(k_i/\sqrt 3). \tag{Paper 1, Eq. 15}$$

The 2D square lattice is unchanged — Papers 1 and 2 confirm it is the unique 2D substrate. Linearization at $|\mathbf{k}| \ll 1$ recovers the v1 split-step propagator, so all 2D tests (Phases A1, A2, B1, B2, C1, D1, E1, E2, F1–F4, F3b) are unaffected. The 3D Phase B/C/D regression must be re-run against the BCC dispersion. *V6 test in the literature reference becomes the gate.*

### S3 — Promote U(1) from external phase to composite-photon construction

**v1 has:** an external classical $A_\mu$ field producing a per-cell phase $\exp(-iqA_0\Delta t)$ on the Dirac spinor (Phase E1, Aharonov–Bohm at $4 \times 10^{-16}$).

**v2 adds:** Paper 1's composite-photon construction. Take two correlated Weyl fields $\psi, \varphi$; build the bilinears

$$G^i(\mathbf{k}, t) = \varphi^T(\mathbf{k}/2, t)\,\sigma^i\,\psi(\mathbf{k}/2, t)$$

and define $\mathbf{E}_G := |\mathbf{n}_{\mathbf{k}/2}|(\mathbf{G}_T + \mathbf{G}_T^\dagger)$, $\mathbf{B}_G := i|\mathbf{n}_{\mathbf{k}/2}|(\mathbf{G}_T^\dagger - \mathbf{G}_T)$. These obey the free Maxwell curl equations in the small-$\mathbf{k}$ limit (Paper 1, Eq. 35). New module `ca_maxwell.py`. The external classical $A_\mu$ phase is retained as a fast approximation, but the composite construction becomes the canonical reference for any test involving photon dynamics — including the Fizeau-scattering predictions of Paper 6 that L4 ultimately rests on.

This is the **single largest architectural gap** in v1: it has no genuine photon dynamics on the lattice. Without composite photons, Paper 6's gravity-as-photon-scattering picture cannot be tested directly; only the macroscopic refractive-index proxy in `ca_curved.py` can be checked.

### S4 — Preserve Yukawa from v1, retire the v1 metric coupling of Φ

The Yukawa coupling $m_{\text{eff}}(\mathbf{x}) = y\,\text{Re}(\Phi)$ from v1 (with the P2/P4 corrections in `ca-f3-propositions.md`) is *kept unchanged*. Φ remains the Higgs sector. What is **removed** from v1 is the second coupling — the direct functional dependence of $c$ on $|\Phi|$. In v2, $c$ depends on the EMQG vacuum potential $\phi$, and $\phi$ depends on the total stress-energy (of which Φ is one contribution, not the only one).

This preserves F1, F2, F4 unchanged. F3 and F3b get rewritten against the new $c(\phi)$ law.

### S5 — Adopt deformed-Lorentz (DSR) boost for tests beyond the small-$\mathbf{k}$ limit

Paper 4 Eq. 25: $L^D_\beta = \mathcal{D}^{-1}\circ L_\beta\circ \mathcal{D}$ with non-linear deformation map $\mathcal{D}$ on wave-vector space. Adopted as the test-time boost when verifying covariance against exact lattice dispersion. Does not change any propagator code; it changes only how we transform between frames in regression tests (V8 in the literature reference).

---

## What v2 preserves (the parameter-preservation contract, extended)

v1 required reduction to its implementation in the $\Phi = v$ limit. v2 inherits this and adds three more limits:

| Limit | Reduces v2 to | Gate test |
|---|---|---|
| $\Phi = v$ everywhere | v1 vacuum regression | F1 |
| $\rho_{\text{tot}} = 0$ in L4 | $\phi = 0$, $c = c_0$ constant; flat-space Weyl | B1, C1 (flat arm) |
| $|\mathbf{k}| \to 0$ in L1 | Linearized FFT propagator (current `ca_core.py`) | B1, B2 |
| Composite photon coherence enforced by hand | External classical $A_\mu$ (current Phase E1) | E1 |

So every existing passing test (8 Phase A–E + 5 Phase F) remains the gate for a specific limit of v2. *Nothing is broken by adopting v2; new tests are gained.*

---

## What is genuinely new in v2

- **Dynamical Newtonian-and-better gravity.** Solving the EMQG modified Poisson on the lattice and feeding $\nabla\phi$ into the Cayley variable-$c$ stepper gives a quantitative gravitational deflection (V11 test target: $\Delta\theta \approx 2GM/(bc^2)$ at leading order; possibly $4GM/(bc^2)$ if photon trajectories pick up the GR factor of 2, per Paper 6's claim).
- **Frequency-dependent $c$ at the lattice scale.** The BCC dispersion in L1 gives $|\Delta c/c| \sim k/\sqrt 3$ at Planck-scale wavevectors (Paper 4, Eq. 23). Distinct from the macroscopic position-dependent $c(\mathbf{x})$ of L4. Both kinds of variable-$c$ coexist.
- **Composite photon polarization deviation.** Paper 4 predicts the photon polarization plane is offset from $\hat{\mathbf{k}}$ by $\sim 10^{-15}$ rad at gamma-ray wavelengths. Below current detection, but a non-trivial lattice prediction once L3 is in.
- **Gravitational redshift as variable-$c$ scattering.** V12 in the literature reference. A linear $c(z)$ profile (set up via a uniform-$\rho$ source in the Poisson solver) should produce $\Delta\nu/\nu \approx -|\nabla c|\,L/c$ at the receiver. Both Paper 6's prediction and the leading-order GR result.
- **Higgs sector unchanged.** F2, F4 keep their existing meaning: $\delta\Phi$ propagates at $m_h = \sqrt 2 \mu$ and the symmetry-restored phase makes fermions massless. v1's Higgs claims are preserved verbatim.

---

## Build sequence

Recommended order (each step is a tested regression that gates the next):

1. **V4 — Composite photon (Paper 1 Eq. 35).** Highest leverage. Two correlated Weyl fields → bilinear $G^i$ → measured $\mathbf{E}_G, \mathbf{B}_G$ obey Maxwell at small $\mathbf{k}$. New `ca_maxwell.py`. Estimate: 4–6 days. Pass criterion: violation of curl equations $\mathcal{O}(k^3)$.

2. **V11 — EMQG modified Poisson + Cayley $c(\phi)$.** Solve $\nabla^2\phi - c_0^{-2}\partial_t^2\phi = 4\pi G\rho$ on the lattice with a static spherical $\rho$. Build $c(\mathbf{x}) = c_0(1 + \phi/c_0^2)^{-1}$. Feed into `CayleyVarcSolver2D`. Probe Weyl packet at impact parameter $b$; measure deflection. Pass criterion: $\Delta\theta$ matches $2GM/(bc^2)$ (Newtonian) or $4GM/(bc^2)$ (GR with photon factor of 2). Estimate: 1 week (most of it the time-dependent Poisson solver).

3. **V12 — Gravitational redshift from variable-$c$.** Uniform-$\rho$ slab → linear $c(z)$ → propagate monochromatic plane wave; measure shift in receiving Fourier window. Pass criterion: $\Delta\nu/\nu \approx -|\nabla c|L/c$ in sign and magnitude. Estimate: 2–3 days once V11 lands.

4. **V6 — BCC 3D substrate.** New `ca_bcc.py`. Re-run the 3D arms of B1, B2, C1, D1 against the BCC dispersion. Pass criterion: at $|\mathbf{k}|\ll 1$ the BCC linearization reproduces existing 3D residuals; at $|\mathbf{k}| \sim 0.5$ the dispersion matches $\arccos(c_x c_y c_z \pm s_x s_y s_z)$ to machine precision. Estimate: 1–2 weeks (the new lattice geometry touches FFT and Laplacian assumptions).

5. **V1, V5 — Exact arccos dispersion in 2D.** Cheap follow-up after V6. Adds the exact-arccos option to `ca_core.py` 2D Weyl. Cross-check against Paper 4 Eq. 23 frequency-dependent $c$. Estimate: 2–3 days.

6. **V2 — Klein paradox quantitative test.** 1D Dirac with step potential. Compare measured $R(\phi)$ against Paper 4 Fig. 3. Estimate: 2 days.

7. **V3, V7 — $n^2 + m^2 = 1$ and $A_0 = 0$ audits.** Documentation / regression test additions. Estimate: half a day.

Total: roughly 4–6 weeks of focused engineering, with V4 + V11 as the load-bearing first half.

---

## Cross-references

- v1: `ca-unified-proposition.md` (the original Φ-does-both-jobs proposition).
- F3 fixes: `ca-f3-propositions.md` (P1–P5 ranking for the Yukawa back-reaction; v2 preserves P1, P2, P4 and replaces the metric coupling that P5 partially worked around).
- Literature: `qca-papers-1-4-overview.md` (Papers 1, 2, 4 for L1/L2/L3; Paper 6 for L4; tests V1–V13).
- Ostoma–Trushyk synthesis: `ostoma-trushyk-1999-summary.md` (full EMQG framework; sources Eq. 19.7 and Eq. 18.31).
- Implementation state: `project-status.md` (13/13 phase tests; F3 symplectic; F3b Cayley lensing demo).
- Reference numerics: `ca-reference.md`.

---

## Honest caveats (extended from v1)

1. **EMQG is a physics essay, not a derivation.** Paper 6's modified Poisson equation has no first-principles derivation from informational axioms — it is motivated by the Fizeau analog and proposed as a phenomenological replacement for Einstein's tensor equation in absolute CA coordinates. Adopting it for L4 inherits this status. v2 is a *consistency-check* program against Paper 6's predictions, not a proof of EMQG.

2. **L4's time-dependent Poisson solver is a new engineering item.** Paper 6 writes the field equation with retardation ($1/c_0^2 \cdot \partial_t^2\phi$); a static Poisson would not capture gravitational waves or radiation back-reaction. The lattice version needs an implicit time step (Crank–Nicolson on the wave equation) to stay unitary. This is the largest implementation risk in v2.

3. **Composite photon coherence.** Paper 1's bilinear photon assumes the two underlying Weyl fields stay correlated. Maintaining correlation under interactions (including the L4 vacuum scattering) is non-trivial; Paper 4 notes that bosonic statistics emerge *approximately* via a smearing function $f_{\mathbf{k}}(\mathbf{q})$. Decoherence channels are not addressed in v2 and may break L3 in the presence of nontrivial L4.

4. **The page-26 disagreement.** v1 routed around Sachs' tetrad/spin-connection derivation by encoding the metric as a position-dependent $c$. v2 does the same: the EMQG potential $\phi$ replaces $g_{\mu\nu}$ as the geometric variable. Whether this evades the page-26 issue or relocates it is still open; a future curved-space implementation that tries to relate $\phi$ to a $g_{\mu\nu}$ would have to revisit it.

5. **No claim of Lorentz invariance.** L1's BCC lattice picks a preferred frame, exactly as the simple-cubic lattice did. DSR (S5) is the route to *deformed* covariance, not ordinary Lorentz. This is the same status as Papers 1, 4 and is not improved by v2.

6. **Renormalization is still not addressed.** Continuum limit (taking $\Delta x \to 0$) is the field-wide open problem; v2 inherits it from v1 and from the literature.

7. **WEP violation at $10^{-40}$ is unfalsifiable in float64.** Paper 6's central observable prediction is below numerical resolution by 24 orders of magnitude. v2 cannot test it.

---

## Summary table — what v2 contributes per mechanism

| Mechanism | v1 implementation | v2 implementation | Gate test |
|---|---|---|---|
| Fermion mass | Per-cell Yukawa $y\|\Phi\|$ | Per-cell Yukawa $y\,\text{Re}(\Phi)$ (unchanged from F3 fixes) | F1, F4 |
| Electromagnetic | External classical $A_\mu$ | Composite photon (Paper 1 Eq. 35) | V4, E1 (regression) |
| Weak | Per-cell SU(2) on left chirality (unchanged) | Unchanged | E2 |
| Higgs | $\delta\Phi$ fluctuations (unchanged) | Unchanged | F2 |
| Metric | $c \propto \|\Phi\|^{-\alpha}$ (ad hoc) | $c = c_0(1 + \phi/c_0^2)^{-1}$ with $\phi$ from Paper 6 Eq. 19.7 | V11, V12, F3b |
| 3D substrate | Simple-cubic (trivial automaton) | BCC ($s=2$, $\arccos$ dispersion) | V6 |
| Lattice dispersion | Linearized $\omega = c\|\mathbf{k}\|$ | Exact $\arccos$; frequency-dependent $c$ | V1, V5 |
| Covariance | Implicit Lorentz at small $\mathbf{k}$ | DSR via $L^D_\beta = \mathcal{D}^{-1}L_\beta\mathcal{D}$ | V8 |

The architecture preserved everywhere is the per-cell phase / Strang composition that made v1 work at machine precision. The substitutions are all *local* to specific files: `ca_core.py` (S2, exact dispersion option), `ca_curved.py` (S1, coupled to a new Poisson solver), `ca_maxwell.py` (S3, new module). v1's `ca_higgs.py`, `ca_weak.py`, `ca_dirac.py`, `ca_unified.py` are unchanged.

*This is a research proposition, not a result. Implementation and test would constitute the actual work; V4 + V11 are the recommended first steps because they close the two gaps where v1 had to substitute placeholder physics.*
