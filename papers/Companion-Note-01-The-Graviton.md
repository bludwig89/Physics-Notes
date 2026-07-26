# Companion Note 1 — The Graviton in the Lattice Model: Why It Exists, What It Is, What It Does, and How It Might Be Seen

**B. Ludwig**
*Independent researcher*

*Companion note to the "A Universe in a Bottle" series (Paper VII, Gravity). This is not a core paper (I–XII); it is a focused, self-contained account of a single object — the graviton — collecting the results of Findings F26, F64, F79, F106, F130, F178, F180, F216, F223, and F228 into one place, and extending them with a discussion of observable effects and detectability. Created 2026-07-15 - 19:14.*

---

## Abstract

In this model the graviton is not a fundamental particle. It is an **emergent, massless, spin-2, luminal collective mode** of the same lattice degrees of freedom that carry light — the real $(\mathbf E,\mathbf B)$ pairs and Weyl spinors of the BCC quantum cellular automaton. Its existence is *forced* rather than posited: the gravitational field is a single impedance-matched dielectric $K(x)$ that renormalises the field-rotation rate (Paper VII, F64); because source-free electromagnetism is conformally invariant in $3{+}1$D, that dielectric carries **zero bare kinetic term** (F79, tracelessness verified to $3.6\times10^{-15}$), so its entire stiffness — and hence its propagating quantum — is the *induced* one-loop response of the underlying modes (Sakharov-induced gravity, here a theorem, not a premise). That single fact fixes every characteristic of the graviton: it is massless (self-energy $\Pi(q)\propto Q^2$, $\Pi(0)=0$, protected by an emergent-diffeomorphism Ward identity, and any mass term is an RG-irrelevant lattice operator); it has exactly two transverse-traceless helicity-$\pm2$ polarisations; and it travels on the **one** lattice light cone $c_\text{grav}=c_\text{lat}=1/\sqrt3$ — identical to the photon's, satisfying GW170817 by $\sim68$ orders of magnitude. We give the derivation chain in full, catalogue the characteristics with their exactness tiers, and then discuss effects (the linearised Newtonian potential, gravitational waves, the model's small lattice dispersion correction, and the geon/Planck-remnant dark-matter object into which gravitons can collapse). We close with a candid treatment of measurability: the classical wave sector is already detected (LIGO/Virgo); a *single* graviton is effectively undetectable for the same reason it is in standard physics (Dyson); and the model's only distinctive, in-principle-falsifiable signatures are a Planck-suppressed high-frequency dispersion and the strict absence of graviton birefringence and of any massive/fifth-force branch.

---

## 1. Where the graviton sits in the model

The model's fundamental substrate is a body-centred-cubic (BCC) Weyl quantum cellular automaton (Paper I). Its physical excitations are real $(\mathbf E,\mathbf B)$ field pairs and spin-$\tfrac12$ Weyl quanta. The single reinterpretation that organises everything is that the speed of light is **not** a phase velocity but the angular rotation rate of the real $(\mathbf E,\mathbf B)$ pair per unit wavenumber (F26):

$$c_\text{lat}=\frac{d\Omega}{d\lvert\mathbf k\rvert}\bigg|_{\lvert\mathbf k\rvert\to0}=\frac{1}{\sqrt d}=\frac{1}{\sqrt3},\qquad \Omega=2\,\omega(\lvert\mathbf k\rvert/2).$$

Gravity, in this model, is **not a second fundamental interaction**. It is a single position-dependent scalar $K(x)$ — the *lattice dielectric* — that locally rescales that rotation rate (Paper VII, F64, D-EM5): a region of higher $K$ is a region where the $(\mathbf E,\mathbf B)$ pair rotates more slowly, $c_\text{eff}=c_\text{lat}/K$. The dielectric is impedance-matched, $\varepsilon=\mu=K$, so that

$$A=\frac1K,\qquad B=K,\qquad AB\equiv1,$$

and the reciprocal lock $AB=1$ keeps the impedance $\sqrt{\mu/\varepsilon}=1$ exactly position-independent. That is what makes it a *genuine dielectric* rather than a clock-only or refractive-only rescaling: the $(\mathbf E,\mathbf B)$ amplitude ratio is preserved and the field evolution stays a *proper* rotation with no scalar contamination. In the weak field $K=e^{2GM/rc^2}$, giving PPN $\beta=\gamma=1$ (GR-identical); under the full-tensor adoption (F178) the canonical law is the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, of which this dielectric is the vacuum/weak-field representation.

The **graviton is the propagating quantum of this dielectric field** — specifically, of ripples $\delta\ln K$ about the flat background $K=1$. The rest of this note explains why such ripples must exist, why they must be massless and luminal, and what they do. The essential and distinctive claim is stated once here and defended below: *there is no fundamental graviton field on this lattice.* The graviton is what a long-wavelength, collective wobble of the light-carrying modes looks like.

---

## 2. What causes the graviton to exist — the zero-tree-stiffness pivot (F79)

### 2.1 An "emergent mode of the lattice dielectric," defined

A mode is **fundamental** if you must write down its own kinetic term (its "stiffness") by hand in the action — the term that lets it propagate and store energy. A mode is **emergent** if it has *no such term of its own*, and acquires all of its dynamics from the collective response of other, more basic degrees of freedom. The canonical analogy is a phonon: there is no "phonon field" in a crystal's fundamental description; the phonon is a quantised sound wave, an emergent mode of the underlying atoms. It is perfectly real, carries energy and momentum, has a dispersion relation and a well-defined speed — but it exists *only* as an organised motion of the atoms, and its speed is inherited from their bonds, not chosen independently.

The claim of this model is that the graviton is emergent in exactly this sense, with the "atoms" being the lattice's $(\mathbf E,\mathbf B)$/spinor modes and the "sound wave" being a ripple in the dielectric $K$. What makes this more than an analogy is that the *absence* of a fundamental graviton kinetic term is a **theorem** here, not an assumption.

### 2.2 The theorem: the dielectric has zero bare kinetic term

$K$ is a **conformal (Weyl) factor**. Writing the conformal mode as $\sigma=\tfrac12\ln K$, a Weyl rescaling $g_{\mu\nu}\to e^{2\sigma}g_{\mu\nu}$ couples to matter only through the **trace** of the stress-energy tensor:

$$\delta S_\text{matter}=\int\sqrt{g}\;T^{\mu}{}_{\mu}\,\delta\sigma.$$

If $T^{\mu}{}_{\mu}=0$, then $\sigma=\tfrac12\ln K$ has **no source and no classical action** — it is a flat direction. And the model's dominant sector, source-free electromagnetism, is **conformally invariant in $3{+}1$ dimensions**: its stress tensor is exactly traceless,

$$T^{\mu}{}_{\mu}^{\,(\text{EM})}=-\tfrac12(E^2+B^2)+\big[-(E^2+B^2)+\tfrac32(E^2+B^2)\big]=0,$$

verified in the module on 4000 random $(\mathbf E,\mathbf B)$ configurations to $\lvert T^{\mu}{}_{\mu}\rvert_\text{max}=3.6\times10^{-15}$ (machine precision, F79-S3). (Control: a *massive* scalar has $T^{\mu}{}_{\mu}=m^2\phi^2\neq0$, mean $0.49>0$ — mass *does* source $K$, which is precisely the F52/F106 rest-energy coupling. Mass sources gravity; the massless kinetic modes set gravity's *stiffness*, and they do so with no tree term.)

So there is **no fundamental graviton on this lattice whose bare stiffness one could measure.** $K$ is a derived reparametrisation of the rotation rule; a derived quantity has no independent kinetic term.

### 2.3 The consequence: the graviton's kinetic term *is* the matter vacuum polarisation

If $K$ has no tree kinetic term, then a wrinkle in $K$ can only acquire dynamics — only propagate, only carry energy — by dragging the surrounding fundamental modes. Formally, with the tree term absent, the graviton's **inverse propagator equals the one-loop vacuum polarisation** $\Pi(q)$ of the $(\mathbf E,\mathbf B)$/spinor modes coupling to $\delta\ln K$. This is Sakharov's "induced gravity": the metric's stiffness is entirely a Casimir/vacuum-fluctuation response of the matter it lives among. In most theories induced gravity is a *choice* (one posits no bare Einstein–Hilbert term); here it is *forced* by the tracelessness above (F79 resolves the F60 tree-vs-loop fork as a theorem: $1/G\propto1/c_\text{lat}=\sqrt d$, the loop channel, because there is nothing for the tree channel to measure).

This is the whole cause of the graviton's existence: **the graviton exists because the lattice's own vacuum fluctuations are stiff against a spatially varying rotation rate.** It is the quantised ripple of that induced stiffness. Newton's constant is the inverse of that stiffness, assembled entirely from lattice quantities (F79):

$$\frac1G=2\pi\,\eta\,g_*\sqrt d\;\frac{\hbar}{a^2c^3}\quad\Longleftrightarrow\quad G=\frac{a^2c^3}{8\pi\sqrt3\,\hbar}\ \ (d=3,\ \eta=\tfrac1{12},\ g_*=48),$$

with $a$ the cell size, $\eta=1/12$ the Weyl heat-kernel coefficient, and $g_*=48=16\times3$ the count of the lattice's protected normal modes ($16$ Weyl fields per generation $\times$ three generations, the latter itself a theorem about the $O_h$ point group). The apparent "dependence of $G$ on how much matter exists" is really dependence on the vacuum's representation theory.

---

## 3. The formation chain, step by step

Collecting §1–§2 into the causal sequence by which a graviton comes to be and to propagate (F26 → F64 → F79 → F106 → F180):

1. **One velocity.** The lattice has a single characteristic speed, the rotation rate $c_\text{lat}=1/\sqrt3$ (F26). Every fundamental propagator has this light cone.
2. **Gravity is a rate-rescaling.** A gravitational field is a spatial variation of that rate, encoded in the dielectric $K(x)$ (F64). A graviton is a small ripple $\delta\ln K$.
3. **No bare stiffness.** That ripple has no kinetic term of its own — the conformal mode is a flat direction of the traceless EM sector (F79).
4. **Induced stiffness.** The ripple can therefore only propagate through the induced self-energy $\Pi(q)$ of the constituent modes it perturbs. This *is* the graviton's kinetic operator.
5. **Inherited light cone.** A loop built from constituent propagators whose only light cone is $\omega=c_\text{lat}\lvert\mathbf k\rvert$ can depend on the external momentum $q=(q_0,\mathbf q)$ **only** through the constituent invariant

$$Q^2\equiv c_\text{lat}^2\lvert\mathbf q\rvert^2-q_0^2.$$

Hence $\Pi(q)=f(Q^2)$, the induced kinetic operator is the d'Alembertian $\Box=\nabla^2-c_\text{lat}^{-2}\partial_t^2$, and the graviton's light cone is forced to be $q_0=c_\text{lat}\lvert\mathbf q\rvert$ (F180, Leg 3). *There is no free speed to choose.* This was confirmed numerically: the induced self-energy is flat to $2.2\times10^{-5}$ along constant-$Q^2$ curves, while a control that ignores $c_\text{lat}$ varies by $\sim27\%$ — so the flatness is genuinely the constituent invariant, not an artefact.
6. **The wave equation.** Promoting the static F106 Poisson law to its causal completion:

$$\boxed{\;\Big(\nabla^2-\frac{1}{c_\text{lat}^2}\partial_t^2\Big)\ln K(\mathbf x,t)=-\frac{8\pi G}{c^4}\,T^{00}[\psi](\mathbf x,t)\;}\qquad(\text{D-GW})$$

with the lattice-only coefficient $8\pi G/c^4=a^2c_\text{lat}/(\hbar c)$ (exact, sympy residual $=0$). In vacuum ($T^{00}=0$) this gives $\delta\ln K\propto e^{i(\mathbf k\cdot\mathbf x-\omega t)}$ with $\omega=c_\text{lat}\lvert\mathbf k\rvert$: **gravitational waves at $c_\text{lat}=1/\sqrt3$.** Its static limit reproduces F106 exactly, so nothing already validated changes; D-GW only supplies the retarded time-derivative the elliptic law was missing.

In short: a graviton *forms* whenever a disturbance of the rotation rate is set up (by a moving mass, a merging binary, or a collapsing field configuration); it propagates by the induced polarisation of the vacuum modes; and it necessarily travels at the speed of light because it is built from the very modes that define that speed.

---

## 4. Characteristics, in depth, with exactness tiers

The following are the graviton's properties as the model derives them. Each row of Table 1 names the property, the mechanism, and the tier (exact-algebraic / machine-precision / analytic), so the strong claims are separated from the softer ones.

### 4.1 Not fundamental (emergent)

The graviton has no bare kinetic term; its entire stiffness is the induced (Sakharov) loop. *Tier: exact.* The forcing fact — EM tracelessness $T^{\mu}{}_{\mu}=0$ — is machine-precision ($3.6\times10^{-15}$); the channel selection and the mode count $g_*=48=16\times3$ are exact rationals/integers. This is the single most distinctive characteristic and everything below follows from it.

### 4.2 Massless — two independent reasons (F216)

**UV reason — transversality (exact-algebraic).** Since the graviton's inverse propagator *is* $\Pi(q)$, and $\Pi(q)\propto Q^2$ with $\Pi(0)=0$, the pole sits at $q_0^2=c_\text{lat}^2\lvert\mathbf q\rvert^2$: massless. A mass would require $\Pi(0)\neq0$, which the induced self-energy structurally cannot produce. The masslessness is protected by the transversality (the emergent-diffeomorphism Ward identity), *not* tuned.

**IR reason — RG irrelevance (F130).** No local diffeomorphism-invariant graviton mass term exists (this is precisely why massive gravity is hard to build). Any contribution to $\Pi(0)$ must come from diff-breaking lattice operators, which are the Lorentz-violating class of F130 and scale as $\lambda_n=b^{-n}<1$ under block-spin coarse-graining — **irrelevant**. Coarse-graining drives any induced mass to zero. So the graviton is massless from both the UV (transversality) and the IR (RG) side.

A massless mediator means gravity has infinite range and the potential is exactly $1/r$ — the observed behaviour, and (via the derived $V=-Gm^2/r$) the starting point for the geon bound state of §5.4.

### 4.3 Spin-2, two polarisations, transverse-traceless (F216)

Linearising the emergent metric $g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}$, the propagating vacuum content is the transverse-traceless tensor, with

$$N_\text{massless}=\frac{D(D-3)}{2}\bigg|_{D=4}=2,$$

the two helicity-$\pm2$ states $h_+,h_\times$, built explicitly and checked transverse and traceless to machine precision (F216-A1). *Tier: exact* (integer little-group identity + orthonormal $J_z$-eigenbasis). There is **no propagating third or "second-branch" mode in vacuum**: the extra polarisations one might imagine belong only to a *massive* spin-2 matter particle (five states, whose helicity-0 member is exactly the model's own $\tfrac12\ln K$ conformal/breathing channel), and no such massive mode exists in vacuum. Consequently there is **no vDVZ discontinuity and no fifth force** — a decisive, testable structural prediction (§6).

### 4.4 Luminal, at exactly the photon speed (F180)

$$c_\text{grav}=c_\text{lat}=\frac{1}{\sqrt3}=c_\text{photon}\quad\text{identically.}$$

This is not two numbers tuned to agree to $10^{-15}$; the photon (even paired-spinor law, F26/F105) and the graviton (D-GW) solve the **same** wave operator $\Box_\text{lat}=\nabla^2-c_\text{lat}^{-2}\partial_t^2$, so $c_\text{grav}$ and $c_\text{photon}$ are the *same symbol*. *Tier: exact at leading order* (slope residual $=0$, sympy). The independent corroboration is F59: the induced inverse coupling carries $1/G\propto1/c_\text{lat}=\sqrt d$ exactly — the gravity sector has one and only one velocity.

### 4.5 Non-birefringent, single light cone (F216, F67)

Both TT polarisations travel on the **one** lattice light cone; there is no second light cone and hence no graviton birefringence — the tensor analogue of the photon's exact non-birefringence (F67), and consistent with GW170817 polarimetry.

### 4.6 Self-energy $\propto Q^2$; inverse coupling $\propto 1/c_\text{lat}$

The induced self-energy is $\Pi(q)\propto Q^2$ (F180 Leg 3, F216-B1; exact-algebraic), and the induced inverse coupling carries $1/G\propto1/c_\text{lat}=\sqrt d$ (F59, machine precision, relative spread $\le7\times10^{-16}$ across $d=1,2,3$).

### 4.7 One honest limit — the scalar mode is what is explicitly built

D-GW as written derives the **scalar (trace/conformal) mode** — the $\tfrac12\ln K$ piece the impedance-locked dielectric carries directly. The full transverse-traceless *tensor* graviton (the physical GW polarisations of GR, §4.3) shares the same $\Box_\text{lat}$ by the identical argument — the induced loop light cone is common to every metric component — but the explicit TT-mode construction on the BCC lattice is flagged as the natural next build (F180 §5). This does not affect the speed or masslessness statements, which are properties of the shared light cone, not of the polarisation structure. It is recorded here so the note does not overclaim.

**Table 1 — the graviton at a glance**

| Property | Value / statement | Mechanism | Tier |
|---|---|---|---|
| Ontology | emergent collective mode of $(\mathbf E,\mathbf B)$/spinor vacuum | zero tree stiffness (F79) | exact (via $T^\mu{}_\mu=0$, $3.6\times10^{-15}$) |
| Mass | $0$ | $\Pi(q)\propto Q^2$, $\Pi(0)=0$; diff-breaking mass RG-irrelevant | exact-algebraic (F216/F180/F130) |
| Spin / dof | spin-2, 2 dof ($h_+,h_\times$) | $D(D-3)/2=2$; TT basis | exact (F216) |
| Speed | $c_\text{grav}=c_\text{lat}=1/\sqrt3=c_\gamma$ | same $\Box_\text{lat}$ as photon | exact slope (F180) |
| Birefringence | none | single light cone | exact (F216/F67) |
| Range / potential | infinite; $V=-Gm^2/r$ | masslessness | derived (linearised F79/F180) |
| Second/massive branch, fifth force | none in vacuum | no propagating massive spin-2 | derived (F216) |
| Coupling | $1/G=8\pi\sqrt3\,\hbar/(a^2c^3)$ | induced loop, structural inputs | exact-algebraic given $a$ (F79) |
| TT tensor mode explicit construction | shares $\Box_\text{lat}$; build pending | common induced light cone | open (F180 §5) |

---

## 5. What the graviton does — its effects

### 5.1 The static field: Newtonian gravity and GR

The static/slow-matter limit of D-GW ($\partial_t\to0$) is the F106 Poisson law $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$, and one-graviton exchange between two masses $m$ reproduces **exactly the Newtonian potential**

$$V(r)=-\frac{Gm^2}{r},\qquad \alpha_g\equiv\Big(\frac{m}{M_\text{Pl}}\Big)^2,$$

with $\alpha_g$ the gravitational "fine-structure constant" between two quanta of mass $m$ (F223 §2, derived, not posited). Beyond weak field, F178 makes the sector exact GR with constant $G$: the strong-field object is Schwarzschild/Kerr (light bending factor $K_\text{bend}\to4$, Mercury perihelion $42.98''$/century, PPN $\beta=\gamma=1$). So the everyday effects of the graviton are simply gravity: free fall, redshift, light deflection, orbital precession — all inherited from the dielectric's action on the rotation rate.

### 5.2 Gravitational waves — already observed

The vacuum solutions of D-GW are transverse waves at $c_\text{lat}$, i.e. classical gravitational radiation. This is the sector LIGO/Virgo already measure. The model's sharp statement is the *speed*: because photon and graviton share $\Box_\text{lat}$,

$$\frac{\lvert c_\text{grav}-c_\text{photon}\rvert}{c}=0\quad(\text{leading order}),$$

and even the first lattice correction is common to both. The residual against the GW170817 multimessenger bound ($\lvert c_\text{grav}-c_\gamma\rvert/c<10^{-15}$) is $\sim3\times10^{-83}$ at LIGO-band frequencies — the constraint is met with $\sim68$ orders of magnitude of margin. This is the effect that turned a potential falsification (the original F106 law was instantaneous/elliptic) into a confirmation (F180 closed audit C1).

### 5.3 The lattice dispersion correction — the model's distinctive kinematic signature

Because both photon and graviton descend from the same discrete rotation kernel, they share a small, computable high-frequency correction to the light cone:

$$c(k)=c_\text{lat}\Big(1-\tfrac16\,\Omega^2+\dots\Big),\qquad \Omega\sim c_\text{lat}(ka),$$

i.e. a Planck-scale dispersion suppressed by $(f/f_\text{Planck})^2$ with $f_\text{Planck}\sim1.86\times10^{43}$ Hz. This is a genuine model prediction (gravitational waves disperse ever-so-slightly, identically to light), but at any accessible frequency it is far below current sensitivity — at $100$ Hz the fractional deviation is $\sim10^{-83}$. It is the honest answer to "how would the graviton's lattice origin ever show up": in the ultraviolet, as a shared, tiny, non-birefringent dispersion — *not* as a species-dependent or polarisation-dependent effect.

### 5.4 Gravitons can bind — the geon / Planck-mass remnant (F223, F228)

A $1/r$ potential always admits bound states, so two gravitons can bind. The lowest $J=2$ (D-wave) state was solved to machine precision (F223); because the constituents are massless, the only self-consistent closure is the relativistic self-gravitating virial, which pins the bound-state ("geon") mass to the Planck scale, $\mu\simeq\sqrt2\,M_\text{Pl}\approx1.7\times10^{19}$ GeV. F228 then showed that a light perturbative $J=2$ geon is not stable *as* spin-2 (it cascades $n{=}3\to2\to1$ to the $J=0$ ground state), so the stable object is necessarily the Planckian one — which is stable as the F190/F107 **one-cell black-hole remnant**,

$$M_\text{rem}=\Big(\tfrac{\sqrt3}{2}\Big)^{1/2}M_\text{Pl}=\frac{3^{1/4}}{\sqrt2}\,M_\text{Pl}\approx0.9306\,M_\text{Pl}\approx1.14\times10^{19}\ \text{GeV},$$

because Hawking evaporation cannot shrink a horizon below one lattice cell. The upshot for this note: **the graviton's most exotic effect is that a sufficient concentration of gravitons collapses into the model's minimal black hole**, a stable, cold, collisionless dark-matter candidate — and the "graviton–graviton geon" and the "Planck-mass relic" are the same object under two descriptions. Its cosmic abundance is set by one external number (the primordial-black-hole fraction $\beta$, F238); this is a soft, un-derived input, and the note flags it as such rather than claiming a relic prediction.

---

## 6. How the graviton could be measured

There are three tiers, and it is important to keep them separate.

### 6.1 Classical gravitational waves — measured, and constraining

The coherent, many-graviton wave sector is already detected (LIGO/Virgo, and pulsar-timing arrays at nanohertz). This directly tests the model's wave equation D-GW. The model's specific, in-principle-falsifiable predictions here are:

- **Speed equal to light**, $\lvert c_\text{grav}-c_\gamma\rvert/c=0$ to leading order — *confirmed* by GW170817 with enormous margin, and any future multimessenger event that found a speed difference above the shared Planck-suppressed dispersion would falsify the shared-light-cone claim.
- **No graviton birefringence** — the two TT polarisations must travel identically; a measured polarisation-dependent GW speed or dispersion would falsify §4.5.
- **Exactly two tensor polarisations, no scalar/vector ("breathing" or longitudinal) modes** in vacuum, and **no fifth force / no vDVZ discontinuity** (§4.3). Tests for extra GW polarisations (with a sufficiently rich detector network) and precision fifth-force/equivalence-principle experiments are therefore direct probes: any confirmed extra propagating polarisation or composition-independent fifth force of gravitational strength would falsify the massless-only spectrum.
- **A shared, tiny UV dispersion** $c(k)=c_\text{lat}(1-\tfrac16\Omega^2+\dots)$ (§5.3), common to light and gravity, scaling as $(f/f_\text{Planck})^2$ — far below current reach, but the correct place to look for the lattice origin, and identical for both sectors (so it is *not* a Lorentz-violation-style species difference).

### 6.2 A single graviton — effectively undetectable (and the model agrees)

Detecting an *individual* graviton is a different matter. The standard argument (Dyson 2013, "Is a graviton detectable?") is that any detector able to absorb one graviton from an astrophysical source would have to be so massive that it collapses into a black hole, or the required exposure exceeds the age of the universe — the cross-section is suppressed by $(E/M_\text{Pl})^2=\alpha_g$, which is minuscule for any sub-Planckian energy. The lattice model reproduces this suppression *exactly*, because $\alpha_g=(m/M_\text{Pl})^2$ is the same gravitational coupling that appears in §5.1. So the model makes no optimistic promise here: single-graviton detection is as hopeless as in standard physics, and for the same structural reason. The graviton is "real" in the model in precisely the sense the phonon is real — a quantised collective mode — but its quantum-level coupling to matter is Planck-suppressed.

### 6.3 The dark-matter object — an indirect, cosmological probe

The one place the graviton sector could show up *non-gravitationally-weakly* is through the geon/Planck-remnant dark matter of §5.4. Because that object is the model's dark-matter candidate, the ordinary dark-matter programme becomes an indirect test: it must be cold, collisionless, and non-fuzzy (all satisfied — de Broglie wavelength $\sim1.7\times10^{-32}$ m, self-interaction $\sigma/m\approx1.7\times10^{-50}$ cm$^2$/g, far below the Bullet-Cluster bound), and it must preserve the model's own ΛCDM timeline ($z_\text{eq}\approx3430$, age $\approx13.8$ Gyr, $\Delta N_\text{eff}\approx0$ — all confirmed, F228 §4). It is genuinely dark: as a Planck-mass, gravitationally-coupled relic it has no electromagnetic, weak, or strong signature, so direct-detection and collider searches are expected to be null. The honest measurability statement is therefore that the *object* is constrained cosmologically (and its abundance rides on the free $\beta$), while the individual graviton that constitutes it is not accessible one at a time.

---

## 7. Summary

The graviton in this model is caused, not assumed. Gravity is a single impedance-matched dielectric that renormalises the lattice's field-rotation rate; that dielectric carries zero bare kinetic term because the electromagnetic vacuum is conformally invariant and traceless; and therefore the graviton's entire stiffness — its very ability to propagate — is the induced vacuum polarisation of the lattice's own light-carrying modes. From that one fact the graviton is forced to be an emergent, massless, spin-2, non-birefringent mode with exactly two polarisations, travelling on the identical light cone as the photon, $c_\text{grav}=c_\text{lat}=1/\sqrt3$. Its effects are gravity itself in the classical limit, gravitational radiation at the speed of light in the wave sector, a Planck-suppressed UV dispersion shared with light, and — at extreme concentration — collapse into the model's minimal one-cell black hole, which is its dark-matter candidate. It is measurable exactly where standard physics says it is (coherent gravitational waves, already detected, and several sharp null predictions: no birefringence, no extra polarisations, no fifth force) and unmeasurable exactly where standard physics says it is (single-graviton absorption, Planck-suppressed). The distinctive content of the model is not a new detectable graviton effect but a new *explanation* of why the graviton has the properties it does: it is the sound of the lattice.

---

## References (internal findings and modules)

- **F26** — the speed of light as the $(\mathbf E,\mathbf B)$ rotation rate ($c_\text{lat}=1/\sqrt3$); mass as confined rotation.
- **F64** — electromagnetic-connection gravity; the single impedance-matched lattice dielectric $K$; D-EM5 derivation of the dielectric placement. Module `ca-simulation/forks/gr_fork_F64_em_connection.py`.
- **F79** — Newton's constant from lattice structure; the zero-tree-stiffness theorem (EM tracelessness $3.6\times10^{-15}$); loop channel forced; $G=a^2c^3/(8\pi\sqrt3\,\hbar)$. Module `gr_fork_F79_structural_G.py`.
- **F106** — the static sourcing law $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$; coefficient $a^2c_\text{lat}/(\hbar c)$.
- **F130** — block-spin RG; diff-breaking (LIV) operators irrelevant, $\lambda_n=b^{-n}$.
- **F178** — full-tensor adoption; canonical induced Einstein equation, exact GR, constant $G$.
- **F180** — the gravitational-wave equation D-GW; $c_\text{grav}=c_\text{lat}$ derived (Leg 3 constituent invariant $Q^2$); GW170817 margin $\sim3\times10^{-83}$. Module `gr_fork_F180_gw_speed.py`.
- **F216** — metric graviton massless, 2 dof, no massive/second branch in vacuum; the massive spin-2 must be a gauge-neutral bound state. Module `gr_fork_F216_*`.
- **F223** — graviton–graviton $J=2$ geon binds; virial mass $\mu\simeq\sqrt2\,M_\text{Pl}$; derived potential $V=-Gm^2/r$, $\alpha_g=(m/M_\text{Pl})^2$. Module `gr_fork_F223_spin2_binding_relic.py`.
- **F228** — stability gate and production; one-cell remnant $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}\approx0.9306\,M_\text{Pl}$; geon $\equiv$ Planck relic; PBH-remnant route with free $\beta$. Module `gr_fork_F228_geon_production_stability.py`.
- **F190 / F107** — horizon-cell structure ($2\pi\sqrt3$ nats/cell; $a^2=8\pi\sqrt3\,\ell_P^2$) that floors evaporation at one cell.
- **F238** — the geon relic abundance as a genuinely free input.
- **Paper VII (Gravity)**, `papers/Paper-07-Gravity.md` — the parent paper this note expands.

## References (external)

- A. D. Sakharov, "Vacuum quantum fluctuations in curved space and the theory of gravitation" (1967) — induced gravity.
- M. Fierz, W. Pauli (1939); H. van Dam, M. Veltman / V. I. Zakharov (1970) — massive spin-2 and the vDVZ discontinuity.
- S. Weinberg, E. Witten (1980) — no massless composite spin-2 with a covariant conserved current (a *massive* composite is allowed).
- LIGO/Virgo, GW170817 multimessenger bound $\lvert c_\text{grav}-c_\gamma\rvert/c<10^{-15}$ (2017).
- F. Dyson, "Is a graviton detectable?" (2013) — single-graviton undetectability.
- J. A. Wheeler (1955), D. R. Brill & J. B. Hartle (1964) — geons and their quasi-stability.
- Babichev, Marzola, Raidal, Urban, Veermäe, von Strauss (2016) — massive spin-2 dark matter.
- MacGibbon (1987); Carr, Kohri, Sendouda, Yokoyama (2010) — Planck-mass black-hole relics as dark matter.
