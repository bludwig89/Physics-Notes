# Paper IX — Black Holes as Horizon-Free Dielectric Condensates: The Exponential Metric, Its Shadow, and the Fate of Hawking Radiation in a Cellular-Automaton Universe

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper IX. A strong-field application of Paper VII (gravity as a lattice dielectric); uses the SI calibration of Paper VII §5 / the F107 cell to convert dimensionless strong-field quantities into angular observables.*

---

## Abstract

In the BCC quantum-cellular-automaton (QCA) model, gravity is not curved spacetime but a position-dependent **lattice dielectric** $K(\mathbf x)$ that renormalises the $(\mathbf E,\mathbf B)$ rotation rate identified with the speed of light (Paper I, Paper VII). The canonical index $K=\exp(2GM/rc^2)$ with metric legs $A=1/K$, $B=K$ and reciprocal lock $AB\equiv1$ is exactly the isotropic **exponential metric**. It is general-relativistic to post-Newtonian order ($\beta=\gamma=1$), but in the strong field it departs from Schwarzschild qualitatively: **it has no event horizon.** We derive the strong-field sector in closed form. The areal radius $R(r)=re^{GM/rc^2}$ has a minimum — a throat — at $R_\text{min}=e\,GM/c^2$, just outside the Schwarzschild radius; the photon sphere sits at $R_\text{ph}=2\sqrt e\,GM/c^2$; and the critical impact parameter (shadow) is $b_c=2e\,GM/c^2$, a factor $2e/3\sqrt3=1.0463$ larger than Schwarzschild — a **$4.63\%$ larger shadow**. With the model's SI cell this predicts shadow diameters of $41.5\,\mu$as (M87\*) and $55.7\,\mu$as (Sgr A\*), within current Event Horizon Telescope precision but a fixed target for next-generation imaging. Because there is no horizon, the standard Hawking mechanism does not operate: the model predicts no thermal Hawking glow, dissolves the information paradox (consistent with its exactly unitary substrate), and reflects gravitational-wave ringdowns into **late-time echoes**. We catalogue the observables that distinguish a dielectric black hole from a Schwarzschild black hole, state the falsifiers, and flag the open debt — a microphysical account of black-hole thermodynamics. Nine field-level and observational checks pass.

---

## 1. Introduction

The black hole is general relativity's most extreme prediction and its sharpest conceptual problem. Its defining feature — the event horizon, a null surface from behind which no signal escapes — is also the origin of the information paradox: Hawking's calculation turns a pure infalling state into thermal radiation, in apparent violation of unitarity. Any theory that claims spacetime is fundamentally a discrete, deterministic, reversible substrate must eventually say what it makes of horizons and of Hawking radiation.

This paper answers that question for the QCA model of the present series. In Paper VII gravity was shown to be a single impedance-matched lattice dielectric: a position-dependent renormalisation $K(\mathbf x)$ of the field-rotation rate that *is* the local speed of light. The weak-field behaviour was fixed there — $\beta=\gamma=1$, Einstein factor-2 light bending, a structural Newton constant $G=a^2c^3/(8\pi\sqrt3\hbar)$, and (Paper VII §5 / F107) a parameter-free lattice cell $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ that turns dimensionless lattice quantities into SI numbers. Here we push the *same* canonical index into the strong field and read off what the model says a black hole is.

The answer is that the canonical index is the **exponential metric**, a known and observationally GR-degenerate alternative to Schwarzschild at post-Newtonian order, but one that is horizon-free. The contribution of this paper is not to invent horizonless black holes — that class is studied in the literature — but to show that the model's *independently motivated* dielectric gravity lands specifically on it, to work out its observables in closed form, to convert them to angular predictions using the model's own SI cell, and to face the consequences for Hawking radiation honestly.

---

## 2. The canonical index is the exponential metric

Paper VII fixes the static, isotropic gravitational field as a dielectric with refractive index equal to the canonical dielectric constant,

$$
n(r)=K=e^{2u},\qquad u\equiv\frac{GM}{rc^2}=-\frac{\phi}{c^2},
\tag{2.1}
$$

placed so that the permittivity and permeability scale together, $\varepsilon=\mu=K$, keeping the lattice impedance $\sqrt{\mu/\varepsilon}=1$ exactly (the "reciprocal lock"). Translated to an effective line element with metric legs $A\equiv-g_{tt}$ and $B\equiv g_{ij}/\delta_{ij}$, the proper-rotation requirement gives

$$
A=\frac1K=e^{-2u},\qquad B=K=e^{2u},\qquad AB\equiv1,
\tag{2.2}
$$

so that

$$
\boxed{\;ds^2=-e^{-2GM/rc^2}\,c^2dt^2+e^{2GM/rc^2}\big(dr^2+r^2d\Omega^2\big)\;}
\tag{2.3}
$$

This is the **isotropic exponential metric** (the Yilmaz/Papapetrou exponential form). Its weak-field expansion $e^{\pm2u}=1\pm2u+2u^2\pm\cdots$ reproduces the Newtonian potential at $O(u)$ and the Eddington PPN parameters $\beta=\gamma=1$ at $O(u^2)$, so every solar-system test is passed identically to GR (Paper VII; F112). The strong field is where it speaks.

### 2.1 No event horizon

The coordinate-time redshift factor is $\sqrt A=e^{-u}$. For Schwarzschild, $\sqrt{-g_{tt}}=\sqrt{1-2GM/rc^2}$ vanishes at the horizon $r_s=2GM/c^2$, producing an infinite-redshift null surface. For the exponential metric,

$$
-g_{tt}=e^{-2u}=e^{-2GM/rc^2}>0\quad\text{for all finite }r,
\tag{2.4}
$$

with $-g_{tt}\to0$ only in the limit $r\to0$. **There is no finite-radius horizon.** Equivalently, the local light speed is

$$
c_\text{loc}(r)=c\,\sqrt{A/B}=c\,e^{-2u}=c\,e^{-2GM/rc^2},
\tag{2.5}
$$

which decreases smoothly toward zero as $r\to0$ but never reaches zero at any finite radius. Light deep in the well is exponentially slowed and redshifted; it is not trapped behind a one-way membrane. A "black hole" is thus an **asymptotically frozen, horizon-free** object — black because of extreme slowing and redshift, not because of a causal seal. The CASIM strong-field scenario (§7) realises this: a compact source builds $K_\text{max}\sim5\times10^{50}$, i.e. $c_\text{loc}\sim10^{-50}c$ near the centre, with no trapping surface anywhere.

### 2.2 The throat

The areal radius (circumferential radius) is

$$
R(r)=r\sqrt B=r\,e^{u}=r\,e^{GM/rc^2}.
\tag{2.6}
$$

Setting $m\equiv GM/c^2$ and differentiating,

$$
\frac{dR}{dr}=e^{m/r}\Big(1-\frac{m}{r}\Big)=0\ \Longrightarrow\ r=m,
\tag{2.7}
$$

a minimum at which

$$
\boxed{\,R_\text{min}=m\,e^{1}=e\,\frac{GM}{c^2}\approx2.718\,\frac{GM}{c^2}\,}
\tag{2.8}
$$

The areal radius pinches to a **throat** at $e\,GM/c^2$, just outside the Schwarzschild radius $2GM/c^2$, and for $r<m$ it grows again — a wormhole-like second sheet rather than a trapped interior. Because no trapped surface ever forms, the Penrose singularity theorem (whose hypothesis is exactly a trapped surface) does not apply: the model is under no theorem-level obligation to hide a singularity.

---

## 3. Strong-field observables in closed form

All quantities below are exact (verified symbolically; §7), expressed in units of $m=GM/c^2$. Schwarzschild references in the same units: horizon $2$, photon sphere $3$, shadow $3\sqrt3$.

### 3.1 Photon sphere

For a static isotropic metric the circular-photon-orbit condition extremises $C/A$, with $C=R^2=r^2e^{2m/r}$ and $A=e^{-2m/r}$:

$$
\frac{C}{A}=r^2e^{4m/r},\qquad \frac{d}{dr}\!\left(r^2e^{4m/r}\right)=e^{4m/r}\,(2r-4m)=0\ \Longrightarrow\ r=2m.
\tag{3.1}
$$

The photon sphere is at isotropic radius $r=2m$, areal radius

$$
\boxed{\,R_\text{ph}=2m\,e^{1/2}=2\sqrt e\,\frac{GM}{c^2}\approx3.297\,\frac{GM}{c^2}\,}\qquad(+9.9\%\text{ vs GR}).
\tag{3.2}
$$

### 3.2 Shadow

The critical impact parameter that bounds the black-hole shadow seen by a distant observer is $b_c=\sqrt{C/A}$ evaluated at the photon sphere:

$$
b_c=\left.r\,e^{2m/r}\right|_{r=2m}=2m\,e^{1}=\boxed{\,2e\,\frac{GM}{c^2}\approx5.437\,\frac{GM}{c^2}\,}
\tag{3.3}
$$

Compared with the Schwarzschild value $3\sqrt3\,GM/c^2\approx5.196\,GM/c^2$, the ratio is

$$
\frac{b_c^\text{exp}}{b_c^\text{Schw}}=\frac{2e}{3\sqrt3}=1.0463,
\tag{3.4}
$$

a **$4.63\%$ larger shadow** — the single sharpest, cleanest strong-field departure, and the one within reach of horizon-scale imaging.

### 3.3 Surface redshift

At the throat ($r=m$), the redshift seen at infinity is

$$
1+z=\frac1{\sqrt A}=e^{m/r}\big|_{r=m}=e\approx2.718\quad(z\approx1.718),
\tag{3.5}
$$

a finite value. The redshift diverges only in the $r\to0$ limit; there is no finite-radius surface of infinite redshift. A material surface frozen near the throat would therefore present a large but finite redshift, not the formally infinite redshift of a horizon.

### 3.4 Second-order light bending

For a spherical index $n(w)=1+2\varepsilon w+\sigma\varepsilon^2w^2+\cdots$ ($w=b/r$, $\varepsilon=GM/bc^2$), the eikonal deflection has the closed form (companion script F111)

$$
\alpha=4\varepsilon+\pi(2+\sigma)\,\varepsilon^2+O(\varepsilon^3).
\tag{3.6}
$$

The exponential index $n=e^{2u}=1+2u+2u^2+\cdots$ has $\sigma=2$, giving $\alpha_2=4\pi$; isotropic Schwarzschild has $\sigma=7/4$, giving $\alpha_2=15\pi/4$. The dielectric black hole therefore **bends light more** than GR at second order,

$$
\Delta\alpha=\alpha_2^\text{exp}-\alpha_2^\text{Schw}=4\pi-\tfrac{15\pi}{4}=\tfrac{\pi}{4}\ \text{per }\varepsilon^2,
\tag{3.7}
$$

relevant for photon-ring (interferometric) measurements that probe rays skimming the photon sphere.

---

## 4. Predictions and observables

### 4.1 The shadow in microarcseconds

With the model's SI cell (Paper VII §5; F107) the relative enlargement (3.4) becomes an absolute prediction. Writing the gravitational angular scale $\theta_g=GM/(c^2D)$ for a source of mass $M$ at distance $D$, the shadow angular diameter is $6\sqrt3\,\theta_g$ (GR) or $4e\,\theta_g$ (dielectric):

| source | $M$ | $D$ | $\theta_g$ | GR shadow | dielectric shadow | measured ring |
|---|---|---|---|---|---|---|
| M87\* | $6.5\times10^9\,M_\odot$ | $16.8$ Mpc | $3.82\,\mu$as | $39.7\,\mu$as | $41.5\,\mu$as | $42\pm3\,\mu$as |
| Sgr A\* | $4.30\times10^6\,M_\odot$ | $8.28$ kpc | $5.13\,\mu$as | $53.3\,\mu$as | $55.7\,\mu$as | $52\pm2\,\mu$as |

The Event Horizon Telescope measures the bright emission **ring**, which is itself $\sim10\%$ wider than the shadow and carries $\sim5$–$10\%$ calibration uncertainty, so present data are consistent with both GR and the dielectric metric. The $4.63\%$ enlargement is, however, a fixed, parameter-free number — a clean discriminator for next-generation (ngEHT/space-VLBI) imaging, where the relevant comparison is the photon-ring diameter rather than the ring brightness peak.

### 4.2 Gravitational-wave echoes

A Schwarzschild horizon perfectly absorbs the ingoing part of a ringdown. A horizon-free object instead **reflects**, so the late-time gravitational-wave signal develops a train of **echoes** delayed by roughly the wave-crossing time of the deep well, $\Delta t_\text{echo}\sim (GM/c^3)\,\ln(\text{compactness})$. Echoes are the generic smoking gun of horizonless ultra-compact objects and are an active LIGO/Virgo/KAGRA (and, for supermassive mergers, LISA) search target. The model predicts their presence; an in-model echo-spectrum computation is posed but not yet done.

### 4.3 Summary of discriminators

A dielectric black hole differs from a Schwarzschild black hole in five measurable ways: (i) shadow $4.63\%$ larger; (ii) photon sphere $9.9\%$ larger; (iii) finite rather than infinite surface redshift; (iv) GW ringdown echoes; (v) excess second-order light bending $\tfrac{\pi}{4}\varepsilon^2$. All five follow from the single replacement of the Schwarzschild factor by the exponential $e^{2u}$.

---

## 5. Hawking radiation, thermodynamics, and information

The Hawking effect is anchored to the horizon: the thermal spectrum follows from the unbounded gravitational redshift of modes climbing out of the near-horizon region, and its temperature is set by the surface gravity $\kappa$ evaluated *at* the horizon, $T_H=\hbar\kappa/2\pi k_Bc$. With no horizon there is no infinite-redshift surface and no $\kappa$ to evaluate, so **the standard Hawking derivation does not operate**, and the model's default prediction is the absence of a thermal Hawking glow. (Astrophysical black holes are far too cold for Hawking radiation to be observable in any case, so this is not in tension with data.) Three consequences deserve explicit statement.

**Information paradox dissolved.** No horizon means nothing is causally sealed; an infalling pure state remains, in principle, recoverable. This is not an added assumption but a near-requirement of the model's foundation: the QCA substrate evolves by exactly unitary ticks (Papers I–II), so global information is conserved by construction, and a genuinely information-destroying horizon would be inconsistent with that substrate. The horizon-free black hole and the unitary automaton pull in the same direction.

**Thermodynamics is an open debt.** Black-hole thermodynamics — the area-entropy law $S=A/4$, the first law, the area theorem — is built on horizons, and astrophysical black holes empirically behave thermodynamically (e.g. merger areas do not decrease). A horizon-free model must explain *why* the area law works as well as it does. The natural candidate is that the frozen ultra-compact object carries genuine statistical entropy from internal lattice microstates that approximate $A/4$; demonstrating this from the QCA degrees of freedom is the principal unsolved problem this paper exposes, and we flag it as such rather than paper over it.

**Where a Hawking-like effect could re-enter.** Because gravity here is literally a dielectric, the analog-gravity literature is directly relevant: in a *moving* or *flowing* medium, Hawking-like emission arises at an **optical horizon**, the surface where the medium's flow speed equals the local wave speed (the basis of claimed laboratory analog-Hawking experiments). A static exponential dielectric has no such surface, but a dynamical, accreting, or collapsing configuration could develop a transient optical horizon and radiate there. This is the natural route by which something Hawking-shaped might be recovered; it is speculative and must be built and tested, not asserted.

---

## 6. Falsifiability

The strong-field predictions are rigid because the index (2.1) and the SI cell are both fixed with no free parameter. The model is falsified by any of: (i) a measured horizon-scale shadow that excludes the $+4.63\%$ enlargement once photon-ring precision reaches the few-percent level; (ii) confirmation of a true event horizon (e.g. an absorptive surface with no echoes) at the precision where echoes would be expected; (iii) detection of a thermal Hawking spectrum from an astrophysical horizon; (iv) a strong-field light-bending measurement consistent with Schwarzschild's $15\pi/4$ but excluding $4\pi$ at second order. Conversely, a robust GW-echo detection or a confirmed shadow enlargement would be strong positive evidence.

---

## 7. Methods

All strong-field quantities are derived symbolically (`sympy`) in `model-tests/test_F114_dielectric_black_hole.py`: the absence of a finite horizon (no real root of $g_{tt}$, $c_\text{loc}\to0$ only at $r\to0$), the throat $R_\text{min}=e$, the photon sphere $R_\text{ph}=2\sqrt e$, the shadow $b_c=2e$, the throat redshift $1+z=e$, and the second-order deflection coefficient $4\pi$. EHT diameters use measured masses and distances (EHT 2019 for M87\*; EHT 2022 and GRAVITY 2022 for Sgr A\*) with CODATA constants as readout anchors only. The field-level strong-field picture is rendered by the CASIM scenario `scenarios/dielectric_black_hole.yaml`, which builds the canonical index $K=e^{2u}$ from an open-boundary Poisson source on a $64^3$ cubic lattice and reports $K_\text{max}=5.1\times10^{50}$ (local light speed $\sim10^{-50}c$ near the centre) and a strong-field ray deflection of $94.5$ versus the weak-field-extrapolated GR value $96$. All nine checks pass.

---

## 8. Discussion

The exponential metric is not new — it appears in Yilmaz's gravitation, in the polarizable-vacuum programme of Puthoff, and in the optical/analog-gravity literature — and it is well known to be GR-degenerate at post-Newtonian order while horizon-free in the strong field. What is new here is that it is *not assumed*: it is forced by the QCA model's independently derived dielectric gravity (Paper VII), in which mass is confined field-rotation energy and gravity is the renormalisation of the rotation rate. The model therefore inherits the exponential metric's horizon-free phenomenology as a prediction rather than a postulate, and — through the SI cell of Paper VII — promotes its dimensionless strong-field ratios to absolute angular and temporal observables. The price is honest and specific: the model trades the Hawking/area-law edifice for a unitarity-friendly frozen object and now owes a microphysical derivation of black-hole thermodynamics from lattice degrees of freedom. That derivation, an in-model computation of the GW-echo spectrum, and a dynamical-collapse search for a transient optical horizon are the natural next works.

---

## References

1. B. Ludwig, *Paper I — The BCC Quantum Cellular Automaton and the Speed of Light as a Rotation Rate* (this series).
2. B. Ludwig, *Paper VII — Gravity as a Lattice Dielectric* (this series).
3. H. Yilmaz, "New approach to general relativity," *Phys. Rev.* **111**, 1417 (1958).
4. H. E. Puthoff, "Polarizable-vacuum (PV) approach to general relativity," *Found. Phys.* **32**, 927 (2002).
5. M. Visser, "Heuristic approach to the Schwarzschild geometry," *Int. J. Mod. Phys. D* (2005) — exponential-metric discussion.
6. S. W. Hawking, "Particle creation by black holes," *Commun. Math. Phys.* **43**, 199 (1975).
7. Event Horizon Telescope Collaboration, "First M87 Event Horizon Telescope Results. I," *ApJL* **875**, L1 (2019).
8. Event Horizon Telescope Collaboration, "First Sagittarius A\* Event Horizon Telescope Results. I," *ApJL* **930**, L12 (2022).
9. GRAVITY Collaboration, "Mass distribution in the Galactic Center," *A&A* **657**, L12 (2022).
10. V. Cardoso & P. Pani, "Testing the nature of dark compact objects: gravitational-wave echoes," *Living Rev. Relativ.* **22**, 4 (2019).
11. W. G. Unruh, "Experimental black-hole evaporation?" *Phys. Rev. Lett.* **46**, 1351 (1981) — analog/optical horizons.

*Companion finding:* F114 (`findings/F114-dielectric-black-hole.md`); test `model-tests/test_F114_dielectric_black_hole.py`; scenario `scenarios/dielectric_black_hole.yaml`.
