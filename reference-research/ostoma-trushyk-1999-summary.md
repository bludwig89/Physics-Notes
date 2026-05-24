# Cellular Automata Theory and Physics — Ostoma & Trushyk (1999)

**Source:** `Cellular Automata Theory.pdf` (108 pages)
**Authors:** Tom Ostoma and Mike Trushyk, Brampton, Ontario (`emqg@rogerswave.ca`)
**Date:** July 7, 1999
**Subtitle:** *A New Paradigm For The Unification of Physics*

This is a structured summary of significant claims, postulates, equations, and arguments from the paper, organized to map onto this project's existing work (`ca-reference.md`, `cellular-automata-research.md`, `ca-forces-integration.md`, `fredkin-correlation.md`).

---

## 1. Thesis

The universe *is* a Cellular Automaton (CA) — a vast 3D geometric lattice of cells holding numeric state, updated synchronously by a single local rule. All physical phenomena (space, time, matter, forces, motion) are emergent from this computation. The paper proposes a unification of relativity, quantum theory, inertia, and gravity within this paradigm, anchored by a new quantum gravity proposal the authors call **ElectroMagnetic Quantum Gravity (EMQG)**.

Two new theories the authors introduce or develop within this framework:

1. **Quantum Inertia (QI)** — modification of Haisch-Rueda-Puthoff (HRP) inertia (ref. 5 in their paper). Inertia is the electromagnetic resistance of charged matter particles to acceleration relative to the charged virtual particles of the quantum vacuum.
2. **EMQG** — gravity arises from two simultaneous exchange processes (graviton and photon). The photon-mediated component, acting through the accelerated virtual vacuum, dominates and produces the *appearance* of curved 4D space-time.

---

## 2. CA Structure (Postulates Implicit in the Model)

The model assumes a **3D geometric CA** with the following structural rules:

- Each cell stores numeric state.
- Each cell has **26 neighbors** (the immediate cube minus the center cell).
- All cells are updated simultaneously on each **clock cycle**.
- The same local rule $F$ runs in every cell:

$$C_{i,j,k}^{(t+1)} = F\left( \{ C_{i+x,\,j+y,\,k+z}^{(t)} : x,y,z \in \{-1,0,1\} \} \right)$$

- Neighbor count for an $N$-dimensional geometric CA: $C_N = 3 C_{N-1} + 2$.
  $C_1 = 2,\ C_2 = 8,\ C_3 = 26,\ C_4 = 80,\ C_5 = 242$.
- Total number of distinct rules for $N$-D CA with $m$ neighbors and binary cells: $2^k$ where $k = 2^{m+1}$. For 3D ($m=26$) this gives $2^{2^{27}} = 2^{134{,}217{,}728}$ possible rules. **Rule discovery by brute force is impossible.**

### Scale (assuming Planck-unit quantization)

- Cell size $\approx L_P = 1.6\times 10^{-35}$ m.
- Clock period $\approx T_P = 5.4\times 10^{-44}$ s.
- $\approx 10^{105}$ cells per cubic meter; $\approx 10^{43}$ clock cycles per second.

The authors note in §17 that **EMQG's actual quantization scale is finer than the Planck scale** — the Planck units only describe the *observed* lattice spacing after virtual-particle scattering effects.

---

## 3. Two Layers of Space-Time

EMQG distinguishes two distinct space/time measurement systems — this is the conceptual move that lets it reconcile CA absolutism with relativistic observer-dependence:

| Layer | Units | Accessibility |
|---|---|---|
| **Low-level / absolute** | cells (plank distance units, pdu) and clock cycles (plank time units, ptu). Light = 1 cell/clock = 1 plank velocity unit (pvu). | Inaccessible by experiment; only the cells themselves "see" these. |
| **Observable / relativistic** | meters and seconds, measured with matter clocks and rulers. 4D Minkowski space-time, can be curved by motion or gravity. | What we measure. |

A cell address forms a hypothetical absolute rest frame, but it cannot be probed — all observables are made of matter patterns living in the cells.

---

## 4. Why Light Has a Maximum Speed (CA Derivation)

Two structural facts of any CA:

1. Cell state changes only on clock ticks.
2. Information can only propagate one cell per clock cycle (locality of rule input).

Therefore the maximum propagation speed is:

$$V_P = \frac{L_P}{T_P} \approx 3 \times 10^8 \text{ m/s} = c$$

The photon is *postulated* to be the information pattern that always shifts exactly one cell per clock — never faster, never slower. This makes both postulates of Special Relativity follow from CA structure:

- **Constancy of $c$**: because photon shifting is decoupled from source motion.
- **Equivalence of inertial frames**: because all cells and rules are identical everywhere; there is no experimentally accessible preferred frame.

### Lorentz transformation derivation (§7)

Two observers A and B with absolute CA velocities $v_a$ and $v_b$ measure a green photon. In absolute units both find:

$$\frac{d + v\, d}{d + v\, d} = 1\ \text{pvu}$$

— light velocity is invariant in CA units regardless of source motion. When they then compare measurements made with material rulers and clocks (whose periods are themselves defined in terms of light cycles), the comparison reduces to a Doppler analysis in 3D, which when integrated over all directions of a spherical wavefront *is* the Lorentz transformation.

> "Light is a messenger from the shadowy CA world."

### Important EMQG correction (§18)

The "raw" or "low-level" photon velocity $c_r$ between scattering events is the true 1 cell/clock invariant. The **measured** light speed $c$ is reduced by photon scattering with virtual particles:

$$c = \frac{c_r}{n}, \qquad n \gg 1$$

where $n$ is the index of refraction of the quantum vacuum. The actual value of $c_r$ is unknown but is much larger than $c$.

---

## 5. The Quantum Vacuum (§3)

The vacuum is not empty. Per QED it is filled with continuously appearing/annihilating virtual particle pairs (electron-positron, etc.) plus zero-point electromagnetic fluctuations (Nernst 1916). Experimental evidence cited:

- **Casimir effect**: $F/A = -\pi^2 \hbar c / (240\, D^4)$ N/m². Measured by Lamoreaux to ~5% accuracy at $D = 0.75\ \mu$m.
- Hyperfine structure of hydrogen and anomalous magnetic moment of $e^-, \mu$ (QED, ~10-digit accuracy).
- **Vacuum polarization** measured directly by Koltick et al. at 58 GeV: effective $\alpha$ = 1/129.6 vs theoretical 1/128.5.
- Liquid helium does not freeze at zero kelvin (vacuum fluctuations).
- Spontaneous photon emission in atoms.
- Electronic noise floor.
- Cavity QED experiments.

Density estimate: at least $10^{90}$ virtual particles per cubic meter.

The vacuum is treated as central to inertia, gravity, and 4D curvature — far more central than in the standard view.

---

## 6. Quantum Inertia (§8) — the third postulate of EMQG

**Origin:** Modification of Haisch, Rueda & Puthoff (Phys. Rev. A, Feb 1994), in which inertia is the magnetic Lorentz force on "parton" particles bound as Planck oscillators interacting with the EM zero-point field of an accelerating frame.

**EMQG modification:** Replace "parton" with a new fundamental particle, the **masseon** (see §7). The masseon is the lowest quantum of mass and electric charge; comes in particle/anti-particle form with both charge sign and "mass charge" sign reversed.

**Postulate (QI):** The state of relative acceleration of the charged virtual particles of the quantum vacuum with respect to a mass is what produces inertial force. Equivalently:

> Inertia is the sum of all the tiny electromagnetic forces (from photon exchanges) between each charged particle of the mass and the surrounding accelerating charged virtual vacuum particles.

Newton's $F = M A$ becomes the macroscopic sum of these microscopic EM force exchanges. Constant-velocity motion has zero net inertial force because the vacuum's acceleration vectors sum to zero in that frame.

### Mach's principle (§10.1)

QI resolves Mach: the reference frame that "tells" an accelerated mass that it is accelerating is the local vacuum, not the distant stars. Mach was partly right — the distant stars *do* slightly perturb the local vacuum's acceleration state via long-range graviton exchange, but in our solar system the local gravitational sources dominate.

### Newton's three laws as QI consequences (§10.2)

1. **First law** (inertia): a mass at zero acceleration relative to the vacuum experiences no force → constant velocity preserved.
2. **Second law** ($F = ma$): the QI vacuum-resistance force.
3. **Third law** ($F_{12} = -F_{21}$): direct consequence of the boson exchange paradigm; both bodies are simultaneously emitters and absorbers.

---

## 7. Three Mass Definitions (§9)

EMQG distinguishes three masses where conventional physics uses one:

| Mass type | Definition | Notes |
|---|---|---|
| **Inertial mass** $m_i$ | From $F = ma$ — resistance to acceleration via vacuum EM coupling. | Absolute. = rest mass in SR. |
| **Gravitational mass** $m_g$ | From $F = G M_1 M_2 / r^2$ — what a scale measures. | Almost equal to $m_i$; differs at ~$10^{-40}$ precision. |
| **Low-level "mass charge"** | Pure graviton-emission rate (analogous to electric charge). | Not directly measurable; swamped by EM interactions with the vacuum. |

**Photons and gravitons** carry inertial and gravitational mass (via $E/c^2$) but carry **no** low-level mass charge. They do not emit/absorb gravitons. This resolves the canonical-quantum-gravity renormalization tangle (graviton-graviton exchange).

### Photon's effective mass

$$m_p = E/c^2$$

is purely an inertial measurement — comes from momentum transfer at the QED vertex when the photon is absorbed by an electron. The authors give a short derivation of $E = mc^2$ purely from quantum relations:

$$p = mc,\quad c = \nu\lambda,\quad E = h\nu,\quad \lambda = h/p$$

$$\Rightarrow\ \frac{c}{\nu} = \frac{h}{p} = \frac{h}{mc}\ \Rightarrow\ \frac{c}{E/h} = \frac{h}{mc}\ \Rightarrow\ E = mc^2$$

— much simpler than Einstein's light-box derivation.

---

## 8. Relativistic Mass — Reinterpreted (§12)

Standard SR: $m = m_0 / \sqrt{1 - v^2/c^2}$ to preserve momentum conservation.

EMQG reinterpretation: mass is absolute; **force** varies with relative velocity because the exchange-particle *flux* received by a receding target is time-dilated:

$$\Phi_b = \Phi_a \sqrt{1 - v^2/c^2}\ \Rightarrow\ F = F_0 \sqrt{1 - v^2/c^2}$$

Operationally indistinguishable from $m = m_0 / \sqrt{1 - v^2/c^2}$, but conceptually it relocates the relativity into the exchange process, preserving an absolute mass. As $v \to c$, the exchange flux $\to 0$ and force becomes ineffective — this is *why* nothing can be accelerated past $c$.

---

## 9. EMQG — ElectroMagnetic Quantum Gravity (§17)

### Why "electromagnetic"

Two reasons:
1. The photon plays a *dominant* role in gravitational interactions on the Earth — bulk of the force at the test mass is EM, not gravitonic. Ratio of EM to graviton force strength: ~$10^{40}$.
2. The graviton particle is physically nearly identical to the photon — same quantum numbers, vastly different coupling.

### Mechanism

- Real masses emit gravitons at a fixed rate (the "mass charge" — analog of electric charge in QED).
- Gravitons exchanged with the charged virtual particles of the vacuum cause those virtual particles to accelerate downward (toward the mass).
- The accelerating charged virtual particles then exert EM forces on the charged particles of any nearby test mass, via the same QI mechanism that produces inertia.
- This EM coupling is what we observe as ordinary gravity.

### Equivalence principle as a *coincidence*

The principle of equivalence is not fundamental in EMQG. It arises because the *vacuum state appears the same* in two physical situations:

- **Rocket at 1g**: mass particles accelerate relative to a stationary vacuum.
- **Earth at rest**: vacuum particles accelerate (downward) relative to the stationary mass particles.

The directions of the acceleration vectors are reversed, but the magnitudes of the resulting EM-summation forces are the same. This is the WEP.

### Prediction: equivalence is NOT exact

The pure graviton exchanges between Earth and the test mass slightly upset the equivalence for unequal test masses:

> A very large and very small mass dropped together near Earth: **the larger arrives slightly sooner**. Imbalance is of order $10^{-40}$ — currently below experimental sensitivity.

Strong equivalence breaks down with hypothetical graviton detection (gravitational fields contain gravitons, accelerated rockets do not) and with radiation from uniformly accelerated charges (cite: ref. 20).

### Negative "mass charge"

EMQG postulates negative mass charge, carried by anti-particles. The vacuum contains roughly equal numbers of positive and negative mass-charged virtual particles — explaining why the cosmological constant is small (ref. 36).

---

## 10. EMQG Field Equations (§15, §19)

In the weak-field limit, replace Einstein's tensor equation with a modified Poisson equation in absolute CA coordinates:

$$\nabla^2 \phi - \frac{1}{c^2}\frac{\partial^2 \phi}{\partial t^2} = 4\pi G\, \rho(x,y,z,t) \tag{15.2}$$

The acceleration vector of an average virtual particle at $(x,y,z)$ is the gradient of the potential:

$$\mathbf{a} = \nabla\phi \tag{15.3}$$

For an arbitrary high-speed mass distribution, the retarded EMQG potential is:

$$\phi_R(\mathbf{x},t) = -G \int \frac{\rho(\mathbf{y},\,t - r/c)}{r}\, d^3 y, \qquad r = |\mathbf{x}-\mathbf{y}| \tag{19.6}$$

These equations are **not generally covariant** — they are formulated in absolute CA coordinates ($x,y,z$ as cell counts, $t$ as clock-cycle counts). The authors argue Einstein's $G_{\alpha\beta} = (8\pi G/c^2)\, T_{\alpha\beta}$ is the same physics formulated for an arbitrary matter-based observer.

---

## 11. Space-Time Curvature from Photon Scattering (§18)

EMQG's most consequential claim: **4D curvature is not geometric** — it is the cumulative effect of photons (and matter) scattering off the downward-accelerating charged virtual vacuum near a mass.

### Fizeau analog

Fizeau (1851) measured that light velocity in moving water differs from light velocity in stationary water by the Fresnel formula:

$$v_c = \frac{c}{n} + \left(1 - \frac{1}{n^2}\right) V \tag{18.31}$$

This is derived by SR (velocity addition), classically by phase delay in glass (Feynman Lectures Vol. 1 Ch. 31), or via Lorentz semi-classical theory (atomic absorption + re-emission with delay).

EMQG replaces "moving water" with "accelerating quantum vacuum." For $n \gg 1$, the photon's downward acceleration matches the vacuum's:

$$v_c(t) = c\left(1 + \frac{gt}{c}\right) \quad \text{(downward photon)} \tag{18.51}$$

$$v_c(t) = c\left(1 - \frac{gt}{c}\right) \quad \text{(upward photon)} \tag{18.52}$$

This reproduces the gravitational redshift and time dilation of GR without invoking geometric curvature. Curvature becomes an emergent description of scattering through an inhomogeneous accelerating medium.

### Variable-$c$ vs curved geometry — observationally identical

The "ladder thought experiment" in §18.2 shows clearly: you cannot distinguish "$c$ changes" from "space and time change with $c$ constant" by measurement alone. Both produce the same redshift; both produce the same clock drift. Einstein chose the geometric route to preserve his postulate; EMQG chooses the scattering route to preserve absolute CA coordinates.

### Geodesics reinterpreted

The geodesic — the natural force-free path of light or matter — becomes "the path of least scattering resistance through the accelerated vacuum." The vacuum acts as an **electromagnetic guide** that replaces Riemannian geodesic guidance.

---

## 12. Two CA-Compatible Wavefunction Models (§5.1)

Both speculative and incomplete; offered as starting points.

### Model 1 — Direct oscillating numeric pattern
The wavefunction *is* the periodic oscillation of the numeric CA pattern. DeBroglie wavelength $\lambda = h/(mv)$ is the spacing of one oscillation cycle, in cells.

- Unobserved because we cannot read out cell numerics.
- Probabilistic because we cannot know the exact pattern state.
- **Doppler interpretation of motion**: the absolute wavelength on the CA is fixed by the particle's energy. A moving observer sees a Doppler-shifted version. Relative velocity is observer-vs-pattern Doppler, not actual wavelength change.

Problems:
- How a low-energy radio photon (wavelength ~ house-sized = $10^{35}+$ cells) maintains coherence is unclear.
- How the wavefunction "collapses" non-locally is unclear, though the authors note that *low-level* information can propagate at $c_r \gg c$ — so collapse could be much faster than light but not infinite.

### Model 2 — Quantum vacuum bow-wave (Bohm-like)
The particle is a small information pattern; the wavefunction is the wake of disturbed virtual particles surrounding it. Reminiscent of Bohm's pilot wave.

Problems: non-local aspects of Bohm pilot waves are hard to reproduce with strictly local CA disturbance.

---

## 13. Cosmology (§20)

EMQG rejects the standard expanding-spacetime Big Bang for these reasons:

- The CA cannot create or destroy cells, so 4D space cannot "expand."
- The initial singularity (infinite curvature, infinite density) is incompatible with discrete finite cells.

Alternative narrative:
- The cells pre-exist the Big Bang ("hardware" is outside our universe).
- There is a **"Matter Creation Era"** — vast virtual/real particle pair production in the early universe from some violent initial energy. Particles end up with a broad distribution of high velocities.
- Hubble redshift is reinterpreted as a **Milne kinematic cosmology** (Milne 1934, ref. 43): outward inertial motion of matter through pre-existing flat low-level CA space.
- Apparent "expansion of space" is the changing curvature of light's path through the accelerating vacuum — itself a function of overall matter density, which decreases as matter spreads out.

The authors acknowledge Milne cosmology violates the strict cosmological principle (isotropy seen by all observers), but they don't consider this a fatal objection.

---

## 14. Block Diagram (Fig. 8) — How the pieces fit

```
         CELLULAR AUTOMATA PARADIGM
                    |
        +-----------+-----------+
        |                       |
    Special Relativity    Quantum Field Theory / QED
        |                       |
        |          +------------+------------+
        |          |                         |
        |   VIRTUAL PARTICLES OF VACUUM   BOSON EXCHANGE
        |   (electrically- and mass-      PARADIGM
        |    charged "masseons")              |
        |          |                          |
   +----+----+     |                +---------+----------+
   |         |     |                |                    |
Newton's   Mach's QUANTUM INERTIA   PHOTON           GRAVITON
 Laws    Principle (photon-mediated  exchange         exchange
                   vacuum resistance) (EM force)      (gravity)
                              \      /
                               \    /
                            EMQG THEORY
                                 |
                          Equivalence Principle
                                 |
                   General Relativity (as observer-
                   dependent emergent description)
```

---

## 15. Postulates of EMQG (Consolidated)

Scattered across §7, §8, §17, §18 — gathering them for clarity:

1. The universe is a 3D geometric CA (26-neighbor) with synchronous local rule.
2. Photons shift exactly 1 cell per clock cycle — they are the maximum-speed information pattern at the raw, low-level scale.
3. **Quantum Inertia**: inertial force is the EM-sum of all photon exchanges between a mass's charged particles and the accelerating charged virtual particles of the vacuum.
4. **Photon scattering postulate**: photons are continually absorbed and re-emitted by charged virtual particles; near a mass, this couples photon motion to the vacuum's downward acceleration via a Fizeau-like process. The time delay between absorption and re-emission is constrained by the uncertainty principle: $\Delta E\, \Delta t > \hbar/2$.
5. **Graviton exchanges**: pure gravitational force is graviton-mediated between particles carrying "mass charge"; gravitons do not self-interact (analogous to photons not self-interacting in QED).
6. The **masseon** is the fundamental quantum of mass and electric charge. Anti-masseons carry reversed signs of both charges. All real particles (electrons, quarks) are composites of masseons.

---

## 16. What the Theory Explains (Mapped to Project Criterion)

The project criterion (per `CLAUDE.md`) is that a new theory must explain existing scientific measurements and either explain them better or extend beyond them. Tracking what Ostoma & Trushyk claim to explain:

| Phenomenon | EMQG Account | Conventional Account | Improvement? |
|---|---|---|---|
| Constancy of $c$ | Photon = 1 cell/clock | Postulated | Mechanism, not postulate |
| Lorentz transforms | Derived from photon CA motion | Derived from $c$ postulate | Same predictions, deeper origin |
| Maximum speed | Hard-coded structural CA limit | Postulated | Mechanism, not postulate |
| $E = mc^2$ | Derived from $p=mc, E=h\nu, \lambda=h/p$ | Light-box thought exp | Shorter derivation |
| Relativistic mass | Force varies, mass absolute | Mass varies | Operationally identical |
| Inertia | EM resistance to accel through vacuum | $F=MA$ postulated | Microscopic mechanism |
| Mach's principle | Vacuum is local Newtonian "absolute space" | Unresolved | Resolved |
| WEP ($m_i = m_g$) | Vacuum looks same in two scenarios | Postulated | Mechanism + predicts violation at $10^{-40}$ |
| Gravitational redshift / time dilation | Photon scatters off accelerating vacuum | 4D curvature | Same observations, different ontology |
| Light bending in gravity | Fizeau-like vacuum scattering | Geodesic in curved space-time | Same observations, different ontology |
| Casimir effect | Standard vacuum-mode-restriction | Standard | No change |
| Cosmological redshift | Milne kinematic + vacuum acceleration | Expanding 4D space-time | Alternative interpretation |
| Cosmological constant | Vacuum mass-charge cancels (ref. 36) | Open problem | Claimed resolution |

**Novel testable predictions** (extending beyond):
- WEP violation at ~$10^{-40}$ accuracy (currently untestable).
- Graviton detection would distinguish gravitational from accelerated frames.
- Radiation from accelerated charges in static gravitational fields (per Parrott, ref. 20).

---

## 17. Connection to This Project

| This project's file | Topic | EMQG relation |
|---|---|---|
| `ca-reference.md` | Weyl spinor CA, split-step FFT, $\psi = (f,g) \in \mathbb{C}^2$ | EMQG works at the same 3D geometric CA layer but assigns a different role to the field: not a particle wavefunction but a numeric pattern undergoing EM-mediated scattering. The Weyl-CA approach is closer to ’t Hooft's CA interpretation of QM (see `cellular-automata-research.md`). |
| `cellular-automata-research.md` | Wolfram Physics, ’t Hooft, causal sets, quantum walks | EMQG is more closely Fredkin-lineage (rigid 26-neighbor cubic lattice) than Wolfram-lineage (hypergraph rewrite). It postdates Fredkin's Digital Mechanics by ~10 years and pre-dates Wolfram (2002) by ~3 years. |
| `ca-forces-integration.md` | CA rules and the four forces | EMQG offers two specific force-particle exchanges (photon and graviton) compatible with the CA rule layer. |
| `fredkin-correlation.md` | Fredkin's Digital Mechanics | EMQG cites Fredkin (refs. 2, 25) as direct lineage. |
| `Digital Mechanics - Edward Fredkin.pdf` | Source document | EMQG explicitly builds on Fredkin's CA-as-physics program. |

---

## 18. Honest Limitations Stated in the Paper

The authors are forthright about what is *not* shown:

- The actual CA rule for our universe is unknown; rule space is $2^{2^{27}}$, brute force impossible.
- No CA has been found whose patterns exactly mimic real elementary particles (the closest is Conway "glider" $\approx$ photon, "gun" $\approx$ charge — both poor analogies).
- The interaction physics of QI (why constant velocity gives zero net force but acceleration gives Newton's $F=MA$) is "raised to the level of a postulate" rather than derived.
- The two wavefunction models in §5.1 are speculative and have unresolved problems (non-locality, large-wavelength coherence).
- No detailed model of how the masseon binds into electrons, quarks, etc.
- The mass hierarchy problem is unsolved; the authors speculate on relativistic masseon orbits.
- The quantum field theory of graviton-masseon interactions is not developed.
- Milne kinematic cosmology violates the strict cosmological principle.

---

## References cited that may warrant follow-up

- (1) Ostoma & Trushyk, *Electromagnetic Quantum Gravity* (1998), arXiv:physics/9902035 — the long-form EMQG paper.
- (3) Ostoma & Trushyk, *Special Relativity Derived from Cellular Automata Theory* (1998), arXiv:physics/9902034.
- (5) Haisch, Rueda & Puthoff, *Inertia as a Zero-Point-Field Lorentz Force*, Phys. Rev. A, Feb 1994 — the original (un-modified) HRP inertia paper.
- (25) Fredkin, *Digital Mechanics: An Informational Process based on Reversible Cellular Automata*, Physica D 45 (1990) 254-270.
- (35) Ostoma & Trushyk, *What are the Hidden Quantum Processes Behind Newton's Laws?* (1999), arXiv:physics/9904036.
- (36) Ostoma & Trushyk, *The Problem of the Cosmological Constant* (1999), arXiv:physics/9903040.

---

*Summary produced 2026-05-15 from `Cellular Automata Theory.pdf`. Page references in the form "§N" correspond to the section numbers used in the paper itself.*
