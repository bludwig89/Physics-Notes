# Chapter 20 — Cosmology: the Friedmann Sector, BBN, Structure Formation, and the Inflation No-Go

*Chapter 20 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F182-friedmann-pressure-cosmology.md`,
`findings/F188-multicomponent-lcdm-cosmology.md`,
`findings/F202-leptogenesis-from-intrinsic-L-violation.md`,
`findings/F282-no-slow-roll-inflaton-sub-planckian-cutoff.md`,
`findings/F283-elastic-lattice-excluded-and-f282-invariance.md`,
`findings/F284-rigid-lattice-expansion-and-primordial-state.md`,
`findings/F285-initial-condition-measure-cannot-tilt.md`,
`findings/F286-second-scale-must-be-a-log-not-a-length.md`,
`findings/F288-structure-formation-zero-free-functions.md`,
`findings/F295-tilt-is-an-anomalous-dimension-not-a-second-scale.md`,
`findings/F296-holographic-cosmology-names-the-operator-and-validates-T1.md`,
`findings/F297-bbn-light-element-abundances.md`,
`findings/F309-gstar-from-model-content.md`,
`findings/F310-gamma-is-a-blockspin-eigenvalue.md`,
`findings/F360-horizon-thermodynamics-frw.md`,
`findings/F361-bbn-a7-rate-repair-and-gdot-prediction.md`,
`findings/F363-k4-inflation-reopening-checked-nogo-survives.md`,
`findings/F364-baryogenesis-boltzmann.md`,
`findings/F369-transfer-function-scoping.md`, and
`findings/F372-npsplit-theory-uncertainty.md`
(the twenty findings `00-plan.md` §2 assigns to this chapter, all read in full), against
`docs/monograph/18-gravity.md` (R18.x, the full-tensor induced Einstein equation), `docs/monograph/
19-strong-field-and-wave-gravity.md` (R19.x, and specifically its forward-flagged F354/F284
convention conflict, resolved in part below), `docs/theory/supersessions.yaml` (none of this
chapter's twenty findings appears in any `superseded:` or `reclassified:` list), `claims-index.md`
(CL161/CL164/CL240–CL244/CL248/CL249/CL254/CL258/CL259/CL266/CL267/CL299/CL304/CL176, read in full
below), and `references/holographic-cosmology-summary.md` (F296's external anchor). Notation and
results are those of Chapters 1 (P1, rigidity), 18 (R18.7–R18.13, the induced Einstein equation and
structural $G$) and 19 (R19.3–R19.4, F354's geodesic-completeness construction), extended, never
redefined.

## 20.0 What this chapter establishes

On this model's own rigid, non-stretching lattice substrate, "the universe is expanding" does not
mean the cell spacing $a$ is growing — F283 shows the spacing cannot be elastic without breaking
already-measured physics, and F284 shows what expansion *is instead*: the homogeneous, conformal
mode of the same dielectric field $K$ that Chapter 18 already built the whole gravity sector from.
Given that reading, the model reproduces standard $\Lambda$CDM's expansion history exactly
(F182/F188), its Big Bang nucleosynthesis light-element abundances to sub-percent (F297/F361,
after a rate-fit repair), and its neutron-lifetime/helium constraint on $m_n-m_p$ once that
constraint is read with an honest theoretical uncertainty rather than as a point-exclusion (F372).
It does **not** reproduce inflation, and proves rather than merely fails to find one: no compact
lattice field direction can slow-roll, by an exact, scale-free obstruction tied to the lattice's own
coordination geometry (F282/F283/F363). That forces the primordial power spectrum to be an
automaton *initial condition* rather than a dynamical output — and the chapter's second headline
result is that even this weaker claim comes with real structure: the primordial tilt survives a
sequence of increasingly sharp characterizations (F285→F286→F295→F296→F310) that end with a clean,
falsifiable in-model identification — the tilt is an anomalous scaling dimension on the automaton's
own $t{=}0$ measure, read off the model's own already-measured renormalization-group spectrum — and
a strong, near-certain prediction that follows for free: no observable primordial tensor mode,
ever. Structure formation is then fixed with **zero** free functions where the standard effective
field theory of dark energy needs two (F288), and the same rigid-substrate, full-tensor-sourced
picture independently reproduces the Friedmann pair by a completely different route, horizon
thermodynamics (F360). The chapter closes with baryogenesis and leptogenesis: the model has every
Sakharov ingredient it needs (F202), and a real Boltzmann calculation (F364) shows precisely how far
short its own *native* numbers fall of the observed asymmetry, and by how much fine-tuning either
free residual would need to close the gap.

## 20.1 Inputs

**Postulates used.** **P1** (the rigid, discrete lattice) is the central postulate of this
chapter — every result in Groups A–C below turns on the fact that $a$ is a constant of the substrate,
not a dynamical variable, so that "cosmic expansion" cannot mean the lattice stretching. **P4**
(linearity/unitarity) underlies the automaton's own $t{=}0$ initial-state framing that Group D's
tilt discussion depends on (F284's "the initial state is specified across the whole lattice at
once"). **P7** (elegant design) is invoked explicitly in F284 (§10, "not obviously a good trade")
and F286 (the coincidence discipline of §6) as a stated *discipline against* over-interpreting
numerical near-misses, the opposite use from earlier chapters — worth noting because it shows the
heuristic cuts both ways in this model's own practice.

**Prior results used, precisely.** **R18.7–R18.9** (F79's structural $G=a^2c^3/(8\pi\sqrt3\hbar)$,
$a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$) is the single most-reused number in this chapter: F282's
inflation obstruction, F283's scale-invariance proof, and F284's epoch scales all assemble directly
from it. **R18.11–R18.13** (F178's decision that the full-tensor induced Einstein equation is
canonical, sourced by the complete stress-energy tensor, with the single-scalar dielectric demoted
to a vacuum/weak-field representation) is the field equation every Friedmann-pair derivation in
Group A adopts — F182's whole point is that the *pressure*-weighted source this decision requires is
what standard cosmology needs and the demoted energy-only law would have gotten wrong by a factor
2. **R19.3–R19.4** (F354's Kretschmann-scalar-as-sum-of-squares construction and its curvature
ceiling $K_\text{max}=1/a^4$) is the object this chapter's §20.3.4 below directly engages, per
Chapter 19's own forward flag.

**Free inputs consumed.** The baryon-to-photon ratio $\eta_{10}=6.137$ (Planck) is external to
every BBN finding in this chapter (F297/F361/F372) — the model derives no asymmetry *magnitude*
(F202/F364 make this precise). $|V_{ud}|$ and $G_F$ (the weak-coupling normalization for the BBN
network) are likewise external. The EH98 no-wiggle transfer function's acoustic-envelope
coefficients remain imported in F288/F369 — F369 replaces two of its scale-setting numbers with
model-native derivations but explicitly does not replace the acoustic-oscillation shape itself. The
oscillation parameters (PMNS mixing angles, mass splittings) F364 uses to fix the Casas–Ibarra
Dirac-Yukawa matrix are external, standard global-fit values, unrelated to this model.

## 20.2 The derivation

### Group A — The Friedmann sector itself

#### 20.2.1 F182 — pressure gravitates; the demoted energy-only law would have mis-weighted the early universe by exactly a factor 2

For flat FLRW under the full-tensor source (R18.11), the Friedmann pair is
$$H^2=\frac{8\pi G}{3}\rho,\qquad \frac{\ddot a}{a}=-\frac{4\pi G}{3}\Big(\rho+\frac{3p}{c^2}\Big),$$
and F182's central algebraic result is that the $\rho+3p$ combination in the acceleration equation
is **forced**, not chosen: differentiating Friedmann I and substituting the continuity equation
gives $\ddot a/a=-4\pi G\rho(1+3w)/3$ exactly (sympy, zero residual), and the demoted energy-only
law's $\ddot a/a=-(4\pi G/3)\rho$ is consistent with this **only if** $p=0$ — the Bianchi identity
rejects it for any $w\ne0$. Radiation ($w=1/3$) is where this bites hardest: the deceleration
parameter is $q=1$ under the full-tensor law and $q=1/2$ under the demoted law, i.e. the energy-only
reduction would have underweighted the radiation-era expansion rate by exactly a factor $2$
(confirmed numerically to $3\times10^{-7}$). Because the radiation era sets the expansion rate
during BBN and at matter–radiation equality, this is not a cosmetic correction.

$$\boxed{\;\ddot a/a=-\tfrac{4\pi G}{3}(\rho+3p/c^2)\text{ forced by Friedmann I + continuity (Bianchi); radiation }q=1\text{ (full-tensor) vs }q=\tfrac12\text{ (energy-only), a factor-2 mis-weighting}\;}\tag{R20.1}$$

(F182, checks A1/A2/N1–N4, 6/6 PASS; CL161, `live`, `exact`, `falsifier: unset`.)

#### 20.2.2 F188 — multi-component ΛCDM: $z_\text{eq}\approx3430$, $z_\text{acc}\approx0.63$, age $\approx13.8$ Gyr

Extending F182's single-component Friedmann pair to a flat three-component background
($\Omega_r+\Omega_m+\Omega_\Lambda=1$), with the acceleration equation weighting each component by
its own $\rho+3p$, reproduces the standard $\Lambda$CDM timeline with no tuning beyond the measured
density fractions: matter–radiation equality at $1+z_\text{eq}=\Omega_m/\Omega_r\Rightarrow
z_\text{eq}=3433$, the onset of accelerated expansion at $z_\text{acc}=0.63$ (driven by $\Lambda$'s
$w=-1$, $\rho+3p=-2\rho$), and a present age of $13.79$ Gyr — all matching Planck 2018. The flat
normalization $E(a{=}1)=1$ holds exactly.

$$\boxed{\;z_\text{eq}=3433,\ z_\text{acc}=0.63,\ \text{age}=13.79\text{ Gyr, all Planck-2018-consistent, pressure-weighted at every transition}\;}\tag{R20.2}$$

(F188, checks L1–L3, 3/3 PASS; CL164, `live`, `quantitative`, `falsifier: unset`.)

#### 20.2.3 F284 — expansion is the conformal mode of $K$, not the substrate stretching: $\dot G/G\equiv0$ exactly

F284 answers the question F282/F283 force: if the lattice does not stretch (P1, and F283 below)
and there is no inflaton, what *is* the expanding universe? The answer reuses machinery Chapter 18
already built rather than positing anything new. The emergent metric is built from the dielectric
$K$ (R18.8–R18.11); $K$ is a field *on* the lattice, $a$ is a property *of* the lattice, and only
$K$ is dynamical. **The FRW scale factor is $K$'s homogeneous mode** — "space expanding" means the
emergent metric assigns growing proper distance to a fixed number of cells, with nothing about the
substrate itself changing. This does not move a single number in F182/F188: those findings solve
the Friedmann equations for the emergent metric, which is exactly the object being re-read here.
What changes is the ontology, and with it one clean, falsifiable observable:

$$\dot G/G\equiv0\ \text{exactly (rigid lattice)},\qquad\text{vs}\qquad \dot G/G=2H_0=1.379\times10^{-10}\,\text{yr}^{-1}\ \text{(a comoving lattice)}.$$

Because F79 makes $G=a^2c^3/(8\pi\sqrt3\hbar)$ *structural* (R18.9), a rigid $a$ forces $G$ to be
exactly constant, not merely slowly varying — a genuine zero with no parameter to absorb a
detection, already sitting three orders inside the Hofmann–Müller (2018) LLR bound
$|\dot G/G|<1.5\times10^{-13}\,\text{yr}^{-1}$.

A comoving mode has a fixed wavenumber in lattice units forever, so cosmological redshift on this
reading is a **gravitational/dielectric redshift** accumulated along the path, not a stretching of
the wave against a stretching ruler — the conformally-equivalent restatement of standard cosmology
(cf. Wetterich's "shrinking matter" frame), observationally identical to FRW by construction. On a
rigid lattice a comoving mode's wavelength in cells is fixed for all time, which removes the
trans-Planckian problem by construction (no mode was ever sub-cutoff) but for the identical reason
forbids expansion from ever *generating* modes — the primordial spectrum must be in the initial
state, because nothing in the substrate's dynamics could put it there later. This is Group D's
starting point.

The lattice is eternal and unchanging; the singularity the model has lives in the *emergent*
Schwarzschild metric (Chapter 19), not the substrate. The earliest epoch the lattice can resolve is
the one whose Hubble radius equals one cell ($R_H=c_\text{lat}/H=a$), giving, in reduced Planck
units,

$$H_\text{max}=\frac{c_\text{lat}}{a}=3^{-3/4}M_\text{Pl}=0.43869\,M_\text{Pl},\qquad t_\text{min}=\frac1{H_\text{max}}=3^{3/4}M_\text{Pl}^{-1}=\sqrt3\ \text{ticks (lattice-native)}.$$

Both statements are exact-algebraic and are unaffected by the SI-unit issue resolved in §20.2.4
below.

$$\boxed{\;\text{expansion}=K\text{'s conformal mode on a fixed substrate};\ \dot G/G\equiv0\text{ exactly (structural }G\text{, F79, + rigidity, F283)};\ H_\text{max}=3^{-3/4}M_\text{Pl},\ t_\text{min}=\sqrt3\text{ ticks (native, exact)}\;}\tag{R20.3}$$

(F284, checks §2–§9, 6/6 PASS; CL242, `open`, `exact`, `falsifier: unset`.)

#### 20.2.4 Resolving Chapter 19's forward-flagged F354/F284 tension

Chapter 19 (§19.6, item 3) forward-flagged two unresolved numerical conflicts between F354's
black-hole-core construction and this chapter's F284, both concerning the *SI translation* of
lattice-native quantities into the same units F354 uses for its own de Sitter-core estimates. Each
is examined here on its own merits, against both findings' own content and against
`test-results/F283_F284_lattice_elasticity.json` (the committed artifact).

**(a) The tick-duration $\sqrt3$ discrepancy — resolved; it is an arithmetic error in F284's own
SI conversion, not a genuine model inconsistency.** F107 derives, as part of the canonical SI
anchor (Chapter 18's R18.9 lineage), $\tau=a/(c\sqrt3)=2.05366\times10^{-43}$ s — the tick duration
implied by $a/\tau=c\sqrt3$, the relation that keeps the lattice-native $c_\text{lat}=1/\sqrt3$
(R6.5) consistent with the physical speed of light $c$. F284 states $t_\text{min}=\sqrt3$ ticks
(exact, native units, uncontested) and then reports its SI value as $t_\text{min}=6.161\times
10^{-43}$ s $=11.43\,t_P$ (confirmed against the committed artifact:
`F284_earliest_epoch/t_min_seconds = 6.160983552126205e-43`). But converting "$\sqrt3$ ticks" to
seconds means multiplying by the tick duration: $\sqrt3\times\tau_{F107}=\sqrt3\times2.05366\times
10^{-43}\text{ s}=3.5570\times10^{-43}\text{ s}$ — not $6.161\times10^{-43}$ s. The two numbers
differ by exactly $\sqrt3$ (confirmed: $6.161/3.557=1.7320$), which is precisely the discrepancy
Chapter 19 flagged and F354 itself named without resolving ("F107 gives $\tau_\text{tick}=
2.054\times10^{-43}$ s. F284 §5's SI $t_\text{min}=6.161\times10^{-43}$ s ... implies
$\tau_\text{tick}=a/c=3.557\times10^{-43}$ s. These differ by $\sqrt3$; one is wrong").

**F107 is the one that is right, and the resolution is clean rather than a coin-flip between two
live alternatives.** Two independent checks pin it down. First, algebraically: $t_\text{min}$
(the physical time for light to cross one cell of length $a$ at the physical speed $c$) must equal
$a/c$ by definition, and $a/c=\sqrt3\times[a/(c\sqrt3)]=\sqrt3\,\tau_{F107}$ — so F107's own $\tau$
convention, applied correctly, gives $t_\text{min}=a/c$ with no leftover $\sqrt3$ anywhere. Second,
and more tellingly, the corrected value satisfies a clean identity that F284's own erroneous number
does not: since $t_\text{min}=a/c$ and the Planck time is $t_P=\ell_P/c$, dividing gives
$t_\text{min}/t_P=a/\ell_P$ identically — the *same* dimensionless ratio $\sqrt{8\pi}\,3^{1/4}=
6.5978$ that F79/F107 already fix as the lattice-cell-to-Planck-length ratio (R18.9), for any
lattice, independent of $c_\text{lat}$ or the spatial dimension $d$. That is:

$$\boxed{\;t_\text{min}=\frac{a}{c}=\sqrt3\,\tau_{F107}=3.5570\times10^{-43}\ \text{s}=\frac{a}{\ell_P}\,t_P=6.5978\,t_P\;}\tag{R20.4a}$$

— a corrected value that is not merely "the other candidate" but the one forced by an identity
already established elsewhere in the tree, replacing F284's $t_\text{min}=6.161\times10^{-43}$
s $=11.43\,t_P$ (itself $\sqrt3\times6.5978=11.428$, confirming the erroneous extra factor
precisely). This chapter records the correction here and treats F284's exact-algebraic,
lattice-native content — $t_\text{min}=\sqrt3$ ticks, $H_\text{max}=3^{-3/4}M_\text{Pl}$ — as
entirely unaffected: the error is confined to one SI unit conversion in F284 §5/§9, not to any
structural claim of that finding.

**(b) The curvature-ceiling $24^{1/4}$ fork — a genuine, unresolved open question, logged
precisely rather than forced closed.** F183 (Chapter 19, R19.3) uses the convention
$K_\text{max}=1/a^4$ — a bare dimensional-analysis ceiling ("curvature saturates when it meets the
cell scale"), with coefficient exactly $1$, applied to the static Schwarzschild black-hole core's
Kretschmann scalar. F284's own earliest-resolvable Hubble rate $H_\text{max}=c_\text{lat}/a$
(R20.3 above), fed into the standard de Sitter Kretschmann formula $K=24H^4$, gives instead
$K_\text{max}=24/a^4$ (Chapter 19's own working, setting $H_\text{max}=1/a$ for the comparison) — a
factor $24$ larger in curvature, hence $24^{1/4}=2.2134$ larger in every derived length. F354
itself examined this directly (its own §7a) and concluded "only one can be fundamental," naming it
"an open decision deserving its own session" without adopting either.

Read against both findings' own content, **this is not a computational error in either finding —
it is an unforced identification.** F183's $1/a^4$ is a static-object convention (a compact-object
core cannot sustain curvature above the bare cell scale) applied in an entirely different physical
regime (a collapsed, essentially time-independent Schwarzschild interior) from F284's
$H_\text{max}=c_\text{lat}/a$ (a cosmological, dynamical quantity — the earliest Hubble rate a
rigid lattice can resolve, derived from setting the Hubble radius to one cell). Nothing in F178,
F183, or F284's own derivations asserts that a black-hole core's maximum sustainable curvature and
the curvature accompanying the earliest cosmological epoch must be numerically identical; they
answer different physical questions that happen to be expressed in the same currency ($1/a^4$).
The two conventions are self-consistent within their own domains, and this chapter cannot supply
the missing physical argument (a derivation that the model has exactly *one* universal curvature
ceiling, applicable identically to a static compact-object interior and a dynamical de Sitter-like
early epoch) that would force a choice between them — that argument does not exist anywhere in the
tree read for either chapter. What *can* be said, and is recorded as a mild point in the
$24/a^4$ convention's favor without adopting it as a decision this documentation-only chapter is
not entitled to make: F354's own §7a table shows the $24/a^4$ reading makes the core radius come
out to *exactly* one cell and the $E=1$ e-folding time come out to *exactly* $t_\text{min}$
(R20.3/R20.4a's own corrected minimum resolvable time) — a cleaner, P7-consistent coincidence than
$1/a^4$'s $2^{1/6}$ core-radius ratio. F354 also explicitly withdraws a tempting further
pattern-match: "the quarter-power-of-3 ladder tie to F284 ... the $24$ is the de Sitter Kretschmann
coefficient (pure GR), the $\sqrt3$ is $1/c_\text{lat}$; unrelated origins" — so the two numbers in
this fork ($24$ and $\sqrt3$) do not share a common origin that could resolve the question by
unification.

> **Gap [G-12].** *(Numbered G-12, not G-11, because Chapter 13b — built concurrently — independently
> claimed [G-11] for its own gap; see `docs/monograph/GAPS.md`'s "Chapter 13b" entry.)* The
> curvature-ceiling convention conflict between F183 ($K_\text{max}=1/a^4$,
> used for the Chapter 19 black-hole core) and the literal de Sitter curvature implied by F284's
> own $H_\text{max}=c_\text{lat}/a$ ($K_\text{max}=24/a^4$) is a genuine, unresolved open question
> in the model's own conventions — not a computational error in either finding, and not
> resolvable from the two findings' existing content, because neither derives (nor claims to
> derive) that a single universal curvature ceiling must govern both a static compact-object core
> and a dynamical cosmological epoch. F354 (Chapter 19, §7a) already identified the fork and its
> exact factor ($24^{1/4}$ in every derived length) and explicitly declined to adopt either
> reading, naming it "an open decision deserving its own session"; this chapter's own read of
> F183/F284/F354 together does not turn up a way to close it either, beyond noting (without
> adopting) that the $24/a^4$ convention makes two of F354's own numbers (the core radius, the
> $E=1$ e-folding time) come out as clean multiples of the model's already-established scales.
> Flagged here per the same discipline as Gaps G-6/G-7/G-9: recorded rather than silently
> resolved by fiat. A future session that wants a single universal curvature ceiling for the model
> would need to either derive one from the lattice's own dynamics (not from dimensional analysis in
> either domain) or explicitly adopt one of the two existing conventions by decision, the way F178
> adopted the full-tensor source. The tick-duration half of the same Chapter-19 forward flag (item
> (b) in that chapter's §19.6.3) is resolved above (§20.2.4a), not left open here.

$$\boxed{\;\text{tick-duration }\sqrt3\text{ discrepancy: RESOLVED — F284's SI conversion had a spurious extra factor of }\sqrt3\text{; corrected }t_\text{min}=a/c=6.5978\,t_P.\ \text{Curvature-ceiling }24^{1/4}\text{ fork: genuinely OPEN (Gap G-12) — two self-consistent conventions in two different physical regimes, no finding forces a single universal ceiling}\;}\tag{R20.4}$$

### Group B — Is the lattice itself elastic or rigid, and does it matter?

#### 20.2.5 F283 — an elastic lattice is excluded four ways, and cannot rescue F282

F282 (below) turns on one number, $r=\sqrt3>1$. The obvious rescue is to make the lattice spacing
smaller and push the cutoff above $M_\text{Pl}$. **It does not work, exactly, because F79 ties $G$
to $a^2$.** Under any stretch $a\to sa$ (constant or dynamical), $M_\text{Pl}=3^{1/4}\hbar/(sac)$
and $\Lambda_\text{UV}=\hbar/(sac)$ scale identically as $1/s$, so
$$\frac{M_\text{Pl}}{\Lambda_\text{UV}}=3^{1/4},\qquad r=\frac{M_\text{Pl}^2}{\Lambda_\text{UV}^2}=\sqrt3=\frac1{c_\text{lat}}\qquad\text{for every }s,\qquad \frac{\partial r}{\partial s}\equiv0$$
(exact, sympy, every symbol kept free). $M_\text{Pl}$ is not an external yardstick in this model —
it *is* a lattice quantity, because $G$ is structural — so the inflation obstruction is a **scale-free
geometric invariant of the BCC coordination geometry** ($1/c_\text{lat}$, from the $d=3$
eight-neighbour Weyl walk), not a statement about how big $a$ happens to be. This directly corrects
F282's own falsifier 5, which had claimed the opposite.

Three further, independent arguments close off elasticity even considered on its own terms. **A
dynamical stretch is a varying $G$**, and $\dot G/G=2qH_0$ for stretch exponent $q$ (rigid: $q=0$;
comoving: $q=1$); LLR and BBN independently bound $q\lesssim10^{-3}$, with a fully comoving
lattice missing the BBN bound by 17 decades. **The volume mode is not a new field — it is $\ln K$**,
already shown by F79/F180/F216 to be sourced, potential-free, and carrying exactly 2 propagating
degrees of freedom in vacuum (no independent scalar mode to be the elastic degree of freedom); the
only alternative (a genuinely new scalar) is Cassini-bounded at a coupling $295\times$ weaker than
gravity itself. **A tree-level elastic stiffness would give gravity a second light cone**, since
F180 *derives* rather than posits $c_\text{grav}=c_\text{lat}$ from the induced matter loop;
GW170817 bounds any such tree fraction at $\lesssim6\times10^{-15}$.

$$\boxed{\;r=\sqrt3=1/c_\text{lat}\text{ invariant under any stretch }a\to sa\text{ (exact, }\partial r/\partial s\equiv0\text{); }\dot G/G\lesssim10^{-3}\times2H_0\text{ (LLR+BBN); volume mode}=\ln K\text{, no new field; tree elastic fraction}<6\times10^{-15}\text{ (GW170817)}\;}\tag{R20.5}$$

(F283, checks E1–E4, 8/8 PASS; CL241, `open`, `exact`, `falsifier: unset`.)

### Group C — The inflation no-go

#### 20.2.6 F282 — no slow-roll inflaton exists, sub-Planckian cutoff forces it

F282 turns the completeness-report question ("does the model admit inflation, and if not, why
not") into an exact theorem. Because F79/F107 fix $a/\ell_\text{red}=3^{1/4}$ in *reduced* Planck
units ($\sqrt{8\pi}$ cancels between the non-reduced $\ell_P$ that $a$ is measured against and the
reduced $M_\text{Pl}$ that slow roll is conventionally written in), the lattice's own UV cutoff is
sub-Planckian, exactly:
$$\Lambda_\text{UV}=\frac1a=\sqrt{c_\text{lat}}\,M_\text{Pl}=0.75984\,M_\text{Pl},\qquad r_\text{min}\equiv\frac{M_\text{Pl}^2}{\Lambda_\text{UV}^2}=\sqrt3=\frac1{c_\text{lat}}.$$
Every per-cell state (unit spinors, $SU(2)$ links, compact angles) is **bounded** — there is no
non-compact scalar to run up — so every candidate field's canonically normalized decay constant is
$f=\sqrt J/a$ with $J$ the dimensionless lattice stiffness, and every slow-roll parameter carries
the universal prefactor $r=M_\text{Pl}^2/f^2=\sqrt3/J$. With $J=O(1)$ read off the model's entire
computed coupling range ($[0.16,2.4]$, from the $E_g$ hat's own F118 couplings), the model's two
genuine scalar directions — the $E_g$ clock angle ($K_\text{clock}=9$, exact, amplitude-independent)
and the $E_g$ radial magnitude ($K_\text{radial}=5.92$, on F193-forced boundary conditions) — both
fail slow roll by $O(10)$, agreeing to within a factor 1.5. Every standard escape route is closed
by an already-established finding or by data: Starobinsky $R^2$ (needs a tree-level coefficient
$9.67$ decades above what F79's zero-tree-stiffness theorem allows), N-flation ($\sim780$
independent scalar directions needed, the model has 2), the conformal mode $\ln K$ (potential-free
by F180/F216), gauge/Stueckelberg phases (forbidden by gauge invariance), and causal seeds
(excluded by acoustic-peak coherence). The identical obstruction reappears in the model's own
measured RG spectrum (F130): the nearest scaling exponents to marginal are $+1$ (confinement) and
$-2$ (deconfinement/LIV) — an $O(1)$ gap with nothing nearly-marginal to be a slow-roll field.

$$\boxed{\;\Lambda_\text{UV}=\sqrt{c_\text{lat}}\,M_\text{Pl}\text{ exactly (sub-Planckian, }3^{1/4}\text{ in reduced units); }r_\text{min}=\sqrt3=1/c_\text{lat}\text{; every compact field candidate fails slow roll by }O(10)\text{; every standard escape closed}\;}\tag{R20.6}$$

(F282, checks §2–§7, 7/7 PASS; CL240, `open`, `exact`, `falsifier: unset`.)

#### 20.2.7 F363 — re-examination one month later: the no-go survives, two more escape classes closed

A dedicated K4 re-examination confirms `a_over_ellP` has not moved (re-verified to $10^{-12}$, and
continuously covered by three unrelated gate-tier records — F357, F359, F362 — that would go red
on any drift) and that no new compact-direction candidate with anomalously large stiffness has
appeared among every finding filed since F282. Two further literature-suggested escape classes are
checked and closed for a *categorically different* reason than F282's original three (which failed
quantitatively, by 9–400$\times$): **axion monodromy** needs an external flux/brane/discrete-charge
construction the model does not contain — and the one genuine discrete holonomy the model does own
on this shell (F253's $2\pi/3$ $E_g$ rotation) is checked directly and found to be the wrong kind
of object (period-setting, not an unwinding charge). **Torsion/DBI-style kinetic enhancement**
needs a dynamical, propagating torsion field with a Nieh–Yan coupling; the model's actual torsion
sector (F63) is algebraically eliminated in favor of a four-fermion contact term and carries no
such coupling. One new, previously-unnamed assumption is surfaced rather than closed: whether the
$E_g$ doublet's kinetic term is exactly canonical is assumed throughout F282's construction and
never independently derived from a second-shell lattice action — flagged as the sharpest concrete
thread for a future session, precisely because closing it would use only content the model already
has.

$$\boxed{\;\text{no-go re-verified, unmoved after one month; axion monodromy and torsion/DBI kinetic enhancement both closed for want of field content the model does not contain; canonical-kinetic-term assumption named as the sharpest open thread}\;}\tag{R20.7}$$

(F363, re-verification + literature review, 9 PASS/4 WEAKENS on its own attack pass, CONFIRMED-NARROWER; no test record — analysis-only; shares CL240 with F282, no separate card.)

### Group D — The primordial tilt / structure-formation puzzle

#### 20.2.8 F285 — all three initial-condition measures close; the tilt, not the scale invariance, is the hard part

Via the model's own Poisson law (R18.11, $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$), the entire question
"what is the primordial spectral index" reduces to "what is the large-scale slope of the initial
energy-density power spectrum," since $P_\rho(k)\propto k^{n_s}$ follows directly. Every
short-range-correlated measure on the $t{=}0$ state — uniform/maximum-entropy, thermal, gapped, or
(F285's own, later corrected by F310 — see below) a critical Gaussian field squared — collapses
under convolution to white noise, $n_s=0$, excluded at $230\sigma$. Local conservation
(Traschen's integral constraints) forces $n_s=4$, excluded at $723\sigma$. The one principled
scale-free choice on the metric itself gives exactly $n_s=1$ — Harrison–Zel'dovich — excluded at
**8.4$\sigma$** by Planck. **The hard fact is not that the spectrum is nearly scale-invariant; it
is that it is not exactly scale-invariant.** The Brillouin-zone edge sits 58.26 decades above the
CMB pivot and, because the lattice is rigid (F284), permanently so — this route is closed for good,
not merely for now. Block-spin (F130) preserves the exponent of any power law exactly under
Kadanoff dilation, so the spectral index is an *exactly marginal label* on a line of fixed points —
explaining why $P(k)$ should be a power law at all (a genuine, non-trivial fact) while being
structurally incapable of selecting which power.

$$\boxed{\;P_\rho\propto k^{n_s}\text{ (Poisson bridge, exact); white noise/conserved-causal measures give }n_s=0,4\text{ (230}\sigma,723\sigma\text{); scale-free-in-metric gives }n_s=1\text{, excluded at }8.4\sigma\text{; BZ edge permanently closed (58 decades, rigid lattice); block-spin: exponent exactly marginal}\;}\tag{R20.8}$$

(F285, checks D1–D3, 7/7 PASS; CL243, `open`, `exact`, `falsifier: unset`.)

#### 20.2.9 F286 — a second scale must be a logarithm, not a length; the tilt is natural in size

F286's classification theorem uses Planck's own measured *running*, $dn_s/d\ln k$, to constrain the
*shape* of any second-scale mechanism rather than its distance: for $n_s-1=F(k\xi)$, a power-law
shape $F=Cx^p$ (any physical length $\xi$) forces $|d\ln F/d\ln x|=p$, and Planck's running bounds
this at $<0.32$ — excluding every integer $p\ge1$, i.e. every candidate length scale, by shape
rather than by how far away it sits (a strictly stronger closure than F285's 58-decade argument).
Only a log-type mechanism, $F=C/L$ with $L=\ln(k_\text{UV}/k)$, survives, and the whole class
predicts, parameter-free (reusing F285's own 58.26-decade separation), $dn_s/d\ln k=-(1-n_s)/L=
-2.62\times10^{-4}$ — currently 25.6$\times$ below Planck's own error, a genuine future target.
The required coefficient $C=(1-n_s)L=4.71$ is an ordinary $O(1)$ number: **the tilt is not
unnaturally small; the missing ingredient is a running coupling, and the model has none evaluable
at CMB momenta** — $\alpha$ is 30$\times$ too small, $\alpha_s$ is 38 decades into confinement at
CMB energies, $G$ does not run (F284's own sharpest prediction removes the most natural candidate),
and block-spin's exactly-marginal exponent (F285) cannot move by construction. A tempting numerical
near-miss, $1-n_s\approx\delta^*/2\pi=1/(9\pi)$ at $0.064\sigma$, is checked against a
pre-registered look-elsewhere family (396 candidates, small rationals times integer powers of
$\pi$) and found to be one of six comparably-close hits ($p=0.32$ chance of at least one this
close) — recorded, per the F253/F256 coincidence discipline, as not evidence.

$$\boxed{\;\text{length scales excluded by shape (}|d\ln F/d\ln x|<0.32\text{); log class predicts }dn_s/d\ln k=-2.62\times10^{-4}\text{, parameter-free; required coefficient }C=4.71\text{ is }O(1)\text{; no model coupling supplies the log; }\delta^*/2\pi\text{ coincidence rejected, }p=0.32\;}\tag{R20.9}$$

(F286, checks T1–T5, 7/7 PASS; CL244, `open`, `exact`, `falsifier: unset`.)

#### 20.2.10 F295 — correction: the tilt can be a scale-free anomalous dimension, needing no second scale at all

Testing whether freeing the two adopted external constants ($\alpha$, $G$) could narrow F286's
loop exposes that neither can — $\alpha$ would need a scale 68.1 decades above the model's own
cutoff, $G$'s coupling is a *power* ($p=2$) already excluded on shape by F286 T1 before magnitude
is even considered — but the exercise surfaces that **F286 mis-read its own theorem**. T1's bound
$|d\ln F/d\ln x|<0.32$ *allows* $p=0$, and F286 had dismissed this as the trivial case; it is not.
A constant $F$ is a scale-free **anomalous dimension** $\gamma$: $n_s-1=-2\gamma$, giving
$dn_s/d\ln k\equiv0$ exactly — no second scale required at all, more consistent with Planck's
null-running measurement than the log class, and identical to F285's D3 marginal label on the line
of fixed points ($\gamma$ *is* that label). This repairs F285's own reading of its row 2: Planck's
8.4$\sigma$ exclusion of exact scale invariance is the *positive* statement $\gamma=(1-n_s)/2=
0.01755\ne0$, not a dead end. The two sub-classes (constant-$\gamma$ vs. log-type) separate only at
$\sigma\sim2.6\times10^{-4}$ running — beyond current reach, but a real, registered discriminator.
A constant $\gamma$ needs a coupling that is scale-*independent* — exactly what a pure
group-theoretic representation weight supplies, and $g_\text{eff}=0.2205\pm0.0264$ lands at $2/9=
0.2222$, $0.064\sigma$ away (the same value appearing independently as $\delta^*$, $\sin^2\theta_W$
on-shell, and $c_\text{Fierz}^\text{colour}$). This is named a **shape-justified target, not a
derivation**: no operator has been identified, the look-elsewhere count (F286 T5) applies unchanged
to the value, and picking one of the three separately-registered $2/9$'s is most of the remaining
work.

$$\boxed{\;p{=}0\text{ is a scale-free anomalous dimension }\gamma\text{, }dn_s/d\ln k\equiv0\text{ exactly, identical to F285's marginal label; F285's 8.4}\sigma\text{ exclusion becomes the positive statement }\gamma=0.01755\ne0\text{; }g_\text{eff}\text{ vs }2/9\text{ at }0.064\sigma\text{ is a shape-justified target, not a derivation}\;}\tag{R20.10}$$

(F295, checks A1–A4, 8/8 PASS; CL248, `open`, `exact`, `falsifier: unset`.)

#### 20.2.11 F296 — a published home: holographic cosmology names the operator, and validates F286's instrument by retrodiction

F295's structure — a scale-free anomalous dimension with no inflaton — is not idiosyncratic: it is
exactly holographic cosmology's own defining move, an established (2009–) framework computing
$n_s-1$ from a three-dimensional QFT with no gravity and no inflaton. **F286's own T1 diagnostic,
built from Planck's running alone with no knowledge of this literature, retrodicts holographic
cosmology's own published tension**: evaluated on the McFadden–Skenderis/Afshordi et al. fitted
spectrum, T1 returns $0.675$ against its own $0.32$ bound (2.1$\times$ over), implying
$dn_s/d\ln k=+0.0151$ — a $2.92\sigma$ tension with Planck that lands squarely on the published
$2.2\sigma$ global disfavour. This is a genuine independent validation of an instrument this
register had already built for a different purpose. The model's own structure (constant-$\gamma$,
requiring a dimensionless dual coupling) sits precisely in the branch — $f_1=0$, conformal —
that the founding PRL's own footnote states is unanalysed: an opening, not a re-tread. The operator
F295 could not name is named externally: the trace of the 3D stress tensor, $T^i{}_i$. But the
naive realization — reading the model's own 48 Weyl fermions and 2 real scalars as the dual's field
content — fails decisively: the resulting tensor-to-scalar ratio, $r=0.32$–$0.97$ depending on
scalar coupling, is excluded by BICEP/Keck's $r<0.036$ by $9$–$27\times$, matching the literature's
own independent exclusion of fermion-only duals.

$$\boxed{\;\text{F286 T1 retrodicts HC's published }2.2\sigma\text{ tension (computed }2.92\sigma\text{); model's branch is HC's own stated-unanalysed }f_1{=}0\text{ conformal case; operator named}=T^i{}_i\text{; naive field-content-as-dual reading excluded by }9\text{--}27\times\text{ via }r\;}\tag{R20.11}$$

(F296, checks L2–L5, 7/7 PASS; CL249, `open`, exactness `unset`, `falsifier: unset`.)

#### 20.2.12 F310 — no 3D dual is needed: the automaton's own $t{=}0$ state IS a 3D Euclidean measure

F310 dissolves rather than closes F296's failure. Holographic cosmology reaches for a 3D dual QFT
by an explicit bulk/boundary dictionary; this model does not need one, because on a **rigid** 3D
lattice (F284/P1) the $t{=}0$ state literally *is* a probability measure on 3D field
configurations — a 3D Euclidean statistical field theory by construction, with F285's own Poisson
bridge already making the primordial spectrum that measure's energy–energy correlator. This is
what repairs F296's $r$-exclusion: the failed $9$–$27\times$ bound was a property of HC's
*dictionary* (how a 4D tensor mode is read off a 3D correlator), and with no dictionary needed,
that formula simply does not apply here. The load-bearing identity: reading $T^{00}$ as the 3D
statistical energy operator with scaling dimension $\Delta_\varepsilon=d-1/\nu$ ($\nu$ the thermal
RG eigenvalue) gives, identically (sympy, literal zero),
$$n_s=3-\frac2\nu\qquad\Longrightarrow\qquad \gamma\equiv\frac{1-n_s}2=\nu^{-1}-1\text{'s partner statement},\ \gamma\equiv y-1,\quad y\equiv1/\nu.$$
**The tilt's anomalous dimension is the anomalous part of the model's own block-spin relevant
eigenvalue** — an in-model identification, where F296's was external. This explains, in one
sentence, why every earlier route failed: an anomalous dimension is by definition a non-integer RG
exponent, and F130's entire measured Kadanoff spectrum is integers ($b^0$ marginal, $b^{+1}$
relevant, $b^{-n}$ irrelevant) — a linear block average is a Gaussian calculation, and Gaussian
calculations cannot generate anomalous dimensions. Running F130's own measured $y=1$ (the
large-$N$/spherical-model fixed point) through the identity gives $n_s=1$ exactly — **the model's
own measured RG predicts Harrison–Zel'dovich, and the data excludes it at $9.4$–$9.9\sigma$
across three datasets**, re-deriving F285's headline from the RG side rather than the measure side.
Along the way F285's own row 2 is corrected in its own favor: a *critical* Gaussian field squared
does not collapse to white noise (its power spectrum is not integrable), giving $n_s=-1$ exactly,
strengthening rather than weakening F285's conclusion.

The identity reading also makes the one genuinely zero-parameter prediction in this entire
group: in any conformal field theory the stress tensor's dimension is *protected* by its own
conservation ($\Delta_T=d$ exactly), while the energy operator's is not — so
$$n_t=2\text{ exactly (a strongly blue tensor spectrum)},\qquad \log_{10}r(k_*)\approx-118.$$
This does not merely survive the test that killed the naive dual reading (§20.2.11); it predicts
the model can **never** produce an observable primordial tensor mode — a prediction every future
CMB-polarization experiment simply confirms by finding nothing, forever. The honest residual: no
model field count (48 Weyl fields, 96 fermionic modes, 110 with gauge+scalars, 192 Grassmann
components) lands inside $1\sigma$ of the $N\approx63$–$81$ a large-$N$ estimate of the required
finite-size correction would need — a declared, asserted-not-a-hit target, in the same discipline
as F286's rejected coincidence.

$$\boxed{\;\text{no 3D dual needed}-t{=}0\text{ state IS a 3D Euclidean measure; }\gamma\equiv y-1\text{ identically (sympy); F130's integer RG spectrum explains every prior failure; }y{=}1\Rightarrow n_s{=}1\text{, excluded }9.4\text{--}9.9\sigma\text{; }n_t=2\text{ exact, }r\sim10^{-118}\text{, repairing F296's exclusion}\;}\tag{R20.12}$$

(F310, checks C1–C8, 16/16 PASS, two controls verified red; CL267, `contingent`, `exact`,
`falsifier: stated`.)

#### 20.2.13 F288 — structure formation: zero free functions where the EFT of dark energy has two

Placed logically here (rather than split off toward F182/F188) because it is the point where the
gravity sector, not the initial spectrum, does the work: linear structure formation is governed in
general by two free functions $\mu(a,k)$ and $\Sigma(a,k)$ (respectively the effective Newton
constant felt by matter and the lensing potential's own effective source), and this model fixes
both to exactly $1$ from three structurally independent, already-established facts: $\mu=1$ with
$\partial_k\mu\equiv0$ (F106/F178's Poisson reduction, sympy zero), $\partial_a\mu=0$ ($G$
structural on a rigid substrate, F79/F284's own $\dot G/G\equiv0$), and $\Sigma=1$ (F64's impedance
lock $AB\equiv1$, the identical condition behind PPN $\gamma=1$, sympy zero). Three distinct
sources closing two functions with no fitted parameter left is the count the whole model is judged
against here. Two exact consequences follow: the growth index $\gamma_g=6/11$ (forced *iff*
$\mu=1$, not a free fit as in general modified gravity), and a literal-zero-residual Meszáros
solution $D(y)=1+\tfrac32y$ across the radiation era — the one place the transfer function's shape
is derived rather than imported. Against real data, $D(1)$ matches Carroll–Press–Turner to
$0.10\%$, $f\sigma_8$ against seven RSD points gives $\chi^2/N=1.012$, and $\sigma_8=0.8204$,
$S_8=0.8410$ ($+1.15\%$ vs. Planck) — reported with its full import budget in the same table,
since $A_s$ and the EH98 transfer-function coefficients are declared free/imported, not derived.
The model has **no screening mechanism** because $\mu\equiv1$ is $k$-independent by derivation, so
it cannot relieve the S8 tension the way a generic modified-gravity theory could: DES Y6's
$S_8=0.789\pm0.012$ sits at $3.00\sigma$ from the model's prediction, with nothing to tune —
a falsifier that can genuinely fire, distinct from the combined-CMB and KiDS-Legacy comparisons
(both under $1.2\sigma$).

$$\boxed{\;\mu=\Sigma=1\text{ exactly, from three independent sources — zero free functions where the EFT of dark energy has two; }\gamma_g=6/11\text{ exact; Meszáros literal-zero residual; }\sigma_8=0.8204\ (+1.15\%);\ \text{no screening} \Rightarrow \text{DES Y6 at }3.00\sigma\text{, a real falsifier}\;}\tag{R20.13}$$

(F288, checks S1–S3/D1–D5/B1–B2/C1, 13/13 PASS; CL254, `live`, `exact`, `falsifier: stated`.)

### Group E — Big Bang nucleosynthesis and the model's own thermal content

#### 20.2.14 F309 — $g_*(T)$ over the model's own 48 Weyl fields: the branch-odd term carries 3/7 of the fermionic lattice correction

Closing the one import F297 (below) inherited — a Standard-Model relativistic degree-of-freedom
count — F309 computes $g_*(T)$ directly from the model's own field content. The single-Weyl BCC
dispersion splits into a branch-even softening term (the photon's own anisotropy, inherited with a
factor 4 because the photon's constituents carry $\mathbf k/2$) and a branch-odd term that a
first-order argument would expect to cancel (it averages to zero by parity, and is exactly what
the paired-spinor photon construction *does* cancel — F67/F68 non-birefringence read from the
thermodynamic side). It does not cancel for a lone fermion: its *square* enters the equation of
state at the same order as the anisotropic term, carrying **3/7 exactly** of the total fermionic
lattice correction — a route a first-order argument would have missed entirely. $C_u/C_w=15/2$
survives as a genuine homogeneity theorem (true term-by-term for both the anisotropic and
branch-odd channels separately, independent of statistics), and the fermion/photon coefficient
ratio factorizes cleanly as $31/4=7\times31/28$ (pure geometry times pure Fermi/Bose statistics).

Assembling the model's own content (48 Weyl fields, forced by two independent zero-reasons to
exclude $\nu_R$ — $Y=0$ forced by anomaly cancellation, and a heavy Majorana mass — and by the
Higgs-free construction to exclude the $E_g$ doublet as a light thermal species) reproduces exactly
F297's assumed BBN bath: $g_*(10\text{ MeV})=10.7493$, converging to $g_*\to3.363$ against the
textbook $2+\tfrac{21}4(4/11)^{4/3}=3.3626$ endpoint to $10^{-4}$. **The content F297 assumed is
the content the model derives** — a null result that is nonetheless a genuine closure, since
excluding $\nu_R$ thermalization ($\Delta g_*=+5.25$, a $48.8\%$ shift, if it occurred) turns into
a new BBN-derived lower bound $m_{E_g}>125.5$ MeV once the $E_g$ doublet's own mass (still
undetermined anywhere in the tree) is priced back in at the level $\Delta g_*<10^{-3}$. The one
non-null substitution is the electron mass itself: re-running BBN on the model's own $m_e=0.51069$
MeV (F121, $-0.0605\%$ from PDG) rather than PDG moves $Y_p$ and D/H both **toward** the
observations, by $+0.032\sigma$ and $+0.009\sigma$ respectively — not evidence, but an honest,
correctly-scoped removal of an input.

$$\boxed{\;g_*(10\text{ MeV})=10.7493\text{ from the model's own 48 Weyl fields, matching F297's assumed content exactly; branch-odd term carries }3/7\text{ of the fermionic correction (a route missed at first order); }m_{E_g}>125.5\text{ MeV new BBN-derived bound; own }m_e\text{ moves }Y_p,\text{D/H toward data by }+0.03\sigma\;}\tag{R20.14}$$

(F309, checks GS-1–GS-13, 14/14 PASS, two controls verified red; shares evidence chain with CL266, `live`, `quantitative`, `falsifier: stated`.)

#### 20.2.15 F297 — BBN on the model's own expansion law: the light elements come out right, and the model measures $m_n-m_p$ 179$\times$ more sharply than the matter sector checked it

Assembling BBN entirely from parts the tree already owned — the structurally derived $G$ (Chapter
18), the full-tensor source law's pressure-weighted expansion ($\kappa=2$ for radiation, giving
$H^2=(8\pi G/3)\rho$ exactly, versus $\kappa=1$ for the demoted energy-only law's $41\%$-too-slow
expansion), $\dot G/G\equiv0$, and $N_\text{eff}=3.044$ (three left-handed neutrinos and nothing
else, forced by the model's own hypercharge/Majorana structure) — reproduces the standard-BBN
light-element yields validated against a PRIMAT-class reference to $\lesssim1\%$ on three of four
species, and confirms **BBN independently discriminates the F178 gravity-law decision on a
completely different observable from the one that decided it**: the demoted energy-only law gives
$Y_p=0.1856$, excluded at $17.6\sigma$ by Aver et al. 2021, where the full-tensor law's $Y_p=0.2449$
sits at $-0.11\sigma$.

The sharpest result is a bound on the matter sector, not a cosmology result at all. Because $Y_p$
and the free-neutron lifetime are both extremely steep functions of $\Delta m=m_n-m_p$, BBN pins
$$\Delta m = 1.293\pm0.0056\ \text{MeV (1}\sigma\text{)}$$
— **179$\times$ tighter** than F122's own $\pm1$ MeV acceptance criterion for the model's derived
splitting. Fed the model's own value ($\Delta m=1.51$ MeV, $+2.51-1.00$ MeV strong-minus-EM,
F122/F123), the naive comparison against this band gives $Y_p=0.1210$ ($-36.6\sigma$) and a
predicted free-neutron lifetime of 330.8 s against the measured $878.4\pm0.4$ s (factor 2.7) — a
striking, quantified tension this chapter's §20.2.17 (F372) revisits and substantially resolves.
$N_\text{eff}=3.044$ against Planck's $2.99\pm0.17$ is a genuine, parameter-free prediction with a
sharp falsifier: any renormalizable $\nu_R$ coupling would add $\Delta N_\text{eff}=1.71$, excluded
at $>10\sigma$.

$$\boxed{\;\text{BBN light elements reproduced to }\lesssim1\%\text{ (validated against PRIMAT); full-tensor law confirmed on an independent observable (energy-only excluded at }17.6\sigma\text{); }N_\text{eff}=3.044\text{ parameter-free; BBN measures }\Delta m=1.293\pm0.0056\text{ MeV, }179\times\text{ tighter than the matter-sector's own check}\;}\tag{R20.15}$$

(F297, checks K2-1–K2-12, 12/12 PASS; CL258, `contingent`, `quantitative`, `falsifier: stated`.)

#### 20.2.16 F361 — the A=7 rate-fit repair: Li7/H moves from $-92\%$ to $-6.3\%$

The one species F297 explicitly declared broken and excluded from its own check battery — the
$A=7$ lithium/beryllium chain, off by nearly an order of magnitude — turns out to be a
**transcription bug against the implementation's own cited source**, not a physics gap. Diffing
the model's `_rate_fits` term-by-term against Kawano's reference NUC123 Fortran code (the primary
source both this module and Smith–Kawano–Malaney 1993 derive from) finds all five $A=7$-adjacent
reaction fits mistranscribed — missing narrow-resonance terms, a garbled/mis-slotted coefficient,
or (for $^7\text{Be}(n,\alpha)^4\text{He}$) an outright wrong functional form (increasing rather
than decreasing in temperature). Repairing all five against the primary source directly takes
$^7$Li/H from $-92\%$ to $-6.28\%$ against the same PRIMAT-class reference the other three species
already validate on — now inside a declared $\pm10\%$ band and included in the check battery as
K2-13. The other three abundances shift only at the $10^{-9}$–$10^{-5}$ relative level (a coupled
network, not twelve independent reactions), confirming the repair is scoped correctly and does not
disturb F297's own headline. $\dot G/G\equiv0$ is additionally registered as a **BBN-internal
consistency check** — honestly scoped, after this finding's own attack pass, as a check that the
assumption is *consistent with* the data rather than a new independent measurement, since the code
is structurally incapable of returning $\dot G\ne0$ by construction.

$$\boxed{\;\text{five }A{=}7\text{ reaction fits mistranscribed against their own cited source (NUC123); repaired: Li7/H }-92\%\to-6.3\%\text{, now validated (K2-13); other three species shift}<2\times10^{-5}\text{ relative; }\dot G/G\equiv0\text{ registered as a BBN-internal consistency check, not a new bound}\;}\tag{R20.16}$$

(F361, checks K2-1–K2-13, 13/13 PASS, one control verified red; CL258 updated in place.)

#### 20.2.17 F372 — the significance, not the physics, was wrong: BMW 2015 and the model's own P2 wavefunction both confirm F122's decomposition; a properly propagated theory uncertainty brings the "$36.6\sigma$" down to $\sim0.8$–$2\sigma$

F297's own next-step item — fix the EM self-energy or show the strong-sector gap moves, to close
the 0.217 MeV needed to match BBN's $\Delta m=1.293\pm0.0056$ MeV — fails on both branches when
checked against independent, non-tuned sources. The EM term ($1.00$ MeV, an *ad hoc* classical
estimate) is confirmed to $3$–$4\%$ by three independent methods sharing no common fit: the
model's own P2 three-body wavefunction, recomputed pairwise with zero new free parameters ($0.968$
MeV); ab initio lattice QCD+QED (BMW 2015, $-1.00(07)(14)$ MeV); and a dispersive Cottingham
sum rule (Thomas–Wang–Young 2015, $1.04\pm0.11$ MeV). The strong (current-quark) term is confirmed
similarly: PDG 2024's updated quark masses shift $m_d-m_u$ by only $0.8\%$, and BMW 2015's own
ab initio QCD piece matches the model's $+2.51$ MeV to the digit. **Neither term is the culprit —
what F297 actually needed was the *theoretical estimate's own uncertainty*, which it implicitly
took as zero.** Borrowing BMW 2015's own combined uncertainty, $\sigma_\text{theory}=0.280$ MeV
(justified because F372's own independent checks show the model tracks BMW's terms to $\le1\%$),
the significance collapses:
$$\sigma_\text{naive}=\frac{1.51-1.29333}{0.0056}=38.7\qquad\longrightarrow\qquad\sigma_\text{theory-aware}=\frac{1.51-1.29333}{0.280}=0.77.$$
A sensitivity check across several legitimate ways to compose the theory uncertainty (using only
numbers already cited) gives a range $0.77$–$1.97\sigma$ — **not excluded at every composition
tried**, though the margin is materially thinner than a single comfortable number would suggest.
The neutron lifetime and $Y_p$ both land inside their $\pm1\sigma$ bands once the $\pm0.280$ MeV
theory uncertainty is propagated through unmodified. What this does **not** claim: a corrected
value of $m_n-m_p$ — F122/F123's $+1.51$ MeV stands exactly as computed, now with an honest
uncertainty attached rather than an implicit zero.

$$\boxed{\;\text{EM term confirmed 3-4\% by three independent methods (P2 pairwise, BMW 2015, dispersive sum rule); strong term confirmed by PDG 2024 and BMW 2015; the naive }38.7\sigma\text{ exclusion used the OBSERVABLE's precision, not the ESTIMATE's own uncertainty; theory-aware significance }0.77\text{--}1.97\sigma\text{, not excluded}\;}\tag{R20.17}$$

(F372, checks K2-14/K2-15, 15/15 PASS, one control verified red; CL259, `narrowed`, `quantitative`, `falsifier: stated`.)

#### 20.2.18 F369 — toward a model-native transfer function: the sound horizon lands 0.11% from Planck

Scoping what a full replacement of the imported EH98 transfer function would need (a complete
photon–baryon–CDM Boltzmann hierarchy — genuinely several sessions of work, not attempted), F369
extracts the two pieces reachable with content the model already owns. **The comoving sound
horizon**, integrated directly on the model's own confirmed multi-component background (F182/F188)
rather than EH98's closed-form fitting approximation, lands $146.923$ Mpc against Planck's
$r_\text{drag}=147.09$ Mpc — $-0.114\%$, a $16.4\times$ improvement over the fitting formula
already in the tree (honestly scoped as substantially an internal-consistency check, since both
sides share the same Planck-fit background parameters). **The hydrogen recombination redshift**,
from the plain Saha equation using the model's own Rydberg energy (F125) and BBN baryon-to-photon
ratio, reproduces the textbook $\sim26\%$ equilibrium-approximation bias against Planck's true
$z_*$ — not a defect, the well-known Saha-vs-true discrepancy the Peebles non-equilibrium
correction closes, honestly reported rather than hidden. Substituting the model-native sound
horizon into F288's $\sigma_8$ calculation moves the result by only $0.013\%$ — two orders below
the $\approx1.15\%$ residual itself — which **localizes** that residual away from the sound-horizon
scale (which the model reproduces well) and onto EH98's still-imported acoustic-wiggle and
Boltzmann-calibrated envelope functions, precisely where a future full solver would need to focus.

$$\boxed{\;\text{model-native sound horizon: }-0.114\%\text{ vs Planck, }16.4\times\text{ better than the imported fit; Saha recombination reproduces the known }\sim26\%\text{ equilibrium bias from the model's own Rydberg energy; }\sigma_8\text{ residual localized away from the sound horizon, onto the still-imported acoustic envelope}\;}\tag{R20.18}$$

(F369, checks S1/S2/D1–D4, 6/6 PASS, two controls verified red; CL304, `open`, `quantitative`, `falsifier: stated`.)

### Group F — Thermodynamics and baryogenesis

#### 20.2.19 F360 — horizon thermodynamics independently reproduces the Friedmann pair; K1 stays QUANT with a sharper residual

Re-examining the completeness rubric's own K1 grade — "solved WITH the model's source, not derived
FROM the lattice" — finds that F284's conformal-mode reading answers a different question
(ontology) than K1 asks (dynamics): F182/F188 still *posit* the covariant field equation and solve
it, and F284 never changes that. A genuinely independent route exists: a Jacobson (1995)/Cai–Kim
(2005) horizon-thermodynamics argument at the cosmological apparent (Hubble) horizon, built from
three more primitive ingredients the model already owns — a horizon temperature from the causal
structure ($c_\text{grav}=c_\text{lat}$, F180, no new input), a horizon entropy $S=A/4G$ with the
model's own induced $G$ (F79), and the Clausius relation $\delta Q=T\,dS$ applied to the energy
flux $(\rho+p)$ crossing the horizon — reproduces F182/F188's exact Friedmann pair by sympy-exact
symbolic derivation, **never writing down or solving $G_{\mu\nu}=8\pi G\,T_{\mu\nu}$**. This never
promotes the rubric grade: the quasi-static approximation this route's simple form rests on is
shown, in closed form, to be an $O(1)$ *convention* rather than a controlled small-parameter
expansion (the dropped term is exactly $-3(1+w)/4$ relative — order unity for both matter and
radiation, vanishing only for $\Lambda$'s $w=-1$), and the entropy coefficient $S=A/4G$ needed to
make the route quantitative is presently *disputed by the model's own two computations of it*
(F79's induced $G$ vs. F355's BCC vacuum-entanglement calculation, disagreeing by a bracketed
factor $[0.79,3.18]$, hostage to a fermion-doubling convention). What the finding delivers instead
is a sharper, better-named residual: a genuine second derivation route to the exact same Friedmann
pair, and a precise diagnosis of the two harder problems (a nonlinear/nonperturbative extension of
F79/F180's induced self-energy, or the fully local Jacobson construction rather than the FRW-global
apparent-horizon shortcut) that would actually promote K1.

$$\boxed{\;\text{horizon-thermodynamics Clausius relation reproduces F182/F188's exact Friedmann pair (sympy-exact), never solving the covariant field equation; quasi-static step is }O(1)\text{, not small (closed-form }-3(1+w)/4\text{); K1 stays QUANT, entropy coefficient hostage to the live F79/F355 tension\;}\tag{R20.19}$$

(F360, checks Q1/Q2, 2/2 PASS; CL299, `open`, `exact`, `falsifier: stated`.)

#### 20.2.20 F364 — a real Boltzmann computation of baryogenesis, replacing a Sakharov checklist with an actual number

Turning F202's conditions-satisfaction check (below) into an actual magnitude, F364 builds a
leading-order resonant-leptogenesis Boltzmann/QKE computation using the model's own F201 heavy
sterile-neutrino texture masses ($M_2\approx0.40$ GeV, $M_3\approx5.60$ GeV — an order-unity split,
$r\approx1.73$) and a Casas–Ibarra Yukawa matrix fit to measured neutrino oscillation data. Two
scans quantify the two free residuals F202 had only named. **The free CP phase alone**, at the
model's own native masses, peaks the baryon-to-entropy ratio at $\sim2\times10^{-11}$ of the
observed value, then collapses under washout as the phase grows further — **10–11 decades short**
even pushed to the edge of perturbativity. **The $N_{2,3}$ mass-splitting resonance alone** (fixed
small perturbative Yukawa) *can* match the observed asymmetry, but only in a window
$\Delta M/M\in[3.2\times10^{-18},2.7\times10^{-17}]$ — **sixteen to seventeen orders of magnitude
finer** than the order-unity split ($r\approx1.73$) the F201 texture actually delivers at the angle
that also produces the keV dark-matter sterile. The sphaleron B-violation rate, computed from the
model's own $\sin^2\theta_W=2/9$ (F320), confirms sphalerons are fast ($\Gamma_\text{sph}/H\approx
1.2\times10^{16}$) throughout the symmetric phase — condition 1's magnitude, not merely its
presence.

$$\boxed{\;\text{real Boltzmann computation on the model's own F201 masses: free CP phase caps 10-11 decades short of }Y_B^\text{obs}\text{; free }N_{2,3}\text{ degeneracy can match it, but only in a window }16\text{--}17\text{ orders finer than the texture's native }O(1)\text{ split; sphalerons confirmed fast on the model's own }\sin^2\theta_W\;}\tag{R20.20}$$

(F364, self-contained Boltzmann calculation, two independent scans; no separate claim card — carried by CL176 alongside F202.)

#### 20.2.21 F202 — the Sakharov conditions are structurally met; the asymmetry's magnitude is free

Asking whether the model's own intrinsic lepton-number violation can source the (much larger)
lepton asymmetry that resonant keV sterile-neutrino production needs (Chapter 16's dark-matter
mechanism; the connection to Chapter 22's dark sector is the reason this question was assigned
here rather than to either of those chapters), F202 certifies all three Sakharov conditions
against the model's own established structure, each owned by a different prior finding: **L
(B$-$L) violation is derived**, not posited — F47's Majorana mass step is anti-linear, the only
gauge-invariant mass a $Y=0$ singlet can carry in the Higgs-free construction. **C and CP
violation are available**: F53 established $C$ is maximal and that single-generation CP-exactness
is the *correct* one-generation answer, not a deficiency — with three generations (F75), the
lepton sector carries 1 Dirac + 2 Majorana phases, and the measured $\delta_\text{CP}\ne0$ is
consistent with (not derived from) this structure. **Out-of-equilibrium and B-violation are
present**: the same $N_{2,3}$ sterile sector never thermalizes (feeble Yukawas), and $SU(2)_L$
sphalerons supply the L$\to$B conversion. One heavy sector — the F201 texture's $N_{2,3}$ states —
therefore does double duty, sourcing both the baryon asymmetry and the $\sim10^6\times$ larger
late lepton asymmetry the resonant-production mechanism needs (the standard $\nu$MSM/ARS
unification, not a coincidence, since the two asymmetries freeze at very different epochs and
never mix). What is explicitly **not** derived, and F364 (above) is what turns this honesty into
a number: the CP-phase values and the $N_{2,3}$ degeneracy that set the magnitude are free,
inherited residuals — the dark-matter-sector counterpart of the single $\Omega_\Lambda$
coincidence Chapter 21 will address for dark energy.

$$\boxed{\;\text{all three Sakharov conditions structurally present, each owned by a distinct prior finding (F47, F53/F75, F41); one heavy sector does double duty for baryogenesis and the DM-production lepton asymmetry (}\nu\text{MSM/ARS); the asymmetry's magnitude is a free, inherited residual, quantified by F364}\;}\tag{R20.21}$$

(F202, checks §Condition 1–3, 5/5 PASS; CL176, `narrowed`, `bracketed`, `falsifier: stated`, shared with F364/F201/F47/F53/F320.)

## 20.3 Results table

| # | Statement | Exactness class | Test record | Claims-index status |
|---|---|---|---|---|
| R20.1 | Friedmann acceleration eq. forced to $\rho+3p$ (Bianchi); radiation mis-weighted $2\times$ by the demoted energy-only law | exact (A1/A2) / numeric (N1-N4) | F182; `test_F182_friedmann_pressure.py` (6/6) | CL161 `live` |
| R20.2 | $z_\text{eq}=3433$, $z_\text{acc}=0.63$, age $=13.79$ Gyr | quantitative | F188; `test_F188_lcdm.py` (3/3) | CL164 `live` |
| R20.3 | expansion $=$ conformal mode of $K$; $\dot G/G\equiv0$ exact; $H_\text{max}=3^{-3/4}M_\text{Pl}$, $t_\text{min}=\sqrt3$ ticks (native) | exact (epoch scales, native units) / interpretive (ontology) | F284; `test_F283_F284_lattice_elasticity.py` (6/6) | CL242 `open` |
| R20.4 | tick-duration $\sqrt3$ discrepancy resolved (F284 SI-conversion error, corrected $t_\text{min}=a/c=6.5978\,t_P$); curvature-ceiling $24^{1/4}$ fork logged as Gap G-12 | resolved (a) / open (b) | — (this chapter's own derivation, §20.2.4) | — |
| R20.5 | inflation obstruction $r=\sqrt3$ scale-invariant under any lattice stretch, exactly | exact (E1) / quantitative (E2-E4) | F283; `test_F283_F284_lattice_elasticity.py` (8/8) | CL241 `open` |
| R20.6 | no compact field direction can slow-roll; every escape route closed | exact (obstruction, closed forms) / quantitative (escape-route margins) | F282; `F282-inflaton-candidate-slowroll` (gate, 7/7) | CL240 `open` |
| R20.7 | no-go re-verified after one month; axion monodromy and torsion/DBI closed | analysis / re-verification | F363; no test record (analysis-only) | CL240 (shared) |
| R20.8 | $P_\rho\propto k^{n_s}$; generic measures $n_s=0,4$; scale-free-in-metric $n_s=1$ excluded $8.4\sigma$ | exact (Poisson bridge, block-spin) / structural (measure classification) | F285; `F285-initial-condition-measure` (gate, 7/7) | CL243 `open` |
| R20.9 | length scales excluded by shape; log class predicts $dn_s/d\ln k=-2.62\times10^{-4}$; $\delta^*/2\pi$ coincidence rejected | exact (T1) / computed (T2-T5) | F286; `F286-second-scale-classification` (gate, 7/7) | CL244 `open` |
| R20.10 | $p{=}0$ is a scale-free anomalous dimension $\gamma$; no second scale needed; $g_\text{eff}$ vs $2/9$ a target, not a derivation | exact (A1-A2) / computed (A3-A4) | F295; `F295-tilt-is-an-anomalous-dimension` (gate, 8/8) | CL248 `open` |
| R20.11 | HC retrodiction validates F286 T1 ($2.92\sigma$ vs published $2.2\sigma$); naive dual $r$-exclusion $9$-$27\times$ | computed (L2, L5) / external citation (L3-L4) | F296; `F296-holographic-anomalous-dimension` (gate, 7/7) | CL249 `open` |
| R20.12 | no 3D dual needed ($t{=}0$ IS a 3D measure); $\gamma\equiv y-1$ identically; $n_t=2$ exact, $r\sim10^{-118}$ | exact (C1-C4, C6-C7) / computed (C5, C8) | F310; `F310-critical-measure` (gate, 16/16) | CL267 `contingent` |
| R20.13 | $\mu=\Sigma=1$ exactly (3 sources); $\gamma_g=6/11$; DES Y6 falsifier at $3.00\sigma$ | exact (S1-S2, D1-D2) / quantitative (D3-D5, B1-B2) | F288; `F288-structure-formation-growth` (gate, 13/13) | CL254 `live` |
| R20.14 | $g_*(10\text{ MeV})=10.7493$ from the model's own content; branch-odd term $=3/7$; $m_{E_g}>125.5$ MeV bound | exact (closed forms, angular means) / quantitative (content, bound) | F309; `F309-gstar-model-content` (gate, 14/14) | CL266 `live` |
| R20.15 | light elements $\lesssim1\%$; $N_\text{eff}=3.044$; BBN measures $\Delta m=1.293\pm0.0056$ MeV | quantitative (network) / structural ($N_\text{eff}$) | F297; `F297-bbn-light-elements` (gate, 12/12) | CL258 `contingent` |
| R20.16 | $A{=}7$ rate-fit repair; Li7/H $-92\%\to-6.3\%$ | quantitative | F361; `F361-bbn-a7-repair` (gate, 13/13) | CL258 (updated) |
| R20.17 | EM/strong terms confirmed independently; theory-aware significance $0.77$-$1.97\sigma$, not excluded | external citation (BMW, TWY, PDG) / computed (significance) | F372; `F372-npsplit-theory-uncertainty` (gate, 15/15) | CL259 `narrowed` |
| R20.18 | model-native sound horizon $-0.114\%$; Saha $z_\text{rec}$ reproduces $\sim26\%$ known bias; $\sigma_8$ residual localized | exact (S1-S2) / quantitative (D1-D4) | F369; `F369-transfer-function-scoping` (gate, 6/6) | CL304 `open` |
| R20.19 | horizon thermodynamics reproduces Friedmann pair exactly, without solving the field equation; K1 stays QUANT | exact (Q1-Q2 derivation) / interpretive (grade) | F360; `F360-horizon-thermodynamics-frw` (battery, 2/2) | CL299 `open` |
| R20.20 | Boltzmann baryogenesis: CP phase 10-11 decades short; degeneracy needs $10^{-17}$-level tuning | quantitative (two independent scans) | F364; `test_F364_baryogenesis_boltzmann.py` | CL176 (shared) |
| R20.21 | all three Sakharov conditions structurally met; magnitude free, quantified by F364 | structural (per-condition) | F202; `test_F202_leptogenesis_sakharov.py` (5/5) | CL176 `narrowed` |

## 20.4 Comparison with measurement

**BBN light-element abundances.** $Y_p=0.24494$ vs. Aver et al. 2021's $0.2453\pm0.0034$
($-0.11\sigma$ using the measured $\Delta m$); D/H $=2.4726\times10^{-5}$ vs. Cooke et al. 2018's
$(2.527\pm0.030)\times10^{-5}$ ($-1.8\sigma$); $^3$He/H matches a PRIMAT-class reference to
$2.5\%$; $^7$Li/H, after the F361 rate repair, matches to $-6.3\%$ (validated, previously excluded
at $-92\%$). $N_\text{eff}=3.044$ vs. Planck's $2.99\pm0.17$ ($+0.32\sigma$). The neutron-lifetime/
helium bound on $m_n-m_p$, evaluated against the model's own theoretical uncertainty rather than
the observable's precision (F372), moves from a naive $38.7\sigma$ exclusion to $0.77$–$1.97\sigma$
depending on how that uncertainty is composed — not excluded at any composition tried.

**Expansion history.** $z_\text{eq}=3433$, $z_\text{acc}=0.63$, age $=13.79$ Gyr — all matching
Planck 2018 to the precision the model's own inputs (measured density fractions) allow, since the
Friedmann pair itself is exact GR under the adopted source (R18.11).

**Primordial tilt.** $n_s=0.9649\pm0.0042$ (Planck 2018) is not derived by this model — the
inflation no-go (R20.6) forces the spectrum to be an automaton initial condition — but the
*character* of the tilt is sharply constrained: exact scale invariance is excluded at $8.4\sigma$
(the model's own scale-free measure would give $n_s=1$), the running $dn_s/d\ln k$ is measured
consistent with the model's own $\gamma$-identity prediction of exactly zero, and the identity
reading's tensor-spectrum prediction ($n_t=2$, $r\sim10^{-118}$) is not merely unfalsified by
BK18's $r<0.036$ but essentially unfalsifiable by any conceivable future measurement.

**Structure formation.** $\sigma_8=0.8204$ ($+1.15\%$ vs. Planck's $0.8111$); $S_8=0.8410$, at
$0.29\sigma$ from the combined-CMB baseline, $1.17\sigma$ from KiDS-Legacy 2025, but $3.00\sigma$
from DES Y6 — a live, genuinely falsifiable tension the model cannot accommodate by construction
(R20.13). $f\sigma_8$ against seven independent RSD points gives $\chi^2/N=1.012$.

**Baryogenesis.** The observed $Y_B=8.7\times10^{-11}$ is not reproduced by the model's own native
inputs under any single free-parameter choice tried: the CP-phase lever alone caps $10$–$11$
decades short, and the degeneracy lever needs a $\Delta M/M\sim10^{-17}$ tuning against a native
$O(1)$ split (R20.20).

## 20.5 What was excluded, and why

**Slow-roll inflation of any kind (F282/F283/F363).** Excluded by an exact, scale-free obstruction
tied to the BCC lattice's own coordination geometry ($r_\text{min}=\sqrt3=1/c_\text{lat}$), not by
a failed search: every compact field direction the model owns fails slow roll by $O(10)$, the
obstruction is provably invariant under any change to the lattice spacing (F283), and every
standard escape route — Starobinsky $R^2$, N-flation, the conformal mode, gauge phases, causal
seeds, axion monodromy, torsion/DBI kinetic enhancement — is closed either by an already-derived
finding or by the model's own field content lacking the necessary ingredient. This is a structural
no-go in the same category as F204 (Alcubierre warp) or F216 (massive spin-2 dark mode), not a
placeholder for "nobody has found one yet."

**An elastic (stretching) lattice (F283).** Excluded four independent ways: the inflation
obstruction is provably scale-invariant under any stretch (so elasticity buys nothing even if
permitted); $\dot G/G$ is independently bounded by LLR and BBN at $q\lesssim10^{-3}$ of a fully
comoving lattice; the only candidate "volume mode" is $\ln K$, already shown sourced,
potential-free, and non-propagating in vacuum (F79/F180/F216), with the alternative (a genuinely
new scalar) Cassini-bounded at a coupling $295\times$ weaker than gravity; and a tree-level elastic
stiffness would give gravity a second light cone, bounded by GW170817 at $\lesssim6\times10^{-15}$.

**The naive holographic-dual reading of the model's own field content (F296, superseded in
character but not in citation-worthiness by F310).** Reading the model's 48 Weyl fermions and 2
scalars as a holographic-cosmology dual's field content gives $r=0.32$–$0.97$, excluded by
BICEP/Keck at $9$–$27\times$. This is not carried forward as a live candidate; F310 shows the
model needs no dual at all, dissolving the question rather than answering it in the dual's own
terms.

**Baryogenesis as a "solved" sector (F202/F364).** Every Sakharov ingredient is present and
structurally derived or available, but neither of the two free residuals — the CP phase, the
$N_{2,3}$ mass-splitting — reaches the observed asymmetry on its own at the model's own native
values, and F364's Boltzmann computation makes this a quantified rather than a qualitative
statement.

## 20.6 What is still open

1. **The curvature-ceiling convention conflict (Gap G-12, §20.2.4b) is not resolved.** F183's
   static-object $K_\text{max}=1/a^4$ and F284's cosmology-implied $K_\text{max}=24/a^4$ remain
   two self-consistent conventions applied to two different physical regimes; no finding in
   either chapter derives that the model must have a single universal curvature ceiling, and
   this chapter, being documentation-only, cannot supply that derivation.
2. **The tilt's anomalous dimension has no computed value.** F310 reduces "which operator carries
   $\gamma$, and what is its value" to "one non-integer eigenvalue in a spectrum the repo already
   measures with machinery it already owns" — a genuinely smaller problem than where the chain
   started, but the eigenvalue itself is not computed anywhere in this chapter's twenty findings.
   The largest single residual named by F310 itself is whether the automaton's $t{=}0$ measure is
   actually critical at all — an inference from the observed power-law shape, not a derivation.
3. **F372's corrected significance is itself a range, not a single number** ($0.77$–$1.97\sigma$
   depending on how the theory uncertainty on $m_n-m_p$ is composed), and F372's own review pass
   explicitly withdrew the more comfortable single-figure framing its first draft used. The
   correct reading is "not excluded, with a margin uncertain by roughly a factor of two," not
   "comfortably safe."
4. **F369's transfer-function work replaces two scale-setting numbers, not the transfer
   function's shape.** The $\approx1.15\%$ $\sigma_8$ residual is localized away from the sound
   horizon but not closed — it sits in the still-imported EH98 acoustic-wiggle and
   Boltzmann-calibrated envelope functions, which need a full multipole Boltzmann hierarchy this
   chapter's sources explicitly scope as several sessions of work, not attempted here.
5. **The K1 horizon-thermodynamics route (F360) does not promote the rubric grade**, and its own
   numeric content (were it ever pursued further) is hostage to the live, unresolved F79/F355
   disagreement over the per-cell entropy coefficient in $S=A/4G$ — a tension this chapter
   inherits rather than resolves, exactly as Chapter 19 flagged it (its own §19.6.3, on a
   different observable).
6. **The $E_g$ doublet's mass is not derived anywhere in the tree** (F309's own honest limit),
   leaving its BBN-derived lower bound ($>125.5$ MeV) as a bound rather than a prediction, and
   leaving the model's own high-temperature $g_*$ plateau ($105.75$ or $107.75$, never the SM's
   $106.75$) as a discriminator with no computed value to discriminate against yet.
7. **DES Y6's $S_8$ tension is a live, unresolved falsification candidate for this model's
   gravity sector specifically** (R20.13): the field's own literature is split on whether the
   discrepancy is physical or systematic (photo-$z$, baryonic feedback), and this model has no
   screening mechanism with which to accommodate a confirmed physical tension if one emerges.

## 20.7 Falsifiers

From the relevant claim cards, reported at their actual status:

1. **CL242 (F284, $\dot G/G\equiv0$) carries `falsifier: unset`, `status: open`** — despite being
   arguably the chapter's cleanest single number (a genuine zero with no parameter to absorb a
   detection, already three orders inside the LLR bound), the claims layer has not yet formalized
   a falsifier statement for it; any measured $\dot G/G$ near $2H_0$ would falsify the rigid
   reading outright.
2. **CL240/CL241 (F282/F283, the inflation no-go and its scale-invariance) carry `falsifier:
   unset`, `status: open`**, despite F282/F283's own text naming concrete falsifiers (a scalar
   direction with $J\ge780$; a non-compact field direction; a derived $R^2$ coefficient
   $\gtrsim10^8$; a super-horizon-coherent causal mechanism) — the claim cards have not yet been
   updated to carry them formally.
3. **CL254 (F288, structure formation) carries `falsifier: stated`, `status: live`**: the DES Y6
   $S_8$ tension is the sharpest live candidate, since the model's $\mu\equiv1$ construction gives
   it no screening mechanism to accommodate a confirmed physical discrepancy.
4. **CL267 (F310, the anomalous-dimension identity) carries `falsifier: stated`,
   `status: contingent`**: a block-spin computation with fluctuation corrections that still
   returns exactly $\lambda_\sigma=b^1$ would remove $\gamma$'s only known home in the model; a
   detection of $r>10^{-10}$ would kill the identity reading outright, since it predicts
   $\sim10^{-118}$ with no parameter to move.
5. **CL258 (F297/F361, BBN) carries `falsifier: stated`, `status: contingent`**: any renormalizable
   $\nu_R$ coupling (excluded at $>10\sigma$ via $\Delta N_\text{eff}=1.71$) would falsify the
   model's own hypercharge/Majorana structure on a completely independent observable from the one
   that established it.
6. **CL259 (F372, the corrected $m_n-m_p$ significance) carries `falsifier: stated`,
   `status: narrowed`**: a tightened, independently-verified theory uncertainty on $m_n-m_p$ below
   roughly $0.11$ MeV would re-open the exclusion the naive $38.7\sigma$ figure had claimed.
7. **CL176 (F202/F364, leptogenesis) carries `falsifier: stated`, `status: narrowed`**: a
   first-principles derivation of either the CP phase or the $N_{2,3}$ mass splitting from the
   model's own $O_h$/$E_g$ structure — closing either of F364's two quantified gaps — would move
   this from a conditions-satisfaction result to an actual prediction of $Y_B$.
8. **CL299 (F360, horizon thermodynamics) carries `falsifier: stated`, `status: open`**: a
   correct, sign-verified, fully local (Jacobson-style) re-derivation without the quasi-static
   convention, or a resolution of the live F79/F355 entropy-coefficient tension, would be the
   two routes to promoting K1 beyond its current grade.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $t_\text{min}$, $H_\text{max}$ | The earliest resolvable cosmological epoch (Hubble radius $=$ one cell); $H_\text{max}=3^{-3/4}M_\text{Pl}$, $t_\text{min}=\sqrt3$ ticks (native, exact), $=a/c=6.5978\,t_P$ (SI, corrected, §20.2.4a) | §20.2.3-20.2.4 |
| $r_\text{min}$ | The exact, scale-free inflation obstruction, $M_\text{Pl}^2/\Lambda_\text{UV}^2=\sqrt3=1/c_\text{lat}$ | §20.2.6 |
| $\gamma$ | The primordial tilt's anomalous dimension, $n_s-1\equiv-2\gamma$; identically the anomalous part of the model's own block-spin relevant eigenvalue, $\gamma\equiv y-1$ | §20.2.10, §20.2.12 |
| $g_*(T)$ | The cosmological relativistic degree-of-freedom count computed from the model's own 48 Weyl fields — **not** to be confused with F61's gravitating-Weyl-mode count of the same symbol in the induced-$G$ prefactor (Chapter 18) | §20.2.14 |
| $\mu(a,k)$, $\Sigma(a,k)$ | The two free functions of general modified-gravity structure-formation phenomenology, both fixed to exactly $1$ by three independent facts already established elsewhere in the tree | §20.2.13 |
| $\gamma_g$ | The linear growth-rate index, $f=\Omega_m^{\gamma_g}$; forced to $6/11$ exactly given $\mu=1$ | §20.2.13 |

---

*This chapter logs one new gap, [G-12] (§20.2.4b): the curvature-ceiling convention conflict
between F183's static black-hole-core convention ($K_\text{max}=1/a^4$) and F284's
cosmology-implied de Sitter ceiling ($K_\text{max}=24/a^4$) is genuinely unresolved from the two
findings' own content, and is recorded rather than forced closed. The companion tick-duration
$\sqrt3$ discrepancy Chapter 19 forward-flagged alongside it is resolved in the same section
(§20.2.4a): it is an arithmetic error in F284's own SI-unit conversion, corrected here using
F107's own established $\tau=a/(c\sqrt3)$ and the identity $t_\text{min}/t_P=a/\ell_P$. No finding,
claim card, module, or test record was created or modified in the writing of this chapter.*
