# Chapter 19 — Strong-field and wave gravity

*Chapter 19 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F111-second-order-light-deflection.md`, `findings/F174-stellar-structure-overlay.md`,
`findings/F176b-covariant-dielectric-tov-recovery.md`, `findings/F180-gravitational-wave-speed.md`,
`findings/F181-covariant-interior-kernel-battery.md`, `findings/F183-blackhole-under-full-tensor.md`,
`findings/F184-tabulated-eos-neutron-stars.md`, `findings/F185-slow-rotation-moment-of-inertia.md`,
`findings/F186-shadow-raytracer-microarcsec.md`, `findings/F187-qnm-ringdown-spectrum.md`,
`findings/F189-pn-binary-inspiral.md`, `findings/F204-alcubierre-warp-structural-exclusion.md`,
`findings/F248-tt-graviton-bcc-explicit.md`, `findings/F354-lattice-core-geodesic-completeness.md`,
`findings/F356-multi-eos-nicer-robustness.md`, `findings/F357-graviton-photon-band-top-uv-scale.md`,
and `findings/F359-graviton-collapse-threshold.md` (the seventeen findings `00-plan.md` §2 assigns to
this chapter, all read in full), against `docs/monograph/18-gravity.md` (R18.1–R18.17, read in full —
the direct prerequisite), `docs/theory/supersessions.yaml` (record **S4-F178-full-stress-energy**,
re-checked specifically for F111 and F181, neither of which appears in its `superseded:` or
`reclassified:` lists — see §19.2.9 and §19.2.12 below for what that means for each), and
`claims-index.md` (CL008/CL015/CL023–CL027 inherited from Chapter 18; CL009/CL013 for F180;
CL154/CL157/CL162/CL163 for F174/F176b/F181/F184/F356 and F185; CL178 for F204; CL219 for F248;
CL295 for F354; CL297/CL298 for F357/F359; CL027 and CL160 specifically cross-checked against their
own source findings' headers, not taken at face value — see §19.2.1 and §19.2.9). Notation is that of
Chapters 1, 6, 11 and 18 — $c_\text{lat}$, $\Omega(\mathbf k)$, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$,
$K=e^{2GM/rc^2}$, the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ — extended, never
redefined.

## 19.0 What this chapter establishes, up front

**Chapter 18 adopted the induced Einstein equation, sourced by the full stress-energy tensor, as the
canonical gravitational law (F178, R18.11/R18.13), and demoted the single impedance-locked dielectric
$K=e^{2GM/rc^2}$ to a vacuum/weak-field representation valid only where $T_{\mu\nu}\to0$ or
$p\ll\rho c^2$.** This chapter works out what that hierarchy means once gravity is no longer weak.
The answer, findings F111–F359 make precise and quantitative: **in the strong-field and wave regimes,
this model's gravity sector is general relativity**, to the precision every finding here tests. Black
holes are exact Schwarzschild/Kerr, with a genuine horizon, the GR photon-sphere shadow
$b_c=3\sqrt3\,M$, Hawking radiation, and GR quasinormal-mode ringdown (F183, F186, F187). Neutron-star
interiors, once the full tensor is carried rather than the single scalar, are genuine TOV stars on
realistic equations of state, consistent with PSR J0740+6620 and current NICER radii (F181, F184,
F356). Gravitational waves propagate at exactly the photon speed $c_\text{lat}=1/\sqrt3$, carried by
an explicit transverse-traceless graviton with two non-birefringent helicities (F180, F248), and a
compact-binary inspiral–ringdown waveform reproduces GW150914's chirp mass and merger frequency
(F189, F187). **This is a consistency result, not a new-physics result**: the chapter's own headline
finding, F183, states its trade plainly — "the model surrenders the dielectric's distinctive
strong-field phenomenology (horizon-free shadow, no Hawking, echoes) and adopts the full GR black
hole — which is what every current observation... actually supports." The one place the model adds
genuine new content beyond textbook GR is the substrate itself: curvature saturates at the lattice
cell scale rather than diverging, and — a result this chapter's own attack pass narrowed rather than
inflated — the bounded curvature alone forces a $C^{1,1}$ regular centre with no parity assumption
needed (F354). Two items withdrawn along the way, precisely stated: F111's $4\pi$ second-order
light-bending coefficient (the model's exponential $K$ was never the *exact* vacuum solution, so its
second-order departure from GR was never a real prediction) and F204's structural exclusion of
faster-than-light Alcubierre warp drives (excluded *more* completely here than in standard GR+QFT).

## 19.1 Inputs

**Postulates used.** No new postulates. P1–P4 (discreteness, locality, homogeneity/isotropy,
linearity/unitarity) continue to underlie every dispersion relation and Brillouin-zone argument this
chapter cites from Chapters 6 and 18. P5/P6 (mass as confined rotation, the rest-leg mechanism) enter
only through Chapter 18's already-derived $G$ and dielectric; this chapter introduces no new use of
them. P7 (elegant design, Chapter 1's Gap [G-1]) is invoked implicitly wherever a finding treats "the
model reduces exactly to GR" as itself a satisfying outcome rather than a disappointment — a framing
choice, not a new derivation, and this chapter does not add to Gap [G-1]'s open status.

**Prior results used, precisely.**

- **R18.9** ($G=a^2c^3/(8\pi\sqrt3\hbar)$, F79) supplies the one physical constant every mass/length
  scale in this chapter is quoted in (Schwarzschild radii, Hawking temperatures, ISCO frequencies).
- **R18.10** (F64's dielectric, D-EM1/D-EM5/D-EM9: $\beta=\gamma=1$, the impedance lock $AB\equiv1$)
  is the vacuum/weak-field object this chapter's exact results (Schwarzschild, the two-function
  interior) *supersede in the strong field while agreeing with at PPN order* — the precise sense in
  which nothing here contradicts Chapter 18, it completes it.
- **R18.11–R18.13** (F178's three-part decision: the induced Einstein equation is canonical; the
  interior is genuine GR/TOV; the exact vacuum solution is Schwarzschild, not the exponential $K$) is
  the load-bearing prior result for this entire chapter — every finding below either builds the
  Schwarzschild/Kerr/TOV consequences of R18.13 directly (F183, F181, F184–F186) or checks that the
  *wave* sector inherits the same full-tensor law consistently (F180, F248, F189, F187).
  R18.13's own text forward-cites this chapter explicitly: "The exact Schwarzschild/Kerr treatment
  that replaces F114 is Chapter 19's, forward-cited here rather than performed" (`18-gravity.md` §18.5).
- **R18.14/R18.15** (F345/F383: the two-derivative field equation is forced at the model's own derived
  $d=4$; the four-derivative term is generated, not forbidden, by locality) bound how far any
  strong-field departure from GR could even be expected to reach — this chapter's own results (the
  lattice-core corrections) are consistent with, and this chapter does not revisit, that order-of-
  magnitude ceiling.
- **R18.16** (F63: Einstein–Cartan torsion $\lesssim0.3\%$ at test densities) is cited once, in §19.6,
  as the reason this chapter's torsion-free black-hole and neutron-star solutions are not begging a
  question Chapter 18 already screened.

**Free inputs consumed.** None new beyond Chapter 18's own accounting (its §18.1 items 1–3, carried
unchanged). What this chapter *does* consume, and states plainly rather than silently: **external
astrophysical data used as comparison targets, not as fitted inputs** — PSR J0740+6620's mass and
NICER radius (Fonseca et al. 2021; Dittmann et al. 2024), PSR J0437−4715 (Choudhury et al. 2024),
GW150914's component masses (Abbott et al. 2016), and the EHT M87\*/Sgr A\* ring measurements
(EHT 2019/2022) — exactly the same status Chapter 18 gave Mercury's perihelion advance: the model's
own $G$ and field equation are parameter-free, and these numbers are what the resulting predictions
are checked against, not tuned to. Piecewise-polytrope equation-of-state digits (Read, Lackey, Owen &
Friedman 2009: SLy, AP4, MPA1, WFF1, MS1) are external nuclear-physics inputs in exactly the sense
Chapter 14's hadron sector consumes external QCD phenomenology — not derived here, and not claimed to
be.

## 19.2 The derivation

### 19.2.1 F183 — the black hole under the full tensor: exact Schwarzschild/Kerr, with one new feature

F183 (2026-06-30) is this chapter's central act: it builds the object R18.13 promised. Under the
canonical law $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, the exact vacuum black hole is **Schwarzschild**
(Kerr with spin) — with a genuine event horizon — replacing F114's horizon-free dielectric object,
now understood (§18.5, R18.13) as an artifact of treating the PPN-order representation $K=e^{2u}$ as
if it were the exact vacuum solution.

Eight checks (8/8 PASS) establish the closed-form content: the standard Schwarzschild invariants
(horizon $2M$, photon sphere $3M$, shadow $b_c=3\sqrt3\,M=5.196M$, ISCO $6M$, surface gravity
$\kappa=1/4M$), cross-checked against a numeric photon-sphere/critical-impact-parameter solve to
$<10^{-3}$ (S1); a genuine **Hawking sector**, present for the first time in this model's gravity
tree — $T_H=\hbar c^3/(8\pi Gk_BM)=6.17\times10^{-8}$ K at $1\,M_\odot$, lifetime
$2.10\times10^{67}$ yr, $T\propto M^{-1}$, lifetime $\propto M^3$ (S2); an eikonal ringdown tied
exactly to the photon sphere, $\Omega_c=\lambda=1/(3\sqrt3\,M)$, converging to the tabulated GR
fundamental mode from $28.8\%$ error at $\ell=2$ to $3.2\%$ at $\ell=6$ (Q1); the full Kerr closed
forms at $a=0.9M$ — horizons, ergosphere, frame-drag $\Omega_H$, prograde/retrograde ISCO — reducing
to Schwarzschild as $a\to0$ (K1); the Bardeen Kerr shadow, correctly flattened and displaced on the
prograde side at high spin (K2); and an Oppenheimer–Snyder dust collapse that forms a horizon and
reaches $R=0$ in finite proper time $\tau=\pi\sqrt{R_0^3/8M}$, horizon crossing preceding the
singularity (C1).

$$\boxed{\;\text{exact Schwarzschild/Kerr: horizon }2M\text{, shadow }b_c=3\sqrt3\,M\text{ (GR-exact, was }+4.63\%\text{ under F114)}\text{, Hawking }T_H\propto M^{-1}\text{ (newly present)}\text{, eikonal ringdown tied to the photon sphere}\;}\tag{R19.1}$$

**The one genuinely new, non-GR feature: a lattice-regulated core.** GR's $r=0$ curvature singularity
($K_\text{Kretschmann}=48M^2/r^6\to\infty$) cannot be reached on the BCC lattice — curvature saturates
at the cell scale $1/a^4$, giving a core radius $r_\text{core}=(48(GM/c^2)^2a^4)^{1/6}\propto M^{1/3}$,
measured $\sim5\times10^{-22}$ m for a solar-mass hole: far inside the horizon, but $\sim10^{12}$ cells
across — a genuine extended core, not a single-cell artifact (L1). This is the substrate's own
singularity resolution, consistent with the exactly-unitary automaton (no true information-destroying
singularity), and the natural anchor for the model's answer to the black-hole information question —
though F183 itself leaves the microstate count open (§19.6).

$$\boxed{\;\text{lattice-regulated core: }r_\text{core}=(48(GM/c^2)^2a^4)^{1/6}\propto M^{1/3}\text{ — finite curvature at the centre, no GR point singularity}\;}\tag{R19.2}$$

(F183, checks S1–S2, Q1, K1–K2, C1, L1, X1; test `F183-blackhole` (8/8 PASS); no independent claim
card — cited within the withdrawn CL023 (F114) and the contingent CL295 (F354, below).)

### 19.2.2 F354 — geodesic completeness: bounded curvature alone forces a regular centre

F354 (2026-09-03) closes an open item F183 §L1 left standing: bounded curvature does not, on its own,
imply geodesic *completeness* — Zhou & Modesto (2023) exhibit regular black holes with everywhere-
bounded curvature that are nonetheless geodesically incomplete (the analytically extended Hayward
metric among them). F354 asks whether the model's own curvature bound is strong enough to rule that
failure mode out.

**It is, but not for the reason the finding's own first draft claimed.** The rebuilt result: for the
general **two-function** static spherically symmetric metric (the class F178/F181 say the interior
actually requires, §19.2.8 below), the Kretschmann scalar decomposes *exactly* as a sum of squares of
orthonormal-frame Riemann components,
$K=4R_{\hat t\hat r\hat t\hat r}^2+8R_{\hat t\hat\theta\hat t\hat\theta}^2+8R_{\hat r\hat\theta\hat r\hat\theta}^2+4R_{\hat\theta\hat\phi\hat\theta\hat\phi}^2$
(check B1). A single global bound $K\le a^{-4}$ therefore bounds **every term separately**, forcing
$B(0)=1$ (no solid-angle deficit), $B'(0)=0$, and $A(0)$ finite with $A'(0)=0$ — i.e.
$g_{\mu\nu}=\eta_{\mu\nu}+O(r^2)$ with bounded derivatives: a $C^{1,1}$ Lorentzian manifold interior
point, not a boundary. At $C^{1,1}$, geodesics exist and are unique (Chruściel–Grant), so timelike
geodesics with $E>1$ and radial null geodesics — the ones that actually reach $r=0$ — cross
transversally and continue (check B4), and the underlying automaton is separately tick-complete
(Tier A, a structural declaration the finding deliberately does not count toward its pass total, since
it does not rule out the affine-parameter failure mode Tier B closes).

$$\boxed{\;K\text{ (Kretschmann) is an exact sum of squares in the two-function metric; }K\le a^{-4}\Rightarrow C^{1,1}\text{ regular centre, no solid-angle defect, geodesics unique and pass through}\;}\tag{R19.3}$$

**The no-go, recorded deliberately rather than deleted.** F354's own first draft claimed a more
attractive route: that the BCC point group $O_h$ contains inversion, so every $O_h$-invariant density
is even in $r$, forcing the parity condition Hayward-class metrics need by fiat. **This is false in
both directions** — Hayward's own density is a function of $r$ alone (hence $O_h$-invariant) but
carries an odd $r^3$ term, because $r^{2k+1}$ is an $O_h$ invariant that is not a *polynomial*; and the
non-centrosymmetric point group $T_d$'s odd invariants all carry the factor $xyz$, whose spherical
average vanishes, so a non-centrosymmetric (diamond/zincblende) lattice would give the identical
regular centre. **The real load-bearing hypothesis is smoothness (analyticity) of the coarse-grained
core density at the centre — not any point-group symmetry** — and that hypothesis is exactly what is
least secure over a core only $\sim2.2$ cells across.

$$\boxed{\;\text{the } O_h\text{-parity route is a no-go, false both directions (Hayward's odd }r^3\text{ is }O_h\text{-invariant; }T_d\text{'s odd invariants have zero monopole)}\text{; the true hypothesis is smoothness of the core density, not symmetry}\;}\tag{R19.4}$$

**Three declared contingencies, one falsifier left standing.** The specific scales ($L=24^{1/4}a$
de Sitter radius at the centre, core radius $96^{1/6}M^{1/3}a^{2/3}$) depend on treating F183's
curvature *bound* as an *equality* (an open, dynamical CA question), on a curvature-ceiling convention
that conflicts by a factor of $24^{1/4}$ with a cosmology finding (F284, forward-cited to Chapter 20
— see §19.6), and on the Bardeen profile specifically (a Gaussian profile changes the core-radius ratio
to F183's proxy from $2^{1/6}$ to $0.7218$). The finding's own honest falsifier: measuring a nonzero
$r^3$ coefficient in the coarse-grained core density from an actual CA run would put the core in
Hayward's incomplete class — "currently unrun."

(F354, checks B1–B7 [7/7 counted, Tier A structural declaration excluded from the count by design];
test `F354-core-geodesic-completeness` (gate tier, 7/7 PASS, two controls verified red); CL295,
`contingent`, `exact`, `falsifier: stated`. Reviewed 2026-09-03 — REFUTED-then-rebuilt: the first
draft's $O_h$-parity mechanism was killed by the session's own attack pass and replaced with the
sum-of-squares argument above, per the finding's own header.)

### 19.2.3 F186 — the shadow ray-tracer: $b_c=3\sqrt3\,M$ confirmed, F114's enlargement withdrawn

F186 (2026-06-30) closes the observational leg of F183's shadow prediction by backward-integrating the
photon orbit equation $d^2u/d\phi^2+u=3Mu^2$ to find the capture/escape boundary directly, rather than
quoting the closed form.

$$\boxed{\;\text{ray-traced }b_c=5.1961\,M\text{ vs analytic }3\sqrt3=5.1962\,M\ (<10^{-3});\ \text{M87* }39.7\,\mu\text{as, Sgr A* }53.3\,\mu\text{as (GR)}\;}\tag{R19.5}$$

The three checks (3/3 PASS): the ray-traced $b_c$ matches the analytic $3\sqrt3\,M$ to the integrator
floor (T1); converted to angular diameters for the two EHT targets, the canonical GR shadow gives
M87\* $39.7\,\mu$as and Sgr A\* $53.3\,\mu$as — sitting consistently inside the EHT rings (the emission
ring is $\sim10\%$ larger than the shadow itself), whereas **F114 would have predicted $41.5$ and
$55.7\,\mu$as, a $+4.63\%$ enlargement now formally withdrawn** (T2); and the Kerr equatorial shadow
displacement grows monotonically with spin from $a=0.3M$ to $a=0.998M$, the spin–shadow asymmetry that
is the model's actual testable rotating-BH signature going forward (T3).

(F186, checks T1–T3 (3/3 PASS); test `test_F186_shadow_raytrace.py`; cited within the withdrawn CL023
(F114)/CL024 (the $+4.63\%$ shadow specifically) — see §19.5.)

### 19.2.4 F180 — the gravitational-wave equation: $c_\text{grav}=c_\text{lat}=1/\sqrt3$ exactly

F180 (2026-06-30) is this chapter's cleanest, most exact result, and it closes what its own header
calls audit C1: F106's static sourcing law $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ is elliptic — hence
instantaneous — and GW170817's multi-messenger bound requires
$\lvert c_\text{grav}-c_\text{photon}\rvert/c<10^{-15}$, an unmet gap the earlier dynamical dielectric
(F64 D-EM8) had left open with a hand-set free speed $c_g$.

**The argument, in four legs.** (1) $K$ renormalises the $(\mathbf E,\mathbf B)$ rotation rate itself
(F64 D-EM5), so the vacuum light cone is $\omega=c_\text{lat}\lvert\mathbf k\rvert$,
$c_\text{lat}=1/\sqrt3$. (2) $K$ has **zero tree stiffness** — the EM stress tensor's exact
tracelessness (F79, §18.2.7) means $K$ carries no bare kinetic term of its own; its entire stiffness
is the induced (Sakharov) response. (3) Because the graviton's inverse propagator *is* the one-loop
vacuum polarization $\Pi(q)$ of constituent propagators whose only velocity is $c_\text{lat}$, $\Pi(q)$
can depend on external momentum only through the constituent invariant
$Q^2=c_\text{lat}^2\lvert\mathbf q\rvert^2-q_0^2$ — verified directly: the induced self-energy is flat
along curves of constant $Q^2$ to an isocontour spread of $2.2\times10^{-5}$, while a control that
ignores $c$ varies by $\sim27\%$ (check C, the decisive one). **There is no free speed to choose**:
the graviton light cone is inherited, not tuned. (4) Promoting F106's static law to its causal
completion with this operator gives

$$\Big(\nabla^2-\frac{1}{c_\text{lat}^2}\partial_t^2\Big)\ln K(\mathbf x,t)=-\frac{8\pi G}{c^4}\,T^{00}[\psi](\mathbf x,t)\qquad\text{(D-GW)},$$

whose vacuum solutions are gravitational waves at exactly $c_\text{lat}$.

$$\boxed{\;\big(\nabla^2-c_\text{lat}^{-2}\partial_t^2\big)\ln K=-(8\pi G/c^4)T^{00}\text{: gravitational waves at }c_\text{grav}=c_\text{lat}=c_\text{photon}\text{ identically, not merely to measured precision}\;}\tag{R19.6}$$

Photon and graviton solve the **same** wave operator $\Box_\text{lat}$, so
$\lvert c_\text{grav}-c_\text{photon}\rvert/c=0$ exactly at leading order, and even the first lattice
correction is shared. At LIGO-band frequencies ($f\sim100$ Hz), the residual is bounded by
$(f/f_\text{Planck})^2\sim3\times10^{-83}$ — **68 orders of magnitude** below the GW170817 limit.

(F180, checks A–E (5/5 PASS: A, B, D exact/machine-precision; C lattice-numeric to $2.2\times10^{-5}$;
E lattice to $\sim3\%$, finite-grid); test `test_F180_gw_speed.py`; CL009 `live`/`exact`,
`falsifier: stated`; CL013 `live`/`exact`, `falsifier: stated` — "any confirmed non-zero
$c_\text{grav}/c_\gamma-1$ falsifies the inheritance mechanism... there is no free coefficient to
absorb it.")

### 19.2.5 F248 — the explicit transverse-traceless graviton: non-birefringent, luminal, for every direction

F248 (2026-07-15) closes the one thing F180 itself flagged as open (§5 of that finding): D-GW derives
only the **scalar** (conformal) mode of the linearised field equation. F248 builds the physical
spin-2 transverse-traceless graviton explicitly, for arbitrary propagation direction, on the genuine
BCC dispersion.

**The decoupling theorem.** For any unit direction $\hat{\mathbf k}$, the two helicity-$\pm2$
polarisation tensors $e^+,e^\times$ (built from any transverse orthonormal frame) are symmetric,
traceless, transverse and orthonormal to machine precision ($\le6.7\times10^{-16}$) over 200 random
directions. Because $K$ has zero tree stiffness (F79, reused here exactly as in F180), the induced
graviton self-energy is a rank-4 tensor forced by transversality into spin-2/spin-1/spin-0 pieces,
each with its own scalar form factor; the spin-2 piece is $f_2(Q^2)\,\Lambda_{ij,kl}(\hat{\mathbf q})$
with $\Lambda$ an exact idempotent projector under which **both** helicities are eigenvalue-1 — so
both multiply the **same** scalar form factor $f_2(Q^2)=A\,Q^2$ and share the **one** pole
$q_0=c_\text{lat}\lvert\mathbf q\rvert$ (sympy-exact). **The polarisation lives entirely in the
projector; the speed lives entirely in the scalar form factor — they are decoupled, so the two
graviton helicities are degenerate (non-birefringent) and luminal, by construction, not by
coincidence.**

$$\boxed{\;\text{TT basis exact for every direction (}\le6.7\times10^{-16}\text{); both helicities eigenvalue-1 of the spin-2 projector }\Lambda\text{, sharing one pole }q_0=c_\text{lat}\lvert\mathbf q\rvert\text{: exactly non-birefringent}\;}\tag{R19.7}$$

The mechanism specific to this model, not generic to any spin-2 field: the photon/graviton dispersion
is the **paired**, helicity-symmetric sum $\Omega_\text{even}=\omega_+(\mathbf k/2)+\omega_-(\mathbf
k/2)$ (F69), and because $\omega_-(\mathbf k)=\omega_+(-\mathbf k)$, this symmetric sum cancels the
odd chirality term $s_xs_ys_z$ that a naive doubled single-branch law $2\omega_+(\mathbf k/2)$ would
keep — leaving a helicity-blind $O((ka)^2)$ lattice anisotropy (ratio $4.000$ under $k\to2k$ along
$[111]$) rather than an $O(ka)$ birefringent one. A real-space TT wave packet propagates at
$0.9998\,c_\text{lat}$ for both polarisations, with a speed difference $<10^{-12}$, while an explicit
BCC constituent-loop calculation confirms the helicity degeneracy independently to $4.5\times10^{-16}$.

(F248, checks A–E (5/5 PASS: A/B exact/machine-precision, C exact, D/E lattice-numeric); test
`test_F248_tt_graviton_bcc.py`; CL219, `open`, `exact`, `falsifier: unset` — the claim card's `open`
status records that its full four-momentum Ward-identity transversality on the genuine lattice bubble
remains an honest open item, per the finding's own §4, even though the analytic projector argument is
closed.)

### 19.2.6 F189 — compact-binary inspiral: GW150914's chirp mass and ISCO frequency

F189 (2026-06-30) builds the two-body GW sector at leading (quadrupole/0PN) order, with the graviton
speed already fixed by F180: the chirp-mass-driven frequency sweep
$df/dt=\tfrac{96}{5}\pi^{8/3}\mathcal M_c^{5/3}f^{11/3}$.

$$\boxed{\;\text{GW150914 (}m_1=36,\,m_2=29\,M_\odot\text{): }\mathcal M_c=28.1\,M_\odot\text{, ISCO frequency }67.6\text{ Hz, }0.19\text{ s from 35 Hz to merger}\;}\tag{R19.8}$$

Three checks (3/3 PASS): the recovered chirp mass, ISCO frequency and in-band duration match the
observed event (I1); the chirp scaling $df/dt\propto f^{11/3}$ holds to machine precision (I2); and
the equal-mass chirp-mass identity $\mathcal M_c=m/2^{1/5}$ is exact (I3). This is standard GR
phasing, not a distinctive model prediction — the content is that the model's gravity sector, once
sourced by the full tensor, reproduces it with no extra parameter, anchored to F183's ISCO for the
merger frequency.

(F189, checks I1–I3 (3/3 PASS); test `test_F189_inspiral.py`; CL165, `live`, `quantitative`,
`falsifier: unset`.)

### 19.2.7 F187 — ringdown: GR quasinormal modes to $<7\%$, echoes exponentially suppressed

F187 (2026-06-30) closes the merger-to-ringdown leg with a WKB (Schutz–Will) solve of the axial
Regge–Wheeler perturbation problem on the Schwarzschild background F183 supplies.

$$\boxed{\;\text{WKB fundamentals track tabulated GR QNMs: }\ell=2\text{ within }6.7\%\text{(real)}/0.8\%\text{(imag)}\text{, improving to }1.6\%/0.2\%\text{ at }\ell=4\text{; echo transmission }\sim e^{-2\pi b_c\omega}\sim10^{-9}\;}\tag{R19.9}$$

Three checks (3/3 PASS): the WKB fundamental modes converge toward the tabulated Schwarzschild QNM
spectrum with increasing $\ell$ — exactly the trend expected as the modes localise on the photon
sphere where $\Omega_c=\lambda=1/(3\sqrt3\,M)$, F183's own eikonal identity (Q1); the ringdown
waveform is a damped sinusoid with quality factor $Q>1.5$ (Q2); and, the sharp observational
discriminator against F114, the near-horizon barrier transmission with a **true horizon** present is
exponentially small ($\sim10^{-9}$), so late-time echoes from the lattice core are suppressed —
consistent with LIGO/Virgo's non-detection of ringdown echoes, versus F114's horizonless object's
order-one predicted echoes (Q3).

(F187, checks Q1–Q3 (3/3 PASS); test `test_F187_qnm.py`; cited within the withdrawn CL025 (F114's
echo prediction) — see §19.5. No independent live claim card: F187's positive content is a GR
reduction, not a distinctive extension per D12's bar.)

### 19.2.8 F174/F176b/F181 — neutron-star interiors: from exclusion to genuine GR/TOV

This is the chapter's most instructive chain, because it shows the F178 decision being *forced* by
data rather than merely asserted. Chapter 18 already carried F173's exact tensor argument (the single
scalar forces anisotropic stress $p_r=-p_t$ and omits the Tolman $3p$ source) as **the argument for**
adopting the full-tensor law (`18-gravity.md` §18.2.10, R18.12); this chapter's job is the
observational leg Chapter 18 did not perform and the covariant fix that actually restores GR.

**F174 (2026-06-29) makes F173's discriminator concrete by solving both theories' hydrostatic
structure and overlaying real data.** Solving the literal F106 law (flat Laplacian, energy-only
source: $dm_E/dr=4\pi r^2\rho$, $dp/dr=-(\rho+p)m_E/r^2$, $z=e^{M_E/R}-1$) against the standard TOV
equations on the same $\Gamma=2$ polytrope EoS (tuned so GR reproduces $M_\text{max}\approx2.1\,
M_\odot$): GR shows the expected turnover at $M_\text{max}=2.14\,M_\odot$, $R=11.9$ km, matching PSR
J0740+6620 (N2). **The literal model has no turnover at all** — mass keeps rising to $25\,M_\odot$ at
the top of the tested density range, overpredicting by $4.5\times$ at fixed central density and
$\sim7$ km too large in radius at the J0740 mass (N3–N4).

$$\boxed{\;\text{the literal energy-only F106 law has no neutron-star maximum mass, overpredicts radii by }\sim7\text{ km at }2.08\,M_\odot\text{ — observationally excluded by PSR J0740+6620}\;}\tag{R19.10}$$

**F176b (2026-06-29) builds the covariant extension and measures how much it recovers.** Feeding the
*exact* Einstein $G^t_t$ of the dielectric metric (F173's own tensor) into a first-order relativistic
solver, sourced either by energy alone (cov-E) or by the GR trace-reversed $\rho+3p$ (cov-3p):
restoring curvature feedback alone rescues the pathology (cov-E gets a turnover at $M_\text{max}=
3.01\,M_\odot$, where the literal law had none), and restoring the Tolman pressure source on top of
that brings $M_\text{max}$ onto GR's to **0.4%** ($2.128$ vs $2.136\,M_\odot$), independent of EoS. A
$\sim2$ km $AB\equiv1$ residual survives even in cov-3p — the irreducible signature of insisting on
one scalar field in matter.

$$\boxed{\;\text{covariant curvature feedback restores a maximum mass; the pressure source matches GR's }M_\text{max}\text{ to }0.4\%\text{; a}\sim2\text{ km }AB\equiv1\text{ residual survives only if the single scalar is kept in matter}\;}\tag{R19.11}$$

**F181 (2026-06-30) is the actual F178 follow-through: the genuine two-function GR/TOV interior,
carrying the AB≡1 residual away entirely.** Rather than covariantizing the single scalar, F181 builds
the metric $ds^2=-A(r)dt^2+B(r)dr^2+r^2d\Omega^2$ with $A,B$ **independent** ($AB\ne1$), matched to
exact Schwarzschild exterior. Nine checks (9/9 PASS), all exact-algebraic where the class is metric-
level: the two-function areal metric solves vacuum $G_{\mu\nu}=0$ identically (C1), the single scalar
does not (its Einstein tensor is anisotropic, reproducing F173 exactly, C2), and the two-function
uniform-density interior sources an **isotropic** perfect fluid, $p_r=p_t$ exactly (C3) — precisely
what the single scalar cannot do. The `integrate_interior` solver reproduces standard TOV bit-for-bit
at the integrator floor, with a maximum-mass turnover present (N1); the full F62/F64 dynamic
wave-packet battery (equivalence principle, redshift, factor-2 deflection, unitary backreaction)
reproduces its earlier results unchanged (B1–B4), because it reads the metric only through $\sqrt A$
and $c_\text{eff}=c_0\sqrt{A/B}$, which agree with the dielectric to $O(u)$.

$$\boxed{\;\text{two-function }A,B\text{ interior: vacuum }=\text{exact Schwarzschild}\text{, interior sources an isotropic perfect fluid exactly (}p_r=p_t\text{), reproduces standard TOV bit-for-bit; the F62/F64 dynamic battery passes unchanged}\;}\tag{R19.12}$$

**A claims-layer bookkeeping note, checked rather than assumed.** `claims-index.md`'s CL160 — F181's
own claim card — reads `status: withdrawn`, `kind: no_go`. Reading CL160's own text (not merely its
front-matter) shows why this is very likely a mechanical extraction artifact, not a genuine physics
withdrawal, of the exact same shape Chapter 8 found for CL084/F89 (Gap [G-6]) and Chapter 12 found for
its own [G-7]: CL160 states outright, "A supersession/withdrawal banner appears in this finding's
header, which is why the card reads `withdrawn`" — but **F181's own header, read in full for this
chapter, carries no such banner**; it reads plainly "Status: Confirmed — 9/9 checks PASS," with no
`⚠` marker of the kind F174 and F176b *do* carry. F181 also appears in no `supersessions.yaml`
`superseded:` or `reclassified:` list (S4 names only F114 superseded and F106/F173/F174
reclassified). Substantively, F181 is not merely un-superseded — it is F178's own decision *carried
out*: the covariant two-function kernel R18.13 calls for, built one day after F178 itself. Flagged
here as **Gap [G-9]** rather than silently corrected (documentation-only chapter) or silently
repeated as fact.

> **Gap [G-9].** `claims-index.md` lists CL160 (F181's claim card) as `status: withdrawn`. F181's own
> finding-file header carries no supersession or withdrawal banner (unlike F174 and F176b, which do),
> and F181 is named in no `supersessions.yaml` record's `superseded:` or `reclassified:` list. CL160's
> own body text states its inferred `withdrawn` status rests on "a supersession/withdrawal banner"
> appearing in F181's header — a claim this chapter's full read of F181 did not confirm. Substantively,
> F181 builds exactly the covariant two-function interior kernel that F178's own decision (R18.13)
> calls for, one day after F178 itself, and is cited approvingly and without qualification by every
> later finding in this chapter's neutron-star chain (F184, F185, F356). This is the same
> claims-layer bookkeeping-artifact pattern Chapter 8 found for CL084/F89 (Gap [G-6]) and Chapter 12
> found independently for its own [G-7] — not fixed here, as this chapter is documentation-only.
> Whoever next touches CL160 should either attach the correct `supersessions.yaml` record (if one
> should exist and does not) or correct the card's `status` field to `live`, matching F181's own
> unambiguous header and this chapter's own reading of its content.

(F174, checks N1–N5 (5/5 PASS); CL154, `live`, `unset`, `falsifier: unset`. F176b, checks C1–C5
(5/5 PASS); CL157, `live`, `unset`, `falsifier: unset`. F181, checks C1–C4, N1, B1–B4 (9/9 PASS); test
`test_F181_covariant_interior_battery.py`; CL160 flagged above, Gap [G-9].)

### 19.2.9 F184/F185/F356 — realistic equations of state, rotation, and current-data robustness

**F184 (2026-06-30) drops realistic tabulated nuclear-matter equations of state (Read, Lackey, Owen &
Friedman 2009: SLy, AP4, MPA1) into the F181 kernel.**

$$\boxed{\;\text{SLy: }M_\text{max}=2.08\,M_\odot\text{ (turnover present)},\ R(1.4\,M_\odot)=11.1\text{ km — consistent with PSR J0740+6620 and the NICER radius band}\;}\tag{R19.13}$$

SLy lands directly on PSR J0740's measured mass with a canonical NICER-band radius (N1); the stiffer
cores show a larger $M_\text{max}$ (N2, narrowed 2026-09-03 from a compound $M_\text{max}$-*and*-
$R(1.4)$ claim to $M_\text{max}$-ordering alone, after an attack pass found the pre-existing `APR`
digit table did not match the published AP4 row — corrected to Read et al.'s verified digits, and the
narrowed check re-verified 3/3 PASS); and every EoS shows the expected stable-branch-to-turnover TOV
structure, not the literal-F106 runaway of F174 (N3).

**F185 (2026-06-30) extends the interior to first order in spin, computing frame dragging and the
moment of inertia via Hartle's slow-rotation theory on the same F181 background.**

$$\boxed{\;\text{a representative }0.95\,M_\odot\text{ star: }I/MR^2=0.313,\ I=0.63\times10^{45}\text{ g cm}^2\text{, correct compactness trend in frame drag and }\bar I\;}\tag{R19.14}$$

Three checks (3/3 PASS): the moment of inertia sits in the physical pulsar band ($I/MR^2=0.313$,
$\bar I=17.2$, surface frame-drag $\omega/\Omega=0.084$, R1); more compact stars drag frames more
strongly and have smaller $\bar I$, the correct GR trend (R2); and the SI value ($6.3\times10^{37}$
kg m$^2$) sits in the pulsar moment-of-inertia range (R3) — all with no extra input beyond the
F181 background, closing what F183's Kerr frame-drag opened for the exterior into the interior sector.

**F356 (2026-09-03) is a dedicated robustness pass against the *tightest current* (2024) NICER/PSR
mass-radius data, run specifically to test whether the F184 check has real discriminating power.**
Against PSR J0740+6620's Dittmann et al. (2024) radius band and, more decisively, PSR J0437−4715's
tighter Choudhury et al. (2024) band, SLy, AP4 (corrected) and MPA1 all pass simultaneously, while two
deliberately extreme cores (WFF1, very soft; MS1, very stiff) are correctly excluded by the same
J0437−4715 band even though both clear the J0740 mass floor — the falsification bracket the check
needed to show it was not vacuously passing anything handed to it.

$$\boxed{\;\text{SLy/AP4/MPA1 all pass current (2024) NICER/PSR bands simultaneously; WFF1 (soft) and MS1 (stiff) are correctly excluded — the discrimination is genuine, not vacuous}\;}\tag{R19.15}$$

AP4's margin against the tighter J0437−4715 band is honestly reported as tight ($0.7\%$) rather than
comfortable, and the finding's own attack pass (2026-09-03) additionally found and corrected the
pre-existing `APR` EoS digit error shared with F184, and a wrong paper attribution ("Salmi et al."
corrected to "Dittmann et al." for the J0740 radius).

(F184, checks N1–N3 (3/3 PASS, N2 narrowed 2026-09-03); test `test_F184_tabulated_ns.py`; CL162,
`live`, `quantitative`, `falsifier: stated` — "a standard, currently-favoured tabulated EoS... that
produces an $M_\text{max}$ below the PSR J0740 floor... would falsify.". F185, checks R1–R3 (3/3 PASS);
test `test_F185_rotation.py`; CL163, `live`, `quantitative`, `falsifier: unset`. F356, checks E1–E3
(3/3 PASS); test `test_F356_eos_robustness.py`; cited under CL162 alongside F181/F184.)

### 19.2.10 F357/F359 — the graviton/photon band top and a Planck-scale collision threshold

**F357 (2026-09-03) asks a question no earlier finding had posed: what is the actual top of the
photon/graviton propagating band, in physical units?** F248's paired even law
$\Omega_\text{even}=\omega_+(\mathbf K/2)+\omega_-(\mathbf K/2)$ is bounded by an exact trigonometric
identity: writing $a=u_+(\mathbf K/2)$, $b=u_-(\mathbf K/2)$, $\arccos(a)+\arccos(b)\le\pi\iff a+b\ge0$
(exact, sympy), and $a+b=2c_xc_yc_z\ge0$ everywhere on the natural single-branch Brillouin zone
(exact by construction) — so $\Omega_\text{even}\le\pi$ **exactly**, with equality attained on an
entire zone-boundary face, not merely at isolated points.

$$\boxed{\;\Omega_\text{max}=\pi\text{ exactly (an entire boundary face, not isolated points)}\ \Rightarrow\ E_\text{max}=\sqrt{\pi\sqrt3/8}\,E_\text{Planck}=0.8247\,E_\text{Planck}\text{, zero new free parameters}\;}\tag{R19.16}$$

Converting through F79/F107's registered ruler $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (reused verbatim, no
new input) gives the closed form $E_\text{max}/E_\text{Planck}=\sqrt{\pi\sqrt3/8}=0.82473$ — an $O(1)$
fraction of the Planck energy, not off by orders of magnitude in either direction, and related to
F352's independent cruder cutoff estimate by an exact factor $\pi\sqrt3$ (one reciprocal-lattice-vector
magnitude). **This is a genuine kinematic UV-completion statement — no propagating photon or graviton
mode exceeds $0.8247\,E_\text{Planck}$ on this lattice, as an exact consequence of the pairing
structure — but it is honestly scoped as a single-particle bound, not a graviton-graviton scattering
calculation**, which the finding's own §7 names as the remaining, still-open dynamical question.

**F359 (2026-09-03) asks the natural next question: does a head-on collision of two band-top quanta
clear the model's own black-hole-formation threshold?** Comparing $\sqrt{s_\text{max}}=2E_\text{max}$
(standard massless two-body kinematics) against $M_\text{rem}c^2$ — the model's own minimal, exact,
stable one-cell Planck-mass black-hole remnant (F228, $M_\text{rem}/M_\text{Pl}=3^{1/4}/\sqrt2\approx
0.9306$) — the registered ruler $A=a/\ell_P$ cancels **completely** in the ratio, sympy-confirmed:

$$\boxed{\;\frac{\sqrt{s_\text{max}}}{M_\text{rem}c^2}=\sqrt\pi\approx1.772\text{ (super-threshold pair)};\qquad\frac{E_\text{max}}{M_\text{rem}c^2}=\frac{\sqrt\pi}{2}\approx0.886\text{ (sub-threshold single quantum)}\;}\tag{R19.17}$$

both exact-algebraic given F357's and F228's own already-conditional-exact derivations (the finding's
own status line flags this compounding explicitly rather than presenting it as unconditional). **This
is honestly scoped, and the finding's own reviewed-and-corrected header is explicit about the scope
after an attack pass found an earlier draft overclaimed it**: it establishes only the *necessary,
purely energetic* precondition for Dvali–Gomez-style gravitational self-completeness/classicalization
— that a collision must first clear the CM-energy-vs-rest-mass threshold before any *geometric*
(hoop-conjecture/impact-parameter) black-hole-formation criterion could apply. No cross-section, no
impact parameter, and no graviton-graviton scattering amplitude is computed; F357's own dynamical
residual is explicitly unchanged by this finding.

(F357, checks A–F (6/6 PASS, exact-algebraic/lattice-numeric as tabulated); test
`F357-graviton-band-top`; CL297, `live`, `exact`, `falsifier: stated`. F359, checks A–E (5/5 PASS);
test `F359-graviton-collapse-threshold`; CL298, `live`, `exact`, `falsifier: stated`. Both reviewed
2026-09-03, both CONFIRMED-NARROWER/OVERSTATED-then-fixed after their own attack passes — residual
figures and scope language corrected in place, no defect required a hard-verdict downgrade in either
case.)

### 19.2.11 F111 — second-order light deflection: the $4\pi$ coefficient, correctly withdrawn

F111 (2026-06-07, recovered as a finding file 2026-07-31) computes the $O(\varepsilon^2)$ term of the
Bouguer/eikonal deflection integral for an index $n=1+2\varepsilon w+\sigma\varepsilon^2w^2$: a
general closed form $\alpha_2(\sigma)=\pi(2+\sigma)$, giving GR's isotropic-Schwarzschild coefficient
$\sigma=7/4\Rightarrow\alpha_2=15\pi/4$ (validating the machinery) and the **canonical lattice index**
$K=e^{2u}=1+2u+2u^2+\dots$ ($\sigma=2$) a coefficient $\alpha_2^\text{lat}=4\pi$ — an excess over GR
of exactly $\pi/4\,\varepsilon^2$.

**This coefficient is correctly withdrawn, for a reason this chapter can now state precisely that
F111's own file — written before F178 — could not.** F111's own text already flags the mechanism: its
D3 check is the one non-black-hole check `supersessions.yaml`'s S4 record notes was duplicated from
the retired `test_F114_dielectric_black_hole.py`, and S4's own `also_superseded` list for F114 names
"the 4 pi second-order deflection coefficient" explicitly as dead. The reason is R18.13: under F178,
$K=e^{2u}$ is understood to be only the **PPN-order** vacuum representation, agreeing with the exact
solution at $O(u)$ but differing from it at $O(u^2)$ — the exact vacuum solution is Schwarzschild, and
Schwarzschild's own second-order deflection is $15\pi/4$, GR's answer, not $4\pi$. F111's computation
is not wrong — the sympy algebra and the mpmath quadrature (checks D1–D3, N1) are correct closed-form
consequences of treating $K=e^{2u}$ as exact — but **the premise that $K=e^{2u}$ is the exact
strong-field metric is exactly what F178 supersedes.** Once the exact vacuum solution is known to be
Schwarzschild, the second-order deflection coefficient the model actually predicts is GR's own
$15\pi/4$, not F111's $4\pi$.

$$\boxed{\;\alpha_2^\text{lat}=4\pi\text{ (correct algebra, for the now-superseded premise }K=e^{2u}\text{ exact)}\text{; the model's actual second-order coefficient, given the exact Schwarzschild vacuum solution (R18.13), is GR's }15\pi/4\text{, not }4\pi\;}\tag{R19.18}$$

(F111, checks D1–D4, N1 (correct algebra, superseded premise); no dedicated test record beyond the
duplicated D3 leg; **CL027, `withdrawn`, `exact`, `falsifier: stated`** — confirmed directly against
S4's `also_superseded` clause for F114, not inferred from CL027 alone.)

### 19.2.12 F204 — the Alcubierre warp family: structurally excluded, more completely than GR+QFT

F204 (2026-06-30) confronts a well-known GR solution family — the Alcubierre warp metric and its
relatives — with the constraint that in this model gravity is *induced*, sourced forward from beable
matter (F178), rather than a freely specifiable geometry. The brief question: not "does GR admit the
metric" (it admits any metric for *some* $T_{\mu\nu}$) but "can the lattice **produce** the
$T_{\mu\nu}$ the warp metric needs." Full treatment, including why this is *stronger* than the standard
GR+QFT exclusion, is given in §19.5 below, where it belongs per this chapter's own "what was excluded"
convention; the headline result is stated here for the record:

$$\boxed{\;\text{superluminal Alcubierre/Natário/contested-Lentz: STRUCTURALLY EXCLUDED (no beable negative-energy channel exists at all, stronger than the Ford--Roman quantum-inequality bound)}\text{; subluminal positive-energy warps: NOT excluded, but FTL-less and capped at }c_\text{lat}\;}\tag{R19.19}$$

(F204, checks G1–G2, PA1, PA3, PC1 (5/5 PASS: G1 exact sympy, remainder numeric); test
`test_F200_alcubierre_structural.py` (filename retains a working `F200` tag; test-registry record
`F200-alcubierre-structural`, `findings:` corrected to name F204); CL178, `live`, `exact`,
`falsifier: unset`.)

## 19.3 Results table

| # | Statement | Class | Exactness | Test record |
|---|---|---|---|---|
| R19.1 | Exact Schwarzschild/Kerr: horizon $2M$, shadow $3\sqrt3\,M$ (GR-exact), Hawking $T_H\propto M^{-1}$, eikonal ringdown $=$ photon sphere | exact (closed forms) / quantitative (numeric cross-checks) | $<10^{-3}$ (photon-sphere solve) | F183; `F183-blackhole` (8/8) |
| R19.2 | Lattice-regulated core: $r_\text{core}\propto M^{1/3}$, finite curvature, no point singularity | quantitative | see F183 §L1 | F183; `F183-blackhole` (8/8) |
| R19.3 | Kretschmann is a sum of squares (two-function metric); $K\le a^{-4}\Rightarrow C^{1,1}$ regular centre, geodesics unique and pass through | exact-algebraic | sympy zero residual | F354; `F354-core-geodesic-completeness` (gate, 7/7) |
| R19.4 | $O_h$-parity route to the regular centre is a no-go (false both directions); real hypothesis is smoothness of the core density | exact-algebraic counterexample | — | F354; `F354-core-geodesic-completeness` (gate, 7/7) |
| R19.5 | Ray-traced $b_c=5.1961\,M$ vs analytic $5.1962\,M$; EHT shadows M87\* $39.7\,\mu$as, Sgr A\* $53.3\,\mu$as; F114's $+4.63\%$ withdrawn | quantitative | $<10^{-3}$ | F186; `test_F186_shadow_raytrace.py` (3/3) |
| R19.6 | $(\nabla^2-c_\text{lat}^{-2}\partial_t^2)\ln K=-(8\pi G/c^4)T^{00}$; $c_\text{grav}=c_\text{lat}=c_\text{photon}$ exactly | exact (coefficient identity, dispersion slope) / lattice-numeric (self-energy flatness, wavefront) | $2.2\times10^{-5}$ (check C, decisive) | F180; `test_F180_gw_speed.py` (5/5) |
| R19.7 | Explicit TT graviton, every direction; both helicities eigenvalue-1 of the spin-2 projector, one common pole; exactly non-birefringent | exact (projector algebra) / lattice-numeric (packet, loop) | $\le6.7\times10^{-16}$ | F248; `test_F248_tt_graviton_bcc.py` (5/5) |
| R19.8 | GW150914: $\mathcal M_c=28.1\,M_\odot$, ISCO $67.6$ Hz, $0.19$ s in band — standard quadrupole chirp | quantitative | matches observed event | F189; `test_F189_inspiral.py` (3/3) |
| R19.9 | WKB QNM fundamentals within $7\%$ of tabulated GR, improving with $\ell$; echo transmission $\sim10^{-9}$ with a true horizon | quantitative | see F187 table | F187; `test_F187_qnm.py` (3/3) |
| R19.10 | Literal energy-only law: no NS maximum mass, $\sim7$ km radius excess at $2.08\,M_\odot$ — excluded by PSR J0740 | quantitative | see F174 table | F174; `test_F174_stellar_overlay.py` (5/5) |
| R19.11 | Covariant curvature feedback restores a turnover; pressure source matches GR $M_\text{max}$ to $0.4\%$; $\sim2$ km $AB\equiv1$ residual if the single scalar is kept | quantitative | $0.4\%$ ($M_\text{max}$) | F176b; `test_F176_covariant_stellar.py` (5/5) |
| R19.12 | Two-function $A,B$ interior: vacuum $=$ exact Schwarzschild; interior sources isotropic fluid exactly; TOV reproduced bit-for-bit | exact (metric-level, C1–C4) / numeric-to-floor (N1) / dynamic (B1–B4) | sympy zero residual | F181; `test_F181_covariant_interior_battery.py` (9/9) |
| R19.13 | SLy: $M_\text{max}=2.08\,M_\odot$, $R(1.4)=11.1$ km — consistent with PSR J0740/NICER; stiffer cores order correctly | quantitative | see F184 table | F184; `test_F184_tabulated_ns.py` (3/3) |
| R19.14 | Slow-rotation: $I/MR^2\approx0.31$, $I\approx0.6\times10^{45}$ g cm$^2$, correct compactness trend | quantitative | pulsar band | F185; `test_F185_rotation.py` (3/3) |
| R19.15 | SLy/AP4/MPA1 pass current NICER/PSR bands; WFF1/MS1 correctly excluded — genuine discrimination | quantitative | see F356 table | F356; `test_F356_eos_robustness.py` (3/3) |
| R19.16 | $\Omega_\text{max}=\pi$ exactly (whole boundary face); $E_\text{max}=0.8247\,E_\text{Planck}$, zero new free parameters | exact-algebraic | sympy $=0$; $4.4\times10^{-16}$ | F357; `F357-graviton-band-top` (6/6) |
| R19.17 | $\sqrt{s_\text{max}}/M_\text{rem}c^2=\sqrt\pi$ (super-threshold pair); $E_\text{max}/M_\text{rem}c^2=\sqrt\pi/2$ (sub-threshold single quantum) | exact-algebraic (compounded conditional) | sympy exact | F359; `F359-graviton-collapse-threshold` (5/5) |
| R19.18 | $\alpha_2^\text{lat}=4\pi$ (correct algebra, superseded premise); model's actual coefficient is GR's $15\pi/4$ | exact (algebra) / withdrawn (as a model prediction) | sympy exact | F111; duplicated D3 leg |
| R19.19 | Superluminal Alcubierre structurally excluded (no beable negative-energy channel); subluminal class allowed, capped at $c_\text{lat}$ | exact (G1) / numeric (remainder) | sympy zero residual (G1) | F204; `test_F200_alcubierre_structural.py` (5/5) |

## 19.4 Comparison with measurement

**GW170817 (the speed of gravity).** F180's identity $c_\text{grav}=c_\text{lat}=c_\text{photon}$ is
satisfied not to the GW170817 bound but by **68 orders of magnitude** beyond it — the residual at
LIGO-band frequencies is bounded by $(f/f_\text{Planck})^2\sim3\times10^{-83}$ against a measured
limit of $10^{-15}$. Because the identity has no free coefficient (CL013), there is nothing to tune;
any confirmed nonzero speed difference falsifies the mechanism outright, not merely the number.

**PSR J0740+6620 and NICER (neutron-star structure).** The chain F174→F176b→F181→F184→F356 is a
genuine falsification-and-recovery story, reported here at each stage's true status. The *literal*
weak-field law is excluded by PSR J0740's $2.08\pm0.07\,M_\odot$ mass (no maximum mass at all,
R19.10). The genuine covariant fix — F178's own two-function kernel, not a patched single scalar — not
only restores a maximum mass but, on realistic tabulated equations of state, lands SLy directly on
J0740's measured mass with a NICER-band radius (R19.13), and passes the tighter, more current
PSR J0437−4715 band (Choudhury et al. 2024) simultaneously while correctly excluding two deliberately
extreme EoS outliers (R19.15) — a genuinely discriminating test, not one that passes anything handed
to it.

**M87\* and Sgr A\* (EHT shadow imaging).** F186's ray-traced GR shadow diameters (M87\* $39.7\,
\mu$as, Sgr A\* $53.3\,\mu$as) sit consistently inside the EHT's measured photon rings (M87\*
$42\pm3\,\mu$as, 2019; Sgr A\* $51.8\pm2.3\,\mu$as, 2022) — the emission ring itself runs
$\sim10\%$ larger than the shadow boundary, as expected. This is precisely the observation that F114's
now-withdrawn $+4.63\%$ enlargement would have had to clear, and does not need to: the canonical
object predicts the number EHT actually measured.

**GW150914 (compact-binary coalescence).** F189's recovered chirp mass ($28.1\,M_\odot$ against the
observed $\sim28.6\,M_\odot$), ISCO frequency ($\sim68$ Hz) and in-band duration ($\sim0.19$ s) track
the observed event at leading PN order, and F187's ringdown spectrum reproduces the tabulated GR
quasinormal-mode frequencies to $<7\%$ at $\ell=2$, improving with $\ell$ — together spanning
inspiral–merger–ringdown with no distinctively model-specific feature in any of the three phases.

## 19.5 What was excluded, and why

- **F114 — the horizon-free dielectric black hole.** Already the subject of Chapter 18's §18.5 in
  full (cross-referenced, not re-derived here); this chapter's own findings supply the specific
  replacement numbers R18.13 forward-cited. F183 replaces the object itself (exact Schwarzschild/Kerr,
  R19.1–R19.2); F186 replaces the shadow prediction, explicitly withdrawing the $+4.63\%$ enlargement
  and confirming the GR value against the actual EHT rings (R19.5); F187 replaces the ringdown
  prediction, showing echoes are exponentially suppressed by the newly-present horizon rather than
  order-one as F114's horizonless object predicted (R19.9); and F354 replaces F114's implicit
  singularity-avoidance story with a derived one — a $C^{1,1}$ regular centre forced by the curvature
  bound alone, with the point-group route that would have made this "automatic" shown to be a no-go
  (R19.3–R19.4). The withdrawn claim family — CL023 (the condensate itself), CL024 (the $+4.63\%$
  shadow), CL025 (ringdown echoes), and CL027 (the $4\pi$ second-order bending coefficient, R19.18) —
  is confirmed here by reading each superseding finding's own numbers against the withdrawn claim, not
  merely by citing the claim cards' `withdrawn` status.
- **F111's $4\pi$ second-order deflection coefficient (this chapter's own finding, not a Chapter 18
  inheritance).** Withdrawn for the reason stated in §19.2.11: the coefficient is a correct algebraic
  consequence of treating $K=e^{2u}$ as the *exact* vacuum metric, and that premise is exactly what
  F178/R18.13 supersedes. The model's actual second-order light-bending prediction, given the exact
  Schwarzschild vacuum solution, is GR's own $15\pi/4$.
- **Superluminal Alcubierre/Natário/contested-Lentz warp drives (F204).** The Eulerian energy density
  of the Alcubierre metric is exactly $\rho\propto-f'(r_s)^2\le0$ wherever the warp-bubble wall profile
  is nonzero (sympy-exact, zero residual) — a standard result (Pfenning–Ford 1997), reproduced here
  symbolically. What makes the exclusion *structural* in this model specifically, and strictly stronger
  than standard GR+QFT's Ford–Roman quantum-inequality bound: the model's gravitating source is the
  beable energy density, a sum of manifestly non-negative per-cell quadratic terms, with the
  zero-point $\tfrac12\hbar\omega$ piece explicitly non-gravitating (F193, cited from Chapter 20's
  cosmology chain) — **there is no negative-beable channel at all**, whereas standard QFT permits
  bounded local negative energy (Casimir, squeezed states) that at least has a chance of threading the
  quantum-inequality needle. The exclusion holds independent of speed (the wall's negative sign
  scales as $-v_s^2$, present for all $v_s$, not only superluminal ones) and the obstruction is
  specifically the source's *sign*, not the covariant kernel's capacity to carry exotic stress (F181's
  own kernel handles anisotropic stress without complaint). The **subluminal** positive-energy family
  (Bobrick–Martire/Fuchs 2024) is not excluded — nothing in the model forbids a $T^{00}\ge0$ source —
  but carries no FTL utility by construction and is capped at $c_\text{lat}=1/\sqrt3$, because the
  metric here is *induced* from $c_\text{lat}$-bounded fields rather than an independently dynamical
  object, so there is no continuum-style "the metric itself carries the ship FTL" loophole.

## 19.6 What is still open

1. **F354's maximal-extension completeness is not established.** The $C^{1,1}$ regular-centre result
   is a local $r\to0$ analysis; completeness of the full two-horizon conformal diagram (what Zhou &
   Modesto actually construct for comparable regular black holes) is not shown. The inner-horizon
   mass-inflation instability — a dynamical perturbation question — is explicitly untouched and named
   by F354 itself as "the strongest live threat, and the natural next session."
2. **F354's own falsifier is currently unrun.** Measuring the $r^3$ coefficient of the coarse-grained
   core density from an actual CA collapse run would settle whether the core is in Hayward's
   geodesically-incomplete class or the regular class this chapter reports — "this is the finding's
   real test and it is currently unrun."
3. **A curvature-ceiling convention conflict, flagged but not resolved, between this chapter and
   cosmology.** F354 uses F183's convention $K_\text{max}=1/a^4$; a cosmology finding (F284, Chapter
   20) implies instead $H_\text{max}=1/a\Rightarrow K_\text{max}=24/a^4$ for a de Sitter ceiling — the
   two conventions differ by $24^{1/4}$ in every derived length, and F354's own text notes the
   alternative convention is "markedly more elegant" (the core radius becomes exactly one cell, the
   $E=1$ e-folding becomes exactly the model's own minimum resolvable time) without adopting it,
   flagging the fork as "an open decision deserving its own session." A related $\sqrt3$ discrepancy
   in the tick duration between F107 and F284 is also flagged, unresolved.
4. **The $\sim2$ km $AB\equiv1$ residual (F176b, R19.11) is not a standing prediction** once F181's
   genuine two-function kernel is adopted (per F178's own decision) — it applies only to the
   intermediate, now-superseded covariant-single-scalar construction. It is reported here as the
   measure of how close the one-field philosophy could have come, not as an open observational target.
5. **F357/F359's dynamical residual is explicitly, and repeatedly, not closed.** Both findings state
   their own scope with unusual care after their attack passes corrected earlier overclaiming: F357
   supplies a single-particle kinematic energy ceiling, not a graviton-graviton scattering amplitude
   or partial-wave unitarity bound; F359 supplies a necessary energetic precondition for
   Dvali–Gomez-style classicalization, not the geometric hoop-conjecture criterion that literature
   actually uses. A genuine black-hole-formation cross-section at the lattice scale remains fully open.
6. **F183's QNM correspondence and echo bound are order-of-magnitude, not precision, results.** F187's
   own text is explicit that a direct Leaver continued-fraction or time-domain Teukolsky solve is
   needed for overtone-level precision and a quantitative (rather than order-of-magnitude) echo-
   amplitude bound against LIGO/Virgo data.
7. **The black-hole information question is named, not answered.** F183's lattice-regulated core is
   the natural substrate for a microstate count reproducing the area-entropy law $S=A/4$ (cited from
   F190, Chapter 20's cosmology chain), but that counting is not performed by any finding in this
   chapter's assigned set.
8. **CL219 (F248's claim card) is honestly `open`**, not `live`: the analytic decoupling-theorem
   argument for TT-graviton non-birefringence is exact, but the full four-momentum Ward-identity
   transversality of the genuine *lattice* self-energy bubble (as opposed to the crude static-vertex
   numeric check F248 itself flags as not gated) is not yet closed.
9. **Gap [G-9]**, logged in §19.2.8 above: `claims-index.md`'s CL160 (F181) reads `withdrawn`, which
   this chapter's full read of F181's own header does not confirm — likely a mechanical extraction
   artifact, not corrected here as this chapter is documentation-only.

## 19.7 Falsifiers

From the relevant claim cards, reported at their actual status:

1. **CL009/CL013 (F180, GW speed) carry `falsifier: stated`, `status: live`**: any confirmed nonzero
   $c_\text{grav}/c_\gamma-1$ falsifies the inheritance mechanism outright — there is no free
   coefficient to re-fit, unlike a modified-gravity model.
2. **CL297/CL298 (F357/F359, band top and collision threshold) carry `falsifier: stated`,
   `status: live`**: a demonstration that F69's paired "even" dispersion law is not the model's actual
   physical photon/graviton law would remove the domain restriction both bounds rely on (each
   finding's own control shows exactly what changes — both ratios exactly double under the wrong
   law); a revision of F79/F107's structural ruler $a/\ell_P$, or of F228's one-cell remnant
   derivation, would move the quoted numbers with it, inheriting rather than duplicating those
   findings' own falsifiers.
3. **CL295 (F354, geodesic completeness) carries `falsifier: stated`, `status: contingent`**: measuring
   a nonzero $r^3$ coefficient in the coarse-grained core density from an actual CA run would put the
   core in the geodesically incomplete Hayward class — the sharpest, and currently unrun, falsifier in
   this chapter.
4. **CL162 (F181/F184/F356, tabulated-EoS neutron stars) carries `falsifier: stated`, `status: live`**:
   a standard, currently-favoured (non-outlier) tabulated nuclear-matter EoS that, run unmodified
   through the F181 kernel, produces an $M_\text{max}$ below the PSR J0740 floor would falsify the
   result — this is a genuinely testable claim against future EoS refinements, not merely against
   current data.
5. **CL154/CL157/CL163/CL178/CL219 carry `falsifier: unset`** — declared debt (D12), not claims that no
   falsifier exists. CL178 (F204, the Alcubierre exclusion) in particular would benefit from an
   explicit falsifier statement given how sharp its structural content is (no beable negative-energy
   channel, full stop) — flagged as an easy follow-up, not performed here.
6. **CL023–CL027 (the withdrawn F114 family) have their falsifiers explicitly inverted**, exactly as
   Chapter 18 already stated for CL023 itself: an observed horizon, an EHT shadow matching the GR
   value rather than F114's $+4.63\%$, an absence of ringdown echoes, and a second-order light-bending
   coefficient matching GR's $15\pi/4$ rather than F111's $4\pi$ — all of which current observation
   already shows — are no longer scored as falsifications; they are confirmations of the model's
   current (F178-era) prediction.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $r_h,\ b_c,\ \kappa$ | Schwarzschild horizon ($2M$), critical impact parameter / shadow radius ($3\sqrt3\,M$), surface gravity ($1/4M$) | §19.2.1 |
| $T_H$ | Hawking temperature, $\hbar c^3/(8\pi Gk_BM)$ | §19.2.1 |
| $r_\text{core}$ | The lattice-regulated black-hole core radius, $\propto M^{1/3}$, where curvature saturates at $1/a^4$ | §19.2.1 |
| $A(r),\ B(r)$ | The two independent metric functions of the genuine GR/TOV interior kernel ($AB\ne1$, unlike the demoted dielectric's $AB\equiv1$) | §19.2.8 |
| $\Omega_\text{max}$ | The exact top of the paired photon/graviton dispersion band, $=\pi$ radians/tick | §19.2.10 |
| $M_\text{rem}$ | The model's minimal, one-cell, stable Planck-mass black-hole remnant (F228, reused here) | §19.2.10 |

---

*This chapter logs one new gap, [G-9] (§19.2.8): `claims-index.md`'s CL160 (F181) reads `withdrawn`,
which F181's own finding-file header — read in full for this chapter — does not confirm; likely a
mechanical extraction artifact of the same shape Chapter 8's [G-6] and Chapter 12's [G-7] found
elsewhere in the claims layer. No finding, claim card, module, or test record was created or modified
in the writing of this chapter.*
