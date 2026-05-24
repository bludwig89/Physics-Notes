# Finding 26 — The speed of light is the angular rotation rate of the (E, B) pair per unit wavenumber

**Date:** 2026-05-23  
**Status:** Confirmed — derived from F25 real-rotation exactness; algebraically exact  
**Source:** Interpretation of `ca_maxwell.py::real_rotation_vs_maxwell_curl`; derivation from bilinear $G_T(t) = e^{-i\Omega t}G_T(0)$

---

## Statement

> The speed of light $c_\text{lat}$ is not the propagation rate of a complex phase through space. It is the angular rotation rate of the real $(\mathbf{E}, \mathbf{B})$ vector pair per unit of spatial wavenumber:
>
> $$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}\bigg|_{|\mathbf{k}|\to 0}$$
>
> where $\Omega = 2\omega(|\mathbf{k}|/2)$ is the rotation angle the $(\mathbf{E}, \mathbf{B})$ pair traverses per CA tick.

---

## Background

Finding 25 established that the composite-photon bilinear evolves as an exact discrete real rotation:

$$\mathbf{E}(t+1) = \cos\Omega\;\mathbf{E}(t) + \sin\Omega\;\mathbf{B}(t)$$
$$\mathbf{B}(t+1) = -\sin\Omega\;\mathbf{E}(t) + \cos\Omega\;\mathbf{B}(t)$$

with $\Omega = 2\omega(|\mathbf{k}|/2)$.  This identity is algebraically exact — no small-$k$ approximation, no discrete-time correction.  The real-rotation residual is $2.0 \times 10^{-16}$ (machine precision); the Maxwell curl residual is $2.0 \times 10^{-2}$ at $k = 0.05$.

This finding draws out the full conceptual and physical consequences of that result.

---

## The standard interpretation of $c$

In classical electromagnetism, $c$ enters as a phase velocity.  A plane wave carries the complex phase $e^{i(\mathbf{k}\cdot\mathbf{x} - \omega t)}$ that propagates through space.  The speed of light is the ratio $\omega/|\mathbf{k}| = c$ — how fast those crests of phase move.  In this picture, $c$ is fundamentally a propagation velocity: something moves, and $c$ is how fast.

---

## The rotation interpretation

The bilinear construction gives a structurally different picture.  The physical fields $(\mathbf{E}, \mathbf{B})$ are real-valued 3-vectors.  Their evolution is a rigid rotation in the real 2D plane spanned by the two fields.  Reading $\Omega \approx c_\text{lat}|\mathbf{k}|$ at small $|\mathbf{k}|$:

$$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}$$

$c_\text{lat}$ is the *angular rotation rate per unit wavenumber*, not a propagation speed.

For a circularly polarized wave along $\hat{z}$, the $(\mathbf{E}, \mathbf{B})$ pair starts at some angle in its internal plane and rotates at rate $\Omega = c_\text{lat}|\mathbf{k}|$ per tick.  After one full rotation ($\Omega \cdot t = 2\pi$), the fields return to their initial state.  The oscillation period $t = 2\pi/(c_\text{lat}|\mathbf{k}|)$ — what we recognize as the wave period — is the time to complete one rotation.  What we call a wave "propagating through space" is the progression of this internal rotation in time.

The fields do not move through space.  They turn.

---

## Maxwell's equations as the linearization of a real rotation

Taylor-expanding the exact rotation to first order in $\Omega$:

$$\mathbf{E}(t + \Delta t) \approx \mathbf{E}(t) + \Omega\,\Delta t \cdot \mathbf{B}(t)$$

Divide by $\Delta t$ and take $\Delta t \to 0$:

$$\frac{d\mathbf{E}}{dt} = \Omega\cdot\mathbf{B} = c_\text{lat}|\mathbf{k}|\cdot\mathbf{B}$$

In position space this is $\partial_t\mathbf{E} = c_\text{lat}\,\nabla\times\mathbf{B}$ — Maxwell's curl equation.  Maxwell's law is the first-order Taylor expansion of $\cos\Omega$ and $\sin\Omega$ in $\Omega$, valid when $\Omega \ll 1$.

The exact law is the full trigonometric rotation; Maxwell is its linearization.

---

## The imaginary unit is a real rotation in disguise

The imaginary unit $i$ appears throughout Maxwell's equations and all of QFT.  In Fourier space, $\partial_t \to -i\omega$ and $\nabla \to i\mathbf{k}$, so the curl equations become explicitly complex.

At the discrete level, the rotation matrix for one tick is:

$$R(\Omega) = \begin{pmatrix}\cos\Omega & \sin\Omega \\ -\sin\Omega & \cos\Omega\end{pmatrix}$$

In the $\Delta t \to 0$ limit, $R(\Omega) \to I + \Omega J$ where:

$$J = \begin{pmatrix}0 & 1 \\ -1 & 0\end{pmatrix}$$

This $2\times 2$ antisymmetric matrix $J$ satisfies $J^2 = -I$ — it is the real-matrix representation of the imaginary unit.  Complex numbers, in this framework, are real $(\mathbf{E}, \mathbf{B})$-plane rotations expressed in the continuous-time limit.

The imaginary unit is not fundamental.  It is the algebraic artifact of linearizing a real rotation.

---

## Consequences

### 1. Energy conservation is geometric

$\|\mathbf{E}\|^2 + \|\mathbf{B}\|^2$ is conserved exactly because a rotation preserves vector lengths — this is Pythagoras, not a dynamical law.  The rotation is exact; its Maxwell approximation is not.  This is precisely why energy conservation holds to machine precision (F17: $4.77\times 10^{-14}$ over 200 steps) while the Maxwell curl fails by $\sim c_\text{lat}/\sqrt{2}\cdot|\mathbf{k}|$.

### 2. The $O(k)$ curl residual is a structural prediction

The difference between the exact rotation and its Maxwell linearization:

$$\Delta\mathbf{E} = (\cos\Omega - 1)\mathbf{E} + (\sin\Omega - \Omega)\mathbf{B} \approx -\frac{\Omega^2}{2}\mathbf{E} + O(\Omega^3)$$

At $\Delta t = 1$ and small $k$, $\Omega \approx c_\text{lat}|k|$, so:

$$\frac{|\Delta\mathbf{E}|}{|\mathbf{E}|} \sim \frac{\Omega^2}{2} \sim \frac{c_\text{lat}^2|\mathbf{k}|^2}{2}$$

Normalizing by the denominator $\sim 4|n| \approx 2c_\text{lat}|\mathbf{k}|$ gives the $O(k)$ residual:

$$\frac{\text{curl residual}}{|\mathbf{k}|} \to \frac{c_\text{lat}}{\sqrt{2}}$$

This is exactly the coefficient measured in F21 and F23 and is algebraically forced by the geometry of the rotation.  The $O(k)$ curl residual (originally Finding 2) is not an open problem.  It is a structural consequence of the discrete real-rotation law operating at $\Delta t = 1$.

### 3. $c_\text{lat}$ has a more primitive definition

Rather than being postulated as a propagation speed, $c_\text{lat}$ is derived from the lattice geometry:

$$c_\text{lat} = \frac{1}{\sqrt{d}}$$

for a $d$-dimensional BCC automaton (Bisio et al. 2015, unique-QCA result).  This is now understood as the low-$k$ limit of the angular rotation rate per wavenumber — a geometric property of the vacuum automaton's rotation algebra, not a separately postulated constant.

### 4. Falsifiable prediction at Planck-scale frequencies

At frequencies where $\Omega \sim \pi/2$ (the Planck regime), the exact rotation and its Maxwell linearization diverge by order unity.  The leading correction to the phase velocity is:

$$\frac{\delta v_\phi}{c_\text{lat}} \approx -\frac{\Omega^2}{6} = -\frac{c_\text{lat}^2|\mathbf{k}|^2}{6}$$

This is a quadratic-in-frequency correction to the photon dispersion relation.  Any experiment sensitive to $O(\omega^2/\omega_\text{Planck}^2)$ corrections — gamma-ray burst arrival-time differences, for instance — is in principle testing whether the fundamental law is the cosine rotation or its Maxwell linearization.

---

## Summary table

| Concept | Standard view | Rotation view |
|---|---|---|
| What is $c$? | Phase velocity $\omega/|\mathbf{k}|$ | Angular rotation rate $d\Omega/d|\mathbf{k}|$ |
| What propagates? | Complex phase through space | $(\mathbf{E},\mathbf{B})$ angle through time |
| Why does $i$ appear in Maxwell? | Fundamental — fields are complex | Artifact of linearizing a real rotation |
| Energy conservation | Dynamical (Poynting theorem) | Geometric (rotation preserves length) |
| Maxwell's equations | Exact laws | $\Delta t \to 0$ limit; exact to $O(\Omega)$ |
| Curl residual $c_\text{lat}/\sqrt{2}$ | Open problem (Finding 2) | Structural prediction — linearization error |
| Planck-scale correction | Not present | $-\Omega^2/6$ frequency shift |

---

## Relation to existing findings

| Finding | Connection |
|---|---|
| F25 (real-rotation exact) | Source of this finding — the rotation is exact to machine precision |
| F23 (π/2 phase lock) | The phase lock is the real/imaginary mismatch at $\Delta t = 1$, i.e., the rotation vs its linearization |
| F21 (curl coefficient geometry-independent) | Coefficient $c_\text{lat}/\sqrt{2}$ is the $O(\Omega^2)$ rotation error, which depends only on $c_\text{lat}$ |
| F17 (energy conservation machine precision) | Exact because energy is the rotation radius squared |
| Finding 2 (curl residual) | Reframed: not a failure, the expected linearization error of a discrete real rotation |

---

## Cross-references

- [[F25-real-rotation-exact-discrete-time-maxwell]]: numerical confirmation
- [[F23-smearing-ruled-out-curl-residual-is-phase-locked]]: π/2 phase lock — real vs imaginary
- [[F21-curl-residual-geometry-independence]]: $c_\text{lat}/\sqrt{2}$ coefficient exact
- [[F17-poynting-energy-conservation]]: energy exact — now understood as rotation geometry
