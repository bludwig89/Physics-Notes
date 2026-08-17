# Gravity-sector scenario catalog (post-F178 full-tensor adoption)

**Date:** 2026-06-30 - 03:30
**Context:** After [[F178-gravity-full-tensor-adoption]] the canonical gravitational law is the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$; the single-scalar dielectric $K=e^{2u}$ is the vacuum/weak-field representation. The first follow-ups are built: covariant two-function interior kernel (F181), full-tensor Friedmann cosmology (F182), and the canonical Schwarzschild/Kerr black hole (F183). This catalog maps what gravity–mass scenarios can now be built, the predictions at each stage, and two questions raised in review: **(A) where the dielectric must expand to the full tensor**, and **(B) whether the vacuum dielectric connects to dark matter**.

---

## 1. The regime ladder — gravity–mass interaction at each stage

Gravity–mass coupling is best organised by two dimensionless knobs: the compactness $u=GM/rc^2$ (how strong the field is) and the stiffness $w=p/\rho c^2$ (how much the matter's pressure gravitates). Each rung names the correct description, the model's prediction, and the build status.

| Stage | Regime ($u$, $w$) | Correct description | Model prediction | Status |
|---|---|---|---|---|
| **1. Test-particle / solar system** | $u\lesssim10^{-6}$, $w\approx0$ | dielectric = full tensor (agree) | $\beta=\gamma=1$, light bending $4GM/bc^2$, Mercury $42.98''$/cy, Shapiro, redshift; structural $G$ | built (F64/F79/F107) |
| **2. Compact-star interior** | $u\sim0.1$–$0.3$, $w\sim0.1$–$0.3$ | **full tensor** (two functions) | GR/TOV: maximum mass, mass–radius, surface redshift; pressure gravitates ($+3p$) | built (F176/F181) |
| **3. Strong-field exterior / horizon** | $u\sim0.3$–$0.5$, vacuum | **full tensor** (exact Schwarzschild/Kerr) | horizon $2M$; shadow $3\sqrt3\,M$; ISCO $6M$; Hawking $T\propto M^{-1}$; QNM ringdown | built (F183) |
| **4. Rotating compact object** | any $u$, with spin $a$ | **full tensor** (off-diagonal $g_{t\phi}$) | Kerr: ergosphere, frame-drag $\Omega_H$, prograde/retrograde ISCO, spin-dependent shadow | built (F183, exterior); interior kernel open |
| **5. Gravitational collapse** | time-dependent, $u\to0.5$ | **full tensor** (dynamical) | Oppenheimer–Snyder horizon formation in finite proper time; settles to Kerr | built (F183, OS); live collapse open |
| **6. Gravitational waves** | dynamical vacuum | **full tensor** (spin-2) | $c_{\rm grav}=c_{\rm lat}=1/\sqrt3=c_{\rm photon}$ (GW170817) | built (F180) |
| **7. Cosmology (radiation era)** | homogeneous, $w=1/3$ | **full tensor** (Friedmann pair) | $\ddot a/a=-(4\pi G/3)(\rho+3p)$; $a\propto t^{1/2}$; pressure gravitates | built (F182) |
| **8. Sub-horizon BH core** | $u\to\infty$ at $r\to0$ | **full tensor + lattice cutoff** | curvature regulated at the cell scale $a$: $r_{\rm core}=(48 r_g^2 a^4)^{1/6}\propto M^{1/3}$ — no point singularity | built (F183, static estimate); dynamical open |

**The throughline:** in every stage where pressure, strong curvature, momentum flux, rotation, or time-dependence matters, the description is exactly GR — the model's distinctive content is the *origin and value of $G$* (induced/Sakharov, $G=a^2c^3/8\pi\sqrt3\,\hbar$) and the rotation-rate substrate, not new strong-field phenomenology. The one substrate-level departure is the lattice-regulated core (stage 8).

---

## 2. (A) Where does the vacuum dielectric expand to the full tensor system?

The dielectric $K=e^{2u}$ ($A=1/K,\ B=K,\ AB\equiv1$) is the representation of $G_{\mu\nu}=8\pi G T_{\mu\nu}$ that is valid only when **all three** conditions hold; it must be replaced by the full two-function (or full ten-component) tensor whenever **any** fails:

| Condition for the dielectric | Quantitative boundary | What forces the full tensor when it fails |
|---|---|---|
| **(i) Pressure negligible**, $p\ll\rho c^2$ | omitted source fraction $3w/(1+3w)$ | matter interiors & radiation era: $w{=}0.1\Rightarrow23\%$, $w{=}0.3\Rightarrow47\%$, $w{=}\tfrac13\Rightarrow50\%$ (F173/F181/F182). Crossover: $w\gtrsim10^{-2}$ |
| **(ii) Weak field**, $u\ll1$ | metric error $\sim u^2/2$ | $u{=}0.1$ ($r{\approx}10\,GM/c^2$) $\Rightarrow0.5\%$; photon sphere $u{=}\tfrac13\Rightarrow5.6\%$; horizon $u{=}\tfrac12\Rightarrow12.5\%$. The exponential keeps $\beta{=}\gamma{=}1$ so PPN survives further, but the **metric components and the horizon structure** diverge for $u\gtrsim0.1$ (F183) |
| **(iii) Static & isotropic**, $T_{0i}{=}0$, $p_r{=}p_t$ | frame-drag $\sim a/r^3$; $\dot T\neq0$ | any rotation needs off-diagonal $g_{t\phi}$ (Kerr) — the scalar has no slot (F183 K1); any time-dependence needs the spin-2 wave equation (F180); the impedance lock forces anisotropic $p_r=-p_t$, wrong for a perfect fluid (F173) |

**One-line answer.** The dielectric is the correct description for $u\lesssim0.01$ **and** $p\ll\rho c^2$ **and** static-non-rotating geometry — i.e. the weak-field vacuum exterior of slowly-moving, nearly-pressureless sources (the solar system, weak lensing, galactic-scale potentials). It must expand to the full tensor at the compact-star interior ($p$ matters), the strong-field/horizon region ($u\gtrsim0.1$), any rotating or time-dependent or anisotropic configuration, and the radiation-dominated universe. The expansion is not a sharp switch but a graded one: the leading correction is $O(u^2)$ in the field and $O(3p/\rho c^2)$ in the source, both computed above.

---

## 3. Buildable scenarios (catalog)

Concrete simulations that the new sector supports. Modules in `ca-simulation/`; CASIM scenarios in `scenarios/`.

**Built this session**
- `ca_interior_metric.py` — two-function TOV interior + Schwarzschild exterior (F181).
- `ca_cosmology.py` — Friedmann pair, radiation/matter eras, energy-only mis-weighting (F182).
- `ca_blackhole.py` — Schwarzschild/Kerr observables, OS collapse, lattice core, F114 contrast (F183).

**Ready to build (high value, mechanical) — ALL BUILT 2026-06-30**
1. **Tabulated-EoS neutron stars** — `ca_ns_eos.py`, **F184** ✅: SLy/APR/MPA1 piecewise polytropes on the F181 TOV kernel; SLy $M_{\max}=2.08\,M_\odot$, $R(1.4)=11.1$ km, consistent with PSR J0740/NICER; no $AB\equiv1$ residual.
2. **Rotation: frame dragging & moment of inertia** — `ca_rotation.py`, **F185** ✅: Hartle slow-rotation $\omega(r)$, $I/MR^2=0.31$, $I\approx0.6\times10^{45}$ g cm². *(Full Kerr-interior/live collapse still open; the exterior Kerr + OS collapse are in F183.)*
3. **Black-hole shadow renderer** — `ca_raytrace.py`, **F186** ✅: geodesic $b_c=3\sqrt3\,M$; M87\* 39.7 μas, Sgr A\* 53.3 μas (GR); **F114 +4.63% withdrawn**; spin–shadow asymmetry.
4. **Ringdown spectrum** — `ca_qnm.py`, **F187** ✅: WKB QNMs reproduce GR fundamentals to $<7\%$; lattice-core echoes exponentially suppressed (vs F114's order-one).
5. **Multi-component cosmology** — `ca_cosmology.py`, **F188** ✅: $z_{\rm eq}=3430$, $z_{\rm acc}=0.63$, age $13.8$ Gyr — standard $\Lambda$CDM.
6. **Binary inspiral / GW phasing** — `ca_inspiral.py`, **F189** ✅: GW150914 chirp mass $28.1\,M_\odot$, ISCO 67.6 Hz, ~0.19 s; graviton speed $c_{\rm lat}$ (F180).

**Speculative / ambitious — BUILT at scoped depth 2026-06-30**
7. **Lattice-core microstate counting** → $S=A/4$ — `ca_horizon_entropy.py`, **F190** ✅ (scoped): area law exact; $S=A/4$ reproduced iff each F107 cell carries $2\pi\sqrt3$ nats (the open derivation target).
8. **Dark-matter scenario** — `ca_darkmatter.py`, **F191** ✅ (assessment): rotation curves cannot separate halo from modified gravity; the Bullet-Cluster lensing offset favours a dark *source* over a dielectric reweighting. See §4.
9. **Cosmological-constant** — `ca_vacuum_energy.py`, **F192** ✅ (open): full-tensor fixes the dark-energy *sign* ($w=-1\Rightarrow\rho+3p=-2\rho$ accelerates); the $\sim10^{121}$ *magnitude* (F164) stays open.

---

## 4. (B) Does the vacuum dielectric connect to "dark matter"?

This is an open research question; the honest assessment has two parts.

**The conservative answer: under exact GR, the dielectric does not substitute for dark matter.** F178 committed the model to $G_{\mu\nu}=8\pi G T_{\mu\nu}$ with the *full, standard* source and a *constant* $G$. That is ordinary general relativity at galactic scales, which does **not** produce flat rotation curves from visible matter alone. So a vacuum dielectric that merely re-weights the potential of visible mass (a MOND-like reading of $K(x)$) is disfavoured by the same evidence that disfavours modified gravity generally — most sharply the **Bullet Cluster** (the gravitational-lensing mass is offset from the gas, i.e. from the dominant baryons) and the **CMB acoustic peaks / structure growth** (which need a collisionless, non-baryonic clustering component). A pure-dielectric "no new matter" route fails these.

**The constructive answer: the model has a natural dark-matter *source*, and it lives in the same vacuum/condensate sector that the dielectric responds to.** The dielectric $K$ is sourced by energy density (F106); anything that carries energy density but does **not** couple to photons will (i) gravitate / dig a dielectric well and (ii) be electromagnetically invisible — which *is* the operational definition of dark matter. Candidates native to this model:

- **A gravitating, dark lattice condensate / vacuum component.** The BCC zero-point sector already carries a huge energy density (F164). If a *clustering, collisionless* fraction of it (a CA-native condensate, e.g. the leading 't Hooft-vacuum or marginal-binding channel of F164/F69) tracks structure, it behaves exactly like cold dark matter: it sources $T_{\mu\nu}$ (hence $K$ and the full metric), lenses, and is dark. This connects DM and the cosmological-constant problem to **one** vacuum-energy sector — an attractive unification, but it must be shown to (a) cluster into NFW-like halos and (b) pass the Bullet Cluster / CMB tests, neither of which is done.
- **A sterile / right-handed neutrino-like excitation.** Ludwig's SU(2) derivation leaves right-handed singlet slots; a stable heavy singlet is the standard particle-DM candidate and needs no dielectric story.

**Where the dielectric *could* genuinely matter (the speculative-but-principled route): induced/running $G$.** Because $G$ is **induced** (Sakharov; $G=a^2c^3/8\pi\sqrt3\,\hbar$, Paper VII §5), it is in principle scale/curvature-dependent. An IR enhancement of the induced coupling at the very low curvatures of galactic outskirts is the model-native version of emergent-gravity DM proposals (Verlinde-type). This is the one way the *gravity sector itself* (not a new matter species) could mimic DM. It is ambitious, not built, and faces the same Bullet-Cluster hurdle — but it is falsifiable and sits naturally on the induced-$G$ result.

**Verdict.** The vacuum dielectric as a *re-weighting of visible matter* is **not** a dark-matter substitute under F178's exact-GR commitment. But the dielectric's **source** — a gravitating-yet-dark vacuum/condensate component — is a legitimate dark-matter candidate that would unify DM with the F164 vacuum-energy sector, and an IR-running of the induced $G$ is a second, gravity-side candidate. Both are buildable scenarios (§3 item 8); both must be confronted with rotation curves **and** the Bullet Cluster **and** the CMB before any claim. Recommended first step: a galactic-halo run sourcing $K$ from a collisionless dark condensate and checking the rotation-curve shape, then the Bullet-Cluster lensing/gas offset as the make-or-break test.

---

## Files referenced
- Findings: F178 (decision), F181 (interior kernel), F182 (cosmology), F183 (black hole), F180 (GW speed), F173 (pressure discriminator), F164 (cosmological constant), F114 (superseded dielectric BH), F79/F107 (structural $G$ / canonical cell).
- Modules: `ca_interior_metric.py`, `ca_cosmology.py`, `ca_blackhole.py`, `ca_gravity.py`, `ca_stellar.py`.
- Paper: `papers/Paper-07-Gravity.md` (§4 re-issued).
