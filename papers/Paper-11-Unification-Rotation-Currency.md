# Paper XI — One Currency: Mass, Energy, Light, and Gravity as a Single Rotation Rate

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Synthesis paper (XI), drawing together Paper I (light as a rotation rate), Paper II (the paired photon), Paper III (Higgs-free mass), and Paper VII (gravity as a lattice dielectric). It introduces no new construction; it shows that the four objects those papers treat separately are one object read four ways, and that this is what fixes the gravitational source.*

*Issued 2026-06-29 - 18:00.*

*Revision 2 (2026-07-01): re-issued as Paper XI (was Paper XII) following the deprecation of the horizon-free "dielectric black hole" paper (F114→F178) and the consequent renumbering of Papers IX–XIII down by one.*

*Revision 1 (2026-06-30): **gravity section re-issued per Findings F178–F183.** The canonical gravitational law is now the **induced Einstein equation** $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, sourced by the **full** stress-energy tensor. The single impedance-matched dielectric $K=e^{2u}$ — and with it the "couples to energy density $T^{00}$ only" reading — is reclassified as the **vacuum/weak-field (PPN-order) representation** of that law (F178). The "one currency" thesis is retained as the **origin story**: the rotation field's full stress-energy is what gravitates, and $E=mc^2$ is why mass cannot be a source distinct from that. Strong-field consequences — exact Schwarzschild/Kerr black holes (F183), the two-function GR/TOV interior (F181), pressure-weighted Friedmann cosmology (F182), and gravitational waves at $c_\text{grav}=c_\text{lat}=1/\sqrt3$ (F180) — are folded into §4 and §6. Canonical SI cell per Finding F107: $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.5978\,\ell_P=1.0664\times10^{-34}$ m.*

---

## Abstract

The BCC quantum-cellular-automaton model contains a single dynamical quantity: the angular rotation rate $\Omega$ of the real field pair $(\mathbf E,\mathbf B)$ per lattice tick. We show that the four things usually treated as distinct — rest mass, energy, light, and gravity — are four readings of that one quantity, and that recognising this fixes *what gravity is allowed to be sourced by*. The argument is built from results already verified elsewhere in the series: rest mass is the intercept $\Omega(0)=\arcsin m$ and the speed of light is the slope $d\Omega/d|\mathbf k|=1/\sqrt3$ of *one* generator (F26/F167); the photon is the massless, gapless ($\Omega(0)=0$) limit of that generator, gauge-protected by the $U(1)$ identity channel (F68/F69/F168); and gravity is an induced (Sakharov-type) renormalisation of $\Omega$, whose canonical law is the **induced Einstein equation** $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ sourced by the rotation field's **full stress-energy tensor** (F178). Because mass *is* confined rotation energy, there is no separate rest-mass density for gravity to couple to — the rest-mass-sourced alternative (F50/F52/F62) is excluded by the very fact that light gravitates, bends light, and bends by the Einstein factor 2 (F64). The familiar "couples to energy density $T^{00}$" dielectric $K(\mathbf x)$ (F64/F106) is the **vacuum/weak-field representation** of the full-tensor law — exact for lensing, PPN $\beta=\gamma=1$, redshift and the origin of $G$, but superseded inside matter and in the strong field, where the second metric function and the pressure ($3p$) source matter: the interior is GR/TOV (F181), cosmology is the pressure-weighted Friedmann pair (F182), black holes are exact Schwarzschild/Kerr (F183), and gravitational waves propagate at $c_\text{grav}=c_\text{lat}=1/\sqrt3$ (F180). The "one currency" reading survives as the *origin* of all this: $E=mc^2$ is why the rotation field's energy-momentum is the whole gravitational source, with nothing left over to reconcile.

---

## 1. The thesis

Unification in this model is not the merging of separate forces under a larger symmetry. It is the observation that the model only ever had one thing to begin with. Every dynamical statement in Papers I–X is a statement about the rotation of the real field pair $(\mathbf E,\mathbf B)$ through an angle $\Omega$ per tick. What look like four independent concepts are four questions asked of the single dispersion relation

$$
\Omega(\mathbf k, m)=\arccos\!\big(\sqrt{1-m^2}\;u(\mathbf k)\big),
\tag{1.1}
$$

where $u(\mathbf k)$ is the BCC pure-hop amplitude (F167, T5). The map is:

| Reading of $\Omega$ | Physical name | Where it lives in (1.1) |
|---|---|---|
| intercept $\Omega(0,m)=\arcsin m$ | **rest mass** | the $m$ term (zero-wavenumber eigen-rotation) |
| value of $\Omega$ at given $\mathbf k$ | **energy** | the whole function $E=(\hbar/\tau)\,\Omega$ |
| slope $d\Omega/d\lvert\mathbf k\rvert\to 1/\sqrt3$ | **speed of light** | the $m=0$, $\mathbf k\to0$ tangent |
| $\mathbf x$-dependence $\Omega\to\Omega/K(\mathbf x)$ | **gravity** | a position-dependent renormalisation of the rate (weak-field reading of the full-tensor law) |

This paper makes that table precise and draws the one non-obvious consequence: it fixes what gravity is allowed to be sourced by — the rotation field's full stress-energy tensor, of which the position-dependent rate $\Omega/K(\mathbf x)$ is the vacuum/weak-field representation.

---

## 2. Mass and energy are the same confined rotation (Papers I, III; F26, F167)

Paper III builds rest mass from the chiral-$SU(2)$ complex-mass step, and F167 closes the structural question the audit raised (G1): the mass term is *forced and unique* — among the sixteen Hermitian Dirac covariants exactly two are simultaneously chirality-off-diagonal and spin-rotation scalars, of which one is the physical mass and the other a pure-gauge phase. Unitarity then forces the kinetic rescale $n=\sqrt{1-m^2}$ ($n^2+m^2=1$, residual $2\times10^{-16}$), and the rest map's eigen-phase is

$$
\Omega_\text{rest}(m)=\arcsin m,\qquad \cos\Omega_\text{rest}=\sqrt{1-m^2}=n .
\tag{2.1}
$$

The same generator gives $d\Omega/d|\mathbf k|\to 1/\sqrt3=c_\text{lat}$ at $m=0$ (F26). Rest mass is the *intercept* and the speed of light is the *slope* of one function — verified together to $<10^{-12}$ (F167, T5). Restoring the lattice clock, $E=(\hbar/\tau)\,\Omega$, so

$$
E_0=\frac{\hbar}{\tau}\arcsin m\;\xrightarrow[m\ll1]{}\;\frac{\hbar}{\tau}\,m,\qquad m_\text{phys}=E_0/c^2 .
\tag{2.2}
$$

The conclusion is the linchpin of the whole synthesis: **there is no "mass substance" distinct from energy.** A massive particle at rest is rotation energy that has been confined ($\Omega(0)\ne0$); a particle in motion carries more of the same rotation. $E=mc^2$ is not a bridge between two categories — it is the single statement that energy and confined rotation are the same thing, read once as a rate and once as an intercept.

---

## 3. The photon is the gapless limit of the same generator (Papers I, II, IV; F68, F69, F168)

A photon is what (1.1) becomes when there is no confinement: $m=0$, so the intercept vanishes and the *only* energy available is the propagating slope term,

$$
\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2),\qquad
\Omega_\text{pair}(0)=0,\qquad \frac{\Omega_\text{pair}}{|\mathbf k|}\to\frac1{\sqrt3}.
\tag{3.1}
$$

Three structural facts (F168) make this the *forced* form, not an assumption:

1. **Masslessness is the absence of a self-loop.** The BCC walk is a pure body-diagonal hop with no on-site term ($A_0=0$), so $u(0)=1$ and $\omega^{\pm}(0)=\arccos 1=0$. An on-site deficit $\varepsilon$ would open a gap $\omega(0)\approx\sqrt{2\varepsilon}$; the photon has none (F168, B1).
2. **The binder is the conserved vector current.** $\omega^-(\mathbf k)=\omega^+(-\mathbf k)$ exactly (residual $0$), so the symmetric pair is the parity-even $U(1)$ identity channel that minimal coupling forces (F68); the single-branch alternative is the chiral, birefringent object excluded by GRB/AGN polarimetry (F67).
3. **Zero binding energy is gauge-protected, not tuned.** Mass lives entirely in the branch-coupling vertex $X$ (gap $=m$, F168 B4); the photon's identity-channel coupling has $X\equiv0$, so it cannot generate a mass term and $\Omega(0)=0$ is forced. This is Weinberg's massless-spin-1 theorem realised on the lattice, and the sharp contrast with the scalar sibling (F73/F74), whose gap is *un*protected and needs fine-tuning.

So the photon carries energy with zero mass and zero charge for one reason: it is the parity-even identity channel of a pure-hop walk. Pure hop ⇒ no mass intercept; identity channel ⇒ no charge, no mass term. The only thing it can carry is the moving rotation, $E=c\lvert\mathbf k\rvert\,\hbar/\tau$ — the model's reading of $E=pc$. For a photon, "to exist" and "to move" are the same statement.

---

## 4. Gravity renormalises the one rate, and the full stress-energy is its source (Paper VII; F178, F64, F106)

If mass, energy and light are all the rotation $\Omega$, then a theory of gravity in this model has exactly one thing to act on: the value of $\Omega$ as a function of position and time. Whatever object carries the rotation also carries its energy, momentum, and stress — and because mass *is* confined rotation energy (Section 2), there is no separate rest-mass substance hiding behind it. So the gravitational source is the rotation field's own **stress-energy tensor**, in full. The canonical law of the model is the **induced Einstein equation** (F178)

$$
G_{\mu\nu} = \frac{8\pi G}{c^4}\,T_{\mu\nu},\qquad
G=\frac{a^2c^3}{8\pi\sqrt3\,\hbar}\ \ (\text{structural, F79/F107}),
\tag{4.1}
$$

with no free coupling: $G$ collapses to pure lattice quantities. This is gravity as an emergent, induced (Sakharov-type) renormalisation of the rotation substrate, whose low-energy dynamics are exactly Einstein's. The unification still *fixes the source* — it just fixes it to the whole tensor, not to one component.

**The rest-mass route is what gets excluded.** The fact that prompted the older "couples to energy" reading — that massless photons feel and bend in gravity — is exactly what kills a rest-mass-density source. The model once offered two gravities:

| Route | Source | Light bending | Light bends light? |
|---|---|---|---|
| Rest-leg (F50/F52/F62, superseded) | rest-mass density $\rho$ | factor-1 (Newton); $0$ for pure light | **no** |
| Energy/full-tensor (F64→F178, canonical) | stress-energy $T_{\mu\nu}$ | **factor-2 (Einstein)** | **yes** |

Equal-energy rest-mass and massless-field sources bend probe rays equally (ratio $1.00002$, F64 D-EM3), and a Maxwell pulse bends through a well sourced by a *massless* energy lump at full factor-2 (F64 D-EM6). Observation says light gravitates and bends by factor 2 — so the rotation field's energy-momentum, not any rest-mass density, is the source. $E=mc^2$ is why this is consistent: "the full stress-energy gravitates" already contains mass, with nothing left to reconcile.

### 4.1 The dielectric is the vacuum/weak-field representation (F64, F106)

In the regime where $T_{\mu\nu}\to0$ (vacuum) or $p\ll\rho c^2$ (Newtonian), the full-tensor law (4.1) reduces to a single impedance-matched index $K(\mathbf x)$ renormalising the $(\mathbf E,\mathbf B)$ rotation rule — the dielectric of Paper VII, with metric legs $A=1/K$, $B=K$ and the reciprocal lock $AB\equiv1$. Its static sourcing law (F106),

$$
\nabla^2\ln K(\mathbf x) = -\frac{8\pi G}{c^4}\,T^{00}[\psi]
= -\frac{a^2\,c_\text{lat}}{\hbar c}\,T^{00}[\psi],
\tag{4.2}
$$

is exactly the **static weak-field reduction** of (4.1) — F106 derived it as precisely that. A rest eigenstate hands the source $\sqrt A\,m\,|\Psi|^2\to m|\Psi|^2$ — energy, not bare probability (F106, E5). What makes one scalar reproduce GR's PPN phenomenology — factor-1 redshift *and* factor-2 bending together — is the impedance-matched placement $\varepsilon=\mu=K$: the lock $AB\equiv1$ keeps $\sqrt{\mu/\varepsilon}=1$ exactly $u$-independent, so the rotation stays a *proper* rotation with no scalar contamination (F64 D-EM5). The result is GR-identical at the post-Newtonian level: $\beta=\gamma=1$, Mercury $42.98''$/century, Shapiro delay (F64 D-EM9).

### 4.2 Where one scalar is not enough (F173, F178, F181)

A single impedance-locked scalar cannot be the *exact* field equation, because $A=1/K,\ B=K$ is one function where Einstein's equations need two. The exact Einstein tensor of the dielectric metric carries an irreducible *anisotropic* field stress $p_r=-p_t=-e^{-2u}u'^2/8\pi$ and no isotropic matter-pressure term (F173, sympy-exact) — so it omits GR's Tolman $3p$ source. This is null in the solar system ($\sim10^{-11}$) but $O(3p/\rho c^2)$ — a few to tens of percent — inside neutron stars, and a clean factor of 2 in the radiation era. The full-tensor law (4.1) has no such gap: inside matter the metric carries its **second independent function** ($A,B$ free, $AB\neq1$) and the dynamics are GR/TOV. The covariant two-function interior kernel (F181) solves the isotropic perfect-fluid Einstein equations exactly where the single scalar forces $p_r=-p_t$, reproducing GR-TOV to the integrator floor, and the F62/F64 dynamic Dirac battery — equivalence principle, redshift $\propto\sqrt{-g_{tt}}$, factor-2 deflection, unitary backreaction — passes unchanged on the two-function background. Nothing in the weak-field phenomenology is lost; only the *exact* strong-field content changes.

### 4.3 The same light cone for gravity and light (F180)

The causal completion of (4.2) is the hyperbolic wave equation $\big(\nabla^2-c_\text{lat}^{-2}\partial_t^2\big)\ln K=-(8\pi G/c^4)T^{00}$ (F180, D-GW). Its speed is not chosen: the dielectric has zero tree stiffness (its conformal factor has no bare kinetic term, F79), so the graviton's inverse propagator *is* the induced vacuum polarisation of the lattice's own rotation modes, and that loop can carry only the constituent light cone $c_\text{lat}=1/\sqrt3$. Gravitational waves and photons therefore solve the *same* operator $\Box_\text{lat}$ — $c_\text{grav}=c_\text{lat}=c_\text{photon}$ is one symbol, not two numbers tuned to agree. The GW170817 residual is bounded at $\sim3\times10^{-83}$, 68 orders below the observed limit. This is the rotation-currency thesis at its sharpest: light and gravity share a light cone because they share the rotation rule.

---

## 5. The closed chain

The unification is a single implication chain, each link verified in the cited finding:

$$
\underbrace{\text{mass}=\text{confined }(\mathbf E,\mathbf B)\text{ rotation}}_{\text{F26/F167}}
\;\Rightarrow\;
\underbrace{\text{the gravitational source is the rotation field's full }T_{\mu\nu}}_{\text{F178}}
\;\Rightarrow\;
$$
$$
\underbrace{\text{it gravitates light per unit energy as mass, bends it by factor 2}}_{\text{F64 D-EM3/D-EM6}}
\;\Rightarrow\;
\underbrace{\text{the law is the induced Einstein equation }G_{\mu\nu}=\tfrac{8\pi G}{c^4}T_{\mu\nu}}_{\text{F178/F181}}
\;\Rightarrow\;
\underbrace{c_\text{grav}=c_\text{lat}}_{\text{F180}} .
$$

In the vacuum/weak field this collapses to the impedance-matched dielectric — one scalar that keeps the rotation proper while reproducing GR's PPN tests (F64 D-EM5). $E=mc^2$ is the hinge that makes the rotation field's energy-momentum the *whole* source, with no rest-mass density to add. Mass, energy, light and gravity are not unified by adding structure; they were one rotation all along, and gravity is simply that rotation's full stress-energy made to curve its own substrate.

---

## 6. What this is, and what remains open

This synthesis is a re-reading, not a new result: every equation and number above is quoted from a verified finding (Section 7). Its claim to content is (i) the recognition that the four concepts share one generator, and (ii) the demonstration that gravity's source is *forced* — to the rotation field's full stress-energy — by mass–energy equivalence together with the empirical gravitation of light.

The model is GR-identical at the PPN level ($\beta=\gamma=1$, Mercury $42.98''$/century, factor-2 bending; Paper VII, F64 D-EM9), and under the full-tensor source (F178) its low-energy dynamics are exactly Einstein's: the canonical black hole is exact Schwarzschild/Kerr — horizon present, GR shadow $3\sqrt3\,M$, Hawking radiation, photon-sphere ringdown — with one genuinely new feature, a lattice-regulated core (curvature saturating at the cell scale, $r_\text{core}\sim(r_g^2a^4)^{1/6}\propto M^{1/3}$) replacing the point singularity (F183). This **supersedes** the horizon-free "dielectric black hole" (deprecated, F114), now understood as a PPN-order representation artifact; the ngEHT $+4.6\%$ shadow target is withdrawn. Cosmology is the standard pressure-weighted Friedmann pair, $\ddot a/a=-(4\pi G/3)(\rho+3p/c^2)$ (F182); the demoted energy-only law would have mis-weighted the radiation era by exactly a factor 2.

The model's distinctive gravitational content therefore narrows, deliberately, from "novel strong-field phenomenology" to **the origin and value of $G$** — gravity as an induced renormalisation of the rotation substrate — plus the shared light cone $c_\text{grav}=c_\text{lat}$ (F180). The honest open edges: the Kerr/frame-dragging interior ($T_{0i}$) on the two-function kernel and a tabulated-EoS TOV for an absolute neutron-star placement (F181); the interacting two-body photon wavefunction — F168 proves *why* the bound pair sits at zero binding energy, but the first-principles Bethe–Salpeter build is unfinished; and the overall mass *scale* (F119 no-go), where the spectrum's shape is locked but its single normalisation needs an external anchor or a dynamical condensate.

---

## 7. Findings and modules cited

| Result used | Finding | Module |
|---|---|---|
| $c_\text{lat}=d\Omega/d\lvert\mathbf k\rvert=1/\sqrt3$ (rotation-rate slope) | F26 | `ca-simulation/ca_bcc.py` |
| Rest mass $=\arcsin m$ = intercept of the same generator; mass forced & unique | F167 | `ca_bcc.py`, `ca_dirac.py` |
| Paired-spinor photon: massless, luminal, non-birefringent | F69 | `ca-simulation/ca_photon_pair.py` |
| $U(1)$ identity channel forces the even (non-birefringent) photon | F68 | `ca-simulation/ca_wmu.py` |
| Photon binding gauge-protected ($\Omega(0)=0$ forced, $A_0=0$ pure hop) | F168 | (analytical; `ca_bcc` walk) |
| **Canonical law: induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$; dielectric demoted to vacuum/weak-field representation** | **F178** | `ca-simulation/ca_gravity.py`, `ca_stellar.py` |
| Dielectric gravity $K=e^{2GM/rc^2}$, $AB\equiv1$ (weak-field rep); radiation gravitates as mass; light bends light | F64 | `ca-simulation/forks/gr_fork_F64_em_connection.py` |
| $\psi\to K$ sourcing law $\nabla^2\ln K=-(a^2c_\text{lat}/\hbar c)T^{00}$ (no free $G$); static weak-field reduction of F178 | F106 | `tests/findings/test_F106_psi_K_sourcing.py` |
| Single scalar omits the Tolman $3p$ source ($p_r=-p_t$); null in solar system, $O(3p/\rho c^2)$ in neutron stars | F173 | `ca-simulation/ca_tolman.py` |
| Covariant two-function GR/TOV interior ($A,B$ free, $AB\neq1$); F62/F64 dynamic battery unchanged | F181 | `ca-simulation/ca_interior_metric.py` |
| Pressure-weighted Friedmann cosmology $\ddot a/a=-(4\pi G/3)(\rho+3p/c^2)$; energy-only law off by factor 2 in radiation era | F182 | `ca-simulation/ca_cosmology.py` |
| Gravitational-wave equation; $c_\text{grav}=c_\text{lat}=1/\sqrt3$ (GW170817 margin $\sim10^{-83}$) | F180 | `ca-simulation/forks/gr_fork_F180_gw_speed.py` |
| Strong field: exact Schwarzschild/Kerr (horizon, shadow $3\sqrt3 M$, Hawking, ringdown) + lattice-regulated core | F183 | `ca-simulation/ca_blackhole.py` |
| Canonical SI cell $a=\sqrt{8\pi}\,3^{1/4}\ell_P=6.5978\,\ell_P$; structural $G$ | F107 | — |
| Horizon-free dielectric black hole (**superseded by F183**) | F114 | — |

External lineage: Puthoff polarizable-vacuum and Ostoma–Trushyk dielectric-vacuum programmes (the energy-coupled-index line, now understood as the vacuum/weak-field representation of induced Einstein gravity); see `references/ostoma-trushyk-1999-summary.md`.

---

*End of Paper XI.*
