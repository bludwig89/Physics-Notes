# Physics Notes — Pages 16–30

*Continuation of "Sachs Made Easy" — matter-field Lagrangians, Hamiltonian formulation, and curved-spacetime derivations.*

---

## Page 16

where $\mathcal{L}_M$ is the matter-field.

Now $\mathcal{L}_M$ will have an overall $(-g)^{1/2}$ for the invariant volume element $(-g)^{1/2} d^4x$.

At the next fundamental level, suppose we have only matter fields that are massless and 2-spinors, $\eta$ and $\chi$, where $\tilde{q}^{\mu}\partial_{\mu}\eta = 0$, $\tilde{\sigma}^{\mu}\partial_{\mu}\chi = 0$. Their free Lagrangians then take the form

$$\mathcal{L}_\eta = i\,\eta^{+}q^{\mu}\partial_{\mu}\eta \;-\; i\,\partial_{\mu}\eta^{+}q^{\mu}\eta \qquad \left(q^{\mu+} = q^{\mu}\;\text{etc.}\right)$$

$$\mathcal{L}_\chi = i\,\chi^{+}\tilde{q}^{\mu}\partial_{\mu}\chi \;-\; i\,\partial_{\mu}\chi^{+}\tilde{q}^{\mu}\chi$$

The interaction is added in the canonical fashion, s.t.

$$\boxed{\;\mathcal{L}_M^{\eta} = (-g)^{1/2}\!\left\{ i\,\eta^{+}q^{\mu}\eta_{;\mu} \;-\; i\,\eta_{;\mu}^{+}q^{\mu}\eta \right\}\;}$$

---

$$q_{\mu}\tilde{q}^{\mu} = -4\,\sigma^{0}_{0}$$

$$
\begin{aligned}
q^{\mu} &= q^{\mu}_{i}\,\sigma^{i} \\
        &= q^{\mu}_{4}\sigma_{0} - i\sigma_{1}q^{\mu}_{1} - i\sigma_{2}q^{\mu}_{2} - i\sigma_{3}q^{\mu}_{3} \\[4pt]
\tilde{q}^{\mu} &= -\sigma_{0}q^{\mu}_{4} - i\sigma_{1}q^{\mu}_{1} - i\sigma_{2}q^{\mu}_{2} - i\sigma_{3}q^{\mu}_{3}
\end{aligned}
$$

Sachs writes

$$\tag{3.60} q^{\mu}(x) = \sigma_{\nu}\!\left(\nu\sigma^{\mu}(x)\right) = \begin{pmatrix} 0v^{\mu}-{}_{3}v^{\mu} & -{}_{1}v^{\mu}+i_{2}v^{\mu} \\ -{}_{1}v^{\mu}-i_{2}v^{\mu} & {}_{0}v^{\mu}+{}_{3}v^{\mu} \end{pmatrix}$$

$$\tag{3.62} \tilde{q}^{\mu}(x) = \begin{pmatrix} -{}_{0}v^{\mu}-{}_{3}v^{\mu} & -{}_{1}v^{\mu}+i_{2}v^{\mu} \\ -{}_{1}v^{\mu}-i_{2}v^{\mu} & -{}_{0}v^{\mu}+{}_{3}v^{\mu} \end{pmatrix}$$

---

## Page 17

where

$$\eta_{;\mu} = \partial_{\mu}\eta + \Omega_{\mu}\,\eta$$

Can we simplify this and equate $\chi$ with $\eta^{+}$?

$$\chi = \varepsilon\,\eta^{*}, \qquad \varepsilon = \text{(antisymmetric)}$$

These are time-reflected fields. Space-reflected fields might be better, as

$$\sigma^{\mu}\partial_{\mu}\varphi + i\,m\,\zeta = 0$$
$$-\tilde{\sigma}^{\mu}\partial_{\mu}\zeta + i\,m\,\varphi = 0$$

since weak interactions have to do w/ Left–Right handedness — but I guess this falls out either way, so use $\eta$ and $\chi$.

$$\boxed{\begin{aligned}
\eta_{;\mu} &= \partial_{\mu}\eta + \Omega_{\mu}\,\eta \\
\chi_{;\mu} &= \partial_{\mu}\chi + \Omega^{(\chi)}_{\mu}\chi
\end{aligned}}$$

$$\boxed{\Omega^{(x)}_{\rho} = -\tfrac{1}{4}\,\tilde{q}_{\mu}\!\left(\partial_{\rho}q^{\mu} + \Gamma^{\mu}_{\tau\rho}\,q^{\tau}\right)} \tag{3.77}$$

$$= \tfrac{1}{4}\,q_{\mu}\!\left(\partial_{\rho}\tilde{q}^{\mu} + \Gamma^{\mu}_{\tau\rho}\,\tilde{q}^{\tau}\right) \tag{3.79b}$$

Do we need the hermitian conjugates? Why? I don't think so. These should be equivalent to a single Dirac Bispinor. Then, in concise notation,

$$\boxed{\;\mathcal{L} = (-g)^{1/2}\!\left\{\,R + i\,\eta^{+}q^{\mu}\eta_{;\mu} + i\,\chi^{+}\tilde{q}^{\mu}\chi_{;\mu}\,\right\}\;}$$

as the total Lagrangian.

---

## Page 18

Now, an important question is, where do *complex constants* come in, if they do? (at a fundamental level)

This must also be cleaned up for a Hamiltonian formulation in order to generate a multi-particle quantum formulation.

$$T_{00} = \mathcal{H} = \frac{\partial\mathcal{L}}{\partial\dot{\varphi}}\,\dot{\varphi} - \mathcal{L} \;\equiv\; \pi\,\dot{\varphi} - \mathcal{L}$$

If $\;G_{\mu\nu} = 8\pi\,T_{\mu\nu}$, then $\;T_{00} = \mathcal{H} = \dfrac{1}{8\pi}\,G_{00}$ for the gravitational field itself.

$$G_{\mu\nu} = R_{\mu\nu} - \tfrac{1}{2}g_{\mu\nu}R$$

$$\boxed{\;\frac{\partial\mathcal{L}}{\partial\dot{\varphi}_{\text{E}}} = \tfrac{1}{8\pi}G_{00} = \tfrac{1}{8\pi}\!\left(R_{00} - \tfrac{1}{2}g_{00}R\right)\;}$$

$$\boxed{\begin{aligned}
R_{00} &= R^{\lambda}_{\,00\lambda} = \partial_{\lambda}\Gamma^{\lambda}_{00} - \cdots \\
       &= R^{\lambda}_{\,0\lambda 0} = \partial_{\lambda}\Gamma^{\lambda}_{00} - \partial_{0}\Gamma^{\lambda}_{0\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{00} - \Gamma^{\alpha}_{\beta 0}\Gamma^{\beta}_{0\alpha}
\end{aligned}}$$

$\mathcal{H}$, however, should *not* be expressed merely in terms of $q^{\mu\nu}$, but in terms of independent $g$ and $\Gamma$.

For a field $\varphi$,

$$\pi_{\varphi} = \frac{\partial \mathcal{L}}{\partial(\partial_{0}\varphi)}$$

---

## Page 19

For non-spinor Gen. Rel.,

$$\mathcal{H}_{E} = \tfrac{1}{8\pi}\!\left(R_{00} - \tfrac{1}{2}g_{00}R\right) \qquad \text{(ok)}$$

$$= \tfrac{1}{8\pi}\!\left\{\partial_{\lambda}\Gamma^{\lambda}_{00} - \partial_{0}\Gamma^{\lambda}_{0\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{00} - \Gamma^{\alpha}_{\beta 0}\Gamma^{\beta}_{0\alpha}\right.$$
$$\left.\quad -\;\tfrac{1}{2}g_{00}\!\left[g^{\mu\nu}\!\left(\partial_{\lambda}\Gamma^{\lambda}_{\mu\nu} - \partial_{\mu}\Gamma^{\lambda}_{\nu\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{\mu\nu} - \Gamma^{\alpha}_{\beta\nu}\Gamma^{\beta}_{\mu\alpha}\right)\right]\right\}$$

To keep this 1st order in derivatives, we must treat $\Gamma^{\lambda}_{\mu\nu}$ and $g^{\mu\nu}$ as independent variables and let the formulation derive the relation between them.

For Spinor Gen. Rel.,

$$\mathcal{H}_{E} = \tfrac{1}{8\pi}\!\left(R_{00} - \tfrac{1}{2}g_{00}R\right) \qquad \text{(ok)}$$

$$= \tfrac{1}{8\pi}\!\left\{\tfrac{1}{4}\mathrm{Tr}\!\left(K_{0\lambda}q^{\lambda}\tilde{q}_{0} - q_{0}\tilde{q}^{\lambda}K_{0\lambda} + q^{\lambda}K^{+}_{0\lambda}\tilde{q}_{0} - q_{0}K^{+}_{0\lambda}\tilde{q}^{\lambda}\right)\right.$$
$$\left.\quad + \tfrac{1}{2}g^{0}_{\,0}\tilde{q}^{0}\cdot \tfrac{1}{4}\mathrm{Tr}\!\left(K_{\nu\mu}q^{\mu}\tilde{q}^{\nu} - K_{\nu\mu}\tilde{q}^{\mu}q^{\nu} + q^{\mu}K^{+}_{\mu\nu}\tilde{q}^{\nu} - q^{\nu}K^{+}_{\mu\nu}\tilde{q}^{\mu}\right)\right\}$$

where

$$K_{\rho\lambda} \;\equiv\; \partial_{\rho}\Omega_{\lambda} - \partial_{\lambda}\Omega_{\rho} + \Omega_{\rho}\Omega_{\lambda} - \Omega_{\lambda}\Omega_{\rho}$$

Again, to keep 1st order derivatives, we must treat $\Omega_{\mu}$ and $q^{\mu}$ as separate independent variables.

---

## Page 20

To handle the matter-field Hamiltonian in the spinor case, we use

$$\mathcal{H} = \frac{\partial \mathcal{L}}{\partial(\dot{\eta})}\,\dot{\eta} - \mathcal{L}, \qquad \pi_{\eta} = \frac{\partial \mathcal{L}}{\partial \dot{\eta}}$$

i.e. on

$$\mathcal{L}_M = i\,\eta^{+}q^{\mu}(\partial_{\mu}+\Omega_{\mu})\eta \;+\; i\,\chi^{+}\tilde{q}^{\mu}(\partial_{\mu}+\Omega^{(\chi)}_{\mu})\chi$$

$$\frac{\partial \mathcal{L}_M}{\partial \dot{\eta}} = i\,\eta^{+}q^{0} = \pi_{\eta}, \qquad \frac{\partial \mathcal{L}_M}{\partial \dot{\chi}} = i\,\chi^{+}\tilde{q}^{0} = \pi_{\chi}$$

*(margin):  $\mathcal{L} = A\dot{\eta}$, $\;\partial\mathcal{L}/\partial\dot{\eta} = A$, $\;\mathcal{H} = A\dot{\eta} - A\dot{\eta} = 0\,!$*

So

$$\mathcal{H} = i\,\eta^{+}q^{0}\pi_{\eta} + i\,\chi^{+}\tilde{q}^{0}\pi_{\chi} \;-\; i\,\eta^{+}q^{\mu}(\partial_{\mu}+\Omega_{\mu})\eta \;-\; i\,\chi^{+}\tilde{q}^{\mu}(\partial_{\mu}+\Omega^{(\chi)}_{\mu})\chi$$

$$= \cdots$$

No, we want

$$\mathcal{L}_M = \tfrac{i}{2}\!\left(\eta^{+}q^{\mu}\partial_{\mu}\eta - (\partial_{\mu}\eta^{+})q^{\mu}\eta\right) \;+\; \tfrac{i}{2}\!\left(\chi^{+}\tilde{q}^{\mu}\partial_{\mu}\chi - (\partial_{\mu}\chi^{+})\tilde{q}^{\mu}\chi\right)$$

*(assuming $q^{\mu+} = q^{\mu}$).*

The energy-momentum tensor is

$$\Theta^{\mu\nu} = (\partial^{\nu}\eta^{+})\frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\eta^{+})} + \frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\eta)}\,\partial^{\nu}\eta$$
$$\quad + (\partial^{\nu}\chi^{+})\frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\chi^{+})} + \frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\chi)}\,\partial^{\nu}\chi \;-\; g^{\mu\nu}\mathcal{L}$$

$$= \tfrac{i}{2}\!\left(\eta^{+}q^{\mu}\partial^{\nu}\eta + (\partial^{\nu}\eta^{+})q^{\mu}\eta + \chi^{+}\tilde{q}^{\mu}\partial^{\nu}\chi + (\partial^{\nu}\chi^{+})\tilde{q}^{\mu}\chi\right)$$

---

## Page 21

and

$$\mathcal{H}_M = \Theta^{00} = \tfrac{i}{2}\!\left(\eta^{+}q^{0}(\partial_{0}\eta) + (\partial_{0}\eta^{+})q^{0}\eta + \chi^{+}\tilde{q}^{0}(\partial_{0}\chi) + (\partial_{0}\chi^{+})\tilde{q}^{0}\chi\right)$$

This does not seem right — maybe ok for flat spacetime, but not curved, as this doesn't show any interaction of $\eta$ & $\chi$ with curvature. It seems like $\Theta^{\mu\nu}$ needs to be redefined with covariant derivatives,

$$\Theta^{\mu\nu} = \eta^{+;\nu}\frac{\partial \mathcal{L}}{\partial(\eta^{+}_{;\mu})} + \frac{\partial \mathcal{L}}{\partial(\eta_{;\mu})}\,\eta^{;\nu}$$
$$\quad + \chi^{+;\nu}\frac{\partial \mathcal{L}}{\partial(\chi^{+}_{;\mu})} + \frac{\partial \mathcal{L}}{\partial \chi_{;\mu}}\,\chi^{;\nu} \;-\; g^{\mu\nu}\mathcal{L}$$

$$\mathcal{L}_M = \tfrac{i}{2}\!\left(\eta^{+}q^{\mu}\eta_{;\mu} - \eta^{+}_{;\mu}q^{\mu}\eta\right) + \tfrac{i}{2}\!\left(\chi^{+}\tilde{q}^{\mu}\chi_{;\mu} - \chi^{+}_{;\mu}\tilde{q}^{\mu}\chi\right)$$

$$\Theta^{00} = \tfrac{i}{2}\!\left(\eta^{+}q^{0}\eta_{;0} + \eta^{+}_{;0}q^{0}\eta + \chi^{+}\tilde{q}^{0}\chi_{;0} + \chi^{+}_{;0}\tilde{q}^{0}\chi\right)$$

We must derive classical equations of motion to see if these are correct. Try w/ non-spinor form first. Add a scalar field for matter to interact w/:

$$\mathcal{L}_M = i\,\partial_{\mu}\varphi\,\partial^{\mu}\varphi - \mu^{2}\varphi^{2}$$

or, in G.R.,

$$\mathcal{L}_M = i\,\varphi_{;\mu}\varphi^{;\mu} - \mu^{2}\varphi^{2}$$

---

## Page 22

$$\frac{\partial \mathcal{L}}{\partial(\varphi_{;\mu})} = 2i\,\varphi_{;\mu}$$

$$\mathcal{H}_M = \varphi_{;0}\,\frac{\partial \mathcal{L}}{\partial(\varphi_{;0})} - \mathcal{L}$$

$$= 2i\,\varphi_{;0}\,\varphi^{;0} + i\,\varphi_{;i}\,\varphi^{;i} + \mu^{2}\varphi^{2}$$

But the covariant derivative of a scalar is just the ordinary derivative, so

$$\mathcal{H}_M = i\,\partial_{0}\varphi\,\partial^{0}\varphi + i\,\nabla\varphi\cdot\nabla\varphi + \mu^{2}\varphi^{2}$$

So the total Hamiltonian density, w/ the measure factor, is

$$\boxed{\;\mathcal{H} = \frac{(-g)^{1/2}}{8\pi}\!\left\{\partial_{\lambda}\Gamma^{\lambda}_{00} - \partial_{0}\Gamma^{\lambda}_{0\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{00} - \Gamma^{\alpha}_{\beta 0}\Gamma^{\beta}_{0\alpha}\right.}$$
$$\boxed{\quad\left.-\tfrac{1}{2}g_{00}g^{\mu\nu}\!\left(\partial_{\lambda}\Gamma^{\lambda}_{\mu\nu} - \partial_{\mu}\Gamma^{\lambda}_{\nu\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{\mu\nu} - \Gamma^{\alpha}_{\beta\nu}\Gamma^{\beta}_{\mu\alpha}\right)\right\}}$$
$$\boxed{\quad +\; i(-g)^{1/2}\!\left(\partial_{0}\varphi\,\partial^{0}\varphi + i\,\nabla\varphi\cdot\nabla\varphi + \mu^{2}\varphi^{2}\right)\;}$$

$$\frac{d}{dx_{\nu}}\!\left(\frac{\partial \mathcal{L}}{\partial \eta_{\rho,\nu}}\right) - \frac{\partial \mathcal{L}}{\partial \eta_{\rho}} = 0 \qquad \text{Lagrange field eqn.}$$

---

## Page 23 — Lagrangian Approach

The Lagrangian, in concise notation, is

$$\boxed{\;\mathcal{L} = (-g)^{1/2}\!\left\{R + i\,\eta^{+}q^{\mu}\eta_{;\mu} + i\,\chi^{+}\tilde{q}^{\mu}\chi_{;\mu}\right\}\;}$$

where

$$\eta_{;\mu} = \partial_{\mu}\eta + \Omega_{\mu}\,\eta$$
$$\chi_{;\mu} = \partial_{\mu}\chi + \Omega^{(\chi)}_{\mu}\,\chi$$

$$R = \tfrac{1}{4}\mathrm{Tr}\!\left(K_{\mu\nu}q^{\mu}\tilde{q}^{\nu} - K_{\mu\nu}\tilde{q}^{\mu}q^{\nu} + q^{\mu}K^{+}_{\mu\nu}\tilde{q}^{\nu} - q^{\nu}K^{+}_{\mu\nu}\tilde{q}^{\mu}\right)$$

$$\to \;\Omega_{\lambda,\rho} - \Omega_{\rho,\lambda}$$

$$K_{\rho\lambda} = \partial_{\rho}\Omega_{\lambda} - \partial_{\lambda}\Omega_{\rho} + \Omega_{\rho}\Omega_{\lambda} - \Omega_{\lambda}\Omega_{\rho}$$

$$g \equiv -\det g_{\mu\nu}, \qquad \text{or}\;\; g^{\mu\nu} = -\tfrac{1}{2}(q^{\mu}\tilde{q}^{\nu} + q^{\nu}\tilde{q}^{\mu})$$

Now, treating $q^{\mu}$, $\tilde{q}^{\mu}$, $\Omega^{\mu}$ and $\Omega^{(\chi)}_{\mu}$ independently, can we derive equations of motion? We should write all of this out, then apply the Lagrange eqn:

$$\partial^{\nu}\!\left(\frac{\partial \mathcal{L}}{\partial \eta_{\rho,\nu}}\right) - \frac{\partial \mathcal{L}}{\partial \eta_{\rho}} = 0$$

*(margin: No)*

We may use $\;\dfrac{\partial\,\mathrm{Tr}(AB)}{\partial B} = \tilde{A}\;$ to get

$$\frac{\partial(-g)^{1/2}}{\partial \tilde{q}^{\lambda}} = \left(\tfrac{1}{4}q_{\lambda}(-g)^{-1/2}\right)^{*}$$

*(margin: In curved space:)*

$$\left(\frac{\partial \mathcal{L}}{\partial(\eta_{\rho;\nu})}\right)_{\!;\nu} - \frac{\partial \mathcal{L}}{\partial \eta_{\rho}} = 0$$

---

## Page 24

Trying this with $\eta$:

$$\frac{\partial \mathcal{L}}{\partial \eta_{;\mu}} = \frac{\partial}{\partial \eta_{;\mu}}\!\left[(-g)^{1/2}\,i\,\eta^{+}q^{\nu}\eta_{;\nu}\right]$$

$$= (-g)^{1/2}\,i\,\eta^{+}q^{\mu}$$

$$\left(\frac{\partial \mathcal{L}}{\partial \eta_{;\mu}}\right)_{\!;\mu} = \left((-g)^{1/2}\,i\,\eta^{+}q^{\mu}\right)_{\!;\mu}$$

$$= i\,\left\{(-g)^{1/2}_{\;;\mu}\,\eta^{+}q^{\mu} + (-g)^{1/2}\,\eta^{+}_{;\mu}\,q^{\mu} + (-g)^{1/2}\,\eta^{+}q^{\mu}_{\;;\mu}\right\}$$

$$\frac{\partial \mathcal{L}}{\partial \eta} = \cdots\;\frac{\partial \mathcal{L}}{\partial \eta^{+}}$$

If we write the interaction term so that $\mathcal{L} = \mathcal{L}^{+}$, then

$$\mathcal{L}_\eta = \tfrac{1}{2}\!\left[i\,\eta^{+}q^{\mu}\eta_{;\mu} - i\,\eta^{+}_{;\mu}q^{\mu}\eta\right](-g)^{1/2}$$

Then

$$\frac{\partial \mathcal{L}}{\partial \eta} = -\tfrac{1}{2}i\,\eta^{+}_{;\mu}q^{\mu}(-g)^{1/2}$$

$$\frac{\partial \mathcal{L}}{\partial \eta^{+}} = \tfrac{1}{2}i\,q^{\mu}\eta_{;\mu}(-g)^{1/2}$$

$$\left(\frac{\partial \mathcal{L}}{\partial \eta_{;\mu}}\right)_{\!;\mu} = \tfrac{i}{2}\!\left((-g)^{1/2}_{\;;\mu}\,\eta^{+}q^{\mu} + (-g)^{1/2}\eta^{+}_{;\mu}q^{\mu} + (-g)^{1/2}\eta^{+}q^{\mu}_{\;;\mu}\right)$$

$$\left(\frac{\partial \mathcal{L}}{\partial \eta^{+}_{;\mu}}\right)_{\!;\mu} = -\tfrac{i}{2}\!\left((-g)^{1/2}_{\;;\mu}\,q^{\mu}\eta + (-g)^{1/2}q^{\mu}_{\;;\mu}\eta + (-g)^{1/2}q^{\mu}\eta_{;\mu}\right)$$

---

## Page 25

Whereby

(1a) $\quad\tfrac{i}{2}\!\left((-g)^{1/2}_{\;;\mu}\,\eta^{+}q^{\mu}\right) + \tfrac{i}{2}(-g)^{1/2}\!\left(\eta^{+}_{;\mu}q^{\mu} + \eta^{+}q^{\mu}_{\;;\mu} + \eta^{+}_{;\mu}q^{\mu}\right) = 0$

(1b) $\quad -\tfrac{i}{2}(-g)^{1/2}_{\;;\mu}\,q^{\mu}\eta - \tfrac{i}{2}(-g)^{1/2}\!\left(q^{\mu}_{\;;\mu}\eta + q^{\mu}\eta_{;\mu} + q^{\mu}\eta_{;\mu}\right) = 0$

Now $(-g)^{1/2}_{\;;\mu} = 0$ per p. 52 of Notebook 2. This follows from $g = -\det g_{\mu\nu}$ and $g_{\mu\nu;\rho} = g^{\mu\nu}_{\;;\rho} = 0$ &

$$\frac{\partial (-g)^{1/2}}{\partial g^{\rho\sigma}} = -\tfrac{1}{2}(-g)^{1/2}g_{\rho\sigma}$$

Whereby

(2a) $\quad 2\eta^{+}_{;\mu}q^{\mu} + \eta^{+}q^{\mu}_{\;;\mu} = 0$

(2b) $\quad 2q^{\mu}\eta_{;\mu} + q^{\mu}_{\;;\mu}\eta = 0$

What can we say of $q^{\mu}_{\;;\mu}$? $\;\tilde{q}^{\mu}_{\;;\rho} = 0$ per back of Sachs, p. 64. Per notebook p. 42, this gives $q^{\mu}_{\;;\rho} = 0$ too. Whereby

$$\eta^{+}_{;\mu}q^{\mu} = 0$$
$$q^{\mu}\eta_{;\mu} = 0$$

And if $q^{\mu}$ is hermitian, $q^{\mu+} = q^{\mu}$, these are just the same equation,

$$\boxed{\;q^{\mu}\partial_{\mu}\eta + q^{\mu}\Omega_{\mu}\eta = 0\;}$$

---

## Page 26

*(small sketch at top: a coil/spring icon flowing into a rectangular block — perhaps representing a flow or transformation diagram.)*

Next, we want to consider $\mathcal{L}$ and the terms $q^{\mu}$ and $\Omega_{\rho}$. Starting with $\Omega$,

$$\mathcal{L} = (-g)^{1/2}\!\left\{\tfrac{1}{4}\mathrm{Tr}\!\left(K_{\mu\nu}q^{\mu}\tilde{q}^{\nu} - K_{\nu\mu}q^{\mu}\tilde{q}^{\nu} + q^{\mu}K^{+}_{\mu\nu}\tilde{q}^{\nu} - q^{\nu}K^{+}_{\nu\mu}\tilde{q}^{\mu}\right)\right.$$
$$\left.\quad + \tfrac{i}{2}\eta^{+}q^{\mu}(\partial_{\mu}\eta + \Omega_{\mu}\eta) - \tfrac{i}{2}(\partial_{\mu}\eta^{+} + \eta^{+}\Omega^{+}_{\mu})\,q^{\mu}\eta\right\}$$

$$K_{\mu\nu} = \Omega_{\nu,\mu} - \Omega_{\nu,\mu} \quad\text{(antisymmetric in $\mu,\nu$)}$$

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}} = (-g)^{1/2}\,\tfrac{1}{4}\,\frac{\partial}{\partial \Omega_{\rho,\nu}}\mathrm{Tr}\!\left[(\Omega_{\nu,\nu} - \Omega_{\nu;\mu})q^{\mu}\tilde{q}^{\nu}\right.$$
*(margin: Treat $\Omega \;\&\; \Omega^{+}$ as separate variables.)*
$$\quad - (\Omega_{\nu,\mu} - \Omega_{\nu,\nu})\,\tilde{q}^{\mu}q^{\nu} - q^{\mu}(\Omega^{+}_{\nu,\nu} - \Omega^{+}_{\nu,\mu})\tilde{q}^{\nu}$$
$$\left.\quad + q^{\mu}(\Omega^{+}_{\nu,\mu} - \Omega^{+}_{\nu,\nu})\tilde{q}^{\nu}\right]$$

Now we need some formulas:

$$\frac{\partial\,\mathrm{Tr}[AB]}{\partial B_{ij}} = A_{ji}, \qquad \text{or}\;\; \frac{\partial\,\mathrm{Tr}(AB)}{\partial B} = \tilde{A} \;\;(\text{transpose})$$

$$\frac{\partial\,\mathrm{Tr}(ABC)}{\partial B} = A^{t}C^{t}$$

So

$$\frac{\partial}{\partial \Omega_{\rho,\nu}}\mathrm{Tr}\!\left((\Omega_{\nu,\nu} - \Omega_{\nu,\mu})\,q^{\mu}\tilde{q}^{\nu}\right) = (q^{\rho}\tilde{q}^{\nu})^{t} - (q^{\nu}\tilde{q}^{\rho})^{t} = \widetilde{q^{\nu}}\tilde{q}^{\rho} - \widetilde{q^{\rho}}\tilde{q}^{\nu}$$

$$\frac{\partial}{\partial \Omega_{\rho,\nu}}\mathrm{Tr}\!\left((\Omega_{\nu,\nu} - \Omega_{\nu,\nu})\,\tilde{q}^{\mu}q^{\nu}\right) = (\tilde{q}^{\rho}q^{\nu} - \tilde{q}^{\nu}q^{\rho})^{t}$$

---

## Page 27 — Question

G.R. says the world is locally Lorentzian. e.g. in a small enough neighborhood of any given point $x$, in the local coord. sys. at that point, $g_{\mu\nu}(x) \to g^{*}_{\mu\nu} = (1, -1, -1, -1)$. Is this identical to requiring $q^{\mu} \to \sigma^{\mu}$ at that point or not? Could there be a whole set of $q$'s at any point that give the same $g_{\mu\nu}$? Presumably so, like a gauge invariance, with $\sigma^{\mu}g^{\mu\nu} = -\tfrac{1}{2}(q^{\mu\nu}\tilde{q} + q^{\nu}\tilde{q}^{\mu})$ and $q^{\mu} = \sum_{\nu} q^{\mu}_{\;\nu}\sigma^{\nu}$. $q^{\mu}$ is a matrix, $g^{\mu\nu}$ a scalar.

Factor the Lorentz metric,

$$g^{*}_{\mu\nu} = \tfrac{1}{2}(q^{\mu}\tilde{q}^{\mu}) = \begin{cases} 1, & \mu = 0 \\ -1, & \mu = 1,2,3 \end{cases}$$

and

$$g^{\mu\nu} = 0 = -\tfrac{1}{2}(q^{\mu}\tilde{q}^{\nu} + q^{\nu}\tilde{q}^{\mu}), \quad \mu \neq \nu$$

Writing the spinor component form,

$$q^{\mu\nu} = \sum_{\alpha\beta} q^{\mu}_{\;\alpha}\,q^{\nu}_{\;\beta}\,\sigma^{\alpha}\tilde{\sigma}^{\beta}, \qquad \tilde{\sigma}^{\beta} = \begin{cases} \sigma^{0}, & \beta = 0 \\ -\sigma^{\beta}, & \beta = 1,2,3 \end{cases}$$

$$\frac{\partial(\mathrm{Tr}(AB^{\pm}C))}{\partial B} = CA$$

$$\frac{\partial}{\partial B_{mn}}\!\left(\sum_{i,j,k} A_{ij}B_{kj}C_{ki}\right) = \sum_{i} A_{in}C_{mi} = (CA)_{mn} = (A^{t}C^{t})_{mn}$$

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}}\,\mathrm{Tr}\!\left(q^{\mu}(\Omega^{+}_{\nu,\nu} - \Omega^{+}_{\nu,\mu})\tilde{q}^{\nu}\right) = \widetilde{q}^{\nu}q^{\rho} - \widetilde{q}^{\rho}q^{\nu}$$

---

## Page 28

$$\frac{\partial}{\partial \Omega_{\rho,\nu}}\!\left(q_{\mu}(\Omega_{\mu,\nu}^{+} - \Omega^{+}_{\nu,\mu})\tilde{q}^{\nu}\right) = \widetilde{q}_{\rho}\,q_{\nu} - \widetilde{q}_{\nu}\,q_{\rho}$$

So

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}} = \tfrac{1}{4}(-g)^{1/2}\!\left[\widetilde{q^{\nu}\tilde{q}^{\rho}} - \widetilde{q^{\rho}\tilde{q}^{\nu}} - \widetilde{\tilde{q}^{\rho}q^{\nu}} + \widetilde{\tilde{q}^{\nu}q^{\rho}}\right.$$
$$\left.\qquad + \widetilde{q^{\nu}\tilde{q}^{\rho}} - \widetilde{q^{\rho}\tilde{q}^{\nu}} - \widetilde{\tilde{q}^{\rho}q^{\nu}} + \widetilde{\tilde{q}^{\nu}q^{\rho}}\right]$$

$$= \tfrac{1}{4}(-g)^{1/2}\!\left[\widetilde{q^{\nu}}\tilde{q}^{\rho} + \widetilde{q^{\nu}}\tilde{\tilde{q}}^{\rho} + \tilde{q}^{\nu}\widetilde{q^{\rho}} + \tilde{\tilde{q}}^{\nu}\widetilde{q^{\rho}}\right.$$
$$\left.\qquad - \widetilde{q^{\rho}}\tilde{q}^{\nu} - \widetilde{q^{\rho}}\tilde{\tilde{q}}^{\nu} - \tilde{q}^{\rho}\widetilde{q^{\nu}} - \tilde{\tilde{q}}^{\rho}\widetilde{q^{\nu}}\right]$$

Likewise,

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho}} = \tfrac{i}{2}\,\eta^{+}q^{\rho}\eta(-g)^{1/2}$$

is a current term.

Now, we need to *(margin: This way above — many a $\sim$)*

$$\left(\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}}\right)_{\!;\nu} = \tfrac{i}{4}(-g)^{1/2}\!\left(\widetilde{q}^{\nu}q^{\rho} + q^{\nu}\widetilde{q}^{\rho} - \widetilde{q}^{\rho}q^{\nu} - q^{\rho}\widetilde{q}^{\nu}\right)_{\!;\nu}$$

This appears to all go to 0 — not good! See notebook 2 p 53.

$$\left(\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}}\right)_{\!;\nu} = \left[\tfrac{1}{4}(-g)^{1/2}\!\left(\widetilde{q}^{\nu}q^{\rho}\tilde{q}^{\nu} - \widetilde{q}^{\nu}\tilde{q}^{\rho}q^{\nu}\right)\right]_{\!;\nu}$$

And for matrix $(-g)^{1/2}_{\;;\nu} = 0$, so

$$\tfrac{1}{2}\!\left(\widetilde{q}^{\rho}q^{\nu} - \widetilde{q}^{\nu}q^{\rho}\right)_{\!;\nu} = -\tfrac{i}{2}\eta^{+}q^{\rho}\eta$$

Sachs gets 0 on the LHS & gets usual relation of $\Omega$ to $q$... but apparently this

---

## Page 29

doesn't hold! Now, also

We also get, for the field part,

$$\frac{\partial \mathcal{L}}{\partial q^{\lambda}} = (-g)^{1/2}\!\left(-\tfrac{1}{2}\!\left(K^{+}_{\lambda\rho}\widetilde{q}^{\rho} + \widetilde{q}^{\rho}K_{\lambda\rho}\right)^{*} + \tfrac{1}{4}R\,\widetilde{q}^{*}_{\lambda}\right)$$

and

$$\frac{\partial \mathcal{L}_M}{\partial q^{\lambda}} = \left(\tfrac{i}{2}\eta^{+}\eta_{;\lambda} - \tfrac{i}{2}\eta^{+}_{;\lambda}\eta\right)(-g)^{1/2}$$

Need $\;\widetilde{\Omega}^{(\chi)}_{\rho} = -\Omega^{x+}_{\rho} = \Omega_{\rho}\;$

---

## Page 30

*(Page is blank/bleed-through from previous pages — no original content.)*
