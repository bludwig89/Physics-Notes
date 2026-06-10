# Physics Notes — Pages 61–90

Source: `physics_notes_0708.pdf`, pages 61–90 of 182.

This batch is dominated by an extended investigation into the **Weinberg–Salam electroweak model without the Higgs mechanism** (pages 62–72), followed by a short "Mass & rotational travel" musing (pages 73–74), reference data lifted from a high-energy-physics conference volume (pages 75–76), and a long technical exercise translating Dirac plane-wave solutions from the standard to the Weyl representation and isolating the four chirality/charge-conjugation pieces (pages 81–89).

---

## Page 61 — Weak Interactions

1. The weak interaction bosons, $W_\pm, Z$, act only on the **left**-handed half of the Dirac spinor of a 4-spinor.
2. The electromagnetic interaction boson, $\gamma$ or $A$, acts only on the **bottom** part of the 4-spinors
   $$\binom{\nu_L}{e_L}\qquad \binom{\nu_R}{e_R}$$
3. The $L \leftrightarrow R$ interaction creates, or defines, mass. $W_\pm$ and $Z$, which make a distinction here, have mass. Does their having mass have to do with the $L$-only coupling? Or does it have to do with its charge?
4. *(blank — author started numbering a 4th point but did not continue)*

---

## Page 62 — Weinberg–Salam w/o Higgs

We try to formulate W–S without the Higgs since it isn't physical, and we don't worry about renormalizability or gauge violation of mass terms yet.

Introduce 2 fields, $\vec W^\mu$ an $SU(2)$ field and $W_0^\mu$, a $U(1)$ field. Call
$$L = \binom{\nu_L}{e_L}, \qquad R = \binom{\nu_R}{e_R}.$$

Then
$$\vec G^{\mu\nu} = \partial^\mu \vec W^\nu - \partial^\nu \vec W^\mu - g\, \vec W^\mu \times \vec W^\nu$$
$$H^{\mu\nu} = \partial^\mu W_0^\nu - \partial^\nu W_0^\mu$$

and
$$\mathcal L = -\tfrac14\!\left(\vec G^{\mu\nu}\!\cdot\!\vec G_{\mu\nu} + H^{\mu\nu} H_{\mu\nu}\right) \;-\; m_\nu c^2\!\left(\bar L_\nu R_\nu + \bar R_\nu L_\nu\right) \;-\; m_e c^2\!\left(\bar L_e R_e + \bar R_e L_e\right)$$
$$\hphantom{\mathcal L =}\; + \bar L\, i\,\bar\sigma^\mu D^L_\mu L \;+\; \bar R\, i\,\bar\sigma^\mu D^R_\mu R$$

with covariant derivatives
$$D^L_\mu \equiv \partial_\mu + i g\, \vec W_\mu \!\cdot\! \vec\tau + i g'\, W_{0\mu}\, \tau_0 \qquad (\text{where } \tau_a = \tfrac{1}{2}\sigma_a \text{ on the } \nu\text{-}e\text{ doublet})$$
$$D^R_\mu \equiv \partial_\mu + i e\, A_\mu (\tau_3 - \tau_0)$$

and $A_\mu$ is a linear combination of $W_0$ and $W_3$. Part of our problem here is that conventional W–S throws out $\nu_R$ and makes $e_R$ a singlet. That's stupid because it destroys the basic ⟶

---

## Page 63

⟶ symmetry between $\binom{\nu_R}{e_R}$ and $\binom{\nu_L}{e_L}$ which is the key to deeper understanding. Now if we give $\vec W$ and $W_0$ masses, the mass term would be
$$\mathcal L_m = \tfrac12 m_W^2 \vec W_\mu \!\cdot\! \vec W^\mu + \tfrac12 m_{W_0}^2 W_{0\mu} W_0^\mu$$
but of course these screw up the gauge symmetry, as terms that go as $W'_\mu = W_\mu + \partial_\mu \Theta$ aren't invariant.

Now W–S has $W_0$ coupling to both $e_L$ and $\nu_L$ and one wants an electromagnetic interaction that operates only on $e_L$. This is obtained by combining $W_0$ and $W_3$ in a linear combination. In other words, we have
$$(\bar\nu_L\ \bar e_L)\!\left(\partial_\mu + i g\, W^1_\mu \tau_1 + i g\, W^2_\mu \tau_2 + i g\, W^3_\mu \tau_3 + i g' W_{0\mu}\right)\!\binom{\nu_L}{e_L}$$

So the last two terms look like
$$i\!\begin{pmatrix} g + g' & 0 \\ 0 & -g + g' \end{pmatrix}\;\longrightarrow\; i\!\begin{pmatrix} g W^3_\mu + g' W^0_\mu & 0 \\ 0 & -g W^3_\mu + g' W^0_\mu\end{pmatrix}$$

So we want to write
$$W^3_\mu = Z_\mu \cos\theta - A_\mu \sin\theta \qquad Z_\mu = \cos\theta\, W^3_\mu + \sin\theta\, W^0_\mu$$
$$W^0_\mu = Z_\mu \sin\theta + A_\mu \cos\theta \qquad A_\mu = -\sin\theta\, W^3_\mu + \cos\theta\, W^0_\mu$$

in such a way that $A_\mu$ doesn't couple to $\nu_L$. That is,
$$g\, W^3_\mu + g'\, W^0_\mu = \alpha\, Z_\mu$$

---

## Page 64

or, substituting,
$$\alpha Z_\mu = g(Z_\mu \cos\theta - A_\mu \sin\theta) + g'(Z_\mu \sin\theta + A_\mu \cos\theta)$$
$$= (g\cos\theta + g'\sin\theta) Z_\mu + (g'\cos\theta - g\sin\theta) A_\mu$$

so
$$\boxed{\;\frac{g'}{g} = \tan\theta\;} \quad (*)$$
gives what we want — an $A_\mu$ that does not couple to $\nu_L$. We also want $A$'s coupling to $e_L$ to be $e$, so
$$g\, W^3_\mu + g'\, W^0_\mu = e A_\mu + \beta Z_\mu$$

so substituting,
$$g(Z_\mu \cos\theta - A_\mu \sin\theta) + g'(Z_\mu \sin\theta + A_\mu \cos\theta) = e A_\mu + \beta Z_\mu$$

and, separately,
$$g'\cos\theta + g\sin\theta \;\to\; e \quad\text{(should be }-g\sin\theta\text{ — sign flipped)}$$
$$g\cos\theta - g'\sin\theta = \beta$$

And using $(*)$ above,
$$e = g'\cos\theta - g\sin\theta = g\sin\theta + g\sin\theta = 2g\sin\theta$$
$$\beta = g\cos\theta - g'\sin\theta = g\cos\theta - g\tan\theta\sin\theta = \tfrac12 e\,(\cot\theta - \tan\theta)$$

*(margin: the author flips a sign somewhere; both forms are kept as written.)*

---

## Page 65

These results are in accord with Huey p. 108, 109. They're really not too extraordinary, in as much as such a rotation, in combination with $g, g'$ chosen at will, allows one to fit theory to experiment. It would appear strange that a massless vector boson $A_\mu$ should emerge from this. The right-handed doublet also poses problems! After all, it doesn't couple to $Z$ at all, and only to $A$. Yet the $A$ consists partly of $W^3_\mu$ and so by symmetry it should couple to $W_+, W_-$ too.

Let's look at the mass term
$$\mathcal L_m = \tfrac12 m_W^2 \vec W_\mu \!\cdot\! \vec W^\mu + \tfrac12 m_{W_0}^2 W_{0\mu} W_0^\mu$$
$$= \tfrac12 m_W^2 W_{\mu 1} W_1^\mu + \tfrac12 m_W^2 W_{\mu 2} W_2^\mu + \tfrac12 m_W^2 W_{\mu 3} W_3^\mu + \tfrac12 m_{W_0}^2 W_{0\mu} W_0^\mu$$

and substituting our formulae for $W_3$ and $W_0$, we get
$$\mathcal L_{m_{30}} = \tfrac12 m_W^2 W_{\mu 3} W_3^\mu + \tfrac12 m_{W_0}^2 W_{\mu 0} W_0^\mu$$
$$= \tfrac12 m_W^2 (Z_\mu \cos\theta - A_\mu \sin\theta)^2 + \tfrac12 m_{W_0}^2 (Z_\mu \sin\theta + A_\mu \cos\theta)^2$$
$$= \tfrac12 m_W^2 Z_\mu^2 \cos^2\theta + \tfrac12 m_W^2 A_\mu^2 \sin^2\theta - \tfrac12 m_W^2 Z_\mu A^\mu \sin\theta\cos\theta$$
$$\quad + \tfrac12 m_{W_0}^2 Z_\mu^2 \sin^2\theta + \tfrac12 m_{W_0}^2 A_\mu^2 \cos^2\theta + m_{W_0}^2 Z_\mu A_\mu \sin\theta\cos\theta$$

$$\Rightarrow\quad m_Z^2 = m_W^2 \cos^2\theta + m_{W_0}^2 \sin^2\theta$$
$$m_A^2 = m_W^2 \sin^2\theta + m_{W_0}^2 \cos^2\theta$$

W–S gets $\;m_Z^2 = \dfrac{m_W^2}{\cos^2\theta}$.

---

## Page 66

Perhaps a better way to see it is to say $m_W$ and $m_{W_0}$ are wholly from $m_Z$ and $m_A = 0$. Thus,
$$\tfrac12 m_Z^2 Z_\mu^2 = \tfrac12 m_W^2 W_3^2 + \tfrac12 m_{W_0}^2 W_0^2$$
$$Z_\mu = W_{3\mu}\cos\theta + W_{0\mu}\sin\theta$$
$$\tfrac12 m_Z^2 Z_\mu^2 = \tfrac12 m_Z^2 W_{3\mu}^2 \cos^2\theta + \tfrac12 m_Z^2 W_{0\mu}^2 \sin^2\theta + m_Z^2 W_{0\mu} W_{3\mu}\sin\theta\cos\theta$$

So $\;m_Z^2 \cos^2\theta = m_W^2 \quad\Longrightarrow\quad \boxed{\;m_Z^2 = \dfrac{m_W^2}{\cos^2\theta}\;}$

This is the W–S model prediction. However, there is an anomalous term,
$$\mathcal L_{\text{Anom}} = m_Z^2\, W_{0\mu} W_{3\mu}$$
and what happens to it? Presumably, it is transformed away or hidden somehow.

It seems like the kinetic term would pose a similar problem.

---

## Page 67

Now let's get some new ideas. $A_\mu$ works on the isospin vector just like $W$ works on the spin vector. In other words, $A_\mu$ couples to $\binom{\nu_L}{e_L}$ like
$$\begin{pmatrix} 0 & 0 \\ 0 & 1\end{pmatrix} = \tfrac12 (\tau_0 + \tau_3)$$
and $W$ couples to $\binom{e_R}{e_L}$ as
$$\begin{pmatrix} 0 & 0 \\ 0 & 1\end{pmatrix} = \tfrac12 (\sigma_0 + \sigma_3) \ldots \text{identical}.$$
This kind of cross coupling looks very elegant. Can we write a more concrete theory? A completely massless one to start? Or is the mass/charge fundamental and endemic to the theory?

OK, the mass terms take the form
$$mc^2 \bar\psi \psi = mc^2 (\bar R L + \bar L R)$$

So we have
$$\mathcal L_{\text{mass}} = m_e c^2 (\bar e_R e_L + \bar e_L e_R) + m_\nu c^2 (\bar\nu_R \nu_L + \bar\nu_L \nu_R)$$

The complement to this mass term in isospin space would be
$$\mathcal L_{\text{weak}} = g\,(\bar\nu_L e_L + \bar e_L \nu_L) + g'\,(\bar\nu_R e_R + \bar e_R \nu_R)$$

Interestingly $m_\nu \approx 0$ and $g' \approx 0$ and both interactions have the same nature. This is not at all a dynamically mediated force, but rather more like a contact force. But like mass, we should understand that it really arises dynamically, from a field.

---

## Page 68

It would appear that this is, or very nearly is, what the original Fermi theory of weak interactions comprised. Clearly it does not explain neutral currents, or the particulate nature of $W_\pm, Z$. Yet we might find these as we add kinetic and gauge terms.

The non-interacting kinetic term for the $\binom{e_R}{e_L}$ or $\binom{\nu_R}{\nu_L}$ takes the form
$$(\bar e_R\ \bar e_L)\!\left(\tfrac{\partial}{\partial t} - \sigma_3 \otimes \vec\sigma\!\cdot\!\nabla\right)\!\binom{e_R}{e_L}$$
etc. What would a complementary kinetic term be for the weak interaction? Presumably
$$(\bar\nu_L\ \bar e_L)\!\left(\tfrac{\partial}{\partial t} - \tau_3 \otimes \vec\sigma\!\cdot\!\nabla\right)\!\binom{\nu_L}{e_L}$$

Yet if we put one of these in, what is the need for the other? If we have an $\bar e_L \tfrac{\partial}{\partial t} e_L$ term for one, isn't it there for the other too? The big question appears to be, are these consistent? Can they be made consistent?

While we are at it, perhaps we should use a gauge field with them too. In other words, the pair $\binom{e_R}{e_L}$ can transform as $\psi_e \to e^{i\theta(x)} \psi_e$. However, at the same time, $\psi_\nu \to \psi_\nu$ because the charge of $\nu$ is $0$ and generally speaking $\psi \to e^{i Q \theta(x)} \psi$. Plainly then, a pair $\binom{\nu_L}{e_L}$ will not transform the same, and is not $U(1)$ symmetric for this gauge symmetry. Yet it ⟶

---

## Page 69

*(Two Feynman diagrams at the top:)*
- *Left: charged current.* $\nu_\mu \to \mu^- $ via $W^-$, with $\nu_e \to e^-$ on the other vertex. Labelled "charge current."
- *Right: neutral current.* $\nu_\mu \to \nu_\mu$ via $Z$, with $e^- \to e^-$ on the other vertex. Labelled "neutral current."

⟶ would appear that another $U(1)$ field could be introduced such that $\binom{\nu_L}{e_L} \to e^{i\phi(x)}\binom{\nu_L}{e_L}$ while $\binom{\nu_R}{e_R} \to \binom{\nu_R}{e_R}$. This gauge field would, in fact, provide the neutral currents we need, although it wouldn't particulate $W_\pm$.

If we call $A_\mu$ the usual electromagnetic field, and $B_\mu$ the new field, then the two kinetic terms would be of the form
$$i\hbar(\partial_0 + i g A_0)\!\binom{e_R}{e_L} - i\hbar c \sigma_3 \!\otimes\! \left[\vec\sigma\!\cdot\!(\nabla + i g\vec A)\right]\!\binom{e_R}{e_L}$$
$$+\; i\hbar(\partial_0 + i g A_0)\!\binom{\nu_R}{\nu_L} - i\hbar c \sigma_3\!\otimes\!\left[\vec\sigma\!\cdot\!(\nabla + i g\vec A)\right]\!\binom{\nu_R}{\nu_L}$$

and
$$i\hbar(\partial_0 + i g B_0)\!\binom{\nu_L}{e_L} - i\hbar c \sigma_3 \!\otimes\! \left[\vec\sigma\!\cdot\!(\nabla + i g\vec B)\right]\!\binom{\nu_L}{e_L}$$
$$+\; i\hbar(\partial_0 + i g_R B_0)\!\binom{\nu_R}{e_R} - i\hbar c \sigma_3\!\otimes\!\left[\vec\sigma\!\cdot\!(\nabla + i g_R \vec B)\right]\!\binom{\nu_R}{e_R}$$

where $g_\nu \approx 0$ and $g_R \approx 0$. Note that $g_\nu$ has nothing, per se, to do with $m_\nu$ and $g_R$ has nothing per se, to do with $g'$ in our "mass" equations, but, amazingly, $g_\nu = 0, m_\nu = 0, g_R = 0, g' \approx 0$, making a perfect symmetry between the two equations.

If I work out all of the kinetic terms, what do I get? Will I see a "why" to all of these zeros? Or understand why $B$ should end up with an effective mass? And all of this seems to have something to do with the gauging of the mass term.

Above all, we don't want **different** kinetic terms. If they all get doubled, we can absorb it somewhere, but if we have $2 \partial_0 e_R + \partial_0 e_R$ then we can't do that.

---

## Page 70

OK, the pure kinetic terms will be ($\hbar = c = 1$)
$$\binom{i\partial_0 e_R - i\vec\sigma\!\cdot\!\nabla e_R}{i\partial_0 e_L + i\vec\sigma\!\cdot\!\nabla e_L} \;+\; \binom{i\partial_0 \nu_R - i\vec\sigma\!\cdot\!\nabla \nu_R}{i\partial_0 \nu_L + i\vec\sigma\!\cdot\!\nabla \nu_L}$$
$$\binom{i\partial_0 \nu_L - i\vec\sigma\!\cdot\!\nabla \nu_L}{i\partial_0 e_L + i\vec\sigma\!\cdot\!\nabla e_L} \;+\; \binom{i\partial_0 \nu_R - i\vec\sigma\!\cdot\!\nabla \nu_R}{i\partial_0 e_R + i\vec\sigma\!\cdot\!\nabla e_R}$$

Combining terms, we have
$$\binom{i\bar\sigma_\mu \partial^\mu e_R + i\sigma_\mu \partial^\mu \nu_R + i\sigma_\mu \partial^\mu \nu_L}{2 i\sigma_\mu \partial^\mu e_L + i\sigma_\mu \partial^\mu \nu_L + i\sigma_\mu \partial^\mu e_R}$$
where $\sigma_\mu \partial^\mu = \partial_0 - \vec\sigma\!\cdot\!\nabla$, $\;\bar\sigma_\mu \partial^\mu = \partial_0 + \vec\sigma\!\cdot\!\nabla$, and we do get inconvenient factors of 2 here. If we flip $\binom{e_R}{e_L} \to \binom{e_L}{e_R}$ as I think we may need to, then the kinetic terms become
$$\binom{i\bar\sigma_\mu \partial^\mu e_L + 2 i\sigma_\mu \partial^\mu \nu_L + i\sigma_\mu \partial^\mu \nu_R}{2 i\sigma_\mu \partial^\mu e_R + i\bar\sigma_\mu \partial^\mu \nu_R + i\bar\sigma_\mu \partial^\mu e_L}$$

Now there is a 2 on both particles that couple to only one of $A_\mu, B_\mu$, and a single term for those that couple to both or neither. In any case all particles have 2 kinetic terms that don't cancel.

This is becoming an ugly way to write equations of motion like this. We shall instead use a quadruplet $(e_L\ e_R\ \nu_L\ \nu_R)$ or some such thing. I don't want to go that way yet — but only pursue the symmetry between the two separated equations to understand the neutral current.

---

## Page 71

The neutral current is mediated by $B_\mu$. In Lagrangian language it's something like
$$(\bar\nu_L\ \bar e_L)\!\left(-g_L (B_0 + \sigma_3 \vec B)\right)\!\binom{\nu_L}{e_L}$$
and equivalent to
$$(\bar e_L\ \bar e_R)\!\left(-e(A_0 + \sigma_3 \vec A)\right)\!\binom{e_L}{e_R}$$

This differs from Weinberg in that the cross-couplings $\nu_L e_L$ have a variable field acting between them, instead of a constant. The connection, where "mass" arises dynamically, is of great interest.

**Key questions:**

**Q)** Neutral current aside, what is the experimental evidence that the coupling between $\nu_L$ and $e_L$ is a particle, and not merely a mass term?

**A)** The obvious answer lies in the fact that a decay like $\mu^- \to e^- + \bar\nu_e + \nu_\mu$ exists. If it were merely a "mass term" it couldn't happen. You'd need higher order terms connecting $\mu$ and $e$, etc., unless of course the neutral current alone was responsible for all such transactions (which may be, but not by the Fermi-style representation of things). By particulizing the contact interaction, a $\mu, \nu_\mu$ doublet can give off a $W_-$ which then acts on an $e, \nu_e$ doublet easily enough.

**Q)** If $W_\pm$ are the dynamic expression of a contact term between $e, \nu_e$, then could there be a ⟶

---

## Page 72

⟶ similar dynamic nature to mass, e.g. the contact term $m(\bar e_L e_R + \bar e_R e_L)$ is really mediated by a boson of some sort?

**A)** That might be true.

**Q)** How would $\mu$ decay work in a mass-term-like theory with only a neutral current?

**A)**

i) $\mu_L$ couples to $\nu_L$ via a direct contact $\;\mu_L \times \nu_\mu\;$
ii) $\nu_\mu$ radiates a $B_\mu$, which then decays into a pair of $\bar\nu_e, e$'s. *(margin: "i.e. $\nu_e \bar\nu_e$.")* One $\nu_e$ turns into an $e$ by the contact interaction.

Clearly in this scenario, charge conservation is violated temporarily. This leads back to viewing charge as a dynamic quantity, not static, and the idea that a Heisenberg uncertainty principle is in operation for it too, like $\Delta p \Delta x \geq \hbar$, $\Delta E \Delta t \geq \hbar$. In a normal mass term, there are things like $\bar e_R \times e_L$ which make angular momentum get violated temporarily, too, e.g., $L_z$. Both charge and angular momentum seem to have to do with a rotational variable too.

---

## Page 73 — Mass & rotational travel

Suppose that a particle, rather than being able to travel in a straight line $\longrightarrow$ had to travel in a helical spiral *(little drawn helix)*. Then it would have a lower forward velocity.

To describe a helix in $x$-$y$-$z$ space, we suppose the direction of travel is along $z$, and the helix has diameter $r$ and frequency $\nu$. Thus,
$$\vec X(t) = r\cos(2\pi\nu t)\,\hat x + r\sin(2\pi\nu t)\,\hat y + a t\,\hat z$$

We wish to find $\dfrac{dz}{dt}$ as a function of $|\vec v|$.
$$\vec v(t) = \dot{\vec X}(t) = -2\pi\nu r \sin(2\pi\nu t)\,\hat x + 2\pi\nu r\cos(2\pi\nu t)\,\hat y + a\,\hat z$$
$$\vec v\!\cdot\!\vec v = 4\pi^2 \nu^2 r^2 + a^2 \qquad \frac{dz}{dt} = a$$

Now supposing that $|\vec v| = c$ and $\dfrac{dz}{dt}$ is $v_{\text{eff}}$, the effective velocity, then
$$c^2 = 4\pi^2 \nu^2 r^2 + v_{\text{eff}}^2$$
or
$$v_{\text{eff}} = \sqrt{c^2 - 4\pi^2 \nu^2 r^2}$$
whereby the effective velocity can be reduced arbitrarily with such a "trick." Now,
$$E^2 = p^2 c^2 + m^2 c^4$$
coupled with a quantum understanding of $E$ and $p$ also relates speed to frequencies & wavelengths.

---

## Page 74

$$\hbar^2 \omega^2 = \tfrac{4\pi^2}{\lambda^2}\,\hbar^2 c^2 + m^2 c^4 = \hbar^2 \nu^2 c^2 + m^2 c^4$$
$$\frac{\hbar^2 \omega^2}{m^2 c^2} = v^2 + c^2$$
$$v_{\text{eff}} = \sqrt{\frac{\hbar^2 \omega^2}{m^2 c^2} - c^2}$$

Here, the larger $\omega$ is, the larger $v$ is. Yet $v$ can apparently go to $\infty$ with this formulation. That isn't right!

$p \neq m v$, $\;p = m v = \dfrac{m_0 v}{\sqrt{1 - v^2/c^2}}$
$$\hbar^2 \omega^2 = \frac{m_0^2 v^2 c^2}{1 - v^2/c^2} + m_0^2 c^4$$
$$\hbar^2 \omega^2 (1 - v^2/c^2) = m_0^2 v^2 c^2 + m_0^2 c^4 (1 - v^2/c^2)$$
$$\hbar^2 \omega^2 (c^2 - v^2) = m_0^2 v^2 c^4 + m_0^2 c^4 (c^2 - v^2)$$
$$\hbar^2 \omega^2 c^2 - \hbar^2 \omega^2 v^2 = m_0^2 v^2 c^4 + m_0^2 c^6 - m_0^2 c^4 v^2$$
$$\hbar^2 \omega^2 c^2 - m_0^2 c^6 = (\hbar^2 \omega^2 + m_0^2 c^4 - m_0^2 c^4) v^2$$
$$v^2 = c^2 - \frac{m_0^2 c^4}{\hbar^2 \omega^2} = c^2 - \frac{E_0^2}{E^2}$$

**Way way — no good.**

---

## Page 75 — Reference: Ferbel (ASI)

*(Reference page — bibliographic data from a textbook the author was reading. Top header:)*

**NATO Advanced Science Institutes Series — Techniques & Concepts of High Energy Physics — Thomas Ferbel, Vol 7, Plenum Press NY**

Selected numerical values copied from the book:

$$m_W = 80.22 \pm 0.26\ \text{GeV (exp)} \quad \text{vs}\quad 80.213 \pm .12$$
$$80.10 \pm .27\ \text{theory w/ LEP}$$

$$m_W^2 = \frac{\pi\alpha}{\sqrt 2\, G_F\, \sin^2\theta_W} \qquad m_Z^2 = \frac{\pi\alpha}{\sqrt 2\, \bar\rho\, G_F\, \sin^2\theta_W \cos^2\theta_W}$$
$$\bar\rho = 1 + \frac{3\sqrt 2}{16\pi^2} G_F\, m_t^2 \qquad \sin^2\theta_W = \frac{e^2}{g^2} = 1 - \frac{m_W^2}{\bar\rho\, m_Z^2}$$

$$m_Z = 91.187 \pm .007\ \text{GeV (LEP)}$$
$$m_\tau = 1776.9^{+.4}_{-.5} \pm .2\ \text{MeV}$$
$$\tau_\tau = 296.8 \pm 3.2\ \text{fs lifetime, so}\quad \frac{G_F^\tau}{G_F^\mu} = 0.987 \pm .006\quad (2.2\sigma\text{ away from standard!})$$

$$1 - \left(\frac{m_W}{m_Z}\right)^2 = 0.2283 \pm 0.0026 \qquad \sin^2\theta_W = .232 \pm .009$$

$$\sigma_{\nu_\mu e} = \frac{2 G_F^2 m_e}{\pi}\, E_\nu \!\left[(g_{Ve} + g_{Ae})^2 + \tfrac13 (g_{Ve} - g_{Ae})^2\right]$$
$$\frac{\sigma_{\bar\nu_\mu e}}{\sigma_{\nu_\mu e}} = 3\,\frac{1 - 4\sin^2\theta_W + \tfrac{16}{3}\sin^4\theta_W}{1 - 4\sin^2\theta_W + 16\sin^4\theta_W}$$

$$g_{Ve} = -0.075 \pm 0.020,\quad g_{Ae} = -.503 \pm 0.017\quad \text{ref Z3p.125}$$

At LEP: $g_{V\ell} = -0.372 \pm .0029$, $\;g_{A\ell} = -.4999 \pm 0.0009$.
At LEP: $\sin^2\theta_W = .2319 \pm .0007 \;\Rightarrow\; m_t = 160^{+16+16}_{-17-20}\ \text{GeV}$.
Vol 9 has $m_t = 175 \pm 6$ w/ 172 for standard model.

---

## Page 76 — Majorana mass / Fermi 4-particle

**Majorana mass term** violates charge conservation, but not for neutrinos:
$$M_D \bar\psi_L \psi_R + \tfrac12 M_L \bar\psi_L (\psi_L)^c + \tfrac12 M_R \bar\psi_R (\psi_R)^c + \text{h.c.}$$

Written in matrix form:
$$\tfrac12 \bar\Psi\!\begin{pmatrix} M_L & M_D \\ M_D^+ & M_R\end{pmatrix}\!\Psi^c + \text{h.c.}$$

Margin: "*ln V10 p 265*"

|  | (book) |
|---|---|
| $m_{\nu_e} < 3.4\ \text{eV}$ | $15\ \text{eV}$ |
| $m_{\nu_\mu} < 160\ \text{keV}$ | $170\ \text{keV}$ |
| $m_{\nu_\tau} < 24\ \text{MeV}$ | $18.2\ \text{MeV}$ |

*Reference noted:* "The Physics of Massive Neutrinos — Francois Vannucci, LPNHE Univ Paris 7, 4 Place Jussieu Tour 33, 75252 Paris."

**Fermi 4-particle interaction** for $n \to p\, e^-\,\bar\nu_e$:
$$\mathcal L_F = -\frac{G_F}{\sqrt 2}\, \bar p\, \gamma_\lambda n\, \bar e\, \gamma^\lambda \nu_e$$
$$G_F = 1.167 \times 10^{-5}\ \text{GeV}^{-2}$$

Parity:
$$J_\mu \sim V_\mu - A_\mu$$
$$V^\mu = \bar\psi\gamma^\mu\psi \quad\xrightarrow{P}\quad +\bar\psi\gamma^\mu\psi \;\;/\;\; -\bar\psi\gamma_\mu\psi$$
$$A^\mu = \bar\psi\gamma^\mu\gamma^5\psi \quad\xrightarrow{P}\quad -\bar\psi\gamma^\mu\gamma^5\psi \;\;/\;\; \bar\psi\gamma_\mu\gamma^5\psi$$

Parity violation comes from $\mathcal L \sim J_\mu J^\mu$.
**V–A Theory** Feynman & Gell-Mann:
$$\mathcal L_{VA} = -\frac{G_F}{\sqrt 2}\, J_\mu^{\ell\ell}\, J^{\mu\ell\,+}$$
$$J_\mu^{\ell\ell} = \bar\nu_e \gamma_\mu (1 - \gamma_5) e + \bar\nu_\mu \gamma_\mu (1 - \gamma_5)\mu + \bar\nu_\tau \gamma_\mu (1 - \gamma_5)\tau$$

---

## Page 77 — Program for Weak Interaction Physics

We have shown the similarity between a massive free Dirac equation and a reduced weak interaction. The difference between this and what is observable is that the equivalent of a mass term in the weak interaction violates charge conservation, at least when charge is seen as a property of a particle.

However, a mass term in the free Dirac equation apparently violates spin conservation too. Yet with free Dirac we understand that there's a bigger concept — angular momentum conservation — which holds the conservation principle. When the mass term flips spin it creates angular momentum in the field, so that $S_{-1/2} \to S_{1/2}$ is compensated with $J_N \to J_{N+1}$. Perhaps charge should be understood in a better way too, such that it is partly due to intrinsic properties of a particle, and partly not. These intrinsic qualities, then, would become $W_\pm$ bosons in a more advanced theory.

With such an understanding, we might then turn around and understand mass as arising quite naturally from another field.

**Greiner Rel QM, p. 216, 217** — Shows $J$ commutes w/ $H$ w/ spherical potential:
$$J = L + S = L + \tfrac12 \hbar \vec\Sigma$$
$$[L, \vec\alpha\!\cdot\!\vec p] = i\hbar\, \vec\alpha \times \vec p \qquad (\vec L = \vec r \times \vec p)$$
$$\vec\Sigma = \begin{pmatrix}\vec\sigma & 0 \\ 0 & \vec\sigma\end{pmatrix}\qquad [S, \vec\alpha\!\cdot\!\vec p] = \tfrac12 \hbar [\vec\Sigma, \vec\alpha\!\cdot\!\vec p] = -i\hbar\, \vec\alpha \times \vec p \;=\; -\tfrac{i}{\hbar}(\vec r \times \nabla)$$

---

## Page 78 — Black-body Radiation

$$\bar n_\omega = \frac{1}{e^{\hbar\omega/kT} - 1}$$
$$dN_\omega = \frac{V}{\pi^2 c^3}\,\frac{\omega^2\, d\omega}{e^{\hbar\omega/kT} - 1}$$
$$E \sim \omega N$$

Visible spectrum (nm):
- Red: 620–750
- Green: 495–570
- Blue: 450–495

*(Rest of page blank.)*

---

## Page 79

How does a gauge theory with a massive WB reduce to a contact interaction as $m_{WB} \to \infty$? Can the contact interaction be modeled as a 2-point term instead of a 4-point term? Can we do this naively, with a simple mass term and ignore the Higgs?

Think of something like:

*(diagram: $\mu^- \to \nu_\mu$ at one vertex via $W^-$, which gives $\bar\nu_e + e^-$ at the other vertex. Standard 4-fermion vertex with $W^-$ propagator.)*

Taking $m_{W^-} \to \infty$ with a corresponding change in $G$ pulls the $W$ line in to zero length:

*(diagram: same as above, but $W^-$ propagator collapsed to a single 4-fermion point.)*

This is a 4-point interaction. Suppose, however, there was still a neutral current with a non-infinite mass WB, or a mass-like term between $\mu_L, \nu_{\mu L}$, etc. Then, we'd have interactions like this:

*(diagram: $\mu_L \to \nu_{\mu L}$ via a $\times$ ("mass") vertex; then $\nu_{\mu L} \to \bar\nu_{eL}$ via a $B_0$ exchange to an $e^- \to \nu_{eL}$ pair at the other end. A second $\times$ symbol on the lepton line on the right.)*

Instant-by-instant, charge is **not** conserved in this diagram. What would it be like for the electromagnetic current? $B_0$ seems like it would correspond to a spinless photon. Maybe we should let $W_\pm$ exist but not $Z$, similar to spin $\pm 1$ photons & no spin 0 photon?

---

## Page 80

Then a neutral current interaction must look like:

*(diagram top: $e_L^-, e_L^+$ scatter via $Z$ exchange to $\bar e_L, e_L^+$. The $Z$-line connects two crossed-vertex pairs.)*

$\Downarrow$

*(diagram middle: same external legs, but $Z$ replaced by two $\times$ ("mass") vertices joined by an internal $\bar\nu_e \to W_- \to \bar\nu_e$ chain, showing the neutral current as two contact interactions linked by a charged $W$ exchange.)*

plus 3 other possibilities. Much like:

*(diagram bottom: photon-band scattering — $e_L^+ \to \bar e_R^+ \to e_R^+$ via two crossed vertices, photon $\gamma_{s=+1}$ exchanged, then $e_L^- \to \bar e_R^- \to e_L^+$ on the other side.)*

This allows photon-based scattering in this mode, though there is no spin-0 photon. But here $W_\pm$ are just like two spin states of one field — not really separate fields. How can we formulate that mathematically and get the charge states to come out, just like spin states come out for a photon??

The analogy we're drawing clearly suggests that the exchange particles are neutral in the first analysis, if the symmetry is to hold. And if the $B$ should have mass then $A$ has a certain interaction with the $W_\pm$ reduced to "weak mass."

We obviously lose charge conservation with a weak mass — naively speaking, and yet somehow Dirac conserves $L$ despite a mass term. How??

---

## Page 81

Somehow there is an interchange between $L$ and $S$ so that $J = L + S$ is conserved although $L$ is not and $J$ is not. One might even say that $S$ was invented to save $L$ conservation. Thus, for example,
$$\overline{e_L} \xrightarrow{\,\times\, m\,} e_R$$
happens and it doesn't bother anyone. We need to understand the details of how that happens. Then maybe we can do a similar thing with charge.

Let us start by examining electron states in both Dirac and **Weyl** representations. For this we first need a matrix transform between the two. Then we'll look at steady state & pure spin components of an electron field travelling along the $z$ axis.

**Dirac standard rep:** (diagonalizes mass term)
$$\alpha_i = \sigma_1 \otimes \sigma_i \qquad \beta = \sigma_3 \otimes I$$

**Weyl rep:** (diagonalizes $\beta$)
$$\alpha_i = -\sigma_3 \otimes \sigma_i \qquad \beta = -\sigma_1 \otimes I$$

We want a unitary map $U$ to go between these, specifically $\sigma_1 \to -\sigma_3, \;\sigma_3 \to -\sigma_1$. This is a rotation about the $y$-axis of $90°$ and then a reflection in the $y$-$z$ plane. First rotate about the $y$-axis to get $\sigma_1 \to \sigma_3, \sigma_3 \to -\sigma_1$ with
$$U_y = \frac{1}{2}\!\begin{pmatrix} 1+i & 1+i \\ -1-i & 1+i\end{pmatrix}$$
and then rotate $180°$ using $U_0 = \sigma_1 = \begin{pmatrix}0 & 1\\ 1& 0\end{pmatrix}$, namely $\sigma_3 \to -\sigma_3,\;\sigma_1 \to \sigma_1$. So
$$U_{DW} = U_0\, U_y = \frac{1}{2}\!\begin{pmatrix} 0 & 1\\ 1 & 0\end{pmatrix}\!\begin{pmatrix} 1+i & 1-i \\ -1-i & 1+i\end{pmatrix} = \frac12\!\begin{pmatrix} -1-i & 1+i \\ 1+i & 1-i\end{pmatrix}$$

---

## Page 82

In the standard representation, there are plane wave solutions of the form (positive energy)
$$\psi_+^{(\alpha)}(x) = e^{-i(k_0 x_0 - \vec k\!\cdot\!\vec x)}\, u^\alpha(k)$$
$$u^\alpha(k) = \frac{\gamma^\mu k_\mu + m I}{\sqrt{2m(m+E)}}\, u^\alpha(0)$$
$$u^1(0) = \begin{pmatrix} 1\\0\\0\\0 \end{pmatrix}\quad u^2(0) = \begin{pmatrix} 0\\1\\0\\0 \end{pmatrix}$$

and (negative energy)
$$\psi_-^{(\alpha)}(x) = e^{+i(k_0 x_0 + \vec k\!\cdot\!\vec x)}\, v^{(\alpha)}(k)$$
$$v^\alpha(k) = \frac{-\gamma^\mu k_\mu + m I}{\sqrt{2m(m+E)}}\, v^\alpha(0)$$
$$v^1(0) = \begin{pmatrix} 0\\0\\1\\0 \end{pmatrix}\quad v^2(0) = \begin{pmatrix} 0\\0\\0\\1 \end{pmatrix}$$

We want to transform these solutions to the Weyl rep. so we can better see the dynamic interdependence of spin states and angular momentum. Applying $U_{DW}$ to $\psi$ just re-casts the $\gamma$ matrices into Weyl form and acts straight on the basis vectors $u^\alpha(0)$ etc. Thus
$$U_{DW}\, u^1(0) = \tfrac12\!\begin{pmatrix} -1-i & 1+i \\ 1+i & 1-i\end{pmatrix}\!\begin{pmatrix} 1\\0\\0\\0\end{pmatrix} = \tfrac12\!\begin{pmatrix} -1-i \\ 0\\ 1+i\\ 0\end{pmatrix}$$
$$U_{DW}\, u^2(0) = \tfrac12\!\begin{pmatrix} 0\\ -1-i\\ 0\\ 1-i\end{pmatrix} \qquad U_{DW}\, v^1(0) = \tfrac12\!\begin{pmatrix} 0\\ 1+i\\ 0\\ 1-i\end{pmatrix} \qquad U_{DW}\, v^2(0) = \tfrac12\!\begin{pmatrix} 1+i\\ 0\\ 1-i\\ 0\end{pmatrix}$$

The $\gamma$ matrices are given by $\gamma^0 = \beta,\;\gamma^i = \beta \alpha_i$.

---

## Page 83

whereby in Weyl representation,
$$\alpha_i = -\sigma_3 \otimes \sigma_i \qquad \beta = -\sigma_1 \otimes I$$
so
$$\gamma_i = \beta \alpha_i = (\sigma_1 \otimes I)(\sigma_3 \otimes \sigma_i) = (\sigma_1 \sigma_3 \otimes \sigma_i) = \begin{pmatrix} 0 & 1\\ 1 & 0\end{pmatrix}\!\begin{pmatrix} 1 & 0\\ 0 & -1\end{pmatrix}\!\otimes\sigma_i = \begin{pmatrix} 0 & -1\\ 1 & 0\end{pmatrix}\!\otimes\sigma_i = -i\sigma_2 \otimes \sigma_i$$

Plane wave solution for the upper:
$$u^\alpha(k) = \frac{1}{\sqrt{2m(m+E)}}\,(\gamma^\mu k_\mu + m I)$$
$$= \frac{1}{\sqrt{2m(m+E)}}\,(\gamma^0 k_0 - \gamma^i k_i + m I)$$

and if only $k_0,\,k_3 = k_z \neq 0$, then
$$u^\alpha(k) = \frac{1}{\sqrt{2m(m+E)}}\!\left[ -\!\begin{pmatrix} 0 & 0 & k_0 & 0\\ 0 & 0 & 0 & k_0\\ k_0 & 0 & 0 & 0\\ 0 & k_0 & 0 & 0\end{pmatrix} + i\!\begin{pmatrix} 0 & 0 & -ik_3 & 0\\ 0 & 0 & 0 & ik_3\\ ik_3 & 0 & 0 & 0\\ 0 & -ik_3 & 0 & 0\end{pmatrix} + \begin{pmatrix} m & 0 & 0 & 0\\ 0 & m & 0 & 0\\ 0 & 0 & m & 0\\ 0 & 0 & 0 & m\end{pmatrix}\right]\!u^\alpha(0)$$

So
$$u_z^{(2)}(k) = \frac{1}{2\sqrt{2m(m+E)}}\,\left[\!\begin{pmatrix} 0\\ 0\\ -k_0(1+i)\\ 0\end{pmatrix} + \begin{pmatrix} 0\\ 0\\ k_3(1+i)\\ 0\end{pmatrix} + \begin{pmatrix} (-1-i)m \\ 0\\ 0\\ (1+i)m\end{pmatrix}\right]$$

$$\boxed{\;\psi_z^{(2)+} = \frac{1}{2\sqrt{2m(m+E)}}\,\begin{pmatrix}(1+i)(k_3 - k_0 - m)\\ 0\\ (1+i)(k_3 + k_0 + m)\\ 0\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;}$$

---

## Page 84

$$\psi_z^{(2)+} = \frac{1}{2\sqrt{2m(m+E)}}\!\left[-\!\begin{pmatrix} 0 & 0 & k_3 & 0\\ 0 & 0 & 0 & k_0\\ k_0 & 0 & 0 & 0\\ 0 & k_3 & 0 & 0\end{pmatrix}\!\begin{pmatrix} 0\\ -1-i\\ 0\\ 1+i\end{pmatrix} + \begin{pmatrix} 0 & 0 & k_3 & 0\\ 0 & 0 & 0 & -k_3\\ -k_3 & 0 & 0 & 0\\ 0 & k_3 & 0 & 0\end{pmatrix}\!\begin{pmatrix} 0\\ -1-i\\ 0\\ 1+i\end{pmatrix} + \begin{pmatrix} 0\\ -1-i\\ 0\\ 1+i\end{pmatrix}m\,\right]\,e^{-i(k_0 t - k_3 z)}$$

$$\boxed{\;\psi_z^{(2)+} = \frac{1+i}{2\sqrt{2m(m+E)}}\,\begin{pmatrix}0\\ -k_0 - k_3 - m\\ 0\\ +k_0 - k_3 + m\end{pmatrix}\,e^{-i(k_0 t - k_3 z)}\;}$$

$$\psi_z^{(1)-} = \frac{1}{2\sqrt{2m(m+E)}}\!\left[\!\begin{pmatrix} 0 & 0 & k_0 & 0\\ 0 & 0 & 0 & k_0\\ k_0 & 0 & 0 & 0\\ 0 & k_0 & 0 & 0\end{pmatrix} + \begin{pmatrix} 0 & 0 & -k_3 & 0\\ 0 & 0 & 0 & k_3\\ k_3 & 0 & 0 & 0\\ 0 & -k_3 & 0 & 0\end{pmatrix} + m\right]\!\begin{pmatrix} 1+i\\ 0\\ 1-i\\ 0\end{pmatrix} e^{i(k_0 t + k_3 z)}$$

$$\boxed{\;\psi_z^{(1)-} = \frac{1}{2\sqrt{2m(m+E)}}\!\begin{pmatrix} (1-i)(k_0 - k_3) + (1+i)m\\ 0\\ (1+i)(k_0 + k_3) + (1-i)m\\ 0\end{pmatrix}\,e^{i(k_0 t + k_3 z)}\;}$$

$$\psi_z^{(2)-} = \frac{1}{2\sqrt{2m(m+E)}}\!\left[\!\begin{pmatrix} m & 0 & k_0 - k_3 & 0\\ 0 & m & 0 & k_3 + k_0\\ k_0 + k_3 & 0 & m & 0\\ 0 & k_0 - k_3 & 0 & m\end{pmatrix}\!\begin{pmatrix} 0\\ 1+i\\ 0\\ 1-i\end{pmatrix}\right]\,e^{i(k_0 t + k_3 z)}$$

$$\boxed{\;\psi_z^{2-} = \frac{1}{2\sqrt{2m(m+E)}}\!\begin{pmatrix} 0\\ (1-i)(k_0 + k_3) + (1+i)m\\ 0\\ (1+i)(k_0 - k_3) + (1-i)m\end{pmatrix}\,e^{i(k_0 t + k_3 z)}\;}$$

In the $m \to 0$ limit,
$$\psi_z^{(2)+} \sim \frac{1}{\sqrt{8 k_3}}\,(1-i)\,2 k_3 \begin{pmatrix} 0\\ 0\\ 0\\ 1\end{pmatrix}\, e^{i k_3(t+z)}$$
$$\psi_z^{2-} \sim \frac{1}{\sqrt{2 k_3}}(1+i) k_3 \begin{pmatrix} 0\\ 1\\ 0\\ 0\end{pmatrix} e^{i k_3 (t+z)}$$
$$\psi_z^{(1)-} \sim \frac{-(1+i)}{\sqrt{2 k_3}}\!\begin{pmatrix} 0\\ k_3\\ 0\\ 0\end{pmatrix} e^{i k_3(t+z)}$$

Note that there seems to be a degeneracy here, in that we don't get any $\begin{pmatrix} 1\\0\\0\\0\end{pmatrix}$ or $\begin{pmatrix} 0\\0\\1\\0\end{pmatrix}$ states as the limit of $m \to 0$. Why not? Are we going to a negative energy state in which $k_0 = -k_3$?

---

## Page 85

Let's try another way to solve these. Write Weyl out like this:
$$i\hbar\,\frac{\partial \psi_+}{\partial t} = -i\hbar c\,\vec\sigma\!\cdot\!\nabla\psi_+ - m_0 c^2 \psi_- \tag{4a}$$
$$i\hbar\,\frac{\partial \psi_-}{\partial t} = i\hbar c\,\vec\sigma\!\cdot\!\nabla\psi_- - m_0 c^2 \psi_+ \tag{4b}$$
where $\psi_+$ and $\psi_-$ are both 2-component spinors. To factor out space–time dependences, we have to write
$$\psi_+ \sim A_+ e^{i(k_0 c t - \vec k\!\cdot\!\vec x)} \;(1) \qquad\text{or}\qquad \psi_+ \sim B_+ e^{i(k_0 c t + \vec k\!\cdot\!\vec x)}\;(2)$$
and take the derivatives. Let's start with (1).
$$i\hbar\,\tfrac{\partial}{\partial t}\!\big(A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}\big) = -\hbar c k_0 A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}$$
$$i\hbar c\,\vec\sigma\!\cdot\!\nabla\!\big(A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}\big) = i\hbar c\, \vec\sigma\!\cdot\!\big(A_\pm (-i\vec k) e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}\big) = \hbar c\, (\vec\sigma\!\cdot\!\vec k) A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)} \tag{3a/3b}$$

whereby (4a/b) becomes
$$-\hbar c k_0 A_+ = -\hbar c\,(\vec\sigma\!\cdot\!\vec k) A_+ - m_0 c^2 A_- \tag{3a}$$
$$-\hbar c k_0 A_- = \hbar c\,(\vec\sigma\!\cdot\!\vec k) A_- - m_0 c^2 A_+ \tag{3b}$$

Now, we want solutions such that as $m_0 \to 0$, only one component of the four is non-zero. Is this possible? In the massless case, 3a & 3b are completely independent, so $A_+$ or $A_-$ can be non-zero without affecting the other. We treat $m_0$ as an interaction & a perturbation. Now, 3a takes the form
$$k_0 I A_+ = (\vec\sigma\!\cdot\!\vec k) A_+$$
If $\vec k = k_3 \hat z$ then
$$\begin{pmatrix} k_0 & 0\\ 0 & k_0\end{pmatrix} A_+ = \begin{pmatrix} k_3 & 0\\ 0 & -k_3\end{pmatrix} A_+$$
If $A_+^{(1)} = \binom{1}{0}$ then $k_0 = k_3$ and if $A_+^{(2)} = \binom{0}{1}$ then $k_0 = -k_3$. Simply put, $A_+^{(1)}$ is the positive energy solution and $A_+^{(2)}$ is the negative ⟶

---

## Page 86

⟶ energy solution. Doing the same with $A_-$, we get
$$\begin{pmatrix} k_0 & 0\\ 0 & k_0\end{pmatrix} A_- = \begin{pmatrix} -k_3 & 0\\ 0 & k_3\end{pmatrix} A_-$$
so $A_-^{(1)} = \binom{1}{0}$ is the negative energy solution and $A_-^{(2)} = \binom{0}{1}$ is the positive energy solution. This also encompasses the $B$-solutions (2) above. The standard normalization of these solutions is $\dfrac{1}{(2\pi)^3 \sqrt{2E}}$. (Greiner 14.5)

The upper component of $A^+$ is understood as a right handed (spin in the direction of motion) particle. The lower component is understood as a left handed antiparticle. This is clear because $\vec\sigma\!\cdot\!\vec p$ is pure helicity for a massless particle & these are its eigenstates. In the same way, the upper component of $A^-$ is a right-handed antiparticle and the lower component is a left-handed particle. *(margin: "helicity, really, for a plane wave")*

Now, the mass term **conserves spin**. It mixes a right-handed particle with a right-handed antiparticle and a left-handed antiparticle with a left-handed particle.

To derive solutions that reduce to the above in the massless case, write $A_+^{(1)} = \binom{1}{\alpha}$, $A_-^{(1+)} = \binom{\beta}{\gamma}$ and plug these into the equations (3):
$$-\hbar c k_0 \binom{1}{\alpha} = -\hbar c \sigma_3 k_3 \binom{1}{\alpha} - m_0 c^2 \binom{\beta}{\gamma}$$
$$-\hbar c k_0 \binom{\beta}{\gamma} = \hbar c \sigma_3 k_3 \binom{\beta}{\gamma} - m_0 c^2 \binom{1}{\alpha}$$

This gives us 4 equations,
$$\delta k_0 = \delta k_3 + \frac{m_0 c}{\hbar}\,\beta \tag{4a}$$
$$k_0 \alpha = -k_3 \alpha + \frac{m_0 c}{\hbar}\,\gamma \tag{4b}$$

---

## Page 87

$$-k_0 \beta = k_3 \beta - \frac{m_0 c}{\hbar} \tag{4c}$$
$$-k_0 \gamma = -k_3 \gamma - \frac{m_0 c}{\hbar}\,\alpha \tag{4d}$$

4b and 4d are completely independent of 4a & 4c so solve 4a & 4c. Writing $\lambda_0 = \dfrac{m_0 c}{\hbar}$ and $\delta = 1$,
$$k_0 = k_3 + \lambda_0 \beta \tag{4a}$$
$$k_0 \beta = -k_3 \beta + \lambda_0 \;\Rightarrow\; \beta = \frac{\lambda_0}{k_0 + k_3} \tag{4c}$$

Substituting into 4a,
$$k_3 - k_0 = -\frac{\lambda_0^2}{k_0 + k_3}$$
$$k_3^2 - k_0^2 = -\lambda_0^2 = -\frac{m_0^2 c^2}{\hbar^2}$$
$$p_z^2 - E_z^2 = -m_0^2 c^2 \quad\text{(off by a sign, but pretty close)}$$

To normalize, we'd like to write $A_+^{(1)} = \binom{a}{0}$, $A_-^{(1+)} = \binom{b}{0}$ where $a^2 + b^2 = 1$.
$$\eta \equiv 1 + \frac{\lambda_0^2}{(k_0 + k_3)^2} \qquad a = \frac{1}{\eta^{1/2}}\qquad b = \frac{\beta}{\eta^{1/2}}$$
$$1/\eta = \frac{(k_0 + k_3)^2}{(k_0 + k_3)^2 + \lambda_0^2}\qquad 1/\eta^{1/2} = \frac{k_0 + k_3}{\sqrt{(k_0 + k_3)^2 + \lambda_0^2}}$$
$$\beta/\eta = \frac{\lambda_0 (k_0 + k_3)}{(k_0 + k_3)^2 + \lambda_0^2}\qquad \beta/\eta^{1/2} = \frac{\lambda_0}{\sqrt{(k_0 + k_3)^2 + \lambda_0^2}}$$

and
$$\boxed{\;\Psi_{RP} = \binom{\psi_+}{\psi_-} = \frac{1}{(2\pi)^3 \sqrt{2E}}\!\begin{pmatrix} k_0 + k_3\\ 0\\ \lambda_0\\ 0\end{pmatrix} \big((k_0 + k_3)^2 + \lambda_0^2\big)^{-1/2}\, e^{i(k_0 t - k_3 z)}\;} \tag{6A}$$
**Right-handed particle:** $k_0 > 0$, $\lambda_0 = \dfrac{m_0 c}{\hbar}$.

As $\lambda_0 \to 0$ this reduces to the proper values for a pure right particle.

If we set $\beta = 1$ then
$$\delta k_0 = \delta k_3 + \lambda_0 \;\Rightarrow\; \delta = \frac{\lambda_0}{k_0 - k_3} \tag{5a}$$
$$-k_0 = k_3 - \lambda_0 \delta \;\Rightarrow\; \delta = \frac{k_0}{\lambda_0}\!\cdot\!\frac{1}{k_0 + k_3} \tag{5b}$$
$$k_0 + k_3 = \lambda_0^2 / (k_0 - k_3)$$

---

## Page 88

$$\boxed{\;\Psi_{LA} = \frac{1}{(2\pi)^3 \sqrt{2E}}\big((k_0 - k_3)^2 + \lambda_0^2\big)^{-1/2}\!\begin{pmatrix} \lambda_0\\ 0\\ k_0 - k_3\\ 0\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;} \tag{6B}$$
**The Left-Handed Antiparticle**, ($k_0 < 0$)!

Using 4b & 4d with $\alpha = 1$, we get
$$k_0 = -k_3 + \lambda_0 \gamma$$
$$k_0 \gamma = k_3 \gamma + \lambda_0 \;\Rightarrow\; \gamma = \frac{\lambda_0}{k_0 - k_3}$$
$$1/\eta^{1/2} = \frac{(k_0 - k_3)}{\sqrt{(k_0 - k_3)^2 + \lambda_0^2}}$$

$$\boxed{\;\Psi_{RA} = \frac{1}{(2\pi)^3 \sqrt{2E}}\,\big((k_0 - k_3)^2 + \lambda_0^2\big)^{-1/2}\!\begin{pmatrix} 0\\ k_0 - k_3\\ 0\\ \lambda_0\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;} \tag{6C}$$
**The Right-handed Antiparticle**, ($k_0 < 0$)!

Finally, setting $\gamma = 1$,
$$k_0 \alpha = -k_3 \alpha + \lambda_0 \;\Rightarrow\; \alpha = \frac{\lambda_0}{k_0 + k_3}$$
$$k_0 = k_3 + \lambda_0 \alpha$$

$$\boxed{\;\Psi_{LP} = \frac{1}{(2\pi)^3 \sqrt{2E}}\,\big((k_0 + k_3)^2 + \lambda_0^2\big)^{-1/2}\!\begin{pmatrix} 0\\ \lambda_0\\ 0\\ k_0 + k_3\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;} \tag{6D}$$
**The Left-Handed Particle** ($k_0 > 0$).

---

## Page 89

Now, note that the mass term mixes particle–antiparticle for either handedness, but does **not** mix handedness — i.e. it conserves helicity/spin. The introduction of the photon gets the spin though, and the photon carries spin $\pm 1$ in itself. (Never spin 0.) If we think of the photon as 2 separate particles, one w/ spin $+1$ and one w/ spin $-1$ then it is somewhat like the $W_\pm$ bosons. They carry charge instead of spin though, and flip spin states instead of charge states, whereas the $W$ flips charge states but not spin states … thus its "handedness."

In Weyl, $\gamma_5 = i\gamma_0 \gamma_1 \gamma_2 \gamma_3 = \begin{pmatrix} I & 0\\ 0 & -I\end{pmatrix}$ and the weak interaction couples via $1 - \gamma_5$ — that is, to the left-handed particle and right-handed antiparticle. This we take to be analogous to E–M coupling to $e$ and not $\nu_e$. Take the analogy 1 step further: If $e$ has "mass", or a mixing between $e_L^+ \leftrightarrow e_R^+$, $e_L^- \leftrightarrow e_R^-$ as a result of $A_\mu$, couldn't there be something like a "mass" as a result of $W$? Could the $Z$ be the result of that?

We should be able to draw the analogy clearly. The E&M ⟶ (margin) ⟶ interactions here are the "new idea." They don't conserve charge any more than the mass term in e&m. The mass term conserves magnetic moment.

*(Table sketched in the left margin — electromagnetic block:)*

| mass | particle | charge | spin | comment |
|---|---|---|---|---|
| m | $e_R^-$ | $-q$ | $+1$ | $A$ is to $S$ what $W$ is to $Q$ |
| m | $e_L^+$ | $+q$ | $-1$ | $A$ is to $Q$ what $W$ is to $S$ |
| m | $e_R^+$ | $+q$ | $-1$ | $\mu$ violates $q$ |
| m | $e_L^-$ | $-q$ | $+1$ | $n$ violates $q_3, g$ |
| 0 | $\nu_R$ | 0 | $+1$ | So if $A$ couple to $Q$, $W$ couples to $S$.  |
| 0 | $\bar\nu_L$ | 0 | $-1$ | Since 2-component spinor flips, not a scalar like $g$ |
| 0 | $\bar\nu_R$ | 0 | $-1$ | Could $W$ be a scalar field?  |
| 0 | $\nu_L$ | 0 | $+1$ | |

Bottom: separate **Weak** block — same particles, but now charges $\pm g$ and the curly braces label $P_C$ violation pairs. $\mu$ acts like $W$? Author labels the chains $)P_{C_Z}$ and $)P_{C_W}, P_{C_V}$.

---

## Page 90

*(Top of page — three Feynman diagrams of the weak/EM vertices:)*

- $\nu_L \to \bar\nu_R \to e_L^-,\;\bar\nu_e \to e_L^+$ via a $Z$ exchange (neutral current).
- $\bar\nu_R \to e_L^-$ and $\nu_L \to e_L^-$ via a $W^-$ exchange (charged current).
- $\bar\nu_{eR} \to e_L^-,\; \nu_{eR} \to e_L^-$ via $W^-$ (another configuration).

**Could $Z$ be viewed as a bound state of $W^+ W^-$?**

*(box diagram: $\nu_e$ and $e^-$ on one side, $\nu_e$ and $e^-$ on the other; two $W^+$ exchanges plus two intermediate $\nu_e$ propagators forming a closed box.)*

"One would certainly think so. Energies just don't work out."

---

### **Electromagnetic** *(tabulation continued)*

| $m$ | $\binom{e_R^-}{e_L^+}$ | $-q$ | $+1$ | |
| $m$ | $\binom{e_R^+}{e_L^-}$ | $+g$ | $-1$ | $A$ is to $S$ what $W$ is to $Q$ |
| $m$ |  | $-g$ | $+1$ | $A$ is to $Q$ what $W$ is to $S$ |
| $m$ |  | $+g$ | $-1$ | $\mu$ violates $q$ |
| $m$ |  | $-g$ | $+1$ | $n$ violates $q_3, g$ |
| 0 | $\nu_R$ | 0 | $+1$ | So if $A$ couples to $Q$, $W$ couples to $S$. |
| 0 | $\bar\nu_L$ | 0 | $-1$ | Since 2-component spinor flips, not a scalar like $g$. |
| 0 | $\bar\nu_R$ | 0 | $-1$ | Could $W$ be a scalar field?  |
| 0 | $\nu_L$ | 0 | $+1$ | |

### **Weak** *(separate block)*

|  | particle | $Q$ | spin |  |
|---|---|---|---|---|
| 0 | $e_R^-$ | 0 | $+1$ | |
| 0 | $e_L^+$ |  | $-1$ | |
| $\mu$ | $e_R^+$ | $+g$ | $-1$ | $\big\}P_{C_Z}\;\mu$ violates $q, g, \beta$ |
| $\mu$ | $e_L^-$ | $-g$ | $+1$ |  |
| 0 | $\nu_R$ | 0 | $+1$ | $\big\}P_{C_W}$  $\mu$ ↔ $W$ the same?  |
| 0 | $\bar\nu_L$ | 0 | $-1$ |  |
| $\bar\mu$ | $\bar\nu_R$ | $+g$ | $-1$ | $\big\}P_{C_V}$ |
| $\mu$ | $\nu_L$ | $-g$ | $+1$ |  |

*(margin: "$\mu \alpha W$ the same?")*

---

## End of batch — pages 61–90 transcribed.

The notebook continues past page 90. Open issues flagged by the author that have not yet been resolved in subsequent pages:

- The "anomalous" $m_Z^2\, W_{0\mu} W_{3\mu}$ cross-term that survives mass-mixing on page 66.
- The factor-of-2 mismatch in combined kinetic terms on page 70 (motivates the move to a quadruplet $(e_L, e_R, \nu_L, \nu_R)$ rather than two doublets).
- The $p_z^2 - E_z^2 = -m_0^2 c^2$ sign discrepancy on page 87 ("off by a sign, but pretty close").
- The "massless-limit degeneracy" on page 84 — only two of the four basis spinors emerge cleanly as $m \to 0$; the question of whether the missing two are absorbed into negative-energy states is left open and is what motivates the alternative derivation on pages 85–88.
- The speculation on page 90 that $Z$ might be a $W^+W^-$ bound state, immediately rejected on energetic grounds.
