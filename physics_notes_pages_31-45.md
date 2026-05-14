# Physics Notes — Pages 31–45 (Transcribed)

Source: `physics_notes_0708.pdf`, pages 31–45.

---

## Page 31 — Motivation & Development of the σ-Matrices

The standard field equation for a scalar field is

$$\partial_\mu \partial^\mu \psi = 0 = (\partial_0^2 - \nabla^2)\psi$$

Generalizing to a non-Lorentzian metric,

$$g_{\mu\nu}\,\partial^\mu \partial^\nu \psi = 0$$

Now, in going to spinors, an operator $\sigma^\mu \partial_\mu$ is proposed such that

$$\sigma^\mu \partial_\mu \psi = 0$$

is the equivalent wave equation, and

$$(\sigma^\nu \partial_\nu)(\sigma^\mu \partial_\mu \psi) = 0$$

is just

$$(\partial_0^2 - \nabla^2)\psi = 0$$

*Margin:*

$$\tilde\sigma_\nu = \begin{cases} +\sigma & \nu = 0 \\ -\sigma & \nu = 1,2,3 \end{cases} \qquad$$

*Spatially reflected version:*
$$\tilde\sigma = \begin{cases} -\sigma & \nu = 0 \\ \sigma & \nu = 1,2,3 \end{cases}$$

This leads to equations for $\sigma$:

$$(\sigma^0)^2 = 1$$

$$(\sigma^i)^2 = 1$$

$$\sigma^\nu \sigma^\mu + \sigma^\mu \sigma^\nu = 0 \quad (\mu \neq \nu)$$

*Verifying that the system is self-consistent:*

$$(-\sigma^0 \partial_0 - \sigma\cdot\nabla)(\sigma^0 \partial_0 - \sigma\cdot\nabla)\psi$$

$$\big(-\partial_0^2 \psi - (\sigma\cdot\nabla)(\sigma_0 \partial_0) + (\sigma_0\partial_0)(\sigma\cdot\nabla) + (\sigma\cdot\nabla)^2\big)\psi$$

$$\tfrac{1}{2}(\sigma_\mu \tilde\sigma_\nu + \sigma_\nu \tilde\sigma_\mu)\,\partial^\mu \partial^\nu \psi = 0 \qquad \text{(symmetrized form)}$$

With $\sigma_\mu = (\sigma_0, \vec\sigma)$ and $\tilde\sigma_\mu = (\sigma_0, -\vec\sigma)$, then

$$\sigma_i \sigma_j + \sigma_j \sigma_i = 0 \qquad$$

$$\tfrac{1}{2}(\sigma_\mu \sigma_\nu + \sigma_\mu \sigma_\mu) = \mathbb{1} \qquad$$

$$\sigma_0 \sigma_i - \sigma_i \sigma_0 = 0 \qquad$$

---

## Page 32 — Question

If $g^{\mu\nu}$ is the Lorentz metric, does this force $q^\mu = \sigma^\mu$? Plainly, no:

$$g^{\mu\nu} = \tfrac{1}{2}\!\left(q^\mu \tilde q^\nu + q^\nu \tilde q^\mu\right)$$

$\sigma^\mu$ forms a Hermitian basis of $2 \times 2$ matrices, so

$$q^\mu = q^\mu_{\,0}\,\sigma^0 - q^\mu_{\,1}\,\sigma^1 - q^\mu_{\,2}\,\sigma^2 - q^\mu_{\,3}\,\sigma^3$$

$$\tilde q^\mu = q^\mu_{\,0}\,\sigma^0 + q^\mu_{\,1}\,\sigma^1 + q^\mu_{\,2}\,\sigma^2 + q^\mu_{\,3}\,\sigma^3$$

---

## Page 33 — Lagrangian Approach to Sachs Electrogravity

Here we will write a Lagrangian for Sachs Electrogravity with two matter fields, and solve for the equations of motion.

$$\mathcal{L} = (-g)^{1/2}\!\left\{\, R + \tfrac{1}{2}\!\left[\,i\eta^{+} q^\mu \eta_{j\mu} - i\eta^{+}_{i\mu}\, q^\mu \eta\,\right] + \tfrac{1}{2}\!\left[\,i\chi^{+}\, \tilde q^\mu \chi_{i\mu} - i\chi^{+}_{j\mu}\, \tilde q^\mu \chi\,\right]\right\}$$

Where

$$\eta_{i\mu} \equiv \partial_\mu \eta + \Omega_\mu\, \eta$$

$$\chi_{j\mu} \equiv \partial_\mu \chi + \Omega_\mu^{(\chi)}\, \chi$$

and

$$\Omega_\mu^{(\chi)} = -\Omega_\mu^{+}$$

$$\sigma^0 g^{\mu\nu} = \tfrac{1}{2}(q^\mu \tilde q^\nu + q^\nu \tilde q^\mu) \qquad g \equiv -\det g_{\mu\nu}$$

$$R = \tfrac{1}{4}\mathrm{Tr}\!\left(K_{\mu\nu}\, q^\mu \tilde q^\nu - K_{\nu\mu}\, q^\mu q^\nu + q^\mu K^{+}_{\mu\nu}\, q^\nu - q^\nu K^{+}_{\mu\nu}\, \tilde q^\mu\right)$$

$$K_{\mu\nu} \equiv \Omega_{\nu{i}\mu} - \Omega_{\mu{i}\nu} = \partial_\mu \Omega_\nu - \partial_\nu \Omega_\mu + \Omega_\mu \Omega_\nu - \Omega_\nu \Omega_\mu$$

In curved spacetime, the Lagrangian equations of motion are

---

## Page 34

$$\left(\frac{\partial \mathcal{L}}{\partial \psi_{;\mu}}\right)_{\!;\mu} - \frac{\partial \mathcal{L}}{\partial \psi} = 0$$

for each independent field variable $\psi$. Here we will treat $q^\mu$, $\Omega_\mu$, $\eta$ and $\chi$ as independent field variables and derive the equations of motion for them.

*(Remainder of page blank.)*

---

## Page 35 — Cellular Automata & Spacetime Geometry (Speculation)

Would it be possible to model spacetime geometry and elementary particle physics using cellular automata?

In other words: links of cells to one another, and their behavior according to those links, leads to geometry, etc.?

Geometry from rules of interaction is implicit in cellular automata rules. For example, in the game of life, a cell is turned on or off depending on its neighbors:

```
      [ 2 ]
[ 1 ] [ A ] [ 3 ]
      [ 4 ]
```

The state of $A$ in the next time increment depends on the state of $A$, 1, 2, 3 & 4 *now*. But, that $A$ depends on 1, 2, 3 & 4 and *not* 23, 47, 217, 1098 **implies** that 1, 2, 3 & 4 are neighbors. And the lists of all neighbors creates a 2D lattice geometry.

> **Dependence implies neighborhood. Rules imply geometry.**

Has anything been written about this? How could we create a cellular automaton that generates a Lorentzian geometry? Could they also generate a time coordinate?

---

## Page 36 — Dimensionality from Connection Number

It would appear that a CA can only establish a certain dimensionality based on the number of connections it can establish.

- A CA with **0 connections** is 0-dimensional.
- A CA with **1 connection** has a sort of 1D structure but cannot form a 1D space.
- CA's with **2 connections** can form 1-dimensional lines & circles.
- CA's with **3 connections** can form a variety of different structures — *Linear Strip, Circular Strip, Möbius Strip*, or 2D lattice.
- **4 connections** can form a 2D lattice or a 3D lattice, or something like a 3D tube or torus.

We could also consider **asymmetric connections** — e.g. if there are two cells $A$ & $B$, the state of $A$ could depend on $B$, but not $B$ on $A$; or $B$ could depend on $A$ in a different way than $A$ on $B$.

---

## Page 37 — Discretized Wave Equation on a CA

For cells to propagate waves / particles they must obey some kind of wave equation, i.e., in 2D,

$$\frac{\partial^2 f}{\partial t^2} - \frac{\partial^2 f}{\partial y^2} - \frac{\partial^2 f}{\partial z^2} = 0$$

where $f$ is in some sense the value of the cell. Presumably we can discretize this by writing

$$\frac{\partial^2 f}{\partial z^2}(x) = \frac{\dfrac{f(x+\Delta x) - f(x)}{\Delta x} - \dfrac{f(x) - f(x-\Delta x)}{\Delta x}}{\Delta x} = \frac{f(x + \Delta x) - 2f(x) + f(x - \Delta x)}{\Delta x^2}$$

etc., or in cellular form,

$$\frac{\partial^2 f}{\partial z^2} \;\to\; f(m,n+1) - 2 f(m,n) + f(m,n-1)$$

so

$$f(m,n,t+1) - 2f(m,n,t) + f(m,n,t-1) = f(m+1,n,t) - 2f(m,n,t) + f(m-1,n,t)$$
$$\quad + f(m,n+1,t) - 2f(m,n,t) + f(m,n-1,t)$$

would be the basic relation, i.e.

$$f(m,n,t+1) = -2f(m,n,t) - f(m,n,t-1) + f(m+1,n,t) + f(m-1,n,t) + f(m,n+1,t) + f(m,n-1,t)$$

The problem with this is that $f(m,n,t+1)$ is *not* dependent just on $f(-,-,t)$ but also on $f(m,n,t-1)$. To get it to depend only on the previous time step we have to make the Dirac reduction and make each cell spinor-valued. Try just a 2-component massless equation:

$$i\hbar \frac{\partial \psi_{+}}{\partial t} = -i\hbar c\, \boldsymbol\sigma \cdot \nabla \psi_{+}$$

---

## Page 38 — Spinor-Valued CA (continued)

With $\hbar = c = 1$,

$$\frac{\partial \psi_{+}}{\partial t} = -\boldsymbol\sigma \cdot \nabla \psi_{+}$$

$$\boldsymbol\sigma \cdot \nabla = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}\frac{\partial}{\partial x} + \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}\frac{\partial}{\partial y} + \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}\frac{\partial}{\partial z}$$

$$\frac{\partial \psi}{\partial t} = \begin{pmatrix} -\partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_z \end{pmatrix} \psi$$

and with $\psi = \begin{pmatrix} f \\ g \end{pmatrix}$,

$$\frac{\partial f}{\partial t} = -\partial_z f - \partial_x g + i\partial_y g$$

$$\frac{\partial g}{\partial t} = -\partial_x f - i\partial_y f + \partial_z g$$

Finite-differencing (centered):

$$\left.\frac{\partial f}{\partial z}\right|_{(x,y,z,t)} \approx \tfrac{1}{2}\!\left(\frac{f(x,y,z+\Delta z, t) - f(x,y,z, t)}{\Delta z} + \frac{f(x,y,z, t) - f(x,y,z - \Delta z, t)}{\Delta z}\right)$$

$$= \frac{1}{2\Delta z}\!\left(f(x,y,z+\Delta z,t) - f(x,y,z-\Delta z,t)\right)$$

giving (with $\Delta = 1$):

$$\boxed{\;\begin{aligned}
f(l,m,n,t+1) - f(l,m,n,t) &= -\tfrac{1}{2}\!\big(f(l,m,n+1,t) - f(l,m,n-1,t)\big) \\
&\quad -\tfrac{1}{2}\!\big(g(l+1,m,n,t) - g(l-1,m,n,t)\big) \\
&\quad +\tfrac{i}{2}\!\big(g(l,m+1,n,t) - g(l,m-1,n,t)\big) \\[4pt]
g(l,m,n,t+1) - g(l,m,n,t) &= -\tfrac{1}{2}\!\big(f(l+1,m,n,t) - f(l-1,m,n,t)\big) \\
&\quad -\tfrac{i}{2}\!\big(f(l,m+1,n,t) - f(l,m-1,n,t)\big) \\
&\quad +\tfrac{1}{2}\!\big(g(l,m,n+1,t) - g(l,m,n-1,t)\big)
\end{aligned}\;}$$

These spinor equations provide relations in which $f(l,m,n,t)$ etc. are dependent only on $t-1$ states — really a 1st-order causal relation.

---

## Page 39 — Numerical Stability Notes

If we made $\Delta x = \Delta y = \Delta z = \tfrac{1}{2}$ while $\Delta t = 1$, then these equations would work with integer-valued complex numbers. I wonder if they're stable.

Let's try to write this in spinor notation:

$$\psi(l,m,n,t+1) = \sigma_0\, \psi(l,m,n,t) - \tfrac{1}{2}\sigma_z\!\big(\psi(l,m,n+1,t) - \psi(l,m,n-1,t)\big)$$
$$\quad - \tfrac{1}{2}\sigma_x\!\big(\psi(\ell+1,m,n,t) - \psi(\ell-1,m,n,t)\big)$$
$$\quad - \tfrac{1}{2}\sigma_y\!\big(\psi(\ell,m+1,n,t) - \psi(\ell,m-1,n,t)\big)$$

> Programming this up certainly does something, but it blows up w/o the $\tfrac{1}{2}$'s there — goes from unity values to values of about 11,000 in ~10 time steps. And, well, $2^{10} = 1024$, so how surprised are we? Putting the $\tfrac{1}{2}$ in brings it down to about 120 — still not ideal.
>
> I wonder if the factor needed to keep it at unity varies much? It "interestingly" seems to stabilize at $\sim 0.43$. In this world, that factor has to do with the speed of light, so to speak. A $\tfrac{1}{2}$ in the above eqn gives $c = 1$. A smaller value gives a smaller $c$. Renormalization of everything sort of like a change of $c$.

---

### Simulation notes (added 2026-05-13)

The equations on pages 37–39 were implemented in Python (`ca-simulation/ca_core.py`) and run to 200 time steps.

**Explicit-Euler scheme (as written on page 38):**
The scheme is unconditionally unstable. Every value of $c$ diverges over a sufficient number of steps; the notebook's observation of ~0.43 as a stabilization threshold reflects only that divergence is slower at lower $c$ — not that there is a true stable region. This is consistent with the general result that explicit Euler applied to a skew-Hermitian operator is always unstable.

**Split-step FFT propagator (derived from the same page 38 equations):**
Each Fourier mode $\mathbf{k}$ is propagated by the exact $2\times2$ unitary:

$$U(\mathbf{k}) = \cos(c\kappa)\,I - \frac{i\sin(c\kappa)}{\kappa}(\boldsymbol\sigma\cdot\mathbf{k}), \qquad \kappa = |\mathbf{k}|$$

This is exactly unitary for all $c$. Results at 200 steps:
- All $c$ values from 0.10 to 0.61 remained stable.
- Time-reversal residuals (100 steps forward, 100 back) were $\sim 6\times10^{-14}$ — machine-precision, independent of $c$.
- Norm $\|\psi\|^2$ was conserved to double precision at every step.

The split-step result confirms the physical content of the page 38 equations: the Weyl CA is unitary and time-reversible. The instability in the notebook was a property of the numerical method, not the physics.

---

## Page 40

*Blank / back-of-page bleed-through only.*

---

## Page 41 — Quantum Hierarchy Equations of a Free Scalar Field (paper, p. 1)

This paper is intended to take up where my dissertation left off and advance the art of numerical quantum field calculations somewhat. Let us start with the simplest possible example, a massive spin-zero field whose equation of motion is

$$\partial_\mu \partial^\mu \phi + m^2 \phi = 0$$

The corresponding Lagrangian density is

$$\mathcal{L} = \tfrac{1}{2}(\partial_\nu \phi)(\partial^\nu \phi) - \tfrac{1}{2} m^2 \phi^2$$

and the Lagrangian field equation is

$$\partial_\nu\!\left(\frac{\partial \mathcal{L}}{\partial \phi_{,\nu}}\right) - \frac{\partial \mathcal{L}}{\partial \phi} = 0, \qquad \phi_{,\nu} \equiv \partial_\nu \phi \qquad \text{(Goldstein 12-23)}$$

The canonical momentum is

$$\pi_\phi \equiv \frac{\partial \mathcal{L}}{\partial \phi_{,0}} = \partial_0 \phi \qquad \text{(Goldstein 12-53)}$$

*(which we hereinafter refer to as $\partial_0 \phi$).*

and the Hamiltonian density is given by

$$\mathcal{H} = \frac{\partial \mathcal{L}}{\partial \phi_{,0}} \partial_0 \phi - \mathcal{L} \qquad \text{(Goldstein 12-50)}$$

so

$$\mathcal{H} = \tfrac{1}{2}\!\left(\pi_\phi^{\,2} + (\nabla\phi)^2 + m^2 \phi^2\right)$$

The Hamiltonian field equations are

$$\phi_{,0} = \frac{\partial \mathcal{H}}{\partial \pi_\phi} \qquad \pi_{,0} = -\frac{\partial \mathcal{H}}{\partial \phi} \qquad \text{(Goldstein 12-62)}$$

To proceed, we must transform the Hamiltonian

$$H \equiv \int \mathcal{H}(x)\, d^3 x$$

to momentum space, for which we must introduce some Fourier transforms. We want to have a measure that will be Lorentz invariant & easily generalizable. For this purpose we diverge from the dissertation and write

---

## Page 42 — (paper, p. 2)

$$\tilde\phi(k) \equiv 2\omega_k \int \phi(x)\, e^{ik\cdot x}\, d^3 x \qquad \nabla\phi(x) = \int -ik\, \tilde\phi(k)\, e^{-ik\cdot x}\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k}$$

$$\phi(x) = \int \tilde\phi(k)\, e^{-ik\cdot x}\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k} \qquad \text{(also for } \pi\text{)}$$

where

$$\omega_k \equiv \sqrt{k^2 + m^2}$$

This gives

$$\phi(x) = \iint \phi(y)\, e^{ik\cdot y}\, e^{-ik\cdot x}\, d^3 y\, \frac{d^3 k}{(2\pi)^3}$$

$$= \frac{1}{(2\pi)^3} \int \phi(y) \!\left[\int e^{ik(y-x)}\, d^3 k\right]\! d^3 y$$

$$= \int \phi(y)\, \delta^3(y - x)\, d^3 y = \phi(x)$$

given that

$$(2\pi)^3\, \delta^3(x) = \int e^{ik\cdot x}\, dk$$

which is the standard definition of the $\delta$-function.

The advantage of this measure is that

$$\int_k \frac{d^3 k}{(2\pi)^3\, 2\omega_k} = \int_{\vec k} \int_{k_0} 2\pi\, \delta(k^2 - m^2)\, \Theta(k_0)\, \frac{d^4 k}{(2\pi)^4} \qquad \text{(IzZ 3.35)}$$

where $\Theta(x) \equiv 1$ if $x \geq 0$, $\equiv 0$ if $x < 0$. This will be useful later.

Now we transform $\mathcal{H}$ to $k$-space:

$$H = \tfrac{1}{2}\int\!\big(\pi^2 + (\nabla\phi)^2 + m^2\phi^2\big)\, d^3 x$$

$$= \tfrac{1}{2}\iiint \frac{1}{(2\pi)^6 (2\omega_k)(2\omega_p)}\,\Big(\tilde\pi(k)\tilde\pi(p) - k\!\cdot\!p\, \tilde\phi(k)\tilde\phi(p) + m^2\, \tilde\phi(k)\tilde\phi(p)\Big)\, e^{-ik\cdot x}\, e^{-ip\cdot x}\, d^3 k\, d^3 p\, d^3 x$$

---

## Page 43 — (paper, p. 3)

The integration over $x$ is given by

$$\int e^{-i(k+p)\cdot x}\, d^3 x = (2\pi)^3\, \delta^3(k+p)$$

so

$$H = \tfrac{1}{2}\iint \frac{1}{(2\pi)^3\, 2\omega_p\, 2\omega_k}\, \delta^3(k+p)\, \Big(\tilde\pi(k)\tilde\pi(p) + m^2\, \tilde\phi(k)\tilde\phi(p) - k\!\cdot\!p\, \tilde\phi(k)\tilde\phi(p)\Big)\, d^3 k\, d^3 p$$

$$= \tfrac{1}{2}\!\int \frac{1}{(2\pi)^3\, 4\omega_k^2}\Big(\big(\tilde\pi(k)\big)^2 + m^2\big(\tilde\phi(k)\big)^2 + k^2\big(\tilde\phi(k)\big)^2\Big)\, d^3 k$$

$$= \frac{1}{8(2\pi)^3}\int \!\left(\frac{\tilde\pi_k^{\,2}}{\omega_k^2} + \frac{m^2 + k^2}{\omega_k^2}\, \tilde\phi_k^{\,2}\right)\! d^3 k \qquad (\ast)$$

Now we want to write $H$ in terms of creation & annihilation operators, $a_k^+$ and $a_k$, where $a_k^+$ creates and $a_k$ annihilates. Then, to quantize, the operators are made to fulfill

$$[a_k, a_p^+] = (2\pi)^3\, 2\omega_k\, \delta^3(k - p) \qquad \text{(IzZ 3.36)}$$

$$[a_k, a_p] = [a_k^+, a_p^+] = 0$$

whereby

$$\phi(x) = \int\!\big(a_k\, e^{ik\cdot x} + a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3 (2\omega_k)} \qquad \text{(IzZ 3.37a)}$$

or

$$\tilde\phi_k = a_k^+ + a_{-k}$$

and

$$\pi(x) = -i \int \omega_k\, \big(a_k\, e^{ik\cdot x} - a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3 (2\omega_k)} \qquad \text{(IzZ 3.37b)}$$

or

$$\tilde\pi_k = i\omega_k\, a_k^+ - i\omega_k\, a_{-k} = i\omega_k\,(a_k^+ - a_{-k})$$

Substituting these into $(\ast)$ above gives

---

## Page 44 — (false-start algebra, crossed out in original)

*The author began the substitution into $(\ast)$ on this page, but crossed the entire calculation out and re-did it on the next page. For completeness:*

$$H \overset{?}{=} \frac{1}{8(2\pi)^3}\int \Big[-(a_k^+ - a_k)^2 + (a_k^+ + a_k)^2\Big]\, d^3 k$$

$$= \frac{1}{8(2\pi)^3}\int\!\Big[\,-a_k^{+\,2} - a_k^{\,2} + 2 a_k^+ a_{-k} + a_k^{+\,2} + a_{-k}^{\,2} + 2 a_k^+ a_k\,\Big]\, d^3 k$$

$$\overset{?}{=} \frac{1}{2(2\pi)^3}\int a_k^+ a_{-k}\, d^3 k \qquad \text{\small (crossed out)}$$

*Marginal note:* "if we assume $a_k$ commute" — also crossed out, as does the trial commutator $a_k a_k^+ - a_k^+ a_k = \delta$.

A separate side-computation of $\phi(x)\phi(y)$ appears:

$$\phi(x)\phi(y) = \iint\!\big(a_k\, e^{ik\cdot x} + a_k^+\, e^{-ik\cdot x}\big)\!\big(a_p\, e^{ip\cdot y} + a_p^+\, e^{-ip\cdot y}\big)\, dk\, dp$$

$$= \iint\!\Big(a_k a_p\, e^{i(k\cdot x + p\cdot y)} + a_k^+ a_p\, e^{i(p\cdot y - k\cdot x)} + a_k a_p^+\, e^{-i(p\cdot y - k\cdot x)} + a_k^+ a_p^+\, e^{-i(k\cdot x + p\cdot y)}\Big)\, dk\, dp$$

$$= \iint\!\Big(a_k a_p + a_{-k}^+ a_p^+ + a_k^+ a_p + a_k a_p^+\Big)\, e^{i(k\cdot x + p\cdot y)}\, dk\, dp$$

*("...note no sense.")*

---

## Page 45 — (paper, p. 4 — clean redo)

$$H = \frac{1}{2(2\pi)^3}\int \frac{1}{4\omega_k^2}\!\Big(\tilde\pi_k \tilde\pi_{-k} + (m^2 + k^2)\, \tilde\phi_k \tilde\phi_{-k}\Big)\, d^3 k$$

$$= \frac{1}{8(2\pi)^3}\!\int \!\left(\frac{\tilde\pi_k\, \tilde\pi_{-k}}{\omega_k^2} + \tilde\phi_k\, \tilde\phi_{-k}\right)\! d^3 k \qquad (\ast)$$

Now we want to write $H$ in terms of creation & annihilation operators, $a_k^+$ and $a_k$ where $a_k^+$ creates and $a_k$ annihilates. These obey commutation relations

$$[a_k, a_p^+] = (2\pi)^3\, 2\omega_k\, \delta^3(k - p) \qquad \text{(IzZ 3-36)}$$

$$[a_k, a_p] = [a_k^+, a_p^+] = 0$$

whereby

$$\phi(x) = \int\!\big(a_k\, e^{ik\cdot x} + a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k} \qquad \text{(IzZ 3.37a)}$$

or

$$\tilde\phi_k = a_k^+ + a_{-k}$$

with the inverses

$$a_k^+ = \tfrac{1}{2}\!\left(\tilde\phi_k - \tfrac{i}{\omega_k}\,\tilde\pi_k\right) \qquad a_{-k} = \tfrac{1}{2}\!\left(\tilde\phi_k + \tfrac{i}{\omega_k}\,\tilde\pi_k\right)$$

and

$$\pi(x) = -i \int \omega_k\, \big(a_k\, e^{ik\cdot x} - a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k} \qquad \text{(IzZ 3.37b)}$$

or

$$\tilde\pi_k = i\omega_k\, a_k^+ - i\omega_k\, a_{-k} = i\omega_k\,(a_k^+ - a_{-k})$$

Substituting these into $(\ast)$ gives

$$H = \frac{1}{8(2\pi)^3}\!\int\!\Big[\, -(a_k^+ - a_{-k})(a_{-k}^+ - a_k) + (a_k^+ + a_{-k})(a_{-k}^+ + a_k)\,\Big]\, d^3 k$$

$$= \frac{1}{4(2\pi)^3}\!\int\!\big(\, a_k^+ a_k + a_{-k}\, a_{-k}^+ \,\big)\, d^3 k$$

$$= \frac{1}{4(2\pi)^3}\!\int\!\big(\, a_k^+ a_k + a_k\, a_k^+ \,\big)\, d^3 k$$

$$\boxed{\; H = \tfrac{1}{2}\!\int \omega_k\,\big(a_k^+ a_k + a_k\, a_k^+\big)\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k}\;} \qquad \text{(Ludwig eq.\ 3)}$$

---

*End of transcription, pages 31–45.*
