# A Unified Proposition: Higgs Mass Generation and Metric Backreaction from a Single Scalar Field

*Speculative.  Builds on the implemented CA architecture in `ca_core.py`, `ca_dirac.py`, `ca_curved.py`, `ca_weak.py`.  All current tests (8/8) must remain passing in the appropriate limit.*

*Drafted 2026-05-14.*

---

## The pattern the test results reveal

The Phase A–E test results show a sharp asymmetry. Three things reach machine precision on the existing CA:

| What works at machine precision | Residual |
|---|---|
| Dirac dispersion (mass term in propagator) | 9×10⁻¹⁷ |
| U(1) Aharonov–Bohm phase pickup | 4×10⁻¹⁶ |
| SU(2) parity violation (right-chirality leakage) | 0 (exact) |

And one thing does not:

| What stays approximate | Residual |
|---|---|
| Variable-c (refractive analog of curvature) | ~30% norm drift over 200 steps |

The pattern: anything that can be implemented as **a per-cell phase** is exact. Anything that requires **modifying the propagator structure across cells** is approximate. That is the signature distinction between gauge fields (which add phases) and gravity (which modifies the metric).

The proposition below uses this distinction to put Higgs mass generation and metric backreaction on the same footing — as per-cell phase-like couplings of a single new scalar field. If it works, both follow naturally from the existing architecture without breaking any of the implemented tests.

---

## The proposition

Add one new field to the CA: a complex scalar **Φ(x, t)** at each cell. Φ obeys its own Klein–Gordon-like CA on the same lattice. All existing fermion fields (η, χ, isospin doublet) couple to Φ in two specific ways. The two couplings give, respectively, the Higgs mass-generation mechanism and the metric-backreaction (gravity) mechanism. The CA implementation reduces to the existing implementation in the limit Φ(x, t) = v (a fixed nonzero background value).

### The single field

Per cell, in addition to everything already in the CA:

$$\Phi(\mathbf{x}, t) \in \mathbb{C}, \qquad \text{state size: +2 real numbers per cell}$$

Φ obeys a self-coupled Klein–Gordon equation derived from a Mexican-hat potential:

$$\mathcal{L}_\Phi = \partial_\mu\Phi^*\partial^\mu\Phi - V(|\Phi|), \qquad V(|\Phi|) = -\mu^2|\Phi|^2 + \lambda|\Phi|^4$$

with minimum at $|\Phi|^2 = \mu^2/(2\lambda) \equiv v^2$. The CA implements this as a Φ-stepper analogous to the existing Weyl/Dirac steppers; details below.

### Coupling 1 — Higgs mass generation (per-cell phase)

The existing Dirac propagator has a constant mass $m$ that couples η ↔ χ. Replace this with a Yukawa coupling to Φ:

$$m_{\text{eff}}(\mathbf{x}, t) = y \cdot |\Phi(\mathbf{x}, t)|$$

In the existing `dirac_step_2d_splitstep`, the constant `m` parameter becomes a field. Where the code currently has `mc2 = m * c**2`, substitute `mc2 = y * |Phi(x)| * c**2` evaluated per cell.

In the **vacuum limit** $\Phi = v$ (constant), $m_{\text{eff}} = y v$ — a constant fermion mass. All existing Dirac tests pass with $m \to y v$. *No existing test is broken.*

In the **excited regime** $\Phi = v + \delta\Phi(\mathbf{x}, t)$, fluctuations $\delta\Phi$ are the Higgs boson. They propagate via the same Klein–Gordon CA at mass $m_h^2 = 2\mu^2$ (standard result from expanding $V$ around $v$).

For gauge bosons (Phase E2 SU(2) and a future Phase F extension): the kinetic term $|D_\mu \Phi|^2$ contributes mass terms when $\Phi$ has VEV. With $D_\mu = \partial_\mu - i g W^a \tau^a$:

$$|D_\mu \Phi|^2_{\Phi=v} \supset \tfrac{1}{2} g^2 v^2 W^a_\mu W^{a\mu}$$

giving $m_W = gv/2$. Same per-cell phase structure as the existing SU(2) gauge step — the Φ field just sets the local mass scale.

### Coupling 2 — Metric backreaction (per-cell phase, same field)

Define the local propagation speed as a function of $|\Phi|$:

$$c(\mathbf{x}, t) = c_0 \cdot \left(\frac{|\Phi(\mathbf{x}, t)|}{v}\right)^{-\alpha}$$

for some coupling exponent $\alpha > 0$. In the vacuum limit $|\Phi| = v$, $c = c_0$ — the existing implementation, unchanged.

Where $|\Phi|$ is locally above $v$: $c < c_0$, the analog of a slower region (gravitational time dilation, redshift). Where $|\Phi|$ is below $v$: $c > c_0$, the analog of negative curvature.

This is the same structure as the Phase C1 variable-c stepper that we just put on a proper Strang split. The CA implementation: at each timestep, build the c-field `c(x) = c_0 * (|Phi(x)| / v)^(-alpha)`, then call `weyl_step_2d_varc_strang(f, g, c_field)`. The implementation is already there.

The dynamical backreaction is automatic: Φ evolves under its own Klein–Gordon CA, with the Φ stress-energy *also* sourced by the fermion fields via the Yukawa coupling. Where fermions concentrate, $|\Phi|$ shifts from $v$, $c$ changes, and the fermions feel curvature. This is the discrete analog of "matter tells geometry how to curve; geometry tells matter how to move."

### Why both couplings to one field

Because every existing CA mechanism is a per-cell phase. The "metric" $c(\mathbf{x})$ acts on the kinetic propagator as $\cos(c\kappa)$ — a phase. The "mass" acts on the mass propagator as $\cos(E\Delta t)$ with $E$ depending on $m$ — a phase. The "U(1) gauge" acts as $\exp(-iqA_0\Delta t)$ — a phase. The "SU(2) gauge" acts as $\exp(-ig W^a\tau^a\Delta t)$ — a phase.

A single scalar field that sets the local coupling strength of each propagator phase is the minimal way to make both Higgs and gravity *of the same kind* as everything that already works.

---

## What this preserves and what it adds

### Reduction to current tests (the parameter-preservation contract)

Set $\Phi(\mathbf{x}, t) = v$ everywhere, for all time. Then:

1. $m_{\text{eff}} = yv$, a constant. **Phase D1** (Dirac CA, dispersion, zitterbewegung) passes exactly with $m \to yv$.
2. $c(\mathbf{x}) = c_0$, constant. **Phase C1** trivializes to the existing flat-space Weyl propagator; **Phase B1** group-velocity measurement gives $|v_g| = c_0$.
3. No new phase enters U(1) or SU(2) gauge steps. **Phase E1** (Aharonov–Bohm at machine precision) and **Phase E2** (parity violation exact) are unchanged.
4. The Bloch-coloring visualization (**Phase A1, A2**) is unchanged; an optional Φ-magnitude overlay can be added.

This is the contract: the unified theory must reduce to the implemented CA in the $\Phi = v$ limit. All eight passing tests remain passing.

### What's genuinely new

- **Dynamical Higgs.** Fluctuations $\delta\Phi$ around $v$ are propagating Higgs bosons. The CA can simulate Higgs production and decay just like fermion scattering.
- **Mass running.** $m_{\text{eff}}(\mathbf{x}, t) = y|\Phi(\mathbf{x}, t)|$ varies in time and space. Pre-electroweak-symmetry-breaking ($\langle\Phi\rangle = 0$) regimes become accessible: when $\Phi$ has not yet settled to $v$, fermions are massless and gauge bosons are massless.
- **Self-sourced curvature.** Energy density (fermions, gauge fields, Φ itself) shifts $\Phi$ off its VEV, which changes the local $c$. Gravity is sourced by everything that carries energy.
- **One coupling does two jobs.** $\alpha$ in the metric coupling and $y$ in the Yukawa coupling are independent parameters. But they share the same field, so consistency constraints emerge: the Higgs particle mass $m_h$ and the gravitational coupling $G$ are related through the Φ potential parameters $\mu$ and $\lambda$. The CA implementation makes these constraints empirically testable.

---

## Concrete CA implementation sketch

### Step structure (Strang-symmetric, three layers)

Per timestep:

1. **Half-step Φ kinetic:** apply the Klein–Gordon split-step propagator to Φ at the current $c_0$ (a constant background speed). The Klein–Gordon CA is its own module — `ca_higgs.py` — and uses a 2-component representation $(\Phi, \dot\Phi)$ analogous to how the original scalar wave CA worked, but now first-order in time via a Pauli-doubling trick.

2. **Half-step Φ self-potential:** apply the position-space phase $\exp(-i V'(|\Phi|)\Delta t/2)$ at each cell. $V'(|\Phi|) = -2\mu^2|\Phi| + 4\lambda|\Phi|^3$. This is a per-cell phase, exact-unitary.

3. **Full fermion + gauge step using the *current* Φ:**
   - Build $m_{\text{eff}}(\mathbf{x}) = y|\Phi(\mathbf{x})|$.
   - Build $c(\mathbf{x}) = c_0 (|\Phi|/v)^{-\alpha}$.
   - Call the variable-mass, variable-c Dirac stepper (a small extension of the existing `dirac_step_2d_splitstep` to take per-cell $m$ and call `weyl_step_2d_varc_strang` for the kinetic).
   - Apply existing U(1) and SU(2) gauge phases.

4. **Half-step Φ self-potential and Φ kinetic** (Strang second halves).

This is six existing pieces glued together. No new propagator math is required.

### Per-cell state size

The CA cell state grows from:
- Existing fermion + gauge: 4 (Dirac) + 4 (left doublet extra) + 8·real (W gauge field) + 4·real (A gauge field) ≈ 20 numbers/cell.

To:
- Add Φ: 2 real numbers (Re Φ, Im Φ) plus 2 for $\dot\Phi$ → **+4 real numbers per cell**.

A 4-real-number addition to the cell state is the entire cost of unifying Higgs and gravity.

### Validation plan

A new `Phase F` test suite (proposed):

| Test | Limit | Expected result |
|---|---|---|
| F1 | Φ = v constant everywhere | All 8 existing phase tests pass unchanged |
| F2 | Φ = v + small wave packet (Higgs) | δΦ propagates at mass $m_h = \sqrt{2}\mu$; Higgs dispersion ω² = k² + m_h² verified at machine precision |
| F3 | Φ = v but local fermion density spike | $c(\mathbf{x})$ decreases at the spike; a probe Weyl packet refracts toward the density spike (Newtonian-limit gravitational attraction) |
| F4 | Φ in symmetry-restored phase ($\langle\Phi\rangle = 0$) | Fermions are massless; zitterbewegung disappears; Weyl regression holds |
| F5 | Higgs decay channel | Higgs packet ($\delta\Phi$) decays into fermion-antifermion pair via Yukawa coupling; energy conservation holds |

F1 is the mandatory regression. F2–F5 are the new physics this proposition predicts.

---

## Honest caveats

This proposition does not claim to *derive* the Higgs mechanism or general relativity from the CA. It claims that **both can be accommodated by adding one scalar field**, with all current implementation passing as the vacuum limit. It is a toy model, not a fundamental theory. The specific choice $c(\mathbf{x}) = c_0(|\Phi|/v)^{-\alpha}$ is a parameterization, not a derivation; the Brans–Dicke / dilaton-gravity literature has well-known issues with this form (scalar can drive cosmological expansion in unphysical ways) that any serious implementation will hit.

**The variable-c stepper is the bottleneck.** Even after the Strang split, norm drift was ~30% over 200 steps in the test. For F3 (self-sourced curvature) to give clean numerical results, the variable-c implementation needs to improve to Cayley/Padé (exactly unitary, requires sparse linear solve per step) or higher-order Trotter splitting. This is the single most important engineering follow-up.

**Yang–Mills self-coupling.** The SU(2) gauge field W is currently static. For the Higgs mechanism to give the W its mass, W must be a dynamic field with its own kinetic and self-interaction terms. Adding Yang–Mills dynamics to the CA is a separate prerequisite (notebook pages 62–66 sketch the structure, but a working implementation has not been built).

**Renormalization is not addressed.** The CA at lattice scale $\Delta x = 1$ is regularized by the Nyquist cutoff. Whether the continuum limit (taking $\Delta x \to 0$) gives the Standard Model + GR in a controlled way is the open question every lattice-gauge-theory practitioner faces, and it is not solved here.

**The page-26 disagreement.** Notebook pages 26–28 flagged a discrepancy with Sachs' tetrad-formalism derivation. This proposition routes around the issue by *not* using the tetrad/spin-connection formulation at all — the metric is encoded as a position-dependent $c$ rather than as $e^a{}_\mu$. Whether this evades the page-26 problem or just relocates it is a question for whoever implements F3.

---

## Why this is the right shape

Three observations from the implemented CA make this proposition look natural rather than ad-hoc:

1. **Phase D1's mass term is already a Yukawa coupling waiting for a field.** The existing `dirac_step_2d_splitstep` takes a scalar `m` parameter at each call. Promoting `m` to a per-cell field is a one-line code change. The propagator structure is unchanged.

2. **Phase E2's parity violation already uses one field acting selectively on one chirality.** SU(2) on η only. Adding a second selective coupling — Φ acting on the (η, χ) mass term — uses the same architectural slot. Both are "per-cell field acts on a specific spinor subspace."

3. **Phase C1's variable-c was always going to require a sourcing scalar.** A constant external $c$ field is implausible as gravity; it needs to be set by something. Φ being that something is the natural choice, especially given (1) — the same field that sources mass via Yukawa is the same field that sources $c$ via the metric coupling. Two effects, one field, both implemented as per-cell phases.

The proposition is the minimal extension that preserves every implemented test, adds Higgs mass generation, and adds metric backreaction. It does not require new propagator mathematics — only one new field, one new self-potential, and two new couplings (both of the same type the CA already does machine-precision well).

---

## Recommended sequencing

1. **Klein–Gordon CA for Φ** as a standalone module (`ca_higgs.py`). Verify its own dispersion, norm conservation, and Mexican-hat dynamics in isolation. Estimate: 1–2 days.
2. **Variable-mass Dirac stepper.** Promote the `m` parameter of `dirac_step_2d_splitstep` to a per-cell array, recompute $E(\mathbf{k}, \mathbf{x})$ via the same split-step structure but with a per-cell mass. Re-run Phase D1 with constant $m(\mathbf{x}) = yv$ to confirm regression. Estimate: half a day.
3. **Yukawa coupling end-to-end (no gravity yet):** combine Φ stepper + variable-mass Dirac with the Yukawa link $m(\mathbf{x}) = y|\Phi(\mathbf{x})|$. Run F1 (regression: Φ = v fixed), F2 (Higgs propagation), F4 (symmetry restoration). Estimate: 1–2 days.
4. **Improve variable-c to Cayley/Padé.** Strict unitary requirement for the metric coupling. This is the bottleneck. Estimate: 3–5 days including testing.
5. **Couple Φ to $c(\mathbf{x})$:** run F3 (Newtonian gravity demo — wave packet refracts toward fermion density). Estimate: 1–2 days once (4) is in.
6. **Yang–Mills dynamics for W** (deferred prerequisite for full Higgs–weak coupling): add the gauge field kinetic + self-interaction. Estimate: 1 week.
7. **Full Higgs–weak coupling:** $|D_\mu \Phi|^2$ kinetic term, gauge boson mass generation. Run F5 (Higgs decay channel). Estimate: 1 week.

Total: roughly 3–4 weeks of focused engineering once the variable-c bottleneck is resolved. Compared with the project to date (which built the Weyl/Dirac/U(1)/SU(2) stack in one session), this is a comparable expansion.

---

## Summary

| Mechanism | How the CA implements it | Test that demonstrates it |
|---|---|---|
| Fermion mass | Per-cell propagator phase $\cos(E\Delta t)$ | Phase D1 — Dirac dispersion, zitterbewegung |
| Electromagnetic | Per-cell phase $\exp(-iqA_0\Delta t)$ | Phase E1 — Aharonov–Bohm |
| Weak | Per-cell SU(2) phase on left chirality | Phase E2 — parity violation |
| Metric (current) | Position-dependent $c$ in kinetic propagator | Phase C1 — Snell refraction (~30% norm drift) |
| **Higgs (proposed)** | **Per-cell Yukawa: $m_{\text{eff}} = y\|\Phi\|$** | **F2 — Higgs dispersion** |
| **Backreaction (proposed)** | **$c(\mathbf{x}) = c_0(\|\Phi\|/v)^{-\alpha}$ sourced by Φ** | **F3 — wave packet refracts toward fermion density** |

The two proposed mechanisms are the same kind of object as the four that already work. The only thing that has to improve is the variable-c implementation. Everything else falls out naturally.

*This is a research proposition, not a result. Implementation and test would constitute the actual work.*
