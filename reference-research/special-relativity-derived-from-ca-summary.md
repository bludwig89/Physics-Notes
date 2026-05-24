# Special Relativity Derived from Cellular Automata Theory — Ostoma & Trushyk (1999)

**Source:** `reference-research/special-relativity-derived-from-ca-theory.pdf` (also indexed as `3 - Special Relativity Derived from Cellular Automata Theory.pdf`)
**Authors:** Tom Ostoma and Mike Trushyk, Brampton, Ontario (`emqg@rogerswave.ca`)
**Date:** January 22, 1999
**Subtitle:** *The origin of the universal speed limit*
**Companion paper:** Ostoma & Trushyk 1999 *Cellular Automata Theory and Physics* — summarized in [`ostoma-trushyk-1999-summary.md`](ostoma-trushyk-1999-summary.md)

*Summary generated 2026-05-21 - 19:34.*

---

## 1. Thesis

Special Relativity (SR) is not a fundamental theory — it is the **measurement-frame projection** of a deeper, strictly local computation on a 3D geometric Cellular Automaton (CA). The two SR postulates and the Lorentz transformation drop out as theorems once two ingredients are stipulated:

1. The universe is a 3D geometric CA with a separate (also discrete) absolute time, where every cell updates from local rules in one global "clock" tick.
2. Photons are the simplest possible CA motion: an information pattern that shifts **exactly one cell per clock tick**, independent of source motion.

From these, the paper recovers Minkowski 4D space-time, constancy of $c$, length contraction, time dilation, and $m = m_0 / \sqrt{1 - v^2/c^2}$ — but reinterprets the last result as a **reduction in force**, not an increase in mass.

---

## 2. Core postulates

| # | Postulate | Status in current model |
|---|---|---|
| P1 | Universe is a 3D geometric CA; each cell updates by one local rule each clock tick (Fredkin's *Digital Mechanics*). | Adopted (see `ca-reference.md`). |
| P2 | Photon = information pattern shifting **one cell per clock cycle**, in any allowed CA direction, decoupled from source motion. | Bisio uniqueness result + our 2D arccos QCA give $c_\text{lat} = 1/\sqrt d$ (Exactness Inventory T1 #9, #12). |
| P3 | A hidden "CA absolute reference frame" exists (the cell coordinate grid + global clock) but is **not experimentally accessible** for inertial frames. Only accelerated frames can detect a quasi-absolute reference via the quantum vacuum. | Compatible with our emergent-time / emergent-Lorentz approach. |
| P4 | All forces are quantum vector-boson exchange (QFT-style), realized as information pattern transfers between fermion patterns. | Aligned with composite-photon framework and SU(3) gauge link work. |

---

## 3. Derivation of the universal speed limit

The CA cannot propagate information faster than one cell per tick. Identifying the cell pitch with the Planck length and the tick with the Planck time gives the maximum information-transfer velocity:

$$
V_P \;=\; \frac{L_P}{T_P} \;=\; \frac{1.6 \times 10^{-35}\ \text{m}}{5.4 \times 10^{-44}\ \text{s}} \;\approx\; 3 \times 10^{8}\ \text{m/s} \;=\; c \qquad (9.1)
$$

**Authors' caveat:** in their companion EMQG paper the *raw* CA velocity is higher than the observed $c$; vacuum scattering with virtual charged particles reduces the propagation speed to the measured value. This caveat is important — it leaves room for the *measured* $c$ to be smaller than $L_P/T_P$ without breaking the CA model.

---

## 4. Two-frame measurement argument

Two observers A and B move at absolute CA velocities $v_a, v_b$ with $v_r = v_b - v_a$. Each carries a "ruler" of length $d$ in absolute (cell-count) units. Because light shifts one cell per tick regardless of source motion, the **measured** light speed for A is

$$
\frac{d + v_a d}{d + v_a d} \;=\; 1\ \text{pvu (Planck velocity unit)}
$$

and identically for B. So both observers measure $c$ = constant **in absolute CA units**, even though they are moving differently with respect to the hidden grid.

When A and B compare their meter-stick and clock readings (defined as 1000 wavelengths and 1000 cycles of a reference green light), they discover that B's ruler is contracted and B's clock dilated relative to A, with the Lorentz factor $\gamma = (1 - v^2/c^2)^{-1/2}$. The paper credits Einstein's spherical-wavefront algebra (Eqs. 9.2–9.4) as the route from "constancy of measured $c$" to the full Lorentz transformation.

$$
x^{*} = \gamma (x - v t), \quad y^{*} = y, \quad z^{*} = z, \quad t^{*} = \gamma\left(t - \frac{v}{c^2} x\right) \qquad (9.2)
$$

---

## 5. The flux-rate reinterpretation of relativistic mass

This is the paper's most distinctive technical claim and the one most worth testing against our lattice work.

**Setup.** Force between two bodies is the exchange of bosons. The magnitude of the transmitted force is proportional to the **received flux rate** $\Phi$ (exchange particles per unit time at the receiver). If receiver B recedes from emitter A at relative velocity $v$, then by Lorentz time dilation the timing of received bosons is dilated, and

$$
\Phi_b \;=\; \Phi_a \sqrt{1 - v^2/c^2}.
$$

Therefore the force itself is reduced:

$$
\boxed{\,F \;=\; F_0 \sqrt{1 - v^2/c^2}\,} \qquad (10.1)
$$

**Reinterpretation.** Equating to $F = m a$ with $m$ held constant gives

$$
F_0 \sqrt{1 - v^2/c^2} \;=\; m_0\, a \qquad (10.2)
$$

If, instead, one keeps $F = F_0$ fixed and absorbs the slow-down into the mass, one recovers the textbook formula

$$
m \;=\; \frac{m_0}{\sqrt{1 - v^2/c^2}}.
$$

The two pictures are **operationally indistinguishable** in a single inertial frame, but the CA picture says the mass is actually absolute and the *force is what changes*. The paper claims this is consistent with the "Ultimate Speed" electron experiment (French, ref. 21) — at $v \to c$ the force tends to zero, so further acceleration is impossible.

**Consequence for the absolute frame.** Because *inertial force* (from QI) and the *acceleration of virtual quanta* are absolute, inertial mass is absolute. SR's mass-velocity formula becomes a frame-projection artifact of the flux-rate slowdown, not a property of matter.

---

## 6. Other relations the paper recovers or asserts

| Item | Form | Notes |
|---|---|---|
| Casimir force (cited from QED) | $F/A = -\pi^2 h c / (240\, D^4)$ | Eq. 4.1 — cited as evidence for the quantum vacuum that QI requires; experimentally confirmed by Lamoreaux to ~5%. |
| Photon momentum | $P = mc$ | Eq. 10.31 |
| Wave/frequency | $c = \nu \lambda$ | Eq. 10.32 |
| Planck quantum | $E = h\nu$ | Eq. 10.33 |
| de Broglie | $\lambda = h/p$ | Eq. 10.34 |
| $E = mc^2$ | Derived purely from 10.31–10.34, *without* SR algebra. | Their alternate route: $c/\nu = h/p = h/(mc)\Rightarrow E = mc^2$. |
| Geometric-CA connectivity | $C_D = 3 C_{D-1} + 2$ | Number of neighbors of an N-dim geometric CA in terms of the next-lower one. 1D:2, 2D:8, 3D:26, 4D:80, 5D:242. |
| Rule-space size for 3D binary CA with 26+1 inputs | $2^{2^{27}} = 2^{134{,}217{,}728}$ | Argues against rule discovery by brute force. |

---

## 7. Where the paper aligns with our existing model

| Our result | Paper's claim | Match quality |
|---|---|---|
| Lattice speed of light $c_\text{lat} = 1/\sqrt d$ exactly (Tier 1 #9). | Photon shifts one cell per tick → $c = L_P/T_P$ exactly in absolute units (Eq. 9.1). | Same conceptual mechanism, same algebraic form (modulo the $\sqrt d$ factor that the authors do not explicitly include — they assume 1D shift while we use the BCC / d-cube). |
| Exact 2D dispersion $\omega = \arccos(c_x c_y)$, Dirac dispersion $\omega = \arccos(\sqrt{1-m^2}\, c_x c_y)$ (Tier 1 #12, #13). | Photon = simplest CA motion; matter has lower velocity because it requires $>1$ tick per cell shift. | Compatible. Our dispersion *quantifies* the slowdown they describe qualitatively. |
| SR-2 LV coefficients $\beta_\text{LV}(m), \gamma_\text{LV}(m)$ — closed-form Lorentz-violation residues for the 2D-square QCA (Tier 1 #20, #21). | Lorentz transformation is exact in absolute CA units; deviations would only show at the Planck scale. | Our derivation **finds those deviations algebraically**; the paper says they should exist but doesn't compute them. We are quantitatively ahead here. |
| Mohr Lorentz-boost covariance of the photon wave function (Tier 1 #25–27). | Lorentz transformation follows from absolute-unit measurement of an expanding light sphere (Eqs. 9.3–9.4). | Our test confirms the result the paper asserts. |
| Composite-photon energy conservation, transversality (Tier 1 #7, #8; Tier 2 #7). | Forces are boson-exchange flux; vacuum is teeming with virtual photons. | Aligned. |

---

## 8. Tests and equations worth adding to the model

Listed in rough order of leverage. Each refers to something the paper *asserts* but does not numerically demonstrate, and that our lattice machinery is positioned to verify or falsify.

### 8.1 Flux-rate identity $\Phi_b = \Phi_a \sqrt{1 - v^2/c^2}$ (Paper Eq. 10.1)

**Why it matters.** This is the paper's structural rewrite of relativistic mass. If we can verify (or refute) the flux-rate identity at the lattice level, we get either an algebraic alternative to relativistic mass *or* a clean disconfirmation of the CA-flux picture.

**Proposed test.** In a 2D arccos QCA (or BCC) sandbox, emit a periodic stream of "boson" wavepackets from a stationary site A toward a receiver B drifting at lattice velocity $v_\text{lat}$. Count arrivals per absolute tick at B and compare to $\Phi_a \sqrt{1 - v_\text{lat}^2 c_\text{lat}^{-2}}$.
**Expected exactness tier.** Machine precision if the identity is correct — the test is essentially a counting problem driven by the Dirac dispersion we already verify exactly.

### 8.2 Force-or-mass operational indistinguishability (Paper §10.1)

**Why it matters.** The paper's central reinterpretation hinges on the claim that $F = F_0 \sqrt{1 - v^2/c^2}$ with $m = m_0$ is *operationally equivalent* to $F = F_0$ with $m = \gamma m_0$ in a single inertial frame. We can stage that equivalence on the lattice and check whether any observable (e.g. lattice analogue of the Ultimate-Speed experiment) breaks it.

**Proposed test.** Apply a constant "external" force pulse to a Dirac wavepacket on the BCC lattice. Measure (a) the change in group velocity as $v \to c$ and (b) the energy delivered at a downstream collision site. Compare to both Einstein-mass and CA-flux predictions.
**Expected exactness tier.** Quantitative match within FFT round-off floor.

### 8.3 $E = mc^2$ from QM-only identities (Paper §10.3, Eqs. 10.31–10.34)

**Why it matters.** The paper derives $E = mc^2$ without SR algebra, using only $P = mc$, $c = \nu\lambda$, $E = h\nu$, $\lambda = h/p$. Our composite-photon framework supplies $P, c, \nu, \lambda$ as lattice observables. A bit-for-bit verification of the chain would join the exactness inventory.

**Proposed test.** Build a small test in `ca_maxwell.py` that, for a series of photon momenta on the lattice, evaluates each of the four identities and the composite relation $E = mc^2$ ⟺ $c/\nu = h/(mc)$.
**Expected exactness tier.** Tier 1 (exact algebraic). Should hold to ε per quantity.

### 8.4 Two-observer measurement projection onto absolute CA units (Paper §9.3)

**Why it matters.** The paper's derivation pivots on the claim that two inertial observers, using rulers and clocks defined in absolute Planck units, both measure $c$ as one Planck velocity. This is the lattice-native version of the "spherical light sphere" argument.

**Proposed test.** Initialize a 2D-square QCA photon pulse at the origin, propagate, then perform two distinct "measurements" — one in the lattice-rest frame, one in a Lorentz-boosted frame (re-using the boost machinery already verified in Tier 1 #25–27). Compare measured $c$ in both, plus the contracted-ruler / dilated-clock readings.
**Expected exactness tier.** Machine precision via FFT.

### 8.5 Casimir force prediction in the lattice vacuum (Paper Eq. 4.1)

**Why it matters.** Verifying $F/A = -\pi^2 h c / (240\, D^4)$ as an emergent property of a lattice vacuum would strongly support QI / vacuum-flux interpretation. This is far more ambitious than the items above and might require a virtual-photon zero-point spectrum on the lattice that we don't yet have.

**Status.** Open / out-of-scope for current sandbox. Worth flagging in `findings.md` as a long-range falsifiable target.

### 8.6 Velocity-addition rule under the flux-rate picture

**Why it matters.** The paper claims the standard relativistic velocity-addition formula follows from CA primitives. Our exact dispersions let us derive a closed-form velocity-addition law for 2D-square / BCC QCAs and compare it to the Einstein form.

**Proposed test.** Symbolic derivation (sympy) of velocity addition from $\omega = \arccos(\sqrt{1-m^2}\, c_x c_y)$, then compare to $u' = (u + v)/(1 + uv/c^2)$ in the continuum limit.
**Expected exactness tier.** Closed-form algebraic match in the small-$k$ continuum limit; quantifiable LV residue at higher $k$ (extension of Finding 15).

---

## 9. Caveats and weak points in the paper

A short list of places the argument is hand-wavy or could mislead future work:

- The author's identification $V_P = L_P/T_P = c$ is **numerical, not algebraic** — $L_P/T_P$ is exactly $c$ by *definition* of the Planck units, so Eq. 9.1 is a tautology, not a derivation. The real claim is that the cell-shift rule produces a fixed $c$; our $\omega = \arccos(\cdot)$ derivations are stronger.
- The authors explicitly note (paper p. 20 and §13) that observed $c$ may be **lower** than the raw cell-shift speed due to vacuum scattering. This must be reconciled with our exact $c_\text{lat} = 1/\sqrt d$ result before any quantitative comparison to lab $c$.
- Quantum Inertia is raised "to the level of a postulate" (their words) — it is not derived. Any model element that depends on QI inherits that postulational status.
- The paper conflates "Lorentz transformation" (a global linear map) with "measurement projection from absolute CA units" (a per-observer construction). These are equivalent in the small-$k$ limit only; at the Planck scale the projection picks up the LV residues we already quantify in Finding 15.
- No numerical demonstrations anywhere in the paper. Every claim is conceptual.

---

## 10. Recommended next actions

1. Add a short entry to `findings.md` (new file `findings/F18-flux-rate-relativistic-mass.md`) covering 8.1.
2. Add the four-identity $E = mc^2$ chain (8.3) to `exactness-inventory.md` as a candidate Tier 1 test once implemented.
3. Update `lattice-vs-spacetime-tests.md` with the two-observer measurement projection (8.4) as a pending test.
4. Append a one-line note to `ca-reference.md` linking this summary alongside the existing Ostoma-Trushyk 1999 summary, since the two papers form a pair (CA → SR ; CA → QI/EMQG).

---

## 11. References cited by the paper (selected)

- (1) Ostoma & Trushyk, *ElectroMagnetic Quantum Gravity*, LANL physics/9809042 / APS aps1998sep11_004
- (2) Gutowitz (ed.), *Cellular Automata: Theory and Experiment* (1991) — includes Fredkin, *Digital Mechanics*
- (5) Haisch, Rueda, Puthoff — HRP theory of inertia
- (10) Planck units / scales
- (11) Casimir effect (1948)
- (12) Lamoreaux Casimir measurement
- (19) Inertial-frame definition (textbook)
- (20) Einstein's spherical-wavefront derivation of Lorentz
- (21) A. P. French, *Special Relativity*
- (22) Experimental confirmations of SR
- (23) Modern critiques of SR foundations
