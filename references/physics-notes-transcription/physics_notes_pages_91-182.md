# Physics Notes — Pages 91–182
*Transcribed from physics_notes_0708.pdf*

---

## Page 91 — Dirac Mass Term and Charge Conservation

The ordinary mass term in the Dirac equation does not really conserve charge, if viewed in terms of perturbation theory. Only by solving exactly do we get a balance between the two charge states with the result of charge conservation. In diagrammatic terms, though, we have something like

$$e_R \quad e_R^+ \quad e_R \quad e_R^+ \quad e_R \quad e_R^+$$

where the switching decreases at higher energies.

**Can we say that W actually couples to spin?** Apparently, yes. **In what sense is it a vector particle??**

---

## Pages 92–97 — Electromagnetic and Weak Interactions

*(Motivational paper introduction)*

This paper will explore the similarities between the electromagnetic and weak interactions, and their respective charge spectra. It is intended as a motivational paper that will provide guidance for future, more detailed research.

There are some important likenesses between the electromagnetic and weak interactions which may provide important clues to a deeper understanding of these interactions. Although the Weinberg–Salam theory of electro-weak interactions has had some success in making predictions, it leaves some important questions unanswered, that we might expect a proper theory to answer. For example, W-S posits a symmetry that is then broken to give the W and Z mass. The Higgs boson supposed to be associated to this theory has not been found. Where is it? Or is the supposed symmetry merely an artificial construct to hide the abnormalities of a renormalization scheme? After all, what is the difference between a broken symmetry with no Higgs and a symmetry that never existed in the first place?

Another important problem with W-S is that it uses non-specific techniques that could be formulated in a variety of ways. This fact lays aside a whole class of questions that are simply never asked. They are rooted in the choice of $U(1) \times SU(2)$ as a gauge field. The question is, why did God/Nature choose $U(1) \times SU(2)$, and not something else, like $U(1) \times SO(6,2)$? Our supposition is that there is something important to be learned, probably about the structure of spacetime, in the particulars of $U(1) \times SU(2)$.

By looking at the symmetries of these interactions, we both raise the questions that need to be raised and frame those questions in a way that will hopefully point to an answer, without unwittingly introducing unspoken assumptions.

First, let us consider the leptonic doublets of the electro-weak interaction,

$$\begin{pmatrix} e \\ \nu_e \end{pmatrix} \quad \begin{pmatrix} \mu \\ \nu_\mu \end{pmatrix} \quad \begin{pmatrix} \tau \\ \nu_\tau \end{pmatrix}$$

and potentially others, undiscovered as yet. Let us write these out in detail using the Weyl representations:

$$\begin{pmatrix} e \\ \nu_e \end{pmatrix} = \begin{pmatrix} e_R^- \\ e_L^+ \\ e_R^+ \\ e_L^- \\ \nu_R \\ \bar{\nu}_L \\ \bar{\nu}_R \\ \nu_L \end{pmatrix}$$

Note that we have included $\nu_R$ and $\bar{\nu}_L$, which most treatments of W-S omit, and claim to be non-existent. That claim is based on the assertion that neutrino masses are exactly zero. Experimentally, this claim is open to question.

Certainly the fact that they interact at all suggests that they ought to gain some renormalization mass from the interaction. Leaving it out also clouds the symmetry between electromagnetic and weak interactions. (W-S does this for simplicity, so one can deal with only one singlet and one doublet for each leptonic pair. That way the singlet covariant derivative need only deal with the charged electron, and it needn't have two forms.)

In this representation, we may see that both electromagnetic and weak interactions have four charged states and four neutral states that do not interact:

| State | EM | W |
|---|---|---|
| $e_R^-$ | EM | — |
| $e_L^+$ | EM | — |
| $e_R^+$ | EM | W |
| $e_L^-$ | EM | W |
| $\nu_R$ | — | — |
| $\bar{\nu}_L$ | — | — |
| $\bar{\nu}_R$ | — | W |
| $\nu_L$ | — | W |

These include two states that interact both weakly and electromagnetically, two that interact only electromagnetically, two that interact only weakly, and two that do not interact at all. This is a very symmetric representation of these forces.

It is interesting to note that these neutral states correspond to a "missing" charge state. The right-handed weak interaction does not exist, and neither does the magnetic monopole. By this line of reasoning the neutrino would be the magnetic monopole that doesn't exist. Both a right-handed weak interaction and a magnetic monopole would require the introduction of new sets of fields, a $(W_R^\pm, Z')$ for right-handed weak and an $A'$ for monopoles. We should also mention that with symmetry breaking and Higgs, we may not be able to rule these out completely — perhaps we can only set lower limits on the mass of thin IVBs, as the interaction becomes weaker as the mass goes up.

Again, we must ask: why is there no right-handed weak interaction? Why is there no magnetic monopole? This is something a fundamental theory should answer.

The similarity between electromagnetic and weak interactions might also be examined at the level of the IVB. The photon is massless and carries no charge, only angular momentum, coupling charged particles. The weak interaction carries charge, but no angular momentum (coupling only to left-handed particles). It is essential that the weak IVB be massive in order to avoid coupling to right-handed particles too *(it has a longitudinal mode, not just transverse, and can flip chirality)*. And it is essential that the photon be chargeless to avoid developing a mass from self-energy. In other words, electromagnetism is to charge as the weak interaction is to left-handedness.

The strong interaction appears to be a quantum effect, in ways similar to the Heisenberg Uncertainty Principle, in ways similar to spin and angular momentum.

The fact that quarks cannot be observed alone in nature seems to correspond in a way to spin and orbital angular momentum — that orbital angular momentum occurs in quantum steps of $0, 1, 2, 3$ etc. whereas spin takes values of $\frac{1}{2}, \frac{3}{2}$, etc. too. These spin values cannot exist as independent orbital angular momentum values, but they can be attached to the mathematics of particles as an intrinsic property. In the same way, perhaps electric charge has a deeper principle or something such that only charge-1 particles can be seen on a macroscopic level, but there are intrinsic charges $\frac{1}{3}e$ that do exist under a Heisenberg-like arrangement that cannot be seen macroscopically, due to some fundamental principle.

---

## Pages 98–101 — Rotation Matrices, Tensor Products, 3D Dirac

### Tensor Products of Rotation Matrices

$$R_z \otimes R_z = \begin{pmatrix} e^{i\theta/2} & 0 \\ 0 & e^{-i\theta/2} \end{pmatrix} \otimes \begin{pmatrix} e^{i\theta/2} & 0 \\ 0 & e^{-i\theta/2} \end{pmatrix} = \begin{pmatrix} e^{i\theta} & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & e^{-i\theta} \end{pmatrix}$$

$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \qquad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$$

$$R_x(\phi) = \exp(i\sigma_x \phi/2) = \begin{pmatrix} i\sin\phi/2 & \cos\phi/2 \\ \cos\phi/2 & i\sin\phi/2 \end{pmatrix}$$

$$R_x = R_x \otimes R_x = \begin{pmatrix} i\sin\phi/2 & \cos\phi/2 \\ \cos\phi/2 & i\sin\phi/2 \end{pmatrix} \otimes \begin{pmatrix} i\sin\phi/2 & \cos\phi/2 \\ \cos\phi/2 & i\sin\phi/2 \end{pmatrix}$$

$$= \begin{pmatrix} -\sin^2\phi/2 & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & i\cos\frac{\phi}{2}\sin\frac{\phi}{2} & \cos^2\frac{\phi}{2} \\ i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & -\sin^2\frac{\phi}{2} & \cos^2\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} \\ i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & \cos^2\frac{\phi}{2} & -\sin^2\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} \\ \cos^2\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & -\sin^2\frac{\phi}{2} \end{pmatrix}$$

$$R_y(\phi) = \exp(i\sigma_y \phi/2) = \begin{pmatrix} \sin\phi/2 & \cos\phi/2 \\ -\cos\phi/2 & -\sin\phi/2 \end{pmatrix}$$

$$R_y = R_y \otimes R_y = \begin{pmatrix} \sin^2\phi/2 & -\sin\frac{\phi}{2}\cos\frac{\phi}{2} & -\sin\frac{\phi}{2}\cos\frac{\phi}{2} & \cos^2\frac{\phi}{2} \\ \cos^2\frac{\phi}{2}\sin\frac{\phi}{2} & \sin^2\frac{\phi}{2} & -\cos^2\frac{\phi}{2} & -\cos^2\frac{\phi}{2}\sin\frac{\phi}{2} \\ \cos\frac{\phi}{2}\sin\frac{\phi}{2} & -\cos^2\frac{\phi}{2} & \sin^2\frac{\phi}{2} & -\cos\frac{\phi}{2}^2\sin\frac{\phi}{2} \\ \cos^2\frac{\phi}{2} & \cos\frac{\phi}{2}^2\sin\frac{\phi}{2} & \sin^2\frac{\phi}{2}\cos\frac{\phi}{2} & \sin^2\frac{\phi}{2} \end{pmatrix}$$

Using $\sin 2\theta = 2\sin\theta\cos\theta$ and $\cos 2\theta = \cos^2\theta - \sin^2\theta$:

$$R_x = \begin{pmatrix} -\sin^2\phi/2 & 2i\sin\phi & 2i\sin\phi & \cos^2\phi/2 \\ 2i\sin\phi & -\sin^2\phi/2 & \cos^2\phi/2 & 2i\sin\phi \\ 2i\sin\phi & \cos^2\phi/2 & -\sin^2\phi/2 & 2i\sin\phi \\ \cos^2\phi/2 & 2i\sin\phi & 2i\sin\phi & -\sin^2\phi/2 \end{pmatrix}$$

We want to transform this to get rid of all $\phi/2$, presumably making $\cos^2\frac{\phi}{2} - \sin^2\frac{\phi}{2}$ into $\cos\frac{\phi}{2} + \sin^2\frac{\phi}{2}$ out of it.

### Spin-1 Matrices

$$S_x = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -i \\ 0 & i & 0 \end{pmatrix}, \quad S_y = \begin{pmatrix} 0 & 0 & i \\ 0 & 0 & 0 \\ -i & 0 & 0 \end{pmatrix}, \quad S_z = \begin{pmatrix} 0 & -i & 0 \\ i & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$$

$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

$$\sigma_x \otimes \sigma_x = \begin{pmatrix} 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \end{pmatrix}, \quad \sigma_y \otimes \sigma_y = \begin{pmatrix} 0 & 0 & 0 & -1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \end{pmatrix}, \quad \sigma_z \otimes \sigma_z = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

We want a basis transformation to turn $\sigma_z \otimes \sigma_z$ etc. into $\begin{pmatrix} 0 & \cdot \\ \cdot & S_x \end{pmatrix}$.

Let $A = \begin{pmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & \cdots \end{pmatrix}$, then $A(\sigma_z \otimes \sigma_z)A^\dagger$ is computed.

Need a rep where $S_z$ is diagonal. The required transformation for the Z direction:

$$\begin{pmatrix} 1/\sqrt{2} & 0 & 1/\sqrt{2} \\ 0 & 1 & 0 \\ 1/\sqrt{2} & 0 & -1/\sqrt{2} \end{pmatrix}$$

In the new basis:

$$S_x = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}, \quad S_y = \begin{pmatrix} 0 & -i & 0 \\ i & 0 & -i \\ 0 & i & 0 \end{pmatrix}, \quad S_z = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & -1 \end{pmatrix}$$

### 3D Dirac Equation

A 3D Dirac equation:

$$\frac{\partial \psi_+}{\partial t} = -c\, \mathbf{S} \cdot \nabla\, \psi_+$$

$$\frac{\partial \psi_-}{\partial t} = c\, \mathbf{S} \cdot \nabla\, \psi_-$$

Breaking these out:

$$\begin{pmatrix} \partial_0 \psi_+^1 \\ \partial_0 \psi_+^2 \\ \partial_0 \psi_+^3 \end{pmatrix} = -c \begin{pmatrix} \partial_3 & \partial_1 - i\partial_2 & 0 \\ \partial_1 + i\partial_2 & 0 & \partial_1 - i\partial_2 \\ 0 & \partial_1 + i\partial_2 & -\partial_3 \end{pmatrix} \begin{pmatrix} \psi_+^1 \\ \psi_+^2 \\ \psi_+^3 \end{pmatrix}$$

$$= -c \begin{pmatrix} \partial_3\psi_+^1 + \partial_1\psi_+^2 - i\partial_2\psi_+^2 \\ \partial_1\psi_+^1 + i\partial_2\psi_+^1 + \partial_1\psi_+^3 - i\partial_2\psi_+^3 \\ \partial_1\psi_+^2 + i\partial_2\psi_+^2 - \partial_3\psi_+^3 \end{pmatrix}$$

If $\psi_+ = E + iB$ [note for further investigation]

---

## Pages 103–104 — Neutral Charge and Weinberg Angle

### Neutral Charge Operator

$$Q' = t_3 \cot\theta_W - t_0 \tan\theta_W$$

Experimental values:
$$\sin^2\theta_W = 0.232 \pm 0.009, \quad \cos^2\theta_W = 0.768$$
$$\sin\theta_W = 0.481, \quad \cos\theta_W = 0.876$$
$$\cot\theta_W = 1.821, \quad \tan\theta_W = 0.549$$

$$Q' = \begin{pmatrix} 1.821 + 0.549 & 0 \\ 0 & -1.821 + 0.549 \end{pmatrix} = \begin{pmatrix} 2.37 & 0 \\ 0 & -1.27 \end{pmatrix}$$

### Hypothetical $\sin\theta_W = \frac{1}{2}$

What if $\sin\theta_W = \frac{1}{2}$? Then $\cos\theta_W = \frac{\sqrt{3}}{2}$, $\cot\theta_W = \sqrt{3}$, $\tan\theta_W = \frac{1}{\sqrt{3}}$.

*(After all, renormalization could throw it off a little.)*

For W coupling: $e = g\sin\theta_W$, so $g$ couples $W_1$, $W_2$.

$$\tau_\pm = \frac{1}{\sqrt{2}}(\tau_1 \pm i\tau_2) = \begin{pmatrix} 0 & \sqrt{2} \\ 0 & 0 \end{pmatrix}, \quad \begin{pmatrix} 0 & 0 \\ \sqrt{2} & 0 \end{pmatrix}$$

$$V_\pm = \frac{1}{\sqrt{2}}(W_1 \pm iW_2)$$

$$W_+\tau_+ + W_-\tau_- = \frac{1}{\sqrt{2}}W_1\tau_1 + \frac{1}{\sqrt{2}}W_2\tau_2$$

$$|W_+|^2 + |W_-|^2 = |W_1|^2 + |W_2|^2$$

$$gW_1\tau_1 + gW_2\tau_2 = g(W_-\tau_+ + W_+\tau_-)$$

So coupling $\sim \sqrt{2}g \sim \frac{\sqrt{2}}{\sin\theta_W} e$

### Hypothetical $\text{Coupling to } W^\pm = 3e$

What if coupling to $W^\pm = 3e$ exactly? Then $\frac{\sqrt{2}}{\sin\theta_W} = 3 \Rightarrow \sin\theta_W = \frac{\sqrt{2}}{3}$

$$\sin^2\theta_W = \frac{2}{9} = 0.222\overline{2} = \frac{2}{9}$$

Is there any significance to this?

$$\sin\theta_W = \frac{\sqrt{2}}{3}, \qquad \tan\theta_W = \sqrt{\frac{1}{7}} \approx 0.535, \qquad \cot\theta_W = \sqrt{\frac{7}{2}} \approx 1.871$$

$$Q_z = \begin{pmatrix} \cot\theta_W + \tan\theta_W & 0 \\ 0 & \cot\theta_W - \tan\theta_W \end{pmatrix} = \begin{pmatrix} 2\sqrt{7}/3 & 0 \\ 0 & 1/\sqrt{3} \end{pmatrix} \approx \begin{pmatrix} 2.37 & 0 \\ 0 & 1.33 \end{pmatrix}$$

Other algebra: $\cot\theta + \tan\theta = 7/3$, $\cot\theta - \tan\theta = 4/3$,
$2\cot\theta = 11/3$, $\cot\theta = 11/6$,
$x + 1/x = 7/3$, $x - 1/x = 4/3$, $2x = 11/3$, $x = 11/6$,
$\frac{11}{6} + \frac{6}{11} = \frac{121+36}{66} = \frac{157}{66} = 2\frac{25}{66}$ ✗

Working out $Q'\sin^2\theta$:
$$t_3\left(\frac{\cos\theta}{\sin\theta} - t_0\frac{\sin\theta}{\cos\theta}\right)\sin^2\theta = t_3\frac{\sin^{2\theta}}{\cos\theta}\cdot\cos\theta - t_0\frac{\sin^{2\theta}}{\cos\theta}\cos\theta$$
$$= t_3 2\cos^2\theta - t_0 2\sin^2\theta$$

---

## Page 105 — Electromagnetic Self-Energy Calculation

### Electromagnetic Field Energy

$$\mathcal{E}_e = \int_{r_0}^\infty |E|^2 \, dV = \int_{r_0}^\infty \frac{e^2}{r^4} 4\pi r^2 \, dr = 4\pi e^2 \int_{r_0}^\infty \frac{dr}{r^2}$$
$$= 4\pi e^2 / r_0 \quad \text{(adding factors of } 8\pi\text{)} \quad \Rightarrow \mathcal{E} = \frac{e^2}{2r_0}$$

### Yukawa Field Energy

For a Yukawa field, $V = \frac{e}{r^2}e^{-\alpha r}$:

$$\mathcal{E}_W = \int_{r_0}^\infty |W|^2 \, dV = \int_{r_0}^\infty \frac{e^2}{r^4} e^{-2\alpha r} 4\pi r^2 \, dr = 4\pi e^2 \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r^2} \, dr$$

$$= 4\pi e^2 \left[ -\frac{e^{-2\alpha r}}{r}\Big|_{r_0}^\infty - 2\alpha \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r} \, dr \right]$$

$$= 4\pi e^2 \left[ \frac{e^{-2\alpha r_0}}{r_0} - \left\{ \log(2\alpha r_0) + \sum_{n=1}^\infty \frac{(-2\alpha)^n r^n}{n \cdot n!} \right\}_{r_0}^\infty \right]$$

$$= 4\pi e^2 \left[ \frac{e^{-2\alpha r_0}}{r_0} + \log(2\alpha r_0) + \sum_{n=1}^\infty \frac{(-2\alpha)^n r^n}{n \cdot n!}\Big|_{r_0}^\infty \right]$$

This is quite ugly, and should probably be done numerically.

### Ratio of Energies

$$\frac{\mathcal{E}_W}{\mathcal{E}_e} = \frac{g^2}{e^2} \left\{ \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r^2} \, dr \Bigg/ \int_{r_0}^\infty \frac{1}{r^2} \, dr \right\} = \frac{g^2}{e^2 r_0} \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r^2} \, dr$$

Numerical results for $I(n) = \int$ with $\alpha \sim k = \frac{2\pi}{\lambda_c}$, $\lambda_c = \frac{\hbar}{m_e c}$:

| $n$ | $I(n)$ | Note |
|---|---|---|
| 1 | 0.1493 | $m_e = 511\text{ keV}$ |
| 2 | 0.01885 | $m_\nu = 5\text{ eV}$ |
| 3 | 0.00356 | $\to 10^{-5}$ |
| 5 | 0.000 (truncated) | |
| 7 | $1.48 \times 10^{-5}$ | |

$$M_W = 80\text{ GeV} = 1.43 \times 10^{-25}\text{ kg}$$
$$h = 6.626 \times 10^{-34}\text{ J·s}$$
$$k = \frac{\hbar c}{m_e c^2} = 1.39, \qquad \alpha \sim 4 \times 10^{17}, \qquad \alpha r_0 = 400$$

---

## Page 106 — Newton's Method / Classical Electron Radius

### Linear Interpolation

$$f(x) = \left(\frac{f(x_1) - f(x_2)}{x_1 - x_2}\right)^{(x - x_0)} + f(x_2)$$

$$f(x) = f(x_2) + \partial f\,(x - x_2)$$

$$\frac{f(x) - f(x_0)}{\partial f} + x_2 = x, \qquad f'(x_0) = \frac{f(x) - f(x_0)}{x - x_0}$$

$$f(x) = f(x_0) + f'(x_0)\,\Delta x, \qquad \frac{1}{f'(x_0)} = \frac{x - x_0}{f(x) - f(x_0)}$$

$$x_0 + (f(x) - f(x_0)) \cdot \frac{1}{f'(x_0)} \approx x$$

### Classical Electron Radius

Setting $\mathcal{E} = \frac{e^2}{2r_0} = m_e c^2 = 9.11 \times 10^{-28} \times 9 \times 10^{20}\text{ cm}^2\text{/s}^2$:

$$\frac{(1.602 \times 10^{-19})^2 (3 \times 10^9)^2}{2r_0} = \frac{2.9 \times 10^{-38} \cdot 9 \times 10^{20}}{(1.602 \times 10^{-19} \cdot 3 \times 10^9)^2}$$

$$r_0 = \frac{e^2}{2mc^2} \approx 1.43 \times 10^{-15}\text{ m}$$

---

## Page 107 — Ellipse Foci

Given an ellipse of the form:

$$\frac{x^2}{b^2} + \frac{y^2}{b^2} = 1$$

it should have foci at $x = \pm a$, $y = 0$. We seek to calculate $a$ as a function of $b$.

The foci have the property that $d_1 + d_2 = \text{constant}$ for every point on the ellipse, where:
$$d_+ = \sqrt{(x-a)^2 + y^2}, \qquad d_- = \sqrt{(x+a)^2 + y^2}$$

The x-intercepts are $x = \pm b$, $y = 0$. Here $d_+ + d_- = |b - a| + |b + a| = 2b$.

The y-intercepts are $x = 0$, $y = \pm 1$, whereby:
$$d_+ + d_- = 2\sqrt{a^2 + 1}$$

Whereby:
$$\sqrt{a^2 + 1} = b \quad \Rightarrow \quad a^2 + 1 = b^2$$

*(b is the y-factor)* So if $b = 1.2$: $a = \sqrt{1.44 - 1} = \sqrt{0.44} \approx 0.67$ — **quite large!**

---

## Pages 108–109 — Weinberg–Salam and W Bosons as Vectors

To get W-S, we want the mass-like term to be mediated by a boson instead. That is, take:

$$\mathcal{L}_{\text{local}} = g(\bar{\nu}_e e_L + \bar{e}_L \nu_e) + g'(\bar{\nu}_R e_R + \bar{e}_R \nu_R)$$

and turn it into something like:

$$\mathcal{L}_{WS} = g_0 W_+ \bar{\nu}_L e_L + g_0 W_- \bar{e}_L \nu_L$$

Putting $g' = 0$. These $W^\pm$ are still scalars. How are they turned into a vector field? Presumably by writing something like $W_\pm = \partial_\mu W_\pm^\mu$, etc. Then:

$$\mathcal{L}_{WS} = g_0 (\sigma_\mu \otimes \tau_0) W_\mu^{\ +} \bar{\nu}_L e_L + g_0 (\sigma_\mu \otimes \tau) W_\mu^{\ -} \bar{e}_L \nu_L$$

This has the essential form necessary for W-S, and naturally goes with the term:

$$(\bar{\nu}_L\; \bar{e}_L)\; \frac{1}{2}\big((\sigma_0 \otimes \tau_0) B_\mu + \bar{\tau}_0 \otimes \tau_3 B^{\ \mu}\big)\begin{pmatrix} \nu_L \\ e_L \end{pmatrix}$$

Yet how can we properly expect $g_0 = g_e$? In general, we cannot. Such would be the source of the so-called Weinberg angle, which is just a kludge to allow $g_0 \neq g_e$ and yet still pretend a gauge field of $SU(2)$ symmetry.

Now, is there any reason $B$ and $W^\pm$ should be massive? It seems funny they should be, in view of the fact that a massive field is one that shifts L and R components, yet this one specifically couples only to itself.

---

## Pages 110–124 — What is a Spinor?

*(Numbered paper, pages 5–15)*

### The Spinor as a Two-Component Complex Vector

A spinor is a two-component complex vector:

$$\begin{pmatrix} \alpha \\ \beta \end{pmatrix} \tag{11}$$

which exists in an abstract complex space. At the same time, it is commonly understood that this abstract space has some connection with the spacetime we live in, by virtue of the spin matrices. For example, the spin of a particle in the Z direction is given by:

$$\frac{1}{2} \otimes \sigma_z \begin{pmatrix} \alpha \\ \beta \end{pmatrix} \tag{12}$$

etc. As such, we understand that this abstract space has something to do with direction, but what? How does one map $(x, y, z, t)$ into a spinor and vice versa?

Part of the problem we face is that a spinor contains a certain amount of ambiguity. If any 2-spinor field $\Psi_+$ is a solution of the Weyl equation, then so is $a\Psi_+$, where $a$ is any complex number. *(This is only a trivial phase-invariance and normalization of theory.)* Thus, considered at any point $x_0$, $a\Psi_+(x_0) = \begin{pmatrix} a\alpha \\ a\beta \end{pmatrix}$. $\tag{13}$

The values $\alpha$ and $\beta$ have no meaning in any absolute terms. The only real meaning is in the single complex ratio:

$$\eta = \frac{\alpha}{\beta} \tag{14}$$

which is invariant under the transformation $\Psi_+ \to a\Psi_+$.

This immediately raises the question: if a spinor's only real content consists of a single complex number, why must it be represented by two complex numbers? Why can't it be represented as a single complex number and have an ordinary scalar wave equation? **In the answer to this question lies the key to what a spinor is.**

### What is a Spinor?

*(Section heading, crossed out in original)*

Rather than trying to work backward to what a spinor is, we will state what it is and then show why this "what" leads to the spinor's natural structure. As it turns out, that structure is rather convoluted *(it is not very easy to guess)*, and not so easy to work backward.

We understand that a scalar $q$ is a magnitude only. A vector $\vec{v} = x\hat{x} + y\hat{y} + z\hat{z}$ is both a magnitude and a direction. **A spinor, then, is a direction without a magnitude.** It should be no surprise that a spinor has something to do with direction in as much as it describes spin, or intrinsic angular momentum, and angular momentum is directional.

Note that angular momentum is also apparently the same — $\frac{1}{2}\hbar$ — for all spinor particles, so no magnitude information is really needed.

To complete this geometrical picture, a map between a direction-without-magnitude and a complex spinor is needed. A direction without magnitude can be described as a point on the unit sphere:

$$x^2 + y^2 + z^2 = r^2 \tag{15}$$

Every point on this sphere corresponds to a particular direction. Every vector starting at the origin passing through this sphere passes through a single point which indicates its directional component.

To equate the unit sphere with spinors, we need a mapping between it and the complex plane, which consists of all complex numbers $\alpha + i\beta$. Since the surface of a sphere is two-dimensional and the complex plane is two-dimensional, a mapping can be imagined.

However, the sphere is topologically different from the plane. On a sphere, one may proceed in a certain direction and eventually return to the point where they started. On a plane, going in any direction will never lead back to where one started. **This topological difference between the sphere and the plane** *(a direction-without-magnitude)* **is the source of the reason why a spinor cannot be described by a single complex number.** (We will come to it in a moment.)

### Stereographic Projection

There is a well-known mapping between the unit sphere and the complex plane in the mathematics of complex analysis, known as the **stereographic projection**. Imagine a sphere with radius $\frac{1}{2}$ situated with its center on the Z axis, at $x=0$, $y=0$, $z=\frac{1}{2}$. Then the bottom of the sphere will be at the origin and the top will be at $x=0$, $y=0$, $z=1$ on the Z axis.

Now, if one draws a line from $(0,0,1)$ that passes through any point on the sphere or the plane, the line will intersect the sphere exactly once and the plane exactly once. This creates defines a one-to-one mapping of the sphere into the plane.

If we let $(x,y,z)$ be the coordinates on the sphere centered at the origin, we translate the sphere up $\frac{1}{2}$ unit:

$$(x,y,z) \to (x',y',z') = \left(x, y, z+\frac{1}{2}\right)$$

whereby:

$${x'}^2 + {y'}^2 + \left(z' - \frac{1}{2}\right)^2 = \frac{1}{4} \tag{17}$$

Now, a line passing through $(0,0,1)$ and $(\alpha, \beta, 0)$ is parameterized by the equations:

$$x = \frac{1}{2}\alpha t \tag{18a}$$
$$y = \beta t \tag{18b}$$
$$z = 1 - t \tag{18c}$$

with $t$ ranging from 0 to 1. This line will intersect the sphere at:

$$(\alpha t)^2 + (\beta t)^2 + \left(\frac{1}{2} - t\right)^2 = \frac{1}{4} \tag{19}$$

or:

$$\alpha^2 + \beta^2 + \frac{1}{4t^2} + 1 - \frac{1}{t} = \frac{1}{4t^2} + \frac{1}{2} \tag{20}$$

which gives:

$$t = (\alpha^2 + \beta^2 + 1)^{-1} \tag{21}$$

or, writing $\zeta = \alpha + i\beta$:

$$\zeta = \alpha + i\beta \tag{22a}$$
$$t = (1 + |\zeta|^2)^{-1} \tag{23}$$

Whereupon:

$$x = \frac{\zeta + \bar{\zeta}}{1 + |\zeta|^2} \tag{24a}$$

$$y = \frac{\zeta - \bar{\zeta}}{1 + |\zeta|^2} \tag{24b}$$

$$z = \frac{|\zeta|^2}{1 + |\zeta|^2} \tag{24c}$$

and:

$$\zeta = \frac{x + iy}{1 - z} \tag{25}$$

These define the stereographic projection in both directions.

Yet this stereographic projection has a problem due to the topological difference between the sphere and the plane. The one point where it does not work is at the very top of the sphere, $x=0$, $y=0$, $z=1$. In this case, $\zeta$ takes the ambiguous form $0/0$, which tends to $\infty$ in every direction of approach.

The standard solution which complex analysts use is to add the single point $\infty$, called infinity, to the complex plane. Then $(x,y,z) = (0,0,1) \leftrightarrow \infty$ and the mapping is complete.

Note that this choice, to map all "infinite points", if you will, into the single point $\infty$ effectively forces the topology of the plane to become that of the sphere. It effectively equates all possible infinities. Another mapping could be imagined that did not do that, but then we would not have a stereographic projection for the sphere.

Our purpose here is not to explore such mappings, but to show how a single complex number maps into a direction-without-magnitude. Yet it is this one point, $\infty$, which makes the direct mapping of a spinor/complex number into a direction-without-magnitude impossible. One must wonder that a single mathematical point should cause so much trouble, but it does, since it is the difference between two topologies.

In order to define all of the mapping without an abstract point $\infty$, we must write $\zeta$ as a ratio of two complex numbers:

$$\zeta = \frac{\xi}{\eta} \tag{26}$$

Now $\zeta$ can be $\infty$ if $\eta = 0$ and $\xi$ is any finite number. Thus we may write:

$$x = \frac{\xi\bar{\eta} + \eta\bar{\xi}}{\bar{\xi}\xi + \eta\bar{\eta}} \tag{27a}$$

$$y = \frac{\xi\bar{\eta} - \eta\bar{\xi}}{\bar{\xi}\xi + \eta\bar{\eta}} \tag{27b}$$

$$z = \frac{\xi\bar{\xi} - \eta\bar{\eta}}{\bar{\xi}\xi + \eta\bar{\eta}} \tag{27c}$$

Clearly there is some ambiguity in $\xi$ and $\eta$, because if $\xi$ and $\eta$ solve (27) then so do $\lambda\xi$ and $\lambda\eta$, where $\lambda$ is any complex number. This is exactly the ambiguity we observed in a spinor, summarized in eq. (14). As such, we may recognize $\xi$ and $\eta$ as two components of a spinor.

In consequence, we may understand the spinor as a direction, since every point on a sphere corresponds to a unique direction. To fully understand the spinor, though, we must consider it in the context of Minkowskian 4-space.

### Spinors in Minkowski 4-Space

Every null vector satisfies:

$$V_0^2 - V_x^2 - V_y^2 - V_z^2 = 0$$

which is the equation of a sphere of radius $V_0^n$. More generally, the set of all such vectors corresponds to the "light cone." Physically speaking, all of the points on the light cone are points connected by the origin along the trajectories of massless particles. These points are "zero distance" from the origin in Minkowski space.

If we think in terms of length contraction and time dilation, as any body or particle approaches the speed of light, the distance along its direction of motion contracts as:

$$d = d_0\sqrt{1 - v^2/c^2}$$

and time dilates as:

$$t = t_0 / \sqrt{1 - v^2/c^2}$$

In that body's frame of reference, the distances between two objects gets smaller, and the time required to travel between them shrinks. In the limit $v \to c$, the dimensions of time and direction of motion collapse. If we could speak of the frame of reference of a photon, then all points through which it travels are identified. They are zero distance apart and zero time apart. In this sense, every line along the light cone is as a single point. Every vector pointing to a point on this line has only a direction, and zero length. **This is exactly what we understood a spinor to be — a direction without a length.**

### Spinors, Space Reflection and Time Reversal

If we consider two points in space, $x_1$ and $x_2$, then, at any given time, there are exactly four connections between them on the light cone, two past and two future:

- $f_{12} = \left(\frac{|\Delta x|}{c},\; \vec{X}_2 - \vec{X}_1\right) = \left(\frac{|\Delta x|}{c},\; \Delta\vec{x}\right)$
- $f_{21} = \left(\frac{|\Delta x|}{c},\; \vec{X}_1 - \vec{X}_2\right) = \left(\frac{|\Delta x|}{c},\; -\Delta\vec{x}\right)$
- $p_{12} = \left(-\frac{|\Delta x|}{c},\; \Delta\vec{x}\right)$
- $p_{21} = \left(-\frac{|\Delta x|}{c},\; -\Delta\vec{x}\right)$

where $\Delta\vec{x} = \vec{X}_2 - \vec{X}_1$.

Note that $p_{21} = -f_{12}$ and $p_{12} = -f_{21}$.

These four vectors represent the only possible direct communication paths between $x_1$ and $x_2$ using massless particles. They also represent the space and time reflections of a null vector. Writing the space reflection operator as $\mathcal{S}$ and the time reflection operator as $\mathcal{T}$, we have:

$$f_{21} = \mathcal{S}(f_{12}), \quad p_{12} = \mathcal{T}(f_{12}), \quad p_{21} = \mathcal{T}(f_{21})$$
$$p_{21} = \mathcal{S}(p_{12}), \quad p_{21} = \mathcal{S}(\mathcal{T}(f_{12})) = -f_{12}, \quad p_{12} = \mathcal{T}(\mathcal{S}(f_{21})) = -f_{21}$$

From these relations we can work out the effect of $\mathcal{S}$ and $\mathcal{T}$ on spinors. Recognizing the "1" in the denominator of (25) as $t$ on the light cone, we may write:

$$\zeta = \frac{x + iy}{t - z}$$

and:

$$\mathcal{S}(\zeta) = \frac{-x - iy}{t + z} = -\frac{t - z}{x - iy} = -\frac{1}{\zeta^*}$$

$$\mathcal{T}(\zeta) = -\left(\frac{x + iy}{-t + z}\right) = -\frac{1}{\zeta^*}$$

*(for the definitions of space and time reflection)*

We then use the fact that:

$$x^2 + y^2 = t^2 - z^2$$

or $(x + iy)(x - iy) = (t - z)(t + z)$, or $\frac{x+iy}{t+z} = \frac{t-z}{x-iy}$, to write:

$$\mathcal{S}(\zeta) = -\left(\frac{x+iy}{t+z}\right) = -\frac{t-z}{x-iy} = -\frac{1}{\zeta^*}$$

Likewise:

$$\mathcal{T}(\zeta) = -\left(\frac{x+iy}{t+z}\right) = -\left(\frac{t+z}{x-iy}\right) = -\frac{1}{\zeta^*}$$

In terms of two-component spinors $\zeta = \xi/\eta$, the ambiguity in the definitions of $\xi$ and $\eta$ leaves some ambiguity in the definition of the action of $\mathcal{S}$ and $\mathcal{T}$ on them. For example, we might write:

$$\mathcal{S}(\xi/\eta) = -\eta^*/\xi^*$$

and say:

$$\mathcal{S}(\xi) = -\eta^*, \qquad \mathcal{S}(\eta) = \xi^*$$

etc. Yet this is rather ambiguous given the variability in $\eta$ and $\xi$.

### Stereographic Projection — Detailed Derivation (Revised)

*(Pages 121–124 present a rederivation for general sphere of radius $r$.)*

Sphere equation: $x^2 + y^2 + z^2 = r^2$

Parametric line from $(0,0,r)$ through $(\alpha, \beta)$ on the plane at $z=0$:

$$x = \alpha t, \quad y = \beta t, \quad z = r(1-t)$$

with $t = 0$ at top, $t=1$ at $(\alpha, \beta)$.

Substituting into the sphere equation:

$$(\alpha t)^2 + (\beta t)^2 + r^2(1-t)^2 = r^2$$

$$\frac{2r}{t} = r^2 + \alpha^2 + \beta^2 \quad \Rightarrow \quad t = \frac{2r}{r^2 + \alpha^2 + \beta^2}$$

If $\eta = \alpha + i\beta$:

$$x = \frac{r^2(\eta + \eta^*)}{r^2 + \eta\eta^*}, \qquad y = \frac{-ir^2(\eta - \eta^*)}{r^2 + \eta\eta^*}, \qquad z = r\cdot\frac{\eta\eta^* - r^2}{r^2 + \eta\eta^*}$$

And the inverse:

$$\eta = \frac{x + iy}{t} = \frac{x + iy}{r - z}$$

The $\eta = \frac{x+iy}{r-z}$ formula is independent of $r$, given that $x,y,z$ are on the sphere.

#### Inverse Stereographic Projection: Finding $(x_0, y_0)$

Given $(x_c, y_c, z_c)$ on the sphere and seeking $(x_0, y_0)$ on the plane:

$$x_c = \frac{2r^2 x_0}{r^2 + x_0^2 + y_0^2}, \quad y_c = \frac{2r^2 y_0}{r^2 + x_0^2 + y_0^2}, \quad z_c = r\left(\frac{x_0^2 + y_0^2 - r^2}{x_0^2 + y_0^2 + r^2}\right) \tag{30a,b,c}$$

Solving for $x_0$ (setting $y_0 = 0$ for simplicity and using a rotation to generalize):

$$x_c x_0^2 - 2r^2 x_0 + x_c r^2 = 0 \tag{32}$$

$$x_0^\pm = \frac{r}{x_c}\left(r \pm \sqrt{r^2 - x_c^2}\right) \tag{33}$$

Generally, there are two points on the sphere with $x = x_c$, one at $z_c$ and one at $-z_c$.

The spinor ratio:

$$\tilde{\zeta} = \frac{x_0 + iy_0}{r} \tag{34}$$

From similar triangles (Figure 1, stereographic projection):

$$\zeta^*_g = \frac{x_c + iy_c}{r - z_c} \tag{36}$$

Note that $x_0^+ x_0^- = r^2$ (37) and $\frac{x_0}{r} = \frac{r}{x_0^+}$ (38).

From Figure 2:

$$\frac{x_c}{r - z_c} = \frac{r + z_c}{x_c} \tag{39}$$

or when rotated:

$$\frac{x_c + iy_c}{r - z_c} = \frac{r + z_c}{x_c - iy_c} \tag{40}$$

Comparing these results with (23a) and (23b), we may see that the **stereographic projection defines a unique complex number $\zeta$ which is the ratio of the two spinor components of a null quaternion treated as a pair of spinors.** In other words, we must treat this as two separate projections from the antipodes. The "top" involves a rotation by $\theta$ and the bottom by $-\theta$.

It would be nice to show that all of the ambiguity in the spinor is due to the arbitrariness of the projection.

---

## Pages 127–140 — Spinor Functions

*(New spiral-bound notebook, repeats/continues spinor paper)*

### Spinor Functions

A spinor function $\Psi(x)$ assigns a spinor — a direction-without-magnitude — to each point of spacetime. We would like to investigate how equations of motion for spinor functions act on the various forms of the spinor. Let's consider the basic equation:

$$\sigma^\mu \partial_\mu \Psi = (\partial_0 - \sigma^i \partial_i)\Psi = 0$$

If we write:

$$\Psi = \begin{pmatrix} \eta \\ \xi \end{pmatrix}$$

then:

$$\partial_0 \begin{pmatrix} \eta \\ \xi \end{pmatrix} = \begin{pmatrix} 0 & \partial_x - i\partial_y \\ \partial_x + i\partial_y & 0 \end{pmatrix} \begin{pmatrix} \eta \\ \xi \end{pmatrix} + \begin{pmatrix} \partial_z & 0 \\ 0 & -\partial_z \end{pmatrix} \begin{pmatrix} \eta \\ \xi \end{pmatrix}$$

or:

$$\partial_0 \eta = \partial_x \xi - i\partial_y \xi + \partial_z \eta$$
$$\partial_0 \xi = \partial_x \eta + i\partial_y \eta - \partial_z \xi$$

Rewriting:

$$(\partial_0 - \partial_z)\eta = (\partial_x - i\partial_y)\xi \tag{1a}$$
$$(\partial_0 + \partial_z)\xi = (\partial_x + i\partial_y)\eta \tag{1b}$$

Can we write an equation for the spinor ratio $\eta/\xi$? Write $\varphi_g = \eta/\xi$, then $\eta = \varphi\xi$. Substituting into (1a) and (1b):

$$(\partial_0 - \partial_z)\varphi\xi = (\partial_x - i\partial_y)\xi = \varphi(\partial_0 - \partial_z)\xi + (\partial_0 + \partial_z)\varphi \cdot \xi$$
$$-(\partial_0 + \partial_z)\xi = (\partial_x + i\partial_y)(\varphi\xi) = \xi(\partial_x + i\partial_y)\varphi + \varphi(\partial_x + i\partial_y)\xi$$

This seems an intractable mess! Do we need to write a 2nd-order equation out of it?

$$(\partial_0 + \partial_z)(\partial_0 - \partial_z)(\varphi\xi) = (\partial_0 + \partial_z)\left[\varphi(\partial_0 - \partial_z)\xi + \xi(\partial_0 - \partial_z)\varphi\right]$$
$$= (2\partial_0 + \partial_z)\ldots$$

Taking (1b) and applying $(\partial_0 - \partial_z)$ to both sides, using (1a):

$$(\partial_0^2 - \partial_z^2)\xi = (\partial_0 - \partial_z)(\partial_x + i\partial_y)\eta = (\partial_x + i\partial_y)(\partial_x - i\partial_y)\xi = (\partial_x^2 + \partial_y^2)\xi$$

or:

$$(\partial_0^2 - \nabla^2)\xi = 0 \tag{2b}$$

Likewise we can show $(\partial_0^2 - \nabla^2)\eta = 0$ (2a), whereby we have the wave equation for $\xi$ and $\eta$.

Writing $\varphi = \eta/\xi$ and then $\eta = \varphi\xi$:

$$(2b') \quad (\partial_0^2 - \nabla^2)(\varphi\xi) = 0$$

$$\partial_0^2(ab) = \partial_0(a\partial_0 b + b\partial_0 a) = 2\partial_0 a\,\partial_0 b + a\partial_0^2 b + b\partial_0^2 a$$

So:

$$0 = \xi\partial_0^2\varphi + \varphi\partial_0^2\xi + 2(\partial_0\varphi)(\partial_0\xi) - \xi\nabla^2\varphi - \varphi\nabla^2\xi - 2(\nabla\varphi)\cdot(\nabla\xi)$$

Applying (2a):

$$\xi(\partial_0^2\varphi - \nabla^2\varphi) = 2(\nabla\varphi)\cdot(\nabla\xi) - 2(\partial_0\varphi)(\partial_0\xi)$$

Could we split these, writing both:

$$\partial_0^2\varphi - \nabla^2\varphi = 0 \tag{3a}$$

and:

$$(\nabla\varphi)\cdot(\nabla\xi) - (\partial_0\varphi)(\partial_0\xi) = 0 \tag{3b}$$

Then interpreting (3a) as an equation of motion for $\varphi$ and (3b) as a "gauge" term?

Maybe we should work the other way. Suppose we have a 4-vector field $V_\mu(x)$. We want to constrain $V_\mu$ to be such that it is always on the light cone:

$$V_0^2(x) - V_x^2(x) - V_y^2(x) - V_z^2(x) = 0$$

and always unimodular. Both of these conditions impose constraints on $V_\mu(x)$ that should be expressible as differential equations.

Let us begin with the light-cone constraint. To simplify this, consider only one dimension. If $V_\mu(x_0)$ is on the light cone then:

$$V_0(t_0) = V_z(x_0) \tag{4}$$

Let us then write:

$$V_\mu(x_0 + \Delta x) = V_\mu(x_0) + \Delta x^\mu \partial_\mu V_\mu(x_0)$$

The light-cone constraint for $V_\mu(x_0 + \Delta t)$ is then:

$$V_0(x_0 + \Delta x) + \Delta x^0\partial_0 V_0 + \Delta x^1\partial_1 V_0 = V_1(x_0) + \Delta x^0\partial_0 V_1 + \Delta x^1\partial_1 V_1$$

and applying (4):

$$\Delta x^0\partial_0 V_0 - \Delta x^1\partial_1 V_0 = \Delta x^0\partial_0 V_1 - \Delta x^1\partial_1 V_1$$

or, generalizing:

$$\Delta x^\mu \partial_\mu V_0 = \Delta x^\mu \partial_\mu \vec{V}$$

and for any $\Delta x^\mu$:

$$\boxed{V^\mu \partial_\mu V_0 = \vec{\Delta x}\cdot\nabla V_\mu}$$

We'd like to eliminate the $\Delta x$'s and get an equation in $V$. Think about this in 2-d again: if $V_0(x_0) = u_0$ then $V_1(x_0) = \pm u_0$, so that $V_0^2(x_0) - V_1^2(x_0) = 0$.

From the unimodular condition plus the light-cone constraint we derive (in 4D):

$$\boxed{V^\mu \partial_\nu V_\mu = 0}$$

This is the essential equation. And since $u^\mu = V^\mu(x_0)$, the field equation is:

$$\boxed{V^\mu \partial_\nu V_\mu = 0}$$

This reduces, in 2D, to:

$$V^0\partial_0 V_0 = V^1\partial_1 V_1, \qquad V^0\partial_1 V_0 = V^1\partial_1 V_1$$

*(It works, using the example above.)*

Now if we also constrain $V^\mu$ to have a fixed length, so that it becomes a direction-without-magnitude, then $V\cdot V = 1 = V_x^2 + V_y^2 + V_z^2$. The unit-length condition gives:

$$\boxed{\vec{V}\cdot(\partial_\mu\vec{V}) = 0}$$

Combining with $V^\mu\partial_\nu V_\mu = 0$, we also obtain $V^0\partial_\mu V_0 = 0$, whereby $V_0 = \text{const}$, which makes complete sense, and the vector equation tells us that $\vec{V}$ varies such that $\partial_\mu\vec{V}$ is at right angles to $\vec{V}$ for all $\mu = 0\ldots 3$. In other words, $\vec{V}$ varies from point to point only by a rotation.

If we convert this to a spinor, using $\zeta = \frac{x+iy}{t-z}$, or here $\zeta = \frac{V_1+iV_2}{V_0-V_3}$, or $\eta = V_1+iV_2$, $\xi = V_0-V_3$ with $\zeta = \eta/\xi$.

### Maxwell Equations from the Weyl Equation Applied to Null Vectors

$$\sigma^\mu\partial_\mu = \begin{pmatrix} \partial_0 - \partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_0 + \partial_z \end{pmatrix}$$

So:

$$\sigma^\mu\partial_\mu \begin{pmatrix} \eta \\ \xi \end{pmatrix} = \begin{pmatrix} (\partial_0-\partial_z)\eta + (\partial_x - i\partial_y)\xi \\ -(\partial_x+i\partial_y)\eta + (\partial_0+\partial_z)\xi \end{pmatrix} = 0 \tag{1}$$

With $\xi = V_x + iV_y = V_0 - V_z$ and $\eta = t - z$. Separating real and imaginary parts (since $V_\mu$ is real):

$$\partial_0 V_x - \partial_z V_x - \partial_x V_0 + \partial_x V_z = 0$$
$$\partial_0 V_y - \partial_z V_y + \partial_y V_0 - \partial_y V_z = 0$$
$$-\partial_x V_x + \partial_y V_y + \partial_0 V_0 + \partial_z V_0 - \partial_0 V_z + \partial_z V_0 = 0$$
$$\partial_y V_x - \partial_x V_y = 0$$

By symmetry, arguing therefore $\nabla \times \vec{V} = 0$, these reduce to:

$$\partial_0 V_x - \partial_z V_x + \partial_x V_z = 0 \tag{2a}$$
$$\partial_0 V_y + \partial_y V_0 = 0 \tag{2b}$$
$$\partial_0 V_0 + \partial_z V_0 - \nabla\cdot\vec{V} + 2\partial_y V_y = 0 \tag{2c}$$

By symmetry again:

$$\boxed{\partial_0 \vec{V} = -\nabla V_0} \tag{3b}$$

whereby:

$$\partial\partial_0 V_0 + \partial_0 V_0 - \nabla\cdot\vec{V} + 2\partial_y V_y = 0 \tag{3a}$$

and by symmetry:

$$\boxed{\partial_0 V_0 = \vec{\nabla}\cdot\vec{V}}$$

Considering the pair of equations simultaneously:

$$\sigma^\mu\partial_\mu\begin{pmatrix} \xi \\ \eta \end{pmatrix} = 0 \quad \text{and} \quad \sigma^\mu\partial_\mu\begin{pmatrix} \xi' \\ \eta' \end{pmatrix} = 0$$

If $\xi' = -\eta^*$ and $\eta' = \xi^*$, then these equations transform into:

- $(3b)$: $\partial_0\eta + \partial_z\eta - \partial_x\xi^* - i\partial_y\xi^* = 0$
- $(3a)$: $\partial_x\eta - i\partial_y\eta - \partial_0\xi^* + \partial_z\xi^* = 0$

These are the same as (1a) and (1b). But if we treat $\xi'$ and $\eta'$ as independent fields, we have more degrees of freedom.

**"Let me find grace in thy sight, oh Yahweh. Let I might see thy way here."**

These transform into Maxwell equations. 4-vectors are transformed into spinors by way of quaternions. Any 4-vector is a quaternion by virtue of:

$$q = \sigma^\mu V_\mu$$

and this is a $2\times2$ matrix of the form:

$$q = \begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

This $q$ consists of two spinors: $\frac{V_x - iV_y}{V_0 + V_z}$ and $\frac{V_0 - V_z}{V_x + iV_y}$.

Or if we prefer, two 2-component spinors:

$$\varphi_1 = \begin{pmatrix} V_0 - V_z \\ -V_x - iV_y \end{pmatrix}, \quad \varphi_2 = \begin{pmatrix} -V_x + iV_y \\ V_0 + V_z \end{pmatrix}$$

---

## Pages 141–160 — Spinors as Null Vectors; Vector Decomposition

### Light-Cone Field Equation (Boxed Result)

From the constraint that $V_\mu(x)$ always lies on the light cone and is unimodular:

$$\boxed{V^\mu\partial_\nu V_\mu = 0}$$

$$\boxed{\vec{V}\cdot(\partial_\mu\vec{V}) = 0}$$

And combining: $V^0\partial_\mu V_0 = 0$.

### Is a Spinor a Null Vector?

Write a 4-vector as:

$$V = \sigma^\mu V_\mu = \begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

If $V$ is a null vector, $V^\mu V_\mu = 0$, and then the left-hand and right-hand columns are equal within a constant $k$:

$$\frac{V_0 - V_z}{-V_x - iV_y} = \frac{-V_x + iV_y}{V_0 + V_z}$$

which gives $V_0^2 - V_z^2 = V_x^2 + V_y^2$, i.e., $V^\mu V_\mu = 0$.

If we alternatively write $V = \sigma^\mu V_\mu$ as a tensor product:

$$(k_1 \quad k_2) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} k_1\alpha & k_2\alpha \\ k_1\beta & k_2\beta \end{pmatrix}$$

This tensor product always represents a null vector if $k_1\alpha$ is real (which requires $k_1 = k_0\alpha^*$, $k_2 = k_0'\beta^*$ where $k_0, k_0'$ are real). Thus:

$$\sigma^\mu V_\mu = (k_0\alpha^* \quad k_0'\beta^*) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$$

where $k_0' = k_0$. The spinor $\begin{pmatrix} \alpha \\ \beta \end{pmatrix}$ with complex $\alpha$ and $\beta$ forms a null vector via the tensor product $(\alpha^*\;\beta^*) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$.

### Decomposition of Any Vector into Two Null Vectors

Can any vector $V_\mu$ (not null) be composed of two null vectors?

$$V_\mu = a_\mu + b_\mu, \qquad a^\mu a_\mu = 0, \quad b^\mu b_\mu = 0$$

$$V^\mu V_\mu = 2a^\mu b_\mu$$

For a timelike $V_\mu = (t, \vec{V})$, a possible decomposition is:

$$\boxed{V_\mu = \left(\frac{1}{2}(t + |\vec{V}|),\; \frac{1}{2}(\vec{V} + \hat{V}\,t)\right) + \left(\frac{1}{2}(t - |\vec{V}|),\; \frac{1}{2}(\vec{V} - \hat{V}\,t)\right)}$$

$$= \frac{1}{2}\left(1 + \frac{V_0}{|\vec{V}|}\right)(|\vec{V}|,\; \vec{V}) + \frac{1}{2}\left(1 - \frac{V_0}{|\vec{V}|}\right)(-|\vec{V}|,\; \vec{V})$$

This is a possible decomposition, but not the only one. $(t, 0)$ can break down into $(t/2, \hat{u}\,t/2) + (t/2, -\hat{u}\,t/2)$ for any unit vector $\hat{u}$.

### Classification of $V_\mu$ by Type

| $V_\mu$ | $V_0$, $|\vec{V}|$ | $1 + V_0/|\vec{V}|$ | $1 - V_0/|\vec{V}|$ |
|---|---|---|---|
| + timelike | $V_0 > |\vec{V}|$ | $> 1$ | $< 0$ |
| − timelike | $V_0 < -|\vec{V}|$ | $< 0$ | $> 1$ |
| + spacelike | $V_0 < |\vec{V}|$ | $> 1$ | $> 1$ |
| − spacelike | $V_0 > -|\vec{V}|$ | $> 1$ | $> 0$ |

Two possible decompositions for spacelike, only 1 for timelike. On the spacelike, we can switch the signs of both — just the order is all that changes.

*(Two light-cone diagrams drawn showing decomposition geometry for timelike and spacelike cases. Intersection of two light cones is a hyperbolic or elliptic surface generally.)*

- Timelike points → ellipse
- Spacelike points → 2 hyperbolas
- The ellipse and hyperbolas are 2D surfaces, generally

### Solution for Timelike $V_\mu$

For timelike $V_\mu$: consider 2 points, $a_\mu$ and $0$. Then $V_\mu = a_\mu + b_\mu$ where $a_\mu$ is on the 0-light cone and $b_\mu$ is on the light cone for $V_\mu$:

$$a^\mu a_\mu = 0 \quad (a), \qquad (V_\mu - a_\mu)(V^\mu - a^\mu) = 0 \quad (b)$$

So: $V_\mu V^\mu - 2a_\mu V^\mu + a_\mu a^\mu = V^\mu V_\mu - 2a^\mu V_\mu = 0$

Writing $v^2 = V^\mu V_\mu \neq 0$:

$$2a^\mu V_\mu = v^2 \qquad (b')$$

and $a_0^2 = a_x^2 + a_y^2 + a_z^2 \quad (a')$.

Pick any direction $\hat{a}$. Then:

$$a_\mu = (a_0, a_0\hat{a}) \quad \text{is a null vector}$$

$$V_\mu = a_\mu + b_\mu = a_\mu + (V_\mu - a_\mu)$$

Both $a_\mu$ and $V_\mu - a_\mu$ on the light cone:

$$a^\mu a_\mu = 0, \qquad (V_\mu - a_\mu)(V^\mu - a^\mu) = 0$$

$$(V_\mu - a_\mu)(V^\mu - a^\mu) = V_\mu V^\mu - 2V_\mu a^\mu + a_\mu a^\mu = 0$$

$$v^2 = V_\mu V^\mu = 2V_\mu a^\mu = 2V^\mu a_\mu = 2a_0 V_0 - 2\hat{a}\cdot\vec{V} \cdot a_0$$

which can be solved for $a_0$:

$$\boxed{a_\mu = \frac{1}{2V_0}\left(V_0^2 - |\vec{V}|^2 + 2\hat{a}\cdot\vec{V}\right)(1,\;\hat{a})}$$

$$\boxed{b_\mu = V_\mu - a_\mu}$$

**This is valid for all positive timelike $V_\mu$.**

Note that $\sqrt{V_\mu V^\mu} = \det(\sigma^\mu V_\mu)$.

---

## Pages 161–175 — Maxwell Equations from Spinor; Final Stereographic Results

### Weyl Operator Acting on a Vector/Quaternion

$$\sigma^\mu\partial_\mu\Psi = \begin{pmatrix} \partial_0 - \partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_0 + \partial_z \end{pmatrix}\begin{pmatrix} \psi_1 \\ \psi_2 \end{pmatrix} = 0$$

Acting on the quaternion $\sigma^\mu V_\mu$:

$$\begin{pmatrix} \partial_0 - \partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_0 + \partial_z \end{pmatrix}\begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

The result expands to four equations, two from each row. Writing them out with real $V_\mu$:

$$(\partial_0 - \partial_z)(V_0 - V_z) + (\partial_x - i\partial_y)(V_x + iV_y) = 0 \tag{1a}$$
$$(\partial_x + i\partial_y)(V_0 - V_z) + (\partial_0 + \partial_z)(V_x + iV_y) = 0 \tag{1b}$$

$$(\partial_0 - \partial_z)(V_x - iV_y) + (\partial_x - i\partial_y)(V_0 + V_z) = 0 \tag{2a}$$
$$(\partial_x + i\partial_y)(V_x - iV_y) + (\partial_0 + \partial_z)(V_0 + V_z) = 0 \tag{2b}$$

Separating real and imaginary parts (since $V_\mu$ is real):

From (1a):
$$\partial_0 V_0 + \partial_z V_z - \partial_z V_0 - \partial_0 V_z + \partial_x V_x - \partial_y V_y + \partial_y V_x + \partial_x V_y = 0 \quad \text{Re(1a)}$$

From Im(1a): $\partial_x V_y - \partial_y V_x = 0$ ✓

By symmetry and combining equations:

$$(\nabla\times\vec{V})_z = 0 \Rightarrow \nabla\times\vec{V} = 0 \tag{2d}$$

$$\partial_0\vec{V} = -\nabla V_0 \tag{7}$$

$$\nabla\times\vec{V} = 0 \tag{8}$$

$$\vec{\nabla}\cdot\vec{V} = -\partial_0 V_0 \tag{9}$$

Adding and subtracting Re(1b) and Re(2a):

$$\partial_0 V_x + \partial_x V_0 = 0 \tag{4+} \checkmark$$
$$\partial_z V_x - \partial_x V_z = 0 \tag{4-} \checkmark$$

Adding and subtracting Re(2b) and Re(1a):

$$\partial_0 V_0 + \partial_x V_x + \partial_y V_y + \partial_z V_z = 0 \tag{5+} \checkmark$$
$$\partial_z V_0 + \partial_0 V_z = 0 \tag{5-} \checkmark$$

**These are Maxwell-like equations to be sure:**

$$\nabla\times\vec{B} = -\partial_0\vec{E}, \qquad \vec{\nabla}\cdot\vec{B} = 0$$
$$\nabla\times\vec{E} = \partial_0\vec{B}, \qquad \vec{\nabla}\cdot\vec{E} = 0$$

in source-free form. There is no $E_0$, $B_0$ here.

### Wave Equation from (7) and (9)

Applying (9) to (7):

$$\partial_0(\nabla V_0) = -\partial_0^2\vec{V} = \nabla(\partial_0 V_0) = -\nabla(\nabla\cdot\vec{V})$$

And for $\nabla\times\vec{V} = 0$:

$$= \nabla^2\vec{V}$$

So (7), (8), and (9) together give:

$$\boxed{\partial_0^2\vec{V} = \nabla^2\vec{V}} \tag{10}$$

which is the standard wave equation.

At this level it appears that $\vec{V}$ is completely decoupled from $V_0$, and $V_0$ is defined as a sort of ancillary field for which:

$$\nabla V_0 = -\partial_0\vec{V}, \qquad \partial_0 V_0 = -\vec{\nabla}\cdot\vec{V}$$

Now suppose $\vec{V} = v\hat{z}\,e^{i(kz-\omega t)}$. Then requiring $k^2 = \omega^2$ for (10):

$$\partial_0\vec{V} = -i\omega v\hat{z}\,e^{i(kz-\omega t)}$$

so $\nabla V_0 = i\omega v\hat{z}\,e^{i(kz-\omega t)}$ and $\vec{\nabla}\cdot\vec{V} = ikv\hat{z}\,e^{i(kz-\omega t)}$, giving:

$$V_0 = v\,e^{i(kz-\omega t)} \quad \text{if and only if } k = \omega \text{ (not } k = -\omega\text{)}$$

So: $(\partial_0^2 - \nabla^2)V_\mu = 0 \tag{11}$

### Null Vector Constraint Equations

Now, suppose $V_\mu$ is a null vector. Then $V_0$ is essentially determined by $\vec{V}$:

$$V_0 = \sqrt{V_x^2 + V_y^2 + V_z^2}$$

Can equations (7) and (9) be satisfied?

$$\nabla V_0 = \nabla\sqrt{V_x^2 + V_y^2 + V_z^2} = \frac{1}{2V_0}(2V_x\partial_x V_x + 2V_y\partial_y V_y + 2V_z\partial_z V_z)\,\ldots$$

$$= \frac{1}{\vec{V}_0}\vec{V} = -\partial_0\vec{V}$$

or:

$$V_0\partial_0\vec{V} = -\vec{V} \tag{12}$$

From (12), write $\partial_0\vec{V} = -\vec{V}/V_0$ and combine with (13) to get:

$$V_0(\vec{\nabla}\cdot\vec{V}) = -\vec{V}\cdot(\partial_0\vec{V})$$

$$\vec{\nabla}\cdot\vec{V} = \frac{\vec{V}\cdot\vec{V}}{V_0^2} = 1$$

but from (7): $\vec{\nabla}\cdot\vec{V} = -\partial_0 V_0$

Working this through carefully:

$$-V_0\partial_0\vec{V} = V_j\partial_j V_j \quad j = x,y,z \tag{14'}$$
$$V_0\vec{\nabla}\cdot\vec{V} = -\vec{V}\cdot\partial_0\vec{V} \tag{15'}$$

### Transverse vs Longitudinal Waves

If $\nabla\times\vec{V} = 0$, can $\vec{V}$ exist as a longitudinal or transverse wave?

This is the "spin-0 condition." If $\vec{V} = v\hat{z}\,e^{i(kz-\omega t)}$, then $\partial_z V_z \neq 0$ but $\partial_x V_z$, $\partial_y V_z$ etc. are all 0, so $\nabla\times\vec{V} = 0$ and longitudinal waves are OK.

A pure transverse wave, e.g., $\vec{V} = v\hat{x}\,e^{i(kz-\omega t)}$, has $\partial_z V_x \neq 0$ but $\partial_x V_z = 0$, so it is **not allowed**. One way or another, this drives us to a **pure longitudinal wave**.

### Stereographic Projection — Summary (Numbered Paper, Pages 20–21)

*Figure 1: Stereographic projection diagram — sphere of radius $r$ with point $(x_c, y_c, z_c)$ on the sphere and $(x_0, y_0)$ on the plane at $z=0$.*

We may compute $(x_0, y_0)$ for any given $(x_c, y_c, z_c)$ by parametrizing the line:

$$x(t) = x_0 t \tag{27a}$$
$$y(t) = y_0 t \tag{27b}$$
$$z(t) = r(1-t) \tag{27c}$$

Now, at $(x_c, y_c, z_c)$ the sphere equation is satisfied:

$$(x_0 t)^2 + (y_0 t)^2 + r^2(1-t)^2 = r^2 \tag{28}$$

Solving for $t$:

$$t = \frac{2r^2}{r^2 + x_0^2 + y_0^2} \tag{29}$$

So:

$$x_c = \frac{2r^2 x_0}{r^2 + x_0^2 + y_0^2}, \qquad y_c = \frac{2r^2 y_0}{r^2 + x_0^2 + y_0^2}, \qquad z_c = r\cdot\frac{x_0^2 + y_0^2 - r^2}{x_0^2 + y_0^2 + r^2} \tag{30a,b,c}$$

The inverse solutions for $(x_0, y_0)$ in terms of $(x_c, y_c, z_c)$ (taking $y_c = 0$ for simplicity):

$$x_c = \frac{2r^2 x_0}{r^2 + x_0^2} \tag{31}$$

or:

$$x_c x_0^2 - 2r^2 x_0 + x_c r^2 = 0 \tag{32}$$

with solutions:

$$x_0^\pm = \frac{r}{x_c}\left(r \pm \sqrt{r^2 - x_c^2}\right) \tag{33}$$

Generally speaking, there are two points on the sphere with $x = x_c$, one at $z_c$ and one at $-z_c$.

The quantities $x_0/r$ and $y_0/r$ depend only on the direction. These may be written as a complex number:

$$\tilde{\zeta} = \frac{x_0 + iy_0}{r} \tag{34}$$

From the law of similar triangles, we see from Figure 1 that $\frac{x_c}{r - z_c} = \frac{x_0}{r}$, so:

$$\zeta^*_g = \frac{x_c + iy_c}{r - z_c} \tag{36}$$

Note that $x_0^+ x_0^- = r^2$ (37) and $\frac{x_0}{r} = \frac{r}{x_0^+}$ (38).

From Figure 2:

$$\frac{x_c}{r - z_c} = \frac{r + z_c}{x_c} \tag{39}$$

or when rotated:

$$\frac{x_c + iy_c}{r - z_c} = \frac{r + z_c}{x_c - iy_c} \tag{40}$$

Comparing with (23a) and (23b), we may see that the stereographic projection defines a unique complex number $\zeta$ which is the ratio of the two spinor components of a null **quaternion** treated as a pair of spinors.

We must treat this as two separate projections from the antipodes. The "top" involves a rotation by $\theta$ and the bottom by $-\theta$. Be exact here, and explain carefully. We want to fully understand the quaternion $V$. Use $V_\mu$ not $x_\mu$. Fully explore the arbitrariness of the Z axis and the inherent ambiguity in the spinor.

**★ It would be nice to show that all of the ambiguity in the spinor is due to the arbitrariness of the projection.**

---

## Pages 176–182 — Construction of Null Vectors; Spinor Paper Outline

### Two Coordinate Systems

Consider two separate coordinate systems and their respective stereographic representations $(x_s, y_s, z_s)$ versus $(x_s', y_s', z_s')$ and $(x_0, y_0)$ vs $(x_0', y_0')$.

Rotation about $z$: changes overall phase of $(x_0, y_0)$, sending $x_0 + iy_0 \to e^{i\theta}(x_0 + iy_0)$.

- $Z$ determined by direction of motion of photon
- $R$ of sphere determines relative magnitude
- What is overall phase?

### Outline for Spinor Paper

*(Marked with × for to-do items)*

1. Deal with null vectors as tensor products
2. Discuss breakdown of non-null vectors into 2 null vectors
3. Discuss equations of motion of spinor field

### Construction of Null Vectors as Tensor Products

$$(\alpha^* \quad \beta^*) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} \alpha\alpha^* & \beta^*\alpha \\ \alpha^*\beta & \beta^*\beta \end{pmatrix} = \begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

So $\det Q = \alpha\alpha^*\beta\beta^* - \alpha^*\beta\alpha\beta^* = 0$ ✓

$$\alpha\alpha^* = V_0 - V_z, \qquad \beta\beta^* = V_0 + V_z, \qquad \alpha^*\beta = -V_x - iV_y$$

Write:

$$\alpha = \sqrt{V_0 - V_z}\,e^{i\theta}, \qquad \beta = \sqrt{V_0 + V_z}\,e^{i\phi}$$

$$\alpha^*\beta = \sqrt{(V_0-V_z)(V_0+V_z)}\,e^{i(\phi-\theta)} = \sqrt{V_0^2 - V_z^2}\,e^{i(\phi-\theta)} = \sqrt{V_x^2+V_y^2}\,e^{i(\phi-\theta)}$$

so:

$$\frac{V_x + iV_y}{\sqrt{V_x^2 + V_y^2}} = -e^{i(\phi-\theta)}$$

**Ambiguity of $e^{i\theta}$ key.**

### Null Matrix Factorization

A matrix $M = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ with $\det(M) = ad - bc = 0$:

$$ad = bc \quad \Rightarrow \quad \frac{a}{b} = \frac{c}{d} \quad \text{and} \quad \frac{a}{c} = \frac{b}{d}$$

So if $b = \alpha a$ then $c = \alpha d$; if $c = \beta a$ then $d = \beta b$; so:

$$M = \begin{pmatrix} a & \alpha a \\ \beta a & \alpha\beta a \end{pmatrix} = a\begin{pmatrix} 1 & \alpha \end{pmatrix} \otimes \begin{pmatrix} 1 \\ \beta \end{pmatrix}, \quad \alpha = b/a$$

### Timelike Decomposition (Final Form)

1) **Timelike** — diagram shows $a$ and $b$ both future-pointing with $a + b = b + a = V$:

$$\frac{1}{2}(V_0^2 - |\vec{V}|^2)^{1/2} = a_0(V_0 - \hat{a}\cdot\vec{V})$$

2) **Spacelike** — diagram shows $a + b = V = b + a$

**Timelike:** $a_\mu = (a_0, a_0\hat{a})$ is a null vector.

$$V_\mu = a_\mu + b_\mu = a_\mu + (V_\mu - a_\mu)$$

For both $a_\mu$ and $V_\mu - a_\mu$ on the light cone:

$$a^\mu a_\mu = 0, \qquad (V_\mu - a_\mu)(V^\mu - a^\mu) = 0$$

$$(V_\mu - a_\mu)(V^\mu - a^\mu) = V_\mu V^\mu - 2V_\mu a^\mu + a_\mu a^\mu = 0$$

$$v^2 \equiv V_\mu V^\mu = 2V_\mu a^\mu = 2a_0 V_0 - 2a_0(\hat{a}\cdot\vec{V})$$

which can be solved for $a_0$:

$$a_0 = \frac{1}{2V_0}(V_0^2 - |\vec{V}|^2 + 2\hat{a}\cdot\vec{V})$$

$$\boxed{a_\mu = \frac{1}{2V_0}(V_0^2 - |\vec{V}|^2 + 2\hat{a}\cdot\vec{V})(1,\;\hat{a})}$$

### Final Calculation — Null Component Geometry (Last Pages)

$$a_0 = \frac{1}{2V_0}(V_0^2 - |V|^2 + 2\hat{a}\cdot\vec{V}) = b + \hat{a}\cdot\vec{u}$$

where $\hat{a} = \frac{a_x\hat{x} + a_y\hat{y} + a_z\hat{z}}{\sqrt{a_x^2 + a_y^2 + a_z^2}}$, $b = \frac{V_0^2 - |V|^2}{2V_0}$, $\vec{u} = \frac{\vec{V}}{V_0}$.

If $\vec{V}$ is along the $\hat{z}$ axis, then $u_x = u_y = 0$ and:

$$a_0(V_0 - a_z V_z) = \frac{1}{2}(V_0^2 - V_z^2)$$

$$\sqrt{a_x^2 + a_y^2 + a_z^2} = a_0 = \frac{1}{4}\cdot\frac{(V_0^2 - V_z^2)}{(V_0 - a_z V_z)^2}$$

$$a_x^2 + a_y^2 + \left(a_z - \frac{1}{2}V_z\right)^2 = \frac{1}{4}\alpha, \qquad \alpha = 1 - \frac{V_z^2}{V_0^2}$$

where $\alpha > 0$ if $|V_z| < |V_0|$ (timelike) and $\alpha < 0$ if $|V_z| > |V_0|$ (spacelike).

In cylindrical coordinates:

$$\rho_s = \frac{2r\,\rho_0}{r^2 - \rho^2}, \qquad \theta_s = \theta_0$$

*(End of notebook)*

---

*Transcribed 2026-05-22 — 11:35*
