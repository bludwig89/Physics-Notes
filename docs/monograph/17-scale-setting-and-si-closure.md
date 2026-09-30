# Chapter 17 — Scale Setting and SI Closure: the Lattice Spacing, Mass-Scale Transmutation, $\sqrt\sigma/f_\pi$, and the SI Anchor

*Chapter 17 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from the nine
findings `00-plan.md` §2 assigns to this chapter — F83, F107, F112, F119, F123, F232, F233, F235,
F351 — all read in full, plus `docs/monograph/01-postulates-and-ontology.md` (whose own notation
table lists $a$ and $\tau$ as reserved symbols "set to 1 in lattice-native units... SI value is a
Chapter 17 result" — this is the chapter that discharges that promise for the whole monograph),
`docs/monograph/13a-colour-structure-and-confinement.md` / `docs/monograph/13b-dynamical-qcd-and-x1-saga.md`
(R13a.x/R13b.x, especially R13b.13/R13b.14/R13b.16/R13b.18, the $d_1$/scheme-conversion chain), and
`docs/monograph/14-hadrons.md` (its own §14.5.5 and R14.16, the F146 string-tension measurement this
chapter's $\sqrt\sigma/f_\pi$ discussion inherits). Checked against `docs/theory/key-decisions.md`'s
"Canonical SI ruler" entry (quoted here in full for the first time, rather than partial quotation, as
this is that decision's home chapter), `docs/theory/supersessions.yaml` record **S5** (read in full),
`claims-index.md` (CL008, CL011, CL106, CL204, CL205, CL206 — all read in full, front matter and body
text), and `docs/monograph/GAPS.md` (re-read immediately before writing; last entry **G-12**, from
Chapter 20, at first read — a second, immediate re-read right before appending found Chapter 24 had
concurrently claimed **G-13** in the interim, so this chapter's own gap below is numbered **G-14**).
This chapter is documentation-only; it logs one new gap, **G-14**, on a claims-layer bookkeeping
question it found while reading CL205.

## 17.0 What this chapter establishes, and its one-paragraph statement

Every chapter before this one has worked in lattice-native units ($a=1$, $\tau=1$, $\hbar=1$,
$c_\text{lat}=1/\sqrt3$) and reported its results as pure numbers or dimensionless ratios. This
chapter is where the model commits to an actual metre value for $a$ — **F107's adoption of
$a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=1.06638\times10^{-34}$ m**, selected over the only competing
candidate (F83's fermion-mass ceiling) by two independent observational gates — and then asks, as
precisely as the source material allows, *how many further numbers, beyond that one ruler, does the
model actually need from measurement to reach an absolute SI prediction for gravity, the hadron
spectrum, the lepton spectrum, and the electroweak scale?* The headline finding is that the mass
scale is not a free normalization knob sitting outside the theory: F233 shows the deepest
lepton-sector scale is *generated*, to within a factor of $\approx1.9$ across nineteen decades, by
QCD's own asymptotic freedom running from the rule-locked bare coupling at the lattice cutoff — with
zero additional free parameters — and that the residual left over is not a new, independent unknown
but the *same* single nonperturbative scheme constant ($d_1$) that the $\sqrt\sigma/f_\pi$
scale-setting ratio (F235) and the electroweak scale $v$ (F351) also reduce to, once each is
checked. This is a genuine reduction in the number of moving parts the model relies on — from what
looked, as recently as F119 (2026-06-09), like a hard, un-mechanized no-go, to a single named,
not-yet-computed integral. It is not, however, a completed closure: Chapter 13b's own later work
(F337, F350 — logged there as Gap **G-11**) found that a native computation of that same constant
does not yet land inside the bracket F233/F235/F351's $d_1\approx1.78$ figure assumes, and this
chapter states that tension plainly rather than quoting the $1.78$ figure as settled.

## 17.1 Inputs

**Postulates used.** P1 (discreteness — this chapter gives the discrete unit $a$ its first SI
number) and, indirectly, P6 (the chiral-$SU(2)$ mass mechanism, whose output the mass-scale
questions of §17.2.4–§17.2.7 are about).

**Prior results used.**
- Chapter 6's $c_\text{lat}=1/\sqrt3$ and the lattice lightcone $a/\tau=c\sqrt3$ (Option C, the
  convention F83's and F107's own maps use throughout).
- Chapter 13a/13b's colour-sector results: R13a.x's confinement/dielectric machinery (the
  $\sigma=2\pi v^2$ relation, F86/F88, that F235's confinement factor is built from) and, with the
  explicit caveat below, **R13b.13/R13b.14/R13b.16/R13b.18** — the $d_1$/scheme-conversion chain.
  **Gap [G-11] caveat, carried forward exactly as Chapter 13b's own text asks:** R13b.14 records the
  $d_1$ bracket $[1,\,7.980]$ (F280) as containing the value $1.773$ that F233/F235 use, but R13b.16
  records that a later, more direct native computation (F337, sharpened by F350) extrapolates the
  same quantity to $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\approx31$–$34$ — **outside that
  bracket by a factor of $\sim4$** — and that F350's own stated exhaustion condition for treating
  this as more than ordinary non-convergence has now fired, unresolved as of Chapter 13b's own
  build. This chapter therefore does **not** cite $d_1\approx1.78$ as a settled number; it cites the
  *qualitative* result (three apparently separate residuals collapse to one shared open constant)
  as the finding, and states the $1.78$ figure only as the value F233/F235/F351 computed under the
  bracket that was current at the time each was written, with the later tension named explicitly in
  §17.2.6 and §17.5.
- Chapter 14's R14.16 and its own explicit caveat (§14.5.5 and its "what was excluded" section):
  F146's string-tension measurement $\sqrt\sigma=0.42$ GeV, which F235's confinement factor uses,
  "runs on a 3D simple-cubic $SU(3)$ action" that `supersessions.yaml`'s **S21** record shows is
  blind to $\approx1/3$ of the curvature-carrying link content relative to the model's genuine BCC
  lattice, so $\sqrt\sigma$ itself "could shift by ~1/3-curvature-sized amount" on re-derivation.
  This chapter treats F235's $+12\%$ $\sqrt\sigma/f_\pi$ residual as a number carrying that
  systematic uncertainty, not as a number known to $+12\%$ precision in an absolute sense — see
  §17.6.
- Chapter 15's R15.30 (not R15.7, which is a different, unrelated result — the assignment brief's
  reference to "R15.7's electron-mass calibration point" does not match Chapter 15's own numbering;
  the calibration result this chapter connects to is **R15.30**, "electron is the worst mass anchor
  … $\tau$ is exactly $\delta$-stable … adopted as canonical anchor," F120/F121). R15.30/R15.32 are
  the direct upstream of this chapter's $N$ discussion (§17.2.4–17.2.5): the $\tau$-anchored
  normalization *is* $N\equiv m_\text{lat}(\tau)$, and R15.32's mechanism argument (the lepton scale
  tracks $\Lambda_\text{QCD}$ to $O(1)$ because the $E_g$ condensate has no independent coupling of
  its own) is the qualitative statement that F233 makes quantitative in this chapter.

**Free inputs consumed — the chapter's central count, stated precisely up front and re-derived in
§17.2.8.** As of the findings this chapter reports, reaching a full absolute-SI prediction across
gravity, hadrons, leptons and the electroweak sector from this model requires exactly **four**
externally-measured dimensionful numbers, not one:

1. **$G$** (equivalently $\ell_P=\sqrt{\hbar G/c^3}$) — pins $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$
   (F79/F107); this input is not special to this model — *any* theory needs one length/mass/time
   anchor to connect a dimensionless rule to SI units, and the model's own contribution is that the
   ratio $a/\ell_P$ is a parameter-free structural prediction rather than a further fitted number.
2. **$f_\pi=92.07$ MeV** (F123) — the one hadron/matter-sector anchor; without it the geometric cell
   alone places the hadron scale $\sim18$ orders above the GeV world (F119's hierarchy) and every
   hadronic result stays a dimensionless ratio.
3. **$m_\tau$** (equivalently $N\equiv m_\text{lat}(\tau)=5.54\times10^{-19}$, F119/R15.30) — the one
   lepton-sector overall-scale anchor; the lepton mass-ratio *shape* is entirely derived
   (Chapter 15, zero shape parameters) but the multiplicative scale on top of that shape is not.
4. **$v=246.22$ GeV** (equivalently $G_F$) — the electroweak scale, F351.

The chapter's central finding is that #2, #3 and #4's *residuals* — after everything each sector's
own exact structure already accounts for — are argued, with varying degrees of completeness, to be
the **same** single open number ($d_1$), which would reduce the true count of independent free
inputs from four to two ($G$ and $d_1$) if and when $d_1$ is computed from first principles and the
three collapse arguments are confirmed rather than merely checked to $O(1)$/factor-of-two accuracy.
This has **not** happened yet (§17.2.6, §17.6); the honest count today is four measured anchors,
with a documented, partially-checked, partially-unresolved case that three of them are secretly one.

## 17.2 The derivation

### 17.2.1 F83 — the mass-anchor route: a degeneracy, not a fix (the superseded candidate)

Before F107's adoption, the natural candidate for pinning $a$ was a measured fermion mass, via the
F46 rest-leg relation $\Omega_\text{rest}(m_\text{lat})=\arcsin(m_\text{lat})$ radians/tick and the
lattice lightcone $a/\tau=c\sqrt d$:

$$a=\sqrt d\,\arcsin(m_\text{lat})\,\bar\lambda_C,\qquad \bar\lambda_C=\frac{\hbar}{m_\text{phys}c}
\tag{$\triangle$, F83}$$

F83 shows this is **one equation in two unknowns** ($a$ and $m_\text{lat}$): a measured mass fixes
only the ray $a(m_\text{lat})$, not a point — an entire family of lattices spanning $a/\ell_P$ from
$10^{-8}$ to $10^{22}$ reproduces the electron mass exactly (F83 §2, T5). What the mass *does* fix
is an exact **ceiling**, tightest for the heaviest fermion:

$$\boxed{\;a_\text{max}(\text{top quark})=\sqrt d\,\tfrac\pi2\,\bar\lambda_C^\text{top}=3.11\times10^{-18}\text{ m}=1.9\times10^{17}\,\ell_P\;}\tag{R17.1}$$

— about 17 orders of magnitude above the Planck length, and (as later chapters will show) about 17
orders above the value the model actually adopts. F83's round-trip is exact to $2.5\times10^{-16}$
(machine precision); the ceiling is real, but it excludes almost nothing.

### 17.2.2 F232 — why no dimensionless observable could ever have closed the degeneracy

Before adopting a specific closing input, F232 proves *why* the natural second attempt — the
absolute light-deflection coefficient $\Delta\theta=4GM/(bc^2)$, flagged in earlier work as possibly
carrying a stray $\sqrt d$ that could break F83's degeneracy — fails, and fails for a structural
reason rather than a numerical accident. For the canonical dielectric $K=e^{2u}$ (Chapter 18's
F64), the straight-ray eikonal deflection coefficient is **exactly $-4$, a pure number, at every
field strength** (F107 L4a, sympy) and independent of $a$ over a 47-decade sweep (F232 T3). This is
an instance of a general theorem:

$$\boxed{\;\textbf{Theorem (F232).}\ \text{No lattice observable that is both dimensionless AND independent of a measured mass can pin the absolute cell size } a.\;}\tag{R17.2}$$

Any such observable is invariant under $a\to sa$ (with $\tau=a/(c\sqrt d)$ scaled to match, holding
$c_\text{lat}=1/\sqrt d$ fixed) — the factor-4 bending, PPN $\beta=\gamma=1$, the birefringence
coefficient, and $\sin^2\theta_W$ are all instances. Pinning $a$ requires an input carrying a length
or mass dimension: either a measured fermion mass (F83, which only supplies a ray) or a measured
*dimensionful gravitational coupling*, $G$. This is the theoretical justification for why F107's
route — the $G$-match, not lensing — is the only one that could have worked, and it closes F83's own
open follow-up #1 negatively (the light-deflection route to $a$ is degenerate, full stop).

### 17.2.3 F107 — the adopted canonical ruler and its two gates

The lattice spacing is adopted at F79's parameter-free value:

$$\boxed{\;a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.59782\,\ell_P=1.06638\times10^{-34}\text{ m},\qquad
\tau=\frac{a}{c\sqrt3}=2.05366\times10^{-43}\text{ s}\;}\tag{R17.3}$$

with $a/\ell_P=\sqrt{2\pi\eta g_*}\,d^{1/4}$, $\eta=\tfrac1{12}$ (the Sakharov-induced stiffness),
$g_*=48$ (the exact fermionic Weyl mode count), $d=3$ — every input to this ratio structural, none
of them fitted to the value of $a$ itself. F83's mass map is **demoted from anchor to consistency
check** (`supersessions.yaml` **S5**, `kind: demoted`, `demoted: [F83]`, `by: [F107, F79]`): every
PDG fermion still lands at $m_\text{lat}\ll1$ at this cell (electron $1.59\times10^{-22}$), and the
canonical $a$ sits $\sim16.5$ decades below F83's own top-quark ceiling — consistent, but not
selected by the mass constraint.

The adoption is gated on two independent campaigns, not asserted by fiat:

**L4 — absolute lensing (exact + numeric + lattice + $G$-match).** For $K=e^{2u}$, $u=GM/(rc^2)$
(F64's canonical dielectric, D-EM5), $\ln K=2GM/(rc^2)$ is exactly Coulombic, giving a straight-ray
bending coefficient $K_\text{bend}=-4$ symbolically at **every** field strength (L4a, sympy),
confirmed by mpmath quadrature (L4b) and by a full 3D FFT-Poisson lattice calculation returning
$3.92\approx4$ with the dielectric/rest-leg ratio exact to $7.7\times10^{-14}$ (L4c). Feeding the
adopted $a$ through $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ gives:

$$\boxed{\;G_\text{pred}=6.674300\times10^{-11}\text{ m}^3\text{kg}^{-1}\text{s}^{-2}\quad
(\text{CODATA residual }3.0\times10^{-8}),\qquad \Delta\theta_\odot=1.751190''\quad
(\text{residual }3.0\times10^{-8})\;}\tag{R17.4}$$

**GRB gate — the observational discriminator between the two candidate anchors.** The physical
photon (Chapter 8's paired-spinor construction) is exactly non-birefringent, so the polarimetry
channel clears at any $a$; the surviving discriminating channel is the even-law $n{=}2$
time-of-flight scale, $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$ (from F30's exact even dispersion law):

| anchor | $a$ | $E_{\text{QG},2}$ | vs. LHAASO $7.0\times10^{11}$ GeV | verdict |
|---|---|---|---|---|
| **F79/F107 (adopted)** | $1.066\times10^{-34}$ m | $1.36\times10^{19}$ GeV $=1.11\,E_P$ | clears by $1.9\times10^7$ | **clears** |
| F83 top-quark ceiling | $3.11\times10^{-18}$ m | $466$ GeV | $6.7\times10^{-10}$ of bound | **excluded** |

$$\boxed{\;\text{The GRB gate observationally discriminates the two candidate anchors by }\sim16\text{ decades of margin, excluding the F83 ceiling and clearing the F107 value}\;}\tag{R17.5}$$

### 17.2.4 F112 — the SI prediction registry (18/18 PASS)

With $a$ fixed, every dimensionless lattice output becomes an absolute SI number. F112 evaluates 18
such outputs across five sectors — lattice scales, gravity, photon/Lorentz-invariance, electroweak
(dimensionless, $a$-independent but reported for completeness), and the gravity sourcing
coefficient — tagging each **PREDICTION** (parameter-free), **CONSISTENCY** (the model cannot be
wrong here without breaking GR/QM), or **FALSIFIER** (a one-sided bound). All 18 pass; the full
registry is reproduced in §17.3/§17.4 below.

### 17.2.5 F119 — the kilogram is already tied in; the open number is one dimensionless ratio, $N$

With $\{a,\tau\}$ fixed, the kilogram is discharged as a *unit* with no additional free knob: the
map $m_\text{phys}c^2=\hbar\arcsin(m_\text{lat})/\tau$ turns any dimensionless $m_\text{lat}$ into a
definite kg through $\hbar$ (J·s = kg·m²/s), using the same $\{c,\hbar,G\}$ triple that already fixed
the metre and second. The genuine open item is the single dimensionless normalization tying the
condensate's own units (which pin the $\tau$-generation constituent at $m^\text{cond}_\tau\equiv1$,
Chapter 15's saturation-wall result) to the physical $\tau$ rest-leg:

$$N\equiv\frac{m_\text{lat}(\tau)}{m^\text{cond}_\tau}=m_\text{lat}(\tau)=5.54\times10^{-19}.$$

F119 shows this factorizes cleanly out of the derived shape ($m_\text{lat}(a)=N\cdot m^\text{cond}_a$
to $4\times10^{-7}$ for $\mu,e$) and then tries three closure routes, each closing negatively at the
time of writing (2026-06-09):

$$\boxed{\;\text{R17.6 — Route 1 (NJL gap mechanism): a sharp no-go.}\ \text{The 3D contact-NJL gap equation is a mean-field power-law transition } (M\sim(g-g_c)^{1/2},\ p=1.95),\text{ requiring tuning }\Delta g/g_c\sim N^2\approx2.8\times10^{-36}\text{ to reach }N\text{ — no dynamical-transmutation channel found at the time}\;}$$

$$\boxed{\;\text{R17.7 — Route 2 ($W$/brake localization): }\lambda_6=0.243=O(1)\text{ localized (F118), but its exact value remains fitted, not derived; the rotor conjecture }\lambda_6=\tfrac14\text{ predicts the angle to }+0.63°\text{, suggestive but not exact}\;}$$

$$\boxed{\;\text{R17.8 — Route 3 (gravity): consistent, not closing.}\ G\text{ to }3\times10^{-8}\text{ and every fermion at } m_\text{lat}<1,\text{ but the adopted } a \text{ sits }\sim16.5\text{ decades below the top-quark ceiling — gravity pins }a,\text{ not the mass scale }N\;}$$

F119's own summary was blunt: "$N$ *is* the fermion-mass hierarchy" — at the time, apparently a
genuinely free number.

### 17.2.6 F233 — F119's no-go superseded: QCD asymptotic freedom transmutes $N$

Three weeks after F119, F233 identifies the channel F119's Route 1 diagnosis said was needed (a
logarithmically-running/marginal coupling) as **already built and already published**: F144's QCD
asymptotic-freedom chain, which F119 (2026-06-09) did not cross-reference against its own
"non-running couplings" verdict — that verdict (F115) applies to the electroweak angle across the
desert, not to the colour coupling, which *does* run the whole desert. The rule fixes, with zero
knobs, $\alpha_s(\mu_0)=g_s^2/(4\pi)=1/(16\pi)=0.019894$ at $\mu_0=\hbar c/a=1.8504\times10^{18}$ GeV;
running down in standard $\overline{\rm MS}$:

$$\boxed{\;N_\text{pred}=\Lambda_{\overline{\rm MS}}^{(3)}/\mu_0=2.86\times10^{-19}\ (\text{4-loop converged}),\qquad
\frac{N_\text{pred}}{N_\text{F119}}=\frac{2.86}{5.54}=1.94\;}\tag{R17.9}$$

$$\boxed{\;\text{The 19-decade hierarchy }N\approx5\times10^{-19}\text{ is generated by asymptotic freedom exponentiating an }O(1)\text{ coupling — the "}\sim10^{-36}\text{ tuning" objection is answered: there is no tuning}\;}\tag{R17.10}$$

The factor $1.94$ residual is identified, at the time F233 was written, as the single one-loop
matching constant $d_1$ (equivalently $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$,
compared with the Wilson action's notorious $28.81$ — i.e. the model's own rule normalization was
diagnosed as already $16\times$ closer to continuum than the standard lattice-QCD comparison point).
**This chapter does not repeat that $1.78$ figure as a settled number** (see §17.1's Gap-11 caveat
and §17.2.8/§17.5 below); what stands independently of the bracket dispute is the qualitative result
— the channel exists, is zero-parameter, and lands the hierarchy to a factor $\sim2$ across 19
decades — and F233's re-tagging of F119's Route 1 no-go from "closed, genuinely free" to
"transmutation-generated, residual is a named open constant."

### 17.2.7 F123 — matter-sector SI closure: the nucleon from one hadronic anchor

The geometric cell alone cannot reach the GeV world ($\hbar c/a=1.85\times10^{18}$ GeV, 18 orders
above it — F119's hierarchy again). F123 supplies the **one** further dimensionful input the strong
sector needs, $f_\pi=92.07$ MeV, and reads off the entire dimensionless NJL/RPA spectrum (already
fixed by Chapter 13/14's dimensionless couplings) as absolute MeV:

$$\boxed{\;m_c=309.5\text{ MeV (constituent)},\qquad m_p\simeq3m_c=928.5\text{ MeV}\quad(\text{PDG }938.27,\ -1.05\%)\;}\tag{R17.11}$$

$$\boxed{\;m_n-m_p=+1.51\text{ MeV}\quad(\text{PDG }+1.293\text{ MeV}, \ +0.22\text{ MeV})\text{ — needs NO QCD anchor: it is the F40 down–up current-mass gap beating the proton's larger EM self-energy}\;}\tag{R17.12}$$

This is F97 (Chapter 13/14) made quantitative — the nucleon mass *is* the dynamical (χSB)
constituent mass, not the $\sim1\%$ current-quark sum — and it resolves the P2 $m_p/\sqrt\sigma$
overshoot flagged in Chapter 14 as an artifact of a non-relativistic Cornell solve with a light
current quark. F123's own honest flag: the model carries **two** independent QCD calibrations
($f_\pi$ here, and $\sqrt\sigma$ used in the baryon three-body solve) and connecting them from first
principles — the $\sqrt\sigma/f_\pi\approx4.6$ ratio — was not yet done as of F123; that is exactly
F235's target.

### 17.2.8 F235 — $\sqrt\sigma/f_\pi$: the chiral factor is exact, the confinement residual is not removable, and it too is $d_1$

The ratio factorizes exactly:

$$\frac{\sqrt\sigma}{f_\pi}=\underbrace{\frac{\Lambda}{f_\pi}}_{7.037\ \text{(Pagels–Stokar, machine-exact)}}\times\underbrace{\frac{\sqrt\sigma}{\Lambda}}_{\text{confinement (open)}}.$$

$$\boxed{\;\text{R17.13 — the chiral half, }\Lambda/f_\pi=7.037,\text{ is machine-exact and closed; nothing in this chapter's residual discussion touches it}\;}$$

The entire $\sqrt\sigma/f_\pi\approx4.0$ (per-axis BZ convention) vs. empirical $4.56$ ($-12\%$)
residual lives in the confinement factor $\sqrt\sigma/\Lambda$. F235 checks whether any principled
BCC Brillouin-zone cutoff convention can close this gap and finds **no**: reaching $4.56$ needs
$\Lambda_\text{eff}=2.758/a$, which is **below** even the smallest principled cutoff (the per-axis
BZ edge, $\pi/a=3.14$) — the closest available convention, the per-axis edge itself, still misses by
$-12.2\%$:

$$\boxed{\;\text{R17.14 — no BCC-BZ cutoff convention closes }\sqrt\sigma/f_\pi\text{ to }<5\%;\text{ the residual is a genuine scale-setting factor, not a cutoff-convention artifact}\;}$$

F235 then identifies this residual as the *same* $d_1$ constant that F233's $N$-transmutation
residual and F154/F144-A4's $\alpha_s$-scheme residual reduce to — again subject to this chapter's
Gap-11 caveat about whether the specific $1.78$/bracket figure is currently well-determined
(§17.2.6, §17.5).

### 17.2.9 F351 — the electroweak scale $v$: not forced by $G$, not an independent gap either

F351 poses the question `open-derivations.md` had not asked directly: is $v=246.22$ GeV a *second*
dimensionful pin, analogous to $G$'s role for $a$, or is it forced by the same one? Two readings,
both closing negative, for different reasons:

**Reading 1 — mechanically false.** $G$'s structural equation, $1/G=2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3)$,
is one scalar equation in $\{a,G\}$; a symbolic free-symbol check (T1) confirms $v$ is not among its
free symbols. One equation, already saturated fixing one unknown ($a/\ell_P$), cannot also fix a
second, independent unknown.

$$\boxed{\;\text{R17.15 — }v\text{ is not, and cannot be, forced by }G\text{'s defining equation — a mechanical type-check, not a physics argument}\;}$$

**Reading 2 — not an independent gap either, but not yet proven to collapse.** Checking the two
known scale-generation mechanisms directly against $v$: (i) Sakharov/loop-induction (the same
mechanism that gave F79 its $1/G$, but from the fermion sea instead of the photon vacuum) supplies
only $0.16$–$0.36\%$ of $v^2$ (F143) — negligible; (ii) NJL-style dynamical transmutation is **not
absent**, correcting a stale reading of F119's "no channel" conclusion the same way F233 corrected
it for $N$ — the mechanism exists (F233's asymptotic-freedom channel), is live, and F351 flags $v$'s
residual as **plausibly, though not yet provably**, the same $d_1$ cluster that already owns $N$ and
the lepton brake $\lambda_6$ (F150).

$$\boxed{\;\text{R17.16 — Fermion-loop induction of }v\text{ is checked directly and found negligible (}\le0.36\%\text{); dynamical transmutation is live but unproven for }v\text{ specifically; the honestly-flagged, genuinely-untried mechanism is gauge-boson-loop induction (no finding computes it)}\;}$$

F351's own verdict, quoted directly because this chapter should not overstate it: "No number for $v$
is claimed... this finding documents *why*, not a closure." Ledger row E7/parameter #17 stays
`FIT (N=1)`.

### 17.2.10 The free-input count, assembled

Putting §17.1's four anchors and §17.2.4–17.2.9's collapse arguments together:

$$\boxed{\;\text{R17.17 — as measured today, the model needs FOUR independent dimensionful inputs for full SI closure: }G\text{ (}\to a\text{), }f_\pi\text{ (hadron scale), }m_\tau\text{ (equiv. }N\text{, lepton scale), and }v\text{ (electroweak scale)}\;}$$

$$\boxed{\;\text{R17.18 — three of those four (}f_\pi\text{'s residual after the chiral factor, }N\text{'s residual after asymptotic freedom, }v\text{'s residual after loop-induction) are ARGUED, with varying completeness, to be the SAME single open constant }d_1\text{ — a documented, not-yet-confirmed reduction path from four inputs to two (}G\text{ and }d_1\text{)}\;}$$

This is the chapter's answer to "how many free numbers does this model actually have": **four in
current practice**, with an honest, partially-checked case (quantitatively verified to a factor of
$\sim2$ for $N$, checked-and-ruled-negligible for one of two mechanisms for $v$, and structurally
argued but numerically contested — Gap G-11 — for the $\sqrt\sigma/f_\pi$ residual) that the true
count may be **two**, pending a first-principles computation of $d_1$ that Chapter 13b's own later
findings (F337, F350) show has not yet converged to a specific value.

## 17.3 Results table

| # | Statement | Status | Exactness | Source |
|---|---|---|---|---|
| R17.1 | Fermion-mass ceiling on $a$: top quark gives $a\le3.11\times10^{-18}$ m ($1.9\times10^{17}\,\ell_P$); the mass anchor supplies a ceiling, not a value | degenerate route, superseded | exact (algebra), $2.5\times10^{-16}$ round-trip | F83 (5/5) |
| R17.2 | Scale-invariance theorem: no dimensionless, mass-blind lattice observable can pin $a$ | theorem (negative) | exact (sympy $K_\text{bend}=-4$) | F232 (5/5) |
| R17.3 | Canonical SI ruler adopted: $a=\sqrt{8\pi}\,3^{1/4}\ell_P=1.06638\times10^{-34}$ m, $\tau=2.05366\times10^{-43}$ s | adoption, parameter-free ratio | exact ($a/\ell_P$ structural) | F79/F107 |
| R17.4 | $G$-match: $G_\text{pred}=6.6743\times10^{-11}$ (CODATA $3.0\times10^{-8}$); solar deflection $1.751190''$ (same residual) | PREDICTION | quantitative | F107 (6/6) |
| R17.5 | GRB gate discriminates F107 (clears by $1.9\times10^7$) from F83's ceiling (excluded by $\sim9$ decades) | FALSIFIER (gate) | quantitative | F107 (6/6) |
| R17.6–8 | F119's three closure routes for $N$: gap-mechanism no-go, $W$ $O(1)$-localized but fitted, gravity consistent-not-closing | partial (2026-06-09 state) | machine | F119 (8/8) |
| R17.9–10 | F233: QCD asymptotic freedom transmutes $N$ to a factor $1.94$ across 19 decades, zero free parameters; F119's no-go superseded | reclassification | machine ($<10^{-12}$ on the lock) | F233 (5/5) |
| R17.11 | Nucleon mass from one hadronic anchor ($f_\pi$): $m_p\simeq3m_c=928.5$ MeV vs. PDG $938.27$ ($-1.05\%$) | PREDICTION | quantitative | F123 (10/10) |
| R17.12 | $n$–$p$ splitting $+1.51$ MeV vs. $+1.293$ MeV, needs no QCD anchor | PREDICTION | quantitative | F123 (10/10) |
| R17.13 | $\sqrt\sigma/f_\pi$ chiral factor $=7.037$ (Pagels–Stokar) | exact, closed | exact | F235 (4/4) |
| R17.14 | No principled BCC-BZ cutoff closes the $+12\%$ confinement residual to $<5\%$ | honest negative | quantitative | F235 (4/4) |
| R17.15 | $v$ mechanically not forced by $G$'s defining equation | type-check (negative) | exact (symbolic) | F351 (5/5) |
| R17.16 | $v$'s residual: loop-induction negligible ($\le0.36\%$); transmutation live but unproven; gauge-boson-loop channel untried | scoping | machine (checked pieces) | F351 (5/5) |
| R17.17 | Four independent dimensionful inputs needed today: $G,f_\pi,m_\tau,v$ | tally | — | this chapter |
| R17.18 | Three of the four residuals argued (not proven) to reduce to one shared constant $d_1$ — contested by Chapter 13b's own later findings (Gap G-11) | open synthesis | contested | F233/F235/F351 + Ch.13b |

## 17.4 Comparison with measurement

This is the chapter where every lattice-native-unit result in the monograph acquires an SI number.
The canonical cell:

$$a=1.06638\times10^{-34}\text{ m}=6.59782\,\ell_P,\qquad \tau=2.05366\times10^{-43}\text{ s},\qquad
c_\text{lat}=1/\sqrt3,\qquad \hbar c/a=1.85\times10^{18}\text{ GeV}=0.15\,E_P.$$

The F112 registry's headline comparisons (18/18 PASS, all at this single $a$, no per-prediction
anchor choice):

| quantity | model | measured | residual | tier |
|---|---|---|---|---|
| Newton $G$ | $6.674300\times10^{-11}$ | $6.674300\times10^{-11}$ (CODATA) | $3.0\times10^{-8}$ | PREDICTION |
| solar light deflection | $1.751190''$ | $1.751190''$ (GR/VLBI) | $3.0\times10^{-8}$ | PREDICTION |
| bending coeff. $K_\text{bend}$ | $-4$ (all field strengths) | $-4$ (GR) | $0$ | PREDICTION |
| $E_{\text{QG},2}$ ($n{=}2$ ToF) | $1.360\times10^{19}$ GeV | $>7.0\times10^{11}$ GeV (LHAASO) | clears $\times1.9\times10^7$ | FALSIFIER |
| vacuum birefringence $\eta$ | $0$ (exact) | $<10^{-15}$ | cleared at any $a$ | PREDICTION |
| nucleon $m_p$ (one $f_\pi$ anchor) | $928.5$ MeV | $938.27$ MeV | $-1.05\%$ | PREDICTION |
| $n$–$p$ splitting | $+1.51$ MeV | $+1.293$ MeV | $+0.22$ MeV | PREDICTION |
| $\sqrt\sigma/f_\pi$ | $4.00$ (axis) | $4.56$ | $-12\%$ | quantitative (chiral half exact) |
| electroweak $v$ | $246.22$ GeV | (input, via $G_F$) | — | FIT (N=1), not yet reduced |

The Chapter 15/12 dimensionless comparisons (Koide $Q$, $m_Z/m_W$, $\sin^2\theta_W$) do not need $a$
and are reported in their home chapters; they belong to this chapter's report card only as
cross-sector context, not as new SI-closure results.

## 17.5 What was excluded, and why

- **F83's fermion-mass anchor.** Demoted from anchor to consistency check by `supersessions.yaml`
  **S5** (`kind: demoted`, `by: [F107, F79]`, `demoted: [F83]`). The mass map is exact and the
  degeneracy proof stands; it is excluded as the *primary* SI anchor specifically because it is one
  equation short (F83 §2) and because the GRB gate excludes its own natural ceiling region by
  $\sim9$ decades (R17.5) — not because anything in F83 is wrong.
- **F232's light-deflection route to a second, independent pin.** Excluded not by a numerical
  failure but by the general scale-invariance theorem (R17.2): the deflection coefficient is exactly
  $-4$ and dimensionless at every field strength, so it is structurally blind to $a$ by construction.
  This is a clean theoretical exclusion, not a near-miss.
- **The $d_1\approx1.78$ figure, as a settled input to this chapter's own reasoning.** F233 and F235
  both compute their residuals using the bracket $[1,\,7.98]$ (F280) current when each was written;
  Chapter 13b's own later work (F337, F350 — Gap G-11) found the native computation extrapolates
  outside that bracket by a factor of $\sim4$, with the exhaustion condition for treating this as
  more than non-convergence now fired. This chapter uses F233/F235/F351's *qualitative* collapse
  argument (three residuals, one shared constant) while explicitly declining to cite the specific
  $1.78$ number as settled — see §17.1 and §17.2.6.
- **F146's $\sqrt\sigma=0.42$ GeV as a precision input to F235's residual.** Chapter 14's own caveat
  (its §14.5.5/"what was excluded") that F146 runs on a pre-BCC simple-cubic gauge action, shown by
  `supersessions.yaml`'s **S21** to miss $\approx1/3$ of the curvature-carrying link content, is
  carried forward here: the $+12\%$ confinement-factor residual (R17.14) should be read as
  carrying that systematic, not as a number pinned to $\pm1\%$.

## 17.6 What is still open

1. **$d_1$ itself.** The single largest open computation this chapter inherits: a first-principles
   background-field calculation ($b_0=\tfrac{11}3C_A$ already exact; the finite digit gated by
   vertex form factors, the F162 programme) would close F233's $N$-transmutation residual, F235's
   $\sqrt\sigma/f_\pi$ residual, and (contingently) F351's $v$ residual simultaneously. As of this
   chapter's own sources, this computation has been attempted (F337) and re-attempted with the
   leading systematic hypothesis ruled out (F350), without landing inside the bracket the earlier
   findings assumed (Gap G-11, `docs/monograph/13b-dynamical-qcd-and-x1-saga.md` §13b.10).
2. **F235's $+12\%$ residual is confirmed not removable by any principled BCC cutoff convention**,
   and is further complicated by the F146 systematic (§17.5) — so the honest residual band is wider
   than $+12\%$, not narrower, until F146 is re-measured on the true BCC action.
3. **F351's gauge-boson-loop induction channel for $v$ is genuinely untried** — no finding checked
   for this chapter computes whether a lattice gauge-boson (rather than fermion) loop induces the
   electroweak wrap stiffness, which F351 itself names as the correctly-scoped next calculation
   (distinct from F143's already-checked, already-negligible fermion-loop channel).
4. **F351's $f_{E_g}(d_1)$ conjecture is stated but not proven** — that the lepton condensate's own
   phase stiffness depends on $d_1$ the same way the brake $\lambda_6$ does (F150) is a natural
   extension of the pattern, explicitly flagged by F351 itself as unproven rather than established.

## 17.7 Falsifiers

The adopted cell is not unfalsifiable — three live edges, all inherited directly from F107/F112:

$$\boxed{\;\textbf{The sharpest, already-active falsifier:}\ \text{any future subluminal }n{=}2\text{ time-of-flight bound above }1.36\times10^{19}\text{ GeV kills the adopted cell outright}\;}$$

quoted precisely from `docs/theory/key-decisions.md`'s own "Canonical SI ruler" entry: "falsification
handle: any $n{=}2$ time-of-flight bound above $1.36\times10^{19}$ GeV kills the adopted cell." The
current best bound (LHAASO GRB 221009A, $7.0\times10^{11}$ GeV) is seven decades short of this
threshold, so the falsifier is sharp in principle and far from being tripped in practice.

Two further, softer edges (F112 §4): (2) any confirmed vacuum-birefringence detection at the
polarimetry frontier would exclude the even-law paired photon this chapter's cell relies on (the
$\sigma$-bilinear counterfactual is already excluded, F66/F67); (3) any measured $G$ shift, or any
confirmed PPN deviation from $\beta=\gamma=1$, would break the canonical dielectric this chapter's
$G$-match depends on, since the model is GR-identical in the weak field and cannot be "slightly
wrong" there without contradiction.

Separately, and specific to this chapter's own free-input count: **if a future first-principles
computation of $d_1$ lands well outside the range that would make F233's factor-$1.94$/F235's
$-12\%$/F351's plausibility argument mutually consistent** — which is precisely the tension Chapter
13b's F337/F350 have already raised for the $\sqrt\sigma/f_\pi$ leg (Gap G-11) — the "three residuals,
one constant" reduction this chapter reports would itself be falsified, and the honest free-input
count would revert from the contingent two ($G$, $d_1$) to the confirmed four ($G$, $f_\pi$,
$m_\tau$, $v$) with no known relation between the last three.

---

> **Gap [G-14]** *(numbered G-14, not G-13, because Chapter 24 — built concurrently — independently
> claimed G-13 for its own gap first; see `docs/monograph/GAPS.md`'s "Chapter 24" entry).*
> `claims-index.md` lists **CL205** (F233's own claim card) as `status: withdrawn`,
> `kind: no_go`. Reading CL205's own body text shows this status is *inferred*, not independently
> established — the card states plainly: "A supersession/withdrawal banner appears in this finding's
> header, which is why the card reads `withdrawn`." But `findings/F233-mass-scale-N-transmutation-supersedes-F119.md`'s
> own header, read in full for this chapter, carries **no** such banner: its status line reads
> "Reconciliation / reclassification — 5/5 checks PASS," with none of the `⚠` markers findings
> genuinely superseded elsewhere in this tree (e.g. F174, F176b) carry, and F233 appears in no
> `docs/theory/supersessions.yaml` record's `superseded:` list. Substantively, F233 is not
> withdrawn at all — it is cited approvingly and without qualification by `CL106` (which folds
> F233's result into its own `findings:` list and narrative update) and by this very chapter as one
> of its central results (§17.2.6, R17.9–R17.10). This is the same claims-layer bookkeeping-artifact
> pattern already found and logged for CL084/F89 (Gap G-6), Chapter 12's own gap (G-7), and
> CL160/F181 (Gap G-9) — a mechanical extraction/cross-reference error (the seeding pass appears to
> have matched on the word "supersedes" appearing in F233's own *title*, describing what F233 does
> to F119, not on any banner in F233's own header), not a genuine physics withdrawal. Not fixed here,
> as this chapter is documentation-only; flagged for whoever next touches CL205 to correct its
> `status` field to `live` (or equivalent), matching F233's own unambiguous, unbannered header and
> its unqualified use by CL106 and this chapter.

*Chapter 17 built 2026-09-17. Findings used: F83, F107, F112, F119, F123, F232, F233, F235, F351
(9/9, all assigned findings covered, none deferred). One new gap logged: G-14 (above, and appended
to `docs/monograph/GAPS.md`).*
