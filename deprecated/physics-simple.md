# The Physics of the Model, Explained Simply

*2026-05-29 - 22:30 — A plain-language tour of the entire model: what it is, how it works, and what each piece of physics means. Written for someone who is technically sharp but not a physicist. Every claim traces to a finding (F##), to `ca-reference.md`, `project-status.md`, `exactness-inventory.md`, or to the transcribed notebook in `reference-research/physics-notes-complete.md`. Where something is unproven or only suggested, it says so.*

---

## 0. The one-sentence version

We are testing whether the universe could be a giant grid of simple cells that update in lockstep, by building a small version of that grid on a computer and checking whether real physics — light, relativity, quantum behavior, the weak and strong forces, even gravity — falls out of the rules instead of being hand-installed.

That idea comes from Mark Ludwig's handwritten notebook (2007–2008). His core hunch: *"Dependence implies neighborhood; rules imply geometry."* If a cell's next value depends on certain neighbors, that list of neighbors **is** the shape of space. Spacetime is not the stage — it is the wiring diagram of the automaton.

---

## 1. The grid, the cells, and the tick

**The grid.** Space is a finite 3D lattice that wraps around at the edges. We don't use a plain cubic grid. We use the **body-centered cubic (BCC)** lattice — a cube with an extra point in the middle of each cell, so every point has 8 natural neighbors. This is not a taste choice: published math (the QCA uniqueness theorems) proves BCC is the *only* 3D arrangement on which a massless spin-½ particle can move correctly while respecting locality, reversibility, and isotropy. A simple cubic grid only supports a trivial, do-nothing automaton. (`ca-reference.md`; module `ca_bcc.py`.) A simpler 2D square grid is used for fast checks.

**The cells.** Each cell holds a small bundle of complex numbers — a *field*. The simplest is a two-number **Weyl spinor** $\psi = (f, g)$, which describes a massless spin-½ particle (think: a neutrino). Heavier machinery just adds more numbers per cell: a full electron is 4 complex numbers, a colored quark is 36, and the force fields (photon, W, Z, gluons) are stored either as field values or as small rotation matrices sitting on the links between cells.

**The tick.** Time advances in discrete steps called ticks. On each tick, every cell updates from its neighbors using one fixed rule. The honest way we run that rule is in *frequency space*: transform the whole grid (FFT), multiply each wave-mode by an exact small rotation matrix, transform back. This matters for three reasons:

- It exactly conserves total probability ("norm").
- It is exactly **reversible** — run it forward then backward and you return to the start, accurate to about $10^{-14}$ over thousands of ticks.
- Ludwig's original hand-written rule blew up numerically. We later showed the blow-up was a bad numerical method, *not* bad physics — the exact version is rock-stable. (`ca-reference.md`, Stages 1–2b; `ca_core.py`, `ca_fft.py`.)

The per-mode update matrix for a massless particle is

$$U(\mathbf{k}) = \cos(c\kappa)\,I - \frac{i\sin(c\kappa)}{\kappa}\,(\boldsymbol{\sigma}\cdot\mathbf{k}), \qquad \kappa = |\mathbf{k}|,$$

where $\boldsymbol{\sigma}$ are the Pauli matrices. The takeaway: **each tick is a tiny rotation.** That single idea — physics as rotation — runs through the entire model.

---

## 2. Light, and why the speed of light is a rotation rate

This is the model's most distinctive reframing (Finding **F26**), and it is worth slowing down for.

**The photon is not fundamental here.** Instead of a built-in light field, the photon is *composite* — built from a correlated pair of the massless fermion fields above. This is De Broglie's old "neutrino theory of light," **(2026-06-01 Update - The photon model element has been modified to the bound pair of Weyl spin-1/2 quanta in Ludwig's formulation due to De Broglie's composite bilinear being falsified see F66)** and we use it because it arises naturally from the lattice; the Standard Model's elementary photon would require bolting on a whole new field. (`ca_maxwell.py`; F17, F39.)

**Light turns; it does not travel.** The electric and magnetic fields form a real vector pair $(\mathbf{E}, \mathbf{B})$. Each tick, that pair undergoes an exact rigid rotation (verified exact to $\sim 2\times10^{-16}$):

$$\mathbf{E}(t{+}1) = \cos\Omega\,\mathbf{E}(t) + \sin\Omega\,\mathbf{B}(t), \qquad \mathbf{B}(t{+}1) = -\sin\Omega\,\mathbf{E}(t) + \cos\Omega\,\mathbf{B}(t).$$

So the **speed of light is not how fast something moves through space — it is the angular rate that the $(\mathbf{E},\mathbf{B})$ pair spins, per unit of spatial wavenumber:**

$$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}\bigg|_{|\mathbf{k}|\to 0} = \frac{1}{\sqrt{3}} \ \text{(BCC)}, \quad \frac{1}{\sqrt{2}}\ \text{(2D square)}.$$

A "wave moving across the room" is really this internal rotation advancing in time. The wave period is just the time to complete one full turn.

**Maxwell's equations are an approximation — ours is the exact law.** If you Taylor-expand the exact rotation to first order, you recover Maxwell's curl equation:

$$\frac{d\mathbf{E}}{dt} \approx \Omega\,\mathbf{B} = c_\text{lat}\,\nabla\times\mathbf{B}.$$

Maxwell is the *linearization* of a real rotation, valid when the turn-per-tick $\Omega$ is small. The exact law is the full trigonometric rotation.

**Two consequences fall out for free:**
- The mysterious $i$ in Maxwell's equations is just the continuous-time shadow of the real $90°$ rotation matrix $J = \big[\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\big]$, which satisfies $J^2 = -I$.
- Energy conservation $\|\mathbf{E}\|^2 + \|\mathbf{B}\|^2 = \text{const}$ is **geometry, not a separate law** — a rotation preserves length (Pythagoras). That's why energy is conserved exactly while Maxwell's curl law is only approximate. (F26, F17.)

**The leftover error is honest and expected.** Because Maxwell is a first-order approximation, there's a residual error that grows linearly in $k$ (the "$O(k)$ curl residual"), with an exactly-known leading coefficient $c_\text{lat}/\sqrt{2}$. We confirmed it's the same across five different lattice geometries (F21) and that you cannot smooth it away (F23 ruled that out). It's the price of running a discrete rotation at full tick size — not a bug.

**A real, testable prediction.** Building the photon from *both* handedness branches of the lattice gives a complete two-helicity photon (F39). The BCC grid is very slightly directional, so it predicts a tiny **vacuum birefringence**: light of opposite handedness travels at imperceptibly different speeds, strongest along the cube's body diagonal (coefficient $\sim -\sqrt{3}/27 \cdot k^2$, F30/F39). The effect is Planck-scale tiny and quadratic in frequency, but it is falsifiable against gamma-ray-burst and distant-source polarization data (F28). This is the kind of "extends beyond current measurements" prediction the project is hunting for.

---

## 3. Relativity, and why it is only *almost* exact

A fixed grid secretly picks a preferred frame (the grid's own rest frame), so perfect Einstein relativity is **not** baked in. Instead it emerges at long wavelengths and is gently modified near the Planck scale — this is the well-known "deformed" or "doubly-special" relativity. Two results make it concrete:

- **Boosts work exactly (F24).** The Weyl 4-current $j^\mu = \psi^\dagger\bar\sigma^\mu\psi$ transforms as a proper relativistic 4-vector under a Lorentz boost, to machine precision ($3.7\times10^{-16}$). Relativity's transformation law is exact on the lattice's currents.

- **Velocity addition is slightly bent (F22).** From the exact lattice dispersion relation, the familiar Einstein velocity-addition formula picks up a small, mass-dependent correction:

$$u' = \frac{u + v}{1 + 2\rho^2(m)\,uv}, \qquad \rho(m) = \frac{m}{\sqrt{1-m^2}\,\arcsin m}.$$

The correction always makes the lattice add velocities a hair *less* than Einstein (and dilate time a hair *more*). The deviations scale like $(v/c)^2$ and are minuscule, but they are exact, closed-form, and in principle testable.

---

## 4. Mass without a Higgs — the project's central bet

The Standard Model gives particles mass with the Higgs field. **This project deliberately replaces the Higgs** with Ludwig's "complex mass" idea (Finding **F27**, the project's signature decision in `key-decisions.md`).

**The notebook seed.** Ludwig noticed (notebook pages 59–60) that the matrices used to build the Dirac equation aren't unique — you can rotate the mass term and get identical physics. He asked: *what if that rotation is allowed to vary from place to place?* Promoting the constant mass phase $im$ to a local rotation $im\,e^{i\theta(x)}$, and then to a local SU(2) rotation $U(x)$ acting on the particle's isospin, produces a symmetry that touches **only one handedness** of the particle. That one-handedness is exactly the fingerprint of the weak force. His leap: **mass and the weak force may be two faces of the same left/right asymmetry**, with no separate Higgs needed.

**What we verified.** The mass step is

$$M_\text{SU2} = \cos(m\,\delta t)\,I + i\sin(m\,\delta t)\begin{pmatrix} 0 & U \\ U^\dagger & 0 \end{pmatrix},$$

which is exactly reversible for *any* choice of $U(x)$. The gauge "Ward identity" — the bookkeeping check that the symmetry is respected — holds with **no Higgs field present** ($\sim10^{-17}$). A mass gap exists with no scalar condensate. The field $U(x)$ does the Higgs's *job* (steering which components pair up) but is pure gauge: it is not a physical particle. (F27.)

**Where the boson masses come from instead.** With no Higgs to give $W$ and $Z$ their mass, that role is played by the **Stueckelberg mechanism** — a gauge field whose own internal motion acts as a mass term, giving $m_W = g f$ (F34b). A clean bonus: the photon comes out *exactly massless* because the relevant mass matrix is rank-1, so it automatically has one zero eigenvalue, and that eigenvalue is the photon (F44, exact to $\sim10^{-16}$).

**The prettiest result: mass is spherical Pythagoras (F46).** The full massive-particle energy law turns out to be the *law of cosines on a sphere* for a right triangle whose two legs are the photon's rotation and the mass's rotation:

$$\cos\Omega_\text{Dirac}(\mathbf{k}, m) = \cos\Omega_\text{rest}(m)\cdot\cos\omega_\text{kin}(\mathbf{k}), \qquad \Omega_\text{rest} = \arcsin m.$$

Expand that for small angles and you get **Einstein's $E^2 = p^2c^2 + m^2c^4$** as the flat-space limit of an exact discrete spherical identity. In other words, $E=mc^2$-style mass-energy is *geometry*: the photon rotation of §2 and the chirality rotation of §4 combine by spherical Pythagoras. Verified 8/8 at machine precision on both grids, both handedness branches.

---

## 5. The electroweak sector (photon, W, Z, hypercharge) — still Higgs-free

The model assembles a full electroweak sector on top of the F27 mass idea, with no Higgs anywhere:

- **Hypercharge without a scalar (F41, F42).** The $U(1)_Y$ hypercharge force is folded into the same pure-gauge field $U(x)$ by giving it the right diagonal phase. No physical scalar is added. The symmetry checks hold exactly, and turning the phase off reduces bit-for-bit to the plain F27 step. F42 extends this to quarks and to the right-handed particles.

- **Electroweak mixing and the W/Z (F35, F48).** The Weinberg mixing — how the photon and $Z$ are blended from two underlying fields — is an exact rotation. The mass ratio comes out **exactly** $m_Z/m_W = 1/\cos\theta_W$ (bit-for-bit, residual 0.0), and the charge formula $Q = T_3 + Y/2$ holds for all seven first-generation particles ($\sim10^{-17}$). The $Z$ is a fully propagating field with the correct per-particle couplings (F48, 12/12 tests pass).

- **The Weinberg angle is *predicted*, not assumed — partially (F45, F49).** In the Standard Model, $\theta_W$ is measured and put in by hand. Here, two independent counting arguments try to derive it from grid geometry: F45 gives $\sin^2\theta_W = 1/4$ (mass ratio within ~2% of experiment, zero fit parameters); F49 gives $\sin^2\theta_W = 2/9 = 0.2222$, within **0.44%** of the measured value, as an exact fraction. **Honest caveat the project flags itself:** the *number* 2/9 emerges cleanly, but the geometric assignment that produces it is not yet derived from first principles. So this is a strong structural hint, not a finished derivation.

A nice structural prediction drops out: at the bare angle $\sin^2\theta_W = 1/4$, the electron's $Z$ vector coupling vanishes exactly ($g_V^{e_L} = 0$) — not a coincidence, but a consequence of the underlying geometry (F48).

**Beta decay runs end-to-end.** The defining weak process $d \to u + W^- \to u + e^- + \bar\nu_e$ is implemented as a full lattice pipeline with charge, baryon, and lepton number all conserved (F54, `ca_charged_current.py`, 10/10 pass).

---

## 6. The strong force (quarks and gluons)

The strong sector uses standard lattice-QCD machinery (Wilson / Kogut–Susskind links) rather than the per-cell-phase trick, because color genuinely requires local gauge covariance. Each cell carries quarks (3 flavors × 3 colors × 4 components) plus small $3\times3$ SU(3) rotation matrices on its links. (`ca_strong.py`.)

Finding **F43** promotes gluons from static links to fully dynamical, propagating fields that obey the *same rotation law* as light (§2), self-interact through the Yang–Mills structure constants $f^{abc}$ (Jacobi identity verified to $10^{-16}$), and carry a Wilson-loop confinement diagnostic. 20/20 tests pass, 8 of them bit-for-bit exact; with trivial links it reduces exactly to three color copies of a plain fermion. Quark mass uses the same F27 mechanism as the electron. **Not yet done:** the full quark-binding (linear confinement) regime, and CKM/Cabibbo flavor mixing.

---

## 7. Gravity — the youngest, most provisional piece

Gravity is built by extending the spherical-triangle picture (§4): a particle's two rotation "legs" are allowed to vary from place to place in a curved background. It is the most exploratory part of the model, and the documents are careful about what is derived versus assumed.

- **Which leg does what (F50).** Putting the particle on a static curved metric, the **clock-rate / mass leg** carries gravitational redshift — reproducing the correct general-relativity redshift factor — while the **kinetic leg** carries light bending and the Shapiro time delay (8/8 pass). *Caveat:* F50 still imports the gravitational potential $\phi = -GM/r$ by hand.

- **Closing the loop, but only to Newton (F52).** Instead of importing the potential, F52 generates it from mass density via $\nabla^2\Phi = 4\pi G\rho$. The loop closes — but sourcing only the clock-rate leg gives the *Newtonian* light-bending (half of Einstein's value).

- **Recovering Einstein (F55).** Sourcing the *spatial* part of the metric from the same mass, via the linearized Einstein equation, supplies the missing half through "trace reversal," landing on Einstein's bending coefficient exactly and uniquely. *Honest caveat the finding states:* this **assumes** the linearized Einstein equation — it does not derive general relativity from the lattice rule. Newton's $G$ is still an input.

Earlier, separate variable-speed-of-light work (`ca_curved.py`, `ca_emqg.py`) reproduced light deflection (~0.3–3% off Einstein), Shapiro delay (~0.06%), and Mercury's perihelion precession (~1.5%) as quantitative matches. The deeper goal — deriving gravity *and* electromagnetism together from spacetime structure (Ludwig's "Sachs electrogravity" inspiration) — remains a roadmap (`ca-dirac-gravity-plan.md`), not implemented code.

---

## 8. "Exact" versus "machine precision" — the standard the project holds itself to

The project grades every result on a three-rung ladder (`exactness-inventory.md`), and strongly prefers the top rung:

1. **Exact algebraic** — the result is an identity, true at the symbolic level, often computed with exact fractions so the answer is *literally zero*. It does not depend on floating-point and does not get worse as the grid grows. Examples: the light speed $c_\text{lat} = 1/\sqrt{d}$; the F46 spherical-Pythagoras mass law; $m_Z/m_W = 1/\cos\theta_W$ (residual 0.0); the charge relation $Q = T_3 + Y/2$; all six anomaly-cancellation conditions (exactly 0); the entanglement Tsirelson bound $|S| = 2\sqrt{2}$.

2. **Machine precision** — true down to the computer's round-off floor (~$10^{-15}$), the best a numerical calculation can do. Examples: energy and norm conservation, time-reversibility, dispersion relations, boost covariance.

3. **Quantitative** — agreement within a stated percentage, with no claim of an exact underlying identity. Examples: the gravitational light-bending and perihelion results.

As of the latest status (2026-05-29), the inventory lists roughly **140+ exact-algebraic** and **~55 machine-precision** results.

---

## 9. The honest bottom line

**What the model claims to do:** reproduce the *structure* of one full generation of known physics — the electron, neutrino, up/down quarks, photon, W, Z, and gluons, plus relativity, quantum behavior, and gravitational lensing — from a single deterministic, local, reversible rule on a BCC grid, **without a Higgs field**, using Ludwig's chiral complex-mass mechanism. The project reports that every "Tier-A" structural test for that first generation is now closed: anomaly cancellation is exact, beta decay runs end-to-end, and the force carriers all propagate by the same rotation law.

**What is still open (stated plainly in the project's own notes):**

- **Real units and real numbers (the big gap).** Everything currently runs in grid-natural units with couplings set to 1 and $c_\text{lat} = 1/\sqrt{3}$. The model has **not** been pinned to SI units, to the measured coupling constants ($\alpha \approx 1/137$, $\sin^2\theta_W \approx 0.231$, $\alpha_s$), or to absolute particle masses. This is the difference between "reproduces the *shape* of physics" and "predicts the *measured numbers*," and it is the next major phase of work.
- **Gravity is partial** — phenomenological lensing and a redshift/bending split, not a fully emergent general relativity; $G$ is an input.
- **Quark confinement, flavor mixing (CKM), and the heavier 2nd/3rd generations** are not yet built.
- The standout original prediction — **vacuum birefringence** from the grid's slight directionality — has not yet been confronted with real polarization data.

**One caveat worth stating clearly:** all of the exactness claims and the "first generation structurally complete" status are the project's own internal test results and self-assessment. They have not been externally peer-reviewed, and the originating ideas (a Higgs-free electroweak sector, Sachs-style unification) are outside the mainstream. This document faithfully describes what the model *does and tests internally* — it does not independently certify that the underlying theory is correct. That is exactly the body of work the project is building up so that a willing physicist could one day check it.

---

*Sources: `ca-reference.md`, `project-status.md`, `first-gen-completeness.md`, `exactness-inventory.md`, `key-decisions.md`, `reference-research/physics-notes-complete.md`, and findings F16–F55 (load-bearing: F17, F21, F22, F24, F26, F27, F30, F34b, F35, F39, F41, F42, F43, F44, F45, F46, F48, F49, F50, F52, F54, F55).*
