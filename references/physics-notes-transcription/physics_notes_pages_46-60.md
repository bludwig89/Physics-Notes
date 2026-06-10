# Physics Notes — Pages 46–60

Source: `physics_notes_0708.pdf`, pages 46–60 of 182.
Continuation of the "Quantum Hierarchy Equations of a Free Scalar Field" paper begun on page 41, then a new entry dated 9/6/2007 on "Complex mass."

---

## Page 46 (notebook page 5)

Then to derive a hierarchy, we go to discrete space by defining

$$a_j = a_{k_j} \frac{d^3k}{(2\pi)^3 2\omega_k}$$

and writing $H$ as a discrete sum over finite volume elements. Then $H$ becomes

$$H = \sum_{j=-p}^{p} \tfrac{1}{2}\,\omega_j\,(a_j a_j^+ + a_j^+ a_j) \tag{$\boxtimes$}$$

which is the free-field case of eq. 7 in Ludwig [i]. Now we write a Schrödinger equation,

$$i \frac{\partial |\psi\rangle}{\partial t} = H |\psi\rangle \qquad \text{(Ludwig eq. 1)} \quad \text{\textcircled{A}}$$

The eigenstates are written as $|n_{-p}\ldots n_j \ldots n_p\rangle$ which represent $n_j$ particles in the $k_j$ state. This is by definition an eigenstate of $H$ with

$$H |n_{-p}\ldots n_p\rangle = \left[\sum_{j=-p}^{p} \left(n_j + \tfrac{1}{2}\right)\omega_j \right] |n_{-p}\ldots n_p\rangle \qquad \text{(Ludwig eq. 4)} \quad \text{\textcircled{B}}$$

Expand a general state

$$|\psi\rangle = \sum_{n_{-p}\ldots n_p = 0}^{\infty} C_{n_{-p}\ldots n_p}\, |n_{-p}\ldots n_p\rangle \qquad \text{(Ludwig eq. 2)}$$

and substitute into Ludwig [a], giving

$$\sum_{n_{-p}\ldots n_p = 0}^{\infty} i \frac{\partial C_{n_{-p}\ldots n_p}}{\partial t}\, |n_{-p}\ldots n_p\rangle \;=\; \sum_{n_{-p}\ldots n_p = 0}^{\infty} \left[\sum_{j=-p}^{p} \omega_j (n_j + \tfrac{1}{2}) \right] C_{n_{-p}\ldots n_p}\, |n_{-p}\ldots n_p\rangle \qquad \text{(Ludwig eq. 3)}$$

By orthogonality of the basis vectors, we write

$$i \frac{\partial C_{n_{-p}\ldots n_p}}{\partial t} = \sum_{j=-p}^{p} \omega_j \left(n_j + \tfrac{1}{2}\right) C_{n_{-p}\ldots n_p} \qquad (\ast\ast) \quad \text{(Ludwig eq. 15)}$$

---

## Page 47 (notebook page 6)

Now write

$$C_{n_{-p}\ldots n_p} = A\,\psi_N(k_1,\ldots,k_N)$$

The constant $A$ is selected so that $|\psi\rangle$ may be understood as a Schrödinger wavefunction with

$$1 = \langle \psi | \psi \rangle = \sum_{N=0}^{\infty} \int \psi_N^*(k_1\ldots k_N)\, \psi_N(k_1\ldots k_N)\, \frac{d^3k_1}{(2\pi)^3 2\omega_{k_1}}\cdots \frac{d^3k_N}{(2\pi)^3 2\omega_{k_N}} \qquad \text{(Ludwig eq. 19)}$$

In discrete terms,

$$\langle \psi | \psi \rangle = \sum_{N=0}^{\infty} \sum_{k_1\ldots k_N = -p}^{p} |\psi_N(k_1\ldots k_N)|^2 \,\prod_{j=1}^{N} \frac{(\Delta k)^3}{(2\pi)^3 2\omega_{k_j}} \qquad \text{(Ludwig eq. 19)}$$

Compare this with the $C$'s, defined such that

$$1 = \langle \psi | \psi \rangle = \sum_{N=0}^{\infty} \sum_{\sum n_j = N} \left| C_{n_{-p}\ldots n_p}\right|^2 \qquad \text{(Ludwig eq. 8)}$$

Whereby (per Ludwig p.22)

$$C_{n_{-p}\ldots n_p} = \psi_N(k_1\ldots k_N) \cdot \sqrt{\frac{(\Delta k)^{3N}}{\prod_{j=1}^{N}(2\omega_{k_j})}\,\frac{N!}{\prod_{j=-p}^{p} n_j!}}$$

Substituting into $\boxtimes$ $(\ast\ast)$, these factors cancel on both sides yielding

$$i \frac{\partial \psi_N(k_1\ldots k_N)}{\partial t} = \left(\sum_{j=-p}^{p} \tfrac{1}{2}\omega_j + \sum_{j=-p}^{p} n_j \omega_j\right)\psi_N(k_1\ldots k_N)$$

$$\qquad = \sum_{j=-p}^{p} \tfrac{1}{2}\omega_j \,\psi_N(k_1\ldots k_N) + \sum_{j=1}^{N} \omega_{k_j}\, \psi_N(k_1\ldots k_N)$$

Now, we can write

$$K = \sum_{j=-p}^{p} \tfrac{1}{2}\omega_j$$

as a constant, dependent only on the lattice (as usual),

---

## Page 48 (notebook page 7)

and then define

$$|\psi'| = e^{-iKt}\, |\psi|$$

so that

$$i \frac{\partial |\psi'|}{\partial t} = K |\psi'| \;+\; e^{-iKt}\left(i\frac{\partial |\psi|}{\partial t}\right)$$

and thus,

$$i \frac{\partial \psi'_N}{\partial t}(k_1\ldots k_N) = \sum_{j=1}^{N} \omega_{k_j}\, \psi'_N(k_1\ldots k_N) \qquad \text{(Ludwig eq. 3)}$$

The constant $K$ is just the vacuum energy, which we have subtracted away. Thus we may drop the prime on $\psi$, and this is the multiparticle state equation for a free scalar boson. It is perhaps not very interesting, but it illustrates a technique, and brings up a number of issues that arise as a result of that technique which are important.

One problem we immediately see here is that this equation cannot easily be converted back to spacetime coordinates. The presence of $\omega_k = \sqrt{k^2 + m^2}$ acts effectively as an operator $\sqrt{m^2 + \nabla^2}$ that cannot be **differentiated** integrated by a Fourier transform. The derivation seems to single out a single time direction, which is not very elegant, ~~first~~ in defining the Hamiltonian, and then in defining the Schrödinger equation. It would be much nicer if it were entirely covariant. Secondly, it is unclear how the bosonic symmetry, which

---

## Page 49 (notebook page 8)

requires

$$\psi_N(k_1,\ldots,k_i,\ldots,k_j,\ldots,k_N) = \psi_N(k_1,\ldots,k_j,\ldots,k_i,\ldots,k_N)$$

is enforced. This is very important and must be understood.

It is to be supposed that some of the issues of coordinate space will be easier to work out with Dirac spinors, as well as issues of a covariant presentation, since the Dirac equation is linear first order in its derivatives, whereas the Klein–Gordon equation can't be written as a 1st order equation in the first place. Thus we will defer these issues to the development of the spinor formulation of these systems. However, it would be good to understand the boson symmetry here now before we try to tackle antisymmetric fermions.

Bose and Fermi statistics are enforced by the commutation relations. Bose particles must have creation and annihilation operators that commute. Fermi particles have operators that anti-commute.

---

## Page 50 (bleed-through / blank)

*Page is blank — only a faint mirror image of pen pressure from the verso shows through. No content to transcribe.*

---

## Page 51

Going from $\text{\textcircled{A}}$ to $\text{\textcircled{B}}$:

$$\mathcal{H} = \tfrac{1}{2}(\pi_j \pi_{-j} + \omega_j^2 \phi_j \phi_{-j})$$

$$i \frac{\partial}{\partial t} |n_{-p}\ldots n_p\rangle = \sum_{j=-p}^{p} \tfrac{1}{2}\,\omega_j\,(a_j a_j^+ + a_j^+ a_j)\, |n_{-p}\ldots n_p\rangle$$

is the Schrödinger equation, where $|n_{-p}\ldots n_p\rangle$ is taken as an eigenstate of $H$.

$$a_k^+ = \tfrac{1}{2}\!\left(\phi_{-k} - \frac{i}{\omega_k}\pi_k\right) \qquad a_k = \tfrac{1}{2}\!\left(\phi_k + \frac{i}{\omega_k}\pi_{-k}\right) \qquad \big[a_k = (a_{-k}^+)^*\big]$$

In quantum theory, $\pi_j = i\hbar\,\dfrac{\partial}{\partial \phi_j}$.

The state $|n_{-p}\ldots n_p\rangle$ is a wave function that is a function of the value of $\phi$ at each $k_j$:

$$|n_{-p}\ldots n_p\rangle = \Psi(\phi_{-p},\ldots,\phi_j,\ldots,\phi_p)$$

Rather than speaking of the value of the field $\phi$ at any point $k_j$, we speak of a probability density of the field at that point, given by

$$P(\phi_j) = \int \Psi^* \Psi\,\bigl(\phi_{-p},\ldots,\phi_p\bigr)\, d\phi_{-p}\cdots d\phi_{j-1}\, d\phi_{j+1}\cdots d\phi_p$$

Now we should get a harmonic oscillator at any point, and if we were sloppy about $k$ and $-k$ we could get it right off — but this is oversimplistic.

$$N_j = a_j^+ a_j \qquad H = \sum \omega_j N_j \qquad a_j a_j^+ - a_j^+ a_j = 0$$

$$a_k^+ a_k = \tfrac{1}{4}\!\left(\phi_k - \frac{i}{\omega_k}\pi_k\right)\!\!\left(\phi_{-k} + \frac{i}{\omega_k}\pi_{-k}\right)$$

$$\qquad\quad = \tfrac{1}{4}\!\left(\phi_k \phi_{-k} - \frac{i}{\omega_k}(\pi_k \phi_{-k} - \phi_k \pi_{-k}) + \frac{1}{\omega_k^2}\pi_k \pi_{-k}\right)$$

It is **overly simplistic** to say $a_k^+ a_k$ are creation & annihilation operators for a "harmonic oscillator."

---

## Page 52

[chain-rule sidebar at the top:]

$x = f(x', y')$

$$\frac{\partial}{\partial x} = \frac{\partial x'}{\partial x}\frac{\partial}{\partial x'} + \frac{\partial y'}{\partial x}\frac{\partial}{\partial y'} = \tfrac{1}{\sqrt{2}}\!\left(\frac{\partial}{\partial x'} + \frac{\partial}{\partial y'}\right)$$

$$a_j^+ a_j = N_j, \qquad a_j |n_{-p}\ldots n_j\ldots n_p\rangle = \sqrt{n_j}\,|n_{-p}\ldots n_j-1\ldots n_p\rangle$$
$$a_j^+ |n_{-p}\ldots n_j\ldots n_p\rangle = \sqrt{n_j+1}\,|n_{-p}\ldots n_j+1\ldots n_p\rangle$$
$$a_j^+ a_j |n_{-p}\ldots n_j\ldots n_p\rangle = n_j\,|n_{-p}\ldots n_j\ldots n_p\rangle$$
$$a_j a_j^+ |n_{-p}\ldots n_j\ldots n_p\rangle = (n_j+1)\,|n_{-p}\ldots n_j\ldots n_p\rangle$$

So $\tfrac{1}{2}(a_j^+ a_j + a_j a_j^+) = (N_j + \tfrac{1}{2})\;\checkmark$.

This gets us from $\boxtimes$ to $\ast\ast$.

$$\mathcal{H} \simeq \frac{\pi_k \pi_{-k}}{\omega_k^2} - \omega_k^2\,\phi_k \phi_{-k}$$

If it were $\pi^2$ and $\phi^2$ we could do harmonic oscillators. As it is, each of these is more like a coupled pair of oscillators. It's like having a system $\psi(x,y) = \cdots$

$$\mathcal{H}\psi = -\hbar^2\frac{\partial^2}{\partial x\,\partial y}\psi(x,y) - \omega_0^2 x y\,\psi(x,y) = E_0\,\psi \quad \text{\textcircled{C}}$$

instead of

$$-\hbar^2\,\frac{\partial^2 \psi}{\partial x^2} + \omega^2 x^2\,\psi(x) = E_0\,\psi$$

What kind of mess is this? What if we rotate $\text{\textcircled{C}}$ $45°$ so that

$$x^* = \tfrac{1}{\sqrt{2}}(x' + y'), \qquad x' = \tfrac{1}{\sqrt{2}}(x + y)$$
$$y^* = \tfrac{1}{\sqrt{2}}(x' - y'), \qquad y' = \tfrac{1}{\sqrt{2}}(x - y)$$

$$xy = \tfrac{1}{2}(x'+y')(x'-y') = \tfrac{1}{2}(x'^2 - y'^2)$$

$$\frac{\partial}{\partial x} = \tfrac{1}{\sqrt{2}}\!\left(\frac{\partial}{\partial x'} + \frac{\partial}{\partial y'}\right) \qquad \frac{\partial}{\partial y} = \tfrac{1}{\sqrt{2}}\!\left(\frac{\partial}{\partial x'} - \frac{\partial}{\partial y'}\right)$$

$$\frac{\partial^2}{\partial x\,\partial y} = \tfrac{1}{2}\!\left(\frac{\partial^2}{\partial x'^2} - \frac{\partial^2}{\partial y'^2}\right)$$

so

$$\mathcal{H}\psi \simeq -\tfrac{1}{2}\frac{\partial^2 \psi(x', y')}{\partial x'^2} + \tfrac{\omega^2}{2}x'^2\,\psi \;-\; \tfrac{1}{2}\frac{\partial^2 \psi}{\partial y'^2} - \tfrac{\omega^2}{2}y'^2\,\psi$$

One is a positive harmonic oscillator; the other negative. These perhaps correspond to sin and cos waves.

$$a_{\cos}^+ = \tfrac{1}{2}\!\left(x + \tfrac{i}{\omega}\pi_x\right), \qquad a_x = \tfrac{1}{2}(y - \cdots)$$

---

## Page 53

Bose statistics mean that $\psi$ must be completely symmetric w.r.t. the exchange of any pair of particles. It must be set up by hand to be this symmetric. See Messiah V.2 pp.586–600. Since there is no interaction with a free field, maintaining this symmetrization is trivial.

If I apply creation & annihilation operators, their commutator relations enforce the symmetry, e.g.

$$a_k^+ a_p^+ |\psi\rangle = a_p^+ a_k^+ |\psi\rangle$$

since $a_k^+ a_p^+ - a_p^+ a_k^+ = 0$. It may be of interest to see how the creation & annihilation operators are written in the Schrödinger representation we are discussing. Part of it is that $|n_{-p}\ldots n_j\ldots n_p\rangle$ naturally reflects the degeneracies, as one particle in slot $j$ is the same as any other. Thus,

$$|n_{-p}\ldots n_j\ldots n_p\rangle \;\longrightarrow\; \psi_N(\underbrace{-p,-p,-p,\ldots}_{n_{-p}\text{ times}}\;\ldots\;j,j,j\;\ldots\;\underbrace{p,p,p,\ldots}_{n_p\text{ times}})$$

and this $\psi_N$ must be symmetric, i.e. $\psi_N = S\psi_N = \dfrac{1}{N!}\sum_P P\,\psi_N$.

---

## Page 54

$$\bar\phi_p = \tfrac{1}{\sqrt{2}}(\phi_p + \phi_{-p}) \qquad \widetilde{\phi}_q = \tfrac{1}{\sqrt{2}}(\phi_p - \phi_{-p})$$

$$\phi_k = \tfrac{1}{\sqrt{2}}(\bar\phi_p + \widetilde{\phi}_q), \qquad \phi_{-k} = \tfrac{1}{\sqrt{2}}(\bar\phi_p - \widetilde{\phi}_q)$$

Let $\alpha_p^+$ create $\bar\phi_p$ and $\beta_q^+$ create $\widetilde{\phi}_q$:

$$\alpha_p^+ = \tfrac{1}{2}\!\left(\bar\phi_p - \tfrac{i}{\omega_p}\bar\pi_p\right), \qquad \beta_q^+ = \tfrac{1}{2}\!\left(\widetilde{\phi}_q - \tfrac{i}{\omega_q}\widetilde{\pi}_q\right)$$

$$\alpha_p = \tfrac{1}{2}\!\left(\bar\phi_p + \tfrac{i}{\omega_p}\bar\pi_p\right), \qquad \beta_q = \tfrac{1}{2}\!\left(\widetilde{\phi}_q + \tfrac{i}{\omega_q}\widetilde{\pi}_q\right)$$

$$\bar\phi_k = \alpha_k^+ + \alpha_k, \qquad \widetilde{\phi}_k = \beta_k^+ + \beta_k$$
$$\bar\pi_k = i\omega_k(\alpha_k^+ - \alpha_k), \qquad \widetilde{\pi}_k = i\omega_k(\beta_k^+ - \beta_k)$$

Then if $\phi_k = \tfrac{1}{\sqrt{2}}(\bar\phi_p + \widetilde{\phi}_q)$, we can create $\phi_k$ with

$$\phi_k = a_k^+ + a_{-k}$$

$$a_k^+ = \tfrac{1}{\sqrt{2}}(\alpha_p^+ + \beta_q^+)$$

$$\quad = \tfrac{1}{2}\!\left(\tfrac{1}{\sqrt{2}}\!\left(\bar\phi_p - \tfrac{i\bar\pi_k}{\omega_k}\right) + \tfrac{1}{\sqrt{2}}\!\left(\widetilde{\phi}_q - \tfrac{\widetilde\pi_q}{\omega_k}\right)\right)$$

$$\quad = \tfrac{1}{2}\!\left(\tfrac{1}{\sqrt{2}}(\bar\phi_p + \widetilde{\phi}_q) - \tfrac{i}{\omega_k}\tfrac{1}{\sqrt{2}}(\bar\pi_k + \widetilde{\pi}_q)\right)$$

$$\quad = \tfrac{1}{2}\!\left(\phi_k - \tfrac{i}{\omega_k}\pi_k\right)$$

$$a_k = \tfrac{1}{\sqrt{2}}(\alpha_p + \beta_q) = \tfrac{1}{\sqrt{2}}\!\left(\phi_k - \tfrac{i}{\omega_k}\pi_k\right)$$

(Standard rep uses $\alpha_p^+ = \left(\sqrt{\omega}\,\bar\phi_p - \tfrac{1}{\sqrt{\omega_p}}\bar\pi_p\right)$ etc.)

$$h_k \sim \alpha_k^+ \alpha_k + \alpha_k \alpha_k^+ \;-\; \beta_k^+ \beta_k - \beta_k \beta_k^+$$

If $\phi(x)$ is real, what can we say about $\phi_k$?

$$\phi_k = 2\omega_k \int \phi(x)\,e^{ik\cdot x}\,d^3x$$

$$\quad = 2\omega_k \int \phi(x)\cos(k\!\cdot\!x)\,d^3x \;+\; i\,2\omega_k\int \phi(x)\sin(k\!\cdot\!x)\,d^3x$$

$$\phi_{-k} = 2\omega_k \int \phi(x)\cos(k\!\cdot\!x) - i\phi(x)\sin(k\!\cdot\!x)\,d^3x$$

$$\phi_k - \phi_{-k} = 0 \quad\Longrightarrow\quad \widetilde{\phi}_q = 0$$

---

## Page 55

$$H = \frac{1}{8(2\pi)^3}\int \left(\frac{\pi_k \pi_{-k}}{\omega_k^2} + \phi_k \phi_{-k}\right) d^3k$$

$$\quad = \frac{1}{16(2\pi)^3} \int \frac{1}{\omega_k^2}\!\left(\bar\pi_k^2 + \omega_k^2 \bar\phi_k^2 \;+\; \widetilde\pi_k^2 + \omega_k^2 \widetilde\phi_k^2\right) d^3k$$

$$\quad = \tfrac{1}{8}\int \frac{d^3k}{(2\pi)^3 \, 2\omega_k}\,\frac{1}{\omega_k}\!\left(\bar\pi_k^2 + \omega_k^2 \bar\phi_k^2 + \widetilde\pi_k^2 + \omega_k^2 \widetilde\phi_k^2\right)$$

Note that $\bar\phi_k = \bar\phi_{-k}$ and $\widetilde\phi_k = -\widetilde\phi_{-k}$.

Introduce $\alpha_k$, $\beta_k$ operators now so that

$$H = \frac{1}{16(2\pi)^3}\int \frac{d^3k}{\omega_k}\!\left(-(\alpha_k - \alpha_k^+)^2 + (\alpha_k^+ + \alpha_k)^2\right) + (\beta)$$

$$\quad = \frac{1}{16(2\pi)^3}\int d^3k\,\Big(-\alpha_k^+\alpha_k^+ - \alpha_k \alpha_k + \alpha_k^+\alpha_k + \alpha_k \alpha_k^+ \;+\; \alpha_k^+\alpha_k^+ + \alpha_k\alpha_k + \alpha_k^+\alpha_k + \alpha_k\alpha_k^+\Big)$$

$$\quad = \frac{1}{8(2\pi)^3}\int \left(\alpha_k^+ \alpha_k + \alpha_k\alpha_k^+ + \beta_k^+\beta_k + \beta_k\beta_k^+\right) d^3k$$

$$\quad = \tfrac{1}{4}\int \omega_k\!\left(\alpha_k^+\alpha_k + \alpha_k\alpha_k^+ + \beta_k^+\beta_k + \beta_k\beta_k^+\right) \frac{d^3k}{(2\pi)^3 2\omega_k}$$

Two sets of particles described here. Can antisymmetric be done away with due to non-Bose statistics?

[ink-blot redaction at lower right, partial commutator algebra below visible:]

$$[\alpha_k,\alpha_p^+]\,f \quad \text{with } \pi_k = i\frac{\partial}{\partial\phi_k}$$

$$= \tfrac{1}{4}\!\left(\phi_k + \tfrac{i}{\omega_k}\frac{\partial}{\partial\phi_k}\right)\!\!\left(\phi_p - \tfrac{i}{\omega_p}\cdots\right)\,f$$

$$\;\;\vdots\;\;\;\text{(further algebra, partly obscured by ink blot)}$$

$$= \tfrac{i}{4}\!\left[\,\phi_k\phi_p\,f - \tfrac{i}{\omega_p}\phi_k\frac{\partial f}{\partial\phi_p} + \phi_p\,(\text{partial})\,f - \tfrac{i}{\omega_p}\phi_p\,\frac{\partial f}{\partial\phi_p}\right]$$

$$= \tfrac{1}{4}\Big(\cdots - \tfrac{i}{\omega_p}(\partial\phi_p/\partial\phi_k)\,f + \phi_p\,(\cdots) - \tfrac{i}{\omega_p}\,\frac{\partial}{\partial\phi_p}f + \phi_p\,(\cdots)\Big)$$

---

## Page 56

$$a_k^+ = \tfrac{1}{\sqrt{2}}(\alpha_k^+ + i\beta_k^+), \qquad a_k = \tfrac{1}{\sqrt{2}}(\alpha_k - i\beta_k)$$

create pure $\phi_k$ particles

$$a_k^+ a_k + a_k a_k^+ = \tfrac{1}{2}\Big((\alpha_k^+ + i\beta_k^+)(\alpha_k - i\beta_k) + (\alpha_k - i\beta_k)(\alpha_k^+ + i\beta_k^+)\Big)$$

$$\quad = \tfrac{1}{2}\Big(\alpha_k^+\alpha_k + \beta_k^+\beta_k + i(\beta_k^+\alpha_k - \alpha_k^+\beta_k) + \alpha_k\alpha_k^+ + \beta_k\beta_k^+ - i\beta_k\alpha_k^+ + i\alpha_k\beta_k^+\Big)$$

Can we say anything about these 4 terms,

$$T = \tfrac{1}{2}i\,\big(\beta_k^+\alpha_k - \alpha_k^+\beta_k + \beta_k\alpha_k^+ - \alpha_k\beta_k^+\big)\;?$$

If $\alpha$ and $\beta$ all commute, then

$$\beta_k^+\alpha_k - \alpha_k\beta_k^+ = 0$$

so

$$T = \alpha_k^+\beta_k + \alpha_k\beta_k^+$$

No, **but** $\alpha_k = \alpha_{-k}$, $\beta_k = -\beta_{-k}$, whereby

$$T_k = -T_{-k}$$

and

$$\int T_k\, d^3k \;=\; 0$$

---

## Page 57 (inserted printed page — Sakurai-style angular momentum text, oriented sideways)

*This page is a photocopy / insertion from a printed textbook section "2. Angular Momentum Algebra Representations of Angular Momentum Operators," not handwritten notes. Equation references on the page include (2.20)–(2.22b). The visible content includes:*

The matrix elements are the integrals

$$\langle j', m' | J_\pm | j, m \rangle = \delta_{j j'}\,\delta_{m', m\pm 1}\sqrt{(j\mp m)(j\pm m + 1)}$$

In the case of angular momentum $j = \tfrac{1}{2}$, we obtain the Pauli matrices.

$$(J_x)_{m m'} = \tfrac{1}{2}\!\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = \tfrac{1}{2}\sigma_x$$

and

$$(J_y)_{m m'} = \tfrac{1}{2}\sigma_y, \qquad (J_z)_{m m'} = \tfrac{1}{2}\sigma_z \tag{2.22}$$

In the case of angular momentum $j = 1$ (absolute value $\sqrt{2}\hbar$) we obtain three-dimensional matrices with $m = -1, 0, 1$:

$$S_x = \tfrac{1}{\sqrt{2}}\!\begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}, \quad
S_y = \tfrac{1}{\sqrt{2}}\!\begin{pmatrix} 0 & -i & 0 \\ i & 0 & -i \\ 0 & i & 0 \end{pmatrix}, \quad
S_z = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & -1 \end{pmatrix} \tag{2.22a}$$

In the same way we used the spinors $\chi_+, \chi_-$ and $\chi_\pm \tfrac{1}{2}$ to describe the states with spin $\tfrac{1}{2}$, we now may use the vectors $\chi_m$, i.e.

$$\chi_1 = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}, \;\; \chi_0 = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}, \;\; \chi_{-1} = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}$$

which represent the possible states for spin 1. Hence, the vectors $\chi_m$ are eigenstates of the matrix $S_z$.

*[Right column of the printed page — partially legible:]*

This will be the velocity-like spin 1 behaves like a part of, the photon (as a vector field) has spin 1. The relation $\text{Eq.}(0) \to$ representation in (2.21)

For higher spin we obtain analogous matrices:

$$S_x = \tfrac{1}{\sqrt{2}}\!\begin{pmatrix} 0 & \sqrt{3} & 0 & 0 \\ \sqrt{3} & 0 & 2 & 0 \\ 0 & 2 & 0 & \sqrt{3} \\ 0 & 0 & \sqrt{3} & 0 \end{pmatrix},$$

$$S_y = \cdots$$

$$S_z = \tfrac{1}{2}\!\begin{pmatrix} 3 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & -3 \end{pmatrix} \tag{2.22b}$$

which have matrix elements as components. We mapping in such representations are not closed in quantum mechanics, in part as a product of irreducible representations.

EXERCISES — *(headings only visible)*

---

## Page 58 (mostly blank verso of the inserted printed page)

*Blank apart from faint vertical column rules from the printed page on the verso. No handwritten content.*

---

## Page 59 — "Complex mass" (dated 9/6/2007)

**Complex mass**

The usual Dirac equation takes the form

$$i\hbar\,\frac{\partial}{\partial t}\Psi = i\hbar c\,\vec\alpha \cdot \nabla \Psi + \beta\, m_0 c^2\,\Psi \tag{1}$$

This is the result of taking the square root of

$$\sqrt{p^2 c^2 + m^2 c^4} \tag{2}$$

using matrices $\vec\alpha$, $\beta$, i.e.

$$\bigl(\vec\alpha \cdot \vec p\, c + m c^2 \beta\bigr)^2 = (p^2 c^2 + m^2 c^4)\,\mathbb{I} \tag{3}$$

Interestingly, the choice of these matrices need not be unique. ~~For example,~~ A typical representation of these matrices is given by

$$\alpha_i = \sigma_3 \otimes \sigma_i, \qquad \beta = -\sigma_1 \otimes \sigma_0 \tag{4}$$

where

$$\sigma_0 = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad
\sigma_1 = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad
\sigma_2 = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad
\sigma_3 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \tag{5}$$

We might simply look at the fact that one could just as well write

$$\beta = (a\,\sigma_1 + b\,\sigma_2)\otimes \sigma_0 \tag{6}$$

where $a^2 + b^2 = 1$ and get the same solution of (3) above. Normally this choice of the $\alpha$ and $\beta$ are considered arbitrary, and left at that. Then one picks a convenient representation & solves the equation.

---

## Page 60

Suppose, however, that these representations were gauged, so that they weren't the same from point to point. This seems to introduce an $SU(2)$ gauge symmetry of sorts into the system. If we start by just looking at the symmetries in $\beta$ for a fixed $\alpha$, then we can write a general $\beta_g$ of the form $\beta$ using the $\beta$ in (4) via the formula

$$\beta_g = (U \sigma_1 U^+)\otimes \sigma_0$$

where

$$U = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\theta} \end{pmatrix}$$

If we gauge $U$, then $\theta = \theta(x)$. It is fascinating to note that such a gauge symmetry acts on only one half of the bispinor. In this, the Weyl representation, that half of the bispinor corresponds to one particular helicity. This would seem to tie in with the weak interaction, which is also helicity-dependent and *thus related to mass*, and which involves an $SU(2)$ symmetry that is **broken**, while here we're looking at an $SU(2)$ symmetry broken by $U(1)$.

---

*End of pages 46–60 batch.*
